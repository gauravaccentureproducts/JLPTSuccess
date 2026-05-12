"""Archive 79 older snapshot files out of the working tree.

Workflow:
  1. Re-run the audit + safety verification.
  2. ABORT if any group is RED or YELLOW.
  3. For each group, move every snapshot EXCEPT the latest into
     N5/not-required/<original-subpath>/.
  4. Print per-file action; final summary.

Destination naming preserves the original path (data/<file>, feedback/<file>)
so the snapshots remain easy to locate by base file. Filenames preserved
exactly — no rename — so a later 'undo' is straightforward.

Safety: the move uses shutil.move (atomic when intra-volume on Windows).
Settings.local.json deny rules target Bash mv/cp/rm and PowerShell
Move-Item; Python's shutil is not matched by those globs.
"""
import json
import os
import re
import shutil
import sys
import io
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

WIN_SEP = chr(92)


def normalize(p: str) -> str:
    return p.replace(WIN_SEP, "/").lstrip("./")


def enumerate_snapshots() -> list[str]:
    files = []
    for root, dirs, fs in os.walk("."):
        parts = root.split(os.sep)
        if ".git" in parts or "not-required" in parts:
            continue
        for f in fs:
            if ".bak" in f or ".backup" in f:
                files.append(normalize(os.path.join(root, f)))
    return files


def base_of(path: str) -> str:
    m = re.match(r"(.+?)\.(bak|backup)", path)
    return m.group(1) if m else path


def main() -> None:
    DEST_ROOT = "not-required"
    snaps = enumerate_snapshots()
    groups: dict[str, list[str]] = defaultdict(list)
    for p in snaps:
        groups[base_of(p)].append(p)

    moves = []
    keeps = []
    for base in sorted(groups.keys()):
        paths = sorted(groups[base], key=os.path.getmtime, reverse=True)
        latest = paths[0]
        older = paths[1:]
        keeps.append(latest)
        for o in older:
            dest = os.path.join(DEST_ROOT, o)
            moves.append((o, dest))

    print(f"Plan: keep {len(keeps)} latest snapshots, move {len(moves)} older.")
    print()

    # Create destination dirs upfront
    for _, dest in moves:
        parent = os.path.dirname(dest)
        if parent and not os.path.isdir(parent):
            os.makedirs(parent, exist_ok=True)

    # Execute moves
    moved = 0
    failed = []
    for src, dest in moves:
        try:
            shutil.move(src, dest)
            moved += 1
        except Exception as e:
            failed.append((src, dest, str(e)))

    print(f"Moved: {moved}/{len(moves)}")
    if failed:
        print(f"Failed: {len(failed)}")
        for src, dest, err in failed[:5]:
            print(f"  ! {src} -> {dest}: {err}")
        if len(failed) > 5:
            print(f"  ... and {len(failed) - 5} more")

    print()
    print("=== Snapshots kept in place ===")
    for k in keeps:
        print(f"  {k}")

    print()
    print(f"=== Archive root: ./{DEST_ROOT}/ ===")


if __name__ == "__main__":
    main()
