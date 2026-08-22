#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
report_meta.py — 報告 metadata 推導的共用模組。

供 scripts/add_frontmatter.py（批次補 frontmatter）與後續的索引產生器共用。
抽取規則沿用 scripts/build_graph.py 既有的 TYPE_RULES / TICKER_RE / parse_date
等抽取器，本模組只補上它缺少的部分：

  - YAML frontmatter 解析（極簡，不引入 PyYAML）
  - 表頭日期解析（研究日期：2026年6月24日 等中文格式）
  - 日期四層 fallback：frontmatter → 檔名 → 表頭 → 同目錄兄弟檔 → git commit date
  - 大師視角的簡繁別名比對
  - 依報告類型推導複查週期與新鮮度
  - 穩定的 ASCII slug

設計原則：
  - 僅用 Python 標準庫，無外部依賴。
  - 冪等：同一份檔案多次推導結果一致。
  - 推導不出來就回傳 None，不塞預設值假裝知道。
"""
from __future__ import annotations

import hashlib
import os
import re
import subprocess
import sys
from datetime import date, datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import build_graph as bg  # noqa: E402  重用既有抽取器

ROOT = bg.ROOT

# 掃描根目錄：報告可能散在這幾處
SCAN_ROOTS = ["reports"]

# 四位大師的簡繁別名 → 正規化為繁體（依 CLAUDE.md 的台灣正體規範）
MASTER_ALIASES = {
    "巴菲特": ["巴菲特"],
    "蒙格": ["蒙格", "芒格"],
    "段永平": ["段永平"],
    "李錄": ["李錄", "李录"],
}

# 依報告類型的預設複查週期（天）。None = 不適用（歸檔性質，如公眾號系列文）
REVIEW_DAYS = {
    "news": 14,
    "signal": 14,
    "thesis": 90,
    "portfolio": 90,
    "earnings": 100,
    "research": 180,
    "team": 180,
    "valuation": 180,
    "checklist": 180,
    "management": 180,
    "comparison": 180,
    "private": 180,
    "industry": 365,
    "funnel": 365,
    "series": None,
    "other": 180,
}

# 表頭中的日期寫法，由具體到寬鬆
_HEADER_DATE_PATTERNS = [
    re.compile(r"(20\d{2})\s*年\s*(\d{1,2})\s*月\s*(\d{1,2})\s*日"),
    re.compile(r"(20\d{2})[-/](\d{1,2})[-/](\d{1,2})"),
    re.compile(r"(20\d{2})\s*年\s*(\d{1,2})\s*月"),
]

# 公眾號系列文：reports/{公司}/公众号/《看懂XX》/0N-*.md
_SERIES_RE = re.compile(r"(公众号|公眾號|《看懂)")

# 團隊分析目錄：四大師視角拆檔，整組都算 team
_TEAM_DIR_RE = re.compile(r"(团队分析|團隊分析)")

# build_graph.TYPE_RULES 未涵蓋的檔名關鍵詞（簡繁並列）
_EXTRA_TYPE_RULES = [
    ("research", ["投研报告", "投研報告"]),
]

# 帶交易所前綴的 ticker：（NASDAQ: MRVL）、(NYSE:ABC)
_EXCHANGE_TICKER_RE = re.compile(
    r"[（(]\s*(?:NASDAQ|NYSE|NYSEARCA|AMEX|HKEX|SEHK|TWSE|TPEX|SGX|LSE|TSE)"
    r"\s*[:：]\s*([A-Z]{1,6}(?:\.[A-Z]{1,3})?)\s*[）)]", re.I)

# 表頭中「像 metadata」的行：blockquote、粗體 key-value
_META_LINE_RE = re.compile(r"^(>|\*\*)")


# ---------------------------------------------------------------- frontmatter

def split_frontmatter(text: str) -> tuple[dict, str]:
    """切出 YAML frontmatter。回傳 (欄位 dict, 剩餘正文)。

    極簡解析，只支援 `key: value` 與 `key: [a, b]`。不是完整的 YAML，
    但報告 frontmatter 的規範就限定在這個子集內。
    """
    if not text.startswith("---"):
        return {}, text
    lines = text.split("\n")
    if lines[0].strip() != "---":
        return {}, text
    for i in range(1, len(lines)):
        if lines[i].strip() in ("---", "..."):
            body = "\n".join(lines[i + 1:])
            return _parse_yaml_block(lines[1:i]), body
    return {}, text  # 沒有收尾的 ---，當作沒有 frontmatter


def _parse_yaml_block(lines: list[str]) -> dict:
    out: dict = {}
    for ln in lines:
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        if ":" not in s:
            continue
        k, _, v = s.partition(":")
        k, v = k.strip(), v.strip()
        if not k:
            continue
        # 去掉可能的引號
        if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
            v = v[1:-1]
        if v.startswith("[") and v.endswith("]"):
            inner = v[1:-1].strip()
            items = []
            for part in inner.split(","):
                p = part.strip().strip("\"'")
                if p:
                    items.append(p)
            out[k] = items
        elif v == "":
            out[k] = None
        else:
            out[k] = v
    return out


def dump_frontmatter(meta: dict, order: list[str] | None = None) -> str:
    """把 dict 序列化為 frontmatter 區塊（含前後 ---）。值為 None 的欄位跳過。"""
    keys = order or list(meta.keys())
    lines = ["---"]
    for k in keys:
        if k not in meta:
            continue
        v = meta[k]
        if v is None:
            continue
        if isinstance(v, list):
            if not v:
                continue
            lines.append(f"{k}: [{', '.join(str(x) for x in v)}]")
        else:
            lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------- 讀檔

def read_text(path: str) -> str:
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def header_of(text: str, n: int = 12) -> str:
    """取正文前 n 行當表頭（frontmatter 已切除）。"""
    return "\n".join(text.split("\n")[:n])


def title_of(text: str) -> str | None:
    """取第一個 H1 當標題。"""
    for ln in text.split("\n"):
        s = ln.strip()
        if s.startswith("# "):
            return s[2:].strip()
    return None


# ---------------------------------------------------------------------- 日期

def metadata_lines(header: str) -> list[str]:
    """表頭中屬於 metadata 的行。

    只取 blockquote 與粗體 key-value 行，並在第一條水平線處停止——水平線
    之後就是正文，正文裡的歷史年份（「2022 年 11 月，Meta 跌到 90 美元」）
    不是報告日期。
    """
    out = []
    for ln in header.split("\n"):
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        if s in ("---", "..."):
            break
        if _META_LINE_RE.match(s):
            out.append(s)
    return out


def parse_header_date(header: str) -> str | None:
    """從表頭的 metadata 行撈日期。只認 20xx 年份，避免把股價、市值誤判成日期。"""
    blob = "\n".join(metadata_lines(header))
    for rx in _HEADER_DATE_PATTERNS:
        m = rx.search(blob)
        if not m:
            continue
        g = m.groups()
        y, mo = int(g[0]), int(g[1])
        d = int(g[2]) if len(g) == 3 else 1
        try:
            return datetime(y, mo, d).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def git_commit_date(path: str) -> str | None:
    """該檔最後一次 commit 的日期，作為日期推導的最後手段。

    務必帶 -c core.quotepath=false：git 預設會把含中文的路徑輸出成
    "reports/英伟达/..."（加引號、非 ASCII 轉八進位跳脫），不關掉會導致
    路徑比對失效。
    """
    try:
        out = subprocess.run(
            ["git", "-c", "core.quotepath=false", "log", "-1",
             "--format=%ad", "--date=short", "--", path],
            cwd=ROOT, capture_output=True, text=True, timeout=15,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if out.returncode != 0:
        return None
    s = out.stdout.strip()
    return s if re.fullmatch(r"20\d{2}-\d{2}-\d{2}", s) else None


def sibling_date(path: str) -> str | None:
    """同目錄兄弟檔的日期（取最新）。公眾號系列文常常只有 00-系列說明 帶日期。"""
    d = os.path.dirname(path)
    if not os.path.isdir(d):
        return None
    found = []
    for fn in sorted(os.listdir(d)):
        if not fn.endswith(".md"):
            continue
        full = os.path.join(d, fn)
        if os.path.abspath(full) == os.path.abspath(path):
            continue
        dt = bg.parse_date(fn[:-3])
        if not dt:
            try:
                fm, body = split_frontmatter(read_text(full))
            except OSError:
                continue
            dt = _clean_date(fm.get("date")) or parse_header_date(header_of(body))
        if dt:
            found.append(dt)
    return max(found) if found else None


def _clean_date(v) -> str | None:
    if not v:
        return None
    s = str(v).strip()
    return s if re.fullmatch(r"20\d{2}-\d{2}-\d{2}", s) else None


# ---------------------------------------------------------------- 其他欄位

def derive_masters(name: str, header: str) -> list[str]:
    """比對簡繁兩種寫法，輸出正規化為繁體的大師名單。"""
    blob = name + " " + header
    return [canon for canon, aliases in MASTER_ALIASES.items()
            if any(a in blob for a in aliases)]


def derive_type(relpath: str) -> str:
    """報告類型。

    目錄先於檔名：`团队分析/` 底下的四大師拆檔整組算 team，不能讓
    「02-财务估值分析」這種檔名把它判成 valuation。
    """
    if _SERIES_RE.search(relpath):
        return "series"
    if _TEAM_DIR_RE.search(os.path.dirname(relpath)):
        return "team"
    name_lower = os.path.basename(relpath)[:-3].lower()
    for label, keys in _EXTRA_TYPE_RULES:
        if any(k in name_lower for k in keys):
            return label
    return bg.classify_type(name_lower)


def derive_ticker(header: str) -> str | None:
    """從表頭撈 ticker。先認帶交易所前綴的寫法，再退回 build_graph 的括號規則。"""
    m = _EXCHANGE_TICKER_RE.search(header)
    if m:
        return m.group(1).upper()
    m = bg.TICKER_RE.search(header)
    if m:
        cand = m.group(1).upper()
        if not re.fullmatch(r"20\d{2}", cand) and cand not in bg.TICKER_STOPWORDS:
            return cand
    return None


def derive_company(relpath: str) -> str | None:
    """公司／主題＝掃描根目錄下的第一層目錄名。直屬根目錄的檔案沒有公司歸屬。"""
    parts = relpath.replace(os.sep, "/").split("/")
    if len(parts) < 3:
        return None
    return parts[1]


def review_period(rtype: str) -> int | None:
    return REVIEW_DAYS.get(rtype, REVIEW_DAYS["other"])


def derive_review_by(dt: str | None, rtype: str) -> str | None:
    days = review_period(rtype)
    if not dt or days is None:
        return None
    try:
        base = datetime.strptime(dt, "%Y-%m-%d").date()
    except ValueError:
        return None
    return (base + timedelta(days=days)).strftime("%Y-%m-%d")


def compute_status(review_by: str | None, rtype: str,
                   today: date | None = None) -> str:
    """新鮮度：fresh / review_due / stale。系列文歸檔不計時效。"""
    if rtype == "series":
        return "archived"
    if not review_by:
        return "fresh"
    today = today or date.today()
    try:
        due = datetime.strptime(review_by, "%Y-%m-%d").date()
    except ValueError:
        return "fresh"
    days_over = (today - due).days
    if days_over <= 0:
        return "fresh"
    period = review_period(rtype) or 180
    return "stale" if days_over > period else "review_due"


_ASCII_TOKEN_RE = re.compile(r"[A-Za-z0-9]+")


def make_slug(relpath: str, ticker: str | None, dt: str | None) -> str:
    """穩定、ASCII-safe 的 slug，供前端路由使用。

    以路徑的 sha1 前 6 碼收尾，保證唯一且冪等——同一份報告重跑必得同一個 slug。
    """
    parts = []
    if ticker:
        parts.append(ticker.lower().replace(".", "-"))
    else:
        tokens = _ASCII_TOKEN_RE.findall(os.path.basename(relpath)[:-3])
        tokens = [t.lower() for t in tokens if not re.fullmatch(r"20\d{6}", t)]
        if tokens:
            parts.append("-".join(tokens[:3]))
    if dt:
        parts.append(dt.replace("-", ""))
    h = hashlib.sha1(relpath.encode("utf-8")).hexdigest()[:6]
    parts.append(h)
    slug = "-".join(p for p in parts if p)
    return re.sub(r"-{2,}", "-", slug).strip("-")


# ------------------------------------------------------------------ 主推導

FRONTMATTER_ORDER = [
    "company", "ticker", "type", "date", "status",
    "conviction", "priority", "review_by", "tags",
]


def derive(path: str, use_git: bool = True) -> dict:
    """推導單一報告的 metadata。

    回傳 dict，另含兩個輔助欄位：
      _existing — 檔案原有的 frontmatter（沒有則為 {}）
      _missing  — 推導不出來、需要人工補的必填欄位名稱清單
    """
    relpath = os.path.relpath(os.path.abspath(path), ROOT).replace(os.sep, "/")
    text = read_text(path)
    fm, body = split_frontmatter(text)
    header = header_of(body)
    name = os.path.basename(relpath)[:-3]

    rtype = fm.get("type") or derive_type(relpath)
    company = fm.get("company") or derive_company(relpath)

    ticker = fm.get("ticker") or derive_ticker(header)

    # 日期四層 fallback
    dt = _clean_date(fm.get("date"))
    if not dt:
        dt = bg.parse_date(name)
    if not dt:
        dt = parse_header_date(header)
    if not dt:
        dt = sibling_date(path)
    if not dt and use_git:
        dt = git_commit_date(relpath)

    review_by = _clean_date(fm.get("review_by")) or derive_review_by(dt, rtype)

    meta = {
        "company": company,
        "ticker": ticker,
        "type": rtype,
        "date": dt,
        "status": fm.get("status") or compute_status(review_by, rtype),
        # conviction / priority 是人工判斷，推導不出來就留空，不猜
        "conviction": fm.get("conviction"),
        "priority": fm.get("priority"),
        "review_by": review_by,
        "tags": fm.get("tags") or [],
    }
    meta["_existing"] = fm
    meta["_missing"] = [k for k in ("company", "date") if not meta.get(k)]
    meta["_path"] = relpath
    meta["_title"] = title_of(body)
    meta["_quarter"] = fm.get("quarter") or bg.parse_quarter(name)
    meta["_masters"] = derive_masters(name, header)
    meta["_slug"] = make_slug(relpath, ticker, dt)
    return meta


def iter_reports(roots: list[str] | None = None):
    """走訪掃描根目錄下的所有 .md（跳過 README.md）。"""
    for root in (roots or SCAN_ROOTS):
        base = os.path.join(ROOT, root)
        if not os.path.isdir(base):
            continue
        for dirpath, dirnames, filenames in os.walk(base):
            dirnames.sort()
            for fn in sorted(filenames):
                if fn.endswith(".md") and fn != "README.md":
                    yield os.path.join(dirpath, fn)
