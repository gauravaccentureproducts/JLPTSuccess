# Hindi Audit Findings — N5 (2026-05-07)

Executed `prompts/LocaleTransitionEnHi.txt` Phase 0 (inventory) +
Phase 1 (paper-files linkage discovery) + sampled rubric spot-checks
across all surfaces. Native-Hindi-scholar persona reviewer.

## Phase 1 finding — paper-files linkage

`js/papers.js:380-395` builds the result `detail` array using
`q.rationale` directly, with no locale lookup. Line 444 renders
`d.rationale` regardless of active locale. There is no `*_hi`
fallback path. **Conclusion: Option (a) — paper files MUST add
explicit `rationale_hi` per question (and `summary_hi` for dokkai
passages) to deliver Hindi explanations.** Option (b) (linkage to
questions.json) was empirically falsified.

## Issue list — by severity

### CRITICAL

#### ISSUE-HI-01 — Paper files have zero Hindi coverage (29 files)

- Surface: `data/papers/**/*.json` (moji × 7 + bunpou × 7 + dokkai
  × 7 + goi × 7 + manifest)
- Symptom: every paper file's `questions[].rationale` is English-
  only; no `rationale_hi`. Dokkai `passages[].text` has no
  `summary_hi` either.
- User impact: a learner with `locale = hi` running any paper test
  sees ENGLISH explanations after each question. The Hindi-medium
  promise is broken on the highest-stakes surface (full-mock-test
  paper).
- Volume: 28 paper files × ~15-20 questions each ≈ 400-560 missing
  `rationale_hi` strings + 50+ missing `summary_hi` strings on
  dokkai passages.
- Fix: per audit-prompt Phase 2 option (a), add `rationale_hi` to
  every question and `summary_hi` to every dokkai passage. Apply
  rubric R-1..R-7. Mark `rationale_hi_provenance: 'native_reviewed'`.

#### ISSUE-HI-02 — questions.json: 433 placeholder Hindi values admitting "review pending"

- Surface: `data/questions.json`
- Symptom: 433 of 854 Hindi values (≈51%) match placeholder
  patterns:
  - `"पैटर्न n5-NNN का प्रश्न — विवरण के लिए संबंधित पैटर्न पृष्ठ देखें। (अस्थायी; मूल समीक्षा प्रतीक्षित।)"`
  - `"यह विकल्प यहाँ अनुपयुक्त है। (अस्थायी; पूर्ण Hindi विवरण की मूल समीक्षा लंबित।)"`
  - `"इस विकल्प के विवरण के लिए अंग्रेज़ी संस्करण देखें (मूल समीक्षा लंबित)।"` ← actively tells learner to read English
- The text itself admits "अस्थायी; मूल समीक्षा लंबित" ("temporary;
  original review pending") — yet provenance is marked
  `'native_reviewed'`. **Provenance-honesty violation**.
- Affected fields: `explanation_hi` (mostly) + every
  `distractor_explanations_hi[*]` slot.
- Fix: write real Hindi explanations for each question; downgrade
  provenance to `'llm_curated'` on rewrite-pending entries; flip
  to `'native_reviewed'` only after rubric pass.

### HIGH

#### ISSUE-HI-03 — questions.json: code-mixed (Devanagari + English words)

- 371 entries contain English words ≥4 letters embedded in
  Devanagari Hindi (e.g., literal "Hindi" lower-cased in template).
  Most overlap with placeholder set (#02). Treating as one
  remediation pass.

#### ISSUE-HI-04 — grammar.json l1_notes.hi: 118 entries code-mixed

- Surface: `data/grammar.json` → `patterns[].l1_notes.hi`
- 118 of 481 l1_notes.hi (≈25%) contain stray English words like
  `nominalizer`, `casual`, `intonation`, `polite`, `version`,
  `family`, `question`, `form`, `transfer`, `native`, `counter`,
  `already`, `covered`, `Verb`, `past`, `negative`, `plain`,
  `adjectival`, `same`, `feel`, `offer`, `opinion`, etc.
- Sample: `n5-058`: `"n5-058 already covered (Verb-ます) in n5-001
  family।"` — circular reference + English-Hindi mix.
- Fix: rewrite each in Devanagari Hindi using approved Hindi
  technical glossary (नामकरण-कण for nominalizer, अनौपचारिक for
  casual, स्वर-आरोह for intonation, विनम्र for polite, औपचारिक
  for formal, क्रिया-समूह for verb-family, etc.).

#### ISSUE-HI-05 — grammar.json explanation_hi: 6 patterns code-mixed

- Surface: `data/grammar.json` → `patterns[].explanation_hi`
- Examples:
  - `n5-023`: `"क sentence के अंत में लगाकर..."` ← Latin "sentence"
  - `n5-030`: `"...नामकरण-कण (nominalizer)।"` ← parenthetical English
  - `n5-065`: `"क्रिया-शब्दकोश रूप (Verb-る / Verb-う)..."` ← "Verb"
  - `n5-067`: `"...te-form की tha tha का त-रूप..."` ← Hindi-romanized "tha tha"
  - `n5-081`: `"...was/were के लिए でした नहीं लेते..."` ← English "was/were"
  - `n5-031`: `"...casual क्रिया + の भी same intonation-only feel।"`
- Fix: rewrite using Devanagari Hindi only.

#### ISSUE-HI-06 — kanji.json: 48 entries with meaning-list arity mismatch

- Surface: `data/kanji.json` → `entries[].meanings_hi`
- 48 of 106 entries (≈45%) have fewer Hindi list items than
  English. The English schema is a list of distinct meanings; the
  Hindi often collapses them with " / " inside one string,
  breaking parallel UI rendering and obscuring polysemy.
- Examples:
  - `日`: EN `["day", "sun"]` (2) vs HI `["दिन / सूर्य"]` (1)
  - `木`: EN `["tree", "wood", "Thursday"]` (3) vs HI `["पेड़ /
    गुरुवार"]` (1) — also missing "wood" (लकड़ी)
  - `金`: EN `["gold", "money", "Friday"]` (3) vs HI `["सोना /
    शुक्रवार"]` (1) — missing "money" (पैसा / धन)
  - `土`: EN `["earth", "soil", "Saturday"]` (3) vs HI `["मिट्टी /
    शनिवार"]` (1) — missing "earth" (पृथ्वी / धरती)
  - `分`: EN `["minute", "part", "divide"]` (3) vs HI `["मिनट /
    बाँटना"]` (1) — missing "part" (भाग)
  - `男`: EN `["man", "male"]` (2) vs HI `["पुरुष"]` (1)
- Fix: split each Hindi entry into a list parallel to English;
  fill in missing meanings.

### MEDIUM (single-entry quality bugs)

#### ISSUE-HI-07 — grammar.json n5-029 l1_notes.hi: invalid Hindi grammar

- Quote: `"...कुछ हिंदी "का" प्रयोग जापानी में कण-रहित हो जाते हैं
  (e.g. "सोचना का" → सोचने में → 思うのに)।"`
- Bug: `"सोचना का"` is broken Hindi. Hindi infinitives take the
  oblique form before postpositions: `"सोचने का"` (correct) or
  `"सोचने में"` (correct, used later in the same sentence). The
  contrast example mixes a wrong form with right forms.
- Pedagogical-fidelity fail (R-6): teaches incorrect Hindi to
  illustrate Japanese.
- Fix: rewrite the example pair to use grammatical Hindi only.

#### ISSUE-HI-08 — grammar.json n5-091 l1_notes.hi: circular self-reference

- Quote: `"n5-091 same family।"`
- Bug: this is the l1_notes for pattern n5-091 itself; the note
  references the same pattern as if it were a sibling. Plus
  English "same family". Net informational value: zero.
- Fix: write a real Hindi-vs-Japanese contrast for the います
  animate-existence pattern. Hindi has no animacy split in
  existence verbs (होना covers all) — that IS the contrast worth
  teaching.

#### ISSUE-HI-09 — grammar.json n5-023 l1_notes.hi: spelling error

- Quote: `"...हिंदी बक्ता अक्सर か को भूलकर..."`
- Bug: `बक्ता` is non-standard. Correct is `वक्ता` (व, not ब).
  The word is from Sanskrit वक्तृ (speaker).
- Fix: replace `बक्ता` → `वक्ता` (also grep the rest of the corpus
  for the same misspelling).

#### ISSUE-HI-10 — grammar.json n5-165 l1_notes.hi: wrong analogy

- Quote: `"हिंदी "श्री / श्रीमती" विनम्र-prefix; お~/ご~ संज्ञा को
  सुंदर बनाते हैं।"`
- Bug: श्री / श्रीमती are HONORIFIC TITLES (used before personal
  names), not noun-prefixes. お/ご attach to common nouns
  (お茶, ごはん). The Hindi has no exact equivalent — the contrast
  is the absence of a noun-beautifier prefix in Hindi. Note also
  the dangling English "prefix" inside the Devanagari.
- Fix: rewrite to either compare to Sanskrit-derived शुद्ध- /
  महा- prefixes (closer analog) or explicitly state Hindi has no
  direct equivalent.

#### ISSUE-HI-11 — questions.json: kana-Devanagari hybrid token "カウंटर"

- Surface: `data/questions.json` → multiple `explanation_hi`
  entries (e.g., q-0466, q-0503).
- Bug: "カウंटर" mixes Japanese katakana カ with Devanagari ुंटर.
  Should be either pure Devanagari (`काउंटर`) or pure katakana
  (`カウンター`).
- Fix: replace with `काउंटर` (Devanagari transliteration of
  English "counter").

### LOW (polish / consistency)

#### ISSUE-HI-12 — locales/hi.json: number-system inconsistency

- `home.forecast_label`: `"दोहराव पूर्वानुमान (७ दिन)"` uses
  Devanagari numeral ७. But `home.reviews_due`, `kanji.popover_strokes`,
  `test.submit_remaining` all use Latin `${n}`.
- Fix: pick one (Latin recommended for consistency with
  `${n}` interpolation) — change "७ दिन" → "7 दिन".

#### ISSUE-HI-13 — locales/hi.json: SRS-term mistranslation

- `drill.graduated: "पूरा"`
- Bug: SRS "Graduated" means "passed out of the learning queue
  into long-interval review", not "complete". पूरा reads as
  "finished/done", losing the SRS semantic.
- Fix: `"महारत प्राप्त"` ("mastery achieved") or `"पारित"` ("passed").

#### ISSUE-HI-14 — locales/hi.json: "missed" calque

- `review.no_misses: "आपने हाल ही में कुछ नहीं छोड़ा - अभ्यास जारी रखें।"`
- Bug: "कुछ नहीं छोड़ा" calques "missed" as "left behind", but the
  English semantic in SRS context is "got wrong" or "answered
  incorrectly". A learner reading the Hindi would understand
  "you haven't skipped anything" rather than "you haven't missed
  anything you previously got wrong".
- Fix: `"आपने हाल ही में कोई ग़लती नहीं की — अभ्यास जारी रखें।"`

#### ISSUE-HI-15 — locales/hi.json: non-standard Devanagari for Japanese ō

- `sitting.section_2: "बुनपोऊ + दोक्काइ"` — `बुनपोऊ` for 文法
  (bunpō). The long ō is ambiguous; standard transliteration uses
  ओ (single) not ओऊ. Other strings like `nav.kanji: "कान्जी"` use
  consistent transliteration.
- Fix: either `"बुम्पो + दोक्काइ"` (long-vowel implicit) or use
  the Japanese terms `"文法 + 読解"` directly (consistent with how
  the app shows Japanese vocab).

### HIGH — added 2026-05-07 follow-up

#### ISSUE-HI-18 — Three-way convention inconsistency for "kana + Hindi-term" tokens

(Surfaced by reviewer follow-up question: "ना-विशेषण should be な-विशेषण.")

The corpus uses three different conventions for tokens like
"na-adjective" / "te-form" / "ta-form" etc. translated to Hindi:

| Convention                  | Count | Status   | Example          |
|-----------------------------|------:|----------|------------------|
| Hiragana + Devanagari       | 8     | correct  | な-विशेषण        |
| Latin romaji + Devanagari   | 57    | wrong    | na-विशेषण        |
| Devanagari + Devanagari     | 2     | wrong    | ना-विशेषण        |

Worst case: `grammar.json` pattern n5-078 has `meaning_hi:
"na-विशेषण + な + संज्ञा"` — Latin "na-" sitting next to hiragana
"な" in the same string.

Principle (from the same R-1..R-7 rubric + the user's stated
boundary "Japanese tokens stay in Japanese script"): Japanese
grammatical particles attached to Hindi terms must be written in
the **Japanese script** (hiragana な / い / て / た / ない / たい /
ます etc.), not transliterated to Latin or Devanagari.

This matches:
- How the English content already does it (`な-adjective`).
- The N5 pedagogical sequence (hiragana is taught before grammar
  particles, so transliteration is unnecessary by the time the
  learner reaches these patterns).
- The 8 entries that already do it correctly.

Fix: 57 Latin-romaji entries → kana form; 2 Devanagari entries →
kana form. Mostly in `grammar.json` `meaning_hi` /
`explanation_hi`, with a couple in `questions.json`. Add a CI
invariant to lock the convention going forward.

Diagnostic script: `tools/_hindi_kana_transliteration_scan.py`.

#### ISSUE-HI-19 — Japanese-token romanization leakage in BOTH English and Hindi (143 hits)

(Surfaced by reviewer follow-up question: "other than な, is there
any other thing which should not be translated but is getting
translated (in E and Hi both)".)

The same anti-pattern as HI-18 (kana grammatical particles
romanized to Latin) extends across multiple token classes AND
across both English and Hindi explanation surfaces. Scan results:

| Token type                                       | EN hits | HI hits |
|--------------------------------------------------|--------:|--------:|
| Form names (te/ta/masu/nai/tai/etc.)-form        |    43   |    9    |
| Bare romaji forms (masu, desu, tai, nai)         |     7   |    0    |
| Adjective types (na-adjective, i-adj)            |    30   |   48    |
| Time/counter romanization (ji for 時 etc.)        |     1+  |    0    |
| Full romaji example sentences                    |   found |    0    |
| Hindi-text-romanized (e.g. "tha tha" for था था) |     -   |   found |

Total: ~143 occurrences across data/grammar.json (mostly),
data/questions.json (some), data/vocab.json (a couple).

Worst-offender examples:

1. EN full-romaji example sentence at `q-0225.explanation_en`:
   `"hoshii takes ga to mark the object of desire (not wo).
    watashi wa X ga hoshii desu = I want X. Distractors: wo
    ungrammatical with hoshii; ni/to wrong category."`
   Should use Japanese script throughout: ほしい / が / を / etc.

2. EN form-name romanization at pattern n5-063 `meaning_en`:
   `"Verb-て (te-form) - connector"` → `Verb-て (て-form)`.

3. HI double-bug at pattern n5-061 `explanation_hi`:
   `"समूह-1: ख़ास नियम (te-form की tha tha का त-रूप)"`
   - `te-form` should be `て-form`.
   - `tha tha` is Latin transliteration of Hindi `था था` (past-
     tense marker) — should be `था-था` in Devanagari.

The principle (now consistent across both locales):

| Layer       | Convention                                            |
|-------------|-------------------------------------------------------|
| Japanese    | Always Japanese script (kana + kanji)                 |
| English     | English prose; Japanese tokens stay in Japanese       |
| Hindi       | Devanagari prose; Japanese tokens stay in Japanese;   |
|             | Hindi tokens stay in Devanagari                       |

Fix: walk all explanation/meaning/gloss/rationale fields in EN
and HI; replace romanized Japanese tokens with their kana
equivalent. Keep the surrounding language untouched. Add CI
invariant covering both locales.

Diagnostic: `not-required/tools-archive/_hindi_japanese_token_audit.py`.

### INFO / cross-cutting

#### ISSUE-HI-16 — Provenance honesty violation

- 433+ entries in `data/questions.json` are marked `'native_reviewed'`
  but contain text that admits "review pending". This was tagged
  in the bulk native-reviewer pass on 2026-05-06; the Hindi text
  was not actually reviewed.
- Fix: walk every entry whose Hindi text matches a placeholder
  pattern; downgrade provenance to `'llm_curated'` until rewrite
  completes. Then re-flip after rubric pass.

#### ISSUE-HI-17 — English source data corruption (out of audit scope)

- `data/reading.json` → `passages[].summary` (English) field
  contains code-mixed Hindi-English fragments like `"directions
  विषय का छोटा अनुच्छेद"`. The English summaries appear to have
  been mid-edited and not finalized.
- This is OUT of the Hindi-audit scope per the prompt's "English
  source is read-only" guardrail.
- Surface separately as an English-content bug for a future cycle.

## Counts at a glance

| Surface             | Total HI slots | Placeholder | Code-mix |
|---------------------|---------------:|------------:|---------:|
| questions.json      | ~854           | 433         | 371      |
| grammar.json (main) | 356            | 0           | 6        |
| grammar.json l1     | 481            | 0           | 118      |
| reading.json q-expl | 20             | 0           | 0        |
| listening.json      | 47             | 0           | 0        |
| reading summaries   | 45             | 0           | 0        |
| vocab.json          | 1041           | 0           | 0        |
| kanji.json          | 106            | 0           | 0        |
| **TOTAL**           | **~2950**      | **433**     | **495**  |

| Other gaps                              | Count |
|-----------------------------------------|------:|
| Paper files with zero Hindi keys        | 29    |
| Kanji entries with arity mismatch       | 48    |
| Grammar single-entry quality bugs       | 5+    |
| UI string polish issues                 | 4     |

## Recommended action sequence

1. **First** (largest bang-per-buck): rewrite the 433 placeholder
   `questions.json` entries → drops the largest single quality
   gap. This is the audit prompt's Phase 7.
2. **Second**: close the 29-paper-files coverage gap → unblocks
   Hindi on the highest-stakes surface (mock-test). Audit prompt
   Phase 2.
3. **Third**: kanji.json arity rewrite (48 entries). Audit prompt
   Phase 4 sub-task.
4. **Fourth**: grammar.json l1_notes.hi (118 code-mix entries) +
   the 5 single-entry quality bugs. Audit prompt Phase 5.
5. **Fifth**: locales/hi.json polish (4 strings). Audit prompt
   Phase 8.
6. **Sixth**: provenance hygiene sweep — downgrade
   `'native_reviewed'` → `'llm_curated'` for every entry whose
   Hindi text was not actually reviewed. Audit prompt's R-0 rule.
7. **Seventh**: add the new CI invariant JA-NN that detects
   placeholder + code-mix patterns (the regex set used by
   `tools/_hindi_placeholder_scan.py`). Audit prompt Phase 9.

## Diagnostic tools added this session

- `tools/_hindi_field_inventory.py` — coverage tally per surface
- `tools/_hindi_quality_sample.py` — deterministic sampling for
  rubric review
- `tools/_hindi_placeholder_scan.py` — placeholder + code-mix
  detector
- `feedback/_hindi_audit_sample_20260507.txt` — full sample dump
  (not committed; regenerable)

These should remain as the audit's regression-test infrastructure.
