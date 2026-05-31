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
