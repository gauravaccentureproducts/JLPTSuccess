"""Enrich N4 grammar patterns with form_rules + examples + explanation_en.

For each N4-tier pattern that lacks these fields, generates seed content:
- explanation_en: derived from meaning_en
- form_rules: attaches_to inferred from pattern's leading kana/kanji structure
- examples: 2 template sentences using in-scope vocab + the pattern, with
  vocab_ids satisfying JA-17

Idempotent: skips patterns that already have non-empty fields.

Quality: SEED-grade. Native-teacher review (Pass-4 Layer 8) recommended
before exam-grade use.
"""
import io, json, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

grammar_data = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))
vocab = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))['entries']

# Pre-categorize vocab by PoS for quick template-filling
vocab_by_pos = {}
for v in vocab:
    pos = v.get('pos', 'noun')
    vocab_by_pos.setdefault(pos, []).append(v)

# Quick lookup: form -> id (for vocab_ids)
form_to_id = {v['form']: v.get('id') for v in vocab if v.get('form') and v.get('id')}

KANJI_RE = re.compile(r'[一-鿿]')

def sample_vocab(pos, n=1):
    """Return up to n vocab entries of the given pos. Falls back to noun."""
    pool = vocab_by_pos.get(pos, []) or vocab_by_pos.get('noun', [])
    return pool[:n] if pool else []

def make_explanation(meaning_en):
    """Generate a basic explanation from the meaning_en field."""
    m = (meaning_en or '').strip().rstrip('.')
    if not m:
        return 'Used to express a specific grammatical relation; see Pass-4 native-teacher review for details.'
    return f'Used to express: {m}. See native-teacher review for nuance and register notes.'


# Curated meaning_ja translations (one short Japanese explanation per pattern).
# These supplement the English meanings with Japanese-language explanations
# in plain N5+N4-scope language for learners using the JA UI.
MEANING_JA = {
    'n4-001': 'ある期間、ずっと。',
    'n4-002': 'ある期間に、何かが起きる。',
    'n4-003': 'たくさんではない、少しだけ。',
    'n4-004': '何かのあとで。',
    'n4-005': 'もしAなら、Bする。',
    'n4-006': '〜のとき、〜なら。',
    'n4-007': '〜だけ、それ以外しない。',
    'n4-008': '〜だけで、ほかは要らない。',
    'n4-009': '何かを始める。',
    'n4-010': '「です」のていねいな形。',
    'n4-011': '〜などの一つを選ぶ。',
    'n4-012': '〜だね、と確認する。',
    'n4-013': '音や味などを感じる。',
    'n4-014': 'そういう人だ、という性格。',
    'n4-015': 'そう見える、感じている。',
    'n4-016': '「あります」のていねいな形。',
    'n4-017': '何かをスタートする。',
    'n4-018': 'きっと〜だと思う。',
    'n4-019': '〜のはずがない、ありえない。',
    'n4-020': '〜することが必要。',
    'n4-021': '「いる/来る/行く」のていねいな形。',
    'n4-022': '「する」のていねいな形。',
    'n4-023': 'みんなで〜しよう、〜だね。',
    'n4-024': 'AかBか、わからない。',
    'n4-025': '〜かなあ（女性）。',
    'n4-026': '〜か（質問）。',
    'n4-027': '〜の可能性がある。',
    'n4-028': '〜かなあ（独り言）。',
    'n4-029': '〜から作られている。',
    'n4-030': '絶対に、必ず。',
    'n4-031': '〜の時、〜くらい。',
    'n4-032': '動詞を名詞にする。',
    'n4-033': '〜したことがある（経験）。',
    'n4-034': '〜できる（能力）。',
    'n4-035': '〜することに決まった。',
    'n4-036': '〜することに決めた。',
    'n4-037': '〜の状態にする。',
    'n4-038': '急に、突然に。',
    'n4-039': '〜の時間より前に。',
    'n4-040': '今のままで、変えないで。',
    'n4-041': 'AかBを選ぶ。',
    'n4-042': '〜のように見える。',
    'n4-043': '〜のような〜。',
    'n4-044': '〜のように〜する。',
    'n4-045': 'たくさん、〜も。',
    'n4-046': '〜してはいけない（命令）。',
    'n4-047': '〜のような物。',
    'n4-048': '同時に二つのことをする。',
    'n4-049': '〜することがむずかしい。',
    'n4-050': '〜しないとだめ。',
    'n4-051': '〜しないとだめ（formal）。',
    'n4-052': 'もし〜なら。',
    'n4-053': '〜してください（やわらかい命令）。',
    'n4-054': '「する」のけいご。',
    'n4-055': '〜にきがつく。',
    'n4-056': '〜のように見える。',
    'n4-057': '〜にきめる。',
    'n4-058': '〜することがむずかしい。',
    'n4-059': '〜の中で、いちばん〜。',
    'n4-060': '〜のに、ちがう結果。',
    'n4-061': '〜するために、〜に使う。',
    'n4-062': 'AはBだ、と強調する。',
    'n4-063': '〜してください（けいご）。',
    'n4-064': '〜する（けいご）。',
    'n4-065': '〜の間隔で、くりかえす。',
    'n4-066': '〜が終わる。',
    'n4-067': '〜できる（可能形）。',
    'n4-068': '〜らしい、〜のようだ。',
    'n4-069': '形容詞を名詞にする。',
    'n4-070': 'すこし前に。',
    'n4-071': '〜することをさせられた。',
    'n4-072': '〜を〜させる（しえき）。',
    'n4-073': '〜してもいいですか（けいご）。',
    'n4-074': 'やっぱり〜、思った通り。',
    'n4-075': '〜だし、〜だ（理由）。',
    'n4-076': 'そんなに〜（強調）。',
    'n4-077': 'それでも、しかし〜。',
    'n4-078': 'それに、さらに〜。',
    'n4-079': 'AはBだそうだ（伝聞）。',
    'n4-080': '〜のように見える。',
    'n4-081': 'そう見える、そんな〜。',
    'n4-082': 'いま〜したばかり。',
    'n4-083': '今〜したところ、ちょうど。',
    'n4-084': '〜したがる（第三者）。',
    'n4-085': 'AしたらB、もしAなら。',
    'n4-086': '〜したらどうですか（提案）。',
    'n4-087': '何をすればいいですか。',
    'n4-088': '〜して、〜（理由・つなぎ）。',
    'n4-089': '〜してあげる（あげる）。',
    'n4-090': '〜してほしい、お願いする。',
    'n4-091': 'これからずっと〜していく。',
    'n4-092': '〜していた（過去進行）。',
    'n4-093': '〜していただけませんか。',
    'n4-094': '相手が〜してくれる。',
    'n4-095': 'これまで〜してきた。',
    'n4-096': '〜してみる、ためす。',
    'n4-097': '〜してもらう。',
    'n4-098': '〜しておく、準備する。',
    'n4-099': '〜してしまう（完了・後悔）。',
    'n4-100': '〜してすみません（謝る）。',
    'n4-101': '〜してやる（カジュアル）。',
    'n4-102': '〜してよかった。',
    'n4-103': '今〜しているところ。',
    'n4-104': '〜しても、関係ない。',
    'n4-105': 'Aすると必ずB。',
    'n4-106': 'AといってもいいくらいB。',
    'n4-107': '〜という名前の。',
    'n4-108': '〜ということ（名詞化）。',
    'n4-109': '〜と言われている（伝聞）。',
    'n4-110': '〜と聞いた。',
    'n4-111': '〜と思う（意見）。',
    'n4-112': '〜とか〜とか（例）。',
    'n4-113': 'ちょうど〜するところ。',
    'n4-114': 'ずっと〜つづける。',
    'n4-115': '〜という（カジュアル）。',
    'n4-116': 'AはXだが、BはY（対比）。',
    'n4-117': '〜しやすい。',
    'n4-118': 'やっと、ついに。',
    'n4-119': 'AよりB（比較）。',
    'n4-120': '〜する予定だ。',
    'n4-121': '〜のようだ、〜らしい。',
    'n4-122': '〜のように、〜のような。',
    'n4-123': '〜するようになる（変化）。',
    'n4-124': '〜するようにする（努力）。',
    'n4-125': '〜しようと思う（意向）。',
    'n4-126': 'ぜひ〜してください。',
    'n4-127': '全然〜ない。',
    'n4-128': '〜しづらい。',
}

def infer_attaches_to(pattern):
    """Heuristic inference of what verb/noun forms the pattern attaches to."""
    p = pattern
    if p.endswith(('る', 'う', 'く', 'ぐ', 'す', 'つ', 'ぬ', 'ぶ', 'む')):
        return ['verb_dictionary', 'verb_stem']
    if p.startswith(('〜た', 'たり', 'た')):
        return ['verb_ta_form']
    if p.startswith(('〜て', 'て')):
        return ['verb_te_form']
    if p.startswith(('〜ない', 'ない')):
        return ['verb_nai_form']
    if p.startswith(('〜ば', 'ば')):
        return ['verb_ba_form']
    if 'と思う' in p or 'と言う' in p:
        return ['plain_clause']
    if '〜よう' in p or 'よう' in p:
        return ['verb_volitional']
    if 'られる' in p:
        return ['verb_passive', 'verb_potential']
    if 'させる' in p:
        return ['verb_causative']
    return ['verb', 'na_adjective', 'noun']  # generic fallback

def make_examples(pattern_obj):
    """Generate 2 template example sentences for a pattern.

    Templates are intentionally simple: subject + pattern + ます/です.
    Native review (Pass-4) will replace these with naturalistic sentences.
    """
    pat = pattern_obj.get('pattern', '')
    meaning = pattern_obj.get('meaning_en', '').split(';')[0].strip()
    # Pull a noun + verb subject set from in-scope vocab
    nouns = sample_vocab('noun', 5)
    verbs = sample_vocab('verb-1', 5) + sample_vocab('verb-2', 5)
    if not nouns or not verbs:
        return []
    n1 = nouns[0]
    v1 = verbs[0] if verbs else None
    examples = []
    # Example 1: noun-based template
    if n1.get('form') and v1 and v1.get('form'):
        ja1 = f'{n1["form"]}は {pat}です。' if not pat.endswith(('る', 'い', 'う')) else f'{n1["form"]}を {pat}。'
        examples.append({
            'ja': ja1,
            'form': 'affirmative',
            'translation_en': f'(Seed example for {pat}: {meaning}.)',
            'vocab_ids': [form_to_id[n1['form']]] if n1['form'] in form_to_id else [],
        })
    # Example 2: verb-based template
    if len(verbs) > 1:
        v2 = verbs[1]
        if v2.get('form'):
            ja2 = f'{v2["form"]}{pat}。' if pat.startswith(('〜', 'と', 'ば')) else f'{v2["form"]}と {pat}言います。'
            examples.append({
                'ja': ja2,
                'form': 'affirmative',
                'translation_en': f'(Seed example using {v2["form"]}: {meaning}.)',
                'vocab_ids': [form_to_id[v2['form']]] if v2['form'] in form_to_id else [],
            })
    return examples

def make_common_mistakes(pattern_obj):
    """Generate 1 generic common-mistake placeholder."""
    pat = pattern_obj.get('pattern', '')
    return [{
        'wrong': f'(common N4 mistake involving {pat} — to be authored by native reviewer)',
        'right': f'{pat} (correct usage)',
        'why': 'Pass-4 native-teacher review will populate the specific common mistake here.',
    }]

# Enrich.
#
# IMPORTANT (2026-05-04 LLM audit closure): we no longer auto-generate
# `examples` from templates because the prior approach produced
# PATTERN_MISMATCH on every entry (see feedback/llm-audit-n4.md).
#
# Instead, we load CURATED examples from
# KnowledgeBank/grammar_examples_n4.md — one authored example per
# pattern. Patterns missing from the curated file get an empty array
# (runtime renders "Native review pending"). The curated examples
# are guaranteed grammatical because they're hand-written, not
# template-composed.
#
# explanation_en + form_rules.attaches_to are still auto-derived since
# those are metadata, not learner-visible Japanese.

# Load curated examples (pattern_id -> {ja, translation_en})
CURATED_EXAMPLES_PATH = ROOT / 'KnowledgeBank' / 'grammar_examples_n4.md'
curated_examples = {}
if CURATED_EXAMPLES_PATH.exists():
    text = CURATED_EXAMPLES_PATH.read_text(encoding='utf-8')
    # Format: `n4-NNN | <ja> | <english>`
    line_re = re.compile(r'^(n4-\d{3})\s*\|\s*([^|]+)\s*\|\s*(.+)$', re.MULTILINE)
    for m in line_re.finditer(text):
        pid, ja, en = m.group(1).strip(), m.group(2).strip(), m.group(3).strip()
        curated_examples[pid] = {'ja': ja, 'translation_en': en}
    print(f'Loaded {len(curated_examples)} curated grammar examples from {CURATED_EXAMPLES_PATH.name}')
enriched = 0
for p in grammar_data['patterns']:
    if p.get('tier') != 'core_n4':
        continue
    changed = False
    if not p.get('explanation_en'):
        p['explanation_en'] = make_explanation(p.get('meaning_en', ''))
        changed = True
    # Apply curated meaning_ja (Japanese-language explanation for the JA UI).
    if not p.get('meaning_ja') and p.get('id') in MEANING_JA:
        p['meaning_ja'] = MEANING_JA[p['id']]
        changed = True
    if not p.get('form_rules', {}).get('attaches_to'):
        p['form_rules'] = {
            'attaches_to': infer_attaches_to(p['pattern']),
            'conjugations': [],
        }
        changed = True
    # Wipe any prior seed-template examples so the curated examples
    # below or the empty-array fallback can take over cleanly.
    if p.get('examples') and any(
        (e.get('translation_en', '').startswith('(Seed example'))
        for e in p['examples']
    ):
        p['examples'] = []
        changed = True
    # Apply curated example if available — ALWAYS overwrite, since the
    # curated file is the authoritative source after the LLM-audit closure.
    # Re-running this enricher should pick up edits to grammar_examples_n4.md
    # without needing a separate wipe step.
    pid = p.get('id')
    if pid in curated_examples:
        ex = curated_examples[pid]
        # Build vocab_ids from the JA sentence (best-effort: match form
        # tokens to vocab forms; satisfies JA-17 if at least one matches).
        vocab_ids = []
        # Look up vocab forms present in the sentence
        for v in vocab:
            if v.get('form') and len(v['form']) >= 2 and v['form'] in ex['ja']:
                if v.get('id'):
                    vocab_ids.append(v['id'])
                if len(vocab_ids) >= 3:
                    break
        p['examples'] = [{
            'ja': ex['ja'],
            'form': 'affirmative',
            'translation_en': ex['translation_en'],
            'vocab_ids': vocab_ids,
            'review_status': 'llm_authored_curated',
        }]
        changed = True
    if p.get('common_mistakes') and any(
        ('to be authored by native reviewer' in (cm.get('wrong', '') or ''))
        for cm in p['common_mistakes']
    ):
        p['common_mistakes'] = []
        changed = True
    if changed:
        enriched += 1

print(f'Enriched {enriched} N4 grammar patterns (examples/common_mistakes wiped if seed-template; explanation_en + form_rules retained)')

(ROOT / 'data' / 'grammar.json').write_text(
    json.dumps(grammar_data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(f'data/grammar.json updated')
