# n5_vocab_whitelist.json - Design

---
**Document status:**
- Last verified against corpus: 2026-05-21
- Corpus version at verification: v1.15.5
- Maintenance: hand-updated; CI does not regenerate this README
---

This whitelist is the **hand-tuned canonical N5 vocab scope**, used by
CI for scope enforcement. The file was originally generated from
`KnowledgeBank/vocabulary_n5.md`, which was merged into
`docs/N5-syllabus-methodology.md` + `data/` on 2026-05-14 (along with
all other files under `KnowledgeBank/`, including the
`*_questions_n5.md` source files for the per-category paper sets).
The `KnowledgeBank/` directory was deleted as part of that merge.
Since the merge, the whitelist is hand-maintained as a flat token
list - no longer regenerated.

## Purpose

The whitelist serves as the **recognition allowlist** consumed by
`tools/lint_content.py` when checking that no out-of-N5-scope
vocabulary appears in user-facing content. A token in the whitelist
means "in-scope at N5"; a token absent from the whitelist triggers a
lint warning when it appears in user-facing content.

## Relationship to data/vocab.json

As of **2026-05-21 (v1.15.5)**, the whitelist and vocab.json are
**near-fully aligned**: 966 of 969 whitelist tokens (99.7 %) match
a `form` or `reading` value in some `vocab.json` entry.

  - **vocab.json**:  **995** structured catalog entries (form, reading,
                     gloss, section, pos, examples).
  - **whitelist**:    **969** unique form-tokens, 966 of which match
                     vocab.json (3 unmatched as of 2026-05-21:
                     `倍`, `国籍`, `週末` - see "Known mismatches" below).

The size difference (**995 entries vs 969 unique tokens, gap of 26**)
reflects entries-side multi-section homographs:

  - **24 forms appear in 2+ vocab.json entries** (cross-section
    homographs - same kana/kanji form but different POS / section /
    sense). Each duplicate contributes 1 surplus entry above the
    whitelist's once-only count.
  - Total cross-section entries: 50 entries across 24 forms
    (24 forms × 1 + 26 surplus = 50; alternative count: 50 entries
    minus 24 distinct forms = 26 surplus). **26 ✓** - math
    reconciles.

Examples of cross-section homographs (10 of 24):
  - `あつい` - 3 entries in section 31 (adjectives): hot / thick /
    sympathetic senses
  - `あの` - section 5 (demonstrative) + section 39 (filler/hesitation)
  - `いくつ` - section 6 (question word) + section 8 (native counter)
  - `いる` - section 28 (Group-2 verbs, "to need") + section 30
    (existence verbs, "to exist") - same form, different verbs
  - `おく` - section 7 (numbers, 億) + section 27 (Group-1 verbs,
    "to place")
  - `かい` - 2 entries in section 9 (counters: 回 vs 階)
  - `かぜ` - section 14 (nature, "wind") + section 37 (common nouns,
    "cold/illness")
  - `から` - section 34 (conjunction, "because") + section 35
    (particle, "from")
  - `が` - section 34 (conjunction, "but") + section 35 (particle,
    subject marker)
  - `かた` - section 1 (people, "person - honorific") + section 37
    (nouns, "way / method")

### Known mismatches (3, as of 2026-05-21)

These 3 whitelist tokens have no matching form/reading in vocab.json:

  - `倍` - counter suffix (e.g., 三倍 "triple"). Documented as FP-13
    in the audit-prompt false-positive catalog; treated as a multiplier
    suffix, not a noun-counter. Likely intentional whitelist-only
    inclusion for kanji-scope purposes without a standalone vocab.json
    entry.
  - `国籍` (こくせき, "nationality") - borderline N5/N4; appears in
    listening drill stems but never as a vocab.json entry.
  - `週末` (しゅうまつ, "weekend") - same shape: appears in
    reading/listening prose but not catalogued as a standalone entry.

The 3-token gap is **not drift** - these are deliberate kanji-scope
whitelist entries that don't need a vocab.json catalog row. Future
authoring may add them as full entries; until then, document them
here so the audit chain is clean.

## History

  - **Before v1.12.7**: vocab.json had 1003 entries; whitelist had
    40 tokens with no vocab.json match (split as 10 multi-form
    aliases + 30 recognition-only items). Documented as "intentional
    superset" in the original draft of this README.
  - **v1.12.8 (2026-05-04)**: closed most of the drift by authoring
    38 new vocab.json entries (29 standalone catalog entries + 9
    multi-form merge entries). Count went 1003 → 1041.
  - **v1.12.9 → v1.15.5 (May 2026 audit cycle)**: VOCAB-001..006
    cleanup batches removed nonsense template-generated entries +
    merged over-duplicated entries (BUG-018/019/024 dedup batches).
    Count went 1041 → 995.

## Consumers

  - `tools/lint_content.py` reads the whitelist as an allowlist for
    the vocab-scope check across the following user-facing data files:
    - `data/grammar.json` (178 patterns with examples)
    - `data/questions.json` (290 questions - bank source)
    - `data/papers/<cat>/paper-{1..7}.json` (per-category paper-pack
      files: bunpou / dokkai / goi / moji; 28 paper files total
      containing 402 paper-bound questions)
  - `tools/check_content_integrity.py` derives N5 scope from the
    whitelist's union with the kanji whitelist for various invariants
    (JA-13, JA-66, JA-99 etc.)

## Maintenance

  - **Adding a new word to N5 scope**: add the token directly to this
    JSON (must be sorted), add a structured entry to
    `data/vocab.json` (form, reading, gloss, section, pos, examples),
    and update CI invariants if needed. Document the addition in
    `docs/N5-syllabus-methodology.md` if it affects scope policy.
  - **Removing a deprecated form**: remove the token from this JSON
    and remove the corresponding `data/vocab.json` entry.

The whitelist is **hand-maintained** post-2026-05-14 (was a generated
artifact before).
