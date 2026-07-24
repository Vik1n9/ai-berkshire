---
name: investment-team
description: "AI Berkshire skill: 投研團隊：四角色並行分析框架. Source: skills/investment-team.md."
---

## Codex adapter note

This skill is generated from `skills/investment-team.md` so Claude Code and Codex users share one canonical workflow.

- Treat `$ARGUMENTS` as the user's request in the current Codex thread.
- When the source mentions Claude-only surfaces such as Task, Agent, WebSearch, Bash, Read, or Write, use the closest Codex capability available in this session: subagents when available, web search when needed, shell commands for local tools, and normal file edits for workspace files.
- Use shared project tools from `tools/` in this repository. Prefer running commands from the repository root with paths like `python3 tools/financial_rigor.py ...`; if the current thread starts outside the repo, locate the actual checkout path first instead of assuming a fixed home-directory path.
- Before starting research, run the `date` command to confirm today's date; treat it as the baseline for "latest" data and state the data cutoff date in the report header. Never assume the current date from training data.
- Preserve the research quality rules from `AGENTS.md`: cross-check financial data, use exact arithmetic tools for valuation/math, and clearly label uncertainty and source gaps.

# 投研團隊：四角色並行分析框架

對 $ARGUMENTS 進行團隊化投資研究分析。使用 Team 工具建立真正的多Agent並行研究團隊。

## 執行流程

### 第一步：展示團隊框架

向使用者展示以下團隊結構，確認後啟動：

| 角色 | 職責 | 分析框架 |
|------|------|----------|
| **team-lead**（你自己） | 統籌協調、彙總研判、輸出最終報告 | 四大師綜合框架 |
| **business-analyst** | 商業模式 & 護城河分析 | 段永平視角 |
| **financial-analyst** | 財務報表 & 估值分析 | 巴菲特視角 |
| **industry-researcher** | 行業格局 & 競爭態勢 | 芒格視角 |
| **risk-assessor** | 風險評估 & 管理層研判 | 李錄視角 |

### 第一步半：AI研究偏見評估

在建立團隊前，先向使用者展示該公司的"AI可研究性"評估：

**資訊豐富度評級**（決定研究策略）：
| 等級 | 特徵 | 研究策略調整 |
|------|------|------------|
| A級（資訊充裕） | 上市多年、券商覆蓋廣 | 團隊重點放在**反面檢驗**和**非共識視角**，避免輸出與市場一致的"正確的廢話" |
| B級（資訊適中） | 上市不久、覆蓋有限 | 每個Agent的推算資料必須標註置信度，team-lead彙總時標註"資料充分度" |
| C級（資訊稀缺） | 冷門/新上市/新興市場 | 團隊轉為"第一性原理模式"：不追求報告完整性，聚焦商業本質的幾個核心問題 |

**關鍵提醒**：資料多≠確定性高，資料少≠確定性低。AI能輸出的置信度 ≠ 投資的真實確定性。確定性來自商業模式本身，不來自資料數量。

將評級結果告知每個Agent，影響其研究方式。

### 第二步：建立團隊

使用 TeamCreate 建立團隊：
- team_name: `{公司名}-research`（英文小寫，如 `meituan-research`）
- agent_type: `team-lead`

### 第三步：建立4個任務

使用 TaskCreate 建立以下4個任務（每個都要有 subject、description、activeForm）：

#### 任務1：商業模式分析
- subject: `分析{公司名}商業模式、護城河與使用者價值`
- description 包含：
  1. 商業模式本質：核心生意定義、收入結構拆解
  2. 平台/產品飛輪效應如何運轉
  3. 護城河分析：品牌/轉換成本/網路效應/規模效應/技術壁壘，逐一驗證
  4. 使用者/客戶價值：為各方創造了什麼獨特價值
  5. 業務矩陣與協同效應
  6. 段永平"好生意"標準評估：差異化、定價權、可持續競爭優勢
  7. 要求搜尋最新財報、行業報告等公開資訊

#### 任務2：財務與估值分析
- subject: `分析{公司名}財務資料、盈利能力與估值`
- description 包含：
  1. 近3-5年營收、淨利潤、經營利潤趨勢
  2. 盈利能力指標：ROE、ROA、毛利率、經營利潤率
  3. 現金流分析：經營性現金流、自由現金流、資本開支
  4. 資產負債表健康度：現金儲備、負債率、流動性
  5. 估值分析：PE/PS/PB/EV等，與歷史及同業對比
  6. 安全邊際評估：內在價值 vs 當前股價
  7. **金融嚴謹性驗證（必須使用Bash呼叫工具，禁止心算）**：
     - 市值驗算：`python3 tools/financial_rigor.py verify-market-cap --price {價格} --shares {股本} --reported {報告市值} --currency {幣種}`
     - 估值驗算：`python3 tools/financial_rigor.py verify-valuation --price {價格} --eps {EPS} --bvps {每股淨資產}`
     - 關鍵資料交叉驗證：`python3 tools/financial_rigor.py cross-validate --field {欄位} --values '{JSON}' --unit {單位}`
     - 三情景估值：`python3 tools/financial_rigor.py three-scenario --price {價格} --eps {EPS} --shares {股本億} --growth {樂觀} {中性} {悲觀} --pe {樂觀PE} {中性PE} {悲觀PE}`
     - 將工具輸出結果直接嵌入報告中作為驗證記錄

#### 任務3：行業與競爭分析
- subject: `分析{行業}行業格局與{公司名}競爭態勢`
- description 包含：
  1. 行業規模與增長：市場規模、增速、滲透率
  2. 競爭格局：主要對手市場份額、競爭策略對比
  3. 核心競爭者威脅評估：逐個分析主要競爭對手
  4. 各細分賽道格局
  5. 行業趨勢：技術變革、政策影響、新進入者
  6. 產業鏈分析：上中下游價值分配
  7. 要求搜尋最新行業資料和競爭動態

#### 任務4：風險與管理層評估
- subject: `評估{公司名}投資風險與管理層質量`
- description 包含：
  1. 管理層評估：CEO能力圈、誠信度、戰略眼光、資本配置能力、歷史決策質量
  2. 監管風險：當前及潛在監管影響
  3. 競爭風險：各競爭對手威脅程度評估
  4. 業務風險：新業務虧損、擴張不確定性
  5. 宏觀風險：經濟週期、行業週期影響
  6. 治理結構：股權結構、關聯交易、股東回報政策
  7. 長期確定性：10年後公司會怎樣？什麼可能顛覆其商業模式？
  8. 要求搜尋最新監管動態、管理層言論等

### 第四步：啟動4個並行Agent

使用 Task 工具同時啟動4個Agent（**必須在同一條訊息中並行呼叫**）：

每個Agent的配置：
- `subagent_type`: `general-purpose`
- `run_in_background`: `true`
- `team_name`: 對應團隊名
- `name`: 對應角色名（business-analyst / financial-analyst / industry-researcher / risk-assessor）

每個Agent的prompt模板：

```
你是{公司名}投研團隊中的"{角色中文名}"，負責從{大師名}投資視角分析{公司名}。

請完成任務 #{任務編號}：{任務subject}

具體要求：
{任務description的內容}

**研究方法**：
- 使用 WebSearch 搜尋最新公開資訊（財報、行業報告、新聞）
- **財務資料必須來自兩個獨立來源**，按 `skills/financial-data.md` 規範執行（美股：macrotrends+stockanalysis；港股：aastocks+macrotrends；A股：東方財富+巨潮資訊；台股：FinMind `tools/twstock_data.py`+Goodinfo），兩源誤差>1%須標記
- 確保資料準確，關鍵資料標註來源
- 分析要深入，不流於表面

**輸出要求**：
- 報告要詳盡，使用Markdown表格呈現關鍵資料
- 每個分析維度要有明確結論和評分
- 報告末尾要有該維度的總體結論

**完成後**：
1. 使用 TaskUpdate 將任務 #{任務編號} 標記為 completed
2. 透過 SendMessage 把完整分析報告傳送給 team-lead（type: "message", recipient: "team-lead"）
```

### 第五步：接收報告並跟蹤進度

- 向使用者實時展示進度表（哪些Agent已完成、哪些仍在研究中）
- 每收到一份報告，更新進度並展示該報告的核心要點（3-5條）
- 等待全部4份報告到齊

### 第六步：關閉團隊成員

全部報告收到後，向4個Agent傳送 shutdown_request（使用 SendMessage，type: "shutdown_request"）。

### 第七步：彙總最終報告

綜合4份分析報告，輸出以下結構的最終報告：

---

#### 1. 一句話結論
> 用一段話（50-100字）概括是否值得投資及核心邏輯

#### 2. 四維評分總表
| 維度 | 框架 | 評分(1-5星) | 核心判斷 |
|------|------|------------|----------|

綜合評分：X / 5

#### 3. 核心資料速覽
關鍵財務和經營指標表格（近2年對比）

#### 4. 各維度分析摘要
每個維度摘取3-5條最重要的發現

#### 5. 投資論點（Bull vs Bear）
- 🟢 看多邏輯（5-7條）
- 🔴 看空邏輯（5-7條）

#### 6. 巴菲特買入前Checklist
| # | 檢查項 | 透過? | 說明 |
10個核心檢查項，逐一評估

#### 7. 最終投資建議
- 定性判斷表（生意質量/管理層/估值/時機）
- 分層操作建議表（激進型/穩健型/保守型 → 建議+價格區間）
- 關鍵催化劑（加倉訊號/減倉訊號各3-5條）

#### 8. 總結段落
100-200字的最終總結

---

### 第八步：儲存報告

將完整最終報告寫入 `~/{公司名}投資研究報告_{日期}.md`（日期格式 YYYYMMDD）。

### 第九步：資料抽檢（準出流程）

```bash
# Step 1 — 提取抽檢清單（15%隨機抽樣）
python3 tools/report_audit.py extract \
  --report <報告檔案路徑>

# Step 2 — 對清單每項從可靠信源取數（參見 skills/financial-data.md）

# Step 3 — 輸出準出/打回判決
python3 tools/report_audit.py verdict \
  --results '<填好的JSON>' \
  --report <報告檔名>
```

**【準出】** 全部透過 → 報告可釋出；**【打回】** 有不透過 → 修正後重審。

### 第十步：清理團隊

使用 TeamDelete 清理團隊資源。

## 重要注意事項

1. **4個Agent必須並行啟動**——在同一條訊息中呼叫4次Task工具
2. **Agent透過SendMessage彙報**——不是檔案協作，是訊息通訊
3. **資料準確性**——要求Agent使用WebSearch搜尋最新資料，關鍵資料交叉驗證
4. **結論要明確**——不迴避給出買入/觀望/迴避建議和具體價格區間
5. **所有分析必須有資料支撐**——附資料來源
6. **耐心等待**——4個Agent研究需要幾分鐘，實時向使用者更新進度
7. **反偏見意識**——team-lead在彙總時必須評估：各Agent的分析是否受限於資料充裕度？是否與市場共識過度趨同？最終報告需包含"資訊豐富度評級"和"AI研究侷限性宣告"
8. **資訊稀缺時的誠實原則**——寧可在報告中留白標註"資料不足"，也不要用推測填滿框架偽裝確定性
