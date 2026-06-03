# JLPT N5 - Bug-to-Test-Coverage Traceability Audit (2026-05-31)

This document is the honest accounting of a **meta-audit**: not a content
audit of the corpus, but an audit of whether every *Fixed* bug in the bug
tracker has a corresponding regression guard / test-scenario, and of how
well that coverage is *recorded*.

**Writing-discipline note.** Every count below is bounded by *what was
scanned* (the xlsx snapshot on 2026-05-31 + the 174 CI invariants in
`tools/check_content_integrity.py` at this checkpoint) and *how it was
matched* (the heuristics named per-step). Phrases like "covered",
"residue", "no signal" carry the implicit qualifier *"as determined by the
matching method described, against this snapshot."* A future invariant, or
a per-bug manual read of all 237 rows, may reclassify individual bugs.

Auditor: Claude (LLM), with explicit user authorisation. Trigger: user
question *"check if all the bugs fixed are covered in the test scenarios."*

---

## Session scope

- Surface audited: `specifications/test-scenarios-by-specialist-perspective.xlsx`,
  sheet **"User Reported Bugs"** (245 rows; **237 Fixed**, 3 Open, 2 Deferred).
- Cross-referenced against: the **174 JA-NN content-integrity invariants**
  (the release-blocker CI, `tools/check_content_integrity.py`), the two
  coverage columns ("JA-Invariant Locked" col 10, "Verification Method"
  col 13), and the fix-note text per row.

## Method (layered coverage determination)

A Fixed bug was counted "covered" by the strongest signal available:

1. **Recorded** - coverage col 10 or 13 already populated.
2. **Inferable** - the fix-note text cites a `JA-NN` invariant / "regression"
   / "Playwright" / "verified" / "smoke".
3. **Literal-ID** - the bug's audit-ID (extracted from the title) appears
   verbatim in a JA invariant's registry description.
4. **Class-level** - the invariant's description names a *sibling* bug-ID of
   the same structural class, or enumerates a range covering this bug
   (e.g. JA-132 = "MOB-001..016 mobile-UI compliance batch").

Buckets that a regression test does **not** apply to were separated out:
test-scenario-quality / schema / triage / process bugs (fixing scenario
A-007's wording *is* editing the test), and non-product items (HTTP-header
/ CSP deploy config, native-review queue, tooling).

---

## Findings - coverage ledger (237 Fixed)

| Bucket | Count (pre-audit) | Notes |
|--------|------------------:|-------|
| Recorded coverage (col 10/13) | 44 | populated for recent bugs only |
| Inferable (fix-note cites invariant/regression) | 94 | |
| Invariant cites the bug ID literally | 16 | |
| Class-level (invariant guards the class; ID not in row) | 13 | MOB-001..016 -> JA-132; NTR-FU-002/006 -> JA-151/152; BUG-027 -> JA-68 |
| **Demonstrable coverage subtotal** | **~167 (70%)** | |
| Scenario-quality / schema / triage / process (test N/A) | 38 | |
| Non-product / deferred-human-review / deploy-config | 7 | |
| Genuine product/content residue | 25 | weighed below |

**Headline:** the dominant issue was a **traceability gap, not a testing
gap**. The tracker's own coverage columns were populated for only ~19% of
Fixed bugs while demonstrable coverage was ~70%.

## Action taken this session - traceability back-fill (50 rows)

Back-filled the "JA-Invariant Locked" column for **50 Fixed bugs** whose
cell was blank but whose linkage to a CI invariant is verifiable:

- **46 description-named** - the invariant's own registry description names
  the bug (authoritative, author-declared). Examples: MOB-001..016/020 ->
  JA-132; LLM-001..005 -> JA-123..126; PAPER-001/003/004 -> JA-120/121/122;
  DOKKAI-001/003 -> JA-128/130; REG-001 -> JA-127; GOI-001 -> JA-136/137;
  MOJI-002/006 -> JA-141/143; NTR-FU-001/003/004/007 -> JA-151..154;
  RV-004 -> JA-158; BUG-020..024 -> JA-100..103; BUG-027 -> JA-68 (class).
  BUG-017/018/019 -> JA-56/67 marked as *count-effect* locks (count
  provenance).
- **4 class-level (verified by reading the invariant check, not just the
  description)** - bugs whose exact failure mode an existing invariant
  already guards: **KANJI-006 -> JA-103** ((form,reading) compound-tuple
  uniqueness); **READ-003 -> JA-106** (+JA-19, format_type closed enum);
  **LISTEN-001 -> JA-110** (deprecates `voice_planned`, the field whose
  engine/provider contradiction was the defect); **LISTEN-005 -> JA-111**
  (drops legacy `format`).

Each note is explicitly tagged a cross-reference back-fill, not a
reconstructed fix narrative; no fix details or tool names were fabricated.
Post-back-fill recorded coverage: **90/237**.

## Key methodology finding - verify class-level coverage before adding guards

The audit initially flagged ~10 "structurally guardable" residue bugs as
candidates for new CI invariants. Reading the invariant *checks* (not just
descriptions) showed **the structural ones were already guarded** -
KANJI-006/READ-003/LISTEN-001/LISTEN-005 by JA-103/106/110/111 respectively.
**No new invariants were warranted** (adding them would duplicate existing
guards). The general lesson: an apparent coverage gap is often a
*recording* gap; read the actual invariant logic before concluding a fix is
unguarded, because invariant descriptions cite the *first* bug of a class,
not every sibling.

## Genuine residue (weighed, not closed)

After the back-fill and the class-level verification, the residue that is
*both* unrecorded *and* not structurally guardable is dominated by
**human-judgment correctness** items a regression invariant cannot fully
lock:

- Grammar-fact correctness (e.g. に/と transitivity wording, particle
  examples), translation_en accuracy (RV-001/002), distractor validity
  (MOJI-003/004/007).
- Content-freshness / target items: LISTEN-006 (stale `voice_variety_plan`
  prose), LISTEN-007 (voice-variety target not met), READ-002 (summary
  field language mix).

These belong to the **deferred native-human-review track** already
documented in the project's path-forward notes (see procedure manual F.36.4
and the native-speaker-verification discipline in F.44.21). They are not
gaps a CI invariant should chase.

---

## What this audit does NOT cover (acknowledged limits)

- The bucket boundaries (meta / non-product / residue) use **title-pattern
  heuristics**; a per-bug read of all 237 rows would refine the exact split.
- Coverage was matched against invariant **descriptions + (for the 4
  class-level rows) the check bodies**; the full check logic of all 174
  invariants was not read against all 237 bugs.
- The "~167 / 70%" figure is a *demonstrable-link* count, not a proof that
  each linked invariant fully locks each fix; some (e.g. JA-56/67 count
  locks) guard only part of a fix.
- Open (3) and Deferred (2) bugs were out of scope (only Fixed bugs were
  audited for coverage).

## Artifacts updated in this audit cycle

- **Bug tracker** (class 5): 50 "JA-Invariant Locked" cells back-filled.
- **User-facing/audit docs** (class 9): this file.
- **Procedure manual** (class 8): appendix **F.47** (coverage-traceability
  audit methodology).
- CI: PASS all 174 invariants (the back-fill touches metadata only; the
  Fix-Commit column that JA-146 checks was untouched).

*Deferred (flagged, not silent):* spec section 25.8 closed-bug invariant
lineage was not hand-expanded with the 50 back-fill rows - the tracker xlsx
is the operational record of record for bug-to-invariant mapping; section
25.8 remains the curated lineage narrative.

---

## Part 62 — BUG-243: static mirror HOW TO USE strip (added 2026-05-31)

**Trigger.** User screenshot of `n5-017` (何 / なに・なん) showed an empty
HOW TO USE / 使い方 section on the grammar pattern detail page. User text:
*"no info in highlighted part"*.

**What was actually true (against this commit, as scanned):**

1. The **SPA renderer** (`js/learn-grammar.js renderHowToUseTable`) emits the
   rich section correctly — verified by a headless Playwright probe on
   both the local dev server and the live GitHub Pages deploy
   (`section.pattern-usage` exists with 1365 chars innerHTML / 525 chars
   text; top table = "Question word | 何（なに／なん）"; conjugation
   table = 4 rows なに+を / なん+です / なん+counter / なんで). Horizontal
   sweep across all 175 grammar patterns with `form_rules` confirmed
   non-empty SPA rendering at the current code state.
2. The **static SEO mirror** at `learn/n5-017/index.html` (the
   noscript-readable / pre-SPA-boot fallback) emitted only
   `<h2>Attaches to</h2><p>question_word</p>` — a single technical token.
   The 4 conjugation examples were not in the mirror at all. Anyone
   hitting the mirror with JS disabled, slow boot, or a paused SPA saw
   what the user reported: a section header with effectively no content
   beneath it.
3. This is the **third repetition** of the "builder-alone produces
   stripped content" class. Part 60 caught it on app-header (→ JA-170),
   the 2026-05-30 SW-bump caught it on app-footer (→ JA-172), and this
   audit catches it on the HOW TO USE section (→ JA-173).

**Addressed this part:**

- **`tools/build_static_mirrors.py`** — `_render_grammar_pattern_body` now
  emits `<section class="pattern-usage">` with the SAME structure the SPA
  renders (header chip + top table + conjugation table). The legacy
  `<h2>Attaches to</h2><p>{tokens}</p>` block was removed.
- **`tools/refresh_grammar_howto_in_mirrors.py`** (new) — surgical script
  that opens each `learn/<id>/index.html`, locates the body region
  between `</h1>` and the first `<footer>`, and regenerates the body
  in place using the updated renderer. Preserves app-header,
  app-footer, SPA boot script, canonical URLs, breadcrumb. 178 mirrors
  rewritten; 0 unparseable; 0 missing. The build_static_mirrors.py
  trap (a wholesale run re-migrates ~1,372 hand-patched mirrors) is
  side-stepped by editing in place.
- **JA-173** (new CI invariant): every pattern whose `form_rules.attaches_to`
  is non-empty OR whose `form_rules.conjugations` has ≥ 2 entries must
  have a static mirror containing `class="pattern-usage"` PLUS each
  conjugation `example` string verbatim. Catches both the bare-token
  regression and any drift where a new example is authored but the
  mirror keeps an old one. Verified against this commit:
  `python tools/check_content_integrity.py` → PASS on all 175
  invariants (174 prior + JA-173).
- **`sw.js` CACHE_VERSION** — bumped `v1.17.31 → v1.17.32` so users on
  stale caches re-fetch the regenerated mirrors on their next visit.
  `data/version.json` synced to the same `v1.17.32`.

**Bounded phrasing.** *"Empty"* in the user report refers to the static
mirror render path; the SPA-hydrated render was non-empty *against this
commit's data + JS, at the screenshot timestamp window we can verify*.
JA-173 prevents re-introduction of *the specific bare-token mirror shape*
and *missing-conjugation-example* drift catalogued above; it does not
constrain renderer-side regressions in the SPA (JA-NN-level work item, not
in this audit cycle).

**Pattern class.** *"builder-alone produces stripped content"* keeps
re-surfacing because `build_static_mirrors.py` and the post-build injectors
each own a different slice of the final mirror. Long-term path: fold the
post-build injectors back into the builder so a wholesale rebuild is once
again a true superset of the live mirrors. Tracked as a separate refactor;
out of scope for BUG-243.

**Artifacts updated in this audit cycle:**

- **Code** (class 2): `tools/build_static_mirrors.py`,
  `tools/refresh_grammar_howto_in_mirrors.py` (new),
  `tools/check_content_integrity.py` (+ JA-173).
- **Data** (class 3): `data/version.json` (v1.17.31 → v1.17.32).
- **UI / static mirrors** (class 4): 178 grammar mirrors regenerated.
- **Service worker** (class 2): `sw.js` CACHE_VERSION bumped.
- **Bug tracker** (class 5): BUG-243 row added with JA-173 link.
- **User-facing/audit docs** (class 9): this file.
- **Prompts** (class 7): FP-22 (stale-static-mirror-content) added to
  the Japanese-Accuracy-Check FP catalog; N5Improvement Phase-0 gained
  the JA-173 regression-block.
- **Procedure manual** (class 8): appendix F.48 (HOW-TO-USE-strip
  retrospective + the three-strikes pattern).

## Part 63 - N5 grammar native-review-prep content cleanup (added 2026-05-31)

First-pass cleanup of 9 mechanical issue-classes across all 178 grammar patterns ahead of native review (calibrated on n5-121, then horizontal-deployed). Bounded by the detectors named per class, against this corpus snapshot.

Instance counts found / fixed (data-agnostic detectors):
- C8 raw n5-NNN ids in prose: ~119 patterns / 234+ fields stripped (residual 0). Guard JA-174.
- C9 duplicate cultural note (two fields): 174/178 - render-level de-dup (generator + SPA renderer), not data edits.
- C1 fragmented English: 30 broken "vs ?:" placeholders stripped + 35 ALL-CAPS POS jargon de-jargoned. Guard JA-175.
- C3 overstated register: 17 superlatives softened; correct hard grammar rules LEFT intact (false positives).
- C5 repetitive examples: 7 genuine near-identical duplicates replaced; inherent comparison repetition left. Guard JA-176.
- C6 bilingual labels: 4 sections chipped (誤用/丁寧さ/出典/文化) in generator + renderer.
- C4 false contrast: 1 (n5-121, isolated) -> register_variant. C7 force-fit ladder: 1 (n5-121, isolated).
- C2 inconsistent translations: addressed on n5-121 (calibration); corpus-wide pass deferred to native review.

Deliverable: N5/docs/grammar-review/N5-grammar-178-patterns-for-native-review.docx (one pattern per page, audio dropped, incorrect forms struck, reviewer-notes box, 0 rendered ids).

Provisional / future native-human review: all maintainer-authored JP/English (rewrites, new examples, trimmed ladders, chip labels) is tagged for native confirmation. Registered BUG-245..253. CI guards JA-174/175/176 added (CI at this checkpoint: 178 invariants).

---

## Part 63 - Native-review false-negatives (BUG-247, added 2026-05-31)

A native pass over all 1,027 wrong/correct grammar pairs flagged false negatives
(correct Japanese marked wrong): 4 CRITICAL + 5 HIGH + 13 MALFORMED + the が/は focus
class. All 29 reframed - valid forms to register/intent variants; malformed to genuine
errors; が/は focus note - tagged needs_native_review. The malformed sub-class is locked
by JA-177; the broad class (struck sentence actually valid) is native-judgment, not
auto-guardable. Methodology: procedure manual F.49.
