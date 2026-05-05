"""Round-7 Batch C — quick content wins (2026-05-06).

Adds four cross-cutting content layers in one pass:
  1. IMP-084: transitivity pair_id on the 12 canonical N5 transitive/
     intransitive verb pairs (開ける/開く etc.)
  2. ISSUE-064 partial / IMP-083: confusable_with cross-links on the 8
     well-known visually-confusable kanji clusters.
  3. IMP-085: false_friends_zh on N5 vocab entries that share a glyph with
     Mandarin but mean something different (大丈夫, 手紙, 娘, 勉強, ...).
  4. ISSUE-069: sources arrays on the top-30 N5 grammar patterns
     (Genki/Minna/Bunpro/JLPT-Sensei/JLPT-jp provenance).

All four are additive and idempotent. No rendering changes; downstream
JS readers can lazily consume the new fields.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
VF = ROOT / 'data' / 'vocab.json'
KF = ROOT / 'data' / 'kanji.json'
GF = ROOT / 'data' / 'grammar.json'

# ============================================================
# 1. IMP-084: transitivity pairs
# ============================================================
# Each pair_id groups one transitive + one intransitive entry.
# Format: pair_id -> [(form, reading, transitivity), ...]
TRANSITIVITY_PAIRS = {
    'open':       [('開ける', 'あける', 'transitive'),   ('開く', 'あく', 'intransitive')],
    'close':      [('閉める', 'しめる', 'transitive'),   ('閉まる', 'しまる', 'intransitive')],
    'enter':      [('入れる', 'いれる', 'transitive'),   ('入る', 'はいる', 'intransitive')],
    'exit':       [('出す',   'だす',   'transitive'),   ('出る',  'でる',  'intransitive')],
    'begin':      [('始める', 'はじめる', 'transitive'), ('始まる', 'はじまる', 'intransitive')],
    'stop':       [('止める', 'とめる', 'transitive'),   ('止まる', 'とまる', 'intransitive')],
    'switch_on':  [('つける', 'つける', 'transitive'),   ('つく',   'つく',   'intransitive')],
    'switch_off': [('消す',   'けす',   'transitive'),   ('消える', 'きえる', 'intransitive')],
    'wake':       [('起こす', 'おこす', 'transitive'),   ('起きる', 'おきる', 'intransitive')],
    'drop':       [('落とす', 'おとす', 'transitive'),   ('落ちる', 'おちる', 'intransitive')],
    'fix':        [('直す',   'なおす', 'transitive'),   ('直る',   'なおる', 'intransitive')],
    'cut':        [('切る',   'きる',   'transitive'),   ('切れる', 'きれる', 'intransitive')],
}

# ============================================================
# 2. IMP-083: confusable kanji clusters
# ============================================================
# Each cluster is a set of visually-similar kanji that learners conflate.
# We add `confusable_with: [glyph, ...]` to each kanji listing the OTHER
# members of its cluster.
CONFUSABLE_CLUSTERS = [
    ['大', '犬', '太'],          # the dot moves
    ['木', '本', '末', '未'],    # line position
    ['人', '入', '八'],          # radical similarity
    ['日', '目', '白'],          # rectangle variations
    ['千', '干'],                # vertical bar
    ['上', '止', '正'],          # cross-bar position
    ['古', '占'],                # stroke count (top-half)
    ['千', '午'],                # top stroke direction
]

# ============================================================
# 3. IMP-085: Mandarin false-friends
# ============================================================
# (form, reading) -> Mandarin meaning that DIFFERS from JA. The note
# warns Mandarin-L1 learners not to apply the Chinese reading.
MANDARIN_FALSE_FRIENDS = {
    ('大丈夫', 'だいじょうぶ'): "Looks like Mandarin 大丈夫 ('big husband'); in Japanese means 'OK / no problem'. The literal kanji breakdown is misleading.",
    ('手紙', 'てがみ'):           "Looks like Mandarin 手纸 ('toilet paper'); in Japanese means 'letter (correspondence)'.",
    ('娘', 'むすめ'):             "Looks like Mandarin 娘 ('mother'); in Japanese means 'daughter'. Polar-opposite generation.",
    ('勉強', 'べんきょう'):       "Mandarin 勉强 means 'reluctantly / barely'; in Japanese 勉強 means 'study'. Mandarin learners must un-learn the negative connotation.",
    ('先生', 'せんせい'):         "Mandarin 先生 ('Mr.' / 'sir', polite address for any adult man); in Japanese 'teacher / doctor / professional', much narrower.",
    ('丈夫', 'じょうぶ'):         "Mandarin 丈夫 ('husband'); in Japanese means 'sturdy / durable'. Different domain entirely.",
    ('機', 'き'):                 "Mandarin 机 (jī) ='machine' / 'opportunity'; in Japanese 机 (つくえ) means 'desk', 機 (き) is 'machine'. The simplified-Chinese 机 maps to Japanese 机 (desk), but the Mandarin meaning is 'machine'.",
    ('湯', 'ゆ'):                 "Mandarin 汤 ('soup'); in Japanese 湯 means 'hot water'. お湯 is hot water, NOT soup. Order お湯 in a restaurant and you get plain hot water.",
    ('愛人', 'あいじん'):         "Mandarin 爱人 ('spouse', neutral term for husband or wife); in Japanese 愛人 means 'lover / mistress', strongly negative.",
    ('勝手', 'かって'):           "Mandarin 胜手 is uncommon; in Japanese 勝手 means 'one's own way / selfish' or, separately, 'kitchen' (as in 勝手口 = kitchen door).",
    ('迷惑', 'めいわく'):         "Mandarin 迷惑 ('puzzled / confused'); in Japanese 迷惑 means 'trouble / inconvenience caused to others'. Different domain.",
    ('結構', 'けっこう'):         "Mandarin 结构 ('structure'); in Japanese 結構 means 'fine / no thank you' (when refusing) or 'quite / rather' (adverb). Refusing food with 結構です sounds polite, not structural.",
    ('面白い', 'おもしろい'):     "Mandarin 面白 ('pale-faced'); in Japanese 面白い means 'interesting / fun'. The kanji breakdown 'face' + 'white' is misleading.",
    ('一番', 'いちばん'):         "Mandarin 一番 ('one round / one time') as a counter; in Japanese 一番 means 'most / number one (best)' as an adverb/adjective.",
    ('時間', 'じかん'):           "Mandarin 时间 ('time'); in Japanese 時間 also means 'time' BUT also serves as a duration counter ('hours': 二時間 = two hours). Mandarin uses 小时 for 'hours'.",
    ('女', 'おんな'):             "Mandarin 女 (nǚ) is a neutral 'female / woman'; in Japanese 女 (おんな) standalone is informal/blunt. Polite is 女性 (じょせい) or 女の人.",
    ('男', 'おとこ'):             "Mandarin 男 (nán) is neutral 'male / man'; in Japanese 男 (おとこ) standalone is informal/blunt. Polite is 男性 (だんせい) or 男の人.",
    ('学生', 'がくせい'):         "Mandarin 学生 covers all education levels; in Japanese 学生 typically refers to university/college students. For elementary/junior high use 小学生/中学生 specifically.",
    ('新聞', 'しんぶん'):         "Mandarin 新闻 means 'news (broadcast)'; in Japanese 新聞 means 'newspaper (printed)'. For TV news use ニュース.",
    ('車', 'くるま'):             "Mandarin 车 covers all vehicles; in Japanese 車 most commonly means 'car/automobile'. For 'bicycle' use 自転車; for 'train' use 電車.",
    ('地下鉄', 'ちかてつ'):       "Mandarin 地铁 ('subway'); Japanese 地下鉄 also 'subway' — same meaning, but the kanji 鉄 (iron) is jarring to Mandarin readers since simplified Chinese uses 铁.",
    ('中国', 'ちゅうごく'):       "Mandarin 中国 ('China'); in Japanese ALSO refers to a region of Western Honshu (中国地方 — Hiroshima, Okayama etc.). 'China' is unambiguously 中国 in news context, but in regional context it can mean the Japanese region.",
    ('天', 'てん'):               "Mandarin 天 ('day' / 'sky'); in Japanese 天 means 'heaven / sky' but is rarely a standalone word. For 'day' use 日.",
    ('家族', 'かぞく'):           "Mandarin 家族 ('clan, extended family'); in Japanese 家族 means immediate household family (one's own household). Use 一族 for clan-level.",
    ('暗算', 'あんざん'):         "Mandarin 暗算 ('to plot against / scheme'); in Japanese 暗算 means 'mental arithmetic'. Polar-opposite tone (one is sinister, one is academic).",
}

# ============================================================
# 4. ISSUE-069: sources arrays on top-30 patterns
# ============================================================
# Standard reference codes:
#   genki-1-l<N>     Genki I, Lesson N (1..12)
#   genki-2-l<N>     Genki II, Lesson N (13..23)
#   minna-1-c<N>     Minna no Nihongo I, Chapter N
#   minna-2-c<N>     Minna no Nihongo II, Chapter N (1..25)
#   bunpro-n5        Bunpro N5 deck
#   jlpt-sensei-n5   JLPT Sensei N5 list
#   jlpt-jp-official Old JLPT 出題基準 1994/2002 N4 (= modern N5 scope)
#   tae-kim          Tae Kim's guide (free)
#   tofugu-n5        Tofugu's N5 page
SOURCES_TOP30 = {
    'n5-001': ['genki-1-l1', 'minna-1-c1', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # です/だ
    'n5-002': ['genki-1-l1', 'minna-1-c1', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # は (topic)
    'n5-003': ['genki-1-l1', 'minna-1-c2', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # が (subject)
    'n5-004': ['genki-1-l2', 'minna-1-c2', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # を (object)
    'n5-005': ['genki-1-l2', 'minna-1-c3', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # に (place)
    'n5-006': ['genki-1-l3', 'minna-1-c5', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # で (means/place of action)
    'n5-007': ['genki-1-l4', 'minna-1-c4', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # と (with)
    'n5-008': ['genki-1-l4', 'minna-1-c5', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # から (from)
    'n5-009': ['genki-1-l4', 'minna-1-c5', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # まで (until)
    'n5-010': ['genki-1-l3', 'minna-1-c6', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # ます polite
    'n5-011': ['genki-1-l3', 'minna-1-c6', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # ました
    'n5-012': ['genki-1-l3', 'minna-1-c6', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # ません
    'n5-013': ['genki-1-l3', 'minna-1-c6', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # ませんでした
    'n5-014': ['genki-1-l5', 'minna-1-c8', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # i-adj affirmative
    'n5-015': ['genki-1-l5', 'minna-1-c8', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # i-adj negative
    'n5-016': ['genki-1-l5', 'minna-1-c8', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # i-adj past
    'n5-017': ['genki-1-l5', 'minna-1-c8', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # na-adj
    'n5-018': ['genki-1-l5', 'minna-1-c8', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # na-adj negative
    'n5-019': ['genki-1-l6', 'minna-1-c14', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'], # te-form
    'n5-020': ['genki-1-l6', 'minna-1-c14', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'], # te-form ください
    'n5-021': ['genki-1-l7', 'minna-1-c14', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'], # te-imasu (progressive)
    'n5-022': ['genki-1-l8', 'minna-1-c15', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'], # te-mo ii (permission)
    'n5-023': ['genki-1-l8', 'minna-1-c15', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'], # te-wa ikenai (prohibition)
    'n5-024': ['genki-1-l9', 'minna-1-c16', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'], # te-form chain
    'n5-025': ['genki-1-l3', 'minna-1-c4', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # も
    'n5-026': ['genki-1-l1', 'minna-1-c1', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # ね (sentence-final)
    'n5-027': ['genki-1-l1', 'minna-1-c1', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # よね
    'n5-028': ['genki-1-l1', 'minna-1-c1', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # よ
    'n5-029': ['genki-1-l1', 'minna-1-c2', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'],  # の (possessive)
    'n5-030': ['genki-1-l9', 'minna-1-c20', 'bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official'], # の (nominalizer)
}


def main() -> int:
    n_total = 0

    # === 1. transitivity pairs ===
    # Vocab catalog often stores form==reading (kana-only), so we match
    # on EITHER (form,reading) exact OR (reading) alone.
    vdata = json.loads(VF.read_text(encoding='utf-8'))
    pair_by_key = {}
    pair_by_reading = {}
    for pair_id, members in TRANSITIVITY_PAIRS.items():
        for form, reading, trans in members:
            pair_by_key[(form, reading)] = (pair_id, trans)
            # Reading-only fallback (kana-stored entries)
            pair_by_reading[reading] = (pair_id, trans)
    n_pair_added = 0
    for e in vdata.get('entries', []):
        form = e.get('form')
        reading = e.get('reading')
        key = (form, reading)
        match = pair_by_key.get(key) or pair_by_reading.get(reading)
        if match:
            pair_id, trans = match
            if e.get('pair_id') != pair_id or e.get('transitivity') != trans:
                e['pair_id'] = pair_id
                e['transitivity'] = trans
                n_pair_added += 1
    print(f'[IMP-084] Transitivity pairs tagged on {n_pair_added} entries.')
    n_total += n_pair_added

    # === 3. Mandarin false-friends ===
    # Same kana-only fallback as transitivity.
    ff_by_key = dict(MANDARIN_FALSE_FRIENDS)
    ff_by_reading = {reading: msg for (form, reading), msg in MANDARIN_FALSE_FRIENDS.items()}
    n_ff_added = 0
    seen_keys = set()
    for e in vdata.get('entries', []):
        form = e.get('form')
        reading = e.get('reading')
        key = (form, reading)
        if key in seen_keys:
            continue
        msg = ff_by_key.get(key) or ff_by_reading.get(reading)
        if msg:
            existing = e.get('false_friends') or {}
            if not isinstance(existing, dict):
                existing = {}
            if existing.get('zh') != msg:
                existing['zh'] = msg
                e['false_friends'] = existing
                n_ff_added += 1
            seen_keys.add(key)
    print(f'[IMP-085] Mandarin false-friend flags added on {n_ff_added} entries.')
    n_total += n_ff_added

    VF.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # === 2. confusable kanji clusters ===
    kdata = json.loads(KF.read_text(encoding='utf-8'))
    glyph_to_cluster = {}
    for cluster in CONFUSABLE_CLUSTERS:
        for glyph in cluster:
            others = [g for g in cluster if g != glyph]
            # Multiple clusters may share a glyph (e.g. 千 in two clusters);
            # union the others.
            existing = glyph_to_cluster.setdefault(glyph, [])
            for g in others:
                if g not in existing:
                    existing.append(g)

    n_cluster_added = 0
    for e in kdata.get('entries', []):
        glyph = e.get('glyph')
        if glyph in glyph_to_cluster:
            new_list = glyph_to_cluster[glyph]
            if e.get('confusable_with') != new_list:
                e['confusable_with'] = new_list
                n_cluster_added += 1
    print(f'[IMP-083] Confusable cluster cross-links added on {n_cluster_added} kanji.')
    n_total += n_cluster_added
    KF.write_text(json.dumps(kdata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # === 4. sources arrays ===
    gdata = json.loads(GF.read_text(encoding='utf-8'))
    n_sources_added = 0
    for p in gdata.get('patterns', []):
        pid = p.get('id')
        if pid in SOURCES_TOP30:
            new_sources = SOURCES_TOP30[pid]
            if p.get('sources') != new_sources:
                p['sources'] = new_sources
                n_sources_added += 1
    print(f'[ISSUE-069] sources arrays added on {n_sources_added} patterns.')
    n_total += n_sources_added
    GF.write_text(json.dumps(gdata, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print(f'\nTotal field updates this pass: {n_total}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
