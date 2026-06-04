"""Register BUG row for native-review Batch G."""
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
    3: 'Native Japanese / JLPT expert reviewer',
    4: 'Native-review batch G (45 entries): final P1/P2 section-level fixes from sections 11-30',
    5: (
        'Follow-up to BUG-262 (batches A-D) and BUG-264 (batch F). '
        'Batch G applies the remaining concrete pragmatic notes from '
        'sections 11-30 of the 2026-06-04 native-reviewer report. '
        '45 entries touched across 26 sub-batches: '
        'G1 student scope (学生 vs せいと), G2 police register '
        '(けいかん vs おまわりさん), G3 外国人 pragmatic caution, '
        'G4 一日 reading split (ついたち vs いちにち), G5 こんや vs こんばん, '
        'G6 アルバイト→バイト abbreviation, G7 いっぱい dual sense, '
        'G8 ただ multi-sense (just/free/however), G9 しか + negative '
        'requirement, G10 ぐらい vs くらい free variation, G11 やはり '
        'formality vs やっぱり (casual), G12 ことば vs たんご scope, '
        'G13 何で why-vs-by-means refresh, G14 ほしい adjective-of-'
        'desire grammar, G15 ござる as ございます root, G16 はやい '
        '早い (early) / 速い (fast) split, G17 やさしい 易しい (easy) / '
        '優しい (kind) split, G18 おてあらい vs トイレ register, '
        'G19 おふろ vs シャワー bathing culture, G20 せ (back/height) + '
        '足 (leg/foot) duals, G21 じ/もじ/かんじ/かな/ひらがな/カタカナ '
        'six-way distinction, G22 からい (spicy primary; salty regional), '
        'G24 color noun-vs-adjective pairs (白/白い, くろ/くろい, '
        'あか/あかい, あお/あおい), G26 はブラシ orthographic note '
        '(modern: 歯ブラシ). Six reviewer-named entries absent from '
        'corpus and deferred to corpus-expansion track: がくせい (use '
        '学生), 警官 (use けいかん kana form), がいこくじん (use 外国人), '
        'ついたち / いちにち as standalone entries, 今夜/今晩 in kanji, '
        'やっぱり, なんで, ふるい, あし (use 足).'
    ),
    6: 'Medium',
    7: 'P2',
    8: 'Fixed',
    9: '2026-06-04',
    10: '<pending-commit-hash>',
    11: '',
    12: '',
    13: 'BUG-262 (A-D), BUG-264 (F)',
    14: 'tools/apply_native_review_batch_g_2026_06_04.py + python tools/check_content_integrity.py (179/179 PASS)',
}

for col in range(1, ws.max_column + 1):
    src_cell = ws.cell(src_row, col)
    new_cell = ws.cell(new_row, col)
    if col in values:
        new_cell.value = values[col]
    if src_cell.has_style:
        new_cell.font = copy(src_cell.font)
        new_cell.alignment = copy(src_cell.alignment)
        if src_cell.fill.fill_type:
            new_cell.fill = copy(src_cell.fill)

wb.save(XLSX)
print(f'Inserted row {new_row}')
