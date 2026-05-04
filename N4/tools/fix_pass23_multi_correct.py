"""Pass-23 fixes triggered by user audit (2026-05-02):
- Multi-correct bugs in 2 runtime questions
- Scope-leak in 2 question prompts (from earlier user finding)
- Empty-stem questions in 1 paper (parser bug; drop the paper)

All fixes are scoped to data/questions.json + data/papers/{bunpou/manifest}.
NOT touching parallel-session-active files (css/main.css, index.html,
js/app.js, js/home.js, sw.js, tests/p0-smoke.spec.js).

Idempotent.
"""
import json
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# --------------------------------------------------------------------
# Runtime data/questions.json fixes
# --------------------------------------------------------------------

QUESTION_FIXES = {
    # User example #1 (multi-correct):
    # original: コーヒー（ ）飲みます。choices [など,だけ,に,や] correct=だけ
    # Both など ("etc.") and だけ ("only") work as scope-restriction
    # particles before 飲みます. Fix: add follow-up sentence
    # "おちゃや ジュースは 飲みません" which rejects など (etc. implies
    # other items) and locks だけ.
    'q-0293': {
        'question_ja': 'わたしは コーヒー（  ）飲みます。 おちゃや ジュースは 飲みません。',
        'prompt_ja': '「ほかは 飲まない」こと を あらわす ことばを えらんで ください。',
        'explanation_en': "だけ means 'only / nothing but' — it limits the action to the noun marked. The follow-up sentence 'I don't drink tea or juice' confirms the scope: only coffee, nothing else.",
        'distractor_explanations': {
            'など': "など means 'and others / etc.' — it implies more than just coffee. The follow-up sentence ('I don't drink tea or juice') contradicts that, so など is wrong here.",
            'に': "に marks destinations, recipients, or specific times. It does not mark scope-limitation on a direct object before a transitive verb.",
            'や': "や means 'and (non-exhaustive)' BETWEEN two nouns. It needs a second noun after the blank — there isn't one here.",
        },
    },
    # User-implicit problem #2 (multi-correct):
    # original: 9時（ ）しごとです。 choices [は, から, まで, に]  correct=から
    # Both から (from 9) and まで (until 9) work with the copula です. Fix:
    # change the verb to はじまる (start), which only pairs with から.
    'q-0018': {
        'question_ja': 'しごとは 9時（　）はじまります。',
        'prompt_ja': '「いつから はじまるか」を しめす ことばを えらんで ください。',
        'explanation_en': "から marks the starting point ('from'). Paired with the verb はじまる ('to start'), the natural reading is 'work starts FROM 9'.",
        'distractor_explanations': {
            'は': "は is the topic marker. It cannot mark a time as a start/end point.",
            'まで': "まで marks an end point ('until'). With はじまる ('start'), an end-point marker doesn't fit — start-verbs pair with から.",
            'に': "に marks a single specific time ('at 9'), not the start of a range. With はじまる, a starting point is what's being marked, so から is the natural fit.",
        },
    },
    # Earlier user finding (scope leak in prompt vocabulary):
    # q-0487 prompt used あらわす (N3 vocab); rewrite with N5-only.
    'q-0487': {
        'prompt_ja': '（  ）に いれる ことばを えらんで ください。',
    },
    # q-0488 prompt used ひんど (N3), あらわす (N3), のような (N4 grammar);
    # rewrite with N5-only.
    'q-0488': {
        'prompt_ja': '（  ）に いれる ことばを えらんで ください。',
    },
}


def fix_questions():
    qpath = ROOT / 'data' / 'questions.json'
    data = json.load(qpath.open(encoding='utf-8'))
    applied = []
    for q in data['questions']:
        qid = q.get('id')
        if qid not in QUESTION_FIXES:
            continue
        patch = QUESTION_FIXES[qid]
        # Idempotency check: if any patched field already matches, skip
        fields_match = all(q.get(k) == v for k, v in patch.items())
        if fields_match:
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
    return applied


# --------------------------------------------------------------------
# Paper data fix: drop bunpou paper 7 (empty-stem Mondai-3 questions)
# --------------------------------------------------------------------

def fix_papers_manifest():
    """Remove bunpou paper 7 from the manifest (questions are empty-stem
    due to a Mondai-3 passage parser bug; tracked as Pass-24 work). Also
    delete the paper-7.json file. The bunpou category drops from 7 to 6
    papers, 100 → 90 questions."""
    mpath = ROOT / 'data' / 'papers' / 'manifest.json'
    paper7_path = ROOT / 'data' / 'papers' / 'bunpou' / 'paper-7.json'
    manifest = json.load(mpath.open(encoding='utf-8'))
    changed = False
    for cat in manifest['categories']:
        if cat['id'] != 'bunpou':
            continue
        before = len(cat['papers'])
        cat['papers'] = [p for p in cat['papers'] if p['paperNumber'] != 7]
        after = len(cat['papers'])
        if after < before:
            removed_q = sum(15 for _ in range(before - after))  # ~10 actual; close enough
            # Fix the count more accurately: the dropped paper had 10 Qs
            cat['paperCount'] = after
            cat['questionCount'] = sum(p['questionCount'] for p in cat['papers'])
            changed = True
            print(f'  Dropped bunpou paper 7 from manifest. '
                  f'bunpou now: {after} papers, {cat["questionCount"]} questions')
    if changed:
        # Recompute totals
        manifest['totalPapers'] = sum(c['paperCount'] for c in manifest['categories'])
        manifest['totalQuestions'] = sum(c['questionCount'] for c in manifest['categories'])
        mpath.write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
        if paper7_path.exists():
            paper7_path.unlink()
            print(f'  Deleted {paper7_path.relative_to(ROOT)}')
        return True
    return False


def main():
    print('=== Pass-23 multi-correct + scope-leak fixes ===\n')
    applied = fix_questions()
    print(f'data/questions.json: fixed {len(applied)} questions: {applied}')
    print()
    fixed_pap = fix_papers_manifest()
    print(f'data/papers/manifest.json: changed = {fixed_pap}')


if __name__ == '__main__':
    main()
