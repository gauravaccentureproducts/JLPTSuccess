# Audit-prompt drift findings (2026-05-12)

During the 34-commit sprint from "resume with pending items" to
"finish remaining items", **10 separate items** flagged by the
2026-05-09 richness audit (`prompts/N5Improvement.txt`) turned out
to be "false pending" — the actual data state was already at or
above the audit bar, but the audit script was checking the wrong
field names or wrong denominators.

This document catalogs the discrepancies so a future audit pass
can update the prompt's Python block to match the live schema.

## Field-name corrections needed

The audit script's Python census block (in `prompts/N5Improvement.txt`)
should be updated as follows. The current keys produce 0/N counts
on every release because the schema uses different names.

| Audit-script key (current, wrong) | Live schema key (actual) |
|---|---|
| `kanji[].mnemonic_visual` | `kanji[].mnemonic.visual` (nested) |
| `kanji[].mnemonic_reading` | `kanji[].mnemonic.reading` (nested) |
| `kanji[].etymology` | top-level field exists; covered in P2-13 + P5-redirect wave 2 + wave 3 |
| `kanji[].look_alike_clusters` | `kanji[].lookalikes` |
| `kanji[].stroke_order_mistakes` | `kanji[].stroke_order_trap` (`.trap` field describes the learner mistake) |
| `kanji[].vocab_cross_links` | `kanji[].n5_compounds` |
| `kanji[].kun_yomi_origin` | covered by `kanji[].mnemonic.visual` for many entries |

## Denominator / threshold corrections

| Audit claim | Reality (verified post-fixes) |
|---|---|
| "vocab_glossary 0/47" on listening | was 47/50 at audit time; now 50/50 |
| "audio_slow 0/50" on listening | was 47/50 at audit time; now 50/50 |
| "Examples ≥5 (above Bunpro) on grammar: 15%" | actually 177/178 patterns have exactly 10 examples (one has 12). The corpus has been FAR above the audit bar for some time. |
| "Tofugu pedagogical essays: 0/178 explanation_en at ≥500 chars" | 178/178 patterns already had a nested `essay` field (intro/why_it_matters/common_pitfalls/contrasts/closing_practice_tip) at avg 680 chars; 118/178 already ≥500 chars; now all 178 ≥500 chars after enrichment pass. |
| "Grammar examples vocab_ids density: needs verification" | 1774/1782 (99.5%) at audit time; now 1782/1782 (100%) |

## Items confirmed as actual gaps (not drift)

The following audit-flagged gaps WERE real and were closed in this
session — useful for sanity-checking the audit format:

| Item | Real-gap state addressed |
|---|---|
| P2 #12 cultural_callout | 0/178 → 178/178 (authored across 4 waves) |
| P2 #11 discourse_markers_used | 0/50 → 46/50 (4 single-utterance items have no marker tokens — terminal) |
| P2 #14 inference_question_expansion | 0/50 → 50/50 (3 waves) |
| P3 #15 vocab examples ≥3 | 38/1009 → 1009/1009 (16 waves authored 971 examples) |
| P3 #17 listening timestamped_transcript | 0/50 → 50/50 (estimated mora-proportional timing for all items) |
| Vocab counter on nouns | 134/566 → 289/566 (3 waves; remaining 277 are uncountable in Japanese) |
| Reading reflection_prompts | 0/54 → 54/54 |
| Reading paragraph_summary | 0/54 → 7/7 multi-para (47 single-para use existing summary field by design) |
| Reading summary_hi | 45/54 → 54/54 |
| Kanji n5_compounds | 101/106 → 106/106 |
| Kanji lookalikes | 92/106 → 103/106 (3 lack strong N5 lookalike partners — terminal) |
| Kanji stroke-order trap depth | 12 short entries deepened (avg 17 → 175 chars) |
| Grammar contrasts cross-links | 97/178 → ~125/178 (3 waves; remaining lack natural N5 partners) |
| Authentic ↔ vocab cross-links | 0% → 39 cards / 40 vocab linked |
| Authentic ↔ kanji cross-links | 0% → 18 cards / 24 kanji linked |
| Authentic ↔ reading cross-links | 0% → 34 passages thematically linked |
| Authentic ↔ grammar cross-links | 0% → 14 cards / 18 patterns linked |
| Authentic ↔ listening cross-links | 0% → 25 items thematically linked |

## Recommended audit-script update

Replace the field-name keys in the audit's Python census block
with the corrected names from the table above. After that, the
"% below bar" counts should match the actual on-disk data, and
"false pending" findings will stop appearing in subsequent
audit runs.

This document is informational only; the audit prompt itself is a
user-managed file and should be updated at the user's discretion.

## Source of truth

The live data files are:
  - `data/grammar.json` (patterns + nested essay + cultural_callout + contrasts)
  - `data/vocab.json`   (entries + counter + frequency_rank + transitivity_pair + honorific_chain)
  - `data/kanji.json`   (entries with nested mnemonic{summary, visual, reading, meaning} + etymology + lookalikes + stroke_order_trap + n5_compounds + authentic_refs)
  - `data/reading.json` (passages + reflection_prompts + paragraph summary_en + authentic_categories + summary_hi + cultural_context)
  - `data/listening.json` (items + vocab_glossary + discourse_markers_used + inference_question_expansion + timestamped_transcript + audio_slow + authentic_categories)
  - `data/authentic.json` (100 cards with bidirectional cross-link arrays: vocab_refs + kanji_refs + grammar_refs)

Each of these was a "0/N" in the original audit and is now at the documented coverage.
