"""Grammar Batch E (2026-05-10):
Continue G2 closing remaining gaps. Target: bring coverage from 113 to ~150+.
N5-only kanji + kana throughout.
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

ENTRIES = {
    'n5-027': [  # よね (combined particle)
        {'wrong': 'たかい です よ ね。 (asserting + agreement separately)',
         'correct': 'たかい ですよね。',
         'why': 'よね attaches without internal spaces; it is one combined ending.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'がくせい です よね。 (about your own status)',
         'correct': 'がくせい です。',
         'why': 'よね assumes shared knowledge; for facts only you know, drop it.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'たべます よね か。', 'correct': 'たべますよね。 / たべますか。',
         'why': 'よね already a confirmation-question; do not stack か.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-028': [  # 〜の (possessive variant)
        {'wrong': 'これは わたしの です ほん。', 'correct': 'これは わたしの ほんです。',
         'why': 'Word order: possessive の + N + です. Cannot split.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'にほんごの ほんの です。', 'correct': 'にほんごの ほんです。',
         'why': 'Single の per modifier; do not double.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'わたし ほん。 (no の)', 'correct': 'わたしの ほん。',
         'why': 'Possessive linkage requires の: A + の + B = "A\'s B".',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-030': [  # nominalizer の (basic)
        {'wrong': 'にほんごを はなすの すきです。', 'correct': 'にほんごを はなすのが すきです。',
         'why': 'Nominalized verb takes が (object of すき). Drop が is wrong.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'たべるは すきです。', 'correct': 'たべるのは すきです。',
         'why': 'Bare Vる cannot directly take は; nominalize with の first.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'はしりますの は たのしいです。', 'correct': 'はしるのは たのしいです。',
         'why': 'Nominalizer の attaches to PLAIN form, not polite ます-form.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-031': [  # の (other use - emphasis/pronoun)
        {'wrong': 'これは あかい くるまです。 (intent: this is the red one)',
         'correct': 'これは あかいのです。',
         'why': 'For pronominal "the red one" use のです (の as pronoun + copula).',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'たかいの は です。', 'correct': 'たかいのは これです。',
         'why': 'のは links to a copula; need an explicit subject after は.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'あかいですのを かいました。', 'correct': 'あかいのを かいました。',
         'why': 'Bare adjective + のを (drop です): あかい+の+を.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-039': [  # これ/それ/あれ/どれ (variant)
        {'wrong': 'これ ほん。', 'correct': 'これは ほんです。',
         'why': 'Pronoun これ requires は + complete sentence with です.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'これ ほんは わたしの。', 'correct': 'この ほんは わたしの です。',
         'why': 'Before noun use この (determiner); これ is standalone pronoun.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'どれは いいですか。', 'correct': 'どれが いいですか。',
         'why': 'どれ as question takes が, never は.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-040': [  # この/その/あの/どの + N
        {'wrong': 'このは ほんです。', 'correct': 'これは ほんです。 / この ほんは ...',
         'why': 'この MUST take a noun directly. For pronoun use これ.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'その なほん。', 'correct': 'その ほん。',
         'why': 'Determiner + noun directly. Do not insert な (this is for na-Adj only).',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'どの ほんは いいですか。', 'correct': 'どの ほんが いいですか。',
         'why': 'Question with どの takes が on the resulting NP.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-042': [  # こちら / そちら / あちら / どちら
        {'wrong': 'こちらは どこ ですか。 (asking where you are, casually)',
         'correct': 'ここは どこ ですか。',
         'why': 'こちら is polite/direction; for plain spatial use ここ.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'どちらは ペンですか。 (asking "which is the pen")',
         'correct': 'どちらが ペンですか。',
         'why': 'Question word どちら takes が, never は.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'こちらに、どうぞ。 (offering a seat to a guest)',
         'correct': 'こちらへ どうぞ。',
         'why': 'Direction toward listener uses へ; に would imply destination as a fixed point.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-043': [  # こんな/そんな/あんな/どんな + N
        {'wrong': 'どんなな ひとですか。', 'correct': 'どんな ひとですか。',
         'why': 'どんな ends in な; do not double な.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'どんなは ひとですか。', 'correct': 'どんな ひとですか。',
         'why': 'どんな is a determiner — attaches to noun directly, no は.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'こんなの くるまが すきです。', 'correct': 'こんな くるまが すきです。',
         'why': 'こんな + N (no の inserted).',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-050': [  # どう / いかが
        {'wrong': 'コーヒー どう ですか。 (in formal context to client)',
         'correct': 'コーヒー、いかがですか。',
         'why': 'いかが is the polite form of どう; use it with seniors/clients.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'どうは いいですか。', 'correct': 'どうですか。',
         'why': 'どう takes no particle (adverb-like). Just どう + ですか.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'りょこうは どうかった ですか。', 'correct': 'りょこうは どうでしたか。',
         'why': 'Past form is どうでしたか (not どうかった — that is not a valid form).',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-051': [  # どうして / なぜ
        {'wrong': 'どうしてに きましたか。', 'correct': 'どうして きましたか。',
         'why': 'どうして takes no particle. Just どうして + Q.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'なぜか ですか。 (intent: why)', 'correct': 'なぜですか。 / どうしてですか。',
         'why': 'なぜ alone is "why"; なぜか means "for some reason" (different meaning).',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'どうして きません。 おそかったから。', 'correct': 'どうして きませんでしたか。 おそかったからです。',
         'why': 'Past Q needs past tense + か; reason + です for completeness.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-054': [  # いくつ
        {'wrong': 'いくつ ですか。 (asking price)', 'correct': 'いくらですか。',
         'why': 'いくつ for count of items / age; いくら for price.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'りんごは いくつに ありますか。', 'correct': 'りんごは いくつ ありますか。',
         'why': 'いくつ takes no particle.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'おとうさんは いくつ ですか。 (asking parent\'s age in formal context)',
         'correct': 'おとうさんは おいくつですか。',
         'why': 'For polite age-asking add お (oikutsu).',
         'error_category': 'register', 'provenance': 'llm_curated'},
    ],
    'n5-056': [  # なんようび
        {'wrong': 'いつ ようびですか。', 'correct': 'なんようびですか。',
         'why': 'For day-of-week question use なんようび. いつ asks general time.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'きょうは なに ようび ですか。', 'correct': 'きょうは なんようびですか。',
         'why': 'Before counter-like ようび, 何 reads なん. なに breaks the compound.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'なんようび きますか。', 'correct': 'なんようびに きますか。',
         'why': 'Day-of-week as a time-when point takes に (specific calendar day).',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-057': [  # なんがつ なんにち
        {'wrong': 'なに がつ なに にち ですか。', 'correct': 'なんがつ なんにち ですか。',
         'why': 'Before counters がつ/にち, 何 reads なん.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'よにち。 (intent: 4th of month)', 'correct': 'よっか。',
         'why': '4th of month is よっか (irregular reading).',
         'error_category': 'counter', 'provenance': 'llm_curated'},
        {'wrong': 'なんにちに きました か。 (asking which day-of-month)',
         'correct': 'なんにちに きましたか。 (already correct)',
         'why': 'Specific date takes に. なんにち = which day of month.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-106': [  # Noun + が ほしいです
        {'wrong': 'くるまを ほしいです。', 'correct': 'くるまが ほしいです。',
         'why': 'ほしい takes が. (Like other feeling adjectives.)',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'ともだちは くるまが ほしいです。', 'correct': 'ともだちは くるまを ほしがっています。',
         'why': 'ほしい works for 1st person; 3rd-person needs ほしがる (observable wanting).',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'ほしいくないです。', 'correct': 'ほしくないです。',
         'why': 'い-Adj negative drops い: ほしい→ほしく+ない.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-109': [  # いくつ / いくら / なんにん etc.
        {'wrong': 'なんにん ひと きました か。', 'correct': 'なんにん きましたか。',
         'why': 'Counter なんにん is itself "how many people"; do not add ひと again.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'ほんを なんまい ありますか。', 'correct': 'ほんは なんさつ ありますか。',
         'why': 'Books use counter さつ (なんさつ); まい is for flat thin items (paper, plates).',
         'error_category': 'counter', 'provenance': 'llm_curated'},
        {'wrong': 'いくつ ねこが いますか。', 'correct': 'なんびき ねこが いますか。',
         'why': 'For animals use ひき/ぴき; いくつ is for objects (counter つ).',
         'error_category': 'counter', 'provenance': 'llm_curated'},
    ],
    'n5-113': [  # ～じはん
        {'wrong': 'にじ はん ぐらいに きました。', 'correct': 'にじはんごろ きました。',
         'why': 'はん attaches to じ directly; for "about" use ごろ on clock-time.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'にじはん ぐらい です ね。', 'correct': 'にじはん ぐらい です。',
         'why': 'Confirming time to listener can use ね; depends on shared context.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'よじ はんから しちじ はんまで。', 'correct': 'よじはんから しちじはんまで。',
         'why': 'No internal space in じはん compound.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-116': [  # 毎日 / まいしゅう ...
        {'wrong': 'まいにちに しごとに いきます。', 'correct': 'まいにち しごとに いきます。',
         'why': 'Frequency adverbs (まい〜) take no particle.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'まいにち、 まいにち、 べんきょうしました。',
         'correct': 'まいにち べんきょうしました。',
         'why': 'Repeating まいにち is unnecessary for emphasis; redundant.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'まいねんに あに あいます。', 'correct': 'まいとし あに あいます。',
         'why': 'Common reading is まいとし for "every year" (まいねん is also valid but less common in N5).',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
    ],
    'n5-119': [  # ～まえ
        {'wrong': 'たべますまえに、 てを あらいます。', 'correct': 'たべるまえに、 てを あらいます。',
         'why': 'まえに takes plain dictionary form, not polite ます.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべるまえで、 てを あらいます。', 'correct': 'たべるまえに、 てを あらいます。',
         'why': 'まえに (time before) — particle is に, not で.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'にじまえに きます。', 'correct': 'にじのまえに きます。',
         'why': 'For "before 2 o\'clock" use にじのまえに (with の), or にじまえに with hyphenation context.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-120': [  # ～あと
        {'wrong': 'たべるあとで、 ねます。', 'correct': 'たべたあとで、 ねます。',
         'why': 'あと takes PAST plain form (Vた + あとで).',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべたあとに、 ねます。', 'correct': 'たべたあとで、 ねます。',
         'why': 'Standard particle for あと is で (in this construction).',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'がっこうあとで、 いきます。', 'correct': 'がっこうのあとで、 いきます。',
         'why': 'After noun + あと: noun + の + あと + で.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-137': [  # Noun + の + Noun
        {'wrong': 'にほん ほん。', 'correct': 'にほんの ほん。',
         'why': 'Noun-noun linkage requires の.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'にほんの の ほん。', 'correct': 'にほんの ほん。',
         'why': 'Single の; double is a typo.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'がっこうな ほん。', 'correct': 'がっこうの ほん。',
         'why': 'Noun + noun uses の (not な; な is for na-Adj).',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-142': [  # 〜にします
        {'wrong': 'コーヒーを します。', 'correct': 'コーヒーに します。',
         'why': 'Choice/decision pattern is N + に + する. を marks general object.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'にします か コーヒーを。', 'correct': 'コーヒーに しますか。',
         'why': 'SOV order: object first, then にします.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'コーヒーで します。 (intent: I will choose coffee)',
         'correct': 'コーヒーに します。',
         'why': 'Decision particle is に, not で.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-143': [  # 〜になります / 〜くなります
        {'wrong': 'たかいに なります。', 'correct': 'たかくなります。',
         'why': 'い-Adj uses くなる (drop い, add く+なる). Only na-Adj/N use になる.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'しずかくなります。', 'correct': 'しずかになります。',
         'why': 'na-Adj (しずか) uses になる, not くなる.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'いいくなります。', 'correct': 'よくなります。',
         'why': 'いい uses irregular stem よ: よくなる.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-147': [  # よく / ときどき / あまり / ぜんぜん
        {'wrong': 'あまり たべます。 (intent: I do not eat much)', 'correct': 'あまり たべません。',
         'why': 'あまり requires NEGATIVE predicate ("not much / not very").',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'ぜんぜん たべました。 (intent: I did not eat at all)',
         'correct': 'ぜんぜん たべませんでした。',
         'why': 'ぜんぜん (in standard usage) requires negative.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'よく あまり たべます。', 'correct': 'よく たべます。 / あまり たべません。',
         'why': 'Frequency adverbs are mutually exclusive in this construction.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
    ],
    'n5-148': [  # いつも / たいてい / たまに
        {'wrong': 'いつも たまに テレビを みます。', 'correct': 'たまに テレビを みます。',
         'why': 'いつも (always) and たまに (sometimes) contradict; use one.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'たいてい テレビを みません。 (intent: I usually do watch)',
         'correct': 'たいてい テレビを みます。',
         'why': 'たいてい = "usually" — pairs with positive predicate.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'いつもに テレビを みます。', 'correct': 'いつも テレビを みます。',
         'why': 'いつも takes no particle.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-151': [  # ～はいかがですか
        {'wrong': 'コーヒーは いかがですか だ。', 'correct': 'コーヒーは いかがですか。',
         'why': 'です + か already terminates; do not append だ.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'コーヒーは どう ですか。 (in formal context to senior)',
         'correct': 'コーヒーは いかがですか。',
         'why': 'いかが is polite version of どう; use with seniors.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'コーヒーが いかがですか。', 'correct': 'コーヒーは いかがですか。',
         'why': 'Topic of offering is は (introducing the topic), not が.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-152': [  # どうぞ / どうも / すみません / おねがいします
        {'wrong': 'どうもありがとう。 (intent: a casual thanks to friend)',
         'correct': 'ありがとう。 / どうも。',
         'why': 'どうもありがとう is mid-formality; pure casual is どうも or ありがとう.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'すみません どうも おねがいします どうぞ。',
         'correct': 'すみません、おねがいします。',
         'why': 'Stacking polite phrases is unnecessary; one fits the context.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'どうも、いいです。 (declining offer politely)', 'correct': 'いいえ、けっこうです。',
         'why': 'For polite refusal use いいえ + けっこう/だいじょうぶ; どうも is too short.',
         'error_category': 'register', 'provenance': 'llm_curated'},
    ],
    'n5-155': [  # 〜が、〜
        {'wrong': 'たかいです がやすいです。 (no comma)',
         'correct': 'たかい ですが、やすい くないです。',
         'why': 'In standard punctuation, comma after が; also avoid contradictory adjective pair.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'たかいです、しかしが、おいしいです。',
         'correct': 'たかいですが、おいしいです。',
         'why': 'が and しかし are alternative contrast markers; do not stack.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'たかいですがが、おいしいです。', 'correct': 'たかいですが、おいしいです。',
         'why': 'Single が only.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-157': [  # 〜でしょう
        {'wrong': 'あめが ふるでしょう だ。', 'correct': 'あめが ふるでしょう。',
         'why': 'でしょう terminates; do not append だ/です.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たかいですでしょう。', 'correct': 'たかい でしょう。',
         'why': 'でしょう attaches to PLAIN form (drop です first): たかい+でしょう.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'がくせいでしょう ですか。', 'correct': 'がくせいでしょう。',
         'why': 'でしょう can be a question on its own (rising tone); do not add ですか.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-160': [  # Noun + の + あとで
        {'wrong': 'がっこうあとで、 いきます。', 'correct': 'がっこうのあとで、 いきます。',
         'why': 'Noun + あとで needs の: N + の + あとで.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'がっこうのあと いきます。', 'correct': 'がっこうのあとで いきます。',
         'why': 'あと needs で in this construction (after-of).',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'がっこうのあとに いきます。', 'correct': 'がっこうのあとで いきます。',
         'why': 'Standard particle is で (sometimes に is used in narrative; で is more common in N5).',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-161': [  # Noun + の + まえに
        {'wrong': 'がっこうまえに、 たべます。', 'correct': 'がっこうのまえに、 たべます。',
         'why': 'Noun + まえに needs の.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'がっこうのまえで、 たべます。 (intent: before going to school)',
         'correct': 'がっこうのまえに、 たべます。',
         'why': 'まえに for "before (time)"; まえで is a different meaning ("in front of").',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'にじのまえで、 きました。 (time intent)', 'correct': 'にじのまえに、 きました。',
         'why': 'Time-before takes に, not で.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-164': [  # ～さん
        {'wrong': 'わたしさんは がくせいです。 (about yourself)',
         'correct': 'わたしは がくせいです。',
         'why': 'Never add さん to your own name. さん is for OTHERS.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'やまださまさん。', 'correct': 'やまださま。 / やまださん。',
         'why': 'Do not stack honorifics さま + さん; choose one (さま is more formal).',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'せんせいさん。', 'correct': 'せんせい。',
         'why': 'せんせい already a title; do not add さん.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
    ],
    'n5-165': [  # お～ / ご～
        {'wrong': 'おビール。', 'correct': 'ビール。',
         'why': 'お/ご prefix is for native Japanese words; foreign loan-words (ビール) do not take it.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'お がっこう。', 'correct': 'がっこう。',
         'why': 'お prefix on がっこう is unnecessary; only specific words take お (おちゃ, おみず, おかね etc.).',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'ごおちゃ。', 'correct': 'おちゃ。',
         'why': 'おちゃ takes お (kun-yomi); ご is for on-yomi compounds (ごはん exception).',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
    ],
    'n5-166': [  # いただきます etc.
        {'wrong': 'いただく ます。', 'correct': 'いただきます。',
         'why': 'Set phrase いただきます; not separated.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'ごちそうさまだ。', 'correct': 'ごちそうさま。 / ごちそうさまでした。',
         'why': 'Set phrase; standard polite form is ごちそうさまでした (after meal).',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'おはよう ございます。 (between intimates, casual time)',
         'correct': 'おはよう。',
         'why': 'おはようございます is polite; おはよう alone for casual.',
         'error_category': 'register', 'provenance': 'llm_curated'},
    ],
    'n5-168': [  # 〜たり〜たりする
        {'wrong': 'たべる ね、よむり する。', 'correct': 'たべたり よんだり する。',
         'why': 'たり attaches to PAST plain form: 食べた→食べたり, 読んだ→読んだり.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべたり する。 (single item)', 'correct': 'たべたり よんだり する。',
         'why': 'たり〜たり is a list; needs at least 2 items (or follow with など).',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'たべたり よんだり します ます。', 'correct': 'たべたり よんだり します。',
         'why': 'する becomes polite します at end; do not double ます.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-171': [  # Vない + ほうがいい
        {'wrong': 'たべない ほうが いいですね。 (commanding tone)',
         'correct': 'たべない ほうが いいですよ。',
         'why': 'Advice typically uses よ (informing); ね (agreement-seeking) sounds odd here.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'たべないて ほうがいい。', 'correct': 'たべない ほうがいい。',
         'why': 'Vない directly + ほうがいい (no て-form).',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべない ほうが いい です だ。', 'correct': 'たべない ほうが いいです。',
         'why': 'いい + です terminates; do not add だ.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-172': [  # 〜なくてもいい
        {'wrong': 'たべないで もいいです。', 'correct': 'たべなくても いいです。',
         'why': 'Optional negative: Vなくてもいい (drop い, use なくて+も). Vないで is for "without doing".',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべなくてもよくないです。', 'correct': 'たべなくてもいいです。 / たべなくちゃいけない。',
         'why': 'Negate the optional form by reframing — double-negation is confusing.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'たべない も いいです。', 'correct': 'たべなくてもいいです。',
         'why': 'Need full なくて + も + いいです construction.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-177': [  # 〜すぎる
        {'wrong': 'たべるすぎる。', 'correct': 'たべすぎる。',
         'why': 'すぎる attaches to V-stem (drop る from G2): 食べる→食べ+すぎる.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たかいすぎる。', 'correct': 'たかすぎる。',
         'why': 'い-Adj drops い before すぎる: 高い→高+すぎる.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'しずかいすぎる。', 'correct': 'しずかすぎる。',
         'why': 'na-Adj uses bare stem + すぎる (no な, no い). 静か→静か+すぎる.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-179': [  # 〜って
        {'wrong': 'たなかさんは くるって いいました。',
         'correct': 'たなかさんは くるって。 / たなかさんが くると いいました。',
         'why': 'って is casual quotative ("said"); often standalone. Stacking with といいました mixes registers.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'たなかさんですって? (in formal context)', 'correct': 'たなかさんですか。',
         'why': '〜って? as a question is casual; in formal context use か.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'がくせいだって、しかし わかりません。 (intent: I hear he\'s a student but I don\'t know)',
         'correct': 'がくせいだそうですが、よくわかりません。',
         'why': 'Hearsay in N5 written form is そうです; って is conversational.',
         'error_category': 'register', 'provenance': 'llm_curated'},
    ],
    'n5-188': [  # Vる + ことができます
        {'wrong': 'たべるが できます。', 'correct': 'たべることが できます。',
         'why': 'Need ことが to nominalize the verb. Bare Vる + が cannot take できる.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべることを できます。', 'correct': 'たべることが できます。',
         'why': 'Object of できる takes が, not を.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'たべますことが できます。', 'correct': 'たべることが できます。',
         'why': 'こと attaches to PLAIN form (Vる), not polite ます.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
}

# Apply
patterns_by_id = {p['id']: p for p in patterns}
added = 0
skipped = 0
for pid, entries in ENTRIES.items():
    p = patterns_by_id.get(pid)
    if not p:
        skipped += 1
        continue
    if p.get('wrong_corrected_pair'):
        skipped += 1
        continue
    p['wrong_corrected_pair'] = entries
    added += 1

print(f'New patterns covered: {added}')
print(f'Skipped: {skipped}')

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# OOS check
K = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
N5 = set()
for e in K.get('entries', []):
    g = e.get('glyph') or e.get('id','').split('.')[-1]
    if g: N5.add(g)
def is_kanji(c): return 0x4E00 <= ord(c) <= 0x9FFF

oos = {}
for pid in ENTRIES:
    p = patterns_by_id.get(pid)
    if not p: continue
    wcp = p.get('wrong_corrected_pair')
    if not isinstance(wcp, list): continue
    for entry in wcp:
        for k in ('wrong','correct','why'):
            for c in entry.get(k, ''):
                if is_kanji(c) and c not in N5:
                    oos.setdefault(c, []).append(pid)
print(f'OOS check: {len(oos)} chars: {list(oos.keys())}')

total = len(patterns)
ge3 = sum(1 for p in patterns if isinstance(p.get('wrong_corrected_pair'), list) and len(p['wrong_corrected_pair']) >= 3)
print()
print('=== FINAL ===')
print(f'  wrong_corrected_pair >=3:  {ge3}/{total}')
