"""One-shot audit: group untracked backup files by base filename, identify
latest version per group, build a relocation plan. Run from N5/ root.

Read-only — produces the plan; user confirms before any move happens.
"""
import os
import re
import sys
import io
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

WIN_SEP = chr(92)  # backslash; avoid escape in source


def normalize(p: str) -> str:
    return p.replace(WIN_SEP, "/").lstrip("./")


def enumerate_backups() -> list[str]:
    files = []
    for root, dirs, fs in os.walk("."):
        # skip .git
        if ".git" in root.split(os.sep):
            continue
        for f in fs:
            if ".bak" in f or ".backup" in f:
                files.append(normalize(os.path.join(root, f)))
    return files


def base_of(path: str) -> str:
    m = re.match(r"(.+?)\.(bak|backup)", path)
    return m.group(1) if m else path


def mtime(p: str) -> float:
    try:
        return os.path.getmtime(p)
    except OSError:
        return 0.0


def main() -> None:
    bak = enumerate_backups()
    groups: dict[str, list[str]] = defaultdict(list)
    for p in bak:
        groups[base_of(p)].append(p)

    print(f"Total backup files: {len(bak)}")
    print(f"Distinct base files: {len(groups)}")
    print()
    print("=== Per-group breakdown ===")
    total_keep = 0
    total_move = 0
    for base in sorted(groups.keys()):
        paths = sorted(groups[base], key=mtime, reverse=True)
        latest = paths[0]
        older = paths[1:]
        total_keep += 1
        total_move += len(older)
        if len(paths) > 1:
            print()
            print(f"{base}  ({len(paths)} backup files)")
            print(f"  KEEP latest: {latest}")
            for o in older:
                print(f"  MOVE older:  {o}")

    print()
    print("=== Singletons (no older versions; just keep) ===")
    singletons = [base for base, paths in groups.items() if len(paths) == 1]
    print(f"  {len(singletons)} files have no older sibling - keep in place.")

    print()
    print("=== Plan summary ===")
    print(f"  KEEP: {total_keep} latest backups (one per logical group)")
    print(f"  MOVE: {total_move} older backups -> not-required/")
    print(f"  Net: {len(bak)} -> {total_keep} kept + {total_move} moved")


if __name__ == "__main__":
    main()
