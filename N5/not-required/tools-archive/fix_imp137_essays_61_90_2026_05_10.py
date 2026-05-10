"""IMP-137 round-3: essays for patterns 61-90 (next 30 trickiest).

Same 5-field structure: intro, why_it_matters, common_pitfalls,
contrasts, closing_practice_tip. All N5-kanji-compliant.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ESSAYS = {
    'n5-162': {  # Verb-plain まえに
        'intro': "Verb-plain + まえに = 'before doing X.' Use the dictionary form (NOT past): 食べる まえに 手を あらう (wash hands before eating).",
        'why_it_matters': "The dictionary-form-before-まえに rule is counter-intuitive — even when the action is in the past (yesterday before eating I washed my hands), Japanese still uses dictionary form. The まえに locks the temporal sequence, the verb stays neutral.",
        'common_pitfalls': "Using た-form (×食べた まえに → 食べる まえに). Forgetting the に (まえ alone is ambiguous). Mixing with ながら (ながら = simultaneous; まえに = sequential).",
        'contrasts': "vs Verb-た あとで (n5-163): あとで = AFTER, takes た-form. まえに = BEFORE, takes dictionary form. Mirror of each other.",
        'closing_practice_tip': "Pick 5 daily routines. Build まえに sentences for each: ねる まえに はを みがく (brush teeth before sleep). Then build the あとで mirror: ねた あとで ゆめを みた (after sleeping I dreamed). Notice the verb-form flip.",
    },
    'n5-156': {  # ね/よ casual
        'intro': "Sentence-final particles in casual register. ね = seek agreement / share feeling ('isn't it?'). よ = inform / assert ('you know!'). Used after plain forms among friends.",
        'why_it_matters': "These particles inject conversational warmth. Without them, casual speech sounds robotic. Native conversation drops them constantly — recognising ね vs よ is core listening skill.",
        'common_pitfalls': "Using ね when listener has no shared context. Using よ when listener already knows (sounds preachy). Mixing register: 食べるよ (casual) is fine; 食べますよ (polite) is too.",
        'contrasts': "vs ですね/ですよ (n5-159): polite versions. Same pragmatics, different register.",
        'closing_practice_tip': "Take a casual conversation and add ね or よ to 5 lines based on whether you're seeking agreement or asserting. The conversational rhythm is the lesson.",
    },
    'n5-137': {  # Noun + の + Noun
        'intro': "The simplest noun-noun connection: NOUN1 の NOUN2. Covers possession (私の 本), category (日本の 食べもの), and source (会社の 友だち).",
        'why_it_matters': "の is the most-used particle in noun phrases. Without it, you can't link two nouns. Mastering の sets the foundation for relative clauses and noun-modifying constructions.",
        'common_pitfalls': "Forgetting の (×私 本 → 私の 本). Stacking too many の (×私の 母の 父の 本 reads awkwardly — restructure). Confusing の-possessive with の-question (n5-031).",
        'contrasts': "vs Adjective + Noun (n5-136): adjectives modify nouns directly (大きい 本); the の-bridge is for noun-noun.",
        'closing_practice_tip': "Identify 5 N1-of-N2 relationships in your room: 友だちの くるま, 私の つくえ. Build a sentence for each. The の-glue is the muscle.",
    },
    'n5-155': {  # 〜が、〜 mid-sentence
        'intro': "が between two clauses = 'but/however' (mid-sentence). Different from subject-marker が. Position is the cue: between clauses, not before a verb.",
        'why_it_matters': "Mid-sentence が gives you a way to pivot in formal/written register: 寒いですが、行きます (it's cold, but I'll go). In casual speech, けど is more common. Both are needed.",
        'common_pitfalls': "Confusing the two が functions. Using が when the connection isn't really contrast (use そして or それから for plain 'and').",
        'contrasts': "vs けれど/けど (n5-127): casual variants of the same connector. が is more formal/written.",
        'closing_practice_tip': "Build 5 'X but Y' sentences. Try each in formal (が) and casual (けど) form. The register shift is the lesson.",
    },
    'n5-080': {  # い-Adj negative ~くないです
        'intro': "Negative present polite for い-adjectives: replace い with くない + です. 高い → 高くないです (is not expensive). Variant: 高くありません (slightly more formal).",
        'why_it_matters': "Negation is daily vocabulary. The くない transformation follows the i-adj rule (just like かった for past). Get the い-stem instinct here and the rest of い-adjective grammar follows.",
        'common_pitfalls': "Adding な (×高くないなです). Forgetting irregular いい → よくないです. Using じゃない (na-adj negative) on i-adj.",
        'contrasts': "vs ~じゃない (n5-086): na-adjectives negate with じゃない. i-adjectives use くない.",
        'closing_practice_tip': "Conjugate 5 i-adjectives through the cycle: present (高いです), negative (高くないです), past (高かったです), past-negative (高くなかったです). The い-くない / い-かった / い-くなかった template is the muscle.",
    },
    'n5-185': {  # だれか / だれも
        'intro': "Personal pronoun + か/も: だれか + positive = someone; だれも + negative = no one. The か introduces existence; the も + negative produces 'nobody'.",
        'why_it_matters': "Daily question/answer vocabulary. The か/も swap matches the verb polarity perfectly. Mastering this trio (なにか/だれか/どこか + the も versions) makes existential statements automatic.",
        'common_pitfalls': "Mismatching polarity (だれか + negative or だれも + positive). Forgetting the verb negation that pairs with も.",
        'contrasts': "vs なにか/なにも (n5-184), どこか/どこも (n5-186): same template, different question word.",
        'closing_practice_tip': "Build a yes/no minipair: だれか 来ましたか — はい、ともだちが 来ました / いいえ、だれも 来ませんでした. The か-or-も swap follows the answer's polarity.",
    },
    'n5-118': {  # いま / すぐ / もう / まだ
        'intro': "Four temporal adverbs that describe action-timing relative to NOW: いま (right now), すぐ (immediately), もう (already), まだ (still / not yet).",
        'why_it_matters': "Each marks a different temporal stance: いま is precise present; すぐ is imminent; もう is completed; まだ is ongoing or pending. Mastering them lets you describe state with precision.",
        'common_pitfalls': "Confusing もう with すぐ (もう = already happened; すぐ = will happen soon). Using まだ + positive vs まだ + negative — both valid but mean different things (まだ + positive = still doing; まだ + negative = not yet).",
        'contrasts': "もう and まだ are direct opposites in negation: もう 来ました (already came) vs まだ 来ません (hasn't come yet).",
        'closing_practice_tip': "Build a daily-routine sentence using each: いま べんきょうします, すぐ 行きます, もう 食べました, まだ ねていません. The temporal landscape locks in.",
    },
    'n5-136': {  # Adjective + Noun
        'intro': "Adjectives directly modify nouns. い-adj attach plain: 大きい 本 (big book). な-adj need な: 静かな 部屋 (quiet room). The split mirrors the entire adjective system.",
        'why_it_matters': "Modifying nouns is daily vocabulary. The い vs な split is the foundation — get this and the rest of adjective grammar (past, negative, te-form) follows mechanically.",
        'common_pitfalls': "Adding な to い-adj (×大きいな 本). Omitting な on na-adj (×静か 部屋).",
        'contrasts': "vs Noun-no-Noun (n5-137): adjective modifies directly; noun-noun needs の.",
        'closing_practice_tip': "Build 5 each: い-adj-noun (大きい 木), な-adj-noun (きれいな 花), noun-noun (友だちの 本). Notice which connector each takes.",
    },
    'n5-176': {  # ~なくちゃ / ~なきゃ casual must
        'intro': "Casual contractions of 'must do.' なくちゃ from なくては; なきゃ from なければ. Used among friends/family. Often dropped at sentence-end as an implied 'have to.'",
        'why_it_matters': "Native casual speech contracts heavily. Recognising 行かなくちゃ as 'I gotta go' is essential listening skill. The full forms (~なくてはいけません) feel formal in conversation.",
        'common_pitfalls': "Using these in formal writing (sounds too casual). Mixing the contraction (×行かなくちゃならない sometimes used; not standard).",
        'contrasts': "vs ~なくてはいけません (n5-174): formal/written equivalent. vs ~ないといけない (n5-175): another spoken variant.",
        'closing_practice_tip': "Take 3 'must-do' obligations. Say each in casual (なくちゃ): ねなくちゃ (gotta sleep). Then formal (なくてはいけません). Notice the register flip.",
    },
    'n5-174': {  # ~なくてはならない formal must
        'intro': "Formal/written 'must do.' Verb negative-て + は + ならない (or いけない). 行かなくては ならない = must go. Slightly stiffer than いけない version.",
        'why_it_matters': "Knowing the formal version makes you readable in business writing and signs. The double-negative structure is unique to Japanese: 'doing-not is not-permitted' = 'must do.'",
        'common_pitfalls': "Using in casual speech (use なくちゃ instead). Confusing ならない (formal/general moral) with いけない (more general).",
        'contrasts': "vs ~ないといけない (n5-175): variant. vs ~なくちゃ (n5-176): casual contraction.",
        'closing_practice_tip': "Build 3 formal 'must' sentences. Then re-cast each in なくちゃ for casual speech. The same obligation, two registers.",
    },
    'n5-175': {  # ~ないといけない must variant
        'intro': "Common spoken variant of 'must do.' Verb-ない + と + いけない. 行かないと いけない (must go). The と is conditional ('if you don't').",
        'why_it_matters': "This is the most-used 'must' form in everyday speech. The conditional logic ('if not done, can't go on') makes it intuitive once you internalise it.",
        'common_pitfalls': "Conjugating the wrong verb (the negative goes on the action verb, not いけない). Trying to use と for 'and' here (it's conditional と).",
        'contrasts': "vs ~なくてはならない (n5-174): formal. vs ~なくちゃ (n5-176): casual contraction. All three same meaning, different register.",
        'closing_practice_tip': "Build 5 obligations using ~ないといけない. The pattern: VERB-ない + と + いけない. Repeat until the structure is automatic.",
    },
    'n5-160': {  # Noun + の + あとで
        'intro': "'After NOUN' — NOUN + の + あとで. The の glues the noun to the time-marker あとで. しごと の あとで = after work.",
        'why_it_matters': "Time-relative expressions chain naturally with の. Same template as まえに but flipped temporally.",
        'common_pitfalls': "Forgetting の. Using で alone instead of あとで. Confusing with Verb-た + あとで (verb-form, not noun-form).",
        'contrasts': "vs Verb-た + あとで (n5-163): for actions, use た-form; for nouns, use の.",
        'closing_practice_tip': "Build pairs: noun-version (しごと の あとで), verb-version (しごとを した あとで). Notice when の vs た is the connector.",
    },
    'n5-158': {  # ~だろう
        'intro': "Casual/plain version of でしょう. Expresses probability or seeks confirmation. 雨 が ふる だろう (it'll probably rain).",
        'why_it_matters': "Recognising だろう in casual speech is core listening skill. The probability marker is one of the few JP grammatical structures with no direct English equivalent.",
        'common_pitfalls': "Using だろう in formal contexts (use でしょう). Confusing with だ (statement) — だろう adds uncertainty.",
        'contrasts': "vs でしょう (n5-157): formal version. Same probability meaning.",
        'closing_practice_tip': "Take 3 future predictions. Say each casually with だろう, then formally with でしょう: あした 雨が ふる だろう / ふる でしょう. The shift is one syllable.",
    },
    'n5-114': {  # ~から~まで paired range
        'intro': "Paired range marker. NOUN1 から NOUN2 まで = from N1 to N2. Works for time (9時から 5時まで), place (東京から 大阪まで), or any range.",
        'why_it_matters': "Most common way to express bounds in Japanese. Pairs are mandatory — leaving off まで feels open-ended.",
        'common_pitfalls': "Using just から without まで (sounds incomplete). Confusing with sentence-final から (causation).",
        'contrasts': "vs sentence-final から (n5-009): same particle, different function. The paired まで is the cue.",
        'closing_practice_tip': "Build 3 ranges: time (9時 から 5時 まで), place (東京 から 大阪 まで), price (100円 から 500円 まで). The pair is the muscle.",
    },
    'n5-082': {  # い-Adjective past negative
        'intro': "Past-negative for い-adjectives: replace い with くなかった + です. 高い → 高くなかったです (was not expensive).",
        'why_it_matters': "Completes the i-adjective conjugation cycle. The くなかった step is the past-negative join: くない (negative) + かった (past).",
        'common_pitfalls': "Stacking でした (×高くなかったでした). Forgetting irregular いい → よくなかったです.",
        'contrasts': "vs ~じゃありませんでした (na-adj past-neg): different morphology, same time meaning.",
        'closing_practice_tip': "Conjugate 5 i-adjectives through the full quartet: 高いです / 高くないです / 高かったです / 高くなかったです. Speak each aloud — the rhythm locks in.",
    },
    'n5-103': {  # ~ができます
        'intro': "Productive 'can-do' with NOUN. NOUN が できます = can do NOUN / be able. すいえいが できます (can swim). Pairs with verbs that nominalise.",
        'why_it_matters': "Common ability-statement form. Pairs with the verb-based ことができる (n5-188); the noun version is more compact when you have a -する verb already in noun form.",
        'common_pitfalls': "Using を instead of が. Mixing with the verb potential form (when noun is available, prefer this).",
        'contrasts': "vs ~ことができます (n5-188): verb-version. Same ability meaning, different grammatical anchor.",
        'closing_practice_tip': "Build 5 ability statements with nouns: すいえい / りょうり / 日本語 / ピアノ / うんてん が できます. The が-marker sticks.",
    },
    'n5-163': {  # Verb-た + あとで
        'intro': "'After doing X.' Verb-past (た-form) + あとで. ごはんを 食べた あとで、おちゃを 飲みました (after eating I drank tea). Verb form is past even if the whole sentence is present/future.",
        'why_it_matters': "Sequential actions use た-form before あとで, regardless of overall sentence tense. This decouples the verb-form from the sentence-tense — a key step beyond simple past.",
        'common_pitfalls': "Using dictionary form (×食べる あとで → 食べた あとで). Forgetting で (just あと is ambiguous).",
        'contrasts': "vs Verb-plain まえに (n5-162): まえ takes dictionary form, あと takes past form. Mirror.",
        'closing_practice_tip': "Build 3 sequence pairs: Aを した あと、Bを した. Repeat with まえ to see the form-flip.",
    },
    'n5-098': {  # Likes / dislikes contrast
        'intro': "Expressing like/dislike: NOUN が すき/きらい です. すき = like; きらい = dislike. The が marker is critical (NOT を).",
        'why_it_matters': "Daily-life vocabulary. The が-marker is unique to suki/kirai because the liked-thing is grammatically the SUBJECT of liking, not its object.",
        'common_pitfalls': "Using を (×コーヒーを すき → コーヒーが すき). Using すき as a verb (it's a na-adj — needs です to be polite).",
        'contrasts': "vs ~がほしい (n5-101): same が-marker rule for state-of-mind verbs.",
        'closing_practice_tip': "Build 5 like/dislike sentences with concrete nouns: コーヒーが すき, やさいが きらい. The が-marker is the muscle.",
    },
    'n5-066': {  # Verb-ない plain negative
        'intro': "Plain non-past negative — the ない form: 食べる → 食べない, 行く → 行かない. Used in casual speech and as the base for many other forms (なくて, ないで, なければ, etc.).",
        'why_it_matters': "Casual default among friends. Also the foundation for ~なくちゃ, ~ないといけない, ~ないで, conditional ~なければ, etc. Master the conjugation here and a dozen N4 patterns follow.",
        'common_pitfalls': "Mixing with ~ません (jarring register switch). Forgetting irregular する → しない, 来る → こない. Confusing ない with the い-adjective ない (which inflects differently).",
        'contrasts': "vs ~ません (polite negative): same meaning, different register.",
        'closing_practice_tip': "Conjugate 5 verbs from each verb class to plain negative: 食べない / 行かない / 来ない / しない. Then speak in casual sentences. The form unlocks the casual register.",
    },
    'n5-092': {  # ~に~があります location-first
        'intro': "Location-first existence: LOCATION に NOUN が あります/います. へやに テーブルが あります (in the room there is a table). The が-marker introduces NEW information.",
        'why_it_matters': "This is the existence-construction's NEW-info variant. Pair with n5-093 (the は-form) which marks the topic as already known. Choosing が vs は signals the conversational state.",
        'common_pitfalls': "Using で instead of に (で is action-location). Using は instead of が when the noun is new. Forgetting animacy (います for animate, あります for inanimate).",
        'contrasts': "vs ~は~にあります (n5-093): topic-first vs location-first. Same situation, different conversational frame.",
        'closing_practice_tip': "Walk around your room and announce 5 things using location-first: テーブルの 上に 本が あります. The location-に + thing-が pattern is the muscle.",
    },
    'n5-075': {  # Verb-てはいけません
        'intro': "'Must not / forbidden': Verb-て + は + いけません. 食べてはいけません = you must not eat. Common on signs.",
        'why_it_matters': "Daily public-space vocabulary. Negation of permission (~てもいいです). Pairs with the casual contraction ~ちゃダメ.",
        'common_pitfalls': "Confusing with ~なくてはいけません (must do — note the double negative). The は particle is essential.",
        'contrasts': "vs ~てもいいです (permission): opposite meaning. Same Verb-て base.",
        'closing_practice_tip': "Build 5 prohibition signs in your context: ここで しゃしんを とっては いけません. The Verb-て + は + いけません template sticks.",
    },
    'n5-034': {  # しか~ない
        'intro': "'Only X' with negative verb. NOUN しか VERB-NEG. 千円 しか ありません = I only have 1000 yen. The negation is mandatory; the meaning is positive ('only' / 'just').",
        'why_it_matters': "Distinct from だけ — しか implies the speaker thinks it's INSUFFICIENT ('only this much, regrettably'). Use しか when expressing scarcity; use だけ for neutral 'only.'",
        'common_pitfalls': "Using positive verb (×しか あります → しか ありません). Confusing with だけ (no negative needed).",
        'contrasts': "vs だけ (n5-033): だけ = neutral 'only/just.' しか = 'only [and that's not enough]'. Different emotional weight.",
        'closing_practice_tip': "Take 3 'only' sentences. Say each with だけ (neutral) and しか + neg (regretful). Notice how the emotional weight shifts.",
    },
    'n5-071': {  # Verb-てください
        'intro': "Polite request / instruction: Verb-て + ください. 食べて ください = please eat. Used for asking favors, giving instructions, polite imperatives.",
        'why_it_matters': "The single most-used polite request form. Mastering it unlocks polite interaction with everyone — staff, teachers, strangers.",
        'common_pitfalls': "Using ください after a noun WITHOUT the verb (use ~を ください for noun requests). Forgetting the て (just くれる is rude).",
        'contrasts': "vs noun + を ください: for things (お水を ください). Verb form for actions (食べて ください).",
        'closing_practice_tip': "Build 5 polite requests for actions: 待って ください, 教えて ください, 来て ください. Then 5 polite requests for things: お水を ください, きっぷを ください. Action vs thing — different forms.",
    },
    'n5-119': {  # ~まえ
        'intro': "Time-marker 'before.' Used after nouns (の + まえ) or verbs (dictionary + まえに). 三日 まえ = three days ago; ねる まえに = before sleeping.",
        'why_it_matters': "Time-axis vocabulary. Pairs with あと (after). Use まえ for both 'time-ago' (without に) and 'before-doing' (with に).",
        'common_pitfalls': "Forgetting に when used with verbs. Using past form before まえに (×食べた まえに).",
        'contrasts': "vs あと (n5-120): opposite time direction. Same templates, mirror meaning.",
        'closing_practice_tip': "Build 3 time-ago sentences: 三日 まえ・三年 まえ・しゅうかん まえ. Then 3 before-doing: ねる まえに・しごと の まえに. Notice the に goes with verb-form, not bare-time.",
    },
    'n5-025': {  # ね sentence-final
        'intro': "Sentence-final particle for seeking agreement. 寒いね (it's cold, isn't it?) presumes the listener shares your perception.",
        'why_it_matters': "Conversational warmth. Without ね (and よ), Japanese sounds flat and informational. ね specifically signals 'you and I share this view' — the social glue of casual conversation.",
        'common_pitfalls': "Using ね when listener has no shared context (sounds presumptuous). Mixing with formal speech (use ですね).",
        'contrasts': "vs よ (asserting): よ tells; ね asks for agreement.",
        'closing_practice_tip': "In a casual exchange, add ね to 3 statements where you're seeking agreement (天気が いいね). Notice how it softens the sentence.",
    },
    'n5-033': {  # だけ
        'intro': "Limiting particle: 'only / just.' NOUN だけ. 一つ だけ = just one. Doesn't require negative verb (unlike しか).",
        'why_it_matters': "The neutral 'only' marker. Use when you want to express limitation without the regret-tinge of しか. Daily-conversation common.",
        'common_pitfalls': "Confusing with しか (which needs negative). Forgetting だけ is a particle (attaches directly to noun).",
        'contrasts': "vs しか~ない (n5-034): だけ is neutral; しか + neg implies insufficiency.",
        'closing_practice_tip': "Build 5 'only X' sentences with だけ: 一日 だけ, 私 だけ, すこし だけ. The neutral-only sense lands consistently.",
    },
    'n5-180': {  # ~かた
        'intro': "Productive nominaliser: 'way of doing X.' Verb-stem + かた. 読みかた = how to read. Use the ます-stem (not dictionary form).",
        'why_it_matters': "Daily-life productive: つくりかた (how to make), 行きかた (how to get to). Asking 'how do I X?' constantly uses this form.",
        'common_pitfalls': "Using dictionary form instead of ます-stem (×読むかた → 読みかた). Confusing with ~かた as a noun-suffix for people (お国の かた = a person from your country).",
        'contrasts': "vs ~こと (nominaliser): more abstract. かた is specifically about the METHOD of doing.",
        'closing_practice_tip': "Build 5 'how-to' nouns: 行きかた・読みかた・書きかた・つくりかた・話しかた. Each is a real object you can ask about.",
    },
    'n5-086': {  # な-Adjective negative
        'intro': "Negative present polite for な-adjectives: ADJ + じゃありません or じゃないです. 静かじゃありません (is not quiet). The な disappears in negation.",
        'why_it_matters': "Mirrors noun negation (since na-adj behave like nouns). The じゃ is a contraction of では. Variants: ではありません (more formal), じゃないです (more conversational).",
        'common_pitfalls': "Adding な (×静かなじゃありません). Using くない (i-adj rule wrong category).",
        'contrasts': "vs ~くない (n5-080): i-adj negative. Different morphology, same negative meaning.",
        'closing_practice_tip': "Conjugate 5 na-adjectives through the negative cycle: 静かじゃありません / 静かじゃ ありませんでした / 静かじゃない / 静かじゃなかった. The じゃ-pattern locks in.",
    },
    'n5-024': {  # か (or)
        'intro': "Mid-sentence or: NOUN か NOUN. コーヒー か おちゃ = coffee or tea. Different from sentence-final か (question marker) — position is the cue.",
        'why_it_matters': "Daily choice-making vocabulary. Knowing the か-as-or vs か-as-question split is core grammar literacy.",
        'common_pitfalls': "Using と instead of か (と is exhaustive listing, not alternatives). Confusing with question-か.",
        'contrasts': "vs か question marker (n5-023): mid-sentence vs sentence-final. Position differentiates.",
        'closing_practice_tip': "Build 3 choice-questions with か: バスか でんしゃで 来ますか. The か between alternatives is the muscle.",
    },
    'n5-064': {  # Verb-ませんか polite invitation
        'intro': "'Won't you...?' polite invitation. Verb-ます-stem + ませんか. 食べませんか = won't you eat? More polite than the imperative.",
        'why_it_matters': "Standard invitation form. Less direct than 食べましょう (let's eat) — gives the listener the choice. Polite-conversation default.",
        'common_pitfalls': "Confusing with the negative ~ません (just statement, not invitation). The か at the end is the cue for invitation.",
        'contrasts': "vs ~ましょう (let's): invitation that assumes agreement. ~ませんか offers the choice.",
        'closing_practice_tip': "Invite a friend to 5 things using ~ませんか: いっしょに 食べませんか, えいがを 見ませんか. Then say 5 with ~ましょう (let's). The politeness-asymmetry is the lesson.",
    },
}


# ---- Apply ----
grammar_path = ROOT / 'data' / 'grammar.json'
data = json.loads(grammar_path.read_text(encoding='utf-8'))
patterns = data['patterns']

added = 0
for p in patterns:
    pid = p['id']
    if pid not in ESSAYS:
        continue
    if p.get('essay'):
        continue
    payload = ESSAYS[pid]
    p['essay'] = {
        'intro': payload['intro'],
        'why_it_matters': payload['why_it_matters'],
        'common_pitfalls': payload['common_pitfalls'],
        'contrasts': payload['contrasts'],
        'closing_practice_tip': payload['closing_practice_tip'],
        'provenance': 'llm_curated',
    }
    added += 1


# Apply kanji-compliance cleanup before save
COMPOUNDS = [
    ('家族', 'かぞく'), ('部屋', 'へや'), ('音楽', 'おんがく'),
    ('運転', 'うんてん'), ('元気', 'げんき'), ('天気', 'てんき'),
    ('一緒', 'いっしょ'), ('普通', 'ふつう'), ('時々', 'ときどき'),
    ('家庭', 'かてい'), ('教科書', 'きょうかしょ'), ('鉛筆', 'えんぴつ'),
    ('図書館', 'としょかん'), ('結婚', 'けっこん'), ('宿題', 'しゅくだい'),
    ('勉強', 'べんきょう'), ('遊ぶ', 'あそぶ'), ('遊び', 'あそび'),
    ('歩く', 'あるく'), ('運動', 'うんどう'), ('働く', 'はたらく'),
    ('泳ぐ', 'およぐ'), ('泳ぎ', 'およぎ'), ('運転する', 'うんてんする'),
    ('全部', 'ぜんぶ'), ('世界', 'せかい'),
    ('部', 'へ'), ('屋', 'や'), ('音', 'おと'), ('楽', 'がく'),
    ('運', 'うん'), ('転', 'てん'), ('普', 'ふ'), ('通', 'つう'),
    ('時々', 'ときどき'), ('教', 'きょう'), ('科', 'か'),
    ('鉛', 'えん'), ('筆', 'ぴつ'), ('図', 'ず'), ('書館', 'しょかん'),
    ('結', 'けっ'), ('婚', 'こん'), ('宿', 'しゅく'), ('題', 'だい'),
    ('勉', 'べん'), ('遊', 'あそ'), ('歩', 'ある'), ('泳', 'およ'),
    ('働', 'はたら'), ('全', 'ぜん'), ('世界', 'せかい'),
    ('世', 'せ'), ('界', 'かい'), ('一緒', 'いっしょ'), ('緒', 'しょ'),
    ('一日', 'いちにち'), ('家', 'いえ'), ('族', 'ぞく'),
    ('元', 'もと'), ('運', 'うん'),
]

# Read whitelist
kdata = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
ke = kdata.get('entries', kdata) if isinstance(kdata, dict) else kdata
if isinstance(ke, dict): ke = list(ke.values())
whitelist = set()
for k in ke:
    g = k.get('glyph') or (k.get('id', '').split('.')[-1])
    if g: whitelist.add(g)

# Single-char fallback for any leftover
SINGLE_FALLBACK = {
    '物': 'もの', '寒': 'さむ', '静': 'しず', '机': 'つくえ',
    '方': 'ほう', '京': 'きょう', '阪': 'さか', '元': 'げん',
    '朝': 'あさ', '昼': 'ひる', '夜': 'よる',
    '部': 'へ', '屋': 'や', '音': 'おと', '楽': 'がく',
    '運': 'うん', '転': 'てん', '普': 'ふ', '通': 'つう',
    '教': 'きょう', '科': 'か', '鉛': 'えん', '筆': 'ぴつ',
    '図': 'ず', '館': 'かん', '結': 'けっ', '婚': 'こん',
    '宿': 'しゅく', '題': 'だい', '勉': 'べん', '強': 'きょう',
    '遊': 'あそ', '歩': 'ある', '泳': 'およ', '働': 'はたら',
    '全': 'ぜん', '世': 'せ', '界': 'かい', '緒': 'しょ',
    '族': 'ぞく', '誰': 'だれ', '体': 'からだ', '心': 'こころ',
    '声': 'こえ', '帰': 'かえ', '考': 'かんが', '使': 'つか',
    '持': 'も', '待': 'ま', '作': 'つく', '知': 'し',
    '思': 'おも', '住': 'す', '教師': 'きょうし', '師': 'し',
    '質': 'しつ', '問': 'もん', '聞': 'き', '理': 'り', '由': 'ゆう',
}

for p in patterns:
    e = p.get('essay')
    if not isinstance(e, dict): continue
    for fld in ['intro','why_it_matters','common_pitfalls','contrasts','closing_practice_tip']:
        v = e.get(fld) or ''
        if not isinstance(v, str): continue
        for cmp, kn in sorted(COMPOUNDS, key=lambda x: -len(x[0])):
            v = v.replace(cmp, kn)
        out = []
        for c in v:
            if c in SINGLE_FALLBACK:
                out.append(SINGLE_FALLBACK[c])
            else:
                out.append(c)
        e[fld] = ''.join(out)


grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

with_essay = sum(1 for p in patterns if p.get('essay'))
print(f'Added: {added}')
print(f'Total essays: {with_essay}/178')
