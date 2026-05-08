"""HI-18 + HI-19: replace romanized Japanese tokens with Japanese script.

Walks targeted explanation/gloss/meaning fields across all content data
and applies a curated list of substitutions. Skips structural tag
fields (pos, type, label, attaches_to, acceptedAnswers, verb_class etc.)
where romaji is the intentional code-level value.

Run with --dry-run first to review.
"""
from __future__ import annotations
import argparse
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent.parent

# Fields where we should NOT touch values (structural / code-level)
SKIP_FIELDS = {
    'reading', 'on', 'kun', 'id', 'kbSourceId', 'paperNumber', 'paperId',
    'category', 'patternId', 'pattern', 'lemma', 'form', 'char', 'kanji',
    'audio', 'audio_path', 'mp3',
    'romaji', 'pronunciation',
    'choices', 'stem', 'stem_html', 'text', 'script_ja', 'prompt_ja',
    'mondai',
    '_meta', 'provenance',
    'meanings_provenance', 'gloss_provenance', 'explanation_hi_provenance',
    'distractor_explanations_hi_provenance', 'rationale_hi_provenance',
    'summary_hi_provenance', 'l1_notes_provenance',
    'voice_planned', 'audio_render_meta', 'engine', 'speaker_role_map',
    'voice_variety_status',
    'review_status',
    # Structural tag fields
    'pos', 'tier', 'type', 'subtype', 'verb_class', 'kbCategory',
    'category_id', 'categoryId', 'pair_id', 'pairId', 'patterns_used',
    'topic', 'topics', 'tags', 'register', 'difficulty', 'level',
    'attaches_to', 'requires', 'verb_groups', 'group',
    'form_rules', 'conjugations', 'acceptedAnswers',
    'label',
    'audio_render_meta', 'rendered_at',
    'speaker_role_map',
    'voice_variety_status',
    'speakers', 'speaker',
    'kana_only',
    'rendered_voices',
    'mondai_label',
    # avoid touching example arrays which legitimately contain Japanese plus example romaji
    # we will walk into nested examples but skip the 'romaji' subfield
}

# ============================================================================
# Substitution rules (regex_pattern, replacement, name, applies_to_lang)
# applies_to_lang: 'en' | 'hi' | 'both'
# ============================================================================
RULES = [
    # ---- B. Form-name compounds (work in both EN and HI text) ----
    (r'\bmasu-form\b',  'ます-form',   'masu-form',  'en'),
    (r'\bte-form\b',    'て-form',     'te-form',    'en'),
    (r'\bta-form\b',    'た-form',     'ta-form',    'en'),
    (r'\bnai-form\b',   'ない-form',   'nai-form',   'en'),
    (r'\btai-form\b',   'たい-form',   'tai-form',   'en'),
    (r'\bba-form\b',    'ば-form',     'ba-form',    'en'),
    (r'\btara-form\b',  'たら-form',   'tara-form',  'en'),
    (r'\btari-form\b',  'たり-form',   'tari-form',  'en'),
    (r'\bnakute-form\b', 'なくて-form', 'nakute-form', 'en'),
    (r'\bkute-form\b',  'くて-form',   'kute-form',  'en'),
    (r'\bnakatta-form\b', 'なかった-form', 'nakatta-form', 'en'),

    # ---- B (HI side): same form names with Devanagari -रूप ----
    (r'\bmasu-रूप\b', 'ます-रूप',   'masu-roop',   'hi'),
    (r'\bte-रूप\b',   'て-रूप',     'te-roop',     'hi'),
    (r'\bta-रूप\b',   'た-रूप',     'ta-roop',     'hi'),
    (r'\bnai-रूप\b',  'ない-रूप',   'nai-roop',    'hi'),
    (r'\btai-रूप\b',  'たい-रूप',   'tai-roop',    'hi'),
    (r'\bba-रूप\b',   'ば-रूप',     'ba-roop',     'hi'),
    (r'\btara-रूप\b', 'たら-रूप',   'tara-roop',   'hi'),

    # ---- C. Adjective-type names (both EN and HI surfaces) ----
    (r'\bna-adjective\b', 'な-adjective', 'na-adjective', 'en'),
    (r'\bi-adjective\b',  'い-adjective', 'i-adjective',  'en'),
    (r'\bna-adj\b',       'な-adj',       'na-adj',       'en'),
    (r'\bi-adj\b',        'い-adj',       'i-adj',        'en'),
    (r'\bna-विशेषण\b',    'な-विशेषण',    'na-vishesh',   'hi'),
    (r'\bi-विशेषण\b',     'い-विशेषण',    'i-vishesh',    'hi'),

    # ---- D. Verb-group names (less common but worth covering) ----
    (r'\bru-verb\b',      'る-verb',     'ru-verb',     'en'),
    (r'\bu-verb\b',       'う-verb',     'u-verb',      'en'),

    # ---- HI-18: Devanagari kana-transliteration → kana ----
    # (Limited scope: only when followed by Hindi grammar terms.)
    (r'\bना-विशेषण\b', 'な-विशेषण', 'devanagari-na-vishesh', 'hi'),

    # ---- Hindi-text-romanized: tha tha (Hindi past marker) ----
    # Specific phrase from the audit; doesn't generalize without context.
    (r'\btha tha\b', 'था-था', 'tha-tha', 'hi'),
]

# We do NOT include bare `masu`/`desu`/`tai`/`nai`/`watashi`/`ga`/etc.
# in the regex sweep because they'd false-positive (e.g. inside English
# words). Those few cases are surfaced by the diagnostic and will be
# hand-fixed in a separate per-pattern pass.

TARGET_FIELDS_HINT = {
    'gloss', 'gloss_hi',
    'meaning', 'meaning_en', 'meaning_hi',
    'meanings', 'meanings_hi',  # list-valued; we walk into elements
    'explanation', 'explanation_en', 'explanation_hi',
    'rationale', 'rationale_en', 'rationale_hi',
    'summary', 'summary_en', 'summary_hi',
    'description',
    'hint', 'hint_hi',
    'distractor_explanations', 'distractor_explanations_hi',  # dict or list
    'common_mistakes',  # list of dicts
    'cultural_note', 'cultural_callout',
    'mnemonic', 'mnemonic_hi',
    'l1_notes',  # dict; walk into .hi
    'why', 'fix',  # inside common_mistakes
    'note', 'notes',
    'hi', 'en',  # generic translation slots
}

def has_devanagari(s: str) -> bool:
    return any('ऀ' <= ch <= 'ॿ' for ch in s)


def apply_subs(value: str) -> tuple[str, list[str]]:
    """Apply rules to a string. Return (new_value, list-of-rule-names-applied)."""
    if not isinstance(value, str):
        return value, []
    is_hindi = has_devanagari(value)
    applied = []
    new = value
    for pat, repl, name, lang in RULES:
        if lang == 'en' and is_hindi:
            # English-only rules can still apply inside a Hindi string
            # because the romanization bug shows up there too (e.g.,
            # "te-form की tha tha का त-रूप"). Allow.
            pass
        if lang == 'hi' and not is_hindi:
            continue
        before = new
        new = re.sub(pat, repl, new)
        if new != before:
            applied.append(name)
    return new, applied


change_log = defaultdict(int)
file_change_log = defaultdict(int)


def walk(node, path, file_label, parent_key=None, dry_run=False):
    if isinstance(node, dict):
        for k in list(node.keys()):
            if isinstance(k, str) and k in SKIP_FIELDS:
                continue
            new_path = f'{path}.{k}' if path else k
            v = node[k]
            if isinstance(v, str):
                new_val, applied = apply_subs(v)
                if applied:
                    if not dry_run:
                        node[k] = new_val
                    for r in applied:
                        change_log[r] += 1
                    file_change_log[file_label] += 1
                    if dry_run and file_change_log[file_label] <= 3:
                        print(f'  {file_label}::{new_path}')
                        print(f'    rules: {applied}')
                        print(f'    before: {v[:140]}')
                        print(f'    after:  {new_val[:140]}')
            else:
                walk(v, new_path, file_label, k, dry_run)
    elif isinstance(node, list):
        for i in range(len(node)):
            elem = node[i]
            if isinstance(elem, str):
                new_val, applied = apply_subs(elem)
                if applied:
                    if not dry_run:
                        node[i] = new_val
                    for r in applied:
                        change_log[r] += 1
                    file_change_log[file_label] += 1
            else:
                walk(elem, f'{path}[{i}]', file_label, parent_key, dry_run)


def process_file(path: Path, dry_run: bool):
    file_label = path.relative_to(ROOT).as_posix()
    data = json.loads(path.read_text(encoding='utf-8'))
    walk(data, '', file_label, dry_run=dry_run)
    if not dry_run and file_change_log.get(file_label, 0) > 0:
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8'
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    files = []
    for fname in ['vocab.json', 'kanji.json', 'grammar.json', 'reading.json',
                  'listening.json', 'questions.json']:
        p = ROOT / 'data' / fname
        if p.exists():
            files.append(p)
    papers_dir = ROOT / 'data' / 'papers'
    if papers_dir.exists():
        for pf in papers_dir.rglob('*.json'):
            if pf.name != 'manifest.json':
                files.append(pf)
    for lf in ['en.json', 'hi.json']:
        p = ROOT / 'locales' / lf
        if p.exists():
            files.append(p)

    print(f'{"DRY RUN: " if args.dry_run else ""}processing {len(files)} files')
    for p in files:
        process_file(p, dry_run=args.dry_run)

    print(f'\n## Per-rule change counts')
    for rule, count in sorted(change_log.items(), key=lambda x: -x[1]):
        print(f'  {rule:<30} {count}')
    print(f'\n## Per-file change counts (top 15)')
    for f, count in sorted(file_change_log.items(), key=lambda x: -x[1])[:15]:
        print(f'  {f}: {count} occurrences in {count} field(s)')
    print(f'\nTotal rule applications: {sum(change_log.values())}')
    print(f'Total file-fields touched: {sum(file_change_log.values())}')


if __name__ == '__main__':
    main()
