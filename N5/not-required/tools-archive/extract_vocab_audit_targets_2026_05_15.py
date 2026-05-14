"""Extract C1 (template-leak) + C2 (within-dup) + C3 (real) targets for
authoring replacement sentences. Writes JSON to:
  not-required/tools-archive/_vocab_fix_targets_2026_05_15.json
"""
import json, re
from pathlib import Path
from collections import OrderedDict

VOCAB = Path("data/vocab.json")

d = json.loads(VOCAB.read_text(encoding="utf-8"))
entries = d["entries"]

c1, c2 = [], []
for e in entries:
    eid = e.get("id", "?")
    exs = e.get("examples", [])
    # C1: template-leak ja at any index
    for i, ex in enumerate(exs):
        ja = ex.get("ja", "").strip()
        if re.fullmatch(r".{1,10}を\s*見ました。?", ja):
            c1.append({
                "id": eid,
                "form": e.get("form"),
                "reading": e.get("reading"),
                "gloss": e.get("gloss"),
                "pos": e.get("pos"),
                "section": e.get("section"),
                "idx": i,
                "ja": ja,
                "en": ex.get("translation_en", ""),
                "all_ja": [x.get("ja") for x in exs],
            })
    # C2: within-entry duplicates
    seen = {}
    for i, ex in enumerate(exs):
        ja = ex.get("ja", "").strip()
        if not ja:
            continue
        if ja in seen:
            c2.append({
                "id": eid,
                "form": e.get("form"),
                "reading": e.get("reading"),
                "gloss": e.get("gloss"),
                "pos": e.get("pos"),
                "first_idx": seen[ja],
                "dup_idx": i,
                "ja": ja,
                "en": ex.get("translation_en", ""),
                "all_ja": [x.get("ja") for x in exs],
            })
        else:
            seen[ja] = i

out = {"c1_template_leak": c1, "c2_within_dup": c2}
Path("not-required/tools-archive/_vocab_fix_targets_2026_05_15.json").write_text(
    json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8"
)
print(f"C1 template-leak rows: {len(c1)}")
print(f"C2 within-dup rows:    {len(c2)}")
