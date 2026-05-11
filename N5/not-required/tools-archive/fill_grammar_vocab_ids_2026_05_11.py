"""Close the 8 grammar examples still missing `vocab_ids` cross-links.

Audit context: vocab_ids density on grammar examples is 1774/1782
(99.5%). The remaining 8 are short interjection / set-phrase /
suffix examples where the vocab linkage is straightforward.

Curated mappings:
  n5-125.example[8] "じゃ、また。"          -> [] (set-phrase, no countable vocab)
  n5-164.example[8] "すずきさん…"            -> ['n5.vocab.36-greetings.おはようございます'] etc.
  n5-166.example[9] "おはよう ございます。"  -> n5.vocab id for おはようございます if present
  n5-167.example[9] "がくせいなんです。"     -> n5.vocab.がくせい
  n5-177.example[7] "たべすぎました。"       -> n5.vocab.27.食べる (via たべる stem)
  n5-177.example[8] "のみすぎました。"       -> n5.vocab.27.飲む
  n5-181.example[7] "たかいなあ。"           -> n5.vocab.31.たかい
  n5-182.example[9] "たべるな。"             -> n5.vocab.28.食べる

Script validates each id against vocab.json; drops stale ones
silently. Provenance recorded at the example level.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Each entry: (pattern_id, example_index, candidate_vocab_ids)
# Set empty list when no linkable vocab in N5 corpus (e.g., set
# phrase greetings whose canonical vocab entry doesn't include
# the contracted form).
FILLS = [
    ('n5-125', 8, []),  # じゃ、また - casual set phrase, no canonical vocab
    ('n5-164', 8, ['n5.vocab.36-greetings-and-set-phr.おはようございます']),
    ('n5-166', 9, ['n5.vocab.36-greetings-and-set-phr.おはようございます']),
    ('n5-167', 9, ['n5.vocab.24-school-and-study.がくせい']),
    ('n5-177', 7, ['n5.vocab.28-verbs-group-2-verbs.食べる']),
    ('n5-177', 8, ['n5.vocab.27-verbs-group-1-verbs.飲む']),
    ('n5-181', 7, ['n5.vocab.31-adjectives.たかい']),
    ('n5-182', 9, ['n5.vocab.28-verbs-group-2-verbs.食べる']),
]


def main() -> int:
    fp = ROOT / 'data' / 'grammar.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_vocab_ids_fill')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {p['id']: p for p in data['patterns']}

    vocab = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))['entries']
    valid_ids = {e['id'] for e in vocab}

    n = 0
    for pid, idx, ids in FILLS:
        p = by_id.get(pid)
        if not p:
            print(f'  ! pattern not found: {pid}')
            continue
        exs = p.get('examples') or []
        if idx >= len(exs):
            print(f'  ! {pid}.example[{idx}]: index out of range ({len(exs)} examples)')
            continue
        ex = exs[idx]
        if ex.get('vocab_ids'):
            print(f'  - skip {pid}.example[{idx}] (already has vocab_ids)')
            continue
        # Drop stale ids
        filtered = []
        for vid in ids:
            if vid in valid_ids:
                filtered.append(vid)
            else:
                print(f'  ! {pid}.example[{idx}]: stale vocab_id dropped: {vid}')
        ex['vocab_ids'] = filtered  # Empty array is valid (set phrase)
        ex['vocab_ids_provenance'] = 'llm_curated'
        n += 1
        print(f'  + {pid}.example[{idx}]: {filtered}')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nFilled vocab_ids on {n} examples.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
