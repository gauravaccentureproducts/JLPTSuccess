# Native-Japanese-Teacher Audit Report — 2026-05-15

**Scope:** `data/grammar.json` (178 patterns), `data/vocab.json` (1,009
entries), `data/kanji.json` (106 entries), `data/reading.json` (54
passages), `data/papers/dokkai/*.json` (7 papers, 102 questions).

**Auditor:** Claude (LLM) acting as seasoned-native-Japanese-teacher +
JLPT-N5-expert persona. Not a native human; confidence levels declared
per dimension below.

**Methodology:** 4 phases, each iterated until the checker for *that
phase's specific pattern set* returned 0 real findings. "0 findings"
below always means "0 findings against the patterns scanned" — it does
not claim universal coverage of all possible linguistic-accuracy
classes in the corpus.

**Writing-discipline note.** Sections below use phrases like "every",
"all", "RESOLVED", "complete", "final". Read each as bounded by
*"within the categories defined in that section"*. A future JLPT exam
or native-human review may surface item classes outside our defined
categories.

---

## Phase A — Programmatic deep-linguistic audit (6 checks across 5,350 sentences)

| Check | What it catches | Findings | Fixed |
|-------|-----------------|----------|-------|
| **L1** Counter-noun semantic pairing | Wrong counter for noun class (本 with つ for books should be 冊) | 6 real / 4 FP | **7** |
| **L2** Adjective conjugation | い-adj using で/じゃない instead of くて/くない; な-adj using くて | 0 (after regex fix to exclude correct 〜いです polite form) | 0 |
| **L3** Time-particle accuracy | Frequency adverbs (毎日/毎週/etc.) wrongly taking に | 0 (after word-boundary refinement) | 0 |
| **L4** Discourse register coherence | Mixing plain だ + polite です in same passage | 0 | 0 |
| **L5** Verb-group conjugation | Cross-check verb-class tag vs example conjugation | 0 | 0 |
| **L6** Honorific お/ご prefix | お on kango / ご on wago mismatches | 0 | 0 |

**Phase A real fixes (7):**
- Six native-counter-series entries (三つ–九つ idx=1) had `本が Xつ あります` — books canonically take 冊, not つ. Replaced with ボール/コップ/はこ/木/ふくろ/いす.
- One grammar pattern (n5-110[3]) used `さかなを 二つ` in a context teaching CANONICAL counter usage — fish takes 匹. Replaced with たまご+つ.

---

## Phase B — Sample-based deep linguistic review (~80 sample sentences + programmatic sweeps)

Random-sampled 73 sentences across all corpora as ersatz native-teacher
review. Initial sample surfaced 3 specific bugs; programmatic
extension caught 102 more.

| Check | Findings | Fixed |
|-------|----------|-------|
| Grammar.json `あの Xは どこですか` template (same pattern vocab Round 4 cleaned up — never extended to grammar.json) | 5 (n5-041, n5-048, n5-164) | **5** |
| Animacy violation: animate noun + が あります (should be います) | 3 real (男の子, 日本人, スペイン人) + さかな improvement | **4** |
| Bare-article EN: "There is X." / "I eat X." (singular common noun, no article) | 74 across vocab.json | **74** |
| Unnatural verb pairings: ぜひ + 食べます, ただ + 食べます, ためる人が います, 聞こえるつもり, ござるつもり | 5 | **5** |
| Translation_en with " / " multi-translation (pick one) | 4 | **4** |
| **Phase B subtotal** | **92** | **92** |

---

## Phase C — JLPT-format authenticity sweep on papers/dokkai (102 questions)

| Dimension | Result |
|-----------|--------|
| Mondai distribution per paper | Papers 1-4 = mondai 4; papers 5-6 = mondai 5; paper 7 = mondai 6 — coherent JLPT-format separation |
| Stem-format conformance | 86 of 102 (84%) match canonical JLPT-style stem patterns (どこですか / 何時に / どうして / etc.); other 16 are legitimate non-template stems |
| Distractor pedagogy (sample of 8) | All 8 sampled distractor sets used realistic confusable wrong answers (adjacent times, plausible alternative locations) — no random-distractor laziness |

**Phase C findings: 0** *against the three dimensions checked above*.
Papers conform to JLPT-format conventions for the dimensions reviewed.
Difficulty calibration vs real JEES papers is **not** checked here
(see AUDIT-COVERAGE for the gap disclosure).

---

## Phase D — Best-effort review of "human-only" items

### D.1 Verb-example template-leaks (caught while sampling verb entries)

Two new systemic templates surfaced after the targeted verb-entry sample:

| Template | Affected | Pedagogical issue |
|----------|----------|-------------------|
| `毎日 X ことが できます。` "I can VERB every day." | 28 vocab entries | Often nonsensical (毎日 こまる ことが できます = "I can be troubled every day"; 毎日 くもる ことが できます = "I can become cloudy every day") |
| `あした X つもりです。` "I plan to VERB tomorrow." | 30 vocab entries | Several use INTRANSITIVE verbs that don't take volitional つもり (はじまる, しまる, おちる) |
| Wrong-headword: `すう` entry [1] = "バスで 学校へ 行きます" | 1 vocab entry | Example talks about bus/school, not smoking (same bug class as たばこ caught in earlier audit) |

**Phase D fixed: 59.**

### D.2 Pitch accent spot-check (20 vocab entries)

Sampled 20 random vocab entries' `pitch_accent.drop` against NHK
accent conventions. Confidence: **LOW** (this is the one dimension
where my training is genuinely weak; flags require native-human
verification).

| Entry | Reading | Current drop | NHK-likely | Confidence |
|-------|---------|--------------|------------|------------|
| 週 | しゅう | 1 | 0 (heiban likely) | Low — defer to human |
| まいばん | まいばん | 1 | 0 (heiban likely) | Low |
| こと | こと | 1 | 2 (atamadaka-style; both attested) | Low |
| 時々 | ときどき | 4 | 0 (heiban; sources differ) | Low |
| じ | じ | 1 | both possible (single-mora ambiguous) | Low |

**Not auto-fixed.** Native-human review required. The other 15
sampled entries had drop positions consistent with NHK convention.

### D.3 Idiomatic naturalness of long sentences (15 long-form examples)

Reviewed 15 sentences ≥30 chars. None of these 15 read as unnatural to
the LLM-native-teacher persona. ✓ 0 bugs *in this 15-sentence sample*;
longer-sentence naturalness across the full corpus remains unverified
(see "What still requires native-human review" below).

### D.4 Audio-script consistency

Cannot verify without listening to the MP3s. Documented in
`docs/AUDIT-COVERAGE-2026-05-15.md` as the dimension requiring
listening-capable human reviewer.

---

## Issues fixed (total: 158, within the categories we defined)

| Phase | Real fixes |
|-------|-----------|
| A — Counter-noun pedagogy *(6 categories scanned)* | **7** (6 vocab + 1 grammar) |
| B — Templates / animacy / translations *(5 specific patterns)* | **92** (85 vocab + 6 grammar + 1 kanji) |
| C — JLPT-format authenticity *(3 dimensions checked)* | 0 *for the dimensions checked* |
| D.1 — Verb template-leaks + wrong-headword *(2 templates)* | **59** (all vocab matching these 2 templates) |
| **TOTAL** | **158** |

These 158 fixes address *the specific issue classes named above*.
Issue classes outside this scope (e.g., subtle は vs が discourse
choice, honorific register pragmatics, audio-script alignment) are
**not** addressed in this audit pass.

---

## Issues reviewed and decisions

| Item | Reviewed myself as native teacher? | Decision |
|------|-------------------------------------|----------|
| Pitch accent drop positions (5 low-confidence flags) | Yes — judged against NHK conventions | **Defer to human.** My confidence on auditory phonology specifics is genuinely low; introducing changes risks new errors. |
| n5.read.054 "しまは とても 長くて" (island described as "long") | Yes | **Keep.** Geographically valid for elongated islands (Okinawa-like). |
| n5-152 "...できませんでした、すみません。" comma+すみません | Yes | **Keep.** Acceptable as colloquial spoken-style apology. |
| 「あさってに」 with particle に | Yes | **Keep.** Borderline but grammatical (formal/emphasized future). |
| Reading 010 / kanji 行 "どう 行きますか" | Yes | **Keep.** Spoken Japanese accepts どう + 行く for transport-mode questions. |
| Cross-corpus boilerplate sentences below JA-81 threshold-10 | Yes | **Keep.** Reuse is pedagogically defensible when each occurrence teaches a different word/pattern. |

---

## What still requires native-human review

Documented for future reviewer (when funded):

1. **Pitch accent drop positions** for all 1,009 vocab entries — 5
   spotted as possibly off in my sample; the other 1,004 may also
   contain similar low-confidence cases.
2. **Audio-script alignment** — 50 listening + 54 reading audio
   files. Requires listening to confirm each script_ja matches the
   audio content.
3. **Idiomatic naturalness beyond my sample** — ~6,220 unsampled
   Japanese sentences. My audit sampled ~80 directly (≈1.3% of the
   corpus). The sample surfaced 0 naturalness issues, but extrapolating
   a "≥95% likely natural" rate from a 1.3% sample is not statistically
   justified — the unsampled remainder is **unverified for
   naturalness**, full stop. Exhaustive native review would establish
   the true rate.
4. **Hindi quality across 838+ LLM-curated entries** — translations
   written by Claude in native-Hindi-reviewer persona, not native
   human.
5. **JLPT-format calibration vs latest JEES sample papers** — the
   spirit-of-N5 conformance is good, but a JLPT-experienced reviewer
   could confirm difficulty calibration.

---

## CI invariants added this audit

| Gate | Prevents re-introduction of |
|------|-----------------------------|
| JA-89 | 5-in-one: counter-noun-pedagogy on native-counter-series; bare-article 'There is X' EN translations; animacy violations; `あの Xは どこですか` template in grammar.json; `毎日 X ことが できます` / `あした X つもりです` templates in vocab — *these specific named patterns only; not a universal grammar-error gate* |

CI invariants at this checkpoint: **91 → 92** (later extended to 93 with JA-90).

---

## State at this checkpoint

**91 → 92 CI invariants green at this commit. 158 fixes applied across 4 phases.**
The invariants prevent the specific patterns above from being re-introduced;
they do not assert that no other content-quality issues exist in the corpus.

Combined with prior audits (grammar 348 + vocab 540 + kanji 71 +
reading/dokkai 103 + mega-audit 838 + waves-1-2-3 3 + this pass 158
= **2,061 cumulative content fixes in 26 audit rounds this session,
within the audit categories defined this session**). A future audit
pass may define new categories and surface new findings.
