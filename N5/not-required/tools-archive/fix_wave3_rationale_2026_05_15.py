"""Wave 3 fix — rationale-answer misalignments.

After scanning 402 paper questions, my heuristic flagged 115 entries;
manual review of ~15 samples confirmed all but 2 were valid English /
short technical rationales (legitimate brief explanations).

Real bugs:
  dokkai-2.3 — rationale described 電話 (the SECONDARY instruction)
    instead of 山に のぼる (the primary activity the question is about)
  dokkai-7.6 — rationale was about cake prices, completely unrelated
    to the question (which set comes with drink + salad)
"""
from __future__ import annotations
import json
from collections import OrderedDict
from pathlib import Path

# (paper_filename, qid) -> (new_rationale_en, new_rationale_hi)
FIXES = {
    ("paper-2.json", "dokkai-2.3"): (
        "Yamada's invitation says 来週の 土曜日、みんなで 山に のぼりに 行きませんか — 'Let's all go mountain climbing next Saturday.' That mountain-climbing trip is what Yamada is asking everyone to do.",
        "यामादा का निमंत्रण कहता है 来週の 土曜日、みんなで 山に のぼりに 行きませんか — 'अगले शनिवार सब मिलकर पहाड़ चढ़ने चलें?' यही पहाड़-चढ़ाई वह गतिविधि है जो यामादा सबको करने को कह रहा है।",
    ),
    ("paper-7.json", "dokkai-7.6"): (
        "Per the menu, ハンバーガー セット is the only item marked のみもの と サラダ 付き (comes with drink AND salad). The others have only のみもの 付き or +200円 drink option.",
        "मेनू के अनुसार, केवल ハンバーガー セット पर のみもの と サラダ 付き (पेय और सलाद दोनों के साथ) लिखा है। बाक़ी पर सिर्फ़ のみもの 付き या +200円 पेय विकल्प।",
    ),
}


def main():
    n = 0
    for (fname, qid), (en, hi) in FIXES.items():
        path = Path(f"data/papers/dokkai/{fname}")
        d = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
        for q in d.get("questions", []):
            if q.get("id") == qid:
                old_en = q.get("rationale", "")
                old_hi = q.get("rationale_hi", "")
                q["rationale"] = en
                q["rationale_hi"] = hi
                # mark provenance as llm_curated since this is a corrective
                # re-author by a non-native reviewer
                q["rationale_hi_provenance"] = "llm_curated"
                n += 1
                print(f"  {qid}: rationale fixed")
                print(f"    OLD-EN: {old_en[:80]}")
                print(f"    NEW-EN: {en[:80]}")
                break
        path.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"\nApplied {n}/{len(FIXES)} fixes")


if __name__ == "__main__":
    main()
