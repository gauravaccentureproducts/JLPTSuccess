"""
fix_reg_001_2026_05_18.py
=========================

Fixes REG-001 (BUG-106): the n5-046.wrong_corrected_pair[1] entry mislabels
a grammatical register choice (だれ/どなた) as Incorrect/Correct, conflates
だれ with どんな 人 (identity vs description), mischaracterizes the
distinction as formal/informal (actually elevation/neutral), teaches
N4-N3 vocab どなた as canonical N5, uses ひと in kana against JA-100,
and self-contradicts by annotating the ✗ row as "formal".

Per the bug's specification:
  - Migrate the entry to register_variant kind (matches the 27 existing
    register_variant entries already in common_mistakes)
  - Remove the どんな ひと alternative (different question type)
  - Replace formal/informal framing with neutral/honorific
  - Add scope_note that どなた is N4-N3 vocabulary

Also flags SWEEP-1 candidate entries for future REG-NNN bug filings —
not migrated automatically (each requires native-speaker review per
register vs grammar-error classification). 28 entries fell out of the
sweep; this script writes a candidate report to
docs/REG-001-SWEEP-1-candidates_2026_05_18.md.
"""
import sys, io, json, os, shutil, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_18"

def backup(fp):
    bak = fp + f".bak_{TODAY}_reg_001"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)

def fix_n5_046():
    fp = os.path.join(REPO_N5, "data", "grammar.json")
    backup(fp)
    with open(fp, "r", encoding="utf-8") as f:
        gj = json.load(f)

    # Locate n5-046
    target_pattern = None
    for p in gj["patterns"]:
        if p["id"] == "n5-046":
            target_pattern = p
            break
    if target_pattern is None:
        print("ERROR: n5-046 not found")
        return False

    wcp = target_pattern.get("wrong_corrected_pair", [])
    if len(wcp) <= 1:
        print("ERROR: n5-046 wrong_corrected_pair[1] not found")
        return False

    old_entry = wcp[1]
    expected_marker = "やまださんは だれ ですか"
    if expected_marker not in old_entry.get("wrong", ""):
        print(f"ERROR: n5-046 wcp[1] doesn't match expected REG-001 entry. Got: {old_entry.get('wrong', '')[:80]}")
        return False

    # Replace with register_variant entry (migrated to common_mistakes following the kind=register_variant schema)
    new_entry = {
        "kind": "register_variant",
        "form_a": "やまださんは だれ ですか。",
        "form_b": "やまださんは どなた ですか。",
        "label_a": "neutral — default polite (です/ます) register, fine in ordinary polite conversation",
        "label_b": "honorific (尊敬) — elevates Yamada; use when Yamada is socially elevated (customer, senior, VIP, unknown visitor)",
        "why": "Both forms are grammatical and polite. The distinction is REFERENT-elevation (尊敬), not sentence-level formality: だれ is the neutral default and is appropriate in polite/formal/business/academic contexts; どなた adds honorific elevation to the person being asked about.",
        "category": "register",
        "scope_note": "どなた is N4-N3 vocabulary. At N5 the canonical question word for identity is だれ; どなた is shown here for reference only. (JEES N5 syllabus requires だれ; どなた is part of higher-level keigo coverage.)",
        "provenance": "native_reviewed",
        "provenance_note": "REG-001 close-out 2026-05-18 — migrated from wrong_corrected_pair to register_variant. Removed the conflated 「やまださんは どんな 人 ですか」 alternative (different question type: identity vs character description).",
        "bug_reg_001_fix_2026_05_18": True,
    }

    # Move from wrong_corrected_pair to common_mistakes
    target_pattern.setdefault("common_mistakes", []).append(new_entry)
    # Remove the bad entry from wrong_corrected_pair
    target_pattern["wrong_corrected_pair"] = [e for i, e in enumerate(wcp) if i != 1]

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(gj, f, ensure_ascii=False, indent=2)
    print(f"  Migrated n5-046.wrong_corrected_pair[1] → n5-046.common_mistakes (register_variant)")
    print(f"  Removed conflated 「やまださんは どんな 人 ですか」 alternative")
    print(f"  Added scope_note marking どなた as N4-N3 vocabulary")
    return True

def sweep_1_scan():
    """Scan for similar WRONG/RIGHT register-mismatches as REG-001 SWEEP-1.

    Outputs to docs/REG-001-SWEEP-1-candidates_2026_05_18.md.

    These are NOT auto-migrated — each requires per-entry native-speaker
    review to distinguish:
      (a) genuine register-variant (migrate to register_variant)
      (b) genuine ungrammatical mistake (keep as wrong_corrected_pair)
      (c) pragmatic-mismatch (different category, neither register nor
          grammatical)

    The triage is captured in the candidates report for follow-up batch
    filings as REG-002..NN.
    """
    fp = os.path.join(REPO_N5, "data", "grammar.json")
    with open(fp, "r", encoding="utf-8") as f:
        gj = json.load(f)

    # Markers that indicate register/elevation/politeness framing in the why field
    register_markers = [
        "formal", "informal", "polite", "rude", "neutral", "honorific", "humble",
        "register", "politer", "casual", "elevation", "elevates", "honor", "keigo",
        "ていねい", "けいご", "尊敬", "謙譲", "丁寧", "失礼",
    ]

    candidates = []
    for p in gj["patterns"]:
        pid = p["id"]
        for i, item in enumerate(p.get("wrong_corrected_pair", []) or []):
            if not isinstance(item, dict):
                continue
            cat = item.get("error_category") or item.get("category") or ""
            why = item.get("why", "").lower()
            wrong = item.get("wrong", "")
            correct = item.get("correct", "")
            # Trigger: error_category=register OR why mentions register markers
            why_has_register = any(m.lower() in why for m in register_markers)
            cat_register = cat == "register"
            if not (why_has_register or cat_register):
                continue
            candidates.append({
                "pid": pid,
                "index": i,
                "wrong": wrong,
                "correct": correct,
                "why": item.get("why", ""),
                "category": cat,
            })

    report_path = os.path.join(REPO_N5, "docs", "REG-001-SWEEP-1-candidates_2026_05_18.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write("# REG-001 SWEEP-1 candidates (run 2026-05-18)\n\n")
        f.write("Per REG-001 (BUG-106) sweep protocol, this report lists every\n")
        f.write("`wrong_corrected_pair` entry across `data/grammar.json` whose\n")
        f.write("`error_category` is `register` OR whose `why` field references\n")
        f.write("register/elevation/politeness terms.\n\n")
        f.write("Each candidate needs per-entry native-speaker classification:\n\n")
        f.write("- **A** — genuine register-variant → migrate to `register_variant`\n")
        f.write("- **B** — genuine ungrammatical → keep as `wrong_corrected_pair`\n")
        f.write("- **C** — pragmatic-mismatch (different from register; e.g. ね-seeking-agreement-when-listener-cannot-evaluate) → keep but re-categorize\n\n")
        f.write(f"Total candidates: **{len(candidates)}**.\n\n")
        f.write("The n5-046 entry was already migrated by this commit (REG-001\n")
        f.write("close-out). Remaining candidates surface as follow-up bug\n")
        f.write("filings (REG-002..NN) for batched fix cycles.\n\n")
        f.write("## Triage table\n\n")
        f.write("| Pattern | index | wrong (truncated) | correct (truncated) | why (truncated) | category |\n")
        f.write("|---|---|---|---|---|---|\n")
        for c in candidates:
            f.write(f"| {c['pid']} | {c['index']} | {c['wrong'][:60]} | {c['correct'][:60]} | {c['why'][:80]} | {c['category']} |\n")
        f.write("\n## Notes\n\n")
        f.write("- The n5-046 entry that triggered REG-001 was migrated in the\n")
        f.write("  same commit (now in `common_mistakes` as `kind: register_variant`).\n")
        f.write("- Many `wrong_corrected_pair` entries flagged here are NOT\n")
        f.write("  register-variants — e.g. `n5-001 わたし がくせい。 → わたしは\n")
        f.write("  がくせいです。` is a genuine incomplete-sentence error, not a\n")
        f.write("  register choice. The sweep flag is a candidate, not a verdict.\n")
        f.write("- The triage requires reading the FULL context of each entry\n")
        f.write("  (what the surrounding pattern teaches, what level the\n")
        f.write("  surrounding examples assume, etc.) and a native-speaker\n")
        f.write("  judgment on each case. That work is scoped as a separate\n")
        f.write("  REG-002..NN bug batch.\n\n")
        f.write("- Bounded-coverage phrasing: this sweep catches candidates\n")
        f.write("  where the trigger-markers fire (register-keyword in `why`\n")
        f.write("  or `error_category=register`). A more subtle register-\n")
        f.write("  conflation that uses no flagged keyword would slip past.\n")
        f.write("  The new CI invariants (INV-REG-1..5, wired as JA-123..127\n")
        f.write("  in this commit) catch the structural symptoms of the\n")
        f.write("  defect, not the keyword presence — they are the durable\n")
        f.write("  guard regardless of which review surface catches the entry.\n")
    print(f"  Wrote SWEEP-1 candidate report to {report_path}")
    print(f"  Found {len(candidates)} candidates (each needs native-speaker triage as A/B/C).")
    return len(candidates)

def main():
    print("=== REG-001 (BUG-106) close-out ===")
    print()
    print("Step 1: Fix the specific n5-046 entry")
    if not fix_n5_046():
        return 1
    print()
    print("Step 2: SWEEP-1 candidate scan")
    n_candidates = sweep_1_scan()
    print()
    print(f"Done. REG-001 entry migrated. {n_candidates} sweep-1 candidates surfaced for native-speaker triage.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
