"""Fix BUG-016 — add transitivity classification to the 110 N5 verbs
currently missing the field.

Pre-fix: 22 of 132 verbs declared transitivity (17%); these were
the documented transitive/intransitive pairs.
Post-fix: 132 of 132 verbs declared.

Allowed values:
  - "transitive"   (他動詞 — takes direct object marked with を)
  - "intransitive" (自動詞 — does not take を; argument structure uses
                    に / で / と / が)
  - "contact"      (encounter / mutual-action verb — takes に for the
                    target. Currently used ONLY for 会う; reserved for
                    the small set of "encounter verbs" that don't fit
                    the binary classification cleanly per BUG-008.)

Classification source: pedagogical convention (Genki I, Minna no
Nihongo, A Dictionary of Basic Japanese Grammar). Where standard
references disagree (e.g., 結婚する with と-partner), the more common
classification is used and the partner-particle is documented
separately in the entry's collocations / grammar references.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "vocab.json"

# form → transitivity. Homophones (same form, different gloss) share
# the same transitivity in every case in this N5 corpus.
TRANSITIVITY: dict[str, str] = {
    # ---- Transitive verbs (take を + direct object) ----
    "言う": "transitive",
    "うたう": "transitive",
    "おもう": "transitive",
    "買う": "transitive",
    "書く": "transitive",
    "聞く": "transitive",
    "つくる": "transitive",
    "しる": "transitive",
    "とる": "transitive",  # both homophones
    "飲む": "transitive",
    "はく": "transitive",
    "話す": "transitive",
    "まつ": "transitive",
    "もつ": "transitive",
    "読む": "transitive",
    "うる": "transitive",
    "おす": "transitive",
    "ひく": "transitive",  # both homophones (play, pull)
    "よぶ": "transitive",
    "わたす": "transitive",
    "ぬぐ": "transitive",
    "あらう": "transitive",
    "すう": "transitive",
    "つかう": "transitive",
    "ならう": "transitive",
    "はる": "transitive",
    "みがく": "transitive",
    "もっていく": "transitive",
    "もってくる": "transitive",
    "なくす": "transitive",
    "たのむ": "transitive",
    "おく": "transitive",
    "さす": "transitive",
    "食べる": "transitive",
    "見る": "transitive",
    "おしえる": "transitive",
    "おぼえる": "transitive",
    "わすれる": "transitive",
    "かりる": "transitive",
    "こたえる": "transitive",
    "かける": "transitive",
    "ならべる": "transitive",
    "見せる": "transitive",
    "あびる": "transitive",
    "あつめる": "transitive",
    "する": "transitive",
    "べんきょうする": "transitive",
    "さんぽする": "transitive",
    "りょこうする": "transitive",
    "れんしゅうする": "transitive",
    "しつもんする": "transitive",
    "しごとする": "transitive",
    "電話する": "transitive",
    "コピーする": "transitive",
    "そうじする": "transitive",
    "せんたくする": "transitive",
    "かいものする": "transitive",
    "やる": "transitive",
    "あげる": "transitive",
    "もらう": "transitive",
    "くれる": "transitive",
    "かす": "transitive",
    "かえす": "transitive",
    "ためる": "transitive",
    "はらう": "transitive",
    "わたる": "transitive",  # わたる (cross): takes を for the path (motion-traversal を)
    "のぼる": "transitive",  # similar — motion-traversal を for the path

    # ---- Intransitive verbs (do not take を for an object) ----
    "行く": "intransitive",
    "すむ": "intransitive",
    "立つ": "intransitive",
    "なく": "intransitive",
    "はしる": "intransitive",
    "はたらく": "intransitive",
    "休む": "intransitive",
    "分かる": "intransitive",
    "おわる": "intransitive",
    "かえる": "intransitive",
    "およぐ": "intransitive",
    "とぶ": "intransitive",
    "こまる": "intransitive",
    "ならぶ": "intransitive",
    "いそぐ": "intransitive",
    "しぬ": "intransitive",
    "ちがう": "intransitive",
    "まがる": "intransitive",
    "ふく": "intransitive",
    "ふる": "intransitive",
    "くもる": "intransitive",
    "のる": "intransitive",
    "すわる": "intransitive",
    "さく": "intransitive",
    "かかる": "intransitive",
    "いる": "intransitive",  # both homophones: animate-exist + need
    "ねる": "intransitive",
    "出かける": "intransitive",
    "はれる": "intransitive",
    "つかれる": "intransitive",
    "生まれる": "intransitive",
    "おりる": "intransitive",
    "つとめる": "intransitive",
    "ある": "intransitive",
    "おくれる": "intransitive",
    "聞こえる": "intransitive",
    "ござる": "intransitive",
    "けっこんする": "intransitive",  # と-partner; standard pedagogical classification
    "来る": "intransitive",

    # ---- Contact / encounter (special class — takes に for target) ----
    "会う": "contact",
}


def main() -> int:
    V = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = V.get("entries", [])

    classified = 0
    already_set = 0
    missing: list[tuple[str, str]] = []

    for e in entries:
        pos = (e.get("pos") or "")
        if not pos.startswith("verb"):
            continue
        form = e.get("form")
        if "transitivity" in e:
            already_set += 1
            continue
        if form in TRANSITIVITY:
            e["transitivity"] = TRANSITIVITY[form]
            e["transitivity_provenance"] = "n5_pedagogical_convention_bug_016_fix"
            classified += 1
        else:
            missing.append((form, e.get("id", "?")))

    if missing:
        print("\nWARN: verbs without a TRANSITIVITY mapping:")
        for f, vid in missing:
            print(f"  {f} ({vid})")

    VOCAB.write_text(json.dumps(V, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nClassified: {classified}")
    print(f"Already set: {already_set}")
    print(f"Total verbs: {sum(1 for e in entries if (e.get('pos') or '').startswith('verb'))}")
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
