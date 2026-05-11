"""Fill the 5 missing `n5_compounds` entries on data/kanji.json.

Audit context: the 2026-05-09 richness audit flagged 5/106 kanji
without `n5_compounds` (体-part + 力). All 5 are body-part /
simple-noun kanji that mostly stand alone as N5 vocab; few
compounds appear at the N5 level. We seed each with at least one
direct one-kanji compound (the body-part vocab itself, which is
canonical kanji-form even if N5 vocab.json stores the kana
reading-only spelling), plus any obvious 2-kanji N5 compounds.

Kanji + compounds:
  友 -> 友だち (ともだち)
  手 -> 手 (て), 手紙 (てがみ), 上手 (じょうず)
  足 -> 足 (あし)
  目 -> 目 (め), 番号 (— uses 目's homophone in mind, but actually 番号 doesn't contain 目)
        真面目 (まじめ) — does contain 目
  力 -> 力 (ちから)

Schema (matches existing entries):
  {form, reading, gloss, vocab_id}

Provenance: llm_curated.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

MAPPINGS = {
    '友': [
        {'form': '友だち',  'reading': 'ともだち', 'gloss': 'friend',
         'vocab_id': 'n5.vocab.2-people-family.ともだち'},
    ],
    '手': [
        {'form': '手',     'reading': 'て',       'gloss': 'hand',
         'vocab_id': 'n5.vocab.4-body-parts.て'},
        {'form': '手紙',   'reading': 'てがみ',   'gloss': 'letter',
         'vocab_id': 'n5.vocab.22-money-and-shopping.てがみ'},
        {'form': '上手',   'reading': 'じょうず', 'gloss': 'skilled',
         'vocab_id': 'n5.vocab.32-adjectives.じょうず'},
    ],
    '足': [
        {'form': '足',     'reading': 'あし',     'gloss': 'leg, foot',
         'vocab_id': 'n5.vocab.4-body-parts.あし'},
    ],
    '目': [
        {'form': '目',     'reading': 'め',       'gloss': 'eye',
         'vocab_id': 'n5.vocab.4-body-parts.め'},
    ],
    '力': [
        {'form': '力',     'reading': 'ちから',   'gloss': 'power, strength',
         'vocab_id': None},
    ],
}


def main() -> int:
    fp = ROOT / 'data' / 'kanji.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_n5_compounds_fill')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    entries = data.get('entries', data) if isinstance(data, dict) else data
    entries_iter = entries.values() if isinstance(entries, dict) else entries
    by_glyph = {e.get('glyph'): e for e in entries_iter}

    # Cross-check that vocab_ids exist (drop any that don't).
    vocab = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))['entries']
    valid_ids = {e['id'] for e in vocab}

    n = 0
    for glyph, compounds in MAPPINGS.items():
        if glyph not in by_glyph:
            print(f'  ! missing in data: {glyph}')
            continue
        e = by_glyph[glyph]
        if e.get('n5_compounds'):
            print(f'  - skip (already filled): {glyph}')
            continue
        # Filter out compounds with non-existent vocab_ids; allow None vocab_id.
        filtered = []
        for c in compounds:
            vid = c.get('vocab_id')
            if vid is None or vid in valid_ids:
                filtered.append(c if vid else {k: v for k, v in c.items() if k != 'vocab_id'})
            else:
                print(f'  ! dropping {glyph}: vocab_id not found: {vid}')
        if not filtered:
            print(f'  ! {glyph}: no valid compounds after filter')
            continue
        e['n5_compounds'] = filtered
        e['n5_compounds_provenance'] = 'llm_curated'
        n += 1
        forms = [c['form'] for c in filtered]
        print(f'  + {glyph}: {forms}')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nFilled {n} n5_compounds entries.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
