"""Fix BUG-020 — propagate the BUG-017 fix to kanji.json by removing
the two compounds that contain non-N5-whitelist kanji (末 in 週末, 籍 in
国籍).

Per the bug description's option (c) (the cleanest pedagogical fix):
remove the OOS-kanji compounds entirely. The kanji 末 and 籍 are N4
territory and the compounds 週末 / 国籍 may not belong in the N5 corpus
regardless of which form (kanji vs kana) is displayed.

Affected entries:
  週 (n5.kanji.週): drop n5_compounds[?]=週末 and examples[?]=週末
  国 (n5.kanji.国): drop n5_compounds[?]=国籍 and examples[?]=国籍

These compounds reference vocab entries that already exist with
kana forms (しゅうまつ, こくせき) from the BUG-017 fix. Removing
them from kanji.json does NOT delete the vocab entries — those
remain reachable from the SPA's vocab list and search.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
KANJI = ROOT / "data" / "kanji.json"

# (kanji_glyph, compound_form_to_remove)
# 週末 / 国籍 were the cases called out in BUG-020. JA-100 surfaced
# one additional case of the same class during close-out validation:
# 手紙 in 手's compounds (紙 is not in N5 whitelist). Same fix shape.
REMOVALS = [
    ("週", "週末"),
    ("国", "国籍"),
    ("手", "手紙"),
]


def main() -> int:
    K = json.loads(KANJI.read_text(encoding="utf-8"))
    entries = K.get("entries", [])

    removed = 0
    for glyph, drop_form in REMOVALS:
        entry = next((e for e in entries if e.get("glyph") == glyph), None)
        if not entry:
            print(f"  ERROR: kanji {glyph} not found")
            return 1

        # Remove from n5_compounds
        new_compounds = [
            c for c in (entry.get("n5_compounds") or [])
            if not (isinstance(c, dict) and c.get("form") == drop_form)
        ]
        old_len = len(entry.get("n5_compounds") or [])
        if len(new_compounds) < old_len:
            entry["n5_compounds"] = new_compounds
            removed += 1
            print(f"  {glyph}: removed n5_compounds entry form={drop_form!r}")

        # Remove from examples (auto-derived or otherwise that match the form/lemma)
        new_examples = [
            ex for ex in (entry.get("examples") or [])
            if not (
                isinstance(ex, dict)
                and (ex.get("form") == drop_form or ex.get("lemma") == drop_form)
            )
        ]
        old_len = len(entry.get("examples") or [])
        if len(new_examples) < old_len:
            entry["examples"] = new_examples
            removed += 1
            print(f"  {glyph}: removed examples entry form/lemma={drop_form!r}")

    KANJI.write_text(json.dumps(K, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nTotal removals: {removed}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
