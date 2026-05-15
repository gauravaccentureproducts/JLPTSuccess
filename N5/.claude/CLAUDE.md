# JLPT N5 Tutor - Project Instructions

## Permission posture for this project (BINDING)

**The user has explicitly granted blanket autonomous-operation authorization for this repo.** This overrides the default "ask before pushing code / before shared-state actions" guidance from the global system prompt. Inside this repository tree, proceed without confirmation prompts for any of the actions below - including **compound commands** (`cd ... && git push ...`), commands with **stderr redirects** (`2>&1`), and commands **piped to other tools** (`| tail`, `| head`, `| grep`).

The user has explicitly authorized the following classes of action **without per-call confirmation prompts** for this repository:

- **All file edits and writes** in this project tree, including:
  - `.github/workflows/*.yml` - CI workflow files
  - `.claude/*` - Claude config
  - `data/*`, `docs/*`, `tools/*`, `specifications/*`, `feedback/*`, `js/*`, `css/*`, `locales/*` - all project content (the former `KnowledgeBank/` directory was merged into `data/` + `docs/N5-syllabus-methodology.md` on 2026-05-14 as a single source of truth)
- **Git push to remote** (`git push origin main`, `git push origin HEAD`, `git push origin <branch>`) - proceed without asking
- **Git commit** - including `git commit -m "msg"` AND heredoc-style `git commit -m "$(cat <<'EOF' ... EOF)"` AND batched `git add ... && git commit -m ... && git push ...` chains - proceed without asking
- **Git add / status / diff / log / show** - including all `cd "..." && git <cmd>` compound forms - proceed without asking
- **Git fetch / pull / branch / tag / merge / rebase** - proceed without asking
- **Standard `gh` PR / release / issue / workflow / run commands** - proceed without asking
- **Package installs in this project** (`npm install`, `pip install`) - proceed without asking

These are listed in `.claude/settings.local.json`. The user has stated they don't want repeated permission prompts for routine git workflow.

## Still requires confirmation (do NOT auto-run)

- **`git push --force`, `git push -f`, `git push --force-with-lease`** - destructive; warrants explicit confirmation
- **`git push --no-verify`** - bypasses hooks; warn before running
- **`git reset --hard`, `rm -rf`** - explicitly denied in settings; if the user asks, propose a safer alternative first
- **Any push to branches other than the user's working branch** - confirm target branch first

## Backup policy (BINDING — set 2026-05-10)

`git checkout -- <file>` and similar revert operations are now allowed without prompts. In exchange, the user has granted commit/upload rights but **NOT** file-replace/delete rights without explicit instruction. Concretely:

1. **Never overwrite an existing backup file.** If a backup at the target path already exists (e.g. `data/grammar.json.bak`), create a new versioned name (`data/grammar.json.bak_2026_05_10_v2`, then `_v3`, etc.) — do NOT replace v1.
2. **Never delete an older backup version.** Once written, backup files stay until the user explicitly says to clean them up. If you see `*.bak`, `*.bak_*`, `*.backup`, `*_backup_*` files, treat them as read-only.
3. **Before any destructive op** (`git checkout -- <file>`, overwrite-via-Write, `mv` over an existing file), check for and create a versioned backup if one doesn't already exist for this revision.
4. **Replacing or deleting any file the user did not ask you to touch** still requires asking first — even non-backup files. The blanket "don't replace/delete without telling me" rule applies broadly.

Settings enforcement: `**/*.bak*`, `**/*.backup*`, `**/*_backup_*`, `**/backups/**` are denied for `Write`, `Edit`, `Bash(rm/mv/cp ...)` and `PowerShell(Remove-Item/Move-Item/Copy-Item ...)`. If a deny rule fires when you needed to act, explain the situation to the user and ask — don't try to work around the deny.

## Documentation propagation (BINDING — set 2026-05-15)

**Whenever an audit cycle, fix batch, methodology change, new CI invariant, or new false-positive class is produced, you MUST update — without being asked, as part of the same commit:**

1. `JLPT Common/procedure-manual-build-next-jlpt-level.md` (cross-level build manual; lives in its own git repo)
2. `N5/prompts/Japanese language Accuracy check.txt` (audit categories + FP catalog)
3. `N5/prompts/N5Improvement.txt` (anti-items + Phase-0 regression blocks)
4. `N5/docs/AUDIT-COVERAGE-YYYY-MM-DD.md` (coverage matrix + future-review section)

See the parent `JLPTSuccess/.claude/CLAUDE.md` Rule 4 for the full specification, including the "ask yourself per-file" commit pattern and the mechanical-change exception.

## Commit workflow (BINDING — set 2026-05-11)

**Never** use inline heredoc commit messages (`git commit -m "$(cat <<'EOF' ... EOF)"`). Claude Code Desktop's permission gating treats those as new prompts every time even with matching glob rules and `defaultMode: "bypassPermissions"` — this has blocked overnight runs and is non-negotiable.

**Always** use the file-based commit pattern:

1. `Write` tool → `N5/.commit_msg.tmp` (multiline message OK; file is gitignored via `.commit_msg.tmp` line in `.gitignore` or created/removed transactionally)
2. `cd "<repo path>" && git add <files> && git commit -F .commit_msg.tmp && rm -f .commit_msg.tmp && git push origin master`

That single-line shape matches the existing allow rules in `settings.local.json` (line 30 explicit, plus `Bash(cd * && git * && git * && git * && git *)` covers it broadly). Empirically validated on Batches J/K/L/M/N — zero prompts, zero blocks.

If you find yourself reaching for `"$(cat <<'EOF'...` STOP. Use the file pattern.

## Working notes

- Repo backups have a known GH007 email-privacy block on `origin` for normal push; the project uses release-bundle workaround for backups (per MEMORY.md). Regular pushes to working branches are fine.
- Tests: `python tools/check_content_integrity.py` is the release-blocker CI check (21 invariants). Run it after any data/ or KB change.
- The 13 audit passes have produced ~185 content fixes; the JA-accuracy bar is high and CI-enforced.
