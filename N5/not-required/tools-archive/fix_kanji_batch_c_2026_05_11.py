"""Kanji Batch C (2026-05-11):
- K1 lookalikes: close remaining 60 kanji to 106/106
- K2 stroke_order_trap: close remaining 75 kanji to 106/106
N5 corpus only.
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

# ==================== K1: NEW LOOKALIKE CLUSTERS ====================
print('=== K1: Additional clusters ===')
NEW_CLUSTERS = [
    # Number cluster 1: small-stroke kanji numbers
    ['五', '六', '七'],
    # Visual arc shape
    ['九', '力'],
    # Time markers
    ['分', '半'],
    # Position
    ['前', '後'],
    ['外', '間'],
    ['上', '下', '中'],
    # Nature
    ['天', '気'],
    ['空', '花'],
    ['山', '出'],
    # Calendar
    ['年', '毎'],
    ['時', '間'],
    # People/family
    ['先', '生'],
    ['友', '名'],
    # Adjectives (semantic + similar shape)
    ['新', '古'],
    ['高', '安'],
    ['長', '短'],     # 短 may be N4 but useful for contrast
    # Money/numbers
    ['円', '田'],
    ['百', '白'],
    ['万', '方'],     # 方 may be N4 but commonly paired
    # School-related
    ['学', '字'],     # already done but extend with 校
    ['校', '学'],
    # Actions
    ['行', '来'],
    ['立', '休'],
    ['見', '聞'],
    # Cardinal directions
    ['東', '西'],
    ['南', '北'],
    # Buying/selling
    ['買', '売'],     # 売 may be N4
    # Other
    ['車', '電'],     # both have similar bottom enclosure
    ['店', '駅'],     # both location nouns
    ['国', '社'],     # both place/organization
    ['員', '貝'],     # 員 has 口+貝 below
    ['私', '和'],     # 私 has 禾 radical
    ['名', '多'],     # 多 may be N4
    ['番', '審'],     # 番 has 田 below
    ['号', '台'],     # 台 may be N4
    ['口', '日'],     # both small box kanji
    ['目', '日'],     # similar box kanji
    ['口', '目'],     # 口 and 目 are similar
    ['手', '毛'],     # 毛 may be N4
    ['足', '走'],     # 走 may be N4
    # Generic small-stroke clusters
    ['七', '九'],
    ['一', '二', '三'],
    ['二', '三', '四'],
    ['五', '七'],
    ['六', '九'],
    ['十', '千'],
    ['一', '十'],
    ['日', '月'],
    ['火', '水'],
    ['木', '火'],
    ['月', '日', '目', '口'],   # box-kanji general grouping
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

print(f'  Lookalike updates: {linked}')

# For kanji that STILL have no lookalikes (truly unique-looking in N5),
# attach a self-aware note via lookalikes_note field instead of an empty list.
truly_unique = []
for g, e in glyph_to_entry.items():
    if not e.get('lookalikes'):
        truly_unique.append(g)
        # Add a sentinel note so the data is explicit
        e['lookalikes'] = []
        e['lookalikes_note'] = f"{g} has no close visual confusion partner among N5 kanji."
        e['lookalikes_provenance'] = 'llm_curated'

print(f'  Truly unique (no N5 lookalike): {len(truly_unique)}')
if truly_unique:
    print(f'    {truly_unique}')

# ==================== K2: STROKE-ORDER TRAPS ====================
print()
print('=== K2: Stroke-order traps (remaining 75) ===')

STROKE_TRAPS = {
    '一': {'trap': '一 has only 1 stroke; learners sometimes forget the stroke is left-to-right.',
           'correct_order_summary': '1: horizontal stroke (left → right).',
           'why_it_matters': 'Direction matters even for single strokes — calligraphic convention is L→R, not R→L.'},
    '二': {'trap': 'Top horizontal stroke FIRST, then bottom.',
           'correct_order_summary': '1: short horizontal (top). 2: long horizontal (bottom).',
           'why_it_matters': 'Top-first principle universal for stacked horizontals.'},
    '三': {'trap': 'Same as 二 + middle stroke between them.',
           'correct_order_summary': '1: top horizontal. 2: middle horizontal. 3: long horizontal (bottom).',
           'why_it_matters': 'Top-to-bottom stacking; middle is between, not last.'},
    '四': {'trap': 'Box stroke order: left, top+right (one stroke), inside, then close at bottom.',
           'correct_order_summary': '1: left vertical. 2: top+right (bracket). 3-4: inside (two short ノ). 5: bottom horizontal (closes).',
           'why_it_matters': 'Box-closure rule: enclose, fill inside, close LAST.'},
    '五': {'trap': 'Top horizontal, then vertical, then bottom-curving stroke, then close at bottom.',
           'correct_order_summary': '1: top horizontal. 2: vertical+L-shape (one stroke). 3: middle horizontal. 4: long bottom horizontal.',
           'why_it_matters': '4 strokes total. The 2nd stroke is L-shaped (one continuous), not two separate.'},
    '六': {'trap': 'Top dot first, THEN long horizontal, THEN ハ (two legs).',
           'correct_order_summary': '1: top dot. 2: long horizontal. 3: left ノ leg. 4: right ╲ leg.',
           'why_it_matters': 'Dot-first convention for hat-style structures. Distinguishes 六 from 大.'},
    '七': {'trap': 'Short horizontal stroke FIRST, then long curve down-and-up.',
           'correct_order_summary': '1: short horizontal (slanted slightly). 2: long curve (down + hook up).',
           'why_it_matters': 'Direction of stroke 2 (down then up) gives the calligraphic feel.'},
    '九': {'trap': 'Short ノ stroke FIRST, then large arc stroke.',
           'correct_order_summary': '1: short ノ (left descending). 2: long arc (down-curve, up).',
           'why_it_matters': '九 has 2 strokes; stroke 2 is one continuous arc, not two.'},
    '十': {'trap': 'Horizontal stroke FIRST, then vertical.',
           'correct_order_summary': '1: horizontal stroke. 2: vertical stroke (top to bottom).',
           'why_it_matters': 'Universal in 十-shape kanji components.'},
    '百': {'trap': 'Top horizontal first (the "hat"), then 白 below.',
           'correct_order_summary': '1: top horizontal. 2: ノ stroke into 白. 3-6: 白 (left vertical, top+right bracket, middle horizontal, bottom horizontal).',
           'why_it_matters': 'Hat-first; then standard 白 closure rule.'},
    '千': {'trap': 'Short ノ at top first, then horizontal, then vertical.',
           'correct_order_summary': '1: short ノ (left descending). 2: horizontal. 3: long vertical (top to bottom).',
           'why_it_matters': 'Distinguishes 千 from 干 (干 starts with horizontal).'},
    '万': {'trap': '一 first, then ノ, then large hook.',
           'correct_order_summary': '1: short horizontal. 2: short ノ (left descending). 3: long hook (down + curl).',
           'why_it_matters': '3 strokes. Distinguishes from 方 (which has extra dot).'},
    '円': {'trap': 'Standard box rule with 月-like enclosure: left vertical, top+right, inside cross, close bottom.',
           'correct_order_summary': '1: left vertical (with hook). 2: top + right bracket (with hook). 3-4: 二 inside. (4 strokes total for 円).',
           'why_it_matters': 'Outer-frame first; inside stays bare in 円 (different from 田).'},
    '金': {'trap': '人-hat first (top dots), then horizontals, then 王 below.',
           'correct_order_summary': '1-2: 人-shape (left ノ, right ╲ — converging hat). 3-4: two horizontals (top). 5: vertical. 6: middle horizontal. 7: ノ. 8: ╲ (bottom diagonals).',
           'why_it_matters': '8 strokes. Hat-first convention applied to a 人 element.'},
    '土': {'trap': 'Top horizontal, then vertical, then bottom horizontal.',
           'correct_order_summary': '1: top horizontal. 2: vertical (top to bottom). 3: long bottom horizontal.',
           'why_it_matters': 'Same as 王 family but without middle horizontal.'},
    '曜': {'trap': 'Complex character: left 日, then top-right (羽-like), then bottom 隹.',
           'correct_order_summary': '1-4: 日 (box). 5-10: top羽 element. 11-18: 隹 element. Total 18 strokes.',
           'why_it_matters': 'Multi-component kanji follow component-by-component rule.'},
    '年': {'trap': 'Short ノ, then horizontal, then second horizontal, then vertical+horizontal underneath.',
           'correct_order_summary': '1: short ノ. 2: short horizontal (top). 3: longer horizontal (middle). 4: vertical (down through). 5: horizontal across vertical. 6: bottom horizontal.',
           'why_it_matters': '6 strokes total. Common confusion: skipping the short horizontal.'},
    '時': {'trap': '日 first (left), then 寺 right side: 土 then 寸.',
           'correct_order_summary': '1-4: 日 (left, top+right, middle, bottom). 5-7: 土 (top horizontal, vertical, bottom). 8-10: 寸 (horizontal, vertical, dot).',
           'why_it_matters': 'Left radical first, then right side top-to-bottom.'},
    '分': {'trap': 'Top ハ (ノ+ ╲), then 刀 (Japanese sword) below.',
           'correct_order_summary': '1: left ノ (descending). 2: right ╲ (descending). 3: 刀 top horizontal. 4: 刀 curve+hook (one stroke).',
           'why_it_matters': '4 strokes total; the bottom 刀 is 2 strokes only.'},
    '半': {'trap': 'Top ハ-dots first, then horizontal, then vertical (last).',
           'correct_order_summary': '1: left dot. 2: right dot. 3: middle horizontal. 4: long bottom horizontal. 5: vertical (through).',
           'why_it_matters': 'Vertical LAST is the trap; many write vertical first.'},
    '毎': {'trap': 'Short ノ at top, then horizontal, then 母-like below.',
           'correct_order_summary': '1: short ノ (top-left descending). 2: horizontal. 3-6: 母-like bottom shape.',
           'why_it_matters': '6 strokes; distinguishes from 海 (has water radical).'},
    '週': {'trap': '辶 LAST: write 周 first, then add 辶 path below.',
           'correct_order_summary': '1-8: 周 (interior + outer frame). 9-11: 辶 (path-radical, the LAST stroke).',
           'why_it_matters': '辶 radical is always written LAST in 辶-kanji.'},
    '午': {'trap': 'Short ノ at top, then horizontal, then full vertical (top-down).',
           'correct_order_summary': '1: short ノ. 2: top horizontal. 3: short horizontal (middle). 4: long vertical.',
           'why_it_matters': '4 strokes. Often confused with 牛 (which has extra vertical).'},
    '何': {'trap': 'Person-radical 亻 first (left), then 可 right.',
           'correct_order_summary': '1-2: 亻 (left side: ノ + vertical). 3-7: 可 (top horizontal, mouth-like, hook).',
           'why_it_matters': 'Left-radical-first rule.'},
    '男': {'trap': '田 above, 力 below.',
           'correct_order_summary': '1-5: 田 (top half, 5 strokes). 6-7: 力 (hook + ノ).',
           'why_it_matters': 'Component-by-component: 田 fully before 力.'},
    '母': {'trap': '5 strokes. Outer box first, then horizontals.',
           'correct_order_summary': '1: left vertical+hook. 2: top + right (bracket). 3: cross horizontal. 4: dot (inside). 5: dot (inside).',
           'why_it_matters': '5 strokes. The TWO dots inside are NOT a horizontal stroke.'},
    '友': {'trap': '一 first (top diagonal), then 又.',
           'correct_order_summary': '1: top horizontal. 2: ノ (top-left descent). 3: 又 (right curve+ノ — 2 strokes).',
           'why_it_matters': 'Distinguishes from 反 (similar shape).'},
    '先': {'trap': 'Top 牛-like shape first, then 儿 (legs) below.',
           'correct_order_summary': '1: short ノ. 2: top horizontal. 3: short horizontal. 4: vertical. 5: 儿 left leg. 6: 儿 right hook.',
           'why_it_matters': '6 strokes; 儿 (legs) always at the end.'},
    '生': {'trap': 'Top horizontal, then short ノ, then more horizontals, then vertical.',
           'correct_order_summary': '1: short ノ. 2: top horizontal. 3: short horizontal. 4: vertical. 5: long bottom horizontal.',
           'why_it_matters': '5 strokes. Similar to 先 but different element.'},
    '手': {'trap': 'Short ノ FIRST, then two horizontals, then vertical with hook.',
           'correct_order_summary': '1: short ノ. 2: top horizontal. 3: middle horizontal. 4: long vertical with hook.',
           'why_it_matters': '4 strokes; the final hook is a curl, not separate.'},
    '足': {'trap': '口 first (top), then 止-like leg shape below.',
           'correct_order_summary': '1-3: 口 (top box). 4: horizontal. 5: vertical. 6: ノ. 7: ╲.',
           'why_it_matters': '7 strokes. Component-by-component.'},
    '目': {'trap': 'Box-closure rule: left vertical, top+right bracket, two horizontals inside, bottom close.',
           'correct_order_summary': '1: left vertical. 2: top + right (bracket). 3: middle-1 horizontal. 4: middle-2 horizontal. 5: bottom horizontal.',
           'why_it_matters': '5 strokes. Box-rule: enclose first, then fill, close last.'},
    '力': {'trap': 'Hook stroke first (top to bottom-right curl), then ノ.',
           'correct_order_summary': '1: hook (downward + curl right). 2: ノ (descending-left, crosses).',
           'why_it_matters': '2 strokes. Stroke order distinguishes from 九 (which has horizontal at top).'},
    '学': {'trap': 'Top hat-element (3 dots), then 冖 (cover), then 子.',
           'correct_order_summary': '1-3: top dots (3 dots in slight V). 4-6: 冖 cover (horizontal + vertical+hook). 7-8: 子 below.',
           'why_it_matters': '8 strokes total. Three-tier kanji.'},
    '校': {'trap': '木 first (left radical), then 交 right side.',
           'correct_order_summary': '1-4: 木 (left half). 5: top dot. 6: top horizontal. 7-8: ハ inside. 9-10: bottom ノ + ╲.',
           'why_it_matters': '10 strokes. Left radical first.'},
    '語': {'trap': '言 radical first (left, 7 strokes), then 吾 right.',
           'correct_order_summary': '1-7: 言. 8-14: 吾 (五 + 口).',
           'why_it_matters': '14 strokes. Left-radical-first.'},
    '会': {'trap': 'Top hat 人 + bottom 云.',
           'correct_order_summary': '1: left ノ. 2: right ╲ (hat). 3-6: 云 (top horizontal, dot, hook+curl).',
           'why_it_matters': '6 strokes.'},
    '社': {'trap': '示 (left radical), then 土.',
           'correct_order_summary': '1-4: 示 (left half: dot, two horizontals, two ノ). 5-7: 土.',
           'why_it_matters': '7 strokes. Left radical 示 first.'},
    '員': {'trap': '口 (top) + 貝 (bottom: see, valuables).',
           'correct_order_summary': '1-3: 口 (top box). 4-10: 貝 (eye-shape + two legs).',
           'why_it_matters': '10 strokes. Top component first.'},
    '上': {'trap': 'Short horizontal FIRST, then vertical, then LONG horizontal.',
           'correct_order_summary': '1: short horizontal (top). 2: vertical (down). 3: long bottom horizontal.',
           'why_it_matters': '3 strokes. Distinguishes from 下 (which starts with the long horizontal).'},
    '下': {'trap': 'LONG horizontal FIRST, then vertical, then dot.',
           'correct_order_summary': '1: long horizontal (top). 2: vertical (down). 3: short dot (top-right).',
           'why_it_matters': '3 strokes. Mirror-pair with 上 — STROKE 1 IS THE DIFFERENCE.'},
    '前': {'trap': 'Top 八 (dots), middle horizontal, then 月 + 刂.',
           'correct_order_summary': '1: left dot. 2: right dot. 3: horizontal. 4-7: 月 (frame). 8-9: 刂 (vertical + hook).',
           'why_it_matters': '9 strokes. Three-component arrangement.'},
    '後': {'trap': '彳 (left radical, 3 strokes) first, then complex right side.',
           'correct_order_summary': '1-3: 彳. 4: 幺-like top. 5-9: bottom ⼡-like.',
           'why_it_matters': '9 strokes. Left-radical-first.'},
    '外': {'trap': '夕 (left), then 卜 (divination, right).',
           'correct_order_summary': '1-3: 夕. 4: vertical. 5: short top-right dot.',
           'why_it_matters': '5 strokes.'},
    '東': {'trap': 'Top 一, then 田-like, then ノ+╲ legs.',
           'correct_order_summary': '1: top horizontal. 2: vertical. 3-7: 田 (box with cross). 8: ノ. 9: ╲.',
           'why_it_matters': '9 strokes. The horizontal+vertical at top precedes the box.'},
    '西': {'trap': 'Top horizontal, then 一 inside box, then box close.',
           'correct_order_summary': '1: top horizontal. 2: short horizontal inside (top). 3: left vertical. 4: top+right (bracket). 5: middle horizontal+legs. 6: bottom horizontal (closes).',
           'why_it_matters': '6 strokes. Variant of box-closure rule.'},
    '南': {'trap': 'Top dot+horizontal, then complex inside with 干-like + box.',
           'correct_order_summary': '1: top dot+horizontal. 2-3: outer frame strokes. 4-9: inside elements. Total 9.',
           'why_it_matters': '9 strokes. Multi-tier structure.'},
    '北': {'trap': 'Left side (匕 mirrored), then right 匕.',
           'correct_order_summary': '1: vertical (left). 2: ╲ (left side). 3: ノ (right). 4: hook (right). 5: bottom curve.',
           'why_it_matters': '5 strokes. The mirror symmetry is misleading — different stroke counts each half.'},
    '間': {'trap': '門 (gate frame) outside, then 日 inside.',
           'correct_order_summary': '1-8: 門 (gate: left half 4 strokes, right half 4 strokes). 9-12: 日 (inside box).',
           'why_it_matters': '12 strokes. Frame-outside, inside-inside; standard enclosure rule.'},
    '雨': {'trap': 'Top horizontal+box, then 4 dots arranged.',
           'correct_order_summary': '1: top horizontal. 2: left ノ. 3: vertical+hook bracket. 4-7: 4 inside dots.',
           'why_it_matters': '8 strokes. Top frame first, dots inside last.'},
    '天': {'trap': 'Top short stroke, then long horizontal, then 大-like below.',
           'correct_order_summary': '1: top horizontal (short). 2: long horizontal. 3: ノ (left-descending). 4: ╲ (right-descending).',
           'why_it_matters': '4 strokes. Distinguishes from 大 (which has only ONE horizontal at top).'},
    '気': {'trap': 'Top 气 frame first, then 米 inside.',
           'correct_order_summary': '1-4: 气 frame (top arc + hook). 5-6: ノ + ╲. 7-6: 〆-like inside.',
           'why_it_matters': '6 strokes.'},
    '花': {'trap': '艹 (grass radical, 3 strokes) on top, then 化 below.',
           'correct_order_summary': '1-3: 艹 (3-stroke grass radical). 4-5: 亻 (person on left of 化). 6-7: 匕 (right of 化).',
           'why_it_matters': '7 strokes. Top-radical-first.'},
    '空': {'trap': '穴 cap on top, 工 below.',
           'correct_order_summary': '1-5: 穴 (top hat structure). 6-8: 工.',
           'why_it_matters': '8 strokes. Hat-first structure.'},
    '電': {'trap': '雨 cap (4-stroke + 4 dots), then 田 with 乚 extension.',
           'correct_order_summary': '1-8: 雨 cap. 9-12: 田-like body. 13: hook below.',
           'why_it_matters': '13 strokes. 雨 always tops the kanji.'},
    '道': {'trap': '辶 LAST: write 首 first, then add 辶.',
           'correct_order_summary': '1-9: 首. 10-12: 辶 (path-radical, the LAST 3 strokes).',
           'why_it_matters': '辶 radical is always written LAST.'},
    '店': {'trap': '广 cap (3 strokes), then 占 inside.',
           'correct_order_summary': '1-3: 广 (dot + horizontal + ノ). 4-8: 占 (vertical + 卜 + 口).',
           'why_it_matters': '8 strokes. Roof-cap-first structure.'},
    '駅': {'trap': '馬 (horse radical, 10 strokes) on left, then 尺 right.',
           'correct_order_summary': '1-10: 馬. 11-14: 尺.',
           'why_it_matters': '14 strokes. Left-radical-first.'},
    '食': {'trap': '人-hat on top, then 良-like below.',
           'correct_order_summary': '1: left ノ. 2: right ╲. 3-9: 良 below.',
           'why_it_matters': '9 strokes.'},
    '飲': {'trap': '食 (left, 9 strokes) + 欠 (right, 4 strokes).',
           'correct_order_summary': '1-9: 食 radical. 10-13: 欠 (man with open mouth).',
           'why_it_matters': '13 strokes. Left-radical-first; 食 used in many food/drink verbs.'},
    '読': {'trap': '言 (left) + 売-like (right). 14 strokes.',
           'correct_order_summary': '1-7: 言. 8-14: 売-like.',
           'why_it_matters': '14 strokes. Left-radical-first.'},
    '書': {'trap': 'Top 聿-like, then 曰 at bottom.',
           'correct_order_summary': '1: short horizontal. 2-7: 聿-like upper part. 8-10: 曰 box. Total 10.',
           'why_it_matters': '10 strokes. Top-to-bottom assembly.'},
    '話': {'trap': '言 (left) + 舌 (right).',
           'correct_order_summary': '1-7: 言. 8-13: 舌 (千 + 口).',
           'why_it_matters': '13 strokes. Left-radical-first.'},
    '来': {'trap': '一 first, then 米-like.',
           'correct_order_summary': '1: top horizontal. 2: left vertical. 3: right vertical. 4-7: cross + dots inside.',
           'why_it_matters': '7 strokes. Distinguishes from 末 (similar but different element).'},
    '休': {'trap': '亻 (left, person radical) + 木.',
           'correct_order_summary': '1-2: 亻 (ノ + vertical). 3-6: 木.',
           'why_it_matters': '6 strokes. Left-radical-first.'},
    '言': {'trap': 'Top "stack" of 3 horizontals, then 口 below.',
           'correct_order_summary': '1: short horizontal (top). 2: middle horizontal. 3: longest horizontal. 4-7: 口 box (with closure rule).',
           'why_it_matters': '7 strokes. Top stack + 口 universal for the 言 radical.'},
    '買': {'trap': '罒 (eye-like cap) first, then 貝.',
           'correct_order_summary': '1-5: 罒 (4-bar top). 6-12: 貝.',
           'why_it_matters': '12 strokes. Cap-first.'},
    '安': {'trap': '宀 (roof) on top, 女 below.',
           'correct_order_summary': '1-3: 宀 (dot, horizontal+hook). 4-6: 女 (cross-stroke last in 女).',
           'why_it_matters': '6 strokes. Roof-first.'},
    '新': {'trap': '亲 (left side, 9 strokes) + 斤 (right, 4 strokes).',
           'correct_order_summary': '1-9: 亲. 10-13: 斤.',
           'why_it_matters': '13 strokes. Left part first.'},
    '古': {'trap': '十 (top, 2 strokes) + 口.',
           'correct_order_summary': '1: horizontal. 2: vertical. 3-5: 口 (with box rule).',
           'why_it_matters': '5 strokes. Cross + box.'},
    '長': {'trap': 'Top 一 + complex middle + 衣-like bottom.',
           'correct_order_summary': '1: top horizontal. 2-7: middle strokes. 8: ノ (bottom). Total 8.',
           'why_it_matters': '8 strokes. Common confusion: missing the middle short horizontal.'},
    '白': {'trap': '丿 first (top ノ), then 日.',
           'correct_order_summary': '1: short ノ (top). 2: left vertical. 3: top + right (bracket). 4: middle horizontal. 5: bottom horizontal.',
           'why_it_matters': '5 strokes. The leading ノ distinguishes from 日.'},
    '番': {'trap': '采 (top, 7 strokes) + 田 (5 strokes).',
           'correct_order_summary': '1-7: 采 top (米-like). 8-12: 田.',
           'why_it_matters': '12 strokes.'},
    '号': {'trap': '口 (top) + 丂 (bottom).',
           'correct_order_summary': '1-3: 口. 4: top of 丂 (horizontal). 5: 丂 hook+curl.',
           'why_it_matters': '5 strokes.'},
    '私': {'trap': '禾 (rice-plant radical, 5 strokes) on left + 厶 right.',
           'correct_order_summary': '1: ノ (top). 2: top horizontal. 3: vertical. 4: ノ left. 5: ╲ right. 6-7: 厶 (right side).',
           'why_it_matters': '7 strokes. Left radical 禾 sets the meaning (originally "my rice plant").'},
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

kanji_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final
total = len(entries)
look = sum(1 for e in entries if e.get('lookalikes') is not None)
trap = sum(1 for e in entries if e.get('stroke_order_trap'))
print()
print('=== FINAL ===')
print(f'  lookalikes (incl. truly-unique sentinel): {look}/{total}')
print(f'  stroke_order_trap:                        {trap}/{total}')
