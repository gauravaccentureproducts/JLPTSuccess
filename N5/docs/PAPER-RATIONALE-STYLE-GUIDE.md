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

## Anti-patterns to AVOID in non-moji-Mondai-2 rationales (added 2026-05-24)

The minimal style above is INTENTIONAL for moji Mondai 2 only. For
all OTHER paper sections, `rationale_hi` must be natural Hindi prose
that explains the underlying grammar / vocabulary / comprehension
point. Specific anti-patterns surfaced by external reviewers and
locked by **JA-160**'s 7-pattern marker set:

| Anti-pattern | Example (BROKEN) | Why it's wrong |
|---|---|---|
| `कुछ एक` | `コーヒー है कुछ एक पेय` (goi-1.1, v1.16.8) | "some one" English anglicism — Hindi doesn't compound `कुछ` + `एक` this way |
| `है में` | `माता काम करता है में अस्पताल` (dokkai-2.5, v1.16.8) | Copula + postposition wrong order — postposition `में` comes BEFORE the verb, not after |
| `करना यह` | `(जहाँ आप करना यह)` (bunpou-1.8, v1.16.8) | Infinitive `करना` + demonstrative `यह` doesn't form a valid Hindi construction |
| `नहीं में सब` | `ぜんぜん + नकारात्मक = "नहीं में सब"` (goi-3.4, v1.16.8) | Literal English-to-Hindi transfer of "not in all" — meaningless Hindi |
| `करता है में` | (subsumed by above patterns) | Masculine verb + locative wrong shape |
| `है कुछ एक` | `コーヒー है कुछ एक पेय (のむ)` (goi-1.1, v1.16.8) | Compound anglicism (combines `है में` + `कुछ एक`) |
| `चाहना को` | `भूखा + चाहना को खाना` (bunpou-3.7, v1.16.10) | Infinitive `चाहना` (want.INF) + object-marker `को` + noun is non-standard Hindi; the natural shape is `X करना चाहना` ("want to do X") with X as the action, not `चाहना को X` |

**Repair shape (natural Hindi).** When rewriting a flagged
rationale_hi, follow these rules:

1. **Use natural Hindi SOV.** Subject + Object + Verb. Postpositions
   come AFTER the noun they govern, not separated by copula.
2. **Preserve Japanese in 「」 brackets.** Cite the Japanese form
   directly (`「～たい」`, `「に」`, `「で」`) so the learner sees the
   grammatical token being explained.
3. **End with the N5 pedagogy hook.** A clause like `N5 का मूल
   पैटर्न: 場所 + で + क्रिया।` or `N5 इच्छा-पैटर्न।` ties the
   explanation back to the N5 syllabus.
4. **Hindi auxiliary verbs over romaji infinitives.** Use
   `खाना चाहता हूँ` (want to eat) not `*खाना चाहना को*`. The
   auxiliary `चाहना` agrees with the main verb's tense/person.
5. **Don't translate from memory.** Re-read the stem + correct
   answer before composing the rationale. Reviewer-recalled
   translations (Project-Knowledge cache effect, prior-session
   memory) produce stale strings that look right but don't
   match current data.

**Examples of natural-Hindi rewrites (post-fix, v1.16.11):**

```text
bunpou-3.7 (～たい "want to eat"):
  BROKEN: "भूखा + चाहना को खाना।"
  FIXED:  "「～たい」 इच्छा-रूप ("करना चाहना")。 おなかが すいた
          (भूख लगी) → 「たべたい」 (खाना चाहता हूँ)। N5 इच्छा-पैटर्न।"

bunpou-1.7 (に particle for time):
  BROKEN: "समय का क्रिया-कर्म।"
  FIXED:  "「に」 कण निश्चित समय-बिंदु बताता है (कब कार्य होता है)।
          七時に = "सात बजे" (जागने का निश्चित समय)। N5 का मूल समय-पैटर्न।"
```

## Cross-reference

- `prompts/Japanese language Accuracy check.txt` — overall audit prompt
  (§A89 RECALL-NOT-READ + §A90 REAL-pattern + STALE-entries)
- `docs/REVIEW-PACKET-PROMPT.md` — reviewer-facing prompt (3-block
  BINDING preflight + STALE-MARKER list + anti-patterns table)
- `tools/check_content_integrity.py` — JA-160 (7-marker word-salad
  lock) + JA-161 (12-marker preflight defense lock)
- `JLPT Common/procedure-manual-build-next-jlpt-level.md` — F.44.27
  (RECALL-NOT-READ defense) + F.44.29 (REAL-pattern + STALE-entries
  sub-pattern)
