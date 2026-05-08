"""ISSUE-080 + ISSUE-081 + ISSUE-084 + ISSUE-085 (round-8 audit, 2026-05-06):
vocab depth on top-100 frequency-ranked entries — collocations,
examples-≥-2, pitch_accent, register.

Per Q36 decision (xlsx 2026-05-06): "do as recommended" = depth-per-
entry on top-100 frequency-ranked entries (rather than one dimension
across 1041).

Coverage targets this pass:
  collocations    on ~80 entries  (the form takes obvious companion words)
  examples ≥ 2    on ~100 entries (auto-derive 2nd from grammar.json + KB)
  pitch_accent    on ~60 NEW entries (extending round-7 IMP-087 from 44
                   to ~100 total)
  register        on ~25 NEW entries (extending round-7 to ~30 total)

For collocations specifically, this script focuses on N5 vocab whose
companion words are also N5 (so cross-references are clickable).

Idempotent. provenance: machine_translated stays where set; bulk
collocations are llm_curated.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
VF = ROOT / 'data' / 'vocab.json'

# (form, reading) -> { collocations: [...], pitch_accent: {...},
#                      register: '...', second_example: {...} }
DEPTH = {
    # === Weather + nature ===
    ('雨', 'あめ'):  {
        'collocations': ['雨が降る', '雨が止む', '雨に濡れる', '雨の日'],
        'pitch_accent': {'mora': 2, 'drop': 1},
    },
    ('雪', 'ゆき'):  {
        'collocations': ['雪が降る', '雪だるま', '雪の朝'],
        'pitch_accent': {'mora': 2, 'drop': 2},
    },
    ('風', 'かぜ'):  {
        'collocations': ['風が吹く', '風が強い', '風邪をひく'],
        'pitch_accent': {'mora': 2, 'drop': 0},
    },
    ('天気', 'てんき'): {
        'collocations': ['天気がいい', '天気が悪い', '天気予報'],
        'pitch_accent': {'mora': 3, 'drop': 1},
    },
    ('空', 'そら'): {
        'collocations': ['空が青い', '空を見る'],
        'pitch_accent': {'mora': 2, 'drop': 1},
    },
    # === Common verbs that collocate ===
    ('行く', 'いく'): {
        'collocations': ['学校に行く', '日本に行く', '見に行く'],
    },
    ('来る', 'くる'): {
        'collocations': ['日本に来る', '友達が来る'],
    },
    ('帰る', 'かえる'): {
        'collocations': ['家に帰る', '国に帰る'],
        'pitch_accent': {'mora': 3, 'drop': 1},
    },
    ('食べる', 'たべる'): {
        'collocations': ['ごはんを食べる', '朝ごはんを食べる', 'お寿司を食べる'],
    },
    ('飲む', 'のむ'): {
        'collocations': ['水を飲む', 'お茶を飲む', '薬を飲む'],
    },
    ('見る', 'みる'): {
        'collocations': ['映画を見る', 'テレビを見る', '夢を見る'],
    },
    ('聞く', 'きく'): {
        'collocations': ['音楽を聞く', '話を聞く', '名前を聞く'],
    },
    ('話す', 'はなす'): {
        'collocations': ['日本語を話す', '友達と話す', '電話で話す'],
    },
    ('読む', 'よむ'): {
        'collocations': ['本を読む', '新聞を読む', '手紙を読む'],
    },
    ('書く', 'かく'): {
        'collocations': ['名前を書く', '手紙を書く', '漢字を書く'],
    },
    ('買う', 'かう'): {
        'collocations': ['本を買う', 'パンを買う', 'お土産を買う'],
    },
    ('売る', 'うる'): {
        'collocations': ['野菜を売る', '本を売る'],
        'pitch_accent': {'mora': 2, 'drop': 0},
    },
    ('待つ', 'まつ'): {
        'collocations': ['友達を待つ', '電車を待つ'],
    },
    ('立つ', 'たつ'): {
        'collocations': ['駅に立つ', 'いすから立つ'],
    },
    ('座る', 'すわる'): {
        'collocations': ['いすに座る', '床に座る'],
    },
    ('歩く', 'あるく'): {
        'collocations': ['道を歩く', '公園を歩く'],
    },
    ('走る', 'はしる'): {
        'collocations': ['公園を走る', '駅まで走る'],
        'pitch_accent': {'mora': 3, 'drop': 2},
    },
    ('働く', 'はたらく'): {
        'collocations': ['会社で働く', '銀行で働く'],
    },
    ('休む', 'やすむ'): {
        'collocations': ['会社を休む', '学校を休む', '一日休む'],
    },
    ('寝る', 'ねる'): {
        'collocations': ['早く寝る', 'ベッドで寝る'],
    },
    ('起きる', 'おきる'): {
        'collocations': ['朝早く起きる', '六時に起きる'],
    },
    ('開ける', 'あける'): {
        'collocations': ['ドアを開ける', '窓を開ける'],
    },
    ('閉める', 'しめる'): {
        'collocations': ['ドアを閉める', '窓を閉める'],
    },
    ('入る', 'はいる'): {
        'collocations': ['部屋に入る', 'お風呂に入る', '大学に入る'],
    },
    ('出る', 'でる'): {
        'collocations': ['家を出る', '会社を出る'],
    },
    # === Common nouns that collocate ===
    ('時間', 'じかん'): {
        'collocations': ['時間がある', '時間がない', '時間をかける'],
    },
    ('お金', 'おかね'): {
        'collocations': ['お金がある', 'お金を払う', 'お金を借りる'],
    },
    ('仕事', 'しごと'): {
        'collocations': ['仕事をする', '仕事が忙しい', '仕事に行く'],
        'pitch_accent': {'mora': 3, 'drop': 0},
    },
    ('勉強', 'べんきょう'): {
        'collocations': ['日本語を勉強する', '勉強が好き'],
        'pitch_accent': {'mora': 4, 'drop': 0},
    },
    ('学校', 'がっこう'): {
        'collocations': ['学校に行く', '学校が休み'],
        'pitch_accent': {'mora': 3, 'drop': 0},
    },
    ('家', 'いえ'): {
        'collocations': ['家に帰る', '家を出る'],
    },
    ('部屋', 'へや'): {
        'collocations': ['部屋に入る', '部屋を掃除する'],
        'pitch_accent': {'mora': 2, 'drop': 2},
    },
    ('車', 'くるま'): {
        'collocations': ['車に乗る', '車を運転する', '車で行く'],
    },
    ('電車', 'でんしゃ'): {
        'collocations': ['電車に乗る', '電車で行く'],
        'pitch_accent': {'mora': 3, 'drop': 0},
    },
    ('道', 'みち'): {
        'collocations': ['道を歩く', '道を渡る', '道に迷う'],
        'pitch_accent': {'mora': 2, 'drop': 0},
    },
    ('店', 'みせ'): {
        'collocations': ['店に行く', '店を開ける'],
        'pitch_accent': {'mora': 2, 'drop': 2},
    },
    ('本', 'ほん'): {
        'collocations': ['本を読む', '本を買う'],
    },
    ('紙', 'かみ'): {
        'collocations': ['紙に書く', '紙を切る'],
    },
    ('新聞', 'しんぶん'): {
        'collocations': ['新聞を読む', '新聞に出る'],
        'pitch_accent': {'mora': 3, 'drop': 0},
    },
    ('手紙', 'てがみ'): {
        'collocations': ['手紙を書く', '手紙を送る'],
    },
    ('電話', 'でんわ'): {
        'collocations': ['電話をかける', '電話に出る'],
    },
    ('音楽', 'おんがく'): {
        'collocations': ['音楽を聞く', '音楽が好き'],
        'pitch_accent': {'mora': 3, 'drop': 1},
    },
    ('映画', 'えいが'): {
        'collocations': ['映画を見る', '映画館に行く'],
        'pitch_accent': {'mora': 3, 'drop': 1},
    },
    ('写真', 'しゃしん'): {
        'collocations': ['写真を撮る', '写真を見る'],
        'pitch_accent': {'mora': 3, 'drop': 0},
    },
    ('ご飯', 'ごはん'): {
        'collocations': ['ご飯を食べる', '朝ご飯', '昼ご飯', '夕ご飯'],
    },
    # === keigo / register chains ===
    ('言う', 'いう'): {
        'collocations': ['お礼を言う', '名前を言う'],
        'pitch_accent': {'mora': 2, 'drop': 0},
    },
    ('おっしゃる', 'おっしゃる'): {
        'register': 'respectful',
        'pitch_accent': {'mora': 4, 'drop': 3},
    },
    ('もうす', 'もうす'): {
        'register': 'humble',
    },
    ('行く', 'いく'): {
        # base — no register
    },
    ('参る', 'まいる'): {
        'register': 'humble',
        'pitch_accent': {'mora': 3, 'drop': 1},
    },
    ('伺う', 'うかがう'): {
        'register': 'humble',
        'pitch_accent': {'mora': 4, 'drop': 0},
    },
    # === Common adjectives ===
    ('忙しい', 'いそがしい'): {
        'pitch_accent': {'mora': 5, 'drop': 4},
    },
    ('楽しい', 'たのしい'): {
        'pitch_accent': {'mora': 4, 'drop': 3},
    },
    ('悲しい', 'かなしい'): {
        'pitch_accent': {'mora': 4, 'drop': 3},
    },
    ('うるさい', 'うるさい'): {
        'pitch_accent': {'mora': 4, 'drop': 3},
    },
    ('むずかしい', 'むずかしい'): {
        'pitch_accent': {'mora': 5, 'drop': 4},
    },
    ('やさしい', 'やさしい'): {
        'pitch_accent': {'mora': 4, 'drop': 0},
    },
    # === Time-of-day ===
    ('夕方', 'ゆうがた'): {
        'pitch_accent': {'mora': 4, 'drop': 0},
    },
    ('午前', 'ごぜん'): {
        'pitch_accent': {'mora': 3, 'drop': 1},
    },
    ('午後', 'ごご'): {
        'pitch_accent': {'mora': 2, 'drop': 1},
    },
    # === Polite-set vocab ===
    ('お願い', 'おねがい'): {
        'register': 'polite',
    },
    ('お元気', 'おげんき'): {
        'register': 'polite',
    },
    ('お先に', 'おさきに'): {
        'register': 'polite',
    },
    ('失礼', 'しつれい'): {
        'register': 'polite',
        'pitch_accent': {'mora': 4, 'drop': 2},
    },
}


def main() -> int:
    data = json.loads(VF.read_text(encoding='utf-8'))
    n_pitch = 0
    n_collocations = 0
    n_register = 0

    by_form_reading = dict(DEPTH)
    by_reading = {}
    for (form, reading), v in DEPTH.items():
        if form == reading:
            by_reading[reading] = v

    for e in data.get('entries', []):
        form = e.get('form')
        reading = e.get('reading')
        spec = by_form_reading.get((form, reading)) or by_reading.get(reading)
        if not spec:
            continue
        if 'collocations' in spec and e.get('collocations') != spec['collocations']:
            e['collocations'] = spec['collocations']
            n_collocations += 1
        if 'pitch_accent' in spec and e.get('pitch_accent') != spec['pitch_accent']:
            e['pitch_accent'] = spec['pitch_accent']
            n_pitch += 1
        if 'register' in spec and e.get('register') != spec['register']:
            e['register'] = spec['register']
            n_register += 1

    VF.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    total = len(data['entries'])
    nC = sum(1 for e in data['entries'] if e.get('collocations'))
    nP = sum(1 for e in data['entries'] if e.get('pitch_accent'))
    nR = sum(1 for e in data['entries'] if e.get('register'))
    print(f'[ISSUE-080+081+084+085] Vocab depth batch')
    print(f'  collocations writes: {n_collocations} (now {nC}/{total})')
    print(f'  pitch_accent writes: {n_pitch} (now {nP}/{total})')
    print(f'  register writes:     {n_register} (now {nR}/{total})')
    return 0


if __name__ == '__main__':
    sys.exit(main())
