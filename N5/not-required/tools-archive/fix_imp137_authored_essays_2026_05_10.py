"""IMP-137 follow-up: fill in why_it_matters + closing_practice_tip
on the top-30 essay scaffolds with hand-authored content.

The scaffold pass populated intro / common_pitfalls / contrasts
auto-derived from existing fields. This pass authors the two
remaining sub-fields where pedagogical content matters most:
  why_it_matters:        why a learner should care
  closing_practice_tip:  concrete drill the learner can do today

Provenance bumps from 'needs_native_review' to 'llm_curated'.
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Hand-authored content for the top-30 trickiest patterns. Keyed by
# pattern id. Each entry: {why_it_matters, closing_practice_tip}.
ESSAYS = {
    'n5-002': {  # は topic marker
        'why_it_matters': 'は is the difference between "I am a student" (私は学生です — known topic) and "I, specifically, am the student" (私が学生です — new info). Beginners who default to が everywhere sound oddly emphatic. Mastering は means sounding NEUTRAL — the everyday, conversational baseline of Japanese.',
        'closing_practice_tip': 'Take any 5 sentences from your day and say each one in Japanese, deciding for each: "Is this a topic I\'m introducing or one already in the conversation?" If introducing, use が; if continuing, use は. Repeat the drill at week 1, week 2, and month 1 to lock in the instinct.',
    },
    'n5-003': {  # が subject marker
        'why_it_matters': 'が picks out NEW information, the answer to a "who?" or "what?" question. Confusing は and が is the single biggest source of unnatural Japanese for beginners. Native speakers use this distinction to signal which part of a sentence is the focus — get it wrong and your statement sounds like you\'re emphasizing something trivial.',
        'closing_practice_tip': 'Drill the question-answer pair: 誰がきましたか — 田中さんがきました (who came? Tanaka came). Repeat with 5 different verbs (きます / 食べます / 見ます / 来ます / 行きます). The answer-half always uses が; this drills the "new-info" instinct.',
    },
    'n5-004': {  # を direct object
        'why_it_matters': 'を marks the direct object — the thing being acted on. It also marks the path traversed (公園を歩く — walk through the park) and the point of departure (家を出る — leave home). The transitive/intransitive split (見る/見える, 開ける/開く) is a daily decision; using を with an intransitive verb is one of the most-corrected errors.',
        'closing_practice_tip': 'Build 5 transitive-verb sentences using を today, then convert each to its intransitive counterpart (no を, use が). Example: ドアを閉めます → ドアが閉まります. This drills the transitivity-pair vocabulary and forces you to feel which verb takes を.',
    },
    'n5-005': {  # に multi-purpose
        'why_it_matters': 'に has at least 6 distinct uses (location-of-existence, time-point, indirect object, direction, purpose, agent in passive). Beginners freeze when speaking. Internalising the "settles into / arrives at / pins to" intuition unlocks all six uses as variations of one core image.',
        'closing_practice_tip': 'Write one sentence for each of the 6 uses: (1) いる/ある location, (2) clock time, (3) indirect-object 〜にあげる, (4) destination 行く, (5) purpose 〜に行く, (6) absorbed-into 〜になる. Read each aloud 3× — the rhythm of に across uses settles the multi-purpose instinct.',
    },
    'n5-006': {  # へ direction
        'why_it_matters': 'へ overlaps with に for direction, which makes learners avoid it. The nuance: へ feels like "toward" or "in the direction of" while に is "to / arrives at". Native usage is roughly interchangeable for movement, but in formal letters and song lyrics, へ is preferred. Knowing the choice exists is the difference between sounding like a textbook and sounding fluent.',
        'closing_practice_tip': 'Write the address line of an imaginary letter: 田中さんへ ("To Mr. Tanaka"). Then build 3 movement sentences: 学校へ行きます / 駅へ向かいます / 日本へ来ました. Notice the soft, directional feel of each.',
    },
    'n5-007': {  # で location/instrument/means
        'why_it_matters': 'で is the "where the action happens" particle (公園で遊ぶ) AND the "instrument/means" particle (鉛筆で書く / 電車で来る). One particle covers two grammatically distinct concepts. Mistaking で for に in the location-of-existence sense (いる/ある needs に) is the single biggest beginner error.',
        'closing_practice_tip': 'Make a 3-column table: action verb / instrument / location. Fill 5 rows. Then write each row as a sentence with two で\'s: 学校で 鉛筆で 書きます (at school, with a pencil, write). The double-で feels redundant in English, but in Japanese it\'s how you compress action + tool + place into one breath.',
    },
    'n5-008': {  # と with/and
        'why_it_matters': 'と does double duty: "with X" (companion) and "X and Y and Z" (exhaustive listing). The exhaustive listing is the catch — や is for non-exhaustive ("X and Y, among others"). Get this wrong and you\'re telling Japanese listeners "these are literally the only items," when you meant "things like X and Y."',
        'closing_practice_tip': 'List the contents of your bag two ways: 教科書とノートとペン (textbook AND notebook AND pen — that\'s exactly what\'s in there) vs 教科書やノートやペン (textbook, notebook, pen — and probably other stuff). Choose based on whether your list is COMPLETE or not.',
    },
    'n5-009': {  # から from
        'why_it_matters': 'から marks the STARTING POINT — of time, place, or causation. The same particle does triple duty: 9時から (from 9 o\'clock), 東京から (from Tokyo), 寒いから (because it\'s cold). The causation use is what makes Japanese explanations feel cumulative — the reason precedes the result.',
        'closing_practice_tip': 'Build a one-day schedule sentence: 9時から12時まで仕事をします (I work from 9 to 12). Then add a reason: 疲れたから、休みます (I\'m tired, so I\'ll rest). Practice the time-from / cause-from pairing in 5 different sentences.',
    },
    'n5-010': {  # まで until/up to
        'why_it_matters': 'まで pairs with から to bracket a span: from-X-to-Y. Without まで, Japanese times sound open-ended. The contrast with まで{に} (a deadline marker, by-X) is also a frequent confusion: 5時まで means up-to-5 and 5時までに means by-5.',
        'closing_practice_tip': 'Write your daily schedule using から/まで pairs for 3 activities. Then rewrite ONE of them with までに to indicate a deadline (e.g., 宿題を10時までに出します). Notice how までに collapses the span into a deadline.',
    },
    'n5-011': {  # や non-exhaustive
        'why_it_matters': 'や signals "X, Y, and other things like that". This is the everyday, low-key way Japanese speakers list — claiming an exhaustive と-list usually feels too formal or oddly precise.',
        'closing_practice_tip': 'Describe what you ate today using や: 朝はパンやコーヒーや果物などを食べました (for breakfast I had bread, coffee, fruit, and so on). Add など at the end to reinforce the "and others" sense.',
    },
    'n5-013': {  # も also/too/even
        'why_it_matters': 'も replaces the marker (は/が/を) it inherits, NOT stack with it. 私もです, not 私はもです. Same with negation: 何もありません (nothing at all) vs 何かあります (something does). The double-no rule (も + negative = nothing/no one/nowhere) is a closed-system pattern worth memorising.',
        'closing_practice_tip': 'Make 5 negative sentences using question-word + も: 誰も来ません, 何もありません, どこも行きません, etc. Note how each "nothing" depends on a single も sitting between the question word and the negative verb.',
    },
    'n5-014': {  # これ／それ／あれ／どれ
        'why_it_matters': 'The kosoado pronoun system encodes spatial+conversational distance: これ near speaker, それ near listener, あれ far from both, どれ which-one. Pointing at something with これ when it\'s far away makes you sound like a child mis-mapping space.',
        'closing_practice_tip': 'Stand in your room. Point at 3 things at different distances and say これ / それ / あれ for each. Then ask これは何ですか about a near object you don\'t know the name of. The body memory of which finger goes with which word is what makes the system stick.',
    },
    'n5-016': {  # ここ／そこ／あそこ／どこ
        'why_it_matters': 'Place-version of the kosoado system. Same near/medium/far/which logic but applied to LOCATIONS. ここ ≠ here in English (it includes "where the speaker is"); 図書館はあそこです vs 図書館はそこです changes the listener\'s mental map.',
        'closing_practice_tip': 'In any conversation today (or imagined), use here/there/over-there in the right slot. Bonus: ask どこですか three times for genuinely unknown locations and notice how the answer always uses one of the other three.',
    },
    'n5-040': {  # この / その / あの / どの + Noun
        'why_it_matters': 'These are the ADJECTIVAL form of kosoado — they MUST attach to a noun. Beginners often write この alone meaning "this" — but この is a determiner, not a pronoun. これ stands alone; この needs a noun behind it.',
        'closing_practice_tip': 'Write 5 sentences where you replace English "this/that" with この/その/あの + noun. Then replace each with これ/それ/あれ alone — notice which sentences sound complete and which sound like fragments.',
    },
    'n5-045': {  # なん / なに
        'why_it_matters': 'Same kanji 何, two readings. なに in stand-alone questions (何ですか, what is it?), なん before counters and です-elements (何時, nanji; 何人, nannin; 何曜日, nan-youbi). The split feels arbitrary but it\'s phonetic — the next sound determines the reading.',
        'closing_practice_tip': 'Make a "what time / what day / what month / what number" wall. Practice naming each: 何時 / 何日 / 何月 / 何番. Then ask 何ですか about an unknown object. The shift between なん and なに will feel automatic after 10 repetitions.',
    },
    'n5-058': {  # Verb-ます polite present
        'why_it_matters': 'ます is the polite-language ON switch. Most textbooks teach ます-form first and never explain that it\'s a register choice — among friends, dictionary form is the default. Knowing when to drop ます (with peers/family) and when to keep it (with bosses/strangers/customers) is the difference between sounding stiff and sounding situationally aware.',
        'closing_practice_tip': 'Take a sentence you\'d say to a friend (drop ます: 食べる) and re-cast it for a teacher (keep ます: 食べます). Do this for 5 verbs. The mental flick between casual and polite is exactly the social muscle you\'re building.',
    },
    'n5-069': {  # Verb-て te-form
        'why_it_matters': 'The て-form is the universal connector. Every multi-clause sentence in Japanese (do this and then that, please do X, currently doing Y, may I do Z) leans on it. Memorising the て-form conjugation rules now saves DOZENS of hours later — every other request, progressive, and connector pattern is built on top.',
        'closing_practice_tip': 'Conjugate 5 verbs from each verb-class to て-form: 書く→書いて, 食べる→食べて, 来る→来て, etc. Then chain three actions: 起きて、朝ごはんを食べて、学校へ行きます. The chained-て becomes second nature after 50 reps.',
    },
    'n5-072': {  # Verb-ています progressive/state
        'why_it_matters': 'ています has TWO uses: ongoing action (今食べています — currently eating) and current state (結婚しています — am married, not "currently marrying"). The state-of-being interpretation is what trips learners — 知っています is "I know," not "I am knowing."',
        'closing_practice_tip': 'For 5 verbs, write both readings: 食べています (now eating, action) vs 結婚しています (married, state) vs 住んでいます (live in, state) vs 持っています (have, state) vs 知っています (know, state). The "state" verbs are a closed list worth memorising.',
    },
    'n5-085': {  # な-Adjective + です polite present
        'why_it_matters': 'な-adjectives behave like nouns: 静かです (it is quiet) follows the noun+です template. The な only appears when modifying a noun (静かな部屋 — a quiet room), not when ending a sentence. Mistakenly adding な to the predicate (×静かなです) is a daily error.',
        'closing_practice_tip': 'Pick 5 な-adjectives. For each, write (1) sentence-end form (静かです) and (2) noun-modifier form (静かな部屋). Mark both with the な position highlighted. The difference between predicate and modifier becomes muscle memory.',
    },
    'n5-090': {  # あります inanimate
        'visual_skip': True,
        'why_it_matters': 'あります is "there is" for INANIMATE things — books, pens, problems, time, money. Pairs with います for animate things (people, animals). Mistakenly using います for objects (×机にいます) marks you instantly as a beginner.',
        'closing_practice_tip': 'Walk around your room and identify 5 inanimate things: 机の上に本があります. Then 5 animate: 部屋に犬がいます. The animate/inanimate split is a one-time learning that pays daily dividends.',
    },
    'n5-091': {  # います animate
        'why_it_matters': 'います is "there is" for ANIMATE — people, animals, anything that breathes. Plants are NOT animate (they take あります), which surprises learners. The split exists because Japanese grammatically distinguishes "movable life" from "static existence."',
        'closing_practice_tip': 'Make a list: 5 animate things you\'d encounter today (人、先生、犬、猫、子ども) and 5 inanimate (本、机、車、電話、お金). Build a sentence for each: ___ がいます / ___があります. Cross-classify until the split is automatic.',
    },
    'n5-104': {  # たいです want to
        'why_it_matters': 'たい conjugates like an い-adjective, NOT a verb. 食べたい (want to eat), 食べたかった (wanted to), 食べたくない (don\'t want to). Beginners try to verb-conjugate it (×食べたます) — wrong category. Also, たい only works for the SPEAKER\'s desire; for "X wants to," use がっている.',
        'closing_practice_tip': 'For 3 verbs, conjugate the full たい-cycle: present (食べたいです), negative (食べたくないです), past (食べたかったです), past-negative (食べたくなかったです). It\'s the same pattern as the い-adjective family from n5-080.',
    },
    'n5-109': {  # いくつ / いくら / なんにん / なんまい etc.
        'why_it_matters': 'Counter questions are a closed system: いくつ for general count (1-10 native), いくら for price, 何人 for people, 何枚 for flat objects. Mismatching the counter (×何個の人) marks you as not knowing the noun\'s shape category. Native speakers categorise by shape automatically.',
        'closing_practice_tip': 'Walk through your room and count 5 different categories: 本(冊), 鉛筆(本), 紙(枚), りんご(個), 人(人). Speak each count aloud: 本が3冊あります. The counter+noun pairing is what cements the shape system.',
    },
    'n5-115': {  # に at clock time
        'why_it_matters': 'に marks SPECIFIC times that have a number — 7時に、月曜日に、3月に. Vague time references (今日、明日、毎日) take NO particle. Adding に to vague times (×今日に) is the most-common time-particle error for English speakers (because English uses "on" for both).',
        'closing_practice_tip': 'Write today\'s schedule. Use に on every numbered time (7時に起きました) and NOTHING on every vague time (今日勉強します, no particle). The asymmetry is the lesson.',
    },
    'n5-130': {  # ～に～をあげます give to
        'why_it_matters': 'The Japanese give-receive system tracks WHO gives to WHOM relative to YOU. あげる = I/inner-circle gives outward, くれる = outer gives to me/inner-circle, もらう = I receive. Misuse and you\'ll either accidentally claim a gift you didn\'t get, or fail to thank the giver. Daily, high-stakes vocabulary.',
        'closing_practice_tip': 'Build a triangle: you (私), close friend (友だち), distant person (先生). Build sentences for: 私 → 友だち, 先生 → 私, 友だち → 先生. Use the right verb for each: あげる/くれる/もらう/さしあげる. Repeat until the direction is automatic.',
    },
    'n5-133': {  # から sentence-causation
        'why_it_matters': 'Sentence-final から explains WHY. The Japanese reason-result order is the OPPOSITE of casual English ("It\'s late, so I\'m leaving" → 遅いから、帰ります — reason FIRST, result second). Reordering this in your head is the daily cognitive task.',
        'closing_practice_tip': 'Take 5 English "X because Y" sentences. Reverse them to "Y so X" form. Then translate. The grammar lesson is muscle, but the mental reordering is the deeper skill.',
    },
    'n5-167': {  # ～んです / ～のです explanatory
        'why_it_matters': 'んです adds an EXPLANATORY tone — "(here\'s the reason)" or "(it\'s because)". You hear it constantly in conversation. Without it, your statements sound abrupt or context-less. Misusing it (everywhere) makes you sound defensive.',
        'closing_practice_tip': 'Find 3 statements you\'ve made today and recast each as んです. ATM is closed → ATMが閉まっているんです. Then ask 3 questions in んです: どこへ行くんですか. Notice the warmer, more curious tone.',
    },
    'n5-184': {  # なにか / なにも something / nothing
        'why_it_matters': 'なにか + positive = something; なにも + negative = nothing. The split is rigid: なに ALONE is a question word; なにか/なにも are existential quantifiers. Forgetting to attach に+verb after なに in negative ("nothing was eaten" — 何も食べませんでした) is a common slip.',
        'closing_practice_tip': 'Build a yes/no minipair: 何か食べましたか — はい、食べました / いいえ、何も食べませんでした. Drill the か-or-も swap until it follows the answer\'s polarity automatically.',
    },
    'n5-186': {  # どこか / どこも somewhere / nowhere
        'why_it_matters': 'Place version of なにか/なにも. どこか + positive = somewhere; どこも + negative = nowhere. どこも + POSITIVE means "everywhere" (どこも混んでいます — everywhere is crowded) — same どこも, opposite meaning depending on the verb polarity. This is a subtle inversion worth memorising explicitly.',
        'closing_practice_tip': 'Build all four: どこか行きました (went somewhere), どこへも行きませんでした (went nowhere), どこも混んでいます (everywhere is crowded), どこも空いていません (nowhere is empty). Track how どこも flips meaning with the verb sign.',
    },
    'n5-187': {  # いつか / いつも sometime / always
        'why_it_matters': 'Time version of question-word + か/も. いつか = sometime/someday; いつも = always (regardless of polarity — unlike どこも which depends on the verb). The asymmetry across the なにか/どこか/いつか triplets is a closed-system gotcha.',
        'closing_practice_tip': 'Write 3 future hopes using いつか (いつか日本に行きたいです). Then 3 daily routines using いつも (いつも7時に起きます). Drill until each adverb has a default mental tense attached.',
    },
}


# ---- Apply ----
grammar_path = ROOT / 'data' / 'grammar.json'
data = json.loads(grammar_path.read_text(encoding='utf-8'))
patterns = data['patterns']

updated = 0
not_found = []
already_authored = 0

for p in patterns:
    pid = p['id']
    if pid not in ESSAYS:
        continue
    essay = p.get('essay')
    if not essay or not isinstance(essay, dict):
        not_found.append(pid)
        continue
    payload = ESSAYS[pid]
    if essay.get('provenance') == 'llm_curated':
        already_authored += 1
        continue
    essay['why_it_matters'] = payload['why_it_matters']
    essay['closing_practice_tip'] = payload['closing_practice_tip']
    essay['provenance'] = 'llm_curated'
    updated += 1

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print(f'Patterns in ESSAYS dict: {len(ESSAYS)}')
print(f'  authored sub-fields:           {updated}')
print(f'  no essay scaffold (skipped):   {len(not_found)}')
print(f'  already llm_curated:           {already_authored}')
if not_found:
    print(f'  missing scaffold: {not_found}')
