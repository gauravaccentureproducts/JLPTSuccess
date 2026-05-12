"""P4 #23 + #25 — Generate cloze + production drill questions
from existing grammar / vocab data.

Outputs (written into data/questions.json's questions[] array, with
new ids prefixed):
  cloze-XXXX        cloze-deletion drills from grammar examples
                    (blank the example's key term)
  production-XXXX   production drills from vocab entries
                    (show English gloss, expect Japanese)

The existing drill engine (js/drill.js) already understands:
  type: 'cloze'       — sentence with ()(blank) placeholder + type input
  type: 'production'  — prompt + free-type input
gradeQuestion() normalizes whitespace + punctuation + case.

Schema (matches existing questions.json entries):
  {
    id, type, grammarPatternId (or vocabId for production),
    stem, prompt_en, correctAnswer, acceptedAnswers,
    explanation_en
  }

Idempotent: regenerates from source data every run. Re-running
replaces all cloze-* / production-* entries.
"""
from __future__ import annotations
import io, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def build_cloze_drills(grammar):
    """For each grammar pattern, pick the first 1-2 examples and
    generate a cloze drill by blanking out the pattern occurrence."""
    out = []
    for p in grammar:
        pattern_id = p.get('id')
        pattern_ja = p.get('pattern_ja') or p.get('pattern')
        if not pattern_id or not pattern_ja:
            continue
        examples = p.get('examples') or []
        for i, ex in enumerate(examples[:2]):
            ja = ex.get('ja') or ''
            if not ja:
                continue
            # Find a meaningful substring to blank out. Strategy:
            #   - If the example contains the pattern_ja literal, blank that
            #   - Otherwise skip (we can't reliably identify the keyword)
            blank_target = pattern_ja
            if blank_target not in ja:
                # Try without trailing form-markers like 〜
                cleaned = pattern_ja.replace('〜', '').replace('～', '').strip()
                if cleaned and cleaned in ja:
                    blank_target = cleaned
                else:
                    continue
            stem = ja.replace(blank_target, '（　　）', 1)
            qid = f'cloze-{pattern_id}-ex{i}'
            out.append({
                'id': qid,
                'type': 'cloze',
                'grammarPatternId': pattern_id,
                'stem': stem,
                'prompt_en': f'Fill the blank: {ex.get("translation_en", "")}',
                'correctAnswer': blank_target,
                'acceptedAnswers': [blank_target],
                'explanation_en': p.get('meaning_en') or p.get('summary') or '',
                'auto_generated': True,
            })
    return out


def build_production_drills(vocab, limit_per_pos=None):
    """For each vocab entry, generate a production drill: show
    English gloss → expect the Japanese form typed.

    Strategy:
      - prompt_en = vocab gloss
      - correctAnswer = vocab.form (canonical)
      - acceptedAnswers = [form, reading] (both kanji and kana)
      - acceptedAnswers also includes the FIRST example's ja form
        (for sentence-level production drills, optional)
    """
    out = []
    pos_count = {}
    for e in vocab:
        pos = e.get('pos', '')
        if limit_per_pos and pos_count.get(pos, 0) >= limit_per_pos:
            continue
        pos_count[pos] = pos_count.get(pos, 0) + 1
        gloss = e.get('gloss')
        form = e.get('form')
        reading = e.get('reading')
        if not gloss or not form:
            continue
        # Build accepted variants
        accepted = list({form, reading} - {None, ''})
        qid = f'production-{e["id"]}'
        out.append({
            'id': qid,
            'type': 'production',
            'vocabId': e['id'],
            'stem': '',  # no stem; prompt_en is the cue
            'prompt_en': f'Type the Japanese for: {gloss}',
            'correctAnswer': form,
            'acceptedAnswers': accepted,
            'explanation_en': gloss,
            'auto_generated': True,
        })
    return out


def main() -> int:
    grammar_fp = ROOT / 'data' / 'grammar.json'
    vocab_fp = ROOT / 'data' / 'vocab.json'
    out_fp = ROOT / 'data' / 'drills_auto.json'

    grammar = json.loads(grammar_fp.read_text(encoding='utf-8'))['patterns']
    vocab = json.loads(vocab_fp.read_text(encoding='utf-8'))['entries']

    cloze = build_cloze_drills(grammar)
    production = build_production_drills(vocab)

    payload = {
        '_meta': {
            'source': 'tools/build_cloze_production_drills.py',
            'generated_from': ['data/grammar.json', 'data/vocab.json'],
            'cloze_count': len(cloze),
            'production_count': len(production),
        },
        'questions': cloze + production,
    }
    out_fp.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print(f'Wrote {out_fp.relative_to(ROOT)}:')
    print(f'  Cloze drills:      {len(cloze)}')
    print(f'  Production drills: {len(production)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
