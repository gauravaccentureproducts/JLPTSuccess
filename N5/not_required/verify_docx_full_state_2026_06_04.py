"""Final comprehensive content audit of the regenerated vocab review docx.
Verifies content from EVERY batch (A through I) is present."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document

doc = Document('docs/vocab-review/N5-vocab-995-entries-for-native-review.docx')
print(f'Total paragraphs:  {len(doc.paragraphs)}')
print(f'Total tables:      {len(doc.tables)}')
print()

para_text = '\n'.join(p.text for p in doc.paragraphs)
# Also collect table text — Reviewer-notes box content lives in tables
table_text_chunks = []
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                table_text_chunks.append(p.text)
table_text = '\n'.join(table_text_chunks)
full_text = para_text + '\n' + table_text

# Markers grouped by batch
markers_by_batch = {
    'A — sense de-contamination': [
        ('A1', "あの方は"),
    ],
    'B — homonym cross-references': [
        ('B-cross-form', "Same-kana homonym (multiple N5 senses)"),
        ('B-multi-sense template', "covers 2 distinct N5 meanings"),
    ],
    'C — counter cleanup': [
        ('C — 家族/両親 lack 「Counter:」 line', None),  # check via side-effect
    ],
    'D — family English pragmatic': [
        ('D1', "Use 母 when referring to YOUR own"),
        ('D2', "Use お母さん to refer politely to SOMEONE ELSE"),
    ],
    'F — section-level fixes': [
        ('F1 legacy', "use 電車 instead in modern Japanese"),
        ('F2 naku', "鳴く is for animal sounds"),
        ('F3 pronouns', "In everyday modern Japanese, かのじょ"),
        ('F4 sensei', "respectful title used for any expert"),
        ('F5 sayounara', "surprisingly formal in modern usage"),
        ('F6 umi/mizuumi', "lake (use みずうみ for lake)"),
        ('F7 suki na-adj', "but すき is a な-adjective"),
        ('F8 kirei dual', "pretty/beautiful"),
    ],
    'G — final P1/P2 section-level': [
        ('G1 student', "STUDENTS in higher education"),
        ('G3 foreigner', "literally means 'foreign-country person'"),
        ('G6 baito', "shortened to バイト"),
        ('G8 tada', "has several meanings"),
        ('G9 shika', "REQUIRES a negative predicate"),
        ('G14 hoshii', "い-adjective, not a verb"),
        ('G16 hayai split', "早い means 'early'"),
        ('G17 yasashii split', "易しい = 'easy / simple'"),
        ('G21 kana umbrella', "umbrella term for the two Japanese syllabic systems"),
        ('G24 color noun', "NOUN form of the color"),
    ],
    'H — mechanical closure': [
        ('H2 legacy revivals', "vinyl audio record"),
        ('H2 film legacy', "photographic film"),
        ('H4 watashi note', "usually OMIT the subject"),
        ('H4 minna/minasan', "casual / informal 'everyone'"),
        ('H5 concise JA', "自分の母を外の人に話すときの言い方。"),
        ('H5 concise JA caution', "家族や親しい文脈では自然だが"),
    ],
    'I — reviewer-box pre-population': [
        ('I1 placeholder', "☐ 未確認"),
        ('I1 instruction', "Native reviewer: delete the line above"),
    ],
}

print('=== Content markers by batch ===')
total_hits = 0
total_checks = 0
missing = []
for batch, items in markers_by_batch.items():
    print(f'\n[{batch}]')
    for label, needle in items:
        if needle is None:
            # Special check
            continue
        total_checks += 1
        if needle in full_text:
            total_hits += 1
            print(f'  ✓ {label}')
        else:
            print(f'  ✗ MISS: {label}  needle={needle[:60]!r}')
            missing.append((batch, label, needle))

# Special check: batch C — verify 家族(かぞく)/両親(りょうしん) entries
# don't carry a Counter: line in their per-page block
print('\n[C — counter cleanup spot-check on かぞく / りょうしん entry blocks]')
import re
for headword in ('かぞく', 'りょうしん'):
    # Find this headword as a standalone paragraph (the entry title)
    block_lines = para_text.split('\n')
    if headword in block_lines:
        idx = block_lines.index(headword)
        block = block_lines[idx:idx + 25]
        has_counter = any('Counter: 〜' in line for line in block)
        if has_counter:
            print(f'  ✗ MISS: {headword} entry block still has 「Counter: 〜」')
            missing.append(('C', headword + ' counter cleanup', '(no counter line)'))
        else:
            print(f'  ✓ {headword}: no Counter: line in entry block')

print(f'\n=== Summary ===')
print(f'Markers checked:  {total_checks}')
print(f'Markers found:    {total_hits}')
print(f'Coverage:         {100 * total_hits // total_checks if total_checks else 0}%')
if missing:
    print(f'\nMissing items:')
    for b, l, n in missing:
        print(f'  [{b}] {l}')

# Count Reviewer-notes tables (should be 995)
notes_tables = 0
for t in doc.tables:
    for row in t.rows:
        for cell in row.cells:
            for p in cell.paragraphs:
                if '☐ 未確認' in p.text:
                    notes_tables += 1
                    break
print(f'\nReviewer-notes tables with 未確認 placeholder: {notes_tables}')
print(f'(Expected: 995 — one per vocab entry)')
