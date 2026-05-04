"""Build N4 listening corpus seed (~30 items).

Generates ~30 listening items with the schema:
  id, format, title_ja, audio, script_ja, prompt_ja, choices,
  correctAnswer, explanation_en

Each item is template-based, drawing from in-scope vocab + grammar.
Audio files are NOT generated here; tools/build_audio.py renders MP3s
from script_ja in a subsequent pass.

Quality: SEED-grade. Native-speaker review (Pass-4) recommended.

Idempotent.
"""
import io, json, random, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
random.seed(42)

ROOT = Path(__file__).resolve().parent.parent

vocab = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))['entries']
whitelist = set(json.loads((ROOT / 'data' / 'n4_kanji_whitelist.json').read_text(encoding='utf-8')))

KANJI_RE = re.compile(r'[一-鿿]')

def in_scope(s):
    return all((not KANJI_RE.match(c)) or c in whitelist for c in s)

# Pool of in-scope nouns + verbs for templates
nouns = [v for v in vocab if v.get('pos') == 'noun' and in_scope(v.get('form', ''))][:80]
verbs = [v for v in vocab if v.get('pos') in ('verb-1', 'verb-2', 'verb-3') and in_scope(v.get('form', ''))][:60]

# Template generators
def gen_meeting_item(idx, place, time_str):
    """Two-person dialogue about where to meet."""
    other_place = random.choice(['えき', 'カフェ', 'デパート', '本や', '銀行', '病院'])
    return {
        'id': f'n4.listen.{idx:03d}',
        'format': 'task',
        'title_ja': 'どこで 会いますか',
        'audio': f'audio/listening/n4.listen.{idx:03d}.mp3',
        'script_ja': (
            f'男の人と 女の人が 話しています。あした、二人は どこで 会いますか。\n'
            f'男：あした、{time_str}に 会いませんか。\n'
            f'女：いいですね。どこで 会いますか。\n'
            f'男：{other_place}の 前で どうですか。\n'
            f'女：{place}の 前の ほうが いいです。\n'
            f'男：はい、わかりました。'
        ),
        'prompt_ja': 'あした、二人は どこで 会いますか。',
        'choices': [other_place + 'の 前', place + 'の 前',
                    'えいがかんの 前', 'こうえんの 前'],
        'correctAnswer': place + 'の 前',
        'explanation_en': f'The man initially suggested {other_place}, but the woman preferred {place} and the man agreed.',
        'voice': 'synthetic',
        'review_status': 'llm_only',
    }

def gen_shopping_item(idx, item_form, item_reading, price):
    """Shopping dialogue."""
    return {
        'id': f'n4.listen.{idx:03d}',
        'format': 'task',
        'title_ja': '何を 買いましたか',
        'audio': f'audio/listening/n4.listen.{idx:03d}.mp3',
        'script_ja': (
            f'おとこの ひとが みせで かいものを しています。'
            f'なにを かいましたか。\n'
            f'男：すみません、{item_form}は ありますか。\n'
            f'店：はい、こちらです。{price}円です。\n'
            f'男：じゃあ、ふたつ ください。'
        ),
        'prompt_ja': 'おとこの ひとは なにを かいましたか。',
        'choices': [
            f'{item_form}を ひとつ',
            f'{item_form}を ふたつ',
            f'{item_form}を みっつ',
            'なにも かいませんでした',
        ],
        'correctAnswer': f'{item_form}を ふたつ',
        'explanation_en': f'The man asked for two of the {item_form} ({item_reading}).',
        'voice': 'synthetic',
        'review_status': 'llm_only',
    }

def gen_short_item(idx, n):
    """Short single-line item."""
    if n.get('form') and n.get('reading'):
        return {
            'id': f'n4.listen.{idx:03d}',
            'format': 'task',
            'title_ja': 'なんと いいましたか',
            'audio': f'audio/listening/n4.listen.{idx:03d}.mp3',
            'script_ja': f'{n["form"]}は とても いいです。',
            'prompt_ja': 'おとこの ひとは なにに ついて はなしていますか。',
            'choices': [
                n['gloss'].split(';')[0].strip(),
                'てんき',
                'りょこう',
                'しごと',
            ],
            'correctAnswer': n['gloss'].split(';')[0].strip(),
            'explanation_en': f'The speaker is talking about {n["gloss"].split(";")[0].strip()}.',
            'voice': 'synthetic',
            'review_status': 'llm_only',
        }
    return None

# Generate ~30 listening items
items = []

places = ['カフェ', 'えき', 'デパート', '本や', '銀行', 'ホテル']
times = ['さん時', 'よ時', 'ご時', 'はち時', 'く時']
for i in range(10):
    items.append(gen_meeting_item(
        i + 1,
        places[i % len(places)],
        times[i % len(times)],
    ))

shopping_items = [
    ('りんご', 'りんご', 200),
    ('パン', 'ぱん', 150),
    ('ぎゅうにゅう', 'ぎゅうにゅう', 180),
    ('お茶', 'おちゃ', 120),
    ('みず', 'みず', 100),
    ('カバン', 'かばん', 3000),
    ('くつ', 'くつ', 5000),
    ('シャツ', 'しゃつ', 2500),
    ('ぼうし', 'ぼうし', 1500),
    ('じてんしゃ', 'じてんしゃ', 12000),
]
for i, (form, reading, price) in enumerate(shopping_items):
    items.append(gen_shopping_item(i + 11, form, reading, price))

# Fill out to ~30 with short items from in-scope nouns
random.shuffle(nouns)
i = 21
for n in nouns:
    if i > 30:
        break
    item = gen_short_item(i, n)
    if item:
        items.append(item)
        i += 1

print(f'Generated {len(items)} listening items')

# Write data/listening.json
payload = {
    '_meta': {
        'schema_version': 1,
        'entity_count': len(items),
        'id_range': 'n4.listen.001..n4.listen.NNN',
        'id_gap_policy': 'Numeric IDs reserved per item; never re-used.',
        'history': [
            {'date': '2026-05-04',
             'delta': f'+{len(items)} N4 listening seed items (template-generated; native review pending)'},
        ],
    },
    'items': items,
}
(ROOT / 'data' / 'listening.json').write_text(
    json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'data/listening.json written ({len(items)} items)')

# Update KnowledgeBank/chokai_questions_n4.md to mirror items as MD
md = ['# JLPT N4 Chokai Questions', '',
      f'{len(items)} listening items covering JLPT N4 chokai. Generated as a SEED corpus.',
      '',
      '## Subtypes covered',
      '',
      '| Mondai | Subtype | Count |',
      '|---|---|---|',
      f'| Mondai 1 | 課題理解 (task understanding) | 10 |',
      f'| Mondai 2 | 買い物 (shopping) | 10 |',
      f'| Mondai 3 | 短文 (short statements) | {len(items) - 20} |',
      '',
      '## Engine display note',
      '',
      "For mock-test mode, the app's test engine MUST hide the `**Answer:**` line and rationale until the student commits an answer.",
      '',
      '---', '']
for it in items:
    md.append(f"### {it['id']}")
    md.append('')
    md.append(f"**Title:** {it['title_ja']}")
    md.append(f"**Audio:** `{it['audio']}`")
    md.append('')
    md.append('**Script:**')
    md.append('')
    for line in it['script_ja'].split('\n'):
        md.append(f'> {line}')
    md.append('')
    md.append(f"**Prompt:** {it['prompt_ja']}")
    md.append('')
    md.append('**Choices:**')
    correct_index = it['choices'].index(it['correctAnswer']) + 1
    for i, ch in enumerate(it['choices'], 1):
        md.append(f'{i}. {ch}')
    md.append('')
    md.append(f"**Answer: {correct_index}** - {it['explanation_en']}")
    md.append('')

(ROOT / 'KnowledgeBank' / 'chokai_questions_n4.md').write_text(
    '\n'.join(md) + '\n', encoding='utf-8')
print(f'KnowledgeBank/chokai_questions_n4.md written')
