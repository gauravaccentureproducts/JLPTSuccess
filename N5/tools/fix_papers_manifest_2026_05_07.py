"""IMP-118 + IMP-120 + ISSUE-095: Manifest updates for JLPT-shape mock papers.

Three related items, all data-side manifest changes (no UI code).
The UI-rendering items (IMP-115, IMP-121) are tracked separately.

IMP-120 — Per-paper expectedDurationMin field.
  Adds an `expectedDurationMin` integer to each paper card in manifest.
  Derivation:
    moji      : 43 sec/Q (35Q-in-25min real-exam pace)
    goi       : 43 sec/Q
    bunpou    : 94 sec/Q (32Q-in-50min real-exam pace)
    dokkai    : 94 sec/Q
    chokai    : 75 sec/Q (24Q-in-30min real-exam pace)
  Rounded up to nearest minute.

IMP-118 — Listening 24-Q chokai virtual paper.
  Adds a `chokai` category to manifest containing virtual papers
  built by sampling 7×M1 + 6×M2 + 5×M3 + 6×M4 from the 47-item
  listening pool (data/listening.json). 1 virtual paper for now;
  manifest schema accommodates more if/when the listening pool grows.

ISSUE-095 — Virtual combined-section papers (real JLPT shape).
  Adds a `combined_sections` block to manifest enumerating:
    - 言語知識 (moji+goi pair-N): 30Q / 25 min
    - 言語知識・読解 (bunpou+dokkai pair-N): 31Q / 50 min
    - 聴解 (chokai virtual): 24Q / 30 min
  Each is a virtual aggregation referring to the existing per-mondai
  papers — no new content, just manifest-level grouping the UI can
  render as a "Full Mock Test Paper N" tile.

Idempotent.
"""
from __future__ import annotations
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / 'data' / 'papers' / 'manifest.json'
LISTENING = ROOT / 'data' / 'listening.json'

PER_Q_SECONDS = {
    'moji': 43,
    'goi': 43,
    'bunpou': 94,
    'dokkai': 94,
    'chokai': 75,
}


def estimate_duration_min(category_id: str, q_count: int) -> int:
    """Return expectedDurationMin (ceiling-rounded) for a paper."""
    sec = PER_Q_SECONDS.get(category_id, 60) * q_count
    return math.ceil(sec / 60)


def main():
    with MANIFEST.open('r', encoding='utf-8') as f:
        manifest = json.load(f)

    changes = 0

    # === IMP-120: per-paper expectedDurationMin ===
    for cat in manifest['categories']:
        cid = cat['id']
        for p in cat.get('papers', []):
            qc = p.get('questionCount', 15)
            existing = p.get('expectedDurationMin')
            new_dur = estimate_duration_min(cid, qc)
            if existing != new_dur:
                p['expectedDurationMin'] = new_dur
                changes += 1
    print(f'IMP-120: per-paper expectedDurationMin set on {changes} papers')

    # === IMP-118: chokai virtual paper category ===
    L = json.loads(LISTENING.read_text(encoding='utf-8'))
    items = L['items']
    by_mondai = {1: [], 2: [], 3: [], 4: []}
    for it in items:
        m = it.get('mondai')
        if m in by_mondai:
            by_mondai[m].append(it['id'])

    print(f'Listening pool: M1={len(by_mondai[1])}, M2={len(by_mondai[2])}, '
          f'M3={len(by_mondai[3])}, M4={len(by_mondai[4])}')

    # Build virtual chokai paper-1: 7 M1 + 6 M2 + 5 M3 + 6 M4 = 24
    needed = {1: 7, 2: 6, 3: 5, 4: 6}
    can_build = all(len(by_mondai[m]) >= needed[m] for m in needed)
    chokai_already_present = any(c['id'] == 'chokai' for c in manifest['categories'])
    if not chokai_already_present and can_build:
        # Pick first N items per mondai (deterministic; in practice the UI
        # layer would shuffle for each session)
        virtual_paper_items = []
        for m in (1, 2, 3, 4):
            virtual_paper_items.extend(by_mondai[m][:needed[m]])

        chokai_cat = {
            'id': 'chokai',
            'label': 'Chokai',
            'label_ja': '聴解',
            'description': 'Listening — virtual paper aggregating 24-Q from 47-item pool',
            'paperCount': 1,
            'questionCount': 24,
            'papers': [
                {
                    'id': 'chokai-1',
                    'paperNumber': 1,
                    'name': '聴解 Virtual Paper 1',
                    'questionCount': 24,
                    'expectedDurationMin': estimate_duration_min('chokai', 24),
                    'mondai_breakdown': {'M1': 7, 'M2': 6, 'M3': 5, 'M4': 6},
                    'source_listening_ids': virtual_paper_items,
                    'note': 'Virtual paper — sampled from listening pool. Real JLPT N5 Chokai = 24Q in 30 min.',
                },
            ],
        }
        manifest['categories'].append(chokai_cat)
        changes += 1
        print(f'IMP-118: added chokai virtual paper category with 1 paper (24 questions)')
    else:
        print(f'IMP-118: chokai already present OR pool insufficient (have M1={len(by_mondai[1])}/7, M2={len(by_mondai[2])}/6, M3={len(by_mondai[3])}/5, M4={len(by_mondai[4])}/6)')

    # === ISSUE-095: combined_sections block ===
    # Lists virtual aggregations. Real JLPT N5 shape:
    #   Section 1 言語知識(文字・語彙) = moji+goi = 35Q in 25min
    #   Section 2 言語知識(文法)・読解 = bunpou+dokkai = 32Q in 50min
    #   Section 3 聴解 = chokai = 24Q in 30min
    # Build paired aggregations for paper-1 .. paper-7 plus a chokai-only entry
    if 'combined_sections' not in manifest:
        combined = []
        for n in range(1, 8):  # paper-1 through paper-7
            combined.append({
                'id': f'genngo-chishiki-moji-goi-{n}',
                'paperNumber': n,
                'name_ja': f'言語知識（文字・語彙）Paper {n}',
                'name_en': f'Language Knowledge (Moji+Goi) Paper {n}',
                'sectionLabel': '言語知識（文字・語彙）',
                'questionCount': 30,
                'expectedDurationMin': 25,
                'componentPapers': [f'moji-{n}', f'goi-{n}'],
                'note': 'Real JLPT N5 Section 1: 35Q in 25min. App ships 30Q via two 15Q half-papers.',
            })
            combined.append({
                'id': f'genngo-chishiki-bunpou-dokkai-{n}',
                'paperNumber': n,
                'name_ja': f'言語知識（文法）・読解 Paper {n}',
                'name_en': f'Language Knowledge (Bunpou)+Reading Paper {n}',
                'sectionLabel': '言語知識（文法）・読解',
                'questionCount': 31,
                'expectedDurationMin': 50,
                'componentPapers': [f'bunpou-{n}', f'dokkai-{n}'],
                'note': 'Real JLPT N5 Section 2: 32Q in 50min. App ships 31Q (15+16).',
            })
        # Chokai-only entry (refers to virtual chokai paper)
        combined.append({
            'id': 'chokai-1-virtual',
            'paperNumber': 1,
            'name_ja': '聴解 Virtual Paper 1',
            'name_en': 'Chokai (Listening) Virtual Paper 1',
            'sectionLabel': '聴解',
            'questionCount': 24,
            'expectedDurationMin': 30,
            'componentPapers': ['chokai-1'],
            'note': 'Virtual paper sampled from 47-item listening pool. Real JLPT N5 Chokai = 24Q in 30min.',
        })
        # Full-paper aggregations (Sections 1+2+3 = real JLPT shape)
        full_papers = []
        for n in range(1, 8):
            full_papers.append({
                'id': f'full-mock-{n}',
                'paperNumber': n,
                'name_ja': f'JLPT N5 模擬試験 Paper {n}',
                'name_en': f'JLPT N5 Full Mock Paper {n}',
                'totalQuestions': 30 + 31 + 24,  # 85
                'totalDurationMin': 25 + 50 + 30,  # 105
                'sections': [
                    f'genngo-chishiki-moji-goi-{n}',
                    f'genngo-chishiki-bunpou-dokkai-{n}',
                    'chokai-1-virtual',
                ],
                'note': 'Real-exam-shape mock test. Real JLPT N5 = 85Q (35+32+24=91 actually, app ships 85 via 30+31+24).',
            })

        manifest['combined_sections'] = combined
        manifest['full_mock_papers'] = full_papers
        changes += 1
        print(f'ISSUE-095: added combined_sections ({len(combined)} entries) + full_mock_papers ({len(full_papers)} entries)')
    else:
        print('ISSUE-095: combined_sections already present (skipping)')

    # Update top-level totals
    if 'chokai' in [c['id'] for c in manifest['categories']]:
        new_total_papers = sum(c['paperCount'] for c in manifest['categories'])
        new_total_qs = sum(c['questionCount'] for c in manifest['categories'])
        if manifest.get('totalPapers') != new_total_papers:
            manifest['totalPapers'] = new_total_papers
        if manifest.get('totalQuestions') != new_total_qs:
            manifest['totalQuestions'] = new_total_qs

    with MANIFEST.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(manifest, f, ensure_ascii=False, indent=2)
    print(f'\nWrote: {MANIFEST}')
    print(f'Total changes: {changes}')


if __name__ == '__main__':
    main()
