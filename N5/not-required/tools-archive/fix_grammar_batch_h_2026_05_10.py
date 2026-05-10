"""Grammar Batch H (2026-05-10):
G6 politeness_ladder expansion. From 76/178 to ~110+.
Schema per entry: {casual, polite, humble, respectful}
N5-only kanji + kana.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

grammar_path = ROOT / 'data' / 'grammar.json'
data = json.loads(grammar_path.read_text(encoding='utf-8'))
patterns = data['patterns']

LADDER = {
    'n5-006': {  # へ (direction)
        'casual': 'がっこう いく。 (drop へ in casual)',
        'polite': 'がっこうへ いきます。',
        'humble': 'がっこうへ まいります。',
        'respectful': 'がっこうへ いらっしゃいます。',
    },
    'n5-010': {  # まで
        'casual': 'にじまで いる。',
        'polite': 'にじまで います。',
        'humble': 'にじまで おります。',
        'respectful': 'にじまで いらっしゃいます。',
    },
    'n5-011': {  # や (non-exhaustive list)
        'casual': 'ノートやペンや なんか かう。',
        'polite': 'ノートや ペンを かいます。',
        'humble': 'ノートや ペンを ちょうだいいたします。',
        'respectful': 'ノートや ペンを おもとめになります。',
    },
    'n5-021': {  # から〜まで
        'casual': 'はちじから ろくじまで いる。',
        'polite': 'はちじから ろくじまで います。',
        'humble': 'はちじから ろくじまで おります。',
        'respectful': 'はちじから ろくじまで いらっしゃいます。',
    },
    'n5-068': {  # なかった (plain past negative)
        'casual': 'たべなかった。',
        'polite': 'たべませんでした。',
        'humble': 'いただきませんでした。',
        'respectful': 'めしあがりませんでした。',
    },
    'n5-070': {  # Vて、Vて、…
        'casual': 'たべて、ねた。',
        'polite': 'たべて、ねました。',
        'humble': 'いただいて、やすみました。',
        'respectful': 'めしあがって、おやすみに なりました。',
    },
    'n5-082': {  # i-Adj past negative
        'casual': 'たかくなかった。',
        'polite': 'たかくなかった です。 / たかくありませんでした。',
        'humble': 'たかく ございませんでした。',
        'respectful': '(rare for adjectives)',
    },
    'n5-088': {  # na-Adj past negative
        'casual': 'しずかじゃ なかった。',
        'polite': 'しずかじゃ ありませんでした。',
        'humble': 'しずかでは ございませんでした。',
        'respectful': '(rare)',
    },
    'n5-105': {  # たくない
        'casual': 'たべたくない。',
        'polite': 'たべたくないです。',
        'humble': 'いただきたくない です。',
        'respectful': 'めしあがりたくないと おもって いらっしゃいます。',
    },
    'n5-115': {  # に (time)
        'casual': 'はちじに おきる。',
        'polite': 'はちじに おきます。',
        'humble': 'はちじに おきます。 (no humble shift for self-time)',
        'respectful': 'はちじに おきに なります。',
    },
    'n5-118': {  # いま/すぐ/もう/まだ
        'casual': 'いま いく。',
        'polite': 'いま いきます。',
        'humble': 'ただいま まいります。',
        'respectful': 'ただいま いらっしゃいます。',
    },
    'n5-119': {  # ～まえ
        'casual': 'たべるまえに あらう。',
        'polite': 'たべるまえに あらいます。',
        'humble': 'いただくまえに おてあらいします。',
        'respectful': 'めしあがるまえに あらいに なります。',
    },
    'n5-120': {  # ～あと
        'casual': 'たべたあとで ねる。',
        'polite': 'たべたあとで ねます。',
        'humble': 'いただいたあとで やすみます。',
        'respectful': 'めしあがった あとで おやすみに なります。',
    },
    'n5-129': {  # どうして〜から
        'casual': 'なんで？ おそかったから。',
        'polite': 'どうしてですか。 おそかったからです。',
        'humble': 'なぜでございましょうか。 おそうございましたゆえ。',
        'respectful': 'なぜでいらっしゃいますか。 おそかった ためで ございます。',
    },
    'n5-142': {  # 〜にします
        'casual': 'コーヒーに する。',
        'polite': 'コーヒーに します。',
        'humble': 'コーヒーに いたします。',
        'respectful': 'コーヒーに なさいます。',
    },
    'n5-143': {  # 〜になります／〜くなります
        'casual': 'たかく なる。',
        'polite': 'たかく なります。',
        'humble': 'たこう なります。 (literary)',
        'respectful': 'おたかく おなりに なります。 (rare)',
    },
    'n5-144': {  # 〜ながら
        'casual': 'たべながら みる。',
        'polite': 'たべながら みます。',
        'humble': 'いただきながら はいけんします。',
        'respectful': 'めしあがりながら ごらんに なります。',
    },
    'n5-147': {  # よく/ときどき/あまり/ぜんぜん
        'casual': 'よく たべる。',
        'polite': 'よく たべます。',
        'humble': 'よく いただきます。',
        'respectful': 'よく めしあがります。',
    },
    'n5-148': {  # いつも/たいてい/たまに
        'casual': 'いつも テレビを みる。',
        'polite': 'いつも テレビを みます。',
        'humble': 'いつも テレビを はいけん いたします。',
        'respectful': 'いつも テレビを ごらんに なります。',
    },
    'n5-151': {  # ～はいかがですか
        'casual': 'コーヒー どう？',
        'polite': 'コーヒーは いかがですか。',
        'humble': '(self-not-applicable; いかが is for offering to others)',
        'respectful': 'コーヒーは いかがで いらっしゃいますか。 (very formal)',
    },
    'n5-155': {  # 〜が、〜
        'casual': '〜けど、〜。',
        'polite': '〜ですが、〜です。',
        'humble': '〜でございますが、〜でございます。',
        'respectful': '〜でいらっしゃいますが、〜でいらっしゃいます。',
    },
    'n5-157': {  # 〜でしょう
        'casual': '〜だろう。',
        'polite': '〜でしょう。',
        'humble': '(rare; conjecture about self uncommon)',
        'respectful': '〜でいらっしゃるでしょう。',
    },
    'n5-158': {  # 〜だろう
        'casual': '〜だろう。',
        'polite': '〜でしょう。',
        'humble': '〜でございましょう。',
        'respectful': '〜でいらっしゃるだろう。',
    },
    'n5-160': {  # Noun + の + あとで
        'casual': 'がっこうの あとで いく。',
        'polite': 'がっこうの あとで いきます。',
        'humble': 'がっこうの のちで まいります。',
        'respectful': 'がっこうの のちで いらっしゃいます。',
    },
    'n5-161': {  # Noun + の + まえに
        'casual': 'にじの まえに きた。',
        'polite': 'にじの まえに きました。',
        'humble': 'にじの まえに まいりました。',
        'respectful': 'にじの まえに いらっしゃいました。',
    },
    'n5-164': {  # ～さん
        'casual': 'やまだ。 (no honorific)',
        'polite': 'やまださん。',
        'humble': '(N/A — さん is for others)',
        'respectful': 'やまださま。 / やまだ先生。',
    },
    'n5-165': {  # お～ / ご～
        'casual': 'はな。',
        'polite': 'おはな。',
        'humble': 'お／ご- (for beautification, used by self)',
        'respectful': 'おはな (when speaking to/about senior)',
    },
    'n5-168': {  # 〜たり〜たりする
        'casual': 'たべたり よんだり する。',
        'polite': 'たべたり よんだり します。',
        'humble': 'いただいたり はいけんしたり いたします。',
        'respectful': 'めしあがったり ごらんに なったり なさいます。',
    },
    'n5-172': {  # 〜なくてもいい
        'casual': 'たべなくても いい。',
        'polite': 'たべなくても いいです。',
        'humble': '(self-not-applicable in this register)',
        'respectful': 'おたべに ならなくても よろしい です。',
    },
    'n5-173': {  # 〜なくてはいけない
        'casual': 'たべなくちゃ。 (contracted)',
        'polite': 'たべなくては いけません。',
        'humble': 'いただかなくては いけません。',
        'respectful': 'めしあがらなくては いけません。',
    },
    'n5-174': {  # 〜なくてはならない
        'casual': 'たべなくちゃ なんない。',
        'polite': 'たべなくては なりません。',
        'humble': 'いただかなくては なりません。',
        'respectful': 'めしあがらなくては なりません。',
    },
    'n5-175': {  # 〜ないといけない
        'casual': 'たべないと いけない。',
        'polite': 'たべないと いけません。',
        'humble': 'いただかないと いけません。',
        'respectful': 'めしあがらないと いけません。',
    },
    'n5-176': {  # 〜なくちゃ／〜なきゃ (already casual)
        'casual': 'たべなくちゃ。 / たべなきゃ。',
        'polite': 'たべなくては いけません。 / たべなければ なりません。',
        'humble': 'いただかなくては なりません。',
        'respectful': 'めしあがらなくては なりません。',
    },
    'n5-177': {  # 〜すぎる
        'casual': 'たべすぎた。',
        'polite': 'たべすぎました。',
        'humble': 'いただきすぎました。',
        'respectful': 'めしあがりすぎに なりました。',
    },
    'n5-178': {  # つもりだ／つもりです
        'casual': 'たべるつもり。',
        'polite': 'たべるつもりです。',
        'humble': 'いただくつもりで ございます。',
        'respectful': 'めしあがるつもりで いらっしゃいます。',
    },
    'n5-180': {  # Vstem + かた
        'casual': 'たべかたが わからない。',
        'polite': 'たべかたが わかりません。',
        'humble': 'いただきかたが わかりません。',
        'respectful': 'めしあがり かたを ごぞんじですか。',
    },
    'n5-185': {  # だれか／だれも
        'casual': 'だれか いる？',
        'polite': 'だれか いますか。',
        'humble': 'どなたか おりますか。',
        'respectful': 'どなたか いらっしゃいますか。',
    },
    'n5-186': {  # どこか／どこも
        'casual': 'どこか いく？',
        'polite': 'どこかへ いきますか。',
        'humble': 'どこかへ まいりますか。',
        'respectful': 'どこかへ いらっしゃいますか。',
    },
    'n5-187': {  # いつか／いつも
        'casual': 'いつか いきたい。',
        'polite': 'いつか いきたい です。',
        'humble': 'いつか まいりたい と ぞんじます。',
        'respectful': 'いつか いらっしゃりたいと おもって いらっしゃいます。',
    },
}

added = 0
patterns_by_id = {p['id']: p for p in patterns}
for pid, ladder in LADDER.items():
    p = patterns_by_id.get(pid)
    if not p:
        continue
    if p.get('politeness_ladder'):
        continue
    p['politeness_ladder'] = ladder
    p['politeness_ladder_provenance'] = 'llm_curated'
    added += 1

print(f'Patterns with new politeness_ladder: {added}')

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# OOS check
K = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
N5 = set()
for e in K.get('entries', []):
    g = e.get('glyph') or e.get('id','').split('.')[-1]
    if g: N5.add(g)
def is_kanji(c): return 0x4E00 <= ord(c) <= 0x9FFF
oos = {}
for pid in LADDER:
    p = patterns_by_id.get(pid)
    if not p: continue
    pl = p.get('politeness_ladder')
    if not pl: continue
    for k, v in pl.items():
        if isinstance(v, str):
            for c in v:
                if is_kanji(c) and c not in N5:
                    oos.setdefault(c, []).append(pid)
print(f'OOS: {len(oos)} -> {list(oos.keys())}')

total = len(patterns)
ladder_count = sum(1 for p in patterns if p.get('politeness_ladder'))
print()
print('=== FINAL ===')
print(f'  politeness_ladder:  {ladder_count}/{total}')
