"""Pass-23 round 2: fix the remaining real issues round-1 audit found.

(1) Five prompts have non-N5 vocab (あらわす, ような, めいし, どうし) —
    rewrite all to the generic N5-pure prompt. The question stems
    already carry the context anchor; the prompts' explanatory hints
    were leaking N3+ vocabulary for no learner benefit.

(2) q-0022 (ペン（ ）ノートなどを かいました) — や is the canonical N5
    pattern for "X や Y など" (non-exhaustive list); と with など is also
    grammatical but less idiomatic. To eliminate any multi-correct
    risk, replace と in the choices with へ (clearly wrong).

All edits restricted to data/questions.json. Idempotent.
"""
import json
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

QUESTION_FIXES = {
    # Cat J prompt scope-leak fixes — five prompts use N3+ vocab.
    # Replace with the generic N5-pure prompt; question stems carry context.
    'q-0020': {
        'prompt_ja': '（  ）に いれる ことばを えらんで ください。',
    },
    'q-0293': {
        'prompt_ja': '（  ）に いれる ことばを えらんで ください。',
    },
    'q-0484': {
        'prompt_ja': '「ので」の まえに つける もじを えらんで ください。',
    },
    'q-0485': {
        'prompt_ja': '（  ）に いれる ことばを えらんで ください。',
    },
    'q-0486': {
        'prompt_ja': '（  ）に いれる ことばを えらんで ください。',
    },
    # q-0022: borderline multi-correct (や / と with など both grammatical).
    # Replace と with へ (clearly wrong: へ doesn't connect nouns).
    'q-0022': {
        'choices': ['へ', 'や', 'は', 'で'],
        # correctAnswer stays や; the only change is と → へ in distractors
    },
}


def main():
    qpath = ROOT / 'data' / 'questions.json'
    data = json.load(qpath.open(encoding='utf-8'))
    applied: list[str] = []
    skipped: list[str] = []
    for q in data['questions']:
        qid = q.get('id')
        if qid not in QUESTION_FIXES:
            continue
        patch = QUESTION_FIXES[qid]
        # Idempotency: if every patched field already matches, skip
        if all(q.get(k) == v for k, v in patch.items()):
            skipped.append(qid)
            continue
        for k, v in patch.items():
            q[k] = v
        # Mark as manually reviewed
        q['auto'] = False
        applied.append(qid)
    if applied:
        qpath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
    print(f'Applied: {applied}')
    print(f'Skipped (already fixed): {skipped}')
    missing = set(QUESTION_FIXES) - set(applied) - set(skipped)
    if missing:
        print(f'WARNING - not found: {sorted(missing)}')


if __name__ == '__main__':
    main()
