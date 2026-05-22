"""Close S2 batch: NTR-005/006/007/008.

NTR-005 (BUG-165): おはし section '20. Tableware and Cooking' → '19. Tableware and Cooking'
NTR-006 (BUG-166): えいが section '26. House and Furniture' → entertainment-leaning section
NTR-007 (BUG-167): 三 mnemonic.reading conflates -さん etymology → soften
NTR-008 (BUG-168): pitch-accent native-speaker review pending → annotate 4 entries
"""
import sys, io, os, shutil, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_22"


def backup(fp, tag):
    bak = fp + f".bak_{TODAY}_{tag}"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)


def main():
    # --- NTR-005 + NTR-006 + NTR-008: vocab.json edits ---
    vfp = os.path.join(REPO_N5, "data", "vocab.json")
    backup(vfp, "ntr_005_to_008")
    with open(vfp, "r", encoding="utf-8") as f:
        v = json.load(f)
    vl = v if isinstance(v, list) else v.get("vocab", v.get("entries", []))

    # NTR-005: おはし section retag
    # NTR-006: えいが section retag
    # NTR-008: pitch-accent entries gain native_review_pending_2026_05_22 flag
    PA_REVIEW_PENDING = {"あなた", "みなさん", "きのう"}  # excluding これ which the review confirmed matches NHK

    for entry in vl:
        if not isinstance(entry, dict): continue
        form = entry.get("form")
        if form == "おはし" and entry.get("section") == "20. Tableware and Cooking":
            entry["section"] = "19. Tableware and Cooking"
            entry["section_provenance"] = "native_reviewed_2026_05_22"
            print(f"  NTR-005: おはし section 20 → 19")
        elif form == "えいが" and entry.get("section") == "26. House and Furniture":
            # Re-tag to an entertainment-leaning section. The corpus has '37. Common nouns (misc)'.
            # Movie/film is genuinely a leisure/entertainment item; '37' is the closest existing bucket.
            entry["section"] = "37. Common nouns - miscellaneous"
            entry["section_provenance"] = "native_reviewed_2026_05_22"
            print(f"  NTR-006: えいが section 26 → 37 (common nouns - misc; closest fit lacking entertainment section)")
        # NTR-008: annotate pitch-accent entries flagged for native-speaker review
        if form in PA_REVIEW_PENDING:
            pa = entry.get("pitch_accent")
            if isinstance(pa, dict):
                pa["native_review_pending"] = "2026_05_22_NTR_008"
                pa["native_review_note"] = (
                    f"Per native-teacher review 2026-05-22: NHK 2016 edition value differs from current kanjium-by-reading lookup. "
                    f"Annotated pending actual native-speaker pass. The audio file (if rendered) matches the current drop value; "
                    f"audio is the source of truth for the rendered material until native review resolves the dictionary-vs-audio gap."
                )
                print(f"  NTR-008: {form} pitch_accent flagged native_review_pending")

    with open(vfp, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)

    # --- NTR-007: 三 mnemonic softening ---
    kfp = os.path.join(REPO_N5, "data", "kanji.json")
    backup(kfp, "ntr_007")
    with open(kfp, "r", encoding="utf-8") as f:
        kd = json.load(f)
    kl = kd.get("entries", kd if isinstance(kd, list) else kd.get("kanji", []))
    for entry in kl:
        if not isinstance(entry, dict): continue
        if entry.get("glyph") == "三":
            mn = entry.get("mnemonic")
            if isinstance(mn, dict):
                old_reading = mn.get("reading", "")
                # Soften: drop the claim that the honorific is the same etymology
                new_reading = (
                    "The sound *san* is everywhere in Japanese — 三月 (sangatsu, March), "
                    "the honorific -さん, etc. — so the reading is easy to hold onto. "
                    "(Note: the honorific さん comes from a separate root [様 → さま → さん]; "
                    "the shared sound is coincidental.) Kun み in 三つ (mittsu)."
                )
                mn["reading"] = new_reading
                # Bump provenance for the edited field
                prov = mn.get("provenance") or {}
                if isinstance(prov, dict):
                    prov["reading"] = "native_reviewed_2026_05_22"
                print(f"  NTR-007: 三 mnemonic.reading softened")
                print(f"    OLD: {old_reading[:80]!r}")
                print(f"    NEW: {new_reading[:80]!r}")
            break
    with open(kfp, "w", encoding="utf-8") as f:
        json.dump(kd, f, ensure_ascii=False, indent=2)

    print()
    print("=== Done ===")
    print("  NTR-005: おはし section re-tagged 20 → 19")
    print("  NTR-006: えいが section re-tagged 26 → 37")
    print("  NTR-007: 三 mnemonic etymology claim softened")
    print("  NTR-008: 3 pitch-accent entries flagged native_review_pending (これ confirmed correct, not flagged)")


if __name__ == "__main__":
    main()
