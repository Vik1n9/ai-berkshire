# AI Berkshire — 專案指令

## 專案概述

基於 Claude Code 的價值投資研究 Skill 合集。四大師框架：巴菲特、芒格、段永平、李錄。
GitHub: xbtlin/ai-berkshire

## 專案結構

```
skills/          — 投研 Skill 定義（.md），複製到 ~/.claude/commands/ 使用
tools/           — 輔助工具（financial_rigor.py 精確計算、twstock_data.py 台股FinMind取數）
reports/         — 投資研究報告輸出
assets/          — 圖片等靜態資源
```

## 報告目錄結構

所有報告按**公司名**建資料夾，公司相關的所有報告放在對應資料夾內：

```
reports/
├── AI產業研究/              — AI產業鏈全景研究（置頂）
│   ├── AI五層蛋糕-產業全景研究-20260605.md
│   └── AI五層蛋糕-公眾號-20260605.md
├── 騰訊/                    — 騰訊所有研究報告
│   ├── 騰訊-research-20260408.md
│   ├── 騰訊-earnings-2025Q4.md
│   ├── 騰訊-management-20260409.md
│   └── 騰訊-thesis.md
├── 拼多多/                  — 拼多多所有研究報告
├── 泡泡瑪特/                — 泡泡瑪特所有研究報告
├── 核電-industry-20260409.md — 行業報告放根目錄
├── AI算力-funnel-20260509.md  — 漏斗篩選報告放根目錄
├── AI-輪動判斷-20260509.md    — 主題級綜合判斷報告放根目錄
├── portfolio-latest.md       — 組合報告放根目錄
└── 多公司對比-checklist-20260408.md — 多公司報告放根目錄
```

## 報告命名規範

| Skill | 檔案命名格式 | 示例 |
|------|---------|------|
| /investment-team | `{公司名}/` 目錄內含4個視角+最終報告 | `reports/拼多多/最終報告.md` |
| /investment-research | `{公司名}-research-{YYYYMMDD}.md` | `reports/騰訊/騰訊-research-20260408.md` |
| /investment-checklist | `{公司名}-checklist-{YYYYMMDD}.md` | `reports/騰訊/騰訊-checklist-20260408.md` |
| /industry-research | `{行業名}-industry-{YYYYMMDD}.md`（根目錄） | `reports/核電-industry-20260409.md` |
| /industry-funnel | `{行業名}-funnel-{YYYYMMDD}.md`（根目錄） | `reports/AI算力-funnel-20260509.md` |
| /private-company-research | `{公司名}-private-{YYYYMMDD}.md` | `reports/位元組跳動/位元組跳動-private-20260408.md` |
| /earnings-review | `{公司名}-earnings-{期間}.md` | `reports/騰訊/騰訊-earnings-2025Q4.md` |
| /earnings-team | `{公司名}/` 目錄內含4個大師視角+研究底稿+公眾號文章+讀者評審 | `reports/騰訊/騰訊-earnings-2025Q4.md`（公眾號定稿） |
| /thesis-tracker | `{公司名}-thesis.md`（長期維護） | `reports/騰訊/騰訊-thesis.md` |
| /portfolio-review | `portfolio-latest.md`（根目錄，持續更新） | `reports/portfolio-latest.md` |
| /management-deep-dive | `{公司名}-management-{YYYYMMDD}.md` | `reports/騰訊/騰訊-management-20260409.md` |

## /investment-team 檔案結構

```
reports/{公司名}/
├── README.md                         — 研究框架概覽+核心結論
├── 01-商業模式分析-段永平視角.md
├── 02-財務估值分析-巴菲特視角.md
├── 03-行業競爭分析-芒格視角.md
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
- 所有skill（investment-team、investment-research、earnings-review等）在執行時都必須遵守以上原則

## 報告語言與風格

- 所有報告與回覆一律使用**繁體中文（台灣正體）**，不得使用簡體字
- 用語採**台灣慣用詞**，注意簡繁用語差異，例如：軟體（非軟件）、硬體、網路（非網絡）、資料/資料庫（非數據/資料庫）、記憶體、程式（非程序）、演算法、最佳化、預設值、人工智慧、影片（非視訊/視頻）、螢幕、專案（非項目）、資訊、品質、聯準會（非美聯儲）、本益比（非市盈率）、每股盈餘（非每股收益）
- 遇到**不確定或易誤解的名詞**（尤其專有名詞、技術詞、金融詞），可直接改用**英文原詞**避免歧義，例如：free cash flow、moat、guidance、EPS、ROE、CAGR、take rate 等
- 風格：直接、犀利、不說廢話
- 資料必須標註來源，關鍵資料至少2個來源交叉驗證
- 估計值必須註明"估計"
- 評分使用★符號（★1-5），不含半星
- 穿插巴菲特/芒格/段永平/李錄的語錄點評

## GitHub 操作

- 本地克隆路徑：`~/ai-berkshire/`
- 遠端倉庫：`https://github.com/xbtlin/ai-berkshire.git`
- 推送前先 `git pull --rebase origin main`（遠端經常有新提交）
- commit message 用中文，描述清楚改了什麼
- 不要推送中間過程檔案（如 data_collection.md），只推最終報告

## 常用命令

```bash
# 推送報告到GitHub
cd ~/ai-berkshire
git add reports/xxx.md
git commit -m "新增xxx報告"
git pull --rebase origin main
git push origin main
```

## 注意事項

- 市值必須手算校驗：股價 × 總股本，與報告市值對比
- 貨幣單位要明確（港幣/人民幣/美元/新台幣），防止混淆
- PE/ROE等指標用 tools/financial_rigor.py 精確計算
- 台股資料用 tools/twstock_data.py（FinMind）獲取，並按 skills/financial-data.md 台股章節交叉驗證
- 報告寫完後主動詢問是否推送到GitHub
