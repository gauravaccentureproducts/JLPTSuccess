"""IMP-131: auto-scan vocab.json for each N5 kanji and populate
the kanji entry's examples array with up to 10 vocab cross-links.

Sorts by:
  1. position-of-kanji-in-lemma (kanji at start preferred)
  2. lemma length (shorter preferred)
  3. lemma alphabetical
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

vocab = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))
v_entries = vocab['entries']

kpath = ROOT / 'data' / 'kanji.json'
kdata = json.loads(kpath.read_text(encoding='utf-8'))
k_entries = kdata['entries']

# Pre-build vocab index: glyph → list of (lemma_position, lemma, entry)
vocab_by_kanji = {}
for v in v_entries:
    lemma = v.get('lemma') or v.get('form') or ''
    if not lemma:
        continue
    for i, ch in enumerate(lemma):
        if '一' <= ch <= '鿿':  # CJK Unified Ideographs
            vocab_by_kanji.setdefault(ch, []).append((i, len(lemma), lemma, v))

updated = 0
total_links = 0
for k in k_entries:
    glyph = k.get('glyph') or k.get('char') or k.get('id', '').split('.')[-1]
    if not glyph:
        continue
    candidates = vocab_by_kanji.get(glyph, [])
    if not candidates:
        continue

    # Sort: kanji-at-start (position 0) first, then by lemma length, then alphabetical
    candidates.sort(key=lambda x: (x[0], x[1], x[2]))

    # Take up to 10
    selected = candidates[:10]

    # Existing examples — preserve manual ones; only add auto-derived
    existing = k.get('examples') or []
    existing_lemmas = set()
    for ex in existing:
        if isinstance(ex, dict):
            l = ex.get('lemma') or ex.get('form') or ex.get('vocab_form')
            if l:
                existing_lemmas.add(l)

    new_examples = list(existing) if isinstance(existing, list) else []
    for pos, lng, lemma, v_entry in selected:
        if lemma in existing_lemmas:
            continue
        new_examples.append({
            'lemma': lemma,
            'reading': v_entry.get('reading'),
            'gloss': v_entry.get('gloss'),
            'vocab_id': v_entry.get('id'),
            'auto_derived': True,
        })
        existing_lemmas.add(lemma)

    if len(new_examples) > len(existing):
        k['examples'] = new_examples
        updated += 1
        total_links += len(new_examples) - len(existing)

kpath.write_text(json.dumps(kdata, ensure_ascii=False, indent=2) + '\n',
                 encoding='utf-8')

# Stats
kanji_with_5plus = sum(1 for k in k_entries if len(k.get('examples', []) or []) >= 5)
print(f'Updated {updated} kanji entries')
print(f'Added {total_links} new vocab cross-links total')
print(f'Kanji with ≥5 vocab cross-links: {kanji_with_5plus}/{len(k_entries)} ({100*kanji_with_5plus/len(k_entries):.0f}%)')
