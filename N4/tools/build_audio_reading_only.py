"""Render audio for reading passages only.

Mirrors build_audio_listening_only.py but for the reading corpus.
"""
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_audio  # noqa

ROOT = build_audio.ROOT
READING_JSON = build_audio.READING_JSON
OUT_READING = build_audio.OUT_READING

backend = build_audio.detect_backend('gtts')
print(f'Backend: {backend}')

OUT_READING.mkdir(parents=True, exist_ok=True)

r = json.loads(READING_JSON.read_text(encoding='utf-8'))
passages = r.get('passages', [])
print(f'Reading passages: {len(passages)}')

rendered = 0
skipped = 0
failed = 0
manifest_items = []

for p in passages:
    ja = p.get('ja')
    if not ja:
        continue
    out_base = OUT_READING / p['id']
    out_path = Path(str(out_base) + '.mp3')
    if out_path.exists():
        skipped += 1
        manifest_items.append({'id': p['id'], 'path': str(out_path.relative_to(ROOT)), 'voice': 'synthetic-gtts'})
        continue
    try:
        text = build_audio.normalize_for_tts(ja)
        from gtts import gTTS
        gTTS(text=text, lang='ja', slow=False).save(str(out_path))
        rendered += 1
        manifest_items.append({'id': p['id'], 'path': str(out_path.relative_to(ROOT)), 'voice': 'synthetic-gtts'})
        if rendered % 5 == 0:
            print(f'  ... {rendered} rendered')
    except Exception as e:
        failed += 1
        print(f'  failed: {p["id"]}: {e}')

# Update manifest (additive)
m_path = ROOT / 'data' / 'audio_manifest.json'
existing = json.loads(m_path.read_text(encoding='utf-8')) if m_path.exists() else {'items': []}
existing_items = [it for it in existing.get('items', []) if not it.get('id', '').startswith('reading.n4.')]
for mi in manifest_items:
    existing_items.append({
        'id': f'reading.{mi["id"]}',
        'path': mi['path'],
        'voice': mi['voice'],
    })
existing['items'] = existing_items
m_path.write_text(json.dumps(existing, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

print(f'\nDone. rendered={rendered} skipped={skipped} failed={failed}')
