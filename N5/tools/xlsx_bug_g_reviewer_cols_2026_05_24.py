#!/usr/bin/env python3
"""
BUG-G: Add Reviewer + Reviewed Date columns to CategorizedtestScenarios.xlsx
'Grammar Pattern List' sheet, and re-mark TS-* cells that were programmatic-only
to disclose the reviewer source.

All Pass verdicts on TS-01..TS-10 currently come from programmatic schema checks,
not native-teacher review. The new columns make this provenance explicit.
"""

import argparse
from pathlib import Path
from openpyxl import load_workbook

XLSX = Path('test/categorized testing/CategorizedtestScenarios.xlsx')
SHEET = 'Grammar Pattern List'
NEW_COLS = [
    ('Reviewer', 'Claude (LLM, programmatic schema)'),
    ('Reviewed Date', '2026-05-24'),
    ('Native Review Status', 'Pending — awaiting native-teacher pass'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    wb = load_workbook(XLSX)
    ws = wb[SHEET]
    max_col = ws.max_column
    print(f'before: cols={max_col} rows={ws.max_row}')

    # Look up current header positions of new columns (skip if already present)
    hdr = [ws.cell(row=1, column=c).value for c in range(1, max_col + 1)]
    new_col_offsets = {}
    for name, default in NEW_COLS:
        if name in hdr:
            new_col_offsets[name] = hdr.index(name) + 1
        else:
            max_col += 1
            ws.cell(row=1, column=max_col, value=name)
            new_col_offsets[name] = max_col

    # Populate the new columns for each data row (rows 2..179)
    for r in range(2, ws.max_row + 1):
        # Only populate if pattern ID present
        pid = ws.cell(row=r, column=2).value
        if not pid:
            continue
        for name, default in NEW_COLS:
            col = new_col_offsets[name]
            cur = ws.cell(row=r, column=col).value
            if cur is None or cur == '':
                ws.cell(row=r, column=col, value=default)

    print(f'after:  cols={ws.max_column} new col positions: {new_col_offsets}')

    if args.apply:
        wb.save(XLSX)
        print(f'saved: {XLSX}')
    else:
        print('--dry-run: not saved')


if __name__ == '__main__':
    main()
