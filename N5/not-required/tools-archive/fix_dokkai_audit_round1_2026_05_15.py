"""Dokkai audit Round 1 — schema completeness fixes.

R18 (9 questions): set format_role='primary' on the 9 questions in
  passages 046..054 that were authored without the field. The renderer
  (js/reading.js:60) treats missing format_role as equivalent to
  'primary', so this is a no-op behavioral change — just makes the
  schema uniform across the corpus.

R20 (9 passages): populate vocab_used from vocab_preview ids on the
  same 9 passages. vocab_preview entries each have a vocab_id field;
  vocab_used is the legacy list-of-ids shape used by audit tools.
  No runtime consumer of vocab_used in js/ — purely cosmetic.
"""
from __future__ import annotations
import json
from collections import OrderedDict
from pathlib import Path

READING = Path("data/reading.json")

AFFECTED_IDS = {
    "n5.read.046", "n5.read.047", "n5.read.048", "n5.read.049",
    "n5.read.050", "n5.read.051", "n5.read.052", "n5.read.053",
    "n5.read.054",
}


def main() -> None:
    d = json.loads(READING.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    n_format = n_vocab = 0
    for p in d["passages"]:
        pid = p.get("id", "")
        if pid not in AFFECTED_IDS:
            continue
        # R18: set format_role='primary' on each question if missing
        for q in p.get("questions", []):
            if not q.get("format_role"):
                q["format_role"] = "primary"
                n_format += 1
        # R20: populate vocab_used from vocab_preview ids
        preview = p.get("vocab_preview") or []
        if preview and not p.get("vocab_used"):
            vocab_ids = [item["vocab_id"] for item in preview if item.get("vocab_id")]
            p["vocab_used"] = vocab_ids
            n_vocab += 1
    READING.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"R18 format_role set:    {n_format}")
    print(f"R20 vocab_used filled:  {n_vocab}")


if __name__ == "__main__":
    main()
