"""Show full choices + correct for the multi-correct candidates so the
fix patches can be designed precisely."""
import json
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

QUESTIONS_PATH = Path(__file__).resolve().parent.parent / 'data' / 'questions.json'

CANDIDATES = [
    'q-0013', 'q-0016', 'q-0020', 'q-0026', 'q-0027', 'q-0043', 'q-0044',
    'q-0419', 'q-0420', 'q-0421', 'q-0422',
    # Tier-3 sanity-check
    'q-0007', 'q-0008',
    # Re-look at q-0004 since it's identical stem to q-0026
    'q-0004',
]

with QUESTIONS_PATH.open('r', encoding='utf-8') as f:
    data = json.load(f)

for q in data['questions']:
    if q['id'] in CANDIDATES:
        print(f"== {q['id']} (pattern={q.get('grammarPatternId')}) ==")
        print(f"  P: {q.get('prompt_ja','')}")
        print(f"  Q: {q.get('question_ja','')}")
        print(f"  choices: {q.get('choices')}")
        print(f"  correct: {q.get('correctAnswer')}")
        print()
