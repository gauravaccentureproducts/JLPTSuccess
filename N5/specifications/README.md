# N5 Specifications

This folder holds the functional and implementation specifications for the JLPT N5 sub-app of JLPTSuccess.

## Read this first

**`JLPT-N5-Current-Implementation-Spec.md`** - the **authoritative living spec**. Describes what the app actually is today (v1.12.32, round-4 close-out, 2026-05-05; CI invariants reference section added 2026-05-17 covering all 91 wired JA-NN rules). If you need ground truth for any decision or hand-off, start here.

**Strategic positioning (post-2026-05-06 narrowing):** primary niche is N1 (Hindi-medium JLPT prep - India is the 5th-largest JLPT country with ~50K applicants/year and no dedicated Hindi-native prep app); secondary niche is N2 (privacy / no-account / offline). The 5-locale shell (en/vi/id/ne/zh) was narrowed to en+hi on 2026-05-06 per the IMP-096 architectural decision; vi/id/ne/zh markets are saturated by established native-language competitors. The audit prompt at `../prompts/N5Improvement.txt` carries the canonical niche framing. Do NOT chase Bunpou grammar-review depth or WaniKani kanji-mnemonic depth - these are documented anti-niches per `Q13` in `../feedback/n5-audit-2026-05-04.xlsx`.

## Historical record

The remaining files are kept as point-in-time snapshots for traceability. **Do not edit them.** They are superseded by the current-implementation spec above.

| File | Status | Date | Notes |
|---|---|---|---|
| `JLPT-N5-Current-Implementation-Spec.md` | **CURRENT** | 2026-05-05 | Source of truth |
| `JLPT-N5-Functional-Spec-v3.1-supplement.md` | Historical | 2026-04-30 | Gap-fill addendum to v3 .docx; covered the drift between v3 and the live app at that point |
| `JLPT N5 - Consolidated Spec.docx` | Historical | 2026-05-04 | v3-consolidated form - pre-migration |
| `JLPT N5 Grammar Tutor – Functional Spec.docx` | Historical | 2026-04-30 | v3 (informally amended); the original .docx spec |

## What changed between the historical record and the current spec

The historical .docx + supplement reflected the app *before* the JLPTSuccess monorepo migration (2026-05-04). Since then:

1. **Repo and live URL changed.** Was `gauravaccentureproducts/jlpt-n5-tutor` deploying to `…github.io/jlpt-n5-tutor/`; now `gauravaccentureproducts/JLPTSuccess` deploying the N5 sub-app to `…github.io/JLPTSuccess/N5/`.
2. **Brand-link routes changed.** The brand-link now goes `../` (one level up to the JLPTSuccess level picker), not `#/levels` (an in-app placeholder route that no longer exists).
3. **Service worker cache version reset.** Was `jlpt-n5-tutor-v138`; now `jlptsuccess-n5-v1.12.32` (mirrors `version.json:version`).
4. **Logo deployed.** The five-bar ladder mark from `assets/logo/` (top-level shared) is now wired into the favicon + PWA icons.
5. **Content scale grew.** Audio MP3 count now 711, locale files at 2 (en + hi, narrowed from 5 on 2026-05-06 per IMP-096; ~113 keys per locale, hi llm_curated until native review), integrity invariants at 47 (round-7 added JA-36/37/38).
6. **Other levels around it.** N4 is work-blocked; N3/N2/N1 placeholders exist.
7. **New routes (round-3):** `#/missed` (wrong-answer history) + `#/sitting` (full mock-paper sitting flow).
8. **New surfaces on home (round-4):** trust band (5 niche-N2 pills), 7-day review forecast, daily-goal progress ring.
9. **License formalized (round-4):** MIT for code (`/LICENSE`), CC BY-SA 4.0 for content. Self-host docs at `docs/SELF-HOST.md`. Translator on-ramp at `docs/TRANSLATING.md`.
10. **Provenance scaffold (round-4):** every content item carries `review_status` from a closed enum {native_reviewed, llm_curated, auto_generated}; current default is `llm_curated` pending native-review pass (audit `Q16`).

The current-implementation spec captures the post-migration state in full.

## When to update which file

- App behavior changed → update `JLPT-N5-Current-Implementation-Spec.md` and bump its "Last updated" header.
- Audit found a drift between spec and reality → fix the spec to match reality (the spec follows the implementation, not the other way around).
- Strategic direction changed (niche pivot, positioning) → update both `JLPT-N5-Current-Implementation-Spec.md` (§22 Out of scope, §23 Roadmap) AND `prompts/N5Improvement.txt` (the strategic-framing intro).
- **New CI invariant added** to `tools/check_content_integrity.py` → mirror it in `JLPT-N5-Current-Implementation-Spec.md` §25 (CI invariants reference) in the same commit. The script is the source of truth; §25 is its human-readable index — keep them in sync.
- Historical files should never be edited.
