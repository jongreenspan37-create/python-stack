import json
import mimetypes
import threading
import time
from collections import defaultdict, deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import router

STATIC_DIR = Path(__file__).parent.resolve()

RATE_LIMIT_WINDOW_SECONDS = 10
RATE_LIMIT_MAX_REQUESTS = 20
MAX_BODY_BYTES = 1_000_000  # 1MB cap so a bogus Content-Length can't force huge reads


class RateLimiter:
    """Fixed-size sliding window limiter, keyed by client IP."""

    def __init__(self, max_requests, window_seconds):
        self.max_requests = max_requests
        self.window_seconds = window_seconds
        self._hits = defaultdict(deque)
        self._lock = threading.Lock()

    def allow(self, key):
        now = time.monotonic()
        with self._lock:
            hits = self._hits[key]
            while hits and now - hits[0] > self.window_seconds:
                hits.popleft()
            if len(hits) >= self.max_requests:
                return False
            hits.append(now)
            return True


rate_limiter = RateLimiter(RATE_LIMIT_MAX_REQUESTS, RATE_LIMIT_WINDOW_SECONDS)


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith("/api/run/"):
            if not self.check_rate_limit():
                return
            self.handle_run(body=None)
        else:
            self.handle_static()

    def do_POST(self):
        if not self.path.startswith("/api/run/"):
            self.send_json(404, {"error": "not found"})
            return

        if not self.check_rate_limit():
            return

        length = int(self.headers.get("Content-Length", 0))
        if length > MAX_BODY_BYTES:
            self.send_json(413, {"error": "request body too large"})
            return
        raw = self.rfile.read(length) if length else b""
        body = None
        if raw:
            try:
                body = json.loads(raw)
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid JSON body"})
                return

        self.handle_run(body)

    def check_rate_limit(self):
        client_ip = self.client_address[0]
        if rate_limiter.allow(client_ip):
            return True
        self.send_response(429)
        self.send_header("Retry-After", str(RATE_LIMIT_WINDOW_SECONDS))
        body = json.dumps({"error": "too many requests, slow down"}).encode()
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
        return False

    def handle_run(self, body):
        name = self.path.removeprefix("/api/run/")
        try:
            payload = router.run_script(name, body)
        except Exception as e:
            self.send_json(500, {"error": str(e)})
            return
        self.send_json(200, payload)

    def handle_static(self):
        path = self.path.lstrip("/") or "index.html"
        file_path = (STATIC_DIR / path).resolve()

        # Guard against path traversal (e.g. GET /../app.py)
        if STATIC_DIR not in file_path.parents and file_path != STATIC_DIR:
            self.send_error(403, "Forbidden")
            return

        if not file_path.is_file():
            self.send_error(404, "Not Found")
            return

        content_type, _ = mimetypes.guess_type(str(file_path))
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, status, payload):
        data = json.dumps(payload).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8080), Handler)
    print("Serving on http://0.0.0.0:8080")
    server.serve_forever()
