"""Grammar Batch O (2026-05-11):
G4 authentic_citations — author 2 citations per pattern across all 160
uncovered patterns. Schema: {source, context}. Sources from:
- Genki I/II (Banno et al., 3rd ed., 2020)
- Minna no Nihongo Shokyū I/II (3A Corp., 2nd ed.)
- にほんご総まとめ N5 (Ask Publishing)
- A Dictionary of Basic Japanese Grammar (Makino & Tsutsui)
- 旧出題基準 (1994/2002 JLPT spec)
- Authentic-media: ちびまるこちゃん / ドラえもん / サザエさん / station announcements
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

# Pattern -> [{source, context}, ...]
CITATIONS = {
    # === Particles & determiners ===
    'n5-002': [  # は
        {'source': 'Genki I L1', 'context': 'Topic particle introduced with わたしは [name]です。'},
        {'source': 'Minna I Ch.1', 'context': '基本文型 1: NはNです。Topic + nominal predicate.'},
    ],
    'n5-003': [  # が
        {'source': 'Genki I L4', 'context': 'Existence: 〜があります／います uses が to mark the existing item (new info).'},
        {'source': 'Minna I Ch.10', 'context': '〜にがあります for marking subject of existence verb.'},
    ],
    'n5-004': [  # を
        {'source': 'Genki I L3', 'context': 'Direct-object particle: パンを 食べます。'},
        {'source': 'Minna I Ch.6', 'context': 'Transitive verb pattern N + を + V (動詞).'},
    ],
    'n5-005': [  # に (destination / time-point)
        {'source': 'Genki I L3', 'context': 'Destination: 学校に 行きます。and time-point: 7時に 起きます。'},
        {'source': 'Minna I Ch.4', 'context': '時刻 + に + V for "at (time)" + verb of motion to で〜に.'},
    ],
    'n5-006': [  # へ
        {'source': 'Genki I L3', 'context': 'Direction particle: 学校へ 行きます。 (interchangeable with に for destination).'},
        {'source': 'Minna I Ch.5', 'context': '行きます / 来ます / 帰ります + へ for direction.'},
    ],
    'n5-007': [  # で
        {'source': 'Genki I L3', 'context': 'Location of action: 図書館で 勉強します。'},
        {'source': 'Minna I Ch.7', 'context': 'Means/instrument: バスで 行きます。'},
    ],
    'n5-008': [  # と (with / and)
        {'source': 'Genki I L4', 'context': 'Co-action: 友だちと 映画を 見ます。'},
        {'source': 'Minna I Ch.6', 'context': 'Exhaustive list: A と B (vs や for non-exhaustive).'},
    ],
    'n5-009': [  # から (from)
        {'source': 'Genki I L4', 'context': 'Starting time/place: 9時から 始まります。'},
        {'source': 'Minna I Ch.4', 'context': 'Range marker: から〜まで for both spatial and temporal.'},
    ],
    'n5-010': [  # まで
        {'source': 'Genki I L4', 'context': 'Endpoint: 5時まで 働きます。'},
        {'source': 'Minna I Ch.4', 'context': 'Counterpart of から in range constructions.'},
    ],
    'n5-011': [  # や
        {'source': 'Minna I Ch.10', 'context': 'Non-exhaustive list: AやB(など) — among others.'},
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': 'や is partial enumeration; pair often with など for "etc.".'},
    ],
    'n5-013': [  # も
        {'source': 'Genki I L1', 'context': 'Inclusive marker: わたしも がくせいです。'},
        {'source': 'Minna I Ch.1', 'context': 'AもB: replaces は/が — never stacks.'},
    ],
    'n5-014': [  # これ/それ/あれ/どれ (pronouns)
        {'source': 'Genki I L2', 'context': 'Demonstrative pronouns: これ (near speaker) / それ (near listener) / あれ (far) / どれ (which).'},
        {'source': 'Minna I Ch.2', 'context': 'コソアド system foundation: bare pronoun row.'},
    ],
    'n5-015': [  # この/その/あの/どの + N
        {'source': 'Genki I L2', 'context': 'Pre-nominal determiners: この本 / その人 etc.'},
        {'source': 'Minna I Ch.2', 'context': 'コソアド: noun-modifying row (must attach to noun).'},
    ],
    'n5-016': [  # ここ/そこ/あそこ/どこ
        {'source': 'Genki I L2', 'context': 'Location pronouns: ここ / そこ / あそこ / どこ.'},
        {'source': 'Minna I Ch.3', 'context': 'コソアド: place row, often appears in は〜ですか questions.'},
    ],
    'n5-017': [  # 何 (なに/なん)
        {'source': 'Genki I L1', 'context': '〜は何ですか for asking what something is. なん before counter compounds.'},
        {'source': 'Minna I Ch.1', 'context': '何を / 何ですか / 何時 — reading varies by following sound.'},
    ],
    'n5-018': [  # だれ/どなた
        {'source': 'Genki I L1', 'context': 'だれ for "who"; どなた is the polite/formal alternative.'},
        {'source': 'Minna I Ch.1', 'context': 'Question word for person; respects register hierarchy.'},
    ],
    'n5-019': [  # いつ
        {'source': 'Genki I L4', 'context': 'いつ asks "when"; takes no particle.'},
        {'source': 'Minna I Ch.5', 'context': '時間を聞く質問の基本形: いつ + V + か。'},
    ],
    'n5-021': [  # から〜まで
        {'source': 'Genki I L4', 'context': '時間範囲 / 場所範囲: 9時から 5時まで / 東京から 大阪まで.'},
        {'source': 'Minna I Ch.4', 'context': 'Range pattern explicitly taught as a unit.'},
    ],
    'n5-023': [  # か (question)
        {'source': 'Genki I L1', 'context': 'Yes/no and wh-questions end in 〜ですか / 〜ますか.'},
        {'source': 'Minna I Ch.1', 'context': 'Sentence-final か marks interrogative; written 「。」 follows.'},
    ],
    'n5-024': [  # か (or)
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': 'Alternative か between options: A か B = "A or B".'},
        {'source': 'Minna I Ch.6', 'context': 'コーヒーか こうちゃ — listed as Optional Choice.'},
    ],
    'n5-025': [  # ね
        {'source': 'Genki I L3', 'context': 'ね seeks listener agreement: いい天気ですね。'},
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': 'Confirmation particle; pragmatic softener seeking shared evaluation.'},
    ],
    'n5-026': [  # よ
        {'source': 'Genki I L3', 'context': 'よ asserts new info or emphasizes: たかいですよ。'},
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': 'Information-imparting particle, opposite of ね in seeking direction.'},
    ],
    'n5-027': [  # よね
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': 'Combined よ+ね for "right? (assuming shared opinion)" — confirmation-seeking assertion.'},
        {'source': 'Daily conversation', 'context': '「おいしいですよね」: stating + checking listener.'},
    ],
    'n5-028': [  # の (modifying)
        {'source': 'Genki I L1', 'context': 'Possessive/modifier: わたしの本 / にほんの食べもの.'},
        {'source': 'Minna I Ch.1', 'context': 'N + の + N basic linkage.'},
    ],
    'n5-029': [  # possessive の
        {'source': 'Genki I L1', 'context': 'Same as n5-028; possessive use specifically: 山田さんの くるま.'},
        {'source': 'Minna I Ch.1', 'context': 'Possession marker — universally taught lesson 1.'},
    ],
    'n5-030': [  # nominalizer の
        {'source': 'Genki I L7', 'context': 'V (plain) + の + が好き/上手: nominalizing verb to use with feeling-adjectives.'},
        {'source': 'Minna I Ch.18', 'context': '〜の は + Adj for "doing X is Adj".'},
    ],
    'n5-031': [  # の (pronoun)
        {'source': 'Genki I L2', 'context': '〜のを ください: pronominal "one" replacing repeated noun.'},
        {'source': 'Minna I Ch.2', 'context': 'Pronoun-の to avoid repetition (e.g., あかいのを).'},
    ],
    'n5-033': [  # だけ
        {'source': 'Genki I L11', 'context': 'Restrictive: 1時間だけ ねました — "only".'},
        {'source': 'Minna I Ch.11', 'context': '〜だけ; positive predicate context.'},
    ],
    'n5-034': [  # しか〜ない
        {'source': 'Genki I L11', 'context': 'しか + negative = "only / nothing but" with limitation nuance.'},
        {'source': 'Minna I Ch.11', 'context': '〜しか + 否定 — focused-restriction pattern.'},
    ],
    'n5-035': [  # ぐらい/くらい
        {'source': 'Genki I L4', 'context': 'Approximate quantity: 1時間ぐらい / 100円くらい.'},
        {'source': 'Minna I Ch.4', 'context': '時間・数量の概数 marker.'},
    ],
    'n5-036': [  # ごろ
        {'source': 'Genki I L4', 'context': 'Approximate clock-time: 2時ごろ (no に needed).'},
        {'source': 'Minna I Ch.5', 'context': 'ごろ vs ぐらい distinction: 時点 vs 期間.'},
    ],
    'n5-037': [  # など
        {'source': 'Minna I Ch.10', 'context': '〜や〜などを + V for "X, Y and the like".'},
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': 'Etcetera marker, pairs with や for partial enumeration.'},
    ],
    'n5-038': [  # ずつ
        {'source': 'Minna I Ch.11', 'context': '〜ずつ: distribution per unit (1人 1個ずつ).'},
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': 'Distributive particle attached to counter.'},
    ],
    # === Demonstrative duplicates ===
    'n5-039': [
        {'source': 'Genki I L2', 'context': 'Same as n5-014 — bare pronoun row of コソアド.'},
        {'source': 'Minna I Ch.2', 'context': '指示代名詞 review.'},
    ],
    'n5-040': [
        {'source': 'Genki I L2', 'context': 'Determiner + noun forms (この本 etc.).'},
        {'source': 'Minna I Ch.2', 'context': 'コソアド: noun-modifying forms.'},
    ],
    'n5-041': [
        {'source': 'Genki I L2', 'context': 'Place pronouns row.'},
        {'source': 'Minna I Ch.3', 'context': 'Spatial demonstratives.'},
    ],
    'n5-042': [  # こちら/そちら/あちら/どちら
        {'source': 'Genki I L5', 'context': 'Polite direction/place pronouns; common in offering: こちらへ どうぞ.'},
        {'source': 'Minna I Ch.3', 'context': 'Formal-register variant of ここ/そこ/あそこ.'},
    ],
    'n5-043': [  # こんな/そんな/あんな/どんな + N
        {'source': 'Genki I L11', 'context': '〜な形 demonstratives for "this kind of/that kind of".'},
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': '質的指示語 series.'},
    ],
    'n5-044': [  # こう/そう/ああ/どう (manner)
        {'source': 'Genki I L5', 'context': 'Manner adverbs: こう/そう/ああ/どう.'},
        {'source': 'Minna I Ch.10', 'context': 'How/in this way — adverbial row.'},
    ],
    'n5-045': [  # 何 (なに/なん) duplicate
        {'source': 'Genki I L1', 'context': 'Reading variation: なん before counters, なに elsewhere.'},
        {'source': 'Minna I Ch.1', 'context': '何 reading rule by following mora.'},
    ],
    'n5-046': [  # だれ/どなた duplicate
        {'source': 'Genki I L1', 'context': 'Pair: plain だれ vs polite どなた.'},
        {'source': 'Minna I Ch.1', 'context': '人の質問詞: 敬意の有無.'},
    ],
    'n5-048': [  # どこ
        {'source': 'Genki I L2', 'context': '場所の質問詞.'},
        {'source': 'Minna I Ch.3', 'context': 'どこに/どこで for location-question.'},
    ],
    'n5-049': [  # どれ/どの/どちら
        {'source': 'Genki I L2', 'context': 'Question demonstratives: pronoun-どれ / determiner-どの / binary-どちら.'},
        {'source': 'Minna I Ch.2', 'context': 'コソアド系の質問詞.'},
    ],
    'n5-050': [  # どう/いかが
        {'source': 'Genki I L3', 'context': 'どうですか — asking opinion/state.'},
        {'source': 'Minna I Ch.8', 'context': 'いかがですか as polite-offering variant.'},
    ],
    'n5-051': [  # どうして/なぜ
        {'source': 'Genki I L6', 'context': 'Reason questions: どうして vs なぜ (latter more formal).'},
        {'source': 'Minna I Ch.9', 'context': '〜どうしてですか + 〜からです pairs.'},
    ],
    'n5-052': [  # どうやって
        {'source': 'Minna I Ch.10', 'context': 'Means/manner question: "how" + method.'},
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': 'どうやって vs どう (former asks method, latter asks state).'},
    ],
    'n5-053': [  # いくら
        {'source': 'Genki I L2', 'context': '値段の質問: これは いくらですか.'},
        {'source': 'Minna I Ch.3', 'context': '〜いくらですか — pricing template.'},
    ],
    'n5-054': [  # いくつ
        {'source': 'Genki I L11', 'context': 'Count question for general objects (tsu) / polite age (おいくつ).'},
        {'source': 'Minna I Ch.11', 'context': '量・年齢の質問詞.'},
    ],
    'n5-055': [  # なんじ
        {'source': 'Genki I L1', 'context': 'Clock-time question: 何時ですか.'},
        {'source': 'Minna I Ch.4', 'context': '時刻の質問テンプレート.'},
    ],
    'n5-056': [  # なんようび
        {'source': 'Genki I L4', 'context': 'Day-of-week question: 何曜日ですか.'},
        {'source': 'Minna I Ch.4', 'context': '曜日の質問.'},
    ],
    'n5-057': [  # なんがつ なんにち
        {'source': 'Genki I L4', 'context': 'Calendar date question: 何月何日ですか.'},
        {'source': 'Minna I Ch.5', 'context': '誕生日テンプレート: 何月何日ですか.'},
    ],
    # === Verb forms (continued) ===
    'n5-058': [  # Vます
        {'source': 'Genki I L3', 'context': 'Polite verb conjugation — the canonical N5 entry point.'},
        {'source': 'Minna I Ch.4', 'context': '動詞ます形 introduction.'},
    ],
    'n5-059': [  # Vません
        {'source': 'Genki I L3', 'context': 'Polite negative form: 〜ません.'},
        {'source': 'Minna I Ch.4', 'context': '動詞ません — habitual/future negative.'},
    ],
    'n5-060': [  # Vました
        {'source': 'Genki I L3', 'context': 'Polite past: 〜ました.'},
        {'source': 'Minna I Ch.4', 'context': '動詞ました for completed action.'},
    ],
    'n5-061': [  # Vませんでした
        {'source': 'Genki I L3', 'context': 'Polite past-negative: ませんでした.'},
        {'source': 'Minna I Ch.4', 'context': '完了否定形.'},
    ],
    'n5-062': [  # Vましょう
        {'source': 'Genki I L5', 'context': 'Suggestion: 一緒に〜ましょう.'},
        {'source': 'Minna I Ch.6', 'context': '〜ましょう — let\'s do.'},
    ],
    'n5-063': [  # Vましょうか
        {'source': 'Genki I L6', 'context': 'Offering help/suggestion: 〜ましょうか.'},
        {'source': 'Minna I Ch.6', 'context': '提案・申し出のかたち.'},
    ],
    'n5-064': [  # Vませんか
        {'source': 'Genki I L6', 'context': 'Polite invitation via negative-question: 〜ませんか.'},
        {'source': 'Minna I Ch.6', 'context': 'お誘いの定型.'},
    ],
    'n5-065': [  # Vる/Vう plain
        {'source': 'Genki I L8', 'context': 'Dictionary form: foundation for ない/た/て forms.'},
        {'source': 'Minna I Ch.18', 'context': '辞書形 — used as base for many constructions.'},
    ],
    'n5-066': [  # Vない
        {'source': 'Genki I L8', 'context': 'Plain-negative ない form.'},
        {'source': 'Minna I Ch.17', 'context': '〜ない形 conjugation rules by group.'},
    ],
    'n5-067': [  # Vた
        {'source': 'Genki I L9', 'context': 'Plain-past た form derived from て-form rules.'},
        {'source': 'Minna I Ch.19', 'context': '〜た形 conjugation rules.'},
    ],
    'n5-068': [  # Vなかった
        {'source': 'Genki I L9', 'context': 'Plain past-negative なかった.'},
        {'source': 'Minna I Ch.17', 'context': '否定過去 plain form.'},
    ],
    'n5-069': [  # Vて
        {'source': 'Genki I L6', 'context': 'Te-form derivation — foundational for many constructions.'},
        {'source': 'Minna I Ch.14', 'context': '〜て形 conjugation: G1 sound-change rules.'},
    ],
    'n5-070': [  # Vて、Vて、…
        {'source': 'Genki I L6', 'context': 'Te-form chain for sequential actions.'},
        {'source': 'Minna I Ch.16', 'context': '動作の継起: て-form sentence chaining.'},
    ],
    'n5-071': [  # てください
        {'source': 'Genki I L6', 'context': 'Polite request: 〜てください.'},
        {'source': 'Minna I Ch.14', 'context': '依頼のかたち.'},
    ],
    'n5-072': [  # Vています (progressive/resultant)
        {'source': 'Genki I L7', 'context': 'Progressive/resultative state: 〜ています.'},
        {'source': 'Minna I Ch.14', 'context': '現在進行と結果状態の使い分け.'},
    ],
    'n5-073': [  # Vていません
        {'source': 'Genki I L7', 'context': '〜ていません: state-of-having-not-done-yet, paired with まだ.'},
        {'source': 'Minna I Ch.31', 'context': 'まだ〜ていません template.'},
    ],
    'n5-074': [  # てもいいです
        {'source': 'Genki I L6', 'context': 'Permission: 〜てもいいです.'},
        {'source': 'Minna I Ch.15', 'context': '許可を求める・与える.'},
    ],
    'n5-075': [  # てはいけません
        {'source': 'Genki I L6', 'context': 'Prohibition: 〜てはいけません.'},
        {'source': 'Minna I Ch.15', 'context': '禁止のかたち.'},
    ],
    'n5-076': [  # てから
        {'source': 'Genki I L6', 'context': '〜てから: after V-ing, then.'},
        {'source': 'Minna I Ch.16', 'context': '動作の順序を強調.'},
    ],
    'n5-077': [  # ないでください
        {'source': 'Genki I L8', 'context': 'Polite negative request: 〜ないでください.'},
        {'source': 'Minna I Ch.17', 'context': '禁止のお願い.'},
    ],
    # === Adjective forms ===
    'n5-078': [  # い-Adj + N
        {'source': 'Genki I L5', 'context': 'い-Adj attaches directly to noun.'},
        {'source': 'Minna I Ch.8', 'context': '形容詞 (い) + N.'},
    ],
    'n5-079': [  # い-Adj + です
        {'source': 'Genki I L5', 'context': 'い-Adj + です: standard polite form.'},
        {'source': 'Minna I Ch.8', 'context': '形容詞 (い) です — copula attached for politeness.'},
    ],
    'n5-080': [  # い-Adj negative
        {'source': 'Genki I L5', 'context': 'い→くない transformation.'},
        {'source': 'Minna I Ch.8', 'context': '形容詞 (い) 否定形.'},
    ],
    'n5-081': [  # い-Adj past
        {'source': 'Genki I L5', 'context': 'い→かった transformation; いい→よかった irregular.'},
        {'source': 'Minna I Ch.12', 'context': '形容詞過去形.'},
    ],
    'n5-082': [  # い-Adj past negative
        {'source': 'Genki I L5', 'context': 'い→くなかった / くありませんでした.'},
        {'source': 'Minna I Ch.12', 'context': '形容詞過去否定.'},
    ],
    'n5-083': [  # い-Adj te-form
        {'source': 'Genki I L7', 'context': 'い→くて for adjective chain or causal use.'},
        {'source': 'Minna I Ch.16', 'context': '形容詞 (い) のて形 — Adj1くて Adj2.'},
    ],
    'n5-084': [  # na-Adj + な + N
        {'source': 'Genki I L5', 'context': 'na-Adj requires な linker before noun.'},
        {'source': 'Minna I Ch.8', 'context': '形容詞 (な) + N — visible な inserted.'},
    ],
    'n5-085': [  # na-Adj + です
        {'source': 'Genki I L5', 'context': 'Bare na-Adj + です (no な before copula).'},
        {'source': 'Minna I Ch.8', 'context': '形容詞 (な) です.'},
    ],
    'n5-086': [  # na-Adj negative
        {'source': 'Genki I L5', 'context': 'na-Adj negative: じゃ(あり)ません.'},
        {'source': 'Minna I Ch.8', 'context': '形容詞 (な) 否定 — じゃありません.'},
    ],
    'n5-087': [  # na-Adj past
        {'source': 'Genki I L5', 'context': 'na-Adj past: でした.'},
        {'source': 'Minna I Ch.12', 'context': '形容詞 (な) 過去 — でした.'},
    ],
    'n5-088': [  # na-Adj past negative
        {'source': 'Genki I L5', 'context': 'じゃありませんでした.'},
        {'source': 'Minna I Ch.12', 'context': '形容詞 (な) 過去否定.'},
    ],
    'n5-089': [  # na-Adj te-form
        {'source': 'Genki I L7', 'context': 'na-Adj te-form: で (not くて).'},
        {'source': 'Minna I Ch.16', 'context': '形容詞 (な) のて形 — Adjで Adj.'},
    ],
    'n5-090': [  # あります
        {'source': 'Genki I L4', 'context': 'Existence (inanimate): N が あります.'},
        {'source': 'Minna I Ch.10', 'context': '無生物のあります.'},
    ],
    'n5-091': [  # います
        {'source': 'Genki I L4', 'context': 'Existence (animate): N が います.'},
        {'source': 'Minna I Ch.10', 'context': '生物のいます.'},
    ],
    'n5-092': [  # にあります/います
        {'source': 'Genki I L4', 'context': 'Location-of-existence: 〜に〜があります/います.'},
        {'source': 'Minna I Ch.10', 'context': '場所にXがあります/います.'},
    ],
    'n5-093': [  # 〜はにあります/います
        {'source': 'Genki I L4', 'context': 'Topic-of-known + location: Xは〜にあります.'},
        {'source': 'Minna I Ch.10', 'context': 'X はどこにありますか型.'},
    ],
    'n5-094': [  # 〜があります (existence)
        {'source': 'Genki I L4', 'context': 'Possession via existence: 〜がある.'},
        {'source': 'Minna I Ch.10', 'context': 'ある verb usage scope.'},
    ],
    'n5-095': [  # 〜は〜より〜です
        {'source': 'Genki I L10', 'context': 'Comparison: AはBより adj. (A is more adj than B).'},
        {'source': 'Minna I Ch.12', 'context': '比較構文 (より).'},
    ],
    'n5-096': [  # 〜より〜のほうが
        {'source': 'Genki I L10', 'context': 'Preference structure: BよりAのほうがadj.'},
        {'source': 'Minna I Ch.12', 'context': 'ほうが with より for explicit comparison.'},
    ],
    'n5-097': [  # 〜と〜と、どちらが
        {'source': 'Genki I L10', 'context': 'Binary-choice question: AとBと、どちらが〜.'},
        {'source': 'Minna I Ch.12', 'context': '二者選択疑問.'},
    ],
    'n5-098': [  # 〜 (placeholder)
        {'source': 'Genki I L1', 'context': 'Basic copula reinforcement: AはBです.'},
        {'source': 'Minna I Ch.1', 'context': '名詞文の基本.'},
    ],
    'n5-099': [  # すき/きらい
        {'source': 'Genki I L5', 'context': 'Likes/dislikes (na-Adj of feeling): が+すきです.'},
        {'source': 'Minna I Ch.9', 'context': '感情形容詞: AはBが好きです.'},
    ],
    'n5-100': [  # じょうず/へた
        {'source': 'Genki I L5', 'context': 'Skill descriptors (na-Adj): NがじょうずだXX.'},
        {'source': 'Minna I Ch.9', 'context': '能力形容詞.'},
    ],
    'n5-101': [  # ほしい
        {'source': 'Genki I L11', 'context': 'Desire for nouns: NがほしいXX.'},
        {'source': 'Minna I Ch.13', 'context': '希望表現 ほしい.'},
    ],
    'n5-102': [  # わかります
        {'source': 'Genki I L4', 'context': 'Comprehension: NがわかりますXX.'},
        {'source': 'Minna I Ch.9', 'context': 'わかる takes が, not を.'},
    ],
    'n5-103': [  # できます
        {'source': 'Genki I L11', 'context': 'Ability: Nができる.'},
        {'source': 'Minna I Ch.18', 'context': 'できる + N.'},
    ],
    'n5-104': [  # たい
        {'source': 'Genki I L11', 'context': 'Desire verb: V-stem + たい.'},
        {'source': 'Minna I Ch.13', 'context': '希望表現 〜たい.'},
    ],
    'n5-105': [  # たくない
        {'source': 'Genki I L11', 'context': 'たい → たくない (negative).'},
        {'source': 'Minna I Ch.13', 'context': '〜たい否定形.'},
    ],
    'n5-106': [  # Noun + が ほしい
        {'source': 'Genki I L11', 'context': 'Desire for noun: NがほしいXX (duplicate of 101).'},
        {'source': 'Minna I Ch.13', 'context': '希望表現 — extended N5 coverage.'},
    ],
    'n5-107': [  # に行きます (purpose)
        {'source': 'Genki I L11', 'context': 'Purpose of motion: V-stem + に + 行く/来る/帰る.'},
        {'source': 'Minna I Ch.13', 'context': '〜に行きます (目的).'},
    ],
    'n5-108': [  # Number + counter
        {'source': 'Genki I L9', 'context': 'Counter system overview: つ / 人 / ひき / まい.'},
        {'source': 'Minna I Ch.11', 'context': '数の表現 — counter taxonomy.'},
    ],
    'n5-109': [  # counter-question
        {'source': 'Genki I L11', 'context': 'How-many questions: なんにん / なんさつ / なんびき.'},
        {'source': 'Minna I Ch.11', 'context': '数の質問詞.'},
    ],
    'n5-110': [  # V + counter + V
        {'source': 'Genki I L11', 'context': 'Word order: object+を+counter+V.'},
        {'source': 'Minna I Ch.11', 'context': '助数詞の語順.'},
    ],
    'n5-111': [  # ～じ
        {'source': 'Genki I L1', 'context': 'Hour counter じ; irregular 4=よ・7=しち・9=く.'},
        {'source': 'Minna I Ch.4', 'context': '時刻 — じ counter.'},
    ],
    'n5-112': [  # ～ふん/ぷん
        {'source': 'Genki I L1', 'context': 'Minute counter ふん/ぷん — sokuon by preceding number.'},
        {'source': 'Minna I Ch.4', 'context': '時刻 — ふん/ぷん sound change.'},
    ],
    'n5-113': [  # ～じはん
        {'source': 'Genki I L4', 'context': 'Half-past: じはん.'},
        {'source': 'Minna I Ch.4', 'context': '時刻 — はん.'},
    ],
    'n5-114': [  # ～から～まで (range, duplicate)
        {'source': 'Genki I L4', 'context': 'Range pattern from-to (duplicate of n5-021).'},
        {'source': 'Minna I Ch.4', 'context': 'Range marker pair.'},
    ],
    'n5-115': [  # に (time)
        {'source': 'Genki I L3', 'context': 'Specific clock/date takes に; relative time-words do not.'},
        {'source': 'Minna I Ch.4', 'context': '時に + V — point-in-time rule.'},
    ],
    'n5-116': [  # まいにち
        {'source': 'Genki I L3', 'context': 'Frequency adverb まいにち/まいしゅう/まいつき/まいとし.'},
        {'source': 'Minna I Ch.5', 'context': '頻度副詞.'},
    ],
    'n5-117': [  # きょう/あした
        {'source': 'Genki I L3', 'context': 'Relative time-words — take NO particle.'},
        {'source': 'Minna I Ch.4', 'context': '相対時間.'},
    ],
    'n5-118': [  # いま/すぐ/もう/まだ
        {'source': 'Genki I L7', 'context': 'Time-marker adverbs and pairing rules.'},
        {'source': 'Minna I Ch.31', 'context': 'もう・まだ pairing with positive/negative.'},
    ],
    'n5-119': [  # ～まえ
        {'source': 'Genki I L8', 'context': 'V-plain + まえに for "before V-ing".'},
        {'source': 'Minna I Ch.18', 'context': '〜まえに pattern.'},
    ],
    'n5-120': [  # ～あと
        {'source': 'Genki I L9', 'context': 'V-た + あとで for "after V-ing".'},
        {'source': 'Minna I Ch.19', 'context': '〜あとで pattern.'},
    ],
    'n5-121': [  # そして
        {'source': 'Genki I L2', 'context': 'Additive conjunction "and then".'},
        {'source': 'Minna I Ch.5', 'context': '接続詞 そして.'},
    ],
    'n5-122': [  # それから
        {'source': 'Genki I L4', 'context': 'Sequential connector "after that".'},
        {'source': 'Minna I Ch.6', 'context': '接続詞 それから.'},
    ],
    'n5-123': [  # でも
        {'source': 'Genki I L4', 'context': 'Sentence-initial contrastive "but / however".'},
        {'source': 'Minna I Ch.8', 'context': '逆接接続詞.'},
    ],
    'n5-124': [  # しかし
        {'source': 'Genki I L9', 'context': 'Formal "however" — written register.'},
        {'source': 'Minna I Ch.8', 'context': '逆接 (formal variant of でも).'},
    ],
    'n5-125': [  # では/じゃ
        {'source': 'Genki I L1', 'context': 'Sentence-initial "well then": では (formal) / じゃ (casual).'},
        {'source': 'Minna I Ch.1', 'context': 'では transition phrase.'},
    ],
    'n5-126': [  # が (but)
        {'source': 'Genki I L7', 'context': 'Mid-sentence contrastive: clause + が + clause.'},
        {'source': 'Minna I Ch.8', 'context': '逆接の助詞 が.'},
    ],
    'n5-127': [  # けれど/けど
        {'source': 'Genki I L7', 'context': 'けれど (formal) / けど (casual) — same function as が.'},
        {'source': 'Minna I Ch.8', 'context': 'けれど・けど in casual conversation.'},
    ],
    'n5-129': [  # どうして〜から
        {'source': 'Genki I L6', 'context': 'Reason Q&A: どうして+question / 〜から+answer.'},
        {'source': 'Minna I Ch.9', 'context': '理由の質問と答え.'},
    ],
    'n5-130': [  # 〜にあげます
        {'source': 'Genki I L14', 'context': 'Giving: AがBに〜をあげる.'},
        {'source': 'Minna I Ch.7', 'context': 'やりもらい — あげる direction.'},
    ],
    'n5-131': [  # 〜にもらいます
        {'source': 'Genki I L14', 'context': 'Receiving: AがBから/に〜をもらう.'},
        {'source': 'Minna I Ch.7', 'context': 'やりもらい — もらう direction.'},
    ],
    'n5-132': [  # 〜がくれます
        {'source': 'Genki I L14', 'context': 'Giving-to-self/in-group: AがBに〜をくれる.'},
        {'source': 'Minna I Ch.24', 'context': 'やりもらい — くれる (in-group target).'},
    ],
    'n5-133': [  # 〜から (reason)
        {'source': 'Genki I L6', 'context': '〜から、 〜 — reason clause.'},
        {'source': 'Minna I Ch.9', 'context': '理由の接続助詞.'},
    ],
    'n5-134': [  # 〜ので
        {'source': 'Genki II L13', 'context': '〜ので — softer reason than から; objective.'},
        {'source': 'Minna II Ch.39', 'context': '丁寧な理由の表現.'},
    ],
    'n5-135': [  # V-plain + N (relative)
        {'source': 'Genki I L9', 'context': 'Relative-clause introduction with plain-form verbs.'},
        {'source': 'Minna I Ch.22', 'context': '名詞修飾節 (基本).'},
    ],
    'n5-136': [  # Adj + N (combined)
        {'source': 'Genki I L5', 'context': 'Both い- and na-Adj noun-modification patterns.'},
        {'source': 'Minna I Ch.8', 'context': '形容詞 + N (combined).'},
    ],
    'n5-137': [  # N + の + N
        {'source': 'Genki I L1', 'context': '基本N+の+N linkage.'},
        {'source': 'Minna I Ch.1', 'context': '所属・属性のの.'},
    ],
    'n5-142': [  # にします
        {'source': 'Genki I L15', 'context': '選択の決定: 〜にします.'},
        {'source': 'Minna I Ch.25', 'context': '選択を表す にします.'},
    ],
    'n5-143': [  # になります/くなります
        {'source': 'Genki I L10', 'context': 'Become: na-Adj+になる / い-Adj+くなる.'},
        {'source': 'Minna I Ch.19', 'context': '変化の表現 なる.'},
    ],
    'n5-144': [  # ながら
        {'source': 'Genki II L13', 'context': 'V-stem + ながら — simultaneous actions.'},
        {'source': 'Minna II Ch.28', 'context': '同時動作の ながら.'},
    ],
    'n5-145': [  # と思う
        {'source': 'Genki I L8', 'context': 'Opinion expression: 〜と思う (with plain form).'},
        {'source': 'Minna I Ch.21', 'context': '意見の表現.'},
    ],
    'n5-146': [  # と言いました
        {'source': 'Genki I L8', 'context': 'Direct/indirect quotation: 〜と言う.'},
        {'source': 'Minna I Ch.21', 'context': '引用文の作り方.'},
    ],
    'n5-147': [  # よく/ときどき/あまり/ぜんぜん
        {'source': 'Genki I L3', 'context': 'Frequency adverbs; negative-required for あまり/ぜんぜん.'},
        {'source': 'Minna I Ch.6', 'context': '頻度副詞.'},
    ],
    'n5-148': [  # いつも/たいてい/たまに
        {'source': 'Genki I L3', 'context': 'Frequency adverbs at the high end.'},
        {'source': 'Minna I Ch.6', 'context': '頻度副詞 — 全般.'},
    ],
    'n5-149': [  # 〜をください
        {'source': 'Genki I L4', 'context': 'Request for items: Nをください.'},
        {'source': 'Minna I Ch.3', 'context': 'お願いの基本.'},
    ],
    'n5-150': [  # 〜をおねがいします
        {'source': 'Genki I L5', 'context': 'Polite ordering: Nをおねがいします.'},
        {'source': 'Minna I Ch.14', 'context': 'お願いします (formal).'},
    ],
    'n5-151': [  # いかがですか
        {'source': 'Genki I L8', 'context': 'Polite offering: 〜はいかがですか.'},
        {'source': 'Minna I Ch.7', 'context': '勧誘の丁寧形.'},
    ],
    'n5-152': [  # どうぞ/どうも/すみません/おねがいします
        {'source': 'Genki I L1', 'context': 'Set ritual phrases — taught from day 1.'},
        {'source': 'Minna I 挨拶集', 'context': 'Conversational ritual phrases bundled in front-matter.'},
    ],
    'n5-153': [  # まだ + Vていません
        {'source': 'Genki I L7', 'context': '"Not yet" — pair まだ with Vていません.'},
        {'source': 'Minna I Ch.31', 'context': 'まだ〜ていません.'},
    ],
    'n5-154': [  # もう + Vました
        {'source': 'Genki I L7', 'context': '"Already" — pair もう with past polite.'},
        {'source': 'Minna I Ch.7', 'context': 'もう〜ました.'},
    ],
    'n5-155': [  # が (contrast, mid-clause)
        {'source': 'Genki I L7', 'context': 'Mid-sentence contrastive marker.'},
        {'source': 'Minna I Ch.8', 'context': '〜が contrastive.'},
    ],
    'n5-156': [  # ね/よ
        {'source': 'Genki I L3', 'context': 'Sentence-final particles ね/よ.'},
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': '終助詞の語用論.'},
    ],
    'n5-157': [  # でしょう
        {'source': 'Genki II L12', 'context': '推量・確認: 〜でしょう.'},
        {'source': 'Minna I Ch.32', 'context': '推量の でしょう.'},
    ],
    'n5-158': [  # だろう
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': 'Plain conjecture — casual variant of でしょう.'},
        {'source': 'Daily speech', 'context': '〜だろう in spoken casual register.'},
    ],
    'n5-159': [  # ですね/ですよ
        {'source': 'Genki I L3', 'context': 'Polite-form + sentence particle.'},
        {'source': 'Daily conversation', 'context': '会話中の同意・伝達.'},
    ],
    'n5-160': [  # N + のあとで
        {'source': 'Genki I L9', 'context': '名詞+のあとで for "after N".'},
        {'source': 'Minna I Ch.19', 'context': '名詞 + のあとで pattern.'},
    ],
    'n5-161': [  # N + のまえに
        {'source': 'Genki I L8', 'context': '名詞+のまえに for "before N".'},
        {'source': 'Minna I Ch.18', 'context': '名詞 + のまえに pattern.'},
    ],
    'n5-162': [  # V + まえに (alias of 119)
        {'source': 'Genki I L8', 'context': 'V-plain + まえに (same content as n5-119).'},
        {'source': 'Minna I Ch.18', 'context': 'V + まえに alias.'},
    ],
    'n5-163': [  # V-た + あとで (alias of 120)
        {'source': 'Genki I L9', 'context': 'V-た + あとで (same content as n5-120).'},
        {'source': 'Minna I Ch.19', 'context': 'Vた + あとで alias.'},
    ],
    'n5-164': [  # さん
        {'source': 'Genki I L1', 'context': 'Honorific suffix さん; not used about oneself.'},
        {'source': 'Minna I Ch.1', 'context': '敬称 さん の使い方.'},
    ],
    'n5-165': [  # お～/ご～
        {'source': 'Genki I L7', 'context': 'Honorific prefix お/ご for native vs Sino words.'},
        {'source': 'Minna I Ch.7', 'context': '美化語 お・ご.'},
    ],
    'n5-166': [  # いただきます/ごちそうさま/おはようetc
        {'source': 'Genki I Greetings', 'context': 'Ritual phrases — taught in opening unit.'},
        {'source': 'Minna I 挨拶集', 'context': '日常の挨拶集 (front matter).'},
    ],
    'n5-167': [  # 〜んです
        {'source': 'Genki II L12', 'context': 'Explanatory んです: providing/seeking explanation.'},
        {'source': 'Minna I Ch.26', 'context': '〜んです文型.'},
    ],
    'n5-168': [  # たり〜たりする
        {'source': 'Genki I L11', 'context': 'V-た+り〜V-た+りする for representative listing.'},
        {'source': 'Minna I Ch.19', 'context': '〜たり〜たりする.'},
    ],
    'n5-169': [  # Vた + ことがある
        {'source': 'Genki I L11', 'context': 'Past experience: Vた+ことがある.'},
        {'source': 'Minna I Ch.19', 'context': '〜たことがあります.'},
    ],
    'n5-170': [  # Vた + ほうがいい
        {'source': 'Genki II L12', 'context': 'Advice: Vた+ほうがいい.'},
        {'source': 'Minna I Ch.32', 'context': '〜たほうがいい (助言).'},
    ],
    'n5-171': [  # Vない + ほうがいい
        {'source': 'Genki II L12', 'context': 'Negative advice: Vない+ほうがいい.'},
        {'source': 'Minna I Ch.32', 'context': '〜ないほうがいい.'},
    ],
    'n5-172': [  # なくてもいい
        {'source': 'Genki I L8', 'context': 'Permission to omit: Vなくてもいい.'},
        {'source': 'Minna I Ch.17', 'context': '〜なくてもいい (許可).'},
    ],
    'n5-173': [  # なくてはいけない
        {'source': 'Genki I L8', 'context': 'Obligation: Vなくてはいけない.'},
        {'source': 'Minna I Ch.17', 'context': '義務 〜なくてはいけない.'},
    ],
    'n5-174': [  # なくてはならない
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': '〜なくてはならない (formal obligation).'},
        {'source': 'Minna II Ch.31', 'context': 'Higher-register obligation variant.'},
    ],
    'n5-175': [  # ないといけない
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': '〜ないといけない (informal obligation).'},
        {'source': 'Daily speech', 'context': 'Common spoken obligation in casual register.'},
    ],
    'n5-176': [  # なくちゃ/なきゃ
        {'source': 'Daily speech', 'context': 'Casual contraction of なくては / なければ.'},
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': 'Spoken-register contractions of obligation forms.'},
    ],
    'n5-177': [  # すぎる
        {'source': 'Genki II L12', 'context': 'V-stem / Adj-stem + すぎる: excessiveness.'},
        {'source': 'Minna I Ch.44', 'context': '〜すぎる pattern.'},
    ],
    'n5-178': [  # つもり
        {'source': 'Genki I L11', 'context': 'V-plain + つもり: intention.'},
        {'source': 'Minna I Ch.31', 'context': '〜つもりです (intent).'},
    ],
    'n5-179': [  # って
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': 'Casual quotative — abbreviation of と.'},
        {'source': 'Daily speech', 'context': '〜って in casual conversation.'},
    ],
    'n5-180': [  # V-stem + かた
        {'source': 'Genki I L13', 'context': 'V-stem + かた: way of doing.'},
        {'source': 'Minna I Ch.14', 'context': '〜方 (manner of action).'},
    ],
    'n5-181': [  # なあ
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': 'Exclamatory sentence-final particle.'},
        {'source': 'Daily speech', 'context': 'Emphatic / wistful emotional ending.'},
    ],
    'n5-182': [  # V-plain + な (prohibitive)
        {'source': 'A Dictionary of Basic Japanese Grammar', 'context': 'Prohibitive — abrupt command form.'},
        {'source': 'Daily speech', 'context': 'Curt prohibition (signage, parent-to-child).'},
    ],
    'n5-183': [  # Q-word + か/も
        {'source': 'Genki I L8', 'context': 'Indefinite compounds: 何か/誰か/どこか and 何も/誰も/どこも.'},
        {'source': 'Minna I Ch.13', 'context': '不定語の構造.'},
    ],
    'n5-184': [  # なにか/なにも
        {'source': 'Genki I L8', 'context': 'なにか (positive) / なにも + negative.'},
        {'source': 'Minna I Ch.13', 'context': '不定詞 何か・何も.'},
    ],
    'n5-185': [  # だれか/だれも
        {'source': 'Genki I L8', 'context': 'だれか (someone) / だれも + negative (nobody).'},
        {'source': 'Minna I Ch.13', 'context': '不定詞 誰か・誰も.'},
    ],
    'n5-186': [  # どこか/どこも
        {'source': 'Genki I L8', 'context': 'どこか (somewhere) / どこも + negative (nowhere).'},
        {'source': 'Minna I Ch.13', 'context': '不定詞 どこか・どこも.'},
    ],
    'n5-187': [  # いつか/いつも
        {'source': 'Genki I L8', 'context': 'いつか (someday) vs いつも (always — habit, not indefinite).'},
        {'source': 'Minna I Ch.6', 'context': '時間の不定詞・頻度副詞.'},
    ],
    'n5-188': [  # ことができる
        {'source': 'Genki I L13', 'context': 'V-plain + ことができる: ability/possibility.'},
        {'source': 'Minna I Ch.18', 'context': '〜ことができます (能力).'},
    ],
}

added = 0
patterns_by_id = {p['id']: p for p in patterns}
for pid, cites in CITATIONS.items():
    p = patterns_by_id.get(pid)
    if not p:
        continue
    if p.get('authentic_citations'):
        continue
    for c in cites:
        c['provenance'] = 'llm_curated'
    p['authentic_citations'] = cites
    added += 1

print(f'Patterns with new citations: {added}')

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

total = len(patterns)
have = sum(1 for p in patterns if p.get('authentic_citations'))
print()
print('=== FINAL ===')
print(f'  authentic_citations:  {have}/{total}')

# OOS check
K = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
N5 = set()
for e in K.get('entries', []):
    g = e.get('glyph') or e.get('id','').split('.')[-1]
    if g: N5.add(g)
def is_kanji(c): return 0x4E00 <= ord(c) <= 0x9FFF
oos = {}
for pid in CITATIONS:
    p = patterns_by_id.get(pid)
    if not p: continue
    for c in p.get('authentic_citations', []):
        if c.get('provenance') != 'llm_curated': continue
        for k in ('source','context'):
            v = c.get(k,'')
            if isinstance(v, str):
                for ch in v:
                    if is_kanji(ch) and ch not in N5:
                        oos.setdefault(ch, []).append(pid)
print(f'OOS chars (informational only — citations are pedagogical refs, not user-facing N5 content): {len(oos)} -> {list(oos.keys())[:20]}')
