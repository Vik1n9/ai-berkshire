#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_graph.py — 為 AI Berkshire 專案建立知識圖譜，便於後續查詢。

掃描 reports/ skills/ tools/ data/，抽取實體（公司/行業/主題）、報告、
Skill、工具，構建節點+邊的圖譜，輸出：

  data/project_graph.json   機器可讀知識圖譜（供 query_graph.py / RAG 查詢）
  docs/PROJECT_GRAPH.md      人類可讀索引（公司→報告清單、Skill 目錄、統計）

設計原則：
  - 僅用 Python 標準庫，無外部依賴，隨時可重跑（報告持續新增）。
  - 後設資料從「檔名約定 + 表頭輕量掃描」抽取，不做重推斷。
  - 冪等：同一份程式碼庫多次執行結果一致。

用法：
    python3 scripts/build_graph.py            # 生成圖譜
    python3 scripts/build_graph.py --check    # 只校驗、列印統計，不寫檔案
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(ROOT, "reports")
SKILLS_DIR = os.path.join(ROOT, "skills")
TOOLS_DIR = os.path.join(ROOT, "tools")
DATA_DIR = os.path.join(ROOT, "data")
DOCS_DIR = os.path.join(ROOT, "docs")

GRAPH_JSON = os.path.join(DATA_DIR, "project_graph.json")
GRAPH_MD = os.path.join(DOCS_DIR, "PROJECT_GRAPH.md")

# 四位投資大師視角
MASTERS = ["巴菲特", "芒格", "段永平", "李錄"]

# 報告型別識別規則：(型別標籤, 檔名匹配關鍵詞列表)
# 順序敏感：越具體的規則越靠前。
TYPE_RULES = [
    ("earnings", ["earnings", "財報電話會", "財報精讀", "-earnings-", "季報", "年報點評"]),
    ("thesis", ["thesis", "-論文", "投資論文", "投資論述"]),
    ("management", ["management", "管理層", "高管", "-mgmt-"]),
    ("valuation", ["valuation", "估值", "dcf", "公允價值", "fair_value", "內在價值"]),
    ("team", ["-team-", "investment-team", "最終報告", "四大師"]),
    ("private", ["private", "未上市", "招股書", "ipo"]),
    ("checklist", ["checklist", "檢查清單", "鏡子測試"]),
    ("industry", ["industry", "行業研究", "-行業-", "產業全景", "產業鏈", "全景研究"]),
    ("funnel", ["funnel", "漏斗", "篩選", "召回池", "候選池", "選股", "screen"]),
    ("news", ["news", "-新聞-", "news-pulse", "-快訊-", "政策解讀"]),
    ("portfolio", ["portfolio", "投資組合", "組合報告", "持倉", "13f"]),
    ("comparison", ["對比", "vs", "相關性", "輪動", "對決", "換倉", "allin"]),
    ("research", ["research", "investment-research", "深度研究", "深度分析",
                  "研究報告", "投資研究", "-研究-", "deep-dive", "deep_dive"]),
]

# 檔名 → Skill 名（對應 skills/*.md）
SKILL_HINTS = {
    "investment-research": "investment-research",
    "investment-team": "investment-team",
    "investment-checklist": "investment-checklist",
    "industry-research": "industry-research",
    "industry-funnel": "industry-funnel",
    "private-company-research": "private-company-research",
    "earnings-review": "earnings-review",
    "earnings-team": "earnings-team",
    "thesis-tracker": "thesis-tracker",
    "thesis-drift": "thesis-drift",
    "portfolio-review": "portfolio-review",
    "management-deep-dive": "management-deep-dive",
    "news-pulse": "news-pulse",
    "quality-screen": "quality-screen",
    "bottleneck-hunter": "bottleneck-hunter",
    "deep-company-series": "deep-company-series",
    "wechat-article": "wechat-article",
    "dyp-ask": "dyp-ask",
    "investment-memo-craft": "investment-memo-craft",
}

# ticker：表頭裡 （00700.HK） (2449) （600519.SH） 等
TICKER_RE = re.compile(r"[（(]\s*([0-9]{3,6}(?:\.[A-Za-z]{1,3})?|[A-Z]{1,5}(?:\.[A-Z]{1,3})?)\s*[）)]")
# 括號內常見的「非 ticker」大寫縮寫（財務術語/交易所/口徑），需過濾
TICKER_STOPWORDS = {
    "TTM", "TTMPE", "NYSE", "NASDAQ", "HKEX", "SEHK", "DCF", "PE", "PB", "PS",
    "ROE", "ROIC", "GDP", "CPI", "AI", "ETF", "IPO", "FCF", "EPS", "YOY", "QOQ",
    "HK", "US", "USD", "RMB", "CNY", "EV", "GAAP", "GMV", "ARPU", "MAU", "DAU",
    "CEO", "CFO", "VIE", "SEC", "PPT", "FY", "Q1", "Q2", "Q3", "Q4",
}
# 檔名中的日期：20260408 / 2026-04-08
DATE8_RE = re.compile(r"(20\d{2})[-_]?(\d{2})[-_]?(\d{2})")
# 財報期間：2025Q4 / 2026Q1 / 2025年報
QUARTER_RE = re.compile(r"(20\d{2})\s*(Q[1-4]|年報|中報|半年報|一季報|三季報)", re.IGNORECASE)


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT).replace(os.sep, "/")


def classify_type(name_lower: str) -> str:
    for label, keys in TYPE_RULES:
        for k in keys:
            if k in name_lower:
                return label
    return "other"


def detect_skill(name_lower: str) -> str | None:
    for hint, skill in SKILL_HINTS.items():
        if hint in name_lower:
            return skill
    return None


def parse_date(name: str) -> str | None:
    m = DATE8_RE.search(name)
    if not m:
        return None
    y, mo, d = m.groups()
    try:
        return datetime(int(y), int(mo), int(d)).strftime("%Y-%m-%d")
    except ValueError:
        return None


def parse_quarter(name: str) -> str | None:
    m = QUARTER_RE.search(name)
    if not m:
        return None
    return f"{m.group(1)}{m.group(2).upper()}"


def detect_masters(name: str, header: str) -> list[str]:
    blob = name + " " + header
    return [m for m in MASTERS if m in blob]


def scan_header(path: str) -> tuple[str, str | None]:
    """讀前若干行，返回 (原始表頭文字, ticker)。容錯編碼問題。"""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            head = "".join([next(f, "") for _ in range(10)])
    except (OSError, StopIteration):
        return "", None
    ticker = None
    m = TICKER_RE.search(head)
    if m:
        cand = m.group(1).upper()
        # 過濾純年份、財務縮寫/交易所等噪聲
        if not re.fullmatch(r"20\d{2}", cand) and cand not in TICKER_STOPWORDS:
            ticker = cand
    return head, ticker


def build_report_nodes():
    """掃描 reports/，返回 (reports, entities)。"""
    reports = []
    # entity_name -> {reports:[id], tickers:set, industries:set}
    entities = defaultdict(lambda: {"reports": [], "tickers": set()})

    for dirpath, dirnames, filenames in os.walk(REPORTS_DIR):
        dirnames.sort()
        for fn in sorted(filenames):
            if not fn.endswith(".md"):
                continue
            full = os.path.join(dirpath, fn)
            relpath = rel(full)
            name = fn[:-3]  # 去掉 .md
            name_lower = name.lower()

            # 實體：reports/ 直屬檔案歸為「_root」（主題/多公司報告），
            # 子目錄檔案歸到目錄名（公司/主題）。
            sub = os.path.relpath(dirpath, REPORTS_DIR)
            if sub == ".":
                entity = "_專題與多公司"
            else:
                entity = sub.split(os.sep)[0]

            header, ticker = scan_header(full)
            rtype = classify_type(name_lower)
            skill = detect_skill(name_lower)
            date = parse_date(name)
            quarter = parse_quarter(name)
            masters = detect_masters(name, header)

            try:
                size = os.path.getsize(full)
            except OSError:
                size = 0

            rid = relpath
            node = {
                "id": rid,
                "path": relpath,
                "title": name,
                "entity": entity,
                "type": rtype,
                "skill": skill,
                "date": date,
                "quarter": quarter,
                "ticker": ticker,
                "masters": masters,
                "bytes": size,
            }
            reports.append(node)
            entities[entity]["reports"].append(rid)
            if ticker:
                entities[entity]["tickers"].add(ticker)

    # 整理 entities
    entity_nodes = []
    for name, info in sorted(entities.items()):
        entity_nodes.append({
            "id": f"entity:{name}",
            "name": name,
            "report_count": len(info["reports"]),
            "tickers": sorted(info["tickers"]),
            "reports": info["reports"],
        })
    return reports, entity_nodes


def first_desc(path: str) -> str:
    """取 Skill/文件首個非標題正文段作為簡述。"""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            lines = [ln.rstrip("\n") for ln in f]
    except OSError:
        return ""
    title = ""
    for ln in lines:
        s = ln.strip()
        if s.startswith("# "):
            title = s[2:].strip()
            break
    desc = ""
    for ln in lines:
        s = ln.strip()
        # 跳過空行、標題、frontmatter 分隔線/欄位
        if not s or s.startswith("#") or s in ("---", "...") or s.startswith("> "):
            continue
        if re.match(r"^[A-Za-z_]+:\s", s):  # yaml frontmatter 欄位
            continue
        desc = s
        break
    return (title + " — " + desc).strip(" —") if title or desc else ""


def build_skill_nodes():
    nodes = []
    if not os.path.isdir(SKILLS_DIR):
        return nodes
    for fn in sorted(os.listdir(SKILLS_DIR)):
        if not fn.endswith(".md"):
            continue
        full = os.path.join(SKILLS_DIR, fn)
        nodes.append({
            "id": f"skill:{fn[:-3]}",
            "name": fn[:-3],
            "path": rel(full),
            "desc": first_desc(full),
        })
    return nodes


def build_tool_nodes():
    nodes = []
    if not os.path.isdir(TOOLS_DIR):
        return nodes
    for fn in sorted(os.listdir(TOOLS_DIR)):
        full = os.path.join(TOOLS_DIR, fn)
        if not os.path.isfile(full):
            continue
        doc = ""
        if fn.endswith(".py"):
            # 抓模組 docstring 首行
            try:
                with open(full, "r", encoding="utf-8", errors="replace") as f:
                    txt = f.read(2000)
                m = re.search(r'"""(.*?)"""', txt, re.DOTALL)
                if m:
                    doc = m.group(1).strip().splitlines()[0].strip()
            except OSError:
                pass
        nodes.append({
            "id": f"tool:{fn}",
            "name": fn,
            "path": rel(full),
            "desc": doc,
        })
    return nodes


def build_graph():
    reports, entities = build_report_nodes()
    skills = build_skill_nodes()
    tools = build_tool_nodes()

    # 統計
    by_type = Counter(r["type"] for r in reports)
    by_skill = Counter(r["skill"] for r in reports if r["skill"])
    by_master = Counter(m for r in reports for m in r["masters"])
    dated = [r["date"] for r in reports if r["date"]]

    graph = {
        "meta": {
            "project": "AI Berkshire",
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "generator": "scripts/build_graph.py",
            "note": "價值投資研究知識圖譜：公司/主題實體 + 報告 + Skill + 工具。可用 scripts/query_graph.py 查詢。",
        },
        "stats": {
            "reports": len(reports),
            "entities": len(entities),
            "skills": len(skills),
            "tools": len(tools),
            "reports_by_type": dict(sorted(by_type.items(), key=lambda x: -x[1])),
            "reports_by_skill": dict(sorted(by_skill.items(), key=lambda x: -x[1])),
            "reports_by_master": dict(sorted(by_master.items(), key=lambda x: -x[1])),
            "date_range": [min(dated), max(dated)] if dated else [None, None],
        },
        "entities": entities,
        "reports": reports,
        "skills": skills,
        "tools": tools,
    }
    return graph


def write_json(graph):
    os.makedirs(DATA_DIR, exist_ok=True)
    with open(GRAPH_JSON, "w", encoding="utf-8") as f:
        json.dump(graph, f, ensure_ascii=False, indent=2)


TYPE_LABELS = {
    "research": "投研報告", "thesis": "投資論文", "earnings": "財報精讀",
    "management": "管理層研究", "valuation": "估值", "team": "團隊研究",
    "private": "未上市研究", "checklist": "檢查清單", "industry": "行業研究",
    "funnel": "篩選/漏斗", "news": "新聞/時事", "portfolio": "組合/持倉",
    "comparison": "對比/輪動", "other": "其他",
}


def write_markdown(graph):
    os.makedirs(DOCS_DIR, exist_ok=True)
    s = graph["stats"]
    lines = []
    A = lines.append
    A("# AI Berkshire 專案圖譜（PROJECT GRAPH）\n")
    A("> 自動生成，請勿手工編輯。執行 `python3 scripts/build_graph.py` 重新生成。")
    A(f"> 生成時間：{graph['meta']['generated_at']}\n")
    A("本圖譜為專案的**查詢索引**：把散落在 `reports/`（僅限美股與台股公開發行公司）的報告，")
    A("按「公司/主題實體 → 報告」組織，並附 Skill 與工具目錄，便於後續檢索。\n")
    A("機器可讀版本見 [`data/project_graph.json`](../data/project_graph.json)，")
    A("命令列查詢用 [`scripts/query_graph.py`](../scripts/query_graph.py)。\n")

    A("## 總覽統計\n")
    A(f"- 報告總數：**{s['reports']}**")
    A(f"- 實體（公司/主題）數：**{s['entities']}**")
    A(f"- Skill 數：**{s['skills']}**，工具數：**{s['tools']}**")
    if s["date_range"][0]:
        A(f"- 報告日期跨度：{s['date_range'][0]} ~ {s['date_range'][1]}")
    A("")
    A("**按報告型別：**\n")
    A("| 型別 | 數量 |")
    A("|------|------|")
    for t, c in s["reports_by_type"].items():
        A(f"| {TYPE_LABELS.get(t, t)} (`{t}`) | {c} |")
    A("")
    if s["reports_by_master"]:
        A("**按大師視角（檔案命中）：** " +
          " ／ ".join(f"{m} {c}" for m, c in s["reports_by_master"].items()) + "\n")

    # Skill 目錄
    A("## Skill 目錄\n")
    A("| Skill | 簡述 |")
    A("|-------|------|")
    for sk in graph["skills"]:
        desc = sk["desc"].replace("|", "\\|")[:80]
        A(f"| `/{sk['name']}` | {desc} |")
    A("")

    # 工具目錄
    A("## 工具目錄（tools/）\n")
    A("| 工具 | 說明 |")
    A("|------|------|")
    for tl in graph["tools"]:
        desc = tl["desc"].replace("|", "\\|")[:90]
        A(f"| `{tl['name']}` | {desc} |")
    A("")

    # 實體索引
    A("## 實體索引（公司 / 主題 → 報告）\n")
    A("按報告數量降序。點選路徑可直達。\n")
    reports_by_id = {r["id"]: r for r in graph["reports"]}
    ents = sorted(graph["entities"], key=lambda e: (-e["report_count"], e["name"]))
    for e in ents:
        tick = f" `{'/'.join(e['tickers'])}`" if e["tickers"] else ""
        A(f"### {e['name']}{tick} — {e['report_count']} 份\n")
        rs = [reports_by_id[i] for i in e["reports"]]
        # 按日期倒序（無日期排最後）
        rs.sort(key=lambda r: (r["date"] or "0000-00-00"), reverse=True)
        for r in rs:
            meta = []
            if r["date"]:
                meta.append(r["date"])
            if r["type"] != "other":
                meta.append(TYPE_LABELS.get(r["type"], r["type"]))
            if r["quarter"]:
                meta.append(r["quarter"])
            tag = f" — {' · '.join(meta)}" if meta else ""
            A(f"- [{r['title']}]({os.path.relpath(os.path.join(ROOT, r['path']), DOCS_DIR).replace(os.sep, '/')}){tag}")
        A("")

    with open(GRAPH_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))


def main():
    ap = argparse.ArgumentParser(description="構建 AI Berkshire 專案知識圖譜")
    ap.add_argument("--check", action="store_true", help="只列印統計，不寫檔案")
    args = ap.parse_args()

    graph = build_graph()
    st = graph["stats"]
    print("=== AI Berkshire 圖譜統計 ===")
    print(f"報告 {st['reports']} | 實體 {st['entities']} | "
          f"Skill {st['skills']} | 工具 {st['tools']}")
    print("按型別:", st["reports_by_type"])
    if st["date_range"][0]:
        print("日期跨度:", st["date_range"])

    if args.check:
        print("(--check：未寫檔案)")
        return

    write_json(graph)
    write_markdown(graph)
    print(f"已寫入:\n  {rel(GRAPH_JSON)}\n  {rel(GRAPH_MD)}")


if __name__ == "__main__":
    main()
