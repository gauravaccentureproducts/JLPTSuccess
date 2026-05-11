"""Render slow-rate audio for the 3 listening items missing it.

Audit context: audio_slow = 47/50. The 3 missing items
(n5.listen.048/049/050) were recently added without a slow
variant. This script renders slow gtts audio for each.

Output: audio/listening/<id>.slow.mp3 with gtts(slow=True)
+ update listening.json audio_slow field.

Idempotent: skips items where .slow.mp3 already exists.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

TARGETS = ['n5.listen.048', 'n5.listen.049', 'n5.listen.050']


def main() -> int:
    fp = ROOT / 'data' / 'listening.json'
    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {it['id']: it for it in data['items']}

    try:
        from gtts import gTTS
    except ImportError:
        print('gTTS not available — run: pip install gTTS')
        return 1

    audio_dir = ROOT / 'audio' / 'listening'
    n_rendered = 0
    n_wired = 0

    for lid in TARGETS:
        it = by_id.get(lid)
        if not it:
            print(f'  ! missing item: {lid}')
            continue
        if it.get('audio_slow'):
            print(f'  - skip (already wired): {lid}')
            continue

        script = it.get('script_ja') or ''
        if not script:
            print(f'  ! {lid}: no script_ja — skipping')
            continue

        slow_path = audio_dir / f'{lid}.slow.mp3'
        if not slow_path.exists():
            print(f'  + rendering {slow_path.name} ({len(script)} chars)...')
            tts = gTTS(text=script, lang='ja', slow=True)
            tts.save(str(slow_path))
            n_rendered += 1
        else:
            print(f'  ~ slow mp3 exists already: {slow_path.name}')

        rel = f'audio/listening/{lid}.slow.mp3'
        it['audio_slow'] = rel
        it['audio_slow_provenance'] = 'auto_derived'
        n_wired += 1

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nRendered {n_rendered} slow mp3s; wired {n_wired} items.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
