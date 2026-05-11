"""Fill the 11 most-confident missing `lookalikes` entries on
data/kanji.json.

Audit context: the 2026-05-09 richness audit flagged 14/106 kanji
without `lookalikes`. Of those 14, 11 have clear in-N5 visual
confusion partners; the remaining 3 (何, 長, 私) lack strong N5
lookalike candidates and stay empty rather than carry forced/weak
links.

Each lookalike list keeps only N5 kanji (preserves the closed-set
contract). Provenance: `llm_curated`.

Curated mappings:
  万 -> [力, 九]   simple 2-3-stroke shape similarity
  金 -> [今, 会, 食]  share 人 top component
  土 -> [上]       simple cross-stroke
  曜 -> [日, 月]    weekday-component kanji
  員 -> [買, 円]    member/buy/yen share 貝/口 internals
  大 -> [人]       center-peak silhouette
  小 -> [川]       vertical-stroke pattern
  川 -> [三, 小]    minimal-stroke patterns
  買 -> [員]       share 貝 inside
  番 -> [田]       田 inside 番
  号 -> [口]       号 has 口 component

Skipped (no high-confidence N5 partner):
  何 (only 亻-radical link is weak; textbook partners 河/化 not in N5)
  長 (textbook partners 表/衣 not in N5)
  私 (禾-radical is unique in N5; 厶 component partner 公 not in N5)
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

MAPPINGS = {
    '万': ['力', '九'],
    '金': ['今', '会', '食'],
    '土': ['上'],
    '曜': ['日', '月'],
    '員': ['買', '円'],
    '大': ['人'],
    '小': ['川'],
    '川': ['三', '小'],
    '買': ['員'],
    '番': ['田'],
    '号': ['口'],
}


def main() -> int:
    fp = ROOT / 'data' / 'kanji.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_lookalikes_fill')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    entries = data.get('entries', data) if isinstance(data, dict) else data
    if isinstance(entries, dict):
        entries_iter = entries.values()
    else:
        entries_iter = entries

    by_glyph = {e.get('glyph'): e for e in entries_iter}
    n5_glyphs = set(by_glyph.keys())

    n = 0
    for glyph, lookalikes in MAPPINGS.items():
        if glyph not in by_glyph:
            print(f'  ! missing in data: {glyph}')
            continue
        e = by_glyph[glyph]
        if e.get('lookalikes'):
            print(f'  - skip (already filled): {glyph}')
            continue
        # Filter to in-N5 only (belt-and-suspenders)
        filtered = [l for l in lookalikes if l in n5_glyphs]
        if not filtered:
            print(f'  ! {glyph}: no in-N5 lookalikes after filter')
            continue
        e['lookalikes'] = filtered
        e['lookalikes_provenance'] = 'llm_curated'
        n += 1
        print(f'  + {glyph}: {filtered}')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nFilled {n} lookalikes entries.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
