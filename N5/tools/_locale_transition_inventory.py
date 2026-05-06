"""Phase 0 inventory script for the en+hi locale transition.

Produces a markdown report of every N5-tree file that references the
four locales being removed (vi, id, ne, zh) plus any 5-locale claim
text. Output: feedback/locale-transition-inventory.md.

Excluded directories: js/min/* (generated), audio/, svg/, fonts/,
__pycache__, node_modules, .git, /N4/ tree (work-blocked but flagged
in the report so the user sees the contamination expected).
"""
from __future__ import annotations
import io, os, re, sys
from collections import defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent  # JLPT N5 root
REPO_ROOT = ROOT.parent  # JLPTSuccess root

EXCLUDE_DIRS = {'min', 'node_modules', '.git', 'audio', 'svg', 'fonts',
                '__pycache__', '.claude', 'dist'}
EXCLUDE_EXTS = {'.png', '.mp3', '.woff2', '.svg', '.lock', '.ico',
                '.webp', '.jpg', '.jpeg', '.gif', '.pdf', '.docx',
                '.xlsx', '.bin', '.pyc'}

# Patterns that indicate vi/id/ne/zh involvement.
PATTERNS = [
    ('locale_suffixed_field', re.compile(r'\b(?:gloss|meaning|meanings|explanation|notes|title|prompt)_(vi|id|ne|zh)\b')),
    ('quoted_locale', re.compile(r"['\"]\s*(vi|id|ne|zh)\s*['\"]")),
    ('locale_json',  re.compile(r'locales/(vi|id|ne|zh)\.json')),
    ('english_name', re.compile(r'\b(Vietnamese|Indonesian|Nepali|Mandarin|Chinese)\b')),
    ('native_name',  re.compile(r'(Tiếng\s*Việt|Bahasa\s*Indonesia|नेपाली|中文)')),
    ('claim_phrase', re.compile(r'(5\s*locales?|five[-\s]locale|en/vi/id/ne/zh|vi/id/ne/zh|EN\s*[\|·,/]\s*VI)')),
]


def scan(scope_root: Path, label: str) -> dict[str, list[tuple[str, str]]]:
    hits = defaultdict(list)
    for dirpath, dirnames, filenames in os.walk(scope_root):
        # Skip excluded subtrees in-place
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS]
        for fn in filenames:
            ext = os.path.splitext(fn)[1].lower()
            if ext in EXCLUDE_EXTS:
                continue
            path = Path(dirpath) / fn
            try:
                text = path.read_text(encoding='utf-8')
            except Exception:
                continue
            rel = str(path.relative_to(REPO_ROOT)).replace('\\', '/')
            for kind, pat in PATTERNS:
                m = pat.search(text)
                if m:
                    hits[rel].append((kind, m.group(0)[:50]))
                    break
    return hits


def main() -> int:
    n5_hits = scan(ROOT, 'N5')
    repo_top_hits = {}
    for top in REPO_ROOT.iterdir():
        if not top.is_file():
            continue
        ext = top.suffix.lower()
        if ext in EXCLUDE_EXTS:
            continue
        try:
            text = top.read_text(encoding='utf-8')
        except Exception:
            continue
        for kind, pat in PATTERNS:
            m = pat.search(text)
            if m:
                repo_top_hits[top.name] = (kind, m.group(0)[:50])
                break

    # N4 (work-blocked) - separate
    n4_root = REPO_ROOT / 'N4'
    n4_hits = scan(n4_root, 'N4') if n4_root.exists() else {}

    # Render markdown
    out = []
    out.append('# Locale-transition pre-flight inventory (Phase 0)')
    out.append('')
    out.append('Date: 2026-05-06.')
    out.append('Goal: locate every reference to the four locales being removed (vi, id, ne, zh)')
    out.append('plus any 5-locale claim text. The transition prompt requires this inventory')
    out.append('to be committed before Phase 1 begins.')
    out.append('')
    out.append('## N5 sub-app - files to edit')
    out.append('')
    by_dir = defaultdict(list)
    for path in sorted(n5_hits):
        d = os.path.dirname(path) or 'N5/'
        by_dir[d].append(path)
    out.append(f'**Total: {len(n5_hits)} files.** Grouped by directory:')
    out.append('')
    for d, paths in sorted(by_dir.items()):
        out.append(f'### `{d}/` ({len(paths)} files)')
        out.append('')
        for p in paths:
            kinds = ', '.join(f'`{k}`' for k, _ in n5_hits[p][:3])
            sample = n5_hits[p][0][1].replace('|', '\\|')
            out.append(f'- `{p}` - kinds: {kinds} - sample: `{sample}`')
        out.append('')

    out.append('## Top-level (JLPTSuccess root) files to edit')
    out.append('')
    if repo_top_hits:
        for fn, (kind, sample) in sorted(repo_top_hits.items()):
            sample_md = sample.replace('|', '\\|')
            out.append(f'- `{fn}` - kind `{kind}` - sample `{sample_md}`')
    else:
        out.append('_(no top-level hits)_')
    out.append('')

    out.append('## /N4/ contamination (FLAGGED - must NOT be edited)')
    out.append('')
    out.append('Per `.claude/CLAUDE.md` Rule 1, `/N4/` is work-blocked. The grep below')
    out.append('shows N4 files that reference vi/id/ne/zh - they MUST remain unchanged.')
    out.append('Phase 10 verifies `git diff pre-locale-transition..HEAD --stat` shows zero')
    out.append('N4 deltas.')
    out.append('')
    if n4_hits:
        out.append(f'**N4 hits: {len(n4_hits)} files.**')
        for path in sorted(n4_hits)[:20]:
            kinds = ', '.join(f'`{k}`' for k, _ in n4_hits[path][:2])
            out.append(f'- `{path}` ({kinds})')
        if len(n4_hits) > 20:
            out.append(f'- ... and {len(n4_hits) - 20} more')
    else:
        out.append('_(no N4 hits found)_')
    out.append('')

    # Summary stats per pattern
    out.append('## Pattern-frequency summary (N5 only)')
    out.append('')
    pat_count = defaultdict(int)
    for path in n5_hits:
        for kind, _ in n5_hits[path]:
            pat_count[kind] += 1
    for kind, n in sorted(pat_count.items(), key=lambda x: -x[1]):
        out.append(f'- `{kind}`: {n} hits')
    out.append('')

    # Phase mapping note
    out.append('## Phase mapping')
    out.append('')
    out.append('Per `prompts/LocaleTransitionEnHi.txt`:')
    out.append('')
    out.append('- **Phase 1 (additive)**: create `locales/hi.json`, add `hi` to')
    out.append('  `js/i18n.js` SUPPORTED_LOCALES + chip group + sw.js precache.')
    out.append('- **Phase 2 (migration)**: add `migrateLocaleSetting()` to bootstrap.')
    out.append('- **Phase 3 (remove)**: delete the four locale files; remove the four chips;')
    out.append('  prune SUPPORTED_LOCALES; bump CACHE_VERSION.')
    out.append('- **Phase 4 (data prune)**: tooling script removes `gloss_<lc>` /')
    out.append('  `meaning_<lc>` / `explanation_<lc>` / `meanings_<lc>` keys for')
    out.append('  lc ∈ {vi,id,ne,zh}; seeds `_hi` placeholders.')
    out.append('- **Phase 5 (docs)**: rewrite multilingual claim text in README, PRIVACY,')
    out.append('  CHANGELOG, specs, audit prompt, top-level brand surfaces.')
    out.append('- **Phase 6 (CI)**: update `tools/check_content_integrity.py` locale list.')
    out.append('- **Phase 7 (tests)**: update Playwright specs that assert chip count.')
    out.append('- **Phase 8 (smoke)**: live preview walkthrough.')
    out.append('- **Phase 9 (registry)**: append IMP-NNN row to xlsx.')
    out.append('- **Phase 10 (push)**: `git push origin master`; `pre-locale-transition`')
    out.append('  tag already exists at the parent commit.')
    out.append('')
    out.append('---')
    out.append('')
    out.append('_Generated by `tools/_locale_transition_inventory.py`._')

    inventory_path = ROOT / 'feedback' / 'locale-transition-inventory.md'
    inventory_path.write_text('\n'.join(out) + '\n', encoding='utf-8')
    print(f'Inventory written to {inventory_path}')
    print(f'  N5 hits:  {len(n5_hits)} files')
    print(f'  Top-level hits: {len(repo_top_hits)} files')
    print(f'  N4 hits:  {len(n4_hits)} files (FLAGGED, must not edit)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
