#!/usr/bin/env python3
"""Tiny static file server for the OH AUDIO landing page with live reload."""

from __future__ import annotations

import argparse
import json
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Iterable

WATCHED_SUFFIXES = {
    ".html",
    ".css",
    ".js",
    ".svg",
    ".jpg",
    ".jpeg",
    ".png",
    ".json",
}


def latest_mtime(directory: Path) -> float:
    newest = 0.0
    for path in iter_files(directory):
        try:
            mtime = path.stat().st_mtime
        except OSError:
            continue
        if mtime > newest:
            newest = mtime
    return newest or time.time()


def iter_files(directory: Path) -> Iterable[Path]:
    for path in directory.rglob("*"):
        if path.is_file() and path.suffix.lower() in WATCHED_SUFFIXES:
            yield path


def create_handler(directory: Path):
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, directory=str(directory), **kwargs)

        def do_GET(self):  # noqa: N802 - keeping SimpleHTTPRequestHandler signature
            if self.path == "/__livereload":
                payload = json.dumps(
                    {"token": str(latest_mtime(directory))}
                ).encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Cache-Control", "no-store")
                self.send_header("Content-Length", str(len(payload)))
                self.end_headers()
                self.wfile.write(payload)
                return

            return super().do_GET()

    return Handler


def main():
    parser = argparse.ArgumentParser(
        description="Serve the OH AUDIO site over HTTP."
    )
    parser.add_argument(
        "--port",
        "-p",
        type=int,
        default=8000,
        help="Port to listen on (default: 8000)",
    )
    parser.add_argument(
        "--host",
        "-H",
        default="127.0.0.1",
        help="Host/interface to bind (default: 127.0.0.1)",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    handler = create_handler(root)

    with ThreadingHTTPServer((args.host, args.port), handler) as httpd:
        host_label = "localhost" if args.host == "127.0.0.1" else args.host
        print(f"Serving OH AUDIO at http://{host_label}:{args.port}")
        print("Live reload polling available at /__livereload")
        print("Press Ctrl+C to stop.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer stopped.")


if __name__ == "__main__":
    main()
