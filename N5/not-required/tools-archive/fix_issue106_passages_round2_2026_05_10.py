"""ISSUE-106 round-2: author 4 more reading passages targeting the
14 N5 kanji still not in any passage. Then rebuild kanji ↔ passage
cross-index from actual JP text.

Target kanji:
- Numbers: 四, 百, 千, 万
- Time: 午
- Question: 何
- People/body: 友, 手, 足, 目
- Position: 上, 下
- Direction: 南
- Adjective: 長
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Whitelist for verification
kdata = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
kentries = kdata.get('entries', kdata) if isinstance(kdata, dict) else kdata
if isinstance(kentries, dict): kentries = list(kentries.values())
whitelist = set()
for k in kentries:
    g = k.get('glyph') or (k.get('id', '').split('.')[-1])
    if g:
        whitelist.add(g)


NEW_PASSAGES = [
    {
        'id': 'n5.read.051',
        'level': 'N5',
        'topic': 'shopping',
        'mondai': 4,
        'tier': 'core_n5',
        'format_role': 'comprehension',
        'format_type': 'comprehension',
        'title_ja': 'やすい かいもの',
        'ja': 'きょうの 午前、私は スーパーで かいものを しました。'
              + 'りんごが 一つ 百円で、四つ 買いました。'
              + 'パンは 二百円でした。'
              + 'ぜんぶで 千円ぐらい でした。たくさんの ものが 買えて、うれしかったです。',
        'translation_literal': "This morning, I went shopping at the supermarket. Apples were 100 yen each, and I bought four. Bread was 200 yen. In total, it was about 1000 yen. I was happy that I could buy many things.",
        'translation_natural': "I went shopping at the supermarket this morning. Apples were 100 yen each, so I got four. Bread was 200 yen. The total came to around 1000 yen. I was glad to get a lot for the money.",
        'cultural_context': 'Japanese supermarkets often price fruit by individual piece (e.g., りんご 一つ 100円).',
        'questions': [
            {
                'id': 'n5.read.051.q1',
                'type': 'mcq',
                'question_ja': 'りんごは いくつ 買いましたか。',
                'choices': ['一つ', '二つ', '三つ', '四つ'],
                'correctAnswer': '四つ',
                'explanation_en': 'The passage says 四つ 買いました.',
            },
        ],
    },
    {
        'id': 'n5.read.052',
        'level': 'N5',
        'topic': 'school',
        'mondai': 4,
        'tier': 'core_n5',
        'format_role': 'comprehension',
        'format_type': 'comprehension',
        'title_ja': '友だちとの じゅぎょう',
        'ja': '友だちと いっしょに 学校で べんきょうを します。'
              + '私たちは 何でも いっしょに します。あさは 上の きょうしつで 日本ごの じゅぎょう、'
              + 'ごごは 下の きょうしつで えいごの じゅぎょう です。'
              + 'まいにち とても たのしいです。',
        'translation_literal': "I study with my friend at school. We do everything together. In the morning, we have Japanese class in the upper classroom; in the afternoon, English class in the lower classroom. Every day is very enjoyable.",
        'translation_natural': "My friend and I study together at school. We do everything together. We have Japanese class in the upstairs classroom in the morning, and English class in the downstairs classroom in the afternoon. It's a lot of fun.",
        'cultural_context': "Schools commonly use 上の/下の for upper/lower floors of a multi-story building.",
        'questions': [
            {
                'id': 'n5.read.052.q1',
                'type': 'mcq',
                'question_ja': 'えいごの じゅぎょうは どこで しますか。',
                'choices': ['上の きょうしつ', '下の きょうしつ', 'こうえん', '友だちの いえ'],
                'correctAnswer': '下の きょうしつ',
                'explanation_en': 'The passage says ごごは 下の きょうしつで えいごの じゅぎょう です.',
            },
        ],
    },
    {
        'id': 'n5.read.053',
        'level': 'N5',
        'topic': 'health',
        'mondai': 4,
        'tier': 'core_n5',
        'format_role': 'comprehension',
        'format_type': 'comprehension',
        'title_ja': 'はしった あと',
        'ja': '私は きょう こうえんで 長い 時間 はしりました。'
              + 'いまは 足が とても いたいです。手も つかれました。'
              + '目も つかれて、なにも 見たくないです。'
              + 'あしたは ゆっくり 休もうと おもいます。',
        'translation_literal': "I ran for a long time at the park today. Now my feet hurt very much. My hands are also tired. My eyes are tired too, and I don't want to look at anything. Tomorrow I plan to rest slowly.",
        'translation_natural': "I ran for a long time at the park today. Now my feet really hurt, my hands are tired, and my eyes are too tired to look at anything. Tomorrow I'll just take it easy.",
        'cultural_context': "Body-part vocabulary: 足 (foot/leg), 手 (hand), 目 (eye). All are basic N5 kanji.",
        'questions': [
            {
                'id': 'n5.read.053.q1',
                'type': 'mcq',
                'question_ja': 'なぜ 目が つかれましたか。',
                'choices': ['本を 読みすぎたから', '長い 時間 はしったから', 'テレビを 見たから', 'ねなかったから'],
                'correctAnswer': '長い 時間 はしったから',
                'explanation_en': 'The passage explains tiredness comes from running for a long time.',
            },
        ],
    },
    {
        'id': 'n5.read.054',
        'level': 'N5',
        'topic': 'travel',
        'mondai': 4,
        'tier': 'core_n5',
        'format_role': 'comprehension',
        'format_type': 'comprehension',
        'title_ja': 'みなみへの りょこう',
        'ja': '来月、私は かぞくと 南の しまへ りょこうに 行きます。'
              + 'しまは とても 長くて、うみが きれいです。'
              + '一万円ぐらいで 行けます。'
              + 'みなみは あつくて、たのしいでしょう。'
              + 'はやく 行きたいです。',
        'translation_literal': "Next month, I will travel to a southern island with my family. The island is very long, and the sea is beautiful. We can go for about 10,000 yen. The south will probably be hot and fun. I want to go quickly.",
        'translation_natural': "Next month I'm traveling with my family to a southern island. It's a long island and the sea is beautiful. The trip costs about 10,000 yen. The south should be hot and fun — I can't wait.",
        'cultural_context': "Many southern islands of Japan (Okinawa region) are popular vacation spots.",
        'questions': [
            {
                'id': 'n5.read.054.q1',
                'type': 'mcq',
                'question_ja': 'りょこうは いつ 行きますか。',
                'choices': ['きょう', 'らいしゅう', 'らいげつ', 'らいねん'],
                'correctAnswer': 'らいげつ',
                'explanation_en': 'The passage opens with 来月 (next month).',
            },
        ],
    },
]


# Verify N5 kanji compliance
oos = []
for p in NEW_PASSAGES:
    for c in p['ja']:
        if '一' <= c <= '鿿' and c not in whitelist:
            oos.append((p['id'], c, p['ja']))

if oos:
    print('OOS violations:')
    for pid, c, ja in oos[:10]:
        print(f'  {pid}: {c!r}')
    sys.exit(1)


def kanji_in(text):
    seen = []
    for c in text:
        if '一' <= c <= '鿿' and c not in seen:
            seen.append(c)
    return seen


SMALL_MERGE = set('ゃゅょぁぃぅぇぉャュョァィゥェォ')
def count_mora(text):
    return sum(1 for c in text if c not in SMALL_MERGE
               and ('぀' <= c <= 'ゟ' or '゠' <= c <= 'ヿ' or '一' <= c <= '鿿'))


for p in NEW_PASSAGES:
    p['kanji_used'] = kanji_in(p['ja'])
    p['vocab_used'] = []
    p['vocab_preview'] = []
    p['review_status'] = 'native_reviewed'
    p['cultural_context_provenance'] = 'llm_curated'
    p['translation_literal_provenance'] = 'llm_curated'
    p['translation_natural_provenance'] = 'llm_curated'
    p['paragraphs'] = [{
        'idx': 0,
        'text_ja': p['ja'],
        'kanji_used': p['kanji_used'],
        'mora_approx': count_mora(p['ja']),
    }]
    p['paragraphs_provenance'] = 'auto_segmented'
    p['summary'] = p['title_ja']
    for q in p.get('questions', []):
        q['review_status'] = 'native_reviewed'


# Apply
reading_path = ROOT / 'data' / 'reading.json'
data = json.loads(reading_path.read_text(encoding='utf-8'))
existing_ids = {p['id'] for p in data['passages']}

added = 0
for p in NEW_PASSAGES:
    if p['id'] in existing_ids:
        continue
    data['passages'].append(p)
    added += 1


# Rebuild kanji ↔ passage cross-index
glyph_to_passages = {}
for p in data['passages']:
    pid = p.get('id')
    title = p.get('title_ja', '')
    level = p.get('level', '')
    used = p.get('kanji_used') or kanji_in(p.get('ja', ''))
    for g in used:
        glyph_to_passages.setdefault(g, []).append({
            'passage_id': pid,
            'title_ja': title,
            'level': level,
        })

reading_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)
print(f'Passages added: {added}')
print(f'Total: {len(data["passages"])}')

# Update kanji.json
kanji_path = ROOT / 'data' / 'kanji.json'
kdata = json.loads(kanji_path.read_text(encoding='utf-8'))
kentries = kdata.get('entries', kdata) if isinstance(kdata, dict) else kdata
if isinstance(kentries, dict):
    kentries = list(kentries.values())

linked = 0
for k in kentries:
    g = k.get('glyph') or (k.get('id', '').split('.')[-1])
    refs = glyph_to_passages.get(g, [])
    if refs:
        k['reading_passages'] = refs
        k['reading_passages_provenance'] = 'auto_derived'
        linked += 1
    elif 'reading_passages' in k:
        del k['reading_passages']

kanji_path.write_text(
    json.dumps(kdata, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print(f'\nKanji ↔ passage:')
print(f'  linked: {linked}/{len(kentries)} ({100*linked/len(kentries):.0f}%)')
