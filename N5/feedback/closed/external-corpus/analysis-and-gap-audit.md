# learnjapaneseaz.com extraction — analysis and gap audit

**Source:** `feedback/external-corpus/learnjapaneseaz-extract.json`
**Date:** 2026-05-01
**Sample:** 218 questions extracted (21 of 25 kanji tests, 9 of 17 vocab tests, 16 of 23 reading tests)

---

## 1. Format taxonomy (across all 65 source tests)

| Format | Source tests | Question shape | Equivalent in our app |
|---|---|---|---|
| **Kanji-reading MCQ** | kanji 1-15 | Underlined kanji word in JA stem + 4 kana choices | We have *moji_questions_n5.md* but data/questions.json doesn't expose this format. **Gap.** |
| **Kanji-writing MCQ** | kanji 16-25 (mixed) | Given kana, pick correct kanji from 4 kanji choices | Not in our app. **Gap.** |
| **Vocab blank-fill** | vocab 1-3, 6-7 | Sentence with （　）+ 4 vocab choices | Matches our `mcq` type. **Have parity.** |
| **Vocab paraphrase** | vocab 4-5, 15, 17 | Given a sentence, pick the synonymous one from 4 alternatives | Not in our `mcq` distribution. **Gap.** |
| **Reading short** (Mondai 4) | reading 1-23 | 1 passage + 2 questions: (a) fill-blank, (b) comprehension | We have this exactly. **Have parity.** |
| **Reading info-search** (Mondai 6) | none observed in source | Schedule / menu / signage + comprehension | We have 3 (n5.read.007/017/021). **We have richer info-search coverage than this source.** |

---

## 2. What the external corpus reveals about scope

### 2.1 Kanji we don't currently have but the external uses heavily

Looking at the kanji tests' underlined targets:

| Kanji | External uses | Our N5 whitelist | Note |
|---|---|---|---|
| 田舎 (いなか) | test 3 | `田`,`舎` — 田 is N5; 舎 is OOS | Compound used at N5 level externally |
| 億 (おく) | test 3 | OOS | Hundred-million counter; could appear at N5 |
| 大使館 (たいしかん) | test 3 | `大` N5; `使`,`館` OOS | "embassy" |
| 銀行 (ぎんこう) | tests 5, 6, 13 | `銀`,`行` — 行 N5; 銀 N4 | Standard N5 location vocab |
| 動物 (どうぶつ) | test 2 | `動`,`物` — both N5? | Verify |
| 写真 (しゃしん) | test 2 | both N5 | OK |
| 北海道 (ほっかいどう) | test 16 | `北`,`海`,`道` N5 | OK |
| 風呂 (ふろ) | test 16 | both OOS | "bath" |
| 一週間 (いっしゅうかん) | test 14 | `一`,`週`,`間` N5 | OK |
| 荷物 (にもつ) | test 12 | `荷`,`物` — 物 N5; 荷 OOS | "luggage" |
| 黒い (くろい) | test 12 | `黒` N5? | Verify |
| 雑誌 (ざっし) | reading 15 | `雑`,`誌` OOS | "magazine" |

**Action:** Cross-reference our `data/n5_kanji_whitelist.json` against the union of kanji used in the external 21 kanji tests (~150 unique kanji). Gap candidates: 億, 使, 館, 銀, 黒, 風, 呂, 雑, 誌, 紹, 介, 卒, 業, 舎, 荷.

### 2.2 Vocabulary we don't currently have

Distinct vocab observed in external corpus that's not in our `n5_vocab_whitelist.json`:

| Word | External context | N5-appropriate? |
|---|---|---|
| かいだん (階段) | vocab 6 q1 — "stairs" | **Yes** — common N5 |
| ポケット | vocab 6 q6 — "pocket" | **Yes** — standard katakana N5 |
| わたる (渡る) | vocab 6 q8 — "to cross" | **Yes** — Genki I L13 |
| かける (眼鏡を掛ける) | vocab 6 q9 — "to wear glasses" | **Yes** — N5 collocation |
| ぬぐ (脱ぐ) | vocab 6 q10 — "to take off (shoes)" | **Yes** — N5 |
| はく (履く) | vocab 2 q7 — "to wear (lower body)" | **Yes** — N5 |
| すう (吸う) | vocab 2 q6 — "to inhale / smoke" | **Yes** — N5 |
| ひく (引く) | vocab 2 q4 + 7 q1 — "風邪を引く / catch a cold" | **Yes** — N5 collocation |
| とまる (止まる) | vocab 7 q2 — "to stop" | **Yes** — N5 |
| あまい (甘い) | vocab 7 q4 — "sweet" | **Yes** — N5 |
| くらい (暗い) | vocab 7 q5 — "dark" | **Yes** — N5 |
| わかい (若い) | vocab 7 q3 + 2 q10 — "young" | **Yes** — N5 |
| やさしい (易しい) | vocab 7 q9 — "easy" | **Yes** — N5 (note: vs 優しい "kind") |
| ニュース | vocab 7 q7 — "news" | **Yes** — katakana N5 |
| しゃわー (シャワー) | vocab 3 q10 — "shower" | **Yes** — katakana N5 |
| あびる (浴びる) | vocab 3 q10 — "to take a shower" | **Yes** — N5 collocation |
| じしょ (辞書) | vocab 3 q9 — "dictionary" | **Yes** — N5 |
| たんご (単語) | vocab 3 q8 — "vocabulary word" | **Yes** — N5 |
| すくない (少ない) | vocab 3 q8 — "few" | **Yes** — N5 |
| あのう | vocab 3 q6 — interjection "um..." | **Yes** — N5 spoken |
| たったいま | vocab 4 q2, 3 q7 — "just now" | **Yes** — N5 |

**Action:** Audit `n5_vocab_whitelist.json` against the union of all vocab used in external. Likely 30-50 N5-legitimate words missing.

### 2.3 Grammar patterns the external tests but we may not

The external corpus tests grammar through reading-fill-blanks. Patterns observed:

| Pattern | Reading test | Our coverage |
|---|---|---|
| Verb-dict + 前に | reading 20 (`朝ごはんを 食べる 前に`) | n5-119 ✓ |
| ながら simultaneous | reading 17 (`働きながら 大学院で 勉強`) | n5-022 ✓ |
| Verb-stem + に + 行く (purposive) | reading 8 (`遊びに / 買いに 行きました`) | n5-107 ✓ |
| こと nominaliser | reading 1, 2, 5 (`眠ることが できました / 読むことです`) | n5-103 ✓ |
| ～ながら + relative | reading 9 (`コーヒーを 飲みながら ... 話しました`) | n5-022 ✓ |
| Comparison より | reading 23 (`青いの より 2,000円 高かった`) | n5-095 ✓ |
| Counter rendaku 匹 ひき/ぴき | reading 11 (1ぴき / 12ひき / 6ぴき) | **Not directly drilled. Gap?** |
| ～たり～たり | none observed | We have via grammar (n5-094) |
| ～たら conditional | kanji 3 (`一億円あったら`) | **N4 boundary; we deliberately exclude.** |

The external corpus is **slightly more lenient** than ours on N4-boundary patterns (たら conditional, 紹介する, 卒業する, 大学院). This validates our stricter N5-scope — our content will feel "lower-N4-level" to a strict-N5 learner, but we're aligned with where the official JLPT actually lands.

---

## 3. What our corpus has that the external doesn't

| Feature | Our app | External |
|---|---|---|
| Sentence-order drills | 16 questions | None |
| Text-input drills | 9 questions | None |
| Per-pattern grammar deep-dives | 187 patterns × multi-example | None |
| Audio for every reading + listening | 30 + 12 items | None |
| FSRS-4 SRS | yes | none |
| Info-search reading (Mondai 6) | 3 passages | none |
| Mock-test mode with proper question distribution | yes | none |
| Dark mode + i18n + PWA offline | yes | none |

**Conclusion:** Our app is broader and deeper. The external corpus is a **focused MCQ-drill bank** at ~3x our raw question volume, but lacks the surrounding learning infrastructure.

---

## 4. Use cases for the imported corpus

### 4.1 Audit ammunition (use it to find OUR errors)

We have 138 mcq + 16 sentence_order + 9 text_input = 163 questions. Cross-checking patterns:

- **Counter rendaku consistency:** External reading-11 explicitly tests ひき / ぴき distinction. Our n5-108 covers counters but doesn't directly drill the 1/6/8/10 → ぴき rule. **Action:** Add 2-3 sentence_order or text_input questions on this rule.
- **Particle pairs in passages:** External heavily tests に vs で in employment contexts (病院に勤める / 会社で働く, reading 17). We test these in standalone question stems. **Action:** Add reading-context test for に vs で employment (we can author this since we've seen the format).
- **Family kinship paraphrase:** External vocab-15 tests おじさん = おかあさんの おにいさん. We test family terms in `n5.read.022` etc. but not as paraphrase chains. **Action:** Could add 3-4 paraphrase-style text_input questions.
- **Time relative paraphrase:** External vocab-15 tests おととい = ふつかまえ. Useful synonym chain. **Action:** Author 2-3 paraphrase questions on time vocabulary.

### 4.2 New question seeds (use it to grow OUR corpus)

The external paraphrase-format questions (vocab tests 4, 5, 15, 17 = ~22 examples) are a **format we don't have**. We could:

- Add a new `paraphrase` question type to data/questions.json schema
- Author ~15-20 paraphrase questions modeled on the external pattern
- Each paraphrase tests vocab-equivalence (synonym/antonym/calculated equivalence)

This would grow our bank from 163 to ~180 with a new question-type category.

### 4.3 Curriculum scope validation (confirm our scope is right)

Cross-checking external scope against ours:

- **External is more lenient on N4-edge:** uses 雑誌, 紹介する, 卒業, 大学院, ～たら conditional, ～ながら + relative clause.
- **Our scope is stricter (per `tier: "late_n5"` flag in reading.json):** we explicitly tag/contain these as late-N5 instead of mixing with core-N5.
- **Our stricter approach is defensible:** real JLPT N5 is closer to our scope. The external corpus is "exam-prep with realistic dilution" — i.e., ~10% N4 leakage that mirrors the real test's hardest 10%.

**Action:** Document this scope-discipline difference in spec supplement so future authors don't drift.

### 4.4 Distractor-quality benchmark

The external distractors are consistently:
- **Plausible:** all 4 are real Japanese words / forms.
- **Same word-class:** all nouns OR all verbs OR all adjectives within an option set.
- **Length-symmetric:** 4 choices have similar character counts.
- **Phonetically near-similar (kanji-reading tests):** お**な**じ / お**う**じ / そ**う**じ / ど**う**じ — minimal-pair distractors.

Our F-14 audit found pattern-meta questions where distractors mixed pattern labels with single particles. The external corpus shows what good looks like. **Action:** Add this as a question-authoring-style note in README.

---

## 5. Concrete authoring proposals (priority-ranked)

### P0 — Immediately useful for our corpus

1. **Add ~10 paraphrase-style text_input/mcq questions** modeled on external vocab-15 / vocab-17. Each tests vocab equivalence:
   - おととい = ふつかまえ
   - おじさん = おかあさんの おにいさん
   - くらい = あかるくない
   - ふくをせんたくする = ふくをあらう
   - リーさんが もりさんに かす = もりさんが リーさんから かりる
   - This adds a new pedagogical surface (synonym recognition) we currently lack.

2. **Add 3-5 counter-rendaku drills** as text_input:
   - 1階 → いっかい
   - 6本 → ろっぽん
   - 1杯 → いっぱい
   - 3階 → さんがい (rendaku)
   - 1分 → いっぷん
   - These currently appear as readings on the Counters page but aren't drillable as MCQ/text-input.

3. **Add 3-4 reading-context particle questions** modeled on external reading 9, 17:
   - "私は バス（）会社（）行きます" (で / に / で)
   - Tests particle selection in connected discourse (richer than our isolated-particle MCQs).

### P1 — Worth doing if time

4. **Add ~5 kanji-writing MCQ questions** (give kana, pick correct kanji from 4 visually-similar options). The external tests 16-25 show this is a standard JLPT format. Currently we only test kanji-recognition (reading) via the Kanji deep-dive page; not as graded MCQ.

5. **Add a `paraphrase` question type** to questions.json schema. Documented in README. Renderer needs minor update to format the "given X, pick equivalent" prompt.

### P2 — Roadmap

6. **Re-audit `n5_vocab_whitelist.json`** against the union of all vocab observed in the external 218 questions. Estimated 30-50 missing core-N5 words (kaiダん, ぬぐ, わたる, ひく, とまる, etc).

7. **Add `tier` taxonomy to grammar.json** (parallel to reading.json). Current grammar lacks core_n5 vs late_n5 distinction; the external corpus's N4 leakage shows where the boundary is.

---

## 6. Recommended next action

**Start with proposal #1 (paraphrase questions, P0).** Highest-yield: it adds a missing pedagogical surface, uses a proven external format, and grows our bank. Concrete plan:

1. Define a new `paraphrase` question type in `data/questions.json` schema
2. Author 10 paraphrase questions in a new `tools/_author_paraphrase_batch.py` one-shot script (same pattern as Pass-14 Phase F)
3. Update the test/drill renderers if needed
4. Re-run integrity (JA-18 / JA-20 may need extending to paraphrase format)
5. Commit

Estimated effort: ~30 min for the script + author, plus renderer time if changes are needed.
