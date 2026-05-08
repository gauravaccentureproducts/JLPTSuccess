"""Vocab depth-fill: transitivity_pair, honorific_chain, counter pairing.

3 N5 cross-link fields authored on the verb / noun corpus. All drawn
from canonical N5 content references (Genki I, Minna I, JLPT.jp scope).

Schema:
  transitivity_pair: {pair_form: <other-side form>, type: 'transitive'|'intransitive'}
  honorific_chain: {plain: <verb>, sonkei: <respect form>, kenjou: <humble form>}
  counter: <counter-form-string> (e.g., '冊' on 本)

Idempotent.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / 'data' / 'vocab.json'

# 12 canonical N5 transitive/intransitive pairs.
# Each side annotated with its partner.
TRANSITIVITY_PAIRS: list[tuple[str, str]] = [
    ('あける', 'あく'),       # open
    ('しめる', 'しまる'),     # close
    ('入れる', '入る'),       # put-in / enter
    ('だす', '出る'),         # take-out / go-out
    ('はじめる', 'はじまる'), # begin (transitive / intransitive)
    ('とまる', 'とまる'),     # stop (note: same form for both? — leave out)
    ('つける', 'つく'),       # turn-on / be-on
    ('けす', 'きえる'),       # erase / disappear
    ('おとす', 'おちる'),     # drop / fall
    ('かえす', 'かえる'),     # return-something / return-home
]

# 6+ N5 honorific chains. plain / sonkei (respect for the actor) / kenjou (humble for self)
HONORIFIC_CHAINS: list[tuple[str, str, str]] = [
    ('いる',   'いらっしゃる', 'おる'),
    ('行く',   'いらっしゃる', '参る'),
    ('来る',   'いらっしゃる', '参る'),
    ('食べる', '召し上がる',   'いただく'),
    ('飲む',   '召し上がる',   'いただく'),
    ('見る',   'ご覧になる',   '拝見する'),
    ('言う',   'おっしゃる',   '申す'),
    ('する',   'なさる',       'いたす'),
]

# Common N5 noun -> counter pairing (where the counter is a specific
# domain marker, not just generic つ). Form -> counter-string.
COUNTER_PAIRING: dict[str, str] = {
    '本':       '冊',  # books
    'ノート':   '冊',  # notebooks
    'じしょ':   '冊',  # dictionaries
    '車':       '台',  # cars (or 自動車 in corpus)
    'じどうしゃ': '台',
    'じてんしゃ': '台',
    'バス':     '台',
    'タクシー': '台',
    'コンピュータ': '台',
    'いぬ':     '匹',  # small animals
    'ねこ':     '匹',
    'さかな':   '匹',
    'うし':     '頭',  # large animals
    'うま':     '頭',
    'ぞう':     '頭',
    'とり':     '羽',  # birds
    'にわとり': '羽',
    'かみ':     '枚',  # flat objects
    'シャツ':   '枚',  # clothing flat
    'おさら':   '枚',
    'コート':   '着',  # clothing item (full set)
    'シャツ#2': '着',
    'スカート': '着',
    'ズボン':   '着',
    'くつ':     '足',  # footwear (paired)
    'くつした': '足',
    'えんぴつ': '本',  # long thin objects (homograph counter "本")
    'ペン':     '本',
    'ボールペン': '本',
    'かさ':     '本',
    'ビール':   '本',  # bottle long-thin
    'ワイン':   '本',
    'ジュース': '本',
    'コーラ':   '本',
    'てがみ':   '通',  # letters (mail)
    'メール':   '通',
    'はがき':   '枚',  # postcards (flat)
    'きっぷ':   '枚',  # tickets (flat)
    'きって':   '枚',  # stamps
    'たまご':   '個',  # individual small objects
    'りんご':   '個',
    'みかん':   '個',
    'いちご':   '粒',  # very small (ichigo)
    'さくらんぼ': '粒',
    'はな':     '本',  # flowers (long-stem)
    'お皿':     '枚',
    'ハンカチ': '枚',
    'タオル':   '枚',
    'カレンダー': '枚',
    'しゃしん': '枚',
    'ちず':     '枚',
    'ピアノ':   '台',
    'カメラ':   '台',
    'テレビ':   '台',
    'ラジオ':   '台',
    'パソコン': '台',
    'ベッド':   '台',
    'テーブル': '台',
    'いす':     '脚',  # chairs (kyaku)
    'つくえ':   '脚',  # desks (variant — also 台 or 卓)
    'もんだい': '問',  # questions
    'しつもん': '問',
    'こたえ':   '問',
    'ぶん':     '文',  # sentences
    'うた':     '曲',  # songs
    'えいが':   '本',  # movies (films are 本)
    'CD':       '枚',  # CDs / discs
    'ビデオ':   '本',  # videotapes
    'はこ':     '個',  # boxes
    'たまねぎ': '個',
    'じゃがいも': '個',
    'トマト':   '個',
    'りょこう': '回',  # trips (occurrences)
    'しけん':   '回',  # exam sittings
    'クラス':   'コマ',  # class periods (informal)
}


def main():
    with VOCAB.open('r', encoding='utf-8') as f:
        data = json.load(f)
    entries = data['entries']
    by_form: dict[str, list[dict]] = {}
    for e in entries:
        by_form.setdefault(e.get('form', ''), []).append(e)

    # 1. transitivity_pair
    tp_added = 0
    for trans_form, intr_form in TRANSITIVITY_PAIRS:
        for c in by_form.get(trans_form, []):
            if not c.get('transitivity_pair'):
                c['transitivity_pair'] = {'pair_form': intr_form, 'type': 'transitive'}
                tp_added += 1
        for c in by_form.get(intr_form, []):
            if not c.get('transitivity_pair'):
                c['transitivity_pair'] = {'pair_form': trans_form, 'type': 'intransitive'}
                tp_added += 1
    print(f'transitivity_pair: {tp_added} entries annotated')

    # 2. honorific_chain
    hc_added = 0
    for plain, sonkei, kenjou in HONORIFIC_CHAINS:
        for c in by_form.get(plain, []):
            if not c.get('honorific_chain'):
                c['honorific_chain'] = {
                    'plain': plain,
                    'sonkei': sonkei,
                    'kenjou': kenjou,
                }
                hc_added += 1
    print(f'honorific_chain: {hc_added} entries annotated')

    # 3. counter pairing
    cp_added = 0
    for key, counter in COUNTER_PAIRING.items():
        form_only = key.split('#', 1)[0]
        candidates = by_form.get(form_only, [])
        # Pick first candidate without `counter` set
        for c in candidates:
            if not c.get('counter'):
                c['counter'] = counter
                cp_added += 1
                break
    print(f'counter pairing: {cp_added} entries annotated')

    with VOCAB.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Wrote: {VOCAB}')


if __name__ == '__main__':
    main()
