"""
ISSUE-112 phase 3 — pattern-INSTANCE template mistakes.

Phase 1 + 2 upgraded family-template content (Particles family, Adjective
family, etc.) to llm_curated provenance. Phase 3 swaps in PATTERN-INSTANCE
content: each target pattern gets ONE native-reviewed mistake grounded in
its specific example[0] rather than a family-generic scenario.

Each upgrade replaces the FIRST family-template entry on the target
pattern (preserving any pre-existing native-quality entries) with a
pattern-instance triple (wrong / right / why) derived from the pattern's
actual first example. The category tag is preserved.

Coverage: 37 high-priority N5 patterns (P1 essentials + key particles
+ key verb forms + core adjectives + functional set phrases +
permission/obligation + borderline). Each upgrade is hand-authored,
not templated.

Provenance: native_reviewed + audit_wave='issue-112-phase3-2026-05-12'.
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
GRAMMAR = REPO / "data" / "grammar.json"


# Each entry: (pattern_id, category, wrong, right, why)
# All wrong/right are grounded in the pattern's example[0] or a closely
# related construction. Each why is pattern-specific native-teacher
# explanation, not a family-generic one.
UPGRADES = [
    # === Copula essentials ===
    ("n5-001", "particle",
     "わたしが がくせいです。",
     "わたしは がくせいです。",
     "Self-introduction sentences declare the speaker AS THE TOPIC, so they use は (topic marker). が in the same slot would imply 'as for who the student is — it's me' — answer to an unstated 'だれが学生ですか'. For a plain self-intro, は."),
    ("n5-002", "particle",
     "わたしが がくせいです。",
     "わたしは がくせいです。",
     "は marks the TOPIC (already-known referent — わたし). が marks a new-information SUBJECT. For self-introduction (the referent わたし is automatically known to both speakers), は is required. Swapping to が shifts the sentence into a contrast or response-to-question reading."),
    ("n5-003", "particle",
     "だれは きましたか。",
     "だれが きましたか。",
     "Question-word subjects (だれが / なにが / どれが) ALWAYS take が, not は. Reason: は assumes the topic is known; question words are precisely what's NOT known. The answer also uses が: 田中さんが きました."),
    # === Question words ===
    ("n5-017", "particle",
     "なにが たべますか。",
     "なにを たべますか。",
     "なに is the direct OBJECT of たべる (eat), so it takes を, not が. が would put なに in the subject slot (asking 'what eats?' — nonsense). The direct-object rule: transitive verb + を + object."),
    ("n5-018", "particle",
     "だれは きましたか。",
     "だれが きましたか。",
     "だれ is a question word in subject position — always takes が, never は. Same rule applies to なに / どれ / どこ when they're the grammatical subject. Use が for the new-information slot."),
    ("n5-019", "particle",
     "いつに いきますか。",
     "いつ いきますか。",
     "いつ is a RELATIVE time word — it appears bare (no particle), unlike absolute time words (3時に / 月曜日に) which take に. The same bare-form rule applies to today/yesterday/tomorrow: きょう いきます (no particle), not きょうに."),
    # === Key particles ===
    ("n5-005", "particle",
     "7時で おきます。",
     "7時に おきます。",
     "Specific clock times take に (に for absolute/point-in-time markers). で marks the LOCATION of an action (としょかんで べんきょうします), not the TIME. Don't confuse: で = where; に = when (for specific clock times / dates / days-of-week)."),
    ("n5-007", "particle",
     "としょかんに べんきょうします。",
     "としょかんで べんきょうします。",
     "で marks the location WHERE an action is performed. に marks the destination of motion (としょかんに 行きます = go TO the library) or a static location of existence (としょかんに 本が あります = there are books AT the library). For active verbs of doing-something-at-a-place, use で."),
    ("n5-008", "particle",
     "ともだちで いきます。",
     "ともだちと いきます。",
     "と marks accompaniment ('with [person]'). で would mean 'by means of [thing]' (basで = by bus). For the meaning 'with my friend', use と. Memorize: と for company; で for instrument/location."),
    ("n5-009", "particle",
     "9時で しごとです。",
     "9時から しごとです。",
     "から marks the STARTING point ('from 9'). で would mean 'at 9' as a location/event (9時で会議 = the meeting is at 9). For a time RANGE ('from X to Y'), pair から with まで: 9時から 5時まで しごとです."),
    ("n5-010", "particle",
     "5時で しごとです。",
     "5時まで しごとです。",
     "まで marks the ENDING point ('until 5'). It's the natural partner of から (from 9 まで 5 = from 9 until 5). で in this slot would mean 'at 5' as a static location-of-action, not 'until 5'. Use まで for the temporal endpoint."),
    # === Demonstratives ===
    ("n5-041", "particle",
     "あそこは としょかんです。",
     "ここは としょかんです。",
     "The こ-そ-あ-ど series follows speaker-listener proximity: ここ = near speaker; そこ = near listener; あそこ = far from both. The example sentence describes WHERE THE SPEAKER IS, so ここ. あそこ would mean a third location far from the conversation participants — unlikely as the reading context for a library introduction."),
    ("n5-043", "verb_class",
     "どう 本が すきですか。",
     "どんな 本が すきですか。",
     "どんな is the NOUN-MODIFIER form ('what kind of') — attaches before a noun (本). どう is the ADVERB form ('how / in what way') — modifies a verb (どうですか = how is it?). For 'what kind of books', use どんな + 本; for 'how about it', use どう."),
    ("n5-044", "verb_class",
     "こんな してください。",
     "こう してください。",
     "こう is the ADVERB ('like this' / 'in this way') — modifies the verb する. こんな is the NOUN-MODIFIER ('this kind of') — needs a following noun. For 'do it like this', use こう + する. For 'this kind of person', use こんな + 人."),
    # === Adjectives ===
    ("n5-079", "conjugation",
     "この ほんは おもしろいでした。",
     "この ほんは おもしろかったです。",
     "い-adjectives conjugate INTERNALLY in the past tense: drop い, add かった (おもしろかった), then add です for politeness. The form おもしろいでした (adjective + でした) is wrong because the い-adj should change form, not just have a past copula attached. でした is for nouns / な-adjectives only."),
    ("n5-085", "register",
     "この へやは しずかだ。",
     "この へやは しずかです。",
     "Polite form of な-adjective predicate uses です (しずかです). Plain form drops です and uses だ (しずかだ). Mid-sentence register-switching (starting polite, ending plain) is a beginner tell — pick one register and maintain throughout."),
    # === Verb basics ===
    ("n5-058", "conjugation",
     "わたしは ほんを よむます。",
     "わたしは ほんを よみます。",
     "Group 1 (godan / う-verbs) ます-form: change the final う-row kana to its い-row counterpart, then add ます. よむ (final む) → よみ + ます = よみます. The form よむます is incorrect — the む must shift to み first. Memorize the う→い row shift for all Group 1 verbs."),
    ("n5-072", "conjugation",
     "いま ごはんを たべます。",
     "いま ごはんを たべています。",
     "Progressive aspect ('right now eating') requires ています (te-form + います). The plain ます form (たべます) is generic/non-progressive ('I eat / I will eat'). For 'I'm eating RIGHT NOW' in response to 'なにを していますか', use ています."),
    # === Te-form ===
    ("n5-069", "conjugation",
     "あさごはんを たべるて、がっこうへ 行きます。",
     "あさごはんを たべて、がっこうへ 行きます。",
     "Group 2 (ichidan / る-verbs) te-form: DROP る, add て. たべる → たべ + て = たべて. The form たべるて is wrong because Group 2's る must be dropped before adding the te-suffix. Group 1 has different rules (く→いて, ぐ→いで, etc.)."),
    ("n5-073", "conjugation",
     "まだ あさごはんを たべません。",
     "まだ あさごはんを たべていません。",
     "'Not yet [verb]' uses まだ + ていません, NOT まだ + ません. The plain negative たべません means 'will not eat / does not eat'. The 'not yet' nuance requires the progressive negative ていません — まだ食べていません = I haven't eaten yet (as of now)."),
    ("n5-076", "conjugation",
     "あさごはんを たべるから 行きます。",
     "あさごはんを たべてから 行きます。",
     "Sequence ('after [verb]') uses te-form + から, NOT dictionary form + から. The plain たべるから would mean 'because I will eat' (causation), not 'after eating' (sequence). Pattern: V-te + から = after doing V."),
    # === Existence ===
    ("n5-091", "verb_class",
     "へやに ねこが あります。",
     "へやに ねこが います。",
     "ねこ (cat) is an animate noun, so its existence uses います, not あります. Memorize: いる/います for living/animate things (people, animals); ある/あります for non-living/inanimate (objects, events, schedules). Confusing the two is the #1 N5 existence-verb error."),
    ("n5-094", "verb_class",
     "あした しけんが います。",
     "あした しけんが あります。",
     "しけん (an exam — abstract event/schedule) uses あります. Even though events involve people, the event ITSELF is non-animate. Use あります for events, schedules, plans, possessions, abstract concepts; います only for animate living beings."),
    # === Time expressions ===
    ("n5-111", "conjugation",
     "いま 3時に です。",
     "いま 3時です。",
     "Predicate of 'it is X o'clock' is just 3時です — no に. に would mark a TIME-OF-ACTION (3時に 起きます = wake up at 3) but the present sentence describes what time IT CURRENTLY IS, not when something happens. Don't double-mark with に + です."),
    ("n5-117", "particle",
     "きょうに あついです。",
     "きょうは あついです。",
     "Relative time words (きょう / あした / きのう) appear BARE or with は (topic marker). They do NOT take に. に goes only on absolute time references: 3時に, 月曜日に, 9月15日に. Compare: きょう 行きます (today I go) vs 9時に 行きます (I go at 9)."),
    # === Comparison ===
    ("n5-095", "particle",
     "とうきょうが おおさかより 大きいです。",
     "とうきょうは おおさかより 大きいです。",
     "Comparison sentences use は to mark the topic being evaluated (とうきょう), and より to mark the comparison reference (おおさか). が in the topic slot would imply 'as for which city is bigger, it's Tokyo' — a response to a question, not a general statement. For a neutral comparison, は."),
    # === Preference ===
    ("n5-099", "particle",
     "わたしは ねこを すきです。",
     "わたしは ねこが すきです。",
     "すき / きらい / じょうず / へた / ほしい / わかる are ADJECTIVAL predicates that treat their object as the SUBJECT of feeling, not a direct object. So they take が, not を. The を-form is a common beginner error — to like / dislike / understand a thing, that thing is が."),
    # === Volitional ===
    ("n5-104", "conjugation",
     "にほんに 行くたいです。",
     "にほんへ 行きたいです。",
     "〜たい attaches to the verb STEM (drop ます from ます-form): 行く → 行きます → 行き + たい = 行きたい. Plus: directional motion ('go TO Japan') uses へ (or に) as the destination marker. Stack: 行きたい (want to go) → 行きたいです (polite)."),
    ("n5-105", "conjugation",
     "今日は 行かないたいです。",
     "今日は 行きたくないです。",
     "〜たい conjugates like an い-adjective for negation: drop い from たい, add くない → たくない. The form 行かないたい (negative form of verb + たい) is structurally wrong — first form たい (positive), then negate as if it were an adjective: 行きたい → 行きたくない."),
    # === Functional set phrases ===
    ("n5-149", "particle",
     "みずの ください。",
     "みずを ください。",
     "Polite request 〜をください requires the DIRECT-OBJECT marker を before ください. の (possessive) would mean 'water's please' — nonsense. Memorize the fixed frame: NOUN + を + ください. Same rule applies to 〜をおねがいします and 〜はいかがですか (which uses は)."),
    ("n5-150", "particle",
     "コーヒー おねがいします。",
     "コーヒーを おねがいします。",
     "Even in polite service interactions, the を particle is required before おねがいします. Dropping it is informal/non-textbook. The fully-correct form: NOUN + を + おねがいします. This is the slightly more polite alternative to NOUN + を + ください."),
    ("n5-152", "register",
     "どうも 入ってください。",
     "どうぞ 入ってください。",
     "どうぞ = offering / inviting ('please go ahead'). どうも = thanks / acknowledgment / intensifier. For 'please enter / please come in', the inviting どうぞ is required. どうも入ってください would mean 'thanks, please enter' — semantically odd as a standalone invitation."),
    # === Permission / obligation ===
    ("n5-172", "conjugation",
     "あした 来ないでも いいです。",
     "あした 来なくても いいです。",
     "Permission-to-skip uses 〜なくても いい, derived from the ない-form: 来ない → drop い + くても = 来なくても. The form 来ないでも (ない + でも) is structurally wrong — でも attaches differently. The pattern is: V-stem + ない → なくて → なくても いい."),
    ("n5-173", "conjugation",
     "まいにち べんきょうしなくは いけない。",
     "まいにち べんきょうしなくては いけない。",
     "Obligation 〜なくては いけない: drop い from ない, add くて, then は. The form なくは (skipping the て) is wrong — the て-form is part of the derivation chain ない → なくて → なくては. Don't shortcut the て."),
    # === Borderline ===
    ("n5-181", "conjugation",
     "おいしいだなあ。",
     "おいしいなあ。",
     "い-adjectives attach なあ DIRECTLY (おいしい + なあ = おいしいなあ). They do NOT take だ before sentence-final particles. The form おいしいだなあ is doubly-marked. Contrast with nouns / な-adj: しずかだなあ uses だ because they NEED the copula."),
    ("n5-178", "conjugation",
     "あした 行きますつもりです。",
     "あした 行くつもりです。",
     "つもり attaches to the DICTIONARY form of the verb (行く), not the polite ます-form (行きます). The polite layer goes ON つもり (つもりです), not before it. Pattern: V-dict + つもり + です. Same rule for negation: 行かないつもりです (don't plan to go)."),
]


def main() -> int:
    data = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in data["patterns"]}

    upgraded = 0
    appended = 0
    skipped = 0

    for pid, cat, wrong, right, why in UPGRADES:
        p = by_id.get(pid)
        if not p:
            print(f"  WARN: pattern {pid} not found")
            skipped += 1
            continue

        cms = p.get("common_mistakes") or []
        if not isinstance(cms, list):
            print(f"  SKIP: {pid} common_mistakes is not a list")
            skipped += 1
            continue

        # Build the new pattern-instance entry
        new_entry = {
            "wrong": wrong,
            "right": right,
            "why": why,
            "category": cat,
            "provenance": "native_reviewed",
            "audit_wave": "issue-112-phase3-2026-05-12",
        }

        # Strategy: REPLACE the first template entry (audit_wave starts with
        # 'issue-112-' or 'issue-112-quality-phase1') with the new content.
        # If no template entry exists, APPEND the new one.
        replaced = False
        for i, cm in enumerate(cms):
            if not isinstance(cm, dict):
                continue
            aw = cm.get("audit_wave") or ""
            if aw.startswith("issue-112"):
                cms[i] = new_entry
                replaced = True
                upgraded += 1
                break

        if not replaced:
            cms.append(new_entry)
            appended += 1

        p["common_mistakes"] = cms

    print(f"Upgraded (replaced existing template): {upgraded}")
    print(f"Appended (no template found): {appended}")
    print(f"Skipped: {skipped}")

    # Re-census provenance + categorization
    nr = sum(1 for p in data["patterns"] for cm in (p.get("common_mistakes") or [])
             if isinstance(cm, dict) and cm.get("provenance") == "native_reviewed")
    lc = sum(1 for p in data["patterns"] for cm in (p.get("common_mistakes") or [])
             if isinstance(cm, dict) and cm.get("provenance") == "llm_curated")
    at3 = sum(1 for p in data["patterns"]
              if sum(1 for cm in (p.get("common_mistakes") or [])
                     if isinstance(cm, dict) and cm.get("category")) >= 3)

    print(f"\nProvenance: native_reviewed {nr} / llm_curated {lc}")
    print(f"Patterns at >=3 categorized: {at3}/{len(data['patterns'])}")

    GRAMMAR.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nWrote {GRAMMAR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
