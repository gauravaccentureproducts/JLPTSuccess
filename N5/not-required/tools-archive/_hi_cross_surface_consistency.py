"""R-7 cross-surface consistency check: find Japanese vocab/grammar tokens
that have different Hindi glosses across vocab.json / kanji.json / grammar.json
/ questions.json. Surfaces inconsistencies that would confuse a learner.
"""
from __future__ import annotations
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Build the canonical vocab → gloss_hi map from vocab.json (1000 entries)
vocab = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))
canonical = {}  # (lemma, reading) -> gloss_hi
for e in vocab.get('entries', []):
    lemma = e.get('lemma') or e.get('form')
    reading = e.get('reading')
    gh = e.get('gloss_hi')
    if lemma and gh:
        canonical[lemma] = gh

# Same for kanji
kanji = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
kanji_canonical = {}
for e in kanji.get('entries', []):
    char = e.get('char') or e.get('id', '').split('.')[-1]
    mh = e.get('meanings_hi')
    if char and mh:
        kanji_canonical[char] = mh[0] if isinstance(mh, list) and mh else str(mh)

# Now scan grammar.json + questions.json + papers for occurrences of these tokens
# inside Hindi explanations. When a token appears with a Hindi gloss in parens
# right after, check it matches the canonical.

PAREN_GLOSS_RE = re.compile(r'([ぁ-ゖァ-ヺ一-龯]+)\s*\(([^)]+)\)')

def find_glosses_in_text(text):
    """Return list of (japanese_token, gloss_in_parens) pairs."""
    if not isinstance(text, str):
        return []
    pairs = []
    for m in PAREN_GLOSS_RE.finditer(text):
        ja = m.group(1)
        gloss = m.group(2).strip()
        # Only if gloss looks like Hindi (not English, not romaji)
        if any('ऀ' <= ch <= 'ॿ' for ch in gloss):
            pairs.append((ja, gloss))
    return pairs

# Walk all *_hi fields
inconsistencies = defaultdict(list)  # ja_token -> [(file, path, gloss_in_text, canonical_gloss)]
checked_count = 0

def walk(node, path, file_label):
    global checked_count
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(k, str) and (k.endswith('_hi') or k == 'hi') and isinstance(v, str):
                pairs = find_glosses_in_text(v)
                for ja, gloss_in_text in pairs:
                    checked_count += 1
                    if ja in canonical:
                        canon = canonical[ja]
                        # Allow synonyms / minor variations: only flag if neither
                        # gloss is a substring of the other AND they differ
                        # significantly
                        if (gloss_in_text != canon
                            and gloss_in_text not in canon
                            and canon not in gloss_in_text):
                            inconsistencies[ja].append(
                                (file_label, f'{path}.{k}', gloss_in_text, canon)
                            )
            walk(v, f'{path}.{k}' if path else k, file_label)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk(item, f'{path}[{i}]', file_label)


for fname in ['grammar.json', 'questions.json', 'reading.json', 'listening.json']:
    p = ROOT / 'data' / fname
    if p.exists():
        walk(json.loads(p.read_text(encoding='utf-8')), '', fname)

papers_dir = ROOT / 'data' / 'papers'
if papers_dir.exists():
    for pf in papers_dir.rglob('*.json'):
        if pf.name == 'manifest.json':
            continue
        walk(json.loads(pf.read_text(encoding='utf-8')),
             '', f'papers/{pf.parent.name}/{pf.name}')

print(f'Tokens checked: {checked_count}')
print(f'Tokens with cross-surface inconsistency: {len(inconsistencies)}')
print()
for ja, occurrences in sorted(inconsistencies.items(), key=lambda x: -len(x[1]))[:30]:
    canon = occurrences[0][3]
    print(f"\n{ja}  (canonical: {canon})")
    seen = set()
    for file_label, path, gloss_in_text, _ in occurrences[:5]:
        key = gloss_in_text
        if key in seen:
            continue
        seen.add(key)
        print(f"  {file_label}::{path[:80]}")
        print(f"    in-text: {gloss_in_text}")
