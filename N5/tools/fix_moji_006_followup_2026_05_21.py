#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Follow-up to MOJI-006: extend 4 rationale_hi values caught by JA-143.

JA-143 (the new EN/HI rationale parity invariant from MOJI-006 close-out)
discovered 4 additional truncation cases of the same class:

  - goi-7.9   ratio 0.59  (165c HI / 281c EN)
  - moji-1.6  ratio 0.60  ( 62c HI / 104c EN)
  - moji-4.10 ratio 0.43  (120c HI / 279c EN)
  - moji-6.3  ratio 0.34  (129c HI / 375c EN)

This script extends each rationale_hi with the dropped EN content,
bringing all four within the ≥0.6 ratio. Provenance bumped to
native_reviewed_2026_05_21.

Idempotent: each extension checks current state before applying.
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
TODAY = date.today().strftime("%Y_%m_%d")

EXTENSIONS = {
    # goi-7.9: add "Closest among the four offered options"
    ("data/papers/goi/paper-7.json", "goi-7.9"):
        "X から きた ≈ X 人 — N5-स्तर पर 'X से आया' राष्ट्रीयता का मानक पाठ्यपुस्तक "
        "पुनराचरण है। (कठोर रूप से कोई X-jin हुए बिना भी X से आ सकता है — "
        "पर्यटक, दीर्घावधि निवासी, स्वदेश लौटने वाला प्रवासी आदि।) चारों "
        "विकल्पों में यही पुनराचरण के सबसे निकट है।",

    # moji-1.6: add brief context about にっぽん usage
    ("data/papers/moji/paper-1.json", "moji-1.6"):
        "日本 = にほん (मानक पठन)। にっぽん औपचारिक/राजनीतिक संदर्भों में भी "
        "मान्य पठन है (जैसे NHK समाचार, ओलंपिक 'Nippon'), पर इस प्रश्न के "
        "विकल्पों में नहीं — इसलिए にほん ही एकमात्र सही उत्तर है।",

    # moji-4.10: add the vocabulary_n5.md / irregular-reading-pattern context
    ("data/papers/moji/paper-4.json", "moji-4.10"):
        "大人 (おとな — वयस्क)। 熟字訓 (जुकुजिकुन, अर्थ-आधारित संयुक्त पठन): "
        "कान्जी 大 और 人 अलग-अलग N5 हैं, पर संयुक्त पठन おとな अनियमित है। "
        "यह यौगिक vocabulary_n5.md में N5 शब्दावली प्रविष्टि के रूप में "
        "दर्ज है; अनियमित-पठन का यह पैटर्न N5 परिवार/उम्र-संबंधी शब्दावली "
        "के लिए मानक है।",

    # moji-6.3: add distractor-family detail + pedagogical purpose
    ("data/papers/moji/paper-6.json", "moji-6.3"):
        "道 (みち — रास्ता)। 道 N5 श्वेत-सूचीबद्ध कान्जी है (श्वेत-सूची "
        "पंक्ति 98) और vocabulary_n5.md में दर्ज है। विकर्षक 通 / 路 / 行 "
        "अर्थ-परिवार के विकल्प हैं जो प्रायः N4+ शब्दावली में दिखते हैं "
        "(通る / 通り 'गुजरना', 道路 / 路上 'सड़क', 行く 'जाना')। "
        "इस अर्थ-विकर्षक डिज़ाइन से जाँचा जाता है कि छात्र विशेष रूप से "
        "道 को पहचानता है या केवल 'रास्ता / दिशा' अर्थ-क्षेत्र को।",
}


def backup(path: Path) -> Path:
    bak = path.parent / f"{path.name}.bak_{TODAY}_moji_006_followup"
    if bak.exists():
        i = 2
        while True:
            alt = path.parent / f"{bak.name}_v{i}"
            if not alt.exists():
                bak = alt
                break
            i += 1
    shutil.copy2(path, bak)
    return bak


def main() -> None:
    applied = 0
    for (rel_path, qid), new_rh in EXTENSIONS.items():
        fp = ROOT / rel_path
        d = json.loads(fp.read_text(encoding="utf-8"))
        changed = False
        for q in d.get("questions", []):
            if q.get("id") == qid:
                if q.get("rationale_hi") != new_rh:
                    q["rationale_hi"] = new_rh
                    q["rationale_hi_provenance"] = "native_reviewed_2026_05_21"
                    changed = True
                break
        if changed:
            bak = backup(fp)
            fp.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n",
                          encoding="utf-8")
            applied += 1
            print(f"  WROTE {rel_path} :: {qid}  (backup: {bak.name})")
        else:
            print(f"  unchanged {rel_path} :: {qid}")
    print(f"\nApplied: {applied}/{len(EXTENSIONS)}")


if __name__ == "__main__":
    main()
