# AI Berkshire 專案圖譜（PROJECT GRAPH）

> 自動生成，請勿手工編輯。執行 `python3 scripts/build_graph.py` 重新生成。
> 生成時間：2026-08-30T19:28:13Z

本圖譜為專案的**查詢索引**：把散落在 `REPORT/`（僅限美股與台股公開發行公司）的報告，
按「公司/主題實體 → 報告」組織，並附 Skill 與工具目錄，便於後續檢索。

機器可讀版本見 [`data/project_graph.json`](../data/project_graph.json)，
命令列查詢用 [`scripts/query_graph.py`](../scripts/query_graph.py)。

## 總覽統計

- 報告總數：**145**
- 實體（公司/主題）數：**25**
- Skill 數：**19**，工具數：**10**
- 報告日期跨度：2026-04-08 ~ 2026-08-30

**按報告型別：**

| 型別 | 數量 |
|------|------|
| 其他 (`other`) | 76 |
| 估值 (`valuation`) | 23 |
| 投研報告 (`research`) | 19 |
| 管理層研究 (`management`) | 11 |
| 團隊研究 (`team`) | 11 |
| 財報精讀 (`earnings`) | 3 |
| 對比/輪動 (`comparison`) | 2 |

**按大師視角（檔案命中）：** 段永平 31 ／ 巴菲特 31 ／ 李錄 30 ／ 芒格 22

## Skill 目錄

| Skill | 簡述 |
|-------|------|
| `/bottleneck-hunter` | 供應鏈瓶頸獵手：AI驅動的全球產業鏈瓶頸套利 — 對 $ARGUMENTS 超級趨勢執行供應鏈瓶頸掃描與套利機會挖掘。 |
| `/deep-company-series` | 深度公司系列：8 篇長文拆一家公司 — 為 $ARGUMENTS 撰寫一個 8 篇深度長文系列，釋出在公眾號/影片號等公開渠道。**核心 IP 不是"會寫"，而 |
| `/dyp-ask` | 段永平問答：以他的方式思考 — 你現在扮演段永平（大道至簡/大道行思）本人，回答使用者的任何問題。 |
| `/earnings-review` | 財報精讀：一手資料深度解讀 — 對 $ARGUMENTS 進行財報精讀分析。 |
| `/earnings-team` | 財報精讀團隊：四大師並行解讀 + 公眾號釋出 — 對 $ARGUMENTS 進行團隊化財報精讀分析。四位大師並行解讀財報，編輯潤色成文，讀者評審把關質量，最終產 |
| `/financial-data` | 財務資料獲取與交叉驗證規範 — 本規範適用於所有涉及企業財務資料的研究。**每個關鍵資料必須來自兩個獨立來源，誤差>1%須標記。** |
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
| `report_audit.py` | Report Audit Tool for AI Berkshire. |
| `stock_screener.py` | stock_screener.py — 动量发现 + 价值验证 选股筛 |
| `twstock_data.py` | 台股数据工具 — FinMind 开放数据 API，零外部依赖（仅 stdlib）。 |
| `xueqiu_scraper.py` | 雪球通用爬虫：遍历指定用户的完整时间线，按关键词筛选本人原发言。 |

## 實體索引（公司 / 主題 → 報告）

按報告數量降序。點選路徑可直達。

### NVIDIA `NVDA` — 23 份

- [20260830-投研報告-NVIDIA-research](../REPORT/NVIDIA/深度分析/20260830-投研報告-NVIDIA-research.md) — 2026-08-30 · 投研報告
- [20260830-財報精讀-NVIDIA-FY2027Q2](../REPORT/NVIDIA/財報分析/20260830-財報精讀-NVIDIA-FY2027Q2.md) — 2026-08-30 · 財報精讀 · 2027Q2
- [20260426-專題-NVIDIA-安全墊分析](../REPORT/NVIDIA/專題研究/20260426-專題-NVIDIA-安全墊分析.md) — 2026-04-26
- [20260424-專題-NVIDIA-CUDA護城河三問精簡版](../REPORT/NVIDIA/專題研究/20260424-專題-NVIDIA-CUDA護城河三問精簡版.md) — 2026-04-24
- [20260424-專題-NVIDIA-子報告1-訓練vs推理市場分化](../REPORT/NVIDIA/專題研究/20260424-專題-NVIDIA-子報告1-訓練vs推理市場分化.md) — 2026-04-24 · 對比/輪動
- [20260424-專題-NVIDIA-子報告2-NVIDIA推理護城河](../REPORT/NVIDIA/專題研究/20260424-專題-NVIDIA-子報告2-NVIDIA推理護城河.md) — 2026-04-24
- [20260424-專題-NVIDIA-子報告3-CUDA護城河本質](../REPORT/NVIDIA/專題研究/20260424-專題-NVIDIA-子報告3-CUDA護城河本質.md) — 2026-04-24
- [20260424-專題-NVIDIA-子報告4-AI程式設計對CUDA顛覆](../REPORT/NVIDIA/專題研究/20260424-專題-NVIDIA-子報告4-AI程式設計對CUDA顛覆.md) — 2026-04-24
- [20260424-專題-NVIDIA-推理護城河與CUDA護城河](../REPORT/NVIDIA/專題研究/20260424-專題-NVIDIA-推理護城河與CUDA護城河.md) — 2026-04-24
- [20260420-估值-NVIDIA-財務估值分析](../REPORT/NVIDIA/估值分析/20260420-估值-NVIDIA-財務估值分析.md) — 2026-04-20 · 估值
- [最終報告-安全邊際-20260420](../REPORT/NVIDIA/團隊分析/最終報告-安全邊際-20260420.md) — 2026-04-20 · 團隊研究
- [20260419-專題-NVIDIA-自研晶片威脅](../REPORT/NVIDIA/專題研究/20260419-專題-NVIDIA-自研晶片威脅.md) — 2026-04-19
- [20260413-估值-NVIDIA-valuation](../REPORT/NVIDIA/估值分析/20260413-估值-NVIDIA-valuation.md) — 2026-04-13 · 估值
- [20260413-專題-NVIDIA-反面證據](../REPORT/NVIDIA/專題研究/20260413-專題-NVIDIA-反面證據.md) — 2026-04-13
- [20260413-投研報告-NVIDIA-research](../REPORT/NVIDIA/深度分析/20260413-投研報告-NVIDIA-research.md) — 2026-04-13 · 投研報告
- [20260408-投研報告-NVIDIA-research](../REPORT/NVIDIA/深度分析/20260408-投研報告-NVIDIA-research.md) — 2026-04-08 · 投研報告
- [00-系列說明](../REPORT/NVIDIA/公眾號文章/00-系列說明.md)
- [01-開篇-AI時代的賣鏟人](../REPORT/NVIDIA/公眾號文章/01-開篇-AI時代的賣鏟人.md)
- [02-商業本質-一座19年建成的軟體城堡](../REPORT/NVIDIA/公眾號文章/02-商業本質-一座19年建成的軟體城堡.md)
- [03-訓練與推理-兩個不同的戰場](../REPORT/NVIDIA/公眾號文章/03-訓練與推理-兩個不同的戰場.md)
- [04-競爭與威脅-四面楚歌](../REPORT/NVIDIA/公眾號文章/04-競爭與威脅-四面楚歌.md)
- [05-風險估值與決策-終章](../REPORT/NVIDIA/公眾號文章/05-風險估值與決策-終章.md) — 估值
- [資料-NVIDIA-段永平雪球發言-NVDA相關](../REPORT/NVIDIA/參考資料/資料-NVIDIA-段永平雪球發言-NVDA相關.md)

### Mastercard `MA` — 11 份

- [00-系列說明](../REPORT/Mastercard/公眾號文章/00-系列說明.md)
- [01-開篇-全球支付網路的收費站](../REPORT/Mastercard/公眾號文章/01-開篇-全球支付網路的收費站.md)
- [02-商業模式-四方模式與五層護城河](../REPORT/Mastercard/公眾號文章/02-商業模式-四方模式與五層護城河.md)
- [03-增長空間-三條曲線與天花板](../REPORT/Mastercard/公眾號文章/03-增長空間-三條曲線與天花板.md)
- [04-競爭與風險-雙寡頭的壓力測試](../REPORT/Mastercard/公眾號文章/04-競爭與風險-雙寡頭的壓力測試.md)
- [05-估值判斷-為確定性付多少溢價（終章）](../REPORT/Mastercard/公眾號文章/05-估值判斷-為確定性付多少溢價（終章）.md) — 估值
- [01-商業模式分析-段永平視角](../REPORT/Mastercard/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../REPORT/Mastercard/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-行業競爭分析-芒格視角](../REPORT/Mastercard/團隊分析/03-行業競爭分析-芒格視角.md)
- [04-風險管理層評估-李錄視角](../REPORT/Mastercard/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../REPORT/Mastercard/團隊分析/最終報告.md) — 團隊研究

### lululemon `LULU` — 11 份

- [20260516-投研報告-lululemon-research](../REPORT/lululemon/深度分析/20260516-投研報告-lululemon-research.md) — 2026-05-16 · 投研報告
- [00-系列說明](../REPORT/lululemon/公眾號文章/00-系列說明.md)
- [01-開篇-不只是瑜伽褲](../REPORT/lululemon/公眾號文章/01-開篇-不只是瑜伽褲.md)
- [02-品牌護城河的真實深度](../REPORT/lululemon/公眾號文章/02-品牌護城河的真實深度.md)
- [03-增長引擎與中國市場](../REPORT/lululemon/公眾號文章/03-增長引擎與中國市場.md)
- [04-風險管理層與估值判斷](../REPORT/lululemon/公眾號文章/04-風險管理層與估值判斷.md) — 管理層研究
- [01-商業模式分析-段永平視角](../REPORT/lululemon/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../REPORT/lululemon/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-行業競爭分析-芒格視角](../REPORT/lululemon/團隊分析/03-行業競爭分析-芒格視角.md)
- [04-風險管理層評估-李錄視角](../REPORT/lululemon/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../REPORT/lululemon/團隊分析/最終報告.md) — 團隊研究

### Adobe `ADBE` — 10 份

- [20260607-投研報告-Adobe-research](../REPORT/Adobe/深度分析/20260607-投研報告-Adobe-research.md) — 2026-06-07 · 投研報告
- [01-開篇-創意軟體帝國的關鍵資料](../REPORT/Adobe/公眾號文章/01-開篇-創意軟體帝國的關鍵資料.md)
- [02-商業模式-訂閱制印鈔機的運轉邏輯](../REPORT/Adobe/公眾號文章/02-商業模式-訂閱制印鈔機的運轉邏輯.md)
- [03-AI衝擊-Firefly是救星還是掘墓人](../REPORT/Adobe/公眾號文章/03-AI衝擊-Firefly是救星還是掘墓人.md)
- [04-風險與估值-PE十年最低是機會還是陷阱](../REPORT/Adobe/公眾號文章/04-風險與估值-PE十年最低是機會還是陷阱.md) — 估值
- [01-商業模式分析-段永平視角](../REPORT/Adobe/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../REPORT/Adobe/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-行業競爭分析-芒格視角](../REPORT/Adobe/團隊分析/03-行業競爭分析-芒格視角.md)
- [04-風險管理層評估-李錄視角](../REPORT/Adobe/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../REPORT/Adobe/團隊分析/最終報告.md) — 團隊研究

### Meta `META` — 10 份

- [01-開篇-社交廣告帝國的關鍵資料](../REPORT/Meta/公眾號文章/01-開篇-社交廣告帝國的關鍵資料.md)
- [02-廣告機器-AI驅動的注意力變現引擎](../REPORT/Meta/公眾號文章/02-廣告機器-AI驅動的注意力變現引擎.md)
- [03-AI與元宇宙-1450億美元的豪賭與836億美元的沉沒成本](../REPORT/Meta/公眾號文章/03-AI與元宇宙-1450億美元的豪賭與836億美元的沉沒成本.md)
- [04-競爭與監管-護城河的實戰檢驗](../REPORT/Meta/公眾號文章/04-競爭與監管-護城河的實戰檢驗.md)
- [05-估值判斷-一道關於信任的數學題](../REPORT/Meta/公眾號文章/05-估值判斷-一道關於信任的數學題.md) — 估值
- [01-商業模式分析-段永平視角](../REPORT/Meta/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../REPORT/Meta/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-行業競爭分析-芒格視角](../REPORT/Meta/團隊分析/03-行業競爭分析-芒格視角.md)
- [04-風險管理層評估-李錄視角](../REPORT/Meta/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../REPORT/Meta/團隊分析/最終報告.md) — 團隊研究

### Uber `UBER` — 10 份

- [00-系列說明](../REPORT/Uber/公眾號文章/00-系列說明.md)
- [01-開篇-從虧損之王到盈利機器](../REPORT/Uber/公眾號文章/01-開篇-從虧損之王到盈利機器.md)
- [02-商業模式-出行加外賣的雙飛輪](../REPORT/Uber/公眾號文章/02-商業模式-出行加外賣的雙飛輪.md)
- [03-自動駕駛-機遇還是威脅](../REPORT/Uber/公眾號文章/03-自動駕駛-機遇還是威脅.md)
- [04-風險與估值-終章](../REPORT/Uber/公眾號文章/04-風險與估值-終章.md) — 估值
- [01-商業模式分析-段永平視角](../REPORT/Uber/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../REPORT/Uber/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-行業競爭分析-芒格視角](../REPORT/Uber/團隊分析/03-行業競爭分析-芒格視角.md)
- [04-風險管理層評估-李錄視角](../REPORT/Uber/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../REPORT/Uber/團隊分析/最終報告.md) — 團隊研究

### ADP — 9 份

- [01-開篇-全球最大的發薪公司](../REPORT/ADP/公眾號文章/01-開篇-全球最大的發薪公司.md)
- [02-商業模式-一臺三層收入的複利機器](../REPORT/ADP/公眾號文章/02-商業模式-一臺三層收入的複利機器.md)
- [03-競爭與增長-薪酬領域的Visa](../REPORT/ADP/公眾號文章/03-競爭與增長-薪酬領域的Visa.md)
- [04-風險與估值-打了七折的收費公路](../REPORT/ADP/公眾號文章/04-風險與估值-打了七折的收費公路.md) — 估值
- [01-商業模式分析-段永平視角](../REPORT/ADP/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../REPORT/ADP/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-行業競爭分析-芒格視角](../REPORT/ADP/團隊分析/03-行業競爭分析-芒格視角.md)
- [04-風險管理層評估-李錄視角](../REPORT/ADP/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../REPORT/ADP/團隊分析/最終報告.md) — 團隊研究

### Accenture `ACN` — 9 份

- [01-開篇-全球最大IT諮詢公司的真面目](../REPORT/Accenture/公眾號文章/01-開篇-全球最大IT諮詢公司的真面目.md)
- [02-商業模式-諮詢加外包的雙輪驅動](../REPORT/Accenture/公眾號文章/02-商業模式-諮詢加外包的雙輪驅動.md)
- [03-競爭與增長-AI時代的護城河攻防戰](../REPORT/Accenture/公眾號文章/03-競爭與增長-AI時代的護城河攻防戰.md)
- [04-風險與估值-14倍PE是恐慌還是理性](../REPORT/Accenture/公眾號文章/04-風險與估值-14倍PE是恐慌還是理性.md) — 估值
- [01-商業模式分析-段永平視角](../REPORT/Accenture/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../REPORT/Accenture/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-行業競爭分析-芒格視角](../REPORT/Accenture/團隊分析/03-行業競爭分析-芒格視角.md)
- [04-風險管理層評估-李錄視角](../REPORT/Accenture/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../REPORT/Accenture/團隊分析/最終報告.md) — 團隊研究

### Booking `BKNG` — 9 份

- [01-開篇-全球最大的旅行撮合機器](../REPORT/Booking/公眾號文章/01-開篇-全球最大的旅行撮合機器.md)
- [02-商業模式-一門不擁有酒店的酒店生意](../REPORT/Booking/公眾號文章/02-商業模式-一門不擁有酒店的酒店生意.md)
- [03-競爭與增長-一場關於搜尋入口的戰爭](../REPORT/Booking/公眾號文章/03-競爭與增長-一場關於搜尋入口的戰爭.md)
- [04-風險與估值-好公司也需要好價格](../REPORT/Booking/公眾號文章/04-風險與估值-好公司也需要好價格.md) — 估值
- [01-商業模式分析-段永平視角](../REPORT/Booking/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../REPORT/Booking/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-行業競爭分析-芒格視角](../REPORT/Booking/團隊分析/03-行業競爭分析-芒格視角.md)
- [04-風險管理層評估-李錄視角](../REPORT/Booking/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../REPORT/Booking/團隊分析/最終報告.md) — 團隊研究

### Progressive `PGR` — 9 份

- [01-開篇-美國車險之王的誕生](../REPORT/Progressive/公眾號文章/01-開篇-美國車險之王的誕生.md)
- [02-商業模式-一家偽裝成保險公司的資料公司](../REPORT/Progressive/公眾號文章/02-商業模式-一家偽裝成保險公司的資料公司.md)
- [03-競爭與增長-從老二到老大之後怎麼辦](../REPORT/Progressive/公眾號文章/03-競爭與增長-從老二到老大之後怎麼辦.md)
- [04-風險與估值-10倍PE到底貴不貴](../REPORT/Progressive/公眾號文章/04-風險與估值-10倍PE到底貴不貴.md) — 估值
- [01-商業模式分析-段永平視角](../REPORT/Progressive/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../REPORT/Progressive/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-行業競爭分析-芒格視角](../REPORT/Progressive/團隊分析/03-行業競爭分析-芒格視角.md)
- [04-風險管理層評估-李錄視角](../REPORT/Progressive/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../REPORT/Progressive/團隊分析/最終報告.md) — 團隊研究

### Qualcomm `QCOM` — 9 份

- [01-開篇-移動晶片之王的真面目](../REPORT/Qualcomm/公眾號文章/01-開篇-移動晶片之王的真面目.md)
- [02-商業模式-晶片加專利的雙輪印鈔機](../REPORT/Qualcomm/公眾號文章/02-商業模式-晶片加專利的雙輪印鈔機.md)
- [03-AI與多元化-後手機時代的三條賽道](../REPORT/Qualcomm/公眾號文章/03-AI與多元化-後手機時代的三條賽道.md)
- [04-風險與估值-五重壓力下的價格判斷](../REPORT/Qualcomm/公眾號文章/04-風險與估值-五重壓力下的價格判斷.md) — 估值
- [01-商業模式分析-段永平視角](../REPORT/Qualcomm/團隊分析/01-商業模式分析-段永平視角.md)
- [02-財務估值分析-巴菲特視角](../REPORT/Qualcomm/團隊分析/02-財務估值分析-巴菲特視角.md) — 估值
- [03-行業競爭分析-芒格視角](../REPORT/Qualcomm/團隊分析/03-行業競爭分析-芒格視角.md)
- [04-風險管理層評估-李錄視角](../REPORT/Qualcomm/團隊分析/04-風險管理層評估-李錄視角.md) — 管理層研究
- [最終報告](../REPORT/Qualcomm/團隊分析/最終報告.md) — 團隊研究

### Marvell `MRVL` — 6 份

- [20260624-投研報告-Marvell-investment-research](../REPORT/Marvell/深度分析/20260624-投研報告-Marvell-investment-research.md) — 2026-06-24 · 投研報告
- [20260516-投研報告-Marvell-research](../REPORT/Marvell/深度分析/20260516-投研報告-Marvell-research.md) — 2026-05-16 · 投研報告
- [01-開篇-定製晶片賽道的關鍵玩家](../REPORT/Marvell/公眾號文章/01-開篇-定製晶片賽道的關鍵玩家.md)
- [02-商業模式-資料中心管道工的四塊業務](../REPORT/Marvell/公眾號文章/02-商業模式-資料中心管道工的四塊業務.md)
- [03-AI機遇-定製晶片的黃金時代與博通之戰](../REPORT/Marvell/公眾號文章/03-AI機遇-定製晶片的黃金時代與博通之戰.md)
- [04-風險與估值-58倍PE在賭什麼](../REPORT/Marvell/公眾號文章/04-風險與估值-58倍PE在賭什麼.md) — 估值

### PayPal `PYPL` — 3 份

- [20260608-專題-PayPal-vs-螞蟻集團-對比分析](../REPORT/PayPal/專題研究/20260608-專題-PayPal-vs-螞蟻集團-對比分析.md) — 2026-06-08 · 對比/輪動
- [20260607-投研報告-PayPal-深度研究報告](../REPORT/PayPal/深度分析/20260607-投研報告-PayPal-深度研究報告.md) — 2026-06-07 · 投研報告
- [01-PayPal-8倍PE的支付巨頭是撿便宜還是接飛刀](../REPORT/PayPal/公眾號文章/01-PayPal-8倍PE的支付巨頭是撿便宜還是接飛刀.md)

### Intel — 2 份

- [20260825-INTC-購買前確認](../REPORT/Intel/買前確認/20260825-INTC-購買前確認.md) — 2026-08-25
- [20260623-投研報告-Intel-investment-research](../REPORT/Intel/深度分析/20260623-投研報告-Intel-investment-research.md) — 2026-06-23 · 投研報告

### Reddit `RDDT` — 2 份

- [Reddit-research-20260830](../REPORT/Reddit/深度分析/Reddit-research-20260830.md) — 2026-08-30 · 投研報告
- [Reddit-earnings-2026Q2](../REPORT/Reddit/財報分析/Reddit-earnings-2026Q2.md) — 財報精讀 · 2026Q2

### ServiceNow `NOW.US` — 2 份

- [20260724-財報精讀-ServiceNow-2026Q2](../REPORT/ServiceNow/財報分析/20260724-財報精讀-ServiceNow-2026Q2.md) — 2026-07-24 · 財報精讀 · 2026Q2
- [20260721-投研報告-ServiceNow-research](../REPORT/ServiceNow/深度分析/20260721-投研報告-ServiceNow-research.md) — 2026-07-21 · 投研報告

### Tesla `TSLA` — 2 份

- [20260702-投研報告-Tesla-特斯拉投資研究報告](../REPORT/Tesla/深度分析/20260702-投研報告-Tesla-特斯拉投資研究報告.md) — 2026-07-02 · 投研報告
- [20260624-投研報告-Tesla-research](../REPORT/Tesla/深度分析/20260624-投研報告-Tesla-research.md) — 2026-06-24 · 投研報告

### GE Vernova `GEV` — 1 份

- [20260623-投研報告-GE Vernova-GEV](../REPORT/GE Vernova/深度分析/20260623-投研報告-GE Vernova-GEV.md) — 2026-06-23

### Google — 1 份

- [20260623-投研報告-Google-Alphabet投資研究報告](../REPORT/Google/深度分析/20260623-投研報告-Google-Alphabet投資研究報告.md) — 2026-06-23 · 投研報告

### Micron — 1 份

- [20260825-MU-購買前確認](../REPORT/Micron/買前確認/20260825-MU-購買前確認.md) — 2026-08-25

### Microsoft `MSFT` — 1 份

- [20260623-投研報告-Microsoft-research](../REPORT/Microsoft/深度分析/20260623-投研報告-Microsoft-research.md) — 2026-06-23 · 投研報告

### RKLB `RKLB` — 1 份

- [投研報告-RKLB-investment-research](../REPORT/RKLB/深度分析/投研報告-RKLB-investment-research.md) — 投研報告

### Take-Two — 1 份

- [Take-Two-research-20260827](../REPORT/Take-Two/深度分析/Take-Two-research-20260827.md) — 2026-08-27 · 投研報告

### Victoria's Secret — 1 份

- [Victoria's Secret-research-20260826](../REPORT/Victoria's Secret/深度分析/Victoria's Secret-research-20260826.md) — 2026-08-26 · 投研報告

### 京元電子 `2449.TW` — 1 份

- [20260719-投研報告-京元電子-research](../REPORT/京元電子/深度分析/20260719-投研報告-京元電子-research.md) — 2026-07-19 · 投研報告
