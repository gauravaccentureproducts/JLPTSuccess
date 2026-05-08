"""Dump all remaining llm_curated entries (questions.json + papers) for
native-Hindi expert hand-rewrite."""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 15 explanation_hi
print('### EXPLANATION_HI (still llm_curated):')
qs = json.loads((ROOT / 'data' / 'questions.json').read_text(encoding='utf-8'))
for q in qs['questions']:
    if q.get('explanation_hi_provenance') == 'llm_curated':
        print(f"\n{q.get('id')}")
        print(f"  ja: {q.get('question_ja', q.get('stem_html', ''))[:80]}")
        print(f"  ans: {q.get('correctAnswer', '?')}")
        print(f"  en: {q.get('explanation_en', '')[:200]}")
        print(f"  hi: {q.get('explanation_hi', '')[:200]}")

# 79 distractor blocks
print('\n\n### DISTRACTOR BLOCKS (still llm_curated):')
count = 0
for q in qs['questions']:
    if q.get('distractor_explanations_hi_provenance') != 'llm_curated':
        continue
    de_hi = q.get('distractor_explanations_hi') or {}
    de_en = q.get('distractor_explanations') or {}
    if not isinstance(de_hi, dict):
        continue
    count += 1
    # show all this time
    print(f"\n{q.get('id')}")
    print(f"  ans: {q.get('correctAnswer', '?')}")
    for k in de_hi:
        en = de_en.get(k, '')
        hi = de_hi.get(k, '')
        print(f"  [{k}]")
        print(f"    en: {en[:160]}")
        print(f"    hi: {hi[:200]}")

print(f'\n(Showing first 30 distractor blocks; remaining 49 omitted for brevity.)')
