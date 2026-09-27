#!/usr/bin/env python3
"""官方来源取数工具：直接从权威来源产生「資料帳本」列，减少手抄与转述误差。

子命令：
  sec           SEC XBRL companyfacts（美股 10-K／10-Q／8-K 的结构化财报数字）
  tw-pdf        台股 MOPS 格式财报 PDF（公司官网「每季财务报告」或公开资讯观测站下载档）
  twse-price    证交所个股日成交资讯（收盘、区间最高／最低）
  nasdaq-price  Nasdaq 个股历史行情（收盘、区间最高／最低）

输出为 Markdown 表格列，栏位与 skills/financial-data.md「資料帳本」一致：
  | ID | 項目 | 口徑 | 期間 | 值 | 單位 | 來源 | 公式 | 容差 |
直接贴进报告附录的资料帐本，再以 tools/report_audit.py ledger 验算。

网路请求的 User-Agent 预设不含个人资讯；SEC 若要求联络资讯，请自行设定环境变数
SEC_USER_AGENT（例如「公司名 联络信箱」）。本工具不会写入或传送任何个人资料。

用法示例：
  python3 tools/official_data.py sec --cik 723125 --accn 0000723125-26-000015 \\
      --concepts RevenueFromContractWithCustomerExcludingAssessedTax,GrossProfit \\
      --period-map 2026-05-28=FY2026Q3 --prefix S
  python3 tools/official_data.py tw-pdf --file 115Q2_IS.pdf --accounts 營業收入合計,營業利益（損失） \\
      --col 0 --period 2026Q2 --source "官網合併損益表 115Q2" --prefix I
  python3 tools/official_data.py twse-price --stock 2449 --date 2026-08-31
  python3 tools/official_data.py nasdaq-price --symbol MU --date 2026-09-25
"""

import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.request
from datetime import date, datetime, timedelta

_UA = os.environ.get('SEC_USER_AGENT', 'ai-berkshire-research-tool')
_TIMEOUT = 30


def _get(url: str, ua: str = None) -> bytes:
    req = urllib.request.Request(url, headers={'User-Agent': ua or _UA, 'Accept': 'application/json'})
    with urllib.request.urlopen(req, timeout=_TIMEOUT) as r:
        return r.read()


def _row(i, item, basis, period, value, unit, source):
    if isinstance(value, float) and value.is_integer() and abs(value) >= 1000:
        value = int(value)
    return f'| {i} | {item} | {basis} | {period} | {value} | {unit} | {source} |  |  |'


# CJK 部首补充区（U+2E80–U+2EFF）没有 NFKC 映射，PDF 常用它们代替正字
_RADICALS = str.maketrans({'⻑': '長', '⻓': '长', '⻄': '西', '⻝': '食', '⻟': '食', '⻩': '黃', '⻢': '馬',
                           '⻔': '門', '⻛': '風', '⻜': '飛', '⻤': '鬼', '⻘': '青', '⻭': '齒', '⻯': '龍',
                           '⻰': '龍', '⻳': '龜', '⺠': '民', '⺟': '母', '⻅': '見', '⻆': '角', '⻉': '貝'})


def _norm(s: str) -> str:
    """正规化：PDF 常见的「⼊」「⽉」「⻑」等相容字元／部首字统一成标准字。"""
    return unicodedata.normalize('NFKC', (s or '').translate(_RADICALS))


# ---------------------------------------------------------------------------
# SEC XBRL
# ---------------------------------------------------------------------------

_SEC_UNITS = {'USD': '美元', 'USD/shares': '美元/股', 'shares': '股', 'pure': '比率'}


def _duration_tag(start, end) -> str:
    if not start:
        return '期末'
    days = (datetime.strptime(end, '%Y-%m-%d') - datetime.strptime(start, '%Y-%m-%d')).days
    if days <= 100:
        return '單季'
    if days <= 190:
        return '半年累計'
    if days <= 280:
        return '九個月累計'
    return '全年'


def cmd_sec(a):
    cik = str(a.cik).zfill(10)
    data = json.loads(_get(f'https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json'))
    pmap = dict(x.split('=', 1) for x in (a.period_map or '').split(',') if '=' in x)
    wanted = [c.strip() for c in (a.concepts or '').split(',') if c.strip()]
    names = dict(x.split('=', 1) for x in (a.names or '').split(',') if '=' in x)
    rows = []
    for ns in ('us-gaap', 'dei', 'ifrs-full'):
        for concept, body in data.get('facts', {}).get(ns, {}).items():
            if wanted and concept not in wanted:
                continue
            for unit, facts in body.get('units', {}).items():
                for f in facts:
                    if a.accn and f.get('accn') != a.accn:
                        continue
                    if not a.accn and a.form and f.get('form') != a.form:
                        continue
                    if a.ends and f['end'] not in a.ends.split(','):
                        continue
                    tag = _duration_tag(f.get('start'), f['end'])
                    period = pmap.get(f['end'], f['end'])
                    src = f"SEC XBRL {f.get('form')} {f.get('accn')} {ns}:{concept}（{f.get('start') or ''}～{f['end']}）"
                    rows.append((concept, f['end'], tag,
                                 (names.get(concept) or body.get('label') or concept, f'GAAP {tag}', period, f['val'],
                                  _SEC_UNITS.get(unit, unit), src)))
    if not rows:
        print('找不到符合条件的 XBRL 数据（确认 CIK、accn、概念名称）', file=sys.stderr)
        return 1
    order = {c: i for i, c in enumerate(wanted)}
    rows = sorted(set(rows), key=lambda x: (order.get(x[0], 999), x[0], x[2], x[1]))
    for n, (_, _, _, fields) in enumerate(rows, 1):
        print(_row(f'{a.prefix}{n}', *fields))
    return 0


# ---------------------------------------------------------------------------
# 台股 MOPS 格式 PDF
# ---------------------------------------------------------------------------

def _pdf_lines(path: str) -> list:
    try:
        import pdfplumber
    except ImportError:
        print('需要 pdfplumber：pip install pdfplumber', file=sys.stderr)
        sys.exit(2)
    import logging
    logging.disable(logging.CRITICAL)
    with pdfplumber.open(path) as p:
        text = '\n'.join(pg.extract_text() or '' for pg in p.pages)
    return [_norm(l) for l in text.splitlines()]


def cmd_tw_pdf(a):
    lines = _pdf_lines(a.file)
    accounts = [_norm(x.strip()) for x in a.accounts.split(',') if x.strip()]
    rc = 0
    for k, acct in enumerate(accounts, 1):
        hits = [l for l in lines if l.startswith(acct) and not l[len(acct):len(acct) + 1] in ('－', '-')
                and re.search(r'\d', l[len(acct):])]
        if len(hits) <= a.occurrence:
            print(f'找不到科目「{acct}」（第 {a.occurrence} 次出现）', file=sys.stderr)
            rc = 1
            continue
        nums = re.findall(r'-?[\d,]+(?:\.\d+)?', hits[a.occurrence][len(acct):])
        nums = [x for x in nums if re.search(r'\d', x)]
        if len(nums) <= a.col:
            print(f'科目「{acct}」只有 {len(nums)} 个数字栏，取不到第 {a.col} 栏', file=sys.stderr)
            rc = 1
            continue
        raw = nums[a.col].replace(',', '')
        val = float(raw) if '.' in raw else int(raw)
        print(_row(f'{a.prefix}{k}', acct, a.basis, a.period, val, a.unit, f'{a.source} {acct}'))
    return rc


# ---------------------------------------------------------------------------
# 行情
# ---------------------------------------------------------------------------

def _twse_month(stock: str, yyyymm: str) -> list:
    url = (f'https://www.twse.com.tw/rwd/zh/afterTrading/STOCK_DAY?date={yyyymm}01'
           f'&stockNo={stock}&response=json')
    import time
    for attempt in range(5):  # 证交所限流时回 307／安全性页面，退避重试
        try:
            d = json.loads(_get(url, 'Mozilla/5.0'))
            break
        except Exception:
            if attempt == 4:
                raise
            time.sleep(10 * 2 ** attempt)
    out = []
    for r in d.get('data', []):
        y, m, dd = r[0].split('/')
        out.append({'date': date(int(y) + 1911, int(m), int(dd)), 'high': float(r[4].replace(',', '')),
                    'low': float(r[5].replace(',', '')), 'close': float(r[6].replace(',', ''))})
    return out


def _months(d1: date, d2: date):
    y, m = d1.year, d1.month
    while (y, m) <= (d2.year, d2.month):
        yield f'{y}{m:02d}'
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)


def cmd_twse_price(a):
    import time
    d1 = datetime.strptime(a.start or a.date, '%Y-%m-%d').date()
    d2 = datetime.strptime(a.date, '%Y-%m-%d').date()
    rows = []
    for ym in _months(d1, d2):
        rows += _twse_month(a.stock, ym)
        time.sleep(a.sleep)
    rows = [r for r in rows if d1 <= r['date'] <= d2]
    if not rows:
        print('查无交易资料', file=sys.stderr)
        return 1
    last = [r for r in rows if r['date'] == d2]
    if last:
        print(_row(f'{a.prefix}1', '收盤價', '', a.date, f"{last[0]['close']:.2f}", '元',
                   f'TWSE STOCK_DAY {a.stock} {a.date} 收盤價'))
    if a.start:
        hi = max(rows, key=lambda r: r['high'])
        lo = min(rows, key=lambda r: r['low'])
        print(_row(f'{a.prefix}2', '區間最高價', f'{a.start}～{a.date}', a.date, f"{hi['high']:.2f}", '元',
                   f"TWSE STOCK_DAY {a.stock} {hi['date']} 最高價"))
        print(_row(f'{a.prefix}3', '區間最低價', f'{a.start}～{a.date}', a.date, f"{lo['low']:.2f}", '元',
                   f"TWSE STOCK_DAY {a.stock} {lo['date']} 最低價"))
    return 0


def cmd_nasdaq_price(a):
    d2 = datetime.strptime(a.date, '%Y-%m-%d').date()

    def fetch(start, end):
        url = (f'https://api.nasdaq.com/api/quote/{a.symbol}/historical?assetclass=stocks'
               f'&fromdate={start}&todate={end}&limit=400')
        d = json.loads(_get(url, 'Mozilla/5.0'))
        return ((d.get('data') or {}).get('tradesTable') or {}).get('rows') or []
    # Nasdaq API 对某些区间（起迄同日、部分短区间）会回空：依序换几个查询窗口，直到含目标日
    if a.start:
        windows = [(a.start, a.date)]
    else:
        windows = [((d2 - timedelta(days=n)).isoformat(), (d2 + timedelta(days=m)).isoformat())
                   for n, m in ((30, 0), (10, 0))]
        windows.append(((d2 - timedelta(days=10)).isoformat(), date.today().isoformat()))  # 较旧日期的短区间常回空
    rows = []
    for st, en in windows:
        got = fetch(st, en)
        if got:
            rows = got
        if any(r['date'] == d2.strftime('%m/%d/%Y') for r in got):
            break
    if not rows:
        print('查无交易资料', file=sys.stderr)
        return 1

    def num(s):
        return float(s.replace('$', '').replace(',', ''))
    recs = [{'date': datetime.strptime(r['date'], '%m/%d/%Y').date(), 'close': num(r['close']),
             'high': num(r['high']), 'low': num(r['low'])} for r in rows]
    last = [r for r in recs if r['date'] == d2]
    if not last:
        print(f'{a.date} 非交易日或查无资料', file=sys.stderr)
        return 1
    if last:
        print(_row(f'{a.prefix}1', '收盤價', '', a.date, f"{last[0]['close']:.2f}", '美元',
                   f'Nasdaq historical (api.nasdaq.com) {a.symbol} {a.date} Close'))
    if a.start:
        recs = [r for r in recs if r['date'] <= d2]
        hi = max(recs, key=lambda r: r['high'])
        lo = min(recs, key=lambda r: r['low'])
        print(_row(f'{a.prefix}2', '區間最高價', f'{a.start}～{a.date}', a.date, f"{hi['high']:.2f}", '美元',
                   f"Nasdaq historical (api.nasdaq.com) {a.symbol} {hi['date']} High"))
        print(_row(f'{a.prefix}3', '區間最低價', f'{a.start}～{a.date}', a.date, f"{lo['low']:.2f}", '美元',
                   f"Nasdaq historical (api.nasdaq.com) {a.symbol} {lo['date']} Low"))
    return 0


def main():
    p = argparse.ArgumentParser(description='官方来源取数，输出资料帐本列',
                                formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    sub = p.add_subparsers(dest='cmd')

    s = sub.add_parser('sec', help='SEC XBRL companyfacts')
    s.add_argument('--cik', required=True, help='SEC CIK（数字）')
    s.add_argument('--accn', help='只取某一份申报（accession number，如 0000723125-26-000015）')
    s.add_argument('--form', help='未指定 accn 时依表单过滤（10-Q／10-K）')
    s.add_argument('--concepts', help='XBRL 概念，逗号分隔；省略则输出该申报全部概念')
    s.add_argument('--period-map', help='期末日→期间标签，如 2026-05-28=FY2026Q3,2025-05-29=FY2025Q3')
    s.add_argument('--ends', help='只取这些期末日（逗号分隔），避免带出不需要的比较期')
    s.add_argument('--names', help='概念→帐本项目名，如 GrossProfit=毛利,NetIncomeLoss=淨利；同一项目名跨期一致才能自动推导变化率')
    s.add_argument('--prefix', default='S')

    t = sub.add_parser('tw-pdf', help='台股 MOPS 格式财报 PDF')
    t.add_argument('--file', required=True)
    t.add_argument('--accounts', required=True, help='会计科目，逗号分隔（行首比对）')
    t.add_argument('--col', type=int, default=0, help='取第几个数字栏（0 起算；金额与百分比交错时注意）')
    t.add_argument('--occurrence', type=int, default=0, help='科目出现多次时取第几次（0 起算）')
    t.add_argument('--period', required=True)
    t.add_argument('--basis', default='合併')
    t.add_argument('--unit', default='仟元')
    t.add_argument('--source', required=True, help='来源描述（档名／报表名称）')
    t.add_argument('--prefix', default='T')

    w = sub.add_parser('twse-price', help='证交所行情')
    w.add_argument('--stock', required=True)
    w.add_argument('--date', required=True, help='YYYY-MM-DD')
    w.add_argument('--start', help='区间起日（给定时另输出区间最高／最低）')
    w.add_argument('--sleep', type=float, default=3.0, help='每次请求间隔秒数（证交所有频率限制）')
    w.add_argument('--prefix', default='P')

    n = sub.add_parser('nasdaq-price', help='Nasdaq 行情')
    n.add_argument('--symbol', required=True)
    n.add_argument('--date', required=True, help='YYYY-MM-DD')
    n.add_argument('--start', help='区间起日（给定时另输出区间最高／最低）')
    n.add_argument('--prefix', default='P')

    a = p.parse_args()
    fn = {'sec': cmd_sec, 'tw-pdf': cmd_tw_pdf, 'twse-price': cmd_twse_price, 'nasdaq-price': cmd_nasdaq_price}
    if a.cmd not in fn:
        p.print_help()
        sys.exit(1)
    sys.exit(fn[a.cmd](a))


if __name__ == '__main__':
    main()
