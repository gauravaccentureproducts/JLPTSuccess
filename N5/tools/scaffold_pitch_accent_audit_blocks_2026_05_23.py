"""Scaffold pitch-accent audit blocks for the 3 entries the
2026-05-23 reviewer task flagged for native-speaker verification.

This script ADDS the audit-block schema; it does NOT populate the
verification result fields. Those are explicitly left for a real
human native speaker (per F.44.7 / F.44.15 Shape 2 / NATIVE-SPEAKER-
RE-VERIFICATION.md discipline).

The audit block carries:
  - verifier_pending: true (flag — JA-155 triggers when an entry's
    match_kind='exact' lacks this resolved)
  - pending_since: 2026-05-23
  - pending_wave: "pitch-accent-native-verify-2026-05-23"
  - current_state_at_audit_request: snapshot of drops + match_kind
    so the reviewer can see what they're verifying against
  - review_question: per-entry question lifted from the task
    description verbatim
  - verification_protocol_link: pointer to NATIVE-SPEAKER-RE-
    VERIFICATION.md's pitch-accent protocol section
  - result_schema: blank fields the human verifier fills in

Cross-update vocab.json side: the existing
pitch_accent.native_review_pending field is updated to point at
this audit block.
"""
import sys, io, os, json, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_23"

PENDING_WAVE = "pitch-accent-native-verify-2026-05-23"
PROTOCOL_LINK = "docs/NATIVE-SPEAKER-RE-VERIFICATION.md#pitch-accent-protocol-2026-05-23"

REVIEW_QUESTIONS = {
    "みなさん": (
        "NHK lists ③ as well-known standard. Is the data choice of ② "
        "the one our voice actor recorded? If audio uses ③, update "
        "drops to [3] or [3, 2]."
    ),
    "あなた": (
        "NHK 2016 lists ⓪ as the generic-pronoun form and ② as the "
        "address-spouse form. The data has ② primary and ① alternate — "
        "neither matches the ⓪ heiban-pronoun NHK reading. Three "
        "possibilities: (a) NHK has updated since the data was sourced — "
        "verify in current edition. (b) Our voice actor uses the ② "
        "address-pronoun consistently across all contexts (acceptable "
        "but should be documented). (c) Data is wrong — replace with "
        "[0] or [0, 2]."
    ),
    "きのう": (
        "NHK lists ② as standard. Three drops listed is generous. "
        "Confirm whether the audio recording uses ②, and if so, "
        "reorder to put 2 first (drops[0] is treated as primary by "
        "the UI per the schema)."
    ),
}


def build_audit_block(form, current_drops, current_match_kind):
    return {
        "verifier_pending": True,
        "pending_since": "2026-05-23",
        "pending_wave": PENDING_WAVE,
        "current_state_at_audit_request": {
            "drops": list(current_drops),
            "match_kind": current_match_kind,
        },
        "review_question": REVIEW_QUESTIONS[form],
        "verification_protocol_link": PROTOCOL_LINK,
        "verification_required_against": [
            "NHK 日本語発音アクセント新辞典 (2016) — cite page + drop notation if conflicting",
            "Audio recordings — for this corpus, per-vocab pitch audio does NOT exist as standalone files. The word must be located within listening passages (audio_manifest_voice.json / data/listening.json entries) where it occurs in script_ja. Note timestamp + passage_id when verifying.",
        ],
        "verifier_credential_required": (
            "Native Japanese speaker OR certified Japanese-language teacher "
            "(CIJL / 日本語教師 marketplace / Upwork JLPT-instructor pool acceptable). "
            "LLM-only verification is explicitly REJECTED per F.44.7 + F.44.15 "
            "Shape 2 circular-authority discipline."
        ),
        "result_schema": {
            "_doc": (
                "Human verifier fills these fields. When all are populated and "
                "verifier_pending is flipped to false, JA-155 unblocks promotion "
                "of match_kind from 'by-reading' to 'exact'."
            ),
            "verified_against": None,
            "verified_at": None,
            "verifier_credential": None,
            "verified_drops": None,
            "verified_match_kind": None,
            "decision_note": None,
            "audio_passage_reference": None,
            "nhk_page_reference": None,
        },
    }


def update_pitch_accent_reference():
    fp = os.path.join(REPO_N5, "data", "n5_pitch_accent_reference.json")
    bak = fp + f".bak_{TODAY}_pitch_accent_audit_scaffold"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    entries = d["entries"]
    touched = 0
    for e in entries:
        if not isinstance(e, dict): continue
        f_ = e.get("form")
        if f_ in REVIEW_QUESTIONS and e.get("match_kind") == "by-reading":
            e["audit"] = build_audit_block(f_, e.get("drops") or [], e.get("match_kind"))
            print(f"  n5_pitch_accent_reference.json {f_!r}: audit block added (verifier_pending=true)")
            touched += 1
    # Add wave to _meta
    if isinstance(d.get("_meta"), dict):
        d["_meta"].setdefault("audit_waves", []).append({
            "wave": PENDING_WAVE,
            "scope": "3 by-reading entries flagged by 2026-05-23 reviewer task",
            "entries": list(REVIEW_QUESTIONS.keys()),
            "scaffold_landed": "2026-05-23",
            "discipline": (
                "Scaffold-only — verification fields blank pending real human "
                "native-speaker review. F.44.7 + F.44.15 Shape 2 prohibit LLM-"
                "authored verification (circular authority)."
            ),
            "broader_pass_queue": "see tools/build_pitch_accent_by_reading_queue_2026_05_23.py output",
        })
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"  Touched {touched} entries in n5_pitch_accent_reference.json")


def update_vocab_cross_reference():
    """Update vocab.json side: bump native_review_pending wave ID."""
    fp = os.path.join(REPO_N5, "data", "vocab.json")
    bak = fp + f".bak_{TODAY}_pitch_accent_audit_xref"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        v = json.load(f)
    vl = v if isinstance(v, list) else v.get("vocab", v.get("entries", []))
    touched = 0
    for e in vl:
        if not isinstance(e, dict): continue
        f_ = e.get("form")
        if f_ in REVIEW_QUESTIONS:
            pa = e.get("pitch_accent")
            if isinstance(pa, dict):
                pa["native_review_pending_wave"] = PENDING_WAVE
                pa["native_review_audit_block_at"] = f"data/n5_pitch_accent_reference.json → form={f_!r}"
                print(f"  vocab.json {f_!r}: cross-reference pointer added to audit block")
                touched += 1
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)
    print(f"  Touched {touched} entries in vocab.json")


def main():
    update_pitch_accent_reference()
    update_vocab_cross_reference()
    print()
    print("=== Scaffold complete ===")
    print("3 audit blocks added with verifier_pending=true; vocab.json cross-references updated.")
    print("Verification fields are explicitly BLANK pending real human native-speaker review.")
    print("See NATIVE-SPEAKER-RE-VERIFICATION.md#pitch-accent-protocol-2026-05-23 for the protocol.")


if __name__ == "__main__":
    main()
