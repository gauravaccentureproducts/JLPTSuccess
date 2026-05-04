# Seasoned-Japanese-Teacher Audit — 2026-05-02

Pass-24 content audit done from the perspective of a working JLPT N5
instructor. Combined automated heuristic scans (`tools/audit_teacher_review.py`)
and manual eyeball review of a stratified 25-question sample.

## Scope

- `data/questions.json` (250 MCQs / sentence-order / text-input items)
- `data/grammar.json` (187 patterns × ~5 examples each = ~935 examples)
- `data/reading.json` (30 graded passages)
- `data/listening.json` (30 items)
- `data/vocab.json` (1003 entries)
- `data/kanji.json` (106 entries)
- `KnowledgeBank/{moji,goi,bunpou,dokkai}_questions_n5.md` (591 KB questions)

## Methodology

Nine automated check classes (T-1 .. T-9) covering common N5-instructor
red flags:

| Code | Class | Findings |
|---|---|---|
| T-1 | Particle-verb mismatch (を行く, で住む, に飲む…) | **0** |
| T-2 | Conjugation errors (来って, 行きった, 食べりて…) | **0** |
| T-3 | Register inconsistency (plain + polite in one clause) | **0** |
| T-4 | Counter-reading errors (3本=さんぼん etc.) | **0** |
| T-5 | EN-gloss faithfulness (negation/tense mismatch) | 11 (all FP) |
| T-6 | N4-borderline grammar without `tier=late_n5` | **2 → 0 fixed** |
| T-7 | High-confusion grammar without `common_mistakes` | 56 (gap-not-bug) |
| T-8 | Vocab kanji form out-of-scope vs catalog | **0** |
| T-9 | Ko-so-a-do distance-Q without scene anchor | 0 (after refining) |

Plus 25-question stratified manual eyeball review.

## Findings — fixed in this pass

### F-T6.1 (LOW) — `n5-172` (～なくてもいい) missing `tier: late_n5`
Pattern is at the N5/N4 boundary (Genki I L17 in some editions; Genki II
L17 in others; JEES official scope places it in N4). The category name
already calls it "Borderline" but the machine-readable `tier` field was
unset.

**Fix applied:** added `"tier": "late_n5"`.

### F-T6.2 (LOW) — `n5-176` (～なくちゃ / ～なきゃ) missing `tier: late_n5`
Colloquial contractions of `～なければならない`. Standard textbook
classification: N4 (Genki II L17 plain-form contractions). Should not
appear at core-N5 level without a boundary flag.

**Fix applied:** added `"tier": "late_n5"`.

### F-T7.1 (MEDIUM) — q-0507 multi-correct (の vs こと)
Stem: 「えいがを 見る（  ）が すきです。」
Choices: こと / の / もの / ところ
Marked correct: の.

The question's own rationale admitted: *"Either could work; の is the
most direct."* Native speakers freely use either の or こと with sensory
verbs like 見る; the textbook rule of thumb (の for concrete activities,
こと for abstract concepts) is not a hard rule. Marking こと as wrong is
incorrect.

**Fix applied:** replaced こと with で in the choice set. の is now the
unambiguously correct nominaliser-particle (で is a particle, not a
nominaliser; もの and ところ form different noun phrases that don't fit
the 「X が すきです」 frame as cleanly). Rationale rewritten to document
the substitution and acknowledge the の/こと interchangeability.

## Findings — clean (audit confirms no issue)

### T-1, T-2, T-3, T-4, T-8 — clean
Zero findings each. The Pass-23 round-3 multi-correct sweep + Pass-13
kanji-scope work + the N5-vocab/kanji catalog discipline have already
caught the patterns these checks watch for.

### T-9 — clean (after refining heuristic)
Initial heuristic flagged 6 questions; on review, 5 had parenthetical
scene contexts that were the anchor (heuristic missed them) and 1
(q-0509 「（  ）ほんを ください。」) was a form-test (これ vs この vs
それ vs ここ — only one is grammatical regardless of distance), not a
distance-test. Heuristic refined to filter these false positives; final
finding count: 0.

## Findings — false positives (heuristic limitations)

### T-5 (EN gloss) — 11 findings, all false positives

Manual review confirmed every flagged item is a correct natural
translation. The patterns my heuristic over-fires on:

1. **い-adjective ending in ない** (あぶない = "dangerous"): regex sees
   `ない` as a negative marker.
2. **すみません as fixed apology** ("excuse me / sorry"): regex sees
   `ません` as verbal negative.
3. **～ませんか invitation idiom** ("won't you ~?" → natural EN
   "Shall we?" / "Would you?"): JA negative form, EN positive form,
   both correct.
4. **～ね tag question** ("isn't it?" / "right?"): EN "n't" matches
   negation regex but is a tag-question marker, not negation.
5. **～なくてもいい / ～なくては いけない / ～なくては ならない idioms**:
   double-negative obligation patterns. JA has なく/ない, EN has "don't
   have to" / "must" — semantically aligned but surface-level
   negation polarity differs.

**No fixes needed.** The regex is documented in
`tools/audit_teacher_review.py` and these false-positive classes are
called out in the SUPPRESS_IDIOM list and the comment block. A more
sophisticated heuristic would need a JA dependency parser; out of scope
for an automated check.

## Findings — content-authoring opportunities (not bugs)

### T-7 — 56 high-confusion patterns lack `common_mistakes` content

187 grammar patterns, 177 carry a `common_mistakes` array, ~10 have it
empty. Of those plus a broader high-confusion subset (patterns whose
pattern-string contains a particle character), 56 lack the rich
"learner pitfall" content that distinguishes a teaching-quality bank
from a reference-quality one.

This is **not an error** — the patterns are correct, and the
`common_mistakes` field is optional. It IS a content-authoring
opportunity: a real Japanese teacher would say a learner-facing bank
should call out the top 1-2 confusion classes per high-frequency
pattern.

**Recommendation:** treat as a Pass-25 backlog item. Estimated effort:
~2-3 hours per 10 patterns to author 1-3 `common_mistakes` entries
each from teacher experience; total ~12-15 hours for the 56-pattern
set. Out of scope for this audit.

## Manual eyeball review — 25 stratified-random questions

Reviewed deterministically (random.seed=42) across 25 grammar patterns:

- **23/25**: fully correct, natural Japanese, accurate answer key,
  pedagogically sound rationale.
- **q-0500** 「およぎ（  ）できます」 (answer が): borderline natural —
  「およぎが できます」 is colloquial; standard form is 「およぐ ことが
  できます」 or just 「およげます」. Acceptable but a teacher would
  prefer the standard form. **NOT FIXED** (acceptable as-is).
- **q-0507** 「えいがを 見る（  ）が すきです」: confirmed multi-correct
  (の and こと both valid). **FIXED** (see F-T7.1 above).

Sample-confirmed correctness rate: 23/25 = **92%**, with one fixed and
one acceptable-with-caveat.

## Overall verdict

**Content quality is high.** The four "if-it-existed-it-would-be-bad"
classes (T-1 / T-2 / T-3 / T-4) all came back zero. The two real
issues caught (T-6 × 2 patterns missing `tier`, T-7.1 multi-correct
question) are edge-case items that a routine audit would catch on the
next pass, and have been fixed in this commit.

The biggest standing opportunity is content authoring on
`common_mistakes` (T-7, ~56 patterns). That's a teaching-richness
item, not a correctness item.

## Tooling shipped

- `tools/audit_teacher_review.py` — 9-class teacher-perspective heuristic
  audit. Re-runnable. Filterable via `--category T-N`. Documents its own
  false-positive boundaries inline.
- `tools/sample_questions_for_review.py` — deterministic stratified
  25-question sampler for manual review.
- `tools/audit_dokkai_kanji_scope.py` (shipped earlier in the JA-sweep) —
  inventories non-N5 kanji in dokkai papers.
