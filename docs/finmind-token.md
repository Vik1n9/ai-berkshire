# FinMind API 金鑰保管與設定

FinMind 是台股資料的主來源（見 `skills/financial-data.md`）。未註冊可以匿名取數，
但有小時級限額；註冊後的 API token 能拉高額度、解鎖部分 dataset。

token 是憑證，不是設定值：**不進 git、不進報告、不出現在任何輸出**。
`.gitignore` 已經永久排除 `/local/`、`.env*`、`*_token.txt`、`*.token`，
但那只是最後一道防線，真正的保管位置是下面三處。

## 金鑰放哪裡

| 位置 | 誰讀得到 | 用途 |
|------|---------|------|
| GitHub Repository secret `FINMIND_TOKEN` | 只有本倉庫的 GitHub Actions | 排程／CI 取數、金鑰有效性檢查 |
| 環境變數 `FINMIND_TOKEN` | 當下這台機器的 shell、Claude Code | 本機跑 skill 與 `tools/twstock_data.py` |
| `local/finmind_token.txt` | 本機 | 懶得每次 export 時的備援，`local/` 永不入庫 |

三者互不相通。**在 GitHub 存了 secret，本機跑 skill 不會自動拿到**——GitHub secret
只在 Actions 執行時注入。反過來也一樣。要哪邊能用，就在哪邊設一份。

`tools/twstock_data.py` 與 `tools/finmind_token_check.py` 的讀取順序一致：
環境變數 `FINMIND_TOKEN` 優先，其次 `local/finmind_token.txt`，都沒有就匿名取數。

## 一、取得 token

1. 到 https://finmindtrade.com 註冊／登入
2. 後台頁面（Data / API Token 區塊）複製 API token
3. 免費帳號有每小時請求上限，Backer／Sponsor 層級額度更高、可用 dataset 更多

## 二、把 token 存進 GitHub

**網頁操作**：開 https://github.com/Vik1n9/ai-berkshire/settings/secrets/actions/new
（路徑是 Settings → Secrets and variables → Actions → New repository secret）

- Name：`FINMIND_TOKEN`
- Secret：貼上 token，按 Add secret

存進去之後就讀不出來了，只能覆蓋（Update）或刪除，所以自己那份要留著。

**指令操作**（本機裝了 gh CLI 的話，貼上時不會留在 shell history）：

```bash
gh secret set FINMIND_TOKEN --repo Vik1n9/ai-berkshire
# 出現 "Paste your secret:" 後貼上，Enter
```

## 三、驗證這把金鑰有效

到 Actions → 「FinMind 金鑰檢查」→ Run workflow，或本機直接跑：

```bash
FINMIND_TOKEN='貼上token' python3 tools/finmind_token_check.py
```

輸出長這樣（**不會印出 token 內容**，只印 sha256 前 8 碼指紋，用來確認機器上這把
和你手上那把是同一把）：

```
FinMind 金鑰檢查
來源：環境變數 FINMIND_TOKEN
指紋：sha256:398ec870（長度 28）
本小時用量：12 / 600
資料連線：成功 — TaiwanStockPrice 2330 取得 10 筆，最新 2026-08-28 收盤 2420.0
結論：金鑰有效
```

exit code：0 有效／1 無效或過期／2 找不到金鑰。`--allow-anonymous` 會讓「找不到金鑰」
只警告不失敗（退回匿名模式）。

`.github/workflows/finmind-token-check.yml` 除了手動觸發，每週一 09:00（台北時間）
自動跑一次，token 過期時不必等到要用才發現。

## 四、本機設定

擇一即可：

```bash
# 方式 A：寫進 shell profile（~/.zshrc 或 ~/.bashrc）
echo 'export FINMIND_TOKEN="貼上token"' >> ~/.zshrc && source ~/.zshrc

# 方式 B：寫進本地檔案（local/ 已被 .gitignore 永久排除）
mkdir -p local && printf '%s' '貼上token' > local/finmind_token.txt
chmod 600 local/finmind_token.txt
```

Claude Code on the web 的遠端 session 是另一台機器，本機的環境變數不會跟過去。
要讓遠端 session 也拿得到，把 `FINMIND_TOKEN` 加進該環境的 environment variables
設定（見 https://code.claude.com/docs/en/claude-code-on-the-web）。

## 五、在其他 workflow 用這把金鑰

secret 不會自動出現在環境裡，要在需要的 step 明確注入：

```yaml
      - name: 取台股資料
        env:
          FINMIND_TOKEN: ${{ secrets.FINMIND_TOKEN }}
        run: python3 tools/twstock_data.py quote 2330
```

只在真正需要的 step 加 `env:`，不要整個 job 都掛上去。

## 六、安全守則

本倉庫是 **public**，Actions 的執行紀錄任何人都看得到，所以：

- workflow 不接 `pull_request` / `pull_request_target` 觸發。GitHub 預設不會把 secret
  給來自 fork 的 PR，但 `pull_request_target` 會在基底分支的權限下跑，等於把金鑰交給
  外部 PR 的內容擺佈——不要用。
- 不要 `echo $FINMIND_TOKEN`、不要 `set -x`、不要把 token 拼進 URL 後印出來。
  GitHub 會自動遮罩 secret 的完整字串，但經過 base64、切片、拼接就遮不住了。
- token 不得出現在報告、skill 檔、commit message、issue、PR 內容裡。

**輪替**：到 FinMind 後台重新產生 token，回到步驟二覆蓋 secret，本機那份也一起換掉。

**懷疑外洩時**：先去 FinMind 後台作廢舊 token 再換新的——把新 token 存進 GitHub 只是
換鎖，舊鑰匙沒作廢一樣開得了門。若 token 曾被 commit 進 git，改檔案沒有用，
history 裡還在，必須當作已外洩處理。
