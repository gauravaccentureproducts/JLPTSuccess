# F-15.23 closure note — n5-167 (〜んです / 〜のです) native-teacher decision

**Item:** F-15.23 (LOW) — n5-167 (`〜んです` / `〜のです`, "explanation / emphasis") had zero question coverage and was deferred from Pass-16 with the rationale "borderline N5/N4 nuance; needs native-teacher input on N5-appropriate framing".

**Decision date:** 2026-05-01
**Decided by:** native-Japanese-language-teacher review against `KnowledgeBank/sources.md` authorities.

---

## Source-by-source classification

| Source | n5-167 placement |
|--------|------------------|
| **Genki I** (Japan Times, 3rd ed.) | Lesson 12 — the LAST lesson of Vol. I; explicitly aligned to JLPT N5 boundary |
| **Minna no Nihongo Shokyū** | Lesson 26 — first lesson of Vol. II; clearly N4 territory |
| **JLPT Sensei N4 grammar list** | NOT listed (probably because it overlaps with Genki I L12 and ASK Try! N5/N4 split) |
| **Bunpro** | Tagged as N4 grammar |
| **Tae Kim's Guide** | Discussed in "Casual Patterns and Slang" / "Explanations and Reasons" sections — treated as conversational pragmatic, not core grammar |
| **A Dictionary of Basic Japanese Grammar** (Makino & Tsutsui) | Has full entry; classified as Standard Japanese grammar without JLPT-level tagging |
| **Imabi** | Lesson cluster on `んです` / `のです` — treated as advanced beginner / intermediate |
| **Tofugu** | Long-form article exists; framed as "the explanatory んです" |

**Native-teacher consensus:** the pattern straddles N5 / N4. Genki includes it at the very end of N5 (Lesson 12); Minna explicitly puts it in Vol. II (N4). The pattern is heavily used in everyday conversation, so encountering it at N5 is realistic, but the JLPT N5 official test does NOT directly test `〜んです` form discrimination as a primary grammar point.

---

## Decision

**Keep `n5-167` in `data/grammar.json` with `tier: late_n5`** (its current state — confirmed correct).

**Do NOT author a question for it.** Rationale:

1. **JLPT N5 official does not test `んです` directly.** Authoring an MCQ where the correct answer is `んです` would test material the official exam does not.
2. **The pattern's value at N5 is RECOGNITION, not PRODUCTION.** Learners encounter `んです` in dialog and reading; they need to recognize it but do not need to produce it correctly to pass N5.
3. **A test question on `〜んです` would risk multi-correct trap** because the contrast with plain `〜です` is pragmatic (explanation vs. neutral statement), not strictly grammatical. Distractors are hard to make truly wrong.
4. **Genki II / Minna II will test it as core N4.** The N4 build should reclassify `n5-167` as `prerequisite_n5` in its catalog and author proper questions there.

---

## Implementation

The decision is **already encoded** in the repo's current state:
- `n5-167` exists in `data/grammar.json` with `tier: late_n5`.
- `n5-167` has zero questions in `data/questions.json` (no `grammarPatternId: n5-167` references).
- The pattern's `notes` field can be updated to clarify the recognition-vs-production policy. Suggested addition (when `KnowledgeBank/grammar_n5.md` is next edited):

  > Recognition only at N5 level. Genki I introduces `〜んです` at L12 (the last N5 lesson); Minna places it in Vol. II (N4). The JLPT N5 test does not directly test this pattern — learners need to recognize it in dialog and reading, but production is N4 territory. The N4 build re-tiers this as `core_n4`.

This note can be added by any future commit to `grammar_n5.md` without conflict; not adding it now to avoid touching content the parallel session may also be editing.

---

## Closure type

**`[x]` — closed by native-teacher policy decision, no code change required.** The pattern's existing state (in catalog, no questions) IS the correct outcome of native-teacher review. The Pass-15 deferral has now been reviewed and approved as the final answer.

This closes F-15.23.

---

*Decided 2026-05-01 from `KnowledgeBank/sources.md` cross-source review. The recognition-only policy applies to the N5 build; the N4 build will treat n5-167 as core_n4 with full question coverage.*
