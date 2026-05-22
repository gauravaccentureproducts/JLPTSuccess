"""Close S3 batch: NTR-010/011/012/013.

NTR-010 (BUG-170): q-0226 explanation_en — append は-contrast note
NTR-011 (BUG-171): pronoun `collocations` mechanically generated → rename field
NTR-012 (BUG-172): 七 reading_rule — add なな-usage note
NTR-013 (BUG-173): pronoun counter cleanup (drop on collective pronouns; fix みなさん typo)
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
    # --- NTR-010: q-0226 explanation_en append ---
    qfp = os.path.join(REPO_N5, "data", "questions.json")
    backup(qfp, "ntr_010")
    with open(qfp, "r", encoding="utf-8") as f:
        qd = json.load(f)
    qlist = qd if isinstance(qd, list) else qd.get("questions", [])
    for q in qlist:
        if isinstance(q, dict) and q.get("id") == "q-0226":
            old = q.get("explanation_en") or ""
            note = (" Note: は after a time noun introduces contrast "
                    "('yesterday in particular' — implying other days are different). "
                    "Fine here, but typical neutral past-negative would drop the particle "
                    "(きのう ばんごはんを 食べませんでした) or use 'に'.")
            if note.strip() not in old:
                q["explanation_en"] = old.rstrip() + note
                q["explanation_provenance"] = "native_reviewed_2026_05_22"
                print(f"  NTR-010: q-0226 explanation_en appended with は-contrast note")
            break

    with open(qfp, "w", encoding="utf-8") as f:
        json.dump(qd, f, ensure_ascii=False, indent=2)

    # --- NTR-011 + NTR-013: vocab.json edits ---
    vfp = os.path.join(REPO_N5, "data", "vocab.json")
    backup(vfp, "ntr_011_013")
    with open(vfp, "r", encoding="utf-8") as f:
        v = json.load(f)
    vl = v if isinstance(v, list) else v.get("vocab", v.get("entries", []))

    # NTR-011: rename `collocations` → `particle_examples` on pronoun entries
    # (mechanically generated particle-template substitution, not real collocation data)
    # Scope: section "1. People - Pronouns and Self"
    renamed = 0
    counter_drop = 0
    counter_typo_fix = 0
    for entry in vl:
        if not isinstance(entry, dict): continue
        section = entry.get("section") or ""
        form = entry.get("form") or ""
        # NTR-011: pronoun collocations rename
        if section.startswith("1. People - Pronouns and Self") and "collocations" in entry:
            entry["particle_examples"] = entry.pop("collocations")
            entry["particle_examples_provenance"] = (
                "native_reviewed_2026_05_22 (NTR-011: renamed from `collocations`; "
                "these are particle-template-illustrative, not real corpus-linguistics "
                "collocations. Real collocations can override this field where they exist.)"
            )
            renamed += 1

        # NTR-013: pronoun counter cleanup
        # - Fix typo: みなさん.counter.reading should be 'にん' not '人'
        # - For collective pronouns (私たち, みなさん): the counter
        #   applies to the noun-of-reference, not the pronoun itself.
        #   Annotate with a note rather than silently dropping (preserves
        #   ID-shape; downstream consumers can decide whether to render).
        if isinstance(entry.get("counter"), dict):
            c = entry["counter"]
            if form == "みなさん" and c.get("reading") == "人":
                c["reading"] = "にん"
                counter_typo_fix += 1
                print(f"  NTR-013 (a): みなさん.counter.reading '人' → 'にん' (typo fix)")
            if form in ("私たち", "みなさん"):
                # Annotate that the counter applies to the noun-of-reference, not the pronoun
                c["applies_to"] = "noun_of_reference"
                c["note"] = (
                    "Counter 人/にん applies to the people the pronoun refers to, "
                    "not to the pronoun itself. (We don't count 'we's' / 'みなさん's.) "
                    "UI may choose to suppress counter display for collective pronouns."
                )
                counter_drop += 1
                print(f"  NTR-013 (b): {form}.counter annotated applies_to='noun_of_reference'")

    with open(vfp, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)
    print(f"  NTR-011: renamed `collocations` → `particle_examples` on {renamed} pronoun entries")

    # --- NTR-012: 七 reading_rule append ---
    kfp = os.path.join(REPO_N5, "data", "kanji.json")
    backup(kfp, "ntr_012")
    with open(kfp, "r", encoding="utf-8") as f:
        kd = json.load(f)
    kl = kd.get("entries", kd if isinstance(kd, list) else kd.get("kanji", []))
    for entry in kl:
        if not isinstance(entry, dict): continue
        if entry.get("glyph") == "七":
            old_rule = entry.get("reading_rule") or ""
            usage_note = (
                " Usage note (2026-05-22): なな is heard in ordering/listing contexts "
                "(especially to disambiguate from いち over the phone); しち in fixed "
                "time/date compounds (七時 しちじ, 七月 しちがつ). NHK uses なな when "
                "reading numerals aloud. 七人 takes either reading (しちにん or ななにん); "
                "七つ is exclusively ななつ. For phone/list disambiguation, prefer なな."
            )
            if usage_note.strip() not in old_rule:
                entry["reading_rule"] = old_rule.rstrip() + usage_note
                entry["reading_rule_provenance"] = "native_reviewed_2026_05_22"
                print(f"  NTR-012: 七 reading_rule appended with なな-usage note")
            break
    with open(kfp, "w", encoding="utf-8") as f:
        json.dump(kd, f, ensure_ascii=False, indent=2)

    print()
    print("=== Done ===")
    print(f"  NTR-010: q-0226 explanation_en + は-contrast note")
    print(f"  NTR-011: {renamed} pronouns: collocations → particle_examples (terminology fix)")
    print(f"  NTR-012: 七 reading_rule + なな-usage note")
    print(f"  NTR-013: {counter_typo_fix} typo fix + {counter_drop} collective-pronoun counter annotations")


if __name__ == "__main__":
    main()
