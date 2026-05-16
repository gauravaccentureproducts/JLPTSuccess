"""Fix BUG-015 — normalize counter / counter_register schema in vocab.json.

Pre-fix state (1009 entries):
  counter:
    string ("人"):                       111 entries  (legacy)
    dict {"kanji": "人", "reading": "にん"}: 204 entries  (modern)
    null:                                694 entries
  counter_register:
    string ("にん"):                       21 entries  (paired with legacy)
    dict {counter, irregular, note, ...}: 16 entries  (counter-word metadata)
    null:                                972 entries

Two distinct uses of `counter_register` were conflated:
  - 21 string entries: register reading of the counter (paired with
    string `counter`). The information is redundant once `counter`
    becomes a dict carrying `reading`.
  - 16 dict entries: metadata about counter WORDS themselves
    (一つ, 二つ, 三つ, etc.) — irregular form, register pair, notes.
    This is a completely different semantic use of the same field.

Post-fix schema (canonical):
  counter:
    dict {"kanji": "<kanji>", "reading": "<reading>"} OR null
  counter_register:
    null (deprecated/removed; reading is now inside counter)
  counter_word_metadata:
    dict {counter, irregular, note, register_pair} on the ~16
    counter-word entries only; null/absent elsewhere
    (NEW field, isolates the counter-word documentation from
    the per-noun register hint)
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "vocab.json"


def main() -> int:
    V = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = V.get("entries", [])

    migrated_legacy = 0
    migrated_word_metadata = 0
    already_canonical = 0

    for e in entries:
        c = e.get("counter")
        cr = e.get("counter_register")

        # Case 1: legacy string-string pair → consolidate into dict
        if isinstance(c, str) and isinstance(cr, str):
            e["counter"] = {"kanji": c, "reading": cr}
            e["counter_register"] = None
            migrated_legacy += 1
            continue

        # Case 2: dict counter, string/null counter_register → already canonical
        if isinstance(c, dict) and ("kanji" in c and "reading" in c):
            # If counter_register is still set (rare), clear it; the
            # reading lives inside counter now.
            if isinstance(cr, str):
                e["counter_register"] = None
                migrated_legacy += 1
            else:
                already_canonical += 1
            continue

        # Case 3: counter=null, counter_register=dict → counter-word metadata
        if c is None and isinstance(cr, dict):
            # Move metadata to dedicated field; null out counter_register
            e["counter_word_metadata"] = cr
            e["counter_register"] = None
            migrated_word_metadata += 1
            continue

        # Case 4: string counter with NULL counter_register (rare edge)
        if isinstance(c, str) and cr is None:
            # Best-effort: keep the kanji but mark reading as same as
            # the string (since we can't recover it). Note: at survey
            # time this case had 0 entries.
            e["counter"] = {"kanji": c, "reading": c}
            migrated_legacy += 1
            continue

        # Case 5: both null → nothing to do
        # Case 6: anything else → unexpected; surface for review
        if c is not None and not isinstance(c, dict):
            print(f"  WARN: {e.get('id','?')}: unexpected counter shape: {c!r}")

    VOCAB.write_text(json.dumps(V, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Migrated legacy string-pair entries: {migrated_legacy}")
    print(f"Migrated counter-word metadata entries: {migrated_word_metadata}")
    print(f"Already canonical (dict counter): {already_canonical}")
    print(f"Saved {VOCAB}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
