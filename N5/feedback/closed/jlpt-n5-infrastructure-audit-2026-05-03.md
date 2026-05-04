# JLPT N5 Tutor - Infrastructure & Data Files Audit

**Date:** 2026-05-03
**Audit scope:** the batch of 9 files uploaded for review:

- `audio_manifest.json` (708 entries, 108 KB) - audio path catalogue
- `questions.json` (288 questions, 238 KB) - the test/practice question bank
- `vocab.json` (1,003 entries, 378 KB) - re-check of the runtime vocab data
- `kanji.json` (106 entries, 68 KB) - re-check of the runtime kanji data
- `n5_vocab_whitelist.json` (951 entries, 15 KB) - vocabulary inclusion list
- `n5_kanji_whitelist.json` (106 entries, 1 KB) - kanji inclusion list
- `n5_kanji_readings.json` (106 entries, 13 KB) - canonical readings + primary
- `dokkai_kanji_exception.json` (25 entries, 1 KB) - non-N5 kanji allowed in dokkai
- `n5_kanji_whitelist_exceptions.md` - exception register (currently bootstrapping)

**Audit lens:** Japanese-language accuracy from a 日本語教師 perspective, plus cross-file consistency, schema integrity, and policy compliance.

**Comparison baseline:** data-files audit (2026-05-02) which flagged 10 items on grammar/vocab/kanji.

---

## 0. Executive summary

A lot of solid infrastructure work has landed in this batch. The exception-register pattern for non-N5 kanji in dokkai content is a clean policy formalization that addresses last cycle's vocab leakage debate (HIGH 2.2 in the content-files audit) head-on. The whitelist files are now consistent in size and complete in coverage. Coverage of grammar patterns by questions reached 100%.

But there are seams. Most are inconsistencies between the files in this batch itself, not within any single file. The pattern: the project is now operating with multiple sources of truth (`vocab.json` and `n5_vocab_whitelist.json`; `kanji.json`'s embedded readings and `n5_kanji_readings.json`'s canonical readings) and they don't all agree.

**Verified resolved since the previous data-files audit:**

- **POS-by-section bug (CRITICAL 1.1) fully fixed.** All 24+ entries previously affected (Section 14 i-adjectives, Section 20 colors, Section 30 verb-2 group, Section 12 adverbs) now carry their correct POS tags. This was the largest pedagogical risk in the corpus.
- **n5.vocab.37-common-nouns-miscella.はんぶん form/reading swap (HIGH 2.1) fixed.** Now `form: "半分"`, `reading: "はんぶん"`. (One small follow-on: see §3.1.)
- **Kanji duplicate examples (MEDIUM 3.2) fully fixed.** Zero kanji entries with duplicate examples now (was 10).
- **Reading whitelist conformance** holds across all 40 reading passages.
- **Coverage of grammar patterns by questions: 100%** (was ~63% before Pass-15 coverage batch). Every one of the 177 patterns has at least one question.

**Still outstanding from prior audits (carried forward):**

- 132 vocab entries lack examples (HIGH 2.4 from data-files audit) - unchanged.
- 32 stub patterns from F-19 dedup (LOW 4.1) - unchanged, treated as deliberate.

**Total NEW actionable items from this batch: 9** (1 critical, 4 high, 3 medium, 1 low).

---

## 1. CRITICAL

### 1.1 `n5_kanji_readings.json` - 3 primary readings don't match how the kanji is used at N5

The `primary` field is the single most important field in this file - it determines which reading the runtime surfaces by default for a given kanji. Three primary readings are pedagogically wrong for N5:

| Kanji | Current `primary` | Should be | Evidence (from `kanji.json` examples) |
|---|---|---|---|
| 語 | `かた` (kun) | `ご` (on) | All 3 examples use ご: 外国語 (がいこくご), 中国語 (ちゅうごくご), 日本語 (にほんご). Zero examples use かた. かた is N1+ literary. |
| 天 | `あめ` (kun) | `てん` (on) | Both examples use てん: 天気 (てんき), 天ぷら (てんぷら). あめ for 天 alone (not 雨) is rare/literary. |
| 入 | `い` (kun) | `はい` (kun) | The standard verb 入る reads はいる, not いる. The example list correctly shows 入る = はいる. The `い` reading is for compounds like 入れる (いれる) but that's the secondary kun. |

**Why this is critical:** these three kanji are foundational to N5 vocab. 日本語 (にほんご, "Japanese language") appears in the N5 self-introduction context, on title cards, in nearly every textbook. 天気 (てんき, "weather") is one of the first 50 N5 nouns. 入る (はいる, "to enter") is a Group-2-look-alike Group-1 verb that needs careful handling - and getting its reading wrong is bad pedagogy.

A learner who looks up 語 in this app sees `かた` as the primary reading and forms a false expectation that the kanji 語 is read かた. They then read 日本語 and have to unlearn that.

**Evidence this is purely a data-file bug:** the project's other infrastructure is correct - the kanji.json examples use the right readings, the vocab.json entries have the right glosses, the questions.json tests use these words correctly. Only `n5_kanji_readings.json`'s `primary` field is wrong.

**Suggested fix:** for these three kanji, set `primary` to: 語 → ご, 天 → てん, 入 → はい.

**Also flag (debatable but worth review):**
- **間** primary=`あいだ` while both examples use compound かん (時間, 一時間). At N5, 〜時間, 一週間, 三日間 are dominant. This explains why listening item 036's "三日かん" with kana spelling - the primary points away from かん so the spelling defaults to kana. Fixing primary to かん would let 三日間 be written naturally.

**Severity:** Critical. Three readings are clearly wrong and one (間) is questionable enough to merit a decision. These are visible to every user who consults a kanji card.

---

## 2. HIGH

### 2.1 `audio_manifest.json` - backslash paths conflict with forward-slash paths in reading.json / listening.json

**Audio_manifest.json uses backslash:**
```json
{"id": "reading.n5.read.001", "path": "audio\\reading\\n5.read.001.mp3", ...}
```

**reading.json and listening.json use forward slash:**
```json
{"id": "n5.read.001", ..., "audio": "audio/reading/n5.read.001.mp3"}
```

**Problem:** if any code consumes the manifest path directly (without normalization), it will fail in a web/PWA context. Browsers fetch with forward-slash URLs; backslash is a Windows file-system convention only. Even on a Windows-served web app, `fetch("audio\\reading\\n5.read.001.mp3")` is interpreted as a single-segment URL with literal backslashes.

The fix is either:
1. Normalize manifest paths to forward slash at write time (recommended), or
2. Document a mandatory normalization step at consume time.

The manifest was likely generated on a Windows build system using `os.path.join()` which used `\` as the separator. On POSIX builds the same code would produce `/`. If the build is multi-platform, this needs `pathlib.PurePosixPath` or explicit `.replace('\\', '/')` at serialization.

**Severity:** High. Runtime-breaking on PWA deployment.

### 2.2 `audio_manifest.json` - 688 of 708 items are `skipped: true` (97% missing audio)

**Breakdown:**
- 628 of 628 grammar items: skipped (zero audio for grammar examples)
- 30 of 40 reading passages: skipped (only 31-40 have audio)
- 30 of 40 listening items: skipped (only 31-40 have audio)
- Only 20 items (the newest 10 reading + 10 listening) have actual audio

**Problem:** the audio infrastructure exists, the file paths are declared in reading.json and listening.json, but for the older 30 of each (the ones from before the most recent batch), no audio file exists. The PWA's audio button will be present in the UI for items where `audio` is declared in the JSON, but clicking it will 404.

This isn't necessarily wrong if the project is deliberately building audio incrementally. But the consumer code needs to either:
- Check `audio_manifest.json[id].skipped` before showing the play button, OR
- Hide the button for older items, OR
- Generate placeholder audio so the older items at least don't 404

**Severity:** High. UX bug visible to users on at least 60 of 80 reading/listening items.

### 2.3 `questions.json` - `_meta` is significantly stale (off by 65 questions)

**`_meta` says:**
```json
"question_count": 223,
"type_distribution": {"mcq": 193, "sentence_order": 16, "text_input": 14},
"id_range": {"first": "q-0001", "last": "q-0513"}
```

**Actual:**
- question_count: 288 (off by 65)
- mcq: 258 (off by 65)
- last id: q-0578 (off by 65)

Looking at the audit_history field, the most recent documented pass is "Pass-15 coverage batch (2026-05-01): authored 25 mcq (q-0479..0503) ... Bank: 198 -> 223." After that, 75 more questions were added (q-0504..0578) with no audit_history entry and no count update.

Spot-checking q-0504..0578 (sampled 15): all are well-formed mcq questions with valid grammar pattern references, natural Japanese, plausible distractors, and detailed explanations. The new questions are not a quality problem; only the metadata is stale.

**Why this matters:** any tooling that reads `_meta.question_count` (test runners, coverage reports, dashboards) will report stale numbers. The audit_history field is supposed to be the canonical record of this corpus's history; missing the most recent 75-question addition breaks that trust.

**Severity:** High. Documentation drift, not a content error, but the count discrepancy is large enough to mislead.

### 2.4 `questions.json` - 65 em-dashes (style policy violations)

64 em-dashes spread across 46 questions, mostly in `explanation_en` and `distractor_explanations` fields. Examples:

- q-0007: "...は can sound contrastive — 'as for cats, [I] like [them], but...' — which is N3+ nuance..."
- q-0008: "...は can topicalize 'books' for contrastive nuance — 'as for books, [I] read [them], but...' — ..."
- q-0044: "...the recipient — the person being called..."
- q-0488: 4 em-dashes in a single explanation about frequency adverbs

**Problem:** the project's documented style policy prohibits U+2014 em-dashes in user-facing strings. These appear in explanations that get rendered to learners. Same class of issue as the previously-flagged grammar.json em-dashes (which were partially cleaned up - 4 remain there).

**Severity:** High by count. 65 mechanical replacements across 46 questions. Recommended fix: use hyphen-with-spaces ` - ` or split into two sentences.

---

## 3. MEDIUM

### 3.1 `n5_vocab_whitelist.json` - 1 stale entry: missing 半分, has only old はんぶん

After the previous data-files audit fix, n5.vocab.37-common-nouns-miscella.はんぶん changed from `form: "はんぶん"` to `form: "半分"`. But the whitelist still contains the old kana form `はんぶん` and not the new kanji form `半分`.

```
n5_vocab_whitelist.json: 'はんぶん' present, '半分' absent
vocab.json: form='半分', reading='はんぶん' (id still uses はんぶん in the path)
```

Cross-check: vocab.json has 1 form not in the whitelist (`半分`), and the whitelist has 23 items not in vocab.json - of those 23, most are alternate readings/spellings (いい, いえ, さくら, スペイン人) that are deliberately admitted as recognizable forms even if not in the formal lexicon. So the whitelist is bigger than vocab forms by design.

The 半分 missing entry is the one anomaly: a vocab.json form that should be in the whitelist but isn't, because the whitelist wasn't updated when the form changed.

**Suggested fix:** either add `半分` to the whitelist, or replace `はんぶん` with `半分` in the whitelist. (My recommendation: add `半分` AND keep `はんぶん` so that text-search / fuzzy matching works against either spelling.)

**Severity:** Medium. Minor data drift; impact depends on whether any consumer uses the whitelist as a "known forms" check.

### 3.2 `n5_kanji_readings.json` vs `kanji.json` - inconsistent `kun` list ordering for 入

```
n5_kanji_readings.json: 入 kun = ["はい", "い"]
kanji.json:             入 kun = ["い", "はい"]
```

Both files have the same readings, but in opposite order. Since the cover.md precedence rule says "first kun is primary unless explicit primary_reading set," the order matters. n5_kanji_readings.json is the "more correct" order (はい first, matching 入る = はいる) but its own `primary` field overrides this with the wrong value.

The kanji.json file should match n5_kanji_readings.json ordering for consistency. Better: kanji.json should ALSO carry the explicit `primary_reading` field for any kanji where the choice matters (currently only 4 kanji - 高/長/安/白 - have it set in kanji.json; the other 102 rely on first-in-list precedence).

**Severity:** Medium. Subtle but affects which reading the runtime surfaces if it consumes kanji.json directly.

### 3.3 `kanji.json` - explicit `primary_reading` field set for only 4 of 106 kanji

Only `高`, `安`, `長`, `白` have explicit `primary_reading`. The other 102 fall through to the precedence rule (first kun, else first on).

**Problem:** `n5_kanji_readings.json` carries `primary` for ALL 106 kanji, with deliberately chosen values that sometimes deviate from "first kun." For example:
- 月: kun=["つき"], on=["げつ","がつ"], n5_kanji_readings.json primary="がつ"
- 人: kun=["ひと"], on=["じん","にん"], n5_kanji_readings.json primary="にん"
- 日: kun=["ひ"...], on=["にち","じつ"], n5_kanji_readings.json primary="にち"

Per kanji.json's first-kun precedence, these would surface as つき / ひと / ひ. Per n5_kanji_readings.json, they surface as がつ / にん / にち.

These are different runtime answers depending on which file the consumer reads.

**Suggested fix:** either (a) propagate the `primary` from n5_kanji_readings.json into kanji.json's `primary_reading` field for all 106 entries, or (b) document that n5_kanji_readings.json is the canonical source and kanji.json's reading data is for display only.

**Severity:** Medium. Two sources of truth disagree on default reading for non-trivial cases.

---

## 4. LOW

### 4.1 `audio_manifest.json` - some grammar audio paths suggest non-existent grammar question IDs

The manifest has 628 grammar audio entries with IDs like `grammar.n5-001.0`, `grammar.n5-001.1` ... `grammar.n5-001.4`. These appear to be one entry per `examples[i]` in each grammar pattern. With 177 patterns averaging ~5 examples each = ~885 expected entries; actual is 628. Some patterns have fewer examples, others have more, so this is roughly consistent.

But: the manifest carries audio entries for retired patterns. For example, n5-128 was retired in F-19 dedup pass, but the manifest has no `grammar.n5-128.*` entries (verified). Good. Stub patterns like n5-040 (dedup of n5-015) DO have manifest entries (n5-040.0, n5-040.1, etc.) - presumably the same audio as the canonical pattern. That's wasteful (5 duplicate audio files per stub × 32 stubs ≈ 160 redundant entries) but not actively wrong.

**Severity:** Low. Storage waste, not a correctness issue.

---

## 5. Cross-cutting good news

- **dokkai_kanji_exception.json is well-designed.** The 25-kanji exception list is bounded, justified by reading-passage authenticity, and documents the policy crisply: dokkai may use these; reading.json stays strict; bunpou/moji/goi must stay strict. This formalizes the answer to last cycle's HIGH 2.2 vocab leakage question.
- **n5_kanji_whitelist_exceptions.md is correctly empty (bootstrapping mode).** The contract is sensible: when `n5_official_kanji_scope.json` is added, JA-25 begins enforcing accountability for any whitelist additions beyond the canonical 103. Until then, the file is a placeholder with the correct intent documented.
- **All 40 reading passages stay within (whitelist + dokkai exceptions).** Whitelist conformance is clean.
- **All 177 grammar patterns have at least one question** (was ~63% pre-coverage-batch).
- **All 288 questions reference valid grammar pattern IDs** (zero broken refs).
- **Whitelist file sizes are coherent**: 106 kanji whitelist matches 106 kanji.json entries matches 106 n5_kanji_readings.json entries.

---

## 6. Recommended next-step priorities

If only 5 things get worked on:

1. **Fix the three primary readings in `n5_kanji_readings.json`** (§1.1). 語→ご, 天→てん, 入→はい. Three-line edit. Highest pedagogical impact.
2. **Normalize audio_manifest.json paths to forward slash** (§2.1). Either at write time or as a one-time sweep. Otherwise PWA deployment breaks.
3. **Decide on the audio button UX** for items with `skipped: true` (§2.2). Either generate placeholder audio, or hide the button when manifest says skipped.
4. **Refresh `_meta` in questions.json** (§2.3). Update count, type_distribution, id_range, and add an audit_history entry covering q-0504..0578.
5. **Sweep questions.json em-dashes** (§2.4). 65 mechanical replacements. The em-dash style violation is now the single largest accumulated style-policy debt in the corpus.

The remaining items (whitelist `半分` entry, kanji.json/readings inconsistency, 102 missing primary_reading fields) are polish-grade and can be batched.

---

## 7. Quick-reference issue summary

| Severity | ID | File | Issue |
|---|---|---|---|
| CRITICAL | 1.1 | n5_kanji_readings.json | 3 primary readings wrong (語=かた, 天=あめ, 入=い); 1 debatable (間=あいだ) |
| HIGH | 2.1 | audio_manifest.json | Backslash paths conflict with forward-slash paths in reading/listening |
| HIGH | 2.2 | audio_manifest.json | 97% of audio entries marked skipped; UX bug if consumer doesn't gate the play button |
| HIGH | 2.3 | questions.json | _meta stale by 65 questions; audit_history missing latest q-0504..0578 batch |
| HIGH | 2.4 | questions.json | 65 em-dashes across 46 questions (style policy violation) |
| MEDIUM | 3.1 | n5_vocab_whitelist.json | Stale entry: has old `はんぶん`, missing new `半分` after vocab.json fix |
| MEDIUM | 3.2 | n5_kanji_readings.json vs kanji.json | 入 kun list order differs between the two files |
| MEDIUM | 3.3 | kanji.json | Only 4 of 106 entries have explicit primary_reading; rest disagree silently with n5_kanji_readings |
| LOW | 4.1 | audio_manifest.json | Stub patterns get ~160 redundant audio entries (same audio as canonical pattern) |

**Total: 9 actionable items** (1 critical, 4 high, 3 medium, 1 low).

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
| **Infrastructure files audit (May 3, this audit)** | **1** | **4** | **3** | **1** | **9** |

Steady cadence. The number of issues per cycle has stabilized around 9-14 as the corpus matures and audits dig into more peripheral surfaces (whitelists, manifests, exception registers). The CRITICAL counts have come down from the early "10 critical issues" to "1 per cycle" - and each cycle's critical issue is increasingly narrow in scope. This audit's CRITICAL is three primary-reading fixes (a 30-second edit), not a systemic content quality issue.

---

*End of audit. Prepared 2026-05-03.*
