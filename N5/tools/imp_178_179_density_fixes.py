"""IMP-178 + IMP-179 — Density verification fixes.

IMP-179 (Density-8): 13 lookalike-cluster asymmetric edges.
  Kanji X claims partner Y as lookalike, but Y doesn't claim X back.
  Fix by adding the back-edge to make all clusters bidirectional.

IMP-178 (Density-7): 108 paper-Q without grammarPatternId.
  108 of 402 paper questions don't link to the grammar pattern they
  test. Derive by:
    1. For each unlinked question, scan its stem + correct-answer + choices
    2. Match against grammar.examples[*].ja using substring containment
    3. If a clean unique match exists, set grammarPatternId
    4. Mark provenance auto_derived; leave blanks for ambiguous matches
       (those need hand-review).
"""
import json
import io
import sys
import os
import shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

KANJI = "data/kanji.json"
KANJI_BAK = "data/kanji.json.bak_2026_05_13_imp_179_lookalike_symmetry"


def fix_imp_179():
    shutil.copy2(KANJI, KANJI_BAK)
    K_raw = json.load(open(KANJI, encoding="utf-8"))
    K = K_raw["entries"]

    by_glyph = {k["glyph"]: k for k in K}

    def extract_partner_glyphs(lookalikes):
        out = []
        for la in lookalikes or []:
            if isinstance(la, str):
                out.append(la)
            elif isinstance(la, dict):
                g = la.get("glyph") or la.get("kanji") or ""
                if g:
                    out.append(g)
        return out

    fixes = 0
    for k in K:
        glyph = k["glyph"]
        partners = extract_partner_glyphs(k.get("lookalikes"))
        for p_glyph in partners:
            if p_glyph not in by_glyph:
                continue
            p_entry = by_glyph[p_glyph]
            p_partners = extract_partner_glyphs(p_entry.get("lookalikes"))
            if glyph not in p_partners:
                # Add back-edge using the same schema shape as existing entries
                existing = p_entry.get("lookalikes") or []
                # Detect schema: list-of-str vs list-of-dict
                if existing and isinstance(existing[0], dict):
                    # Find the parent (k) entry's lookalike that points back; reuse note shape
                    # Simplest: create a dict with just glyph + auto note
                    new_entry = {
                        "glyph": glyph,
                        "note": f"Lookalike pair with {glyph} (symmetric back-edge).",
                        "audit_wave": "imp-179-symmetry-2026-05-13",
                    }
                else:
                    new_entry = glyph
                p_entry.setdefault("lookalikes", []).append(new_entry)
                if "lookalikes_provenance" not in p_entry:
                    p_entry["lookalikes_provenance"] = "auto_derived"
                fixes += 1
                print(f"  back-edge added: {p_glyph} <- {glyph}")

    with open(KANJI, "w", encoding="utf-8") as f:
        json.dump(K_raw, f, ensure_ascii=False, indent=2)
    print(f"IMP-179: {fixes} back-edges added")
    return fixes


def fix_imp_178():
    """Attempt to derive grammarPatternId for the 108 unlinked paper Qs.

    Strategy: load all grammar patterns + their example JA texts. For each
    unlinked question, check if any example's JA text appears as a
    substring in the question stem (or vice-versa). If one unique match,
    assign grammarPatternId. Otherwise leave for hand-review.
    """
    G = json.load(open("data/grammar.json", encoding="utf-8"))["patterns"]
    # Build (example_text -> pattern_id) index. Sort by length desc so
    # longest matches win.
    examples_index = []
    for p in G:
        for ex in (p.get("examples") or []):
            ja = (ex.get("ja") or "").strip()
            if len(ja) >= 4:  # skip trivial
                examples_index.append((ja, p["id"]))
    examples_index.sort(key=lambda x: -len(x[0]))

    total_q = 0
    initial_linked = 0
    newly_linked = 0
    ambiguous = 0
    no_match = 0
    files_modified = set()

    for root, dirs, files in os.walk("data/papers"):
        for fname in files:
            if not fname.endswith(".json") or fname == "manifest.json":
                continue
            path = os.path.join(root, fname)
            try:
                data = json.load(open(path, encoding="utf-8"))
            except:
                continue
            if not isinstance(data, dict):
                continue
            qs = data.get("questions") or data.get("items") or []
            file_changed = False
            for q in qs:
                if not isinstance(q, dict):
                    continue
                total_q += 1
                if q.get("grammarPatternId"):
                    initial_linked += 1
                    continue
                # Build search text from stem + correct + choices
                pieces = []
                for fld in ("stem", "question", "stem_ja", "prompt_ja",
                            "correctAnswer", "correct", "answer"):
                    val = q.get(fld)
                    if isinstance(val, str):
                        pieces.append(val)
                for fld in ("choices", "options"):
                    arr = q.get(fld) or []
                    if isinstance(arr, list):
                        for c in arr:
                            if isinstance(c, str):
                                pieces.append(c)
                            elif isinstance(c, dict) and isinstance(c.get("text"), str):
                                pieces.append(c["text"])
                search_text = " ".join(pieces)
                if not search_text:
                    no_match += 1
                    continue
                # Find matches (any example JA that's a substring of search_text)
                matches = set()
                for ex_ja, pid in examples_index:
                    if ex_ja in search_text:
                        matches.add(pid)
                if len(matches) == 1:
                    pid = matches.pop()
                    q["grammarPatternId"] = pid
                    q["grammarPatternId_provenance"] = "auto_derived_example_match"
                    newly_linked += 1
                    file_changed = True
                elif len(matches) > 1:
                    ambiguous += 1
                else:
                    no_match += 1
            if file_changed:
                with open(path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                files_modified.add(path)

    print(f"\nIMP-178 paper-Q cross-link:")
    print(f"  Total paper questions: {total_q}")
    print(f"  Initially linked:      {initial_linked}")
    print(f"  Newly linked:          {newly_linked}")
    print(f"  Ambiguous (skipped):   {ambiguous}")
    print(f"  No match:              {no_match}")
    print(f"  Files modified:        {len(files_modified)}")
    new_total = initial_linked + newly_linked
    print(f"  Final coverage:        {new_total}/{total_q} "
          f"({new_total*100//total_q if total_q else 0}%)")
    return newly_linked


if __name__ == "__main__":
    fix_imp_179()
    print()
    fix_imp_178()
