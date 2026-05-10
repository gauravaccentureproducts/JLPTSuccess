"""Vocab Batch Va (2026-05-11):
Combined sparse-bar expansion:
- V5 devoiced_vowels: 35 -> ~100
- V2 pragmatic_functions: 13 -> ~50
- V8 counter_register: 4 -> ~30
- false_friends: 18 -> ~80
- honorific_chain: 9 -> ~35
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

# ===== V5: devoiced_vowels expansion =====
DEVOICING = {
    # Already had 35; add ~65 more for ~100 total
    'いく':       {'positions': [0], 'note': "い devoices between voiceless i+k", 'rule': 'between_voiceless'},
    'いそぐ':     {'positions': [0], 'note': "い devoices before voiceless s", 'rule': 'between_voiceless'},
    'いす':       {'positions': [0], 'note': "い devoices before voiceless s", 'rule': 'between_voiceless'},
    'いち':       {'positions': [0], 'note': "い marginally devoiced before ch", 'rule': 'between_voiceless'},
    'いつ':       {'positions': [0], 'note': "い devoices before voiceless ts", 'rule': 'between_voiceless'},
    'うし':       {'positions': [0], 'note': "う devoices before voiceless sh", 'rule': 'between_voiceless'},
    'うた':       {'positions': [0], 'note': "う devoices before voiceless t", 'rule': 'between_voiceless'},
    'おかし':     {'positions': [], 'note': 'no devoicing - all voiced consonants', 'rule': 'no_devoicing'},
    'かつ':       {'positions': [0], 'note': "か devoices before voiceless ts", 'rule': 'between_voiceless'},
    'きく':       {'positions': [0], 'note': "き devoices between k+k", 'rule': 'between_voiceless'},
    'きせつ':     {'positions': [0], 'note': "き devoices before voiceless s", 'rule': 'between_voiceless'},
    'きた':       {'positions': [0], 'note': "き devoices before voiceless t", 'rule': 'between_voiceless'},
    'きって':     {'positions': [0], 'note': "き devoices before voiceless tt", 'rule': 'between_voiceless'},
    'きっぷ':     {'positions': [0], 'note': "き devoices before voiceless pp", 'rule': 'between_voiceless'},
    'きそく':     {'positions': [0], 'note': "き devoices before voiceless s", 'rule': 'between_voiceless'},
    'きかい':     {'positions': [0], 'note': "き devoices before voiceless k", 'rule': 'between_voiceless'},
    'くち':       {'positions': [0], 'note': "く devoices before voiceless ch", 'rule': 'between_voiceless'},
    'くさい':     {'positions': [0], 'note': "く devoices before voiceless s", 'rule': 'between_voiceless'},
    'くつ':       {'positions': [0], 'note': "く devoices before voiceless ts", 'rule': 'between_voiceless'},
    'くだもの':   {'positions': [], 'note': 'no standard devoicing (voiced d)', 'rule': 'no_devoicing'},
    'くち':       {'positions': [0], 'note': "く devoices before voiceless ch", 'rule': 'between_voiceless'},
    'こうつう':   {'positions': [1], 'note': "う in こう devoices in coda", 'rule': 'long_vowel_coda'},
    'さく':       {'positions': [1], 'note': "く final devoices", 'rule': 'final_after_voiceless'},
    'しか':       {'positions': [0], 'note': "し devoices before voiceless k", 'rule': 'between_voiceless'},
    'しご':       {'positions': [0], 'note': "し devoices before voiced g (variable)", 'rule': 'between_voiceless'},
    'した':       {'positions': [0], 'note': "first し devoices to sht'", 'rule': 'between_voiceless'},
    'しち':       {'positions': [0], 'note': "し devoices before voiceless ch", 'rule': 'between_voiceless'},
    'しっぱい':   {'positions': [0], 'note': "し devoices before voiceless pp", 'rule': 'between_voiceless'},
    'しつ':       {'positions': [0], 'note': "し devoices before voiceless ts", 'rule': 'between_voiceless'},
    'しゅくだい': {'positions': [0], 'note': "しゅ devoices before voiceless k", 'rule': 'between_voiceless'},
    'しゅみ':     {'positions': [0], 'note': "しゅ marginally devoiced", 'rule': 'between_voiceless'},
    'すいか':     {'positions': [0], 'note': "す devoices before voiceless k", 'rule': 'between_voiceless'},
    'すき':       {'positions': [0], 'note': "す devoices before voiceless k", 'rule': 'between_voiceless'},
    'すこし':     {'positions': [0], 'note': "first す devoices before voiceless k", 'rule': 'between_voiceless'},
    'すし':       {'positions': [0], 'note': "first す devoices before voiceless sh", 'rule': 'between_voiceless'},
    'すずしい':   {'positions': [0], 'note': "first す devoices before voiceless す/ず", 'rule': 'between_voiceless'},
    'すてき':     {'positions': [0], 'note': "す devoices before voiceless t", 'rule': 'between_voiceless'},
    'たかい':     {'positions': [], 'note': 'no devoicing — a/i are non-high vowels here', 'rule': 'no_devoicing'},
    'たてもの':   {'positions': [], 'note': 'no devoicing in this form', 'rule': 'no_devoicing'},
    'ちかく':     {'positions': [0], 'note': "ち devoices before voiceless k", 'rule': 'between_voiceless'},
    'ちかい':     {'positions': [0], 'note': "ち devoices before voiceless k", 'rule': 'between_voiceless'},
    'ちかてつ':   {'positions': [0], 'note': "ち devoices before voiceless k", 'rule': 'between_voiceless'},
    'ちず':       {'positions': [0], 'note': "ち devoices before voiceless s", 'rule': 'between_voiceless'},
    'つかう':     {'positions': [0], 'note': "つ devoices before voiceless k", 'rule': 'between_voiceless'},
    'つくえ':     {'positions': [0], 'note': "つ devoices before voiceless k", 'rule': 'between_voiceless'},
    'つくる':     {'positions': [0], 'note': "つ devoices before voiceless k", 'rule': 'between_voiceless'},
    'なつ':       {'positions': [1], 'note': "final つ devoices", 'rule': 'final_after_voiceless'},
    'はち':       {'positions': [0], 'note': "は often shortened/devoiced before ch", 'rule': 'between_voiceless'},
    'はちじ':     {'positions': [0], 'note': "は devoices before voiceless ch", 'rule': 'between_voiceless'},
    'ひこうき':   {'positions': [0], 'note': "ひ devoices before voiceless k", 'rule': 'between_voiceless'},
    'ひと':       {'positions': [0], 'note': "ひ devoices before voiceless t", 'rule': 'between_voiceless'},
    'ひとつ':     {'positions': [0], 'note': "ひ devoices before voiceless t", 'rule': 'between_voiceless'},
    'ひとり':     {'positions': [0], 'note': "ひ devoices before voiceless t", 'rule': 'between_voiceless'},
    'ふく':       {'positions': [0], 'note': "ふ devoices before voiceless k", 'rule': 'between_voiceless'},
    'ふたつ':     {'positions': [0], 'note': "ふ devoices before voiceless t", 'rule': 'between_voiceless'},
    'ふたり':     {'positions': [0], 'note': "ふ devoices before voiceless t", 'rule': 'between_voiceless'},
    'ふつう':     {'positions': [0], 'note': "ふ devoices before voiceless ts", 'rule': 'between_voiceless'},
    'まつ':       {'positions': [1], 'note': "final つ devoices", 'rule': 'final_after_voiceless'},
    'みち':       {'positions': [], 'note': 'no standard devoicing — voiced m', 'rule': 'no_devoicing'},
    'もつ':       {'positions': [1], 'note': "final つ devoices", 'rule': 'final_after_voiceless'},
    'やすい':     {'positions': [1], 'note': "す between voiceless contexts can devoice", 'rule': 'between_voiceless'},
    'やすみ':     {'positions': [1], 'note': "す devoices in some renditions", 'rule': 'between_voiceless'},
    'りつ':       {'positions': [1], 'note': "final つ devoices", 'rule': 'final_after_voiceless'},
    'いっしょ':   {'positions': [], 'note': 'sokuon-initial; no vowel devoicing', 'rule': 'no_devoicing'},
    'いっぱい':   {'positions': [], 'note': 'sokuon present; no vowel devoicing', 'rule': 'no_devoicing'},
    'もうふ':     {'positions': [], 'note': 'no standard devoicing', 'rule': 'no_devoicing'},
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

# ===== V2: pragmatic_functions expansion =====
PRAGMA = {
    'いえ':      [  # (no, casual)
        {'function': 'casual-negation', 'gloss': 'no / nope', 'context': 'informal disagreement'},
        {'function': 'mild-refusal', 'gloss': 'nah / not really', 'context': 'softening a refusal'},
    ],
    'はい':      [
        {'function': 'affirmative', 'gloss': 'yes', 'context': 'standard yes'},
        {'function': 'aizuchi', 'gloss': 'I see / mhm', 'context': 'back-channel'},
        {'function': 'attention-confirmation', 'gloss': 'present / here', 'context': 'roll call'},
        {'function': 'handing-over', 'gloss': 'here you go', 'context': '「はい、これ」'},
    ],
    'もしもし':  [
        {'function': 'phone-greeting', 'gloss': 'hello (phone)', 'context': 'opening phone call'},
        {'function': 'attention-getting', 'gloss': 'hey / excuse me', 'context': 'getting attention'},
    ],
    'ちょっと':  [
        {'function': 'a-little', 'gloss': 'a little', 'context': 'quantity'},
        {'function': 'pragmatic-softener', 'gloss': '...well... / hmm', 'context': 'declining politely'},
        {'function': 'attention-getter', 'gloss': 'excuse me / hey', 'context': 'casual call'},
    ],
    'まあ':      [
        {'function': 'mild-affirm', 'gloss': 'well / sort of', 'context': 'hedged agreement'},
        {'function': 'soothing', 'gloss': 'well now / there there', 'context': 'calming someone'},
        {'function': 'exclamation', 'gloss': 'oh my / wow', 'context': 'surprise (female-coded)'},
    ],
    'なるほど':  [
        {'function': 'understanding', 'gloss': 'I see / indeed', 'context': 'comprehension marker'},
        {'function': 'agreement-acknowledging', 'gloss': 'you have a point', 'context': 'acknowledging argument'},
    ],
    'いただきます': [
        {'function': 'pre-meal-ritual', 'gloss': 'thanks for the meal', 'context': 'said before eating'},
        {'function': 'humble-receive', 'gloss': 'I humbly receive', 'context': 'when given a gift'},
    ],
    'ごちそうさま': [
        {'function': 'post-meal-ritual', 'gloss': 'thanks for the meal', 'context': 'said after eating'},
        {'function': 'declining-future-meal', 'gloss': 'no more thanks', 'context': 'declining seconds'},
    ],
    'おはよう':  [
        {'function': 'morning-greeting', 'gloss': 'good morning', 'context': 'casual / before noon'},
        {'function': 'first-encounter-greeting', 'gloss': 'first hello of the day', 'context': 'workplace (any time)'},
    ],
    'こんにちは': [
        {'function': 'day-greeting', 'gloss': 'hello / good afternoon', 'context': 'midday to evening'},
        {'function': 'general-greeting', 'gloss': 'hi', 'context': 'opening encounters'},
    ],
    'こんばんは': [
        {'function': 'evening-greeting', 'gloss': 'good evening', 'context': 'after dusk'},
    ],
    'さようなら': [
        {'function': 'formal-farewell', 'gloss': 'goodbye', 'context': 'formal parting'},
        {'function': 'final-parting', 'gloss': 'farewell', 'context': 'sense of finality (parents often avoid with children)'},
    ],
    'おやすみ':  [
        {'function': 'bedtime-greeting', 'gloss': 'good night', 'context': 'parting before sleep'},
        {'function': 'breaks', 'gloss': 'rest / break', 'context': 'noun: holiday/break'},
    ],
    'おめでとう': [
        {'function': 'congratulations', 'gloss': 'congratulations', 'context': 'birthday, wedding, achievement'},
        {'function': 'happy-event-marker', 'gloss': 'happy X', 'context': '誕生日おめでとう / 明けまして〜'},
    ],
    'がんばって': [
        {'function': 'encouragement', 'gloss': 'do your best / good luck', 'context': 'sending off into challenge'},
        {'function': 'cheer', 'gloss': 'go for it', 'context': 'sports/exam support'},
    ],
    'なんで':    [
        {'function': 'why-casual', 'gloss': 'why', 'context': 'casual reason-question'},
        {'function': 'how-means', 'gloss': 'by what means', 'context': 'ambiguous — disambiguate with どうやって'},
    ],
    'ほら':      [
        {'function': 'attention-getter', 'gloss': 'look / see', 'context': 'pointing out something'},
        {'function': 'i-told-you-so', 'gloss': 'see, told you', 'context': 'mild reproach'},
    ],
    'ね':        [
        {'function': 'agreement-seeking', 'gloss': 'right?', 'context': 'sentence-final'},
        {'function': 'topic-checker', 'gloss': 'hey... / so...', 'context': 'sentence-initial'},
    ],
    'よ':        [
        {'function': 'assertion-marker', 'gloss': 'you know', 'context': 'informing listener of new info'},
        {'function': 'mild-warning', 'gloss': 'be careful', 'context': 'cautioning context'},
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

# ===== V8: counter_register expansion =====
COUNTER_REG = {
    # General object counter
    'いっこ':   {'counter': 'こ',     'irregular': False, 'note': '1-thing (small object); generic counter こ.',  'register_pair': {'casual_alt': 'ひとつ', 'formal_same': '一個 (いっこ)'}},
    'にこ':     {'counter': 'こ',     'irregular': False, 'note': '2-objects こ counter.',                       'register_pair': {'casual_alt': 'ふたつ', 'formal_same': '二個 (にこ)'}},
    'みっつ':   {'counter': 'つ',     'irregular': True,  'note': '3-things; kun-stem mit-tsu (1-10 are kun).',  'register_pair': {'casual_alt': 'みっつ', 'formal_same': '三個 (さんこ)'}},
    'よっつ':   {'counter': 'つ',     'irregular': True,  'note': '4-things; kun-stem yot-tsu.',                 'register_pair': {'casual_alt': 'よっつ', 'formal_same': '四個 (よんこ)'}},
    'いつつ':   {'counter': 'つ',     'irregular': True,  'note': '5-things; kun-stem itsu-tsu.',                'register_pair': {'casual_alt': 'いつつ', 'formal_same': '五個 (ごこ)'}},
    'むっつ':   {'counter': 'つ',     'irregular': True,  'note': '6-things; kun-stem mut-tsu.',                 'register_pair': {'casual_alt': 'むっつ', 'formal_same': '六個 (ろっこ)'}},
    'ななつ':   {'counter': 'つ',     'irregular': True,  'note': '7-things; kun-stem nana-tsu.',                'register_pair': {'casual_alt': 'ななつ', 'formal_same': '七個 (ななこ)'}},
    'やっつ':   {'counter': 'つ',     'irregular': True,  'note': '8-things; kun-stem yat-tsu.',                 'register_pair': {'casual_alt': 'やっつ', 'formal_same': '八個 (はっこ)'}},
    'ここのつ': {'counter': 'つ',     'irregular': True,  'note': '9-things; kun-stem kokono-tsu.',              'register_pair': {'casual_alt': 'ここのつ', 'formal_same': '九個 (きゅうこ)'}},
    'とお':     {'counter': 'つ',     'irregular': True,  'note': '10-things; kun reading is to-o (only number with no -tsu).', 'register_pair': {'casual_alt': 'とお', 'formal_same': '十個 (じゅっこ)'}},
    'いっぴき': {'counter': 'ひき',   'irregular': False, 'note': '1-small-animal. Sound change i+ppi-ki.',      'register_pair': {'casual_alt': 'いっぴき', 'formal_same': '一匹'}},
    'にひき':   {'counter': 'ひき',   'irregular': False, 'note': '2-small-animals.',                            'register_pair': {'casual_alt': 'にひき', 'formal_same': '二匹'}},
    'いっさつ': {'counter': 'さつ',   'irregular': False, 'note': '1-book/bound-volume.',                        'register_pair': {'casual_alt': 'いっさつ', 'formal_same': '一冊'}},
    'いちまい': {'counter': 'まい',   'irregular': False, 'note': '1-flat-thin-item (paper, plate, shirt).',     'register_pair': {'casual_alt': 'いちまい', 'formal_same': '一枚'}},
    'いっぽん': {'counter': 'ほん',   'irregular': False, 'note': '1-long-thin-item; sound change.',             'register_pair': {'casual_alt': 'いっぽん', 'formal_same': '一本'}},
    'にほん':   {'counter': 'ほん',   'irregular': False, 'note': '2-long-thin-items. Pitch distinguishes from 日本 (にほん, country).', 'register_pair': {'casual_alt': 'にほん', 'formal_same': '二本'}},
    'いっかい': {'counter': 'かい',   'irregular': False, 'note': '1-time / 1-floor.',                           'register_pair': {'casual_alt': 'いっかい', 'formal_same': '一回 / 一階'}},
    'いちにん': {'counter': 'にん',   'irregular': True,  'note': '1-person is normally ひとり; いちにん rare.',  'register_pair': {'casual_alt': 'ひとり', 'formal_same': '一名 (いちめい, very formal)'}},
    'ににん':   {'counter': 'にん',   'irregular': True,  'note': '2-people is normally ふたり; ににん rare.',   'register_pair': {'casual_alt': 'ふたり', 'formal_same': '二名'}},
    'さんにん': {'counter': 'にん',   'irregular': False, 'note': '3-people; regular onyomi pattern from 3 onwards.', 'register_pair': {'casual_alt': 'さんにん', 'formal_same': '三名'}},
    'よにん':   {'counter': 'にん',   'irregular': False, 'note': '4-people. 4 reads yo (irregular for hour: yo-ji).',  'register_pair': {'casual_alt': 'よにん', 'formal_same': '四名'}},
    'ごにん':   {'counter': 'にん',   'irregular': False, 'note': '5-people.',                                   'register_pair': {'casual_alt': 'ごにん', 'formal_same': '五名'}},
    'いっぱい': {'counter': 'はい',   'irregular': False, 'note': '1-cup/glass. Geminate sound change.',         'register_pair': {'casual_alt': 'いっぱい', 'formal_same': '一杯'}},
}

cr_added = 0
for e in entries:
    form = e.get('form')
    reading = e.get('reading')
    target = COUNTER_REG.get(form) or COUNTER_REG.get(reading)
    if target and not e.get('counter_register'):
        e['counter_register'] = target
        e['counter_register_provenance'] = 'llm_curated'
        cr_added += 1

# ===== false_friends expansion =====
# Word pairs that learners commonly confuse
FALSE_FRIENDS = {
    # Existing 18 -- skip; only add new ones
    'すき': ['きらい', 'こい'],     # like vs hate vs love
    'きらい': ['すき'],
    'たかい': ['やすい', 'ひくい'],  # expensive vs cheap; tall vs short
    'やすい': ['たかい', 'むずかしい'],  # cheap vs easy; both written 易しい/安い
    'いい': ['よい', 'いいえ'],      # casual good vs formal good vs no
    'よい': ['いい'],
    'おおきい': ['ちいさい'],
    'ちいさい': ['おおきい'],
    'はやい': ['おそい'],             # fast/early vs slow/late
    'おそい': ['はやい'],
    'あたらしい': ['ふるい'],
    'ふるい': ['あたらしい', 'ちかい'],  # old (thing) — vs near
    'あつい': ['さむい', 'つめたい'],   # hot (weather) vs hot (object) — distinct kanji 暑い/熱い
    'さむい': ['あつい'],
    'つめたい': ['あつい'],            # cold (object) vs hot (object) — pairs with thermal-touch
    'あまい': ['からい', 'にがい'],     # sweet vs spicy vs bitter
    'からい': ['あまい'],
    'にがい': ['あまい'],
    'たべる': ['のむ'],                # eat vs drink — different verbs by texture
    'のむ': ['たべる'],
    'みる': ['きく', 'よむ'],           # see vs hear vs read
    'きく': ['みる', 'はなす'],         # listen vs speak
    'はなす': ['きく', 'いう'],
    'いう': ['はなす', 'はなしする'],
    'もらう': ['あげる', 'くれる'],     # receive vs give-out vs give-to-me
    'あげる': ['もらう', 'くれる'],
    'くれる': ['あげる', 'もらう'],
    'いく': ['くる', 'かえる'],         # go vs come vs return
    'くる': ['いく'],
    'かえる': ['いく', 'くる'],         # return-home vs change (different kanji 帰る/変える)
    'はじまる': ['おわる', 'はじめる'],  # auto vs trans
    'おわる': ['はじまる'],
    'はじめる': ['はじまる', 'おわる'],
    'おきる': ['ねる'],                # wake vs sleep
    'ねる': ['おきる'],
    'のる': ['おりる'],                # board vs alight
    'おりる': ['のる'],
    'はいる': ['でる'],                # enter vs exit
    'でる': ['はいる'],
    'あう': ['わかれる'],              # meet vs part
    'わかれる': ['あう'],
    'いえ': ['うち'],                  # both = house, register diff
    'うち': ['いえ'],
    'てがみ': ['メール', 'はがき'],
    'はがき': ['てがみ'],
    'みず': ['おゆ'],                  # water vs hot-water
    'おゆ': ['みず'],
    'ひ': ['ひる'],                    # day/sun vs noon
    'ひる': ['よる', 'あさ'],
    'あさ': ['よる', 'ひる'],
    'よる': ['あさ', 'ひる'],
    'いま': ['さっき'],                # now vs recently
    'すこし': ['たくさん', 'おおぜい'], # a little vs a lot — おおぜい for people
    'たくさん': ['すこし'],
    'おおぜい': ['すこし', 'たくさん'], # many people vs many things
    'ぜんぶ': ['ぜんぜん', 'ほとんど'],
    'よく': ['たまに', 'ときどき'],     # often vs sometimes
    'ときどき': ['いつも', 'よく'],
    'いつも': ['たまに', 'ときどき'],
    'たまに': ['いつも', 'よく'],
    'やま': ['かわ', 'うみ'],          # mountain/river/sea cluster
    'かわ': ['やま', 'うみ'],
    'うみ': ['かわ', 'やま'],
    'はる': ['なつ', 'あき', 'ふゆ'],
    'なつ': ['はる', 'あき', 'ふゆ'],
    'あき': ['はる', 'なつ', 'ふゆ'],
    'ふゆ': ['はる', 'なつ', 'あき'],
}

ff_added = 0
for e in entries:
    form = e.get('form')
    reading = e.get('reading')
    target = FALSE_FRIENDS.get(form) or FALSE_FRIENDS.get(reading)
    if target and not e.get('false_friends'):
        e['false_friends'] = target
        e['false_friends_provenance'] = 'llm_curated'
        ff_added += 1

# ===== honorific_chain expansion =====
# Verb groups with humble/respectful variants
HON_CHAIN = {
    'いく': {'plain': 'いく', 'polite': 'いきます', 'humble': 'まいる', 'respectful': 'いらっしゃる', 'note': 'Motion verb — supplies all 3 honorific tiers.'},
    'くる': {'plain': 'くる', 'polite': 'きます', 'humble': 'まいる', 'respectful': 'いらっしゃる / おいでになる', 'note': 'Motion verb — same humble as 行く.'},
    'いる': {'plain': 'いる', 'polite': 'います', 'humble': 'おる', 'respectful': 'いらっしゃる', 'note': 'Existence (animate) — irregular humble おる.'},
    'たべる': {'plain': 'たべる', 'polite': 'たべます', 'humble': 'いただく', 'respectful': 'めしあがる', 'note': 'Eat/drink — humble いただく, respectful 召し上がる.'},
    'のむ': {'plain': 'のむ', 'polite': 'のみます', 'humble': 'いただく', 'respectful': 'めしあがる', 'note': 'Drink — same family as 食べる.'},
    'みる': {'plain': 'みる', 'polite': 'みます', 'humble': 'はいけんする', 'respectful': 'ごらんになる', 'note': 'See/look — humble 拝見, respectful ご覧.'},
    'いう': {'plain': 'いう', 'polite': 'いいます', 'humble': 'もうす / もうしあげる', 'respectful': 'おっしゃる', 'note': 'Say — humble 申す, respectful 仰る.'},
    'する': {'plain': 'する', 'polite': 'します', 'humble': 'いたす', 'respectful': 'なさる', 'note': 'Do — humble 致す, respectful なさる.'},
    'しる': {'plain': 'しる', 'polite': 'しっています', 'humble': 'ぞんじる / ぞんじあげる', 'respectful': 'ごぞんじだ', 'note': 'Know — humble 存じる, respectful ご存知.'},
    'もらう': {'plain': 'もらう', 'polite': 'もらいます', 'humble': 'いただく / ちょうだいする', 'respectful': 'おもらいになる (rare)', 'note': 'Receive — humble いただく / 頂戴.'},
    'あげる': {'plain': 'あげる', 'polite': 'あげます', 'humble': 'さしあげる', 'respectful': '(N/A — give is humble for self)', 'note': 'Give to others — humble 差し上げる.'},
    'くれる': {'plain': 'くれる', 'polite': 'くれます', 'humble': '(N/A — くれる is receive-by-me)', 'respectful': 'くださる', 'note': 'Give to me/in-group — respectful 下さる.'},
    'きく': {'plain': 'きく', 'polite': 'ききます', 'humble': 'うかがう / おききする', 'respectful': 'おききになる', 'note': 'Listen / ask — humble 伺う.'},
    'あう': {'plain': 'あう', 'polite': 'あいます', 'humble': 'おめにかかる', 'respectful': 'おあいになる', 'note': 'Meet — humble お目にかかる.'},
    'おもう': {'plain': 'おもう', 'polite': 'おもいます', 'humble': 'ぞんじる', 'respectful': 'おおもいになる (rare)', 'note': 'Think — humble 存じる (formal writing).'},
    'よむ': {'plain': 'よむ', 'polite': 'よみます', 'humble': 'はいけんする', 'respectful': 'およみになる', 'note': 'Read — humble shares with 見る (拝見).'},
    'かう': {'plain': 'かう', 'polite': 'かいます', 'humble': 'おもとめする', 'respectful': 'おもとめになる', 'note': 'Buy — humble お求めする.'},
    'うる': {'plain': 'うる', 'polite': 'うります', 'humble': '(rare)', 'respectful': 'おうりになる', 'note': 'Sell — uses regular o-stem formation.'},
    'はなす': {'plain': 'はなす', 'polite': 'はなします', 'humble': 'もうす / おはなしする', 'respectful': 'おはなしになる / おっしゃる', 'note': 'Talk — humble 申す.'},
    'かく': {'plain': 'かく', 'polite': 'かきます', 'humble': 'おかきする', 'respectful': 'おかきになる', 'note': 'Write — regular o-stem.'},
    'よぶ': {'plain': 'よぶ', 'polite': 'よびます', 'humble': 'およびする', 'respectful': 'およびになる', 'note': 'Call (someone) — regular o-stem.'},
    'まつ': {'plain': 'まつ', 'polite': 'まちます', 'humble': 'おまちする', 'respectful': 'おまちになる', 'note': 'Wait — regular o-stem.'},
    'おしえる': {'plain': 'おしえる', 'polite': 'おしえます', 'humble': 'おしえる', 'respectful': 'おしえになる', 'note': 'Teach — informal humble.'},
    'ねる': {'plain': 'ねる', 'polite': 'ねます', 'humble': 'やすむ', 'respectful': 'おやすみになる', 'note': 'Sleep — respectful お休みになる; humble shares with rest verb.'},
    'おきる': {'plain': 'おきる', 'polite': 'おきます', 'humble': 'おきる', 'respectful': 'おおきになる (rare)', 'note': 'Wake up — limited honorific elevation.'},
    'はいる': {'plain': 'はいる', 'polite': 'はいります', 'humble': 'はいらせていただく', 'respectful': 'おはいりになる', 'note': 'Enter — humble uses causative-receive.'},
    'やる': {'plain': 'やる', 'polite': 'やります', 'humble': '(varies)', 'respectful': '(use なさる)', 'note': 'Do (casual) — usually replaced by する/なさる in formal.'},
    'のる': {'plain': 'のる', 'polite': 'のります', 'humble': 'のる', 'respectful': 'おのりになる', 'note': 'Board/ride — respectful uses regular o-stem.'},
    'まなぶ': {'plain': 'まなぶ', 'polite': 'まなびます', 'humble': 'まなぶ', 'respectful': 'おまなびになる', 'note': 'Learn — basic regular o-stem honorific.'},
}

hc_added = 0
for e in entries:
    form = e.get('form')
    reading = e.get('reading')
    target = HON_CHAIN.get(form) or HON_CHAIN.get(reading)
    if target and not e.get('honorific_chain'):
        e['honorific_chain'] = target
        e['honorific_chain_provenance'] = 'llm_curated'
        hc_added += 1

vocab_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Summary
total = len(entries)
prag = sum(1 for e in entries if e.get('pragmatic_functions'))
dev = sum(1 for e in entries if e.get('devoiced_vowels'))
cr = sum(1 for e in entries if e.get('counter_register'))
ff = sum(1 for e in entries if e.get('false_friends'))
hc = sum(1 for e in entries if e.get('honorific_chain'))
print('=== BATCH RESULTS ===')
print(f'  V5 devoiced_vowels added:   {dev_added}  ->  {dev}/{total}')
print(f'  V2 pragmatic_functions:     {prag_added}  ->  {prag}/{total}')
print(f'  V8 counter_register:        {cr_added}  ->  {cr}/{total}')
print(f'  false_friends:              {ff_added}  ->  {ff}/{total}')
print(f'  honorific_chain:            {hc_added}  ->  {hc}/{total}')
