"""Round-5: fix 2 regressions from round-4 batch.

n5.vocab.4-body-parts.かお [1] collided with [2] (both "まいあさ かおを
あらいます。"). Replacing [1] with a different sentence.

n5.vocab.4-body-parts.みみ [1] collided with [0] (both "みみで おんがくを
聞きます。"). Replacing [1] with a different sentence.

The 2 C1 hits on demonstrative entries (これ[1], あれ[0]) are not data
bugs — `これは Xです。` IS the canonical example for the これ/あれ
headwords themselves. The checker is over-flagging; suppress in code.
"""
from __future__ import annotations
import json
from collections import OrderedDict
from pathlib import Path

VOCAB = Path("data/vocab.json")

FIXES = {
    ("n5.vocab.4-body-parts.かお", 1):
        ("子どもの かおは とても かわいいです。",
         "The child's face is very cute."),
    ("n5.vocab.4-body-parts.みみ", 1):
        ("いぬの みみは とても 大きいです。",
         "The dog's ears are very big."),
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
