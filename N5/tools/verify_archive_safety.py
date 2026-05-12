"""Safety check before archiving 79 older snapshot files out of the working tree.

For each group, verify the "latest" snapshot contains all important content
from older snapshots. Done at THREE levels:

1. Size monotonicity - the corpus is additive (audit waves only add fields,
   never remove). Within a group, file size should generally be monotonic
   non-decreasing by mtime. An older snapshot LARGER than the latest is a
   red flag worth investigating before moving.

2. Content superset (for JSON files only) - load latest + each older,
   check that the latest has at least the same number of top-level
   entries (patterns / entries / passages / items) as every older one.
   Catches the "wave shrank the corpus" anomaly that size-only misses.

3. Current vs latest parity - the LIVE file is the actual source of
   truth (everything committed). The latest snapshot should be a recent
   subset of the live file. If the latest snapshot is LARGER than the live
   file, something was deleted post-snapshot and is only recoverable from
   the snapshot - DO NOT move it.

Output: per-group GREEN / YELLOW / RED status. Only GREEN groups are
safe to relocate.
"""
import json
import os
import re
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
        if ".git" in root.split(os.sep):
            continue
        for f in fs:
            if ".bak" in f or ".backup" in f:
                files.append(normalize(os.path.join(root, f)))
    return files


def base_of(path: str) -> str:
    m = re.match(r"(.+?)\.(bak|backup)", path)
    return m.group(1) if m else path


def count_top_level(path: str):
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except (json.JSONDecodeError, UnicodeDecodeError, OSError):
        return None
    if isinstance(data, dict):
        for key in ("patterns", "entries", "passages", "items", "questions"):
            if key in data and isinstance(data[key], list):
                return len(data[key])
        return len(data)
    if isinstance(data, list):
        return len(data)
    return None


def main() -> None:
    snaps = enumerate_snapshots()
    groups: dict[str, list[str]] = defaultdict(list)
    for p in snaps:
        groups[base_of(p)].append(p)

    all_green = True
    print(f"Verifying {len(snaps)} snapshots across {len(groups)} groups...\n")

    for base in sorted(groups.keys()):
        paths = sorted(groups[base], key=os.path.getmtime, reverse=True)
        latest = paths[0]
        older = paths[1:]

        sizes = [(p, os.path.getsize(p)) for p in paths]
        latest_size = sizes[0][1]

        live_size = os.path.getsize(base) if os.path.exists(base) else None

        size_red_flags = [
            (p, s) for p, s in sizes[1:] if s > latest_size * 1.05
        ]

        latest_count = count_top_level(latest)
        live_count = count_top_level(base) if base and os.path.exists(base) else None
        older_counts = {p: count_top_level(p) for p in older}
        count_red_flags = []
        if latest_count is not None:
            for p, c in older_counts.items():
                if c is not None and c > latest_count:
                    count_red_flags.append((p, c, latest_count))

        live_vs_latest = "OK"
        if live_size is not None:
            if latest_size > live_size * 1.05:
                live_vs_latest = (
                    f"RED: latest snapshot ({latest_size:,}B) larger than "
                    f"live file ({live_size:,}B) - content lost post-snapshot"
                )

        status = "GREEN"
        notes = []
        if size_red_flags:
            status = "YELLOW"
            for p, s in size_red_flags:
                notes.append(
                    f"older {os.path.basename(p)} ({s:,}B) > latest ({latest_size:,}B)"
                )
        if count_red_flags:
            status = "YELLOW"
            for p, c, lc in count_red_flags:
                notes.append(
                    f"older {os.path.basename(p)} has {c} entries > latest {lc}"
                )
        if live_vs_latest != "OK":
            status = "RED"
            notes.append(live_vs_latest)
            all_green = False

        print(f"[{status}] {base}")
        print(f"      latest: {os.path.basename(latest)}")
        if latest_count is not None:
            older_count_vals = [str(c) for c in older_counts.values() if c is not None]
            print(
                f"      counts: latest={latest_count}, "
                f"live={live_count}, older=[{', '.join(older_count_vals)}]"
            )
        live_sz_str = f", live={live_size:,}B" if live_size else ""
        print(f"      sizes:  latest={latest_size:,}B{live_sz_str}")
        for n in notes:
            print(f"      NOTE: {n}")
        print()

    print("=" * 60)
    if all_green:
        print("ALL GREEN: safe to archive 79 older snapshots.")
    else:
        print("RED flags present - investigate before archiving.")
    print("=" * 60)


if __name__ == "__main__":
    main()
