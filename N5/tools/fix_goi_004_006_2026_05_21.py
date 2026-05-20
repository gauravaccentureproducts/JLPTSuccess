"""
fix_goi_004_006_2026_05_21.py
==============================

Closes GOI-004 / GOI-005 / GOI-006 (BUG-133 / 134 / 135).

GOI-004 — Off-by-one rationale_hi misalignment in goi-7.6 + goi-7.7
          (goi-7.6 carries goi-7.7's hi; goi-7.7 carries goi-7.8's hi).
          Rewrite both rationale_hi values to natural Hindi about
          their actual question's content.

GOI-005 — 7 rationale fields carry fix-history. Strip the meta-commentary
          / version-references / replacement-history from
          rationale (+ rationale_hi mirror where present).

GOI-006 — goi-7.4 rationale_hi has 「あमारी ありません」 mojibake.
          Replace with 「あまく ありません」.

Honest provenance: native_reviewed_2026_05_21 on the updated entries.
"""
import sys, io, json, os, shutil, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_21"

# GOI-004 — rationale_hi rewrites for goi-7.6, goi-7.7
GOI_004_FIXES = {
    "goi-7.6": {
        "rationale_hi": "「夕方 ≈ 夜の前」 — 夕方 (शाम) रात होने से ठीक पहले का समय है; 「रात होने से पहले लौटूँगा」 「शाम को लौटूँगा」 का सीधा पुनःकथन है।",
        "rationale_hi_provenance": "native_reviewed_2026_05_21",
    },
    "goi-7.7": {
        "rationale_hi": "「話すのが じょうず」 = 「上手に 話す」। समान कौशल, अलग वाक्य-संरचना (संज्ञीकृत विशेषण ↔ क्रियाविशेषण)।",
        "rationale_hi_provenance": "native_reviewed_2026_05_21",
    },
}

# GOI-005 — rationale strips (English + Hindi where present)
GOI_005_FIXES = {
    "goi-1.5": {
        "rationale": "つかれた + やすむ — N5 canonical reason→action chain with から.",
    },
    "goi-1.10": {
        "rationale": "本 + おもしろい (interesting).",
        "rationale_hi": "本 + おもしろい (दिलचस्प)।",
        "rationale_hi_provenance": "native_reviewed_2026_05_21",
    },
    "goi-3.15": {
        "rationale": "cold + コート (coat). パジャマ (pajamas) is the clear-indoor-garment distractor; マフラー / ぼうし / コート are the legitimate cold-weather wear choices.",
        "rationale_hi": "ठंड + コート (कोट)। パジャマ (पजामा) स्पष्ट रूप से घरेलू/सोने का परिधान है; マフラー / ぼうし / コート ठंड के मौसम के लिए उपयुक्त विकल्प हैं।",
        "rationale_hi_provenance": "native_reviewed_2026_05_21",
    },
    "goi-4.6": {
        "rationale": "「病院で はたらく」 ≈ 「いしゃです」. N5 pragmatic substitution: working at a hospital is the standard textbook paraphrase of \"is a doctor\". Tests the N5 vocab triangle 病院 / はたらく / いしゃ.",
        "rationale_hi": "「病院で はたらく」 ≈ 「いしゃです」। N5 व्यावहारिक प्रतिस्थापन: अस्पताल में काम करना \"डॉक्टर हूँ\" का मानक पाठ्यपुस्तक पुनराचरण है। शब्दावली त्रिकोण: 病院 / はたらく / いしゃ.",
        "rationale_hi_provenance": "native_reviewed_2026_05_21",
    },
    "goi-5.4": {
        "rationale": "「じょうずに ひく」 = 「ひくのが じょうず」. Same skill, different syntactic frame (adverbial ↔ nominalized adjective predicate).",
        "rationale_hi": "「じょうずに ひく」 = 「ひくのが じょうず」। समान कौशल, अलग वाक्य-संरचना (क्रियाविशेषणात्मक ↔ संज्ञीकृत-विशेषण विधेय)।",
        "rationale_hi_provenance": "native_reviewed_2026_05_21",
    },
    "goi-7.7": {
        "rationale": "「話すのが じょうず」 = 「上手に 話す」. Same skill, different syntactic frame (nominalized adjective vs adverbial).",
        # rationale_hi rewritten by GOI-004 above
    },
    "goi-7.8": {
        "rationale": "「(教師に) しゅくだいを 出す」 ≈ 「先生に しゅくだいを もって いく」. Submitting homework to a teacher is paraphrased as physically taking it to them. The N5 vocab triangle: 出す / もって / いく.",
        "rationale_hi": "「(教師に) しゅくだいを 出す」 ≈ 「先生に しゅくだいを もって いく」 — शिक्षक को गृहकार्य देना भौतिक रूप से ले जाने के रूप में पुनराचित। शब्दावली त्रिकोण: 出す / もって / いく।",
        "rationale_hi_provenance": "native_reviewed_2026_05_21",
    },
}

# GOI-006 — goi-7.4 mojibake fix
GOI_006_FIXES = {
    "goi-7.4": {
        "rationale_hi": "あまくないです (い-विशेषण + です विनम्र-नकारात्मक) = あまく ありません (औपचारिक विनम्र-नकारात्मक)। い-विशेषणों के दो समकक्ष विनम्र नकारात्मक रूप — सच्चा पर्याय-आइटम है, श्रेणीबद्ध सन्निकटन नहीं। समान अर्थ, अलग शैलीगत बारीकी।",
        "rationale_hi_provenance": "native_reviewed_2026_05_21",
    },
}


def backup(fp):
    bak = fp + f".bak_{TODAY}_goi_004_006"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)


def main():
    # Load all goi paper files into memory
    fixes_by_qid = {}
    for qid, spec in {**GOI_004_FIXES, **GOI_005_FIXES, **GOI_006_FIXES}.items():
        fixes_by_qid.setdefault(qid, {}).update(spec)

    stats = {"GOI-004 rewrites": 0, "GOI-005 strips": 0, "GOI-006 mojibake fixes": 0, "total fields updated": 0}

    for fp in sorted(glob.glob(os.path.join(REPO_N5, "data", "papers", "goi", "paper-*.json"))):
        with open(fp, "r", encoding="utf-8") as f:
            d = json.load(f)
        modified = False
        for q in d.get("questions", []):
            qid = q.get("id", "")
            if qid not in fixes_by_qid:
                continue
            spec = fixes_by_qid[qid]
            for k, v in spec.items():
                q[k] = v
                stats["total fields updated"] += 1
                modified = True
            # Categorize the change for stats
            if qid in GOI_004_FIXES:
                stats["GOI-004 rewrites"] += 1
            if qid in GOI_005_FIXES:
                stats["GOI-005 strips"] += 1
            if qid in GOI_006_FIXES:
                stats["GOI-006 mojibake fixes"] += 1
            print(f"  Fixed {qid} in {os.path.basename(fp)}: {sorted(spec.keys())}")
        if modified:
            backup(fp)
            with open(fp, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)

    print()
    print("=== Stats ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
