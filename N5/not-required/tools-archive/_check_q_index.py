import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

for fname in [('goi/paper-6.json', 11), ('goi/paper-7.json', 7)]:
    f, idx = fname
    d = json.loads((ROOT / 'data' / 'papers' / f).read_text(encoding='utf-8'))
    q = d['questions'][idx]
    print(f'\n{f} questions[{idx}]:')
    print(f'  id: {q.get("id")}')
    print(f'  rationale_hi: {q.get("rationale_hi", "")[:200]}')
