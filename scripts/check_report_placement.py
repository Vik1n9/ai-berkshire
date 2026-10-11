#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_report_placement.py — 檢查 reports/ 內報告的存放位置與檔名是否符合 CLAUDE.md 規範。

原則：除非使用者明確要求「跨公司對比」，否則一律每家公司分開放置。

規則：
  1. 單一公司報告一律放在 reports/{公司}/{中文類別}/，檔名為 {公司}-{英文類別詞}-...md，
     檔名開頭的公司名必須等於所在的公司資料夾，英文類別詞必須對應所在的中文類別資料夾。
  2. 上述中文類別資料夾（深度分析、財報分析、買前確認…）內的檔案，檔名必須以
     {公司}-{對應英文類別詞} 開頭，不可混放其他類別或其他公司的報告。
  3. 名稱含 checklist／買前確認／檢查清單、但不符合規則 1 的檔案，只允許放在
     reports/跨公司比較/（即使用者明確要求的跨公司對比）；放在其他位置一律違規。
  4. reports/ 頂層不得直接放檔案。

reports/跨公司比較/ 只能在使用者明確要求跨公司對比時使用。腳本無法判斷使用者意圖，
因此 hook 模式下：用 Write 新建該資料夾內的檔案時改為請使用者確認（permissionDecision=ask）；
Stop 時若該資料夾有未提交的新檔案，提示使用者確認。

用法：
    python3 scripts/check_report_placement.py              # 掃描整個 reports/，違規 exit 1
    python3 scripts/check_report_placement.py PATH ...     # 只檢查指定路徑（可為尚未建立的檔案）
    python3 scripts/check_report_placement.py --hook       # Claude Code hook：從 stdin 讀工具輸入 JSON
"""
from __future__ import annotations

import json
import os
import re
import subprocess
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

# 只有使用者明確要求跨公司對比時才可寫入的資料夾
COMPARISON_DIR = "跨公司比較"

NAME_RE = re.compile(r"^(?P<co>.+?)-(?P<cat>" + "|".join(CATEGORY_DIRS) + r")(?:-|\.md$)")
CHECKLIST_HINT_RE = re.compile(r"checklist|買前確認|檢查清單", re.IGNORECASE)


def _parts(path: str) -> list[str] | None:
    """回傳相對 reports/ 的路徑片段；不在 reports/ 下或非 .md 檔回傳 None。"""
    full = os.path.abspath(path)
    if not full.endswith(".md"):
        return None
    rel = os.path.relpath(full, REPORTS_DIR)
    if rel.startswith(".."):
        return None
    return rel.split(os.sep)


def check_path(path: str) -> list[str]:
    """回傳違規訊息清單；不在 reports/ 下或非 .md 檔回傳空清單。"""
    parts = _parts(path)
    if parts is None:
        return []
    fn = parts[-1]
    shown = "reports/" + "/".join(parts)

    if len(parts) == 1:
        return [f"{shown}：reports/ 頂層不得直接放檔案，單一公司報告放 reports/{{公司}}/{{類別}}/"]

    top = parts[0]
    errs: list[str] = []

    # 規則 1：檔名表示單一公司報告 → 必須在該公司、該類別的資料夾
    m = NAME_RE.match(fn)
    if m:
        co, cat = m.group("co"), m.group("cat")
        want = f"reports/{co}/{CATEGORY_DIRS[cat]}/{fn}"
        if shown != want:
            errs.append(f"{shown}：檔名表示這是 {co} 的 {cat} 報告，應放在 {want}")
    # 規則 3：其他買前確認類檔案只允許出現在跨公司比較（明確要求的跨公司對比）
    elif CHECKLIST_HINT_RE.search("/".join(parts)) and top != COMPARISON_DIR:
        errs.append(
            f"{shown}：買前確認預設每家公司各一份，路徑為 "
            f"reports/{{公司}}/買前確認/{{公司}}-checklist-{{YYYYMMDD}}.md；"
            f"只有使用者明確要求跨公司對比時，才寫入 reports/{COMPARISON_DIR}/"
        )

    # 規則 2：類別資料夾內不得混放其他類別或其他公司（規則 1 已指出應改放位置時不重複報）
    if not errs and len(parts) >= 3 and parts[1] in DIR_CATEGORIES:
        cat = DIR_CATEGORIES[parts[1]]
        if not re.match(rf"^{re.escape(top)}-{cat}(?:-|\.md$)", fn):
            errs.append(f"{shown}：{parts[1]}/ 內的檔名必須以「{top}-{cat}」開頭")

    return errs


def scan_all() -> list[str]:
    errs: list[str] = []
    for dirpath, dirnames, filenames in os.walk(REPORTS_DIR):
        dirnames.sort()
        for fn in sorted(filenames):
            errs.extend(check_path(os.path.join(dirpath, fn)))
    return errs


def new_comparison_files() -> list[str]:
    """跨公司比較/ 內尚未提交（新增或修改）的檔案，供 Stop 時提醒使用者確認。"""
    target = os.path.join("reports", COMPARISON_DIR)
    if not os.path.isdir(os.path.join(ROOT, target)):
        return []
    try:
        out = subprocess.run(
            ["git", "-c", "core.quotepath=false", "status", "--porcelain",
             "--untracked-files=all", "--", target],
            cwd=ROOT, capture_output=True, text=True, timeout=20,
        ).stdout
    except (OSError, subprocess.SubprocessError):
        return []
    return [ln[3:] for ln in out.splitlines() if ln[3:].endswith(".md") and not ln.startswith(" D")]


def hook_main() -> int:
    """PreToolUse(Write|Edit)：違規 exit 2 擋下；新建跨公司比較檔案時請使用者確認。
    Stop：掃描整個 reports/，違規 exit 2 要求修正（stop_hook_active 時只提示，避免迴圈）；
    跨公司比較/ 有未提交的新檔案時提示使用者確認是否為明確要求的跨公司對比。"""
    try:
        data = json.load(sys.stdin)
    except (ValueError, OSError):
        return 0

    if data.get("hook_event_name") == "Stop":
        errs = scan_all()
        pending = new_comparison_files()
        notes = [f"本次 reports/{COMPARISON_DIR}/ 有未提交的檔案：{', '.join(pending)}。"
                 "此資料夾只用於你明確要求的跨公司對比，若非你的指示，請要求改為每家公司分開放置。"] \
            if pending else []
        if errs and not data.get("stop_hook_active"):
            print("報告位置不符規範：\n" + "\n".join(f"- {e}" for e in errs)
                  + "\n請依 CLAUDE.md 報告命名規範移動或拆分檔案後再結束。", file=sys.stderr)
            return 2
        msgs = (["報告位置不符規範：\n" + "\n".join(f"- {e}" for e in errs)] if errs else []) + notes
        if msgs:
            print(json.dumps({"systemMessage": "\n".join(msgs)}, ensure_ascii=False))
        return 0

    tool_input = data.get("tool_input") or {}
    path = tool_input.get("file_path") or tool_input.get("notebook_path") or ""
    if not path:
        return 0
    errs = check_path(path)
    if errs:
        print("報告位置不符規範，已阻止寫入：\n" + "\n".join(f"- {e}" for e in errs), file=sys.stderr)
        return 2
    parts = _parts(path)
    if parts and parts[0] == COMPARISON_DIR and not os.path.exists(path):
        print(json.dumps({"hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": "ask",
            "permissionDecisionReason": (
                f"即將新建 reports/{COMPARISON_DIR}/ 的檔案。此資料夾只用於你明確要求的跨公司對比；"
                "若你沒有下達跨公司對比，請拒絕，報告應每家公司分開放置。"),
        }}, ensure_ascii=False))
    return 0


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
