"""Iteration 3 fixes: English-leak in stems + bilingual choice gloss.

Findings:
1. bunpou-7.* (Q91-Q100, Mondai 3) all have stem_html = "→ blank [N]"
   where "blank" is English leaked into a Japanese stem field. The
   stem in this format is a stub pointing to a numbered blank in the
   passage above. Replace "blank" with "[N]番" Japanese form, or
   simplify to "→ [N]".

2. dokkai-1.2 Q2 choice [1] is "インド (India)" - bilingual gloss
   in a Japanese choice. Drop "(India)".

Idempotent.
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
# 1. Bunpou Mondai 3 stems: "→ blank [N]" → "→ [N]番"
# ============================================================================
def fix_bunpou_mondai3() -> None:
    p_path = ROOT / 'data/papers/bunpou/paper-7.json'
    paper = json.loads(p_path.read_text(encoding='utf-8'))
    modified = False
    for q in paper['questions']:
        stem = q.get('stem_html', '')
        m = re.match(r'→ blank \[(\d+)\]', stem)
        if m:
            new_stem = f'→ [{m.group(1)}]番'
            if q['stem_html'] != new_stem:
                q['stem_html'] = new_stem
                modified = True
                changes.append(f'paper-7.json {q["id"]}: stem "→ blank [{m.group(1)}]" -> "→ [{m.group(1)}]番"')
    if modified:
        p_path.write_text(json.dumps(paper, ensure_ascii=False, indent=2), encoding='utf-8')

    # Mirror to MD source
    md_path = ROOT / 'KnowledgeBank/bunpou_questions_n5.md'
    text = md_path.read_text(encoding='utf-8')
    new_text = re.sub(r'→ blank \[(\d+)\]', r'→ [\1]番', text)
    if new_text != text:
        md_path.write_text(new_text, encoding='utf-8')
        changes.append('bunpou_questions_n5.md: replaced "blank" stub with Japanese [N]番')


# ============================================================================
# 2. dokkai-1.2 Q2 choice [1] "インド (India)" → "インド"
# ============================================================================
def fix_dokkai_india() -> None:
    p_path = ROOT / 'data/papers/dokkai/paper-1.json'
    paper = json.loads(p_path.read_text(encoding='utf-8'))
    modified = False
    for q in paper['questions']:
        if q['id'] != 'dokkai-1.2':
            continue
        choices = q.get('choices', [])
        for i, c in enumerate(choices):
            if c == 'インド (India)':
                choices[i] = 'インド'
                modified = True
                changes.append(f'paper-1.json dokkai-1.2 choice [{i+1}]: "インド (India)" -> "インド"')
        if modified:
            q['choices'] = choices
    if modified:
        p_path.write_text(json.dumps(paper, ensure_ascii=False, indent=2), encoding='utf-8')

    # MD mirror
    md_path = ROOT / 'KnowledgeBank/dokkai_questions_n5.md'
    text = md_path.read_text(encoding='utf-8')
    if 'インド (India)' in text:
        text = text.replace('インド (India)', 'インド')
        md_path.write_text(text, encoding='utf-8')
        changes.append('dokkai_questions_n5.md: stripped "(India)" gloss')


def main() -> int:
    fix_bunpou_mondai3()
    fix_dokkai_india()
    if not changes:
        print('No changes (already in fixed state).')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
