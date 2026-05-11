"""Kanji Batch D (2026-05-11):
Add two new pedagogical fields to every kanji:
- on_kun_pair_drill: concrete on-yomi vs kun-yomi example pair
- n5_compounds: auto-derived list of N5 vocab forms containing this kanji
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

kanji_path = ROOT / 'data' / 'kanji.json'
data = json.loads(kanji_path.read_text(encoding='utf-8'))
entries = data.get('entries', [])

# ==================== n5_compounds: scan vocab.json ====================
print('=== n5_compounds: scan vocab.json for occurrences ===')
V = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))['entries']

# Build glyph -> list of compounds map
glyph_to_compounds = defaultdict(list)
for v in V:
    form = v.get('form') or ''
    reading = v.get('reading') or ''
    gloss = v.get('gloss') or ''
    for ch in form:
        if 0x4E00 <= ord(ch) <= 0x9FFF:  # kanji
            glyph_to_compounds[ch].append({
                'form': form,
                'reading': reading,
                'gloss': gloss[:50],
                'vocab_id': v.get('id'),
            })

# Annotate kanji entries
compounds_added = 0
for e in entries:
    g = e.get('glyph') or e.get('id','').split('.')[-1]
    if not g:
        continue
    compounds = glyph_to_compounds.get(g, [])
    if compounds and not e.get('n5_compounds'):
        # Sort by length (shortest first — primary compounds), cap at 15
        compounds_sorted = sorted(compounds, key=lambda c: len(c['form']))[:15]
        e['n5_compounds'] = compounds_sorted
        e['n5_compounds_provenance'] = 'auto_derived'
        compounds_added += 1

print(f'  Annotated with n5_compounds: {compounds_added}')

# Density-3 check: kanji with <2 N5 vocab compounds
sparse = []
for e in entries:
    g = e.get('glyph') or e.get('id','').split('.')[-1]
    n_compounds = len(glyph_to_compounds.get(g, []))
    if n_compounds < 2:
        sparse.append((g, n_compounds))
print(f'  Density floor (<2 N5 vocab): {len(sparse)} kanji')
if sparse:
    print(f'    Examples: {sparse[:10]}')


# ==================== on_kun_pair_drill ====================
print()
print('=== on_kun_pair_drill: concrete on/kun example pairs ===')
# For each kanji, author 1 standalone (typically kun-yomi) + 1 compound (typically on-yomi) pair
# Schema: {standalone: {form, reading, gloss}, compound: {form, reading, gloss}, contrast_note}

PAIRS = {
    '一': {'standalone': {'form': '一つ', 'reading': 'ひとつ', 'gloss': 'one thing (kun-stem 一-)'},
           'compound':   {'form': '一月', 'reading': 'いちがつ', 'gloss': 'January (on-yomi)'},
           'contrast_note': 'Numbers usually take on-yomi (いち) in compounds and times; kun (ひと-) appears in counter 一つ.'},
    '二': {'standalone': {'form': '二つ', 'reading': 'ふたつ', 'gloss': 'two things (kun-stem)'},
           'compound':   {'form': '二月', 'reading': 'にがつ', 'gloss': 'February (on)'},
           'contrast_note': '二 reads ふた- in 一/二/三-counter compounds; に in numerical compounds.'},
    '三': {'standalone': {'form': '三つ', 'reading': 'みっつ', 'gloss': 'three things (kun)'},
           'compound':   {'form': '三月', 'reading': 'さんがつ', 'gloss': 'March (on)'},
           'contrast_note': 'みっつ kun in 〜つ counter; さん on in numerical/time compounds.'},
    '四': {'standalone': {'form': '四つ', 'reading': 'よっつ', 'gloss': 'four things (kun)'},
           'compound':   {'form': '四月', 'reading': 'しがつ', 'gloss': 'April (on, irregular)'},
           'contrast_note': '四 has THREE readings: よ (4-time), し (months/sino-compounds), よん (general).'},
    '五': {'standalone': {'form': '五つ', 'reading': 'いつつ', 'gloss': 'five things (kun)'},
           'compound':   {'form': '五月', 'reading': 'ごがつ', 'gloss': 'May (on)'},
           'contrast_note': 'いつ- (kun) in counter; ご (on) in compounds.'},
    '六': {'standalone': {'form': '六つ', 'reading': 'むっつ', 'gloss': 'six things (kun)'},
           'compound':   {'form': '六月', 'reading': 'ろくがつ', 'gloss': 'June (on)'},
           'contrast_note': 'むっ- (kun); ろく (on).'},
    '七': {'standalone': {'form': '七つ', 'reading': 'ななつ', 'gloss': 'seven things (kun)'},
           'compound':   {'form': '七月', 'reading': 'しちがつ', 'gloss': 'July (on)'},
           'contrast_note': '七 has both しち (on) and なな (kun); しち in months, なな more common in modern speech.'},
    '八': {'standalone': {'form': '八つ', 'reading': 'やっつ', 'gloss': 'eight things (kun)'},
           'compound':   {'form': '八月', 'reading': 'はちがつ', 'gloss': 'August (on)'},
           'contrast_note': 'やっ- (kun); はち (on).'},
    '九': {'standalone': {'form': '九つ', 'reading': 'ここのつ', 'gloss': 'nine things (kun)'},
           'compound':   {'form': '九月', 'reading': 'くがつ', 'gloss': 'September (on, irregular く)'},
           'contrast_note': '九 has く and きゅう (on) variants; く in dates/times.'},
    '十': {'standalone': {'form': '十', 'reading': 'とお', 'gloss': 'ten (kun, no -tsu)'},
           'compound':   {'form': '十月', 'reading': 'じゅうがつ', 'gloss': 'October (on)'},
           'contrast_note': '十 reads とお as standalone count and じゅう in compounds.'},
    '百': {'standalone': {'form': '百', 'reading': 'ひゃく', 'gloss': '100 (on)'},
           'compound':   {'form': '三百', 'reading': 'さんびゃく', 'gloss': '300 (compound with sound change)'},
           'contrast_note': '百 only has on-yomi ひゃく; sound changes (びゃく/ぴゃく) by preceding number.'},
    '千': {'standalone': {'form': '千', 'reading': 'せん', 'gloss': '1,000 (on)'},
           'compound':   {'form': '三千', 'reading': 'さんぜん', 'gloss': '3,000 (compound with sound change ぜん)'},
           'contrast_note': '千 only has on せん; combines with ぜん variant.'},
    '万': {'standalone': {'form': '万', 'reading': 'まん', 'gloss': '10,000 (on)'},
           'compound':   {'form': '一万', 'reading': 'いちまん', 'gloss': '10,000 (on, with まん)'},
           'contrast_note': '万 standalone まん; compounds use まん with the preceding number.'},
    '円': {'standalone': {'form': '円', 'reading': 'えん', 'gloss': 'yen / circle (on)'},
           'compound':   {'form': '百円', 'reading': 'ひゃくえん', 'gloss': '100 yen (compound)'},
           'contrast_note': '円 reads えん (on) standalone for "yen" or in compounds.'},
    '日': {'standalone': {'form': '日', 'reading': 'ひ', 'gloss': 'day (kun)'},
           'compound':   {'form': '日本', 'reading': 'にほん', 'gloss': 'Japan (on+on)'},
           'contrast_note': '日 reads ひ (kun, "day/sun") standalone, にち/じつ (on) in most compounds.'},
    '月': {'standalone': {'form': '月', 'reading': 'つき', 'gloss': 'moon (kun)'},
           'compound':   {'form': '月曜日', 'reading': 'げつようび', 'gloss': 'Monday (on)'},
           'contrast_note': '月 kun=つき (moon) standalone, on=げつ/がつ in day-name/month compounds.'},
    '火': {'standalone': {'form': '火', 'reading': 'ひ', 'gloss': 'fire (kun)'},
           'compound':   {'form': '火曜日', 'reading': 'かようび', 'gloss': 'Tuesday (on)'},
           'contrast_note': '火 kun=ひ (fire) standalone, on=か in day-name compounds.'},
    '水': {'standalone': {'form': '水', 'reading': 'みず', 'gloss': 'water (kun)'},
           'compound':   {'form': '水曜日', 'reading': 'すいようび', 'gloss': 'Wednesday (on)'},
           'contrast_note': '水 kun=みず, on=すい in day-name and Sino-compounds.'},
    '木': {'standalone': {'form': '木', 'reading': 'き', 'gloss': 'tree (kun)'},
           'compound':   {'form': '木曜日', 'reading': 'もくようび', 'gloss': 'Thursday (on)'},
           'contrast_note': '木 kun=き (tree), on=もく in compounds.'},
    '金': {'standalone': {'form': '金', 'reading': 'かね', 'gloss': 'money / gold (kun)'},
           'compound':   {'form': '金曜日', 'reading': 'きんようび', 'gloss': 'Friday (on)'},
           'contrast_note': '金 kun=かね/きん (money), on=きん in day-name compounds.'},
    '土': {'standalone': {'form': '土', 'reading': 'つち', 'gloss': 'earth / soil (kun)'},
           'compound':   {'form': '土曜日', 'reading': 'どようび', 'gloss': 'Saturday (on)'},
           'contrast_note': '土 kun=つち, on=ど in day-name compounds.'},
    '人': {'standalone': {'form': '人', 'reading': 'ひと', 'gloss': 'person (kun)'},
           'compound':   {'form': '日本人', 'reading': 'にほんじん', 'gloss': 'Japanese person (on)'},
           'contrast_note': '人 kun=ひと, on=じん in nationality/group compounds.'},
    '子': {'standalone': {'form': '子', 'reading': 'こ', 'gloss': 'child (kun)'},
           'compound':   {'form': '子供', 'reading': 'こども', 'gloss': 'child (kun+kun)'},
           'contrast_note': '子 kun=こ standalone or compound. on=し (e.g. 椅子 いす — N4+).'},
    '父': {'standalone': {'form': '父', 'reading': 'ちち', 'gloss': 'my father (kun)'},
           'compound':   {'form': 'お父さん', 'reading': 'おとうさん', 'gloss': "father / someone else's father (kun, polite)"},
           'contrast_note': '父 kun=ちち (humble) vs お父さん (polite, about others).'},
    '母': {'standalone': {'form': '母', 'reading': 'はは', 'gloss': 'my mother (kun)'},
           'compound':   {'form': 'お母さん', 'reading': 'おかあさん', 'gloss': "mother (polite)"},
           'contrast_note': '母 kun=はは (humble) vs お母さん (polite).'},
    '友': {'standalone': {'form': '友', 'reading': 'とも', 'gloss': 'friend (kun, formal)'},
           'compound':   {'form': '友達', 'reading': 'ともだち', 'gloss': 'friend (kun + N5-tail)'},
           'contrast_note': '友 kun=とも; common compound 友達 (友達 is N4 but とも is N5).'},
    '男': {'standalone': {'form': '男', 'reading': 'おとこ', 'gloss': 'man (kun)'},
           'compound':   {'form': '男の子', 'reading': 'おとこのこ', 'gloss': 'boy'},
           'contrast_note': '男 kun=おとこ. on=だん in 男性.'},
    '女': {'standalone': {'form': '女', 'reading': 'おんな', 'gloss': 'woman (kun)'},
           'compound':   {'form': '女の子', 'reading': 'おんなのこ', 'gloss': 'girl'},
           'contrast_note': '女 kun=おんな. on=じょ in 女性.'},
    '先': {'standalone': {'form': '先', 'reading': 'さき', 'gloss': 'before / ahead (kun)'},
           'compound':   {'form': '先生', 'reading': 'せんせい', 'gloss': 'teacher (on)'},
           'contrast_note': '先 kun=さき (ahead/before), on=せん in 先生/先週.'},
    '生': {'standalone': {'form': '生きる', 'reading': 'いきる', 'gloss': 'to live (kun-verb)'},
           'compound':   {'form': '学生', 'reading': 'がくせい', 'gloss': 'student (on)'},
           'contrast_note': '生 has multiple readings: い-(kun verb), う- (kun verb), せい/しょう (on).'},
    '学': {'standalone': {'form': '学ぶ', 'reading': 'まなぶ', 'gloss': 'to learn (kun-verb)'},
           'compound':   {'form': '学校', 'reading': 'がっこう', 'gloss': 'school (on+on)'},
           'contrast_note': '学 kun=まな-ぶ (verb), on=がく in compounds.'},
    '校': {'standalone': {'form': '校', 'reading': 'こう', 'gloss': '(on; school — appears mostly in compounds)'},
           'compound':   {'form': '高校', 'reading': 'こうこう', 'gloss': 'high school'},
           'contrast_note': '校 only on=こう; rarely standalone.'},
    '本': {'standalone': {'form': '本', 'reading': 'ほん', 'gloss': 'book (on)'},
           'compound':   {'form': '日本', 'reading': 'にほん', 'gloss': 'Japan (on+on)'},
           'contrast_note': '本 is unusual: uses on-yomi ほん even standalone. kun=もと (origin).'},
    '名': {'standalone': {'form': '名前', 'reading': 'なまえ', 'gloss': 'name (kun)'},
           'compound':   {'form': '有名', 'reading': 'ゆうめい', 'gloss': 'famous (on) — N4'},
           'contrast_note': '名 kun=な (name), on=めい in compounds.'},
    '時': {'standalone': {'form': '時', 'reading': 'とき', 'gloss': 'time / occasion (kun)'},
           'compound':   {'form': '時間', 'reading': 'じかん', 'gloss': 'time / duration (on)'},
           'contrast_note': '時 kun=とき (occasion), on=じ in clock-time compounds.'},
    '間': {'standalone': {'form': '間', 'reading': 'あいだ', 'gloss': 'between (kun)'},
           'compound':   {'form': '時間', 'reading': 'じかん', 'gloss': 'time-duration (on)'},
           'contrast_note': '間 kun=あいだ, on=かん/けん in compounds.'},
    '年': {'standalone': {'form': '年', 'reading': 'とし', 'gloss': 'year (kun)'},
           'compound':   {'form': '来年', 'reading': 'らいねん', 'gloss': 'next year (on)'},
           'contrast_note': '年 kun=とし (one\'s years), on=ねん in compounds.'},
    '今': {'standalone': {'form': '今', 'reading': 'いま', 'gloss': 'now (kun)'},
           'compound':   {'form': '今日', 'reading': 'きょう', 'gloss': 'today (special reading)'},
           'contrast_note': '今 kun=いま standalone; on=こん in compounds; 今日 has irregular reading きょう.'},
    '行': {'standalone': {'form': '行く', 'reading': 'いく', 'gloss': 'to go (kun-verb)'},
           'compound':   {'form': '銀行', 'reading': 'ぎんこう', 'gloss': 'bank (on)'},
           'contrast_note': '行 kun=い-く (verb), on=こう in compounds.'},
    '来': {'standalone': {'form': '来る', 'reading': 'くる', 'gloss': 'to come (kun-verb)'},
           'compound':   {'form': '来年', 'reading': 'らいねん', 'gloss': 'next year (on)'},
           'contrast_note': '来 kun=く-る (verb), on=らい in compounds.'},
    '見': {'standalone': {'form': '見る', 'reading': 'みる', 'gloss': 'to see (kun-verb)'},
           'compound':   {'form': '意見', 'reading': 'いけん', 'gloss': 'opinion (on) — N4'},
           'contrast_note': '見 kun=み-る (verb), on=けん in compounds.'},
    '聞': {'standalone': {'form': '聞く', 'reading': 'きく', 'gloss': 'to listen / ask (kun-verb)'},
           'compound':   {'form': '新聞', 'reading': 'しんぶん', 'gloss': 'newspaper (on)'},
           'contrast_note': '聞 kun=き-く (verb), on=ぶん in compounds.'},
    '読': {'standalone': {'form': '読む', 'reading': 'よむ', 'gloss': 'to read (kun-verb)'},
           'compound':   {'form': '読書', 'reading': 'どくしょ', 'gloss': 'reading (books) (on) — N4'},
           'contrast_note': '読 kun=よ-む (verb), on=どく in compounds.'},
    '書': {'standalone': {'form': '書く', 'reading': 'かく', 'gloss': 'to write (kun-verb)'},
           'compound':   {'form': '書道', 'reading': 'しょどう', 'gloss': 'calligraphy (on) — N4'},
           'contrast_note': '書 kun=か-く (verb), on=しょ in compounds.'},
    '話': {'standalone': {'form': '話す', 'reading': 'はなす', 'gloss': 'to talk (kun-verb)'},
           'compound':   {'form': '電話', 'reading': 'でんわ', 'gloss': 'phone (on)'},
           'contrast_note': '話 kun=はな-す (verb), on=わ in compounds.'},
    '食': {'standalone': {'form': '食べる', 'reading': 'たべる', 'gloss': 'to eat (kun-verb)'},
           'compound':   {'form': '食事', 'reading': 'しょくじ', 'gloss': 'meal (on)'},
           'contrast_note': '食 kun=た-べる (verb), on=しょく in compounds.'},
    '飲': {'standalone': {'form': '飲む', 'reading': 'のむ', 'gloss': 'to drink (kun-verb)'},
           'compound':   {'form': '飲料', 'reading': 'いんりょう', 'gloss': 'drinks (on) — N4'},
           'contrast_note': '飲 kun=の-む (verb), on=いん in compounds.'},
    '買': {'standalone': {'form': '買う', 'reading': 'かう', 'gloss': 'to buy (kun-verb)'},
           'compound':   {'form': '売買', 'reading': 'ばいばい', 'gloss': 'buying/selling (on) — N4'},
           'contrast_note': '買 kun=か-う (verb), on=ばい in compounds.'},
    '言': {'standalone': {'form': '言う', 'reading': 'いう', 'gloss': 'to say (kun-verb)'},
           'compound':   {'form': '言語', 'reading': 'げんご', 'gloss': 'language (on) — N4'},
           'contrast_note': '言 kun=い-う (verb), on=げん/ごん in compounds.'},
    '入': {'standalone': {'form': '入る', 'reading': 'はいる', 'gloss': 'to enter (kun-verb)'},
           'compound':   {'form': '入口', 'reading': 'いりぐち', 'gloss': 'entrance (kun+kun!)'},
           'contrast_note': '入 has both kun (はい-る, い-る verbs) and on (にゅう); 入口 unusually combines kun+kun.'},
    '出': {'standalone': {'form': '出る', 'reading': 'でる', 'gloss': 'to exit (kun-verb)'},
           'compound':   {'form': '出口', 'reading': 'でぐち', 'gloss': 'exit (kun+kun)'},
           'contrast_note': '出 kun=で-る/だ-す (verbs), on=しゅつ in compounds.'},
    '立': {'standalone': {'form': '立つ', 'reading': 'たつ', 'gloss': 'to stand (kun-verb)'},
           'compound':   {'form': '国立', 'reading': 'こくりつ', 'gloss': 'national (on) — N4'},
           'contrast_note': '立 kun=た-つ, on=りつ in compounds.'},
    '休': {'standalone': {'form': '休む', 'reading': 'やすむ', 'gloss': 'to rest (kun-verb)'},
           'compound':   {'form': '休日', 'reading': 'きゅうじつ', 'gloss': 'holiday (on)'},
           'contrast_note': '休 kun=やす-む, on=きゅう in compounds.'},
    '高': {'standalone': {'form': '高い', 'reading': 'たかい', 'gloss': 'expensive / tall (kun-adj)'},
           'compound':   {'form': '高校', 'reading': 'こうこう', 'gloss': 'high school (on)'},
           'contrast_note': '高 kun=たか-い (adj), on=こう in compounds.'},
    '安': {'standalone': {'form': '安い', 'reading': 'やすい', 'gloss': 'cheap (kun-adj)'},
           'compound':   {'form': '安心', 'reading': 'あんしん', 'gloss': 'peace of mind (on)'},
           'contrast_note': '安 kun=やす-い (adj), on=あん in compounds.'},
    '新': {'standalone': {'form': '新しい', 'reading': 'あたらしい', 'gloss': 'new (kun-adj)'},
           'compound':   {'form': '新聞', 'reading': 'しんぶん', 'gloss': 'newspaper (on)'},
           'contrast_note': '新 kun=あたら-しい (adj), on=しん in compounds.'},
    '古': {'standalone': {'form': '古い', 'reading': 'ふるい', 'gloss': 'old (kun-adj)'},
           'compound':   {'form': '中古', 'reading': 'ちゅうこ', 'gloss': 'used (item) (on) — N4'},
           'contrast_note': '古 kun=ふる-い (adj), on=こ in compounds.'},
    '長': {'standalone': {'form': '長い', 'reading': 'ながい', 'gloss': 'long (kun-adj)'},
           'compound':   {'form': '社長', 'reading': 'しゃちょう', 'gloss': 'company president (on)'},
           'contrast_note': '長 kun=なが-い (adj), on=ちょう in compounds.'},
    '大': {'standalone': {'form': '大きい', 'reading': 'おおきい', 'gloss': 'big (kun-adj)'},
           'compound':   {'form': '大学', 'reading': 'だいがく', 'gloss': 'university (on)'},
           'contrast_note': '大 kun=おお-きい (adj), on=だい/たい in compounds.'},
    '小': {'standalone': {'form': '小さい', 'reading': 'ちいさい', 'gloss': 'small (kun-adj)'},
           'compound':   {'form': '小学校', 'reading': 'しょうがっこう', 'gloss': 'elementary school (on)'},
           'contrast_note': '小 kun=ちい-さい (adj), on=しょう in compounds.'},
    '上': {'standalone': {'form': '上', 'reading': 'うえ', 'gloss': 'top / above (kun)'},
           'compound':   {'form': '上手', 'reading': 'じょうず', 'gloss': 'skilled (on+kun unique reading)'},
           'contrast_note': '上 kun=うえ, on=じょう in compounds.'},
    '下': {'standalone': {'form': '下', 'reading': 'した', 'gloss': 'below (kun)'},
           'compound':   {'form': '下手', 'reading': 'へた', 'gloss': 'unskilled (kun+kun unique)'},
           'contrast_note': '下 kun=した, on=か/げ in compounds.'},
    '中': {'standalone': {'form': '中', 'reading': 'なか', 'gloss': 'inside / middle (kun)'},
           'compound':   {'form': '中国', 'reading': 'ちゅうごく', 'gloss': 'China (on)'},
           'contrast_note': '中 kun=なか, on=ちゅう in compounds.'},
    '左': {'standalone': {'form': '左', 'reading': 'ひだり', 'gloss': 'left (kun)'},
           'compound':   {'form': '左右', 'reading': 'さゆう', 'gloss': 'left and right (on)'},
           'contrast_note': '左 kun=ひだり, on=さ in compounds.'},
    '右': {'standalone': {'form': '右', 'reading': 'みぎ', 'gloss': 'right (kun)'},
           'compound':   {'form': '左右', 'reading': 'さゆう', 'gloss': 'left and right (on)'},
           'contrast_note': '右 kun=みぎ, on=う/ゆう in compounds.'},
    '東': {'standalone': {'form': '東', 'reading': 'ひがし', 'gloss': 'east (kun)'},
           'compound':   {'form': '東京', 'reading': 'とうきょう', 'gloss': 'Tokyo (on)'},
           'contrast_note': '東 kun=ひがし, on=とう in compounds.'},
    '西': {'standalone': {'form': '西', 'reading': 'にし', 'gloss': 'west (kun)'},
           'compound':   {'form': '関西', 'reading': 'かんさい', 'gloss': 'Kansai region (on) — N4'},
           'contrast_note': '西 kun=にし, on=さい/せい in compounds.'},
    '南': {'standalone': {'form': '南', 'reading': 'みなみ', 'gloss': 'south (kun)'},
           'compound':   {'form': '南北', 'reading': 'なんぼく', 'gloss': 'north-south (on)'},
           'contrast_note': '南 kun=みなみ, on=なん in compounds.'},
    '北': {'standalone': {'form': '北', 'reading': 'きた', 'gloss': 'north (kun)'},
           'compound':   {'form': '東北', 'reading': 'とうほく', 'gloss': 'Tohoku region (on)'},
           'contrast_note': '北 kun=きた, on=ほく in compounds.'},
    '前': {'standalone': {'form': '前', 'reading': 'まえ', 'gloss': 'front / before (kun)'},
           'compound':   {'form': '名前', 'reading': 'なまえ', 'gloss': 'name (kun)'},
           'contrast_note': '前 kun=まえ, on=ぜん in compounds.'},
    '後': {'standalone': {'form': '後ろ', 'reading': 'うしろ', 'gloss': 'behind (kun)'},
           'compound':   {'form': '午後', 'reading': 'ごご', 'gloss': 'afternoon (on)'},
           'contrast_note': '後 kun=うし-ろ / あと, on=ご/こう in compounds.'},
    '外': {'standalone': {'form': '外', 'reading': 'そと', 'gloss': 'outside (kun)'},
           'compound':   {'form': '外国', 'reading': 'がいこく', 'gloss': 'foreign country (on)'},
           'contrast_note': '外 kun=そと, on=がい in compounds.'},
    '国': {'standalone': {'form': '国', 'reading': 'くに', 'gloss': 'country (kun)'},
           'compound':   {'form': '中国', 'reading': 'ちゅうごく', 'gloss': 'China (on)'},
           'contrast_note': '国 kun=くに, on=こく in compounds.'},
    '会': {'standalone': {'form': '会う', 'reading': 'あう', 'gloss': 'to meet (kun-verb)'},
           'compound':   {'form': '会社', 'reading': 'かいしゃ', 'gloss': 'company (on+on)'},
           'contrast_note': '会 kun=あ-う (verb), on=かい in compounds.'},
    '社': {'standalone': {'form': '社', 'reading': 'しゃ', 'gloss': '(on — appears in compounds)'},
           'compound':   {'form': '会社', 'reading': 'かいしゃ', 'gloss': 'company'},
           'contrast_note': '社 only on=しゃ; rarely standalone.'},
    '員': {'standalone': {'form': '員', 'reading': 'いん', 'gloss': '(on — member-suffix)'},
           'compound':   {'form': '会社員', 'reading': 'かいしゃいん', 'gloss': 'company employee'},
           'contrast_note': '員 only on=いん; suffix in workplace compounds.'},
    '力': {'standalone': {'form': '力', 'reading': 'ちから', 'gloss': 'strength (kun)'},
           'compound':   {'form': '電力', 'reading': 'でんりょく', 'gloss': 'electric power (on)'},
           'contrast_note': '力 kun=ちから, on=りょく in compounds.'},
    '私': {'standalone': {'form': '私', 'reading': 'わたし', 'gloss': 'I / me (kun)'},
           'compound':   {'form': '私立', 'reading': 'しりつ', 'gloss': 'private (school) (on) — N4'},
           'contrast_note': '私 kun=わたし (informal わたくし), on=し in compounds.'},
    '何': {'standalone': {'form': '何', 'reading': 'なに', 'gloss': 'what (kun)'},
           'compound':   {'form': '何時', 'reading': 'なんじ', 'gloss': 'what time (なん before counter)'},
           'contrast_note': '何 has two readings: なに (standalone) and なん (before counter compounds: 何時/何人/何月).'},
    '田': {'standalone': {'form': '田', 'reading': 'た', 'gloss': 'rice field (kun)'},
           'compound':   {'form': '田中', 'reading': 'たなか', 'gloss': 'Tanaka (surname)'},
           'contrast_note': '田 kun=た, appears in many surnames (田中/山田).'},
    '山': {'standalone': {'form': '山', 'reading': 'やま', 'gloss': 'mountain (kun)'},
           'compound':   {'form': '富士山', 'reading': 'ふじさん', 'gloss': 'Mt. Fuji (on with rendaku)'},
           'contrast_note': '山 kun=やま, on=さん in mountain-name compounds.'},
    '川': {'standalone': {'form': '川', 'reading': 'かわ', 'gloss': 'river (kun)'},
           'compound':   {'form': '小川', 'reading': 'おがわ', 'gloss': 'stream / surname (kun+kun)'},
           'contrast_note': '川 kun=かわ, on=せん rare.'},
    '雨': {'standalone': {'form': '雨', 'reading': 'あめ', 'gloss': 'rain (kun)'},
           'compound':   {'form': '大雨', 'reading': 'おおあめ', 'gloss': 'heavy rain (kun+kun)'},
           'contrast_note': '雨 kun=あめ, on=う rare.'},
    '天': {'standalone': {'form': '天', 'reading': 'てん', 'gloss': 'heaven (on)'},
           'compound':   {'form': '天気', 'reading': 'てんき', 'gloss': 'weather (on+on)'},
           'contrast_note': '天 mostly on=てん; kun=あめ archaic.'},
    '気': {'standalone': {'form': '気', 'reading': 'き', 'gloss': 'spirit / feeling (on)'},
           'compound':   {'form': '元気', 'reading': 'げんき', 'gloss': 'energetic (on+on) — N4 for 元'},
           'contrast_note': '気 only on=き/け; very common compound element.'},
    '花': {'standalone': {'form': '花', 'reading': 'はな', 'gloss': 'flower (kun)'},
           'compound':   {'form': '花火', 'reading': 'はなび', 'gloss': 'fireworks (kun+kun)'},
           'contrast_note': '花 kun=はな, on=か rare.'},
    '空': {'standalone': {'form': '空', 'reading': 'そら', 'gloss': 'sky (kun)'},
           'compound':   {'form': '空港', 'reading': 'くうこう', 'gloss': 'airport (on+on) — 港 is N4'},
           'contrast_note': '空 kun=そら, on=くう in compounds.'},
    '電': {'standalone': {'form': '電', 'reading': 'でん', 'gloss': '(on — electricity element)'},
           'compound':   {'form': '電車', 'reading': 'でんしゃ', 'gloss': 'train (on+on)'},
           'contrast_note': '電 only on=でん; element in many "electric" compounds.'},
    '車': {'standalone': {'form': '車', 'reading': 'くるま', 'gloss': 'car (kun)'},
           'compound':   {'form': '電車', 'reading': 'でんしゃ', 'gloss': 'train (on)'},
           'contrast_note': '車 kun=くるま standalone for "car", on=しゃ in vehicle compounds.'},
    '道': {'standalone': {'form': '道', 'reading': 'みち', 'gloss': 'road (kun)'},
           'compound':   {'form': '北海道', 'reading': 'ほっかいどう', 'gloss': 'Hokkaido (on)'},
           'contrast_note': '道 kun=みち, on=どう in compounds.'},
    '店': {'standalone': {'form': '店', 'reading': 'みせ', 'gloss': 'shop (kun)'},
           'compound':   {'form': '本店', 'reading': 'ほんてん', 'gloss': 'head store (on)'},
           'contrast_note': '店 kun=みせ, on=てん in compounds.'},
    '駅': {'standalone': {'form': '駅', 'reading': 'えき', 'gloss': 'station (on)'},
           'compound':   {'form': '東京駅', 'reading': 'とうきょうえき', 'gloss': 'Tokyo Station (on)'},
           'contrast_note': '駅 only on=えき; appears as both standalone and station-name suffix.'},
    '半': {'standalone': {'form': '半', 'reading': 'はん', 'gloss': 'half (on)'},
           'compound':   {'form': '半分', 'reading': 'はんぶん', 'gloss': 'half (on+on)'},
           'contrast_note': '半 on=はん; very common in time/half compounds.'},
    '分': {'standalone': {'form': '分かる', 'reading': 'わかる', 'gloss': 'to understand (kun-verb)'},
           'compound':   {'form': '十分', 'reading': 'じゅっぷん', 'gloss': '10 minutes (on)'},
           'contrast_note': '分 kun=わ-かる/わ-ける (verbs), on=ふん/ぷん (minutes) / ぶん (part).'},
    '毎': {'standalone': {'form': '毎日', 'reading': 'まいにち', 'gloss': 'every day (on)'},
           'compound':   {'form': '毎週', 'reading': 'まいしゅう', 'gloss': 'every week (on)'},
           'contrast_note': '毎 only on=まい; always in compounds for "every-".'},
    '週': {'standalone': {'form': '週', 'reading': 'しゅう', 'gloss': 'week (on)'},
           'compound':   {'form': '今週', 'reading': 'こんしゅう', 'gloss': 'this week'},
           'contrast_note': '週 only on=しゅう.'},
    '午': {'standalone': {'form': '午前', 'reading': 'ごぜん', 'gloss': 'morning (a.m.) (on)'},
           'compound':   {'form': '午後', 'reading': 'ごご', 'gloss': 'afternoon (p.m.) (on)'},
           'contrast_note': '午 only on=ご; in 午前/午後 only.'},
    '曜': {'standalone': {'form': '曜日', 'reading': 'ようび', 'gloss': 'day of week (on+on)'},
           'compound':   {'form': '日曜日', 'reading': 'にちようび', 'gloss': 'Sunday'},
           'contrast_note': '曜 only on=よう; appears only in day-of-week compounds.'},
    '番': {'standalone': {'form': '番', 'reading': 'ばん', 'gloss': 'turn / number (on)'},
           'compound':   {'form': '一番', 'reading': 'いちばん', 'gloss': 'number one / most (on+on)'},
           'contrast_note': '番 on=ばん standalone or suffix.'},
    '号': {'standalone': {'form': '号', 'reading': 'ごう', 'gloss': 'number / issue (on)'},
           'compound':   {'form': '番号', 'reading': 'ばんごう', 'gloss': 'number (on+on)'},
           'contrast_note': '号 only on=ごう; suffix for serial numbers.'},
    '足': {'standalone': {'form': '足', 'reading': 'あし', 'gloss': 'foot / leg (kun)'},
           'compound':   {'form': '足音', 'reading': 'あしおと', 'gloss': 'footstep sound (kun+kun)'},
           'contrast_note': '足 kun=あし, on=そく in compounds.'},
    '手': {'standalone': {'form': '手', 'reading': 'て', 'gloss': 'hand (kun)'},
           'compound':   {'form': '上手', 'reading': 'じょうず', 'gloss': 'skilled (irregular reading)'},
           'contrast_note': '手 kun=て standalone. Most common compound 上手/下手 use irregular reading.'},
    '目': {'standalone': {'form': '目', 'reading': 'め', 'gloss': 'eye (kun)'},
           'compound':   {'form': '一番目', 'reading': 'いちばんめ', 'gloss': 'first / number one (kun-suffix)'},
           'contrast_note': '目 kun=め standalone, also ordinal-suffix (1つ目, 2番目).'},
    '口': {'standalone': {'form': '口', 'reading': 'くち', 'gloss': 'mouth (kun)'},
           'compound':   {'form': '入口', 'reading': 'いりぐち', 'gloss': 'entrance (kun+kun)'},
           'contrast_note': '口 kun=くち, on=こう in compounds.'},
    '白': {'standalone': {'form': '白い', 'reading': 'しろい', 'gloss': 'white (kun-adj)'},
           'compound':   {'form': '白人', 'reading': 'はくじん', 'gloss': 'white person (on) — N4+'},
           'contrast_note': '白 kun=しろ/しろ-い (adj), on=はく/びゃく in compounds.'},
    '王': {'standalone': {'form': '王', 'reading': 'おう', 'gloss': 'king (on)'},
           'compound':   {'form': '国王', 'reading': 'こくおう', 'gloss': 'monarch (on+on)'},
           'contrast_note': '王 on=おう; mostly used standalone or in title compounds.'},
    '太': {'standalone': {'form': '太い', 'reading': 'ふとい', 'gloss': 'thick / fat (kun-adj)'},
           'compound':   {'form': '太陽', 'reading': 'たいよう', 'gloss': 'sun (on) — 陽 is N4'},
           'contrast_note': '太 kun=ふと-い (adj), on=たい in compounds.'},
    '犬': {'standalone': {'form': '犬', 'reading': 'いぬ', 'gloss': 'dog (kun)'},
           'compound':   {'form': '小犬', 'reading': 'こいぬ', 'gloss': 'puppy (kun+kun)'},
           'contrast_note': '犬 kun=いぬ standalone, on=けん in compounds (rare in N5).'},
    '末': {'standalone': {'form': '週末', 'reading': 'しゅうまつ', 'gloss': 'weekend (on)'},
           'compound':   {'form': '末', 'reading': 'すえ', 'gloss': 'end (kun)'},
           'contrast_note': '末 on=まつ in compounds, kun=すえ.'},
    '字': {'standalone': {'form': '字', 'reading': 'じ', 'gloss': 'character (on)'},
           'compound':   {'form': '漢字', 'reading': 'かんじ', 'gloss': 'kanji (on+on)'},
           'contrast_note': '字 only on=じ; very common in writing-related compounds.'},
    '語': {'standalone': {'form': '語', 'reading': 'ご', 'gloss': 'word (on; suffix-form)'},
           'compound':   {'form': '日本語', 'reading': 'にほんご', 'gloss': 'Japanese language (on)'},
           'contrast_note': '語 only on=ご; language-suffix marker.'},
}

okj_added = 0
for e in entries:
    g = e.get('glyph') or e.get('id','').split('.')[-1]
    if g in PAIRS and not e.get('on_kun_pair_drill'):
        e['on_kun_pair_drill'] = PAIRS[g]
        e['on_kun_pair_drill_provenance'] = 'llm_curated'
        okj_added += 1

print(f'  on_kun_pair_drill added: {okj_added}/{len(entries)}')

kanji_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final
total = len(entries)
n5c = sum(1 for e in entries if e.get('n5_compounds'))
okj = sum(1 for e in entries if e.get('on_kun_pair_drill'))
print()
print('=== FINAL ===')
print(f'  n5_compounds (NEW):       {n5c}/{total}')
print(f'  on_kun_pair_drill (NEW):  {okj}/{total}')
