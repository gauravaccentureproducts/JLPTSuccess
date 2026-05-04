# JLPT N5 Tutor - Content Files Audit (grammar / listening / reading)

**Date:** 2026-05-03
**Audit scope:** three content JSON files in their current state:
- `grammar.json` (177 patterns, 500 KB)
- `listening.json` (40 items, 31 KB - up from 30)
- `reading.json` (40 passages, 74 KB - up from 30)

**Audit lens:** Japanese-language accuracy from a seasoned 日本語教師's perspective, plus schema-completeness and policy-compliance checks against prior audit baselines.

**Comparison baselines:**
- Data files audit (2026-05-02): identified 10 items including the n5-134 ので tier issue, broken cross-refs, and 8 grammar em-dashes.
- reading.json focused audit (April 2026): 20 items.

---

## 0. Executive summary

Most prior issues are now resolved, and the new content (10 reading passages and 10 listening items added since the last cycle) is generally of good quality. The corpus is in better shape than at the previous cycle's checkpoint.

**Verified resolved since the previous data-files audit:**

- **n5-134 (ので) is now `tier: late_n5`** ✓ - the previously-flagged HIGH 2.3 tier inconsistency.
- **Zero broken cross-references** ✓ - both `contrasts.with_pattern_id` and `form_rules` see-also fields no longer point to the 10 retired patterns. HIGH 2.2 fully resolved.
- **Em-dashes in grammar.json reduced from 8 to 4** ✓ - half the policy-violation strings have been fixed (translation_en cases for n5-129 and n5-167; the remaining 4 are in `common_mistakes.why` text).
- **All previously-fixed reading passages hold** ✓ - n5.read.001 (space), n5.read.007 (potential form), n5.read.010 (こ counter), n5.read.018 (たんご), n5.read.022 (よろこぶ→言いました), n5.read.024 (日本語), n5.read.026 (いくつ), n5.read.029 (高い), n5.read.030 (te-form), all confirmed.
- **n5.listen.011 (polite refusal)** is now internally consistent (script + prompt + choices align) ✓.
- **All 40 reading passages stay within the N5 kanji whitelist** ✓.
- **All 40 reading passages have `tier`** and **all questions have `format_role`** ✓.

**Trajectory:**

| Audit cycle | Crit | High | Med | Low | Total |
|---|---|---|---|---|---|
| Initial markdown audit (Apr) | 5 | 7 | 9 | 6 | 27 |
| First JSON audit (Apr) | 10 | 9 | 10 | 6 | 35 |
| reading.json focused (Apr) | 5 | 5 | 6 | 4 | 20 |
| Consolidated JSON (May 1) | 1 | 4 | 5 | 2 | 12 |
| Consolidated MD (May 1) | 1 | 3 | 4 | 1 | 9 |
| Native-reviewer dossier first (May 2) | 3 | 4 | 5 | 2 | 14 |
| Native-reviewer dossier follow-up (May 2) | 0 | 0 | 0 | 0 | 0 |
| Data files audit (May 2) | 1 | 4 | 3 | 2 | 10 |
| **Content files audit (May 3)** | **1** | **4** | **4** | **1** | **10** |

**Total actionable items: 10** (1 critical, 4 high, 4 medium, 1 low). Most of these concentrate on the 10 newly added reading passages (031-040) and 10 listening items (031-040) where authoring quality is good but a few seams show.

---

## 1. CRITICAL

### 1.1 reading.json - schema regression: 10 new passages missing `kanji_used` and `vocab_used`

**Affected:** all 10 of `n5.read.031` through `n5.read.040`.

**Problem:** the prior 30 passages (n5.read.001-030) all carry two metadata arrays:

```json
"kanji_used": ["今", "大", "学", "日", "本", "来", "見", "語"],
"vocab_used": ["いま", "えいが", "おねがいします", ...]
```

These power any feature that depends on knowing which kanji or vocab a passage exercises - lesson sequencing, kanji-readiness gating, "find passages that use this word" search, vocabulary-coverage analytics. The `_meta.schema_additions` field documents these as part of the formal schema:

```
"schema_additions": "passages[].tier (core_n5|late_n5|info_search), 
                     passages[].format_type (info-search only: schedule_table|menu_list), 
                     passages[].questions[].format_role (primary|extra)."
```

The new passages 031-040 added the three documented additions (tier, format_type, format_role) correctly, but skipped kanji_used and vocab_used - which were already part of the schema before this round of additions.

**Severity:** Critical. Schema completeness regression on 25% of the passage corpus. Any feature that does `passage.kanji_used.includes(...)` will silently miss the new passages.

**Suggested fix:** generate kanji_used and vocab_used from each new passage's `ja` text using the same extraction logic that produced the fields for passages 1-30. This is a build-time step, not authoring work.

---

## 2. HIGH

### 2.1 reading.json n5.read.033 - factually awkward content claim

**Passage `とうきょうの あき`:**
> とうきょうの あきは とても きれいです。木の はが あかや きいろに なります。すずしくて、さんぽが たのしいです。**あさは 七時ごろ、そらが あかいです。**とりの こえも 聞こえます。あきは わたしの すきな きせつです。

**Problem:** "In the morning around 7am, the sky is red." Tokyo autumn sunrise occurs roughly 5:30-6:00 am, after which the sky turns from red/orange to pale blue within 30-60 minutes. By 7am the sky is normally light blue. The claim "そらが あかいです" at 7am isn't grammatically wrong, but a native reader will pause - this isn't how autumn mornings look in Tokyo.

The passage seems to be reaching for romantic imagery (autumn + red sky) but conflates sunset/sunrise timing. Two natural fixes:

- **Move to evening:** `ゆうがた、そらが あかいです` ("In the evening, the sky is red"). Autumn sunsets ARE red and around 5pm, which fits with afterschool walks.
- **Move time earlier:** `あさは 五時ごろ、そらが あかいです` ("At about 5am, the sky is red"). Matches actual Tokyo autumn sunrise.
- **Substitute imagery:** `あさひが きれいです` ("The morning sun is beautiful") - keeps the morning frame without the meteorological awkwardness.

**Severity:** High. Not a Japanese-language error, but a content credibility problem in a reading passage that students will read carefully looking for the answer.

### 2.2 reading.json - vocab leakage in 10 new passages (11+ items not in N5 whitelist)

The new passages introduce vocabulary not present in the project's `vocabulary_n5.md` whitelist. Some of this is unavoidable (proper-noun-like loanwords, thematic vocabulary), but the count is significant:

| Passage | Out-of-whitelist vocab | Notes |
|---|---|---|
| n5.read.032 | アルバイト, ためる | アルバイト is N5/N4 borderline; ためる is N4 |
| n5.read.033 | 聞こえる | N4 (potential/spontaneous form of 聞く) |
| n5.read.036 | りか (Q distractor) | 理科 = N4 vocab |
| n5.read.037 | おくれる, つく | both N4-borderline; "電車が おくれる" is functional N5 collocation |
| n5.read.038 | コンサート | not in whitelist; common loan |
| n5.read.039 | セール, おしらせ, ぜひ, ばい (倍 counter), ただ (Q distractor) | ぜひ is N4; ばい is N4 counter; ただ "free" is N4 |
| n5.read.040 | ベンチ | not in whitelist; common loan |

**Problem:** the project has historically been strict about staying within the vocab whitelist for passage text, with distractors permitted to leak. Several of these (アルバイト, 聞こえる, ためる, ぜひ, ばい, おくれる) appear in passage TEXT, not just in distractors.

This is a policy question more than a Japanese-language error. The new passages would all comfortably pass an external N5 reader. But against the project's documented "strict whitelist" policy, they regress.

**Two ways forward:**

- **Tighten:** rewrite passages to use only whitelist vocab (e.g., n5.read.032 substitute "しごと" for "アルバイト"; n5.read.039 substitute "やすい" for "半分の ねだん" etc.).
- **Loosen:** update `vocabulary_n5.md` to include the genuinely-N5 items (アルバイト, セール, ベンチ, コンサート, おじゃまします are common-enough loanwords/expressions that N5 textbooks DO include them) and tier the others as late_n5 vocab.

Most other JLPT N5 source materials accept all of these as N5-appropriate. So if the project's whitelist is more conservative than typical N5, that's a project choice - but it should be applied consistently or relaxed deliberately.

**Severity:** High (policy-compliance scope creep on new content; not a language error).

### 2.3 listening.json n5.listen.036 - 三日かん vs 三日間 orthographic inconsistency

**Script:**
> 男の人が しごとの あとで 話して います。
> 来月の 七日から 九日まで、おおさかに 行きます。**三日かんの** りょこうです。新かんせんで 行きます。

**Question:** りょこうは **何日かん**ですか。

**Problem:** the kanji 間 IS in the N5 kanji whitelist (verified). The project's documented orthography policy is "use kanji where N5 allows." Other passages and listening items use 間 as a standalone kanji (e.g., 一週間 in n5.read.038 where it's still spelled 一週間 with kanji). Here, 三日**かん** spells 間 in kana for no defensible reason.

The same passage spells 新**かん**せん with kana for 幹 - which IS correct because 幹 is NOT in the N5 whitelist.

The fix: change 三日かん to 三日間 in both script and question prompt. Same for any other 〜かん usages in the corpus.

**Severity:** High (internal orthographic inconsistency; user will see 三日かん one place and 一週間 another).

### 2.4 listening.json n5.listen.034 - em-dash and curly apostrophe in explanation

**Two policy violations in a single explanation:**
```json
"explanation_en": "'はやく かおを あらって' — wash face first, then breakfast."
```
> uses U+2014 em-dash (project policy: forbidden)

```json
"explanation_en": "おじゃまします is the polite phrase when entering someone's home or place."
```
> uses U+2019 right single quotation mark (curly apostrophe) instead of ASCII U+0027

The `someone's` curly apostrophe (`’`) is in n5.listen.038's explanation, not 034. The em-dash is in 034.

**Severity:** High (style policy compliance; same class of issue as the previously-flagged grammar.json em-dashes; trivially fixable).

---

## 3. MEDIUM

### 3.1 grammar.json - 4 em-dashes still remain in `common_mistakes.why`

The previous data-files audit flagged 8 em-dashes in grammar.json. 4 are now fixed (the translation_en ones); 4 remain in `common_mistakes.why` strings:

```
"why": "いつも is \"always\" — does not pair with negation. Use ぜんぜん..."
"why": "...colloquial and overused — pick one in clean speech."
"why": "\"I want to eat something\" is affirmative — use なにか, not なにも."
"why": "\"Want to go somewhere\" is affirmative wish — use どこか."
```

**Severity:** Medium (incomplete cleanup of a previously-flagged item).

### 3.2 reading.json n5.read.034 - "たのしい ですから" register clunkiness

**Letter text:**
> たのしい ですから、来て ください。

**Problem:** i-adjective + ですから is grammatically valid but reads awkwardly in a casual letter from one student to another. The space between たのしい and ですから makes it read as two separate words. More natural alternatives in this context:

- `たのしいですから、来て ください。` (no space, more polite)
- `たのしいから、来て ください。` (plain causal から - fits the casual letter register better)
- `おもしろいですから、来て ください。` or `おもしろいですよ。来て ください。`

Also worth noting: the title `友だちからの てがみ` ("letter from a friend") frames this as the recipient's view, but the letter's signature is `たなか` (Tanaka). So the perspective is "Yamada is reading a letter from Tanaka." This works, but the title might be clearer as `たなかさんからの てがみ` or `ともだちの てがみ`.

**Severity:** Medium (register/style; not wrong).

### 3.3 reading.json n5.read.032 - tier classification question

**Passage `アルバイト`:** tier=core_n5, level=medium.

**Content includes:**
- `アルバイト` (N5/N4 borderline loanword)
- `アルバイトを して います` (te-iru duration)
- `お金を ためて、来年 日本に 行きたいです` (te-form chain + tai-form)

The grammar is core_n5. The vocab leans N5/N4 borderline (アルバイト, ためる). Compare to the 3 existing late_n5 passages (013 きょうとへの りょこう, 018 日本語の べんきょう, 025 土よう日の あさ) - those have similar grammar density but cleaner vocab.

This passage might fit better as `tier: late_n5` given the borderline vocab. Not strictly wrong as core_n5 but the tier-distinction signal is muddied.

**Severity:** Medium (tier-classification judgement call; affects late_n5 surfacing).

### 3.4 listening.json - listening items 031-040 borderline vocab leakage

Parallel to §2.2 in reading. The new listening scripts contain N4-borderline vocab not in the N5 whitelist:

| Item | Borderline vocab |
|---|---|
| n5.listen.031 | 「いいかな」particle stack (かな is N4) |
| n5.listen.032 | 週まつ (週末 = N5/N4 borderline) |
| n5.listen.033 | フロント (loanword, not in whitelist) |
| n5.listen.034 | じゅんび (N4-borderline) |
| n5.listen.035 | こくせき (国籍 = N4) |
| n5.listen.036 | 新かんせん (新幹線 - previously flagged in bunpou Q24) |
| n5.listen.038 | おじゃまします (set phrase, not in greetings whitelist) |
| n5.listen.039 | はらう (N4-borderline) |

Same recommendation as §2.2: either tighten (rewrite to whitelist) or loosen (expand whitelist deliberately). The listening genre is more forgiving than reading (real-world listening always exposes more vocab than the test-taker has formally studied), so a relaxed policy is more defensible here.

**Severity:** Medium (same class as 2.2; mentioned separately for completeness).

---

## 4. LOW

### 4.1 reading.json - mixed orthography for 「日にち」in n5.read.039

**Sign text:**
```
日にち：八月一日から 八月七日まで
```

The word 日にち (date) mixes 日 (kanji) with にち (kana). In real Japanese signage this DOES occur, but the more standard convention for a notice would be either `日付`(ひづけ - 付 not in N5 whitelist so this is excluded), or simply `日：` followed by the date range, or the colloquial `日にち：`.

The current rendering is acceptable colloquial Japanese but slightly unusual. Not actionable - just worth noting.

**Severity:** Low (style preference).

---

## 5. Cross-cutting good news

Items where the trajectory continues to be positive:

- **Zero non-N5 kanji** in any reading passage, listening script, or grammar example.
- **Zero broken vocab_id references** between grammar.json and vocab.json (was 0 last audit, still 0).
- **All 40 listening items have explanation_en**, all 40 have prompt_ja, all 40 have non-empty choices.
- **All 40 reading passages have tier and audio fields** populated.
- **The previously-flagged ので tier issue is cleanly fixed** (now `tier: late_n5`, joining the 24 other late_n5 patterns for a total of 25 - which matches the project's source markdown borderline tagging).

The corpus continues to mature in the right direction. The new content is good quality - the 10 issues found are mostly rough edges on the new authoring rather than systemic problems.

---

## 6. Recommended next steps

If only 5 things get worked on:

1. **Add kanji_used and vocab_used to passages 031-040** (§1.1). Build-time generation, not authoring.
2. **Fix n5.read.033's 七時ごろ red sky** (§2.1) - move to ゆうがた or restructure imagery.
3. **Decide on the vocab whitelist policy** (§2.2 + §3.4) - either rewrite the new passages to fit, or expand the whitelist to include the genuinely-N5 loanwords. Recommend the latter; document any additions in `vocabulary_n5.md` and re-audit the older passages for any vocab that should now be added.
4. **Fix 三日かん → 三日間** in n5.listen.036 (§2.3). Two-character change.
5. **Sweep remaining grammar.json em-dashes and the listening 034 em-dash + 038 curly apostrophe** (§2.4 + §3.1). Six character replacements total.

The remaining items (n5.read.034 register, n5.read.032 tier judgement, 日にち orthography) are polish-grade.

---

## 7. Quick-reference issue summary

| Severity | ID | File | Issue |
|---|---|---|---|
| CRITICAL | 1.1 | reading.json | 10 new passages (031-040) missing kanji_used and vocab_used arrays that all prior 30 have |
| HIGH | 2.1 | reading.json | n5.read.033 claims そらが あかい at 7am autumn morning - meteorologically off |
| HIGH | 2.2 | reading.json | New passages 031-040 leak ~11 N4-borderline vocab not in whitelist |
| HIGH | 2.3 | listening.json | n5.listen.036 spells 三日かん in kana when 間 IS in N5 whitelist |
| HIGH | 2.4 | listening.json | n5.listen.034 has em-dash in explanation; n5.listen.038 has curly apostrophe |
| MEDIUM | 3.1 | grammar.json | 4 em-dashes remain in common_mistakes.why (down from 8) |
| MEDIUM | 3.2 | reading.json | n5.read.034 "たのしい ですから" register slightly clunky for casual letter |
| MEDIUM | 3.3 | reading.json | n5.read.032 (アルバイト) should arguably be tier=late_n5 given vocab |
| MEDIUM | 3.4 | listening.json | New items 031-040 leak similar N4-borderline vocab |
| LOW | 4.1 | reading.json | n5.read.039 mixes 日にち orthography (acceptable colloquial) |

**Total: 10 actionable items** (1 critical, 4 high, 4 medium, 1 low).

---

*End of audit. Prepared 2026-05-03.*
