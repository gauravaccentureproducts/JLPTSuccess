"""IMP-137 round-4: essays for patterns 91-120."""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ESSAYS = {
    'n5-074': {
        'intro': "Permission: 'may I do X.' Verb-て + も + いい です. 食べてもいいですか = may I eat? The negation is ~てはいけません.",
        'why_it_matters': "Asking permission politely is daily-life vocabulary — at host families, classrooms, restaurants, hotels. The construction is logical: 'doing-also-good' = 'OK to do.'",
        'common_pitfalls': "Forgetting the も (×食べていいです → 食べてもいいです). Using で instead of て.",
        'contrasts': "vs ~てはいけません (n5-075): permission negated. vs ~ないでください (n5-077): polite request not to.",
        'closing_practice_tip': "Build 5 polite-permission sentences in your daily context: ここで しゃしんを とってもいいですか. Speak each aloud.",
    },
    'n5-026': {
        'intro': "Sentence-final particle for assertion / new info: よ. 高いよ (it's expensive, you know!). Tells the listener something they don't yet know.",
        'why_it_matters': "Without よ, casual statements sound flat. With it, you signal 'I'm informing you.' Misuse (when listener already knows) sounds preachy.",
        'common_pitfalls': "Using よ with shared info (sounds presumptuous). Mixing with formal speech (use ですよ).",
        'contrasts': "vs ね (n5-025): ね seeks agreement; よ asserts new info.",
        'closing_practice_tip': "Take 5 statements where you're informing a friend. Add よ to each. The 'I'm telling you' tone is the lesson.",
    },
    'n5-054': {
        'intro': "Question word: 'how many.' いくつ asks a general count — for things you can count by ones (apples, ideas, ages of small kids).",
        'why_it_matters': "Counter-question vocabulary. いくつ is the universal counter-question; specific counters (何人 nannin, 何枚 nanmai, 何冊 nansatsu) are for specific shape categories.",
        'common_pitfalls': "Using いくつ for clearly-categorized items (use 何 + counter). Forgetting that いくつ doubles as 'how old' for young children.",
        'contrasts': "vs 何 + counter (n5-109): specific counter for the noun's shape. vs いくら (price-only).",
        'closing_practice_tip': "Build 3 'how many' questions for general items: りんごは いくつ ありますか. Then 3 with specific counters: 何人いますか, 何枚 ありますか. Notice when you can use the universal いくつ vs the shape-specific.",
    },
    'n5-035': {
        'intro': "'About / approximately' for quantities. NUMBER + ぐらい/くらい. 五分 ぐらい = about 5 minutes. The two readings are interchangeable.",
        'why_it_matters': "Daily-conversation softener. Without ぐらい/くらい, statements sound clinical. Adding them signals approximation, which is the polite default in Japanese.",
        'common_pitfalls': "Using with vague time-expressions (use ごろ instead — n5-036). Confusing with ごろ (point in time) vs ぐらい (duration/quantity).",
        'contrasts': "vs ごろ (n5-036): ぐらい = duration/amount approx; ごろ = time-point approx.",
        'closing_practice_tip': "Build 3 quantity-approximations with ぐらい (5分 ぐらい, 100円 ぐらい, 二十人 ぐらい). Then 3 time-points with ごろ (3時 ごろ, あした ごろ). Notice which is duration vs point.",
    },
    'n5-051': {
        'intro': "Question word: 'why.' どうして = casual/conversational; なぜ = formal/written. どうして 来ました? = why did you come?",
        'why_it_matters': "The most-used 'why' in conversation. The casual/formal split is similar to だれ/どなた — knowing both gives you register flexibility.",
        'common_pitfalls': "Using なぜ in casual speech (sounds stiff). Forgetting that the answer often uses から (from) or んです (explanation).",
        'contrasts': "vs なぜ: same meaning, formal register.",
        'closing_practice_tip': "Build 3 'why' questions. Use どうして for casual (どうして 行きませんか), なぜ for formal (なぜ おそく なりましたか). The register flick is the lesson.",
    },
    'n5-095': {
        'intro': "Comparative: A は B より [adj] です = 'A is more [adj] than B.' The subject-marker は picks the topic; より marks the comparison base.",
        'why_it_matters': "Daily comparative vocabulary. Pairs with the more focused n5-096 (A より B のほうが — focuses on B as winner).",
        'common_pitfalls': "Word-order inversion (English is 'A is more X than B'; Japanese is 'A は B より X'). Forgetting より.",
        'contrasts': "vs ~より~のほうが (n5-096): focuses on the WINNER. n5-095 is more neutral.",
        'closing_practice_tip': "Build 3 simple comparisons using both: 東京は 大阪より 大きいです (n5-095) and 東京より 大阪のほうが 食べものが おいしいです (n5-096).",
    },
    'n5-036': {
        'intro': "'Around X time.' TIME + ごろ. 三時 ごろ = around 3 o'clock. Used for points in time; pairs with ぐらい which is for durations.",
        'why_it_matters': "Daily time-approximation. Native conversation rarely gives exact times.",
        'common_pitfalls': "Using ごろ for durations (use ぐらい instead). Mixing the two readings — both ぐらい and くらい are interchangeable forms of the same particle.",
        'contrasts': "vs ぐらい/くらい (n5-035): time-point vs amount/duration.",
        'closing_practice_tip': "Build 5 time-point sentences: 7時 ごろ, ごぜんちゅう ごろ. The point-vs-duration distinction is the muscle.",
    },
    'n5-062': {
        'intro': "Volitional / 'let's': Verb-stem + ましょう. 食べましょう = let's eat. Polite suggestion that assumes shared agreement.",
        'why_it_matters': "Standard 'let's' form. Pairs with the offer-form ~ましょうか (n5-063) which gives the listener a choice. ~ましょう presumes agreement.",
        'common_pitfalls': "Using ~ましょう when the listener hasn't agreed (sounds presumptuous; use ~ませんか instead). Confusing with the casual ~う/よう volitional.",
        'contrasts': "vs ~ませんか (n5-064): polite invitation that gives the listener choice. vs ~ましょうか (n5-063): polite offer of help.",
        'closing_practice_tip': "Build 3 'let's' suggestions: いっしょに 食べましょう, さんぽしましょう. Then re-cast each as ~ませんか (less assumed) and ~ましょうか (offering). Three subtle politeness levels.",
    },
    'n5-068': {
        'intro': "Plain past-negative — the なかった form: 食べる → 食べなかった (didn't eat). Combine with です for polite (食べなかったです — but 食べませんでした is more standard).",
        'why_it_matters': "Casual past-negative is everyday vocabulary. The conjugation: take ない form, replace い with かった. なかった → mature い-adjective behavior.",
        'common_pitfalls': "Using ~ませんでした in casual (jarring register). Forgetting irregular しなかった / こなかった.",
        'contrasts': "vs ~ませんでした (polite past-neg): same meaning, different register.",
        'closing_practice_tip': "Conjugate 5 verbs through the casual quartet: ない / なかった / 〜ない form. Speak each in casual sentences.",
    },
    'n5-063': {
        'intro': "Polite offer of help / suggestion: Verb-stem + ましょうか. まどを あけましょうか = shall I open the window? Asks if action is wanted.",
        'why_it_matters': "Service-Japanese vocabulary. Used in shops (お包みしましょうか?), at home (お茶を いれましょうか?), in classes. The か at the end is what makes it an offer, not a directive.",
        'common_pitfalls': "Confusing with ~ましょう (assumes agreement; here you're offering). Forgetting the か.",
        'contrasts': "vs ~ましょう (n5-062): assumes agreement. vs ~ませんか (n5-064): asks the listener to do something with you.",
        'closing_practice_tip': "Build 3 offers: コーヒーを いれましょうか, まどを あけましょうか, テレビを けしましょうか. The 'shall I?' tone is the muscle.",
    },
    'n5-121': {
        'intro': "Sentence connector: 'and then.' そして CLAUSE. Used to add a new sentence: 朝ごはんを 食べました。そして、しごとに 行きました.",
        'why_it_matters': "Sentence-level connector — different from word-level と (which joins nouns). Spoken JP relies heavily on そして / それから for sequential narration.",
        'common_pitfalls': "Using mid-sentence (そして is sentence-initial). Confusing with それから (very similar — そして is generic; それから emphasizes 'after that').",
        'contrasts': "vs それから (n5-122): nuance — それから = 'after that, then'. そして = 'and (further)'. Often interchangeable.",
        'closing_practice_tip': "Narrate a 3-step sequence using そして between each step. Then re-tell using それから. Same story, slightly different feel.",
    },
    'n5-169': {
        'intro': "Experience expression: Verb-た + ことがある. 行ったことがあります = have been (somewhere). Indicates past experience, not just past tense.",
        'why_it_matters': "Distinct from simple past — ~たことがある answers 'have you ever...?' questions. Universal travel/conversation vocabulary.",
        'common_pitfalls': "Using dictionary form (×行く ことがある = different meaning, 'sometimes I go'). Confusing with ~たことがあった (had experienced before — past in past).",
        'contrasts': "vs simple past ~た: simple past is one specific event. ~たことがある is general experience anytime in life.",
        'closing_practice_tip': "Ask a friend (real or imagined): 日本に 行ったことが ありますか? Then 5 of your own experiences: ___を 食べたことが あります.",
    },
    'n5-059': {
        'intro': "Polite non-past negative: Verb-stem + ません. 食べません = don't eat. Pairs with ~ます (positive). Standard polite negative.",
        'why_it_matters': "Mirrors ~ます. Mastering this completes the polite-conjugation foundation: ~ます / ~ません / ~ました / ~ませんでした.",
        'common_pitfalls': "Mixing with plain ~ない in same sentence. Forgetting irregular しません / きません.",
        'contrasts': "vs plain ~ない (n5-066): casual variant.",
        'closing_practice_tip': "Conjugate 5 verbs through the polite quartet: 食べます / 食べません / 食べました / 食べませんでした. The four-form template is the foundation.",
    },
    'n5-153': {
        'intro': "'Not yet.' まだ + Verb-ていません. まだ 食べて いません = haven't eaten yet. The まだ flips ~ています to 'still not done.'",
        'why_it_matters': "Subtle distinction from まだ + simple negative (which means 'still not'). The ~ていません form specifically implies the action is PENDING, not refused.",
        'common_pitfalls': "Using simple negative (×まだ 食べません) — wrong implication. Forgetting to keep ~ています form.",
        'contrasts': "vs もう ~ました (already done): opposite. vs まだ + Verb-non-past (still doing): different.",
        'closing_practice_tip': "Build 3 'not yet' sentences: しゅくだいを まだ して いません. The pending-implication is the lesson.",
    },
    'n5-077': {
        'intro': "Polite negative request: 'please don't do X.' Verb-ない + で + ください. たばこを すわないで ください = please don't smoke.",
        'why_it_matters': "Daily polite-prohibition vocabulary. The ~ないで is the negative te-form; +ください makes it a request.",
        'common_pitfalls': "Using positive ~てください + negative idea (wrong). Forgetting で.",
        'contrasts': "vs ~てはいけません (n5-075): more authoritative ('you must not'). ~ないで ください is a polite request.",
        'closing_practice_tip': "Build 5 polite prohibitions: ここで 食べないで ください, おそく 来ないで ください. The 'please-not-do' form sticks.",
    },
    'n5-123': {
        'intro': "Sentence-initial 'but / however.' でも CLAUSE. 高いです。でも、おいしいです = it's expensive. But it's tasty.",
        'why_it_matters': "Conversational pivot. Different from mid-sentence が — でも starts a NEW sentence, signaling contrast.",
        'common_pitfalls': "Using mid-sentence (use が or けど). Confusing with the particle でも which means 'even.'",
        'contrasts': "vs しかし (n5-124): formal/written. vs けど/が (n5-126/127): mid-sentence variants.",
        'closing_practice_tip': "Build 3 contrast pairs as separate sentences. Connect with でも (casual), then with しかし (formal). Same logic, different register.",
    },
    'n5-087': {
        'intro': "な-Adjective past: ADJ + でした. 静かでした = was quiet. The な disappears in past form (since na-adj behave like nouns).",
        'why_it_matters': "Mirror of noun past. Distinct from i-adj past (which uses かった). Get the na-adj-as-noun instinct.",
        'common_pitfalls': "Using かった (i-adj rule wrong). Adding な (×静かなでした).",
        'contrasts': "vs ~かったです (i-adj past, n5-081): different morphology.",
        'closing_practice_tip': "Conjugate 5 na-adjectives: 静かでした, きれいでした, しんせつでした. The でした-form parallels noun + でした.",
    },
    'n5-084': {
        'intro': "な-Adjective + な + Noun. The な is the link between na-adj and the noun: 静かな へや (quiet room).",
        'why_it_matters': "The な is mandatory when modifying a noun. Forgetting it produces ungrammatical Japanese — one of the most-corrected errors among English speakers.",
        'common_pitfalls': "Forgetting the な. Adding な at sentence-end (it's only between adj and noun).",
        'contrasts': "vs i-Adj + Noun (n5-078): direct attachment, no な.",
        'closing_practice_tip': "Pick 5 na-adjectives. For each, build modifier-form (___ な ___) AND predicate-form (___ です). Notice when な appears.",
    },
    'n5-037': {
        'intro': "'Etc. / and so on.' Used after listed nouns: りんご、バナナ、みかん など (apples, bananas, oranges, etc.). Pairs with や.",
        'why_it_matters': "Signals 'this list isn't exhaustive.' Adding など softens claims — Japanese-conversation polite default.",
        'common_pitfalls': "Using with と (which is exhaustive). Omitting when the list isn't actually complete.",
        'contrasts': "vs と (n5-008, exhaustive listing): use と for complete lists; や/など for partial.",
        'closing_practice_tip': "List 3 categories: foods, places, hobbies — each with や connecting and など at the end. The 'partial-list' marker is the lesson.",
    },
    'n5-031': {
        'intro': "Sentence-final の as informal question. PLAIN-FORM + の? どこに 行く の? = where are you going? Different from possessive の.",
        'why_it_matters': "Casual conversational question marker. Replaces か in plain speech. The intonation is rising. Common in family/friend context.",
        'common_pitfalls': "Using with formal speech (×行きます の). Confusing with possessive の (n5-029).",
        'contrasts': "vs か (n5-023): formal question marker. vs ~んです (n5-167): explanatory rather than purely question.",
        'closing_practice_tip': "Take 5 polite questions and re-cast each as casual の-questions: 行きますか → 行く の?",
    },
    'n5-108': {
        'intro': "Number + Counter pattern. 三人 (3 people), 五枚 (5 sheets), 七冊 (7 books). The counter classifies the noun by SHAPE.",
        'why_it_matters': "Universal counting system. Memorising the right counter for common noun categories (人/まい/ほん/さつ/つ etc.) is essential vocabulary.",
        'common_pitfalls': "Mixing counters (×五人の 本 → 五冊の 本). Forgetting the kanji-vs-kana number reading shifts (3さつ vs 三冊).",
        'contrasts': "Each shape category has its own counter: long-thin (本), flat (まい), bound (冊), small-round (こ).",
        'closing_practice_tip': "Walk through your room. Identify 5 things and count each with the right counter: えんぴつ三本, 本五冊, りんご二つ, 紙十枚, ともだち二人.",
    },
    'n5-070': {
        'intro': "Sequential / chained actions. Verb-て、Verb-て、… Used to chain actions: 朝ごはんを食べて、シャワーを あびて、しごとに 行きます (I eat breakfast, take a shower, and go to work).",
        'why_it_matters': "Native Japanese loves to chain. Without ~て, you'd need separate sentences. The chain creates natural narrative flow.",
        'common_pitfalls': "Mixing tense — only the FINAL verb takes the past tense; the chain stays in て-form. Using ~て with non-sequential actions.",
        'contrasts': "vs それから (n5-122): explicitly sequential, sentence-by-sentence. ~て is more compact.",
        'closing_practice_tip': "Narrate your morning routine as one chained sentence: おきて、ごはんを 食べて、シャワーを あびて、出かけました.",
    },
    'n5-100': {
        'intro': "'Good at / bad at': NOUN が じょうずです / へたです. テニスが じょうずです (good at tennis). The が-marker is mandatory.",
        'why_it_matters': "Daily ability-assertion. The が-marker is the same as for すき/きらい — mental-state predicates need が, not を.",
        'common_pitfalls': "Using を (×テニスを じょうず). Using じょうず as a verb (×じょうずします).",
        'contrasts': "vs できる (n5-103): できる is potential ('can do'); じょうず is skill ('good at').",
        'closing_practice_tip': "Build 3 sentences: ___が じょうずです / ___が へたです. Pick honest examples — Japanese listeners use these about real abilities, not bragging.",
    },
    'n5-094': {
        'intro': "Existence / 'have' for events, skills, possessions. NOUN が あります. しごとが あります = have work. Daily-event vocabulary.",
        'why_it_matters': "Different from physical existence (n5-090). For events and abstract things, ある is the correct verb. パーティーが あります (there's a party).",
        'common_pitfalls': "Using いる for events/abstract (×パーティーが いる). Confusing with possession (which uses 持っています for objects).",
        'contrasts': "vs います (n5-091): for animate beings. vs もっている (have-as-possession): for objects.",
        'closing_practice_tip': "Build 5 'I have an event/ability' sentences: しごとが あります, テストが あります, ピアノの 才能が あります.",
    },
    'n5-117': {
        'intro': "Time-of-day vocabulary cluster: きょう (today), あした (tomorrow), きのう (yesterday), あさって (day after tomorrow), おととい (day before yesterday). All take NO particle.",
        'why_it_matters': "Daily-time vocabulary. The no-particle rule is unique to vague time refs — clock times take に, but vague times stand alone.",
        'common_pitfalls': "Adding に (×あしたに 行きます → あした 行きます). Confusing the directional pairs (おととい / あさって).",
        'contrasts': "vs clock-time + に (n5-115): specific times need に. Vague times don't.",
        'closing_practice_tip': "Build 5 sentences using each of the time words. No particle. The asymmetry with に-times is the lesson.",
    },
    'n5-165': {
        'intro': "Beautifying / honorific prefixes: お~ for native Japanese words, ご~ for Sino-Japanese. お水、お茶、ご飯、ご家族.",
        'why_it_matters': "Politeness-marker. Used when speaking to/about others' things or in formal contexts. Some words are virtually inseparable from お/ご (お茶、お水).",
        'common_pitfalls': "Mixing お/ご (the rule is native vs Sino). Using on speaker's own things in formal contexts (sometimes correct, sometimes not).",
        'contrasts': "Different prefix for different word origins. お for native (お米); ご for Sino (ご家族).",
        'closing_practice_tip': "Build 5 sentences using お/ご prefixes appropriately: お水を ください, ご家族は おげんきですか.",
    },
    'n5-042': {
        'intro': "Polite kosoado: こちら (this way / this person), そちら (that way / that person), あちら (that-far way), どちら (which way). More formal than これ/それ/あれ/どれ.",
        'why_it_matters': "Service / business / introductions. こちらは 田中さんです = 'this is Mr. Tanaka' (introducing). The polite version of the kosoado pronouns.",
        'common_pitfalls': "Mixing register (use casual これ with friends, polite こちら with customers).",
        'contrasts': "vs これ/それ/あれ/どれ (n5-039): casual versions.",
        'closing_practice_tip': "Practice 3 introductions using こちら: こちらは 田中さんです, こちらは わたしの ともだちです. The polite pivot is the muscle.",
    },
    'n5-049': {
        'intro': "Selection question words: どれ (which-one, from 3+), どの (+ noun), どちら (which-one, from 2). The number split is the cue.",
        'why_it_matters': "Asking 'which?' is a daily question. The 2-or-3+ split is unique to Japanese.",
        'common_pitfalls': "Using どれ when there are only 2 options (use どちら). Forgetting the noun-attachment for どの.",
        'contrasts': "vs これ/それ/あれ (n5-039): pronouns alone. vs この/その/あの (n5-040): determiner-form.",
        'closing_practice_tip': "Practice questions for 2-option (どちらが いい?), 3+option (どれが いい?), determiner (どの 本ですか?).",
    },
    'n5-028': {
        'intro': "Possessive / noun-modifier の. NOUN1 + の + NOUN2 = N1's N2. Same as n5-029 — both entries cover this fundamental connector.",
        'why_it_matters': "の is the workhorse of noun connections. Without it, you can't link two nouns. Master one of these patterns and the others follow.",
        'common_pitfalls': "Forgetting の. Stacking too many の (deep nesting).",
        'contrasts': "vs ~んです (n5-167): explanatory ending. vs sentence-final の (n5-031): question marker.",
        'closing_practice_tip': "Build 5 'X's Y' relationships: 私の 本, ともだちの くるま, 日本の 食べもの.",
    },
    'n5-110': {
        'intro': "Quantity-before-verb: NOUN を NUMBER COUNTER + Verb. りんごを 三つ 食べました = I ate three apples. The number+counter goes BEFORE the verb, not before the noun.",
        'why_it_matters': "JP word-order surprise: while you'd say 'three apples' in English, Japanese says 'apples-three.' Mastering the inversion is daily-counting vocabulary.",
        'common_pitfalls': "Putting the number before the noun (×三つの りんごを 食べました — though this is also valid, less common). Using the wrong counter.",
        'contrasts': "vs Number + の + Noun (less common but valid): same meaning, different word-order.",
        'closing_practice_tip': "Count 5 actions: 本を 二冊 読みました, りんごを 三つ 食べました. The number+counter + verb sequence is the muscle.",
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
    p['essay'] = {
        **payload,
        'provenance': 'llm_curated',
    }
    added += 1


# Kanji compliance cleanup
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
    ('包', 'つつみ'),
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
    '酒': 'さけ', '飯': 'ごはん',
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
