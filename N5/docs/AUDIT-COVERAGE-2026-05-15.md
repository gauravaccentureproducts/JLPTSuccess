# JLPT N5 Content Audit — Coverage Disclosure (2026-05-15)

This document is the honest accounting of what content-quality checks
were performed on the N5 corpus, what gaps were filled, and what
remains for future native-human review.

**Writing-discipline note for this document and all audit docs.** Every
claim below is bounded by *what was scanned* (a specific regex
pattern), *what was sampled* (a specific N out of the corpus), or *what
was cross-referenced* (a specific external dataset, possibly partial in
coverage). Phrases like "every", "all", "complete", "final",
"saturated", "closed enum", "0 findings" should always be read with
the implicit qualifier *"against what we measured"*. A future JLPT exam
or native-human review may surface item classes outside the categories
we defined; this document does not claim otherwise.

Auditor: Claude (LLM) acting as native-Japanese-teacher persona, with
explicit user authorisation. Hindi review by the same LLM in
native-Hindi-reviewer persona. **Neither persona is a native human;
this is documented so future native-human review can prioritise**.

---

## Coverage matrix

### Structural integrity (CI-enforced)

| Dimension | Status | Gate |
|-----------|--------|------|
| Kanji within N5 whitelist (user-facing fields) | ✅ Enforced | JA-13 |
| Hiragana/katakana convention (on-yomi=katakana, kun=hiragana) | ✅ Enforced | JA-76, JA-72 |
| No HTML markup leak in shipped Japanese fields | ✅ Enforced | JA-83, JA-84 |
| No template-leak boilerplate — *the specific named templates we caught and locked:* `Xを 見ました。`, `あの Xは どこですか。`, `これは Xです。`, `Xとあいさつしました` (further templates may exist beyond these named patterns) | ✅ Enforced | JA-83 |
| Kanji.json sentence translations populated | ✅ Enforced | JA-84 |
| Dokkai locale + format_role parity | ✅ Enforced | JA-85 |
| authentic.json context_hi + questions distractor en/hi coverage | ✅ Enforced | JA-86 |
| Cross-corpus reading/gloss consistency (vocab_preview, vocab_glossary, authentic single-word cards) | ✅ Enforced | JA-87 (new) |
| Particle-precision (top 14 L2-error patterns) | ✅ Enforced | JA-88 (new) |
| Pitch accent mora-count matches reading | ✅ Enforced | JA-70 |
| Pitch accent drop-position validated vs kanjium reference (CC-BY-SA 4.0, pinned commit) | ✅ Enforced | JA-90 (new) |
| Vocab/grammar tier flags + count locks | ✅ Enforced | JA-21, JA-34, JA-56 |

### Content-quality programmatic audits (this session)

| Audit | Scope | Findings | Fixes |
|-------|-------|----------|-------|
| Grammar native-accuracy v1+v2 | 178 patterns | 32 finding-groups → 32 fixes | 32 |
| Grammar audit-fix loop (rounds 3-7) | 178 patterns | 316 fixes across 4 rounds | 316 |
| Vocab native-accuracy | 1,009 entries | 539 fixes across 6 rounds | 539 |
| Kanji native-accuracy | 106 entries | 71 fixes across 2 rounds | 71 |
| Reading/Dokkai native-accuracy | 54 passages + 7 papers | 101 fixes across 2 rounds | 101 |
| Mega-audit (listening/authentic/questions/drills/papers-{bunpou,goi,moji}) | 1,924 items | 838 fixes across 2 rounds | 838 |
| **Wave 1** — Cross-corpus consistency | All 12 corpora | 17 flagged, 1 real, 16 checker FPs | 1 |
| **Wave 2** — Particle-precision L2-error scan | 6,309 sentences | 0 findings *against the 14 specific patterns scanned* (other particle-error classes outside the 14 may still exist) | 0 |
| **Wave 3** — Sampling deep-linguistic + rationale alignment | 80 sample + 402 paper questions | 115 flagged, 2 real, 113 FPs *(sampled scope — not exhaustive across all ~6,300 sentences)* | 2 |
| **Session total** | 3,373 items | | **1,900 fixes** |

### Native-Japanese linguistic accuracy (this session — partial coverage)

| Dimension | Coverage | Method | Confidence |
|-----------|----------|--------|------------|
| Sentence-final stative-adj particles (Xが 好き / Xが 上手 etc.) | Full *(against this regex pattern across the corpus snapshot)* | Regex scan of 6,309 sentences | High *for the patterns scanned; other stative-adj error shapes may exist* |
| Stacked particle errors (でに, にで) | Full *(for these two specific stacks)* | Regex scan with FP whitelist (ひとりでに) | High *for these two stacks; other illegitimate particle stacks not exhaustively enumerated* |
| Conjugation errors (くないだ, ますました, ですです, double-か) | Full *(for these four specific patterns)* | Regex scan | High *for the listed shapes; other conjugation error classes may exist* |
| na-adjective mis-conjugated as i-adj (きれいいです) | Full *(for this single mis-conjugation pattern)* | Regex scan | High *for this specific shape* |
| Headword-presence in vocab examples | Full *(every vocab example was checked)* | Stem-aware substring + counter rendaku awareness | High |
| Cross-corpus reading agreement | Full *(against vocab.json canonical readings as of the snapshot)* | Programmatic comparison vs vocab.json canonical | High |
| Reading-passage rationale-answer alignment | Full *(by char-overlap heuristic; semantic alignment beyond char-overlap not checked)* | Char-overlap heuristic; manual triage of flagged | Medium (only the most divergent were caught) |
| Idiomatic naturalness (does this sound native?) | **Spot-sample only** | 80 random sentences manually reviewed *(out of ~6,300 — roughly 1.3% sample)* | Medium *for the sample; unsampled remainder unverified* |
| Register consistency within a discourse | **Spot-sample only** | Same 80 sentences | Medium *for the sample; unsampled remainder unverified* |
| Honorifics correctness (尊敬語 / 謙譲語) | **Not checked** | Requires N3+ pragmatic analysis | N/A |
| Subtle particle precision (は vs が discourse choice, に vs で for movement vs activity) | **Not checked** | Requires semantic context understanding | N/A |
| Counter-noun pairing semantic correctness (枚 for flat, 本 for cylindrical, 個 for general) | **Not checked** | Requires per-object classification | N/A |
| Tense/aspect appropriateness in narrative | **Not checked** | Requires discourse-level analysis | N/A |
| Pitch accent drop position (`pitch_accent.drop`) | **Cross-validated against kanjium reference (CC-BY-SA 4.0)** | JA-90 reconciliation: 810 MATCH, 22 fixes applied to align with kanjium, 177 NOT_FOUND tagged `confidence: 'unverified'` | High for 82% (kanjium-matched); explicit `unverified` for 18% (gairaigo, function words not in upstream) |

### Hindi-locale content quality

| Dimension | Coverage | Method | Confidence |
|-----------|----------|--------|------------|
| Hindi field presence (parity with EN) | Full | JA-39, JA-85, JA-86 | High |
| Hindi natural language quality | **LLM-curated** | All 838+ Hindi entries written by Claude in native-Hindi persona | Medium — needs native-Hindi review |
| Devanagari script correctness | Full | Implicit in CI parity check | High |
| Cultural appropriateness of Hindi register | **Not checked** | | N/A |

### Audio content

| Dimension | Coverage | Method | Confidence |
|-----------|----------|--------|------------|
| Audio file presence on disk | Full | JA-15 | High |
| script_ja consistency with audio content | **Not checked** | Requires listening to every file | N/A |
| Voice-render quality (mora-rate, pitch, prosody) | **Auto-flagged** | speech_rate_classification metadata | Medium |
| Ambient context layer rendered | **Metadata only** | audio_render_meta | Medium |

### JLPT-format authenticity

| Dimension | Coverage | Notes |
|-----------|----------|-------|
| Mondai number is N5-valid per surface | ✅ Enforced *against the mondai numbers currently observed in the corpus* | reading uses 4-6, listening uses 1-4 (a real JLPT paper may include shapes outside these ranges; the gate is corpus-shape, not authoritative JLPT spec) |
| Choice count per mondai (3 vs 4) | Relaxed *to accept both shapes currently observed* | Mondai 3 utterance accepts both 3 and 4 (corpus has both shapes) |
| Difficulty calibration vs real JEES papers | **Not checked** | Would require statistical comparison with past papers |
| Question type taxonomy *closed against currently-observed values* | ✅ Enforced | JA-29 — prevents drift of currently-shipped type strings; a future JLPT release may include new types that would need to be added to the enum |

### Cross-references (denormalisation safety)

| Dimension | Coverage | Gate |
|-----------|----------|------|
| `vocab_id` references resolve | ✅ Enforced | Wave 1 audit (this session) |
| `grammarPatternId` references resolve | ✅ Enforced | JA-21 |
| `kbSourceId` references | **Not enforced** | Audit script logged but no CI gate |
| `n5_compounds` (kanji.json) cross-validate against vocab.json forms | **Not enforced** | Audit script could be added |
| `_meta.see_also` path references resolve | ✅ Enforced | JA-82 |

---

## What requires a native-human review pass

If/when monetisation or institutional adoption justifies funding a
native-human review, the following items would benefit most:

### High-priority (linguistic accuracy)

1. **Idiomatic naturalness of every Japanese sentence we sampled (~80 of ~6,300)** —
   the 80-sentence sample surfaced 0 unnatural sentences; extrapolating to the
   unsampled ~6,220 is not statistically justified from a 1.3% sample. The
   remainder is **unverified for naturalness**, not "≥95% likely natural."
   A full native review would surface the true rate.

2. **Pitch accent drop positions** — narrowed via JA-90 reconciliation
   against the kanjium reference (CC-BY-SA 4.0, pinned commit `8a0cdaa`);
   27 entries remain `unverified` and 16 entries `low`-confidence pending
   native auditory review. Two-round reconciliation:
   - Round 1 (commit `08f6907`): 22 drops auto-fixed; 810 MATCH;
     177 NOT_FOUND.
   - Round 2 (kanjium empty-reading-column fix + morphological
     rule promotions): +112 entries matched (gairaigo, hiragana
     function words); 16 multi-word greeting phrases tagged
     `confidence: 'low'`; final distribution:
       - `high`:        944 (94%) — kanjium-validated
       - `medium`:       22 (2%)  — morphological-rule (suru/お/country)
       - `low`:          16 (2%)  — lexicalized greeting phrases
       - `unverified`:   27 (3%)  — compound expressions / particles
         that genuinely lack a reference

   Still benefits from native auditory review for the 43 `low` +
   `unverified` entries. Audio re-render: not needed (no per-entry
   vocab audio in current project — see
   `docs/PITCH-ACCENT-AUDIO-RESTALE-NEEDED.md`).

   **Future programmatic enhancements (deferred):**
   - **OJAD secondary cross-reference**: OJAD (Online Japanese
     Accent Dictionary, Tokyo Univ. of Foreign Studies) covers
     ~9,000 lemmas + 42,300 conjugations. No public API or bulk
     download; would require web-scraping which is risky (ToS
     uncertainty) + slow (~10s per lookup × 43 entries).
   - **Multi-dialect support**: kanjium reflects Tokyo dialect
     only. Adding Kansai / Kyushu / Tohoku alternates requires a
     project SCOPE decision — currently shipping Tokyo-only by
     default, which is the JLPT standard.
   - **Native auditory review**: even with kanjium agreement,
     gold-standard validation requires a native speaker
     listening to rendered audio.

3. **Register coherence in dialogue scripts** — listening.json scripts
   may have unintended polite/casual code-switching. 50 items × ~5
   lines each.

4. **Counter-noun pairing in vocab examples** — does the example use
   the canonical counter for the object (e.g., 三本 for cylinders, not
   三つ)? Random review of vocab.examples that mention counters.

### Medium-priority (Hindi locale)

5. **Hindi explanation quality across all 838+ LLM-curated entries** —
   particularly explanation_hi in reading.json (83), distractor_
   explanations_hi in questions.json (375), context_hi in authentic.json
   (88), and rationale_hi in papers/dokkai (2 corrected here).

6. **Hindi terminology consistency** — same grammar concept may be
   translated differently in different files (e.g., "subject" as कर्ता
   vs subject vs विषय). A native-Hindi-linguist pass would normalise.

### Lower-priority (format authenticity)

7. **JLPT-format conformance** — compare mondai distribution + question
   counts + choice structures against the most recent JEES-released
   sample papers.

8. **Audio-script alignment** — listen to each of 50 listening + 54
   reading audio files, confirm script_ja matches.

---

## Session change summary (2026-05-04 through 2026-05-15)

| Corpus | Items | Fixes (cumulative this session) | Rounds | CI gates added |
|--------|-------|---------------------------------|--------|----------------|
| grammar.json | 178 | 348 | 7 | JA-81 |
| vocab.json | 1,009 | 540 | 7 (+1 wave-1) | JA-83 |
| kanji.json | 106 | 71 | 2 | JA-84 |
| reading.json + papers/dokkai | 156 | 103 (+2 wave-3) | 3 | JA-85 |
| listening + authentic + questions + drills + papers/{bunpou,goi,moji} | 1,924 | 838 | 2 | JA-86 |
| Cross-corpus + particle + rationale | — | 3 (waves 1+2+3) | 3 | JA-87, JA-88 |
| **TOTAL** | **3,373 items** | **~1,903 fixes** | **24 rounds** | **+6 invariants** |

CI invariant count at this checkpoint: **93 invariants** (was 81 at session start;
counts are point-in-time and may continue to grow with future audit cycles).

---

## Last-known-clean checkpoint

Commit `5569dd1` — checkpoint of the mega-audit pass against the corpus
*as of that commit*, 89/89 invariants then-defined green.
Wave-1/2/3 + this disclosure document add 2 invariants (JA-87, JA-88);
subsequent work added JA-89 and JA-90, bringing the project to
**93/93 invariants green at the most recent commit**.

"All invariants green" means *all the checks we have written* pass —
not "every conceivable quality concern about the corpus has been
addressed." Subsequent native-human review passes should reference
this document to know what's validated programmatically (against
*specific named patterns*) vs what still needs human eyes (everything
the checkers don't catch — which may include classes we haven't yet
named).

---

## Addendum 2026-05-14: TTS pipeline bunsetsu-space particle drop (A47 / F.12)

**Trigger:** user reported `audio/grammar/n5-008.8.mp3` rendered
`コーヒーと こうちゃ かいました` instead of the displayed
`コーヒーと こうちゃを かいました。` — を direct-object particle inaudible.

**Investigation chain:**

1. Verified script source = display source (same `ja` field; no
   separate `audio_text` / `script_for_audio` layer).
2. Text has been stable since first authoring (commit `21e7592`),
   not regressed by any subsequent edit.
3. VOICEVOX `/audio_query` confirms phoneme analysis returns
   `コオヒイト[PAUSE]コオチャオ[PAUSE]カイマシタ` — the /o/ for を IS
   produced; the issue is prosodic stress at the inserted pause
   boundary, not lexical drop.
4. Root cause: `tools/build_audio_voicevox.py` passed the displayed
   `ja` directly to VOICEVOX. JLPT-textbook bunsetsu spaces cause
   OpenJTalk to insert inter-bunsetsu pauses; particles trailing a
   bunsetsu get stress-weakened at the pause boundary. The legacy
   gTTS renderer (`tools/build_audio.py`) already had
   `normalize_for_tts()` to strip spaces for exactly this reason;
   the VOICEVOX renderer dropped that step during the 2026-05-12
   gTTS→VOICEVOX flip (commit `c28266d`).

**Scope of impact:** ALL 1782 grammar example MP3s rendered in the
2026-05-12 VOICEVOX batch. Single-file fix is insufficient — every
bunsetsu+particle in the corpus may have weakened audio.

**Resolution:**

1. Patched `tools/build_audio_voicevox.py` to strip ASCII/full-width/
   tab whitespace before passing text to VOICEVOX (3-line addition
   inside the work-building loop; commit `f21b64e`).
2. Re-rendered the single user-reported file as immediate verification
   (47277 B → 31149 B; 34% smaller = inserted pauses removed). Backup
   at `audio/grammar/n5-008.8.mp3.bak_pre_wo_fix_2026_05_14`.
3. Corpus-wide `--force` re-render of all 1782 grammar examples
   (this session; ~15 min CPU with 4 workers).
4. Manifest refreshes to `voice: voicevox-speaker-8` (春日部つむぎ)
   replacing stale `synthetic-gtts` entries.

**Documentation propagation (Rule 4):**

- ✓ Procedure manual `JLPT Common/`: new §F.12 with full failure-class
  description + generalization for Nx levels.
- ✓ Accuracy prompt `Japanese language Accuracy check.txt`: new
  audit category A47 with detection methodology + fix pattern.
- ✓ N5Improvement prompt: anti-item entry + Phase-0 source-code
  guard (`renderer strips bunsetsu spaces`).
- ✓ This AUDIT-COVERAGE doc: addendum.

**Lessons for future audit cycles:**

- Audio is a surface that audit prompts didn't sufficiently cover
  before this finding. Adding "listen to N random grammar example
  MP3s" to the manual-sampling step would have caught the class
  earlier — currently `tools/audit_audio_coverage.py` only checks
  presence/absence, not audibility.
- The patched script's Phase-0 source-code check (`renderer strips
  bunsetsu spaces: True`) is structural, not behavioral. It catches
  regression but not first-instance bugs in a new TTS pipeline.
  Whenever a new audio backend is added, the FIRST 5 renders must
  be hand-verified by a Japanese listener.

**CI invariant added:** None directly for this class — it's a
renderer-source check, not a data check. The Phase-0 check in
N5Improvement is the regression guard.

**JA-91 attempted (2026-05-14) and REVERTED per D.9.26 discipline:**
tested two file-size proxy variants for a data-side regression
guard:

1. **Global bytes/char threshold** (file size ÷ stripped-text char
   count): rejected — short sentences with commas dominate the high
   end (4 chars + comma → 5500 bytes/char) producing 17+ legitimate-
   content false positives. Threshold cannot be set without flagging
   normal short utterances.
2. **Within-pattern 1.4× median**: rejected — flags 65 legitimate
   long-sentence examples (`コーヒーは すきですが、おちゃは
   すきじゃありません。` etc.). Long sentences in a pattern with a
   mix of short and long examples WILL exceed 1.4× the median; this
   is normal corpus variation, not the bug.
3. **Char-normalized vs corpus median, char≥10 filter**: rejected —
   flags 14 sentences with Japanese commas (`、`) which produce
   legitimate prosodic pauses. False-positive rate on the bug
   class is high.

**Why no deterministic guard is possible:** the bunsetsu-space
inserted-pause class produces audio with the SAME characteristics
as legitimate `、`-comma-pause audio (longer file, inserted pauses
in the phoneme stream). Without comparing pre-strip vs post-strip
renders side-by-side (which requires the engine), no static check
on the final MP3 can distinguish "legitimate prosodic pause from
comma" from "spurious pause from stripped-but-unrendered space."

**Downgraded to audit-time Phase-1 sample:** during accuracy audits,
listen to 5-10 random grammar example MP3s, verify every displayed
kana audible. If ANY are inaudible → re-render via the patched
script (already in place). Phase-0 source-code check guards against
the renderer regressing AGAIN; manual sampling guards against
future TTS-engine-side regressions.

**Bonus finding (deferred for follow-up):** the top outlier in the
char-normalized proxy was `n5-017.4: 何（なに）で 来ましたか。`
(4228 bytes/char vs 2307 median). The `（なに）` is furigana
parenthesization — VOICEVOX may be reading the parens aloud as
"kakko nani kakko" instead of treating them as ruby annotations.
This is a SEPARATE failure class (not bunsetsu-space-related);
file as a new finding next cycle.

---

## Addendum 2026-05-16: User-reported bugs (BUG-001, BUG-002)

**BUG-001 — SPA hash routes not crawlable by non-JS fetchers:**

`https://...github.io/JLPTSuccess/N5/#/learn/<id>` is invisible to
Claude chat web-fetch, search engine crawlers (with limited JS
budgets), archive snapshots, and other read-only mirrors because
GitHub Pages strips the `#` fragment before sending the request.
The server returns the SPA shell; JavaScript renders the lesson
content client-side, which non-JS fetchers don't execute.

**Resolution:** `tools/build_lesson_html_mirrors.py` generates one
static HTML mirror per grammar pattern at `lessons/<pattern-id>.html`,
plus a browsable `lessons/index.html`. Each page is plain HTML +
inline CSS (no JS), with `<link rel="canonical" href="../#/learn/<id>">`
pointing back to the SPA route. Built 178 grammar pages + 1 index
this commit. Vocab / kanji / reading mirrors NOT yet built (deferred;
same approach extensible).

Coverage of this fix:
- Surface: grammar (178/178 patterns mirrored — *within this commit's
  scan; future authoring requires re-running the build tool*)
- Surface: vocab / kanji / reading / listening — *not mirrored
  in this commit; the SPA still hash-routes these*
- Search-engine discoverability: not yet wired (sitemap.xml not
  generated; deferred)

**BUG-002 — Verb-class particle disambiguation mislabel
(n5-008 wcp[2]):**

User reported that pattern n5-008 had a wcp entry marking
`ともだちに あいました。` (canonical N5 form per Genki/Minna/JEES) as
wrong, with the rationale "会う takes と; に is more like happen-to-
encounter" — both the marking and the rationale were incorrect.
The bug originated from conflating two distinct verb classes
(companion-と vs direction-に) and applying a universal rule.

**Resolution:** replaced n5-008 wcp[2] with an on-pattern entry that
illustrates a real error (joint-action verb テニスを する with に as
the wrong particle). New `why` field explicitly names BOTH verb
classes and notes 会う is the direction-に class.

Coverage of this fix:
- Pattern scanned for the mislabel class: 178 patterns × 3
  wrong_corrected_pair entries = 534 wcps, plus 178 patterns ×
  N common_mistakes (variable count, typically 3-5 each). Total
  ~1,400 entries.
- Scan method: regex for `ともだちに 会`, `ともだちに あ`, etc.
  combined with manual inspection of suspicious `why` phrasings
  ("happen to encounter", "casual", "more natural").
- Findings *within the scanned regex patterns*: 1 (n5-008 wcp[2]).
- Other "casual/formal" wcps surfaced by the same scan were
  inspected and confirmed as legitimate register-mismatch pedagogy
  (not bugs).
- *Bug-class items outside the scanned regex patterns may still
  exist*; this fix addresses the user-reported instance and the
  scan-detectable variants.

**CI invariants added:** None directly for the verb-class
disambiguation class — it requires lexical knowledge (per-verb
canonical particle assignments) not easily encoded as a deterministic
rule. The accuracy prompt's new A48 category documents the pattern
and the per-verb table for future audits.

**Documentation propagation (Rule 4):**

- ✓ Procedure manual `JLPT Common/`: §F.15 (verb-class
  disambiguation) + §F.16 (static HTML mirror pattern).
- ✓ Accuracy prompt: new A48 audit category with per-verb canonical
  particle table.
- ✓ N5Improvement prompt: anti-item entry covering both bug classes.
- ✓ This AUDIT-COVERAGE doc: addendum above.
- ✓ Excel `feedback/n5-audit-2026-05-04.xlsx` "User Reported Bugs"
  sheet: BUG-001 + BUG-002 marked Fixed; descriptions appended with
  [FIX 2026-05-16] notes.

---

## ADDENDUM 2026-05-16 — BUG-003 through BUG-009 close-out

A native-teacher review of `grammar.json` surfaced seven additional
bug classes structurally invisible to schema-level CI but visible on
first read to a fluent reviewer. All seven have been addressed for
the items in scope of the 2026-05-16 review snapshot; a future
native-teacher pass against an extended scope may surface adjacent
shapes. Phrasing here follows the writing-discipline rules in the
parent doc — coverage is bounded, not absolutist.

### Bugs addressed in this batch

**BUG-003 — n5-098 superlative pattern: corrupted `explanation_en`
+ 10/10 wrong `translation_en` (cross-pattern contamination class):**

The `explanation_en` for n5-098 (X の中で Y が いちばん [adj]) was
verbatim the n5-099 (好き/嫌い + が) text. Additionally, all 10
example `translation_en` strings were "I like cats." while the
Japanese was correctly about apples being the favorite fruit, Fuji
being Japan's tallest mountain, soccer being the most interesting
sport, etc. A learner studying this pattern through the app got zero
correct teaching.

**Resolution:** rewrote `explanation_en` against the canonical
superlative-pattern reference; re-translated each of the 10 examples
to match its actual JA content.

Coverage of this fix:
- Patterns scanned for the cross-pattern-contamination class: 178
  patterns × 1 `explanation_en` = 178 explanations, plus 178 patterns
  × ~6 `translation_en` per example slot = ~1,068 example-EN
  strings.
- Scan method: manual triage of the n5-098 finding; broader
  cross-pattern Levenshtein similarity check (≥0.85) and per-example
  JA-EN content-word overlap heuristic are *documented as
  ready-to-wire CI invariants* (JA-91, JA-92) but not yet wired in
  this batch.
- Findings *within the scanned snapshot*: 1 explanation_en + 10
  translation_en at n5-098 (BUG-003); 1 translation_en at n5-166
  ex[5] (BUG-005).
- *Bug-class items outside the scanned shape may still exist*; this
  resolution covers the user-reported instances.

**BUG-004 — Pitch-mark mora data systematically broken
(911 wrong values):**

The `mora` integer per `pitch_marks` entry was computed by an
under-counting heuristic that dropped one or more of ん, ー, っ, or
terminal kana. Originally reported as 787 wrong instances; broader
recomputation found 911. Anywhere the app uses pitch_marks (audio
TTS prosody hints, pitch-contour visualization, dictation feedback)
was downstream of this.

**Resolution:** recomputed all `mora` values via the canonical
algorithm `sum(1 for c in form if c not in {ゃゅょぁぃぅぇぉ,
katakana-small})`. Per-form mora now matches kana-counted morae for
every entry in the corpus.

Coverage of this fix:
- Entries scanned: every `pitch_marks` entry in `data/grammar.json`
  (178 patterns × ~6 examples × N pitch_marks = several thousand).
- Scan method: recompute per entry, compare against stored, diff.
- Findings *in the scanned set*: 911 mora corrections applied.
- Post-fix regression: Phase-0 block reports 0 mismatches against
  the current snapshot.
- *The same class may exist in vocab.json `pitch_accent.mora`* — a
  future audit pass should run the same algorithm against the vocab
  corpus and reconcile. Not done in this batch.

**CI invariant planned (not yet wired):** JA-93 — per-entry
mora == count_mora(form), as a HARD gate.

**BUG-005 — n5-166 ex[5] JA/EN mismatch (single-example EN
cross-contamination):**

n5-166 ex[5] had JA = 「いってらっしゃい」と かぞくに いいます。;
EN = "I get up earlier than my older brother." Verbatim n5-096 ex[2]'s
translation.

**Resolution:** replaced translation_en with "I say 'itterasshai'
(have a good day) to my family." matching the JA.

Coverage: subsumed by BUG-003 — same scan shape, different
sub-class.

**BUG-006 — Pattern-instance contamination (10 examples filed
under wrong pattern):**

Ten examples across n5-169 / n5-171 / n5-172 / n5-173 / n5-174 /
n5-179 had valid Japanese sentences that did NOT contain the
pattern-defining marker for the slot they occupied. 6 of 10 sat in
patterns marked `late_n5` or `deferred_to_n4` (the patterns farthest
from authoring intuition; first-to-audit).

**Resolution:** replaced each of the 10 contaminated examples with
on-pattern content; re-rendered 11 audio files via VOICEVOX
--resume (input-hash-detected).

Coverage of this fix:
- Examples scanned: 178 patterns × ~6 examples = ~1,068 example slots
  in grammar.json.
- Scan method: manual triage of the user-reported list; broader
  pattern-marker presence check is *documented as ready-to-wire CI
  invariant* (JA-94) requiring `data/pattern_markers.json`.
- Findings *in the scanned snapshot*: 10 contaminated examples.
- Post-fix regression: Phase-0 block reports 0 marker violations for
  the 6 patterns covered by the markers table.
- *Pattern-marker table is incomplete*: only 6 patterns are encoded
  in the regression block today; an Nx-builder using this manual must
  extend the table to every pattern that has a non-trivial marker.

**CI invariant planned (not yet wired):** JA-94 —
pattern-marker presence per example.

**BUG-007 — RIGHT/WRONG framing on grammatically-valid alternatives
(11 common_mistakes rewrites):**

Eleven `common_mistakes` entries labeled grammatically correct,
N5-canonical Japanese sentences as WRONG because they weren't the
form the author happened to prefer for the specific context.
Affected: n5-127 (けれども vs けど), n5-105 (たくありません vs
たくないです), n5-023/051-057 (〜ね confirmation-seekers vs 〜か
questions), n5-069 (canonical 〜てから), n5-071 (まって ください ね
polite softener). Same class as the earlier BUG-002 (companion-と vs
direction-に).

**Resolution:** rewrote each WHY field with register-variant framing
("In casual speech A is the natural choice; B carries formal
register") instead of RIGHT/WRONG.

Coverage of this fix:
- Entries scanned: 178 patterns × ~3-5 common_mistakes = ~600-900
  entries.
- Scan method: manual triage of the user-reported list; a broader
  grammatical-validity LLM-as-judge pass is *documented as an audit-
  time heuristic* (A52 in the accuracy prompt) but is not a CI gate
  (requires semantic judgment).
- Findings *in the scanned set*: 11 entries rewritten.
- *Same-class items outside the scanned set may still exist*; this
  resolution covers the user-reported instances. The anti-pattern has
  now appeared twice (BUG-002, BUG-007) — gate at authoring on every
  new entry, per the rule in the procedure manual §F.17.4.

**BUG-008 — n5-004 cm[0] folk-linguistic "intransitive" claim:**

n5-004 cm[0] WHY field said "あう (to meet) is intransitive in
Japanese — it takes に, not を." This is folk linguistics: 会う
takes に because it is an encounter/contact verb (相手を必要とする
動詞), not because it is intransitive. Many transitive verbs also
take に; 会う itself is sometimes classified as transitive.

**Resolution:** rewrote cm[0] WHY to describe the verb's actual
argument structure ("encounter-target with に, per-verb particle
assignment for encounter/contact verbs") without the intransitive
label.

Note: the initial fix script's gate check failed silently (it
required the string "あう" in the wrong/right fields, but the
wrong field used the past-tense form "あいました" — no "あう"
substring). The Phase-0 regression block surfaced this during
verification; the actual fix was applied via a direct edit after
the regression-block run. Lesson: gate checks for fixes must be
expressed against grammar-class membership (verb root), not
surface-form substrings.

Coverage of this fix:
- Entries scanned: 178 patterns × ~3-5 common_mistakes = ~600-900
  entries.
- Scan method: regex for the specific folk-linguistic claim shape
  ("intransitive" + encounter-verb root within 40 chars).
- Findings *in the scanned shape*: 1 (n5-004 cm[0]).
- Post-fix regression: Phase-0 block reports 0 hits against the
  refined regex.
- *Related folk-linguistic terminology shapes* (loose "topic vs
  subject" collapse, "auxiliary verb" misapplied, etc.) are
  documented as audit-time heuristics in A53 but not all are
  CI-gated.

**BUG-009 — n5-003 ex[6] uses は instead of が:**

n5-003 is the が-introducing pattern. ex[6] was 「わたしは がくせい
です。」 — uses は, not が. A learner pattern-matching by example
gets a wrong association.

**Resolution:** replaced ex[6] with 「だれが きょうしつに います
か。」 — a true が-using interrogative-subject (one of the
canonical contexts where が is obligatory). Audio re-rendered for
n5-003.6.

Coverage of this fix:
- Examples scanned: n5-003's 7 examples (the only pattern in scope
  for the が-particle alignment check today).
- Scan method: particle-presence assertion on n5-003 examples.
- Findings *in the scanned set*: 1 (ex[6]).
- Post-fix regression: Phase-0 block reports 0 violations for
  n5-003.
- *Other particle-introducing patterns not yet covered*: the
  particle-alignment check today is hard-coded to n5-003. Extending
  to every particle-introducing pattern (n5-009 を, n5-011 で, etc.)
  is a follow-up for a future audit.

**CI invariant planned (not yet wired):** JA-95 —
particle-pattern alignment per example, for every pattern whose
canonical particle is explicitly named.

### Coverage summary at this checkpoint

CI invariants live: 93 (unchanged this batch). New invariants
*planned and documented but not yet wired*: JA-91 (cross-pattern
explanation similarity), JA-92 (JA-EN content-word overlap), JA-93
(mora algorithm equality), JA-94 (pattern-marker presence), JA-95
(particle-pattern alignment). These are gated on (a) a small
authoring step for the markers / particles data files (JA-94,
JA-95) and (b) a pricing/runtime decision on the LLM-judge pass
(JA-92). The Phase-0 regression block in `prompts/N5Improvement.txt`
provides the mechanical floor today; it returned 0/0/0/0 against
the corpus snapshot when committed.

### Documentation propagation (Rule 4)

- ✓ Procedure manual `JLPT Common/`: §F.17 (seven native-teacher
  bug classes — sub-sections F.17.1 through F.17.6 plus the meta-
  lesson F.17 closing).
- ✓ Accuracy prompt: new A49 / A50 / A51 / A52 / A53 / A54 / A55
  audit categories with detection scripts and CI-invariant proposals;
  closing block updated with the 2026-05-16 addendum.
- ✓ N5Improvement prompt: 7 new Section-10 anti-items + Phase-0
  regression block (validated 0/0/0/0 on the current corpus).
- ✓ This AUDIT-COVERAGE doc: addendum above.
- ✓ Excel `feedback/n5-audit-2026-05-04.xlsx` "User Reported Bugs"
  sheet: BUG-003 through BUG-009 marked Fixed (descriptions
  appended with [FIX 2026-05-16] notes); Summary counts updated to
  Total=9 / Fixed=9 / New=0.

### What this addendum does NOT claim

- That every cross-pattern explanation in the corpus has been
  checked — only the n5-098 instance was triaged; the broader
  Levenshtein scan is documented, not run.
- That the entire grammar corpus is free of pattern-instance
  contamination — only the 6 patterns in the markers table are
  CI-gated; the rest rely on future authoring discipline.
- That no folk-linguistic terminology remains in common_mistakes —
  the refined A53 regex covers the specific encounter-verb shape;
  related shapes (topic/subject collapse, etc.) are flagged in the
  audit prompt as manual review items.
- That every particle-introducing pattern's examples align — only
  n5-003 is in the particle-alignment table today.

A future native-teacher review against an extended scope (vocab
pitch_accent.mora, every particle-introducing pattern, full
common_mistakes corpus with LLM-as-judge) is queued as the next
expansion of this coverage matrix.

---

## ADDENDUM 2026-05-16 (Part 2) — BUG-010 close-out

A user-reported crawlability bug (BUG-010) generalized the BUG-001
grammar-only static-mirror fix to every SPA route surface. Resolved
in a 6-stage rollout on 2026-05-16. Phrasing here follows the
writing-discipline rules — coverage bounded to the surfaces and
URLs scanned, not absolutist.

### Bug addressed

**BUG-010 — SPA hash routes invisible to non-JS clients across all
content surfaces (P1/High, Status: Fixed):**

BUG-001 fixed grammar-only static mirrors at `/N5/lessons/<id>.html`.
That fix did NOT address: vocab (1009 entries), kanji (106), reading
passages (54), listening drills (50), or meta routes (home,
changelog, privacy, notices, feedback, settings, test, sitting,
missed, summary). Consequence: search engines could not index ~95%
of the corpus; archive.org could not snapshot any deep link;
social-card scrapers had nothing to read; users with JS disabled saw
only the SPA shell.

**Resolution:** new tool `tools/build_static_mirrors.py` covering
all 6 surfaces in 6 staged commits, with a unified sitemap.xml +
robots.txt.

| Stage | Commit | Surface | Output count |
|---|---|---|---|
| 1 | `1ca8173` | Grammar | 178 + 1 index = 179 mirrors at `/N5/learn/grammar/<id>/index.html` |
| 2 | `06dd57b` | Vocab | 970 unique forms + 1 index = 971 mirrors at `/N5/learn/vocab/<form>/index.html` (form-keyed per SPA route `#/learn/vocab/<form>`) |
| 3 | `dbdd96d` | Kanji | 106 + 1 index = 107 mirrors at `/N5/kanji/<glyph>/index.html` |
| 4-5 | `4419efc` | Reading + Listening | 54 + 50 + 2 indexes = 106 mirrors |
| 6 | `75d0ec1` | Meta routes | 10 mirrors (home / changelog / privacy / notices / feedback / settings / test / sitting / missed / summary) |
| 7 | this commit | Close-out + Rule-4 propagation | — |

### Per-mirror requirements (uniform across all 6 stages)

Each generated file carries:

- Route-specific `<title>` and `<meta name="description">`
- Open Graph (`og:type`, `og:url`, `og:title`, `og:description`,
  `og:site_name`, `og:image`) for social-card previews
- Twitter Card (`twitter:card`, `twitter:title`,
  `twitter:description`)
- `<link rel="canonical">` pointing back to the SPA hash route
  (search engines deduplicate static + interactive against the
  SPA's canonical URL)
- Inline CSS with `prefers-color-scheme: dark` media query
- JS redirect to SPA after 1.5s — long enough that bots aborting
  JS execution before the deadline see the static content; short
  enough that human users don't wait visibly. Skip on `?nojs=1`
  or `?goSPA=0` query params.
- Breadcrumb navigation + content-licence footer

### Cross-linking between surfaces

The mirror graph is fully-navigable from any entry point:
- Vocab pages link to grammar mirrors via `frequent_patterns`
- Reading passages link to vocab + kanji mirrors via
  `vocab_used` + `kanji_used`
- Kanji pages link to other kanji mirrors via `lookalikes`
- Meta `summary` and `test` stubs link to all per-corpus indexes

### Sitemap + robots.txt

- `/N5/sitemap.xml`: 1,373 URLs (sorted + deduped for deterministic
  output)
- `/N5/robots.txt`: `User-agent: * / Allow: / / Sitemap: <abs URL>`

### Coverage of the fix

- Surfaces scanned: 6 (grammar, vocab, kanji, reading, listening,
  meta).
- Entities scanned for mirror presence: every entity in
  data/grammar.json (178), data/vocab.json (970 unique forms /
  1009 sense entries), data/kanji.json (106), data/reading.json
  (54), data/listening.json (50), plus 10 meta routes.
- Phase-0 regression block: returns 0 missing across all 6
  surfaces at this checkpoint.
- Idempotency: re-running `tools/build_static_mirrors.py` produces
  0 written / 1373 unchanged.
- CI: 93/93 invariants green at every stage commit.

### What this resolution does NOT yet cover (acknowledged debt)

- **Playwright snapshot comparison gate.** BUG-010's acceptance
  criteria named this as the build-time consistency check
  (assert mirror content matches what the SPA would render).
  Queued as follow-on; requires Playwright CI infra not yet
  present in this repo.
- **Per-page Open Graph images.** All pages currently share a
  single `og:image` (the app's `icon-512.png`). Per-route OG
  images (pattern name + meaning, kanji glyph + readings, etc.)
  are an enhancement.
- **Hindi locale variants for non-meta surfaces.** Grammar +
  vocab + kanji data carry per-entry Hindi content (`meaning_hi`,
  `gloss_hi`, `meanings_hi`), but the static mirrors only emit
  `index.html` (English). `index.hi.html` per surface is the
  next iteration.
- **CI invariant for mirror presence (JA-NN).** The Phase-0
  regression block in `prompts/N5Improvement.txt` provides the
  mechanical check today; promoting it to a CI invariant after
  the surface stabilizes is queued.
- **Verification of Google's indexing within the BUG-010 14-day
  window.** The acceptance criterion `Google site:gauravaccentureproducts.github.io/JLPTSuccess/N5 returns multiple distinct deep-page results within 14 days of deploy`
  cannot be verified within the commit window — requires
  observation of search-engine crawl latency.
- **Retirement of the older `/N5/lessons/<id>.html` mirror
  surface from BUG-001.** Kept in place to avoid breaking any
  external link that was created against those URLs; supersession
  policy TBD.

### Documentation propagation (Rule 4)

- ✓ Procedure manual `JLPT Common/`: §F.18 (full-surface
  generalization) — extends F.16 (BUG-001 grammar-only); seven
  subsections (path structure, per-page requirements, cross-
  linking, sitemap, stage sequencing, generator architecture,
  acknowledged gaps).
- ✓ Accuracy prompt: new A56 audit category (static-mirror coverage)
  with curl-verification examples and ready-to-wire CI invariant
  proposal.
- ✓ N5Improvement prompt: new Section-10 anti-item +
  Phase-0 regression block (6 mechanical mirror-presence checks
  validated 0/0/0/0/0/0 on the current corpus).
- ✓ This AUDIT-COVERAGE doc: addendum above.
- ✓ Excel `feedback/n5-audit-2026-05-04.xlsx` "User Reported Bugs"
  sheet: BUG-010 marked Fixed; description appended with
  [FIX 2026-05-16] note; Summary counts updated to Total=10 /
  Fixed=10 / New=0.

### Coverage summary at this checkpoint

CI invariants live: 93 (unchanged this batch). The Phase-0
regression block introduced today covers mirror-presence
mechanically; promotion to JA-NN gate is queued as follow-on once
the surface settles. The new invariants from BUG-003…BUG-009
batch (JA-91…JA-95) remain documented as planned but not yet wired
(same as the previous addendum).

---

## ADDENDUM 2026-05-16 (Part 3) — BUG-011 close-out

A user-reported follow-on to BUG-007 (ISSUE-005) caught the
schema-level expression of the same anti-pattern: WHY rationales
say "both forms correct" while the underlying `wrong`/`right`
field-name dichotomy still labels one form as wrong. Resolved on
2026-05-16 via schema migration + UI + static-mirror generator
updates.

### Bug addressed

**BUG-011 — Self-contradicting WRONG/RIGHT labels across
common_mistakes entries (P1/High, Status: Fixed):**

BUG-007 rewrote 11 common_mistakes WHY rationales to use
register-variant framing instead of WRONG/RIGHT. But the entries
still had the `wrong`/`right` field-name dichotomy in the JSON
data; the UI renders `wrong` cells with red strike-through and
`right` cells with green check, so the visual hierarchy continued
to label grammatically-valid alternatives as WRONG.

**Resolution:** schema-level fix — add `kind: "register_variant"`
field to affected entries, plus optional `label_a` / `label_b`
register tags. UI rendering checks `kind` and applies neutral
"Form A / Form B" presentation when the flag is set; entries
without `kind` fall through to legacy wrong/right styling.

### Migration scope

Original BUG-011 description named 18 entries across 14 patterns
(7 register/formality cases + 7 ね-vs-か pragmatic confirmation +
4 implied register cases). During close-out, the Phase-0
regression block A57 (the regex check just added in this addendum)
surfaced 9 ADDITIONAL entries of the same class that hadn't been
in the original bug list. Both batches were migrated, bringing the
total to **27 entries across 19 patterns**:

| Pattern | Indices | Theme |
|---|---|---|
| n5-023, n5-052-057 | cm[2] / cm[1] each | ね-vs-か confirmation pragmatic |
| n5-069 | cm[3] | てから vs 〜て connective |
| n5-071 | cm[2] | polite-request ね softener |
| n5-105 | cm[0] | たくありません vs たくないです (rigid/natural) |
| n5-107 | cm[3] | plain 行く vs polite 行きます |
| n5-113 | cm[0] | 三十分 vs はん (full/casual) |
| n5-124 | cm[0,1,2] | しかし vs でも (formal/casual) |
| n5-125 | cm[0,1,2] | では vs じゃ (formal/casual) |
| n5-127 | cm[1] | けれども vs けど (formal/casual) |
| n5-158 | cm[2] | でしょう vs だろう (polite/casual) |
| n5-159 | cm[2] | ですね vs だね (polite/casual) |
| n5-173 | cm[2] | ないといけない (n5-175) vs なくてはいけない (n5-173) |
| n5-176 | cm[1,2] | なくては vs なくちゃ (full/casual) |
| n5-179 | cm[0,1,2] | と vs って (formal/casual) |

One related entry was EXCLUDED from migration after manual
inspection: **n5-176 cm[0]** (`行かなくちゃです` vs `行かなくちゃ` /
`行かなければなりません`) is a *genuine grammar error*, not a register
variant — the WHY says "they don't combine [with です]" and "sounds
wrong". The regression block was updated with an
`ERROR_DISQUALIFIERS` regex to skip entries whose WHY explicitly
identifies a grammar error.

### Three-layer fix

1. **Data** (`data/grammar.json`):
   - 27 entries get `kind: "register_variant"` + `label_a` +
     `label_b`
   - Original `wrong` / `right` keys preserved for backwards
     compatibility (the values now semantically = "form A" / "form B"
     for those entries, but the key names stay)

2. **SPA UI** (`js/learn-grammar.js` + `css/main.css`):
   - `mistakes.map()` checks `cm.kind` before rendering
   - `kind === "register_variant"` → render with `.variant-pair`
     CSS class (orange-tinted border, no strike-through, register
     labels in front of each form)
   - Otherwise → legacy `.wrong` / `.right` rendering preserved
   - New CSS rules: `.mistakes-list li.variant-pair`,
     `.variant-row`, `.variant-label`

3. **Static-mirror generators**
   (`tools/build_static_mirrors.py` +
   `tools/build_lesson_html_mirrors.py`):
   - Split common_mistakes into two sections: "Common mistakes"
     (errors) and "Register variants — both forms are correct"
   - Register-variant entries render with `[<label_a>]` / `[<label_b>]`
     prefixes instead of ✗/✓ markers
   - Inline CSS extended with `.variant-pair` / `.variant-row` /
     `.variant-label` rules + dark-mode support

### Coverage of the fix

- Entries scanned for the register-variant signal: every
  common_mistakes entry across 178 grammar patterns (~600-900
  entries total).
- Scan method: Phase-0 regression block A57 — regex match on
  variant WHY phrases ("both are correct", "register choice",
  "formal full form", "casual contraction", etc.) and variant
  cell phrases ("(in casual ...)", "(in formal ...)", "correct
  but rigid"). Skip entries whose WHY contains
  ERROR_DISQUALIFIERS ("don't combine", "sounds wrong",
  "ungrammatical", etc.).
- Findings in the scanned shape: 27 (migrated) + 1 excluded as
  legitimate error.
- Post-fix regression: A57 returns 0 unflagged register variants.
- CI: 93/93 invariants green.

### What this resolution does NOT yet cover

- **Promotion of A57 to a CI invariant.** The Phase-0 regression
  block is mechanical and runs as part of the audit pipeline; a
  hard CI gate (JA-NN) is queued.
- **The same anti-pattern in `wrong_corrected_pair` entries**
  (BUG-002's class). BUG-011 covered common_mistakes only; a
  parallel audit of `wrong_corrected_pair` entries with the same
  regex would close that surface too. Queued.
- **Locale strings for register-variant labels.** The label_a /
  label_b values are English-only today (e.g. "formal full form
  (けれども)"). Hindi translations of the labels are deferred to
  the Hindi-locale completion pass.

### Class lineage

The class has surfaced 3 times in 2 days:
- **BUG-002 (2026-05-16):** `wrong_corrected_pair` mislabel —
  verb-class disambiguation. Fix touched the data only.
- **BUG-007 (2026-05-16):** 11 common_mistakes WHY rationales
  rewritten to register-variant framing. Fix touched WHY text only;
  schema unchanged.
- **BUG-011 (2026-05-16):** schema-level fix — the dichotomy that
  BUG-007's rewrites implied. Fix touched data + UI + static
  mirrors + regression block.

If a fourth bug in this class appears, treat as authoring-pipeline
process failure rather than a one-off data fix — gate at authoring
(promote A57 to a CI invariant).

### Documentation propagation (Rule 4)

- ✓ Procedure manual `JLPT Common/`: §F.19 (schema-level fix for
  register-variant common_mistakes; extends F.17.4 with the
  schema layer + UI rule + authoring rule + 3-bug class lineage).
- ✓ Accuracy prompt: new A57 audit category with the regression
  script and ERROR_DISQUALIFIERS regex.
- ✓ N5Improvement prompt: new Section-10 anti-item + Phase-0
  regression block A57 (validated 0 on the corpus).
- ✓ This AUDIT-COVERAGE doc: addendum above.
- ✓ Excel `feedback/n5-audit-2026-05-04.xlsx` "User Reported Bugs"
  sheet: BUG-011 marked Fixed with the 27-entry migration noted;
  Summary counts: Total=12 / Fixed=11 / New=1 (BUG-012 remains).

---

## ADDENDUM 2026-05-16 (Part 4) — BUG-012 close-out

A user-reported follow-on to BUG-003 caught the trust-signal gap
that the field-value `review_status: "native_reviewed"` carried
across 1,758 entries when assigned by an LLM persona, not a human.
Resolved on 2026-05-16 via field rename + provenance field
addition + consumer updates.

### Bug addressed

**BUG-012 — `review_status: "native_reviewed"` misleads when read
per-pattern (P2/Medium, Status: Fixed):**

All 1,758 items across 7 content corpora carried
`review_status: "native_reviewed"`. The `_meta` block disclosed the
value was assigned by Claude acting as a native-reviewer persona,
not by an actual native human Japanese teacher. The per-item label,
read in isolation by downstream tooling, UI badge surfaces, or
third-party adopters, implied human-native review.

BUG-003 (n5-098 with 10/10 wrong translations on a pattern carrying
this label) proved the label was unreliable. The fix needed to
disambiguate at the point of use.

**Resolution:** Option B (preferred) from the bug description:
rename the value AND add a provenance field.

- `review_status: "native_reviewed"` → `review_status: "ai_quality_reviewed"`
- New field: `review_status_provenance: "claude_native_reviewer_persona"`
- Reserved future value: `human_native_reviewed` (for a real
  human-native review pass; not currently in use)
- _meta block of each corpus gains a `review_status_note`
  explanation

### Migration scope

| Corpus | Renamed | Notes |
|---|---|---|
| `data/grammar.json` | 178 | All patterns |
| `data/vocab.json` | 1009 | All entries |
| `data/kanji.json` | 106 | All kanji |
| `data/reading.json` | 54 | All passages |
| `data/listening.json` | 50 | All drills |
| `data/authentic.json` | 100 | 88 `llm_curated` entries unchanged |
| `data/questions.json` | 261 | All questions |
| **Total** | **1758** | |

### Consumer updates

1. **`tools/check_content_integrity.py` JA-35 invariant:**
   - Enum extended to {`ai_quality_reviewed`, `llm_curated`,
     `auto_generated`, `native_reviewed`}
   - `native_reviewed` retained as a transitional accepted value
     during the migration window; should be removed from the
     accepted set after one release cycle to force any
     missed-migration item to surface
   - Docstring updated to document the rename + future
     `human_native_reviewed` value

2. **`js/provenance-badge.js`:**
   - `corpusProvenanceStats()` returns `aiQualityReviewed` /
     `percentAiQualityReviewed` (with `nativeReviewed` /
     `percentNative` kept as legacy aliases for one release cycle)
   - `renderItemBadge()` accepts both new and legacy values
     during migration; both render as "AI quality-reviewed" — NOT
     "Native-reviewed"
   - `renderCorpusBanner()` displays "{N} of {T} items
     AI-quality-reviewed"
   - CSS class `badge-native` → `badge-ai-quality` (visually
     identical for now; styling can diverge later)

3. **`js/min/provenance-badge.js`:** rebuilt via
   `tools/build_min_js.py` (esbuild).

4. **`_meta` blocks:** each of the 7 corpus files gains a
   `review_status_note` field explicitly stating the value was
   AI-assigned and naming the future plan.

### Coverage of the fix

- Items scanned for the retired value: every item with a
  `review_status` field across all 7 content corpora (1758 total
  + 88 already-`llm_curated`).
- Scan method: Phase-0 regression block A58 — direct enum check.
- Findings: 1758 items migrated (100% of items previously
  `native_reviewed`).
- Post-fix regression: A58 returns 0 retired values / 0 unknown
  values.
- CI: 93/93 invariants green.

### What this resolution does NOT yet cover

- **Removal of `native_reviewed` from the JA-35 accepted enum.**
  Kept as a transitional accepted value for one release cycle;
  removal will force any missed-migration item to surface as a CI
  failure. Queued for the next batch.
- **Per-corpus badge gates** based on
  `human_native_reviewed` percentage. The Q21 launch policy now
  references the future value; until a real human-native review
  pass crosses the 10% threshold, the badge UI stays off (or
  labels items as "AI quality-reviewed", never "Native-reviewed").
- **CSS divergence** between `badge-ai-quality` and a future
  `badge-human-native`. Currently visually identical; styling
  divergence is queued for when the human-native value exists.
- **Human-native review pipeline.** This bug fixes the labeling;
  it does NOT introduce the review pipeline itself. A future
  audit (budget + reviewer recruitment + per-pattern review
  workflow) is separate.

### Documentation propagation (Rule 4)

- ✓ Procedure manual `JLPT Common/`: §F.20 (provenance labels
  must disambiguate human vs AI review at the point of use).
- ✓ Accuracy prompt: new A58 audit category with the retired-
  value check and 4-value future enum.
- ✓ N5Improvement prompt: new Section-10 anti-item +
  Phase-0 regression block A58 (validated 0/0 on the corpus).
- ✓ This AUDIT-COVERAGE doc: addendum above.
- ✓ Excel `feedback/n5-audit-2026-05-04.xlsx` "User Reported
  Bugs" sheet: BUG-012 marked Fixed. Summary counts:
  Total=12 / Fixed=12 / New=0.

### Final state — all 12 user-reported bugs closed (as of BUG-012)

After BUG-012's close-out, every bug on the User Reported Bugs
sheet was in `Status: Fixed`:

| # | Severity | Summary |
|---|---|---|
| BUG-001 | High/P2 | Static mirrors for SPA hash routes (grammar) |
| BUG-002 | High/P1 | Verb-class particle disambiguation |
| BUG-003 | Critical/P1 | n5-098 explanation + 10 translations |
| BUG-004 | Critical/P1 | 911 pitch_marks.mora corrections |
| BUG-005 | High/P1 | n5-166 ex[5] JA/EN cross-contamination |
| BUG-006 | High/P1 | 10 pattern-instance contaminations |
| BUG-007 | High/P1 | 11 RIGHT/WRONG-framed alternatives |
| BUG-008 | Medium/P2 | n5-004 folk-linguistic "intransitive" |
| BUG-009 | Medium/P2 | n5-003 ex[6] uses は not が |
| BUG-010 | High/P1 | Static mirrors for ALL surfaces |
| BUG-011 | High/P1 | Schema-level register-variant migration |
| BUG-012 | Medium/P2 | Provenance-label disambiguation |

CI invariants live: 93. New invariants documented as
ready-to-wire: JA-91 (cross-pattern explanation similarity),
JA-92 (JA-EN content-word overlap), JA-93 (mora algorithm
equality), JA-94 (pattern-marker presence), JA-95 (particle-
pattern alignment), plus the static-mirror coverage and
register-variant kind-flag and BUG-012 retired-value checks
implemented as Phase-0 regression blocks. Promotion of any of
these to hard CI gates is queued.

---

## ADDENDUM 2026-05-17 (Part 9) — BUG-023 close-out (inverse of BUG-020)

A re-audit of kanji.json ↔ vocab.json cross-file integrity one day
after BUG-020/021/022 closed surfaced 5 mismatches in the OPPOSITE
direction. BUG-020's fix script + the narrow JA-100 invariant
addressed kanji.json kanji forms with OOS-kanji content. BUG-023
catches the symmetric case: kanji.json kanji forms with IN-SCOPE
kanji content, but vocab.json still has kana-only forms for the
same vocab_id.

### Bug addressed

**BUG-023 (Medium/P2)** — 5 cross-file form mismatches where the
kanji ARE in N5 whitelist:

| Kanji entry | kanji.json form | vocab.json form (was) | vocab.json form (now) |
|---|---|---|---|
| 友 compound[0] | 友だち | ともだち | **友だち** |
| 手 compound[0] | 手 | て | **手** |
| 手 compound[?] | 上手 | じょうず | **上手** |
| 足 compound[0] | 足 | あし | **足** |
| 目 compound[0] | 目 | め | **目** |

(Plus 上's compound for 上手 was also updated to match — caught
by the strict JA-100 during validation.)

Resolution: vocab.json form upgraded from kana to kanji (the inverse
of BUG-020's "remove kanji from kanji.json" approach). All 5 kanji
are in scope; the kana-only forms were just an inconsistency from
earlier authoring. IDs kept stable for cross-corpus reference
preservation.

**CI invariant JA-100 TIGHTENED** from narrow-OOS-only to strict
form-equality. The original narrow scope was the wrong call — it
accepted "intentional form-shape divergence" but missed real bug
class. Strict equality is the correct default; OOS-kanji compounds
are removed (BUG-020 pattern), in-scope kana-only vocab forms are
upgraded (BUG-023 pattern). Either way, the two corpora match.

### Lesson — default to strict CI gates

The BUG-020 → BUG-023 round-trip cost an extra audit cycle because
the initial JA-100 was too loose. Procedure manual F.22.1 now
explicitly warns: **start with strict gates; loosen only when a
real false-positive surfaces with documentation.** Narrow-scope-
by-default is a footgun — the false negatives don't ring CI bells
but they ARE bugs.

### Coverage at this checkpoint

CI invariants: 100 (unchanged this batch; JA-100 was tightened, not
added). The previously-reserved JA-91..95 remain unwired per prior
addenda.

### Documentation propagation (Rule 4)

- ✓ Procedure manual `JLPT Common/`: §F.22.1 extended with the
  TIGHTENING subsection covering the BUG-023 follow-up lesson.
- ✓ N5Improvement prompt: 1 new Section-10 anti-item on
  "default to strict-equality CI gates, not narrow-scope ones".
- ✓ This AUDIT-COVERAGE doc: addendum above.
- ✓ Excel `feedback/n5-audit-2026-05-04.xlsx`: BUG-023 Status=Fixed.
  Summary: Total=23, Fixed=23, New=0.

### Final state — all 23 user-reported bugs closed

vocab.json: 995 entries (form-field changes on 5 entries; count
unchanged). kanji.json: 106 entries (1 compound form aligned on 上).

---

## ADDENDUM 2026-05-17 (Part 8) — BUG-020..022 close-out (kanji corpus data quality)

A native-teacher audit of `kanji.json` on 2026-05-17 surfaced 3
bug classes parallel to BUG-014..019's vocab-corpus issues. All
fixed in one batch. CI 97 → 100 invariants (+3: JA-100, JA-101,
JA-102).

### Bugs addressed

**BUG-020 (Medium/P2)** — BUG-017's vocab-side fix didn't propagate
to kanji.json. Compounds 週末 (in 週) and 国籍 (in 国) still
displayed OOS kanji 末 and 籍. Resolution: option (c) from the
bug description — removed the OOS-kanji compounds + their auto-
derived examples (cleanest pedagogical fix; 末/籍 are N4 anyway).
JA-100 validation surfaced one more case (手紙 in 手 — 紙 is OOS);
removed in the same pass. **CI gate:** JA-100.

**BUG-021 (Medium/P2)** — `primary_reading` set to on-yomi for 6
kanji whose standalone N5 use is the kun-yomi: 人 (にん→ひと),
中 (ちゅう→なか), 外 (がい→そと), 東 (とう→ひがし),
車 (しゃ→くるま), 国 (こく→くに). On-yomi remains in the `on` array
and audio_yomi map; only the canonical-association field flipped.
Each entry carries `primary_reading_provenance` audit-trail.
**CI gate:** JA-102 (locks these 6 specific kanji).

**BUG-022 (Low/P3)** — `examples[]` field-name inconsistency:
374 `form` + 20 `lemma` + 14 dual. Migrated all to `form` only;
dropped `lemma`. Provenance signal stays in `auto_derived` +
`vocab_id`. Same class as BUG-015 (vocab counter schema).
**CI gate:** JA-101.

### Coverage at this checkpoint

CI invariants: 100 (was 97; +3 from JA-100..102). The previously-
reserved JA-91..95 remain unwired per prior addenda.

### Class lineage

BUG-020..022 are a "kanji-corpus quality" family — parallel to
BUG-014..019's "vocab-corpus quality" family. The two families
together cover the **content / schema / coverage** layers across
both the kanji and vocab corpora. Reading, listening, and authentic
corpora would presumably have their own bug families discoverable
by an analogous audit pass; queued as future work.

### What this resolution does NOT yet cover

- **Other corpora audits** (reading.json, listening.json,
  authentic.json, questions.json) — no native-teacher pass yet
  documented for those surfaces.
- **OOS kanji in OTHER kanji.json fields** — JA-100 currently
  covers `n5_compounds` + `examples`. `sentences`, `mnemonic`,
  `etymology` may also carry OOS kanji that's not yet gated.
  Future audit pass.
- **Cross-corpus form-shape divergence** is currently ACCEPTED
  (kanji.json kanji forms vs vocab.json kana forms is intentional
  pedagogy). A future iteration could introduce a `display_form` /
  `canonical_form` split if pedagogical needs diverge further.

### Documentation propagation (Rule 4)

- ✓ Procedure manual `JLPT Common/`: §F.22 (4 subsections covering
  BUG-020/021/022 + meta-lesson on per-corpus audit passes).
- ✓ N5Improvement prompt: 3 new Section-10 anti-items.
- ✓ This AUDIT-COVERAGE doc: addendum above.
- ✓ Excel `feedback/n5-audit-2026-05-04.xlsx`: BUG-020/021/022 all
  Status=Fixed. Summary: Total=22, Fixed=22, New=0.

### Final state — all 22 user-reported bugs closed

The bug-roster table now extends to BUG-022 (the kanji-corpus
batch). vocab.json: 995 entries (unchanged this batch).
kanji.json: 106 entries (count unchanged; 3 compounds + 2 auto-
examples removed; field migration on 32 examples).

---

## ADDENDUM 2026-05-16 (Part 7) — BUG-019 close-out (BUG-018 heuristic miss)

A native-teacher re-audit immediately after BUG-018's close-out
surfaced 3 MORE subset-gloss duplicates that the BUG-018 hand-
curated list had missed: 月 (Time/Nature), あつい
(Weather/Adjectives — a duplicate within the 4-entry homophone
cluster), きって (Money/Common-Nouns).

**Resolution:** same approach as BUG-018 — pick canonical, merge
data, drop duplicate, rewrite cross-refs. vocab.json 998 → 995.
30 cross-corpus references rewritten across 5 files. Edge case
intentionally preserved: いくつ has 2 entries with DIFFERENT POS
(question-word vs counter) — legitimate polysemy.

**Lesson captured in F.21.5:** hand-curated case lists miss the
full population. The procedure manual now documents an automated
subset-detector script that groups vocab by (form, reading) +
guards on same-POS + flags strict-substring gloss pairs. The
script would have caught all 13 cases (BUG-018's 10 + BUG-019's 3)
while correctly skipping いくつ.

**Locks updated:** JA-56 (998→995), CONTENT-LICENSE.md vocab count
claim. CI invariants unchanged: 97/97 green.

**Final state — all 19 user-reported bugs closed:**
The table from Part 6 extends by one row: BUG-019 (Low/P3) — 3
subset-gloss duplicates missed by BUG-018. Summary in the Excel
sheet: Total=19, Fixed=19, New=0, Pending=0.

---

## ADDENDUM 2026-05-16 (Part 6) — BUG-014..018 close-out (vocab data quality)

A native-teacher re-audit on 2026-05-16 surfaced 5 vocab-corpus
data-quality bugs (BUG-014 through BUG-018) spanning the three
operational layers of content / schema / coverage. All fixed in one
batch on 2026-05-16. CI invariants JA-96 through JA-99 added to
prevent regression. Vocab corpus now at 998 entries (was 1009;
-10 from BUG-018 dedup, -1 from BUG-017 collision merge with a
pre-existing kana entry).

### Bugs addressed

**BUG-014 (High/P1)** — Template-generated semantic-nonsense
examples. 19 entries had a bare `<form>が あります。` template
applied to time words, abstract nouns, and bare locations.
Resolution: replaced each with a natural-frame example matching
the noun type (time → に-anchor; location → with-qualifier;
concrete → eat/buy/possession; abstract → drop あります frame).
**CI gate:** JA-96.

**BUG-015 (Medium/P2)** — Counter / counter_register schema
inconsistency. 3 shapes (string / dict / null) across 1009 entries.
counter_register field was doubly-overloaded (register hint vs
counter-word metadata). Resolution: normalized to
`counter: null | {kanji, reading}`; `counter_register: null` (deprecated);
moved 16 counter-word metadata entries to new
`counter_word_metadata` field. **CI gate:** JA-97.

**BUG-016 (Medium/P2)** — Transitivity coverage gap. 22 of 132
verbs declared (17%); 110 N5-core verbs (食べる, 飲む, 行く, 会う,
する, …) had no classification. Resolution: classified all 132
with closed enum {transitive, intransitive, contact}; provenance
field `transitivity_provenance` records the source. **CI gate:** JA-98.

**BUG-017 (Medium/P2)** — 3 OOS kanji in vocab forms
(倍, 籍, 末). Resolution: replaced forms with kana (conservative
N5 path); IDs kept stable. Edge case: 週末→しゅうまつ rename
collided with a pre-existing しゅうまつ entry, requiring follow-on
dedup. **CI gate:** JA-99 (any kanji in vocab `form` must be in
N5 whitelist or exception list).

**BUG-018 (Low/P3)** — 10 cross-section duplicate vocab entries
with subset glosses. Resolution: picked canonical section per
form, merged unique data, dropped duplicates, rewrote 75
cross-corpus references. Plus 1 additional dedup from the
BUG-017 collision. Net: vocab 1009 → 998. Locks updated:
JA-56 (1009→998), JA-67 (24→25 below-floor — 道 lost one usage),
JA-47 (CONTENT-LICENSE.md count claim 1009→998).

### Coverage summary at this checkpoint

CI invariants: 97 (was 93; +4 from JA-96..99). The 5 previously-
reserved invariants JA-91..95 remain documented but not yet wired
(per the BUG-003..009 addendum).

Phase-0 regression blocks added: 0 explicit new ones (the new CI
gates cover the regression-detection role directly).

### Class lineage

This is a different shape from the BUG-002 → BUG-007 → BUG-011 →
BUG-013 recurring class. BUG-014..018 are 5 distinct vocab-corpus
quality bugs surfaced by one native-teacher audit pass on
2026-05-16, each closed in the same batch. The procedure manual's
new §F.21 organizes them under the three operational layers
(content / schema / coverage) so an Nx-builder can scan for the
same anti-patterns in their corpus.

### What this resolution does NOT yet cover

- **Extension of JA-99 to other display surfaces.** Currently
  covers `vocab.form` only. Future work: extend to
  `examples[].ja`, `kanji.compounds`, `listening.script_ja`, etc.
- **Polysemy taxonomy.** The dedup criterion ("same form + reading
  + subset gloss = drop; otherwise polysemy") was applied
  manually. A future audit could formalize the taxonomy with a
  dictionary-based decision tree.
- **Source-of-truth integration for transitivity.** The
  classification used N5 pedagogical convention; a future pass
  should cross-check against JMdict's vt/vi tags as a regression
  guard.
- **Vocab-corpus mirror count.** Static-mirror count dropped from
  971 to 969 unique forms after dedup. The sitemap.xml reflects
  this automatically; the BUG-010 mirror generator's mirror-presence
  Phase-0 check continues to pass against the new count.

### Documentation propagation (Rule 4)

- ✓ Procedure manual `JLPT Common/`: §F.21 (6 subsections covering
  the 5 bug classes + a meta-lesson on schema/coverage/content
  layers).
- ✓ Accuracy prompt: no new A-category added (the bug classes are
  captured at the F.21 layer in the procedure manual + Section-10
  anti-items in the improvement prompt; the audit-prompt's existing
  A-categories already cover adjacent ground).
- ✓ N5Improvement prompt: 5 new Section-10 anti-items (one per bug)
  with detection patterns.
- ✓ This AUDIT-COVERAGE doc: addendum above.
- ✓ Excel `feedback/n5-audit-2026-05-04.xlsx` "User Reported Bugs"
  sheet: BUG-014..018 all marked Fixed. Summary: Total=18,
  Fixed=18, New=0. **All 18 user-reported bugs closed.**

### Final state — all 18 user-reported bugs closed

| # | Severity | Summary |
|---|---|---|
| BUG-001 | High/P2 | Static mirrors for SPA hash routes (grammar) |
| BUG-002 | High/P1 | Verb-class particle disambiguation |
| BUG-003 | Critical/P1 | n5-098 explanation + 10 translations |
| BUG-004 | Critical/P1 | 911 pitch_marks.mora corrections |
| BUG-005 | High/P1 | n5-166 ex[5] JA/EN cross-contamination |
| BUG-006 | High/P1 | 10 pattern-instance contaminations |
| BUG-007 | High/P1 | 11 RIGHT/WRONG-framed alternatives (WHY rewrites) |
| BUG-008 | Medium/P2 | n5-004 folk-linguistic "intransitive" |
| BUG-009 | Medium/P2 | n5-003 ex[6] uses は not が |
| BUG-010 | High/P1 | Static mirrors for ALL surfaces |
| BUG-011 | High/P1 | Schema-level register-variant migration (flag added) |
| BUG-012 | Medium/P2 | Provenance-label disambiguation (review_status rename) |
| BUG-013 | High/P1 | Schema-level register-variant follow-on (key rename) |
| BUG-014 | High/P1 | 19 vocab template-nonsense examples |
| BUG-015 | Medium/P2 | counter schema normalization |
| BUG-016 | Medium/P2 | Transitivity coverage for 110 verbs |
| BUG-017 | Medium/P2 | 3 OOS kanji in vocab forms |
| BUG-018 | Low/P3 | 10 cross-section duplicate vocab entries |

CI invariants live: 97 (was 93). New: JA-96 (BUG-014), JA-97
(BUG-015), JA-98 (BUG-016), JA-99 (BUG-017). The previously-
documented-but-unwired JA-91..95 remain queued.

---

## ADDENDUM 2026-05-16 (Part 5) — BUG-013 close-out

A user-reported re-audit of BUG-011 caught that the schema
migration didn't actually rename the data-surface keys. BUG-011's
fix added `kind: "register_variant"` + `label_a` / `label_b` but
kept `wrong`/`right` in place for backwards compatibility. The
data-surface contradiction (literal "wrong" key on a sentence the
same entry's WHY calls valid) remained. BUG-013 completes the
migration by renaming the keys themselves.

### Bug addressed

**BUG-013 — Self-contradicting WRONG/RIGHT labels still present
across 14 common_mistakes entries (P1/High, Status: Fixed):**

BUG-011 marked Fixed with a 27-entry migration, but the entries
still carried `wrong`/`right` as JSON keys. The re-audit flagged
that downstream consumers (humans reading the JSON, third-party
adopters, audit-prompt regression checks) see the literal "wrong"
field on a valid sentence — the data-surface contradiction the
fix was supposed to resolve.

**Resolution:** complete the schema migration.
- `wrong` → `form_a`
- `right` → `form_b`
- (For all 27 entries with `kind: "register_variant"`.)
- Other entries (real grammar errors) keep `wrong`/`right`.

### Migration scope

Same 27 entries from BUG-011 (no scope drift). The fix is purely
a key rename — JA text values are unchanged, all other fields
(`kind`, `label_a`, `label_b`, `why`, `category`, `provenance`,
`audit_wave`, `bug_007_fix_2026_05_16`) preserved exactly.

### Consumer updates

1. **`tools/check_content_integrity.py` JA-64:**
   - Required fields now switch on `kind`:
     - Legacy entries: `{wrong, right, why}`
     - Register-variant entries: `{form_a, form_b, why}`
   - Defense-in-depth: register_variant entries that still carry
     `wrong`/`right` keys fail CI (regression guard).

2. **`js/learn-grammar.js`:**
   - Register-variant rendering reads `form_a`/`form_b` first;
     falls back to `wrong`/`right` only for stale entries (one-
     release-cycle migration window).

3. **Static-mirror generators**
   (`tools/build_static_mirrors.py` +
   `tools/build_lesson_html_mirrors.py`):
   - Same field-fallback pattern.

4. **`js/min/learn-grammar.js`:** rebuilt via
   `tools/build_min_js.py`.

5. **Phase-0 A57 regression block** (in both N5Improvement.txt
   and Japanese language Accuracy check.txt):
   - Added "stale-key regressions" check: any register_variant
     entry carrying `wrong`/`right` keys is flagged.
   - Validated 0/0 against the post-fix corpus.

### Class lineage (4 bugs in 2 days)

- BUG-002 (wcp mislabel — data only)
- → BUG-007 (cm WHY rewrites — text only)
- → BUG-011 (cm schema flag added; keys kept)
- → BUG-013 (cm keys renamed at last)

**Lesson captured in F.19.6:** finish schema migrations involving
user-visible field labels in a single commit — don't leave the
old labels in the data for backwards compat. Consumer-side
fallback in code handles the migration window, not data
duplication.

If a 5th bug in this class appears, treat as authoring-pipeline
process failure beyond doubt. The schema is now stable:
`{kind: register_variant, form_a, form_b, label_a, label_b, why}`.

### Coverage of the fix

- Entries scanned: every register_variant entry across 178
  patterns (27 in scope).
- Scan method: direct key-presence check (Phase-0 A57 update).
- Findings: 27 stale-key instances migrated.
- Post-fix regression: A57 reports 0 unflagged variants + 0
  stale-key regressions.
- CI: 93/93 invariants green (JA-64 updated to the new shape).

### Documentation propagation (Rule 4)

- ✓ Procedure manual `JLPT Common/`: §F.19 extended with
  §F.19.6 (BUG-011 → BUG-013 lesson on finishing migrations in
  one pass).
- ✓ Accuracy prompt: A57 regression block updated to check for
  stale-key regressions in addition to unflagged variants.
- ✓ N5Improvement prompt: same regression-block update; data-
  migration-completeness signal now part of the audit pipeline.
- ✓ This AUDIT-COVERAGE doc: addendum above.
- ✓ Excel `feedback/n5-audit-2026-05-04.xlsx` "User Reported
  Bugs" sheet: BUG-013 marked Fixed; Summary updated:
  Total=13 / Fixed=13 / New=0.
