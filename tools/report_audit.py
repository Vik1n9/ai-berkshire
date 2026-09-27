#!/usr/bin/env python3
"""Report Audit Tool for AI Berkshire.

数据抽检工具：从研究报告中抽取15%的财务数据点，与可靠信源比对，
通过则准出，不通过则打回并说明原因。

Zero external dependencies — uses only Python stdlib.
Requires Python >= 3.7.

工作流程（Step 0–3，规范见 skills/financial-data.md「資料抽檢標準流程」）：
  Step 0 — 口径与出处检查（EPS 口径、推算值、具名引述、关系人科目）：
    python3 tools/report_audit.py lint --report reports/xxx.md

  Step 1 — 提取数据点：核心表每列本期值全数纳入，其余随机抽样15%：
    python3 tools/report_audit.py extract --report reports/xxx公司/深度分析/xxx.md \
      --must-section 核心財務資料 --seed 20260928

  Step 2 — Claude 对抽检清单中的每个数据点取数，填入 fetched_value。
            来源1必须是权威来源（SEC EDGAR / MOPS / 交易所 / 公司官网 IR 原始档），
            来源2可用第三方（stockanalysis / macrotrends / FinMind / Goodinfo）交叉验证。
            本仓库 reports/ 内的报告不得作为核验来源（循环验证）。
            深度分析、财报分析的 verdict 必须加 --require-official。

  Step 3 — 输入核验结果，输出准出/打回判决：
    python3 tools/report_audit.py verdict --results '[...]'

  一步完成（仅提取+打印抽检清单，不做网络验证）：
    python3 tools/report_audit.py extract --report reports/xxx公司/深度分析/xxx.md --dry-run
"""

import argparse
import json
import math
import os
import re
import sys
from decimal import Decimal, Context, ROUND_HALF_EVEN
from random import Random

_CTX = Context(prec=28, rounding=ROUND_HALF_EVEN)

# ---------------------------------------------------------------------------
# 数据点提取：从 Markdown 报告中识别财务数字
# ---------------------------------------------------------------------------

# 匹配模式：数字 + 单位，前面有上下文标签
# 例：收入：1,239亿元、PE 18.8x、毛利率 56%、市值 ~$5,670亿
_PATTERNS = [
    # 百分比
    (r'([\d,，\.]+)\s*%',                        '%',    'percent'),
    # 亿元/亿美元/亿港元
    (r'([\d,，\.]+)\s*亿(元|美元|港元|RMB|USD|HKD)?', '亿',    'hundred_million'),
    # 倍数 PE/PB/PS
    (r'([\d,，\.]+)\s*[xX倍]',                   'x',    'multiple'),
    # 万亿
    (r'([\d,，\.]+)\s*万亿',                      '万亿', 'trillion'),
    # 美元绝对值（B/T）
    (r'\$\s*([\d,，\.]+)\s*([BMT亿])',             '$',    'usd_abs'),
    # 纯整数（如市值、收入、用户数等，出现在表格 | 里）
    (r'\|\s*[~约]?\$?([\d,，\.]+)\s*\|',          '',     'table_num'),
]

_LABEL_RE = re.compile(
    r'(?P<label>[^\|\n：:]{2,25})[：:\s]+[~约]?\$?(?P<num>[\d,，\.]+)\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?'
)

_TABLE_ROW_RE = re.compile(
    r'\|\s*(?P<label>[^|]{1,40})\s*\|\s*[~约]?\$?(?P<num>[\d,，\.]+)\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?\s*\|'
)


def _clean_num(s: str) -> float:
    """把带逗号、中文逗号的数字字符串转为 float。"""
    s = s.replace(',', '').replace('，', '').strip()
    try:
        return float(s)
    except ValueError:
        return None


def _is_valid_label(label: str) -> bool:
    """判断标签是否是有意义的财务字段名，过滤噪声。"""
    label = label.strip()
    # 太短
    if len(label) < 2:
        return False
    # 纯数字或纯年份
    if re.fullmatch(r'[\d\s年季度Q]+', label):
        return False
    # 以符号/markdown标记开头
    if re.match(r'^[+\-\*#\|~\$>_`]', label):
        return False
    # 含有 markdown 粗体/代码标记
    if '**' in label or '`' in label or '__' in label:
        return False
    # 标签含有纯增速符号（如 +56%、-13% 单独作标签）
    if re.fullmatch(r'[+\-]?\d+(\.\d+)?%', label):
        return False
    # 常见无意义标签
    _SKIP = {'来源', 'sources', 'source', '说明', '注意', '备注', '数据来源',
             'n/a', '—', '-', '/', '合计', 'total', '单位', '趋势'}
    if label.lower() in _SKIP:
        return False
    return True


# 两列表格行：| 标签 | 数值 unit |（专为财务报告的 KV 表设计）
_KV_TABLE_RE = re.compile(
    r'^\|\s*(?P<label>[^|*\n]{2,40}?)\s*\|\s*[~约]?\$?(?P<num>[\d,，\.]+)\s*'
    r'(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT亿])?\s*[\|（\(]'
)

# 带标签的 KV 行：标签：数值 单位
_KV_LABEL_RE = re.compile(
    r'(?P<label>[\u4e00-\u9fa5A-Za-z][^\|\n：:*]{1,30})[：:]\s*[~约]?\$?'
    r'(?P<num>[\d,，\.]+)\s*(?P<unit>亿[元美港]?元?|万亿|[xX倍]|%|[BMT])?'
)


_CELL_NUM_RE = re.compile(r'[~约約]?\$?([\d,，\.]+)\s*(亿[元美港]?元?|億[元美港]?元?|万亿|兆|[xX倍]|%|[BMT])?')


def _is_noise_number(text: str, start: int, end: int, unit: str) -> bool:
    """判断 text[start:end] 的数字是否为非数据（年份、季度、月份、章节编号）。"""
    before = text[max(0, start - 2):start]
    after = text[end:end + 1]
    num = text[start:end]
    if unit:
        return False
    # 日期的月／日部分：2026-07、2026/09
    if re.search(r'(19|20)\d{2}[\-/]$', text[max(0, start - 5):start]):
        return True
    # 季度／半年／财年标签：Q2、H1、FY2027、第3季
    if re.search(r'(Q|H|FY|第)$', before, re.IGNORECASE):
        return True
    # 年份或日期：2026-07、2026/09、2026年、1Q26 前后
    if re.fullmatch(r'(19|20)\d{2}', num) and after in ('', '-', '/', '年', 'Q', 'q', ' ', '）', ')', '|'):
        return True
    # 月份、日期、区间：10-11月、7/28、9月
    if after in ('月', '日', '/', '-', '年') or re.match(r'[\-–]\d+月', text[end:end + 4]):
        return True
    # 章节编号：§9.3、见 9.3
    if re.search(r'(§|見|见)\s?$', before):
        return True
    return False


def _first_data_number(text: str):
    """返回单元格中第一个「数据型」数字 (value, unit)，跳过年份／季度／月份等噪声。"""
    for m in _CELL_NUM_RE.finditer(text):
        raw = m.group(1).strip('.，,')
        if not raw or not re.search(r'\d', raw):
            continue
        unit = (m.group(2) or '').strip()
        if _is_noise_number(text, m.start(1), m.start(1) + len(m.group(1).rstrip('.，,')), unit):
            continue
        val = _clean_num(raw)
        if val is not None:
            return val, unit
    return None, ''


def _parse_md_tables(lines: list) -> list:
    """解析 Markdown 中所有表格，返回 (row_label, col_header, value, unit, lineno, raw) 列表。"""
    results = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        # 检测表头行（含 | 且不是分隔行）
        if '|' in line and not re.match(r'^\|[\-\s\|:]+\|$', line):
            headers_raw = [h.strip().strip('*_').strip() for h in line.split('|')]
            headers_raw = [h for h in headers_raw if h]
            # 下一行应是分隔行
            if i + 1 < len(lines) and re.match(r'^\|[\-\s\|:]+\|$', lines[i+1].strip()):
                i += 2  # 跳过分隔行
                # 读数据行
                while i < len(lines):
                    dline = lines[i].strip()
                    if not dline or not dline.startswith('|'):
                        break
                    cells = [c.strip().strip('*_~').strip() for c in dline.split('|')]
                    cells = [c for c in cells if c != '']
                    if len(cells) < 2:
                        i += 1
                        continue
                    row_label = cells[0]
                    for col_idx, cell in enumerate(cells[1:], start=1):
                        col_header = headers_raw[col_idx] if col_idx < len(headers_raw) else f'列{col_idx}'
                        # 提取 cell 中的数字+单位
                        val, unit = _first_data_number(cell)
                        if val and val != 0 and val < 1e15:
                            results.append((row_label, col_header, val, unit, i + 1, dline))
                    i += 1
                continue
        i += 1
    return results


# 变化率栏（QoQ、YoY、pp、变化）：由基础数值推导，不列入必检章节的 100% 核验
_DERIVED_COL_RE = re.compile(r'QoQ|YoY|HoH|MoM|季增|年增|月增|變化|变化|差異|差异|偏差|pp', re.IGNORECASE)


def extract_data_points(md_text: str) -> list:
    """从 Markdown 报告中提取所有可识别的财务数据点。

    覆盖三类结构：
      1. 多列 Markdown 表格（最主要的来源）：(行标签 + 列标题) → 数值
      2. 带冒号的 KV 行：标签：数值 单位
      3. 加粗数字行：**数值** 单位

    返回 list of dict：
      {id, label, reported_value, unit, raw_text, line_number}
    """
    points = []
    seen = set()

    def _add(label, val, unit, lineno, raw, derived=False):
        label = re.sub(r'[\*_`]+', '', label).strip()
        if not _is_valid_label(label):
            return
        if val is None or val == 0 or val > 1e15:
            return
        # 过滤纯年份/季度
        if re.fullmatch(r'(20\d{2}|Q[1-4]|\d{4}\s*Q[1-4])', label.strip()):
            return
        key = f"{label}|{round(val,4)}|{unit}"
        if key in seen:
            return
        seen.add(key)
        points.append({
            'id': len(points) + 1,
            'label': label,
            'reported_value': val,
            'unit': unit,
            'raw_text': raw[:120],
            'line_number': lineno,
            'section': section_of[lineno - 1] if 0 < lineno <= len(section_of) else '',
            'derived': derived,
        })

    lines = md_text.split('\n')
    in_code = False

    # 每一行所属的最近标题（供 --must-section 分层抽样）
    # 记录完整标题路径（「一、核心數據速覽 > 1.1 損益表」），子标题下的数据也归属上层章节
    section_of = []
    stack = []
    for ln in lines:
        hm = re.match(r'^(#{1,6})\s+(.*)', ln.strip())
        if hm:
            level = len(hm.group(1))
            stack = [h for h in stack if h[0] < level] + [(level, hm.group(2).strip())]
        section_of.append(' > '.join(h[1] for h in stack))

    # --- 1. 多列表格 ---
    for row_label, col_header, val, unit, lineno, raw in _parse_md_tables(lines):
        # 跳过无意义行标签
        if not _is_valid_label(row_label):
            continue
        # 跳过无意义列标题（YoY增速列单独标注，不作为待核验数据）
        if col_header.upper() in ('YOY', 'YOY增速', '增速', '同比', '变化', '趋势', '说明', '备注'):
            continue
        # 评分／品质栏（1-5 分、★）不是财务数据
        if re.search(r'評分|评分|質量|质量|分數|分数|1-5|★', col_header):
            continue
        # label = "行标签 · 列标题"（若列标题是行标签的补充）
        if col_header and col_header != row_label:
            label = f"{row_label} · {col_header}"
        else:
            label = row_label
        _add(label, val, unit, lineno, raw,
             derived=bool(_DERIVED_COL_RE.search(col_header or '')))

    # --- 2. KV 冒号行 ---
    for lineno, line in enumerate(lines, start=1):
        stripped = line.strip()
        if stripped.startswith('```'):
            in_code = not in_code
            continue
        if in_code or stripped.startswith('> ') or re.match(r'^#{1,6}\s', stripped):
            continue
        if '|' in stripped:
            continue  # 表格已在上面处理

        for m in _KV_LABEL_RE.finditer(stripped):
            label = m.group('label')
            val = _clean_num(m.group('num'))
            unit = (m.group('unit') or '').strip()
            if _is_noise_number(stripped, m.start('num'), m.end('num'), unit):
                continue
            _add(label, val, unit, lineno, stripped)

    return points


def sample_points(points: list, ratio: float = 0.15, seed: int = None,
                  must_sections: list = None) -> list:
    """分层抽样：must_sections 标题（子字串匹配，含上层标题）下，每一列的「本期」值
    （该行第一个非变化率的数值）全数纳入；其余数据点随机抽取 ratio 比例（最少 3 个，最多 30 个）。"""
    must_sections = must_sections or []
    # 必检：章节内每一列的「本期」值（该行第一个基础数值），即报告最常被引用的标题数字
    must, seen_lines = [], set()
    for p in points:
        if p.get('derived') or p['line_number'] in seen_lines:
            continue
        if any(ms and ms in p.get('section', '') for ms in must_sections):
            must.append(p)
            seen_lines.add(p['line_number'])
    must_ids = {p['id'] for p in must}
    rest = [p for p in points if p['id'] not in must_ids]
    n = max(3, min(30, math.ceil(len(rest) * ratio)))
    n = min(n, len(rest))
    rng = Random(seed)
    sampled = must + rng.sample(rest, n)
    # 按行号排序，方便人工比对
    return sorted(sampled, key=lambda p: p['line_number'])


# ---------------------------------------------------------------------------
# 准出/打回判决
# ---------------------------------------------------------------------------

_TOLERANCE = 0.01   # 1% 容差


def _decimals(v: float) -> int:
    """报告值显示的小数位数（26.0 → 0，35.53 → 2）。"""
    txt = repr(float(v))
    if 'e' in txt or 'E' in txt:
        return 0
    frac = txt.split('.')[1].rstrip('0') if '.' in txt else ''
    return len(frac)


def _within_rounding(reported: float, fetched: float) -> bool:
    """官方值四舍五入到报告显示位数后是否与报告值一致。"""
    half = 0.5 * 10 ** (-_decimals(reported))
    return abs(abs(reported) - abs(fetched)) <= half + 1e-9


def _pct_diff(reported: float, fetched: float) -> float:
    """相对偏差 (absolute)。"""
    if reported == 0:
        return 0.0 if fetched == 0 else float('inf')
    return abs(reported - fetched) / abs(reported)


# ---------------------------------------------------------------------------
# 来源分类：权威来源 / 计算值 / 循环来源 / 第三方
# ---------------------------------------------------------------------------

# 权威来源：监理机关申报、交易所、公司官网 IR 原始档
_OFFICIAL_KEYS = (
    'sec.gov', 'edgar', 'xbrl', '10-k', '10-q', '8-k', '20-f', '6-k', 'def 14a', 'form 4',
    'mops', '公開資訊觀測站', '公开资讯观测站', 'twse', 'tpex', '證交所', '证交所', '櫃買', '柜买',
    'hkexnews', '披露易', 'cninfo', '巨潮', 'sse.com.cn', 'szse',
    'nasdaq.com', 'nyse.com',
    '官網', '官网', '官方', 'investor relations', 'investors.', '公司公告', '公司新聞稿', '公司新闻稿',
    'press release', 'earnings release', '營運報告', '营运报告', '法說會簡報', '法说会简报',
    '財報原文', '财报原文', '財務報告書', '财务报告书', '年報', '年报', 'annual report',
)
# 计算值 / 非数据点：不需要外部来源
_COMPUTED_KEYS = (
    'financial_rigor', 'three-scenario', '計算', '计算', '重算', '參數', '参数',
    '假設', '假设', '非數據點', '非数据点', '章節', '章节', '年份標籤', '年份标签',
)
# 循环来源：本仓库其他报告
_CIRCULAR_KEYS = (
    'reports/', '.md', '報告轉引', '报告转引', '本倉庫', '本仓库', '版報告', '版报告',
)
# 本仓库报告档名样式：{公司}-research-20260926、earnings-2026Q2、checklist-20260825、-thesis
_CIRCULAR_RE = re.compile(r'(research|earnings|checklist|management|news|industry|funnel)-(19|20)\d{2}|-thesis\b',
                          re.IGNORECASE)
# 明示「此类数据没有权威来源」（如分析师共识、法人预估）
_NO_OFFICIAL_MARK = '[第三方唯一]'


def classify_source(src: str) -> str:
    """返回 'official' | 'computed' | 'circular' | 'third_party' | 'none'。"""
    if not src:
        return 'none'
    low = src.lower()
    if any(k in low for k in _CIRCULAR_KEYS) or _CIRCULAR_RE.search(src):
        return 'circular'
    if any(k in low for k in _COMPUTED_KEYS):
        return 'computed'
    if any(k in low for k in _OFFICIAL_KEYS):
        return 'official'
    return 'third_party'


def official_check(item: dict) -> tuple:
    """检查单一抽检点的来源是否满足「至少一个权威来源、无循环来源」。

    返回 (ok: bool, reason: str)。
    """
    s1 = item.get('fetched_source', '') or ''
    s2 = item.get('fetched_source2', '') or ''
    classes = [classify_source(s1)]
    if item.get('fetched_value2') is not None:
        classes.append(classify_source(s2))
    if 'circular' in classes:
        return False, '引用本仓库报告作为核验来源（循环验证）'
    if 'official' in classes:
        return True, ''
    if 'computed' in classes:
        return True, ''
    if _NO_OFFICIAL_MARK in s1 or _NO_OFFICIAL_MARK in s2:
        return True, '标注为无权威来源的第三方数据'
    return False, '两个来源都不是权威来源（SEC/MOPS/交易所/公司官网）'


def render_verdict(results: list, report_name: str = "", require_official: bool = False) -> dict:
    """
    根据核验结果输出准出/打回判决。

    results: list of dict，每项包含：
      - id, label, reported_value, unit, fetched_value, fetched_source
      - (可选) fetched_value2, fetched_source2   ← 第二来源

    require_official=True 时，来源不含权威来源、或引用本仓库报告的数据点
    一律判为不通过（深度分析、财报分析必须开启）。

    返回：
      {
        'verdict': 'PASS' | 'FAIL',
        'pass_count': int,
        'fail_count': int,
        'total': int,
        'fail_items': [...],
        'summary': str,
      }
    """
    BOLD = '\033[1m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RESET = '\033[0m'

    print('=' * 70)
    print(f'{BOLD}报告数据抽检 — 准出/打回判决{RESET}')
    if report_name:
        print(f'报告：{report_name}')
    print('=' * 70)
    print()

    fail_items = []
    warn_items = []
    source_issues = []

    for item in results:
        label = item.get('label', '?')
        reported = float(item.get('reported_value', 0))
        unit = item.get('unit', '')
        fetched = item.get('fetched_value')
        source = item.get('fetched_source', '?')
        fetched2 = item.get('fetched_value2')
        source2 = item.get('fetched_source2', '')

        # --- 主来源比对 ---
        if fetched is None:
            # 没有提供核验值 → 跳过（不计入通过/失败）
            print(f'  ⬜ [{item["id"]:>2}] {label[:35]:35s} {reported:>12.2f} {unit}  →  [未提供核验值，跳过]')
            continue

        fetched = float(fetched)
        diff1 = _pct_diff(reported, fetched)

        # --- 第二来源比对（如有）---
        diff2 = None
        if fetched2 is not None:
            fetched2 = float(fetched2)
            diff2 = _pct_diff(reported, fetched2)

        # 判断：权威来源用「四舍五入到报告显示位数」比对（官方值是精确值，
        # 1% 容差会放过 1.78 vs 1.77、35.53% vs 35.54% 这类口径或抄录错误）；
        # 其余来源沿用 1% 容差
        if classify_source(source) == 'official':
            pass1 = _within_rounding(reported, fetched)
        else:
            pass1 = diff1 <= _TOLERANCE
        if diff2 is None:
            pass2 = True
        elif classify_source(source2) == 'official':
            pass2 = _within_rounding(reported, fetched2)
        else:
            pass2 = diff2 <= _TOLERANCE

        src_ok, src_reason = official_check(item)
        if not src_ok:
            source_issues.append({'id': item['id'], 'label': label, 'reason': src_reason,
                                  'line_number': item.get('line_number', 0)})

        if require_official and not src_ok:
            status = f'{RED}❌ 来源不合格{RESET}'
            detail = f'{source} / {source2 or "-"} → {src_reason}'
            fail_items.append({
                'id': item['id'], 'label': label, 'reported': reported, 'unit': unit,
                'fetched': fetched, 'source': source, 'fetched2': fetched2, 'source2': source2,
                'diff1_pct': round(diff1 * 100, 2),
                'diff2_pct': round(diff2 * 100, 2) if diff2 is not None else None,
                'raw_text': item.get('raw_text', ''),
                'line_number': item.get('line_number', 0),
                'source_reason': src_reason,
            })
        else:
            # 判定：权威来源不符 → 不通过（第三方相符也不能抵销）；
            #       只有一个来源且不符 → 不通过；
            #       两个非权威来源一符一不符、或权威相符但第三方不符 → 警告
            off1 = classify_source(source) == 'official'
            off2 = diff2 is not None and classify_source(source2) == 'official'
            if off1 or off2:
                official_bad = (off1 and not pass1) or (off2 and not pass2)
                outcome = 'fail' if official_bad else ('pass' if pass1 and pass2 else 'warn')
            elif diff2 is None:
                outcome = 'pass' if pass1 else 'fail'
            else:
                outcome = 'pass' if pass1 and pass2 else ('fail' if not pass1 and not pass2 else 'warn')

            detail = f'{source}: {fetched:.2f} (偏差 {diff1*100:.2f}%)'
            if diff2 is not None:
                detail += f'  |  {source2}: {fetched2:.2f} (偏差 {diff2*100:.2f}%)'
            if outcome == 'pass':
                status = f'{GREEN}✅ 通过{RESET}'
            elif outcome == 'fail':
                status = f'{RED}❌ 不通过{RESET}'
                fail_items.append({
                    'id': item['id'],
                    'label': label,
                    'reported': reported,
                    'unit': unit,
                    'fetched': fetched,
                    'source': source,
                    'fetched2': fetched2,
                    'source2': source2,
                    'diff1_pct': round(diff1 * 100, 2),
                    'diff2_pct': round(diff2 * 100, 2) if diff2 is not None else None,
                    'raw_text': item.get('raw_text', ''),
                    'line_number': item.get('line_number', 0),
                })
            else:
                status = f'{YELLOW}⚠️  警告{RESET}'
                warn_items.append({
                    'id': item['id'], 'label': label,
                    'reported': reported, 'unit': unit,
                    'diff1_pct': round(diff1 * 100, 2),
                    'diff2_pct': round(diff2 * 100, 2) if diff2 is not None else None,
                })

        print(f'  {status} [{item["id"]:>2}] {label[:35]:35s}  报告: {reported:>12.2f} {unit}')
        print(f'              {" " * 38}{detail}')

    print()
    print('-' * 70)

    total = len([r for r in results if r.get('fetched_value') is not None])
    fail_count = len(fail_items)
    warn_count = len(warn_items)
    pass_count = total - fail_count - warn_count

    print(f'  抽检总数: {total}  |  通过: {GREEN}{pass_count}{RESET}  |  警告: {YELLOW}{warn_count}{RESET}  |  不通过: {RED}{fail_count}{RESET}')
    print()

    if fail_count == 0:
        print(f'{BOLD}{GREEN}【准出】所有抽检数据通过，报告可发布。{RESET}')
        verdict = 'PASS'
    else:
        print(f'{BOLD}{RED}【打回】{fail_count} 个数据点核验不通过，报告需修正后重审。{RESET}')
        print()
        print(f'{BOLD}打回原因：{RESET}')
        for fi in fail_items:
            print(f'  ❌ 第 {fi["line_number"]} 行 | {fi["label"]}')
            print(f'     报告值：{fi["reported"]} {fi["unit"]}')
            print(f'     {fi["source"]}：{fi["fetched"]}  （偏差 {fi["diff1_pct"]}%）')
            if fi.get('fetched2') is not None:
                print(f'     {fi["source2"]}：{fi["fetched2"]}  （偏差 {fi["diff2_pct"]}%）')
            if fi.get('source_reason'):
                print(f'     来源问题：{fi["source_reason"]}')
            print(f'     原文：{fi["raw_text"][:80]}')
            print()
        verdict = 'FAIL'

    if warn_count > 0:
        print(f'{YELLOW}注意：{warn_count} 个数据点的第三方来源与报告不一致（权威来源相符或两个第三方来源分歧），可能是口径差异（GAAP/Non-GAAP、汇率、关系人科目），请人工复核。{RESET}')
        for wi in warn_items:
            print(f'  ⚠️  {wi["label"]}  报告:{wi["reported"]} {wi["unit"]}  偏差: {wi["diff1_pct"]}% / {wi["diff2_pct"]}%')

    if source_issues and not require_official:
        print(f'{YELLOW}来源提醒：{len(source_issues)} 个数据点缺少权威来源或引用本仓库报告（未开启 --require-official，不计入打回）：{RESET}')
        for si in source_issues:
            print(f'  ⚠️  第 {si["line_number"]} 行 | {si["label"]} → {si["reason"]}')

    print('=' * 70)

    return {
        'verdict': verdict,
        'pass_count': pass_count,
        'warn_count': warn_count,
        'fail_count': fail_count,
        'total': total,
        'fail_items': fail_items,
        'warn_items': warn_items,
        'source_issues': source_issues,
        'require_official': require_official,
    }


# ---------------------------------------------------------------------------
# 口径与出处检查（lint）：抽检前扫描已知的错误模式
# ---------------------------------------------------------------------------

_EPS_RE = re.compile(r'EPS|每股盈餘|每股盈余|每股收益', re.IGNORECASE)
_EPS_BASIS_RE = re.compile(r'基本|稀釋|稀释|diluted|basic|GAAP|估計|估计|預估|预估|共識|共识|指引|guidance|法人|\d{4}E\b',
                           re.IGNORECASE)
_DERIVED_RE = re.compile(r'推算|回推|估算')
_OFFICIAL_METRIC_RE = re.compile(r'營業現金流|營業活動現金流|經營現金流|经营现金流|OCF|資本支出|资本支出|CapEx|'
                                 r'週轉天數|周转天数|DSO|DIO|股本', re.IGNORECASE)
_BACKDERIVE_RE = re.compile(r'FCF\s*[+＋]\s*CapEx|自由現金流\s*[+＋]\s*資本支出|自由现金流\s*[+＋]\s*资本支出',
                            re.IGNORECASE)
_NAMED_QUOTE_RE = re.compile(r'[「“"][^」”"]{8,}[」”"]\s*[（(][\u4e00-\u9fa5A-Za-z·\s]{2,12}[）)]')
_QUOTE_SOURCE_RE = re.compile(r'http|法說|法说|電話會|电话会|逐字稿|新聞稿|新闻稿|\d{1,2}/\d{1,2}|\d{4}-\d{2}-\d{2}|年報|年报|10-[KQ]')


def lint_report(md_text: str) -> list:
    """扫描报告中的已知错误模式，返回 [(line_number, rule, message, text)]。"""
    issues = []
    lines = md_text.split('\n')
    in_code = False
    for n, line in enumerate(lines, start=1):
        st = line.strip()
        if st.startswith('```'):
            in_code = not in_code
            continue
        if in_code or not st:
            continue
        # L1 EPS 未标口径
        if st.startswith('|') and not re.match(r'^\|[\-\s\|:]+\|$', st):
            first = st.strip('|').split('|')[0]
            if _EPS_RE.search(first) and not _EPS_BASIS_RE.search(st):
                issues.append((n, 'L1', 'EPS 未标示口径（基本／稀释、GAAP／Non-GAAP）', st))
        # L2 官方通常已揭露的数字却用推算
        if _DERIVED_RE.search(st) and _OFFICIAL_METRIC_RE.search(st):
            issues.append((n, 'L2', '营业现金流／资本支出／周转天数／股本等官方通常已揭露，'
                                    '确认是否已查官方原始档；若官方有揭露不得用推算值', st))
        # L3 用公司自定义 FCF 回推
        if _BACKDERIVE_RE.search(st):
            issues.append((n, 'L3', '不得以公司自定义 FCF 加回资本支出推算营业现金流', st))
        # L4 具名引述缺出处
        if _NAMED_QUOTE_RE.search(st) and not _QUOTE_SOURCE_RE.search(st):
            issues.append((n, 'L4', '具名引述缺出处（连结、日期或法说场次）；无法核实的引述应删除', st))
    # L5 讨论应收周转天数却未交代关系人科目（仅台股报告：IFRS 台股报表常分列，美国 GAAP 通常不分列）
    text = md_text
    summed = re.search(r'(含|加總|合計|加总|合计|兩行|两行)\S{0,8}(關係人|关系人)|(關係人|关系人)\S{0,12}(加總|合計|加总|合计)',
                       text) or re.search(r'related[- ]part(y|ies).{0,40}(includ|sum|combin)', text, re.IGNORECASE)
    is_tw = re.search(r'新台幣|新台币|TWD|MOPS|公開資訊觀測站|公开资讯观测站|台股', text)
    if is_tw and re.search(r'DSO|應收帳款週轉|应收账款周转', text) and not summed:
        first_line = next((i for i, l in enumerate(lines, start=1)
                           if re.search(r'DSO|應收帳款週轉|应收账款周转', l)), 0)
        issues.append((first_line, 'L5', '讨论应收周转却未写明「应收帐款－关系人」是否已加总（须明写「含关系人」或「两行合计」）', lines[first_line - 1].strip()))
    return issues


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description='Report Audit Tool — 研究报告数据抽检工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
工作流程：

  Step 1 — 提取数据点并随机抽样 15%，输出抽检清单：
    python3 tools/report_audit.py extract --report reports/腾讯/腾讯-research-20260408.md

  Step 2 — Claude 对清单中每个数据点，从可靠信源取数，
            填入 fetched_value / fetched_source / fetched_value2 / fetched_source2

  Step 3 — 输入核验结果，输出准出/打回判决：
    python3 tools/report_audit.py verdict --results '[
      {"id":1,"label":"营业收入","reported_value":7518,"unit":"亿","fetched_value":7518,"fetched_source":"10-K FY2025 (SEC EDGAR)","fetched_value2":7500,"fetched_source2":"stockanalysis"},
      ...
    ]' --require-official

  --require-official：来源1/来源2 都不是权威来源（SEC/MOPS/交易所/公司官网），
    或引用本仓库报告（循环验证）的数据点判为不通过。深度分析、财报分析必须开启。
    分析师共识等本来就没有权威来源的数据，来源名称加注 [第三方唯一]。

  一步预览（只打印抽检清单，不核验）：
    python3 tools/report_audit.py extract --report reports/xxx公司/深度分析/xxx.md --dry-run

  指定抽样比例（默认0.15）：
    python3 tools/report_audit.py extract --report reports/xxx公司/深度分析/xxx.md --ratio 0.20

  固定随机种子（复现同一批样本）：
    python3 tools/report_audit.py extract --report reports/xxx公司/深度分析/xxx.md --seed 42
        """)

    sub = parser.add_subparsers(dest='command')

    # extract
    ext = sub.add_parser('extract', help='从报告提取数据点并随机抽样')
    ext.add_argument('--report', required=True, help='报告文件路径（Markdown）')
    ext.add_argument('--ratio', type=float, default=0.15, help='抽样比例，默认 0.15')
    ext.add_argument('--seed', type=int, default=None, help='随机种子（可选，用于复现）')
    ext.add_argument('--dry-run', action='store_true', help='只打印，不输出 JSON')
    ext.add_argument('--must-section', action='append', default=[],
                     help='该标题（子字串匹配）下每一列的本期值全数纳入抽检，可重复指定；'
                          '财报分析用「核心數據速覽」，深度分析用「核心財務資料」')

    # lint
    lnt = sub.add_parser('lint', help='抽检前扫描口径与出处问题（EPS 口径、推算值、具名引述、关系人科目）')
    lnt.add_argument('--report', required=True, help='报告文件路径（Markdown）')
    lnt.add_argument('--strict', action='store_true', help='有任何问题即以非零码退出')

    # verdict
    vrd = sub.add_parser('verdict', help='根据核验结果输出准出/打回判决')
    vrd.add_argument('--results', required=True, help='JSON 数组，含 fetched_value 等字段')
    vrd.add_argument('--report', default='', help='报告名称（可选，用于显示）')
    vrd.add_argument('--output-json', action='store_true', help='将判决结果以 JSON 输出到 stdout')
    vrd.add_argument('--require-official', action='store_true',
                     help='要求每个数据点至少一个权威来源且不得引用本仓库报告（深度分析/财报分析必开）')

    args = parser.parse_args()

    if args.command == 'extract':
        if not os.path.exists(args.report):
            print(f'❌ 文件不存在: {args.report}', file=sys.stderr)
            sys.exit(1)

        with open(args.report, 'r', encoding='utf-8') as f:
            text = f.read()

        all_points = extract_data_points(text)
        sampled = sample_points(all_points, ratio=args.ratio, seed=args.seed,
                                must_sections=args.must_section)

        print('=' * 70)
        print(f'报告数据抽检清单')
        print(f'文件：{args.report}')
        print(f'总提取数据点：{len(all_points)}  |  抽样比例：{args.ratio:.0%}  |  抽检数量：{len(sampled)}')
        if args.seed is not None:
            print(f'随机种子：{args.seed}（可用于复现同一批样本）')
        if args.must_section:
            n_must = sum(1 for p in sampled
                         if any(ms in p.get('section', '') for ms in args.must_section))
            print(f'必检章节：{"、".join(args.must_section)}（每列本期值 {n_must} 点全数纳入，其余随机抽样）')
            if n_must == 0:
                print('⚠️  必检章节未匹配到任何数据点，请确认标题文字')
        print('=' * 70)
        print()
        print(f'{"ID":>3}  {"行号":>5}  {"数据标签":<35}  {"报告值":>12}  {"单位"}')
        print(f'{"─"*3}  {"─"*5}  {"─"*35}  {"─"*12}  {"─"*6}')
        for p in sampled:
            print(f'{p["id"]:>3}  {p["line_number"]:>5}  {p["label"][:35]:<35}  {p["reported_value"]:>12.2f}  {p["unit"]}')
        print()
        print('↑ 请对上述每个数据点取数，填入 fetched_value（规范见 skills/financial-data.md）：')
        print('  来源1（权威，必查）：美股 SEC EDGAR / 公司 IR；台股 MOPS / 证交所 / 公司官网；')
        print('                       港股 HKEXnews；A股 cninfo / 交易所')
        print('  来源2（交叉验证）：  stockanalysis / macrotrends / FinMind / Goodinfo / aastocks / eastmoney')
        print('  禁止：以本仓库 reports/ 内报告作为核验来源（循环验证）')
        print()

        if not args.dry_run:
            # 输出可填写的 JSON 模板
            template = []
            for p in sampled:
                template.append({
                    'id': p['id'],
                    'label': p['label'],
                    'reported_value': p['reported_value'],
                    'unit': p['unit'],
                    'line_number': p['line_number'],
                    'section': p.get('section', ''),
                    'raw_text': p['raw_text'],
                    'fetched_value': None,       # ← 填入主来源核验值
                    'fetched_source': '',        # ← 填入主来源名称
                    'fetched_value2': None,      # ← 填入副来源核验值（可选）
                    'fetched_source2': '',       # ← 填入副来源名称（可选）
                })
            print('抽检清单 JSON（填入 fetched_value 后，传给 verdict 命令）：')
            print()
            print(json.dumps(template, ensure_ascii=False, indent=2))

    elif args.command == 'lint':
        if not os.path.exists(args.report):
            print(f'❌ 文件不存在: {args.report}', file=sys.stderr)
            sys.exit(1)
        with open(args.report, 'r', encoding='utf-8') as f:
            issues = lint_report(f.read())
        print('=' * 70)
        print(f'口径与出处检查：{args.report}')
        print('=' * 70)
        for n, rule, msg, txt in issues:
            print(f'  ⚠️  [{rule}] 第 {n} 行：{msg}')
            print(f'       {txt[:110]}')
        print('-' * 70)
        print(f'  共 {len(issues)} 项。逐项修正，或在报告中说明为何不适用，再进行抽检。')
        sys.exit(1 if (args.strict and issues) else 0)

    elif args.command == 'verdict':
        try:
            results = json.loads(args.results)
        except json.JSONDecodeError as e:
            print(f'❌ JSON 解析失败: {e}', file=sys.stderr)
            sys.exit(1)

        report_name = args.report or ''
        outcome = render_verdict(results, report_name=report_name,
                                 require_official=args.require_official)

        if args.output_json:
            print(json.dumps(outcome, ensure_ascii=False, indent=2))

        # 非零退出码表示打回，方便 CI/脚本判断
        sys.exit(0 if outcome['verdict'] == 'PASS' else 1)

    else:
        parser.print_help()


if __name__ == '__main__':
    main()
