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

| 2026-05-17 | Native Japanese teacher review batch 1 (NR-001..005) | — | — | 5 native-teacher findings: NR-001 まえに pattern-instance contamination (5 examples); NR-002 n5-161 duplicate examples; NR-003 n5-160/163 misfiled adverbial; NR-004 wh+は anti-pattern; NR-005 13 wrong rendaku forms. 9 grammar examples + 13 vocab collocations fixed. Cross-checked vs Genki I + Minna I + NHK accent dictionary + JEES samples. | d26e677 |
| 2026-05-17 | Native Hindi teacher + JLPT exam expert review batch 2 (NR-HI-001..003 + NR-JE-001) | — | — | 4 specialist findings: NR-HI-001 q-0264 corrupted Hindi distractor; NR-HI-002 q-0462 English possessive 's; NR-HI-003 q-0234 mixed-English; NR-JE-001 40 JLPT format violations (half-width ___). 3 Hindi explanations + 40 stem-format patches. Cross-checked vs Hindi Vyakaran + Sahitya Akademi register + JEES format. | 8159b49 |
| 2026-05-17 | Full specialist-sweep review batch 3 (NR-SEC-001/002 + NR-LIC-001 + NR-DATA-001) | — | — | 4 specialist findings: NR-SEC-001 4/4 workflows missing permissions: block; NR-SEC-002 defense-in-depth meta tags missing (later partly retired per NR-UI-001); NR-LIC-001 kanjium attribution missing from CONTENT-LICENSE.md; NR-DATA-001 14/22 data files lack schema_version (informational). 4 workflow YAMLs + 3 index.html meta tags + CONTENT-LICENSE.md updates. Cross-checked vs OpenSSF Scorecard + GDPR Art. 13 + DPDP + CC-BY-SA 4.0. 175 prior scenarios stamped across 11 tabs (D/E/F/G/H/I/J/K/L/M/N). | 46be3e1 |
| 2026-05-17 | Brutal-honesty re-audit batch 4 (NR-DATA-002) | — | — | 1 finding caught by deeper-scan that 30-sample passes missed: NR-DATA-002 4 vocab demonstrative entries reference retired pattern n5-012 (grammar.json skips n5-011 → n5-013). 4 vocab entries scrubbed. 42 prior PASSes re-labeled with bounded-honest qualifiers (PASS / PASS-limited / PASS-architectural / PASS-spot-check / etc.) for honest ground-truth. | d1e0d90 |
| 2026-05-17 | Selenium UI test class batch 5 (NR-UI-001) + NEW "UI Tests" xlsx tab | — | — | 55-scenario E2E UI test suite via Selenium 4 (auto-driver) covering every spec §5 functional route + static-mirror + a11y + security headers + Service Worker + audio + i18n + console health. NR-UI-001 surfaced: CSP `frame-ancestors` and X-Frame-Options are HTTP-header-only — IGNORED via <meta>; cosmetic-only fix. Removed both meta tags from index.html with documented static-hosting limitation. Post-fix: 53/55 PASS, 1 SKIP, 0 FAIL; 0 SEVERE console errors. NEW xlsx tab "UI Tests" (18 total tabs now). | 5635425 |
| 2026-05-17 | Cross-artifact propagation catch-up | — | — | Procedure manual F.28 (multi-role specialist-review methodology + bounded-honest stamping vocabulary) + F.29 (Selenium UI test class + NR-UI-001 lesson). Accuracy prompt A65 (multi-role methodology) + A66 (Selenium UI test class). N5Improvement.txt Phase-0 Selenium UI test regression block + Phase-0 multi-role specialist-review regression block. AUDIT-COVERAGE Part 23 (consolidated batch narrative). Sync-map this row + 5 prior batch rows. CHANGELOG Unreleased entry. Spec §25 intro reflection. | 063d6cd |
| 2026-05-17 | data/ folder cleanup — 89 *.bak files archived to not-required/ per explicit user authorization | — | — | Moved all 89 backup files from N5/data/ (grammar.json.bak_* / vocab.json.bak_* / kanji.json.bak_* / listening.json.bak_* / reading.json.bak_* / questions.json.bak_* / authentic.json.bak_* / drills_auto.json.bak_* / audio_manifest.json.bak_*) to N5/not-required/data/bak_archive_2026_05_17/ (~136 MB). 28 active files remain in data/; all 28 verified as runtime-referenced by js/* + tools/* + docs/* (0 orphans). Archive carries a README explaining recovery procedure. CI 122/122 PASS post-move; sync-report CLEAN. Non-destructive — files preserved at the archive path. | 9c051d5 |
| 2026-05-18 | PAPER-001..004 + LISTEN-4 close-out — 5 paper-question bug-class fixes + 3 new CI invariants | data → bug tracker, prompts, procedure manual, audit-coverage, CHANGELOG, spec | INV-1 (data shape), INV-3 (rationale text), INV-7 (cross-ref grammarPatternId → grammar.json), INV-10 (procedure manual + prompts → script refs) | PAPER-001: re-tagged 58 bunpou questions whose `grammarPatternId` was wrong (29 Mondai 1 particle re-tags + 14 non-particle re-tags + 7 Mondai 3 + 2 Mondai 2 + 1 missing-field for bunpou-4.3 = PAPER-002). PAPER-003: stripped commit-message-style meta-fix history from 14 rationale fields (6 bunpou + 2 goi via JA-121 catch). PAPER-004: rewrote 58 rationale_hi fields with natural Hindi sourced from rationale_en (NOT from broken rationale_hi — anti-pattern documented at F.30.6). LISTEN-4: data already correct (counts 995/106/54/50, version v1.15.5); tracker status flipped. New CI invariants: JA-120 (grammarPatternId↔particle alignment, PAPER-001 guard), JA-121 (no meta-fix history in rationale, PAPER-003 guard), JA-122 (no English-pattern fragments in rationale_hi, PAPER-004 guard). CI now 125/125 PASS. Horizontal-scan across grammar/vocab/kanji/reading/listening/questions: 0 similar findings. Tooling: tools/fix_paper_bugs_2026_05_18.py + tools/fix_paper_bugs_part2_2026_05_18.py. Procedure manual F.30 (6 sub-sections incl. particle ↔ pattern_id canonical map + anti-pattern). Accuracy prompt A67/A68/A69. N5Improvement Phase-0 paper-question regression block. AUDIT-COVERAGE Part 24. CHANGELOG Unreleased entry. Spec §25 PAPER-001..004 close-out. Bug tracker 109/109 Fixed / 0 Open. | 7728348 |
| 2026-05-18 | LLM-001..005 + REG-001 close-out — 6 crawler-accessibility + register-conflation bugs + 5 new CI invariants | data + UI + code → bug tracker, prompts, procedure manual, audit-coverage, CHANGELOG, spec | INV-1 (data shape), INV-2 (UI surface), INV-4 (corpus count drift on new index.json), INV-7 (cross-ref every static mirror to a data entity), INV-10 (procedure manual + prompts → script refs) | LLM-001: added 28 paper static mirrors + 1 paper landing (papers/ tree). LLM-002: sitemap.xml regenerated 10→1589 URLs covering all 1370+ existing mirrors + 7 new summary pages + meta routes + paper mirrors. LLM-003: created data/index.json (39-entry corpus discovery catalog with size_bytes / mtime / item_count / description per file). LLM-004: expanded N5/index.html noscript with path-routed nav (no hash routes) + corrected stale counts (was 45/47 → 54/50). LLM-005: created 7 thin summary pages (home/grammar/vocabulary/kanji/reading/listening/test.html) + llms.txt at /JLPTSuccess/ root and /N5/ + updated root index.html with static-summary footer link + root robots.txt with sitemap reference. REG-001: migrated n5-046.wrong_corrected_pair[1] (やまださんは だれ ですか) to common_mistakes register_variant; JA-127 first-run caught 5 more D6-class entries (n5-097, n5-102, n5-127, n5-173, n5-179 — all "(in formal context)" self-contradiction class) — all migrated; SWEEP-1 candidate report at docs/REG-001-SWEEP-1-candidates_2026_05_18.md surfaces 84 entries for native-speaker triage (deferred as REG-002..NN). New CI invariants: JA-123 (papers mirror coverage), JA-124 (sitemap floor ≥1000), JA-125 (data/index.json byte-size drift guard), JA-126 (7 summary pages + llms.txt presence), JA-127 (REG-001 D6 self-contradiction guard). CI now 130/130 PASS. Tooling: tools/build_llm_surfaces_2026_05_18.py (8-stage) + tools/fix_reg_001_2026_05_18.py + tools/fix_reg_001_d6_migrations_2026_05_18.py. Procedure manual F.31 (8-surface LLM-accessibility canonical set) + F.32 (register-variant vs grammar-error 6 defect classes). Accuracy prompt A70/A71. N5Improvement Phase-0 LLM-surfaces + register-variant blocks. AUDIT-COVERAGE Part 25. Spec §25 LLM-001..005 + REG-001 close-out. Bug tracker 109/109 Fixed / 0 Open. | c55d7f6 |
| 2026-05-18 | DOKKAI-001..003 close-out — 3 paper schema-discipline bugs + 3 new CI invariants + horizontal sweep across all 4 paper categories | data (4 paper categories) → bug tracker, prompts, procedure manual, audit-coverage, CHANGELOG, spec | INV-1 (data shape), INV-3 (rationale text), INV-7 (passage_label → passages[].label foreign key), INV-10 (procedure manual + prompts → script refs) | DOKKAI-001: dropped passage_text from all 102 dokkai questions (single source of truth = passages[label].text); normalized 40 passages[].text by stripping leading "> " markdown-blockquote prefix; horizontal sweep caught bunpou/paper-7.json (10 Mondai-3 questions with stray passage_text but no passages[] block) — created 2-entry passages[] + dropped 10 passage_text fields. DOKKAI-002: rewrote dokkai-1.1 rationale_hi (untranslated "ago" → natural Hindi "पहले"); horizontal sweep caught goi-7.1 with the same English-fragment class — also rewritten. DOKKAI-003: filled 24 dokkai grammarPatternId=null + provenance="not_applicable_comprehension"; horizontal sweep filled 83 more non-dokkai (11 goi → "not_applicable_vocab", 72 moji → "not_applicable_orthography"). All 412 paper questions now have grammarPatternId as a guaranteed key (matches VOCAB-002 always-a-key pattern). New CI invariants: JA-128 (no passage_text on paper questions), JA-129 (no untranslated " ago"/" yet"/" lot" English temporal markers in rationale_hi — extends JA-122), JA-130 (grammarPatternId always-a-key with documented null provenance). CI now 133/133 PASS. Tooling: tools/fix_dokkai_bugs_2026_05_18.py + tools/fix_dokkai_bugs_horizontal_2026_05_18.py. Procedure manual F.33 (3 schema-discipline classes A/B/C + bounded-coverage phrasing). Accuracy prompt A72. N5Improvement Phase-0 dokkai-schema regression block. AUDIT-COVERAGE Part 26. Spec §25.4 JA-128..130 rows. Bug tracker 112/112 Fixed / 0 Open. | 0a957bc |
| 2026-05-19 | MOB-001..019 + DOKKAI-004 close-out — 20 mobile-UI compliance bugs + 4 new CI invariants + JA-129 trigger extension | CSS + JS + locale + data → bug tracker, prompts, procedure manual, audit-coverage, CHANGELOG, spec | INV-1 (data shape), INV-2 (UI surface), INV-3 (rationale text), INV-5 (locale parity), INV-7 (cross-file refs in router), INV-10 (procedure manual + prompts → script refs) | MOB-001: removed @media(max-width:599px) rule hiding Test+Progress nav items. MOB-002/003/004/005/011/012/013/014/015/016: consolidated mobile-UI compliance CSS block at end of main.css (+ minified mirror) — `min-height: 44px` on .btn-action, .study-order-link, .home-up-link a, .back-link, .toc-expand-all, .brand-link, .skip-link, .btn-tiny, authentic ref-chips, examday/weakareas inline links. MOB-006: site-wide `input,textarea,select { font-size: max(1rem, 16px); }` (iOS Safari auto-zoom guard). MOB-007: added nav.all_levels key to en+hi locales (`सभी JLPT स्तर`); home.js home-up link uses t('nav.all_levels'). MOB-008: js/listening-story.js canonicalized from `#/listening/story` to `#/listeningstory` (4 href edits). MOB-009: js/home.js home-up link `href="#/levels"` → `href="../"` (skip in-SPA redirect). MOB-010: declined as P5 design-decision. MOB-017: js/reading.js reading list `<button>` → `<a href>` deep-links (restores crawlability). MOB-018/019: scenario-rewrite recommendations documented (not app-code). DOKKAI-004: dokkai-4.1 rationale_hi `आना-जाना by ट्रेन` rewritten to natural Hindi; JA-129 trigger set extended with ` by ` family. New CI invariants: JA-131 (nav.all_levels locale parity), JA-132 (MOB-001..016 CSS compliance batch marker + canonical class set), JA-133 (form-input font-size>=16px), JA-134 (no dead-end hash routes #/levels / #/listening/story). CI now 137/137 PASS. Procedure manual F.34 (5 mobile-UI defect classes A-E). Accuracy prompt A73. N5Improvement Phase-0 mobile-UI block. AUDIT-COVERAGE Part 27. Spec §25.4 JA-131..134 rows. Bug tracker 129/129 Fixed / 0 Open. | 6f424dc |
| 2026-05-19 | Audit-artifact provenance + doc-drift fix + JA-135 + MOB-018 scenario split | code (audit tools) + docs (count fix) + CI invariant + xlsx scenario | INV-10 (procedure manual + script refs) | Committed 8 mobile-audit artifact files (run_mobile_ui_tests.py, register_mobile_bugs*.py, analyze_test_coverage.py, etc.) preserving provenance of the MOB-* audit run. Fixed doc-arithmetic drift (CHANGELOG + AUDIT-COVERAGE Part 27 said 132/132 — actual 129/129). Added JA-135 hash-route-resolution guard (extends JA-134 from 2 known patterns to "every #/X href in js/*.js resolves to app.js routes dict"). Updated Mobile UI tab Row 18 (O-X-014 Footer reach) with MOB-018 Auto/Manual split recommendation. MOB-019 noted as not-applicable (referenced O-S-a-* IDs are runner-internal, not xlsx scenarios). CI now 138/138 PASS. | 614930c |
| 2026-05-19 | GOI-001..003 close-out — 3 goi-paper-6 rationale-content bugs + 1 new CI invariant + JA-121 trigger extension | data → bug tracker, prompts, procedure manual, audit-coverage, CHANGELOG, spec | INV-1 (data shape), INV-3 (rationale text), INV-10 (procedure manual + prompts → script refs) | GOI-001: goi-6.11 rationale_hi was verbatim copy-paste of goi-6.12 (about 二十さい/age) on a phone-call stem — hard learner-facing breakage. Rewrote in natural Hindi about phone-call paraphrase. GOI-002: goi-6.14 rationale ended with "Hence the rewording from a prior version" — same anti-pattern as PAPER-003 / JA-121 with new trigger phrase. Trimmed to first sentence. GOI-003: goi-6.12 rationale ended with meta-doc pointer ("documented at vocabulary_n5.md ... does not bear on the test point") — replaced with direct pedagogical note (はたち on-yomi exception). New CI invariants: JA-136 (no rationale_hi shared verbatim by 2+ questions within same paper, GOI-001 copy-paste guard) + JA-121 trigger set extension (7 new phrases catching GOI-002/003 patterns). Rejected bug spec's stricter token-overlap invariant (~100 false positives on existing corpus). CI now 139/139 PASS. Procedure manual F.35 (2 rationale-content discipline classes). Accuracy prompt A74. N5Improvement Phase-0 rationale-content block. AUDIT-COVERAGE Part 28. Spec §25.4 JA-136 row. Bug tracker 132/132 Fixed / 0 Open. | 0343bf4 |
| 2026-05-19 | REG-001 SWEEP-1 native-Japanese-teacher triage (Tier 1) — 21 A migrations + 15 C recategorizations + 1 B-escape | data (grammar.json schema migration + category corrections) → audit-coverage, CHANGELOG, sync-map | INV-3 (rationale/categorization), INV-9 (closed-bug → fix-commit link) | Of 84 original SWEEP-1 candidates, 34 already-migrated in earlier batches; 50 triaged in this pass. A-class (21): wrong_corrected_pair → common_mistakes register_variant with form_a/form_b/label_a/label_b (n5-018, n5-042, n5-045, n5-048, n5-050, n5-054, n5-062, n5-071, n5-074, n5-075, n5-077, n5-125×2, n5-131, n5-132, n5-134, n5-151, n5-166, n5-173, n5-174, n5-176). C-class (15): error_category recategorized register → pragmatic (14) or cultural (1, n5-100[2] modesty norm). B-class (14): kept as wcp; 1 (n5-125[0]) recategorized to register_coherence to escape JA-127. SWEEP-5 (kana-form-of-whitelist-kanji) DECLINED: corpus convention check showed grammar.json examples strongly favor kana (わたし 14× vs 私 2×; ともだち 35× vs 友だち 14×); bug spec D5 claim conflicts with documented N5-pedagogy convention. Honest provenance: llm_curated_with_reference_genki_minna_jees_2026_05_19 on all A migrations (LLM-with-reference review, not actual native-speaker; flagged for future re-verification). CI 139/139 PASS (no new invariants — triage pass with data + categorization changes only). Tooling: tools/sweep1_triage_2026_05_19.py. AUDIT-COVERAGE Part 29. CHANGELOG entry. Bug tracker 132/132 Fixed / 0 Open. | 8c06567 |
| 2026-05-19 | Tier 2: SWEEP-4 OOS-keigo scope_note audit (clean) + JA-129 trigger extension (`before`/`then` added after 0-hit pre-deployment scan) | code (CI invariant trigger set) → audit-coverage, CHANGELOG, sync-map | INV-3 (rationale/text trigger sets) | SWEEP-4 scanned grammar.json examples + wrong_corrected_pair + common_mistakes for OOS keigo terms (どなた/なさる/いただく/ご覧になる/召し上がる/いらっしゃる/ございます/かしこまりました/存じる/申す/伺う/くださる/どちらから/いかが/おいくつ/ご遠慮ください) — 0 actionable items beyond what SWEEP-1 already covered. 54 register_variant entries from SWEEP-1 all carry label_b + scope_note; 28 discussion-field mentions documented at pattern level (n5-018/046/050/149/151/166 all have OOS terms in their pattern field). JA-129 trigger extension: pre-deployment scan of all paper + corpus rationale_hi for ` before ` / ` then ` (+ punctuated variants) in Devanagari context = 0 hits; safe to add to the JA-129 substring set alongside ` ago ` / ` yet ` / ` lot ` / ` by `. CI 139/139 PASS unchanged (trigger set update, not new invariant). AUDIT-COVERAGE Part 30. CHANGELOG entry. Bug tracker 132/132 Fixed / 0 Open. | 7059ba7 |
| 2026-05-19 | Tier 3: SWEEP-2 + SWEEP-3 audits (both clean) — REG-001 sweep series closed | docs only (no code or data changes) → audit-coverage, CHANGELOG, sync-map | INV-3 (rationale/categorization) | SWEEP-2 (D2 semantically-distinct forms as register-equivalents): 54 register_variant entries + 3 wcp multi-alternative `correct` candidates audited = 0 violations. The borderline n5-069[3] (てから vs 〜て) has accurate labels honestly noting "register / emphasis choice"; 3 wcp candidates (n5-024 coffee-or-tea, n5-051 nazeka, n5-152 thanks) all offer synonyms/syntactic variants, not semantically-distinct alternatives. SWEEP-3 (D3 formality vs elevation conflation): scanned register_variant labels = 0 violations. 1 trigger candidate (n5-097 どちら) was false positive — どちら is correctly labeled "polite / formal" (not over-claimed as 尊敬 elevation). REG-001 sweep series fully closed: SWEEP-1 done (Tier 1 commit 8c06567), SWEEP-2/3 clean (this commit), SWEEP-4 done (Tier 2 commit 7059ba7), SWEEP-5 declined-with-reason, SWEEP-6 closed in earlier batches via JA-127. CI 139/139 PASS unchanged (audit-only). AUDIT-COVERAGE Part 31. CHANGELOG entry. Bug tracker 132/132 Fixed / 0 Open. | 40700d6 |
| 2026-05-21 | 4-class batch closure of accumulated deferred items: codify-policy (SWEEP-5 orthography) + advisory-tool (rationale-overlap audit) + CI-workflow (LLM-surfaces drift detection) + path-forward-doc (native-speaker re-verification) | docs + code + workflow (no data changes) → procedure manual, audit-coverage, CHANGELOG, sync-map | INV-10 (procedure manual + script refs), INV-7 (CI workflow ↔ surfaces consistency) | Class A: ORTHOGRAPHY-POLICY-N5.md codifies per-word kana-vs-kanji convention (21 N5 high-freq words tabulated; わたし 14× vs 私 2×, ともだち 35× vs 友だち 14×, 人 25× vs ひと 6× etc.); SWEEP-5 closes-as-policy (was declined-with-reason). Class B: tools/audit_rationale_overlap_2026_05_21.py advisory tool with lightweight Japanese stemmer; 21% false-positive rate documented; not strict CI invariant. Class C: .github/workflows/regen-llm-surfaces.yml triggers on data/** push, re-runs build_llm_surfaces.py + build_static_mirrors.py --stages meta, asserts no drift; closes LLM-005 build-script-integration deferred. Class D: NATIVE-SPEAKER-RE-VERIFICATION.md documents 3 options + tracking signal + expected-outcome ranges for the 54 register_variant entries with llm_curated_with_reference_* / native_reviewed (undocumented depth) provenance; explicit acknowledgment of LLM limits. Procedure manual F.36 codifies the 4-class batch-closure pattern as reusable Nx-builder methodology. CI 139/139 PASS unchanged. Bug tracker 132/132 Fixed / 0 Open. | (this commit) |
| 2026-05-21 | GOI-004..006 close-out + horizontal mojibake sweep — 3 goi-paper rationale-content bugs + 2 new CI invariants (JA-137 + JA-139) + JA-121 trigger extension + 2 dokkai horizontal-deployment fixes | data → bug tracker, prompts, procedure manual, audit-coverage, CHANGELOG, spec | INV-1 (data shape), INV-3 (rationale text), INV-7 (CI invariant ↔ corpus pass), INV-10 (procedure manual + prompts → script refs) | GOI-004: off-by-one rationale_hi shift goi-7.6 → goi-7.7 (goi-7.6 carried goi-7.7's じょうずに 話す Hindi; goi-7.7 carried goi-7.8's しゅくだいを 出す Hindi). Rewrote both as natural Hindi about own stems. GOI-005: stripped fix-history from 7 rationale fields across goi-1.5/1.10/3.15/4.6/5.4/7.7/7.8 ("replaces the prior", "Strict-N5:", "in v1.X", "policy applied at", "previous version" + Hindi mirrors). GOI-006: mojibake 「あमारी ありません」 → 「あまく ありません」 in goi-7.4 rationale_hi (kana あ + Devanagari ma + Devanagari ī as a single word). **Horizontal-deployment sweep with JA-139 detector surfaced 2 MORE same-class mojibake in dokkai-2.11 (ぐらि → ぐらい) and dokkai-3.4 (あमारी → あまり)** — both fixed in this batch. New CI invariants: JA-137 (narrow off-by-one shift detector: 0 token overlap with own stem AND ≥2 overlap with next-Q stem; false-positive rate <1%, vs ~21% for broad token-overlap); JA-139 (no Devanagari letter embedded inside JP-character word in rationale_hi, excluding danda U+0964/U+0965 + hyphen-separated cross-script terms). JA-121 trigger set extended in place with 11 new phrases (no separate JA-NN minted — existing detector's intent already covered the class). Operational rule from F.37: every CI invariant runs corpus-wide BEFORE declaring class closed; horizontal-deployment is part of the fix commit, not a follow-up. CI now 141/141 PASS. Tooling: tools/fix_goi_004_006_2026_05_21.py + tools/fix_dokkai_mojibake_2026_05_21.py + tools/file_goi_004_006_bugs_2026_05_21.py + tools/flip_goi_004_006_fixed_2026_05_21.py. Procedure manual F.37 (3 drift classes A/B/C + horizontal-deployment operational rule + lineage table). Accuracy prompt A75 (7-invariant family on paper-question rationale fields documented). N5Improvement Phase-0 mixed-script + off-by-one + extended-fix-history regression block. AUDIT-COVERAGE Part 33. Spec §25.4 JA-137/JA-139 rows + count update. Bug tracker 135/135 Fixed / 0 Open. | (this commit) |

| 2026-05-22 | DOCS-VOCAB-005 close-out — paper-file source_file canonical sentinel + JA-145 + pre-existing drift fixes (A76/A77/A78 catalog gap + Phase-0 CI-recovery catalog gap + changelog mirror staleness) | data + code + prompts + audit-coverage + spec + procedure manual + xlsx + changelog mirror | INV-1 (data shape), INV-7 (CI invariant ↔ canonical sentinel), INV-10 (procedure manual + prompts → script refs) | DOCS-VOCAB-005 (BUG-136): trimmed 28 paper-file source_file values from "(authored in-place; was KnowledgeBank/<x>_questions_n5.md before merge on 2026-05-14)" to canonical sentinel "(authored in-place)". Bug-spec verification rejected the original proposed fix (replace with docs/N5-syllabus-methodology.md#bunpou-questions etc.) because (1) those anchors don't exist in the methodology doc, (2) the doc describes authoring methodology not question content, (3) replacing accurate "authored in-place" prose with a non-existent pointer is a regression not a fix. User chose Option 1 (shorten prose to literal sentinel). Closes the unaddressed half of DOCS-VOCAB-003 (which prematurely closed on 2026-05-21 as a README-only fix). New CI invariant JA-145: paper-file source_file must be either the literal sentinel OR a resolvable file path; other values fail. Bumped version.json v1.15.5 → v1.15.6 (corpus counts unchanged). Pre-existing drift fixed in same commit (Rule 5): tools/sync_test_scenarios_with_prompts_feedback_2026_05_17.py catalog gained A76 / A77 / A78 / A79 + P0-ci-recovery-triage + P0-source-file-sentinel entries (4 new xlsx scenario rows); changelog/index.html mirror regenerated via build_static_mirrors.py --stages meta to reflect 2026-05-21 CI-recovery Unreleased entry. CI 147/147 PASS (was 146; +JA-145). Tooling: tools/fix_docs_vocab_005_2026_05_22.py + tools/file_docs_vocab_005_bug_2026_05_22.py + tools/audit_docs_vocab_005_2026_05_22.py + tools/audit_paper_kb_refs_2026_05_22.py. Procedure manual F.41 (canonical-sentinel pattern + multi-case-bug close-out discipline). Accuracy prompt A79. N5Improvement Phase-0 source_file canonical-sentinel regression block. AUDIT-COVERAGE Part 37. Spec §25.4 JA-145 row + count update. Bug tracker 155/155 Fixed / 0 Open. | (this commit) |

Each future cross-artifact ripple gets a row here so future
auditors can trace which sync hops landed when.

---

*Doc owner: project author. Update this map whenever a new
artifact class enters scope or an INV-N invariant changes
status. Cross-ref: parent `JLPTSuccess/.claude/CLAUDE.md` →
Rule 5 (governance) + `N5/.claude/CLAUDE.md` → Documentation
propagation section.*
