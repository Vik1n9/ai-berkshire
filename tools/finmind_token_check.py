#!/usr/bin/env python3
"""FinMind 金鑰檢查 — 驗證 FINMIND_TOKEN 是否有效，並回報用量額度。

零外部依賴（僅 stdlib），供本機與 GitHub Actions 共用。
token 讀取優先順序與 tools/twstock_data.py 完全一致：
    1. 環境變數 FINMIND_TOKEN（GitHub Actions 由 Repository Secret 注入）
    2. 本地檔案 local/finmind_token.txt（local/ 已被 .gitignore 永久排除）

**本腳本任何情況下都不會印出 token 內容**，只印出 sha256 前 8 碼的指紋，
用來確認「機器上這把」與「你手上那把」是不是同一把。倉庫是 public，
Actions 執行紀錄任何人都看得到，所以輸出一律先過遮罩再印。

用法：
    python3 tools/finmind_token_check.py                # 沒有 token 時 exit 2
    python3 tools/finmind_token_check.py --allow-anonymous  # 沒有 token 時只警告，exit 0

Exit code：0 金鑰有效（或匿名模式放行）／1 金鑰無效或連線失敗／2 找不到金鑰
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


def main():
    parser = argparse.ArgumentParser(description="檢查 FinMind API 金鑰是否有效（不會印出 token）")
    parser.add_argument(
        "--allow-anonymous", action="store_true",
        help="找不到金鑰時只警告不失敗（匿名模式仍可取數，但有小時級限額）",
    )
    args = parser.parse_args()

    token, source = _load_token()
    print("FinMind 金鑰檢查")

    if not token:
        print("來源：找不到金鑰（環境變數 FINMIND_TOKEN 與 local/finmind_token.txt 都是空的）")
        if args.allow_anonymous:
            ok, detail = _check_data(None)
            print(f"匿名取數：{'成功' if ok else '失敗'} — {detail}")
            print("結論：以匿名模式運作，額度受限。設定金鑰請見 docs/finmind-token.md")
            return 0 if ok else 1
        print("結論：未設定金鑰。GitHub → Settings → Secrets and variables → Actions")
        print("      新增 Repository secret，名稱 FINMIND_TOKEN，內容貼上 FinMind 後台的 API token")
        print("      詳細步驟見 docs/finmind-token.md")
        return 2

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
    print("結論：金鑰無效或已過期。到 https://finmindtrade.com 重新取得 token 後更新 Secret")
    return 1


if __name__ == "__main__":
    sys.exit(main())
