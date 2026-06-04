"""Confirm the 家族 (かぞく) and 両親 (りょうしん) pages in the docx no
longer carry a 'Counter:' line. Read-only."""
import sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from docx import Document

doc = Document('docs/vocab-review/N5-vocab-995-entries-for-native-review.docx')

# Each entry is a sequence of paragraphs separated by page breaks. Scan
# for the target headwords and the surrounding ~20 paragraphs to see if
# a "Counter:" line appears in that window.
paras = [p.text for p in doc.paragraphs]
for headword in ('かぞく', 'りょうしん'):
    print(f'=== Page block around {headword!r} ===')
    # Find the title paragraph (just the headword on its own line).
    indices = [i for i, t in enumerate(paras) if t.strip() == headword]
    if not indices:
        print('  not found in docx body')
        continue
    for idx in indices:
        # Show ~30 paragraphs starting from the headword.
        block = paras[idx:idx + 30]
        # Detect any "Counter:" line in this window.
        counter_lines = [b for b in block if 'Counter:' in b or 'Counter ' in b]
        print(f'  start at paragraph {idx}')
        if counter_lines:
            print(f'  ⚠ FOUND counter line(s) in this entry block:')
            for c in counter_lines:
                print(f'    {c[:80]}')
        else:
            print(f'  ✓ NO Counter: line in this entry block (batch C confirmed)')
        # Show first 10 lines for context
        for b in block[:10]:
            t = b.strip()
            if t:
                print(f'    | {t[:80]}')
        print()
