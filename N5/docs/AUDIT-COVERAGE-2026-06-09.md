# JLPT N5 — Gloss-Coverage Lesson Propagation (2026-06-09)

This document records a **cross-level lesson propagation**, not an N5 audit
cycle. The lesson originated in native review (rounds 5–6) of the **standalone
N4 grammar deliverable** (`JLPT/N4_Grammar_Patterns_128_*.docx`, outside this
repo; the N4 product remains paused under JLPTSuccess Rule 1). Per Rule 4, the
generalizable learning is propagated to the four documentation surfaces and
**validated against the live N5 corpus**.

**Writing-discipline note.** Counts below are bounded by *what was scanned*
(the 178-pattern `data/grammar.json` snapshot on 2026-06-09) and *how it was
matched* (the sense-segment heuristic named in DIR-A/DIR-B). "0/178" means the
DIR-A proxy found no segment-count overreach *in this snapshot*; it does NOT
mean every gloss is native-verified to cover its examples — the too-narrow
direction is explicitly native-judgment (DIR-B), not gate-able.

---

## The lesson (procedure-manual F.60)

A grammar entry's English gloss must be the **union of exactly the senses its
examples exercise** — no example without a covering gloss-clause (too-narrow),
and no gloss-clause without a demonstrating example (overreach). Highest-risk:
polysemous particles / enders (`って`, `と`, `し`, `から`, `のに`, `ば`/`たら`)
where one surface form spans naming / topic / quote / hearsay / cause / contrast.

Origin defects in the N4 deliverable:
- **TOO NARROW** — `って` glossed "named; called ~" while example 3
  (`あした 雨が ふるって`) was casual hearsay ("I hear it'll rain").
- **OVERREACH** — a cleft-focus gloss listing a "reason for …" sense that none
  of the shown examples demonstrated.

---

## Propagation ledger (Rule 4, four surfaces)

| Surface | Edit | Status |
|---------|------|--------|
| `JLPT Common/procedure-manual-build-next-jlpt-level.md` | Appendix **F.60** (F.60.1 rule, F.60.2 reconciliation pass, F.60.3 high-risk set + bounded claim) | Added |
| `N5/prompts/Japanese language Accuracy check.txt` | Category **A93** (gloss↔example sense-coverage) + **FP-24** (polysemous-substring ≠ multi-sense-gloss-required) | Added |
| `N5/prompts/N5Improvement.txt` | Section-10 anti-item (2026-06-09) bundling the DIR-A Phase-0 check | Added |
| `N5/docs/AUDIT-COVERAGE-2026-06-09.md` | This document | Added |

---

## Corpus validation (178-pattern `grammar.json`, 2026-06-09)

| Signal | Definition | Result | Disposition |
|--------|-----------|-------:|-------------|
| empty `meaning_en` | gloss blank | 0/178 | — |
| zero examples | no examples | 0/178 | — |
| **DIR-A** (overreach, gate-able) | sense-segments(`meaning_en`) > `len(examples)` | **0/178** | Clean 0-return regression mirror |
| **DIR-B** (too-narrow, NOT gate-able) | polysemous-surface substring + single-sense gloss | 58/178 | Almost all false positives → native-judgment surface (FP-24) |

DIR-B false-positive examples (mono-sense patterns whose *name* merely contains
a particle substring): `しか〜ない` ("only"), `など` ("etc."), `何` ("what"),
`だれ` ("who"), `から〜まで` ("from X to Y"). These confirm the too-narrow
direction must NOT be a 0-gate.

**CI status:** no new JA-NN invariant. DIR-A is a Phase-0 maintainer-side
regression mirror (deterministic, currently 0); the too-narrow direction needs
sense judgment and is not auto-detectable. This matches the A92 precedent
("no new JA-NN").

---

## Future native-human review

- The **too-narrow** direction (gloss narrower than the senses its examples
  show) is not mechanizable without per-sense tagging and remains a native-
  reviewer surface for any level that authors grammar glosses.
- Validation was run with `JLPT/_n5_gloss_check.py` (standalone, outside this
  repo). If a permanent gate is later wanted, DIR-A could be wired into
  `tools/check_content_integrity.py` as a JA-NN — that is a Code change beyond
  this Rule-4 propagation and is intentionally deferred.
