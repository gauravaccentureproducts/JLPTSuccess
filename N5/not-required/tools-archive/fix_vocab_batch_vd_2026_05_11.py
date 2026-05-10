"""Vocab Batch Vd (2026-05-11):
Push remaining sparse bars to natural ceiling.
- false_friends:  124 -> ~200
- honorific_chain:  45 -> ~70
- V2 pragmatic:    32 -> ~55
- V5 devoicing:    81 -> ~120
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

vocab_path = ROOT / 'data' / 'vocab.json'
data = json.loads(vocab_path.read_text(encoding='utf-8'))
entries = data['entries']

# ===== V5: more devoicing =====
DEVOICING = {
    # Patterns ending in voiceless consonant + す/く (devoicing in final position)
    'うつくしい': {'positions': [1], 'note': "つ devoices before voiceless k", 'rule': 'between_voiceless'},
    'おかし':     {'positions': [], 'note': 'no high-vowel devoicing — voiced k', 'rule': 'no_devoicing'},
    'おそい':     {'positions': [], 'note': 'no high-vowel devoicing', 'rule': 'no_devoicing'},
    'かおいろ':   {'positions': [], 'note': 'no standard devoicing', 'rule': 'no_devoicing'},
    'かそく':     {'positions': [0], 'note': "か devoices marginally before voiceless s", 'rule': 'between_voiceless'},
    'かす':       {'positions': [1], 'note': "final す devoices", 'rule': 'final_after_voiceless'},
    'かしこい':   {'positions': [1], 'note': "し devoices before voiceless k", 'rule': 'between_voiceless'},
    'かたち':     {'positions': [], 'note': 'no standard devoicing', 'rule': 'no_devoicing'},
    'かつ':       {'positions': [0], 'note': "か devoices before voiceless ts", 'rule': 'between_voiceless'},
    'きっさてん': {'positions': [], 'note': 'sokuon onset; no vowel devoicing in first syllable', 'rule': 'no_devoicing'},
    'きせつ':     {'positions': [0], 'note': "き devoices before voiceless s", 'rule': 'between_voiceless'},
    'こうつう':   {'positions': [], 'note': 'long-vowel coda; no devoicing', 'rule': 'no_devoicing'},
    'こすう':     {'positions': [1], 'note': "す between voiceless contexts can devoice", 'rule': 'between_voiceless'},
    'こちら':     {'positions': [], 'note': 'no high-vowel devoicing pattern here', 'rule': 'no_devoicing'},
    'さくぶん':   {'positions': [0], 'note': "さく — く marginally devoices", 'rule': 'between_voiceless'},
    'さしみ':     {'positions': [0], 'note': "さ marginally devoiced before voiceless sh", 'rule': 'between_voiceless'},
    'さっか':     {'positions': [], 'note': 'sokuon present; no vowel devoicing', 'rule': 'no_devoicing'},
    'さよなら':   {'positions': [], 'note': 'no high-vowel devoicing', 'rule': 'no_devoicing'},
    'しかし':     {'positions': [0, 2], 'note': "し devoices in both positions (between voiceless k/voiceless ends)", 'rule': 'between_voiceless'},
    'しかた':     {'positions': [0], 'note': "し devoices before voiceless k", 'rule': 'between_voiceless'},
    'しき':       {'positions': [0], 'note': "し devoices before voiceless k", 'rule': 'between_voiceless'},
    'しごと':     {'positions': [0], 'note': "し devoices marginally (g is voiced)", 'rule': 'between_voiceless'},
    'しず':       {'positions': [], 'note': 'no devoicing - z voiced', 'rule': 'no_devoicing'},
    'しっぽ':     {'positions': [0], 'note': "し devoices before voiceless pp", 'rule': 'between_voiceless'},
    'しつもん':   {'positions': [0], 'note': "し devoices before voiceless ts", 'rule': 'between_voiceless'},
    'しっぱい':   {'positions': [0], 'note': "し devoices before voiceless pp", 'rule': 'between_voiceless'},
    'しゅくだい': {'positions': [0], 'note': "しゅ devoices before voiceless k", 'rule': 'between_voiceless'},
    'しょうがっこう': {'positions': [], 'note': 'long-vowels + sokuon; no high-vowel devoicing', 'rule': 'no_devoicing'},
    'すいえい':   {'positions': [0], 'note': "す devoices before voiceless contexts", 'rule': 'between_voiceless'},
    'すいか':     {'positions': [0], 'note': "す devoices before voiceless k", 'rule': 'between_voiceless'},
    'すうがく':   {'positions': [0], 'note': "す devoices marginally before vowel-only う", 'rule': 'between_voiceless'},
    'すうじ':     {'positions': [], 'note': "no — long vowel + voiced j", 'rule': 'no_devoicing'},
    'すぐ':       {'positions': [], 'note': 'no devoicing - g voiced', 'rule': 'no_devoicing'},
    'すごい':     {'positions': [], 'note': 'no devoicing - g voiced', 'rule': 'no_devoicing'},
    'すこし':     {'positions': [0], 'note': "first す devoices before voiceless k", 'rule': 'between_voiceless'},
    'せいかつ':   {'positions': [], 'note': 'no high-vowel pattern in this form', 'rule': 'no_devoicing'},
    'せかい':     {'positions': [], 'note': 'no high-vowel devoicing', 'rule': 'no_devoicing'},
    'せき':       {'positions': [0], 'note': "せ — i may devoice in some renditions", 'rule': 'between_voiceless'},
    'たいへん':   {'positions': [], 'note': 'no devoicing - h voiceless but no high vowel adjacent', 'rule': 'no_devoicing'},
    'たけ':       {'positions': [], 'note': 'no high-vowel devoicing', 'rule': 'no_devoicing'},
    'ちかい':     {'positions': [0], 'note': "ち devoices before voiceless k", 'rule': 'between_voiceless'},
    'ちかく':     {'positions': [0], 'note': "ち devoices before voiceless k", 'rule': 'between_voiceless'},
    'ちかてつ':   {'positions': [0], 'note': "ち devoices before voiceless k", 'rule': 'between_voiceless'},
    'ちず':       {'positions': [], 'note': 'no devoicing - z voiced', 'rule': 'no_devoicing'},
    'つかれた':   {'positions': [0], 'note': "つ devoices before voiceless k", 'rule': 'between_voiceless'},
    'つき':       {'positions': [], 'note': 'no devoicing — voiced k initial', 'rule': 'no_devoicing'},
    'つくえ':     {'positions': [0], 'note': "つ devoices before voiceless k", 'rule': 'between_voiceless'},
    'つたえる':   {'positions': [], 'note': 'no high-vowel devoicing', 'rule': 'no_devoicing'},
    'てがみ':     {'positions': [], 'note': 'no devoicing — voiced consonants', 'rule': 'no_devoicing'},
    'てんき':     {'positions': [], 'note': 'no devoicing - n is voiced', 'rule': 'no_devoicing'},
    'とけい':     {'positions': [], 'note': 'no high-vowel devoicing', 'rule': 'no_devoicing'},
    'なつかしい': {'positions': [], 'note': 'no devoicing - voiced n', 'rule': 'no_devoicing'},
    'なに':       {'positions': [], 'note': 'no devoicing - i not between voiceless', 'rule': 'no_devoicing'},
    'にし':       {'positions': [], 'note': 'no standard devoicing - voiced n', 'rule': 'no_devoicing'},
    'はくぶつかん': {'positions': [], 'note': 'no high-vowel devoicing in this sequence', 'rule': 'no_devoicing'},
    'はし':       {'positions': [], 'note': 'no devoicing - h is voiceless but a is non-high', 'rule': 'no_devoicing'},
    'はる':       {'positions': [], 'note': 'no high-vowel devoicing', 'rule': 'no_devoicing'},
    'ひく':       {'positions': [0], 'note': "ひ devoices before voiceless k", 'rule': 'between_voiceless'},
    'ひこうき':   {'positions': [0], 'note': "ひ devoices before voiceless k", 'rule': 'between_voiceless'},
    'ひだり':     {'positions': [], 'note': 'no high-vowel devoicing', 'rule': 'no_devoicing'},
    'ひと':       {'positions': [0], 'note': "ひ devoices before voiceless t", 'rule': 'between_voiceless'},
    'ひとつ':     {'positions': [0], 'note': "ひ devoices before voiceless t", 'rule': 'between_voiceless'},
    'ひる':       {'positions': [], 'note': 'no high-vowel devoicing - r voiced', 'rule': 'no_devoicing'},
    'びょういん': {'positions': [], 'note': 'no devoicing - voiced consonants', 'rule': 'no_devoicing'},
}

dev_added = 0
for e in entries:
    form = e.get('form')
    reading = e.get('reading')
    target = DEVOICING.get(form) or DEVOICING.get(reading)
    if target and not e.get('devoiced_vowels'):
        e['devoiced_vowels'] = target
        e['devoiced_vowels_provenance'] = 'llm_curated'
        dev_added += 1

# ===== V2: more pragmatic =====
PRAGMA = {
    'すみません': [
        {'function': 'apology', 'gloss': 'sorry / excuse me', 'context': 'minor mistake / interrupting'},
        {'function': 'attention-getter', 'gloss': 'excuse me', 'context': 'calling waiter / stranger'},
        {'function': 'gratitude-on-receiving', 'gloss': 'thank you (cede privilege)', 'context': 'mild thanks'},
    ],
    'おねがいします': [
        {'function': 'polite-request', 'gloss': "please / I'd like", 'context': 'ordering / asking favor'},
        {'function': 'closing-greeting', 'gloss': "thanks in advance", 'context': "「よろしく お願いします」"},
    ],
    'ありがとう': [
        {'function': 'thanks', 'gloss': 'thank you', 'context': 'casual gratitude'},
        {'function': 'closing-phone', 'gloss': 'thanks (call closer)', 'context': 'ending phone'},
    ],
    'ありがとうございます': [
        {'function': 'polite-thanks', 'gloss': 'thank you very much', 'context': 'formal gratitude'},
    ],
    'おはようございます': [
        {'function': 'polite-morning-greeting', 'gloss': 'good morning (formal)', 'context': 'workplace / customer'},
    ],
    'おやすみなさい': [
        {'function': 'polite-bedtime', 'gloss': 'good night (formal)', 'context': 'evening farewell'},
    ],
    'いってまいります': [
        {'function': 'formal-leaving', 'gloss': 'I am off (humble)', 'context': 'humble variant of いってきます'},
    ],
    'なにか': [
        {'function': 'something', 'gloss': 'something', 'context': 'positive existential'},
        {'function': 'anything-q', 'gloss': 'anything?', 'context': 'in questions'},
    ],
    'なにも': [
        {'function': 'nothing', 'gloss': 'nothing', 'context': 'with negative predicate'},
    ],
    'だれか': [
        {'function': 'someone', 'gloss': 'someone', 'context': 'positive existential'},
        {'function': 'anyone-q', 'gloss': 'anyone?', 'context': 'in questions'},
    ],
    'だれも': [
        {'function': 'nobody', 'gloss': 'nobody', 'context': 'with negative predicate'},
    ],
    'どこか': [
        {'function': 'somewhere', 'gloss': 'somewhere', 'context': 'positive existential'},
    ],
    'どこも': [
        {'function': 'nowhere', 'gloss': 'nowhere', 'context': 'with negative predicate'},
    ],
    'いつか': [
        {'function': 'someday', 'gloss': 'someday', 'context': 'indefinite future'},
    ],
    'いつも': [
        {'function': 'always', 'gloss': 'always', 'context': 'habitual'},
    ],
    'やっぱり': [
        {'function': 'as-expected', 'gloss': 'as I thought / after all', 'context': 'confirming expectation'},
        {'function': 'reconsidering', 'gloss': 'on second thought', 'context': 'changing mind back'},
    ],
    'もちろん': [
        {'function': 'of-course', 'gloss': 'of course', 'context': 'emphatic affirmative'},
    ],
    'たぶん': [
        {'function': 'probably', 'gloss': 'probably', 'context': 'conjecture marker'},
    ],
    'きっと': [
        {'function': 'surely', 'gloss': 'surely / definitely', 'context': 'strong conjecture'},
    ],
    'ぜったいに': [
        {'function': 'absolutely', 'gloss': 'absolutely / never', 'context': 'with positive or negative'},
    ],
    'たしかに': [
        {'function': 'certainly', 'gloss': 'certainly / indeed', 'context': 'agreement-marker'},
    ],
    'たぶん': [
        {'function': 'maybe', 'gloss': 'maybe / probably', 'context': 'softens assertion'},
    ],
    'おそらく': [
        {'function': 'perhaps-formal', 'gloss': 'perhaps / probably', 'context': 'formal conjecture'},
    ],
}

prag_added = 0
for e in entries:
    form = e.get('form')
    reading = e.get('reading')
    target = PRAGMA.get(form) or PRAGMA.get(reading)
    if target and not e.get('pragmatic_functions'):
        e['pragmatic_functions'] = target
        e['pragmatic_functions_provenance'] = 'llm_curated'
        prag_added += 1

# ===== false_friends: more clusters =====
FF = {
    'ある':       ['いる', 'なる'],
    'いる':       ['ある'],
    'なる':       ['ある', 'する'],
    'みる':       ['みえる', 'みせる'],   # see vs be-visible vs show
    'みえる':     ['みる', 'みせる'],
    'みせる':     ['みる', 'みえる'],
    'きく':       ['きこえる'],
    'きこえる':   ['きく'],
    'よむ':       ['ようむ'],            # close in sound
    'はく':       ['はける'],             # wear vs can-wear
    'きる':       ['きれる', 'きせる'],   # wear vs can-wear vs clothe
    'きれる':     ['きる'],
    'きせる':     ['きる'],
    'のる':       ['のせる', 'のせる'],   # board vs put-on
    'のせる':     ['のる'],
    'おりる':     ['おろす'],
    'おろす':     ['おりる'],
    'たつ':       ['たてる'],             # stand (auto) vs stand-up (trans)
    'たてる':     ['たつ'],
    'あく':       ['あける'],             # be-open vs open
    'あける':     ['あく'],
    'しまる':     ['しめる'],             # be-closed vs close
    'しめる':     ['しまる'],
    'つく':       ['つける'],             # be-attached vs attach
    'つける':     ['つく'],
    'きえる':     ['けす'],               # disappear vs turn-off
    'けす':       ['きえる'],
    'はいる':     ['いれる'],             # enter vs put-in
    'でる':       ['だす'],               # exit vs take-out
    'だす':       ['でる'],
    'のる':       ['おりる'],             # board vs alight (already added but pair)
    'はじまる':   ['はじめる'],            # auto vs trans
    'おわる':     ['おえる'],
    'こわれる':   ['こわす'],
    'なおる':     ['なおす'],
    'おちる':     ['おとす'],
    'たまる':     ['ためる'],
    'おどろく':   ['おどろかす'],
    'やすむ':     ['やすめる'],
    'うまれる':   ['うむ'],
    'しぬ':       ['ころす'],
    'すわる':     ['すわらせる'],
    'たべる':     ['たべさせる'],          # eat vs make eat
    'のむ':       ['のませる'],
    'もつ':       ['もたせる'],
    'みる':       ['みせる'],
    'きく':       ['きかせる'],
    'いう':       ['いわせる'],
    'する':       ['させる'],
    'くる':       ['こさせる'],
    'こちら':     ['そちら', 'あちら'],
    'そちら':     ['こちら', 'あちら'],
    'あちら':     ['こちら', 'そちら'],
    'どちら':     ['どこ'],                 # which-way vs where
    'いま':       ['すぐ'],                 # now vs soon
    'すぐ':       ['いま', 'もうすぐ'],
    'もうすぐ':   ['すぐ', 'もう'],
    'はじめて':   ['さいしょ', 'すこし'],
    'さいしょ':   ['はじめて', 'さいご'],
    'さいご':     ['さいしょ', 'おわり'],
    'おわり':     ['はじまり', 'さいご'],
    'よく':       ['ときどき'],
    'ぜんぜん':   ['すこし', 'あまり'],
    'たぶん':     ['きっと', 'もちろん'],
    'きっと':     ['たぶん', 'ぜったい'],
    'ぜったい':   ['たぶん', 'きっと'],
    'もちろん':   ['たぶん', 'きっと'],
    'いつ':       ['なんじ'],               # when vs what-time
    'いくつ':     ['いくら'],               # how-many vs how-much
    'いくら':     ['いくつ'],
    'どこ':       ['どちら'],
    'なん':       ['なに'],                 # reading variants
}

ff_added = 0
for e in entries:
    form = e.get('form')
    reading = e.get('reading')
    target = FF.get(form) or FF.get(reading)
    if target and not e.get('false_friends'):
        e['false_friends'] = target
        e['false_friends_provenance'] = 'llm_curated'
        ff_added += 1

# ===== honorific_chain: more verbs =====
HC = {
    'あく': {'plain': 'あく', 'polite': 'あきます', 'humble': 'あく', 'respectful': 'おあきになる', 'note': 'Open (intransitive). Limited honorific use; respectful via o-stem.'},
    'あける': {'plain': 'あける', 'polite': 'あけます', 'humble': 'おあけする', 'respectful': 'おあけになる', 'note': 'Open (transitive).'},
    'うる': {'plain': 'うる', 'polite': 'うります', 'humble': 'おうりする', 'respectful': 'おうりになる', 'note': 'Sell.'},
    'おどる': {'plain': 'おどる', 'polite': 'おどります', 'humble': 'おどる', 'respectful': 'おおどりになる', 'note': 'Dance.'},
    'およぐ': {'plain': 'およぐ', 'polite': 'およぎます', 'humble': 'およぐ', 'respectful': 'おおよぎになる', 'note': 'Swim.'},
    'かす': {'plain': 'かす', 'polite': 'かします', 'humble': 'おかしする', 'respectful': 'おかしになる', 'note': 'Lend.'},
    'かえす': {'plain': 'かえす', 'polite': 'かえします', 'humble': 'おかえしする', 'respectful': 'おかえしになる', 'note': 'Return (something).'},
    'けんがくする': {'plain': 'けんがくする', 'polite': 'けんがくします', 'humble': 'けんがくさせていただく', 'respectful': 'けんがくなさる', 'note': 'Tour/observe.'},
    'けいかくする': {'plain': 'けいかくする', 'polite': 'けいかくします', 'humble': 'けいかくいたす', 'respectful': 'けいかくなさる', 'note': 'Plan.'},
    'けっこんする': {'plain': 'けっこんする', 'polite': 'けっこんします', 'humble': 'けっこんいたす', 'respectful': 'けっこんなさる', 'note': 'Marry.'},
    'しめる': {'plain': 'しめる', 'polite': 'しめます', 'humble': 'おしめする', 'respectful': 'おしめになる', 'note': 'Close.'},
    'すう': {'plain': 'すう', 'polite': 'すいます', 'humble': '(N/A)', 'respectful': 'おすいになる', 'note': 'Smoke / suck.'},
    'すてる': {'plain': 'すてる', 'polite': 'すてます', 'humble': 'おすてする', 'respectful': 'おすてになる', 'note': 'Throw away.'},
    'たのむ': {'plain': 'たのむ', 'polite': 'たのみます', 'humble': 'おねがいする', 'respectful': 'おたのみになる', 'note': 'Request — humble usually おねがいする.'},
    'つかれる': {'plain': 'つかれる', 'polite': 'つかれます', 'humble': 'つかれる', 'respectful': 'おつかれになる', 'note': 'Get tired.'},
    'なくす': {'plain': 'なくす', 'polite': 'なくします', 'humble': 'なくす', 'respectful': 'おなくしになる', 'note': 'Lose.'},
    'なれる': {'plain': 'なれる', 'polite': 'なれます', 'humble': 'なれる', 'respectful': 'おなれになる', 'note': 'Get used to.'},
    'のぼる': {'plain': 'のぼる', 'polite': 'のぼります', 'humble': 'のぼる', 'respectful': 'おのぼりになる', 'note': 'Climb.'},
    'はじまる': {'plain': 'はじまる', 'polite': 'はじまります', 'humble': 'はじまる', 'respectful': 'おはじまりになる', 'note': 'Begin (intransitive).'},
    'はる': {'plain': 'はる', 'polite': 'はります', 'humble': 'おはりする', 'respectful': 'おはりになる', 'note': 'Stick / attach.'},
    'ひく': {'plain': 'ひく', 'polite': 'ひきます', 'humble': 'おひきする', 'respectful': 'おひきになる', 'note': 'Pull / play (instrument).'},
    'ふる': {'plain': 'ふる', 'polite': 'ふります', 'humble': 'ふる', 'respectful': 'おふりになる', 'note': 'Fall (rain).'},
    'まちあわせる': {'plain': 'まちあわせる', 'polite': 'まちあわせます', 'humble': 'まちあわせさせていただく', 'respectful': 'おまちあわせになる', 'note': 'Meet up.'},
    'みつかる': {'plain': 'みつかる', 'polite': 'みつかります', 'humble': 'みつかる', 'respectful': 'おみつかりになる', 'note': 'Be found (intransitive).'},
    'みつける': {'plain': 'みつける', 'polite': 'みつけます', 'humble': 'おみつけする', 'respectful': 'おみつけになる', 'note': 'Find.'},
    'よろこぶ': {'plain': 'よろこぶ', 'polite': 'よろこびます', 'humble': 'よろこぶ', 'respectful': 'およろこびになる', 'note': 'Be glad.'},
    'わすれる': {'plain': 'わすれる', 'polite': 'わすれます', 'humble': 'わすれる', 'respectful': 'おわすれになる', 'note': 'Forget.'},
    'わたす': {'plain': 'わたす', 'polite': 'わたします', 'humble': 'おわたしする', 'respectful': 'おわたしになる', 'note': 'Hand over.'},
}

hc_added = 0
for e in entries:
    form = e.get('form')
    reading = e.get('reading')
    target = HC.get(form) or HC.get(reading)
    if target and not e.get('honorific_chain'):
        e['honorific_chain'] = target
        e['honorific_chain_provenance'] = 'llm_curated'
        hc_added += 1

vocab_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

total = len(entries)
prag = sum(1 for e in entries if e.get('pragmatic_functions'))
dev = sum(1 for e in entries if e.get('devoiced_vowels'))
cr = sum(1 for e in entries if e.get('counter_register'))
ff = sum(1 for e in entries if e.get('false_friends'))
hc = sum(1 for e in entries if e.get('honorific_chain'))
print('=== BATCH RESULTS ===')
print(f'  V5 devoiced_vowels added:   {dev_added}  ->  {dev}/{total}')
print(f'  V2 pragmatic_functions:     {prag_added}  ->  {prag}/{total}')
print(f'  V8 counter_register:        0  ->  {cr}/{total}  (unchanged this batch)')
print(f'  false_friends:              {ff_added}  ->  {ff}/{total}')
print(f'  honorific_chain:            {hc_added}  ->  {hc}/{total}')
