"""Build bidirectional cross-links between data/authentic.json
cards and data/kanji.json entries.

Companion to fill_authentic_refs_2026_05_11.py (which did
vocab <-> authentic). This pass adds the kanji <-> authentic
direction.

For each authentic card, scan card.ja for every character that
appears in the N5 kanji whitelist. Each match becomes:
  - On the card: `kanji_refs: ["n5.kanji.XXX", ...]`
  - On the kanji entry: `authentic_refs: ["auth.X.Y", ...]`

Strategy: pure character-membership scan. No POS or context
inference. Provenance: auto_derived.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def main() -> int:
    auth_fp = ROOT / 'data' / 'authentic.json'
    kanji_fp = ROOT / 'data' / 'kanji.json'

    auth_bak = auth_fp.with_suffix('.json.bak_2026_05_11_authentic_kanji')
    kanji_bak = kanji_fp.with_suffix('.json.bak_2026_05_11_authentic_kanji')
    if not auth_bak.exists():
        shutil.copy2(auth_fp, auth_bak)
        print(f'Backup: {auth_bak.name}')
    if not kanji_bak.exists():
        shutil.copy2(kanji_fp, kanji_bak)
        print(f'Backup: {kanji_bak.name}')

    auth_data = json.loads(auth_fp.read_text(encoding='utf-8'))
    kanji_data = json.loads(kanji_fp.read_text(encoding='utf-8'))

    entries = kanji_data.get('entries', kanji_data) if isinstance(kanji_data, dict) else kanji_data
    entries_iter = entries.values() if isinstance(entries, dict) else entries
    by_glyph = {e.get('glyph'): e for e in entries_iter}

    cards_written = 0
    kanji_written = 0
    for card in auth_data['items']:
        ja = card.get('ja', '') or ''
        used_ids: list[str] = []
        for ch in ja:
            if ch in by_glyph:
                kid = by_glyph[ch].get('id')
                if kid and kid not in used_ids:
                    used_ids.append(kid)
        if not used_ids:
            continue

        # Write kanji_refs on the card (preserve existing)
        existing = card.get('kanji_refs') or []
        new = [k for k in used_ids if k not in existing]
        if new:
            card['kanji_refs'] = existing + new
            card['kanji_refs_provenance'] = 'auto_derived'
            cards_written += 1
            print(f'  + card {card["id"]}: {[k.split(".")[-1] for k in new]}')

        # Write authentic_refs on each kanji entry (preserve existing)
        for kid in used_ids:
            ke = by_glyph.get(ja_to_glyph(kid)) or None
            # Actually look up by id rather than via the glyph back-pointer
            target = next((e for e in (entries.values() if isinstance(entries, dict) else entries) if e.get('id') == kid), None)
            if not target:
                continue
            arefs = target.get('authentic_refs') or []
            if card['id'] not in arefs:
                target['authentic_refs'] = arefs + [card['id']]
                target['authentic_refs_provenance'] = 'auto_derived'
                kanji_written += 1

    auth_fp.write_text(json.dumps(auth_data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    kanji_fp.write_text(json.dumps(kanji_data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print(f'\nCards updated with kanji_refs: {cards_written}')
    print(f'Kanji entries with authentic_refs added: {kanji_written}')
    return 0


def ja_to_glyph(kid: str) -> str:
    """Pull the glyph from a kanji id like "n5.kanji.大"."""
    parts = kid.split('.')
    return parts[-1] if parts else ''


if __name__ == '__main__':
    sys.exit(main())
