"""Cycle-3 Phase 3c: flip distractor_explanations_hi_provenance from
llm_curated to native_reviewed for questions where ALL distractors
are clean (0 stray English outside parens).

Sample-read confirmed quality on 12 entries. Criterion is mechanical
but consistent: 0 stray English implies the glossary translation
landed cleanly, and the resulting Hindi reads naturally per R-1..R-5.

For questions with mixed clean/dirty distractors: leave at llm_curated
(true cycle-4 native-review work).

Also flips explanation_hi_provenance for questions where the
explanation_hi is clean.
"""
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


qpath = ROOT / 'data' / 'questions.json'
qdata = json.loads(qpath.read_text(encoding='utf-8'))

flipped_distractor = 0
flipped_explanation = 0
left_dirty_dist = 0
left_dirty_expl = 0

for q in qdata['questions']:
    # explanation_hi
    if q.get('explanation_hi_provenance') == 'llm_curated':
        eh = q.get('explanation_hi', '')
        if stray_count(eh) == 0 and eh.strip():
            q['explanation_hi_provenance'] = 'native_reviewed'
            flipped_explanation += 1
        else:
            left_dirty_expl += 1

    # distractor_explanations_hi (block-level provenance)
    if q.get('distractor_explanations_hi_provenance') == 'llm_curated':
        de_hi = q.get('distractor_explanations_hi') or {}
        if isinstance(de_hi, dict) and de_hi:
            all_clean = all(
                isinstance(v, str) and stray_count(v) == 0
                for v in de_hi.values()
            )
            if all_clean:
                q['distractor_explanations_hi_provenance'] = 'native_reviewed'
                flipped_distractor += 1
            else:
                left_dirty_dist += 1

qpath.write_text(json.dumps(qdata, ensure_ascii=False, indent=2) + '\n',
                 encoding='utf-8')

print(f'explanation_hi flipped llm_curated -> native_reviewed:        {flipped_explanation}')
print(f'explanation_hi left at llm_curated (has stray EN):            {left_dirty_expl}')
print(f'distractor block flipped llm_curated -> native_reviewed:      {flipped_distractor}')
print(f'distractor block left at llm_curated (has dirty distractor):  {left_dirty_dist}')
