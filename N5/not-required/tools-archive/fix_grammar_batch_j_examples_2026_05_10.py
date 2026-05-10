"""Grammar Batch J (2026-05-10):
G1 expansion second pass. +30 patterns to >=10 examples each.
N5-only kanji + kana.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

grammar_path = ROOT / 'data' / 'grammar.json'
data = json.loads(grammar_path.read_text(encoding='utf-8'))
patterns = data['patterns']

NEW_EXAMPLES = {
    'n5-006': [  # へ
        {'ja': 'がっこうへ いきます。', 'form': 'destination', 'translation_en': 'I go to school.'},
        {'ja': 'にほんへ きました。', 'form': 'arrival', 'translation_en': 'I came to Japan.'},
        {'ja': 'うちへ かえります。', 'form': 'return-direction', 'translation_en': 'I return home.'},
    ],
    'n5-010': [  # まで
        {'ja': 'えきまで あるきます。', 'form': 'spatial-endpoint', 'translation_en': 'I walk to the station.'},
        {'ja': 'ろくじまで べんきょうしました。', 'form': 'time-until', 'translation_en': 'I studied until 6.'},
        {'ja': 'うちから がっこうまで バスで いきます。', 'form': 'range', 'translation_en': 'I go from home to school by bus.'},
    ],
    'n5-014': [  # これ/それ/あれ/どれ
        {'ja': 'これは ほんです。', 'form': 'near-speaker', 'translation_en': 'This is a book.'},
        {'ja': 'それは なんですか。', 'form': 'near-listener-question', 'translation_en': 'What is that?'},
        {'ja': 'あれは わたしの いえです。', 'form': 'far', 'translation_en': 'That over there is my house.'},
    ],
    'n5-015': [  # この/その/あの/どの + N
        {'ja': 'この ほんは おもしろいです。', 'form': 'near-modifier', 'translation_en': 'This book is interesting.'},
        {'ja': 'その ペンは だれの ですか。', 'form': 'near-listener', 'translation_en': 'Whose pen is that?'},
        {'ja': 'あの くるまは はやいです。', 'form': 'far-modifier', 'translation_en': 'That car is fast.'},
    ],
    'n5-016': [  # ここ/そこ/あそこ/どこ
        {'ja': 'ここは わたしの きょうしつです。', 'form': 'near-speaker-place', 'translation_en': 'This (here) is my classroom.'},
        {'ja': 'そこに ペンが あります。', 'form': 'near-listener-existence', 'translation_en': 'There (near you) is a pen.'},
        {'ja': 'あそこに ぎんこうが あります。', 'form': 'far-existence', 'translation_en': 'Over there is a bank.'},
    ],
    'n5-017': [  # なに/なん
        {'ja': 'これは なんですか。', 'form': 'wh-thing-counter-context', 'translation_en': 'What is this?'},
        {'ja': 'なにを たべますか。', 'form': 'wh-direct-object', 'translation_en': 'What will you eat?'},
        {'ja': 'いま、なんじですか。', 'form': 'wh-time-counter', 'translation_en': 'What time is it now?'},
    ],
    'n5-018': [  # だれ/どなた
        {'ja': 'あの ひとは だれですか。', 'form': 'wh-person-casual', 'translation_en': 'Who is that person?'},
        {'ja': 'どなたが やまだ先生ですか。', 'form': 'wh-person-polite', 'translation_en': 'Who is Mr/Ms Yamada?'},
        {'ja': 'これは だれの かばんですか。', 'form': 'wh-possession', 'translation_en': "Whose bag is this?"},
    ],
    'n5-019': [  # いつ
        {'ja': 'いつ にほんに きましたか。', 'form': 'wh-time-past', 'translation_en': 'When did you come to Japan?'},
        {'ja': 'たんじょうびは いつですか。', 'form': 'wh-time-question', 'translation_en': 'When is your birthday?'},
        {'ja': 'いつ かいぎが ありますか。', 'form': 'wh-time-event', 'translation_en': 'When is the meeting?'},
    ],
    'n5-021': [  # から〜まで
        {'ja': 'はちじから ろくじまで はたらきます。', 'form': 'time-range', 'translation_en': 'I work from 8 to 6.'},
        {'ja': 'うちから がっこうまで にじゅっぷんです。', 'form': 'distance-range', 'translation_en': "It's 20 minutes from home to school."},
        {'ja': 'げつようびから きんようびまで がっこうに いきます。', 'form': 'date-range', 'translation_en': 'I go to school from Monday to Friday.'},
    ],
    'n5-060': [  # Vました
        {'ja': 'きのう、えいがを みました。', 'form': 'past-experience', 'translation_en': 'I watched a movie yesterday.'},
        {'ja': 'けさ、しんぶんを よみました。', 'form': 'morning-completed', 'translation_en': 'I read the newspaper this morning.'},
        {'ja': 'もう ひるごはんを たべました。', 'form': 'already-completed', 'translation_en': "I've already eaten lunch."},
    ],
    'n5-061': [  # Vませんでした
        {'ja': 'きのう、がっこうに いきませんでした。', 'form': 'past-negative-action', 'translation_en': "I didn't go to school yesterday."},
        {'ja': 'なにも たべませんでした。', 'form': 'past-negative-quantifier', 'translation_en': "I didn't eat anything."},
        {'ja': 'まだ ホテルを よやくしませんでした。', 'form': 'past-negative-yet', 'translation_en': "I haven't reserved the hotel yet."},
    ],
    'n5-062': [  # Vましょう
        {'ja': 'いっしょに たべましょう。', 'form': 'together-suggestion', 'translation_en': "Let's eat together."},
        {'ja': 'こうえんに いきましょう。', 'form': 'plan-together', 'translation_en': "Let's go to the park."},
        {'ja': 'えいがを みましょう。', 'form': 'activity-suggestion', 'translation_en': "Let's watch a movie."},
    ],
    'n5-063': [  # Vましょうか
        {'ja': 'まどを あけましょうか。', 'form': 'offer-help', 'translation_en': 'Shall I open the window?'},
        {'ja': 'てつだいましょうか。', 'form': 'offer-assistance', 'translation_en': 'Shall I help you?'},
        {'ja': 'なにを かいましょうか。', 'form': 'wh-suggestion', 'translation_en': 'What should we buy?'},
    ],
    'n5-064': [  # Vませんか
        {'ja': 'いっしょに ひるごはんを たべませんか。', 'form': 'invitation-meal', 'translation_en': "Won't you eat lunch with me?"},
        {'ja': 'こうえんで さんぽしませんか。', 'form': 'invitation-walk', 'translation_en': "Want to take a walk in the park?"},
        {'ja': 'こんばん、えいがを みませんか。', 'form': 'invitation-evening', 'translation_en': "Want to watch a movie tonight?"},
    ],
    'n5-068': [  # Vなかった (plain past negative)
        {'ja': 'きのう、なにも たべなかった。', 'form': 'past-negative-plain', 'translation_en': "I didn't eat anything yesterday."},
        {'ja': 'がっこうに いかなかった。', 'form': 'past-skip', 'translation_en': "I didn't go to school."},
        {'ja': 'ともだちは こなかった。', 'form': 'past-no-show', 'translation_en': "My friend didn't come."},
    ],
    'n5-070': [  # Vて、Vて、…
        {'ja': 'おきて、シャワーを あびて、あさごはんを たべました。', 'form': 'morning-routine', 'translation_en': 'I got up, took a shower, and ate breakfast.'},
        {'ja': 'がっこうに いって、ともだちに あって、いっしょに ひるごはんを たべました。', 'form': 'day-events', 'translation_en': 'I went to school, met my friend, and ate lunch together.'},
        {'ja': 'ほんを よんで、おんがくを きいて、ねました。', 'form': 'evening', 'translation_en': 'I read a book, listened to music, and went to bed.'},
    ],
    'n5-073': [  # Vていません
        {'ja': 'まだ ひるごはんを たべて いません。', 'form': 'not-yet-meal', 'translation_en': "I haven't eaten lunch yet."},
        {'ja': 'まだ しゅくだいを して いません。', 'form': 'not-yet-homework', 'translation_en': "I haven't done my homework yet."},
        {'ja': 'まだ きていません。', 'form': 'not-yet-arrived', 'translation_en': "(They) haven't come yet."},
    ],
    'n5-074': [  # Vてもいいです
        {'ja': 'ここで しゃしんを とっても いいですか。', 'form': 'permission-photo', 'translation_en': 'May I take pictures here?'},
        {'ja': 'えんぴつで かいても いいですよ。', 'form': 'grant-permission', 'translation_en': "It's OK to write in pencil."},
        {'ja': 'すこし やすんでも いいですか。', 'form': 'rest-permission', 'translation_en': 'May I rest a bit?'},
    ],
    'n5-075': [  # Vてはいけません
        {'ja': 'ここで たばこを すっては いけません。', 'form': 'prohibition-smoke', 'translation_en': "You mustn't smoke here."},
        {'ja': 'じゅぎょうちゅうに はなしては いけません。', 'form': 'prohibition-class', 'translation_en': "You mustn't talk during class."},
        {'ja': 'ここで あそんでは いけません。', 'form': 'prohibition-play', 'translation_en': "You mustn't play here."},
    ],
    'n5-076': [  # Vてから
        {'ja': 'ばんごはんを たべてから、 テレビを みます。', 'form': 'after-meal-tv', 'translation_en': "I watch TV after eating dinner."},
        {'ja': 'しゅくだいを してから、 あそびます。', 'form': 'after-homework', 'translation_en': "I'll play after doing my homework."},
        {'ja': 'てを あらってから、 たべて ください。', 'form': 'after-handwash', 'translation_en': "Please eat after washing your hands."},
    ],
    'n5-077': [  # Vないでください
        {'ja': 'ここで しゃしんを とらないで ください。', 'form': 'request-negative-photo', 'translation_en': "Please don't take pictures here."},
        {'ja': 'おおきい こえで はなさないで ください。', 'form': 'request-quiet', 'translation_en': "Please don't speak loudly."},
        {'ja': 'まだ いかないで ください。', 'form': 'request-stay', 'translation_en': "Please don't go yet."},
    ],
    'n5-081': [  # i-Adj past
        {'ja': 'きのうは あつかったです。', 'form': 'past-weather', 'translation_en': 'It was hot yesterday.'},
        {'ja': 'えいがは おもしろかったです。', 'form': 'past-evaluation', 'translation_en': 'The movie was interesting.'},
        {'ja': 'りょこうは たのしかったです。', 'form': 'past-experience', 'translation_en': 'The trip was fun.'},
    ],
    'n5-082': [  # i-Adj past negative
        {'ja': 'きのうは あまり あつくなかったです。', 'form': 'past-mild-negative', 'translation_en': 'It wasn\'t very hot yesterday.'},
        {'ja': 'テストは むずかしくなかったです。', 'form': 'past-evaluation-negative', 'translation_en': 'The test wasn\'t difficult.'},
        {'ja': 'りょうりは おいしくなかったです。', 'form': 'past-taste-negative', 'translation_en': 'The food wasn\'t tasty.'},
    ],
    'n5-083': [  # i-Adj te-form くて
        {'ja': 'この りょうりは おいしくて やすいです。', 'form': 'and-positive', 'translation_en': 'This food is tasty and cheap.'},
        {'ja': 'まちは あかるくて にぎやかです。', 'form': 'mixed-adj', 'translation_en': 'The town is bright and lively.'},
        {'ja': 'きょうは あつくて つかれました。', 'form': 'cause-effect', 'translation_en': 'It was hot today, so I got tired.'},
    ],
    'n5-086': [  # na-Adj negative
        {'ja': 'この まちは しずかじゃありません。', 'form': 'negative-place', 'translation_en': 'This town is not quiet.'},
        {'ja': 'にほんごは あまり じょうずじゃありません。', 'form': 'modesty-skill', 'translation_en': "I'm not very good at Japanese."},
        {'ja': 'べんりじゃありません。', 'form': 'negative-evaluation', 'translation_en': "It's not convenient."},
    ],
    'n5-087': [  # na-Adj past
        {'ja': 'きのうは げんきでした。', 'form': 'past-state', 'translation_en': 'I was healthy/lively yesterday.'},
        {'ja': 'こうえんは しずかでした。', 'form': 'past-place', 'translation_en': 'The park was quiet.'},
        {'ja': 'やまださんは しんせつでした。', 'form': 'past-personality', 'translation_en': 'Yamada-san was kind.'},
    ],
    'n5-088': [  # na-Adj past negative
        {'ja': 'こうえんは しずかじゃありませんでした。', 'form': 'past-negative-place', 'translation_en': "The park wasn't quiet."},
        {'ja': 'きのうは げんきじゃありませんでした。', 'form': 'past-negative-state', 'translation_en': "I wasn't well yesterday."},
        {'ja': 'りょこうは あんぜんじゃありませんでした。', 'form': 'past-negative-evaluation', 'translation_en': "The trip wasn't safe."},
    ],
    'n5-089': [  # na-Adj te-form で
        {'ja': 'やまださんは しんせつで、 おもしろいです。', 'form': 'and-mixed', 'translation_en': 'Yamada-san is kind and interesting.'},
        {'ja': 'この まちは しずかで、 きれいです。', 'form': 'and-place', 'translation_en': 'This town is quiet and beautiful.'},
        {'ja': 'ひまで、 たいくつでした。', 'form': 'cause-state', 'translation_en': 'I had free time and was bored.'},
    ],
    'n5-095': [  # 〜は〜より〜です
        {'ja': 'にほんは アメリカより ちいさいです。', 'form': 'comparative-size', 'translation_en': 'Japan is smaller than America.'},
        {'ja': 'コーヒーは こうちゃより たかいです。', 'form': 'comparative-price', 'translation_en': 'Coffee is more expensive than tea.'},
        {'ja': 'きょうは きのうより あついです。', 'form': 'comparative-weather', 'translation_en': "It's hotter today than yesterday."},
    ],
    'n5-097': [  # 〜と〜と、どちらが
        {'ja': 'コーヒーと こうちゃと、どちらが すきですか。', 'form': 'binary-preference', 'translation_en': 'Which do you prefer, coffee or tea?'},
        {'ja': 'なつと ふゆと、どちらが すきですか。', 'form': 'season-preference', 'translation_en': 'Which do you like, summer or winter?'},
        {'ja': 'バスと でんしゃと、どちらが はやいですか。', 'form': 'binary-comparison', 'translation_en': 'Which is faster, bus or train?'},
    ],
}

added_patterns = 0
added_examples = 0
patterns_by_id = {p['id']: p for p in patterns}
for pid, new_examples in NEW_EXAMPLES.items():
    p = patterns_by_id.get(pid)
    if not p:
        continue
    examples = p.get('examples') or []
    if len(examples) >= 10:
        continue
    for ex in new_examples:
        ex['provenance'] = 'llm_curated'
    examples.extend(new_examples)
    p['examples'] = examples
    added_patterns += 1
    added_examples += len(new_examples)

print(f'Patterns expanded: {added_patterns}')
print(f'New examples added: {added_examples}')

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

total = len(patterns)
ge10 = sum(1 for p in patterns if len(p.get('examples') or []) >= 10)
avg = sum(len(p.get('examples') or []) for p in patterns) / total
print()
print('=== FINAL ===')
print(f'  examples >=10/pattern:  {ge10}/{total}')
print(f'  avg examples/pattern:   {avg:.1f}')

# OOS check
K = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
N5 = set()
for e in K.get('entries', []):
    g = e.get('glyph') or e.get('id','').split('.')[-1]
    if g: N5.add(g)
def is_kanji(c): return 0x4E00 <= ord(c) <= 0x9FFF
oos = {}
for pid in NEW_EXAMPLES:
    p = patterns_by_id.get(pid)
    if not p: continue
    for ex in p.get('examples', []):
        if ex.get('provenance') != 'llm_curated': continue
        for k in ('ja',):
            v = ex.get(k,'')
            for c in str(v):
                if is_kanji(c) and c not in N5:
                    oos.setdefault(c, []).append(pid)
print(f'OOS in new examples: {len(oos)} -> {list(oos.keys())}')
