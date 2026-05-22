"""Close review §4 item 6 — refine pitch-accent annotations with the
reviewer's specific NHK 2016 citation claims.

The current native_review_note is generic ('differs from kanjium').
Refining to record:
  - The specific NHK 2016 drop value the reviewer cited
  - The sense / register the NHK value applies to (where the review
    distinguished, e.g., あなた generic-pronoun vs spousal-address)
  - audio_uses_drop = current drop (source of truth for rendered audio)
  - Honest provenance: "review-cited, pending NHK source verification"

DOES NOT change primary drop values — the reviewer is Claude (same
author), so elevating those claims to authoritative would be circular.
Future native-speaker pass (per NATIVE-SPEAKER-RE-VERIFICATION.md)
remains the gating step.

私 (わたし) confirmed correct (drop=0 matches NHK per review); not
re-annotated.
"""
import sys, io, os, shutil, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_22"

REFINEMENTS = {
    "あなた": {
        "nhk_2016_claim_drops_by_sense": {
            "generic_pronoun": 0,
            "spousal_address": 2,
        },
        "nhk_2016_claim_provenance": "review-cited 2026-05-22 (NTR-008 native-teacher review § 2.4); pending actual NHK 2016 source verification",
        "audio_uses_drop": 2,
        "native_review_note_v2": (
            "Reviewer-cited NHK 2016 distinguishes two senses for あなた: "
            "drop=0 (heiban) for the generic-pronoun sense; drop=2 (atamadaka) "
            "for the spousal-address sense. Current data lists drop=2 primary "
            "+ alternate [1]. The audio file (if rendered) is at drop=2; that "
            "value remains source of truth for rendered material. Native-"
            "speaker pass (per NATIVE-SPEAKER-RE-VERIFICATION.md) needed to "
            "resolve dictionary-vs-audio gap and decide whether to split the "
            "entry by sense."
        ),
    },
    "みなさん": {
        "nhk_2016_claim_drop": 3,
        "nhk_2016_claim_provenance": "review-cited 2026-05-22 (NTR-008 native-teacher review § 2.4); pending actual NHK 2016 source verification",
        "audio_uses_drop": 2,
        "native_review_note_v2": (
            "Reviewer-cited NHK 2016 lists drop=3 (nakadaka on 4th mora). "
            "Current data lists drop=2 (review notes this is heard "
            "regionally). If audio is rendered at drop=2, that value "
            "matches the audio. Native-speaker pass needed to confirm "
            "the standard dictionary value vs the regional/audio value."
        ),
    },
    "きのう": {
        "nhk_2016_claim_drop": 2,
        "nhk_2016_claim_alts": [0],
        "nhk_2016_claim_provenance": "review-cited 2026-05-22 (NTR-008 native-teacher review § 2.4); pending actual NHK 2016 source verification",
        "audio_uses_drop": 1,
        "native_review_note_v2": (
            "Reviewer-cited NHK 2016 lists drop=2 standard; drop=0 is "
            "the colloquial alternate. Current data lists drop=1 primary "
            "+ alternates [0, 2] — drop=1 is unusual as primary. The "
            "audio file (if rendered) is at drop=1; mark which value "
            "the audio uses. Native-speaker pass needed to resolve."
        ),
    },
}


def main():
    fp = os.path.join(REPO_N5, "data", "vocab.json")
    bak = fp + f".bak_{TODAY}_pitch_accent_nhk_refinement"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        v = json.load(f)
    vl = v if isinstance(v, list) else v.get("vocab", v.get("entries", []))

    touched = 0
    for entry in vl:
        if not isinstance(entry, dict): continue
        form = entry.get("form")
        if form in REFINEMENTS:
            pa = entry.get("pitch_accent")
            if not isinstance(pa, dict): continue
            r = REFINEMENTS[form]
            # Add specific NHK-claim fields
            for k, val in r.items():
                if k == "native_review_note_v2":
                    pa["native_review_note"] = val
                else:
                    pa[k] = val
            print(f"  {form}: pitch_accent annotation refined with NHK-claim specifics")
            touched += 1

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)

    print()
    print(f"=== Touched {touched} entries (expected 3: あなた, みなさん, きのう) ===")
    print("  Primary drop values UNCHANGED — reviewer is the same author; ")
    print("  elevating those NHK claims to authoritative would be circular.")
    print("  Future native-speaker pass remains the gating step.")
    print("  私 (drop=0) confirmed correct in review and NOT re-annotated.")


if __name__ == "__main__":
    main()
