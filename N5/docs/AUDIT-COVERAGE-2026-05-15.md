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
