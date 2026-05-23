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

---

## Pitch-accent protocol 2026-05-23

### Scope

The pitch-accent verification protocol is a SECOND, INDEPENDENT
deferred-human-only review track separate from the
`register_variant` track above. It targets entries in
`data/n5_pitch_accent_reference.json` with
`match_kind: "by-reading"`.

### Why this is a separate, second track

Pitch-accent claims are a different kind of authority claim from
register_variant claims:

  - **register_variant** asks: "does a native speaker accept this
    pair as register-equivalent in this context?" — qualitative,
    context-sensitive, native intuition.
  - **pitch-accent** asks: "does NHK 2016 list drop=N for this
    headword, AND does our voice actor's recording match?" — a
    two-part objective claim (dictionary lookup + audio
    verification) that still requires native-speaker fluency
    plus access to the physical reference.

The current data carries `match_kind: "by-reading"` for entries
where the kanjium lookup matched by reading rather than exact
headword form. These are defensible (Genki / Minna / kanjium
all use the same reading-to-drop map) but not authoritative —
the reading-form lookup is a proxy for the headword-form
lookup, and NHK 2016 may diverge on specific entries.

### Discipline guard rails (binding)

  - **F.44.7 — Defensible-but-deviant pitch-accent class.**
    Annotate, don't auto-correct. Add `native_review_pending`
    flag rather than promoting `match_kind` to `exact`.
  - **F.44.15 Shape 2 — Annotation-only when verifier == author.**
    When the only verifier of NHK 2016 is the same author
    (Claude) who produced the audit pipeline, circular
    authority — annotate to preserve the gap, don't claim
    NHK-verified.
  - **CI invariant JA-155** locks the discipline: any entry with
    `match_kind: "exact"` must carry a complete `audit` block
    (verifier_pending: false + result_schema populated with
    verified_against / verified_at / verifier_credential /
    verified_drops / verified_match_kind). Grandfathered
    exception: `source: "kanjium-8a0cdaa1-exact"` (legacy
    exact-form lookup that pre-dates the audit-block discipline).

### Per-entry verification procedure

For each entry on the queue (see
`docs/PITCH-ACCENT-VERIFICATION-QUEUE-2026-05-23.md`):

**Step 1 — NHK 2016 lookup.**
  - Look up the form in NHK 日本語発音アクセント新辞典 (2016).
  - Cite page number + drop notation (Maru notation:
    ⓪ ① ② ③ …).
  - If multiple drops listed in NHK, note which is primary +
    which are alternates.
  - If NHK distinguishes senses (e.g., あなた generic-pronoun
    vs spousal-address), note all senses.

**Step 2 — Audio location.**
  - Per-vocab pitch audio does NOT exist as standalone files
    in this corpus. The form must be located within listening
    passages (`data/listening.json` → `script_ja` containing
    the form string).
  - Grep `data/listening.json` for the form. Note `passage_id`
    + approximate `timestamp` (mm:ss) within the passage.
  - If the form does not appear in any listening passage, mark
    `audio_passage_reference: "not_found_in_listening_corpus"`
    and rely on the dictionary value alone (with explicit note
    in `decision_note` that audio could not be cross-checked).

**Step 3 — Audio vs dictionary reconciliation.**
  - Listen to the audio at the noted timestamp. Identify the
    actual drop produced by the voice actor.
  - If audio and dictionary AGREE: simple case; populate audit
    with `verified_drops: [<agreed value>]`,
    `verified_match_kind: "exact"`, `decision_note: "NHK and
    audio agree on drop=N at passage X timestamp Y."`
  - If audio and dictionary DISAGREE: **default to the audio**
    (that's what the learner hears). Populate
    `verified_drops: [<audio value>, <NHK value>]` (audio
    first as primary). `decision_note` must explicitly
    document the disagreement + which value the learner will
    encounter at runtime.

**Step 4 — Promote match_kind.**
  - Once the audit block is fully populated and
    `verifier_pending` is flipped to `false`, promote
    `match_kind` from `"by-reading"` to `"exact"`.
  - JA-155 will then pass for this entry.

**Step 5 — Cross-update vocab.json.**
  - The vocab.json `pitch_accent` field carries the active drop
    value used by the rendered UI. If the audit changed `drops`
    on the n5_pitch_accent_reference side, mirror the change
    into vocab.json's `pitch_accent.drop` field.
  - Provenance: stamp `pitch_accent_provenance:
    "native_speaker_verified_<YYYY_MM_DD>"` on the vocab entry.

### Audit-block schema (canonical)

```json
"audit": {
  "verifier_pending": true,
  "pending_since": "2026-05-23",
  "pending_wave": "pitch-accent-native-verify-2026-05-23",
  "current_state_at_audit_request": {
    "drops": [2],
    "match_kind": "by-reading"
  },
  "review_question": "...specific per-entry question...",
  "verification_protocol_link": "docs/NATIVE-SPEAKER-RE-VERIFICATION.md#pitch-accent-protocol-2026-05-23",
  "verification_required_against": [
    "NHK 日本語発音アクセント新辞典 (2016)",
    "Audio in listening passages"
  ],
  "verifier_credential_required": "Native Japanese speaker OR certified Japanese-language teacher",
  "result_schema": {
    "verified_against": null,
    "verified_at": null,
    "verifier_credential": null,
    "verified_drops": null,
    "verified_match_kind": null,
    "decision_note": null,
    "audio_passage_reference": null,
    "nhk_page_reference": null
  }
}
```

### Canary entries (already scaffolded 2026-05-23)

Three entries are scaffolded with the audit block:

  - **みなさん** (drops=[2], by-reading) — NHK lists ③; question
    is whether voice actor recorded ② or ③.
  - **あなた** (drops=[2, 1], by-reading) — NHK lists ⓪ for
    generic pronoun; question is whether to add ⓪ as primary.
  - **きのう** (drops=[1, 0, 2], by-reading) — NHK lists ②;
    question is whether ② should be primary if audio matches.

These three are the entry point. Once verified by a real human
native speaker, the methodology proves out on a small set
before the broader 587-entry queue is engaged.

### Broader pass (587 entries)

`docs/PITCH-ACCENT-VERIFICATION-QUEUE-2026-05-23.md` lists all
remaining `match_kind: "by-reading"` entries sorted by N5 vocab
frequency proxy (vocab.json section number, lower = more
foundational). Top section coverage:

  - section 1 (Pronouns/Self): 5 entries
  - section 2 (People-Family): 15 entries
  - section 3 (Greetings): 5 entries
  - section 4 (Numbers): 8 entries
  - section 5 (Time-Hours): 19 entries
  - section 6 (Time-Day Parts): 4 entries
  - … 587 total

A native speaker working at ~5 entries/hour can clear the queue
in ~120 hours. At ~30/hour with the canonical reference open,
~20 hours. This is the cost of moving from "kanjium-by-reading"
to "human-verified-NHK-matched-audio-aligned".

### Discipline meta-note

LLM-authored verification of pitch-accent claims is rejected
by F.44.7 + F.44.15 Shape 2 + JA-155 in concert. The 2026-05-23
reviewer task asked Claude to perform this verification;
Claude declined and produced this protocol + scaffold instead.
The audit-block schema preserves the gap honestly so a real
human can fill it in later without us pretending the
verification has happened.
