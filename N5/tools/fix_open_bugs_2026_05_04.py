"""Close 7 of 8 items from the open-bug-list filed 2026-05-04.

Items handled:
  Bug 1: dokkai exception register/JSON alignment - VERIFIED already
         aligned (向/央/付 all in JSON; marker comment in MD is correct).
         No fix needed.
  Bug 2: dokkai source 2 occurrences of 初めて → はじめて
  Bug 3: dokkai source 1 occurrence of 急いで → いそいで
  Bug 4: dokkai narrator unification (30 書いた 人 + 6 ひっしゃ → この 人)
         in source MD AND data/papers/dokkai/*.json
  Bug 5: bunpou Q24 でんしゃ → しんかんせん (Tokyo-Osaka realism)
  Bug 6: moji distractor-convention section extended with 3rd type
  Bug 7: vocab POS-tag legend header date-stamp removed (cosmetic)

Bug 8 (filename rename of authentic_extracted_n5.md → externally_sourced_n5.md):
  was deferred when this script was written (2026-05-04 morning); closed
  in a follow-up commit later the same day. See CHANGELOG v1.12.5.

Idempotent. JA-13 / JA-28 / etc. invariants run via
check_content_integrity.py after this script.
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KB = ROOT / 'KnowledgeBank'
PAPERS = ROOT / 'data' / 'papers'

changes: list[str] = []


def read(p: Path) -> str:
    return p.read_text(encoding='utf-8')


def write(p: Path, s: str) -> None:
    p.write_text(s, encoding='utf-8')


# =====================================================================
# Bug 2 + 3 + 4: dokkai source MD fixes (kanji-scope + narrator unify)
# =====================================================================
def fix_dokkai_md() -> None:
    p = KB / 'dokkai_questions_n5.md'
    text = read(p)
    before_len = len(text)
    n_isogu = text.count('急いで')
    n_init = text.count('初めて')
    n_kaita = text.count('書いた 人')
    n_hisha = text.count('ひっしゃ')

    # Bug 2: 初めて → はじめて (catch both kanji-only forms)
    if '初めて' in text:
        text = text.replace('初めて', 'はじめて')
        changes.append(f'Bug 2: dokkai_questions_n5.md - replaced {n_init}× 初めて → はじめて')

    # Bug 3: 急いで → いそいで
    if '急いで' in text:
        text = text.replace('急いで', 'いそいで')
        changes.append(f'Bug 3: dokkai_questions_n5.md - replaced {n_isogu}× 急いで → いそいで')

    # Bug 4: 書いた 人 → この 人; ひっしゃ → この 人
    if '書いた 人' in text:
        text = text.replace('書いた 人', 'この 人')
        changes.append(f'Bug 4: dokkai_questions_n5.md - replaced {n_kaita}× 書いた 人 → この 人')
    if 'ひっしゃ' in text:
        text = text.replace('ひっしゃ', 'この 人')
        changes.append(f'Bug 4: dokkai_questions_n5.md - replaced {n_hisha}× ひっしゃ → この 人')

    if len(text) != before_len:
        write(p, text)


# =====================================================================
# Bug 4 propagation: dokkai paper JSON narrator unification
# =====================================================================
def fix_dokkai_papers_json() -> None:
    for n in (1, 2, 3, 4):
        p = PAPERS / 'dokkai' / f'paper-{n}.json'
        if not p.exists():
            continue
        text = read(p)
        before = text
        # Substring replace inside the JSON string. Safe because both
        # strings are only used inside Japanese question text fields.
        if '書いた 人' in text:
            cnt = text.count('書いた 人')
            text = text.replace('書いた 人', 'この 人')
            changes.append(f'Bug 4: papers/dokkai/paper-{n}.json - replaced {cnt}× 書いた 人 → この 人')
        if 'ひっしゃ' in text:
            cnt = text.count('ひっしゃ')
            text = text.replace('ひっしゃ', 'この 人')
            changes.append(f'Bug 4: papers/dokkai/paper-{n}.json - replaced {cnt}× ひっしゃ → この 人')
        # Also catch 初めて / 急いで if they made it through extraction.
        if '初めて' in text:
            cnt = text.count('初めて')
            text = text.replace('初めて', 'はじめて')
            changes.append(f'Bug 2: papers/dokkai/paper-{n}.json - replaced {cnt}× 初めて → はじめて')
        if '急いで' in text:
            cnt = text.count('急いで')
            text = text.replace('急いで', 'いそいで')
            changes.append(f'Bug 3: papers/dokkai/paper-{n}.json - replaced {cnt}× 急いで → いそいで')
        if text != before:
            # Validate JSON shape didn't break.
            json.loads(text)
            write(p, text)


# =====================================================================
# Bug 5: bunpou Q24 でんしゃ → しんかんせん (Tokyo-Osaka route)
# =====================================================================
def fix_bunpou_q24() -> None:
    p = KB / 'bunpou_questions_n5.md'
    text = read(p)
    OLD = 'とうきょう（　　）おおさかまで でんしゃで いきます。'
    NEW = 'とうきょう（　　）おおさかまで しんかんせんで いきます。'
    if OLD in text:
        text = text.replace(OLD, NEW)
        changes.append('Bug 5: bunpou Q24 - でんしゃ → しんかんせん (Tokyo-Osaka route)')
        write(p, text)
    # Propagate to bunpou paper JSONs - Q24 lives in bunpou-2 (Q16-Q30).
    for paper_n in (2,):
        pj = PAPERS / 'bunpou' / f'paper-{paper_n}.json'
        if not pj.exists():
            continue
        text2 = read(pj)
        if 'おおさかまで でんしゃで' in text2:
            text2 = text2.replace('おおさかまで でんしゃで', 'おおさかまで しんかんせんで')
            json.loads(text2)  # validate
            write(pj, text2)
            changes.append(f'Bug 5: papers/bunpou/paper-{paper_n}.json - same Q24 fix')


# =====================================================================
# Bug 6: moji distractor-convention section - add 3rd type
# =====================================================================
def fix_moji_distractor_convention() -> None:
    p = KB / 'moji_questions_n5.md'
    text = read(p)
    OLD = (
        'In Mondai 2 (orthography), distractor verb forms may be '
        '**invented** (not real conjugations) or use **non-N5 kanji** '
        'with the same on-yomi as the target. The test asks "which '
        'kanji visually belongs in this word", not "is this conjugation '
        'pattern independently grammatical". Examples: a 入ります '
        'distractor of `出ります` is NOT a real conjugation (the correct '
        'form is 出ます); a 立ちます distractor of `経ちます` IS a real '
        'verb but uses N3+ kanji. Both are acceptable distractor types '
        'because the question is purely orthographic.'
    )
    NEW = (
        'In Mondai 2 (orthography) and Mondai 1 (kanji-reading), '
        'distractors fall into three acceptable types:\n'
        '\n'
        '1. **Visually-similar N5 kanji** with a different reading '
        '(e.g., 多い / 古い / 長い for a 高い target). Most common '
        'distractor type at N5; tests whether the learner recognizes '
        'the right glyph among lookalikes drawn entirely from the '
        'N5 syllabus.\n'
        '\n'
        '2. **Non-N5 kanji with the same on-yomi** as the target '
        '(e.g., a 立ちます distractor of `経ちます` - N3+ kanji, real '
        'verb meaning "elapse"). Tests glyph recognition; the '
        'non-N5 kanji is acceptable because the question is purely '
        'orthographic.\n'
        '\n'
        '3. **Invented (non-real) verb forms** that combine an N5 '
        'kanji with a wrong conjugation pattern (e.g., a 入ります '
        'distractor of `出ります` - the real form is 出ます). Tests '
        'glyph recognition without requiring the distractor to be '
        'a grammatically valid conjugation.\n'
        '\n'
        'All three types are acceptable because the question asks '
        '"which kanji visually belongs in this word", not "is this '
        'conjugation pattern grammatical".'
    )
    if OLD in text and 'Visually-similar N5 kanji' not in text:
        text = text.replace(OLD, NEW)
        changes.append('Bug 6: moji distractor-convention section extended (3 types: visually-similar-N5, same-on-yomi-non-N5, invented-form)')
        write(p, text)


# =====================================================================
# Bug 7: vocab POS-tag legend header - strip date stamp
# =====================================================================
def fix_vocab_pos_legend_header() -> None:
    p = KB / 'vocabulary_n5.md'
    text = read(p)
    OLD = '## Part-of-Speech Tags (added 2026-05-02)'
    NEW = '## Part-of-Speech Tags'
    if OLD in text:
        text = text.replace(OLD, NEW)
        changes.append('Bug 7: vocabulary_n5.md - stripped (added 2026-05-02) date stamp from POS legend header')
        write(p, text)


def main() -> int:
    fix_dokkai_md()
    fix_dokkai_papers_json()
    fix_bunpou_q24()
    fix_moji_distractor_convention()
    fix_vocab_pos_legend_header()
    if not changes:
        print('No changes (already in fixed state).')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
