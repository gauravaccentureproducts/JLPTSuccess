"""Thematic-category cross-link between reading passages /
listening items and authentic-content categories.

Builds the THIRD direction of the authentic-content layer back-link
(after vocab <-> authentic and kanji <-> authentic). Reading and
listening surfaces don't share word-level identity with authentic
cards, so the link is THEMATIC via topic / category mapping rather
than per-token.

Mapping (reading topic -> authentic category, curated):
  shopping     -> shop
  weather      -> weather
  schedule     -> time
  transport    -> transit
  health       -> hospital
  food         -> menu
  restaurant   -> menu
  directions   -> signs
  nature       -> weather
  calendar     -> time
  communication -> post

Each passage with a mapped topic gets:
  authentic_categories: ["shop", ...]

This is a lightweight pointer (one or two category names) rather
than per-card cross-link, so the renderer can show "Related
authentic content: [signs] [hospital]" inline without spamming
30 individual card links.

For listening, items don't have a topic field (they use
format_type for mondai classification). Skipping for now —
listening->authentic would need authored topic tagging.

Schema (matches the lightweight pointer pattern):
  passage.authentic_categories: list[str] (category names)
  passage.authentic_categories_provenance: "auto_derived"
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Reading topic -> list of authentic categories that thematically apply.
TOPIC_TO_CATEGORIES = {
    'shopping':       ['shop'],
    'weather':        ['weather'],
    'schedule':       ['time'],
    'transport':      ['transit'],
    'health':         ['hospital'],
    'food':           ['menu'],
    'restaurant':     ['menu'],
    'directions':     ['signs'],
    'nature':         ['weather'],
    'calendar':       ['time'],
    'communication':  ['post'],
    'request':        ['shop', 'menu'],  # polite-request style appears in both
    'travel':         ['transit'],
    'workplace':      ['notice'],
    'work':           ['notice'],
    'daily routine':  ['signs', 'time'],
}


def main() -> int:
    fp = ROOT / 'data' / 'reading.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_authentic_thematic')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    passages = data['passages']

    n = 0
    for p in passages:
        topic = (p.get('topic') or '').lower().strip()
        cats = TOPIC_TO_CATEGORIES.get(topic)
        if not cats:
            continue
        if p.get('authentic_categories'):
            continue
        p['authentic_categories'] = list(cats)
        p['authentic_categories_provenance'] = 'auto_derived'
        n += 1
        print(f'  + {p["id"]} ({topic}) -> {cats}')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nLinked {n} reading passages to authentic categories.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
