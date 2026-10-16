#!/usr/bin/env python3
"""AutoIP 文生圖範例；Python 3.10+，僅使用標準函式庫。

介面依使用者指定及 @autoip/mcp 0.7.0 核對；即時 OpenAPI 尚待可連線環境驗證。
"""

import argparse
import getpass
from http.client import HTTPException
import json
import math
import os
from pathlib import Path
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid


BASE_URL = "https://autoip.app/api/v1"


class AutoIPError(Exception):
    """可直接向使用者呈現的 API／流程錯誤。"""


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        # 不將 Bearer 金鑰轉送至重新導向的其他位址。
        return None


class AutoIP:
    def __init__(self, api_key, base_url=BASE_URL, request_timeout=30):
        self.api_key = api_key
        self.base_url = base_url.rstrip("/")
        self.request_timeout = request_timeout
        # 保留系統的 HTTP(S)_PROXY 與 TLS 驗證設定。
        self.opener = urllib.request.build_opener(NoRedirect())

    def request(self, path, *, data=None, content_type=None, timeout=None):
        headers = {"Authorization": "Bearer " + self.api_key}
        if content_type:
            headers["Content-Type"] = content_type
        request = urllib.request.Request(
            self.base_url + path, data=data, headers=headers,
            method="POST" if data is not None else "GET",
        )
        try:
            return self.opener.open(
                request, timeout=self.request_timeout if timeout is None else timeout
            )
        except urllib.error.HTTPError as error:
            detail = error.read(2048).decode("utf-8", errors="replace")
            detail = detail.replace(self.api_key, "[REDACTED]")
            raise AutoIPError(f"{request.method} {path}: HTTP {error.code} {detail}") from None
        except (urllib.error.URLError, TimeoutError, socket.timeout) as error:
            detail = str(error).replace(self.api_key, "[REDACTED]")
            raise AutoIPError(f"{request.method} {path}: 連線失敗：{detail}") from None

    def json_request(self, path, **kwargs):
        with self.request(path, **kwargs) as response:
            try:
                value = json.load(response)
            except (ValueError, UnicodeError):
                raise AutoIPError(f"{path}: 回應不是有效的 JSON") from None
        if not isinstance(value, dict):
            raise AutoIPError(f"{path}: 預期 JSON 物件")
        return value

    def fetch_spec(self, save_path=None):
        with self.request("/openapi.yaml") as response:
            raw = response.read()
        # 不把 HTTP 200 的 HTML 錯誤頁誤認成規格；此檢查不是 schema 驗證。
        if not re.search(rb'(?m)^\s*[\x22\x27]?openapi[\x22\x27]?\s*:', raw.lstrip(b"\xef\xbb\xbf{")):
            raise AutoIPError("/openapi.yaml: 找不到 OpenAPI 版本宣告，停止建立任務")
        if save_path:
            try:
                with Path(save_path).open("xb") as target:
                    target.write(raw)
            except FileExistsError:
                self._exists(save_path)
        return raw

    @staticmethod
    def _exists(path):
        raise AutoIPError(f"檔案已存在，不覆寫：{path}")

    def create_image(self, prompt):
        boundary = "autoip-" + uuid.uuid4().hex
        data = (
            f'--{boundary}\r\nContent-Disposition: form-data; name="prompt"\r\n'
            f"\r\n{prompt}\r\n--{boundary}--\r\n"
        ).encode("utf-8")
        # POST 不自動重試；連線逾時可能代表伺服器已接受任務並扣點。
        result = self.json_request(
            "/images/text-to-image", data=data,
            content_type="multipart/form-data; boundary=" + boundary,
        )
        task_uuid = result.get("task_uuid")
        if not isinstance(task_uuid, str) or not task_uuid.strip():
            raise AutoIPError("建立任務後未取得 task_uuid；不要直接重送，先查 AutoIP 任務列表")
        return task_uuid

    def wait_for_task(self, task_uuid, *, timeout=900, interval=5):
        path = "/tasks/" + urllib.parse.quote(task_uuid, safe="")
        deadline = time.monotonic() + timeout
        while True:
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                raise AutoIPError(f"等待逾時；保留 task_uuid={task_uuid}，稍後以 --task-uuid 接續")
            result = self.json_request(path, timeout=min(self.request_timeout, remaining))
            status = result.get("status")
            if not isinstance(status, str) or not status:
                raise AutoIPError(f"任務 {task_uuid} 回應缺少有效的 status")
            if status == "completed":
                return result
            if status in {"failed", "cancelled", "timeout"}:
                raise AutoIPError(f"任務 {task_uuid} 結束：{status}")
            print(f"任務狀態：{status}", file=sys.stderr)
            time.sleep(min(interval, max(0, deadline - time.monotonic())))

    def download(self, task_uuid, output):
        path = "/tasks/" + urllib.parse.quote(task_uuid, safe="") + "/outputs/0"
        with self.request(path) as response:
            media_type = response.headers.get_content_type()
            if not (media_type.startswith("image/") or media_type == "application/octet-stream"):
                raise AutoIPError(f"下載回應不是圖片：{media_type}")
            total = 0
            created = False
            try:
                with Path(output).open("xb") as target:
                    created = True
                    while chunk := response.read(64 * 1024):
                        target.write(chunk)
                        total += len(chunk)
                    expected = response.headers.get("Content-Length")
                    if not total or (expected is not None and total != int(expected)):
                        raise AutoIPError("圖片下載不完整")
            except FileExistsError:
                self._exists(output)
            except BaseException:
                if created:
                    Path(output).unlink(missing_ok=True)
                raise
        return total


def positive_number(value):
    number = float(value)
    if not math.isfinite(number) or number <= 0:
        raise argparse.ArgumentTypeError("必須是大於 0 的有限數值")
    return number


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--prompt", help="建立文生圖任務，送出即會扣點")
    source.add_argument("--task-uuid", help="接續既有任務，不重新建立")
    source.add_argument("--fetch-spec-only", action="store_true", help="只取得規格，不建立任務")
    parser.add_argument("--output", type=Path, default=Path("autoip-output.png"))
    parser.add_argument("--spec-output", type=Path, help="另存完整 OpenAPI 原始內容，不覆寫既有檔案")
    parser.add_argument("--timeout", type=positive_number, default=900, help="輪詢等待上限（秒）")
    parser.add_argument("--interval", type=positive_number, default=5, help="輪詢間隔（秒）")
    args = parser.parse_args(argv)
    if args.prompt is not None and not args.prompt.strip():
        parser.error("prompt 不可空白")
    if args.task_uuid is not None and not args.task_uuid.strip():
        parser.error("task_uuid 不可空白")
    if not args.fetch_spec_only and args.output.exists():
        parser.error(f"輸出檔已存在，請換一個 --output：{args.output}")
    api_key = os.environ.get("AUTOIP_API_KEY") or getpass.getpass("AutoIP API key（輸入隱藏）: ")
    if not api_key.strip():
        parser.error("請設定 AUTOIP_API_KEY，或在隱藏輸入提示中提供金鑰")
    client = AutoIP(api_key)
    try:
        spec = client.fetch_spec(args.spec_output)
        print(f"已取得 OpenAPI 規格：{len(spec)} bytes")
        if args.fetch_spec_only:
            return 0
        task_uuid = args.task_uuid or client.create_image(args.prompt)
        print(f"task_uuid={task_uuid}", flush=True)
        client.wait_for_task(task_uuid, timeout=args.timeout, interval=args.interval)
        size = client.download(task_uuid, args.output)
        print(f"已儲存：{args.output.resolve()}（{size} bytes）")
        return 0
    except (AutoIPError, OSError, ValueError, HTTPException) as error:
        print(f"錯誤：{str(error).replace(api_key, '[REDACTED]')}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
