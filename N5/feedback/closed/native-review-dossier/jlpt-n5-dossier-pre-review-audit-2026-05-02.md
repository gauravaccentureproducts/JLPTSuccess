# JLPT N5 Native-Reviewer Dossier - Pre-Review Audit

**Date:** 2026-05-02
**Audit scope:** the 5-file dossier prepared for native-Japanese-teacher review:
- `01_grammar_patterns.md` (177 patterns)
- `02_vocab_borderline.md` (122 vocab entries)
- `03_kanji_readings.md` (106 kanji)
- `04_reading_passages.md` (30 dokkai passages)
- `05_listening_scripts.md` (30 listening items)
- `cover.md` (reviewer instructions)

**Audit lens:** Japanese-language accuracy from a seasoned 日本語教師's perspective, with attention both to (a) Japanese-content quality and (b) dossier-readiness so the eventual native reviewer doesn't have to chase missing data.

**Comparison baseline:** prior audits dated April-May 2026 of the source corpus.

---

## 0. Executive summary

The corpus has clearly continued to improve. Most of the previously flagged CRITICAL and HIGH issues from April / May 2026 audits are resolved in this dossier:

**Verified resolved across files:**

- The wrong on-yomi for 会 (was いん) and 番 (was ごう) - now correct.
- The 4 missing kanji entries (号, 員, 社, 私) - now present.
- All 106 whitelist kanji have entries; none extra.
- The copy-paste propagation bug across n5-184/185/186/187 (question word + か/も compounds) - each pattern now has its own examples featuring the correct question word.
- Pattern n5-031 mislabel "informal question marker" with polite-か examples - now correctly uses 〜の plain-form examples.
- Pattern n5-091 (います) - the inappropriate `来ました` example has been replaced with `二ひき います`.
- Pattern n5-104 (たい) - the plain-form `もう ねたい` is now `もう ねたいです` matching the pattern's polite register.
- Pattern n5-110 (counter rendaku) - the awkward `3ぼん` form replaced with `3本`.
- The 10+ entries with duplicate kun readings (二, 七, 分, 見, 入, 立, 休, 高, 白, etc.) are deduplicated.
- Reading passage `n5.read.007` Q2 - N4 potential `かりられる` replaced with N5 `かりる ことが できる`.
- Reading passage `n5.read.029` Q1 choice - matches the passage's `30どより 高い` correctly.
- Reading passage `n5.read.030` - N4 `〜と` conditional replaced with N5 te-form.
- Reading passage `n5.read.022` - N3 verb `よろこびました` replaced with N5 `「おいしい」と 言いました`.
- Reading passage `n5.read.001` - missing space `とうきょうの大学` is now `とうきょうの 大学`.
- Reading passage `n5.read.018` Q2 - non-N5 distractor `はつおん` replaced with N5 `たんご`.
- Reading passage `n5.read.024` Q2 - mixed kana `日本ご` is now `日本語`.
- Reading passage `n5.read.010` Q1 - bare-number choices now use the こ counter (`10こ / 15こ / 20こ / 25こ`) matching the passage.
- All 30 reading passages now stay within the N5 kanji whitelist.

**Total issues remaining: 14** (3 critical, 4 high, 5 medium, 2 low). These are concentrated in dossier completeness, tier classification, and a small set of POS-tagging errors. The Japanese-language accuracy of the content itself is in solid shape.

---

## 1. CRITICAL - blockers for native-reviewer pass

### 1.1 `05_listening_scripts.md` - script, setup, and question text completely absent

**Cover.md promises** (file table):
> Per-item: format / setup / script / question / choices.

**Cover.md describes the reviewer's task** as:
> Speaker-turn naturalness; pacing of greetings; correctness of context (e.g. shop vs office vs school register).

**Actual file content:** Each of the 30 listening items contains ONLY the format tag (task / point / utterance) and the four answer choices. There is no script, no setup line, no comprehension question.

```
## `n5.listen.001` - どこで 会いますか

- **format:** task

  - [ ] えきの 前
  - [✓] カフェの 前
  - [ ] えいがかんの 前
  - [ ] デパートの 前
```

**Problem:** The reviewer's stated task (evaluate speaker-turn naturalness, pacing, register fit) is impossible without the scripts. The dossier promises "script" as a per-item field but delivers none. A reviewer reading the audit instructions and then opening this file will either:
- Stop immediately and ask for the missing data, or
- Try to evaluate "naturalness" of standalone choice strings, which is meaningless for a dialogue task

**Severity:** Critical (blocks the entire listening-review pass).

**Affected items:** all 30.

### 1.2 `02_vocab_borderline.md` - 3 nouns mistagged as `[interjection]`

**Affected entries:**
```
- n5.vocab.38-sounds-and-voice.こえ - 声 (voice)   - tagged [interjection]
- n5.vocab.38-sounds-and-voice.おと - 音 (sound)   - tagged [interjection]
- n5.vocab.38-sounds-and-voice.うた - 歌 (song)    - tagged [interjection]
```

**Problem:** こえ, おと, うた are common nouns. None of them functions as an interjection in Japanese (interjections are words like えーと, あの, さあ, うん, ええ used for hesitation, agreement, surprise, etc.). The mistag suggests the section name "sounds and voice" was misinterpreted by the POS-tagging step as "things that make sound = interjections."

**Severity:** Critical (factually wrong POS classification, will mislead any consumer of the data).

### 1.3 `01_grammar_patterns.md` - 14 patterns marked tier=`core_n5` that should be `late_n5`

**Affected patterns:**

| ID | Pattern | Current tier | Project source policy |
|---|---|---|---|
| n5-052 | どうやって | core_n5 | (Upper N5 / borderline) per grammar_n5.md |
| n5-145 | ～とおもいます | core_n5 | (Upper N5 / borderline) |
| n5-146 | ～と言いました | core_n5 | (Upper N5 / borderline) |
| n5-158 | 〜だろう | core_n5 | (Upper N5 / borderline) |
| n5-171 | Verb-ない + ほうがいい | core_n5 | parallel of n5-170 which is late_n5 |
| n5-174 | ～なくてはならない | core_n5 | parallel of n5-173 which is late_n5 |
| n5-175 | ～ないといけない | core_n5 | (Upper N5 / borderline) |
| n5-177 | ～すぎる | core_n5 | (Upper N5 / borderline) |
| n5-178 | ～つもりだ | core_n5 | (Upper N5 / borderline) |
| n5-179 | ～って (casual quote) | core_n5 | (Upper N5 / borderline) |
| n5-180 | Verb-stem + ～かた | core_n5 | (Upper N5 / borderline) |
| n5-181 | ～なあ | core_n5 | (Upper N5 / borderline) |
| n5-182 | Verb-plain + な (prohibitive) | core_n5 | (Upper N5 / borderline) |

**Inversely:** `n5-009` (から - particle for from / because) is currently tier=`late_n5`. This is wrong - the particle から is foundational, taught in Genki I L3 and Minna no Nihongo L4. Only the conjunction-から as a clause connector for "because" leans toward late N5; the basic particle should be `core_n5`.

**Problem:** The tier system is supposed to give the runtime app and the reviewer a clean signal about which patterns are foundational vs. which are stretch material. Currently 14 of 177 patterns are mis-tiered. This affects the quiz-mix calibration and the SRS scheduling if those depend on tier.

**Severity:** Critical (the project's own classification rule is not consistently applied).

---

## 2. HIGH - inconsistencies that hurt the reviewer's work

### 2.1 `03_kanji_readings.md` - primary readings still on-yomi for 高 / 長 / 安 / 白

The previous audit flagged primary readings for 高, 長, 安 as on-yomi when N5 standalone use is the kun-yomi i-adjective form.

**Current state:**
| Kanji | First on | First kun | Most common N5 use |
|---|---|---|---|
| 高 | こう | たか | たかい (i-adjective) |
| 長 | ちょう | なが | ながい (i-adjective) |
| 安 | あん | やす | やすい (i-adjective) |
| 白 | はく | しろ | しろ(い) (color noun / i-adjective) |

**Problem:** The cover.md instruction is *"the FIRST in each list is the one used by the runtime."* For these four, the first reading in the on list is what the runtime would surface, but for an N5 learner reading the kanji standalone (`高い` = "expensive" / "tall"), the kun reading is what they need. 新 also leans this way (新しい = あたらしい is N5; 新聞 = しんぶん is also N5, so 新 is genuinely tied).

**Severity:** High (recurring issue across audits; pedagogical impact is real).

### 2.2 `03_kanji_readings.md` - cover.md is ambiguous about what "primary" means

**Cover.md states:**
> The FIRST reading in each `on` / `kun` list is the runtime primary

**Problem:** "The first in each list" is two firsts (one for on, one for kun). The cover doesn't say which list takes precedence when both exist. The reviewer cannot flag a "wrong primary" without knowing which reading the runtime actually surfaces. The previous JSON format had an explicit `primary` field; the markdown format dropped it in favor of "first in list" but doesn't say which list.

**Recommended (for next dossier revision):** restore an explicit primary or document the precedence rule in the cover.

**Severity:** High (every flag-or-pass decision on every kanji entry depends on this).

### 2.3 `03_kanji_readings.md` - duplicate freq_rank values across 17 pairs

**Affected ranks:** 8, 22, 28, 33, 41, 50, 65, 71, 73, 79, 80, 93, 96, 98, 100, 102, 104.

Each of these rank values is shared by exactly two kanji. Examples:
- Rank 100: 六 and 古
- Rank 104: 番 and 号
- Rank 102: 白 and 私
- Rank 41: 手 (and earlier somewhere)
- Rank 28: 高 and 毎

**Problem:** A frequency rank is supposed to uniquely order entries. Either these are genuine ties (and the rubric should say so), or they're transcription errors. As-is, the field is unreliable for any feature that depends on a stable ordering (e.g., "show me the 10 most-frequent N5 kanji").

**Severity:** High (data quality; affects any downstream sequencing).

### 2.4 `01_grammar_patterns.md` - n5-152 has a typo in `meaning_ja`

**Current:**
```
## n5-152 - `どうぞ / どうも / すみません / おねがいします`
- meaning_ja: あいさつ・しゃいいご
```

**Problem:** `しゃいいご` is not a Japanese word. The intended term is almost certainly `しゃこうご` (社交語 - "courtesy / social language") or simply `あいさつ`. The current value will look like a careless error to any native reader.

**Severity:** High (visible Japanese-language defect; one entry, easy fix).

---

## 3. MEDIUM - quality and clarity

### 3.1 `01_grammar_patterns.md` - 88 of 177 patterns have weak `meaning_ja`

**Pattern:** roughly half of the patterns have `meaning_ja` consisting only of the pattern itself enclosed in 「」 quotes, with no actual Japanese-language gloss.

**Examples:**
```
n5-010 まで:    meaning_ja: 「いつ・どこ まで」
n5-011 や:      meaning_ja: 「Aや B (など)」
n5-027 よね:    meaning_ja: 「〜よね」
n5-052 どうやって: meaning_ja: 「どうやって」
n5-053 いくら:  meaning_ja: 「いくら」
n5-054 いくつ:  meaning_ja: 「いくつ」
```

**Problem:** When 50% of `meaning_ja` entries don't add information beyond what the pattern field already shows, the field is half-finished. A reviewer scanning these will not know whether to flag them as "missing gloss" (and propose Japanese-language explanations) or pass them as "deliberately blank."

**Recommended (for cover.md):** add a line specifying whether reviewers should flag empty meaning_ja as missing or skip them.

**Severity:** Medium (visible inconsistency in the dossier; doesn't affect Japanese accuracy).

### 3.2 `01_grammar_patterns.md` - n5-175 example doesn't use the pattern

**Current:**
```
## n5-175 - `～ないといけない`
examples:
  [0] はやく かえらなきゃ いけない。
```

**Problem:** The pattern is `〜ないといけない`. The example uses `〜なきゃいけない` (the `〜なくちゃ / 〜なきゃ` casual contraction). These are different patterns (n5-176 covers 〜なきゃ separately). A learner studying n5-175 doesn't see the form being taught.

**Severity:** Medium (content/pattern mismatch in one entry).

### 3.3 `02_vocab_borderline.md` - cross-listed POS inconsistency

**Affected entries:** どうぞ, どうも, もしもし, どうぞよろしく each appear twice (in section 33-adverbs AND section 36-greetings) with conflicting POS tags:

```
33-adverbs.どうぞ        - [adverb]
36-greetings.どうぞ      - [expression]

33-adverbs.もしもし      - [adverb]
36-greetings.もしもし    - [expression]
```

**Problem:** The same word receiving two different POS tags is internally inconsistent. もしもし is an interjection / phatic phrase, not an adverb. どうぞ is a set phrase / interjection, not an adverb. The 33-adverbs entries are mis-tagged.

If the cross-listing is deliberate (the project does have thematic sections), the entries should at least share the same POS tag. Pick one tag per word and use it in both places.

**Severity:** Medium (dossier consistency).

### 3.4 `04_reading_passages.md` - n5.read.026 Q1 question and choices use different counters

**Current Q1:**
> りんごを **何こ** 買いましたか。
> Choices: 1**つ** / 2**つ** / 3**つ** / 5**つ**

**Problem:** The question asks "how many こ?" but the answers use the つ counter. They're both valid counters for fruit, but mixing them in the same question is inconsistent. Either the question asks `何つ` (or `いくつ`) and choices use つ, or the question asks `何こ` and choices use こ.

The passage itself uses 3つ (`りんごを 3つ`), so the choices match the passage; the question stem is the off-by-one.

**Severity:** Medium (minor pedagogical inconsistency).

### 3.5 `05_listening_scripts.md` - title-only items make audit impossible

The title field on each item is a Japanese phrase (e.g., `どこで 会いますか` for n5.listen.001). With no script visible, the reviewer can ONLY evaluate the title, the format tag, and the four choices.

**What can actually be reviewed from this file:**
- Whether the four choices are grammatical Japanese (yes, with one previously-flagged exception in n5.listen.011)
- Whether the marked-correct choice is plausibly correct (impossible without the script)
- Whether the distractors are realistic (impossible without context)

**Problem:** Compounding issue 1.1 - even within the limited reviewable content, the dossier's review-rubric promises ("speaker-turn naturalness, pacing, register fit") cannot be honored because the reviewable surface doesn't contain anything that has speakers, turns, pacing, or register.

**Severity:** Medium (already counted in 1.1 as critical; mentioned here for completeness).

---

## 4. LOW - polish

### 4.1 `01_grammar_patterns.md` - n5-008 (と) has stilted `meaning_ja`

**Current:**
```
n5-008 と:    meaning_ja: 「いっしょに」「と」「いう」
```

**Problem:** Three Japanese-quoted concepts strung together with no connector. A native teacher would phrase this more naturally, e.g., `〜と(同伴)・〜と(れっきょ)・〜と(いんよう)` or `〜と(いっしょに / れっきょ / いんよう)`. The current form looks auto-generated.

**Severity:** Low.

### 4.2 `04_reading_passages.md` - n5.read.005 distractor uses non-N5 vocabulary

**Q1 distractors include `きょうし` (教師, "teacher / instructor")** which is N4 vocab. The passage's correct answer uses `先生` (sensei, the standard N5 term). Distractor vocab leakage is permitted by the project's documented exception, but きょうし is a notable case because the distractor isn't more discriminating than a clearly-wrong N5 term would be (e.g., `がくせい` "student" or `いしゃ` "doctor" would work as well and stay in scope).

**Severity:** Low.

---

## 5. Per-file summary

### `01_grammar_patterns.md`
**Status:** Largely improved. Previously-fixed bugs (n5-031, n5-091, n5-184/185/186/187, n5-069 missing ぐ rule, n5-104 register, mixed numerals) are all confirmed fixed. Remaining items: 14 tier mis-classifications (1.3), one typo (2.4), 88 weak meaning_ja entries (3.1), one example-pattern mismatch in n5-175 (3.2), one stilted meaning_ja in n5-008 (4.1).

### `02_vocab_borderline.md`
**Status:** Largely OK. Remaining: 3 noun-as-interjection mis-tags (1.2), 4 cross-listed POS inconsistencies (3.3). Coverage (~122 entries instead of stated ~100) is slightly larger than cover.md says but is not a problem.

### `03_kanji_readings.md`
**Status:** Substantially improved. Previously-fixed bugs (会, 番, missing 4 entries, 10 duplicate kun readings) all confirmed fixed. Remaining: 4 primary readings still on-yomi when N5 use is kun (2.1), ambiguous "primary" definition in cover.md (2.2), 17 duplicate freq ranks (2.3).

### `04_reading_passages.md`
**Status:** Substantially improved. All previously-flagged grammar / vocab / rendering issues from prior audits are confirmed fixed. Remaining: one counter inconsistency in n5.read.026 Q1 (3.4), one borderline distractor in n5.read.005 (4.2). Whitelist conformance is clean across all 30 passages.

### `05_listening_scripts.md`
**Status:** Critical incompleteness (1.1). The dossier file delivers ~5% of what the cover.md promises. The reviewer cannot do listening-review work from this file as currently shipped.

### `cover.md`
**Status:** Mostly clear. The "primary = first in list" ambiguity (2.2) needs a one-line clarification. The reviewer turnaround estimate ("2-3 hours per file, 5 files = 10-15h total") is internally consistent but assumes the listening file is reviewable; with the script-absent state, the listening review takes 0 hours (or unbounded hours, depending on whether the reviewer chases data).

---

## 6. Recommended next steps

If only 5 things get worked on before sending to the native reviewer:

1. **Add scripts, setup, and question text to `05_listening_scripts.md`** (1.1). Without this, the reviewer cannot start on the listening file.
2. **Fix the 3 noun-as-interjection POS tags** in `02_vocab_borderline.md` (1.2). Two-line edit.
3. **Re-tier the 14 mis-classified grammar patterns** (1.3). Mechanical edit; the project's own grammar_n5.md already documents which should be late_n5.
4. **Fix the しゃいいご typo** in n5-152 (2.4). Single character correction.
5. **Clarify "primary" in cover.md** (2.2). One-line addition: "When both on and kun are listed, the FIRST entry of the kun list takes precedence as primary unless the kanji has no kun reading, in which case the FIRST on entry is primary." (Or whatever the runtime actually does - confirm with the dev side.)

The remaining issues are polish-grade and can be worked through during or after the native review.

---

## 7. Acceptance criteria

This pre-review work is complete when:

1. The CRITICAL items (1.1, 1.2, 1.3) are fixed.
2. The HIGH items (2.1, 2.2, 2.3, 2.4) are fixed.
3. Each MEDIUM item is either fixed or has a one-line note in the cover.md telling the reviewer to skip / pass it.
4. A second pre-review audit (or a spot-check by the dev) confirms the dossier matches the cover's promised contents per file.
5. The native reviewer, given the dossier cold, is able to complete the audit without sending back "where is X?" questions.

---

## 8. Quick-reference issue summary

| Severity | ID | File | Issue |
|---|---|---|---|
| CRITICAL | 1.1 | 05_listening_scripts.md | Scripts, setup, and questions absent for all 30 items |
| CRITICAL | 1.2 | 02_vocab_borderline.md | 3 nouns (こえ, おと, うた) mistagged as [interjection] |
| CRITICAL | 1.3 | 01_grammar_patterns.md | 14 patterns mis-tiered relative to project's own classification |
| HIGH | 2.1 | 03_kanji_readings.md | Primary readings for 高/長/安/白 still on-yomi when N5 use is kun |
| HIGH | 2.2 | cover.md | "Primary = first in list" doesn't say which list takes precedence |
| HIGH | 2.3 | 03_kanji_readings.md | 17 duplicate freq_rank values |
| HIGH | 2.4 | 01_grammar_patterns.md | n5-152 meaning_ja typo "しゃいいご" |
| MEDIUM | 3.1 | 01_grammar_patterns.md | 88 of 177 patterns have weak meaning_ja (just pattern in 「」 quotes) |
| MEDIUM | 3.2 | 01_grammar_patterns.md | n5-175 example uses 〜なきゃ instead of the pattern's 〜ないと |
| MEDIUM | 3.3 | 02_vocab_borderline.md | Cross-listed entries have conflicting POS tags (どうぞ, どうも, もしもし, どうぞよろしく) |
| MEDIUM | 3.4 | 04_reading_passages.md | n5.read.026 Q1 mixes 何こ stem with つ choices |
| MEDIUM | 3.5 | 05_listening_scripts.md | Reviewable surface insufficient for cover-stated rubric |
| LOW | 4.1 | 01_grammar_patterns.md | n5-008 と has stilted "「いっしょに」「と」「いう」" meaning_ja |
| LOW | 4.2 | 04_reading_passages.md | n5.read.005 distractor きょうし uses N4 vocab when N5 alternatives work |

**Total: 14 actionable items** (3 critical, 4 high, 5 medium, 2 low).

---

## 9. Comparison with prior audits

| Audit cycle | Critical | High | Medium | Low | Total |
|---|---|---|---|---|---|
| Initial markdown audit (April 2026) | 5 | 7 | 9 | 6 | 27 |
| First JSON audit (April 2026) | 10 | 9 | 10 | 6 | 35 |
| reading.json focused (April 2026) | 5 | 5 | 6 | 4 | 20 |
| Consolidated JSON (May 2026) | 1 | 4 | 5 | 2 | 12 |
| Consolidated MD (May 2026) | 1 | 3 | 4 | 1 | 9 |
| **Native-reviewer dossier (May 2026)** | **3** | **4** | **5** | **2** | **14** |

This audit's CRITICAL count (3) is higher than the previous cycle (1) because the listening dossier is missing its primary content - this isn't a content regression, it's a NEW issue introduced by the dossier-prep step. The actual Japanese-content quality continues to improve. With the listening scripts added back, the dossier would be in genuinely strong shape for native review.

---

*End of audit. Prepared 2026-05-02.*
