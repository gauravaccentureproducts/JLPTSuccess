"""Sample English source from HI-02 placeholders for glossary planning."""
from __future__ import annotations
import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

PH = re.compile(r'अस्थायी|समीक्षा\s*(प्रतीक्षित|लंबित)|यह\s*विकल्प\s*यहाँ\s*अनुपयुक्त|अंग्रे[ज़ज]ी\s*संस्करण')

d = json.loads((ROOT / 'data' / 'questions.json').read_text(encoding='utf-8'))
items = d['questions']

print('## Sample placeholder explanation_hi sources (English):')
phs = [q for q in items if isinstance(q.get('explanation_hi'), str) and PH.search(q['explanation_hi'])]
for q in phs[:30]:
    print(f"  {q['id']}: {q.get('explanation', '')[:140]}")

print('\n## Sample placeholder distractor_explanations_hi sources (English):')
count = 0
for q in items:
    de = q.get('distractor_explanations') or {}
    de_hi = q.get('distractor_explanations_hi') or {}
    if isinstance(de, dict) and isinstance(de_hi, dict):
        for k, v in de_hi.items():
            if isinstance(v, str) and PH.search(v) and count < 20:
                en = de.get(k, '')
                print(f"  {q['id']}.{k!r}: {en[:140]}")
                count += 1

# Tally most common English words/phrases
print('\n## Most common words in English source of placeholders:')
all_en = []
for q in phs:
    if q.get('explanation'):
        all_en.append(q['explanation'])
for q in items:
    de = q.get('distractor_explanations') or {}
    de_hi = q.get('distractor_explanations_hi') or {}
    if isinstance(de, dict) and isinstance(de_hi, dict):
        for k, v in de_hi.items():
            if isinstance(v, str) and PH.search(v):
                all_en.append(de.get(k, ''))

word_count = Counter()
for s in all_en:
    for w in re.findall(r'[a-zA-Z]+', s.lower()):
        if len(w) >= 3:
            word_count[w] += 1
for w, c in word_count.most_common(60):
    print(f'  {w:<20} {c}')
