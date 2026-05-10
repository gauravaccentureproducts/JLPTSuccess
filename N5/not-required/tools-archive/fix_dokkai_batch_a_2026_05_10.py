"""Dokkai Batch A:
- D1: render audio for 14 missing reading passages
- D3: populate vocab_preview on 9 passages missing it (auto-derived)
- D2: skeleton grammar_footnotes on 11 passages missing them
"""
from __future__ import annotations
import io, json, sys, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

reading_path = ROOT / 'data' / 'reading.json'
data = json.loads(reading_path.read_text(encoding='utf-8'))
passages = data['passages']

# --- D1: Render audio for missing passages ---
print('=== D1: Audio rendering for missing passages ===')
import gtts
AUDIO_DIR = ROOT / 'audio' / 'reading'
AUDIO_DIR.mkdir(parents=True, exist_ok=True)

rendered = 0
failures = []
for p in passages:
    if p.get('audio'):
        continue
    pid = p['id']
    ja = p.get('ja') or ''
    if not ja:
        continue
    audio_rel = f'audio/reading/{pid}.mp3'
    audio_abs = ROOT / audio_rel
    if not audio_abs.exists():
        try:
            tts = gtts.gTTS(text=ja, lang='ja', slow=False)
            tts.save(str(audio_abs))
        except Exception as e:
            failures.append((pid, str(e)))
            continue
    p['audio'] = audio_rel
    rendered += 1
    print(f'  rendered: {pid}')

print(f'Rendered: {rendered}, failures: {len(failures)}')

# --- D3: Auto-derive vocab_preview ---
print()
print('=== D3: vocab_preview backfill ===')
V = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))['entries']

# Build form/reading -> entry map (longest-first for greedy match)
form_to_entry = {}
for e in V:
    form = e.get('form')
    reading = e.get('reading')
    if form: form_to_entry.setdefault(form, e)
    if reading and reading != form: form_to_entry.setdefault(reading, e)

forms_by_len = sorted(form_to_entry.keys(), key=lambda s: -len(s))

# Skip set — overly common particles / function words (would balloon every preview)
SKIP = {'は','が','を','に','へ','で','と','の','も','や','か','ね','よ','です','ます',
        'これ','それ','あれ','どれ','この','その','あの','どの','ここ','そこ','あそこ',
        'わたし','私','です','ます'}

backfilled = 0
for p in passages:
    if p.get('vocab_preview'):
        continue
    ja = p.get('ja') or ''
    if not ja:
        continue
    seen = set()
    preview = []
    for f in forms_by_len:
        if f in SKIP: continue
        if len(f) < 2: continue
        if f in ja and f not in seen:
            seen.add(f)
            entry = form_to_entry[f]
            preview.append({
                'form': entry.get('form'),
                'reading': entry.get('reading'),
                'gloss': entry.get('gloss'),
                'gloss_hi': entry.get('gloss_hi'),
                'vocab_id': entry.get('id'),
            })
            if len(preview) >= 12: break
    if preview:
        # Sort by appearance order in ja text
        def first_pos(item):
            return ja.find(item['form']) if item['form'] in ja else (
                ja.find(item['reading']) if item['reading'] else 999_999)
        preview.sort(key=first_pos)
        p['vocab_preview'] = preview
        p['vocab_preview_provenance'] = 'auto_derived'
        backfilled += 1

print(f'  Backfilled: {backfilled}')

# --- D2: Grammar footnotes skeleton ---
# For passages without grammar_footnotes, scan for known pattern signatures
# and tag the sentence position.
print()
print('=== D2: grammar_footnotes skeleton backfill ===')
G = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))['patterns']

# Build pattern surface form → pattern id
PATTERN_SIGNATURES = []
for p in G:
    pat = p.get('pattern','').replace('〜','').replace('～','').strip()
    if pat and len(pat) >= 2:
        PATTERN_SIGNATURES.append((pat, p['id'], p.get('meaning_en','')))

footnotes_added = 0
for p in passages:
    if p.get('grammar_footnotes'):
        continue
    ja = p.get('ja') or ''
    if not ja:
        continue
    # Per-sentence: split on 。
    sentences = [s for s in ja.replace('\n','。').split('。') if s.strip()]
    footnotes = []
    for i, s in enumerate(sentences):
        s_patterns = []
        for pat_surface, pid, meaning in PATTERN_SIGNATURES:
            if len(pat_surface) >= 2 and pat_surface in s:
                s_patterns.append({'pattern_id': pid, 'surface': pat_surface, 'gloss': meaning[:60]})
        # Take top 3 by surface length (most specific)
        s_patterns.sort(key=lambda x: -len(x['surface']))
        if s_patterns[:3]:
            footnotes.append({
                'sentence_idx': i,
                'sentence_ja': s.strip()[:80],
                'patterns': s_patterns[:3],
            })
    if footnotes:
        p['grammar_footnotes'] = footnotes
        p['grammar_footnotes_provenance'] = 'auto_derived'
        footnotes_added += 1

print(f'  Backfilled: {footnotes_added}')

reading_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final
total = len(passages)
audio = sum(1 for p in passages if p.get('audio'))
vp = sum(1 for p in passages if p.get('vocab_preview'))
gf = sum(1 for p in passages if p.get('grammar_footnotes'))
print()
print('=== FINAL ===')
print(f'audio:               {audio}/{total}')
print(f'vocab_preview:       {vp}/{total}')
print(f'grammar_footnotes:   {gf}/{total}')
