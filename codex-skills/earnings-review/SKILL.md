---
name: earnings-review
description: "AI Berkshire skill: 財報精讀：一手資料深度解讀. Source: skills/earnings-review.md."
---

## Codex adapter note

This skill is generated from `skills/earnings-review.md` so Claude Code and Codex users share one canonical workflow.

- Treat `$ARGUMENTS` as the user's request in the current Codex thread.
- When the source mentions Claude-only surfaces such as Task, Agent, WebSearch, Bash, Read, or Write, use the closest Codex capability available in this session: subagents when available, web search when needed, shell commands for local tools, and normal file edits for workspace files.
- Use shared project tools from `tools/` in this repository. Prefer running commands from the repository root with paths like `python3 tools/financial_rigor.py ...`; if the current thread starts outside the repo, locate the actual checkout path first instead of assuming a fixed home-directory path.
- Before starting research, run the `date` command to confirm today's date; treat it as the baseline for "latest" data and state the data cutoff date in the report header. Never assume the current date from training data.
- Preserve the research quality rules from `AGENTS.md`: cross-check financial data, use exact arithmetic tools for valuation/math, and clearly label uncertainty and source gaps.

# 財報精讀：一手資料深度解讀

對 $ARGUMENTS 進行財報精讀分析。

**支援輸入格式**：`公司名 季度`，例如：`騰訊 2025Q4`、`PDD 2025年報`、`美團 最新`（預設讀取最近一期）

> "我從不看賣方研報，只讀原始財報。" —— 李錄
>
> "我每天讀500頁。知識就是這樣積累的，像複利一樣。" —— 巴菲特

## 設計理念

大多數AI投研工具依賴二手資訊（新聞、研報摘要、資料網站）。但巴菲特和李錄的核心能力是**讀一手資料**——年報、季報、電話會紀要。

二手資訊的問題：
- 被篩選過——分析師選擇性呈現對其觀點有利的資料
- 有時滯——等別人消化完，alpha已經沒了
- 缺乏語境——"收入增長15%"脫離了管理層對增長質量的討論

本Skill直接解讀一手資料，關注巴菲特和李錄真正會看的內容。

## 執行流程

### 前置步驟：資料可得性評級

| 等級 | 特徵 | 影響 |
|------|------|------|
| A級 | 獲取到完整原文（10-K/年報/電話會紀要） | 正常執行全部步驟 |
| B級 | 僅獲取到部分原文或第三方彙總 | 標註"非原始來源"，降低附註分析權重 |
| C級 | 僅有新聞報道和資料網站摘要 | 聚焦核心財務資料變化，跳過附註挖掘，標註"一手資料不足" |

### 第一步：獲取一手資料

使用 Task 工具啟動多個後台 Agent **並行**獲取以下原始材料：

1. **財報原文**：從公司IR頁面、SEC EDGAR（美股10-K/10-Q）、港交所披露易（港股）、巨潮資訊網（A股）獲取
2. **業績電話會紀要/錄音**：從 Seeking Alpha、公司IR頁面、雪球等獲取
3. **管理層致股東信**（如有年報）：完整閱讀
4. **投資者日/分析師日材料**（如近期有）

如果無法獲取完整原文，按 `skills/financial-data.md` 規範使用標準資料來源拼湊（美股：macrotrends+stockanalysis；港股：aastocks+macrotrends；A股：東方財富+巨潮資訊；台股：FinMind `tools/twstock_data.py`+Goodinfo），但必須標註"非原始財報，來自第三方彙總"，且關鍵資料兩源誤差>1%須標記。

### 第二步：核心財務資料提取與驗證

#### 2.1 收入與利潤表

| 指標 | 本期 | 上期 | YoY變化 | 管理層指引 | 是否達標 |
|------|------|------|---------|-----------|---------|

必須覆蓋：
- 總收入及分業務/分地區收入拆解
- 毛利潤、毛利率變化
- 經營利潤、經營利潤率變化（區分GAAP和Non-GAAP）
- 淨利潤（注意非經常性損益的影響）
- EPS（基本 vs 稀釋）

#### 2.2 現金流表（巴菲特最看重）

| 指標 | 本期 | 上期 | 變化 | 關注點 |
|------|------|------|------|--------|

必須覆蓋：
- 經營性現金流 vs 淨利潤的比率（>100%為佳，<80%需警惕）
- 資本開支及其構成（維護性 vs 擴張性）
- 自由現金流 = 經營現金流 - 資本開支
- 回購金額、分紅金額
- 現金及等價物期末餘額

#### 2.3 資產負債表健康度

必須覆蓋：
- 現金+短期投資 vs 有息負債
- 淨現金/淨負債變化趨勢
- 應收賬款週轉天數變化（是否在放鬆信用條件衝收入？）
- 存貨週轉天數變化（是否在積壓？）
- 商譽及無形資產佔比（是否有減值風險？）

**資料驗證**：使用 `tools/financial_rigor.py` 對關鍵資料進行校驗：

```bash
# 收入和淨利潤交叉驗證（至少2個來源）
python3 tools/financial_rigor.py cross-validate \
  --metric "revenue" --values 108.3e9 107.9e9 --sources "公司財報" "Yahoo Finance"

# 市值校驗
python3 tools/financial_rigor.py verify-market-cap \
  --price 101 --shares 1.488e9 --reported 1.44e11 --currency USD

# 估值指標驗算
python3 tools/financial_rigor.py verify-valuation \
  --price 101 --eps 9.6 --bvps 26.5 --fcf-per-share 10.2
```

### 第三步：管理層討論精讀（MD&A）

這是巴菲特和李錄花最多時間的部分。不是看數字，是**聽管理層怎麼說**。

#### 3.1 管理層語氣分析

逐段閱讀管理層討論/電話會發言，標註以下訊號：

| 訊號型別 | 具體表現 | 示例 |
|---------|---------|------|
| 🟢 **坦誠訊號** | 主動承認問題、給出具體原因 | "本季度利潤率下降主要因為我們在X領域的投入超出預期" |
| 🟢 **清晰訊號** | 戰略表述具體、有量化目標 | "我們計劃在未來12個月將X業務的市場份額從15%提升到20%" |
| 🔴 **模糊訊號** | 大量使用"我們相信"、"長期來看"等沒有實質內容的話 | "我們對未來充滿信心" |
| 🔴 **轉移訊號** | 迴避直接問題、用其他話題帶過 | 被問利潤率時轉談收入增速 |
| 🔴 **歸因外部化** | 把問題全歸咎於宏觀/行業/競爭對手 | "由於宏觀環境影響..." |

#### 3.2 承諾追蹤

從上一期財報/電話會中提取管理層的具體承諾，與本期實際情況對比：

| 上期承諾 | 本期兌現情況 | 評價 |
|---------|------------|------|
| "下半年利潤率將恢復到X%" | 實際Y% | ✅達標 / ❌未達標 / ⚠️部分達標 |

**段永平**："看一個管理層靠不靠譜，最簡單的方法就是看他以前說的話做到了沒有。"

#### 3.3 關鍵問題識別

從電話會Q&A環節提取分析師最尖銳的問題，以及管理層的回答質量：

| 分析師問題 | 管理層回答 | 回答質量(1-5) | 是否迴避 |
|-----------|-----------|:------------:|:-------:|

### 第四步：附註與隱藏資訊挖掘

財報附註裡藏著管理層不想讓你輕易看到的資訊：

#### 4.1 必查附註項

- [ ] **關聯交易**：與大股東/關聯方的交易條款是否公允？
- [ ] **股權激勵**：期權/RSU的稀釋效應有多大？行權價是多少？
- [ ] **或有負債**：訴訟、擔保、承諾等表外風險
- [ ] **會計政策變更**：是否改變了收入確認方式、折舊年限等？
- [ ] **分部資訊**：不同業務的利潤率差異，是否有"好業務補貼壞業務"
- [ ] **客戶/供應商集中度**：前五大客戶/供應商佔比

#### 4.2 異常訊號檢測

- [ ] 應收賬款增速 > 收入增速（可能在塞渠道）
- [ ] 存貨增速 > 收入增速（可能在積壓）
- [ ] 經營現金流 < 淨利潤且差距擴大（利潤質量存疑）
- [ ] 資本化開支突然增加（可能在美化利潤）
- [ ] 非經常性收益佔比突然上升

### 第五步：與歷史資料對比

#### 5.1 趨勢分析

將本期關鍵指標放入至少4個季度（或3年年報）的時間序列中：

| 指標 | Q-4 | Q-3 | Q-2 | Q-1 | 本期 | 趨勢判斷 |
|------|-----|-----|-----|-----|------|---------|

重點關注：
- 利潤率是在改善還是惡化？
- 收入增速是在加速還是減速？
- 現金流質量是在提升還是下降？
- 資本開支強度是在增加還是減少？

#### 5.2 與管理層指引對比

| 指標 | 管理層此前指引 | 實際結果 | 偏差 | 解讀 |
|------|--------------|---------|------|------|

### 第六步：輸出精讀報告

#### 報告結構

```
一、核心資料速覽（一頁表格）
二、本期最重要的3個變化（不超過500字）
三、管理層語氣與承諾追蹤
四、附註中的隱藏資訊
五、關鍵問題（電話會Q&A精選）
六、與投資論文的關係（如有持倉）
七、結論：這份財報改變了什麼？
```

#### 結論必須明確回答

1. **這份財報是超預期、符合預期、還是低於預期？**（不能說"基本符合"然後列一堆兩面話）
2. **對投資論文的影響**：強化 / 無影響 / 削弱 / 破裂
3. **需要關注的下一個催化劑是什麼？**
4. **如果你已持有，該加倉/持有/減倉？**

### 第七步：儲存報告

將報告寫入 `reports/{公司名}-earnings-{期間}.md`，例如 `reports/騰訊-earnings-2025Q4.md`

### 第八步：資料抽檢（準出流程）

報告寫入後，執行資料抽檢，透過方可釋出：

```bash
# Step 1 — 提取抽檢清單
python3 tools/report_audit.py extract \
  --report reports/{公司名}-earnings-{期間}.md

# Step 2 — 對清單每項從可靠信源取數（參見 skills/financial-data.md）

# Step 3 — 輸出準出/打回判決
python3 tools/report_audit.py verdict \
  --results '<填好的JSON>' \
  --report {報告檔名}
```

**【準出】** 全部透過 → 釋出；**【打回】** 有不透過 → 修正後重審。

## 關鍵原則

- **讀原文，不讀摘要**：盡一切可能獲取一手資料
- **看變化，不看絕對值**：趨勢比數字本身重要
- **聽語氣，不只聽內容**：管理層怎麼說和說了什麼一樣重要
- **查附註，不只看正文**：魔鬼藏在細節裡
- **給結論，不做彙總**：精讀的目的是形成判斷，不是複述財報
