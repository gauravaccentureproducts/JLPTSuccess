# Cross-Artifact Synchronization Map

> Operational handbook for **BINDING Rule 5** (set 2026-05-17).
> Whenever ONE artifact changes, every OTHER artifact that
> references or implements the changed thing must be updated
> in the same commit. Atomic only — either all dependents
> land together or the source reverts.

This document maps the protocol's 9 abstract artifact classes
to the concrete files and directories in this repository, plus
the dependency matrix + INV-N invariant catalog. Update this
file whenever a new artifact class enters the project or an
invariant is wired/retired.

## The 9 artifact classes (concrete file map)

### 1. Specifications
- `N5/specifications/JLPT-N5-Current-Implementation-Spec.md` —
  master implementation spec (25 sections; §25 = CI invariants
  reference).
- `N5/specifications/test-scenarios-by-specialist-perspective.xlsx`
  — 14 specialist-perspective test-scenario tabs + 1 derived
  "Unit Tests (Auto-runnable)" sheet + 1 "User Reported Bugs"
  sheet (the bug-tracker artifact).
- `N5/docs/N5-syllabus-methodology.md` — content scope &
  pedagogy methodology spec.
- `N5/docs/RECOMMENDER-RULES.md` — recommendation-engine spec.
- `N5/docs/UNIFIED-REVIEW-QUEUE-DESIGN.md` — review queue spec.

### 2. Code
- `N5/js/*.js` — application source (vanilla, no framework).
- `N5/sw.js` — service worker (cache version derives from
  `data/version.json.cacheVersion`).
- `N5/css/*.css` — styling.
- `N5/tools/*.py` — build / audit / fix scripts.
- `tools/check_content_integrity.py` — CI invariant registry
  (currently 104 invariants pre-Rule-5; protocol install adds
  JA-107/108/109).
- `.github/workflows/*.yml` — CI pipeline.
- `N5/playwright.config.js` + Playwright suite — P0 smoke
  tests + axe-core a11y.
- `N5/package.json` — devDependencies (only Playwright + axe).

### 3. Data / content
- `N5/data/grammar.json` (178 patterns).
- `N5/data/vocab.json` (995 entries — post-BUG-018/019 dedup).
- `N5/data/kanji.json` (106 entries).
- `N5/data/reading.json` (54 passages — post-BUG-041..046 fix).
- `N5/data/listening.json` (50 items).
- `N5/data/questions.json` (290 question entries).
- `N5/data/papers/manifest.json` + `papers/{moji,goi,bunpou,
  dokkai}/*.json` (28 papers / 402 questions).
- `N5/data/version.json` — build-stamp + count manifest
  (consumed by `js/app.js`, `sw.js`, README footer).
- `N5/data/build_metadata.json` — CI-metadata sibling per
  IMP-002.
- `N5/data/pattern_markers.json`, `n5_kanji_*.json`, etc.
- `N5/locales/en.json` + `N5/locales/hi.json` — UI string
  bundles.
- `N5/external-data/*` — third-party reference data (KanjiVG,
  kanjium pitch-accent).

### 4. UI
- `N5/index.html` — SPA shell.
- `N5/learn/grammar/{n5-NNN}/index.html` — static mirrors of
  per-pattern surfaces.
- `N5/learn/vocab/{form}/index.html` — static mirrors.
- `N5/kanji/{glyph}/index.html` — static mirrors.
- `N5/reading/{passage_id}/index.html` — static mirrors.
- `N5/listening/{item_id}/index.html` — static mirrors.
- `N5/changelog/`, `N5/home/`, `N5/missed/`, `N5/notices/`,
  `N5/privacy/`, `N5/settings/`, `N5/lessons/` — meta-route
  mirrors.
- `N5/manifest.webmanifest` — PWA manifest.
- `N5/sitemap.xml` + `N5/robots.txt` — crawlability surfaces.

### 5. Bug tracker
- `N5/specifications/test-scenarios-by-specialist-perspective.xlsx`
  → "User Reported Bugs" sheet (BUG-NNN canonical IDs;
  Summary block tracks Total / Fixed / New).
- BUGS in `N5/feedback/n5-audit-2026-05-04.xlsx` "User
  Reported Bugs" sheet — LEGACY (entries BUG-001..024 first
  landed here; superseded by `specifications/` location for
  BUG-025+). Both files reflect the same bugs; the
  specifications-side file is authoritative.

### 6. Test scenarios
- `N5/specifications/test-scenarios-by-specialist-perspective.xlsx`
  — 14 specialist tabs (A. Japanese language..N. End-user POV)
  + "Unit Tests (Auto-runnable)" derived index (265+ scenarios).
- `tools/check_content_integrity.py` — CI invariant registry
  (104 JA-NN as of 2026-05-17, pre-Rule-5; adds JA-107/108/109).
- `N5/tools/` — fix-script regression tests embedded in each
  fix script's main().
- `N5/feedback/ui-testing-plan.md` + Playwright suite — P0 UI
  smoke + a11y.

### 7. Prompts
- `N5/prompts/Japanese language Accuracy check.txt` — the audit
  prompt (A-NN audit categories, FP-NN false-positive catalog,
  per-batch ADDENDUM blocks).
- `N5/prompts/N5Improvement.txt` — the improvement prompt
  (Phase-0 regression blocks + Section-10 anti-items + 11
  scoring sections).
- `N5/prompts/*` — other situational prompts (e.g.,
  accessibility-audit, security-vulnerability-scan).

### 8. Procedure manuals
- `JLPT Common/procedure-manual-build-next-jlpt-level.md`
  — cross-level build manual (own git repo
  `gauravaccentureproducts/JLPT-Common`, embedded as a
  submodule of JLPTSuccess; appendices F.1..F.23 capture
  methodology + bug-class lessons).
- `N5/docs/NATIVE-AUDIO-WORKFLOW.md` — VOICEVOX render
  procedure.
- `N5/docs/RECORDING-BRIEF.md` + `RECORDING-BRIEF.ja.md` —
  native-recording playbook (queued).
- `N5/docs/REVIEWER-PACK.ja.md` — native-reviewer hand-off
  packet.
- `N5/docs/SELF-HOST.md` + `SELF-HOST.hi.md` — self-host
  deployment runbook.
- `N5/SELFHOST.md` — top-level self-host pointer.

### 9. User-facing docs
- `N5/README.md` + `N5/README.hi.md` — landing docs.
- `N5/CHANGELOG.md` — user-visible release history (linked
  archive in `docs/CHANGELOG-archive.md`).
- `N5/PRIVACY.md` — privacy posture.
- `N5/NOTICES.md` — third-party attribution.
- `N5/CONTENT-LICENSE.md` — content licensing + corpus counts
  (locked by JA-47).
- `N5/AUDIO.md` — audio pipeline notes.
- `N5/SELFHOST.md` — self-host quick-start.
- `N5/TASKS.md` — project task tracker (open / done).
- `N5/docs/AUDIT-COVERAGE-2026-05-15.md` — audit coverage
  disclosure (cumulative, per-batch addenda).
- `N5/docs/PROJECT-OVERVIEW.ja.md` — Japanese-language project
  intro.
- `N5/docs/TRANSLATING.md` — translation contribution guide.

## Dependency matrix (concrete for this project)

Reading the matrix: a change in the SOURCE column triggers checks
of every DEPENDENT marked ✓.

| Source ↓ \\ Dependent → | Spec | Code | Data | UI | Bug | Test | Prompt | Manual | Doc |
|---|---|---|---|---|---|---|---|---|---|
| **Specification** | — | ✓ | ✓ | ✓ | — | ✓ | ✓ | ✓ | ✓ |
| **Code** | ✓ (if behavior) | — | ✓ (if schema) | ✓ (if surface) | — | ✓ | — | ✓ | ✓ |
| **Data / content** | — | ✓ (if shape) | — | ✓ (if rendered) | ✓ (if bug src) | ✓ (fixtures) | ✓ (if cited) | — | ✓ (counts) |
| **UI** | ✓ (if behavior) | ✓ | — | — | — | ✓ | — | ✓ | ✓ (screenshots) |
| **Bug filed/fixed** | ✓ (if spec gap) | ✓ (the fix) | ✓ (the fix) | ✓ (if user-facing) | — | ✓ (regression) | ✓ (if prompt missed) | ✓ (if proc change) | ✓ (CHANGELOG) |
| **Test scenarios** | ✓ (if gap) | ✓ (if fix implied) | — | — | ✓ (file new) | — | — | ✓ (manual ops) | — |
| **Prompts** | ✓ (intent) | — | — | — | — | ✓ (golden output) | — | ✓ (when to invoke) | ✓ |
| **Procedure manuals** | — | ✓ (any tooling) | — | — | — | ✓ (golden path) | — | — | ✓ |
| **User-facing docs** | ✓ (if promised) | ✓ (if surface) | — | ✓ (must match) | — | ✓ (testable) | — | — | — |

If a SOURCE row appears to have no DEPENDENTS for your specific
change, you have **under-identified** the impact. Re-check.

## Sync invariants (INV-1..INV-10 → JA-NN mapping)

The protocol defines INV-1..INV-10 as build-time guards. Each
maps to one or more JA-NN CI invariants in
`tools/check_content_integrity.py` (or to a Phase-0 regression
block in `prompts/N5Improvement.txt` if not yet hard-CI).

| INV | Description | JA-NN coverage | Status |
|---|---|---|---|
| INV-1 | Bug-fix commit touches a test file or annotates "no test" | **`.githooks/commit-msg`** (rejects bug-fix commits without a test / regression / JA-NN / "no test — reason:" annotation) | Convention + commit-hook (2026-05-17; install via `git config core.hooksPath .githooks`) |
| INV-2 | Spec change references corresponding code change; new-field spec adds test | **`.githooks/pre-commit`** (warns when `N5/specifications/*.md` staged without code/data file under N5/) | Convention + commit-hook (2026-05-17) |
| INV-3 | Code public-API change updates API docs | N/A — project has no traditional API (static SPA + content corpus) | Out of scope for this project |
| INV-4 | Data-file count changes update version.json AND CHANGELOG | **JA-107** (version.json.counts ↔ live data) + **JA-47** (CONTENT-LICENSE.md counts ↔ live data) | WIRED 2026-05-17 |
| INV-5 | UI string change propagates to all locales | **JA-108** (`locales/*.json` key-set parity) | WIRED 2026-05-17 |
| INV-6 | Prompt change includes a regression test of golden output | **JA-116** (every A-NN / Phase-0 / FP-NN in prompts has ≥1 matching xlsx scenario row; auto-extracted, asserted at CI). The 2026-05-17 wire-up caught a real drift instance — A5 was missing from xlsx due to a substring-match bug in the b466293 sync (`"A5" in "A55"` was True); fixed inline. | **Wired** (promoted 2026-05-17 from Partial) |
| INV-7 | Cross-file references resolve | JA-15 (audio refs), JA-17 (vocab_id in grammar examples), JA-82 (`_meta.see_also` / `_meta.consumers`), JA-100 (kanji↔vocab form STRICT), JA-105 (vocab_preview vocab_id refs), JA-113 (meta-route mirror reflects source markdown's latest heading), **JA-117** (passage_id kanji↔reading + pattern_id reading↔grammar — 363 + 319 refs all resolve, added 2026-05-17) | **Wired** (promoted 2026-05-17 from Partial after JA-117 covered the canonical remaining cross-corpus ID fields) |
| INV-8 | CHANGELOG entry names every dependent updated | **`.githooks/pre-commit` + `commit-msg`** (pre-commit warns when N5/data/*.json staged without N5/CHANGELOG.md; commit-msg warns on multi-file commits with short message bodies) | Convention + commit-hook (2026-05-17) |
| INV-9 | Closed bug links to fix commit + regression test (or "no test — reason") | **JA-118** (every Fixed row in xlsx User Reported Bugs has a non-empty Fix Commit cell). Companion tool `tools/populate_bug_fix_commits_2026_05_17.py` scans git log for commit subjects mentioning each BUG-NNN (including range patterns like "BUG-041 through BUG-046"); all 53 Fixed bugs populated on 2026-05-17 wire-up. | **Wired** (promoted 2026-05-17 from Partial) |
| INV-10 | Procedure-manual script/tool references resolve | **JA-109** (procedure manual + prompts → script references resolve) | WIRED 2026-05-17 |

**Strategy update (2026-05-17 final batch):** 9 of 10 INVs now
enforced at some layer:
  - 6 hard-wired at CI (INV-4 / INV-5 / INV-6 / INV-7 / INV-9 / INV-10)
    — runs on every push + PR via the content-integrity workflow
  - 3 backed by commit-time git hooks (INV-1 / INV-2 / INV-8) —
    in `.githooks/`, opt-in via `git config core.hooksPath .githooks`

INV-3 stays Out of Scope (project has no traditional API surface
— static SPA + content corpus). The remaining unwired sub-cases
of the wired classes (JA-91 cross-pattern similarity; JA-94
pattern-marker presence) have specific gating notes documented
in spec §25.7 — either need a Japanese-linguistics review pass
or a structural-markers data file authored.

## Commit-time checklist (the 8-step loop)

Use this as a pre-commit walk for any substantive change:

**Step 1 — Identify the SOURCE.** Name the artifact class (one
of the 9 above) and the specific file(s) edited.

**Step 2 — Derive DEPENDENTS.** Look up your SOURCE row in the
matrix. List every ✓-marked dependent.

**Step 3 — Check each DEPENDENT.** Read it. One of:
- (a) updates required → describe what changes
- (b) verified consistent → explain why
- (c) out of scope → explain why not affected

**Step 4 — APPLY the full change set.** Update source + all
(a)-dependents together. Do not commit source alone.

**Step 5 — Run INTEGRITY CHECKS.** Minimum:
- `python tools/check_content_integrity.py` (104 JA-NN; must
  exit 0 / all green)
- `python tools/cross_artifact_sync_report.py` (this batch's
  protocol-install tool — emits structured report; surfaces
  any cross-artifact gap)
- For test-scenario / xlsx changes: re-run
  `tools/build_unit_tests_sheet_2026_05_17.py` to refresh the
  derived sheet.
- For static-mirror surface changes: run
  `tools/build_static_mirrors.py`.

**Step 6 — VERIFY SYMMETRY.** For each updated dependent, check
both directions:
- SOURCE mentions X → DEPENDENT describes X correctly
- DEPENDENT describes X → SOURCE actually does X

**Step 7 — DOCUMENT the ripple.** Add a CHANGELOG entry naming
the source change and every dependent updated. Reference the
commit hash once committed.

**Step 8 — LOOP or EXIT.** If any step surfaced a NEW change
(e.g., updating a doc revealed a spec gap), recurse with that
new change as SOURCE. Continue until no drift remains. Stop at
30 iterations max — if you hit the cap, something is
structurally wrong; surface for human review.

## Exit conditions

- **CLEAN EXIT** — every dependent updated, all CI invariants
  pass, CHANGELOG documents the ripple. Only this is success.
- **POLICY BLOCK** — a required update would violate a binding
  rule (e.g., propagating into `/N4/` is blocked by Rule 1).
  Surface the conflict; do not partial-sync.
- **OSCILLATION** — two consecutive iterations cannot reach a
  consistent state. Surface the cycle and stop.
- **CAP** — 30 cross-artifact propagation iterations in one
  change. Stop; surface for human review.

## Existing-drift policy

If propagating a fresh change reveals **pre-existing drift**
in any artifact class, fix it in the **same change set**. The
protocol's "drift compounds" principle: each missed drift makes
the next change inherit the gap. The Rule-5 install commit
itself demonstrated this — fixing `version.json.counts.vocab`
(1009 → 995, pre-existing drift from the BUG-018/019/024 dedup
batches) was bundled into the same commit as the new
JA-107/108/109 invariants that prevent its recurrence.

## Per-class "what to remember" cheatsheet

**Touching Data?** → Run JA-107 (counts), JA-108 (locales),
JA-47 (license). Update version.json + CHANGELOG + CONTENT-
LICENSE.md if counts change. Update static mirrors via
`tools/build_static_mirrors.py`. Re-run CI.

**Touching Code (tool/build script)?** → Update procedure
manual section if the script is referenced there (JA-109
enforces). Update implementation spec §10 (Build pipeline) if
the script is part of CI.

**Touching UI (rendered surface or copy string)?** → Update
both locales (JA-108). Regenerate static mirrors. Update test
scenarios (xlsx D. UX design tab + E. Accessibility tab).
Refresh README screenshots if a major UI change.

**Closing a Bug?** → Mark Fixed in xlsx "User Reported Bugs"
sheet. Add a regression test (CI invariant or Phase-0 block).
Update procedure manual Appendix F.NN with the lesson.
Update accuracy prompt + N5Improvement with the new audit
category + Section-10 anti-item. Update AUDIT-COVERAGE Part
N with the close-out. Update Section 25.8 lineage table.
Update CHANGELOG.

**Editing a Prompt?** → If the change adds a new audit
category, update Section 25 if it introduces a new CI
invariant. Update procedure manual when a new audit-cycle
methodology is introduced. CHANGELOG entry.

**Editing the Procedure Manual?** → Bump submodule pointer in
parent repo. Update CHANGELOG. If a new tool is referenced,
JA-109 will require the file to exist.

**Editing User-Facing Docs?** → Ensure documented behavior
matches code + UI (JA-47 enforces count-claim alignment for
CONTENT-LICENSE.md; JA-112 for AUDIO.md). Update CHANGELOG.
Refresh any cross-doc links. **If the doc has a meta-route
static mirror** (README.md → home/, CHANGELOG.md → changelog/,
PRIVACY.md → privacy/, NOTICES.md → notices/), run
`python tools/build_static_mirrors.py --stages meta` in the
same commit; JA-113 enforces the mirror's freshness against the
markdown source's latest H1/H2.

## Audit log

| Date | Change | INV-N added | JA-NN added | Drift fixed | Commit |
|---|---|---|---|---|---|
| 2026-05-17 | Protocol install batch (Rule 5 adopted) | INV-4, INV-5, INV-10 wired | JA-107, JA-108, JA-109 | version.json.counts.vocab 1009 → 995 | cdef185 |
| 2026-05-17 | Static-mirror drift + not-required cleanup | — | — | learn/vocab/index.html (BUG-023 leftover) + changelog/index.html (post-cdef185 mirror); 7 not-required/ deletions | f96475b |
| 2026-05-17 | BUG-047..053 listening.json VOICEVOX migration drift | — | JA-110, JA-111 | voice_planned dropped (50 items); audit-status fields (10 items); format dropped (50 items); _meta voice_variety_plan + voicevox_speaker_catalog rewritten | 04bd8f4 |
| 2026-05-17 | Test-scenarios sync with prompts/ + feedback/ | INV-6 → Partial | — | (no data drift; +134 specialist scenarios added across 14 tabs to make prompt/feedback coverage explicit) | b466293 |
| 2026-05-17 | Redundant feedback/ files → not-required/; trim legacy xlsx sheet | — | — | audio-coverage-gaps.json + _n5_richness_audit_20260509.txt moved; "User Reported Bugs" sheet dropped from legacy n5-audit-2026-05-04.xlsx | 8c57f2e |
| 2026-05-17 | BUG-050 charitable close-out — AUDIO.md count + speaker drift | — | JA-112 | AUDIO.md "47 listening items" → "50 items / 6 speakers"; speaker-table character names corrected | 5d14cde |
| 2026-05-17 | BUG-048 + BUG-049 close-out — listening pacing refresh + ffmpeg atempo | — | — | 50 items re-measured; 39 ffmpeg atempo tempo-changes; ALL items in target band 180-240 mpm; bug tracker 53/53 Fixed/0 Open | 47d1edc |
| 2026-05-17 | changelog/index.html static-mirror regen | — | — | meta-route mirror drift after CHANGELOG.md edits in 5d14cde + 47d1edc | 360eb74 |
| 2026-05-17 | Meta-route static-mirror freshness CI guard | — | JA-113 | (no drift this commit — JA-113 wired prospectively to prevent recurrence of the meta-route mirror drift class observed 3× this session) | 481e9ad |
| 2026-05-17 | 2 untracked files resolved | — | — | n5-008.pdf gitignored; build_test_scenarios_workbook.py moved to not-required/tools-archive/ with DEPRECATED guard | 407ef64 |
| 2026-05-17 | JA-114 (pacing_status enum) + JA-115 (README counts) | — | JA-114, JA-115 | README "1041 vocab / 40 reading / 40 listening" → 995 / 54 / 50 (stale v1.12.29-era counts caught by JA-115's first run) | c1c7107 |
| 2026-05-17 | INV-6 promotion + INV-7 extension + INV-9 promotion | INV-6 → Wired, INV-7 → Wired, INV-9 → Wired | JA-116, JA-117, JA-118 | A5 missing scenario row (substring-match bug in b466293 sync — `"A5" in "A55"` was True); 53 Fixed bugs back-filled with Fix Commit links | bbea337 |
| 2026-05-17 | Final batch — JA-91..95 partial promotion + INV-1/2/8 commit-time hooks + Audio Phase-2 maintainer doc | INV-1/2/8 → Convention+Hook | JA-92, JA-93, JA-95 (JA-91 + JA-94 stay reserved with gating notes) | n5-028 ex[5] ja `父は 先生です。` → `わたしの 父は 先生です。` (JA-95 first-run caught the possessive-の omission) | 9c5efa7 |
| 2026-05-17 | BUG-050 round-3 close-out — spec §7.3 sample version.json drift | INV-4 fifth-surface coverage | JA-119 | Spec §7.3 sample carried v1.12.50-era values (vocab 1041, reading 45, listening 47, papers 29, paperQuestions 426, invariants 48/48) — auditor read this as authoritative current state and re-filed BUG-050 three times against the actual file. Sample updated to current values; JA-119 locks future drift. | (this commit) |
| 2026-05-17 | Audio Phase-1.5 — rubberband replaces chained atempo on 3 listening items | — | — | 3 items (n5.listen.041/044/045) rubberband-processed from pre-47d1edc source at factors 0.476–0.487; replaces 2-pass `atempo=0.5,atempo=X` chain with single-pass librubberband; audio_render_meta.post_render_tempo_method flipped to "ffmpeg-rubberband"; AUDIO-PHASE2-VOICEVOX-RERENDER.md "7 items below 0.5 factor" → "3 items" (hand-tally drift fix); CHANGELOG entry + Part 20 addendum + audit-log row. CI 122/122 green. | c79c02e |
| 2026-05-17 | Audio Phase-2 — VOICEVOX re-render at speed_scale=1.00 (full 50-item from-source render) | — | — | Replaced 2026-05-12 render at 0.95 + Phase-1 atempo (47d1edc) + Phase-1.5 rubberband (c79c02e) with from-source VOICEVOX render at speed_scale=1.00. 50/50 items re-rendered via `tools/render_listening_phase2_voicevox_1_00_2026_05_17.py` (~12 min wall-clock; 6 distinct speakers preserved). Post-render pacing pass via `refresh_listening_pacing_2026_05_17.py --apply-speedup`: 16 items needed no adjustment, 29 needed single-pass atempo, 5 needed chained atempo (factor < 0.5). The 5 chained-atempo items (n5.listen.010/041/044/045/047) had their atempo replaced with single-pass librubberband via `tools/apply_phase2_rubberband_chained_items_2026_05_17.py`. Final: 50/50 in_range, mean 214.5 mpm (target 180-240). AUDIO-PHASE2-VOICEVOX-RERENDER.md rewritten from runbook to COMPLETED state. CHANGELOG entry + AUDIT-COVERAGE Part 22 + this audit-log row. CI 122/122 green. | (this commit) |
| 2026-05-17 | JA-91 + JA-94 Phase A + Phase B resolution — empty both baselines | — | — | Phase A: 14 BUG-006-CANDIDATE wrong-example replacements (n5-030 ×3 / n5-048 ×3 / n5-065 ×1 / n5-071 ×1 / n5-084 ×1 / n5-112 ×1 / n5-157 ×3 / n5-164 ×1) — each authored to demonstrate the parent pattern's canonical structure; `data/_ja94_baseline.json` emptied. Phase B: 33 explanation_en rewrites covering all 43 prior JA-91 pairs (DUPLICATE_PATTERN ×8 / CROSS_REFERENCE ×21 / ALTERNATIVE_VARIANT ×12 / SUBSET ×2); deferring sides rewritten so similarity falls below 0.85; ALTERNATIVE_VARIANT pairs got register-distinguishing rewrites on BOTH sides; `data/_ja91_baseline.json` emptied. Verified: no NEW pairs crossed 0.85 from the rewrites. CI 122/122 green; both invariants now run with empty baselines. Spec §25.4 JA-91 + JA-94 rows updated to RESOLVED; §25.7 deferred block updated; §25 intro counts unchanged. Phase-0 regression block in N5Improvement.txt updated to target 0/0 (was 43/14). | (this commit) |
| 2026-05-17 | JA-91 + JA-94 final unblock (last two reserved JA-91..95 slots) | — | JA-91, JA-94 | `data/_ja91_baseline.json` authored (43-pair classification: DUPLICATE_PATTERN ×8 / CROSS_REFERENCE ×21 / ALTERNATIVE_VARIANT ×12 / SUBSET ×2); `data/pattern_markers.json` authored via `tools/author_pattern_markers_2026_05_17.py` (178-pattern structural-markers catalog, 99.2% coverage of 1782 examples); `data/_ja94_baseline.json` snapshots the 14 BUG-006-CANDIDATE wrong-example failures with per-entry classification notes. JA-91 + JA-94 now PASS on the current corpus and trip on any NEW pair / NEW pattern-instance contamination. Removed duplicate pre-baseline `_check_ja_91_explanation_similarity()` definition. Spec §25.7 reserved list trimmed to JA-42..46 + JA-80; §25.4 gains JA-91 + JA-94 rows; §25.9 step-3 reserved-slot note updated. | (this commit) |

Each future cross-artifact ripple gets a row here so future
auditors can trace which sync hops landed when.

---

*Doc owner: project author. Update this map whenever a new
artifact class enters scope or an INV-N invariant changes
status. Cross-ref: parent `JLPTSuccess/.claude/CLAUDE.md` →
Rule 5 (governance) + `N5/.claude/CLAUDE.md` → Documentation
propagation section.*
