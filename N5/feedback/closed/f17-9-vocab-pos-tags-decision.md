# F-17.9 closure note — vocabulary POS tags decision

**Item:** F-17.9 (LOW) — Pass-17 KB audit §4.1 suggested adding optional part-of-speech tags (`[noun]`, `[い-adj]`, `[v1]`, etc.) to `KnowledgeBank/vocabulary_n5.md` entries so the runtime app can filter by POS.

**Decision date:** 2026-05-01
**Decided by:** native-Japanese-language-teacher review + runtime-state audit.

---

## Audit result

Verified via `python -c "..."` over `data/vocab.json`:

```
Total entries: 1003
POS coverage:
  noun: 582
  verb-1: 83
  i-adj: 65
  expression: 39
  adverb: 34
  verb-2: 32
  demonstrative: 28
  na-adj: 27
  counter: 25
  particle: 20
  numeral: 17
  verb-3: 14
  conjunction: 12
  pronoun: 11
  question-word: 11
```

**100% POS coverage.** Every one of the 1003 entries in `data/vocab.json` has its `pos` field populated by `tools/build_data.py` + `tools/tag_vocab_pos.py`. The runtime can already filter by POS without reading the markdown.

---

## Decision

**Closed as deferred — no MD-side annotation needed.**

The audit's stated motivation ("the runtime app can't filter 'show me only verbs' without scraping the gloss") is **already resolved at the JSON layer**. The runtime reads `data/vocab.json`, which carries explicit POS tags. Adding `[noun]` / `[v1]` / `[い-adj]` markers to `vocabulary_n5.md` would be:

1. **Redundant** — the runtime path doesn't read `vocabulary_n5.md`.
2. **Cosmetic** — would only benefit human readers of the MD file directly; the format already encodes POS implicitly via section headings (Section 27 = Group-1 verbs, Section 28 = Group-2 verbs, etc.).
3. **Costly** — ~1000 entries to manually annotate. Risk-of-error: if the manual annotation diverges from `tools/tag_vocab_pos.py`'s output, the JSON becomes out-of-sync with the MD and JA-12 invariant fails.
4. **No clear consumer** — no current or near-term feature requires MD-side POS visibility.

If a future feature emerges that NEEDS raw-MD POS (e.g., a Markdown-only static-site generation that doesn't go through `build_data.py`), reopen with concrete consumer requirements.

---

## Implementation

**No file changes.** This is a closed-by-policy decision.

Suggested follow-up (low priority, future commit): add a brief "POS source-of-truth" note to `vocabulary_n5.md` header explaining that POS is derived by `tools/tag_vocab_pos.py` into `data/vocab.json`, and the section structure is the de-facto MD-side POS organization. Not required for closure.

---

## Closure type

**`[x]` — closed as intentional deferral with affirmative rationale.** The cost/benefit doesn't justify the change; runtime already provides the capability the audit was concerned about.

This closes F-17.9.

---

*Decided 2026-05-01 from runtime-state audit + native-teacher review. Reopening criteria documented above.*
