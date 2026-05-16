"""Fix BUG-018 — 10 vocab forms duplicated across sections with
subset glosses. Pick one canonical entry per form, merge unique data,
delete the duplicate, and rewrite cross-references in other corpora.

Canonical-section picks (form → canonical_section_id_segment).
Tie-breaking heuristic: prefer the section whose gloss is more
comprehensive (more meanings listed); fall back to the section
referenced more times in OTHER corpora.

After fix:
  - vocab.json: 1009 → 999 entries
  - Other corpora: stale duplicate-ID refs rewritten to canonical
  - Each kept entry: merged examples / collocations from the dropped
    entry, where unique

Cross-files updated (string-replace of full ID, safe because IDs
are unambiguous):
  data/grammar.json, data/reading.json, data/listening.json,
  data/authentic.json, data/questions.json, data/drills_auto.json,
  data/kanji.json
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "vocab.json"

# (form, canonical_id_full, drop_id_full)
PICKS: list[tuple[str, str, str]] = [
    ("道",     "n5.vocab.13-locations-and-places-.道",       "n5.vocab.23-transport.道"),
    ("とけい", "n5.vocab.10-time-general.とけい",            "n5.vocab.21-clothing-and-accessor.とけい"),
    ("ことば", "n5.vocab.24-school-and-study.ことば",         "n5.vocab.37-common-nouns-miscella.ことば"),
    # 'え': furniture section had MORE cross-corpus refs (~46 vs ~9),
    # but the school-and-study gloss is richer ("picture, drawing").
    # Keep the more-referenced one (lower migration cost), merge the
    # richer gloss data in.
    ("え",     "n5.vocab.26-house-and-furniture.え",         "n5.vocab.24-school-and-study.え"),
    ("電気",   "n5.vocab.24-school-and-study.電気",          "n5.vocab.26-house-and-furniture.電気"),
    ("もう",   "n5.vocab.12-time-frequency-sequen.もう",     "n5.vocab.33-adverbs.もう"),
    ("すぐ",   "n5.vocab.12-time-frequency-sequen.すぐ",     "n5.vocab.33-adverbs.すぐ"),
    ("前",     "n5.vocab.12-time-frequency-sequen.前",       "n5.vocab.13-locations-and-places-.前"),
    ("どうも", "n5.vocab.36-greetings-and-set-phr.どうも",   "n5.vocab.33-adverbs.どうも"),
    ("どうぞよろしく", "n5.vocab.36-greetings-and-set-phr.どうぞよろしく", "n5.vocab.33-adverbs.どうぞよろしく"),
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


def merge_data(canonical: dict, dropped: dict) -> None:
    """Merge unique data from dropped → canonical (in place)."""
    # Merge examples: add dropped's examples that have a JA not already present
    canon_jas = {(ex.get("ja") or "").strip()
                 for ex in canonical.get("examples") or []
                 if isinstance(ex, dict)}
    for ex in dropped.get("examples") or []:
        if not isinstance(ex, dict):
            continue
        ja = (ex.get("ja") or "").strip()
        if ja and ja not in canon_jas:
            canonical.setdefault("examples", []).append(ex)
            canon_jas.add(ja)

    # Merge collocations: union of strings
    canon_cols = list(canonical.get("collocations") or [])
    for c in dropped.get("collocations") or []:
        if isinstance(c, str) and c not in canon_cols:
            canon_cols.append(c)
    if canon_cols:
        canonical["collocations"] = canon_cols

    # Merge gloss: if dropped gloss has content not in canonical,
    # keep the canonical's (preferred — we chose it for a reason)
    # but note the alternative in a new field for provenance.
    if dropped.get("gloss") and dropped["gloss"] != canonical.get("gloss"):
        canonical["gloss_alt_dropped_section"] = dropped["gloss"]

    # Track the dropped ID + section for audit trail
    canonical["bug_018_merged_from"] = dropped.get("id")
    canonical["bug_018_merged_from_section"] = dropped.get("section")


def main() -> int:
    V = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = V.get("entries", [])
    by_id = {e["id"]: e for e in entries if "id" in e}

    canonical_for: dict[str, str] = {}   # drop_id -> canonical_id
    merge_pairs: list[tuple[dict, dict]] = []
    drop_ids: set[str] = set()

    for form, canon_id, drop_id in PICKS:
        if canon_id not in by_id:
            print(f"  WARN: canonical ID not found: {canon_id}")
            continue
        if drop_id not in by_id:
            print(f"  WARN: drop ID not found: {drop_id}")
            continue
        canonical_for[drop_id] = canon_id
        merge_pairs.append((by_id[canon_id], by_id[drop_id]))
        drop_ids.add(drop_id)
        print(f"  {form}: keep {canon_id} / drop {drop_id}")

    # Merge data from each dropped into its canonical
    for canon, dropped in merge_pairs:
        merge_data(canon, dropped)

    # Remove dropped entries
    V["entries"] = [e for e in entries if e.get("id") not in drop_ids]

    pre_count = len(entries)
    post_count = len(V["entries"])
    print(f"\nvocab.json: {pre_count} → {post_count} entries (dropped {len(drop_ids)})")

    VOCAB.write_text(json.dumps(V, ensure_ascii=False, indent=2), encoding="utf-8")

    # Rewrite cross-references in other corpora
    rewrite_summary: dict[str, int] = {}
    for rel in CROSS_FILES:
        fpath = ROOT / rel
        if not fpath.exists():
            continue
        text = fpath.read_text(encoding="utf-8")
        original = text
        rewritten = 0
        for drop_id, canon_id in canonical_for.items():
            count = text.count(drop_id)
            if count:
                text = text.replace(drop_id, canon_id)
                rewritten += count
        if text != original:
            fpath.write_text(text, encoding="utf-8")
            rewrite_summary[rel] = rewritten
            print(f"  {rel}: rewrote {rewritten} refs")
        else:
            rewrite_summary[rel] = 0

    total_rewritten = sum(rewrite_summary.values())
    print(f"\nTotal cross-references rewritten: {total_rewritten}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
