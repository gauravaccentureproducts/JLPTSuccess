"""Fill vocab.honorific_chain on the 67 verbs missing it using
PRODUCTIVE forms (お+stem+する / お+stem+になる).

Audit context: 65/132 verbs have honorific_chain. The iconic
suppletive forms (食べる→召し上がる, 行く→いらっしゃる, etc.) are
already filled. The remaining 67 verbs lack a suppletive honorific
form — for these, native speakers use the PRODUCTIVE pattern:

  - plain:      dictionary form
  - polite:     masu-stem + ます (deterministic from verb_class)
  - humble:     お + masu-stem + する        [kenjoogo]
  - respectful: お + masu-stem + になる      [sonkeigo]
  - note:       'Productive forms — no suppletive honorific exists
                for this verb.'

Stem derivation by verb_class:
  ichidan:   reading minus trailing る
  godan:     reading with final char swapped u-row -> i-row
  irregular: skip (handled separately — most are する-compounds
             which take ご+base+いたします / なさいます productively)

Provenance: auto_derived. The note field explicitly says the forms
are productive (not native canonical), so the renderer / learner
can interpret accordingly.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Godan u-row -> i-row map
GODAN_STEM = {
    'う': 'い', 'く': 'き', 'ぐ': 'ぎ', 'す': 'し', 'つ': 'ち',
    'ぬ': 'に', 'ぶ': 'び', 'む': 'み', 'る': 'り',
}


def derive_stem(reading: str, verb_class: str) -> str | None:
    """Return masu-stem of a verb reading. None if can't derive."""
    if not reading or len(reading) < 2:
        return None
    if verb_class == 'ichidan':
        if reading.endswith('る'):
            return reading[:-1]
        return None
    if verb_class == 'godan':
        last = reading[-1]
        if last not in GODAN_STEM:
            return None
        return reading[:-1] + GODAN_STEM[last]
    return None


def build_chain(reading: str, stem: str) -> dict:
    """Build the productive honorific_chain entry."""
    polite = stem + 'ます'
    humble = 'お' + stem + 'する'
    respectful = 'お' + stem + 'になる'
    return {
        'plain': reading,
        'polite': polite,
        'humble': humble,
        'respectful': respectful,
        'note': 'Productive forms (お+stem+する / お+stem+になる) — no suppletive honorific exists for this verb.',
    }


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_honorific_productive')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    n = 0
    skipped_irregular = 0
    skipped_other = 0

    for e in data['entries']:
        if not e.get('pos', '').startswith('verb'):
            continue
        if e.get('honorific_chain'):
            continue
        reading = e.get('reading') or ''
        vc = e.get('verb_class')

        if vc == 'irregular':
            skipped_irregular += 1
            continue

        stem = derive_stem(reading, vc)
        if not stem:
            skipped_other += 1
            print(f'  ! skip {e.get("form")} ({reading}) vc={vc}: cannot derive stem')
            continue

        e['honorific_chain'] = build_chain(reading, stem)
        e['honorific_chain_provenance'] = 'auto_derived'
        n += 1
        if n <= 8:
            print(f'  + {e.get("form"):<10} ({reading:<8}) -> humble={e["honorific_chain"]["humble"]}, respectful={e["honorific_chain"]["respectful"]}')

    if n > 8:
        print(f'  ... (and {n - 8} more)')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nFilled productive honorific_chain on {n} verbs.')
    print(f'  Skipped (irregular): {skipped_irregular}')
    print(f'  Skipped (no stem):  {skipped_other}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
