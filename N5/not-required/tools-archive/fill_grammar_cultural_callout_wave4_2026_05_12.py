"""Wave 4 — finish cultural_callout (n5-117..n5-187).

After this, coverage 121/178 -> 178/178 (100%).
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CALLOUTS = {
    'n5-117': {'note': 'きょう / あした / きのう / あさって / おととい — daily time words. Mind the readings (kyou not konnichi for "today"). きのう / あした are the most-used; あさって / おととい are extras. Native speakers chain them: "あしたのあさって" sounds wrong — be specific.', 'contexts': ['daily_speech']},
    'n5-118': {'note': 'いま / すぐ / もう / まだ — temporal adverbs. もう ("already" with affirmative; "anymore" with negative) flips meaning by sentence polarity. まだ ("still / not yet") — context decides. Drill the polarity-flipping behavior.', 'contexts': ['daily_speech', 'progress_status']},
    'n5-119': {'note': '〜まえ (before) — noun-style "before". "食事のまえ" = "before the meal". Combine with verbs via plain form: "食べるまえに" = "before eating". Don\'t use past tense — まえ always takes plain-non-past.', 'contexts': ['scheduling', 'sequence']},
    'n5-120': {'note': '〜あと (after) — counterpart to まえ. With verbs: "食べたあとで" — note the た-form (past) before あと. The で is optional but common.', 'contexts': ['scheduling', 'sequence']},
    'n5-121': {'note': 'そして (and / and then) is the most-used clause connector in written narrative. In speech, それから feels more natural. Don\'t overuse そして — it can sound list-like / mechanical.', 'contexts': ['writing', 'narrative']},
    'n5-122': {'note': 'それから (and then / after that) — sequential. Stronger than そして; emphasizes the AFTER-NESS. Restaurant orders: "コーヒー、それからケーキ" = "coffee, and then cake".', 'contexts': ['sequence', 'ordering']},
    'n5-123': {'note': 'でも (but / however) — sentence-initial casual contrast. "暑いです。でも、行きます" = "It\'s hot. But I\'m going". Conversational; in writing use しかし for emphasis.', 'contexts': ['conversation', 'contrast']},
    'n5-124': {'note': 'しかし (however) — formal/written contrast. Business documents, news articles, academic writing. Replace with でも in casual chat.', 'contexts': ['business', 'news', 'academic']},
    'n5-125': {'note': 'では / じゃ (well then, in that case) — topic-shift adverb. じゃ is casual; では is formal. Used as conversational hinge: "じゃ、行きましょう" = "well then, let\'s go". Often signals beginning of the end of a conversation.', 'contexts': ['conversation', 'leaving']},
    'n5-126': {'note': 'が (clause-but) — mid-sentence adversative. "高いですが、おいしいです" = "expensive but tasty". Softer than けど/けれど; works in both casual and formal contexts.', 'contexts': ['mid-sentence_contrast', 'soft_disclaimer']},
    'n5-127': {'note': 'けれど / けど (but, informal) — casual mid-sentence contrast. けど is conversational; けれど slightly more polished. "美味しいですけど、高いです" = "tasty but expensive". Use けど freely with peers; switch to が in formal.', 'contexts': ['casual_contrast']},
    'n5-130': {'note': 'あげる (give to others, downward/outward) — direction-of-action verb. "私が彼にあげる" = "I give to him". Cannot be used for giving TO YOURSELF (use もらう / くれる instead). Cultural rule: outsider-giving is あげる.', 'contexts': ['gift_giving', 'verb_direction']},
    'n5-131': {'note': 'もらう (receive) — counterpart to あげる. "私が彼にもらう" = "I receive from him". Direction is INWARD to speaker. Takes に for personal givers, から for impersonal sources ("会社からもらう" = "received from the company").', 'contexts': ['receiving', 'verb_direction']},
    'n5-132': {'note': 'くれる (give to me / in-group) — direction-of-action verb. ONLY when the receiver is the speaker or speaker\'s in-group. "彼が私にくれる" = "he gives to me". The verb FLIPS direction vs あげる.', 'contexts': ['receiving_to_in-group', 'verb_direction']},
    'n5-133': {'note': '〜から / 〜ので — see n5-009 / n5-129 / n5-134. The "because" cluster: から (direct), ので (softer/polite). Choose by register.', 'contexts': ['reasons']},
    'n5-135': {'note': 'Verb (plain) + Noun — basic relative clause. "私が食べた本" = "the book I ate (read)". NO の between the verb and noun. Common error: inserting の: "私が食べたの本" — WRONG.', 'contexts': ['descriptions', 'relative_clauses']},
    'n5-136': {'note': 'Adj + Noun — see n5-078 / n5-084 for i-adj vs na-adj. Mind the な mandatory for na-adj before noun.', 'contexts': ['descriptions']},
    'n5-137': {'note': 'Noun の Noun — see n5-029. の binds nouns hierarchically.', 'contexts': ['descriptions']},
    'n5-142': {'note': '〜にします — "to decide on / choose". Restaurant: "コーヒーにします" = "I\'ll have coffee". Used at decision-points. The に here is the marker of the chosen option.', 'contexts': ['decisions', 'ordering']},
    'n5-143': {'note': '〜になります / 〜くなります — "becomes". With nouns: になる. With i-adj: drop い + くなる ("高くなる"). With na-adj: になる ("きれいになる"). Captures transformation / change over time.', 'contexts': ['change', 'progression']},
    'n5-144': {'note': 'Verb-stem + ながら (while doing) — simultaneous action. "歩きながら話します" = "I talk while walking". Mind: the SUBJECT for both actions must be the same person.', 'contexts': ['simultaneity']},
    'n5-145': {'note': '〜とおもいます (I think that ~) — softens opinions. "明日は雨だとおもいます" = "I think it\'ll rain tomorrow". Mandatory hedge in polite contexts; brashly asserting an opinion without とおもいます sounds aggressive.', 'contexts': ['opinions', 'polite_hedging']},
    'n5-146': {'note': '〜と言いました — "said that ~". Quote marker と + 言う. The quoted clause stays in plain form: "明日来ると言いました" not "明日来ますと言いました" (the latter is acceptable in formal quotation).', 'contexts': ['reporting', 'narration']},
    'n5-147': {'note': 'よく / ときどき / あまり / ぜんぜん — frequency adverbs. ぜんぜん is NEGATIVE-only ("ぜんぜん飲みません" = "I don\'t drink at all"). あまり is also negative-only ("あまり飲みません" = "I don\'t drink much"). Common error: positive ぜんぜん usage in casual modern Japanese sounds wrong in textbooks.', 'contexts': ['frequency', 'descriptions']},
    'n5-148': {'note': 'いつも / たいてい / たまに — always / usually / occasionally. Place at the head of the sentence: "いつも起きるのが遅いです" = "I always wake up late". たまに is rarer than ときどき.', 'contexts': ['frequency']},
    'n5-149': {'note': '〜をください — "please give me ~". Direct request. Less polite than おねがいします. Restaurant + shopping default. "コーヒーをください" = "please, coffee".', 'contexts': ['service', 'requests']},
    'n5-150': {'note': '〜をおねがいします — "I\'d like ~, please". MORE polite than 〜をください. Used in fancier service contexts, business, formal requests. "コーヒーをおねがいします" softer than 〜をください.', 'contexts': ['polite_service', 'business']},
    'n5-151': {'note': '〜はいかがですか — "how about ~?" (polite offer). Service worker default. "コーヒーはいかがですか" = "would you like some coffee?". Customer-to-friend: use どう instead.', 'contexts': ['service', 'offers']},
    'n5-154': {'note': 'もう + V-ました — "already done". "もう食べました" = "I\'ve already eaten". Often answers a "have you ~ed yet?" question. The もう is essential for the "already" semantic.', 'contexts': ['progress_status', 'questions']},
    'n5-155': {'note': 'See n5-126 for mid-sentence が (but).', 'contexts': ['mid-sentence_contrast']},
    'n5-158': {'note': 'でしょ / だろう — casual だろう sounds masculine/confident. でしょ is gender-neutral / softer. Watch register and gender connotations: men use だろう, women lean toward でしょ.', 'contexts': ['casual_prediction', 'gender_register']},
    'n5-159': {'note': 'See n5-025 / n5-026 for ね / よ. The polite forms are unchanged — register hinges on the sentence ending, not the particle itself.', 'contexts': ['polite_speech']},
    'n5-160': {'note': 'See n5-120 for あとで.', 'contexts': ['scheduling']},
    'n5-161': {'note': 'See n5-119 for まえ.', 'contexts': ['scheduling']},
    'n5-162': {'note': 'Verb-plain + まえに — "before doing X". Mind: ALWAYS plain non-past, even if the action is past. "行くまえに食べた" = "I ate before going" (past).', 'contexts': ['sequence']},
    'n5-163': {'note': 'Verb-た + あとで — "after doing X". Mind: ALWAYS plain past form before あとで. "食べたあとで行きます" = "I\'ll go after eating".', 'contexts': ['sequence']},
    'n5-164': {'note': '〜さん — universal name suffix. Use it FOR EVERYONE except yourself and family insiders. Dropping the さん is intimate / disrespectful in non-close contexts. Top-3 cultural rule.', 'contexts': ['names', 'politeness']},
    'n5-165': {'note': 'お〜 / ご〜 — beautifying / honorific prefixes. お for native Japanese (お茶, おみず); ご for Sino-Japanese (ご飯, ご家族). Wrong prefix sounds strange. Used by women slightly more than men; both should know the conventional forms.', 'contexts': ['polite_speech', 'gendered_register']},
    'n5-166': {'note': 'Set greetings (いただきます / ごちそうさま / おはようございます) — situational fixed phrases that learners CANNOT vary. Saying "ごはんを食べる前のあいさつ" instead of いただきます sounds learner-laboratory. Memorize verbatim.', 'contexts': ['set_phrases', 'meal_etiquette']},
    'n5-167': {'note': '〜んです / 〜のです — "the reason is that ~" or "is it that ~?". Explanation hedge. "あ、痛いんです" = "ah, it hurts (that\'s why)". Native speakers add this when explaining a situation; learners over-use it on ALL statements.', 'contexts': ['explanation', 'soft_assertion']},
    'n5-169': {'note': 'Verb-た + ことがある — "have done before (experience)". "日本に行ったことがあります" = "I\'ve been to Japan". Past-tense FORM (た) but PRESENT-tense meaning ("have experience"). Don\'t use for one-off past actions — use plain past.', 'contexts': ['experience', 'travel']},
    'n5-172': {'note': '〜なくてもいい — "don\'t have to". Polite refusal of obligation. "行かなくてもいいです" = "you don\'t have to go". Useful for excusing oneself in business contexts.', 'contexts': ['obligation', 'permission']},
    'n5-173': {'note': '〜なくてはいけない — "must do". Formal full form. Used in business writing and instruction signs. The negative double-no morphology ("if not doing then no-good") is a key drill point.', 'contexts': ['obligation', 'rules']},
    'n5-174': {'note': '〜なければならない — formal variant of 〜なくてはいけない. Slightly more academic / official. Both express "must do".', 'contexts': ['formal_obligation']},
    'n5-175': {'note': '〜なきゃいけない / 〜なきゃならない — spoken contraction. Casual conversation default for "must do". Native ear: 〜なきゃ is everyday, 〜なくては is textbook.', 'contexts': ['casual_obligation']},
    'n5-176': {'note': '〜なきゃ — ultra-contracted "must do" (drop いけない / ならない entirely). "もう行かなきゃ" = "I gotta go". Very casual; signals time pressure / monologue.', 'contexts': ['ultra_casual', 'monologue']},
    'n5-177': {'note': 'V-stem + すぎる — "too much / excessive". "食べすぎる" = "eat too much". Conjugates as ichidan: すぎます/すぎた/すぎない. Often used confessionally: "昨日、飲みすぎました" = "I overdrank yesterday".', 'contexts': ['excess', 'confession']},
    'n5-178': {'note': 'Verb-plain + つもりだ — "intend to". Stronger commitment than たい (want). "来年、日本に行くつもりです" = "I plan to go to Japan next year". Used for confident future plans.', 'contexts': ['plans', 'commitment']},
    'n5-179': {'note': '〜って — casual quotation marker / topic introducer. Replaces formal と / は in chat. "東京って大きい街だ" = "Tokyo, it\'s a big city". Avoid in formal contexts.', 'contexts': ['casual_quotation', 'topic_intro']},
    'n5-180': {'note': 'V-stem + かた — "way of doing". "食べかた" = "way of eating", "書きかた" = "how to write". Often combined with の: "書きかたを教えてください" = "please teach me how to write".', 'contexts': ['how_to', 'instructions']},
    'n5-181': {'note': '〜なあ — sentence-final exclamation. "高いなあ" = "wow, expensive!". Strongly informal / introspective. Saying なあ in business context sounds inappropriate; even with friends, it\'s mostly used in monologue or warm exclamation.', 'contexts': ['exclamation', 'monologue']},
    'n5-182': {'note': 'Verb-plain + な — STRONG / CASUAL prohibition. "見るな" = "DON\'T look!". Very imperative; used by male speakers in command contexts (sports coaches, parents-to-kids). Avoid in polite speech.', 'contexts': ['strong_command', 'gendered_register']},
    'n5-183': {'note': 'Question word + か / も — "something / anyone" compounds. 何か (something), 誰か (someone), どこか (somewhere). With も: 何も (nothing — needs negative verb), 誰も (no one). The か-vs-も distinction is critical: か = some, も = no.', 'contexts': ['indefinite_pronouns']},
    'n5-184': {'note': 'See n5-183 — 何か / 何も rule for something / nothing.', 'contexts': ['indefinite_pronouns']},
    'n5-185': {'note': 'See n5-183 — 誰か / 誰も for someone / no one.', 'contexts': ['indefinite_pronouns']},
    'n5-186': {'note': 'See n5-183 — どこか / どこも for somewhere / nowhere.', 'contexts': ['indefinite_pronouns']},
    'n5-187': {'note': 'いつか / いつも — sometime / always. Note いつも is the ONLY question-word+も compound that doesn\'t require negative ("いつも勉強します" = "I always study"). The others (誰も / 何も / どこも) require negative.', 'contexts': ['indefinite_time']},
}


def main() -> int:
    fp = ROOT / 'data' / 'grammar.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_cultural_callout_wave4')
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
    print(f'\nWave 4 added cultural_callout on {n} more patterns.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
