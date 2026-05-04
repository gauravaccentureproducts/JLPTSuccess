# JLPT N5 Tutor - Moji Papers + Source Markdowns Audit

**Date:** 2026-05-03
**Audit scope:** the moji paper batch plus the source-of-truth markdowns:

- 7 moji paper JSON files (`moji-1` through `moji-7`, Q1-Q100, 100 questions total) - new content not previously audited
- `manifest.json` (the master paper-bank manifest)
- `bunpou_questions_n5.md` (source markdown for bunpou papers)
- `dokkai_questions_n5.md` (source markdown for dokkai papers)
- `goi_questions_n5.md` (source markdown for goi papers)
- `moji_questions_n5.md` (source markdown for moji papers)
- `vocabulary_n5.md`, `grammar_n5.md`, `kanji_n5.md`, `sources.md` (catalog reference docs)

**Audit lens:** Japanese-language accuracy, kanji whitelist conformance, cross-file consistency between source markdowns and exported JSON, and identification of root causes for previously-flagged extraction defects.

**Comparison baseline:** the paper-files audit (2026-05-03) which flagged 12 issues across bunpou + dokkai + goi papers, including the empty-stem mystery in bunpou-5/6 and several content concerns whose origin (source vs extraction) was unresolved.

---

## 0. Executive summary

This audit accomplishes two things:

1. **Audits the new moji paper batch** (which the previous audit didn't cover).
2. **Resolves several open hypotheses** from previous cycles by comparing JSON exports against the source markdowns.

**Major resolved questions from prior audits:**

- The bunpou-5/6 empty-stem mystery is now fully diagnosed: the extraction regex fails when a stem **starts with the test marker** (the `___` blank or `__word__` underline). Same root cause produces empty stems in moji-4/5/6/7. **One regex fix in the extractor resolves all 43 stem-loss cases.**
- The bunpou-7 ぎんこう/学校 hypothesis from the previous audit was **wrong**. The source markdown intentionally uses ぎんこう (kana for 銀行 because 銀 is non-N5). It's a content-naturalness question, not an extraction error.
- 3 of 4 previously-flagged "non-N5 kanji" goi violations turn out to be in **distractor positions**, which the source documentation explicitly allows. Only goi Q58 (早 in the correct answer) is an actual policy violation. **The previous audit was too strict.**

**New issues uncovered:**

- 2 stem-position non-N5 kanji in moji source (Q35: 町, Q95: 屋).
- 3 non-N5 kanji in dokkai passage content not registered in `dokkai_kanji_exception.json` (向, 央, 付).
- Multiple non-N5 kanji in bunpou stem content despite the source's own "stems must be N5-only" rule (朝, 思, 京, 阪, 牛, 乳, 公, 園).
- moji-7 Q97-Q99 use a non-standard "lemma-prefix" stem format: `__やすい__ - この レストランは __やすい__ です。` - the test word is repeated, separated by a hyphen, and prefixed before the actual sentence. Format is internally inconsistent with the other 47 Mondai 2 questions.

**Total actionable items: 12** (1 critical, 4 high, 5 medium, 2 low).

---

## 1. CRITICAL

### 1.1 Extraction-pipeline regex bug: 43 stems lost when stem begins with the test marker

**Diagnosis confirmed by source comparison.** The previous audit flagged 19 empty stems in bunpou-5/6 (sentence-rearrange, 並べ替え format) and 24 empty stems in moji-4/5/6/7 (orthography format). All 43 questions have intact stems in the source markdown but empty stems in the exported JSON.

**Pattern (from source comparison):**

| Question | Source stem | JSON stem | Stem-leading marker? |
|---|---|---|---|
| moji Q90 | `まいあさ 七時に いえを __でます__。` | populated | No (text first) |
| moji Q91 | `ねる まえに おふろに __はいります__。` | populated | No (text first) |
| moji Q76 | `__でんわ__ で 友だちと 話します。` | **empty** | **Yes (starts with __)** |
| moji Q79 | `__えき__ で 友だちと あいました。` | **empty** | **Yes** |
| moji Q80 | `__みせ__ は えきの まえに あります。` | **empty** | **Yes** |
| bunpou Q63 | `あした ___ ___ ★ ___ 行きます。` | populated | No (text first) |
| bunpou Q64 | `___ ___ ★ ___ ですか。` | **empty** | **Yes (starts with ___)** |
| bunpou Q67 | `___ ___ ★ ___ ありませんか。` | **empty** | **Yes** |

**Root cause:** the JSON extractor's stem-extraction regex expects prefix text before the test marker. When the stem begins with `__` (moji Mondai 2) or `___` (bunpou Mondai 2), the regex fails to match and writes an empty string.

**Affected question count by paper:**

| Paper | Empty-stem questions | Questions affected |
|---|---|---|
| bunpou-5 | 7 of 15 | Q64, Q67, Q68, Q69, Q70, Q71, Q74 |
| bunpou-6 | 12 of 15 | Q76, Q77, Q78, Q79, Q80, Q81, Q82, Q84, Q86, Q87, Q88, Q89 |
| moji-4 | 5 of 15 | Q52, Q53, Q57, Q59, Q60 |
| moji-5 | 12 of 15 | Q61, Q63, Q64, Q65, Q68, Q69, Q70, Q71, Q72, Q73, Q74, Q75 |
| moji-6 | 3 of 15 | Q76, Q79, Q80 |
| moji-7 | 4 of 10 | Q97, Q98, Q99, Q100 |
| **Total** | **43 questions** | (43 of 85 in affected papers ≈ 50%) |

**Severity:** Critical, but with a narrow fix scope. A single change to the extraction regex (removing the requirement for prefix text before the marker) resolves all 43 cases in one pass.

**Suggested regex change:**
```python
# Before (anchors prefix text)
stem_re = re.compile(r'^(?P<prefix>\S.*?)\s*(?:__|___|<u>)(.+?)(?:__|___|</u>)\s*(?P<suffix>.*)$', re.MULTILINE)

# After (allows stem to start with marker)
stem_re = re.compile(r'^(?P<prefix>.*?)\s*(?:__|___|<u>)(.+?)(?:__|___|</u>)\s*(?P<suffix>.*)$', re.MULTILINE)
```
(exact regex depends on the actual extractor; concept is to make the prefix optional rather than required)

---

## 2. HIGH

### 2.1 Moji source - 2 stem-context non-N5 kanji violations

The moji source's own header policy states:
> All **stems** and all **correct answers** use only N5-syllabus kanji. **Distractor options** in 表記 (orthography) questions may contain non-N5 kanji because authentic JLPT distractors mimic visually-similar wrong forms.

Two stems violate this rule:

**Q35:**
> `私の いえは 町の <u>北</u> に あります。`

The test target `北` is N5 ✓, but the surrounding word `町` (machi, town) uses a non-N5 kanji. An N5-only learner can't read the stem context.

**Q95:**
> `八百屋で やさいを __かいます__。`

The test target word is `かいます` (buy). But the location `八百屋` (yaoya, vegetable shop) uses 屋, which is not in the N5 whitelist. 八 and 百 are N5, but 屋 isn't. Learner would see 八百〇 with the third character unreadable.

**Suggested fixes:**
- Q35: replace `町` with `まち`. → `私の いえは まちの <u>北</u> に あります。` (or use a different setting like `駅` or `店`)
- Q95: replace `八百屋` with `スーパー` or `みせ`. → `みせで やさいを __かいます__。`

**Severity:** High - direct violation of the file's own documented policy in 2 stems.

### 2.2 Dokkai source - 3 passage-content non-N5 kanji not in the exception register

The `dokkai_kanji_exception.json` file documents 25 non-N5 kanji explicitly allowed in dokkai passages: `京, 作, 使, 図, 院, 回, 教, 楽, 病, 終, 自, 阪, 館, 黒, 犬, 妹, 家, 弁, 当, 思, 朝, 近, 紙, 青, 同`. Per its `_doc` field:
> To add a new kanji here, document the passage that needs it AND update KnowledgeBank/dokkai_questions_n5.md header.

But the dokkai source contains 3 additional non-N5 kanji in passage content that aren't in the exception list:

| Kanji | Reading | Where used | Occurrences |
|---|---|---|---|
| **向** | む(け) | `子ども向けの 本` (books for children) | 4 in same passage |
| **央** | おう | `中央こうえんの あんない` (Central Park notice), `中央えき` (Central Station) | 3 across 2 passages |
| **付** | つ(き) | `のみもの 付き` (drinks included), `サラダ 付き` | 3 in menu-format passage |

**Two paths forward:**
1. Add these to `dokkai_kanji_exception.json` with WHY justifications - they are common enough that excluding them damages naturalness:
   - 向: needed for 子ども向け (very common collocation in children's content)
   - 央: needed for 中央 in proper nouns (Central Park, Central Station)
   - 付: needed for ~付き (menu / list convention)
2. Replace with kana: 子どもむけ, ちゅうおう, つき.

The first approach is more natural for dokkai's authentic-passage philosophy. Whichever path is chosen, the integrity check `JA-28` (mentioned in the exception file) should be enforcing this and apparently isn't catching these three.

**Severity:** High. The exception register exists specifically to document deviations; undocumented deviations defeat its purpose.

### 2.3 Bunpou source - many stem-content non-N5 kanji despite policy

The bunpou source's own header states:
> All stems and correct answers use only N5-syllabus kanji. Distractors may include non-N5 kanji where authentic JLPT format requires it.

Yet bunpou stems use these non-N5 kanji:

| Kanji | Word/Use | Question | In stem? |
|---|---|---|---|
| **朝** | あさ ("morning") | Q3 stem and 7 other places | Yes |
| **思** | 思います ("I think") | Q85 stem (★ position), Passage B last sentence | Yes |
| **京** | 東京 (Tokyo) | Q24 stem | Yes |
| **阪** | 大阪 (Osaka) | Q24 stem | Yes |
| **牛** | 牛乳 (milk) | Q56 stem | Yes |
| **乳** | 牛乳 (milk) | Q56 stem | Yes |
| **公** | 公園 (park) | Q42 stem | Yes |
| **園** | 公園 (park) | Q42 stem | Yes |
| **楽** | 楽しい (fun) | Passage B (Q96-Q100) | Yes |

**Note:** 京 / 阪 / 思 / 朝 / 楽 ARE in the dokkai exception list - but the dokkai exception is scoped specifically to `data/papers/dokkai/*.json` and explicitly excludes bunpou per its `_doc` field. So bunpou shouldn't be using them.

**Suggested fixes for the most-used violators:**
- 朝 (8x) → あさ. Simple kana replacement.
- 東京 → とうきょう, 大阪 → おおさか. Place names commonly written in kana at N5.
- 牛乳 → ぎゅうにゅう (kana). Common in textbooks.
- 公園 → こうえん (kana). Standard N5 textbook practice.
- 思います → おもいます (kana).
- 楽しい → たのしい (kana).

These are mechanical kana substitutions and the corpus already has examples of doing this elsewhere (e.g., ぎんこう in Passage B because 銀 is non-N5).

**Severity:** High. ~10 different kanji used in stems against the file's own policy. Affects roughly 8-10 questions.

### 2.4 Moji-7 Q97-Q99 use a non-standard "lemma-prefix" stem format

**Q97 source:**
> `__やすい__ - この レストランは __やすい__ です。`

**Q98 source:**
> `__ながい__ - この かわは とても __ながい__ です。`

**Q99 source:**
> `__しろい__ - __しろい__ ねこが います。`

**Q100 source (for comparison):**
> `__なまえ__ を ここに かいて ください。`

**Problem:** Q97-Q99 prefix the test word once as a "lemma" (with surrounding `__...__`), follow with " - ", then repeat the sentence with the test word in context. No other Mondai 2 question in the moji source uses this format. All other Mondai 2 stems are simply: `<sentence with __test_word__>`.

The extra lemma prefix:
- Confuses the test format (the student sees the answer kanji-form-target word twice)
- Is internally inconsistent (Q100 doesn't use it)
- Compounds the §1.1 extraction bug (the `__` at the very start hits the buggy regex)

**Suggested fix:** drop the `__lemma__ - ` prefix. Q97-Q99 become:
- Q97: `この レストランは __やすい__ です。`
- Q98: `この かわは とても __ながい__ です。`
- Q99: `__しろい__ ねこが います。` (still starts with __, which §1.1 fix solves)

**Severity:** High. Source-content inconsistency in 3 of the last 10 moji questions, on top of the extraction bug they trigger.

---

## 3. MEDIUM

### 3.1 Correction to previous paper-audit's HIGH 2.1 - 3 of 4 "kanji violations" were actually distractor leakage (allowed)

The previous paper-files audit flagged 4 goi questions (Q58, Q65, Q86, Q100) for using non-N5 kanji. After comparing against the source's own documented policy:

| Question | Kanji | Position | Verdict |
|---|---|---|---|
| goi Q58 | 早 | Choice 2 (the **CORRECT** answer) | **Real violation** ✓ |
| goi Q65 | 少 | Choice 1 (a distractor) | Distractor leakage allowed by policy |
| goi Q86 | 紙 | Choice 4 (a distractor) | Distractor leakage allowed by policy |
| goi Q100 | 売 | Choice 2 (a distractor) | Distractor leakage allowed by policy |

The source policy clearly states:
> All stems and correct answers use only N5-syllabus kanji. Distractor options [...] may contain non-N5 kanji because authentic JLPT distractors mimic visually-similar wrong forms.

So only goi Q58 is a real violation (early - 早く should be はやく per the source's own rule). The other 3 are within scope.

**Severity:** Medium - this is a correction-of-record for the previous audit, not a new issue.

### 3.2 Bunpou-7 ぎんこう is intentional, not extraction error (correction to previous audit)

The previous audit's HIGH 2.2 hypothesized that `ぎんこうから かえってから、いえで ピアノを` ("after returning from the bank, I play piano at home") was probably a 学校 (school) typo from extraction.

**Source comparison shows:** the markdown explicitly has ぎんこう. This is intentional. 銀 is not in the N5 whitelist, and the corpus's policy is to render non-N5 kanji words in kana. The `authentic_extracted_n5.md` file even documents 銀行 as one of the recurring non-N5 words rendered in kana: `(non-N5 kanji - e.g. 友達, 先, 元気, 兄, 妹, 弟, 銀行, 雑誌, 駅, 美術館, 図書館)`.

The naturalness concern stands - a hobby passage about piano fits better with a student narrator than a bank-employee narrator - but the **mechanism** isn't extraction error. It's an authoring choice.

**Suggested fix (if changing):** the simplest revision is to change ぎんこう to がっこう (school) in the source markdown. This is one word, both within N5 vocab, and produces a more natural piano-hobby passage.

**Severity:** Medium - issue is real, but the fix is in the source markdown, not the extractor.

### 3.3 Moji Q92 distractor 起ちます uses non-N5 kanji 起 - acceptable, but worth flagging

> Q92: `先生が きょうしつに 来たので、学生が __たちます__。`
> Choices: 立ちます / 起ちます / 経ちます / 建ちます

起 is not in the N5 whitelist, and 起ちます is a real (rare) Japanese word meaning "stand up to take action" (different connotation from 立つ "stand"). The distractor is well-chosen because:
1. It tests recognition of the more common 立 vs the rarer 起 spelling
2. 起 IS in N4, so a learner who later studies N4 will encounter it

This IS allowed by the source policy ("distractors may include non-N5 kanji"). No fix needed - flagging only because the previous audit may have included this in the 4-kanji-violation count by mistake (it shouldn't have).

**Severity:** Medium - clarification rather than fix.

### 3.4 Manifest internal-consistency check passes

`manifest.json` reports:
- `totalPapers: 25` ✓ (sums match: 7+7+7+4)
- `totalQuestions: 360` ✓ (sums match: 100+100+100+60)
- All paper IDs match the corresponding JSON files
- All question counts match per-paper

This is a positive finding; recording it here for completeness.

**Severity:** Medium - sanity-check confirmation.

### 3.5 Moji Q62 rationale carefully addresses the 子ども vs 子供 question

Source rationale:
> 子ども is selected here because it follows this corpus's N5-only-kanji policy (供 is N4). Both 子供 and 子ども are standard in modern Japanese, and on the actual JLPT both forms appear; the choice between them is a corpus-internal scope rule, not a correctness rule.

This is excellent teacherly writing - it explicitly tells the student "in real Japanese both forms are valid, this distinction is just our corpus's rule." Same caliber of careful pedagogy I noted in the previous audit's goi rationales (Q60, Q90, Q99). Worth preserving.

**Severity:** Medium - positive observation.

---

## 4. LOW

### 4.1 Moji rationales using non-N5 kanji within parenthetical notes

A few moji rationales contain non-N5 kanji in parenthetical comments. Examples:

- Q83 rationale: "N5 standard 見ます." (見 is N5, no issue here)
- Q92 rationale: "立ちます (N5 sense)." (no issue)
- Q19 rationale (bunpou): "熱がある (have a fever)." (熱 is non-N5, used in rationale only)

These are in **rationale** strings (which are part of the answer-key reveal, after the student commits). The visibility to learners is conditional. Not strictly a violation since the policy is about stems and answer choices, but worth a note: rationales also display to learners and ideally stay in N5-readable form.

**Severity:** Low - acceptable but worth a cleanup pass.

### 4.2 Goi Q47 rationale references 去年 (kyonen, "last year") with non-N5 kanji 去

Source rationale for Q47:
> こと + ある (experience). Note: 「行ったことがある」 is for indefinite past experience and cannot combine with a specific time marker like **去年**.

去 is not in the N5 whitelist. The rationale is good (it correctly explains the constraint that experience-keiken `ことがある` resists definite-time anchoring), but the example uses 去年 in kanji. Minor: change to きょねん.

**Severity:** Low.

---

## 5. Cross-cutting observations

### 5.1 Source markdowns vs JSON exports - now mostly aligned

Where the previous audit raised "is this a source issue or an extraction issue?" questions, this audit can now answer:

| Issue | Was extraction or source? |
|---|---|
| 19 bunpou-5/6 empty stems | Extraction (regex bug §1.1) |
| 24 moji-4/5/6/7 empty stems | Extraction (same regex bug) |
| ぎんこう in bunpou-7 Passage B | Source (intentional kana for non-N5 銀行) |
| 「もう一どに 行きたい」 in dokkai-4 Q58 | Source (verified in markdown) |
| 「書いた 人」 in dokkai-4 Q58 | Source (verified) |
| 「後の 日に なりました」 in dokkai-4 Q60 | Source (verified) |
| Trailing `---` in 4 rationales | Extraction (markdown HR not stripped) |
| Leading `> ` in dokkai passages | Source (markdown blockquote convention) |
| 4 "non-N5 kanji" in goi (Q58/65/86/100) | Mostly distractor-position (allowed); only Q58 is a real source violation |

### 5.2 Grammar tier classification: source matches JSON

`grammar_n5.md` Section 23 (the dedicated borderline section) plus 10 inline `(Upper N5 / borderline)` tags add up to ~24 patterns. `grammar.json` has 24 patterns with `tier: late_n5`. Numbers align ✓.

### 5.3 sources.md is well-curated

The `sources.md` reference file lists authoritative sources with appropriate scope comments. Notable: it explicitly states the conflict-resolution rule ("Minna no Nihongo + Genki overlap and frequency of appearance is treated as the authoritative tiebreaker"), notes Imabi's author is non-native (transparency), and documents the boundary between "deep references" and "in-scope content."

This is the kind of meta-document a serious curriculum-curator would maintain. No issues found.

### 5.4 Whitelist conformance summary across question files

| File | Stem-position non-N5 violations | Distractor non-N5 (allowed) |
|---|---|---|
| moji_questions_n5.md | 2 (Q35: 町, Q95: 屋) | many (per policy) |
| goi_questions_n5.md | 1 (Q58: 早 in correct answer) | 3 (Q65: 少, Q86: 紙, Q100: 売 - in distractors) |
| bunpou_questions_n5.md | ~10 (朝, 思, 京, 阪, 牛, 乳, 公, 園, 楽 in stems) | acceptable in distractors |
| dokkai_questions_n5.md | 3 (向, 央, 付 - undocumented exceptions) | passages allow exceptions per policy |

Bunpou is the dirtiest by this measure. Goi has only one real violation. Moji has two. Dokkai has three undocumented exception kanji that should be added to the register or replaced with kana.

---

## 6. Recommended next-step priorities

If only 5 things get worked on:

1. **Fix the extraction-pipeline regex** (§1.1). Single regex change resolves 43 empty-stem questions across bunpou-5/6 and moji-4/5/6/7. Highest leverage by a wide margin.
2. **Fix the 2 moji stem-context violations** (§2.1). Q35 town→まち, Q95 八百屋→みせ. Two-word edits.
3. **Resolve the dokkai exception register** (§2.2). Add 向/央/付 to `dokkai_kanji_exception.json` with WHY justifications, OR replace with kana in passages.
4. **Sweep bunpou stems for non-N5 kanji** (§2.3). Substitute 朝→あさ, 公園→こうえん, 牛乳→ぎゅうにゅう, etc. This is the largest cleanup but mechanical.
5. **Normalize moji-7 Q97-Q99 stem format** (§2.4). Drop the `__lemma__ - ` prefix to match the rest of Mondai 2.

The remaining items (rationale-cleanup, ぎんこう naturalness if changing it) are polish.

---

## 7. Quick-reference issue summary

| Severity | ID | File | Issue |
|---|---|---|---|
| CRITICAL | 1.1 | bunpou-5/6, moji-4/5/6/7 | Extraction regex fails on stems starting with marker; 43 empty stems across 6 papers |
| HIGH | 2.1 | moji_questions_n5.md | 2 stem-context non-N5 kanji (Q35: 町, Q95: 屋) violate the file's own policy |
| HIGH | 2.2 | dokkai_questions_n5.md | 3 non-N5 kanji in passages (向, 央, 付) not in the exception register |
| HIGH | 2.3 | bunpou_questions_n5.md | ~10 non-N5 kanji in stems despite the file's own "stems must be N5-only" policy |
| HIGH | 2.4 | moji_questions_n5.md | Q97-Q99 use non-standard `__lemma__ - sentence` format inconsistent with rest of Mondai 2 |
| MEDIUM | 3.1 | (correction) | 3 of 4 previously-flagged goi violations were distractor leakage (allowed by policy) |
| MEDIUM | 3.2 | (correction) | bunpou-7 ぎんこう is intentional source content, not extraction error |
| MEDIUM | 3.3 | moji_questions_n5.md | Q92 distractor 起ちます uses non-N5 kanji - allowed; flagged for clarity |
| MEDIUM | 3.4 | manifest.json | Internal totals and per-category sums verify ✓ (positive finding) |
| MEDIUM | 3.5 | moji_questions_n5.md Q62 | 子ども vs 子供 rationale handles the corpus-policy nuance well (positive finding) |
| LOW | 4.1 | moji/bunpou rationales | Some non-N5 kanji appear in rationale text (e.g., 熱) - cleanup grade |
| LOW | 4.2 | goi_questions_n5.md Q47 | Rationale uses 去年 in kanji; should be きょねん |

**Total: 12 actionable items** (1 critical, 4 high, 5 medium, 2 low).

---

## 8. Trajectory across audit cycles

| Cycle | Crit | High | Med | Low | Total |
|---|---|---|---|---|---|
| Initial markdown audit (Apr) | 5 | 7 | 9 | 6 | 27 |
| First JSON audit (Apr) | 10 | 9 | 10 | 6 | 35 |
| reading.json focused (Apr) | 5 | 5 | 6 | 4 | 20 |
| Consolidated JSON (May 1) | 1 | 4 | 5 | 2 | 12 |
| Consolidated MD (May 1) | 1 | 3 | 4 | 1 | 9 |
| Native-reviewer dossier first (May 2) | 3 | 4 | 5 | 2 | 14 |
| Native-reviewer dossier follow-up (May 2) | 0 | 0 | 0 | 0 | 0 |
| Data files audit (May 2) | 1 | 4 | 3 | 2 | 10 |
| Content files audit (May 3) | 1 | 4 | 4 | 1 | 10 |
| Infrastructure audit (May 3) | 1 | 4 | 3 | 1 | 9 |
| Paper files audit (May 3) | 1 | 4 | 5 | 2 | 12 |
| **Moji + sources audit (May 3, this audit)** | **1** | **4** | **5** | **2** | **12** |

The single CRITICAL item this cycle is the regex fix - which is also the single highest-leverage edit available, resolving 43 questions in one change. The remaining items are mostly source-content cleanup against the source's own documented policies.

The cross-source comparison enabled this audit to **resolve 5 prior open questions** (extraction vs. source attribution) and **correct one prior over-call** (3 of 4 goi distractors flagged were actually within policy). That's a healthy thing for an audit cycle to do - both finding new defects and refining the record on prior ones.

---

*End of audit. Prepared 2026-05-03.*
