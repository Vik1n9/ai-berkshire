#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_graph.py — 为 AI Berkshire 专案建立知识图谱，便于后续查询。

扫描 reports/ skills/ tools/ data/，抽取实体（公司/行业/主题）、报告、
Skill、工具，构建节点+边的图谱，输出：

  data/project_graph.json   机器可读知识图谱（供 query_graph.py / RAG 查询）
  docs/PROJECT_GRAPH.md      人类可读索引（公司→报告清单、Skill 目录、统计）

设计原则：
  - 仅用 Python 标准库，无外部依赖，随时可重跑（报告持续新增）。
  - 元数据从「文件名约定 + 表头轻量扫描」抽取，不做重推断。
  - 幂等：同一份代码库多次运行结果一致。

用法：
    python3 scripts/build_graph.py            # 生成图谱
    python3 scripts/build_graph.py --check    # 只校验、打印统计，不写文件
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

# 四位投资大师视角
MASTERS = ["巴菲特", "芒格", "段永平", "李录"]

# 报告类型识别规则：(类型标签, 文件名匹配关键词列表)
# 顺序敏感：越具体的规则越靠前。
TYPE_RULES = [
    ("earnings", ["earnings", "财报电话会", "财报精读", "-earnings-", "季报", "年报点评"]),
    ("thesis", ["thesis", "-论文", "投资论文", "投资论述"]),
    ("management", ["management", "管理层", "高管", "-mgmt-"]),
    ("valuation", ["valuation", "估值", "dcf", "公允价值", "fair_value", "内在价值"]),
    ("team", ["-team-", "investment-team", "最终报告", "四大师"]),
    ("private", ["private", "未上市", "招股书", "ipo"]),
    ("checklist", ["checklist", "检查清单", "镜子测试"]),
    ("industry", ["industry", "行业研究", "-行业-", "产业全景", "产业链", "全景研究"]),
    ("funnel", ["funnel", "漏斗", "筛选", "召回池", "候选池", "选股", "screen"]),
    ("news", ["news", "-新闻-", "news-pulse", "-快讯-", "政策解读"]),
    ("portfolio", ["portfolio", "投资组合", "组合报告", "持仓", "13f"]),
    ("comparison", ["对比", "vs", "相关性", "轮动", "对决", "换仓", "allin"]),
    ("research", ["research", "investment-research", "深度研究", "深度分析",
                  "研究报告", "投资研究", "-研究-", "deep-dive", "deep_dive"]),
]

# 文件名 → Skill 名（对应 skills/*.md）
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

# ticker：表头里 （00700.HK） (2449) （600519.SH） 等
TICKER_RE = re.compile(r"[（(]\s*([0-9]{3,6}(?:\.[A-Za-z]{1,3})?|[A-Z]{1,5}(?:\.[A-Z]{1,3})?)\s*[）)]")
# 括号内常见的「非 ticker」大写缩写（财务术语/交易所/口径），需过滤
TICKER_STOPWORDS = {
    "TTM", "TTMPE", "NYSE", "NASDAQ", "HKEX", "SEHK", "DCF", "PE", "PB", "PS",
    "ROE", "ROIC", "GDP", "CPI", "AI", "ETF", "IPO", "FCF", "EPS", "YOY", "QOQ",
    "HK", "US", "USD", "RMB", "CNY", "EV", "GAAP", "GMV", "ARPU", "MAU", "DAU",
    "CEO", "CFO", "VIE", "SEC", "PPT", "FY", "Q1", "Q2", "Q3", "Q4",
}
# 文件名中的日期：20260408 / 2026-04-08
DATE8_RE = re.compile(r"(20\d{2})[-_]?(\d{2})[-_]?(\d{2})")
# 财报期间：2025Q4 / 2026Q1 / 2025年报
QUARTER_RE = re.compile(r"(20\d{2})\s*(Q[1-4]|年报|中报|半年报|一季报|三季报)", re.IGNORECASE)


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
    """读前若干行，返回 (原始表头文本, ticker)。容错编码问题。"""
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            head = "".join([next(f, "") for _ in range(10)])
    except (OSError, StopIteration):
        return "", None
    ticker = None
    m = TICKER_RE.search(head)
    if m:
        cand = m.group(1).upper()
        # 过滤纯年份、财务缩写/交易所等噪声
        if not re.fullmatch(r"20\d{2}", cand) and cand not in TICKER_STOPWORDS:
            ticker = cand
    return head, ticker


def build_report_nodes():
    """扫描 reports/，返回 (reports, entities)。"""
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

            # 实体：reports/ 直属文件归为「_root」（主题/多公司报告），
            # 子目录文件归到目录名（公司/主题）。
            sub = os.path.relpath(dirpath, REPORTS_DIR)
            if sub == ".":
                entity = "_专题与多公司"
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
    """取 Skill/文档首个非标题正文段作为简述。"""
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
        # 跳过空行、标题、frontmatter 分隔线/字段
        if not s or s.startswith("#") or s in ("---", "...") or s.startswith("> "):
            continue
        if re.match(r"^[A-Za-z_]+:\s", s):  # yaml frontmatter 字段
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
            # 抓模块 docstring 首行
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

    # 统计
    by_type = Counter(r["type"] for r in reports)
    by_skill = Counter(r["skill"] for r in reports if r["skill"])
    by_master = Counter(m for r in reports for m in r["masters"])
    dated = [r["date"] for r in reports if r["date"]]

    graph = {
        "meta": {
            "project": "AI Berkshire",
            "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            "generator": "scripts/build_graph.py",
            "note": "价值投资研究知识图谱：公司/主题实体 + 报告 + Skill + 工具。可用 scripts/query_graph.py 查询。",
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
    "research": "投研报告", "thesis": "投资论文", "earnings": "财报精读",
    "management": "管理层研究", "valuation": "估值", "team": "团队研究",
    "private": "未上市研究", "checklist": "检查清单", "industry": "行业研究",
    "funnel": "筛选/漏斗", "news": "新闻/时事", "portfolio": "组合/持仓",
    "comparison": "对比/轮动", "other": "其他",
}


def write_markdown(graph):
    os.makedirs(DOCS_DIR, exist_ok=True)
    s = graph["stats"]
    lines = []
    A = lines.append
    A("# AI Berkshire 专案图谱（PROJECT GRAPH）\n")
    A("> 自动生成，请勿手工编辑。运行 `python3 scripts/build_graph.py` 重新生成。")
    A(f"> 生成时间：{graph['meta']['generated_at']}\n")
    A("本图谱为专案的**查询索引**：把散落在 `reports/` 的 2000+ 份报告，")
    A("按「公司/主题实体 → 报告」组织，并附 Skill 与工具目录，便于后续检索。\n")
    A("机器可读版本见 [`data/project_graph.json`](../data/project_graph.json)，")
    A("命令行查询用 [`scripts/query_graph.py`](../scripts/query_graph.py)。\n")

    A("## 总览统计\n")
    A(f"- 报告总数：**{s['reports']}**")
    A(f"- 实体（公司/主题）数：**{s['entities']}**")
    A(f"- Skill 数：**{s['skills']}**，工具数：**{s['tools']}**")
    if s["date_range"][0]:
        A(f"- 报告日期跨度：{s['date_range'][0]} ~ {s['date_range'][1]}")
    A("")
    A("**按报告类型：**\n")
    A("| 类型 | 数量 |")
    A("|------|------|")
    for t, c in s["reports_by_type"].items():
        A(f"| {TYPE_LABELS.get(t, t)} (`{t}`) | {c} |")
    A("")
    if s["reports_by_master"]:
        A("**按大师视角（文件命中）：** " +
          " ／ ".join(f"{m} {c}" for m, c in s["reports_by_master"].items()) + "\n")

    # Skill 目录
    A("## Skill 目录\n")
    A("| Skill | 简述 |")
    A("|-------|------|")
    for sk in graph["skills"]:
        desc = sk["desc"].replace("|", "\\|")[:80]
        A(f"| `/{sk['name']}` | {desc} |")
    A("")

    # 工具目录
    A("## 工具目录（tools/）\n")
    A("| 工具 | 说明 |")
    A("|------|------|")
    for tl in graph["tools"]:
        desc = tl["desc"].replace("|", "\\|")[:90]
        A(f"| `{tl['name']}` | {desc} |")
    A("")

    # 实体索引
    A("## 实体索引（公司 / 主题 → 报告）\n")
    A("按报告数量降序。点击路径可直达。\n")
    reports_by_id = {r["id"]: r for r in graph["reports"]}
    ents = sorted(graph["entities"], key=lambda e: (-e["report_count"], e["name"]))
    for e in ents:
        tick = f" `{'/'.join(e['tickers'])}`" if e["tickers"] else ""
        A(f"### {e['name']}{tick} — {e['report_count']} 份\n")
        rs = [reports_by_id[i] for i in e["reports"]]
        # 按日期倒序（无日期排最后）
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
    ap = argparse.ArgumentParser(description="构建 AI Berkshire 专案知识图谱")
    ap.add_argument("--check", action="store_true", help="只打印统计，不写文件")
    args = ap.parse_args()

    graph = build_graph()
    st = graph["stats"]
    print("=== AI Berkshire 图谱统计 ===")
    print(f"报告 {st['reports']} | 实体 {st['entities']} | "
          f"Skill {st['skills']} | 工具 {st['tools']}")
    print("按类型:", st["reports_by_type"])
    if st["date_range"][0]:
        print("日期跨度:", st["date_range"])

    if args.check:
        print("(--check：未写文件)")
        return

    write_json(graph)
    write_markdown(graph)
    print(f"已写入:\n  {rel(GRAPH_JSON)}\n  {rel(GRAPH_MD)}")


if __name__ == "__main__":
    main()
