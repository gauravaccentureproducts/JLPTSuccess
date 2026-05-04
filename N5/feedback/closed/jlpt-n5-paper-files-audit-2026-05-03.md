# JLPT N5 Tutor - Mock Paper Files Audit (bunpou + dokkai + goi)

**Date:** 2026-05-03
**Audit scope:** 15 mock-test paper JSON files:
- 7 bunpou papers (`bunpou-1` through `bunpou-7`, Q1-Q100, 100 questions total)
- 1 dokkai paper (`dokkai-4`, Q49-Q60, 12 questions across 6 passages)
- 7 goi papers (`goi-1` through `goi-7`, Q1-Q100, 100 questions total)

**Audit lens:** Japanese-language accuracy from a 日本語教師 perspective, plus correctness of answer keys, distractor strength, schema integrity, and policy compliance against the N5 kanji whitelist and dokkai exception register.

---

## 0. Executive summary

These mock papers are mostly well-constructed, with thoughtful distractors and honest rationales that acknowledge nuance (e.g., goi-4 Q60 noting おおぜい ≠ たくさん strictly, goi-7 Q99 noting 知っている ≠ 覚えている in general). The pedagogical instinct in many of the rationales is excellent - the kind of nuance a native teacher would explain in person.

But there are real defects that need attention before these papers can be used live:

- **The most serious issue is structural**: 19 of the 30 questions in bunpou papers 5 and 6 (the JLPT 並べ替え / sentence-rearrange format) have **empty `stem_html` fields**. These questions cannot be answered as currently exported.
- **4 goi papers contain non-N5 kanji** in distractor or correct-answer text, in violation of the policy stated in `dokkai_kanji_exception.json` ("bunpou / moji / goi paper content MUST stay strictly N5").
- **One reading-passage word in bunpou-7 looks like an extraction typo**: ぎんこう (bank) where context strongly implies 学校 (school).
- **Several questions have stale "---" residue** from the source markdown's section separators.

**Total actionable items: 12** (1 critical, 4 high, 5 medium, 2 low).

---

## 1. CRITICAL

### 1.1 Bunpou Papers 5 + 6 - 19 of 30 questions have empty `stem_html`

Bunpou papers 5 and 6 use the JLPT-style 並べ替え (sentence-rearrange) format. Each question presents a sentence frame with 4 numbered blanks, one of them marked ★, and 4 word-tile choices. The student must mentally arrange all 4 tiles into the right order, then pick which tile lands on the ★ position.

**Example of a working question (bunpou-5.1, Q61):**
```json
{
  "stem_html": "きのう ___ ___ ★ ___ 見ました。",
  "choices": ["を", "ともだちと", "えいが", "いっしょに"],
  "correctIndex": 2
}
```
Reconstructed: 「きのう ともだちと いっしょに えいがを 見ました。」 - the ★ position holds えいが. ✓

**Example of a broken question (bunpou-5.4, Q64):**
```json
{
  "stem_html": "",
  "choices": ["何", "あの 店", "の", "名前は"],
  "correctIndex": 3
}
```

With no sentence frame, the student sees four disconnected words. There's no way to know what sentence is being formed, and no anchor for what the ★ position represents. Even reconstructing the intended sentence (probably 「あの 店の 名前は 何 ですか。」) requires knowing that the stem ends with 「ですか。」 - which isn't present in the JSON.

**Affected questions:**

| Paper | Empty-stem question IDs |
|---|---|
| bunpou-5 | Q64, Q67, Q68, Q69, Q70, Q71, Q74 (7 of 15) |
| bunpou-6 | Q76, Q77, Q78, Q79, Q80, Q81, Q82, Q84, Q86, Q87, Q88, Q89 (12 of 15) |
| **Total** | **19 of 30** |

**Likely cause:** the JSON appears to have been generated from `KnowledgeBank/bunpou_questions_n5.md`. The extraction step probably parses the stem from a specific markdown pattern and fails when the pattern is non-standard. Bunpou-5/6 use sentence-rearrange which has different markdown structure than fill-in-the-blank.

**Severity:** Critical. 19 questions are unanswerable as currently shipped. If these papers are exposed to learners, two-thirds of paper 6 (and half of paper 5) will display as a 4-tile word salad.

**Suggested fix:** re-extract these 19 stems from the source markdown. As a temporary mitigation, the affected questions can be hidden until stems are populated.

---

## 2. HIGH

### 2.1 Goi papers - 4 non-N5 kanji violations in distractor / correct-answer text

The `dokkai_kanji_exception.json` `_doc` field is explicit:

> bunpou / moji / goi paper content MUST stay strictly N5 (catalog at KnowledgeBank/kanji_n5.md).

Yet 4 goi questions contain kanji not in the N5 whitelist:

| Question | Non-N5 kanji | Where it appears |
|---|---|---|
| goi-4 Q58 | **早** (はや) | Choice [1] (the correct answer): 「きのう **早**く ねました。」 |
| goi-5 Q65 | **少** (すこ) | Choice [0] (distractor): 「もう少し いましょう。」 |
| goi-6 Q86 | **紙** (かみ) | Choice [3] (distractor): 「友だちに **手紙**を 書きました。」 |
| goi-7 Q100 | **売** (う) | Choice [1] (distractor): 「わたしは ピアノを **売**って います。」 |

**Most pedagogically problematic:** goi-4 Q58. The stem uses kana 「はやく」, but the marked-correct answer uses kanji 「早く」. The rationale says "paraphrase identical with kanji." But this isn't a paraphrase - the words are identical; only the writing system differs. And 早 is not in the N5 whitelist, so a learner who has only studied N5 kanji has no way to read this answer choice. The question essentially tests a kanji the student wasn't supposed to learn yet.

**Fixes (per question):**
- goi-4 Q58: change choice [1] to 「きのう はやく ねました。」 (kana). The "paraphrase" is then: stem 「きのうの よる、はやく ねました」 → answer 「きのう はやく ねました」 (drops 「の よる」). This is a weak paraphrase but at least within scope.
- goi-5 Q65: change to 「もう すこし いましょう。」 (kana for 少).
- goi-6 Q86: change to 「友だちに てがみを 書きました。」 (kana for 紙). Note 手 IS N5; the problem is just 紙.
- goi-7 Q100: change to 「わたしは ピアノを うって います。」 (kana for 売).

**Severity:** High. Direct policy violation in 4 places. Goi-4 Q58 in particular is a real teaching defect: the marked-correct answer uses a non-N5 kanji that the learner cannot read.

### 2.2 Bunpou Paper 7 Passage B - ぎんこう reads like a 学校 extraction typo

**Passage B (Q96-Q100 context):**
> わたしの しゅみ
> わたしは おんがく [ 1 ] すきです。 まいにち、 **ぎんこう**から かえってから、いえで ピアノを 一時間 [ 2 ]。 にちようびは 友だちと いっしょに [ 3 ] に 行きます。 友だち も ピアノが じょうずですから、 とても たのしいです。 [...]

**Translation of the sentence:** "Every day, after returning from **the bank**, I play piano at home for one hour."

**Problem:** the surrounding context is hobby (しゅみ) - piano, friends, lessons - and the speaker plays for one hour after returning home. The natural daily-routine framing would be a student returning from school. 「学校から かえってから、いえで ピアノを ひきます」 is an N5 textbook-canonical sentence.

「銀行から かえってから」 ("after returning from the bank") is grammatically fine but contextually strange - it would mean the speaker either works at a bank, visits the bank daily, or has banking errands every day before piano. None of these is wrong, but none fits naturally with a hobbies passage.

**Hypothesis:** the source markdown probably has 学校 here, and the JSON extraction step rendered the kanji incorrectly. Worth verifying against `KnowledgeBank/bunpou_questions_n5.md`.

**Severity:** High. Single-word fix; affects how natural the passage reads. If 銀行 is intentional, the passage should be re-anchored (e.g., establish "わたしは ぎんこういんです" up front so the bank reference fits).

### 2.3 Dokkai Paper 4 Q58 prompt has two Japanese-language issues

**Prompt:**
> どうして **書いた 人**は 友だちと **もう一どに** 行きたいですか。

**Issue A - もう一どに:** the adverb もう一度 (もういちど, "one more time") does not take particle に. The natural form is just 「もう一ど 行きたい」. The に here parses as ungrammatical. Possibilities:
- It's a typo (extra に)
- It was intended as 「もう一日」 (もう一にち, "one more day"), which IS sometimes followed by に, but the kana 一ど argues against this reading.
- It's meant as 「もう一度に」 (a literary/archaic emphatic form - unusual outside formal writing)

For an N5 question prompt, none of these reads as intended. The clean fix: remove the に.

**Issue B - 書いた 人:** standard JLPT N5 dokkai question phrasing uses 「この 人」 (this person) or 「私」 to refer to the passage's narrator. 「書いた 人」 ("the person who wrote") is grammatically valid but unusual at N5 level - it sounds slightly stilted and doesn't match the conventions of authentic JLPT past papers.

**Suggested fix:**
> どうして この 人は 友だちと もう一ど 行きたいですか。

**Severity:** High. Affects a single question but combines two non-natural elements in one prompt. A native reviewer would flag both immediately.

### 2.4 Bunpou Paper 4 Q60 ends with stray "より. ---" in rationale

**Q60 rationale:** `"comparison より. ---"`

The trailing `---` is markdown horizontal-rule syntax that leaked from the source file's section-separator. Same issue confirmed in:
- goi-4 Q50 rationale: `"taller than father. ---"`
- bunpou-7 Q100 rationale: ends with `「ぜったいに」 (firm resolve). ---`
- goi-7 Q100 rationale: `"learning ≈ practicing. ---"`

**Pattern:** each affected question is the LAST question of the LAST paper in its category (Q60 = end of bunpou-4, Q50 = end of goi paper section, Q100 = end of paper 7 in both bunpou and goi). The `---` separator from the source markdown was preserved verbatim into the rationale field instead of being stripped.

**Severity:** High by visibility - these strings render in the rationale UI and look like a bug to any user reading them.

---

## 3. MEDIUM

### 3.1 Bunpou-5 / Bunpou-6 - empty `rationale` fields on the same 19 broken questions

The 19 questions with empty `stem_html` (§1.1) ALSO have empty `rationale` fields. So even if the runtime fetched the stem from a markdown source as a fallback, the user would still get no explanation when answering correctly or incorrectly.

For comparison, bunpou-1/2/3/4 average ~30-character rationales explaining each particle / form choice. Bunpou-5/6 sentence-rearrange questions need at least a one-line rationale showing the full reconstructed sentence with the answer position highlighted.

**Severity:** Medium. Subsumed by 1.1 in priority (fix the stems first), but worth knowing the rationale gap exists too.

### 3.2 Schema inconsistency - only 2 of 100+ questions have BOTH `rationale` AND `explanation_en`

`explanation_en` appears on exactly 2 questions across the entire dataset:

- bunpou-4 Q56: explains 「や 〜 など」 listing pattern
- goi-2 Q21: explains why a previous version's stem was ambiguous

All other questions use only `rationale`. The 2 outliers seem to be edit-history artifacts where someone added detail beyond what the existing rationale field would hold and used a new field name rather than extending the existing one.

**Suggested fix:** merge the explanation_en content into rationale, or formally promote explanation_en as a sibling field used by all questions (in which case 100+ questions need migration).

**Severity:** Medium. Not a learner-facing issue if the renderer falls back to rationale, but it's a schema-cleanliness flag.

### 3.3 Goi-6 Q87 - 二十さい (mixed reading) vs はたち (canonical N5 reading)

**Stem:** 「わたしは 二十さいです。」

**Rationale (paraphrased):** acknowledges that the canonical reading at N5 is **はたち** (二十歳), and that 二十さい is technically valid but not the form most-tested at N5.

**Problem:** the rationale is correctly nuanced, but the stem still uses the non-standard form. JLPT N5 tests the irregular reading はたち explicitly. A student answering this question may also be tested on はたち in a moji/goi paper - and there they would need to read 「二十歳」 as はたち, not にじゅうさい.

**Suggested fix:** change the stem to 「わたしは はたちです。」 or 「わたしは 二十歳です。」 (using the kanji 歳 - but 歳 is not in N5 whitelist, which forces back to はたち kana). The cleanest fix is the all-kana form 「わたしは はたちです。」

**Severity:** Medium. Affects one question but represents a subtle teaching gap.

### 3.4 Dokkai Paper 4 Q60 - 「後の 日に なりました」 is awkward phrasing

**Prompt:** どうして ハイキングは **後の 日**に なりましたか。

**Problem:** 「後の 日」 reads literally as "later day / subsequent day," but native Japanese rarely uses this construction. The natural ways to express "got pushed to a later date":
- 「来週に なりました」 ("became next week")
- 「べつの日に なりました」 ("changed to another day")
- 「のちの日に なりました」 (slightly stilted but more natural than 後の日)

The passage itself uses 「らいしゅうに します」 ("decide on next week"), so 「来週に なりました」 would also be the cleanest match to the passage register.

**Severity:** Medium. Comprehensible but not natural Japanese.

### 3.5 Dokkai Paper 4 - 「> 」 markdown blockquote prefix in passage text

All 6 passages in dokkai-4 begin with `"> "` (blockquote marker plus space) in the `text` field. For example:
```json
"text": "> 私の 父は 毎日 八時に 家を 出ます。 ..."
```

**Problem:** if the runtime renders this as plain text, learners will see `> ` literally before each passage. If the runtime interprets it as markdown, it'll render as a quoted block - which may or may not be the intended visual treatment.

This is the markdown's own quoting convention from the source `dokkai_questions_n5.md` file leaking into the JSON without normalization. Other passages in older audits (reading.json, listening.json) didn't carry this prefix.

**Suggested fix:** strip the leading `"> "` from each passage text during JSON generation.

**Severity:** Medium. Visible to users if the runtime doesn't process markdown.

---

## 4. LOW

### 4.1 Goi-1 Q11 - multi-defensible distractors

**Stem:** 「この りんごは （　　）。」 (This apple is __.)

**Choices:** おいしいです / たかいです / あおいです / おもしろいです
**Correct:** おいしいです (delicious)

**Problem:** at N5, this is technically a "best fit" question, but two of the four choices are linguistically natural completions:
- 「この りんごは おいしいです」 ✓ - most common everyday completion
- 「この りんごは たかいです」 ✓ - perfectly natural for an expensive apple
- 「この りんごは あおいです」 - defensible for an unripe (green) apple, but unusual standalone
- 「この りんごは おもしろいです」 - almost never said about an apple

A learner could legitimately answer たかい and be told they're wrong, with no semantic basis for why おいしい is more correct. The rationale 「food + おいしい」 is true as a default association but doesn't disqualify たかい.

**Suggested fix:** anchor the stem with context. For example: 「この りんごは あまくて、（　　）です」 ("This apple is sweet and __") forces おいしい over たかい. Or remove たかい from the distractors.

**Severity:** Low. The intended answer is the most natural; the distractor weakness only matters if a learner gets unfairly penalized.

### 4.2 Goi-4 Q58 is mislabeled as a "paraphrase" question

**Stem:** A: 「きのうの よる、はやく ねました。」 ("Last night, I went to sleep early.")
**Marked correct:** 「きのう 早く ねました。」 ("Yesterday, I went to sleep early.")
**Rationale:** "paraphrase identical with kanji."

**Problem:** the rationale's own admission says it all - this isn't a paraphrase. Stem and answer are the same sentence, with one phrase change (「きのうの よる」 → 「きのう」, dropping "the night of" as a small information loss) and one orthographic change (はやく → 早く).

A real paraphrase question would test understanding by rewording with different vocabulary or syntax. Examples:
- 「きのうの よる、はやく ねました」 ↔ 「きのう、はやい じかんに ねました」
- 「きのうの よる、はやく ねました」 ↔ 「きのうは おそく ねません でした」

The current question is essentially a kanji-recognition exercise mislabeled as a paraphrase task. Combined with §2.1 (the kanji 早 isn't in N5 whitelist), this question has multiple problems compounding.

**Severity:** Low. Question still "works" as long as the learner reads either form correctly, but it misrepresents what skill is being tested.

---

## 5. Cross-cutting good news

This deserves emphasis because the quality of thinking in the rationale fields is genuinely high:

**Examples of nuanced pedagogical rationales** that a native teacher would write:

- **goi-4 Q60** explicitly notes that おおぜい (many people) is restricted to people while たくさん is general - and explains why the substitution works in this specific stem. That's careful teacherly writing.
- **goi-7 Q99** says 「知っている and 覚えている are near-synonyms in the context of remembering someone's name, but they are not interchangeable in general - you can 知っている a name without 覚えている it (knew it but forgot), and vice versa. **Don't memorize this as a synonymy rule.**」 The closing don't-memorize-this directive is exactly what a good textbook would say.
- **goi-6 Q90** acknowledges that 元気 implies vigor while 病気ではない is just absence of illness - they overlap in everyday speech but aren't identical.
- **bunpou-4 Q50/Q51** distractors include けど/が which are concessive (not causal), and the rationale explicitly explains they "would invert the logic." This trains the student to think about logical-flow, not just particle memorization.
- **bunpou-7 Q98** rationale notes that an earlier version of choice [4] was "ピアノを 買い" which would have been a structurally-valid alternate answer, and explains the replacement.

**Other positive findings:**
- All 100 goi questions have populated stem_html, choices, correctIndex, rationale, and ID fields.
- Goi questions stay structurally well-formed throughout - no missing fields, no malformed JSON.
- Dokkai-4 passages stay within (N5 whitelist + dokkai exception) - kanji conformance is clean.
- Many questions thoughtfully include "by elimination" language in the rationale where the closest answer is admittedly imperfect - instead of pretending exact synonymy, the rationale teaches the student to choose the best among options.

This is the kind of corpus where the content-author's voice clearly cares about the language. The defects above are mostly extraction-pipeline artifacts and a small number of inherited issues, not content-quality problems.

---

## 6. Recommended next-step priorities

If only 5 things get worked on:

1. **Fix the 19 empty stems in bunpou-5 and bunpou-6** (§1.1). Re-extract from `KnowledgeBank/bunpou_questions_n5.md`. As a stopgap, hide these questions from the user-facing test runner until populated.
2. **Fix the 4 non-N5 kanji violations in goi papers** (§2.1). Replace 早/少/紙/売 with their kana forms in the affected choices.
3. **Verify and fix bunpou-7 Passage B's ぎんこう/学校** (§2.2). Check the source markdown; it's almost certainly an extraction error.
4. **Fix dokkai-4 Q58's prompt** (§2.3). Two textual edits: remove に from もう一どに, replace 書いた 人 with この 人.
5. **Strip the trailing `---` from 4 rationales** (§2.4) and the leading `> ` from dokkai-4 passages (§3.5). Both are markdown-residue cleanups in the JSON generator.

The remaining items (schema inconsistency, 二十さい/はたち, 後の日, multi-defensible distractors, mislabeled paraphrase) are polish-grade and can be batched.

---

## 7. Quick-reference issue summary

| Severity | ID | Paper | Issue |
|---|---|---|---|
| CRITICAL | 1.1 | bunpou-5, bunpou-6 | 19 of 30 sentence-rearrange questions have empty stem_html |
| HIGH | 2.1 | goi-4, goi-5, goi-6, goi-7 | 4 non-N5 kanji (早/少/紙/売) in choice text, violating policy |
| HIGH | 2.2 | bunpou-7 | Passage B uses ぎんこう where context implies 学校 (likely extraction error) |
| HIGH | 2.3 | dokkai-4 Q58 | Prompt has 「もう一どに 行きたい」 (extra に) and 「書いた 人」 (unusual JLPT phrasing) |
| HIGH | 2.4 | bunpou-4, bunpou-7, goi-4, goi-7 | Trailing `---` markdown residue in 4 rationales |
| MEDIUM | 3.1 | bunpou-5, bunpou-6 | Empty rationale on the same 19 broken questions |
| MEDIUM | 3.2 | bunpou-4 Q56, goi-2 Q21 | Schema: only 2 questions have both rationale and explanation_en |
| MEDIUM | 3.3 | goi-6 Q87 | Stem uses 二十さい when N5-canonical reading is はたち |
| MEDIUM | 3.4 | dokkai-4 Q60 | Prompt phrase 「後の 日に なりました」 reads awkwardly |
| MEDIUM | 3.5 | dokkai-4 (all 6 passages) | Leading `> ` markdown blockquote marker leaked into passage text |
| LOW | 4.1 | goi-1 Q11 | Multi-defensible distractors (おいしい / たかい both natural for "this apple is __") |
| LOW | 4.2 | goi-4 Q58 | Mislabeled as "paraphrase" - stem and answer differ only in writing system |

**Total: 12 actionable items** (1 critical, 4 high, 5 medium, 2 low).

---

*End of audit. Prepared 2026-05-03.*
