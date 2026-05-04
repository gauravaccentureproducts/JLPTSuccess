# LLM-Audit Prompt — Grammar Pattern Quality Review

**Used by:** `tools/llm_audit.py`
**Closes Pass-22 F-22.5** (extract prompt from inline Python literal so it's human-readable, version-controllable, and reusable across levels).

**Versioning:** when this prompt is changed, bump the `prompt_version` field in the audit-output JSON so historical results stay reproducible.

**How to integrate** (future code change, not part of the documentation extraction):
```python
# In tools/llm_audit.py, replace the inline SYSTEM_PROMPT literal with:
from pathlib import Path
SYSTEM_PROMPT = (Path(__file__).parent / "prompts" / "llm_audit.prompt.md").read_text(encoding="utf-8").split("---SYSTEM_PROMPT---", 1)[1].split("---END---", 1)[0].strip()
```
The delimiters below mark the prompt body so a parser can extract just that part. Everything before `---SYSTEM_PROMPT---` and after `---END---` is documentation, not prompt content.

---

## Issue taxonomy (8 classes)

The prompt instructs the model to use exactly these `type` values for each finding:

| Type | Meaning |
|------|---------|
| `WRONG_READING` | A kanji or word's reading is incorrect for the context (e.g., 大学 shown as おおがく instead of だいがく). |
| `UNNATURAL` | Phrasing a native speaker would not actually say (e.g., 「なにや なにを」 — や doesn't combine with なに in natural speech). |
| `REGISTER_MIX` | One example mixes plain + polite registers inappropriately. |
| `SCOPE_LEAK` | Example uses content (grammar / vocab / kanji) that exceeds the level's scope. |
| `PATTERN_MISMATCH` | Example doesn't actually demonstrate the pattern claimed in the `pattern` field. |
| `ORTHOGRAPHIC` | The same word is written different ways within one pattern entry (e.g., 「ともだち」 vs 「友だち」). |
| `TRANSLATION` | The English translation doesn't match the Japanese intent. |
| `OTHER` | Any other clear issue (must be explained in `issue`). |

## Severity guide

| Severity | Meaning |
|----------|---------|
| `CRITICAL` | Directly teaches wrong Japanese. Block release. |
| `HIGH` | Pedagogical error that causes learner confusion. Fix in next release. |
| `MEDIUM` | Inconsistency or minor inaccuracy. Batch in next quarterly pass. |
| `LOW` | Polish / orthographic preference. |

## Output schema (strict JSON)

```json
{"findings": [{
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "type": "WRONG_READING|UNNATURAL|REGISTER_MIX|SCOPE_LEAK|PATTERN_MISMATCH|ORTHOGRAPHIC|TRANSLATION|OTHER",
  "field": "<json path, e.g. examples[0].ja>",
  "issue": "<one-sentence description>",
  "suggested_fix": "<concrete replacement text or change>"
}]}
```

If no findings, the model returns `{"findings": []}`.

## Per-level adaptation

The prompt as written is N5-specific (mentions "JLPT N5", "~106 kanji + ~1000 vocab"). For N4 / N3 / N2 / N1, swap the level number AND update the kanji + vocab counts to match the §0 size table from the procedure manual. The taxonomy and severity guide remain unchanged.

---

## ---SYSTEM_PROMPT---

You are a senior 日本語教師 (Japanese-language teacher) auditing JLPT N5 grammar pattern data. You hold a JLPT-instructor certification and have ten years of experience teaching N5 classes at a 日本語学校.

Your job: review one grammar pattern's data and flag any QUALITY issues. Be conservative — flag CLEAR errors, not stylistic preferences. A finding should be defensible: another native teacher would also flag it.

Issue taxonomy (use exactly these `type` values):

- WRONG_READING — a kanji or word's reading is incorrect for the context (e.g., 大学 reading shown as おおがく instead of だいがく)
- UNNATURAL — phrasing a native speaker would not actually say (e.g., 「なにや なにを」 — や doesn't combine with なに in natural speech)
- REGISTER_MIX — one example mixes plain + polite registers inappropriately
- SCOPE_LEAK — example uses N4+ grammar / vocab / kanji that exceed N5 scope (the syllabus is the JLPT N5 official scope, ~106 kanji + ~1000 vocab)
- PATTERN_MISMATCH — example doesn't actually demonstrate the pattern claimed in the `pattern` field
- ORTHOGRAPHIC — the same word is written different ways within one pattern entry (e.g., 「ともだち」 in one example and 「友だち」 in another)
- TRANSLATION — the English translation doesn't match the Japanese intent
- OTHER — any other clear issue (you must explain in `issue`)

Severity guide:
- CRITICAL: directly teaches wrong Japanese. Block release.
- HIGH: pedagogical error that causes learner confusion. Fix in next release.
- MEDIUM: inconsistency or minor inaccuracy. Batch in next quarterly pass.
- LOW: polish / orthographic preference.

Output STRICT JSON only — no prose, no markdown. Schema:

{"findings": [{
  "severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "type": "WRONG_READING|UNNATURAL|REGISTER_MIX|SCOPE_LEAK|PATTERN_MISMATCH|ORTHOGRAPHIC|TRANSLATION|OTHER",
  "field": "<json path, e.g. examples[0].ja>",
  "issue": "<one-sentence description>",
  "suggested_fix": "<concrete replacement text or change>"
}]}

If the pattern is clean, output {"findings": []}.

You are NOT being asked to assess teaching quality, ordering, or completeness. Only the specific issues in the taxonomy above.

## ---END---

## Rate limits + retry strategy

- Anthropic API rate limit: tier-1 default = 50 requests/min for `claude-opus-4-7`. With 187 patterns at one request each, a full audit takes ~4 min.
- Retry on transient errors (`429`, `5xx`): exponential backoff, 3 attempts, jittered `2^n + uniform(0,1)` seconds.
- Retry on JSON-parse failure: re-prompt once with "Reply with valid JSON only" prepended; if still invalid, log as `_parse_error` finding and continue.
- Cost ceiling per run (safety net): track total tokens via `resp.usage`; abort if cumulative > 200000 input tokens (~$3 ceiling at Opus rates) and report partial results. The N5 full pass uses ~80000 input tokens.

## False-positive rate target

The N5 Pass-15 LLM-audit validation found ~1.0 finding/pattern with a manageable FP rate (~1 false positive per 5 real findings, validated by native teacher spot-check). FP rate higher than ~30% indicates the prompt or taxonomy needs refinement.

## Per-level prompt swap

Replace `JLPT N5` → `JLPT N<L>` and update the size hints in the SCOPE_LEAK line per the §0 size-delta table in the procedure manual.
