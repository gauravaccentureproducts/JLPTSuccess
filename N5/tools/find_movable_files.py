#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Identify movable files for archival to not-required/.

Candidates considered:
- Date-stamped one-off scripts in tools/ (pattern: *_2026_*.py)
- Standalone artifact JSONs in tools/ (e.g., ui_test_results_*.json)

Excluded by user request:
- data/, locales/, papers/, specifications/, docs/, audio/, fonts/,
  svg/, tests/, .github/, .githooks/, .claude/, not-required/, dist/,
  external-data/, prompts/ (knowledge-base-like)
- Any file in feedback/ (review tracker etc.)
- Any *.bak* / *.backup* (project backup policy)

A candidate is MOVABLE only if it has ZERO references in any of these
"live citation" surfaces:
- Any .md file outside not-required/
- Any .yml file under .github/ or .githooks/
- Any other .py file in tools/ (import or string reference)
- Any .json file in data/ (cross-ref via _meta block etc.)
- Any .txt file under prompts/
- index.html / sw.js / package.json / playwright.config.js
- CHANGELOG.md / README.md / TASKS.md / CONTENT-LICENSE.md / NOTICES.md
- N5/.claude/CLAUDE.md, parent JLPTSuccess/.claude/CLAUDE.md
- JLPT Common/procedure-manual-build-next-jlpt-level.md

Outputs:
- Stdout: per-candidate report (MOVABLE / KEEP {reasons})
- specifications/not_required_move_plan.json: machine-readable plan
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
REPO_ROOT = ROOT.parent  # JLPTSuccess/

# Surfaces to scan for live citations.
LIVE_SCAN_DIRS = [
    ROOT / "tools",
    ROOT / ".github",
    ROOT / "data",
    ROOT / "prompts",
    ROOT / "docs",
    ROOT / "specifications",
    ROOT / "feedback",
    ROOT / "tests",
    ROOT / "js",
    ROOT / "css",
    REPO_ROOT / "JLPT Common",  # cross-level procedure manual
]
LIVE_SCAN_FILES = [
    ROOT / "index.html",
    ROOT / "sw.js",
    ROOT / "package.json",
    ROOT / "playwright.config.js",
    ROOT / "CHANGELOG.md",
    ROOT / "README.md",
    ROOT / "README.hi.md",
    ROOT / "TASKS.md",
    ROOT / "CONTENT-LICENSE.md",
    ROOT / "NOTICES.md",
    ROOT / "PRIVACY.md",
    ROOT / "AUDIO.md",
    ROOT / "SELFHOST.md",
    ROOT / "verification.md",
    ROOT / "browserstack.yml",
    ROOT / "manifest.webmanifest",
    ROOT / ".claude" / "CLAUDE.md",
    REPO_ROOT / ".claude" / "CLAUDE.md",
]

# Exclude from scan (the candidate itself + already-archived material)
EXCLUDE_PATTERNS = [
    "/not-required/",
    "/not_required/",
    "/__pycache__/",
    "/.git/",
    "/dist/",
    "/external-data/",
    "/audio/",
    "/fonts/",
    "/svg/",
]

# Glob to enumerate candidates
CANDIDATE_GLOBS = [
    "tools/*_2026_*.py",          # date-stamped one-off scripts
    "tools/ui_test_results_*.json",  # historical UI test results
]


def is_excluded(p: Path) -> bool:
    sp = str(p).replace("\\", "/")
    return any(pat in sp for pat in EXCLUDE_PATTERNS)


def collect_live_text() -> dict[str, str]:
    """Return {relative_path -> text} for every live-scan file."""
    out = {}
    for d in LIVE_SCAN_DIRS:
        if not d.exists():
            continue
        for p in d.rglob("*"):
            if not p.is_file():
                continue
            if is_excluded(p):
                continue
            try:
                rel = str(p.relative_to(ROOT)).replace("\\", "/")
            except ValueError:
                rel = str(p)
            ext = p.suffix.lower()
            if ext not in (".md", ".yml", ".yaml", ".py", ".json",
                           ".txt", ".html", ".js", ".css", ".webmanifest",
                           ".toml", ".sh"):
                continue
            try:
                out[rel] = p.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
    for f in LIVE_SCAN_FILES:
        if not f.exists() or is_excluded(f):
            continue
        try:
            rel = str(f.relative_to(ROOT)).replace("\\", "/")
        except ValueError:
            rel = str(f)
        try:
            out[rel] = f.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
    return out


def find_references(needle: str, text_by_path: dict[str, str],
                    skip_self: str) -> list[tuple[str, int]]:
    """Find occurrences of `needle` (literal substring) in any live-scan
    file. Returns [(file, line_number)] tuples. Skips the candidate's
    own file."""
    hits = []
    for path, text in text_by_path.items():
        if path == skip_self:
            continue
        idx = 0
        while True:
            i = text.find(needle, idx)
            if i < 0:
                break
            # Compute line number
            line_no = text.count("\n", 0, i) + 1
            hits.append((path, line_no))
            idx = i + len(needle)
    return hits


def main() -> None:
    text_by_path = collect_live_text()
    print(f"Scanned {len(text_by_path)} live-citation files.\n")

    candidates: list[Path] = []
    for pat in CANDIDATE_GLOBS:
        for p in ROOT.glob(pat):
            if is_excluded(p):
                continue
            if p.is_file():
                candidates.append(p)

    candidates = sorted(set(candidates))
    print(f"Candidate count: {len(candidates)}\n")

    movable = []
    keep = []
    for c in candidates:
        rel = str(c.relative_to(ROOT)).replace("\\", "/")
        name = c.name
        stem = c.stem
        # Look up by full filename + bare stem (catches both `tools/foo.py`
        # citations and `foo` Python import refs)
        hits_name = find_references(name, text_by_path, skip_self=rel)
        hits_stem = []
        # Bare-stem only for python files (import x or 'x' references)
        if c.suffix == ".py":
            # Use word-boundary check by searching with python regex on each text
            pat_re = re.compile(rf"(?<![A-Za-z0-9_]){re.escape(stem)}(?![A-Za-z0-9_])")
            for path, text in text_by_path.items():
                if path == rel:
                    continue
                for m in pat_re.finditer(text):
                    line_no = text.count("\n", 0, m.start()) + 1
                    hits_stem.append((path, line_no))
        all_hits = hits_name + hits_stem
        # Deduplicate (filename hit + stem hit can land on same line)
        all_hits = sorted(set(all_hits))
        if all_hits:
            keep.append((rel, all_hits))
        else:
            movable.append(rel)

    print(f"=== MOVABLE ({len(movable)}, zero live references) ===")
    for r in movable:
        print(f"  {r}")
    print()
    print(f"=== KEEP ({len(keep)}, has live references) ===")
    for r, hits in keep:
        print(f"  {r}")
        for h, ln in hits[:5]:
            print(f"    referenced by {h}:{ln}")
        if len(hits) > 5:
            print(f"    ... + {len(hits) - 5} more")
    print()

    # Emit plan JSON
    plan = {
        "scan_root": str(ROOT),
        "scanned_files": len(text_by_path),
        "candidates_total": len(candidates),
        "movable": movable,
        "keep_with_references": [
            {"file": r, "ref_count": len(h),
             "first_refs": [{"path": p, "line": ln} for p, ln in h[:10]]}
            for r, h in keep
        ],
    }
    out_path = ROOT / "specifications" / "not_required_move_plan.json"
    out_path.write_text(json.dumps(plan, indent=2, ensure_ascii=False),
                         encoding="utf-8")
    print(f"Plan written: {out_path}")


if __name__ == "__main__":
    main()
