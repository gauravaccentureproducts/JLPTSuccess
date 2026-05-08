"""Q41 (decision: top-50 + normalize): vocab `counter` field.

Two-part fix:
  1. Normalize the legacy romaji-style counters ('satsu', 'dai',
     'mai', 'hon', 'nin', 'tsu', 'ko', 'kai') to their canonical
     kanji form so the renderer's _counterKana() lookup is the
     ONLY source of romaji translation.
  2. Add the `counter` field to ~30 high-frequency N5 nouns that
     are commonly counted but were missing the field. Combined with
     existing 68 entries, lifts coverage past 100/589 (~17%) — the
     practically-useful subset (most remaining nouns don't take a
     specific counter, e.g. 雨, weather, time durations).

Idempotent: skips entries that already have the canonical counter set.
"""
from __future__ import annotations
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

VOCAB = Path(__file__).parent.parent / 'data' / 'vocab.json'

# Romaji → kanji canonical (per the N5 counter taxonomy in the spec).
ROMAJI_TO_KANJI = {
    'satsu': '冊',  # books / volumes
    'dai':   '台',  # machines / vehicles
    'mai':   '枚',  # flat objects (paper, dishes)
    'hon':   '本',  # long objects (pens, bottles, trees)
    'nin':   '人',  # people
    'tsu':   'つ',  # native generic counter (1-10)
    'ko':    '個',  # generic small objects
    'kai':   '回',  # times / occurrences
    'do':    '度',  # times / degrees
    'fun':   '分',  # minutes
    'ji':    '時',  # hours
    'ken':   '軒',  # houses / shops
    'soku':  '足',  # footwear pairs
    'wa':    '羽',  # birds
    'hiki':  '匹',  # small animals
}

# Additional nouns + their canonical counter. Each value is the
# kanji-or-kana counter character that the renderer's _counterKana()
# already knows how to turn into ふりがな furigana on display.
NEW_COUNTERS = {
    # People (高 frequency, counter 人)
    'がくせい': '人',    # student
    '先生': '人',         # teacher
    'ともだち': '人',    # friend
    '父': '人',          # father
    '母': '人',          # mother
    'おとうさん': '人',  # someone else's father
    'おかあさん': '人',  # someone else's mother
    'あに': '人',        # older brother (own)
    'あね': '人',        # older sister (own)
    'おとうと': '人',    # younger brother
    'いもうと': '人',    # younger sister
    '男': '人',          # man (also 男の人)
    '女': '人',          # woman
    'こども': '人',      # child
    'おとな': '人',      # adult
    'みなさん': '人',    # everyone
    # Objects — long things (本)
    '木': '本',          # tree
    'はし': '本',        # chopsticks (one pair = 一膳, but 一本 colloq.)
    # Flat things (枚)
    'コピー': '枚',      # copy / sheet
    # Books / magazines (冊)
    'ざっし': '冊',      # magazine
    'ほん': '冊',        # book (kana variant)
    # Generic counter for small objects (個)
    'おにぎり': '個',    # rice ball
    'ケーキ': '個',      # cake
    'おかし': '個',      # snack / sweets
    'パン': '個',        # bread
    'おべんとう': '個',  # bento
    # Houses / shops (軒)
    'うち': '軒',        # house (own)
    'いえ': '軒',        # house
    'みせ': '軒',        # shop
    'おみせ': '軒',      # shop (polite)
    # Floors / rooms — typically use the noun itself or 〜階 / 〜室
    'へや': '部屋',       # room (counter is 部屋 itself, written verbatim)
    # Vehicles (台)
    'ひこうき': '台',    # airplane
    # Vague generic (つ — for 1-9 native-counter usage)
    'たまご': '個',      # already 個 in some lists
}


def main() -> int:
    doc = json.loads(VOCAB.read_text(encoding='utf-8'))
    entries = doc['entries']

    by_form_reading = {}
    for w in entries:
        by_form_reading.setdefault(w.get('reading'), []).append(w)

    # Phase 1: normalize romaji counters
    n_normalized = 0
    for w in entries:
        c = w.get('counter')
        if c in ROMAJI_TO_KANJI:
            w['counter'] = ROMAJI_TO_KANJI[c]
            n_normalized += 1

    # Phase 2: add counter to new entries (matched by reading; skip if
    # the entry already has counter set — idempotent).
    n_added = 0
    n_no_match = 0
    for reading, counter_val in NEW_COUNTERS.items():
        matches = by_form_reading.get(reading, [])
        if not matches:
            n_no_match += 1
            continue
        # Pick the FIRST matching entry that doesn't already have counter
        for w in matches:
            if not w.get('counter'):
                w['counter'] = counter_val
                n_added += 1
                break
        # else: all matches already have counter — skip silently

    VOCAB.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )

    # Verify
    doc2 = json.loads(VOCAB.read_text(encoding='utf-8'))
    nouns = [w for w in doc2['entries'] if w.get('pos') == 'noun']
    have_counter = sum(1 for w in nouns if w.get('counter'))
    # Distribution of counters
    from collections import Counter
    dist = Counter(w['counter'] for w in nouns if w.get('counter'))
    print(f'Romaji counters normalized: {n_normalized}')
    print(f'New counter entries added:  {n_added}')
    print(f'No match (skipped):         {n_no_match}')
    print(f'\nFinal noun coverage: {have_counter}/{len(nouns)} ({100*have_counter/len(nouns):.1f}%)')
    print(f'Counter distribution:')
    for c, n in dist.most_common():
        print(f'  {c}: {n}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
