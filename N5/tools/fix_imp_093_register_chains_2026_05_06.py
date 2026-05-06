"""IMP-093 (round-7 carry-over → round-8 close-out, 2026-05-06):
register_chain_id cross-links on 6 N5-relevant keigo trios.

Each trio has 3 forms — plain, humble (謙譲), respectful (尊敬) — that
share a meaning. Cross-linking them helps Hindi-L1 learners (whose
politeness system is pronoun-based, not verb-morphology-based) see the
register chain as a unit.

The 6 trios:
  1. いる (be) ⇄ いらっしゃる (resp.) ⇄ おる (humb.)
  2. 食べる (eat) ⇄ 召し上がる (resp.) ⇄ いただく (humb.)
  3. 見る (see) ⇄ ご覧になる (resp.) ⇄ 拝見する (humb.)
  4. 行く/来る (go/come) ⇄ いらっしゃる (resp.) ⇄ 参る/伺う (humb.)
  5. 言う (say) ⇄ おっしゃる (resp.) ⇄ 申す (humb.)
  6. する (do) ⇄ なさる (resp.) ⇄ いたす (humb.)

Each entry gets:
  register_chain_id: '<chain-name>'
  register_chain_role: 'plain' | 'humble' | 'respectful'

Renderer can use these to surface a "see also" callout on the vocab
detail page. Match by reading-only since most vocab.json verb entries
store form==reading.

Idempotent.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
VF = ROOT / 'data' / 'vocab.json'

# trio_id -> [(reading, role), ...]
TRIOS = {
    'be':   [('いる', 'plain'), ('いらっしゃる', 'respectful'), ('おる', 'humble')],
    'eat':  [('たべる', 'plain'), ('めしあがる', 'respectful'), ('いただく', 'humble')],
    'see':  [('みる', 'plain'), ('ごらんになる', 'respectful'), ('はいけんする', 'humble')],
    'go':   [('いく', 'plain'), ('くる', 'plain'),
             ('いらっしゃる', 'respectful'),
             ('まいる', 'humble'), ('うかがう', 'humble')],
    'say':  [('いう', 'plain'), ('おっしゃる', 'respectful'), ('もうす', 'humble')],
    'do':   [('する', 'plain'), ('なさる', 'respectful'), ('いたす', 'humble')],
}


def main() -> int:
    data = json.loads(VF.read_text(encoding='utf-8'))

    # reading -> (chain_id, role)
    by_reading = {}
    for chain_id, members in TRIOS.items():
        for reading, role in members:
            # Note: いらっしゃる appears in both 'be' and 'go'; keep the
            # more-specific 'be' (the entry's primary semantic) — but if
            # vocab.json gloss says go/come, the 'go' chain wins. This is
            # rare; default to first-seen.
            if reading not in by_reading:
                by_reading[reading] = (chain_id, role)

    n_chain_added = 0
    n_role_added = 0
    for e in data.get('entries', []):
        reading = e.get('reading')
        if reading in by_reading:
            chain_id, role = by_reading[reading]
            if e.get('register_chain_id') != chain_id:
                e['register_chain_id'] = chain_id
                n_chain_added += 1
            if e.get('register_chain_role') != role:
                e['register_chain_role'] = role
                n_role_added += 1

    VF.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    total = len(data['entries'])
    nC = sum(1 for e in data['entries'] if e.get('register_chain_id'))
    print(f'[IMP-093] register_chain_id cross-links')
    print(f'  chain_id writes:   {n_chain_added}')
    print(f'  role writes:       {n_role_added}')
    print(f'  total entries with register_chain_id: {nC}/{total}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
