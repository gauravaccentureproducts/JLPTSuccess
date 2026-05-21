# N5 kanji whitelist - exception register

---
**Document status:**
- Last verified against corpus: 2026-05-21
- Corpus version at verification: v1.15.5
- Maintenance: hand-updated; CI does not regenerate this README
---

Each line below documents a kanji that is in the project whitelist
(`n5_kanji_whitelist.json`) but not in the project's reference scope
(`data/n5_official_kanji_scope.json` - a consensus reconstruction of
N5 kanji scope, ~100-103 characters, derived from major textbooks
(Genki, Minna no Nihongo) and analysis of pre-2010 旧4級 lists and
post-2010 official sample materials, since JLPT.jp no longer
publishes specific kanji lists post the 2010 test-format reform). Required
for any exception:

- The kanji glyph
- WHY: a one-sentence reason
- REVIEW_DATE (optional): ISO 8601 date for re-evaluation
  (`YYYY-MM-DD` format only; CI invariant JA-144 will reject other formats
  once wired). Omit the field if no review is planned.

The integrity check `JA-25` (Pass-22 F-22.4) enforces this contract:
every kanji in the project whitelist that is not in
`data/n5_official_kanji_scope.json` must have a corresponding entry
below with a `WHY:` justification.

This file may be empty during bootstrapping. Once
`data/n5_official_kanji_scope.json` is populated with the consensus list,
JA-25 begins enforcing accountability for the deltas.

## Authority note (added 2026-05-21)

The "103 kanji" figure circulates widely in third-party study
materials (WaniKani, Tofugu, Genki, "first 103 kanji" flashcard
decks), and matches the **pre-2010 旧4級 (Old level 4)** published
list. It is NOT a current canonical figure from JLPT.jp. JLPT.jp's
own FAQ (https://www.jlpt.jp/sp/e/faq/) explicitly states:

> "Therefore, we decided that publishing 'Test Content Specifications'
> containing a list of vocabulary, kanji and grammar items was not
> necessarily appropriate. As information to replace [...] 'Summary of
> Linguistic Competence Required for Each Level' and 'Composition of
> test items' are available."

So the actual scope boundary for N5 today is a consensus reconstruction,
not an authoritative published list. The project treats ~100-103 as a
range estimate and reconciles via `data/n5_official_kanji_scope.json`
(when populated; currently bootstrapping per "Bootstrapping exit
criteria" below).

## Exceptions

(none currently documented - JA-25 is in bootstrapping mode until the
official-scope reference file is added at
`data/n5_official_kanji_scope.json`)

<!--
Format (one block per exception). The 3 required lines are: the H3 heading
with the glyph, the WHY line, and (optionally) the REVIEW_DATE line.

  ### 妹
  - WHY: appears as recognition-only distractor in moji-4.12 (Q57) per
    moji-corpus kanji-scope exception (Mondai 2 distractors may use
    non-whitelist kanji for family-relation tests).
  - REVIEW_DATE: 2026-08-01

  ### 供
  - WHY: appears in 子供 spelling variant of こども; documented in
    moji-5.2 rationale as N5-policy-excluded alternative spelling.
    The 子供 distractor was replaced with 子分 on 2026-05-21 (MOJI-004
    close-out) so 供 is no longer in any user-facing field; this row
    documents the historical use for audit-trail purposes.
  - REVIEW_DATE: 2026-07-15

These two examples (妹 from moji-4.12, 供 from moji-5.2) are
self-documenting evidence of the policy applied in practice - both are
real cases in the corpus history. Uncomment them only if they re-enter
the active whitelist.
-->

## Bootstrapping exit criteria (added 2026-05-21)

JA-25 leaves bootstrapping mode when ALL of:

1. `data/n5_official_kanji_scope.json` is committed, containing the
   consensus N5 kanji list (target: ~100-103 entries; sources:
   intersection of Genki I-II vocab kanji + Minna no Nihongo Shokyu
   1-2 kanji + pre-2010 旧4級 list + cross-check against published
   N5 sample papers from 2010 onwards).
2. Owner reviews the `n5_kanji_whitelist.json` delta vs the scope file
   and adds WHY entries here for every superset kanji.
3. CI begins running JA-25 in enforce mode (currently no-op).

**Target**: v1.16.0 or whenever the next major content review lands.
**Owner**: project author (Gaurav Srivastava per spec §27 Stakeholders).
**Estimated effort**: ~2-3 hours (consensus-build from 3 textbook
sources + N5 sample paper kanji extraction + delta review).

## Notes

- Spec: `specifications/procedure-manual-appendix-c-pass22-polish.md` §C.4.
- Per-level files: when an N4 / N3 / N2 / N1 build adds its own whitelist,
  it gets its own `n<L>_kanji_whitelist.exceptions.md` following the
  same format (including the Document status header convention above).
- Do NOT silence violations by adding kanji here without a WHY. The
  whole point of the WHY-comment is accountability; an undocumented
  addition defeats the invariant.
- REVIEW_DATE format: ISO 8601 (`YYYY-MM-DD`) only. CI invariant
  JA-144 (wired 2026-05-21 alongside this README revision) enforces
  the format with regex `^- REVIEW_DATE: \d{4}-\d{2}-\d{2}$`. Other
  date shapes ("Q3 2026", "next release", "August 2026") are rejected
  to prevent downstream parsing fragility.
