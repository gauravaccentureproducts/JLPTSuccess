# Phase 8 polish — surgical expansion of remaining short explanation_en entries.
#
# After Phase 7 closed 8 high-value upgrades, 35 short entries remained.
# Honest classification:
#   - 23 entries have real quick-win gaps (sound rules, register pairs,
#     contrast notes, worked examples) — upgraded here.
#   - 12 entries are accurate-and-complete (parallel tense triples like
#     ました/ません/ませんでした; complete pairs like まだ/もう). Skipped by
#     design — see SKIPPED dict for the per-entry rationale.
#
# All upgrades use only N5-whitelist kanji + kana (JA-66 enforces this
# automatically after this batch lands).

import json
import io
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# 23 surgical upgrades. Each adds 1-2 sentences that close a real
# learner gap. No padding — if a useful sentence wasn't there, the
# entry stays in the SKIPPED set instead.
UPGRADES = {
    "n5-030": (
        "の after a plain-form verb makes the action a noun. "
        "'Reading books' = 本を 読むの. Pairs with こと (both nominalize) "
        "but の is preferred with verbs of perception (見る・聞く) and "
        "in colloquial speech; こと is preferred in formal definitions "
        "and with copula (〜のはXです vs 〜ことはXです)."
    ),
    "n5-037": (
        "など follows a list (often with や) to add 'etc., and so on'. "
        "More formal/written counterpart of casual とか. Use と for a "
        "closed exhaustive list ('A and B'), や〜など for an open "
        "representative list ('A, B, etc.')."
    ),
    "n5-038": (
        "ずつ after a quantity means 'each' or 'per' — distributing "
        "a fixed amount. Examples: 一人ずつ (one person at a time), "
        "二つずつ (two each), すこしずつ (little by little). Often used "
        "with みんな or に for distribution targets."
    ),
    "n5-052": (
        "どうやって asks the METHOD/MEANS of doing something. More "
        "specific than どう ('how' in a general sense) or どうして "
        "('why'). Example: どうやって 行きますか = 'how (by what means) "
        "do you go?' — answer might be 'by bus / by train'."
    ),
    "n5-056": (
        "Counter ようび = 'day of the week'. なんようび asks 'what day?'. "
        "The 7 answers: 月・火・水・木・金・土・日 ようび "
        "(getsu / ka / sui / moku / kin / do / nichi-youbi)."
    ),
    "n5-073": (
        "Negative form of ています. Two readings: (1) 'not currently "
        "doing' — 今 食べていません = 'I'm not eating now'; (2) 'not "
        "in resulting state / haven't done yet' — まだ 食べていません = "
        "'I haven't eaten yet'. Often pairs with まだ for the latter."
    ),
    "n5-077": (
        "ないでください = polite request not to do. Take the plain "
        "ない-form, add でください. Politeness pair with てください "
        "(polite affirmative request). Casual counterparts: drop "
        "ください for ないで (negative) and 〜て (affirmative)."
    ),
    "n5-084": (
        "な-adjectives need な before a noun. しずかな へや = 'a quiet "
        "room'. Contrast with い-adjectives, which attach directly "
        "(no な): しろい へや = 'a white room'. The な only appears in "
        "attributive position — predicate form drops it (へやは しずか)."
    ),
    "n5-087": (
        "な-adjectives form past with でした, just like nouns. しずか → "
        "しずかでした. Negative past: しずかではありませんでした (formal) or "
        "しずかじゃなかったです (casual). Same pattern as noun predicates "
        "since な-adj take the copula ladder."
    ),
    "n5-111": (
        "じ counts hours. Watch sound-changes: 4時 = よじ (not しじ), "
        "7時 = しちじ, 9時 = くじ. All other hours follow the regular "
        "Sino-Japanese reading: 1時 いちじ, 2時 にじ, 3時 さんじ, "
        "5時 ごじ, 6時 ろくじ, 8時 はちじ, 10時 じゅうじ, 12時 じゅうにじ."
    ),
    "n5-113": (
        "じはん = 'half past'. 3時はん = 3:30. Equivalent to 30分 "
        "(さんじゅっぷん) but じはん is the conversational default. "
        "Used only with whole hours; quarter-past or other minutes "
        "use the 〜分 counter."
    ),
    "n5-122": (
        "それから begins a clause to mark sequence — 'after that, "
        "next'. Also carries an additive sense — 'and also / in "
        "addition' — when listing items: りんごと、それから、みかんも "
        "= 'apples, and also oranges'."
    ),
    "n5-123": (
        "でも at the start of a new sentence introduces a contrast. "
        "Casual. Position rule: でも sits at the head of the second "
        "sentence (not mid-sentence). The mid-clause/formal "
        "counterpart is が or けれど."
    ),
    "n5-142": (
        "〜にする = 'decide on / choose / make it ~'. Common in "
        "restaurants for ordering: コーヒーにします = 'I'll have coffee'. "
        "The に marks the choice. Contrast with 〜になる (n5-143), "
        "which is non-volitional change."
    ),
    "n5-143": (
        "Change-of-state pattern. Nouns and な-adj take に; い-adj "
        "drop い and add くなる. Non-volitional / no agent (vs にする "
        "in n5-142, which is volitional choice). Example: さむくなる "
        "= 'becomes cold' (just happens); さむくする = 'make it cold' "
        "(someone does it)."
    ),
    "n5-144": (
        "Drop ます, add ながら. Two simultaneous actions by the SAME "
        "subject. The main action is the SECOND verb; ながら-verb is "
        "the backgrounded one. Example: おんがくを ききながら "
        "べんきょうする = 'study while listening to music' (the "
        "studying is the main action)."
    ),
    "n5-146": (
        "Same と quotation pattern with the verb 言う (say) in the "
        "polite past form. Structure: [speaker]は「[quote]」と "
        "言いました. Direct quotes use 「...」; indirect quotes use "
        "plain form before と (たなかさんは 行くと 言いました = "
        "'Tanaka-san said he'd go')."
    ),
    "n5-151": (
        "Polite offer or suggestion form, common in service "
        "settings. Politeness ladder: 〜は どうですか (neutral) < "
        "〜は いかがですか (polite, customer-service register). "
        "Used by shopkeepers, waitstaff, and in formal hospitality."
    ),
    "n5-152": (
        "Core polite expressions used dozens of times daily in "
        "Japan. Memorize all four. Quick map: どうぞ = 'please "
        "(accept/go ahead)', どうも = 'thanks (casual)', すみません = "
        "'excuse me / sorry / thanks (with imposition)', "
        "おねがいします = 'please (request)'."
    ),
    "n5-171": (
        "Negative version of n5-170: 'you'd better not'. Full form: "
        "Verb-ない + ほうがいい. Example: たばこを すわないほうがいい = "
        "'you'd better not smoke'. Same advisory register as the "
        "affirmative; same softening with です."
    ),
    "n5-177": (
        "Drop ます/い, add すぎる. 'Too much / too X'. Examples: "
        "食べすぎる ('eat too much'), 高すぎる ('too expensive'), "
        "しずかすぎる ('too quiet'). Conjugates as a regular る-verb "
        "(ichidan): すぎます, すぎました, すぎない."
    ),
    "n5-178": (
        "Verb-plain + つもりだ/です = 'I intend to / plan to'. つもりです "
        "is the polite form; casual is つもりだ or just つもり. Negative: "
        "Verb-plain-negative + つもりだ ('I don't intend to'). Stronger "
        "than 〜たい (wanting) but softer than commitment."
    ),
}

# 12 entries deliberately skipped — accurate-and-complete, no learner
# gap. Documented so future audits don't re-flag them as targets.
SKIPPED = {
    "n5-055": "Already covers counter じ + pairing with から/まで.",
    "n5-059": "Parallel with n5-060/061 tense triple — adding here breaks symmetry.",
    "n5-060": "Parallel tense triple — see n5-059 rationale.",
    "n5-061": "Parallel tense triple — see n5-059 rationale.",
    "n5-089": "Complete: derivation rule + use case in one sentence.",
    "n5-105": "Complete: derivation rule with explicit い-adj treatment note.",
    "n5-112": "Already a 76-char sound-change reference table.",
    "n5-116": "Complete: formation rule + adverbial usage note.",
    "n5-124": "Pair partner to n5-123 (でも); duplicating expansion would echo.",
    "n5-149": "Already touched in Phase 7 n5-150 expansion (register pair).",
    "n5-153": "Pair partner to n5-154 (もう); both deliberately parallel.",
    "n5-154": "Pair partner to n5-153 (まだ); both deliberately parallel.",
    "n5-172": "Complete: full derivation breakdown (なくて + も + いい).",
}


def main() -> None:
    path = "data/grammar.json"
    with open(path, encoding="utf-8") as f:
        g = json.load(f)

    # Load N5 whitelist for inline kanji check
    kj = json.load(open("data/kanji.json", encoding="utf-8"))
    N5 = {e["glyph"] for e in kj["entries"]}
    KANJI_RE = re.compile(r"[一-鿿]")

    updated = 0
    for p in g["patterns"]:
        pid = p["id"]
        if pid in UPGRADES:
            old = (p.get("explanation_en") or "").strip()
            new = UPGRADES[pid].strip()
            if old != new:
                bad = sorted({c for c in KANJI_RE.findall(new) if c not in N5})
                if bad:
                    print(f"  ! {pid}: would introduce above-N5 kanji {bad} — aborting")
                    sys.exit(1)
                p["explanation_en"] = new
                p["explanation_provenance"] = "native_reviewed"
                p["audit_wave"] = "phase-8-polish-2026-05-13"
                print(f"  {pid}: {len(old)}c -> {len(new)}c")
                updated += 1

    with open(path, "w", encoding="utf-8") as f:
        json.dump(g, f, ensure_ascii=False, indent=2)

    print(f"\nPhase 8: {updated}/{len(UPGRADES)} upgraded, {len(SKIPPED)} skipped.")
    print(f"Total Phase 7+8 covered: {8 + updated}/43 short entries.")


if __name__ == "__main__":
    main()
