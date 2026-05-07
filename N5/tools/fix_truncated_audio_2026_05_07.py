"""User-reported audio truncation: example sentences cut at the first
comma / sentence-internal pause produced half-truncated MP3s in the
gtts batch render. The user's screenshot showed
"コーヒーは 飲みますが、にくは たべません。" (audio/grammar/n5-002.2.mp3)
playing only the first clause.

Detection: scan all grammar / vocab / reading / question audio files;
flag any where (morae / duration_sec) > 5.5 (well above gtts default
~4 morae/sec pace). For each flagged file, re-render fresh via gtts;
if the fresh render is ≥ 20% longer than the cached file, replace it.
That ratio test catches genuine truncation while leaving naturally-
fast renders (e.g., short emphatic sentences) untouched.

Idempotent: re-runs are no-ops if all flagged files have been replaced.
"""
from __future__ import annotations
import sys, io, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path
from mutagen.mp3 import MP3
from gtts import gTTS

ROOT = Path(__file__).parent.parent
MANIFEST = ROOT / 'data' / 'audio_manifest.json'

SMALL = set('ゃゅょぁぃぅぇぉっゎャュョァィゥェォッヮ')
def count_morae(s: str) -> int:
    n = 0
    for c in s or '':
        cp = ord(c)
        if 0x3041 <= cp <= 0x3096 or 0x30A1 <= cp <= 0x30FA:
            if c not in SMALL: n += 1
        elif c == 'ー':
            n += 1
        elif 0x4E00 <= cp <= 0x9FFF:
            n += 2
    return n


def text_for_id(audio_id: str, corpus: dict) -> str | None:
    parts = audio_id.split('.')
    if parts[0] == 'grammar' and len(parts) >= 3:
        pid, idx = parts[1], int(parts[2])
        for p in corpus['grammar']:
            if p['id'] == pid and idx < len(p.get('examples', [])):
                return p['examples'][idx].get('ja', '')
    elif parts[0] == 'vocab' and len(parts) >= 3:
        # vocab.<entry-id>.<idx>
        entry_id = '.'.join(parts[1:-1])
        try: idx = int(parts[-1])
        except ValueError: return None
        for w in corpus['vocab']:
            if w.get('id') == entry_id and idx < len(w.get('examples', [])):
                return w['examples'][idx].get('ja', '')
    elif parts[0] == 'reading' and len(parts) >= 2:
        rid = '.'.join(parts[1:])
        for p in corpus['reading']:
            if p.get('id') == rid:
                return p.get('ja', '')
    elif parts[0] == 'question' and len(parts) >= 2:
        qid = '.'.join(parts[1:])
        for x in corpus['questions']:
            if x.get('id') == qid:
                return x.get('question_ja') or x.get('prompt_ja', '')
    return None


def main() -> int:
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    corpus = {
        'grammar': json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))['patterns'],
        'vocab': json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))['entries'],
        'reading': json.loads((ROOT / 'data' / 'reading.json').read_text(encoding='utf-8'))['passages'],
        'questions': json.loads((ROOT / 'data' / 'questions.json').read_text(encoding='utf-8'))['questions'],
    }

    flagged = []
    for it in manifest['items']:
        p = ROOT / it['path']
        if not p.exists(): continue
        txt = text_for_id(it['id'], corpus)
        if txt is None or len(txt) < 5: continue
        try:
            dur = MP3(p).info.length
        except Exception:
            continue
        morae = count_morae(txt)
        if morae < 4 or dur < 0.5: continue
        rate = morae / dur
        if rate > 5.5:
            flagged.append((it, p, txt, dur, morae, rate))

    print(f'Flagged for re-render: {len(flagged)}')

    rerendered = 0
    skipped_close = 0
    failures = 0
    for it, p, txt, orig_dur, morae, rate in flagged:
        # Render fresh to a temp path
        try:
            fresh = gTTS(txt, lang='ja')
            tmp_path = p.with_suffix('.tmp.mp3')
            fresh.save(str(tmp_path))
            new_dur = MP3(tmp_path).info.length
        except Exception as e:
            print(f'  FAIL {it["id"]}: {e}')
            failures += 1
            continue

        # If fresh is ≥20% longer than cached, replace
        if new_dur > orig_dur * 1.20:
            tmp_path.replace(p)
            rerendered += 1
            print(f'  RE-RENDER {it["id"]:<32}  {orig_dur:.2f}s → {new_dur:.2f}s  (+{new_dur-orig_dur:.2f}s)')
        else:
            tmp_path.unlink()
            skipped_close += 1
            print(f'  SKIP      {it["id"]:<32}  {orig_dur:.2f}s ≈ fresh {new_dur:.2f}s (within 20%)')
        time.sleep(0.1)  # gentle rate-limit on Google's TTS endpoint

    print(f'\nSummary:')
    print(f'  re-rendered: {rerendered}')
    print(f'  skipped (already fine): {skipped_close}')
    print(f'  failures: {failures}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
