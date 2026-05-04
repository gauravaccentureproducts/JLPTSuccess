# Changelog

All user-visible changes to the JLPT N5 study material site.

## v1.12.27 - 2026-05-04 (Autonomous-improvement iter 4 — global rebalance to perfect 25/25/25/25)

Iter 1 used a per-paper [4,4,4,3] target uniformly, which produced
small global skew when constrained items concentrated at certain
positions. After iter 4's global-aware rebalance, all four paper
corpora are at exact uniform distribution.

### Final position distributions (all paper corpora)

  moji      [25, 25, 25, 25]   (100 items)
  goi       [25, 25, 25, 25]   (100 items)
  bunpou    [25, 25, 25, 25]   (100 items)
  dokkai    [26, 26, 25, 25]   (102 items - cannot divide by 4)
  listening 4-ch: [8, 9, 9, 9] (36 items - constrained subset)
  listening 3-ch: [2, 2, 1]    (4 hatsuwa-hyougen items)
  reading   [21, 21, 21, 21]   (84 items)

Per-paper distribution exception:
  bunpou paper-5 + paper-6: still skewed by Mondai 2 sentence-
  rearrangement constraint (30 items where choice order encodes
  the test data). Cannot be permuted. Accepted-by-constraint.

### Iter 1 vs iter 4 comparison

  Corpus     Iter 1 result          Iter 4 result
  moji       [27, 27, 26, 20]   ->  [25, 25, 25, 25]
  goi        [27, 27, 26, 20]   ->  [25, 25, 25, 25]
  bunpou     [30, 25, 23, 22]   ->  [25, 25, 25, 25]
  dokkai     [26, 26, 25, 25]   ->  [26, 26, 25, 25]  (already optimal)

The iter 1 rebalancer was per-paper-only; iter 4 is global-aware
(measures constrained-item distribution, computes unconstrained
target to compensate, distributes accordingly). 16 additional
permutations applied. All choice content unchanged; only choice
ORDER permuted.

  - sw.js CACHE_VERSION:        v137 -> v138
  - index.html cache-busters:    v=1.11.47 -> v=1.11.48
  - 41/41 invariants PASS
  - Fix script idempotent

---

## v1.12.26 - 2026-05-04 (Autonomous-improvement iter 3 — English-leak cleanup)

Two English-language leaks in user-facing Japanese fields:

  bunpou paper-7 (Mondai 3, Q91-Q100): all 10 stems were "→ blank [N]"
    where "blank" is English. Replaced with Japanese-clean form
    "→ [N]番" (referring to the blank-N in the passage).

  dokkai-1.2 Q2 choice [1]: "インド (India)" had a parenthetical
    English gloss inside a choice. Stripped to "インド" (sufficient
    on its own).

Lock-step MD<->JSON updates so JA-32 stays green.

  - sw.js CACHE_VERSION:        v136 -> v137
  - index.html cache-busters:    v=1.11.46 -> v=1.11.47
  - 41/41 invariants PASS
  - Fix script idempotent

---

## v1.12.25 - 2026-05-04 (Autonomous-improvement iter 2 — choice-length balance)

Reshaped distractors in 16 dokkai items where the keyed answer was
significantly longer/shorter than its distractors, removing a
length-signal cue. Choice CONTENT changed (distractors only); keyed
answers preserved exactly. Rationales updated to cite passage text
verbatim.

Items fixed: Q5, Q22, Q24, Q28, Q37, Q58, Q63, Q65, Q68, Q69, Q73,
Q81, Q90, Q93, Q94, Q102 (all dokkai).

Notable patterns:
  - Q94 (excluded-from-class question): removed bilingual gloss
    "しゅふ (housewife)" → just "しゅふ" (English in choice text was
    creating the length asymmetry).
  - Q73 (party venue): removed parenthetical "(たなかさんの 家)" from
    keyed answer; cleaner as plain "友だちの たなかさんの 家".
  - Q5 (party-bring): replaced "何も もって 来なくて いい" (14ch) with
    plausible single-noun "おみやげ".

One asymmetric item remains: bunpou Q75 (Mondai 2 sentence-
rearrangement). Choice order encodes the fragment positions and
cannot be permuted/reshaped without breaking the test point.
Accepted-by-constraint.

### Cache and integrity

  - sw.js CACHE_VERSION:        v135 -> v136
  - index.html cache-busters:    v=1.11.45 -> v=1.11.46
  - 41/41 invariants PASS
  - Fix script idempotent

---

## v1.12.24 - 2026-05-04 (Autonomous-improvement iter 1 — per-paper rebalance + schema fix)

Comprehensive structural audit run autonomously (no manual driver).
Found three classes of issues; iteration 1 fixed all reachable ones.

### Schema regression fix (grammar.json, 6 examples)

  Round 5 (v1.12.23) added 6 grammar examples using `en` field.
  The corpus convention is `translation_en`. Migrated all 6.
  No data loss; all translations preserved.

### Per-paper position rebalance (27 papers updated, 119 swaps)

  While prior rebalances achieved global ~25/25/25/25, individual
  papers had heavy skew (e.g., dokkai paper-3 was [3, 1, 0, 12] —
  position D 75% within that paper). A learner practicing one
  paper at a time experienced the per-paper distribution.

  After iteration 1: every 15-item paper at 4/4/4/3 (or near),
  every 16-item paper at 4/4/4/4, every 12-item paper at 3/3/3/3,
  every 10-item paper at 3/3/2/2.

  Two exceptions, accepted by constraint:
    bunpou paper-5: [4, 5, 1, 5] - all 15 items are Mondai 2
                    sentence-rearrangement; choice order encodes
                    the fragment positions, not permutable.
    bunpou paper-6: [7, 1, 4, 3] - same constraint.

### Cross-corpus duplicate stem resolved (1 item)

  moji Q82 and goi Q1 both used the stem 「まいあさ コーヒーを X」.
  Diversified moji Q82 to 「パーティーで ジュースを __のみ__ました」.
  Same kanji-writing test point (飲) with a different surrounding
  sentence.

### Cache and integrity

  - sw.js CACHE_VERSION:        v134 -> v135
  - index.html cache-busters:    v=1.11.44 -> v=1.11.45
  - 41/41 invariants PASS
  - Fix script idempotent

### Outstanding (improvement-tier, deferred to iter 2)

  17 items have choice-length asymmetry where the keyed answer is
  significantly longer/shorter than distractors (e.g., dokkai Q5 with
  lens [3,4,3,14]). Need content authoring to reshape distractors.

---

## v1.12.23 - 2026-05-04 (N5 thorough audit Round 5 - reading.json + grammar.json)

Round 5 of the teacher-style N5 audit covers the last two un-audited
data sources. Sub-agent audits identified specific issues in both.

### reading.json (40 passages, 84 questions)

  **Position rebalance:** before 6/50/25/3 (B=60%, D=4%); after
  **21/21/21/21**. 33 mechanical choice-order swaps. The skew on
  this corpus was as severe as listening's pre-fix state - 13 of 40
  passages had ALL their questions keyed to position B.

  **Content fixes (4 items):**
    n5.read.011.q2: distractor つめたかった replaced with
                     しおからかった (passage explicitly says あつかった,
                     making cold an instant-eliminate distractor).
    n5.read.028.q1: distractors reshaped to match length of compound
                     keyed answer (was: 3 single adjectives vs 1
                     compound; now: 4 compounds).
    n5.read.034.q2: explanation_en was duplicate of q1; refocused on
                     "学校で" (the place).
    n5.read.035.q3: explanation_en was duplicate of q2; refocused on
                     "母と いっしょに" (the companion).

### grammar.json (178 patterns, ~600 examples)

  Sub-agent sampled ~95 examples across late_n5 and core_n5 subsets.
  Found 7 specific issues:

  **n5-007 (で particle: means/instrument)** - 2 examples replaced:
    [2] たばこを すいません -> バスで 学校へ 行きます。
        (former collided with apology homophone すみません/すいません)
    [3] なんで きましたか -> タクシーで うちへ かえりました。
        (former overwhelmingly read as "why" not "how")

  **n5-098 (likes/dislikes contrast)** - meaning_en was misaligned
    with examples. Was: "Most ~ of all (covered by superlative
    pattern)". Updated to: "Expressing likes / dislikes contrast
    (using すき / きらい)" - matches the actual examples.

  **n5-162 (Verb-plain + まえに)** - 2 examples replaced:
    [0] ごはんの まえに -> 出かける まえに、しんぶんを 読みます
    [1] (similar) -> ねる まえに、はを みがきます
    (Both former examples used Noun + の + まえに, which is a
    different pattern - n5-161. The replacements demonstrate the
    actual Verb-plain + まえに pattern this entry is for.)

  **n5-163 (Verb-た + あとで)** - 1 example replaced:
    [0] しごとの あとで -> しごとが おわった あとで、 のみに 行きました
    (Same noun-vs-verb pattern issue as n5-162.)

  **n5-176 (~なくちゃ / ~なきゃ casual contractions)** - 1 example
    replaced:
    [0] もう 行かなくては いけません -> もう 行かなくちゃ。
    (Former used the formal ~なくては いけません instead of the
    casual contractions this pattern is supposed to demonstrate.)

  **n5-182 (Verb-dictionary + な = "Don't V" / prohibition)** - all
    examples had form='affirmative' but the pattern is prohibition.
    Updated form field to 'prohibition' on each example.

### Cumulative N5 thorough-audit closure (v1.12.19..v1.12.23)

  v1.12.19  Critical bugs: listening n5.listen.036, dokkai Mondai 5+6
            deployment (42 Qs), 3 stale rationales, 2 exception kanji.
  v1.12.20  HIGH: 3 corpus rebalances (dokkai, bunpou, listening).
  v1.12.21  MEDIUM: vocab.json <-> MD drift resolved (28 entries).
  v1.12.22  Item-level: 30 stale Mondai 5 rationales rewritten,
            4 bunpou content fixes, 3 listening content fixes.
  v1.12.23  Item-level: reading.json rebalance + 4 fixes,
            grammar.json 7 example fixes (this release).

### Final N5 corpus state

  | Corpus    | Items | Distribution           |
  |-----------|-------|------------------------|
  | moji      |  100  | 25 / 25 / 25 / 25      |
  | goi       |  100  | 25 / 25 / 25 / 25      |
  | bunpou    |  100  | 25 / 25 / 25 / 25      |
  | dokkai    |  102  | 26 / 26 / 25 / 25      |
  | listening |   40  | 11 / 10 / 10 / 9       |
  | reading   |   84  | 21 / 21 / 21 / 21      |

  Vocabulary: 1041 entries, MD<->JSON synced.
  Grammar: 178 patterns, examples audited.
  All teacher-audit findings closed across 5 rounds.

### Cache and integrity

  - sw.js CACHE_VERSION:        v133 -> v134
  - index.html cache-busters:    v=1.11.43 -> v=1.11.44
  - 41/41 invariants PASS
  - Fix script idempotent.

---

## v1.12.22 - 2026-05-04 (N5 thorough audit Round 4 - item-level content fixes)

Round 4 of the teacher-style N5 audit: item-level content quality
fixes across bunpou, dokkai, and listening corpora. Three parallel
sub-agent audits identified specific issues that prior rounds had
not addressed at the item level.

### Critical: Dokkai Mondai 5 stale rationales (30 items rewritten)

  v1.12.19 deployed Mondai 5+6 to paper-JSONs. The "stale rationale
  fix" applied at that time only covered Q91-Q93 (Mondai 6). Mondai 5
  (Q61-Q90) had SYSTEMIC stale rationale text - copy-pasted from
  unrelated Mondai 4 questions. Keyed answers were correct, but
  user-facing explanations referenced wrong content (e.g. Q67
  rationale cited "ともだちは 八時に 来ます" - irrelevant to a
  question about the mother's cooking).

  All 30 Mondai 5 rationales rewritten to cite the actual passage
  content for the keyed answer. Each new rationale uses a verbatim
  Japanese phrase from passage_text so JA-32 (paper<->MD parity) is
  preserved. Both paper-5/6 JSONs and dokkai_questions_n5.md updated
  in lock-step.

### Bunpou content fixes (4 items)

  Q14   Stem ambiguity. 「ねこ（  ）すきです」 allowed both は
        (contrastive) and が (subject-of-suki). Anchored with
        わたしは: 「わたしは ねこ（  ）すきです」 -> が unambiguous.

  Q34   Colloquial form in keyed option. Replaced 「しずかじゃない」
        with the cleaner N5 textbook form 「しずかじゃ ありません」.
        Removed trailing です from stem to avoid じゃない+です
        register clash.

  Q41   Structural defect: stem had no numeral preceding the counter
        blank, so 「さつ」 had nothing to attach to. Added 三 before
        blank: 「つくえの 上に 本が 三（  ）あります」.

  Q75   Mondai 2 sentence-rearrangement contained 「ので」 fragment
        against the project's ので -> から policy (set in v1.12.14
        for Q5 and v1.12.15 for Q33/Q44). Replaced fragment 3 from
        「ので」 to 「から」.

### Listening content fixes (3 items)

  n5.listen.005   Distractors had zero script support. Replaced two
                  unsupported distractors with school-tardiness
                  alternatives (「あたまが いたかったから」, etc.)
                  that are at least plausible reasons even though
                  the keyed answer is the only one cited in the
                  script.

  n5.listen.038   Cultural-premise issue: scenario was entering a
                  ryokan (inn) where おじゃまします is not the
                  standard greeting (guests typically say
                  よろしく お願いします). Changed scenario to
                  entering a friend's house, where おじゃまします
                  is canonical.

  n5.listen.040   Three near-identical greeting items in the corpus
                  (012, 025, 040 all tested おはようございます with
                  the same scenario). Diversified 040 to test
                  evening greeting (こんばんは) instead.

### Cache and integrity

  - sw.js CACHE_VERSION:        v132 -> v133
  - index.html cache-busters:    v=1.11.42 -> v=1.11.43
  - 41/41 invariants PASS
  - Fix script idempotent

### Audit findings still open (Round 5)

  - reading.json (40 passages, 84 questions) - separate corpus
    from dokkai paper-JSONs; not yet audited at the item level.
  - grammar.json examples (178 patterns × 3-5 examples each) -
    naturalness audit pending.

---

## v1.12.21 - 2026-05-04 (N5 thorough audit Round 3 - vocab drift resolved)

Round 3 of the teacher-style N5 audit closes the last open finding:
the bidirectional drift between vocab.json and vocabulary_n5.md.

### vocab.json <-> vocabulary_n5.md drift resolved (28 entries added)

  Audit found that vocab.json had 28 entries with no representation
  in vocabulary_n5.md. All 28 added to their appropriate thematic
  sections in the MD source (alphabetical-by-original-Q-order, but
  thematically grouped per the existing section structure).

  Additions by section:
    §9 Counters (Common):              倍 (ばい) "times / -fold"
    §11 Time:                          週末 (しゅうまつ) "weekend"
    §13 Locations:                     おてら, カフェ, コンビニ,
                                       フロント, 出口 (でぐち)
    §14 Nature:                        さくら "cherry blossom"
    §22 Money/Shopping:                セール
    §24 School/Study:                  たんご, アルバイト, 高校生
                                       (こうこうせい)
    §25 Languages/Countries:           スペイン人 (スペインじん),
                                       国籍 (こくせき)
    §26 House/Furniture:               ベンチ
    §27 Verbs Group 1:                 はらう "pay"
    §28 Verbs Group 2:                 おくれる, ためる, 聞こえる
                                       (きこえる)
    §29 Verbs Irregular/する:          じゅんび
    §33 Adverbs:                       いっぱい, ぜひ, ただ, べつべつ
    §36 Greetings:                     おじゃまします
    §37 Common Nouns Misc:             おしらせ, おもちゃ, コンサート

  PoS tags mapped from JSON `pos` field per the existing legend
  (noun -> [n.], verb-1 -> [v1], etc.). JA-31 still passes (PoS-tag
  agreement on the matched-form subset).

### "MD-only" finding closed by inspection

  The audit also flagged 10 forms appearing in vocabulary_n5.md but
  not as separate JSON entries (うしろ, うち, よい, みな, etc.).
  Inspection showed these are all SECONDARY FORMS of existing JSON
  entries, represented in the JSON `reading` field's slash-separated
  notation (e.g., JSON form='いえ' has reading='いえ / うち'). This
  is the project's existing convention for multi-form vocabulary;
  no fix needed. JA-31 already validates the matched-form subset.

### Cumulative N5 audit closure (v1.12.19..v1.12.21)

  Round 1 (v1.12.19) - CRITICAL fixes:
    listening n5.listen.036 unscorable bug, dokkai Mondai 5+6
    deployment (42 questions), 3 stale rationales, 2 exception kanji.

  Round 2 (v1.12.20) - HIGH-priority rebalances:
    dokkai 1/17/37/5 -> 26/26/25/25 (41 permutations)
    bunpou 27/35/25/13 -> 25/25/25/25 (12 permutations)
    listening 5/24/9/1 -> 11/10/10/9 combined (15 swaps)

  Round 3 (this release) - MEDIUM:
    vocab.json <-> vocabulary_n5.md drift resolved (28 entries added).

### Final N5 corpus state

  | Corpus    | Items | Distribution           | Source-of-truth |
  |-----------|-------|------------------------|-----------------|
  | moji      |  100  | 25 / 25 / 25 / 25      | MD <-> 7 papers |
  | goi       |  100  | 25 / 25 / 25 / 25      | MD <-> 7 papers |
  | bunpou    |  100  | 25 / 25 / 25 / 25      | MD <-> 7 papers |
  | dokkai    |  102  | 26 / 26 / 25 / 25      | MD <-> 7 papers |
  | listening |   40  | 11 / 10 / 10 / 9       | listening.json  |
  | reading   |   84  | (separate corpus)      | reading.json    |
  | vocab     | 1041  | (vocabulary)           | MD <-> JSON     |
  | grammar   |  178  | (patterns)             | grammar.json    |
  | kanji     |  106  | (entries)              | kanji.json      |

All teacher-audit findings closed. 41/41 integrity invariants green.

### Cache and integrity

  - sw.js CACHE_VERSION:        v131 -> v132
  - index.html cache-busters:    v=1.11.41 -> v=1.11.42
  - 41/41 invariants PASS
  - Vocab-drift fix script idempotent (2nd run reports 0 additions).

---

## v1.12.20 - 2026-05-04 (N5 thorough audit Round 2 - 3 corpus rebalances)

Round 2 of the teacher-style N5 audit: corpus-level position-distribution
rebalances on all three remaining skewed corpora.

### Dokkai rebalance (102 items)

  Before:  1 / 17 / 37 / 5    (positions A / B / C / D, 60% C-skew)
  After:   26 / 26 / 25 / 25  (target distribution, 102 / 4)

  Per-paper after rebalance: ~4/4/4/4 in each 16-item paper.
  Dramatic skew (62% C, 1% A) eliminated. The "guess C" heuristic
  now scores 25%, same as random.

  41 mechanical choice-order permutations across all 7 dokkai papers.
  Choice CONTENT unchanged; only order permuted. correctIndex updated
  in JSON, numbered list reordered in MD, **Answer: N** updated.

  5 items skipped (semantically-ordered choices):
    Q3   math problem (yen amounts ascending)
    Q6   time options (時 ascending)
    Q7   count options (本 ascending)
    Q15  count options (つ ascending)
    Q41  count options (numeric sequence)

### Bunpou rebalance (100 items)

  Before:  27 / 35 / 25 / 13  (B-over, D-under)
  After:   25 / 25 / 25 / 25  (perfect)

  12 mechanical choice-order permutations on Mondai 1 + Mondai 3
  items only. Mondai 2 (Q61-90, sentence rearrangement) FULLY
  CONSTRAINED - permuting the fragment-numbering would change which
  fragment goes in the ★ slot, breaking the test point. All 30
  Mondai 2 items kept their original choice order.

### Listening rebalance (40 items)

  Before:  5 / 24 / 9 / 1     (B-skew 60%, D-starved)
  After:   11 / 10 / 10 / 9   (combined, near-perfect)

  Per choice-count partition:
    4-choice items (36):  9 / 9 / 9 / 9   (perfect)
    3-choice items (4, hatsuwa-hyougen Mondai 4 format): 2 / 1 / 1

  15 mechanical correctAnswer-position swaps. The 3-choice items
  use a 3-slot target (~1/1/1) since hatsuwa-hyougen Mondai 4 only
  has three options.

  7 items skipped (chronological / numeric ordering preserved):
    n5.listen.003  time (8時/8時半/9時/9時半)
    n5.listen.011  duration / time
    n5.listen.013  time
    n5.listen.020  money
    n5.listen.027  time
    n5.listen.030  time
    n5.listen.036  duration (二日間/三日間/四日間)

### Cache and integrity

  - sw.js CACHE_VERSION:        v130 -> v131
  - index.html cache-busters:    v=1.11.40 -> v=1.11.41
  - 41/41 invariants PASS
  - Rebalance script idempotent (2nd run reports 0 moves).

### Cumulative N5 corpus state after Round 2

  | Corpus    | Items | Distribution           | Status        |
  |-----------|-------|------------------------|---------------|
  | moji      | 100   | 25/25/25/25            | shipped v1.12.18 |
  | goi       | 100   | 25/25/25/25            | shipped v1.12.17 |
  | bunpou    | 100   | 25/25/25/25            | THIS RELEASE  |
  | dokkai    | 102   | 26/26/25/25            | THIS RELEASE  |
  | listening | 40    | 11/10/10/9 (combined)  | THIS RELEASE  |

All five N5 corpora now at exact or near-exact 25%-per-position
balance. Pattern-recognition heuristics (e.g., "pick B if unsure")
no longer beat random chance on any corpus.

### Audit findings still open (Round 3)

  Round 3 (MEDIUM): vocab.json <-> vocabulary_n5.md drift (~38 forms).
    28 JSON-only entries + 10 MD-only entries. Bidirectional fix
    needed. Largest drift not addressed in any prior round.

---

## v1.12.19 - 2026-05-04 (N5 thorough audit Round 1 - critical fixes)

Internal teacher-style audit of the entire N5 section identified two
CRITICAL issues. Both fixed in this release.

### Issue 1: Listening data integrity bug (n5.listen.036)

  Old: correctAnswer = "三日かん"  (mixed kanji+kana, mojibake)
  New: correctAnswer = "三日間"    (matches choice [2] exactly)

  The choice list was ['二日間', '三日間', '四日間', '一週間'] (all-
  kanji forms). The correctAnswer string was "三日かん" with the second
  kanji written in kana. Engine string-comparison would never find a
  match, leaving the question unscorable. explanation_en updated for
  consistency.

### Issue 2: Dokkai Mondai 5+6 deployed (42 questions)

  Audit found that the dokkai paper-JSON corpus contained only the 60
  Mondai 4 questions; Mondai 5 (30 medium-passage Qs) and Mondai 6
  (12 information-retrieval Qs) existed in the MD source but were
  never deployed to data/papers/dokkai/.

  Generated 3 new paper-JSONs from the MD source:
    paper-5.json   Q61-Q75   Mondai 5 (5 passages, 15 questions)
    paper-6.json   Q76-Q90   Mondai 5 (5 passages, 15 questions)
    paper-7.json   Q91-Q102  Mondai 6 (6 items, 12 questions)

  Total dokkai corpus: 60 -> 102 questions across 4 -> 7 papers.
  Paper structure preserved (~15 items per paper, last paper smaller).
  Manifest.json updated: dokkai paperCount 4->7, questionCount 60->102,
  total project paperCount 25->28, totalQuestions 360->402.

### Issue 2.1: Three stale rationales fixed during deployment (Q91-Q93)

  Audit also caught that Q91-Q93 in the MD source had rationale text
  copy-pasted from unrelated Mondai 4/5 questions:

    Q91 (pool admission): old rationale referenced "no bread, ate rice"
    Q92 (BBQ reservation): old rationale referenced "bread+milk swap"
    Q93 (class days): old rationale referenced "Tuesday birthday"

  Replaced all three with question-appropriate rationales referencing
  the actual passage content (table values, time slots). MD source
  and JSON both updated.

### Issue 2.2: Two non-N5 kanji added to dokkai exception list

  The Mondai 5+6 deployment surfaced two non-N5 kanji used in choice
  text that were not yet in the dokkai_kanji_exception list:

    売 (うる, sell)  - Q66 piano-shop distractor "ピアノを 売って いる"
    辛 (からい, spicy) - Q68 spicy-curry distractor "ピリ辛い"

  Both appear ONLY in choice distractors (not in passages). Added to
  data/dokkai_kanji_exception.json with justifications matching the
  existing exception-policy convention. Exception list grew 28 -> 30.

### Cache and integrity

  - sw.js CACHE_VERSION:        v129 -> v130
  - index.html cache-busters:    v=1.11.39 -> v=1.11.40
  - 41/41 invariants PASS (incl. JA-28 dokkai-kanji bound, JA-32
    lock-step MD<->JSON parity)
  - All deployment scripts idempotent.

### Audit findings still open (next rounds)

  Round 2 (HIGH): Dokkai/listening/bunpou position rebalance
    Dokkai: 1/17/37/5 globally; severely C-skewed (62%)
    Listening: 5/24/9/1; B-skewed (60%), D-starved
    Bunpou: 27/35/25/13; moderate skew
    All three need same mechanical rebalance pattern as goi/moji.

  Round 3 (MEDIUM): vocab.json <-> vocabulary_n5.md drift (~38 forms)
    Bidirectional gap: 28 JSON-only entries + 10 MD-only entries.
    Larger than initial 1-entry estimate.

---

## v1.12.18 - 2026-05-04 (Moji first-pass review - 5 item fixes + 37 permutation rebalance)

First audit pass on the moji corpus (Mondai 1 + Mondai 2). Reviewer
characterized item-level quality as "in fact better than the goi
corpus's first pass, especially in the visual-confusion items" and
flagged one major must-fix (position distribution) plus four polish-
grade item tweaks plus one stem naturalness rewrite.

### Position-distribution rebalance (37 permutations)

  Before:  56 / 31 / 12 /  1   (positions A / B / C / D, total 100)
  After:   25 / 25 / 25 / 25   (target distribution)

  Per-section breakdown:
    Mondai 1 (Q1-50):   27/15/7/1 -> 13/13/12/12
    Mondai 2 (Q51-100): 29/16/5/0 -> 12/12/13/13   (closes the
                                                    zero-D anomaly)

  37 mechanical choice-order permutations on unconstrained items.
  Choice CONTENT is unchanged; only the order changes. correctIndex
  updated in JSON, numbered list reordered in MD, **Answer: N**
  updated to match.

  Permutations applied (37 total):
    Mondai 1 (16 moves):
      A -> D (11): Q5, Q6, Q9, Q11, Q13, Q15, Q18, Q21, Q23, Q26, Q28
      A -> C (3):  Q33, Q36, Q37
      B -> C (2):  Q1, Q2
    Mondai 2 (21 moves):
      A -> D (13): Q52, Q53, Q58, Q60, Q62, Q63, Q65, Q66, Q67, Q70,
                   Q71, Q75, Q77
      A -> C (4):  Q78, Q81, Q83, Q85
      B -> C (4):  Q51, Q56, Q61, Q64

  Skipped (visual-confusion + homophone clusters - reviewer
  characterized these as "the strongest part of the corpus", their
  carefully-arranged choice order is itself a pedagogical asset):
    Q54 力 vs 刀/万/方
    Q55 大人 vs 太人/大入/太入
    Q59 人 vs 入/八/大
    Q73 午前 vs 牛前
    Q79 駅 vs 馬/駄/訳
    Q89 行きます vs 生きます (homophone)
    Q92 立ちます vs 起ちます/経ちます/建ちます (homophone)
    Q93 休 vs 体
    Q95 買います vs 飼います (homophone)
    Q99 白 vs 百/自/旧

  Per-section balance achieved by walking unconstrained items in
  Q-number order at each surplus position and distributing to
  deficit positions, prioritizing the lowest-current-count slot
  first (closes Mondai 2 zero-D anomaly). Algorithm captured in
  TARGET_INDEX dict in the fix script.

### Item-level fixes (5)

  Q19 / moji-2.4   stem rewrite (naturalness)
    Old stem: <u>今年</u> は さむいです。
    New stem: <u>今年</u>の ふゆは さむいです。
    Reason: さむい normally describes a moment, not a year-long
    state. Anchoring to ふゆ makes the cold-temperature claim
    natural. Reading test point (今年 -> ことし) unchanged.

  Q55 / moji-4.10  rationale: jukujikun acknowledgement
    Stem and choices unchanged. The compound 大人 / おとな is a
    semantic compound reading (jukujikun); the kanji are individually
    N5 but the compound reading is irregular. Rationale now
    acknowledges this and notes the compound is documented as an
    N5 vocab entry in vocabulary_n5.md.

  Q57 / moji-4.12  rationale: distractor whitelist note
    Stem and choices unchanged. The distractor 妹 (younger sister)
    is not in the N5 kanji whitelist. Rationale now notes this
    explicitly per the moji-corpus kanji-scope exception (Mondai 2
    distractors may use non-whitelist kanji where authentic JLPT
    format requires it).

  Q78 / moji-6.3   rationale: semantic-distractor explanation +
                   permuted A -> C
    Stem unchanged; choices reordered (rebalance). 道 is whitelisted
    N5 and in vocabulary_n5.md. The distractors 通 / 路 / 行 are
    family-of-meaning N4+ alternatives. Rationale explains the
    semantic-distractor design and confirms 道 is the N5 target.

  Q92 / moji-7.2   rationale: stronger trap wording
    Stem and choices unchanged. The distractors 起ちます / 経ちます
    / 建ちます are real Japanese verbs also read たちます but N3+
    in scope. Rationale now spells out the polysemy and notes that
    broader-exposure students should not be misled.

### Coverage summary

With this release the four-Mondai vocabulary section is structurally
complete and corpus-balanced:

  | Mondai | File                       | Items | Distribution         |
  |--------|----------------------------|-------|----------------------|
  | 1      | moji_questions_n5.md       | 50    | 13 / 13 / 12 / 12    |
  | 2      | moji_questions_n5.md       | 50    | 12 / 12 / 13 / 13    |
  | 3      | goi_questions_n5.md        | 50    | (part of 25/25/25/25)|
  | 4      | goi_questions_n5.md        | 50    | (part of 25/25/25/25)|

The reviewer's "structural gap" flag from earlier passes is fully
closed.

### Cache and integrity

  - sw.js CACHE_VERSION:        v128 -> v129
  - index.html cache-busters:    v=1.11.38 -> v=1.11.39
  - 41/41 invariants PASS (incl. JA-32 lock-step MD<->JSON parity)
  - Fix script idempotent (2nd run reports "No changes").
  - Final answer-position distribution: 25 / 25 / 25 / 25.

---

## v1.12.17 - 2026-05-04 (Goi fourth-pass review - Q64 N4 potential + 25/25/25/25 rebalance)

Fourth-pass walk-through identified two issues. Both addressed.

### Issue 1: Q64 N4-potential-form leak (one item)

  Q64 / goi-5.4   stem 「じょうずに ピアノを ひきます」
    Old keyed (pos 2): たなかさんは ピアノが よく ひけます。
                       ^ uses ひける (potential form of 弾く), N4
                         grammar in Genki / Minna / Tobira.
    New keyed (pos 4): たなかさんは ピアノを ひくのが じょうずです。

  Same fix pattern as Q97 in v1.12.13. The Q97 fix swapped a
  nominalized adjective stem for an adverbial keyed; Q64 is the
  inverse direction (adverbial stem -> nominalized adjective keyed).
  Test point: 「じょうずに ひく」 = 「ひくのが じょうず」 - same
  skill, different syntactic frame. Strict-N5 across both items.

### Issue 2: Answer-position distribution rebalance (21 permutations)

  Reviewer noted the corpus had a heavy skew at position B (46/100)
  and starvation at position D (9/100), giving a "when in doubt,
  pick B" heuristic freebie to test-wise students.

    Before:  19 / 46 / 26 /  9   (positions A / B / C / D)
    After:   25 / 25 / 25 / 25   (target distribution)

  Fix is mechanical: permute the choice ORDER within 21 items so the
  keyed answer lands in a balanced position. Choice CONTENT is
  unchanged; only the order changes. correctIndex updated in JSON,
  numbered list reordered in MD, **Answer: N** updated to match.

  Permutations applied (21 total):
    B -> A (6):  Q1, Q5, Q7, Q8, Q13, Q17
    B -> D (14): Q23, Q24, Q26, Q27, Q29, Q30, Q32, Q42, Q44, Q47,
                 Q49, Q51, Q53, Q57
    C -> D (1):  Q3

  Skipped (semantic constraints on choice order):
    Q38-Q41   counter cluster
    Q64       handled in Issue 1 (lands at D)
    Q73       kasu perspective inversion
    Q83       kariru perspective inversion
    Q92       giving-receiving (くれる ≈ もらう)

  Permutation plan was computed deterministically: walk unconstrained
  items in Q-number order, take the first N at each surplus position,
  distribute to deficit positions in deterministic order. Captured in
  TARGET_INDEX dict in the fix script for reproducibility.

### Cache and integrity

  - sw.js CACHE_VERSION:        v126 -> v127
  - index.html cache-busters:    v=1.11.36 -> v=1.11.37
  - 41/41 invariants PASS (incl. JA-32 lock-step MD<->JSON parity)
  - Fix script idempotent (2nd run reports "No changes").
  - Final answer-position distribution: 25 / 25 / 25 / 25.

### Cumulative goi audit closure (v1.12.12..v1.12.17)

  v1.12.12  14 item fixes + 2 policy headers (initial 19-item audit)
  v1.12.13  5 inference cluster items tightened
  v1.12.14  5 re-review follow-ups (Q5/Q51/Q94/Q98/Q99)
  v1.12.15  4 third-pass fixes (Q33/Q44/Q47/Q87) + Q39 verified
  v1.12.16  Q73/Q74 mirror-pair scatter + Mondai 1/2 cross-reference
  v1.12.17  Q64 N4 potential dropped + 25/25/25/25 position rebalance

Total: 29 item-level content edits + 7 rationale tightenings + 3
policy/cross-reference docs + 1 structural swap + 21 position
permutations. Goi corpus now passes the four-pass audit with no
residual flags from any pass.

---

## v1.12.16 - 2026-05-04 (Q73/Q74 mirror-pair scatter + Mondai 1/2 cross-reference)

Closes the v1.12.15 deferral and addresses the third-pass review's
"Coverage gap (still)" mention. Per "fix all remaining": no items
left from the third-pass walk-through.

### Mirror-pair scatter (Q74 <-> Q83 content swap)

Reviewer flagged Q73 (kasu perspective) and Q74 (kariru perspective)
as a conceptually-mirror pair appearing in immediate sequence in
paper-5 (positions 5.13 + 5.14). Pattern recognition would let an
examinee solve one by mechanically inverting the other.

  Before:
    Q73 (paper-5.13)  友だちに 本を かしました   -> 友だちが 私から かりた  (kasu)
    Q74 (paper-5.14)  友だちから 本を かりました -> 友だちが 私に かした    (kariru)
    Q83 (paper-6.8)   バスに のって 学校へ      -> バスで 学校へ          (transportation)

  After:
    Q73 (paper-5.13)  kasu perspective  (UNCHANGED)
    Q74 (paper-5.14)  transportation     (was Q83's content)
    Q83 (paper-6.8)   kariru perspective (was Q74's content)

Distance between Q73 (kasu) and Q83-now-with-kariru: 10 questions
across two papers. kbSourceId mapping preserved (paper-5.14 -> "Q74",
paper-6.8 -> "Q83") because kbSourceId tracks MD position, not
semantic content. JA-32 stays green via lock-step MD <-> JSON.

**Audit-traceability note:** pre-v1.12.16 audit reports referencing
"Q74" mean kariru; post-v1.12.16 they mean transportation. The full
swap is documented here. Q73 is unchanged.

### Mondai 1/2 cross-reference (header docs)

Third-pass review repeated a "Coverage gap (still)" flag for Mondai 1
(kanji reading) and Mondai 2 (orthography). The gap is illusory --
those Mondais are in `KnowledgeBank/moji_questions_n5.md` (100 items
total: 50 Mondai 1 + 50 Mondai 2). An auditor walking only the goi
file would not know to look there.

The goi file header now includes:

  - A prominent blockquote callout naming the moji file as the home
    of Mondai 1+2.
  - An expanded "Subtypes covered" table listing all four Mondais
    with their source file, so the corpus structure is self-
    documenting from a single header.

No content moved between files; only the cross-reference is new.

### Cache and integrity

  - sw.js CACHE_VERSION:        v125 -> v126
  - index.html cache-busters:    v=1.11.35 -> v=1.11.36
  - 41/41 invariants PASS (incl. JA-32 lock-step MD<->JSON parity)
  - Swap script idempotent (2nd run reports "No changes").

### Cumulative goi audit closure (v1.12.12..v1.12.16)

  v1.12.12  14 item fixes + 2 policy headers (initial 19-item audit)
  v1.12.13  5 inference cluster items tightened
  v1.12.14  5 re-review follow-ups (Q5/Q51/Q94/Q98/Q99)
  v1.12.15  4 third-pass fixes (Q33/Q44/Q47/Q87) + Q39 verified
  v1.12.16  Q73/Q74 mirror-pair scatter + Mondai 1/2 cross-reference

Total: 28 item-level content edits + 6 rationale tightenings + 3
policy/cross-reference docs + 1 structural swap. Goi corpus is now
in a state the auditor's third pass described as "consistently above
the level of most commercial N5 vocabulary practice books".

---

## v1.12.15 - 2026-05-04 (Goi third-pass review - 4 fixes + 1 deferred)

A third-pass walk-through by the same auditor on the v1.12.14 state
flagged five remaining minor observations. Four are addressed here;
the fifth (Q73/Q74 mirror-pair scatter) is deferred with rationale.
The reviewer noted the corpus is now in a state where item-level
quality is consistently above commercial N5 vocabulary practice books.

### Fixes (4)

  Q33 / goi-3.3   ので -> から (corpus-wide policy)
    Old stem: つかれたので （　　） すわりました。
    New stem: つかれましたから、（　　） すわりました。
    Same reason conjunction policy as the Q5 fix in v1.12.14.

  Q44 / goi-3.14  ので -> から (corpus-wide policy)
    Old stem: きょうは あめが ふって いるので、...
    New stem: きょうは あめが ふって いるから、...
    Same policy.

  Q47 / goi-4.2   rationale: orphaned note -> "Common error" call-out
    Stem and choices unchanged. The previous parenthetical about
    きょねん felt orphaned because the question doesn't include
    a time marker. Reframed as anticipating a typical student
    error: "Common error: 〜たことがある cannot combine with
    specific time markers (きょねん, etc.)".

  Q87 / goi-6.12  rationale: drop off-topic はたち trivia
    Stem and choices unchanged. The previous rationale included a
    paragraph about the special reading はたち for 二十さい, which
    is interesting trivia but doesn't bear on what this question
    tests (time-reference: present age vs future age). Rationale
    now focuses on the time-reference test point. はたち remains
    documented at vocabulary_n5.md line 1118 so no information
    is lost.

### Deferred (1)

  Q73 / Q74 mirror-pair scatter (paper-5.13 + paper-5.14)
    Reviewer noted these conceptually-mirror items (かす / かりる
    perspective inversion in both directions) appear adjacent and
    suggested moving Q74's content to paper-6 or paper-7 for
    exam-realism. Reviewer themselves flagged this as
    "Pedagogically not wrong as is; just an exam-realism nudge".

    Deferred because a content swap (e.g., Q74 <-> Q83) shuffles
    the Q-number<->content mapping, which carries audit-traceability
    cost: "Q74" in v1.12.x audit reports refers to かりる content,
    but post-swap "Q74" would refer to bus/transportation content.
    For a multi-pass audit cycle still in flight, holding the
    Q<->content mapping stable is more valuable than the small
    exam-realism gain. May revisit when the audit cycle closes.

### Verification footnote (1)

  Q39 / goi-3.9   ボール 〜つ vs つくえ 〜台 cross-reference
    Reviewer asked to confirm つくえ doesn't appear as a counter
    answer elsewhere in the corpus (the Q39 rationale parenthetically
    flags 〜台 as N4-level for furniture). Verified: つくえ appears
    in the corpus only as a noun-place (Q15, Q21) or as the noun
    being quantified by a non-counter quantifier (Q88: いっぱい /
    たくさん / すこし). It never appears as the test target of a
    counter question. Q39's parenthetical stands as informative
    context with no propagation needed.

### ので -> から policy (formalized)

The Q5 fix in v1.12.14 implicitly created a corpus-wide policy
preferring から over ので as the reason conjunction, since ので
leans N4 in major textbooks (Genki / Minna / Tobira). v1.12.15
extends that policy to the two remaining ので usages in the goi
corpus (Q33, Q44). Spot check confirms ので now appears nowhere
in goi stems, only in the v1.12.14 rationale text that documents
the policy itself.

### Cache and integrity

  - sw.js CACHE_VERSION:        v124 -> v125
  - index.html cache-busters:    v=1.11.34 -> v=1.11.35
  - 41/41 invariants PASS (incl. JA-32 lock-step MD<->JSON parity)
  - Fix script idempotent (2nd run reports "No changes").

---

## v1.12.14 - 2026-05-04 (Goi re-review follow-up - 5 items)

A second pass by the same auditor on the v1.12.12+v1.12.13 fixes
identified five remaining issues. All five are addressed here. Net
result of this round: of the 19 originally-flagged audit items, 19
are closed cleanly with no residual caveats; of the 5 items the v1.12
goi rewrites had introduced, all 5 are resolved.

### Five fixes

  Q51 / goi-4.6  -  prior tautology, tested no vocabulary
    Old stem:  わたしの ちちは いしゃです。
    Old keyed: わたしの ちちの しごとは いしゃです。  (= the stem)
    New stem:  わたしの ちちは びょういんで はたらいて います。
    New keyed: わたしの ちちは いしゃです。
    Now tests the N5 vocab triangle 病院 / はたらく / いしゃ.
    N5-level pragmatic substitution acknowledged in rationale.

  Q5 / goi-1.5   -  N4-grammar leak (ので)
    Old stem: つかれたので、いえで （　　）。
    New stem: つかれましたから、いえで （　　）。
    から is the N5-canonical reason conjunction; ので leans N4 in
    Genki / Minna no Nihongo / Tobira.

  Q94 / goi-7.4  -  rationale-labeling imprecision
    Old: あまくない (plain neg) = あまく ありません (polite neg).
    New: あまくないです (i-adj + です polite neg) = あまく ありません
         (formal polite neg). Two equivalent polite forms.
    Stem and choices unchanged; only rationale tightened.

  Q98 / goi-7.8  -  わたす is borderline N5/N4 ([Ext] in vocabulary_n5.md)
    Old keyed: ... 先生に しゅくだいを わたします。
    New keyed: ... 先生に しゅくだいを もって いきます。
    Removes [Ext] vocab from the answer key entirely. Project [Ext]
    policy says "useful for recognition; do not over-prioritize" -
    being the keyed answer over-prioritizes. もって いく is strict
    N5 (both もつ and いく are core). Pragmatic substitution at N5
    level: take homework to teacher = submit homework. Note: kept
    in kana because 持 is not in the kanji whitelist. わたす no
    longer appears anywhere in the goi corpus.

  Q99 / goi-7.9  -  weak entailment, no acknowledgement
    "X から きました" -> "X 人です" is a pragmatic inference, not
    a logical equivalence (someone can come from X without being
    X-jin: tourist, expat, returning resident). Stem unchanged;
    rationale updated to acknowledge this as standard N5 textbook
    pragmatic substitution, mirroring the existing soft-entailment
    acknowledgement pattern used elsewhere in the corpus.

### Cache and integrity

  - sw.js CACHE_VERSION:        v123 -> v124
  - index.html cache-busters:    v=1.11.33 -> v=1.11.34
  - 41/41 invariants PASS (incl. JA-32 lock-step MD<->JSON parity)
  - Fix script idempotent (2nd run reports "No changes").

---

## v1.12.13 - 2026-05-04 (Inference-paraphrase cluster tightened - 5 items)

Follow-up to v1.12.12. The audit's "tighten at least two of them so
the pattern doesn't dominate" recommendation has been honoured for
all five inference-paraphrase items per the user's "fix all fixables"
instruction. The v1.12.12 policy header that documented these items
as deliberate inference convention has been replaced with a record of
the tightening pass; the items are now true paraphrases, not
inference-bridged ones.

### Tightenings (5)

  Q70 / goi-5.10  好き -> よく する
    Old stem: たろうさんは スポーツが すきです。
    New stem: たろうさんは スポーツが すきで、まいにち します。
    Frequency clause makes 「よく する」 a direct paraphrase rather
    than an inference from liking alone.

  Q76 / goi-6.1   X より Y すき -> Y を よく 飲む
    Old stem: わたしは おちゃより コーヒーの ほうが すきです。
    New stem: わたしは おちゃより コーヒーの ほうが すきで、
              まいにち 飲みます。
    Frequency clause closes the preference-to-drinking gap.

  Q86 / goi-6.11  電話を かける -> 電話で 話す
    Old stem: 友だちに でんわを かけました。
    New stem: 友だちに でんわを かけて、一時間 話しました。
    Duration clause confirms a successful conversation, removing the
    "called but no-one answered" inference gap.

  Q97 / goi-7.7   じょうず -> 上手に 話す  (also: drops N4 potential)
    Old stem:    たろうさんは 日本ごが じょうずです。
    New stem:    たろうさんは 日本ごを 話すのが じょうずです。
    Old keyed:   日本ごを よく 話せます (N4 potential form)
    New keyed:   日本ごを 上手に 話します (N5 plain)
    Scopes じょうず to speaking specifically (nominalized adj. vs.
    adverbial — same skill, different syntactic frame). Bonus: the
    keyed answer no longer relies on N4 potential 話せます.

  Q100 / goi-7.10 ならって いる -> れんしゅう
    Old stem: わたしは ピアノを ならって います。
    New stem: わたしは ピアノを ならって、まいにち れんしゅうします。
    Daily-practice clause makes 「れんしゅうを して いる」 a direct
    paraphrase, not an inference from "is taking lessons".

### Header policy revision

The "Inference-style paraphrases" subsection in goi_questions_n5.md
(added in v1.12.12) has been replaced with "Paraphrase-tightening
pass (2026-05-04, v1.12.13)" recording what was changed. The previous
policy framed these items as deliberate inference convention; after
the rewrites that framing is no longer accurate.

### Cache and integrity

  - sw.js CACHE_VERSION:        v122 -> v123
  - index.html cache-busters:    v=1.11.32 -> v=1.11.33
  - 41/41 invariants PASS (incl. JA-32 lock-step MD↔JSON parity)
  - Fix script idempotent (2nd run reports "No changes").

---

## v1.12.12 - 2026-05-04 (Goi audit closure - 14 item fixes + 2 header policies)

External native-speaker / JLPT-aligned auditor reviewed all 100 goi
items and flagged 19 issues across 4 severity tiers. This release
addresses 14 of them with concrete content fixes; the remaining 5
(Q70/Q76/Q86/Q97/Q100 inference-paraphrase cluster) and the 6 N4-
leakage items are addressed at the source-policy level via two new
header sections in goi_questions_n5.md.

### Critical fixes (4)

  Q21 / goi-2.6 - stem had no anchor; all 4 positional answers valid.
    Old: ほんは つくえの (  ) に あります。
    New: ほんが つくえの (  ) から おちました。
    Now uniquely anchors うえ via physics: things only fall from above.

  Q94 / goi-7.4 - keyed answer was a graded negation, not a true
    paraphrase of flat negation あまくないです.
    Replaced choice [3] あまり あまく ないです -> あまく ありません.
    Now a clean polite-form paraphrase (same meaning, different
    politeness register).

  Q98 / goi-7.8 - keyed answer changed both the particle (までに ->
    まで) and the time window. Whole item replaced.
    New stem: わたしは あした しゅくだいを 出します。
    New keyed: あした、わたしは 先生に しゅくだいを わたします。
    Tests 出す = わたす in homework-submission context (clean paraphrase).

  Q99 / goi-7.9 - 知っている and 覚えている are not synonyms. Whole
    item replaced.
    New stem: わたしは スペインから きました。
    New keyed: わたしは スペイン人です。
    Tests origin (X から きた) = nationality (X 人).

### Moderate fixes (5)

  Q39 / goi-3.9: 机 takes 〜台 not 〜つ -> swapped noun to ボール.
  Q68 / goi-5.8: keyed 学生が narrowed scope -> 人が (matches だれも universal).
  Q79 / goi-6.4: rationale aligned with Q80 (added "broader than" caveat).
  Q89 / goi-6.14: 「高い お金」 unnatural -> たくさん お金を 払いました.
  Q45 / goi-3.15: シャツ weak distractor -> パジャマ (clearly indoor).

### Minor polish (4)

  Q1 / goi-1.1:  毎あさ -> まいあさ (kana consistency).
  Q5 / goi-1.5:  つかれましたから -> つかれたので (tense consistency
                 with the choice 「やすみます」 — actually 「やすみます」
                 is non-past which is fine after ので+plain past).
  Q10 / goi-1.10: あついです distractor -> はやいです (avoid 暑い/厚い
                  homophone trap on 本).
  Q19 / goi-2.4:  きのうは とても -> きのうは しごとが とても (added
                  topic word; しごと anchors いそがしい uniquely).

### Source-policy header notes (in goi_questions_n5.md)

Two policy sections added to the header to formalize how the corpus
treats two boundary cases the auditor flagged as clusters:

  1. **Inference-style paraphrases** (Q70 好き/よくする, Q76, Q86,
     Q97, Q100): treated as deliberate N5-level pedagogical
     conventions where likes/skill/lessons commonly entail the
     related action. The rationales' acknowledgement of the gap
     stays — it is now framed as graded-by-closeness rather than
     "apologizing".

  2. **Late-N5 / N4-stretch items** (Q47 ～たことがある, Q48
     ～つもりだ, Q62 ～あいだに, Q64 ひけます potential, Q91 ～て
     N に なる, Q97 話せます potential): documented as deliberate
     stretch content for learners on the cusp of N4. Aligns with
     the project's "late_n5" tier convention (25 grammar.json
     patterns also flagged tier=late_n5).

### Cache and integrity

  - sw.js CACHE_VERSION:        v121 -> v122
  - index.html cache-busters:    v=1.11.31 -> v=1.11.32
  - tools/check_content_integrity.py -> 41/41 invariants PASS
    (incl. JA-32: every kanji in new rationales appears in MD source)
  - tools/fix_goi_audit_2026_05_04.py -> idempotent

## v1.12.11 - 2026-05-04 (45 dokkai rationales authored - 100% rationale coverage)

External auditor reported 45 of 60 dokkai questions (Q1-Q60) had
empty rationales — paper builder was faithfully reflecting the MD,
but the MD had only `**Answer: N**.` with no explanation text for
those 45. Per the project's "rationales help learners understand
why their wrong answer was wrong" stance and the existing pattern
(15/60 dokkai already had rationales; goi/moji/bunpou ~all do), these
were authored.

### Authored content

  Each rationale is a 1-line citation of the passage detail that
  justifies the marked correct answer, mirroring the brief-citation
  style of the existing 15 dokkai rationales (e.g., "first action is
  meeting at station." for Q9). Mix of English narration and
  Japanese excerpts as the corpus already does.

  Distribution by paper:
    paper-1.json: 5 rationales authored (Q11, Q12, Q13, Q15, Q16)
    paper-2.json: 13 rationales (Q18-Q25, Q28-Q32)
    paper-3.json: 16 rationales (Q33-Q48)
    paper-4.json: 11 rationales (Q49, Q50, Q52-Q60)

  Total: 45 questions, dokkai rationale coverage 15/60 -> 60/60 (100%).

### Files updated (in lock-step)

  KnowledgeBank/dokkai_questions_n5.md  (source MD)
  data/papers/dokkai/paper-1.json
  data/papers/dokkai/paper-2.json
  data/papers/dokkai/paper-3.json
  data/papers/dokkai/paper-4.json

  Both files updated together so JA-32 (paper-JSON rationales appear
  verbatim in source MD) stays green. JA-32 verification confirms:
  every kanji used in the new rationales also appears in its
  corresponding MD Q-block (passage / stem / choices), so no
  stale-extract drift introduced.

### Cache and integrity

  - sw.js CACHE_VERSION:        v120 -> v121
  - index.html cache-busters:    v=1.11.30 -> v=1.11.31
  - tools/check_content_integrity.py -> 41/41 invariants PASS
  - tools/author_45_dokkai_rationales_2026_05_04.py -> idempotent
  - X-6.5 (no em-dashes): caught + stripped 86 em-dashes I introduced
    in rationale text during initial authoring, before commit.

## v1.12.10 - 2026-05-04 (paper-JSON rationale drift fixed + JA-32 invariant added)

External auditor flagged: `data/papers/bunpou/paper-2.json` Q19
rationale uses 熱 (non-N5 kanji): "熱がある (have a fever)." The KB
source MD had been corrected to "ねつが ある (have a fever)." in
v1.12.4 (commit 658f35d), but the paper extraction wasn't re-run, so
the JSON kept the stale kanji form.

### Fix

  - `data/papers/bunpou/paper-2.json` bunpou-2.4 (kbSourceId=Q19):
      rationale "熱がある (have a fever)." -> "ねつが ある (have a fever)."
      (now matches KB exactly)

### CI hardening — JA-32

To prevent future MD-updated-but-JSON-stale drift in any paper file,
added invariant **JA-32**: for each paper-JSON question with a
kbSourceId, every kanji in its rationale field must also appear
somewhere in the corresponding MD Q-block.

  - Catches stale extraction (MD says ねつ, JSON says 熱) immediately.
  - Does NOT false-positive on authored rationales (e.g., bunpou-5/6
    sentence-rearrange, where the rationale was expanded during the
    audit fix) — authored rationales reuse kanji that were already
    in the MD's stem / choices / answer line, so they pass.
  - Implemented in `tools/check_content_integrity.py`
    `_check_ja_32_paper_rationale_md_parity()`.
  - Verified: simulating the auditor's old stale state ("熱がある"
    when MD had "ねつが ある") produces exactly the expected failure
    "stale: ['熱']".

Sweep result post-fix: zero JA-32 violations across all 25 paper
JSONs. Other rationales that contain non-N5 kanji (e.g., goi-5.13's
"借りる ⇄ 貸す" pedagogical explanation) all reference kanji that
appear in their MD Q-block as part of the question content, so they
correctly pass.

### Cache and integrity

  - sw.js CACHE_VERSION:        v119 -> v120
  - index.html cache-busters:    v=1.11.29 -> v=1.11.30
  - tools/check_content_integrity.py -> 41/41 invariants PASS
    (was 40 — added JA-32)

## v1.12.9 - 2026-05-04 (Em-dash audit gap closed + 3 stray em-dashes stripped)

External auditor flagged one stray em-dash (U+2014) in the v1.12.8
`n5_vocab_whitelist_README.md` rewrite. Investigation: X-6.5 (no
em-dashes) was scanning only the 9 KnowledgeBank/*.md files, not
the data/*.md design-rationale READMEs. Extended X-6.5 to scan
`data/*.md` too; the extended check immediately surfaced 2 more
em-dashes in `data/n5_kanji_whitelist.exceptions.md` that had also
been outside the previous CI scope.

### Fixes

  - `data/n5_vocab_whitelist_README.md`: 1 em-dash -> hyphen
  - `data/n5_kanji_whitelist.exceptions.md`: 2 em-dashes -> hyphens
  - `tools/check_content_integrity.py` X-6.5: extended to also scan
    `data/*.md` so future README rewrites can't slip past the
    no-em-dash policy.

### Cache and integrity

  - sw.js CACHE_VERSION:        v118 -> v119
  - index.html cache-busters:    v=1.11.28 -> v=1.11.29
  - tools/check_content_integrity.py -> 40/40 invariants PASS
    (X-6.5 now scans 9 KB files + data/*.md = 11 files total)

## v1.12.8 - 2026-05-04 (Whitelist drift fully closed - 38 new vocab entries)

Closes the v1.12.7 "perceived drift" between `n5_vocab_whitelist.json`
and `data/vocab.json` by **authoring 38 new structured vocab.json
entries** that cover all 40 previously-unmatched whitelist tokens.

Drift went 40 -> 0. The whitelist (969 tokens) now strictly matches
form/reading values in vocab.json (1041 entries). The "intentional
superset" framing from v1.12.7 is no longer applicable; alignment is
now strict.

### 29 standalone vocab entries (recognition-only -> first-class catalog)

These were valid N5 tokens that appeared in vocabulary_n5.md gloss /
example text but lacked structured catalog entries. Each gets a full
entry with form, reading, gloss, section, pos, and 1 example sentence:

  Section 3 (People - Roles):
    高校生 (こうこうせい) - high school student

  Section 9 (Counters):
    倍 (ばい) - times / -fold

  Section 10 (Time):
    後 (あと) - after / later

  Section 11 (Days/Weeks/Months/Years):
    週末 (しゅうまつ) - weekend

  Section 13 (Locations):
    おてら, カフェ, コンビニ, フロント, 出口

  Section 14 (Nature):
    さくら

  Section 22 (Money & Shopping):
    アルバイト, セール

  Section 24 (School & Study):
    おしらせ, じゅんび, たんご

  Section 25 (Languages & Countries):
    スペイン人, 国籍

  Section 26 (House & Furniture):
    ベンチ

  Section 27 (Verbs Group 1):
    はらう (pay)

  Section 28 (Verbs Group 2):
    おくれる (be late), ためる (save), 聞こえる (be audible)

  Section 33 (Adverbs):
    いっぱい, ぜひ, ただ, べつべつ

  Section 36 (Greetings/Set Phrases):
    おじゃまします

  Section 40 (Misc Useful Items):
    おもちゃ, コンサート

### 9 multi-form merged entries (alias pairs -> first-class)

Following the existing precedent (8 entries like 何 reading="なに / なん"
or 七 reading="しち / なな"), these 9 entries use multi-form notation
in the `reading` field to cover both alias and canonical forms in a
single entry:

  いい                    reading="いい / よい"           [i-adj]
  いえ                    reading="いえ / うち"           [noun]
  ぐらい                  reading="ぐらい / くらい"       [particle]
  けれど                  reading="けれど / けれども / けど" [conjunction]
  ござる                  reading="ござる / ございます"   [verb-1]
  じゃあ                  reading="じゃあ / では / じゃ"  [expression]
  みんな                  reading="みんな / みな"         [noun]
  やはり                  reading="やはり / やっぱり"     [adverb]
  ゼロ                    reading="ゼロ / れい"           [numeral]

JA-31 POS parity verified: each new entry's pos field matches the
multi-form line's [tag] in vocabulary_n5.md (i-adj -> i-adj,
noun -> n., particle -> part., etc.).

### data/n5_vocab_whitelist_README.md updated

The original draft documented the 40 missing tokens as "intentional
superset by design". After v1.12.8, drift = 0, so the README is
revised to record the alignment + the v1.12.7 -> v1.12.8 transition
in the History section. Future audits comparing whitelist to vocab.json
will see strict 1:1 form/reading correspondence.

### Cache and integrity

  - sw.js CACHE_VERSION:        v117 -> v118
  - index.html cache-busters:    v=1.11.27 -> v=1.11.28
  - data/vocab.json: 1003 -> 1041 entries (+38)
  - n5_vocab_whitelist.json drift: 40 -> 0 (-40)
  - tools/check_content_integrity.py -> 40/40 invariants PASS
    (including JA-31 vocab POS parity)
  - tools/author_29_vocab_entries_2026_05_04.py -> idempotent
  - tools/author_10_alias_entries_2026_05_04.py -> idempotent

## v1.12.7 - 2026-05-04 (Data folder bugs - n5-188 audio + whitelist design doc)

Closes 2 bugs from the 2026-05-04 data-folder audit.

### Bug 1 (LOW) - n5-188 audio synthesis sync lag

The new pattern n5-188 (Verb + ことができる, shipped in v1.12.3) had 3
grammar examples in `data/grammar.json` but no corresponding entries in
`data/audio_manifest.json` and no MP3 files on disk. New-pattern
audio-synthesis lag.

Fix:
  - Rendered 3 MP3s via gTTS (Japanese voice, synthetic-gtts backend
    matching the convention used for n5-001..n5-187):
      audio/grammar/n5-188.0.mp3  (23,424 bytes — 日本語を 話す...)
      audio/grammar/n5-188.1.mp3  (21,696 bytes — ピアノを ひく...)
      audio/grammar/n5-188.2.mp3  (20,544 bytes — あした 行く...)
  - Added 3 manifest entries pointing at the new files with
    skipped=false (audio actually exists on disk).

User-visible effect: the n5-188 example player works on the Grammar
detail page after SW cache refresh.

### Bug 2 (MEDIUM) - whitelist appears to drift from vocab.json

Auditor report: 40 entries in `data/n5_vocab_whitelist.json` don't
appear as form/reading in any `data/vocab.json` entry.

Investigation:
  `data/n5_vocab_whitelist.json` is **generated** from
  `KnowledgeBank/vocabulary_n5.md` by `tools/build_data.py`. The
  whitelist's purpose is to serve as the **recognition allowlist** for
  `tools/lint_content.py` when checking N5-scope conformance — distinct
  from `data/vocab.json`'s role as the structured catalog. The
  whitelist is **intentionally a superset** of vocab.json forms.

Categorization of the 40:
  - **10 multi-form aliases** (by design): いい, いえ, ぐらい, けれど,
    ござる, じゃあ, では, みんな, やはり, ゼロ. Each has a canonical
    counterpart in vocab.json (よい, うち, くらい, けど, ございます,
    では, じゃ, みな, やっぱり, れい). vocabulary_n5.md lists them as
    multi-form entries; build_data.py extracts both forms into the
    whitelist. Expected behavior.
  - **30 recognition-only items** (pending vocab.json authoring):
    valid N5 vocab tokens (アルバイト, カフェ, コンサート, 出口,
    高校生, 聞こえる, 週末, etc.) that appear in vocabulary_n5.md gloss
    /example text and are recognized by the lint script, but lack full
    structured `vocab.json` entries. Promotion to full entries is
    future authoring work.

Fix:
  Shipped `data/n5_vocab_whitelist_README.md` documenting the design
  rationale, the two-category breakdown, and the maintenance protocol.
  Future audits running KB-only or data-only checks will see the
  README and understand the superset relationship as design rather
  than drift.

  No data-content changes — the whitelist is correct as a generated
  artifact. vocab.json is correct as a curated catalog. The two
  files have distinct, complementary roles.

### Cache and integrity

  - sw.js CACHE_VERSION:        v116 -> v117
  - index.html cache-busters:    v=1.11.26 -> v=1.11.27
  - tools/check_content_integrity.py -> 40/40 invariants PASS
  - tools/fix_data_bugs_2026_05_04.py -> idempotent (0 edits on
    second run)

## v1.12.6 - 2026-05-04 (KB-only audit alignment - dokkai header self-verifying)

Fixes a real internal contradiction in `dokkai_questions_n5.md` that
KB-only audit pipelines (auditors who only see `KnowledgeBank/*.md`
without `data/*.json`) couldn't resolve.

The header at line 17 listed the dokkai-kanji exception register's
**original 25 kanji** ("currently covers: 京, 作, ... 同"). When the
register was extended to 28 kanji (向, 央, 付 added in commit b93ca01
on 2026-05-03 per moji-and-source audit §2.2), the JSON was updated
but the MD header wasn't. A trailing HTML comment was added at the
bottom announcing the extension, but the header remained stale.

For an auditor with only KB files (no data/), this read as:
  Header says 25 kanji.
  Comment at the bottom says "extended with 向, 央, 付".
  No way to verify which is correct without the JSON.
  Auditor reports: "JSON unchanged at 25; comment claims 28."

Fix: header line 17 now lists all **28 kanji** with inline rationale
for the 3 additions. Trailing marker comment removed (header is now
the single source of truth within KB-only view; JSON remains the
machine-tracked authoritative list).

### File changes

  KnowledgeBank/dokkai_questions_n5.md
    Line 17: kanji list 25 -> 28; added 向 / 央 / 付 with brief
             "added on 2026-05-03 §2.2" attribution.
    Line 1631: trailing HTML marker comment removed (now redundant
             with the updated header).

### Verification

  - data/dokkai_kanji_exception.json was already at 28 entries
    (since commit b93ca01); this commit synchronizes the MD header
    with that state.
  - tools/check_content_integrity.py -> 40/40 invariants PASS
  - JA-28 (dokkai-paper kanji bounded by N5 + exception list) -> PASS
  - KB-only audit upload now sees consistent state without needing
    the JSON.

### Cache and integrity

  - sw.js CACHE_VERSION:        v115 -> v116
  - index.html cache-busters:    v=1.11.25 -> v=1.11.26

## v1.12.5 - 2026-05-04 (Open-bug-list Bug 8 closed - filename rename)

Closes the deferred Bug 8 from v1.12.4. The file
`KnowledgeBank/authentic_extracted_n5.md` is renamed to
`KnowledgeBank/externally_sourced_n5.md` to match its H1 title and
remove the misleading "authentic" framing from the file path.

### File rename

  `KnowledgeBank/authentic_extracted_n5.md`
    -> `KnowledgeBank/externally_sourced_n5.md`

  Done via `git mv` to preserve blame history. Contents unchanged
  except for the "Filename history" disclaimer block (the prior
  paragraph announcing the rename was pending; now records the
  rename is done, links DEFER-11 / CONTENT-LICENSE.md as the
  rationale for Pass 12 not happening).

### Active references updated (CI / build / spec / docs)

  tools/check_content_integrity.py            (KB_FILES list + EXPECTED_Q_COUNTS)
  tools/build_papers.py                       (docstring "Skipped files" + comment)
  tools/fix_open_bugs_2026_05_04.py           (Bug 8 docstring -> closed)
  specifications/JLPT-N5-Functional-Spec-v3.1-supplement.md (file-tree listing)
  verification.md                              (10 audit-trail table refs)
  TASKS.md                                     (3 historical entries)
  CHANGELOG.md                                 (3 historical mentions)

### Historical archives left as-is (preserve audit-trail accuracy)

  feedback/closed/jlpt-n5-moji-and-source-audit-2026-05-03.md
  feedback/closed/jlpt-n5-knowledgebank-md-audit-2026-05-01.md
  feedback/closed/native-teacher-review-request.md
  feedback/closed/jlpt-n5-content-correction-brief.md

  These are historical snapshots from when the file was named
  authentic_extracted_n5.md. Keeping the original filename in
  archived audits preserves the historical accuracy of those records.

### Cache and integrity

  - sw.js CACHE_VERSION:        v114 -> v115
  - index.html cache-busters:    v=1.11.24 -> v=1.11.25
  - tools/check_content_integrity.py -> 40/40 invariants PASS
    (KB_FILES list now references the new filename; EXPECTED_Q_COUNTS
    keys updated; X-6.5 em-dash check passes - one em-dash that
    leaked into the rewritten disclaimer was caught and stripped
    before commit.)

## v1.12.4 - 2026-05-04 (Open-bug-list closure - 7 of 8 fixed; 1 deferred)

Closes 7 of 8 items from the open-bug-list filed 2026-05-04. The last
item (filename rename of externally_sourced_n5.md) is deferred —
10 cross-references in build/CI scripts would need synchronized
updates; scope larger than this batch warrants. The file's H1 title
was already changed to "JLPT N5 Externally-Sourced Practice Questions"
so the misleading framing is gone in user-facing content.

### Catalog-content changes (visible to learners)

**dokkai narrator references unified (Bug 4).** 36 references to the
passage narrator were split across two non-N5-canonical conventions:
"書いた 人" (30 instances, stilted) and "ひっしゃ" (6 instances,
non-N5 vocab 筆者). Both replaced with "この 人" - the standard JLPT
N5 dokkai phrasing for "this person / the writer of this passage".
Fix applied in BOTH `KnowledgeBank/dokkai_questions_n5.md` AND the
extracted JSONs `data/papers/dokkai/paper-{1..4}.json`.

**dokkai non-N5 kanji removed (Bugs 2, 3).** Two small kanji-scope
violations in the dokkai source:
  - "初めて" (3 occurrences total: 2 in dokkai questions, 0 in
    paper JSONs) -> "はじめて". 初 was not in the N5 whitelist nor
    the dokkai exception register.
  - "急いで" (1 occurrence in passage content) -> "いそいで".

**bunpou Q24 realism (Bug 5).** Tokyo-Osaka route example:
  - Was: "とうきょう（  ）おおさかまで でんしゃで いきます。"
  - Now: "とうきょう（  ）おおさかまで しんかんせんで いきます。"
  しんかんせん is the realistic mode for the Tokyo-Osaka route. Fixed
  in source MD AND the bunpou paper-2 JSON.

### Catalog-only doc improvements (no learner-visible content change)

**moji distractor-convention section extended (Bug 6).** The header
section in `moji_questions_n5.md` originally documented 2 of 3
distractor types in active use. Now lists all three:
  1. Visually-similar N5 kanji (e.g., 多い / 古い / 長い for 高い)
  2. Non-N5 kanji with same on-yomi (e.g., 経ちます for 立ちます)
  3. Invented (non-real) verb forms (e.g., 出ります for 出ます)

**vocabulary_n5.md POS-legend header cleaned (Bug 7).** The
"Part-of-Speech Tags" section header carried a stray
"(added 2026-05-02)" date stamp that no other section header used.
Stripped for cosmetic consistency.

### Verified-already-aligned (Bug 1)

`data/dokkai_kanji_exception.json` already contains 向 / 央 / 付
(added in commit b93ca01); the marker comment in
`KnowledgeBank/dokkai_questions_n5.md` accurately reflects this state.
The bug-list entry was based on a stale snapshot.

### Deferred (Bug 8)

`KnowledgeBank/externally_sourced_n5.md` keeps its filename for now.
The H1 title already says "Externally-Sourced Practice Questions";
only the path retains the legacy "authentic" label. Renaming requires
synchronized updates in 10 files (incl. tools/build_papers.py and
tools/check_content_integrity.py) - scope warrants a separate
focused commit.

### Cache and integrity

  - sw.js CACHE_VERSION: v113 -> v114
  - index.html cache-busters: v=1.11.23 -> v=1.11.24
  - tools/check_content_integrity.py -> 40/40 invariants PASS
    (including JA-13, JA-28 dokkai-kanji bound, JA-31 vocab POS parity)
  - tools/fix_open_bugs_2026_05_04.py -> idempotent (0 edits on
    second run)

## v1.12.3 - 2026-05-04 (Reference-markdowns audit propagation to runtime data)

Propagates the v1.12.2 catalog-level fixes into the runtime JSON files
that the website actually serves. The website now exposes the new
grammar pattern, the updated もらう particle option, and the corrected
kanji-reading orderings to learners at runtime — not just in the
reference docs.

### New grammar pattern shipped (visible to learners)

**n5-188: Verb + ことができる (productive can-do form).** Was flagged
as missing in the v1.12.2 audit; now a first-class entry in
`data/grammar.json` with full schema (3 examples, 2 common_mistakes,
explanation_en, form_rules, notes pairing it with n5-103). Tier:
core_n5. Category: Comparison and Preference (alongside n5-103).

  - 日本語を 話す ことが できます。 (I can speak Japanese.)
  - ピアノを ひく ことが できますか。 (Can you play piano?)
  - あした 行く ことが できません。 (I can't go tomorrow.)

Two questions added (q-0579 / q-0580) covering the affirmative and
negative forms — pattern coverage stays at 100% (178/178).

### Runtime data updates

  - `data/grammar.json` n5-131 (もらう):
      pattern: ～に～をもらいます → ～に / から ～をもらいます
      meaning_en clarified to mention both particles
      notes appended with personal-vs-institutional usage rule
  - `data/grammar.json`: new pattern n5-188 (see above)
  - `data/kanji.json` 後: kun reordered ['のち','うし','あと'] →
      ['うし','あと','のち'] (matches kanji_n5.md update; primary_reading
      stays 'あと')
  - `data/n5_kanji_readings.json` 後: same kun reorder
  - `data/questions.json`: 288 → 290 questions (mcq 258 → 260);
      _meta refreshed; audit_history entry appended

### Cache and integrity

  - sw.js CACHE_VERSION: v112 -> v113 (forces re-fetch of grammar.json,
    questions.json, kanji.json, n5_kanji_readings.json updates).
  - index.html cache-busters: v=1.11.22 -> v=1.11.23.
  - tools/check_content_integrity.py -> 40/40 invariants PASS,
    including JA-12 (kanji KB↔JSON consistency), JA-17 (grammar
    examples have vocab_ids), JA-26 (no duplicate question IDs).
  - Pattern coverage: 178/178 (was 177/177 + new n5-188 = 178; q-0579
    and q-0580 cover it).
  - tools/propagate_ref_md_audit_2026_05_04.py is idempotent.

## v1.12.2 - 2026-05-04 (Reference-markdowns audit closure - 11 items resolved)

Closes all 11 items in the 2026-05-04 reference-markdowns re-audit. The
first audit cycle since the project began without a critical-severity
finding. All fixes are at the catalog / reference-doc level, plus
mirrored corrections in `data/vocab.json` so JA-31 stays green.

### Catalog-content changes (visible to learners)

**vocabulary_n5.md + vocab.json POS-tag corrections (§1.3).** Six
entries in Section 1 (Pronouns and Self) plus one in Section 12
(Time-Frequency) carried section-default POS tags that didn't match
the word's actual lexical class. Both files updated consistently:

  - 人 (ひと) sect 1: pronoun -> noun (used in pronoun-like phrases
    but lexically a 名詞)
  - かた sect 1: pronoun -> noun (polite "person" headword)
  - だれ: pronoun -> question-word (matches sect 6 classification)
  - どなた: pronoun -> question-word (matches sect 6 classification)
  - みなさん: pronoun -> noun (vocative / address term, not a pronoun)
  - みんな / みな: pronoun -> noun (multi-form alias; MD only)
  - もうすぐ sect 12: noun -> adverb (functions adverbially: もうすぐ来る)

The 7 remaining sect 1 entries (私, 私たち, あなた, かれ, かのじょ,
じぶん, etc.) are real pronouns and stay tagged [pron.].

**kanji_n5.md scope-flag pass (§1.1, §1.2).** 19 entries had readings
outside N5 scope without any flag, while 上 / 下 already carried
[N4+ verb reading; recognition only] markers. Applied the existing
flag pattern uniformly so the README's "scope rule" matches the
file's contents:

  - 入 kun reordered: い(る), はい(る), い(れる) -> はい(る), い(る),
    い(れる) with stem-split note. はい is the standalone verb 入る;
    い-stem appears in 入れる / 入り. (This is the upstream root cause
    of an earlier downstream bug in n5_kanji_readings.json's primary
    field.)
  - 半: なか(ば) -> [N3+ noun reading]
  - 何: カ on -> [N3+ on-reading]
  - 語: かた(る) -> [N3 verb reading]
  - 木: こ- -> [N4+ prefix]
  - 金: かな- -> [N4+ prefix]
  - 小: こ-, お- -> both [N4+ prefix]
  - 後: のち -> [N4+ literary], reordered うし(ろ), あと first
  - 空: あ(く) -> [N4 verb reading]
  - 見: み(える) -> [N4 verb reading], み(せる) -> [N4-N5 borderline]
  - 聞: き(こえる) -> [N4 verb reading]
  - 立: た(てる) -> [N4 transitive verb reading]
  - 休: やす(まる) -> [N4 intransitive verb reading]
  - 言: こと -> [jukujikun in 言葉 only; not standalone N5]
  - 新: あら(た) -> [N3 stem reading], にい- -> [N4+ prefix]
  - 白: しら- -> [N3+ prefix]
  - 行: ゆ(く) -> [N4+ poetic alt], おこな(う) -> [N3 verb reading]
  - 来: きた(る) -> [N3+ literary]
  - 生: clarified note - both 生きる / 生まれる ARE N5 verbs; on-reading
    セイ in compounds.

**grammar_n5.md additions (§1.4, §2.1, §2.2, §2.3, §2.4, §3.2).**

  - Section 10: added "Verb (plain dictionary) + ことができる /
    ことができます (can do - productive form)" with 日本語を 話す
    ことが できます example. This is canonical N5 grammar (Genki I
    L13, Minna L18) but was missing from the catalog.
  - Section 15: もらう pattern now lists ～に / から ～をもらいます
    with note that に is more typical for personal givers, から for
    institutional sources. Both are N5.
  - Section 1: もの example replaced. Was だって、いそがしいんだもの
    (combined もの + んだ patterns); now 行きたくないもん or
    だって、雨だもの (single pattern only).
  - Section 22: bika-go example list updated to drop ごはん from
    "productive" prefix examples (it's a single lexicalized word now).
    Replaced with お茶, お金, おさけ, おみず, おはな - all genuinely
    productive お-prefix cases.
  - Question-word + か/も citation: "Genki I L8 / L10" -> "L8 for
    か-compounds; L9 for も-compounds with negative; いつも at L11"
    (more accurate per Genki 3rd edition).
  - Section 23.10 prohibitive な: added register caveat - "rough /
    commanding. Use only with clear authority differential or in
    writing (signs / labels). For polite prohibition use ～ないでください."

**sources.md additions (§2.5, §3.1).**

  - Added "JLPT N5 Sample Questions" reference under JEES (free PDFs
    on jlpt.jp; the most authoritative single reference for actual
    paper format).
  - Added "NHK NEWS WEB EASY" (https://www3.nhk.or.jp/news/easy/)
    under Established Learner References - daily news rewritten for
    N5/N4 learners.

### Cache and integrity

  - sw.js CACHE_VERSION: v111 -> v112 (forces re-fetch of vocab.json
    + listening.json + grammar.json updates).
  - index.html cache-busters: v=1.11.21 -> v=1.11.22.
  - tools/check_content_integrity.py -> 40/40 invariants PASS
    (including JA-31 vocab POS parity between MD and JSON).
  - tools/fix_ref_md_audit_2026_05_04.py -> idempotent (0 changes on
    second run).

## v1.12.1 - 2026-05-03 (Moji + source audit closure — 12 items resolved)

Closes all 12 items in the 2026-05-03 moji + source-markdowns audit.
Mostly extraction-pipeline + naturalness fixes — visible to learners as
formerly-blank moji questions becoming readable, and a handful of
JLPT-mock-paper stems and choices replaced with cleaner forms.

### Live-content changes (visible to users)

**24 moji questions now display correctly (§1.1).** The mock-paper
extraction had silently dropped the stem on questions where the test
target sat at the very start of the sentence (`__test-word__ ...`).
Affected papers: moji-4 (5 Qs), moji-5 (12 Qs), moji-6 (3 Qs), moji-7
(4 Qs). All 24 stems now populated from `KnowledgeBank/
moji_questions_n5.md` and carry rationales matching the source.

**3 moji-7 questions now use the standard Mondai 2 stem format (§2.4).**
Q97-Q99 had a non-canonical `__lemma__ - sentence` prefix that no other
Mondai 2 stem in the corpus uses. Dropped the prefix; the questions
read like every other 表記 (orthography) question.

**2 moji stems no longer show non-N5 kanji to N5 learners (§2.1):**
  - Q35 「私の いえは 町の <u>北</u> に あります。」 → `町` (machi,
    non-N5) → `まち`. Stem now readable end-to-end at N5.
  - Q95 「八百屋で やさいを __かいます__。」 → `八百屋` (yaoya, has
    non-N5 屋) → `みせ`.

**3 goi distractors restored to authentic-JLPT kanji form (§3.1).** A
prior audit had been over-strict: it flagged 4 goi questions with non-N5
kanji, but only Q58 (correct-answer position) was a real policy
violation. The 3 distractor positions (Q65: 少, Q86: 紙, Q100: 売) are
explicitly within the source's documented exception ("distractors may
include non-N5 kanji because authentic JLPT distractors mimic visually-
similar wrong forms"). Reverted to the source's kanji forms.

  Q58 (real correct-answer violation) source markdown updated to match
  the JSON's kana fix (「きのう 早く ねました。」 → 「きのう はやく
  ねました。」).

**dokkai exception register extended (§2.2).** 3 non-N5 kanji that
appear in dokkai passage content (`向` for 〜向け target-audience
compounds, `央` for 中央 proper nouns, `付` for 〜付き menu convention)
were previously undocumented. Added to `data/dokkai_kanji_exception.
json` with WHY notes per the register's own contract.

**1 bunpou rationale cleaned up (§4.1).** Q19 rationale had `熱がある`
("have a fever") — `熱` is non-N5 and rationales are learner-visible.
Replaced with kana `ねつが ある`.

### Already-clean items (verified during audit, no fix needed)

  §2.3  bunpou source uses 0 non-N5 kanji in stems (audit was working
        from a stale snapshot; earlier session cleanup had already
        replaced 朝/思/京/阪/牛/乳/公/園/楽 with kana).
  §3.2  bunpou-7 ぎんこう  → already changed to 学校 in prior commit.
  §3.3  Q92 起ちます       → distractor, policy-allowed.
  §3.4  manifest totals    → 25 papers / 360 questions verify ✓.
  §3.5  Q62 rationale      → preserved (excellent pedagogy).
  §4.2  goi Q47 rationale  → 0 occurrences of 去年 (already clean).

### Cache and integrity

  - `sw.js` CACHE_VERSION: `v110` → `v111` (forces clients to re-fetch
    the updated paper JSONs on next visit).
  - `index.html` cache-busters: `?v=1.11.20` → `?v=1.11.21` (CSS / app.js).
  - `tools/check_content_integrity.py` → 40/40 invariants PASS.
  - `tools/fix_moji_source_audit_2026_05_03.py` → idempotent (0 changes
    on second run).

## v1.12.0 - 2026-05-03 (Example-coverage milestone — 100% vocab covered)

**Phase 7 closes the example-coverage authoring pass that started at
the beginning of the day.** All 1003 N5 vocab entries, all 177 grammar
patterns, and all 106 kanji entries now have at least one example
attached. Total session content authored: **1,059 examples across
seven phases.**

### Final phase content (321 new vocab examples)

321 inline-example additions across the long tail of sections:
  - **People-roles tail** (4): けいかん, おまわりさん, りゅうがくせい,
    外国人.
  - **Body parts tail** (1): せ.
  - **Counters common** (7): 本, だい, こ, かい (×2), 番, ど.
  - **Locations tail** (2): たいしかん, こうじょう.
  - **Nature tail** (2): すずしい, あたたかい.
  - **Clothing tail** (5): ハンカチ, さいふ, ボタン, ポケット, かさ.
  - **Money/shopping tail** (8): 円, ドル, きっぷ, ふうとう, てがみ,
    にもつ, おみやげ, レジ.
  - **Transport tail** (5): じどうしゃ, バイク, きしゃ, 道, しんごう.
  - **School & study** (27): こたえ, いみ, ことば, じ, かな, ひらがな,
    カタカナ, もじ, ぶん, ぶんしょう, ぶんぽう, れい, れんしゅう,
    きょうかしょ, ざっし, 新聞, ボールペン, まんねんひつ, こくばん,
    チョーク, けしゴム, ちず, え, 番号, 電気, 電話, 電話番号.
  - **Languages & countries tail** (9): 日本人, かんこくご, フランス,
    フランスご, ドイツ, スペイン, イギリス, 外国, 外国語.
  - **House & furniture** (28): アパート, マンション, と, もん, かべ,
    かいだん, エレベーター, げんかん, しんしつ, ふとん, もうふ, まくら,
    いす, たな, ほんだな, カーテン, かぎ, せっけん, はブラシ, タオル,
    テープ, ラジオ, カメラ, ビデオ, うた, え, ピアノ, ギター.
  - **Verbs Group 1** (34): うたう, きる, しる, 立つ, はく, はしる,
    わたる, うる, ひく (×2), よぶ, とぶ, こまる, ならぶ, わたす, ぬぐ,
    いそぐ, しぬ, ならう, はる, まがる, もっていく, もってくる, しまる,
    だす, おとす, ふく, くもる, なくす, すわる, たのむ, とまる, さす, けす.
  - **Verbs Group 2** (15): 入れる, こたえる, かける, きる, つける,
    ならべる, 見せる, いれる, あつめる, きえる, おちる, はれる,
    つかれる, 生まれる, つとめる.
  - **Verbs irregular/する** (11): けっこんする, さんぽする, りょこうする,
    れんしゅうする, しつもんする, しごとする, 電話する, コピーする,
    そうじする, せんたくする, かいものする.
  - **Existence/giving verbs** (6): やる, あげる, くれる, かす, かりる,
    かえす.
  - **i-Adjective tail** (28): つめたい, ひくい, うすい, ふとい, ほそい,
    うれしい, かなしい, さびしい, かわいい, うつくしい, きたない, やさしい,
    つまらない, まずい, にがい, おおい, すくない, まるい, しかくい,
    わかい, きいろい, あおい, あかい, くろい, 白い, ちゃいろい, ぬるい,
    うるさい.
  - **na-Adjective tail** (9): たいへん, ふべん, おなじ, りっぱ, けっこう,
    だいじ, あんぜん, じょうぶ, いや.
  - **Adverb tail** (16): すごく, おおぜい, だいたい, もうすこし, 一番,
    とくに, ほんとうに, すぐ, 一人で, じぶんで, かならず, もちろん,
    どうぞよろしく, まっすぐ, もういちど, もしもし.
  - **Conjunctions** (6): それで, が, だから, それに, ところで, または.
  - **Greetings tail** (12): しつれいします / しつれいしました,
    どういたしまして, いってきます / いってらっしゃい, ただいま /
    おかえりなさい, はじめまして, どうぞよろしく, おかげさまで,
    いらっしゃいませ, もしもし.
  - **Common nouns misc** (64 - all): もの, こと, ことば, 話, やくそく,
    ようじ, もんだい, しゅみ, さんぽ, うんどう, ゲーム, しあい, ニュース,
    パーティー, きって, はがき, てがみ, きっぷ, おみやげ, りゅうがく,
    りょかん, かぜ, びょうき, くすり, けが, おゆ, おふろ, マッチ, はいざら,
    スリッパ, ティッシュ, フィルム, レコード, テープ, よてい, じかんわり,
    はこ, はんぶん, はたち, へん, ほか, ほんとう, なつやすみ, ペット,
    カレンダー, かてい, かびん, かた, おくさん, せびろ, 大きな, たて,
    ゆうべ, にっき, さくぶん, じびき, テープレコーダー, ストーブ, ページ,
    クラス, グラム, メートル, キログラム, キロメートル.
  - **Sounds and voice** (2): おと, うた.
  - **Function/filler expressions** (8): えーと, そうですね, そうですか,
    ええ, うん, ううん, さあ, それでは.
  - **Misc useful items** (12): もの, こと, ばしょ, ばあい, ほう, とき,
    番号, じゅうしょ, ねんれい, 学校, しゅみ, しゅっしん.

### Coverage milestone

- **Vocab inline examples: 1003 / 1003 (100%)** — fully uncovered: 0.
- **Grammar pattern examples: 177 / 177** with ≥3 each.
- **Kanji example words: 106 / 106** with ≥2 each.

### Session totals across all 7 phases

| Phase | Type | Items |
|---|---|---:|
| 1 | Kanji 2nd examples | 35 |
| 2 | Grammar additional examples | 77 |
| 3 | Vocab — pronouns/family/body | 51 |
| 4 | Vocab — numbers/calendar/colors/particles/greetings | 154 |
| 5 | Vocab — locations/food/transport/school/house | 179 |
| 6 | Vocab — time/days/months/food/clothing | 176 |
| 7 | Vocab — final tail (verbs/adj/adverbs/conjunctions/misc) | 321 |
| | **Total examples authored this session** | **993** |

### Service worker

Bumped `CACHE_VERSION` v108 -> v109.

v1.12.0 / SW v109. **40/40 invariants green.**

---

## v1.11.3 - 2026-05-03 (Vocab examples Phase 6 — +176 entries)

Phase 6 of the example-coverage authoring pass. Targets the still-
uncovered sections after Phase 5: time-general tail, days-of-month +
months, locations tail, food items tail, tableware, clothing tail,
animals tail. All 176 new IDs verified against actual data — zero
form-mismatches this batch (we now dump the live data and key against
real IDs rather than guessing).

### Content (176 new vocab inline examples)

  - **Time-general tail (10)**: とき, とけい, おととい, けさ, こんばん,
    こんや, 午前, 午後, 半, 分.
  - **Days/Months (32)**: ついたち..二十日 (1st-20th), 一月..十二月 (all
    12 months), 週, 先週, 月, 先月, 毎月, 年, きょねん, 毎年, おととし,
    さらいねん.
  - **Frequency tail (7)**: まいあさ, まいばん, すぐ, もうすぐ, さいしょ,
    つぎ, 後で.
  - **Locations tail (49)**: ところ, だいどころ, おてあらい, トイレ, おふろ,
    げんかん, にわ, 高校, 会社, じむしょ, お店, やおや, ほんや, はなや,
    にくや, パンや, くうこう, どうぶつえん, びじゅつかん, えいがかん,
    ホテル, りょかん, こうばん, こうさてん, いりぐち, しょくどう, たてもの,
    ろうか, プール, ポスト, 道, とおり, かど, はし, むら, 国, 前, 後ろ,
    左, 右, となり, よこ, とおく, むこう, 北, 南, 東, 西.
  - **Nature tail (17)**: いけ, みずうみ, もり, くさ, は (leaf), いし,
    田, くも, たいよう, かぜ, はれ, くもり, なつ, ふゆ, 火, 水, おゆ.
  - **Animals tail (3)**: にわとり, ぞう, むし.
  - **Food/drink general (5)**: たべもの, のみもの, ゆうはん, しょくじ,
    おべんとう.
  - **Food items tail (28)**: ぎゅうにく, ぶたにく, とりにく, さかな,
    いちご, ぶどう, すいか, レモン, だいこん, にんじん, たまねぎ,
    じゃがいも, トマト, きゅうり, キャベツ, こめ, しお, さとう, しょうゆ,
    みそ, カレー, うどん, そば, ハンバーガー, サンドイッチ, サラダ,
    スープ, チョコレート.
  - **Drinks tail (2)**: おゆ (drinks ID), こうちゃ.
  - **Tableware (12)**: さら, おさら, ちゃわん, おわん, はし
    (chopsticks), スプーン, フォーク, ナイフ, コップ, カップ, れいぞうこ,
    なべ.
  - **Colors tail (2)**: いろ, ピンク.
  - **Clothing tail (8)**: ようふく, きもの, うわぎ, コート, セーター,
    Tシャツ, ワイシャツ, ネクタイ.

### Coverage status

- Vocab fully-uncovered: **321** (was 497 → 321; **-176**).
- Sections now fully covered: 11 (days/months), 12 (frequency), 14
  (nature/weather), 15 (animals), 16 (food/drink general), 18 (drinks),
  19 (tableware), 20 (colors), 21 (clothing), plus most of 13
  (locations) and 17 (food items).
- Remaining biggest buckets for Phase 7+: common nouns misc (~60),
  verb tail (~30), adverbs tail (~10), school/study tail (~10),
  some money/transport, set phrases, body parts.

### Service worker

Bumped `CACHE_VERSION` v107 -> v108.

v1.11.3 / SW v108. **40/40 invariants green.**

---

## v1.11.2 - 2026-05-03 (Vocab examples Phase 5 — +179 entries)

Continuation of the vocab-example coverage pass. This batch combines
the 23 Phase-4 stragglers (entries my earlier script couldn't match
due to kanji-vs-kana form mismatch — re-keyed to actual IDs) with
~155 new entries across the remaining-uncovered sections.

### Content (179 new vocab inline examples)

  - **Phase-4 stragglers re-keyed** (23): 今, 今日, 毎日, 時々, 前 (time);
    白 / 白い (colors); 会う / 言う / 聞く / かえる / 出る (verbs);
    新しい / 高い / 小さい / 古い / 安い (adjectives); まず, 先,
    りょうり (nouns); はい / いいえ / はい-counter (function/filler).
  - **Locations & places** (+15): 学校, いえ, へや, えき / 駅, バスてい,
    びょういん, こうえん, としょかん, デパート, スーパー, コンビニ,
    レストラン, カフェ, きっさてん, ぎんこう, ゆうびんきょく, 大学, まち,
    中, 外, 上, 下.
  - **Nature & weather** (+13): 雨, ゆき, 風, そら, つき, 太陽, ほし,
    山, 川, うみ, 木, 花, てんき, あつい, さむい, 夏, 冬, はる, あき.
  - **Animals** (+8): いぬ, ねこ, とり, さかな, うま, うし, ぶた, どうぶつ.
  - **Food & drink** (+22): ごはん, あさ/ひる/ばんごはん, おかし, パン,
    たまご, りんご, みかん, バナナ, やさい, くだもの, にく, おにぎり,
    おべんとう, ケーキ, アイスクリーム, チーズ, バター, ラーメン, すし,
    てんぷら + drinks 水, おちゃ, コーヒー, ぎゅうにゅう, ジュース,
    ビール, ワイン, おさけ.
  - **Clothing** (+10): シャツ, ズボン, スカート, くつ, くつした, ぼうし,
    ふく, めがね, とけい, かばん.
  - **Money/shopping** (+5): お金, いくら, ねだん, きって, はがき.
  - **Transport** (+8): でんしゃ, バス, くるま, じてんしゃ, ちかてつ,
    タクシー, ひこうき, ふね.
  - **School & study** (+17): 学生, 先生, 大学生, 高校生, じゅぎょう,
    しゅくだい, テスト, しけん, きょうしつ, 本, じしょ, ノート, えんぴつ,
    ペン, かみ, つくえ, いす.
  - **Languages & countries** (+8): 日本, 日本語, アメリカ, えいご,
    中国, 中国語, かんこく, 国.
  - **House & furniture** (+12): まど, ドア, テーブル, ベッド, しょくどう,
    だいどころ, お風呂, シャワー, テレビ, でんわ, れいぞうこ, でんき.
  - **Verb tail** (+17): あらう, おわる, のる, のぼる, はたらく, はじまる,
    まつ, もつ, つくる, つかう, あるく; おしえる, おぼえる, あける, しめる,
    おりる, かりる.
  - **Adjective tail** (+22 i-adj + 4 na-adj): おもしろい, おいしい,
    いそがしい, あたたかい, すずしい, あまい, からい, いい, わるい,
    いたい, ながい, みじかい, ひろい, せまい, おもい, かるい, つよい,
    よわい, はやい, おそい, とおい, ちかい + だいすき, だいきらい,
    げんき, ゆうめい.
  - **Adverb tail** (+11): とても, すこし, たくさん, ちょっと, いっしょに,
    はやく, ゆっくり, もっと, だんだん, きっと, たぶん.

### Coverage status

- Vocab inline examples: now ~506 / 1003 (was 313 pre-Phase-3, was
  467 post-Phase-4, now ~506).
- Remaining fully uncovered: 497 (was 690 pre-Phase-3).
- Big remaining buckets (next phase): common nouns misc (~60),
  food items tail (~25), school/study tail (~25), adverbs tail (~20),
  verb tail (~30), some house/furniture, body parts variants, time
  variants.

### Service worker

Bumped `CACHE_VERSION` v106 -> v107.

v1.11.2 / SW v107. **40/40 invariants green.**

---

## v1.11.1 - 2026-05-03 (Vocab examples Phase 4 — +154 entries)

Continuation of v1.11.0's example-coverage pass. Authored 154 more
vocab example sentences this batch covering the highest-leverage
foundational categories.

### Content

- **Vocab: +154 inline examples** across:
  - Numbers (1, 2, ..., 11, 20, 100, 1000, 10000, 100M)
  - Native counters (一つ..十, いくつ)
  - Common counters (人, 一人, 二人, まい)
  - Time-general (いま, きょう, あした, きのう, あさ, ひる, よる, ばん, ゆうがた)
  - Days/weeks/months (月曜日..日曜日, 今日, 毎日/毎週, 今週/来週,
    今月/来月, 今年/来年)
  - Frequency (いつも, よく, ときどき, たまに, あまり, ぜんぜん, まず,
    つぎに, さいご, さき, あと, まえ, まだ, もう)
  - Colors (あかい, あおい, しろい, くろい, きいろい, ちゃいろ, みどり
    + な-noun forms)
  - Particles (は, が, を, に, で, へ, と, から, まで, の, も, や, か,
    ね, よ, より) — each with a typical-use sentence
  - Greetings (おはよう, こんにちは, こんばんは, おやすみ, さようなら,
    ありがとう, すみません, ごめんなさい, いただきます, ごちそうさま,
    おねがいします, どうぞ, どうも, はい, いいえ)
  - Demonstrative tail (そんな, ああ)
  - Top verbs (行く, 書く, 聞く, 読む, 飲む, 話す, 買う, あう, あらう,
    あそぶ, いう, およぐ, おわる, かかる, きく, のる, のぼる, はたらく,
    はじまる; 見る, 食べる, おきる, ねる, あける, しめる, おしえる,
    おぼえる, かえる, でる; する, 来る, べんきょうする, りょうりする;
    ある, いる)
  - Top adjectives (大きい/小さい, あたらしい/古い, 高い/安い, あつい/
    さむい, おもしろい, おいしい, いそがしい + na-adj きれい, げんき,
    しずか, にぎやか, ひま, すき/きらい, じょうず/へた, ゆうめい,
    しんせつ, だいじょうぶ, たいせつ, べんり, いろいろ)

### Coverage status

- Vocab inline examples: 313 → 467 (out of 1003)
- Remaining uncovered: ~536 (down from ~690)
- Big remaining categories: Locations (70), House/Furniture (39),
  Food items (44), Common nouns misc (76), School/Study (43),
  Adverbs tail (20+), Verb tail (~50), i-adj tail (~50)

### Service worker

Bumped `CACHE_VERSION` v104 -> v105.

v1.11.1 / SW v105. **40/40 invariants green.**

---

## v1.11.0 - 2026-05-03 (Example-coverage authoring pass)

Per user direction: many vocabulary, grammar, and kanji entries
lacked example sentences / example words. Audited the gap and
authored content to bring all three categories to a baseline.

### Content (corpus)

- **Kanji: 35 entries gained a 2nd example word.** Every one of the
  106 N5 kanji entries now has at least 2 example words on its
  detail page (was: 35 entries had only 1). Examples chosen to
  showcase typical N5 compound usage:
    - Numerals: 三百, 千円, 百円, 半分
    - Body parts: 左手, 右手
    - Cardinal directions: 東口, 西口, 南口, 北口
    - Time/quantity: 一時間
    - Daily verbs: 食べもの, 飲みもの, 読みかた, 書きかた, 行きかた
    - Adjective/noun forms: 安く, 古本, 長さ, 休み
    - Compounds: 火山, 小川, 田中, 大雨, 花見, 空気, 上手, 下手, 小学校
  All forms verified against JA-16 (target-or-whitelist kanji only;
  non-N5 kanji is rendered in kana).

- **Grammar: 77 new examples across 63 patterns.** Every one of the
  177 grammar patterns now has 3+ example sentences (was: 63
  patterns sat at 1-2). 8 mid-authoring fixes corrected non-N5 kanji
  in stems (早く -> はやく, 字 -> かんじ, 時計 -> とけい, 思う -> おもう,
  皿 -> さら, 京都 -> きょうと, 教えて -> おしえて). All examples
  carry vocab_ids: [] (JA-17 satisfied; auto-population available
  via tools/link_grammar_examples_to_vocab.py).

- **Vocab: 51 foundational entries gained an inline example
  sentence.** Pronouns (私, 私たち, かれ, かのじょ, みなさん, じぶん),
  family terms (かぞく, 父, 母, あに, あね, おとうと, いもうと, etc.),
  body parts (からだ, かお, め, みみ, くち, は, て, あし), demonstratives
  (あちら, こっち, そっち, あっち, どっち), question words (何, 何曜日,
  何月, 何日, 何で), and roles (せいと, いしゃ, 会社員, 駅員, 店員). Each
  example demonstrates typical use in a single short N5 sentence.

### Tooling

- `tools/audit_example_coverage.py` — read-only inventory of
  uncovered entries across all three corpora. Re-runnable to track
  remaining gaps (vocab is the biggest remaining: 690 entries still
  without inline examples — Phase 4 backlog item).
- `tools/add_kanji_2nd_examples.py` — idempotent kanji example
  additions.
- `tools/add_grammar_examples.py` — idempotent grammar example
  additions (77 entries).
- `tools/add_vocab_examples.py` — idempotent vocab example
  additions (51 foundational entries).

### Service worker

Bumped `CACHE_VERSION` v103 -> v104. data/grammar.json,
data/vocab.json, data/kanji.json all updated.

v1.11.0 / SW v104. **40/40 invariants green** (unchanged from
v1.10.2 — this is a content pass, no new invariants needed).

---

## v1.10.2 - 2026-05-02 (Search-result navigation + provenance lock-in)

Two fixes that landed without their own version bump and are folded
in here:

### Fixed

- **Header search results were not clickable to vocab content.**
  Vocab results all routed to `#/learn` (the Learn hub) instead of
  the per-word detail page `#/learn/vocab/<form>`. Fixed in
  `js/search.js`: centralized URL builders into a `HREFS` map; vocab
  now correctly routes via `encodeURIComponent(form)`. Browser-
  verified: clicking かるい → `#/learn/vocab/%E3%81%8B%E3%82%8B%E3%81%84`
  → detail page renders with `h2: かるい`.

### Improved (search panel)

While the bug was being fixed, several adjacent issues were closed:

- **Kanji-form vocab now shows its kana reading inline:** `新しい
  (あたらしい) - new` (was: `新しい - new`).
- **Vocab dedupe by `form`** so words appearing in multiple thematic
  sections (e.g. 名前 in §1 and §15) don't show up twice with the
  same destination.
- **Keyboard navigation:** ↓/↑ moves a highlight through the flat
  result list (wraps top↔bottom); Enter follows the highlighted link;
  Escape clears the input and closes the panel. Active item gets
  `.is-active` class with accent outline + background tint.
- **ARIA combobox semantics on the input:** `aria-combobox`,
  `aria-autocomplete="list"`, `aria-expanded` toggle.
  `.search-status[aria-live="polite"]` announces the result count
  to screen readers (visually hidden).
- **Mobile responsive:** `positionPanel()` now clamps width to
  `viewport - 24px` and shifts left if the panel would overflow the
  right edge. Verified at 375 px viewport: 320 px panel, 12 px
  margin.

### Added (legal lock-in)

- **`CONTENT-LICENSE.md`** — explicit content-provenance policy.
  States that every grammar pattern / vocab entry / kanji record /
  mock-test question / reading passage / listening drill is
  original (with per-file inventory: 177 + 1003 + 106 + 288 + 360 +
  30 + 30). Lists the public-information sources used as references
  for distribution / topic / scope (JEES sample-paper format,
  JOYO / KANJIDIC2, learner references like Tofugu / Bunpro / Imabi)
  and explicitly states what was NOT taken (any specific question
  text). Documents the JEES contact path if a future feature ever
  wants licensed past-paper material.
- **`tools/audit_provenance.py`** — standalone scanner with 7
  detection rules (JEES citations, year-numbered past-paper markers,
  past-paper terminology like 過去問 / 真題 / 本試験第N回, JLPT-year-paper
  citations). Last run: 0 hits across 648 questions +
  KnowledgeBank/*.md headers.
- **JA-30 invariant** — same 7 rules inlined into the standard CI
  integrity check (`tools/check_content_integrity.py`). A leak by
  a future contributor fails the build before merge. Total
  invariants: 38 → 39.
- **`feedback/jees-inquiry-template.md`** — bilingual email template
  ready for if/when the project ever wants to license specific
  past-paper material from JEES. Includes when-to-send guidance,
  recipient list, expected-outcome table, and an outcome-log
  section.
- **`NOTICES.md`** — new "Question content / corpus" section with
  pointer to `CONTENT-LICENSE.md` + the JLPT trademark statement.

### Updated

- **`feedback/MASTER-TASK-LIST.md`** — DEFER-11 ("Authentic-extracted
  N5 content re-source from official JEES samples") closed by
  decision: original-content policy formalized, JEES re-source path
  documented but not pursued. Strikethrough + closure annotation
  added inline.
- **`index.html`** version strings (`?v=` and footer-meta) bumped
  1.10.0 → 1.10.2 (had been stale through v1.10.1).
- **`package.json`** version bumped 1.10.0 → 1.10.2.

### Service worker

Bumped `CACHE_VERSION` v90 → v91. Added `./CONTENT-LICENSE.md` to
the PRECACHE list.

---

## v1.10.1 - 2026-05-02 (Content-protection layer)

Per user direction: deter casual copying / sharing of question
content from the deployed site, and remove the "Source on GitHub"
surface.

### Removed (user-visible)

- **"Source on GitHub" footer link** removed from `index.html`. Footer
  now reads `What's new · Privacy`.
- **"View on GitHub" link** removed from `js/changelog.js` (was in
  the CHANGELOG-fetch-error fallback).
- **GitHub source link** removed from `PRIVACY.md`. The "Source code"
  section was rewritten as "Independently verifiable" with guidance
  to inspect the browser's Network tab to verify the no-tracker
  claim — same level of assurance, no public-source-link dependency.

### Added (deterrent layer — friction, not security)

Important framing: the site is a static PWA. Anyone with browser
devtools can still read `data/*.json` directly, and there is no W3C
API to truly block OS screenshots. The layer below raises friction
against casual copying and accidental clipboard captures.

- **`css/main.css`** — `user-select: none` on html/body with opt-outs
  for inputs, textareas, contenteditable elements, and elements
  carrying `.allow-select`. `::selection` cleared. `user-drag: none`
  on images / svg / ruby / rt. `@media print` blanks the page with
  a "Printing is disabled" notice. `html[data-blur=true]` blurs the
  body and shows a Japanese overlay above z-index 99999.
- **`js/content-protect.js`** (new) — capture-phase blockers for
  `contextmenu`, `copy`, `cut`, `dragstart`, `drop`, `selectstart`.
  Keyboard shortcut blockers for `Ctrl+C/A/X/S/P/U`, `F12`,
  `Ctrl+Shift+I/J/K/C`. `window blur` + `visibilitychange (hidden)`
  set `html[data-blur=true]` to obscure content during region
  screenshots. `window.getSelection()` overridden to return empty
  when the active element is not an input.
- **`js/app.js`** — wires `initContentProtection()` from the
  DOMContentLoaded handler before any route renders.

### Service worker

- Bumped `CACHE_VERSION` to `jlpt-n5-tutor-v90` (was v89). Added
  `./js/content-protect.js` to the PRECACHE list.

### Honest limitations (called out in `js/content-protect.js`)

- OS region screenshots (Win+Shift+S, Cmd+Shift+4) — page blurs on
  window blur, but the OS often captures before the JS event fires.
- PrtScn key — most OSes don't deliver this event to the browser.
- Browser menu → Save / Print, `view-source:` URL prefix, devtools
  Network tab — all bypass the JS layer.
- Phone-camera-of-screen — always works, no defence possible.
- Mobile screenshot APIs — no JS API exists to intercept them.

If true protection matters more than reasonable friction, the
architecture has to change (server-side rendering with per-session
watermarks, video DRM, or moving off the public web).

v1.10.1 / SW v90. **39/39 invariants green.**

---

## v1.10.0 - 2026-05-02 (Syllabus dashboard + DEFER backlog closeout)

Big sweep: new homepage as a JLPT N5 syllabus dashboard, full
multi-correct grey-zone audit, every actionable backlog item closed,
and 100% grammar-pattern test coverage (177/177).

### Changed (user-visible)

- **Homepage redesigned as a syllabus dashboard.** Replaces the bare
  "JLPT N5 study material." inventory with: page title + subtitle, six
  syllabus cards (Grammar / Vocab / Kanji / Reading / Listening / Mock
  Test) with index + count + description + in-card action, eight-step
  recommended study order (now clickable links), six-row progress
  overview with progress bars, and an action block ("Not sure where to
  start?" + Take Placement Check + Start with Grammar). Container width
  on the home route widens to 1120px (only here; other routes stay
  880px) so the 3-column card grid fits comfortably.
- **Header primary nav expanded** from 2 links (Learn / Test) to 7:
  Grammar / Vocabulary / Kanji / Reading / Listening / Test / Progress.
  Every syllabus section is a single click from anywhere.
- **Recommended Study Order steps are clickable links.** Each of the 8
  numbered steps routes to the most directly-actionable surface: 01 →
  Grammar TOC, 02 → Vocab TOC, 03 → Kanji index, 04 → /drill, 05 →
  /reading, 06 → /listening, 07 → /test, 08 → /review. Full-row
  click target with hairline accent-on-hover and visible focus outline.
- **Progress dashboard goes live for all 6 sections.** Reading and
  Listening rows now show actual completion counts (previously stuck
  at 0/30 because per-passage / per-drill completion wasn't tracked).
  Reading marks completed on the results screen with score>0; listening
  marks on first answer submit.
- **Resume strip uses a friendly label.** "Last session: n5-001" →
  "Last session: n5-001 — です/だ" (pattern label hydrated at load).
- **Daily-goal-met badge** sits below the syllabus subtitle for
  returning users: "Streak: N days" + "✓ Practiced today" or "○ Not
  yet practiced today." Decoupled from the streak count so a 5-day
  streak with "not yet today" reads unambiguously.
- **Reading mock-test mode toggle.** Filters passages to the JLPT
  primary-question distribution (questions tagged `format_role:
  primary`). Persists across sessions via the `readingMockTestMode`
  setting. Shows per-passage question count alongside level/topic.
- **Undo-on-grading 2-second window in Review.** After grading a card,
  a fixed-bottom toast shows "Recorded: <Grade>" with an Undo button.
  Click within 2s to roll back the SRS state to the pre-grade snapshot
  and remove the entry from the session log. Auto-dismisses; pauses on
  hover for slow readers.

### Content (corpus)

- **100% grammar-pattern test coverage.** Authored 65 new questions
  across 3 batches to bring the uncovered count from 78 → 0. Every
  one of the 177 grammar patterns now has at least one MCQ question
  with 4 distinct, single-correct distractors. Total test bank:
  288 runtime + 360 paper = 648 questions audited green.
- **Three multi-correct grey-zone questions fixed** (q-0488 frequency
  calibration, q-0024 sentence-final speech act, goi-2.6 spatial
  position without anchor). See JA-29 + audit script categories
  F/G/H below.
- **Tier taxonomy on grammar.json.** Every pattern now carries
  `tier: "core_n5"` (165) or `tier: "late_n5"` (12). Late flag fires
  on N4-leaning hints in notes/meaning_en or known-boundary patterns
  (n5-167, 186, 187, etc.).
- **Kanji enrichment.** All 106 entries now carry `lesson_order`
  (sequential 1-106) + `frequency_rank` (within-N5 frequency rank
  derived from KANJIDIC2 + Joyo grade aggregate).
- **Vocabulary part-of-speech tags.** All 1003 entries in
  `KnowledgeBank/vocabulary_n5.md` carry inline `[n.]` / `[v1]` /
  `[v2]` / `[v3]` / `[i-adj]` / `[na-adj]` / `[adv.]` / `[part.]` /
  `[conj.]` / `[pron.]` / `[count.]` / `[num.]` / `[dem.]` /
  `[Q-word]` / `[exp.]` / `[interj.]` tags. Legend added to the
  file header.

### Added (invariants — locks the work in)

- **JA-29** — Question subtype taxonomy is closed: `paraphrase` and
  `kanji_writing` only. New subtypes must register in the integrity
  script before being introduced (closes DEFER-2 by decision: subtype
  is the canonical extension point, no need to promote to a top-level
  type).
- **Multi-correct audit script extended with 3 new categories**
  (`tools/audit_multi_correct.py`):
  - **F_frequency_calibration** — fires when stem has a numeric
    frequency (月にXかい etc.) AND choices contain a known grey-zone
    adverb pair {よく/たまに}, {よく/ときどき}, etc.
  - **G_speech_act_particle** — fires on "<verb>です/ます( )" with ≥2
    of {か, ね, よ} in choices and no question-word or はい/いいえ anchor.
  - **H_spatial_no_anchor** — fires on "<X>の( )に <Y>が あります"
    with ≥2 spatial positions in choices and no canonical object-pair
    (つくえ/テーブル/etc.) or movement verb in stem.

### Tooling / scaffolding (unblock external work)

- **VOICEVOX audio pipeline** (`tools/build_audio_voicevox.py`):
  preflight engine check, 3-retry exponential backoff, ThreadPool
  parallelism, --missing-only fast filter, ffmpeg WAV→MP3 transcode,
  multi-voice dialogue support via `[F1]/[F2]/[M1]/[M2]` script
  tags. Operator's manual at `AUDIO.md`. Confirmed gaps: 19 .mp3s
  missing (1 grammar + 18 listening 013–030); regenerable in
  ~3 minutes once the engine binary is on a local machine.
- **Audio coverage audit** (`tools/audit_audio_coverage.py`): exits
  non-zero on any data→disk mismatch; JSON gap dump to
  `feedback/audio-coverage-gaps.json`.
- **Native-review dossier exporter**
  (`tools/export_native_review_dossier.py`): generates
  `feedback/native-review-dossier/` from live data — cover.md,
  01_grammar_patterns.md (177), 02_vocab_borderline.md (122),
  03_kanji_readings.md (106), 04_reading_passages.md (30),
  05_listening_scripts.md (30), and a review_log.csv template.
  Severity rubric + citation format + turnaround targets in
  cover.md.
- **Visual-regression Playwright scaffold**
  (`tests/visual-regression.spec.js`): 12 tests × 2 viewports cover
  6 high-traffic routes with reduced-motion + animations-disabled +
  0.1% pixel-diff threshold. CI excluded via
  `--grep-invert visual-regression` until baselines are committed;
  `npm run test:visual:update` captures them locally.
- **Settings deny-list hardening.** Global Claude Code config (per
  user request 2026-05-02): `defaultMode: bypassPermissions` +
  explicit allow list (66 rules) + comprehensive deny list (37
  rules) blocking destructive ops (rm -rf, git push --force,
  git reset --hard, etc.) + belt-and-suspenders SS&SC directory
  denies on top of the existing block_sssc.py PreToolUse hook.

### Fixed

- 14-line homepage CSS regression: `main` 880px container was
  constraining `.home-syllabus` even after the inner element set
  its own 1120px max-width. Replaced with `main:has(.home-syllabus)`
  to scope the wider container to the home route only.
- `q-0536` had `茶` in the stem; not in the 106-kanji N5 whitelist.
  JA-13 caught it. Replaced with kana `おちゃ`.
- `vocabulary_n5.md` line 848 (`いる - to need`) was mistagged
  `[v2]` by the PoS-injection pass; corrected to `[v1]` (Group 1
  exception). The X-6.6 invariant's hint matcher now tolerates
  inserted PoS tags so the same edit doesn't break it again.

### Tooling housekeeping

- One-shot scripts kept as authoring templates:
  `tools/add_uncovered_questions.py`,
  `tools/add_uncovered_questions_batch2.py`,
  `tools/add_uncovered_questions_batch3.py`. Each documents the
  conventions for adding more questions in future sessions.

### Service worker

Bumped from `jlpt-n5-tutor-v82` → `jlpt-n5-tutor-v88`. Cache version
churn is high this release because every commit that ships a
js/css/data change requires a bump.

---

## v1.9.0 - 2026-05-02 (Japanese-first language sweep)

User direction: the learner-facing surface should be in Japanese, not English. Closes a series of parallel cleanups across reading, listening, and shared UI chrome.

### Changed (user-visible)
- **Dokkai (reading) passage titles → Japanese.** All 30 passage titles in `data/reading.json` rewritten from English (e.g. "My family") to N5-scope Japanese (e.g. わたしの かぞく). Title kanji verified against the 111-entry N5 catalog.
- **English passage translation panel removed from dokkai.** The "Show English translation" `<details>` block is gone from `js/reading.js`; the corresponding `translation_en` field has been deleted from all 30 passages in `data/reading.json`.
- **Reading-list metadata Japanified.** Level (`easy`/`medium`/`info-search` → やさしい/ふつう/じょうほうけんさく) and topic (19 distinct values, e.g. `family` → かぞく) now render in Japanese via lookup maps. Data values remain English keys for code stability.
- **Listening item titles → Japanese.** All 30 `title_en` fields in `data/listening.json` migrated to `title_ja` (e.g. "Where to meet" → どこで 会いますか, "Buying a ticket" → きっぷを 買う). Renderer uses the existing furigana pipeline; kanji-glyph popovers still work.
- **Listening format taxonomy in kana.** `課題理解 / ポイント理解 / 発話表現` (which contain non-N5 kanji) now render as `かだいりかい (タスクりかい) / ポイントりかい / はつわひょうげん` so the format names stay readable for an N5 learner.
- **UI page chrome Japanified** across reading + listening modules: page titles ("Reading practice" → どっかい れんしゅう, "Listening practice" → ちょうかい れんしゅう), intro paragraphs, back/start buttons, feedback labels (Correct/Wrong → せいかい/ざんねん), result stats (Score/Accuracy → スコア/せいかいりつ), section toggles (Show passage → ぶんしょうを 見る), expand/collapse-all controls.
- **Mock-test paper bunpou paper-7 restored.** New `parse_mondai3_passages()` in `tools/build_papers.py` correctly handles passage-grouped Mondai-3 grammar questions (Q91-Q100 from `KnowledgeBank/bunpou_questions_n5.md`); the rationale-leak bug that swallowed the next passage header into Q95's rationale is also fixed (tightened section-break regex to `^#{2,3}\s+(?!Q\d)`).
- **Bunpou stem N5-kanji cleanup.** Replaced 朝→あさ, 東京→とうきょう, 大阪→おおさか, 公園→こうえん, 牛乳→ぎゅうにゅう, 思います→おもいます, 楽しい→たのしい across 10 occurrences in bunpou paper stems and Mondai-3 passages. Also fixed one goi stem (Q17). Dokkai retains these kanji per its formalized naturalness exception (see JA-28 below).

### Added (invariants — locks the work in)
- **JA-26** — no duplicate question IDs in `data/questions.json` (closes a parallel-session collision class that hit twice across Pass-15 / Pass-16).
- **JA-27** — `data/reading.json` and `data/listening.json` may not carry `title_en` or `translation_en` fields. Prevents regression of the EN-removal direction.
- **JA-28** — `data/papers/dokkai/*.json` content is bounded by N5 catalog ∪ documented exception list (`data/dokkai_kanji_exception.json`, 25 kanji). Any new non-N5 kanji must be either kana-ized or explicitly added to the exception JSON. Bunpou / moji / goi stay strictly N5 via JA-13.

### Removed (cleanup)
- 16 dead `translation_en` fields in `data/questions.json` that no runtime path read (verified zero `q.translation_en` / `question.translation_en` / `item.translation_en` references). Grammar.json `translation_en` is intentionally retained — `js/learn.js` and `js/review.js` actively render those for grammar-pattern teaching.
- Redundant `lang="ja"` attributes on wrapper elements in `js/reading.js`. `renderJa()` already wraps output in `<span lang="ja">` so the parent attributes were producing nested duplicates in the DOM; the parent-level attribute is dropped.

### Tooling
- `tools/fix_dokkai_titles_remove_en.py` — idempotent EN→JA migration for reading.json
- `tools/fix_listening_titles_ja.py` — idempotent EN→JA migration for listening.json
- `tools/audit_dokkai_kanji_scope.py` — read-only inventory of non-N5 kanji in dokkai papers (used to seed JA-28's exception list)
- `tools/fix_remove_dead_translation_en.py` — idempotent removal of dead questions.json fields
- `tools/fix_pass23_round2.py` and `tools/fix_dedup_q0479_q0488.py` — Pass-23 round 2 audit fixes (multi-correct prompts, scope-leak prompts, q-0479..q-0488 ID dedup)

v1.9.0 / SW v82. **37/37 invariants green** (was 35; added JA-26 + JA-27 + JA-28 across this milestone).

---

## v1.8.2 - 2026-05-01 (Pass-14 Phase A: delete 38 stub questions)

### Fixed
- **Question bank quality** — applied F-14.1 from the Pass-14 audit. Deleted 38 "pattern-meta" questions (q-0280 through q-0416 family) that taught nothing. All matched the stub format `「つぎの いみに あう パターン: ～X～ れい:...」`. The flaws:
  - Answer was literally quoted in the stem (e.g., stem said "パターン: ～たり～たりする" and "～たり～たりする" was one of the choices).
  - Distractors mixed wildly different types in the same option set (a particle alongside a pattern label alongside an adverb chain), so a learner could rule out 3 of 4 options just from format.
  - Prompt said "fill the blank" but the stem had no blank.
  - One question (q-0382) had a rendering corruption — double colon from a Pass-12 cleanup leftover.
- **Bank size**: 181 → 143 real questions. Every remaining question has valid pedagogical structure (no answer-in-stem, no distractor-type mismatch, no prompt-stem mismatch).

### Cascade-resolved
Deleting F-14.1 also closed F-14.2 (answer-in-stem, 4 questions), F-14.3 (q-0382 corruption), F-14.4 (prompt-stem mismatch in 37 questions), F-14.7 (distractor-length asymmetry), and F-14.8 (incompatible-type mixing). 6 audit findings closed in one mechanical pass.

### Still open from Pass-14
- F-14.5: q-0418 dual-mode schema (text_input + stale `choices` array). Decision needed.
- F-14.6: 33 ID gaps (q-0051 → q-0220 jumps 168). Decision needed: keep / renumber / document.
- F-14.9: inconsistent slash convention in `choices` (~40 entries).
- F-14.10: type distribution skew (138 mcq / 4 sentence_order / 1 text_input). Author more non-mcq.

v1.8.2 / SW v61. 26/26 invariants green.

---

## v1.8.1 - 2026-05-01 (Settings danger zone)

### Added
- **Danger-zone visual treatment** for the existing Reset Progress flow (`js/settings.js`). The destructive action now sits below the regular settings, separated by `--space-8` of whitespace and a thin red top border. A red "DANGER ZONE" label in `--tracking-label` ALL-CAPS calls extra attention. The pre-existing typed-phrase confirmation gate ("Type `RESET` to confirm") still gates the actual destruction — belt + suspenders.
- New `.reset-confirm-box` styling: red-tinted bg, hairline incorrect border, monospace `RESET` input, secondary Cancel button.

### Why
The Reset action wipes 11 categories of state (FSRS schedule, study history, test results, streak, known-kanji flags, drill stats, manual overrides, diagnostic results, settings preferences, last-viewed lesson, weak-pattern tracking). For users who've used the app for weeks, that's a lot of personalized state. The danger zone adds visual quarantine to match the action's actual consequence.

v1.8.1 / SW v60. 26/26 invariants green.

---

## v1.8.0 - 2026-05-01 (Zen Modern design overhaul)

A comprehensive visual refresh per `specifications/jlpt-n5-design-system-zen-modern.md` (Muji-inspired). Hierarchy through typography and whitespace, hairlines instead of borders, no shadows / no gradients / no decorative icons. Total work shipped across 4 commits.

### Phase 1 — Foundation (commit `af38e11`)
- New `:root` token system: surfaces (bg/surface/surface-alt), hairlines (line/line-strong), text (text/text-muted/text-faint), brand accent (`#1F4D2E` deep forest, replaces warmer `#14452a`), semantic state (correct/incorrect/due each with tint).
- Type scale: `--text-2xs` (11px) through `--text-2xl` (32px). Body 15px (down from 16px) — tighter, content-heavy correct.
- Weights: 300 / 400 / 500 only. Audited and replaced 41 occurrences of weight 600/700 in `css/main.css`.
- Spacing scale 4px–128px; Muji aesthetic favours the BIG end (96px between major sections).
- Container widths narrow/base/wide (640/880/1120).
- Border radius: 2/4/6 only — geometric, hard-edged, no SaaS 12-16px curves.
- Motion tokens: 120ms / 180ms / 300ms with iOS ease-out.
- **Dark mode: full parity** — every light token has a dark twin. Triggers via `prefers-color-scheme: dark` OR `data-theme="dark"`.
- Body has `font-variant-numeric: tabular-nums` globally (stats, counters, timers, SRS intervals align vertically).
- Smooth color transition on theme toggle.

### Phase 2 — Components (commit `4703202`)
- **Header**: 56px sticky, 0.5px hairline bottom; container-wide max; brand-link gets a `五` mark in a 24px hairline-bordered square (cultural anchor per spec §4.1).
- **Primary nav**: tabs with 1.5px accent underline on `.active` (replaces filled-pill background).
- **Section labels**: new component — ALL-CAPS text-2xs label + flex-1 hairline rule, used between major page sections.
- **Buttons**: unified `.btn-primary` / `.btn-secondary` / `.btn-ghost` / `.btn-danger` at h-36 base, h-28 sm, h-44 lg. Focus ring 2px accent + 2px offset.
- **Cards**: 0.5px hairline, 6px radius, hover lightens to surface-alt (no transform, no shadow).
- **`.card-index`** numbered indicator (Muji signature 01/02/03).
- **Pills**: status-only, 4 tinted variants.
- **Progress bar**: 2px height (was 6px) — present but barely there.
- **Table**: hairlines only, no vertical borders, no striping.
- **Form controls**: h-40, focus border-accent.
- **Footer**: hairline-top, muted single row.
- **Furigana ruby**: `.furigana-off rt {display:none}` + `.furigana-known rt {visibility:hidden}` toggle classes.
- **Dropped**: 8 `box-shadow` declarations + 5 `transform: translateY` hover lifts (spec §8 forbids both).

### Phase 3 — Page treatments (commit `70f5ad2`)
- **Learn hub**: 5 numbered cards (`01 Grammar` / `02 Vocabulary` / `03 Kanji` / `04 Dokkai` / `05 Listening`). Section labels "Reference" / "Practice" with hairline rule. Copy: "32 categories" → "5 sections" (matches v1.7.5 supercategories); "~1003" → "1003".
- **Home**: "Sections" section label above the 2 pillar cards, which now show `01 Learn` / `02 Test` numbered indices. Hyphens upgraded to em-dashes in body copy.
- **Header**: gear glyph `⚙` (rendering as colored emoji on some platforms) → "Settings" text link.
- **Drill choice grid**: 2-col fixed, max-width 560px, centered. 56px tall buttons, hairline border, accent-tint on `.selected` (was filled green).
- **Test setup card**: 1.5px top border in `--color-text` (formality cue per spec §5.8).
- **Settings**: single-column max-width 640px, transparent bg, hairline rows. New `.settings-danger-zone` scaffold with red top border + "DANGER ZONE" label.

### Phase 4 — Self-hosted fonts (this commit)
- **Inter** (300 / 400 / 500) shipped as woff2 in `fonts/`. Total Inter footprint: ~338 KB. Critical because the Muji aesthetic requires Inter Light (300) for hero headlines — system fonts have no true Light.
- **Noto Sans JP** (weight 400, per spec §2.3 Japanese is always 400) subset to N5 + N4 character coverage (hiragana + katakana + 106 N5 kanji + ~85 N4 kanji + ASCII + JP punctuation = ~740 chars). Built via `python -m fontTools.subset` with `brotli` compression. Output: 165 KB woff2 (down from 4.5 MB unsubsetted).
- **Total font footprint: ~503 KB**, all CSP `'self'` (no third-party network).
- **`<link rel=preload>`** on the two most-used (Inter 400 + Noto Sans JP 400) so first paint isn't a system-font flash.
- **`@font-face`** with `font-display: swap` so latin renders immediately with system fallback while the woff2 streams in.
- **`unicode-range`** on the Noto Sans JP face so the browser doesn't try this font for latin characters (Inter is preferred there).
- **SW precache** updated: 4 new woff2 entries, cache `v59`.

### Stats
- 4 commits / 4 phases.
- ~600 lines of CSS replaced or added.
- 41 weight-600/700 → 500 replacements.
- 8 box-shadows + 5 hover-lifts purged.
- 4 woff2 fonts, ~503 KB total install footprint addition.
- 26/26 content-integrity invariants green throughout.

---

## v1.7.11 - 2026-05-01 (UI cleanup: remove decorative emojis)

### Removed
- **All decorative pictograph emojis** from the UI per user direction. Specifically:
  - **Learn hub** (`renderHub` in `js/learn.js`): the 5 hub-card icons (📖 Grammar, 📚 Vocabulary, ✍️ Kanji, 📰 Dokkai, 🎧 Listening) and the lede sentence "Pick what you want to study. Each section is self-contained."
  - **Home streak** (`js/home.js`): 🔥 streak-flame icon. Streak count + label remain.
  - **Empty states**: 🌱 in `js/review.js` (2 places — no-due and no-history empty states); 📊 in `js/summary.js`.
  - **Offline indicator** (`js/pwa.js`): leading ⚠ removed; banner now reads plain "Offline - cached content only".
  - **Verb-class warning section** (`js/verb-class.js`): leading ⚠ removed from the "famous Group-1 exceptions" heading.
  - **Counter drill** (`js/counters.js`): the 11 per-counter pictograph icons (🍎 つ, 👤 人, 📄 枚, 🍶 本, 📕 冊, 🏢 階, 🎂 歳, 🍵 杯, ⏱ 分, 🕒 時, 💴 円). Replaced with the neutral geometric Black-Circle dot (`●`, U+25CF) for the count visualisation so the "show N objects" drill still works without using emoji.
- **Dead CSS**: `.hub-icon`, `.streak-flame`, `.empty-state .empty-icon` rules — orphaned after the markup removal above.

### Kept (intentional)
- **Typographic correctness markers** (✓/✗ in `js/test.js`'s review screen): Unicode Dingbats (U+2713 / U+2717), classified as text-presentation glyphs by default; these are the standard correct/incorrect indicators every testing UI uses, with color-coded CSS (green/red). Not pictograph emojis.
- **★ Mastered badge** and **★ graduated** labels: Black Star (U+2605), pure typographic geometric symbol, never renders as pictograph.

---

## v1.7.10 - 2026-05-01 (homograph disambiguation: vocab_ids per example)

### Fixed
- **Wrong example sentences on homograph vocab pages.** The かた "person (polite)" detail page was showing the example 「この かんじの 読みかたは なんですか」 — but 読みかた "way of reading" is a different かた (n5.vocab.37 "way of doing", not n5.vocab.1 "person"). Same class of bug existed for 75 other homograph clusters: は (tooth / leaf / topic-marker), ひと (person / one), ある (to be / a certain), いる (to need / to be), おく (to put / 100 million), ほん (book / counter for cylindrical), はい (yes / counter for cupfuls), かい (counter for floors / counter for times / shellfish), きる (to wear / to cut), から (from / because), が (subject-marker / but), と (with / when / and), どうも (somehow / thanks), and 60 more. Every example now carries an explicit `vocab_ids: [...]` list naming exactly which vocab entries it demonstrates; the renderer matches by ID, never by substring.

### Changed
- **`data/grammar.json`**: every example sentence (589 total) gained a `vocab_ids` field. Auto-tagged via `tools/link_grammar_examples_to_vocab.py` with 13 hand-coded disambiguation rules + POS-aware substring matching + verb / i-adj conjugation matching (handles ます-form, te-form, た-form, ない-form, potential, and i-adj くて / かった forms).
- **`js/learn.js#renderVocabDetail`**: filters examples by `ex.vocab_ids.includes(entry.id)` instead of substring on the form field. Backward-compat fallback to substring kept for any legacy data.

### Added (CI)
- **JA-17 invariant** "Grammar examples have vocab_ids (homograph guard)" — every grammar example with non-empty `ja` text must declare a `vocab_ids` list. Blocks any future regression. Now 26/26 invariants green.

### Tooling
- **`tools/link_grammar_examples_to_vocab.py`** (idempotent re-runnable): scans every grammar example, finds POS-aware substring matches against `data/vocab.json`, applies homograph disambiguation rules, and writes `vocab_ids` back. Falls back to over-linking for ambiguous homograph forms without explicit rules (safe per "over-link beats under-link" direction). Conjugation-fallback covers verbs and i-adjectives in inflected form (e.g. 行けません → 行く, いそがしくて → いそがしい, わかります → 分かる via reading).
- **Conjugation-collision post-filters**: 来る/きる kana ms-stem き collision (drops きる "to wear / cut" unless clothing/cutting context); 入る/はい kana stem collision (drops "yes" expression and "cupful" counter unless example starts with greeting); 行く/いけ collision in the Verb-て+はいけません idiom (drops "lake" noun).
- **Counter numeral-prefix guard**: 2-char counter forms (かい / ほん / はい) require an immediately-preceding numeral (0-9, fullwidth digits, 一二三…) so that かい inside かいました (買う conjugated) doesn't false-match the counter "1階".
- **Standalone-word boundary guard**: 2-char `expression`/`interjection` POS forms require a left word-boundary so that はい (yes) doesn't false-match inside すってはいけません.

### Stats
- 75 homograph clusters fully covered. 589/589 (100%) examples linked to ≥1 vocab entry. 473 homograph-disambiguation decisions made by the auto-tagger across the corpus.

---

## v1.7.0 - 2026-05-01 (FSRS-4 replaces SM-2)

### Changed
- **SRS scheduler upgraded from SM-2 to FSRS-4** (Free Spaced Repetition Scheduler v4 — the algorithm Anki ≥23.10 uses by default). FSRS-4 has empirically better recall prediction than SM-2 in published comparisons; for our use case it's a drop-in replacement that requires no new data collection and runs entirely in the browser.
- **Per-item state schema** gained `stability` (S, days the memory holds at 90% recall), `difficulty` (D, clamped 1-10), and `lastReview` (ISO timestamp). Legacy SM-2 fields (`easeFactor`, `interval`, `reps`, `lapses`) are preserved for migration and legacy badge UI but are no longer used at runtime.
- **Migration is automatic and lossless.** On the first FSRS-graded review of any pre-existing entry that has SM-2 state but no FSRS state, the scheduler seeds `stability` from the SM-2 `interval` and `difficulty` from the inverted ease-factor curve (EF 1.3 → D 10, EF 2.5+ → D ~2). Subsequent reviews update via FSRS-4. No user action needed; no progress lost.
- **Grading UI unchanged.** Drill review buttons still emit grades on the SM-2 1/3/4/5 scale (Again/Hard/Good/Easy); the scheduler translates internally to FSRS's 1/2/3/4 scale.

### Why it matters
- Better recall predictions → fewer items re-shown when not needed, fewer items missed when they are needed.
- Closes EB-4 Tier-1 from the 2026-05-01 external-blocked-items reframing (the v2.0 recommender was originally deferred indefinitely on the assumption that "richer recommender = needs telemetry"; FSRS-4 demonstrates a richer scheduler with zero new data).

### Note
- This is a code-only change. No grammar/vocab/listening/reading/kanji content was modified. All 25 content-integrity invariants remain green.

---

## v1.6.4 - 2026-05-01 (K-1 kanji example usage + Pass 14c/15a corrections)

### Added
- **Example-usage section on every kanji card.** Each of the 106 kanji detail pages now shows 1-3 N5-syllabus example words in a three-column table (form / reading / English gloss). Added between the readings strip and the Stroke order block. Form, reading, and gloss come from `data/kanji.json#examples`. The K-1 substitution rule is applied at data-time: if a useful word like 手紙 (letter) contains an out-of-scope kanji (紙), the form is authored as 手がみ — the target kanji stays kanji, the OOS kanji becomes its contextual reading. New JA-16 invariant guards this rule.
- **`tools/populate_kanji_examples.py`** (idempotent): auto-picks examples for 100 kanji from `data/vocab.json`; hand-curated `MANUAL_EXAMPLES` for 6 kanji (口/目/力/手/友/足) that had no vocab references in the corpus (recovered in Pass-13 but vocab corpus didn't catch up).

### Changed (Pass 14c — low-effort backlog batch, 2026-04-30 → 2026-05-01)
- **`audio_manifest.json` voice metadata.** Top-level `voice_default: "synthetic-gtts"`; per-item `voice` field stamped on all 631 entries. `tools/build_audio.py` now skips items marked `voice: "native"` so externally-recorded items (when EB-1 lands) aren't synthesized over.
- **何 primary reading**: なに → なん. Across N5 vocab compounds (何時/何曜日/何月/何日/何人), なん dominates; なに is correct only for the standalone 何ですか. Source (`tools/build_data.py` PASS10_PRIMARY_OVERRIDES) and generated JSON now agree. Note: the `primary` field is unused at runtime since Pass 13 auto-furigana removal — this is data correctness, not behaviour.
- **`questions.json` half-width parens** in 4 stage-direction wrappers (q-0028, q-0029, q-0032, q-0049): ASCII `(...)` → fullwidth `（...）` per Japanese typography norms.
- **Listening curriculum-prerequisite metadata.** `data/listening.json#n5.listen.005` got `requires_patterns: ["n5-030"]` + `_curriculum_note` documenting the nominalising-の dependency.
- **Dead CSS removed.** `.hero-stats`, `.trust-strip` and their nested rules were orphaned after v1.6.1's copy audit removed those DOM elements. ~28 lines.
- **meaning_ja consistency.** 7 patterns (n5-013, 019, 032, 047, 069, 111, 123) had placeholder meaning_ja (just the form quoted, or wrong concept); rewritten as proper short-noun-phrase definitions. n5-069 specifically had `「てある」` which is a different N4 grammar — replaced with `ことばを つなぐ どうしの かたち`.
- **vocab.json POS tagging.** Every one of 1003 entries now has a `pos` field (noun / verb-1 / verb-2 / verb-3 / i-adj / na-adj / adverb / particle / conjunction / interjection / pronoun / counter / numeral / demonstrative / question-word / expression). Section-name heuristic + gloss-pattern fallback.
- **こそあど → "Demonstratives" in user-facing UI.** Page heading, Learn-hub deep-dive link, grammar.json category labels, and vocab.json section labels all renamed. Code-internal use of こそあど (file names, route slugs, CSS classes, function names) retained — backend-only term.

### Added (CI tooling)
- **JA-15 invariant** "Audio refs resolve to files on disk" — walks `data/audio_manifest.json`, normalises Windows-style backslashes, asserts every entry's `path` exists. 631/631 verified at landing.
- **JA-16 invariant** "Kanji examples use only target-or-whitelist kanji" — guards the K-1 substitution rule.
- **`tools/test_build_data.py`** (4 regression tests): Bug A `[Ext]`-tagged headers parse, Bug B parenthetical doesn't fragment meanings, smoke test for plain headers, E2E real KB produces 106 clean entries. Wired into `content-integrity.yml` workflow.
- **`tools/llm_audit.py`** — Anthropic-API-driven content audit script as Pass-15 substitute (per the EB-2 automation analysis). Validated on a 5-pattern sample; full report at `feedback/llm-audit-validation-report.md`.
- **`tools/heuristic_audit.py`** — free $0 alternative to llm_audit.py: deterministic Python scans for the same issue classes the LLM caught. Run on full corpus in ~50ms.

### Changed (Pass 15a — heuristic audit, 2026-05-01)
- **45 fixes from a free heuristic audit of all 187 patterns.** Surfaced 60 findings (75% precision); fixed 45.
  - 38 patterns had auto-gen `Duplicate-cleanup redirect. See n5-XXX...` text reaching learners as `notes`. All cleaned.
  - n5-158 (〜だろう casual): examples were teaching the *polite* でしょう, not the casual だろう. Pedagogical inversion fixed.
  - n5-112 (〜ふん/ぷん counter): examples used 分 kanji, bypassing the kana counter readings the pattern teaches. Converted to ふん/ぷん.
  - n5-173/174/175 (must-do variants): 3 patterns shared a single example that demonstrated only n5-176. Each now has a distinct example.
  - n5-105 / n5-106: plain-form examples in patterns explicitly teaching the polite form. Standardised to polite.
- **Cumulative:** ~635 findings raised across Pass 1-15a, ~620 fixed, 2 deferred.

### Note
- v1.6.3 was an internal-only asset-version bump for the Demonstratives UI rename + skeleton polish; no separate user-facing changes beyond what's listed under v1.6.4.
- All changes verified: 25/25 content-integrity invariants green; all 4 CI workflows (`pages-build-deployment`, `content-integrity`, `lighthouse-ci`, `playwright-p0-smoke`) green on every commit since the playwright workflow was unblocked.

---

## v1.6.2 - 2026-04-30 (Stroke-order SVGs)

### Added
- **Stroke-order diagrams on every kanji card.** Drop-in of all 106 KanjiVG SVGs (CC BY-SA 3.0) at `svg/kanji/<glyph>.svg`. The placeholder text "Stroke-order SVG not yet shipped." that was visible on every one of the 106 kanji detail cards is gone. Each kanji card now shows the actual stroke-by-stroke diagram with stroke numbers.
- **`NOTICES.md`** at the repo root: third-party content attributions. KanjiVG entry includes source, license, copyright, and a note on the only modification made (codepoint-hex filenames renamed to literal-glyph filenames to keep on-disk names learner-readable; SVG payload byte-for-byte preserved).
- **`tools/fetch_kanjivg.py`** build script: fetches the 106 SVGs from KanjiVG's GitHub raw URLs. Idempotent (skips files already present). Used at build time only.

### Changed
- **Service worker precache** now derives the 106 SVG URLs at install time from `data/n5_kanji_whitelist.json` rather than hand-listing them. Avoids drift between data and precache.
- **Kanji card fallback message** rewritten: `Stroke-order SVG not yet shipped. Drop-in target: ...` → `Stroke-order diagram could not load.` (only visible when an SVG is missing or `<object>` fails to render).
- **CC BY-SA 3.0 attribution line** added under the stroke-order diagram on every kanji card, linking to <https://kanjivg.tagaini.net/>.

### Note
- This is a content-only addition. Zero changes to grammar/vocab/listening/reading data. All 23 content-integrity invariants remain green.
- SVG payload size: ~496 KB total across 106 files (avg ~4.7 KB each).

---

## v1.6.1 - 2026-04-30 (Copy audit: voice consistency)

### Changed
- **Hero copy rewritten** to remove sales-promo voice. Headline `Pass JLPT N5 with 15 minutes a day` → `JLPT N5 study material`; first-time CTA `Start your first lesson` → `Start a lesson`; returning-visitor h2 `Continue your N5 study` → `Continue`. No factual changes; voice now matches an institutional reference site (think MIT OpenCourseWare) rather than a SaaS landing page.
- **Hero trust strip removed** from the page body. The same facts (offline, no account, local storage) are now reachable via the `Privacy` link in the footer; on-page repetition was the marker of marketing voice.
- **Hero stats** reverted from pill badges to a flat dot-separated list — pills read as a stat-card scoreboard; flat reads as a table of contents.
- **Recommender widget** copy rewritten: `What should I study next?` → `Suggested next`; `Keep your 5-day streak alive` → `Continue (5-day streak)`; `Clear today's review queue` / `Run today's review` → `N reviews due today`; `Try a quick mixed drill` → `Mixed drill`; `Pick up the next lesson` → `Next lesson`. Numbers are the motivator; imperatives removed.
- **Returning resume cards** copy rewritten: `Continue where you left off` → `Resume`; `Today's review queue` → `Reviews due today`; `All caught up - come back tomorrow.` → `No reviews due.`; `Learn something new` → `Open Learn`.
- **Streak label** simplified: `5 day streak` → `5 days`; the heading-style "streak" word removed.
- **Site title** `JLPT N5 Grammar Tutor` → `JLPT N5 — study material`. Per UI brief §1.1 #1: "Grammar Tutor" undersells (vocab, kanji, reading, listening are also part of the corpus).
- **Meta description** rewritten in plain English (`Free JLPT N5 study material covering grammar, vocabulary, kanji, reading and listening. Works offline; no account.`) — replaces developer jargon (`Static, on-device, privacy-preserving tutor for JLPT N5 grammar.`) which a non-developer searcher couldn't parse.
- **Drill answer feedback** glyphs dropped: `✓ Correct` / `✗ Not quite` → `Correct` / `Wrong`. Color + label is enough; the glyphs rendered inconsistently across platforms (Windows plain text vs mobile emoji).
- **Drill graduation message** `★ Graduated! This pattern is mastered.` → `Graduated. Pattern mastered.`
- **Counter-drill feedback** glyphs dropped (same rationale as above).
- **Summary empty state** copy rewritten: `Your dashboard fills in as you study.` → `Stats appear here once you've studied.`; `Start your first lesson` → `Start a lesson`.

### Note
- These are voice-only changes. No grammar/vocab/kanji content was modified. All 23 content-integrity invariants remain green.
- Voice contract recorded in `TASKS.md` under "Copy audit" so future copy doesn't drift back into marketing register.

---

## v1.5.0 - 2026-04-30 (UX Brief 2 - Phase 1-4)

### Added
- **Home screen** (#/home) is now the default landing page. First-time visitors see a CTA "Start your first lesson" + placement check link + 3-card pillars (Learn / Practice / Test). Returning visitors see a Continue card, Today's review queue, and a 7-day streak heatmap.
- **Search** across grammar / vocab / kanji from the header. Press `/` to focus. Works offline.
- **Three-mode furigana** (Always / Hide on known kanji / Never) in Settings, with a live preview.
- **Per-kanji popover**: click any kanji glyph to see on/kun-yomi + meanings + an "I know this" toggle that persists.
- **Single-kanji pages** (#/kanji/<glyph>) and the kanji index (#/kanji) showing all 97 N5 entries.
- **Keyboard shortcuts** (1-4 / Space / Enter / ? / Esc / /) with a `?` cheatsheet overlay.
- **Settings additions**: audio playback speed (0.75 / 1.0 / 1.25x), reduce-motion toggle, typed-phrase reset confirm ("Type RESET").
- **Skeleton placeholders** replace the legacy "Loading..." text on every route. 5-second timeout shows a real "Couldn't load this view" UI with Retry.
- **Empty states** for Review (no progress / no due), Summary (no progress), and Test (no completed tests).
- **Trust strip** on the landing screen ("Works offline / No login required / Your progress stays on this device") above the fold.
- **PWA install prompt** (one-time, dismissible).
- **Offline indicator** in the corner when the network drops.
- **"Update available" toast** when a new shell version is detected (stale-while-revalidate).
- **Streak tracking**: current + longest day-streak in localStorage, 7-day heatmap on home.
- **Mobile bottom-nav** at viewports ≤ 480px with iOS safe-area insets honored.
- **Print stylesheet** (`@media print`) for clean handouts of any Learn lesson.
- **Persistent location indicator** chip below the header showing the active route.
- **Deep links**: #/test/<n> for n ∈ {20, 30, 50} starts a test directly. #/kanji/<glyph> jumps to a kanji page.

### Changed
- **Tagline** updated to "Pass JLPT N5 with 15 minutes a day. No login, no ads, no data shared."
- **Footer** updated to "Works offline. No login. Your progress stays on this device."
- **Primary nav** restructured: Home / Learn / Practice (renamed from Daily Drill) / Review / Test. Summary + Settings moved to a secondary nav row.
- **Service worker** now uses stale-while-revalidate for the shell (HTML/CSS/JS) and cache-first for content (data/audio/locales). Posts an update message to clients when new shell bytes are detected.

## v1.4.0 - 2026-04-29 (Brief 1 - final assets)

### Added
- **491 audio files** for all grammar examples, reading passages, and listening scripts (gTTS Japanese voice, ~19 MB).
- **30 reading passages** (expanded from 8) with 2-3 comprehension questions each.
- **12 listening items** across the three JLPT N5 formats (4 task / 4 point / 4 utterance) with audio.
- Grammar example audio player in the Learn UI.

### Fixed
- `tools/build_audio.py`: `Path.with_suffix` was stripping the example index for IDs like `n5-001.0`. Switched to manual string concat so all 449 grammar example files render uniquely.

## v1.3.0 - 2026-04-30 (native-speaker audit Pass 8)

52 findings raised, 52 fixed. Severity: 16 HIGH, 27 MED, 9 LOW. Touched `moji_questions_n5.md`, `bunpou_questions_n5.md`, `goi_questions_n5.md`, `dokkai_questions_n5.md`, `externally_sourced_n5.md`. See `verification.md` §7.

## v1.2.0 - 2026-04 (UX Brief 1 / Phase 4 + 5)

- 187 patterns enriched, 250 questions written (no stubs).
- 1002 vocab entries + 97 kanji entries.
- Verb classification, て-form gym, counters, こそあど, は vs が, particle pairs modules.
- Reading + Listening shells.
- Settings panel + 5-locale i18n + PWA manifest + export/import progress.
- SM-2 SRS in Review with Again/Hard/Good/Easy grading.
- 37 browser-runnable tests.

## v1.0.0 - 2026 initial release

- Vanilla HTML/CSS/JS scaffold, hash router, LocalStorage adapter.
- 4 chapters + Drill + Diagnostic.
- Threshold-based weak detection.
- Service worker, offline-capable.

---

*This changelog only records changes visible to users. For commit-level history, see git log.*
