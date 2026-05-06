"""ISSUE-102 (round-9): grammar contrasts on the 11 mandatory N5 clusters.

Audit found 95/178 patterns have ≥1 contrast. The remaining 83 either
don't need a contrast (single-pattern concepts) OR need cross-link to
their sibling in one of the 11 mandatory clusters spelled out in the
audit prompt:

  1. は vs が               (n5-002 ↔ n5-003 ✓; n5-126 floats)
  2. から vs ので            (n5-133 ↔ n5-134; n5-009 ✓)
  3. も vs と               (n5-008 ↔ n5-013 — n5-008 had None bug)
  4. で vs に               (n5-005, n5-006, n5-007)
  5. けど/けれど vs が         (n5-127 ✓)
  6. 〜たことがある vs 〜た       (n5-169 ↔ n5-067)
  7. 〜ている progressive vs resultative (n5-072 ↔ n5-073 ✓)
  8. て-form chain vs Verb-ています (n5-069 ↔ n5-072)
  9. 〜たい vs 〜ほしい         (n5-101 ↔ n5-104; n5-106)
 10. 〜ましょう vs 〜ませんか    (n5-062 ↔ n5-064 ✓)
 11. あげる/くれる/もらう trio  (n5-130 / n5-131 / n5-132)

Also fixes 3 contrast data bugs: n5-008 had {'with_pattern_id': None}
referring to や (no N5 pattern for や exists, so the contrast is moved
to a note-only entry); n5-054 same pattern with いくつ/counter; n5-167
uses a non-canonical key shape ({'with': ...} instead of
{'with_pattern_id': ...}) — left as-is since it's a contrast against a
non-pattern (plain copula vs explanation copula).

Idempotent: skips contrasts already cross-linked.
"""
from __future__ import annotations
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

GRAMMAR = Path(__file__).parent.parent / 'data' / 'grammar.json'

# Each entry: (pattern_id, contrast_with_id, note)
# The script will add the cross-link in BOTH directions if the partner
# pattern exists and the contrast isn't already there.
CONTRASTS_TO_ADD = [
    # 1. は vs が — n5-126 (existential/possession が) needs link back to n5-002 (topic は)
    ('n5-126', 'n5-002', 'は marks the topic of conversation; が marks subject (often the new/focused element). With existential verbs ある / いる, が marks what exists.'),
    # 2. から vs ので at sentence level
    ('n5-133', 'n5-134', '〜から (sentence-final causal) is direct / casual. 〜ので is softer / more polite — preferred when the reason is something the listener should sympathize with.'),
    # 3. も vs と (already has partial cross-link from n5-013; this asserts symmetry)
    ('n5-008', 'n5-013', 'と pairs items exhaustively (A and B, full stop). も adds (A も B も = both A and B as well). Distinct functions even though both can join nouns.'),
    # 4. で vs に — n5-007 (で action location) needs link to n5-006 (に direction) to clarify three-way distinction
    ('n5-007', 'n5-006', 'で marks the location where an action takes place; に marks the destination/direction of movement. Pair this with the n5-005 contrast (に for existence location).'),
    # 6. 〜たことがある vs 〜た past
    ('n5-169', 'n5-067', '〜た is plain past ("I did it"). 〜たことがある is experiential ("I have the experience of doing it") — used for life experience, not specific time-marked actions. Adding "yesterday" to 〜たことがある is ungrammatical.'),
    # 8. て-form chain vs Verb-ています continuous
    ('n5-069', 'n5-072', 'Verb-て alone chains successive actions ("did X and then Y"). Verb-ています adds います to express progressive ("doing X right now") or resultative ("X has been done; the state continues").'),
    # 9. 〜たい vs 〜ほしい
    ('n5-104', 'n5-101', '〜たい expresses the speaker\'s own desire to perform an action ("I want to eat"). 〜が ほしい expresses desire for an object/state ("I want a book"). Different parts of speech: たい attaches to verb stems; ほしい attaches to nouns + が.'),
    # 11. Giving verbs trio
    ('n5-130', 'n5-131', 'あげる = "give" from in-group to out-group or speaker → others. もらう = "receive" — the reverse direction, marked with に or から for the giver. Use あげる when speaker/in-group gives, もらう when speaker/in-group receives.'),
    ('n5-130', 'n5-132', 'あげる = "give to others" (out-group). くれる = "give to me / my in-group" — same action, different direction relative to the speaker. Choose based on who receives.'),
    ('n5-131', 'n5-132', 'もらう = "receive" (passive POV from receiver). くれる = "give to me" (active POV from giver). Both describe the same transfer; the choice signals whose perspective the speaker takes.'),
]

# Existing contrast bugs to repair (None pattern_id). Convert to notes-only entry.
BUGS_TO_REPAIR = {
    'n5-008': {
        'old_predicate': lambda c: isinstance(c, dict) and c.get('with_pattern_id') is None,
        'note': 'と (exhaustive: A and B, full stop) vs や (non-exhaustive: A, B, etc., among others). や is often paired with など. Note: や does not have its own grammar entry in this corpus.',
    },
    'n5-054': {
        'old_predicate': lambda c: isinstance(c, dict) and c.get('with_pattern_id') is None,
        'note': 'いくつ = "how many" (native counter). For specific counters use なん + counter (なんにん, なんまい). Note: counter-specific patterns live in the counters section.',
    },
}


def has_contrast(p: dict, partner_id: str) -> bool:
    for c in p.get('contrasts') or []:
        if isinstance(c, dict):
            if c.get('with_pattern_id') == partner_id:
                return True
        elif c == partner_id:
            return True
    return False


def main() -> int:
    doc = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    patterns = doc['patterns']
    by_id = {p['id']: p for p in patterns}

    n_added = 0
    n_skipped = 0
    n_bugs_fixed = 0

    # Phase 1: Add cross-links (both directions)
    for src_id, dst_id, note in CONTRASTS_TO_ADD:
        if src_id not in by_id or dst_id not in by_id:
            print(f'WARN: pattern not found: {src_id} or {dst_id}')
            continue
        # src → dst
        src = by_id[src_id]
        if has_contrast(src, dst_id):
            n_skipped += 1
        else:
            src.setdefault('contrasts', []).append({
                'with_pattern_id': dst_id,
                'note': note,
            })
            n_added += 1
        # dst → src (mirror with same note)
        dst = by_id[dst_id]
        if has_contrast(dst, src_id):
            n_skipped += 1
        else:
            dst.setdefault('contrasts', []).append({
                'with_pattern_id': src_id,
                'note': note,
            })
            n_added += 1

    # Phase 2: Repair contrast bugs
    for pid, repair in BUGS_TO_REPAIR.items():
        p = by_id.get(pid)
        if not p: continue
        contrasts = p.get('contrasts') or []
        new_contrasts = []
        for c in contrasts:
            if repair['old_predicate'](c):
                # Replace with note-only entry (no with_pattern_id)
                new_contrasts.append({'note': repair['note']})
                n_bugs_fixed += 1
            else:
                new_contrasts.append(c)
        p['contrasts'] = new_contrasts

    GRAMMAR.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    # Verify
    doc2 = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    have_contrast = sum(1 for p in doc2['patterns'] if p.get('contrasts'))
    print(f'Cross-links added: {n_added}')
    print(f'Skipped (already linked): {n_skipped}')
    print(f'Buggy contrasts repaired: {n_bugs_fixed}')
    print(f'\nPost-fix: {have_contrast}/{len(doc2["patterns"])} patterns have ≥1 contrast.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
