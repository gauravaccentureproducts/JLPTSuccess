"""Grammar Batch L (2026-05-11):
G1 expansion fourth pass. +30 patterns to >=10 examples.
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
    'n5-011': [  # や (non-exhaustive list)
        {'ja': 'りんごや みかんを かいました。', 'form': 'list-fruit', 'translation_en': 'I bought apples, oranges, etc.'},
        {'ja': 'ねこや いぬが すきです。', 'form': 'list-animals', 'translation_en': 'I like cats and dogs (among others).'},
        {'ja': 'ノートや えんぴつなどを かいました。', 'form': 'list-with-など', 'translation_en': 'I bought notebooks, pencils, etc.'},
    ],
    'n5-023': [  # か (question)
        {'ja': 'これは ペンですか。', 'form': 'yn-question', 'translation_en': 'Is this a pen?'},
        {'ja': 'たべましたか。', 'form': 'past-question', 'translation_en': 'Did you eat?'},
        {'ja': 'なんじですか。', 'form': 'wh-question-with-か', 'translation_en': 'What time is it?'},
    ],
    'n5-025': [  # ね
        {'ja': 'いい てんきですね。', 'form': 'weather-agreement', 'translation_en': 'Nice weather, isn\'t it?'},
        {'ja': 'たかいですね。', 'form': 'observation-agreement', 'translation_en': "It's expensive, isn't it?"},
        {'ja': 'おいしいですね。', 'form': 'taste-agreement', 'translation_en': "It's delicious, isn't it?"},
    ],
    'n5-026': [  # よ
        {'ja': 'これは おいしいですよ。', 'form': 'assertion-recommend', 'translation_en': "This is tasty (you should know)."},
        {'ja': 'もう おそいですよ。', 'form': 'warning', 'translation_en': "It's already late (you should know)."},
        {'ja': 'やまださんは げんきですよ。', 'form': 'informing', 'translation_en': "Yamada-san is well (you should know)."},
    ],
    'n5-028': [  # の (modification)
        {'ja': 'にほんの たべものが すきです。', 'form': 'origin-mod', 'translation_en': 'I like Japanese food.'},
        {'ja': 'やまださんの くるまは あれです。', 'form': 'possession-mod', 'translation_en': "Yamada-san's car is that one."},
        {'ja': 'がっこうの まえに あいましょう。', 'form': 'place-mod', 'translation_en': "Let's meet in front of the school."},
    ],
    'n5-031': [  # の (pronoun)
        {'ja': 'あかいのを ください。', 'form': 'pronoun-color', 'translation_en': "Please give me the red one."},
        {'ja': 'おおきいのが すきです。', 'form': 'pronoun-size', 'translation_en': "I like big ones."},
        {'ja': 'もっと やすいのは ありますか。', 'form': 'pronoun-price', 'translation_en': "Do you have a cheaper one?"},
    ],
    'n5-036': [  # ごろ
        {'ja': 'にじごろ あいましょう。', 'form': 'time-approx-meet', 'translation_en': "Let's meet around 2."},
        {'ja': 'しちじごろ おきます。', 'form': 'time-approx-wake', 'translation_en': 'I get up around 7.'},
        {'ja': 'いつごろ かえりますか。', 'form': 'time-approx-question', 'translation_en': 'Around when will you return?'},
    ],
    'n5-037': [  # など
        {'ja': 'ノートや ペンなどを かいました。', 'form': 'list-with-など', 'translation_en': 'I bought things like notebooks and pens.'},
        {'ja': 'えいがや ほんなどが すきです。', 'form': 'preference-list', 'translation_en': 'I like things like movies and books.'},
        {'ja': 'バスや でんしゃなどで いきます。', 'form': 'transport-list', 'translation_en': 'I go by bus, train, etc.'},
    ],
    'n5-038': [  # ずつ
        {'ja': 'ひとり いっこずつ ください。', 'form': 'distributive', 'translation_en': 'One each per person, please.'},
        {'ja': 'まいにち すこしずつ べんきょうします。', 'form': 'daily-incremental', 'translation_en': 'I study a little each day.'},
        {'ja': 'ふたつずつ かいました。', 'form': 'two-each', 'translation_en': 'I bought two of each.'},
    ],
    'n5-040': [  # この/その/あの/どの + N (variant)
        {'ja': 'この まちは ちいさいです。', 'form': 'near-town', 'translation_en': 'This town is small.'},
        {'ja': 'その くるまは あたらしいです。', 'form': 'near-listener-car', 'translation_en': 'That car (near you) is new.'},
        {'ja': 'あの ひとは だれですか。', 'form': 'far-who', 'translation_en': 'Who is that person?'},
    ],
    'n5-042': [  # こちら/そちら/あちら/どちら
        {'ja': 'こちらへ どうぞ。', 'form': 'this-way-please', 'translation_en': 'This way, please.'},
        {'ja': 'どちらが いいですか。', 'form': 'which-binary', 'translation_en': 'Which is good?'},
        {'ja': 'やまださんは あちらです。', 'form': 'far-person-polite', 'translation_en': 'Yamada-san is over there.'},
    ],
    'n5-044': [  # こう/そう/ああ/どう
        {'ja': 'こう しましょう。', 'form': 'this-way-manner', 'translation_en': "Let's do it this way."},
        {'ja': 'どう しましたか。', 'form': 'what-happened', 'translation_en': 'What happened?'},
        {'ja': 'そう おもいます。', 'form': 'agreement-opinion', 'translation_en': 'I think so.'},
    ],
    'n5-049': [  # どれ/どの/どちら
        {'ja': 'どれが すきですか。', 'form': 'which-pronoun', 'translation_en': 'Which one do you like?'},
        {'ja': 'どの ほんが いいですか。', 'form': 'which-with-noun', 'translation_en': 'Which book is good?'},
        {'ja': 'どちらが はやいですか。', 'form': 'binary-faster', 'translation_en': 'Which is faster?'},
    ],
    'n5-054': [  # いくつ
        {'ja': 'りんごは いくつ ありますか。', 'form': 'count-objects', 'translation_en': 'How many apples are there?'},
        {'ja': 'なん さいですか。 / おいくつですか。', 'form': 'age-polite', 'translation_en': 'How old are you?'},
        {'ja': 'いくつ かいましたか。', 'form': 'count-bought', 'translation_en': 'How many did you buy?'},
    ],
    'n5-056': [  # なんようび
        {'ja': 'きょうは なんようびですか。', 'form': 'today-day', 'translation_en': 'What day is today?'},
        {'ja': 'やすみは なんようびですか。', 'form': 'holiday-day', 'translation_en': 'What day is the holiday?'},
        {'ja': 'なんようびに あいましょうか。', 'form': 'meeting-day', 'translation_en': 'What day shall we meet?'},
    ],
    'n5-057': [  # なんがつ なんにち
        {'ja': 'たんじょうびは なんがつ なんにちですか。', 'form': 'birthday-date', 'translation_en': 'What date is your birthday?'},
        {'ja': 'きょうは なんにちですか。', 'form': 'today-date', 'translation_en': "What's today's date?"},
        {'ja': 'なんがつに きましたか。', 'form': 'arrival-month', 'translation_en': 'What month did you arrive?'},
    ],
    'n5-096': [  # 〜より〜のほうが
        {'ja': 'コーヒーより こうちゃの ほうが すきです。', 'form': 'preference-comparison', 'translation_en': "I like tea more than coffee."},
        {'ja': 'バスより でんしゃの ほうが はやいです。', 'form': 'speed-comparison', 'translation_en': 'Trains are faster than buses.'},
        {'ja': 'にほんごより えいごの ほうが やさしいです。', 'form': 'difficulty-comparison', 'translation_en': 'English is easier than Japanese.'},
    ],
    'n5-112': [  # ふん/ぷん
        {'ja': 'にじゅっぷん かかります。', 'form': 'duration-minutes', 'translation_en': 'It takes 20 minutes.'},
        {'ja': 'ごじはん から いちじかん べんきょうしました。', 'form': 'half-past-duration', 'translation_en': 'I studied for an hour from 5:30.'},
        {'ja': 'よんじゅっぷん あるきました。', 'form': 'walked-minutes', 'translation_en': 'I walked for 40 minutes.'},
    ],
    'n5-113': [  # じはん
        {'ja': 'いま、にじはんです。', 'form': 'current-half-past', 'translation_en': "It's 2:30 now."},
        {'ja': 'よじはんに あいましょう。', 'form': 'half-past-meet', 'translation_en': "Let's meet at 4:30."},
        {'ja': 'がっこうは くじはんから です。', 'form': 'school-half-past', 'translation_en': 'School starts at 9:30.'},
    ],
    'n5-116': [  # まいにち
        {'ja': 'まいにち コーヒーを のみます。', 'form': 'daily-drink', 'translation_en': 'I drink coffee every day.'},
        {'ja': 'まいしゅう、 ともだちに あいます。', 'form': 'weekly-meet', 'translation_en': 'I meet my friend every week.'},
        {'ja': 'まいとし、 にほんに いきます。', 'form': 'yearly-travel', 'translation_en': 'I go to Japan every year.'},
    ],
    'n5-125': [  # では / じゃ
        {'ja': 'では、また あした。', 'form': 'farewell-formal', 'translation_en': 'Well then, see you tomorrow.'},
        {'ja': 'じゃ、また。', 'form': 'farewell-casual', 'translation_en': 'See you.'},
        {'ja': 'それでは、 はじめましょう。', 'form': 'transition-start', 'translation_en': "Well then, let's begin."},
    ],
    'n5-127': [  # けれど/けど
        {'ja': 'たかいけど、 おいしい。', 'form': 'casual-but', 'translation_en': "It's expensive, but tasty."},
        {'ja': 'がっこうは とおいけど、 たのしい。', 'form': 'distance-fun', 'translation_en': "School is far, but fun."},
        {'ja': 'にほんごは むずかしいけれど、 おもしろい。', 'form': 'literary-but', 'translation_en': 'Japanese is difficult, but interesting.'},
    ],
    'n5-129': [  # どうして〜から
        {'ja': 'どうして きませんでしたか。 あめでしたから。', 'form': 'why-rain', 'translation_en': "Why didn't you come? Because it was raining."},
        {'ja': 'どうして すきですか。 おいしいからです。', 'form': 'why-tasty', 'translation_en': 'Why do you like it? Because it\'s tasty.'},
        {'ja': 'どうして いそぎますか。 おそいからです。', 'form': 'why-late', 'translation_en': "Why are you hurrying? Because I'm late."},
    ],
    'n5-133': [  # から (reason)
        {'ja': 'さむいから、 コートを きます。', 'form': 'cold-coat', 'translation_en': "Because it's cold, I'll wear a coat."},
        {'ja': 'あした しごとが あるから、 はやく ねます。', 'form': 'work-sleep', 'translation_en': "Because I have work tomorrow, I'll sleep early."},
        {'ja': 'おなかが すいたから、 たべます。', 'form': 'hungry-eat', 'translation_en': "Because I'm hungry, I'll eat."},
    ],
    'n5-134': [  # ので
        {'ja': 'あめが ふっているので、 でかけません。', 'form': 'rain-stay', 'translation_en': "Since it's raining, I won't go out."},
        {'ja': 'いそがしいので、 いけません。', 'form': 'busy-cant-go', 'translation_en': "Since I'm busy, I can't go."},
        {'ja': 'がくせいなので、 やすいです。', 'form': 'student-cheap', 'translation_en': "Since I'm a student, it's cheap."},
    ],
    'n5-142': [  # にします
        {'ja': 'コーヒーに します。', 'form': 'order-choice', 'translation_en': "I'll have coffee."},
        {'ja': 'なにに しますか。', 'form': 'choice-question', 'translation_en': "What will you have?"},
        {'ja': 'これに します。', 'form': 'pick-this', 'translation_en': "I'll choose this one."},
    ],
    'n5-143': [  # になります/くなります
        {'ja': 'さむく なりました。', 'form': 'become-cold', 'translation_en': "It's gotten cold."},
        {'ja': 'にほんごが じょうずに なりたいです。', 'form': 'aspire-skilled', 'translation_en': 'I want to become good at Japanese.'},
        {'ja': 'おとなに なりました。', 'form': 'became-adult', 'translation_en': "I've become an adult."},
    ],
    'n5-144': [  # ながら
        {'ja': 'おんがくを ききながら べんきょうします。', 'form': 'study-music', 'translation_en': 'I study while listening to music.'},
        {'ja': 'テレビを みながら ごはんを たべました。', 'form': 'eat-tv', 'translation_en': 'I ate while watching TV.'},
        {'ja': 'コーヒーを のみながら はなしました。', 'form': 'talk-drink', 'translation_en': 'We talked while drinking coffee.'},
    ],
    'n5-149': [  # 〜をください
        {'ja': 'みずを ください。', 'form': 'water-request', 'translation_en': 'Please give me water.'},
        {'ja': 'メニューを ください。', 'form': 'menu-request', 'translation_en': 'Please give me the menu.'},
        {'ja': 'これを ください。', 'form': 'this-request', 'translation_en': 'I\'ll have this, please.'},
    ],
    'n5-150': [  # 〜をおねがいします
        {'ja': 'コーヒーを おねがいします。', 'form': 'order-coffee', 'translation_en': 'Coffee, please.'},
        {'ja': 'メニューを おねがいします。', 'form': 'menu-please', 'translation_en': 'The menu, please.'},
        {'ja': 'タクシーを おねがいします。', 'form': 'taxi-please', 'translation_en': 'A taxi, please.'},
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
