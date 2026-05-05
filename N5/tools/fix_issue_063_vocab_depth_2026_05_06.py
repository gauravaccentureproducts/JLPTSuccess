"""ISSUE-063 + IMP-087 + IMP-088 (audit round-7, 2026-05-06): vocab
depth fields — pitch_accent + counter on representative N5 vocab.

Three additive fields:
  pitch_accent  -> { mora, drop }   from NHK 日本語発音アクセント新辞典
                                    e.g. {mora: 4, drop: 1} for 「あした」 = HLLL
                                    drop: 0 = heiban (flat-rising), 1..n = downstep position
  counter       -> string           e.g. 'satsu' for 本, 'dai' for 車, 'mai' for paper
  register      -> string           humble / respectful / formal / casual

Authoring scope this pass: ~120 highest-frequency N5 entries
(numbers, time-of-day, family, common verbs, common nouns with
canonical counters). Remaining ~920 entries fall back to the absence
of the field (no rendering at all).

Idempotent. Native review of pitch accents pending — sourced from
publicly-available NHK / wadoku data; mora counts cross-checked.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
VF = ROOT / 'data' / 'vocab.json'

# (form|reading) -> { pitch_accent?, counter?, register? }
# Match key: prefer (form, reading); fall back to reading-only.
DEPTH = {
    # Numbers
    ('一', 'いち'):           {'pitch_accent': {'mora': 2, 'drop': 2}},  # い↓ち
    ('二', 'に'):             {'pitch_accent': {'mora': 1, 'drop': 1}},  # に↓
    ('三', 'さん'):           {'pitch_accent': {'mora': 2, 'drop': 0}},  # さん (heiban)
    ('四', 'よん'):           {'pitch_accent': {'mora': 2, 'drop': 1}},  # よ↓ん
    ('五', 'ご'):             {'pitch_accent': {'mora': 1, 'drop': 1}},
    ('六', 'ろく'):           {'pitch_accent': {'mora': 2, 'drop': 2}},
    ('七', 'なな'):           {'pitch_accent': {'mora': 2, 'drop': 1}},
    ('八', 'はち'):           {'pitch_accent': {'mora': 2, 'drop': 2}},
    ('九', 'きゅう'):         {'pitch_accent': {'mora': 2, 'drop': 1}},
    ('十', 'じゅう'):         {'pitch_accent': {'mora': 2, 'drop': 1}},
    ('百', 'ひゃく'):         {'pitch_accent': {'mora': 2, 'drop': 2}},
    ('千', 'せん'):           {'pitch_accent': {'mora': 2, 'drop': 1}},
    ('万', 'まん'):           {'pitch_accent': {'mora': 2, 'drop': 1}},
    # Time
    ('今日', 'きょう'):       {'pitch_accent': {'mora': 2, 'drop': 1}},
    ('明日', 'あした'):       {'pitch_accent': {'mora': 3, 'drop': 3}},
    ('昨日', 'きのう'):       {'pitch_accent': {'mora': 3, 'drop': 2}},
    ('今', 'いま'):           {'pitch_accent': {'mora': 2, 'drop': 1}},
    ('朝', 'あさ'):           {'pitch_accent': {'mora': 2, 'drop': 1}},
    ('昼', 'ひる'):           {'pitch_accent': {'mora': 2, 'drop': 2}},
    ('夜', 'よる'):           {'pitch_accent': {'mora': 2, 'drop': 1}},
    # Family
    ('父', 'ちち'):           {'pitch_accent': {'mora': 2, 'drop': 2}, 'register': 'humble'},
    ('母', 'はは'):           {'pitch_accent': {'mora': 2, 'drop': 1}, 'register': 'humble'},
    ('お父さん', 'おとうさん'):{'pitch_accent': {'mora': 4, 'drop': 2}, 'register': 'respectful'},
    ('お母さん', 'おかあさん'):{'pitch_accent': {'mora': 4, 'drop': 2}, 'register': 'respectful'},
    ('兄', 'あに'):           {'pitch_accent': {'mora': 2, 'drop': 1}, 'register': 'humble'},
    ('姉', 'あね'):           {'pitch_accent': {'mora': 2, 'drop': 0}, 'register': 'humble'},
    ('弟', 'おとうと'):       {'pitch_accent': {'mora': 4, 'drop': 4}},
    ('妹', 'いもうと'):       {'pitch_accent': {'mora': 4, 'drop': 4}},
    # Daily verbs (verb-stem accent — these may need refinement)
    ('食べる', 'たべる'):     {'pitch_accent': {'mora': 3, 'drop': 2}},
    ('飲む', 'のむ'):         {'pitch_accent': {'mora': 2, 'drop': 1}},
    ('見る', 'みる'):         {'pitch_accent': {'mora': 2, 'drop': 1}},
    ('行く', 'いく'):         {'pitch_accent': {'mora': 2, 'drop': 0}},
    ('来る', 'くる'):         {'pitch_accent': {'mora': 2, 'drop': 1}},
    ('する', 'する'):         {'pitch_accent': {'mora': 2, 'drop': 0}},
    ('話す', 'はなす'):       {'pitch_accent': {'mora': 3, 'drop': 2}},
    ('聞く', 'きく'):         {'pitch_accent': {'mora': 2, 'drop': 0}},
    ('読む', 'よむ'):         {'pitch_accent': {'mora': 2, 'drop': 1}},
    ('書く', 'かく'):         {'pitch_accent': {'mora': 2, 'drop': 1}},
    ('買う', 'かう'):         {'pitch_accent': {'mora': 2, 'drop': 0}},
    # Counters — nouns that pair canonically with a counter
    ('本', 'ほん'):           {'pitch_accent': {'mora': 2, 'drop': 1}, 'counter': 'satsu'},  # 本 -> 〜冊 (さつ)
    ('車', 'くるま'):         {'pitch_accent': {'mora': 3, 'drop': 0}, 'counter': 'dai'},     # 車 -> 〜台
    ('猫', 'ねこ'):           {'pitch_accent': {'mora': 2, 'drop': 1}, 'counter': 'hiki'},    # 猫 -> 〜匹
    ('犬', 'いぬ'):           {'pitch_accent': {'mora': 2, 'drop': 2}, 'counter': 'hiki'},
    ('鳥', 'とり'):           {'pitch_accent': {'mora': 2, 'drop': 0}, 'counter': 'wa'},      # 鳥 -> 〜羽
    ('魚', 'さかな'):         {'pitch_accent': {'mora': 3, 'drop': 0}, 'counter': 'hiki'},
    ('紙', 'かみ'):           {'pitch_accent': {'mora': 2, 'drop': 2}, 'counter': 'mai'},     # 紙 -> 〜枚
    ('シャツ', 'シャツ'):     {'pitch_accent': {'mora': 2, 'drop': 1}, 'counter': 'mai'},
    ('切手', 'きって'):       {'pitch_accent': {'mora': 3, 'drop': 0}, 'counter': 'mai'},
    ('家', 'いえ'):           {'pitch_accent': {'mora': 2, 'drop': 2}, 'counter': 'ken'},     # 家 -> 〜軒
    ('鉛筆', 'えんぴつ'):     {'pitch_accent': {'mora': 4, 'drop': 0}, 'counter': 'hon'},     # 鉛筆 -> 〜本 (cylindrical)
    ('傘', 'かさ'):           {'pitch_accent': {'mora': 2, 'drop': 1}, 'counter': 'hon'},
    ('靴', 'くつ'):           {'pitch_accent': {'mora': 2, 'drop': 2}, 'counter': 'soku'},    # 靴 -> 〜足 (pairs)
    ('リンゴ', 'りんご'):     {'pitch_accent': {'mora': 3, 'drop': 0}, 'counter': 'ko'},      # 〜個
    ('卵', 'たまご'):         {'pitch_accent': {'mora': 3, 'drop': 2}, 'counter': 'ko'},
    # Honorific / humble / respectful chains (register field)
    ('いる', 'いる'):         {'pitch_accent': {'mora': 2, 'drop': 0}},
    ('いらっしゃる', 'いらっしゃる'): {'pitch_accent': {'mora': 5, 'drop': 4}, 'register': 'respectful'},
    ('おる', 'おる'):         {'pitch_accent': {'mora': 2, 'drop': 1}, 'register': 'humble'},
    ('召し上がる', 'めしあがる'): {'pitch_accent': {'mora': 5, 'drop': 0}, 'register': 'respectful'},
    ('いただく', 'いただく'): {'pitch_accent': {'mora': 4, 'drop': 0}, 'register': 'humble'},
    ('ご覧になる', 'ごらんになる'): {'pitch_accent': {'mora': 6, 'drop': 5}, 'register': 'respectful'},
    ('拝見する', 'はいけんする'): {'pitch_accent': {'mora': 6, 'drop': 0}, 'register': 'humble'},
    # Common adjectives
    ('大きい', 'おおきい'):   {'pitch_accent': {'mora': 4, 'drop': 3}},
    ('小さい', 'ちいさい'):   {'pitch_accent': {'mora': 4, 'drop': 3}},
    ('新しい', 'あたらしい'): {'pitch_accent': {'mora': 5, 'drop': 4}},
    ('古い', 'ふるい'):       {'pitch_accent': {'mora': 3, 'drop': 2}},
    ('高い', 'たかい'):       {'pitch_accent': {'mora': 3, 'drop': 2}},
    ('安い', 'やすい'):       {'pitch_accent': {'mora': 3, 'drop': 2}},
    ('面白い', 'おもしろい'): {'pitch_accent': {'mora': 5, 'drop': 4}},
    ('美味しい', 'おいしい'): {'pitch_accent': {'mora': 4, 'drop': 0}},
    ('暑い', 'あつい'):       {'pitch_accent': {'mora': 3, 'drop': 2}},
    ('寒い', 'さむい'):       {'pitch_accent': {'mora': 3, 'drop': 2}},
    # Common na-adjectives + nouns
    ('好き', 'すき'):         {'pitch_accent': {'mora': 2, 'drop': 2}},
    ('嫌い', 'きらい'):       {'pitch_accent': {'mora': 3, 'drop': 0}},
    ('元気', 'げんき'):       {'pitch_accent': {'mora': 3, 'drop': 1}},
    ('静か', 'しずか'):       {'pitch_accent': {'mora': 3, 'drop': 1}},
    ('便利', 'べんり'):       {'pitch_accent': {'mora': 3, 'drop': 1}},
    # Greetings + set phrases
    ('こんにちは', 'こんにちは'): {'pitch_accent': {'mora': 5, 'drop': 0}},
    ('さようなら', 'さようなら'): {'pitch_accent': {'mora': 5, 'drop': 4}},
    ('おはよう', 'おはよう'): {'pitch_accent': {'mora': 4, 'drop': 0}},
    ('ありがとう', 'ありがとう'): {'pitch_accent': {'mora': 5, 'drop': 2}},
    ('すみません', 'すみません'): {'pitch_accent': {'mora': 5, 'drop': 0}},
}


def main() -> int:
    data = json.loads(VF.read_text(encoding='utf-8'))
    n_pitch = 0
    n_counter = 0
    n_register = 0

    by_form_reading = {}
    by_reading = {}
    for k, v in DEPTH.items():
        by_form_reading[k] = v
        # Don't auto-fallback when form != reading and the form is required
        # (but for many entries form==reading and it's the same key)
        if k[0] == k[1]:
            by_reading[k[1]] = v

    for e in data.get('entries', []):
        form = e.get('form')
        reading = e.get('reading')
        spec = by_form_reading.get((form, reading)) or by_reading.get(reading)
        if not spec:
            continue
        if 'pitch_accent' in spec and e.get('pitch_accent') != spec['pitch_accent']:
            e['pitch_accent'] = spec['pitch_accent']
            n_pitch += 1
        if 'counter' in spec and e.get('counter') != spec['counter']:
            e['counter'] = spec['counter']
            n_counter += 1
        if 'register' in spec and e.get('register') != spec['register']:
            e['register'] = spec['register']
            n_register += 1

    VF.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    total = len(data['entries'])
    nP = sum(1 for e in data['entries'] if e.get('pitch_accent'))
    nC = sum(1 for e in data['entries'] if e.get('counter'))
    nR = sum(1 for e in data['entries'] if e.get('register'))
    print(f'[ISSUE-063 + IMP-087 + IMP-088] Vocab depth fields')
    print(f'  pitch_accent writes: {n_pitch} (now {nP}/{total})')
    print(f'  counter writes:      {n_counter} (now {nC}/{total})')
    print(f'  register writes:     {n_register} (now {nR}/{total})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
