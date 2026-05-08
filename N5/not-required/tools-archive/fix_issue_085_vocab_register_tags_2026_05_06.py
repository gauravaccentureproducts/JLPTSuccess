"""ISSUE-085 (round-8 deferred → fixed 2026-05-06): vocab register tags.

The earlier batch-C attempt had a form/reading key mismatch on 30 keigo
entries. This pass scans by reading-only AND adds register tags on the
broader set of family / register-marked vocab.

Coverage extends register tag from 4 → ~25 entries:
  - Humble (謙譲) family terms: 父, 母, 兄, 姉, 弟, 妹, 祖父, 祖母
  - Respectful (尊敬) family terms: お父さん, お母さん, お兄さん,
    お姉さん, おとうと-related-だんさん, etc.
  - Casual sentence-final particles where applicable on vocab
  - Polite set phrases: お願い, 失礼, おはよう, こんにちは

Idempotent.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
VF = ROOT / 'data' / 'vocab.json'

# (reading) -> register
# Reading is the primary key since most vocab.json entries store form==reading
# for kana-only words. Family members in N5 follow strict humble/respectful split.
REGISTER_BY_READING = {
    # === Humble (謙譲) — speaker referring to own family ===
    'ちち': 'humble',
    'はは': 'humble',
    'あに': 'humble',
    'あね': 'humble',
    'おとうと': 'humble',
    'いもうと': 'humble',
    'そふ': 'humble',
    'そぼ': 'humble',
    # === Respectful (尊敬) — speaker referring to other-family or addressing ===
    'おとうさん': 'respectful',
    'おかあさん': 'respectful',
    'おにいさん': 'respectful',
    'おねえさん': 'respectful',
    'おじいさん': 'respectful',
    'おばあさん': 'respectful',
    'おじさん': 'respectful',
    'おばさん': 'respectful',
    # === Honorific verbs (尊敬語) ===
    'いらっしゃる': 'respectful',
    'めしあがる': 'respectful',
    'ごらんになる': 'respectful',
    'おっしゃる': 'respectful',
    'なさる': 'respectful',
    # === Humble verbs (謙譲語) ===
    'おる': 'humble',
    'いただく': 'humble',
    'はいけんする': 'humble',
    'まいる': 'humble',
    'うかがう': 'humble',
    'もうす': 'humble',
    'いたす': 'humble',
    # === Polite set phrases ===
    'おねがいします': 'polite',
    'しつれいします': 'polite',
    'おはようございます': 'polite',
    'ありがとうございます': 'polite',
    'すみません': 'polite',
    'おねがい': 'polite',
    'おげんき': 'polite',
    'おさきに': 'polite',
    'しつれい': 'polite',
    # === Casual ===
    'じゃん': 'casual',
    'なあ': 'casual',
    'けど': 'casual',
}


def main() -> int:
    data = json.loads(VF.read_text(encoding='utf-8'))
    n_added = 0
    n_skipped_already = 0

    for e in data.get('entries', []):
        reading = e.get('reading')
        if reading not in REGISTER_BY_READING:
            continue
        new_reg = REGISTER_BY_READING[reading]
        cur = e.get('register')
        if cur == new_reg:
            n_skipped_already += 1
            continue
        e['register'] = new_reg
        n_added += 1

    VF.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    total = len(data.get('entries', []))
    nR = sum(1 for e in data['entries'] if e.get('register'))
    from collections import Counter
    rs_dist = Counter(e.get('register') for e in data['entries'] if e.get('register'))
    print(f'[ISSUE-085] Vocab register tags')
    print(f'  writes:               {n_added}')
    print(f'  already correct:      {n_skipped_already}')
    print(f'  total tagged:         {nR}/{total}')
    print(f'  distribution:         {dict(rs_dist)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
