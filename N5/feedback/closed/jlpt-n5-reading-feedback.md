# JLPT N5 Tutor - reading.json Content Audit

**Audit scope:** `reading.json` - 30 graded reading passages with 63 comprehension questions, plus their English translations and answer explanations.
**Audit lens:** Japanese-language accuracy from a seasoned Japanese teacher's perspective. Kanji rendering compliance, grammar scope (N5 vs N4 leakage), vocabulary scope, internal consistency between passages and explanations, naturalness of Japanese, and JLPT format fidelity.
**Comparison baseline:** Prior audit of an earlier version that flagged 13 of 30 passages with kanji-whitelist violations.

---

## 0. Executive summary

The corpus is in noticeably better shape than the prior version. The kanji-whitelist enforcement work has landed: **all 30 passages now use only kanji from `n5_kanji_whitelist.json`**, with zero violations. This was the largest issue in the previous audit; it is resolved.

The remaining issues split into:

- **Mechanical (15 of 20 issues):** rendering consistency between passages and explanations, a small number of typos, three or four scope-creep violations on grammar/vocab. All findable and fixable in a single editing pass.
- **Structural (5 issues):** info-search passages lack a format-type field; several common N5 vocabulary items are missing from the whitelist; question-count-per-passage diverges from JLPT format. These need a small schema decision before editing.

Total actionable items: 20 (5 critical, 5 high, 6 medium, 4 low).

**What's notably good:**

- Kanji whitelist enforcement is now clean across all passages.
- Passage length distribution (62-97 chars, avg 79) is appropriate for N5 short-text reading.
- Topic diversity is strong (19 distinct topics across 30 passages).
- All 3 info-search passages match the JLPT Mondai 6 format conceptually.

---

## 1. CRITICAL - factual errors that mislead a learner

### 1.1 `n5.read.029` Q1 - explanation misquotes the passage

**Passage states:**
> 毎日 30どより 高いです。

**Q1 explanation claims to quote:**
> '毎日 30どより 上です'

**Problem:** The phrase `30どより 上` does not appear in the passage. The passage uses `高い` (high). The two are semantically equivalent at N5 level, but the explanation is presented as a direct quote with single-quote marks, which is misleading. The learner will scan the passage looking for `上` and not find it.

**Fix:** Update Q1 explanation to:
```
"explanation_en": "'毎日 30どより 高いです'."
```

### 1.2 `n5.read.010` Q1 - explanation produces ungrammatical Japanese

**Passage states:**
> つくえが 25こ あります。

**Q1 explanation claims to quote:**
> 'つくえが 25あります'

**Problem:** The explanation drops the `こ` counter, producing a sentence that no native speaker would say. You can't have a bare numeral modifying `あります` for a noun like `つくえ` without a counter. This actively teaches the learner that bare numbers can stand alone, which is wrong.

**Fix:** Update Q1 explanation to:
```
"explanation_en": "'つくえが 25こ あります'."
```

### 1.3 `n5.read.010` Q1 - answer choices missing the counter

**Q1 choices (current):**
- `10`
- `15`
- `20`
- `25` (correct)

**Problem:** The passage uses `25こ`, the question asks `いくつ ありますか`, but the four choices are bare numbers. This is inconsistent with the passage and with sister-passage `n5.read.026` (Q1 choices: `1つ / 2つ / 3つ / 5つ` correctly using the counter `つ`).

**Fix:** Update choices to:
```
"choices": ["10こ", "15こ", "20こ", "25こ"]
"correctAnswer": "25こ"
```

### 1.4 `n5.read.007` Q2 - prompt uses N4 grammar (potential form)

**Q2 prompt:**
> 本は どのくらい かりられますか。

**Problem:** `かりられる` is the potential form of `かりる`. Potential form is firmly N4 grammar in standard syllabi (Genki II L13, Minna II L27, Bunpro N4). The passage itself wisely uses the N5-appropriate `かりる ことが できます` construction. The question prompt then introduces N4 grammar that the learner cannot be expected to know.

**Fix:** Rewrite Q2 prompt to match the passage's grammar level:
```
"prompt_ja": "本は どのくらい かりる ことが できますか。"
```

### 1.5 `n5.read.030` - passage uses `〜と` conditional (N4 grammar)

**Passage states:**
> 100メートルくらい あるくと、左に ゆうびんきょくが あります。

**Problem:** The `〜と` conditional ("when X happens, Y happens") is N4 grammar. Standard sources: Genki II L18, Minna I L23, Bunpro categorizes it as N4. At N5, the same idea is expressed with the te-form imperative or with two separate sentences.

**Fix:** Rewrite to use N5 grammar:
```
"ja": "えきの 出口を 出て、まっすぐ 行きます。はじめの しんごうを 右に まがります。100メートルくらい あるいて ください。左に ゆうびんきょくが あります。あいています：月〜金の 9時から 17時まで。"
```

This replaces `あるくと` (N4 conditional) with `あるいて ください` (N5 te-form imperative) followed by a new sentence.

---

## 2. HIGH - inconsistencies that hurt credibility

### 2.1 `n5.read.022` - uses N3 vocabulary `よろこぶ`

**Passage states:**
> 父も あにも よろこびました。

**Problem:** `喜ぶ / よろこぶ` ("to be glad / pleased") is N3 vocabulary, not N5. The corpus is otherwise disciplined about vocab scope; this slips through. At N5, the same idea is expressed with `うれしい`, `〜と 言いました`, or `たのしかった`.

**Fix:** Rewrite the final sentence with N5 vocab. Suggested:
```
"ja": "...父も あにも 'おいしい' と 言いました。"
```

Or:
```
"ja": "...かぞくは みんな たのしかったです。"
```

### 2.2 Passage-vs-explanation rendering inconsistency (8 occurrences)

**Affected items:**

| Passage uses | Explanation uses | Found in |
|---|---|---|
| `とうきょう` | `東京` | `n5.read.001.q2` |
| `うち` | `家` | `n5.read.002.q3`, `n5.read.008.q1`, `n5.read.008.q2`, `n5.read.016.q1`, `n5.read.022.q2` |
| `かえって` | `帰って` | `n5.read.002.q3` |
| `きょうと` | `京都` | `n5.read.013.q1` |

**Problem:** The explanations claim to quote the passage but use kanji forms that the passage does not contain. The learner reads the explanation, scans the passage for the quoted phrase, doesn't find it, and concludes either (a) the explanation is wrong, or (b) they read the passage incorrectly. Both outcomes hurt trust.

**Fix:** Audit every explanation field against its passage and ensure the rendering matches. Where the explanation needs to refer to a phrase, it must use the exact same kana/kanji rendering the passage uses.

Quick approach: search the dataset programmatically for explanation text that contains kanji not in the corresponding passage, and either update the explanation or update the passage.

### 2.3 `n5.read.024` Q2 - prompt uses inconsistent rendering

**Q2 prompt:**
> マリアさんは 日本ごが どうですか。

**Passage uses:** `日本語` (kanji throughout)

**Problem:** The prompt switches `語` to its kana form `ご`, mid-word. Both `日`, `本`, and `語` are in the N5 kanji whitelist, so this is gratuitous. The mixed form is also visually awkward.

**Fix:** Update the Q2 prompt to use the same form as the passage:
```
"prompt_ja": "マリアさんは 日本語が どうですか。"
```

### 2.4 `n5.read.001` - missing space in passage

**Passage states:**
> 今、とうきょうの大学で 日本語を べんきょうしています。

**Problem:** No space between `とうきょうの` and `大学`. Compare `n5.read.024`: `今、とうきょうの 大学で べんきょうしています` - with a space. The corpus's spacing convention is consistently to insert a space at every word boundary, except this one.

**Fix:** Update passage to:
```
"ja": "わたしは アンナです。アメリカから 来ました。今、とうきょうの 大学で 日本語を べんきょうしています。しゅみは えいがを 見ることです。どうぞ よろしく おねがいします。"
```

### 2.5 `n5.read.026` - English typo

**Translation states:**
> It was very very cheap.

**Fix:** Remove the duplicated word:
```
"translation_en": "I bought fruit at the greengrocer. I bought 3 apples and 5 bananas. The total was 700 yen. It was very cheap."
```

---

## 3. MEDIUM - pedagogical clarity

### 3.1 `n5.read.018` Q2 - distractor uses non-N5 vocabulary

**Q2 choices:**
- `ひらがな`
- `かたかな`
- `かんじ` (correct)
- `はつおん` (= 発音, "pronunciation")

**Problem:** `はつおん` is not in `n5_vocab_whitelist.json` and is not on standard N5 vocab lists (it's typically N4). The corpus is disciplined about vocab scope elsewhere; this distractor leaks higher-level vocab into an N5 question.

**Fix:** Replace with a clearly N5 distractor:
```
"choices": ["ひらがな", "かたかな", "かんじ", "たんご"]
```

(`たんご` = vocabulary words. Or use `かいわ` = conversation.)

### 3.2 `n5.read.025` - uses `〜たい + N` modifier (late-N5 / early-N4 boundary)

**Passage states:**
> よみたい 本も よみます。

**Problem:** Using `たい`-form as a noun modifier (`よみたい 本` = "books I want to read") is taught at the boundary of late N5 and early N4 in most textbooks. The construction itself is grammatical, and individual elements (`たい` form, noun modification) are both N5. But the *combination* is borderline.

**Decision needed:** Either accept this as in-scope and tag the passage as `late-n5`, or rewrite. If keeping, leave as-is. If rewriting:
```
"ja": "...それから、すきな 本を よみます。土曜日が 大すきです。"
```

### 3.3 `n5.read.018` - `1年前から + ています` (durative usage)

**Passage states:**
> わたしは 1年前から 日本語を べんきょうしています。

**Problem:** The "have been [verb]ing for [time period]" construction is more naturally an N4 pattern. Each individual element (`〜から`, `〜ています`) is N5, but the durative meaning ("for one year now") is taught later.

**Decision needed:** Accept as borderline (the pattern does appear in Genki I L7 supplementary notes) or rewrite. If rewriting:
```
"ja": "わたしは 1年間 日本語を べんきょうしました。今も べんきょうしています。"
```

### 3.4 `n5.read.013` - `おみやげに` (purposive `に`)

**Passage states:**
> おみやげに おかしを 買いました。

**Problem:** The purposive `に` ("for / as souvenir") is borderline late N5 (Genki I L11, Minna I L13 cover it as part of the `〜に行く` pattern). Acceptable but worth a tier flag.

**Decision needed:** Tag as late-N5 or rewrite. The current usage is natural and pedagogically valuable; recommend keeping with a tier label.

### 3.5 Question count per passage exceeds JLPT format

**Current:** 2 to 3 questions per passage, total 63 questions across 30 passages.

**Real JLPT N5 format:**
- Mondai 4 (短文 / short text): 4 passages, 1 question each
- Mondai 5 (中文 / mid-length): 1 passage, 2 questions
- Mondai 6 (情報検索 / info search): 1 task, 1 question

**Problem:** The corpus over-questions each passage. This is pedagogically defensible (more practice per passage means better consolidation) but means the corpus does NOT visually mirror the actual exam.

**Recommendation:** Keep as-is for the Practice/Learn mode, but the app's Test/Mock-exam mode should select only 1 question per passage to mirror the actual JLPT distribution. Add a `format_role` field to questions:
```json
"questions": [
  { "id": "...q1", "format_role": "primary", ... },
  { "id": "...q2", "format_role": "extra", ... }
]
```

The mock test selects only `primary` questions; practice mode shows all.

### 3.6 Info-search passages lack format metadata

**Affected:** `n5.read.007`, `n5.read.017`, `n5.read.021`.

**Problem:** All three info-search passages render as plain line-broken text. The actual JLPT presents these as bordered tables, notice boxes, or signage with visual chrome. The current data shape carries no information about how the passage should be visually rendered.

**Fix:** Add a `format_type` field to info-search passages:
```json
{
  "id": "n5.read.007",
  "level": "info-search",
  "format_type": "schedule_table",
  "topic": "schedule",
  ...
}
```

Suggested values:
- `n5.read.007` (library hours): `"format_type": "schedule_table"`
- `n5.read.017` (cafe menu): `"format_type": "menu_list"`
- `n5.read.021` (flight schedule): `"format_type": "schedule_table"`

The renderer maps each type to a visual treatment (bordered table, notice with header, menu with prices right-aligned).

---

## 4. LOW - polish

### 4.1 `n5.read.020` - mimetic `にこにこ`

**Passage states:**
> いつも にこにこ しています。

**Note:** `にこにこ` ("smilingly") is gitaigo (mimetic). Not in N5 vocab list; mimetic vocabulary in general is N4-N3. Acceptable for context (the meaning is clear) but worth flagging if the corpus is rigorous about vocab scope.

**Action:** Either accept (mimetic vocab in passages is realistic and useful) or rewrite as `いつも わらって います`. Recommend accepting.

### 4.2 Common N5 vocabulary missing from `n5_vocab_whitelist.json`

Items found in passages that should likely be in the whitelist:

| Word | Meaning | Found in |
|---|---|---|
| しんごう | traffic light | n5.read.030 |
| まがる | to turn | n5.read.030 |
| 出口 | exit | n5.read.030 |
| カフェ | cafe | n5.read.017, 027 |
| カレー | curry | n5.read.022 |
| デパート | department store | n5.read.014, 027 |
| コンビニ | convenience store | n5.read.004 |
| おとな | adult | n5.read.021, 023 |
| こうこうせい / 高校生 | high school student | n5.read.005 |
| べつべつ | separately | n5.read.017 |
| おてら | temple | n5.read.013 |
| さくら | cherry blossom | n5.read.015 |
| りんご | apple | n5.read.026 |
| バナナ | banana | n5.read.026 |
| スペイン | Spain | n5.read.024 |
| スペイン人 | Spanish person | n5.read.024 |

Most of these are standard N5 vocab in mainstream sources (JLPT Sensei, Tofugu, Bunpro). The whitelist appears to be missing them.

**Action:** Audit the vocab whitelist for completeness against passages. Either add the missing items, or document them as a "in-passage exception" if the whitelist's scope is narrower than the corpus's reading vocabulary.

### 4.3 Personal names not in vocab whitelist

`マリア`, `ヤマダ`, `スズキ`, `たなか`, `アンナ` appear in passages but not in the whitelist.

**Action:** Personal names are universally exempted from textbook vocab whitelists; no fix needed. Recommend documenting the exemption in the project README so the absence isn't flagged in future audits.

### 4.4 `n5.read.014` - tense shift in description

**Passage states:**
> すこし たかかったですが、とても きれいです。

**Problem:** Past tense "was expensive" then present tense "is nice" - for an item the speaker bought yesterday and now owns, the shift is awkward. Native speakers do say this in casual speech, so it's not strictly wrong, just inelegant.

**Action:** Optional fix to either both-past (`たかかったですが、きれいでした`) or to a present description (`たかいですが、きれいです`). Low priority.

---

## 5. Cross-cutting suggestions

### 5.1 Add a `tier` field to passages

The corpus mixes "core N5" and "borderline late-N5 / early-N4" content without distinction. Adding a `tier` field would let the app filter by strict-N5 vs lenient-N5 based on user preference:

```json
{
  "id": "n5.read.018",
  "tier": "late_n5",
  ...
}
```

Suggested values: `core_n5`, `late_n5`, `info_search`. Most passages are `core_n5`; the borderline ones (007, 013, 018, 025, 030 after the fix) are `late_n5`.

### 5.2 Add a `kanji_used` and `vocab_used` index to each passage

For runtime app features (e.g., "this passage uses kanji you haven't learned yet"), each passage should declare its content:

```json
{
  "id": "n5.read.001",
  "kanji_used": ["来", "今", "大", "学", "日", "本", "語", "見"],
  "vocab_used": ["わたし", "アンナ", "アメリカ", "来る", "今", "東京", "大学", ...]
}
```

This is a build-time generation task, not hand-edited.

### 5.3 Standardize space-before-kanji policy

Currently the corpus is mostly consistent (a space before kanji words after particles), but not perfectly so (`n5.read.001`'s `とうきょうの大学` is the exception caught here). Document the rule in the project README: "Insert a single space at every word boundary, including before kanji compounds." Then run an automated check.

### 5.4 Consistency checks to add to CI

If the project has automated testing, add:

1. Every kanji in a passage's `ja` field is in `n5_kanji_whitelist.json`.
2. Every kanji in any explanation's `explanation_en` is also present in the corresponding passage's `ja` field.
3. Every choice in `choices` uses the same rendering convention as the passage.
4. No passage uses any of the documented N4 grammar markers (`〜と` conditional, potential form `〜られる`, `〜たり`, etc.) without a `tier: "late_n5"` flag.

These four checks catch the bulk of the issues found in this audit and prevent regression.

---

## 6. Acceptance criteria

This work is complete when:

1. All 5 CRITICAL items are fixed and verified by spot-check against the passage source.
2. All 5 HIGH items are fixed.
3. All 6 MEDIUM items are either fixed or have a code comment / TODO documenting why they were deferred.
4. The 4 cross-cutting consistency checks (5.4) pass.
5. **A native Japanese speaker has reviewed the diff** for the rewrites in 1.4, 1.5, and 2.1, and confirmed the rewritten Japanese is natural at N5 level.
6. The passage and question count remain at 30 / 63 unless a passage was deliberately removed with documented justification.

---

## 7. Quick-reference issue summary

| Severity | ID | Issue |
|---|---|---|
| CRITICAL | 1.1 | `n5.read.029` Q1 explanation misquotes passage (上 vs 高い) |
| CRITICAL | 1.2 | `n5.read.010` Q1 explanation produces ungrammatical Japanese (drops こ counter) |
| CRITICAL | 1.3 | `n5.read.010` Q1 choices are bare numbers; should include こ |
| CRITICAL | 1.4 | `n5.read.007` Q2 prompt uses N4 potential form かりられる |
| CRITICAL | 1.5 | `n5.read.030` passage uses N4 〜と conditional |
| HIGH | 2.1 | `n5.read.022` uses N3 verb よろこぶ |
| HIGH | 2.2 | 8 occurrences of passage-vs-explanation rendering mismatch |
| HIGH | 2.3 | `n5.read.024` Q2 prompt mixes 日本ご instead of 日本語 |
| HIGH | 2.4 | `n5.read.001` missing space in とうきょうの大学 |
| HIGH | 2.5 | `n5.read.026` English typo "very very cheap" |
| MEDIUM | 3.1 | `n5.read.018` Q2 distractor はつおん is non-N5 vocab |
| MEDIUM | 3.2 | `n5.read.025` borderline `〜たい + N` modifier |
| MEDIUM | 3.3 | `n5.read.018` borderline `1年前から + ています` durative |
| MEDIUM | 3.4 | `n5.read.013` borderline purposive に in おみやげに |
| MEDIUM | 3.5 | Question count per passage exceeds JLPT format |
| MEDIUM | 3.6 | Info-search passages lack format_type metadata |
| LOW | 4.1 | `n5.read.020` mimetic にこにこ (N4-ish) |
| LOW | 4.2 | Common N5 vocab missing from whitelist |
| LOW | 4.3 | Personal names not in vocab whitelist (expected) |
| LOW | 4.4 | `n5.read.014` tense shift in description |

**Total: 20 actionable items** (5 critical, 5 high, 6 medium, 4 low) plus 4 cross-cutting CI checks recommended.

---

*End of feedback.*
