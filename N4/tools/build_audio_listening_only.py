"""Render audio for listening items only (priority over grammar audio).

Wraps build_audio.py logic but processes only the listening items so the
chokai UI works end-to-end. Grammar audio is lower priority and can be
rendered in subsequent passes via the main build_audio.py script.
"""
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Reuse build_audio's helpers
sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_audio  # noqa

ROOT = build_audio.ROOT
LISTENING_JSON = build_audio.LISTENING_JSON
OUT_LISTENING = build_audio.OUT_LISTENING

# Detect backend (will pick gtts if available, voicevox not running locally)
backend = build_audio.detect_backend('gtts')
print(f'Backend: {backend}')

OUT_LISTENING.mkdir(parents=True, exist_ok=True)

l = json.loads(LISTENING_JSON.read_text(encoding='utf-8'))
items = l.get('items', [])
print(f'Listening items: {len(items)}')

manifest_items = []
rendered = 0
skipped = 0
failed = 0

for it in items:
    ja = it.get('script_ja') or it.get('prompt_ja')
    if not ja:
        continue
    out_base = OUT_LISTENING / it['id']
    out_path = Path(str(out_base) + ('.mp3' if backend == 'gtts' else '.wav'))
    if out_path.exists():
        skipped += 1
        manifest_items.append({'id': it['id'], 'path': str(out_path.relative_to(ROOT))})
        continue
    try:
        text = build_audio.normalize_for_tts(ja)
        if backend == 'gtts':
            from gtts import gTTS
            tts = gTTS(text=text, lang='ja', slow=False)
            tts.save(str(out_path))
        else:
            print(f'  Unsupported backend for this script: {backend}')
            break
        rendered += 1
        manifest_items.append({'id': it['id'], 'path': str(out_path.relative_to(ROOT))})
        if rendered % 5 == 0:
            print(f'  ... {rendered} rendered')
    except Exception as e:
        failed += 1
        print(f'  failed: {it["id"]}: {e}')

# Update audio_manifest.json (merge with existing)
manifest_path = ROOT / 'data' / 'audio_manifest.json'
if manifest_path.exists():
    existing = json.loads(manifest_path.read_text(encoding='utf-8'))
else:
    existing = {'_meta': {'schema_version': 1, 'voice_default': 'synthetic'}, 'items': []}

# Replace listening entries; keep others
existing_items = [m for m in existing.get('items', []) if not m.get('id', '').startswith('n4.listen.')]
existing_items.extend(manifest_items)
existing['items'] = existing_items
existing['_meta']['total_files'] = len(existing_items)

manifest_path.write_text(
    json.dumps(existing, ensure_ascii=False, indent=2) + '\n', encoding='utf-8'
)

print(f'\nDone. rendered={rendered} skipped={skipped} failed={failed}')
print(f'Manifest: {manifest_path}')
