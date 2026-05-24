"""Horizontal analysis: for each bug class found in the first pass,
search the entire 178-pattern corpus for OTHER occurrences of the
same pattern. Reports newly-found suspect rows for human triage.

Bug classes to horizontal-deploy on:

  A. Empty audio paths (TS-06) — already exhaustive (auto-check covers
     all 178); just confirm.
  B. (see ...) placeholder examples (TS-06) — TTS skips these, no
     audio gets rendered. Different failure mode from A.
  C. Particle-swap "common mistakes" where both wrong and right are
     valid Japanese with different meanings (TS-03) — extends the
     n5-011 / n5-024 finding.
  D. Malformed wrong/right cells with arrow characters or embedded
     alternatives (TS-03) — extends the n5-021 finding.
  E. Wrong-field annotations in parentheses that change the semantics
     vs a pure "wrong/right" pair (TS-03) — e.g. "X (in context Y)".
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_JSON = ROOT / "data" / "grammar.json"
OUT_FILE = ROOT / "tools" / "grammar_horizontal_findings.json"


def main():
    g = json.loads(GRAMMAR_JSON.read_text(encoding="utf-8"))
    patterns = g["patterns"]

    findings_by_pid = {}

    def add(pid, ts, note):
        findings_by_pid.setdefault(pid, {}).setdefault(ts, []).append(note)

    # === A. Empty audio paths (TS-06) ===
    a_count = 0
    for p in patterns:
        bad = []
        for i, ex in enumerate(p.get("examples") or []):
            ja = (ex.get("ja") or "").strip()
            if not ja or "(see " in ja:
                continue
            audio = (ex.get("audio") or "").strip()
            if not audio:
                bad.append(i)
        if bad:
            a_count += 1
            add(p["id"], "TS-06", f"Class A (empty audio paths): example indices {bad}")

    # === B. (see ...) placeholder examples (TS-06) ===
    b_count = 0
    for p in patterns:
        sees = []
        for i, ex in enumerate(p.get("examples") or []):
            ja = (ex.get("ja") or "").strip()
            if "(see " in ja:
                sees.append((i, ja[:50]))
        if sees:
            b_count += 1
            add(p["id"], "TS-06", f"Class B ((see ...) placeholders, no audio rendered): {sees}")

    # === C. Particle-swap valid-both-ways (TS-03) ===
    # We look for common_mistakes where:
    #  - wrong has と  and right has や or か at the same position
    #  - wrong and right are otherwise near-identical
    # These are HIGH-LIKELIHOOD false "common mistakes" (both valid JP).
    c_count = 0
    PARTICLE_SWAPS = [
        # (a, b, note about what the conflation usually is)
        ("と", "や", "exhaustive vs non-exhaustive listing — both valid"),
        ("と", "か", "and vs or — both valid, different meanings"),
        ("や", "と", "non-exhaustive vs exhaustive listing — both valid"),
    ]
    for p in patterns:
        for i, m in enumerate(p.get("common_mistakes") or []):
            w = (m.get("wrong") or "").strip()
            r = (m.get("right") or "").strip()
            if not w or not r:
                continue
            # Look for cases where ONLY a particle swap differs
            for a, b, label in PARTICLE_SWAPS:
                if a in w and b in r:
                    # Quick sameness check: if we replace `a` with `b` in
                    # the wrong, does it become close to the right?
                    swapped = w.replace(a, b, 1)
                    # Normalise spaces
                    norm = lambda s: re.sub(r"\s+", "", s)
                    if norm(swapped) == norm(r):
                        c_count += 1
                        add(p["id"], "TS-03", f"Class C (particle-swap {a}->{b} but both valid JP, {label}): cm[{i}] wrong='{w[:50]}' right='{r[:50]}'")
                        break

    # === D. Malformed wrong/right with arrow / multi-alternative (TS-03) ===
    d_count = 0
    arrow_re = re.compile(r"[→➔➜⇒]")
    for p in patterns:
        rows = (p.get("common_mistakes") or []) + (p.get("wrong_corrected_pair") or [])
        for i, m in enumerate(rows):
            w = (m.get("wrong") or "")
            r = (m.get("right") or m.get("correct") or "")
            for which, txt in (("wrong", w), ("right", r)):
                if arrow_re.search(txt):
                    d_count += 1
                    add(p["id"], "TS-03", f"Class D (malformed: arrow in {which} field): '{txt[:60]}'")

    # === E. Wrong-field carrying context annotation in parens ===
    # The pattern looks like "<JA sentence> (when meaning X)" or "(in context Y)".
    # These often change the meaning rather than mark a grammar error.
    e_count = 0
    paren_annotation_re = re.compile(r"\((?:when|asking|with|in context|using|intent|about|for)\b[^)]*\)", re.IGNORECASE)
    for p in patterns:
        for i, m in enumerate(p.get("common_mistakes") or []):
            w = (m.get("wrong") or "")
            if paren_annotation_re.search(w):
                e_count += 1
                add(p["id"], "TS-03", f"Class E (wrong-field carries semantic context annotation): cm[{i}] '{w[:80]}'")

    # === Write findings ===
    OUT_FILE.write_text(json.dumps(findings_by_pid, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK wrote {OUT_FILE}")
    print(f"  Class A (empty audio paths)       : {a_count} patterns")
    print(f"  Class B ('(see ...)' placeholders): {b_count} patterns")
    print(f"  Class C (particle-swap both-valid): {c_count} rows")
    print(f"  Class D (arrow in wrong/right)    : {d_count} rows")
    print(f"  Class E (semantic-context paren)  : {e_count} rows")
    print(f"  Unique patterns flagged           : {len(findings_by_pid)}")


if __name__ == "__main__":
    main()
