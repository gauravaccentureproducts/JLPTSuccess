"""IMP-137 final round: essays for the last 28 patterns. Completes
178/178 grammar essays."""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ESSAYS = {
    'n5-142': {
        'intro': "Decision-making: NOUN + に + します. コーヒーに します = I'll have coffee. The に marks the chosen item.",
        'why_it_matters': "Daily restaurant/decision vocabulary. The 'I'll go with X' construction is universal.",
        'common_pitfalls': "Using を (×コーヒーを します — different meaning). Confusing with なる (becomes — passive).",
        'contrasts': "vs ~になります (n5-143): なる is automatic/passive becoming. する is active choice.",
        'closing_practice_tip': "Order 5 things at a restaurant: コーヒーに します, ラーメンに します.",
    },
    'n5-143': {
        'intro': "Becoming: NOUN/ADJ + になります or い-ADJ-stem + くなります. 大きくなりました = (it) became big. Automatic / state-change.",
        'why_it_matters': "Daily change-of-state vocabulary. The split for adjectives (に for na-adj/noun, く for i-adj) parallels the entire adjective system.",
        'common_pitfalls': "Mixing the morpheme (×大きにに → 大きくなる). Using しなる (must be なる).",
        'contrasts': "vs ~にします (n5-142): する is active choice; なる is passive becoming.",
        'closing_practice_tip': "Build 3 change-of-state: 大きくなりました, きれいに なりました, 学生に なりました.",
    },
    'n5-027': {
        'intro': "Combined particle よね. Assertion + seeking confirmation. 高いですよね = it's expensive, right? You're inviting agreement on something the listener also knows.",
        'why_it_matters': "Conversational warmth. Stronger than ね alone — adds the assertion. Common in shared-experience contexts.",
        'common_pitfalls': "Using when listener doesn't share the knowledge (sounds presumptuous).",
        'contrasts': "vs ね alone (n5-025): pure agreement. vs よ alone (n5-026): pure assertion. よね combines both.",
        'closing_practice_tip': "Build 3 sentences where you share an observation and seek agreement: 寒いですよね, おいしいですよね.",
    },
    'n5-111': {
        'intro': "Hour counter. NUMBER + 時 (じ). 三時 = 3 o'clock. Use for telling time and time-of-events.",
        'why_it_matters': "Universal hour-marker. Pairs with 分 (minute, n5-112) for full clock times.",
        'common_pitfalls': "Reading shifts (4時 = よじ; 7時 = しちじ; 9時 = くじ). Using じ alone without number.",
        'contrasts': "vs 分 (n5-112): minute counter.",
        'closing_practice_tip': "Read 5 clock times: 1時, 4時, 7時, 9時, 12時. Pay attention to reading shifts.",
    },
    'n5-038': {
        'intro': "Distributive: NUMBER + COUNTER + ずつ. 一つずつ = one each / one apiece. Distributes the quantity per item.",
        'why_it_matters': "Specific quantification — 'each gets one' vs 'total is one.' Used in many real contexts: handing things out, dosing medicine, voting.",
        'common_pitfalls': "Forgetting the counter before ずつ (×一ずつ → 一つずつ).",
        'contrasts': "vs だけ (n5-033): だけ = only / just. ずつ = one each / per.",
        'closing_practice_tip': "Build 3 distributive sentences: みんなに 一つずつ あげます.",
    },
    'n5-052': {
        'intro': "'How / by what means.' どうやって + Verb. どうやって 来ましたか = how did you come? Asks the method/route.",
        'why_it_matters': "Distinguishes 'how' (method) from 'how' (state). どうやって = method; どう = state/condition.",
        'common_pitfalls': "Using どう (different meaning — state/opinion).",
        'contrasts': "vs どう (n5-050): different question type.",
        'closing_practice_tip': "Ask 3 method-questions: どうやって 行きますか? どうやって つくりますか?",
    },
    'n5-099': {
        'intro': "Like / dislike. NOUN + が + すきです / きらいです. The が-marker is mandatory because feeling-states take subjects, not objects.",
        'why_it_matters': "Daily-life vocabulary. The が-marker is the same rule as じょうず, へた, わかる.",
        'common_pitfalls': "Using を (×コーヒーを すきです). Treating すき as a verb (×すきます).",
        'contrasts': "vs じょうず/へた (n5-100): same が-marker rule for state.",
        'closing_practice_tip': "List 3 likes and 3 dislikes: ___が すきです / ___が きらいです.",
    },
    'n5-073': {
        'intro': "'Currently not doing.' Verb-て + いません. 食べて いません = (I am) not eating / haven't eaten. Specific to ongoing state-of-not-doing.",
        'why_it_matters': "Pairs with まだ + ~ていません ('not yet'). Distinct from simple negative ~ません (just 'don't do').",
        'common_pitfalls': "Confusing with simple negative. The いません implies state, not just generic refusal.",
        'contrasts': "vs ~ません (n5-059): ません = simple don't. ていません = not in state of doing.",
        'closing_practice_tip': "Build 3 'not in state': まだ 来て いません, しゅくだいを して いません.",
    },
    'n5-116': {
        'intro': "'Every X' time-prefix: まいにち (every day), まいしゅう (every week), まいつき (every month), まいとし (every year). The まい prefix is common.",
        'why_it_matters': "Daily-frequency vocabulary. Master the prefix once for all four time-scales.",
        'common_pitfalls': "Adding particles (these are time-words and don't take particles).",
        'contrasts': "Pairs with frequency adverbs (n5-147): まいにち = literal 'every day'; よく = 'often'.",
        'closing_practice_tip': "Build 4 routines using each time-prefix: まいにち, まいしゅう, まいつき, まいとし.",
    },
    'n5-172': {
        'intro': "'Don't have to.' Verb-NEG-て + も + いい. 行かなくても いい = don't have to go. Permission-to-not.",
        'why_it_matters': "Daily-life vocabulary. The opposite of ~なくては いけない (must do).",
        'common_pitfalls': "Confusing with ~てもいい (permission to do). The negation is on the action verb.",
        'contrasts': "vs ~なくては いけない (n5-173): must do. ~なくてもいい = don't have to.",
        'closing_practice_tip': "Build 3 permission-to-not sentences: 行かなくても いいです, 食べなくても いいです.",
    },
    'n5-179': {
        'intro': "Casual quotation marker: ~って. CLAUSE-plain + って + main-verb. 田中って いう 人 = a person called Tanaka. Casual contraction of と言う / という.",
        'why_it_matters': "Native casual speech is full of って. Recognising it as a contraction of と is core listening skill.",
        'common_pitfalls': "Using in formal speech (use と instead). Confusing with the topic-marker って (different role).",
        'contrasts': "vs と (n5-008): formal/written quotation marker.",
        'closing_practice_tip': "Translate 3 casual statements: 田中って いう 人, おもしろいって 言いました.",
    },
    'n5-144': {
        'intro': "'While doing X.' Verb-stem + ながら + main verb. 食べながら 話す = talk while eating. Two simultaneous actions.",
        'why_it_matters': "Daily multitasking vocabulary. The Verb-stem + ながら template is unique — different from the て-form chain.",
        'common_pitfalls': "Using dictionary form (×食べる ながら → 食べ ながら). Forgetting the second verb is the main verb.",
        'contrasts': "vs Verb-て chain (n5-070): chain = sequential. ながら = simultaneous.",
        'closing_practice_tip': "Build 3 multitasking sentences: おんがくを 聞きながら べんきょうします.",
    },
    'n5-124': {
        'intro': "Formal contrast: しかし. Sentence-initial 'however.' 安いです。しかし、おいしくありません = it's cheap. However, it's not tasty.",
        'why_it_matters': "Formal-writing transition. Use in essays, business writing, formal emails. でも is the casual equivalent.",
        'common_pitfalls': "Using in casual speech (sounds stiff). Using mid-sentence (use が instead).",
        'contrasts': "vs でも (n5-123): casual sentence-initial. vs が (n5-126): mid-sentence.",
        'closing_practice_tip': "Construct 3 contrasts. Use しかし for formal: 安いです。しかし、おいしくありません.",
    },
    'n5-149': {
        'intro': "'Please give me X.' NOUN + を + ください. お水を ください = water please. Standard request for items.",
        'why_it_matters': "Service Japanese — restaurants, shops, daily life. The Verb-てください is for actions; ~を ください is for things.",
        'common_pitfalls': "Forgetting を. Using の instead of を (×お水の ください).",
        'contrasts': "vs Verb-てください (n5-071): action vs item.",
        'closing_practice_tip': "Order 5 items: お水を ください, コーヒーを ください, おちゃを ください.",
    },
    'n5-151': {
        'intro': "Polite offer: NOUN + は + いかがですか. コーヒーは いかがですか = how about coffee? More formal than どう ですか.",
        'why_it_matters': "Service-Japanese / hospitality vocabulary. Polite hostess offering refreshments.",
        'common_pitfalls': "Using in casual speech (sounds stiff). Confusing with どうですか (casual).",
        'contrasts': "vs どう ですか (n5-050): casual version.",
        'closing_practice_tip': "Offer 3 things politely: コーヒーは いかがですか, ケーキは いかがですか.",
    },
    'n5-122': {
        'intro': "'And then / after that.' それから. Sentence-initial connector. Stronger sequencer than そして — explicitly 'after that.'",
        'why_it_matters': "Native narrative-style. Use to make sequence explicit.",
        'common_pitfalls': "Using mid-sentence. Confusing with から (different meaning).",
        'contrasts': "vs そして (n5-121): generic 'and.' それから = explicit 'after that.'",
        'closing_practice_tip': "Narrate 3-step sequence using それから between each step.",
    },
    'n5-181': {
        'intro': "Sentence-final exclamation: ~なあ. きれいだなあ = wow, it's pretty! Used in moments of strong feeling.",
        'why_it_matters': "Emotional expression. Recognising it in casual speech and song lyrics is a core listening skill.",
        'common_pitfalls': "Using in formal contexts (sounds too casual/childish).",
        'contrasts': "vs ね (n5-025): seek agreement. なあ = personal exclamation.",
        'closing_practice_tip': "Add なあ to 3 statements where you feel strongly: きれいだなあ, おなかが すいたなあ.",
    },
    'n5-148': {
        'intro': "Frequency adverbs: いつも (always), たいてい (usually), たまに (occasionally). Each marks a different frequency band.",
        'why_it_matters': "Daily-frequency vocabulary. Pairs with the n5-147 cluster (よく/ときどき/あまり/ぜんぜん) — both essential.",
        'common_pitfalls': "Using positive adverb with negative verb. Confusing たいてい with いつも.",
        'contrasts': "Frequency: いつも (always) > たいてい (usually) > たまに (occasionally) > あまり~ない (rarely) > ぜんぜん~ない (never).",
        'closing_practice_tip': "Describe a habit using each: いつも 7時に 起きます, たいてい コーヒーを 飲みます, たまに えいがを 見ます.",
    },
    'n5-056': {
        'intro': "Question: 'what day of the week.' なんようび. 何曜日ですか? = what day is it? Combine with 月曜日, 火曜日, etc.",
        'why_it_matters': "Daily date-vocabulary. Asking and stating the day is essential.",
        'common_pitfalls': "Using なに (must be なん). Forgetting the 曜日 part (just なん is too vague).",
        'contrasts': "vs なんがつ/なんにち (n5-057): different time-units.",
        'closing_practice_tip': "Ask 3 day-related questions: 今日は なんようび?, あしたは なんようび?",
    },
    'n5-060': {
        'intro': "Polite past affirmative: Verb-stem + ました. 食べました = ate. Standard polite past.",
        'why_it_matters': "Daily polite-past vocabulary. Mastering ます/ました/ません/ませんでした completes the polite quartet.",
        'common_pitfalls': "Mixing with plain past. Forgetting irregular forms.",
        'contrasts': "vs plain ~た (n5-067): casual variant.",
        'closing_practice_tip': "Conjugate 5 verbs: 食べました, 行きました, しました, 来ました.",
    },
    'n5-061': {
        'intro': "Polite past negative: Verb-stem + ませんでした. 食べませんでした = didn't eat. Standard polite past-negative.",
        'why_it_matters': "Completes the polite quartet. The longest form (4 syllables) but mechanically simple.",
        'common_pitfalls': "Forgetting でした. Mixing register.",
        'contrasts': "vs plain ~なかった (n5-068): casual.",
        'closing_practice_tip': "Conjugate 5 verbs through past-negative: 食べませんでした, 行きませんでした.",
    },
    'n5-150': {
        'intro': "More polite request: NOUN + を + おねがいします. コーヒーを おねがいします = I'd like coffee, please. Slightly more formal/polite than ~を ください.",
        'why_it_matters': "Hospitality / service-Japanese. The おねがいします is an explicit polite request.",
        'common_pitfalls': "Mixing with ください (interchangeable but different feel). Using in non-request contexts.",
        'contrasts': "vs ~を ください (n5-149): also polite, slightly more direct.",
        'closing_practice_tip': "Order 3 items politely: コーヒーを おねがいします, おちゃを おねがいします.",
    },
    'n5-146': {
        'intro': "'Said that ~.' CLAUSE-plain + と + 言いました. たかいと 言いました = (he/she) said it's expensive.",
        'why_it_matters': "Universal reported-speech. Daily conversation has lots of 'X said Y' — this is the template.",
        'common_pitfalls': "Using polite form before と (×たかいですと → たかいと). Confusing with と思います (think vs said).",
        'contrasts': "vs ~と思います (n5-145): said vs thought.",
        'closing_practice_tip': "Report 3 statements: ___と 言いました, then 3 thoughts: ___と 思います.",
    },
    'n5-171': {
        'intro': "Negative advice: 'shouldn't do.' Verb-NEG + ほうが いい. ねないほうが いい = shouldn't sleep. Mirror of n5-170.",
        'why_it_matters': "Daily-advice vocabulary. The ない-form-before-ほうがいい is the lock.",
        'common_pitfalls': "Using た-form (mixing with positive advice form). Forgetting ない agrees with the verb being warned against.",
        'contrasts': "vs ~た方が いい (n5-170): positive advice.",
        'closing_practice_tip': "Build 3 negative-advice: たばこを すわないほうが いい, おそく ねないほうが いい.",
    },
    'n5-178': {
        'intro': "Intention: Verb-plain + つもりだ / つもりです. 行く つもりです = I intend to go. Expresses planned future action.",
        'why_it_matters': "Daily-future vocabulary. Different from simple future tense — つもり emphasizes the plan/intention.",
        'common_pitfalls': "Using past form before つもり (×行ったつもり — different meaning, 'pretending to have gone'). The standard meaning needs dictionary form.",
        'contrasts': "vs simple future: just present-form. つもり emphasizes intent.",
        'closing_practice_tip': "Build 3 intention statements about future plans: あした 行く つもりです, べんきょうする つもりです.",
    },
    'n5-177': {
        'intro': "'Too much / excessive.' Verb-stem or Adj-stem + すぎる. 食べすぎる = eat too much. The すぎる adds the 'excessive' nuance.",
        'why_it_matters': "Common in real conversation: 高すぎる (too expensive), 寒すぎる (too cold), 食べすぎた (ate too much).",
        'common_pitfalls': "Forgetting to use the stem (not dictionary form). Using with 大きい (×大きすぎ → 大きすぎる, drop the い).",
        'contrasts': "vs ~とても (very): just intensification. すぎる = excessive (negative).",
        'closing_practice_tip': "Build 3 'too X' sentences: 高すぎる, 寒すぎる, 食べすぎた.",
    },
    'n5-113': {
        'intro': "'Half past' = ~時はん. 三時はん = 3:30. The はん indicates 30 minutes past.",
        'why_it_matters': "Daily clock-time vocabulary. Pairs with 何時 + 何分 forms. Universal way to express :30.",
        'common_pitfalls': "Using when not exactly 30 (use 三時 三十分 for precision). Confusing with はん (which is just 'half').",
        'contrasts': "vs ~時 + ~分: more precise; ~時はん is the lazy 'half-past' reading.",
        'closing_practice_tip': "Read 3 half-past times: 7時はん, 10時はん, 12時はん.",
    },
    'n5-053': {
        'intro': "'How much (price).' いくら + ですか. これは いくらですか? = how much is this? Specific to monetary value.",
        'why_it_matters': "Daily-shopping vocabulary. The MOST-asked question by traveler in Japan. Pairs with answers in 円.",
        'common_pitfalls': "Using いくつ instead (×いくつですか — for prices use いくら).",
        'contrasts': "vs いくつ (n5-054): general count. いくら = price specifically.",
        'closing_practice_tip': "Build 3 price-questions: これは いくらですか? あの 本は いくらですか?",
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


# Kanji compliance — same cleanup
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
    ('包', 'つつみ'), ('紙', 'かみ'), ('早く', 'はやく'),
    ('顔', 'かお'), ('太郎', 'たろう'), ('起きる', 'おきる'),
    ('起きた', 'おきた'),
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
    '語': 'ご', '達': 'たち', '起': 'お',
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
