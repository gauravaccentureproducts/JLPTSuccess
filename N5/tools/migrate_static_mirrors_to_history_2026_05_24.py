"""Migrate grammar static mirrors from learn/grammar/n5-XXX/ to
learn/n5-XXX/ AND transform them to boot the SPA in place (instead of
JS-redirecting to the hash URL after 1.5s).

After migration each mirror:
- Lives at learn/<pid>/index.html (clean URL = SPA URL = same URL)
- Has updated canonical / og:url to the clean path
- Has the pattern content wrapped in <main id="app">
- Loads ../../js/min/app.js, which boots the SPA and replaces #app
  with the route-rendered interactive version
- No longer carries the setTimeout(goToSPA, 1500) redirect script

Also:
- Updates learn/grammar/index.html listing to link to ../<pid>/
- Updates sitemap.xml entries
- Leaves learn/grammar/index.html in place (still the listing page)

Backup: each old mirror folder is left in place until verified, then
deleted in a second pass. Re-running is idempotent (skip mirrors that
already exist at new path).

Run from N5/:
  python tools/migrate_static_mirrors_to_history_2026_05_24.py
  python tools/migrate_static_mirrors_to_history_2026_05_24.py --delete-old
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_DIR_OLD = ROOT / "learn" / "grammar"
LEARN_DIR = ROOT / "learn"
SITEMAP = ROOT / "sitemap.xml"

N5_BASE = "https://gauravaccentureproducts.github.io/JLPTSuccess/N5/"
SPA_SCRIPT_TAG = '<script type="module" src="../../js/min/app.js?v=1.16.9"></script>'

# Regex patterns used to transform each mirror
RE_REDIRECT_SCRIPT = re.compile(
    r"<script>\s*\(function\(\)\{\s*var goToSPA[^<]*</script>",
    re.DOTALL,
)
RE_CANONICAL = re.compile(r'<link rel="canonical" href="[^"]*">')
RE_OG_URL = re.compile(r'<meta property="og:url" content="[^"]*">')
RE_BODY = re.compile(r"<body>(.*?)</body>", re.DOTALL)
RE_META_BANNER = re.compile(
    r'<p class="meta-banner">.*?</p>',
    re.DOTALL,
)
# Footer breadcrumb references the old grammar/ index path
RE_OLD_BREADCRUMB = re.compile(r'<a href="\.\./index\.html">Grammar</a>')


def transform_mirror(html_text: str, pid: str) -> str:
    """Transform an old-format mirror into a history-mode mirror."""
    clean_url = f"{N5_BASE}learn/{pid}/"

    # 1) Replace canonical and og:url
    html_text = RE_CANONICAL.sub(
        f'<link rel="canonical" href="{clean_url}">',
        html_text,
        count=1,
    )
    html_text = RE_OG_URL.sub(
        f'<meta property="og:url" content="{clean_url}">',
        html_text,
        count=1,
    )

    # 2) Remove the goToSPA setTimeout redirect script
    html_text = RE_REDIRECT_SCRIPT.sub("", html_text)

    # 3) Replace the meta-banner ("Static read-only mirror" paragraph)
    #    with a small back-link bar (kept for non-JS users)
    html_text = RE_META_BANNER.sub(
        '<p class="meta-banner"><a href="../">&larr; All N5 grammar patterns</a></p>',
        html_text,
        count=1,
    )

    # 4) Update breadcrumb (old: ../index.html for Grammar listing,
    #    new: ../ since we're one level shallower)
    html_text = RE_OLD_BREADCRUMB.sub(
        '<a href="../">Grammar</a>',
        html_text,
    )

    # 5) Wrap the body content in <main id="app">...</main>
    #    so the SPA's route handler can find a container to render into.
    def wrap_body(m):
        inner = m.group(1)
        # Don't double-wrap if already has #app
        if 'id="app"' in inner:
            return m.group(0)
        return f'<body><main id="app">{inner}</main>\n{SPA_SCRIPT_TAG}\n</body>'

    html_text = RE_BODY.sub(wrap_body, html_text, count=1)

    return html_text


def write_new_mirror(pid: str, new_html: str) -> tuple[bool, Path]:
    new_path = LEARN_DIR / pid / "index.html"
    new_path.parent.mkdir(parents=True, exist_ok=True)
    if new_path.exists() and new_path.read_text(encoding="utf-8") == new_html:
        return False, new_path
    new_path.write_text(new_html, encoding="utf-8")
    return True, new_path


def find_old_mirrors() -> list[tuple[str, Path]]:
    """List (pid, old_index_html_path) for every old-format grammar mirror."""
    out = []
    if not GRAMMAR_DIR_OLD.exists():
        return out
    for child in GRAMMAR_DIR_OLD.iterdir():
        if not child.is_dir():
            continue
        if not child.name.startswith("n5-"):
            continue
        idx = child / "index.html"
        if idx.exists():
            out.append((child.name, idx))
    return out


def update_sitemap():
    if not SITEMAP.exists():
        return 0
    text = SITEMAP.read_text(encoding="utf-8")
    # Old: <loc>...learn/grammar/n5-001/</loc>
    # New: <loc>...learn/n5-001/</loc>
    text_new, n = re.subn(r"learn/grammar/(n5-\d+)/", r"learn/\1/", text)
    if n and text_new != text:
        SITEMAP.write_text(text_new, encoding="utf-8")
    return n


def update_grammar_index_listing():
    """The listing at learn/grammar/index.html links to <pid>/ relative
    paths that used to be siblings. After the move, patterns are at ../<pid>/
    instead. Rewrite all those links.
    """
    idx_path = GRAMMAR_DIR_OLD / "index.html"
    if not idx_path.exists():
        return 0
    text = idx_path.read_text(encoding="utf-8")
    # <a class="index-card" href="n5-001/">  ->  href="../n5-001/"
    text_new, n = re.subn(r'href="(n5-\d+)/"', r'href="../\1/"', text)
    if n and text_new != text:
        idx_path.write_text(text_new, encoding="utf-8")
    return n


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--delete-old", action="store_true",
                    help="After successful migration, delete the old learn/grammar/n5-XXX/ folders.")
    args = ap.parse_args()

    mirrors = find_old_mirrors()
    print(f"Found {len(mirrors)} old-format grammar mirrors at learn/grammar/n5-*/")

    written = 0
    unchanged = 0
    for pid, old_idx in mirrors:
        old_html = old_idx.read_text(encoding="utf-8")
        new_html = transform_mirror(old_html, pid)
        was_written, new_path = write_new_mirror(pid, new_html)
        if was_written:
            written += 1
        else:
            unchanged += 1

    print(f"Wrote {written} new mirrors; {unchanged} were already up to date")

    sm_count = update_sitemap()
    print(f"Sitemap.xml: {sm_count} URL(s) rewritten")

    idx_count = update_grammar_index_listing()
    print(f"learn/grammar/index.html listing: {idx_count} href(s) rewritten")

    if args.delete_old:
        # Verify every new mirror exists before deleting the old.
        all_ok = True
        for pid, _ in mirrors:
            new_path = LEARN_DIR / pid / "index.html"
            if not new_path.exists():
                print(f"  SAFETY: skip delete - new mirror missing for {pid}")
                all_ok = False
                break
        if all_ok:
            for pid, old_idx in mirrors:
                shutil.rmtree(old_idx.parent)
            print(f"Deleted {len(mirrors)} old learn/grammar/n5-*/ folders")
        else:
            print("Refusing to delete old folders - safety check failed.")
    else:
        print("Old folders kept (re-run with --delete-old to remove)")


if __name__ == "__main__":
    main()
