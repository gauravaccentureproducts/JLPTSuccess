#!/usr/bin/env python3
"""
Horizontal MCQ ambiguity sweep across choice-set classes.
"""
import json
from collections import defaultdict
from pathlib import Path

PARTICLES = {'は','が','を','に','で','と','の','も','へ','や','か','よ','ね',
             'から','まで','だけ','しか','ぐらい','ごろ','など','ば','けど',
             'し','ても','のに','のだ'}
QUESTION_WORDS = {'なに','何','だれ','誰','どこ','いつ','どう','どの','どれ',
                  'どちら','いくら','いくつ','なんで','なぜ','どうして','なんじ',
                  'なんがつ','なんにち','なんにん','なんびき'}
DEMONSTRATIVES = {'これ','それ','あれ','どれ','この','その','あの','どの',
                  'ここ','そこ','あそこ','どこ','こちら','そちら','あちら',
                  'どちら','こう','そう','ああ','どう'}
VERB_ENDS = {'ます','ません','ました','ませんでした','ましょう','ましょうか',
             'ますか','ませんか','たい','たくない','でした','ながら','ない',
             'でしょう'}


def classify(ch):
    if not ch: return 'EMPTY'
    if all(c in PARTICLES for c in ch): return 'PARTICLE'
    if all(c in QUESTION_WORDS for c in ch): return 'QUESTION_WORD'
    if all(c in DEMONSTRATIVES for c in ch): return 'DEMONSTRATIVE'
    if all(c in VERB_ENDS for c in ch): return 'VERB_ENDING'
    return 'OTHER'


def main():
    q = json.loads(Path('data/questions.json').read_text(encoding='utf-8'))
    by_class = defaultdict(list)
    for it in q['questions']:
        if it.get('type') != 'mcq': continue
        by_class[classify(it.get('choices') or [])].append(it)
    print('Class distribution (questions.json MCQ):')
    for cls, items in sorted(by_class.items(), key=lambda x: -len(x[1])):
        print(f'  {cls}: {len(items)}')
    print()
    print('PARTICLE samples (first 8):')
    for p in by_class.get('PARTICLE', [])[:8]:
        print(f'  {p["id"]} ({p.get("grammarPatternId")}): {p.get("question_ja","")[:60]}')
        print(f'    choices={p.get("choices")}, ca={p.get("correctAnswer")!r}')
    print()
    print('QUESTION_WORD samples (first 8):')
    for p in by_class.get('QUESTION_WORD', [])[:8]:
        print(f'  {p["id"]} ({p.get("grammarPatternId")}): {p.get("question_ja","")[:60]}')
        print(f'    choices={p.get("choices")}, ca={p.get("correctAnswer")!r}')
    print()
    print('DEMONSTRATIVE samples (first 5):')
    for p in by_class.get('DEMONSTRATIVE', [])[:5]:
        print(f'  {p["id"]} ({p.get("grammarPatternId")}): {p.get("question_ja","")[:60]}')
        print(f'    choices={p.get("choices")}, ca={p.get("correctAnswer")!r}')


if __name__ == '__main__':
    main()
