"""FinMind 金鑰檢查 — 確認目前這個環境取數時，金鑰有沒有生效。

零外部依賴（僅 stdlib），本機、雲端 session、GitHub Actions 共用。
金鑰有三條可能的來路，本腳本會逐一判斷：

    1. 環境變數 FINMIND_TOKEN
       — 本機 export，或 Claude Code 雲端環境的 Environment variables，
         或 GitHub Actions 由 Repository secret 注入
    2. 本地檔案 local/finmind_token.txt（local/ 已被 .gitignore 永久排除）
    3. 雲端環境的 API credential — 金鑰存在 Claude Code 環境設定裡，由 agent proxy
       在請求離開 session 之後才補上 Authorization 標頭。session 內看不到金鑰，
       前兩項都會是空的，這是預期行為，不是沒設定

**任何情況下都不會印出 token 內容**，只印 sha256 前 8 碼指紋，用來確認「機器上這把」
與「你手上那把」是不是同一把。倉庫是 public，Actions 執行紀錄任何人都看得到，
輸出一律先過遮罩再印。

用法：
    python3 tools/finmind_token_check.py                 # 檢查目前環境
    python3 tools/finmind_token_check.py --require-token # 找不到金鑰就失敗（給 CI 用）

Exit code：0 取數正常／1 金鑰無效或連線失敗／2 --require-token 且找不到金鑰
"""

import argparse
import hashlib
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, timedelta

_DATA_API = "https://api.finmindtrade.com/api/v4/data"
_USER_API = "https://api.web.finmindtrade.com/v2/user_info"
_TIMEOUT = 30
_TOKEN_FILE = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "local", "finmind_token.txt",
)


def _load_token():
    """回傳 (token, 來源說明)；都找不到則 (None, None)。"""
    t = os.environ.get("FINMIND_TOKEN", "").strip()
    if t:
        return t, "環境變數 FINMIND_TOKEN"
    try:
        with open(_TOKEN_FILE, encoding="utf-8") as f:
            t = f.read().strip()
        if t:
            return t, "本地檔案 local/finmind_token.txt"
    except OSError:
        pass
    return None, None


def _fingerprint(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()[:8]


def _redact(text, token):
    """把任何可能夾帶 token 的字串遮掉，避免寫進公開的執行紀錄。"""
    text = str(text)
    if token and token in text:
        text = text.replace(token, "***REDACTED***")
    return text


def _get_json(url, token):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            return json.loads(resp.read().decode("utf-8")), None
    except urllib.error.HTTPError as e:
        return None, f"HTTP {e.code}"
    except urllib.error.URLError as e:
        return None, _redact(f"網路連線失敗：{e.reason}", token)
    except json.JSONDecodeError:
        return None, "回應不是合法 JSON"


def _check_usage(token):
    """查 FinMind 帳號等級與本小時用量。查不到不算失敗，回傳 None。"""
    url = f"{_USER_API}?{urllib.parse.urlencode({'token': token})}"
    payload, err = _get_json(url, token)
    if err or not payload or payload.get("status") != 200:
        return None
    return payload


def _check_data(token):
    """實際打一次資料 API，確認這把金鑰真的能取數。"""
    start = (date.today() - timedelta(days=14)).isoformat()
    params = {"dataset": "TaiwanStockPrice", "data_id": "2330", "start_date": start}
    if token:
        params["token"] = token
    url = f"{_DATA_API}?{urllib.parse.urlencode(params)}"
    payload, err = _get_json(url, token)
    if err:
        return False, err
    if payload.get("status") != 200:
        return False, _redact(payload.get("msg", "未知錯誤"), token)
    rows = payload.get("data", [])
    if not rows:
        return False, "API 回應成功但沒有資料"
    last = rows[-1]
    return True, f"TaiwanStockPrice 2330 取得 {len(rows)} 筆，最新 {last.get('date')} 收盤 {last.get('close')}"


def _probe_proxy_credential():
    """判斷是否有 agent proxy 在請求離開 session 後改寫認證標頭。

    刻意帶一個必定無效的 Bearer 標頭去打 API：
      - 仍然回 200 ⇒ 一定有東西把這個標頭換掉了，也就是環境的 API credential 生效
      - 回 400（Token is illegal）⇒ 無法判定：可能沒設，也可能 proxy 只在標頭
        缺席時才注入。不做任何結論
    """
    params = {"dataset": "TaiwanStockInfo", "data_id": "2330"}
    url = f"{_DATA_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={
        "User-Agent": "Mozilla/5.0",
        "Authorization": "Bearer invalid-probe-value",
    })
    try:
        with urllib.request.urlopen(req, timeout=_TIMEOUT) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
        return payload.get("status") == 200
    except Exception:
        return False


def main():
    parser = argparse.ArgumentParser(description="檢查 FinMind 取數金鑰是否生效（不會印出 token）")
    parser.add_argument(
        "--require-token", action="store_true",
        help="session 內找不到金鑰就視為失敗（給 CI 用；雲端 API credential 生效時仍算通過）",
    )
    args = parser.parse_args()

    token, source = _load_token()
    print("FinMind 金鑰檢查")

    if not token:
        print("來源：session 內沒有金鑰（環境變數 FINMIND_TOKEN 與 local/finmind_token.txt 都是空的）")
        if _probe_proxy_credential():
            print("代理注入：偵測到 agent proxy 改寫了認證標頭 ⇒ 雲端環境的 API credential 生效")
            ok, detail = _check_data(None)
            print(f"資料連線：{'成功' if ok else '失敗'} — {detail}")
            print("結論：金鑰有效（存在 Claude Code 環境設定，session 內看不到是正常的）")
            return 0 if ok else 1

        ok, detail = _check_data(None)
        print(f"資料連線：{'成功' if ok else '失敗'} — {detail}（無法分辨是匿名額度還是 proxy 注入）")
        print("設定方式見 docs/finmind-token.md：手機／雲端 session 走 Claude Code 環境設定，")
        print("本機走環境變數或 local/finmind_token.txt，GitHub Actions 走 Repository secret")
        if args.require_token:
            return 2
        return 0 if ok else 1

    print(f"來源：{source}")
    print(f"指紋：sha256:{_fingerprint(token)}（長度 {len(token)}）")

    usage = _check_usage(token)
    if usage:
        limit = usage.get("api_request_limit")
        used = usage.get("user_count")
        level = usage.get("level", usage.get("user_level"))
        if level is not None:
            print(f"帳號等級：{_redact(level, token)}")
        if limit is not None and used is not None:
            print(f"本小時用量：{used} / {limit}")
        elif limit is not None:
            print(f"每小時額度：{limit}")
    else:
        print("用量查詢：查不到（不影響金鑰本身，FinMind 用量端點偶爾不回應）")

    ok, detail = _check_data(token)
    print(f"資料連線：{'成功' if ok else '失敗'} — {detail}")
    if ok:
        print("結論：金鑰有效")
        return 0
    print("結論：金鑰無效或已過期。到 https://finmindtrade.com 重新取得 token 後更新")
    return 1


if __name__ == "__main__":
    sys.exit(main())
