# JLPT N5 KnowledgeBank Markdown - Consolidated Content Audit

**Date:** 2026-05-01
**Audit scope:** 9 markdown files comprising the source-of-truth content corpus:
- `grammar_n5.md` - grammar pattern catalog
- `kanji_n5.md` - kanji catalog
- `vocabulary_n5.md` - vocabulary catalog
- `sources.md` - reference documentation
- `moji_questions_n5.md` - kanji reading and orthography questions
- `goi_questions_n5.md` - vocabulary and paraphrase questions
- `bunpou_questions_n5.md` - grammar questions
- `dokkai_questions_n5.md` - reading comprehension questions
- `authentic_extracted_n5.md` - third-party scraped questions

**Audit lens:** Japanese-language accuracy and pedagogical correctness from a seasoned 日本語教師's perspective. Cross-checked against `n5_kanji_whitelist.json` and `n5_vocab_whitelist.json`.
**Comparison baseline:** Earlier KnowledgeBank audit dated April 2026 that flagged 27 actionable items.

---

## 0. Executive summary

The corpus has substantially improved since the April 2026 audit. Most previously flagged CRITICAL and HIGH issues have been addressed:

**Verified resolved:**

- `kanji_n5.md` - the missing kanji 力, 手, 足, 目, 口 are all present (previously CRITICAL §1.1).
- `kanji_n5.md` - 万 reading: バン moved to a note as rare/specialized.
- `kanji_n5.md` - 円 meaning order: "yen" first, with まる(い) noted as N4+.
- `kanji_n5.md` - dropped non-N5-pedagogical kun readings: のぼ(る), お(りる), ほか, キン on 今.
- `kanji_n5.md` - 番 readings: now correctly just バン (no spurious ゴウ).
- `dokkai_questions_n5.md` - Passage F now uses ことし (was こんねん, previously CRITICAL §1.2).
- `dokkai_questions_n5.md` - mixed-kanji-and-kana words (e.g., 大さか) eliminated.
- `bunpou_questions_n5.md` Q50, Q51 - the "two valid answers" issue with から / ので fixed by replacing ので with けど (clearly concessive, so now wrong).
- `bunpou_questions_n5.md` Q24 - しんかんせん replaced with でんしゃ (N5 vocab).
- `bunpou_questions_n5.md` Q98 - the "two structurally valid answers" issue fixed by replacing the broken option.
- `bunpou_questions_n5.md` Q100 - でも rationale corrected: "even (just)" not "at least."
- `bunpou_questions_n5.md` Q70 - 図しょかん mixed form replaced with としょかん.
- `goi_questions_n5.md` Q47 - 去年 (kanji) replaced with きょねん (kana).
- `goi_questions_n5.md` Q70 - rationale softened from synonymy claim to "closest among the choices."
- `goi_questions_n5.md` Q86 - 電話をかける rationale softened similarly.
- `goi_questions_n5.md` Q87 - はたち vs 二十さい note added explicitly.
- `goi_questions_n5.md` Q94 - rationale corrected to "by elimination."
- `goi_questions_n5.md` Q99 - 知っている / 覚えている rationale corrected to "near-synonyms not interchangeable."
- `moji_questions_n5.md` Q6 - rationale tightened (にっぽん noted but not in answer choices).
- `moji_questions_n5.md` Q54 - 力 question now valid because 力 is in the kanji catalog.
- `moji_questions_n5.md` Q58 - 手 question valid for same reason.
- `moji_questions_n5.md` Q62 - 子供 vs 子ども policy note added explicitly.
- `vocabulary_n5.md` Section 27 - Group-1 ru-verb exceptions now flagged BOTH in section header AND on each individual entry.
- `vocabulary_n5.md` line 287 - もう definition fixed: "already (with affirmative); anymore (with negative); more (as in もう一つ)" - dropped misleading "soon" gloss.
- `grammar_n5.md` Section 22 - renamed to "Polite / Beautifying Vocabulary" with explicit terminology note about bika-go vs sonkei-go.
- `grammar_n5.md` Section 6 - now explicitly lists Group-1 ru-verb exceptions inline.
- `sources.md` - CEFR claim softened to "verify the current status" (was a confident date-stamped assertion).
- `authentic_extracted_n5.md` - the file now has explicit provenance disclosure that questions are scraped from a third-party site, NOT from JEES official samples; planned Pass 12 to re-source from official samples.

**This is significant progress.** The previous audit identified roughly 27 items; the majority appear to be addressed.

**Remaining issues split into:**
- **One critical Japanese-grammar bug** (a two-valid-answers question that escaped the previous fix).
- **Mechanical residue** (two "direct synonym" overclaims still present, naming kanji-policy clarifications).
- **Structural** (question stems vs documented kanji policy in dokkai).

Total remaining actionable items: 9 (1 critical, 3 high, 4 medium, 1 low).

---

## 1. CRITICAL - factual errors that mislead a learner

### 1.1 `bunpou_questions_n5.md` Q94 - two grammatically valid answers (に / へ)

**Passage A (Mondai 3):**
> たなかさんの 一日
> ...8時に いえを 出て、電車で 学校 [ 4 ] 行きます。学校は 九時 [ 5 ] 三時までです。

**Q94 (blank 4):**
> 1. に
> 2. を
> 3. へ
> 4. が
>
> **Answer: 3** - direction.

**Problem:** Both `に` (option 1) and `へ` (option 3) are grammatically valid for marking destination with `行く`. Standard textbook treatment:

- Genki I L3 introduces `行きます` with `に` (`大学に 行きます`) as the canonical pattern.
- `へ` is introduced later, often as an interchangeable alternative.
- Bunpro, Tofugu, and Makino & Tsutsui all describe `に` and `へ` as freely interchangeable for destination with motion verbs at N5 level. The fine-grained distinction (`に` for arrival point vs `へ` for direction) is an N4-N3 nuance.

A test-taker who has learned `に` for "go to X" (per Genki / Minna) will mark option 1 and be incorrectly graded wrong.

This is the same class of bug as the previously-fixed Q50/Q51 (`から`/`ので`) - a multiple-choice question where two of the four options are correct.

**Fix:** Replace one of `に` or `へ` with a clearly-wrong distractor. Recommended:

```
1. で  (would be 学校で 行きます - wrong; で is for location of action)
2. を
3. へ  (or に - keep one)
4. が
```

Apply the same audit to every other to-direction question that includes both `に` and `へ` as choices. The Passage A blank 4 is the one I confirmed; sweep the rest of `bunpou_questions_n5.md` and `goi_questions_n5.md` for the same pattern.

---

## 2. HIGH - inconsistencies that hurt credibility

### 2.1 `goi_questions_n5.md` Q60 and Q80 - residual "direct synonym" overclaims

The previous audit fixed Q70, Q86, Q94, Q99 to soften "Direct synonymy" rationales. Two more cases still claim direct synonymy without qualification:

**Q60:** `おおぜい ≈ たくさん (many - direct synonym for people).`

**Q80:** `暑くない ≈ すずしい (cool). Direct synonym for "not hot."`

**Problem:**

- `おおぜい` is restricted to people; `たくさん` is general (people, things, abstract). They are scope-different, not direct synonyms.
- `暑くない` (not hot) is broader than `すずしい` (cool). "Warm" (`あたたかい`) is also "not hot" but is not "cool". The relationship is implication-in-one-direction at most: cool → not hot, but not the reverse.

**Fix (parallel to the previous Q99 / Q70 / Q86 / Q94 fix):** Soften both rationales:

Q60 → `おおぜい (many people) is closest to たくさん in this context. Strictly, おおぜい is restricted to people while たくさん is general; the substitution works only when the noun is human.`

Q80 → `By elimination among the four options. Strictly, あつくない (not hot) is broader than すずしい (cool) - "warm" also qualifies as "not hot" - but the other three options are clearly wrong (opposite meaning, irrelevant property).`

### 2.2 `dokkai_questions_n5.md` - 17 of 102 question stems use non-N5 kanji

**Affected:** 妹 (5 occurrences), 家 (4), 朝 (3), 初 (2), 作 (1), 阪 (1), 図 (1), 館 (1).

**Problem:** The dokkai header documents a "naturalness exception" for **passages** but explicitly says: *"Distractor choices may contain non-N5 vocabulary where authentic JLPT distractor variety requires it"* - this exception is for distractors, not for question stems.

Question stems like `だれが ケーキを 作りますか。` use 作 (N3/N4 kanji) when the equivalent kana (つくります) is available. Other examples:

- `どうして きょうの 朝ごはんは いつもと ちがいましたか。` - 朝 not in N5 list
- `書いた 人の 妹は 何を べんきょうしますか。` - 妹 not in N5 list
- `やまださんは いつ 大阪へ 出ますか。` - 阪 not in N5 list

**Fix:** Two acceptable approaches:

1. **Document the exception:** Update the dokkai header to clarify that question stems may reuse common non-N5 kanji that appear in their corresponding passage (so the question phrasing matches the passage). Rationale: forcing 妹 → いもうと in a question that refers to a passage that says 妹 would be jarring. Add the new policy to the "Notation rules" section.

2. **Convert to kana:** Rewrite the 17 question stems to use kana for any non-N5 kanji. More work but stricter compliance with the project's stated kanji policy.

Recommend option 1 with a clear policy line: *"Question stems may reuse non-N5 kanji that appear in the passage, to keep the phrasing parallel to the source. Standalone non-N5 kanji not present in the passage are forbidden in stems."* This formalizes the practical pattern.

### 2.3 `vocabulary_n5.md` - かれ / かのじょ glosses still misleading

The previous audit flagged these glosses as having the senses backward in importance:
- `かれ - he, him (boyfriend - more advanced sense)`
- `かのじょ - she, her (girlfriend - more advanced sense)`

**Problem:** The "boyfriend / girlfriend" sense is the *common* spoken sense at N5 level. The third-person pronoun sense is more literary. Calling the boyfriend sense "more advanced" is backward from how learners actually encounter these words.

**Fix:**
```
- かれ - boyfriend; he, him (third-person; somewhat literary - Japanese normally drops the pronoun)
- かのじょ - girlfriend; she, her (third-person; somewhat literary - Japanese normally drops the pronoun)
```

This was flagged in the previous audit but doesn't appear to have been addressed.

---

## 3. MEDIUM - pedagogical clarity

### 3.1 `kanji_n5.md` 上 / 下 - kun reading lists still have mixed-N5 entries

**Current 上 entry:**
```
On: ジョウ
Kun: うえ, あ(げる)
```

**Current 下 entry:**
```
On: カ, ゲ
Kun: した, さ(げる)
```

**Note on prior fix:** The previous audit asked to drop のぼ(る) (literary form for climb) and お(りる) (which uses 降 in modern Japanese). Both ARE dropped from the current entries, which is good.

**Remaining minor issue:** 
- 上 still lists `あ(げる)` which is an N4 verb (上げる). At N5, the standalone use of 上 is overwhelmingly うえ.
- 下 still lists `さ(げる)` which is similarly N4 (下げる).

These don't actively mislead but they over-list readings that aren't tested at N5. A learner studying the 上 entry might wonder if they need to memorize あげる as a kanji-form word.

**Fix:** Optional. Add a parenthetical note or move these to a separate "extended readings" section:
```
- **上**
  - On: ジョウ
  - Kun: うえ, あ(げる) [N4+ verb - listed for recognition]
```

Or simply drop them, since the kanji entry's purpose is N5 scope.

### 3.2 `goi_questions_n5.md` - "Direct synonym" still appears beyond the 2 flagged cases

A grep for "synonym" or "Direct" in goi rationales reveals the 2 cases I flagged in §2.1 plus a few others that ARE legitimate:
- "おおぜい ≈ たくさん (direct synonym for people)" - Q60 (HIGH §2.1)
- "Direct synonym for 'not hot.'" - Q80 (HIGH §2.1)

Other Mondai 4 questions handle this correctly. Audit recommendation: search the goi file for the strings `irect synonym`, `irect equivalence`, `directly equivalent` and ensure each instance either is genuine equivalence or has a "by elimination" / "closest among the choices" softening.

### 3.3 `moji_questions_n5.md` - distractor verb forms occasionally invented

**Examples:**
- Q90: 出ます (correct) vs 入ます / 立ます / 来ます (distractors). 出ます is Group 2 → でます; 入ます/立ます/来ます are not real conjugations (the correct forms are 入ります、立ちます、来ます).
- Q91: 入ります (correct) vs 出ります / 立ります / 切ります. 出ります and 立ります are not real conjugations.
- Q92: 立ちます (correct) vs 起ちます / 経ちます / 建ちます. The latter three are real Japanese verb forms but use kanji that aren't in the N5 syllabus.

**Problem:** This is acceptable for orthography test format (the test is "which kanji belongs"), but the invented distractors could teach learners that, e.g., 出ります is a form of 出. It isn't.

**Fix:** Options:
1. Keep current form but add a one-line note in the file header: *"In orthography questions, distractor verb forms may be invented or use non-N5 kanji. The test is which kanji visually belongs - not whether the conjugation pattern is independently valid."*
2. Replace invented distractors with real conjugations using non-N5-similar kanji where possible.

Option 1 is sufficient.

### 3.4 `dokkai_questions_n5.md` Q78 - distractor uses non-N5 kanji 簡単

Q78 distractor 1: `たのしくて、簡単だった`. The kanji 簡 and 単 are N3/N4. Per the documented "distractor exception", this is allowed but visually inconsistent with the rest of the dokkai distractor pool.

**Fix (optional):** Replace with `たのしくて、らくだった` (using kana for 楽 and dropping 簡単). Lower priority - documented exception covers this.

---

## 4. LOW - polish

### 4.1 `vocabulary_n5.md` - hiragana entries could explicitly flag part-of-speech

Vocabulary entries use the format `Japanese (Reading) - English meaning`. Many verbs are listed without a part-of-speech tag, which means the runtime app can't filter "show me only verbs" without scraping the gloss.

**Suggested:** Add an optional `[noun]`, `[い-adj]`, `[な-adj]`, `[v1]`, `[v2]`, `[v3]`, `[adv]` tag where the gloss isn't self-explanatory. This is a nice-to-have for the runtime, not a correctness issue.

---

## 5. Cross-file consistency checks (recommended for CI)

These mechanical checks would catch the bulk of issues found in this and the previous markdown audit, and prevent regression:

1. **Whitelist check:** every kanji in any markdown file must be in `n5_kanji_whitelist.json`, with documented exceptions for `dokkai_questions_n5.md` passages and for moji-orthography distractors.
2. **Two-valid-answers check (semi-automated):** flag every multiple-choice question where the choices contain known "interchangeable" particle pairs (`に`/`へ` for direction, `から`/`ので` for reason, `を`/`が` with stative predicates) and the question is not specifically about that distinction. Manual review of flagged questions.
3. **Synonym overclaim check:** grep for `irect synonym`, `directly equivalent`, `same as` in all `_questions_n5.md` files. Manual review of each match.
4. **Question stem kanji policy check:** every kanji in a question stem (in `moji_questions_n5.md`, `goi_questions_n5.md`, `bunpou_questions_n5.md`) must be in the whitelist. Dokkai stems may reference passage kanji per the documented exception.
5. **Em-dash check:** `grep -P "[\x{2014}\x{2013}]" *.md` should return zero matches. **Status:** all 9 files pass.
6. **Vocabulary cross-reference:** every word used in a question stem (excluding particles, proper names, numbers, and onomatopoeia) should appear in `vocabulary_n5.md` or `n5_vocab_whitelist.json`. Currently passing for catalog files; some borderline vocab in dokkai passages (ロッカー, ひっこし) is covered by the documented exception.

---

## 6. Per-file summary

### `grammar_n5.md`
**Status:** Clean. All previously-flagged issues addressed. Section 22 terminology fix is in place. Section 6 lists Group-1 exceptions inline. The Upper N5 / borderline tier system is well-applied.

### `kanji_n5.md`
**Status:** Substantially improved. Body kanji (手, 足, 目, 口, 力) added. Reading lists trimmed to N5 scope. Two minor pedagogical-clarity items remain (3.1).

### `vocabulary_n5.md`
**Status:** Clean except for the かれ / かのじょ glosses (HIGH §2.3). Group-1 ru-verb exceptions are now flagged in both section header and per-entry. もう definition fixed.

### `sources.md`
**Status:** Clean. CEFR claim correctly softened to verifiable form. All references checked.

### `moji_questions_n5.md`
**Status:** Substantially improved. The previously-flagged Q6, Q54, Q58, Q62 all fixed. Header now documents the orthography-distractor kanji exception explicitly. One minor note (3.3) about invented verb forms.

### `goi_questions_n5.md`
**Status:** Substantially improved. Q47, Q70, Q86, Q87, Q94, Q99 all fixed. Two residual "direct synonym" overclaims remain at Q60 and Q80 (HIGH §2.1).

### `bunpou_questions_n5.md`
**Status:** Substantially improved. Q24, Q50, Q51, Q70, Q98, Q100 all fixed. **One new critical bug:** Q94 (Mondai 3 Passage A blank 4) has the same に / へ ambiguity that the project has not yet swept for (CRITICAL §1.1).

### `dokkai_questions_n5.md`
**Status:** Substantially improved. Passage F now reads ことし. Mixed-kanji forms eliminated. The kanji-policy gap in question stems remains (HIGH §2.2) but is fixable by either policy update or kana conversion.

### `authentic_extracted_n5.md`
**Status:** Clean. The provenance disclosure is now explicit: third-party scraped, NOT from JEES official samples. A planned Pass 12 to re-source from official samples is documented. This is excellent editorial discipline.

---

## 7. Recommended next-step priorities

If only 5 things get worked on next, in this order:

1. **Fix bunpou Q94 (CRITICAL §1.1).** Replace either に or へ with a wrong distractor.
2. **Sweep all bunpou and goi question files for the same に/へ pattern in any direction-verb question.** This is a class of bug; fix the class, not just the instance.
3. **Soften the two remaining "direct synonym" rationales in goi (HIGH §2.1).**
4. **Decide and document the dokkai question-stem kanji policy (HIGH §2.2).** Either formalize the exception or convert to kana.
5. **Fix the かれ / かのじょ glosses (HIGH §2.3).** Two-line edit; long-flagged.

Add the cross-file CI checks (§5) so future content additions don't regress on these patterns.

---

## 8. Acceptance criteria

This work is complete when:

1. The CRITICAL item (§1.1) and any sister cases found in the §7 step 2 sweep are fixed.
2. All HIGH items (§2.1, §2.2, §2.3) are fixed.
3. All MEDIUM items are either fixed or have an explicit defer-comment in the file.
4. The 6 cross-file consistency checks (§5) are wired into CI.
5. **A native Japanese speaker reviews the to-direction sweep results** to confirm which questions truly have ambiguous valid answers vs. which only look ambiguous.
6. Total content count remains at 100 / 100 / 100 / 102 / 189 questions across the five question files unless a question was deliberately removed with a documented justification.

---

## 9. Quick-reference issue summary

| Severity | ID | File | Issue |
|---|---|---|---|
| CRITICAL | 1.1 | bunpou_questions_n5.md | Q94 has two valid answers (に / へ); sweep needed for class |
| HIGH | 2.1 | goi_questions_n5.md | Q60, Q80 still claim "Direct synonym" when relationship is approximate |
| HIGH | 2.2 | dokkai_questions_n5.md | 17 of 102 question stems use non-N5 kanji; policy needs documenting or content needs converting |
| HIGH | 2.3 | vocabulary_n5.md | かれ / かのじょ glosses still mark boyfriend / girlfriend sense as "more advanced" - flagged in prior audit, not fixed |
| MEDIUM | 3.1 | kanji_n5.md | 上 / 下 kun lists still include N4 verb readings (あげる, さげる) |
| MEDIUM | 3.2 | goi_questions_n5.md | Audit any remaining "synonym" claims for accuracy |
| MEDIUM | 3.3 | moji_questions_n5.md | Distractor verb forms occasionally invented; document the conventionin file header |
| MEDIUM | 3.4 | dokkai_questions_n5.md | Q78 distractor uses non-N5 kanji 簡単; replace with kana variant |
| LOW | 4.1 | vocabulary_n5.md | Add optional part-of-speech tags to entries |

**Total: 9 actionable items** (1 critical, 3 high, 4 medium, 1 low).

---

## 10. Comparison with previous audits

The trajectory of issues across audit cycles:

| Audit cycle | Critical | High | Medium | Low | Total |
|---|---|---|---|---|---|
| Initial markdown audit (April 2026) | 5 | 7 | 9 | 6 | 27 |
| First JSON audit (April 2026) | 10 | 9 | 10 | 6 | 35 |
| `reading.json` focused audit (April 2026) | 5 | 5 | 6 | 4 | 20 |
| Consolidated JSON audit (May 2026) | 1 | 4 | 5 | 2 | 12 |
| **This consolidated MD audit (May 2026)** | **1** | **3** | **4** | **1** | **9** |

The trajectory is clearly positive. Most previously-flagged issues are resolved; remaining issues are pointed and well-defined. The corpus has reached a state where the next audit cycle will likely find sub-10 actionable items, and most of those will be polish-grade.

---

*End of audit. Prepared 2026-05-01.*
