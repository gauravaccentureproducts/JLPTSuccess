# Native-Teacher Content Review — JLPT N5 corpus (run 2)

**Conducted:** 2026-05-13 (~3 hours after run 1)
**Persona:** Same as run 1 — Japanese-native teacher with 20+ years JLPT-instruction.
**Mode:** Re-audit of `data/` folder after run-1's V-1 + G-1 + 8 medium/low fixes shipped (commits 99feeba + 8367e10).
**Trigger:** Major content-shape change since run 1 (88 vocab pitch re-derivations + 26 grammar meaning_ja rewrites + 132 listening speaker tags + 145 schema renames + new JA-70/71/72 invariants). Per anti-pattern #23, that's a valid re-audit trigger.

---

## Executive summary

**Overall: SATURATED with 3 small residual findings.** The corpus is in markedly better shape than at run 1. The HIGH findings from run 1 are closed at the data level + locked by new CI invariants. This pass surfaced 3 small residuals — none HIGH:

1. **T-1 (Medium):** 2 more cross-contaminated grammar `meaning_ja` (n5-151, n5-183) that JA-71 didn't catch because the pattern shares 1 coincidental kana with the wrong-marker text. JA-71's threshold is too lenient at 1-character overlap.

2. **T-2 (Low):** C-1 speaker tagging is correct for the 4 explicit-marker dialogue items (n5.listen.014/017/022/023) but defaults to "narrator" for all 24 announcer+content items. Technically right (those items have no explicit speaker breakdown) but not richest possible representation.

3. **T-3 (Low):** 9 reading questions use the legacy `question_ja` schema key instead of the canonical `prompt_ja`. Renderer probably handles both, but it's a schema inconsistency.

---

## Findings

### T-1 — 2 more cross-contaminated meaning_ja (Medium)

**Severity:** Medium
**Evidence:**

- **n5-151** (〜はいかがですか polite offer):
  `meaning_ja`: 「あいさつ」は まいにちの ばめんで つかう ことばです。「おはよう」「さようなら」。
  Describes greetings (n5-152 territory), not the は+いかがですか polite-offer pattern.
- **n5-183** (Question word + か / も compounds):
  `meaning_ja`: 「Verb-た／じしょけい + ことが ある」で、けいけんを いいます。「行った ことが ある」。
  Describes n5-169 (Verb-た + ことがある), not question-word compounds.

**Why JA-71 missed:** JA-71's heuristic accepts 1-character overlap between the marker and the pattern field. For n5-151: pattern has 「い」, marker 「あいさつ」 also has 「い」. For n5-183: pattern is Latin-only and the full-meaning_ja fallback found at least one kana from the pattern's first word.

**Fix:** Rewrite the 2 meaning_ja entries with correct content (1 turn). Refine JA-71 to require ≥2-character overlap OR explicit marker-substring presence (1 turn).

### T-2 — C-1 speaker tagging defaults to "narrator" for announcer+content items (Low)

**Severity:** Low
**Evidence:**

- 4 explicit-dialogue items (n5.listen.014/017/022/023) have correct male/female tagging derived from 男:/女: prefix markers in `script_ja`. ✅
- 24 announcer+content items (e.g., n5.listen.007 — male monologue with female narrator framing) have all lines tagged "narrator" because the script doesn't carry explicit speaker prefixes.
- The audio IS correctly rendered with both F and M voices (per `audio_render_meta.voices_used`), but the per-line speaker attribution requires inferring which line corresponds to which voice — which the script structure doesn't directly encode.

**Why this is Low not Medium:** the speaker tagging is **not wrong**, it's just less specific than possible. A learner reading the transcript still sees the speaker label; the label is correct (narrator) for any single-voiced line. The richer representation (line 0 = female narrator, lines 1+ = content male speaker for a "男の人が はなしています" item) would require either (a) restructuring `script_ja` to include explicit prefixes, or (b) parsing the script's first-sentence "X人が はなしています" framing to derive main-content gender.

**Fix:** Optional refinement of C-1 — improved heuristic that maps "X人が はなしています" → main-speaker-gender, and tags line 0 as the narrator's gender (typically F-narrator for the F+M plan items, M-narrator for M-only plan items). Estimated 1 turn, low priority.

### T-3 — 9 reading questions use legacy `question_ja` schema key (Low)

**Severity:** Low
**Evidence:** 94 reading questions use `prompt_ja` (canonical); 9 use `question_ja` (legacy). The 9 are all in passages n5.read.046 through n5.read.054.

**Why this is Low:** the content is correct; only the schema key differs. The renderer probably handles both — but new code/audit tools that assume `prompt_ja` will miss these.

**Fix:** Rename `question_ja` → `prompt_ja` on the 9 entries. Add JA-73 invariant: assert every reading question has `prompt_ja` (not `question_ja`). 1 turn.

---

## What is defensible (don't touch)

- Run-1 V-1 fix verified: 0 mora-count mismatches remain (excluding 17 documented multi-reading aliases).
- Run-1 G-1 fix verified: meaning_ja in the 26 originally-fixed patterns is correct + N5-kanji-clean.
- Cross-surface integrity: 0 broken vocab_id refs in grammar examples (was a worry; verified 0 hits).
- Vocab example structure: 100% of vocab entries have all examples with `ja` + `translation_en` populated. No missing data.
- Reading paragraph_summary, cultural_callout, native_audio, etc. at 100%.
- Listening voice variety (6 distinct VOICEVOX speakers): unchanged, correct.

---

## Cross-comparison: run-1 vs run-2

| Metric | Run 1 | Run 2 |
|---|---|---|
| Total findings | 10 | 3 |
| HIGH findings | 2 | 0 |
| Medium findings | 4 | 1 |
| Low findings | 4 | 2 |
| Explicit opt-outs | n/a | 0 |
| CI invariants | 70 (before adds) | 76 (after run-1 adds) |

The corpus moved from "10 findings including 2 user-visible HIGH bugs" → "3 polish residuals, no HIGH bugs." Native-teacher review reached saturation in 2 runs.

---

## Recommendation

Same shipping path as run-1: T-1 in one commit (2 meaning_ja rewrites + JA-71 refinement), T-2 in a separate commit if pursued (optional), T-3 in one commit (9 schema renames + JA-73). Total estimated: **2-3 turns** to clear T-1 + T-3; T-2 is opt-in polish.

After T-1 + T-3 ship, **run-3 would produce zero actionable findings** — the same saturation outcome as the N5Improvement audit reached. The corpus's content-quality audit cycle should follow anti-pattern #23's trigger rules going forward (re-run only on major content changes, not on calendar).

---

## Disclosure (unchanged from run 1)

This review is Claude operating in a native-teacher persona. No actual human native-speaker review has occurred. The findings reflect what such a teacher would catch given standard mora-count + JLPT-N5-scope + pedagogical-format conventions.
