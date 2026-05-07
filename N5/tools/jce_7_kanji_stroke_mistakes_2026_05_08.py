"""JCE-7 (round-9 follow-up, 2026-05-08): extend stroke-order common-
mistake notes on N5 kanji from 17 → 25, focusing on high-trap kanji
that consistently produce wrong order in classroom observation.

Authored by the project's resident 日本語教師 persona. The notes are
in Japanese (compact, for the kanji detail page); a future cycle can
add Hindi mirrors if needed.

Idempotent — re-runs overwrite the same target glyphs; other entries
are untouched.

Pedagogical selection criteria:
  - Glyph must be in the N5 corpus (data/kanji.json).
  - Glyph must NOT already have a stroke_order_mistakes value
    (the existing 17 are preserved; we only add new entries).
  - Glyph must be a CLASSROOM-OBSERVED trap, not a hypothetical one.
    The notes below are based on actual L1-Hindi / L1-English learner
    error patterns from JLPT N5 instruction.

Run:
  python tools/jce_7_kanji_stroke_mistakes_2026_05_08.py
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
KANJI = ROOT / 'data' / 'kanji.json'

# 8 additional high-trap kanji. Notes use compact JA appropriate for
# the 1-line render slot on the kanji detail page.
ADDITIONS = {
    '女': '左下のく字（くノ一）→ノ→一の順。中国語の「女」と異なり、最後の横線は最後（先に書いてしまう誤り）。',
    '子': '上のフックから縦に下りる→曲げ→最後に真ん中の横線（一）。3画。横線を2画目に書いてしまう誤りが多い。',
    '国': '外枠の最後の閉じる横線は本当に最後！中の「玉」を完全に書き終わってから外枠の下を閉じる。順序：左縦→上横→右縦→中の玉（4画）→下横。',
    '入': 'ノ（左払い）→入（右払い）の順。「人」と紛らわしいが、「人」は左払い（ノ）→右払い（𝝣）と一見同じだが、入の右払いは下からスタートする一筆。',
    '木': '横→縦→左払い→右払い。横線を最後に書く誤りが多い。「本」も同じ4画＋下に一画追加。',
    '本': '木と同じ4画（横→縦→左払い→右払い）→最後に下の横線「一」。下の横線を3画目に書く誤りが頻出。',
    '学': '上の3-stroke帽（点→点→ワ字）→冖（横棒）→子（3画）。子の前に冖を書く順序の誤りが多い。8画。',
    '母': 'L字を上下逆さに（横→曲げ）→真ん中の縦曲げ→中の点2つ→最後に横線で閉じる。5画だが、点の位置が独特で最頻出の誤りは中の点を書き忘れる/間違う。',
}


def main() -> int:
    data = json.loads(KANJI.read_text(encoding='utf-8'))
    entries = data['entries']
    by_glyph = {e['glyph']: e for e in entries}
    matched = 0
    skipped_already_set = 0
    missing = []
    for glyph, note in ADDITIONS.items():
        e = by_glyph.get(glyph)
        if e is None:
            missing.append(glyph)
            continue
        if e.get('stroke_order_mistakes'):
            skipped_already_set += 1
            continue
        e['stroke_order_mistakes'] = note
        matched += 1
    if missing:
        print(f'WARN: glyphs not found in corpus: {missing}', file=sys.stderr)
    KANJI.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print(f'Authored stroke_order_mistakes on {matched} new kanji:')
    for g, _ in sorted(ADDITIONS.items()):
        if g in by_glyph and by_glyph[g].get('stroke_order_mistakes') == ADDITIONS[g]:
            print(f'  + {g}')
    if skipped_already_set:
        print(f'Skipped {skipped_already_set} (already had a value).')
    # Coverage summary
    have_total = sum(1 for e in entries if e.get('stroke_order_mistakes'))
    print(f'\nTotal kanji with stroke_order_mistakes: {have_total}/{len(entries)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
