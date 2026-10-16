"""本機 HTTP 模擬驗證，不連 AutoIP、不使用真實金鑰、不建立計費任務。"""

import base64
from contextlib import redirect_stderr, redirect_stdout
from email.parser import BytesParser
from email.policy import default
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from io import StringIO
import json
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch

import autoip_api_example as api


SPEC = b"openapi: 3.0.3\ninfo:\n  title: Mock AutoIP\n  version: test\npaths: {}\n"
PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aK1sAAAAASUVORK5CYII="
)
TASK = "00000000-0000-4000-8000-000000000001"
TEST_KEY = "local-test-key-not-a-credential"


class AutoIPFlowTests(unittest.TestCase):
    def setUp(self):
        self.calls = []
        self.statuses = ["pending", "processing", "completed"]
        self.create_code = 200
        self.redirect_spec = False
        self.bad_spec = False
        self.bad_download = False
        self.short_download = False
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.output = Path(self.temp.name) / "output.png"
        test = self

        class Handler(BaseHTTPRequestHandler):
            def log_message(self, *args):
                pass

            def do_GET(self):
                self.handle_request()

            def do_POST(self):
                self.handle_request()

            def handle_request(self):
                body = self.rfile.read(int(self.headers.get("Content-Length", 0)))
                test.calls.append((self.command, self.path, dict(self.headers), body))
                code, media_type = 200, "application/json"
                if self.path.endswith("/openapi.yaml"):
                    if test.redirect_spec:
                        self.send_response(302)
                        self.send_header("Location", "/redirect-must-not-be-followed")
                        self.end_headers()
                        return
                    payload = b"<html>proxy error</html>" if test.bad_spec else SPEC
                    media_type = "text/yaml"
                elif self.command == "POST":
                    code = test.create_code
                    payload = json.dumps({"task_uuid": TASK} if code == 200 else {"error": TEST_KEY}).encode()
                elif self.path.endswith("/outputs/0"):
                    media_type = "application/json" if test.bad_download else "image/png"
                    payload = b'{"error":"not an image"}' if test.bad_download else PNG
                else:
                    status = test.statuses.pop(0) if len(test.statuses) > 1 else test.statuses[0]
                    payload = json.dumps({"status": status}).encode()
                self.send_response(code)
                self.send_header("Content-Type", media_type)
                extra = 10 if test.short_download and self.path.endswith("/outputs/0") else 0
                self.send_header("Content-Length", str(len(payload) + extra))
                self.end_headers()
                self.wfile.write(payload)

        self.server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        thread = threading.Thread(target=self.server.serve_forever, daemon=True)
        thread.start()
        self.addCleanup(self.server.server_close)
        self.addCleanup(self.server.shutdown)
        self.client = api.AutoIP(TEST_KEY, f"http://127.0.0.1:{self.server.server_port}/api/v1")

    def run_cli(self, *arguments):
        out, err = StringIO(), StringIO()
        with patch.object(api, "AutoIP", return_value=self.client), patch.dict(
            "os.environ", {"AUTOIP_API_KEY": TEST_KEY}
        ), redirect_stdout(out), redirect_stderr(err):
            result = api.main([
                "--output", str(self.output), "--interval", "0.001", *arguments,
            ])
        return result, out.getvalue(), err.getvalue()

    def test_full_flow_auth_multipart_poll_and_binary_output(self):
        spec_path = Path(self.temp.name) / "openapi.yaml"
        result, out, err = self.run_cli("--prompt", "崧淳環保工程車", "--spec-output", str(spec_path))
        self.assertEqual(result, 0, err)
        self.assertEqual(self.output.read_bytes(), PNG)
        self.assertEqual(spec_path.read_bytes(), SPEC)
        self.assertEqual([m for m, _, _, _ in self.calls], ["GET", "POST", "GET", "GET", "GET", "GET"])
        self.assertEqual(self.calls[0][1], "/api/v1/openapi.yaml")
        self.assertEqual(self.calls[1][1], "/api/v1/images/text-to-image")
        self.assertEqual(self.calls[-1][1], f"/api/v1/tasks/{TASK}/outputs/0")
        for _, _, headers, _ in self.calls:
            self.assertEqual(headers["Authorization"], "Bearer " + TEST_KEY)
        _, _, headers, body = self.calls[1]
        message = BytesParser(policy=default).parsebytes(
            ("Content-Type: " + headers["Content-Type"] + "\r\n\r\n").encode() + body
        )
        parts = list(message.iter_parts())
        self.assertEqual(len(parts), 1)
        self.assertEqual(parts[0].get_param("name", header="Content-Disposition"), "prompt")
        self.assertEqual(parts[0].get_payload(decode=True).decode(), "崧淳環保工程車")
        self.assertNotIn(TEST_KEY, out + err)

    def test_invalid_spec_stops_before_billable_post(self):
        self.bad_spec = True
        result, _, _ = self.run_cli("--prompt", "example")
        self.assertEqual(result, 1)
        self.assertEqual(len(self.calls), 1)

    def test_create_error_is_redacted_and_not_retried(self):
        self.create_code = 401
        result, out, err = self.run_cli("--prompt", "example")
        self.assertEqual(result, 1)
        self.assertEqual(sum(m == "POST" for m, *_ in self.calls), 1)
        self.assertNotIn(TEST_KEY, out + err)
        self.assertIn("[REDACTED]", err)

    def test_failed_task_never_downloads(self):
        self.statuses = ["failed"]
        result, _, err = self.run_cli("--prompt", "example")
        self.assertEqual(result, 1)
        self.assertIn("failed", err)
        self.assertFalse(self.output.exists())
        self.assertFalse(any("/outputs/" in path for _, path, *_ in self.calls))

    def test_resume_downloads_without_creating_another_task(self):
        self.statuses = ["completed"]
        result, _, err = self.run_cli("--task-uuid", TASK)
        self.assertEqual(result, 0, err)
        self.assertFalse(any(method == "POST" for method, *_ in self.calls))
        self.assertEqual(self.output.read_bytes(), PNG)

    def test_poll_timeout_preserves_id_without_post_or_output(self):
        self.statuses = ["processing"]
        result, _, err = self.run_cli("--task-uuid", TASK, "--timeout", "0.01")
        self.assertEqual(result, 1)
        self.assertIn(TASK, err)
        self.assertFalse(self.output.exists())
        self.assertFalse(any(method == "POST" for method, *_ in self.calls))

    def test_redirect_is_not_followed_with_bearer_key(self):
        self.redirect_spec = True
        result, _, _ = self.run_cli("--fetch-spec-only")
        self.assertEqual(result, 1)
        self.assertEqual(len(self.calls), 1)

    def test_json_download_is_not_saved_as_an_image(self):
        self.statuses = ["completed"]
        self.bad_download = True
        result, _, _ = self.run_cli("--task-uuid", TASK)
        self.assertEqual(result, 1)
        self.assertFalse(self.output.exists())

    def test_truncated_image_does_not_leave_partial_output(self):
        self.statuses = ["completed"]
        self.short_download = True
        result, _, _ = self.run_cli("--task-uuid", TASK)
        self.assertEqual(result, 1)
        self.assertFalse(self.output.exists())

    def test_existing_output_stops_before_network(self):
        self.output.write_bytes(b"keep original")
        with self.assertRaises(SystemExit), redirect_stderr(StringIO()):
            self.run_cli("--prompt", "example")
        self.assertEqual(self.output.read_bytes(), b"keep original")
        self.assertEqual(self.calls, [])


if __name__ == "__main__":
    unittest.main()
