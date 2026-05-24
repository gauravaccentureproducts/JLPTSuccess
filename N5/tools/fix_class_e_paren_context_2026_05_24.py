"""Class E refactor: 27 common_mistakes rows have a JA sentence followed
by an English parenthetical context annotation in the `wrong` field
(e.g. "りんごは いくらですか。 (when asking quantity, not price)").

The parenthetical is essential teaching context — without it, the JA
sentence reads as grammatically valid — but having it inside the wrong
field is structurally awkward and clutters the rendered HTML.

Refactor: lift the parenthetical out of `wrong` and prepend it to `why`
as "Context: <parenthetical>. <existing why>". Cleans up the display
without losing pedagogical content.

Match rule: parenthetical at the end of `wrong` containing at least one
Latin letter (so we don't accidentally split JA-only parentheticals).

Backup: data/grammar.json -> data/grammar.json.bak_2026_05_24_class_e
"""
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_JSON = ROOT / "data" / "grammar.json"
INDEX_JSON = ROOT / "data" / "index.json"
BACKUP = ROOT / "data" / "grammar.json.bak_2026_05_24_class_e"

# Captures: leading JA sentence + trailing English parenthetical.
# Parenthetical must contain at least one Latin letter to qualify as
# "context annotation" rather than a JA parenthetical that legitimately
# belongs in the sentence.
PAREN_RE = re.compile(r"^(?P<ja>.+?)\s*\((?P<paren>[^)]*[a-zA-Z][^)]*)\)\s*$")


def refactor_row(row: dict) -> bool:
    """Try to lift a trailing English paren from the `wrong` field of `row`
    into the `why` field. Returns True if changed."""
    wrong = row.get("wrong") or ""
    m = PAREN_RE.match(wrong)
    if not m:
        return False
    ja = m.group("ja").rstrip()
    paren = m.group("paren").strip()
    # Skip empty paren or paren that's just punctuation
    if not paren:
        return False
    why = row.get("why") or ""
    # Prepend the context note. Use sentence-cased framing.
    if why:
        new_why = f"Context: {paren}. {why}"
    else:
        new_why = f"Context: {paren}."
    row["wrong"] = ja
    row["why"] = new_why
    return True


def main():
    # Backup
    if BACKUP.exists():
        idx = 2
        while True:
            cand = ROOT / "data" / f"grammar.json.bak_2026_05_24_class_e_v{idx}"
            if not cand.exists():
                shutil.copy2(GRAMMAR_JSON, cand)
                print(f"Backup -> {cand.name}")
                break
            idx += 1
    else:
        shutil.copy2(GRAMMAR_JSON, BACKUP)
        print(f"Backup -> {BACKUP.name}")

    g = json.loads(GRAMMAR_JSON.read_text(encoding="utf-8"))

    refactored = []
    for p in g["patterns"]:
        for i, m in enumerate(p.get("common_mistakes") or []):
            # Skip register_variant rows (different schema)
            if m.get("kind") == "register_variant":
                continue
            if refactor_row(m):
                refactored.append((p["id"], i, m["wrong"][:40], (m["why"] or "")[:60]))
        for i, w in enumerate(p.get("wrong_corrected_pair") or []):
            if w.get("kind") == "register_variant":
                continue
            if refactor_row(w):
                refactored.append((p["id"], f"wcp[{i}]", w["wrong"][:40], (w["why"] or "")[:60]))

    GRAMMAR_JSON.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
    with open(GRAMMAR_JSON, "rb") as fh:
        lf_size = len(fh.read().replace(b"\r\n", b"\n"))
    print(f"\nWrote grammar.json (LF-normalised {lf_size} bytes)")

    # Update index.json size_bytes
    idx_doc = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    for f in idx_doc.get("files", []):
        if f.get("path") == "data/grammar.json":
            old = f.get("size_bytes")
            f["size_bytes"] = lf_size
            print(f"Updated index.json size_bytes: {old} -> {lf_size}")
            break
    INDEX_JSON.write_text(json.dumps(idx_doc, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"\nRefactored {len(refactored)} rows:")
    for pid, idx, w, why in refactored:
        print(f"  {pid} cm[{idx}]: wrong='{w}...' why='{why}...'")


if __name__ == "__main__":
    main()
