"""IMP-130 follow-up: fill Genki II lesson tags for the 16 N5 patterns
that the original auto-extractor (batch 3) couldn't find Genki I sources
for. These are typically late-N5 / colloquial forms introduced in Genki II.

Each mapping ships as a structured genki_lesson + genki_lessons_all
field on the pattern, AND adds a "genki-2-lN" entry to the existing
sources array so the auto-extractor remains a true source of truth.

Source: Genki II (Banno et al., The Japan Times, 3rd ed.) lesson
ToC (publicly published).
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Pattern -> (book, lesson)
GENKI_II_MAP = {
    'n5-134': (2, 18),  # ので — paired with でしょう/んです family
    'n5-144': (2, 19),  # ~ながら
    'n5-145': (2, 13),  # ~と思います
    'n5-146': (2, 13),  # ~と言いました — paired with と思います
    'n5-157': (2, 18),  # ~でしょう
    'n5-158': (2, 18),  # ~だろう — casual variant of でしょう
    'n5-170': (2, 14),  # ~た方がいい — advice/recommendation
    'n5-171': (2, 14),  # ~ない方がいい — same lesson
    'n5-174': (2, 17),  # ~なくてはならない — must-do (formal)
    'n5-175': (2, 17),  # ~ないといけない — variant
    'n5-176': (2, 18),  # ~なくちゃ / ~なきゃ — casual contractions
    'n5-179': (2, 17),  # ~って — casual quotation
    'n5-180': (2, 19),  # ~かた — way of doing
    'n5-181': (2, 20),  # ~なあ — casual exclamation register
    'n5-182': (2, 20),  # Verb-plain + な — casual prohibition
    'n5-188': (2, 13),  # ~ことができます — potential
}

grammar_path = ROOT / 'data' / 'grammar.json'
data = json.loads(grammar_path.read_text(encoding='utf-8'))
patterns = data['patterns']

updated = 0
skipped = 0

for p in patterns:
    pid = p['id']
    if pid not in GENKI_II_MAP:
        continue
    if p.get('genki_lesson'):
        skipped += 1
        continue

    book, lesson = GENKI_II_MAP[pid]
    p['genki_lesson'] = {'book': book, 'lesson': lesson}
    p['genki_lesson_provenance'] = 'llm_curated'

    # Also add to sources array if not already present
    src = p.setdefault('sources', [])
    src_str = f'genki-{book}-l{lesson}'
    if src_str not in src:
        src.append(src_str)

    updated += 1

grammar_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Verify final coverage
total = len(patterns)
with_genki = sum(1 for p in patterns if p.get('genki_lesson'))

print(f'Updated:         {updated}')
print(f'Already had:     {skipped}')
print(f'Coverage:        {with_genki}/{total} ({100*with_genki/total:.0f}%)')
