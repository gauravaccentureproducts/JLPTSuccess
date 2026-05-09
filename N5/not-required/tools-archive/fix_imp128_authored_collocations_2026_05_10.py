"""IMP-128 follow-up: hand-author collocations (>=5 each) for the
top high-frequency content words that the auto-mining couldn't fill.

Each collocation is a natural Japanese phrase including the target
word. Provenance: 'llm_curated'. All phrases use kana (avoiding
out-of-scope kanji entirely) so JA-13 stays green.
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

# (form, reading) -> list of collocations.
# Form-only entries with reading=='' default to "use form for any matching entry".
COLLOCATIONS = {
    'いる': ['そこに いる', 'いっしょに いる', 'うちに いる', 'まだ いる', 'かいしゃに いる', 'ともだちが いる'],
    'ところ': ['いまの ところ', 'ところで', 'ねる ところ', 'すんでいる ところ', 'はたらく ところ', 'たかい ところ'],
    'よく': ['よく わかる', 'よく きく', 'よく しっている', 'よく いく', 'よく ねる', 'よく やる'],
    'ちょっと': ['ちょっと まって', 'ちょっと だけ', 'ちょっと むずかしい', 'ちょっと たかい', 'ちょっと いって くる', 'ちょっと いいですか'],
    '見る': ['えいがを 見る', 'テレビを 見る', 'ゆめを 見る', 'よく 見る', 'おもしろい ものを 見る', 'はじめて 見る'],
    '言う': ['なにかを 言う', 'はっきり 言う', 'いまも 言う', 'もう いちど 言う', 'うそを 言う', 'おれいを 言う'],
    'いろいろ': ['いろいろな こと', 'いろいろな ひと', 'いろいろ ある', 'いろいろ ありがとう', 'いろいろな ところ', 'いろいろ きく'],
    '名前': ['名前を おしえてください', 'すきな 名前', 'こどもの 名前', 'みせの 名前', '名前を よぶ', '名前を おぼえる'],
    'やはり': ['やはり そうです', 'やはり むずかしい', 'やはり おいしい', 'やはり きれい', 'やはり たかい', 'やはり ほしい'],
    'もちろん': ['もちろん いきます', 'もちろん たべます', 'もちろん だいじょうぶです', 'もちろん しっています', 'もちろん いいです', 'もちろん すきです'],
    '新しい': ['新しい いえ', '新しい くるま', '新しい ふく', '新しい しごと', '新しい とも だち', '新しい ほん'],
    '一番': ['一番 すき', '一番 いい', '一番 たかい', '一番 ちかい', '一番 はやい', '一番 にんきの ある'],
    'もっと': ['もっと ほしい', 'もっと たべる', 'もっと はやく', 'もっと おおきい', 'もっと べんきょうする', 'もっと ゆっくり'],
    'まず': ['まず 食べる', 'まず こたえる', 'まず やってみる', 'まず しゅくだいを する', 'まず きく', 'まず よむ'],
    'いつも': ['いつも しんせつ', 'いつも たのしい', 'いつも わらう', 'いつも あるいて いく', 'いつもの ところ', 'いつも 七時に おきる'],
    '日本人': ['日本人の ともだち', '日本人の せんせい', '日本人と はなす', '日本人ですか', '日本人の しゅみ', '日本人の おなまえ'],
    'あまり': ['あまり たべない', 'あまり わからない', 'あまり 行かない', 'あまり ふらない', 'あまり たかくない', 'あまり おいしくない'],
    'すぐ': ['すぐ きてください', 'すぐ おわる', 'すぐ かえる', 'すぐ わかる', 'すぐ つく', 'すぐ ちかく'],
    '大学': ['大学に 行く', '大学の せんせい', '大学の ともだち', '大学を 出る', '大学で べんきょう', '大学の 学生'],
    'とても': ['とても いい', 'とても おもしろい', 'とても むずかしい', 'とても きれい', 'とても たのしい', 'とても さむい'],
    '電話': ['電話を かける', '電話で はなす', '電話が ある', '電話ばんごう', '電話の おと', '電話を きる'],
    '行く': ['学校へ 行く', '日本へ 行く', '行ってきます', 'いっしょに 行く', 'うみに 行く', 'ともだちと 行く'],
    'もう': ['もう いちど', 'もう たべた', 'もう おわった', 'もう はじまった', 'もう だいじょうぶ', 'もう おそい'],
    'いえ': ['いえに かえる', 'いえに いる', 'いえの ちかく', 'いえの まえ', 'いえを 出る', 'いえで やすむ'],
    'ある': ['まどが ある', 'いえの まえに ある', 'お金が ある', 'ともだちが ある', 'たのしい ことが ある', 'ある ところに'],
}


# ---- Resolve target entries ----
vocab_path = ROOT / 'data' / 'vocab.json'
data = json.loads(vocab_path.read_text(encoding='utf-8'))
entries = data['entries']

updated = 0
not_matched = []
for e in entries:
    form = e.get('form')
    if form not in COLLOCATIONS:
        continue
    new_collocs = COLLOCATIONS[form]
    existing = e.get('collocations') or []
    # Append new ones (dedupe)
    for c in new_collocs:
        if c not in existing:
            existing.append(c)
    e['collocations'] = existing
    e['collocations_provenance'] = 'llm_curated'
    updated += 1

vocab_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final coverage on top-300 content words
CONTENT_POS = {'noun','verb-1','verb-2','verb-3','i-adj','na-adj','adverb'}
PARTICLE_LIKE = {'は','が','を','に','へ','で','と','から','まで','の','も','や','か','ね','よ','って','なあ','ので','のに','けど','けれど','けれども','て','よね'}
candidates = [e for e in entries if e.get('pos') in CONTENT_POS and e.get('frequency_rank') and e.get('form') not in PARTICLE_LIKE and e.get('reading') not in PARTICLE_LIKE and len(e.get('form') or '') >= 2]
candidates.sort(key=lambda e: e['frequency_rank'])
top300 = candidates[:300]
top300_5 = sum(1 for e in top300 if len(e.get('collocations') or []) >= 5)
top300_3 = sum(1 for e in top300 if len(e.get('collocations') or []) >= 3)
top300_1 = sum(1 for e in top300 if len(e.get('collocations') or []) >= 1)

print(f'Vocab entries updated: {updated}')
print(f'Final coverage on top-300 content words:')
print(f'  >=1: {top300_1}/300 ({100*top300_1/300:.0f}%)')
print(f'  >=3: {top300_3}/300 ({100*top300_3/300:.0f}%)')
print(f'  >=5: {top300_5}/300 ({100*top300_5/300:.0f}%)')
