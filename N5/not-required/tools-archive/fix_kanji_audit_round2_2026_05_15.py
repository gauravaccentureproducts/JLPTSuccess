"""Kanji audit Round 2: strip leaked HTML <u>...</u> markup from 6 sentences.

Renderer at js/kanji.js:347 wraps the sentence ja in esc() — which
HTML-escapes content. The <u>...</u> tags were authored expecting raw
HTML rendering but instead display literally as '<u>会社員</u>'. Strip
the tags to fix the display bug.
"""
from __future__ import annotations
import json
import re
from collections import OrderedDict
from pathlib import Path

KANJI = Path("data/kanji.json")
TAG_RX = re.compile(r"</?u>")


def main() -> None:
    d = json.loads(KANJI.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    fixed = 0
    for e in d["entries"]:
        for s in e.get("sentences", []) or []:
            ja = s.get("ja", "")
            if "<u>" in ja or "</u>" in ja:
                s["ja"] = TAG_RX.sub("", ja)
                fixed += 1
                print(f"  {e['glyph']}: {ja!r} -> {s['ja']!r}")
    KANJI.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nFixed: {fixed} sentences")


if __name__ == "__main__":
    main()
