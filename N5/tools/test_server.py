# -*- coding: utf-8 -*-
"""Local test server for the Playwright P0 smoke suite.

Why this exists (vs. plain `python -m http.server 8000`):

`N5/index.html` ships with `<base href="/JLPTSuccess/N5/">` since v1.17.7
so the SPA's history-mode `replaceState()` calls resolve their CSS/JS/
font/data assets against a fixed prefix on production (GitHub Pages
hosts the site at /JLPTSuccess/N5/, so the prefix matches reality and
asset paths stay valid through any deep-link redirect chain).

On the local Playwright test runner the python http.server has no
URL-prefix concept, so the browser fetches `/JLPTSuccess/N5/css/
main.min.css` → 404 → the SPA never boots → every DOM-querying test
fails on an empty page. This was the dominant cause of CI red on
playwright-p0-smoke from v1.17.7 onward.

Fix: serve from N5/ but strip the `/JLPTSuccess/N5` prefix from any
inbound request path before resolving it on disk. Now:
  - GET /index.html             → N5/index.html
  - GET /JLPTSuccess/N5/index.html → N5/index.html (same file)
  - GET /css/main.min.css       → N5/css/main.min.css
  - GET /JLPTSuccess/N5/css/main.min.css → N5/css/main.min.css (same)

Tests can use either form: `page.goto('/')` and `page.goto('/learn/
n5-098/')` keep working with baseURL `http://localhost:8000` unchanged,
and the asset fetches the SPA issues via the base href also succeed.
"""

import http.server
import os
import socketserver
import sys

PORT = 8000
PREFIX = "/JLPTSuccess/N5"  # without trailing slash


class PrefixStrippingHandler(http.server.SimpleHTTPRequestHandler):
    def translate_path(self, path):
        # Strip the production URL prefix so requests resolve against
        # the on-disk N5/ tree. Two cases:
        #   - "/JLPTSuccess/N5/foo" → "/foo"
        #   - "/JLPTSuccess/N5"     → "/"
        if path == PREFIX:
            path = "/"
        elif path.startswith(PREFIX + "/"):
            path = path[len(PREFIX):]
        return super().translate_path(path)


def main():
    # Serve from the N5/ directory regardless of where this script is run from.
    n5_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    os.chdir(n5_dir)
    with socketserver.TCPServer(("", PORT), PrefixStrippingHandler) as httpd:
        # Match what `python -m http.server` logs so the test runner
        # captures the same shape of log lines.
        httpd.serve_forever()


if __name__ == "__main__":
    main()
