"""Grammar Batch I (2026-05-10):
G1 expansion. Add 3 examples to ~30 high-priority patterns to bring
example count from 7 to 10+. After applying, run the existing
link_grammar_examples_to_vocab.py to populate vocab_ids.
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

# Each entry: pid -> [3 example dicts]
# Example dict: {ja, form, translation_en}
# vocab_ids and pitch_marks will be auto-filled by linker scripts.
NEW_EXAMPLES = {
    'n5-001': [  # です／ます
        {'ja': 'これは ほんです。', 'form': 'affirmative', 'translation_en': 'This is a book.'},
        {'ja': 'わたしは がくせいでは ありません。', 'form': 'negative', 'translation_en': "I'm not a student."},
        {'ja': 'まいにち えいがを みます。', 'form': 'habitual', 'translation_en': 'I watch movies every day.'},
    ],
    'n5-002': [  # は (topic)
        {'ja': 'これは ペンです。', 'form': 'topic-introduction', 'translation_en': 'This is a pen.'},
        {'ja': 'にほんごは おもしろいです。', 'form': 'descriptive', 'translation_en': 'Japanese is interesting.'},
        {'ja': 'わたしは コーヒーを のみません。', 'form': 'contrast-implicit', 'translation_en': "I don't drink coffee (others might)."},
    ],
    'n5-003': [  # が (subject/new info)
        {'ja': 'ねこが います。', 'form': 'existence-new', 'translation_en': 'There is a cat.'},
        {'ja': 'だれが きましたか。', 'form': 'wh-question-subject', 'translation_en': 'Who came?'},
        {'ja': 'やまださんが せんせいです。', 'form': 'identification-answer', 'translation_en': 'Yamada-san is the teacher.'},
    ],
    'n5-004': [  # を
        {'ja': 'ほんを よみます。', 'form': 'object-direct', 'translation_en': 'I read a book.'},
        {'ja': 'コーヒーを かいました。', 'form': 'past', 'translation_en': 'I bought coffee.'},
        {'ja': 'おんがくを きいています。', 'form': 'progressive', 'translation_en': 'I am listening to music.'},
    ],
    'n5-005': [  # に (destination/time)
        {'ja': 'がっこうに いきます。', 'form': 'destination', 'translation_en': 'I go to school.'},
        {'ja': 'はちじに おきました。', 'form': 'time-point', 'translation_en': 'I got up at 8.'},
        {'ja': 'ともだちに あいました。', 'form': 'recipient', 'translation_en': 'I met (with) my friend.'},
    ],
    'n5-007': [  # で
        {'ja': 'バスで がっこうに いきます。', 'form': 'means', 'translation_en': 'I go to school by bus.'},
        {'ja': 'としょかんで べんきょうします。', 'form': 'location-of-action', 'translation_en': 'I study at the library.'},
        {'ja': 'はしで ごはんを たべます。', 'form': 'instrument', 'translation_en': 'I eat with chopsticks.'},
    ],
    'n5-008': [  # と (with / and)
        {'ja': 'ともだちと えいがを みました。', 'form': 'with-companion', 'translation_en': 'I watched a movie with my friend.'},
        {'ja': 'コーヒーと こうちゃを かいました。', 'form': 'list-exhaustive', 'translation_en': 'I bought coffee and tea.'},
        {'ja': 'ははと はなしました。', 'form': 'mutual-action', 'translation_en': 'I talked with my mother.'},
    ],
    'n5-009': [  # から (from)
        {'ja': 'にほんから きました。', 'form': 'origin', 'translation_en': 'I came from Japan.'},
        {'ja': 'いちじから べんきょうします。', 'form': 'starting-time', 'translation_en': "I'll study from 1 o'clock."},
        {'ja': 'ともだちから プレゼントを もらいました。', 'form': 'source-of-receiving', 'translation_en': 'I received a present from my friend.'},
    ],
    'n5-013': [  # も
        {'ja': 'わたしも がくせいです。', 'form': 'inclusive', 'translation_en': 'I am also a student.'},
        {'ja': 'ねこも います。', 'form': 'existence-additional', 'translation_en': 'There is a cat too.'},
        {'ja': 'ほんも ノートも かいました。', 'form': 'both', 'translation_en': 'I bought both books and notebooks.'},
    ],
    'n5-058': [  # Vます
        {'ja': 'まいにち がっこうに いきます。', 'form': 'habitual', 'translation_en': 'I go to school every day.'},
        {'ja': 'いま、ほんを よみます。', 'form': 'near-future', 'translation_en': "I'll read the book now."},
        {'ja': 'あした、ともだちに あいます。', 'form': 'future', 'translation_en': "I'll meet my friend tomorrow."},
    ],
    'n5-066': [  # Vない
        {'ja': 'コーヒーを のまない。', 'form': 'plain-negative', 'translation_en': "I don't drink coffee."},
        {'ja': 'あした、いかない。', 'form': 'future-negative', 'translation_en': "I won't go tomorrow."},
        {'ja': 'これを たべない ほうが いい。', 'form': 'in-advice', 'translation_en': "Better not to eat this."},
    ],
    'n5-067': [  # Vた
        {'ja': 'きのう、えいがを みた。', 'form': 'plain-past', 'translation_en': 'I watched a movie yesterday.'},
        {'ja': 'もう ごはんを たべた。', 'form': 'completed', 'translation_en': "I've already eaten."},
        {'ja': 'どこに いったの？', 'form': 'past-question', 'translation_en': 'Where did you go?'},
    ],
    'n5-069': [  # Vて
        {'ja': 'ごはんを たべて、ねます。', 'form': 'sequence', 'translation_en': "I'll eat and then go to bed."},
        {'ja': 'こうえんに いって、はしりました。', 'form': 'past-sequence', 'translation_en': 'I went to the park and ran.'},
        {'ja': 'ほんを よんで、わかりました。', 'form': 'cause-result', 'translation_en': 'I read the book and understood.'},
    ],
    'n5-071': [  # てください
        {'ja': 'みずを ください。', 'form': 'request-direct', 'translation_en': 'Please give me water.'},
        {'ja': 'ゆっくり はなして ください。', 'form': 'speed-request', 'translation_en': 'Please speak slowly.'},
        {'ja': 'もういちど 言って ください。', 'form': 'repeat-request', 'translation_en': 'Please say it again.'},
    ],
    'n5-072': [  # Vています (progressive)
        {'ja': 'いま、ごはんを たべて います。', 'form': 'progressive-now', 'translation_en': "I'm eating now."},
        {'ja': 'がっこうで べんきょうして います。', 'form': 'ongoing-state', 'translation_en': "I'm studying at school."},
        {'ja': 'ははは でんわを かけて います。', 'form': 'in-progress-other', 'translation_en': 'My mother is on the phone.'},
    ],
    'n5-079': [  # い-Adj + です
        {'ja': 'この ほんは おもしろいです。', 'form': 'descriptive', 'translation_en': 'This book is interesting.'},
        {'ja': 'きょうは あついです。', 'form': 'state', 'translation_en': "It's hot today."},
        {'ja': 'にほんごは むずかしいです。', 'form': 'evaluation', 'translation_en': 'Japanese is difficult.'},
    ],
    'n5-080': [  # い-Adj negative
        {'ja': 'この ほんは おもしろくないです。', 'form': 'negative-descriptive', 'translation_en': "This book isn't interesting."},
        {'ja': 'きょうは あつくないです。', 'form': 'negative-weather', 'translation_en': "It isn't hot today."},
        {'ja': 'たかくないです。', 'form': 'negative-price', 'translation_en': "It's not expensive."},
    ],
    'n5-085': [  # na-Adj + です
        {'ja': 'この まちは しずかです。', 'form': 'descriptive', 'translation_en': 'This town is quiet.'},
        {'ja': 'やまださんは しんせつです。', 'form': 'personality', 'translation_en': 'Yamada-san is kind.'},
        {'ja': 'にほんごが すきです。', 'form': 'preference', 'translation_en': 'I like Japanese.'},
    ],
    'n5-090': [  # あります
        {'ja': 'つくえに ほんが あります。', 'form': 'existence-inanimate', 'translation_en': "There's a book on the desk."},
        {'ja': 'きょう、テストが あります。', 'form': 'event', 'translation_en': "There's a test today."},
        {'ja': 'おかねが あまり ありません。', 'form': 'negative-quantity', 'translation_en': "I don't have much money."},
    ],
    'n5-091': [  # います
        {'ja': 'うちに ねこが います。', 'form': 'animate-existence', 'translation_en': "There's a cat at my house."},
        {'ja': 'きょうしつに がくせいが います。', 'form': 'people-location', 'translation_en': 'There are students in the classroom.'},
        {'ja': 'ともだちが いません。', 'form': 'absence', 'translation_en': "I don't have any friends here."},
    ],
    'n5-099': [  # 〜が好き
        {'ja': 'わたしは すしが すきです。', 'form': 'preference-positive', 'translation_en': 'I like sushi.'},
        {'ja': 'スポーツが あまり すきじゃ ありません。', 'form': 'mild-dislike', 'translation_en': "I don't really like sports."},
        {'ja': 'どんな おんがくが すきですか。', 'form': 'preference-question', 'translation_en': 'What kind of music do you like?'},
    ],
    'n5-100': [  # 〜が上手
        {'ja': 'やまださんは えいごが じょうずです。', 'form': 'skill-praise', 'translation_en': 'Yamada-san is good at English.'},
        {'ja': 'うたが あまり じょうずじゃ ありません。', 'form': 'modesty', 'translation_en': "I'm not very good at singing."},
        {'ja': 'りょうりが じょうずに なりたいです。', 'form': 'aspiration', 'translation_en': 'I want to become good at cooking.'},
    ],
    'n5-101': [  # ほしい
        {'ja': 'あたらしい くるまが ほしいです。', 'form': 'desire-noun', 'translation_en': 'I want a new car.'},
        {'ja': 'なにが いちばん ほしいですか。', 'form': 'question', 'translation_en': 'What do you want most?'},
        {'ja': 'いまは なにも ほしくないです。', 'form': 'negative-want', 'translation_en': "I don't want anything right now."},
    ],
    'n5-104': [  # たい
        {'ja': 'すしを たべたいです。', 'form': 'desire-verb', 'translation_en': 'I want to eat sushi.'},
        {'ja': 'にほんに いきたいです。', 'form': 'travel-desire', 'translation_en': 'I want to go to Japan.'},
        {'ja': 'なにが のみたいですか。', 'form': 'question', 'translation_en': 'What do you want to drink?'},
    ],
    'n5-117': [  # きょう/あした
        {'ja': 'きょうは あついです。', 'form': 'today-state', 'translation_en': "It's hot today."},
        {'ja': 'あした、がっこうに いきます。', 'form': 'tomorrow-plan', 'translation_en': "I'll go to school tomorrow."},
        {'ja': 'きのう、ともだちに あいました。', 'form': 'yesterday-past', 'translation_en': 'I met my friend yesterday.'},
    ],
    'n5-130': [  # 〜にあげます
        {'ja': 'ともだちに ほんを あげました。', 'form': 'past-give', 'translation_en': 'I gave a book to my friend.'},
        {'ja': 'ははに はなを あげる つもりです。', 'form': 'plan-give', 'translation_en': 'I plan to give my mother flowers.'},
        {'ja': 'なにを あげましたか。', 'form': 'question', 'translation_en': 'What did you give?'},
    ],
    'n5-167': [  # んです
        {'ja': 'おなかが いたいんです。', 'form': 'explanation', 'translation_en': "(The thing is,) my stomach hurts."},
        {'ja': 'どうして いかないんですか。', 'form': 'question-explanation', 'translation_en': 'Why aren\'t you going?'},
        {'ja': 'がくせいなんです。', 'form': 'identity-explanation', 'translation_en': "(It's because) I'm a student."},
    ],
    'n5-184': [  # なにか／なにも
        {'ja': 'なにか たべたいです。', 'form': 'something-positive', 'translation_en': 'I want to eat something.'},
        {'ja': 'なにも たべませんでした。', 'form': 'nothing-negative', 'translation_en': "I didn't eat anything."},
        {'ja': 'なにか いいことが ありましたか。', 'form': 'something-question', 'translation_en': 'Did anything good happen?'},
    ],
    'n5-058': [  # Vます (already had — keeping but skipping if dup)
        {'ja': 'まいにち がっこうに いきます。', 'form': 'habitual', 'translation_en': 'I go to school every day.'},
        {'ja': 'まいばん ほんを よみます。', 'form': 'evening-habit', 'translation_en': 'I read books every evening.'},
        {'ja': 'にちようびに テレビを みます。', 'form': 'weekly', 'translation_en': 'I watch TV on Sundays.'},
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
        continue  # already at target
    # Mark each new example with provenance
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

# Stats
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
        for k in ('ja','translation_en'):
            v = ex.get(k,'')
            for c in str(v):
                if is_kanji(c) and c not in N5:
                    oos.setdefault(c, []).append(pid)
print(f'OOS in batch I additions: {len(oos)} -> {list(oos.keys())}')
