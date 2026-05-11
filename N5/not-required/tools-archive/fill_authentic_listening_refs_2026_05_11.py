"""Thematic cross-link between data/listening.json items and
data/authentic.json categories.

Closes the LAST corpus<->authentic direction (after grammar /
vocab / kanji / reading). The listening surface uses
`ambient_context` (station / home / cafe / shop / classroom /
office / clinic / general) as its setting indicator. Map each
specific setting to the matching authentic category.

Mapping (ambient_context -> authentic categories):
  station    -> transit
  cafe       -> menu
  restaurant -> menu
  shop       -> shop
  office     -> notice
  clinic     -> hospital
  home       -> time          (often features schedule/return phrases)
  classroom  -> (skip; no authentic category for "school")
  general    -> (skip; no specific theme)

Each matched listening item gets:
  authentic_categories: ["transit", ...]
  authentic_categories_provenance: "auto_derived"

Provenance: auto_derived (deterministic from ambient_context).
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ambient_context value -> list of authentic categories
CONTEXT_TO_CATEGORIES = {
    'station':    ['transit'],
    'cafe':       ['menu'],
    'restaurant': ['menu'],
    'shop':       ['shop'],
    'office':     ['notice'],
    'clinic':     ['hospital'],
    'home':       ['time'],   # often schedule / return phrases
}


def main() -> int:
    fp = ROOT / 'data' / 'listening.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_authentic_listening')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    items = data['items']

    n = 0
    for it in items:
        ctx = (it.get('ambient_context') or '').lower().strip()
        cats = CONTEXT_TO_CATEGORIES.get(ctx)
        if not cats:
            continue
        if it.get('authentic_categories'):
            continue
        it['authentic_categories'] = list(cats)
        it['authentic_categories_provenance'] = 'auto_derived'
        n += 1
        print(f'  + {it["id"]} ({ctx}) -> {cats}')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nLinked {n} listening items to authentic categories.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
