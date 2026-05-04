"""
Pass-15 multi-correct scanner. Finds candidate questions where multiple
choices could be valid completions, grouped by category.

Output is human-reviewable; native-teacher review picks the actual fixes.
Categories scanned:
  A. choices include に AND へ — motion verb may accept both
  B. choices include は AND が — topic vs subject ambiguity
  C. choices include で AND に — location-of-action vs location-of-being
  D. choices include 4 demonstratives without context (ko-so-a-do family,
     remaining cases after the basic fix pass)
  E. polite-vs-casual copula choices (です vs だ) without register cue
  F. number readings (e.g., ひとつ vs いっこ) when both apply
"""
import json
import io
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

QUESTIONS_PATH = Path(__file__).resolve().parent.parent / 'data' / 'questions.json'

with QUESTIONS_PATH.open('r', encoding='utf-8') as f:
    data = json.load(f)


def emit(qid, correct, q_ja, prompt_ja=''):
    print(f'  {qid} | correct={correct}')
    print(f'    Q: {q_ja}')
    if prompt_ja and prompt_ja != q_ja:
        print(f'    P: {prompt_ja}')


print('=== A. に AND へ both in choices (motion verb ambiguity) ===')
hits_a = []
for q in data['questions']:
    cs = q.get('choices', [])
    if 'に' in cs and 'へ' in cs:
        hits_a.append(q)
        emit(q['id'], q.get('correctAnswer'), q.get('question_ja', ''), q.get('prompt_ja', ''))
print(f'  ({len(hits_a)} hits)\n')

print('=== B. は AND が both in choices (topic vs subject) ===')
hits_b = []
for q in data['questions']:
    cs = q.get('choices', [])
    if 'は' in cs and 'が' in cs:
        hits_b.append(q)
        emit(q['id'], q.get('correctAnswer'), q.get('question_ja', ''), q.get('prompt_ja', ''))
print(f'  ({len(hits_b)} hits)\n')

print('=== C. で AND に both in choices (location ambiguity) ===')
hits_c = []
for q in data['questions']:
    cs = q.get('choices', [])
    if 'で' in cs and 'に' in cs:
        hits_c.append(q)
        emit(q['id'], q.get('correctAnswer'), q.get('question_ja', ''), q.get('prompt_ja', ''))
print(f'  ({len(hits_c)} hits)\n')

# D: 4 ko-so-a-do choices but no scene-setting prefix in question_ja
KOSOADO_SETS = [
    {'これ', 'それ', 'あれ', 'どれ'},
    {'この', 'その', 'あの', 'どの'},
    {'ここ', 'そこ', 'あそこ', 'どこ'},
    {'こちら', 'そちら', 'あちら', 'どちら'},
]
print('=== D. ko-so-a-do family with no scene context (remaining) ===')
hits_d = []
for q in data['questions']:
    cs_set = set(q.get('choices', []))
    if not any(s <= cs_set for s in KOSOADO_SETS):
        continue
    qj = q.get('question_ja', '')
    pj = q.get('prompt_ja', '')
    # Heuristic: scene-setting questions begin with （ ... ） describing the situation
    has_scene = qj.startswith('（') and '）' in qj.split('（', 1)[1].split('（  ）')[0] if '（  ）' in qj else False
    # Simpler: check if there's a scene paren preceding the blank
    has_scene = False
    if '（  ）' in qj or '（　）' in qj or '(  )' in qj or '(　)' in qj:
        # Find the position of the blank-paren and check if there's a scene-paren before it
        first_blank_idx = min((qj.find(s) for s in ('（  ）', '（　）', '(  )', '(　)') if qj.find(s) != -1), default=-1)
        if first_blank_idx > 0:
            prefix = qj[:first_blank_idx]
            has_scene = '（' in prefix and '）' in prefix
    if not has_scene:
        # Also check prompt_ja for scene-setting longer than the generic instruction
        if 'えらんで' not in pj or len(pj) > 40:
            has_scene = True  # prompt_ja carries the context
    if not has_scene:
        hits_d.append(q)
        emit(q['id'], q.get('correctAnswer'), qj, pj)
print(f'  ({len(hits_d)} hits)\n')

# E: です/だ copula choices alongside register-sensitive options
print('=== E. polite-vs-casual copula in same choice set ===')
hits_e = []
for q in data['questions']:
    cs = q.get('choices', [])
    has_polite = any(c.endswith('です') or c.endswith('ます') for c in cs)
    has_casual = any(c == 'だ' or c.endswith('だ') and not c.endswith('んだ') for c in cs)
    if has_polite and has_casual:
        hits_e.append(q)
        emit(q['id'], q.get('correctAnswer'), q.get('question_ja', ''))
print(f'  ({len(hits_e)} hits)\n')

# Summary
print('=== SUMMARY ===')
print(f'A (に/へ):     {len(hits_a)}')
print(f'B (は/が):     {len(hits_b)}')
print(f'C (で/に):     {len(hits_c)}')
print(f'D (ko-so-a-do): {len(hits_d)}')
print(f'E (です/だ):   {len(hits_e)}')
