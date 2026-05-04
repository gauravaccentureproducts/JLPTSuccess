"""Pull 25 stratified-random questions for manual eyeball review.
Stratified by grammarPatternId so we don't oversample any single pattern.

Read-only. Prints stem, choices, correct answer, rationale.
"""
import io
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

random.seed(42)  # deterministic for reproducibility

qs = json.loads((ROOT / 'data' / 'questions.json').read_text(encoding='utf-8'))['questions']
by_pat = defaultdict(list)
for q in qs:
    by_pat[q.get('grammarPatternId') or 'other'].append(q)

# Pick 1-2 from each pattern bucket, up to 25 total
sample = []
for pat in sorted(by_pat.keys()):
    bucket = by_pat[pat]
    take = min(2, len(bucket))
    sample.extend(random.sample(bucket, take))
random.shuffle(sample)
sample = sample[:25]

for n, q in enumerate(sample, 1):
    print(f'\n[{n}] {q.get("id")}  pattern={q.get("grammarPatternId","?")}  type={q.get("type")}')
    print(f'    stem: {q.get("question_ja") or q.get("stem_html") or "(none)"}')
    print(f'    prompt: {q.get("prompt_ja","")}')
    choices = q.get('choices') or []
    correct = q.get('correctAnswer', '')
    for c in choices:
        m = ' <-- correct' if c == correct else ''
        print(f'      [ ] {c}{m}')
    expl = q.get('explanation_en','') or q.get('rationale','')
    if expl:
        print(f'    rationale: {expl[:100]}')
