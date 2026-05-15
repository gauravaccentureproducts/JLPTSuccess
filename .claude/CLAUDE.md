# JLPTSuccess - Project Instructions for Claude

## Permission posture

The user has granted blanket autonomous-operation authorization for this repo. See `.claude/settings.local.json` for the per-tool allow / deny lists.

## BINDING governance rules (set 2026-05-04)

These rules override default helpful-assistant behavior. Read them at session start and before every action.

### Rule 1 - N4 IS WORK-BLOCKED

**Do NOT touch anything under `/N4/`.** Specifically:

- Do not edit any file inside `/N4/` (data, code, KB, audio, SVGs, tests, tools, configs, anything).
- Do not run any builder under `/N4/tools/` (`build_n4_*.py`, `enrich_*.py`, etc.).
- Do not commit changes that affect `/N4/`.
- Do not push changes that affect `/N4/`.
- Do not generate Playwright tests for, or run smoke tests against, `/N4/`.
- The N4 card is hidden from the JLPTSuccess homepage. Do not re-enable it.
- The N4 deploy at `/JLPTSuccess/N4/` continues to serve (legacy URL still works), but the **product is paused** - no further development, no further deploys touching that subtree.

**The block is lifted only when the user issues an explicit, unambiguous instruction like "unblock N4" or "resume N4 work."** Anything else - even a directly worded request to fix a specific N4 issue - should trigger Rule 2.

### Rule 2 - Finish one job before starting another

When the user asks for ANY new work, BEFORE starting:

1. Identify the current outstanding job (the most recently active task that is not yet complete).
2. Surface it back to the user explicitly: "Before I start <new request>, the current outstanding job is <X>. Should I finish that first, or pause it and switch?"
3. **Wait for an explicit re-confirm** ("yes do <new request>", "switch", "drop X and do <new request>") before starting the new work.
4. If the user says "finish X first" - finish X, then come back and ask again.

This applies even when the new request looks small or trivial. The user has explicitly requested this discipline; do not skip it to be more "helpful."

If there is no outstanding job (e.g., previous work was committed and pushed cleanly), proceed with the new request directly - no reminder needed in that case.

### Rule 3 - Keep N4 history intact

The /N4/ subtree is in the migrated state from 2026-05-04. Even though it's blocked from further work, the existing files are valid and tested. Do not delete or refactor them. If a tooling issue forces an N4 file edit (e.g., a security fix in shared dependencies), surface it to the user as an exception request rather than acting unilaterally.

### Rule 4 - Always propagate learnings to procedure manual + audit prompts (set 2026-05-15)

Whenever an audit cycle, fix batch, methodology change, new CI invariant, new false-positive class, or other generalizable learning is produced, the following docs MUST be updated **as part of the same commit** (or the immediately-following commit if grouping for cleanliness) — **without being asked**:

1. **`JLPT Common/procedure-manual-build-next-jlpt-level.md`** — the cross-level build manual (sits in its own git repo: `gauravaccentureproducts/JLPT-Common`, embedded as a submodule of JLPTSuccess). Add to the most recent Appendix (F as of 2026-05-15), or open a new Appendix when the learning class is significantly new. Capture: methodology, false-positive classes documented, CI invariants added, anti-patterns observed, sample/heuristic thresholds. Style: actionable for an Nx-level builder, NOT N5-narrative — abstract the lesson.

2. **`N5/prompts/Japanese language Accuracy check.txt`** — the audit prompt. Add new audit categories (A-numbered), new false-positive classes (FP-numbered), and update the closing block with the session-added CI invariants.

3. **`N5/prompts/N5Improvement.txt`** — the improvement prompt. Add new Section-10 anti-items + new Phase-0 regression-check blocks (validated to return 0 against the current corpus).

4. **`N5/docs/AUDIT-COVERAGE-YYYY-MM-DD.md`** — when the change is audit-related, update or append to the coverage matrix + the "future native-human review" section.

**This rule applies WITHOUT being asked.** Do not surface "should I update the manual?" as a question — just do it as part of the same commit. The user has set this discipline explicitly so methodology drift between code-state and documentation never happens. If you find yourself thinking "the user didn't ask for the manual update," that's the cue to do it anyway.

**Exception:** if the change is purely mechanical (renaming a file, fixing a typo, settings change) with no methodology implication, the doc update can be skipped — but flag it briefly in the commit message ("skipped doc update; mechanical change only").

**Practical commit pattern:** when wrapping up a substantive change, before writing the commit message, list the 4 doc files above and ask yourself per-file: "did this change produce a learning that belongs here?" If yes, edit it; if no, skip. The commit message should note which docs were updated.

## Operational notes

- Live URL: https://gauravaccentureproducts.github.io/JLPTSuccess/
- Default branch: `master`
- Repo: `gauravaccentureproducts/JLPTSuccess`
- N5 is the only currently-active level.
- Pre-migration backups remain at `gauravaccentureproducts/jlpt-n5-tutor` and `…/jlpt-n4-tutor`. Do not push to those.
