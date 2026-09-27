# 財務資料獲取與交叉驗證規範

本規範適用於所有涉及企業財務資料的研究（深度分析、財報分析、團隊分析、買前確認、投資論點）。

**兩條鐵律：**

1. **權威來源優先（必查）**：財務報表數字、股本、公司自行揭露的指標（應收帳款週轉天數、EBITDA、資本支出、自由現金流、產品／應用別佔比等），**一律先查權威來源**：監理機關申報系統（SEC EDGAR、公開資訊觀測站 MOPS、HKEXnews、巨潮資訊）、交易所，或**公司官網投資人關係頁**的原始檔（財報、新聞稿、法說會簡報、營運報告）。第三方網站（macrotrends、stockanalysis、FinMind、Goodinfo、aastocks、東方財富、新聞）只能作為**第二來源交叉驗證**，或在權威來源確實取不到時使用並降級標註。
2. **兩個獨立來源**：每個關鍵資料至少兩個來源，其中**至少一個必須是權威來源**；誤差>1%須標記。**本倉庫內的其他報告不是獨立來源**，不得用來核驗新報告（循環驗證）。

> 以下規範的目的：報告中每一個關鍵數字都能追溯到權威來源的原始值，所有計算都能由工具重算，任何自算指標都能與來源揭露值互相核對。

---

## 來源分層

| 層級 | 定義 | 用途 | 報告標註 |
|------|------|------|---------|
| **第一層：權威來源** | 監理機關申報原文、交易所公告、公司官網 IR 原始檔 | 財報數字、股本、公司揭露指標的**主來源（來源1）** | `[官方]` |
| **第二層：第三方結構化資料** | macrotrends、stockanalysis、FinMind、Goodinfo、aastocks、東方財富 | 交叉驗證（來源2）、歷史時間序列、批次取數 | `[第三方]` |
| **第三層：媒體與分析師** | 新聞、券商報告摘要、共識預估 | 事件、市場預期；**不得作為財報數字來源** | 具名標出處 |
| 推算值 | 由上述資料計算得出 | 必須寫出公式；**權威來源已有揭露的數字，不得用推算值取代** | `（估計）`或`（本報告計算）` |

### 美股

| 層級 | 來源 | 位置 | 取得內容 |
|------|------|------|---------|
| 第一層 | **SEC EDGAR** | sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={ticker} | 10-K、10-Q、8-K（Exhibit 99.1 新聞稿）、20-F／6-K（外國發行人）、DEF 14A、Form 4 |
| 第一層 | **SEC XBRL API** | `https://data.sec.gov/api/xbrl/companyfacts/CIK{10位CIK}.json`（需帶 User-Agent 標頭） | 結構化財報數字，可程式化核對 |
| 第一層 | **公司官網 IR** | investors.{公司}.com | 財報新聞稿、財報簡報、法說會準備稿、公司自行揭露指標 |
| 第二層 | stockanalysis / macrotrends | stockanalysis.com/stocks/{ticker}；macrotrends.net/stocks/charts/{ticker} | 交叉驗證、長期序列、估值倍數 |
| 行情 | 交易所（nasdaq.com / nyse.com）；stockanalysis、Investing.com 為第二層 | | 收盤價、歷史價格 |

### 台股（4 位數代碼）

| 層級 | 來源 | 位置 | 取得內容 |
|------|------|------|---------|
| 第一層 | **公開資訊觀測站（MOPS）** | mops.twse.com.tw | 財務報告書（含附註）、月營收、重大訊息、股東會年報、法說會資訊 |
| 第一層 | **證交所／櫃買中心** | twse.com.tw、tpex.org.tw | 收盤價、本益比、除權息參考價 |
| 第一層 | **公司官網 IR** | 公司官網「投資人關係」頁 | 合併損益表、資產負債表、營運報告（製程別／應用別、週轉天數、現金流、資本支出） |
| 第二層 | FinMind（`tools/twstock_data.py`）、Goodinfo | 見下 | 行情、月營收、時間序列、交叉驗證 |

### 港股

| 層級 | 來源 | 位置 |
|------|------|------|
| 第一層 | **HKEXnews 披露易**、公司官網 IR | hkexnews.hk |
| 第二層 | aastocks、macrotrends（ADR 代碼） | aastocks.com；騰訊 TCEHY、網易 NTES |

### A 股

| 層級 | 來源 | 位置 |
|------|------|------|
| 第一層 | **巨潮資訊**（證監會指定披露網站）、上交所／深交所、公司官網 | cninfo.com.cn；sse.com.cn；szse.cn |
| 第二層 | 東方財富 | eastmoney.com |

### 權威來源取不到時

必須在報告開頭的「資料可得性」說明：**嘗試過哪些權威來源、為何取不到**（例如需登入、檔案未上架、PDF 無法解析），並將該數字標為 `[第三方]`，資料可得性評級不得高於 B 級。不得只寫「來自第三方彙總」帶過。

---

## 數字可信度通則

這些是通則，適用所有公司、所有科目。不要把個案錯誤寫成新的特例規則；新錯誤先判斷違反哪一條通則，再看驗算機制為何沒攔到，補強機制本身。

1. **權威來源優先**：原始數字取自第一層來源；第三方只作交叉驗證，或在權威來源取不到時降級使用並說明。
2. **可追溯**：報告中每個關鍵數字都要能對到資料帳本的一筆紀錄（原始值＋口徑＋期間＋來源位置），或是帳本紀錄經公式算出的結果。帳本以外的數字不得出現在核心表格。
3. **定義一致**：報告標示的口徑、期間，必須與帳本紀錄一致。一個概念若在來源中分散在多個科目，帳本要把構成科目逐筆列出再以公式合計，不得只取其中一行。
4. **工具計算、原始精度**：衍生數字一律寫成帳本公式由工具計算，輸入用來源原始精度（例：仟元、百萬美元），只在報告顯示時四捨五入；不心算、不用已四捨五入的中間值再計算。
5. **揭露值優先、自算值必須勾稽**：來源已揭露的數字直接引用，不得用推算取代。自己算的指標，只要來源也有揭露同一指標（或存在會計恆等式、合計＝分項），就要在帳本列一筆勾稽，自算與揭露不一致時必須查明原因，不得擇一使用。
6. **核驗獨立**：核驗時要回到來源重新取數，不得用本倉庫其他報告或撰稿時的轉述當核驗依據。
7. **不可驗證就不寫成事實**：無法取得出處的引述、數字、說法，刪除或明確標為「未經核實」；估計值標「估計」並在帳本寫出假設。

---

## 資料帳本與驗算流程（深度分析、財報分析、團隊分析必做）

### 資料帳本格式

報告最後加一節 `## 附錄：資料帳本`，放一張表：

```
| ID | 項目 | 口徑 | 期間 | 值 | 單位 | 來源 | 公式 | 容差 |
```

| 列的型態 | 填法 | 用途 |
|---------|------|------|
| 原始值 | 填「值＋來源」，不填公式；值用來源原始精度，來源寫到檔名＋頁碼／科目 | 所有取自來源的數字 |
| 衍生值 | 只填「公式」（例：`=R3/R1*100`），值留空 | 比率、合計、每股數字、估值倍數等，由工具計算 |
| 勾稽列 | 同時填「值＋來源＋公式」 | 來源揭露值 vs 自算值、合計 vs 分項、會計恆等式；工具檢查兩者一致 |
| 假設 | 值＋來源填「假設：理由」 | 預估模型的輸入，讓估計值可重算 |

- 同一「項目＋口徑＋單位」有多個期間時，工具會自動推導跨期間的變化率與差額（年增、季增、pp），不必逐一登記
- 容差留空＝以來源值顯示精度比對；若口徑差異無法避免（例：期末值 vs 平均值），填絕對值或百分比容差，並在「口徑」欄寫明理由

### 用工具從官方來源產生帳本列

手抄是誤差的主要來源，帳本原始值優先用 `tools/official_data.py` 直接從權威來源產生，再貼進附錄：

```bash
# 美股：SEC XBRL（指定一份申報的 accession number；--period-map 把期末日換成報告用的期間標籤）
python3 tools/official_data.py sec --cik <CIK> --accn <accession> \
  --concepts RevenueFromContractWithCustomerExcludingAssessedTax,GrossProfit,NetIncomeLoss \
  --period-map 2026-05-28=FY2026Q3,2025-05-29=FY2025Q3 --prefix S
# 台股：公司官網或公開資訊觀測站下載的 MOPS 格式財報 PDF（--col 指定數字欄位）
python3 tools/official_data.py tw-pdf --file <PDF> --accounts 營業收入合計,營業利益（損失） \
  --col 0 --period 2026Q2 --source "官網合併損益表 115Q2" --prefix I
# 行情：證交所、Nasdaq（--start 另輸出區間最高／最低）
python3 tools/official_data.py twse-price --stock 2449 --date 2026-08-31 --start 2025-09-01
python3 tools/official_data.py nasdaq-price --symbol MU --date 2026-09-25
```

工具輸出的「項目」「口徑」「期間」要依報告用詞調整成一致（同一項目跨期間要用相同名稱，工具才能自動推導變化率）。SEC 若要求聯絡資訊，自行設定環境變數 `SEC_USER_AGENT`，工具本身不含任何個人資料。

### 驗算流程

| 步驟 | 指令 | 通過條件 |
|------|------|---------|
| 1. 帳本驗算 | `python3 tools/report_audit.py ledger --report <檔案> --must-section <核心章節> --all-tables --require-official` | 公式全部可算；勾稽列全部一致；原始值都有權威來源（或標 `[第三方唯一]`／「假設」）且無循環來源；核心章節每個數字都能追溯到帳本，且標示的口徑、期間與帳本一致 |
| 2. 來源重取 | `python3 tools/report_audit.py ledger --report <檔案> --sample 0.2 --seed <日期>` 產生抽樣清單，回到來源重新取數後，`python3 tools/report_audit.py verdict --results '<JSON>' --require-official` | 抽樣的原始值與重新取得的權威來源值，四捨五入到帳本精度後完全一致 |

`--all-tables` 讓全文每張表格的數字都必須追溯到帳本；只有該儲存格明寫「估計」「假設」「推測」「未經官方核實」者除外（這類數字仍須說明來源性質）。「核心章節」是報告集中列出關鍵財務數字的章節（財報分析的「核心資料速覽」、深度分析的「核心財務資料」），以標題文字指定，子標題下的內容一併納入；`--must-section` 可重複指定，凡是用來下判斷的表格（趨勢表、估值表）都應列入。必檢範圍以外無法追溯的數字，工具會列出供複核，撰稿者要補進帳本，或在報告中標明「估計」「未核實」。

任一步驟不通過：修正報告或帳本後，兩個步驟全部重跑。

**判定規則**（`verdict`）：權威來源的值四捨五入到顯示位數後必須完全一致；權威來源不符即不通過，第三方相符也不能抵銷；只有一個來源且不符即不通過；第三方來源之間的差異在 1% 內視為一致。

---

## 台股工具與第二層資料

**FinMind 取數工具**（第二層；輸出自帶市值驗算，適合行情與月營收）：

```bash
python3 tools/twstock_data.py quote 2330        # 最新行情 + PER/PBR/殖利率 + 市值驗算
python3 tools/twstock_data.py valuation 2330    # 估值指標 + PER一年區間 + 52周高低
python3 tools/twstock_data.py financials 2330   # 近5年年度核心財務（營收/毛利率/歸母淨利/EPS/ROE）
python3 tools/twstock_data.py revenue 2330      # 近13個月月營收及同比
python3 tools/twstock_data.py dividend 2330     # 近年股利政策（現金/股票股利、除息日）
python3 tools/twstock_data.py search 台積        # 搜尋股票代碼（注意台股名稱為繁體）
```

台股特別注意：

1. **貨幣單位是新台幣（TWD）**，與港幣/人民幣/美元混排時必須顯式標註，跨市場對比先統一換算
2. **月營收是台股獨有優勢**：上市櫃公司每月10日前強制披露上月營收，是跟蹤基本面拐點最快的公開訊號，earnings-review/thesis-tracker 類分析應優先利用（`revenue` 子命令，並以 MOPS 或公司官網月營收公告核對）
3. FinMind 損益表為**單季值**，工具已自動加總為年度值；不足4季的年份會標註"僅前N季累計"
4. FinMind 的 PER／PBR 在除權配股後可能仍用舊股數 EPS，估值一律用最新股本自行重算
5. FinMind 未註冊可直接用（有小時級限額）。註冊後的 API token **只存本機、嚴禁提交到 git**，工具按優先順序自動讀取：①環境變數 `FINMIND_TOKEN`；②本地檔案 `local/finmind_token.txt`（`local/` 已被 `.gitignore` 永久排除，把 token 單獨一行寫入該檔案即可）。token 不得出現在報告、skill、commit 中
6. 台積電等有 ADR 的公司注意 ADR 與台股原股的匯率/存託比率差異（1 TSM ADR = 5 股 2330）

#### FinMind 取數（第二層：結構化資料與交叉驗證）

FinMind 是 MOPS／TWSE 資料的第三方整理，適合批次取行情、月營收與時間序列，**但財報數字仍須回到 MOPS 或公司官網原始報表核對**（見上方第一層）。網頁搜尋結果的數字不得作為任何一層的來源。

```bash
python3 ~/.codex/skills/finmind-tw-market/scripts/finmind_fetch.py \
  --dataset TaiwanStockPrice --data-id 2330 \
  --start-date 2026-01-01 --end-date 2026-06-30 --format csv --limit 20
```

Token 優先讀環境變數 `FINMIND_TOKEN`，未設定時指令碼自動從技能內建 reference 提取；**嚴禁在任何輸出中列印 token**。`--usage` 可查 API 用量。

常用 dataset 對照：

| 需求 | dataset |
|------|---------|
| 日線行情 | `TaiwanStockPrice`（還原股價用 `TaiwanStockPriceAdj`） |
| 估值 PER/PBR | `TaiwanStockPER` |
| 三大法人買賣超 | `TaiwanStockInstitutionalInvestorsBuySell`（全市場 `TaiwanStockTotalInstitutionalInvestors`） |
| 融資融券 | `TaiwanStockMarginPurchaseShortSale` |
| 財報三表 | `TaiwanStockFinancialStatements` / `TaiwanStockBalanceSheet` / `TaiwanStockCashFlowsStatement` |
| 月營收 | `TaiwanStockMonthRevenue` |
| 股利 | `TaiwanStockDividend` / `TaiwanStockDividendResult` |
| 市值 | `TaiwanStockMarketValue` |
| 個股基本資料 | `TaiwanStockInfo` |
| 個股新聞 | `TaiwanStockNews` |

完整 dataset/欄位/許可權層級參考（大檔案，用 `rg -n "關鍵詞"` 檢索，不要整讀）：
`~/.codex/skills/finmind-tw-market/references/finmind_api_reference_full.md`

**備援**（內含有效 token，均已驗證）：主參考檔案遺失時，依序改用：

1. 本機備份：`~/.codex/skills/finmind-tw-market/references/finmind_api_reference_backup.md`
2. iCloud 副本：`/Users/vikinglu/Library/Mobile Documents/com~apple~CloudDocs/Documents/llms-full.txt`

指令碼可用 `--reference "<路徑>"` 指定；指令碼也遺失時，直接以備援檔案內 Bearer token 呼叫
`GET https://api.finmindtrade.com/api/v4/data?dataset=...&data_id=...&start_date=...`（token 仍不得出現在任何輸出中）。

台股取數注意事項：

- 區分**原始股價**與**還原股價**（除權息），估值與報酬計算用還原價
- 週末/假日無交易紀錄，日期比較以實際交易日為準（`TaiwanStockTradingDate`）
- 部分 dataset 需 FinMind Backer/Sponsor 層級，或當日尚未到更新時間；取不到時明確說明原因，不得用估計值冒充
- 台股財報為 IFRS（合併報表），單位多為新台幣千元，與美股口徑比較時注意換算
- 交叉驗證：MOPS／公司官網為來源1，FinMind／Goodinfo 為來源2，>1% 誤差須標記

---

## 執行規範

### 第一步：獲取資料

對每個財務指標（收入、淨利潤、毛利率、經營現金流、資產負債率等）：

1. **先從第一層權威來源取數**，作為來源1（記下檔案名稱／網址與期間）
2. 再從第二層取數作為來源2
3. 權威來源取不到時，依「權威來源取不到時」一節說明並降級

### 第二步：誤差計算與標記

```
誤差率 = |來源1數值 - 來源2數值| / 來源1數值 × 100%
```

| 誤差 | 處理方式 |
|------|---------|
| ≤ 1% | ✅ 一致，取來源1數值，標註兩個來源 |
| 1% ~ 5% | ⚠️ 標記"資料存在差異"，註明兩個數值，說明可能原因（匯率/會計口徑） |
| > 5% | ❌ 標記"資料存在重大差異"，必須查原始財報核實，不得直接使用 |

### 第三步：資料呈現格式

每個關鍵資料必須按以下格式標註：

```
收入：1,239億元 ✅
  - [官方] 10-K（FY2025，SEC EDGAR）: 1,239億元
  - [第三方] stockanalysis: 1,237億元
  - 誤差: 0.2%
```

差異示例：
```
淨利潤：245億元 ⚠️ 資料存在差異
  - [官方] 8-K Exhibit 99.1: 245億元（GAAP）
  - [第三方] stockanalysis: 278億元（Non-GAAP）
  - 誤差: 13.5% — 原因：會計口徑不同（GAAP vs Non-GAAP）
```

---

## 常見差異原因（不一定是資料錯誤）

| 原因 | 說明 |
|------|------|
| GAAP vs Non-GAAP | 最常見，尤其是利潤類資料 |
| 匯率換算 | 港幣/人民幣/美元換算時間點不同 |
| 財年定義 | 自然年 vs 財年（如蘋果財年10月結束） |
| 合併口徑 | 是否含少數股東權益 |
| 資料更新滯後 | 某平台尚未更新最新一期財報 |

---

## 特別規則

1. **未上市公司**（米哈遊、莉莉絲等）：只有一手資料來源時，資料前標記 `[估計]`，不執行交叉驗證
2. **季度資料 vs 年度資料**：優先使用年度資料做交叉驗證，季度資料部分來源可能有滯後
3. **原始財報為準**：第三方與原始財報（10-K／MOPS 財報／公司官網原始檔）不符時，以原始財報為準，並在報告中標記第三方錯誤
4. **不得循環驗證**：本倉庫 `reports/` 內的既有報告只能作為「對照前期結論」，不能當核驗來源。沿用前期報告的數字時，必須回到權威來源重新核對

---

## 股價與復權（歷史序列必讀）

價格有三種口徑，混用會讓歷史股價位置、長期漲幅、歷史估值分位全部失真：

| 口徑 | 含義 | 用途 |
|------|------|------|
| 不復權 | 實際成交價，除權除息日跳空 | 僅用於"當前時點"快照 |
| 前復權 | 以最新價為基準回撥歷史價 | 歷史股價對比、N年漲幅、歷史PE band 一律用它 |
| 後復權 | 以上市首日為基準前推 | 計算歷史總回報/年化收益 |

規則：

1. 涉及歷史價格的分析統一用**前復權**，且同一分析內**不得混用**復權與不復權來源。
2. 當前市值/當前PE 用**當前實際股價 × 當前總股本**即可，與復權無關——復權隻影響歷史序列。
3. 跨越拆股/大比例送轉的每股指標（歷史EPS、歷史股價），必須復權還原後再同比。
4. 總回報/年化收益需計入分紅（後復權已含），只看價格漲幅會低估。
5. 增發/回購後市值驗算以最新總股本為準（`financial_rigor.py verify-market-cap` 偏差>5% 會提示核對）。

---

## 快速索引

| 場景 | 第一層（來源1） | 第二層（來源2） |
|------|---------|---------|
| 美股（NVDA、MU 等） | SEC EDGAR 10-K／10-Q／8-K、公司 IR | stockanalysis.com／macrotrends.net |
| PDD / 拼多多 | SEC EDGAR 20-F／6-K、公司 IR | stockanalysis.com/stocks/pdd |
| 騰訊 | HKEXnews 年報／業績公告 | aastocks（0700.HK）／macrotrends（TCEHY） |
| 三七互娛 | cninfo.com.cn 定期報告 | eastmoney.com（002555） |
| 台積電 | MOPS 財報、investor.tsmc.com | tools/twstock_data.py（2330）／goodinfo.tw |
