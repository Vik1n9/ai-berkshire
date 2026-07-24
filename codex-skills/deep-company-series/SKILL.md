---
name: deep-company-series
description: "AI Berkshire skill: 深度公司系列：8 篇長文拆一家公司. Source: skills/deep-company-series.md."
---

## Codex adapter note

This skill is generated from `skills/deep-company-series.md` so Claude Code and Codex users share one canonical workflow.

- Treat `$ARGUMENTS` as the user's request in the current Codex thread.
- When the source mentions Claude-only surfaces such as Task, Agent, WebSearch, Bash, Read, or Write, use the closest Codex capability available in this session: subagents when available, web search when needed, shell commands for local tools, and normal file edits for workspace files.
- Use shared project tools from `tools/` in this repository. Prefer running commands from the repository root with paths like `python3 tools/financial_rigor.py ...`; if the current thread starts outside the repo, locate the actual checkout path first instead of assuming a fixed home-directory path.
- Before starting research, run the `date` command to confirm today's date; treat it as the baseline for "latest" data and state the data cutoff date in the report header. Never assume the current date from training data.
- Preserve the research quality rules from `AGENTS.md`: cross-check financial data, use exact arithmetic tools for valuation/math, and clearly label uncertainty and source gaps.

# 深度公司系列：8 篇長文拆一家公司

為 $ARGUMENTS 撰寫一個 8 篇深度長文系列，釋出在公眾號/影片號等公開渠道。**核心 IP 不是"會寫"，而是"會改"——99% 的財經文章在違反本 skill 的事實核查標準**。

參考樣本：`reports/騰訊/《看懂騰訊》/`

---

## 一、觸發場景

使用者希望為一家公司做"教科書級別"的深度研究，並以**系列長文**形式公開發布。區別於一篇研報：
- 8 篇約 12 萬字，從認知重置到決策框架完整閉環
- 每篇獨立成文（適合單篇分享），但貫穿一套估值/管理層/價格判斷
- 寫給"願意花 90 分鐘讀懂一家公司"的讀者，不是寫給券商客戶

**不適合用本 skill 的場景**：單篇研報、季報點評、行業研究——那些用 `/investment-research`、`/earnings-review`、`/industry-research`。

---

## 二、系列篇目模板（8 篇）

| # | 篇名模板 | 核心問題 | 字數 |
|---|---------|---------|------|
| 01 | 你以為你看懂了 X，其實沒有 | 認知重置：破 3 個常見錯覺 | 4,000-5,000 |
| 02 | X 的護城河——`<生意本質一句話>` | 護城河深不深、未來 5/10 年還在不在 | 6,000-8,000 |
| 03 | X 的最大利潤引擎——`<最賺錢業務>` | 主業是什麼、為什麼能持續 | 6,000-8,000 |
| 04 | X 藏在賬上的另一家公司——`<隱藏資產>` | 投資組合 / 子公司 / 隱藏價值 | 8,000-10,000 |
| 05 | AI（或當下敘事）時代，X 是贏家還是輸家 | 時代變數：分業務拆 AI 影響 | 8,000-10,000 |
| 06 | 用巴菲特方式拆 X 的財報 | 財務深度：毛利率/FCF/ROE/SBC | 8,000-10,000 |
| 07 | `<管理層金句>`——X 的管理層值不值得託付 | 資本配置紀律 + 誠信檢驗 + 接班人 | 8,000-10,000 |
| 08 | 多少錢值得買，什麼訊號必須賣（系列終章） | DCF 三情景 + 紅線清單 + 倉位框架 | 10,000-12,000 |

加一篇 `00-系列說明.md` 作為目錄索引，不發表。

---

## 三、寫作風格規範

### 語氣

- **直接、犀利、不說廢話**——第一句就給數字或反常識結論
- **價值投資框架**——巴菲特/芒格/段永平/李錄視角穿插（但不堆砌名言）
- **不預設立場**——先擺資料、再推邏輯、最後得結論
- **呈現正反兩面**——每個核心判斷都附"但另一方面..."的反方
- **公眾號體感**——前 18-20 字必須能獨立站住（手機預覽）

### 禁用詞

| 禁用 | 原因 | 替代 |
|------|------|------|
| 顯然 / 必然 / 一定 | 主觀絕對化 | 資料顯示 / 證據表明 |
| 我認為 / 我覺得 | 主觀腔調 | 刪除或改為"按本框架" |
| 教科書級別 / 神來之筆 | 流量黨褒獎 | 描述具體事實 |
| 嚴重不匹配 / 嚴重低估 | 強主觀詞 | 給具體折讓百分比 |
| 完美 / 無可挑剔 | 單邊判斷 | 加上反方觀察 |

### 標題風格

- 用**反差數字**或**反共識結論**做鉤子（"15 年 7 次挑戰全失敗"、"年薪 4292 萬僅佔利潤的萬分之 1.65"）
- 副標題中性、概括內容（"——`<本質判斷>`"）
- **避免流量黨比喻**："小巴菲特"、"中國版 X"、"YYDS" 一律避開
- 用專業讀者熟悉的術語（"伯克希爾"而不是"巴菲特"，公司名優於人名）

---

## 四、嚴苛事實核查 Checklist（核心 IP）

### 寫之前就要警惕的"偽精確"陷阱

1. **機率加權期望值**：`30% × A + 50% × B + 20% × C = 期望 +X%` 這種計算幾乎全是垃圾——機率分配是純主觀，給讀者錯誤精確感。**只列情景 + 觸發條件 + 方向，不算加權期望**。
2. **第三方測算 MAU/份額**：QuestMobile/七麥/CBNData 等口徑差異巨大（同一時點能差 2-3 倍）。**只用最可信的兩個對比作 anchor，其他做定性描述**。
3. **歷史增速線性外推**：`2025 年 +33% × 5 年複合 → 2030 年 X` 是金融文盲式預測。**情景假設 + 高/低區間 + 不是承諾**。
4. **未公開的持股比例**：位元組、Halti 類未上市公司持股**從未公開披露**。**給區間，標"不可知"**。
5. **強歸因**：競爭對手失敗 = 因為 X。多重原因都列出來，**本文不做單一歸因**。

### 修訂時必跑的 7 項檢查

```
□ 1. 跨篇數字一致性：總市值、Non-IFRS 淨利潤、關鍵持股 % 全系列對齊
□ 2. 口徑標註：Non-IFRS / GAAP / Non-IFRS-SBC / FCF 各用哪個，全文清楚
□ 3. 重複加計掃描：已並表子公司不在"投資組合"裡、SOTP 不雙算
□ 4. 橫向比較公平性：不能"主業 PE（剔除現金+組合）" vs "對手 PE（不剔）"
□ 5. 機率加權全刪：見上一條
□ 6. 絕對化表述全弱化：grep "顯然|必然|嚴重|教科書|完美"
□ 7. 第三方資料來源標註：每條非財報資料後跟"（來源：X）"
```

### 模型偏好

寫之前**先列出已知硬錯誤風險**：
- 歷史回報倍數：必須用累計投入口徑（如 Riot 33 倍 不是 58 倍）
- 持股比例：必須看最新富途/財報口徑（如騰訊持有美團 1.5% 不是 6.4%）
- "派息分派"會計處理：視同處置收益按 IFRIC 17 在宣派日確認（如京東在 2021，美團在 2022 但金額小）
- 總股本會反彈：SBC 集中年初授予會讓股本短期上升

---

## 五、執行流程

### 階段 1：調研（寫 01-02 篇前完成）

1. 閱讀公司近 5 年年報、最新季報
2. 閱讀至少 3 份獨立賣方研報（找共識 + 反共識）
3. 用 `/investment-team` 或 `/investment-research` 先生成內部研究底稿
4. 與使用者確認 8 篇的核心論點（避免寫完才發現方向不對）

### 階段 2：寫作（按 01→08 順序寫，不跳）

- 每篇寫完先存 `reports/{公司名}/《看懂{公司名}》/0X-XX.md`
- 不立即推 GitHub——等使用者審閱
- 使用者提修訂意見後修改
- 修訂完才 git push

### 階段 3：跨篇一致性掃描（08 篇全部寫完後）

派 Explore agent 並行掃描 8 篇做以下檢查：
1. 同一數字（市值、淨利潤、持股比例）跨篇是否一致
2. 同一術語（FBS、SBC、Non-IFRS）首次出現是否解釋
3. 引用關係：02 篇說"詳見 06 篇"是否真的對應
4. 要點回顧 vs 正文是否數字一致

### 階段 4：釋出前最終核查

```bash
# 推送前必須本地 grep 一次（按 ai-berkshire 隱私規則）
grep -r "<本機使用者名稱>\|/Users/\|<個人身份資訊>" reports/ | head
```

確認無誤後才 `git pull --rebase && git commit && git push`。

---

## 六、修訂意見處理流程

使用者給修訂意見時，按以下順序處理：

### 1. 先核查事實（不要直接改）

如果使用者說"X 資料不對"，先用 Bash/Read 找原始資料交叉驗證：
- 看 ai-berkshire 專案裡同公司的 earnings/財報報告
- 看富途/官方披露
- 給出"使用者說的資料 vs 我查到的資料 vs 我之前用的資料"三方對比

### 2. 判斷修訂級別

| 級別 | 型別 | 處理 |
|------|------|------|
| 🔥 硬錯誤 | 數字錯、歸因錯、口徑錯 | 必改，不需猶豫 |
| ⚠️ 主觀化 | 強主觀詞、絕對化、流量黨比喻 | 弱化或刪除 |
| 🔬 顆粒度 | 來源標註、口徑細化 | 優先順序低，按可讀性平衡 |
| ❓ 不可靠 | 第三方測算差異大 | **刪比改更穩**（使用者明確指示） |

### 3. 修訂後聯動檢查

修一處先想"哪些地方還會引用這個數字/概念"。例：
- 改了總市值 → 全系列聯動改 PE / 主業 PE / 折讓 / FCF Yield
- 改了持股 % → 改 TOP 10 排序 + 歷史持股表 + 減持清單
- 改了術語口徑 → 改首次定義 + 後續引用 + 要點回顧

### 4. 推送後立即報告

```
推送成功（commit hash）。
[N] 處修訂總結 [帶表]：
- 改了什麼
- 聯動改了什麼
- 還有什麼沒改

下一步等指示。
```

---

## 七、本 skill 不做什麼

- **不替讀者做投資決策**——所有篇章末尾"不構成投資建議"
- **不預測股價**——只給"情景 + 觸發條件"
- **不算"期望年化回報"加權值**——主觀機率分配會誤導讀者
- **不寫"X 大佬也持有"** —— 用別人的持倉為自己的判斷背書是反價值投資的
- **不強求 8 篇都寫**——如果某篇沒足夠獨立內容（如某公司管理層不夠特別），合併到其他篇或減篇數

---

## 八、合規與隱私

- 所有公開報告**只用公開資訊**（財報、官方披露、券商研報、知名第三方機構）
- 不用任何**使用者個人資訊**（公司花名、內部 IM、未公開持倉資訊）
- 推送前必須用 grep 掃描 本機使用者名稱 / `/Users/` / 真實姓名 等隱私欄位
- 公開署名按使用者多層身份策略，不混用

---

## 一句話總結

**寫《看懂 X 系列》的核心能力 ≠ 寫得好，而是改得嚴**——
89% 的財經長文死於偽精確數字、主觀加權期望值、絕對化表述。本 skill 的存在就是為了把這些坑全部標記出來，寫之前避開，寫之後掃乾淨。
