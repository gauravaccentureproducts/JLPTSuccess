"""IMP-007 (2026-05-14): generate CHANGELOG.md entries from Conventional
Commits messages.

Reads `git log <from>..<to>` (default: last tag .. HEAD), filters commits
that follow the Conventional Commits format (feat:, fix:, chore:, docs:,
refactor:, content:, perf:, test:, ci:, style:), and emits a markdown
block ready to paste into CHANGELOG.md under a new version header.

Conventional Commits format we accept:
    <type>(<optional scope>): <subject>
    [optional body...]

Recognized types (with section headers in output):
    feat        → Features
    content     → Content (corpus authoring, audit findings)
    fix         → Fixes
    perf        → Performance
    refactor    → Refactoring
    docs        → Documentation
    chore       → Chores
    test        → Tests
    ci          → CI / Build
    style       → Style (cosmetic)

Usage:
    python -X utf8 tools/generate_changelog_from_commits.py
        # uses git log <last-tag>..HEAD by default
    python -X utf8 tools/generate_changelog_from_commits.py --from v1.15.4
        # explicit start tag
    python -X utf8 tools/generate_changelog_from_commits.py --version v1.15.5
        # emits the version header
    python -X utf8 tools/generate_changelog_from_commits.py --append
        # prepends the block to CHANGELOG.md after "# Changelog\n\n..."

Adopting Conventional Commits going forward:
    - Every commit message starts with `<type>: <subject>`.
    - Subject is imperative, lower-case, <= 60 chars.
    - For breaking changes, add `!` after type (e.g. `feat!: drop X`).
    - Body (optional) explains the why.
    - Refer to issue IDs (ISSUE-NNN, IMP-NNN) in body when relevant.
"""
from __future__ import annotations
import argparse
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = ROOT / "CHANGELOG.md"

TYPE_HEADERS = {
    "feat":     ("✨ Features",        1),
    "content":  ("📚 Content",         2),
    "fix":      ("🐛 Fixes",           3),
    "perf":     ("⚡ Performance",      4),
    "refactor": ("♻️ Refactoring",      5),
    "docs":     ("📖 Documentation",   6),
    "chore":    ("🔧 Chores",          7),
    "test":     ("✅ Tests",           8),
    "ci":       ("🤖 CI / Build",      9),
    "style":    ("🎨 Style",          10),
}

CONVENTIONAL_RE = re.compile(
    r"^(?P<type>feat|content|fix|perf|refactor|docs|chore|test|ci|style)"
    r"(?P<breaking>!)?"
    r"(?:\((?P<scope>[^)]+)\))?"
    r":\s*(?P<subject>.+)$"
)


def get_last_tag() -> str:
    """Return the most recent annotated git tag (e.g. 'v1.15.4')."""
    try:
        out = subprocess.check_output(
            ["git", "describe", "--tags", "--abbrev=0"],
            cwd=ROOT, text=True, stderr=subprocess.DEVNULL
        )
        return out.strip()
    except subprocess.CalledProcessError:
        return ""


def get_commits(since: str, until: str) -> list[dict]:
    """Return list of {sha, subject, body} for commits in the range."""
    range_spec = f"{since}..{until}" if since else until
    fmt = "%H%n%s%n%b%n--END--"
    out = subprocess.check_output(
        ["git", "log", range_spec, f"--pretty=format:{fmt}"],
        cwd=ROOT, text=True, errors="replace"
    )
    commits = []
    for block in out.split("--END--"):
        block = block.strip()
        if not block:
            continue
        lines = block.split("\n", 2)
        sha = lines[0]
        subject = lines[1] if len(lines) > 1 else ""
        body = lines[2] if len(lines) > 2 else ""
        commits.append({"sha": sha[:7], "subject": subject, "body": body.strip()})
    return commits


def classify(subject: str) -> tuple[str, str, str] | None:
    """Parse a Conventional Commits subject. Returns (type, scope, subject)
    or None if it doesn't match the format."""
    m = CONVENTIONAL_RE.match(subject)
    if not m:
        return None
    return (m.group("type"), m.group("scope") or "", m.group("subject"))


def render_block(version: str, commits: list[dict]) -> str:
    """Build the CHANGELOG.md markdown block."""
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    lines = [f"## {version} - {today} (auto-generated from Conventional Commits)"]
    lines.append("")

    # Group by type
    groups: dict[str, list[dict]] = {t: [] for t in TYPE_HEADERS}
    unclassified: list[dict] = []
    for c in commits:
        parsed = classify(c["subject"])
        if parsed is None:
            unclassified.append(c)
            continue
        typ, scope, subj = parsed
        groups[typ].append({"sha": c["sha"], "scope": scope, "subject": subj, "body": c["body"]})

    for typ, (header, _) in sorted(TYPE_HEADERS.items(), key=lambda kv: kv[1][1]):
        bucket = groups[typ]
        if not bucket:
            continue
        lines.append(f"### {header}")
        lines.append("")
        for c in bucket:
            scope_prefix = f"**{c['scope']}**: " if c["scope"] else ""
            lines.append(f"- {scope_prefix}{c['subject']} ({c['sha']})")
        lines.append("")

    if unclassified:
        lines.append("### Other (non-Conventional-Commits)")
        lines.append("")
        for c in unclassified:
            lines.append(f"- {c['subject']} ({c['sha']})")
        lines.append("")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--from", dest="since", default="",
                        help="Start commit / tag (defaults to last tag)")
    parser.add_argument("--to", dest="until", default="HEAD",
                        help="End commit / tag (defaults to HEAD)")
    parser.add_argument("--version", default="vNEXT",
                        help="Version label for the new entry header")
    parser.add_argument("--append", action="store_true",
                        help="Prepend the generated block to CHANGELOG.md after the title")
    args = parser.parse_args()

    if not args.since:
        args.since = get_last_tag()

    commits = get_commits(args.since, args.until)
    if not commits:
        print(f"No commits found in {args.since}..{args.until}", file=sys.stderr)
        return 1

    block = render_block(args.version, commits)

    if args.append:
        existing = CHANGELOG.read_text(encoding="utf-8")
        marker = "# Changelog\n\nAll user-visible changes to the JLPT N5 study material site.\n\n"
        if marker in existing:
            new_content = existing.replace(marker, marker + block + "\n", 1)
            CHANGELOG.write_text(new_content, encoding="utf-8")
            print(f"Prepended {len(commits)} commits as {args.version} into CHANGELOG.md")
        else:
            print("WARN: marker not found in CHANGELOG.md; printing to stdout instead.", file=sys.stderr)
            print(block)
    else:
        print(block)
    return 0


if __name__ == "__main__":
    sys.exit(main())
