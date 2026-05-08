"""Inspect vocab.json schema for pair_id and transitivity fields."""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

d = json.load(open(ROOT / 'data/vocab.json', encoding='utf-8'))
items = d['entries']

# First entry full schema
print('Schema (first entry keys):')
for k in items[0]:
    v = items[0][k]
    print(f'  {k}: {str(v)[:80]}')

# Entries with transitivity fields
print('\nEntries with transitivity-related fields:')
cnt = 0
for e in items:
    fields = {}
    for k in ('transitivity', 'transitivity_pair', 'pair_id', 'pair', 'verb_class'):
        if e.get(k):
            fields[k] = e[k]
    if fields and cnt < 5:
        print(f"  {e.get('lemma', e.get('form', '?')):<10} {e.get('id','?'):<50} {fields}")
        cnt += 1
print(f'\nTotal entries with any pair/transitivity field: {sum(1 for e in items if any(e.get(k) for k in ("transitivity", "transitivity_pair", "pair_id", "pair")))}')

# Find target verbs
TARGETS_PAIRS = [
    ('開ける', 'あける'), ('開く', 'あく'),
    ('閉める', 'しめる'), ('閉まる', 'しまる'),
    ('入れる', 'いれる'), ('入る', 'はいる'),
    ('出す', 'だす'), ('出る', 'でる'),
    ('始める', 'はじめる'), ('始まる', 'はじまる'),
    ('止める', 'やめる'), ('止まる', 'とまる'),
    ('つける', 'つける'), ('つく', 'つく'),
    ('消す', 'けす'), ('消える', 'きえる'),
    ('起こす', 'おこす'), ('起きる', 'おきる'),
    ('落とす', 'おとす'), ('落ちる', 'おちる'),
    ('直す', 'なおす'), ('直る', 'なおる'),
    ('切る', 'きる'), ('切れる', 'きれる'),
]
TARGETS = [t[0] for t in TARGETS_PAIRS] + [t[1] for t in TARGETS_PAIRS]
print('\nFound target verbs in vocab.json:')
for t in TARGETS:
    matches = [e for e in items if (e.get('lemma') or e.get('form')) == t]
    if matches:
        for m in matches:
            tr = m.get('transitivity') or m.get('transitivity_pair') or m.get('pair_id')
            print(f'  {t:<6} id={m.get("id"):<50} transitivity={tr}')
    else:
        print(f'  {t:<6} NOT FOUND')
