# Anthropic, PBC：S-1 招股書審查與價值分析

> **資料截止日**：2026-10-27（S-1 於 2026-10-26 公開遞交，尚未生效）
> **主要來源**：SEC EDGAR Form S-1，accession 0001628280-26-067168，CIK 2130357（[原文](https://www.sec.gov/Archives/edgar/data/0002130357/000162828026067168/anthropicpbc-sx1.htm)）。年度數字（2023–2025）經審計；2025、2026 上半年與季度數字未經審計。
> **交叉驗證**：營收 $163億、淨損 $807億 等主要數字另與 Yahoo Finance 報導（2026-10-26）及 Anthropic 官網公告（anthropic.com/news/s1-sec）比對一致；所有表格數字回對附錄資料帳本。
> **為何放在 PRIVATE/**：本倉庫 reports/ 只收已上市公司。Anthropic 尚未掛牌（擬於 Nasdaq Global Select 上市，代號 ANT），先依未上市公司框架存放；掛牌後改於 `reports/ANT/` 建正式報告。
> **定價資訊**：發行股數、價格區間、承銷費用、發行後股數在 S-1 原文均為空白。本報告的估值以最近一輪私募價格推算，不是 IPO 價格。
> 本報告為學習與研究用途，不構成投資建議。

---

## 一、一句話結論

Anthropic 是一門正在由「燒錢研究所」轉成「高毛利軟體」的生意：2026 年第二季單季營收 $115.6億、營業利益 $9.7億，首次轉正；但它在 2026 年 6 月底後又簽下約 $2,450億 的最低算力付款義務，2027 年起的算力成本會跳一個量級。以 Series H 私募價推算的股權價值約 $9,976億（估計），等於 Q2 年化營收的 21.6 倍（估計）。這個價格已經假設它能在三年內把營收放大到現在的三倍並維持軟體級利潤率，安全邊際接近零。結論：觀望，等 IPO 定價與 2026 年第三、四季算力成本數字出來再評估。

---

## 二、核心財務資料

### 2.1 損益表（單位：百萬美元）

| 項目 | 2023 | 2024 | 2025 | H1 2025 | H1 2026 |
|---|---|---|---|---|---|
| 營收 | 41 | 386 | 4,585 | 1,163 | 16,286 |
| Compute and infrastructure | 433 | 2,522 | 7,326 | 2,334 | 8,945 |
| Personnel | 95 | 454 | 1,839 | 538 | 3,152 |
| Sales, marketing, and partnerships | 2 | 43 | 568 | 120 | 3,168 |
| 營業損益 | (551) | (2,980) | (8,060) | (2,135) | (693) |
| 可轉換票據等公允價值變動 | (1,045) | (5,434) | (34,308) | (10,942) | (72,388) |
| 淨損 | (1,531) | (8,309) | (41,965) | (12,969) | (80,748) |
| Adjusted Operating Income (Loss) | (522) | (2,788) | (4,854) | (1,849) | 1,618 |

2025 年另有 Bartz 版權和解費用 1,500 百萬美元計入營業費用（帳本 X1），這是 2025 年營業虧損擴大的一次性因素。

### 2.2 季度營收與營業損益（單位：百萬美元，未經審計）

| 項目 | Q1 2025 | Q2 2025 | Q3 2025 | Q4 2025 | Q1 2026 | Q2 2026 |
|---|---|---|---|---|---|---|
| 營收 | 376 | 787 | 1,382 | 2,040 | 4,731 | 11,555 |
| Compute and infrastructure | 944 | 1,390 | 2,047 | 2,945 | 3,387 | 5,558 |
| 營業損益 | (935) | (1,200) | (3,089) | (2,836) | (1,667) | 974 |

### 2.3 關鍵比率（自算，公式見帳本）

| 指標 | 2025 | H1 2025 | H1 2026 |
|---|---|---|---|
| 營收成長（年增） | 1,087.8% | — | 1,300.3% |
| Compute and infrastructure 占營收 | 159.8% | 200.7% | 54.9% |
| 以 Cost of revenue 計算的毛利率（自算，S-1 未揭露毛利率） | 39.5% | — | 85.4% |
| Adjusted Operating Margin | — | — | 9.9% |

| 指標 | Q2 2026 |
|---|---|
| 營收年增（S-1 揭露 1,368%） | 1,368.2% |
| Compute and infrastructure 年增（S-1 揭露 300%） | 299.9% |
| 營收季增 | 144.2% |
| 營業利益率 | 8.4% |

### 2.4 資產負債與現金流（單位：百萬美元）

| 項目 | 2026-06-30 |
|---|---|
| 現金及約當現金 | 112,389 |
| 短期投資 | 19,262 |
| 現金加短期投資 | 131,651 |
| 應收帳款 | 5,833 |
| 遞延收入 | 1,650 |
| 可轉換票據（公允價值） | 108,566 |
| Redeemable convertible preferred stock | 157,510 |
| 總資產 | 147,358 |
| 累計虧損 | (132,902) |

| 項目 | 2025 | H1 2026 |
|---|---|---|
| 營業活動現金流 | (2,637) | 3,929 |
| 購置不動產及設備 | 131 | 482 |
| Free cash flow（營業現金流減購置設備，自算） | (2,768) | 3,447 |
| 股份基礎薪酬（現金流量表） | 1,158 | 2,185 |

---

## 三、公司畫像速覽

| 項目 | 內容 | 置信度 |
|---|---|---|
| 公司名稱 | Anthropic, PBC（Delaware 公益公司） | 高（招股書） |
| 總部 | 舊金山 | 高（招股書） |
| 創辦人 | Dario Amodei（CEO）、Daniela Amodei（President、董事長）等七位共同創辦人 | 高（招股書） |
| CFO | Krishna Rao（2024 年 4 月起） | 高（招股書） |
| 核心業務 | Claude 模型家族（Mythos 與 Fable、Opus、Sonnet、Haiku），透過 API、Claude Code、Claude Cowork、Claude.ai 訂閱銷售 | 高（招股書） |
| 員工 | 約 5,300 人 | 高（招股書） |
| 主要投資方 | Amazon、Google（持無投票權 Class N，各超過 5%）、Spark Capital 等 | 高（招股書） |
| 累計募資 | $1,411億 | 高（招股書） |
| 承銷商代表 | Goldman Sachs、Morgan Stanley | 高（招股書） |
| 擬上市代號 | ANT（Nasdaq Global Select） | 高（招股書） |

---

## 四、六維評分總表

| 維度 | 評分 | 核心判斷 | 置信度 |
|---|---|---|---|
| 商業模式與客戶 | ★★★★★ | 用量計費為主，大客戶滲透才剛開始，NRR 約 900% | 高 |
| 財務與估值 | ★★ | 營運已接近損益兩平，但私募價已反映多年高成長，算力承諾龐大 | 中 |
| 產業與競爭 | ★★★ | 前沿模型三強之一，對手 OpenAI、Google 資本同樣雄厚，領先期以月計 | 中 |
| 風險與治理 | ★★ | Class A 股東實質無控制權；美國國防部供應鏈風險認定仍在訴訟 | 高 |
| 技術與智慧財產 | ★★★★ | 研究團隊與模型能力領先有收入佐證；專利數量少，護城河靠速度不靠法律 | 中 |
| 替代資料訊號 | ★★★★ | 財星五百大企業過半已是大客戶，前五大客戶占比下降 | 中 |

綜合評分：★★★（生意★★★★★，價格與治理把分數拉下來）

---

## 五、商業模式：這門生意到底賣什麼

用段永平的方式講給外行人聽：Anthropic 賣的是「按件計酬的白領工時」。企業把寫程式、讀合約、做研究這些工作交給 Claude，按處理的 token 量付錢。2026 年上半年營收中，用量計費 13,064 百萬美元、訂閱 3,222 百萬美元（帳本 R11、R12），用量計費占八成。

收入結構有三個特點：

1. **客戶自己會長大。** Net Revenue Retention 約 900%（2026-09-30，帳本 K4）：同一批客戶一年後花的錢是原來的九倍。這個數字太高，不能外推。它反映的是 AI 導入初期的爆發，S-1 自己也寫成長率會下降，而且可能「decline significantly」。
2. **大客戶才剛開始用。** 年營收 $10 萬以上的客戶超過 11,900 家，$100 萬以上超過 1,900 家，$1,000 萬以上約 250 家（帳本 K1–K3）。S-1 揭露 Fortune 500 中超過一半已是 $10 萬級客戶，但 Anthropic 營收平均只占這些客戶總支出不到 0.1%。滲透空間很大，但這同樣代表客戶的轉換成本還很低。
3. **雲端市集是主要通路，也是主要風險。** 2026 年上半年約 48% 營收經由 AWS、GCP、Azure 市集收取（帳本 K6）。這些雲端商同時是投資人、算力供應商、競爭對手。

模型降價也是成長引擎。S-1 寫 Opus 4.5 降價後，季增率由 2025 年第四季的 48% 加速到 2026 年第一季的 132%；Opus 5.5 讓每項任務成本比 Opus 5 降約 40%。降價換用量，用量換營收，前提是算力效率持續提升，否則會變成以價換量的價格戰。

**反面論據**：S-1 估計 2026 年前九個月有約 5%–7% 營收來自違反使用政策或商業條款的客戶（帳本 K8），這部分在偵測到後會被停權、不會再出現。營收品質不是百分之百。

> 段永平說「買股票就是買公司」。這家公司賣的東西是真需求：客戶的錢從試用預算移到了正式工作流程，Claude Code 的大量使用者是工程師自己付錢。但「對的生意」還有後半句：要能持續賺錢。這要看下一節的算力帳。

---

## 六、財務深度審查

### 6.1 淨損 $807億 的真相

2026 年上半年淨損 80,748 百萬美元，其中 72,388 百萬美元（約 89.6%，帳本 F2）是可轉換票據、衍生負債與 SAFE 的公允價值變動。這筆是非現金損失：Anthropic 的估值愈漲，Amazon 手上那批可轉換票據的公允價值就愈高，公司帳上就要認列愈大的損失。另有 8,757 百萬美元 的其他費用，主要來自 note purchase agreements 的初始認列與公允價值變動。

可以這樣驗證：可轉換票據公允價值 108,566 百萬美元 ÷ 可轉股數 1,840,444,962 股 ＝ 每股約 $58.99（帳本 V2），與 Series H 每股 $589.0095 按 10:1 轉換比換算的 $58.90 幾乎一致（帳本 V3）。會計師基本是用最近一輪私募價來評這批票據。IPO 完成後票據轉股，這類損失就會消失。

**反面論據**：非現金不等於無成本。$1,132億 的累計公允價值損失（S-1 揭露），代表 Amazon 在 2023–2024 年以每股約 $2.09 和 $5.05 換到大量股權，這是早期股東被稀釋的真實代價。

### 6.2 營運面：Q2 2026 首度營業獲利

2026 年第二季營業利益 974 百萬美元，營業利益率 8.4%。轉正的直接原因是營收（季增 144.2%）跑得比算力成本（季增約 64%）快。S-1 用「營收年增 1,368% vs 算力成本年增 300%」來證明它的算力效率，帳本重算兩者都對得上。

以 Cost of revenue 自算的毛利率，從 2025 年的 39.5% 升到 2026 年上半年的 85.4%。這個數字要小心解讀：S-1 只把「服務客戶的算力」算進 Cost of revenue，訓練模型的算力放在 R&D（2026 年上半年 R&D 9,741 百萬美元，帳本 C3）。對前沿模型公司來說，訓練算力不是可省的研發費用，是不付就會被淘汰的維持性支出。巴菲特算 owner earnings 時會扣掉維持競爭力所需的資本支出，同樣的邏輯，訓練算力應該當成本看。把全部算力都扣掉的口徑是 Adjusted Operating Margin 9.9%（這個數字加回了 SBC），比 85% 更接近這門生意現在的真實獲利能力。

### 6.3 算力承諾：最大的一筆帳

這是整份 S-1 裡最重要的數字，也是最容易被營收成長蓋掉的數字。

| 承諾項目 | 金額（十億美元） | 性質 |
|---|---|---|
| 截至 6 月底的固定或最低付款承諾 | 265.6 | 不可取消為主 |
| 6 月底後新增最低付款義務 | 245 | 期後簽約 |
| 6 月底後短期合約最低付款 | 21 | 短期合約 |
| 以上三項合計 | 531.6 | 自算 |
| Google 等 TPU 額外算力（未定案，不在承諾表內，估計） | 125–150 | 條款未定案 |
| AMD Helios 機櫃（無固定金額，若全數採購，估計） | 20 以上 | 無固定金額 |

個別合約中，Broadcom 設備租賃 161.2、Google 114.5、SpaceXAI 120.5、Amazon 110.0、Microsoft 44.9、Nscale 44.6、Lambda 41.3（單位：十億美元，帳本 M4–M10）。其中 SpaceXAI 合約在全部容量交付後每月約 $31億，換算年化 $372億（帳本 M12），而 2026 年第二季整體 Compute and infrastructure 年化只有 $222億（帳本 M13）。

三項最低承諾合計 $5,316億（自算），是 2026 年上半年營收的 32.6 倍、Q2 年化營收的 11.5 倍（帳本 M14、M15）。這些錢分攤在 2026–2045 年，不是一次付清，但大部分不可取消。

蒙格的逆向思考在這裡最有用：Anthropic 怎樣會死？不是因為模型做得不好，而是因為簽了 $5,000億 以上的算力，結果 AI 需求成長在 2028 年放緩、價格戰壓低單價。到那時，固定成本會吃掉利潤，而且合約大多不能取消。

**反面論據**：帳上有 $1,317億 現金與短期投資（帳本 B3），加上 $150億 循環信用額度、Google 與 Amazon 未動用的票據額度，以及 IPO 募資，短中期流動性不是問題。算力也不全是成本：S-1 把算力描述為可在訓練、推論、內部使用之間調度的「單一池」，需求如果持續，這些合約會是對手拿不到的產能。

### 6.4 股份基礎薪酬的延遲炸彈

截至 2026-06-30，RSU 因「上市」這個績效條件尚未達成，帳上沒有認列費用。S-1 揭露：若以 6 月 30 日上市計，當天要一次認列 $29億 累計費用，之後還有 $237億 未認列費用在約 2.1 年內攤提；另有 $31億 其他股權獎酬未認列。6 月後董事會再核准約 9,100 萬股 RSU，公允價值 $58億。

$237億 ÷ 2.1 年，等於每年約 $113億（估計）的 SBC，對照 2026 年上半年 Adjusted Operating Income 只有 $16.2億。上市後的 GAAP 營業損益會因 SBC 明顯轉差；看 Adjusted 數字的投資人要記得，這是真的發給員工的股票。

---

## 七、產業與競爭

S-1 點名的直接競爭者只有 OpenAI 與 Google，另提到開放權重模型與國家行為者。

Anthropic 的差異化在三個地方，證據強弱不同：

- **企業與程式碼場景**：證據最強。Claude Code 帶動開發者採用，Claude Cowork 的採用速度在同期比較中快於 Claude Code。大客戶數在九個月內從約 1,500 家（2025 年底）增加到 11,900 家以上（2026-09-30）。
- **多晶片算力**：同時使用 AWS Trainium、Google TPU、NVIDIA GPU、AMD GPU，議價力比單一供應商強。但反過來說，它沒有自己的晶片，也沒有自己的雲，關鍵供應商（Amazon、Google）同時是股東與競爭者。
- **安全品牌**：S-1 認為安全與可預測性是企業選型的決定因素。這一點與美國國防部爭議互相拉扯：同一個「不做自主武器與大規模監控」的立場，替它贏得企業信任，也讓它被國防部列為供應鏈風險。

> 蒙格：「Show me the incentive and I will show you the outcome.」Amazon 與 Google 的誘因是同時賣算力給 Anthropic、持有它的股權、又推自己的模型。只要 Anthropic 繼續成長，三種身分的利益一致；一旦它們自己的模型追上，誘因就會分歧。

**模型領先的持續性**：前沿模型的領先期通常以月計，S-1 裡模型代際（Opus 4.5、5、5.5；Mythos 5、5.1；Fable 5、5.1）在不到一年內推出。這是速度型護城河：必須一直跑，停下來就沒有。

---

## 八、治理：Class A 股東買到的是什麼

這是一個分給你經濟利益、但不分給你控制權的結構：

- **Class F（1 股）**：由七位共同創辦人組成的 Founder LLC 持有，固定享有全部投票權的 50.1%（帳本 G1），用於選舉非 Class T 董事及一般股東表決事項。
- **Class T（1 股）**：由 Long-Term Benefit Trust（LTBT）持有，選出 7 席董事中的 4 席（目前為 Reed Hastings、Vas Narasimhan、Christopher Liddell 及 1 席空缺）。LTBT 目前 4 名 trustees，包括前聯準會主席 Ben Bernanke，另有 1 席空缺。
- **Class N**：Amazon、Google 等策略股東持有，無投票權，轉讓給非關係人時轉成 Class A。
- **Class A**：一般投資人，合計投票權最多 49.9%，而且只能選非 Class T 董事。

結果是 LTBT 加 Founder LLC 可以選出全部董事，Nasdaq 認定為 controlled company。公司是 PBC，董事依法要在股東財務利益、受影響者利益與「為人類長期利益負責任地發展先進 AI」三者間平衡，股東利益不是唯一優先。

另外兩項會稀釋 Class A 股東的機制：公司已把 846,840,960 股 Class N（完全稀釋股數的 5%，帳本 V4）投入 Anthropic Public Benefit Fund；之後股價每比前一個里程碑漲 50%，董事會可再發最多 2%。創辦人各自承諾把 80% 個人股權捐給慈善用途。

**反面論據**：這套結構的目的寫得很清楚，也在 S-1 裡完整揭露。對相信長期使命的投資人，創辦人控制可以避免短期壓力；Meta、Google 上市時也有超級投票權，股東照樣賺到錢。差別在於 Anthropic 的董事義務明文不以股東報酬為唯一目標，這一點沒有前例可循。

> 李錄常講投資要待在能力圈內。這套治理結構超出一般投資人評估公司治理的能力圈：LTBT 的實際行為、Class F 的落日條件、公益股份何時發行，都沒有歷史可以參考。

---

## 九、風險矩陣

| 風險 | 機率 | 影響 | 監控指標 |
|---|---|---|---|
| 算力承諾固定成本過高、需求放緩時侵蝕利潤 | 中 | 高 | 每季 Compute and infrastructure 占營收比 |
| 美國政府供應鏈風險認定擴大到國防承包商生態 | 中 | 中 | D.C. Circuit 後續程序、最高法院動向 |
| 前沿模型競爭導致降價、領先消失 | 中 | 高 | 每次模型發布後的季增率 |
| 雲端市集通路與供應商利益衝突 | 低 | 高 | CSP 營收占比、合約續約條件 |
| 版權訴訟（Concord Music、Reddit、加拿大四案等） | 高 | 中 | 判決與和解金額 |
| 上市後 SBC 與稀釋 | 高 | 中 | GAAP 營業損益、完全稀釋股數 |
| 違規使用營收被清除 | 高 | 低 | S-1 揭露的違規營收比例變化 |

美國國防部事件時間線（S-1 揭露，S-1 用語為 Department of War）：2026 年初國防部表示可能動用 Defense Production Act，要求移除模型在自主武器與大規模監控上的使用限制；2026-02-27 總統指示聯邦機構停用，國防部將其列為「supply-chain risk to national security」。北加州聯邦地院 2026-08-27 大致判 Anthropic 勝訴（認定違反第一修正案與第五修正案正當程序），但 D.C. Circuit 以 2-1 駁回其審查聲請，認為國防部依 FASCSA Section 4713 作出的風險認定合法。政府營收約占各期營收 1%（帳本 K9），直接損失小；真正的風險在國防承包商、供應商是否被迫避開 Anthropic。

---

## 十、估值判斷

以下全部是估計，假設寫在帳本。S-1 沒有價格區間，以下以 Series H 私募價為錨。

| 估值方法 | 結果 | 說明 |
|---|---|---|
| Series H 隱含股權價值（估計） | 約 $9,976億 | 每股 $58.90 × 完全稀釋約 169.4 億股 |
| Q2 年化營收倍數（估計） | 約 21.6 倍 | $9,976億 ÷ $462億 |
| 終局倒推：若本益比 25 倍、淨利率 30%，所需營收（估計） | 約 $1,330億 | 約為 Q2 年化營收的 2.9 倍 |

完全稀釋股數是從「846,840,960 股＝完全稀釋股數 5%」反推（假設 Amazon 票據全數轉換，2026-06-30 口徑），未計入 6 月後新發股份，實際數字以 IPO 定價時揭露為準。

怎麼讀這個倒推：Q2 單季年增 1,368%、季增 144%，營收在兩年內到 $1,330億 並不離譜。問題在後半段。30% 淨利率要在扣掉訓練算力、上市後每年約 $113億（估計）的 SBC，以及 $5,316億 承諾分年攤提之後達成。目前 Adjusted Operating Margin 只有 9.9%，而且 2026 年 12 月 SpaceXAI 容量到齊後，算力成本會再跳一階。

> 巴菲特：「Price is what you pay; value is what you get.」這門生意的 value 可能很高，但在私募價這個 price 上，買方已經預付了未來三年最好的情境。

**真實價值區間（估計）**：

| 情境 | 股權價值 | 假設 |
|---|---|---|
| 保守 | 約 $4,000億（估計） | 營收成長 2027 年起大幅放緩、算力承諾壓縮利潤；約為 Q2 年化營收的 8–9 倍（推測） |
| 合理 | 約 $8,000億–$1兆（估計） | 接近私募價，成長延續到 2028 年 |
| 樂觀 | $2兆 以上（估計） | Virtual Collaborator 普及，營收達數千億美元且維持軟體級利潤率 |

保守與樂觀之間差 5 倍以上，這本身就說明不確定性有多大。以 Series H 價格買入，相對保守情境沒有安全邊際。

---

## 十一、投資論點：看多 vs 看空

看多：

1. 營收成長有真實需求支撐：Q2 2026 營收 $115.6億，季增 144.2%，年營收 $10 萬以上客戶數在九個月內變成原來的近 8 倍（S-1）。
2. 營運已經轉正：Q2 2026 營業利益 $9.7億，2026 年上半年營業現金流 $39.3億（S-1）。
3. 客戶集中度下降：前五大客戶以外的營收占比，從 2026 年第一季約 64% 升到第三季約 79%（S-1）。
4. 資金充足：帳上現金加短期投資 $1,317億，並有多個未動用額度（S-1）。
5. 研究速度本身是加速器：S-1 揭露公司內部大量研究與程式碼由 Claude 完成，形成「用模型做下一代模型」的循環。

看空：

1. 算力最低承諾合計約 $5,316億（自算），多數不可取消，需求一旦放緩就是固定成本壓力。
2. NRR 約 900% 是導入初期現象，S-1 自己寫成長率會下降。
3. 上市後 SBC 每年約 $113億（估計），會讓 GAAP 獲利明顯轉差。
4. Class A 股東合計投票權不超過 49.9%，董事會過半由不持有經濟利益的 LTBT 選出。
5. 美國國防部的供應鏈風險認定，Anthropic 在 D.C. Circuit 以 2-1 遭駁回，聯邦地院的勝訴判決不足以解除風險。
6. 約 5%–7% 營收來自違規使用，會被清除。

哪邊論據較強：生意本身的看多證據比看空強，營收、客戶、現金流都是審計師簽過或 SEC 申報的數字。但估值與治理的看空論據更直接影響 Class A 股東的報酬。好公司不等於好價格。

---

## 十二、一頁紙決策表

```
公司：Anthropic, PBC        私募隱含估值：約 $9,976億（估計，Series H 價）
階段：Pre-IPO（S-1 已遞交，未生效）
資訊完整度：充分（S-1 含審計財報），定價資訊缺

核心邏輯：
1. 企業 AI 需求真實存在，Q2 2026 已營業獲利
2. 算力承諾是最大的槓桿，也是最大的風險
3. 私募價已反映多年高成長，治理結構不給 Class A 控制權

結論：觀望
重新評估觸發條件：
- IPO 價格區間揭露，隱含估值明顯低於 Series H
- 2026 年第三、四季 Compute and infrastructure 占營收比維持在六成以下
- D.C. Circuit 案出現新進展或和解
```

---

## 十三、資訊盲區

| 維度 | 已知 | 缺失 | 影響 |
|---|---|---|---|
| 發行條件 | 上市地、代號、承銷商 | 價格區間、股數、募資額 | 無法計算 IPO 估值與安全邊際 |
| 2026 年第三季 | 客戶數、NRR、客戶集中度 | 營收（原文空白） | 無法確認 Q2 的高成長是否延續 |
| 算力承諾 | 主要合約金額 | 分年付款表（原文空白） | 無法精算 2027–2030 年成本曲線 |
| Run-Rate Revenue | 定義 | 2026-10-31 數字（原文空白） | 少了最新營收動能指標 |
| 股東結構 | Amazon、Google 各持股超過 5% | 確切股數 | 無法計算策略股東轉讓後的投票權影響 |

在價格區間與第三季營收缺失的情況下，以上估值結論的置信度為中低。

---

## 十四、持續追蹤清單

- **S-1/A 修正版**：價格區間、發行股數、第三季營收、Run-Rate Revenue（預計 IPO 路演前揭露）。
- **每季財報**：Compute and infrastructure 占營收比是否守住；SpaceXAI 容量 2026 年 12 月到齊後的第一個完整季度。
- **SBC 與完全稀釋股數**：上市當季的一次性認列，以及 Public Benefit Issuances 是否觸發。
- **法律**：D.C. Circuit 案後續、Concord Music 簡易判決（2026-10-21 已開庭）、Reddit 案。
- **競爭**：OpenAI、Google 新模型發布後，Anthropic 下一季營收季增率。

---

## 十五、總結

Anthropic 的生意本質是把白領工作變成可按量計費的軟體服務，S-1 的審計數字證明這個需求是真的：單季營收在五個季度內從 $3.8億 成長到 $115.6億，第二季已經營業獲利。真正的問題在價格和結構。以私募價推算約 $1兆 的估值，需要營收再放大約三倍、並在扣除龐大算力與 SBC 後維持高利潤率；而公司已經簽下超過 $5,000億 的算力最低付款，Class A 股東又沒有實質控制權。最大的確定性是需求，最大的不確定性是算力承諾在需求放緩時的反作用力。建議等 IPO 定價與下兩季算力成本數字出來，若估值明顯低於 Series H 價再評估。

---

## 附錄：資料帳本

> 原始值取自 SEC EDGAR S-1（accession 0001628280-26-067168，以下稱「S-1」）原始精度；衍生值由 `tools/report_audit.py ledger` 以公式計算；勾稽列比對 S-1 揭露值與自算值。行號為本次將 S-1 HTML 轉為純文字後的行號，只用於定位，未附在倉庫內。

| ID | 項目 | 口徑 | 期間 | 值 | 單位 | 來源 | 公式 | 容差 |
|---|---|---|---|---|---|---|---|---|
| R1 | 營收 | GAAP | 2023 | 41 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Revenue |  |  |
| R2 | 營收 | GAAP | 2024 | 386 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Revenue |  |  |
| R3 | 營收 | GAAP | 2025 | 4585 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Revenue |  |  |
| R4 | 營收 | GAAP | H1 2025 | 1163 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Revenue |  |  |
| R5 | 營收 | GAAP | H1 2026 | 16286 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Revenue |  |  |
| Q1 | 營收 | GAAP 單季 | Q1 2025 | 376 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations Revenue |  |  |
| Q2 | 營收 | GAAP 單季 | Q2 2025 | 787 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations Revenue |  |  |
| Q3 | 營收 | GAAP 單季 | Q3 2025 | 1382 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations Revenue |  |  |
| Q4 | 營收 | GAAP 單季 | Q4 2025 | 2040 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations Revenue |  |  |
| Q5 | 營收 | GAAP 單季 | Q1 2026 | 4731 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations Revenue |  |  |
| Q6 | 營收 | GAAP 單季 | Q2 2026 | 11555 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations Revenue |  |  |
| E1 | Compute and infrastructure | GAAP | 2023 | 433 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| E2 | Compute and infrastructure | GAAP | 2024 | 2522 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| E3 | Compute and infrastructure | GAAP | 2025 | 7326 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| E4 | Compute and infrastructure | GAAP | H1 2025 | 2334 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| E5 | Compute and infrastructure | GAAP | H1 2026 | 8945 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| E6 | Compute and infrastructure | GAAP 單季 | Q1 2025 | 944 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations |  |  |
| E7 | Compute and infrastructure | GAAP 單季 | Q2 2025 | 1390 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations |  |  |
| E8 | Compute and infrastructure | GAAP 單季 | Q3 2025 | 2047 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations |  |  |
| E9 | Compute and infrastructure | GAAP 單季 | Q4 2025 | 2945 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations |  |  |
| E10 | Compute and infrastructure | GAAP 單季 | Q1 2026 | 3387 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations |  |  |
| E11 | Compute and infrastructure | GAAP 單季 | Q2 2026 | 5558 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations |  |  |
| P1 | Personnel | GAAP | 2023 | 95 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| P2 | Personnel | GAAP | 2024 | 454 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| P3 | Personnel | GAAP | 2025 | 1839 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| P4 | Personnel | GAAP | H1 2025 | 538 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| P5 | Personnel | GAAP | H1 2026 | 3152 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| S1 | Sales, marketing, and partnerships | GAAP | 2023 | 2 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| S2 | Sales, marketing, and partnerships | GAAP | 2024 | 43 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| S3 | Sales, marketing, and partnerships | GAAP | 2025 | 568 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| S4 | Sales, marketing, and partnerships | GAAP | H1 2025 | 120 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| S5 | Sales, marketing, and partnerships | GAAP | H1 2026 | 3168 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| X1 | Bartz settlement | GAAP | 2025 | 1500 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| O1 | 營業損益 | GAAP | 2023 | -551 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Operating loss |  |  |
| O2 | 營業損益 | GAAP | 2024 | -2980 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Operating loss |  |  |
| O3 | 營業損益 | GAAP | 2025 | -8060 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Operating loss |  |  |
| O4 | 營業損益 | GAAP | H1 2025 | -2135 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Operating loss |  |  |
| O5 | 營業損益 | GAAP | H1 2026 | -693 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Operating loss |  |  |
| O6 | 營業損益 | GAAP 單季 | Q1 2025 | -935 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations |  |  |
| O7 | 營業損益 | GAAP 單季 | Q2 2025 | -1200 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations |  |  |
| O8 | 營業損益 | GAAP 單季 | Q3 2025 | -3089 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations |  |  |
| O9 | 營業損益 | GAAP 單季 | Q4 2025 | -2836 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations |  |  |
| O10 | 營業損益 | GAAP 單季 | Q1 2026 | -1667 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations |  |  |
| O11 | 營業損益 | GAAP 單季 | Q2 2026 | 974 | 百萬美元 | SEC EDGAR S-1 MD&A Quarterly Results of Operations |  |  |
| F1 | 可轉換票據等公允價值變動 | GAAP | 2023 | -1045 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| F3 | 可轉換票據等公允價值變動 | GAAP | 2024 | -5434 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| F4 | 可轉換票據等公允價值變動 | GAAP | 2025 | -34308 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| F5 | 可轉換票據等公允價值變動 | GAAP | H1 2025 | -10942 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| F6 | 可轉換票據等公允價值變動 | GAAP | H1 2026 | -72388 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| F7 | Other income (expense), net | GAAP | H1 2026 | -8757 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations |  |  |
| N1 | 淨損 | GAAP | 2023 | -1531 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Net loss |  |  |
| N2 | 淨損 | GAAP | 2024 | -8309 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Net loss |  |  |
| N3 | 淨損 | GAAP | 2025 | -41965 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Net loss |  |  |
| N4 | 淨損 | GAAP | H1 2025 | -12969 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Net loss |  |  |
| N5 | 淨損 | GAAP | H1 2026 | -80748 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Statements of Operations Net loss |  |  |
| F2 | 公允價值變動占淨損比 | 自算 | H1 2026 |  | % | 計算 | =F6/N5*100 |  |
| A1 | Adjusted Operating Income (Loss) | Non-GAAP | 2023 | -522 | 百萬美元 | SEC EDGAR S-1 Non-GAAP Financial Measures |  |  |
| A2 | Adjusted Operating Income (Loss) | Non-GAAP | 2024 | -2788 | 百萬美元 | SEC EDGAR S-1 Non-GAAP Financial Measures |  |  |
| A3 | Adjusted Operating Income (Loss) | Non-GAAP | 2025 | -4854 | 百萬美元 | SEC EDGAR S-1 Non-GAAP Financial Measures |  |  |
| A4 | Adjusted Operating Income (Loss) | Non-GAAP | H1 2025 | -1849 | 百萬美元 | SEC EDGAR S-1 Non-GAAP Financial Measures |  |  |
| A5 | Adjusted Operating Income (Loss) | Non-GAAP | H1 2026 | 1618 | 百萬美元 | SEC EDGAR S-1 Non-GAAP Financial Measures |  |  |
| A6 | Adjusted Operating Margin | Non-GAAP | H1 2026 | 10 | % | SEC EDGAR S-1 Non-GAAP Financial Measures Adjusted Operating Margin 10% | =A5/R5*100 | 0.5 |
| G2 | 營收成長 | 自算年增 | 2025 |  | % | 計算 | =(R3/R2-1)*100 |  |
| G3 | 營收成長 | 自算年增 | H1 2026 | 1300 | % | SEC EDGAR S-1 MD&A revenue increased by $15.1 billion, or 1,300% | =(R5/R4-1)*100 | 0.5 |
| G4 | 營收年增 | 自算 | Q2 2026 | 1368 | % | SEC EDGAR S-1 Prospectus Summary revenue that grew 1,368% year over year for the three months ended June 30, 2026 | =(Q6/Q2-1)*100 | 0.5 |
| G5 | Compute and infrastructure 年增 | 自算 | Q2 2026 | 300 | % | SEC EDGAR S-1 Prospectus Summary compute and infrastructure expenses that grew 300% | =(E11/E7-1)*100 | 0.5 |
| G6 | 營收季增 | 自算 | Q2 2026 |  | % | 計算 | =(Q6/Q5-1)*100 |  |
| G7 | 營業利益率 | 自算 | Q2 2026 |  | % | 計算 | =O11/Q6*100 |  |
| G8 | Compute and infrastructure 占營收 | 自算 | 2025 |  | % | 計算 | =E3/R3*100 |  |
| G9 | Compute and infrastructure 占營收 | 自算 | H1 2025 | 201 | % | SEC EDGAR S-1 MD&A percentage of revenue 201% | =E4/R4*100 | 0.5 |
| G10 | Compute and infrastructure 占營收 | 自算 | H1 2026 | 55 | % | SEC EDGAR S-1 MD&A percentage of revenue 55% | =E5/R5*100 | 0.5 |
| G11 | Compute and infrastructure 季增 | 自算 | Q2 2026 |  | % | 計算 | =(E11/E10-1)*100 |  |
| C1 | Cost of revenue | GAAP 功能別 | 2025 | 2773 | 百萬美元 | SEC EDGAR S-1 Note 8 Supplemental Operating Expense Information |  |  |
| C2 | Cost of revenue | GAAP 功能別 | H1 2026 | 2380 | 百萬美元 | SEC EDGAR S-1 Note 8 Supplemental Operating Expense Information |  |  |
| C3 | Research and development | GAAP 功能別 | H1 2026 | 9741 | 百萬美元 | SEC EDGAR S-1 Note 8 Supplemental Operating Expense Information |  |  |
| C4 | 以 Cost of revenue 計算的毛利率 | 自算 | 2025 |  | % | 計算 | =(1-C1/R3)*100 |  |
| C5 | 以 Cost of revenue 計算的毛利率 | 自算 | H1 2026 |  | % | 計算 | =(1-C2/R5)*100 |  |
| R11 | 用量計費營收 | GAAP | H1 2026 | 13064 | 百萬美元 | SEC EDGAR S-1 Note 2 consumption-based revenue |  |  |
| R12 | 訂閱營收 | GAAP | H1 2026 | 3222 | 百萬美元 | SEC EDGAR S-1 Note 2 subscription-based revenue |  |  |
| R13 | 營收拆分合計 | 勾稽 | H1 2026 | 16286 | 百萬美元 | SEC EDGAR S-1 Note 2 Total | =R11+R12 |  |
| B1 | 現金及約當現金 | 期末 | 2026-06-30 | 112389 | 百萬美元 | SEC EDGAR S-1 Consolidated Balance Sheets |  |  |
| B2 | 短期投資 | 期末 | 2026-06-30 | 19262 | 百萬美元 | SEC EDGAR S-1 Consolidated Balance Sheets |  |  |
| B3 | 現金加短期投資 | 期末 | 2026-06-30 | 131651 | 百萬美元 | SEC EDGAR S-1 Summary Consolidated Balance Sheet Data | =B1+B2 |  |
| B4 | 應收帳款 | 期末 | 2026-06-30 | 5833 | 百萬美元 | SEC EDGAR S-1 Consolidated Balance Sheets |  |  |
| B5 | 遞延收入 | 期末 | 2026-06-30 | 1650 | 百萬美元 | SEC EDGAR S-1 Consolidated Balance Sheets |  |  |
| B6 | 可轉換票據（公允價值） | 期末 | 2026-06-30 | 108566 | 百萬美元 | SEC EDGAR S-1 Consolidated Balance Sheets Convertible notes payable |  |  |
| B7 | Redeemable convertible preferred stock | 期末 | 2026-06-30 | 157510 | 百萬美元 | SEC EDGAR S-1 Consolidated Balance Sheets |  |  |
| B8 | 總資產 | 期末 | 2026-06-30 | 147358 | 百萬美元 | SEC EDGAR S-1 Consolidated Balance Sheets |  |  |
| B9 | 累計虧損 | 期末 | 2026-06-30 | -132902 | 百萬美元 | SEC EDGAR S-1 Consolidated Balance Sheets |  |  |
| CF1 | 營業活動現金流 | GAAP | 2025 | -2637 | 百萬美元 | SEC EDGAR S-1 Consolidated Statements of Cash Flows |  |  |
| CF2 | 營業活動現金流 | GAAP | H1 2026 | 3929 | 百萬美元 | SEC EDGAR S-1 Consolidated Statements of Cash Flows |  |  |
| CF3 | 購置不動產及設備 | GAAP | 2025 | 131 | 百萬美元 | SEC EDGAR S-1 Consolidated Statements of Cash Flows Purchases of property and equipment |  |  |
| CF4 | 購置不動產及設備 | GAAP | H1 2026 | 482 | 百萬美元 | SEC EDGAR S-1 Consolidated Statements of Cash Flows Purchases of property and equipment |  |  |
| CF5 | Free cash flow | 自算 | 2025 |  | 百萬美元 | 計算 | =CF1-CF3 |  |
| CF6 | Free cash flow | 自算 | H1 2026 |  | 百萬美元 | 計算 | =CF2-CF4 |  |
| CF7 | 股份基礎薪酬 | 現金流量表 | 2025 | 1158 | 百萬美元 | SEC EDGAR S-1 Consolidated Statements of Cash Flows |  |  |
| CF8 | 股份基礎薪酬 | 現金流量表 | H1 2026 | 2185 | 百萬美元 | SEC EDGAR S-1 Consolidated Statements of Cash Flows |  |  |
| K1 | TTM 營收 $10 萬以上客戶數 | 營運指標 | 2026-09-30 | 11900 | 家 | SEC EDGAR S-1 Prospectus Summary More than 11,900 customers |  |  |
| K2 | TTM 營收 $100 萬以上客戶數 | 營運指標 | 2026-09-30 | 1900 | 家 | SEC EDGAR S-1 Prospectus Summary More than 1,900 customers |  |  |
| K3 | TTM 營收 $1,000 萬以上客戶數 | 營運指標 | 2026-09-30 | 250 | 家 | SEC EDGAR S-1 Prospectus Summary Approximately 250 customers |  |  |
| K4 | Net Revenue Retention | 營運指標 | 2026-09-30 | 900 | % | SEC EDGAR S-1 Prospectus Summary Net Revenue Retention of approximately 900% |  |  |
| K5 | 員工人數 | 期末 | 2026-09-30 | 5300 | 人 | SEC EDGAR S-1 Business Human Capital |  |  |
| K6 | 雲端市集營收占比 | 營運指標 | H1 2026 | 48 | % | SEC EDGAR S-1 Risk Factors CSP marketplaces 48% |  |  |
| K7 | 前五大客戶營收占比 | 營運指標 | 2026 前九月 | 25 | % | SEC EDGAR S-1 Risk Factors top five customers approximately 25% |  |  |
| K8 | 違規使用客戶營收占比下限 | 公司估計 | 2026 前九月 | 5 | % | SEC EDGAR S-1 MD&A approximately 5% to 7% of our revenue |  |  |
| K11 | 違規使用客戶營收占比上限 | 公司估計 | 2026 前九月 | 7 | % | SEC EDGAR S-1 MD&A approximately 5% to 7% of our revenue |  |  |
| K9 | 政府機構營收占比 | 營運指標 | 各期 | 1 | % | SEC EDGAR S-1 Risk Factors approximately 1% of our revenue |  |  |
| K10 | 累計募資 | 累計 | 2026-06-30 | 141.1 | 十億美元 | SEC EDGAR S-1 Prospectus Summary raised an aggregate of $141.1 billion |  |  |
| M1 | 固定或最低付款承諾 | 截至期末 | 2026-06-30 | 265.6 | 十億美元 | SEC EDGAR S-1 Note 13 Commitments approximately $265.6 billion |  |  |
| M2 | 期後新增最低付款義務 | 期後 | 2026-06-30 至 2026-10-26 | 245 | 十億美元 | SEC EDGAR S-1 Note 17 Subsequent Events approximately $245 billion |  |  |
| M3 | 期後短期合約最低付款 | 期後 | 2026-06-30 至 2026-10-26 | 21 | 十億美元 | SEC EDGAR S-1 Note 17 Subsequent Events approximately $21 billion |  |  |
| M11 | 最低付款承諾合計 | 自算 | 2026-10-26 |  | 十億美元 | 計算 | =M1+M2+M3 |  |
| M4 | Broadcom 設備租賃租金 | 合約總額 | 2026-10-26 | 161.2 | 十億美元 | SEC EDGAR S-1 MD&A Infrastructure Equipment Leases |  |  |
| M5 | Google 算力承諾 | 合約最低 | 2026-10-26 | 114.5 | 十億美元 | SEC EDGAR S-1 MD&A Infrastructure Service Arrangements |  |  |
| M6 | SpaceXAI 算力承諾 | 合約上限 | 2026-10-26 | 120.5 | 十億美元 | SEC EDGAR S-1 MD&A Infrastructure Service Arrangements |  |  |
| M7 | Amazon 算力承諾 | 合約最低 | 2026-10-26 | 110.0 | 十億美元 | SEC EDGAR S-1 MD&A Infrastructure Service Arrangements |  |  |
| M8 | Microsoft 算力承諾 | 合約最低 | 2026-10-26 | 44.9 | 十億美元 | SEC EDGAR S-1 MD&A Infrastructure Service Arrangements |  |  |
| M9 | Nscale 算力承諾 | 合約上限 | 2026-10-26 | 44.6 | 十億美元 | SEC EDGAR S-1 MD&A Infrastructure Service Arrangements |  |  |
| M10 | Lambda 算力承諾 | 合約總額 | 2026-10-26 | 41.3 | 十億美元 | SEC EDGAR S-1 MD&A Infrastructure Service Arrangements |  |  |
| M16 | Google 等 TPU 額外算力下限 | 公司估計 | 2028–2031 | 125 | 十億美元 | SEC EDGAR S-1 MD&A approximately $125.0 billion to $150.0 billion |  |  |
| M19 | Google 等 TPU 額外算力上限 | 公司估計 | 2028–2031 | 150 | 十億美元 | SEC EDGAR S-1 MD&A approximately $125.0 billion to $150.0 billion |  |  |
| M17 | AMD Helios 機櫃 | 公司估計 | 2027 起 | 20 | 十億美元 | SEC EDGAR S-1 MD&A expect aggregate expenditures to exceed $20.0 billion |  |  |
| M18 | SpaceXAI 每月費用 | 容量到齊後 | 2026-12 起 | 3.1 | 十億美元 | SEC EDGAR S-1 MD&A approximately $3.1 billion in the aggregate per month |  |  |
| M12 | SpaceXAI 年化費用 | 自算 | 2026-12 起 |  | 十億美元 | 計算 | =M18*12 |  |
| M13 | Compute and infrastructure 年化 | 自算 | Q2 2026 |  | 十億美元 | 計算 | =E11*4/1000 |  |
| Q7 | 營收年化 | 自算 | Q2 2026 |  | 十億美元 | 計算 | =Q6*4/1000 |  |
| M14 | 最低付款承諾 ÷ 營收 | 自算 | H1 2026 |  | 倍 | 計算 | =M11*1000/R5 |  |
| M15 | 最低付款承諾 ÷ 年化營收 | 自算 | Q2 2026 |  | 倍 | 計算 | =M11/Q7 |  |
| V1 | Amazon 票據可轉股數 | 期末 | 2026-06-30 | 1840444962 | 股 | SEC EDGAR S-1 MD&A Convertible Notes table |  |  |
| V2 | 票據公允價值隱含每股價值 | 自算 | 2026-06-30 |  | 美元 | 計算 | =B6*1000000/V1 |  |
| V5 | Series H-1 每股價格 | 私募 | 2026-05 至 2026-06 | 589.0095 | 美元 | SEC EDGAR S-1 Certain Relationships Series H Redeemable Convertible Preferred Stock Financing |  |  |
| V6 | 特別股轉換比 | 期末 | 2026-06-30 | 10 | 倍 | SEC EDGAR S-1 Note 10 conversion ratio 10:1 |  |  |
| V3 | Series H 每普通股價格 | 自算 | 2026-06-30 |  | 美元 | 計算 | =V5/V6 |  |
| V4 | Public Benefit Fund 持有 Class N | 發行 | 2026-06-30 | 846840960 | 股 | SEC EDGAR S-1 Prospectus Summary Initial Public Benefit Issuance |  |  |
| V7 | Public Benefit 股數占完全稀釋比 | 公司揭露 | 2026-06-30 | 5 | % | SEC EDGAR S-1 Prospectus Summary representing 5% of our fully diluted shares |  |  |
| V8 | 完全稀釋股數 | 估計 | 2026-06-30 |  | 股 | 計算 | =V4/(V7/100) |  |
| V9 | Series H 隱含股權價值 | 估計 | 2026-06-30 |  | 十億美元 | 計算 | =V8*V3/1000000000 |  |
| V10 | Series H 隱含價值 ÷ 年化營收 | 估計 | Q2 2026 |  | 倍 | 計算 | =V9/Q7 |  |
| V11 | 假設本益比 | 估計 | 終局 | 25 | 倍 | 假設：成熟大型軟體公司常見區間中段 |  |  |
| V12 | 假設淨利率 | 估計 | 終局 | 30 | % | 假設：成熟大型軟體公司水準 |  |  |
| V13 | 支撐隱含價值所需營收 | 估計 | 終局 |  | 十億美元 | 計算 | =V9/V11/(V12/100) |  |
| V14 | 所需營收 ÷ 年化營收 | 估計 | 終局 |  | 倍 | 計算 | =V13/Q7 |  |
| SB1 | RSU 未認列費用 | 若 2026-06-30 上市 | 2026-06-30 | 23.7 | 十億美元 | SEC EDGAR S-1 Risk Factors additional $23.7 billion of unrecognized stock-based compensation |  |  |
| SB2 | RSU 攤提年數 | 加權平均 | 2026-06-30 | 2.1 | 年 | SEC EDGAR S-1 Risk Factors weighted-average period of approximately 2.1 years |  |  |
| SB3 | RSU 年化費用 | 估計 | 上市後 |  | 十億美元 | 計算 | =SB1/SB2 |  |
| G1 | Class F 投票權 | 發行後 | IPO 後 | 50.1 | % | SEC EDGAR S-1 Prospectus Summary Founder Voting Structure |  |  |
