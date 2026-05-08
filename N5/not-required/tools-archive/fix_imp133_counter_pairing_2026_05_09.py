"""IMP-133: complete counter pairing on N5 nouns. Auto-derive from a
canonical mapping of (gloss/lemma keyword → counter)."""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Counter assignment by category-keyword in gloss or lemma
# Format: (counter_kanji, counter_reading, gloss_keywords, lemma_blocklist)
# Counter rules cover the most common N5 categories.
COUNTER_RULES = [
    # 冊 (さつ) - bound things (books, magazines, notebooks)
    ('冊', 'さつ', ['book', 'magazine', 'notebook', 'dictionary', 'textbook'], []),
    # 台 (だい) - mechanical things, vehicles, large appliances
    ('台', 'だい', ['car', 'bicycle', 'computer', 'tv', 'television', 'machine',
                   'refrigerator', 'washing machine', 'desk', 'piano'], []),
    # 枚 (まい) - flat thin things (paper, plates, shirts, tickets, photos, stamps)
    ('枚', 'まい', ['paper', 'sheet', 'plate', 'shirt', 'ticket', 'photo',
                   'photograph', 'stamp', 'card', 'handkerchief', 't-shirt',
                   'cd', 'dvd'], []),
    # 本 (ほん/ぽん/ぼん) - long thin things (pens, bottles, trees, umbrellas, bananas)
    ('本', 'ほん', ['pen', 'pencil', 'bottle', 'tree', 'umbrella', 'banana',
                   'cigarette', 'leg', 'finger', 'rope', 'flower stem'], []),
    # 個 (こ) - small generic objects (apples, oranges, pieces, balls, soaps)
    ('個', 'こ', ['apple', 'orange', 'egg', 'ball', 'soap', 'cake',
                 'piece', 'item', 'eraser'], []),
    # 匹 (ひき/ぴき/びき) - small animals (dogs, cats, fish, insects)
    ('匹', 'ひき', ['dog', 'cat', 'fish', 'insect', 'mouse', 'rabbit',
                   'small animal'], ['fish-counter']),
    # 頭 (とう) - large animals (cows, horses, elephants)
    ('頭', 'とう', ['cow', 'horse', 'elephant', 'bull', 'lion', 'tiger',
                   'large animal'], []),
    # 羽 (わ/ば/ぱ) - birds and rabbits
    ('羽', 'わ', ['bird', 'chicken', 'duck', 'pigeon', 'sparrow'], []),
    # 人 (にん/り) - people
    ('人', 'にん', ['person', 'people', 'student', 'teacher', 'child',
                   'children', 'adult', 'foreigner', 'friend', 'doctor',
                   'office worker'], []),
    # 階 (かい/がい) - floors of a building
    ('階', 'かい', ['floor', 'story', 'storey'], []),
    # 杯 (はい/ぱい) - cups, glasses (drinks served in)
    ('杯', 'はい', ['cup of', 'glass of', 'bowl of'], []),
    # 軒 (けん) - houses, shops
    ('軒', 'けん', ['house', 'shop', 'store', 'restaurant'], []),
    # 着 (ちゃく) - clothing
    ('着', 'ちゃく', ['kimono', 'dress', 'suit', 'jacket'], []),
    # 足 (そく) - pairs of footwear (shoes, socks)
    ('足', 'そく', ['shoe', 'sock', 'sandal', 'boot'], ['leg', 'foot']),
    # 足/足 (already in above; the leg-meaning is on the foot/leg pair)
]


vpath = ROOT / 'data' / 'vocab.json'
vdata = json.loads(vpath.read_text(encoding='utf-8'))
items = vdata['entries']

def assign_counter(entry):
    """Return (counter_kanji, counter_reading) or None."""
    gloss = (entry.get('gloss') or '').lower()
    lemma = entry.get('lemma') or entry.get('form') or ''
    pos = (entry.get('pos') or '').lower()
    # Only nouns get counters
    if pos != 'noun' and 'noun' not in pos:
        return None
    # Already has counter
    if entry.get('counter'):
        return None

    for counter, reading, keywords, blocklist in COUNTER_RULES:
        if any(b in gloss for b in blocklist):
            continue
        for kw in keywords:
            if kw in gloss:
                return (counter, reading)
    return None


added = 0
already_have = 0
no_match = 0
by_counter = {}
for e in items:
    pos = (e.get('pos') or '').lower()
    if pos != 'noun' and 'noun' not in pos:
        continue
    if e.get('counter') or e.get('default_counter'):
        already_have += 1
        continue
    res = assign_counter(e)
    if res:
        kanji, reading = res
        e['counter'] = {'kanji': kanji, 'reading': reading}
        added += 1
        by_counter[kanji] = by_counter.get(kanji, 0) + 1
    else:
        no_match += 1

vpath.write_text(json.dumps(vdata, ensure_ascii=False, indent=2) + '\n',
                 encoding='utf-8')

total_with = already_have + added
total_nouns = sum(1 for e in items if (e.get('pos') or '').lower() == 'noun' or 'noun' in (e.get('pos') or '').lower())
print(f'Counter pairing:')
print(f'  Already had counter:    {already_have}')
print(f'  Newly assigned:         {added}')
print(f'  No match (no counter):  {no_match}')
print(f'  Total nouns:            {total_nouns}')
print(f'  Coverage:               {total_with}/{total_nouns} ({100*total_with/max(1,total_nouns):.0f}%)')
print(f'\nBy counter (newly added):')
for k, v in sorted(by_counter.items(), key=lambda x: -x[1]):
    print(f'  {k}: {v}')
