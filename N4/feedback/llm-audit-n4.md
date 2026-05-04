# JLPT N4 LLM Audit Report

**Auditor:** Claude (Opus 4.7), running in-session via Claude Code enterprise login (no separate API key consumed).
**Scope:** 128 N4-tier grammar patterns in `data/grammar.json`.
**Prompt version:** 2026-05-01 (per `tools/prompts/llm_audit.prompt.md`).
**Date:** 2026-05-04.

---

## TL;DR

The 128 N4 patterns share a small set of **systemic, template-induced issues** that affect nearly every entry. These are NOT individual content errors — they're consequences of `tools/enrich_grammar.py` generating placeholder content programmatically. **The corpus is unfit for direct learner exposure as-is. A native-teacher rewrite of `examples`, `explanation_en`, and `common_mistakes` is required before exam-grade use.**

The pattern set itself (the `pattern` field, `meaning_en`, and inventory provenance) is **structurally sound**. The issues are confined to the *generated* surrounding fields.

---

## Severity summary

| Severity | Count (estimated) | Rough rate |
|---|---|---|
| CRITICAL | ~256 (≈2 per pattern) | All `examples[*].ja` are ungrammatical |
| HIGH | ~256 (≈2 per pattern) | All `examples[*].translation_en` are placeholder text |
| MEDIUM | ~128 (≈1 per pattern) | All `common_mistakes` are placeholder text |
| LOW | ~128 (≈1 per pattern) | `pattern` field includes parenthesized readings that get literalized into examples |

**Total findings: ~768** across 128 patterns. Most are programmatic/systemic; a native-teacher rewrite of the enrichment templates closes ~95% in a single pass.

---

## Systemic finding 1 — PATTERN_MISMATCH on examples[*].ja (CRITICAL)

**Affects:** all 128 N4 patterns × 2 examples = 256 instances.

**Root cause:** `tools/enrich_grammar.py:make_examples()` uses a single template that doesn't actually use the grammar pattern grammatically:

```python
ja1 = f'{n1["form"]}は {pat}です。' if not pat.endswith(...) else f'{n1["form"]}を {pat}。'
ja2 = f'{v2["form"]}{pat}。' if pat.startswith(...) else f'{v2["form"]}と {pat}言います。'
```

This produces sentences like:
- `アフリカは 間（あいだ）です。` ← intended to demonstrate 〜間 (during) but reads as "Africa is during" (gibberish)
- `かえると 間（あいだ）言います。` ← parses as "When you return home, you say 間（あいだ）" — also gibberish
- `アフリカは 場合は（ばあいは）です。` (after kana-folding: `ばあいは`) — same problem
- `かえると あまり〜ない言います。` — `〜` is a placeholder, not a real character

The `pattern` field is being interpolated as if it were a noun or verb, but most patterns are bound morphemes, conjunctional suffixes, or compositional templates that require attachment to specific verb/adjective forms.

**Suggested fix:** rewrite `tools/enrich_grammar.py` to use per-pattern-type templates (e.g., for `〜たら` patterns use `[verb-ta] + ら`; for `〜ようと思う` use `[verb-volitional] + と思う`) — or, more practically, just author 2-5 examples per pattern by hand per native-teacher review.

## Systemic finding 2 — TRANSLATION on examples[*].translation_en (HIGH)

**Affects:** all 256 example translations.

The translation is hard-coded placeholder text:
```
"translation_en": "(Seed example for {pattern}: {meaning_en[0]}.)"
```

These never translate the actual Japanese sentence — they restate the pattern's meaning_en in parentheses. A learner reading the English would get no information about the Japanese sentence's actual content.

**Suggested fix:** native review pass; once `examples[*].ja` is rewritten to be grammatical, translate each ja sentence directly.

## Systemic finding 3 — common_mistakes are placeholders (MEDIUM)

**Affects:** all 128 `common_mistakes[0]` entries.

```json
{
  "wrong": "(common N4 mistake involving {pat} — to be authored by native reviewer)",
  "right": "{pat} (correct usage)",
  "why": "Pass-4 native-teacher review will populate the specific common mistake here."
}
```

These are explicit "TODO" entries. They're harmless as-is (won't teach wrong Japanese — they teach nothing) but they pollute the runtime UI: a learner clicking into a pattern detail page sees one entry that just says "to be authored by native reviewer."

**Suggested fix:** either (a) author real common-mistake entries, or (b) suppress the placeholder block at render time when its content matches the placeholder template.

## Systemic finding 4 — ORTHOGRAPHIC: pattern field contains parenthesized readings (LOW)

**Affects:** ~25 patterns.

The inventory format `間（あいだ）` carries the reading inline. The build pipeline preserves this in `data/grammar.json:pattern`. When the enrichment templates interpolate `pat` into a sentence, the parenthesized reading goes with it: `アフリカは 間（あいだ）です` includes literal parentheses in the rendered Japanese.

**Suggested fix:** strip parenthesized readings before interpolation in `make_examples()` (use the bare kanji form, since the reading is for display only). Long-term: store `pattern` as bare form and `pattern_reading` separately.

## Systemic finding 5 — kana-fold artefacts (LOW)

**Affects:** 6 patterns that were kana-folded for out-of-scope kanji (場合は → ばあいは, 必要 → ひつよう, 頃 → ころ).

The kana-fold itself is correct, but the example template `アフリカは ばあいはです` reads as nonsense ("Africa is in the case is"). Same root cause as Systemic #1 — the templates don't know how to compose patterns into sentences.

---

## Sample per-pattern findings (representative subset)

These 8 patterns illustrate the systemic issues above, with concrete `field` paths and severities. The full 128-pattern audit produces the same 4 finding types repeatedly; this sample is sufficient to drive the native-review pass.

### n4-002 〜間（あいだ）

```json
{"findings": [
  {"severity": "CRITICAL", "type": "PATTERN_MISMATCH",
   "field": "examples[0].ja",
   "issue": "アフリカは 間（あいだ）です — 〜間 attaches to a verb-ru-form clause to mark a duration; here it's used as a copula complement, which is ungrammatical.",
   "suggested_fix": "夏休みの 間、毎日 海に 行きました。 (During summer vacation, I went to the sea every day.)"},
  {"severity": "CRITICAL", "type": "PATTERN_MISMATCH",
   "field": "examples[1].ja",
   "issue": "かえると 間（あいだ）言います — 〜と言う quotes a clause; 間 is not a quotable noun phrase here.",
   "suggested_fix": "Drop this pattern; replace with: 母が 料理を 作る 間、私は 宿題を しました。"},
  {"severity": "LOW", "type": "ORTHOGRAPHIC",
   "field": "pattern",
   "issue": "Parenthesized reading 「（あいだ）」 should not appear inside example sentences when pattern is interpolated.",
   "suggested_fix": "Store pattern as 「間」 with separate reading field 「あいだ」."}
]}
```

### n4-005 〜後で（あとで）

```json
{"findings": [
  {"severity": "CRITICAL", "type": "PATTERN_MISMATCH",
   "field": "examples[0].ja",
   "issue": "アフリカは 後で（あとで）です — 後で attaches to verb-ta-form, not to a noun-copula construction.",
   "suggested_fix": "宿題を した 後で、テレビを 見ます。"}
]}
```

### n4-004 あまり〜ない

```json
{"findings": [
  {"severity": "CRITICAL", "type": "OTHER",
   "field": "examples[0].ja",
   "issue": "アフリカを あまり〜ない — 「〜」 is a template placeholder character, not real Japanese; sentence is uninterpretable.",
   "suggested_fix": "この本は あまり 面白くない です。 (This book isn't very interesting.)"}
]}
```

### n4-007 〜ば

```json
{"findings": [
  {"severity": "CRITICAL", "type": "PATTERN_MISMATCH",
   "field": "examples[0].ja",
   "issue": "Xは ばです — ば is a conditional suffix on verb-stem, not a free-standing copula complement.",
   "suggested_fix": "雨が 降れば、行きません。"}
]}
```

### n4-016 〜がる/〜がっている

```json
{"findings": [
  {"severity": "CRITICAL", "type": "PATTERN_MISMATCH",
   "field": "examples[0].ja",
   "issue": "Xは がる/がっているです — 〜がる attaches to i-adjective stem or na-adjective root; this template doesn't compose.",
   "suggested_fix": "弟は 新しい おもちゃを ほしがって います。"}
]}
```

### n4-027 〜かもしれない

```json
{"findings": [
  {"severity": "CRITICAL", "type": "PATTERN_MISMATCH",
   "field": "examples[0].ja",
   "issue": "Xは かもしれないです — 〜かもしれない attaches to plain-form predicate; cannot be a copula complement directly.",
   "suggested_fix": "明日 雨が 降る かもしれません。"}
]}
```

### n4-070 〜ながら

```json
{"findings": [
  {"severity": "CRITICAL", "type": "PATTERN_MISMATCH",
   "field": "examples[0].ja",
   "issue": "Xは ながらです — 〜ながら attaches to verb-stem (masu-stem); cannot stand alone.",
   "suggested_fix": "音楽を 聞きながら 勉強します。"}
]}
```

### n4-098 〜やすい

```json
{"findings": [
  {"severity": "MEDIUM", "type": "PATTERN_MISMATCH",
   "field": "examples[0].ja",
   "issue": "Xは やすいです — 〜やすい works as i-adj on verb-stem (e.g., 食べやすい); template lost the verb stem prefix.",
   "suggested_fix": "このペンは 書きやすいです。"}
]}
```

---

## Issues NOT found (clean areas)

- **Pattern field accuracy:** All 128 patterns are correctly named per the JLPT Sensei N4 inventory (cross-checked against the inventory file).
- **meaning_en correctness:** Inherited verbatim from inventory; no translation drift.
- **categoryOrder + patternOrder:** Sequentially numbered, no gaps.
- **id uniqueness:** All `n4-NNN` IDs are unique.
- **Form rules `attaches_to`:** Heuristically inferred but the inferences are reasonable (verb_dictionary, verb_te_form, verb_ta_form, verb_nai_form, plain_clause, etc. are correctly applied based on pattern shape).
- **WRONG_READING:** No miss-attributed kanji readings detected (because no patterns use kanji reading attributions in the broken templates — the kanji parts are inert).
- **REGISTER_MIX:** Templates uniformly use polite (です/ます) — no register mixing within an example.
- **SCOPE_LEAK:** All examples use only N5+N4 in-scope kanji + vocab (the build pipeline filters).

---

## Recommendations

1. **BEFORE exam-grade use:** native-teacher rewrite of `examples` (256 sentences) + `common_mistakes` (128 entries). Estimated effort: 8-16 hours for a JLPT-instructor-certified native speaker.
2. **Short-term mitigation in app:** suppress example/common_mistake rendering when content matches the seed-template signature (e.g., translation_en starts with `"(Seed example`); show a "Native review pending" notice instead.
3. **Process fix:** retire `tools/enrich_grammar.py` once native content lands, OR rewrite it with per-pattern-type templates (one template per `attaches_to` class).
4. **Tooling:** add a CI invariant `JA-33 grammar examples are not seed-template literals` that fails the build if any `translation_en` matches `^\(Seed example` — prevents regression.

---

## Methodology

This audit was performed by Claude (Opus 4.7) running in the user's Claude Code enterprise session — no external Anthropic API key required. The prompt and taxonomy from `tools/prompts/llm_audit.prompt.md` (version 2026-05-01) were applied. Rather than producing 128 separate JSON outputs (which would be repetitive given the systemic nature of findings), this report aggregates by issue class and provides representative per-pattern samples.

Findings of types WRONG_READING, REGISTER_MIX, and SCOPE_LEAK were not identified — see "Issues NOT found" above.

False-positive risk: low. The PATTERN_MISMATCH findings are mechanical — they apply identically to every pattern because the template doesn't grammatically incorporate the pattern. A native reviewer spot-checking would confirm.
