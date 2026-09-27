#!/usr/bin/env python3
"""Report Audit Tool for AI Berkshire.

数据抽检工具：从研究报告中抽取15%的财务数据点，与可靠信源比对，
通过则准出，不通过则打回并说明原因。

Zero external dependencies — uses only Python stdlib.
Requires Python >= 3.7.

工作流程（规范见 skills/financial-data.md「資料帳本與驗算流程」）：
  帐本验算（公式重算、勾稽、来源、报告数字回对帐本）：
    python3 tools/report_audit.py ledger --report reports/xxx.md --must-section 核心財務資料 --require-official
  来源重取抽样（帐本原始值）：
    python3 tools/report_audit.py ledger --report reports/xxx.md --sample 0.2 --seed 20260928

  无帐本的报告（如产业研究）沿用下列抽检：
  Step 1 — 提取数据点：--must-section 章节全数纳入，其余随机抽样15%：
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
    # 年份：无单位的 19xx／20xx 且后面不接数字、小数点、千分位（2026-07、2027上半年、2027H2）
    if re.fullmatch(r'(19|20)\d{2}', num) and not re.match(r'[\d\.,，]', after or ' '):
        return True
    # 月份、日期、区间：10-11月、7/28、9月
    if after in ('月', '日', '/', '-', '年') or re.match(r'[\-–]\d+月', text[end:end + 4]):
        return True
    # 章节编号：§9.3、见 9.3
    if re.search(r'(§|見|见)\s?$', before):
        return True
    return False


def _first_data_number(text: str):
    """返回单元格中第一个「数据型」数字 (value, unit, raw)，跳过年份／季度／月份等噪声。"""
    for m in _CELL_NUM_RE.finditer(text):
        raw = m.group(1).strip('.，,')
        if not raw or not re.search(r'\d', raw):
            continue
        unit = (m.group(2) or '').strip()
        if _is_noise_number(text, m.start(1), m.start(1) + len(m.group(1).rstrip('.，,')), unit):
            continue
        val = _clean_num(raw)
        if val is not None:
            return val, unit, raw
    return None, '', ''


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
                        val, unit, raw_num = _first_data_number(cell)
                        if val and val != 0 and val < 1e15:
                            results.append((row_label, col_header, val, unit, i + 1, dline, raw_num))
                    i += 1
                continue
        i += 1
    return results


_LEDGER_HEAD = '資料帳本'


def _raw_decimals(raw: str) -> int:
    """报告显示的小数位数，依原始字串（44.00 → 2，3,300 → 0）。"""
    raw = raw.replace(',', '').replace('，', '').strip()
    return len(raw.split('.')[1]) if '.' in raw else 0


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

    def _add(label, val, unit, lineno, raw, raw_num=''):
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
            'decimals': _raw_decimals(raw_num) if raw_num else _decimals(val),
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
    for row_label, col_header, val, unit, lineno, raw, raw_num in _parse_md_tables(lines):
        if _LEDGER_HEAD in section_of[lineno - 1]:
            continue  # 资料帐本本身不列入报告数字
        # 跳过无意义行标签
        if not _is_valid_label(row_label):
            continue
        # 跳过说明类栏位；变化率栏（YoY／QoQ）照常纳入，由帐本自动推导核对
        if col_header.upper() in ('趋势', '趨勢', '说明', '說明', '备注', '備註'):
            continue
        # 评分／品质栏（1-5 分、★）不是财务数据
        if re.search(r'評分|评分|質量|质量|分數|分数|1-5|★', col_header):
            continue
        # label = "行标签 · 列标题"（若列标题是行标签的补充）
        if col_header and col_header != row_label:
            label = f"{row_label} · {col_header}"
        else:
            label = row_label
        _add(label, val, unit, lineno, raw, raw_num)

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
            if _LEDGER_HEAD in section_of[lineno - 1]:
                continue
            _add(label, val, unit, lineno, stripped, m.group('num'))

    return points


def sample_points(points: list, ratio: float = 0.15, seed: int = None,
                  must_sections: list = None) -> list:
    """分层抽样：must_sections 标题（子字串匹配，含上层标题路径）下的数据点全数纳入，
    其余数据点随机抽取 ratio 比例（最少 3 个，最多 30 个）。"""
    must_sections = must_sections or []
    must = [p for p in points if in_sections(p, must_sections)]
    must_ids = {p['id'] for p in must}
    rest = [p for p in points if p['id'] not in must_ids]
    n = max(3, min(30, math.ceil(len(rest) * ratio)))
    n = min(n, len(rest))
    rng = Random(seed)
    sampled = must + rng.sample(rest, n)
    # 按行号排序，方便人工比对
    return sorted(sampled, key=lambda p: p['line_number'])


def in_sections(point: dict, sections: list) -> bool:
    return any(ms and ms in point.get('section', '') for ms in sections)


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


def _within_rounding(reported: float, fetched: float, decimals: int = None) -> bool:
    """官方值四舍五入到报告显示位数后是否与报告值一致。"""
    d = _decimals(reported) if decimals is None else decimals
    half = 0.5 * 10 ** (-d)
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
        dec = item.get('decimals')
        if classify_source(source) == 'official':
            pass1 = _within_rounding(reported, fetched, dec)
        else:
            pass1 = diff1 <= _TOLERANCE
        if diff2 is None:
            pass2 = True
        elif classify_source(source2) == 'official':
            pass2 = _within_rounding(reported, fetched2, dec)
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
        print(f'{YELLOW}注意：{warn_count} 个数据点的第三方来源与报告不一致（权威来源相符或两个第三方来源分歧），可能是口径差异（GAAP/Non-GAAP、汇率、科目归类），请人工复核。{RESET}')
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
# 资料帐本（Data Ledger）：可追溯 + 工具验算
# ---------------------------------------------------------------------------
#
# 报告附录「## 附錄：資料帳本」放一张表，欄位：
#   | ID | 項目 | 口徑 | 期間 | 值 | 單位 | 來源 | 公式 | 容差 |
# 每一列三种形态：
#   原始值：填「值＋來源」（來源写到档名＋页码／科目），不填公式
#   衍生值：填「公式」（=R1/R2*100，引用 ID），不填值，由工具计算
#   勾稽列：同时填「值＋來源＋公式」→ 工具检查「来源揭露值」与「公式自算值」是否一致
#           （例：公司揭露的周转天数 vs 自算；合计 vs 分项加总；资产 = 负债 + 权益）
# 容差：留空＝来源值显示精度（四舍五入后须一致）；可填绝对值（2）或相对值（1%），须在口徑注明理由
#
# 工具检查（皆为通则，不针对特定科目）：
#   1. 公式以 Decimal 从原始值重算，不经中间四舍五入
#   2. 勾稽列：揭露值 vs 自算值
#   3. 来源：原始值须有来源；不得引用本仓库报告；--require-official 时须为权威来源
#      （第三方唯一资料标 [第三方唯一]，假设标「假設」）
#   4. 报告回对：必检章节内每个数字都须对得到帐本中某一笔（含同项目跨期间的变化率／差额，
#      由工具自动推导），且报告标签中出现的期间、口径字词须与该笔一致
#      （字词表取自帐本本身的「期間」「口徑」欄，不写死任何科目）

_LEDGER_COLS = {'ID': 'id', '項目': 'item', '口徑': 'basis', '期間': 'period', '值': 'value',
                '單位': 'unit', '來源': 'source', '公式': 'formula', '容差': 'tol'}
# 帐本单位 → 基本单位倍数（仅用于跨单位回对报告数字；比率类单位不缩放）
_SCALE_UNITS = {'元': 1, '千元': 1e3, '仟元': 1e3, '萬元': 1e4, '万元': 1e4, '百萬元': 1e6, '百万元': 1e6,
                '億元': 1e8, '亿元': 1e8, '億': 1e8, '亿': 1e8, '兆元': 1e12,
                '美元': 1, '千美元': 1e3, '百萬美元': 1e6, '百万美元': 1e6, '億美元': 1e8, '十億美元': 1e9,
                '股': 1, '千股': 1e3, '百萬股': 1e6, '億股': 1e8}
_REPORT_SCALES = [1, 1e3, 1e4, 1e6, 1e8, 1e9, 1e12]


def _dec(x) -> Decimal:
    return x if isinstance(x, Decimal) else Decimal(str(x))


def parse_ledger(md_text: str) -> tuple:
    """解析附录资料帐本，返回 (rows, errors)。"""
    lines = md_text.split('\n')
    start = None
    for i, ln in enumerate(lines):
        if re.match(r'^#{1,6}\s', ln.strip()) and _LEDGER_HEAD in ln:
            start = i
            break
    if start is None:
        return [], ['找不到「資料帳本」章节']
    header, rows, errors = None, [], []
    for i in range(start + 1, len(lines)):
        st = lines[i].strip()
        if re.match(r'^#{1,6}\s', st):
            break
        if not st.startswith('|'):
            if header and rows:
                break
            continue
        if re.match(r'^\|[\-\s\|:]+\|$', st):
            continue
        cells = [c.strip() for c in st.strip('|').split('|')]
        if header is None:
            header = [_LEDGER_COLS.get(c.replace(' ', ''), c) for c in cells]
            missing = [k for k in ('id', 'item', 'value', 'unit', 'source', 'formula') if k not in header]
            if missing:
                return [], [f'帐本表头缺少栏位：{missing}']
            continue
        row = dict(zip(header, cells + [''] * (len(header) - len(cells))))
        row['line'] = i + 1
        raw_val = row.get('value', '').replace(',', '').replace('，', '').strip()
        row['value_str'] = raw_val
        try:
            row['value'] = Decimal(raw_val) if raw_val not in ('', '-', '—') else None
        except Exception:
            errors.append(f'第 {i+1} 行 {row.get("id")}：值无法解析「{raw_val}」')
            row['value'] = None
        row['formula'] = row.get('formula', '').strip()
        rows.append(row)
    ids = [r['id'] for r in rows]
    dup = {x for x in ids if ids.count(x) > 1}
    if dup:
        errors.append(f'ID 重复：{sorted(dup)}')
    return rows, errors


def _eval_formula(expr: str, env: dict) -> Decimal:
    """安全计算公式（仅四则运算、括号、abs），以 Decimal 精确计算。"""
    import ast
    tree = ast.parse(expr.lstrip('=').strip(), mode='eval')

    def ev(n):
        if isinstance(n, ast.Expression):
            return ev(n.body)
        if isinstance(n, ast.BinOp):
            a, b = ev(n.left), ev(n.right)
            if isinstance(n.op, ast.Add):
                return a + b
            if isinstance(n.op, ast.Sub):
                return a - b
            if isinstance(n.op, ast.Mult):
                return a * b
            if isinstance(n.op, ast.Div):
                return _CTX.divide(a, b)
            if isinstance(n.op, ast.Pow):
                return _dec(float(a) ** float(b))
            raise ValueError('不支援的运算')
        if isinstance(n, ast.UnaryOp):
            v = ev(n.operand)
            return -v if isinstance(n.op, ast.USub) else v
        if isinstance(n, ast.Constant):
            return _dec(n.value)
        if isinstance(n, ast.Name):
            if n.id not in env or env[n.id] is None:
                raise KeyError(n.id)
            return env[n.id]
        if isinstance(n, ast.Call) and getattr(n.func, 'id', '') == 'abs' and len(n.args) == 1:
            return abs(ev(n.args[0]))
        raise ValueError('公式只允许四则运算、括号、abs 与 ID 引用')
    return ev(tree)


def _tol_ok(stated: Decimal, computed: Decimal, tol: str, stated_str: str) -> bool:
    tol = (tol or '').strip()
    if tol.endswith('%'):
        return abs(computed - stated) <= abs(stated) * _dec(tol[:-1]) / 100
    if tol:
        return abs(computed - stated) <= _dec(tol)
    d = len(stated_str.split('.')[1]) if '.' in stated_str else 0
    return abs(computed - stated) <= _dec(0.5) * _dec(10) ** (-d) + _dec('1e-12')


def evaluate_ledger(rows: list, require_official: bool = False) -> dict:
    """计算衍生值、检查勾稽与来源。"""
    env = {r['id']: r['value'] for r in rows if r['value'] is not None and not r['formula']}
    issues, recon = [], []
    pending = [r for r in rows if r['formula']]
    for _ in range(len(pending) + 1):
        progressed = False
        for r in list(pending):
            try:
                r['computed'] = _eval_formula(r['formula'], env)
            except KeyError:
                continue
            except Exception as e:
                issues.append(('公式错误', r, str(e)))
                pending.remove(r)
                continue
            pending.remove(r)
            progressed = True
            if r['value'] is None:
                env[r['id']] = r['computed']
            else:
                env[r['id']] = r['value']
                ok = _tol_ok(r['value'], r['computed'], r.get('tol', ''), r['value_str'])
                recon.append((r, ok))
                if not ok:
                    issues.append(('勾稽不符', r, f'来源值 {r["value_str"]} vs 公式自算 {r["computed"]:.6g}'))
        if not pending or not progressed:
            break
    for r in pending:
        issues.append(('公式无法计算', r, '引用的 ID 不存在或无值'))
    for r in rows:
        if r['formula'] and r['value'] is None:
            continue
        src = r.get('source', '')
        cls = classify_source(src)
        if not src:
            issues.append(('来源缺漏', r, '原始值未填来源'))
        elif cls == 'circular':
            issues.append(('循环来源', r, '引用本仓库报告'))
        elif require_official and cls not in ('official', 'computed') \
                and _NO_OFFICIAL_MARK not in src and '假設' not in src and '假设' not in src:
            issues.append(('非权威来源', r, src))
    return {'env': env, 'issues': issues, 'recon': recon}


def _tokens(text: str) -> set:
    return {t for t in re.split(r'[／/、,，;；\s（）()]+', text or '') if len(t) >= 2}


def _candidates(rows: list, env: dict) -> list:
    """可供报告回对的数值：帐本每一笔，加上同项目、同口径、同单位跨期间的变化率与差额。"""
    cands = []
    for r in rows:
        v = env.get(r['id']) if r['value'] is None else r['value']
        if v is None:
            continue
        scale = _SCALE_UNITS.get(r.get('unit', '').strip())
        cands.append({'v': v, 'scale': scale, 'periods': {r.get('period', '')}, 'row': r,
                      'text': f"{r.get('item','')} {r.get('basis','')}", 'desc': r['id']})
        if r['formula'] and r['value'] is not None:
            cands.append({'v': r['computed'], 'scale': scale, 'periods': {r.get('period', '')}, 'row': r,
                          'text': f"{r.get('item','')} {r.get('basis','')}", 'desc': r['id'] + '(自算)'})
    groups = {}
    for r in rows:
        v = env.get(r['id']) if r['value'] is None else r['value']
        if v is None or not r.get('period'):
            continue
        groups.setdefault((r.get('item'), r.get('basis'), r.get('unit')), []).append((r, v))
    for (item, basis, unit), lst in groups.items():
        for ra, va in lst:
            for rb, vb in lst:
                if ra is rb:
                    continue
                meta = {'periods': {ra['period'], rb['period']}, 'row': ra, 'text': f'{item} {basis}',
                        'desc': f"{ra['id']}vs{rb['id']}"}
                if vb != 0:
                    cands.append(dict(meta, v=(va / vb - 1) * 100, scale=None))
                cands.append(dict(meta, v=va - vb, scale=_SCALE_UNITS.get((unit or '').strip())))
    return cands


def _display_match(cand_v: Decimal, scale, reported: float, decimals: int) -> bool:
    target = abs(_dec(reported))
    half = _dec(0.5) * _dec(10) ** (-decimals) + _dec('1e-12')
    muls = [1] if scale is None else [scale / s for s in _REPORT_SCALES]
    for m in muls:
        if abs(abs(cand_v) * _dec(m) - target) <= half:
            return True
    return False


def check_report_against_ledger(md_text: str, rows: list, env: dict, must_sections: list) -> dict:
    points = extract_data_points(md_text)
    cands = _candidates(rows, env)
    periods_vocab = {r.get('period', '') for r in rows if r.get('period')}
    basis_vocab = set()
    for r in rows:
        basis_vocab |= _tokens(r.get('basis', ''))
    results = []
    for p in points:
        dec = p.get('decimals', _decimals(p['reported_value']))
        matches = [c for c in cands if _display_match(c['v'], c['scale'], p['reported_value'], dec)]
        label = p['label']
        found = {x for x in periods_vocab if x and x in label}
        # 只保留最长匹配（「2026Q2」出现时不另外要求「2026」）
        lab_periods = {x for x in found if not any(x != y and x in y for y in found)}
        lab_basis = {t for t in basis_vocab if t in label}
        consistent = [c for c in matches
                      if lab_periods <= c['periods']
                      and all(t in c['text'] for t in lab_basis)]
        if consistent:
            status = 'ok'
        elif matches:
            status = 'conflict'
        else:
            status = 'unmatched'
        results.append({'point': p, 'status': status, 'must': in_sections(p, must_sections),
                        'match': (consistent or matches or [None])[0],
                        'lab_periods': lab_periods, 'lab_basis': lab_basis})
    return {'results': results}


def run_ledger_check(md_text: str, must_sections: list, require_official: bool) -> int:
    rows, perrs = parse_ledger(md_text)
    print('=' * 70)
    print('资料帐本验算')
    print('=' * 70)
    if perrs and not rows:
        for e in perrs:
            print(f'  ❌ {e}')
        return 1
    ev = evaluate_ledger(rows, require_official)
    n_raw = sum(1 for r in rows if not r['formula'])
    n_der = sum(1 for r in rows if r['formula'] and r['value'] is None)
    n_rec = len(ev['recon'])
    print(f'  帐本：原始值 {n_raw} 笔｜衍生值 {n_der} 笔｜勾稽列 {n_rec} 笔（通过 {sum(ok for _, ok in ev["recon"])}）')
    for e in perrs:
        print(f'  ❌ {e}')
    for kind, r, msg in ev['issues']:
        print(f'  ❌ [{kind}] 第 {r["line"]} 行 {r["id"]} {r.get("item","")} {r.get("period","")}：{msg}')
    der = [r for r in rows if r['formula'] and r['value'] is None and 'computed' in r]
    if der:
        print('\n  衍生值（工具计算，报告须引用此结果）：')
        for r in der:
            print(f'    {r["id"]:>5} {r.get("item","")[:18]:18s} {r.get("period",""):8s} = {r["computed"]:.6f} {r.get("unit","")}')
    chk = check_report_against_ledger(md_text, rows, ev['env'], must_sections)
    res = chk['results']
    must = [x for x in res if x['must']]
    bad_must = [x for x in must if x['status'] != 'ok']
    other_bad = [x for x in res if not x['must'] and x['status'] != 'ok']
    print()
    if must_sections:
        print(f'  必检章节（{"、".join(must_sections)}）：{len(must) - len(bad_must)}/{len(must)} 个数字可追溯到帐本')
    print(f'  全文：{sum(x["status"] == "ok" for x in res)}/{len(res)} 个数字可追溯到帐本')
    for x in bad_must:
        p = x['point']
        why = '口径／期间与帐本不一致' if x['status'] == 'conflict' else '帐本中找不到此数字'
        extra = ''
        if x['status'] == 'conflict':
            m = x['match']
            extra = f'（值对到 {m["desc"]} {m["text"].strip()} {"/".join(sorted(m["periods"]))}；标签含 {sorted(x["lab_periods"] | x["lab_basis"])}）'
        print(f'  ❌ 第 {p["line_number"]} 行 {p["label"][:40]} = {p["reported_value"]}：{why}{extra}')
    if other_bad:
        print(f'\n  必检章节以外有 {len(other_bad)} 个数字未能追溯（列出供复核，不计入打回）：')
        for x in other_bad[:40]:
            p = x['point']
            print(f'     第 {p["line_number"]} 行 {p["label"][:40]} = {p["reported_value"]}（{"口径／期间冲突" if x["status"]=="conflict" else "未追溯"}）')
    failed = bool(perrs or ev['issues'] or bad_must)
    print('-' * 70)
    print('【准出】帐本验算通过' if not failed else '【打回】帐本验算未通过：修正报告或帐本后重跑')
    return 1 if failed else 0


def ledger_sample(md_text: str, ratio: float, seed) -> list:
    """从帐本原始值（非假设）抽样，输出 verdict 用 JSON 模板，供回到来源独立重取。"""
    rows, _ = parse_ledger(md_text)
    raw = [r for r in rows if not r['formula'] and r['value'] is not None
           and '假設' not in r.get('source', '') and '假设' not in r.get('source', '')]
    n = min(len(raw), max(5, math.ceil(len(raw) * ratio)))
    picked = Random(seed).sample(raw, n)
    out = []
    for r in sorted(picked, key=lambda x: x['line']):
        out.append({'id': r['id'], 'label': f'{r["item"]} {r.get("basis","")} {r.get("period","")}'.strip(),
                    'reported_value': float(r['value']), 'unit': r.get('unit', ''),
                    'line_number': r['line'], 'decimals': _raw_decimals(r['value_str']),
                    'ledger_source': r.get('source', ''),
                    'fetched_value': None, 'fetched_source': '', 'fetched_value2': None, 'fetched_source2': ''})
    return out


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

    # ledger
    ldg = sub.add_parser('ledger', help='资料帐本验算：公式重算、勾稽、来源、报告数字回对帐本')
    ldg.add_argument('--report', required=True, help='报告文件路径（附录含「資料帳本」表）')
    ldg.add_argument('--must-section', action='append', default=[],
                     help='该标题（子字串，含上层标题路径）下每个数字都必须追溯到帐本，可重复指定')
    ldg.add_argument('--require-official', action='store_true', help='原始值须为权威来源')
    ldg.add_argument('--sample', type=float, default=None,
                     help='改为输出帐本原始值抽样 JSON（比例，如 0.2），供回到来源独立重取后交给 verdict')
    ldg.add_argument('--seed', type=int, default=None)

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
            print(f'必检章节：{"、".join(args.must_section)}（{n_must} 点全数纳入，其余随机抽样）')
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
                    'decimals': p.get('decimals'),
                    'raw_text': p['raw_text'],
                    'fetched_value': None,       # ← 填入主来源核验值
                    'fetched_source': '',        # ← 填入主来源名称
                    'fetched_value2': None,      # ← 填入副来源核验值（可选）
                    'fetched_source2': '',       # ← 填入副来源名称（可选）
                })
            print('抽检清单 JSON（填入 fetched_value 后，传给 verdict 命令）：')
            print()
            print(json.dumps(template, ensure_ascii=False, indent=2))

    elif args.command == 'ledger':
        if not os.path.exists(args.report):
            print(f'❌ 文件不存在: {args.report}', file=sys.stderr)
            sys.exit(1)
        with open(args.report, 'r', encoding='utf-8') as f:
            text = f.read()
        if args.sample is not None:
            print(json.dumps(ledger_sample(text, args.sample, args.seed), ensure_ascii=False, indent=2))
            sys.exit(0)
        sys.exit(run_ledger_check(text, args.must_section, args.require_official))

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
