"""Fix BUG-022 — normalize kanji.json examples field name from
`lemma` to `form` (same schema as vocab.json and the majority of
existing entries).

Pre-fix:
  form only:        374 examples (manually curated)
  lemma only:        20 examples (auto-derived from vocab.json)
  both form+lemma:   14 examples (auto-derived, duplicate content)

Post-fix:
  form only on every example
  lemma field dropped
  provenance signal stays in `auto_derived: true` + `vocab_id`

Same class as BUG-015 (vocab counter field schema inconsistency).
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
KANJI = ROOT / "data" / "kanji.json"


def main() -> int:
    K = json.loads(KANJI.read_text(encoding="utf-8"))
    entries = K.get("entries", [])

    form_only = 0
    lemma_only = 0
    both = 0
    migrated = 0

    for entry in entries:
        for ex in entry.get("examples") or []:
            if not isinstance(ex, dict):
                continue
            has_form = "form" in ex
            has_lemma = "lemma" in ex
            if has_form and has_lemma:
                # Both: drop lemma (form is canonical)
                # Verify they agree, otherwise warn
                if ex.get("form") != ex.get("lemma"):
                    print(f"  WARN: {entry.get('glyph')} example form={ex['form']!r} != lemma={ex['lemma']!r}; keeping form")
                del ex["lemma"]
                both += 1
                migrated += 1
            elif has_lemma and not has_form:
                ex["form"] = ex["lemma"]
                del ex["lemma"]
                lemma_only += 1
                migrated += 1
            elif has_form:
                form_only += 1

    KANJI.write_text(json.dumps(K, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  form only (unchanged):  {form_only}")
    print(f"  lemma only (migrated):  {lemma_only}")
    print(f"  both (lemma dropped):   {both}")
    print(f"\nTotal migrated: {migrated}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
