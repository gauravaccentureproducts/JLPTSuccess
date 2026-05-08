"""JCE-8: Add chapter-specific Genki / Minna citations to grammar patterns.

Currently 27/178 patterns have chapter-specific citations (e.g.,
genki-1-l3, minna-1-c5); 151 have only generic citations
(bunpro-n5, jlpt-sensei-n5, jlpt-jp-official). This script fills the
chapter-specific Genki I lesson + Minna no Nihongo I chapter for
the remaining 151, based on standard curricula.

Reference:
  - Genki I (3rd ed., Banno et al.): Lessons 1-12 cover N5
  - Minna no Nihongo I (3A Network): Chapters 1-25 cover N5

Idempotent: only adds citations not already present (preserves any
existing chapter-specific citation; appends Genki/Minna where missing).
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR = ROOT / 'data' / 'grammar.json'

# Map: pattern_id -> (genki_lesson, minna_chapter)
# 'multi' for Minna means the pattern spans multiple chapters
# None for Genki means pattern is borderline / not in Genki I scope
MAPPING: dict[str, tuple[str | None, str | None]] = {
    # Particles + sentence enders (Genki l1-l4, Minna c1-c5)
    'n5-031': ('genki-1-l4', 'minna-1-c4'),
    'n5-033': ('genki-1-l11', 'minna-1-c11'),
    'n5-034': ('genki-1-l11', 'minna-1-c25'),
    'n5-035': ('genki-1-l4', 'minna-1-c11'),
    'n5-036': ('genki-1-l3', 'minna-1-c4'),
    'n5-037': ('genki-1-l11', 'minna-1-c14'),
    'n5-038': ('genki-1-l11', 'minna-1-c14'),
    # Demonstratives (kosoado, Genki l2, Minna c2-c3)
    'n5-039': ('genki-1-l2', 'minna-1-c2'),
    'n5-040': ('genki-1-l2', 'minna-1-c2'),
    'n5-041': ('genki-1-l2', 'minna-1-c3'),
    'n5-042': ('genki-1-l2', 'minna-1-c3'),
    'n5-043': ('genki-1-l2', 'minna-1-c3'),
    'n5-044': ('genki-1-l2', 'minna-1-c3'),
    # Question words (Genki l2-l3, Minna c1-c4)
    'n5-045': ('genki-1-l1', 'minna-1-c1'),
    'n5-046': ('genki-1-l1', 'minna-1-c1'),
    'n5-048': ('genki-1-l2', 'minna-1-c3'),
    'n5-049': ('genki-1-l2', 'minna-1-c3'),
    'n5-050': ('genki-1-l3', 'minna-1-c8'),
    'n5-051': ('genki-1-l3', 'minna-1-c9'),
    'n5-052': ('genki-1-l11', 'minna-1-c14'),
    'n5-053': ('genki-1-l2', 'minna-1-c3'),
    'n5-054': ('genki-1-l3', 'minna-1-c11'),
    'n5-055': ('genki-1-l1', 'minna-1-c4'),
    'n5-056': ('genki-1-l1', 'minna-1-c4'),
    'n5-057': ('genki-1-l1', 'minna-1-c5'),
    # Verb-masu paradigm (Genki l3, Minna c4-c6)
    'n5-058': ('genki-1-l3', 'minna-1-c4'),
    'n5-059': ('genki-1-l3', 'minna-1-c4'),
    'n5-060': ('genki-1-l3', 'minna-1-c4'),
    'n5-061': ('genki-1-l3', 'minna-1-c4'),
    'n5-062': ('genki-1-l3', 'minna-1-c6'),
    'n5-063': ('genki-1-l3', 'minna-1-c6'),
    'n5-064': ('genki-1-l3', 'minna-1-c6'),
    # Verb plain forms (Genki l8-l9, Minna c14-c20)
    'n5-065': ('genki-1-l8', 'minna-1-c18'),
    'n5-066': ('genki-1-l8', 'minna-1-c17'),
    'n5-067': ('genki-1-l9', 'minna-1-c19'),
    'n5-068': ('genki-1-l9', 'minna-1-c19'),
    # te-form paradigm (Genki l6-l7, Minna c14-c16)
    'n5-069': ('genki-1-l6', 'minna-1-c14'),
    'n5-070': ('genki-1-l6', 'minna-1-c14'),
    'n5-071': ('genki-1-l6', 'minna-1-c14'),
    'n5-072': ('genki-1-l7', 'minna-1-c14'),
    'n5-073': ('genki-1-l7', 'minna-1-c14'),
    'n5-074': ('genki-1-l6', 'minna-1-c15'),
    'n5-075': ('genki-1-l6', 'minna-1-c15'),
    'n5-076': ('genki-1-l6', 'minna-1-c16'),
    'n5-077': ('genki-1-l8', 'minna-1-c17'),
    # i-Adjective paradigm (Genki l5, Minna c8-c12)
    'n5-078': ('genki-1-l5', 'minna-1-c8'),
    'n5-079': ('genki-1-l5', 'minna-1-c8'),
    'n5-080': ('genki-1-l5', 'minna-1-c8'),
    'n5-081': ('genki-1-l5', 'minna-1-c12'),
    'n5-082': ('genki-1-l5', 'minna-1-c12'),
    'n5-083': ('genki-1-l7', 'minna-1-c16'),
    # na-Adjective paradigm (Genki l5, Minna c8-c12)
    'n5-084': ('genki-1-l5', 'minna-1-c8'),
    'n5-085': ('genki-1-l5', 'minna-1-c8'),
    'n5-086': ('genki-1-l5', 'minna-1-c8'),
    'n5-087': ('genki-1-l5', 'minna-1-c12'),
    'n5-088': ('genki-1-l5', 'minna-1-c12'),
    'n5-089': ('genki-1-l7', 'minna-1-c16'),
    # Existence (arimasu / imasu)
    'n5-090': ('genki-1-l4', 'minna-1-c10'),
    'n5-091': ('genki-1-l4', 'minna-1-c10'),
    'n5-092': ('genki-1-l4', 'minna-1-c10'),
    'n5-093': ('genki-1-l4', 'minna-1-c10'),
    'n5-094': ('genki-1-l9', 'minna-1-c13'),
    # Comparisons + likes/dislikes/skills (Genki l5/l10, Minna c9/c12)
    'n5-095': ('genki-1-l10', 'minna-1-c12'),
    'n5-096': ('genki-1-l10', 'minna-1-c12'),
    'n5-097': ('genki-1-l10', 'minna-1-c12'),
    'n5-098': ('genki-1-l5', 'minna-1-c9'),
    'n5-099': ('genki-1-l5', 'minna-1-c9'),
    'n5-100': ('genki-1-l5', 'minna-1-c9'),
    # Want/can/skill
    'n5-101': ('genki-1-l11', 'minna-1-c13'),
    'n5-102': ('genki-1-l4', 'minna-1-c9'),
    'n5-103': ('genki-1-l11', 'minna-1-c18'),
    'n5-104': ('genki-1-l11', 'minna-1-c13'),
    'n5-105': ('genki-1-l11', 'minna-1-c13'),
    'n5-106': ('genki-1-l11', 'minna-1-c13'),
    # Verb-stem + ni iku/kuru
    'n5-107': ('genki-1-l11', 'minna-1-c13'),
    # Counters + time
    'n5-108': ('genki-1-l3', 'minna-1-c11'),
    'n5-109': ('genki-1-l3', 'minna-1-c11'),
    'n5-110': ('genki-1-l11', 'minna-1-c11'),
    'n5-111': ('genki-1-l1', 'minna-1-c4'),
    'n5-112': ('genki-1-l1', 'minna-1-c4'),
    'n5-113': ('genki-1-l1', 'minna-1-c4'),
    'n5-114': ('genki-1-l3', 'minna-1-c4'),
    'n5-115': ('genki-1-l3', 'minna-1-c4'),
    # Time adverbials + frequency
    'n5-116': ('genki-1-l3', 'minna-1-c4'),
    'n5-117': ('genki-1-l3', 'minna-1-c5'),
    'n5-118': ('genki-1-l4', 'minna-1-c8'),
    'n5-119': ('genki-1-l11', 'minna-1-c18'),
    'n5-120': ('genki-1-l11', 'minna-1-c19'),
    # Conjunctions
    'n5-121': ('genki-1-l3', 'minna-1-c8'),
    'n5-122': ('genki-1-l11', 'minna-1-c11'),
    'n5-123': ('genki-1-l5', 'minna-1-c8'),
    'n5-124': ('genki-1-l9', 'minna-1-c8'),
    'n5-125': ('genki-1-l8', 'minna-1-c8'),
    'n5-126': ('genki-1-l8', 'minna-1-c8'),
    'n5-127': ('genki-1-l9', 'minna-1-c8'),
    'n5-129': ('genki-1-l3', 'minna-1-c9'),
    # Give/receive (Genki l11, Minna c7+c24)
    'n5-130': ('genki-1-l11', 'minna-1-c7'),
    'n5-131': ('genki-1-l11', 'minna-1-c7'),
    'n5-132': ('genki-1-l11', 'minna-1-c7'),
    # Causal (Genki l8, Minna c8)
    'n5-133': ('genki-1-l8', 'minna-1-c9'),
    'n5-134': (None, 'minna-1-c9'),  # ので - late N5; not really in Genki I
    # Relative clauses + adjective+noun + N+の+N
    'n5-135': ('genki-1-l9', 'minna-1-c22'),
    'n5-136': ('genki-1-l5', 'minna-1-c8'),
    'n5-137': ('genki-1-l1', 'minna-1-c2'),
    # Decision/becoming
    'n5-142': ('genki-1-l10', 'minna-1-c20'),
    'n5-143': ('genki-1-l10', 'minna-1-c19'),
    # While doing
    'n5-144': (None, 'minna-1-c25'),  # late N5 borderline
    # Quotation (think/say)
    'n5-145': (None, 'minna-1-c21'),
    'n5-146': (None, 'minna-1-c21'),
    # Frequency adverbs + politeness phrases
    'n5-147': ('genki-1-l3', 'minna-1-c8'),
    'n5-148': ('genki-1-l8', 'minna-1-c8'),
    'n5-149': ('genki-1-l1', 'minna-1-c3'),
    'n5-150': ('genki-1-l11', 'minna-1-c14'),
    'n5-151': ('genki-1-l11', 'minna-1-c8'),
    'n5-152': ('genki-1-l1', 'minna-1-c1'),
    # Already / not yet (Genki l9, Minna c19)
    'n5-153': ('genki-1-l9', 'minna-1-c19'),
    'n5-154': ('genki-1-l9', 'minna-1-c19'),
    # Cross-references to other entries
    'n5-155': ('genki-1-l8', 'minna-1-c8'),
    'n5-156': ('genki-1-l4', 'minna-1-c4'),
    # でしょう / だろう (late N5 in Genki II / Minna II)
    'n5-157': (None, 'minna-2-c32'),
    'n5-158': (None, 'minna-2-c32'),
    'n5-159': ('genki-1-l4', 'minna-1-c4'),
    # まえに / あとで (Genki l11)
    'n5-160': ('genki-1-l11', 'minna-1-c19'),
    'n5-161': ('genki-1-l11', 'minna-1-c18'),
    'n5-162': ('genki-1-l11', 'minna-1-c18'),
    'n5-163': ('genki-1-l11', 'minna-1-c19'),
    # Honorific suffix + greetings
    'n5-164': ('genki-1-l1', 'minna-1-c1'),
    'n5-165': ('genki-1-l9', 'minna-1-c19'),
    'n5-166': ('genki-1-l1', 'minna-1-c1'),
    # んです / explanatory
    'n5-167': ('genki-1-l12', 'minna-1-c26'),
    # Tari-tari-suru (Genki l11)
    'n5-168': ('genki-1-l11', 'minna-1-c19'),
    # Past experience / advice / suggestion
    'n5-169': ('genki-1-l11', 'minna-1-c19'),
    'n5-170': (None, 'minna-1-c32'),
    'n5-171': (None, 'minna-1-c32'),
    # Must / dont have to (Genki l12)
    'n5-172': ('genki-1-l12', 'minna-1-c17'),
    'n5-173': ('genki-1-l12', 'minna-1-c17'),
    'n5-174': (None, 'minna-1-c17'),
    'n5-175': (None, 'minna-1-c17'),
    'n5-176': (None, 'minna-1-c17'),
    # Sugiru
    'n5-177': ('genki-1-l12', 'minna-1-c44'),
    # Tsumori (Genki l10/l12)
    'n5-178': ('genki-1-l10', 'minna-1-c20'),
    # Late N5 / borderline (mostly not in Genki I)
    'n5-179': (None, None),  # って - very casual; not in Genki I
    'n5-180': (None, 'minna-1-c14'),  # verb-stem + kata
    'n5-181': (None, None),  # naa - sentence-final exclamation; casual
    'n5-182': (None, None),  # plain + na = strong prohibition; very casual
    # Question-word + ka/mo compounds
    'n5-183': ('genki-1-l8', 'minna-1-c10'),
    'n5-184': ('genki-1-l8', 'minna-1-c10'),
    'n5-185': ('genki-1-l8', 'minna-1-c10'),
    'n5-186': ('genki-1-l8', 'minna-1-c10'),
    'n5-187': ('genki-1-l11', 'minna-1-c11'),
    # Verb-dictionary + koto ga dekimasu
    'n5-188': (None, 'minna-1-c18'),
}


def main():
    with GRAMMAR.open('r', encoding='utf-8') as f:
        data = json.load(f)

    patterns = data['patterns']
    by_id = {p['id']: p for p in patterns}

    appended = 0
    skipped = 0
    not_found = []
    for pid, (genki, minna) in MAPPING.items():
        p = by_id.get(pid)
        if p is None:
            not_found.append(pid)
            continue
        sources = list(p.get('sources') or [])
        # Check: do existing sources already contain a Genki / Minna entry?
        has_genki = any(s.startswith('genki-') for s in sources)
        has_minna = any(s.startswith('minna-') for s in sources)
        added_any = False
        # Insert at front to preserve textbook-priority ordering
        if genki and not has_genki:
            sources.insert(0, genki)
            added_any = True
        if minna and not has_minna:
            sources.insert(1 if added_any else 0, minna)
            added_any = True
        if added_any:
            p['sources'] = sources
            appended += 1
        else:
            skipped += 1

    print(f'Patterns updated with chapter-specific citations: {appended}')
    print(f'Patterns already complete (skipped): {skipped}')
    if not_found:
        print(f'IDs not found in grammar.json: {not_found}')

    with GRAMMAR.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Wrote: {GRAMMAR}')


if __name__ == '__main__':
    main()
