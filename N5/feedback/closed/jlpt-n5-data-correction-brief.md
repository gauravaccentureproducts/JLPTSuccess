# JLPT N5 Data Bundle — Japanese Accuracy Correction Brief

**Audit scope:** 10 attached files comprising the runtime data bundle for the JLPT N5 tutor app:
`grammar.json`, `kanji.json`, `vocab.json`, `questions.json`, `reading.json`, `listening.json`, `n5_kanji_readings.json`, `n5_kanji_whitelist.json`, `n5_vocab_whitelist.json`, `audio_manifest.json`.

**Audit lens:** Japanese-language accuracy from a seasoned 日本語教師's perspective. Focused on factual errors (wrong readings, ungrammatical sentences, mis-classified words), pedagogical errors (misleading explanations, missing rules), and internal inconsistency between files (e.g., a word in `vocab.json` not in the whitelist).

**Action required:** Apply each [CRITICAL] and [HIGH] fix. Verify each [MEDIUM] item and decide. After all fixes, run the cross-file consistency checks in §6.

**Conventions used in this brief:**
- File paths are written `file.json#path.to.field` for clarity.
- A "fix" specifies the new value or the action to take. Where multiple fixes are valid, options are labeled.
- All references to "N5 syllabus" mean the entries in `n5_kanji_whitelist.json` (106 kanji) and `n5_vocab_whitelist.json` (this corpus's authoritative scope), unless otherwise noted.

---

## 1. CRITICAL — factual errors that teach learners wrong Japanese

### 1.1 `n5_kanji_readings.json#会` — wrong on-yomi listed

**Current:**
```json
"会": { "on": ["いん", "かい"], "kun": [], "primary": "かい" }
```

**Problem:** `いん` is NOT an on-yomi for 会. The on-yomi `いん` belongs to 員 (cf. 会社員 = かいしゃいん, where いん is from 員). This appears to be cross-contamination from an adjacent entry during data generation.

**Fix:**
```json
"会": { "on": ["かい", "え"], "kun": ["あ"], "primary": "かい" }
```
- `かい` is the dominant on-yomi (会社, 会話)
- `え` is the secondary on-yomi (会釈 etc., not strictly N5 but standard for the kanji)
- `あ` is the kun-yomi (会う = あう), which IS in the N5 verb list and must be present

### 1.2 `n5_kanji_readings.json#番` — wrong on-yomi listed

**Current:**
```json
"番": { "on": ["ごう", "ばん"], "kun": [], "primary": "ばん" }
```

**Problem:** `ごう` is NOT an on-yomi for 番. The on-yomi `ごう` belongs to 号 (cf. 番号 = ばんごう, where ごう is from 号). Same kind of cross-contamination as §1.1.

**Fix:**
```json
"番": { "on": ["ばん"], "kun": [], "primary": "ばん" }
```

### 1.3 `n5_kanji_readings.json` — missing entries for 4 kanji in the whitelist

**Current state:** `n5_kanji_whitelist.json` lists 106 kanji. `n5_kanji_readings.json` only has 102. The missing four are:
- 号
- 員
- 社
- 私

**Problem:** Any feature that looks up readings by kanji will throw on these. They're standard N5 kanji.

**Fix:** Add entries:
```json
"号": { "on": ["ごう"], "kun": [], "primary": "ごう" },
"員": { "on": ["いん"], "kun": [], "primary": "いん" },
"社": { "on": ["しゃ"], "kun": ["やしろ"], "primary": "しゃ" },
"私": { "on": ["し"], "kun": ["わたし", "わたくし"], "primary": "わたし" }
```
Note: `わたくし` is the formal first-person and is the JLPT-tested kun-yomi alongside わたし. Both should be present.

### 1.4 `grammar.json` — n5-184/185/186/187 all share the wrong (copy-pasted) examples

**Current state:** Four patterns about question-word + か/も compounds all carry the same two examples, which only feature なにか/なにも:

| Pattern | Examples (current) |
|---|---|
| n5-184 (なにか / なにも) | なにか たべたいです。 / なにも たべません。 ✓ |
| n5-185 (だれか / だれも) | なにか たべたいです。 / なにも たべません。 ✗ |
| n5-186 (どこか / どこも) | なにか たべたいです。 / なにも たべません。 ✗ |
| n5-187 (いつか / いつも) | なにか たべたいです。 / なにも たべません。 ✗ |

**Problem:** Three of the four pattern entries demonstrate the wrong pattern. A learner clicking n5-185 (だれか / だれも) sees example sentences that don't contain だれか or だれも at all. This is a copy-paste propagation bug.

**Fix:** Replace examples on each as follows.

n5-185 (だれか / だれも):
```json
"examples": [
  { "ja": "だれか いますか。", "form": "question", "translation_en": "Is anyone there?", "furigana": [] },
  { "ja": "へやに だれも いません。", "form": "negative", "translation_en": "There's no one in the room.", "furigana": [] },
  { "ja": "だれかと いっしょに いきましょう。", "form": "affirmative", "translation_en": "Let's go with someone.", "furigana": [] }
]
```

n5-186 (どこか / どこも):
```json
"examples": [
  { "ja": "どこかへ いきたいです。", "form": "affirmative", "translation_en": "I want to go somewhere.", "furigana": [] },
  { "ja": "どこも こんで います。", "form": "affirmative", "translation_en": "Everywhere is crowded.", "furigana": [] },
  { "ja": "きょうは どこへも いきません。", "form": "negative", "translation_en": "Today I'm not going anywhere.", "furigana": [] }
]
```
Note: `どこへも + ません` and `どこも + ません` are both used; `どこへも` is more common when motion is involved. Keep both.

n5-187 (いつか / いつも):
```json
"examples": [
  { "ja": "いつか にほんへ 行きたいです。", "form": "affirmative", "translation_en": "Someday I want to go to Japan.", "furigana": [] },
  { "ja": "いつも 7時に おきます。", "form": "affirmative", "translation_en": "I always wake up at 7.", "furigana": [] },
  { "ja": "ちちは いつも しごとで いそがしいです。", "form": "affirmative", "translation_en": "My father is always busy with work.", "furigana": [] }
]
```

n5-184 (なにか / なにも) — current examples are fine, but expand for symmetry:
```json
"examples": [
  { "ja": "なにか たべたいです。", "form": "affirmative", "translation_en": "I want to eat something.", "furigana": [] },
  { "ja": "なにも たべません。", "form": "negative", "translation_en": "I won't eat anything.", "furigana": [] },
  { "ja": "なにか のみますか。", "form": "question", "translation_en": "Will you have something to drink?", "furigana": [] }
]
```

### 1.5 `grammar.json#n5-031` — pattern label says "informal question marker" but examples are all polite-form か questions

**Current:**
```json
{
  "id": "n5-031",
  "pattern": "informal question marker",
  ...
  "explanation_en": "か at the END of a sentence makes it a question - works with yes/no AND wh-questions...",
  "examples": [
    { "ja": "あなたは がくせいですか。" },
    { "ja": "なにを たべましたか。" },
    { "ja": "コーヒーか おちゃが いいです。" },
    { "ja": "いつ いきますか。" },
    { "ja": "これは ペンですか、えんぴつですか。" }
  ]
}
```

**Problem:** Label-content mismatch.
- "Informal question marker" (in modern Japanese pedagogy) refers to **の** at end of plain-form sentences, e.g., 「行くの?」 「どこに行くの?」 — not か.
- The displayed examples all use polite-form か questions, which are the canonical *formal* question marker, not informal.

The grammar source markdown (n5_grammar.md §2 sub-bullets of の) clearly intended "informal question marker = の" as a sub-use of の. The parser stripped that context and turned it into a standalone pattern, then populated examples from the canonical か pattern via the duplicate-cleanup mechanism.

**Fix (Option A — preferred):** Repurpose n5-031 as the informal-の question pattern that was intended:
```json
{
  "id": "n5-031",
  "pattern": "～の (informal question)",
  "category": "Particles",
  "meaning_en": "Sentence-final の as informal question marker (plain-form + の?)",
  "meaning_ja": "ふつうけい + の?",
  "explanation_en": "After plain-form verbs and adjectives, sentence-final の forms a casual / familiar question. Used with friends and family. Note: feminine speech tends to use の?; masculine plain-form often uses のか or just rising intonation on plain form alone. Don't use this in formal contexts.",
  "examples": [
    { "ja": "どこへ 行くの？", "form": "question", "translation_en": "Where are you going?", "furigana": [] },
    { "ja": "なにを たべるの？", "form": "question", "translation_en": "What are you eating?", "furigana": [] },
    { "ja": "あした 来ないの？", "form": "question", "translation_en": "You're not coming tomorrow?", "furigana": [] }
  ],
  "common_mistakes": [
    {
      "wrong": "あした 来ますの？",
      "right": "あした 来るの？",
      "why": "Informal-の attaches to PLAIN form, not polite ます-form."
    }
  ],
  "notes": "Pairs with n5-012 (formal か). Use か in polite contexts; use の in casual ones."
}
```

**Fix (Option B — if scope is fixed):** Delete n5-031 entirely as a redundant artifact of the parsing process. Document the deletion.

### 1.6 `grammar.json#n5-091` (います) — bad example sentence

**Current:**
```
"examples": [
  { "ja": "へやに ねこが います。", ... },
  { "ja": "きょうしつに がくせいが いません。", ... },
  { "ja": "きのう 友だちが 来ました。", ... }
]
```

**Problem:** The pattern n5-091 is the existence verb います (animate). The third example uses 来ました (the verb 来る = to come), which is a verb of motion, not the existence verb. This sentence has no business in the います pattern entry.

**Fix:** Replace the third example with one that actually uses います:
```json
{ "ja": "うちには いぬが 二ひき います。", "form": "affirmative", "translation_en": "We have two dogs at home.", "furigana": [] }
```

### 1.7 `listening.json#n5.listen.007` — script uses N4 grammar (～し, ～すぎる)

**Current script:**
> ぼくは あきが いちばん すきです。あきは あつくない**し**、さむくないです。たべものも おいしいです。なつは あつ**すぎ**ます。ふゆは さむ**すぎ**ます。はるは すきですが、あきの ほうが もっと すきです。

**Problem:** Two grammar items in this script are out of N5 scope:
- `～し` (parallel reasons / "and what's more") is firmly N4.
- `～すぎる` (excess; "too much") is N4 in standard syllabi (Bunpro lists it as N4; Genki II; some sources call it borderline late N5). The corpus's own `grammar.json` only includes `～すぎる` if at all in upper-N5/borderline categories — but the listening script uses it freely.

A learner who is genuinely at N5 will not parse this monologue.

**Fix:** Rewrite the script to use N5 grammar only. Suggested rewrite:
```
ぼくは きせつの 中で あきが いちばん すきです。あきは あつくないです。さむくないです。たべものも おいしいです。なつは あついですから、すきじゃありません。ふゆは さむいですから、すきじゃありません。はるも すきですが、あきが いちばん すきです。
```

This says the same thing using N5-only patterns: いちばん, から (reason), が (topic-shift "but"), いちばん again as superlative.

### 1.8 `reading.json` — 13 of 30 passages use kanji outside the project's whitelist

**Affected passages and the rogue kanji:**

| Passage | Non-whitelist kanji | Suggested action |
|---|---|---|
| n5.read.001 | 京 (in 東京) | Either add 京 to whitelist (it's in standard N5 lists) or render as とうきょう |
| n5.read.002 | 帰, 家 | Render as かえる, いえ — or add to whitelist (家 in particular is on most N5 lists) |
| n5.read.005 | 元, 兄 | Render as げんき, あに |
| n5.read.006 | 思 | Render as おもう (思います → おもいます) |
| n5.read.008 | 家 | Render as いえ — or add 家 to whitelist |
| n5.read.012 | 帰, 家 | Same as above |
| n5.read.013 | 京, 都 | Render 京都 as きょうと; the destination is N5-thematic but the kanji aren't in the project's list |
| n5.read.016 | 家, 早 | Render as いえ, はやく |
| n5.read.022 | 家, 兄 | Render as いえ, あに |
| n5.read.024 | 京 (in 東京) | Render as とうきょう, or add 京 |
| n5.read.025 | 家, 早 | Render as いえ, はやく |
| n5.read.027 | 茶 (in お茶) | Render as おちゃ; お茶 is the standard form but 茶 isn't in this project's N5 list |
| n5.read.029 | 度, 夏 | 度 → ど (kana); 夏 → なつ |

**Recommendation:** Pick ONE policy and apply it everywhere:

- **Policy A — strict whitelist:** Force every kanji rendered in any user-facing JSON to be in `n5_kanji_whitelist.json`. Render anything else in kana. (This is the policy stated in the corpus's own README and source markdown files.)
- **Policy B — naturalness exception for reading passages:** Allow common compounds like 東京, 京都, 家, お茶 in passages because these are visually natural for any Japanese reader and learners will see them everywhere. This requires expanding the whitelist or marking these as a documented "passage exception" (and updating consumers that filter by whitelist).

Whichever you pick, the current state is inconsistent: the whitelist *exists* and is enforced for vocab.json (0 violations there) but not for reading passages.

### 1.9 `reading.json` — comprehension questions use kanji not in passage

In several reading items, the question-prompt or answer-choices use non-whitelist kanji (家, 帰, 京, 都, 兄, 音, 発) that are also not in the corresponding passage's whitelist scope. This is a double violation: scope creep AND inconsistency with §1.8.

**Affected:** n5.read.001.q2, .002.q3, .003.q2, .008.q1/q2, .013.q1/q2, .015.q2, .016.q1/q2, .018.q2, .022.q2.

**Fix:** Apply the same policy decision from §1.8. If whitelist is enforced, rewrite the question stems and choices in kana.

### 1.10 `listening.json` — 4 of 12 listening scripts use kanji outside the whitelist

**Affected:**
- n5.listen.001 — uses `明` (in 明日)
- n5.listen.003 — uses `明` (in 明日), `家`
- n5.listen.004 — uses `注`, `文` (in 注文)
- n5.listen.009 — uses `知` (in 知らない)

**Note:** Listening scripts are spoken; the Japanese on the page is for the test-taker / app developer to see, not for the audio. Still, if the app surfaces these scripts to learners (e.g., as a transcript), the kanji policy applies. And `注文` carries semantic weight that can't be rendered as ちゅうもん without the learner knowing the word.

**Fix:** Apply the same policy as §1.8. If strict, rewrite to: あした (not 明日), 家 → いえ, 注文する → (paraphrase as `カフェで 男の人が 何を ください と 言っています` — but this loses naturalness). Recommend the targeted whitelist expansion to include 明, 家, 知 (all three are on standard JLPT N5 lists from JLPT Sensei, Bunpro, Tobira) before continuing.

---

## 2. HIGH — pedagogical errors that mislead but don't directly teach wrong facts

### 2.1 `grammar.json#n5-069` (Verb-て) — missing the ぐ→いで rule

**Current `form_rules.conjugations`:**
```
g1_む: む / ぬ / ぶ → んで    (のむ → のんで)
g1_く: く → いて (exception: いく → いって)
g1_す: す → して
g1_う: う / つ / る → って
g2:    Group 2: drop る + て
irreg: する → して, 来る → 来て
```

**Problem:** No entry for the **ぐ → いで** rule. This is one of the seven sound-change rules of て-form and is required for high-frequency N5 verbs:
- およぐ (to swim) → およいで
- いそぐ (to hurry) → いそいで
- ぬぐ (to take off) → ぬいで

Both およぐ and いそぐ are in `vocab.json`. A student trying to conjugate them via this rule table will fail.

**Fix:** Insert the ぐ rule between g1_く and g1_す:
```json
{
  "form": "g1_ぐ",
  "label": "ぐ → いで",
  "example": "およぐ → およいで"
}
```

Apply the same fix to the past-tense (た-form) pattern n5-067 if it exists and has the same gap.

### 2.2 `n5_kanji_readings.json` — primary readings for 高/長/安 are the wrong choice for N5

**Current:**
- 高: primary = `こう` (on-yomi)
- 長: primary = `ちょう` (on-yomi)
- 安: primary = `あん` (on-yomi)

**Problem:** At N5, the high-frequency standalone use of these kanji is the i-adjective form (kun-yomi):
- 高い (たかい) "high / expensive"
- 長い (ながい) "long"
- 安い (やすい) "cheap"

The on-yomi readings (こう, ちょう, あん) appear only in compounds that are mostly *not* in the N5 vocab list (高校 is N5; 長女 isn't; 安全 isn't until later). A furigana-or-flashcard system that displays "primary" reading first will show the wrong, confusing reading.

**Fix:**
```json
"高": { "on": ["こう"], "kun": ["たか"], "primary": "たか" },
"長": { "on": ["ちょう"], "kun": ["なが"], "primary": "なが" },
"安": { "on": ["あん"], "kun": ["やす"], "primary": "やす" }
```

For consistency, also review:
- 古: primary = `ふる` ✓ already correct
- 新: primary = `しん` — borderline, but 新しい (あたらしい) is more frequent at N5 than 新聞 (しんぶん). Consider switching to `あたら`.

### 2.3 `n5_kanji_readings.json` — duplicate kun readings polluting the lists

**Current state — duplicate entries within kun arrays:**
```
二: kun = ["ふた", "ふた"]
七: kun = ["なな", "なな", "なの"]
分: kun = ["わ", "わ", "わ"]
見: kun = ["み", "み", "み"]
聞: kun = ["き", "き"]
入: kun = ["い", "はい", "い"]    ← 「い」 listed twice
立: kun = ["た", "た"]
休: kun = ["やす", "やす"]
高: kun = ["たか", "たか"]
白: kun = ["しろ", "しろ", "しら-"]
```

**Problem:** This is artifact from stripping okurigana off entries that were originally distinguished by okurigana:
- 二: `ふた(つ)` and `ふた` → both reduce to `ふた`
- 分: `わ(ける)` and `わ(かる)` and `わ(かれる)` → all reduce to `わ`
- 見: `み(る)` and `み(える)` and `み(せる)` → all reduce to `み`
- 入: `い(る)` and `はい(る)` and `い(れる)` → reduces to `い, はい, い` (with duplicate `い`)

The semantic distinction between 入る (はいる, "enter"), 入る (いる, archaic "enter into"), and 入れる (いれる, "put in") is real and pedagogically important. Stripping the okurigana erases it.

**Fix:** The simple fix is to deduplicate, but the better fix is to preserve the okurigana-bound forms. Schema option:

```json
"入": {
  "on": ["にゅう"],
  "kun": ["はい(る)", "い(る)", "い(れる)"],
  "primary": "はい(る)"
}
```

Or, if the schema can't carry parens:
```json
"入": {
  "on": ["にゅう"],
  "kun_with_okurigana": ["はいる", "いる", "いれる"],
  "kun": ["はい", "い"],
  "primary": "はい"
}
```

Apply across all the listed entries. The minimum acceptable fix is deduplication; the maximum-quality fix preserves okurigana-binding.

### 2.4 `n5_kanji_readings.json` — convention is hiragana for on-yomi (project decision differs from standard)

**Observation:** The corpus's source markdown (`kanji_n5.md`) mandates that on-yomi be displayed in **katakana** (e.g., イチ, セン), per long-standing kanji-dictionary convention. But `n5_kanji_readings.json` stores them in **hiragana** (いち, せん) — same as kun-yomi, which makes on/kun visually indistinguishable.

**Decision needed:**
- If the runtime app converts on-yomi to katakana for display, this is fine, document it.
- If the runtime app displays the JSON values as-is, the on/kun visual distinction is lost — significant pedagogical regression vs. the source markdown.

**Recommended fix:** Normalize on-yomi to katakana in this JSON to match the project's stated convention, OR add a documented note that the runtime renderer is responsible for the conversion. Either is acceptable; ambiguity is not.

### 2.5 `grammar.json#n5-110` — sentence reading conflicts with kana convention

**Current:** "ビールを 3ぼん ください。"

**Problem:** Mixing the Arabic numeral `3` with a hiragana counter `ぼん` is awkward. JLPT papers either write `3本` (Arabic + kanji) or `さんぼん` (all kana). The `3ぼん` rendering is ungainly and can confuse novice readers about whether the rendaku さんぼん is automatic or written.

**Fix:** Standardize on one convention across all of `grammar.json` and `questions.json`. Recommended: kanji counters (3本) since the kanji 本 is in the N5 whitelist and 3 is universally readable. If that's not feasible, use `さんぼん` (all kana) and ensure no learner has to infer rendaku.

### 2.6 `grammar.json#n5-104` (Verb-stem + たいです) — example "もう ねたい。" is plain form in a polite-form pattern

**Current examples list includes:** `"もう ねたい。"`

**Problem:** The pattern is explicitly **～たいです** (polite). Three of the four examples are polite (にほんへ 行きたいです / コーヒーが 飲みたいです / なにを 食べたいですか). The fourth, `もう ねたい`, drops です — making it plain form. That's not wrong Japanese, but it's wrong for *this* pattern.

**Fix:** Either change the example to `もう ねたいです。` or move it to a separate plain-form companion pattern. If you want to demonstrate that たい-stems CAN end the sentence plainly, do so explicitly in the explanation, not silently in an example.

### 2.7 `questions.json#q-0040` — translation matches an unnatural Japanese sentence

**Current:**
```
tiles: ['まいにち', 'を', 'にほんごの', 'べんきょうします', 'ほん']
correctOrder: ['まいにち', 'にほんごの', 'ほん', 'を', 'べんきょうします']
Assembled: まいにち にほんごの ほん を べんきょうします
translation_en: I study Japanese books every day.
```

**Problem:** 「日本語の本を勉強します」 = "study Japanese books" is grammatical but unnatural. A native speaker would say:
- 「日本語を 勉強します」 (study Japanese)
- 「日本語の 本を 読みます」 (read Japanese books)

`勉強する + を + 本` reads as "study a book," which sounds odd in Japanese — the natural object of 勉強 is a subject, not a book.

**Fix:** Replace the verb tile with `読みます` so the assembled sentence becomes 「まいにち にほんごの ほんを 読みます」 ("Every day I read Japanese books"). Update translation accordingly. The pattern being tested (n5-001) is the basic copula/sentence — any natural N5 sentence works.

### 2.8 `listening.json#n5.listen.011` — prompt and answer text overlap too much

**Current:**
- prompt_ja: 「もう おなかが いっぱいです。何と 言いますか。」
- correctAnswer: 「すみません、もう おなかが いっぱいです。」

**Problem:** The prompt literally states the answer's main clause. A test-taker who can read the prompt has 80% of the answer handed to them. Compare authentic JLPT 発話表現 (utterance expression) items, which describe the situation neutrally without echoing the polite phrasing.

**Fix:** Rewrite the prompt to describe the SITUATION, not the FEELING:
```
"prompt_ja": "ともだちに ケーキを すすめられました。たべたく ありません。何と 言いますか。"
```

The test-taker now has to construct the polite refusal from the situation, not pick the option that echoes the prompt.

### 2.9 `grammar.json` — counter rule mixing in n5-110

The pattern says "Object + counter + Verb" but the example has rendaku that students need to know to read it correctly. Without a separate counter-readings module/page, the example `ビールを 3ぼん ください。` introduces さんぼん rendaku without flagging it. Add a `notes` field calling out: "Note: 三本 reads さんぼん with rendaku (連濁). See the counters reference for full reading patterns."

---

## 3. MEDIUM — content correctness with smaller pedagogical impact

### 3.1 `grammar.json` — meaning_ja entries inconsistent quality

**Observation:** Pattern entries have a `meaning_ja` field meant to give a Japanese-language label. Quality is mixed:

| Pattern | meaning_ja | Comment |
|---|---|---|
| n5-001 | ていねいな いいかた | OK |
| n5-002 | わだいの しるし | Uncommon term — `しるし` for "marker" reads as "mark/sign" generally; standard term is `じょし` (助詞). Recommended: `しゅだいの じょし` |
| n5-008 | 「いっしょに」「と」「いう」 | Quoting the words it covers — readable but stilted; better: `「と」(いっしょに、と、ひきよう)` |
| n5-009 | 「いつ・どこ から」「りゆう」 | Mixed Japanese punctuation in a Japanese label |
| n5-013 | 「〜も」 | Empty — just the form again |
| n5-019 | 「いつ」 | Empty — just the form again |

**Fix:** Either:
- Standardize: write `meaning_ja` as one short noun phrase using simple kana (e.g., `いつかを たずねる ことば` for いつ).
- Or remove the field and use a `meaning_simple_ja` only where it adds value.

The current state is half-finished and inconsistent. A 日本語教師 reviewing it would not approve as-is.

### 3.2 `grammar.json#n5-185` (and 186, 187) — ungrammatical "へも" pattern absent

When teaching どこへも and the parallel いつへも constructions (which actually appear in everyday Japanese), the pattern doesn't address them. For learners, knowing 「どこへも 行きません」 vs 「どこにも 行きません」 (both grammatical, slightly different nuance) is a meaningful N5-late distinction.

**Fix:** Add a contrast/notes section in n5-186:
```
"notes": "Both どこへも and どこにも occur. どこへも emphasizes motion ('not going anywhere'); どこにも emphasizes location ('not present anywhere'). At N5, treat them as interchangeable for negative sentences."
```

### 3.3 `vocab.json` — readings missing on hiragana-form entries that are actually pure-kana

Many hiragana-form entries have `"reading": null`. That's correct: a hiragana-form word doesn't need a separate reading. But:

- Entries like `しる` (to know) have `reading: null` and gloss `to know (Group 1 exception - looks like Group 2)`.
- Entries like `はしる` (to run) same.

**Observation:** This is correct schematically. But for the runtime app, a `reading` of null means "no reading data." If the renderer expects every entry to have a reading for SRS / TTS purposes, the null causes UX bugs.

**Fix (defensive):** Set `reading` equal to `form` for hiragana entries, so the field always has a usable value:
```json
{ "form": "しる", "reading": "しる", "gloss": "to know..." }
```

This is a schema-hygiene improvement, not a content bug. Apply systematically.

### 3.4 `vocab.json` — gloss for かれ / かのじょ is misleading

**Current:**
- かれ: "he, him (boyfriend - more advanced sense)"
- かのじょ: "she, her (girlfriend - more advanced sense)"

**Problem:** At N5, 彼/彼女 are taught primarily as boyfriend/girlfriend, not as third-person pronouns. The "boyfriend/girlfriend" sense is the *common* spoken sense; the third-person "he/she" sense is more literary. The gloss has them backwards in importance.

**Fix:**
- かれ: "boyfriend; he, him (third-person — somewhat literary)"
- かのじょ: "girlfriend; she, her (third-person — somewhat literary)"

Also: at N5, learners are taught not to use 彼/彼女 as third-person pronouns in speech because Japanese drops the pronoun. Worth a `notes` field.

### 3.5 `listening.json` — utterance-format prompts mix formality registers

**Item n5.listen.012** asks for the morning greeting to a teacher; correct answer = `おはようございます` (polite form). Good.

But other utterance items (n5.listen.011) put plain-form distractors (`ありがとう、いただきます`, `もう 一つ ください`) where the situation calls for polite refusal. A learner can identify the right answer by the politeness level alone, before parsing the meaning.

**Fix:** Make distractors share the politeness register of the correct answer where possible, so the test discriminates on meaning, not register. For n5.listen.011, the correct answer is polite (`すみません、〜`); distractors should also be polite forms with wrong meanings:
- "ありがとうございます。いただきます。" (correct register, wrong meaning — accepting)
- "すみません、もう 一つ ください。" (correct register, wrong meaning — asking for more)

### 3.6 `reading.json#n5.read.018` — non-N5 kanji 音, 発 in question stem

The reading question for passage 018 uses 音 (おと) and 発 (はつ — in 発音 = はつおん, "pronunciation"). Both are non-N5 kanji.

**Fix:** Either render in kana (はつおん, おと) or rewrite the question to avoid 発音. Since 発音 itself isn't N5 vocab, prefer rewriting.

### 3.7 `questions.json` — coverage gap (84 of 187 grammar patterns have no question)

**Observation:** Of 187 grammar patterns, only 103 have any question in `questions.json`. That includes intentional duplicates that would share questions (n5-022 redirects to n5-011 etc.), but also includes 30+ patterns with no test coverage at all.

**Fix:** Compile the list of patterns with zero coverage and prioritize question-bank growth for them. This is a content-coverage issue, not a correctness issue per se — but it directly affects the app's usability.

### 3.8 `questions.json#q-0028` and similar — situational meta-prompts use non-N5 kanji

Q-0028, q-0029, q-0032, q-0049 use stage-direction prefixes like:
- 「(自分の 手の 中の 本を みせながら)」
- 「(机の上に かばんが 何個も あります)」
- 「(友だちと 学校の 中を 歩きながら、ある へやの 前で)」
- 「(自分の ペンを みせて、それから 友だちの 手の 中の ペンを 指さして)」

**Problem:** These prefixes contain non-N5 kanji (自, 机, 個, 歩, 指).

**Fix:** Either:
- (A) Render meta-prompts in kana: 「(じぶんの 手の 中の 本を みせながら)」
- (B) Document that meta-prompt text is exempt from the N5 kanji rule, since it's framing for the test-taker (who is presumably a teacher or proficient setter), not part of the test stem.

Currently the corpus is silent on this distinction.

### 3.9 `grammar.json#n5-094` notes — 「〜があります」 is overloaded

The pattern n5-094 「〜があります」 shows three meanings packed into one entry:
- "have (ownership): 子どもが あります"
- "there is/exists (event): しけんが あります"
- "have (illness/condition): ねつが あります"

These three meanings are pedagogically distinct. A learner who sees one example might assume the pattern works the same way for all three. In practice:
- 子どもがあります — uncommon in modern Japanese; native speakers say 子どもがいます (animate).
- しけんがあります — standard.
- ねつがあります — standard.

**Fix:** Either split into sub-entries OR add a clear note: "Note: for animate possessions (children, pets), use いる/いて with possessive structure: 子どもが二人 います。 NOT 子どもが二人あります。"

### 3.10 `n5_kanji_readings.json#何` — primary `なに` may be the wrong choice

**Current:** 何 has `primary: なに`.

**Problem:** Across N5 vocabulary in `vocab.json` (何時, 何曜日, 何月, 何日, 何で, 何人), the kun reading `なん` appears far more often than `なに`. `なに` is correct for the standalone 何 in 「何ですか」, but in compounds it switches to `なん`. Setting primary to `なに` will make a furigana display show `なに` for compounds where `なん` is required.

**Fix:** This is an architectural call:
- If "primary" is for **standalone display**, `なに` is correct.
- If "primary" is the **default for furigana over the bare kanji in any context**, `なん` would be a better default because it appears in more compounds.

Document the intent and verify the renderer behaves consistently. A note in the JSON would help: `"primary_role": "standalone-only"`.

---

## 4. LOW — polish

### 4.1 `audio_manifest.json` — 489 of 629 items marked `skipped: true`

Status is OK (the build script clearly knows what it's doing), but worth verifying that the runtime app handles the skipped flag — if it tries to fetch a skipped path it'll 404. Add a release-blocker check: "no question, grammar pattern, listening item references a skipped audio file."

### 4.2 `audio_manifest.json` — backend is `gtts`

gTTS audio is robotic and lacks pitch-accent. For a JLPT N5 learner, gTTS is acceptable for short example sentences but inadequate for listening practice (where pitch and natural prosody matter). Recommend upgrading to:
- Azure Neural Japanese voices (Nanami, Keita) — best quality / lowest cost ratio
- ElevenLabs Japanese — higher quality, higher cost
- Native voice talent — gold standard but expensive

This is a quality-of-content issue, not an accuracy issue, but worth flagging since it affects the listening module's usefulness.

### 4.3 `questions.json` — half-width parens in stage directions

q-0028, q-0029, q-0032, q-0049 use ASCII `()` for stage directions while using full-width `（）` for the test blank. This is a defensible design (visually distinguishes context from test) but inconsistent with Japanese typography norms. If the project has a style guide, follow it. If not, prefer full-width across all Japanese text.

### 4.4 Schema hygiene — `furigana: []` always empty

In `grammar.json`, every example has `"furigana": []`. The field exists in the schema but is never populated. Either:
- Populate it (significant work, but adds value for the app's furigana toggle), or
- Remove it from the schema until the populator is built.

Empty fields invite future bugs.

### 4.5 `listening.json` — choice text and prompt text use の linker inconsistently

In n5.listen.001 choices: "えきの 前", "カフェの 前", "えいがかんの 前", "デパートの 前" — all use `の` linker correctly. ✓

But in n5.listen.005 choices: "おきるのが おそかったから" — uses nominalizing の plus subject が. This is grammatically fine but introduces nominalization (n5-030) inside a listening choice. Borderline; OK to keep but verify the test-taker has met n5-030 before this listening item is exposed to them.

### 4.6 `vocab.json` — missing `pos` (part-of-speech) field

The schema has `id, form, reading, gloss, section`. There's no part-of-speech tag. Without it, the app can't filter (e.g., "show only verbs") or generate inflection drills automatically. Recommend adding `pos`: noun / i-adj / na-adj / verb-1 / verb-2 / verb-3 / adverb / particle / conjunction / interjection.

This is a structural improvement that enables future features rather than a bug fix.

---

## 5. Out of scope (do not change)

- **Grammar pattern duplicate-cleanup redirects** (e.g., n5-020 redirects to n5-010): these are legitimate design choices documented in `notes` fields. Do not collapse.
- **Hiragana-only vocab forms**: deliberate per the project's kanji-rendering policy.
- **The `[Ext]` / `[Cul]` tier system** in source markdown (referenced in vocab.json sections): keep.
- **The 100-questions-per-section markdown structure**: structural, not content.
- **The `furigana: []` array** existing on every example: schema decision, leave alone (or address per §4.4).

---

## 6. Cross-file consistency checks (run after applying fixes)

These can be implemented as test scripts. Each must pass before release.

### 6.1 Whitelist consistency
- Every kanji that appears in any N5 file (grammar.json examples, kanji.json, reading.json passages, listening.json scripts, questions.json stems, vocab.json forms) must be in `n5_kanji_whitelist.json`.
- Every kanji in `n5_kanji_whitelist.json` must have an entry in `n5_kanji_readings.json` AND `kanji.json`.
- Every kanji in `kanji.json` must be in `n5_kanji_whitelist.json`.

After §1.3 fixes, this should pass with zero violations except those that the project deliberately exempts (document the exemption).

### 6.2 Reading consistency
- Cross-check every reading in `n5_kanji_readings.json` against `kanji.json`. After fixes §1.1, §1.2, §2.3, the union of (on, kun) per kanji should match (after deduplication and okurigana stripping).
- Run: for each entry in `kanji.json` and `n5_kanji_readings.json`, normalize and diff. Zero diffs.

### 6.3 Pattern reference integrity
- Every `grammarPatternId` in `questions.json` must exist in `grammar.json`. (Currently passes; keep it that way.)
- Every `grammarPatternId` referenced in `reading.json` (if any) must exist.

### 6.4 Audio reference integrity
- Every `audio` field in `listening.json`, `reading.json`, `grammar.json` (if examples have audio refs) must correspond to a non-skipped entry in `audio_manifest.json`.
- Inverse check: every non-skipped audio file in `audio_manifest.json` must be referenced by something. Orphans are dead weight.

### 6.5 Pattern–example match
- For every pattern in `grammar.json`, at least one example must contain the pattern's literal form (or a clearly inflected form of it). After §1.4 fixes, n5-185/186/187 must each contain their respective question word in examples.
- Manually review the 80+ patterns currently with shared examples (output of the audit grep) to confirm shared examples are intended duplicate-cleanup, not propagation bugs.

### 6.6 Grammar scope check (listening + reading)
- Scan listening scripts and reading passages for non-N5 grammar patterns: ～し, ～すぎる, ～ば, ～と (conditional), ～たら, plain-form citations beyond explicit pattern coverage, etc.
- Anything found should either have its pattern added to `grammar.json` (with N5 / Upper N5 tier marked) or be rewritten using N5-only constructions.

### 6.7 Numeric–counter consistency
- Sweep every counter usage. Decide on one convention: kanji counter (3本), all-kana (さんぼん), or mixed (3ぼん). Apply consistently. Document the choice in the project README.

---

## 7. Acceptance criteria

This work is complete when:

1. Every [CRITICAL] item is fixed and verified by spot-check.
2. Every [HIGH] item is fixed.
3. Every [MEDIUM] item is either fixed or has a code comment / TODO documenting why it was deferred.
4. All §6 cross-file consistency checks pass with zero violations (or with documented exemptions).
5. **A native Japanese speaker (or credentialed 日本語教師) has reviewed at least the following spot-checks:**
   - All listening scripts (12 items)
   - All 30 reading passages
   - All n5-184/185/186/187 example sets after fixing §1.4
   - The repurposed n5-031 (per §1.5)
   - The 6 kanji entries with primary-reading changes (per §2.2)
6. Total entry counts unchanged unless explicitly documented (e.g., n5-031 deletion under §1.5 Option B).

---

## 8. Recommended workflow

1. Branch: `data-content-audit-2026-04`.
2. Apply §1 (CRITICAL) fixes; one commit per item; review each independently.
3. Apply §2 (HIGH) fixes; group by file.
4. Apply §3 (MEDIUM) fixes; group by file.
5. Run §6 consistency checks; iterate until clean.
6. Have a native speaker review the high-impact diff (listening, reading, repurposed n5-031, n5-184–187).
7. Tag merged content as `data-v1.1`. App pins to this revision.

---

## 9. Quick-reference issue summary

| Severity | Count | Examples |
|---|---|---|
| CRITICAL | 10 | Wrong on-yomi for 会/番; 4 missing kanji entries; copy-paste in 4 grammar patterns; mislabeled pattern; bad example in います; out-of-scope grammar in listening; whitelist violations in reading and listening |
| HIGH | 9 | Missing ぐ→いで rule; primary readings for 高/長/安; duplicate kun readings; convention drift on katakana on-yomi; mixed-numeral counter; plain form in polite pattern; unnatural translation; prompt–answer overlap; counter rule note missing |
| MEDIUM | 10 | meaning_ja inconsistency; missing どこへも note; null readings; gloss reordering; register mixing; non-N5 kanji in question prompts; coverage gap; 〜があります overload; 何 primary ambiguity |
| LOW | 6 | gTTS quality; skipped audio refs; half-width parens; empty furigana; choice grammar inconsistency; missing POS tags |

**Total actionable items: 35** (excluding the 7 cross-file checks which are validation, not fixes).

---

*End of brief.*
