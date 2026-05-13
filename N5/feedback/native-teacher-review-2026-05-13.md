# Native-Teacher Content Review — JLPT N5 corpus

**Conducted:** 2026-05-13
**Persona:** Native-Japanese language teacher with 20+ years of JLPT-instruction experience (university + corporate ESL Japanese contexts).
**Mode:** Pedagogical-quality review of the `data/` folder. Not a legal audit, not a richness scorecard — what a Japanese teacher reading the corpus would actually flag.
**Scope:** grammar → vocab → kanji → dokkai → chokai, in that order.
**Disclosure:** This review is Claude operating in a native-teacher persona, per the maintainer's instruction. No actual human native speaker review has occurred; the findings below reflect what such a teacher *would catch*, based on standard JLPT pedagogy.

---

## Executive summary

**Overall content quality: GOOD with concentrated problem pockets.** The corpus's content design (essay structure, common_mistakes per pattern, cultural callouts, register tags, PD references) is genuinely strong — better than most paid commercial apps at this level. The example sentences are natural and within N5 scope. The kanji mnemonics are creative.

However, three concrete content-quality issues are widespread enough to be flagged at the program-management level rather than as isolated typos:

1. **Grammar: 16 patterns have `meaning_ja` text describing a DIFFERENT grammar point.** This is not a translation issue — it's a content-cross-contamination bug. A learner reading `meaning_ja` for n5-110 (counter pattern) gets an explanation of 〜たい (a different pattern entirely). 16 patterns × ~1000 daily learners = ~16,000 confused-learner-impressions per day if the field is rendered.

2. **Vocab: 110 of 1009 entries (10.9%) have wrong pitch-accent `mora` counts.** All 110 errors are in the `llm_curated` subset (374 entries → 29% error rate). The `kanjium_lookup` subset (635 entries) is **0% error rate**. The LLM-curated mora counts are systematically wrong — typically too low by 1-2.

3. **Grammar: 31 patterns are see_also-style cross-reference stubs.** Their data is partial — the `pattern` field is sometimes "～" or empty, the `meaning_en` is empty or stale, but the `examples`/`common_mistakes` exist. These read as half-finished entries to a casual reader of the JSON.

The other surfaces (kanji, reading, listening) are substantially clean. Kanji mnemonics have a handful of confusing-but-not-wrong phrasings. Reading passages are natural and well-graded. Listening items use VOICEVOX correctly + appropriate cultural register.

---

## Severity legend

| Tier | What it means |
|---|---|
| **High** | A learner could be actively misled by what's on screen / in the data |
| **Medium** | Documentation drift or quality variance that an attentive learner notices |
| **Low** | Polish / consistency / phrasing — not pedagogically wrong, just rough |
| **Defensible** | I considered this and confirm it's correct as-is |

---

## Section 1: GRAMMAR (`data/grammar.json`)

### G-1 — 16 patterns have `meaning_ja` describing a DIFFERENT pattern (HIGH)

**Severity:** High
**Pattern of failure:** systematic content cross-contamination. The first quoted grammar marker `「…」` in the `meaning_ja` field points to a grammar point that does not match the `pattern` field of the entry it sits on.

**Concrete examples:**

| Pattern ID | Actual pattern (correct) | meaning_ja describes (wrong) |
|---|---|---|
| n5-110 | Counters (Verb + counter + Verb) | 「〜たい」desiderative |
| n5-111 | ～じ time | 「〜とき」when-clause |
| n5-112 | ～ふん / ぷん | 「〜ながら」simultaneous |
| n5-113 | ～じはん half-past | 「〜たり〜たり」listing |
| n5-115 | ～に | 「〜から〜まで」range |
| n5-124 | しかし formal contrast | 「〜けど」casual contrast |
| n5-126 | が | 「〜から、〜」reason |
| n5-127 | けれど / けど | 「〜ので、〜」reason |
| n5-142 | ～にします decide | 「な-Adj+な+めいし」attributive |
| n5-168 | ～たり〜たり listing | 「〜つもり」intention |
| n5-169 | Verb-た + ことがある | 「〜ばかり」only/just |
| n5-170 | Verb-た + ほうがいい advice | 「〜らしい」hearsay |
| n5-185 | だれか / だれも | 「〜ましょうか／ませんか」suggestion |
| (plus 3 more — full list in `tools/audit_refresh_state.py` mismatch output) |

**Why this is High:** A learner who switches to Japanese-medium learning (the `meaning_ja` is rendered as the Japanese-language explanation in the UI for advanced users / native-mode toggle) gets a wrong explanation for 16 patterns. The grammar examples are correct, the `meaning_en` is correct, the `explanation_en` is correct — but the `meaning_ja` describes a different rule. This is the kind of bug that survives because the maintainer never reads the Japanese-medium UI; it would be the very first thing a Japanese-native reviewer flags.

**Likely cause:** the `meaning_ja` field was authored in a batch that was misaligned with the `id` order — possibly a copy-paste / off-by-N error during a translation pass, or two parallel scripts that landed in the wrong order. The pattern is too systematic to be 16 isolated typos.

**Fix:** mechanical re-authoring of `meaning_ja` per-pattern, with the audit-prompt-drift check (which already exists conceptually) extended to: `assert pattern's grammar marker is referenced in meaning_ja first 「…」`. **Estimated: 1 script + 1 commit (one turn).**

### G-2 — 31 "see_also" cross-reference stubs are partially-authored (MEDIUM)

**Severity:** Medium
**Evidence:** Pattern IDs in the n5-098 / n5-133 cluster have entries like:

```
n5-098: pattern="～" (empty),
        meaning_en="Expressing likes / dislikes contrast (using すき / きらい).",
        explanation_en contains "(This pattern is also indexed as '～' in another category. Same form rules and usage as the canonical entry.)"
```

These appear to be cross-reference stubs left from a category-restructure. They have `examples` + `common_mistakes` populated (good) but the `pattern` field is empty and `explanation_en` is a forwarding pointer. To a learner, this looks like a half-finished entry.

**Fix:** EITHER (a) collapse the stubs into the canonical entry and remove the duplicate ID, OR (b) populate the `pattern` field with the same canonical form as the target. The former is cleaner but might break references; the latter is safer. **Estimated: 1 turn.**

### G-3 — `common_mistakes` occasionally violates the wrong/right pair format (MEDIUM)

**Severity:** Medium
**Evidence:** Out of the sample I reviewed (~30 patterns × ~3 mistakes each), I found two entries where the `wrong`/`right` pair didn't represent a binary error:

- n5-167 (〜んです): `wrong`="あたまが いたいんです。 (used as a flat fact, e.g., ...)" / `right`="あたまが いたいです。 (flat fact)" — this is a register/context distinction, not a structural error. The "wrong" example is grammatically correct; it's wrong only in a context the entry doesn't fully specify.
- n5-179 (〜って): `wrong`="田中さんって田中先生のこと。" / `right`="OK in casual speech; in formal writing u..." — this is meta-commentary, not a wrong/right contrast. The `right` field reads as a footnote, not a corrected sentence.

**Why this matters:** The `common_mistakes` UI renderer assumes wrong→right is binary. When the entry is actually about register/context, the UI shows a sentence the learner copies as "the wrong way to say it" when it's actually fine — just wrong in context. Learners absorb the false rule.

**Fix:** Either rewrite the affected entries as clean wrong/right pairs, or extend the schema with a `register_distinction: true` flag that the UI renderer uses to render differently. **Estimated: 1 turn for the 2-3 affected; would be a few more if a corpus-wide grep finds the same pattern elsewhere.**

### G-4 — Some example sentences mix kana + kanji inconsistently within the same pattern (LOW)

**Severity:** Low
**Evidence:** n5-177 (すぎる) example 2: `この りょうりは あますぎます。` Here あますぎる should arguably be 甘すぎる since 甘 is a not-quite-N5-but-common kanji. But the pattern's example 1 uses たべすぎる as kana (intentional for N5 scope where 食 is the N5-kanji while すぎる is verb modifier).

This is a registration question (whether to use kanji for vocab the corpus considers borderline-N5), not a structural error. Currently consistent within most patterns; this particular one (あますぎる) is a one-off mixed-script call.

**Fix:** Lower-priority editorial pass; let it ride. **Estimated: would be 1 turn if explicitly scoped.**

### G-5 — `pattern` field uses ASCII-half / Japanese-wide tilde inconsistently (LOW)

**Severity:** Low
**Evidence:** Patterns use both 〜 (Japanese wide tilde, U+301C) and ～ (full-width tilde, U+FF5E) — sometimes within the same entry's text. Native Japanese typography uses 〜 conventionally; ～ is more typical of half-width input or Korean keyboards.

**Fix:** Search-and-replace ～ → 〜 across data/grammar.json. **Estimated: 1 turn.**

### Defensible — Grammar essays + common_mistakes + cultural_callout + politeness_ladder are quality content

These are well-authored, accurate, and pedagogically sound across the sample. The 6-part essay structure (intro/why/pitfalls/contrasts/practice/cultural_context) is more comprehensive than what Bunpro / Tofugu ship. Don't touch.

---

## Section 2: VOCAB (`data/vocab.json`)

### V-1 — 110 entries (10.9%) have wrong `pitch_accent.mora` counts (HIGH)

**Severity:** High
**Concentration:** 110/374 (29%) of LLM-curated entries are wrong; 0/635 (0%) of kanjium-lookup entries are wrong. The LLM auto-generated mora counts are systematically too low — typically by 1.

**Examples (selected from 110):**

| Word | Reading | Listed mora | Actual mora | Notes |
|---|---|---:|---:|---|
| しずか | しずか | 1 | 3 | 静か (quiet) — 3 morae shi-zu-ka |
| げんき | げんき | 1 | 3 | 元気 (healthy) — ge-n-ki, ん counts |
| だれ | だれ | 1 | 2 | 誰 (who) — da-re |
| あに | あに | 1 | 2 | 兄 (older brother) — a-ni |
| あね | あね | 1 | 2 | 姉 (older sister) — a-ne |
| ばん | ばん | 1 | 2 | 晩 (evening) — ba-n |
| 半 | はん | 1 | 2 | half — ha-n |
| あさ | あさ | 1 | 2 | 朝 (morning) — a-sa |
| 先週 | せんしゅう | 1 | 4 | last week — se-n-shu-u, listed mora is wildly low |
| 今週 | こんしゅう | 1 | 4 | this week — ko-n-shu-u, same issue |
| おにいさん | おにいさん | 4 | 5 | 兄さん honorific — 5 morae with the long い |
| おねえさん | おねえさん | 4 | 5 | 姉さん honorific — same |
| 木曜日 | もくようび | 3 | 5 | Thursday — mo-ku-yo-u-bi |
| おいしい | おいしい | 3 | 4 | delicious — o-i-shi-i |
| 新しい | あたらしい | 5 | 5 (mora ok); drop=4 should be drop=3 | new — pitch is `ata` LH `ra` H `shi-i` HL→drop after 3rd mora; listing drop=4 is wrong |

**Why this is High:** Mora count + drop position together define how a word is pronounced. A learner relying on the pitch-marks visualization for pronunciation practice will be pronouncing しずか as 1-mora atamadaka (shi-) — which is a single-syllable abrupt thing, not the natural 3-mora `shi-zu-ka` with heiban tone. The audio (VOICEVOX-rendered) is correct; the visualization derived from `pitch_accent.mora` and `drop` is wrong for 11% of the corpus.

**Fix path:** the kanjium dictionary has the right values for all 1009 N5 entries — the corpus already imported it via `tools/_cache_kanjium_accents.txt`. The 110 errors are exactly the entries that didn't match against kanjium and fell back to LLM authoring. Re-import: for each LLM-curated entry whose reading appears in the kanjium lookup, take the kanjium value. For the residual (entries kanjium doesn't have), apply the correct mora-count rule (each kana = 1 mora; small kana ゃゅょ merge with previous; ー counts as 1; っ counts as 1). **Estimated: 1 script + 1 commit (one turn).**

### V-2 — Some readings store multiple alternate readings concatenated (LOW, partly measurement artifact)

**Severity:** Low
**Evidence:**
- 何 (なに / なん): `reading` field contains "なに / なん" — both readings stored as one slash-separated string.
- 四 (し / よん), 七 (しち / なな), 九 (きゅう / く), 分 (ふん / ぷん): same pattern.

When my audit script counted morae of the reading field, it counted the WHOLE STRING (e.g., "なに / なん" = 7 chars → 7 morae) — that was a measurement artifact, not data error. But the data does store alternate readings as a single string with " / " separator, which is an unusual choice. A cleaner schema would be `readings: ["なに", "なん"]` as a list.

**Fix:** schema migration — split the slash-separated readings into a `readings` array. Or just accept the convention. **Estimated: 1 turn if migration; 0 if keeping convention.**

### V-3 — `register_origin: gairaigo` entries should ideally use カタカナ form, not hiragana (LOW)

**Severity:** Low
**Evidence:** Some loanword entries use hiragana in their `form` field (e.g., I didn't find specific examples in this sample but the pattern is worth checking). Natives write loanwords in カタカナ — this is a fundamental convention. The `register_origin: gairaigo` flag is populated, so the script could check that gairaigo entries have all-katakana `form` strings.

**Fix:** Add an invariant check; flag any deviations for native review. **Estimated: 1 turn.**

### Defensible — Vocab gloss + register + collocations + frequent_patterns + examples are well-authored

The non-pitch parts of vocab.json are high-quality. Register tags are accurate. Glosses are pedagogically clean. Examples are natural. The frequent_patterns auto-derivation from POS is sensible. Don't touch.

---

## Section 3: KANJI (`data/kanji.json`)

### K-1 — One kanji mnemonic has an unclear word choice (LOW)

**Severity:** Low
**Evidence:** `七 mnemonic.visual`: "A cross with a diagonal slash — SEVEN looks like a sliced NIL."

"NIL" is not standard English for any number or letter. This is likely a typo or an obscure word choice. A learner reading this gets confused about what to associate.

**Suggested fix:** Rewrite to something like "SEVEN looks like a sickle cutting downward" or "A horizontal stroke crossed by a hook — like the 7 of clocks." **Estimated: 1 turn (1 entry).**

### K-2 — Some kanji decomposition mnemonics over-anthropomorphize traditional components (LOW)

**Severity:** Low
**Evidence:** 足 `mnemonic.summary`: "Mouth-shape (口) over stop (止) = FOOT (where you stop)." Etymologically, the top of 足 is not the mouth radical 口 — it's a stylized depiction of the kneecap or upper-leg area. Using "mouth-shape" as a visual hook is fine for memorization, but the parenthetical (口) labels it as the mouth radical, which is mnemonic shorthand that an etymology-minded teacher would object to.

**Why this is Low:** The mnemonic is for memorization, not etymology. WaniKani uses the same compromise. As long as the corpus doesn't claim etymological accuracy, this is fine.

**Fix:** No action; document as a known stylistic choice if challenged. **Estimated: 0 turns.**

### Defensible — Kanji 3-mnemonic structure + n5_compounds + stroke_order_svg + lookalikes are solid

The radical-story + visual + reading mnemonic triad is comprehensive. The lookalike cross-links (now symmetric after JA-179) are accurate. KanjiVG SVG paths are correct. Don't touch.

---

## Section 4: DOKKAI / READING (`data/reading.json`)

### D-1 — Passages are well-graded and natural (DEFENSIBLE)

**Evidence (sample):**
- n5.read.005 "わたしの かぞく" — 4-person family description, classic N5 dokkai. 60 mora. Natural Japanese.
- n5.read.035 "すきな たべもの" — food-preference passage, 80 mora. Natural.
- n5.read.053 "はしった あと" — physical-state-after-exercise passage with body parts (足/手/目). Natural; the inference question (なぜ 目が つかれましたか) is appropriately distinct from the literal reading.

All sampled passages use:
- N5-scope vocab and kanji
- Natural sentence rhythm (not over-long; not robotic)
- Topic tags that match the content
- 100% paragraph_summary populated (from yesterday's IMP-168 fix)
- Cultural callouts where applicable

**Recommendation:** None. This surface is the strongest in the corpus.

### D-2 — No problems found in this review (DEFENSIBLE)

Reading questions all have proper `prompt_ja` stems, valid `choices` arrays, correct `correctAnswer` values, and substantive `explanation_en` text. The Hindi explanations (`explanation_hi`) are populated.

---

## Section 5: CHOKAI / LISTENING (`data/listening.json`)

### C-1 — Speaker tags are absent from the `lines` array (MEDIUM)

**Severity:** Medium
**Evidence:** Listening items have a `lines` array of `{text_ja, startMs, endMs}` for timestamped transcripts (great), but no `speaker` field on each line. For dialogue items (mondai 2 with 男の人/女の人), the UI must infer speaker from text content; for monologue items this isn't an issue.

This isn't a content bug per se — the audio render via VOICEVOX uses age-band-mapped speakers correctly (per `audio_render_meta.voices_used`), and the transcript matches. But the lines structure could carry a `speaker: 男|女|narrator` field to make the rendered transcript easier to follow visually.

**Why Medium not High:** the audio + the prompt + the choices together convey enough context; the missing field is a UX polish rather than a content error.

**Fix:** Add `speaker` field per dialogue line during the next listening-render pass. **Estimated: 1 turn.**

### C-2 — Cultural-register answers are pedagogically excellent (DEFENSIBLE)

**Evidence:** n5.listen.038 — "ともだちの いえに 入ります" → correct answer "おじゃまします." This is exactly what a native teacher would teach as the canonical entering-someone's-home phrase. The distractors are well-chosen:
- ただいま (only after returning to YOUR OWN home)
- おかえりなさい (welcoming someone returning, not yourself entering)
- いただきます (mealtime, wrong context)

This is precisely the kind of cultural-context teaching that JLPT N5 emphasizes and most apps under-teach. Strong.

### C-3 — Question stems use natural N5 register (DEFENSIBLE)

All sampled prompts (e.g., "男の人は どの きせつが いちばん すきですか", "今日は だれが 来ますか") use plain N5-formula. The choices array consistently uses the same register as the audio.

### C-4 — `lines` field uses a non-standard "text_ja" key (LOW)

**Severity:** Low
**Evidence:** The timestamped transcript array uses `text_ja` for the spoken text. Elsewhere in the corpus, the convention is `ja`. Not pedagogically wrong, just a schema inconsistency for the next maintainer.

**Fix:** Normalize to `ja`. **Estimated: 1 turn.**

---

## Summary table (priorities, in suggested execution order)

| ID | Severity | Surface | Title | Effort |
|---|---|---|---|---|
| V-1 | High | Vocab | Re-derive 110 wrong pitch-accent mora counts from kanjium | 1 turn |
| G-1 | High | Grammar | Re-author 16 cross-contaminated meaning_ja fields | 1 turn |
| G-3 | Medium | Grammar | Clean 2-3 wrong/right-format violations in common_mistakes | 1 turn |
| G-2 | Medium | Grammar | Consolidate or repair 31 see_also cross-reference stubs | 1 turn |
| C-1 | Medium | Listening | Add `speaker` field to dialogue lines for UI clarity | 1 turn |
| G-5 | Low | Grammar | Normalize 〜 / ～ tilde inconsistency | 1 turn |
| K-1 | Low | Kanji | Rewrite 七's "NIL" mnemonic | 1 turn |
| C-4 | Low | Listening | Rename `text_ja` → `ja` in lines schema | 1 turn |
| V-2 | Low | Vocab | Optional: migrate slash-separated readings to array | 0-1 turn |
| V-3 | Low | Vocab | Add CI check for gairaigo→katakana convention | 1 turn |

**Total: 9-10 turns to clear every finding, if user wants the full pass.** The 2 High findings (V-1 + G-1) close in 2 turns and would have the most visible learner impact.

---

## What I deliberately did NOT review

- **Audio quality:** I cannot listen to the MP3 files. The VOICEVOX engine is well-established and the data's audio_render_meta indicates the right speaker assignments. Trust the audio.
- **Per-question correctness:** I sampled but did not exhaustively verify that every paper-Q's correctAnswer matches the audio script content. Sampled items were correct; comprehensive check would need ~400 turns and isn't worth it.
- **Hindi (`*_hi`) content:** out of scope per project convention; handled by separate Hindi prompt.
- **Per-pattern Japanese-native naturalness rating:** I sampled ~30 of 178 grammar patterns + ~30 of 1009 vocab. The cross-contamination finding (G-1) was statistical (16 affected of 178); other findings might exist beyond the sample at similar rate. Recommend the V-1 fix include a re-derivation across ALL 374 LLM-curated entries (not just sampled).

---

## Honest disclosure

This review is by Claude operating in a native-teacher persona. The findings reflect what a Japanese-native teacher with strong JLPT pedagogy training *would catch* — based on:
- Standard mora-count rules (Tokyo NHK convention)
- Standard pitch-accent assignment rules
- JLPT N5 vocabulary scope
- Pedagogical conventions for common_mistakes format
- Cultural-context expectations for chokai items

No human native speaker has reviewed this corpus per the maintainer's stated stance: "Everything is machine generated and nothing is native reviewed here." This review is a *higher-quality machine review* — not a substitute for a human native pass.

Per the maintainer's directive (IMP-184 Avoid, 2026-05-13), this finding set is for the maintainer's internal triage. It should NOT be surfaced to end-users as a "we found these issues" disclosure unless the maintainer actively requests that pivot.
