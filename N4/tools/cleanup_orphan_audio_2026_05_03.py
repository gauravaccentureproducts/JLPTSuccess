"""Delete orphan audio MP3s under audio/ that aren't referenced in audio_manifest.json.

Closes infra-audit §4.1 (storage waste, LOW). Re-derives the orphan set from
manifest vs disk on every run so it stays correct if examples are added later.
Uses `git rm` for tracked files so the deletion goes through git's audit trail.

Idempotent: safe to re-run.
"""
from __future__ import annotations
import io
import json
import subprocess
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
AUDIO_EXT = {'.mp3', '.wav', '.ogg', '.m4a'}


def collect_declared_paths() -> set[str]:
    manifest = json.loads((ROOT / 'data' / 'audio_manifest.json').read_text(encoding='utf-8'))
    items = manifest['items'] if isinstance(manifest, dict) and 'items' in manifest else manifest
    declared: set[str] = set()
    for it in items:
        p = it.get('path') or it.get('audio') or ''
        if p:
            declared.add(p.lstrip('/').replace('\\', '/'))
    return declared


def collect_on_disk() -> list[Path]:
    audio_dir = ROOT / 'audio'
    if not audio_dir.exists():
        return []
    return [f for f in audio_dir.rglob('*')
            if f.is_file() and f.suffix.lower() in AUDIO_EXT]


def is_tracked(rel_posix: str) -> bool:
    """Return True iff the file is tracked by git."""
    try:
        result = subprocess.run(
            ['git', 'ls-files', '--error-unmatch', rel_posix],
            cwd=str(ROOT),
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def main() -> int:
    declared = collect_declared_paths()
    on_disk = collect_on_disk()
    orphans: list[Path] = []
    for f in on_disk:
        rel = f.relative_to(ROOT).as_posix()
        if rel not in declared:
            orphans.append(f)

    if not orphans:
        print('No orphan audio files. Already clean.')
        return 0

    total_bytes = sum(f.stat().st_size for f in orphans)
    print(f'Orphan count: {len(orphans)} files ({total_bytes / 1024 / 1024:.2f} MB)')

    tracked: list[str] = []
    untracked: list[Path] = []
    for f in orphans:
        rel = f.relative_to(ROOT).as_posix()
        if is_tracked(rel):
            tracked.append(rel)
        else:
            untracked.append(f)

    if tracked:
        print(f'Removing {len(tracked)} tracked files via git rm ...')
        # git rm in batches to avoid command-line length limits
        BATCH = 50
        for i in range(0, len(tracked), BATCH):
            batch = tracked[i:i + BATCH]
            subprocess.run(['git', 'rm', '-q', '--', *batch], cwd=str(ROOT), check=True)

    if untracked:
        print(f'Removing {len(untracked)} untracked files via fs unlink ...')
        for f in untracked:
            f.unlink()

    print(f'Done. Removed {len(tracked) + len(untracked)} orphan files.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
