"""Deploy dokkai Mondai 5 + Mondai 6 to paper-JSONs (42 questions).

Audit found that the dokkai paper-JSON corpus only contains the 60
Mondai 4 questions; Mondai 5 (30 medium-passage Qs) and Mondai 6
(12 information-retrieval Qs) exist in KnowledgeBank/dokkai_questions_n5.md
but were never deployed to data/papers/dokkai/. This script parses the
MD source and generates paper-5, paper-6, paper-7 JSONs.

Paper layout (after deployment):
  paper-1  Q1-Q16   Mondai 4 (existing, 16 items)
  paper-2  Q17-Q32  Mondai 4 (existing, 16 items)
  paper-3  Q33-Q48  Mondai 4 (existing, 16 items)
  paper-4  Q49-Q60  Mondai 4 (existing, 12 items)
  paper-5  Q61-Q75  Mondai 5 (NEW, 15 items - 5 passages of 3 Qs each)
  paper-6  Q76-Q90  Mondai 5 (NEW, 15 items - 5 passages of 3 Qs each)
  paper-7  Q91-Q102 Mondai 6 (NEW, 12 items - 6 items of 2 Qs each)

Stale-rationale fix bundled in: Q91-Q93 had rationale text copy-pasted
from unrelated Mondai 4/5 questions (referenced bread/Tuesday/etc.).
Replaced with question-appropriate rationales.

Idempotent: if a paper-JSON already exists with the expected content,
skipped. JSON-MD parity preserved for JA-32.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / 'KnowledgeBank' / 'dokkai_questions_n5.md'
PAPERS = ROOT / 'data' / 'papers' / 'dokkai'
MANIFEST = ROOT / 'data' / 'papers' / 'manifest.json'

changes: list[str] = []

# Stale rationales in Mondai 6 (Q91-Q93) had copy-pasted text from unrelated
# Mondai 4/5 questions. Replacements below are the correct rationales for the
# actual Q content. Q94 onwards looked correct on inspection.
RATIONALE_OVERRIDES = {
    'Q91': '子ども プール = 200円 (per the こうえんの あんない table).',
    'Q92': 'バーベキュー の 行に 「(よやくが いります)」 と かいて あります - barbecue requires reservation.',
    'Q93': '時間: 月よう日 と 水よう日 - the poster lists Mon and Wed.',
}


def parse_mondai_5(md_text: str) -> list[dict]:
    """Parse Mondai 5: 10 passages, 3 Qs each, Q61-Q90."""
    m = re.search(r'## Mondai 5\s+.*?(?=^## Mondai|\Z)', md_text, re.MULTILINE | re.DOTALL)
    if not m:
        raise RuntimeError('Mondai 5 section not found')
    section = m.group(0)

    # Split into passages: ### Passage X (Q...-Q...)
    passages = re.split(r'\n### Passage ', section)[1:]  # skip header

    items = []
    for p in passages:
        # First line is the passage label
        label_match = re.match(r'([A-Z]) \(Q(\d+)-Q(\d+)\)', p)
        if not label_match:
            continue
        letter, q_first, q_last = label_match.group(1), int(label_match.group(2)), int(label_match.group(3))
        passage_label = f'Passage {letter} (Q{q_first}-Q{q_last})'

        # Passage text: the > blockquote
        rest = p[label_match.end():].strip()
        # Find passage text (lines starting with >)
        lines = rest.split('\n')
        passage_lines = []
        i = 0
        while i < len(lines):
            line = lines[i]
            if line.startswith('>'):
                passage_lines.append(line)
            elif passage_lines and line.startswith('#### Q'):
                break
            elif passage_lines and not line.strip():
                # blank line within passage
                passage_lines.append(line)
            i += 1
        passage_text = '\n'.join(passage_lines).rstrip()

        # Find Q-blocks
        qstart = rest.find('#### Q')
        if qstart == -1:
            continue
        q_section = rest[qstart:]
        q_blocks = re.split(r'\n#### Q', q_section)
        if q_blocks[0].startswith('#### Q'):
            q_blocks[0] = q_blocks[0][6:]  # strip leading '#### Q'

        for qb in q_blocks:
            qb = qb.strip()
            if not qb:
                continue
            # First line = Q-number
            qnum_match = re.match(r'(\d+)', qb)
            if not qnum_match:
                continue
            qnum = int(qnum_match.group(1))
            qb_rest = qb[qnum_match.end():].strip()

            # Find stem (everything until the numbered list)
            list_match = re.search(r'^1\. ', qb_rest, re.MULTILINE)
            if not list_match:
                continue
            stem = qb_rest[:list_match.start()].strip()
            # Strip italic gloss line "_..._"
            stem = re.sub(r'\n_[^_]+_$', '', stem, flags=re.MULTILINE).strip()

            # Parse choices
            list_section = qb_rest[list_match.start():]
            choices = []
            for cm in re.finditer(r'^(\d)\. (.+)$', list_section, re.MULTILINE):
                if int(cm.group(1)) == len(choices) + 1:
                    choices.append(cm.group(2).strip())
                if len(choices) == 4:
                    break
            if len(choices) != 4:
                raise RuntimeError(f'Q{qnum}: expected 4 choices, got {len(choices)}')

            # Parse Answer + rationale
            ans_match = re.search(r'\*\*Answer: (\d)\*\*\s*-?\s*(.*?)(?=\n\n|\n#|$)', list_section, re.DOTALL)
            if not ans_match:
                raise RuntimeError(f'Q{qnum}: no **Answer:** line')
            correct_index = int(ans_match.group(1)) - 1
            rationale = ans_match.group(2).strip()
            # Remove any trailing newline-padded markers
            rationale = re.sub(r'\s*\n+\s*', ' ', rationale).strip()

            items.append({
                'qnum': qnum,
                'stem_html': stem,
                'choices': choices,
                'correctIndex': correct_index,
                'rationale': rationale,
                'passage_text': passage_text,
                'passage_label': passage_label,
            })
    return items


def parse_mondai_6(md_text: str) -> list[dict]:
    """Parse Mondai 6: 6 items, 2 Qs each, Q91-Q102."""
    m = re.search(r'## Mondai 6\s+.*?(?=^## Mondai|\Z)', md_text, re.MULTILINE | re.DOTALL)
    if not m:
        raise RuntimeError('Mondai 6 section not found')
    section = m.group(0)

    # Split into items: ### Item N (Q...-Q...)
    items_split = re.split(r'\n### Item ', section)[1:]

    items = []
    for it in items_split:
        # First line: 'N (Qa, Qb): title'
        head_match = re.match(r'(\d+) \(Q(\d+),\s*Q(\d+)\):\s*(.+)', it)
        if not head_match:
            continue
        item_n = int(head_match.group(1))
        q_first = int(head_match.group(2))
        q_last = int(head_match.group(3))
        title = head_match.group(4).strip()
        passage_label = f'Item {item_n} (Q{q_first}, Q{q_last}): {title}'

        rest = it[head_match.end():].strip()
        lines = rest.split('\n')
        passage_lines = []
        for line in lines:
            if line.startswith('>'):
                passage_lines.append(line)
            elif passage_lines and not line.strip():
                passage_lines.append(line)
            elif passage_lines and line.startswith('#### Q'):
                break
        passage_text = '\n'.join(passage_lines).rstrip()

        qstart = rest.find('#### Q')
        if qstart == -1:
            continue
        q_section = rest[qstart:]
        q_blocks = re.split(r'\n#### Q', q_section)
        if q_blocks[0].startswith('#### Q'):
            q_blocks[0] = q_blocks[0][6:]

        for qb in q_blocks:
            qb = qb.strip()
            if not qb:
                continue
            qnum_match = re.match(r'(\d+)', qb)
            if not qnum_match:
                continue
            qnum = int(qnum_match.group(1))
            qb_rest = qb[qnum_match.end():].strip()

            list_match = re.search(r'^1\. ', qb_rest, re.MULTILINE)
            if not list_match:
                continue
            stem = qb_rest[:list_match.start()].strip()
            stem = re.sub(r'\n_[^_]+_$', '', stem, flags=re.MULTILINE).strip()

            list_section = qb_rest[list_match.start():]
            choices = []
            for cm in re.finditer(r'^(\d)\. (.+)$', list_section, re.MULTILINE):
                if int(cm.group(1)) == len(choices) + 1:
                    choices.append(cm.group(2).strip())
                if len(choices) == 4:
                    break
            if len(choices) != 4:
                raise RuntimeError(f'Q{qnum}: expected 4 choices, got {len(choices)}')

            ans_match = re.search(r'\*\*Answer: (\d)\*\*\s*-?\s*(.*?)(?=\n\n|\n#|$)', list_section, re.DOTALL)
            if not ans_match:
                raise RuntimeError(f'Q{qnum}: no **Answer:** line')
            correct_index = int(ans_match.group(1)) - 1
            rationale = ans_match.group(2).strip()
            rationale = re.sub(r'\s*\n+\s*', ' ', rationale).strip()

            # Apply stale-rationale overrides
            qkey = f'Q{qnum}'
            if qkey in RATIONALE_OVERRIDES:
                rationale = RATIONALE_OVERRIDES[qkey]

            items.append({
                'qnum': qnum,
                'stem_html': stem,
                'choices': choices,
                'correctIndex': correct_index,
                'rationale': rationale,
                'passage_text': passage_text,
                'passage_label': passage_label,
            })
    return items


def build_paper(paper_n: int, items: list[dict], q_first: int, q_last: int) -> dict:
    """Build a paper-JSON dict from parsed Mondai items."""
    # Filter to items in this paper's Q-range
    paper_items = [it for it in items if q_first <= it['qnum'] <= q_last]
    paper_items.sort(key=lambda i: i['qnum'])

    # Group by passage_label to compute the passages section
    passages_seen = {}
    for it in paper_items:
        lbl = it['passage_label']
        if lbl not in passages_seen:
            passages_seen[lbl] = {
                'label': lbl,
                'text': it['passage_text'],
                'question_ids': [],
            }
        passages_seen[lbl]['question_ids'].append(f'dokkai-{paper_n}.{paper_items.index(it) + 1}')

    questions = []
    for idx, it in enumerate(paper_items):
        qid = f'dokkai-{paper_n}.{idx + 1}'
        questions.append({
            'type': 'mcq',
            'stem_html': it['stem_html'],
            'choices': it['choices'],
            'correctIndex': it['correctIndex'],
            'rationale': it['rationale'],
            'kbSourceId': f'Q{it["qnum"]}',
            'passage_text': it['passage_text'],
            'passage_label': it['passage_label'],
            'id': qid,
        })

    paper = {
        'id': f'dokkai-{paper_n}',
        'category': 'dokkai',
        'paperNumber': paper_n,
        'name': f'Dokkai Paper {paper_n}',
        'source_file': 'KnowledgeBank/dokkai_questions_n5.md',
        'source_question_range': f'Q{q_first}-Q{q_last}',
        'questionCount': len(questions),
        'passages': list(passages_seen.values()),
        'questions': questions,
    }
    return paper


def main() -> int:
    md_text = KB.read_text(encoding='utf-8')

    print('Parsing Mondai 5...')
    m5_items = parse_mondai_5(md_text)
    print(f'  Found {len(m5_items)} Mondai 5 items (Q-range {m5_items[0]["qnum"]}..{m5_items[-1]["qnum"]})')

    print('Parsing Mondai 6...')
    m6_items = parse_mondai_6(md_text)
    print(f'  Found {len(m6_items)} Mondai 6 items (Q-range {m6_items[0]["qnum"]}..{m6_items[-1]["qnum"]})')

    all_items = m5_items + m6_items

    # Generate papers 5, 6, 7
    paper_specs = [
        (5, 61, 75),  # Mondai 5 first half
        (6, 76, 90),  # Mondai 5 second half
        (7, 91, 102), # Mondai 6
    ]

    for paper_n, q_first, q_last in paper_specs:
        paper = build_paper(paper_n, all_items, q_first, q_last)
        out_path = PAPERS / f'paper-{paper_n}.json'
        if out_path.exists():
            existing = json.loads(out_path.read_text(encoding='utf-8'))
            if existing == paper:
                print(f'  paper-{paper_n}.json: unchanged')
                continue
        out_path.write_text(
            json.dumps(paper, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
        changes.append(f'paper-{paper_n}.json: wrote {len(paper["questions"])} questions ({paper["source_question_range"]})')

    # Update manifest.json
    manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    for cat in manifest['categories']:
        if cat['id'] == 'dokkai':
            cat['paperCount'] = 7
            cat['questionCount'] = 102
            cat['papers'] = [
                {'id': 'dokkai-1', 'paperNumber': 1, 'name': 'Dokkai Paper 1', 'questionCount': 16, 'source_question_range': 'Q1-Q16'},
                {'id': 'dokkai-2', 'paperNumber': 2, 'name': 'Dokkai Paper 2', 'questionCount': 16, 'source_question_range': 'Q17-Q32'},
                {'id': 'dokkai-3', 'paperNumber': 3, 'name': 'Dokkai Paper 3', 'questionCount': 16, 'source_question_range': 'Q33-Q48'},
                {'id': 'dokkai-4', 'paperNumber': 4, 'name': 'Dokkai Paper 4', 'questionCount': 12, 'source_question_range': 'Q49-Q60'},
                {'id': 'dokkai-5', 'paperNumber': 5, 'name': 'Dokkai Paper 5', 'questionCount': 15, 'source_question_range': 'Q61-Q75'},
                {'id': 'dokkai-6', 'paperNumber': 6, 'name': 'Dokkai Paper 6', 'questionCount': 15, 'source_question_range': 'Q76-Q90'},
                {'id': 'dokkai-7', 'paperNumber': 7, 'name': 'Dokkai Paper 7', 'questionCount': 12, 'source_question_range': 'Q91-Q102'},
            ]
            break

    # Update top-level totals
    manifest['totalPapers'] = sum(c['paperCount'] for c in manifest['categories'])
    manifest['totalQuestions'] = sum(c['questionCount'] for c in manifest['categories'])

    # Compare with existing
    existing_manifest = json.loads(MANIFEST.read_text(encoding='utf-8'))
    if existing_manifest != manifest:
        MANIFEST.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
        changes.append(f'manifest.json: dokkai paperCount/questionCount + 3 new paper entries; totalPapers={manifest["totalPapers"]}, totalQuestions={manifest["totalQuestions"]}')

    if not changes:
        print('No changes (already deployed).')
        return 0
    print()
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
