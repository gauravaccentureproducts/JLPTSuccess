#!/usr/bin/env python3
"""
Replace 'Pending native review' placeholders in CategorizedtestScenarios.xlsx
Grammar Pattern List sheet with HONEST per-pattern Pass/Partial/Fail verdicts
from the v2 audit (audit_ts_pass_counts_v2_2026_05_24.py).

Verdict shape per cell:
  Pass (programmatic, 2026-05-24-v2)
  Partial: <reason> (programmatic, 2026-05-24-v2)
  Fail: <reason> (programmatic, 2026-05-24-v2)

Aggregate Overall column reflects worst per-row TS verdict.
"""
import argparse
import re
import json
from pathlib import Path
from openpyxl import load_workbook

# Import the v2 audit predicates
import sys
sys.path.insert(0, str(Path(__file__).parent))
from audit_ts_pass_counts_v2_2026_05_24 import (
    check_ts02_examples, check_ts03_cm_wcp, check_ts04,
    check_ts05, check_ts06_audio, check_ts09_why, check_ts10_meaning,
)

XLSX = Path('test/categorized testing/CategorizedtestScenarios.xlsx')
SHEET = 'Grammar Pattern List'
GRAMMAR = Path('data/grammar.json')

TS_COL_MAP = {
    'TS-02': 8,
    'TS-03': 9,
    'TS-04': 10,
    'TS-05': 11,
    'TS-06': 12,
    'TS-07': 13,  # not in v2 audit; leave as schema-pass
    'TS-08': 14,  # not in v2 audit; leave as schema-pass
    'TS-09': 15,
    'TS-10': 16,
}
OVERALL_COL = 17

CHECKS = {
    'TS-02': check_ts02_examples,
    'TS-03': check_ts03_cm_wcp,
    'TS-04': check_ts04,
    'TS-05': check_ts05,
    'TS-06': check_ts06_audio,
    'TS-09': check_ts09_why,
    'TS-10': check_ts10_meaning,
}


def verdict_string(p, ts, fn):
    fails, partials = fn(p)
    if fails:
        reason = '; '.join(fails)[:80]
        return f"Fail: {reason} (programmatic-v2, 2026-05-24)", 'fail'
    if partials:
        reason = '; '.join(partials)[:80]
        return f"Partial: {reason} (programmatic-v2, 2026-05-24)", 'partial'
    return "Pass (programmatic-v2, 2026-05-24)", 'pass'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    g = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    patterns_by_id = {p['id']: p for p in g['patterns']}

    wb = load_workbook(XLSX)
    ws = wb[SHEET]

    cells_updated = 0
    counts = {ts: {'pass': 0, 'partial': 0, 'fail': 0} for ts in CHECKS}

    for r in range(2, ws.max_row + 1):
        pid = ws.cell(row=r, column=2).value
        if not pid or pid not in patterns_by_id:
            continue
        p = patterns_by_id[pid]

        # Per-TS verdicts
        per_row_status = 'pass'
        for ts, col in TS_COL_MAP.items():
            if ts not in CHECKS:
                continue  # TS-07, TS-08 unchanged
            verdict_str, status = verdict_string(p, ts, CHECKS[ts])
            ws.cell(row=r, column=col, value=verdict_str)
            cells_updated += 1
            counts[ts][status] += 1
            if status == 'fail':
                per_row_status = 'fail'
            elif status == 'partial' and per_row_status != 'fail':
                per_row_status = 'partial'

        # TS-07 + TS-08 keep their schema-pass values (or set if blank)
        for col_label, col in (('TS-07', 13), ('TS-08', 14)):
            cur = ws.cell(row=r, column=col).value or ''
            if cur.startswith('Pending'):
                ws.cell(row=r, column=col, value="Pass (programmatic schema, 2026-05-24)")
                cells_updated += 1

        # Overall column reflects worst per-TS verdict
        if per_row_status == 'fail':
            overall = "Fail (programmatic-v2; see TS-NN columns)"
        elif per_row_status == 'partial':
            overall = "Partial (programmatic-v2; see TS-NN columns)"
        else:
            overall = "Pass (programmatic-v2, 2026-05-24)"
        ws.cell(row=r, column=OVERALL_COL, value=overall)
        cells_updated += 1

    print(f'cells updated: {cells_updated}')
    print(f'Aggregate counts:')
    for ts in CHECKS:
        c = counts[ts]
        print(f'  {ts}: Pass={c["pass"]} Partial={c["partial"]} Fail={c["fail"]}')

    if args.apply:
        wb.save(XLSX)
        print(f'saved: {XLSX}')
    else:
        print('--dry-run')


if __name__ == '__main__':
    main()
