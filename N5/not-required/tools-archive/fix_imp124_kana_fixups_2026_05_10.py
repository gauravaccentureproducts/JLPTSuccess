"""IMP-124 follow-up cleanup: add the 5 examples that the previous
authored-examples pass skipped because they used out-of-scope kanji
(開, 作, 歩, 帰). Same content, kana versions, idempotent (skips
duplicates by JA text)."""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

PATCHES = {
    'n5-063': {'ja': 'まどを あけましょうか。', 'translation_en': 'Shall I open the window?'},
    'n5-135': {'ja': 'これは 母が つくった ケーキです。', 'translation_en': 'This is the cake my mother made.'},
    'n5-144': {'ja': 'あるきながら、でんわで 話さないでください。', 'translation_en': "Please don't talk on the phone while walking."},
    'n5-176': {'ja': 'もう かえらなくちゃ。', 'translation_en': 'I gotta go home now.'},
    'n5-180': {'ja': 'この りょうりの つくりかたは かんたんです。', 'translation_en': 'How to make this dish is simple.'},
}

grammar_path = ROOT / 'data' / 'grammar.json'
data = json.loads(grammar_path.read_text(encoding='utf-8'))
patterns = data['patterns']

added = 0
for p in patterns:
    pid = p['id']
    if pid not in PATCHES:
        continue
    payload = PATCHES[pid]
    examples = p.get('examples') or []
    if any(ex.get('ja') == payload['ja'] for ex in examples):
        continue  # idempotent
    examples.append({
        'ja': payload['ja'],
        'translation_en': payload['translation_en'],
        'provenance': 'llm_curated',
    })
    p['examples'] = examples
    added += 1

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final coverage
from collections import Counter
counts = Counter(len(p.get('examples') or []) for p in patterns)
at7 = sum(c for n, c in counts.items() if n >= 7)
at5 = sum(c for n, c in counts.items() if n >= 5)
print(f'Patches applied:    {added}')
print(f'Coverage:')
print(f'  >=5: {at5}/{len(patterns)} ({100*at5/len(patterns):.0f}%)')
print(f'  >=7: {at7}/{len(patterns)} ({100*at7/len(patterns):.0f}%)')
