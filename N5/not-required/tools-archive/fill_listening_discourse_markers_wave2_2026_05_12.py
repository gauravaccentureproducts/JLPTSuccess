"""Wave 2 — extend discourse_markers_used to single-utterance items.

Wave 1 (2026-05-11) tagged 28 dialog items by scanning script_ja.
The 22 remaining items are utterance_expression / immediate_response
type — their script_ja is just context, not transcript. But their
PROMPT_JA + CORRECT_ANSWER fields often contain set-phrase / polite
discourse markers (the entire genre of this question type).

This wave scans those fields too, so set-phrase markers (おはよう
ございます, すみません, いらっしゃいませ, ありがとうございました
etc.) get tagged on the single-utterance items where they appear.

Same inventory as wave 1.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

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
    ('よろしく', 'politeness'),
    ('すみません', 'politeness'),
    ('どうぞ', 'politeness'),
    ('そうなんですか', 'agreement'),
    ('そうですか', 'agreement'),
    ('そうですね', 'agreement'),
    ('なるほど', 'aizuchi'),
    ('わかりました', 'aizuchi'),
    ('それでは', 'topic-shift'),
    ('ところで', 'topic-shift'),
    ('じゃあ', 'topic-shift'),
    ('では', 'topic-shift'),
    ('えーと', 'filler'),
    ('えーっと', 'filler'),
    ('うーん', 'filler'),
    ('そのー', 'filler'),
    ('あのー', 'filler'),
    ('そして', 'conjunction'),
    ('それから', 'conjunction'),
    ('だから', 'conjunction'),
    ('でも', 'conjunction'),
    ('けど', 'conjunction'),
    ('はい', 'aizuchi'),
    ('うん', 'aizuchi'),
    ('ええ', 'aizuchi'),
    ('そう', 'agreement'),
    ('あの', 'filler'),
    ('へぇ', 'aizuchi'),
    ('ヘえ', 'aizuchi'),
    ('やっぱり', 'emphasis'),
    ('やはり', 'emphasis'),
    ('もちろん', 'emphasis'),
    ('ぜひ', 'emphasis'),
]


def scan(text: str) -> list[dict]:
    if not text:
        return []
    found = {}
    work = text
    for tok, cat in MARKERS:
        cnt = work.count(tok)
        if cnt > 0:
            found[tok] = {'token': tok, 'category': cat, 'count': cnt}
            work = work.replace(tok, ' ' * len(tok))
    return list(found.values())


def main() -> int:
    fp = ROOT / 'data' / 'listening.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_discourse_wave2')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')
    data = json.loads(fp.read_text(encoding='utf-8'))
    n = 0
    for it in data['items']:
        if it.get('discourse_markers_used'):
            continue
        # Scan prompt + answer + script for single-utterance items
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
    print(f'\nWave 2 added discourse_markers_used on {n} more items (via prompt/answer/choices scan).')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
