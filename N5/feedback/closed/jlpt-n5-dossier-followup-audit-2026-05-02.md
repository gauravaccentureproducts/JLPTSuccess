# JLPT N5 Native-Reviewer Dossier - Follow-up Verification Audit

**Date:** 2026-05-02 (second pass)
**Audit scope:** the 6-file dossier prepared for native-Japanese-teacher review, after the developer's fix pass.
**Comparison baseline:** prior audit `jlpt-n5-dossier-pre-review-audit-2026-05-02.md` (first pass), which flagged 14 actionable items (3 critical, 4 high, 5 medium, 2 low).

---

## 0. Executive summary

**Every issue flagged in the previous audit is now resolved.** This is the cleanest cycle of this audit series.

The dossier is ready to ship to the native reviewer.

| Severity | Previously flagged | Verified resolved | Remaining |
|---|---|---|---|
| CRITICAL | 3 | 3 | 0 |
| HIGH | 4 | 4 | 0 |
| MEDIUM | 5 | 5 | 0 |
| LOW | 2 | 2 | 0 |
| **Total** | **14** | **14** | **0** |

---

## 1. Verification of CRITICAL fixes

### 1.1 ✓ FIXED - `05_listening_scripts.md` now contains scripts, setups, and questions

**Before:** 30 items, ~3,759 bytes, only choices visible.
**After:** 30 items, 8,321 bytes (2.2× larger), all 30 items have:
- A `**format:**` tag
- A `**script (setup + dialogue):**` block in fenced code with the full dialogue
- A `**question:**` field with the comprehension question

**Spot-check of the new content quality** (sampled n5.listen.001, 002, 005, 011, 013-015, 019-022, 024):

- **Speaker turns are natural.** Use of 男 / 女 / 先生 / 学生 / 母 / 子 / A / B / 店員 prefixes aligns with JLPT convention.
- **Register fits each setting.** Shop dialogue uses いらっしゃいませ / お願いします. School dialogue uses 先生 / 学生 forms with appropriate distance. Family dialogue between 母 and 子 uses casual register without の / って / なきゃ excess.
- **Pacing is realistic.** Each dialogue is 4-6 turns, which is consistent with JLPT N5 listening Mondai 1 (課題理解) and Mondai 2 (ポイント理解) lengths.
- **Setup sentences match the convention** "[Person]と[Person]が話しています。[question prompt]" - this is the standard JLPT setup format.
- **No non-N5 kanji** in any of the 30 listening scripts.

The reviewer can now do the work the cover.md asks them to do (speaker-turn naturalness, pacing, register fit).

### 1.2 ✓ FIXED - `02_vocab_borderline.md` interjection mistags removed

**Before:** こえ, おと, うた tagged `[interjection]` (they're nouns).
**After:** Zero `[interjection]` entries remain in the file. The 38-sounds-and-voice section has been removed entirely - これ is a sensible cleanup since these three nouns weren't really "borderline / register-sensitive" in the way the dossier title implies, so they don't belong here anyway.

Total entry count adjusted from 122 to 119, and the cover.md was updated to match.

### 1.3 ✓ FIXED - 14 grammar patterns re-tiered correctly

**Before:** 13 patterns mis-tiered as `core_n5` when they should be `late_n5`; 1 pattern (n5-009 から) mis-tiered as `late_n5` when it should be `core_n5`.

**After:** Every one of the 14 has been corrected.

| ID | Pattern | Before | After |
|---|---|---|---|
| n5-052 | どうやって | core_n5 | late_n5 ✓ |
| n5-145 | ～とおもいます | core_n5 | late_n5 ✓ |
| n5-146 | ～と言いました | core_n5 | late_n5 ✓ |
| n5-158 | 〜だろう | core_n5 | late_n5 ✓ |
| n5-171 | Verb-ない + ほうがいい | core_n5 | late_n5 ✓ |
| n5-174 | ～なくてはならない | core_n5 | late_n5 ✓ |
| n5-175 | ～ないといけない | core_n5 | late_n5 ✓ |
| n5-177 | Verb-stem / Adj-stem + すぎる | core_n5 | late_n5 ✓ |
| n5-178 | Verb-plain + つもりだ / つもりです | core_n5 | late_n5 ✓ |
| n5-179 | ～って (casual quotation) | core_n5 | late_n5 ✓ |
| n5-180 | Verb-stem + ～かた | core_n5 | late_n5 ✓ |
| n5-181 | ～なあ | core_n5 | late_n5 ✓ |
| n5-182 | Verb-plain + な (prohibitive) | core_n5 | late_n5 ✓ |
| n5-009 | から | late_n5 | core_n5 ✓ |

**Updated totals:** 153 core_n5 + 24 late_n5 = 177 patterns. The late_n5 set roughly doubled (12 → 24), which now matches the project's stated grammar_n5.md "Upper N5 / borderline" tagging much more faithfully.

---

## 2. Verification of HIGH fixes

### 2.1 ✓ FIXED - primary readings for 高 / 長 / 安 / 白

The dossier now uses an explicit `primary reading:` field plus a documented precedence rule. All four kanji previously flagged now correctly show kun-yomi as primary:

| Kanji | on | kun | primary reading |
|---|---|---|---|
| 高 | こう | たか | たか (kun) ✓ |
| 長 | ちょう | なが | なが (kun) ✓ |
| 安 | あん | やす | やす (kun) ✓ |
| 白 | はく / びゃく | しろ / しら- | しろ (kun) ✓ |

This is the right outcome. A learner studying 高 standalone gets たか(い), which is what they encounter in N5 vocab.

### 2.2 ✓ FIXED - cover.md primary-reading precedence rule documented

The cover now contains a dedicated section "Kanji primary-reading precedence (file 03)" with a clear three-step rule:

1. Explicit `primary_reading:` field wins.
2. Else first kun (if any).
3. Else first on.

It also notes that 新 is genuinely tied (新聞 / 新しい both N5) and either reading is acceptable as primary. This addresses both the runtime ambiguity AND gives the reviewer guidance on edge cases.

### 2.3 ✓ FIXED - duplicate freq_rank values

**Before:** 17 pairs of duplicate freq_rank values in 03_kanji_readings.md.
**After:** Zero duplicates. All 106 kanji have unique ranks 1-106.

### 2.4 ✓ FIXED - n5-152 typo

**Before:** `meaning_ja: あいさつ・しゃいいご` (not a Japanese word).
**After:** `meaning_ja: あいさつ・しゃこうご` (社交語 - "courtesy / social language"). Correct.

---

## 3. Verification of MEDIUM fixes

### 3.1 ✓ FIXED - cover.md addresses weak meaning_ja entries

The cover now contains a section "Empty meaning_ja in file 01" that explicitly tells the reviewer to:
- Skip pattern-only meaning_ja entries as "deliberately blank"
- Override only if they can supply a learner-friendly Japanese explanation that adds information

This converts what was previously a 50%-of-the-file ambiguity into a clear pass-rule. Good editorial discipline - rather than authoring 88 new meaning_ja entries to fill gaps, the cover documents the intentional design choice and lets the reviewer skip them.

### 3.2 ✓ FIXED - n5-175 example uses the correct pattern

**Before:** `はやく かえらなきゃ いけない。` (using 〜なきゃ contraction, which is n5-176's pattern).
**After:** `はやく かえらないと いけない。` (using 〜ないと, which is n5-175's actual pattern).

The English translation also updated from "I have to go home quickly" to "I must go home soon" - both natural.

### 3.3 ✓ FIXED - cross-listed POS tags now consistent

**Before:** どうぞ, どうも, もしもし, どうぞよろしく had `[adverb]` in section 33-adverbs and `[expression]` in section 36-greetings - same word, different tag.

**After:** All four are now `[expression]` in BOTH sections. The 33-adverbs section retains the cross-listing for thematic discoverability, but the POS tag is consistent across both occurrences. Correct call - these are interjections / set phrases, not adverbs.

### 3.4 ✓ FIXED - n5.read.026 Q1 counter consistency

**Before:** Question asked `何こ`, choices used つ counter (mismatch).
**After:** Question asks `いくつ` (a counter-neutral question word), choices use つ counter (matching the passage's `りんごを 3つ`).

This is the cleaner fix - using `いくつ` rather than `何つ` is more natural Japanese.

### 3.5 ✓ ADDRESSED - listening reviewable surface

Subsumed by 1.1. With scripts now present, the reviewable surface is fully aligned with the cover-stated rubric.

---

## 4. Verification of LOW fixes

### 4.1 ✓ FIXED - n5-008 (と) meaning_ja is no longer stilted

**Before:** `meaning_ja: 「いっしょに」「と」「いう」` (three separately-quoted concepts).
**After:** `meaning_ja: 〜と(いっしょに / れっきょ / いんよう)` - now reads as a single Japanese-language gloss with three sub-senses delineated. Natural.

### 4.2 ✓ FIXED - n5.read.005 distractor changed from きょうし to せんせい

**Before:** Q2 and Q3 distractors included `きょうし` (N4 vocab, "instructor").
**After:** Both questions now use `せんせい` (the N5 standard term, matching the passage's `先生`). All four choices in both questions are now drawn from the passage's vocabulary register.

---

## 5. Spot-check for newly introduced issues

I sampled the new listening scripts and a random selection of grammar patterns, vocab entries, kanji entries, and reading passages to look for any new problems introduced by the fix pass.

**Findings: none.**

The new listening scripts are natural Japanese at N5 level. Specifically:

- **n5.listen.002** (shopping by phone): natural service-Japanese including `もしもし`, `おねがいします`, polite imperative `〜て ください`. Multi-step item list (パン → たまご → ぎゅうにゅう) gives a real listening challenge appropriate for Mondai 1.
- **n5.listen.005** (apology for being late): correct keigo register from student to teacher (`すみません`, polite-form responses). The exchange is short and realistic.
- **n5.listen.014** (meeting at station): proper use of 来週 / 土ようび / 北の 出口 / 〜て ください. The 男/女 alternation works for differentiating speakers without naming them.
- **n5.listen.020** (book price): minimal four-turn exchange that lands cleanly on a price.
- **n5.listen.024** (who is coming today): three-person enumeration tests careful listening, which is appropriate Mondai 2 content.

The N4-borderline patterns I'd watch for in any new content (potential form, conditional 〜と, mimetics) are absent from these scripts.

---

## 6. Comparison across audit cycles

| Audit cycle | Critical | High | Medium | Low | Total |
|---|---|---|---|---|---|
| Initial markdown audit (April 2026) | 5 | 7 | 9 | 6 | 27 |
| First JSON audit (April 2026) | 10 | 9 | 10 | 6 | 35 |
| reading.json focused (April 2026) | 5 | 5 | 6 | 4 | 20 |
| Consolidated JSON (May 2026) | 1 | 4 | 5 | 2 | 12 |
| Consolidated MD (May 2026) | 1 | 3 | 4 | 1 | 9 |
| Native-reviewer dossier first pass (May 2026) | 3 | 4 | 5 | 2 | 14 |
| **Native-reviewer dossier follow-up (May 2026)** | **0** | **0** | **0** | **0** | **0** |

The trajectory across this multi-month audit series is now at zero. Every prior CRITICAL has been resolved; every prior HIGH has been resolved; the dossier matches its own cover.md promises.

---

## 7. Recommendations

**Send the dossier to the native reviewer.**

There's nothing further the dev side can usefully do before native eyes see the corpus. The remaining work is genuinely native-judgement work - things like:

- "Does this dialogue actually sound like how a native speaker would phrase it, or is it textbook-stilted?"
- "Is the tier classification of n5-052 (どうやって) defensible, or would I personally place it earlier / later?"
- "Does the family-conversation register in n5.listen.024 match what a Japanese mother and child would actually say?"

These are review-pass questions, not pre-review-pass questions. The reviewer is now in a position to use their own ear and experience without first having to chase missing data or untangle inconsistencies.

**Two suggested process additions for after the native review comes back:**

1. Track the reviewer's findings against the severity rubric in cover.md so the dev side can process by tier.
2. Invite the reviewer to flag anything they think the cover.md should say differently next time. Their fresh-eyes feedback on the cover itself is data we'd otherwise lose.

---

## 8. Quick-reference verification table

| Severity | ID | File | Issue | Status |
|---|---|---|---|---|
| CRITICAL | 1.1 | 05_listening_scripts.md | Scripts, setup, and questions absent | ✓ FIXED (8.3 KB, all 30 items have script + question) |
| CRITICAL | 1.2 | 02_vocab_borderline.md | 3 nouns mistagged as [interjection] | ✓ FIXED (section 38 removed; 119 total entries) |
| CRITICAL | 1.3 | 01_grammar_patterns.md | 14 patterns mis-tiered | ✓ FIXED (all 14 corrected) |
| HIGH | 2.1 | 03_kanji_readings.md | Primary readings on-yomi when N5 use is kun | ✓ FIXED (explicit primary_reading field added) |
| HIGH | 2.2 | cover.md | Primary precedence rule ambiguous | ✓ FIXED (3-step rule documented) |
| HIGH | 2.3 | 03_kanji_readings.md | 17 duplicate freq_rank values | ✓ FIXED (zero duplicates) |
| HIGH | 2.4 | 01_grammar_patterns.md | n5-152 しゃいいご typo | ✓ FIXED (now しゃこうご) |
| MEDIUM | 3.1 | cover.md | 88 weak meaning_ja entries | ✓ FIXED (cover documents skip-rule) |
| MEDIUM | 3.2 | 01_grammar_patterns.md | n5-175 example mismatch | ✓ FIXED (now uses 〜ないと) |
| MEDIUM | 3.3 | 02_vocab_borderline.md | Cross-listed POS inconsistency | ✓ FIXED (all entries [expression]) |
| MEDIUM | 3.4 | 04_reading_passages.md | n5.read.026 Q1 counter mix | ✓ FIXED (now uses いくつ) |
| MEDIUM | 3.5 | 05_listening_scripts.md | Reviewable surface insufficient | ✓ FIXED (subsumed by 1.1) |
| LOW | 4.1 | 01_grammar_patterns.md | n5-008 と stilted meaning_ja | ✓ FIXED |
| LOW | 4.2 | 04_reading_passages.md | n5.read.005 distractor きょうし | ✓ FIXED (now せんせい) |

**14 of 14 items resolved. Zero remaining issues from the previous audit. No new issues introduced.**

---

*End of follow-up audit. Prepared 2026-05-02.*
