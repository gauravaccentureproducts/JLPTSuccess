"""Iteration 1 autonomous-mode fixes.

Findings:
1. MAJOR: Schema regression in grammar.json - Round 5 added 6 examples
   using `en` field instead of canonical `translation_en`. Rename.
2. MAJOR: 19 paper-files have per-paper position skew (max position
   exceeds n/4+1+tolerance). Per-paper rebalance.
3. MINOR: Cross-corpus duplicate stem (moji Q82 / goi Q1) — same shell
   「まいあさ コーヒーを X」. Diversify moji Q82.
4. MINOR: 17 items with choice-length asymmetry — defer to iteration 2
   for content-authoring care; flag 4 worst with stem-only signal risk
   (where the keyed answer is the only "long enough to be the answer"
   choice, e.g. Q5 [3,4,3,14]).

Idempotent. Lock-step MD<->JSON.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

changes: list[str] = []


# ============================================================================
# 1. Fix grammar.json schema regression (en -> translation_en)
# ============================================================================

def fix_grammar_en_field() -> None:
    g_path = ROOT / 'data/grammar.json'
    g = json.loads(g_path.read_text(encoding='utf-8'))
    patterns = g.get('patterns', g) if isinstance(g, dict) else g
    modified = False
    for pat in patterns:
        for ex in pat.get('examples', []):
            # If 'en' is set but 'translation_en' is missing/empty, migrate
            if ex.get('en') and not ex.get('translation_en'):
                ex['translation_en'] = ex.pop('en')
                modified = True
                changes.append(f'grammar.json {pat["id"]}: migrated en -> translation_en')
            elif 'en' in ex:
                # Both fields exist? Drop redundant en
                if ex.get('en') == ex.get('translation_en'):
                    del ex['en']
                    modified = True
                    changes.append(f'grammar.json {pat["id"]}: removed duplicate en field')
            # Also clean up: if 'romaji' is empty string and the rest of the
            # corpus doesn't use it, leave alone for stability.
    if modified:
        g_path.write_text(
            json.dumps(g, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8',
        )


# ============================================================================
# 2. Per-paper position rebalance
# ============================================================================

# Constraint sets from prior rounds — items that should NOT be permuted
# within a paper because their choice order has pedagogical meaning.

GOI_CONSTRAINED = {'Q38', 'Q39', 'Q40', 'Q41', 'Q64', 'Q73', 'Q83', 'Q92'}
MOJI_CONSTRAINED = {'Q54', 'Q55', 'Q59', 'Q73', 'Q79', 'Q89', 'Q92', 'Q93', 'Q95', 'Q99'}
DOKKAI_CONSTRAINED = {'Q3', 'Q6', 'Q7', 'Q15', 'Q41'}
# Bunpou Mondai 2 (Q61-90) is fully constrained
BUNPOU_CONSTRAINED = {f'Q{n}' for n in range(61, 91)}

CONSTRAINED = {
    'goi': GOI_CONSTRAINED,
    'moji': MOJI_CONSTRAINED,
    'dokkai': DOKKAI_CONSTRAINED,
    'bunpou': BUNPOU_CONSTRAINED,
}


def per_paper_target(n: int) -> list[int]:
    """Target distribution for n items: as close to uniform as possible."""
    base = n // 4
    extra = n % 4
    return [base + (1 if i < extra else 0) for i in range(4)]


def per_paper_rebalance(paper_path: Path, constrained: set, md_path: Path = None,
                        md_q_re_template: str = r'### {qnum}\b') -> None:
    """Rebalance a single paper-JSON in-place. Optionally update MD."""
    paper = json.loads(paper_path.read_text(encoding='utf-8'))
    questions = paper['questions']
    n = len(questions)
    target = per_paper_target(n)

    # Bin items
    cur = [0, 0, 0, 0]
    by_pos = {0: [], 1: [], 2: [], 3: []}  # unconstrained
    constrained_dist = [0, 0, 0, 0]
    for q in questions:
        idx = q['correctIndex']
        cur[idx] += 1
        if q['kbSourceId'] in constrained:
            constrained_dist[idx] += 1
        else:
            by_pos[idx].append(q)

    target_uncon = [target[i] - constrained_dist[i] for i in range(4)]
    cur_uncon = [cur[i] - constrained_dist[i] for i in range(4)]
    deltas = [target_uncon[i] - cur_uncon[i] for i in range(4)]

    surplus = [[i, -d] for i, d in enumerate(deltas) if d < 0]
    deficit = [[i, d] for i, d in enumerate(deltas) if d > 0]
    deficit.sort(key=lambda d: cur_uncon[d[0]])

    if not surplus or not deficit:
        return

    # Build per-question target index
    moves = {}
    for src_pos, src_count in surplus:
        for q in by_pos[src_pos][:src_count]:
            for slot in deficit:
                if slot[1] > 0:
                    moves[q['id']] = slot[0]
                    slot[1] -= 1
                    break

    if not moves:
        return

    # Apply: swap positions in choices
    md_text = None
    if md_path is not None:
        md_text = md_path.read_text(encoding='utf-8')

    for q in questions:
        if q['id'] not in moves:
            continue
        target_idx = moves[q['id']]
        cur_idx = q['correctIndex']
        if cur_idx == target_idx:
            continue
        new_choices = list(q['choices'])
        new_choices[cur_idx], new_choices[target_idx] = new_choices[target_idx], new_choices[cur_idx]
        q['choices'] = new_choices
        q['correctIndex'] = target_idx
        changes.append(f'{paper_path.name} {q["id"]} ({q["kbSourceId"]}): pos {cur_idx+1} -> {target_idx+1}')

        # Update MD block
        if md_text is not None:
            qnum = q['kbSourceId']
            # bunpou/goi/moji: "### Q<n>"; dokkai: "#### Q<n>"
            for prefix in ['#### ', '### ']:
                block_re = re.compile(rf'{re.escape(prefix)}{re.escape(qnum)}\b([\s\S]+?)(?=\n#{{3,4}} Q\d|\n## )')
                m = block_re.search(md_text)
                if m:
                    block = m.group(0)
                    new_choice_lines = '\n'.join(f'{i+1}. {c}' for i, c in enumerate(new_choices))
                    list_re = re.compile(r'(?m)^1\. .+\n2\. .+\n3\. .+\n4\. .+')
                    new_block, count = list_re.subn(new_choice_lines, block, count=1)
                    if count == 1:
                        ans_re = re.compile(r'\*\*Answer: \d+\*\*')
                        new_block = ans_re.sub(f'**Answer: {target_idx+1}**', new_block, count=1)
                        if new_block != block:
                            md_text = md_text[:m.start()] + new_block + md_text[m.end():]
                    break

    paper_path.write_text(json.dumps(paper, ensure_ascii=False, indent=2), encoding='utf-8')
    if md_text is not None and md_path is not None:
        original = md_path.read_text(encoding='utf-8')
        if md_text != original:
            md_path.write_text(md_text, encoding='utf-8')


def rebalance_all_papers() -> None:
    md_paths = {
        'goi': ROOT / 'KnowledgeBank/goi_questions_n5.md',
        'moji': ROOT / 'KnowledgeBank/moji_questions_n5.md',
        'dokkai': ROOT / 'KnowledgeBank/dokkai_questions_n5.md',
        'bunpou': ROOT / 'KnowledgeBank/bunpou_questions_n5.md',
    }
    for cat, constrained in CONSTRAINED.items():
        for f in sorted((ROOT / f'data/papers/{cat}').glob('paper-*.json')):
            per_paper_rebalance(f, constrained, md_paths[cat])


# ============================================================================
# 3. Cross-corpus duplicate stem (moji Q82 / goi Q1)
# ============================================================================
# Both have stem 「まいあさ コーヒーを X」 (X = blank with kanji target on
# moji, blank for vocab fill on goi). Diversify moji Q82 to use a different
# verb-target compound.
#
# moji Q82 currently tests writing 飲み (kanji writing for のみ). Shift the
# stem from まいあさ コーヒー to a different N5 context.

def diversify_moji_q82() -> None:
    paper_path = ROOT / 'data/papers/moji/paper-6.json'
    paper = json.loads(paper_path.read_text(encoding='utf-8'))
    target_qid = 'Q82'
    new_stem = 'パーティーで ジュースを __のみ__ました。'
    md_block = '''### Q82

パーティーで ジュースを __のみ__ました。

1. 食み
2. 飲み
3. 読み
4. 進み

**Answer: 2** - 飲む (のむ - to drink). 飲 is N5; the distractors share visual / phonetic similarity in a different context.'''

    modified = False
    for q in paper['questions']:
        if q['kbSourceId'] != target_qid:
            continue
        if q.get('stem_html') != new_stem:
            q['stem_html'] = new_stem
            q['rationale'] = '飲む (のむ - to drink). 飲 is N5; the distractors share visual / phonetic similarity in a different context.'
            modified = True
            changes.append(f'paper-6.json {q["id"]} ({target_qid}): diversified stem (was duplicate of goi Q1)')
    if modified:
        paper_path.write_text(json.dumps(paper, ensure_ascii=False, indent=2), encoding='utf-8')

    md_path = ROOT / 'KnowledgeBank/moji_questions_n5.md'
    text = md_path.read_text(encoding='utf-8')
    block_re = re.compile(r'### Q82\b[\s\S]+?(?=\n### Q\d|\n## )')
    m = block_re.search(text)
    if m and m.group(0).strip() != md_block.strip():
        text = text[:m.start()] + md_block + '\n' + text[m.end():]
        md_path.write_text(text, encoding='utf-8')
        changes.append('moji_questions_n5.md Q82: replaced block (diversification)')


def main() -> int:
    fix_grammar_en_field()
    rebalance_all_papers()
    diversify_moji_q82()
    if not changes:
        print('No changes (already in fixed state).')
        return 0
    print(f'{len(changes)} edits applied.')
    for c in changes[:80]:
        print(f'  - {c}')
    if len(changes) > 80:
        print(f'  ... +{len(changes)-80} more')
    return 0


if __name__ == '__main__':
    sys.exit(main())
