"""ISSUE-125 fix: complete the `frequent_patterns` reverse map on vocab.

Walks grammar.json patterns -> examples -> vocab_ids; builds the inverted
map (vocab_id -> [pattern_id, ...]); merges with any existing
`frequent_patterns` field on vocab entries; persists.

Existing 437/1009 entries already have the field — for those, we ADD any
pattern IDs missing from the live derivation (defensive union). For the
572 remaining, we POPULATE from scratch.

Provenance: auto_derived (the inverse map is mechanically derived from
example-sentence vocab_ids; no native review required for the linkage
itself).
"""
import json
import io
import sys
import shutil
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

VOCAB = "data/vocab.json"
GRAMMAR = "data/grammar.json"
BACKUP = "data/vocab.json.bak_2026_05_13_issue_125_frequent_patterns"


def main():
    shutil.copy2(VOCAB, BACKUP)

    G = json.load(open(GRAMMAR, encoding="utf-8"))
    V = json.load(open(VOCAB, encoding="utf-8"))

    # Build inverted map: vocab_id -> set of pattern_ids
    inverted = defaultdict(set)
    for p in G["patterns"]:
        pid = p["id"]
        for ex in (p.get("examples") or []):
            for vid in (ex.get("vocab_ids") or []):
                inverted[vid].add(pid)

    print(f"Inverted map: {len(inverted)} vocab IDs referenced from grammar examples")

    # Apply to vocab
    updated_from_scratch = 0
    extended = 0
    unchanged = 0
    no_refs = 0
    for entry in V["entries"]:
        vid = entry.get("id")
        existing = entry.get("frequent_patterns") or []
        derived = sorted(inverted.get(vid, set()))

        if not derived:
            # Vocab entry never referenced in any pattern example
            no_refs += 1
            continue

        if not existing:
            entry["frequent_patterns"] = derived
            entry["frequent_patterns_provenance"] = "auto_derived"
            entry.setdefault("audit_wave", "issue-125-drift-fix-2026-05-13")
            updated_from_scratch += 1
        else:
            # Union: keep existing, add any from inverted map not already there
            merged = sorted(set(existing) | set(derived))
            if merged != sorted(existing):
                entry["frequent_patterns"] = merged
                # If existing was native_reviewed, downgrade to merged-auto
                if entry.get("frequent_patterns_provenance") == "native_reviewed":
                    entry["frequent_patterns_provenance"] = "native_reviewed_extended_auto"
                extended += 1
            else:
                unchanged += 1

    with open(VOCAB, "w", encoding="utf-8") as f:
        json.dump(V, f, ensure_ascii=False, indent=2)

    print(f"\nResults:")
    print(f"  Updated from scratch:  {updated_from_scratch}")
    print(f"  Extended existing:     {extended}")
    print(f"  Unchanged (already complete): {unchanged}")
    print(f"  No references found:   {no_refs}")
    print(f"  Total vocab entries:   {len(V['entries'])}")
    total_with = sum(1 for v in V['entries'] if v.get('frequent_patterns'))
    print(f"  Final coverage:        {total_with}/{len(V['entries'])} "
          f"({total_with * 100 // len(V['entries'])}%)")


if __name__ == "__main__":
    main()
