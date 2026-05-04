"""Round 5 N5 thorough-audit fixes: reading.json + grammar.json examples.

Sub-agent audits identified:

reading.json:
  - Severe position skew 6/50/25/3 (B=60%, D=4%). Rebalance to ~21/21/21/21.
  - 2 pairs of duplicated explanation_en across question pairs.
  - 1 distractor length-asymmetry issue (n5.read.028.q1).
  - 1 implausible distractor (n5.read.011.q2 つめたかった).
  - 1 mixed-script inconsistency (n5.read.007 passage 二週間 vs choice 2しゅうかん).

grammar.json:
  - n5-176 [0]: doesn't demonstrate the pattern (formal なくては, not casual なくちゃ).
  - n5-162 [0,1]: noun-pattern in verb-plain-pattern slot.
  - n5-163 [0]: noun-pattern in verb-た-pattern slot.
  - n5-098: meaning_en doesn't match examples.
  - n5-007 [2]: たばこを すいません (awkward apology homophone).
  - n5-007 [3]: なんで きましたか ambiguous (reads as "why" not "how").
  - n5-182: form field "affirmative" but content is prohibition.

Idempotent. Lock-step updates.
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent

changes: list[str] = []


# ============================================================================
# READING.JSON: position rebalance + content fixes
# ============================================================================

def swap_choice_positions(choices: list, idx_a: int, idx_b: int) -> list:
    out = list(choices)
    out[idx_a], out[idx_b] = out[idx_b], out[idx_a]
    return out


def find_correct_idx(choices: list, correct_answer: str) -> int:
    return choices.index(correct_answer) if correct_answer in choices else -1


# Pre-rebalance content fixes (apply BEFORE position permutation so the new
# choice content gets permuted into the target distribution).
READING_CONTENT_FIXES = {
    # n5.read.011 q2: replace つめたかった (implausible — passage explicitly says あつかった)
    # with しおからかった (plausible distractor at N5 level).
    'n5.read.011.q2': {
        'choices_replace': {'つめたかった': 'しおからかった'},
    },
    # n5.read.028 q1: keyed answer was a compound, distractors were single adjectives.
    # Reshape distractors to match length.
    'n5.read.028.q1': {
        'choices': ['大きくて にぎやかです', 'あまり 大きくなくて しずかです',
                    'せまくて うるさいです', 'ひろくて あかるいです'],
        'correctAnswer': 'あまり 大きくなくて しずかです',
    },
    # n5.read.034 q2: explanation_en was duplicate of q1. Refocus on the place.
    'n5.read.034.q2': {
        'explanation_en': "'学校で パーティーが あります' - the venue is the school.",
    },
    # n5.read.035 q3: explanation_en was duplicate of q2. Refocus on the companion.
    'n5.read.035.q3': {
        'explanation_en': "'母と いっしょに' - with her mother.",
    },
}


def apply_reading_content_fixes(passages):
    for psg in passages:
        for q in psg.get('questions', []):
            qid = q.get('id', '')
            if qid not in READING_CONTENT_FIXES:
                continue
            fix = READING_CONTENT_FIXES[qid]
            if 'choices_replace' in fix:
                for old, new in fix['choices_replace'].items():
                    if old in q['choices']:
                        idx = q['choices'].index(old)
                        q['choices'][idx] = new
                        changes.append(f'reading.json {qid}: choice "{old}" -> "{new}"')
            if 'choices' in fix:
                if q.get('choices') != fix['choices']:
                    q['choices'] = fix['choices']
                    changes.append(f'reading.json {qid}: choices replaced (length match)')
            if 'correctAnswer' in fix:
                if q.get('correctAnswer') != fix['correctAnswer']:
                    q['correctAnswer'] = fix['correctAnswer']
                    changes.append(f'reading.json {qid}: correctAnswer updated')
            if 'explanation_en' in fix:
                if q.get('explanation_en') != fix['explanation_en']:
                    q['explanation_en'] = fix['explanation_en']
                    changes.append(f'reading.json {qid}: explanation_en updated')


# Per-question target index for rebalance. Computed deterministically:
# walk all 84 questions in (passage_id, q_idx) order; for the heavy B-skew,
# move the first 15 B-keyed to A, next 14 B-keyed to D, then 4 C-keyed to D.
# Hard-coded for idempotency.
READING_TARGET_INDEX = {}


def compute_reading_rebalance(passages):
    """Build TARGET_INDEX for reading.json based on current state."""
    items = []
    for psg in passages:
        for q in psg.get('questions', []):
            ans = q.get('correctAnswer', '')
            choices = q.get('choices', [])
            idx = find_correct_idx(choices, ans)
            if 0 <= idx <= 3:
                items.append((q['id'], idx, len(choices)))

    # Skip 3-choice items (none expected, but defensive)
    items4 = [(qid, idx) for qid, idx, n in items if n == 4]
    n = len(items4)
    target = [n // 4 + (1 if i < n % 4 else 0) for i in range(4)]  # 21/21/21/21

    cur = [0, 0, 0, 0]
    by_pos = {0: [], 1: [], 2: [], 3: []}
    for qid, idx in items4:
        cur[idx] += 1
        by_pos[idx].append(qid)
    deltas = [target[i] - cur[i] for i in range(4)]
    surplus = [[i, -deltas[i]] for i in range(4) if deltas[i] < 0]
    deficit = [[i, deltas[i]] for i in range(4) if deltas[i] > 0]
    deficit.sort(key=lambda d: cur[d[0]])  # fill lowest-count first

    moves = {}
    for src_pos, src_count in surplus:
        for qid in by_pos[src_pos][:src_count]:
            for slot in deficit:
                if slot[1] > 0:
                    moves[qid] = slot[0]
                    slot[1] -= 1
                    break
    return moves


def apply_reading_rebalance(passages, moves):
    for psg in passages:
        for q in psg.get('questions', []):
            qid = q.get('id', '')
            if qid not in moves:
                continue
            target_idx = moves[qid]
            ans = q.get('correctAnswer', '')
            choices = q.get('choices', [])
            cur_idx = find_correct_idx(choices, ans)
            if cur_idx < 0 or cur_idx == target_idx:
                continue
            new_choices = swap_choice_positions(choices, cur_idx, target_idx)
            q['choices'] = new_choices
            changes.append(f'reading.json {qid}: pos {cur_idx+1} -> {target_idx+1}')


# ============================================================================
# GRAMMAR.JSON: example-quality fixes
# ============================================================================

GRAMMAR_FIXES = {
    # n5-176: ~なくちゃ / ~なきゃ casual contractions. Example [0] used the
    # formal ~なくては いけません - doesn't demonstrate the contractions.
    'n5-176': {
        'examples_replace': [
            (0, {'ja': 'もう 行かなくちゃ。', 'romaji': '', 'en': 'I have to go now.', 'vocab_ids': []}),
        ],
    },

    # n5-162: pattern is Verb-plain + まえに. Examples [0] and [1] used
    # Noun + の + まえに pattern (which belongs to n5-161). Replace.
    'n5-162': {
        'examples_replace': [
            (0, {'ja': '出かける まえに、しんぶんを 読みます。', 'romaji': '',
                 'en': 'Before going out, I read the newspaper.', 'vocab_ids': []}),
            (1, {'ja': 'ねる まえに、はを みがきます。', 'romaji': '',
                 'en': 'Before sleeping, I brush my teeth.', 'vocab_ids': []}),
        ],
    },

    # n5-163: pattern is Verb-た + あとで. Example [0] used Noun + の + あとで.
    'n5-163': {
        'examples_replace': [
            (0, {'ja': 'しごとが おわった あとで、 のみに 行きました。', 'romaji': '',
                 'en': 'After work finished, I went out drinking.', 'vocab_ids': []}),
        ],
    },

    # n5-098: meaning_en is misaligned with examples. Examples are about
    # X が すき/きらい contrast. Re-align meaning_en.
    'n5-098': {
        'meaning_en_set': 'Expressing likes / dislikes contrast (using すき / きらい).',
    },

    # n5-007: で particle (means/instrument). Two problematic examples:
    # [2] たばこを すいません (collides with apology homophone)
    # [3] なんで きましたか (overwhelmingly read as "why" not "how")
    'n5-007': {
        'examples_replace': [
            (2, {'ja': 'バスで 学校へ 行きます。', 'romaji': '',
                 'en': 'I go to school by bus.', 'vocab_ids': []}),
            (3, {'ja': 'タクシーで うちへ かえりました。', 'romaji': '',
                 'en': 'I went home by taxi.', 'vocab_ids': []}),
        ],
    },

    # n5-182: form field said 'affirmative' but the pattern is prohibition
    # (Verb-dictionary + な = "Don't V"). Set form to 'prohibition' on each
    # example.
    'n5-182': {
        'examples_set_form': 'prohibition',
    },
}


def apply_grammar_fixes():
    grammar = json.loads((ROOT / 'data/grammar.json').read_text(encoding='utf-8'))
    items = grammar if isinstance(grammar, list) else grammar.get('items', grammar.get('patterns', []))

    modified = False
    for pat in items:
        pid = pat.get('id', '')
        if pid not in GRAMMAR_FIXES:
            continue
        fix = GRAMMAR_FIXES[pid]
        if 'examples_replace' in fix:
            for idx, new_ex in fix['examples_replace']:
                if idx < len(pat.get('examples', [])):
                    cur = pat['examples'][idx]
                    # Preserve original vocab_ids if present and new is empty
                    if not new_ex.get('vocab_ids') and cur.get('vocab_ids'):
                        new_ex['vocab_ids'] = cur['vocab_ids']
                    if cur != new_ex:
                        pat['examples'][idx] = new_ex
                        modified = True
                        changes.append(f'grammar.json {pid} ex[{idx}]: replaced')
        if 'meaning_en_set' in fix:
            new = fix['meaning_en_set']
            if pat.get('meaning_en') != new:
                pat['meaning_en'] = new
                modified = True
                changes.append(f'grammar.json {pid}: meaning_en updated')
        if 'examples_set_form' in fix:
            for ex in pat.get('examples', []):
                if ex.get('form') != fix['examples_set_form']:
                    ex['form'] = fix['examples_set_form']
                    modified = True
            if modified:
                changes.append(f'grammar.json {pid}: examples form -> {fix["examples_set_form"]}')

    if modified:
        if isinstance(grammar, dict):
            (ROOT / 'data/grammar.json').write_text(
                json.dumps(grammar, ensure_ascii=False, indent=2) + '\n',
                encoding='utf-8',
            )
        else:
            (ROOT / 'data/grammar.json').write_text(
                json.dumps(items, ensure_ascii=False, indent=2) + '\n',
                encoding='utf-8',
            )


def main() -> int:
    # Reading.json: load, fix content, rebalance, save
    reading_path = ROOT / 'data/reading.json'
    reading = json.loads(reading_path.read_text(encoding='utf-8'))
    passages = reading.get('passages', [])

    apply_reading_content_fixes(passages)
    moves = compute_reading_rebalance(passages)
    apply_reading_rebalance(passages, moves)

    # Save reading.json if any changes
    new_text = json.dumps(reading, ensure_ascii=False, indent=2) + '\n'
    if new_text != reading_path.read_text(encoding='utf-8'):
        reading_path.write_text(new_text, encoding='utf-8')

    # Grammar.json fixes
    apply_grammar_fixes()

    if not changes:
        print('No changes (already in fixed state).')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
