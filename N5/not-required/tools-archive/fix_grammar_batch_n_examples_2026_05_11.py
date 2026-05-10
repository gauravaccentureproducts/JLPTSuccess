"""Grammar Batch N (2026-05-11): G1 sixth pass — close to 178/178."""
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
    'n5-157': [  # でしょう
        {'ja': 'あした、 あめが ふるでしょう。', 'form': 'weather-conjecture', 'translation_en': 'It will probably rain tomorrow.'},
        {'ja': 'やまださんも くるでしょう。', 'form': 'person-likely-come', 'translation_en': 'Yamada-san will probably come too.'},
        {'ja': 'これは たかいでしょう。', 'form': 'price-conjecture', 'translation_en': 'This is probably expensive.'},
    ],
    'n5-158': [  # だろう
        {'ja': 'あした、 はれるだろう。', 'form': 'casual-weather', 'translation_en': "It'll probably be sunny tomorrow."},
        {'ja': 'もう ねたろうか。', 'form': 'casual-already-slept', 'translation_en': '(He) is probably already asleep.'},
        {'ja': 'たぶん だいじょうぶ だろう。', 'form': 'casual-ok', 'translation_en': "It's probably OK."},
    ],
    'n5-159': [  # ですね/ですよ
        {'ja': 'おいしい ですね。', 'form': 'shared-tasty', 'translation_en': "It's tasty, isn't it?"},
        {'ja': 'これは ほんとうに たかい ですよ。', 'form': 'really-expensive', 'translation_en': "This is really expensive (you should know)."},
        {'ja': 'にほんごは おもしろい ですね。', 'form': 'shared-interest', 'translation_en': "Japanese is interesting, isn't it?"},
    ],
    'n5-160': [  # Noun + の + あとで
        {'ja': 'がっこうの あとで、 あそびます。', 'form': 'after-school', 'translation_en': "I'll play after school."},
        {'ja': 'しごとの あとで、 のみに いきます。', 'form': 'after-work', 'translation_en': "After work, I'll go for a drink."},
        {'ja': 'ばんごはんの あとで、 テレビを みます。', 'form': 'after-dinner', 'translation_en': 'After dinner, I watch TV.'},
    ],
    'n5-161': [  # Noun + の + まえに
        {'ja': 'しごとの まえに、 コーヒーを のみます。', 'form': 'before-work-coffee', 'translation_en': 'Before work, I drink coffee.'},
        {'ja': 'ごはんの まえに、 てを あらいます。', 'form': 'before-meal-hands', 'translation_en': 'Before meals, I wash my hands.'},
        {'ja': 'にじの まえに きて ください。', 'form': 'before-2-come', 'translation_en': 'Please come before 2.'},
    ],
    'n5-162': [  # V + まえに
        {'ja': 'たべるまえに、 てを あらいます。', 'form': 'before-eating', 'translation_en': 'Before eating, I wash my hands.'},
        {'ja': 'ねるまえに、 ほんを よみます。', 'form': 'before-sleep-read', 'translation_en': 'Before sleeping, I read a book.'},
        {'ja': 'でかけるまえに、 でんわします。', 'form': 'before-out-call', 'translation_en': "Before going out, I'll call."},
    ],
    'n5-163': [  # V-た + あとで
        {'ja': 'たべた あとで、 おちゃを のみます。', 'form': 'after-eat-tea', 'translation_en': 'After eating, I drink tea.'},
        {'ja': 'べんきょうした あとで、 あそびます。', 'form': 'after-study-play', 'translation_en': "After studying, I'll play."},
        {'ja': 'おふろに はいった あとで、 ねます。', 'form': 'after-bath-sleep', 'translation_en': "After taking a bath, I'll sleep."},
    ],
    'n5-164': [  # ～さん
        {'ja': 'やまださんは がくせいです。', 'form': 'person-occupation', 'translation_en': 'Yamada-san is a student.'},
        {'ja': 'すずきさん、 おはよう ございます。', 'form': 'greeting-name', 'translation_en': 'Good morning, Suzuki-san.'},
        {'ja': 'たなかさんに あいました。', 'form': 'met-person', 'translation_en': 'I met Tanaka-san.'},
    ],
    'n5-165': [  # お～/ご～
        {'ja': 'おなまえは なんですか。', 'form': 'polite-name', 'translation_en': 'What is your name?'},
        {'ja': 'おちゃを どうぞ。', 'form': 'polite-tea', 'translation_en': 'Please have some tea.'},
        {'ja': 'ごかぞくは おげんき ですか。', 'form': 'polite-family', 'translation_en': 'How is your family?'},
    ],
    'n5-166': [  # いただきます/ごちそうさま
        {'ja': 'いただきます。', 'form': 'before-eating', 'translation_en': '(I humbly receive — said before eating.)'},
        {'ja': 'ごちそうさま でした。', 'form': 'after-eating', 'translation_en': '(Thank you for the meal — said after eating.)'},
        {'ja': 'おはよう ございます。', 'form': 'morning-greeting', 'translation_en': 'Good morning.'},
    ],
    'n5-168': [  # 〜たり〜たりする
        {'ja': 'やすみの ひは、 ほんを よんだり、 さんぽしたり します。', 'form': 'holiday-activities', 'translation_en': 'On my day off, I read books, take walks, etc.'},
        {'ja': 'パーティーで、 たべたり のんだり しました。', 'form': 'party', 'translation_en': 'At the party, we ate, drank, etc.'},
        {'ja': 'えいがを みたり、 おんがくを きいたり します。', 'form': 'entertainment', 'translation_en': 'I watch movies, listen to music, etc.'},
    ],
    'n5-169': [  # V-た + ことがある
        {'ja': 'にほんに いったことが あります。', 'form': 'experience-japan', 'translation_en': 'I have been to Japan.'},
        {'ja': 'すしを たべたことが あります。', 'form': 'experience-food', 'translation_en': 'I have eaten sushi.'},
        {'ja': 'やまださんに あったことが ありますか。', 'form': 'experience-question', 'translation_en': 'Have you ever met Yamada-san?'},
    ],
    'n5-170': [  # V-た + ほうがいい
        {'ja': 'はやく ねた ほうが いいですよ。', 'form': 'advice-sleep', 'translation_en': "You should sleep early."},
        {'ja': 'やさいを たべた ほうが いいです。', 'form': 'advice-vegetables', 'translation_en': 'You should eat vegetables.'},
        {'ja': 'びょういんに いった ほうが いいです。', 'form': 'advice-hospital', 'translation_en': 'You should go to the hospital.'},
    ],
    'n5-171': [  # V-ない + ほうがいい
        {'ja': 'おさけを のまない ほうが いいですよ。', 'form': 'advice-no-alcohol', 'translation_en': "You shouldn't drink alcohol."},
        {'ja': 'たばこを すわない ほうが いいです。', 'form': 'advice-no-smoke', 'translation_en': "You shouldn't smoke."},
        {'ja': 'むりを しない ほうが いいです。', 'form': 'advice-no-overdo', 'translation_en': "You shouldn't overdo it."},
    ],
    'n5-172': [  # 〜なくてもいい
        {'ja': 'あした、 こなくても いいです。', 'form': 'permission-not-come', 'translation_en': "You don't have to come tomorrow."},
        {'ja': 'しゅくだいを しなくても いいですか。', 'form': 'permission-no-homework', 'translation_en': "Is it OK not to do homework?"},
        {'ja': 'いそがなくても いいです。', 'form': 'permission-no-hurry', 'translation_en': "You don't have to hurry."},
    ],
    'n5-173': [  # 〜なくてはいけない
        {'ja': 'もう いかなくては いけません。', 'form': 'must-go', 'translation_en': "I have to go now."},
        {'ja': 'やくそくを まもらなくては いけません。', 'form': 'must-keep-promise', 'translation_en': 'I have to keep my promise.'},
        {'ja': 'はやく ねなくては いけません。', 'form': 'must-sleep-early', 'translation_en': 'I have to sleep early.'},
    ],
    'n5-174': [  # 〜なくてはならない
        {'ja': 'もっと べんきょうしなくては なりません。', 'form': 'must-study-more', 'translation_en': 'I must study more.'},
        {'ja': 'やくそくを まもらなくては なりません。', 'form': 'must-keep-promise-formal', 'translation_en': 'I must keep my promise.'},
        {'ja': 'はやく かえらなくては なりません。', 'form': 'must-return-early', 'translation_en': 'I must return early.'},
    ],
    'n5-175': [  # 〜ないといけない
        {'ja': 'もう いかないと いけません。', 'form': 'must-go-now', 'translation_en': 'I have to go now.'},
        {'ja': 'やさいを たべないと いけません。', 'form': 'must-eat-veggies', 'translation_en': 'I have to eat vegetables.'},
        {'ja': 'おかねを はらわないと いけません。', 'form': 'must-pay', 'translation_en': 'I have to pay.'},
    ],
    'n5-176': [  # 〜なくちゃ/〜なきゃ
        {'ja': 'もう いかなくちゃ。', 'form': 'casual-must-go', 'translation_en': "I've gotta go."},
        {'ja': 'はやく ねなきゃ。', 'form': 'casual-must-sleep', 'translation_en': "I've gotta sleep early."},
        {'ja': 'べんきょうしなくちゃ。', 'form': 'casual-must-study', 'translation_en': "I've gotta study."},
    ],
    'n5-177': [  # V-stem + すぎる
        {'ja': 'たべすぎました。', 'form': 'ate-too-much', 'translation_en': 'I ate too much.'},
        {'ja': 'のみすぎました。', 'form': 'drank-too-much', 'translation_en': 'I drank too much.'},
        {'ja': 'たかすぎます。', 'form': 'too-expensive', 'translation_en': "It's too expensive."},
    ],
    'n5-178': [  # V-plain + つもりだ
        {'ja': 'あした、 がっこうに いくつもりです。', 'form': 'plan-go-school', 'translation_en': "I plan to go to school tomorrow."},
        {'ja': 'なつやすみに、 にほんに いくつもりです。', 'form': 'plan-japan', 'translation_en': "I plan to go to Japan during summer vacation."},
        {'ja': 'こんばん、 ともだちに あうつもりです。', 'form': 'plan-meet', 'translation_en': "I plan to meet a friend tonight."},
    ],
    'n5-179': [  # って
        {'ja': 'やまださんって やさしい ね。', 'form': 'casual-quotation', 'translation_en': 'Yamada-san is kind, isn\'t (he/she)?'},
        {'ja': 'これって なんですか。', 'form': 'casual-what', 'translation_en': 'What is this?'},
        {'ja': 'あめが ふるって。', 'form': 'casual-hearsay', 'translation_en': '(I heard) it\'s going to rain.'},
    ],
    'n5-180': [  # V-stem + かた
        {'ja': 'この りょうりの つくりかたを おしえて ください。', 'form': 'way-to-cook', 'translation_en': 'Please teach me how to make this dish.'},
        {'ja': 'よみかたが わかりません。', 'form': 'way-to-read', 'translation_en': "I don't know how to read it."},
        {'ja': 'つかいかたを せつめいします。', 'form': 'way-to-use', 'translation_en': "I'll explain how to use it."},
    ],
    'n5-181': [  # なあ
        {'ja': 'たかいなあ。', 'form': 'exclamation-expensive', 'translation_en': "Wow, it's expensive!"},
        {'ja': 'きれいだなあ。', 'form': 'exclamation-beautiful', 'translation_en': "How beautiful!"},
        {'ja': 'いいなあ。', 'form': 'exclamation-nice', 'translation_en': "How nice!"},
    ],
    'n5-182': [  # V-plain + な (prohibitive)
        {'ja': 'はいるな。', 'form': 'prohibition-enter', 'translation_en': "Don't enter."},
        {'ja': 'はしるな。', 'form': 'prohibition-run', 'translation_en': "Don't run."},
        {'ja': 'たべるな。', 'form': 'prohibition-eat', 'translation_en': "Don't eat (it)."},
    ],
    'n5-183': [  # Q + か/も compounds (general)
        {'ja': 'なにか たべましたか。', 'form': 'something-eat-q', 'translation_en': 'Did you eat anything?'},
        {'ja': 'だれも きませんでした。', 'form': 'no-one-came', 'translation_en': 'No one came.'},
        {'ja': 'どこかへ いきましたか。', 'form': 'somewhere-go-q', 'translation_en': 'Did you go anywhere?'},
    ],
    'n5-185': [  # だれか/だれも
        {'ja': 'だれか きましたか。', 'form': 'anyone-came', 'translation_en': 'Did anyone come?'},
        {'ja': 'だれも いませんでした。', 'form': 'no-one-here', 'translation_en': 'No one was here.'},
        {'ja': 'だれかが でんわを かけて きました。', 'form': 'someone-called', 'translation_en': 'Someone called.'},
    ],
    'n5-186': [  # どこか/どこも
        {'ja': 'どこかへ いきましょうか。', 'form': 'somewhere-go', 'translation_en': "Shall we go somewhere?"},
        {'ja': 'どこにも いきませんでした。', 'form': 'nowhere-went', 'translation_en': "I didn't go anywhere."},
        {'ja': 'どこかで みた ことが あります。', 'form': 'seen-somewhere', 'translation_en': "I've seen it somewhere."},
    ],
    'n5-187': [  # いつか/いつも
        {'ja': 'いつか にほんに いきたいです。', 'form': 'someday-japan', 'translation_en': 'I want to go to Japan someday.'},
        {'ja': 'いつも コーヒーを のみます。', 'form': 'always-coffee', 'translation_en': 'I always drink coffee.'},
        {'ja': 'いつか また あいましょう。', 'form': 'meet-again', 'translation_en': "Let's meet again someday."},
    ],
    'n5-188': [  # V + ことができます
        {'ja': 'にほんごを はなすことが できます。', 'form': 'can-speak', 'translation_en': 'I can speak Japanese.'},
        {'ja': 'うんてんすることが できますか。', 'form': 'can-drive', 'translation_en': 'Can you drive?'},
        {'ja': 'はやく はしることが できません。', 'form': 'cannot-run-fast', 'translation_en': "I can't run fast."},
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
