"""
ISSUE-120 / IMP-153 — Auto-derive vocab[].frequent_patterns from
grammar[].examples[].vocab_ids inverse index.

Audit finding (2026-05-12): 161/1009 vocab entries had >=3 patterns in
frequent_patterns. D2b reverse density was 1.1 avg vs target >=3.

Approach (deterministic — no manual authoring):
  For each grammar pattern P:
    For each example E in P.examples:
      For each vocab_id V in E.vocab_ids:
        Add P.id to vocab[V].frequent_patterns (set semantics)

The vocab.frequent_patterns array is written back with stable ordering
(sorted by pattern_id) so the JSON diff is deterministic across runs.

Existing values are MERGED, not replaced — any hand-curated additions
remain. The script is idempotent.

Run from N5/ as: python tools/build_frequent_patterns.py
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
VOCAB = REPO / "data" / "vocab.json"
GRAMMAR = REPO / "data" / "grammar.json"


def main() -> int:
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))
    grammar = json.loads(GRAMMAR.read_text(encoding="utf-8"))

    # Build inverse index: vocab_id -> set(pattern_id)
    inverse: dict[str, set[str]] = {}
    for p in grammar["patterns"]:
        pid = p.get("id")
        if not pid:
            continue
        for ex in p.get("examples") or []:
            for vid in ex.get("vocab_ids") or []:
                inverse.setdefault(vid, set()).add(pid)

    # Census before
    before_counts = {">=5": 0, "3-4": 0, "1-2": 0, "0": 0}
    for v in vocab["entries"]:
        n = len(v.get("frequent_patterns") or [])
        if n >= 5:
            before_counts[">=5"] += 1
        elif n >= 3:
            before_counts["3-4"] += 1
        elif n >= 1:
            before_counts["1-2"] += 1
        else:
            before_counts["0"] += 1

    # Merge existing + inverse-derived; sort by pattern_id for stable JSON
    touched = 0
    for v in vocab["entries"]:
        vid = v.get("id")
        if not vid:
            continue
        existing = set(v.get("frequent_patterns") or [])
        derived = inverse.get(vid, set())
        merged = existing | derived
        if merged != existing:
            touched += 1
            v["frequent_patterns"] = sorted(merged)
        elif "frequent_patterns" not in v and merged:
            v["frequent_patterns"] = sorted(merged)
            touched += 1

    # Census after
    after_counts = {">=5": 0, "3-4": 0, "1-2": 0, "0": 0}
    avg_n = 0
    nonzero = 0
    for v in vocab["entries"]:
        fp = v.get("frequent_patterns") or []
        n = len(fp)
        if n >= 5:
            after_counts[">=5"] += 1
        elif n >= 3:
            after_counts["3-4"] += 1
        elif n >= 1:
            after_counts["1-2"] += 1
        else:
            after_counts["0"] += 1
        if n > 0:
            avg_n += n
            nonzero += 1

    print(f"Total vocab entries: {len(vocab['entries'])}")
    print(f"Entries touched (merged or initialized): {touched}")
    print()
    print(f"{'Bucket':<10} {'Before':>10} {'After':>10}")
    for k in (">=5", "3-4", "1-2", "0"):
        print(f"{k:<10} {before_counts[k]:>10} {after_counts[k]:>10}")
    print()
    at_or_above_target = after_counts[">=5"] + after_counts["3-4"]
    print(f"At target (>=3 patterns): {at_or_above_target}/{len(vocab['entries'])}")
    print(
        f"Average patterns/entry (non-zero): {avg_n/max(nonzero,1):.2f} "
        f"({avg_n}/{nonzero})"
    )

    VOCAB.write_text(
        json.dumps(vocab, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nWrote {VOCAB}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
