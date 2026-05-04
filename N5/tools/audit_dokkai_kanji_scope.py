"""Inventory all non-N5 kanji that actually appear in dokkai paper
JSONs, to compare against the documented naturalness-exception list
(see KnowledgeBank/dokkai_questions_n5.md line 17).

This is a read-only audit — no files are modified. Output is a sorted
list of every non-N5 kanji + its frequency + a sample passage. Used
to make the dokkai naturalness exception explicit and complete.
"""
import json
import io
import sys
import re
from collections import Counter
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
KANJI_RE = re.compile(r'[一-鿿]')

whitelist = set(json.loads((ROOT / 'data' / 'n5_kanji_whitelist.json').read_text(encoding='utf-8')))

counts: Counter[str] = Counter()
samples: dict[str, str] = {}

def walk(obj):
    if isinstance(obj, str):
        for ch in obj:
            if KANJI_RE.match(ch) and ch not in whitelist:
                counts[ch] += 1
                if ch not in samples:
                    samples[ch] = obj[:80]
    elif isinstance(obj, dict):
        for v in obj.values():
            walk(v)
    elif isinstance(obj, list):
        for v in obj:
            walk(v)

for p in (ROOT / 'data' / 'papers' / 'dokkai').glob('*.json'):
    walk(json.load(p.open(encoding='utf-8')))

print(f'Non-N5 kanji in data/papers/dokkai/ ({len(counts)} unique):')
for ch, n in counts.most_common():
    print(f'  {ch}  x{n}   sample: {samples[ch]!r}')
