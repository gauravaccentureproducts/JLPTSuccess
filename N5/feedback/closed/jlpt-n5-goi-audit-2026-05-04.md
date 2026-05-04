# JLPT N5 — Goi Section Audit Report

**Scope:** Papers 1–7 (Q1–Q100), 100 multiple-choice items in total.
**Auditor lens:** Native-speaker teacher / JLPT-aligned item review.
**Audit criteria applied:**

1. Is the keyed answer the *uniquely* correct answer? (No defensible alternative among the distractors.)
2. Is the stem unambiguous? (Sufficient context to force a single reading.)
3. Is the Japanese natural and idiomatic?
4. Is the item level-appropriate for N5? (Grammar/vocabulary should not require N4+ structures unless they are common N5 set phrases.)
5. Are paraphrase items (Papers 4–7) genuine paraphrases, or are they "best of bad options"?
6. Are counters, particles, kana/kanji conventions consistent with N5 norms?

---

## Executive summary

The papers are, on the whole, soundly constructed for N5 and the keyed answers are correct in roughly 90 of 100 items. The issues cluster in three areas:

- **Paraphrase items where the keyed answer is "best by elimination" rather than a true synonym.** Paper 6 and Paper 7 are most affected. Several of these are already flagged in the rationale field, which is honest, but a JLPT-style paper should not ship items where the rationale itself admits the gloss is approximate. These items either need stronger distractors or a tightened stem.
- **A small number of items where the keyed answer is genuinely wrong, ambiguous, or where the Japanese is unnatural.** Q21, Q89, Q98, Q99 are the standouts. These need replacement or rewriting.
- **Level creep.** Roughly half a dozen items lean on N4 grammar (potential form, ～たことがある, ～つもりだ, ～あいだに, ～までに as a contrast point). Some of this is unavoidable at the boundary, but it should be deliberate, not incidental.

The worst offenders are concentrated in Paper 7, which I would re-examine question by question before shipping.

---

## Critical issues (require fixing before publication)

### Q21 (goi-2.6) — Stem has no disambiguator; all four positional answers are valid

```
ほんは つくえの （　　） に あります。
   うえ / した / まえ / うしろ
```

A book can plausibly be **on, under, in front of, or behind** a desk. The rationale notes that this stem "Replaces a previous stem … where all four positions … were grammatically defensible because the stem provided no directional anchor." But the replacement has the **same defect**: there is no anchoring information that forces うえ. うえ is the most *probable* placement, but probability is not what JLPT items test — they test which option the stem licenses.

**Fix:** Add an anchor that rules out the other three. For example:
- `ほんは つくえの （　　） に あります。よみたい ときは すぐ とれます。` → うえ becomes uniquely natural.
- Or change the noun: `しんぶんは いすの （　　） に あります。` is no better; you need a context word like 「おちて います」, 「すわって よみました」, etc.

### Q98 (goi-7.8) — Keyed answer is not a valid paraphrase

```
A: しゅくだいは あした まで に だして ください。
Keyed: あしたの あさまで しゅくだいを 出して ください。
```

Two independent problems:

1. **Particle change is semantic, not cosmetic.** ～までに marks a deadline by which a punctual action must occur. ～まで marks a continuous endpoint. With 出す (a punctual verb), ～まで is grammatically odd in standard Japanese — you cannot "keep submitting" until morning.
2. **The time window has been narrowed.** 「あしたまでに」 = any time before the end of tomorrow. 「あしたのあさまで」 = before tomorrow morning. These are different deadlines.

**Fix:** Replace the keyed option with `あしたまでに しゅくだいを 出して ください。` (which would be a trivial restatement and thus too easy — so the real fix is to rewrite the stem so that a non-trivial paraphrase exists, e.g. test ～までに ↔ ～のうちに, or test 出す ↔ 提出する at a higher level. At N5, this concept may simply be too thin to build a four-way item around).

### Q99 (goi-7.9) — 知っている and 覚えている are not synonyms

```
A: あの 人の 名前を しって いますか。
Keyed: あの 人の 名前を おぼえて います。
```

The rationale itself states "Don't memorize this as a synonymy rule." That is a tell that the item is unsound. 知っている = "I have knowledge of"; 覚えている = "I retain in memory." A learner can 知っている a name without 覚えている it (knew it, then forgot), and they cannot 覚えている what they have never 知っている. The two overlap in a narrow set of contexts but are not interchangeable.

**Fix:** This item should be replaced. Plausible N5-level replacements for 知っている paraphrase:
- `あの 人の 名前が わかりますか。` (knowledge ↔ understanding) — though this also has its own issues.
- Or change the prompt verb to one with a cleaner paraphrase partner.

### Q94 (goi-7.4) — Negation strength mismatch

```
A: この みせの ケーキは あまくないです。
Keyed: この みせの ケーキは あまり あまく ないです。
```

`～くない` is a flat negation ("is not sweet"). `あまり ～ない` is a graded negation ("is not very sweet"). At N5 these are routinely conflated in casual student speech, but a graded test item should not. The other three options are clearly wrong (opposite polarity, unrelated taste, unrelated property), which is why this is solvable — but the keyed answer is technically incorrect.

**Fix:** Replace one distractor with a true paraphrase, e.g. `この みせの ケーキは あまい あじが しません。`, or change the stem to `あまり あまく ないです` and key `あまい ケーキでは ありません` for the inverse direction.

---

## Moderate issues (should fix)

### Q89 (goi-6.14) — Unnatural Japanese in keyed option

```
A: その くつは 高かったです。
Keyed: その くつは とても たかい おかねを はらいました。
```

「高い お金」 is awkward. Money itself is not 高い / 安い — *prices* are. A native speaker would write `たくさん お金を はらいました` or `ねだんが 高かったです`. The intended meaning is clear, but the phrasing is the kind of thing the test would never ship as a model sentence.

**Fix:** Rewrite the keyed option as `たくさん お金を はらいました。`

### Q39 (goi-3.9) — Wrong counter for the noun

```
きょうしつには つくえが 五（　　） あります。
Keyed: つ
```

机 is canonically counted with **〜台 (だい)**. つ is the generic native counter and is taught at N5, but it is not idiomatic with furniture. A test paper should either swap the noun (e.g., りんご, ボール, ケーキ — items where 〜つ is natural) or introduce 〜台 as the option. As written, the keyed answer would be marked down by a native marker.

**Fix:** Replace the noun, e.g. `きょうしつには ボールが 五（　　） あります。` and keep 〜つ as the answer.

### Q79 (goi-6.4) vs Q80 (goi-6.5) — Inconsistent caveating of the same logical pattern

Both items paraphrase a negated i-adjective as its lexical antonym:
- Q79: `大きくない` → `ちいさい` (no caveat in rationale)
- Q80: `あつくない` → `すずしい` (rationale acknowledges that あつくない is broader than すずしい)

Both have the same logical issue (negation ≠ antonym; "not big" admits 中ぐらい). Either both should carry the caveat or, better, both should be rewritten so the paraphrase is exact.

**Fix:** Either accept the N5-level approximation in both rationales, or rewrite one of them with a true antonym pair (e.g., 多くない / 少ない is similarly loose; 高くない / 安い is a cleaner pair if the topic is price).

### Q68 (goi-5.8) — Quantifier scope shift

```
A: だれも きょうしつに いません。
Keyed: きょうしつに 学生が いません。
```

`だれも` is universal over people. `学生が いません` only covers students — a teacher or staff member could be in the room. The two are not equivalent. The other three options have wrong cardinalities, so the item is solvable, but the paraphrase under-translates.

**Fix:** Replace the keyed option with `きょうしつに 人が いません。` or `きょうしつに ひとりも いません。`

### Q70 (goi-5.10), Q76 (goi-6.1), Q86 (goi-6.11), Q97 (goi-7.7), Q100 (goi-7.10) — "Like / good at / learning" → "do often / can do well / practice"

These all rely on a real-world inference rather than semantic equivalence:
- 好き ↔ よくする (one can like sports without doing them — fans, viewers).
- 上手 ↔ よく話せる (上手 covers all four skills, not just speaking).
- 電話をかける ↔ 電話で話す (calling does not entail conversation — it could go to voicemail).
- 習っている ↔ 練習している (lessons ≠ practice).

Each rationale already acknowledges the gap. Individually they are tolerable at N5. **As a cluster** they are a pattern: the paper consistently treats real-world inference as paraphrase. I would tighten at least two of them so that the pattern doesn't dominate.

### Q82 (goi-6.7) — Weather framing assumes a value judgment

```
A: きょうは あめが ふって います。
Keyed: きょうは てんきが よくないです。
```

Conventional Japanese usage does treat 雨 as 天気がよくない, so this is acceptable — but it is a cultural convention, not a logical equivalence. A farmer waiting for rain might call rainy weather 「いい 天気」. For an N5 test this is fine; flag it for awareness.

---

## Minor issues / stylistic flags

- **Q1 (goi-1.1):** `毎あさ` — the kanji-kana split is awkward. Standard N5 spelling would be either `まいあさ` (all kana) or `毎朝` (all kanji). Mixed forms appear elsewhere too (`ばんごはん` next to `見ます`, etc.). Consider running a kana/kanji consistency pass across all stems.
- **Q5 (goi-1.5):** Tense skew between `つかれました` (past) and `やすみます` (non-past) is acceptable but inconsistent. `つかれたから、いえで やすみます` reads more naturally.
- **Q10 (goi-1.10):** `あつい` is a homophone (暑い / 厚い). A book *can* be 厚い. The intended answer おもしろい is clearly more idiomatic, and the stem is fine, but be aware that a sharp learner might pause here.
- **Q12 (goi-1.12):** `はなして` is keyed; `いって` would also work in the request-for-repetition idiom. Not a defect, just a near-tie distractor.
- **Q19 (goi-2.4):** Stem `きのうは とても` is light on context — the answer 忙しかった works because the other options are ungrammatical (`つよいでした`) or wrong-tense, not because the stem points there. Consider adding a topic word.
- **Q27 (goi-2.12):** つぎの みち is a real construction in navigation. かど is the better answer, but みち is not a clean wrong answer.
- **Q33 (goi-3.3):** `つかれたので すぐ すわりました` — semantically `すぐに` would be more standard than the bare adverb `すぐ` before a verb. N5 allows bare すぐ, so this is borderline.
- **Q45 (goi-3.15):** `コート` is the intended cold-weather garment, but `シャツ` paired with `きる` is also possible (a shirt can be worn when cold). Distractor is weak; consider replacing シャツ with something clearly indoor (e.g., パジャマ).

---

## Level-appropriateness flags (N4 leakage)

These items rely on grammar that is canonically tested at N4 rather than N5. In some cases the structure has become a frozen N5 set phrase and is acceptable; in others it is genuinely above level. Flagged for review:

- **Q47 (goi-4.2):** `～たことがあります` — N4 grammar. Common enough at the N5/N4 boundary to keep, but be aware.
- **Q48 (goi-4.3):** `～つもりです` — N4 grammar. Above level for a strict N5 paper.
- **Q62 (goi-5.2):** `～あいだに` — N4 grammar. Above level.
- **Q64 (goi-5.4):** Potential form `ひけます` — N4 grammar. Above level.
- **Q91 (goi-7.1):** `～て、Nに なります` (duration construction) — borderline N4.
- **Q97 (goi-7.7):** Potential form `話せます` — N4 grammar.

If these papers are positioned as strict N5, six items pulling from N4 grammar in the keyed option is too many. If they are positioned as "N5 with stretch," it is fine but should be declared.

---

## Consolidated issue list

| # | Item | Severity | Issue | Recommended action |
|---|---|---|---|---|
| 1 | Q21 / goi-2.6 | Critical | All four positional options are valid; stem has no anchor | Add disambiguating context, or replace stem |
| 2 | Q98 / goi-7.8 | Critical | Keyed option changes both particle (までに→まで) and time window | Replace keyed option or replace whole item |
| 3 | Q99 / goi-7.9 | Critical | 知っている / 覚えている are not synonyms; rationale admits it | Replace item |
| 4 | Q94 / goi-7.4 | Critical | あまくない ≠ あまり あまくない (negation strength) | Replace one distractor with a true paraphrase |
| 5 | Q89 / goi-6.14 | Moderate | 「高い お金を 払う」 is unnatural Japanese | Rewrite as 「たくさん お金を 払いました」 |
| 6 | Q39 / goi-3.9 | Moderate | 机 takes 〜台, not 〜つ | Swap noun (e.g., ボール / りんご) or change counter set |
| 7 | Q79 vs Q80 | Moderate | Same logical pattern, inconsistent caveating | Align treatment; ideally rewrite to genuine antonym pair |
| 8 | Q68 / goi-5.8 | Moderate | 「だれも」 → 「学生が」 narrows scope | Use 「人が いません」 or 「ひとりも いません」 |
| 9 | Q70, Q76, Q86, Q97, Q100 | Moderate (cluster) | Like/skill/lessons → action paraphrases rely on real-world inference | Tighten at least two items in the cluster |
| 10 | Q82 / goi-6.7 | Minor | Weather paraphrase relies on cultural convention | Acceptable; flag for awareness |
| 11 | Q1, plus general | Minor | Mixed kana/kanji spelling (`毎あさ` etc.) | Consistency pass across all stems |
| 12 | Q5 / goi-1.5 | Minor | Past–nonpast tense skew | Either keep both past or both nonpast |
| 13 | Q10 / goi-1.10 | Minor | あつい homophone (暑い/厚い) — 厚い book is plausible | Optional; replace あついです with clearly wrong distractor |
| 14 | Q12 / goi-1.12 | Minor | いって would also fit | Acceptable; flag for awareness |
| 15 | Q19 / goi-2.4 | Minor | Stem light on context | Add a topic word |
| 16 | Q27 / goi-2.12 | Minor | つぎの みち is also defensible | Acceptable |
| 17 | Q33 / goi-3.3 | Minor | Bare すぐ before verb; すぐに more standard | Optional |
| 18 | Q45 / goi-3.15 | Minor | シャツ is a weak distractor for a "wear when cold" prompt | Replace with clearly indoor garment |
| 19 | Q47, Q48, Q62, Q64, Q91, Q97 | Level | Keyed answer relies on N4 grammar | Decide policy: strict N5 vs N5+stretch; replace if strict |

---

## Recommended next steps

1. **Triage the four critical items first.** Q21, Q94, Q98, Q99 should not ship in their current form. Q98 and Q99 in particular are the kind of items that, if they appeared on a real test, would be invalidated post-hoc by the testing body.
2. **Decide a policy on the inference-style paraphrases.** If you are content to teach "好き ≈ よくする" as an N5 rule of thumb, document that decision and stop apologizing for it in the rationale field. If you are not, rewrite the cluster.
3. **Run a kana/kanji and counter consistency pass.** This is mechanical and will sharpen the polish of the whole set.
4. **Make the N5 / N4 boundary explicit.** Either remove the six N4-grammar items or label this as a "late N5 / early N4" set so the level claim matches the content.
