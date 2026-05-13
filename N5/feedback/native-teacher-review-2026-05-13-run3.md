# Native-Teacher Content Review — JLPT N5 corpus (run 3)

**Conducted:** 2026-05-13 (~6 hours after run 1)
**Persona:** Same as runs 1+2.
**Mode:** Re-audit after the opt-outs remediation commit (56ab850).
**Trigger:** Major content change since run 2 (V-2 readings migration, G-2 explanation cleanup, T-2 speaker heuristic refinement) qualifies as anti-pattern #23 trigger #1.

---

## Executive summary

**Approaching saturation but found 3 small residuals.** Two new cross-contaminated `meaning_ja` (n5-154, n5-106) that JA-71 still misses due to incidental kana overlap in the full meaning_ja text. Plus 5 unresolvable `see_also` targets from the G-2 cleanup (extracted from "(also indexed as X)" parentheticals where X was abstract like "Verb" / "Adjective + Noun"). Plus a small schema inconsistency where 3 listening items use M/F single-letter speaker tags instead of male/female.

All 3 closed in one commit.

---

## Findings

### R3-T1 (Medium) — 2 more cross-contaminated meaning_ja

- **n5-154** (もう + Verb-ました):
  Old meaning_ja: 「Noun + へ」で、行く ほうこうを いいます。「とうきょうへ 行きます」(「に」も つかえます)。
  This describes へ direction particle, not もう+ました.
  JA-71 missed it because the full meaning_ja contains 「も」 from 「に」も — the pattern's も coincidentally overlaps.

- **n5-106** (Noun + が ほしいです):
  Old meaning_ja: 「〜を ください」は ものを たのむ ときの ことばです。「水を ください」。
  This describes 〜をください (n5-149), not Noun+が+ほしいです.
  JA-71 missed it because the full meaning_ja contains です/が incidentally.

**Why this class keeps surfacing:** JA-71's character-overlap heuristic has fundamental limits. Single-character incidental overlap (も, が, で, etc.) is enough to pass the check, even when the meaning_ja is about a completely different rule. Tighter thresholds produce false positives on particle patterns. JA-71 catches the egregious systematic-misalignment class but not subtle 1-character coincidences — those require manual native review.

### R3-T2 (Low) — 5 unresolvable see_also targets

The G-2 cleanup extracted see_also targets from the "(also indexed as 'X' in another category)" parentheticals. For 5 entries, X was abstract / placeholder text:

- n5-045 → "なん / なに" (slash-separated reading variant, not a pattern marker)
- n5-098 → "〜" (empty placeholder)
- n5-136 → "Adjective + Noun" (abstract category, not a specific pattern)
- n5-162 → "Verb" (abstract category)
- n5-163 → "Verb" (abstract category)

Fix: drop the unresolvable see_also entries. The underlying explanations remain intact; only the structured cross-link is removed where it doesn't point anywhere specific.

### R3-T3 (Low) — listening speaker tag schema mismatch

3 listening items (n5.listen.048, .049, and one more) use single-letter `M` / `F` speaker tags from hand-authored dialogue items, while the T-2 refinement uses `male` / `female`. Schema inconsistency.

Fix: normalize all M → male, F → female. The hand-authored items keep their content; only the tag form changes.

---

## What is defensible

- All run-1 + run-2 fixes verified in place
- 0 broken vocab_id refs across 7113 grammar example → vocab cross-references
- 0 asymmetric lookalike pairs in kanji
- 0 reading passages missing questions / topic / paragraphs
- T-2's refined listening speaker tags produce diverse distribution (narrator + male + female + teacher + student in 3 items refined)
- CONTENT-LICENSE.md still has 2 mentions of native_reviewed — **this is correct** per the maintainer's stance: keep the internal §9 disclosure (for institutional readers), don't expose as UI badge

---

## Cross-run trend

| Run | Findings | HIGH | Status |
|---|---:|---:|---|
| 1 | 10 | 2 (V-1, G-1) | shipped commit 99feeba + 8367e10 |
| 2 | 3 | 0 | shipped commit fe8bb14 |
| 3 (this) | 3 | 0 | shipped this commit |

Findings are now **all polish-tier** (no HIGH). Each successive run produces fewer, smaller issues. The asymptote is around 2-4 polish items per run — JA-71's character-overlap heuristic has inherent limits + see_also/speaker normalization issues are emerging from the cleanup cascade.

**Per anti-pattern #23:** if a run-4 fires (next major content change), I expect 0-2 findings.

---

## Disclosure (unchanged)

Claude in native-teacher persona; no actual native-speaker review. Findings reflect what such a teacher would catch given standard JLPT pedagogy + schema-consistency conventions.
