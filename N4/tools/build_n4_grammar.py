"""Build N4 grammar catalogue from inventory + N5 prerequisite inheritance.

Reads:
  - <repo>/n4-grammar-inventory.md (~130 N4 patterns)
  - <JLPT-root>/N5/data/grammar.json (178 N5 patterns inherited as prerequisite)

Writes:
  - data/grammar.json: runtime data (N5 prerequisite + N4 patterns)
  - KnowledgeBank/grammar_n4.md: 18-category catalogue with all entries

Pattern -> category mapping is keyword-driven heuristic against the 18 N4
categories defined in spec §12.2. Entries that fall through to fallback land
in category 1 (Verb forms overview) for manual sorting later.

Idempotent.
"""
import io, json, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
N5 = ROOT.parent / 'N5'

# 0. Load N5 grammar
n5_grammar = json.loads((N5 / 'data' / 'grammar.json').read_text(encoding='utf-8'))
n5_patterns = n5_grammar.get('patterns', [])
print(f'[0] N5 prerequisite grammar loaded: {len(n5_patterns)} patterns')

# Load N4 kanji whitelist for kana-folding out-of-scope kanji in pattern strings
n4_kanji_whitelist = set(json.loads(
    (ROOT / 'data' / 'n4_kanji_whitelist.json').read_text(encoding='utf-8')))

# Meta-topics from the inventory's review notes - skip these (they're conceptual
# headers, not patterns; Pass-2 reviewer flags them for removal):
META_TOPICS = {
    '意向形（いこうけい）', '受身形（うけみけい）',
    '他動詞 & 自動詞', '他動詞', '自動詞',
}

KANJI_RE = re.compile(r'[一-鿿]')

def fold_to_scope(pattern):
    """If pattern has out-of-scope kanji and contains a parenthesized kana
    reading, return the parenthesized form. Otherwise return as-is."""
    # Find any kanji in pattern that's not in whitelist
    out_of_scope = [c for c in pattern if KANJI_RE.match(c) and c not in n4_kanji_whitelist]
    if not out_of_scope:
        return pattern
    # Try to extract parenthesized reading: `場合は（ばあいは）` -> `ばあいは`
    paren_match = re.search(r'（([ぁ-んー〜]+)）', pattern)
    if paren_match:
        # Use the kana reading as the canonical form
        return paren_match.group(1)
    # Try /-separated: `頃（ころ / ごろ）` -> first option
    paren_match = re.search(r'（([ぁ-んー〜]+)\s*/', pattern)
    if paren_match:
        return paren_match.group(1)
    # No safe transform available -- caller should drop this entry
    return None

# 1. Parse N4 inventory
inv = (ROOT / 'n4-grammar-inventory.md').read_text(encoding='utf-8')
# Format: `PATTERN | MEANING-BRIEF`
pat_re = re.compile(r'^([^|#\s\n][^|\n]*?) \| ([^\n]+)$', re.MULTILINE)
n4_inv = []
seen_patterns = set()
dropped_meta = 0
folded_to_kana = 0
for m in pat_re.finditer(inv):
    pattern = m.group(1).strip()
    meaning = m.group(2).strip()
    # Skip metadata rows
    if (pattern.startswith('**') or pattern.startswith('|') or
            pattern in seen_patterns or '|' in pattern):
        continue
    if pattern in ('PATTERN', 'Format', 'Source', 'Cross-reference'):
        continue
    # Skip lines whose pattern starts with markdown emphasis or 'Format:' --
    # the inventory's `Format: \`PATTERN | MEANING-BRIEF\`` line would
    # otherwise match the regex and become spurious entry n4-001.
    if pattern.startswith('Format:') or pattern.startswith('`'):
        continue
    if pattern in META_TOPICS:
        dropped_meta += 1
        continue
    # Apply kana-fold for out-of-scope kanji
    folded = fold_to_scope(pattern)
    if folded is None:
        dropped_meta += 1
        continue
    if folded != pattern:
        folded_to_kana += 1
    seen_patterns.add(pattern)
    n4_inv.append({'pattern': folded, 'meaning': meaning, 'original': pattern})
print(f'[1] N4 inventory parsed: {len(n4_inv)} patterns ({dropped_meta} meta-topics dropped, {folded_to_kana} kana-folded for out-of-scope kanji)')

# 2. Define 18 categories per spec §12.2 + categorization rules
CATEGORIES = {
    1: 'Verb forms (overview)',
    2: 'Te-form patterns',
    3: 'Nai-form patterns',
    4: 'Ta-form patterns',
    5: 'Dictionary-form patterns',
    6: 'Potential form',
    7: 'Volitional form',
    8: 'Conditionals (たら / ば / なら / と)',
    9: 'Giving and receiving (あげる / くれる / もらう)',
    10: 'Requests and permission',
    11: 'Obligation and prohibition',
    12: 'Experience and plans',
    13: 'Comparison and degree',
    14: 'Conjunctions and sentence connectors',
    15: 'Quotation and thought',
    16: 'Explanation and reason',
    17: 'Time expressions',
    18: 'Frequency and adverbs',
}

def categorize(pat, meaning):
    """Heuristic mapping of pattern → category index."""
    p = pat
    m = meaning.lower()
    # Conditionals
    if any(k in p for k in ['たら', 'ば', 'なら', 'と言われ']) and ('if' in m or 'when' in m or 'conditional' in m or 'whenever' in m):
        return 8
    if p in ('ば', 'なら', 'と') or 'conditional' in m:
        return 8
    # Giving/receiving
    if any(k in p for k in ['あげる', 'くれる', 'もらう', 'てあげる', 'てくれる', 'てもらう', 'ていただ']):
        return 9
    if 'give' in m or 'receive' in m or 'do for' in m:
        return 9
    # Requests / permission
    if any(k in p for k in ['ください', 'てもいい', 'ても良い', 'てはいけない', 'てはダメ', 'なさい', 'させて']):
        return 10
    if 'permission' in m or 'request' in m or 'please do' in m or 'may i' in m:
        return 10
    # Obligation / prohibition
    if any(k in p for k in ['なければ', 'なきゃ', 'べき', 'てはいけない', 'なくては', 'ないといけない']):
        return 11
    if 'must' in m or 'have to' in m or 'should' in m or 'prohibit' in m or 'obligation' in m:
        return 11
    # Experience / plans
    if any(k in p for k in ['たことがある', 'ことがある', 'つもり', '予定', 'ようと思う']):
        return 12
    if 'experience' in m or 'plan to' in m or 'intend to' in m:
        return 12
    # Comparison
    if any(k in p for k in ['より', 'ほうが', 'ほど', 'のほうが']):
        return 13
    if 'compar' in m or 'than' in m or 'more than' in m:
        return 13
    # Conjunctions / connectors
    if any(k in p for k in ['けど', 'けれども', 'のに', 'ので', 'から', 'し', 'ても', 'たり', 'ながら']):
        return 14
    if 'conjunction' in m or 'connect' in m or 'although' in m or 'even though' in m or 'such as' in m:
        return 14
    # Quotation / thought
    if any(k in p for k in ['と思う', 'と言う', 'って', 'という', 'ということ', 'と聞いた']):
        return 15
    if 'quot' in m or 'think' in m or 'said' in m or 'called' in m:
        return 15
    # Explanation / reason
    if any(k in p for k in ['んです', 'のです', 'ため', 'ので', 'おかげ', 'せい']):
        return 16
    if 'because' in m or 'reason' in m or 'explain' in m or 'thanks to' in m:
        return 16
    # Time expressions
    if any(k in p for k in ['とき', '時', 'うちに', '前に', '後で', 'てから', 'ところ', 'ばかり']):
        return 17
    if 'while' in m or 'during' in m or 'before' in m or 'after' in m or 'time' in m or 'when' in m:
        return 17
    # Frequency / adverbs
    if any(k in p for k in ['いつも', 'よく', 'たまに', 'ときどき', 'ぜひ', 'きっと', 'ぜんぜん', '全然']):
        return 18
    if 'often' in m or 'always' in m or 'sometimes' in m or 'never' in m or 'frequenc' in m:
        return 18
    # Volitional form
    if any(k in p for k in ['よう', 'う/おう', 'ようと']) and ('volitional' in m or 'let' in m or 'plan' in m or 'thinking' in m):
        return 7
    # Potential form
    if any(k in p for k in ['られる', 'える', 'ことができる']) and ('can' in m or 'able' in m or 'potential' in m):
        return 6
    # Te-form patterns
    if any(k in p for k in ['ている', 'てある', 'ておく', 'てしまう', 'てみる', 'ていく', 'てくる', 'て＋']):
        return 2
    # Nai-form patterns
    if any(k in p for k in ['ないで', 'ない方', 'なくて', 'なくても']):
        return 3
    # Ta-form
    if any(k in p for k in ['たばかり', 'たり', 'たほうが']):
        return 4
    # Dictionary-form
    if any(k in p for k in ['ことができる', 'ことにする', 'ことになる', 'こと', 'の']) and 'verb' in m:
        return 5
    # Default: fall back to category 1 (verb forms overview)
    return 1

# 3. Build N4 patterns
n4_built = []
for i, e in enumerate(n4_inv):
    cat = categorize(e['pattern'], e['meaning'])
    pid = f'n4-{i+1:03d}'
    entry = {
        'id': pid,
        'tier': 'core_n4',
        'pattern': e['pattern'],
        'category': CATEGORIES[cat],
        'categoryOrder': cat,
        'patternOrder': i + 1,
        'meaning_en': e['meaning'],
        'meaning_ja': '',  # to be authored
        'form_rules': {
            'attaches_to': [],
            'conjugations': [],
        },
        'explanation_en': '',  # to be authored
        'examples': [],
        'common_mistakes': [],
        'contrasts': [],
        'notes': '',
    }
    n4_built.append(entry)
print(f'[2] N4 patterns built: {len(n4_built)}')

# 4. N5 grammar is NOT inherited (per user directive 2026-05-04: "make sure
# N5 content is not repeated in N4"). N5 patterns are prerequisites; review
# them via the N5 sibling app.
n5_inherited = []
all_patterns = n4_built
print(f'[3] N5 patterns NOT inherited (sibling-app convention)')
print(f'[4] Total: {len(all_patterns)} N4 patterns')

# 5. Write data/grammar.json
payload = {
    '_meta': {
        'schema_version': 1,
        'entity_count': len(all_patterns),
        'id_range': 'n4-prereq-001..n4-prereq-NNN (N5 inherited) + n4-001..n4-NNN (N4 new)',
        'id_gap_policy': 'Reserve numeric ranges per category. Retired IDs are NEVER re-used.',
        'history': [
            {'date': '2026-05-04',
             'delta': f'+{len(n5_inherited)} N5 prerequisite + {len(n4_built)} N4 new (seed; examples + form_rules to be authored)'}
        ],
    },
    'patterns': all_patterns,
}
(ROOT / 'data' / 'grammar.json').write_text(
    json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'[5] data/grammar.json written ({len(all_patterns)} patterns)')

# 6. Write KnowledgeBank/grammar_n4.md
md = ['# JLPT N4 Grammar (Bunpou)', '',
      'Source-of-truth catalogue for N4 grammar patterns. Build pipeline parses this file into `data/grammar.json`.',
      '',
      'Tier legend: `n5_prerequisite` (inherited from N5) / `core_n4` / `late_n4` / `n3_borderline`.',
      '',
      'Note: this is a SEED catalogue with structural placeholders. Detailed form rules, examples, and common-mistakes are authored in subsequent passes.',
      '',
      '---',
      '']

# Group by category, write all 18 N4 categories
cat_buckets = {i: [] for i in range(1, 19)}
for e in n4_built:
    cat_buckets[e['categoryOrder']].append(e)

md.append('## N4 NEW PATTERNS')
md.append('')
md.append(f'{len(n4_built)} patterns from n4-grammar-inventory.md, distributed across 18 categories.')
md.append('')

for cat_idx in sorted(CATEGORIES.keys()):
    md.append(f'## {cat_idx}. {CATEGORIES[cat_idx]}')
    md.append('')
    bucket = cat_buckets[cat_idx]
    if not bucket:
        md.append('(no inventory patterns categorized here yet)')
        md.append('')
        continue
    for e in bucket:
        md.append(f"### {e['pattern']} - {e['id']}")
        md.append(f"**Meaning EN:** {e['meaning_en']}")
        md.append(f"**Meaning JA:** (to be authored)")
        md.append(f"**Tier:** {e['tier']}")
        md.append(f"**Form rules:** (to be authored - see §12.2)")
        md.append(f"**Examples:**")
        md.append(f"- (to be authored - 2-5 examples drawn from N4 vocab)")
        md.append(f"**Common mistakes:**")
        md.append(f"- (to be authored - 1-3 entries per Pass-13 lessons)")
        md.append(f"**Notes:**")
        md.append('')

md.extend(['', '---', '', '## N5 prerequisites',
           '',
           'N5 grammar is a hard prerequisite. Review it via the N5 sibling app at',
           'https://gauravaccentureproducts.github.io/jlpt-n5-tutor/.',
           ''])

(ROOT / 'KnowledgeBank' / 'grammar_n4.md').write_text(
    '\n'.join(md) + '\n', encoding='utf-8')
print(f'[6] KnowledgeBank/grammar_n4.md written')

# 7. Distribution report
print('\nN4 pattern distribution by category:')
for cat_idx in sorted(CATEGORIES.keys()):
    print(f'  {cat_idx:2d}. {CATEGORIES[cat_idx]:50s} {len(cat_buckets[cat_idx]):3d}')

print('\nDone. Run python tools/check_content_integrity.py to verify.')
