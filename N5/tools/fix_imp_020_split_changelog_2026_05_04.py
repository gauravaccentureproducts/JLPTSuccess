"""IMP-020: split N5/CHANGELOG.md after v1.10.x.

Rationale (audit 2026-05-04 round 2): CHANGELOG.md is 2924 lines / ~140 KB,
and the active backlog is everything since v1.10.0 (the "syllabus dashboard"
milestone, when the app stabilised). Older entries (v1.0.0 - v1.9.0) are
historic and bloat the main file.

This script:
1. Reads the current CHANGELOG.md.
2. Splits at the v1.9.0 boundary — keeps v1.10.0 and newer in the main file.
3. Writes the v1.9.0-and-older block to docs/CHANGELOG-archive.md with a
   short preface explaining the split.
4. Replaces the tail of CHANGELOG.md with a "see archive" pointer.

Idempotent: detects the archive pointer and exits cleanly if already split.
"""
from __future__ import annotations
import io, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
MAIN = ROOT / 'CHANGELOG.md'
ARCHIVE = ROOT / 'docs' / 'CHANGELOG-archive.md'

# Anchor: the first line of the v1.9.0 entry (= split boundary).
SPLIT_HEADING = '## v1.9.0 - 2026-05-02 (Japanese-first language sweep)'

ARCHIVE_PREFACE = """# Changelog archive (v1.0.0 - v1.9.0)

These entries pre-date the v1.10.0 syllabus-dashboard milestone (2026-05-02).
They are kept verbatim for historical reference only — see `../CHANGELOG.md`
for the active backlog.

---

"""

POINTER_FOOTER = """## Older releases

For v1.9.0 and earlier (initial release through the Japanese-first language
sweep), see [docs/CHANGELOG-archive.md](docs/CHANGELOG-archive.md).

---

*This changelog only records changes visible to users. For commit-level history, see git log.*
"""


def main() -> int:
    text = MAIN.read_text(encoding='utf-8')

    # Idempotency check.
    if 'docs/CHANGELOG-archive.md' in text:
        print('Already split — pointer present in main CHANGELOG.md.')
        return 0

    idx = text.find(SPLIT_HEADING)
    if idx < 0:
        print(f'ERROR: split heading not found: {SPLIT_HEADING!r}')
        return 1

    # Walk back over the "---\n\n" separator that precedes v1.9.0 so the
    # archive starts cleanly at the heading and the main file ends without
    # a dangling "---".
    head = text[:idx].rstrip()
    if head.endswith('---'):
        head = head[:-3].rstrip()

    # Archive payload = v1.9.0 through end-of-file (drop the original
    # trailing "*This changelog…*" sign-off — the new pointer footer
    # in the main file restores it).
    tail = text[idx:].rstrip()
    SIGN_OFF = '*This changelog only records changes visible to users. For commit-level history, see git log.*'
    if tail.endswith(SIGN_OFF):
        tail = tail[:-len(SIGN_OFF)].rstrip()
        if tail.endswith('---'):
            tail = tail[:-3].rstrip()

    ARCHIVE.parent.mkdir(parents=True, exist_ok=True)
    ARCHIVE.write_text(ARCHIVE_PREFACE + tail + '\n', encoding='utf-8')

    new_main = head + '\n\n---\n\n' + POINTER_FOOTER
    MAIN.write_text(new_main, encoding='utf-8')

    main_lines = new_main.count('\n')
    arch_lines = (ARCHIVE_PREFACE + tail).count('\n')
    print(f'Split CHANGELOG.md: main={main_lines} lines, archive={arch_lines} lines.')
    print(f'Archive written to {ARCHIVE.relative_to(ROOT)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
