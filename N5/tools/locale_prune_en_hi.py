"""Phase 4 of the en+hi locale transition (2026-05-06).

Walks every content JSON under N5/data/ and removes any key that
references the four deprecated locales (vi, id, ne, zh) or carries a
non-locale-suffixed alias for them. Writes back with consistent
formatting (2-space indent, key order preserved).

Removal patterns (case-sensitive, exact key match):
  Locale-suffixed fields: <basename>_<lc> for lc in {vi,id,ne,zh}
    Common bases observed in the corpus: gloss, meaning, meanings,
    explanation, notes, title, prompt, description, note.
  Locale-keyed dict entries: dict.{vi,id,ne,zh} on any object whose
    sibling keys include 'en' or whose parent key matches a known
    translations container (gloss_translations, meanings_translations,
    l1_notes, false_friends).
  Locale-suffixed provenance/status fields: <basename>_provenance with
    a value referencing a deprecated locale (left alone - provenance is
    metadata about the translation, not the translation itself).

After pruning, the script also REMOVES `false_friends.zh` (since the
zh locale is gone) but does not seed `false_friends.hi` placeholders -
those come from a separate authoring pass.

Idempotent: re-runs on an already-pruned file delete nothing extra.

NOT in scope this script: seeding gloss_hi / meanings_hi placeholders.
That's a separate authoring pass - the schema slots are created here
implicitly by leaving _en values in place; a follow-up Hindi-translation
authoring pass populates the _hi side.

N4 protection: refuses to write any path under /N4/.
"""
from __future__ import annotations
import io, json, os, re, sys
from collections import defaultdict
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent  # N5/
REPO_ROOT = ROOT.parent
DEPRECATED = ('vi', 'id', 'ne', 'zh')

# Top-level data files to walk
DATA_FILES = [
    'data/grammar.json',
    'data/vocab.json',
    'data/kanji.json',
    'data/reading.json',
    'data/listening.json',
    'data/questions.json',
]

# Plus all paper files
PAPER_GLOB = 'data/papers/**/*.json'

# Field-key match: <known_base>_<lc>
# IMPORTANT: this regex must be specific. Earlier draft used
# `[a-zA-Z_]+_(vi|id|ne|zh)` which falsely captured `with_pattern_id`
# (it ends in `_id`) and `pair_id` (also ends in `_id`). Those are
# contrast / transitivity-pair fields, not locale translations.
# The fix is to enumerate the KNOWN translation-base names explicitly.
TRANSLATION_BASES = ('gloss', 'meaning', 'meanings', 'explanation',
                     'notes', 'note', 'title', 'prompt', 'description',
                     'rationale', 'hint', 'summary', 'translation')
LOCALE_SUFFIX_RE = re.compile(
    r'^(?:' + '|'.join(TRANSLATION_BASES) + r')_(?:vi|id|ne|zh)$'
)

# Provenance fields where a value-level deprecated-locale reference doesn't
# require deletion. Keep these; they are metadata.
PROVENANCE_FIELDS = {'gloss_provenance', 'meanings_provenance',
                     'meaning_provenance', 'explanation_provenance'}

# Container keys whose direct dict children are the per-locale subtree
# (so direct keys 'vi','id','ne','zh' should be removed).
LOCALE_CONTAINER_KEYS = {'gloss_translations', 'meanings_translations',
                         'l1_notes', 'false_friends', 'meaning_translations',
                         'explanation_translations', 'translations'}


def prune(node, parent_key=None, stats=None):
    """Recursive walk; mutates dicts/lists in place."""
    if stats is None:
        stats = defaultdict(int)
    if isinstance(node, dict):
        # First pass: identify keys to delete.
        to_del = []
        for k in list(node.keys()):
            if k in PROVENANCE_FIELDS:
                continue
            # Pattern 1: locale-suffixed field name
            if LOCALE_SUFFIX_RE.match(k):
                to_del.append(k)
                stats[f'removed:{k}'] += 1
                continue
            # Pattern 2: direct deprecated-locale key inside a container
            if k in DEPRECATED and parent_key in LOCALE_CONTAINER_KEYS:
                to_del.append(k)
                stats[f'removed:{parent_key}.{k}'] += 1
                continue
        for k in to_del:
            del node[k]
        # Second pass: recurse into surviving keys.
        for k, v in list(node.items()):
            if isinstance(v, (dict, list)):
                prune(v, parent_key=k, stats=stats)
    elif isinstance(node, list):
        for item in node:
            if isinstance(item, (dict, list)):
                prune(item, parent_key=parent_key, stats=stats)
    return stats


def process_file(path: Path, stats: defaultdict) -> int:
    if '/N4/' in str(path).replace('\\', '/'):
        raise RuntimeError(f'N4 protection: refusing to touch {path}')
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
    except Exception as e:
        print(f'  parse error on {path.name}: {e}')
        return 0
    before = len(stats)
    file_stats = defaultdict(int)
    prune(data, stats=file_stats)
    n = sum(file_stats.values())
    if n > 0:
        path.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8'
        )
        for k, v in file_stats.items():
            stats[k] += v
    return n


def main() -> int:
    stats = defaultdict(int)
    paths = []
    for rel in DATA_FILES:
        p = ROOT / rel
        if p.exists():
            paths.append(p)

    # Glob papers
    papers_dir = ROOT / 'data' / 'papers'
    if papers_dir.exists():
        for p in sorted(papers_dir.rglob('*.json')):
            paths.append(p)

    print(f'Walking {len(paths)} files...')
    total_removals = 0
    for p in paths:
        n = process_file(p, stats)
        if n > 0:
            rel = p.relative_to(ROOT)
            print(f'  {rel}: removed {n} keys')
            total_removals += n

    print(f'\nTotal keys removed: {total_removals}')
    print(f'Per-pattern breakdown:')
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        if v > 0:
            print(f'  {k}: {v}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
