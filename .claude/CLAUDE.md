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

## Operational notes

- Live URL: https://gauravaccentureproducts.github.io/JLPTSuccess/
- Default branch: `master`
- Repo: `gauravaccentureproducts/JLPTSuccess`
- N5 is the only currently-active level.
- Pre-migration backups remain at `gauravaccentureproducts/jlpt-n5-tutor` and `…/jlpt-n4-tutor`. Do not push to those.
