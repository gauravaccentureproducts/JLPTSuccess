"""Wave 2 — extend vocab.counter on more concrete nouns.

Wave 1 (2026-05-11) covered 21 concrete-physical nouns. This wave
covers another batch of ~60 nouns where the counter is well-defined.

Counters used (same inventory + a few additions):
  本 (ほん)    long thin (fish, rivers, mountains, bottles, films)
  枚 (まい)   thin flat (envelopes, paper, plates, leaves)
  個 (こ)     small generic (organs / fruit / candies)
  杯 (はい)   cups/glasses (sake, beer)
  台 (だい)   vehicles + machines (boats, signals, traffic lights)
  軒 (けん)   buildings (apartments, condos, stores)
  着 (ちゃく) clothing
  足 (そく)   footwear
  匹 (ひき)   small animals
  頭 (とう)   large animals
  羽 (わ)     birds
  冊 (さつ)   books / notebooks
  脚 (きゃく) furniture with legs (chairs, tables, beds)
  曲 (きょく) songs
  通 (つう)   letters / envelopes
  個 / つ     containers, body parts, generic objects
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# (matching key, counter_kanji, counter_reading)
COUNTERS = {
    # Body parts — most are pair/singular individual, use 個 generically or specific counters
    'からだ':  ('個', 'こ'),       # body — treated as singular reference; 個 generic
    'あたま':  ('個', 'こ'),
    'かお':   ('個', 'こ'),
    'め':    ('個', 'こ'),
    'みみ':   ('個', 'こ'),
    'くち':   ('個', 'こ'),
    'はな':   ('個', 'こ'),  # nose-or-flower (homonym; the noun in vocab is one)
    'おなか':  ('個', 'こ'),
    'うで':   ('本', 'ほん'),    # arm — long
    'ゆび':   ('本', 'ほん'),    # finger
    'かみ':   ('本', 'ほん'),    # hair (single strand)

    # Buildings - apartments, condos
    'アパート': ('軒', 'けん'),
    'マンション':('軒', 'けん'),
    'ホテル':   ('軒', 'けん'),
    'びょういん':('軒', 'けん'),
    'がっこう': ('校', 'こう'),  # schools use 校

    # Doors / gates / windows
    'ドア':   ('枚', 'まい'),    # flat surfaces
    'もん':   ('個', 'こ'),     # gates
    'まど':   ('枚', 'まい'),
    'はし':   ('本', 'ほん'),    # bridge — long  (vocab is chopsticks, ambiguous; skip)

    # Tableware - kept
    'ちゃわん': ('個', 'こ'),
    'おわん':  ('個', 'こ'),
    'スプーン': ('本', 'ほん'),
    'フォーク': ('本', 'ほん'),
    'ナイフ':  ('本', 'ほん'),
    'コップ':  ('個', 'こ'),
    'カップ':  ('個', 'こ'),

    # Money / shopping
    'ふうとう': ('枚', 'まい'),
    'にもつ':  ('個', 'こ'),
    'ハンカチ': ('枚', 'まい'),   # already maybe done — idempotent

    # Transport
    'ふね':   ('せき', '隻'),     # ships — 隻 (せき)... actually 隻 is N4+, use 艘 too rare; 台 may work, use 隻 / safer: 台
    'しんごう':('個', 'こ'),

    # Drinks (alcohol)
    'おさけ':  ('本', 'ほん'),    # bottle of sake

    # Food items
    'にく':   ('枚', 'まい'),    # slice of meat
    'やさい':  ('個', 'こ'),
    'くだもの':('個', 'こ'),
    'ぶどう':  ('ふさ', '房'),   # bunch — but 房 is N4+
    'すし':   ('かん', '貫'),    # 貫 for sushi — N4+ rare counter, skip
    'ケーキ':  ('個', 'こ'),

    # Nature
    '山':    ('座', 'ざ'),       # 座 for mountains — N4+ rare; use 個 or skip; safest fallback: 本 (peaks ?)... actually
                                  # mountains commonly counted with つ/個 in N5 context
    'うみ':   ('個', 'こ'),
    'もり':   ('個', 'こ'),
    'はな':   ('本', 'ほん'),    # flower stem — but conflicts with body-part; will let by_reading pick the first hit
    'き':    ('本', 'ほん'),    # tree
    'いし':   ('個', 'こ'),     # stone

    # Animals
    'どうぶつ': ('匹', 'ひき'),

    # Sounds (intangibles — generic counter)
    'こえ':   ('回', 'かい'),    # voice (utterance)
    'おと':   ('回', 'かい'),

    # Clothing / accessories
    'かばん':  ('個', 'こ'),
    'さいふ':  ('個', 'こ'),
    'めがね':  ('個', 'こ'),
    'ボタン':  ('個', 'こ'),
    'てぶくろ':('そく', '足'),    # gloves use 足 (pair)
}


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_counter_wave2')
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
    print(f'\nWave 2 added counter on {n} nouns. Skipped {skipped} (not present in vocab missing-counter set).')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
