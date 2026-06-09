#!/usr/bin/env python3
"""Serves the web tool and saves JSON files in the questions/ directory."""

from __future__ import annotations

import json
import urllib.parse
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QUESTIONS_DIR = ROOT / "questions"


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/api/json/list":
            files = sorted(f"questions/{path.name}" for path in QUESTIONS_DIR.glob("*.json"))
            payload = json.dumps(files).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
            return
        super().do_GET()

    def do_PUT(self) -> None:
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/api/json":
            self.send_error(404)
            return

        filename = urllib.parse.parse_qs(parsed.query).get("file", [""])[0]
        if not _is_safe_json_name(filename):
            self.send_error(400, "Invalid filename")
            return

        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)

        try:
            json.loads(body)
        except json.JSONDecodeError:
            self.send_error(400, "Invalid JSON")
            return

        target = (ROOT / filename).resolve()
        if not _is_inside_root(target):
            self.send_error(403)
            return

        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(body)
        payload = b'{"ok":true}'
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)


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
    server = ThreadingHTTPServer(("127.0.0.1", 8080), Handler)
    print(f"Serving {ROOT} at http://127.0.0.1:8080/")
    print("Open http://127.0.0.1:8080/index.html")
    server.serve_forever()


if __name__ == "__main__":
    main()
