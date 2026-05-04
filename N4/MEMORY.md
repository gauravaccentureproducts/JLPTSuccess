# JLPT N4 Tutor — Memory

Last refreshed: 2026-05-04 (Pass-3 priorities complete; v0.2.0 — ALL 41 invariants PASS). Keep under 200 lines.

## Project location

- Root: `C:\Users\gaurav.l.srivastava\Documents\VS Code\JLPT\N4\`
- Source: vanilla HTML / ES modules / CSS, no build step for runtime
- Tests: `tests-e2e/` (Playwright smoke + a11y)
- Branch: `main` (no remote configured yet — first deploy will configure)
- HEAD: `b1de2c3` (latest [build-step 9/15] UI N4 wiring)

## Sibling repos (level-agnostic context)

- `<JLPT-root>/N5/` — source repo for architectural inheritance.
- `<JLPT-root>/N3/`, `N2/`, `N1/` — not yet created.
- `<JLPT-root>/procedure-manual-build-next-jlpt-level.md` — level-agnostic playbook.

## Key files

- `procedure-manual-build-next-jlpt-level.N4.md` — **the spec.** Single source of truth for what this app must do.
- `README.md` — quick orientation.
- `CHANGELOG.md` — release history.
- `TASKS.md` — Pass-1/Pass-2/Pass-3 backlog.
- `index.html`, `sw.js`, `manifest.webmanifest` — static PWA shell.
- `js/app.js` — entry; router + skeleton renderer.
- `js/home.js`, `js/learn.js`, `js/test.js`, `js/drill.js`, `js/review.js`, `js/settings.js` — main route handlers.
- `js/storage.js` — LocalStorage wrappers + SM-2 SRS math.
- `css/main.css` — Zen Modern design system.
- `tools/build_data.py` — KB markdown → data/*.json. Most-important script.
- `tools/check_content_integrity.py` — 33-invariant CI gate.
- `KnowledgeBank/*.md` — source-of-truth content (markdown). All currently skeleton.
- `data/*.json` — runtime data (regenerated). All currently skeleton with `_meta` populated.

## Current state (2026-05-04, v0.1.0)

- **Pass-2 complete; ALL 41 invariants PASS.**
- All token substitutions applied (`n5` → `n4`, `JLPT N5` → `JLPT N4`, brand `五` → `四`).
- Build-progress checkpoint: `.build-progress.json` (steps 1-9 + 14-15 complete; 10-13 deferred).
- Integrity check: **41/41 invariants PASS**.
- Builders authored:
  - `tools/build_n4_kanji.py` → 249 glyphs (106 N5 prereq + 143 N4 new)
  - `tools/build_n4_vocab.py` → 1159 entries (1041 N5 prereq + 118 N4 from sample)
  - `tools/build_n4_grammar.py` → 307 patterns (178 N5 prereq + 129 N4 from inventory)
  - `tools/build_n4_questions.py` → 591 questions across 5 banks
- Listening/Audio: empty stubs, deferred to Pass-3.

## Pending / next up

1. **Pass-3 Layer 4** — Full Tanos N4 vocab fetch (~600 entries; current 118 is a-h sample).
2. **Pass-3 Layer 7** — Question banks (591 questions; JA-8 release blocker).
3. **Pass-3 Layer 6** — Reading + listening corpora (~30 each).
4. **Pass-3 Layer 5** — Grammar enrichment (form_rules, examples, common_mistakes per pattern).
5. **Pass-3 Layer 3** — Kanji per-glyph examples drawn from full vocab.
6. **Pass-3 Layer 8** — LLM audit, coverage compare, browser smoke test, deploy.

See `TASKS.md` for the full Pass-3 backlog.

## Permission posture

- `.claude/settings.local.json` carries `defaultMode: bypassPermissions` + broad allow rules + destructive-op deny list. Inherited from N5.
- For autonomous operation: launch Claude Code with `--dangerously-skip-permissions`.
- Deny list still gates: `git push --force`, `rm -rf`, `git reset --hard`, `git branch -D`, etc.

## Workflow (per `.claude/CLAUDE.md`)

1. Edit `KnowledgeBank/*.md` (source of truth — never edit `data/*.json` directly).
2. Run `python tools/build_data.py` to regenerate JSON.
3. Run `python tools/check_content_integrity.py` — must exit 0.
4. Commit. Push.
5. CI re-runs integrity check; deploys to GitHub Pages on green.

## Critical gotchas

- **PoS by section is anti-pattern AP-1.** Tag PoS per WORD, not per thematic section. Group-2 verbs in section 30 (Existence/Possession) must NOT inherit `verb-1` default.
- **Cross-reference hygiene:** any pattern-retirement pass must repoint `contrasts.with_pattern_id` and `form_rules.conjugations.label "See n4-XXX"` references. JA-32 catches.
- **Mid-line clipping on tile cards:** `flex: 1` + `display: -webkit-box` + `-webkit-line-clamp: N` + fixed parent height = mid-line crop. Use `max-height: Nlh` + remove `flex: 1` + `margin-top: auto` on action element.
- **Stale module state on URL nav:** reset `view='finished'/'results'` when URL navigates away. Mid-attempt state preserves on refresh.
- **Cache-bust contract:** bumping `CACHE_VERSION` in `sw.js` is necessary but not sufficient — `index.html` must also bump `?v=N` on the entry script. ES modules are cached by URL.
- **iOS auto-zoom:** all inputs need `font-size: 16px` minimum at `≤768px`.

## Decisions made (per spec §39.2 / §0.A.2 defaults)

| Decision | Choice | Rationale |
|---|---|---|
| Audio source | Synthetic gtts | Native re-record deferred to v2 (EB-1). |
| Native review | LLM-only via `tools/llm_audit.py` | Native sign-off deferred to v2 (EB-2). |
| Translation | English-only | EB-3. |
| Monetisation | Free, no telemetry | Hard constraint. |
| SRS algorithm | SM-2 | FSRS-4 deferred to v2 (EB-4). |
| Handwriting practice | Defer | v2. |
| IME-typing input | Defer (kana-strict v1) | v2. |
| Reading speed test | Defer | v2. |
| Mock test timing | JLPT.jp official N4 (125 min: 30/60/35) | Per spec §A.9. |

## GitHub Pages deployment notes

- Target repo: `jlpt-n4-tutor`.
- Live URL: `<org>.github.io/jlpt-n4-tutor/`.
- Base path: `/jlpt-n4-tutor/`.
- All asset paths relative.
- Hash routing only (`#/...`).
- `404.html` fallback redirects to `./`.
- Workflow at `.github/workflows/pages-build.yml`.

## What this session did (continuation)

Pass-2 seed-corpus build (autonomous, steps 3-9 of the §39 build pipeline):

1. **Kanji whitelist [build-step 3]** — built 249-glyph whitelist from inventory + N5 prereq via `tools/build_n4_kanji.py`. Backfilled meanings/examples/notes from N5 source for prerequisite tier. JA-12 PASS.
2. **Kanji catalogue [build-step 4]** — KnowledgeBank/kanji_n4.md format-aligned to JA-12 (`- **{kanji}** ...`). Per-glyph examples deferred.
3. **Vocab seed [build-step 5]** — built 1159 entries via `tools/build_n4_vocab.py`. Suru-noun handling: each "Noun (suru-verb)" generates [n.] + [v3] entries (per N5 convention; JA-31 PASS). Em-dashes stripped (X-6.5). Group-1-exception flags inherited via N5 KB inlining (X-6.6 PASS).
4. **Grammar catalogue [build-step 6]** — built 307 patterns via `tools/build_n4_grammar.py`. Heuristic 18-category mapping. 4 meta-topics dropped, 6 patterns kana-folded for out-of-scope kanji.
5. **UI N4 wiring [build-step 9]** — fixed N5 leftovers in 5 JS files (feedback placeholder, home pillar desc, learn page lede, settings export filename, summary regex). Extended `GRAMMAR_SUPERCATS` with 18 N4 categories.

## Next session start

Read `TASKS.md` for the Pass-3 backlog. The recommended next action is **Pass-3 Layer 4** (full Tanos N4 vocab fetch from `tanos.co.uk/jlpt/jlpt4/vocab/`) followed by **Pass-3 Layer 7** (question banks) which is the JA-8 release blocker.

## Build infrastructure ready

- `tools/build_n4_kanji.py` — re-runnable, idempotent
- `tools/build_n4_vocab.py` — re-runnable, idempotent
- `tools/build_n4_grammar.py` — re-runnable, idempotent
- `tools/check_content_integrity.py` — 41 invariants, 35 PASS, 6 FAIL on JA-8 (expected)
- `.build-progress.json` — checkpoint at step 9; resume from step 7 (Reading+Listening) or jump to step 14 (finalisation) per priorities
