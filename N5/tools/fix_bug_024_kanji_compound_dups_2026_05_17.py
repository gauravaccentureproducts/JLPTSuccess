"""Fix BUG-024 — duplicate compound entries within kanji.json's
n5_compounds. Mirror of the VOCAB-005 / VOCAB-006 dedup pattern,
applied to the kanji corpus.

Same shape: same (form, reading) tuple listed twice in the same
kanji entry, with one gloss being a strict subset of the other (or,
in one case, two distinct senses sharing the same reading that
should be merged).

Migrations:

Drop subset-gloss duplicate (form + reading + gloss-subset):
  月 entry n5_compounds: drop "moon" (subset of "month, moon")
  前 entry n5_compounds: drop "front" (subset of "before, in front")
  気 entry n5_compounds: drop 電気 "light" (subset of 電気 "electricity, light")
  電 entry n5_compounds: drop 電気 "light" (subset of 電気 "electricity, light")
  道 entry n5_compounds: drop "road" (subset of "road, way")
  言 entry n5_compounds: drop ことば "word" (subset of "word, language")

Merge same-reading distinct-senses:
  本 entry n5_compounds: 本/ほん "counter for long thin objects" + 本/ほん "book"
                         → merge to single 本/ほん "book; counter for long thin objects"

Leave as legitimate polysemy (different readings):
  一 entry n5_compounds: 一日/ついたち vs 一日/いちにち
  日 entry n5_compounds: 一日/ついたち vs 一日/いちにち
  人 entry n5_compounds:     人/ひと   vs     人/にん

Post-fix the (kanji_glyph, form, reading) tuple is unique within
any single kanji entry's n5_compounds array — the new CI invariant
JA-103 enforces this going forward.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
KANJI = ROOT / "data" / "kanji.json"

# (kanji_glyph, compound_form, gloss_to_drop)
DROPS = [
    ("月", "月",   "moon"),
    ("前", "前",   "front"),
    ("気", "電気", "light"),
    ("電", "電気", "light"),
    ("道", "道",   "road"),
    ("言", "ことば", "word"),
]


def main() -> int:
    K = json.loads(KANJI.read_text(encoding="utf-8"))
    by_glyph = {e["glyph"]: e for e in K.get("entries", []) if e.get("glyph")}

    dropped = 0
    merged = 0

    # --- DROP subset-gloss compounds ---
    for glyph, form, drop_gloss in DROPS:
        entry = by_glyph.get(glyph)
        if not entry:
            print(f"  ERROR: kanji {glyph} not found")
            return 1
        before = len(entry.get("n5_compounds") or [])
        entry["n5_compounds"] = [
            c for c in (entry.get("n5_compounds") or [])
            if not (
                isinstance(c, dict)
                and c.get("form") == form
                and c.get("gloss") == drop_gloss
            )
        ]
        after = len(entry["n5_compounds"])
        if after < before:
            dropped += before - after
            print(f"  {glyph}: dropped compound {form!r} gloss={drop_gloss!r} ({before} → {after})")
        else:
            print(f"  WARN: {glyph} compound {form!r} gloss={drop_gloss!r} not found to drop")

    # --- MERGE 本: same reading, two distinct senses ---
    entry = by_glyph.get("本")
    if entry:
        comps = entry.get("n5_compounds") or []
        hon_indices = [i for i, c in enumerate(comps)
                       if isinstance(c, dict) and c.get("form") == "本" and c.get("reading") == "ほん"]
        if len(hon_indices) >= 2:
            i0, i1 = hon_indices[0], hon_indices[1]
            c0 = comps[i0]
            c1 = comps[i1]
            # Merge: combine glosses with semicolon. Keep the canonical
            # "book" sense first (it's the primary meaning).
            glosses_seen = []
            for g in (c0.get("gloss"), c1.get("gloss")):
                if g and g not in glosses_seen:
                    glosses_seen.append(g)
            # Reorder to put "book" first if present
            if any("book" == g.strip() for g in glosses_seen):
                book_only = next(g for g in glosses_seen if "book" == g.strip())
                other = [g for g in glosses_seen if g != book_only]
                glosses_seen = [book_only] + other
            merged_gloss = "; ".join(glosses_seen)
            c0["gloss"] = merged_gloss
            c0["bug_024_merged_from"] = c1.get("gloss")
            # Remove the second entry
            entry["n5_compounds"] = [c for j, c in enumerate(comps) if j != i1]
            merged = 1
            print(f"  本: merged {c1.get('gloss')!r} into {c0.get('gloss')!r}")

    KANJI.write_text(json.dumps(K, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nDropped: {dropped} compounds")
    print(f"Merged:  {merged} compounds")
    return 0


if __name__ == "__main__":
    sys.exit(main())
