"""Author `cultural_callout` on the most-used N5 grammar patterns.

Audit context: cultural_callout = 0/178 across all patterns. The
existing `register` field captures politeness level but doesn't
explain WHEN/WHY a learner picks one form over another in real
Japanese culture (situational, generational, regional, gender).
This pass adds a 1-2 sentence cultural-usage note to the 30 most
foundational N5 patterns.

Schema:
  cultural_callout: {
    note: "<1-2 sentence usage culture note>",
    contexts: ["formal_business", "casual_friends", "writing", ...],
  }

Provenance: llm_curated. Starter pass — patterns 31+ pending in
subsequent batches.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CALLOUTS = {
    'n5-001': {
        'note': 'です/ます (polite affirmative) is the DEFAULT register in business, classrooms, customer-facing situations, and any first encounter. Switching to plain だ/だ.ない is reserved for close friends, family, internal thoughts, or written casual contexts. Mismatching the register is the single most common foreigner mistake.',
        'contexts': ['formal_business', 'classroom', 'customer_service', 'first_meeting'],
    },
    'n5-002': {
        'note': 'は (topic) is overused by learners as a generic "subject" marker. Native speakers DROP は when the topic is obvious from context (most natural in casual speech: "コーヒー、好き？" instead of "コーヒーは好きですか？"). Over-use of は signals foreign-learner speech.',
        'contexts': ['casual_conversation', 'classroom'],
    },
    'n5-003': {
        'note': 'が (subject) marks NEW information or contrast. Native ear distinguishes "山田さんは行きます" (topic-known) vs "山田さんが行きます" (it\'s Yamada — emphasizing identity) instinctively. Over-using は where が is needed signals foreign speech.',
        'contexts': ['narrative', 'introducing_new_info'],
    },
    'n5-021': {
        'note': '〜から〜まで (range) is THE go-to pattern for opening hours signs (9:00から5:00まで). Business signs, transit timetables, and event posters use this format extensively. Master the noun form before the more flexible particle uses.',
        'contexts': ['signs', 'schedules', 'business_hours'],
    },
    'n5-028': {
        'note': 'の (attributive) is the most-used particle in Japanese, appearing every ~7 morphemes. Concatenated chains like 私の友だちの本 ("my friend\'s book") feel verbose to learners but are completely natural in Japanese. Avoid over-pruning.',
        'contexts': ['all_speech', 'writing'],
    },
    'n5-060': {
        'note': '〜ました (polite past) is the workhorse in business reports, email, customer interactions, and lesson narration. Even between close friends, formal events (graduations, business announcements) revert to 〜ました.',
        'contexts': ['business', 'email', 'narration'],
    },
    'n5-062': {
        'note': '〜ましょう (let\'s) is mostly used for INVITING others ("行きましょう" = "let\'s go"). When suggesting your OWN action, casual speakers often use 〜よう/〜ようと思う instead. Volitional is also a polite refusal softener ("そうしましょう" = "let\'s do that, then").',
        'contexts': ['invitations', 'group_planning'],
    },
    'n5-071': {
        'note': 'Verb-てください (please do) sounds DIRECT — equivalent to "please do X" in English. In service contexts (clerk to customer), even softer forms (お+stem+ください / 〜ていただけませんか) are preferred. Use てください with peers/subordinates; soften upward.',
        'contexts': ['service', 'instructions', 'requests'],
    },
    'n5-072': {
        'note': '〜ています has THREE distinct meanings: ongoing action ("読んでいます" = is reading), resulting state ("結婚しています" = is married), habitual ("毎日走っています" = run every day). Context disambiguates; learners often default to "ongoing" and miss the resulting-state reading.',
        'contexts': ['descriptions', 'narrative'],
    },
    'n5-074': {
        'note': '〜てもいいです (permission) is grammatically polite but can sound presumptuous if used to GRANT permission upward ("先生、トイレに行ってもいいです" sounds like you\'re permitting the teacher!). Use 〜てもいいですか (asking) when seeking permission from someone of higher status.',
        'contexts': ['permission', 'classroom'],
    },
    'n5-075': {
        'note': '〜てはいけません (must not / forbidden) carries STRONG prohibitive force — used on official signs (写真をとってはいけません), in parent-to-child / teacher-to-student instruction. Adult peers use softer forms (〜ないでください). Reading: tobacco/photo/parking prohibitions on Japanese signs follow this pattern.',
        'contexts': ['prohibitions', 'signs', 'rules'],
    },
    'n5-077': {
        'note': '〜ないでください (please don\'t) is softer than 〜てはいけません. Common on customer-facing signs ("写真をとらないでください") and in polite refusals ("心配しないでください" = please don\'t worry). The negative request is more face-saving than the affirmative てください.',
        'contexts': ['polite_refusal', 'signs', 'reassurance'],
    },
    'n5-090': {
        'note': 'あります (inanimate existence) vs います (animate existence) is a classic learner trap. Plants are inanimate (あります). Pets, fish, insects use います. Vehicles and ghosts vary by context. The 100% rule: if it moves on its own volition → います; otherwise あります.',
        'contexts': ['descriptions', 'questions'],
    },
    'n5-101': {
        'note': '〜が ほしい (want object) is restricted to FIRST-person speaker desire ("私は車がほしいです"). Saying "彼は車がほしい" sounds wrong — for third-person, use 〜たがる/〜と言っている. This is a key learner error point.',
        'contexts': ['first_person_desire', 'shopping'],
    },
    'n5-104': {
        'note': '〜たい (want to do) has the same first-person restriction as ほしい — "彼は行きたい" sounds wrong; use 〜たがる. Also, たい conjugates as an i-adjective: たいです / たくない / たかった. Many learners over-conjugate it as a verb.',
        'contexts': ['first_person_desire', 'planning'],
    },
    'n5-129': {
        'note': 'どうして〜か。〜から。 is the canonical reason Q-A frame. In casual speech, how/why questions often drop どうして and use 〜の？/〜なの？ pattern instead. Formal speech (business, classroom) prefers どうしてですか.',
        'contexts': ['classroom', 'business', 'curiosity'],
    },
    'n5-134': {
        'note': '〜ので (softer because) sounds more polite than 〜から. Business writing, formal apologies, and customer-facing scripts strongly prefer ので over から. Switching unconsciously to から in formal contexts marks foreign-learner speech.',
        'contexts': ['business', 'apologies', 'formal_writing'],
    },
    'n5-152': {
        'note': 'Set phrases (いらっしゃいませ, ありがとうございました, すみません) are SITUATIONAL: いらっしゃいませ is store-clerk-only (never use to greet a friend); すみません blurs "sorry" + "excuse me" + "thanks" — context decides meaning. Mastering set phrases is mastering Japanese register.',
        'contexts': ['service', 'apologies', 'greetings'],
    },
    'n5-156': {
        'note': '〜ね/〜よ are sentence-final particles that CHANGE conversational tone. ね seeks agreement ("いいですね" = "isn\'t it nice?"). よ adds informational punch ("行きますよ" = "I\'m going, FYI"). Mixing them up creates rude or distant impressions. Native ears are very tuned to these.',
        'contexts': ['conversation', 'rapport'],
    },
    'n5-157': {
        'note': '〜でしょう (probably / right?) is the polite hedge — a forecast on TV ("明日は雨でしょう") or a soft confirmation seeker. Casual equivalent is でしょ / だろう. Tone of voice changes meaning: rising でしょう？ = "isn\'t it?"; flat でしょう = "probably."',
        'contexts': ['forecasting', 'soft_confirmation'],
    },
    'n5-168': {
        'note': '〜たり〜たり is the "for-example" list, NEVER a complete list. Saying "週末は本を読んだり、走ったりします" means "I do things like read and run" — leaving room for more. Listing everything with 〜て chain sounds exhaustive; たり is the natural conversational choice.',
        'contexts': ['conversation', 'casual_descriptions'],
    },
    'n5-170': {
        'note': '〜た+ほうがいい (should do) is a strong RECOMMENDATION, not a casual suggestion. Used by parents/teachers/doctors giving advice. Among equals, soften further with 〜たほうがいいかもしれません ("might be better").',
        'contexts': ['advice', 'instruction'],
    },
    'n5-171': {
        'note': '〜ない+ほうがいい (shouldn\'t do) has STRONG implications when delivered directly. Doctors prescribing ("お酒を飲まないほうがいいです"), parents warning. To deliver gently to peers, add ね or qualifications ("〜ないほうがいいと思いますけど").',
        'contexts': ['warning', 'health_advice'],
    },
    'n5-188': {
        'note': 'V+ことができます is the "formal/written" potential. Spoken Japanese strongly prefers the inflected potential form (食べられる) instead. Use ことができます in resumes, formal letters, and on capability-statement signs.',
        'contexts': ['resumes', 'formal_writing', 'signs'],
    },
    'n5-040': {
        'note': 'この/その/あの (this / that / over-there) is determined by physical/conversational PROXIMITY: この (near speaker), その (near listener / just mentioned), あの (far from both or shared memory). Misuse marks foreign speech immediately.',
        'contexts': ['describing_objects', 'conversation'],
    },
    'n5-014': {
        'note': 'これ/それ/あれ (this one / that one / over there) — same proximity rule as この/その/あの but standalone (no noun follows). あれ also indicates "the one we both remember" in conversation ("あの映画、覚えてる？").',
        'contexts': ['pointing', 'shared_memory'],
    },
    'n5-049': {
        'note': 'どれ/どの/どちら (which) — どちら is the POLITE version, common in restaurants ("どちらにしますか？" = "which will you have?"). どれ is neutral/casual. Both restrict to selection from a known set, unlike 何 (open question).',
        'contexts': ['service', 'choice_questions'],
    },
    'n5-050': {
        'note': 'どう/いかが (how) — いかが is the POLITE form. Service workers default to "いかがですか？" / "いかがでしょうか？"; friends use "どう？". Mismatching makes you sound condescending or stiff. いかが is also a polite OFFER ("お茶はいかがですか？" = "would you like tea?").',
        'contexts': ['service', 'offers'],
    },
    'n5-018': {
        'note': 'だれ/どなた (who) — どなた is POLITE and used in business/customer service ("どなた様ですか？"). だれ in formal contexts sounds rude. Reception desks and phone-greeting scripts default to どなた.',
        'contexts': ['business', 'reception', 'phone'],
    },
    'n5-023': {
        'note': 'か (sentence-final question marker) is dropped in casual speech, where rising intonation alone signals a question ("コーヒー飲む？" instead of "コーヒー飲みますか？"). Including か with rising intonation in casual speech can sound stiff or interrogating.',
        'contexts': ['casual_conversation'],
    },
    'n5-153': {
        'note': 'と (with / and) for accompanying agent: "友だちと行きます" = "I go with a friend." NOT used for "with a tool/instrument" — that\'s で. Common error: "ペンと書きました" (wrong) vs "ペンで書きました" (correct, "wrote with a pen").',
        'contexts': ['descriptions', 'tools_vs_companions'],
    },
}


def main() -> int:
    fp = ROOT / 'data' / 'grammar.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_cultural_callout_starter')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {p['id']: p for p in data['patterns']}

    n = 0
    for pid, callout in CALLOUTS.items():
        if pid not in by_id:
            print(f'  ! missing pattern: {pid}')
            continue
        p = by_id[pid]
        if p.get('cultural_callout'):
            print(f'  - skip (already filled): {pid}')
            continue
        p['cultural_callout'] = callout
        p['cultural_callout_provenance'] = 'llm_curated'
        n += 1

    print(f'\nAuthored cultural_callout on {n} patterns (top {len(CALLOUTS)} most-used).')
    print(f'Coverage: 0/178 -> {n}/178 ({100 * n // 178}%)')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
