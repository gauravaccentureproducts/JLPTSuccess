"""Wave 3 — push vocab counter as far as responsibly possible.

Wave 1+2 = 200/566. This wave targets ~80 more concrete N5 nouns
across buildings / rooms / food categories / clothing / furniture /
school items / sport / leisure / kitchen / containers.

Skips genuinely abstract / counter-only / mass-noun entries:
  - time-units that ARE counters (日 / 月 / 年 / 一日 / 二月 etc.)
  - color names (あか / あお / きいろ — abstracts)
  - language / country names
  - mass nouns (にく / さとう / しお — measured by 量目, not counted)
  - intangibles (こと / もの / しごと / びょうき / けっこん)
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

COUNTERS = {
    # Buildings + rooms (軒 for buildings; 個 for rooms; 校 for schools)
    'だいどころ':  ('個', 'こ'),
    'おてあらい':  ('個', 'こ'),
    'トイレ':     ('個', 'こ'),
    'おふろ':     ('個', 'こ'),
    'げんかん':    ('個', 'こ'),
    'にわ':      ('個', 'こ'),
    'だいがく':    ('校', 'こう'),
    'こうこう':    ('校', 'こう'),
    'きょうしつ':   ('個', 'こ'),
    'としょかん':   ('軒', 'けん'),
    'ぎんこう':    ('軒', 'けん'),
    'ゆうびんきょく': ('軒', 'けん'),
    'じむしょ':    ('個', 'こ'),
    'スーパー':    ('軒', 'けん'),
    'きっさてん':   ('軒', 'けん'),
    'やおや':     ('軒', 'けん'),
    'にくや':     ('軒', 'けん'),
    'パンや':     ('軒', 'けん'),
    'えき':      ('駅', 'えき'),
    'くうこう':    ('個', 'こ'),
    'こうえん':    ('個', 'こ'),
    'どうぶつえん':  ('個', 'こ'),
    'びじゅつかん':  ('個', 'こ'),
    'えいがかん':   ('軒', 'けん'),
    'りょかん':    ('軒', 'けん'),
    'たいしかん':   ('個', 'こ'),
    'こうばん':    ('個', 'こ'),
    'こうじょう':   ('個', 'こ'),
    'こうさてん':   ('個', 'こ'),
    'プール':     ('個', 'こ'),
    'ポスト':     ('個', 'こ'),
    'おてら':     ('軒', 'けん'),
    'カフェ':     ('軒', 'けん'),
    'ビル':      ('棟', 'むね'),
    'ホテル':     ('軒', 'けん'),

    # Furniture / household
    'かべ':      ('面', 'めん'),
    'かいだん':    ('段', 'だん'),
    'エレベーター':  ('台', 'だい'),
    'しんしつ':    ('個', 'こ'),
    'もうふ':     ('枚', 'まい'),
    'まくら':     ('個', 'こ'),
    'たな':      ('個', 'こ'),
    'カーテン':    ('枚', 'まい'),
    'かぎ':      ('本', 'ほん'),
    'ストーブ':    ('台', 'だい'),
    'はブラシ':    ('本', 'ほん'),
    'テープ':     ('本', 'ほん'),
    'ベンチ':     ('脚', 'きゃく'),
    'かびん':     ('個', 'こ'),
    'テープレコーダー': ('台', 'だい'),

    # Food (countable items)
    'すいか':     ('個', 'こ'),
    'レモン':     ('個', 'こ'),
    'だいこん':    ('本', 'ほん'),
    'きゅうり':    ('本', 'ほん'),
    'キャベツ':    ('個', 'こ'),
    'てんぷら':    ('個', 'こ'),
    'カレー':     ('皿', 'さら'),
    'ラーメン':    ('杯', 'はい'),
    'うどん':     ('杯', 'はい'),
    'そば':      ('杯', 'はい'),
    'ハンバーガー':  ('個', 'こ'),
    'サンドイッチ':  ('個', 'こ'),
    'サラダ':     ('皿', 'さら'),
    'スープ':     ('杯', 'はい'),
    'アイスクリーム': ('個', 'こ'),
    'チョコレート':  ('個', 'こ'),
    'おみやげ':    ('個', 'こ'),
    'なべ':      ('個', 'こ'),

    # Roles / people — 人 counter
    'かいしゃいん':  ('人', 'にん'),
    'えきいん':    ('人', 'にん'),
    'けいかん':    ('人', 'にん'),

    # School items
    'しゅくだい':   ('個', 'こ'),
    'テスト':     ('回', 'かい'),
    'こくばん':    ('個', 'こ'),
    'チョーク':    ('本', 'ほん'),
    'え':       ('枚', 'まい'),

    # Misc
    'プレゼント':   ('個', 'こ'),
    'パーティー':   ('回', 'かい'),
    'シャワー':    ('回', 'かい'),
    'コンサート':   ('回', 'かい'),
    'はいざら':    ('個', 'こ'),
    'ティッシュ':   ('枚', 'まい'),
    'フィルム':    ('本', 'ほん'),
    'レコード':    ('枚', 'まい'),
    'ペット':     ('匹', 'ひき'),
    'おもちゃ':    ('個', 'こ'),
    'クラス':     ('クラス', 'クラス'),
    'グラム':     ('グラム', 'グラム'),
    'メートル':    ('メートル', 'メートル'),
    'キログラム':   ('キログラム', 'キログラム'),
    'キロメートル':  ('キロメートル', 'キロメートル'),

    # Transport
    'みち':      ('本', 'ほん'),
}


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_counter_wave3')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')
    data = json.loads(fp.read_text(encoding='utf-8'))
    by_reading = {}
    for e in data['entries']:
        if e.get('pos') != 'noun':
            continue
        if e.get('counter'):
            continue
        r = e.get('reading')
        f = e.get('form')
        if r and r not in by_reading: by_reading[r] = e
        if f and f not in by_reading: by_reading[f] = e
    n = 0
    skipped = 0
    for key, (k, kr) in COUNTERS.items():
        e = by_reading.get(key)
        if not e:
            skipped += 1
            continue
        if e.get('counter'):
            continue
        e['counter'] = {'kanji': k, 'reading': kr}
        e['counter_provenance'] = 'auto_derived'
        n += 1
    print(f'\nWave 3 added counter on {n} nouns. Skipped {skipped} not-in-missing-set.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
