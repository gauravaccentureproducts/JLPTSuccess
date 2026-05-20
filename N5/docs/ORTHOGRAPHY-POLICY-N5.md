# N5 Orthography Policy — kana vs kanji for whitelist words

**Set 2026-05-21.** Resolves the REG-001 SWEEP-5 declined item
(AUDIT-COVERAGE Part 29).

## TL;DR

**N5 orthography is per-word, not per-corpus.** Each N5 high-frequency
word has an established kana-vs-kanji preference in `grammar.json`'s
canonical `examples[].ja` field. Maintainers must follow the established
preference per-word, NOT impose a global "kanji-first for all whitelist
kanji" or "kana-first for all whitelist kanji" rule.

The REG-001 SWEEP-5 (D5 defect class) assumed kanji-first as the
universal convention. That assumption is incorrect against the actual
corpus.

## Empirical baseline (2026-05-21 corpus snapshot)

Standalone-word occurrence counts across `grammar.json` `examples[].ja`
fields (the canonical N5 user-facing surface):

| Word | kana count | kanji count | Established preference |
|---|---|---|---|
| わたし / 私 | 14 | 2 | **kana** |
| ともだち / 友だち | 35 | 14 | **kana** |
| ひと / 人 | 6 | 25 | **kanji** |
| じょうず / 上手 | 11 | 1 | **kana** |
| くるま / 車 | 19 | 0 | **kana** |
| ほん / 本 | 52 | 41 | **kana** (slight) |
| みず / 水 | 3 | 2 | **kana** (slight) |
| はな / 花 | 4 | 2 | **kana** |
| やま / 山 | 2 | 6 | **kanji** |
| うみ / 海 | 3 | 0 | **kana** |
| まち / 町 | 11 | 0 | **kana** |
| せんせい / 先生 | 10 | 17 | **kanji** |
| がくせい / 学生 | 14 | 5 | **kana** |
| にほん / 日本 | 16 | 9 | **kana** |
| えいご / 英語 | 5 | 0 | **kana** |
| しゃしん / 写真 | 7 | 0 | **kana** |
| しんぶん / 新聞 | 6 | 0 | **kana** |
| てがみ / 手紙 | 3 | 0 | **kana** |
| じかん / 時間 | 3 | 4 | **kanji** (slight) |
| しごと / 仕事 | 20 | 0 | **kana** |
| かぞく / 家族 | 1 | 0 | **kana** |

## Per-word policy

The corpus convention is established per-word by observed frequency. Where
a word's preference is **>2x** of the alternative, treat as the canonical
form for that word in new content.

**Kanji-preference words** (use the kanji form):
  - 人 (25× vs 6× kana)
  - 山 (6× vs 2× kana)
  - 先生 (17× vs 10× kana)

**Kana-preference words** (use the kana form):
  - わたし (14× vs 2× kanji)
  - ともだち (35× vs 14× kanji)
  - じょうず (11× vs 1× kanji)
  - くるま (19× vs 0× kanji)
  - 諸: 海 (うみ), 町 (まち), 英語, 写真, 新聞, 手紙, 仕事, 家族 — all 0 kanji usage at N5

**Borderline (<2x preference) — use case-by-case judgment**:
  - ほん vs 本 (52 vs 41)
  - みず vs 水 (3 vs 2)
  - じかん vs 時間 (3 vs 4)

## Why this convention (rationale)

This policy reflects pedagogical decisions baked into the corpus over time:

1. **N5 = beginner stage.** Words a beginner would WRITE in hiragana
   stay in hiragana even if the kanji is in the whitelist. This matches
   Genki I (lessons 1-12) and Minna no Nihongo I (lessons 1-25)
   convention — both textbooks introduce many N5 words first in kana
   even when the kanji is taught alongside.

2. **Recognition vs production.** N5 kanji whitelist is the
   RECOGNITION target (you should recognize 人 in real-world text). The
   PRODUCTION target is whatever maximizes learner comprehension at the
   N5 stage — usually kana for daily-life nouns, kanji for nouns that
   are common in textbook contexts (先生, 学校, 日本).

3. **Word-level convention.** Some words "feel" more kanji even at
   beginner level (e.g., 先生 — the kanji is so canonical it's almost
   logo-like). Others stay in kana (e.g., ともだち — the kanji 友
   exists but the kana form is what beginners read in textbooks).

## What this means for REG-001 SWEEP-5

The original SWEEP-5 in the REG-001 bug spec (D5 defect class) flagged
21 occurrences of わたし / ともだち / じょうず in kana within register
example blocks as "violations" of supposed kanji-first policy. **All 21
are correct per this policy.** SWEEP-5 closes as **policy-aligned**,
not "declined-with-reason".

## What this means for CI / future audits

No new CI invariant for orthography enforcement at this time. The
existing JA-100 (kanji.json compound forms vs vocab.json forms) covers
the data-integrity dimension; this policy doc covers the per-word
preference dimension at the example level.

If a future audit wants to flip a specific word's preference (e.g.,
adopt 私 as the kanji-preference for わたし), the path is:

1. Update this policy doc to flip the preference
2. Bulk-rewrite the affected `examples[].ja` fields
3. Update the relevant vocab.json entries
4. Add a CI invariant that the canonical form (per-word) is used
5. Re-render audio if pronunciation changes (it doesn't for わたし vs 私 — same reading; same for the others on this list)

## What is NOT in scope

- Verb endings (kana vs kanji for verb stems): separate policy. Most
  verbs use kana stems (たべる not 食べる) at N5 examples, but kanji
  in headwords (vocab.json `lemma`).
- い-adjectives in kana vs kanji (たかい vs 高い): separate.
- Place names: usually kanji even at N5 (日本 / 東京 etc.).
- Pitch-accent rendering: orthogonal.
- The N5 kanji whitelist itself: JA-13 + JA-14 cover that.

## Bounded coverage

This policy reflects *the corpus convention as of 2026-05-21*. It does
not prescribe what's universally correct in Japanese — different
publishers (Genki, Minna, native materials, news) follow different
conventions. The policy is internal to JLPTSuccess N5; consistency
within the project is the goal.
