# FinMind API 金鑰：放哪裡、怎麼設、怎麼確認有生效

FinMind 是台股資料的主來源（見 `skills/financial-data.md`）。未註冊可以匿名取數，
但有小時級限額；註冊後的 API token 能拉高額度、解鎖部分 dataset。

## 先看你要在哪裡用

金鑰不是設定值，是憑證，而且**三個地方互不相通**——在一處設好，另外兩處還是空的。

| 使用情境 | 金鑰要放哪 | 讀得到的人 |
|---------|-----------|-----------|
| **手機／雲端 session**（Claude App、claude.ai/code、`claude --cloud`） | Claude Code **雲端環境設定**：API credential（建議）或 Environment variables | 該環境跑的所有 session |
| 本機終端機跑 skill 或 `tools/twstock_data.py` | 環境變數 `FINMIND_TOKEN`，或 `local/finmind_token.txt` | 這台機器 |
| GitHub Actions（排程檢查、CI 取數） | Repository secret `FINMIND_TOKEN` | 只有本倉庫的 Actions |

**GitHub 的 Repository secret 只有 Actions 讀得到，雲端 session 拿不到**——secret 存進去就
只能覆寫不能讀出，沒有任何 API 能把它交給 session。手機上要能取數，設定要做在
Claude Code 的雲端環境裡，不是做在 GitHub。

`tools/twstock_data.py` 與 `tools/finmind_token_check.py` 讀取順序一致：
環境變數 `FINMIND_TOKEN` → `local/finmind_token.txt` → 都沒有就匿名（或由 proxy 注入）。

## 一、取得 token

到 https://finmindtrade.com 註冊／登入，在後台（Data / API Token 區塊）複製 API token。
免費帳號有每小時請求上限，Backer／Sponsor 層級額度更高、可用 dataset 更多
（例如 `TaiwanStockMarketValue` 免費層會回 `Your level is free`）。

## 二、手機／雲端 session（這是你要的那條路）

雲端環境在 [claude.ai/code](https://claude.ai/code) 設定：點訊息框上方那排顯示目前環境名稱的
**雲朵圖示**，滑到該環境上按**齒輪**，開啟 **Update cloud environment** 對話框。
沒有其他入口，也沒有直達網址。同一組環境設定適用於網頁、手機 App、桌面 App、
終端機的 `claude --cloud` 與 routines。

### 做法 A：API credential（建議）

對話框裡 **Environment variables** 下方的 **API credentials** → **Add credential**：

- **Credential type**：保持預設 **Bearer**
- **Name**：隨便給個標籤，例如 `FinMind`
- **Allowed websites**：`api.finmindtrade.com`
- **Custom headers**：保持 Name `Authorization`、Prefix `Bearer`，**Value** 貼上 token
- 按 **Connect** 存檔（不需要再按 Save changes）

金鑰存在環境設定裡，由 Anthropic 的 agent proxy 在請求**離開 session 之後**才補上
`Authorization` 標頭。token 不會進到 session 的環境變數、不會進到任何檔案，Claude 看不到，
自然也不可能被寫進報告或 commit。FinMind v4 API 吃這個標頭（實測帶無效 token 會回
`Token is illegal`，代表標頭確實有被讀），所以這條路可行。

附帶好處：列在 **Allowed websites** 的網域，即使環境的 network access 等級原本不放行，
session 也連得到。做法 B 沒有這個效果，得靠環境的網路政策本來就允許 `api.finmindtrade.com`
（本倉庫目前使用的環境實測可通）。

限制：需要 claude.ai 組織的 Admin／Owner 角色（Pro、Max 在自己的組織裡就有）；
只能刪除重加，不能編輯；存檔後看不到值。另外用量查詢端點
`api.web.finmindtrade.com/v2/user_info` 只認 query 參數形式的 token，走這條路查不到用量。

### 做法 B：Environment variables

同一個對話框的 **Environment variables** 欄位，`.env` 格式加一行：

```
FINMIND_TOKEN=貼上token
```

按 **Save changes**。工具會自動讀到，用量查詢也能用。

代價：官方文件明說**任何使用這個環境的人都讀得到這些值**，而且 Claude 在 session 裡
`env` 一下就看得到，因此有被寫進輸出的風險。自己一個人用的個人環境可以接受，
在意的話用做法 A。

### 兩者共同的注意事項

session 只在**啟動時**複製一次環境設定。改完之後，已經在跑的 session 不會生效，
要**開一個新 session**。

## 三、確認金鑰真的有生效

在雲端 session（或本機）裡跑：

```bash
python3 tools/finmind_token_check.py
```

三種可能的輸出：

```
來源：環境變數 FINMIND_TOKEN
指紋：sha256:398ec870（長度 28）
本小時用量：12 / 600
資料連線：成功 — TaiwanStockPrice 2330 取得 10 筆，最新 2026-08-28 收盤 2420.0
結論：金鑰有效
```

```
來源：session 內沒有金鑰（環境變數 FINMIND_TOKEN 與 local/finmind_token.txt 都是空的）
代理注入：偵測到 agent proxy 改寫了認證標頭 ⇒ 雲端環境的 API credential 生效
結論：金鑰有效（存在 Claude Code 環境設定，session 內看不到是正常的）
```

```
來源：session 內沒有金鑰（…都是空的）
資料連線：成功 — …（無法分辨是匿名額度還是 proxy 注入）
```

第三種代表兩條路都沒設好，目前是匿名額度在跑（或 proxy 用的是「標頭缺席才注入」的策略，
腳本無法分辨，不硬下結論）。腳本只印 token 的 sha256 前 8 碼與長度，不會印出 token 本身。

exit code：0 取數正常／1 金鑰無效或過期／2 加了 `--require-token` 卻找不到金鑰。

## 四、本機

擇一即可：

```bash
# 方式 A：寫進 shell profile（~/.zshrc 或 ~/.bashrc）
echo 'export FINMIND_TOKEN="貼上token"' >> ~/.zshrc && source ~/.zshrc

# 方式 B：寫進本地檔案（local/ 已被 .gitignore 永久排除）
mkdir -p local && printf '%s' '貼上token' > local/finmind_token.txt
chmod 600 local/finmind_token.txt
```

## 五、GitHub Actions

只有需要讓 Actions 自己取數時才要設。開
https://github.com/Vik1n9/ai-berkshire/settings/secrets/actions/new
（Settings → Secrets and variables → Actions → New repository secret），
Name 填 `FINMIND_TOKEN`，貼上 token。或用 gh CLI（不會留在 shell history）：

```bash
gh secret set FINMIND_TOKEN --repo Vik1n9/ai-berkshire
```

`.github/workflows/finmind-token-check.yml` 每週一 09:00（台北時間）跑一次
`finmind_token_check.py --require-token`，token 過期時不必等到要用才發現；也可以到
Actions 頁面手動 Run workflow。這支 workflow 檢查的是**Actions 那一份** secret，
與雲端 session 用的那份是兩把獨立的鑰匙，換 token 時記得兩邊都換。

其他 workflow 要用這把金鑰，在需要的那個 step 明確注入，不要整個 job 掛上去：

```yaml
      - name: 取台股資料
        env:
          FINMIND_TOKEN: ${{ secrets.FINMIND_TOKEN }}
        run: python3 tools/twstock_data.py quote 2330
```

## 六、安全守則

本倉庫是 **public**，Actions 的執行紀錄任何人都看得到：

- workflow 不接 `pull_request` / `pull_request_target` 觸發。GitHub 預設不會把 secret 給
  來自 fork 的 PR，但 `pull_request_target` 會在基底分支的權限下跑，等於把金鑰交給外部
  PR 的內容擺佈——不要用。
- 不要 `echo $FINMIND_TOKEN`、不要 `set -x`、不要把 token 拼進 URL 後印出來。GitHub 會
  自動遮罩 secret 的完整字串，但經過 base64、切片、拼接就遮不住了。
- token 不得出現在報告、skill 檔、commit message、issue、PR 內容裡。雲端 session 的
  對話紀錄同理——不要在對話裡貼 token 叫 Claude 寫進檔案，要嘛設環境變數，要嘛用
  API credential。
- `.gitignore` 已永久排除 `/local/`、`.env*`、`*_token.txt`、`*.token`，但那是最後一道
  防線，不是保管方式。

**輪替**：到 FinMind 後台重新產生 token，回頭更新你有設的每一處（雲端環境、本機、
GitHub secret）。

**懷疑外洩時**：先去 FinMind 後台作廢舊 token 再換新的——只換新的等於換鎖沒收鑰匙。
若 token 曾被 commit 進 git，改檔案沒有用，history 裡還在，必須當作已外洩處理。
