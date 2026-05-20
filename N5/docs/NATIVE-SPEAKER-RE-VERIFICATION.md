# Native-speaker re-verification — path forward

**Set 2026-05-21.** Documents the genuine-human-only deferred item
from the REG-001 / GOI-001 / DOKKAI-* / PAPER-* / MOB-* close-out
series.

## What needs native-speaker review

54 `register_variant` entries in `grammar.json` (`common_mistakes`
blocks), of which:

  - **21 entries** were migrated/created in 2026-05-19 REG-001 SWEEP-1
    Tier 1 with provenance
    `llm_curated_with_reference_genki_minna_jees_2026_05_19`. Each
    cites Genki I / Minna no Nihongo I / JEES official N5 sample
    papers as the reference baseline.
  - **6 entries** were created from the REG-001 D6 close-out
    (n5-046 + n5-097/102/127/173/179) with similar provenance.
  - **27 entries** pre-existed from earlier audit batches
    (issue-112-phase4-5, bug-007 fix). These carry provenance
    `native_reviewed` from the prior maintainer, but the depth
    of that review is not documented in the provenance string.

Plus several `wrong_corrected_pair` `category=register` /
`category=pragmatic` / `category=cultural` entries (15 C-class
recategorizations from SWEEP-1 + 14 B-class entries retained).

## Why this is human-only work

An LLM (this one included) can:

  - Cross-reference textbook conventions (Genki / Minna)
  - Check formal JEES syllabus inclusion
  - Apply consistent labeling schemata
  - Catch obvious mismatches via stop-list patterns

An LLM **cannot reliably**:

  - Judge whether a particular form sounds "natural" to a native ear
    in a specific dialect / register / age group
  - Catch subtle regional variation (Kanto/Kansai/Tohoku usage
    differences)
  - Confirm whether a register_variant pair would actually be
    interchanged by a native speaker in the labeled context
  - Catch nuances of 尊敬/謙譲/丁寧 that vary by industry / age /
    relationship dynamics

These need a fluent native Japanese speaker (ideally with
language-teaching experience) reviewing each entry.

## Path forward — three options

### Option A: Community PR-based review (lowest cost, slowest)

  1. Surface the 21+6+27 = 54 entries in a public review thread
     (GitHub Discussion or Issue tagged `native-review-needed`).
  2. Each PR by a native speaker upgrades 1+ entries:
     - Adds `native_review` block:
       ```json
       "native_review": {
         "reviewer_handle": "@example",
         "reviewed_on": "YYYY-MM-DD",
         "verdict": "natural" | "needs_rewrite" | "context_caveat",
         "notes": "..."
       }
       ```
     - Updates `provenance` from
       `llm_curated_with_reference_*` to
       `native_reviewed_<handle>_<date>` on the approved entry.
  3. Track progress in `docs/NATIVE-REVIEW-LOG.md`.

### Option B: Commissioned single-pass review (moderate cost, fastest)

  1. Hire a fluent Japanese-language teacher (e.g. via 日本語教師
     marketplace or Upwork JLPT-instructor pool) for a 4-8 hour
     pass over all 54 entries.
  2. Provide reviewer with:
     - The current 54 entries (export to a shared spreadsheet)
     - A scoring rubric (verdict + notes per entry)
     - The reference baselines (Genki / Minna / JEES) for context
  3. Apply the reviewer's verdicts as a single commit
     post-review.

### Option C: Accept LLM-curated provenance with periodic
     review-on-finding (status-quo, lowest effort)

  1. Keep the `llm_curated_with_reference_*` provenance flag as the
     surfaced marker.
  2. When a user reports a finding that traces to one of the
     LLM-curated entries (e.g., a future bug report says
     "n5-018's どなた label is misleading"), promote that single
     entry to `native_reviewed_<handle>_<date>` via Option A's
     PR mechanism.
  3. Over time, the corpus drifts naturally toward 100% native-
     reviewed as user feedback accumulates.

**This option is the current default.** The corpus ships with
LLM-curated provenance; user-driven re-verification happens as
findings arise.

## Tracking signal

After this work the corpus state is:

  - 54 register_variant entries (40 with `llm_curated_with_reference_*`
    or equivalent; 14 with `native_reviewed` from prior batches)
  - 0 currently-blocking findings
  - All CI-enforceable structural invariants pass (139 / 139 green
    as of commit `40700d6`)

If a maintainer chooses Option A or B and runs a full review pass,
the expected outcome is:

  - **Best case (corpus is already correct)**: 54 entries
    re-stamped `native_reviewed_*`; 0 content edits required.
  - **Realistic case**: 50-52 entries re-stamped clean; 2-4 entries
    flagged for content edits (label refinement, scope_note
    extension, or full migration to a different category).
  - **Worst case**: 5-10 entries flagged for revision; nothing
    structurally broken — the
    `llm_curated_with_reference_*` flag did its job by
    surfacing what needs human review.

## What this doc is NOT

  - Not a commitment to commission paid review
  - Not a public RFP
  - Not a rejection of the corpus quality — Tier 1/2/3 audits
    found 0 structural defects; the LLM-curated entries are
    PROBABLY correct, just need confirmation

## Bounded coverage

This deferred-item documentation is for the
`register_variant` + recategorized `wrong_corrected_pair`
entries from REG-001 SWEEP-1..3. Other parts of the corpus
(examples in `examples[].ja`, vocab.json entries, kanji.json
glosses, etc.) are not in scope here — they have their own
provenance fields and their own review processes.
