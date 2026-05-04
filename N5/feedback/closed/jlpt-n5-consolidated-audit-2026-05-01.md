# JLPT N5 Tutor - Consolidated Content Audit

**Date:** 2026-05-01
**Audit scope:** 9 JSON files covering the full N5 content corpus (grammar, kanji, vocab, questions, listening, audio_manifest, kanji_readings, kanji_whitelist, vocab_whitelist).
**Audit lens:** Japanese-language accuracy plus cross-file consistency, from a seasoned Japanese teacher's perspective.
**Comparison baseline:** Earlier audits dated April 2026 of `KnowledgeBank` markdown source files and the JSON data bundle.

---

## 0. Executive summary

The corpus has improved substantially since the previous audit. Most of the previously flagged CRITICAL and HIGH issues have been fixed:

**Verified resolved:**
- The wrong on-yomi in `n5_kanji_readings.json` for 会 (was `いん`, now `かい/え`) and 番 (was `ごう`, now `ばん`).
- The 4 missing kanji entries (号, 員, 社, 私) are now present.
- Whitelist coverage is exact: 106 kanji in whitelist, 106 entries in readings, zero missing or extra.
- The copy-paste propagation bug in question-word compound patterns: n5-184 through n5-187 now have distinct, correct examples for each (なにか/だれか/どこか/いつか and their negative pairs).
- Pattern `n5-031` is now correctly labeled as the informal `〜の` question marker with plain-form examples.
- Pattern `n5-091` (います) no longer contains the inappropriate 来ました example; the new third example uses 二ひき います properly.
- Pattern `n5-069` (Verb-て) now has the previously-missing ぐ→いで rule.
- Pattern `n5-104` (Verb-stem + たいです): the polite-form mismatch in `もう ねたい` is fixed to `もう ねたいです`.
- Listening item `n5.listen.007` (favorite season): N4 grammar (`〜し`, `〜すぎる`) has been removed and replaced with N5-only constructions.
- Listening item `n5.listen.011` prompt has been rewritten to no longer echo the answer.
- All listening scripts now stay within the N5 kanji whitelist.
- All grammar example sentences now stay within the N5 kanji whitelist.
- All question stems and choices stay within the N5 kanji whitelist.
- Group-1 ru-verb exceptions (入る, 帰る, 走る, 知る, 切る, 要る) are now flagged in vocab.json with `(Group 1 exception - looks like Group 2)` notes.
- The kanji glyphs 手, 力, 足, 目, 口 have been added to `kanji.json` (previously missing despite being in the whitelist).
- Question q-0040 has been rewritten - the unnatural Japanese sentence (`にほんごのほんをべんきょうします`) is now `にほんごのほんを読みます` ("read Japanese books"), which is natural.

**This is significant progress.** The previous audit identified roughly 35 actionable items across files; the majority appear to be addressed.

**Remaining issues split into:**
- **Mechanical residue (8 items):** primary-reading choices for kun-yomi i-adjectives; duplicate kun readings; one listening item internal inconsistency; expanding question coverage; audio backend.
- **Structural (4 items):** primary-reading semantics, audio pipeline status, vocab whitelist completeness for late additions, and one new finding around audio cross-references.

Total remaining actionable items: 12 (1 critical, 4 high, 5 medium, 2 low).

---

## 1. CRITICAL - factual errors that mislead a learner

### 1.1 `listening.json` n5.listen.011 - script and choices array don't match

**Script declares:**
```
1. ありがとう、いただきます。
```

**Choices array shows:**
```
"choices[0]": "ありがとうございます、いただきます。"
```

**Problem:** The audio script (what gets read aloud / displayed as the question) lists choice 1 as `ありがとう、いただきます。` (casual). The choices array - which is what the test-taker sees as a clickable option - shows `ありがとうございます、いただきます。` (polite). The two should be identical so the user can match what they hear to what they pick.

**Fix (recommended):** Use the polite form in both places, since the correct answer is also polite:
```json
"script_ja": "（友だちが ケーキを すすめました。でも、もう おなかが いっぱいです）\n1. ありがとうございます、いただきます。\n2. すみません、もう おなかが いっぱいです。\n3. もう 一つ ください。"
```

**Why this is critical and not lower:** A learner who clicks the option that matches what they heard ("ありがとう、いただきます") will be marked wrong because the choices array contains a different string. The discrepancy is a direct grading bug.

---

## 2. HIGH - inconsistencies that hurt credibility

### 2.1 `n5_kanji_readings.json` - primary readings still on-yomi for 高/長/安

**Current state:**
- 高: `primary: "こう"` (on-yomi)
- 長: `primary: "ちょう"` (on-yomi)
- 安: `primary: "あん"` (on-yomi)

**Problem:** This was flagged in the previous audit. At N5, the high-frequency standalone use of these kanji is the i-adjective form (kun-yomi):
- 高い (たかい) "high / expensive"
- 長い (ながい) "long"
- 安い (やすい) "cheap"

The on-yomi readings are reserved for compounds that mostly fall outside N5 vocab. A furigana-or-flashcard system that displays the "primary" reading first will display the wrong, confusing reading for the most common N5 use case.

**Fix:**
```json
"高": { "on": ["こう"], "kun": ["たか"], "primary": "たか" },
"長": { "on": ["ちょう"], "kun": ["なが"], "primary": "なが" },
"安": { "on": ["あん"], "kun": ["やす"], "primary": "やす" }
```

For 新, keep the current `primary: "しん"` since both 新しい and 新聞 are common N5 vocab and the on-yomi is the more learner-useful default.

### 2.2 `n5_kanji_readings.json` - duplicate kun readings still present

**Current duplicates:**
```
二:  ["ふた", "ふた"]
七:  ["なな", "なな", "なの"]
分:  ["わ", "わ", "わ"]
見:  ["み", "み", "み"]
聞:  ["き", "き"]
入:  ["い", "はい", "い"]
立:  ["た", "た"]
休:  ["やす", "やす"]
高:  ["たか", "たか"]
白:  ["しろ", "しろ", "しら-"]
```

**Problem:** Previously flagged. The duplicates are an artifact of stripping okurigana off entries that were originally distinguished by it. For 入, the duplicates `い, はい, い` collapse three semantically distinct verbs (`入る = はいる`, `入る = いる archaic`, `入れる = いれる`) into garbled list items.

**Fix (minimum):** Deduplicate. For 入, retain `["い", "はい"]` only.

**Fix (better):** Preserve okurigana-binding so `入る` and `入れる` stay distinguishable. Schema option:
```json
"入": {
  "on": ["にゅう"],
  "kun_with_okurigana": ["はい(る)", "い(る)", "い(れる)"],
  "kun": ["はい", "い"],
  "primary": "はい"
}
```

### 2.3 `audio_manifest.json` cross-reference inconsistency for listening items 13-30

**Current state:**
- Listening items 1-12: present in `audio_manifest.json` with `skipped: true`. None have audio.
- Listening items 13-30: NOT in `audio_manifest.json` at all, but each has a `voice: "synthetic-voicevox-shikoku-metan"` field in `listening.json` indicating audio was synthesized via VOICEVOX.
- Audio manifest has 5 active items total: 4 grammar examples + 1 listening item.

**Problem:** Two issues at once:

1. **Manifest is incomplete.** Listening items 13-30 have audio (per the `voice` field) but no manifest entry. The runtime app cannot know whether to fetch them.
2. **Backend mismatch.** The manifest's stated backend is `gtts` but listening items 13-30 declare `synthetic-voicevox-shikoku-metan`. These are two different TTS systems. VOICEVOX produces dramatically better Japanese than gTTS - this is good - but the manifest needs to reflect reality.

**Fix:**
1. Regenerate `audio_manifest.json` to include entries for all listening items 13-30 with `skipped: false` and a per-item `voice` field.
2. Update the manifest's top-level `backend` field to reflect the mixed state (e.g., `"backend": "mixed"`) or remove the field if it's unused.
3. Add a CI check: every audio reference in `listening.json`, `reading.json`, `grammar.json`, etc. must resolve to a non-skipped entry in the manifest.

### 2.4 Question coverage of grammar patterns is partial

**Current:**
- 187 grammar patterns defined.
- 84 patterns referenced by at least one question (45%).
- 103 patterns have zero questions.

**Problem:** Many of the 103 uncovered patterns are duplicate-cleanup redirects (legitimate - their canonical entries are tested), but a substantial subset are genuine N5 patterns with no test coverage. A learner who completes the questions cannot exercise more than half the grammar inventory.

**Fix:** Audit the list of uncovered patterns and add at least one MCQ question for every non-redirect pattern. This is a content-coverage task, not a correctness fix, but it directly affects the app's usefulness.

---

## 3. MEDIUM - pedagogical clarity

### 3.1 Audio quality - gTTS vs native vs VOICEVOX

**Current state:** The corpus has THREE audio states:
- Most items: skipped (no audio)
- Grammar items 184-187: `synthetic-gtts` (robotic, monotone, no pitch accent)
- Listening items 13-30: `synthetic-voicevox-shikoku-metan` (high-quality, natural prosody)

**Problem:** A learner clicking "play" on grammar example n5-184 vs listening item 14 will hear two very different voices and quality levels. The transition from gTTS to VOICEVOX is good news - VOICEVOX is far better - but the inconsistency suggests the TTS pipeline is mid-migration.

**Fix:**
1. Decide on one TTS backend and apply it everywhere. VOICEVOX is the right choice for N5 listening practice; gTTS is inadequate for a serious study tool.
2. Re-generate the 4 active gTTS items via VOICEVOX.
3. Generate audio for the 622 currently-skipped items so the corpus has full audio coverage.
4. For listening items specifically, consider mixing two voices (a male and a female VOICEVOX speaker) for dialogue items - currently all use the same `shikoku-metan` voice which means both A and B in a dialogue sound identical.

### 3.2 Listening dialogue items use a single voice

**Affected:** All listening items with multi-speaker dialogue (n5.listen.001, .002, .003, .004, .005, .006, .013, .014, .015, .016, .017, .018, .019, .020, .021, .022, .023, .024).

**Problem:** Items 13-30 declare `voice: "synthetic-voicevox-shikoku-metan"` - a single voice. Real JLPT N5 listening passages use distinct male/female speakers in dialogues. Without different voices, the learner has to track speaker identity by following 男/女/A/B/母/子/学生/先生 prefixes alone, which is harder than parsing voice differences.

**Fix:** For dialogue items, alternate two VOICEVOX speakers:
- Female lines: `shikoku-metan` (current)
- Male lines: `metan-male` or `kasukabe-tsumugi` or `aoyama-ryusei`
- Add a `speakers` field per item:
```json
"speakers": {
  "男": "voicevox-aoyama-ryusei",
  "女": "voicevox-shikoku-metan"
}
```
The audio generator reads this and uses different voices per speaker tag.

### 3.3 `listening.json` - some scripts contain Arabic numerals where readings could be ambiguous

**Examples:**
- n5.listen.001: `3時に えきの 前で どうですか。` (3 → さんじ)
- n5.listen.013: `9時はん` (9時 → くじ)
- n5.listen.020: `千五百円` - this one is correctly all-kanji.

**Observation:** When Arabic numerals appear in a Japanese sentence, the TTS engine has to infer the reading. `3時` could be read さんじ (correct) or さんじかん (wrong). VOICEVOX usually gets this right, but it's brittle. Standardizing on either kanji numerals or full kana would be safer.

**Fix (optional):** Replace Arabic numerals in listening scripts with kanji numerals OR with hiragana readings:
- `3時` → `三時` or `さんじ`
- `9時の でんしゃ` → `九時の でんしゃ` or `くじの でんしゃ`

This also makes the script more authentically Japanese.

### 3.4 Grammar pattern n5-031 - excellent rewrite, but example #3 risks ambiguity

**Current example 3:**
```
"ja": "あした こないの？"
"translation_en": "You're not coming tomorrow?"
```

**Note:** This is grammatically correct - 来ない (こない) + の = "you're not coming, are you?" or "you're not coming?". But for an N5 learner first encountering 来る's irregular conjugation, seeing the kana-only `こない` rather than `来ない` may confuse them about which verb is being negated.

**Fix:** Consider using a more transparent verb like `たべる` or `いく` for the third example:
```json
"ja": "ごはん 食べないの？"
"translation_en": "Aren't you going to eat?"
```

### 3.5 `vocab.json` - no kanji-form entry for 走る

The Group-1 ru-verb exception list shows `はしる` (kana-only form) flagged. But the kanji form 走 is NOT in the N5 kanji whitelist (it's N4), so this is consistent with the whitelist policy.

**Note:** Some standard N5 vocab lists (Bunpro, JLPT Sensei) do include 走 as N5. The corpus's narrower whitelist is a defensible editorial choice. Document the policy decision in the project README so future editors know the scope is "N5-strict" not "N5-permissive."

---

## 4. LOW - polish

### 4.1 `listening.json` - utterance items 25-30 have minimal scripts

**Examples:**
- n5.listen.025: `script_ja: "あさ 学校で 先生に 会いました。"` (single context line, no choices)
- n5.listen.026: `script_ja: "店で コーヒーを 買いたいです。"` (single line)

**Note:** Compared to items 9-12 which include numbered choices in the script (`1. xxx / 2. xxx / 3. xxx`), items 25-30 have only the situational context with no choices listed in the script. This suggests two different rendering conventions:
- Old style (9-12): choices embedded in script
- New style (25-30): choices in `choices` array only

**Fix:** Standardize on one approach. The new style (choices array only) is cleaner and avoids the script/choices mismatch problem from §1.1. Recommend migrating items 9-12 to remove the embedded choice list from their `script_ja`.

### 4.2 `kanji.json` - no `pos` field per kanji entry indicating frequency / lesson order

A small structural improvement: each kanji entry could carry an optional `lesson_order` or `frequency_rank` for the app to sequence kanji learning by frequency rather than dictionary order. Not a correctness issue, but a quality-of-life improvement for the runtime.

---

## 5. Cross-file consistency checks (to add to CI)

These are mechanical validations that should run on every change. They catch the bulk of issues found across audits and prevent regression.

1. Every kanji used anywhere in the corpus (grammar examples, kanji entries, reading passages, listening scripts, question stems, vocab forms) must be in `n5_kanji_whitelist.json`. **Status:** currently passing for all files.
2. Every kanji in `n5_kanji_whitelist.json` must have an entry in BOTH `n5_kanji_readings.json` AND `kanji.json`. **Status:** currently passing.
3. Every kun reading list must have no duplicates (run `len(kun) == len(set(kun))`). **Status:** failing for 10 entries (see §2.2).
4. Every listening utterance item's `script_ja` choices (when present) must match its `choices` array. **Status:** failing for n5.listen.011 (see §1.1).
5. Every `audio` field must resolve to a non-skipped entry in `audio_manifest.json`. **Status:** failing for listening items 13-30 (see §2.3).
6. Every `grammarPatternId` in `questions.json` must exist in `grammar.json`. **Status:** previously verified passing.
7. Every grammar pattern's example sentences must contain the pattern's literal form OR a documented inflection of it (catches the n5-185/186/187 propagation bug). **Status:** currently passing after the prior fixes.
8. No primary reading should be the on-yomi when the kanji's most common N5 use is as an i-adjective (high/long/cheap rule). **Status:** failing for 高/長/安 (see §2.1).

---

## 6. Per-file summary

### `n5_kanji_readings.json`
**Status:** Greatly improved. The 6 critical issues from the prior audit are 4-of-6 fixed. Remaining: primary-reading choices for 高/長/安 (HIGH), and 10 duplicate-kun-reading entries (HIGH).

### `n5_kanji_whitelist.json`
**Status:** Clean. 106 kanji listed, exactly matched to `kanji.json` entries. The previously missing kanji 力/手/足/目/口 have been added.

### `n5_vocab_whitelist.json`
**Status:** Largely clean. Group-1 ru-verb exceptions are now flagged. Some vocabulary used in `reading.json` (`しんごう`, `まがる`, `カフェ`, etc.) may still be missing - audit periodically against passage vocab.

### `kanji.json`
**Status:** 106 entries matching the whitelist exactly. No kanji missing or extra. Internal data structure is consistent.

### `vocab.json`
**Status:** 1003 entries. No vocab forms use non-N5 kanji. Group-1 exceptions correctly flagged. Solid.

### `grammar.json`
**Status:** 187 patterns. The previously broken patterns (n5-031 mislabel, n5-091 bad example, n5-184/185/186/187 copy-paste, n5-069 missing ぐ rule, n5-104 register mismatch) are all fixed. New issue: only 84 of 187 patterns have any associated question (see §2.4).

### `questions.json`
**Status:** 163 questions. No non-N5 kanji. The previously flagged unnatural q-0040 has been rewritten. Question coverage is partial (84 of 187 patterns referenced).

### `listening.json`
**Status:** Now 30 items (was 12). New items 13-30 use VOICEVOX synthesis. All scripts stay within N5 kanji scope. The N4 grammar in n5.listen.007 is fixed. Remaining issue: n5.listen.011 internal mismatch (CRITICAL - §1.1); audio manifest cross-reference (HIGH - §2.3).

### `audio_manifest.json`
**Status:** Mid-transition. 626 of 631 items skipped. New listening items 13-30 are not in manifest at all but have audio per their `voice` field. Mixed backend (gtts and voicevox). Needs regeneration (HIGH - §2.3).

---

## 7. Recommended next-step priorities

If only 5 things get worked on next, in this order:

1. **Fix the listening.011 script/choices mismatch (§1.1).** It is a direct grading bug.
2. **Regenerate `audio_manifest.json` to include listening items 13-30 (§2.3).** The data exists; the manifest just needs to know about it.
3. **Switch primary readings for 高/長/安 to kun-yomi (§2.1).** Three field edits, removes a known pedagogical defect.
4. **Deduplicate kun reading lists (§2.2).** Ten entries; mechanical fix.
5. **Add CI checks per §5.** Catches 95% of all the issues this audit and the previous ones found.

The deeper structural items (audio backend unification, question coverage gap, multi-voice dialogue audio) are larger projects and can come after.

---

## 8. Acceptance criteria

This work is complete when:

1. The CRITICAL item (§1.1) is fixed.
2. All HIGH items (§2.1, §2.2, §2.3, §2.4) are fixed or have a documented deferral.
3. The 8 cross-file CI checks (§5) all pass.
4. A native Japanese speaker reviews the listening.011 fix and confirms the polite-form choices read naturally.
5. The audio pipeline is stable on a single backend (preferably VOICEVOX with at least two speaker voices for dialogues).
6. Total entry counts unchanged unless explicitly documented (e.g., new questions added to close coverage gap §2.4).

---

## 9. Quick-reference issue summary

| Severity | ID | File | Issue |
|---|---|---|---|
| CRITICAL | 1.1 | listening.json | n5.listen.011 script choice 1 doesn't match choices array |
| HIGH | 2.1 | n5_kanji_readings.json | primary reading is on-yomi for 高/長/安 (should be kun) |
| HIGH | 2.2 | n5_kanji_readings.json | 10 entries have duplicate kun readings |
| HIGH | 2.3 | audio_manifest.json | listening items 13-30 absent from manifest despite having audio |
| HIGH | 2.4 | questions.json | only 84 of 187 grammar patterns have questions |
| MEDIUM | 3.1 | audio_manifest.json | mixed gTTS + VOICEVOX backends |
| MEDIUM | 3.2 | listening.json | dialogue items use a single voice (no speaker differentiation) |
| MEDIUM | 3.3 | listening.json | Arabic numerals in scripts may cause TTS reading ambiguity |
| MEDIUM | 3.4 | grammar.json | n5-031 example 3 uses kana-only conjugation of irregular verb 来る |
| MEDIUM | 3.5 | n5_vocab_whitelist.json | document the "N5-strict" scope policy explicitly |
| LOW | 4.1 | listening.json | utterance items inconsistent in whether script includes choices |
| LOW | 4.2 | kanji.json | no frequency/lesson-order field |

**Total remaining: 12 actionable items** (1 critical, 4 high, 5 medium, 2 low).

---

## 10. Comparison with previous audits

For reference, the trajectory across audits:

| Audit cycle | Critical | High | Medium | Low | Total |
|---|---|---|---|---|---|
| Initial markdown audit (KnowledgeBank, April 2026) | 5 | 7 | 9 | 6 | 27 |
| First JSON audit (April 2026) | 10 | 9 | 10 | 6 | 35 |
| `reading.json` focused audit (April 2026) | 5 | 5 | 6 | 4 | 20 |
| **This consolidated audit (May 2026)** | **1** | **4** | **5** | **2** | **12** |

The trajectory is positive. Most previously-flagged issues have been resolved. The remaining items are concentrated in two areas: kanji-readings polish (high but mechanical) and audio-pipeline maturity (high but a larger workstream).

---

*End of audit. Prepared 2026-05-01.*
