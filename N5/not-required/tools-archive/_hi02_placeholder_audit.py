"""For each placeholder Hindi entry in questions.json, check what English
source content exists - so we can decide whether to translate from English
(option B) or write fresh from question structure (option C).
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path
from collections import Counter

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

PLACEHOLDER_PATTERNS = [
    re.compile(r'अस्थायी'),
    re.compile(r'समीक्षा\s*(प्रतीक्षित|लंबित)'),
    re.compile(r'मूल\s*समीक्षा'),
    re.compile(r'अंग्रे[ज़ज]ी\s*संस्करण'),
    re.compile(r'विवरण\s*के\s*लिए.*पृष्ठ'),
    re.compile(r'यह\s*विकल्प\s*यहाँ\s*अनुपयुक्त\s*है'),
]

def is_placeholder(s):
    return isinstance(s, str) and any(p.search(s) for p in PLACEHOLDER_PATTERNS)

qs = json.loads((ROOT / 'data' / 'questions.json').read_text(encoding='utf-8'))
items = qs.get('questions', [])

# Tally
expl_hi_placeholder = 0
expl_hi_real = 0
expl_hi_missing = 0
expl_en_present_in_placeholder = 0  # has English source, non-empty
expl_en_missing_in_placeholder = 0  # English source is empty/null
expl_en_field_present_str_empty = 0

distractor_hi_total = 0
distractor_hi_placeholder = 0
distractor_en_present = 0

# What does the data look like? Sample a few placeholder entries
samples = []
for q in items:
    eh = q.get('explanation_hi')
    if eh:
        if is_placeholder(eh):
            expl_hi_placeholder += 1
            en = q.get('explanation') or q.get('explanation_en')
            if en and isinstance(en, str) and en.strip():
                expl_en_present_in_placeholder += 1
                if len(samples) < 5:
                    samples.append({
                        'id': q.get('id'),
                        'patternId': q.get('patternId'),
                        'stem_html': q.get('stem_html', '')[:80],
                        'choices': q.get('choices', []),
                        'correctIndex': q.get('correctIndex'),
                        'explanation_en': en[:200],
                        'explanation_hi': eh[:100],
                    })
            elif en is None:
                expl_en_missing_in_placeholder += 1
            else:
                expl_en_field_present_str_empty += 1
        else:
            expl_hi_real += 1
    else:
        expl_hi_missing += 1

    de = q.get('distractor_explanations_hi')
    if isinstance(de, dict):
        for k, v in de.items():
            distractor_hi_total += 1
            if is_placeholder(v):
                distractor_hi_placeholder += 1
            de_en = (q.get('distractor_explanations') or {}).get(k)
            if de_en:
                distractor_en_present += 1
    elif isinstance(de, list):
        for v in de:
            distractor_hi_total += 1
            if is_placeholder(v):
                distractor_hi_placeholder += 1

print(f"Total questions: {len(items)}")
print(f"\nexplanation_hi:")
print(f"  Real (non-placeholder):           {expl_hi_real}")
print(f"  Placeholder:                       {expl_hi_placeholder}")
print(f"  Missing/empty:                     {expl_hi_missing}")
print(f"  Of placeholders, with EN source:   {expl_en_present_in_placeholder}")
print(f"  Of placeholders, EN source missing: {expl_en_missing_in_placeholder}")
print(f"\ndistractor_explanations_hi:")
print(f"  Total slots:                       {distractor_hi_total}")
print(f"  Placeholder slots:                 {distractor_hi_placeholder}")
print(f"  With EN distractor source:         {distractor_en_present}")

print(f"\nSample placeholder entries (5):")
for s in samples:
    print(f"\n  --- {s['id']} (patternId: {s['patternId']}) ---")
    print(f"  stem: {s['stem_html']}")
    print(f"  choices: {s['choices']}")
    print(f"  correctIndex: {s['correctIndex']}")
    print(f"  explanation_en: {s['explanation_en']}")
    print(f"  explanation_hi (placeholder): {s['explanation_hi']}")
