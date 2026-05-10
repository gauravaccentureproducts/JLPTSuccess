"""Grammar Batch K (2026-05-11):
G1 expansion third pass. +30 patterns to >=10 examples.
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
    'n5-029': [  # possessive の
        {'ja': 'これは わたしの ほんです。', 'form': 'simple-possessive', 'translation_en': 'This is my book.'},
        {'ja': 'やまださんの くるまは あれです。', 'form': 'person-possessive', 'translation_en': "Yamada-san's car is that one over there."},
        {'ja': 'にほんの たべものが すきです。', 'form': 'origin-modifier', 'translation_en': 'I like Japanese food.'},
    ],
    'n5-033': [  # だけ
        {'ja': 'いちじかんだけ ねました。', 'form': 'duration-only', 'translation_en': 'I slept only one hour.'},
        {'ja': 'ふたりだけ きました。', 'form': 'people-only', 'translation_en': 'Only two people came.'},
        {'ja': 'これだけ かいました。', 'form': 'quantity-only', 'translation_en': 'I bought only this much.'},
    ],
    'n5-034': [  # しか〜ない
        {'ja': 'いちじかんしか ねませんでした。', 'form': 'duration-only-negative', 'translation_en': "I slept only one hour."},
        {'ja': 'ひとりしか きませんでした。', 'form': 'people-only-negative', 'translation_en': 'Only one person came.'},
        {'ja': 'ひゃくえんしか ありません。', 'form': 'money-only-negative', 'translation_en': "I have only 100 yen."},
    ],
    'n5-035': [  # ぐらい/くらい
        {'ja': 'いちじかんぐらい べんきょうします。', 'form': 'duration-approx', 'translation_en': 'I study about one hour.'},
        {'ja': 'ひゃくえんぐらいです。', 'form': 'price-approx', 'translation_en': "It's about 100 yen."},
        {'ja': 'じゅっぷんぐらい かかります。', 'form': 'time-required-approx', 'translation_en': 'It takes about 10 minutes.'},
    ],
    'n5-053': [  # いくら
        {'ja': 'これは いくらですか。', 'form': 'price-question', 'translation_en': 'How much is this?'},
        {'ja': 'ぜんぶで いくらですか。', 'form': 'total-question', 'translation_en': "How much in total?"},
        {'ja': 'たまごは いくらですか。', 'form': 'specific-item-price', 'translation_en': 'How much are the eggs?'},
    ],
    'n5-055': [  # なんじ
        {'ja': 'いま、なんじですか。', 'form': 'current-time', 'translation_en': 'What time is it now?'},
        {'ja': 'がっこうは なんじから ですか。', 'form': 'start-time', 'translation_en': 'What time does school start?'},
        {'ja': 'なんじに あいましょうか。', 'form': 'meeting-time', 'translation_en': 'What time shall we meet?'},
    ],
    'n5-059': [  # Vません
        {'ja': 'おさけは のみません。', 'form': 'habitual-negative', 'translation_en': "I don't drink alcohol."},
        {'ja': 'あした、がっこうに いきません。', 'form': 'future-negative', 'translation_en': "I won't go to school tomorrow."},
        {'ja': 'にくは たべません。', 'form': 'preference-negative', 'translation_en': "I don't eat meat."},
    ],
    'n5-065': [  # Vる/Vう plain forms
        {'ja': 'まいにち しんぶんを よむ。', 'form': 'plain-habit', 'translation_en': 'I read the newspaper every day.'},
        {'ja': 'おちゃを のむ？', 'form': 'plain-offer', 'translation_en': 'Drink some tea?'},
        {'ja': 'あした、はやく おきる。', 'form': 'plain-future', 'translation_en': "I'll get up early tomorrow."},
    ],
    'n5-078': [  # い-Adj + N
        {'ja': 'たかい くるまを かいました。', 'form': 'price-modifier', 'translation_en': 'I bought an expensive car.'},
        {'ja': 'ちいさい ねこが います。', 'form': 'size-modifier', 'translation_en': 'There is a small cat.'},
        {'ja': 'あたらしい ほんを よみました。', 'form': 'condition-modifier', 'translation_en': 'I read a new book.'},
    ],
    'n5-084': [  # na-Adj + な + N
        {'ja': 'しずかな まちです。', 'form': 'state-modifier', 'translation_en': "It's a quiet town."},
        {'ja': 'きれいな はなが あります。', 'form': 'beauty-modifier', 'translation_en': 'There are beautiful flowers.'},
        {'ja': 'しんせつな ひとに あいました。', 'form': 'personality-modifier', 'translation_en': 'I met a kind person.'},
    ],
    'n5-092': [  # 〜に〜があります/います
        {'ja': 'つくえに ほんが あります。', 'form': 'location-inanimate', 'translation_en': 'There is a book on the desk.'},
        {'ja': 'うちに ねこが います。', 'form': 'location-animate', 'translation_en': 'There is a cat at my house.'},
        {'ja': 'きょうしつに がくせいが います。', 'form': 'place-people', 'translation_en': 'There are students in the classroom.'},
    ],
    'n5-093': [  # 〜は〜にあります/います
        {'ja': 'ほんは つくえに あります。', 'form': 'topic-location', 'translation_en': 'The book is on the desk.'},
        {'ja': 'ねこは うちに います。', 'form': 'topic-location-animate', 'translation_en': 'The cat is at home.'},
        {'ja': 'ぎんこうは えきの まえに あります。', 'form': 'place-relative-location', 'translation_en': 'The bank is in front of the station.'},
    ],
    'n5-102': [  # 〜が分かります
        {'ja': 'えいごが わかります。', 'form': 'comprehension', 'translation_en': 'I understand English.'},
        {'ja': 'にほんごが すこし わかります。', 'form': 'partial-comprehension', 'translation_en': 'I understand a little Japanese.'},
        {'ja': 'いみが わかりません。', 'form': 'negative-comprehension', 'translation_en': "I don't understand the meaning."},
    ],
    'n5-103': [  # 〜ができます
        {'ja': 'にほんごが できます。', 'form': 'ability', 'translation_en': 'I can speak Japanese.'},
        {'ja': 'うんてんが できますか。', 'form': 'ability-question', 'translation_en': 'Can you drive?'},
        {'ja': 'りょうりが あまり できません。', 'form': 'modest-ability', 'translation_en': "I can't cook very well."},
    ],
    'n5-105': [  # たくない
        {'ja': 'いまは なにも たべたくないです。', 'form': 'no-desire-eat', 'translation_en': "I don't want to eat anything now."},
        {'ja': 'がっこうに いきたくないです。', 'form': 'no-desire-go', 'translation_en': "I don't want to go to school."},
        {'ja': 'はたらきたくないです。', 'form': 'no-desire-work', 'translation_en': "I don't want to work."},
    ],
    'n5-107': [  # V-stem + に行きます
        {'ja': 'ともだちに あいに いきます。', 'form': 'purpose-meet', 'translation_en': "I'll go to meet my friend."},
        {'ja': 'おちゃを のみに いきました。', 'form': 'purpose-drink', 'translation_en': 'I went to drink tea.'},
        {'ja': 'えいがを みに きました。', 'form': 'purpose-watch', 'translation_en': 'I came to watch a movie.'},
    ],
    'n5-108': [  # Number + counter
        {'ja': 'りんごを みっつ かいました。', 'form': 'counter-object-tsu', 'translation_en': 'I bought three apples.'},
        {'ja': 'ひとが さんにん きました。', 'form': 'counter-people', 'translation_en': 'Three people came.'},
        {'ja': 'ねこが にひき います。', 'form': 'counter-small-animals', 'translation_en': 'There are two cats.'},
    ],
    'n5-111': [  # ～じ
        {'ja': 'いま、しちじです。', 'form': 'current-time-statement', 'translation_en': "It's 7 o'clock now."},
        {'ja': 'よじに ともだちに あいます。', 'form': 'meeting-time', 'translation_en': "I'll meet my friend at 4."},
        {'ja': 'がっこうは くじから です。', 'form': 'school-start', 'translation_en': "School starts at 9."},
    ],
    'n5-114': [  # ～から～まで (range, duplicate of 021)
        {'ja': 'はちじから ごじまで はたらきます。', 'form': 'work-hours', 'translation_en': 'I work from 8 to 5.'},
        {'ja': 'うちから がっこうまで さんじゅっぷんです。', 'form': 'distance-time', 'translation_en': "It's 30 minutes from home to school."},
        {'ja': 'いちがつから さんがつまで さむいです。', 'form': 'month-range', 'translation_en': "It's cold from January to March."},
    ],
    'n5-115': [  # に (time)
        {'ja': 'しちじに おきます。', 'form': 'time-specific-clock', 'translation_en': "I get up at 7."},
        {'ja': 'にちようびに あそびます。', 'form': 'day-of-week', 'translation_en': "I play on Sundays."},
        {'ja': 'いちがつに にほんに きました。', 'form': 'specific-month', 'translation_en': "I came to Japan in January."},
    ],
    'n5-118': [  # いま/すぐ/もう/まだ
        {'ja': 'もう しゅくだいを しました。', 'form': 'already-done', 'translation_en': "I've already done my homework."},
        {'ja': 'まだ ねないで ください。', 'form': 'not-yet-request', 'translation_en': "Please don't sleep yet."},
        {'ja': 'すぐ きます。', 'form': 'right-away', 'translation_en': "I'll come right away."},
    ],
    'n5-119': [  # ～まえ
        {'ja': 'ねるまえに、 はを みがきます。', 'form': 'before-sleep', 'translation_en': 'I brush my teeth before sleeping.'},
        {'ja': 'がっこうの まえに、 あさごはんを たべます。', 'form': 'before-school', 'translation_en': 'I eat breakfast before school.'},
        {'ja': 'たべるまえに、 てを あらいます。', 'form': 'before-eating', 'translation_en': 'I wash my hands before eating.'},
    ],
    'n5-120': [  # ～あと
        {'ja': 'たべた あとで、 ねます。', 'form': 'after-eat-sleep', 'translation_en': "I'll sleep after eating."},
        {'ja': 'べんきょうした あとで、 テレビを みます。', 'form': 'after-study', 'translation_en': "I watch TV after studying."},
        {'ja': 'がっこうの あとで、 あそびます。', 'form': 'after-school', 'translation_en': "I play after school."},
    ],
    'n5-122': [  # それから
        {'ja': 'あさごはんを たべました。それから、 がっこうに いきました。', 'form': 'sequence-then', 'translation_en': 'I ate breakfast. Then I went to school.'},
        {'ja': 'しゅくだいを しました。それから、 おふろに はいりました。', 'form': 'evening-then', 'translation_en': 'I did my homework. Then I took a bath.'},
        {'ja': 'ほんを かいました。それから、 カフェに いきました。', 'form': 'shopping-then', 'translation_en': 'I bought a book. Then I went to a cafe.'},
    ],
    'n5-123': [  # でも
        {'ja': 'にほんごは むずかしいです。でも、 たのしいです。', 'form': 'contrast-eval', 'translation_en': "Japanese is difficult. But it's fun."},
        {'ja': 'たかいです。でも、 おいしいです。', 'form': 'price-quality-contrast', 'translation_en': "It's expensive. But it's tasty."},
        {'ja': 'あめが ふって います。でも、 でかけます。', 'form': 'weather-contrast', 'translation_en': "It's raining. But I'll go out."},
    ],
    'n5-124': [  # しかし
        {'ja': 'にほんごは むずかしいです。しかし、 がんばります。', 'form': 'difficulty-resolve', 'translation_en': "Japanese is difficult. However, I'll do my best."},
        {'ja': 'たかいです。しかし、 ひつようです。', 'form': 'price-necessity', 'translation_en': "It's expensive. However, it's necessary."},
        {'ja': 'つかれました。しかし、 まだ しごとが あります。', 'form': 'fatigue-work', 'translation_en': "I'm tired. However, I still have work."},
    ],
    'n5-126': [  # が (but)
        {'ja': 'たかいですが、 おいしいです。', 'form': 'price-quality-but', 'translation_en': "It's expensive, but tasty."},
        {'ja': 'にほんごは むずかしいですが、 おもしろいです。', 'form': 'difficulty-interest', 'translation_en': "Japanese is difficult but interesting."},
        {'ja': 'いきたいですが、 じかんが ありません。', 'form': 'desire-no-time', 'translation_en': "I want to go, but I have no time."},
    ],
    'n5-131': [  # 〜にもらいます
        {'ja': 'ともだちから プレゼントを もらいました。', 'form': 'receive-from-friend', 'translation_en': 'I received a present from my friend.'},
        {'ja': 'せんせいに ほんを いただきました。', 'form': 'receive-formal', 'translation_en': 'I received a book from my teacher.'},
        {'ja': 'なにを もらいましたか。', 'form': 'receive-question', 'translation_en': 'What did you receive?'},
    ],
    'n5-132': [  # 〜がくれます
        {'ja': 'ともだちが プレゼントを くれました。', 'form': 'gift-from-friend', 'translation_en': 'My friend gave me a present.'},
        {'ja': 'はは が ほんを くれました。', 'form': 'mother-gift', 'translation_en': 'My mother gave me a book.'},
        {'ja': 'やまださんが おかしを くれました。', 'form': 'person-snack', 'translation_en': 'Yamada-san gave me sweets.'},
    ],
    'n5-145': [  # と思います
        {'ja': 'あした、 あめが ふると おもいます。', 'form': 'opinion-weather', 'translation_en': 'I think it will rain tomorrow.'},
        {'ja': 'やまださんは げんきだと おもいます。', 'form': 'opinion-person', 'translation_en': 'I think Yamada-san is well.'},
        {'ja': 'むずかしいと おもいます。', 'form': 'opinion-evaluation', 'translation_en': 'I think it is difficult.'},
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
