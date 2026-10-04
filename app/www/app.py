# The web server: a hand-built version of what FastAPI + uvicorn do for you.
# Every request is handled by Handler below:
#   /api/run/<file>/<func>  -> run a Python function via router.py, reply with JSON
#   anything else           -> serve a file from this folder (HTML, JS, CSS)
# The server loads all the code ONCE at startup, so edits to .py files need a
# container restart (docker restart python-app); HTML/JS/CSS are re-read per request.
import json
import mimetypes
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

import router

# The folder this file is in (www/); static files are served from here.
STATIC_DIR = Path(__file__).parent.resolve()

MAX_BODY_BYTES = 1_000_000  # 1MB cap so a bogus Content-Length can't force huge reads


# One Handler object is created per request. BaseHTTPRequestHandler calls
# do_GET / do_POST depending on the HTTP method.
class Handler(BaseHTTPRequestHandler):  # rfile and wfile come from this library
    # GET: API call with no body, or a static file.
    def do_GET(self):
        if self.path.startswith("/api/run/"):
            self.handle_run(body=None)
        else:
            self.handle_static()

    # POST: API call with a JSON body. Only /api/run/ accepts POST.
    def do_POST(self):
        if not self.path.startswith("/api/run/"):
            self.send_json(404, {"error": "not found"})
            return

        # Content-Length says how many bytes the body is; read exactly that many.
        length = int(self.headers.get("Content-Length", 0))
        if length > MAX_BODY_BYTES:
            self.send_json(413, {"error": "request body too large"})
            return
        raw = self.rfile.read(length) if length else b""
        # Decode the JSON body into Python objects (dict, list, str...).
        # FastAPI does this (and the validation) for you with a Pydantic model.
        body = None
        if raw:
            try:
                body = json.loads(raw)
            except json.JSONDecodeError:
                self.send_json(400, {"error": "invalid JSON body"})
                return

        self.handle_run(body)

    # Look the route up in router.py, run it, and send back what it returns as JSON.
    # Any exception becomes a 500 JSON error instead of crashing the server.
    def handle_run(self, body):
        name = self.path.removeprefix("/api/run/")
        try:
            payload = router.run_script(name, body)
        except Exception as e:
            self.send_json(500, {"error": str(e)})
            return
        self.send_json(200, payload)

    # Serve a file from www/, e.g. GET /index.html or /script.js.
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

        # Pick the Content-Type from the file extension (.html -> text/html, ...).
        content_type, _ = mimetypes.guess_type(str(file_path))
        data = file_path.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type", content_type or "application/octet-stream")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    # this builds the http response and sends back down the pipe created by the caller
    def send_json(self, status, payload):
        # default=str turns things JSON can't handle (dates, Decimals) into strings.
        data = json.dumps(payload, default=str).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


# Start the server. ThreadingHTTPServer handles each request in its own thread,
# so one slow request doesn't block the others.
if __name__ == "__main__":
    server = ThreadingHTTPServer(("0.0.0.0", 8080), Handler)
    print("Serving on http://0.0.0.0:8080")
    server.serve_forever()