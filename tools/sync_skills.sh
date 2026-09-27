#!/usr/bin/env bash
# 把本倉庫 skills/*.md 同步到 Claude Code 的指令目錄（預設 ~/.claude/commands/）。
# 用法：bash tools/sync_skills.sh [目標目錄]
# 只覆蓋同名檔案，不刪除目標目錄中的其他檔案；同步前後列出差異，方便確認。
set -euo pipefail
SRC="$(cd "$(dirname "$0")/.." && pwd)/skills"
DST="${1:-$HOME/.claude/commands}"
mkdir -p "$DST"
changed=0
for f in "$SRC"/*.md; do
  name="$(basename "$f")"
  if [ ! -f "$DST/$name" ] || ! cmp -s "$f" "$DST/$name"; then
    cp "$f" "$DST/$name"
    echo "已更新：$name"
    changed=$((changed + 1))
  fi
done
echo "完成：$changed 個檔案更新，目標目錄 $DST"
