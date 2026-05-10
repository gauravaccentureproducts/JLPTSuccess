"""IMP-137 round-2: extend Tofugu-style essays from top-30 to top-60
trickiest grammar patterns. Each essay has 5 hand-authored sub-fields:
intro, why_it_matters, common_pitfalls, contrasts, closing_practice_tip.

Provenance: 'llm_curated'."""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Patterns 31-60 by trickiness
ESSAYS = {
    'n5-093': {  # ~は~にあります/います
        'intro': "Used to state the existence of a known entity at a specific location: TOPIC は LOCATION に あります/います. The topic (は) is something already in the conversation; the comment is where it lives.",
        'why_it_matters': "This is the everyday \"X is at Y\" pattern, but it inverts the English-speaker's instinct. In English, location often comes first (\"In the room there's a desk\"); in Japanese, the topic comes first (\"The desk is in the room\"). Beginners default to location-first and end up using ある/いる as if they were \"there is.\" The correct frame is X-as-topic + に + locative + ある/いる.",
        'common_pitfalls': "Using が instead of は when the topic is already known (が introduces NEW information; は marks GIVEN). Forgetting the animacy split (animate → います, inanimate → あります). Using で instead of に for static existence (で is action-location, に is existence-location).",
        'contrasts': "vs ~に~があります (n5-092): the が-form introduces NEW information about a location. は-form assumes the topic is already known and tells you WHERE it is.",
        'closing_practice_tip': "Walk around your room. For 5 already-mentioned items, build the は-に sentence: 「机は ヘや の中に あります」. Then for 5 unmentioned items, build the が-form: 「ヘや に 大きい まどが あります」. The は/が swap drives where the new information lands.",
    },
    'n5-015': {  # この/その/あの/どの + Noun
        'intro': "Adjectival demonstratives that ALWAYS attach directly to a noun: この本 (this book), その人 (that person near you), あの店 (that shop over there), どのカバン (which bag).",
        'why_it_matters': "These look identical in meaning to これ/それ/あれ/どれ but grammatically must take a noun. Mixing up the two systems (using これ as a determiner: ×これ本) is the most-corrected error among English-speaking learners. The kosoado split itself (near-speaker / near-listener / far / which) is unique to Japanese and worth memorising as a system.",
        'common_pitfalls': "Using これ/それ/あれ/どれ in front of a noun (×これ ペン → must be このペン). Forgetting the listener-relative middle term: その is what's near the OTHER person, not what's far from both.",
        'contrasts': "vs これ/それ/あれ/どれ (n5-014): pronouns standing alone vs. determiners attached to nouns. Same kosoado split, different grammar slot.",
        'closing_practice_tip': "Stand somewhere with 3 objects at different distances. Point at each and say two sentences for each: a pronoun-only one (「これは ペンです」) and a determiner-plus-noun one (「このペンは 高いです」). The body memory locks in which form goes where.",
    },
    'n5-081': {  # い-Adjective past
        'intro': "い-Adjectives form their past tense by replacing い with かった + です: 高い → 高かったです (was expensive). Negative past: 高くなかったです.",
        'why_it_matters': "い-adjectives behave like verbs: they conjugate themselves rather than relying on でした. Beginners coming from な-adjective territory often write 高かったでした (over-conjugated) — wrong. The いstem itself carries the past meaning; です just adds politeness.",
        'common_pitfalls': "Adding でした (×高かったでした) — this double-pasts. Forgetting the irregular いい → よかったです transformation. Mixing in な-adjective patterns (×きれいかった — should be きれいでした, since きれい is na-adj).",
        'contrasts': "vs な-Adjective past (なん-adj + でした): な-adjectives are noun-like and use でした. い-adjectives are verb-like and use かった-stem.",
        'closing_practice_tip': "Conjugate 5 い-adjectives through the full cycle: present (高いです), present-negative (高くないです), past (高かったです), past-negative (高くなかったです). The いstem + かった transformation is the template; everything else builds on it.",
    },
    'n5-079': {  # い-Adjective + です
        'intro': "Polite present-affirmative for い-adjectives: ADJ-い です. The い is the verb-like ending; です just makes the sentence polite. 高いです (it's expensive), 寒いです (it's cold).",
        'why_it_matters': "This is the foundation form that the past, negative, te-form, and connector forms all conjugate from. Get the い-stem instinct here and the rest of い-adjective grammar follows mechanically.",
        'common_pitfalls': "Adding な (×高いなです) — that's only for な-adjectives. Treating いい as regular (×いいかったです) — yields よかったです in the past. Putting です between adjective and noun (×大きいです 本 → must be 大きい本).",
        'contrasts': "vs な-Adjective + です (n5-085): な-adjectives are noun-like (静かです). い-adjectives end in い (高いです).",
        'closing_practice_tip': "Pick 5 i-adjectives (高い・安い・大きい・小さい・あつい). Build a single descriptive sentence for each using です. Then drop the です to feel the casual form. The shift between casual and polite is one syllable away.",
    },
    'n5-023': {  # か question marker
        'intro': "Sentence-final か turns any statement into a yes/no question: 学生です → 学生ですか (Are you a student?). Plain forms also take か (~ですか / ~ますか) but casual speech often drops it and rises intonation instead.",
        'why_it_matters': "か is the simplest, most-used grammar particle in conversation. Mastering it lets you ask questions about anything immediately. The catch: it usually appears with です/ます (polite); in casual speech, intonation alone marks a question (「行く?」 with rising tone).",
        'common_pitfalls': "Adding ? in writing (Japanese uses 。 with か, no ? mark needed). Using か in casual speech (sounds stiff; just rise the tone). Confusing か as 'or' (n5-024) with か as question-marker (different positions in the sentence).",
        'contrasts': "vs か as 'or' (n5-024): question-marker か comes at sentence-end. 'Or' か comes between the alternatives mid-sentence (コーヒーか おちゃ).",
        'closing_practice_tip': "Take 5 statements and turn each into a question by adding か. Then say each statement aloud with rising intonation only (no か) — that's the casual form. The same meaning, two registers.",
    },
    'n5-188': {  # ことができます potential
        'intro': "Productive 'can do' construction: VERB-DICTIONARY + ことができます. 食べる → 食べることができます (can eat). The phrase ことができる literally means 'the thing of doing X is possible.'",
        'why_it_matters': "Japanese has TWO ways to express ability: morphological potential verbs (~e form: 食べられる) and the productive ことができる. The morphological form is more native-sounding for everyday verbs; ことができる sounds slightly formal but is universally applicable. Knowing both gives you flexibility.",
        'common_pitfalls': "Using た-form (×食べたことができます) — only dictionary form attaches to こと-できる. Confusing with ~たことがある (experience) which uses た-form. Over-using ことができる where the potential form is more natural.",
        'contrasts': "vs Verb-potential (e-form, N4): 行ける = can go (compact). 行くことができる = same meaning, more formal. Native speakers prefer the e-form for everyday verbs.",
        'closing_practice_tip': "For 5 verbs you use daily, build both: e-form (食べられる) and ことができる (食べることができる). Speak each aloud. Notice the slight register shift — both correct, contextually different.",
    },
    'n5-083': {  # ~くて connector
        'intro': "い-Adjective te-form: replace い with くて. Joins clauses with adjectives: 大きくて、おいしいです (big and delicious). The くて itself is the conjunction.",
        'why_it_matters': "Without くて, you'd have to say 大きいです。そして、おいしいです — clunky. The くて connector smoothes JP into the natural rhythm. It also serves causation (寒くて、出ません = it's cold so I won't go out).",
        'common_pitfalls': "Using で with i-adjectives (×大きいで → 大きくて). Forgetting irregular いい → よくて. Trying to add です mid-sentence (×大きくてです).",
        'contrasts': "vs な-Adjective て-form ~で (n5-089): same connecting role, different morphology — な-adjective + で.",
        'closing_practice_tip': "For 5 i-adjective + i-adjective pairs, build a connecting sentence using くて: この りょうりは 大きくて、あつくて、おいしいです. The chain of くて feels natural in JP and stilted in English.",
    },
    'n5-067': {  # Verb-た past
        'intro': "Plain past affirmative — the た-form: 食べる → 食べた, 行く → 行った, する → した. Conjugation rules mirror the て-form (just swap て for た).",
        'why_it_matters': "Plain past is the casual default among friends and family — and the form most JP novels and manga use. Learning it doubles your input-comprehension. Also, all subsequent N4-N1 grammar (~たことがある、~たほうがいい、relative clauses) builds on this stem.",
        'common_pitfalls': "Mixing past polite (~ました) with past plain (~た) in the same sentence (jarring). Forgetting irregular する → した, 来る → 来た, 行く → 行った (sokuon). Using ます-form with casual conjunctions (~ましたから sounds like teen-textbook Japanese).",
        'contrasts': "vs ~ました (polite past): same meaning, different register. Plain ~た among peers; ~ました with bosses/strangers.",
        'closing_practice_tip': "Conjugate 5 verbs from each verb class to plain past. Then write one sentence in past polite (~ました) and one in past plain (~た) for each. Read aloud — the casual flow is instantly recognisable.",
    },
    'n5-096': {  # ~より~のほうが
        'intro': "Comparative: A より B のほうが [adj] です — 'B is more [adj] than A.' The comparison is mathematically clear: より marks the BASE, のほうが marks the WINNER.",
        'why_it_matters': "Comparisons are daily-life vocabulary. The Japanese word order (loser-より winner-の方が) is the OPPOSITE of English (X is more than Y), so beginners often invert the items. Mastering this lets you compare prices, sizes, weather, and time confidently.",
        'common_pitfalls': "Inverting the loser/winner order. Forgetting の方 (without の方が, you have より alone, which sounds incomplete in this comparative). Using は instead of が on the winner clause.",
        'contrasts': "vs no comparison (just adjective + です): comparative requires both より and のほうが. Drop either and the comparison feels broken.",
        'closing_practice_tip': "Pick 3 paired items (りんご vs バナナ, 東京 vs 大阪, 月 vs 火). Build comparison sentences in both directions: A の方が, then B の方が. Notice how the meaning flips when you swap which item gets のほうが.",
    },
    'n5-106': {  # Noun が ほしいです
        'intro': "'I want noun' — explicit NOUN-が ほしいです form. Same as n5-101 but with the noun explicit (some learners use n5-101 without the noun marked; this disambiguates).",
        'why_it_matters': "ほしい conjugates like an i-adjective, NOT a verb. Beginners try to verb-conjugate it (×ほしいます). The が marker is also unique: most verbs of wanting use を, but ほしい takes が because the desired thing is grammatically the SUBJECT of the want-state.",
        'common_pitfalls': "Verb-conjugating ほしい (×ほしいます). Using を instead of が. Using ほしい to mean 'I want X' for someone else (use ~ほしがる for third-person desire).",
        'contrasts': "vs ~たいです (n5-104): ほしい wants a NOUN; たい wants to perform an ACTION. 食べたい (want to eat) vs ごはんが ほしい (want food).",
        'closing_practice_tip': "Build 5 sentences with concrete nouns: お金が ほしい, 時間が ほしい, 新しい くるまが ほしい, etc. Then do 5 with ~たい (food + たべたい, sleep + ねたい). The が vs を split is the lesson.",
    },
    'n5-089': {  # な-Adj te-form ~で
        'intro': "な-Adjective te-form: ADJ + で. Joins clauses with な-adjectives: しずかで、きれいです (quiet and clean). Pairs with the い-adj ~くて connector.",
        'why_it_matters': "Without で, you'd write しずかです。そして、きれいです (clunky). The で smoothes connections. Note: な-adjectives use で (the COPULA's te-form), not くて (which is i-adj only).",
        'common_pitfalls': "Using くて with na-adjectives (×しずかくて → しずかで). Adding the な (×しずかなで). Adding です mid-sentence (×しずかでです).",
        'contrasts': "vs ~くて (n5-083): same connecting role, different morphology by adjective class.",
        'closing_practice_tip': "For 5 na-adjective + na-adjective pairs (しずか・きれい・しんせつ), build a connecting sentence with で: この みせは しずかで、きれいで、しんせつです. The で-で-で chain works smoothly in Japanese.",
    },
    'n5-105': {  # Verb-stem たくないです
        'intro': "'Don't want to do' — the negative of ~たいです. Replace たい with たくない: 食べたい → 食べたくない (don't want to eat). +です makes it polite.",
        'why_it_matters': "Politely declining is daily vocabulary: 行きたくないです (I don't want to go). The conjugation follows the i-adjective rule (たい is morphologically an i-adjective). Mastering this confirms the i-adj instinct.",
        'common_pitfalls': "Verb-conjugating たい (×食べたいません). Forgetting です makes it abrupt. Using を when the verb itself takes が (some specific verbs like わかる take が).",
        'contrasts': "vs ~たくなかったです (past negative): replace ない with なかった. Same i-adj template.",
        'closing_practice_tip': "Conjugate 5 verbs through the たい cycle: 食べたい / 食べたくない / 食べたかった / 食べたくなかった. The negation + past + negative-past pattern echoes the い-adjective family.",
    },
    'n5-039': {  # これ/それ/あれ/どれ
        'intro': "Pronouns: これ (this, near speaker), それ (that, near listener), あれ (that, far from both), どれ (which one?). They stand ALONE — no following noun.",
        'why_it_matters': "Critically distinct from the determiner forms (この/その/あの/どの) which take a noun. Speaking from one frame to the other is the single biggest determiner-vs-pronoun confusion among English speakers.",
        'common_pitfalls': "Adding a noun (×これ ペン → must be このペン or just これ alone). Forgetting the listener-relative middle term — それ is what's near the OTHER person, not what's far.",
        'contrasts': "vs この/その/あの/どの (n5-040): determiners attach to nouns; pronouns stand alone.",
        'closing_practice_tip': "Stand at one spot. Point at 3 objects at different distances. Say each one as a stand-alone pronoun (これ・それ・あれ). Then point at one and say a full sentence (これは ペンです). Cement which form needs a noun.",
    },
    'n5-019': {  # いつ when
        'intro': "Question word for time: 'when?' Pairs with から (since when?), まで (until when?), and ごろ (around when?) for richer time questions.",
        'why_it_matters': "いつ is the time-axis question word, mirroring どこ (place) and だれ (person). Combining いつ with particles lets you ask precise time questions — a daily-conversation skill.",
        'common_pitfalls': "Adding に (×いつに → just いつ). Using なんじ (what time of day) when the question is broader (いつ asks about a date or general time; なんじ asks about a clock time).",
        'contrasts': "vs なんじ (what time, clock-precise): いつ is broader (year/month/day/era); なんじ is narrow (HH:MM).",
        'closing_practice_tip': "Build 5 question sentences using いつ at different time scales: いつ生まれましたか (born), いつ来ますか (coming), いつから べんきょう (since when studying), いつまで いますか (staying until when), いつ ごろ (around when).",
    },
    'n5-126': {  # が clause connector "but"
        'intro': "が as a CLAUSE connector means 'but/however' mid-sentence: 寒いですが、出かけます (It's cold, but I'll go out). Different from the SUBJECT-marker が (n5-003) — same character, different position.",
        'why_it_matters': "が-as-but is one of TWO common ways to say 'but' in Japanese (the other being けれど/けど). が is more formal/written; けど is conversational. Knowing both gives you register flexibility.",
        'common_pitfalls': "Confusing the two が functions (subject marker vs but-connector). The position is the cue: が before the verb of the FIRST clause = subject marker; が between two clauses = but-connector.",
        'contrasts': "vs けれど/けど (n5-127): casual variant of the same connector. が is more formal.",
        'closing_practice_tip': "Build 5 'X but Y' sentences. Use が for written/formal: 寒いですが、出かけます. Use けど for casual: 寒いけど、出かける. Same meaning, different register.",
    },
    'n5-017': {  # なに/なん
        'intro': "Two readings of the same kanji 何, used in different contexts. なに is the stand-alone question (何ですか?). なん appears before counters (何時 nanji, 何人 nannin) and certain compounds.",
        'why_it_matters': "The reading split is phonetic — based on what sound follows. Learning the heuristic (なん before て-row, さ-row, た-row, だ-row, ら-row, NA-row consonants; なに otherwise) lets you read native correctly without memorising every counter.",
        'common_pitfalls': "Picking the wrong reading. Forgetting that 何時 reads なんじ (not なにじ). Mistakenly reading 何月 as なにがつ (it's なんがつ).",
        'contrasts': "vs どれ/どこ/だれ — these are stand-alone question words; なに/なん has the special phonetic split because of the kanji's broader use.",
        'closing_practice_tip': "Build 8 question sentences: 4 with なに alone (何ですか?), 4 with なん + counter (何時、何人、何月、何曜日). Read aloud — the phonetic shift is the lesson.",
    },
    'n5-101': {  # ~がほしいです
        'intro': "'I want X' for noun objects: NOUN が ほしいです. ほしい is morphologically an i-adjective (it conjugates 高いだ-style). The が is the marker because the desired thing is the SUBJECT of want-state.",
        'why_it_matters': "Wanting is daily vocabulary: 時間が ほしい (I want time), お金が ほしい (I want money). The が-marker is unique to this construction; nouns of wanting elsewhere use を. Plus ほしい conjugates like i-adj, not verb.",
        'common_pitfalls': "Using を (×ペンを ほしい). Verb-conjugating ほしい (×ほしいます). Using ほしい about other people's desires (use ~ほしがる for third-person; ほしい is first-person only).",
        'contrasts': "vs ~たいです (n5-104): ほしい wants a NOUN; たい wants to perform an ACTION.",
        'closing_practice_tip': "Build 5 'I want NOUN' sentences with concrete needs: 時間・お金・新しい本・きゅうけい (rest)・ともだち. The が-marker after each noun is the muscle.",
    },
    'n5-001': {  # ~です/~ます polite copula
        'intro': "The polite-language ON switch. です = polite copula (after nouns / na-adjectives / sentence-end). ます = polite verb ending (replaces dictionary-form ending).",
        'why_it_matters': "These are the foundation of polite Japanese. Master ~です/~ます and you can speak politely to anyone — bosses, strangers, customers. Drop them and you sound casual (only safe with friends/family). Knowing when to switch between the two registers IS the daily social muscle of Japanese.",
        'common_pitfalls': "Mixing です with verb-form (×食べるです). Mixing です with i-adjective (the い is the verb-form: 高いです, NOT 高いだ). Forgetting past forms: でした (was) and ました (did).",
        'contrasts': "vs Plain forms (~る, ~だ): same meanings, casual register. Use plain with friends/family; use polite with everyone else (default to polite as a learner).",
        'closing_practice_tip': "Take a sentence you'd say to a friend (drop です/ます: 食べる) and re-cast it for a teacher (keep them: 食べます). Do this for 5 verbs and 5 noun sentences. The mental flick between casual and polite is the social muscle you're building.",
    },
    'n5-134': {  # Sentence + ので
        'intro': "Soft 'because/since' connector. CLAUSE-plain + ので、CLAUSE = 'Because [first], [second].' Slightly softer / more polite than から.",
        'why_it_matters': "ので vs から is a subtle but real register choice. ので is preferred in formal contexts, requests, and apologies. から is more direct and casual. Using the right one signals social awareness.",
        'common_pitfalls': "Conjugating the verb before ので as polite (~ますので) — usually plain form ~るので or ~たので is more natural. Using ので in casual exclamations (use から or just から).",
        'contrasts': "vs から (sentence-final, n5-009/n5-133): same meaning, slightly different feel. ので is softer/written; から is direct/spoken.",
        'closing_practice_tip': "Build 3 'because X, Y' sentences. Try each with ので (more formal feel) and から (more direct). Notice how the same meaning carries different emotional weight.",
    },
    'n5-132': {  # ~がくれます receive (in-group)
        'intro': "Giving direction: '[Outer person] が [me/in-group] に [thing] を くれます' — they give to ME / my in-group. くれる is the verb that flows OUTSIDE → INSIDE.",
        'why_it_matters': "The Japanese give-receive triple (あげる / くれる / もらう) tracks WHO gives to WHOM relative to YOU. くれる specifically means 'they gave to ME (or someone in my group).' English flatfens this to 'give'; Japanese is precise about direction.",
        'common_pitfalls': "Using あげる when the recipient is YOU (wrong direction; should be くれる). Using もらう (which means 'I receive') when the action is from-the-other-side (use くれる instead). Forgetting the in-group distinction.",
        'contrasts': "vs あげる (n5-130): I/in-group give to outer. vs もらう (n5-131): I receive from outer.",
        'closing_practice_tip': "Build a triangle: you (私), close friend (友だち), distant person (先生). For 5 interactions, decide which verb (あげる/くれる/もらう) is correct based on the direction of the gift. Repeat until the direction is automatic.",
    },
    'n5-041': {  # ここ/そこ/あそこ/どこ
        'intro': "Place words: ここ (here, near speaker), そこ (there, near listener), あそこ (over there, far), どこ (where?). Same kosoado split, applied to LOCATION.",
        'why_it_matters': "Place-asking and direction-giving daily vocabulary. The listener-relative middle term (そこ) is unique to Japanese — English collapses it into 'there.' Asking どこですか? is the most common 'where' question.",
        'common_pitfalls': "Using これ/それ/あれ for LOCATIONS (these are object pronouns). Confusing そこ (near listener) with あそこ (far from both).",
        'contrasts': "vs これ/それ/あれ (objects): same kosoado split, different category (locations vs things).",
        'closing_practice_tip': "Stand and ask どこ for 3 unknown locations. Then point at 3 places (here, near you, far) and label each with the right pronoun. The body memory of which finger goes with which word locks in the system.",
    },
    'n5-046': {  # だれ/どなた who
        'intro': "Question word for people: だれ (casual, who?) / どなた (polite, who?). Pair: だれ for friends and family; どなた when speaking up the social ladder.",
        'why_it_matters': "Choosing the right register here is the difference between casual fluency and rude usage. Asking 'who?' to a customer with だれ sounds curt; どなたですか? signals respect.",
        'common_pitfalls': "Using だれ in formal contexts. Using どなた with friends (sounds stilted). Forgetting that the answer-side often uses regular nouns or names, not the same question word back.",
        'contrasts': "vs です (statement) vs か (question): だれ and どなた are themselves the question words; the sentence still ends in ですか.",
        'closing_practice_tip': "Practice asking 'who is X?' to two imagined audiences: a friend (だれですか?) and a customer (どなたですか?). The register flick is the lesson.",
    },
    'n5-131': {  # ~に/から ~をもらいます
        'intro': "'I receive X from Y' — Y に/から、X を もらいます. に for personal givers (人), から for institutional/abstract sources.",
        'why_it_matters': "Receiving expression. The に vs から split is subtle but native-feeling: receive a gift from a friend = に (friend-に もらう); receive a notification from the company = から (会社-から もらう).",
        'common_pitfalls': "Using を on the giver (it's the receiver who gets を for the thing received; the giver gets に or から). Using もらえる instead of もらう (potential vs basic).",
        'contrasts': "vs くれる (n5-132): くれる is from-their-perspective (they give to me); もらう is from-my-perspective (I receive). Same event, different focus.",
        'closing_practice_tip': "Build 5 'I received X from Y' sentences. Use に for personal givers (友だちに 本を もらいました), から for organizations (会社から お金を もらいました). The に-vs-から signal is the muscle.",
    },
    'n5-048': {  # どこ where
        'intro': "Question word for location: 'where?' Stand-alone or with から/まで/に/で for richer location questions: どこから (from where), どこまで (until where), どこに (at where, existence), どこで (at where, action).",
        'why_it_matters': "Pairs with the kosoado place system (n5-041). Combining どこ with location particles is daily-traveler vocabulary. Each particle changes the meaning subtly.",
        'common_pitfalls': "Using どこ alone when a particle would clarify (どこですか? vs どこに ありますか? — the second specifies existence-location).",
        'contrasts': "vs ここ/そこ/あそこ (n5-041): どこ is the question; the others are answers.",
        'closing_practice_tip': "Build 4 different どこ questions for the same target (the post office): どこですか / どこに ありますか / どこで かいますか / どこから 来ました. Notice the role each particle plays.",
    },
    'n5-065': {  # Verb-る dictionary form
        'intro': "Plain (dictionary) form — non-past affirmative, casual register. The 'verb as listed in a dictionary' form: 食べる, 行く, する, 来る. Replaces ~ます with the verb's basic stem-plus-ending.",
        'why_it_matters': "Dictionary form is the casual default among friends. It's also the form that all subsequent conjugations build from — past plain (~た), te-form (~て), potential (~e), conditional (~ば), passive, causative, etc. all start here.",
        'common_pitfalls': "Mixing dictionary with polite forms in the same sentence (~る...～ました — pick one register). Using dictionary form to bosses/strangers (sounds rude or overly familiar).",
        'contrasts': "vs ~ます (n5-058): same meaning, casual vs polite register.",
        'closing_practice_tip': "Pick 5 verbs you use daily. Conjugate each into dictionary form (食べる、する、来る、行く、書く). Then say each in casual sentences. Notice how the rhythm differs from ~ます-form.",
    },
    'n5-127': {  # けれど/けど but informal
        'intro': "Casual variants of が-as-but: けれど (slightly formal) and けど (most casual). Same role: connect two contrasting clauses. Among friends, けど is the default.",
        'why_it_matters': "けど is what you'll hear in real Japanese conversations. The textbook-が is more written. Using けど in a conversation feels natural; using が feels like reading a textbook out loud.",
        'common_pitfalls': "Confusing けど (but) with the question particle (which doesn't exist in this exact form — but けど can soften a request). Mixing けど with です/ます when the surrounding speech is plain.",
        'contrasts': "vs が (n5-126): formal/written equivalent. Same meaning, different register.",
        'closing_practice_tip': "Take 3 'but' sentences and say each with けど (casual): 寒いけど、行く. Then say each with が (formal): 寒いですが、行きます. Notice the register shift.",
    },
    'n5-018': {  # だれ/どなた (alt)
        'intro': "Same question word as n5-046 — included again because the pattern files split casual だれ from polite どなた as separate entries. The pair: だれ for friends/peers, どなた for customers/elders.",
        'why_it_matters': "Mastering this register split signals social awareness. Asking 'who?' politely (どなたですか?) when you should be casual feels distancing; using だれ when you should be polite sounds curt.",
        'common_pitfalls': "Picking the wrong register. Using だれ with strangers (rude). Using どなた with close friends (overly stiff).",
        'contrasts': "vs n5-046: same word, this entry surfaces it as the polite variant only.",
        'closing_practice_tip': "Imagine 5 conversational partners (boss, friend, stranger, customer, family). Ask 'who is X?' for each — pick だれ or どなた based on the relationship. The social calibration is the lesson.",
    },
    'n5-161': {  # Noun + の + まえに
        'intro': "'Before NOUN' — NOUN + の + まえに. The の glues the noun to the time-marker まえに (before-at). 食事 の まえ に = before the meal.",
        'why_it_matters': "Time-relative expressions chain naturally with の: NOUN + の + TIME-WORD (まえ/あと/とき/ころ). Same pattern across many expressions; learning one unlocks the rest.",
        'common_pitfalls': "Forgetting the の (×食事まえに). Using で instead of に (まえに is the time-marker; で would change the meaning).",
        'contrasts': "vs Noun + の + あとで (n5-160): まえに = before; あとで = after. Same template, opposite time direction.",
        'closing_practice_tip': "Build 3 sentence pairs using まえに / あとで for the same noun: 食事 (before/after the meal), しごと (before/after work), じゅぎょう (before/after class). Mirror the time direction.",
    },
    'n5-029': {  # possessive の
        'intro': "の as the possessive / noun-modifier marker: NOUN1 の NOUN2 = NOUN1's NOUN2 / NOUN2 of NOUN1. 私の本 (my book), 日本の食べ物 (Japan's food / Japanese food).",
        'why_it_matters': "の is the workhorse of Japanese noun-noun connections. Without の, you can't link two nouns. The catch: の has many uses (possessive / category / question marker), and beginners conflate them.",
        'common_pitfalls': "Forgetting の between two nouns (×私 本 → 私の本). Adding extra の (×私の私の本). Confusing の-as-possessive with の-as-question (n5-031).",
        'contrasts': "vs ~んです (n5-167): んです is explanatory ending, not the same の.",
        'closing_practice_tip': "Walk around your room. Identify 5 objects and link each to a possessor or category: 私の本, 母の カバン, 学校の つくえ. The N1のN2 template clicks after 10 reps.",
    },
    'n5-159': {  # ~ですね / ~ですよ
        'intro': "Polite versions of the sentence-final particles ね (seeking agreement) and よ (asserting / informing). Add です first, then the particle: 寒いですね (it's cold, isn't it?), おいしいですよ (it's delicious, you know!).",
        'why_it_matters': "ね and よ inject conversational warmth and engagement. Without them, your sentences sound flat and robotic. Native conversation uses them constantly.",
        'common_pitfalls': "Confusing ね (seek agreement) with よ (assert/inform). Using ね when the listener has no shared knowledge to agree to. Using よ when the listener already knows the info (sounds preachy).",
        'contrasts': "vs ね/よ alone (casual, n5-156): same particles in plain register.",
        'closing_practice_tip': "Take a 5-line conversation. Sprinkle ね or よ at the end of each line based on whether you're seeking agreement (ね) or asserting (よ). Read aloud — the conversational warmth is instantly felt.",
    },
}


# Apply
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

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

with_essay = sum(1 for p in patterns if p.get('essay'))
print(f'Added: {added}')
print(f'Total essays: {with_essay}/178')
