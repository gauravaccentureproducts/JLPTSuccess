"""Fetch KanjiVG stroke-order SVGs for the 106 N5 kanji.

KanjiVG (https://kanjivg.tagaini.net/, CC BY-SA 3.0) names files by zero-padded
hex codepoint (e.g., 古 / U+53E4 -> kanji/053e4.svg).

We rename to <glyph>.svg on save so `data/kanji.json#stroke_order_svg`
("svg/kanji/<glyph>.svg") resolves directly without a translation layer.

Usage: python tools/fetch_kanjivg.py
Idempotent: skips files that already exist.
"""
from __future__ import annotations

import json
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WHITELIST = ROOT / "data" / "n5_kanji_whitelist.json"
OUT_DIR = ROOT / "svg" / "kanji"

# KanjiVG raw SVGs on GitHub (master branch).
# https://github.com/KanjiVG/kanjivg/tree/master/kanji
BASE_URL = "https://raw.githubusercontent.com/KanjiVG/kanjivg/master/kanji"


def codepoint_filename(glyph: str) -> str:
    return f"{ord(glyph):05x}.svg"


def fetch_one(glyph: str, out_path: Path) -> tuple[bool, str]:
    if out_path.exists() and out_path.stat().st_size > 0:
        return True, "exists"
    url = f"{BASE_URL}/{codepoint_filename(glyph)}"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "jlpt-n5-tutor build script"})
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = resp.read()
        out_path.write_bytes(data)
        return True, f"fetched ({len(data)} bytes)"
    except Exception as exc:
        return False, f"failed: {exc}"


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    glyphs: list[str] = json.loads(WHITELIST.read_text(encoding="utf-8"))
    if len(glyphs) != 106:
        print(f"WARNING: expected 106 glyphs, found {len(glyphs)}", file=sys.stderr)

    ok = 0
    failed: list[tuple[str, str]] = []
    for i, g in enumerate(glyphs, 1):
        out_path = OUT_DIR / f"{g}.svg"
        success, msg = fetch_one(g, out_path)
        if success:
            ok += 1
            if msg != "exists":
                # Brief pause to be polite to GitHub raw.
                time.sleep(0.05)
        else:
            failed.append((g, msg))
        # Progress every 10
        if i % 10 == 0 or i == len(glyphs):
            print(f"  [{i:3d}/{len(glyphs)}] ok={ok} failed={len(failed)}", file=sys.stderr)

    print()
    print(f"DONE. {ok}/{len(glyphs)} SVGs in {OUT_DIR}")
    if failed:
        print(f"FAILED ({len(failed)}):")
        for g, msg in failed:
            print(f"  {g} (U+{ord(g):04X}): {msg}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
