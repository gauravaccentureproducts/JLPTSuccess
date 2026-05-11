"""Fill vocab.counter on concrete N5 nouns where the canonical
Japanese counter is unambiguous.

Audit context: noun counter coverage is 134/566 (24%). Many of the
remaining 432 nouns are abstract or take multiple counters
(time-words, weather-states, mass nouns) — for these, filling a
single canonical counter would be misleading. This pass fills
~90 concrete-physical nouns where the textbook counter is
universally agreed.

Counter categories used:
  本 (ほん)    long thin objects (pens, umbrellas, bottles)
  枚 (まい)   thin flat objects (paper, plates, CDs)
  個 (こ)     small generic objects (apples, eggs)
  杯 (はい)   cups/glasses of liquid
  台 (だい)   vehicles, machines, appliances
  軒 (けん)   buildings, houses, shops
  着 (ちゃく) clothing outfits/suits
  足 (そく)   footwear pairs
  匹 (ひき)   small animals (cats, dogs)
  頭 (とう)   large animals (horses, cows)
  羽 (わ)     birds
  冊 (さつ)   books
  脚 (きゃく) chairs / 4-legged furniture
  曲 (きょく) songs

Each entry: counter = {kanji, reading}. Provenance: auto_derived.

The script cross-checks vocab.json for each form; skips if not
present or already has counter.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Counter assignments by reading (matching vocab.reading field).
COUNTERS = {
    # Long thin objects -> 本 (ほん)
    'えんぴつ': ('本', 'ほん'),
    'ペン':     ('本', 'ほん'),
    'ボールペン':('本', 'ほん'),
    'まんねんひつ':('本', 'ほん'),
    'マッチ':   ('本', 'ほん'),
    'バナナ':   ('本', 'ほん'),
    'にんじん': ('本', 'ほん'),
    'ねぎ':     ('本', 'ほん'),
    'びん':     ('本', 'ほん'),
    'ビール':   ('本', 'ほん'),
    'ワイン':   ('本', 'ほん'),
    'ジュース': ('本', 'ほん'),
    'ぎゅうにゅう':('本', 'ほん'),
    'えいが':   ('本', 'ほん'),
    'かわ':     ('本', 'ほん'),

    # Thin flat objects -> 枚 (まい)
    'かみ':     ('枚', 'まい'),
    'ハンカチ': ('枚', 'まい'),
    'タオル':   ('枚', 'まい'),
    'はがき':   ('枚', 'まい'),
    'CD':       ('枚', 'まい'),
    'DVD':      ('枚', 'まい'),
    'シャツ':   ('枚', 'まい'),
    'パンツ':   ('枚', 'まい'),
    'ふとん':   ('枚', 'まい'),
    'チケット': ('枚', 'まい'),
    'おさら':   ('枚', 'まい'),
    'さら':     ('枚', 'まい'),

    # Small generic objects -> 個 (こ)
    'りんご':   ('個', 'こ'),
    'みかん':   ('個', 'こ'),
    'たまご':   ('個', 'こ'),
    'いちご':   ('個', 'こ'),
    'おにぎり': ('個', 'こ'),
    'ぼうし':   ('個', 'こ'),
    'パン':     ('個', 'こ'),
    'ケーキ':   ('個', 'こ'),
    'いす':     ('脚', 'きゃく'),

    # Cups / glasses -> 杯 (はい)
    'コーヒー': ('杯', 'はい'),
    'おちゃ':   ('杯', 'はい'),
    'こうちゃ': ('杯', 'はい'),
    'みず':     ('杯', 'はい'),
    'おみず':   ('杯', 'はい'),

    # Vehicles / machines -> 台 (だい)
    '電車':     ('台', 'だい'),
    'でんしゃ': ('台', 'だい'),
    'バス':     ('台', 'だい'),
    'バイク':   ('台', 'だい'),
    'じてんしゃ':('台', 'だい'),
    'くるま':   ('台', 'だい'),
    'ちかてつ': ('台', 'だい'),
    'タクシー': ('台', 'だい'),
    'きしゃ':   ('台', 'だい'),
    'パソコン': ('台', 'だい'),
    'テレビ':   ('台', 'だい'),
    'れいぞうこ':('台', 'だい'),
    'せんたくき':('台', 'だい'),
    'カメラ':   ('台', 'だい'),
    'でんわ':   ('台', 'だい'),
    'けいたい': ('台', 'だい'),
    'スマホ':   ('台', 'だい'),
    'つくえ':   ('台', 'だい'),
    'ベッド':   ('台', 'だい'),

    # Buildings -> 軒 (けん)
    'いえ':     ('軒', 'けん'),
    'うち':     ('軒', 'けん'),
    'たてもの': ('軒', 'けん'),

    # Clothes (whole outfit) -> 着 (ちゃく)
    'ふく':     ('着', 'ちゃく'),
    'ようふく': ('着', 'ちゃく'),
    'セーター': ('着', 'ちゃく'),
    'スーツ':   ('着', 'ちゃく'),
    'コート':   ('着', 'ちゃく'),
    'きもの':   ('着', 'ちゃく'),

    # Footwear -> 足 (そく)
    'くつ':     ('足', 'そく'),
    'くつした': ('足', 'そく'),
    'スリッパ': ('足', 'そく'),

    # Small animals -> 匹 (ひき)
    'いぬ':     ('匹', 'ひき'),
    'ねこ':     ('匹', 'ひき'),
    'ぶた':     ('匹', 'ひき'),
    'さかな':   ('匹', 'ひき'),
    'むし':     ('匹', 'ひき'),

    # Large animals -> 頭 (とう)
    'うし':     ('頭', 'とう'),
    'うま':     ('頭', 'とう'),
    'ぞう':     ('頭', 'とう'),

    # Birds -> 羽 (わ)
    'とり':     ('羽', 'わ'),
    'にわとり': ('羽', 'わ'),

    # Books -> 冊 (さつ)
    'ほん':     ('冊', 'さつ'),
    'ノート':   ('冊', 'さつ'),
    'きょうかしょ':('冊', 'さつ'),
    'じしょ':   ('冊', 'さつ'),
    'ざっし':   ('冊', 'さつ'),

    # Songs -> 曲 (きょく)
    'うた':     ('曲', 'きょく'),

    # Letters -> 通 (つう)
    'てがみ':   ('通', 'つう'),
}


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_counter_concrete_fill')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    n = 0
    n_not_found = 0
    n_already = 0

    # Build form/reading -> entry lookup
    candidates = []
    for e in data['entries']:
        if e.get('pos') != 'noun':
            continue
        if e.get('counter'):
            continue
        candidates.append(e)

    by_reading = {}
    for e in candidates:
        r = e.get('reading')
        f = e.get('form')
        if r and r not in by_reading: by_reading[r] = e
        if f and f not in by_reading: by_reading[f] = e

    for reading, (k, kr) in COUNTERS.items():
        e = by_reading.get(reading)
        if not e:
            # Look across ALL entries (in case it has counter already)
            full = next((x for x in data['entries'] if x.get('reading') == reading or x.get('form') == reading), None)
            if not full:
                n_not_found += 1
                continue
            if full.get('counter'):
                n_already += 1
                continue
            e = full
        e['counter'] = {'kanji': k, 'reading': kr}
        e['counter_provenance'] = 'auto_derived'
        n += 1
        if n <= 8:
            print(f'  + {e.get("form"):<10} ({reading:<10}) -> {k} ({kr})')

    if n > 8: print(f'  ... (and {n - 8} more)')
    print(f'\nFilled counter on {n} nouns.')
    print(f'  Not found in vocab: {n_not_found}')
    print(f'  Already had counter: {n_already}')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
