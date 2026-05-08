"""Inventory current provenance distribution across all Hindi-bearing
surfaces - tells us where Phase 3 (cycle 3) work actually is."""
from __future__ import annotations
import io
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print('## Provenance distribution by surface\n')

# questions.json
qs = json.loads((ROOT / 'data' / 'questions.json').read_text(encoding='utf-8'))
expl_prov = Counter()
dist_prov = Counter()
for q in qs.get('questions', []):
    if q.get('explanation_hi'):
        expl_prov[q.get('explanation_hi_provenance', '?')] += 1
    if q.get('distractor_explanations_hi'):
        dist_prov[q.get('distractor_explanations_hi_provenance', '?')] += 1
print('questions.json explanation_hi_provenance:', dict(expl_prov))
print('questions.json distractor_explanations_hi_provenance:', dict(dist_prov))

# grammar.json
gram = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))
g_meaning = Counter()
g_expl = Counter()
g_l1 = Counter()
def get_prov(node, *keys):
    """Resolve a provenance value that may be a dict {en, hi} OR a flat string."""
    for k in keys:
        v = node.get(k)
        if v is None:
            continue
        if isinstance(v, dict):
            return v.get('hi', '?')
        return v
    return '?'

for p in gram.get('patterns', []):
    if p.get('meaning_hi'):
        g_meaning[get_prov(p, 'meaning_hi_provenance', 'meaning_provenance')] += 1
    if p.get('explanation_hi'):
        g_expl[get_prov(p, 'explanation_hi_provenance', 'explanation_provenance')] += 1
    l1 = p.get('l1_notes', {})
    if isinstance(l1, dict) and l1.get('hi'):
        g_l1[get_prov(p, 'l1_notes_provenance')] += 1
print('\ngrammar.json meaning_hi prov:', dict(g_meaning))
print('grammar.json explanation_hi prov:', dict(g_expl))
print('grammar.json l1_notes.hi prov:', dict(g_l1))

# vocab.json
vocab = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))
v_prov = Counter()
for e in vocab.get('entries', []):
    if e.get('gloss_hi'):
        gp = e.get('gloss_provenance', {})
        if isinstance(gp, dict):
            v_prov[gp.get('hi', '?')] += 1
        else:
            v_prov[gp or '?'] += 1
print('\nvocab.json gloss_hi prov:', dict(v_prov))

# kanji.json
kanji = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
k_prov = Counter()
for e in kanji.get('entries', []):
    if e.get('meanings_hi'):
        mp = e.get('meanings_provenance', {})
        if isinstance(mp, dict):
            k_prov[mp.get('hi', '?')] += 1
        else:
            k_prov[mp or '?'] += 1
print('kanji.json meanings_hi prov:', dict(k_prov))

# listening.json
listen = json.loads((ROOT / 'data' / 'listening.json').read_text(encoding='utf-8'))
l_prov = Counter()
for it in listen.get('items', []):
    if it.get('explanation_hi'):
        l_prov[it.get('explanation_hi_provenance', '?')] += 1
print('listening.json explanation_hi prov:', dict(l_prov))

# reading.json
read = json.loads((ROOT / 'data' / 'reading.json').read_text(encoding='utf-8'))
r_summary = Counter()
r_expl = Counter()
for p in read.get('passages', []):
    if p.get('summary_hi'):
        r_summary[p.get('summary_hi_provenance', '?')] += 1
    for q in p.get('questions', []):
        if q.get('explanation_hi'):
            r_expl[q.get('explanation_hi_provenance', '?')] += 1
print('reading.json summary_hi prov:', dict(r_summary))
print('reading.json q.explanation_hi prov:', dict(r_expl))

# paper files
p_prov = Counter()
for pf in (ROOT / 'data' / 'papers').rglob('*.json'):
    if pf.name == 'manifest.json':
        continue
    pdata = json.loads(pf.read_text(encoding='utf-8'))
    for q in pdata.get('questions', []):
        if q.get('rationale_hi'):
            p_prov[q.get('rationale_hi_provenance', '?')] += 1
print('\npapers/**/*.json rationale_hi prov:', dict(p_prov))
