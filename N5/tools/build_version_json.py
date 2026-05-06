"""IMP-035 (audit round 3): write data/version.json with the live build
stamp + corpus counts.

Goal: a single machine-readable artefact that the footer parser, the
service worker, the CSP-checker, and the README-consistency check can
all read from. Avoids the silent drift that round-1 closed for the
footer (ISSUE-001) and that round-3 surfaced for sw.js CACHE_VERSION
(ISSUE-024) and README counts (ISSUE-014).

Source of truth:
  - version: first `## v\\d+\\.\\d+\\.\\d+` heading in CHANGELOG.md
  - builtAt: ISO-8601 UTC timestamp of this run
  - counts:  derived live from data/*.json + data/papers/

Run:
    python tools/build_version_json.py

Idempotent: re-running rewrites the file with the same content if no
upstream input has changed.
"""
from __future__ import annotations
import io, json, os, re, sys
from datetime import datetime, timezone
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
CHANGELOG = ROOT / 'CHANGELOG.md'
DATA = ROOT / 'data'
OUT = DATA / 'version.json'
SW = ROOT / 'sw.js'

# ISSUE-024: literal in sw.js to keep in sync with the latest CHANGELOG
# version. Same regression risk as the v1.10→v1.12 footer drift round-1
# closed for the displayed footer; this closes it for the cache key.
SW_CACHE_VERSION_RE = re.compile(
    r"(const\s+CACHE_VERSION\s*=\s*['\"])(jlptsuccess-n5-[^'\"]+)(['\"])"
)

VERSION_RE = re.compile(r'^##\s+(v\d+\.\d+\.\d+)', re.MULTILINE)


def latest_version() -> str:
    text = CHANGELOG.read_text(encoding='utf-8')
    m = VERSION_RE.search(text)
    if not m:
        raise SystemExit('ERROR: no v-version heading in CHANGELOG.md')
    return m.group(1)


def count_top(p: Path, key: str) -> int:
    """Count entries under a top-level array key in a JSON file."""
    return len(json.loads(p.read_text(encoding='utf-8')).get(key, []))


def _count_invariants() -> int:
    """ISSUE-035: read the live CHECKS list length from
    check_content_integrity.py rather than hardcoding. Imports the module
    to access its CHECKS tuple directly - same source the runtime uses,
    so the count cannot drift."""
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        'check_content_integrity',
        Path(__file__).parent / 'check_content_integrity.py',
    )
    if spec is None or spec.loader is None:
        return 0
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    checks = getattr(mod, 'CHECKS', None)
    return len(checks) if checks else 0


def count_papers() -> tuple[int, int]:
    """Return (total_papers, total_questions) by walking data/papers/*."""
    papers = 0
    questions = 0
    for sub in ('moji', 'goi', 'bunpou', 'dokkai'):
        sub_dir = DATA / 'papers' / sub
        if not sub_dir.is_dir():
            continue
        for f in sorted(sub_dir.iterdir()):
            if not f.name.startswith('paper-'):
                continue
            papers += 1
            data = json.loads(f.read_text(encoding='utf-8'))
            questions += len(data.get('questions', []))
    return papers, questions


def main() -> int:
    version = latest_version()
    paper_count, paper_q = count_papers()
    counts = {
        'grammar':         count_top(DATA / 'grammar.json',  'patterns'),
        'vocab':           count_top(DATA / 'vocab.json',    'entries'),
        'kanji':           count_top(DATA / 'kanji.json',    'entries'),
        'reading':         count_top(DATA / 'reading.json',  'passages'),
        'listening':       count_top(DATA / 'listening.json','items'),
        'questions':       count_top(DATA / 'questions.json','questions'),
        'papers':          paper_count,
        'paperQuestions':  paper_q,
    }
    # ISSUE-035 (audit round-5): live invariants count from check_content_integrity.py
    # rather than a hand-written placeholder. Round-3 added JA-33 + round-4 added
    # JA-34/JA-35 without the placeholder catching up. Reading the live CHECKS
    # list keeps the build stamp honest as future invariants land.
    invariants_count = _count_invariants()
    out = {
        'version':       version,
        'builtAt':       datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        'counts':        counts,
        'invariants':    f'{invariants_count}/{invariants_count} (per tools/check_content_integrity.py)',
        'cacheVersion':  f'jlptsuccess-n5-{version}',
        'note':          (
            'Single source of truth for build-stamp + corpus counts. '
            'Read by js/app.js footer parser (fallback path), sw.js '
            'CACHE_VERSION derivation, and the README-consistency check. '
            'Regenerate via `python tools/build_version_json.py`.'
        ),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    # ISSUE-024: rewrite sw.js CACHE_VERSION to match the latest version.
    # Idempotent - replace_all with the same value is a no-op.
    sw_text = SW.read_text(encoding='utf-8')
    new_sw_text, n = SW_CACHE_VERSION_RE.subn(
        lambda m: f'{m.group(1)}{out["cacheVersion"]}{m.group(3)}',
        sw_text,
        count=1,
    )
    if n == 0:
        print('  WARN: CACHE_VERSION literal not found in sw.js (skipped rewrite)')
    elif new_sw_text != sw_text:
        SW.write_text(new_sw_text, encoding='utf-8')
        print(f'  Updated sw.js CACHE_VERSION -> {out["cacheVersion"]}')

    print(f'Wrote {OUT.relative_to(ROOT)}')
    print(f'  version       = {version}')
    print(f'  builtAt       = {out["builtAt"]}')
    print(f'  cacheVersion  = {out["cacheVersion"]}')
    for k, v in counts.items():
        print(f'  counts.{k:<14} = {v}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
