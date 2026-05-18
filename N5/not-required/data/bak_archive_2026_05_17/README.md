# data/*.bak* archive — moved 2026-05-17

Contains 89 backup files moved from `N5/data/` on 2026-05-17 per
the user's explicit instruction to clean the active data folder.

## What's in here

| File pattern | Count | What it backs up |
|---|---|---|
| `grammar.json.bak_2026_05_13_*` | 13 | Pre-/post-audit snapshots of grammar.json during the 2026-05-13 audit round |
| `grammar.json.bak_2026_05_15_*` / `_2026_05_16_*` / `_2026_05_17_*` | 9 | BUG-class close-out snapshots |
| `vocab.json.bak_2026_05_12_*` thru `_2026_05_17_*` | 17 | Vocab corpus snapshots across all close-out batches |
| `kanji.json.bak_2026_05_12_*` thru `_2026_05_17_*` | 14 | Kanji corpus snapshots |
| `listening.json.bak_2026_05_12_*` thru `_2026_05_16_*` | 8 | Listening corpus snapshots (incl. pre-VOICEVOX migration) |
| `reading.json.bak_2026_05_12_*` thru `_2026_05_17_*` | 10 | Reading corpus snapshots |
| `questions.json.bak_2026_05_15_*` thru `_2026_05_16_*` | 4 | Questions corpus snapshots |
| `authentic.json.bak_2026_05_12_*` thru `_2026_05_16_*` | 5 | Authentic content snapshots |
| `drills_auto.json.bak_2026_05_16_*` | 2 | Drill-generation snapshots |
| `audio_manifest.json.bak_2026_05_12_pre_voicevox` | 1 | Pre-VOICEVOX audio manifest |

**Total: 89 backup files; 136 MB on disk.**

## Why they were kept (before this move)

Per the BINDING backup policy in
`JLPTSuccess/.claude/CLAUDE.md` / `N5/.claude/CLAUDE.md`:

> Never delete an older backup version. Once written, backup files
> stay until the user explicitly says to clean them up.

## Why they were moved out of `data/` (now)

The user explicitly authorized cleanup on 2026-05-17 with:

> "clean this folder: ...N5\data. move not required files to not
> required folder"

This move is **non-destructive** — files are preserved at
`not-required/data/bak_archive_2026_05_17/`, not deleted. Any
future maintainer needing to recover a specific snapshot can
restore the file from this archive.

## CI / runtime impact

**Zero impact.** No tool / code / test references any
`*.bak*` file. Confirmed by:

- `tools/check_content_integrity.py` PASS 122/122 post-move
- `tools/cross_artifact_sync_report.py` EXIT: CLEAN post-move
- No JS / Python code in the repo greps for `.bak` paths
  (only the backup-policy doc text mentions them)

## Recovery procedure

If a specific backup is needed:

```bash
cp "N5/not-required/data/bak_archive_2026_05_17/grammar.json.bak_2026_05_13_run3" \
   "N5/data/grammar.json.bak_2026_05_13_run3"
# or to actually restore:
cp "N5/not-required/data/bak_archive_2026_05_17/grammar.json.bak_2026_05_13_run3" \
   "N5/data/grammar.json"
```

## Future cleanup

If the archive gets too large in future sessions:

- Per-month aggregation: zip older months into `bak_archive_2026_05_pre_consolidation.tar.gz`
- Selective deletion: only after user re-authorizes per BINDING
  backup policy
- Move to off-repo storage: e.g., a separate `jlpt-backups`
  repo or S3 bucket

Until then, keep this archive in-repo for fast `git log`-style
forensics on data drift.
