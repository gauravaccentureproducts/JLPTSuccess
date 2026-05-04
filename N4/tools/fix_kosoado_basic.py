"""
Pass-15 Basic-issue fix #1: ko-so-a-do questions without spatial context.

Four context-less ko-so-a-do questions in data/questions.json had multiple
valid answers because no spatial relationship between speaker / listener /
referent was established. Native-teacher review flagged this category as a
critical pedagogical defect (3 of 4 distractors were grammatically valid
completions).

Fix: add scene-setting context inside question_ja (matching the style of
q-0028 / q-0029 / q-0049 which already do this correctly), tighten
prompt_ja, and replace stub distractor explanations with reasons that
contrast each demonstrative's deictic role.

Affected:
  q-0424  (これ/それ/あれ/どれ) — add: speaker holds the book
  q-0425  (こちら/そちら/あちら/どちら) — add: host guiding guest to own seat
  q-0431  (ここ/そこ/あそこ/どこ) — add: speaker is at the library
  q-0432  (どれ/これ/それ/あれ) — add: many bags on the desk

Idempotent: re-running the script after a fix is a no-op.
"""
import json
from pathlib import Path

QUESTIONS_PATH = Path(__file__).resolve().parent.parent / 'data' / 'questions.json'

FIXES = {
    'q-0424': {
        'question_ja': '（じぶんの 手の 中の 本を 友だちに みせて）　（  ）は ほんです。',
        'prompt_ja': 'じぶんの 手に もっている 本を みせて 言う ことばを えらんで ください。',
        'explanation_en': "When the speaker is holding the item, use これ ('this' — near speaker). それ marks things near the listener; あれ marks things far from both; どれ asks 'which one?'.",
        'distractor_explanations': {
            'それ': "それ is for things near the LISTENER. Here the speaker is holding the book in their own hand, so これ (near speaker) is correct.",
            'あれ': "あれ is for things far from BOTH speaker and listener. The book is in the speaker's own hand, so use これ.",
            'どれ': "どれ is the question word 'which one?'. The speaker is making a statement, not asking.",
        },
    },
    'q-0425': {
        'question_ja': '（おきゃくさんを じぶんの 近くの せきへ あんないして）　（  ）へ どうぞ。',
        'prompt_ja': 'おきゃくさんを ていねいに あんないする ことばを えらんで ください。',
        'explanation_en': "こちら ('this way / this side') is used by a host inviting or guiding someone toward their own location. The polite set phrase is こちらへ どうぞ ('please, this way'). そちら points toward the listener; あちら points far from both; どちら asks 'which way?'.",
        'distractor_explanations': {
            'そちら': "そちら points toward the LISTENER's side. The speaker is inviting the guest TO themselves, not directing them away.",
            'あちら': "あちら points to a place FAR from both speaker and listener. The seat being offered is near the speaker.",
            'どちら': "どちら is the question word 'which way?'. The speaker is offering, not asking.",
        },
    },
    'q-0431': {
        'question_ja': '（としょかんの 中で 友だちに 言います）　（  ）は としょかんです。',
        'prompt_ja': 'じぶんが いる ばしょを さして 言う ことばを えらんで ください。',
        'explanation_en': "When the speaker is at the place they are describing, use ここ ('here' — speaker's location). そこ is near the listener; あそこ is far from both; どこ asks 'where?'.",
        'distractor_explanations': {
            'そこ': "そこ is for places near the LISTENER. The speaker is INSIDE the library, so use ここ.",
            'あそこ': "あそこ is for places FAR from both speaker and listener. The speaker is right there in the library.",
            'どこ': "どこ is the question word 'where?'. The speaker is making a statement, not asking.",
        },
    },
    'q-0432': {
        'question_ja': '（つくえの 上に かばんが いくつも あります）　（  ）が あなたの ですか。',
        'prompt_ja': 'たくさんの 中から 一つを たずねる ことばを えらんで ください。',
        'explanation_en': "When asking 'which one?' out of multiple options, use どれ. The が particle here marks the interrogative subject: どれが asks for a selection. これ / それ / あれ + は would be yes/no questions about a single item, not selection from many.",
        'distractor_explanations': {
            'これ': "これは あなたのですか would be a yes/no question about ONE specific bag near the speaker. The question is asking the listener to pick one out of many.",
            'それ': "それは あなたのですか would be a yes/no question about ONE specific bag near the listener. The question is asking selection from a group.",
            'あれ': "あれは あなたのですか would be a yes/no question about ONE specific bag far away. The question is asking selection from a group.",
        },
    },
}


def main():
    with QUESTIONS_PATH.open('r', encoding='utf-8') as f:
        data = json.load(f)

    fixed = []
    skipped = []
    for q in data['questions']:
        qid = q.get('id')
        if qid not in FIXES:
            continue
        patch = FIXES[qid]
        # Idempotency check: if question_ja already matches the new value,
        # this question has already been fixed.
        if q.get('question_ja') == patch['question_ja']:
            skipped.append(qid)
            continue
        q['question_ja'] = patch['question_ja']
        q['prompt_ja'] = patch['prompt_ja']
        q['explanation_en'] = patch['explanation_en']
        q['distractor_explanations'] = patch['distractor_explanations']
        # Mark as manually reviewed.
        q['auto'] = False
        fixed.append(qid)

    if fixed:
        with QUESTIONS_PATH.open('w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    print(f'Fixed: {fixed}')
    print(f'Skipped (already fixed): {skipped}')
    missing = set(FIXES) - set(fixed) - set(skipped)
    if missing:
        print(f'WARNING - not found in questions.json: {sorted(missing)}')


if __name__ == '__main__':
    main()
