# JLPT N4 — Content authoring tasks (parked)

**Status:** Out of scope for the current N5 repo. Tracked here for the eventual N4 sibling project.
**Created:** 2026-05-01
**Source:** lifted from `TASKS.md` Pass-20 §"Deferred to Pass-21" (the Pass-20 procedure-manual review's three remaining content-authoring items).

---

## Why these aren't in the N5 repo's TASKS.md anymore

The N5 repo is in maintenance phase: 33 content-integrity invariants, 8 design-system rules, 223 questions, 177 grammar patterns, 106 kanji, 1003 vocab. The 3 items below describe building the **N4 corpus from authoritative external sources** — not maintaining N5. They were registered under "Pass-21" in `TASKS.md` but cluttered the unchecked-item count (3 of the 5 visible items). Moved here so the N5 maintenance view is clean (now 0 actionable items remain in N5 maintenance scope).

When (if) the N4 project starts, this doc becomes its starter task list.

---

## How to execute (per `specifications/procedure-manual-build-next-jlpt-level.md` Appendix B.12)

The procedure manual's Appendix B.12 contains extraction-script recipes for each task below. The agent operating on the N4 build should:

1. Create the empty `tools/extract_n4_*.py` scripts following Appendix B.12.1 / .2 / .3 recipes.
2. Run each against the cited authoritative sources.
3. Emit the output files described.
4. Run `tools/build_data.py` (ported from N5) to derive the JSON data files.
5. Run the N4 equivalent of `tools/check_content_integrity.py` to validate.

The audit explicitly forbids the agent from inventing content for these — they must come from authoritative sources.

---

## Tasks

### F-20.12 (CRITICAL) — Author full N4 kanji whitelist (~280 entries)

- **Recipe:** procedure-manual Appendix B.12.1
- **Tool to author:** `tools/extract_n4_kanji_from_tanos.py`
- **Sources:** Tanos N4 kanji list (`http://www.tanos.co.uk/jlpt/jlpt4/kanji/`) cross-referenced with JLPT Sensei N4 list
- **Output:**
  - `data/n4_kanji_whitelist.json` (sorted list of 280 glyphs)
  - `data/kanji.json` populated with on/kun + tier per kanji
- **Tier classification:** `prerequisite_n5` for kanji already in N5 whitelist; `core_n4` for new N4 additions
- **CI guard:** N4-version of JA-12 (whitelist ↔ readings JSON consistency) + JA-13 (no out-of-scope kanji in user-facing data)

### F-20.13 (CRITICAL) — Author full N4 vocab inventory (~1500 entries)

- **Recipe:** procedure-manual Appendix B.12.2
- **Tool to author:** `tools/extract_n4_vocab_from_tanos.py`
- **Source:** Tanos N4 vocabulary CSV
- **Output:**
  - `KnowledgeBank/vocabulary_n4.md` (markdown source-of-truth)
  - `data/vocab.json` derived via `tools/build_data.py`
- **Sectioning:** mirror N5 structure (40 thematic sections) with N4 expansions for concepts not covered at N5 (work, travel, complex feelings, etc.)
- **Group-1 ru-verb exceptions:** flag both in section header AND per-entry, matching N5 convention
- **CI guard:** N4-version of JA-4 (vocab reading uniqueness)

### F-20.14 (CRITICAL) — Author full N4 grammar pattern catalog (~210 entries)

- **Recipe:** procedure-manual Appendix B.12.3
- **Tool to author:** `tools/extract_n4_grammar_from_bunpro.py`
- **Sources:** Bunpro N4 grammar list + Tanos N4 grammar list (cross-reference)
- **Output:**
  - `KnowledgeBank/grammar_n4.md` (markdown source-of-truth)
  - `data/grammar.json` derived via `tools/build_data.py`
- **Tier classification per pattern (per procedure-manual Appendix A.7):**
  - `core_n4` = present in BOTH Bunpro N4 and Tanos N4
  - `late_n4` = present in Bunpro N4 only
  - `n3_borderline` = listed by Tanos as N3 but commonly taught at N4
- **Promote ~30-40 N5 borderline patterns** with `tier: "late_n5"` to N4 `core_n4`
- **CI guard:** N4-version of JA-21 (no N4-grammar markers without tier flag — but inverted to "no N3-grammar markers without n3_borderline tier")

---

## Estimated effort

Per the procedure manual's §13 effort table:

| Phase | Mode A (human + AI) | Mode B (one-shot agent) |
|---|---|---|
| F-20.12 (kanji) | 2-3 days | ~2-4 hours (script + run) |
| F-20.13 (vocab) | 5-7 days | ~6-12 hours (script + run + manual section assignments) |
| F-20.14 (grammar) | 7-10 days | impossible without native review (the tier assignments + meaning_en authorings genuinely need linguist judgment) |

A zero-interaction agent should ship F-20.12 + F-20.13 fully, plus a *scaffolded* F-20.14 (extracted patterns with tier defaults, meaning_en stubbed for ~50 patterns max). Full-quality F-20.14 needs a human review pass.

---

## Dependencies on N5 repo

The N4 project depends on:

- **`specifications/procedure-manual-build-next-jlpt-level.md`** (the playbook)
- **`specifications/procedure-manual-appendix-b-extracted-from-n5.md`** (the appendix with extracted schemas, BNF grammars, integrity-check rules)
- **`tools/build_data.py`** (port verbatim — derives JSON from KB markdown)
- **`tools/check_content_integrity.py`** (port + extend with N4 rules)
- **`tools/check_design_system.py`** (port verbatim — Zen Modern is level-agnostic)
- **`tools/llm_audit.py`** (port + adjust prompt for N4 scope)
- **`tools/link_grammar_examples_to_vocab.py`** (port verbatim)
- **`css/main.css`** (port verbatim — design system is level-agnostic)
- **`js/*`** (~25 modules port verbatim)
- **`KnowledgeBank/grammar_n5.md`, `vocabulary_n5.md`, `kanji_n5.md`** (consult for tier-promotion candidates)

The N5 source files are *required inputs* for the N4 build per procedure-manual Appendix A.1.

---

*End of N4 planning doc. Re-incorporate into a dedicated N4 repo when that project starts.*
