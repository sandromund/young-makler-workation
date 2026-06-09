#!/usr/bin/env python3
"""Serves the web tool, saves JSON files and generates Word documents."""

from __future__ import annotations

import json
import traceback
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from generator.main import generate_documents

ROOT = Path(__file__).resolve().parent
QUESTIONS_DIR = ROOT / "questions"
OUTPUT_DIR = ROOT / "output"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/health":
            payload = json.dumps({"ok": True, "generate": True, "version": 2}).encode("utf-8")
            self._send_json(payload)
            return
        if parsed.path == "/api/json/list":
            files = sorted(f"questions/{path.name}" for path in QUESTIONS_DIR.glob("*.json"))
            payload = json.dumps(files).encode("utf-8")
            self._send_json(payload)
            return
        super().do_GET()

    def do_PUT(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/api/json":
            self._send_json_error(404, "Unknown API route")
            return

        filename = urllib.parse.parse_qs(parsed.query).get("file", [""])[0]
        body = self._read_body()
        if body is None:
            return

        if not _is_safe_json_name(filename):
            self._send_json_error(400, "Invalid filename")
            return

        try:
            json.loads(body)
        except json.JSONDecodeError:
            self._send_json_error(400, "Invalid JSON")
            return

        target = (ROOT / filename).resolve()
        if not _is_inside_root(target):
            self._send_json_error(403, "Forbidden")
            return

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
        self._send_json(b'{"ok":true}')

    def do_POST(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/api/generate":
            self._send_json_error(404, "Unknown API route")
            return

        filename = urllib.parse.parse_qs(parsed.query).get("file", [""])[0]
        if not _is_safe_json_name(filename):
            self._send_json_error(400, "Invalid filename")
            return

        target = (ROOT / filename).resolve()
        if not _is_inside_root(target):
            self._send_json_error(403, "Forbidden")
            return

        body = self._read_body(required=False)
        if body:
            try:
                json.loads(body)
            except json.JSONDecodeError:
                self._send_json_error(400, "Invalid JSON")
                return
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(body)

        if not target.exists():
            self._send_json_error(404, f"JSON-Datei nicht gefunden: {filename}")
            return

        try:
            result = generate_documents(input_path=target, create_zip=True)
            payload = json.dumps(result, ensure_ascii=False).encode("utf-8")
            self._send_json(payload)
        except Exception as error:
            traceback.print_exc()
            self._send_json_error(500, str(error))

    def _read_body(self, required: bool = True) -> bytes | None:
        length = int(self.headers.get("Content-Length", 0))
        if length == 0:
            if required:
                self._send_json_error(400, "Missing request body")
                return None
            return b""
        return self.rfile.read(length)

    def _send_json(self, payload: bytes, status: int = 200) -> None:
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def _send_json_error(self, status: int, message: str) -> None:
        payload = json.dumps({"ok": False, "error": message}, ensure_ascii=False).encode("utf-8")
        self._send_json(payload, status=status)


def _is_safe_json_name(filename: str) -> bool:
    if not filename or not filename.endswith(".json"):
        return False
    if ".." in filename or filename.startswith(("/", "\\")) or "\\" in filename:
        return False

    parts = Path(filename).parts
    return len(parts) == 2 and parts[0] == "questions" and parts[1].endswith(".json")


def _is_inside_root(path: Path) -> bool:
    try:
        path.relative_to(ROOT.resolve())
    except ValueError:
        return False
    return True


def main() -> None:
    QUESTIONS_DIR.mkdir(exist_ok=True)
    OUTPUT_DIR.mkdir(exist_ok=True)

    class ReusableThreadingHTTPServer(ThreadingHTTPServer):
        allow_reuse_address = True

    server = ReusableThreadingHTTPServer(("127.0.0.1", 8080), Handler)
    print(f"Serving {ROOT} at http://127.0.0.1:8080/")
    print("Open http://127.0.0.1:8080/index.html")
    print("API: GET /api/health, POST /api/generate")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer beendet.")


if __name__ == "__main__":
    main()
