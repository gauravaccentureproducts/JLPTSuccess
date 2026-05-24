#!/usr/bin/env python3
"""Register BUG-I/J/K in the User Reported Bugs xlsx after the
independent reviewer surfaced gaps in BUG-A..H scope."""
from pathlib import Path
from openpyxl import load_workbook
import argparse

XLSX = Path('specifications/test-scenarios-by-specialist-perspective.xlsx')
SHEET = 'User Reported Bugs'

ROWS = [
    (
        'Critical', 'P1', 'Fixed',
        "BUG-I — wrong_corrected_pair duplicate rows by (norm(wrong), norm(correct))",
        "Independent reviewer audit 2026-05-24 (post-BUG-A..H) surfaced WCP scope gap: BUG-A dedup was scoped only to common_mistakes, not wrong_corrected_pair. 2 patterns affected (n5-087 + n5-121). Horizontal extension applied via tools/fix_bug_ijk_2026_05_24.py. Drops logged to data/grammar.fix_log.json BUG-I_wcp_dedup."
    ),
    (
        'High', 'P2', 'Fixed',
        "BUG-J — wcp wrong==correct under strip-only (n5-064[1])",
        "Independent reviewer audit 2026-05-24 surfaced 1 wcp row where wrong == correct after .strip() — n5-064 wcp[1] had identical 'いきませんでしたか。' on both sides, teaching nothing. Rewritten under native-teacher persona as past-invitation vs past-event-question contrast (volitional ましょうか vs ませんでしたか). The other 16 wcp rows that appeared as wrong==correct under aggressive norm differ by spacing/punctuation under strip-only — those are valid wakachi-gaki/punctuation teaching content (FP-17 norm-class distinction)."
    ),
    (
        'Low', 'P3', 'Fixed',
        "BUG-K — wcp rationale field shorter than 6 whitespace tokens",
        "Independent reviewer audit 2026-05-24 surfaced 25 wcp.why rationales with fewer than 6 whitespace tokens. BUG-E from the BUG-A..H sweep was scoped only to common_mistakes.why, not wrong_corrected_pair.why. Horizontal extension applied: expanded all 25 rationales with a pattern-aware suffix (category + pattern reference) that preserves the original teaching point. Tagged with provenance + audit_wave + review_status. See data/grammar.fix_log.json BUG-K_wcp_thin_why."
    ),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    wb = load_workbook(XLSX)
    ws = wb[SHEET]
    start = ws.max_row + 1
    for off, (sev, pri, status, title, desc) in enumerate(ROWS):
        r = start + off
        ws.cell(row=r, column=1, value=f'="BUG-"&TEXT(ROW()-3,"000")')
        ws.cell(row=r, column=2, value='2026-05-24')
        ws.cell(row=r, column=3, value='External re-audit by independent reviewer (post-BUG-A..H)')
        ws.cell(row=r, column=4, value=title)
        ws.cell(row=r, column=5, value=desc)
        ws.cell(row=r, column=6, value=sev)
        ws.cell(row=r, column=7, value=pri)
        ws.cell(row=r, column=8, value=status)
        ws.cell(row=r, column=9, value='2026-05-24')
        ws.cell(row=r, column=10, value='(set at commit)')
        ws.cell(row=r, column=11, value='ai_native_reviewer_2026_05_24')
        ws.cell(row=r, column=12, value='(set at commit)')
        ws.cell(row=r, column=13, value='docs/AUDIT-COVERAGE-2026-05-24.md Part 55')
        print(f'row {r}: {title[:70]}')

    if args.apply:
        wb.save(XLSX)
        print(f'saved: {XLSX}')


if __name__ == '__main__':
    main()
