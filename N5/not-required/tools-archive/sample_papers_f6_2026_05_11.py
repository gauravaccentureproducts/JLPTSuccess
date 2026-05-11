"""F-6 (legal-vetting 2026-05-11): random sample 10 papers questions for
manual paraphrasing audit. Reproducible via seed.

Run from N5/ root:
    python not-required/tools-archive/sample_papers_f6_2026_05_11.py
"""
import json
import random
from pathlib import Path

random.seed(0xF6)  # reproducible

papers = sorted(Path("data/papers").rglob("paper-*.json"))
all_qs = []
for pp in papers:
    try:
        d = json.loads(pp.read_text(encoding="utf-8"))
        for q in d.get("questions", []):
            all_qs.append((pp.as_posix(), q))
    except Exception:
        continue

print(f"papers files: {len(papers)}  total questions: {len(all_qs)}")
print()
sample = random.sample(all_qs, 10)
for i, (src, q) in enumerate(sample, 1):
    stem = q.get("stem") or q.get("prompt") or q.get("question") or ""
    opts = q.get("options") or q.get("choices") or []
    qid = q.get("id") or q.get("question_id") or "?"
    rationale = q.get("rationale") or q.get("explanation") or q.get("rationale_en") or ""
    print(f"=== {i}. {src} :: {qid} ===")
    print(f"  stem: {stem[:200]}")
    if isinstance(opts, list) and opts:
        for j, o in enumerate(opts[:4]):
            text = o.get("text", o) if isinstance(o, dict) else o
            print(f"  opt[{j}]: {str(text)[:120]}")
    if rationale:
        print(f"  rationale: {str(rationale)[:200]}")
    print()
