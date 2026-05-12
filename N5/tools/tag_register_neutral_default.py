"""
ISSUE-115 — Tag vocab.register with explicit 'neutral' default.

Audit finding (2026-05-12): 61/1009 vocab entries had register set
(humble 8 / respectful 8 / neutral 27 / casual 7 / polite 11). The
remaining 948 had no register tag, leaving the registry ambiguous —
absence-of-tag could mean either "neutral by default" or "not yet
classified".

Audit Open Question Q7: "for 906 entries that are neutral by default,
do we add register: 'neutral' to all (explicit) or leave the field
absent (implicit)?"

POLICY (set 2026-05-12): EXPLICIT neutral default. Every entry carries
a register value. Renderers can choose to suppress display when value
is 'neutral'. This makes the registry self-describing — no inference
needed about "missing means neutral vs. missing means unclassified".

Heuristic rules (in priority order):

  1. PRESERVE existing register tag. Do not overwrite hand-curated
     entries. (61 entries are already correctly tagged.)
  2. ござる (archaic copular) -> 'polite' (formal_archaic flavor)
  3. All other untagged entries -> 'neutral' with provenance='auto_derived'

The 9 N5-canonical humble/respectful verbs (いらっしゃる, おっしゃる,
めしあがる, いただく, くださる, なさる) are above-N5 and not in this corpus,
so no manual exception is needed for them.

Idempotent — re-running preserves manual native_reviewed entries.

Run from N5/ as: python tools/tag_register_neutral_default.py
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
VOCAB = REPO / "data" / "vocab.json"

# Forms that should NOT be tagged neutral by default.
FORM_OVERRIDES = {
    "ござる": "polite",  # archaic formal copular
}


def main() -> int:
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = vocab["entries"]

    preserved = 0
    auto_tagged = 0
    override_applied = 0
    final_counts: dict[str, int] = {}

    for v in entries:
        existing = v.get("register")
        if existing:
            preserved += 1
            final_counts[existing] = final_counts.get(existing, 0) + 1
            continue

        form = v.get("form") or ""
        if form in FORM_OVERRIDES:
            tag = FORM_OVERRIDES[form]
            v["register"] = tag
            v["register_provenance"] = "auto_derived"
            override_applied += 1
            final_counts[tag] = final_counts.get(tag, 0) + 1
            continue

        v["register"] = "neutral"
        v["register_provenance"] = "auto_derived"
        auto_tagged += 1
        final_counts["neutral"] = final_counts.get("neutral", 0) + 1

    print(f"Total vocab entries: {len(entries)}")
    print(f"Preserved (existing register): {preserved}")
    print(f"Override applied (FORM_OVERRIDES): {override_applied}")
    print(f"Auto-tagged neutral: {auto_tagged}")
    print()
    print("Final register-tag distribution:")
    for k in ("neutral", "polite", "humble", "respectful", "casual"):
        n = final_counts.get(k, 0)
        pct = 100 * n / len(entries)
        print(f"  {k:<12}: {n:>4}  ({pct:.1f}%)")
    leftover_keys = set(final_counts) - {"neutral", "polite", "humble", "respectful", "casual"}
    for k in sorted(leftover_keys):
        n = final_counts[k]
        print(f"  {k:<12}: {n:>4}  (other)")
    print()
    print(f"Coverage: {sum(final_counts.values())}/{len(entries)}")

    VOCAB.write_text(
        json.dumps(vocab, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nWrote {VOCAB}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
