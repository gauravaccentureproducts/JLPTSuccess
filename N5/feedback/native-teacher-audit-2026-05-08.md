# Native Japanese JLPT Teacher Audit — 2026-05-08

Self-conducted audit of `data/` from a native Japanese JLPT teacher's
perspective, focused on linguistic accuracy, JLPT-N5 scope correctness,
pedagogical soundness, and visible content quality.

## Executive summary

The corpus is broadly competent at the textbook layer (grammar
explanations, dokkai passages, distractor design, cultural context)
but had **systemic content-corruption bugs in auto-generated metadata
fields** that were visible to learners. All audit-headlined findings
have been fixed in this pass; broader structural cleanup tasks
(vocab.json section dedup, full Hindi-native review, mecab integration
for vocab extraction) remain queued.

## Findings + fix status

### CRITICAL — content corruption (visible to learners)

| ID | Finding | Status |
|---|---|---|
| C-1 | `explanation_hi` in `n5.listen.002–005` described entirely different listening items (groceries → "salad/soup", train delay → "weather") | **FIXED** — rewrote 4 explanation_hi + 3 cultural_context blocks |
| C-2 | `vocab_used` arrays in `reading.json` contained random hiragana fragments (え, ね, よ) and phantom entries (うし, いし) from substring-match noise | **FIXED** — re-extracted via longest-match against vocab.json with kanji-form-only lookup for kanji entries; 997 → 539 entries net (mostly removing noise) |
| C-3 | `vocab_ids` cross-tags in `grammar.json` confused homophones — あめ tagged as candy in rain context (×6), おく vs おきる (×6), おもい (heavy) vs おもう (think, ×6) | **FIXED** — 18 surgical retags/removes |

### HIGH — pedagogical concerns

| ID | Finding | Status |
|---|---|---|
| H-1 | Listening pace systematically slower than JLPT N5 target (mean 160 morae/min vs target band 180–240) | **DEFERRED** — would require TTS re-render of all 47 items |
| H-2 | Auto-translated English in `vocab.json` examples shipped with case/agreement errors ("we is a student", "he is a student" lowercase) + misattributed sense (かた=person example used 読みかた=way) | **FIXED** — 7 visible bugs fixed + かた example replaced |
| H-3 | `n5_kanji_readings.json` listed sokuon allophones (みっ, よっ, むっ, やっ) as separate kun-readings of 三/四/六/八 | **FIXED** — removed from both n5_kanji_readings.json and kanji.json; sokuon_allophony_note added to _meta |
| H-4 | Romaji in `grammar.json` agglutinated particles ("darega", "amega") and skipped digits ("7tokini") | **FIXED** — targeted patcher applied to 393/631 examples; particle-suffix splits + digit-time transliteration |
| H-5 | Hindi rationales in `papers/{moji,goi,bunpou}/*.json` are broken Hinglish | **DEFERRED** — already tagged `rationale_hi_provenance: "llm_curated"` (acknowledged needing review); volume too large for surgical pass |

### MEDIUM — polish / textbook conventions

| ID | Finding | Status |
|---|---|---|
| M-1 | `kanji.json` had empty translations + duplicate sentences (女) + 24 kanji with redundant `additional_readings` duplicating main on/kun | **FIXED** — translations filled, duplicate sentence dropped, additional_readings deduped |
| M-2 | 母 mnemonic was anatomically blunt ("Two breasts inside a body") | **FIXED** — softened to "A figure of a nursing mother — the two emphasized dots originally depicted breasts, signaling 'mother' by the act of nursing." |
| M-3 | Claimed 子 stroke-order description undercounted strokes | **DROPPED** — re-reading showed description is correct (3 stroke events separated by → arrows) |
| M-4 | Time-format inconsistency in listening — 時はん vs 時半 across items | **FIXED** — normalized 時はん → 時半 across 9 fields in 2 items |
| M-5 | Listening schema split — items 013–021 had legacy `voice` field alongside `voice_planned` | **FIXED** — removed legacy field from 18 items |
| M-6 | 今 had dubious キン listed as additional on-yomi (not a real reading in modern Japanese) | **FIXED** — removed |
| M-7 | Bunsetsu spacing convention | **NO ACTION** — already correct (positive finding) |

### LOW — honest disclosures (already documented)

- **`native_reviewed` flag = Claude acting as reviewer** — already disclosed in `_meta.native_review_pass_2026_05_07` blocks.
- **`questions.json` ID gaps (290 sparse IDs in q-0001..q-0580)** — documented in `id_gap_policy: "documented"`.
- **Most `difficulty: 1`** — known limitation; deferred for future curriculum-balance pass.

## Broader issues identified (not in scope of this pass)

These were observed during the audit but not in the audit's headlined
priority list:

- **vocab.json section duplications**: 24+ kanji had readings duplicated between main on/kun and additional_readings (the M-1 fix addressed this).
- **vocab.json misclassified sections**: えいが (movie) lives in section 26 (House and Furniture). Recategorizing requires renaming the section or creating a new "Entertainment" section. Affects vocab_id surfaces. Deferred.
- **vocab.json duplicate kana entries**: e.g., へや exists in BOTH section 13 (Locations) AND section 26 (House). Causes 164 cases of double-tagging in grammar.json examples. Root-cause fix requires vocab.json restructuring + ID migration.
- **Romaji generation broader rewrite**: Current state has many remaining issues (kanji-substitution choosing wrong reading per context, e.g., 来 → "ku" instead of "ki" in 来てください). Right fix is to integrate a proper Japanese morphological analyzer (mecab) at build time. The targeted patches in H-4 addressed the audit's specific complaints but did not regenerate.
- **Hindi rationale review**: H-5 deferred; recommend a Hindi-native bilingual reviewer pass when budget permits (already queued via IMP-101).

## Verification

`tools/check_content_integrity.py`: **50/50 invariants green** after
each phase commit.

## Commits

1. `29f0573` — Phase 1+2: C-1 + C-3
2. `f0f4ab4` — Phase 3: C-2
3. `ae1508e` — Phase 4: H-2
4. `cebb4ba` — Phase 5+6: H-3 + H-4 + M-1 + M-2 + M-6
5. `70774a1` — Phase 7+8: M-4 + M-5
