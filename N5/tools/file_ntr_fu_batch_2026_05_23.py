"""File NTR-FU-001 / NTR-FU-002 / NTR-FU-003 in the bug tracker.

Three bugs registered as broader-scope follow-ups to NTR batch
items where the original close scope was bounded and the user's
re-paste of the review (2026-05-23) flagged remaining work.

Verification per F.41.4:
  - NTR-FU-001 (whitelist mismatch): 11 vocab forms (kana-only +
    katakana) are not in n5_vocab_whitelist.json (form OR reading);
    JA-147 only gates the reverse direction. Bounded scope for
    BUG-156 (DOCS-VOCAB-006) was the 4-token whitelist→vocab gap.
  - NTR-FU-002 (listening pacing): 38/50 items below 220 mpm but
    all tagged `pacing_status: in_range`; target_range is documented
    as [180, 240] which is bounded-correct, but the JEES-strict
    band [220, 240] + ideal band [200, 220] aren't exposed per-item.
  - NTR-FU-003 (collocations templated corpus-wide): 983 entries
    have `collocations` field, 0 have provenance. NTR-011 renamed
    12 pronouns; broader corpus still holds template-substitution
    particle examples (228x "を かう", 220x "を つかう", 215x "は どこ").

#12 (broader-scope pronoun counter) REJECTED with rationale:
singular pronouns counting people with 人 is semantically correct.
NTR-013 close for collective pronouns only was bounded-correct.
"""
import sys, io, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
import openpyxl

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
XLSX = os.path.join(REPO_N5, "specifications", "test-scenarios-by-specialist-perspective.xlsx")

BUGS = [
    {
        "row": 177,
        "title": "NTR-FU-001 — n5_vocab_whitelist.json missing 11 vocab forms (reverse-direction asymmetry)",
        "description": (
            "**Source:** 2026-05-23 native-teacher review re-paste, item #8 (broader scope of DOCS-VOCAB-006/JA-147).\n\n"
            "**Issue:** vocab.json has 11 entries whose form AND reading are both absent from "
            "n5_vocab_whitelist.json. 9 are onomatopoeia (だんだん, どきどき, にこにこ, ぴかぴか, ぺこぺこ, "
            "まあまあ, わくわく + ぺこぺこ context), 1 is a katakana borrowing (ビル), 1 is the kana-form "
            "of a kanji counter (ばい / 倍), 1 is the polite form of chopsticks (おはし), 1 is the "
            "kana-form of 国籍 (こくせき). \n\n"
            "JA-147 enforces the reverse direction only: 4 whitelist tokens (倍/国籍/週末/では) lack a "
            "matching vocab form/reading; this is documented as 'Known mismatches' in the README. "
            "The vocab→whitelist direction is ungated.\n\n"
            "**Fix:** add the 11 entries to n5_vocab_whitelist.json so vocab forms (or readings) "
            "are a subset of the whitelist. Update README to document both directions of asymmetry. "
            "Add JA-151 CI invariant for vocab→whitelist gate."
        ),
        "severity": "Medium",
        "priority": "P3",
    },
    {
        "row": 178,
        "title": "NTR-FU-002 — listening pacing_status='in_range' across all 50 items despite 38/50 below 220 mpm",
        "description": (
            "**Source:** 2026-05-23 native-teacher review re-paste, item #9.\n\n"
            "**Issue:** All 50 listening items are tagged `pacing_status: in_range`, but mean is "
            "214.5 mpm, range 190.4-237.3. 38 of 50 items are below the JEES-strict 220 mpm threshold; "
            "ALL 50 are below the 240 mpm upper bound. The data documents target_range_morae_per_min "
            "= [180, 240] (lenient learner band), so the in_range tag IS bounded-correct against the "
            "documented threshold — but the JEES-strict band [220, 240] and the round-9 ideal band "
            "[200, 220] aren't exposed per-item.\n\n"
            "**Fix:** add `pacing_band_strict` (in/below/above 220-240) + `pacing_band_ideal` "
            "(in/below/above 200-220) as per-item secondary fields. Keep `pacing_status` (180-240 "
            "learner band) for backward compat. Update _meta.pacing_audit.note to document the "
            "three-band methodology decision explicitly."
        ),
        "severity": "Medium",
        "priority": "P3",
    },
    {
        "row": 179,
        "title": "NTR-FU-003 — 983 vocab entries hold templated `collocations` field with no provenance flag",
        "description": (
            "**Source:** 2026-05-23 native-teacher review re-paste, item #13 (broader scope of NTR-011).\n\n"
            "**Issue:** 983 of 969 vocab entries have `collocations` field; 0 carry "
            "`collocations_provenance`. Audit confirms mass template-substitution: 'を かう' appears "
            "228 times across entries, 'を つかう' 220 times, 'は どこ' 215 times, 'を みる' 197 times, "
            "'を ください' 196 times. These are particle-template slot fills, not corpus collocations.\n\n"
            "NTR-011 (BUG-171) closed for 12 pronoun entries (renamed `collocations` → "
            "`particle_examples`). The broader corpus remains as-is.\n\n"
            "**Fix:** stamp `collocations_provenance: 'template_substitution_2026_05_23'` on all 983 "
            "entries (honest labeling without breaking UI consumers that reference the field name). "
            "Update vocab README + _meta to document the field semantics explicitly. Add JA-152 CI "
            "invariant: every entry with `collocations` field must carry `collocations_provenance`."
        ),
        "severity": "Medium",
        "priority": "P3",
    },
]


def main():
    wb = openpyxl.load_workbook(XLSX)
    ws = wb["User Reported Bugs"]
    for b in BUGS:
        r = b["row"]
        # Col 1 (Bug ID): formula
        ws.cell(r, 1).value = '="BUG-"&TEXT(ROW()-3,"000")'
        # Col 2 (Date Reported)
        ws.cell(r, 2).value = "2026-05-23"
        # Col 3 (Reported By)
        ws.cell(r, 3).value = "native-teacher review re-paste 2026-05-23"
        # Col 4 (Title)
        ws.cell(r, 4).value = b["title"]
        # Col 5 (Description)
        ws.cell(r, 5).value = b["description"]
        # Col 6 (Severity)
        ws.cell(r, 6).value = b["severity"]
        # Col 7 (Priority)
        ws.cell(r, 7).value = b["priority"]
        # Col 8 (Status)
        ws.cell(r, 8).value = "Open"
        # Col 9 (Fix Commit) — left blank until fix lands
        ws.cell(r, 9).value = None
        # Col 10 (Fix Date)
        ws.cell(r, 10).value = None
        print(f"  Filed row {r}: BUG-{r-3:03d} — {b['title'][:60]}")
    wb.save(XLSX)
    print()
    print(f"=== Filed {len(BUGS)} new bugs (BUG-174, BUG-175, BUG-176) ===")


if __name__ == "__main__":
    main()
