"""Inventory every Hindi-bearing field across N5 content + UI surfaces.

Outputs which keys carry Hindi values, their per-file counts, and a
sample value for each, so the audit prompt can name the exact schema
slots to verify.
"""
from __future__ import annotations
import io
import json
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent

# Heuristic: any key matching one of these patterns is a Hindi-bearing slot.
HI_KEY_PATTERNS = [
    lambda k: k == 'hi',
    lambda k: k.endswith('_hi'),
    lambda k: k.endswith('.hi'),
    lambda k: '_hi_' in k,
    lambda k: k == 'gloss_hi',
    lambda k: k == 'meanings_hi',
    lambda k: k == 'meaning_hi',
    lambda k: k == 'explanation_hi',
    lambda k: k == 'rationale_hi',
    lambda k: k == 'note_hi',
    lambda k: k == 'notes_hi',
    lambda k: k == 'l1_hindi',
    lambda k: k == 'hint_hi',
    lambda k: k == 'summary_hi',
    lambda k: k == 'description_hi',
]

def is_hi_key(k: str) -> bool:
    return any(p(k) for p in HI_KEY_PATTERNS)

# Devanagari Unicode range: 0900-097F + 0980-09FF (extended)
def has_devanagari(s: str) -> bool:
    return any('ऀ' <= ch <= 'ॿ' for ch in s)

def looks_romanized_hindi(s: str) -> bool:
    """Heuristic: lowercase ASCII Hindi-typical bigrams."""
    if has_devanagari(s):
        return False
    if not s or len(s.strip()) < 3:
        return False
    bigrams = ('aa', 'ee', 'ii', 'oo', 'kh', 'gh', 'ch', 'jh', 'th', 'dh', 'ph', 'bh', 'sh', 'mh')
    s_low = s.lower()
    return sum(1 for bg in bigrams if bg in s_low) >= 2

# Walk content data
def walk(node, path, hits):
    if isinstance(node, dict):
        for k, v in node.items():
            new_path = f'{path}.{k}' if path else k
            if isinstance(k, str) and is_hi_key(k):
                hits.append((new_path, v))
            walk(v, new_path, hits)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk(item, f'{path}[{i}]', hits)

def analyze_file(p: Path):
    try:
        data = json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        print(f'  !! {p.name}: failed to parse — {e}')
        return
    hits = []
    walk(data, '', hits)
    if not hits:
        return
    by_key = defaultdict(list)
    for path, val in hits:
        # Normalize path to last component (the key name) for grouping
        last = path.rsplit('.', 1)[-1].split('[')[0]
        by_key[last].append((path, val))
    print(f'\n=== {p.relative_to(ROOT)} ===')
    print(f'  Total Hindi-key occurrences: {len(hits)}')
    for key, examples in sorted(by_key.items(), key=lambda x: -len(x[1])):
        empty = sum(1 for _, v in examples if v in (None, '', []))
        non_devan = sum(1 for _, v in examples if isinstance(v, str) and v.strip() and not has_devanagari(v))
        romanized = sum(1 for _, v in examples if isinstance(v, str) and looks_romanized_hindi(v))
        print(f'  {key:<30} count={len(examples):<5} empty={empty:<4} no-devanagari={non_devan:<4} looks-romanized={romanized}')
        # Show first non-empty sample
        for path, v in examples:
            if v not in (None, '', []) and isinstance(v, (str, list)):
                sample = str(v)[:80].replace('\n', ' ')
                print(f'    sample @ {path}: {sample}')
                break

# Locale UI files
print('## Locale UI files')
for lf in sorted((ROOT / 'locales').glob('*.json')):
    print(f'\n=== locales/{lf.name} ===')
    data = json.loads(lf.read_text(encoding='utf-8'))
    if isinstance(data, dict):
        # Flatten keys
        def flat(d, prefix=''):
            out = []
            if isinstance(d, dict):
                for k, v in d.items():
                    out.extend(flat(v, f'{prefix}.{k}' if prefix else k))
            elif isinstance(d, str):
                out.append((prefix, d))
            return out
        kv = flat(data)
        empty = sum(1 for _, v in kv if not (v or '').strip())
        if lf.stem == 'hi':
            non_devan = sum(1 for k, v in kv if v and not has_devanagari(v))
            print(f'  Total UI strings: {len(kv)}')
            print(f'  Empty values: {empty}')
            print(f'  Non-Devanagari values: {non_devan}')
            # Show sample non-Devanagari (likely gaps)
            non_d_samples = [(k, v) for k, v in kv if v and not has_devanagari(v)][:20]
            if non_d_samples:
                print('  Non-Devanagari samples (potential English passthroughs):')
                for k, v in non_d_samples:
                    print(f'    {k}: {v[:60]!r}')
        else:
            print(f'  Total UI strings: {len(kv)}')
            print(f'  Empty values: {empty}')

print('\n## Content data files')
for f in sorted((ROOT / 'data').glob('*.json')):
    if f.name in ('audio_manifest.json', 'audio_manifest_voice.json', 'version.json',
                  'recording_directions.json', 'branding.json',
                  'n5_kanji_readings.json', 'n5_kanji_whitelist.json',
                  'n5_vocab_whitelist.json', 'n5_core_pattern_ids.json',
                  'dokkai_kanji_exception.json'):
        continue
    analyze_file(f)

print('\n## Paper files (data/papers/**)')
papers_root = ROOT / 'data' / 'papers'
if papers_root.exists():
    paper_files = list(papers_root.rglob('*.json'))
    print(f'  Total paper files: {len(paper_files)}')
    # Aggregate counts
    hi_keys_total = defaultdict(int)
    files_with_hi = 0
    files_without_hi = 0
    for p in paper_files:
        try:
            data = json.loads(p.read_text(encoding='utf-8'))
        except Exception:
            continue
        hits = []
        walk(data, '', hits)
        if hits:
            files_with_hi += 1
            for path, val in hits:
                last = path.rsplit('.', 1)[-1].split('[')[0]
                hi_keys_total[last] += 1
        else:
            files_without_hi += 1
    print(f'  Files with Hindi keys: {files_with_hi}')
    print(f'  Files WITHOUT any Hindi key: {files_without_hi}')
    print(f'  Aggregate key counts:')
    for k, c in sorted(hi_keys_total.items(), key=lambda x: -x[1]):
        print(f'    {k}: {c}')
