#!/usr/bin/env python3
"""AutoIP 文生圖範例：送出任務 → 輪詢狀態 → 下載第一張圖。

10-16 已對照官方規格 autoip_openapi_20261016.yaml（同資料夾）。
autoip.app 前面有 Cloudflare，Python 預設 User-Agent 會被擋（403 error code 1010），
所以請求一律帶自訂 User-Agent。

金鑰只從環境變數 AUTOIP_API_KEY 讀，不寫在程式裡。
只用 Python 標準函式庫，不需要另外安裝套件。

用法：
    python3 autoip_text_to_image.py "a quiet office desk with documents, natural light" \
        --size 1024x768 --out 輸出.png

每次送出會扣 AutoIP 點數；任務失敗時平台會自動退點（依 SKILL.md）。
"""

import argparse
import json
import os
import sys
import time
import urllib.error
import urllib.request
import uuid

FINAL_STATES = {"completed", "failed", "timeout", "cancelled"}


def base_url():
    root = os.environ.get("AUTOIP_BASE_URL", "https://autoip.app").rstrip("/")
    return root + "/api/v1"


def api_key():
    key = os.environ.get("AUTOIP_API_KEY", "").strip()
    if not key:
        sys.exit("錯誤：沒有設定環境變數 AUTOIP_API_KEY（aip_ 開頭）。"
                 "請到 https://autoip.app/dashboard/api-keys 申請後設成環境變數。")
    if not key.startswith("aip_"):
        sys.exit("錯誤：AUTOIP_API_KEY 應以 aip_ 開頭。")
    return key


def request(method, path, key, body=None, content_type=None):
    req = urllib.request.Request(base_url() + path, data=body, method=method)
    req.add_header("Authorization", "Bearer " + key)
    req.add_header("User-Agent", "curl/8.5.0")
    req.add_header("Accept", "application/json")
    if content_type:
        req.add_header("Content-Type", content_type)
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:
            return resp.status, resp.headers, resp.read()
    except urllib.error.HTTPError as e:
        raw = e.read()
        try:
            info = json.loads(raw)
            msg = f"{info.get('error_code')}: {info.get('message')}"
            if info.get("errors"):
                msg += f" {info['errors']}"
        except ValueError:
            msg = raw[:300].decode("utf-8", "replace")
        retry = e.headers.get("Retry-After")
        sys.exit(f"HTTP {e.code} {method} {path} → {msg}"
                 + (f"（Retry-After {retry} 秒）" if retry else ""))
    except urllib.error.URLError as e:
        sys.exit(f"連不到 {base_url()}：{e.reason}")


def get_json(path, key):
    _, _, raw = request("GET", path, key)
    return json.loads(raw)


def multipart(fields):
    boundary = "----autoip" + uuid.uuid4().hex
    parts = []
    for name, value in fields.items():
        parts.append(f"--{boundary}\r\n"
                     f'Content-Disposition: form-data; name="{name}"\r\n\r\n'
                     f"{value}\r\n")
    parts.append(f"--{boundary}--\r\n")
    return "".join(parts).encode("utf-8"), "multipart/form-data; boundary=" + boundary


def main():
    p = argparse.ArgumentParser(description="AutoIP 文生圖")
    p.add_argument("prompt", help="提示詞（英文效果較佳）")
    p.add_argument("--size", help="1024x1024 / 1024x768 / 768x1024 / 960x540 / 540x960")
    p.add_argument("--mode", help="standard / hd_4k / v2 / v3 / anime")
    p.add_argument("--steps", type=int, help="4–50；v3／anime 模式不生效")
    p.add_argument("--negative", help="negative_prompt")
    p.add_argument("--out", default="autoip_output.png", help="存檔路徑")
    p.add_argument("--interval", type=float, default=8, help="輪詢間隔秒數（5–10）")
    p.add_argument("--max-wait", type=float, default=600, help="最長等待秒數")
    p.add_argument("--check-only", action="store_true",
                   help="只查帳戶、餘額、價目，不送出任務、不扣點")
    args = p.parse_args()

    key = api_key()

    me = get_json("/me", key)
    balance = get_json("/credits/balance", key)
    print("帳戶：", json.dumps(me, ensure_ascii=False))
    print("餘額：", json.dumps(balance, ensure_ascii=False))
    if args.check_only:
        print("價目：", json.dumps(get_json("/pricing", key), ensure_ascii=False))
        return

    fields = {"prompt": args.prompt}
    for name, value in (("size", args.size), ("mode", args.mode),
                        ("steps", args.steps), ("negative_prompt", args.negative)):
        if value:
            fields[name] = value
    body, ctype = multipart(fields)
    _, _, raw = request("POST", "/images/text-to-image", key, body, ctype)
    task = json.loads(raw)
    task_uuid = task["task_uuid"]
    print(f"已送出 {task_uuid}，扣 {task.get('credits_charged')} 點，"
          f"剩 {task.get('remaining_credits')} 點")

    deadline = time.time() + args.max_wait
    while True:
        info = get_json(f"/tasks/{task_uuid}", key)
        status = info.get("status")
        print("狀態：", status)
        if status in FINAL_STATES:
            break
        if time.time() > deadline:
            sys.exit(f"等候逾時，任務仍是 {status}；之後可再查 /tasks/{task_uuid}")
        time.sleep(args.interval)

    if status != "completed":
        sys.exit(f"任務結束但未成功：{status}（失敗會自動退點）")

    _, _, image = request("GET", f"/tasks/{task_uuid}/outputs/0", key)
    with open(args.out, "wb") as f:
        f.write(image)
    print(f"已存檔：{args.out}（{len(image)} bytes）")


if __name__ == "__main__":
    main()
