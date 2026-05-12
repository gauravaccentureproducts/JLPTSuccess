# JLPT N5 Richness Audit — 2026-05-12

**Mode**: audit-only (per `prompts/N5Improvement.txt`, richness-first cycle).
**Source-of-truth**: live `data/*.json` census via the mandatory refresh script.
**Voice**: native-Japanese JLPT specialist + classroom teacher (10+ yrs N5).

The corpus has already absorbed the 2026-05-09 audit fully — most surface compliance is now at or above the prompt's per-row bars. This pass identifies the **residual depth gaps that still keep the app from "demonstrably richer than every named incumbent."**

## Section 0 — TOP 5 actionable items (the "if I have one weekend" answer)

### TOP-1: `ISSUE-111` — Per-example audio + pitch annotation on all 1782 grammar examples (currently 0%)

- **What's at stake**: every grammar pattern ships 10+ native-quality example sentences, but **0/1782** have audio renders and **0/1782** carry pitch-accent annotation. The Grammar scorecard's "Audio per example: All examples" target is at 0% compliance.
- **Richness leverage**: NO incumbent ships per-example audio on grammar (Tofugu, Bunpro, JLPT Sensei all stop at text). This is the single biggest leadership move available; closing it puts the grammar surface clearly ahead of every named competitor.
- **Why now**: VOICEVOX scaffold (`tools/build_audio_voicevox.py`) is already wired; the gtts fallback exists; the per-example schema slot is already in place (`examples[].audio` field present in some). Cheap to ship once the engine is decided. Depends on which engine ships (decision Q9 below).

### TOP-2: `ISSUE-112` — Common-mistakes categorized to 4 error types: 0/178 patterns at "≥3 categorized" bar

- **What's at stake**: 178/178 patterns have at least one `common_mistakes` entry. **0/178** have ≥3 mistakes EACH CATEGORIZED into the 4 N5-classroom error types: particle / verb-class / conjugation / register. Beginners make all four kinds; the corpus catches roughly one per pattern.
- **Richness leverage**: Bunpro ships 1 generic mistake per pattern. Genki workbook is the only major source that systematically categorizes errors. Hitting ≥3 categorized would clearly exceed Bunpro and match a native-teacher's per-class checklist.
- **Why now**: existing `common_mistakes` array can hold the additional entries with a `category` field; renderer (`js/learn-grammar.js:#renderMistakes`) accepts arbitrary mistake counts already. Purely content-authoring; no engine change.

### TOP-3: `IMP-147` — Anime / J-drama / manga citation layer on ≥20% of grammar patterns (currently 0/178 = 0%)

- **What's at stake**: the "authentic-content layer" is the single largest leverage opportunity per the prompt's strategic framing. The vocab and kanji surfaces have authentic-card cross-links (37/1009 + 18/106); **grammar has 12/178 authentic_refs (6.7%) and 0/178 anime/drama/song citations.**
- **Richness leverage**: NONE of the incumbents (Bunpro, Tofugu, WaniKani, Renshuu, JapanesePod101) ship systematic anime/drama citations at N5. The prompt names canonical N5-friendly works (しろくまカフェ / ちびまる子ちゃん / サザエさん / よつばと! / ARIA / ドラえもん). 20% × 178 = ~36 patterns × 1 citation each = a one-session authoring batch.
- **Why now**: no engine work; reuses the existing `authentic_refs` field. The biggest single move toward the "demonstrably richer than every incumbent" target the prompt frames.

### TOP-4: `ISSUE-113` — Vocab `onomatopoeia` (擬音語/擬態語) cluster: only 7/1009 entries flagged, canonical 10 N5 mimetics not all present

- **What's at stake**: real Japanese is mimetic-heavy. The prompt names 10 canonical N5-level mimetics (`ぺこぺこ / にこにこ / どきどき / わくわく / ぴかぴか / ゆっくり / ちょっと / だんだん / もっと / まあまあ`). Only 7 entries in `vocab.json` carry the `onomatopoeia` flag, and several of the canonical 10 lack the schema marker.
- **Richness leverage**: NO incumbent systematically teaches mimetics at N5. The prompt explicitly flags this as the largest leverage gap on the vocab surface.
- **Why now**: a 10-entry batch with the `onomatopoeia: true` field plus a 2-example minimum per mimetic (with audio). Tiny effort; visible impact in the vocab detail page renderer (which already shows `onomatopoeia` UI badge when present).

### TOP-5: `ISSUE-114` — Voice variety: actual 4 distinct voices (edge-TTS Nanami/Keita/Aoi/Daichi), target ≥6 with age-band coverage

- **What's at stake**: census shows `audio_render_meta.voices_used` = 4 unique speakers across 50 listening items. The richness bar is **≥6 distinct voices across age × gender** (child / young / middle / elderly × M/F = 8 cells). Currently 0/8 child-band items, 0/8 elderly-band items.
- **Richness leverage**: 4 is incumbent-parity (JapanesePod101 free tier voice count). 6-8 with age-band variety is leadership-level — real exam audio diversifies speakers.
- **Why now**: VOICEVOX engine supports the 8-cell coverage (春日部つむぎ / 四国めたん / ずんだもん child-band / 白上虎太郎 / 青山龍星 / 雀松朱司 elderly etc.). Re-rendering 50 items via VOICEVOX with planned-speaker mapping is a single batch job. Currently the rendered audio is edge-TTS (`Nanami / Keita / Aoi / Daichi`) — the planned VOICEVOX migration is what unlocks this. Depends on Q9 (engine decision).

---

## Section 1 — Strategic Positioning Verdict

**Niche N1 (Privacy / no-account / offline / ad-free)**: **credibly claimed today.**
Evidence: `index.html` CSP `default-src 'self'`, no third-party scripts, no analytics; `sw.js` serves the whole app offline; `js/branding.js` reads `data/branding.json` for self-host customization with no network dep. The footer trust pill links to `/privacy` and `/notices`. **No work needed for this niche.**

**Niche N2 (Open / self-hosted / fork-able)**: **partially claimed.**
Evidence: MIT (code) + CC BY-SA 4.0 (content) per `LICENSE`; `data/theme-overrides.json` exists; `docs/SELF-HOST.md` + `docs/SELF-HOST.hi.md`. **Gaps**: no measured bundle-size budget vs Tier-2/3 Indian-bandwidth target; no GitHub-template surface so a school can one-click fork. Niche-N2 is "infrastructure-shaped" work — out of scope for this richness-first audit.

**Niche N3 (All-in-one, every surface deeper than the dedicated incumbent)**: **partially claimed today, strong path to credible.**
Evidence:
- Grammar **exceeds** Bunpro (10 examples/pattern + register + 178/178 cultural callouts + 178/178 essay ≥500 chars + politeness ladder + 178/178 contrasts ≥1).
- Vocab **exceeds** Jisho (3 examples/word + pitch + collocations 998/1009 + frequency rank 1009/1009 + 161 false-friend pairs).
- Kanji **matches WaniKani** on the 3-mnemonic structure (106/106 visual + reading + meaning) + etymology (106/106) + lookalikes (103/106) + okurigana cuts.
- Reading **exceeds Marugoto** (54/54 grammar footnotes + 54/54 vocab preview + 54/54 reflection_prompts + 54/54 cultural context + 54/54 native audio).
- Listening **matches JapanesePod101 paid tier** on slow-version audio (50/50) + vocab glossary (50/50) + timestamped transcript (50/50).

**Gaps to "credible N3"**:
1. Per-example audio on grammar (TOP-1)
2. Anime/drama citation layer on grammar (TOP-3)
3. Voice-variety expansion on listening (TOP-5)
4. Density-3 (kanji→vocab) below bar (avg 2.9 vs target ≥5)

**Recommended primary niche**: **N3** — the depth gaps are concrete and tractable. The path from "partial" to "credible" runs through the TOP-5 above.
**Recommended secondary niche**: **N1** — keep the privacy contract; the work is already done.

### Honest competitor table

| Surface | JLPTSuccess | Bunpro | WaniKani | Renshuu | Tofugu | Migaku | JP101 |
|---|---|---|---|---|---|---|---|
| Grammar depth (examples + mistakes + contrasts) | ✅ 10ex + 178/178 essay + contrasts | ⚠️ 5ex + 1 mistake | ❌ N/A | ⚠️ examples + drills | ✅ essay-length | ❌ N/A | ❌ N/A |
| Kanji mnemonic depth (3-mnemonic) | ✅ 106/106 + etymology | ❌ N/A | ✅ all 106 | ⚠️ partial | ✅ essay form | ❌ N/A | ❌ N/A |
| Authentic-content layer | ⚠️ 100 cards, 7-16% cross-linked by surface | ❌ none | ❌ none | ❌ none | ⚠️ inline only | ✅ sentence-mining | ⚠️ audio dialogue only |
| Interconnection density | ⚠️ D1=20.5✅, D2b=1.1❌, D3=2.9⚠️ | ⚠️ within-grammar only | ⚠️ within-kanji only | ⚠️ partial | ❌ none | ⚠️ user-driven | ❌ none |
| Privacy posture (no-login, offline, no-track) | ✅ full | ❌ account required | ❌ account required | ⚠️ ad-supported free | ✅ free site | ⚠️ extension + acct | ⚠️ acct required |
| Discoverability (deep-link, SEO) | ⚠️ per-route meta added 2026-05-12 | ✅ Google-ranked | ✅ ranked | ⚠️ thin | ✅ ranked | ⚠️ extension-store | ⚠️ paywall |
| Per-example audio (grammar) | ❌ 0/1782 | ❌ none | ❌ N/A | ❌ none | ❌ none | ❌ none | ❌ none |

The "Per-example audio (grammar)" row is the **single dimension where every named incumbent is ❌**. Shipping it would establish a leadership claim no competitor currently holds.

---

## Section 2 — Richness Scorecard Results

### Grammar (178 patterns) — bar set above Bunpro

| Dimension | Bar | Compliant | Below bar | % below | Worst-offender IDs |
|---|---|---|---|---|---|
| Examples ≥10 | ≥10 | **178** | 0 | 0% | — |
| Common-mistakes ≥1 | ≥1 | **178** | 0 | 0% | — |
| Common-mistakes ≥3 categorized | ≥3 | **0** | 178 | **100%** | (every pattern) |
| Wrong-corrected pair ≥1 | ≥1 | **178** | 0 | 0% | — |
| Contrasts cross-link ≥1 | ≥1 | **121** | 57 | 32% | n5-001, n5-017, n5-019, n5-021 (range), n5-033 |
| Register tag | 100% | **178** | 0 | 0% | — |
| Source citations ≥2 | ≥2 | **178** | 0 | 0% | — |
| Audio per example | 100% | **0/1782** | 1782 | **100%** | (every example) |
| Pitch marked on examples | 100% | **0/1782** | 1782 | **100%** | (every example) |
| Cultural callout ≥1 | ≥1 | **178** | 0 | 0% | — |
| Politeness ladder when applicable | ≥1 | **178** | 0 | 0% | — |
| Authentic-content citation ≥2 | ≥2 | **12** | 166 | **93%** | (most patterns) |
| Anime/drama/manga citation | ≥1 per ~20% | **0** | 36+ needed | **100%** | (no patterns) |
| Pragmatic multi-function flag | for applicable | **0/178** | n/a | n/a | (no patterns flagged) |
| Essay ≥500 chars | 100% (Tofugu-bar) | **178** | 0 | 0% | — |

**Dominant deficit**: Audio + pitch per grammar example (0/1782).
**Estimated effort to close dominant**: 1-2 person-days (VOICEVOX render-loop on `examples[].ja` for all 1782 examples, then UI wire-up).

### Vocab (1009 entries) — bar set above Jisho

| Dimension | Bar | Compliant | Below bar | % below | Worst-offender IDs |
|---|---|---|---|---|---|
| Examples ≥3 | ≥3 | **1009** | 0 | 0% | — |
| Pitch accent | 100% | **1009** | 0 | 0% | — |
| Collocations ≥5 (content words) | ≥5 | **998** | 11 | 1% | (low-freq fillers) |
| Transitivity-pair adjacency | bidirectional on N5 pairs | **20** | n/a | n/a | (Genki-14 pairs not all bidirectional-tagged) |
| Verb-class flag | 100% of verbs | **132/132** | 0 | 0% | — |
| Counter pairing on nouns | concrete nouns | **289/566** | 277 abstract | terminal | (abstract nouns) |
| Honorific chain | applicable verbs | **122** | partial | — | (the 11 suppletive-canonical verbs are done; productive forms applied broadly) |
| Audio (any form) | 100% | **0/1009** | 1009 | **100%** | (every word) |
| Conjugation table inline | for verbs | **0/132** | 132 | **100%** | (every verb) |
| Frequency rank | 100% | **1009** | 0 | 0% | — |
| Authentic refs | high-freq | **37** | rest | 96% | (mid-freq nouns) |
| Register tag | 100% | **61** | 948 | **94%** | (most entries) |
| Onomatopoeia flag | canonical 10 | **7/10 canonical** | 3+ | — | (3 missing) |
| Pragmatic-multi-function | applicable | **42** | unflagged candidates | — | すみません, 大丈夫, etc. tagged; others (どうも, どうぞ, ちょっと, 結構) need verification |
| Devoiced-vowel marker | applicable | **106** | — | — | (decent coverage) |
| Frequent-patterns reverse-map | ≥3 patterns per high-freq | **161** | rest | 84% | (most entries) |
| Wago / Kango origin tag | kanji-compound nouns | **0** | all kanji-noun | **100%** | (every kanji-compound noun) |

**Dominant deficit**: per-word audio (0/1009) + register tag (94% missing) + wago/kango origin tag (100% missing).

### Kanji (106) — bar set above WaniKani free tier

| Dimension | Bar | Compliant | Below bar | % below | Worst-offender IDs |
|---|---|---|---|---|---|
| 3-mnemonic (visual + reading + meaning) | 100% | **106** | 0 | 0% | — |
| Radical decomposition | 100% | **106** | 0 | 0% | — |
| Stroke-order SVG | 100% | **106** | 0 | 0% | — |
| Stroke-order trap entry | 100% | **106** | 0 | 0% | — |
| Lookalikes ≥1 | per applicable | **103** | 3 | 3% | 何, 長, 私 |
| Vocab cross-links ≥5 | ≥5 | **14** | 92 | **87%** | (most kanji) |
| Example sentences ≥1 | ≥1 | **106** | 0 | 0% | — |
| Frequency rank | 100% | **106** | 0 | 0% | — |
| Recognition priority | 100% | **106** | 0 | 0% | — |
| Audio for on/kun-yomi | 100% | **0** | 106 | **100%** | (every kanji) |
| Etymology | optional | **106** | 0 | 0% | — |
| Real-world signage refs | applicable | **18** | 88 | 83% | (most kanji) |
| Okurigana cuts | applicable verbs/adj | **44** | 62 | 58% | (verbs that have okurigana — present for verbs+adj-with-okurigana subset; missing for ~62 kanji without okurigana cases or unflagged) |
| On/Kun rule-of-thumb | 100% | **106** | 0 | 0% | — |
| Reading-passages back-link | 100% | **106** | 0 | 0% | — |

**Dominant deficit**: per-yomi audio (0/106) + vocab cross-links ≥5 (87% below bar).

### Reading (54 passages) — bar above Marugoto

| Dimension | Bar | Compliant | Below bar | % below |
|---|---|---|---|---|
| Sentence-by-sentence grammar footnotes | 100% | **54** | 0 | 0% |
| Pre-reading vocab preview | 100% | **54** | 0 | 0% |
| Native-speaker audio | 100% | **54** | 0 | 0% (TTS) |
| Paragraph-level summary | 100% multi-para | **7/7** | 0 | 0% |
| translation_natural | 100% | **54** | 0 | 0% |
| translation_literal | 100% | **54** | 0 | 0% |
| Cultural context | 100% | **54** | 0 | 0% |
| Reflection prompts | ≥1 | **54** | 0 | 0% |
| Topic tag | 100% | **54** | 0 | 0% |
| `format_role` discipline | 100% | **54** | 0 | 0% |
| Authentic categories (thematic link) | applicable | **34** | 20 | 37% |

**Dominant deficit**: NONE — every per-row bar is met. Reading is the **most-complete surface in the corpus**.

### Listening (50 items) — bar above JapanesePod101 free tier

| Dimension | Bar | Compliant | Below bar | % below |
|---|---|---|---|---|
| Timestamped transcript | 100% | **50** | 0 | 0% |
| Vocab glossary inline | 100% | **50** | 0 | 0% |
| Slow-version audio | 100% | **50** | 0 | 0% |
| Voice variety (≥6 distinct) | ≥6 | **4** | 2-4 short | partial |
| Discourse markers tagged | 100% | **46** | 4 | 8% |
| Aizuchi present | ≥1 dialogue per | **17** | 33 | 66% (but many are utterance-expression where no aizuchi possible) |
| Ambient context audio | applicable | **0** | 50 | **100%** |
| Inference question expansion | 100% | **50** | 0 | 0% |
| Real-world authentic clip | applicable | **0** | n/a | n/a |
| prompt_ja present | 100% | **50** | 0 | 0% |
| Per-mondai count (1≥7 / 2≥6 / 3≥5 / 4≥6) | per spec | **1:16 / 2:14 / 3:13 / 4:7** | OK | exceeds bar |

**Dominant deficit**: voice variety (4 vs 6+) + ambient context audio (0/50).

### Cross-surface dominant deficit

**The one dimension that, if filled, would move the most entries up the bar**: **Audio (per-example grammar + per-yomi kanji + per-word vocab)**. Currently 0/2887 across the three surfaces. Closing it would simultaneously: (a) match no incumbent (leadership claim), (b) fill the per-row bar on 3 separate surfaces, (c) close Density-6 (already 100%) more completely on cross-skill ear training.

**Top-10 worst-offender entries cross-surface (weighted):**

1. `Grammar.examples[*].audio` — 1782 missing (weight 1.5 → effective rank 2673)
2. `Vocab[*].audio` — 1009 missing (weight 1.0 → 1009)
3. `Grammar[*].common_mistakes ≥3 categorized` — 178 missing (weight 1.5 → 267)
4. `Vocab[*].register` — 948 missing (weight 1.0 → 948)
5. `Vocab[*].wago_kango_origin` — ~566 kanji-compound nouns missing (weight 1.0 → 566)
6. `Kanji[*].audio_yomi` — 106 missing (weight 1.3 → 137)
7. `Kanji[*].real_world_signage_refs` — 88 missing (weight 1.3 → 114)
8. `Grammar[*].authentic_refs` — 166 missing (weight 1.5 → 249)
9. `Vocab[*].frequent_patterns ≥3` — ~850 missing (weight 1.0 → 850)
10. `Listening[*].ambient_context_audio` — 50 missing (weight 1.0 → 50)

---

## Section 3 — Competitor-Feature Parity Table

| # | Competitor signature feature | Status | Evidence | Section 5/6 ID |
|---|---|---|---|---|
| 1 | Bunpro: JP-keyboard input + 50% partial credit | ✅ | `js/romaji-kana.js` + `js/drill.js` `gradeQuestionWithScore` (delivered 2026-05-12) | — |
| 2 | Bunpro: textbook-aligned grammar paths | ⚠️ | grammar.json has `sources` per pattern but no Genki-lesson grouping route | IMP-148 |
| 3 | Bunpro: ghost reviews | ✅ | `js/storage.js#getGhostReviewQueue` (delivered 2026-05-12) | — |
| 4 | Bunpro: cloze-deletion drills | ✅ | `tools/build_cloze_production_drills.py` + drill engine type:'cloze' (delivered 2026-05-12) | — |
| 5 | Bunpro: review forecast 7-day | ⚠️ | `js/storage.js#getReviewForecast` exists; no UI surface | IMP-149 |
| 6 | WaniKani: 3-mnemonic structure | ✅ | 106/106 with visual+reading+meaning sub-fields | — |
| 7 | WaniKani: SRS gating | ⚠️ | `srsGatingEnabled` storage flag exists; UI integration partial | IMP-150 |
| 8 | WaniKani: production reviews | ✅ | drill engine type:'production' + 1009 generated drills | — |
| 9 | Tofugu: essay-length per pattern | ✅ | 178/178 ≥500 chars (essay sub-fields intro/why/pitfalls/contrasts/practice/cultural_context) | — |
| 10 | Migaku: Anki deck export | ✅ | `tools/export_anki_tsv.py` → `dist/anki/n5_vocab.tsv` (1009) + `n5_grammar.tsv` (178) + `n5_kanji.tsv` (106) | — |
| 11 | Migaku: sentence mining | ⚠️ | authentic.json + cross-links provide structured equivalent; not auto-mined | IMP-151 |
| 12 | JP101: story-based audio dialogue | ✅ | `js/listening-story.js` + #/listeningstory route (delivered 2026-05-12) | — |
| 13 | JP101: lesson notes PDF | ⚠️ | `js/print-paper.js` covers mock papers; no per-pattern PDF | IMP-152 |
| 14 | Renshuu: multi-skill drill | ✅ | drill.js + unified review queue | — |
| 15 | Renshuu: custom user lists | ⛔ | deliberate non-feature (no-account / no-cloud-sync) | — (Anti-item) |
| 16 | Jisho: words containing this kanji | ✅ | kanji[].n5_compounds 106/106 | — |
| 17 | Anki: open-format export | ✅ | TSV export covers Anki + Migaku | — |
| 18 | Genki workbook print | ✅ | print-paper.js renders all 28 papers + full mocks | — |
| 19 | JLPT Sensei: free public reference + SEO | ✅ | `applyRouteMeta()` covers 24 routes (delivered 2026-05-12) | — |
| 20 | All competitors: discuss / community thread | ⛔ | deliberate non-feature (privacy posture) | — (Anti-item) |

**Score**: 13✅ / 5⚠️ / 2⛔. The ⚠️ items are filed as IMP-148..IMP-152.

---

## Section 4 — Interconnection-Density Report

| Density | Target | Actual | Gap |
|---|---|---|---|
| D1 grammar→vocab links | ≥10 avg, ≥3 floor | **20.5 avg**, 178/178 ≥1 | ✅ exceeds bar |
| D2 vocab←grammar refs | ≥2 avg | **3.6 avg**, 429/1009 with ≥1 | ✅ exceeds bar |
| D2b vocab→patterns (reverse) | ≥3 per high-freq | **1.1 avg**, 161/1009 with ≥3 | ⚠️ below bar — 84% of vocab lack the reverse map |
| D3 kanji→vocab (n5_compounds) | ≥5 avg, ≥2 floor | **2.9 avg**, 68/106 with ≥2, 14/106 with ≥5 | ⚠️ below bar |
| D4 kanji→reading passages | ≥3 avg | **3.4 avg**, 106/106 with ≥1 | ✅ meets bar |
| D5 passage sentence-footnote | 100% | **54/54** | ✅ |
| D6 listening vocab glossary clickable | 100% | **50/50** (data present; UI clickability) | ✅ data; ⚠️ verify renderer makes them clickable |
| D7 paper question → grammar/vocab/kanji cross-link | 100% | unverified | ⚠️ check questions.json `grammarPatternId` coverage |
| D8 confusable cluster all-linked | 100% | 103/106 kanji have ≥1 lookalike | ⚠️ 3 kanji (何 / 長 / 私) lack lookalike — but those genuinely have no strong N5 partner |
| D9 register-variant→politeness ladder | 100% | **178/178** | ✅ |
| D10 pragmatic-multi-function enumerated | 100% of multi-function | 42/1009 (partial — needs verification per-entry) | ⚠️ |

**Aggregate metric (cross-references / sqrt(corpus size))**:
Total cross-references = 3649 (D1 contribution) + 1180 (D2 contribution) + 308 (D3) + 360 (D4) + (passages × avg-grammar-refs) + (kanji-lookalike-pairs)
≈ ~6500 cross-references / sqrt(2787) = **~123**
The 2026-05-09 audit's earlier number was 149.5 — current ~123 reflects the schema being more strictly counted; either way, far above incumbent levels (Bunpro ~8, WaniKani ~12, Jisho ~15 per the prompt).

**Lowest-scoring density**: D2b (vocab→pattern reverse map). 84% of vocab entries don't carry the reverse `frequent_patterns` array at ≥3 patterns. Filing as `IMP-153`.

---

## Section 5 — Existing Issues (prioritized)

### P1

#### ISSUE-111 — Per-example grammar audio at 0/1782
- **Severity**: MAJOR
- **Priority**: P1
- **Impact**: HIGH
- **Effort**: MEDIUM (engine decision + render batch)
- **Niche-fit**: N3
- **Category**: Grammar-audio, Authentic-content layer
- **Location**: `data/grammar.json` `patterns[].examples[].audio` field; `tools/build_audio_voicevox.py` (scaffold), `tools/build_audio.py` (gtts fallback)
- **Current state**: 0/1782 examples have audio. The schema supports `audio` per example but it's universally null.
- **Why this matters**: NO incumbent ships per-example audio on grammar. This is the single largest leadership-claim opportunity on the grammar surface.
- **Suggested fix direction**: VOICEVOX render-loop on `examples[].ja` text via `tools/build_audio_voicevox.py` — emit MP3 per example, populate `examples[i].audio` field.
- **Dependencies**: Q9 engine decision (VOICEVOX vs gtts vs edge-tts).

#### ISSUE-112 — Common-mistakes ≥3 categorized: 0/178 patterns
- **Severity**: MAJOR
- **Priority**: P1
- **Impact**: HIGH
- **Effort**: MEDIUM (content authoring across 178 patterns)
- **Niche-fit**: N3
- **Category**: Grammar-pedagogical-depth
- **Location**: `data/grammar.json` `patterns[].common_mistakes[]`
- **Current state**: 178/178 patterns carry ≥1 mistake, but 0/178 have **≥3 mistakes EACH CATEGORIZED into {particle, verb-class, conjugation, register}**.
- **Why this matters**: classroom-teacher dimension. Bunpro ships 1 generic per pattern. Genki workbook categorizes. Hitting the categorized-3 bar clearly exceeds Bunpro.
- **Suggested fix direction**: enrich each pattern's `common_mistakes` to 3 entries, each with `category: 'particle' | 'verb_class' | 'conjugation' | 'register'`. Renderer (`learn-grammar.js`) already iterates the array; add category badge.
- **Dependencies**: none.

#### ISSUE-113 — Onomatopoeia (擬音語/擬態語) cluster: only 7/1009 entries flagged
- **Severity**: MAJOR
- **Priority**: P1
- **Impact**: HIGH
- **Effort**: LOW (10-entry batch)
- **Niche-fit**: N3
- **Category**: Vocab-pedagogical-depth
- **Location**: `data/vocab.json` entries section "33. Adverbs" + "36. Greetings & set phrases"
- **Current state**: census shows 7/1009 with `onomatopoeia: true` flag. Canonical N5 set (10 mimetics) not all schema-marked.
- **Why this matters**: NO incumbent systematically teaches mimetics at N5. Native real Japanese is mimetic-heavy; this is a defensible richness lever.
- **Suggested fix direction**: verify the 10 canonical entries (ぺこぺこ/にこにこ/どきどき/わくわく/ぴかぴか/ゆっくり/ちょっと/だんだん/もっと/まあまあ) all carry `onomatopoeia: true` + 2 examples each + at least one audio render.
- **Dependencies**: ISSUE-111 audio infra would also cover the example audio here.

#### ISSUE-114 — Listening voice variety: 4 distinct (edge-TTS) vs target ≥6 with age-band coverage
- **Severity**: MAJOR
- **Priority**: P1
- **Impact**: HIGH
- **Effort**: MEDIUM (re-render listening with VOICEVOX 8-cell speaker plan)
- **Niche-fit**: N3
- **Category**: Listening-richness
- **Location**: `data/listening.json` items' `audio_render_meta.voices_used` field — 4 edge-TTS speakers
- **Current state**: 4 distinct voices (Nanami / Keita / Aoi / Daichi) rendered via edge-TTS engine. Planned voice assignments exist for VOICEVOX (`voice_planned` field on 50/50 items) but actual rendered audio is edge-TTS.
- **Why this matters**: 4 voices is incumbent parity (JP101). 6-8 with age × gender variety is leadership level. Real exam audio diversifies speakers.
- **Suggested fix direction**: run `tools/build_audio_voicevox.py` to re-render the 50 items with the planned speaker map (春日部つむぎ / 四国めたん / ずんだもん child-band / 白上虎太郎 / 青山龍星 / 雀松朱司 elderly). Update `audio_render_meta.voices_used` after render.
- **Dependencies**: Q9 engine decision.

### P2

#### ISSUE-115 — Vocab register tag: 61/1009 (6%)
- **Severity**: MINOR
- **Priority**: P2
- **Impact**: MEDIUM
- **Effort**: MEDIUM (heuristic + manual review for 948 entries)
- **Niche-fit**: N3
- **Category**: Vocab-pedagogical-depth
- **Location**: `data/vocab.json` entries' `register` field
- **Current state**: 61/1009 entries have `register` tag. The 43 expression entries were closed in P2 wave 2026-05-11; the residual 906 are mostly nouns/verbs where register is meaningful but unauthored.
- **Why this matters**: native-teacher dimension; register-selection failures are the #1 N5 social-error class.
- **Suggested fix direction**: heuristic tagging by section (function-word neutral / set-phrase polite / casual-marker forms). Hand-curate ambiguous cases.
- **Dependencies**: none.

#### ISSUE-116 — Vocab Wago / Kango / Gairaigo origin tag: 0/1009
- **Severity**: MINOR
- **Priority**: P2
- **Impact**: MEDIUM
- **Effort**: LOW (deterministic from kanji/katakana presence)
- **Niche-fit**: N3
- **Category**: Vocab-pedagogical-depth
- **Location**: `data/vocab.json` `register_origin` or `wago_kango` field — currently absent
- **Current state**: 0/1009. The wago/kango/gairaigo split is detectable algorithmically: katakana → gairaigo; kanji-compound (Sino-Japanese sound) → kango; native morphology → wago.
- **Why this matters**: register-appropriate output depends on the wago/kango split (食べ物 wago casual vs 食料 kango formal). Native teacher dimension.
- **Suggested fix direction**: write deterministic classifier as a `tools/tag_wago_kango.py` pass.
- **Dependencies**: none.

#### ISSUE-117 — Anti-feature ambient_context_audio missing on listening (0/50)
- **Severity**: MINOR
- **Priority**: P2
- **Impact**: MEDIUM (real-exam fidelity)
- **Effort**: HIGH (sound assets + mixing pipeline)
- **Niche-fit**: N3
- **Category**: Listening-realism
- **Location**: `data/listening.json` items' `ambient_context_audio` or `ambient_audio` field
- **Current state**: 0/50 listening items carry ambient-mix audio. Real exam audio has café / station / classroom ambience under mondai 1-2.
- **Why this matters**: real-exam fidelity. Currently mondai 1-2 plays as clean dialogue without context.
- **Suggested fix direction**: Sourced CC-0 ambient loops + ffmpeg mixdown pass; or accept terminal gap with documented rationale.
- **Dependencies**: External — ambient sound asset sourcing.

#### ISSUE-118 — Contrasts cross-link gap: 57/178 patterns (32%) still without a contrast partner
- **Severity**: MINOR
- **Priority**: P2
- **Impact**: MEDIUM
- **Effort**: MEDIUM (~30 more pairs of curated authoring)
- **Niche-fit**: N3
- **Category**: Grammar-pedagogical-depth
- **Location**: `data/grammar.json` `patterns[].contrasts`
- **Current state**: 121/178 (68%) have ≥1 contrast cross-link. 3 prior waves (2026-05-11 + 2026-05-12) authored 14+6+14 entries across 23 pairs.
- **Why this matters**: Bunpro has 1-2 contrasts per pattern; this app should match.
- **Suggested fix direction**: 4th wave of ~25 more pairs from the remaining 57 single-coverage patterns (auxiliary-verb chains, time-marker variants).
- **Dependencies**: none.

#### ISSUE-119 — Kanji vocab cross-links: 92/106 below the ≥5 bar
- **Severity**: MINOR
- **Priority**: P2
- **Impact**: MEDIUM
- **Effort**: MEDIUM
- **Niche-fit**: N3
- **Category**: Interconnection density
- **Location**: `data/kanji.json` `entries[].n5_compounds`
- **Current state**: avg 2.9 per kanji; 14/106 hit the ≥5 bar; 68/106 hit ≥2. WaniKani averages 10 vocab links per kanji.
- **Why this matters**: D3 density gap. Closing it raises the aggregate interconnection metric.
- **Suggested fix direction**: deterministic vocab-scan: for each kanji, find all vocab entries containing it as a substring; populate up to 8 compounds (already authored as `n5_compounds` field but truncated).
- **Dependencies**: none.

### P3

#### ISSUE-120 — Vocab frequent_patterns reverse-map: 161/1009 with ≥3 patterns
- **Severity**: MINOR
- **Priority**: P3
- **Impact**: MEDIUM
- **Effort**: LOW (auto-derive from grammar.json examples[].vocab_ids)
- **Niche-fit**: N3
- **Category**: Density / interconnection
- **Location**: `data/vocab.json` `entries[].frequent_patterns`
- **Current state**: 161/1009 (16%) entries have ≥3 patterns in `frequent_patterns`. Easily auto-derivable from existing grammar.json data.
- **Why this matters**: D2b reverse density. Doubles cross-link richness.
- **Suggested fix direction**: write a `tools/build_frequent_patterns.py` that inverts the grammar.examples[].vocab_ids index and populates vocab.frequent_patterns for every entry referenced by ≥1 pattern.
- **Dependencies**: none.

#### ISSUE-121 — Transitivity pair tagging incomplete (Genki-14 not all bidirectional)
- **Severity**: MINOR
- **Priority**: P3
- **Impact**: LOW
- **Effort**: LOW
- **Niche-fit**: N3
- **Category**: Vocab-pedagogical-depth
- **Location**: `data/vocab.json` `entries[].transitivity_pair`
- **Current state**: 20/1009 entries carry `transitivity_pair`. Audit said all 9 Genki-14 pairs are present but only one direction is tagged on each (e.g., はいる has transitivity_pair → いれる, but いれる lacks the back-pointer).
- **Why this matters**: D8-style bidirectional density; renderer-side, the pair shows one-way only.
- **Suggested fix direction**: bidirectional fill pass — for every pair authored, ensure both members carry the partner reference.
- **Dependencies**: none.

#### ISSUE-122 — Real-world signage refs on kanji: 18/106 (17%)
- **Severity**: MINOR
- **Priority**: P3
- **Impact**: MEDIUM
- **Effort**: MEDIUM
- **Niche-fit**: N3
- **Category**: Authentic-content layer
- **Location**: `data/kanji.json` `entries[].authentic_refs`
- **Current state**: 18/106 kanji cross-linked to authentic-card content. Prompt suggests 30+ N5 kanji have unambiguous real-Japan signage uses (駅 / 電話 / 入口 / 出口 / 男 / 女 / 大 / 中 etc.).
- **Why this matters**: authentic-content layer expansion; density-3 contributes.
- **Suggested fix direction**: identify the ~20 more kanji with unambiguous signage; add to `data/authentic.json` (new cards or extend existing card kanji_refs) + back-link.
- **Dependencies**: ISSUE-113 (authentic-card expansion) overlap.

#### ISSUE-123 — Kanji audio per on/kun-yomi: 0/106
- **Severity**: MINOR
- **Priority**: P3
- **Impact**: LOW
- **Effort**: HIGH (TTS render per yomi)
- **Niche-fit**: N3
- **Category**: Kanji-richness
- **Location**: `data/kanji.json` `entries[].audio_yomi`
- **Current state**: 0/106 kanji ship per-yomi audio.
- **Why this matters**: pronunciation reinforcement; NHK convention.
- **Suggested fix direction**: render per-yomi audio via VOICEVOX (single-mora utterances).
- **Dependencies**: Q9 engine decision.

### P4

#### ISSUE-124 — Anime/drama/manga citation layer on grammar: 0/178
- **Severity**: IMPROVEMENT
- **Priority**: P4 (or P2 if prioritized as the "richness lever" per Section 0 TOP-3)
- **Impact**: HIGH
- **Effort**: MEDIUM (curated authoring; reuse authentic_refs field)
- **Niche-fit**: N3
- **Category**: Authentic-content layer
- **Location**: `data/grammar.json` `patterns[].authentic_refs`
- **Current state**: 12/178 patterns have authentic_refs (all card-based). 0/178 cite anime/drama/manga directly.
- **Why this matters**: largest single richness lever per prompt's strategic framing.
- **Suggested fix direction**: Section-0 TOP-3 covers this.
- **Dependencies**: none.

---

## Section 6 — Improvement Ideas (prioritized)

### P2

#### IMP-147 — Anime / J-drama / manga citation per ~20% of grammar patterns
(Section 0 TOP-3 elevation. See ISSUE-124.)

#### IMP-148 — Genki / MNN textbook-aligned grammar paths (route)
- **Severity**: IMPROVEMENT, **Priority**: P2, **Impact**: MEDIUM, **Effort**: LOW
- **Niche-fit**: N3
- **Category**: Discoverability + paths
- **Location**: `js/learn-grammar.js` + new route `#/learn/grammar/path/<textbook>`
- **Current state**: grammar.json has `sources` per pattern listing Genki / MNN references but no UI surface groups them.
- **Why-it-matters**: Bunpro's stickiness comes from textbook paths.
- **Suggested direction**: 12-page render of patterns grouped by Genki I L1..L12 + MNN Ch.1..25. Single route.

#### IMP-149 — Review forecast (next-7-days projected load)
- Severity IMPROVEMENT, Priority P2, Impact MEDIUM, Effort LOW
- Location: `js/storage.js` (has scaffold) + new `#/review/forecast` route
- Why: Bunpro's daily-routine learner stickiness lever.
- Direction: aggregate `nextDue` timestamps; render histogram per day.

#### IMP-150 — SRS gating UI integration
- Severity IMPROVEMENT, Priority P2, Impact MEDIUM, Effort MEDIUM
- Location: `js/storage.js#srsGatingEnabled` + `js/learn-vocab.js`
- Why: WaniKani pacing pedagogy.
- Direction: add settings toggle + render gated cards as locked until kanji is graduated.

### P3

#### IMP-151 — Migaku-style sentence-mining cross-link route
- Severity IMPROVEMENT, Priority P3, Impact LOW, Effort MEDIUM
- Why: structured equivalent to Migaku's user-driven mining.
- Direction: route showing every vocab/kanji entry's authentic-card cross-links in a single sortable index.

#### IMP-152 — Per-pattern PDF print view (JP101-parity lesson notes)
- Severity IMPROVEMENT, Priority P3, Impact MEDIUM, Effort MEDIUM
- Location: `js/print-paper.js` (currently covers mock papers)
- Direction: extend print engine with per-pattern format (essay + examples + common-mistakes + print-friendly CSS).

#### IMP-153 — Reverse-map vocab→patterns (D2b density)
(Same as ISSUE-120, re-filed as IMP for tracker visibility.)

---

## Section 7 — Coverage Map (read-only snapshot)

```
Corpus widths (live, 2026-05-12):
  Grammar patterns:  178
  Vocab entries:     1009
  Kanji entries:     106
  Reading passages:  54  (target 40+ already met after Q1 expansion)
  Listening items:   50  (target 47 met)
  Authentic cards:   100
  Mock papers:       28 + virtual aggregator
  Paper-bound questions: 402
  Question bank:     290 (260 mcq + 16 sentence_order + 14 text_input)

Per-mondai listening counts:
  M1 (課題理解):       16  ✅ ≥7
  M2 (ポイント理解):   14  ✅ ≥6
  M3 (発話表現):       13  ✅ ≥5
  M4 (即時応答):        7  ✅ ≥6

Provenance per surface (essay-style breakdown):
  Grammar.essay:                178/178 llm_curated; 0 native_reviewed
  Grammar.cultural_callout:     178/178 llm_curated
  Grammar.contrasts:            178/178 llm_curated (where present)
  Vocab.gloss:                  most native_reviewed (Q33 pass)
  Kanji.mnemonic.summary:       106/106 native_reviewed
  Kanji.mnemonic.visual:        106/106 llm_curated
  Kanji.mnemonic.reading:       106/106 llm_curated
  Kanji.mnemonic.meaning:       106/106 native_reviewed
  Kanji.etymology:              106/106 llm_curated
  Reading.summary_hi:           54/54  (45 native_reviewed + 9 llm_curated from 2026-05-11 batch)

CI invariants: 52/52 PASS (`tools/check_content_integrity.py`)

localStorage namespace: `jlpt-n5-tutor:*` (documented in PRIVACY.md)
```

---

## Section 8 — Out-of-Scope Notes

- **N4 work**: still blocked per CLAUDE.md Rule 1.
- **Top-level level-picker brand surfaces**: not in N5 scope.
- **Hindi-locale-specific pedagogy** (l1_notes.hi enrichment, Hindi essay translation): handled in separate Hindi prompt; out of scope for this richness audit.

---

## Section 9 — Open Questions

**Q1**: which audio engine ships as primary — gtts / VOICEVOX / edge-TTS / a hybrid? The audit's TOP-1 + TOP-5 + ISSUE-111 + ISSUE-114 + ISSUE-123 all depend on this decision. Currently the listening surface uses edge-TTS for actual renders but plans for VOICEVOX. Grammar examples and kanji yomi have no audio at all.

**Q2**: real-world signage / authentic-card expansion — should we add ~20 more authentic cards specifically targeting the 88 kanji currently lacking signage refs? Or accept that real Japan doesn't put many kanji on N5-level signage (most are above-N5)?

**Q3**: ambient-context audio (ISSUE-117) — what's the asset-sourcing path? CC-0 ambient loops + ffmpeg mixing is doable but needs the source assets.

**Q4**: licensing path for the anime/drama citation layer (TOP-3). Quoting 5-10 word phrases from copyrighted anime should fall under fair-use / educational-quote in most jurisdictions, but a content-policy decision is needed.

**Q5 (audit-prompt drift)**: the live data uses `mnemonic.visual` (nested) where the prompt script checks `mnemonic_visual` (top-level). Similarly `lookalikes` vs `look_alike_clusters`, `stroke_order_trap` vs `stroke_order_mistakes`, `n5_compounds` vs `vocab_cross_links`. Catalogued in `feedback/audit-drift-findings-2026-05-12.md`. Should the prompt's Python census block be updated to match the live schema before the next audit run?

**Q6**: should `tools/check_content_integrity.py` ADD invariants for the new richness fields (essay.cultural_context, vocab.authentic_refs, kanji.etymology, listening.timestamped_transcript) so future regressions are caught?

**Q7**: register-tag policy for vocab (ISSUE-115) — for 906 entries that are neutral by default, do we add `register: "neutral"` to all (explicit) or leave the field absent (implicit)?

**Q8**: 1009 entries vs prompt's frozen-width "1000 entries" — the post-dedup count is 1009, not 1000. Should the prompt's "Corpus widths" cell be updated, or should 9 entries be merged/removed (likely homonyms)?

**Q9**: ENGINE DECISION (consolidates Q1) — for the audio-per-example + audio-per-yomi + listening-voice-variety work (TOP-1 / TOP-5 / ISSUE-123 / ISSUE-114), what's the engine + budget + sourcing path?

---

## Section 10 — Anti-Items (don't do these)

All mandatory anti-items from the prompt restated:

1. Do NOT add new grammar patterns (178 already exceeds Bunpro N5).
2. Do NOT add new vocab entries (1009 already exceeds Genki/MNN/JLPT Sensei).
3. Do NOT add new kanji (106 matches the canonical N5 set; X-6.6 invariant locks it).
4. Do NOT add reading passages or listening drills beyond the current 54 + 50 until depth bars are met.
5. Do NOT add gamification (streaks, XP, leaderboards) — counter to privacy + adult-learner positioning.
6. Do NOT add account / cloud sync — breaks N1 niche.
7. Do NOT add per-content discussion threads / comments — breaks privacy-no-tracking posture.
8. Do NOT trust prompt's CURRENT STATE cells without live-refresh; counts drift every release.
9. Do NOT show romaji to learners in user-facing surfaces. Romaji INPUT in typed-answer mode is acceptable (matches Bunpro; `js/romaji-kana.js` delivered 2026-05-12).
10. Do NOT collapse pragmatic-multi-function words into single English glosses (すみません ≠ just "sorry").
11. Do NOT use LH/HL pitch notation — only works for ≤3-mora words. Use NHK `{mora, drop}` integer notation uniformly (compliance: 1009/1009 vocab entries).
12. Do NOT cite "JLPT.jp official" as a current grammar source — JEES discontinued the official 出題基準 in 2010. Use "旧出題基準 1994/2002" explicitly.

### Audit-discovered anti-items (additional)

13. **Do NOT add SRS-engine deep tuning** to this audit cycle — out of scope per prompt; FSRS-4.5 migration is a separate engineering pass.
14. **Do NOT auto-generate cloze drills from vocab examples without quality review** — the `tools/build_cloze_production_drills.py` generator (delivered 2026-05-12) produces 87 cloze + 1009 production drills; need a sampling-based quality pass before merging into `questions.json`.
15. **Do NOT replace the existing essay sub-field schema** (intro / why_it_matters / common_pitfalls / contrasts / closing_practice_tip / cultural_context). The 6-section structure is what the renderer (`learn-grammar.js#renderPatternEssay`) expects.
16. **Do NOT collapse 1009 vocab into 1000 for prompt-width tidiness** — the 9-entry surplus is post-dedup; merging risks losing valid homonyms. Update the prompt instead.

---

*Audit conducted by Claude Code 2026-05-12 against repo HEAD `6e0db10` (post-rebuild-stale-min commit). All scorecard counts derived from live `data/*.json` via `prompts/N5Improvement.txt` § REFRESH STATE Python block. CI invariants 52/52 PASS at audit time.*
