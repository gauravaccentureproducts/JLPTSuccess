# JLPT N5 Tutor - Data Files Audit (grammar.json, vocab.json, kanji.json)

**Date:** 2026-05-02
**Audit scope:** three JSON data files at the heart of the runtime corpus:
- `grammar.json` (177 patterns, 481 KB)
- `vocab.json` (1,003 entries, 378 KB)
- `kanji.json` (106 entries, 69 KB)

**Audit lens:** Japanese-language accuracy, internal cross-file consistency, and runtime data integrity. Cross-checked against `n5_kanji_whitelist`, `n5_vocab_whitelist`, and the `cover.md` policy in the most recent native-reviewer dossier.

**Comparison baseline:** native-reviewer dossier follow-up audit (2026-05-02) which found zero remaining issues in the dossier-extracted view. This audit looks at the underlying full JSON files, which contain content not surfaced in the dossier markdown views.

---

## 0. Executive summary

The runtime data files are in mostly strong shape. All previous high-priority issues from the dossier audit cycle (kanji whitelist conformance, primary readings for 高/長/安/白, freq rank duplicates, tier classifications for n5-052 / n5-145 / n5-146 / n5-158 / n5-171 / n5-174-182, the しゃこうご typo in n5-152, the n5-175 example mismatch) are confirmed resolved in the runtime JSON.

**Verified resolved across files:**

- Zero non-N5 kanji in any vocab `form`, grammar example, or kanji compound example.
- All 106 kanji have unique `lesson_order` and `frequency_rank` values.
- All 106 kanji have stroke_order_svg paths declared.
- All kanji previously flagged for primary-reading issues (高, 長, 安, 白) now carry an explicit `primary_reading` field with the kun-yomi value.
- 24 patterns now correctly tier=`late_n5` matching the project's source markdown.
- Broken references to retired patterns are not in user-facing fields - they're in cross-reference contrast metadata.

**Remaining issues fall into four categories**:

1. **POS classification by thematic section** (the largest pattern by number of affected entries): vocab entries cross-listed in thematic sections like "Nature and Weather" or "Colors" inherit a section-default POS tag rather than their actual linguistic POS, producing internally contradictory entries.
2. **Stale cross-references**: 10 references in grammar.json point to patterns retired in the F-19 dedup pass.
3. **Tier inconsistency**: one pattern (n5-134, ので) is tier=`core_n5` but the project's own notes elsewhere call it "Upper N5 / borderline."
4. **One specific data error**: vocab entry n5.vocab.37-common-nouns-miscella.はんぶん has `form` and `reading` swapped.

Total actionable items: 10 (1 critical, 4 high, 3 medium, 2 low).

---

## 1. CRITICAL - factual or runtime-breaking errors

### 1.1 `vocab.json` - thematic sections mass-stamp POS regardless of word's actual POS

This is the largest issue in the corpus by number of affected entries. The `pos` field on a vocab entry should reflect the word's actual part of speech. In practice, however, vocabulary cross-listed in thematic sections (sections 1-26 and 37-40) is stamped with a single section-default POS, rather than the word's correct POS.

**Verified examples:**

**Section 14 "Nature and Weather":** all 34 entries are `pos: "noun"`. But four of them are i-adjectives:

| ID | form | actual POS | tagged POS |
|---|---|---|---|
| n5.vocab.14-nature-and-weather.あつい | あつい | i-adj | noun ✗ |
| n5.vocab.14-nature-and-weather.さむい | さむい | i-adj | noun ✗ |
| n5.vocab.14-nature-and-weather.すずしい | すずしい | i-adj | noun ✗ |
| n5.vocab.14-nature-and-weather.あたたかい | あたたかい | i-adj | noun ✗ |

The same words are cross-listed in section 31 "i-Adjectives" with the correct `pos: "i-adj"`. So the runtime can fetch either copy, and they disagree.

**Section 20 "Colors":** all 14 entries are `pos: "noun"`. But five of them are i-adjectives whose own gloss text says "(adj)":

| ID | form | gloss | tagged POS |
|---|---|---|---|
| n5.vocab.20-colors.白い | 白い | "white (adj)" | noun ✗ |
| n5.vocab.20-colors.くろい | くろい | "black (adj)" | noun ✗ |
| n5.vocab.20-colors.あかい | あかい | "red (adj)" | noun ✗ |
| n5.vocab.20-colors.あおい | あおい | "blue (adj)" | noun ✗ |
| n5.vocab.20-colors.きいろい | きいろい | "yellow (adj)" | noun ✗ |

The gloss explicitly contradicts the POS tag. Same words in section 31 are correctly `pos: "i-adj"`.

**Section 12 "Time - Frequency / Sequence":** all 19 entries are `pos: "noun"`. But many of them are adverbs:

| ID | form | actual POS | tagged POS |
|---|---|---|---|
| n5.vocab.12-time-frequency-sequen.いつも | いつも | adverb | noun ✗ |
| n5.vocab.12-time-frequency-sequen.よく | よく | adverb | noun ✗ |
| n5.vocab.12-time-frequency-sequen.時々 | 時々 | adverb | noun ✗ |
| n5.vocab.12-time-frequency-sequen.たまに | たまに | adverb | noun ✗ |
| n5.vocab.12-time-frequency-sequen.あまり | あまり | adverb | noun ✗ |
| n5.vocab.12-time-frequency-sequen.ぜんぜん | ぜんぜん | adverb | noun ✗ |
| n5.vocab.12-time-frequency-sequen.すぐ | すぐ | adverb | noun ✗ |
| n5.vocab.12-time-frequency-sequen.もう | もう | adverb | noun ✗ |
| n5.vocab.12-time-frequency-sequen.まだ | まだ | adverb | noun ✗ |
| n5.vocab.12-time-frequency-sequen.はじめて | はじめて | adverb | noun ✗ |

These are cross-listed in section 33 "Adverbs" with the correct `pos: "adverb"`.

**Section 30 "Verbs - Existence and Possession":** all 10 entries are `pos: "verb-1"`. But four of them are Group 2 (verb-2 / ichidan) verbs:

| ID | form | actual POS | tagged POS |
|---|---|---|---|
| n5.vocab.30-verbs-existence-and-p.いる | いる (exist) | verb-2 | verb-1 ✗ |
| n5.vocab.30-verbs-existence-and-p.あげる | あげる | verb-2 | verb-1 ✗ |
| n5.vocab.30-verbs-existence-and-p.くれる | くれる | verb-2 | verb-1 ✗ |
| n5.vocab.30-verbs-existence-and-p.かりる | かりる | verb-2 | verb-1 ✗ |

This is the most pedagogically dangerous case: `pos: "verb-1"` vs `pos: "verb-2"` directly determines conjugation rules. A learner using a flashcard or quiz powered by the section 30 copy of `あげる` would be told this is a Group 1 (う-verb) verb, leading them to conjugate it as `あげります` (wrong) instead of `あげます` (correct). The same word's section 28 entry has the correct `pos: "verb-2"`.

**Other sections affected (smaller counts):** 4 (Body Parts), 5 (Demonstratives), 6 (Question Words), 7 (Numbers), 21 (Clothing), 26 (House and Furniture). Total verified mistags from cross-listing comparison alone: **24 entries.**

The lower bound is 24. The true count is likely higher, since many words appear ONLY in their thematic section without a POS-organized cross-listing to reveal the discrepancy.

**Severity:** Critical. The POS field is functional metadata that drives conjugation, dictionary lookup, and POS-filtered quizzing. Wrong POS in 24+ entries with verb-class confusion in section 30 is a teaching bug.

**Suggested fix:** Either (a) mark thematic-section copies as derivative and require them to copy POS from the canonical entry, or (b) retire the cross-listings entirely and let the runtime expose words via a tag system rather than duplicate entries.

---

## 2. HIGH - inconsistencies that hurt credibility

### 2.1 `vocab.json` - はんぶん entry has `form` and `reading` swapped

**Affected entry:**
```json
{
  "id": "n5.vocab.37-common-nouns-miscella.はんぶん",
  "form": "はんぶん",
  "reading": "半分",
  "gloss": "half",
  "section": "37. Common Nouns - Miscellaneous",
  "pos": "noun",
  "examples": [
    { "ja": "ケーキを はんぶん 食べました。",
      "translation_en": "I ate half the cake." }
  ]
}
```

**Problem:** the `form` field should be the headword (typically with kanji where N5 allows), and `reading` should be the kana pronunciation. Here they're inverted: `form` is the kana `はんぶん`, `reading` is the kanji `半分`.

The spelled-out reading is `はんぶん`, not `半分`. Both 半 and 分 are in the N5 kanji whitelist, so `半分` is a valid form. The cleanest fix is `form: "半分", reading: "はんぶん"`. This is the only entry with this specific bug; sweeping the file confirms.

**Severity:** High. Every other reading-field check came back clean; this single entry will trip up reading-display, search, and any reading-quiz feature.

### 2.2 `grammar.json` - 10 cross-references point to retired patterns

The F-19 dedup pass retired 10 patterns: `n5-012, n5-020, n5-022, n5-032, n5-047, n5-128, n5-138, n5-139, n5-140, n5-141`. References to them remain in two fields:

**Broken `contrasts.with_pattern_id` references:**
- n5-023 contrasts with n5-012 (retired)
- n5-024 contrasts with n5-012 (retired)
- n5-031 contrasts with n5-012 (retired)
- n5-126 contrasts with n5-128 (retired)
- n5-133 contrasts with n5-128 (retired)
- n5-134 contrasts with n5-128 (retired)

**Broken `form_rules.conjugations.label` "See n5-XXX" references:**
- n5-023 form-rules see-also -> n5-012 (retired)
- n5-024 form-rules see-also -> n5-012 (retired)
- n5-031 form-rules see-also -> n5-012 (retired)
- n5-133 form-rules see-also -> n5-128 (retired)

**Problem:** A learner browsing the n5-031 entry will see "Pairs with n5-012 (formal か)" in the notes and "See n5-012" in the form rules. Clicking through (if the runtime renders these as links) will hit a 404 because n5-012 no longer exists. Static notes are easier to forgive, but the form_rules see-also is structured data the runtime is likely to act on.

**Severity:** High. Direct runtime-integrity bug introduced by the retirement pass.

### 2.3 `grammar.json` n5-134 - tier inconsistency for ので

**Affected entry:** n5-134 (Sentence + ので、Sentence) is `tier: "core_n5"`.

**But:** n5-009 (から)'s notes field reads:

> "Note ので is a softer, more polite alternative for 'because' (Upper N5 / borderline)."

So the corpus internally states ので is borderline, while the ので-specific pattern is tagged core. This contradicts the project's own classification.

The previous markdown audit cycle already established that the project's `grammar_n5.md` source tags ので as "(Upper N5 / borderline)". Per the dossier audit's tier-classification standard, n5-134 should be `tier: "late_n5"`.

**Severity:** High. Same class of issue as the previously-fixed 14-pattern tier sweep, but this one wasn't caught.

**Suggested fix:** change n5-134 to `tier: "late_n5"`. Optionally also re-check n5-126 (が conjunction) which is core_n5 - the conjunction-が is borderline-N5 in many sources too, though the case for keeping it core_n5 is defensible since it's introduced in Genki I.

### 2.4 `vocab.json` - 132 entries (13%) have no `examples`

**Distribution by POS:**

| POS | Count without examples |
|---|---|
| noun | 41 |
| demonstrative | 21 |
| verb-1 | 19 |
| i-adj | 8 |
| expression | 7 |
| question-word | 6 |
| adverb | 6 |
| conjunction | 6 |
| pronoun | 5 |
| verb-2 | 5 |
| particle | 5 |
| counter | 2 |
| na-adj | 1 |

**Problem:** Function-word categories (particle, demonstrative, conjunction) reasonably need fewer examples since their grammar-pattern entries provide examples. But 41 nouns and 27 verbs without any example sentence is a content gap. Vocab entries typically benefit from at least one example showing the word in natural context, especially for words with multiple senses.

**Severity:** High (content completeness) - though calibratable based on whether the runtime fills these gaps from grammar.json `examples[].vocab_ids` cross-references.

---

## 3. MEDIUM - quality and clarity

### 3.1 `vocab.json` - Section 38 "Sounds and Voice" still present despite dossier removal

**Current state:** Section 38 contains 3 entries (こえ, おと, うた), all correctly tagged `pos: "noun"` in vocab.json.

**Problem:** During the native-reviewer dossier preparation, these three entries were tagged `[interjection]` (which was wrong). The fix in `02_vocab_borderline.md` removed the section entirely. But vocab.json still has the section.

**Either:**
- (a) Section 38 is a deliberate retention in the runtime - in which case the "removal" in the dossier file was incorrect framing; the section just got filtered out of the borderline view.
- (b) The dossier removal signaled that these entries should be merged into another section (e.g., 37 Common Nouns - Miscellaneous), and the merge wasn't performed in vocab.json.

**Severity:** Medium. Not a runtime error - the entries are correctly tagged here. But the inconsistency between the dossier's "removed" status and the runtime's "still present" status is worth resolving so the next reviewer cycle doesn't ask "what happened to こえ?"

### 3.2 `kanji.json` - 10 kanji entries have duplicate examples

**Affected kanji:** 月, 水, 校, 本, 前, 気, 道, 白, 名, 号.

**Examples:**
```
月: examples include
   { "form": "月", "reading": "つき", "gloss": "moon" }
   { "form": "月", "reading": "つき", "gloss": "month, moon" }

名: examples include
   { "form": "名前", "reading": "なまえ", "gloss": "name" }
   { "form": "名前", "reading": "なまえ", "gloss": "name (also in §37)" }

号: examples include
   { "form": "番号", "reading": "ばんごう", "gloss": "number" }
   { "form": "番号", "reading": "ばんごう", "gloss": "number (also in §24)" }
```

**Problem:** the duplicates appear to come from vocab cross-listing leaking into the kanji-example join. When 名前 appears in both vocab section 1 and section 37, the kanji-entry join produces two rows. The "(also in §37)" gloss suffix confirms this.

A learner viewing the 名 kanji card sees "name" listed twice, which looks like a data bug.

**Severity:** Medium. Visible inconsistency, no runtime crash.

**Suggested fix:** in the build pipeline, deduplicate kanji examples by (form, reading) keypair, preferring the cleaner gloss without the cross-listing annotation.

### 3.3 `grammar.json` - 8 em-dashes / en-dashes against project's no-em-dash policy

**Locations:**

```
grammar.json — em-dashes (U+2014):
- explanation_en for "9時に — specific time + に. かいぎ (meeting)..."
- explanation_en for "何時に — question word for clock-time + に..."
- explanation_en for "12時に — midnight bedtime..."
- translation_en "Why didn't you go? — Because I had a fever."
- translation_en "Why did you skip school? — Because I had a headache."
- meaning_en "～んです / ～のです — explanation, emphasis, or asking..."

grammar.json — en-dashes (U+2013):
- form_rules label "Paired with から (from–to)"
- common_mistakes why "Order is start–end: から first, then まで."
```

**Problem:** the project's documented style policy (multiple prior briefs) prohibits em-dashes (U+2014) and en-dashes (U+2013) in user-facing strings. The fix is to replace with hyphen-with-spaces ` - ` or with a colon. These are 8 mechanical replacements.

**Severity:** Medium (style policy compliance). Visible to any reader rendering these fields.

---

## 4. LOW - polish

### 4.1 `grammar.json` - 32 stub patterns with see-also-only form_rules add little value

The dedup pass left behind 32 patterns whose `form_rules.conjugations` consists of a single entry with `form: "see_also"` pointing to a canonical pattern. These stubs DO carry full `examples` and `explanation_en`, so they're not empty - but they duplicate canonical content and increase the pattern count without adding pedagogical surface area.

Examples: n5-040 (this/that+N) is a stub for n5-015. n5-115 (specific time に) is a stub for n5-005. n5-184/185/186/187 are stubs for n5-183.

**Severity:** Low. The stubs serve a discoverability purpose (a learner browsing the "Demonstratives" category finds n5-040; the canonical pattern is in another category). Worth documenting as a deliberate design choice, or considering whether the runtime could surface the same content via tag-based discovery without the duplicate entries.

### 4.2 `kanji.json` - 大人 example (おとな) uses irregular jukujikun reading without note

The 大 kanji's examples include:
```
{ "form": "大人", "reading": "おとな", "gloss": "adult" }
```

**Problem:** 大人 is a jukujikun (special kanji-to-meaning compound where the reading doesn't follow individual kanji readings). 大 here doesn't read as either of its on-yomi (だい/たい) or kun-yomi (おお). A learner studying 大 readings might be confused why おとな doesn't match.

**Severity:** Low. Not strictly wrong - the example is valid - but a one-line note flagging "irregular compound reading" would help. Most kanji apps flag jukujikun explicitly.

---

## 5. Cross-cutting observations

### 5.1 Em-dash check across files

| File | Em-dashes (U+2014) | En-dashes (U+2013) |
|---|---|---|
| grammar.json | 6 | 2 |
| vocab.json | 0 | 0 |
| kanji.json | 0 | 0 |

Only grammar.json has dash-policy violations, and only 8 of them. Quick fix.

### 5.2 Whitelist conformance

| File | Field checked | Non-N5 kanji found |
|---|---|---|
| vocab.json | form | 0 |
| grammar.json | examples[].ja | 0 |
| kanji.json | examples[].form | 0 |

Clean across all three files. No whitelist violations.

### 5.3 ID uniqueness

| File | Total entries | Unique IDs |
|---|---|---|
| vocab.json | 1003 | 1003 |
| grammar.json | 177 | 177 |
| kanji.json | 106 | 106 |

Clean.

### 5.4 Cross-file references

`grammar.json` examples carry `vocab_ids` arrays. **Zero broken references** - every cited vocab_id resolves to a vocab.json entry. This is excellent linkage hygiene.

---

## 6. Per-file summary

### `vocab.json`
**Status:** Largely correct content but with one systematic POS-classification issue affecting 24+ entries (1.1), one form/reading swap (2.1), and 132 entries lacking examples (2.4). Whitelist-clean and structurally sound.

### `grammar.json`
**Status:** Strong. 24 patterns correctly tier=late_n5; all 177 patterns have all required fields populated; vocab cross-references are 100% intact. Remaining: 10 stale references to retired patterns (2.2), one tier inconsistency for ので (2.3), 32 stub patterns from the dedup pass (4.1), 8 em-dashes (3.3).

### `kanji.json`
**Status:** Substantially improved. All 106 kanji have stroke_order_svg paths; lesson_order and frequency_rank are unique 1-106; explicit primary_reading set for the previously-flagged adjective kanji; no duplicate kun readings. Remaining: duplicate examples within 10 kanji entries (3.2), one jukujikun-not-flagged note (4.2).

---

## 7. Recommended next-step priorities

If only 5 things get worked on next:

1. **Fix the POS-by-section bug (§1.1).** Either standardize POS to the canonical entry's value, or retire thematic-section duplicates entirely. This is the largest pedagogical risk in the corpus today.
2. **Fix the n5.vocab.37-common-nouns-miscella.はんぶん form/reading swap (§2.1).** Two-field edit.
3. **Fix the 10 stale cross-references to retired patterns (§2.2).** Either remove the references or repoint them to the canonical replacements.
4. **Re-tier n5-134 (ので) to late_n5 (§2.3).** Single-field edit consistent with the project's own internal classification.
5. **Add a build-time CI check** that flags any vocab entry whose POS differs from its cross-listed twin's POS. This catches the §1.1 class of issue mechanically and prevents regression.

The remaining items (em-dashes, kanji duplicate examples, jukujikun notes, vocab examples coverage) are polish and can be batched into a later cycle.

---

## 8. Quick-reference issue summary

| Severity | ID | File | Issue |
|---|---|---|---|
| CRITICAL | 1.1 | vocab.json | Thematic sections (12, 14, 20, 30, etc.) mass-stamp section-default POS over actual word POS; 24+ entries affected with verb-1/verb-2 confusion in section 30 |
| HIGH | 2.1 | vocab.json | n5.vocab.37-common-nouns-miscella.はんぶん has form and reading swapped |
| HIGH | 2.2 | grammar.json | 10 cross-references (6 contrasts + 4 form_rules see-also) point to retired patterns |
| HIGH | 2.3 | grammar.json | n5-134 (ので) is tier=core_n5 but classified borderline elsewhere in the corpus |
| HIGH | 2.4 | vocab.json | 132 entries lack examples (mostly nouns and verbs in thematic sections) |
| MEDIUM | 3.1 | vocab.json | Section 38 "Sounds and Voice" present here despite dossier-removal narrative |
| MEDIUM | 3.2 | kanji.json | 10 kanji entries have duplicate compound examples leaking from vocab cross-listing |
| MEDIUM | 3.3 | grammar.json | 8 em/en-dashes against project no-em-dash policy |
| LOW | 4.1 | grammar.json | 32 stub patterns with see-also-only form_rules from F-19 dedup leftovers |
| LOW | 4.2 | kanji.json | 大人 (おとな) example doesn't flag jukujikun irregular reading |

**Total: 10 actionable items** (1 critical, 4 high, 3 medium, 2 low).

---

*End of audit. Prepared 2026-05-02.*
