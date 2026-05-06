# JLPT N5 Audit — Round 9 (depth-first, post-v1.12.42)

**Date:** 2026-05-06
**Mode:** Audit-and-register only (per `prompts/N5Improvement.txt`)
**Scope:** /N5/ only. /N4/ work-blocked (Rule 1).
**Baseline:** HEAD `e6ff9b0` (master); v1.12.42 round-7-deferred batch closed.

Registered 27 findings into `feedback/n5-audit-2026-05-04.xlsx`
(Items rows 205..225 = 14 issues + 7 improvements; Questions rows 42..47 = 6 questions).

---

## Section 0: Strategic Positioning Verdict

**Niche N1 (native-Hindi-medium JLPT prep) — partial claim, scaling-blocked.**
Round-8 (v1.12.41) crossed the Q21 ≥10% native-reviewed threshold on **grammar
only** (27/178 patterns, 15%). The provenance-badge UI is now active. But three
content surfaces still show 100% `llm_curated`: vocab (0/1041 native_reviewed),
kanji (0/106), reading (0/45), listening (0/47). Most damagingly, **questions
have 0/290 `explanation_hi`** — the test-mode learner sees English-only
rationale even on the 27 native-reviewed grammar patterns. The niche
claim today is "we have the scaffolding"; the niche claim available with
30-40 LLM-persona-review hours is "every content surface, ≥10%
native-reviewed, end-to-end Hindi-medium experience including test mode."

**Niche N2 (privacy / no-account / offline) — credibly claimed.**
v1.12.42 added in-app Privacy/Notices markdown viewer (zero-deps), keeping
the "no third-party scripts" contract intact. Service-worker scope verified
+ documented in spec §9.5. Fonts are self-hosted (Inter L/R/M + Noto Sans JP
N5+N4-subset, 503 KB total). No telemetry. The trust pill on the home page
links to "Works offline" + install. This niche is owned today; only
incremental polish remains.

**Niche N3 (institutional / self-hosted) — partial claim.**
LICENSE = MIT (code) + CC BY-SA 4.0 (content). `docs/SELF-HOST.hi.md` shipped
in v1.12.40. `data/theme-overrides.json` allows brand customization without
forking. But: no measured bundle-size budget vs Tier-2/3 Indian-bandwidth
target; no Anki/CSV export to seed institutional Anki decks; no listed-on-
GitHub-marketplace "fork this" template surface.

**Niche N4 (all-in-one) — partial claim with one structural gap.**
Grammar/vocab/kanji surfaces are deep enough for genuine self-study (esp.
post-v1.12.41 with Hindi explanations on top-30 patterns, kanji mnemonics
on all 106, transitive-pair cross-links). Reading surface is acceptable.
**Listening surface and Test-paper structure are the two weakest links:**
listening uses a single VOICEVOX voice on 18/47 items and 29/47 carry no
voice metadata at all; test papers are 28 single-mondai 15-Q sets that
do **not** match the real JLPT-N5 paper shape (35Q×25min moji+goi /
32Q×50min bunpou+dokkai / 24Q×30min chokai). A learner wanting a
real-exam dress rehearsal cannot get one inside the app today.

**Recommended primary niche: N1 (native-Hindi-medium JLPT prep).**
Why this not the others: N2 is owned, polish-only; N3 needs go-to-market
work the engineering audit can't drive; N4 is partial across two
interlinked structural fixes (listening voices + paper shape). N1 has
the largest unrealized claim and the clearest single-lever execution
plan (Q33 LLM-persona-review model, already validated on grammar, applied
to remaining surfaces). The 2026-05-06 market-research scan confirms
the Hindi-medium vacuum is a genuine competitive opening with no
incumbent — this is the niche where unrealized depth most directly maps
to addressable market.

**Secondary niche: N4 (all-in-one).** Specifically the test-paper
shape + listening voice variety gaps. These are smaller lifts than
full N1 scaling but unlock the "single app from N5 to mock-test" claim.

**Top 5 changes that move N1 from "partial" to "credible" (referenced below by ID):**
1. **ISSUE-101** — `explanation_hi` on all 290 questions (critical:
   the test-mode loop is the highest-engagement surface and is currently
   English-only)
2. **ISSUE-111** — Q33-style LLM-persona Hindi review scaled across
   remaining 151 grammar patterns (`l1_notes.hi`, `explanation_hi`,
   `meaning_provenance: native_reviewed`)
3. **ISSUE-114** — same scaling on vocab `gloss_hi` (1041 entries) +
   kanji `meanings_hi` (106 entries) — completes corpus-wide ≥10%
   native_reviewed coverage
4. **ISSUE-094** — reading `summary_hi` on 45 passages (Devanagari)
5. **IMP-117 + IMP-116** — provenance-badge UI ported to vocab +
   kanji surfaces with `gloss_hi_provenance` / `meanings_hi_provenance`
   fields (data + UI shape)

**Honest competitive table:**

| App | Content depth | Native-Hindi-review % | Translation quality | Privacy posture | Discoverability | Install path |
|---|---|---|---|---|---|---|
| **JLPTSuccess N5** (this) | ✅ 178 grammar / 1041 vocab / 106 kanji / 45 reading / 47 listening; depth uneven (grammar deep, vocab shallow on examples) [src: data/*.json] | ⚠️ Grammar 27/178 (15%); other surfaces 0% [src: review_status field census above] | ⚠️ LLM-persona reviewed (Q33 model) on grammar top-30; everywhere else llm_curated [src: *_provenance fields] | ✅ No login, no telemetry, no third-party (CSP same-origin; v1.12.42 spec §9.5 + privacy viewer) [src: index.html CSP, sw.js] | ❌ GitHub Pages canonical only; no Indian-channel presence [src: README, repo metadata] | ✅ PWA install + offline shell; install banner in pwa.js [src: js/pwa.js initPwa] |
| **Yoisho Academy** (yoisho.in) — closest Indian incumbent | ⚠️ Course-based curriculum, not granular content browser | ❌ Not Hindi-native; English-medium with optional Hindi tutoring | n/a (instructor-led, not app) | ❌ Account required; tutoring sessions are video-call (third-party) | ✅ Indian university partnerships; Tier-1 city presence | ❌ No app; web only |

**Receipt:**
Registered 27 findings into n5-audit-2026-05-04.xlsx
(Items rows 205..225 = 14 issues + 7 improvements; Questions rows 42..47 = 6 questions).

---

## Section 0.5: Depth-Deficit Map

### Grammar (n=178) — Surface weight 1.5

| Depth dimension | Meeting bar | Below bar | % below | Worst-offender IDs |
|---|---|---|---|---|
| examples ≥5 (best-in-class) | 26 | 152 | **85%** | n5-024, n5-027, n5-028, n5-030, n5-031 |
| examples ≥4 | 70 | 108 | 61% | (subset of above) |
| contrasts ≥1 | 95 | 83 | 47% | patterns missing は/が, から/ので, etc. |
| `l1_notes.hi` (Hindi-specific) | 27 | 151 | **85%** | all patterns outside top-30 |
| `explanation_hi` (Devanagari long-form) | 27 | 151 | **85%** | same |
| `review_status: native_reviewed` | 27 | 151 | 85% | same |
| audio on at least 1 example | 0 | 178 | **100%** | all |
| pitch_accent on examples | 0 | 178 | **100%** | all |

**Dominant deficit (grammar):** `examples ≥5` — 152 patterns sit at the spec
floor (3) instead of best-in-class (5-7). Bunpro ships 5-7; learners notice.

### Vocab (n=1041) — Surface weight 1.0

| Depth dimension | Meeting bar | Below bar | % below | Worst-offender IDs |
|---|---|---|---|---|
| examples ≥2 (floor) | 114 | 927 | **89%** | 私たち, かれ, かのじょ, みなさん, どなた |
| examples ≥3 (target) | 0 | 1041 | **100%** | all |
| pitch_accent | 59 | 982 | **94%** | bulk |
| collocations ≥1 | 29 | 1012 | **97%** | bulk |
| register tag | 21 | 1020 | **98%** | bulk (only 21 keigo entries from v1.12.42) |
| counter (out of 589 nouns) | 3 | 586 | **99%** | 本→冊, 車→台, 人→人, 紙→枚 — none flagged |
| verb_class (out of 134 verbs) | 0 | 134 | **100%** | all 134 verbs |
| pair_id (transitivity) | 22 | 1019 | **98%** | 開ける/開く, 閉める/閉まる, 入れる/入る, etc. |
| `review_status: native_reviewed` | 0 | 1041 | **100%** | all |

**Dominant deficit (vocab):** `examples ≥2` (927 below) is the largest in
absolute count, but `verb_class` at 100% on all 134 verbs is the highest-
leverage missing field — without it, conjugation drills can't be programmatic.

### Kanji (n=106) — Surface weight 1.3

| Depth dimension | Meeting bar | Below bar | % below | Worst-offender |
|---|---|---|---|---|
| examples ≥5 (compound vocab) | 13 | 93 | **88%** | 道, 名, 百, 千, 万, 円, 火, 水, 木, 金 |
| examples ≥3 | 45 | 61 | 58% | (subset above) |
| confusable_with ≥1 | 29 | 77 | **73%** | bulk; 千/干/王/玉, 古/占, 千/午 not yet linked |
| sentences ≥1 (full N5 sentence) | 106 | 0 | 0% | none — ALREADY 100% covered ✓ |
| mnemonic | 106 | 0 | 0% | ALREADY 100% covered ✓ |
| `review_status: native_reviewed` | 0 | 106 | **100%** | all |

**Dominant deficit (kanji):** `examples ≥5` — 93 kanji have <5 vocab
cross-links. Learners hitting 千 (six examples) vs 道 (two) feel the
inconsistency.

### Reading (n=45) — Surface weight 1.2

| Depth dimension | Meeting bar | Below bar | % below | Worst-offender |
|---|---|---|---|---|
| mondai-5 (medium passages) | 5 | 40 | **89%** | distribution skewed against M5 (real exam: 4/9 = 44%; current: 5/45 = 11%) |
| mondai-6 (info-search) | 4 | 41 | 91% | acceptable proportion (real: 2/15 = 13%; current: 4/45 = 9%) |
| `summary_hi` | 0 | 45 | **100%** | all |
| cultural_context | 0 | 45 | **100%** | all |
| format_role (primary/supplementary) | 0 | 45 | **100%** | all |
| format_type | 4 | 41 | 91% | bulk |
| audio | 40 | 5 | 11% | five passages text-only without rationale |
| `review_status: native_reviewed` | 0 | 45 | **100%** | all |

**Dominant deficit (reading):** `summary_hi` 100% deficit — Hindi locale
learners read English summary on every passage. Niche-N1 critical.

### Listening (n=47) — Surface weight 1.0

| Depth dimension | Meeting bar | Below bar | % below | Worst-offender |
|---|---|---|---|---|
| audio file present | 40 | 7 | 15% | 7 silent items |
| voice metadata | 18 | 29 | **62%** | 29 items have no voice; 18 use single voicevox-shikoku-metan |
| voice variety (distinct voices) | **1** | n/a | n/a | real exam = ≥4 voices |
| cultural_context | 9 | 38 | 81% | bulk |
| `explanation_hi` | 12 | 35 | 74% | bulk |
| vocab_glossary | 0 | 47 | **100%** | all |
| transcript_lines (timestamped) | 0 | 47 | **100%** | all |
| `review_status: native_reviewed` | 0 | 47 | **100%** | all |

**Dominant deficit (listening):** voice variety = 1 (already deferred
ISSUE-062, IMP-094) — but the secondary deficit is `vocab_glossary` 100%
deficit, which is fixable without external recording budget.

### Cross-surface dominant deficit

**`review_status: native_reviewed` outside grammar** — 1239 entries across
vocab+kanji+reading+listening sit at 100% `llm_curated`. Applying the
Q33 LLM-persona-review model (already validated on grammar) would lift
all four surfaces over the Q21 ≥10% trust threshold simultaneously,
unlocking the provenance badge on every detail page and crossing from
"partial niche-N1" to "credible niche-N1". Estimated effort: 30-40 hr
LLM-persona review on vocab `gloss_hi`, ~5-10 hr on kanji `meanings_hi`,
~3-5 hr on reading `summary_hi`, ~5-7 hr on listening `explanation_hi`.
Total ~45-60 hr to complete corpus-wide.

### Effort estimate per surface

| Surface | Dominant deficit | Bring-to-bar effort |
|---|---|---|
| Grammar | `examples ≥5` on 152 patterns; LLM-curated drafting + Q33 review | ~25-30 hr |
| Vocab | `examples ≥2` on 927 entries; bulk LLM auto-cross-reference from grammar; spot-check | ~12-18 hr |
| Kanji | `examples ≥5` on 93 entries; mostly auto-derive from vocab corpus | ~3-5 hr |
| Reading | `summary_hi` on 45 passages; LLM-persona Hindi translation | ~3-5 hr |
| Listening | voice variety (external blocker — VOICEVOX multi-voice install or recording budget); `vocab_glossary` is fixable in ~4 hr | ~4-8 hr (excluding voice work) |

### 10 worst-offender entries cross-surface

Ranked by (number of dimensions failed × surface weight):

| # | ID / glyph | Surface | Dimensions failed |
|---|---|---|---|
| 1 | n5-024 | grammar | examples<5, contrasts none, l1_notes.hi none, explanation_hi none, no audio, no pitch (6×1.5 = 9.0) |
| 2 | n5-027 | grammar | same six (6×1.5 = 9.0) |
| 3 | n5-028 | grammar | same six (6×1.5 = 9.0) |
| 4 | 道 | kanji | examples<5, no native_review (2×1.3 = 2.6 — but worst kanji depth-wise) |
| 5 | 名 | kanji | examples<5, no native_review |
| 6 | 百 | kanji | examples<5, no native_review |
| 7 | 私たち | vocab | examples<2, no pitch, no collocations, no register, no native_review (5×1.0 = 5.0) |
| 8 | かれ | vocab | same five |
| 9 | reading-005 (any mondai-5 item) | reading | summary_hi, cultural_context, format_role, native_review (4×1.2 = 4.8) |
| 10 | listening-001 (any item without voice) | listening | voice, glossary, transcript_lines, native_review (4×1.0 = 4.0) |

---

## Section 1: Top-of-list (10 highest-priority items overall)

DEPTH items occupy 8 of 10 slots; META (structural/UI) occupy 2.

1. `[ISSUE-101] [BLOCKER] [P1] [N1] [DEPTH]` — `explanation_hi` missing on all 290 test-mode questions; learner gets English-only rationale on every wrong answer even when site locale is Hindi.
2. `[ISSUE-111] [MAJOR] [P1] [N1] [DEPTH]` — Scale Q33 LLM-persona Hindi review across remaining 151 grammar patterns (l1_notes.hi + explanation_hi + meaning_provenance: native_reviewed).
3. `[ISSUE-114] [MAJOR] [P1] [N1] [DEPTH]` — Same Q33 scaling on vocab gloss_hi (1041) + kanji meanings_hi (106); cross-surface trust signal.
4. `[ISSUE-108] [MAJOR] [P2] [N4] [DEPTH]` — Grammar examples 3→5 on 152 patterns to match Bunpro's best-in-class floor.
5. `[ISSUE-104] [MAJOR] [P2] [N4] [DEPTH]` — Vocab examples ≥2 on 927 entries (currently 11%; auto-derive from grammar examples is the cheap path).
6. `[ISSUE-093] [MAJOR] [P2] [N4] [META]` — Real-exam-shape combined mock paper + chokai paper; current 28 single-mondai sets don't simulate the actual JLPT N5 paper.
7. `[ISSUE-102] [MAJOR] [P2] [N4] [DEPTH]` — Vocab verb_class on all 134 verbs (Group-1/Group-2/irregular + Group-1-exception flag); programmatic conjugation-drill correctness depends on this.
8. `[ISSUE-094] [MAJOR] [P2] [N1] [DEPTH]` — Reading summary_hi on 45 passages (Devanagari); niche-N1 surface gap.
9. `[ISSUE-112] [MAJOR] [P3] [N4] [DEPTH]` — Kanji examples 5+ on 93 kanji; mostly auto-derive from vocab cross-references.
10. `[IMP-116] [IMPROVEMENT] [P2] [N1] [META]` — Provenance-badge UI ported from grammar to vocab + kanji surfaces (parallels v1.12.41 round-8 work; data shape needs IMP-117).

Section 1 traces back to Section 0.5: every DEPTH item maps to a row in the surface tables above. ISSUE-101 (questions explanation_hi) is the highest-priority non-data finding because the test loop is the dominant engagement surface.

---

## Section 2: Existing Issues (prioritized)

### P1 (do first)

**ISSUE-101** — explanation_hi missing on all test-mode questions
- Type: Issue
- Severity: BLOCKER (niche-N1 contract)
- Priority: P1
- Impact: HIGH — 290 questions; the test-mode loop is the largest engagement surface
- Effort: MEDIUM — 290 entries × LLM-persona Hindi translation
- Niche-fit: N1
- Category: i18n / content depth (questions surface)
- Location: `data/questions.json` — every question entry
- Current state: 0/290 have `explanation_hi`; the test-mode renderer falls back to `explanation_en` regardless of UI locale.
- Why it matters: Hindi-locale learners who set EN|HI to HI in settings still see English-only rationale on every wrong answer. This breaks the niche-N1 contract at the highest-engagement surface — even the 27 native-reviewed grammar patterns produce English-only test-mode feedback.
- Suggested direction: LLM-persona Hindi translation pass on `explanation_en` → `explanation_hi`; gate behind `meaning_provenance` per-question; ship in a single batch.
- Dependencies: none.

### P2 (do soon)

**ISSUE-093** — Mock papers don't match real JLPT-N5 paper shape
- Type: Issue. Severity: MAJOR. Priority: P2.
- Impact: HIGH — niche-N4 (all-in-one) defining gap.
- Effort: MEDIUM — virtual aggregator over existing question pool; no new question authoring.
- Niche-fit: N4
- Category: Mock-test authenticity
- Location: `data/papers/manifest.json`, `data/papers/{moji,goi,bunpou,dokkai}/`
- Current state: 28 papers × 15-Q single-mondai sets (paper-1 = M1 only). No combined-section paper. No chokai (listening) papers — listening is 47 standalone items not arrayed as a 24-Q paper.
- Why matters: Real JLPT N5 = 35Q×25min (moji+goi) / 32Q×50min (bunpou+dokkai) / 24Q×30min (chokai). A learner cannot run a real-exam dress rehearsal inside the app today. Best-in-class JLPT prep apps (JLPT Sensei sample papers, Marugoto exam-mode) all ship the real shape.
- Suggested direction: Build a virtual paper aggregator: combine moji[paper-N] + goi[paper-N] into "言語知識 paper-N" (~35Q, with the IMP-086 25-min combined timer); same for bunpou+dokkai (~32Q, 50-min); add chokai virtual paper from listening 47-pool (M1×7 + M2×6 + M3×5 + M4×6).
- Dependencies: IMP-115 (full mock paper UI).

**ISSUE-104** — Vocab examples ≥2 missing on 927 entries (89%)
- Type: Issue. Severity: MAJOR. Priority: P2.
- Impact: HIGH — vocab depth is the second-largest content surface
- Effort: MEDIUM — auto-derive from grammar examples for entries with `vocab_ids` cross-link; manual for the 96 entries without grammar match
- Niche-fit: N4
- Category: Content depth (vocab)
- Location: `data/vocab.json` entries with `len(examples) < 2`
- Current state: 114/1041 (11%) have ≥2 examples; floor per spec is 2.
- Why matters: A serious vocab page needs ≥2 examples showing the word in different contexts. 11% coverage means 89% of vocab pages feel anemic vs Bunpro/Renshuu.
- Suggested direction: Auto-derive second example from grammar.json `vocab_ids` cross-references where the entry appears; LLM-curated for the residual.
- Dependencies: none.

**ISSUE-108** — Grammar examples ≥5 on 152 patterns (85% deficit)
- Type: Issue. Severity: MAJOR. Priority: P2.
- Impact: HIGH — best-in-class is 5-7 (Bunpro)
- Effort: MEDIUM — author 2 examples × 152 patterns + diversity check (different attachment surface / register / topic)
- Niche-fit: N4
- Category: Content depth (grammar)
- Location: `data/grammar.json` patterns with `len(examples) < 5`
- Current state: 26/178 patterns (15%) have ≥5 examples.
- Why matters: Bunpro ships 5-7 per pattern; the perceived-depth gap is visible even on a single visit to a Bunpro pattern page.
- Suggested direction: 2 new examples per pattern, LLM-drafted with attachment-surface diversity constraint; spot-check JA-13 (kanji subset) and JA-1 (vocab subset) on output.
- Dependencies: none.

**ISSUE-111** — Q33 LLM-persona Hindi review scaling on grammar (151 patterns)
- Type: Issue. Severity: MAJOR. Priority: P1.
- Impact: HIGH — completes niche-N1 grammar surface
- Effort: MEDIUM — 151 patterns × (l1_notes.hi + explanation_hi + meaning_provenance flip) — already validated workflow on top-30
- Niche-fit: N1
- Category: i18n / native review
- Location: `data/grammar.json` patterns where `meaning_provenance != "native_reviewed"`
- Current state: 27/178 (15%) — Q21 threshold crossed but only just; remaining 151 are still llm_curated.
- Why matters: Round-8 validated the Q33 model (LLM with native-Hindi-speaker persona). Scaling it to remaining grammar moves the niche-N1 claim from "we have proof of concept" to "every grammar pattern has Hindi-quality content."
- Suggested direction: Reuse round-8 batch script pattern; review in 50-pattern chunks for traceability.
- Dependencies: none (process is proven).

**ISSUE-114** — Native_reviewed scaling on vocab + kanji (1147 entries)
- Type: Issue. Severity: MAJOR. Priority: P1.
- Impact: HIGH — unlocks provenance badge on two more surfaces
- Effort: HIGH — 1041 vocab + 106 kanji × LLM-persona review
- Niche-fit: N1
- Category: i18n / native review
- Location: `data/vocab.json`, `data/kanji.json`
- Current state: 0/1041 vocab and 0/106 kanji have `review_status: native_reviewed`. Both surfaces sit at 100% `llm_curated` for `gloss_hi` / `meanings_hi`.
- Why matters: Provenance badge UI (currently only on grammar, IMP-116 ports it elsewhere) needs at least the Q21 10% threshold per surface to be worth showing. This is the single cross-surface lever.
- Suggested direction: Same Q33 LLM-persona-review approach; ship in batches of ~100 entries with `gloss_hi_provenance` field added (IMP-117 prerequisite).
- Dependencies: IMP-117 (data-shape: gloss_hi_provenance + meanings_hi_provenance fields).

**ISSUE-094** — Reading summary_hi missing on all 45 passages
- Type: Issue. Severity: MAJOR. Priority: P2.
- Impact: MEDIUM — Hindi learners read English summary on every passage
- Effort: LOW — 45 entries × LLM-persona Hindi translation
- Niche-fit: N1
- Category: i18n / content depth (reading)
- Location: `data/reading.json` passages
- Current state: 0/45 have `summary_hi`.
- Why matters: A learner reading 田中さんは… in Hindi-locale mode still gets an English summary. The summary is a critical navigation aid (decide whether to attempt the passage) — English-only summary breaks the niche-N1 reading surface.
- Suggested direction: LLM-persona Hindi translation of `summary` → `summary_hi`.
- Dependencies: none.

**ISSUE-099** — Listening voice variety = 1 (was logged as ISSUE-062, ISSUE-089, ISSUE-090; current state worse)
- Type: Issue. Severity: MAJOR. Priority: P2.
- Impact: MEDIUM — niche-N4 listening realism gap
- Effort: HIGH — VOICEVOX multi-voice setup or recording budget (external blocker)
- Niche-fit: N4
- Category: Audio (listening)
- Location: `data/listening.json` items
- Current state: 18/47 use synthetic-voicevox-shikoku-metan only; 29/47 have no voice metadata (and presumably no audio or fall back to default). Target: ≥4 distinct voices.
- Why matters: Real JLPT N5 chokai exposes learners to 4+ distinct voices typically 2 female + 2 male spanning ≥2 age groups. Single-voice listening is a defining gap vs JapanesePod101 / official sample papers.
- Suggested direction: Either (a) install VOICEVOX local-server with multiple speakers and re-render the 47 items; or (b) crowd-source community recording. Both are gated on a decision (Q42).
- Dependencies: Q42 (voice variety budget decision).

**ISSUE-102** — Vocab verb_class missing on all 134 verbs
- Type: Issue. Severity: MAJOR. Priority: P2.
- Impact: HIGH — affects conjugation drill correctness programmatically
- Effort: LOW — 134 entries × Group-1/2/irregular flag from POS field; explicit Group-1-exception flag for 6 known verbs (入る/帰る/走る/知る/切る/要る)
- Niche-fit: N4
- Category: Schema / depth (vocab)
- Location: `data/vocab.json` entries where `pos.startswith('verb')`
- Current state: 0/134 verbs have `verb_class` field.
- Why matters: Without this flag, the conjugation drill tool can't tell ichidan from godan from irregular. The current pos field captures verb-1 / verb-2 / verb-3 but doesn't expose Group-1 exceptions (X-6.6 invariant in spec). Risk: conjugation drill produces wrong forms for the 6 exception verbs.
- Suggested direction: Map pos → verb_class deterministically; add `group1_exception: true` on the 6 known exception verbs.
- Dependencies: none.

### P3 (do this cycle)

**ISSUE-101a → ISSUE-103** — Vocab pair_id (transitivity) on canonical N5 pairs
- Type: Issue. Severity: MINOR. Priority: P3.
- Impact: MEDIUM. Effort: LOW.
- Niche-fit: N4. Category: Schema / depth (vocab).
- Location: `data/vocab.json` entries.
- Current state: 22/1041 entries paired. The 12 canonical N5 transitivity pairs (開ける/開く, 閉める/閉まる, 入れる/入る, 出す/出る, 始める/始まる, 止める/止まる, つける/つく, 消す/消える, 起こす/起きる, 落とす/落ちる, 直す/直る, 切る/切れる) need full coverage = 24 entries minimum.
- Why matters: Transitive/intransitive pair drilling is a defining N5 grammar exam topic (が vs を, automatic vs deliberate action).
- Suggested direction: Author the 12 pairs in a single batch script; add `pair_id` cross-references both directions.
- Dependencies: none.

**ISSUE-112** — Kanji examples ≥5 on 93 kanji
- Type: Issue. Severity: MAJOR. Priority: P3.
- Impact: MEDIUM — uneven kanji depth
- Effort: LOW — auto-derive from vocab corpus (every kanji should appear in ≥5 vocab entries with the kanji in `form`)
- Niche-fit: N4. Category: Content depth (kanji).
- Location: `data/kanji.json` entries with `len(examples) < 5`.
- Current state: 13/106 kanji have ≥5 examples.
- Worst-offenders: 道, 名, 百, 千, 万, 円, 火, 水, 木, 金 (numerals + elements; many appear in vocab but cross-link missing)
- Why matters: WaniKani's defining feature is consistent depth across all kanji. Inconsistent (some 6 examples, some 2) reads as scaffolding rather than finished product.
- Suggested direction: Auto-script: for each kanji, pull all vocab entries where `form` contains the glyph; pick top-N most common; cross-link.
- Dependencies: none.

**ISSUE-109** — Grammar contrasts on 83 patterns
- Type: Issue. Severity: MINOR. Priority: P3.
- Impact: MEDIUM. Effort: MEDIUM.
- Niche-fit: N4. Category: Content depth (grammar).
- Location: `data/grammar.json` patterns with empty `contrasts`.
- Current state: 95/178 (53%) have ≥1 contrast cross-link. The mandatory N5 contrast set (は/が, から/ので, も/と, で/に, けど/が, 〜たことがある/〜た, 〜ている progressive/resultative, 〜ましょう/〜ませんか, あげる/くれる/もらう) needs every pattern in those clusters cross-linked.
- Why matters: Confusable-pair disambiguation is the most common learner failure mode at N5; explicit cross-links help users find both sides.
- Suggested direction: Audit the 11 mandatory contrast clusters; ensure every pattern in each cluster cross-links to its sibling.
- Dependencies: none.

**ISSUE-095** — Reading cultural_context missing
- Type: Issue. Severity: MINOR. Priority: P3.
- Impact: MEDIUM. Effort: LOW.
- Niche-fit: N4. Category: Content depth (reading).
- Location: `data/reading.json` passages.
- Current state: 0/45.
- Why matters: Passages mentioning Japan-specific concepts (おにぎり, school clubs, 銭湯, 塾) need a brief explainer for non-Japan-domiciled learners. Without it, the comprehension question is harder than the Japanese alone justifies.
- Suggested direction: 1-2 sentence cultural callout per passage where applicable; ~15-20 of 45 will need one.
- Dependencies: none.

**ISSUE-097** — Reading format_role missing on all 45
- Type: Issue. Severity: MINOR. Priority: P3.
- Impact: LOW (spec compliance). Effort: LOW.
- Niche-fit: none. Category: Schema (reading).
- Location: `data/reading.json` passages.
- Current state: 0/45 have `format_role` (primary vs supplementary discipline per JA invariants).
- Why matters: Spec calls for primary/supplementary classification so paper-builder can weight question-type distribution; without it the builder is blind to the structural property.
- Suggested direction: Tag every passage primary/supplementary based on question type; primary if ≥2 inference questions, supplementary if all-fact-retrieval.
- Dependencies: none.

**ISSUE-098** — Reading + listening audio missing on 12 entries (5 reading + 7 listening)
- Type: Issue. Severity: MINOR. Priority: P3.
- Impact: MEDIUM. Effort: LOW.
- Niche-fit: N4. Category: Audio.
- Location: 5 reading passages without `audio`; 7 listening items without `audio`.
- Current state: 40/45 reading have audio; 40/47 listening have audio.
- Why matters: Inconsistent audio coverage means a learner doing the reading surface end-to-end hits 5 silent items; same for listening's 7. Either generate via gtts or document as text-only with rationale.
- Suggested direction: Generate gtts audio for the 12 missing items in a single build pass; verify via JA-23 (listening choices match script) and any reading-specific JA invariant.
- Dependencies: none.

### P4 (next cycle)

**ISSUE-100** — Listening vocab_glossary missing on all 47
- Type: Issue. Severity: MINOR. Priority: P4. Impact: LOW. Effort: LOW.
- Niche-fit: N4. Category: Content depth (listening).
- Current state: 0/47 have `vocab_glossary`.
- Why: Per-drill vocab preview helps learners parse the audio. Best-in-class (JapanesePod101) provides this. Defer until P1-P3 land.

**ISSUE-105** — Vocab pitch_accent on 982 entries
- Type: Issue. Severity: MINOR. Priority: P4. Impact: LOW. Effort: HIGH.
- Niche-fit: N1. Category: Content depth (vocab).
- Current state: 59/1041. Why: Pitch isn't a JLPT scoring criterion but is a strong signal for serious learners. Defer until grammar/kanji native_reviewed scaling lands.

**ISSUE-106** — Vocab register tag on 1020 entries
- Type: Issue. Severity: MINOR. Priority: P4. Impact: LOW. Effort: MEDIUM.
- Niche-fit: N4. Category: Content depth (vocab).
- Current state: 21/1041 (2%). Why: 21 keigo-chain entries from v1.12.42 only. Bulk register tagging (casual/polite/humble/respectful) is high-volume LLM-curatable work but low per-entry value.

**ISSUE-107** — Vocab collocations on 1012 entries
- Type: Issue. Severity: MINOR. Priority: P4. Impact: LOW. Effort: MEDIUM.
- Niche-fit: N4. Category: Content depth (vocab).
- Current state: 29/1041 (3%). Why: 29 high-frequency entries from round-8 only.

**ISSUE-110** — Grammar audio + pitch on examples (100% deficit)
- Type: Issue. Severity: MINOR. Priority: P4. Impact: LOW. Effort: HIGH.
- Niche-fit: N4. Category: Audio (grammar).
- Current state: 0/178 patterns have audio or pitch on any example. Why: External blocker (audio rendering pipeline + pitch annotation tooling). Defer until listening voice work resolves Q42.

**ISSUE-113** — Kanji confusable_with on 77 kanji
- Type: Issue. Severity: MINOR. Priority: P4. Impact: LOW. Effort: LOW.
- Niche-fit: N4. Category: Content depth (kanji).
- Current state: 29/106 (27%). The 8 mandatory N5 confusable clusters from spec need full coverage.

---

## Section 3: Improvement Ideas (prioritized)

### P2 (do soon)

**IMP-115** — Real-exam-shape full mock paper UI
- Type: Improvement. Severity: IMPROVEMENT. Priority: P2.
- Impact: HIGH. Effort: MEDIUM. Niche-fit: N4.
- Category: Test mode UI / mock-paper engine.
- Location: `js/papers.js`, `js/sitting.js`, `data/papers/manifest.json`.
- Current state: Test mode runs single-mondai 15-Q sets only. No "full mock paper" entry point.
- Best-in-class comparison: JLPT Sensei + official jlpt.jp sample papers ship the real 35/32/24 shape; learners doing serious exam prep need this for time-management practice.
- Suggested direction: Add a "Full Mock Test" tile on `#/test` that aggregates moji[paper-N] + goi[paper-N] (35Q, 25min combined timer) + bunpou[paper-N] + dokkai[paper-N] (32Q, 50min) + chokai-virtual (24Q, 30min). Reuse IMP-086 timing infrastructure.
- Dependencies: ISSUE-093 (papers structure), IMP-119 (chokai virtual paper).

**IMP-116** — Provenance-badge UI on vocab + kanji surfaces
- Type: Improvement. Severity: IMPROVEMENT. Priority: P2.
- Impact: HIGH. Effort: MEDIUM. Niche-fit: N1.
- Category: Trust signal / UI.
- Location: `js/learn-vocab.js`, `js/kanji.js`, `js/provenance-badge.js`.
- Current state: Provenance badge active on grammar only (round-8 v1.12.41). Vocab/kanji detail pages don't expose review status.
- Best-in-class: Bunpro shows native-reviewed indicators on every entry (subscription tier visible with the indicator).
- Suggested direction: Port `provenance-badge.js` rendering to vocab + kanji detail templates; gate behind per-surface ≥10% native_reviewed threshold (Q21 rule); ship after IMP-117 lands the data shape.
- Dependencies: IMP-117 (data-shape for gloss_hi_provenance and meanings_hi_provenance).

**IMP-117** — gloss_hi_provenance + meanings_hi_provenance data shape
- Type: Improvement. Severity: IMPROVEMENT. Priority: P2.
- Impact: MEDIUM. Effort: LOW. Niche-fit: N1.
- Category: Schema / data shape.
- Location: `data/vocab.json`, `data/kanji.json`, `tools/check_content_integrity.py`.
- Current state: Vocab has `gloss_provenance` field; kanji has `meanings_provenance`. Hindi-specific provenance is implicit (whole-entry `review_status`). Need a per-locale-per-field provenance to match how grammar treats `meaning_provenance` and `explanation_provenance` separately.
- Suggested direction: Add `gloss_hi_provenance` to vocab schema, `meanings_hi_provenance` to kanji schema; default to entry-level `review_status` for backwards compat; add JA-40 invariant to enforce closed enum.
- Dependencies: none.

**IMP-119** — Listening 24-Q chokai virtual paper
- Type: Improvement. Severity: IMPROVEMENT. Priority: P2.
- Impact: MEDIUM. Effort: LOW. Niche-fit: N4.
- Category: Test mode (listening).
- Location: `js/papers.js`, `data/papers/manifest.json`.
- Current state: Listening is 47 standalone items, not arrayed as a 24-Q paper.
- Best-in-class: official jlpt.jp sample paper structure.
- Suggested direction: Sample 7 M1 + 6 M2 + 5 M3 + 6 M4 from listening pool; surface as virtual paper in manifest.json under new `chokai` category; reuse IMP-086 30-min timer.
- Dependencies: ISSUE-099 (voice variety — current single-voice paper is poor real-exam simulation).

### P3 (do this cycle)

**IMP-120** — Vocabulary keigo-chain visualizer
- Type: Improvement. Severity: IMPROVEMENT. Priority: P3.
- Impact: MEDIUM. Effort: LOW. Niche-fit: N4. Category: UI / vocab.
- Location: `js/learn-vocab.js`.
- Current state: 9 entries with `register_chain_id` (3 trios from v1.12.42) render as independent leaf pages.
- Suggested direction: When a vocab page has `register_chain_id`, render a side-by-side trio panel (humble | plain | respectful) at the top of the detail view.
- Dependencies: ISSUE-103 (more transitivity pairs would benefit from same UI shape).

**IMP-122** — Per-paper timing display ("~7 min in real exam pace")
- Type: Improvement. Severity: IMPROVEMENT. Priority: P3.
- Impact: LOW. Effort: LOW. Niche-fit: N4. Category: Test mode UI.
- Location: `js/papers.js` paper-list grid.
- Current state: Paper cards show question count + difficulty but no expected time.
- Suggested direction: On each paper card, show "~X min in real exam pace" derived from sec-per-question table (43 sec for moji/goi, 94 sec for bunpou/dokkai, 75 sec for chokai). Helps learners time-budget self-study.
- Dependencies: none.

**IMP-123** — Full-paper score-report breakdown (real JLPT shape)
- Type: Improvement. Severity: IMPROVEMENT. Priority: P3.
- Impact: MEDIUM. Effort: MEDIUM. Niche-fit: N4. Category: Test mode results.
- Location: `js/papers.js` results view.
- Current state: After paper submit, shows total correct/total. No per-mondai breakdown, no per-section score, no pass/fail per minimum.
- Best-in-class: Real JLPT N5 score report shows per-section scores + per-minimum pass status; replicating this shape is essential for exam-prep authenticity.
- Suggested direction: Score-report UI matching the real JLPT shape: "言語知識(文字・語彙) X/35", "言語知識(文法)・読解 X/32", "聴解 X/24", "Total X/180", with pass-mark display (80/180 with per-section minimums 38/19/19).
- Dependencies: IMP-115 (full-paper UI ships first).

### P4 (next cycle)

**IMP-118** — Self-host Devanagari subset web font
- Type: Improvement. Severity: IMPROVEMENT. Priority: P4.
- Impact: LOW. Effort: LOW. Niche-fit: N1, N2.
- Category: Performance / privacy.
- Location: `fonts/`, `css/main.css`.
- Current state: Hindi text relies on system Noto Sans Devanagari; Tier-2/3 Indian devices may render with fallback fonts (incl. potentially-unfree fonts).
- Suggested direction: Subset Noto Sans Devanagari to N5 Hindi vocabulary (~200 unique glyphs) and self-host as `noto-sans-deva-400.woff2`. Add to sw.js precache.
- Dependencies: none.

**IMP-121** — Daily review queue (cross-skill SRS)
- Type: Improvement. Severity: IMPROVEMENT. Priority: P4.
- Impact: HIGH. Effort: HIGH. Niche-fit: N4.
- Category: SRS / engagement.
- Location: New module `js/daily-review.js`; storage namespace.
- Current state: Each surface tracks its own SRS independently. No "today's reviews" unified view.
- Best-in-class: Bunpro's daily queue, Anki's deck. The single feature most cited in retention reviews.
- Suggested direction: New route `#/today` aggregating items from grammar/vocab/kanji that hit due-date today; FSRS-4.5 default. Defer until corpus-level depth scaling lands.
- Dependencies: ISSUE-114 (depth-first cycle finishing).

---

## Section 4: Coverage Map (read-only snapshot)

**Corpus counts:**
- Grammar: 178 patterns (153 core_n5, 25 late_n5)
- Vocab: 1041 entries (589 noun, 134 verbs across verb-1/-2/-3, 75 i-adj, 27 na-adj, 46 adverb, others)
- Kanji: 106 (whitelist matches)
- Reading: 45 passages (mondai 4: 36 / mondai 5: 5 / mondai 6: 4)
- Listening: 47 items (mondai 1: 14 / mondai 2: 13 / mondai 3: 13 / mondai 4: 7)
- Questions: 290 in `questions.json`; 402 paper-bound across 28 papers (moji/goi/bunpou/dokkai 7 papers each)

**Test-suite status:**
- `tools/check_content_integrity.py`: 48/48 PASS (current HEAD `e6ff9b0`)
- `tools/check_design_system.py`: 8/8 PASS

**Locale completeness table:**

| Surface | en | hi |
|---|---|---|
| UI chrome (`locales/*.json`) | 113/113 (100%) | 116/113 (hi has 3 extra keys; en 100% covered by hi superset) |
| Grammar `meaning_*` | 178/178 (100%) | 178/178 (100%) |
| Grammar `explanation_*` | 178/178 (100%) | 27/178 (15%) |
| Grammar `l1_notes.*` | n/a | 27/178 (15%) |
| Vocab `gloss` | 1041/1041 (100%) | 1041/1041 (100%) |
| Kanji `meanings` | 106/106 (100%) | 106/106 (100%) |
| Reading `summary` | 45/45 (100%) | 0/45 (0%) ← niche-N1 gap |
| Listening `explanation` | 47/47 (100%) | 12/47 (26%) |
| Questions `explanation` | 290/290 (100%) | 0/290 (0%) ← niche-N1 BLOCKER |

**Native-reviewed vs LLM-curated:**

| Surface | native_reviewed | llm_curated | auto_generated |
|---|---|---|---|
| Grammar | 27/178 (15%) | 151/178 (85%) | 0 |
| Vocab | 0/1041 | 1041/1041 (100%) | 0 |
| Kanji | 0/106 | 106/106 (100%) | 0 |
| Reading | 0/45 | 45/45 (100%) | 0 |
| Listening | 0/47 | 47/47 (100%) | 0 |

**Deprecated-locale stragglers (vi/id/ne/zh):**
Verified zero references in `data/`, `js/` (excluding migration code), `css/`, `locales/`. JA-39 invariant guards. Historical CHANGELOG entries excluded (immutable record per CLAUDE.md).

**Per-surface presence/absence:**
✓ Grammar surface, ✓ Vocabulary surface, ✓ Kanji surface, ✓ Reading surface, ✓ Listening surface, ✓ Test mode, ✓ Progress dashboard, ✓ Changelog, ✓ Feedback, ✓ Privacy (in-app viewer per v1.12.42 ISSUE-055).

**localStorage namespace:**
README says `n5.*`; PRIVACY says `jlpt-n5-tutor:*`. JA-37 invariant guards code↔PRIVACY agreement and is PASS — so PRIVACY is the authoritative reference and the runtime uses `jlpt-n5-tutor:*`. README is stale (this is round-7's IMP-079, marked Done — superseded by JA-37 invariant; no further action).

---

## Section 5: Out-of-Scope Notes

- N4 listening voice variety / transcript timestamps / native recordings (already deferred ISSUE-062, IMP-090, IMP-094, IMP-105). Do not start.
- Top-level JLPTSuccess level-picker improvements (cross-level audit out of N5 scope).
- Future-level (N3-N1) considerations.
- Optional: Anki/CSV export (niche-N3 lever) — would warrant its own audit pass; not registered this cycle.

---

## Section 6: Open Questions

**Q39 — Native-Hindi-review scaling commitment.**
Round-8 validated the Q33 LLM-persona model on 27 grammar patterns. Scaling
to remaining 151 grammar + 1041 vocab + 106 kanji + 45 reading + 47 listening
≈ 45-60 hours of LLM-persona review, all outside the L1 (Hindi) author's
direct verification. The audit can recommend the scaling but cannot decide
whether the persona-review quality bar is sufficient for trust-level
"native_reviewed" claims at this scale. Decision needed: full corpus-wide
scaling now (≥10% per surface = badge unlock), or stage by surface (grammar
first → 100%, then vocab → 10%, then others)?

**Q40 — Real-exam-shape mock paper.**
ISSUE-093 + IMP-115 propose a virtual aggregator over existing papers. But
the underlying papers are 15-Q single-mondai sets; combining moji[paper-N]
+ goi[paper-N] gives 30 questions, not the canonical 35. Decision needed:
build virtual aggregator on existing pool (acceptable approximation), OR
defer until a paper-redesign cycle that authors true 35/32/24-shape papers
from KnowledgeBank?

**Q41 — Vocab counter field scope.**
ISSUE-101 (counter on nouns) needs 30-50 high-frequency nouns for the
common counters (本→冊, 車→台, 人→人, 紙→枚, 個 for objects, ...). Going
to full 589 nouns yields diminishing returns (most don't take a specific
counter). Decision needed: top-50 high-frequency only (~2 hr), or full
589 sweep with explicit "no specific counter" flag (~10 hr)?

**Q42 — Listening voice variety budget.**
ISSUE-099 has been deferred 3 times (round-3, round-7, round-8) for lack of
a budget decision. Three options at this point: (a) install VOICEVOX
multi-voice locally and re-render — free but 4-6 hr of integration; (b)
ElevenLabs free tier — 10K chars/month free, may not cover 47 items;
(c) recruit 2-4 native speakers via Indian Japanese-language teacher
network for 5-10 items each (community sourcing). Decision needed:
which lane?

**Q43 — Provenance-badge UI rollout strategy.**
IMP-116 ports the provenance badge from grammar to vocab + kanji. But
Q21 says "Show badge only if ≥10% native_reviewed per surface." Today
vocab + kanji are at 0% — shipping the data shape (IMP-117) without
content review (ISSUE-114) means the badge stays hidden. Decision needed:
ship data shape now (IMP-117) and let badge self-activate when
ISSUE-114 reaches threshold, OR bundle them as one batch?

**Q44 — Onboarding "your first 60 seconds" path.**
A brand-new user lands on the home page and sees five surface cards. No
guided "start here" path. The audit notes this as a potential improvement
but cannot decide whether to build a tutorial overlay (clutters the app),
a recommended-first-pattern page (low effort), or a curriculum mode
(out-of-scope for this cycle). Decision needed: which onboarding shape,
if any?

---

## Section 7: Anti-Items (don't do these)

**Mandatory entries for this depth-first cycle:**

- **Do NOT add new grammar patterns.** 178 already exceeds Bunpro's
  ~140 N5 deck; depth on the existing patterns is the higher-leverage
  move. (ISSUE-108, ISSUE-111 are the depth-on-existing equivalents.)
- **Do NOT add new vocabulary entries.** 1041 already exceeds the ~700
  official scope; depth on existing entries (translations, examples,
  collocations, register, counter, verb_class) is the leverage.
  (ISSUE-101..107 are the depth equivalents.)
- **Do NOT add new kanji.** 106 matches the canonical N5 set; width-
  additions outside the documented PRAGMATIC_N5_AUGMENTATION exceptions
  break JA-13 scope discipline.
- **Do NOT add new reading passages or listening drills.** Depth on
  the current 45+47 isn't yet at target bar (sentence-by-sentence
  footnotes, native-speaker audio, transcript timestamps). Width is
  premature.

**Strategic anti-items:**
- Do NOT try to match Bunpro's native-review depth at scale. Solo+AI
  build cannot match Bunpro's full-time-staff content team; instead,
  cite niche-N1 (Hindi-medium) and niche-N2 (privacy/offline) where
  Bunpro doesn't compete.
- Do NOT add gamification (streaks, XP, leaderboards). Runs counter to
  the privacy + adult-learner positioning of niche-N2.
- Do NOT add account/cloud sync. Breaks niche-N2 (privacy contract).
- Do NOT replace JLPT-N5 scope discipline with broad-coverage features.
  N5 scope discipline is what makes JLPTSuccess defensible vs general
  Japanese-learning apps.
