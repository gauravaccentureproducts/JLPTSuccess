"""Wave 2 — extend kanji etymology to lesson_order 31-60.

Wave 1 (2026-05-11) covered the first 31 kanji. This wave covers
the next 30 (people / body / school / country / position).
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ETYMOLOGIES = {
    '何': {'origin_type': 'phono_semantic',
           'story': 'A person (亻) carrying something (可). Originally meant "to carry" — borrowed for "what" through phonetic loan in ancient Chinese.'},
    '人': {'origin_type': 'pictograph',
           'story': 'Pictograph of a standing person seen from the side — two legs forming a triangular figure. One of the oldest characters in the Chinese script.'},
    '男': {'origin_type': 'compound_ideograph',
           'story': '田 (rice field) + 力 (strength/plow) — the one who works the fields with strength. Captures the ancient division of agricultural labor by gender.'},
    '女': {'origin_type': 'pictograph',
           'story': 'Pictograph of a kneeling figure with arms folded — the traditional posture of women in ancient East Asian seated etiquette. Highly stylized over time.'},
    '子': {'origin_type': 'pictograph',
           'story': 'Pictograph of a swaddled infant — head + arms + bundled lower body. The horizontal stroke represents the swaddling.'},
    '父': {'origin_type': 'pictograph',
           'story': 'Pictograph of a hand holding an axe / staff — symbol of authority. The "axe-wielder" came to mean "father" as the patriarchal head of the household.'},
    '母': {'origin_type': 'pictograph',
           'story': 'Pictograph of a kneeling woman (女) with two added dots for breasts — emphasizing the nursing / maternal aspect that distinguishes mother from other women.'},
    '友': {'origin_type': 'compound_ideograph',
           'story': 'Two hands (又) reaching toward each other — the gesture of friendship and mutual support. Originally written with two full hands.'},
    '先': {'origin_type': 'compound_ideograph',
           'story': '人 (person) with a vertical stroke and 之 (going) — a person walking ahead of others. Hence "ahead, previous, first, tip".'},
    '生': {'origin_type': 'pictograph',
           'story': 'Pictograph of a plant sprouting from the ground (土) — a young shoot pushing up. Hence the broad sense of "life / birth / produce / grow / raw".'},
    '手': {'origin_type': 'pictograph',
           'story': 'Pictograph of a hand with five fingers spread. The modern form preserves four finger-strokes plus the thumb/palm structure.'},
    '足': {'origin_type': 'pictograph',
           'story': 'Pictograph of a foot/leg with the knee (口 element) on top and the foot at the bottom. Captures the entire lower limb, not just the foot.'},
    '目': {'origin_type': 'pictograph',
           'story': 'Pictograph of an eye seen sideways — originally drawn horizontally, then rotated 90 degrees in the script standardization. The horizontal strokes inside represent the iris/pupil.'},
    '口': {'origin_type': 'pictograph',
           'story': 'Pictograph of an open mouth — a square enclosure representing the opening. Used as both a character and a radical in many other characters.'},
    '力': {'origin_type': 'pictograph',
           'story': 'Pictograph of a plow / muscular arm — strength in action. The bent shape represents the plow handle or a flexed bicep, depending on the etymological school.'},
    '学': {'origin_type': 'compound_ideograph',
           'story': 'Simplified from 學 — hands handling sticks (used for counting/divination) above a roof and a child (子). The image of teaching the young to count or write.'},
    '校': {'origin_type': 'phono_semantic',
           'story': '木 (wood/tree) + 交 (cross/exchange) — phonetic component. Originally "wooden lattice/frame" then specialized to "place of crossed activities / school".'},
    '本': {'origin_type': 'compound_ideograph',
           'story': '木 (tree) with a horizontal stroke at the BASE — pointing to the root / origin of the tree. Hence "origin, source, main thing, book (as a primary source)".'},
    '語': {'origin_type': 'compound_ideograph',
           'story': '言 (word/speech) + 吾 (I/me) — what I say. The 言 radical anchors it as a speech-related kanji.'},
    '国': {'origin_type': 'compound_ideograph',
           'story': 'Simplified from 國 — 囗 (enclosure / borders) containing 玉 (jade / king\'s treasure). A bordered land with a treasure inside = a country.'},
    '会': {'origin_type': 'pictograph',
           'story': 'Simplified from 會 — pictograph of a steamer with layers + a lid coming together. Hence "to come together / meeting".'},
    '社': {'origin_type': 'compound_ideograph',
           'story': '示 (altar / divine) + 土 (earth) — an earthen altar where the community gathered. Originally "village shrine"; came to mean "society / association / company".'},
    '員': {'origin_type': 'compound_ideograph',
           'story': '口 (mouth) above 貝 (shell / money) — a counted member with status. Originally "round number / count"; came to mean "member, staff (a counted person)".'},
    '大': {'origin_type': 'pictograph',
           'story': 'Pictograph of a person standing with arms outstretched wide — the BIG gesture. Captures "large" through the human reference frame.'},
    '中': {'origin_type': 'pictograph',
           'story': 'Pictograph of a flag/pole stuck through the middle of a square — marking the CENTER of a place. Hence "middle / inside / center".'},
    '小': {'origin_type': 'pictograph',
           'story': 'Three small dots / strokes representing small grains or particles. Captures "small" through the visual minimalism.'},
    '上': {'origin_type': 'ideograph',
           'story': 'A short horizontal stroke ABOVE a long base line — representing "what is on top". One of the earliest abstract positional ideographs.'},
    '下': {'origin_type': 'ideograph',
           'story': 'A short horizontal stroke BELOW a long top line — the mirror of 上. Represents "what is underneath" — positional ideograph.'},
    '左': {'origin_type': 'compound_ideograph',
           'story': '又 (hand) + 工 (work/tool) — the LEFT hand traditionally held the tools while the right hand worked them. The 工 element pins down "left".'},
    '右': {'origin_type': 'compound_ideograph',
           'story': '又 (hand) + 口 (mouth) — the RIGHT hand was used to eat (bring food to the mouth). The 口 element pins down "right".'},
}


def main() -> int:
    fp = ROOT / 'data' / 'kanji.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_etymology_wave2')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')
    data = json.loads(fp.read_text(encoding='utf-8'))
    entries = data.get('entries', data) if isinstance(data, dict) else data
    entries_iter = entries.values() if isinstance(entries, dict) else entries
    by_glyph = {e.get('glyph'): e for e in entries_iter}
    n = 0
    for glyph, etym in ETYMOLOGIES.items():
        if glyph not in by_glyph:
            print(f'  ! missing: {glyph}'); continue
        e = by_glyph[glyph]
        if e.get('etymology'):
            print(f'  - skip (already filled): {glyph}'); continue
        e['etymology'] = etym
        e['etymology_provenance'] = 'llm_curated'
        n += 1
    print(f'\nWave 2 added etymology on {n} more kanji.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
