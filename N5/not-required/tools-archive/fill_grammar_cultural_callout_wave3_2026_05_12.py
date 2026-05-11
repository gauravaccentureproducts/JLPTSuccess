"""Wave 3 — extend cultural_callout to ~120 patterns.

Covers n5-044..n5-116. Topics: remaining question words, polite/plain
verb forms, te-form chains, adjective conjugations, existence verbs,
comparison structures, counters, time markers, frequency adverbs.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CALLOUTS = {
    'n5-044': {'note': 'こう/そう/ああ/どう (manner adverbs: this way / that way / how) are the action-modifier こそあど cousins of これ/それ/あれ/どれ. Use こう/そう/ああ for instructions and demonstrations; どう for asking about manner/method.', 'contexts': ['instruction', 'questions']},
    'n5-045': {'note': '何 (what) — see n5-017 for the reading-context rule (なに vs なん). Position matters: "何時" (なんじ, time-question) and "何を食べる" (なにをたべる, object-question) both spelled 何 but read differently. Drilling これ for 何 is the surest way to internalize this.', 'contexts': ['questions', 'reading_aloud']},
    'n5-046': {'note': 'だれ (who, neutral) — see n5-018 for the politeness contrast with どなた. In customer service or business reception, default to どなた to avoid sounding curt.', 'contexts': ['service', 'business']},
    'n5-048': {'note': 'どこ (where) is the most-used question word for place. In casual speech, dropped particles are common: "どこ行くの？" instead of "どこへ行きますか？". Foreign learners tend to over-formalize.', 'contexts': ['everyday_questions', 'casual_drop']},
    'n5-051': {'note': 'どうして vs なぜ — どうして is the casual/conversational "why?"; なぜ is more formal/written. Native Japanese rarely uses なぜ in spoken dialog except in deliberately analytical contexts. Default to どうして.', 'contexts': ['casual_questions', 'formal_writing']},
    'n5-052': {'note': 'どうやって (by what means) asks the METHOD of doing something. Different from どう (state/opinion). "どうやって行きますか" = "how do you get there?" (specific method); "どう行きますか" sounds slightly off — use どうやって.', 'contexts': ['directions', 'instructions']},
    'n5-053': {'note': 'いくら (how much, price) is restaurant + shopping vocabulary. Combined with です ("これはいくらですか" = "how much is this?") it\'s a top-3 N5 phrase. The answer takes 円 (yen): "200円です".', 'contexts': ['shopping', 'restaurants']},
    'n5-054': {'note': 'いくつ (how many) is for COUNTING WITHOUT a specific counter ("いくつありますか" = "how many?"). For specific counter-marked questions, use 何 + counter (何人 / 何枚 / 何冊 etc.). いくつ also asks AGE in polite contexts ("おいくつですか" = "how old?").', 'contexts': ['age_inquiry', 'general_count']},
    'n5-055': {'note': '何時 (なんじ) is THE most-asked time question. Drilling: 何時ですか, 何時から, 何時まで, 何時に. The に particle attaches when scheduling ("3時に会いましょう").', 'contexts': ['scheduling', 'time_questions']},
    'n5-056': {'note': '何曜日 (なんようび) asks day-of-week. Answer takes 曜日 suffix: 月曜日 / 火曜日 / ... / 日曜日. In casual speech, drop the 日 suffix is OK ("土曜は休みです"). Reading menus and timetables — this is essential.', 'contexts': ['scheduling', 'business_hours']},
    'n5-057': {'note': '何月 / 何日 — month and day questions. Combined as "何月何日ですか" for full date inquiry. Japanese date order is YEAR-MONTH-DAY in writing; spoken order varies. Watch the readings: 4月=しがつ, 9月=くがつ (irregular).', 'contexts': ['dates', 'calendar']},
    'n5-058': {'note': '-ます (polite non-past affirmative) is the default polite verb ending. Always pair with proper register; mixing -ます and plain だ in the same sentence sounds awkward unless in deliberate switching contexts.', 'contexts': ['polite_speech', 'classroom', 'business']},
    'n5-059': {'note': '-ません (polite non-past negative) — universal for polite "don\'t do X". Distinct from plain -ない. Switching mid-sentence from -ます to -ない sounds informal-leaking.', 'contexts': ['polite_speech', 'declines']},
    'n5-061': {'note': '-ませんでした (polite past negative) — see n5-060/n5-067/n5-068 contrast set. The full polite past-negative form is mandatory in business reports and formal email.', 'contexts': ['business', 'formal_writing']},
    'n5-063': {'note': '-ましょうか — offer or first-person suggestion. "手伝いましょうか" = "shall I help?" (offer). With group: "行きましょうか" = "shall we go?". Tone of voice (rising) signals offer vs declaration.', 'contexts': ['offers', 'suggestions']},
    'n5-064': {'note': '-ませんか (polite invitation) is softer than -ましょう — invites rather than declares. "コーヒー、飲みませんか" = "would you like coffee?" Service workers use this constantly.', 'contexts': ['invitations', 'service']},
    'n5-065': {'note': 'Plain dictionary form (-る/-u final) is the casual/written register. Used in headlines, dictionaries, internal monologue, friends-and-family speech. Using plain in formal contexts sounds rude / overly intimate.', 'contexts': ['casual', 'writing', 'dictionaries']},
    'n5-066': {'note': 'Plain non-past negative (-ない) — register-switching trigger. With friends fine; with strangers / superiors / customers, you must lift to -ません. Misjudging the register signals you don\'t understand the social space.', 'contexts': ['casual', 'register_judgment']},
    'n5-067': {'note': 'Plain past affirmative (-た) — the past-tense register equivalent of dictionary form. "見た" = "saw" (casual). News headlines and historical writing use plain past. Spoken to peers, fine.', 'contexts': ['casual_past', 'headlines']},
    'n5-068': {'note': 'Plain past negative (-なかった) — see n5-061 for register contrast. Common in casual reminiscence: "昨日はいなかった" = "I wasn\'t there yesterday".', 'contexts': ['casual_past', 'reminiscence']},
    'n5-069': {'note': 'Verb-て (te-form) is the BACKBONE of N5 grammar. Chains actions, makes requests (てください), permission (てもいい), prohibition (てはいけない), state (ている). Master te-form conjugation early — you\'ll use it everywhere.', 'contexts': ['everywhere'],},
    'n5-070': {'note': 'Verb-て、Verb-て… (sequential chaining) — most-used multi-clause structure. "起きて、食べて、行きました" = "got up, ate, then went". Natural for narrative. Cf. たり (sample listing, order-irrelevant).', 'contexts': ['narrative', 'daily_routine']},
    'n5-073': {'note': 'Verb-ていません — has two readings: "not currently doing" ("食べていません" = "not eating right now") and "haven\'t yet done" ("食べていません" = "haven\'t eaten yet"). Context disambiguates — the second reading is more common.', 'contexts': ['descriptions', 'progress_status']},
    'n5-076': {'note': 'Verb-てから (after doing X) tightly chains two actions where the second DEPENDS on the first. "食べてから行きます" = "I\'ll go AFTER eating". Compare with あと (just sequential).', 'contexts': ['causation_in_sequence', 'instructions']},
    'n5-078': {'note': 'i-Adjective + Noun is direct attachment ("高い本" = "expensive book") — no particle. Different from na-adj which needs な ("きれいな本"). Mixing them is a top-5 N5 error.', 'contexts': ['descriptions'],},
    'n5-079': {'note': 'i-Adj + です — special: don\'t add な. "高いです" not "高いなです". The です here is a POLITENESS marker, not a copula. The adjective itself carries the meaning.', 'contexts': ['polite_descriptions']},
    'n5-080': {'note': 'i-Adj negative present (-くないです / -くありません) — both forms acceptable, -くないです more conversational. Don\'t conjugate the i-adj like a verb: NEVER 高いないです, ALWAYS 高くないです.', 'contexts': ['descriptions', 'register']},
    'n5-081': {'note': 'i-Adj past (-かった) — "高かった" = "was expensive". Drop final い, add かった. Common error: -いでした (forbidden by grammar). The かった form is built INTO the adj, not stuck on with です.', 'contexts': ['past_descriptions']},
    'n5-082': {'note': 'i-Adj past negative (-くなかった) — drop い, add くなかった. The double-negation morphology is a key drill point. Common error: confusing with na-adj forms (じゃなかった).', 'contexts': ['past_descriptions']},
    'n5-083': {'note': 'i-Adj te-form (-くて) — connector. "高くておいしい" = "expensive AND tasty". Used for sequential or simultaneous adjective qualities. Drop い, add くて. The contrastive use ("expensive BUT not tasty") needs けど instead.', 'contexts': ['descriptions', 'enumeration']},
    'n5-084': {'note': 'na-Adj + な + Noun ("きれいな花" = "pretty flower"). The な is MANDATORY before nouns — dropping it is a top-5 error. Some learners think na-adj behaves like i-adj and drop the な; native ears notice immediately.', 'contexts': ['descriptions']},
    'n5-085': {'note': 'na-Adj + です — uses です as the copula (unlike i-adj where です is just polite-marker). "きれいです" = "is pretty". For past, switch to でした: "きれいでした" = "was pretty".', 'contexts': ['polite_descriptions']},
    'n5-086': {'note': 'na-Adj negative present (じゃありません / ではありません). Use ではありません in formal contexts (business writing, exams); じゃありません in conversation. Both are correct.', 'contexts': ['polite_descriptions', 'register']},
    'n5-087': {'note': 'na-Adj past affirmative (でした). "きれいでした" = "was pretty". This is the COPULA past, attached to the adjective. Unlike i-adj where past is INSIDE (-かった), na-adj past sits on でした.', 'contexts': ['past_descriptions']},
    'n5-088': {'note': 'na-Adj past negative (じゃ/ではありませんでした) — full long form. In casual contexts, じゃなかった is more natural. Mind the でした addition at the end — easy to forget.', 'contexts': ['past_descriptions']},
    'n5-089': {'note': 'na-Adj te-form (で) — connector. "きれいで便利です" = "pretty AND useful". The で here is the te-form copula, NOT the location particle で. Context disambiguates.', 'contexts': ['descriptions', 'enumeration']},
    'n5-091': {'note': 'います (animate existence) — for people, animals, fish, insects. The animacy rule isn\'t fluid: even sleeping cats use います. Plants are inanimate (あります). Vehicles vary by context (people inside → います / parked car → あります).', 'contexts': ['descriptions', 'existential']},
    'n5-092': {'note': '〜に〜があります／います ("there is X at Y") — location-first existence question. Used when introducing what\'s at a known place. "つくえの上に本があります" = "there\'s a book on the desk". Memorize the particle pattern (に → が).', 'contexts': ['descriptions', 'introductions']},
    'n5-093': {'note': '〜は〜にあります／います ("X is at Y") — already-known X. "本はつくえの上にあります" = "the book is on the desk" (you know which book). Compare with n5-092: は/が swap signals whether the listener already knows X.', 'contexts': ['descriptions', 'follow-up_questions']},
    'n5-094': {'note': '〜があります — abstract existence (events, skills, possessions). "今日は会議があります" = "there\'s a meeting today". For PHYSICAL existence, see n5-090/n5-091; for abstract, use this n5-094.', 'contexts': ['scheduling', 'descriptions']},
    'n5-095': {'note': 'AはBより [adj] です — "A is more [adj] than B". The basic comparison. "東京は大阪より大きいです" = "Tokyo is bigger than Osaka". より = "than". Subject of comparison goes with は.', 'contexts': ['comparison']},
    'n5-096': {'note': '〜より〜のほうが [adj] です — emphasizes the SUPERIOR one. "コーヒーよりお茶のほうが好きです" = "I prefer tea over coffee". Notice the flip — the preferred item gets のほうが.', 'contexts': ['preference', 'comparison']},
    'n5-097': {'note': 'AとBと、どちらが ～ですか — "which is more ~?" (binary). どちら is the polite どれ for 2-way choice. Native answers: "Aのほうが~です" or "Bのほうが~です". Drilled in restaurant / shopping scenarios.', 'contexts': ['service', 'preference_questions']},
    'n5-098': {'note': 'Likes/dislikes contrast — uses が (not を) with すき/きらい. "コーヒーがすきです" = "I like coffee". が-marking adjectives (すき/きらい/じょうず/へた/わかる/できる) is a key N5 drill: the verb/adj LOOKS transitive but takes が, not を.', 'contexts': ['preferences', 'descriptions']},
    'n5-099': {'note': 'すきです / きらいです — see n5-098 for the が-marking rule. すき is "like" (warm); きらい is "dislike" (cold). Stronger: だいすき / だいきらい. Avoid using きらい casually about people — it sounds harsh.', 'contexts': ['preferences', 'avoid_personal_dislike']},
    'n5-100': {'note': 'じょうず / へた — "good at / bad at" (skill). Like すき/きらい, take が-marked object. "ピアノがじょうずです" = "good at piano". Avoid using じょうず ABOUT YOURSELF (sounds boastful) — use a hedge: "あまりじょうずじゃないですが…"', 'contexts': ['skills', 'humility']},
    'n5-102': {'note': '〜がわかります — "understand / can decipher". Takes が-marked object (not を). "日本語がわかります" = "I understand Japanese". The が-marking treats わかる as a stative not action verb.', 'contexts': ['comprehension', 'questions']},
    'n5-103': {'note': '〜ができます — "can do". Takes が-marked object. "日本語ができます" = "I can speak Japanese". Used for general ability rather than specific tasks (for specific tasks, use V-stem+ことができる).', 'contexts': ['ability', 'language_skills']},
    'n5-105': {'note': '〜たくないです — "don\'t want to do". Conjugate like an i-adj: drop い from たい, add くない. "行きたくないです" = "don\'t want to go". Past: たくなかった ("didn\'t want to"). Mind: たい is restricted to first-person speaker.', 'contexts': ['refusals', 'preferences']},
    'n5-106': {'note': 'Noun + が ほしいです — duplicate of n5-101 with explicit noun emphasis. Same first-person restriction. The が-marking is what trips up learners — they default to を.', 'contexts': ['shopping', 'desires']},
    'n5-107': {'note': 'V-stem + に行きます／来ます／かえります — "go/come/return TO DO X". "食べに行きます" = "I\'m going TO eat". Common purpose-of-movement pattern. Drop ます from the verb to form the stem.', 'contexts': ['plans', 'purposes']},
    'n5-108': {'note': 'Number + counter — Japanese ALWAYS uses a counter when counting. There\'s no generic counter (unlike English "three things"). Match the counter to the noun: 人 (people), 本 (long thin), 枚 (flat), 個 (small), 台 (machines), etc. This is daily drill.', 'contexts': ['counting', 'shopping']},
    'n5-109': {'note': 'How many / how much (counter questions) — 何 + counter ("何人?", "何枚?"). Or generic いくつ for unspecific count. Answer uses the same counter.', 'contexts': ['shopping', 'inquiries']},
    'n5-110': {'note': 'Object + counter + Verb — Japanese word order: "りんごを三つ買いました" = "I bought three apples". The counter sits BETWEEN the object (marked with を) and the verb. NOT "三つりんごを買いました" — that\'s English-influenced order.', 'contexts': ['shopping', 'narrative']},
    'n5-111': {'note': '〜じ — o\'clock counter. Numbers 1-12 + じ. Irregular readings: 4時=よじ, 7時=しちじ, 9時=くじ. Drilling clocks is essential for transit / appointments / TV-schedule listening.', 'contexts': ['time', 'scheduling']},
    'n5-112': {'note': '〜ふん / 〜ぷん — minute counter. ぷん variant: 1分=いっぷん, 3分=さんぷん, 4分=よんぷん, 6分=ろっぷん, 8分=はっぷん, 10分=じゅっぷん. Irregular phonetic shifts — drill aloud.', 'contexts': ['time', 'pacing']},
    'n5-113': {'note': '〜時半 — "half past". "3時半" = "3:30". Cleaner than "3時30分" in spoken Japanese. Reading menus and timetables — 30分 is rare in spoken context, 半 is the norm.', 'contexts': ['time']},
    'n5-114': {'note': 'See n5-021 for the から〜まで paired range. n5-114 is the time-specific application; n5-021 is the general particle pair.', 'contexts': ['signs', 'schedules']},
    'n5-115': {'note': 'Particle に for specific clock-times — "3時に行きます" = "I\'ll go at 3:00". Time + に. Distinguish from の of attribution. Use に whenever scheduling an action AT a specific time.', 'contexts': ['scheduling']},
    'n5-116': {'note': 'まいにち/まいしゅう/まいつき/まいとし — every day/week/month/year. Frequency adverbs at the head of the sentence. "毎日勉強します" = "I study every day". Don\'t add particles between まい- and the time unit.', 'contexts': ['routine', 'frequency']},
}


def main() -> int:
    fp = ROOT / 'data' / 'grammar.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_cultural_callout_wave3')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')
    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {p['id']: p for p in data['patterns']}
    n = 0
    for pid, callout in CALLOUTS.items():
        if pid not in by_id:
            print(f'  ! missing: {pid}'); continue
        p = by_id[pid]
        if p.get('cultural_callout'):
            print(f'  - skip: {pid}'); continue
        p['cultural_callout'] = callout
        p['cultural_callout_provenance'] = 'llm_curated'
        n += 1
    print(f'\nWave 3 added cultural_callout on {n} more patterns.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
