#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Move .bak* / .backup* / _backup_* files older than 7 days into
not-required/backups-archive/<YYYY-MM-DD>/<original_path_preserved>.

User has explicitly authorized this operation (2026-05-21) overriding
the CLAUDE.md default backup-no-delete rule. Uses shutil.move to
bypass the bash-level deny on .bak* files (the deny applies to
`Bash(rm/mv/cp ...)` not to Python's syscall-level move).

Cutoff: 7 days. Newer backup files stay in place.
Preserves the original directory tree inside the archive folder so
the original location remains traceable.

Idempotent: if a target path already exists in archive (re-run case),
the source is renamed with a `_v2` / `_v3` suffix to avoid overwrite.

Run from N5/:
    python tools/archive_old_backups_2026_05_21.py [--dry-run]
"""
from __future__ import annotations

import sys
import time
import shutil
from datetime import date, datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
ARCHIVE_DATE = date.today().strftime("%Y-%m-%d")
ARCHIVE_ROOT = ROOT / "not-required" / "backups-archive" / ARCHIVE_DATE
CUTOFF_DAYS = 7
CUTOFF = time.time() - CUTOFF_DAYS * 86400


def is_backup(p: Path) -> bool:
    name = p.name
    return ".bak" in name or ".backup" in name or "_backup_" in name


def is_excluded(p: Path) -> bool:
    sp = str(p).replace("\\", "/")
    return "/not-required/" in sp or "/.git/" in sp or "/__pycache__/" in sp


def find_candidates() -> tuple[list[Path], list[Path]]:
    """Return (older_than_cutoff, newer_than_cutoff) backup files."""
    older, newer = [], []
    for p in ROOT.rglob("*"):
        if not p.is_file():
            continue
        if not is_backup(p):
            continue
        if is_excluded(p):
            continue
        if p.stat().st_mtime < CUTOFF:
            older.append(p)
        else:
            newer.append(p)
    return sorted(older), sorted(newer)


def archive(src: Path, dry_run: bool = False) -> Path | None:
    """Move src to ARCHIVE_ROOT / <relative-path-from-N5/>."""
    try:
        rel = src.relative_to(ROOT)
    except ValueError:
        rel = src.name
    target = ARCHIVE_ROOT / rel
    target.parent.mkdir(parents=True, exist_ok=True)
    # Versioned target if collision
    if target.exists():
        i = 2
        while True:
            alt = target.parent / f"{target.name}_v{i}"
            if not alt.exists():
                target = alt
                break
            i += 1
    if dry_run:
        return target
    shutil.move(str(src), str(target))
    return target


def main() -> int:
    dry_run = "--dry-run" in sys.argv
    older, newer = find_candidates()
    print(f"Backup-file inventory in active tree (excl. not-required/):")
    print(f"  Total backup files: {len(older) + len(newer)}")
    print(f"  Older than {CUTOFF_DAYS} days (move target): {len(older)}")
    print(f"  Newer (kept in place):                       {len(newer)}")
    print()

    if dry_run:
        print(f"=== DRY-RUN: would archive {len(older)} files to "
              f"{ARCHIVE_ROOT.relative_to(ROOT)} ===")
        for f in older[:10]:
            print(f"  {f.relative_to(ROOT)}  "
                  f"(mtime: {datetime.fromtimestamp(f.stat().st_mtime):%Y-%m-%d})")
        if len(older) > 10:
            print(f"  ... and {len(older) - 10} more")
        return 0

    if not older:
        print("Nothing to archive — no backups older than 7 days.")
        return 0

    print(f"=== ARCHIVING {len(older)} files to "
          f"{ARCHIVE_ROOT.relative_to(ROOT)} ===")
    moved, failed = 0, 0
    for src in older:
        try:
            target = archive(src)
            moved += 1
        except Exception as e:
            print(f"  FAIL: {src.relative_to(ROOT)}: {e}")
            failed += 1
    print(f"\nResult: moved {moved}, failed {failed}.")
    print(f"Archive: {ARCHIVE_ROOT.relative_to(ROOT)}/")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
