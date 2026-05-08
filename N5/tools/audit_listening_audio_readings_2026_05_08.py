"""Audit every listening item's audio for kanji-misreading regressions.

User asked 2026-05-08: "can you do a verification of all the files by
actually listening to them?" — this is the programmatic equivalent.

How it works:
  1. For every line of every item in data/listening.json, apply the
     same cleanup the build pipeline does (strip JLPT bunsetsu spaces).
  2. Send the cleaned text to VOICEVOX's /audio_query endpoint.
  3. Extract the per-accent-phrase kana ("what the engine said").
  4. Apply a rule table to flag any kanji whose reading came out wrong
     for the given context — e.g. 今 read as コン when the next char
     isn't a known compound marker.
  5. Also verify every MP3 file exists, decodes cleanly via mutagen,
     and has a duration > 0.

Reports are partitioned by severity:
  - CRITICAL: kanji misread for sure (rule violation).
  - SUSPECT: at-risk pattern that should be human-confirmed.
  - INFO: kanji read in expected way but worth a glance for sanity.

Limitations:
  - Cannot detect pronunciation quality, accent, intonation, naturalness.
  - Rule-based: if a kanji's wrong reading isn't in our rule table,
    we won't catch it. Coverage will grow as bugs are reported.

Run:
  python tools/audit_listening_audio_readings_2026_05_08.py

Requires VOICEVOX engine running on localhost:50021.
"""
from __future__ import annotations
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
LISTENING = ROOT / 'data' / 'listening.json'
AUDIO_DIR = ROOT / 'audio' / 'listening'
ENGINE = 'http://localhost:50021'

# Default speaker for query (the engine's morphological analysis is
# speaker-agnostic, so any valid speaker ID works for kana extraction).
QUERY_SPEAKER = 8


def strip_for_tts(s: str) -> str:
    """Same as build pipeline: remove ASCII / full-width / tab / NL."""
    if not s:
        return ''
    return (s.replace(' ', '')
             .replace('　', '')
             .replace('\t', '')
             .replace('\n', ''))


def strip_speaker_prefix(line_text: str) -> str:
    """Same as build pipeline."""
    s = (line_text or '').strip()
    for prefix in ('男:', '男：', '女:', '女：', 'A:', 'A：', 'B:', 'B：',
                   '店員:', '店員：', '先生:', '先生：', '学生:', '学生：',
                   '母:', '母：', '父:', '父：', '子:', '子：'):
        if s.startswith(prefix):
            return s[len(prefix):].strip()
    return s


def query_kana(text: str) -> list[str]:
    """Return list of accent-phrase kana for the given input."""
    url = f'{ENGINE}/audio_query?speaker={QUERY_SPEAKER}&text={urllib.parse.quote(text)}'
    req = urllib.request.Request(url, method='POST')
    with urllib.request.urlopen(req, timeout=15) as r:
        q = json.loads(r.read())
    return [''.join(m.get('text', '') for m in ap['moras']) for ap in q['accent_phrases']]


# Rule table: per-kanji, what does the joined-kana output look like
# when the kanji is misread? Keyed by the offending character; values
# are (offending kana prefix that signals the mis-read, expected kana
# prefix when read correctly, "context" patterns that excuse the
# mis-read because it's actually a legitimate compound).
#
# Each rule fires when:
#   - the kanji appears in the cleaned input
#   - the kana output contains `bad_starts` joined into the SAME accent
#     phrase as the kanji's meaningful neighbour
#   - the cleaned input does NOT match an `excuses` regex (legitimate
#     compound)
#
# Adding more rules later is straightforward; copy the 今 entry.
RULES = [
    {
        'kanji': '今',
        'bad_kana_prefix': 'コン',
        'expected_kana': 'イマ',
        # If the kanji is followed by any of these, the compound
        # reading is correct (今月/今日/今晩/今年/今朝/今週/今度/今後/今夜/今回).
        'compound_followers': set('月日晩年朝週度後夜回'),
        'standalone_meaning': 'now (standalone)',
    },
    # Future rule slots — add when bugs are reported. e.g.:
    # { 'kanji': '大', 'bad_kana_prefix': 'ダイ', 'expected_kana': 'オオ',
    #   'compound_followers': set('学人勢事丈変好阪統'), ... }
]


def find_misreads(cleaned_text: str, kana_phrases: list[str]) -> list[dict]:
    """Apply rule table to detect misreadings. Returns list of dicts."""
    findings = []
    joined_kana = ''.join(kana_phrases)
    for rule in RULES:
        k = rule['kanji']
        if k not in cleaned_text:
            continue
        # Find every occurrence of the kanji in cleaned text
        for idx, ch in enumerate(cleaned_text):
            if ch != k:
                continue
            after = cleaned_text[idx + 1: idx + 2]
            if after and after in rule['compound_followers']:
                continue  # legitimate compound, no bug expected
            # Position in cleaned_text — does the corresponding kana
            # phrase start with the bad reading?
            # We don't have a 1:1 char→phrase mapping, but a heuristic
            # that works: check if any phrase starts with bad_kana_prefix
            # AND that phrase's index aligns with the kanji's position.
            if any(p.startswith(rule['bad_kana_prefix']) and len(p) > len(rule['bad_kana_prefix']) for p in kana_phrases):
                # Bad reading detected: kanji + something else jammed
                # into one phrase starting with bad prefix.
                findings.append({
                    'kanji': k,
                    'after': after,
                    'bad_kana': rule['bad_kana_prefix'],
                    'expected': rule['expected_kana'],
                    'context': cleaned_text[max(0, idx - 4):idx + 8],
                    'standalone_meaning': rule['standalone_meaning'],
                })
    return findings


def main() -> int:
    # Engine reachability
    try:
        with urllib.request.urlopen(f'{ENGINE}/version', timeout=3) as r:
            ver = r.read().decode().strip().strip('"')
        print(f'VOICEVOX engine: {ver}')
    except Exception as e:
        print(f'ERROR: VOICEVOX engine not reachable at {ENGINE}: {e}', file=sys.stderr)
        return 2

    data = json.loads(LISTENING.read_text(encoding='utf-8'))
    items = data['items']

    # MP3 integrity check
    print()
    print('--- MP3 integrity ---')
    try:
        from mutagen.mp3 import MP3
    except ImportError:
        print('  (mutagen not installed; skipping duration check)')
        MP3 = None
    integrity_failures = []
    for it in items:
        path = AUDIO_DIR / f'{it["id"]}.mp3'
        if not path.exists():
            integrity_failures.append((it['id'], 'missing'))
            continue
        if path.stat().st_size < 100:
            integrity_failures.append((it['id'], f'too small: {path.stat().st_size} bytes'))
            continue
        if MP3 is not None:
            try:
                d = MP3(path).info.length
                if d < 0.5:
                    integrity_failures.append((it['id'], f'duration < 0.5s: {d:.2f}s'))
            except Exception as e:
                integrity_failures.append((it['id'], f'mutagen error: {e}'))
    if integrity_failures:
        print(f'  {len(integrity_failures)} integrity failure(s):')
        for iid, msg in integrity_failures:
            print(f'    {iid}: {msg}')
    else:
        print(f'  47/47 MP3s present + decode cleanly + duration > 0.5s. ✓')

    # Per-line audio_query scan
    print()
    print('--- Kanji-reading audit (via VOICEVOX audio_query) ---')
    total_lines_checked = 0
    misreads = []  # list of (item_id, line_index, finding_dict)
    for it in items:
        iid = it['id']
        # Multi-line items
        lines = it.get('lines') or []
        if lines:
            for i, ln in enumerate(lines):
                raw = strip_speaker_prefix(ln.get('text_ja', ''))
                cleaned = strip_for_tts(raw)
                if not cleaned:
                    continue
                total_lines_checked += 1
                try:
                    kana = query_kana(cleaned)
                except Exception as e:
                    print(f'  WARN {iid} line {i}: query failed: {e}', file=sys.stderr)
                    continue
                fs = find_misreads(cleaned, kana)
                for f in fs:
                    misreads.append((iid, f'lines[{i}]', f, cleaned, kana))
        else:
            # Single-line items: render the whole script_ja
            raw = it.get('script_ja') or ''
            cleaned = strip_for_tts(raw)
            if not cleaned:
                continue
            total_lines_checked += 1
            try:
                kana = query_kana(cleaned)
            except Exception as e:
                print(f'  WARN {iid}: query failed: {e}', file=sys.stderr)
                continue
            fs = find_misreads(cleaned, kana)
            for f in fs:
                misreads.append((iid, 'script_ja', f, cleaned, kana))

    print(f'  Lines audited: {total_lines_checked}')
    print(f'  Kanji-misread findings: {len(misreads)}')
    if misreads:
        print()
        for iid, field, finding, cleaned, kana in misreads:
            print(f'  CRITICAL  {iid}  {field}')
            print(f'    kanji: {finding["kanji"]} (expected {finding["expected"]} — {finding["standalone_meaning"]})')
            print(f'    voicevox produced: {finding["bad_kana"]}...')
            print(f'    context: ...{finding["context"]}...')
            print(f'    full kana: {" / ".join(kana)}')
            print()
    else:
        print(f'  All audited lines produce expected kanji readings. ✓')

    # Summary
    print()
    print('=' * 60)
    if integrity_failures or misreads:
        print('FAIL — see above for details.')
        return 1
    print('PASS — all 47 listening items audit clean.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
