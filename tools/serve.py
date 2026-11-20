#!/usr/bin/env python3
"""Local preview server for this site.

    python tools/serve.py            # http://0.0.0.0:8787
    python tools/serve.py 9000       # custom port

Differences from `python -m http.server`:

- dotfiles and dot-directories (`.git`, `.gitignore`, `.env`) return 404, so a
  preview left running on a tailnet does not expose the repository internals
- directory listings are disabled
- cache headers are off, so a refresh always shows the current file
"""

from __future__ import annotations

import functools
import http.server
import os
import socketserver
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Handler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self) -> None:  # noqa: N802
        if any(part.startswith(".") for part in self.path.split("?")[0].split("/") if part):
            self.send_error(404, "Not found")
            return
        super().do_GET()

    def do_HEAD(self) -> None:  # noqa: N802
        if any(part.startswith(".") for part in self.path.split("?")[0].split("/") if part):
            self.send_error(404, "Not found")
            return
        super().do_HEAD()

    def list_directory(self, path):  # noqa: ANN001, D401
        self.send_error(404, "No directory listing")
        return None

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store")
        super().end_headers()

    def log_message(self, fmt: str, *args) -> None:  # noqa: ANN002
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


def main() -> int:
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8787
    handler = functools.partial(Handler, directory=ROOT)
    socketserver.TCPServer.allow_reuse_address = True
    with socketserver.ThreadingTCPServer(("0.0.0.0", port), handler) as httpd:
        print(f"serving {ROOT} on http://0.0.0.0:{port}  (dotfiles blocked, no listings)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nstopped")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
