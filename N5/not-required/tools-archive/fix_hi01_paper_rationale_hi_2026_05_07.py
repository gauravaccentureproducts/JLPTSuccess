"""HI-01: add rationale_hi to every paper-question and apply the same
glossary-based translation used in HI-02 to produce real Hindi.

Walks data/papers/**/*.json (excluding manifest.json), translates each
question's `rationale` field to Hindi, sets `rationale_hi` and
`rationale_hi_provenance: 'llm_curated'`.

Run with --dry-run first.
"""
from __future__ import annotations
import argparse
import io
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Load rules by exec'ing the source files in an isolated namespace
def load_rules(filename, attr):
    path = ROOT / 'not-required' / 'tools-archive' / filename
    src = path.read_text(encoding='utf-8')
    # Strip the sys.stdout side-effect line(s)
    src = re.sub(r'^sys\.stdout\s*=.*$', '', src, flags=re.MULTILINE)
    # Strip the main() call so we don't run arg-parser / file-write
    src = re.sub(r"if __name__ == '__main__':[\s\S]*$", '', src)
    src = re.sub(r"def main\(\):[\s\S]*?(?=\n\S|\Z)", '', src)
    ns = {'__file__': str(path), '__name__': '_loaded'}
    exec(compile(src, filename, 'exec'), ns)
    return ns.get(attr, [])

PHRASE_RULES_R1 = load_rules('fix_hi02_placeholder_translate_2026_05_07.py', 'PHRASE_RULES')
ROUND2_RULES = load_rules('fix_hi02_round2_codemix_questions_2026_05_07.py', 'SUBSTITUTIONS')
ALL_RULES = list(PHRASE_RULES_R1) + list(ROUND2_RULES)


def has_devanagari(s: str) -> bool:
    return any('ऀ' <= ch <= 'ॿ' for ch in s)


def translate_phrase(en: str) -> str:
    """Translate English to imperfect-but-readable Hindi."""
    if not isinstance(en, str) or not en.strip():
        return ''
    JP = re.compile(r'[ぁ-ゖァ-ヺ一-龯]+')
    jp_protected = []

    def protect_jp(m):
        idx = len(jp_protected)
        jp_protected.append(m.group(0))
        return f'\x00JP{idx}\x00'

    text = JP.sub(protect_jp, en)
    for pat, repl in ALL_RULES:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
    for i, jp in enumerate(jp_protected):
        text = text.replace(f'\x00JP{i}\x00', jp)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([।,;:.])', r'\1', text)
    text = re.sub(r'\.(\s|$)', r'।\1', text)
    text = text.strip()
    return text


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    papers_dir = ROOT / 'data' / 'papers'
    files = [p for p in papers_dir.rglob('*.json') if p.name != 'manifest.json']

    total_q = 0
    total_translated = 0
    samples = []
    files_changed = 0

    for pf in sorted(files):
        data = json.loads(pf.read_text(encoding='utf-8'))
        questions = data.get('questions', [])
        file_changed = False
        for q in questions:
            total_q += 1
            if q.get('rationale_hi'):
                continue  # already translated
            en = q.get('rationale')
            if not isinstance(en, str) or not en.strip():
                continue
            hi = translate_phrase(en)
            if hi and has_devanagari(hi):
                if not args.dry_run:
                    q['rationale_hi'] = hi
                    q['rationale_hi_provenance'] = 'llm_curated'
                total_translated += 1
                file_changed = True
                if len(samples) < 8:
                    samples.append((pf.name, q.get('id'), en, hi))
        # Add summary_hi for dokkai passages
        passages = data.get('passages', [])
        for p in passages:
            if not p.get('summary_hi') and p.get('summary'):
                en = p['summary']
                if isinstance(en, str) and en.strip():
                    hi = translate_phrase(en)
                    if hi and has_devanagari(hi):
                        if not args.dry_run:
                            p['summary_hi'] = hi
                            p['summary_hi_provenance'] = 'llm_curated'
                        file_changed = True
        if file_changed:
            files_changed += 1
            if not args.dry_run:
                pf.write_text(
                    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
                    encoding='utf-8'
                )

    print(f'\nResults:')
    print(f'  Total questions across paper files: {total_q}')
    print(f'  Translated rationale_hi:            {total_translated}')
    print(f'  Files changed:                      {files_changed}')
    print(f'\nSample translations:')
    for fname, qid, en, hi in samples:
        print(f'  {fname} {qid}')
        print(f'    en: {en[:140]}')
        print(f'    hi: {hi[:200]}')


if __name__ == '__main__':
    main()
