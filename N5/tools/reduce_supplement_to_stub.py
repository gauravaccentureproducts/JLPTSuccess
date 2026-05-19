#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Reduce the v3.1 supplement to a redirect stub + preserve §G design system.

Reads `specifications/JLPT-N5-Functional-Spec-v3.1-supplement.md`, splits at
the `## §G Design System (Zen Modern)` heading, replaces everything above it
with a redirect stub pointing to the merged canonical spec, and writes the
file back atomically.

Backup of the pre-reduction file is saved to
`specifications/JLPT-N5-Functional-Spec-v3.1-supplement.md.bak_YYYY_MM_DD_pre_merge`
per project backup policy (never overwrite an existing backup).
"""
from __future__ import annotations

import shutil
import sys
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

SRC = Path(__file__).resolve().parent.parent / "specifications" / \
    "JLPT-N5-Functional-Spec-v3.1-supplement.md"

STUB = """\
# JLPT N5 Functional Specification - v3.1 Supplement  (REDUCED TO REDIRECT STUB)

**Status:** **MERGED + SUPERSEDED on 2026-05-19.** The functional / governance
content of this supplement (sections A–F) was merged into the canonical
`specifications/JLPT-N5-Current-Implementation-Spec.md` (renamed to
"JLPT N5 — Functional & Implementation Specification" in the same revision).

**Where to read instead:** open
[`JLPT-N5-Current-Implementation-Spec.md`](./JLPT-N5-Current-Implementation-Spec.md)
— that is now the single canonical source-of-truth for "what the N5 app
is, how it's built, what governance + quality contracts apply." See §§ 26–38
of that document for the content merged out of this file.

**What remains here:** the *Zen Modern design system* (§G below) is
preserved unchanged at the bottom of this file because the canonical spec
points to it as a companion-document reference (§36 of the merged spec). A
future revision may extract §G to a standalone
`specifications/jlpt-n5-design-system-zen-modern.md`; until that happens,
this file is the canonical home of the design tokens.

**Git history note:** the full pre-merge content (sections A–F, plus the
historical errata + 2026-05-03 §F revision block + 2026-05-01 §B additions)
is preserved in the git history of this file. Use
`git log specifications/JLPT-N5-Functional-Spec-v3.1-supplement.md` from
before commit-of-merge to recover any specific paragraph if needed. A
backup copy is also at
`specifications/JLPT-N5-Functional-Spec-v3.1-supplement.md.bak_YYYY_MM_DD_pre_merge`.

---

## Subsection-by-subsection redirect map

| Old section in this supplement | Where it now lives |
|---|---|
| A.1 Sections missing from v3 | §§26–35 of merged spec |
| A.2 Drift v3 → current | Historical; resolved per §§3–25 of merged spec |
| B.1 Document control | §1 of merged spec |
| B.2 Glossary | §26 of merged spec |
| B.3 Stakeholders | §27 |
| B.4 User stories | §28 |
| B.5 Success metrics / KPIs | §29 |
| B.6.1 NFR-I Internationalization | §30.1 |
| B.6.2 NFR-W PWA | §30.2 |
| B.6.3 NFR-P Performance | §29 + §30.3 |
| B.6.4 NFR-A Accessibility | §30.4 |
| B.7 Test strategy | §19 + §25 + §32.2 |
| B.8 Risks register | §31 |
| B.9 Open questions / decisions log | Historical (workbook + verification.md) |
| B.10 Maintenance and support model | §32 |
| B.11 Release process | §32.3 |
| B.12 Copy voice contract | §33 |
| B.13 External-blocked items reframed | Historical (verification.md + IMP closures) |
| B.14 Pass 15a heuristic audit | §34.1 |
| B.15 Microinteractions vs Zen Modern | §35 |
| C.1 Scope movement (Audio, etc.) | §22 |
| C.2 Global navigation rewrite | §4.2 + §5.1 |
| C.3 §5 sub-sections | §5.1 – §5.16 |
| C.4 Drill / SRS Leitner → SM-2 → FSRS-4.5 | §5.9 + §5.10 + §22 |
| C.5 Data model additions | §7 + §8 |
| C.6 Repository structure | §3.1 |
| C.7 NFR replacement | §30 |
| C.8 Future enhancements rewrite | §23 |
| D Pass-N audit protocol | §34 |
| E Acceptance criteria for v4 | §37 |
| F.1 Mobile UI NFR-M1..M9 | §30.5 (extended with NFR-M10 / M11 on 2026-05-19) |
| F.2 Disabled-button feedback NFR-U | §30.6 |
| F.3 JA-25..JA-33 invariants | §25 (extended through JA-136+) |
| F.4 Anti-patterns AP-7..AP-10 | Procedure manual Appendix F + workbook tabs |
| F.5 Corpus state snapshot | §7.1 |
| F.6 New routes | §4.2 |
| F.7 SW version + PWA contract | §9 + §30.2 |
| F.8 Pass-N audit log | §34.1 |
| F.9 Procedure manual + companion docs | §32.4 + procedure manual itself |
| F.10 Open / deferred items snapshot | Historical (workbook + verification.md) |
| **G Design System Zen Modern** | **Preserved below in this file** (referenced by §36 of merged spec) |

---

"""


def main() -> None:
    if not SRC.exists():
        print(f"FATAL: source file missing: {SRC}", file=sys.stderr)
        sys.exit(2)

    today = date.today().strftime("%Y_%m_%d")
    bak = SRC.parent / (SRC.name + f".bak_{today}_pre_merge")
    if bak.exists():
        i = 2
        while True:
            alt = SRC.parent / (bak.name + f"_v{i}")
            if not alt.exists():
                bak = alt
                break
            i += 1
    shutil.copy2(SRC, bak)
    print(f"Backup written: {bak.name}")

    text = SRC.read_text(encoding="utf-8")
    lines = text.split("\n")
    g_idx = None
    for i, line in enumerate(lines):
        if line.startswith("## §G "):
            g_idx = i
            break
    if g_idx is None:
        print("FATAL: could not find §G boundary", file=sys.stderr)
        sys.exit(2)

    preserved_tail = "\n".join(lines[g_idx:])
    new_text = STUB + preserved_tail
    SRC.write_text(new_text, encoding="utf-8")

    print(f"Pre-merge length: {len(lines)} lines")
    print(f"Preserved tail (from §G): starts at line {g_idx + 1}, "
          f"{len(lines) - g_idx} lines")
    print(f"New stub: {len(STUB.split(chr(10)))} lines")
    print(f"New total: {len(new_text.split(chr(10)))} lines")
    print(f"Written: {SRC}")


if __name__ == "__main__":
    main()
