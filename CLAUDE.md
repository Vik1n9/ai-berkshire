# AI Berkshire — 專案指令

## 專案概述

基於 Claude Code 的價值投資研究 Skill 合集。四大師框架：巴菲特、蒙格、段永平、李錄。
上游原倉庫：xbtlin/ai-berkshire。**本倉庫（Vik1n9/ai-berkshire）為其分支，定位為個人使用**：
一律使用繁體中文（台灣正體），研究標的聚焦美股與台股公開發行公司，不追求對外開源專案的
多語言/社群貢獻維護（README_EN.md、README_JA.md 為既有內容保留，非本倉庫維護重點）。

## 專案結構

```
skills/          — 投研 Skill 定義（.md），複製到 ~/.claude/commands/ 使用
tools/           — 輔助工具（financial_rigor.py 精確計算）
REPORT/          — 研究報告輸出目錄（僅限美股與台股公開發行公司）
PRIVATE/         — 非公開發行公司研究（如未上市新創），不計入 REPORT/
assets/          — 圖片等靜態資源
```

## 報告輸出目錄

所有 Skill 的報告統一寫入本倉庫內的 `REPORT/`。**REPORT/ 只收錄美股與台股的公開發行公司報告**，其餘（非公開發行公司、產業/跨公司比較、方法論筆記、人物語錄等）不放在這裡（見下方「非個股內容」）。

結構為 `REPORT/{股票名稱}/{報告類別}/{報告內容}`：

```
REPORT/
├── 台積電/
│   ├── 深度分析/台積電-research-20260408.md
│   ├── 財報分析/台積電-earnings-2025Q4.md
│   ├── 管理層分析/台積電-management-20260409.md
│   ├── 投資論點/台積電-thesis.md
│   ├── 團隊分析/最終報告.md
│   └── 公眾號文章/01-開篇-....md
├── NVIDIA/
│   └── ...（同上，類別依實際產出的報告種類建立）
├── 產業研究/           — 跨公司產業研究、篩選漏斗、產業主題公眾號（非單一個股）
├── 跨公司比較/          — 多公司 Checklist 對比
├── 組合管理/portfolio-latest.md — 持倉組合報告（持續更新）
└── 訊號掃描/bottleneck-map/    — 瓶頸訊號掃描日誌
```

`{報告類別}` 依報告性質命名，常見類別：深度分析、財報分析、管理層分析、投資論點、團隊分析、公眾號文章、Checklist、估值分析、專題研究、新聞追蹤、參考資料。無對應類別時可依需要新增，維持繁體中文命名。

`{股票名稱}` 命名規則：**美股用公司英文名（如 NVIDIA、Microsoft、Micron、Adobe、GE Vernova），台股用中文名（如 台積電、京元電子）**，與各股票市場的慣用稱呼一致。建立新公司資料夾前，先確認命名與此規則一致，不要中英文混用或用中文翻譯名稱替代美股公司英文名。

## 報告命名規範

| Skill | 輸出位置 | 範例 |
|------|---------|------|
| /investment-team | `REPORT/{公司名}/團隊分析/` 目錄內含 4 個視角＋最終報告 | `REPORT/台積電/團隊分析/最終報告.md` |
| /investment-research | `REPORT/{公司名}/深度分析/{公司名}-research-{YYYYMMDD}.md` | `REPORT/台積電/深度分析/台積電-research-20260408.md` |
| /investment-checklist | 單一公司：`REPORT/{公司名}/Checklist/`；多公司：`REPORT/跨公司比較/` | `REPORT/台積電/Checklist/巴菲特Checklist-台積電.md` |
| /industry-research | `REPORT/產業研究/{行業名}-industry-{YYYYMMDD}.md` | `REPORT/產業研究/核電-industry-20260409.md` |
| /industry-funnel | `REPORT/產業研究/{行業名}-funnel-{YYYYMMDD}.md` | `REPORT/產業研究/AI算力-funnel-20260509.md` |
| /private-company-research | `PRIVATE/{公司名}/{公司名}-private-{YYYYMMDD}.md`（非公開發行，不進 REPORT/） | `PRIVATE/位元組跳動/位元組跳動-private-20260408.md` |
| /earnings-review | `REPORT/{公司名}/財報分析/{公司名}-earnings-{期間}.md` | `REPORT/台積電/財報分析/台積電-earnings-2025Q4.md` |
| /earnings-team | `REPORT/{公司名}/財報分析/` 目錄內含 4 個大師視角＋研究底稿＋公眾號文章＋讀者評審 | `REPORT/台積電/財報分析/台積電-earnings-2025Q4.md`（公眾號定稿） |
| /thesis-tracker | `REPORT/{公司名}/投資論點/{公司名}-thesis.md`（長期維護） | `REPORT/台積電/投資論點/台積電-thesis.md` |
| /portfolio-review | `REPORT/組合管理/portfolio-latest.md`（持續更新） | `REPORT/組合管理/portfolio-latest.md` |
| /management-deep-dive | `REPORT/{公司名}/管理層分析/{公司名}-management-{YYYYMMDD}.md` | `REPORT/台積電/管理層分析/台積電-management-20260409.md` |
| /deep-company-series、/wechat-article（投資主題） | `REPORT/{公司名}/公眾號文章/` | `REPORT/台積電/公眾號文章/01-開篇-....md` |
| /wechat-article（技術/產業/通用主題） | `REPORT/產業研究/` | `REPORT/產業研究/公眾號-{主題}-20260605.md` |
| /news-pulse | `REPORT/{公司名}/新聞追蹤/{公司名}-news-{YYYYMMDD}.md` | `REPORT/台積電/新聞追蹤/台積電-news-20260409.md` |
| /bottleneck-hunter | `REPORT/訊號掃描/bottleneck-map/`（跨標的訊號日誌，非單一個股） | `REPORT/訊號掃描/bottleneck-map/master-map.md` |

## /investment-team 檔案結構

```
REPORT/{公司名}/團隊分析/
├── 01-商業模式分析-段永平視角.md
├── 02-財務估值分析-巴菲特視角.md
├── 03-產業競爭分析-蒙格視角.md
├── 04-風險管理層評估-李錄視角.md
└── 最終報告.md                       — Team Lead 綜合報告
```

## 投研分析核心原則（最高優先順序）

- **客觀、客觀、客觀**——所有投研分析必須基於事實和資料，嚴禁主觀臆斷
- 嚴格區分"事實"與"觀點"：事實用資料支撐，觀點必須明確標註為"觀點"或"推測"
- **不預設立場**：不預設看多或看空，先擺資料、再推邏輯、最後得結論。結論必須從資料中自然推出
- 禁止使用"我認為"、"我覺得"、"顯然"等主觀表述，改用"資料顯示"、"證據表明"、"根據XX來源"
- **呈現正反兩面**：每個核心判斷都必須附帶反面論據（"但另一方面..."），讓讀者自己權衡
- 對不確定的事情誠實說"不確定"或"資料不足"，不要用推測填充確定性
- 所有skill（investment-team、investment-research、earnings-review等）在執行時都必須遵守以上原則，
  行文風格另見下方「去除 AI 寫作痕跡」一節

## 報告語言與風格

- 所有報告與回覆一律使用**繁體中文（台灣正體）**，不得使用簡體字
- 用語採**台灣慣用詞**，注意簡繁用語差異，例如：軟體（非軟件）、硬體、網路（非網絡）、資料/資料庫（非數據/資料庫）、記憶體、程式（非程序）、演算法、最佳化、預設值、人工智慧、影片（非視訊/視頻）、螢幕、專案（非項目）、資訊、品質、聯準會（非美聯儲）、本益比（非市盈率）、每股盈餘（非每股收益）
- 遇到**不確定或易誤解的名詞**（尤其專有名詞、技術詞、金融詞），可直接改用**英文原詞**避免歧義，例如：free cash flow、moat、guidance、EPS、ROE、CAGR、take rate 等
- 風格：直接、犀利、不說廢話
- 資料必須標註來源，關鍵資料至少2個來源交叉驗證
- 估計值必須註明"估計"
- 評分使用★符號（★1-5），不含半星
- 穿插巴菲特/蒙格/段永平/李錄的語錄點評

## 去除 AI 寫作痕跡（避免報告有明顯 AI 味）

規則參考 [Humanizer-zh](https://github.com/op7418/Humanizer-zh) 整理的 24 種 AI 寫作痕跡，所有 skill
輸出的報告、公眾號文章、回覆都必須避免以下模式。**與「投研分析核心原則」的客觀性規範衝突時，
以客觀性規範為準**（例如：不得因為追求「人味」而加入未經資料支撐的主觀臆斷；下方「適度第一人稱」
指的是行文語氣自然，不是允許"我認為/我覺得"式無依據判斷）。

**內容層面：**
- 不誇大意義：避免"標誌著""至關重要的時刻""具有里程碑意義"這類詞彙，除非有具體資料證明影響力
- 不堆砌無內容支撐的媒體引用/知名度描述
- 不用"……ing"式空洞總結句帶過分析（如"象徵著……""反映了……"卻沒有展開論證）
- 不用宣傳性形容詞：迷人的、令人驚嘆的、卓越非凡的
- 不用模糊歸因：禁止"專家認為""市場普遍認為"，必須具名或標明具體來源
- 結尾不要套用制式化「挑戰與展望」段落，改用報告本身的具體結論

**語言與語法層面：**
- 避免高頻 AI 詞彙氾濫：此外、至關重要、深入探討、強調、持久的、增強、培養、賦能、突出、相互作用、
  複雜性、格局、關鍵性的、展示、織錦、寶貴的、充滿活力的、獨特、堅實——這些詞不是禁用，是禁止氾濫堆疊
- 該用"是"就用"是"，不要為了顯得高階而用"充當""代表"等迂迴表達
- 避免"不僅……而且……"式否定排比句連續堆疊
- 不要每個分析都機械式硬湊三點（三段式），論點該幾點就幾點
- 不要為了不重複而刻意換同義詞，同一概念前後用詞盡量一致，精確優先於花俏
- 避免"從 X 到 Y，涵蓋一切"這類虛假範圍式空洞總括
- 破折號、粗體不濫用：粗體只標記真正的重點，不要整段加粗；破折號不是每句都用
- 不要用「行內小標題＋條列」硬湊版面（連續多個「**重點：** xxx」堆疊）
- 標題不用表情符號，不用不自然的逐字大寫

**交流與填充層面：**
- 不寫"希望這份報告對您有幫助"之類的客套/協作語句
- 不諂媚附和使用者既有立場——證據指向哪裡就寫哪裡
- 刪除填充短語："值得注意的是""需要指出的是""為了實現這一目標"，直接講重點
- 不要疊加限定詞軟化判斷（"可能""或許""在某種程度上"疊用），該給明確結論就給明確結論
- 結尾不要用"整體來看，前景樂觀/謹慎樂觀"這類萬用正面收尾，改成具體的下一步觀察重點

**具體寫法：**
- 給觀點和判斷，不只是條列事實
- 句子長短交錯，避免連續三句以上長度雷同
- 承認不確定性與複雜性，不把每件事講成非黑即白
- 行文語氣可以有作者感（自然口吻），但結論仍須有資料佐證，不能變成主觀臆測
- 用具體數字與細節取代模糊概括

**自我檢查（收尾前快速過一遍）：**
連續三句長度是否雷同？段落是否每行都用破折號起頭？"此外""然而"是否可以直接刪掉？
是不是每個列點都湊成三項？結尾是不是套用了萬用正面結論？

## GitHub 操作

- 本地克隆路徑：`~/Workspace/ai-berkshire/`
- 遠端倉庫：`https://github.com/Vik1n9/ai-berkshire.git`
- 推送前先 `git pull --rebase origin main`（遠端經常有新提交）
- commit message 用繁體中文，描述清楚改了什麼
- 不要推送中間過程檔案（如 data_collection.md），只推最終報告

## 常用命令

```bash
# 更新本倉庫（skills / tools 等程式碼變更）
cd ~/Workspace/ai-berkshire
git add skills/xxx.md
git commit -m "更新xxx skill"
git pull --rebase origin main
git push origin main
```

## 注意事項

- 市值必須手算校驗：股價 × 總股本，與報告市值對比
- 貨幣單位要明確（港幣／人民幣／美元），防止混淆
- PE/ROE 等指標用 tools/financial_rigor.py 精確計算
- 報告寫在本倉庫 `REPORT/` 內，且僅限美股與台股公開發行公司；是否推送到 GitHub 由使用者指示，**不主動**推送

<!-- rtk-instructions v2 -->
# RTK (Rust Token Killer) - Token-Optimized Commands

## Golden Rule

**Always prefix commands with `rtk`**. If RTK has a dedicated filter, it uses it. If not, it passes through unchanged. This means RTK is always safe to use.

**Important**: Even in command chains with `&&`, use `rtk`:
```bash
# ❌ Wrong
git add . && git commit -m "msg" && git push

# ✅ Correct
rtk git add . && rtk git commit -m "msg" && rtk git push
```

## RTK Commands by Workflow

### Build & Compile (80-90% savings)
```bash
rtk cargo build         # Cargo build output
rtk cargo check         # Cargo check output
rtk cargo clippy        # Clippy warnings grouped by file (80%)
rtk tsc                 # TypeScript errors grouped by file/code (83%)
rtk lint                # ESLint/Biome violations grouped (84%)
rtk prettier --check    # Files needing format only (70%)
rtk next build          # Next.js build with route metrics (87%)
```

### Test (60-99% savings)
```bash
rtk cargo test          # Cargo test failures only (90%)
rtk go test             # Go test failures only (90%)
rtk jest                # Jest failures only (99.5%)
rtk vitest              # Vitest failures only (99.5%)
rtk playwright test     # Playwright failures only (94%)
rtk pytest              # Python test failures only (90%)
rtk rake test           # Ruby test failures only (90%)
rtk rspec               # RSpec test failures only (60%)
rtk test <cmd>          # Generic test wrapper - failures only
```

### Git (59-80% savings)
```bash
rtk git status          # Compact status
rtk git log             # Compact log (works with all git flags)
rtk git diff            # Compact diff (80%)
rtk git show            # Compact show (80%)
rtk git add             # Ultra-compact confirmations (59%)
rtk git commit          # Ultra-compact confirmations (59%)
rtk git push            # Ultra-compact confirmations
rtk git pull            # Ultra-compact confirmations
rtk git branch          # Compact branch list
rtk git fetch           # Compact fetch
rtk git stash           # Compact stash
rtk git worktree        # Compact worktree
```

Note: Git passthrough works for ALL subcommands, even those not explicitly listed.

### GitHub (26-87% savings)
```bash
rtk gh pr view <num>    # Compact PR view (87%)
rtk gh pr checks        # Compact PR checks (79%)
rtk gh run list         # Compact workflow runs (82%)
rtk gh issue list       # Compact issue list (80%)
rtk gh api              # Compact API responses (26%)
```

### JavaScript/TypeScript Tooling (70-90% savings)
```bash
rtk pnpm list           # Compact dependency tree (70%)
rtk pnpm outdated       # Compact outdated packages (80%)
rtk pnpm install        # Compact install output (90%)
rtk npm run <script>    # Compact npm script output
rtk npx <cmd>           # Compact npx command output
rtk prisma              # Prisma without ASCII art (88%)
rtk uv run <cmd>        # Compact uv project command output
```

### Files & Search (60-75% savings)
```bash
rtk ls <path>           # Tree format, compact (65%)
rtk read <file>         # Code reading with filtering (60%)
rtk grep <pattern>      # Search grouped by file (75%). Format flags (-c, -l, -L, -o, -Z) run raw.
rtk find <pattern>      # Find grouped by directory (70%)
```

### Analysis & Debug (70-90% savings)
```bash
rtk err <cmd>           # Filter errors only from any command
rtk log <file>          # Deduplicated logs with counts
rtk json <file>         # JSON structure without values
rtk deps                # Dependency overview
rtk env                 # Environment variables compact
rtk summary <cmd>       # Smart summary of command output
rtk diff                # Ultra-compact diffs
```

### Infrastructure (85% savings)
```bash
rtk docker ps           # Compact container list
rtk docker images       # Compact image list
rtk docker logs <c>     # Deduplicated logs
rtk kubectl get         # Compact resource list
rtk kubectl logs        # Deduplicated pod logs
```

### Network (65-70% savings)
```bash
rtk curl <url>          # Compact HTTP responses (70%)
rtk wget <url>          # Compact download output (65%)
```

### Meta Commands
```bash
rtk gain                # View token savings statistics
rtk gain --history      # View command history with savings
rtk discover            # Analyze Claude Code sessions for missed RTK usage
rtk proxy <cmd>         # Run command without filtering (for debugging)
rtk init                # Add RTK instructions to CLAUDE.md
rtk init --global       # Add RTK to ~/.claude/CLAUDE.md
```

## Token Savings Overview

| Category | Commands | Typical Savings |
|----------|----------|-----------------|
| Tests | vitest, playwright, cargo test | 90-99% |
| Build | next, tsc, lint, prettier | 70-87% |
| Git | status, log, diff, add, commit | 59-80% |
| GitHub | gh pr, gh run, gh issue | 26-87% |
| Package Managers | pnpm, npm, npx | 70-90% |
| Files | ls, read, grep, find | 60-75% |
| Infrastructure | docker, kubectl | 85% |
| Network | curl, wget | 65-70% |

Overall average: **60-90% token reduction** on common development operations.
<!-- /rtk-instructions -->