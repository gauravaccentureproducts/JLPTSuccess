"""Sample Hindi entries across N5 content surfaces for native-scholar review.

Outputs deterministic random samples (seeded) of:
  - vocab.json gloss_hi
  - kanji.json meanings_hi
  - grammar.json meaning_hi + explanation_hi + l1_notes.hi
  - listening.json explanation_hi
  - reading.json summary_hi + explanation_hi
  - questions.json explanation_hi + distractor_explanations_hi
  - locales/hi.json (full dump)

For each sample, prints English source + Hindi target side-by-side so
the rubric (R-1..R-7) can be applied by a reviewer.
"""
from __future__ import annotations
import io
import json
import random
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Walk up until we find the N5 root (where data/ lives)
ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
random.seed(20260507)  # deterministic

def line(): print('-' * 72)

# ============================================================================
# VOCAB — 25 random entries
# ============================================================================
print('=' * 72)
print('VOCAB.JSON gloss_hi — 25 random entries')
print('=' * 72)
vocab = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))
v_entries = vocab.get('entries', vocab.get('items', []))
v_sample = random.sample(v_entries, min(25, len(v_entries)))
for e in v_sample:
    line()
    print(f"id: {e.get('id', '?')}  pos: {e.get('pos', '?')}")
    print(f"lemma: {e.get('lemma', e.get('form', '?'))}")
    print(f"reading: {e.get('reading', '?')}")
    print(f"gloss (en): {e.get('gloss', '?')}")
    print(f"gloss_hi:   {e.get('gloss_hi', '<MISSING>')}")

# ============================================================================
# KANJI — 20 random entries
# ============================================================================
print('\n' + '=' * 72)
print('KANJI.JSON meanings_hi — 20 random entries')
print('=' * 72)
kanji = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
k_entries = kanji.get('entries', [])
k_sample = random.sample(k_entries, min(20, len(k_entries)))
for e in k_sample:
    line()
    print(f"char: {e.get('char', e.get('kanji', '?'))}  id: {e.get('id', '?')}")
    print(f"meanings (en):  {e.get('meanings', '?')}")
    print(f"meanings_hi:    {e.get('meanings_hi', '<MISSING>')}")
    print(f"on:  {e.get('on', '?')}   kun: {e.get('kun', '?')}")

# ============================================================================
# GRAMMAR — 12 patterns (meaning_hi + explanation_hi + l1_notes.hi)
# ============================================================================
print('\n' + '=' * 72)
print('GRAMMAR.JSON — 12 random patterns')
print('=' * 72)
gram = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))
g_entries = gram.get('patterns', [])
g_sample = random.sample(g_entries, min(12, len(g_entries)))
for e in g_sample:
    line()
    print(f"id: {e.get('id', '?')}")
    print(f"pattern: {e.get('pattern', '?')}")
    print(f"meaning (en):  {e.get('meaning', e.get('meaning_en', '?'))}")
    print(f"meaning_hi:    {e.get('meaning_hi', '<MISSING>')}")
    print(f"explanation (en):")
    print(f"  {str(e.get('explanation', e.get('explanation_en', '?')))[:300]}")
    print(f"explanation_hi:")
    print(f"  {str(e.get('explanation_hi', '<MISSING>'))[:300]}")
    l1n = e.get('l1_notes', {})
    if isinstance(l1n, dict) and l1n.get('hi'):
        print(f"l1_notes.hi:")
        print(f"  {str(l1n['hi'])[:400]}")

# ============================================================================
# LISTENING — 8 random items
# ============================================================================
print('\n' + '=' * 72)
print('LISTENING.JSON explanation_hi — 8 random items')
print('=' * 72)
listen = json.loads((ROOT / 'data' / 'listening.json').read_text(encoding='utf-8'))
l_items = listen.get('items', [])
l_sample = random.sample(l_items, min(8, len(l_items)))
for e in l_sample:
    line()
    print(f"id: {e.get('id', '?')}  mondai: {e.get('mondai', '?')}")
    print(f"prompt_en: {str(e.get('prompt_en', e.get('question_en', '?')))[:120]}")
    print(f"explanation (en):")
    print(f"  {str(e.get('explanation', e.get('explanation_en', '?')))[:300]}")
    print(f"explanation_hi:")
    print(f"  {str(e.get('explanation_hi', '<MISSING>'))[:300]}")

# ============================================================================
# READING — 6 passages (summary_hi)
# ============================================================================
print('\n' + '=' * 72)
print('READING.JSON summary_hi — 6 random passages')
print('=' * 72)
read = json.loads((ROOT / 'data' / 'reading.json').read_text(encoding='utf-8'))
r_passages = read.get('passages', [])
r_sample = random.sample(r_passages, min(6, len(r_passages)))
for e in r_sample:
    line()
    print(f"id: {e.get('id', '?')}")
    print(f"summary (en): {str(e.get('summary', e.get('summary_en', '?')))[:200]}")
    print(f"summary_hi:   {str(e.get('summary_hi', '<MISSING>'))[:300]}")

# Plus 5 reading questions
print('\nReading-question explanation_hi — 5 random:')
r_qs = []
for p in r_passages:
    for q in p.get('questions', []):
        if q.get('explanation_hi'):
            r_qs.append((p.get('id', '?'), q))
if r_qs:
    rq_sample = random.sample(r_qs, min(5, len(r_qs)))
    for pid, q in rq_sample:
        line()
        print(f"{pid} > {q.get('id', '?')}")
        print(f"explanation (en):  {str(q.get('explanation', '?'))[:200]}")
        print(f"explanation_hi:    {str(q.get('explanation_hi', '?'))[:250]}")

# ============================================================================
# QUESTIONS — 20 random (explanation_hi + distractor_explanations_hi)
# ============================================================================
print('\n' + '=' * 72)
print('QUESTIONS.JSON — 20 random with explanation_hi')
print('=' * 72)
qs = json.loads((ROOT / 'data' / 'questions.json').read_text(encoding='utf-8'))
q_items = qs.get('questions', [])
q_with_hi = [q for q in q_items if q.get('explanation_hi')]
q_sample = random.sample(q_with_hi, min(20, len(q_with_hi)))
for q in q_sample:
    line()
    print(f"id: {q.get('id', '?')}  patternId: {q.get('patternId', '?')}")
    print(f"stem: {str(q.get('stem', q.get('stem_html', '?')))[:120]}")
    print(f"explanation (en):  {str(q.get('explanation', '?'))[:200]}")
    print(f"explanation_hi:    {str(q.get('explanation_hi', '?'))[:250]}")
    de = q.get('distractor_explanations_hi')
    if de:
        print(f"distractor_explanations_hi:")
        if isinstance(de, list):
            for i, d in enumerate(de):
                print(f"  [{i}] {str(d)[:150]}")
        elif isinstance(de, dict):
            for k, v in list(de.items())[:4]:
                print(f"  [{k}] {str(v)[:150]}")

# ============================================================================
# UI — full dump of locales/hi.json
# ============================================================================
print('\n' + '=' * 72)
print('LOCALES/HI.JSON — full dump (125 strings)')
print('=' * 72)
hi_ui = json.loads((ROOT / 'locales' / 'hi.json').read_text(encoding='utf-8'))
en_ui = json.loads((ROOT / 'locales' / 'en.json').read_text(encoding='utf-8'))
def flat(d, prefix=''):
    out = []
    if isinstance(d, dict):
        for k, v in d.items():
            out.extend(flat(v, f'{prefix}.{k}' if prefix else k))
    else:
        out.append((prefix, d))
    return out
hi_flat = dict(flat(hi_ui))
en_flat = dict(flat(en_ui))
all_keys = sorted(set(hi_flat.keys()) | set(en_flat.keys()))
for k in all_keys:
    hi_v = hi_flat.get(k, '<MISSING>')
    en_v = en_flat.get(k, '<MISSING>')
    print(f"{k}")
    print(f"  en: {en_v!r}")
    print(f"  hi: {hi_v!r}")

# ============================================================================
# PAPER FILES — confirm coverage gap (ONE sample, since linkage = option a)
# ============================================================================
print('\n' + '=' * 72)
print('PAPER FILES — coverage gap confirm (3 random questions)')
print('=' * 72)
paper_files = list((ROOT / 'data' / 'papers').rglob('*.json'))
paper_files = [p for p in paper_files if p.name != 'manifest.json']
sample_papers = random.sample(paper_files, min(3, len(paper_files)))
for pf in sample_papers:
    line()
    print(f'paper: {pf.relative_to(ROOT)}')
    pdata = json.loads(pf.read_text(encoding='utf-8'))
    qs = pdata.get('questions', [])
    if qs:
        q = qs[0]
        print(f"first question id: {q.get('id', '?')}")
        print(f"  rationale (en): {str(q.get('rationale', '?'))[:150]}")
        print(f"  rationale_hi:   {q.get('rationale_hi', '<MISSING>')}")
