"""IMP-124 finalisation: top up the remaining 34 patterns to >=7
examples each. Idempotent — skips examples whose JA already exists."""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Pattern_id -> list of additional examples (keep adding until >=7)
EXAMPLES = {
    'n5-021': [
        {'ja': 'えきから 学校まで 二十分です。', 'translation_en': "It's 20 minutes from the station to school."},
    ],
    'n5-023': [
        {'ja': 'これは あなたの ほんですか。', 'translation_en': 'Is this your book?'},
        {'ja': 'もう 食べましたか。', 'translation_en': 'Have you eaten yet?'},
    ],
    'n5-026': [
        {'ja': 'がんばってくださいよ。', 'translation_en': 'Please do your best, you know!'},
        {'ja': 'これ、おいしいですよ。', 'translation_en': 'This is tasty, you know!'},
    ],
    'n5-036': [
        {'ja': '六時ごろに 来てください。', 'translation_en': 'Please come around 6 oclock.'},
        {'ja': 'はる ごろに 日本へ 行きます。', 'translation_en': 'I will go to Japan around spring.'},
    ],
    'n5-038': [
        {'ja': 'みんなに 一つずつ あげます。', 'translation_en': "I'll give one to each person."},
        {'ja': '少しずつ にほんごが 上手に なります。', 'translation_en': 'Little by little, my Japanese is getting better.'},
    ],
    'n5-039': [
        {'ja': 'これは 何ですか。', 'translation_en': 'What is this?'},
        {'ja': 'それは わたしの ほんです。', 'translation_en': "That's my book."},
    ],
    'n5-040': [
        {'ja': 'この りょうりは おいしいです。', 'translation_en': 'This dish is delicious.'},
        {'ja': 'あの 大きい たてものは 学校です。', 'translation_en': 'That big building is the school.'},
    ],
    'n5-043': [
        {'ja': 'こんな りょうりが すきです。', 'translation_en': 'I like this kind of food.'},
        {'ja': 'どんな 本を 読みますか。', 'translation_en': 'What kind of books do you read?'},
    ],
    'n5-045': [
        {'ja': '何時ですか。', 'translation_en': 'What time is it?'},
        {'ja': 'なには すきですか。', 'translation_en': 'What do you like?'},
    ],
    'n5-063': [
        {'ja': 'もう 帰りましょうか。', 'translation_en': 'Shall we go home now?'},
    ],
    'n5-066': [
        {'ja': 'にほんごを 話さない。', 'translation_en': "I don't speak Japanese.", 'tier': 'late_n5'},
        {'ja': 'お金が ないから、行かない。', 'translation_en': "I don't have money, so I won't go.", 'tier': 'late_n5'},
    ],
    'n5-108': [
        {'ja': 'りんごを 三つ 買いました。', 'translation_en': 'I bought three apples.'},
        {'ja': 'えんぴつが 五本 あります。', 'translation_en': 'There are five pencils.'},
    ],
    'n5-112': [
        {'ja': '十五ふん 待ちました。', 'translation_en': 'I waited 15 minutes.'},
    ],
    'n5-114': [
        {'ja': '一時から 五時まで しごとを します。', 'translation_en': 'I work from 1 to 5.'},
        {'ja': '月よう日から きんよう日まで 学校です。', 'translation_en': 'School is Monday to Friday.'},
        {'ja': 'うちから 学校まで 十分です。', 'translation_en': "It's 10 minutes from home to school."},
    ],
    'n5-115': [
        {'ja': '七時に おきます。', 'translation_en': 'I get up at 7 oclock.'},
        {'ja': '日よう日に こうえんへ 行きます。', 'translation_en': "I'll go to the park on Sunday."},
    ],
    'n5-119': [
        {'ja': '五分まえに 来ました。', 'translation_en': 'I came 5 minutes before.'},
    ],
    'n5-120': [
        {'ja': '十分あとに きてください。', 'translation_en': 'Please come 10 minutes later.'},
        {'ja': 'しごとの あとで えいがを 見ます。', 'translation_en': "I'll watch a movie after work."},
    ],
    'n5-121': [
        {'ja': 'うちで ごはんを 食べました。そして、ねました。', 'translation_en': 'I ate at home. Then I slept.'},
        {'ja': 'べんきょうしました。そして、しゅくだいを しました。', 'translation_en': 'I studied. Then I did homework.'},
    ],
    'n5-122': [
        {'ja': 'コーヒーを のみました。それから、しごとを はじめました。', 'translation_en': 'I drank coffee. Then I started work.'},
        {'ja': 'えいがを 見ました。それから、ばんごはんを 食べました。', 'translation_en': 'I watched a movie. Then I ate dinner.'},
    ],
    'n5-123': [
        {'ja': 'たかいです。でも、おいしいです。', 'translation_en': "It's expensive. But it's delicious."},
    ],
    'n5-124': [
        {'ja': 'いそがしいです。しかし、たのしいです。', 'translation_en': "I'm busy. However, it's enjoyable."},
        {'ja': 'やすかったです。しかし、よく ありません。', 'translation_en': 'It was cheap. However, the quality is not good.'},
    ],
    'n5-130': [
        {'ja': 'ともだちに ほんを あげました。', 'translation_en': 'I gave a book to my friend.'},
        {'ja': '父に ネクタイを あげます。', 'translation_en': 'I will give a tie to my father.'},
    ],
    'n5-133': [
        {'ja': 'いそがしいから、行きません。', 'translation_en': "I'm busy, so I won't go."},
        {'ja': 'おいしいから、また 食べたいです。', 'translation_en': "It's delicious, so I want to eat it again."},
        {'ja': 'にほんごが むずかしいから、まいにち べんきょうします。', 'translation_en': 'Japanese is hard, so I study every day.'},
    ],
    'n5-136': [
        {'ja': '大きい 本を 買いました。', 'translation_en': 'I bought a big book.'},
        {'ja': 'おもしろい えいがを 見ました。', 'translation_en': 'I watched an interesting movie.'},
        {'ja': 'やさしい 先生は たなかさんです。', 'translation_en': 'The kind teacher is Ms. Tanaka.'},
    ],
    'n5-137': [
        {'ja': 'にほんごの 先生は しんせつです。', 'translation_en': 'The Japanese teacher is kind.'},
        {'ja': 'ともだちの くるまは あかいです。', 'translation_en': "My friend's car is red."},
        {'ja': 'わたしの いえの ちかくに こうえんが あります。', 'translation_en': "There's a park near my house."},
    ],
    'n5-160': [
        {'ja': 'しごとの あとで さんぽします。', 'translation_en': "I'll take a walk after work."},
        {'ja': 'えいがの あとで しょくじします。', 'translation_en': "I'll have a meal after the movie."},
    ],
    'n5-161': [
        {'ja': 'ねる まえに しゅくだいを します。', 'translation_en': "I'll do homework before bed."},
    ],
    'n5-163': [
        {'ja': 'ごはんを 食べた あとで、おちゃを のみました。', 'translation_en': 'After eating, I drank tea.'},
        {'ja': 'しゅくだいを した あとで、テレビを 見ました。', 'translation_en': 'After doing homework, I watched TV.'},
    ],
    'n5-165': [
        {'ja': 'おちゃを ください。', 'translation_en': 'Please give me tea.'},
        {'ja': 'お時間 ありますか。', 'translation_en': 'Do you have time?'},
    ],
    'n5-169': [
        {'ja': 'にほんへ 行ったことが ありますか。', 'translation_en': 'Have you ever been to Japan?'},
        {'ja': 'すしを 食べたことが あります。', 'translation_en': "I've eaten sushi before."},
    ],
    'n5-173': [
        {'ja': 'はやく 学校へ 行かなくては いけません。', 'translation_en': 'I have to go to school early.'},
        {'ja': 'もっと べんきょうしなくては いけません。', 'translation_en': 'I have to study more.'},
    ],
    'n5-180': [
        {'ja': 'えきへの 行きかたを おしえてください。', 'translation_en': 'Please tell me how to get to the station.'},
    ],
    'n5-183': [
        {'ja': 'なにか 飲みますか。', 'translation_en': 'Will you drink something?'},
        {'ja': 'だれも 来ませんでした。', 'translation_en': 'Nobody came.'},
        {'ja': 'どこかへ 出かけますか。', 'translation_en': 'Are you going somewhere?'},
    ],
    'n5-187': [
        {'ja': 'いつか 日本へ 行きたいです。', 'translation_en': 'Someday I want to go to Japan.'},
        {'ja': 'いつも 七時に おきます。', 'translation_en': 'I always get up at 7 oclock.'},
    ],
}

# ---- Verify N5 kanji compliance ----
kdata = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
kentries = kdata.get('entries', kdata) if isinstance(kdata, dict) else kdata
whitelist = set()
for k in kentries:
    g = k.get('glyph') or (k.get('id', '').split('.')[-1])
    if g:
        whitelist.add(g)

# ---- Apply ----
grammar_path = ROOT / 'data' / 'grammar.json'
data = json.loads(grammar_path.read_text(encoding='utf-8'))
patterns = data['patterns']

added = 0
oos_skipped = []
for p in patterns:
    pid = p['id']
    if pid not in EXAMPLES:
        continue
    new_exs = EXAMPLES[pid]
    examples = p.get('examples') or []
    existing_ja = {ex.get('ja') for ex in examples if ex.get('ja')}
    for ex in new_exs:
        if ex['ja'] in existing_ja:
            continue  # idempotent
        oos = [c for c in ex['ja'] if '一' <= c <= '鿿' and c not in whitelist]
        if oos:
            oos_skipped.append((pid, ex['ja'][:30], oos))
            continue
        new_ex = {
            'ja': ex['ja'],
            'translation_en': ex['translation_en'],
            'provenance': 'llm_curated',
        }
        examples.append(new_ex)
        existing_ja.add(ex['ja'])
        added += 1
    p['examples'] = examples

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final coverage
from collections import Counter
counts = Counter(len(p.get('examples') or []) for p in patterns)
at7 = sum(c for n, c in counts.items() if n >= 7)
at5 = sum(c for n, c in counts.items() if n >= 5)
print(f'New examples added:       {added}')
print(f'Out-of-scope skipped:     {len(oos_skipped)}')
if oos_skipped:
    for pid, ja, oos in oos_skipped[:8]:
        print(f'  {pid}: {ja} {oos}')
print()
print(f'Coverage:')
print(f'  >=5: {at5}/{len(patterns)} ({100*at5/len(patterns):.0f}%)')
print(f'  >=7: {at7}/{len(patterns)} ({100*at7/len(patterns):.0f}%)')
