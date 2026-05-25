#!/usr/bin/env python3
"""Class-aware MCQ ambiguity sweep. Detects ambiguity in non-verb-ending
MCQ classes (PARTICLE, QUESTION_WORD, DEMONSTRATIVE)."""
import json
from collections import defaultdict
from pathlib import Path

QUESTION_WORDS_SET = {'なに','何','だれ','誰','どこ','いつ','どう','どの','どれ',
                      'どちら','いくら','いくつ','なんで','なぜ','どうして'}
DEICTIC_MARKERS = ['じぶんの 手', '友だちの', 'とおく', 'むこう', 'はなれた',
                   'みせる', 'ゆびさ', 'ある へや', 'つくえの上', 'がっこうの']


def main():
    q = json.loads(Path('data/questions.json').read_text(encoding='utf-8'))
    findings = defaultdict(list)
    for it in q['questions']:
        if it.get('type') != 'mcq': continue
        ch = it.get('choices') or []
        if not ch: continue
        stem = it.get('question_ja','') or ''
        ca = it.get('correctAnswer')
        pid = it.get('grammarPatternId')

        # A1: question-word + が/は both in choices
        if 'が' in ch and 'は' in ch:
            if any(qw in stem for qw in QUESTION_WORDS_SET):
                findings['A1_qword_ga_wa'].append({'id': it['id'], 'pid': pid, 'stem': stem[:70], 'choices': ch, 'ca': ca})

        # B1: multiple question words in choices, all common types
        qw_in = [c for c in ch if c in QUESTION_WORDS_SET]
        if len(qw_in) >= 3:
            findings['B1_multi_qword'].append({'id': it['id'], 'pid': pid, 'stem': stem[:70], 'choices': ch, 'ca': ca, 'qws': qw_in})

        # C1: deictic (これ/それ/あれ) without spatial cue
        deictic_in = [c for c in ch if c in {'これ','それ','あれ'}]
        if len(deictic_in) >= 2 and not any(m in stem for m in DEICTIC_MARKERS):
            findings['C1_deictic_no_cue'].append({'id': it['id'], 'pid': pid, 'stem': stem[:70], 'choices': ch, 'ca': ca})

    for cls in ['A1_qword_ga_wa', 'B1_multi_qword', 'C1_deictic_no_cue']:
        items = findings.get(cls, [])
        print(f'=== {cls}: {len(items)} ===')
        for x in items[:8]:
            print(f'  {x["id"]} ({x["pid"]}): {x["stem"]}')
            print(f'    choices={x["choices"]}, ca={x["ca"]!r}')
        print()


if __name__ == '__main__':
    main()
