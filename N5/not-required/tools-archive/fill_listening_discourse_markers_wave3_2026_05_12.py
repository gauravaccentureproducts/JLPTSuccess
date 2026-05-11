"""Wave 3 — pick up the last 10 listening items via whitespace-
normalized scan + expanded marker inventory.

Wave 1+2 = 40/50. The 10 remaining items have set-phrase markers
split by whitespace (e.g., "おはよう ございます" with a space)
that exact-match scanning missed. This wave normalizes whitespace
and adds a few more markers seen in the remaining items
(いいですね / いいえ / ましょう as suggestion / じゃ-prompt).
"""
from __future__ import annotations
import io, json, re, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Same inventory, but matched against whitespace-normalized text.
# Tokens stored WITHOUT internal whitespace; the scan normalizes the
# search text the same way.
MARKERS = [
    ('どうもありがとうございます', 'politeness'),
    ('ありがとうございました', 'politeness'),
    ('ありがとうございます', 'politeness'),
    ('どういたしまして', 'politeness'),
    ('いらっしゃいませ', 'politeness'),
    ('おはようございます', 'politeness'),
    ('しつれいします', 'politeness'),
    ('いただきます', 'politeness'),
    ('ごちそうさまでした', 'politeness'),
    ('ごちそうさま', 'politeness'),
    ('おじゃまします', 'politeness'),
    ('おねがいします', 'politeness'),
    ('おはよう', 'politeness'),
    ('よろしく', 'politeness'),
    ('すみません', 'politeness'),
    ('どうぞ', 'politeness'),
    # Agreement / aizuchi
    ('そうなんですか', 'agreement'),
    ('そうですか', 'agreement'),
    ('そうですね', 'agreement'),
    ('いいですね', 'agreement'),
    ('なるほど', 'aizuchi'),
    ('わかりました', 'aizuchi'),
    ('いいえ', 'aizuchi'),
    # Topic-shift
    ('それでは', 'topic-shift'),
    ('ところで', 'topic-shift'),
    ('じゃあ', 'topic-shift'),
    ('じゃ', 'topic-shift'),
    ('では', 'topic-shift'),
    # Fillers
    ('えーと', 'filler'),
    ('えーっと', 'filler'),
    ('うーん', 'filler'),
    ('そのー', 'filler'),
    ('あのー', 'filler'),
    # Conjunctions
    ('そして', 'conjunction'),
    ('それから', 'conjunction'),
    ('だから', 'conjunction'),
    ('でも', 'conjunction'),
    ('けど', 'conjunction'),
    # Short
    ('はい', 'aizuchi'),
    ('うん', 'aizuchi'),
    ('ええ', 'aizuchi'),
    ('そう', 'agreement'),
    ('あの', 'filler'),
    ('へぇ', 'aizuchi'),
    ('ヘえ', 'aizuchi'),
    # Suggestion / volitional
    ('ましょう', 'suggestion'),
    # Emphasis
    ('やっぱり', 'emphasis'),
    ('やはり', 'emphasis'),
    ('もちろん', 'emphasis'),
    ('ぜひ', 'emphasis'),
]


def normalize(s: str) -> str:
    """Strip whitespace so multi-word set phrases match across spaces."""
    return re.sub(r'\s+', '', s)


def scan(text: str) -> list[dict]:
    if not text:
        return []
    norm = normalize(text)
    found = {}
    work = norm
    for tok, cat in MARKERS:
        cnt = work.count(tok)
        if cnt > 0:
            found[tok] = {'token': tok, 'category': cat, 'count': cnt}
            work = work.replace(tok, ' ' * len(tok))
    return list(found.values())


def main() -> int:
    fp = ROOT / 'data' / 'listening.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_discourse_wave3')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')
    data = json.loads(fp.read_text(encoding='utf-8'))
    n = 0
    for it in data['items']:
        if it.get('discourse_markers_used'):
            continue
        text = ' '.join([
            it.get('script_ja') or '',
            it.get('prompt_ja') or '',
            it.get('correctAnswer') or '',
            ' '.join(it.get('choices') or []),
        ])
        hits = scan(text)
        if not hits:
            continue
        it['discourse_markers_used'] = hits
        it['discourse_markers_used_provenance'] = 'auto_derived'
        n += 1
    print(f'\nWave 3 added discourse_markers_used on {n} more items.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
