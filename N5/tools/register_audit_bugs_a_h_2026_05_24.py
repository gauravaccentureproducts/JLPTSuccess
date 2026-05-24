#!/usr/bin/env python3
"""
Register the 8 audit bug clusters (BUG-A..H) into
specifications/test-scenarios-by-specialist-perspective.xlsx
'User Reported Bugs' sheet.

Header layout (from inspection):
- col 1 : BUG-NNN id (formula on most rows)
- col 2 : Reported Date
- col 3 : Source
- col 4 : Issue Title
- col 5 : Description / Repro / Root cause
- col 6 : Severity (Low/Medium/High/Critical)
- col 7 : Priority (P0..P4)
- col 8 : Status (Open / Fixed / Won't Fix / etc.)
- col 9 : Fix Date
- col 10: Fix Commit
- col 11..14: extras / cross-refs
"""
import argparse
from pathlib import Path
from openpyxl import load_workbook

XLSX = Path('specifications/test-scenarios-by-specialist-perspective.xlsx')
SHEET = 'User Reported Bugs'

ROWS = [
    # (severity, priority, status, title, description) — Fix Date + Fix Commit added later
    (
        'Critical', 'P1', 'Fixed',
        "BUG-A — common_mistakes duplicate rows by (norm(wrong), norm(right))",
        "Audit 2026-05-24 surfaced duplicate common_mistakes rows in 59 patterns where (norm(wrong), norm(right)) collided across two entries. Dedup pass kept the row with the longer 'why' text and dropped 52 rows in total. For 44 patterns that fell below the JA-51 floor (>=3 categorized common_mistakes), a backfill pass promoted non-duplicate wrong_corrected_pair entries to the common_mistakes array (47 promotions). All backfilled rows tagged with provenance=auto_fix_2026_05_24 + audit_wave=claude_audit_2026_05_24. Drops logged to data/grammar.fix_log.json BUG-A section."
    ),
    (
        'High', 'P2', 'Fixed',
        "BUG-B — category rename for n5-065..068",
        "Audit 2026-05-24 found 4 patterns (n5-065, n5-066, n5-067, n5-068) using legacy category label 'Verbs - Plain (Dictionary) Form and Negation' which understates the present/past + affirmative/negative coverage of those patterns. Renamed to 'Verbs - Plain Forms (Present/Past, Affirmative/Negative)' across all 4 patterns. provenance + audit_wave tagged."
    ),
    (
        'Critical', 'P1', 'Fixed',
        "BUG-C — cross-contradiction cm vs wcp in n5-025 (ね) and n5-166 (greetings)",
        "Audit 2026-05-24 detected forms appearing as 'wrong' in common_mistakes AND as 'correct' in wrong_corrected_pair within the same pattern. n5-025: cm[2].wrong='いい てんきです。' contradicted wcp[0].correct='いい てんきです。'. n5-166: cm[1].wrong='いただきます。' contradicted wcp[0].correct='いただきます。'. Resolved by rewriting the cm rows to non-contradicting learner errors (n5-025: よ+ね stacking; n5-166: spacing in おはようございます)."
    ),
    (
        'High', 'P2', 'Fixed',
        "BUG-H — common_mistakes rows where wrong == right (after strip-only)",
        "Audit 2026-05-24 found 8 common_mistakes rows where the wrong and right fields, after .strip(), differ only by internal whitespace or punctuation, making the wrong field not actually a learner error (n5-019, n5-023, n5-077, n5-105, n5-133 x2, n5-155, n5-166). 7 rows rewritten to realistic learner-error variants; the 8th (n5-166 cm[1]) was already replaced by the BUG-C fix. provenance + audit_wave tagged."
    ),
    (
        'Medium', 'P2', 'Fixed',
        "BUG-D — duplicate examples within patterns",
        "Audit 2026-05-24 found 13 patterns containing duplicate example sentences within their own examples array (matched by norm(ja) + translation_en.lower()). Dedup pass dropped 14 examples (n5-162 had 2 dup pairs). Affected patterns now carry 8-9 examples instead of 10; no CI invariant requires exactly 10. Drops logged to data/grammar.fix_log.json BUG-D section."
    ),
    (
        'Low', 'P3', 'Fixed',
        "BUG-E — common_mistakes 'why' field shorter than 6 whitespace tokens",
        "Audit 2026-05-24 found 1 pre-existing common_mistakes row with 'why' under 6 tokens (n5-098[0]) plus 2 backfilled rows from the BUG-A wcp-promotion that inherited short wcp.why text. Expanded all 3 with pattern-aware suffix referencing the construction and category."
    ),
    (
        'Low', 'P3', 'Fixed',
        "BUG-F — meaning_ja > 100 characters",
        "Audit 2026-05-24 found 4 patterns (n5-098, n5-154, n5-166, n5-183) with meaning_ja over 100 chars. Split at first 。 between chars 60-100; head stays in meaning_ja, tail moved to a new explanation_ja field. UI/renderer changes deferred to a follow-up if any surface needs the new field; for now the data is structured per the audit recommendation."
    ),
    (
        'Medium', 'P2', 'Fixed',
        "BUG-G — Grammar Pattern List xlsx process change (Reviewer + Reviewed Date)",
        "Audit 2026-05-24 surfaced the lack of explicit reviewer-source disclosure in test/categorized testing/CategorizedtestScenarios.xlsx 'Grammar Pattern List' sheet. All 178 TS-01..TS-10 'Pass' cells are programmatic-only (Claude LLM + schema checks), not native-teacher reviewed. Added 3 columns: Reviewer ('Claude (LLM, programmatic schema)'), Reviewed Date ('2026-05-24'), Native Review Status ('Pending — awaiting native-teacher pass'). This makes the AI-origin of the Pass verdicts visible at the point of use."
    ),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--fix-commit', default='', help='Commit hash to fill in Fix Commit column once the data commit is done.')
    args = ap.parse_args()

    wb = load_workbook(XLSX)
    ws = wb[SHEET]
    start_row = ws.max_row + 1
    fix_date = '2026-05-24'
    fix_commit = args.fix_commit or '(filled at commit time)'

    print(f'starting at row {start_row}')
    for offset, (sev, pri, status, title, desc) in enumerate(ROWS):
        r = start_row + offset
        # Col 1: id formula
        ws.cell(row=r, column=1, value=f'="BUG-"&TEXT(ROW()-3,"000")')
        ws.cell(row=r, column=2, value='2026-05-24')
        ws.cell(row=r, column=3, value="Internal audit — Claude_audit_2026-05-24 cluster sweep (BUG-A..H)")
        ws.cell(row=r, column=4, value=title)
        ws.cell(row=r, column=5, value=desc)
        ws.cell(row=r, column=6, value=sev)
        ws.cell(row=r, column=7, value=pri)
        ws.cell(row=r, column=8, value=status)
        ws.cell(row=r, column=9, value=fix_date)
        ws.cell(row=r, column=10, value=fix_commit)
        print(f'  row {r}: {title[:80]}')

    if args.apply:
        wb.save(XLSX)
        print(f'saved: {XLSX}')
    else:
        print('--dry-run: not saved')


if __name__ == '__main__':
    main()
