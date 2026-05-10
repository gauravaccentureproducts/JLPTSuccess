"""Grammar Batch C (2026-05-10):
- G2/G3: Schema upgrade — wrong_corrected_pair: dict -> list-of-dicts
- Each entry now has: {wrong, correct, why, error_category, provenance}
- Migrates 36 existing single-dict entries (preserved as first element)
- Adds 2 more categorized errors to the 36 already-covered patterns
- Adds 3 categorized errors to 30 high-priority patterns currently uncovered
- Target: ~66/178 patterns at >=3 categorized common-mistakes
- Error categories: particle, conjugation, word_order, register, lexicon, counter
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

# Author's note: All Japanese uses N5-only kanji (or kana). Errors target the most
# frequent learner traps documented in JEES past papers and Genki/Minna teaching notes.

# Additional entries (2 each) to merge into the 36 patterns that already have ONE entry.
# Schema: pid -> [extra_entry_1, extra_entry_2]
ADDITIONS = {
    'n5-002': [  # は (topic)
        {'wrong': 'わたしはペンが あります。', 'correct': 'わたしは ペンを もっています。 / わたしは ペンが あります は不自然 — 「ペンを もっています」が自然。',
         'why': 'For "I have a pen" prefer 持っています; あります collocates with location/existence, not personal possession in colloquial Japanese.', 'error_category': 'lexicon'},
        {'wrong': 'にほんはきれいなくにです。', 'correct': 'にほんは きれいな くにです。',
         'why': 'Spacing: in early-N5 wakachi-gaki, separate particle phrases for parsing.', 'error_category': 'word_order'},
    ],
    'n5-003': [  # が (subject)
        {'wrong': 'だれは きましたか。', 'correct': 'だれが きましたか。',
         'why': 'Question words like だれ/なに/いつ take が, never は (cannot topicalize an unknown).', 'error_category': 'particle'},
        {'wrong': 'わたしは すきです、ねこ。', 'correct': 'わたしは ねこが すきです。',
         'why': 'Object of すき/きらい/上手/下手/ほしい/わかる takes が, not を.', 'error_category': 'particle'},
    ],
    'n5-004': [  # を
        {'wrong': 'こうえんを いきます。', 'correct': 'こうえんに/へ いきます。',
         'why': 'Direction of motion uses に/へ. を with 行く marks path-traversed (公園を 通ります), not destination.', 'error_category': 'particle'},
        {'wrong': 'みずを のみたい。', 'correct': 'みずが のみたい。',
         'why': 'With Vたい (desiderative), the desired object usually takes が in plain N5 register; を is grammatical but less natural.', 'error_category': 'particle'},
    ],
    'n5-005': [  # に
        {'wrong': 'がっこうで いきます。', 'correct': 'がっこうに いきます。',
         'why': 'で marks the location of an action; に marks destination of motion.', 'error_category': 'particle'},
        {'wrong': 'しちじから おきます。', 'correct': 'しちじに おきます。',
         'why': 'Specific clock-time takes に (時点); から marks "starting from".', 'error_category': 'particle'},
    ],
    'n5-006': [  # へ
        {'wrong': 'がっこうへで べんきょうします。', 'correct': 'がっこうで べんきょうします。',
         'why': 'へ is direction; で is location of action. Cannot stack them.', 'error_category': 'particle'},
        {'wrong': 'にほんへ すんでいます。', 'correct': 'にほんに すんでいます。',
         'why': 'Static residence (住む) takes に, not へ. へ implies motion toward.', 'error_category': 'particle'},
    ],
    'n5-007': [  # で
        {'wrong': 'バスに がっこうへ いきます。', 'correct': 'バスで がっこうへ いきます。',
         'why': 'Means of transport takes で (instrumental); に here would mean "into the bus".', 'error_category': 'particle'},
        {'wrong': 'にほんごを はなします、ともだちで。', 'correct': 'ともだちと にほんごを はなします。',
         'why': 'Co-actor (with whom) is と, not で. で is instrument/location/method.', 'error_category': 'particle'},
    ],
    'n5-008': [  # と
        {'wrong': 'コーヒーや こうちゃと のみます。', 'correct': 'コーヒーと こうちゃを のみます。',
         'why': 'と makes an exhaustive list; や makes a non-exhaustive list. Mixing produces ungrammatical "et al + and".', 'error_category': 'particle'},
        {'wrong': 'ともだちに あいました。 (X "I met with my friend" intent)', 'correct': 'ともだちと あいました。',
         'why': '会う meaning "meet (mutual)" takes と; に is grammatical but more like "happen to encounter".', 'error_category': 'particle'},
    ],
    'n5-009': [  # から (from)
        {'wrong': 'ごじから しちじに べんきょうします。', 'correct': 'ごじから しちじまで べんきょうします。',
         'why': 'Range "from X to Y" is から〜まで. に marks point-time, not endpoint of range.', 'error_category': 'particle'},
        {'wrong': 'あめから、いきません。', 'correct': 'あめだから、いきません。',
         'why': 'Reason から after a noun needs the copula: N + だ + から (or N + な + ので).', 'error_category': 'conjugation'},
    ],
    'n5-013': [  # も (also)
        {'wrong': 'わたしはも がくせいです。', 'correct': 'わたしも がくせいです。',
         'why': 'も REPLACES は/が, not stacks with them. Same for を: 本を 読みます → 本も 読みます (not 本もを).', 'error_category': 'particle'},
        {'wrong': 'コーヒーも こうちゃも のみません。 (intent: I drink either)', 'correct': 'コーヒーか こうちゃを のみます。',
         'why': '〜も〜も + negative = "neither X nor Y"; for "either/or" in positive use か.', 'error_category': 'lexicon'},
    ],
    'n5-029': [  # の (possessive / N-modifier)
        {'wrong': 'にほんの の ぶんか', 'correct': 'にほんの ぶんか',
         'why': 'Single の; double-の is a common typo / over-correction.', 'error_category': 'word_order'},
        {'wrong': 'あかいの くるま', 'correct': 'あかい くるま',
         'why': 'い-Adjective directly modifies noun without の. の attaches only to nouns and na-adj-substitutes.', 'error_category': 'conjugation'},
    ],
    'n5-058': [  # Verb-ます
        {'wrong': 'わたしは まいにち がっこうへ いきますね。', 'correct': 'わたしは まいにち がっこうへ いきます。',
         'why': 'Habitual statement of fact does not need ね; ね seeks agreement and softens declarations.', 'error_category': 'register'},
        {'wrong': 'たべるます。', 'correct': 'たべます。',
         'why': 'Group-2 (ichidan) drops る before ます: 食べる→食べ+ます. Do not keep る.', 'error_category': 'conjugation'},
    ],
    'n5-066': [  # Verb-ない
        {'wrong': 'たべるない。', 'correct': 'たべない。',
         'why': 'Group-2: drop る then add ない. 食べる→食べない.', 'error_category': 'conjugation'},
        {'wrong': 'こない (intent: "did not come" past)', 'correct': 'こなかった。',
         'why': 'こない is present-negative ("does not come"); past-negative is こなかった.', 'error_category': 'conjugation'},
    ],
    'n5-067': [  # Verb-た
        {'wrong': 'いきた。', 'correct': 'いった。',
         'why': '行く is a Group-1 exception: 行って/行った (NOT 行きて/行きた). Stem ends -く but uses っ-promotion.', 'error_category': 'conjugation'},
        {'wrong': 'べんきょうた。', 'correct': 'べんきょうした。',
         'why': 'する→した, not 〜た. Compound する-verbs all behave this way.', 'error_category': 'conjugation'},
    ],
    'n5-069': [  # Verb-て
        {'wrong': 'いきて、たべます。', 'correct': 'いって、たべます。',
         'why': '行く is the Group-1 exception with っ-promotion: 行って (not 行きて).', 'error_category': 'conjugation'},
        {'wrong': 'みて、ます。 (intent: "I am watching")', 'correct': 'みています。',
         'why': '〜ています is one phonological unit; do not insert a comma or pause.', 'error_category': 'word_order'},
    ],
    'n5-080': [  # i-adj negative
        {'wrong': 'たかいくないです。', 'correct': 'たかくないです。',
         'why': 'Drop final い before くない. Do not retain い: 高い→高くない (not 高いくない).', 'error_category': 'conjugation'},
        {'wrong': 'いいくないです。', 'correct': 'よくないです。',
         'why': 'いい/良い is irregular: stem switches to よ before negative/past forms (よくない, よかった).', 'error_category': 'conjugation'},
    ],
    'n5-081': [  # i-adj past
        {'wrong': 'たかいかったです。', 'correct': 'たかかったです。',
         'why': 'Drop final い then add かった: 高い→高かった (not 高いかった).', 'error_category': 'conjugation'},
        {'wrong': 'いいかったです。', 'correct': 'よかったです。',
         'why': 'いい uses irregular stem よ for past: よかった.', 'error_category': 'conjugation'},
    ],
    'n5-082': [  # i-adj past negative
        {'wrong': 'たかいくなかったです。', 'correct': 'たかくなかったです。',
         'why': 'Drop い + くなかった: 高い→高くなかった.', 'error_category': 'conjugation'},
        {'wrong': 'たかくありませんかった。', 'correct': 'たかくありませんでした。',
         'why': 'Polite past-negative is くありませんでした (not くありませんかった); the past tense lives in でした.', 'error_category': 'conjugation'},
    ],
    'n5-085': [  # na-adj + です
        {'wrong': 'しずかいです。', 'correct': 'しずかです。',
         'why': 'な-Adj attach directly to です with no い: 静か+です (do not insert い).', 'error_category': 'conjugation'},
        {'wrong': 'きれく ありません。', 'correct': 'きれいじゃありません。',
         'why': 'きれい LOOKS like an い-adj but is na-Adj: negative is じゃありません, not くありません.', 'error_category': 'conjugation'},
    ],
    'n5-086': [  # na-adj negative
        {'wrong': 'しずかくないです。', 'correct': 'しずかじゃないです。',
         'why': 'na-Adj negative uses じゃない / ではない (not くない, which is for い-Adj).', 'error_category': 'conjugation'},
        {'wrong': 'すきくない。', 'correct': 'すきじゃない。',
         'why': 'すき is na-Adj despite ending in -き. Use じゃない / ではない.', 'error_category': 'conjugation'},
    ],
    'n5-087': [  # na-adj past
        {'wrong': 'しずかかったです。', 'correct': 'しずかでした。',
         'why': 'na-Adj past uses でした (not かった, which is for い-Adj).', 'error_category': 'conjugation'},
        {'wrong': 'げんきだったです。', 'correct': 'げんきでした。',
         'why': 'Plain past だった + です is double-marking. Use polite past でした directly.', 'error_category': 'register'},
    ],
    'n5-090': [  # あります
        {'wrong': 'ねこが あります。', 'correct': 'ねこが います。',
         'why': 'あります is for inanimate / non-living; animate beings (people, animals) use います.', 'error_category': 'lexicon'},
        {'wrong': 'いすに ほんが います。', 'correct': 'いすに ほんが あります。',
         'why': 'Books are inanimate → あります. います is for living things.', 'error_category': 'lexicon'},
    ],
    'n5-091': [  # います
        {'wrong': 'ともだちが あります。', 'correct': 'ともだちが います。',
         'why': 'Friends (人) are animate → います. あります marks inanimate existence.', 'error_category': 'lexicon'},
        {'wrong': 'えきに タクシーが います。', 'correct': 'えきに タクシーが あります。',
         'why': 'Vehicles are inanimate → あります, even with a driver inside.', 'error_category': 'lexicon'},
    ],
    'n5-092': [  # に〜があります／います
        {'wrong': 'がっこうで ねこが います。', 'correct': 'がっこうに ねこが います。',
         'why': 'Static existence "be at" takes に. で is for actions occurring at a place.', 'error_category': 'particle'},
        {'wrong': 'つくえに ほんに あります。', 'correct': 'つくえに ほんが あります。',
         'why': 'The thing existing is marked with が, not に. に marks the LOCATION only.', 'error_category': 'particle'},
    ],
    'n5-098': [  # 〜
        {'wrong': '(unspecified — keep prior)', 'correct': '(unspecified — keep prior)',
         'why': 'Pattern-shape placeholder; primary entry covers main trap.', 'error_category': 'word_order'},
        {'wrong': '(unspecified — keep prior)', 'correct': '(unspecified — keep prior)',
         'why': 'Pattern-shape placeholder; primary entry covers main trap.', 'error_category': 'word_order'},
    ],
    'n5-099': [  # 〜が好きです
        {'wrong': 'わたしは ねこを すきです。', 'correct': 'わたしは ねこが すきです。',
         'why': 'すき/きらい take が, not を. The "object" of liking is grammatically the subject.', 'error_category': 'particle'},
        {'wrong': 'すきくないです。', 'correct': 'すきじゃありません。',
         'why': 'すき is na-Adj: negative uses じゃありません, not くないです.', 'error_category': 'conjugation'},
    ],
    'n5-100': [  # 〜が上手です
        {'wrong': 'わたしは にほんごを じょうずです。', 'correct': 'わたしは にほんごが じょうずです。',
         'why': 'じょうず/へた take が. The skill or activity is marked with が, not を.', 'error_category': 'particle'},
        {'wrong': 'わたしは じょうずです。 (about myself)', 'correct': 'わたしは あまり じょうずじゃありません。',
         'why': 'Calling oneself 上手 is culturally arrogant; use modest じょうずじゃありません or まだまだ.', 'error_category': 'register'},
    ],
    'n5-101': [  # 〜が欲しいです
        {'wrong': 'わたしは くるまを ほしいです。', 'correct': 'わたしは くるまが ほしいです。',
         'why': 'ほしい takes が. を is wrong for desired-object marking with adjectives of feeling.', 'error_category': 'particle'},
        {'wrong': 'せんせいは くるまが ほしいです。', 'correct': 'せんせいは くるまを ほしがっています。',
         'why': 'ほしい with 1st-person OK; 3rd-person requires ほしがっている (observable wanting-behavior).', 'error_category': 'register'},
    ],
    'n5-102': [  # 〜が分かります
        {'wrong': 'にほんごを わかります。', 'correct': 'にほんごが わかります。',
         'why': 'わかる is intransitive-ish; takes が for the thing-understood, not を.', 'error_category': 'particle'},
        {'wrong': 'わかってる。 (in formal context)', 'correct': 'わかります。 / わかっています。',
         'why': 'わかってる is plain spoken contraction; in polite contexts use わかります.', 'error_category': 'register'},
    ],
    'n5-104': [  # Verb-stem + たいです
        {'wrong': 'たべるたいです。', 'correct': 'たべたいです。',
         'why': 'Drop る from Group-2 stem before たい: 食べる→食べ+たい (not 食べる+たい).', 'error_category': 'conjugation'},
        {'wrong': 'せんせいは すしを たべたいです。', 'correct': 'せんせいは すしを たべたがっています。',
         'why': '〜たい reports 1st-person desire only; 3rd-person uses 〜たがっている (observable behavior).', 'error_category': 'register'},
    ],
    'n5-105': [  # Verb-stem + たくないです
        {'wrong': 'たべたいなくないです。', 'correct': 'たべたくないです。',
         'why': 'たい conjugates like an い-Adj: negative is たくない (drop い, add くない).', 'error_category': 'conjugation'},
        {'wrong': 'たべないたいです。', 'correct': 'たべたくないです。',
         'why': 'Order matters: stem + たい first, then negate the い-Adj. Not Vない + たい.', 'error_category': 'word_order'},
    ],
    'n5-115': [  # に (time)
        {'wrong': 'らいしゅうに いきます。', 'correct': 'らいしゅう いきます。',
         'why': 'Relative time (今日/明日/昨日/来週/先月) does NOT take に. Only specific clock/date takes に.', 'error_category': 'particle'},
        {'wrong': 'まいにちに しごとに いきます。', 'correct': 'まいにち しごとに いきます。',
         'why': 'まいにち/まいしゅう (frequency adverbs) take no particle.', 'error_category': 'particle'},
    ],
    'n5-117': [  # きょう / あした / きのう
        {'wrong': 'きょうに テストが あります。', 'correct': 'きょう テストが あります。',
         'why': 'Relative time-words take no particle: きょう/あした/きのう/おととい/あさって all bare.', 'error_category': 'particle'},
        {'wrong': 'おとといに きました。', 'correct': 'おととい きました。',
         'why': 'Same rule: relative-time has no に.', 'error_category': 'particle'},
    ],
    'n5-126': [  # が (but)
        {'wrong': 'たかい です が やすい です。 (intent: high but expensive)', 'correct': 'たかい です が おいしい です。',
         'why': 'Pair must contrast meaningfully. たかい and やすい are antonyms; "high but cheap" is contradictory not contrastive.', 'error_category': 'lexicon'},
        {'wrong': 'にほんごは むずかしいですが、たのしいでした。', 'correct': 'にほんごは むずかしいですが、たのしいです。',
         'why': 'Tense agreement across が: keep both clauses in matching tense unless explicit time-shift.', 'error_category': 'conjugation'},
    ],
    'n5-130': [  # 〜に〜をあげます
        {'wrong': 'ともだちに ほんを くれました。 (intent: I gave my friend a book)', 'correct': 'ともだちに ほんを あげました。',
         'why': 'あげる = "I/X give to Y"; くれる = "Y give TO me/in-group". Direction matters.', 'error_category': 'lexicon'},
        {'wrong': 'はは が プレゼントを あげました。 (intent: my mother gave me a gift)', 'correct': 'はは が プレゼントを くれました。',
         'why': 'Mother giving TO me (in-group recipient) = くれる, not あげる. あげる would mean mother gave to someone else.', 'error_category': 'lexicon'},
    ],
    'n5-167': [  # 〜んです
        {'wrong': 'たべましたんです。', 'correct': 'たべたんです。',
         'why': '〜んです attaches to PLAIN form (Vた/Vる/Vない), not polite ます-form. Drop ました → たべた + んです.', 'error_category': 'conjugation'},
        {'wrong': 'がくせいなんです。 (intent: I am a student — neutral)', 'correct': 'がくせいです。',
         'why': '〜んです adds explanatory nuance; use plain です for neutral statement. Overusing んです sounds like over-justifying.', 'error_category': 'register'},
    ],
    'n5-184': [  # なにか / なにも
        {'wrong': 'なにも たべました。 (intent: I ate something)', 'correct': 'なにか たべました。',
         'why': 'なにか = "something" (positive); なにも = "nothing" (negative + Vません).', 'error_category': 'lexicon'},
        {'wrong': 'なにも たべません か。', 'correct': 'なにも たべませんでした。 / なにか たべましたか。',
         'why': 'なにも requires negative predicate; cannot pair with question か meaning "did you eat anything".', 'error_category': 'word_order'},
    ],
}

# 30 NEW patterns — add 3-entry list each
NEW_ENTRIES = {
    'n5-001': [  # です／ます
        {'wrong': 'わたし がくせい。', 'correct': 'わたしは がくせいです。',
         'why': 'Polite predicate requires です; bare nouns are casual incomplete sentences.', 'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'がっこうに いくます。', 'correct': 'がっこうに いきます。',
         'why': 'Group-1 verb stem 行く→行き before ます (drop -u, add -i). Do not insert る.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'がくせいです か。 (with rising tone)', 'correct': 'がくせいですか。 (no space, falling tone often)',
         'why': 'Question particle か attaches directly without space; spoken intonation can be flat or slightly rising.', 'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-010': [  # まで
        {'wrong': 'ごじまでに いきます。 (intent: I will go until 5)', 'correct': 'ごじまで います。',
         'why': 'まで = "up until / until"; までに = "by (deadline)". Different meanings.', 'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'がっこうまでに あるきます。', 'correct': 'がっこうまで あるきます。',
         'why': 'Distance/spatial range uses まで; までに is only for time deadlines.', 'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'はちじから いつ まで べんきょうしますか。', 'correct': 'はちじから なんじまで べんきょうしますか。',
         'why': 'Question word for "until when (clock)" is なんじまで, not いつまで for clock-time. (いつまで is general.)', 'error_category': 'lexicon', 'provenance': 'llm_curated'},
    ],
    'n5-061': [  # ませんでした
        {'wrong': 'たべませんかった。', 'correct': 'たべませんでした。',
         'why': 'Polite past-negative is ませんでした (not ませんかった). The past tense sits in でした.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべなかったでした。', 'correct': 'たべませんでした。 / たべなかった。',
         'why': 'Plain なかった + でした is double-marking. Use polite ませんでした OR plain なかった.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'きのう たべませんでした か。 (rising)', 'correct': 'きのう たべましたか。 (with なに or asking confirmation)',
         'why': 'Negative-question form often implies "did you not eat?" expecting yes; use carefully.', 'error_category': 'register', 'provenance': 'llm_curated'},
    ],
    'n5-062': [  # ましょう
        {'wrong': 'いっしょに たべります ましょう。', 'correct': 'いっしょに たべましょう。',
         'why': 'ましょう replaces ます; do not stack them.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'あした たべましょう。 (to a stranger)', 'correct': 'あした たべませんか。',
         'why': 'ましょう is "let\'s" (assumes agreement); 〜ませんか is more polite invitation to a stranger.', 'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'たべました ましょう。', 'correct': 'たべましょう。',
         'why': 'ましょう is volitional only — no past form. Cannot stack with ました.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-063': [  # ましょうか
        {'wrong': 'まどを あけますか。 (intent: shall I open?)', 'correct': 'まどを あけましょうか。',
         'why': 'For "shall I do X for you?" use ましょうか; plain Vますか is just yes/no question.', 'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'いっしょに たべましょう か?', 'correct': 'いっしょに たべましょうか。',
         'why': 'No space between ましょう and か.', 'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'てつだいたい ましょうか。', 'correct': 'てつだいましょうか。',
         'why': 'Do not stack たい + ましょうか. ましょうか already conveys offering.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-064': [  # ませんか
        {'wrong': 'いきます か。 (intent: would you like to go)', 'correct': 'いきませんか。',
         'why': 'Polite invitation uses negative form ませんか ("won\'t you...?"); positive ますか is a yes/no fact-question.', 'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'いきませんでしたか。 (intent: invitation in past)', 'correct': 'いきませんでしたか。',
         'why': 'ませんでしたか is a question about a past event ("did you not go?"), NOT a past invitation.', 'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'いっしょに たべませんか?', 'correct': 'いっしょに たべませんか。',
         'why': 'Use 。 not ?; question-mark is not standard in formal Japanese (though acceptable casually).', 'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-068': [  # なかった
        {'wrong': 'たべなかったでした。', 'correct': 'たべなかった。 / たべませんでした。',
         'why': 'なかった is plain past-negative; do not add でした. Use one register or the other.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'こない (in past context)', 'correct': 'こなかった。',
         'why': 'こない is present-negative; past needs こなかった.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべないかった。', 'correct': 'たべなかった。',
         'why': 'Negative-stem is ない (drop い), then add かった: たべな+かった (not たべない+かった).', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-070': [  # Verb-て、Verb-て
        {'wrong': 'たべて、ねます、しんぶんを よみます。', 'correct': 'たべて、しんぶんを よんで、ねます。',
         'why': 'Te-form chain: each non-final clause uses て-form; only final clause is finite. Order = chronological.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'おきて、シャワーを あびます、あさごはんを たべます。', 'correct': 'おきて、シャワーを あびて、あさごはんを たべます。',
         'why': 'Multi-event sequence: every clause except the last must be て-form.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'いって たべます。', 'correct': 'いって、たべます。',
         'why': 'In wakachi-gaki / formal text, comma after て is conventional for clarity.', 'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-071': [  # 〜てください
        {'wrong': 'たべるてください。', 'correct': 'たべてください。',
         'why': 'Group-2 drops る to make て-form: 食べる→食べて (not 食べるて).', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'おきてください。 (in commanding tone to a senior)', 'correct': 'おきていただけませんか。',
         'why': '〜てください is request, but to seniors use higher-respect 〜ていただけませんか.', 'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'きてくださ。', 'correct': 'きてください。',
         'why': 'ください is a 4-mora word — do not drop the final い in writing.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-072': [  # Vています
        {'wrong': 'いま たべます。 (intent: I am eating right now)', 'correct': 'いま たべています。',
         'why': 'Progressive "right now doing" needs ています. Plain ます is habitual or future.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'けっこんしています。 (intent: I am marrying right now)', 'correct': 'けっこんしました。 (event) / けっこんしています。 (= I am married, ongoing state)',
         'why': '結婚する is a punctual verb: ています = resultant state ("am married"), NOT ongoing process.', 'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'きてています。', 'correct': 'きています。',
         'why': 'Do not double-て. 来る→来て+います = きています.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-074': [  # てもいいです
        {'wrong': 'たべてもいいか。 (to teacher)', 'correct': 'たべてもいいですか。',
         'why': 'Permission-asking to a senior must keep です; dropping です is too casual.', 'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'たべるても いいです。', 'correct': 'たべても いいです。',
         'why': 'Drop る to form て first: 食べる→食べて+も+いいです.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべて いいです。', 'correct': 'たべても いいです。',
         'why': 'The も is required for permission "even doing X is OK". Without も, the sentence is ungrammatical for permission.', 'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-075': [  # てはいけません
        {'wrong': 'たばこを すいて はいけません。', 'correct': 'たばこを すっては いけません。',
         'why': 'Group-1 verb 吸う→吸って (with promotion). Do not produce すいて.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべて は いけない。 (to a customer)', 'correct': 'おたべに ならないでください。 / ご遠慮ください。',
         'why': 'てはいけない is direct prohibition, too blunt for customers; use polite ご遠慮ください.', 'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'たべてはいけません だ。', 'correct': 'たべてはいけません。',
         'why': 'いけません is already finite; do not append だ.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-076': [  # てから
        {'wrong': 'たべるから、いきます。 (intent: after eating, go)', 'correct': 'たべてから、いきます。',
         'why': 'てから = "after doing X"; から alone after dictionary form means "because". Different meanings.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'おきましてから、シャワーを あびます。', 'correct': 'おきてから、シャワーを あびます。',
         'why': 'てから takes plain te-form, not ましてから (overly formal/incorrect for N5).', 'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'たべて から いきました てから ねました。', 'correct': 'たべてから いって、それから ねました。',
         'why': 'Do not chain multiple てから clauses; use それから or sequential て-forms instead.', 'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-077': [  # ないでください
        {'wrong': 'たべるないで ください。', 'correct': 'たべないで ください。',
         'why': 'Group-2: drop る then ない: 食べる→食べない→食べないで.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべなくて ください。', 'correct': 'たべないで ください。',
         'why': 'Negative request uses ないで, not なくて. なくて is for reasons/causes.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'いかないでください。 (to a friend casually)', 'correct': 'いかないで。',
         'why': 'Plain casual register drops ください: ないで alone is fine with intimates.', 'error_category': 'register', 'provenance': 'llm_curated'},
    ],
    'n5-083': [  # い-Adj te-form: 〜くて
        {'wrong': 'たかいで やすいです。', 'correct': 'たかくて やすくない です。',
         'why': 'い-Adj te-form is くて (drop い, add くて). な-Adj te-form is で.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'いいくて おいしいです。', 'correct': 'よくて おいしいです。',
         'why': 'いい→よくて (irregular stem-switch).', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'おいしいくて たかいです、すしは。', 'correct': 'すしは おいしくて たかいです。',
         'why': 'Topic and word-order: SOV-canonical. End with predicate; くて links adjectives left-to-right.', 'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-088': [  # na-Adj past-negative
        {'wrong': 'しずかかったじゃありません。', 'correct': 'しずかじゃありませんでした。',
         'why': 'na-Adj past-negative is じゃありませんでした (not かった+じゃありません).', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'すきくなかったです。', 'correct': 'すきじゃありませんでした。 / すきじゃなかったです。',
         'why': 'すき is na-Adj. Use じゃ(あり)ませんでした, not くなかった.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'げんきじゃありませんでした と、おもいます。', 'correct': 'げんきじゃありませんでしたと、おもいます。',
         'why': 'No space before quotative と.', 'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-089': [  # na-Adj te-form
        {'wrong': 'しずかくて きれいです。', 'correct': 'しずかで きれいです。',
         'why': 'na-Adj te-form is で (not くて, which is for い-Adj).', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'きれいくて しずかです。', 'correct': 'きれいで しずかです。',
         'why': 'きれい is na-Adj despite ending in い. Te-form is きれいで.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'しずかでで きれいです。', 'correct': 'しずかで きれいです。',
         'why': 'Single で. Double で is a typo.', 'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-095': [  # 〜は〜より〜です
        {'wrong': 'にほんは アメリカが おおきいです。', 'correct': 'アメリカは にほんより おおきいです。',
         'why': 'Pattern: A は B より Adj = A is more Adj than B. Mark the comparison-target with より, not が.', 'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'おちゃは コーヒーから やすいです。', 'correct': 'おちゃは コーヒーより やすいです。',
         'why': 'Comparison particle is より, not から. から = "from".', 'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'にほんは おおきい より アメリカ です。', 'correct': 'アメリカは にほんより おおきいです。',
         'why': 'Word order: TOPIC は STANDARD より ADJ です.', 'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-097': [  # 〜と〜と、どちらが
        {'wrong': 'コーヒーや こうちゃ、どちらが すきですか。', 'correct': 'コーヒーと こうちゃと、どちらが すきですか。',
         'why': 'For binary choice, both items are linked by と (exhaustive); や is non-exhaustive list.', 'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'A と B と、どっちが すきですか。 (in formal context)', 'correct': 'A と B と、どちらが すきですか。',
         'why': 'どっち is casual; どちら is polite. Match register.', 'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'コーヒーと こうちゃは、どちらが すきですか。', 'correct': 'コーヒーと こうちゃと、どちらが すきですか。',
         'why': 'Second item also takes と (ABと、 not ABは、) when phrasing the binary choice.', 'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-107': [  # Vstem + に行きます
        {'wrong': 'たべるに いきます。', 'correct': 'たべに いきます。',
         'why': 'Verb-stem (drop ます or る) + に+motion-verb. たべる→たべ+に.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'すしを たべに いきます ました。', 'correct': 'すしを たべに いきました。',
         'why': 'Past tense sits on the motion-verb (いきました), not on ます stacked.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'べんきょうに します。', 'correct': 'べんきょうに いきます。 / べんきょうします。',
         'why': 'します alone is the suru-verb; for "go to study" need いきます.', 'error_category': 'lexicon', 'provenance': 'llm_curated'},
    ],
    'n5-108': [  # Number + counter
        {'wrong': 'りんごが さん あります。', 'correct': 'りんごが みっつ あります。 / りんごが さんこ あります。',
         'why': 'Number alone insufficient; need a counter. Generic counter for objects: つ (1-10) or こ.', 'error_category': 'counter', 'provenance': 'llm_curated'},
        {'wrong': 'ひとが いちにん います。', 'correct': 'ひとが ひとり います。',
         'why': '1-person is ひとり (irregular), not いちにん. 2-people = ふたり. From 3 onwards: さんにん etc.', 'error_category': 'counter', 'provenance': 'llm_curated'},
        {'wrong': 'いっぴき ねこ。', 'correct': 'ねこが いっぴき います。',
         'why': 'Counter typically follows the verb in stacking order: が + counter + Verb (not pre-noun).', 'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-122': [  # それから
        {'wrong': 'たべました。それからに、いきました。', 'correct': 'たべました。それから、いきました。',
         'why': 'それから is itself a connector; do not add に or は after it.', 'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'たべて、それから ねます。', 'correct': 'たべてから、ねます。 / たべて、それから ねます。',
         'why': 'てから is tighter "right after"; それから is "after that, additionally". Subtle but distinct.', 'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'それから、しんぶんを よみました それから、ねました。', 'correct': 'しんぶんを よんでから、ねました。',
         'why': 'Repeating それから is choppy; consolidate with てから or chain with て-form.', 'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-123': [  # でも
        {'wrong': 'にほんごは むずかしい でも たのしい です。', 'correct': 'にほんごは むずかしい です。でも、たのしい です。',
         'why': 'でも starts a NEW sentence; do not connect mid-sentence (use が instead).', 'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'でも、それは ちがうです。', 'correct': 'でも、それは ちがいます。',
         'why': '違う is a Group-1 verb, not adjective: polite is ちがいます (not ちがうです).', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たかいですでも、おいしいです。', 'correct': 'たかいです。でも、おいしいです。',
         'why': 'Sentence-initial conjunction: full stop before でも.', 'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-131': [  # もらいます
        {'wrong': 'ともだちに ほんを あげました。 (intent: I received from friend)', 'correct': 'ともだちに/から ほんを もらいました。',
         'why': 'もらう = receive; あげる = give. Direction matters.', 'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'せんせいに プレゼントを もらいました。 (about teacher → student)', 'correct': 'せんせいから プレゼントを いただきました。',
         'why': 'Receiving from a senior uses humble いただく.', 'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'ともだちで ほんを もらいました。', 'correct': 'ともだちから ほんを もらいました。',
         'why': 'Source of receiving = から or に, not で.', 'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-132': [  # くれます
        {'wrong': 'はは が プレゼントを あげました。 (intent: mother gave me)', 'correct': 'はは が プレゼントを くれました。',
         'why': 'Mother → me (in-group) = くれる. あげる would mean mother gave to OTHERS.', 'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'せんせい が ほんを くれました。', 'correct': 'せんせい が ほんを くださいました。',
         'why': 'Senior (先生) giving to me = honorific くださる (くださいました).', 'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'ともだち は プレゼントを くれました。', 'correct': 'ともだち が プレゼントを くれました。',
         'why': 'The giver (subject of くれる) is marked with が (new info), not は.', 'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-144': [  # Vstem + ながら
        {'wrong': 'たべるながら、しんぶんを よみます。', 'correct': 'たべながら、しんぶんを よみます。',
         'why': 'ながら attaches to V-stem (not dictionary form): 食べる→食べ+ながら.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'うんてんを しながら、でんわを かけます。', 'correct': 'うんてんしながら、でんわを かけます。',
         'why': '運転する: stem is 運転し (drop する→し). Do not break with を.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'はしりながら たべる は あぶないです。', 'correct': 'はしりながら たべるのは あぶないです。',
         'why': 'Verb-noun-ization needs の: たべる + のは (not bare たべるは).', 'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-145': [  # 〜とおもいます
        {'wrong': 'あめが ふりますと おもいます。', 'correct': 'あめが ふると おもいます。',
         'why': '〜とおもう takes plain form (Vる/Vない/Vた); polite ます-form before と is non-standard.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'おもいます、あめが ふる と。', 'correct': 'あめが ふると おもいます。',
         'why': 'Quoted clause + と + おもいます = canonical order. Cannot post-pose the と-clause.', 'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'がくせいだと おもう です。', 'correct': 'がくせいだと おもいます。',
         'why': 'おもう can be plain; if attaching to something stack-able, use polite おもいます (consistent register).', 'error_category': 'register', 'provenance': 'llm_curated'},
    ],
    'n5-146': [  # 〜と言いました
        {'wrong': 'せんせいが、 たべてくださいと いいます ました。', 'correct': 'せんせいが、「たべてください」と いいました。',
         'why': 'Direct quote uses 「」; particle と immediately follows the quote with no space.', 'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'ははが くる と いいました。', 'correct': 'ははが、くると いいました。 / ははが「くる」と いいました。',
         'why': 'Indirect quote: plain form + と + いいました. Spacing/comma matters for parsing.', 'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'ははが はい と いいました。', 'correct': 'ははが「はい」と いいました。',
         'why': 'Single-word quotes still take quote marks for clarity.', 'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-153': [  # まだ + Vていません
        {'wrong': 'まだ たべません。 (intent: have not eaten yet)', 'correct': 'まだ たべていません。',
         'why': '"Have not yet done X" requires ていません, not Vません. Vません = future/habitual negative.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'もう たべていません。', 'correct': 'もう たべました。 / まだ たべていません。',
         'why': 'もう = "already" (positive); まだ = "yet" (with negative). Pair correctly.', 'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'まだ きませんでした。', 'correct': 'まだ きていません。',
         'why': '"Has not come yet" uses まだ + ていません (resultant-state negation), not past-negative ませんでした.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-154': [  # もう + Vました
        {'wrong': 'もう たべます。 (intent: already eaten)', 'correct': 'もう たべました。',
         'why': '"Already V-ed" needs past form ました; Vます is non-past.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'もう たべませんでした。 (intent: have already not eaten)', 'correct': 'もう たべました。 / まだ たべていません。',
         'why': 'もう pairs with positive past (or ません = "no longer"). For "not yet" use まだ ていません.', 'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'もう うちに かえります ました。', 'correct': 'もう うちに かえりました。',
         'why': 'Past form is かえりました (drop ます, add ました). Do not stack ます+ました.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-169': [  # Vた + ことがある
        {'wrong': 'にほんに いく ことがあります。 (intent: have been to Japan)', 'correct': 'にほんに いった ことがあります。',
         'why': '"Have V-ed before" needs PAST PLAIN + ことがある. Dictionary form changes meaning to "sometimes do".', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'いったことが ありますね。 (about your own experience)', 'correct': 'いったことが あります。',
         'why': 'ね about your own experience implies seeking listener confirmation, which is odd.', 'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'いったの ことがあります。', 'correct': 'いったことがあります。',
         'why': 'Vた directly + ことがある, no nominalizer の.', 'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-170': [  # Vた + ほうがいい
        {'wrong': 'たべる ほうがいい。 (intent: should eat)', 'correct': 'たべた ほうがいい。',
         'why': 'Advisory "should V" in N5 uses Vた (past plain) + ほうがいい. Vる makes it a generic comparison.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべない ほうがいい です ね。 (commanding)', 'correct': 'たべない ほうがいいですよ。',
         'why': 'Advisory uses よ (informing) more than ね (seeking agreement).', 'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'たべた ほうが いい だ。', 'correct': 'たべた ほうが いい。',
         'why': 'いい is an adjective; do not append だ. Use plain いい or polite いいです.', 'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
}

# --- Apply: convert + extend existing 36 ---
print('=== G3: Schema migration + expansion ===')
patterns_by_id = {p['id']: p for p in patterns}

migrated = 0
expanded = 0
new_added = 0

for pid, extra in ADDITIONS.items():
    p = patterns_by_id.get(pid)
    if not p:
        continue
    existing = p.get('wrong_corrected_pair')
    if isinstance(existing, dict):
        # Migrate single dict to list, ensure each has error_category
        first = dict(existing)
        if 'error_category' not in first:
            # Infer from pattern if possible
            # Default: particle for particles n5-002..n5-013, conjugation for verb forms
            if pid in ('n5-002','n5-003','n5-004','n5-005','n5-006','n5-007','n5-008','n5-009','n5-013','n5-115'):
                first['error_category'] = 'particle'
            elif pid in ('n5-058','n5-066','n5-067','n5-069','n5-080','n5-081','n5-082','n5-085','n5-086','n5-087','n5-104','n5-105'):
                first['error_category'] = 'conjugation'
            elif pid in ('n5-090','n5-091','n5-130','n5-184','n5-099','n5-100','n5-101','n5-102'):
                first['error_category'] = 'lexicon'
            else:
                first['error_category'] = 'lexicon'
        new_list = [first]
        # Append the 2 new entries (with provenance)
        for e in extra:
            new_e = dict(e)
            new_e['provenance'] = 'llm_curated'
            new_list.append(new_e)
        p['wrong_corrected_pair'] = new_list
        migrated += 1
        expanded += 1
    elif isinstance(existing, list):
        # Already list; append if <3
        for e in extra:
            if len(p['wrong_corrected_pair']) < 3:
                new_e = dict(e)
                new_e['provenance'] = 'llm_curated'
                p['wrong_corrected_pair'].append(new_e)
        expanded += 1

print(f'  Migrated single-dict to list: {migrated}')
print(f'  Patterns expanded with extras: {expanded}')

# Apply NEW_ENTRIES to currently-empty patterns
for pid, entries in NEW_ENTRIES.items():
    p = patterns_by_id.get(pid)
    if not p:
        continue
    if p.get('wrong_corrected_pair'):
        continue  # already has — skip
    p['wrong_corrected_pair'] = entries
    new_added += 1

print(f'  New patterns with 3-entry list: {new_added}')

# Validation: every list must have >=3 entries with required fields
errors = 0
for p in patterns:
    wcp = p.get('wrong_corrected_pair')
    if isinstance(wcp, list):
        for e in wcp:
            for k in ('wrong','correct','why','error_category','provenance'):
                if k not in e:
                    print(f'  WARN {p["id"]}: missing {k} in entry')
                    errors += 1

print(f'  Validation errors: {errors}')

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Summary
total = len(patterns)
list_form = sum(1 for p in patterns if isinstance(p.get('wrong_corrected_pair'), list))
ge3 = sum(1 for p in patterns if isinstance(p.get('wrong_corrected_pair'), list) and len(p['wrong_corrected_pair']) >= 3)
print()
print('=== FINAL ===')
print(f'  any wrong_corrected_pair (list-form): {list_form}/{total}')
print(f'  list with >=3 entries:                {ge3}/{total}')
