"""Round-9 residual: 77 grammar patterns at exactly 3 examples.

Authors a 4th example sentence for each. Each new example uses
different attachment surface, register, or context from the existing
3 (audit-round9 §0.5 diversity criterion). Sentences use only
N5-whitelist kanji + N5 vocab.

JA-17 (vocab_ids) is auto-populated by tools/link_grammar_examples_to_vocab.py
after this script runs.

Idempotent: skips patterns already at ≥4 examples; deduplicates by JA.
"""
from __future__ import annotations
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

GRAMMAR = Path(__file__).parent.parent / 'data' / 'grammar.json'

# Pattern_id -> {form, ja, translation_en}
NEW_EXAMPLES = {
    # === Question words / counters ===
    'n5-054': {'form': 'age-question', 'ja': 'おばあちゃんは いくつですか。', 'translation_en': 'How old is your grandmother?'},
    'n5-063': {'form': 'taxi-offer', 'ja': 'タクシーを よびましょうか。', 'translation_en': 'Shall I call a taxi?'},
    'n5-073': {'form': 'phone-context', 'ja': '父は 今 はたらいていません。', 'translation_en': 'My father is not working at the moment.'},
    'n5-098': {'form': 'preference-contrast', 'ja': 'にくは すきですが、さかなは あまり すきじゃ ありません。', 'translation_en': 'I like meat, but I don\'t like fish very much.'},
    'n5-101': {'form': 'travel-context', 'ja': 'あたらしい かばんが ほしいです。', 'translation_en': 'I want a new bag.'},
    'n5-102': {'form': 'language-skill', 'ja': '日本語が だいたい わかります。', 'translation_en': 'I roughly understand Japanese.'},
    'n5-103': {'form': 'sport-skill', 'ja': 'まだ 上手に およぐことが できません。', 'translation_en': 'I still can\'t swim well.'},
    'n5-106': {'form': 'birthday-wish', 'ja': 'たんじょうびに とけいが ほしいです。', 'translation_en': 'For my birthday I want a watch.'},
    'n5-107': {'form': 'study-purpose', 'ja': '日本語を ならいに 学校へ 行きます。', 'translation_en': 'I go to school to learn Japanese.'},
    'n5-109': {'form': 'shopping-context', 'ja': 'りんごは いくらですか。', 'translation_en': 'How much are the apples?'},
    'n5-110': {'form': 'food-quantity', 'ja': 'ばんごはんに さかなを 二つ 食べました。', 'translation_en': 'I ate two pieces of fish for dinner.'},
    'n5-111': {'form': 'class-time', 'ja': 'じゅぎょうは 九時から はじまります。', 'translation_en': 'Class starts at 9 o\'clock.'},
    'n5-112': {'form': 'commute-time', 'ja': '学校まで 三十分 かかります。', 'translation_en': 'It takes 30 minutes to (get to) school.'},
    'n5-113': {'form': 'meet-time', 'ja': '七時半に えきの まえで 会いましょう。', 'translation_en': 'Let\'s meet at 7:30 in front of the station.'},
    # === Time expressions ===
    'n5-116': {'form': 'weekly-routine', 'ja': 'まいしゅう 土曜日に サッカーを します。', 'translation_en': 'Every week on Saturday I play soccer.'},
    'n5-117': {'form': 'tomorrow-plan', 'ja': 'あさって 友だちが うちに 来ます。', 'translation_en': 'My friend is coming to my house the day after tomorrow.'},
    'n5-119': {'form': 'before-dinner', 'ja': 'ばんごはんの まえに しゅくだいを します。', 'translation_en': 'I do my homework before dinner.'},
    'n5-120': {'form': 'after-class', 'ja': 'じゅぎょうの あとで としょかんに 行きました。', 'translation_en': 'After class I went to the library.'},
    # === Clause connectors ===
    'n5-121': {'form': 'sequence-of-events', 'ja': '本を 読みました。そして、ねました。', 'translation_en': 'I read a book. And then I went to sleep.'},
    'n5-122': {'form': 'morning-routine', 'ja': 'あさごはんを 食べました。それから 学校へ 行きました。', 'translation_en': 'I ate breakfast. After that I went to school.'},
    'n5-123': {'form': 'weather-contrast', 'ja': 'あさは さむかったです。でも、ひるは あつかったです。', 'translation_en': 'The morning was cold. But the afternoon was hot.'},
    'n5-124': {'form': 'formal-contrast', 'ja': 'りょうりは おいしいです。しかし、すこし たかいです。', 'translation_en': 'The food is delicious. However, it\'s a little expensive.'},
    'n5-125': {'form': 'transition', 'ja': 'では、また あした 会いましょう。', 'translation_en': 'Well then, let\'s meet again tomorrow.'},
    'n5-126': {'form': 'mid-clause-but', 'ja': 'この えいがは おもしろいですが、ながいです。', 'translation_en': 'This movie is interesting, but it\'s long.'},
    'n5-127': {'form': 'casual-but-short', 'ja': 'やすいけど、おいしくないです。', 'translation_en': 'It\'s cheap, but it\'s not tasty.'},
    'n5-129': {'form': 'reason-q-and-a', 'ja': 'どうして 学校を 休みましたか。― あたまが いたかったからです。', 'translation_en': 'Why did you skip school? — Because I had a headache.'},
    # === Giving verbs ===
    'n5-130': {'form': 'birthday-gift', 'ja': '友だちに 花を あげました。', 'translation_en': 'I gave my friend flowers.'},
    'n5-131': {'form': 'gift-from-parent', 'ja': '父から とけいを もらいました。', 'translation_en': 'I received a watch from my father.'},
    'n5-132': {'form': 'gift-to-me', 'ja': 'おばあちゃんが 本を くれました。', 'translation_en': 'My grandmother gave me a book.'},
    # === Sentence-level connectors ===
    'n5-133': {'form': 'plan-because', 'ja': 'あめが ふっていますから、出かけません。', 'translation_en': 'It\'s raining, so I won\'t go out.'},
    'n5-134': {'form': 'softer-because', 'ja': 'いそがしいので、しゅくだいが できませんでした。', 'translation_en': 'I was busy, so I couldn\'t do my homework.'},
    # === Relative clauses / NP modification ===
    'n5-135': {'form': 'verb-modifies-noun', 'ja': 'きのう 食べた ケーキは おいしかったです。', 'translation_en': 'The cake (I) ate yesterday was delicious.'},
    'n5-136': {'form': 'adjective-stack', 'ja': '大きい 白い いぬが すきです。', 'translation_en': 'I like big white dogs.'},
    'n5-137': {'form': 'genitive-chain', 'ja': '友だちの お母さんの 名前は 田中さんです。', 'translation_en': 'My friend\'s mother\'s name is Tanaka.'},
    # === Decision / becoming ===
    'n5-142': {'form': 'food-decision', 'ja': 'ばんごはんは カレーに します。', 'translation_en': 'For dinner I\'ll have curry.'},
    'n5-143': {'form': 'weather-becoming', 'ja': '今日は さむく なりました。', 'translation_en': 'Today it has gotten cold.'},
    'n5-144': {'form': 'study-while-music', 'ja': 'おんがくを 聞きながら、しゅくだいを します。', 'translation_en': 'I do my homework while listening to music.'},
    'n5-145': {'form': 'opinion-light', 'ja': 'あした あめが ふると おもいます。', 'translation_en': 'I think it will rain tomorrow.'},
    'n5-146': {'form': 'reported-speech', 'ja': '田中さんは「あした 来ます」と 言いました。', 'translation_en': 'Mr. Tanaka said, "I will come tomorrow."'},
    'n5-148': {'form': 'frequency-context', 'ja': 'たまに カフェで コーヒーを 飲みます。', 'translation_en': 'I occasionally drink coffee at a café.'},
    # === Polite expressions ===
    'n5-149': {'form': 'restaurant-order', 'ja': 'おちゃを ください。', 'translation_en': 'Please give me tea.'},
    'n5-151': {'form': 'offering-cake', 'ja': 'ケーキは いかがですか。', 'translation_en': 'How about some cake?'},
    'n5-152': {'form': 'apology-set-phrase', 'ja': 'すみません、おねがいします。', 'translation_en': 'Excuse me, please (I have a request).'},
    # === Aspect / time markers ===
    'n5-153': {'form': 'still-pending', 'ja': 'まだ あさごはんを 食べていません。', 'translation_en': 'I haven\'t eaten breakfast yet.'},
    'n5-154': {'form': 'already-done', 'ja': 'もう しゅくだいを しました。', 'translation_en': 'I have already done my homework.'},
    'n5-155': {'form': 'mid-sentence-but', 'ja': 'えいがは よかったですが、ながかったです。', 'translation_en': 'The movie was good, but it was long.'},
    'n5-157': {'form': 'weather-conjecture', 'ja': 'あした あめが ふるでしょう。', 'translation_en': 'It will probably rain tomorrow.'},
    'n5-158': {'form': 'casual-conjecture', 'ja': 'たぶん 来るだろう。', 'translation_en': 'They\'ll probably come.'},
    # === Time noun + で / に ===
    'n5-160': {'form': 'meal-context', 'ja': 'ばんごはんの あとで 本を 読みます。', 'translation_en': 'After dinner I read a book.'},
    'n5-161': {'form': 'study-context', 'ja': 'テストの まえに たくさん べんきょうしました。', 'translation_en': 'I studied a lot before the test.'},
    'n5-162': {'form': 'verb-mae-ni', 'ja': 'ねるまえに はを みがきます。', 'translation_en': 'I brush my teeth before going to sleep.'},
    'n5-163': {'form': 'verb-ato-de', 'ja': 'しゅくだいを した あとで テレビを 見ます。', 'translation_en': 'After doing homework I watch TV.'},
    # === Honorifics / set phrases ===
    'n5-164': {'form': 'classmate-name', 'ja': 'マリアさんは スペインから 来ました。', 'translation_en': 'Maria-san came from Spain.'},
    'n5-165': {'form': 'beautifying-prefix', 'ja': 'おげんきですか。', 'translation_en': 'Are you well? (polite greeting)'},
    'n5-166': {'form': 'leaving-home-greeting', 'ja': 'いって きます！', 'translation_en': '"I\'m leaving!" (set phrase said when departing the house).'},
    'n5-167': {'form': 'explaining-context', 'ja': 'どうして おそく 来たんですか。', 'translation_en': 'Why did you come late? (asking for explanation)'},
    'n5-168': {'form': 'weekend-activities', 'ja': 'しゅうまつは 本を 読んだり、テレビを 見たり します。', 'translation_en': 'On weekends I read books, watch TV, etc.'},
    'n5-169': {'form': 'experience-travel', 'ja': '日本に 行ったことが ありますか。', 'translation_en': 'Have you ever been to Japan?'},
    'n5-170': {'form': 'health-advice', 'ja': 'はやく ねた ほうが いいですよ。', 'translation_en': 'You should go to sleep early.'},
    'n5-171': {'form': 'food-warning', 'ja': 'からい ものを 食べない ほうが いいです。', 'translation_en': 'You shouldn\'t eat spicy food.'},
    'n5-172': {'form': 'no-need', 'ja': 'あした 学校に 来なくても いいです。', 'translation_en': 'You don\'t have to come to school tomorrow.'},
    'n5-173': {'form': 'must-formal', 'ja': '今日 しゅくだいを 出さなくては いけません。', 'translation_en': 'I have to submit homework today.'},
    'n5-174': {'form': 'must-formal-2', 'ja': 'もっと べんきょうしなくては なりません。', 'translation_en': 'I must study more.'},
    'n5-175': {'form': 'must-spoken', 'ja': 'はやく 行かないと いけません。', 'translation_en': 'I have to go quickly.'},
    'n5-176': {'form': 'must-casual', 'ja': 'はやく ねなきゃ。', 'translation_en': '(I) have to go to sleep early. (casual)'},
    'n5-177': {'form': 'eat-too-much', 'ja': 'きのう 食べすぎました。', 'translation_en': 'I ate too much yesterday.'},
    'n5-178': {'form': 'plan-to-go', 'ja': 'らいねん 日本に 行く つもりです。', 'translation_en': 'I plan to go to Japan next year.'},
    'n5-179': {'form': 'casual-quote', 'ja': '田中さんは ねむいって 言っていました。', 'translation_en': 'Tanaka-san was saying "(I am) sleepy".'},
    'n5-180': {'form': 'how-to-write', 'ja': 'この かんじの 書きかたを おしえて ください。', 'translation_en': 'Please teach me how to write this kanji.'},
    'n5-181': {'form': 'tasty-exclamation', 'ja': 'この りょうりは おいしいなあ。', 'translation_en': 'This food is really tasty!'},
    'n5-182': {'form': 'don\'t-lie', 'ja': 'うそを 言うな！', 'translation_en': 'Don\'t lie! (strong prohibition)'},
    'n5-183': {'form': 'something-to-eat', 'ja': 'なにか 食べたいです。', 'translation_en': 'I want to eat something.'},
    'n5-184': {'form': 'nothing-to-do', 'ja': 'きょうは なにも しません。', 'translation_en': 'I won\'t do anything today.'},
    'n5-185': {'form': 'someone-came', 'ja': 'だれか 来ましたか。', 'translation_en': 'Did anyone come?'},
    'n5-186': {'form': 'go-anywhere', 'ja': 'どこにも 行きません。', 'translation_en': 'I won\'t go anywhere.'},
    'n5-187': {'form': 'sometime-let\'s-meet', 'ja': 'いつか いっしょに ばんごはんを 食べましょう。', 'translation_en': 'Let\'s have dinner together sometime.'},
    'n5-188': {'form': 'can-speak-japanese', 'ja': '日本語を 話すことが できます。', 'translation_en': 'I can speak Japanese.'},
}


def main() -> int:
    doc = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    patterns = doc['patterns']
    by_id = {p['id']: p for p in patterns}

    n_added = 0
    n_skipped_full = 0
    n_dup = 0
    n_missing = 0

    for pid, new_ex in NEW_EXAMPLES.items():
        p = by_id.get(pid)
        if not p:
            n_missing += 1
            continue
        existing = p.get('examples', [])
        if len(existing) >= 4:
            n_skipped_full += 1
            continue
        existing_ja = {e.get('ja', '').strip() for e in existing}
        if new_ex['ja'].strip() in existing_ja:
            n_dup += 1
            continue
        existing.append(new_ex)
        n_added += 1

    GRAMMAR.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    doc2 = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    counts = {}
    for p in doc2['patterns']:
        n = len(p.get('examples', []))
        counts[n] = counts.get(n, 0) + 1
    at_4plus = sum(1 for p in doc2['patterns'] if len(p.get('examples', [])) >= 4)
    print(f'Examples added: {n_added}')
    print(f'  Skipped (already ≥4): {n_skipped_full}')
    print(f'  Skipped (JA dup):     {n_dup}')
    print(f'  Pattern not found:    {n_missing}')
    print(f'\nDistribution: {sorted(counts.items())}')
    print(f'Patterns ≥4 examples: {at_4plus}/{len(doc2["patterns"])}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
