"""Rewrite KnowledgeBank/grammar_examples_n4.md to use only in-scope kanji.

The N4 whitelist is 249 kanji (N5 + N4 union). The first cut of the curated
examples used 43 kanji outside this set (e.g., 宿題, 好き, 降り, 寒). This
script replaces those out-of-scope words with their kana readings, preserving
naturalness while satisfying JA-13.

The kanji→kana mapping below is hand-curated for the specific words used in
grammar_examples_n4.md as of 2026-05-04. Idempotent: re-running on already
fixed text is a no-op.
"""
import io, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
PATH = ROOT / 'KnowledgeBank' / 'grammar_examples_n4.md'

# Word-level replacements: out-of-scope kanji compound -> kana equivalent
# Using ONLY in-scope kanji or kana to satisfy JA-13.
REPLACEMENTS = [
    # Out-of-scope individual words
    ('出かけている', 'でかけている'),
    ('出かけ', 'でかけ'),
    ('出ない', 'でない'),
    ('宿題', 'しゅくだい'),
    ('好き', 'すき'),
    ('好きじゃ', 'すきじゃ'),
    ('降りません', 'ふりません'),
    ('降ります', 'ふります'),
    ('降る', 'ふる'),
    ('降って', 'ふって'),
    ('降った', 'ふった'),
    ('降ら', 'ふら'),
    ('降り出', 'ふりだ'),
    ('降り', 'ふり'),
    ('寒がり', 'さむがり'),
    ('寒い', 'さむい'),
    ('寒く', 'さむく'),
    ('寒くて', 'さむくて'),
    ('寒さ', 'さむさ'),
    ('寒', 'さむ'),
    ('受付', 'うけつけ'),
    ('受', 'う'),
    ('結婚', 'けっこん'),
    ('引っ越', 'ひっこ'),
    ('引っ越す', 'ひっこす'),
    ('引', 'ひ'),
    ('掃除', 'そうじ'),
    ('撮って', 'とって'),
    ('撮', 'と'),
    ('紅茶', 'こうちゃ'),
    ('米から', 'こめから'),
    ('座り', 'すわり'),
    ('案内', 'あんない'),
    ('部屋', 'へや'),
    ('部', 'ぶ'),
    ('全部', 'ぜんぶ'),
    ('内', 'うち'),
    ('続けて', 'つづけて'),
    ('続け', 'つづけ'),
    ('続いた', 'つづいた'),
    ('続', 'つづ'),
    ('遊びに', 'あそびに'),
    ('遊び', 'あそび'),
    ('一緒', 'いっしょ'),
    ('緒', 'しょ'),
    ('一緒に', 'いっしょに'),
    ('払いました', 'はらいました'),
    ('払い', 'はらい'),
    ('払', 'はら'),
    ('違いました', 'ちがいました'),
    ('違い', 'ちがい'),
    ('違', 'ちが'),
    ('間違い', 'まちがい'),
    ('選んで', 'えらんで'),
    ('選', 'えら'),
    ('飛び', 'とび'),
    ('飛びたい', 'とびたい'),
    ('飛', 'と'),
    ('易しい', 'やさしい'),
    ('易', 'やさ'),
    ('覚えられ', 'おぼえられ'),
    ('覚え', 'おぼえ'),
    ('守', 'まも'),
    ('約束', 'やくそく'),
    ('議', 'ぎ'),
    ('会議', 'かいぎ'),
    ('合', 'あ'),
    ('場合', 'ばあい'),
    ('合い', 'あい'),
    ('都', 'と'),
    ('京都', 'きょうと'),
    ('笑って', 'わらって'),
    ('笑', 'わら'),
    ('咲', 'さ'),
    ('咲きます', 'さきます'),
    ('晴れる', 'はれる'),
    ('晴', 'は'),
    ('留学', 'りゅうがく'),
    ('留', 'りゅう'),
    ('難しい', 'むずかしい'),
    ('難', 'むずか'),
    ('引っ越し', 'ひっこし'),
    ('一束', 'いっそく'),
    ('束', 'たば'),
    ('案', 'あん'),
    ('付', 'つ'),
    ('気がつき', 'きがつき'),
    ('気がついた', 'きがついた'),
    ('気がつく', 'きがつく'),
    ('寝なさい', 'ねなさい'),
    ('寝', 'ね'),
    ('君', 'きみ'),
    ('君の', 'きみの'),
    ('除', 'じょ'),
    ('掃', 'そう'),
    ('守ら', 'まもら'),
    ('受け', 'うけ'),
    ('易さ', 'やさしさ'),
    ('結', 'けつ'),
]

text = PATH.read_text(encoding='utf-8')
orig = text
applied = 0
for old, new in REPLACEMENTS:
    if old in text:
        before = text.count(old)
        text = text.replace(old, new)
        applied += before
print(f'Replacements applied: {applied}')

if text != orig:
    PATH.write_text(text, encoding='utf-8')
    print(f'Updated: {PATH.relative_to(ROOT)}')
else:
    print('No changes needed (idempotent).')
