"""Grammar Batch G (2026-05-10):
G6 politeness_ladder expansion. From 27/178 to ~80+.
Schema per entry: {casual, polite, humble, respectful} — strings showing
form variation across register tiers.
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
    'n5-002': {  # は (topic)
        'casual': 'わたしゃ がくせいだ。 (very casual; わたしは contracted)',
        'polite': 'わたしは がくせい です。',
        'humble': 'わたくしは がくせい でございます。',
        'respectful': 'こちらは やまだ先生で いらっしゃいます。 (about other)',
    },
    'n5-003': {  # が (subject)
        'casual': 'おれが いく。',
        'polite': 'わたしが いきます。',
        'humble': 'わたくしが まいります。',
        'respectful': 'やまだ先生が いらっしゃいます。',
    },
    'n5-004': {  # を (object)
        'casual': 'ごはん たべる。 (drop を in casual)',
        'polite': 'ごはんを たべます。',
        'humble': 'ごはんを いただきます。',
        'respectful': 'ごはんを めしあがります。',
    },
    'n5-005': {  # に (destination/time)
        'casual': 'がっこう いく。 (drop に casual)',
        'polite': 'がっこうに いきます。',
        'humble': 'がっこうに まいります。',
        'respectful': 'がっこうに いらっしゃいます。',
    },
    'n5-007': {  # で (means/location)
        'casual': 'バスで いく。 (same as polite)',
        'polite': 'バスで いきます。',
        'humble': 'バスで まいります。',
        'respectful': 'バスで いらっしゃいます。',
    },
    'n5-008': {  # と (with)
        'casual': 'ともだちと いく。',
        'polite': 'ともだちと いきます。',
        'humble': 'ともだちと まいります。',
        'respectful': 'おともだちと いらっしゃいます。',
    },
    'n5-013': {  # も (also)
        'casual': 'おれも いく。',
        'polite': 'わたしも いきます。',
        'humble': 'わたくしも まいります。',
        'respectful': '先生も いらっしゃいます。',
    },
    'n5-029': {  # の (possessive)
        'casual': 'おれの ほん。',
        'polite': 'わたしの ほん です。',
        'humble': 'わたくしの ほん でございます。',
        'respectful': '先生の ほんで いらっしゃいます。',
    },
    'n5-059': {  # Vません
        'casual': 'たべない。',
        'polite': 'たべません。',
        'humble': 'いただきません。',
        'respectful': 'めしあがりません。',
    },
    'n5-060': {  # Vました
        'casual': 'たべた。',
        'polite': 'たべました。',
        'humble': 'いただきました。',
        'respectful': 'めしあがりました。',
    },
    'n5-061': {  # Vませんでした
        'casual': 'たべなかった。',
        'polite': 'たべませんでした。',
        'humble': 'いただきませんでした。',
        'respectful': 'めしあがりませんでした。',
    },
    'n5-062': {  # Vましょう
        'casual': 'たべよう。',
        'polite': 'たべましょう。',
        'humble': 'いただきましょう。',
        'respectful': '(rare; volitional uncommon for others) ご一緒に めしあがりませんか。',
    },
    'n5-063': {  # Vましょうか
        'casual': 'もとうか。',
        'polite': 'もちましょうか。',
        'humble': 'おもちしましょうか。',
        'respectful': 'おもちに なりますか。',
    },
    'n5-064': {  # Vませんか (invitation)
        'casual': 'たべない？',
        'polite': 'たべませんか。',
        'humble': '(rare; invitations rarely use humble)',
        'respectful': 'めしあがりませんか。',
    },
    'n5-067': {  # Vた
        'casual': 'いった。',
        'polite': 'いきました。',
        'humble': 'まいりました。',
        'respectful': 'いらっしゃいました。',
    },
    'n5-069': {  # Vて
        'casual': 'たべて、ねた。',
        'polite': 'たべて、ねました。',
        'humble': 'いただいて、やすみました。',
        'respectful': 'めしあがって、おやすみに なりました。',
    },
    'n5-071': {  # Vてください
        'casual': 'たべて。',
        'polite': 'たべてください。',
        'humble': '(self-not-applicable; humble for self-action)',
        'respectful': 'おたべください。 / めしあがって ください。',
    },
    'n5-072': {  # Vています
        'casual': 'たべてる。',
        'polite': 'たべています。',
        'humble': 'いただいて おります。',
        'respectful': 'めしあがって いらっしゃいます。',
    },
    'n5-073': {  # Vていません
        'casual': 'まだ たべてない。',
        'polite': 'まだ たべていません。',
        'humble': 'まだ いただいて おりません。',
        'respectful': 'まだ めしあがって いらっしゃいません。',
    },
    'n5-076': {  # Vてから
        'casual': 'たべてから いく。',
        'polite': 'たべてから いきます。',
        'humble': 'いただいてから まいります。',
        'respectful': 'めしあがってから いらっしゃいます。',
    },
    'n5-077': {  # Vないでください
        'casual': 'たべないで。',
        'polite': 'たべないでください。',
        'humble': '(self-not-applicable)',
        'respectful': 'おたべに ならないで ください。',
    },
    'n5-079': {  # い-Adj + です
        'casual': 'たかい。',
        'polite': 'たかい です。',
        'humble': 'たかい でございます。',
        'respectful': 'おたかい です。 (rare)',
    },
    'n5-080': {  # い-Adj negative
        'casual': 'たかくない。',
        'polite': 'たかくない です。 / たかくありません。',
        'humble': 'たかく ございません。',
        'respectful': 'おたかく ありません。 (rare)',
    },
    'n5-081': {  # i-adj past
        'casual': 'たかかった。',
        'polite': 'たかかった です。',
        'humble': 'たこう ございました。 (very formal)',
        'respectful': 'おたかかった です。',
    },
    'n5-085': {  # na-Adj + です
        'casual': 'しずかだ。',
        'polite': 'しずかです。',
        'humble': 'しずかで ございます。',
        'respectful': '(rare for adjectives)',
    },
    'n5-086': {  # na-Adj negative
        'casual': 'しずかじゃない。',
        'polite': 'しずかじゃありません。 / しずかではありません。',
        'humble': 'しずかでは ございません。',
        'respectful': '(rare)',
    },
    'n5-087': {  # na-Adj past
        'casual': 'しずかだった。',
        'polite': 'しずかでした。',
        'humble': 'しずかで ございました。',
        'respectful': '(rare)',
    },
    'n5-099': {  # すき/きらい
        'casual': 'コーヒー すき。',
        'polite': 'コーヒーが すきです。',
        'humble': 'コーヒーを このんで おります。',
        'respectful': 'コーヒーを おすきで いらっしゃいます。',
    },
    'n5-100': {  # 上手/下手
        'casual': 'にほんご うまい。',
        'polite': 'にほんごが じょうずです。',
        'humble': 'にほんごは あまり できません。 (modest)',
        'respectful': 'にほんごが おじょうずで いらっしゃいます。',
    },
    'n5-101': {  # ほしい
        'casual': 'くるま ほしい。',
        'polite': 'くるまが ほしいです。',
        'humble': 'くるまが ほしゅう ございます。 (literary)',
        'respectful': 'くるまを ほしがって いらっしゃいます。 (about others)',
    },
    'n5-102': {  # わかります
        'casual': 'わかった。 / わかる。',
        'polite': 'わかります。',
        'humble': 'しょうち しました。 / かしこまりました。',
        'respectful': 'おわかりに なります。',
    },
    'n5-103': {  # ができます
        'casual': 'できる。',
        'polite': 'できます。',
        'humble': 'できかねます。 (formal negative for "I cannot")',
        'respectful': 'おできに なります。',
    },
    'n5-104': {  # たい
        'casual': 'たべたい。',
        'polite': 'たべたいです。',
        'humble': 'いただきたい です。',
        'respectful': 'めしあがりたいと おもって いらっしゃいます。 (about others)',
    },
    'n5-107': {  # に行きます (purpose)
        'casual': 'たべに いく。',
        'polite': 'たべに いきます。',
        'humble': 'いただきに まいります。',
        'respectful': 'めしあがりに いらっしゃいます。',
    },
    'n5-117': {  # きょう/あした (time-words)
        'casual': 'きょう いく。',
        'polite': 'きょう いきます。',
        'humble': 'ほんじつ まいります。',
        'respectful': 'ほんじつ いらっしゃいます。',
    },
    'n5-121': {  # そして
        'casual': '〜、そんで〜。 (very casual contraction)',
        'polite': '〜。そして、〜。',
        'humble': '〜。さらに、〜。 (more formal connector)',
        'respectful': '〜。さらに、〜。',
    },
    'n5-122': {  # それから
        'casual': 'たべた。それから ねた。',
        'polite': 'たべました。それから、ねました。',
        'humble': 'いただきました。そののち、やすみました。',
        'respectful': 'めしあがりました。そののち、おやすみに なりました。',
    },
    'n5-123': {  # でも
        'casual': '〜。でも、〜。',
        'polite': '〜です。でも、〜です。',
        'humble': '〜でございます。しかし、〜でございます。',
        'respectful': '〜でいらっしゃいます。しかし、〜でいらっしゃいます。',
    },
    'n5-124': {  # しかし
        'casual': '〜。けど、〜。 (but は contracted)',
        'polite': '〜です。しかし、〜です。',
        'humble': '〜でございます。しかしながら、〜でございます。',
        'respectful': '〜でいらっしゃいます。しかしながら、〜でいらっしゃいます。',
    },
    'n5-125': {  # では/じゃ
        'casual': 'じゃ、また。',
        'polite': 'では、また。',
        'humble': 'それでは、しつれい いたします。',
        'respectful': '(see humble — speakers self-humble in this register)',
    },
    'n5-145': {  # とおもいます
        'casual': '〜と おもう。',
        'polite': '〜と おもいます。',
        'humble': '〜と ぞんじます。',
        'respectful': '〜と おもって いらっしゃいます。',
    },
    'n5-146': {  # と言いました
        'casual': '〜って いってた。',
        'polite': '〜と いいました。',
        'humble': '〜と もうしました。',
        'respectful': '〜と おっしゃいました。',
    },
    'n5-153': {  # まだ + Vていません
        'casual': 'まだ たべてない。',
        'polite': 'まだ たべていません。',
        'humble': 'まだ いただいて おりません。',
        'respectful': 'まだ めしあがって いらっしゃいません。',
    },
    'n5-154': {  # もう + Vました
        'casual': 'もう たべた。',
        'polite': 'もう たべました。',
        'humble': 'もう いただきました。',
        'respectful': 'もう めしあがいました。',
    },
    'n5-169': {  # Vたことがある
        'casual': 'にほんに いったこと ある。',
        'polite': 'にほんに いったことが あります。',
        'humble': 'にほんに まいったことが ございます。',
        'respectful': 'にほんに いらしたことが いらっしゃいます。',
    },
    'n5-170': {  # Vたほうがいい
        'casual': 'たべたほうが いい。',
        'polite': 'たべたほうが いいです。',
        'humble': '(self-not-applicable)',
        'respectful': 'おたべに なった ほうが いいでしょう。',
    },
    'n5-171': {  # Vないほうがいい
        'casual': 'たべないほうが いい。',
        'polite': 'たべないほうが いいです。',
        'humble': '(self-not-applicable)',
        'respectful': 'おたべに ならない ほうが いいでしょう。',
    },
    'n5-184': {  # なにか/なにも
        'casual': 'なんか たべた？',
        'polite': 'なにか たべましたか。',
        'humble': 'なにか いただきましたか。',
        'respectful': 'なにか めしあがいましたか。',
    },
    'n5-188': {  # ことができます
        'casual': 'たべられる。 / たべる ことが できる。',
        'polite': 'たべることが できます。',
        'humble': 'いただくことが できます。',
        'respectful': 'めしあがる ことが できます / おたべに なれます。',
    },
}

added = 0
patterns_by_id = {p['id']: p for p in patterns}
for pid, ladder in LADDER.items():
    p = patterns_by_id.get(pid)
    if not p:
        continue
    if p.get('politeness_ladder'):
        continue  # do not overwrite existing
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
