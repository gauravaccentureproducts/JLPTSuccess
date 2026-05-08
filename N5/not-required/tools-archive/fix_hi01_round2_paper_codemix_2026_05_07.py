"""Apply the HI-02 round-2 substitution glossary to paper-files Hindi text.

Walks data/papers/**/*.json and applies the same glossary used in
fix_hi02_round2_codemix_questions_2026_05_07.py to clean residual
English in the freshly-translated rationale_hi / summary_hi fields.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Load rules from the round-2 sweep
def load_rules(filename, attr):
    path = ROOT / 'not-required' / 'tools-archive' / filename
    src = path.read_text(encoding='utf-8')
    src = re.sub(r'^sys\.stdout\s*=.*$', '', src, flags=re.MULTILINE)
    src = re.sub(r"if __name__ == '__main__':[\s\S]*$", '', src)
    src = re.sub(r"def main\(\):[\s\S]*?(?=\n\S|\Z)", '', src)
    ns = {'__file__': str(path), '__name__': '_loaded'}
    exec(compile(src, filename, 'exec'), ns)
    return ns.get(attr, [])

RULES = load_rules('fix_hi02_round2_codemix_questions_2026_05_07.py', 'SUBSTITUTIONS')


def has_devanagari(s: str) -> bool:
    return any('ऀ' <= ch <= 'ॿ' for ch in s)


def apply_subs(value: str) -> str:
    if not isinstance(value, str) or not has_devanagari(value):
        return value
    JP = re.compile(r'[ぁ-ゖァ-ヺ一-龯]+')
    jp_protected = []

    def protect_jp(m):
        idx = len(jp_protected)
        jp_protected.append(m.group(0))
        return f'\x00JP{idx}\x00'

    text = JP.sub(protect_jp, value)
    PAREN_EN = re.compile(r'\(([^()]*[a-zA-Z][^()]*)\)')
    paren_protected = []

    def protect_paren(m):
        content = m.group(1)
        if any('ऀ' <= ch <= 'ॿ' for ch in content):
            return m.group(0)
        idx = len(paren_protected)
        paren_protected.append(m.group(0))
        return f'\x00PR{idx}\x00'

    text = PAREN_EN.sub(protect_paren, text)
    for pat, repl in RULES:
        text = re.sub(pat, repl, text, flags=re.IGNORECASE)
    for i, c in enumerate(paren_protected):
        text = text.replace(f'\x00PR{i}\x00', c)
    for i, jp in enumerate(jp_protected):
        text = text.replace(f'\x00JP{i}\x00', jp)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\s+([।,;:.])', r'\1', text)
    text = re.sub(r'\.(\s|$)', r'।\1', text)
    return text.strip()


papers_dir = ROOT / 'data' / 'papers'
files_changed = 0
total_subs = 0
for pf in papers_dir.rglob('*.json'):
    if pf.name == 'manifest.json':
        continue
    data = json.loads(pf.read_text(encoding='utf-8'))
    changed = False
    for q in data.get('questions', []):
        rh = q.get('rationale_hi')
        if isinstance(rh, str):
            new_rh = apply_subs(rh)
            if new_rh != rh:
                q['rationale_hi'] = new_rh
                changed = True
                total_subs += 1
    for p in data.get('passages', []):
        sh = p.get('summary_hi')
        if isinstance(sh, str):
            new_sh = apply_subs(sh)
            if new_sh != sh:
                p['summary_hi'] = new_sh
                changed = True
                total_subs += 1
    if changed:
        pf.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        files_changed += 1

print(f'Files changed: {files_changed}')
print(f'Fields changed: {total_subs}')
