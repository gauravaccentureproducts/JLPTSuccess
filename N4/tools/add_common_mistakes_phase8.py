"""Phase 8 (2026-05-03): author `common_mistakes` for the 56 high-
confusion grammar patterns the teacher-perspective audit (T-7) flagged
as missing them.

Each entry follows the existing structure:
  { "wrong": "<learner error>", "right": "<corrected>", "why": "<brief>" }

Mistakes target the most common N5-learner pitfalls per pattern:
  - particle confusions (に/へ, は/が, など…)
  - register / form mismatches
  - homophone particle vs adnominal usage
  - kosoado distance vs form
  - verb-form irregulars
  - obligation/should-not double-negative idioms

Idempotent: re-running skips entries that already have any mistake.
JA-13 enforced post-run for kanji scope.
"""
import io, json, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

def M(wrong, right, why):
    return {'wrong': wrong, 'right': right, 'why': why}

ADDITIONS = {
    # Question particle か (yes/no question)
    'n5-023': [
        M('げんきか？', 'げんきですか。', 'Plain か without ですか drops to rough/masculine register; use ですか in polite speech.'),
        M('行きますか？', '行きますか。', 'Japanese sentence-final question particle is か, not ？; the ？ is optional and Western. Period (。) is the canonical end-mark in formal text.'),
    ],
    # Question particle か (alternative-listing "or")
    'n5-024': [
        M('コーヒー、おちゃ', 'コーヒーか おちゃ', 'For "or", connect with か (e.g., A か B). Comma alone reads as a list, not an alternative.'),
    ],
    # ～の (nominalizer "the act of doing X")
    'n5-028': [
        M('日本語を 話す が すきです。', '日本語を 話すのが すきです。',
          'Bare verbs cannot be subjects of すき. Add の (or こと) to nominalize: 話すのが すき.'),
    ],
    # この/その/あの/どの + Noun (adnominal demonstrative)
    'n5-040': [
        M('これ 本は おもしろいです。', 'この 本は おもしろいです。',
          'これ is a standalone pronoun; cannot precede a noun. Use この + Noun for "this X".'),
        M('それの 本', 'その 本', 'No の after その/この/あの/どの when a noun directly follows.'),
    ],
    # なん / なに (what)
    'n5-045': [
        M('なに ですか。', '何ですか。 (なん ですか。)',
          'Before だ/です/の or counters, 何 reads なん. Standalone before particles を/が, it reads なに.'),
        M('なに 時に 行きますか。', '何時に 行きますか。 (なんじに)',
          'In counter compounds (なんじ, なんにち, なんさい), the reading is なん, not なに.'),
    ],
    # どう / いかが
    'n5-050': [
        M('げんき いかが？', 'お げんきですか。 (or げんき どう？)',
          'いかが is the polite/respectful form of どう, used with です. Plain casual speech uses どう, not いかが.'),
    ],
    # どうやって (how / by what means)
    'n5-052': [
        M('どう 学校に 行きますか。 (asking method)', 'どうやって 学校に 行きますか。',
          'どう alone often asks "how is it?" (state/quality). For "by what means", use どうやって.'),
    ],
    # なんがつ なんにち (what month / what day)
    'n5-057': [
        M('何月日ですか。', '何月 何日ですか。',
          'Month and day are asked separately: 何月 (なんがつ) and 何日 (なんにち), each with its own counter.'),
    ],
    # Verb-ましょうか (offer / propose)
    'n5-063': [
        M('行こうか？ (formal context)', '行きましょうか。',
          'Plain volitional 行こうか is casual; in polite contexts use ～ましょうか for offers/proposals.'),
    ],
    # ～は～にあります / います (location of existence)
    'n5-093': [
        M('本は つくえに います。', '本は つくえに あります。',
          'いる is for animate (people, animals); ある is for inanimate (objects). 本 is inanimate → あります.'),
        M('ねこは ベッドの 上に あります。', 'ねこは ベッドの 上に います。',
          'Animate ねこ (cat) takes います, not あります.'),
    ],
    # ～があります (something exists)
    'n5-094': [
        M('テストは あした います。', 'あした テストが あります。',
          'For events/scheduled things (test, meeting, party), use ～が あります. The subject is the event, not its time.'),
    ],
    # ～より～のほうが (X-er than Y)
    'n5-096': [
        M('なつは ふゆより 大きい。', 'なつは ふゆより あつい です。',
          'Comparison adjective should fit the dimension being compared. (Also, dictionary form alone is too informal; use です.)'),
        M('AのほうがBより 大きいです。', 'BよりAのほうが 大きいです。',
          'より marks the standard (B), のほうが marks the topic (A). Standard order: BよりAのほうが ～.'),
    ],
    # ～と～と、どちらが～ですか (which of A or B?)
    'n5-097': [
        M('AかBか、どちらが すきですか。', 'AとBと、どちらが すきですか。',
          'For "which of A or B?", use と...と to list, then どちら. か...か is grammatical but と...と is the standard frame for comparison questions.'),
    ],
    # Verb-stem + たくないです (don't want to)
    'n5-105': [
        M('行きたくありません。 (correct but rigid)', '行きたくないです。 (more natural)',
          'Both are correct; ～たくないです is more natural in conversation. ～たくありません is hyper-formal.'),
        M('食べたくない です。', '食べたくないです。',
          'たくない is one unit; no space between くない and です.'),
    ],
    # Noun + が ほしいです (I want X)
    'n5-106': [
        M('わたしは 新しい かばんを ほしいです。', 'わたしは 新しい かばんが ほしいです。',
          'ほしい takes が, not を. The desired thing is the が-marked target.'),
        M('田中さんは 車が ほしいです。', '田中さんは 車を ほしがって います。',
          'ほしい can only describe SPEAKER\'s desire. For third-person desires, use ほしがる.'),
    ],
    # Counter questions (いくつ / いくら / なんにん etc.)
    'n5-109': [
        M('りんごは いくらですか。 (asking quantity)', 'りんごは いくつ ありますか。',
          'いくら asks price; いくつ asks count of objects (no fixed counter).'),
        M('かぞくは なんにん ですか。', 'かぞくは なんにん いますか。',
          'For people-count, pair with います (animate existence verb).'),
    ],
    # ～じはん (half past N)
    'n5-113': [
        M('三時 三十分 (in casual speech)', '三時はん',
          'In casual speech, 三十分 (sanjuppun) is replaced by はん (han). 三時はん = "3:30" / "half past 3".'),
    ],
    # ～から～まで (from-to)
    'n5-114': [
        M('九時まで 五時から しごとです。', '九時から 五時まで しごとです。',
          'Order is start-end: から first, then まで. Reversed order is ungrammatical.'),
    ],
    # に (multi-purpose particle)
    'n5-115': [
        M('学校で 行きます。', '学校に 行きます。',
          'For destination of motion verbs (行く, 来る, かえる), use に (or へ), not で. で marks the location of action.'),
        M('七時で おきます。', '七時に おきます。',
          'For points in time, use に, not で. (Days of week, months, clock times.)'),
    ],
    # いま / すぐ / もう / まだ (time adverbs)
    'n5-118': [
        M('まだ 食べました。', 'もう 食べました。',
          'もう = "already" (with affirmative past); まだ = "still / not yet" (often with negative). Don\'t mix.'),
        M('もう 食べていません。', 'まだ 食べていません。',
          'For "haven\'t eaten yet", use まだ + negative-progressive (まだ食べていません), not もう + negative.'),
    ],
    # それから (and then / after that)
    'n5-122': [
        M('シャワーを あびました。それから ねます。', 'シャワーを あびました。それから ねました。',
          'それから connects sequential past events; both clauses should match in tense.'),
    ],
    # でも (but / however - sentence-initial)
    'n5-123': [
        M('わたしは 学生です。でも 田中さんも 学生です。', 'わたしは 学生です。それに 田中さんも 学生です。',
          'でも introduces contrast/exception; for "moreover/additionally" use それに.'),
    ],
    # しかし (formal "however")
    'n5-124': [
        M('むずかしかったです。しかし、できました。 (in casual speech)', 'むずかしかったです。でも、できました。',
          'しかし is formal/written; in casual conversation, でも is more natural.'),
    ],
    # では / じゃ (well then; in that case)
    'n5-125': [
        M('じゃ、はじめましょう。 (in formal meeting)', 'では、はじめましょう。',
          'じゃ is the colloquial contraction of では; in formal contexts (meetings, speeches), prefer では.'),
    ],
    # どうして～か。～から。(Q-and-A reason pattern)
    'n5-129': [
        M('どうして 来ませんでしたか。―ねつが あって。', 'どうして 来ませんでしたか。―ねつが あったからです。',
          'Reason answers in formal speech end in ～からです, not just the bare clause.'),
    ],
    # ～に～をあげます (give to)
    'n5-130': [
        M('わたしは 田中さんが 本を あげました。', 'わたしは 田中さんに 本を あげました。',
          'Recipient is marked with に, not が. Pattern: [giver] は [recipient] に [object] を あげる.'),
    ],
    # から (because - sentence connector)
    'n5-133': [
        M('あついから まどを あけて くださいから。', 'あついから、まどを あけて ください。',
          'から goes ONCE between cause and result, not at the end of both clauses.'),
        M('雨が ふっています、ですから 行きません。 (overly formal)', '雨が ふっていますから、行きません。',
          'In one sentence, から attaches directly to the cause clause; ですから is for stand-alone "therefore" at sentence start.'),
    ],
    # Noun + の + Noun (modifier の noun)
    'n5-137': [
        M('日本 学校', '日本の 学校',
          'Two nouns require の between them in modifier-modifier-of-noun position. Direct-juxtaposed compounds (日本人, 日本語) are exceptions where の is dropped by convention.'),
    ],
    # ～にします (decide on / choose)
    'n5-142': [
        M('コーヒーを します。', 'コーヒーに します。',
          '"Choose / decide on X" uses に, not を. を します means "do X" (action verb).'),
    ],
    # ～と言いました (said that ~)
    'n5-146': [
        M('田中さんは 行くを 言いました。', '田中さんは 行くと 言いました。',
          'Quotative particle is と, not を. Quoted clause stays in plain form before と (not 行くを).'),
    ],
    # いつも / たいてい / たまに (frequency)
    'n5-148': [
        M('いつも 行きません。 (intent: "I never go")', '行きません。 / ぜんぜん 行きません。',
          'いつも is "always" — does not pair with negation. Use ぜんぜん or just the negative verb for "never".'),
    ],
    # ～をください (please give me)
    'n5-149': [
        M('みず ください。', 'みずを ください。',
          'を is required between noun and ください in standard speech. Drop is colloquial only.'),
    ],
    # ～をおねがいします (please / I would like)
    'n5-150': [
        M('コーヒーを ください。 (in restaurant ordering)', 'コーヒーを おねがいします。',
          'Both work, but おねがいします is more polite/standard for ordering at a restaurant or making polite requests.'),
    ],
    # ～はいかがですか (how about / would you like)
    'n5-151': [
        M('おちゃは どうですか。 (offering to a customer)', 'おちゃは いかがですか。',
          'いかが is the polite form of どう. When offering to customers / superiors, use いかが.'),
    ],
    # どうぞ / どうも / すみません / おねがいします (set phrases)
    'n5-152': [
        M('ありがとう、 どうぞ。 (thanking)', 'ありがとう、 どうも。 / どうも、 ありがとう。',
          'どうぞ = "please go ahead / here you are" (offering). For "thanks", pair ありがとう with どうも, not どうぞ.'),
    ],
    # もう + Verb-ました (already done)
    'n5-154': [
        M('もう 食べます。', 'もう 食べました。',
          'もう = "already" requires past (～ました). Present tense もう食べます would mean "I\'ll eat now", not "already ate".'),
    ],
    # ～が、～ (clause-connector "but")
    'n5-155': [
        M('むずかしいです。が おもしろいです。', 'むずかしいですが、おもしろいです。',
          'Mid-sentence が attaches directly to the first clause; do NOT split into two sentences. Period before が breaks the connection.'),
    ],
    # ～でしょう (probably / right?)
    'n5-157': [
        M('あした 雨ですでしょう。', 'あした 雨でしょう。',
          'でしょう attaches directly to the noun/adj/verb-plain form, NOT to です. です + でしょう is double-copula.'),
    ],
    # ～ですね / ～ですよ (tag particles)
    'n5-159': [
        M('いい てんきですよね。 (overuse)', 'いい てんきですね。 (or よ, not both)',
          'よ asserts new info; ね seeks agreement. Stacking よね is colloquial and overused — pick one in clean speech.'),
    ],
    # Noun + の + あとで (after Noun)
    'n5-160': [
        M('しごと あとで 行きます。', 'しごとの あとで 行きます。',
          'Noun + あと requires の. (Verb-た + あとで does NOT take の: 食べた あとで.)'),
    ],
    # Noun + の + まえに (before Noun)
    'n5-161': [
        M('ごはん まえに てを あらいます。', 'ごはんの まえに てを あらいます。',
          'Noun + まえ requires の. (Verb-plain + まえに does NOT take の: 食べる まえに.)'),
    ],
    # いただきます / ごちそうさま / おはようございます etc.
    'n5-166': [
        M('ごはんを 食べる まえに 「ごちそうさま」', 'ごはんを 食べる まえに 「いただきます」',
          'いただきます = before eating; ごちそうさま = after eating. Don\'t reverse them.'),
    ],
    # Verb-た + ことがある (have done before)
    'n5-169': [
        M('日本に 行く ことが あります。 (intent: "have been to Japan")', '日本に 行った ことが あります。',
          'Past experience requires the た-form before ことがある. Plain form 行く + ことがある means "sometimes go (habit)", a different meaning.'),
    ],
    # Verb-た + ほうがいい (should do)
    'n5-170': [
        M('行く ほうが いいです。', '行った ほうが いいです。',
          'Recommendations use the た-form: ～たほうがいい. Plain form ～ほうがいい is grammatical but sounds like a comparison ("the going option is better"), not advice.'),
    ],
    # Verb-ない + ほうがいい (shouldn't do)
    'n5-171': [
        M('行かなく ほうが いいです。', '行かない ほうが いいです。',
          'Negative ほうがいい uses the plain ない form (行かない), not the て-form ない (行かなくて).'),
    ],
    # ～なくてもいい (don't have to)
    'n5-172': [
        M('行かなくて いいです。', '行かなくても いいです。',
          'The set phrase requires も between なくて and いい: ～なくても いい. Without も it sounds like "don\'t go and it\'s fine".'),
    ],
    # ～なくてはいけない (must)
    'n5-173': [
        M('行きなくては いけません。', '行かなくては いけません。',
          '～なくては attaches to the negative-stem (ない-form base): 行か + なくては. NOT to the polite-stem 行き.'),
    ],
    # ～なくてはならない (must - formal)
    'n5-174': [
        M('行かないと ならない。', '行かなくては ならない。 / 行かないと いけない。',
          '～と pairs with いけない, not ならない. Mismatch: ～なくては + ならない/いけない (both OK); ～ないと + いけない (only).'),
    ],
    # ～ないといけない (must - common spoken)
    'n5-175': [
        M('しゅくだいを しないと なりません。', 'しゅくだいを しないと いけません。',
          '～ないと idiomatically pairs with いけない/いけません (more colloquial), not ならない. (See n5-174.)'),
    ],
    # Verb-plain + つもり (intend to)
    'n5-178': [
        M('行きます つもりです。', '行く つもりです。',
          'つもり attaches to the PLAIN form (行く), not the polite form (行きます).'),
    ],
    # Verb-stem + ～かた (way of doing)
    'n5-180': [
        M('読むかた', '読みかた',
          '～かた attaches to the verb-STEM (ます-form base), not the dictionary form. 読む → 読み + かた.'),
        M('食べるかた', '食べかた',
          'For Group-2 verbs, drop the final る before adding かた: 食べる → 食べ + かた.'),
    ],
    # Question word + か / も compounds (general)
    'n5-183': [
        M('なに か 食べません。', 'なにも 食べません。',
          'With negative verbs, use なにも (nothing). なにか + negative is ungrammatical.'),
    ],
    # なにか / なにも (something / nothing)
    'n5-184': [
        M('なにか 食べません。', 'なにも 食べません。',
          'なにか pairs with affirmative ("eat something"); なにも with negative ("eat nothing"). Don\'t mix.'),
        M('なにも 食べたいです。', 'なにか 食べたいです。',
          '"I want to eat something" is affirmative — use なにか, not なにも.'),
    ],
    # だれか / だれも (someone / nobody)
    'n5-185': [
        M('だれか 来ませんでした。', 'だれも 来ませんでした。',
          'With negative verbs, use だれも (nobody). だれか + negative shifts meaning to "didn\'t someone come?", which is awkward in N5.'),
    ],
    # どこか / どこも (somewhere / nowhere)
    'n5-186': [
        M('どこか 行きません。', 'どこも 行きません。',
          'With negative, どこも = "(go) nowhere". どこか + negative is ungrammatical.'),
        M('どこも 行きたいです。', 'どこか 行きたいです。',
          '"Want to go somewhere" is affirmative wish — use どこか.'),
    ],
    # いつか / いつも (sometime / always)
    'n5-187': [
        M('いつも 日本に 行きたいです。 (intent: "someday")', 'いつか 日本に 行きたいです。',
          'いつも = "always" (every time); いつか = "someday / sometime in the future". For aspirations, use いつか.'),
        M('いつか コーヒーを 飲みます。 (intent: "always")', 'いつも コーヒーを 飲みます。',
          'For habit "always drink coffee", use いつも. いつか implies a single future occasion.'),
    ],
}


def main() -> int:
    gpath = ROOT / 'data' / 'grammar.json'
    data = json.loads(gpath.read_text(encoding='utf-8'))
    added = []
    skipped = []
    not_found = set(ADDITIONS.keys())
    for p in data['patterns']:
        pid = p.get('id')
        if pid not in ADDITIONS:
            continue
        not_found.discard(pid)
        existing = p.get('common_mistakes') or []
        new_entries = ADDITIONS[pid]
        # Idempotency: skip if any of the new entries already exists by `wrong`
        existing_wrong = {e.get('wrong') for e in existing}
        actually_new = [e for e in new_entries if e['wrong'] not in existing_wrong]
        if not actually_new:
            skipped.append(pid)
            continue
        existing.extend(actually_new)
        p['common_mistakes'] = existing
        added.append((pid, len(actually_new)))
    if added:
        gpath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
    print(f'Added common_mistakes to {len(added)} patterns:')
    for pid, n in added:
        print(f'  {pid}: +{n}')
    if skipped:
        print(f'Skipped (already present): {len(skipped)}')
    if not_found:
        print(f'WARNING - patterns not found: {sorted(not_found)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())

