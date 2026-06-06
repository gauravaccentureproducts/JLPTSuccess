# JLPT N5 — Vocabulary Native-Review Cycle Coverage (2026-06-04)

This document records the 2026-06-04 vocabulary native-review remediation
cycle (batches A–J) driven by two consolidated native-Japanese / JLPT
expert review reports plus a specific-bug audit, against the 995-entry
`data/vocab.json` corpus of JLPTSuccess release v1.17.37→v1.17.39.

**Writing-discipline note.** Counts below are bounded by *what was scanned*
(the vocab corpus snapshot on 2026-06-04 + the 180 CI invariants at this
checkpoint) and *how it was matched* (the per-batch heuristics named). A
later native-human per-entry pass may reclassify individual entries. The
phrase "fixed" means "the cited/systematic defect was corrected and, where
deterministic, CI-locked"; it does NOT mean "the entry is native-verified
complete" — see the corpus-level disclosure
`_meta.native_human_review_status_2026_06_04` (PENDING).

---

## Cycle scope

- Surface: `data/vocab.json` (995 entries), its SPA renderer
  (`js/learn-vocab.js`), and the reviewer-facing docx at
  `docs/vocab-review/`.
- Triggers: two consolidated native-reviewer reports (broad issue-class
  reviews) + a specific-bug audit citing 12 concrete JP-content errors.
- Approach: each reviewer issue-class became a batch (A–J). Deterministic
  / clearly-confirmed items were fixed and (where a regression class
  existed) CI-locked; sense-judgment items were either allowlist-handled
  or deferred to the native queue (BUG-263).

---

## Batch ledger

| Batch | Class | Entries | Disposition |
|-------|-------|--------:|-------------|
| A | Sense de-contamination (かた polite-person particle_examples) | 1 | Fixed (BUG-262) |
| B | Homonym cross-references (false_friends / same-form pragmatic) | 27 | Fixed (BUG-262) |
| C | Counter cleanup (家族 / 両親 collective nouns) | 2 | Fixed (BUG-262) |
| D | Family pragmatic notes (uchi/soto + address-form) | 15 | Fixed (BUG-262) |
| E | Particle-example corpus-wide naturalness re-audit | ~589 flagged | **OPEN** (BUG-263, native judgment) |
| F | Section-level fixes (legacy / disambig / greetings / な-adj predicate / きれい) | 27 | Fixed (BUG-264) |
| G | Final P1/P2 section-level fixes (G1–G26) | 45 | Fixed (BUG-265) |
| H | Mechanical closure (counter / legacy / pronoun / family-JA / disclosure) | 23 | Fixed (BUG-264 follow-up) |
| I | Surface remaining OPEN items (docx placeholders + findings report + homonym UI badge) | 995 boxes + UI | Fixed (surfacing) |
| J | Template-generation artifacts (verb conjugations + nonsense sentences) | 142 | Fixed (BUG-266) |

Cumulative data entries with native-reviewer-grade metadata or corrections:
~165 of 995 distinct entries (some touched by multiple batches).

---

## Part 64 — Batch J: template-generation artifacts (added 2026-06-04)

**Trigger.** A specific-bug audit cited 12 concrete JP-content errors
(べんきょうするます, かすました, あるます, しごとするました, まいにち すむ, いま すむ,
あたらしい カタカナ, たかい カタカナ, 今日は とても ぬるいです, この りんごは
うるさいです, えいがは まずいでした, 今日は とても まるいです).

**What was actually true (reproduced against the live corpus).** All 12
confirmed, AND they are instances of a systematic template-generation
defect:

1. **Malformed verb conjugations (objective).** Every verb's
   `particle_examples` carried `<dict-form>ます` and `<dict-form>ました`
   — invalid Japanese (ます appends to the stem, not the dictionary form).
   Scope: **110 verbs** (68 godan, 31 ichidan, 11 irregular) — not the 4
   cited. Fixed deterministically with a verb-class-aware conjugator
   (J1). Homonym disambiguation correct via per-entry pos
   (きる→きります for cut vs きる→きます for wear). Residual sweep: 0
   malformed conjugations remain.
2. **Semantic-frame nonsense (judgment).** Fixed example frames pasted
   onto headwords they can't pair with:
   - `えいがは <i-adj>でした` (16) — grammar error (い-adj past is かった
     です) + nonsense ("the movie was yellow/thin/bitter"). Removed (J2).
   - `今日は とても <adj>です` (14 non-weather: 白い/くろい/みじかい/まるい/
     ぬるい/とおい/おおい/…) — a day can't be those. Removed; weather
     adjectives (すずしい/あたたかい/いい) kept (J3).
   - カタカナ purchase-template collocations (あたらしい/たかい/やすい カタカナ,
     カタカナを かう/ください) — a writing system isn't a buyable object.
     Removed (J4).
   - `この りんごは うるさいです` — an apple isn't noisy. Removed (J4).
   A removal guard ensured no entry dropped below 1 example (0 skips).

**Disposition of the 12 cited.** 10 fully fixed (the 4 conjugations + the
6 semantic-nonsense items). 2 (まいにち すむ / いま すむ) are adverb
collocations in particle_examples — grammatical but stylistically weak —
and belong to the broad particle-example-naturalness class (Batch E /
BUG-263), since fixing them well needs the same per-verb native judgment
as the other ~109 verbs' adverb collocations.

**Addressed this part.**
- `tools/apply_native_review_batch_j_2026_06_04.py` (new) — conjugator
  (J1) + frame-nonsense remover with empty-guard (J2/J3/J4).
- **JA-178** (new CI invariant) — verb entries' `particle_examples`
  must not contain `form+ます` / `form+ました`. Precise comparison
  (against the entry's own form) so it never false-positives on a
  correctly conjugated form. Negative-tested: injected a malformed
  entry → caught (1); restored → 0. CI: **PASS all 180 invariants**
  (179 prior + JA-178).
- Bug tracker: BUG-266 (Fixed), links BUG-263 (residual naturalness).
- sw.js CACHE_VERSION v1.17.38 → v1.17.39; data/version.json synced;
  CHANGELOG v1.17.39; vocab review docx regenerated.

**Bounded phrasing.** JA-178 prevents re-introduction of *the specific
`form+ます`/`form+ました` malformation in verb particle_examples*. It does
NOT certify that a particle_example is a *good* particle example (the
field is template-seeded; naturalness is native-judgment, tracked in
BUG-263), nor catch malformed conjugations in other fields
(`examples[].ja`, glossaries). The semantic-frame removals are addressed
against the cited frames + the conservative allowlist, this snapshot;
the native queue owns the residual.

---

## What this cycle does NOT cover (acknowledged limits)

- **OPEN-001** (per-entry 「問題なし」/「要修正」 native verdicts) — the
  docx now pre-populates a visible 「☐ 未確認」 placeholder per entry
  (batch I) so the unreviewed queue self-flags, but the verdicts
  themselves require a human native speaker.
- **OPEN-003/004** (particle-example + collocation naturalness across
  ~589 flagged entries) — tracked in BUG-263; the
  `docs/vocab-review/N5-vocab-open-items-findings-2026-06-04.md`
  report surfaces the candidates.
- **OPEN-005 / OPEN-013** (English-gloss reframing, example-sentence
  N5-suitability) — case-by-case native judgment; candidates surfaced
  in the same findings report.
- The corpus remains **AI-reviewed, native-human review PENDING**
  (`_meta.native_human_review_status_2026_06_04`). Release docs should
  say "native review in progress", not "native-reviewed complete".

## Artifacts updated in this cycle (Rule 5)

- **Code** (class 2): `tools/apply_native_review_batch_{a-j}_*.py`,
  `tools/register_batch_*_bug_*.py`,
  `tools/build_vocab_review_docx.py` (README + reviewer-box placeholder),
  `tools/audit_open_items_2026_06_04.py`,
  `js/learn-vocab.js` (homonym badge),
  `tools/check_content_integrity.py` (+ JA-178).
- **Data** (class 3): `data/vocab.json` (~165 entries + `_meta` tags),
  `data/version.json`, `data/index.json`.
- **UI** (class 4): SPA homonym badge + CSS; meta mirrors;
  `sw.js` CACHE_VERSION.
- **Bug tracker** (class 5): BUG-262..266 + OPEN-followup roll-up.
- **Test scenarios** (class 6): JA-178.
- **Prompts** (class 7): FP-23 + Phase-0 template-artifact block.
- **Procedure manual** (class 8): F.52.
- **User-facing docs** (class 9): CHANGELOG, vocab review docx,
  findings report, this file.

## Part 65 — Batch E follow-up: reviewer-cited particle-collocation subset fixed (added 2026-06-06)

**Trigger.** A native reviewer re-reported specific `particle_examples`
items from the deferred particle-example-naturalness class (Part 64's
Batch E / BUG-263): pronoun/noun 「Xを しる」, question-word 「だれを しますか」
/「どなたを しますか」/「だれに いきますか」, reflexive じぶんは がくせい, plus
notation typos (日本ご, よ人, 一いっしょ, そふぼや) and a 大人 admission-price
inconsistency.

**Disposition.** The reviewer-CITED entries were fixed per-headword
(native-judgment, no auto-fix): 「Xを しる」 → the natural verb across 24
pronoun/noun entries; question-word frames → grammatical だれと いきますか /
だれに ききますか; じぶんは がくせい → じぶんで つくる; notation typos repaired;
大人 price made internally consistent (千円). The vocab review docx was
regenerated and re-verified (0 「を しる」, 0 「じぶんは がくせい」).

**Bounded phrasing.** Only the reviewer-CITED entries are addressed this
snapshot; the corpus-wide particle-example naturalness sweep across the
remaining entries stays deferred to the native queue (Batch E / BUG-263).
No new CI invariant — naturalness is native-judgment, not auto-checkable.
Reviewer-deliverable hygiene for this cycle is captured in procedure-manual
Appendix F.53 (auto-stamped review docx, keep-exactly-one).
