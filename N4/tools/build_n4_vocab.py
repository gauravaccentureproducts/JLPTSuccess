"""Build N4 vocab corpus from 100-entry sample + N5 prerequisite inheritance.

Reads:
  - <repo>/n4-vocab-inventory-sample.md (100 entries, alphabetical a-h)
  - <JLPT-root>/N5/data/vocab.json (1041 N5 entries inherited as prerequisite)
  - <JLPT-root>/N5/KnowledgeBank/vocabulary_n5.md (for Group-1-exception flags)

Writes:
  - data/vocab.json: runtime data (N5 prerequisite + N4 seed)
  - KnowledgeBank/vocabulary_n4.md: full catalogue per 18 thematic sections

Note: the N4 sample is a SEED corpus, not the full ~600-entry N4 vocab. Per spec,
the full corpus is fetched from Tanos N4 CSV at build time. This builder
demonstrates the format + tagging conventions and produces a runnable seed
that lets later build steps proceed.

Suru-noun handling: per N5 convention, a "Noun (suru-verb)" generates TWO
entries — a [n.] for the noun and a [v3] for the form+する. JA-31 expects
exact PoS match between KB and JSON.

PoS mapping (inventory format -> KB tag):
  Noun                    -> n.
  Noun (suru-verb)        -> n. (separately tagged as suru-capable)
  Noun (katakana)         -> n.
  Verb (godan, ...)       -> v1
  Verb (ichidan, ...)     -> v2
  Verb-3 / 来る           -> v3
  い-adjective            -> i-adj
  な-adj                  -> na-adj
  Adverb                  -> adv.
  Particle                -> part.
  Conjunction             -> conj.
  Pronoun                 -> pron.
  Counter                 -> count.
  Demonstrative           -> dem.
  Q-word                  -> Q-word
  Expression              -> exp.
  Interjection            -> interj.

Section assignment is heuristic per semantic + PoS rules; per AP-1, individual
words are tagged with their actual PoS, not the section default.

Idempotent.
"""
import io, json, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
N5 = ROOT.parent / 'N5'

# 0. Load N5 vocab as prerequisite tier
n5_vocab_data = json.loads((N5 / 'data' / 'vocab.json').read_text(encoding='utf-8'))
n5_entries = n5_vocab_data.get('entries', [])
print(f'[0] N5 prerequisite vocab loaded: {len(n5_entries)} entries')

# Load N5 KB markdown (for Group-1-exception lines we'll inline into N4)
n5_kb_text = (N5 / 'KnowledgeBank' / 'vocabulary_n5.md').read_text(encoding='utf-8')

# Romaji-to-hiragana converter for the pages-3-6 portion of the inventory.
# Order matters: longer matches first so 'kyou' is consumed before 'ky'.
ROMAJI_MAP = [
    # 3-char digraphs first
    ('kyou', 'きょう'), ('kyuu', 'きゅう'), ('kya', 'きゃ'), ('kyu', 'きゅ'), ('kyo', 'きょ'),
    ('shou', 'しょう'), ('shuu', 'しゅう'), ('sha', 'しゃ'), ('shi', 'し'), ('shu', 'しゅ'), ('she', 'しぇ'), ('sho', 'しょ'),
    ('chou', 'ちょう'), ('chuu', 'ちゅう'), ('cha', 'ちゃ'), ('chi', 'ち'), ('chu', 'ちゅ'), ('che', 'ちぇ'), ('cho', 'ちょ'),
    ('tsu', 'つ'),
    ('nyou', 'にょう'), ('nyuu', 'にゅう'), ('nya', 'にゃ'), ('nyu', 'にゅ'), ('nyo', 'にょ'),
    ('hyou', 'ひょう'), ('hyuu', 'ひゅう'), ('hya', 'ひゃ'), ('hyu', 'ひゅ'), ('hyo', 'ひょ'),
    ('myou', 'みょう'), ('myuu', 'みゅう'), ('mya', 'みゃ'), ('myu', 'みゅ'), ('myo', 'みょ'),
    ('ryou', 'りょう'), ('ryuu', 'りゅう'), ('rya', 'りゃ'), ('ryu', 'りゅ'), ('ryo', 'りょ'),
    ('gyou', 'ぎょう'), ('gyuu', 'ぎゅう'), ('gya', 'ぎゃ'), ('gyu', 'ぎゅ'), ('gyo', 'ぎょ'),
    ('jou', 'じょう'), ('juu', 'じゅう'), ('ja', 'じゃ'), ('ji', 'じ'), ('ju', 'じゅ'), ('jo', 'じょ'),
    ('byou', 'びょう'), ('byuu', 'びゅう'), ('bya', 'びゃ'), ('byu', 'びゅ'), ('byo', 'びょ'),
    ('pyou', 'ぴょう'), ('pyuu', 'ぴゅう'), ('pya', 'ぴゃ'), ('pyu', 'ぴゅ'), ('pyo', 'ぴょ'),
    # 2-char vowel combos and basic kana
    ('aa', 'ああ'), ('ii', 'いい'), ('uu', 'うう'), ('ee', 'ええ'), ('oo', 'おお'),
    ('ka', 'か'), ('ki', 'き'), ('ku', 'く'), ('ke', 'け'), ('ko', 'こ'),
    ('sa', 'さ'), ('su', 'す'), ('se', 'せ'), ('so', 'そ'),
    ('ta', 'た'), ('te', 'て'), ('to', 'と'),
    ('na', 'な'), ('ni', 'に'), ('nu', 'ぬ'), ('ne', 'ね'), ('no', 'の'),
    ('ha', 'は'), ('hi', 'ひ'), ('fu', 'ふ'), ('he', 'へ'), ('ho', 'ほ'),
    ('ma', 'ま'), ('mi', 'み'), ('mu', 'む'), ('me', 'め'), ('mo', 'も'),
    ('ya', 'や'), ('yu', 'ゆ'), ('yo', 'よ'),
    ('ra', 'ら'), ('ri', 'り'), ('ru', 'る'), ('re', 'れ'), ('ro', 'ろ'),
    ('wa', 'わ'), ('wo', 'を'),
    ('ga', 'が'), ('gi', 'ぎ'), ('gu', 'ぐ'), ('ge', 'げ'), ('go', 'ご'),
    ('za', 'ざ'), ('zu', 'ず'), ('ze', 'ぜ'), ('zo', 'ぞ'),
    ('da', 'だ'), ('de', 'で'), ('do', 'ど'),
    ('ba', 'ば'), ('bi', 'び'), ('bu', 'ぶ'), ('be', 'べ'), ('bo', 'ぼ'),
    ('pa', 'ぱ'), ('pi', 'ぴ'), ('pu', 'ぷ'), ('pe', 'ぺ'), ('po', 'ぽ'),
    ("n'", 'ん'),
    # Final-position consonants
    ('a', 'あ'), ('i', 'い'), ('u', 'う'), ('e', 'え'), ('o', 'お'),
    ('n', 'ん'),
]

def romaji_to_hiragana(s):
    """Convert romaji to hiragana. Handles double consonants (kk -> っk) and
    long-vowel ou/uu/aa/ee/oo. Skips strings already in kana."""
    if not s:
        return s
    # If string contains hiragana/katakana already, return as-is
    if any('぀' <= c <= 'ヿ' for c in s):
        return s
    s = s.lower()
    # Handle double consonants: kk, tt, pp, ss, etc.  → っ + single
    s = re.sub(r'([kstpghczbdmrjf])\1', r'っ\1', s)
    out = ''
    i = 0
    while i < len(s):
        matched = False
        for romaji, kana in ROMAJI_MAP:
            if s[i:i+len(romaji)] == romaji:
                out += kana
                i += len(romaji)
                matched = True
                break
        if not matched:
            out += s[i]
            i += 1
    return out

# 1. Parse N4 inventory (prefer full > sample)
full_inv_path = ROOT / 'n4-vocab-inventory-full.md'
sample_inv_path = ROOT / 'n4-vocab-inventory-sample.md'
inv_path = full_inv_path if full_inv_path.exists() else sample_inv_path
inv = inv_path.read_text(encoding='utf-8')
print(f'[1a] Reading inventory from: {inv_path.name}')
# Format: `FORM | READING (romaji) | ENGLISH | POS`
# CRITICAL: use [^|\n] not [^|] so the lazy quantifier doesn't span lines
# (a previous bug captured multi-line preamble blocks as spurious entries).
entry_pat = re.compile(r'^([^|#\s\n][^|\n]*?) \| ([^|\n]+?) \| ([^|\n]+?) \| ([^\n]+)$', re.MULTILINE)
inv_entries = []
for m in entry_pat.finditer(inv):
    form = m.group(1).strip()
    reading = m.group(2).strip()
    gloss = m.group(3).strip()
    pos_raw = m.group(4).strip()
    # Skip header rows + non-entry markdown (bold-prefixed metadata, table headers)
    if (form in ('KANJI/KANA', 'Section', 'FORM', 'Form') or 'Section' in pos_raw
            or form.startswith('**') or form.startswith('|') or form.startswith('---')):
        continue
    # Skip rows where reading is the romaji 'reading' label header
    if reading.lower() in ('reading', 'romaji'):
        continue
    # Convert romaji readings to hiragana (pages 3-6 of full inventory use romaji)
    reading = romaji_to_hiragana(reading)
    inv_entries.append({
        'form': form, 'reading': reading, 'gloss': gloss, 'pos_raw': pos_raw
    })
print(f'[1] Inventory parsed: {len(inv_entries)} entries')

# 2. Normalize PoS
def normalize_pos(raw):
    """Map inventory PoS string to KB tag + suru flag."""
    s = raw.lower()
    suru = 'suru' in s
    if 'godan' in s or 'verb (godan' in s:
        return 'v1', suru
    if 'ichidan' in s or 'verb (ichidan' in s:
        return 'v2', suru
    if 'い-adj' in raw or 'i-adjective' in s:
        return 'i-adj', False
    if 'な-adj' in raw or 'na-adj' in s:
        return 'na-adj', suru
    if s.startswith('adverb'):
        return 'adv.', suru
    if 'particle' in s:
        return 'part.', False
    if 'conjunction' in s:
        return 'conj.', False
    if 'pronoun' in s:
        return 'pron.', False
    if 'counter' in s:
        return 'count.', False
    if 'pre-noun adjectival' in s or 'demonstrative' in s:
        return 'dem.', False
    if 'expression' in s:
        return 'exp.', suru
    if 'interjection' in s:
        return 'interj.', False
    if 'noun' in s:
        return 'n.', suru
    return 'n.', suru  # default fallback

# 3. Assign thematic section
SECTIONS = {
    1: 'People and relationships',
    2: 'Home and daily life',
    3: 'School and study',
    4: 'Work and society',
    5: 'Travel and transportation',
    6: 'Shopping and money',
    7: 'Food and restaurants',
    8: 'Health and body',
    9: 'Weather and nature',
    10: 'Time and frequency',
    11: 'Feelings and opinions',
    12: 'Verbs (general)',
    13: 'I-adjectives',
    14: 'Na-adjectives',
    15: 'Adverbs',
    16: 'Conjunctions',
    17: 'Counters and quantities',
    18: 'Set phrases / expressions',
}

def assign_section(entry, pos_tag):
    """Heuristic section assignment based on PoS + semantic keywords."""
    g = entry['gloss'].lower()
    f = entry['form']
    # PoS-driven first
    if pos_tag == 'i-adj':
        return 13
    if pos_tag == 'na-adj':
        return 14
    if pos_tag == 'adv.':
        return 15
    if pos_tag == 'conj.':
        return 16
    if pos_tag == 'count.':
        return 17
    if pos_tag in ('exp.', 'interj.'):
        return 18
    if pos_tag in ('v1', 'v2', 'v3'):
        return 12
    if pos_tag in ('pron.', 'dem.'):
        return 1
    # Semantic keywords for nouns
    if any(k in g for k in ['baby', 'infant', 'father', 'mother', 'brother', 'sister',
                             'husband', 'wife', 'parent', 'child', 'family',
                             'i (used', 'male', 'female', 'man;', 'woman;', 'announcer',
                             'thief', 'manager', 'dentist']):
        return 1
    if any(k in g for k in ['art gallery', 'museum', 'building', 'lodging', 'futon',
                             'bedding', 'tool', 'rubbish', 'gas', 'gasoline']):
        return 2
    if any(k in g for k in ['school', 'university', 'study', 'review', 'literature',
                             'culture', 'grammar', 'geography', 'student']):
        return 3
    if any(k in g for k in ['program', 'work', 'society', 'company', 'office',
                             'department', 'section', 'trade', 'meeting', 'business',
                             'fax']):
        return 4
    if any(k in g for k in ['africa', 'asia', 'america', 'europe', 'travel', 'trip',
                             'parking', 'car', 'station', 'airport', 'escalator',
                             'bridge']):
        return 5
    if any(k in g for k in ['part-time', 'accessory', 'handbag', 'price', 'money',
                             'shop', 'shopping', 'pay', 'cost']):
        return 6
    if any(k in g for k in ['flavor', 'taste', 'feast', 'food', 'meal', 'drink',
                             'restaurant', 'alcohol', 'tea', 'rice', 'bread',
                             'grapes', 'leaf']):
        return 7
    if any(k in g for k in ['blood', 'body', 'health', 'pain', 'condition', 'medicine',
                             'doctor', 'injection', 'caution', 'embarrassed']):
        return 8
    if any(k in g for k in ['weather', 'rain', 'sun', 'wind', 'cloud', 'snow', 'sky',
                             'forest', 'woods', 'cherry blossom', 'shallow', 'deep']):
        return 9
    if any(k in g for k in ['time', 'minute', 'hour', 'day', 'week', 'month', 'year',
                             'morning', 'evening', 'night', 'as much as possible',
                             'rapidly', 'considerably']):
        return 10
    if any(k in g for k in ['safety', 'peace of mind', 'opinion', 'feel', 'thought',
                             'opposition', 'caution', 'reserve', 'apolog', 'surprise',
                             'happy', 'sad', 'angry', 'lonely', 'embarrassed',
                             'mind', 'heart', 'spirit', 'mood', 'feeling',
                             'sleepy', 'tired', 'glad', 'sorry']):
        return 11
    # Expanded section keywords (iter-2 rebalance):
    if any(k in g for k in ['conjunction', 'and', 'but', 'because', 'so',
                             'because of', 'in addition', 'moreover', 'however',
                             'still', 'then']):
        return 16
    if any(k in g for k in ['count', 'tens of', 'hundred', 'thousand',
                             'amount', 'number', 'quantity', 'time(s)',
                             'piece', 'sheet', 'volume']):
        return 17
    if any(k in g for k in ['greeting', 'farewell', 'thank', 'sorry',
                             'please', 'expression', 'phrase', 'set', 'idiom',
                             'saying', 'congratulation']):
        return 18
    # Sub-bucket nouns by topic to reduce section-4 dominance
    if any(k in g for k in ['english', 'japan', 'china', 'korea',
                             'language', 'culture', 'history', 'science',
                             'mathematics', 'arithmetic', 'biology']):
        return 3
    if any(k in g for k in ['airport', 'driver', 'commute', 'transport',
                             'taxi', 'subway', 'train', 'ship', 'bicycle']):
        return 5
    if any(k in g for k in ['ring', 'glove', 'handbag', 'cloth', 'fabric',
                             'silk', 'cotton', 'jewelry', 'sandal']):
        return 6
    if any(k in g for k in ['sweet', 'spicy', 'sour', 'bitter', 'cake',
                             'salad', 'sandwich', 'soup', 'sushi']):
        return 7
    if any(k in g for k in ['hospital', 'medicine', 'fever', 'illness',
                             'cold (sickness)', 'arm', 'leg', 'finger',
                             'tooth', 'ear', 'beard']):
        return 8
    if any(k in g for k in ['island', 'lake', 'mountain', 'ocean',
                             'river', 'forest', 'flower', 'tree',
                             'plant', 'star', 'moon']):
        return 9
    if any(k in g for k in ['century', 'era', 'period', 'season',
                             'recently', 'lately', 'soon', 'always',
                             'sometimes', 'never']):
        return 10
    # Fall back: noun → section 4 (work and society — generic)
    return 4

# 4. Build entries with full schema
def slugify_section(sec_idx):
    name = SECTIONS[sec_idx]
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    return f'{sec_idx}-{slug}'

def pos_to_field(pos_tag):
    """Map abbreviated PoS tag to data/vocab.json pos field name."""
    return {
        'n.': 'noun', 'v1': 'verb-1', 'v2': 'verb-2', 'v3': 'verb-3',
        'i-adj': 'i-adj', 'na-adj': 'na-adj', 'adv.': 'adverb',
        'part.': 'particle', 'conj.': 'conjunction', 'pron.': 'pronoun',
        'count.': 'counter', 'num.': 'numeral', 'dem.': 'demonstrative',
        'Q-word': 'question-word', 'exp.': 'expression', 'interj.': 'interjection',
    }.get(pos_tag, 'noun')

vocab_entries = []
section_buckets = {i: [] for i in range(1, 19)}

# 4a. N5 vocabulary is NOT inherited into N4 (per user directive 2026-05-04:
# "make sure N5 content is not repeated in N4"). Users who need N5 review
# should use the N5 sibling app.
#
# EXCEPTION: the 6 Group-1 ru-verb exceptions (入る/かえる/はしる/しる/きる/いる)
# are kept as a "review reference" sub-section in vocab.md AND a small set of
# entries in vocab.json. These verbs CONJUGATE differently than they look,
# and N4 learners still routinely get them wrong. Without these in JSON,
# JA-31 (PoS parity) would fail on the KB review-reference lines.
GROUP1_EXCEPTIONS = [
    {'form': '入る', 'reading': 'はいる', 'gloss': 'to enter (Group 1 exception - looks like Group 2)'},
    {'form': 'かえる', 'reading': 'かえる', 'gloss': 'to return home (Group 1 exception - looks like Group 2)'},
    {'form': 'はしる', 'reading': 'はしる', 'gloss': 'to run (Group 1 exception - looks like Group 2)'},
    {'form': 'しる', 'reading': 'しる', 'gloss': 'to know (Group 1 exception - looks like Group 2)'},
    {'form': 'きる', 'reading': 'きる', 'gloss': 'to cut (Group 1 exception - looks like Group 2; homophone of きる "to wear" which is Group 2)'},
    {'form': 'いる', 'reading': 'いる', 'gloss': 'to need (Group 1 exception - looks like Group 2; homophone of existence-いる which is Group 2)'},
]
for ex in GROUP1_EXCEPTIONS:
    vocab_entries.append({
        'id': f'n4.vocab.0-group1-exceptions.{ex["form"]}',
        'form': ex['form'],
        'reading': ex['reading'],
        'gloss': ex['gloss'],
        'section': '0. Group-1 ru-verb exceptions (review reference)',
        'pos': 'verb-1',
        'tier': 'n5_review_reference',
        'examples': [],
        'kb_pos_tag': 'v1',
    })

# 4b. Build N4-new entries from inventory
for inv_e in inv_entries:
    pos_tag, suru_flag = normalize_pos(inv_e['pos_raw'])
    sec_idx = assign_section(inv_e, pos_tag)
    sec_label = f"{sec_idx}. {SECTIONS[sec_idx]}"
    slug_id = slugify_section(sec_idx)
    form_clean = inv_e['form']

    # Primary entry (tagged as the actual PoS)
    pos_field = pos_to_field(pos_tag)
    entry = {
        'id': f'n4.vocab.{slug_id}.{form_clean}',
        'form': form_clean,
        'reading': inv_e['reading'],
        'gloss': inv_e['gloss'],
        'section': sec_label,
        'pos': pos_field,
        'tier': 'core_n4',
        'examples': [],
        'kb_pos_tag': pos_tag,
    }
    vocab_entries.append(entry)
    section_buckets[sec_idx].append(entry)

    # If suru-capable noun, ALSO generate a [v3] entry per N5 convention.
    # This makes JA-31 happy (both PoS appear in JSON; KB tags one per line).
    if suru_flag and pos_tag == 'n.':
        suru_form = form_clean + 'する'
        suru_reading = inv_e['reading'].replace(' ', '') + 'する'
        suru_gloss = f"to {inv_e['gloss'].split(';')[0]}".replace('to to ', 'to ')
        # Suru forms go to section 12 (Verbs)
        sec_idx_v3 = 12
        sec_label_v3 = f"{sec_idx_v3}. {SECTIONS[sec_idx_v3]}"
        slug_id_v3 = slugify_section(sec_idx_v3)
        suru_entry = {
            'id': f'n4.vocab.{slug_id_v3}.{suru_form}',
            'form': suru_form,
            'reading': suru_reading,
            'gloss': suru_gloss,
            'section': sec_label_v3,
            'pos': 'verb-3',
            'tier': 'core_n4',
            'examples': [],
            'kb_pos_tag': 'v3',
        }
        vocab_entries.append(suru_entry)
        section_buckets[sec_idx_v3].append(suru_entry)

print(f'[2-3] Entries built: {len(vocab_entries)} across {sum(1 for b in section_buckets.values() if b)} sections')

# 5. Write data/vocab.json
vocab_payload = {
    '_meta': {
        'schema_version': 1,
        'entity_count': len(vocab_entries),
        'id_range': 'n4.vocab.<section-slug>.<form>',
        'id_gap_policy': 'IDs encode section + form; never re-used.',
        'history': [
            {'date': '2026-05-04', 'delta': f'+{len(vocab_entries)} N4 vocab seed entries (from a-h sample inventory)'}
        ],
        'note': 'SEED corpus from 100-entry sample. Full ~600-entry N4 vocab to be authored in subsequent passes.',
    },
    'entries': vocab_entries,
}
(ROOT / 'data' / 'vocab.json').write_text(
    json.dumps(vocab_payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'[5] data/vocab.json written ({len(vocab_entries)} entries)')

# 6. Build KnowledgeBank/vocabulary_n4.md
md = ['# JLPT N4 Vocabulary (Goi)', '',
      'Source-of-truth catalogue. Build pipeline parses into `data/vocab.json`. Schema per spec.',
      '',
      'Entry format:',
      '```',
      '- <form> (<reading>) - [<pos>] <gloss> [tier:<tier>] [examples:<count>]',
      '```',
      '',
      'PoS tags: `[n.]`, `[v1]`, `[v2]`, `[v3]`, `[i-adj]`, `[na-adj]`, `[adv.]`, `[part.]`, `[conj.]`, `[pron.]`, `[count.]`, `[num.]`, `[dem.]`, `[Q-word]`, `[exp.]`, `[interj.]`.',
      '',
      "**Tag the WORD's actual PoS, not the section default** (anti-pattern AP-1).",
      '',
      'Corpus = N4-new only (no N5 repetition). N5 vocabulary is a prerequisite;',
      'review it via the N5 sibling app at https://gauravaccentureproducts.github.io/jlpt-n5-tutor/.',
      '',
      '## Group-1 ru-verb exceptions (review reference)',
      '',
      'These N5 verbs LOOK like Group 2 but conjugate as Group 1. They are listed',
      'here as a quick reference at N4 because students still routinely conjugate',
      'them incorrectly. The full lemma + reading set lives in the N5 catalogue.',
      '',
      '- 入る (はいる) - [v1] to enter (Group 1 exception - looks like Group 2)',
      '- かえる (帰る) - [v1] to return home (Group 1 exception - looks like Group 2)',
      '- はしる (走る) - [v1] to run (Group 1 exception - looks like Group 2)',
      '- しる (知る) - [v1] to know (Group 1 exception - looks like Group 2)',
      '- きる (切る) - [v1] to cut (Group 1 exception - looks like Group 2; homophone of きる "to wear" which is Group 2)',
      '- いる (要る) - [v1] to need (Group 1 exception - looks like Group 2; homophone of existence-いる which is Group 2)',
      '',
      '---',
      '',
      '## N4 vocabulary',
      '',
      f"{len([e for e in vocab_entries if e.get('tier') == 'core_n4'])} N4 entries distributed across 18 thematic sections.",
      '']

for sec_idx in sorted(SECTIONS.keys()):
    md.append(f'## {sec_idx}. {SECTIONS[sec_idx]}')
    md.append('')
    bucket = section_buckets[sec_idx]
    if not bucket:
        md.append('(seed corpus has no entries for this section yet - extend from Tanos N4 in next pass)')
        md.append('')
        continue
    for e in bucket:
        tag = e['kb_pos_tag']
        examples_count = len(e['examples'])
        md.append(f'- {e["form"]} ({e["reading"]}) - [{tag}] {e["gloss"]} [tier:core_n4] [examples:{examples_count}]')
    md.append('')

(ROOT / 'KnowledgeBank' / 'vocabulary_n4.md').write_text(
    '\n'.join(md) + '\n', encoding='utf-8')
print(f'[6] KnowledgeBank/vocabulary_n4.md written ({len(vocab_entries)} entries)')

# 7. Section coverage report
print('\nSection distribution:')
for sec_idx in sorted(SECTIONS.keys()):
    print(f'  {sec_idx:2d}. {SECTIONS[sec_idx]:40s} {len(section_buckets[sec_idx]):3d} entries')

print('\nDone. Run python tools/check_content_integrity.py to verify.')
