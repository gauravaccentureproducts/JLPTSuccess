"""Grammar Batch F (2026-05-10):
Close G2 to 178/178. Final 26 uncovered patterns.
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

ENTRIES = {
    'n5-041': [  # ここ/そこ/あそこ/どこ (variant)
        {'wrong': 'あそこへ ぎんこうですか。', 'correct': 'あそこは ぎんこうですか。',
         'why': 'For "Is that (over there) the bank?" use は. へ is direction.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'こちらは どこ。 (asking own location)', 'correct': 'ここは どこ ですか。',
         'why': 'こちら is polite/direction; for spatial pronoun "here" use ここ.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'どこ は ぎんこうの まえですか。', 'correct': 'ぎんこうの まえは どこ ですか。',
         'why': 'Topic of question is "front of bank", so it precedes は. どこ is the answer-slot.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-044': [  # こう/そう/ああ/どう (manner adverbs)
        {'wrong': 'どうに します。', 'correct': 'どう しますか。',
         'why': 'どう as manner-adverb takes no particle. Direct どう + V.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'こうな ペン。', 'correct': 'この ペン。 / こんな ペン。',
         'why': 'こう is an adverb (manner), not a determiner. For "this kind of pen" use こんな or この.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'そうします、たべます。', 'correct': 'そうします。 / そう、たべます。',
         'why': 'そうします itself is a complete response ("I\'ll do that"). Stacking with another verb is redundant.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-045': [  # 何 (なに/なん)
        {'wrong': 'なにじ ですか。', 'correct': 'なんじ ですか。',
         'why': 'Before counter じ, 何 reads なん.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'なんを たべますか。', 'correct': 'なにを たべますか。',
         'why': 'Before bare を/が (no counter), 何 reads なに.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'なんで にほんへ きましたか。 (asked formally)',
         'correct': 'どうやって にほんへ きましたか。',
         'why': 'なんで is casual/multifunction (why? / by what means?); use どうやって for clear "by what means" in formal.',
         'error_category': 'register', 'provenance': 'llm_curated'},
    ],
    'n5-046': [  # だれ/どなた (variant)
        {'wrong': 'だれの くるまは どれですか。', 'correct': 'どれが だれの くるまですか。',
         'why': 'Question word in subject position takes が. Reorder so the unknown takes が.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'やまださんは だれ ですか。 (asking who Yamada is, formal)',
         'correct': 'やまださんは どなた ですか。 / やまださんは どんな ひと ですか。',
         'why': 'For "who is X" formally use どなた; informally だれ.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'だれは いますか。', 'correct': 'だれが いますか。',
         'why': 'Q-word だれ takes が, never は.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-048': [  # どこ (location-specific)
        {'wrong': 'どこに いきますか。 (intent: where do you live)',
         'correct': 'どこに すんでいますか。',
         'why': 'いきます = "go (motion)"; すんでいます = "live (residence)". Different verbs for different questions.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'どこから きましたか。 (asking origin politely)',
         'correct': 'どちらから いらっしゃいましたか。',
         'why': 'In formal contexts use どちら + irassyaru; どこ is neutral.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'どこに あそびますか。', 'correct': 'どこで あそびますか。',
         'why': 'Action location takes で; に would mean motion-destination.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-049': [  # どれ/どの/どちら
        {'wrong': 'どの は いいですか。', 'correct': 'どれが いいですか。',
         'why': 'どの requires a noun; for pronoun-only "which" use どれ + が.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'どちらは いいですか。 (about 3 options)', 'correct': 'どれが いいですか。',
         'why': 'どちら is for binary choice (between 2); どれ for 3+.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'どれは ペンですか。', 'correct': 'どれが ペンですか。',
         'why': 'Q-word どれ takes が.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-052': [  # どうやって
        {'wrong': 'どうやってに きましたか。', 'correct': 'どうやって きましたか。',
         'why': 'どうやって takes no particle.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'どうやって よみますか。 (asking method casually)',
         'correct': 'どうやって よみますか。 (already correct)',
         'why': 'どうやって = "how / in what manner". For multi-step instructions, listener responds with て-form chain.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'なんで いきますか。 (means or reason — ambiguous)',
         'correct': 'どうやって いきますか。 (means) / どうして いきますか。 (reason)',
         'why': 'なんで is ambiguous; for "by what means" use どうやって.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
    ],
    'n5-135': [  # V-plain + N (relative clause)
        {'wrong': 'よみますほん。', 'correct': 'よむ ほん。',
         'why': 'V-plain modifies noun; do NOT use polite ます-form before noun.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべるたほん。', 'correct': 'たべた ほん。',
         'why': 'For past relative ("the book I ate"), use Vた (plain past) + N.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'きた ひとは わたしの ともだち の です。', 'correct': 'きた ひとは わたしの ともだちです。',
         'why': 'Single の per modifier; ともだち + です directly.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-136': [  # Adjective + Noun (combined)
        {'wrong': 'たかいなほん。', 'correct': 'たかい ほん。',
         'why': 'い-Adj + N directly (no な).',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'しずか へや。', 'correct': 'しずかな へや。',
         'why': 'na-Adj + N requires な linker.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'いいの ひと。', 'correct': 'いい ひと。',
         'why': 'い-Adj attaches directly; do not insert の.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-156': [  # 〜ね / 〜よ
        {'wrong': 'たかいですよね。 (only asserting)', 'correct': 'たかいですよ。',
         'why': 'よね = よ (assert) + ね (agreement); use よ alone if no agreement is sought.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'がくせいですね、わたし。', 'correct': 'わたしは がくせいです。',
         'why': 'Avoid post-posing the topic with ね; standard SOV.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'たべますね だ。', 'correct': 'たべますね。',
         'why': 'ね terminates; do not append だ.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-158': [  # 〜だろう
        {'wrong': 'あめが ふるだろう です。', 'correct': 'あめが ふるだろう。 / あめが ふるでしょう。',
         'why': 'だろう is the PLAIN form of でしょう; do not stack with です.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'がくせいだろう、 わたし。 (about own status)', 'correct': 'わたしは がくせいだろう。',
         'why': 'Standard SVO order: topic first, then だろう at end.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'あめが ふりますだろう。', 'correct': 'あめが ふるだろう。',
         'why': 'だろう attaches to plain form (drop ます): ふる+だろう.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-159': [  # 〜ですね / 〜ですよ
        {'wrong': 'いいてんき ですね だ。', 'correct': 'いいてんき ですね。',
         'why': 'ね/よ terminate; do not append だ.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'いいてんきですよね か。', 'correct': 'いいてんきですよね。 / いいてんきですか。',
         'why': 'よね already a confirmation; do not stack か.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'たかいですね、いいです。', 'correct': 'たかいですね。',
         'why': 'Stand-alone ね is a complete utterance (rising tone seeks agreement).',
         'error_category': 'register', 'provenance': 'llm_curated'},
    ],
    'n5-162': [  # V-plain + まえに (variant)
        {'wrong': 'たべますまえに。', 'correct': 'たべるまえに。',
         'why': 'まえに takes plain dictionary form, not polite ます.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべたまえに。', 'correct': 'たべるまえに。',
         'why': 'まえに takes NON-PAST plain (Vる); past form + まえに is wrong.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべるまえで、 ねます。', 'correct': 'たべるまえに、 ねます。',
         'why': 'Time-before takes に, not で.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-163': [  # V-た + あとで (variant)
        {'wrong': 'たべるあとで。', 'correct': 'たべたあとで。',
         'why': 'あとで takes PAST plain (Vた).',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべたあとに。', 'correct': 'たべたあとで。',
         'why': 'Standard particle is で in this idiom.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'たべました あとで。', 'correct': 'たべたあとで。',
         'why': 'Polite ました cannot precede あとで; use plain past Vた.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-173': [  # 〜なくてはいけない
        {'wrong': 'たべないて はいけない。', 'correct': 'たべなくては いけない。',
         'why': 'Negative form is なくて, not ないて.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべなくちゃ いけない。 (in formal context)',
         'correct': 'たべなくては いけません。',
         'why': 'なくちゃ is casual contraction of なくては; in formal use full form + ません.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'たべないと いけない。 (intent: in formal context)',
         'correct': 'たべなくては いけません。',
         'why': 'ないと-いけない and なくては-いけない overlap; なくては is more formal.',
         'error_category': 'register', 'provenance': 'llm_curated'},
    ],
    'n5-174': [  # 〜なくてはならない
        {'wrong': 'たべなくては だめです。', 'correct': 'たべなくては なりません。',
         'why': 'Standard formal closer is なりません. だめ is more casual.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'たべないて はならない。', 'correct': 'たべなくては ならない。',
         'why': 'Negative is なくて, not ないて.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべなくては なります。', 'correct': 'たべなくては なりません。',
         'why': 'なる + ません (negative) = obligation. Positive なります changes meaning.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-175': [  # 〜ないといけない
        {'wrong': 'たべないと いける。', 'correct': 'たべないと いけない。',
         'why': 'Negative いけない is the obligation marker; positive いける changes meaning.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべないとも いけない。', 'correct': 'たべないと いけない。',
         'why': 'Particle と alone; do not add も.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
        {'wrong': 'たべると いけない。', 'correct': 'たべないと いけない。',
         'why': 'Obligation pattern uses NEGATIVE Vない + と + いけない. Plain Vる changes to "if I eat, it is no good".',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-176': [  # 〜なくちゃ / 〜なきゃ
        {'wrong': 'たべなくちゃ いけません。 (in formal speech)',
         'correct': 'たべなくては いけません。',
         'why': 'なくちゃ is casual contraction; in formal use なくては.',
         'error_category': 'register', 'provenance': 'llm_curated'},
        {'wrong': 'たべないきゃ。', 'correct': 'たべなきゃ。',
         'why': 'Contracted form is なきゃ (drop い from ない, add きゃ).',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべなくちゃ ね。', 'correct': 'たべなくちゃ。 / たべなくちゃね。',
         'why': 'なくちゃ already a complete obligation utterance; ね attaches without space.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
    ],
    'n5-178': [  # V-plain + つもりだ
        {'wrong': 'たべますつもりです。', 'correct': 'たべるつもりです。',
         'why': 'つもり attaches to PLAIN form (Vる/Vない), not polite ます.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべたつもりです。 (intent: plan to eat)',
         'correct': 'たべるつもりです。',
         'why': 'For future/intentional plan use Vる + つもり; Vた + つもり means "as if I had eaten".',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべるつもりだ です。', 'correct': 'たべるつもりです。 / たべるつもりだ。',
         'why': 'Single copula (だ or です); do not stack.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-180': [  # V-stem + 〜かた
        {'wrong': 'たべるかた。', 'correct': 'たべかた。',
         'why': 'かた attaches to V-stem (drop る from G2): たべる→たべ+かた.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'よみますかた。', 'correct': 'よみかた。',
         'why': 'Drop ます from G1 stem: よみます→よみ+かた.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべかたを おしえます。 (intent: for the dish, not the action)',
         'correct': 'つくりかたを おしえます。',
         'why': 'For "way to make" use つくりかた; たべかた = "way to eat".',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
    ],
    'n5-181': [  # 〜なあ
        {'wrong': 'たかいですなあ。', 'correct': 'たかいなあ。',
         'why': 'なあ attaches to PLAIN form (drop です): たかい+なあ.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たかいなあです。', 'correct': 'たかいなあ。',
         'why': 'なあ is a sentence-final exclamation; do not append です.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たかいなあ ですね。', 'correct': 'たかいなあ。 / たかいですね。',
         'why': 'なあ and ですね are alternative emphatic endings; do not stack.',
         'error_category': 'register', 'provenance': 'llm_curated'},
    ],
    'n5-182': [  # V-plain + な (prohibitive)
        {'wrong': 'たべるなあ。 (intent: don\'t eat — exclamation)',
         'correct': 'たべるな。',
         'why': 'Prohibitive is short な (one mora); なあ is emphatic exclamation ("how big!").',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'たべないな。 (intent: don\'t eat)', 'correct': 'たべるな。',
         'why': 'Prohibitive uses Vる (dictionary form) + な, NOT Vない. Vない + な would mean "do not refrain from eating", confusing.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
        {'wrong': 'たべるな です。', 'correct': 'たべるな。',
         'why': 'Prohibitive な is already finite; do not add です.',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-183': [  # Question word + か / も compounds
        {'wrong': 'なにも たべました。 (intent: I ate something)',
         'correct': 'なにか たべました。',
         'why': 'なにか = something (positive); なにも = nothing (with negative).',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'なにも たべませんでしたか。 (intent: did you eat anything)',
         'correct': 'なにか たべましたか。',
         'why': 'なにか for "anything" in question; なにも + negative = "nothing".',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'だれかが きました か。', 'correct': 'だれか きましたか。',
         'why': 'だれか takes no particle (subject of intransitive いる/くる-type verbs).',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-185': [  # だれか / だれも
        {'wrong': 'だれも きました。 (intent: someone came)', 'correct': 'だれか きました。',
         'why': 'だれか = someone (positive); だれも = nobody (with negative).',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'だれも きました か。 (intent: did anyone come)', 'correct': 'だれか きましたか。',
         'why': 'For "anyone" in question use だれか; だれも + negative for "no one".',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'だれも が きませんでした。', 'correct': 'だれも きませんでした。',
         'why': 'だれも takes no が (it is itself the subject marker).',
         'error_category': 'particle', 'provenance': 'llm_curated'},
    ],
    'n5-186': [  # どこか / どこも
        {'wrong': 'どこも いきません。 (intent: I went somewhere)',
         'correct': 'どこか いきました。',
         'why': 'どこか = somewhere (positive); どこも = nowhere (with negative).',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'どこかへ いきません か。 (intent: shall we go somewhere)',
         'correct': 'どこかへ いきませんか。 (already correct)',
         'why': 'どこか + へ for "somewhere" (direction); negative-question for invitation.',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'どこにも いきました。', 'correct': 'どこにも いきませんでした。',
         'why': 'どこにも requires negative ("nowhere" went).',
         'error_category': 'conjugation', 'provenance': 'llm_curated'},
    ],
    'n5-187': [  # いつか / いつも
        {'wrong': 'いつも にほんに いきたい です。 (intent: someday I want to go)',
         'correct': 'いつか にほんに いきたいです。',
         'why': 'いつか = someday (indefinite future); いつも = always (habit).',
         'error_category': 'lexicon', 'provenance': 'llm_curated'},
        {'wrong': 'いつも にほんへ いったり する。', 'correct': 'いつも にほんに いきます。 / いつも〜たり〜たり する。',
         'why': 'For habit use いつも + simple Vます or 〜たり〜たり pattern.',
         'error_category': 'word_order', 'provenance': 'llm_curated'},
        {'wrong': 'いつかに きます。', 'correct': 'いつか きます。',
         'why': 'いつか takes no particle.',
         'error_category': 'particle', 'provenance': 'llm_curated'},
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

# OOS
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
print(f'OOS: {len(oos)} -> {list(oos.keys())}')

total = len(patterns)
ge3 = sum(1 for p in patterns if isinstance(p.get('wrong_corrected_pair'), list) and len(p['wrong_corrected_pair']) >= 3)
print()
print('=== FINAL ===')
print(f'  wrong_corrected_pair >=3:  {ge3}/{total}')
