# Paper rationale style guide

**Set 2026-05-23 to address reviewer Finding 6 (FRAMING).**

## Moji Mondai 2 (orthography) rationales

`rationale_hi` fields on moji Mondai 2 (表記 / orthography) questions
follow an **intentional minimal-rationale style**:

```json
"rationale": "学 (ガク) + 生 (セイ).",
"rationale_hi": "店。"
```

The style consists of:
- **Morpheme + reading breakdown** (e.g., `学 (ガク) + 生 (セイ)`) for
  the rationale field.
- **Single-kanji or single-word recognition cue** (e.g., `店。`,
  `買います。`) for the Hindi rationale field.

This is by design. Mondai 2 tests whether the learner can recognize the
correct kanji writing of a given kana word — the discriminating
information is the kanji-form itself, not a prose explanation. A 1-2
character recognition cue is more effective than 100-character prose
for this format.

**Future reviewers:** do not flag minimal moji Mondai 2 rationales as
"incomplete" or "underexplained." If you see a 5-character rationale
on a moji Mondai 2 question, it's working as documented.

## Other paper sections

Other paper sections (Mondai 1 / 3 / 4 / 5 / 6 / 7 + goi + bunpou +
dokkai) use longer prose rationales appropriate to the question type.
The minimal style is unique to moji Mondai 2.

## Cross-reference

- `prompts/Japanese language Accuracy check.txt` — overall audit prompt
- `docs/REVIEW-PACKET-PROMPT.md` — reviewer-facing prompt (mentions this
  style guide in its anti-patterns section)
