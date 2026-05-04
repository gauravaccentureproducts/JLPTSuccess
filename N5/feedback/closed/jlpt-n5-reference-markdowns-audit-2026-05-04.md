# JLPT N5 Tutor - Reference Markdowns Re-audit (grammar / kanji / sources / vocabulary)

**Date:** 2026-05-04
**Audit scope:** dedicated close-read of the four catalog reference markdowns:

- `grammar_n5.md` (13.8 KB; +661 bytes since prior audit)
- `kanji_n5.md` (9.9 KB; +487 bytes since prior audit; 5 new kanji added)
- `sources.md` (7.3 KB; +50 bytes since prior audit; CEFR claim softened)
- `vocabulary_n5.md` (43.3 KB; +7,947 bytes since prior audit; POS tags added throughout)

**Audit lens:** Japanese-language correctness, internal-consistency between catalog rules and their application, and verification that previously-flagged issues are resolved.

**Comparison baseline:** moji-and-source audit (2026-05-03) which examined these files in passing during cross-referencing but did not give them a dedicated file-by-file pass.

---

## 0. Executive summary

Real progress since the previous round, with several previously-flagged systemic issues now resolved at the source level:

**Verified resolved since the previous audit cycle:**

- **vocabulary_n5.md POS-by-section bug fully fixed.** Section 12 (Time-Frequency) now correctly distinguishes [n.] (毎日, まいあさ, まいばん) from [adv.] (いつも, よく, 時々, etc.). Section 14 (Nature) and 20 (Colors) properly tag i-adjectives separately from color/feature nouns. Section 30 (Verbs - Existence) now correctly tags あげる / くれる / かりる / いる(exist) as [v2], with the homophone いる(need) correctly tagged [v1]. This was the largest pedagogical risk in the corpus.
- **kanji_n5.md scope-trimming has begun.** 円 has been corrected to remove the rare まる(い) kun (now `Kun: -` with explanatory note). 万 narrowed from `マン, バン` to `マン` with note. 上 and 下 now carry explicit `[N4+ verb reading; listed for recognition only]` flags on their verb readings. Five new entries added: 手 / 足 / 目 / 口 / 力 (Body section).
- **grammar_n5.md improved verb-class explanation.** Section 6 now explicitly enumerates Group 1 vs Group 2 conjugation rules with the standard six Group-1 ru-verb exceptions (入る / 帰る / 走る / 知る / 切る / 要る). Section 22 properly distinguishes 美化語 (bika-go, beautifying) from 尊敬語 (sonkei-go, honorific) - terminologically precise, valuable for serious learners.
- **sources.md CEFR claim softened.** Previous version asserted "Starting December 2025, JLPT score reports include CEFR reference levels"; new version reads "Note (as of April 2026): The JLPT site indicates CEFR reference levels may be added to score reports - verify the current status." The cautious phrasing is appropriate.

**Remaining issues**, mostly carried-over from previous cycles or surfaced by the new POS-tagging work:

- kanji_n5.md applies the `[N4+ ...]` scope flag to only 2 of ~19 entries that need it. The README's "limited to N5 senses" rule is inconsistently enforced.
- The 入 / 語 entries continue to drive the upstream readings inconsistency that affected n5_kanji_readings.json's `primary` field in earlier audits.
- vocabulary_n5.md's new POS tags introduce 6-7 mistags concentrated in Section 1 (pronouns) and one in Section 12.

**Total actionable items: 11** (0 critical, 4 high, 5 medium, 2 low).

This is the first audit cycle without a critical-severity item since the project began. The corpus is converging.

---

## 1. HIGH

### 1.1 kanji_n5.md - readings-scope inconsistency: `[N4+]` flag applied to only 2 of ~19 entries that need it

The README states explicitly:
> **Pedagogical scope rule** - meanings shown are limited to the senses an N5 learner needs. Advanced senses (e.g., literary or technical readings) are intentionally omitted.

Two entries have begun applying this rule to readings (not just meanings):
- 上: `Kun: うえ, あ(げる) [N4+ verb reading; listed for recognition only]`
- 下: `Kun: した, さ(げる) [N4+ verb reading; listed for recognition only]`

But many other entries list readings outside N5 scope without any flag. A native Japanese teacher or JLPT specialist scanning the file would notice the following inconsistencies:

| Kanji | Listed reading | Issue |
|---|---|---|
| 入 | Kun: `い(る), はい(る), い(れる)` | い is the secondary stem; 入る reads はいる. List order misleads. |
| 語 | Kun: `かた(る)` | 語る "to tell/narrate" is N3 verb; not N5 use. |
| 何 | On: `カ` | カ is N3+ (e.g., 幾何 きか); not used at N5. |
| 半 | Kun: `なか(ば)` | 半ば "midst" is N3+; at N5, 半 is only はん in 〜時半. |
| 後 | Kun: `のち, うし(ろ), あと` | のち is literary/N4+; common N5 readings are うしろ, あと. |
| 木 | Kun: `き, こ-` | こ- prefix (木陰 etc.) is N4+. |
| 金 | Kun: `かね, かな-` | かな- prefix (金物 etc.) is N4+. |
| 小 | Kun: `ちい(さい), こ-, お-` | Both prefixes are N4+; only ちい(さい) is N5. |
| 見 | Kun: `み(る), み(える), み(せる)` | み(える) is N4 (見える "be visible"); み(せる) is N4-N5 borderline. |
| 聞 | Kun: `き(く), き(こえる)` | き(こえる) is N4 (聞こえる "be audible"). |
| 立 | Kun: `た(つ), た(てる)` | た(てる) is N4 (立てる "set up"). |
| 休 | Kun: `やす(む), やす(まる)` | やす(まる) is N4 (休まる, intransitive). |
| 空 | Kun: `そら, あ(く), から` | あ(く) is N4 (空く "become vacant"). |
| 白 | Kun: `しろ, しろ(い), しら-` | しら- prefix (白雪 etc.) is N3+. |
| 新 | Kun: `あたら(しい), あら(た), にい-` | あら(た) is N3; にい- prefix is N4+. |
| 行 | Kun: `い(く), ゆ(く), おこな(う)` | ゆ(く) is N4 poetic alt; おこな(う) is N3 (行う). |
| 来 | Kun: `く(る), きた(る)` | きた(る) is N3+ literary. |
| 言 | Kun: `い(う), こと` | こと is jukujikun-only (言葉 ことば); not standalone N5 use. |
| 生 | Kun: `い(きる), う(まれる)` (note says "primary N5 use: in compounds") | Note describes on-yomi compound use; kun list shows verbs. Both 生きる / 生まれる ARE N5 vocab. Note misleads. |

**Two paths to consistency:**

1. **Apply the flag uniformly:** add `[N4+ ...]` markers to every out-of-scope reading. Example:
   ```
   - **見**
     - On: ケン
     - Kun: み(る), み(える) [N4 verb reading; recognition only], み(せる) [N4 verb reading]
     - Meaning: see, look
   ```

2. **Strip out-of-scope readings entirely** for kanji where the README rule is meant to prevail. This makes the file a learning catalog rather than a reference catalog.

The first option preserves reference value; the second is more pedagogically clean. Either is acceptable; the current state (some kanji flagged, most not) is the worst outcome because it suggests rules are being applied unevenly.

**Severity:** High. ~19 entries affected. Direct contradiction between the README's documented scope rule and its application.

### 1.2 kanji_n5.md 入 - kun reading order misleads (root cause of previously-flagged primary-reading bug)

**Current entry:**
```
- **入**
  - On: ニュウ
  - Kun: い(る), はい(る), い(れる)
  - Meaning: enter, put in
```

**Problem:** the kun list has `い(る)` first. By the project's "first kun is primary" precedence rule (documented in the dossier's `cover.md`), this means い is the surfaced primary reading.

But:
- 入る reads **はい**る (the standard, dominant modern reading)
- 入れる reads **い**れる (uses the alternate kun stem)
- 入り reads **い**り
- The verb form 入る = いる (with い kun) exists but is archaic/poetic (e.g., set phrase 気に入る きにいる)

**Effect:** the previous infrastructure audit flagged that `n5_kanji_readings.json` has `入: primary="い"` which is wrong for N5 use. **This is the upstream source of that bug.** The kanji_n5.md kun list ordering propagates to all downstream files that follow first-kun precedence.

**Suggested fix:** reorder to `Kun: はい(る), い(る), い(れる)` so that はい is the primary reading. Add note: "Note: い-stem appears in 入れる, 入り; はい- is the standalone verb 入る." This single edit cascades correctness through n5_kanji_readings.json and any consumer.

**Severity:** High. Single root cause of a downstream bug previously audited.

### 1.3 vocabulary_n5.md - 6-7 POS-tag inaccuracies in Section 1 (Pronouns) and 1 in Section 12

The new POS-tag system introduced in vocabulary_n5.md is well-designed (mirrors `data/vocab.json`, uses Japanese-grammar conventions). But in application, Section 1 ("People - Pronouns and Self") tags some entries `[pron.]` that aren't actually pronouns lexically:

| Entry | Current tag | Should be | Why |
|---|---|---|---|
| 人 (ひと) | [pron.] | [n.] | 人 is a noun ("person"). Used in pronoun-like phrases (この人) but lexical class is 名詞. |
| かた | [pron.] | [n.] | 方 (polite "person") is a noun, used in noun-headed phrases like あの方. |
| だれ | [pron.] | [Q-word] | Internal inconsistency: section 6 has だれ as [Q-word]. Same word should have one canonical POS. |
| どなた | [pron.] | [Q-word] | Same as だれ; polite interrogative for "who". |
| みなさん | [pron.] | [n.] | "Everyone" - used vocatively / as address term, not pronominally. |
| みんな / みな | [pron.] | [n.] | Same as みなさん; classed as 名詞 in standard Japanese grammar. |

**Section 12** has one similar issue:

| Entry | Current tag | Should be | Why |
|---|---|---|---|
| もうすぐ | [n.] | [adv.] | "Soon, before long" - functions adverbially (もうすぐ来る). Compare すぐ [adv.] and もうすこし [adv.] which are correctly tagged. |

**The legend itself is correct** (`[Q-word] = interrogative (なに / どこ / etc.)` is the right pattern). The application is what's drifting. The 6 pronoun-section mistags suggest the tags were applied by section-default ([pron.] for everything in "Pronouns and Self") rather than per-word linguistic class.

The defensible 7 [pron.] entries that remain (私, 私たち, あなた, かれ, かのじょ, じぶん, plus arguably 1 more) are all genuine pronouns. So the cleanup is targeted, not wholesale.

**Severity:** High. Internal inconsistency between two sections (だれ/どなた tagged differently in §1 vs §6) is the kind of issue that breaks any consumer relying on POS-tag uniqueness.

### 1.4 grammar_n5.md - Verb + ことができる construction not explicitly listed

**Current state:** Section 10 ("Comparison and Preference") includes `～ができます`, which covers noun + が + できる patterns like 日本語ができます ("can do Japanese").

**Missing:** Verb-dictionary + ことができる, the productive "can-do" construction:
- 日本語を話すことができます (can speak Japanese)
- ピアノを弾くことができます (can play piano)

This is a separate grammatical construction (nominalizer こと + ができる), introduced at N5 in:
- Genki I, Lesson 13 ("Potential Forms" - covers both Verb-potential and Verb+ことができる)
- Minna no Nihongo I, Lesson 18 (focused on Vる ことができる)
- Bunpro lists it as N5 grammar

The current grammar_n5.md only covers the noun-based ～ができる. A learner using this catalog will not see the productive sentence-pattern they need for "can do X" expressions until they reach N4 study materials, even though it's a textbook-canonical N5 pattern.

**Suggested fix:** add to Section 10 (or as a new sub-bullet under Section 17 Nominalization):

```markdown
- Verb (plain dictionary) + ことができる / ことができます (can do - productive form)
  - Example: 日本語を 話すことが できます。 (I can speak Japanese.)
  - Pairs with な-adj / noun + ができる; covered in Section 10.
```

**Severity:** High. A genuine N5 grammar pattern is absent from the catalog.

---

## 2. MEDIUM

### 2.1 grammar_n5.md Section 15 - もらう construction lists only `に`; `から` is also valid at N5

**Current entry:**
```
- ～に～をもらいます
```

**Issue:** at N5, the source-of-getting in もらう can be either particle:
- 友だちに本をもらいました ✓
- 友だちから本をもらいました ✓ (also N5)

Both forms appear in Genki I (Chapter 9: Giving and Receiving) and Minna no Nihongo (Lesson 7). The に form is more typical when the giver is a close person; から is more typical for institutional / non-personal sources.

**Suggested fix:** change to `～に / から ～をもらいます`. Add brief note: "Either particle is acceptable at N5; に is more common for personal givers, から for institutional sources."

**Severity:** Medium. Affects how completely a learner understands the もらう construction.

### 2.2 grammar_n5.md Section 1 - もの example combines two borderline patterns

**Current example for ～もの / もん:**
> E.g., だって、いそがしいんだもの。 - "But, you know, I'm busy."

**Problem:** this example chains TWO borderline patterns: `んだ` (Section 23.1, also tagged borderline) AND `もの` (the entry being illustrated). For a learner first encountering もの, having to parse んだ in the same example doubles the cognitive load.

**Suggested cleaner examples:**
- 行きたくないもん。(I don't wanna go.) - simple
- だって、雨だもの。(Because, you know, it's raining.) - uses bare copula instead of んだ

**Severity:** Medium. Pedagogical clarity issue, not a correctness issue.

### 2.3 grammar_n5.md Section 22 - ごはん is a poor example of bika-go (synchronically lexicalized)

**Current entry:**
> お～ / ご～ (beautifying prefixes - limited to common cases like お茶, お金, ごはん)

**Problem:** お茶 and お金 are clean examples - the お- prefix can be removed (茶, 金 - though 金 means "gold/money" without the prefix). But ごはん is etymologically ご + 飯, where 飯 alone (めし) means "rice/meal" but is masculine/rough register. Synchronically, ごはん is a single lexical word with no productive ご- alternation - learners don't say 「飯ありがとうございます」 to distinguish "thanks for meal" from "thanks for rice."

**Cleaner examples:** お茶, お金, おさけ, おみず, おはな, おちゃわん.

**Severity:** Medium. The terminological note about 美化語 vs 尊敬語 is excellent (a real pedagogical strength of this file); the example list slightly undermines it.

### 2.4 grammar_n5.md Section 4 - "Genki I L8 / L10" citation slightly off

**Current entry:**
> Question word + か / も compounds (Genki I L8 / L10):

**Issue:** in Genki I (3rd edition), the question-word + か forms (なにか, だれか, どこか) are introduced in Lesson 8. The negation-compound forms (なにも, だれも, どこも with negative verbs) are taught in Lesson 8/9 (some sources put them in 9). いつも is introduced in Lesson 11 as a frequency adverb. The "L8 / L10" citation is approximately right but Lesson 9 is more accurate for the も compounds.

This is a minor citation precision issue; the grammar content itself is correctly described.

**Severity:** Medium. Affects only the lesson-citation note, not the grammar.

### 2.5 sources.md - missing reference: official JLPT.jp sample papers

The file lists "Japan Foundation & Japan Educational Exchanges and Services (JEES)" with the URL https://www.jlpt.jp - but doesn't specifically call out the official **N5 sample paper PDFs** that the JLPT site hosts. These are:

- N5 Sample Questions page (free PDFs) - the closest thing to "what the actual test looks like" that exists outside of buying past papers
- 「JLPT N5 サンプル問題」 series

For a project building mock papers, this is the most authoritative single reference for format compliance. Worth adding as a sub-bullet under the JLPT.jp entry.

**Severity:** Medium. The site is referenced in general but the specific high-value resource within it isn't.

---

## 3. LOW

### 3.1 sources.md - could add NHK Web Easy / NHK NEWS WEB EASY for authentic N5 reading practice

NHK NEWS WEB EASY (やさしい日本語のニュース) at https://www3.nhk.or.jp/news/easy/ provides daily news rewritten for N5/N4 learners. It's the largest source of authentic-feeling N5 reading material on the open web, and is widely cited in N5 prep guides. Worth adding under "Established Learner References."

**Severity:** Low. Nice-to-have addition; not a deficiency.

### 3.2 grammar_n5.md Section 23.10 - plain prohibitive な merits a register caveat

**Current entry:**
```
- Verb-plain + な (don't do! - strong / casual prohibition)
  - Example: ここで たばこを すうな! (Don't smoke here!)
```

The `(Upper N5 / borderline)` tag handles the scope question. But pedagogically, this form is **rough** - it would only be used by someone in clear authority (parent to child, sergeant to soldier, traffic sign). A learner repeating this construction toward a peer or stranger could come across as confrontational.

**Suggested addition:** "Register: rough / commanding. Use only with clear authority differential, or in writing (signs). For polite prohibition, use ～ないでください (Section 7)."

**Severity:** Low. The pattern is correctly tagged borderline; the register caveat is polish.

---

## 4. Cross-cutting observations

### 4.1 The terminological precision in grammar_n5.md Section 22 is excellent

> **Terminology note:** お〜 / ご〜 prefixes here are **beautifying language (美化語 / bika-go)**, not honorifics (尊敬語 / sonkei-go). Honorific verbs (sonkei-go) like いらっしゃる, おっしゃる are out of scope for N5.

This is the kind of note a 上級 Japanese teacher writes when they care about students not over-applying a concept. Most beginner textbooks blur お-prefix into a vague "polite form" - this distinction is genuinely important and rarely articulated. Keep it.

### 4.2 The vocabulary_n5.md Group-1 ru-verb exception note is well-handled

> いる - [v1] to need (Group 1 exception - looks like Group 2; homophone of existence-いる which is Group 2)

This explicitly documents the homophone collision (いる "to need" vs いる "to exist" with different conjugation classes). A common stumbling block for learners. The fact that BOTH are listed in section 30 with their correct tags, and the gloss text disambiguates them, is good content design.

### 4.3 sources.md conflict-resolution rule is operationally meaningful

> **Conflict-resolution rule** - When sources disagree on whether an item is N5 or N4, **Minna no Nihongo + Genki overlap and frequency of appearance** is treated as the authoritative tiebreaker.

This is the kind of rule that's only useful if it's actually applied. Across 11 audit cycles, the project has consistently used Minna+Genki overlap to make tier-classification calls. The rule isn't decorative.

### 4.4 The previous critical bugs are largely off the books

| Prior critical issue | Current state |
|---|---|
| POS-by-section mass-tagging in vocab.json | Fixed at source; vocabulary_n5.md now correctly differentiates |
| n5-134 (ので) tier inconsistency | Fixed (now late_n5) |
| 19 empty stems in bunpou-5/6 | Diagnosed (extraction regex) - awaiting fix |
| 24 empty stems in moji-4/5/6/7 | Same root cause - awaiting fix |
| 3 wrong primary readings in n5_kanji_readings.json | Pending - 入 is now identifiable as having upstream origin in this audit |
| Audio path separator (backslash vs forward slash) | Awaiting fix |

Of the prior criticals, ~half are fixed and the rest are diagnosed with clear fix paths. **No new critical-severity issue surfaced in this audit.**

---

## 5. Recommended next-step priorities

If only 5 things get worked on:

1. **Apply `[N4+]` flags consistently in kanji_n5.md** (§1.1). 19 entries with out-of-scope readings need the flag. Pick path A (flag) or path B (strip) and apply uniformly.
2. **Reorder 入 kun readings** in kanji_n5.md (§1.2). Single-line edit: change to `Kun: はい(る), い(る), い(れる)`. Cascades to fix the n5_kanji_readings.json primary bug.
3. **Add Verb + ことができる** to grammar_n5.md Section 10 or 17 (§1.4). Three-line addition for a missing N5 construction.
4. **Fix the 6 [pron.] mistags + the もうすぐ [n.] mistag** in vocabulary_n5.md (§1.3). One-line edits each, total 7 lines.
5. **Add "from / personal source" note to もらう** in grammar_n5.md Section 15 (§2.1). Single-line addition.

The remaining items (もの example, ごはん bika-go example, JLPT.jp sample papers, NHK Easy, prohibitive な register note) are polish-grade and can be batched.

---

## 6. Quick-reference issue summary

| Severity | ID | File | Issue |
|---|---|---|---|
| HIGH | 1.1 | kanji_n5.md | 19 entries with out-of-scope readings; only 上, 下 carry the [N4+] scope flag |
| HIGH | 1.2 | kanji_n5.md | 入 kun list order has い first; should be はい first (root cause of previous primary-reading bug) |
| HIGH | 1.3 | vocabulary_n5.md | 6-7 POS-tag mistags: 人/かた/みなさん/みんな as [pron.] (should be [n.]); だれ/どなた as [pron.] in §1 vs [Q-word] in §6; もうすぐ as [n.] (should be [adv.]) |
| HIGH | 1.4 | grammar_n5.md | Verb + ことができる pattern not explicitly listed (canonical N5 grammar in Genki/Minna) |
| MEDIUM | 2.1 | grammar_n5.md | Section 15 もらう lists only に; から is also valid at N5 |
| MEDIUM | 2.2 | grammar_n5.md | もの example combines two borderline patterns (もの + んだ) |
| MEDIUM | 2.3 | grammar_n5.md | ごはん is a poor example of bika-go (synchronically lexicalized) |
| MEDIUM | 2.4 | grammar_n5.md | "Genki I L8 / L10" citation slightly off; も compounds are L9 |
| MEDIUM | 2.5 | sources.md | Missing reference: JLPT.jp official N5 sample paper PDFs |
| LOW | 3.1 | sources.md | Could add NHK NEWS WEB EASY for authentic N5 reading practice |
| LOW | 3.2 | grammar_n5.md | 23.10 prohibitive な could use a register caveat |

**Total: 11 actionable items** (0 critical, 4 high, 5 medium, 2 low).

---

## 7. Trajectory across audit cycles

| Cycle | Crit | High | Med | Low | Total |
|---|---|---|---|---|---|
| Initial markdown audit (Apr) | 5 | 7 | 9 | 6 | 27 |
| First JSON audit (Apr) | 10 | 9 | 10 | 6 | 35 |
| reading.json focused (Apr) | 5 | 5 | 6 | 4 | 20 |
| Consolidated JSON (May 1) | 1 | 4 | 5 | 2 | 12 |
| Consolidated MD (May 1) | 1 | 3 | 4 | 1 | 9 |
| Native-reviewer dossier first (May 2) | 3 | 4 | 5 | 2 | 14 |
| Native-reviewer dossier follow-up (May 2) | 0 | 0 | 0 | 0 | 0 |
| Data files audit (May 2) | 1 | 4 | 3 | 2 | 10 |
| Content files audit (May 3) | 1 | 4 | 4 | 1 | 10 |
| Infrastructure audit (May 3) | 1 | 4 | 3 | 1 | 9 |
| Paper files audit (May 3) | 1 | 4 | 5 | 2 | 12 |
| Moji + sources audit (May 3) | 1 | 4 | 5 | 2 | 12 |
| **Reference markdowns re-audit (May 4, this audit)** | **0** | **4** | **5** | **2** | **11** |

**First audit cycle without a critical-severity finding** since the project began. The trajectory is now stably in the 9-12 issue range per cycle, with critical counts having dropped from 10 (first JSON audit) through 5 / 3 / 1 / 1 / 1 / 1 / 1 / 1 / 1 / 1 to **0** in this cycle. The remaining issues are correctness-of-detail rather than systemic failures.

The corpus has matured into a state where each audit cycle finds increasingly narrow issues - a sign that the core content is solid and what remains is polish.

---

*End of audit. Prepared 2026-05-04.*
