"""IMP-128 final pass: generate template collocations for the 563
vocab entries that still lack them. Section-aware + POS-aware.

Provenance: 'auto_generated_template' — distinguishes from
'llm_curated' (hand-authored) and 'auto_derived' (from corpus
mining). Future native review can refine.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


def make_collocations(entry):
    form = entry.get('form', '')
    reading = entry.get('reading', '')
    pos = entry.get('pos', '')
    section = entry.get('section', '')
    surface = form  # use form for collocations

    if not surface:
        return []

    collocs = []

    # Section-specific templates
    if 'Time' in section:
        # Time words pair with particles indicating time
        collocs.extend([
            f'{surface}に',
            f'{surface}から',
            f'{surface}まで',
            f'{surface}は',
            f'{surface}も',
            f'{surface}ごろ',
        ])
    elif 'Pronoun' in section or 'Self' in section:
        collocs.extend([
            f'{surface}は',
            f'{surface}が',
            f'{surface}も',
            f'{surface}の',
            f'{surface}に',
            f'{surface}と',
        ])
    elif 'Family' in section or 'Roles' in section:
        collocs.extend([
            f'{surface}と 話す',
            f'{surface}に 会う',
            f'{surface}の しごと',
            f'やさしい {surface}',
            f'{surface}の しゃしん',
            f'{surface}に あげる',
        ])
    elif 'Body' in section:
        collocs.extend([
            f'{surface}が いたい',
            f'{surface}を あらう',
            f'大きい {surface}',
            f'{surface}が きれい',
            f'{surface}の くすり',
            f'{surface}を 見る',
        ])
    elif 'Number' in section or 'Counter' in section:
        collocs.extend([
            f'{surface}つ',
            f'{surface}かい',
            f'{surface}ばん',
            f'{surface}じ',
            f'{surface}にん',
            f'{surface}ふん',
        ])
    elif 'Question' in section:
        collocs.extend([
            f'{surface}ですか',
            f'{surface}が いいですか',
            f'{surface}でしたか',
            f'{surface}に 行きますか',
            f'{surface}を 食べますか',
            f'{surface}と 話しますか',
        ])
    elif 'Location' in section or 'Place' in section:
        collocs.extend([
            f'{surface}に 行く',
            f'{surface}で あう',
            f'{surface}から 出る',
            f'{surface}まで 行く',
            f'近くの {surface}',
            f'{surface}の まえ',
        ])
    elif 'Direction' in section:
        collocs.extend([
            f'{surface}に 行く',
            f'{surface}を 見る',
            f'{surface}から 来る',
            f'{surface}の ほう',
            f'{surface}に まがる',
            f'{surface}の 国',
        ])
    elif 'Nature' in section or 'Weather' in section:
        collocs.extend([
            f'{surface}が きれい',
            f'{surface}が いい',
            f'{surface}を 見る',
            f'{surface}の 中',
            f'{surface}に なる',
            f'{surface}の おと',
        ])
    elif 'Animal' in section:
        collocs.extend([
            f'{surface}を かう',
            f'{surface}が すき',
            f'小さい {surface}',
            f'{surface}と あそぶ',
            f'{surface}の こえ',
            f'{surface}の しゃしん',
        ])
    elif 'Food' in section or 'Drink' in section:
        collocs.extend([
            f'{surface}を 食べる',
            f'{surface}を 飲む',
            f'{surface}を かう',
            f'おいしい {surface}',
            f'{surface}の あじ',
            f'{surface}が すき',
        ])
    elif 'Tableware' in section or 'Cooking' in section:
        collocs.extend([
            f'{surface}を つかう',
            f'{surface}を かう',
            f'新しい {surface}',
            f'{surface}が ある',
            f'{surface}の 上',
            f'{surface}を あらう',
        ])
    elif 'Color' in section:
        collocs.extend([
            f'{surface}い ふく',
            f'{surface}い いえ',
            f'{surface}い はな',
            f'{surface}が すき',
            f'{surface}の くるま',
            f'{surface}の シャツ',
        ])
    elif 'Clothing' in section:
        collocs.extend([
            f'{surface}を きる',
            f'{surface}を かう',
            f'新しい {surface}',
            f'{surface}が すき',
            f'{surface}の デザイン',
            f'白い {surface}',
        ])
    elif 'Money' in section or 'Shopping' in section:
        collocs.extend([
            f'{surface}を はらう',
            f'{surface}を かう',
            f'{surface}が ある',
            f'{surface}の みせ',
            f'たくさんの {surface}',
            f'{surface}を つかう',
        ])
    elif 'Transport' in section:
        collocs.extend([
            f'{surface}に のる',
            f'{surface}で 行く',
            f'{surface}から おりる',
            f'{surface}の じかん',
            f'はやい {surface}',
            f'{surface}を まつ',
        ])
    elif 'School' in section or 'Study' in section:
        collocs.extend([
            f'{surface}で べんきょう',
            f'{surface}の せんせい',
            f'{surface}に 行く',
            f'{surface}が すき',
            f'{surface}を おしえる',
            f'{surface}の クラス',
        ])
    elif 'Language' in section or 'Countries' in section:
        collocs.extend([
            f'{surface}を 話す',
            f'{surface}が じょうず',
            f'{surface}の せんせい',
            f'{surface}に 行く',
            f'{surface}人',
            f'{surface}の りょうり',
        ])
    elif 'House' in section or 'Furniture' in section:
        collocs.extend([
            f'{surface}を かう',
            f'{surface}が ある',
            f'大きい {surface}',
            f'{surface}を つかう',
            f'{surface}の そうじ',
            f'{surface}の 中',
        ])
    elif pos and pos.startswith('verb'):
        collocs.extend([
            f'{surface}ます',
            f'{surface}ません',
            f'{surface}ました',
            f'{surface}ない',
            f'{surface}たい',
            f'{surface}て',
        ])
    elif pos == 'i-adj':
        # Use stem (drop trailing い)
        stem = surface[:-1] if surface.endswith('い') else surface
        collocs.extend([
            f'{surface}です',
            f'{stem}くない',
            f'{stem}かった',
            f'{stem}くて',
            f'{stem}く なる',
            f'とても {surface}',
        ])
    elif pos == 'na-adj':
        collocs.extend([
            f'{surface}です',
            f'{surface}じゃない',
            f'{surface}だった',
            f'{surface}な ひと',
            f'{surface}に なる',
            f'とても {surface}',
        ])
    elif pos == 'adverb':
        collocs.extend([
            f'{surface} 食べる',
            f'{surface} 行く',
            f'{surface} 見る',
            f'{surface} わかる',
            f'{surface} 思う',
            f'{surface} 来る',
        ])
    elif 'Greeting' in section or 'Set Phrase' in section:
        # Set phrases: just stand-alone usage variants
        collocs.extend([
            f'{surface}',
            f'はい、{surface}',
            f'どうも、{surface}',
            f'えっ、{surface}',
            f'では、{surface}',
            f'あ、{surface}',
        ])
    else:
        # Default: noun-like fallback
        collocs.extend([
            f'{surface}が ある',
            f'{surface}を 見る',
            f'{surface}を つかう',
            f'大きい {surface}',
            f'{surface}の 中',
            f'{surface}が すき',
        ])

    # Ensure 5+ unique collocations
    seen = set()
    out = []
    for c in collocs:
        if c not in seen:
            seen.add(c)
            out.append(c)
        if len(out) >= 6:
            break
    return out


vocab_path = ROOT / 'data' / 'vocab.json'
data = json.loads(vocab_path.read_text(encoding='utf-8'))
entries = data['entries']

added = 0
for e in entries:
    if e.get('collocations'):
        continue
    new_collocs = make_collocations(e)
    if not new_collocs:
        continue
    e['collocations'] = new_collocs
    e['collocations_provenance'] = 'auto_generated_template'
    added += 1

vocab_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

with_collocs = sum(1 for e in entries if e.get('collocations'))
print(f'Added: {added}')
print(f'Total with collocations: {with_collocs}/1000 ({100*with_collocs/1000:.0f}%)')
