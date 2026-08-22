# reports/ — 研究報告目錄

所有 Skill 的報告統一寫入此目錄。**md 檔本身是唯一真相**（single source of truth），
索引與前端都是可隨時重建的衍生產物，刪掉不會掉資料。

## 目錄結構

公司／主題各一個子目錄，報告放在其下；跨公司的主題報告放根目錄。

```
reports/
├── 輝達/
│   ├── 投研報告/20260426-投研報告-輝達-安全墊分析.md
│   ├── 團隊分析/01-商業模式分析-段永平視角.md
│   │              …04-風險管理層評估-李錄視角.md
│   │              最終報告.md
│   └── 公眾號/《看懂輝達》/01-開篇-….md
├── AI產業研究/
│   └── AI五層蛋糕-產業全景研究-20260605.md
├── community/            — 社群投稿（見 CONTRIBUTING.md）
├── AI算力-funnel-20260509.md      — 漏斗篩選報告放根目錄
└── 多公司對比-checklist-20260408.md — 多公司報告放根目錄
```

命名規範見 [`CLAUDE.md`](../CLAUDE.md) 的「報告命名規範」表。

## frontmatter（必要）

每份報告開頭第一行起必須是 YAML frontmatter：

```yaml
---
company: 輝達
ticker: NVDA
type: research
date: 2026-08-22
status: active
conviction: 4
priority: high
review_by: 2027-02-22
tags: [AI算力, 半導體]
---
```

完整欄位定義、type 取值與複查週期見 [`CLAUDE.md`](../CLAUDE.md) 的
「報告 frontmatter 規範」。GitHub 會把 frontmatter 渲染成表格，不影響 md 直接閱讀。

## 上傳報告後的流程

```bash
python3 scripts/add_frontmatter.py --dry-run   # 先看推導結果
python3 scripts/add_frontmatter.py --apply     # 確認無誤後寫入
```

推導規則（優先序由高到低）：

| 欄位 | 推導方式 |
|------|---------|
| `date` | frontmatter → 檔名 `YYYYMMDD` → 表頭 metadata 行 → 同目錄兄弟檔 → git commit 日期 |
| `company` | frontmatter → `reports/` 下的第一層目錄名 |
| `type` | frontmatter → 目錄（`公眾號/`→series、`團隊分析/`→team）→ 檔名關鍵詞 |
| `ticker` | frontmatter → 表頭括號，含 `（NASDAQ: MRVL）` 這類交易所前綴寫法 |
| `review_by` | frontmatter → 依 `type` 的預設複查週期自動推導 |

兩點注意：

- **`conviction` 與 `priority` 不會被自動填入**——它們是人工判斷，需自行補上。
- 表頭日期只掃 metadata 行（`>` 開頭或 `**粗體**`），且在第一條水平線處停止。
  正文裡的歷史年份（例如「2022 年 11 月，Meta 跌到 90 美元」）不會被誤判為報告日期。

## 歷史報告

本目錄曾存有 713 份報告，於重整時清空，**完整保留在 git 歷史中**：

```bash
git checkout fc17867 -- reports/          # 整包取回
git show fc17867:reports/Meta/团队分析/最终报告.md   # 取回單一檔案
```
