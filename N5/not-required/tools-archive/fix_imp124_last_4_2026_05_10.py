"""IMP-124 last-mile: top up the final 4 patterns to >=7 each."""
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
    'n5-038': {'ja': 'すこしずつ にほんごが じょうずに なります。', 'translation_en': 'Little by little, my Japanese is getting better.'},
    'n5-063': {'ja': 'もう かえりましょうか。', 'translation_en': 'Shall we go home now?'},
    'n5-112': {'ja': 'じゅうごふん まちました。', 'translation_en': 'I waited 15 minutes.'},
    'n5-187': {'ja': 'いつか おかあさんに 会いたいです。', 'translation_en': 'Someday I want to meet your mother.'},
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
        continue
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

from collections import Counter
counts = Counter(len(p.get('examples') or []) for p in patterns)
at7 = sum(c for n, c in counts.items() if n >= 7)
print(f'Patches: {added}')
print(f'Final >=7: {at7}/{len(patterns)} ({100*at7/len(patterns):.0f}%)')
