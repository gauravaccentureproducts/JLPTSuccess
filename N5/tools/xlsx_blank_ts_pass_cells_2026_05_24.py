#!/usr/bin/env python3
"""
Followup item 1: blank the TS-01..TS-10 Pass verdicts in
CategorizedtestScenarios.xlsx 'Grammar Pattern List' sheet.

Per the BUG-G acceptance criterion: 'clear unjustified Pass cells; add
columns'. The columns were added in xlsx_bug_g_reviewer_cols_2026_05_24.py;
this script clears the 178x10 TS cells so the new Reviewer / Reviewed Date /
Native Review Status columns are the sole verdict source.

The 'Overall (Pass/Fail/Partial)' column is also blanked for consistency.

Replacement: 'Pending native review (programmatic-only)'.
"""
import argparse
from pathlib import Path
from openpyxl import load_workbook

XLSX = Path('test/categorized testing/CategorizedtestScenarios.xlsx')
SHEET = 'Grammar Pattern List'
TS_COLS = list(range(7, 17))  # TS-01..TS-10 = cols 7..16
OVERALL_COL = 17
PLACEHOLDER = 'Pending native review (programmatic-only)'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    wb = load_workbook(XLSX)
    ws = wb[SHEET]
    n_cleared = 0
    for r in range(2, ws.max_row + 1):
        pid = ws.cell(row=r, column=2).value
        if not pid:
            continue
        for c in TS_COLS:
            cur = ws.cell(row=r, column=c).value
            if cur and isinstance(cur, str) and cur.startswith('Pass'):
                ws.cell(row=r, column=c, value=PLACEHOLDER)
                n_cleared += 1
        # Overall column
        cur = ws.cell(row=r, column=OVERALL_COL).value
        if cur and isinstance(cur, str) and cur.startswith('Pass'):
            ws.cell(row=r, column=OVERALL_COL, value=PLACEHOLDER)
            n_cleared += 1

    print(f'cells cleared: {n_cleared}')

    if args.apply:
        wb.save(XLSX)
        print(f'saved: {XLSX}')
    else:
        print('--dry-run: not saved')


if __name__ == '__main__':
    main()
