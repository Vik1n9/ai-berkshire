#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
add_frontmatter.py — 批次為報告推導並寫入 YAML frontmatter。

對應的工作流程：先人工整理報告取捨並上傳到 reports/，再用本工具自動推導
metadata，最後人工校正推導不出來的部分。

    python3 scripts/add_frontmatter.py --dry-run           # 只印出會寫什麼，不動檔案
    python3 scripts/add_frontmatter.py --apply             # 實際寫入
    python3 scripts/add_frontmatter.py --apply --only reports/輝達
    python3 scripts/add_frontmatter.py --apply --force     # 覆寫已有的 frontmatter

原則：
  - 已有 frontmatter 的檔案預設跳過，除非 --force。
  - conviction / priority 是人工判斷，一律留空，不猜。
  - 推導不出 company 或 date 的檔案會列在結尾，供人工補，不塞預設值。
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import report_meta as rm  # noqa: E402


def collect(only: str | None) -> list[str]:
    if not only:
        return list(rm.iter_reports())
    target = only if os.path.isabs(only) else os.path.join(rm.ROOT, only)
    if os.path.isfile(target):
        return [target]
    if os.path.isdir(target):
        rel = os.path.relpath(target, rm.ROOT).replace(os.sep, "/")
        return list(rm.iter_reports([rel]))
    sys.exit(f"找不到路徑：{only}")


def build_block(meta: dict) -> str:
    out = {k: meta.get(k) for k in rm.FRONTMATTER_ORDER}
    return rm.dump_frontmatter(out, rm.FRONTMATTER_ORDER)


def write_frontmatter(path: str, block: str) -> None:
    text = rm.read_text(path)
    _, body = rm.split_frontmatter(text)
    with open(path, "w", encoding="utf-8") as f:
        f.write(block + "\n" + body.lstrip("\n"))


def main() -> int:
    ap = argparse.ArgumentParser(
        description="批次為報告推導並寫入 frontmatter",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--dry-run", action="store_true", help="只印出會寫入什麼，不動檔案")
    g.add_argument("--apply", action="store_true", help="實際寫入檔案")
    ap.add_argument("--only", metavar="PATH", help="限定單一檔案或目錄")
    ap.add_argument("--force", action="store_true", help="覆寫已有的 frontmatter")
    ap.add_argument("--no-git", action="store_true",
                    help="不使用 git commit date 作為日期的最後手段（較快）")
    args = ap.parse_args()

    files = collect(args.only)
    if not files:
        print("沒有找到任何報告（reports/ 是空的？）")
        return 0

    written = skipped = 0
    incomplete: list[tuple[str, list[str]]] = []

    for path in files:
        meta = rm.derive(path, use_git=not args.no_git)
        rel = meta["_path"]

        if meta["_existing"] and not args.force:
            skipped += 1
            continue

        block = build_block(meta)
        if meta["_missing"]:
            incomplete.append((rel, meta["_missing"]))

        if args.dry_run:
            print(f"\n── {rel}")
            print(block, end="")
        else:
            write_frontmatter(path, block)
        written += 1

    verb = "會寫入" if args.dry_run else "已寫入"
    print(f"\n{'=' * 60}")
    print(f"{verb} {written} 份　跳過（已有 frontmatter）{skipped} 份　共 {len(files)} 份")

    if incomplete:
        print(f"\n⚠ 以下 {len(incomplete)} 份推導不完整，需要人工補上：")
        for rel, missing in incomplete:
            print(f"   {rel}  ← 缺 {'、'.join(missing)}")

    if args.dry_run and written:
        print("\n確認無誤後改用 --apply 實際寫入。")
    if not args.dry_run and written:
        print("\n提醒：conviction / priority 屬人工判斷，未自動填入，請自行補上。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
