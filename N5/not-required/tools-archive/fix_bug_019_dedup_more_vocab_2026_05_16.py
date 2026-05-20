"""Fix BUG-019 — 3 over-duplicated (form, reading) pairs missed by
the BUG-018 dedup pass. Same shape as BUG-018: same form, same reading,
one gloss being a subset/near-duplicate of the other.

Cases (canonical-side picks below):

(a) 月 (つき) — 2 entries:
    - n5.vocab.11-time-days-weeks-month.月  gloss="month, moon"  ← KEEP (richer gloss; 18 refs)
    - n5.vocab.14-nature-and-weather.月     gloss="moon"          ← DROP (subset; 3 refs)

(b) あつい — 4 entries (3 legitimate kanji-distinct + 1 duplicate):
    - n5.vocab.14-nature-and-weather.あつい  gloss="hot (weather)"  ← DROP (25 refs, but `31-adjectives.あつい` has 60 refs and lives in the natural section for an i-adj)
    - n5.vocab.31-adjectives.あつい            gloss="hot (weather; ...)"  ← KEEP and clean gloss
    - n5.vocab.31-adjectives.あつい.2          gloss="hot (touch; 熱い)"   ← KEEP unchanged
    - n5.vocab.31-adjectives.あつい.3          gloss="thick (厚い)"         ← KEEP unchanged

(c) きって (きって) — 2 entries:
    - n5.vocab.22-money-and-shopping.きって       gloss="postage stamp"  ← KEEP (more precise; 3 refs)
    - n5.vocab.37-common-nouns-miscella.きって    gloss="stamp"          ← DROP (less precise; 2 refs)

Plus: cross-corpus reference rewrites in drills_auto.json,
grammar.json, reading.json, listening.json, authentic.json,
questions.json, kanji.json.

Edge case left untouched: いくつ (いくつ) has 2 entries with
DIFFERENT POS (question-word vs counter). Per the bug description,
that duplication is legitimate and stays.

Expected post-fix: 998 → 995 entries.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "vocab.json"

# (form, canonical_id, drop_id, new_gloss_on_canonical_or_None)
PICKS = [
    ("月",
     "n5.vocab.11-time-days-weeks-month.月",
     "n5.vocab.14-nature-and-weather.月",
     None),  # canonical gloss "month, moon" already covers both
    ("あつい",
     "n5.vocab.31-adjectives.あつい",
     "n5.vocab.14-nature-and-weather.あつい",
     "hot (weather; 暑い — distinct from 熱い 'hot to touch' and 厚い 'thick', same reading)"),
    ("きって",
     "n5.vocab.22-money-and-shopping.きって",
     "n5.vocab.37-common-nouns-miscella.きって",
     None),  # canonical gloss "postage stamp" is the precise one
]

CROSS_FILES = [
    "data/grammar.json",
    "data/reading.json",
    "data/listening.json",
    "data/authentic.json",
    "data/questions.json",
    "data/drills_auto.json",
    "data/kanji.json",
]


def merge_examples_and_collocations(canon: dict, dropped: dict) -> None:
    """Pull unique examples + collocations from dropped → canon."""
    canon_jas = {(ex.get("ja") or "").strip()
                 for ex in canon.get("examples") or []
                 if isinstance(ex, dict)}
    for ex in dropped.get("examples") or []:
        if not isinstance(ex, dict):
            continue
        ja = (ex.get("ja") or "").strip()
        if ja and ja not in canon_jas:
            canon.setdefault("examples", []).append(ex)
            canon_jas.add(ja)
    canon_cols = list(canon.get("collocations") or [])
    for c in dropped.get("collocations") or []:
        if isinstance(c, str) and c not in canon_cols:
            canon_cols.append(c)
    if canon_cols:
        canon["collocations"] = canon_cols
    # Audit trail
    canon["bug_019_merged_from"] = dropped.get("id")
    canon["bug_019_merged_from_section"] = dropped.get("section")


def main() -> int:
    V = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = V.get("entries", [])
    by_id = {e["id"]: e for e in entries if "id" in e}

    drops: set[str] = set()
    id_rewrites: dict[str, str] = {}

    for form, canon_id, drop_id, new_gloss in PICKS:
        if canon_id not in by_id:
            print(f"  ERROR: canonical {canon_id} not found")
            return 1
        if drop_id not in by_id:
            print(f"  ERROR: drop {drop_id} not found")
            return 1
        canon = by_id[canon_id]
        dropped = by_id[drop_id]
        merge_examples_and_collocations(canon, dropped)
        if new_gloss:
            canon["gloss"] = new_gloss
        drops.add(drop_id)
        id_rewrites[drop_id] = canon_id
        print(f"  {form}: keep {canon_id} / drop {drop_id}")
        if new_gloss:
            print(f"    new gloss: {new_gloss}")

    pre_count = len(entries)
    V["entries"] = [e for e in entries if e.get("id") not in drops]
    post_count = len(V["entries"])
    print(f"\nvocab.json: {pre_count} → {post_count} entries (dropped {len(drops)})")

    VOCAB.write_text(json.dumps(V, ensure_ascii=False, indent=2), encoding="utf-8")

    # Rewrite cross-references
    total_rewritten = 0
    for rel in CROSS_FILES:
        fpath = ROOT / rel
        if not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")
        original = text
        rewritten = 0
        for drop_id, canon_id in id_rewrites.items():
            count = text.count(drop_id)
            if count:
                text = text.replace(drop_id, canon_id)
                rewritten += count
        if text != original:
            fpath.write_text(text, encoding="utf-8")
            total_rewritten += rewritten
            print(f"  {rel}: rewrote {rewritten} refs")

    print(f"\nTotal cross-references rewritten: {total_rewritten}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
