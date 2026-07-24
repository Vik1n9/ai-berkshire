---
name: portfolio-review
description: "AI Berkshire skill: 組合管理：從\"研究公司\"到\"管理組合\". Source: skills/portfolio-review.md."
---

## Codex adapter note

This skill is generated from `skills/portfolio-review.md` so Claude Code and Codex users share one canonical workflow.

- Treat `$ARGUMENTS` as the user's request in the current Codex thread.
- When the source mentions Claude-only surfaces such as Task, Agent, WebSearch, Bash, Read, or Write, use the closest Codex capability available in this session: subagents when available, web search when needed, shell commands for local tools, and normal file edits for workspace files.
- Use shared project tools from `tools/` in this repository. Prefer running commands from the repository root with paths like `python3 tools/financial_rigor.py ...`; if the current thread starts outside the repo, locate the actual checkout path first instead of assuming a fixed home-directory path.
- Before starting research, run the `date` command to confirm today's date; treat it as the baseline for "latest" data and state the data cutoff date in the report header. Never assume the current date from training data.
- Preserve the research quality rules from `AGENTS.md`: cross-check financial data, use exact arithmetic tools for valuation/math, and clearly label uncertainty and source gaps.

# 組合管理：從"研究公司"到"管理組合"

對 $ARGUMENTS 執行投資組合審視與最佳化。

**支援輸入格式**：
- 持倉清單，例如：`騰訊30%, 美團20%, 茅台20%, 英偉達15%, 現金15%`
- 或：`騰訊 500股 @480港元, 美團 1000股 @130港元, ...`
- 或：`我的持倉`（如果已有儲存的組合檔案 `reports/portfolio-latest.md`）

> "分散投資是對無知的保護。如果你知道自己在做什麼，分散投資就沒有意義。" —— 巴菲特
>
> "我這輩子見過的真正好的投資機會，十個手指就數得完。" —— 李錄

## 設計理念

研究公司只是投資的一半。另一半是**組合層面的決策**：
- 買多少？（倉位）
- 用什麼錢買？（資金來源——新錢還是換倉）
- 和已有持倉是否衝突？（相關性）
- 最優組合長什麼樣？（機會成本）

巴菲特從不孤立地看一隻股票——他總是在想"這是不是我能做的最好的事？"

## 執行流程

### 第一步：解析持倉

從輸入中解析出當前持倉，標準化為以下格式：

| 標的 | 程式碼 | 持倉量 | 成本價 | 現價 | 市值 | 佔比 | 盈虧 |
|------|------|--------|-------|------|------|------|------|

如果輸入只有比例沒有金額，按比例分析即可。

同時檢查是否存在已有的組合檔案（`reports/portfolio-latest.md`），如有則讀取並更新。

### 第二步：獲取最新資料

使用 Task 工具啟動後台 Agent，透過 WebSearch 為每個持倉並行獲取：
1. 當前股價和估值指標（PE、PB、股息率）
2. 最近一個季度的關鍵財務變化
3. 近期重大事件
4. 分析師一致預期（前瞻PE、目標價）

對每個持倉使用 `tools/financial_rigor.py verify-valuation` 校驗估值資料。對每隻持倉標註資訊豐富度（A/B/C級），C級持倉的分析結論標註低置信度。

### 第三步：單倉位體檢

對每個持倉進行快速健康檢查：

| 標的 | 當前PE | 買入邏輯是否變化 | 論文健康度 | 倉位建議 |
|------|:------:|:--------------:|:---------:|---------|
| 騰訊 | 18x | 未變化 | 8/10 | 合理 |
| 美團 | 25x | 競爭加劇 | 6/10 | 偏高，考慮減倉 |

對每個持倉回答：
- [ ] **如果今天沒有持倉，你還會在當前價格買入嗎？**
- [ ] **如果明天不能交易，持有5年你舒服嗎？**
- [ ] **買入論文還完整嗎？**

**段永平**："如果你不想持有一隻股票10年，那就一天也不要持有。"

### 第四步：組合層面分析

#### 4.1 集中度分析

| 指標 | 當前值 | 建議範圍 | 判斷 |
|------|-------|---------|------|
| 第一大持倉佔比 | | <40% | |
| 前三大持倉佔比 | | 50-80% | |
| 總持倉數量 | | 5-15只 | |
| 現金佔比 | | 10-30%（視市場環境） | |

**李錄的標準**：3-5只核心持倉，前3佔80%+。**但這要求每一隻都研究透徹。**

**巴菲特的標準**：核心持倉不超過10只，但允許更多衛星倉位。

#### 4.2 相關性檢查

識別持倉之間的隱性關聯：

| 持倉A | 持倉B | 相關型別 | 風險 |
|-------|-------|---------|------|
| 騰訊 | 快手 | 同屬中國網際網路 | 監管風險共振 |
| 英偉達 | 台積電 | AI供應鏈上下游 | AI Capex同向波動 |
| 美團 | 拼多多 | 同屬中國消費 | 宏觀消費同向波動 |

**檢查清單**：
- [ ] 是否有超過50%的倉位暴露在同一個主題/行業？
- [ ] 是否有超過50%的倉位暴露在同一個國家/貨幣？
- [ ] 如果中美關係惡化，組合會虧多少？
- [ ] 如果全球經濟衰退，組合會虧多少？

#### 4.3 機會成本分析

這是巴菲特最核心的思維方式——**每一塊錢都應該放在回報最高的地方**。

將所有持倉按"預期年化回報"排序：

| 排名 | 標的 | 當前佔比 | 預期年化回報 | 確定性 | 預期回報×確定性 |
|:----:|------|:-------:|:----------:|:------:|:--------------:|
| 1 | | | | | |
| 2 | | | | | |
| ... | | | | | |

預期回報估算方法（使用 `tools/financial_rigor.py three-scenario` 計算）：
- **簡化公式**：預期年化 ≈ FCF Yield + 預期增速（主要方法）
- **價值型驗證**：安全邊際迴歸 + 利潤增速 + 股息率
- **成長型驗證**：利潤增速 × 合理PE的變化

**關鍵問題**：排名最後的持倉，預期回報是否高於現金（無風險利率~4%）？如果不是，應該賣出換成現金。

#### 4.4 壓力測試

| 情景 | 假設 | 組合預計影響 | 最大回撤 |
|------|------|-----------|---------|
| 全球衰退 | 企業盈利下降20-30% | | |
| 中美衝突升級 | 中概股折價50% | | |
| 利率飆升 | 10年期國債→6% | | |
| 科技泡沫破裂 | 科技股PE壓縮40% | | |

對每個情景做定性+粗估評估（基於各持倉的行業屬性和歷史估值波動範圍）：
- 哪些持倉受衝擊最大？大致影響方向和量級範圍
- 組合整體是否能承受？
- 是否需要對沖？

### 第五步：最佳化建議

#### 5.1 調倉建議

基於以上分析，給出具體的調倉建議：

| 動作 | 標的 | 當前佔比 | 建議佔比 | 理由 |
|------|------|:-------:|:-------:|------|
| 加倉 | | | | |
| 減倉 | | | | |
| 清倉 | | | | |
| 新建倉 | | | | |
| 不動 | | | | |

#### 5.2 尋找替代標的

如果組合中有"不如現金"的倉位，或者現金佔比過高，建議使用 `/industry-research` 或 `/investment-checklist` 對感興趣的行業/公司進行系統篩選，而非在本Skill內直接推薦個股。

#### 5.3 現金管理

| 當前現金佔比 | 建議現金佔比 | 理由 |
|:----------:|:----------:|------|

**巴菲特**：目前持有$3,820億現金，佔比超過總資產的25%——當找不到好機會時，現金是最好的倉位。

### 第六步：輸出組合報告

#### 報告結構

```
一、組合概覽（持倉表格+餅圖描述）
二、單倉位體檢（每個持倉的健康狀態）
三、組合分析
   - 集中度：是否過度分散/集中？
   - 相關性：隱性關聯和風險共振
   - 機會成本：排名最低的倉位是否值得持有？
   - 壓力測試：極端情景下的回撤預估
四、調倉建議（具體操作+理由）
五、下次審視時間和關注重點
```

#### 結論必須明確回答

1. **組合整體健康度**：優秀 / 良好 / 需要調整 / 問題嚴重
2. **最應該做的一件事是什麼？**（加倉X / 減倉Y / 不動）
3. **當前最大風險是什麼？**

### 第七步：儲存組合檔案

將組合資訊寫入 `reports/portfolio-latest.md`，包含：
- 最新持倉表
- 本次審視日期和結論
- 調倉記錄（追加）
- 下次審視提醒

---

## 關鍵原則

- **每一塊錢都有機會成本** — 持有一隻平庸的股票，成本是錯過了一隻優秀的
- **集中不是風險，無知才是** — 持有3只你深度理解的股票，比持有30只你一知半解的安全
- **現金是一種倉位** — 找不到好機會時，持有現金不丟人
- **組合層面 > 個股層面** — 一隻好股票在錯誤的倉位上也會拖累你
- **定期審視，但不要過度交易** — 每季度審視一次足夠，不要每天盯盤調倉
