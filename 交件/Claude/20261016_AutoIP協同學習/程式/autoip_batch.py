#!/usr/bin/env python3
"""AutoIP 批次生圖：一個 JSON 檔列多個任務，依序送出（帳號同時只能 1 個任務）。

金鑰只讀環境變數 AUTOIP_API_KEY。規格見同資料夾 autoip_openapi_20261016.yaml。
每個任務的提示詞、參數、扣點、任務編號寫進輸出資料夾的 log.jsonl，方便回查。

任務檔格式（list）：
  [{"name": "e1_amber", "type": "t2i", "prompt": "...", "negative": "...",
    "size": "1024x768", "mode": "standard", "steps": 30},
   {"name": "e3_card", "type": "i2i", "image": "路徑.png", "prompt": "...",
    "strength": 0.4, "size": "original"}]

用法：python3 autoip_batch.py 任務.json 輸出資料夾 [--only name1,name2]
"""

import argparse
import json
import mimetypes
import os
import sys
import time
import urllib.error
import urllib.request
import uuid

BASE = os.environ.get("AUTOIP_BASE_URL", "https://autoip.app").rstrip("/") + "/api/v1"
FINAL = {"completed", "failed", "timeout", "cancelled"}


def key():
    k = os.environ.get("AUTOIP_API_KEY", "").strip()
    if not k.startswith("aip_"):
        sys.exit("沒有設定 AUTOIP_API_KEY（aip_ 開頭）")
    return k


def call(method, path, body=None, ctype=None, tries=4):
    for i in range(tries):
        req = urllib.request.Request(BASE + path, data=body, method=method)
        req.add_header("Authorization", "Bearer " + key())
        # Cloudflare 擋 Python 預設 User-Agent（403 code 1010）
        req.add_header("User-Agent", "curl/8.5.0")
        if ctype:
            req.add_header("Content-Type", ctype)
        try:
            with urllib.request.urlopen(req, timeout=180) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            raw = e.read()[:400].decode("utf-8", "replace")
            if e.code == 429 and i < tries - 1:
                time.sleep(float(e.headers.get("Retry-After") or 15))
                continue
            raise RuntimeError(f"HTTP {e.code} {method} {path}: {raw}")
        except urllib.error.URLError as e:
            if i < tries - 1:
                time.sleep(2 ** (i + 1))
                continue
            raise RuntimeError(f"連不到 AutoIP：{e.reason}")


def multipart(fields, files):
    b = "----autoip" + uuid.uuid4().hex
    out = bytearray()
    for k, v in fields.items():
        out += (f'--{b}\r\nContent-Disposition: form-data; name="{k}"\r\n\r\n{v}\r\n').encode()
    for k, path in files.items():
        ct = mimetypes.guess_type(path)[0] or "application/octet-stream"
        out += (f'--{b}\r\nContent-Disposition: form-data; name="{k}"; '
                f'filename="{os.path.basename(path)}"\r\nContent-Type: {ct}\r\n\r\n').encode()
        out += open(path, "rb").read() + b"\r\n"
    out += f"--{b}--\r\n".encode()
    return bytes(out), "multipart/form-data; boundary=" + b


def run(task, outdir):
    t = task.get("type", "t2i")
    fields = {"prompt": task["prompt"]}
    for src, dst in (("negative", "negative_prompt"), ("size", "size"), ("mode", "mode"),
                     ("steps", "steps"), ("strength", "strength")):
        if task.get(src) is not None:
            fields[dst] = task[src]
    files = {"image": task["image"]} if t == "i2i" else {}
    path = "/images/image-to-image" if t == "i2i" else "/images/text-to-image"
    body, ct = multipart(fields, files)
    created = json.loads(call("POST", path, body, ct))
    uid = created["task_uuid"]
    t0 = time.time()
    while True:
        info = json.loads(call("GET", f"/tasks/{uid}"))
        if info["status"] in FINAL:
            break
        if time.time() - t0 > 900:
            break
        time.sleep(6)
    rec = {"name": task["name"], "type": t, "task_uuid": uid, "status": info["status"],
           "credits": created.get("credits_charged"), "refunded": info.get("credits_refunded"),
           "seconds": round(time.time() - t0), "params": {k: v for k, v in task.items() if k != "name"}}
    if info["status"] == "completed":
        n = 0
        for o in info.get("outputs", []):
            ext = os.path.splitext(o.get("filename", ""))[1] or ".png"
            fn = os.path.join(outdir, f"{task['name']}" + (f"_{n}" if n else "") + ext)
            open(fn, "wb").write(call("GET", f"/tasks/{uid}/outputs/{o['index']}"))
            rec.setdefault("files", []).append(os.path.basename(fn))
            n += 1
    else:
        rec["error"] = info.get("error_message")
    with open(os.path.join(outdir, "log.jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print(task["name"], rec["status"], rec.get("credits"), "點", rec["seconds"], "秒", flush=True)


def main():
    p = argparse.ArgumentParser()
    p.add_argument("tasks")
    p.add_argument("outdir")
    p.add_argument("--only")
    a = p.parse_args()
    tasks = json.load(open(a.tasks, encoding="utf-8"))
    if a.only:
        keep = set(a.only.split(","))
        tasks = [t for t in tasks if t["name"] in keep]
    os.makedirs(a.outdir, exist_ok=True)
    for t in tasks:
        try:
            run(t, a.outdir)
        except Exception as e:  # 單一任務失敗不中斷整批
            print(t["name"], "錯誤", e, flush=True)
    bal = json.loads(call("GET", "/credits/balance"))
    print("餘額", bal.get("available_credits"))


if __name__ == "__main__":
    main()
