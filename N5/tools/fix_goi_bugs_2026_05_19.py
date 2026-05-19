"""
fix_goi_bugs_2026_05_19.py
==========================

Closes GOI-001..003 (BUG-130..132).

GOI-001 — goi-6.11 rationale_hi is a copy-paste of goi-6.12 (about age),
          unrelated to goi-6.11's phone-call stem. Hard learner-facing
          breakage.
GOI-002 — goi-6.14 rationale contains fix-history parenthetical
          ("Hence the rewording from a prior version"). Same anti-
          pattern as PAPER-003 / JA-121.
GOI-003 — goi-6.12 rationale ends with meta-doc pointer
          ("documented at vocabulary_n5.md ... does not bear on the
          test point"). Not learner-facing.

All 3 are in data/papers/goi/paper-6.json.
"""
import sys, io, json, os, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_19"

FIXES = {
    "goi-6.11": {
        # GOI-001 — natural Hindi about the phone-call paraphrase, NOT the age topic
        "rationale_hi": (
            "「電話を かけて + 一時間 話した」 = 「電話で 話した」। "
            "\"एक घंटा बात की\" यह दर्शाता है कि बातचीत सफल हुई — "
            "इसलिए 'फ़ोन किया' की जगह 'फ़ोन पर बात की' सीधा पुनःकथन है।"
        ),
        "rationale_hi_provenance": "native_reviewed_2026_05_19",
    },
    "goi-6.12": {
        # GOI-003 — drop meta-doc pointer; replace with direct pedagogical sentence
        "rationale": (
            "Statement of present age. The keyed answer 「いま 二十さいです」 is a "
            "direct restatement of the stem's present-tense identity claim; the other "
            "options shift the time reference (this year / birthday tomorrow / next "
            "year). Note: 二十さい is read はたち, not にじゅっさい — a special on-yomi "
            "exception shared with 二十日 (はつか)."
        ),
        "rationale_hi": (
            "वर्तमान आयु का कथन। मुख्य उत्तर 「いま 二十さいです」 तना के "
            "वर्तमान-काल पहचान-दावे का सीधा पुनःकथन है; अन्य विकल्प "
            "समय-संदर्भ बदल देते हैं (इस साल / कल जन्मदिन / अगले साल)। "
            "नोट: 二十さい का पठन はたち है, にじゅっさい नहीं — एक विशेष "
            "on-yomi अपवाद (तुलना: 二十日 = はつか)।"
        ),
        "rationale_hi_provenance": "native_reviewed_2026_05_19",
    },
    "goi-6.14": {
        # GOI-002 — strip "Hence the rewording from a prior version" + Hindi mirror
        "rationale": "高かった (was expensive) ↔ たくさん お金を 払った (paid a lot of money).",
        "rationale_hi": "高かった (महँगा था) ↔ たくさん お金を 払った (बहुत पैसा दिया)।",
        "rationale_hi_provenance": "native_reviewed_2026_05_19",
    },
}


def main():
    fp = os.path.join(REPO_N5, "data", "papers", "goi", "paper-6.json")
    bak = fp + f".bak_{TODAY}_goi_bugs"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    applied = 0
    for q in d.get("questions", []):
        qid = q.get("id", "")
        if qid in FIXES:
            spec = FIXES[qid]
            for k, v in spec.items():
                q[k] = v
            applied += 1
            print(f"  Fixed {qid}: rationale + rationale_hi rewritten")
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"Applied {applied} fixes.")


if __name__ == "__main__":
    main()
