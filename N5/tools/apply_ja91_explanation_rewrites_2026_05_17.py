"""Apply explanation_en rewrites to retire all 43 JA-91 baseline pairs (Phase B).

Strategy: rewrite the "deferring" side of each pair so the SequenceMatcher
similarity falls below the 0.85 JA-91 threshold. After this script, the
_ja91_baseline.json baseline_pairs array becomes empty and JA-91 enforces
its cross-pattern similarity invariant unconditionally on the current corpus.

Pair classes addressed:
  - DUPLICATE_PATTERN x8: rewrite the "re-introduction" pattern so it
    diverges from the canonical pattern in prose / framing / register.
    Both members retain their full coverage; only the surface text
    diverges enough to fall below the similarity threshold.
  - CROSS_REFERENCE x21: rewrite the deferring pattern to be a focused
    sub-scope entry that explicitly points to the parent. The parent
    keeps its full explanation; the deferrer becomes a sub-treatment.
  - ALTERNATIVE_VARIANT x12: rewrite BOTH members of each pair to focus
    on what's distinctive about each variant (register, syntactic frame,
    function nuance). Function-equivalent pairs stay function-equivalent;
    only the prose framing differs enough to drop below the threshold.
  - SUBSET x2: rewrite the subset member (n5-048) to a focused
    sub-scope entry pointing at the full kosoado-location series.

Run from N5/:
    python tools/apply_ja91_explanation_rewrites_2026_05_17.py
"""
from __future__ import annotations

import io
import json
import sys
import difflib
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_JSON = ROOT / "data" / "grammar.json"
BASELINE_JSON = ROOT / "data" / "_ja91_baseline.json"


# Pattern ID → new explanation_en. Authored 2026-05-17 Phase B.
REWRITES: dict[str, str] = {
    # ===== DUPLICATE_PATTERN deferrers =====
    "n5-115": (
        "When に attaches to a specific clock-time expression (7時に, "
        "9時はんに, 何時に), it pins the action to that instant. This is "
        "the TIME sub-use of the multi-purpose particle に — see n5-005 "
        "for the full breakdown including existence-location, "
        "destination, and recipient uses. With time, に attaches only "
        "to fixed points (clock-time, dates, weekdays — not generic "
        "time words like きょう or いま)."
    ),
    "n5-039": (
        "Re-introduction entry for the kosoado-pronoun set, parallel "
        "to n5-014. The four-way deixis system (こ near speaker / そ "
        "near listener / あ far from both / ど which) carries across "
        "pronouns, adjectival modifiers, and locations — this entry "
        "highlights the standalone-pronoun use; the adjectival "
        "counterpart appears at n5-015 / n5-040 and the locational "
        "counterpart at n5-016 / n5-041."
    ),
    "n5-040": (
        "Adjectival counterpart to the n5-014 pronoun series: paired "
        "with a following noun rather than standing alone. "
        "Re-introduced in the kosoado-paradigm sequence as the "
        "modifier-form sibling of n5-015. Same こ/そ/あ/ど four-way "
        "deixis applies; the noun is obligatory, no particle "
        "intervenes between modifier and noun."
    ),
    "n5-041": (
        "Locational counterpart to the kosoado-pronoun set, parallel "
        "to n5-016. While n5-014 / n5-039 cover object pronouns, this "
        "entry pairs with location particles (に, で, から, まで). The "
        "どこ member also takes question-word が to form 'where is X?' "
        "queries; see n5-048 for どこ in isolation as a question-word."
    ),
    "n5-045": (
        "Re-introduction of the question word for things, parallel to "
        "n5-017. The dual reading なに/なん is conditioned by the "
        "following sound: なん before です / ですか / でしょう and most "
        "counters (なんじ, なんにん); なに before particles を / が / も / "
        "は. Pair with question particle か at sentence end."
    ),
    "n5-046": (
        "Re-introduction of the question word for people, parallel to "
        "n5-018. The register split is the key point: だれ is the "
        "everyday form; どなた elevates the register for strangers, "
        "customers, and formal contexts. Like other wh-words at N5, "
        "takes が (never は) when asking about new information."
    ),
    "n5-114": (
        "Time-axis instance of the paired range marker from n5-021. "
        "The same から (starting point) + まで (ending point) frame "
        "applies, with the example set narrowed to clock-time, dates, "
        "and durations (e.g., 9時から 5時まで). The non-time uses — "
        "distances, places, sequences of items — sit at the parent "
        "entry n5-021."
    ),
    "n5-029": (
        "Re-presentation of the noun-linking particle の (canonical "
        "entry: n5-028). This entry frames の under its three roles "
        "individually — possession (わたしの = 'mine'), classification "
        "(日本語の しんぶん = 'Japanese newspaper'), and apposition / "
        "modification — for learners studying the noun-modifier system "
        "in isolation."
    ),

    # ===== CROSS_REFERENCE deferrers =====
    "n5-137": (
        "The noun-linking particle の treated under the Nominalization "
        "category. Same surface form as n5-028 (possessive / "
        "noun-modifier); listed here because the resulting 'X の Y' "
        "phrase functions as a noun unit. See n5-028 for the full "
        "role breakdown; this entry's scope is the noun-phrase-"
        "building function specifically."
    ),
    "n5-109": (
        "Counter-question vocabulary set: いくつ (how many, native "
        "ひと-counter), いくら (how much, money / quantity), なんにん "
        "(how many people), なんまい (how many flat objects), なんぼん "
        "(how many cylindrical), なんさつ (how many books), なんかい "
        "(how many times), and friends. Each question matches its "
        "target's counter class — choose by what's being counted. "
        "n5-054 covers いくつ in isolation."
    ),
    "n5-136": (
        "Combined-category entry for adjective-noun modification. "
        "Covers both い-adjective + noun (adjective placed directly, "
        "no particle, keep the い: 高い 山) and な-adjective + noun "
        "(linker な required: しずかな まち). See n5-078 for the "
        "い-adjective sub-rule and n5-084 for the な-adjective "
        "sub-rule with the obligatory な linker."
    ),
    "n5-161": (
        "Noun-frame instance of まえ ('before'): noun + の + まえ(に). "
        "Parent entry n5-119 covers both noun-frame and verb-frame "
        "uses; this entry isolates the noun-frame for syllabus "
        "sequencing. The trailing に is the time-locative particle "
        "(n5-005 / n5-115) attaching to the まえ phrase as a whole."
    ),
    "n5-162": (
        "Verb-frame instance of まえ ('before'): verb-plain (NON-PAST) "
        "+ まえに. The verb stays NON-PAST even when describing past "
        "'before doing X' — this is the key trip-up vs the English "
        "'before [past]'. Parent entry n5-119 covers both frames; "
        "n5-161 is the parallel noun-frame entry."
    ),
    "n5-160": (
        "Noun-frame instance of あと ('after'): noun + の + あとで. "
        "Parent entry n5-120 lists both frames; this entry isolates "
        "the noun-frame. The で is the means / time particle marking "
        "'doing X after Y' — semantically distinct from まえに's に."
    ),
    "n5-163": (
        "Verb-frame instance of あと ('after'): verb-PAST (た-form) + "
        "あとで. The PAST verb-form is obligatory here, mirror-image "
        "of まえに's NON-PAST requirement. Parent entry n5-120; the "
        "noun-frame sibling is n5-160."
    ),
    "n5-155": (
        "Mid-sentence clause connector が — see n5-126 for the "
        "function. This entry highlights the WRITING convention: a "
        "comma typically follows the clause containing が "
        "(X です が、 Y). The softening tone makes it gentler than "
        "でも at clause-start, which is why dialogue and personal "
        "narrative favor mid-sentence が over でも."
    ),
    "n5-184": (
        "Indefinite-thing instance of the parent rule at n5-183. "
        "なにか = 'something' (positive context, indefinite reference); "
        "なにも = 'nothing' (always paired with negative predicate; "
        "なにも たべません = 'I don't eat anything'). The か→indefinite, "
        "も→universal-or-negative mapping is consistent across the "
        "kosoado family."
    ),
    "n5-185": (
        "Indefinite-person instance of the parent rule at n5-183. "
        "だれか = 'someone' (positive context); だれも = 'no one' "
        "(negative predicate required; だれも きません = 'no one "
        "comes'). Note: with positive predicate, だれも is rare in "
        "modern usage — the 'everyone' sense often goes to みんな "
        "instead."
    ),
    "n5-186": (
        "Indefinite-place instance of the parent rule at n5-183. "
        "どこか = 'somewhere'; どこも + negative = 'nowhere' (どこにも "
        "いきません). The locative particle (に, で) often surfaces "
        "between どこ and も in negative contexts — どこにも instead "
        "of just どこも."
    ),
    "n5-187": (
        "Indefinite-time instance of the parent rule at n5-183, with "
        "a register twist: いつか = 'someday / sometime'; いつも = "
        "'always' (POSITIVE universal, not paired with negation like "
        "なにも / だれも). This is the one member of the family where "
        "+も + positive predicate is the dominant usage."
    ),

    # ===== SUBSET (n5-048 → n5-016 / n5-041) =====
    "n5-048": (
        "The 'where' member of the kosoado-location series, isolated "
        "for question-word indexing. Full series treatment at n5-016 "
        "/ n5-041. どこ takes the same particles as the statement "
        "forms ここ / そこ / あそこ (に, で, から, まで) and pairs with "
        "sentence-final か to form 'where' questions."
    ),

    # ===== ALTERNATIVE_VARIANT (function-equivalent pairs; rewrite both) =====
    "n5-023": (
        "Sentence-final か turns any sentence into a question — works "
        "equally with yes / no (これは ほんですか) and wh-frames "
        "(なにを たべますか). The written convention omits the question "
        "mark in standard Japanese (か itself does the job). The "
        "mid-sentence Aか Bか 'A or B' use lives at the sibling entry "
        "n5-024."
    ),
    "n5-024": (
        "Mid-sentence か connects nouns or noun phrases as 'X or Y': "
        "コーヒーか おちゃ (coffee or tea), 月よう日か 火よう日 "
        "(Monday or Tuesday). The か's are typically placed after "
        "EACH alternative (Aか Bか), though dropping the final か in "
        "casual speech is common. Sentence-final か (the question "
        "particle) is the sibling entry n5-023."
    ),
    "n5-060": (
        "Polite affirmative past: ます → ました. The ま base stays; "
        "only the suffix changes. たべました = 'ate'; いきました = "
        "'went'. This is the polite-register counterpart to plain "
        "past V-た (e.g., たべた); the negative counterpart is the "
        "sibling entry n5-061."
    ),
    "n5-061": (
        "Polite negative past: ます → ませんでした. Three morphemes "
        "stack — ません (polite negative) + でした (was). たべません"
        "でした = 'did not eat'. Learners often shorten incorrectly "
        "to ませんだ — the でした segment is fixed and obligatory. "
        "Affirmative sibling: n5-060."
    ),
    "n5-156": (
        "Paired sentence-final particles ね and よ presented together "
        "in the Other Core Patterns category. ね (canonical n5-025) "
        "seeks agreement; よ (n5-026 sibling) informs the listener of "
        "new info. Together they cover speaker-listener stance "
        "management. See the canonical entries for register and tone "
        "details."
    ),
    "n5-159": (
        "Polite-register version of the ね / よ pair: stack the "
        "particle after です rather than directly on a plain-form "
        "predicate. Function is unchanged from n5-025 / n5-026 — "
        "confirmation (ね) and assertion (よ) — but the です-prefix "
        "raises the register to match the rest of the polite-speech "
        "context."
    ),
    "n5-157": (
        "Polite-register probability marker — 'probably', 'I suppose', "
        "or seeking light agreement ('right?'). Attaches to plain-form "
        "predicates: あした 雨でしょう, おもしろいでしょう. The intonation "
        "distinguishes assertion (falling) from confirmation (rising). "
        "Casual / plain register counterpart: だろう (n5-158)."
    ),
    "n5-158": (
        "Plain-register counterpart of でしょう (n5-157): same "
        "probability / mild assertion sense, dropped formality. "
        "Speech-typical, less common in writing where でしょう "
        "dominates. Contracts further in very casual speech to だろ. "
        "The compound past たろう ('it must have been') also derives "
        "from this base."
    ),
    "n5-173": (
        "Obligation expression at the formal-spoken register: "
        "negative-て + は + いけない, literally 'not doing won't do', "
        "idiomatically 'must do'. Common in news broadcasts, lectures, "
        "and polite directives. Stacks with な-adj and noun via the "
        "じゃ negative chain: しずかじゃ なくては いけない = 'must be "
        "quiet'. Variants at n5-174 (formal-written) / n5-175 "
        "(conditional-frame) / n5-176 (casual contraction)."
    ),
    "n5-174": (
        "Formal-written register variant of the obligation paradigm. "
        "Negative-て + は + ならない, literally 'not doing won't become "
        "(acceptable)', idiomatically 'must do'. Dominant in legal "
        "text, government notices, written instructions. Spoken-"
        "register counterpart: n5-173 (いけない); conditional-frame: "
        "n5-175; casual contractions: n5-176."
    ),
    "n5-175": (
        "Conditional-frame variant of the obligation paradigm: plain "
        "negative + と + いけない, literally 'if you don't do, won't "
        "do'. The と here is the conditional connective. Slightly "
        "more conversational than the なくては frames (n5-173 / "
        "n5-174). All four — n5-173, n5-174, n5-175, n5-176 — express "
        "identical functional meaning at different register or "
        "syntactic frames."
    ),
    "n5-176": (
        "Casual contractions of the obligation expression: なくては → "
        "なくちゃ; なければ → なきゃ. The trailing いけない / ならない is "
        "OFTEN dropped, so the contraction alone (たべなくちゃ, いか"
        "なきゃ) carries the full 'must' meaning. Highly informal — "
        "friend-to-friend and inner-monologue speech only. Formal "
        "counterparts: n5-173 / n5-174 / n5-175."
    ),
}


def main() -> int:
    g = json.loads(GRAMMAR_JSON.read_text(encoding="utf-8"))
    by_pid = {p.get("id"): p for p in g.get("patterns") or []}
    n_applied = 0
    n_skipped = 0
    for pid, new_text in REWRITES.items():
        p = by_pid.get(pid)
        if not p:
            print(f"  SKIP {pid}: pattern not found")
            n_skipped += 1
            continue
        old = p.get("explanation_en", "")
        p["explanation_en"] = new_text
        n_applied += 1
        print(f"  {pid}: {len(old)} -> {len(new_text)} chars")
    GRAMMAR_JSON.write_text(
        json.dumps(g, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nApplied {n_applied} rewrites; skipped {n_skipped}.")

    # Verify all baseline pairs now fall below 0.85
    g2 = json.loads(GRAMMAR_JSON.read_text(encoding="utf-8"))
    by_pid2 = {p.get("id"): p.get("explanation_en", "")
               for p in g2.get("patterns") or []}
    bl = json.loads(BASELINE_JSON.read_text(encoding="utf-8"))
    still_above = []
    for entry in bl.get("baseline_pairs") or []:
        pair = entry.get("pair") or []
        if len(pair) != 2:
            continue
        a, b = pair
        ta = by_pid2.get(a, "")
        tb = by_pid2.get(b, "")
        if not ta or not tb:
            continue
        r = difflib.SequenceMatcher(None, ta, tb, autojunk=False).ratio()
        if r >= 0.85:
            still_above.append((a, b, r, entry.get("class")))
    if still_above:
        print(f"\nStill above 0.85 threshold: {len(still_above)} pairs:")
        for a, b, r, cls in still_above:
            print(f"  {a}/{b}: {r:.3f} ({cls})")
    else:
        print(f"\nAll {len(bl.get('baseline_pairs') or [])} baseline pairs "
              f"now fall below 0.85 — JA-91 can run unconditionally.")

    # Also check for NEW pairs that may have crossed threshold during
    # rewriting (false-positive risk from rewriting toward similar text)
    patterns = [(p.get("id"), p.get("explanation_en", ""))
                for p in g2.get("patterns") or []
                if isinstance(p.get("explanation_en"), str)
                and p.get("explanation_en", "").strip()]
    new_hits = []
    baseline_set = set(
        frozenset(e.get("pair") or []) for e in bl.get("baseline_pairs") or []
    )
    for i in range(len(patterns)):
        for j in range(i + 1, len(patterns)):
            id_i, ti = patterns[i]
            id_j, tj = patterns[j]
            sm = difflib.SequenceMatcher(None, ti, tj, autojunk=False)
            if sm.quick_ratio() < 0.85 or sm.real_quick_ratio() < 0.85:
                continue
            r = sm.ratio()
            if r >= 0.85 and frozenset([id_i, id_j]) not in baseline_set:
                new_hits.append((id_i, id_j, r))
    if new_hits:
        print(f"\nNEW pairs that cross 0.85 (not in old baseline): "
              f"{len(new_hits)}:")
        for a, b, r in new_hits:
            print(f"  {a}/{b}: {r:.3f}")
        print("  These must be re-authored or added to baseline.")
    else:
        print("\nNo NEW pairs crossed 0.85 — rewrites are clean.")

    # Empty the baseline if all pairs resolved AND no new pairs
    if not still_above and not new_hits:
        n_prior = len(bl.get("baseline_pairs") or [])
        bl["baseline_pairs"] = []
        if "_audit_summary" in bl and isinstance(bl["_audit_summary"], dict):
            bl["_audit_summary"]["total_pairs_at_or_above_threshold"] = 0
            bl["_audit_summary"]["classification_counts"] = {
                "DUPLICATE_PATTERN": 0,
                "CROSS_REFERENCE": 0,
                "ALTERNATIVE_VARIANT": 0,
                "SUBSET": 0,
            }
            bl["_audit_summary"]["next_review_trigger"] = (
                "RESOLVED 2026-05-17 (Phase B): all 43 prior baseline pairs "
                "addressed via explanation_en rewrites on the deferring "
                "(or both, for ALTERNATIVE_VARIANT) sides. JA-91 now "
                "enforces cross-pattern similarity unconditionally on the "
                "current corpus."
            )
        if "_meta" in bl and isinstance(bl["_meta"], dict):
            bl["_meta"]["purpose"] = (
                "Baseline allowlist for JA-91 (cross-pattern explanation_en "
                "similarity ≥ 0.85 Levenshtein). RESOLVED 2026-05-17 "
                "(Phase B) — all 43 prior baseline pairs addressed via "
                "explanation_en rewrites. JA-91 enforces the threshold "
                "unconditionally; baseline_pairs is empty and serves as a "
                "RESOLVED snapshot."
            )
            bl["_meta"]["resolution_date"] = "2026-05-17"
        BASELINE_JSON.write_text(
            json.dumps(bl, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        print(f"\nEmptied {BASELINE_JSON.name}: {n_prior} -> 0 baseline_pairs")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
