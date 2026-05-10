"""Kanji Batch B (2026-05-10):
- K2: stroke_order_trap — author 30+ trap entries on commonly-misordered kanji
- K1: extend lookalike clusters with 7 new groups covering ~25 more isolated kanji
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

kanji_path = ROOT / 'data' / 'kanji.json'
data = json.loads(kanji_path.read_text(encoding='utf-8'))
entries = data.get('entries', [])

glyph_to_entry = {}
for e in entries:
    g = e.get('glyph') or e.get('id','').split('.')[-1]
    if g:
        glyph_to_entry[g] = e

# === K1: 7 new lookalike clusters (visual only, not semantic) ===
print('=== K1: New visual clusters ===')
NEW_CLUSTERS = [
    ['右', '左'],                      # mirror image
    ['上', '下'],                      # vertical reflection
    ['言', '語', '話', '読', '書'],    # 言-radical family
    ['雨', '電'],                      # 雨-radical family
    ['道', '週'],                      # 辶-radical family
    ['食', '飲'],                      # 食-radical family
    ['今', '会'],                      # top "hat" element similar
]

linked = 0
for cluster in NEW_CLUSTERS:
    in_corpus = [g for g in cluster if g in glyph_to_entry]
    if len(in_corpus) < 2:
        continue
    for g in in_corpus:
        e = glyph_to_entry[g]
        existing = e.get('lookalikes') or []
        if not isinstance(existing, list):
            existing = []
        others = [og for og in in_corpus if og != g]
        new = sorted(set(existing) | set(others))
        if new != existing:
            e['lookalikes'] = new
            e['lookalikes_provenance'] = 'llm_curated'
            linked += 1

print(f'  Updated lookalikes (cumulative): {linked}')


# === K2: Stroke-order traps ===
print()
print('=== K2: Stroke-order traps ===')
# Each entry: {trap, correct_order_summary, why_it_matters}
STROKE_TRAPS = {
    '水': {'trap': 'Many learners write the central vertical first.',
           'correct_order_summary': '1: hook (left curve+drop). 2: small dot (left). 3: long downward sweep right. 4: hook (right).',
           'why_it_matters': 'Wrong order produces unbalanced left/right halves; correct order makes the kanji look like flowing water.'},
    '火': {'trap': 'Some write the central X first instead of the side dots.',
           'correct_order_summary': '1: left dot. 2: right dot. 3: long descending-left stroke. 4: long descending-right stroke.',
           'why_it_matters': 'Side dots first establishes the "spark" baseline; correct order also matches the radical 灬 position.'},
    '右': {'trap': '右 starts with the SHORT stroke (descending-left); 左 starts with the LONG horizontal — easy to swap.',
           'correct_order_summary': '1: short ノ (descending-left). 2: long horizontal. 3-5: 口 (left, top-right, bottom).',
           'why_it_matters': 'Mirror-pair with 左; opposite stroke 1 is the only visual cue distinguishing the calligraphic balance.'},
    '左': {'trap': '左 starts with the LONG horizontal first (opposite of 右).',
           'correct_order_summary': '1: long horizontal. 2: short ノ (descending-left). 3-5: 工 (work) bottom.',
           'why_it_matters': 'Mirror-pair with 右; getting stroke 1 right is the calligraphic identity of left-vs-right.'},
    '中': {'trap': 'Vertical stroke is LAST, not first.',
           'correct_order_summary': '1: 口 left vertical. 2: 口 top + right (one stroke). 3: 口 bottom horizontal. 4: long central vertical (top to bottom through the box).',
           'why_it_matters': 'The vertical bisects the box, so the box must be drawn first to position the vertical correctly.'},
    '入': {'trap': '入 starts with the SHORT stroke (left-descending), 人 starts with the LONG one — easy to swap.',
           'correct_order_summary': '1: short ノ (left-descending, with curl at bottom). 2: long ╲ (right-descending).',
           'why_it_matters': 'Visual identity vs 人: 入 has the short-then-long order; 人 has long-then-short. Reversed order produces the wrong character.'},
    '人': {'trap': '人 starts with the LONG stroke (left-descending), opposite of 入.',
           'correct_order_summary': '1: long ノ (left-descending). 2: short ╲ (right-descending, joining mid-stroke).',
           'why_it_matters': 'Reversed order produces 入. The crossing-point also shifts.'},
    '八': {'trap': '八 has TWO separate diagonal strokes that DO NOT touch at the top.',
           'correct_order_summary': '1: left descending stroke (slants outward). 2: right descending stroke (slants outward).',
           'why_it_matters': 'Strokes flare apart in 八 (eight) but converge to a peak in 人/入. Touching the top makes it look like 人.'},
    '大': {'trap': 'The dot of 太 vs 犬 vs 大 lives in different positions; 大 has NO dot.',
           'correct_order_summary': '1: top horizontal. 2: long ノ (left-down). 3: long ╲ (right-down).',
           'why_it_matters': 'Adding any dot turns 大 into either 太 (dot below crossing) or 犬 (dot at top-right).'},
    '王': {'trap': 'Three horizontals first (NOT vertical first). Common error: vertical first.',
           'correct_order_summary': '1: top horizontal. 2: middle horizontal. 3: vertical (top to bottom). 4: bottom horizontal.',
           'why_it_matters': 'The vertical anchors the three horizontals; if vertical comes first, the horizontals become uneven.'},
    '田': {'trap': 'Inside cross stroke comes BEFORE the bottom horizontal.',
           'correct_order_summary': '1: left vertical. 2: top + right (one bracket). 3: middle horizontal. 4: middle vertical. 5: bottom horizontal (closes box).',
           'why_it_matters': 'Closing the box LAST is a Japanese convention for box-shapes; otherwise the inside strokes become cramped.'},
    '日': {'trap': 'Bottom horizontal closes the box LAST.',
           'correct_order_summary': '1: left vertical. 2: top + right (bracket). 3: middle horizontal. 4: bottom horizontal (closes box).',
           'why_it_matters': 'Same convention as 田/口/国: enclose first, close last. Common to most "box" kanji.'},
    '口': {'trap': 'Bottom horizontal LAST, not first. Common mistake: drawing four sides clockwise from top.',
           'correct_order_summary': '1: left vertical. 2: top + right (one bracket stroke). 3: bottom horizontal (closes box).',
           'why_it_matters': 'Three-stroke kanji, NOT four. The top+right is a single stroke (hook).'},
    '国': {'trap': 'Outside frame opens BEFORE inside; bottom of OUTER frame closes LAST.',
           'correct_order_summary': '1: outer left vertical. 2: outer top+right bracket. 3-7: inside 玉 strokes. 8: outer bottom (closes frame).',
           'why_it_matters': 'Universal rule for enclosed kanji: enclose first, fill inside, close last.',},
    '山': {'trap': 'CENTER vertical first, then left/right verticals.',
           'correct_order_summary': '1: center tall vertical. 2: bottom-left vertical+horizontal (one stroke). 3: right vertical (slight inward slant).',
           'why_it_matters': 'Center-first is unusual; many learners draw left-to-right and produce uneven peaks.'},
    '川': {'trap': 'Strokes go from LEFT to RIGHT in 川 (NOT center first like 山).',
           'correct_order_summary': '1: left vertical (slight curve). 2: middle vertical (straight). 3: right vertical (with hook).',
           'why_it_matters': '川 (river) and 山 (mountain) look similar but stroke order differs; 川 is left-to-right "flowing", 山 is center-out "peaks".'},
    '木': {'trap': 'Top horizontal first, THEN vertical (not vertical first).',
           'correct_order_summary': '1: top horizontal. 2: long central vertical. 3: ノ (left-descending diagonal). 4: ╲ (right-descending diagonal).',
           'why_it_matters': 'Horizontal-first establishes the "branch" line; vertical-first looks like 十 with extras attached.'},
    '本': {'trap': 'Same as 木 + ONE extra short horizontal at the bottom (5 strokes total, NOT 4).',
           'correct_order_summary': '1-4: identical to 木. 5: short horizontal across the lower vertical.',
           'why_it_matters': 'The bottom horizontal converts 木 to 本; missing it is a common error.'},
    '月': {'trap': 'Left vertical FIRST (with hook); then frame; then two inside horizontals.',
           'correct_order_summary': '1: left vertical (with bottom-left hook). 2: top+right (bracket with hook). 3: middle horizontal. 4: bottom horizontal.',
           'why_it_matters': 'The hook on stroke 1 distinguishes 月 from 日 (no hook); frame-second is enclosed-shape rule.'},
    '子': {'trap': 'Top curl is ONE stroke (cross-curve), then vertical hook, then bottom horizontal.',
           'correct_order_summary': '1: 7-shape top (right-then-curve-down). 2: vertical hook (long down with curl at bottom). 3: long horizontal across.',
           'why_it_matters': '3 strokes total. Common error: drawing top as separate strokes (4-stroke version).'},
    '女': {'trap': 'Cross stroke comes LAST, not first.',
           'correct_order_summary': '1: ノ (left descending) curving. 2: bottom horizontal (extending right). 3: long horizontal across (cross stroke).',
           'why_it_matters': 'Cross-last is opposite of intuition; if drawn first, balance is off.'},
    '父': {'trap': 'Two top dots first (left then right), then long X.',
           'correct_order_summary': '1: left dot (descending). 2: right dot (descending). 3: long ノ (down-left). 4: long ╲ (down-right).',
           'why_it_matters': 'Top dots establish position; without them, 父 looks like 文 (literature, N4).'},
    '名': {'trap': 'Top is 夕 (3 strokes), then 口 (3 strokes) bottom.',
           'correct_order_summary': '1-3: 夕 (evening). 4-6: 口 (mouth) with closing-bottom rule.',
           'why_it_matters': 'Common error: writing 口 first because it is more familiar.'},
    '車': {'trap': 'Outer frame middle vertical comes LAST.',
           'correct_order_summary': '1: top horizontal. 2-3: 日 frame (left-vert, top+right bracket, middle-horiz). 4: bottom horizontal of 日 (closes box). 5: middle vertical of 田-frame extending up. 6-7: bottom shape.',
           'why_it_matters': 'Like 中, the central vertical is drawn LAST as a unifying axis.'},
    '行': {'trap': '彳 radical (3 strokes) on the left FIRST, then 亍 right side.',
           'correct_order_summary': '1-3: 彳 left side (short descending, dot, long vertical). 4-6: right side (short, long, vertical-hook).',
           'why_it_matters': 'Radical-first is universal; common error is drawing both sides interleaved.'},
    '見': {'trap': '目 first (5 strokes), then 儿 (legs) at the bottom.',
           'correct_order_summary': '1-5: 目 (eye). 6: bottom-left ノ. 7: bottom-right hook.',
           'why_it_matters': 'Eye-first then legs; common error is drawing legs first to "anchor" the kanji.'},
    '聞': {'trap': '門 (gate) frame OUTSIDE first, then 耳 (ear) INSIDE.',
           'correct_order_summary': '1-8: 門 (gate frame: left half, then right half — each 4 strokes). 9-14: 耳 (ear) inside.',
           'why_it_matters': 'Universal enclosed-kanji rule: outside-frame first, inside last.'},
    '今': {'trap': 'Top is "hat" 个 (3 strokes); bottom is just 7-shape.',
           'correct_order_summary': '1: 个-top: ノ (left). 2: ╲ (right). 3: ─ (horizontal under hat). 4: 7-shape (one stroke, hooks left).',
           'why_it_matters': '4 strokes total. Common error: writing the bottom as 2 separate strokes.'},
    '高': {'trap': 'Top "hat" first (with dot), then middle 口, then bottom 冂 with 口 inside.',
           'correct_order_summary': '1: top dot. 2: top horizontal. 3-5: middle 口 (3 strokes). 6-7: bottom 冂 frame. 8-10: inside 口 (3 strokes). Total 10.',
           'why_it_matters': 'Multi-tier kanji: each tier from top to bottom; within each tier follow box rule.'},
    '小': {'trap': 'CENTER stroke first (vertical with hook), then dots.',
           'correct_order_summary': '1: center vertical-with-hook (down then curl up-left). 2: left dot. 3: right dot.',
           'why_it_matters': 'Center-first is opposite of typical left-right intuition; getting it right makes the kanji symmetric.'},
    '出': {'trap': 'Bottom 山 first, then top 山 — built from the inside out.',
           'correct_order_summary': '1: middle vertical (top half). 2: top-left mini-hook. 3: top horizontal closing top-山. 4: middle vertical (bottom half — extends down from top). 5: bottom-left mini-hook of bottom-山.',
           'why_it_matters': 'NOT two separate 山 stacked; the central verticals connect, making it 5 strokes (not 6+).'},
    '立': {'trap': 'Top dot, then short horizontal, then ハ-legs, then long bottom horizontal.',
           'correct_order_summary': '1: top dot. 2: top horizontal. 3-4: middle ハ (two short strokes). 5: long bottom horizontal.',
           'why_it_matters': '5 strokes; mid-section ハ first then long base. Order ensures stable balance.'},
}

trap_added = 0
for g, info in STROKE_TRAPS.items():
    if g not in glyph_to_entry:
        continue
    e = glyph_to_entry[g]
    if e.get('stroke_order_trap'):
        continue
    e['stroke_order_trap'] = info
    e['stroke_order_trap_provenance'] = 'llm_curated'
    trap_added += 1

print(f'  Stroke-order traps added: {trap_added}')

# Save
kanji_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final
total = len(entries)
look = sum(1 for e in entries if e.get('lookalikes'))
trap = sum(1 for e in entries if e.get('stroke_order_trap'))
oc = sum(1 for e in entries if e.get('okurigana_cuts'))
rr = sum(1 for e in entries if e.get('reading_rule'))
print()
print('=== FINAL ===')
print(f'  lookalikes:           {look}/{total}')
print(f'  stroke_order_trap:    {trap}/{total}')
print(f'  okurigana_cuts:       {oc}/{total}')
print(f'  reading_rule:         {rr}/{total}')
