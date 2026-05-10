"""Grammar Batch M (2026-05-11): G1 fifth pass. +30 patterns."""
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
    'n5-024': [  # か (or)
        {'ja': 'コーヒーか こうちゃを のみます。', 'form': 'or-binary', 'translation_en': "I'll drink coffee or tea."},
        {'ja': 'バスか でんしゃで いきます。', 'form': 'transport-or', 'translation_en': "I'll go by bus or train."},
        {'ja': 'いくか いかないか きめます。', 'form': 'whether-or-not', 'translation_en': "I'll decide whether to go or not."},
    ],
    'n5-027': [  # よね
        {'ja': 'おいしいですよね。', 'form': 'shared-tasty', 'translation_en': "It's tasty, isn't it?"},
        {'ja': 'たかいですよね。', 'form': 'shared-expensive', 'translation_en': "It's expensive, right?"},
        {'ja': 'いい てんきですよね。', 'form': 'shared-weather', 'translation_en': 'Nice weather, isn\'t it?'},
    ],
    'n5-030': [  # nominalizer の
        {'ja': 'ほんを よむのが すきです。', 'form': 'verb-noun-subj', 'translation_en': 'I like reading books.'},
        {'ja': 'にほんごを はなすのは むずかしいです。', 'form': 'verb-noun-topic', 'translation_en': "Speaking Japanese is difficult."},
        {'ja': 'りょうりを つくるのが じょうずです。', 'form': 'cook-skilled', 'translation_en': 'I am good at cooking.'},
    ],
    'n5-039': [  # これ/それ/あれ (duplicate)
        {'ja': 'これは わたしの ペンです。', 'form': 'near-possess', 'translation_en': 'This is my pen.'},
        {'ja': 'それは あなたの ほんですか。', 'form': 'near-listener-yn', 'translation_en': 'Is that your book?'},
        {'ja': 'あれは なんですか。', 'form': 'far-what', 'translation_en': 'What is that over there?'},
    ],
    'n5-041': [  # ここ/そこ/あそこ/どこ (duplicate)
        {'ja': 'ここで まちましょう。', 'form': 'here-wait', 'translation_en': "Let's wait here."},
        {'ja': 'そこに ねこが います。', 'form': 'there-cat', 'translation_en': 'There is a cat there.'},
        {'ja': 'あそこに スーパーが あります。', 'form': 'over-there-shop', 'translation_en': 'There is a supermarket over there.'},
    ],
    'n5-043': [  # こんな/そんな/あんな/どんな + N
        {'ja': 'こんな ほんが すきです。', 'form': 'this-kind-book', 'translation_en': 'I like this kind of book.'},
        {'ja': 'どんな たべものが すきですか。', 'form': 'what-kind-food', 'translation_en': 'What kind of food do you like?'},
        {'ja': 'そんな ことを いわないで ください。', 'form': 'that-kind-please-not', 'translation_en': "Please don't say such things."},
    ],
    'n5-045': [  # 何 (なに/なん) - duplicate of 017
        {'ja': 'なんじですか。', 'form': 'time-counter', 'translation_en': 'What time is it?'},
        {'ja': 'なにが いいですか。', 'form': 'what-good', 'translation_en': 'What would be good?'},
        {'ja': 'なにを かいますか。', 'form': 'what-buy', 'translation_en': 'What will you buy?'},
    ],
    'n5-046': [  # だれ/どなた (duplicate)
        {'ja': 'あの ひとは だれですか。', 'form': 'who-casual', 'translation_en': 'Who is that person?'},
        {'ja': 'どなたが やまだ先生ですか。', 'form': 'who-polite', 'translation_en': 'Who is the teacher Yamada?'},
        {'ja': 'これは だれの ですか。', 'form': 'whose-this', 'translation_en': 'Whose is this?'},
    ],
    'n5-048': [  # どこ
        {'ja': 'どこから きましたか。', 'form': 'origin-wh', 'translation_en': 'Where did you come from?'},
        {'ja': 'どこで かいましたか。', 'form': 'location-action', 'translation_en': 'Where did you buy it?'},
        {'ja': 'どこに すんで いますか。', 'form': 'residence', 'translation_en': 'Where do you live?'},
    ],
    'n5-050': [  # どう/いかが
        {'ja': 'りょこうは どうでしたか。', 'form': 'how-was-trip', 'translation_en': 'How was the trip?'},
        {'ja': 'コーヒーは いかがですか。', 'form': 'polite-offer-coffee', 'translation_en': 'How about some coffee?'},
        {'ja': 'おちゃは いかがですか。', 'form': 'polite-offer-tea', 'translation_en': 'How about some tea?'},
    ],
    'n5-051': [  # どうして/なぜ
        {'ja': 'どうして いきませんか。', 'form': 'why-not-go', 'translation_en': "Why aren't you going?"},
        {'ja': 'なぜ そう おもいますか。', 'form': 'why-think-so', 'translation_en': 'Why do you think so?'},
        {'ja': 'どうして おそかったですか。', 'form': 'why-late', 'translation_en': 'Why were you late?'},
    ],
    'n5-052': [  # どうやって
        {'ja': 'どうやって がっこうに いきますか。', 'form': 'how-go-school', 'translation_en': 'How do you go to school?'},
        {'ja': 'どうやって つくりますか。', 'form': 'how-make', 'translation_en': 'How do you make it?'},
        {'ja': 'どうやって よみますか。', 'form': 'how-read', 'translation_en': 'How do you read it?'},
    ],
    'n5-094': [  # 〜があります
        {'ja': 'にもつが たくさん あります。', 'form': 'many-luggage', 'translation_en': 'There is a lot of luggage.'},
        {'ja': 'しつもんが ありますか。', 'form': 'have-question', 'translation_en': 'Do you have a question?'},
        {'ja': 'たいせつな ものが あります。', 'form': 'important-thing', 'translation_en': 'There is an important thing.'},
    ],
    'n5-098': [  # 〜 placeholder (general particle slot)
        {'ja': 'これは わたしの ほんです。', 'form': 'identification', 'translation_en': 'This is my book.'},
        {'ja': 'やまださんは がくせいです。', 'form': 'profession', 'translation_en': 'Yamada-san is a student.'},
        {'ja': 'にほんは アジアに あります。', 'form': 'location-fact', 'translation_en': 'Japan is in Asia.'},
    ],
    'n5-106': [  # Noun + が ほしい
        {'ja': 'あたらしい パソコンが ほしいです。', 'form': 'want-noun-tech', 'translation_en': 'I want a new computer.'},
        {'ja': 'なにが いちばん ほしいですか。', 'form': 'want-question', 'translation_en': 'What do you want most?'},
        {'ja': 'おかねが ほしいです。', 'form': 'want-money', 'translation_en': 'I want money.'},
    ],
    'n5-109': [  # counter-question
        {'ja': 'りんごは いくつ ありますか。', 'form': 'count-tsu', 'translation_en': 'How many apples are there?'},
        {'ja': 'なんにん きましたか。', 'form': 'count-people', 'translation_en': 'How many people came?'},
        {'ja': 'ほんは なんさつ ありますか。', 'form': 'count-books', 'translation_en': 'How many books are there?'},
    ],
    'n5-110': [  # V + counter + V
        {'ja': 'ねこを にひき かいました。', 'form': 'bought-cats', 'translation_en': 'I bought two cats.'},
        {'ja': 'りんごを みっつ たべました。', 'form': 'ate-apples', 'translation_en': 'I ate three apples.'},
        {'ja': 'ノートを いっさつ かいました。', 'form': 'bought-notebook', 'translation_en': 'I bought one notebook.'},
    ],
    'n5-121': [  # そして
        {'ja': 'がっこうに いきました。そして、 ほんを よみました。', 'form': 'school-then-book', 'translation_en': 'I went to school. And then I read a book.'},
        {'ja': 'ごはんを たべました。そして、 ねました。', 'form': 'ate-then-slept', 'translation_en': 'I ate. And then I slept.'},
        {'ja': 'ほんを かいました。そして、 すぐ よみました。', 'form': 'bought-then-read', 'translation_en': 'I bought a book. And then I read it right away.'},
    ],
    'n5-135': [  # V-plain + N (relative clause)
        {'ja': 'よむ ほんが ありません。', 'form': 'no-book-to-read', 'translation_en': "I don't have a book to read."},
        {'ja': 'たべた りんごは あまかったです。', 'form': 'apple-i-ate', 'translation_en': 'The apple I ate was sweet.'},
        {'ja': 'きた ひとは ともだちです。', 'form': 'person-who-came', 'translation_en': 'The person who came is my friend.'},
    ],
    'n5-136': [  # Adjective + Noun (general)
        {'ja': 'おおきい ねこが います。', 'form': 'big-cat', 'translation_en': 'There is a big cat.'},
        {'ja': 'しずかな まちが すきです。', 'form': 'quiet-town', 'translation_en': 'I like quiet towns.'},
        {'ja': 'たかい ほんを かいました。', 'form': 'expensive-book', 'translation_en': 'I bought an expensive book.'},
    ],
    'n5-137': [  # Noun + の + Noun
        {'ja': 'にほんの ほんが すきです。', 'form': 'origin-book', 'translation_en': 'I like Japanese books.'},
        {'ja': 'やまださんの くるまは あれです。', 'form': 'person-car', 'translation_en': "Yamada-san's car is that one."},
        {'ja': 'きょうの しんぶんを よみました。', 'form': 'today-newspaper', 'translation_en': "I read today's newspaper."},
    ],
    'n5-146': [  # と言いました
        {'ja': 'やまださんは「あした きます」と いいました。', 'form': 'direct-quote', 'translation_en': 'Yamada-san said, "I will come tomorrow."'},
        {'ja': 'ははが くると いいました。', 'form': 'indirect-quote', 'translation_en': 'My mother said she would come.'},
        {'ja': 'なんと いいましたか。', 'form': 'what-said', 'translation_en': 'What did you say?'},
    ],
    'n5-147': [  # よく/ときどき/あまり/ぜんぜん
        {'ja': 'よく テレビを みます。', 'form': 'often-tv', 'translation_en': 'I often watch TV.'},
        {'ja': 'ときどき ともだちに あいます。', 'form': 'sometimes-friend', 'translation_en': 'I sometimes meet my friend.'},
        {'ja': 'あまり たべません。', 'form': 'not-much-eat', 'translation_en': "I don't eat much."},
    ],
    'n5-148': [  # いつも/たいてい/たまに
        {'ja': 'いつも はちじに おきます。', 'form': 'always-wake', 'translation_en': 'I always wake up at 8.'},
        {'ja': 'たいてい うちで ごはんを たべます。', 'form': 'usually-eat-home', 'translation_en': 'I usually eat at home.'},
        {'ja': 'たまに がいしょくします。', 'form': 'occasionally-eat-out', 'translation_en': 'I occasionally eat out.'},
    ],
    'n5-151': [  # いかがですか
        {'ja': 'おちゃは いかがですか。', 'form': 'offer-tea', 'translation_en': 'How about some tea?'},
        {'ja': 'これは いかがですか。', 'form': 'offer-this', 'translation_en': 'How about this one?'},
        {'ja': 'おかわりは いかがですか。', 'form': 'offer-refill', 'translation_en': 'How about a refill?'},
    ],
    'n5-152': [  # どうぞ/どうも/すみません/おねがいします
        {'ja': 'どうぞ おかけ ください。', 'form': 'invite-sit', 'translation_en': 'Please sit down.'},
        {'ja': 'どうも ありがとう ございます。', 'form': 'polite-thanks', 'translation_en': 'Thank you very much.'},
        {'ja': 'すみません、 みずを ください。', 'form': 'attention-request', 'translation_en': 'Excuse me, water please.'},
    ],
    'n5-153': [  # まだ + Vていません
        {'ja': 'まだ しゅくだいを して いません。', 'form': 'not-yet-homework', 'translation_en': "I haven't done my homework yet."},
        {'ja': 'まだ ごはんを たべて いません。', 'form': 'not-yet-eaten', 'translation_en': "I haven't eaten yet."},
        {'ja': 'まだ ともだちから へんじが きていません。', 'form': 'not-yet-reply', 'translation_en': "I haven't gotten a reply from my friend yet."},
    ],
    'n5-154': [  # もう + Vました
        {'ja': 'もう しゅくだいを しました。', 'form': 'already-homework', 'translation_en': "I've already done my homework."},
        {'ja': 'もう ごはんを たべました。', 'form': 'already-eaten', 'translation_en': "I've already eaten."},
        {'ja': 'もう がっこうに いきました。', 'form': 'already-went-school', 'translation_en': "I've already gone to school."},
    ],
    'n5-155': [  # が、(contrast)
        {'ja': 'にほんごは むずかしいですが、 おもしろいです。', 'form': 'difficulty-interest', 'translation_en': 'Japanese is difficult, but interesting.'},
        {'ja': 'たかいですが、 かいます。', 'form': 'expensive-buy', 'translation_en': "It's expensive, but I'll buy it."},
        {'ja': 'すきですが、 たべません。', 'form': 'like-not-eat', 'translation_en': "I like it, but I won't eat it."},
    ],
    'n5-156': [  # ね/よ
        {'ja': 'いい てんきですね。', 'form': 'weather-agreement', 'translation_en': 'Nice weather, isn\'t it?'},
        {'ja': 'これは おいしいですよ。', 'form': 'informing-good', 'translation_en': "This is tasty (you should know)."},
        {'ja': 'たいへんでしたね。', 'form': 'sympathy', 'translation_en': "That was hard, wasn't it?"},
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

# OOS
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
        for c in ex.get('ja',''):
            if is_kanji(c) and c not in N5:
                oos.setdefault(c, []).append(pid)
print(f'OOS: {len(oos)} -> {list(oos.keys())}')
