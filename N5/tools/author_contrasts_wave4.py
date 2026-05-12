"""
ISSUE-118 — Author contrast cross-links wave 4.

Pre-wave state (2026-05-12): 121/178 patterns with >=1 contrast.
57 patterns have zero contrasts.

This wave authors 30+ pattern pairs based on natural N5 pedagogical
groupings (time expressions, question-word families, particle dual-
functions, register pairs, etc.). Each PAIR yields 2 contrast entries
(bidirectional) when both patterns are in the missing-set; if the
partner already has contrasts, only the single-direction entry is
added (per existing-data mixed convention).

Target: bring 121 -> ~150 patterns with >=1 contrast. The remaining
~30 patterns (n5-030, n5-038, n5-107, n5-177, n5-180, plus a few
others) genuinely lack natural N5 partners and will remain terminal
per the audit's note that "some patterns lack natural N5 partners".

Notes are 1-2 sentences, native-teacher voice. Each note targets the
SPECIFIC distinction a learner needs (not generic glosses).
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
GRAMMAR = REPO / "data" / "grammar.json"

# Each tuple: (source_pattern_id, target_pattern_id, note)
# A pair like (A, B, ...) + (B, A, ...) is bidirectional.
CONTRASTS = [
    # === Question-word family ===
    ("n5-018", "n5-017", "だれ/どなた asks about PEOPLE; 何（なに/なん）asks about THINGS. どなた is the polite form of だれ — use it in formal contexts."),
    ("n5-017", "n5-018", "何 asks about things; だれ asks about people. Both take は or が depending on focus."),
    ("n5-019", "n5-055", "いつ asks for general time (day, year, occasion); なんじ asks for the specific clock time. Don't use なんじ when the question is about a date or general period."),
    ("n5-055", "n5-019", "なんじ asks for the clock hour specifically; いつ is the general 'when' for any time period."),
    ("n5-055", "n5-056", "なんじ asks the clock time; なんようび asks the day of the week. Both are answered with specific time-unit nouns."),
    ("n5-056", "n5-055", "なんようび asks the day-of-week; なんじ asks the clock time."),
    ("n5-056", "n5-057", "なんようび asks the day-of-week (月曜日, 火曜日...); なんがつなんにち asks the calendar month-and-day (3月15日)."),
    ("n5-057", "n5-056", "なんがつなんにち asks for the calendar date; なんようび asks for the day-of-week label."),
    ("n5-052", "n5-053", "どうやって asks the MANNER (how something is done); いくら asks the AMOUNT (how much / what price). Different question categories despite both being 'how' in English."),
    ("n5-053", "n5-052", "いくら asks the amount or price; どうやって asks the manner. Use どのぐらい for general quantity / duration / distance."),
    ("n5-183", "n5-017", "Question-word + か forms an INDEFINITE pronoun (だれか someone, 何か something); the bare question word asks an actual question."),

    # === Particle dual-functions ===
    ("n5-028", "n5-031", "〜の as a possessive links two nouns (わたしの本 = my book). The SAME particle 〜の also nominalizes verbs/sentences (走るのが好き). Same particle, two distinct grammatical jobs."),
    ("n5-031", "n5-028", "〜の as a nominalizer turns a verb/clause into a noun-equivalent (たべるのは楽しい). The same 〜の elsewhere is a possessive/genitive link between two nouns."),
    ("n5-031", "n5-030", "〜の nominalizer (たべるの) is the more colloquial form; こと in basic nominalizer use (たべること) is the more formal/written form. Many contexts allow either."),

    # === Demonstratives ===
    ("n5-043", "n5-044", "こんな/そんな/あんな/どんな + Noun (こんな本 = this kind of book) — describes a TYPE of thing. こう/そう/ああ/どう is the ADVERB form (こうする = do it like this) — describes a manner of action."),
    ("n5-044", "n5-043", "こう/そう/ああ/どう modifies a VERB (こう書く = write like this). こんな/そんな/あんな/どんな + Noun modifies a NOUN (こんな人 = this kind of person)."),

    # === Time-counter family ===
    ("n5-111", "n5-112", "〜じ counts hours on the clock (3時 = 3:00); 〜ふん/ぷん counts minutes (15分 = 15 minutes / quarter past). Combine: 3時15分 = 3:15."),
    ("n5-112", "n5-113", "〜ふん/ぷん gives explicit minutes (30分); 〜じはん is the contracted form meaning 'half past the hour' (3時はん = 3:30). Native speakers prefer はん over 30分 in casual speech."),
    ("n5-113", "n5-112", "〜じはん = exactly 'X-thirty'; 〜ふん/ぷん gives any minute count. はん replaces 30分 only at the half-hour."),

    # === Time expressions ===
    ("n5-116", "n5-117", "毎日/毎週/毎月/毎年 marks RECURRING time intervals (every day, every week...); 今日/あした/きのう refers to SPECIFIC calendar days. Pair them: 毎日、今日は…"),
    ("n5-117", "n5-118", "今日/あした/きのう = specific calendar days (today, tomorrow, yesterday). 今/すぐ/もう/まだ = aspect adverbs (now, soon, already, still). Use 今 when speaking about THIS moment, 今日 about today's entire span."),
    ("n5-118", "n5-154", "今/すぐ/もう/まだ are time-aspect adverbs that PRECEDE verbs (もう食べました = I already ate). もう + V-ました explicitly combines もう with the past-perfect, the highest-frequency もう pattern."),
    ("n5-154", "n5-118", "もう + V-ました = 'already done X' (完了 perfect aspect). The same もう also pairs with まだ/もうすぐ in n5-118 to mark non-completion or imminence."),

    # === Existence + possession ===
    ("n5-094", "n5-092", "〜があります = a thing exists / I have an inanimate thing. The fuller pattern 〜に〜があります specifies WHERE the existence holds (テーブルに本があります). Use 〜があります when location is implied or already known."),
    ("n5-107", "n5-092", "Verb-stem + に + 行きます/来ます/かえります = 'go to do X' (purpose-of-motion). Contrast with 〜に〜があります which uses に to mark LOCATION rather than purpose."),

    # === Preference & ability ===
    ("n5-099", "n5-100", "〜がすき/きらい expresses PREFERENCE / emotional liking (映画が好きです). 〜がじょうず/へた expresses SKILL or ability level (テニスがじょうずです). Both use が, but the predicate semantic class differs."),
    ("n5-100", "n5-099", "〜がじょうず/へた = skill-level adjective. 〜がすき/きらい = preference adjective. Both take が rather than を because the adjective treats the noun as object-of-feeling, not direct object of an action."),
    ("n5-102", "n5-103", "〜がわかります = 'understand X' (cognitive comprehension). 〜ができます = 'can do X' (potential / ability). Different meanings; わかります is mental, できます is performative."),
    ("n5-103", "n5-188", "〜ができます takes a NOUN (日本語ができます = can speak Japanese). V-dictionary + ことができます takes a VERB (話すことができます = can speak). Use the V-form when the ability is about doing a specific action."),
    ("n5-188", "n5-103", "V-dictionary + ことができます explicitly says 'be able to do [verb]'. The simpler 〜ができます uses a noun. Both express potential but differ in syntactic input."),

    # === Frequency adverbs ===
    ("n5-147", "n5-148", "よく/ときどき/あまり/ぜんぜん describes frequency QUANTITY: often / sometimes / not much / never. いつも/たいてい/たまに describes frequency PROPORTION: always / usually / occasionally. The two sets overlap pragmatically; いつも is highest, ぜんぜん is lowest."),
    ("n5-148", "n5-147", "いつも/たいてい/たまに sits on the 'always-rare' axis. よく/ときどき/あまり/ぜんぜん sits on the 'often-never' axis. Native usage often combines: たいていよく eats out = 'usually often eats out'."),

    # === Request register ladder ===
    ("n5-149", "n5-150", "〜をください is the standard polite request ('please give me X'). 〜をおねがいします is slightly MORE polite / formal — often used in restaurants and customer-service contexts. Genki teaches them as near-synonyms."),
    ("n5-150", "n5-149", "〜をおねがいします is more deferential than 〜をください — use it when asking for service (お水をおねがいします in a restaurant). 〜をください works for any polite request."),
    ("n5-150", "n5-151", "〜をおねがいします is a REQUEST ('I'd like X please'). 〜はいかがですか is an OFFER ('How about X / would you like X?'). The first is for the customer; the second is what the staff says."),

    # === Conjunctions ===
    ("n5-122", "n5-124", "それから = sequential connector ('and then', 'after that'). しかし = adversative connector ('but', 'however'). Don't substitute one for the other — different discourse functions."),
    ("n5-124", "n5-122", "しかし introduces CONTRAST; それから introduces SEQUENCE. しかし is more formal than でも; both express 'but' but しかし fits written/announcement contexts."),

    # === Change-of-state vs deliberate choice ===
    ("n5-142", "n5-143", "〜にします = the speaker DELIBERATELY chooses/decides (コーヒーにします = I'll have coffee). 〜になります = something CHANGES STATE naturally (寒くなります = it becomes cold). Different agency: にします is volitional, になります is descriptive."),
    ("n5-143", "n5-142", "〜になります describes a change happening (春になりました = spring has come). 〜にします is the speaker's act of selecting (これにします = I'll go with this one)."),

    # === Quotation register ===
    ("n5-145", "n5-146", "〜とおもいます = 'I THINK X' (speaker's opinion / hedged statement). 〜と言いました = 'X SAID' (reporting someone else's words). Same particle と but different speech-acts."),
    ("n5-146", "n5-145", "〜と言いました reports speech literally ('they said X'). 〜とおもいます reports the speaker's own opinion. The と marks quoted/thought content in both."),
    ("n5-145", "n5-178", "〜とおもいます = 'I think (probably) X' (speaker's belief). 〜つもりだ = 'I intend to X' (speaker's plan/resolve). Belief vs intention — don't conflate."),
    ("n5-178", "n5-145", "〜つもりだ commits to a future action ('I plan to'). 〜とおもいます softens an opinion ('I think...'). Native speakers use つもり for plans and とおもう for guesses."),
    ("n5-146", "n5-179", "〜と言いました is the POLITE quotation form. 〜って is the CASUAL contraction of と言って/と言う — heard in conversation but not formal writing. Same content, different register."),
    ("n5-179", "n5-146", "〜って is the casual/colloquial quotation form. 〜と言いました is the polite explicit form. Use って with friends, と言いました in reports/exams."),
    ("n5-157", "n5-145", "〜でしょう conveys probability/conjecture often with rising intonation seeking agreement (明日は雨でしょう = It'll probably rain tomorrow, right?). 〜とおもいます is the speaker's INTERNAL opinion (明日は雨だとおもいます). でしょう invites listener confirmation; とおもいます doesn't."),

    # === Honorific noun-prefix ===
    ("n5-164", "n5-165", "〜さん is the standard person-suffix (田中さん). お〜/ご〜 is the noun-prefix that adds politeness to objects (お水, ご家族). Different scope: 〜さん attaches to names, お〜 attaches to common nouns."),
    ("n5-165", "n5-164", "お〜 (wago nouns) / ご〜 (kango nouns) prefix adds politeness to nouns. 〜さん attaches to people's names. Both elevate register but target different word classes."),

    # === Permission vs obligation ===
    ("n5-172", "n5-173", "〜なくてもいい = 'don't have to do X' (PERMISSION to skip). 〜なくてはいけない = 'must do X / can't skip X' (OBLIGATION). Direct logical opposites — beware swapping them."),
    ("n5-173", "n5-172", "〜なくてはいけない = OBLIGATION ('I have to'). 〜なくてもいい = no obligation ('I don't have to'). The ない-stem branches into 'must' vs 'don't need to'."),

    # === Functional set phrases ===
    ("n5-152", "n5-166", "どうぞ/どうも/すみません/おねがいします are flexible courtesy openers/closers. The greeting-set (いただきます/ごちそうさま/おはようございます) are FIXED ritual phrases tied to specific situations (meals, time of day)."),
    ("n5-166", "n5-152", "Greetings (いただきます etc.) are RITUAL set phrases — they only fit their specific occasion. どうぞ/どうも/すみません are flexible courtesy markers used across many contexts."),

    # === Sentence-final particles ===
    ("n5-181", "n5-182", "〜なあ is an EXCLAMATORY sentence-final particle (きれいだなあ = how pretty!). The SAME な on V-plain forms a PROHIBITIVE (行くな = don't go!). Different syntactic environments: exclamation after copula/adjective vs imperative after verb-dictionary."),
    ("n5-182", "n5-181", "V-dictionary + な is a strong CASUAL prohibitive ('don't!') — male-coded, often considered rough. 〜なあ ending an adjective/copula sentence is an emotional exclamation, register-neutral."),

    # === Adjective + Noun, relative clause ===
    ("n5-078", "n5-079", "い-Adjective + Noun directly modifies (大きい家 = a big house). い-Adjective + です ends a sentence with a predicate adjective (家は大きいです = the house is big). Same adjective, modifier-position vs predicate-position."),
    ("n5-135", "n5-084", "V-plain + Noun is a relative clause (食べる人 = a person who eats). な-Adjective + な + Noun is a noun-modifier (きれいな人 = a beautiful person). Both modify nouns but using different word-class syntax."),

    # === Counter family ===
    ("n5-108", "n5-038", "Number + counter (1冊/3個/2人) names a quantity. ずつ ('each') adds DISTRIBUTIVE meaning: 一つずつ = 'one each'. Use ずつ when each member of a group gets the same amount."),
    ("n5-038", "n5-108", "ずつ is the DISTRIBUTIVE marker that follows a number-counter to mean 'each' (二人ずつ = two each). Plain Number + counter has no distributive nuance."),

    # === Copula + topic ===
    ("n5-001", "n5-002", "〜です / 〜ます is the polite-form predicate ending. The topic-marker は usually pairs with です in introductory sentences (わたしは学生です). The two patterns work together — topic + polite predicate."),

    # === Excess and manner ===
    ("n5-177", "n5-079", "Verb-stem / Adj-stem + すぎる means 'too much / excessive' (食べすぎる = eat too much; 大きすぎる = too big). For い-adjectives, drop the い before adding すぎる (大きい → 大きすぎる)."),
    ("n5-180", "n5-058", "Verb-stem + 〜かた = 'way / method of doing' (たべかた = way of eating). Same stem extraction as the 〜ます form: drop ます from V-ます, append かた."),
]


def main() -> int:
    data = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in data["patterns"]}

    added = 0
    skipped_duplicate = 0
    missing_target = 0
    coverage_before = sum(1 for p in data["patterns"] if p.get("contrasts"))

    for src_id, tgt_id, note in CONTRASTS:
        src = by_id.get(src_id)
        if not src:
            print(f"  SOURCE MISSING: {src_id}")
            continue
        if tgt_id not in by_id:
            print(f"  TARGET MISSING: {src_id} -> {tgt_id}")
            missing_target += 1
            continue
        existing = src.get("contrasts") or []
        # Avoid duplicates
        if any(c.get("with_pattern_id") == tgt_id for c in existing):
            skipped_duplicate += 1
            continue
        existing.append({
            "with_pattern_id": tgt_id,
            "note": note,
            "provenance": "llm_curated",
            "audit_wave": "issue-118-wave4-2026-05-12",
        })
        src["contrasts"] = existing
        added += 1

    coverage_after = sum(1 for p in data["patterns"] if p.get("contrasts"))
    print(f"\nAdded: {added}")
    print(f"Skipped (duplicate): {skipped_duplicate}")
    print(f"Skipped (target missing): {missing_target}")
    print(f"Coverage: {coverage_before}/{len(data['patterns'])} -> {coverage_after}/{len(data['patterns'])}")

    GRAMMAR.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Wrote {GRAMMAR}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
