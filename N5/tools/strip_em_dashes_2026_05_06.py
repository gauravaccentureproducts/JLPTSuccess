"""Strip em-dash (U+2014) characters across all in-scope files in the
JLPTSuccess repo, replacing with a regular hyphen-minus (U+002D).

User-visible em-dashes had crept back into top-level brand surfaces,
specs, docs, prompts, code, content data, and several feedback files
since the v1.10.x "em-dash-free" pass. The X-6.5 integrity invariant
only covers KnowledgeBank/*.md + data/*.md, so most files were not
guarded. This pass cleans them all.

Scope (in):
  - Top-level *.html *.md *.txt *.yml
  - N5/index.html, N5/css/main.css (NOT main.min.css)
  - N5/js/*.js (NOT N5/js/min/*)
  - N5/data/**/*.json (including paper files)
  - N5/locales/*.json
  - N5/tools/*.py
  - N5/specifications/*.md
  - N5/prompts/*.txt
  - N5/feedback/*.md (including closed/ historical archives, per
    user's "all places" directive)
  - .github/**

Scope (out — skipped):
  - N4/* (work-blocked per CLAUDE.md Rule 1)
  - N5/js/min/* (auto-generated; will regenerate clean)
  - *.js.map *.min.js *.min.css (auto-generated)
  - node_modules, __pycache__, .git, _npx
  - visual-regression.spec.js-snapshots (binary PNG)
  - This script itself (would create a self-reference loop)

Idempotent: re-running on already-cleaned files is a no-op.
"""
from __future__ import annotations
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent  # JLPTSuccess root

EM_DASH = '—'
REPLACEMENT = '-'

SKIP_DIR_PARTS = {
    '.git', 'node_modules', '__pycache__', '_npx',
    'min', 'visual-regression.spec.js-snapshots',
    'N4',  # N4 work-block
}
SKIP_FILE_SUFFIXES = ('.js.map', '.min.js', '.min.css', '.png', '.jpg', '.jpeg',
                      '.gif', '.ico', '.svg.gz', '.woff', '.woff2', '.mp3',
                      '.zip', '.xlsx', '.docx', '.pdf', '.bin')
INCLUDED_EXTS = {'.html', '.css', '.js', '.json', '.md', '.txt', '.py',
                 '.yml', '.yaml', '.svg'}

# Files that hold the literal U+2014 character as a SENTINEL (used to
# DETECT em-dashes in other files). These must NOT be processed by this
# script — replacing their em-dash sentinel with a hyphen would break
# the integrity check / fix scripts.
SENTINEL_FILES = {
    'strip_em_dashes_2026_05_06.py',  # this script (self-exclude)
    'check_content_integrity.py',     # X-6.5 invariant
    'fix_audit_2026_05_03_batch.py',  # round-3 fix script
    'fix_infra_audit_2026_05_03.py',  # infra-audit fix script
}


def should_process(p: Path) -> bool:
    if p.name in SENTINEL_FILES:
        return False
    if p.suffix not in INCLUDED_EXTS:
        return False
    parts = set(p.parts)
    if parts & SKIP_DIR_PARTS:
        return False
    if any(p.name.endswith(s) for s in SKIP_FILE_SUFFIXES):
        return False
    return True


def main():
    total_files = 0
    total_replacements = 0
    changed_files = []
    for p in ROOT.rglob('*'):
        if not p.is_file():
            continue
        if not should_process(p):
            continue
        try:
            text = p.read_text(encoding='utf-8')
        except (UnicodeDecodeError, PermissionError):
            continue
        n = text.count(EM_DASH)
        if n == 0:
            continue
        new_text = text.replace(EM_DASH, REPLACEMENT)
        # Preserve LF line endings from the original
        p.write_text(new_text, encoding='utf-8', newline='\n')
        changed_files.append((str(p.relative_to(ROOT)), n))
        total_files += 1
        total_replacements += n

    print(f'Replaced {total_replacements} em-dashes across {total_files} files.')
    print()
    print('Top 20 changed files by count:')
    for path, n in sorted(changed_files, key=lambda x: -x[1])[:20]:
        print(f'  {n:>5} {path}')


if __name__ == '__main__':
    main()
