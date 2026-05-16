"""Fix BUG-013 — complete the register-variant migration by renaming
the JSON keys themselves (`wrong` → `form_a`, `right` → `form_b`)
for entries with `kind: "register_variant"`.

Background:
  BUG-011 (2026-05-16) added the `kind` field + `label_a` / `label_b`
  but kept `wrong` / `right` keys for UI backwards compatibility.
  BUG-013 re-audit (2026-05-16) flagged that the keys themselves
  still imply WRONG/RIGHT framing at the data surface — any
  downstream consumer reading the JSON sees a literal "wrong" field
  on a sentence that the same entry's WHY paragraph calls valid.
  The contradiction at the data surface remains even with the kind
  flag added.

Fix:
  Rename the keys in-place for the 27 entries with
  `kind: "register_variant"`:
    wrong → form_a
    right → form_b
  Other entries (legacy `wrong`/`right` for actual grammar errors)
  are LEFT UNCHANGED — those are real wrongs, and the field names
  match the semantic.

Coverage: 27 entries across 19 patterns (the same set BUG-011 fixed).
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR = ROOT / "data" / "grammar.json"


def main() -> int:
    G = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    renamed = 0
    skipped = 0

    for p in G.get("patterns", []):
        for cm in p.get("common_mistakes", []) or []:
            if not isinstance(cm, dict):
                continue
            if cm.get("kind") != "register_variant":
                continue
            # Already migrated to form_a/form_b? Skip.
            if "form_a" in cm and "form_b" in cm and "wrong" not in cm and "right" not in cm:
                skipped += 1
                continue
            # Build a new ordered dict with form_a/form_b in place of wrong/right.
            new_cm: dict = {}
            for k, v in cm.items():
                if k == "wrong":
                    new_cm["form_a"] = v
                elif k == "right":
                    new_cm["form_b"] = v
                else:
                    new_cm[k] = v
            # If `form_a` ended up missing because the entry had no `wrong`
            # field for some reason, fall back to whatever exists.
            if "form_a" not in new_cm and "wrong" in cm:
                new_cm["form_a"] = cm["wrong"]
            if "form_b" not in new_cm and "right" in cm:
                new_cm["form_b"] = cm["right"]
            cm.clear()
            cm.update(new_cm)
            renamed += 1

    GRAMMAR.write_text(
        json.dumps(G, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )

    print(f"Renamed wrong→form_a, right→form_b in {renamed} register_variant entries.")
    print(f"Skipped {skipped} entries already migrated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
