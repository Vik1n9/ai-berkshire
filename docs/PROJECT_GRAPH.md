# AI Berkshire 專案圖譜（PROJECT GRAPH）

> 自動生成，請勿手工編輯。執行 `python3 scripts/build_graph.py` 重新生成。
> 生成時間：2026-09-27T14:25:24Z

本圖譜為專案的**查詢索引**：把散落在 `reports/`（僅限美股與台股公開發行公司）的報告，
按「公司/主題實體 → 報告」組織，並附 Skill 與工具目錄，便於後續檢索。

機器可讀版本見 [`data/project_graph.json`](../data/project_graph.json)，
命令列查詢用 [`scripts/query_graph.py`](../scripts/query_graph.py)。

## 總覽統計

- 報告總數：**197**
- 實體（公司/主題）數：**49**
- Skill 數：**19**，工具數：**12**
- 報告日期跨度：2026-04-08 ~ 2026-09-26

**按報告型別：**

| 型別 | 數量 |
|------|------|
| 其他 (`other`) | 73 |
| 投研報告 (`research`) | 52 |
| 估值 (`valuation`) | 23 |
| 管理層研究 (`management`) | 11 |
| 團隊研究 (`team`) | 11 |
| 財報精讀 (`earnings`) | 10 |
| 投資論文 (`thesis`) | 7 |
| 檢查清單 (`checklist`) | 6 |
| 對比/輪動 (`comparison`) | 4 |

**按大師視角（檔案命中）：** 巴菲特 42 ／ 李錄 42 ／ 段永平 41 ／ 芒格 13

## Skill 目錄

| Skill | 簡述 |
|-------|------|
| `/bottleneck-hunter` | 供應鏈瓶頸獵手：AI驅動的全球產業鏈瓶頸套利 — 對 $ARGUMENTS 超級趨勢執行供應鏈瓶頸掃描與套利機會挖掘。 |
| `/deep-company-series` | 深度公司系列：8 篇長文拆一家公司 — 為 $ARGUMENTS 撰寫一個 8 篇深度長文系列，釋出在公眾號/影片號等公開渠道。**核心 IP 不是"會寫"，而 |
| `/dyp-ask` | 段永平問答：以他的方式思考 — 你現在扮演段永平（大道至簡/大道行思）本人，回答使用者的任何問題。 |
| `/earnings-review` | 財報精讀：一手資料深度解讀 — 對 $ARGUMENTS 進行財報精讀分析。 |
| `/earnings-team` | 財報精讀團隊：四大師並行解讀 + 公眾號釋出 — 對 $ARGUMENTS 進行團隊化財報精讀分析。四位大師並行解讀財報，編輯潤色成文，讀者評審把關質量，最終產 |
| `/financial-data` | 財務資料獲取與交叉驗證規範 — 本規範適用於所有涉及企業財務資料的研究（深度分析、財報分析、團隊分析、買前確認、投資論點）。 |
| `/industry-funnel` | 行業漏斗篩選：從全市場到 3 家的價值投資精選流程 — 對 $ARGUMENTS 行業/方向執行漏斗式價值投資篩選，從全市場掃描逐層精選到 3 家終選標的。 |
| `/industry-research` | 行業投資研究：產業鏈全景掃描 + 四大師個股分析框架 — 對 $ARGUMENTS 行業進行系統化產業鏈投資研究。 |
| `/investment-checklist` | 巴菲特價值投資買入前 Checklist — 對 $ARGUMENTS 執行巴菲特價值投資買入前 Checklist 分析。 |
| `/investment-research` | 投資研究：巴菲特-蒙格-段永平-李錄 四大師綜合分析框架 — 對 $ARGUMENTS 進行系統化投資研究分析。 |
| `/investment-team` | 投研團隊：四角色並行分析框架 — 對 $ARGUMENTS 進行團隊化投資研究分析。使用 Team 工具建立真正的多Agent並行研究團隊。 |
| `/management-deep-dive` | 管理層縱深研究：買股票就是買人 — 對 $ARGUMENTS 進行管理層深度研究。 |
| `/news-pulse` | 公司新聞脈搏：股價異動快速歸因團隊 — > |
| `/portfolio-review` | 組合管理：從"研究公司"到"管理組合" — 對 $ARGUMENTS 執行投資組合審視與最佳化。 |
| `/private-company-research` | 未上市公司研究：多Agent並行深度研究框架 — 對 $ARGUMENTS 進行團隊化深度研究分析。專為螞蟻集團、小紅書、SpaceX、Stripe 等未上市公 |
| `/quality-screen` | 去劣篩選：7條指標快速排除非一流公司 — 對 $ARGUMENTS 執行去劣指標篩選，快速排除不符合一流公司標準的標的。 |
| `/thesis-drift` | 投資論文漂移檢測：分清事實變化與措辭變化 — 對 $ARGUMENTS 執行投資論文漂移檢測。 |
| `/thesis-tracker` | 投資論文追蹤：買入後的紀律系統 — 對 $ARGUMENTS 執行投資論文追蹤檢查。 |
| `/wechat-article` | 微信公眾號文章：作者-編輯-讀者三Agent協作 — 對 $ARGUMENTS 進行深度研究，產出一篇可直接釋出的微信公眾號文章。三個Agent各司其職：作者寫 |

## 工具目錄（tools/）

| 工具 | 說明 |
|------|------|
| `ashare_data.py` | A股数据工具 — 腾讯行情 + 东方财富搜索/财务，零外部依赖（仅 stdlib）。 |
| `financial_rigor.py` | Financial Rigor Toolkit for AI Berkshire. |
| `log-command.sh` |  |
| `momentum_backtest.py` | 动量发现 + 价值验证 回测工具 |
| `momentum_backtest_v2.py` | 动量发现 + 价值验证 回测工具 v2 |
| `morningstar_fair_value.py` | 从 Morningstar 筛选器 API 抓取所有有公允价值估计的股票， |
| `official_data.py` | 官方来源取数工具：直接从权威来源产生「資料帳本」列，减少手抄与转述误差。 |
| `report_audit.py` | Report Audit Tool for AI Berkshire. |
| `stock_screener.py` | stock_screener.py — 动量发现 + 价值验证 选股筛 |
| `sync_skills.sh` |  |
| `twstock_data.py` | 台股数据工具 — FinMind 开放数据 API，零外部依赖（仅 stdlib）。 |
| `xueqiu_scraper.py` | 雪球通用爬虫：遍历指定用户的完整时间线，按关键词筛选本人原发言。 |

## 實體索引（公司 / 主題 → 報告）

按報告數量降序。點選路徑可直達。

### NVDA `NVDA` — 24 份

- [NVDA-research-20260830](../reports/NVDA/深度分析/NVDA-research-20260830.md) — 2026-08-30 · 投研報告
- [NVDA-topic-20260426-安全墊分析](../reports/NVDA/專題研究/NVDA-topic-20260426-安全墊分析.md) — 2026-04-26
- [NVDA-topic-20260424-CUDA護城河三問精簡版](../reports/NVDA/專題研究/NVDA-topic-20260424-CUDA護城河三問精簡版.md) — 2026-04-24
- [NVDA-topic-20260424-子報告1-訓練vs推理市場分化](../reports/NVDA/專題研究/NVDA-topic-20260424-子報告1-訓練vs推理市場分化.md) — 2026-04-24 · 對比/輪動
- [NVDA-topic-20260424-子報告2-推理護城河](../reports/NVDA/專題研究/NVDA-topic-20260424-子報告2-推理護城河.md) — 2026-04-24
- [NVDA-topic-20260424-子報告3-CUDA護城河本質](../reports/NVDA/專題研究/NVDA-topic-20260424-子報告3-CUDA護城河本質.md) — 2026-04-24
- [NVDA-topic-20260424-子報告4-AI程式設計對CUDA顛覆](../reports/NVDA/專題研究/NVDA-topic-20260424-子報告4-AI程式設計對CUDA顛覆.md) — 2026-04-24
- [NVDA-topic-20260424-推理護城河與CUDA護城河](../reports/NVDA/專題研究/NVDA-topic-20260424-推理護城河與CUDA護城河.md) — 2026-04-24
- [NVDA-valuation-20260420](../reports/NVDA/估值分析/NVDA-valuation-20260420.md) — 2026-04-20 · 估值
- [NVDA-topic-20260419-自研晶片威脅](../reports/NVDA/專題研究/NVDA-topic-20260419-自研晶片威脅.md) — 2026-04-19
- [NVDA-valuation-20260413](../reports/NVDA/估值分析/NVDA-valuation-20260413.md) — 2026-04-13 · 估值
- [NVDA-topic-20260413-反面證據](../reports/NVDA/專題研究/NVDA-topic-20260413-反面證據.md) — 2026-04-13
- [NVDA-research-20260413](../reports/NVDA/深度分析/NVDA-research-20260413.md) — 2026-04-13 · 投研報告
- [NVDA-research-20260408](../reports/NVDA/深度分析/NVDA-research-20260408.md) — 2026-04-08 · 投研報告
- [00-系列說明](../reports/NVDA/公眾號文章/00-系列說明.md)
- [01-開篇-AI時代的賣鏟人](../reports/NVDA/公眾號文章/01-開篇-AI時代的賣鏟人.md)
- [02-商業本質-一座19年建成的軟體城堡](../reports/NVDA/公眾號文章/02-商業本質-一座19年建成的軟體城堡.md)
- [03-訓練與推理-兩個不同的戰場](../reports/NVDA/公眾號文章/03-訓練與推理-兩個不同的戰場.md)
- [04-競爭與威脅-四面楚歌](../reports/NVDA/公眾號文章/04-競爭與威脅-四面楚歌.md)
- [05-風險估值與決策-終章](../reports/NVDA/公眾號文章/05-風險估值與決策-終章.md) — 估值
- [NVDA-reference-段永平雪球發言](../reports/NVDA/參考資料/NVDA-reference-段永平雪球發言.md)
- [最終報告](../reports/NVDA/團隊分析/最終報告.md) — 團隊研究
- [NVDA-thesis](../reports/NVDA/投資論點/NVDA-thesis.md) — 投資論文
- [NVDA-earnings-FY2027Q2](../reports/NVDA/財報分析/NVDA-earnings-FY2027Q2.md) — 財報精讀 · 2027Q2

### UBER `UBER` — 14 份

- [UBER-research-20260901](../reports/UBER/深度分析/UBER-research-20260901.md) — 2026-09-01 · 投研報告
- [UBER-checklist-20260901](../reports/UBER/買前確認/UBER-checklist-20260901.md) — 2026-09-01 · 檢查清單
- [00-系列說明](../reports/UBER/公眾號文章/00-系列說明.md)
- [01-開篇-從虧損之王到盈利機器](../reports/UBER/公眾號文章/01-開篇-從虧損之王到盈利機器.md)
- [02-商業模式-出行加外賣的雙飛輪](../reports/UBER/公眾號文章/02-商業模式-出行加外賣的雙飛輪.md)
- [03-自動駕駛-機遇還是威脅](../reports/UBER/公眾號文章/03-自動駕駛-機遇還是威脅.md)
- [04-風險與估值-終章](../reports/UBER/公眾號文章/04-風險與估值-終章.md) — 估值
- [01-商業模式分析-段永平視角](../reports/UBER/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../reports/UBER/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-產業競爭分析-蒙格視角](../reports/UBER/團隊分析/03-產業競爭分析-蒙格視角.md)
- [04-風險管理層評估-李錄視角](../reports/UBER/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../reports/UBER/團隊分析/最終報告.md) — 團隊研究
- [UBER-thesis](../reports/UBER/投資論點/UBER-thesis.md) — 投資論文
- [UBER-earnings-2026Q2](../reports/UBER/財報分析/UBER-earnings-2026Q2.md) — 財報精讀 · 2026Q2

### MA `MA` — 12 份

- [MA-research-20260901](../reports/MA/深度分析/MA-research-20260901.md) — 2026-09-01 · 投研報告
- [00-系列說明](../reports/MA/公眾號文章/00-系列說明.md)
- [01-開篇-全球支付網路的收費站](../reports/MA/公眾號文章/01-開篇-全球支付網路的收費站.md)
- [02-商業模式-四方模式與五層護城河](../reports/MA/公眾號文章/02-商業模式-四方模式與五層護城河.md)
- [03-增長空間-三條曲線與天花板](../reports/MA/公眾號文章/03-增長空間-三條曲線與天花板.md)
- [04-競爭與風險-雙寡頭的壓力測試](../reports/MA/公眾號文章/04-競爭與風險-雙寡頭的壓力測試.md)
- [05-估值判斷-為確定性付多少溢價（終章）](../reports/MA/公眾號文章/05-估值判斷-為確定性付多少溢價（終章）.md) — 估值
- [01-商業模式分析-段永平視角](../reports/MA/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../reports/MA/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-產業競爭分析-蒙格視角](../reports/MA/團隊分析/03-產業競爭分析-蒙格視角.md)
- [04-風險管理層評估-李錄視角](../reports/MA/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../reports/MA/團隊分析/最終報告.md) — 團隊研究

### LULU `LULU` — 11 份

- [LULU-research-20260516](../reports/LULU/深度分析/LULU-research-20260516.md) — 2026-05-16 · 投研報告
- [00-系列說明](../reports/LULU/公眾號文章/00-系列說明.md)
- [01-開篇-不只是瑜伽褲](../reports/LULU/公眾號文章/01-開篇-不只是瑜伽褲.md)
- [02-品牌護城河的真實深度](../reports/LULU/公眾號文章/02-品牌護城河的真實深度.md)
- [03-增長引擎與中國市場](../reports/LULU/公眾號文章/03-增長引擎與中國市場.md)
- [04-風險管理層與估值判斷](../reports/LULU/公眾號文章/04-風險管理層與估值判斷.md) — 管理層研究
- [01-商業模式分析-段永平視角](../reports/LULU/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../reports/LULU/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-產業競爭分析-蒙格視角](../reports/LULU/團隊分析/03-產業競爭分析-蒙格視角.md)
- [04-風險管理層評估-李錄視角](../reports/LULU/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../reports/LULU/團隊分析/最終報告.md) — 團隊研究

### META `META` — 11 份

- [META-research-20260901](../reports/META/深度分析/META-research-20260901.md) — 2026-09-01 · 投研報告
- [01-開篇-社交廣告帝國的關鍵資料](../reports/META/公眾號文章/01-開篇-社交廣告帝國的關鍵資料.md)
- [02-廣告機器-AI驅動的注意力變現引擎](../reports/META/公眾號文章/02-廣告機器-AI驅動的注意力變現引擎.md)
- [03-AI與元宇宙-1450億美元的豪賭與836億美元的沉沒成本](../reports/META/公眾號文章/03-AI與元宇宙-1450億美元的豪賭與836億美元的沉沒成本.md)
- [04-競爭與監管-護城河的實戰檢驗](../reports/META/公眾號文章/04-競爭與監管-護城河的實戰檢驗.md)
- [05-估值判斷-一道關於信任的數學題](../reports/META/公眾號文章/05-估值判斷-一道關於信任的數學題.md) — 估值
- [01-商業模式分析-段永平視角](../reports/META/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../reports/META/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-產業競爭分析-蒙格視角](../reports/META/團隊分析/03-產業競爭分析-蒙格視角.md)
- [04-風險管理層評估-李錄視角](../reports/META/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../reports/META/團隊分析/最終報告.md) — 團隊研究

### ACN `ACN` — 10 份

- [ACN-research-20260901](../reports/ACN/深度分析/ACN-research-20260901.md) — 2026-09-01 · 投研報告
- [01-開篇-全球最大IT諮詢公司的真面目](../reports/ACN/公眾號文章/01-開篇-全球最大IT諮詢公司的真面目.md)
- [02-商業模式-諮詢加外包的雙輪驅動](../reports/ACN/公眾號文章/02-商業模式-諮詢加外包的雙輪驅動.md)
- [03-競爭與增長-AI時代的護城河攻防戰](../reports/ACN/公眾號文章/03-競爭與增長-AI時代的護城河攻防戰.md)
- [04-風險與估值-14倍PE是恐慌還是理性](../reports/ACN/公眾號文章/04-風險與估值-14倍PE是恐慌還是理性.md) — 估值
- [01-商業模式分析-段永平視角](../reports/ACN/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../reports/ACN/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-產業競爭分析-蒙格視角](../reports/ACN/團隊分析/03-產業競爭分析-蒙格視角.md)
- [04-風險管理層評估-李錄視角](../reports/ACN/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../reports/ACN/團隊分析/最終報告.md) — 團隊研究

### ADBE `ADBE` — 10 份

- [ADBE-research-20260607](../reports/ADBE/深度分析/ADBE-research-20260607.md) — 2026-06-07 · 投研報告
- [01-開篇-創意軟體帝國的關鍵資料](../reports/ADBE/公眾號文章/01-開篇-創意軟體帝國的關鍵資料.md)
- [02-商業模式-訂閱制印鈔機的運轉邏輯](../reports/ADBE/公眾號文章/02-商業模式-訂閱制印鈔機的運轉邏輯.md)
- [03-AI衝擊-Firefly是救星還是掘墓人](../reports/ADBE/公眾號文章/03-AI衝擊-Firefly是救星還是掘墓人.md)
- [04-風險與估值-PE十年最低是機會還是陷阱](../reports/ADBE/公眾號文章/04-風險與估值-PE十年最低是機會還是陷阱.md) — 估值
- [01-商業模式分析-段永平視角](../reports/ADBE/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../reports/ADBE/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-產業競爭分析-蒙格視角](../reports/ADBE/團隊分析/03-產業競爭分析-蒙格視角.md)
- [04-風險管理層評估-李錄視角](../reports/ADBE/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../reports/ADBE/團隊分析/最終報告.md) — 團隊研究

### ADP — 10 份

- [ADP-research-20260901](../reports/ADP/深度分析/ADP-research-20260901.md) — 2026-09-01 · 投研報告
- [01-開篇-全球最大的發薪公司](../reports/ADP/公眾號文章/01-開篇-全球最大的發薪公司.md)
- [02-商業模式-一臺三層收入的複利機器](../reports/ADP/公眾號文章/02-商業模式-一臺三層收入的複利機器.md)
- [03-競爭與增長-薪酬領域的Visa](../reports/ADP/公眾號文章/03-競爭與增長-薪酬領域的Visa.md)
- [04-風險與估值-打了七折的收費公路](../reports/ADP/公眾號文章/04-風險與估值-打了七折的收費公路.md) — 估值
- [01-商業模式分析-段永平視角](../reports/ADP/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../reports/ADP/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-產業競爭分析-蒙格視角](../reports/ADP/團隊分析/03-產業競爭分析-蒙格視角.md)
- [04-風險管理層評估-李錄視角](../reports/ADP/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../reports/ADP/團隊分析/最終報告.md) — 團隊研究

### BKNG `BKNG` — 10 份

- [BKNG-research-20260901](../reports/BKNG/深度分析/BKNG-research-20260901.md) — 2026-09-01 · 投研報告
- [01-開篇-全球最大的旅行撮合機器](../reports/BKNG/公眾號文章/01-開篇-全球最大的旅行撮合機器.md)
- [02-商業模式-一門不擁有酒店的酒店生意](../reports/BKNG/公眾號文章/02-商業模式-一門不擁有酒店的酒店生意.md)
- [03-競爭與增長-一場關於搜尋入口的戰爭](../reports/BKNG/公眾號文章/03-競爭與增長-一場關於搜尋入口的戰爭.md)
- [04-風險與估值-好公司也需要好價格](../reports/BKNG/公眾號文章/04-風險與估值-好公司也需要好價格.md) — 估值
- [01-商業模式分析-段永平視角](../reports/BKNG/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../reports/BKNG/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-產業競爭分析-蒙格視角](../reports/BKNG/團隊分析/03-產業競爭分析-蒙格視角.md)
- [04-風險管理層評估-李錄視角](../reports/BKNG/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../reports/BKNG/團隊分析/最終報告.md) — 團隊研究

### PGR `PGR` — 10 份

- [PGR-research-20260901](../reports/PGR/深度分析/PGR-research-20260901.md) — 2026-09-01 · 投研報告
- [01-開篇-美國車險之王的誕生](../reports/PGR/公眾號文章/01-開篇-美國車險之王的誕生.md)
- [02-商業模式-一家偽裝成保險公司的資料公司](../reports/PGR/公眾號文章/02-商業模式-一家偽裝成保險公司的資料公司.md)
- [03-競爭與增長-從老二到老大之後怎麼辦](../reports/PGR/公眾號文章/03-競爭與增長-從老二到老大之後怎麼辦.md)
- [04-風險與估值-10倍PE到底貴不貴](../reports/PGR/公眾號文章/04-風險與估值-10倍PE到底貴不貴.md) — 估值
- [01-商業模式分析-段永平視角](../reports/PGR/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../reports/PGR/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-產業競爭分析-蒙格視角](../reports/PGR/團隊分析/03-產業競爭分析-蒙格視角.md)
- [04-風險管理層評估-李錄視角](../reports/PGR/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../reports/PGR/團隊分析/最終報告.md) — 團隊研究

### QCOM `QCOM` — 10 份

- [QCOM-research-20260901](../reports/QCOM/深度分析/QCOM-research-20260901.md) — 2026-09-01 · 投研報告
- [01-開篇-移動晶片之王的真面目](../reports/QCOM/公眾號文章/01-開篇-移動晶片之王的真面目.md)
- [02-商業模式-晶片加專利的雙輪印鈔機](../reports/QCOM/公眾號文章/02-商業模式-晶片加專利的雙輪印鈔機.md)
- [03-AI與多元化-後手機時代的三條賽道](../reports/QCOM/公眾號文章/03-AI與多元化-後手機時代的三條賽道.md)
- [04-風險與估值-五重壓力下的價格判斷](../reports/QCOM/公眾號文章/04-風險與估值-五重壓力下的價格判斷.md) — 估值
- [01-商業模式分析-段永平視角](../reports/QCOM/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../reports/QCOM/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-產業競爭分析-蒙格視角](../reports/QCOM/團隊分析/03-產業競爭分析-蒙格視角.md)
- [04-風險管理層評估-李錄視角](../reports/QCOM/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../reports/QCOM/團隊分析/最終報告.md) — 團隊研究

### MRVL `MRVL` — 6 份

- [MRVL-research-20260624](../reports/MRVL/深度分析/MRVL-research-20260624.md) — 2026-06-24 · 投研報告
- [MRVL-research-20260516](../reports/MRVL/深度分析/MRVL-research-20260516.md) — 2026-05-16 · 投研報告
- [01-開篇-定製晶片賽道的關鍵玩家](../reports/MRVL/公眾號文章/01-開篇-定製晶片賽道的關鍵玩家.md)
- [02-商業模式-資料中心管道工的四塊業務](../reports/MRVL/公眾號文章/02-商業模式-資料中心管道工的四塊業務.md)
- [03-AI機遇-定製晶片的黃金時代與博通之戰](../reports/MRVL/公眾號文章/03-AI機遇-定製晶片的黃金時代與博通之戰.md)
- [04-風險與估值-58倍PE在賭什麼](../reports/MRVL/公眾號文章/04-風險與估值-58倍PE在賭什麼.md) — 估值

### MU `MU` — 5 份

- [MU-checklist-20260926](../reports/MU/買前確認/MU-checklist-20260926.md) — 2026-09-26 · 檢查清單
- [MU-research-20260831](../reports/MU/深度分析/MU-research-20260831.md) — 2026-08-31 · 投研報告
- [MU-checklist-20260825](../reports/MU/買前確認/MU-checklist-20260825.md) — 2026-08-25 · 檢查清單
- [MU-thesis](../reports/MU/投資論點/MU-thesis.md) — 投資論文
- [MU-earnings-FY2026Q3](../reports/MU/財報分析/MU-earnings-FY2026Q3.md) — 財報精讀 · 2026Q3

### RDDT `RDDT` — 4 份

- [RDDT-checklist-20260831](../reports/RDDT/買前確認/RDDT-checklist-20260831.md) — 2026-08-31 · 檢查清單
- [RDDT-research-20260830](../reports/RDDT/深度分析/RDDT-research-20260830.md) — 2026-08-30 · 投研報告
- [RDDT-thesis](../reports/RDDT/投資論點/RDDT-thesis.md) — 投資論文
- [RDDT-earnings-2026Q2](../reports/RDDT/財報分析/RDDT-earnings-2026Q2.md) — 財報精讀 · 2026Q2

### 京元電子 `2449/2449.TW` — 4 份

- [京元電子-research-20260926](../reports/京元電子/深度分析/京元電子-research-20260926.md) — 2026-09-26 · 投研報告
- [京元電子-research-20260719](../reports/京元電子/深度分析/京元電子-research-20260719.md) — 2026-07-19 · 投研報告
- [京元電子-thesis](../reports/京元電子/投資論點/京元電子-thesis.md) — 投資論文
- [京元電子-earnings-2026Q2](../reports/京元電子/財報分析/京元電子-earnings-2026Q2.md) — 財報精讀 · 2026Q2

### AVGO `AVGO` — 3 份

- [AVGO-research-20260904](../reports/AVGO/深度分析/AVGO-research-20260904.md) — 2026-09-04 · 投研報告
- [AVGO-thesis](../reports/AVGO/投資論點/AVGO-thesis.md) — 投資論文
- [AVGO-earnings-FY2026Q3](../reports/AVGO/財報分析/AVGO-earnings-FY2026Q3.md) — 財報精讀 · 2026Q3

### MCD `MCD` — 3 份

- [MCD-research-20260923](../reports/MCD/深度分析/MCD-research-20260923.md) — 2026-09-23 · 投研報告
- [MCD-checklist-20260923](../reports/MCD/買前確認/MCD-checklist-20260923.md) — 2026-09-23 · 檢查清單
- [MCD-earnings-2026Q2](../reports/MCD/財報分析/MCD-earnings-2026Q2.md) — 財報精讀 · 2026Q2

### PYPL `PYPL` — 3 份

- [PYPL-topic-20260608-vs螞蟻集團對比分析](../reports/PYPL/專題研究/PYPL-topic-20260608-vs螞蟻集團對比分析.md) — 2026-06-08 · 對比/輪動
- [PYPL-research-20260607](../reports/PYPL/深度分析/PYPL-research-20260607.md) — 2026-06-07 · 投研報告
- [01-開篇-8倍PE的支付巨頭是撿便宜還是接飛刀](../reports/PYPL/公眾號文章/01-開篇-8倍PE的支付巨頭是撿便宜還是接飛刀.md)

### TTWO `TTWO` — 3 份

- [TTWO-research-20260827](../reports/TTWO/深度分析/TTWO-research-20260827.md) — 2026-08-27 · 投研報告
- [TTWO-thesis](../reports/TTWO/投資論點/TTWO-thesis.md) — 投資論文
- [TTWO-earnings-FY2027Q1](../reports/TTWO/財報分析/TTWO-earnings-FY2027Q1.md) — 財報精讀 · 2027Q1

### GFS `GFS` — 2 份

- [GFS-research-20260923](../reports/GFS/深度分析/GFS-research-20260923.md) — 2026-09-23 · 投研報告
- [GFS-earnings-2026Q2](../reports/GFS/財報分析/GFS-earnings-2026Q2.md) — 財報精讀 · 2026Q2

### INTC — 2 份

- [INTC-checklist-20260825](../reports/INTC/買前確認/INTC-checklist-20260825.md) — 2026-08-25 · 檢查清單
- [INTC-research-20260623](../reports/INTC/深度分析/INTC-research-20260623.md) — 2026-06-23 · 投研報告

### NOW `NOW.US` — 2 份

- [NOW-research-20260721](../reports/NOW/深度分析/NOW-research-20260721.md) — 2026-07-21 · 投研報告
- [NOW-earnings-2026Q2](../reports/NOW/財報分析/NOW-earnings-2026Q2.md) — 財報精讀 · 2026Q2

### TSLA `TSLA` — 2 份

- [TSLA-research-20260702](../reports/TSLA/深度分析/TSLA-research-20260702.md) — 2026-07-02 · 投研報告
- [TSLA-research-20260624](../reports/TSLA/深度分析/TSLA-research-20260624.md) — 2026-06-24 · 投研報告

### AMPX — 1 份

- [AMPX-research-20260907](../reports/AMPX/深度分析/AMPX-research-20260907.md) — 2026-09-07 · 投研報告

### CAPR — 1 份

- [CAPR-research-20260907](../reports/CAPR/深度分析/CAPR-research-20260907.md) — 2026-09-07 · 投研報告

### CNTB — 1 份

- [CNTB-research-20260907](../reports/CNTB/深度分析/CNTB-research-20260907.md) — 2026-09-07 · 投研報告

### EOSE — 1 份

- [EOSE-research-20260907](../reports/EOSE/深度分析/EOSE-research-20260907.md) — 2026-09-07 · 投研報告

### GEV `GEV` — 1 份

- [GEV-research-20260623](../reports/GEV/深度分析/GEV-research-20260623.md) — 2026-06-23 · 投研報告

### GOOGL — 1 份

- [GOOGL-research-20260623](../reports/GOOGL/深度分析/GOOGL-research-20260623.md) — 2026-06-23 · 投研報告

### GOSS — 1 份

- [GOSS-research-20260907](../reports/GOSS/深度分析/GOSS-research-20260907.md) — 2026-09-07 · 投研報告

### INO — 1 份

- [INO-research-20260907](../reports/INO/深度分析/INO-research-20260907.md) — 2026-09-07 · 投研報告

### IREN — 1 份

- [IREN-research-20260907](../reports/IREN/深度分析/IREN-research-20260907.md) — 2026-09-07 · 投研報告

### IVA — 1 份

- [IVA-research-20260907](../reports/IVA/深度分析/IVA-research-20260907.md) — 2026-09-07 · 投研報告

### KYTX — 1 份

- [KYTX-research-20260907](../reports/KYTX/深度分析/KYTX-research-20260907.md) — 2026-09-07 · 投研報告

### MSFT `MSFT` — 1 份

- [MSFT-research-20260623](../reports/MSFT/深度分析/MSFT-research-20260623.md) — 2026-06-23 · 投研報告

### OKLO — 1 份

- [OKLO-research-20260907](../reports/OKLO/深度分析/OKLO-research-20260907.md) — 2026-09-07 · 投研報告

### PRQR — 1 份

- [PRQR-research-20260907](../reports/PRQR/深度分析/PRQR-research-20260907.md) — 2026-09-07 · 投研報告

### QBTS — 1 份

- [QBTS-research-20260907](../reports/QBTS/深度分析/QBTS-research-20260907.md) — 2026-09-07 · 投研報告

### RANI — 1 份

- [RANI-research-20260907](../reports/RANI/深度分析/RANI-research-20260907.md) — 2026-09-07 · 投研報告

### RGTI — 1 份

- [RGTI-research-20260907](../reports/RGTI/深度分析/RGTI-research-20260907.md) — 2026-09-07 · 投研報告

### RKLB `RKLB` — 1 份

- [RKLB-research-20260624](../reports/RKLB/深度分析/RKLB-research-20260624.md) — 2026-06-24 · 投研報告

### SILC — 1 份

- [SILC-research-20260907](../reports/SILC/深度分析/SILC-research-20260907.md) — 2026-09-07 · 投研報告

### SLS — 1 份

- [SLS-research-20260907](../reports/SLS/深度分析/SLS-research-20260907.md) — 2026-09-07 · 投研報告

### SMR — 1 份

- [SMR-research-20260907](../reports/SMR/深度分析/SMR-research-20260907.md) — 2026-09-07 · 投研報告

### VSTM — 1 份

- [VSTM-research-20260907](../reports/VSTM/深度分析/VSTM-research-20260907.md) — 2026-09-07 · 對比/輪動

### VSXY — 1 份

- [VSXY-research-20260826](../reports/VSXY/深度分析/VSXY-research-20260826.md) — 2026-08-26 · 對比/輪動

### WULF — 1 份

- [WULF-research-20260907](../reports/WULF/深度分析/WULF-research-20260907.md) — 2026-09-07 · 投研報告

### ZVRA — 1 份

- [ZVRA-research-20260907](../reports/ZVRA/深度分析/ZVRA-research-20260907.md) — 2026-09-07 · 投研報告

### 訊芯-KY `6451.TW` — 1 份

- [訊芯-KY-research-20260831](../reports/訊芯-KY/深度分析/訊芯-KY-research-20260831.md) — 2026-08-31 · 投研報告
