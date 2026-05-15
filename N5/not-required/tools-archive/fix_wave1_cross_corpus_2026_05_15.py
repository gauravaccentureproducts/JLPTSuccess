"""Wave 1 cross-corpus consistency fix.

X5: vocab.json まがる gloss was 'to turn' (incomplete);
listening.json glossary correctly has 'to turn, to bend'.
Update vocab.json to the more complete form so all corpora agree.
"""
from __future__ import annotations
import json
from collections import OrderedDict
from pathlib import Path

VOCAB = Path("data/vocab.json")

GLOSS_FIXES = {
    "n5.vocab.27-verbs-group-1-verbs.まがる": "to turn, to bend",
}


def main():
    d = json.loads(VOCAB.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    n = 0
    for e in d["entries"]:
        if e["id"] in GLOSS_FIXES:
            old = e.get("gloss")
            e["gloss"] = GLOSS_FIXES[e["id"]]
            n += 1
            print(f"  {e['id']}: {old!r} -> {e['gloss']!r}")
    VOCAB.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Applied {n}/{len(GLOSS_FIXES)} fixes")


if __name__ == "__main__":
    main()
