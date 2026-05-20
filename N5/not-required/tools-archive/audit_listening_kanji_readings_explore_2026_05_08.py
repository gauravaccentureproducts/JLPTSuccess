"""Exploratory pass: dump every kanji's reading as VOICEVOX produced it,
across all 132 lines of all 47 listening items, so a human reviewer can
spot misreadings my rule table doesn't yet catch.

Output is grouped by kanji so the reviewer can see if a single kanji is
ever read inconsistently. Companion to:

    tools/audit_listening_audio_readings_2026_05_08.py

(which is the rule-driven version that flags definite bugs).

Run:
  python tools/audit_listening_kanji_readings_explore_2026_05_08.py
"""
from __future__ import annotations
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from collections import defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
LISTENING = ROOT / 'data' / 'listening.json'
ENGINE = 'http://localhost:50021'
QUERY_SPEAKER = 8


def strip_for_tts(s: str) -> str:
    if not s:
        return ''
    return s.replace(' ', '').replace('　', '').replace('\t', '').replace('\n', '')


def strip_speaker_prefix(s: str) -> str:
    s = (s or '').strip()
    for prefix in ('男:', '男：', '女:', '女：', 'A:', 'A：', 'B:', 'B：',
                   '店員:', '店員：', '先生:', '先生：', '学生:', '学生：',
                   '母:', '母：', '父:', '父：', '子:', '子：'):
        if s.startswith(prefix):
            return s[len(prefix):].strip()
    return s


def query_full(text: str) -> dict:
    url = f'{ENGINE}/audio_query?speaker={QUERY_SPEAKER}&text={urllib.parse.quote(text)}'
    req = urllib.request.Request(url, method='POST')
    with urllib.request.urlopen(req, timeout=15) as r:
        return json.loads(r.read())


KANJI_RE = re.compile(r'[一-鿿]')


def main() -> int:
    data = json.loads(LISTENING.read_text(encoding='utf-8'))
    items = data['items']

    # kanji -> set of (kana_phrase_containing_it, item_id, snippet)
    by_kanji = defaultdict(list)
    total_lines = 0
    skipped = 0

    for it in items:
        iid = it['id']
        lines = it.get('lines') or []
        sources = []
        if lines:
            for i, ln in enumerate(lines):
                sources.append((f'lines[{i}]', strip_speaker_prefix(ln.get('text_ja', ''))))
        else:
            sources.append(('script_ja', it.get('script_ja') or ''))

        for field, raw in sources:
            cleaned = strip_for_tts(raw)
            if not cleaned:
                continue
            kanji_in_line = set(KANJI_RE.findall(cleaned))
            if not kanji_in_line:
                continue
            total_lines += 1
            try:
                q = query_full(cleaned)
            except Exception as e:
                skipped += 1
                continue
            phrases = [''.join(m.get('text', '') for m in ap['moras']) for ap in q['accent_phrases']]
            joined = ' / '.join(phrases)
            for k in kanji_in_line:
                # Tiny snippet around the kanji
                idx = cleaned.find(k)
                snippet = cleaned[max(0, idx - 3):idx + 5]
                by_kanji[k].append((iid, field, snippet, joined))

    print(f'Lines audited: {total_lines}; skipped: {skipped}')
    print(f'Distinct kanji observed: {len(by_kanji)}')
    print()
    print('Per-kanji readings (one row per occurrence). Kanji with multiple')
    print('observations are sorted to surface inconsistencies. Look for any')
    print('row where the joined kana looks wrong for the snippet context.')
    print()
    print(f'{"kanji":<6} {"item":<20} {"field":<16} {"snippet":<14} kana')
    print('-' * 110)
    for k in sorted(by_kanji.keys(), key=lambda x: (-len(by_kanji[x]), x)):
        rows = by_kanji[k]
        for iid, field, snippet, kana in rows:
            print(f'{k:<6} {iid:<20} {field:<16} {snippet:<14} {kana}')
        print()
    return 0


if __name__ == '__main__':
    sys.exit(main())
