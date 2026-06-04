"""Register two BUG rows for the 2026-06-04 native-reviewer report:
  - BUG-NNN closed: batches A-D applied (sense de-contamination,
    homonym sweep, counter cleanup, family pragmatic notes).
  - BUG-NNN open: batch E deferred — particle-example native re-audit
    (50-300 entries, judgment-heavy, needs follow-up native pass on
    replacements).
"""
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

from copy import copy
from pathlib import Path
from openpyxl import load_workbook

ROOT = Path(__file__).resolve().parents[1]
XLSX = ROOT / 'specifications' / 'test-scenarios-by-specialist-perspective.xlsx'

wb = load_workbook(XLSX)
ws = wb['User Reported Bugs']
src_row = ws.max_row  # use latest existing row as style template

# Re-derive bug-id formula from the existing rows (they use a ROW()-3 formula)
def insert_row(values_by_col):
    new_row = ws.max_row + 1
    for col in range(1, ws.max_column + 1):
        src_cell = ws.cell(src_row, col)
        new_cell = ws.cell(new_row, col)
        if col in values_by_col:
            new_cell.value = values_by_col[col]
        if src_cell.has_style:
            new_cell.font = copy(src_cell.font)
            new_cell.alignment = copy(src_cell.alignment)
            if src_cell.fill.fill_type:
                new_cell.fill = copy(src_cell.fill)
    return new_row


# Row 1: native-review batches A-D (Fixed)
r_ad = insert_row({
    1: '="BUG-"&TEXT(ROW()-3,"000")',
    2: '2026-06-04',  # date reported
    3: 'Native Japanese / JLPT expert reviewer',
    4: 'Native-review batches A-D applied (sense de-contamination + homonym sweep + counter cleanup + family pragmatic notes)',
    5: (
        'Consolidated native-reviewer report dated 2026-06-04 flagged seven '
        'P0 issue classes across the 995-entry N5 vocab corpus. Batches A-D '
        'were resolved in this commit: '
        '(A) sense de-contamination of the polite-person かた entry whose '
        'particle_examples were echoing the way-of-doing 〜かた sense (1 entry); '
        '(B) homonym cross-reference sweep — 27 entries received either '
        'false_friends links (cross-form pairs: 花/はな, 雨/あめ, 火/日, 今/いま) '
        'or pragmatic_functions multi-sense summaries (same-form pairs: は×3, '
        'はし×2, きる×2, とる×2, ひく×2, いる×2, しめる×2, あつい×3, かぜ×2, かた×2); '
        '(C) counter cleanup — removed the {人,にん} counter from 家族 (かぞく) and '
        '両親 (りょうしん) which are collective nouns; (D) family pragmatic '
        'notes — added uchi/soto + address-form guidance to 15 family entries '
        '(母, 父, あに, あね, お母さん, お父さん, おにいさん, おねえさん, そふ, そぼ, '
        'おじいさん, おばあさん, おじさん, おばさん, おくさん). 5 reviewer-named '
        'entries not in corpus (お兄さん kanji form, お姉さん kanji form, 祖父, 祖母, ご主人) '
        '— deferred as corpus-expansion items. Total: 45 entries touched. '
        'Driver: tools/apply_native_review_batches_2026_06_04.py. '
        'CI: 179/179 invariants PASS.'
    ),
    6: 'High',
    7: 'P1',
    8: 'Fixed',
    9: '2026-06-04',  # fix date col (per JA-146 swapped convention)
    10: '<pending-commit-hash>',  # fix commit goes here (sentinel until push)
    11: 'JA-108',  # locale-parity / pragmatic_functions schema parity
    12: '(no AUDIT-COVERAGE part for this batch)',
    13: 'BUG-010 (native-review-queue), BUG-203 (UI parity)',
    14: 'tools/apply_native_review_batches_2026_06_04.py + python tools/check_content_integrity.py',
})

# Row 2: batch E deferred (Open)
r_e = insert_row({
    1: '="BUG-"&TEXT(ROW()-3,"000")',
    2: '2026-06-04',
    3: 'Native Japanese / JLPT expert reviewer',
    4: 'Native-review batch E DEFERRED — particle-example corpus-wide re-audit (highest-judgment, ~50-300 entries)',
    5: (
        'The same 2026-06-04 native-reviewer report flagged the particle_examples '
        'field across the vocab corpus as the highest-risk learner-facing area. '
        'Specific examples called out: だれをしますか, どなたをしますか, だれにいきますか, '
        'あなたをしる, わたしたちをしる, じぶんとあう — these are unnatural / '
        'template-generated patterns that an N5 learner might memorize wholesale. '
        'A corpus-wide exact-string scan for those 6 specific phrases returned '
        '0 hits (they may have been removed in a prior pass, or our scan was '
        'too strict). Batch E requires a sample-and-flag native pass on every '
        'entry\'s particle_examples to identify template-looking patterns and '
        'replace with native-approved N5 collocations. Estimated scope: '
        '50-300 entries. Deferred to a follow-up cycle per user direction '
        '(2026-06-04 chat). Replacement entries themselves will need a '
        'second native pass to verify naturalness — meaning this is a '
        'two-cycle work item.'
    ),
    6: 'Medium',
    7: 'P2',
    8: 'Open',
    9: '',  # no fix date yet
    10: '<pending-cycle>',
    11: '',
    12: '',
    13: 'BUG-010 (native-review-queue)',
    14: 'Awaiting native-reviewer follow-up pass + replacement audit',
})

wb.save(XLSX)
print(f'Inserted 2 rows: r{r_ad} (batches A-D, Fixed) + r{r_e} (batch E, Open)')
