#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
query_graph.py — 查询 AI Berkshire 专案知识图谱（data/project_graph.json）。

先运行 `python3 scripts/build_graph.py` 生成图谱，再用本工具查询。

用法示例：
    python3 scripts/query_graph.py stats                # 总览统计
    python3 scripts/query_graph.py companies            # 列出所有实体（按报告数）
    python3 scripts/query_graph.py company 腾讯          # 某公司的全部报告
    python3 scripts/query_graph.py type earnings        # 某类型的全部报告
    python3 scripts/query_graph.py master 段永平         # 命中某大师视角的报告
    python3 scripts/query_graph.py ticker 00700         # 按 ticker 查
    python3 scripts/query_graph.py search 护城河         # 按标题/路径关键词模糊查
    python3 scripts/query_graph.py skills               # 列出 Skill 目录
    python3 scripts/query_graph.py recent 20            # 最近 N 份（按日期）
"""
from __future__ import annotations

import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRAPH_JSON = os.path.join(ROOT, "data", "project_graph.json")


def load():
    if not os.path.exists(GRAPH_JSON):
        sys.exit("未找到 data/project_graph.json，请先运行: python3 scripts/build_graph.py")
    with open(GRAPH_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def fmt(r):
    bits = [r["date"] or "        ", f"[{r['type']}]"]
    if r.get("ticker"):
        bits.append(r["ticker"])
    return f"  {' '.join(bits)}  {r['path']}"


def cmd_stats(g, _):
    s = g["stats"]
    print(f"报告 {s['reports']} | 实体 {s['entities']} | Skill {s['skills']} | 工具 {s['tools']}")
    print(f"日期跨度 {s['date_range'][0]} ~ {s['date_range'][1]}")
    print("按类型:")
    for t, c in s["reports_by_type"].items():
        print(f"  {t:12} {c}")
    print("按大师:")
    for m, c in s["reports_by_master"].items():
        print(f"  {m:8} {c}")


def cmd_companies(g, args):
    n = int(args[0]) if args else 9999
    ents = sorted(g["entities"], key=lambda e: -e["report_count"])
    for e in ents[:n]:
        tick = f" ({'/'.join(e['tickers'])})" if e["tickers"] else ""
        print(f"  {e['report_count']:4}  {e['name']}{tick}")


def cmd_company(g, args):
    if not args:
        sys.exit("用法: query_graph.py company <公司名关键词>")
    kw = args[0]
    hits = [r for r in g["reports"] if kw in r["entity"]]
    if not hits:
        print(f"未找到实体包含「{kw}」的报告")
        return
    hits.sort(key=lambda r: (r["date"] or "0000-00-00"), reverse=True)
    print(f"「{kw}」相关报告 {len(hits)} 份:")
    for r in hits:
        print(fmt(r))


def cmd_type(g, args):
    if not args:
        sys.exit("用法: query_graph.py type <research|earnings|thesis|...>")
    t = args[0]
    hits = [r for r in g["reports"] if r["type"] == t]
    hits.sort(key=lambda r: (r["date"] or "0000-00-00"), reverse=True)
    print(f"类型「{t}」报告 {len(hits)} 份:")
    for r in hits:
        print(fmt(r))


def cmd_master(g, args):
    if not args:
        sys.exit("用法: query_graph.py master <巴菲特|芒格|段永平|李录>")
    m = args[0]
    hits = [r for r in g["reports"] if m in r["masters"]]
    hits.sort(key=lambda r: (r["date"] or "0000-00-00"), reverse=True)
    print(f"命中「{m}」视角报告 {len(hits)} 份:")
    for r in hits:
        print(fmt(r))


def cmd_ticker(g, args):
    if not args:
        sys.exit("用法: query_graph.py ticker <代码，如 00700 / 600519>")
    kw = args[0].upper()
    hits = [r for r in g["reports"] if r.get("ticker") and kw in r["ticker"]]
    hits.sort(key=lambda r: (r["date"] or "0000-00-00"), reverse=True)
    print(f"ticker 含「{kw}」报告 {len(hits)} 份:")
    for r in hits:
        print(fmt(r))


def cmd_search(g, args):
    if not args:
        sys.exit("用法: query_graph.py search <关键词>")
    kw = args[0]
    hits = [r for r in g["reports"] if kw in r["title"] or kw in r["path"]]
    hits.sort(key=lambda r: (r["date"] or "0000-00-00"), reverse=True)
    print(f"标题/路径含「{kw}」报告 {len(hits)} 份:")
    for r in hits:
        print(fmt(r))


def cmd_skills(g, _):
    for sk in g["skills"]:
        print(f"  /{sk['name']}\n      {sk['desc'][:100]}")


def cmd_recent(g, args):
    n = int(args[0]) if args else 20
    hits = [r for r in g["reports"] if r["date"]]
    hits.sort(key=lambda r: r["date"], reverse=True)
    for r in hits[:n]:
        print(fmt(r))


COMMANDS = {
    "stats": cmd_stats, "companies": cmd_companies, "company": cmd_company,
    "type": cmd_type, "master": cmd_master, "ticker": cmd_ticker,
    "search": cmd_search, "skills": cmd_skills, "recent": cmd_recent,
}


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in COMMANDS:
        print(__doc__)
        sys.exit(0)
    g = load()
    COMMANDS[sys.argv[1]](g, sys.argv[2:])


if __name__ == "__main__":
    main()
