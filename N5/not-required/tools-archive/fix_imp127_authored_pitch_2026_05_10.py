"""IMP-127 follow-up: hand-author pitch_accent for the 172 entries
that the Kanjium auto-mining missed (mostly katakana loanwords +
fixed expressions whose readings aren't in Kanjium's dict).

Pitch values per Tokyo standard (NHK pronunciation conventions
where authoritative; loanword conventions for katakana entries).

Schema: pitch_accent = {mora, drop} where drop is mora-position
(0 = heiban, 1 = atamadaka, etc.)
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

SMALL_MERGE = set('ゃゅょぁぃぅぇぉャュョァィゥェォ')

def count_mora(reading: str) -> int:
    """Count mora — sokuon and ー count, small ya/yu/yo merge."""
    return sum(1 for c in (reading or '') if c not in SMALL_MERGE)

# Authored pitch by form (Tokyo standard, NHK conventions for loanwords).
# (drop value; mora is auto-computed from the entry's reading.)
DROPS = {
    # Demonstratives
    'こんな': 0, 'そんな': 0, 'あんな': 0, 'どんな': 1,
    # Question words / numerals
    '何': 1, 'いくら': 1, '一万': 3,
    # Adverbs
    'もうすぐ': 0, 'もっと': 1, 'ゆっくり': 3, 'いっしょに': 0,
    '一人で': 2, 'じぶんで': 0, 'もういちど': 4, 'やはり': 2,
    # Common nouns (kana writing)
    '後で': 1, 'お店': 0, 'おさけ': 0, 'おさら': 0, 'おわん': 0,
    'とおく': 1, 'いえ': 2, 'おしらせ': 0,
    # Loanword nouns (katakana — Tokyo loanword conventions)
    'トイレ': 1, 'スーパー': 1, 'デパート': 2, 'レストラン': 1,
    'ホテル': 1, 'プール': 1, 'ポスト': 1, 'カフェ': 1,
    'コンサート': 3, 'コンビニ': 0, 'セール': 1, 'フロント': 1,
    'ベンチ': 1, 'アパート': 2, 'マンション': 1, 'ドア': 1,
    'エレベーター': 4, 'ベッド': 1, 'テーブル': 0, 'カーテン': 1,
    'タオル': 1, 'テープ': 1, 'テレビ': 1, 'ラジオ': 0,
    'カメラ': 1, 'ビデオ': 1, 'ピアノ': 0, 'ギター': 1,
    'バイク': 1, 'バス': 1, 'タクシー': 1, 'テスト': 1,
    'ボールペン': 0, 'ペン': 1, 'ノート': 1, 'チョーク': 1,
    # Food loanwords
    'レモン': 0, 'じゃがいも': 0, 'トマト': 0, 'キャベツ': 0,
    'バター': 0, 'チーズ': 1, 'カレー': 0, 'ハンバーガー': 3,
    'サンドイッチ': 4, 'サラダ': 0, 'スープ': 1, 'ケーキ': 1,
    'アイスクリーム': 5, 'チョコレート': 3, 'ジュース': 1,
    'ワイン': 1, 'スプーン': 1, 'フォーク': 1, 'ナイフ': 1,
    'コップ': 0, 'カップ': 1,
    # Clothing
    'ピンク': 1, 'コート': 1, 'セーター': 1, 'ワイシャツ': 0,
    'ズボン': 1, 'スカート': 2, 'ネクタイ': 1, 'ハンカチ': 0,
    'ボタン': 0, 'ポケット': 1,
    # Money / shop
    'ドル': 1, 'レジ': 1,
    # Country names (loanword conventions)
    '日本': 2, 'アメリカ': 0, 'フランス': 0, 'ドイツ': 1,
    'スペイン': 2, 'イギリス': 0,
    # Loanword "other"
    'カタカナ': 3, 'ゲーム': 1, 'スポーツ': 2, 'ニュース': 1,
    'パーティー': 1, 'プレゼント': 2, 'シャワー': 1,
    'スリッパ': 0, 'ティッシュ': 1, 'フィルム': 1, 'レコード': 0,
    'カレンダー': 2, 'テープレコーダー': 5, 'ストーブ': 0,
    'クラス': 1, 'グラム': 1, 'アルバイト': 3,
    # Verbs (する compounds — most heiban)
    'もっていく': 4, 'さんぽする': 0, 'れんしゅうする': 0,
    'しつもんする': 0, 'しごとする': 1, '電話する': 0,
    'コピーする': 1, 'そうじする': 0, 'せんたくする': 0,
    'かいものする': 0,
    # Conjunctions
    'そして': 0, 'それから': 0, 'それで': 0, 'でも': 1,
    'だから': 1, 'ですから': 0, 'それに': 0, 'ところで': 3,
    'けれど': 0,
    # Particles / function words (heiban-default; particles aren't
    # really pitched on their own but for consistency we tag them)
    'を': 0, 'まで': 0, 'だけ': 0, 'ずつ': 0, 'ぐらい': 1,
    # Existence verbs (variant)
    'ござる': 1,
    # Set expressions (heiban for long polite forms)
    'どうぞ': 1, 'どうも': 1, 'どうぞよろしく': 0, 'もしもし': 1,
    'おはようございます': 0, 'おやすみなさい': 0,
    'しつれいします': 0, 'しつれいしました': 0,
    'ありがとうございます': 0, 'ごめんなさい': 0,
    'おねがいします': 0, 'いただきます': 4,
    'ごちそうさまでした': 0, 'いってきます': 4,
    'いってらっしゃい': 0, 'おげんきですか': 0,
    'おかげさまで': 0, 'いらっしゃいませ': 0,
    'えーと': 1, 'そうですね': 0, 'そうですか': 0,
    'いいえ': 0, 'ええ': 0, 'ううん': 0, 'さあ': 1,
    'それでは': 0, 'おじゃまします': 0,
    'じゃあ': 1,
    # Crowd
    'みんな': 3, 'ゼロ': 0,
}

vocab_path = ROOT / 'data' / 'vocab.json'
data = json.loads(vocab_path.read_text(encoding='utf-8'))
entries = data['entries']

assigned = 0
mora_mismatch = []
not_in_dict = []

for e in entries:
    if e.get('pitch_accent'):
        continue
    form = e.get('form', '')
    if form not in DROPS:
        not_in_dict.append(form)
        continue
    drop = DROPS[form]
    # Compute mora from reading (use form when reading is empty)
    reading = e.get('reading') or form
    # Reading sometimes has '/' alternates: 'なに / なん'. Use first.
    reading_first = reading.split('/')[0].strip()
    mora = count_mora(reading_first)
    if mora == 0 or drop > mora:
        mora_mismatch.append((form, reading_first, mora, drop))
        continue
    e['pitch_accent'] = {'mora': mora, 'drop': drop}
    e['pitch_accent_provenance'] = 'llm_curated'
    assigned += 1

vocab_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final coverage
total = len(entries)
with_pitch = sum(1 for e in entries if e.get('pitch_accent'))
print(f'Newly authored:       {assigned}')
print(f'Skipped (mora<drop):  {len(mora_mismatch)}')
if mora_mismatch:
    for f, r, m, d in mora_mismatch[:5]:
        print(f'  {f} ({r}) mora={m} drop={d}')
print(f'Not in DROPS dict:    {len(not_in_dict)}')
if not_in_dict[:5]:
    print(f'  samples: {not_in_dict[:5]}')
print(f'\\nTotal coverage:       {with_pitch}/{total} ({100*with_pitch/total:.0f}%)')
