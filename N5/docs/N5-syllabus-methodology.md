# JLPT N5 Syllabus, Sources, and Authoring Methodology

> **Status**: Consolidated 2026-05-14 from the former `KnowledgeBank/` directory. KB was the historical scope-reference directory; its content has been migrated here (methodology, conventions, source citations) and into the structured data files (membership scope, question content). This file is the single human-readable methodology reference; `data/*.json` files are the live source-of-truth for content and scope.

---

## Part A — Source Citations and Reference Works

The N5 content in this project is curated against a corpus of authoritative references. Each reference is consulted for **accuracy of interpretation**, not to expand the scope of N5 beyond the official syllabus.

### A.1 Official sources

- **Japan Foundation & Japan Educational Exchanges and Services (JEES)** — [https://www.jlpt.jp](https://www.jlpt.jp)
  - **N5 Sample Questions** (free PDFs hosted by JEES) — the closest authoritative reference for what an actual N5 paper looks like. Includes sample 文字 (moji), 語彙 (goi), 文法 (bunpou), 読解 (dokkai), 聴解 (chōkai) sections. Cited as 「JLPT N5 サンプル問題」 in this project for format-fidelity checks on mock paper authoring.
  - The official JLPT administering bodies. Their site provides the official test specifications, sample questions, and the "JLPT Can-do Self-Evaluation List" for each level.
- **Japan Foundation — JF Standard for Japanese Language Education** — [https://www.jfstandard.jpf.go.jp](https://www.jfstandard.jpf.go.jp)
  - Official framework developed by the Japan Foundation since 2010, based on CEFR. Defines language proficiency benchmarks (A1-C2 mapping).

### A.2 Foundational reference lists (pre-2010 official)

- **Original JLPT Test Content Specifications (しゅつだいきじゅん / *shutsudai kijun*)** — Japan Foundation (1994/2002 editions)
  - The original officially published vocabulary and kanji lists for the old Levels 3 and 4, which form the historical basis of the modern N5 list. Although the post-2010 JLPT no longer publishes an official list, this remains the academic baseline used by virtually all textbooks and study sites.

### A.3 Major textbooks (industry standards)

- **Minna no Nihongo Shokyū I** — 3A Corporation. Lessons 1-25 align closely with N5.
- **Genki I: An Integrated Course in Elementary Japanese** — The Japan Times Publishing. Chapters 1-12 cover N5. Current edition is 3rd Edition; Vol. 1 officially aligned to JLPT N5 and CEFR A1 by the publisher.
- **Try! N5** — Ask Publishing. JLPT-specific prep series.
- **Nihongo Sō-Matome N5 / Nihongo Challenge N5** — ASK Publishing / Unicom.

### A.4 Academic and educational platforms

- **Japan Foundation Marugoto** — [https://marugoto.jpf.go.jp](https://marugoto.jpf.go.jp). Official Japan Foundation course platform aligned with JF Standard / CEFR. A1 (Starter) + A2 (Elementary 1 & 2) overlap with N5.
- **Tofugu** — [https://www.tofugu.com](https://www.tofugu.com). Editorially reviewed long-form articles on Japanese grammar and kanji.
- **Imabi** — [https://imabi.org](https://imabi.org). Comprehensive grammar reference (~450 lessons across ten proficiency tiers).

### A.5 Established learner references

- **Jisho.org** — [https://jisho.org](https://jisho.org). Free Japanese-English dictionary built on JMdict/EDICT and KANJIDIC.
- **JMdict / EDICT / KANJIDIC / KANJIDIC2** — Electronic Dictionary Research and Development Group (EDRDG) — [https://www.edrdg.org](https://www.edrdg.org). Long-running open-data Japanese dictionary projects.
- **WaniKani** — [https://www.wanikani.com](https://www.wanikani.com). Structured kanji and vocabulary SRS platform.
- **Bunpro** — [https://bunpro.jp](https://bunpro.jp). Grammar-focused SRS platform organized by JLPT level.
- **NHK NEWS WEB EASY** — [https://www3.nhk.or.jp/news/easy/](https://www3.nhk.or.jp/news/easy/). Daily news rewritten for N5/N4 learners. Useful as an extension to in-corpus reading material.

### A.6 Reference grammars

- **A Dictionary of Basic Japanese Grammar** — Seiichi Makino & Michio Tsutsui (The Japan Times). Canonical academic reference for beginner-to-intermediate Japanese grammar.
- **Tae Kim's Guide to Learning Japanese** — [https://guidetojapanese.org](https://guidetojapanese.org). Free online grammar guide.

### A.7 Why these sources are reliable

- **Official authority** — JLPT site, Japan Foundation, and JEES define the test itself.
- **Editorial review** — Major textbooks (Minna, Genki, Try!) are produced by established publishers with native-speaker editors.
- **Academic grounding** — Makino & Tsutsui's dictionaries and EDRDG's dictionary projects are peer-recognized references.
- **Consensus** — Cross-referencing these sources yields the standard JLPT N5 content set used across the industry.

---

## Part B — Pedagogical-curation policy

This project's content is curated with classroom and exam outcomes in mind, not theoretical completeness.

### B.1 Pedagogical-lens principles

- **Exam realism first** — The list prioritizes *what is realistically tested at N5*, not every form, reading, or borderline item that exists in the language.
- **Conflict-resolution rule** — When sources disagree on whether an item is N5 or N4, **Minna no Nihongo + Genki overlap and frequency of appearance** is treated as the authoritative tiebreaker.
- **No silent N4 creep** — Borderline items are kept only when they appear in mainstream N5 prep textbooks, and are tagged as `tier=late_n5` or borderline rather than mixed into the Core list.

### B.2 Exam scope vs reference depth

Some references on this list (e.g., Imabi, Makino & Tsutsui, Tae Kim) go significantly deeper than the JLPT N5 syllabus. Their inclusion is intentional but bounded:

> Advanced explanatory references are used for **accuracy of interpretation** of N5 items (e.g., precise nuance of は vs が, transitive/intransitive pairs), **not to expand scope** beyond N5.

In short: deep references inform the *quality* of N5 explanations; they do not push the *quantity* of N5 content upward.

---

## Part C — Vocabulary authoring conventions

### C.1 Kanji-usage rule

To match the N5 learner's actual reading ability, vocabulary uses **only kanji that appear in the N5 kanji syllabus** (`data/n5_kanji_whitelist.json`).

- If every kanji in a word is part of the N5 syllabus, the kanji form is shown (e.g., 学生).
- If a word contains any kanji that is *not* in the N5 syllabus, the entire word is rendered in **hiragana** (or katakana for loanwords) — even if part of the word would otherwise use a known kanji. This avoids "half-known" presentations.
- Loanwords stay in their conventional katakana form.

### C.2 Tier system

- Items without a tag are **Core N5** — confidently expected at N5.
- `tier=late_n5` / **[Ext]** = *Extended / borderline* — listed by some N5 sources but commonly placed at N4 by others. Useful for recognition; do not over-prioritize.
- **[Cul]** = *Cultural / situational* — encountered in everyday Japan but rarely a focus on the N5 exam.

### C.3 Part-of-speech taxonomy

Verb classes use Japanese-grammar conventions, not English categories. Mirrors the `pos` field in `data/vocab.json`.

- **[n.]** = noun
- **[v1]** = godan verb (Group 1, consonant-stem)
- **[v2]** = ichidan verb (Group 2, vowel-stem)
- **[v3]** = irregular verb (する / 来る only at N5)
- **[i-adj]** = i-adjective
- **[na-adj]** = na-adjective
- **[adv.]** = adverb
- **[part.]** = particle
- **[conj.]** = conjunction
- **[pron.]** = pronoun
- **[count.]** = counter
- **[num.]** = numeral
- **[dem.]** = demonstrative (こ/そ/あ/ど series)
- **[Q-word]** = interrogative (なに / どこ / etc.)
- **[exp.]** = fixed expression / phrase
- **[interj.]** = interjection

### C.4 Variant policy

When two forms exist (e.g., a Sino-Japanese term plus a katakana loan), the dominant form is listed first, with the alternate noted on the same line. Some words intentionally appear under more than one section (e.g., 名前 under both *Common Nouns* and *Misc Useful Items*) because they belong functionally to multiple thematic groups. This is by design, not duplication.

---

## Part D — Kanji authoring conventions

### D.1 Reading notation

- **On'yomi** is written in **katakana** (e.g., イチ). Enforced by JA-76 invariant.
- **Kun'yomi** is written in **hiragana** (e.g., ひと). Okurigana shown in parentheses (e.g., ひと(つ)).
- A dash (`-`) means the reading is not commonly used at N5.

### D.2 Tier system

- **[Core]** — universally accepted N5 kanji. Appear in every N5 prep textbook (Minna, Genki, Try!) and are confidently tested. Untagged kanji default to Core.
- **[Ext]** = *Extended / borderline*. Listed by some N5 sources but commonly placed in N4 by others. Recognize the shape and the most common reading; do not over-prioritize.

### D.3 Pedagogical scope rule

Meanings shown are limited to the senses an N5 learner needs. Advanced senses (e.g., literary or technical readings) are intentionally omitted.

Specific reading-level annotations are captured in `data/kanji.json` per-entry on the `reading_notes` field where the kanji has out-of-scope readings the learner should know to avoid (e.g., 木 `こ-` is "N4+ prefix; recognition only").

---

## Part E — Grammar authoring conventions

### E.1 Category organization

`data/grammar.json` patterns carry a `category` field grouping them by function. The 32 categories include: Copula and Basic Sentence Structure, Particles, Demonstratives (こそあど), Question Words, Verbs - Tense and Politeness (ます-form), Verbs - Plain (Dictionary) Form and Negation, Te-form and Related Patterns, Adjectives, Existence and Possession, Comparison and Preference, Desiderative and Volitional, Counters and Quantity, Time Expressions, Conjunctions and Connectives, Giving and Receiving (basic), Asking and Stating with から/ので (basic causation), Nominalization and Modification, Common Set Patterns, Existence-of-Plans and Frequency, Functional Expressions (Non-Grammar), Other Core Patterns, Honorific / Polite Vocabulary at N5 (functional), and Additional Upper N5 / Borderline Patterns (subdivided into sub-categories).

### E.2 Tier system

The `tier` field on each pattern carries `core_n5` / `late_n5` / borderline classification. The `Additional Upper N5 / Borderline Patterns - *` categories are all tagged `late_n5` and group patterns at the N5/N4 boundary that appear in mainstream N5 lists (Bunpro, JLPT Sensei) but are commonly placed at the late-N5 / early-N4 boundary.

### E.3 Verb class rules

- **Group 1 (五段)** verbs end in a syllable from the う-row of the kana chart (う、く、ぐ、す、つ、ぬ、ぶ、む、る — all ending in `/u/` when romanized).
- **Group 2 (一段)** verbs end in -iる or -eる (e.g., みる, たべる).
- **Group-1 ru-verb exceptions:** 入る (はいる), 帰る (かえる), 走る (はしる), 知る (しる), 切る (きる), 要る (いる) look like Group 2 (-iる / -eる) but conjugate as Group 1. Six standard N5 exceptions; CI invariant X-6.6 enforces correct flagging.

### E.4 Honorific terminology — beautifying vs honorific

The お〜 / ご〜 prefixes at N5 are **beautifying language (美化語 / bika-go)**, not honorifics (尊敬語 / sonkei-go). Honorific verbs (sonkei-go) like いらっしゃる, おっしゃる are out of scope for N5.

- Productive cases: お茶, お金, おさけ, おみず, おはな.
- ごはん is a single lexicalized word now, not a productive ご-prefix; it's included in N5 vocab as one item rather than as an example of generative 美化語.

---

## Part F — Question authoring methodology

These conventions apply to the question content shipped in `data/papers/{moji,goi,bunpou,dokkai}/*.json` and `data/questions.json`.

### F.1 Subtype coverage

| Mondai | Subtype | Count | Surface |
|---|---|---|---|
| Moji M1 | 漢字読み (kanji reading) | 50 | `data/papers/moji/` |
| Moji M2 | 表記 (orthography) | 50 | `data/papers/moji/` |
| Goi M3 | 文脈規定 (contextual vocabulary) | 50 | `data/papers/goi/` |
| Goi M4 | 言い換え類義 (paraphrase) | 50 | `data/papers/goi/` |
| Bunpou M1 | 文の文法1 (sentence grammar 1) | 60 | `data/papers/bunpou/` |
| Bunpou M2 | 文の文法2 (sentence composition / 並べ替え) | 30 | `data/papers/bunpou/` |
| Bunpou M3 | 文章の文法 (text grammar) | 10 | `data/papers/bunpou/` |
| Dokkai M4 | 内容理解 短文 (short passages) | 30 passages, 60 Qs | `data/papers/dokkai/` |
| Dokkai M5 | 内容理解 中文 (medium passages) | 10 passages, 30 Qs | `data/papers/dokkai/` |
| Dokkai M6 | 情報検索 (information retrieval) | 6 items, 12 Qs | `data/papers/dokkai/` |

### F.2 Notation rules

- Kanji words being tested are surrounded by `<u>...</u>` (HTML underline). Renders as actual underline in browsers and faithful markdown renderers, matching the underline used on the real JLPT paper.
- Hiragana words being tested in Mondai 2 are surrounded by `__...__` (markdown underscore-bold).
- The blank in Mondai 3 (goi) and Mondai 1 (bunpou) questions is shown as `（　　）`.
- In Bunpou Mondai 2, the four shuffled elements are listed as 1-4 and the original sentence shows positions A B C D where one is marked `★`. The answer identifies which option-number goes in the `★` slot.
- Bunpou Mondai 3 passages have multiple inline blanks numbered `[ 1 ]` `[ 2 ]` etc., each with its own 4-option set.
- Dokkai passages are shown in blockquotes (`>`) so they visually mirror the test paper.
- Each question has 4 numbered choices. `**Answer:**` shows the correct number.
- No em dashes (U+2014) appear in question content.

### F.3 Engine display

For mock-test mode, the app's test engine MUST hide the `**Answer:**` line and rationale until the student commits an answer. The visible-by-default format in source files is for self-study reference; runtime test rendering is the engine's responsibility.

### F.4 Numeral convention

Numbers are written using both kanji forms (一, 二, 三, 五, 十, 百, 千) and arabic numerals (1, 2, 100, 1000) — mirroring authentic JLPT papers, which use kanji numerals in narrative text and arabic numerals in prices, addresses, schedules, and time tables. This is intentional, not inconsistency.

### F.5 Kanji-scope exception for question files

The catalog rule (vocab + grammar fields use only N5-syllabus kanji) carries a deliberate exception for **questions**:

- All **stems** and all **correct answers** use only N5-syllabus kanji.
- **Distractor options** in 表記 (orthography) questions may contain non-N5 kanji because authentic JLPT distractors mimic visually-similar wrong forms — some of which are N4 or higher kanji that look like the N5 target. Forcing N5-only distractors would either require random hiragana (defeats the orthography test) or unrelated N5 kanji (no longer plausible distractors).
- This exception is scoped strictly to question files. The catalog rule applied to vocab + grammar fields is unchanged. Enforced by JA-1 (stems + correct answers) and JA-40 (distractor exemption).

### F.6 Dokkai naturalness exception

Authentic JLPT N5 reading passages routinely use a small number of common non-N5 kanji where forcing kana would harm readability. The full exception list is machine-tracked in `data/dokkai_kanji_exception.json` and currently covers 30 kanji: 京, 作, 使, 図, 院, 回, 教, 楽, 病, 終, 自, 阪, 館, 黒, 犬, 妹, 家, 弁, 当, 思, 朝, 近, 紙, 青, 同, 向, 央, 付, 売, 辛. Enforced by JA-28.

### F.7 Question-stem kanji policy

Question stems may reuse any non-N5 kanji that already appears in the passage they reference, so the question phrasing stays parallel to the source text (e.g., a passage that uses 妹 may have a stem `この 人の 妹は 何を べんきょうしますか。`). Standalone non-N5 kanji that are NOT present in the corresponding passage are forbidden in stems and must be written in kana.

### F.8 Distractor-form convention (orthography questions)

In Mondai 2 (orthography) and Mondai 1 (kanji-reading), distractors fall into three acceptable types:

1. **Visually-similar N5 kanji** with a different reading (e.g., 多い / 古い / 長い for a 高い target). Most common distractor type at N5; tests whether the learner recognizes the right glyph among lookalikes drawn entirely from the N5 syllabus.
2. **Non-N5 kanji with the same on-yomi** as the target (e.g., a 立ちます distractor of `経ちます` — N3+ kanji, real verb meaning "elapse"). Tests glyph recognition; the non-N5 kanji is acceptable because the question is purely orthographic.
3. **Invented (non-real) verb forms** that combine an N5 kanji with a wrong conjugation pattern (e.g., a 入ります distractor of `出ります` — the real form is 出ます). Tests glyph recognition without requiring the distractor to be a grammatically valid conjugation.

All three types are acceptable because the question asks "which kanji visually belongs in this word", not "is this conjugation pattern grammatical".

### F.9 Paper segmentation policy (Bunpou)

`data/papers/bunpou/paper-N.json` files segment the 100-question bunpou corpus into 7 papers using a **Q-order slice rule**: paper-1 covers Q1-Q15, paper-2 covers Q16-Q30, …, paper-7 covers Q91-Q100. The mapping is recorded in each paper-JSON's `source_question_range` field and in `data/papers/manifest.json`.

Q-order slices were chosen over JLPT-format mixed-Mondai segmentation because:
- Mondai 2 (Q61-90, sentence rearrangement) has a fixed choice-encoding that cannot be permuted without breaking the question; mixed-Mondai segmentation conflicts with per-paper position-balance.
- The autonomous-improvement Round 4 rebalance (v1.12.27) achieved 25/25/25/25 corpus-wide for bunpou by re-permuting only the unconstrained Mondai 1 + Mondai 3 items.

Accepted-with-rationale cost: a learner practicing paper-5 in isolation will see C-position 1 time out of 15. Across the corpus the distribution is exactly uniform, so multi-paper practice is unbiased. Future enhancement: an "exam-realism" test mode that virtually constructs a 15- or 17-item mixed-Mondai paper at runtime (ISSUE-006).

### F.10 Goi paraphrase-tightening pass (2026-05-04 history)

Five paraphrase items in Papers 5-7 originally relied on real-world inference rather than strict semantic equivalence:

```
Q70   好き              →  よく する
Q76   X より Y すき      →  Y を よく 飲む
Q86   電話を かける      →  電話で 話した
Q97   じょうず           →  よく 話せる    (also dropped N4 potential 話せます)
Q100  ならって いる      →  れんしゅう
```

Each stem was tightened in v1.12.13 by adding explicit context that makes the keyed answer a direct paraphrase rather than an inference. The rationales no longer carry "by elimination" or "closest among the four" hedges — these are now true paraphrases.

### F.11 Borderline N5 / late-N5 stretch items in Goi

Six items in the goi corpus rely on grammar canonically tested at N4 rather than N5: Q47 (〜たことがあります), Q48 (〜つもりです), Q62 (〜あいだに), Q64 (potential ひけます), Q91 (〜て、N に なります), Q97 (potential 話せます). Each is included because the structure is encountered at the strict N5/N4 boundary and the keyed answer remains correct under the construction. Per the project's `late_n5` tier convention these items are positioned as **stretch content** for learners on the cusp of N4.

---

## Part G — Mapping to live data

The structured live source-of-truth for content + scope is:

| Surface | File | Purpose |
|---|---|---|
| N5 grammar patterns (178) | `data/grammar.json` | Full pattern bodies + examples + tier + category |
| N5 vocab entries (1009) | `data/vocab.json` | Full entries + pitch_accent + collocations + frequent_patterns |
| N5 kanji (106) | `data/kanji.json` | Full entries + mnemonics + lookalikes + etymology + reading_notes |
| Kanji scope whitelist | `data/n5_kanji_whitelist.json` | The 106 N5 kanji — canonical for CI scope enforcement |
| Kanji readings table | `data/n5_kanji_readings.json` | Hand-tuned on/kun per kanji + primary-reading flag |
| Vocab scope whitelist | `data/n5_vocab_whitelist.json` | Vocab tokens for CI scope enforcement |
| Dokkai non-N5 exceptions | `data/dokkai_kanji_exception.json` | 30 kanji allowed in dokkai passages |
| Reading passages (54) | `data/reading.json` | Full passages + questions + comprehension targets |
| Listening items (50) | `data/listening.json` | Full scripts + choices + audio metadata |
| Moji paper questions (100) | `data/papers/moji/paper-*.json` | 7 papers × ~15 questions each |
| Goi paper questions (100) | `data/papers/goi/paper-*.json` | 7 papers × ~15 questions each |
| Bunpou paper questions (100) | `data/papers/bunpou/paper-*.json` | 7 papers × ~15 questions each |
| Dokkai paper questions (102) | `data/papers/dokkai/paper-*.json` | 7 papers × ~15 questions each |
| Question bank (290) | `data/questions.json` | Standalone grammar-pattern questions |

CI invariants in `tools/check_content_integrity.py` (83 active as of 2026-05-14) enforce scope discipline, schema integrity, and cross-surface consistency.

---

## Document history

- 2026-05-14: Initial consolidation from `KnowledgeBank/*.md` directory (deleted in same commit). All unique methodology + source citations + authoring conventions migrated here. Membership scope content remains in `data/*.json`. Question content remains in `data/papers/*/*.json`.
- Prior: KB directory was the original scope reference; never updated past initial monorepo commit. Discovered as out-of-sync with live data during run-4 accuracy audit cycle (2026-05-13). Merged into this single source of truth in the same cycle.
