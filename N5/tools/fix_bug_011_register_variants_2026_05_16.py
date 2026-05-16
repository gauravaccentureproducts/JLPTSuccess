"""Fix BUG-011 — convert self-contradicting WRONG/RIGHT common_mistakes
entries into register_variant entries (kind-tagged).

Background:
  BUG-007 (closed 2026-05-16) rewrote WHY rationales for 11
  common_mistakes entries to use register-variant framing instead of
  RIGHT/WRONG. But the entries still had the literal `wrong`/`right`
  field-name dichotomy in the data; the WHY text said "both are
  correct" while the data labels still said WRONG and RIGHT. That
  contradiction is BUG-011.

Fix:
  Add a `kind: "register_variant"` field to the affected entries,
  plus optional `label_a` and `label_b` for register dimensions.
  Keep the `wrong`/`right` keys for UI backwards compatibility
  (existing code still reads them) but the UI checks `kind` and
  renders differently — no strike-through, no green check, neutral
  "Form A / Form B" presentation with register labels.

  This is a layered fix: data carries the kind signal; UI rendering
  + static-mirror rendering check for kind and apply
  register-variant presentation when set. Entries without a kind
  field fall through to the existing wrong/right behavior.

Affected entries (18 total across 14 patterns):
  Grammar register/context choices (11):
    n5-069 cm[3], n5-071 cm[2], n5-105 cm[0],
    n5-124 cm[0,1,2], n5-127 cm[1], n5-179 cm[0,1,2]
  Pattern-contrast (1):
    n5-173 cm[2]  (kind=register_variant with pattern-keyed labels)
  Ne-vs-ka pragmatic confirmation (7):
    n5-023 cm[2], n5-052 cm[1], n5-053 cm[1], n5-054 cm[1],
    n5-055 cm[1], n5-056 cm[1], n5-057 cm[1]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR = ROOT / "data" / "grammar.json"

# Migration table: (pattern_id, cm_index, label_a, label_b)
# label_a applies to the `wrong` field (which becomes "form A");
# label_b applies to the `right` field (which becomes "form B");
# The labels are short register / context tags shown next to each form.
MIGRATIONS: list[tuple[str, int, str, str]] = [
    # n5-069 cm[3]: てから vs 〜て、〜
    ("n5-069", 3, "explicit-sequence (てから)", "neutral connective (〜て)"),
    # n5-071 cm[2]: ちょっと まって ください ね vs ちょっと まってください
    ("n5-071", 2, "friendly softener (with ね)", "neutral polite request"),
    # n5-105 cm[0]: 行きたくありません vs 行きたくないです
    ("n5-105", 0, "formal-rigid (たくありません)", "natural polite (たくないです)"),
    # n5-124 cm[0,1,2]: しかし vs でも register choice
    ("n5-124", 0, "formal (しかし in casual context)", "casual (でも)"),
    ("n5-124", 1, "casual (でも)", "formal (しかし)"),
    ("n5-124", 2, "casual (でも in formal context)", "formal (しかし)"),
    # n5-127 cm[1]: けれども vs けど
    ("n5-127", 1, "formal full form (けれども)", "casual contraction (けど)"),
    # n5-173 cm[2]: しないと いけない vs しなくては いけない (pattern-contrast)
    ("n5-173", 2, "n5-175 pattern (ないといけない)", "n5-173 pattern (なくてはいけない)"),
    # n5-179 cm[0,1,2]: と vs って register choice
    ("n5-179", 0, "casual contraction (って in formal context)", "formal quotation (と)"),
    ("n5-179", 1, "formal quotation (と)", "casual contraction (って)"),
    ("n5-179", 2, "formal quotation (と in casual context)", "casual contraction (って)"),
    # ne-vs-ka pragmatic confirmation across 7 question-word patterns
    ("n5-023", 2, "confirmation-seeker (〜ね)", "neutral question (〜か)"),
    ("n5-052", 1, "confirmation-seeker (〜ね)", "neutral question (〜か)"),
    ("n5-053", 1, "confirmation-seeker (〜ね)", "neutral question (〜か)"),
    ("n5-054", 1, "confirmation-seeker (〜ね)", "neutral question (〜か)"),
    ("n5-055", 1, "confirmation-seeker (〜ね)", "neutral question (〜か)"),
    ("n5-056", 1, "confirmation-seeker (〜ね)", "neutral question (〜か)"),
    ("n5-057", 1, "confirmation-seeker (〜ね)", "neutral question (〜か)"),
    # Additional register-variant entries surfaced by the Phase-0
    # regression block during BUG-011 close-out (2026-05-16). Same
    # class as the originally-reported entries; the bug description
    # listed examples, not the exhaustive set.
    ("n5-107", 3, "casual plain (行く in formal context)", "polite (行きます)"),
    ("n5-113", 0, "polite full (三時 三十分)", "casual (三時はん)"),
    ("n5-125", 0, "casual contraction (じゃ in formal context)", "formal (では)"),
    ("n5-125", 1, "formal (では in casual context)", "casual contraction (じゃ)"),
    ("n5-125", 2, "formal (では in casual context)", "casual contraction (じゃ)"),
    ("n5-158", 2, "polite (でしょう in casual context)", "casual plain (だろう)"),
    ("n5-159", 2, "casual plain (だね in formal context)", "polite (ですね)"),
    # NOTE: n5-176 cm[0] is intentionally EXCLUDED — `行かなくちゃです`
    # is a genuine grammar error (casual contraction `なくちゃ` cannot
    # combine with `です` — the WHY says "they don't combine" and
    # "sounds wrong"). It should remain a legacy wrong/right entry.
    ("n5-176", 1, "full form (なくては in casual context)", "casual contraction (なくちゃ)"),
    ("n5-176", 2, "full form (なくては in casual context)", "casual contraction (なくちゃ)"),
]


def main() -> int:
    sys.stdout = open(sys.stdout.fileno(), "w", encoding="utf-8", buffering=1)
    G = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in G.get("patterns", []) if p.get("id")}

    written = 0
    skipped = 0
    errors: list[str] = []

    for pid, idx, label_a, label_b in MIGRATIONS:
        p = by_id.get(pid)
        if not p:
            errors.append(f"{pid}: pattern not found")
            continue
        cms = p.get("common_mistakes") or []
        if idx >= len(cms):
            errors.append(f"{pid} cm[{idx}]: index out of range (have {len(cms)})")
            continue
        cm = cms[idx]
        if cm.get("kind") == "register_variant":
            skipped += 1
            print(f"  {pid} cm[{idx}]: already migrated, skipping")
            continue
        cm["kind"] = "register_variant"
        cm["label_a"] = label_a
        cm["label_b"] = label_b
        written += 1
        print(f"  {pid} cm[{idx}]: marked kind=register_variant (label_a={label_a!r}, label_b={label_b!r})")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  {e}")
        return 1

    GRAMMAR.write_text(
        json.dumps(G, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(f"\nSummary: {written} entries migrated, {skipped} skipped (already migrated).")
    print(f"Saved {GRAMMAR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
