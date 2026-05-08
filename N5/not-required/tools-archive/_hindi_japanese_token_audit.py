"""Find Japanese tokens romanized into English/Hindi when they should stay
in Japanese script.

Scans both English fields (gloss, meaning, explanation, summary, rationale,
notes_*) and Hindi fields (*_hi) across all content data + UI strings.

Categories detected:
  A. Particles    : wa/ga/wo/ni/de/to/mo/yo/ne/no/kara/made (should be は/が/を/に/で/と/も/よ/ね/の/から/まで)
  B. Forms        : te-form/ta-form/nai-form/masu/desu/tai-form/ba-form/tara-form (should be て-form / た-form / etc.)
  C. Adjectives   : na-adjective/i-adjective/na-adj/i-adj (should be な- / い-)
  D. Verb groups  : ru-verb/u-verb/ichidan/godan (should be る-verb / う-verb / 一段 / 五段)
  E. Honorifics   : o-prefix/go-prefix (should be お / ご)
  F. Counters     : ko/tsu/hon/mai/nin/sai/satsu (without preceding kanji number)
  G. Sentence-end : yo/ne/wa/no (when discussed as particles)

Filters out fields where romaji is intentional:
  - vocab.reading (intentional romaji/kana)
  - kanji.on / kanji.kun (intentional)
  - kbSourceId / id / paperNumber (intentional)
  - any field containing 'romaji' in its name

Outputs per category: count, sample paths, sample text excerpts.
"""
from __future__ import annotations
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent.parent

# Fields where romaji is intentionally allowed (skip them)
SKIP_FIELDS = {
    'reading', 'on', 'kun', 'id', 'kbSourceId', 'paperNumber', 'paperId',
    'category', 'patternId', 'pattern', 'lemma', 'form', 'char', 'kanji',
    'audio', 'audio_path', 'mp3',
    'romaji', 'pronunciation',
    'choices', 'stem', 'stem_html', 'text', 'script_ja', 'prompt_ja',
    'mondai',
    'l1_notes',  # nested dict, walks into .hi etc separately
    'examples',  # may contain romaji intentionally
    '_meta', 'note', 'provenance',  # metadata
    'meanings_provenance', 'gloss_provenance', 'explanation_hi_provenance',
    'distractor_explanations_hi_provenance', 'rationale_hi_provenance',
    'summary_hi_provenance',
    'voice_planned', 'audio_render_meta', 'engine', 'speaker_role_map',
    'voice_variety_status',
    'review_status',
    'collocations',
    # Structural / tag fields — code-level, not learner-facing
    'pos', 'tier', 'type', 'subtype', 'verb_class', 'kbCategory',
    'category_id', 'categoryId', 'pair_id', 'pairId', 'patterns_used',
    'topic', 'topics', 'tags', 'register', 'difficulty', 'level',
    'attaches_to', 'requires', 'verb_groups', 'group',
    'form_rules', 'conjugations', 'acceptedAnswers',  # contain romaji answer keys
    'label',  # often code-tag-like
}

# Fields whose VALUES are explanatory text we want to scan
TARGET_FIELDS = {
    'gloss', 'gloss_hi',
    'meaning', 'meaning_en', 'meaning_hi',
    'meanings', 'meanings_hi',
    'explanation', 'explanation_en', 'explanation_hi',
    'rationale', 'rationale_en', 'rationale_hi',
    'summary', 'summary_en', 'summary_hi',
    'description',
    'hint', 'hint_hi',
    'distractor_explanations', 'distractor_explanations_hi',
    'common_mistakes', 'cultural_note', 'cultural_callout',
    'mnemonic', 'mnemonic_hi',
    'hi',  # generic l1_notes.hi etc.
    'en',
    'note', 'notes',  # text fields (different from _meta.note)
}

# ============================================================================
# Patterns
# ============================================================================
# Conservative: only flag when surrounded by clear pedagogical context
# Use word boundaries + nearby cues to avoid false positives.

# Category A: Particles. Must be standalone token, often near "particle" or after a number
# or in quoted/italic context. Use the word boundary + non-letter context.
PARTICLE_TOKENS = ['wa', 'ga', 'wo', 'ni', 'de', 'to', 'mo', 'yo', 'ne', 'no', 'kara', 'made', 'he']
# Pattern: " 'wa' " or '"wa"' or " wa-particle" or " (wa)" or " wa が" etc.
# Most reliable: token in single quotes followed by 'particle' nearby, OR token-particle compound
PARTICLE_RE = re.compile(
    r"(?<![a-zA-Z])(?:'|\"|`|‘|’|“|”)?(" + '|'.join(PARTICLE_TOKENS) + r")(?:'|\"|`|‘|’|“|”)?[\s\-–—]*(?:particle|कण)(?![a-z])",
    re.IGNORECASE
)
# Inverse: "particle wa" / "कण wa"
PARTICLE_RE_2 = re.compile(
    r"(?:particle|कण)[\s\-–—]*(?:'|\"|`|‘|’|“|”)?(" + '|'.join(PARTICLE_TOKENS) + r")(?:'|\"|`|‘|’|“|”)?(?![a-z])",
    re.IGNORECASE
)

# Category B: Form-names with hyphen
FORM_TOKENS = ['te', 'ta', 'nai', 'masu', 'desu', 'tai', 'ba', 'tara', 'tari',
               'sou', 'reba', 'nakute', 'kute', 'nakatta', 'rare']
FORM_RE = re.compile(
    r'(?<![a-zA-Z])(' + '|'.join(FORM_TOKENS) + r')[\s\-]?(?:form|रूप)\b',
    re.IGNORECASE
)
# Bare 'masu' / 'desu' as words (without -form)
BARE_RE = re.compile(
    r"(?<![a-zA-Z])(?:'|\")?(masu|desu|tai|nai|sou|tara|reba)(?:'|\")?(?![a-z])",
    re.IGNORECASE
)

# Category C: na/i adjective
ADJ_RE = re.compile(
    r'(?<![a-zA-Z])(na|i)[\s\-]?(?:adjective|adj|विशेषण)\b',
    re.IGNORECASE
)

# Category D: verb groups
VERBGRP_RE = re.compile(
    r'(?<![a-zA-Z])(ru|u|ichidan|godan)[\s\-]?(?:verb|क्रिया|verbs)\b',
    re.IGNORECASE
)

# Category E: honorifics — careful, "o-" alone matches everything; require following Japanese
HONORIFIC_RE = re.compile(
    r'(?<![a-zA-Z])(o|go)[\s\-]?prefix\b',
    re.IGNORECASE
)

# Category F: numeric + counter romaji, e.g., "3-tsu", "ni-hon", "san-mai"
COUNTER_TOKENS = ['tsu', 'hon', 'mai', 'nin', 'satsu', 'hiki', 'dai', 'kai',
                  'fun', 'pun', 'ji', 'ko', 'sai']
COUNTER_RE = re.compile(
    r"(?<![a-zA-Z])(?:\d+|ichi|ni|san|yon|go|roku|nana|hachi|kyuu|juu)[\s\-](" + '|'.join(COUNTER_TOKENS) + r")(?![a-z])",
    re.IGNORECASE
)

# Category G: sentence-final particles in quoted form
SF_PARTICLES_RE = re.compile(
    r"(?<![a-zA-Z])(?:'|\")(yo|ne|wa|no|ka|kana|wa|ze|na)(?:'|\")",
    re.IGNORECASE
)

# Helper: count Japanese characters in a string (kana/kanji)
def has_japanese(s: str) -> bool:
    return any(
        ('ぁ' <= ch <= 'ゖ') or  # hiragana
        ('ァ' <= ch <= 'ヺ') or  # katakana
        ('一' <= ch <= '龯')      # CJK unified
        for ch in s
    )

def has_devanagari(s: str) -> bool:
    return any('ऀ' <= ch <= 'ॿ' for ch in s)

# ============================================================================
# Scan
# ============================================================================

CATEGORIES = [
    ('A.particles',     PARTICLE_RE),
    ('A.particles-rev', PARTICLE_RE_2),
    ('B.forms',         FORM_RE),
    ('B.bare-form',     BARE_RE),
    ('C.adjectives',    ADJ_RE),
    ('D.verb-groups',   VERBGRP_RE),
    ('E.honorifics',    HONORIFIC_RE),
    ('F.counters',      COUNTER_RE),
]

# We'll classify hits as English-context vs Hindi-context based on whether the
# enclosing string contains Devanagari.

results = defaultdict(list)  # (category, lang) -> [(path, match_text, value_excerpt)]

def scan_string(value, path, file_label):
    if not isinstance(value, str) or len(value.strip()) < 3:
        return
    lang = 'hi' if has_devanagari(value) else 'en'
    for cat_name, regex in CATEGORIES:
        for m in regex.finditer(value):
            full_match = m.group(0)
            captured = m.group(1) if m.lastindex else full_match
            # Skip false positives: if the same string ALREADY contains the kana version
            # nearby, the romaji is probably an intentional pronunciation aid.
            # (Best-effort heuristic — review samples manually.)
            results[(cat_name, lang)].append((f'{file_label}::{path}', full_match, value[:160]))

def walk(node, path, file_label, parent_key=None):
    if isinstance(node, dict):
        for k, v in node.items():
            if isinstance(k, str) and k in SKIP_FIELDS:
                continue
            new_path = f'{path}.{k}' if path else k
            walk(v, new_path, file_label, parent_key=k)
    elif isinstance(node, list):
        for i, item in enumerate(node):
            walk(item, f'{path}[{i}]', file_label, parent_key=parent_key)
    elif isinstance(node, str):
        # Only scan if the parent key is a target field OR not in skip list
        if parent_key in TARGET_FIELDS or (parent_key is not None and parent_key not in SKIP_FIELDS):
            scan_string(node, path, file_label)

# Scan content data
for fname in ['vocab.json', 'kanji.json', 'grammar.json', 'reading.json',
              'listening.json', 'questions.json']:
    path = ROOT / 'data' / fname
    if not path.exists():
        continue
    data = json.loads(path.read_text(encoding='utf-8'))
    walk(data, '', fname)

# Scan paper files
papers_dir = ROOT / 'data' / 'papers'
if papers_dir.exists():
    for pf in papers_dir.rglob('*.json'):
        if pf.name == 'manifest.json':
            continue
        try:
            data = json.loads(pf.read_text(encoding='utf-8'))
            walk(data, '', f'papers/{pf.parent.name}/{pf.name}')
        except Exception:
            pass

# Scan locales
for lf in ['en.json', 'hi.json']:
    p = ROOT / 'locales' / lf
    if p.exists():
        walk(json.loads(p.read_text(encoding='utf-8')), '', f'locales/{lf}')

# ============================================================================
# Report
# ============================================================================

print('=' * 72)
print('Japanese-token-romanized scan: English vs Hindi')
print('=' * 72)

cat_summary = defaultdict(lambda: {'en': 0, 'hi': 0})
for (cat, lang), hits in results.items():
    cat_summary[cat][lang] += len(hits)

print(f"\n{'Category':<22} {'en hits':>10} {'hi hits':>10}")
print('-' * 50)
for cat in sorted(cat_summary.keys()):
    en = cat_summary[cat]['en']
    hi = cat_summary[cat]['hi']
    print(f'{cat:<22} {en:>10} {hi:>10}')

# Per-category samples
for cat in sorted(set(c for c, _ in results.keys())):
    en_hits = results.get((cat, 'en'), [])
    hi_hits = results.get((cat, 'hi'), [])
    if not (en_hits or hi_hits):
        continue
    print('\n' + '=' * 72)
    print(f'## {cat}: en={len(en_hits)}, hi={len(hi_hits)}')
    print('=' * 72)
    if en_hits:
        print(f'\n--- English examples (first 6) ---')
        # Dedupe by match text
        seen = set()
        shown = 0
        for path, match, excerpt in en_hits:
            if match.lower() in seen:
                continue
            seen.add(match.lower())
            shown += 1
            print(f'  [{match!r}] @ {path[:80]}')
            print(f'    "{excerpt}"')
            if shown >= 6: break
    if hi_hits:
        print(f'\n--- Hindi examples (first 6) ---')
        seen = set()
        shown = 0
        for path, match, excerpt in hi_hits:
            if match.lower() in seen:
                continue
            seen.add(match.lower())
            shown += 1
            print(f'  [{match!r}] @ {path[:80]}')
            print(f'    "{excerpt}"')
            if shown >= 6: break

# Grand totals
total_en = sum(c['en'] for c in cat_summary.values())
total_hi = sum(c['hi'] for c in cat_summary.values())
print('\n' + '=' * 72)
print(f'GRAND TOTAL: en={total_en}, hi={total_hi}')
print('=' * 72)
