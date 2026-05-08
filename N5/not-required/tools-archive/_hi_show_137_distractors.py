"""Sample distractor_explanations_hi entries marked llm_curated."""
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

def stray_count(s):
    if not isinstance(s, str):
        return 0
    s2 = PAREN.sub('', s)
    s2 = re.sub(r'[ぁ-ゖァ-ヺ一-龯]+', '', s2)
    words = LATIN.findall(s2)
    return sum(1 for w in words if w.upper() not in ALLOWED)


qs = json.loads((ROOT / 'data' / 'questions.json').read_text(encoding='utf-8'))
total_clean = 0
total_dirty = 0
clean_short = 0  # <40 chars + 0 stray = good candidates
sample_clean = []
sample_dirty = []
for q in qs['questions']:
    if q.get('distractor_explanations_hi_provenance') != 'llm_curated':
        continue
    de_hi = q.get('distractor_explanations_hi') or {}
    de_en = q.get('distractor_explanations') or {}
    if isinstance(de_hi, dict):
        for k, v in de_hi.items():
            if not isinstance(v, str):
                continue
            stray = stray_count(v)
            en = de_en.get(k, '')
            if stray == 0:
                total_clean += 1
                if len(v) < 60:
                    clean_short += 1
                if len(sample_clean) < 12:
                    sample_clean.append((q.get('id'), k, en, v))
            else:
                total_dirty += 1
                if len(sample_dirty) < 6:
                    sample_dirty.append((q.get('id'), k, en, v, stray))

print(f'Total distractor entries marked llm_curated: {total_clean + total_dirty}')
print(f'  Clean (0 stray English):      {total_clean}')
print(f'  Of clean, short (<60 chars):  {clean_short}')
print(f'  Dirty (1+ stray):             {total_dirty}')
print('\nSample clean:')
for qid, k, en, hi in sample_clean:
    print(f'  {qid}.{k}')
    print(f'    en: {en[:80]}')
    print(f'    hi: {hi[:100]}')
print('\nSample dirty:')
for qid, k, en, hi, stray in sample_dirty:
    print(f'  {qid}.{k} ({stray} stray)')
    print(f'    en: {en[:80]}')
    print(f'    hi: {hi[:100]}')
