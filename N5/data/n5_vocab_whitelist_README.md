# n5_vocab_whitelist.json - Design

This whitelist is **generated** from `KnowledgeBank/vocabulary_n5.md` by
`tools/build_data.py`. It is not a hand-curated mirror of `data/vocab.json`.

## Purpose

The whitelist serves as the **recognition allowlist** consumed by
`tools/lint_content.py` when checking that no out-of-N5-scope vocabulary
appears in `data/grammar.json` or `data/questions.json`. A token in the
whitelist means "in-scope at N5"; a token absent from the whitelist
triggers a lint warning when it appears in user-facing content.

## Relationship to data/vocab.json

As of 2026-05-04 (after v1.12.8), the whitelist and vocab.json are
**fully aligned**: every one of the 969 whitelist tokens matches a
`form` or `reading` value in some `vocab.json` entry.

  - **vocab.json**:  1041 structured catalog entries (form, reading,
                     gloss, section, pos, examples).
  - **whitelist**:    969 unique form-tokens, all of which match
                     vocab.json (drift = 0).

The size difference (1041 entries vs 969 unique tokens) reflects:
  - Eight existing multi-form entries that combine multiple readings
    under one form (e.g., 何 with reading="なに / なん"). One entry
    in vocab.json contributes multiple tokens to the whitelist.
  - Nine new multi-form entries shipped in v1.12.8 to close the
    previously-flagged alias gap (いい / よい, ぐらい / くらい, etc.).
    Same pattern: one entry, multiple reading tokens.
  - vocab.json entries can be cross-referenced by section (e.g., 人
    appears as both pronoun in section 1 and counter にん in section 9
    - same form but different entries; whitelist counts the form once).

## History

  - **Before v1.12.7**: vocab.json had 1003 entries; whitelist had
    40 tokens with no vocab.json match (split as 10 multi-form aliases
    + 30 recognition-only items). Documented as "intentional superset"
    in the original draft of this README.
  - **v1.12.8 (2026-05-04)**: closed the drift by authoring 38 new
    vocab.json entries (29 standalone catalog entries + 9 multi-form
    merge entries). The "intentional superset" framing is no longer
    applicable; the whitelist is now a strict subset of vocab.json
    form/reading tokens.

## Consumers

  - `tools/lint_content.py` reads whitelist as an allowlist for the
    vocab-scope check across grammar.json + questions.json.
  - `tools/check_content_integrity.py` derives N5 scope from the
    whitelist's union with the kanji whitelist for various invariants.

## Maintenance

  - **Adding a new word to N5 scope**: edit `vocabulary_n5.md`, then
    run `python tools/build_data.py` to regenerate
    `n5_vocab_whitelist.json`. Also add a structured entry to
    `data/vocab.json` (form, reading, gloss, section, pos, examples)
    so the catalog stays aligned.
  - **Removing a deprecated form**: edit `vocabulary_n5.md` to remove
    the line, regenerate the whitelist, and remove the corresponding
    `data/vocab.json` entry (or update its multi-form notation if the
    other form in a pair stays).

The whitelist is a **derived artifact** - never edit it by hand.
