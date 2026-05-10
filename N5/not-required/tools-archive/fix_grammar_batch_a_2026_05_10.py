"""Grammar Batch A: mechanical fixes
- B1: strip `romaji` field from grammar examples (defeats kana literacy)
- B3: add 5 more 行って te-form examples (irregular conjugation under-exposed)
- G5: auto-derive pitch annotation on each example's head verb/adjective
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

grammar_path = ROOT / 'data' / 'grammar.json'
data = json.loads(grammar_path.read_text(encoding='utf-8'))
patterns = data['patterns']

# --- B1: Strip romaji field from grammar examples ---
print('=== B1: Romaji strip ===')
romaji_stripped = 0
for p in patterns:
    for ex in (p.get('examples') or []):
        if isinstance(ex, dict) and 'romaji' in ex:
            del ex['romaji']
            romaji_stripped += 1
print(f'Romaji fields removed: {romaji_stripped}')

# --- B3: Add 5 more 行って te-form examples ---
# Place under n5-069 (Verb-て pattern) which is the canonical te-form home
print()
print('=== B3: 行って te-form coverage ===')
itte_examples = [
    {
        'ja': '私は あした がっこうへ 行って、しゅくだいを します。',
        'translation_en': 'Tomorrow I will go to school and do my homework.',
        'provenance': 'llm_curated',
    },
    {
        'ja': 'コンビニに 行って、コーヒーを 買いました。',
        'translation_en': 'I went to the convenience store and bought coffee.',
        'provenance': 'llm_curated',
    },
    {
        'ja': 'えきへ 行って、でんしゃに のります。',
        'translation_en': 'Go to the station and take the train.',
        'provenance': 'llm_curated',
    },
    {
        'ja': '友だちと カフェに 行って、はなしました。',
        'translation_en': 'I went to a café with my friend and we talked.',
        'provenance': 'llm_curated',
    },
    {
        'ja': 'うちに 行って、いっしょに 食べませんか。',
        'translation_en': "Won't you come to my house and eat together?",
        'provenance': 'llm_curated',
    },
]

for p in patterns:
    if p['id'] == 'n5-069':
        existing_ja = {ex.get('ja') for ex in (p.get('examples') or []) if ex.get('ja')}
        added = 0
        for ex in itte_examples:
            if ex['ja'] not in existing_ja:
                p['examples'].append(ex)
                added += 1
        print(f'  Added {added} 行って examples to n5-069')
        break

# --- G5: Auto-derive pitch on each example head word ---
# For each example, find vocab entries whose form appears in the JA text and
# tag the example with `pitch_marks: [{form, mora, drop}]`
print()
print('=== G5: Pitch annotations on examples ===')
V = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))['entries']
# Build form->{mora,drop} index for entries with pitch
pitch_index = {}
for v in V:
    if v.get('pitch_accent'):
        form = v.get('form')
        if form:
            pitch_index[form] = v['pitch_accent']
        reading = v.get('reading')
        if reading and reading != form:
            pitch_index[reading] = v['pitch_accent']

# Sort by length desc so longest-match wins
forms_by_len = sorted(pitch_index.keys(), key=lambda s: -len(s))

annotated_examples = 0
for p in patterns:
    for ex in (p.get('examples') or []):
        ja = ex.get('ja') if isinstance(ex, dict) else ''
        if not ja: continue
        # Find up to 3 head words present in this example
        marks = []
        seen = set()
        for f in forms_by_len:
            if len(f) < 2: continue
            if f in ja and f not in seen:
                seen.add(f)
                marks.append({'form': f, **pitch_index[f]})
                if len(marks) >= 3: break
        if marks:
            ex['pitch_marks'] = marks
            annotated_examples += 1

print(f'Examples with pitch_marks: {annotated_examples}')

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final state
print()
print('=== FINAL STATE ===')
total_examples = sum(len(p.get('examples') or []) for p in patterns)
have_romaji = sum(1 for p in patterns for ex in (p.get('examples') or [])
                  if isinstance(ex, dict) and 'romaji' in ex)
have_pitch = sum(1 for p in patterns for ex in (p.get('examples') or [])
                 if isinstance(ex, dict) and ex.get('pitch_marks'))
print(f'Total grammar examples: {total_examples}')
print(f'Examples still with romaji: {have_romaji}')
print(f'Examples with pitch_marks: {have_pitch}')
