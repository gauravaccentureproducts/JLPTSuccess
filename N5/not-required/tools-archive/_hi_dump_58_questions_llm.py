"""Dump the 58 questions.json explanation_hi entries marked llm_curated
with their English source for native-scholar review."""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ALLOWED = {'JLPT', 'N5', 'JJN', 'OK'}
LATIN = re.compile(r'\b[a-zA-Z]{4,}\b')
PAREN = re.compile(r'\([^()]*\)')

def stray_english_count(s):
    if not isinstance(s, str):
        return 0
    s2 = PAREN.sub('', s)
    s2 = re.sub(r'[ぁ-ゖァ-ヺ一-龯]+', '', s2)
    words = LATIN.findall(s2)
    return sum(1 for w in words if w.upper() not in ALLOWED)


qs = json.loads((ROOT / 'data' / 'questions.json').read_text(encoding='utf-8'))
items = qs['questions']

clean = []
dirty = []
for q in items:
    if q.get('explanation_hi_provenance') != 'llm_curated':
        continue
    en = q.get('explanation_en', '')
    hi = q.get('explanation_hi', '')
    stray = stray_english_count(hi)
    rec = (q.get('id'), en, hi, stray)
    if stray == 0:
        clean.append(rec)
    else:
        dirty.append(rec)

print(f'Clean (0 stray English):  {len(clean)}')
print(f'Dirty (1+ stray English): {len(dirty)}')
print()
print('=== Clean entries (eligible for native_reviewed flip after read) ===')
for qid, en, hi, _ in clean:
    print(f'\n{qid}')
    print(f'  EN: {en[:120]}')
    print(f'  HI: {hi[:200]}')

print('\n=== Dirty entries (need glossary expansion or hand rewrite) ===')
for qid, en, hi, stray in dirty:
    print(f'\n{qid} ({stray} stray)')
    print(f'  EN: {en[:120]}')
    print(f'  HI: {hi[:200]}')
