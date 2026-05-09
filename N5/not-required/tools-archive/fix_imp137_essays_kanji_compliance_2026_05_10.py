"""IMP-137 follow-up: convert out-of-scope kanji in essay text to
kana to satisfy the JA-13 invariant (no out-of-scope kanji in
user-facing data).

The essays I authored used native-fluent kanji (誰, 公園, 図書館,
etc.) that aren't on the N5 whitelist. The JA-13 invariant scans
user-facing fields and rejects any non-whitelist CJK ideograph.
This script does compound-aware substitution: first replace known
compounds with kana, then catch stragglers char-by-char.
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

# Compound replacements applied first (longest first to win).
# These cover words a learner might naturally write with kanji
# but where the kanji aren't on the N5 list.
COMPOUNDS = [
    ('図書館', 'としょかん'),
    ('教科書', 'きょうかしょ'),
    ('鉛筆', 'えんぴつ'),
    ('家族', 'かぞく'),
    ('家庭', 'かてい'),
    ('東京', 'とうきょう'),
    ('北海道', 'ほっかいどう'),
    ('結婚', 'けっこん'),
    ('宿題', 'しゅくだい'),
    ('勉強', 'べんきょう'),
    ('果物', 'くだもの'),
    ('部屋', 'へや'),
    ('公園', 'こうえん'),
    ('仕事', 'しごと'),
    ('教師', 'きょうし'),
    ('教える', 'おしえる'),
    ('遅い', 'おそい'),
    ('遅れる', 'おくれる'),
    ('寒い', 'さむい'),
    ('静か', 'しずか'),
    ('住む', 'すむ'),
    ('住所', 'じゅうしょ'),
    ('閉める', 'しめる'),
    ('閉まる', 'しまる'),
    ('開ける', 'あける'),
    ('開く', 'あく'),
    ('帰る', 'かえる'),
    ('知る', 'しる'),
    ('知っている', 'しっている'),
    ('遊ぶ', 'あそぶ'),
    ('歩く', 'あるく'),
    ('歩きます', 'あるきます'),
    ('起きる', 'おきる'),
    ('起きます', 'おきます'),
    ('持つ', 'もつ'),
    ('持っている', 'もっている'),
    ('持っています', 'もっています'),
    ('明日', 'あした'),
    ('明後日', 'あさって'),
    ('混む', 'こむ'),
    ('混んでいます', 'こんでいます'),
    ('疲れる', 'つかれる'),
    ('疲れた', 'つかれた'),
    ('向かう', 'むかう'),
    ('向かいます', 'むかいます'),
    ('事', 'こと'),
    ('物', 'もの'),
    ('物を', 'ものを'),
    ('犬', 'いぬ'),
    ('猫', 'ねこ'),
    ('机', 'つくえ'),
    ('紙', 'かみ'),
    ('朝', 'あさ'),
    ('朝ごはん', 'あさごはん'),
    ('飲み物', 'のみもの'),
    ('食べ物', 'たべもの'),
    ('果', 'か'),  # shouldn't appear standalone but safety
    ('1個', '1こ'),
    ('1枚', '1まい'),
    ('1冊', '1さつ'),
    ('一枚', 'いちまい'),
    ('一冊', 'いっさつ'),
    ('一個', 'いっこ'),
    ('3冊', '3さつ'),
    ('5枚', '5まい'),
    ('誰', 'だれ'),
]

# Single-char fallbacks for any out-of-scope chars left after the
# compound pass.
SINGLE_FALLBACK = {
    '事': 'こと',
    '京': 'きょう',
    '仕': 'し',
    '住': 'す',
    '個': 'こ',
    '公': 'こう',
    '冊': 'さつ',
    '勉': 'べん',
    '向': 'む',
    '図': 'ず',
    '園': 'えん',
    '婚': 'こん',
    '家': 'いえ',
    '宿': 'しゅく',
    '寒': 'さむ',
    '屋': 'や',
    '帰': 'かえ',
    '強': 'きょう',
    '持': 'も',
    '教': 'きょう',
    '明': 'あ',
    '朝': 'あさ',
    '机': 'つくえ',
    '枚': 'まい',
    '果': 'か',
    '歩': 'ある',
    '混': 'こ',
    '物': 'もの',
    '犬': 'いぬ',
    '猫': 'ねこ',
    '疲': 'つか',
    '知': 'し',
    '科': 'か',
    '筆': 'ぴつ',
    '紙': 'かみ',
    '結': 'けっ',
    '誰': 'だれ',
    '起': 'お',
    '遅': 'おそ',
    '遊': 'あそ',
    '部': 'へ',
    '鉛': 'えん',
    '閉': 'し',
    '開': 'あ',
    '静': 'しず',
    '題': 'だい',
    '館': 'かん',
}


def kana_compliant(text: str) -> str:
    """Replace out-of-scope kanji compounds, then any leftover chars."""
    for compound, kana in sorted(COMPOUNDS, key=lambda x: -len(x[0])):
        text = text.replace(compound, kana)
    # Remaining single-char substitutions
    out = []
    for c in text:
        if c in SINGLE_FALLBACK:
            out.append(SINGLE_FALLBACK[c])
        else:
            out.append(c)
    return ''.join(out)


# ---- Apply ----
grammar_path = ROOT / 'data' / 'grammar.json'
data = json.loads(grammar_path.read_text(encoding='utf-8'))
patterns = data['patterns']

# Whitelist for verification
kdata = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
kentries = kdata.get('entries', kdata) if isinstance(kdata, dict) else kdata
whitelist = set()
for k in kentries:
    g = k.get('glyph') or (k.get('id', '').split('.')[-1])
    if g:
        whitelist.add(g)

ESSAY_FIELDS = ['intro', 'why_it_matters', 'common_pitfalls', 'contrasts', 'closing_practice_tip']

modified = 0
remaining_oos = []
for p in patterns:
    essay = p.get('essay')
    if not isinstance(essay, dict):
        continue
    for fld in ESSAY_FIELDS:
        original = essay.get(fld)
        if not original or not isinstance(original, str):
            continue
        cleaned = kana_compliant(original)
        if cleaned != original:
            essay[fld] = cleaned
            modified += 1
        # Verify no out-of-scope chars remain
        for c in cleaned:
            if '一' <= c <= '鿿' and c not in whitelist:
                remaining_oos.append((p['id'], fld, c))

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print(f'Essay sub-fields modified: {modified}')
print(f'Remaining out-of-scope chars: {len(remaining_oos)}')
if remaining_oos:
    for pid, fld, c in remaining_oos[:10]:
        print(f'  {pid}.{fld}: {c!r}')
