# JLPT N5 Tutor — Native-Reviewer Dossier

Generated: 2026-05-02
Source revision: see git log on `data/` directory at this commit
Review channel: file findings into `review_log.csv` (template included)

## Purpose

This pack is the single bundle a native-Japanese teacher needs to
audit the live JLPT N5 corpus end-to-end. Every entry has a stable ID
(e.g. `n5-001`, `n5.kanji.人`, `n5.read.001`) — the reviewer cites
that ID in the log; we map the citation back to the source file
without ambiguity.

## Files in this dossier

| File | Scope | Reviewer attention |
|---|---|---|
| `01_grammar_patterns.md` | 177 grammar patterns | Confirm each pattern's *meaning_en* + *notes* match standard N5 textbook framing. Flag any example that sounds unnatural to a native ear. |
| `02_vocab_borderline.md` | ~100 vocab entries with high register / usage variability | Flag entries where the gloss obscures a register split (e.g. casual vs polite vs formal). |
| `03_kanji_readings.md` | 106 kanji | Confirm primary reading (see precedence rule below). Flag any entry where the listed primary is not the most common N5-context reading. |
| `04_reading_passages.md` | 30 dokkai passages + comprehension Qs | Especially Pass-15 rewrites (flagged inline). Naturalness > textbook-strictness for these. |
| `05_listening_scripts.md` | 30 listening dialogues | Speaker-turn naturalness; pacing of greetings; correctness of context (e.g. shop vs office vs school register). |

## Severity rubric (use in `review_log.csv`)

| Severity | Definition |
|---|---|
| CRITICAL | Factually wrong (false claim about Japanese grammar / wrong reading / etc). Must fix before next release. |
| HIGH | Unnatural-but-not-wrong (a native speaker would phrase it differently). Should fix. |
| MEDIUM | Polish / register / nuance. Fix when convenient. |
| LOW | Style preference — e.g. "I'd use 〜じゃ instead of 〜では here." Optional. |

## Issue format

In `review_log.csv`, one row per finding. Required fields:

- `id` — the cited pattern/word/passage/script ID
- `field` — which field has the issue (e.g. `meaning_en`, `examples[2].ja`, `notes`)
- `severity` — CRITICAL / HIGH / MEDIUM / LOW
- `finding` — what's wrong, in 1-2 sentences
- `suggested_fix` — concrete replacement text (ideal) or "discuss" (if it needs a chat)

Optional:

- `reviewer_initials` — for multi-reviewer setups
- `confidence` — 1-5 (5 = certain; 1 = "I'd want to check with a colleague")

## Kanji primary-reading precedence (file 03)

Each kanji record lists `on:` and `kun:` reading lists, and may also
carry an explicit `primary_reading:` field. The runtime surfaces the
primary in this order:

1. If `primary_reading:` is set explicitly, that's the primary
   regardless of which list it came from.
2. Otherwise: if the kanji has any kun readings, the **first kun**
   is primary (the standalone i-adjective / verb-stem form is what
   N5 learners encounter first — see `高い`, `長い`, `安い`, `白い`).
3. Otherwise: the **first on** is primary.

Some kanji are genuinely tied (e.g. `新` — 新聞 しんぶん and 新しい
あたらしい are both N5 contexts). For those, either reading is
acceptable as primary; the listed one is fine unless you have a
strong textbook-aligned reason to swap.

## Empty meaning_ja in file 01

Some grammar patterns have a `meaning_ja:` field that contains only
the pattern itself in 「」 brackets (e.g., `「いつ・どこ まで」` for
`まで`). This is intentional — those patterns are particles or
function words whose meaning is best explained in English at N5
level; a Japanese gloss would be circular. **Skip these as
"deliberately blank"** unless you can supply a learner-friendly
Japanese explanation that adds information beyond the pattern itself.

## Turnaround

Recommended cadence: 2-3 hours per file (5 files = 10-15h total). The
reviewer can return finished `review_log.csv` in batches; the dev
side processes by severity tier.
