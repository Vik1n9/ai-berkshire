#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_report_placement.py — 檢查 reports/ 內報告的存放位置與檔名是否符合 CLAUDE.md 規範。

規則（與 CLAUDE.md「報告輸出目錄」「報告命名規範」一致）：
  1. 單一公司報告一律放在 reports/{公司}/{中文類別}/，檔名為 {公司}-{英文類別詞}-...md，
     檔名開頭的公司名必須等於所在的公司資料夾，英文類別詞必須對應所在的中文類別資料夾。
  2. 上述中文類別資料夾（深度分析、財報分析、買前確認…）內的檔案，檔名必須以
     {公司}-{對應英文類別詞} 開頭，不可混放其他類別或其他公司的報告。
  3. 買前確認（checklist）沒有「多公司合併」形式：一次分析多家公司時，每家各寫一份
     reports/{公司}/買前確認/{公司}-checklist-{YYYYMMDD}.md。檔名或路徑含 checklist／
     買前確認／檢查清單的檔案，只要不符合上述位置就判為違規。
  4. reports/ 頂層只允許公司資料夾與保留的非個股資料夾（產業研究、組合管理、訊號掃描）；
     不得直接放檔案，也不得建立 跨公司比較/ 等未列入的非個股資料夾。

用法：
    python3 scripts/check_report_placement.py              # 掃描整個 reports/，違規 exit 1
    python3 scripts/check_report_placement.py PATH ...     # 只檢查指定路徑（可為尚未建立的檔案）
    python3 scripts/check_report_placement.py --hook       # Claude Code hook：從 stdin 讀工具輸入 JSON
"""
from __future__ import annotations

import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPORTS_DIR = os.path.join(ROOT, "reports")

# 英文類別詞 → 中文類別資料夾（CLAUDE.md 報告命名規範）
CATEGORY_DIRS = {
    "research": "深度分析",
    "earnings": "財報分析",
    "management": "管理層分析",
    "thesis": "投資論點",
    "checklist": "買前確認",
    "news": "新聞追蹤",
    "valuation": "估值分析",
    "topic": "專題研究",
    "reference": "參考資料",
}
DIR_CATEGORIES = {v: k for k, v in CATEGORY_DIRS.items()}

# reports/ 頂層允許的非個股資料夾
NON_COMPANY_DIRS = {"產業研究", "組合管理", "訊號掃描"}
# 明確停用的資料夾（曾用於多公司買前確認合併檔）
RETIRED_DIRS = {"跨公司比較": "買前確認一律每家公司各一份，放在 reports/{公司}/買前確認/"}

NAME_RE = re.compile(r"^(?P<co>.+?)-(?P<cat>" + "|".join(CATEGORY_DIRS) + r")(?:-|\.md$)")
CHECKLIST_HINT_RE = re.compile(r"checklist|買前確認|檢查清單", re.IGNORECASE)


def expected_path(co: str, cat: str, fn: str) -> str:
    return f"reports/{co}/{CATEGORY_DIRS[cat]}/{fn}"


def check_path(path: str) -> list[str]:
    """回傳違規訊息清單；不在 reports/ 下或非 .md 檔回傳空清單。"""
    full = os.path.abspath(path)
    if not full.endswith(".md"):
        return []
    rel = os.path.relpath(full, REPORTS_DIR)
    if rel.startswith(".."):
        return []
    parts = rel.split(os.sep)
    fn = parts[-1]
    shown = "reports/" + "/".join(parts)
    errs: list[str] = []

    if len(parts) == 1:
        return [f"{shown}：reports/ 頂層不得直接放檔案，單一公司報告放 reports/{{公司}}/{{類別}}/"]

    top = parts[0]
    if top in RETIRED_DIRS:
        errs.append(f"{shown}：reports/{top}/ 已停用（{RETIRED_DIRS[top]}）")

    m = NAME_RE.match(fn)
    if m:
        co, cat = m.group("co"), m.group("cat")
        want = expected_path(co, cat, fn)
        if shown != want:
            errs.append(f"{shown}：檔名表示這是 {co} 的 {cat} 報告，應放在 {want}")
    elif CHECKLIST_HINT_RE.search(rel):
        errs.append(
            f"{shown}：買前確認必須每家公司各一份，路徑為 "
            f"reports/{{公司}}/買前確認/{{公司}}-checklist-{{YYYYMMDD}}.md，不做多公司合併檔"
        )

    # 規則 2：類別資料夾內不得混放其他類別或其他公司（規則 1 已指出應改放位置時不重複報）
    if not errs and len(parts) >= 3 and parts[1] in DIR_CATEGORIES:
        cat = DIR_CATEGORIES[parts[1]]
        if not re.match(rf"^{re.escape(top)}-{cat}(?:-|\.md$)", fn):
            errs.append(f"{shown}：{parts[1]}/ 內的檔名必須以「{top}-{cat}」開頭")

    return errs


def scan_all() -> list[str]:
    errs: list[str] = []
    if not os.path.isdir(REPORTS_DIR):
        return errs
    for name in sorted(os.listdir(REPORTS_DIR)):
        full = os.path.join(REPORTS_DIR, name)
        if os.path.isdir(full) and name in RETIRED_DIRS and not any(
            f.endswith(".md") for _, _, fs in os.walk(full) for f in fs
        ):
            errs.append(f"reports/{name}/：已停用的資料夾（{RETIRED_DIRS[name]}），請刪除")
    for dirpath, dirnames, filenames in os.walk(REPORTS_DIR):
        dirnames.sort()
        for fn in sorted(filenames):
            errs.extend(check_path(os.path.join(dirpath, fn)))
    return errs


def hook_main() -> int:
    """PreToolUse(Write|Edit)：違規就以 exit 2 擋下並把原因回饋給 Claude。
    Stop：掃描整個 reports/，違規就 exit 2 要求修正（stop_hook_active 時只提示，避免迴圈）。"""
    try:
        data = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0
    event = data.get("hook_event_name", "")
    if event == "Stop":
        errs = scan_all()
        if not errs:
            return 0
        msg = "報告位置不符規範：\n" + "\n".join(f"- {e}" for e in errs)
        if data.get("stop_hook_active"):
            print(json.dumps({"systemMessage": msg}, ensure_ascii=False))
            return 0
        print(msg + "\n請依 CLAUDE.md 報告命名規範移動或拆分檔案後再結束。", file=sys.stderr)
        return 2
    tool_input = data.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not path:
        return 0
    errs = check_path(path)
    if not errs:
        return 0
    print("報告位置不符規範，已阻止寫入：\n" + "\n".join(f"- {e}" for e in errs), file=sys.stderr)
    return 2


def main(argv: list[str]) -> int:
    if "--hook" in argv:
        return hook_main()
    paths = [a for a in argv if not a.startswith("--")]
    errs = [e for p in paths for e in check_path(p)] if paths else scan_all()
    if errs:
        print("報告位置不符規範：")
        for e in errs:
            print(f"  ❌ {e}")
        return 1
    print("報告位置檢查通過")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
