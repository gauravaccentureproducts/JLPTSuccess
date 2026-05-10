"""Grammar Batch P (2026-05-11):
G6 politeness_ladder — close from 115/178 to 178/178.
For 'register-invariant words' (particles, demonstratives, counters), the
ladder still applies because the SURROUNDING UTTERANCE shifts register.
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
    'n5-014': {  # これ/それ/あれ/どれ
        'casual': 'これ、なに？',
        'polite': 'これは なんですか。',
        'humble': 'こちらは なんでございましょうか。',
        'respectful': 'こちらは なにでいらっしゃいますか。 (rare)',
    },
    'n5-015': {  # この+N
        'casual': 'この ほん、おもしろい。',
        'polite': 'この ほんは おもしろいです。',
        'humble': 'こちらの ほんは おもしろうございます。',
        'respectful': 'こちらの ほんを ごらんに なって ください。',
    },
    'n5-016': {  # ここ/そこ/あそこ/どこ
        'casual': 'ここ、いい ね。',
        'polite': 'ここは いいですね。',
        'humble': 'こちらは いいところで ございますね。',
        'respectful': 'こちらは いい ところで いらっしゃいますね。',
    },
    'n5-017': {  # 何
        'casual': 'なに、これ？',
        'polite': 'これは なんですか。',
        'humble': 'これは なんでございましょうか。',
        'respectful': 'こちらは なんで いらっしゃいますか。',
    },
    'n5-019': {  # いつ
        'casual': 'いつ いく？',
        'polite': 'いつ いきますか。',
        'humble': 'いつ まいりますか。',
        'respectful': 'いつ いらっしゃいますか。',
    },
    'n5-023': {  # か (question)
        'casual': 'いく？ (intonation only)',
        'polite': 'いきますか。',
        'humble': 'まいりますか。',
        'respectful': 'いらっしゃいますか。',
    },
    'n5-024': {  # か (or)
        'casual': 'コーヒーか こうちゃ？',
        'polite': 'コーヒーか こうちゃ、 どちらに しますか。',
        'humble': 'コーヒーか こうちゃ、 どちらに いたしましょうか。',
        'respectful': 'コーヒーか こうちゃ、 いかがで いらっしゃいますか。',
    },
    'n5-025': {  # ね
        'casual': 'いいね。',
        'polite': 'いいですね。',
        'humble': 'いいで ございますね。',
        'respectful': 'いいで いらっしゃいますね。',
    },
    'n5-026': {  # よ
        'casual': 'いいよ。',
        'polite': 'いいですよ。',
        'humble': 'いいで ございますよ。',
        'respectful': '(よ rarely used in highest respectful register; sounds too assertive)',
    },
    'n5-027': {  # よね
        'casual': 'おいしいよね。',
        'polite': 'おいしいですよね。',
        'humble': 'おいしゅう ございますよね。',
        'respectful': '(よね rarely used at highest register)',
    },
    'n5-028': {  # の (modifier)
        'casual': 'おれの ほん。',
        'polite': 'わたしの ほんです。',
        'humble': 'わたくしの ほんで ございます。',
        'respectful': '先生の ほんで いらっしゃいます。',
    },
    'n5-030': {  # nominalizer の
        'casual': 'よむのが すき。',
        'polite': 'よむのが すきです。',
        'humble': 'よむのが すきで ございます。',
        'respectful': 'よむのが おすきで いらっしゃいます。',
    },
    'n5-031': {  # の (pronoun)
        'casual': 'あかいの ちょうだい。',
        'polite': 'あかいのを ください。',
        'humble': 'あかいのを いただけませんか。',
        'respectful': 'あかいのを おもとめに なりますか。',
    },
    'n5-033': {  # だけ
        'casual': 'ひとりだけ きた。',
        'polite': 'ひとりだけ きました。',
        'humble': 'ひとりだけ まいりました。',
        'respectful': 'ひとりだけ いらっしゃいました。',
    },
    'n5-034': {  # しか〜ない
        'casual': 'ひゃくえんしか ない。',
        'polite': 'ひゃくえんしか ありません。',
        'humble': 'ひゃくえんしか ございません。',
        'respectful': '(highest register would reframe; しか + neg too curt)',
    },
    'n5-035': {  # ぐらい/くらい
        'casual': 'いちじかんぐらい かかる。',
        'polite': 'いちじかんぐらい かかります。',
        'humble': 'いちじかんぐらい かかります。 (humble for self-time uncommon)',
        'respectful': 'いちじかんぐらい おかかりに なります。',
    },
    'n5-036': {  # ごろ
        'casual': 'にじごろ いく。',
        'polite': 'にじごろ いきます。',
        'humble': 'にじごろ まいります。',
        'respectful': 'にじごろ いらっしゃいます。',
    },
    'n5-037': {  # など
        'casual': 'りんごやみかんなど かう。',
        'polite': 'りんごや みかんなどを かいます。',
        'humble': 'りんごや みかんなどを ちょうだい いたします。',
        'respectful': 'りんごや みかんなどを おもとめに なります。',
    },
    'n5-038': {  # ずつ
        'casual': 'いっこずつ あげる。',
        'polite': 'いっこずつ あげます。',
        'humble': 'いっこずつ さしあげます。',
        'respectful': 'いっこずつ おもらいに なります。 (rare)',
    },
    'n5-039': {  # これ/それ/あれ (dup)
        'casual': 'これ、なに？',
        'polite': 'これは なんですか。',
        'humble': 'こちらは なんでございましょうか。',
        'respectful': 'こちらは なんで いらっしゃいますか。',
    },
    'n5-040': {  # この+N (dup)
        'casual': 'この ほん、おもしろい。',
        'polite': 'この ほんは おもしろいです。',
        'humble': 'こちらの ほんは おもしろうございます。',
        'respectful': 'こちらの ほんを ごらんに なって ください。',
    },
    'n5-041': {  # ここ (dup)
        'casual': 'ここ、いい。',
        'polite': 'ここは いいです。',
        'humble': 'こちらは いいで ございます。',
        'respectful': 'こちらは いいところで いらっしゃいます。',
    },
    'n5-042': {  # こちら/そちら etc.
        'casual': 'こっち。 / そっち。',
        'polite': 'こちらです。 / そちらです。',
        'humble': 'こちらで ございます。',
        'respectful': 'こちらで いらっしゃいます。',
    },
    'n5-043': {  # こんな/そんな + N
        'casual': 'こんな ほん、すき。',
        'polite': 'こんな ほんが すきです。',
        'humble': 'こんな ほんが すきで ございます。',
        'respectful': 'こんな ほんを おすきで いらっしゃいます。',
    },
    'n5-044': {  # こう/そう/ああ/どう
        'casual': 'こう する。',
        'polite': 'こう します。',
        'humble': 'こう いたします。',
        'respectful': 'こう なさいます。',
    },
    'n5-045': {  # 何 (dup)
        'casual': 'なに する？',
        'polite': 'なにを しますか。',
        'humble': 'なにを いたしましょうか。',
        'respectful': 'なにを なさいますか。',
    },
    'n5-048': {  # どこ
        'casual': 'どこ いく？',
        'polite': 'どこに いきますか。',
        'humble': 'どこに まいりましょうか。',
        'respectful': 'どこに いらっしゃいますか。',
    },
    'n5-049': {  # どれ/どの/どちら
        'casual': 'どれ？',
        'polite': 'どれですか。',
        'humble': 'どれでございましょうか。',
        'respectful': 'どちらで いらっしゃいますか。',
    },
    'n5-052': {  # どうやって
        'casual': 'どうやって いく？',
        'polite': 'どうやって いきますか。',
        'humble': 'どうやって まいりましょうか。',
        'respectful': 'どうやって いらっしゃいますか。',
    },
    'n5-053': {  # いくら
        'casual': 'いくら？',
        'polite': 'いくらですか。',
        'humble': 'いくらでございましょうか。',
        'respectful': 'いくらで いらっしゃいますか。',
    },
    'n5-054': {  # いくつ
        'casual': 'いくつ？',
        'polite': 'いくつですか。',
        'humble': 'おいくつで ございますか。',
        'respectful': 'おいくつで いらっしゃいますか。',
    },
    'n5-055': {  # なんじ
        'casual': 'なんじ？',
        'polite': 'なんじですか。',
        'humble': 'なんじでございましょうか。',
        'respectful': '(time-asking rarely escalates to highest register)',
    },
    'n5-056': {  # なんようび
        'casual': 'なんようび？',
        'polite': 'なんようびですか。',
        'humble': 'なんようびでございましょうか。',
        'respectful': '(rare highest register for day-asking)',
    },
    'n5-057': {  # なんがつ なんにち
        'casual': 'なんにち？',
        'polite': 'なんがつ なんにちですか。',
        'humble': 'なんがつ なんにちでございましょうか。',
        'respectful': '(rare highest register)',
    },
    'n5-065': {  # Vる/Vう plain
        'casual': 'たべる。 / いく。',
        'polite': 'たべます。 / いきます。',
        'humble': 'いただきます。 / まいります。',
        'respectful': 'めしあがります。 / いらっしゃいます。',
    },
    'n5-078': {  # い-Adj + N
        'casual': 'たかい ほん。',
        'polite': 'たかい ほんです。',
        'humble': 'おたかい ほんで ございます。',
        'respectful': 'おたかい ほんで いらっしゃいます。 (rare)',
    },
    'n5-083': {  # い-Adj te-form
        'casual': 'おいしくて やすい。',
        'polite': 'おいしくて やすいです。',
        'humble': 'おいしゅう ございまして やすうございます。',
        'respectful': '(literary humble form rarely used in conversation)',
    },
    'n5-084': {  # na-Adj + な + N
        'casual': 'しずかな まち。',
        'polite': 'しずかな まちです。',
        'humble': 'しずかな まちで ございます。',
        'respectful': 'しずかな まちで いらっしゃいます。',
    },
    'n5-089': {  # na-Adj te-form
        'casual': 'しずかで きれい。',
        'polite': 'しずかで きれいです。',
        'humble': 'しずかで きれいで ございます。',
        'respectful': '(rare)',
    },
    'n5-092': {  # に〜があります/います
        'casual': 'つくえに ほんが ある。',
        'polite': 'つくえに ほんが あります。',
        'humble': 'つくえに ほんが ございます。',
        'respectful': 'つくえに ほんが いらっしゃいます。 (rare, only for people)',
    },
    'n5-093': {  # は〜にあります/います
        'casual': 'ほんは つくえに ある。',
        'polite': 'ほんは つくえに あります。',
        'humble': 'ほんは つくえに ございます。',
        'respectful': '(rare for inanimate)',
    },
    'n5-094': {  # 〜があります
        'casual': 'おかねが ある。',
        'polite': 'おかねが あります。',
        'humble': 'おかねが ございます。',
        'respectful': '(possession rarely at highest respectful)',
    },
    'n5-095': {  # は〜より〜です
        'casual': 'にほんは アメリカより ちいさい。',
        'polite': 'にほんは アメリカより ちいさいです。',
        'humble': 'にほんは アメリカより ちいそう ございます。',
        'respectful': '(comparison rarely at highest register)',
    },
    'n5-096': {  # より〜のほうが
        'casual': 'コーヒーより こうちゃの ほうが すき。',
        'polite': 'コーヒーより こうちゃの ほうが すきです。',
        'humble': 'コーヒーより こうちゃの ほうが すきで ございます。',
        'respectful': 'コーヒーより こうちゃの ほうが おすきで いらっしゃいます。',
    },
    'n5-097': {  # と〜と、どちらが
        'casual': 'コーヒーと こうちゃと、 どっちが すき？',
        'polite': 'コーヒーと こうちゃと、 どちらが すきですか。',
        'humble': 'コーヒーと こうちゃと、 どちらが すきで ございましょうか。',
        'respectful': 'コーヒーと こうちゃと、 どちらが おすきで いらっしゃいますか。',
    },
    'n5-098': {  # 〜 (placeholder)
        'casual': 'これ、 すき。',
        'polite': 'これが すきです。',
        'humble': 'これが すきで ございます。',
        'respectful': 'これが おすきで いらっしゃいます。',
    },
    'n5-106': {  # Noun + ほしい
        'casual': 'くるま ほしい。',
        'polite': 'くるまが ほしいです。',
        'humble': 'くるまが ほしゅう ございます。',
        'respectful': 'くるまを ほしがって いらっしゃいます。 (about other)',
    },
    'n5-108': {  # Number + counter
        'casual': 'みっつ ある。',
        'polite': 'みっつ あります。',
        'humble': 'みっつ ございます。',
        'respectful': '(rare highest register for counting)',
    },
    'n5-109': {  # counter-question
        'casual': 'なんにん？',
        'polite': 'なんにんですか。',
        'humble': 'なんにんで ございますか。',
        'respectful': 'なんにんで いらっしゃいますか。 (about a group)',
    },
    'n5-110': {  # V + counter + V
        'casual': 'ふたつ かった。',
        'polite': 'ふたつ かいました。',
        'humble': 'ふたつ ちょうだい いたしました。',
        'respectful': 'ふたつ おもとめに なりました。',
    },
    'n5-111': {  # じ
        'casual': 'にじ。',
        'polite': 'にじです。',
        'humble': 'にじでございます。',
        'respectful': '(rare highest register for time)',
    },
    'n5-112': {  # ふん/ぷん
        'casual': 'にじゅっぷん。',
        'polite': 'にじゅっぷんです。',
        'humble': 'にじゅっぷんでございます。',
        'respectful': '(rare highest register)',
    },
    'n5-113': {  # じはん
        'casual': 'にじはん。',
        'polite': 'にじはんです。',
        'humble': 'にじはんでございます。',
        'respectful': '(rare)',
    },
    'n5-114': {  # から〜まで (range, dup)
        'casual': '8じから 5じまで はたらく。',
        'polite': '8じから 5じまで はたらきます。',
        'humble': '8じから 5じまで はたらいて おります。',
        'respectful': '8じから 5じまで はたらいて いらっしゃいます。',
    },
    'n5-116': {  # まいにち
        'casual': 'まいにち コーヒー のむ。',
        'polite': 'まいにち コーヒーを のみます。',
        'humble': 'まいにち コーヒーを いただきます。',
        'respectful': 'まいにち コーヒーを めしあがります。',
    },
    'n5-135': {  # V-plain + N (relative)
        'casual': 'よむ ほんが ない。',
        'polite': 'よむ ほんが ありません。',
        'humble': 'よむ ほんが ございません。',
        'respectful': '(rare for inanimate possession)',
    },
    'n5-136': {  # Adj + N
        'casual': 'たかい ほん。',
        'polite': 'たかい ほんです。',
        'humble': 'おたかい ほんで ございます。',
        'respectful': 'おたかい ほんで いらっしゃいます。 (rare)',
    },
    'n5-137': {  # N + の + N
        'casual': 'わたしの ほん。',
        'polite': 'わたしの ほんです。',
        'humble': 'わたくしの ほんで ございます。',
        'respectful': '先生の ほんで いらっしゃいます。',
    },
    'n5-162': {  # V + まえに (alias of 119)
        'casual': 'たべるまえに、 てを あらう。',
        'polite': 'たべるまえに、 てを あらいます。',
        'humble': 'いただくまえに、 てを あらいます。',
        'respectful': 'めしあがるまえに、 てを おあらいに なります。',
    },
    'n5-163': {  # V-た + あとで (alias of 120)
        'casual': 'たべた あとで ねる。',
        'polite': 'たべた あとで ねます。',
        'humble': 'いただいた あとで やすみます。',
        'respectful': 'めしあがった あとで、 おやすみに なります。',
    },
    'n5-181': {  # なあ
        'casual': 'たかいなあ。',
        'polite': 'たかいですなあ。 (rare, sounds old-fashioned)',
        'humble': 'たかうございますね。',
        'respectful': '(exclamatory なあ is casual by nature)',
    },
    'n5-182': {  # Vplain + な (prohibitive)
        'casual': 'たべるな。',
        'polite': 'たべないで ください。',
        'humble': 'おたべに ならないで ください。',
        'respectful': 'おたべに なりませんように。',
    },
    'n5-183': {  # Q + か/も
        'casual': 'なにか たべた？ / なにも たべない。',
        'polite': 'なにか たべましたか。 / なにも たべません。',
        'humble': 'なにか いただきましたか。 / なにも いただきません。',
        'respectful': 'なにか めしあがいましたか。 / なにも めしあがりません。',
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

total = len(patterns)
ladder_count = sum(1 for p in patterns if p.get('politeness_ladder'))
print()
print('=== FINAL ===')
print(f'  politeness_ladder:  {ladder_count}/{total}')
