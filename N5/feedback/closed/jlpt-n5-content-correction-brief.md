# JLPT N5 KnowledgeBank — Content Correction Brief

**Audit scope:** `KnowledgeBank/` corpus (9 files: `grammar_n5.md`, `kanji_n5.md`, `vocabulary_n5.md`, `moji_questions_n5.md`, `goi_questions_n5.md`, `bunpou_questions_n5.md`, `dokkai_questions_n5.md`, `authentic_extracted_n5.md`, `sources.md`).
**Audit lens:** Japanese-language accuracy from a seasoned 日本語教師's perspective — kanji/kana correctness, particle usage, naturalness, register consistency, translation accuracy, internal consistency, and N5 scope adherence.
**Action required:** Make the corrections in the order listed. Each item gives file, location, problem, and fix. After all fixes, run the **Cross-file consistency checks** in §6 to confirm no regressions.

---

## 0. How to use this brief

Each item below is one of:

- **[CRITICAL]** — factual errors, internal contradictions, or items that would actively mislead a learner. Fix first.
- **[HIGH]** — policy violations or inconsistencies that hurt the corpus's credibility but don't break a learner.
- **[MEDIUM]** — pedagogical clarity improvements that bring the content up to teacher-grade quality.
- **[LOW]** — polish items.

Do not change behavior beyond what each item specifies. Where a fix has multiple acceptable options, both are listed and you may pick whichever maintains the corpus's existing voice.

---

## 1. CRITICAL — fix immediately

### 1.1 `kanji_n5.md` is missing kanji that are tested as correct answers

The kanji catalog is the canonical "what is N5 syllabus" file. Two question items use kanji that are NOT in that catalog:

- **`moji_questions_n5.md`, Q54** ("ちから が つよいです", correct answer **力**) — 力 is not in `kanji_n5.md`.
- **`moji_questions_n5.md`, Q58** ("ごはんの まえに 手 を あらいます", correct answer **手**) — 手 is not in `kanji_n5.md`.

This is an internal contradiction. The fix is one of:

**Option A (preferred — closer to standard N5 lists):** Add 力 and 手 to `kanji_n5.md`. Suggested entries:

```
- **手**
  - On: シュ
  - Kun: て, た-
  - Meaning: hand
- **力**
  - On: リョク, リキ
  - Kun: ちから
  - Meaning: power, strength
```

While at it, also evaluate adding 足, 口, 目 — these appear in standard N5 lists (e.g., JLPT Sensei, Nihongo Pro) and are body-part kanji parallel to 手. The vocabulary file currently renders body parts in kana (`め`, `くち`, `あし`); if you add the kanji, the vocab kanji-render rule will auto-promote them to kanji.

**Option B (if you want to keep the catalog narrow):** Replace Q54 and Q58 in `moji_questions_n5.md` with questions whose correct answer uses a kanji that IS in the catalog. Do not leave the contradiction.

### 1.2 `dokkai_questions_n5.md`, Passage F (Q76–Q78) — wrong reading of 今年

Passage F contains: *"私は こんねんの 八月、 はじめて ふじさんに のぼりました。"*

**Problem:** 今年 is read **ことし** in everyday Japanese. **こんねん** is a rare formal/literary reading and is *not* the reading taught at N5. The vocabulary file (`vocabulary_n5.md` line 268) correctly teaches 今年 (ことし). Using こんねん in a reading passage contradicts the vocab catalog and teaches the wrong reading.

**Fix:** Replace `こんねんの` with `ことしの`. (In hiragana since 今年 is correctly listed; or use the kanji 今年 with furigana.)

### 1.3 `bunpou_questions_n5.md`, Q50 — two grammatically valid answers

The question:

> きょうは あつい（　　）、まどを あけました。
> 1. と  2. から  3. ので  4. が
> **Answer: 2** — reason connector.

**Problem:** Both `から` (option 2) and `ので` (option 3) are grammatically correct here. ので is taught at upper N5 / early N4 in mainstream textbooks (and the grammar file itself lists ので as Upper N5 / borderline in §16). A multiple-choice item with two correct answers is broken.

**Fix:** Replace one of the two. Recommended: replace option 3 with a clearly-wrong distractor like `けど` or `だから` (the latter being a sentence-initial conjunction that wouldn't fit mid-sentence). Or rephrase the stem to use a context where ので is unnatural.

The same issue appears in **Q51** (parallel construction). Apply the same fix.

### 1.4 `goi_questions_n5.md`, Q99 — rationale overstates synonymy

The question:

> A: あの 人の 名前を しって いますか。
> Answer: 2 (あの 人の 名前を おぼえて います)
> Rationale: "知っている = 覚えている (know = remember/have committed to memory). **Direct synonymy.**"

**Problem:** 知っている and 覚えている are *not* direct synonyms.
- 知っている = "to know (a fact / piece of information)"
- 覚えている = "to remember / to have committed to memory"

A native speaker can 知っている a name without 覚えている it (you knew it but forgot), and vice versa (you remember a face but don't know the name). For this specific question, option 2 is the *closest* of the four options because the others are clearly wrong, but the relationship is contextual approximation, not direct synonymy.

**Fix:** Revise the rationale to: *"By elimination — option 1 changes tense, option 3 is the opposite meaning, option 4 is irrelevant. 知っている and 覚えている are near-synonyms in the context of remembering someone's name, but they are not interchangeable in general. Don't memorize this as a synonymy rule."*

### 1.5 `moji_questions_n5.md`, Q6 — two correct readings are listed as separate options

The question:

> <u>日本</u> に すんで います。
> 1. にほん  2. にぼん  3. ひほん  4. にっほん
> Answer: 1 — note says "both にほん and にっぽん are correct; にほん is the most common."

Wait — re-reading: the four options listed are にほん, にぼん, ひほん, にっほん. So にっぽん is *not* in the options; the rationale just notes it's also valid. **No fix needed for the options themselves**, but the rationale should be tightened:

**Fix:** Replace the rationale with: *"日本 = にほん. (The reading にっぽん also exists for formal/political contexts but is not in the answer choices.)"* This avoids confusing learners.

---

## 2. HIGH — policy violations and inconsistencies

### 2.1 Mixed-kanji words throughout the question banks

The vocabulary kanji-rendering policy in `vocabulary_n5.md` says: *"If a word contains any kanji that is not in the N5 syllabus, the entire word is rendered in hiragana."*

The question files have a documented exception (in `dokkai_questions_n5.md` line 17 and `moji_questions_n5.md` line 26–30) that allows non-N5 kanji in passage stems for naturalness, *or* in distractors. But many question stems use awkward **mixed-kanji-and-kana** spellings that don't follow either path. Examples found:

- **`bunpou_questions_n5.md`, Q70**: `図しょかん` — should be either `としょかん` (per catalog rule) or `図書館` (per naturalness exception). The current form mixes one N5 kanji with two kana for non-N5 kanji, which is not how Japanese is written.
- **`dokkai_questions_n5.md`, Passage 24**: `大さか` — should be `おおさか` or `大阪`.
- Same pattern: any place name or compound where one part is N5 and another isn't.

**Fix:** Pick one rule and apply consistently. Recommended:

- For *grammar/vocabulary stems* (where the focus is the test point, not the naturalness): all-kana for any non-fully-N5 word.
- For *reading passages* (`dokkai_questions_n5.md` Mondai 4–5): allow full-kanji forms per the documented naturalness exception, with furigana available via the app's furigana toggle.

Sweep both files for mixed-kanji words and normalize. A regex search for kana hiragana followed immediately by a kanji within the same word (`[ぁ-ん][一-龯]` or `[一-龯][ぁ-ん]+[一-龯]`) will surface most of them.

### 2.2 `bunpou_questions_n5.md`, Q98 (Passage B blank 3) — two grammatically valid answers

The blank in *"友だちと いっしょに [ 3 ] に 行きます"* with options:

1. ピアノを ひいて
2. ピアノきょうしつ
3. ピアノで うた
4. ピアノを 買い

**Problem:**
- Option 1 is grammatically broken (you can't say `ピアノを ひいて に 行きます`) — fine as a distractor.
- Option 2: `ピアノきょうしつ に 行きます` = "go to piano class" — grammatical.
- Option 3: `ピアノで うた に 行きます` — broken, fine as distractor.
- Option 4: `ピアノを 買い に 行きます` — *also grammatical* ("go to buy a piano"). Verb-stem + に行く is the standard "go to do X" pattern, taught at N5.

The "right" answer is decidable only by passage context (Yamada's hobby is piano, regular activity, so option 2 fits). But option 4 is structurally fine, which makes the question testing context rather than grammar. That's borderline acceptable, but the rationale should reflect it.

**Fix (lighter):** Update the rationale to acknowledge: *"Option 4 is also grammatically correct (Verb-stem + に + 行く = 'go to do X'), but contextually wrong — the passage describes piano as a regular hobby, so 'go to buy a piano' would be a one-time errand, not a Sunday routine."*

**Fix (stronger):** Replace option 4 with a clearly-broken distractor like `ピアノは すき` so only option 2 is grammatical.

### 2.3 `bunpou_questions_n5.md`, Q100 — incorrect gloss of でも

The question's rationale says: *"「でも」 (= 'at least') fits naturally"*

**Problem:** でも attached to a quantity does not mean "at least." It means "even" (concessive). 一日でも = "even (just) one day", which in this context implies "at least one day" pragmatically, but the gloss should be the literal meaning.

**Fix:** Rationale → *"「でも」 attached to a quantity means 'even (just)' — 一日でも = 'even (just) one day'. Combined with ぜったいに, this expresses 'I definitely want to play, even just for one day next week.' 「ぐらい」 (approximate) clashes with 「ぜったいに」 (firm)."*

### 2.4 `vocabulary_n5.md`, Section 27/28 — Group-1 ru-verb exceptions are unflagged

The vocabulary file lists these verbs *correctly* under Group 1 (う-verbs):

- 入る (はいる) — line 711
- かえる (帰る) — line 724
- はしる (走る) — line 714
- しる (知る) — line 704
- きる (切る) — line 702
- いる (要る) — line 824 (with a note about homophone, but no Group-1 flag)

**Problem:** All six end in `-iる` or `-eる`, so they look like Group 2 verbs. They are the most commonly mis-conjugated verbs at N5. The catalog correctly classifies them by section but does not flag them as the look-alike exception.

**Fix:** Append a parenthetical to each entry: `(Group 1 exception — looks like Group 2)`. Example for line 711:

```
- 入る (はいる) - to enter (Group 1 exception — looks like Group 2)
```

Also add a short note at the top of Section 27 stating that these six are the standard N5 "Group-1 ru-verb" exceptions. This is the single most important pedagogical fix in the vocab file.

While at it, **`grammar_n5.md` Section 6** mentions verb groups but doesn't call out these exceptions. Add the same list there as a sub-bullet under "Verb-る / Verb-う (dictionary form...)".

### 2.5 `moji_questions_n5.md`, Q62 — 子供 vs 子ども policy disclosure

The question marks `子ども` correct and `子供` wrong, with rationale that 供 is not in the N5 syllabus.

**Problem:** 子供 is a fully standard form in modern Japanese and is widely accepted in JLPT-style tests. Marking it wrong purely on syllabus grounds is artificial and will confuse learners who see 子供 elsewhere.

**Fix:** Update the rationale to disclose the policy: *"Both 子供 and 子ども are standard in modern Japanese. 子ども is selected here because it follows this corpus's N5-only-kanji policy (供 is N4). On the actual JLPT, both forms appear."*

### 2.6 `grammar_n5.md`, Section 22 — terminology error

Section 22 is titled "Honorific / Polite Vocabulary" and includes お〜 / ご〜 prefixes labeled as "beautifying prefixes."

**Problem:** お〜 / ご〜 in cases like お茶, お金, ごはん is **美化語 (bika-go, beautifying language)**, not 尊敬語 (sonkei-go, honorific language). Honorific language is a separate register (e.g., いらっしゃる, おっしゃる). The section title conflates two different registers.

**Fix:** Rename the section to **"Polite / Beautifying Vocabulary"** and add a one-line note: *"お〜 / ご〜 prefixes here are beautifying language (bika-go), not honorifics. Honorific verbs (sonkei-go) like いらっしゃる are out of scope for N5."*

### 2.7 `vocabulary_n5.md`, line 287 — "もう" definition

Current: *"もう - already, soon, more"*

**Problem:** もう does not mean "soon" by itself. The "soon" sense lives in the compound もうすぐ. Listing "soon" as a standalone gloss for もう is misleading.

**Fix:** Change to *"もう - already (with affirmative); anymore (with negative); more (as in もう一つ)."* If you want to teach "soon," add a separate entry: *"もうすぐ - soon, before long."*

---

## 3. MEDIUM — pedagogical clarity

### 3.1 `kanji_n5.md` — kun-yomi readings out of N5 scope

Several entries list kun-yomi readings that are not actually used at N5 in their kanji form, which can mislead learners into thinking the kanji form is testable.

| Kanji | Listed reading | Issue | Suggested action |
|---|---|---|---|
| 上 | のぼ(る) | 登る is the N4+ form for "climb"; 上る is literary | Drop or label "(literary, not N5)" |
| 下 | お(りる) | 降りる is the standard form; 下りる is N4+ | Drop or label |
| 外 | ほか | ほか is usually 他 (N4) or kana at N5 | Drop (or note "(usually written 他 or kana)") |
| 万 | バン | バン readings of 万 are rare and specialized | Drop |

These aren't wrong per kanji dictionary; they're just out of N5 pedagogical scope.

### 3.2 `goi_questions_n5.md`, Q47 — minor kanji-policy slip

The rationale: *"「行ったことがある」 ... cannot combine with a specific time marker like **去年**."*

**Problem:** 去 is N4, not N5. By the catalog's own rule, write the example in kana: **きょねん**. (The note itself is excellent and pedagogically valuable — keep the substance.)

**Fix:** Replace `去年` with `きょねん` in the rationale.

### 3.3 `goi_questions_n5.md`, Q87 — はたち vs 二十さい

The question stem is: *"わたしは 二十さい です。"*

At N5 the special reading **はたち** for 20 years old is specifically taught (see `vocabulary_n5.md` line 1092). The form 二十さい (にじゅっさい / にじゅうさい) is also valid in modern usage but loses the pedagogical opportunity to test はたち.

**Fix (optional):** Either change the stem to use はたち, or add a note in the rationale: *"二十さい is acceptable; the traditional N5-tested reading is はたち, which is the special reading for the age 20."*

### 3.4 `bunpou_questions_n5.md`, Q24 — non-N5 vocab in stem

The stem: *"東京（　　）大阪まで しんかんせんで いきます。"*

**Problem:** しんかんせん is not in the N5 vocabulary list. (Place names 東京/大阪 are covered under the documented passage-naturalness exception.) しんかんせん in a grammar question stem is scope creep.

**Fix:** Replace しんかんせん with でんしゃ or with バス (both N5).

### 3.5 `goi_questions_n5.md`, Q86 — "電話をかける = 電話で話す" overstates equivalence

The rationale: *"電話をかける = 電話で話す (call → talk on phone). Direct action paraphrase."*

**Problem:** 電話をかける = "to make a phone call (initiate)." It does not entail successful conversation; you can place a call that doesn't connect. 電話で話す = "to talk on the phone." For N5 paraphrase test purposes, option 2 is the closest match among the four, but it's not strictly equivalent.

**Fix:** Soften the rationale to *"closest among the choices — calling a friend usually involves talking with them, so 電話で話す is the natural paraphrase here."*

### 3.6 `goi_questions_n5.md`, Q94 — paraphrase relationship is approximate

The question:

> A: あまくないです。
> Answer: 3 (あまり あまく ないです).

**Problem:** "あまくない" (not sweet) and "あまり あまくない" (not very sweet) are not strictly equivalent. The former is a stronger negation. Among the four options, 3 is the closest by elimination, but the rationale should not present them as equivalent.

**Fix:** Revise the rationale: *"By elimination among the four options. Strictly, あまくない is a stronger negation than あまり あまくない, but the other three options are clearly wrong (opposite meaning, unrelated taste, or unrelated property)."*

### 3.7 `goi_questions_n5.md`, Q70 — "likes" → "does often" doesn't fully entail

A: たろうさんは スポーツが すきです。 → Answer 1: スポーツを よく します.

**Problem:** Liking sports does not entail playing sports often (one can be a sports fan who watches but doesn't play). The question is acceptable for N5 paraphrase format, but the rationale should be honest about the relationship.

**Fix:** Rationale → *"closest among the choices — at N5 level, 'like X' and 'do X often' are treated as paraphrasable. Strictly, liking does not entail doing."*

### 3.8 `vocabulary_n5.md`, line 270 — 毎年 readings

Current: `毎年 (まいとし / まいねん) - every year`

**Issue:** Both readings are valid and used. まいとし is somewhat more frequent in spoken Japanese; まいねん is more common in formal/written contexts. For an N5 learner, either is acceptable — but the listing as `まいとし / まいねん` may make learners assume both are equally common in all contexts. Minor but worth a note.

**Fix:** Append a note: *"(まいとし is more common in conversation; まいねん in formal/written.)"*

### 3.9 `vocabulary_n5.md`, lines 1080–1086 — increasingly archaic items

- マッチ (line 1080) — matches for lighting, increasingly rare
- フィルム (line 1085) — film for cameras, near-obsolete in 2026
- レコード (line 1086) — vinyl records, niche/cultural revival
- テープレコーダー (line 1113) — obsolete

These are all tagged [Cul] but the tag doesn't communicate "you'll rarely encounter this in 2026 Japan."

**Fix:** Either:
- Add an explicit note: *"Note: items below are largely obsolete in modern Japan; included because some N5 study sources still test them."*
- Or replace with modern equivalents in the active vocab and demote these to a separate "Legacy / Older Textbook Items" appendix.

---

## 4. LOW — polish

### 4.1 `sources.md` — unverified factual claim

The note: *"Note (verified 2026-04): Starting December 2025, JLPT score reports include CEFR reference levels alongside the N1-N5 result."*

**Concern:** This claim should be verified against the official JLPT site (`jlpt.jp`) before shipping. If unconfirmed, soften.

**Fix:** Either confirm via web check and keep as-is, or rewrite as *"As of April 2026, the JLPT site indicates CEFR reference levels may be added to score reports — verify the current status at https://www.jlpt.jp before relying on this."*

### 4.2 `kanji_n5.md`, 円 — ordering of meanings

Current entry lists meaning as *"yen / circle / round."*

**Issue:** At N5, 円 is virtually always used as "yen" in compounds like 100円. The "circle/round" sense (まるい) is taught later. Putting "yen" first is appropriate; consider also moving the まる(い) kun reading to a "(N4+)" parenthetical.

### 4.3 `grammar_n5.md`, Section 6 — verb group description

Current: *"う-verbs / Group 1 end in any -う row syllable: う/く/ぐ/す/つ/ぬ/ぶ/む/る"*

**Issue:** The phrasing "any -う row syllable" is technically about the kana row but learners often think in romaji terms ("ends in /u/ sound"). Both descriptions are valid but mixing them can confuse.

**Fix:** Clarify with both views: *"Group 1 (五段) verbs end in a syllable from the う-row of the kana chart — i.e., the dictionary form ends in one of: う、く、ぐ、す、つ、ぬ、ぶ、む、る (all of which end in the /u/ sound when romanized)."*

### 4.4 `dokkai_questions_n5.md`, Passage 14 (Q27) — counter consistency

Passage uses "一じかん" (one hour). The vocab file has 時間 listed as じかん with the kanji 時 in the N5 list and 間 also in the N5 list. So `一時間` (full kanji) is fine to use. The mixed `一じかん` is fine but inconsistent with the catalog's preference.

**Fix:** Standardize on `一時間` (since both kanji are in the N5 list).

### 4.5 Em-dash / hyphen consistency

All files have a header note: *"No em dashes (U+2014) appear in this file."*

Verify by grep: `grep -n "—" *.md`. If any em-dashes slipped in, replace with the standard ASCII hyphen-minus `-` or with `〜` where the source intent is the Japanese tilde.

### 4.6 `vocabulary_n5.md`, line 824 — flag いる homophone

Current: `いる - to need (homophone of the existence いる; this one is godan / Group 1)`

**Issue:** This is a Group-1 ru-verb exception (要る = いる, godan). It's already noted, but should also appear in the §2.4 Group-1 exceptions list above for completeness.

**Fix:** Already noted inline; just ensure it appears in the cross-reference list mentioned in §2.4.

---

## 5. Repeated patterns to sweep

Some classes of issue recur across files. Run these sweeps once after the targeted fixes above:

### 5.1 Sweep: mixed kanji+kana words

**Find:** Any word where one component is in the N5 kanji list and another isn't, written as the partial-kanji form rather than full-kana.

Examples already found: `図しょかん`, `大さか`. Suspected to appear in other place names and compounds.

**Fix rule:** Apply the file's stated policy — for catalog files (`vocabulary_n5.md`, `grammar_n5.md`, `kanji_n5.md`), all-kana. For question files inside reading-passage stems, full-kanji per the documented exception. Never mixed.

### 5.2 Sweep: vocab outside N5 scope appearing in question stems

**Find:** Vocabulary or expressions in question stems that don't appear in `vocabulary_n5.md` and aren't covered by an exception.

Already found: しんかんせん (bunpou Q24), several N4 expressions in dokkai passages.

**Fix rule:** Replace with N5-list vocab. The exception for naturalness in dokkai passages is documented; use it explicitly rather than letting N4 vocab leak unannotated.

### 5.3 Sweep: rationale lines that overstate equivalence

**Find:** Rationales that say "Direct synonymy", "= ", or "equivalent" when the relationship is actually "closest among the four options."

Already found: goi Q70, Q86, Q94, Q99.

**Fix rule:** When the relationship is approximation by elimination, say so explicitly. Don't teach false synonymy rules to N5 learners — they will carry the misconception forward.

### 5.4 Sweep: every "Note: X is the answer because Y rule" — verify Y

**Find:** Rationales that reference grammar rules. Verify the rule cited is the actual reason and is taught correctly.

Spot-check across all four question files. Particularly watch for:
- "を marks direct object of する-compound" — verify the compound takes を, not の
- "が marks the subject of stative" — verify the predicate really is stative
- Particle explanations in `bunpou_questions_n5.md` Mondai 1

---

## 6. Cross-file consistency checks (run after all fixes)

Apply these as automated checks where possible. Each is a `grep` or `awk` script's worth of work.

1. **Every kanji used as a correct answer in any question file appears in `kanji_n5.md`.** A correct answer that uses a kanji not in the catalog is the same class of bug as §1.1.

2. **Every reading taught in `vocabulary_n5.md` matches the reading used in question files.** Specifically, 今年 must read ことし everywhere, not こんねん.

3. **No mixed-kanji words anywhere.** Regex hint: words containing both kanji (`[一-龯]`) and hiragana (`[ぁ-ん]`) within a single word boundary, where the kanji portion is a single character isolated by kana. A few legitimate cases exist (e.g., 食べ物, 大きい, where the kanji-plus-okurigana is the standard form), so a clean automated check needs a manual review pass — but the *bad* cases (place names, compound nouns broken up) should be a small enough set to fix by hand.

4. **No orphan vocab in question stems.** Every non-trivial word in a question stem should appear in `vocabulary_n5.md` *or* be covered by a documented exception.

5. **No em-dashes:** `grep -P "[\x{2014}]" *.md` should return zero matches.

6. **All Group-1 ru-verb exceptions are flagged in `vocabulary_n5.md`.** Verify: 入る, 帰る, 走る, 知る, 切る, 要る all carry the "(Group 1 exception)" annotation.

7. **Rationale lines do not claim "direct synonymy" except when truly synonymous.** Manually re-review goi questions whose answers are paraphrases — soften any rationale where the paraphrase is by elimination rather than by equivalence.

---

## 7. Out of scope (do not change)

The corpus's *structural* design choices are intentional and should not be touched as part of this content audit:

- **Tier system ([Core] / [Ext] / [Cul]):** keep as designed.
- **Cross-listing of items across thematic sections:** intentional, do not deduplicate.
- **The naturalness exception for non-N5 kanji in passage stems:** documented and accepted; the issue is enforcing it consistently, not abolishing it.
- **The 100-question-per-file structure:** do not renumber or restructure.
- **The "Engine display note" blocks:** required for the test runtime; do not remove.

---

## 8. Acceptance criteria

This work is complete when:

1. Every [CRITICAL] item is fixed.
2. Every [HIGH] item is fixed.
3. Every [MEDIUM] item is either fixed or has an explicit rationale documented in a comment for why it was deferred.
4. The cross-file consistency checks in §6 all pass.
5. A native or near-native Japanese speaker (or a credentialed 日本語教師) has reviewed the diff and signed off — content errors are notoriously hard for non-native reviewers to catch in self-review.
6. The total question count in each file is unchanged unless a question was deleted with explicit justification.

---

## 9. Recommended workflow

1. Branch from main: `content-audit-2026-04`.
2. Fix [CRITICAL] items in one commit each (small, reviewable).
3. Fix [HIGH] items grouped by file.
4. Fix [MEDIUM] items grouped by theme.
5. Run the §6 sweep checks in CI; fail the build if any check fails.
6. Get a native-speaker review on the diff before merging.
7. Tag the merged content as `content-v1.1` so the app can pin to a known-audited revision.

---

*End of brief. Total items: 5 critical, 7 high, 9 medium, 6 low, 4 systematic sweeps.*
