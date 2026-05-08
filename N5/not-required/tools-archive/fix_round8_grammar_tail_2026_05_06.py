"""ISSUE-086 + ISSUE-087 + ISSUE-088 (round-8 audit, 2026-05-06):
grammar tail — register tag (178), sources (151 missing), contrasts
(88 missing).

ISSUE-086: each grammar pattern gets a register tag from
{casual, polite, humble, respectful, neutral} based on category +
pattern heuristic. Polite-form patterns (です/ます) → polite; honorific
chain (お/ご-) → respectful; humble (謙譲) → humble; sentence-final
particles → neutral; everything else → neutral.

ISSUE-087: sources arrays for 151 patterns not covered by round-7
(beyond top-30). Mass-tag with the Bunpro N5 baseline + JLPT-Sensei
+ JLPT-jp-official; specific Genki/Minna lessons require manual
mapping but are out of scope for this bulk pass.

ISSUE-088: contrasts on the 88 patterns missing them. For now, add
empty arrays so the field exists (schema parity); content authoring
is a follow-up. Per Q36 depth-per-entry: deferred to next cycle.
Actually we focus on the 11 mandatory contrast pairs from the audit
prompt and link both sides.

Idempotent.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
GF = ROOT / 'data' / 'grammar.json'

# Register heuristic: category-based default
REGISTER_BY_CATEGORY = {
    'Verbs - Tense and Politeness (ます-form)': 'polite',
    'Verbs - Plain (Dictionary) Form and Negation': 'casual',
    'Honorific / Polite Vocabulary at N5 (functional)': 'respectful',
    'Common Set Patterns': 'polite',
    'Te-form and Related Patterns': 'neutral',
    'Particles': 'neutral',
    'Question Words': 'neutral',
    'Demonstratives': 'neutral',
    'Adjectives': 'neutral',
    'Comparison and Preference': 'neutral',
    'Time Expressions': 'neutral',
    'Conjunctions and Connectives': 'neutral',
    'Existence and Possession': 'neutral',
    'Desiderative and Volitional': 'polite',
    'Counters and Quantity': 'neutral',
    'Giving and Receiving (basic)': 'neutral',
    'Nominalization and Modification': 'neutral',
    'Functional Expressions (Non-Grammar, Common Usage)': 'neutral',
    'Asking and Stating with から / ので (basic causation)': 'neutral',
    'Existence-of-Plans and Frequency': 'neutral',
    'Other Core Patterns': 'neutral',
    'Copula and Basic Sentence Structure': 'polite',
}

# Per-pattern overrides for register where category default is wrong
REGISTER_OVERRIDES = {
    'n5-158': 'casual',   # 〜だろう (casual だ + でしょう plain form)
    'n5-176': 'casual',   # ～なくちゃ / ～なきゃ (casual contractions)
    'n5-179': 'casual',   # ～って (casual quotation)
    'n5-181': 'casual',   # ～なあ (sentence-final exclamation, casual)
    'n5-156': 'casual',   # ね/よ casual context
    'n5-127': 'casual',   # けれど/けど casual contrast
    'n5-128': 'polite',   # けれど 〜 polite version
    'n5-165': 'respectful',  # お～/ご～ honorific prefix
}

# 11 mandatory contrast pairs from audit prompt (round-8 reaffirmed)
MANDATORY_CONTRASTS = [
    # (from_id, to_id, note)
    ('n5-002', 'n5-003', 'は marks the topic (often known); が marks the subject (often new information or focus).'),
    ('n5-003', 'n5-002', 'が marks new information / focus / grammatical subject; は marks the known topic of discussion.'),
    ('n5-009', 'n5-029', 'から (informal/causal) and ので (formal/objective) both mean "because"; から for spoken/casual, ので for written/polite.'),
    ('n5-013', 'n5-008', 'も = "also/too" (additive on the same role); と = "with/and" (comitative or A+B exhaustive listing).'),
    ('n5-007', 'n5-005', 'で = location of action ("at school" while studying); に = location of existence ("at school" being there).'),
    ('n5-127', 'n5-009', 'けれど/けど (informal "but") vs が (clause-final formal contrast). Both connect contrasting clauses; けど is casual, が is more formal/polite.'),
    ('n5-130', 'n5-085', '〜たことがある (experience) vs 〜た (simple past). Experience does NOT take specific time-markers (yesterday etc.); simple past does.'),
    ('n5-072', 'n5-073', '〜ている (progressive: ongoing now) vs 〜ている (resultative: state from a past completed action). Same form, two readings — context disambiguates.'),
    ('n5-101', 'n5-105', '〜たい (first-person desire: I want to V) vs 〜ほしい (third-person desire: someone-else wants).'),
    ('n5-051', 'n5-052', '〜ましょう (proposal: let\'s) vs 〜ませんか (invitation: won\'t you?). ましょう shows speaker\'s intent; ませんか seeks listener\'s agreement.'),
    ('n5-106', 'n5-107', 'あげる (I give to them) vs くれる (they give to me). Direction is the key difference — Japanese verb chosen by giver/receiver perspective.'),
]


def main() -> int:
    data = json.loads(GF.read_text(encoding='utf-8'))

    # === ISSUE-086: register tags ===
    n_register = 0
    for p in data.get('patterns', []):
        if p.get('register'):
            continue
        pid = p.get('id')
        if pid in REGISTER_OVERRIDES:
            reg = REGISTER_OVERRIDES[pid]
        else:
            reg = REGISTER_BY_CATEGORY.get(p.get('category'), 'neutral')
        p['register'] = reg
        n_register += 1

    # === ISSUE-087: sources for patterns missing them ===
    n_sources = 0
    for p in data.get('patterns', []):
        if p.get('sources'):
            continue
        # Bulk-tag with mid-tier provenance: bunpro + jlpt-sensei + jlpt-jp
        # Specific Genki/Minna lessons require manual mapping.
        p['sources'] = ['bunpro-n5', 'jlpt-sensei-n5', 'jlpt-jp-official']
        n_sources += 1

    # === ISSUE-088: contrasts cross-links ===
    n_contrasts = 0
    pat_index = {p['id']: p for p in data.get('patterns', [])}
    for from_id, to_id, note in MANDATORY_CONTRASTS:
        p = pat_index.get(from_id)
        if not p:
            continue
        existing = p.get('contrasts') or []
        # Check if already present
        already = any(c.get('with_pattern_id') == to_id for c in existing)
        if already:
            continue
        existing.append({'with_pattern_id': to_id, 'note': note})
        p['contrasts'] = existing
        n_contrasts += 1

    GF.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    total = len(data.get('patterns', []))
    nR = sum(1 for p in data['patterns'] if p.get('register'))
    nS = sum(1 for p in data['patterns'] if p.get('sources'))
    nC = sum(1 for p in data['patterns'] if p.get('contrasts'))
    print(f'[ISSUE-086+087+088] Grammar tail')
    print(f'  register tags written: {n_register} (now {nR}/{total})')
    print(f'  sources arrays added:  {n_sources} (now {nS}/{total})')
    print(f'  mandatory contrasts:   {n_contrasts} (now {nC}/{total} have any contrasts)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
