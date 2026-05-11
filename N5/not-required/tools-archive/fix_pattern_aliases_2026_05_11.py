"""P3.34: Tag pattern aliases explicitly.

Pairs like n5-014 ↔ n5-039 both cover "これ／それ／あれ／どれ" with
DIFFERENT content (different examples, mistakes, citations). They're
intentional dual-coverage patterns mirroring how Genki / Minna re-cover
the same concept across multiple lessons. NOT byte-duplicates.

This pass adds a small `_alias_of` metadata field to each member of an
alias pair so the renderer can show a "Also see: n5-XXX" cross-link
badge. Both directions get tagged (n5-014 has _alias_of=n5-039, and
n5-039 has _alias_of=n5-014).
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

grammar_path = ROOT / 'data' / 'grammar.json'
data = json.loads(grammar_path.read_text(encoding='utf-8'))

# Known alias pairs (intentional dual-coverage; preserved from N5 corpus).
ALIASES = [
    ('n5-014', 'n5-039'),  # これ／それ／あれ／どれ
    ('n5-015', 'n5-040'),  # この／その／あの／どの ＋ N
    ('n5-016', 'n5-041'),  # ここ／そこ／あそこ／どこ
    ('n5-017', 'n5-045'),  # 何（なに／なん）
    ('n5-018', 'n5-046'),  # だれ／どなた
    ('n5-021', 'n5-114'),  # から〜まで
]

by_id = {p['id']: p for p in data['patterns']}
tagged = 0
for a, b in ALIASES:
    if a in by_id and b in by_id:
        by_id[a]['_alias_of'] = b
        by_id[b]['_alias_of'] = a
        tagged += 2

# Also tag the same-title homonyms (が / か):
HOMONYM_PAIRS = [
    ('n5-003', 'n5-126'),  # が (subject) vs が (but)
    ('n5-023', 'n5-024'),  # か (question) vs か (or)
]
for a, b in HOMONYM_PAIRS:
    if a in by_id and b in by_id:
        # Different meanings — use a different tag
        by_id[a]['_homonym_of'] = b
        by_id[b]['_homonym_of'] = a
        tagged += 2

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print(f'Tagged: {tagged} entries')
print(f'  {len(ALIASES)} alias pairs (same concept, dual coverage)')
print(f'  {len(HOMONYM_PAIRS)} homonym pairs (same kana, different meanings)')
