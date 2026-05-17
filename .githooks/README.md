# Git hooks — commit-time INV-1 / INV-2 / INV-8 enforcement

This directory carries the Cross-Artifact Sync Protocol's
commit-time enforcement (Rule 5 in `JLPTSuccess/.claude/CLAUDE.md`).
The hooks complement the corpus-content CI invariants
(`tools/check_content_integrity.py` — JA-1..JA-118) by catching
issues at commit time rather than after-the-fact in CI.

## One-time install

```bash
git config core.hooksPath .githooks
```

After this, every `git commit` runs the hooks below automatically.

## What each hook does

### `pre-commit` (runs on staged files)

- **INV-1 (bug-fix touches test):** if any staged file path mentions
  `BUG-NNN` or fix-script naming patterns, surface as warning if no
  test / CI / regression signal is also staged.
- **INV-2 (spec change references code):** if `N5/specifications/*.md`
  is staged but no code/data file is, warn — possibly a doc-only
  change (legitimate), possibly a spec change that needs
  corresponding code (caught early).
- **INV-8 (CHANGELOG completeness, file-side):** if `N5/data/*.json`
  is staged but `N5/CHANGELOG.md` is not, warn — most data changes
  are user-visible and need a CHANGELOG entry; exceptions are
  internal-only / backup / regen changes which should say so in the
  commit message.

### `commit-msg` (runs on the prepared commit message)

- **INV-1 (bug-fix touches test, message-side):** if the commit
  subject mentions `BUG-NNN` or `fix(bugs)`, the message body must
  reference a test, regression check, JA-NN invariant, Phase-0
  block, or carry an explicit `no test — reason: ...` annotation.
  Otherwise **the commit is rejected**.
- **INV-8 (atomic-commit discipline):** if the commit touches ≥4
  files and the message body is short (<6 non-blank lines), warn
  — Rule-5 atomic-commits should name every dependent updated.

## Bypass

If a check fires incorrectly (rare), bypass with:

```bash
git commit --no-verify -m "..."
```

Use sparingly — the hooks exist because the failure modes they
guard against (a bug closed with no test; a multi-file commit
that hides what was touched) are real and were observed in the
project's history.

## Local-only (not enforced on CI)

These hooks run on the maintainer's machine at commit time. They
are NOT a substitute for the corpus-content CI invariants in
`tools/check_content_integrity.py`, which run on every push +
PR via `N5/.github/workflows/content-integrity.yml`. The
sync-report tool `tools/cross_artifact_sync_report.py` rolls up
both views (CI invariants + commit-time discipline) into the
end-of-batch status output.

## When to update these hooks

Add a new check here when:
- A drift class is caught in code review or via CI but would be
  cheaper to catch at commit time (parallel to the meta-route
  mirror drift that motivated JA-113 — three instances in one
  session before the invariant was wired).
- The protocol's INV-N catalog gets a new entry.

Coordinate hook updates with the corresponding INV-N status in
`N5/docs/cross-artifact-sync-map.md`'s "Sync invariants" table.
