"""Register Batch K row + mark the 2 cited すむ items closed."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from copy import copy
from pathlib import Path
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
XLSX = ROOT / 'specifications' / 'test-scenarios-by-specialist-perspective.xlsx'
wb = load_workbook(XLSX)
ws = wb['User Reported Bugs']
src_row = ws.max_row
new_row = ws.max_row + 1

values = {
    1: '="BUG-"&TEXT(ROW()-3,"000")',
    2: '2026-06-04',
    3: 'Native Japanese / JLPT expert reviewer (BUG-266 re-check)',
    4: 'Native-review batch K — close last 2 BUG-266 re-check items on すむ (frequency-adverb collocations → location-particle)',
    5: (
        'The BUG-266 re-check confirmed 10/12 batch-J bugs fixed; 2 remained, '
        'both on すむ ("to live/reside"): まいにち すむ ("live every day") and '
        'いま すむ ("live now") — unnatural frequency/time-adverb collocations '
        'for a stative verb. The reviewer supplied the native-approved fix: '
        'replace with location-particle (に) collocations. Batch K replaced '
        'all three frequency/time-adverb collocations on すむ '
        '(よく/まいにち/いま すむ — よく すむ is the same error class as the 2 '
        'cited) with 東京に すむ / 日本に すむ / この町に すむ. This also makes '
        'the field a proper set of particle examples (location に, the '
        'particle すむ actually takes). すむ particle_examples is now '
        '[すむ, すみます, すみました, 東京に すむ, 日本に すむ, この町に すむ]. '
        'Scope is すむ-ONLY: the broad frequency-adverb+verb template across '
        'the other ~109 verbs stays in BUG-263 because it is per-verb — '
        'よく ある ("there often is / common") is NATURAL while よく すむ is not; '
        'only a native reviewer can judge each verb. '
        'Driver: tools/apply_native_review_batch_k_2026_06_04.py. CI 180/180.'
    ),
    6: 'Medium',
    7: 'P2',
    8: 'Fixed',
    9: '2026-06-04',
    10: '<pending-commit-hash>',
    11: '',
    12: '',
    13: 'BUG-266 (batch J — 10/12), BUG-263 (broad particle-example naturalness, still open for other verbs)',
    14: 'tools/apply_native_review_batch_k_2026_06_04.py + reviewer re-check (10/12 then 12/12 cited) + CI 180/180',
}

for col in range(1, ws.max_column + 1):
    sc = ws.cell(src_row, col)
    nc = ws.cell(new_row, col)
    if col in values:
        nc.value = values[col]
    if sc.has_style:
        nc.font = copy(sc.font)
        nc.alignment = copy(sc.alignment)
        if sc.fill.fill_type:
            nc.fill = copy(sc.fill)

wb.save(XLSX)
print(f'Inserted Batch K row {new_row}')
