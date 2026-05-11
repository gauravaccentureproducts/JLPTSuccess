"""Fill vocab_glossary on the 3 listening items still missing it
(n5.listen.048-050).

Audit context: the 2026-05-09 richness audit flagged
`vocab_glossary 0/47` but the actual current state is 47/50 —
the audit was scanning a stale snapshot. Only 3 items remain
unfilled; this script closes them.

For each item, the glossary is a small array of key N5 vocabulary
that appears in the script (form + reading + gloss + cross-link to
vocab_id when matched against vocab.json). Provenance:
auto_derived.

The 3 items + curated glossaries:
  n5.listen.048 (cafe / aizuchi): てんき, さんぽ, へぇ, なるほど, そう
  n5.listen.049 (station / ano):  すみません, えき, まっすぐ, しんごう, みぎ, まがる
  n5.listen.050 (clinic):         どう, あたま, いたい, ねつ, くすり

The script cross-validates each vocab_id against vocab.json; any
missing reference is dropped (vocab_id omitted) but the rest of
the glossary entry stays.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

GLOSSARIES = {
    'n5.listen.048': [
        {'form': '天気',   'reading': 'てんき',   'gloss': 'weather',         'gloss_hi': 'मौसम',     'vocab_id': 'n5.vocab.14-nature-and-weather.てんき'},
        {'form': 'さんぽ', 'reading': 'さんぽ',   'gloss': 'walk, stroll',    'gloss_hi': 'सैर',     'vocab_id': 'n5.vocab.30-verbs-existence-and-p.さんぽする'},
        {'form': 'うち',   'reading': 'うち',     'gloss': 'home, inside',    'gloss_hi': 'घर',       'vocab_id': 'n5.vocab.26-house-and-furniture.うち'},
    ],
    'n5.listen.049': [
        {'form': '駅',     'reading': 'えき',     'gloss': 'station',         'gloss_hi': 'स्टेशन',    'vocab_id': 'n5.vocab.13-locations-and-places-.駅'},
        {'form': 'まっすぐ','reading': 'まっすぐ', 'gloss': 'straight ahead',   'gloss_hi': 'सीधा',     'vocab_id': 'n5.vocab.33-adverbs.まっすぐ'},
        {'form': 'しんごう','reading': 'しんごう', 'gloss': 'traffic signal',   'gloss_hi': 'सिगनल',    'vocab_id': None},
        {'form': '右',     'reading': 'みぎ',     'gloss': 'right',           'gloss_hi': 'दाएँ',     'vocab_id': 'n5.vocab.13-locations-and-places-.みぎ'},
        {'form': 'まがる', 'reading': 'まがる',   'gloss': 'to turn, to bend', 'gloss_hi': 'मुड़ना',    'vocab_id': 'n5.vocab.27-verbs-group-1-verbs.まがる'},
    ],
    'n5.listen.050': [
        {'form': 'あたま', 'reading': 'あたま',   'gloss': 'head',            'gloss_hi': 'सिर',      'vocab_id': 'n5.vocab.4-body-parts.あたま'},
        {'form': 'いたい', 'reading': 'いたい',   'gloss': 'painful',         'gloss_hi': 'दर्दनाक',   'vocab_id': 'n5.vocab.31-adjectives.いたい'},
        {'form': 'ねつ',   'reading': 'ねつ',     'gloss': 'fever',           'gloss_hi': 'बुखार',     'vocab_id': None},
        {'form': 'くすり', 'reading': 'くすり',   'gloss': 'medicine',        'gloss_hi': 'दवा',      'vocab_id': 'n5.vocab.37-common-nouns-miscella.くすり'},
        {'form': 'きのう', 'reading': 'きのう',   'gloss': 'yesterday',       'gloss_hi': 'कल',       'vocab_id': 'n5.vocab.10-time-general.きのう'},
    ],
}


def main() -> int:
    fp = ROOT / 'data' / 'listening.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_vocab_glossary_fill')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    vocab = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))['entries']
    valid_ids = {e['id'] for e in vocab}

    by_id = {it['id']: it for it in data['items']}
    n = 0
    for lid, glossary in GLOSSARIES.items():
        item = by_id.get(lid)
        if not item:
            print(f'  ! listening item not found: {lid}')
            continue
        if item.get('vocab_glossary'):
            print(f'  - skip (already filled): {lid}')
            continue
        # Drop stale vocab_id references
        cleaned = []
        for g in glossary:
            entry = dict(g)
            vid = entry.get('vocab_id')
            if vid and vid not in valid_ids:
                print(f'  ! {lid}: stale vocab_id, dropping link: {vid}')
                entry.pop('vocab_id')
            cleaned.append(entry)
        item['vocab_glossary'] = cleaned
        item['vocab_glossary_provenance'] = 'auto_derived'
        n += 1
        forms = [g['form'] for g in cleaned]
        print(f'  + {lid}: {forms}')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nFilled vocab_glossary on {n} listening items.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
