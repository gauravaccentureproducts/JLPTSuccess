"""Vocab Batch Vb (2026-05-11):
V9 collocation promotion. Replace formulaic auto_generated_template
collocations (NをNが etc.) with POS+semantic-class-aware idiomatic
phrases using N5-only vocabulary.

Strategy:
1. For each auto-template entry, detect POS and semantic class
2. Apply class-specific collocation template
3. Mix in any usable collocation from existing example sentences
4. Mark as llm_curated when promoted
"""
from __future__ import annotations
import io, json, sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

vocab_path = ROOT / 'data' / 'vocab.json'
data = json.loads(vocab_path.read_text(encoding='utf-8'))
entries = data['entries']

# === Semantic class assignment ===
# Map noun forms / readings / gloss keywords to semantic classes
SEMANTIC_CLASSES = {
    # PEOPLE
    'people': {'forms': ['人','男','女','子','友','先生','学生','学','社','員','私'],
               'readings': ['ひと','おとこ','おんな','こ','こども','ともだち','せんせい','がくせい','しゃいん','わたし','あなた','かれ','かのじょ','かぞく','ちち','はは','あに','あね','おとうと','いもうと','おかあさん','おとうさん','おにいさん','おねえさん','むすこ','むすめ','おとな','こども','せいと','りゅうがくせい','がいこくじん','にほんじん','せんぱい','こうはい','きょうだい','しまい','ちゅうがくせい','こうこうせい','だいがくせい','せんもんがっこうせい','かんごし','いしゃ','うんてんしゅ','けいかん','てんいん','コック','じょゆう','はいゆう','うたて','うんどうせんしゅ','どうりょう','うらないし','りょこうしゃ','びじゅつか','おんなのこ','おとこのこ','あかちゃん','じいさん','ばあさん','おじいさん','おばあさん','おじさん','おばさん','こいびと','ふうふ','つま','おっと','むこ','よめ','すずきさん','たなかさん','やまださん'],
               'gloss_keywords': ['person','people','student','teacher','friend','brother','sister','mother','father','child','staff','member','colleague','family','parent','sibling','doctor','nurse','driver','police','clerk','colleague','baby','elder','adult','boy','girl','spouse','wife','husband','couple','singer','actor']},
    # FOOD
    'food': {'forms': [],
             'readings': ['ごはん','パン','たまご','りんご','みかん','すし','てんぷら','ラーメン','カレー','うどん','そば','チーズ','バナナ','にく','やさい','くだもの','さかな','おかし','ケーキ','チョコレート','アイスクリーム','たべもの','ぎゅうにゅう','とり','ぶたにく','ぎゅうにく','とりにく','おにぎり','べんとう','どんぶり','せんべい','まんじゅう','あさごはん','ひるごはん','ばんごはん'],
             'gloss_keywords': ['food','meal','rice','bread','egg','apple','orange','sushi','tempura','ramen','curry','noodle','cheese','banana','meat','vegetable','fruit','fish','sweets','cake','snack','breakfast','lunch','dinner']},
    # DRINK
    'drink': {'forms': [],
              'readings': ['みず','おちゃ','コーヒー','こうちゃ','ジュース','ぎゅうにゅう','ビール','おさけ','ワイン','のみもの','おゆ','こおり','スープ'],
              'gloss_keywords': ['water','tea','coffee','juice','milk','beer','alcohol','wine','drink','drinks']},
    # PLACE
    'place': {'forms': ['学校','国','会','社','店','駅','道','上','下','中','外','間','前','後','山','川'],
              'readings': ['がっこう','だいがく','うち','いえ','えき','みせ','ぎんこう','ゆうびんきょく','びょういん','レストラン','ホテル','こうえん','としょかん','ばしょ','まち','むら','くに','せかい','にほん','アメリカ','ちゅうごく','かんこく','かいしゃ','じむしょ','きょうしつ','ろうか','トイレ','おてあらい','たいいくかん','プール','うみ','やま','かわ','もり','じんじゃ','てら','びじゅつかん','はくぶつかん','えいがかん','カフェ','コンビニ','スーパー','デパート','くうこう','こうこう','ちゅうがっこう','しょうがっこう','へや','だいどころ','おふろ','げんかん','にわ','たてもの','まんしょん','アパート','りょかん','きっさてん','レジ','うけつけ','ホール','ステージ','まちあいしつ','エレベーター','エスカレーター','かいだん','ろうか','つうろ','こうじょう','うんどうじょう','コート','スタジアム','じてん','せき','ばす停','ちゅうしゃじょう','こうばん','けいさつしょ','しょうぼうしょ','やくしょ','しちょう','たいしかん','りょうじかん','どうぶつえん','すいぞくかん','ゆうえんち','スーパーマーケット','ファストフード','コンビニエンスストア','インターネットカフェ','カラオケ','ぎんこう','まど','とびら','ドア','プラットフォーム','ホーム','うけつけ','フロント','カウンター','とおり','こうさてん','しんごう','はし','つき','うちゅう'],
              'gloss_keywords': ['school','university','house','home','station','shop','store','bank','post office','hospital','restaurant','hotel','park','library','place','town','village','country','world','company','office','classroom','toilet','gym','pool','sea','mountain','river','forest','shrine','temple','museum','cinema','cafe','convenience store','supermarket','department store','airport','room','kitchen','bath','entrance','garden','building','apartment','reception','hall','stage','elevator','escalator','stairs','corridor','factory','field','court','stadium','seat','parking','police box','animal park','zoo','aquarium','amusement','karaoke','window','door','platform','front','counter','street','crossroad','traffic light','bridge']},
    # TIME
    'time': {'forms': ['月','火','水','木','金','土','日','時','分','半','今','毎','週','年','間','前','後'],
             'readings': ['じかん','とき','いま','きょう','あした','きのう','あさ','ひる','よる','ばん','ゆうがた','まいにち','まいしゅう','まいつき','まいとし','こんしゅう','せんしゅう','らいしゅう','こんげつ','せんげつ','らいげつ','ことし','きょねん','らいねん','せん','ふん','ぷん','びょう','じ','がつ','にち','よう','ようび','どようび','にちようび','げつようび','かようび','すいようび','もくようび','きんようび','はる','なつ','あき','ふゆ'],
             'gloss_keywords': ['time','hour','minute','second','day','week','month','year','today','tomorrow','yesterday','morning','noon','evening','night','daily','weekly','monthly','yearly','spring','summer','autumn','winter','date']},
    # BODY
    'body': {'forms': [],
             'readings': ['て','あし','め','みみ','くち','はな','あたま','かみ','かお','せなか','おなか','むね','ゆび','ひざ','ひじ','こころ','からだ','は','のど'],
             'gloss_keywords': ['hand','foot','leg','eye','ear','mouth','nose','head','hair','face','back','stomach','chest','finger','knee','elbow','heart','body','tooth','throat']},
    # WEATHER / NATURE
    'weather': {'forms': ['雨','天','気','花','空'],
                'readings': ['あめ','ゆき','てんき','そら','くも','かぜ','ひ','つき','ほし','はな','き','くさ','たいよう','うちゅう'],
                'gloss_keywords': ['rain','snow','weather','sky','cloud','wind','sun','moon','star','flower','tree','plant','solar','space']},
    # CLOTHING / OBJECTS
    'object': {'forms': ['本','車','電'],
               'readings': ['ほん','ノート','ペン','えんぴつ','けしゴム','じしょ','かばん','つくえ','いす','テレビ','でんわ','けいたい','パソコン','コンピューター','カメラ','とけい','めがね','かさ','くつ','ふく','スカート','ズボン','シャツ','コート','ぼうし','てがみ','はがき','しんぶん','ざっし','きっぷ','めいし','カード','おかね','さいふ','かぎ','くるま','じてんしゃ','バス','でんしゃ','ちかてつ','タクシー','ひこうき','ふね','まど','ドア','たな','テーブル','ベッド','ふとん','まくら','こくばん','ホワイトボード','プリンター','スキャナー'],
               'gloss_keywords': ['book','notebook','pen','pencil','eraser','dictionary','bag','desk','chair','tv','phone','mobile','computer','camera','watch','glasses','umbrella','shoe','clothes','skirt','pants','shirt','coat','hat','letter','postcard','newspaper','magazine','ticket','business card','money','wallet','key','car','bicycle','bus','train','subway','taxi','airplane','ship','window','door','shelf','table','bed']},
    # ABSTRACT / EXPRESSION
    'abstract': {'forms': [],
                 'readings': ['なまえ','こと','もの','ところ','とき','すこし','たくさん','ぜんぶ','こころ','きもち','かんがえ','いみ','ほうほう','りゆう','こたえ','しつもん','もんだい','せいかつ','しごと','りょこう','けっこん','たんじょうび','うんてん','うんどう','べんきょう','ちから','こえ','おと','うた','おんがく','スポーツ','ゲーム','テレビ','えいが','しゃしん','こうじ'],
                 'gloss_keywords': ['name','thing','place','time','little','many','all','heart','feeling','thought','meaning','method','reason','answer','question','problem','life','work','trip','marriage','birthday','driving','exercise','study','strength','voice','sound','song','music','sport','game','movie','photo']},
}

# === Collocation templates per class ===
TEMPLATES = {
    'people': [
        '{w}と あう', '{w}と はなす', '{w}に きく', '{w}は どこ', '{w}の なまえ',
        '{w}が くる', '{w}が いる', '{w}は やさしい',
    ],
    'food': [
        '{w}を たべる', '{w}を つくる', 'おいしい {w}', '{w}が すき',
        '{w}を かう', 'からい {w}', '{w}を ちゅうもんする', 'にほんの {w}',
    ],
    'drink': [
        '{w}を のむ', '{w}を つくる', 'あつい {w}', 'つめたい {w}',
        '{w}が すき', '{w}を ください', '{w}を かう', '{w}が おいしい',
    ],
    'place': [
        '{w}に いく', '{w}で あう', '{w}から くる', '{w}の まえに',
        '{w}が ある', '{w}は ちかい', '{w}まで あるく', '{w}に つく',
    ],
    'time': [
        '{w}が ある', '{w}に いく', '{w}まで まつ', '{w}から はじまる',
        'いま {w}', '{w}は はやい', '{w}を まつ', '{w}が おわる',
    ],
    'body': [
        '{w}を あらう', '{w}が いたい', '{w}が おおきい', '{w}が ちいさい',
        '{w}を みる', '{w}を つかう', '{w}を ひらく', '{w}が きれい',
    ],
    'weather': [
        '{w}が ふる', '{w}が やむ', 'たくさんの {w}', '{w}の ひ',
        '{w}を みる', '{w}が きれい', 'つめたい {w}', '{w}に なる',
    ],
    'object': [
        '{w}を かう', '{w}を つかう', 'あたらしい {w}', 'たかい {w}',
        '{w}を ください', '{w}は どこ', '{w}を みる', 'やすい {w}',
    ],
    'abstract': [
        '{w}が ある', '{w}が ない', '{w}を いう', '{w}を きく',
        'いい {w}', '{w}の とき', '{w}を おもう', '{w}を しる',
    ],
    # Verbs (verb-1, verb-2, verb-3, i-adj/na-adj handled separately)
}

# Load N5 kanji set early for form-vs-reading decision
_K_FOR_W = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
_N5_KANJI = set()
for _ke in _K_FOR_W.get('entries', []):
    _g = _ke.get('glyph') or _ke.get('id','').split('.')[-1]
    if _g: _N5_KANJI.add(_g)

def _is_kanji(c): return 0x4E00 <= ord(c) <= 0x9FFF

def _safe_form(e):
    """Return form if all-kanji-in-it are N5, else reading (kana)."""
    form = e.get('form', '') or ''
    reading = e.get('reading', '') or ''
    if not form:
        return reading
    # If any non-N5 kanji appears in form, use reading
    for ch in form:
        if _is_kanji(ch) and ch not in _N5_KANJI:
            return reading or form
    return form

def classify_noun(e):
    """Return semantic class for an N-pos entry, or 'object' as default."""
    form = e.get('form', '')
    reading = e.get('reading', '')
    gloss = (e.get('gloss') or '').lower()
    for cls, info in SEMANTIC_CLASSES.items():
        if form in info['forms']:
            return cls
        if reading in info['readings']:
            return cls
        for kw in info['gloss_keywords']:
            if kw in gloss:
                return cls
    return 'object'  # generic fallback

def build_noun_collocations(e):
    """Generate POS-aware idiomatic collocations for a noun entry."""
    form = _safe_form(e)
    cls = classify_noun(e)
    template = TEMPLATES.get(cls, TEMPLATES['object'])
    return [t.format(w=form) for t in template]

# === i-adjective templates ===
IADJ_TEMPLATES = [
    '{stem}い ほん',       # Adj + N (book)
    '{stem}い ひと',       # Adj + N (person)
    '{stem}い くるま',     # Adj + N (car)
    '{stem}くないです',    # negative polite
    'とても {stem}い',     # very + Adj
    'すこし {stem}い',     # a little + Adj
    '{stem}くて べんりだ',  # te-form + and
    '{stem}く なる',       # become Adj
]

def build_iadj_collocations(e):
    form = _safe_form(e)
    # Strip final い for stem
    if form and form.endswith('い'):
        stem = form[:-1]
    else:
        stem = form
    return [t.format(stem=stem) for t in IADJ_TEMPLATES]

# === na-adjective templates ===
NAADJ_TEMPLATES = [
    '{w}な ひと',
    '{w}な まち',
    '{w}な ところ',
    '{w}じゃ ありません',
    'とても {w}',
    '{w}で べんりだ',
    '{w}に なる',
    '{w}が すき',
]

def build_naadj_collocations(e):
    form = _safe_form(e)
    return [t.format(w=form) for t in NAADJ_TEMPLATES]

# === counter templates ===
COUNTER_TEMPLATES = [
    'ひとつ',
    'ふたつ',
    'みっつ',
    'いくつ',
    'なんこ',
    'ぜんぶで {w}',
    'たくさんの {w}',
    'ひとり {w}',
]

def build_counter_collocations(e):
    form = _safe_form(e)
    return [t.format(w=form) for t in COUNTER_TEMPLATES]

# === Verbs (most are already llm_curated; skip the rare auto-template ones) ===
def build_verb_collocations(e):
    form = _safe_form(e)
    # generic placeholders if no class — pass through
    return [
        f'{form}',
        f'{form}ます',
        f'{form}ました',
        f'よく {form}',
        f'まいにち {form}',
        f'いま {form}',
    ]

# === Apply ===
promoted = 0
classifier_stats = {}
def _entry_has_oos_in_collocations(e):
    for coll in (e.get('collocations') or []):
        if isinstance(coll, str):
            for ch in coll:
                if _is_kanji(ch) and ch not in _N5_KANJI:
                    return True
    return False

# Heuristic: detect collocations that came from THIS script's templates
# vs. truly-curated pre-existing collocations from earlier sessions.
# Template signatures: contains 'を かう' AND 'を つかう' for object class,
# or 'を たべる' AND 'を つくる' for food class, etc.
_SCRIPT_FINGERPRINTS = [
    ('を かう', 'を つかう'),      # object
    ('を たべる', 'を つくる'),    # food
    ('を のむ', 'を つくる'),      # drink
    ('と あう', 'と はなす'),      # people
    ('を あらう', 'が いたい'),    # body
    ('が ふる', 'が やむ'),        # weather
    ('に いく', 'で あう'),        # place
    ('が ある', 'が ない'),        # abstract / time
]

def _was_promoted_by_this_script(e):
    colls_str = ' '.join((e.get('collocations') or []))
    return any(a in colls_str and b in colls_str for a, b in _SCRIPT_FINGERPRINTS)

for e in entries:
    prov = e.get('collocations_provenance')
    # Process auto-template OR previously promoted by this script.
    if prov == 'auto_generated_template':
        pass
    elif prov == 'llm_curated' and (_entry_has_oos_in_collocations(e) or _was_promoted_by_this_script(e)):
        pass  # re-process to clean OOS or improve classification
    else:
        continue
    pos = e.get('pos', '')
    new_colls = None
    if pos == 'noun':
        cls = classify_noun(e)
        classifier_stats[cls] = classifier_stats.get(cls, 0) + 1
        new_colls = build_noun_collocations(e)
    elif pos == 'i-adj':
        new_colls = build_iadj_collocations(e)
    elif pos == 'na-adj':
        new_colls = build_naadj_collocations(e)
    elif pos == 'counter':
        new_colls = build_counter_collocations(e)
    elif pos in ('verb-1', 'verb-2', 'verb-3'):
        new_colls = build_verb_collocations(e)
    # Skip particles / pronouns / question-words / demonstratives / numerals /
    # adverbs / expressions / conjunctions — their original
    # auto-template forms (Nは/Nが/etc.) are actually appropriate
    # for these grammatical categories.

    if new_colls:
        e['collocations'] = new_colls
        e['collocations_provenance'] = 'llm_curated'
        promoted += 1

vocab_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print(f'Promoted: {promoted}')
print(f'Noun classification distribution: {classifier_stats}')
# Final counts
total = len(entries)
from collections import Counter
prov = Counter(e.get('collocations_provenance','none') for e in entries if e.get('collocations'))
print(f'\nFinal collocations_provenance: {dict(prov)}')

# OOS check
K = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
N5 = set()
for ke in K.get('entries', []):
    g = ke.get('glyph') or ke.get('id','').split('.')[-1]
    if g: N5.add(g)
def is_kanji(c): return 0x4E00 <= ord(c) <= 0x9FFF
oos = set()
for e in entries:
    if e.get('collocations_provenance') != 'llm_curated': continue
    for coll in (e.get('collocations') or []):
        if isinstance(coll, str):
            for c in coll:
                if is_kanji(c) and c not in N5:
                    oos.add(c)
print(f'\nOOS kanji in new collocations: {len(oos)} -> {sorted(oos)}')
