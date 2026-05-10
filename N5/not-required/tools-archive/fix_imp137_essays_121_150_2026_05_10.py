"""IMP-137 round-5: essays for patterns 121-150."""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ESSAYS = {
    'n5-135': {
        'intro': "Relative clauses: VERB-PLAIN + NOUN. きのう 食べた りょうり = 'the food I ate yesterday.' The verb directly modifies the noun without any 'that/which.'",
        'why_it_matters': "JP relative clauses are huge in literature and dialogue. The compactness ('the food I ate' = three syllables in JP) is what makes JP feel so concise. No relative pronoun needed.",
        'common_pitfalls': "Adding な/の between verb and noun (×食べたな りょうり). Using polite form (×食べました りょうり → 食べた りょうり).",
        'contrasts': "vs Adj + Noun (n5-136): adjective modifies noun. Verb-plain + Noun is the action-modifier counterpart.",
        'closing_practice_tip': "Build 5 relative clauses: きのう 食べた もの, よく 行く みせ, 私が 買った 本. The verb-direct-attachment is the muscle.",
    },
    'n5-107': {
        'intro': "Movement-with-purpose: Verb-stem + に + 行きます/来ます/かえります. 食べに 行きます = go to eat. The に marks the purpose.",
        'why_it_matters': "Daily-life movement vocabulary. Without this, you have to chain two verbs awkwardly. The compact 'go-to-do-X' form is core spoken JP.",
        'common_pitfalls': "Using で instead of に (×食べで 行きます). Forgetting to use Verb-stem (not dictionary form).",
        'contrasts': "vs ~に + 行きます (n5-005): same に-marker, but here it's verb-stem (action), not noun (location).",
        'closing_practice_tip': "Build 5 'go to do X' sentences: 買い物に 行きます, あいに 行きます, 食べに きました.",
    },
    'n5-183': {
        'intro': "Question word + か/も compound: なにか/なにも, だれか/だれも, どこか/どこも, いつか/いつも. The か introduces existence; the も + neg = nothing.",
        'why_it_matters': "Closed-system pattern that maps cleanly onto English 'something/someone/somewhere/sometime' and 'nothing/no one/nowhere'. Master the pattern once for all 4 question words.",
        'common_pitfalls': "Mismatching polarity (か needs positive, も needs negative for nothing-meaning). Forgetting どこも + positive = 'everywhere.'",
        'contrasts': "vs each individual entry (n5-184/185/186/187): same template, applied to specific question words.",
        'closing_practice_tip': "Build a yes/no minipair for each: なにか 食べた? — はい / いいえ、なにも 食べていない. Repeat for だれ/どこ/いつ.",
    },
    'n5-129': {
        'intro': "Q-and-A reason pattern: どうして〜か。〜から。 'Why? Because.' Sets up a question-answer rhythm.",
        'why_it_matters': "Standard Q&A grammar. The どうして・なぜ asks why; the answer-clause uses から (or です). Learn the question-answer pair as a unit.",
        'common_pitfalls': "Forgetting から in the answer. Using でも instead of から (でも contrasts; から explains).",
        'contrasts': "vs Sentence + から (n5-133): from-the-answer side. n5-129 is the full Q&A unit.",
        'closing_practice_tip': "Construct 3 Q&A pairs: どうして 来ましたか? — 田中さんに 会いたかったから.",
    },
    'n5-102': {
        'intro': "Understanding: NOUN + が + わかります. 日本語が わかります = I understand Japanese. The が-marker is mandatory.",
        'why_it_matters': "Daily-conversation vocabulary. Like すき/きらい/じょうず, わかる takes が because the comprehended thing is grammatically the SUBJECT of the understanding-state.",
        'common_pitfalls': "Using を (×日本語を わかります). Confusing わかる with 知る (n5-145 conceptual differences).",
        'contrasts': "vs 知っている (knowing as fact): わかる = comprehending; 知っている = factual knowledge.",
        'closing_practice_tip': "Build 5 'I understand X' sentences using が: ___が わかります.",
    },
    'n5-147': {
        'intro': "Frequency adverbs cluster: よく (often), ときどき (sometimes), あまり~ない (not often), ぜんぜん~ない (not at all). The first two are positive; the last two need negative verb.",
        'why_it_matters': "Daily frequency-talk. Mastering these 4 covers the entire frequency spectrum. The negation-pairing for あまり/ぜんぜん is grammatical.",
        'common_pitfalls': "Using あまり with positive (must be negative). Forgetting ぜんぜん requires negative.",
        'contrasts': "Frequency goes from よく (often) → ときどき (sometimes) → あまり (rarely) → ぜんぜん (never). Native frequency-vocabulary.",
        'closing_practice_tip': "For 5 hobbies/habits, pick the right frequency: よく 食べます / ときどき 行きます / あまり 見ません / ぜんぜん しません.",
    },
    'n5-050': {
        'intro': "'How / how about?' どう (casual) / いかが (formal). コーヒーは どう ですか? = how about coffee? Used to ask state, opinion, or to offer.",
        'why_it_matters': "Daily-conversation vocabulary. The casual/formal split mirrors だれ/どなた and どうして/なぜ. Native interaction relies on these.",
        'common_pitfalls': "Using いかが in casual speech (sounds stiff). Confusing with どうして (which asks 'why,' not 'how').",
        'contrasts': "vs どう (casual): same word, different register.",
        'closing_practice_tip': "Build 3 questions in both: コーヒーは どう?(casual) / コーヒーは いかが?(formal). The register flick is the lesson.",
    },
    'n5-097': {
        'intro': "2-way comparison: A と B と、どちらが [adj] ですか? = 'A or B, which is [adj]?' The pair is mandatory; the question word is どちら.",
        'why_it_matters': "Daily comparative-question. Different from 3+ option (which uses どれ). The 2-way limit makes どちら-form unique.",
        'common_pitfalls': "Using どれ (which is for 3+). Forgetting the second と.",
        'contrasts': "vs どれが (3+ options): different question word.",
        'closing_practice_tip': "Build 3 2-way questions: コーヒーと おちゃと、どちらが すきですか? Each forces a binary answer.",
    },
    'n5-173': {
        'intro': "'Must do.' Verb-NEG-て + は + いけない (or なりません). 行かなくては いけない = must go. The double-negative ('not-going-doesn't-work') logic.",
        'why_it_matters': "Common formal must-do form. The いけない vs ならない is subtle: いけない = generally required; ならない = morally/socially required. Both work.",
        'common_pitfalls': "Casual register confusion (use なくちゃ for casual). Mixing いけない with いけません (the latter is just polite form).",
        'contrasts': "vs ~なくちゃ (n5-176): casual contraction. vs ~ないといけない (n5-175): variant.",
        'closing_practice_tip': "Build 3 must-do sentences: べんきょうしなくては いけません. Then re-cast each in casual なくちゃ form.",
    },
    'n5-145': {
        'intro': "'I think (that).' CLAUSE-plain + と + おもいます. たかいと おもいます = I think it's expensive. The と is the quotation marker for thoughts.",
        'why_it_matters': "Universal 'I think' for opinions. Different from 知っている (factual knowledge). Learn to express opinion vs fact.",
        'common_pitfalls': "Using polite form before と (×たかいですと → たかいと). Confusing with knowing (use 知っている for factual knowledge).",
        'contrasts': "vs ~と言いました (n5-146): said vs thought. Same と-marker, different verb.",
        'closing_practice_tip': "Build 5 opinion statements: ___ と おもいます. Stop using です/ます before と.",
    },
    'n5-182': {
        'intro': "Strong / casual prohibition. Verb-plain + な = 'don't!' 行くな = don't go! Used in commanding tones — among friends, in coaching, signs.",
        'why_it_matters': "Recognizing this in real speech is core listening skill. Subtitles/manga use this constantly. Distinguish from な (don't!) and な (sentence-final).",
        'common_pitfalls': "Confusing with sentence-final な. Using in polite contexts (sounds rude or curt).",
        'contrasts': "vs ~ないでください (n5-077): polite negative request. vs ~てはいけません (n5-075): more formal prohibition.",
        'closing_practice_tip': "Build 3 strong-prohibition sentences: 来るな, 食べるな, ねるな. Notice the abrupt commanding tone.",
    },
    'n5-043': {
        'intro': "Adjectival demonstrative + Noun: こんな/そんな/あんな/どんな + N. 'This/that kind of N.' こんな 本 = this kind of book.",
        'why_it_matters': "Different from この/その/あの (specific instance). こんな is the QUALITY/KIND. こんな 人 (this kind of person, as a category).",
        'common_pitfalls': "Confusing with この (which is specific instance). Forgetting どんな is the question form ('what kind of').",
        'contrasts': "vs この/その/あの/どの (n5-040): kind/category vs specific instance.",
        'closing_practice_tip': "Build 3 kind-of sentences: こんな 本が すきです. Then 3 specific-instance: この 本が すきです. Notice the category vs item shift.",
    },
    'n5-078': {
        'intro': "Direct attachment: い-Adjective + Noun. 大きい いえ = big house. No な, no の — just adjective immediately before noun.",
        'why_it_matters': "Foundational i-adj + noun pattern. Without な or の, just direct attachment. The simplest noun-modifier rule.",
        'common_pitfalls': "Adding な (the い-adj keeps its い form). Using past form unnecessarily.",
        'contrasts': "vs な-Adj + な + N (n5-084): different morphology. vs Noun + の + N (n5-137): noun-noun bridge.",
        'closing_practice_tip': "Build 5 i-adj noun phrases: 大きい いえ, 小さい こども, 高い 山, あつい コーヒー, 安い 本.",
    },
    'n5-168': {
        'intro': "List of representative actions: ~たり~たりする. 本を 読んだり、テレビを 見たり します = (I do things like) read books and watch TV. Implies 'among other things.'",
        'why_it_matters': "Universal way to describe routines. The ~たり~たり pattern signals 'these are examples of what I do, not the complete list.' Native conversation common.",
        'common_pitfalls': "Forgetting する at the end. Using only one ~たり without the second (the pair is essential).",
        'contrasts': "vs Verb-て chain (n5-070): chain is sequential ('then this'). ~たり is unordered representative actions.",
        'closing_practice_tip': "Describe a weekend routine using 3 ~たり verbs: 本を 読んだり、コーヒーを のんだり、ねたり します.",
    },
    'n5-157': {
        'intro': "Probability marker. CLAUSE-plain + でしょう. あした 雨 でしょう = it'll probably rain tomorrow. Polite version of だろう.",
        'why_it_matters': "Daily forecast / opinion vocabulary. The polite probability form. Used in news weather forecasts and polite conversation.",
        'common_pitfalls': "Using だ before でしょう (×だ でしょう → just でしょう). Confusing with definite statement.",
        'contrasts': "vs だろう (n5-158): casual variant. vs ~んです (n5-167): explanatory.",
        'closing_practice_tip': "Make 3 future predictions politely: あした さむい でしょう, ともだちが 来る でしょう.",
    },
    'n5-166': {
        'intro': "Set greetings cluster: いただきます (before eating), ごちそうさま (after eating), おはようございます (good morning), and the related rituals.",
        'why_it_matters': "Cultural backbone of Japanese daily life. These aren't optional — say them at the right moments and you signal cultural competence.",
        'common_pitfalls': "Saying just いただき or おはよう alone in formal context. Forgetting the closing rituals.",
        'contrasts': "Each greeting has a paired moment: いただきます ↔ ごちそうさま; おはよう ↔ いってらっしゃい. Pairs.",
        'closing_practice_tip': "Run through a daily flow: morning greeting → meal opening → meal closing → goodbye. Practice each in correct context.",
    },
    'n5-170': {
        'intro': "Advice / recommendation: 'should do.' Verb-た + ほうが いい. ねた ほうが いい = should sleep. Past form is mandatory; the た marks completed-state-as-recommendation.",
        'why_it_matters': "Daily-advice vocabulary. The た-form-before-ほうがいい is the lock; using dictionary form changes meaning.",
        'common_pitfalls': "Using dictionary form (×ねる ほうがいい — different meaning). Mixing with ~た方が (the kanji is N5; the kana is the same here).",
        'contrasts': "vs ~ない方が いい (n5-171): negative advice (shouldn't do).",
        'closing_practice_tip': "Build 3 advice sentences: ねた ほうがいい, べんきょうした ほうがいい, 早く 起きた ほうがいい.",
    },
    'n5-021': {
        'intro': "Paired range. NOUN1 から NOUN2 まで. Standard time/place/quantity range form. 9時から 5時まで = from 9 to 5.",
        'why_it_matters': "Same as n5-114 but simpler entry. The paired form is mandatory — leaving off まで sounds incomplete.",
        'common_pitfalls': "Using just から without まで. Confusing with sentence-final から (causation).",
        'contrasts': "vs sentence-final から (n5-009): different function. The paired まで is the cue.",
        'closing_practice_tip': "Build 3 ranges: 月曜日から 金曜日まで, 1時から 3時まで, 100円から 500円まで.",
    },
    'n5-076': {
        'intro': "Sequential 'after doing X.' Verb-て + から. 食べてから 行きます = after eating, I go. The てから is more emphatic than just て.",
        'why_it_matters': "Common sequencer. ~てから specifically asserts 'first X, then Y' more explicitly than just ~て chain.",
        'common_pitfalls': "Confusing with ~てから (causation, which uses から alone after a clause). The てから is a single unit.",
        'contrasts': "vs Verb-た + あとで (n5-163): after-completion. ~てから emphasizes the sequence.",
        'closing_practice_tip': "Build 3 sequences: 食べてから 行きます, 顔を あらってから ねます.",
    },
    'n5-044': {
        'intro': "Manner-kosoado: こう (this way), そう (that way), ああ (that-far way), どう (how). Adverbial — describe MANNER of doing.",
        'why_it_matters': "Native manner-vocabulary. これ/それ/あれ/どれ are objects; ここ/そこ/あそこ/どこ are places; こう/そう/ああ/どう are MANNERS.",
        'common_pitfalls': "Confusing with これ/それ (objects). Mixing with どうして (different meaning, 'why').",
        'contrasts': "vs これ etc. (object): kosoado for objects. vs ここ etc. (place): kosoado for places. Same kosoado split, different category.",
        'closing_practice_tip': "Demonstrate something. Say 「こう やります」 (do it this way). Then ask 「どう やりますか?」 (how do you do it?).",
    },
    'n5-088': {
        'intro': "な-Adj past-negative: ADJ + じゃ + ありませんでした. 静かじゃ ありませんでした = wasn't quiet.",
        'why_it_matters': "Completes the na-adj cycle: present, past, negative, past-negative. Mirrors noun-conjugation.",
        'common_pitfalls': "Using くなかった (i-adj rule wrong). Adding な (×静かなじゃ).",
        'contrasts': "vs ~くなかったです (n5-082): i-adj past-neg.",
        'closing_practice_tip': "Conjugate 5 na-adjectives through past-neg cycle: 静か, きれい, しんせつ.",
    },
    'n5-120': {
        'intro': "Time-marker 'after.' Used after nouns (の あとで) or verbs (た あとで). Mirror of まえ.",
        'why_it_matters': "Time-axis essential vocabulary. Get まえ/あと as a pair and you have past-future fluency.",
        'common_pitfalls': "Confusing with あと alone (just 'remaining'). Using dictionary form before あとで (must be た-form).",
        'contrasts': "vs まえ (n5-119): opposite time direction.",
        'closing_practice_tip': "Build 3 'after' sentences: ねた あとで, ごはんを 食べた あとで.",
    },
    'n5-125': {
        'intro': "Transitional phrase: 'well then / in that case.' では (formal) / じゃ (casual). では、はじめましょう = well, let's begin.",
        'why_it_matters': "Conversation-pivot marker. Use to transition between topics or to wind down/start something. Universal in spoken JP.",
        'common_pitfalls': "Using では in casual speech (use じゃ). Confusing with the negative-suffix では (different particle).",
        'contrasts': "vs それでは (more formal version): same meaning, slightly more formal.",
        'closing_practice_tip': "Construct a conversation that pivots: 「では、行きましょう」 vs 「じゃ、行こう」. The register flick is the lesson.",
    },
    'n5-057': {
        'intro': "Time questions: 何月 (なんがつ — what month) / 何日 (なんにち — what day). Combine 何 with the time-counter.",
        'why_it_matters': "Daily date-asking vocabulary. The 何 + counter pattern is universal; learning it once for time unlocks all date questions.",
        'common_pitfalls': "Using なに instead of なん (×なにがつ → なんがつ). Confusing with なんようび (day of week).",
        'contrasts': "vs なんじ (clock time, n5-055): clock-precise vs date.",
        'closing_practice_tip': "Build 3 date-questions using 何月 and 何日.",
    },
    'n5-164': {
        'intro': "Name suffix: ~さん. The Mr./Ms. equivalent. Use after surnames or full names: 田中さん. Universal politeness marker.",
        'why_it_matters': "Used in EVERY formal interaction. Forgetting さん when addressing someone is rude. Adding it shows basic social competence.",
        'common_pitfalls': "Using on your own name (sounds arrogant — use just your name to others). Forgetting ~ちゃん (small/cute) and ~くん (junior male) variants.",
        'contrasts': "vs ~ちゃん (cute/small): different register. vs ~くん (junior male): age/gender-specific.",
        'closing_practice_tip': "Address 3 people with the right suffix: 田中さん (general), 太郎くん (junior male friend), さくらちゃん (cute/small).",
    },
    'n5-055': {
        'intro': "Clock-precise time question: 何時 (なんじ — what time?). Asks the hour. なんじですか? = what time is it?",
        'why_it_matters': "Daily-life essential. Master once and you can ask the time anywhere.",
        'common_pitfalls': "Using なに (×なにじ → なんじ). Confusing with 何月 (なんがつ).",
        'contrasts': "vs いつ (n5-019): broader time question (year/month/era). なんじ is narrow (HH:MM).",
        'closing_practice_tip': "Ask a friend: 「今、なんじですか?」 Then for an event: 「えいがは なんじから ですか?」.",
    },
    'n5-152': {
        'intro': "Polite-phrase cluster: どうぞ (please/here you go), どうも (thank you, briefly), すみません (excuse me / sorry), おねがいします (please / I beg of you).",
        'why_it_matters': "Service-Japanese essentials. Each maps to a specific social moment. Master the cluster and you cover most polite interactions.",
        'common_pitfalls': "Using どうも as 'thank you' in formal contexts (use ありがとうございます). Confusing どうぞ (giving) with どうも (thanking).",
        'contrasts': "Each phrase has a specific role — どうぞ (offering), どうも (acknowledging), すみません (apologizing/excusing), おねがいします (requesting).",
        'closing_practice_tip': "Run through 4 social moments and say the right phrase: receiving something (どうも), offering food (どうぞ), bumping someone (すみません), making a request (おねがいします).",
    },
    'n5-154': {
        'intro': "'Already did X.' もう + Verb-ました. もう 食べました = already ate. The もう shifts the past tense to 'completed-already.'",
        'why_it_matters': "Common past-completion vocabulary. Pairs with まだ + ~ていません ('not yet'). Learn as a pair.",
        'common_pitfalls': "Using with non-past forms (must be ました). Confusing with もう as 'more' / 'no more.'",
        'contrasts': "vs まだ + ~ていません (n5-153): opposite (not yet).",
        'closing_practice_tip': "Build 3 already-done statements: もう 食べました. Then 3 not-yet: まだ 食べていません.",
    },
    'n5-030': {
        'intro': "Nominalizer: VERB/ADJ-clause + の. Turns the clause into a noun. 食べる の = the act of eating; 高い の = the expensive one.",
        'why_it_matters': "Universal nominalisation. Learn this and you can turn any verb/adj into a noun on the fly. Replaces こと in casual contexts.",
        'common_pitfalls': "Forgetting the の. Confusing with possessive の (n5-029).",
        'contrasts': "vs こと (also nominalizer): こと is more abstract; の is more concrete.",
        'closing_practice_tip': "Nominalize 5 verbs: 食べる の が すき, 行く の が 大すき. Notice how the clause becomes the subject.",
    },
    'n5-112': {
        'intro': "Minute counter: NUMBER + ふん/ぷん. The reading shifts based on the number: 一ぷん (ippun), 二ふん (nifun), 三ぷん (sanpun), 四ふん (yonpun), 五ふん (gofun).",
        'why_it_matters': "Daily time-precision vocabulary. The reading shifts are systematic but require memorising — voiced ぷ after sokuon.",
        'common_pitfalls': "Using one reading uniformly (must shift by number). Forgetting voiced/unvoiced patterns.",
        'contrasts': "vs 時間 (hour, n5-111): different counter.",
        'closing_practice_tip': "Read 5 different minute numbers aloud: 5ふん, 7ふん, 10ぷん, 15ふん, 30ぷん. Notice how the reading varies.",
    },
}


# ---- Apply ----
grammar_path = ROOT / 'data' / 'grammar.json'
data = json.loads(grammar_path.read_text(encoding='utf-8'))
patterns = data['patterns']

added = 0
for p in patterns:
    pid = p['id']
    if pid not in ESSAYS or p.get('essay'):
        continue
    payload = ESSAYS[pid]
    p['essay'] = {**payload, 'provenance': 'llm_curated'}
    added += 1


# Kanji compliance cleanup (extended set)
COMPOUNDS = [
    ('家族', 'かぞく'), ('部屋', 'へや'), ('音楽', 'おんがく'),
    ('元気', 'げんき'), ('天気', 'てんき'), ('一緒', 'いっしょ'),
    ('普通', 'ふつう'), ('時々', 'ときどき'), ('教科書', 'きょうかしょ'),
    ('鉛筆', 'えんぴつ'), ('図書館', 'としょかん'), ('結婚', 'けっこん'),
    ('宿題', 'しゅくだい'), ('勉強', 'べんきょう'), ('遊ぶ', 'あそぶ'),
    ('歩く', 'あるく'), ('運動', 'うんどう'), ('働く', 'はたらく'),
    ('泳ぐ', 'およぐ'), ('運転', 'うんてん'), ('全部', 'ぜんぶ'),
    ('世界', 'せかい'), ('運転する', 'うんてんする'), ('動く', 'うごく'),
    ('才能', 'さいのう'), ('米', 'こめ'), ('包む', 'つつむ'),
    ('包', 'つつみ'), ('五枚', '5まい'), ('七冊', '7さつ'),
    ('五冊', '5さつ'), ('十枚', '10まい'), ('二冊', '2さつ'),
    ('三冊', '3さつ'), ('紙', 'かみ'), ('早く', 'はやく'),
    ('顔', 'かお'), ('太郎', 'たろう'),
]
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
    '思': 'おも', '住': 'す', '才': 'さい', '能': 'のう',
    '動': 'うご', '米': 'こめ', '包': 'つつ', '茶': 'ちゃ',
    '酒': 'さけ', '飯': 'ごはん', '枚': 'まい', '冊': 'さつ',
    '紙': 'かみ', '早': 'はや', '顔': 'かお', '太': 'た',
    '郎': 'ろう', '関': 'かん', '係': 'けい', '事': 'こと',
    '語': 'ご', '達': 'たち',
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
