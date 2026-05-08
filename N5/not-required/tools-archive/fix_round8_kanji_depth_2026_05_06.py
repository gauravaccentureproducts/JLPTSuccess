"""ISSUE-082 + IMP-104 + IMP-108 + IMP-109 (round-8 audit, 2026-05-06):
kanji depth — extend examples to ≥5 compounds via vocab cross-reference,
add 10 more confusable_with clusters, add recognition_priority based on
lesson_order, add stroke_order_mistakes for ~20 traps.

ISSUE-082: every kanji had only 2 compounds; floor is ≥5. Auto-derive
from data/vocab.json reverse-mapping (every vocab entry containing the
kanji glyph).

IMP-104: 10 additional confusable_with clusters beyond round-7's 8.

IMP-108: recognition_priority 1|2|3 derived from lesson_order:
  1 = lesson 1-30 (highest priority — Genki lessons 1-3 / Minna ch 1-5)
  2 = lesson 31-70 (mid priority)
  3 = lesson 71+ (final tier)

IMP-109: stroke_order_mistakes notes for kanji with known textbook traps.

Idempotent.
"""
from __future__ import annotations
import io, json, sys
from collections import defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
KF = ROOT / 'data' / 'kanji.json'
VF = ROOT / 'data' / 'vocab.json'

# IMP-104: additional confusable clusters beyond the 8 from round-7.
ADDITIONAL_CLUSTERS = [
    ['言', '話', '語'],          # all have 言 component
    ['学', '字', '子'],          # 子 component nesting
    ['来', '米'],                # similar core
    ['会', '今'],                # 人 + horizontal lines
    ['東', '車', '束'],          # vertical-line dominant
    ['見', '貝', '具'],          # bottom feet 儿
    ['友', '反'],                # similar diagonal frame
    ['口', '日', '目'],          # rectangle nesting
    ['火', '水'],                # element pair
    ['母', '毋'],                # mother / not (radical)
]

# IMP-109: known stroke-order traps. Glyph -> brief warning.
STROKE_TRAPS = {
    '田': '横→縦の順。外枠は最後ではなく1画目（縦）→2画目（横）→中の十字→最後に下の横線で閉じる。',
    '力': '左から右へ斜めに払い、その後下に折れる一筆。逆向きにすると違う字になる。',
    '必': '点→左払い→中央の縦→右払い→点の順（5画）。多くの初心者が中央の縦を最後に書く誤り。',
    '右': '左払い（ノ）→横→口の順。「左」と書き順が異なる（左は横→ノ→工）。',
    '左': '横→左払い（ノ）→工の順。「右」と書き順が異なる。',
    '九': '左払い→曲線で下まで一筆。2画ではなく1画＋1画。',
    '世': '横→縦縦縦→最後に下の横（5画）。',
    '出': '中央の縦→左の山→右の山。重ねた山ではなく一気に。',
    '何': '人偏→可（口の上に丁）。可の中の口は最後でなく真ん中。',
    '飲': '食偏（9画、複雑）→欠（4画）。食偏の最後は払い。',
    '時': '日偏→寺（3画＋3画）。寺の最初は土ではなく上に１画。',
    '間': '門（外枠）→日（中）。門は左の縦→上の横→右の縦の順。',
    '長': '上3本の横→真ん中の縦→残り。8画で覚える。',
    '高': '亠→口→冂→口（4部分）。上から下へ。',
    '新': '立→木→斤の順。斤は最後。',
    '電': '雨（外）→田（中）の順。田の中の横は最後。',
    '読': '言偏→売の順。売は士＋冖＋儿。',
    '書': '聿（上半）→曰（下半）。横画の本数に注意。',
}


def main() -> int:
    kdata = json.loads(KF.read_text(encoding='utf-8'))
    vdata = json.loads(VF.read_text(encoding='utf-8'))

    # === ISSUE-082: extend examples to ≥5 via vocab reverse-map ===
    # Build map: kanji glyph -> list of vocab entries containing it
    by_kanji = defaultdict(list)
    for e in vdata.get('entries', []):
        form = e.get('form') or ''
        for ch in form:
            if '一' <= ch <= '鿿':  # CJK kanji range
                by_kanji[ch].append({
                    'form': form,
                    'reading': e.get('reading', ''),
                    'gloss': e.get('gloss', ''),
                })

    n_examples_extended = 0
    for ke in kdata.get('entries', []):
        glyph = ke.get('glyph')
        existing = ke.get('examples') or []
        if len(existing) >= 5:
            continue
        existing_forms = {ex.get('form') for ex in existing if isinstance(ex, dict)}
        candidates = by_kanji.get(glyph, [])
        for cand in candidates:
            if len(existing) >= 5:
                break
            if cand['form'] in existing_forms:
                continue
            existing.append({
                'form': cand['form'],
                'reading': cand['reading'],
                'gloss': cand['gloss'],
            })
            existing_forms.add(cand['form'])
        if existing != ke.get('examples'):
            ke['examples'] = existing
            n_examples_extended += 1

    # === IMP-104: extend confusable_with ===
    additional_lookup = defaultdict(set)
    for cluster in ADDITIONAL_CLUSTERS:
        for glyph in cluster:
            for other in cluster:
                if other != glyph:
                    additional_lookup[glyph].add(other)

    n_confusable_extended = 0
    for ke in kdata.get('entries', []):
        glyph = ke.get('glyph')
        if glyph in additional_lookup:
            current = ke.get('confusable_with') or []
            new_set = list(current)
            for other in additional_lookup[glyph]:
                if other not in new_set:
                    new_set.append(other)
            if new_set != current:
                ke['confusable_with'] = new_set
                n_confusable_extended += 1

    # === IMP-108: recognition_priority from lesson_order ===
    n_priority = 0
    for ke in kdata.get('entries', []):
        if ke.get('recognition_priority'):
            continue
        lo = ke.get('lesson_order')
        if not isinstance(lo, int):
            continue
        if lo <= 30:
            prio = 1
        elif lo <= 70:
            prio = 2
        else:
            prio = 3
        ke['recognition_priority'] = prio
        n_priority += 1

    # === IMP-109: stroke_order_mistakes ===
    n_traps = 0
    for ke in kdata.get('entries', []):
        glyph = ke.get('glyph')
        if glyph in STROKE_TRAPS:
            note = STROKE_TRAPS[glyph]
            if ke.get('stroke_order_mistakes') != note:
                ke['stroke_order_mistakes'] = note
                n_traps += 1

    KF.write_text(json.dumps(kdata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    total = len(kdata.get('entries', []))
    nE5 = sum(1 for e in kdata['entries'] if len(e.get('examples', [])) >= 5)
    nC = sum(1 for e in kdata['entries'] if e.get('confusable_with'))
    nP = sum(1 for e in kdata['entries'] if e.get('recognition_priority'))
    nS = sum(1 for e in kdata['entries'] if e.get('stroke_order_mistakes'))
    print(f'[ISSUE-082+IMP-104+IMP-108+IMP-109] Kanji depth')
    print(f'  examples extended:          {n_examples_extended} (now {nE5}/{total} have >=5)')
    print(f'  confusable_with extended:   {n_confusable_extended} (now {nC}/{total})')
    print(f'  recognition_priority added: {n_priority} (now {nP}/{total})')
    print(f'  stroke_order_mistakes added:{n_traps} (now {nS}/{total})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
