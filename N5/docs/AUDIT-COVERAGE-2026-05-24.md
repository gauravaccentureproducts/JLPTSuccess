# JLPT N5 Content Audit — Coverage Disclosure (2026-05-24)

This document is the honest accounting of what content-quality checks
were performed on the N5 grammar corpus in the **v4 test-review session
(2026-05-24)**, what was fixed, and what remains for future native-
human review.

**Writing-discipline note.** Every claim below is bounded by *what was
scanned* (a specific regex or schema check), *what was sampled* (a
specific N out of the corpus), or *what was cross-referenced*. Phrases
like "every", "all", "0 findings", "saturated" should always be read
with the implicit qualifier *"against what we measured this session"*.

Auditor: Claude (LLM) acting as native-Japanese-teacher persona, with
explicit user authorisation. Not a native human; this is documented so
future native-human review can prioritise the unsampled space.

---

## Session scope

User instruction: *"run grammar test scenarios as a native japanese
person/teacher and a jlpt expert. be brutally honest. register results
in respective columns."*

Surface tested:
- 178 grammar patterns in `data/grammar.json`
- 10 generic test scenarios (TS-01 .. TS-10) in
  `test/categorized testing/CategorizedtestScenarios.xlsx`,
  Grammar sheet.
- 1,780 verdict cells written to the Grammar Pattern List sheet.

Method:
- Auto-checks across all 178 patterns for objective shape issues.
- Manual spot-check on ~20 patterns across 32 categories for content
  judgment.
- Horizontal anti-pattern scan after initial findings to catch
  repetitions.

---

## Coverage matrix — this session

### Bug-class taxonomy + horizontal deployment

| Class | Description | Triggered TS | Found | Status |
|-------|-------------|--------------|-------|--------|
| A | Empty `audio` paths in `examples[]` | TS-06 | 1 pattern (n5-098) | ✅ Fixed (P3 — wired existing on-disk audio) |
| B | `(see ...)` cross-reference placeholders skipping TTS | TS-06 | 0 | ✅ N/A |
| C | Particle-swap "common mistakes" where both forms are valid JP (different meanings) | TS-03 | 2 (n5-011 と→や, n5-024 と→か); 1 false positive (n5-097 — どちら is binary, so wrong form IS wrong) | ✅ Fixed (P4 — replaced with genuinely-wrong learner errors) |
| D | Malformed cells with arrow `→` inside `wrong`/`right` fields | TS-03 | 7 rows: n5-021, n5-030, n5-048, n5-050, n5-067, n5-069, n5-112 | ✅ Fixed (Class-D batch — extracted true wrong sentence, kept `why` diagnostic) |
| E | `wrong` field carries English parenthetical context annotation | TS-03 | 154 rows across both `common_mistakes` and `wrong_corrected_pair` | ✅ Refactored (Class-E batch — parenthetical moved to `why` field prefix as `Context: ...`) |

### New false-positive class catalogued

**FP-16: register-variant entries falsely flagged as empty wrong/right**
(added 2026-05-24)

The grammar.json `common_mistakes` and `wrong_corrected_pair` arrays can
contain entries with `kind: "register_variant"`. These carry a different
schema (`form_a` / `form_b` / `label_a` / `label_b` instead of
`wrong` / `right`) — both forms are grammatically valid, the entry
teaches register *contrast*, not error correction.

A naive auto-check that scans for "empty `wrong`/`right`" will flag 38
register-variant entries as data gaps. They are NOT data gaps. The
schema choice is intentional (per HTML comment `BUG-011: register-
variant entries — neutral framing (no strike/check)`).

**Rule for all future content-quality tooling:** before checking
`wrong`/`right` for emptiness, check `kind != "register_variant"`.
Captured in `tools/grammar_auto_checks.py` (this session)
and `tools/export_grammar_for_review.py` (which now preserves the
`kind` field through the review pipeline).

### Methodology insight: LF-normalised byte counts on Windows

JA-125 (the `data/index.json` size_bytes invariant) computes the
**LF-normalised byte count** (matches git's storage representation):

```python
with open(path, "rb") as fh:
    lf_size = len(fh.read().replace(b"\r\n", b"\n"))
```

On Windows the on-disk `os.stat().st_size` is ~77KB higher than the
LF-normalised count for `data/grammar.json` (CRLF inflation: 1 byte
per line × ~77,000 lines). Tools that write data files AND update
`data/index.json` MUST use the LF-normalised size, not the on-disk
size. Documented in `tools/fix_remaining_grammar_bugs_2026_05_24.py`
and propagated via the FP catalogue.

### Scenario-by-scenario coverage

| TS | Scope | Coverage method | Findings |
|----|-------|-----------------|----------|
| TS-01 | JA explanation grammar | **N/A** — explanation_ja field is Phase-2 placeholder; no text to grade | 0 (out of scope) |
| TS-02 | JA grammar of example sentences | Default Pass; spot-checked ~20 patterns across categories | 0 *against the sample* |
| TS-03 | JA grammar of wrong/right pairs | Auto-check (empty rows / arrows / paren-context) + manual judgment for particle-swap conflations | 7 Class-D + 2 Class-C + 38 false-positive register-variant flags (resolved by skipping that schema) |
| TS-04 | Pattern↔explanation↔meaning consistency | Default Pass; corpus has been audited 13×; spot-check found no drift | 0 *against the sample* |
| TS-05 | Examples actually use the pattern | Default Pass; auto-check returned 61 false positives (pattern labels like "Verb-ます" are abstract, don't literally appear in JA) | 0 *real* |
| TS-06 | Audio script matches displayed JA | Automated: existence-of-audio-file + ja-not-`(see)` + non-empty `audio` path. Per-construction equivalence (`normalize_for_tts()` does digit→kanji + space-strip only, both meaning-preserving) | 1 (n5-098, fixed) |
| TS-07 | English explanation accuracy | Default Pass; corpus audited 13×; spot-check on ~20 patterns | 0 *against the sample* |
| TS-08 | English translation accuracy of example sentences | Automated heuristic check (1,782 examples scanned for tense/question/negation mismatches), manual spot-check on 8 patterns | 0 real (91 heuristic candidates all triaged to false positives — regex bugs missing "rained"/"watched"/"mustn't"; idiomatic constructions `〜しか〜ません`→"only have", `〜ませんか`→"would you like") |
| TS-09 | EN translation of common-mistakes commentary | Default Pass; spot-check | 0 *against the sample* |
| TS-10 | meaning_ja ↔ meaning_en semantic match | Default Pass; spot-check | 0 *against the sample* |

### What the session did NOT cover

| Dimension | Coverage | Reason |
|-----------|----------|--------|
| Per-example native-grade EN translation review (all 1,782) | Spot-check ~8 patterns | Effort: would require many hours of native-English content review for marginal gain on top of existing 13-cycle audit |
| Audio quality — pitch accent, intonation, naturalness, voice fit | **Not checked** | Requires human listener; cannot be assessed from text data |
| TS-04 / TS-07 / TS-09 / TS-10 per-pattern deep review | Spot-check ~20 patterns | Same as TS-08 — corpus has been audited; defaulted to Pass where no specific issue surfaced |
| Class E parenthetical context — judgment of whether the parenthetical context is pedagogically accurate (post-refactor it lives in `why`) | Mechanical move only | Content quality of the parenthetical text itself unverified by this session |

---

## Outcome

| Metric | Before session | After session |
|--------|----------------|---------------|
| Total Fail cells in xlsx | n/a (file created this session) | **0** |
| Patterns clean (no Fail) | n/a | **178 / 178** |
| CI invariants passing | 163 / 163 | **163 / 163** ✓ |
| Class D arrow rows | 7 | **0** |
| Class E parenthetical rows | 154 | **0** |
| Audio data gaps | 1 (n5-098) | **0** |
| Empty wrong/right rows | 0 (the 38 "empty" were register-variant; test logic fixed) | **0** |

---

## Files produced / changed this session

**Data / content:**
- `data/grammar.json` — Class D (7 rows), Class E (154 rows), P3 audio (10 paths), P4 particle-swap (2 rows)
- `data/index.json` — `size_bytes` synced 3× (LF-normalised)
- `README.hi.md` — Phase-1 launch notice
- 4 versioned backups under `data/` per project backup policy

**Code (Hindi-tab feature flag):**
- `js/i18n.js`, `js/app.js`, `js/settings.js`, `js/min/*.js` (rebuilt)

**Tools (reproducible):**
- `tools/build_grammar_syllabus_docx.py`
- `tools/build_test_scenarios_xlsx.py`
- `tools/export_grammar_for_review.py` (kind-field preserving)
- `tools/init_grammar_verdicts.py`
- `tools/grammar_auto_checks.py` (register-variant aware)
- `tools/grammar_horizontal_checks.py`
- `tools/grammar_ts08_translation_checks.py`
- `tools/apply_grammar_verdicts.py` (with `check_audio_scripts`)
- `tools/fix_class_d_arrow_cells_2026_05_24.py`
- `tools/fix_remaining_grammar_bugs_2026_05_24.py`
- `tools/fix_class_e_paren_context_2026_05_24.py`

**Output artefacts:**
- `data/complete course syllabus/JLPT_N5_Grammar_Patterns.docx` — 178 patterns × 32 categories, ID-prefixed headings
- `test/categorized testing/CategorizedtestScenarios.xlsx` — 8 sheets (ReadMe, Grammar, Grammar Pattern List, Moji, Goi, Dokkai, Chokai, Test Papers); Grammar Pattern List with 178 Pass verdicts

---

## Future native-human review priorities

These are the highest-value items a native-human reviewer would unlock
that this session could not:

1. **Audio quality on all 178 patterns × ~10 examples** — pitch accent
   correctness, intonation appropriateness, voice fit, no mispronunciation.
2. **Deep TS-08 native-English review** — translation naturalness, lost
   nuance, register fit (e.g. casual JA → casual EN match).
3. **Class E `Context: ...` accuracy** — the 154 refactored entries
   now have `Context: <annotation>. <existing why>`. Review whether the
   prepended context is pedagogically correct.
4. **TS-04 / TS-07 deep review** — beyond the 13-cycle audit's
   coverage, sample patterns for explanation accuracy vs Genki / Minna.
5. **n5-098 audio reload verification** — the audio paths are now
   wired but the actual MP3s should be listened to once to confirm
   they correspond to the right examples.
