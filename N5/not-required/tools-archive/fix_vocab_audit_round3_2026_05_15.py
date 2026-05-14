"""Vocab audit Round 3 fix: the 1 real remaining issue.

すわる entry [1] was 'すわる人が います。' / 'There is a person who to sit.'
Round-2 missed it because round-1 had already fixed its C2 duplicate
(replacing the [2] occurrence), but the [1] occurrence still carried
the verb-template anti-pattern.
"""
from __future__ import annotations
import json
from collections import OrderedDict
from pathlib import Path

VOCAB = Path("data/vocab.json")

FIXES = {
    ("n5.vocab.27-verbs-group-1-verbs.すわる", 1):
        ("つかれたので こうえんの ベンチに すわります。",
         "I sit on a park bench because I'm tired."),
}


def main():
    d = json.loads(VOCAB.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    entries = d["entries"]
    applied = 0
    for (eid, idx), (new_ja, new_en) in FIXES.items():
        for e in entries:
            if e.get("id") == eid:
                e["examples"][idx]["ja"] = new_ja
                e["examples"][idx]["translation_en"] = new_en
                applied += 1
                break
    print(f"Applied: {applied}/{len(FIXES)}")
    VOCAB.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
