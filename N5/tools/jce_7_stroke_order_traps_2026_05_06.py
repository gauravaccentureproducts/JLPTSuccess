"""JCE-7: Author `stroke_order_mistakes` field on kanji entries with
known textbook stroke-order traps.

Schema: stroke_order_mistakes is a string describing the trap and the
correct order. Renderer expected to surface as a yellow-warning
callout on the kanji detail page.

Reference: standard Japanese kanji-stroke-order textbooks, KanjiVG
documentation, and Wenlin/Genki appendix tables. Traps documented
here are the small set where Western beginners commonly write the
strokes in the wrong sequence.

Idempotent: skips kanji that already have a populated value.
Marks `stroke_order_mistakes_provenance: llm_curated`.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KANJI = ROOT / 'data' / 'kanji.json'

TRAPS: dict[str, str] = {
    '田': (
        'Common mistake: writing the inside-cross BEFORE closing the box. Correct order: '
        '(1) left vertical | (2) top horizontal + right vertical written as ONE stroke '
        '"hook" stroke | (3) middle horizontal | (4) middle vertical | (5) bottom horizontal '
        'closing the box. The cross inside is written AFTER the box outline is mostly drawn.'
    ),
    '力': (
        'Common mistake: writing the bottom-curve as a separate stroke. Correct order: '
        'just 2 strokes — (1) the angled top stroke going down-right then sharply down-left '
        '(one continuous stroke with a bend), (2) the long slash from top-right going '
        'down-left. The hook at bottom-left of stroke 1 is part of stroke 1, not separate.'
    ),
    '必': (
        'Common mistake: writing strokes in the order suggested by 心 (heart) embedded inside. '
        'Correct order: (1) middle slash going down-left, (2) top-left dot, (3) curve going '
        'right-down-and-around (the 心 left side), (4) middle dot, (5) right dot. Note that '
        'this is NOT 心 with a slash through it; the slash comes FIRST, not last.'
    ),
    '右': (
        'Common mistake: writing the top-left horizontal stroke FIRST (as in 左). Correct '
        'for 右: (1) short slash going down-left, (2) horizontal stroke. For 左: (1) horizontal '
        'stroke, (2) short slash going down-left. The order DIFFERS between 右 and 左 — this '
        'is one of the most-asked stroke-order questions among beginners.'
    ),
    '左': (
        'Common mistake: applying the 右-order to 左 (or vice versa). Correct for 左: '
        '(1) horizontal stroke FIRST (going left-to-right), (2) short slash going down-left. '
        'Compare with 右 where the slash comes FIRST. The order tells you whether the '
        'horizontal "covers" the slash or vice versa.'
    ),
    '九': (
        'Common mistake: drawing the J-hook as two separate strokes. Correct: '
        '(1) short slash going down-left from upper area, (2) one continuous stroke '
        'starting from top-right, going down, curving sharply leftward, ending in a hook. '
        'The full curve + hook is ONE stroke, not two.'
    ),
    '生': (
        'Common mistake: writing the bottom-horizontal before the middle-horizontals. '
        'Correct: top to bottom, building the kanji like a stack — (1) upper short slash, '
        '(2) top horizontal, (3) middle slash going down, (4) middle horizontal, (5) bottom '
        'horizontal LAST. The bottom is written last.'
    ),
    '出': (
        'Common mistake: writing the middle vertical first, or treating the kanji as two '
        'stacked 山. Correct: (1) middle vertical going DOWN, (2) bottom-left short '
        'horizontal, (3) bottom-right short horizontal closing the lower-left loop, '
        '(4) outer-right vertical with hook closing the upper area, (5) top-left horizontal '
        'closing the top opening. NOT two 山 stacked.'
    ),
    '飛': (
        'Common mistake: writing this complex 9-stroke kanji left-to-right naively. '
        'Correct: build from the top-down structure — (1-3) the 升 element on the left, '
        '(4-5) the central diagonal element, (6-9) the right-side wing elements. The '
        'two "wing" strokes on the right are written LAST. (Note: 飛 is borderline N5; '
        'verify whether it appears in the corpus before relying on this.)'
    ),
    '何': (
        'Common mistake: writing the 可 part before the イ (person) radical. Correct: '
        '(1-2) the イ radical on the LEFT first — top short slash, then long vertical going '
        'down. (3-7) THEN the 可 on the right. Radicals on the left are always written '
        'before the rest in left-right composite kanji.'
    ),
    '時': (
        'Common mistake: writing 寺 (right side) before 日 (left side). Correct: '
        '(1-4) the 日 radical on the LEFT first, (5-10) THEN the 寺 component on the right. '
        'This is the standard left-right composite rule: write LEFT before RIGHT.'
    ),
    '間': (
        'Common mistake: writing the inside 日 before the outer 門 (gate). Correct: '
        '(1-8) the 門 (gate) outline FIRST, building from top-left going around, '
        '(9-12) THEN the 日 inside. The "container" is always written before the "contents". '
        'Same rule applies to 国, 回, 図, 困 — outer frame first.'
    ),
}


def main():
    with KANJI.open('r', encoding='utf-8') as f:
        data = json.load(f)

    entries = data['entries']
    by_glyph = {e.get('glyph'): e for e in entries if e.get('glyph')}

    matched = 0
    skipped = 0
    not_in_corpus = []
    for glyph, note in TRAPS.items():
        e = by_glyph.get(glyph)
        if e is None:
            not_in_corpus.append(glyph)
            continue
        if e.get('stroke_order_mistakes'):
            skipped += 1
            continue
        e['stroke_order_mistakes'] = note
        e['stroke_order_mistakes_provenance'] = 'llm_curated'
        matched += 1

    print(f'Authored stroke_order_mistakes on {matched} kanji.')
    print(f'Skipped (already had value): {skipped}')
    if not_in_corpus:
        print(f'Glyphs not in N5 corpus (skipped): {not_in_corpus}')

    with KANJI.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Wrote: {KANJI}')


if __name__ == '__main__':
    main()
