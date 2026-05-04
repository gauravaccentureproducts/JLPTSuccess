# Native Japanese Teacher - Content Review Request

> **This file has two parts:**
> - **Part A** (§1-§11): the review brief - what to do, what's in scope, how to deliver findings.
> - **Part B** (at the bottom): a fillable findings template - copy this whole file, rename it to `feedback/pass-11-native-review-findings.md`, and replace the placeholders in Part B with your findings.

---

# Part A - Review brief

**Project:** JLPT N5 Grammar Tutor & Test (open educational web app)
**Live site:** https://gauravaccentureproducts.github.io/jlpt-n5-tutor/
**Date:** 2026-04-30
**Estimated effort:** ~10-15 hours total, splittable across sessions; partial reviews welcome
**Reviewer profile we are looking for:** native Japanese speaker who has taught N5/N4 to non-native learners (formal teaching credentials preferred but not required if you have classroom experience)

---

## 1. What this app is

A free, browser-based, no-login, offline-capable study app for learners who are wrapping up JLPT N5. It teaches all N5 grammar patterns, drills them with a 591-question bank, and runs SM-2 spaced repetition over weak items. All progress lives on the user's device; no telemetry; no accounts.

**Why we need you:** the app's correctness has been audited 10 times already, summarized below. Even after this much auditing, fresh native eyes find things prior reviewers (and automated checks) miss — especially when you read the content as a teacher would, not as a checklist.

| Pass | Lens | Findings closed |
|---|---|---|
| 1-7 | JLPT 出題者 (paper-maker / format-fidelity) review | 86 |
| 8 | 日本語教師 (native-speaker) review of `KnowledgeBank/` question banks | 52 |
| 9 | 日本語教師 (external) - content correction brief on `KnowledgeBank/` catalog files | 38 |
| 10 | TTS audio + auto-furigana correctness | 309 |
| **Total** | - | **485 closed, 0 open** |

### 1.1 Pass-10 summary (relevant context for this review)

Pass 10 closed 309 findings in two categories:
- **(a) ASCII digits in TTS-source strings** (274 cases). gTTS would have read 「3さつ」 as "three-satsu" instead of 「さんさつ」. Fixed by `tools/build_audio.py:normalize_for_tts()` which converts ASCII digits to kanji digits before gTTS. The helper is now CI-guarded (X-6.8).
- **(b) Wrong primary readings in `data/n5_kanji_readings.json`** (35 cases). Examples: 本 corrected from もと → ほん, 時 from とき → じ, 月 from つき → がつ, 学 from まな → がく, 人 from ひと → にん. The auto-furigana renderer uses the `primary` field as a fallback when no explicit furigana annotation is given. Drift here causes wrong-context rendering throughout the app.

For Pass 11, this means: if you find auto-furigana errors in the runtime UI, the underlying data is `data/n5_kanji_readings.json` (Pass-10 audited; flag as a regression if you see drift). Manual furigana annotations in JSON / MD content are a separate audit surface.

### 1.2 Project's institutional alignment

While this app is not endorsed by 文部科学省 (MEXT) or 国際交流基金 (Japan Foundation), it aspires to align with their published N5-level guidance and the JEES official sample papers. Reviewer findings that strengthen this alignment — especially via the Japanese-side authoritative sources in §7.1 — are particularly welcome.

This review (Pass 11) covers **both** the source-of-truth catalog files in `KnowledgeBank/` **and** the runtime JSON files in `data/` that the app actually serves. The two are related but not identical — `data/*.json` is derived from / inspired by `KnowledgeBank/*.md` but contains additional examples, expanded forms, and runtime-only content (questions, reading passages, listening scripts) that have never been deeply native-reviewed.

---

## 2. What we need you to do

Read the files below as a native speaker would read a textbook draft. For each entry, ask: **"Would a Japanese speaker actually say it this way?"** If the answer is no, log it.

### 2.1 Files to review (in priority order)

> **Estimate footnote:** Estimates below are for fluent silent reading. A careful audit (mental render-aloud + cross-reference against catalog rules + naturalness check) is typically **2-3× these durations**. If you find yourself going faster, you are sampling, not auditing — please note that explicitly in your findings file.

| Priority | File | What's in it | Approx. items | Estimated effort (fluent read; 2-3× for audit) |
|---|---|---|---|---|
| **P1** | `data/grammar.json` | 187 grammar patterns, each with ~5 example sentences; the runtime examples shown in every Learn lesson | **~935 example sentences** | 2-3 hours |
| **P2** | `data/reading.json` | 30 graded reading passages with comprehension questions | 30 passages, ~80 Qs | 1.5 hours |
| **P3** | `data/listening.json` + paired audio | 12 listening items across 3 JLPT formats; pair with audio QA from §2.2 | 12 scripts | 30 min + audio listen |
| **P4** | `KnowledgeBank/moji_questions_n5.md` | 100 漢字読み + 表記 questions | 100 Qs | 1 hour |
| **P5** | `KnowledgeBank/goi_questions_n5.md` | 100 文脈規定 + 言い換え類義 questions | 100 Qs | 1 hour |
| **P6** | `KnowledgeBank/bunpou_questions_n5.md` | 100 文の文法 + 文章の文法 questions | 100 Qs | 1 hour |
| **P7** | `KnowledgeBank/dokkai_questions_n5.md` | 102 短文 + 中文 + 情報検索 questions | 102 Qs | 1.5 hours |
| **P8** | `KnowledgeBank/authentic_extracted_n5.md` | 189 third-party-sourced Qs (see provenance disclosure in file header) | 189 Qs | 2 hours |
| **P9** | `data/questions.json` | 250 runtime test questions (MCQ + sentence-order + fill-in) | 250 Qs | 1 hour |
| **P10** | `KnowledgeBank/grammar_n5.md` | Source-of-truth pattern catalog (187 patterns, examples in source form) | 187 patterns | 1 hour |
| **P11** | `KnowledgeBank/vocabulary_n5.md` | 1002 vocab entries (form + reading + gloss) | 1002 entries | 1 hour |
| **P12** | `KnowledgeBank/kanji_n5.md` | 102 kanji entries (on/kun + meaning) | 102 entries | 30 min |
| **P13** | `data/vocab.json` | Runtime vocab JSON (1002 entries; mostly mirrors `KnowledgeBank/vocabulary_n5.md`) | 1002 entries | 30 min spot-check |
| **P14** | `data/kanji.json` | Runtime kanji JSON (106 entries; mostly mirrors `KnowledgeBank/kanji_n5.md`) | 106 entries | 20 min spot-check |

> **Note on P3 prioritization:** Listening was promoted from P9 to P3 because audio quality is the area where native expertise is most uniquely needed (TTS errors in pitch accent / rendaku / gemination are inaudible to non-native maintainers) and the highest-stakes pedagogically (a learner who internalizes a wrong pronunciation carries it for years).

If you only have time for one file, do **P1 (`data/grammar.json`)** — it has the highest learner exposure (every Learn lesson surfaces 4-6 of these examples).

If you have several hours, the recommended sequence is **P1 → P2 → P3 (with audio)** → one of **P4-P8** (pick the question type you teach most often).

### 2.2 Optional - audio quality (~45 min)

Listen to ~20 random MP3 files from `audio/` while reading the script in the corresponding JSON. Flag mispronunciations, wrong pitch accent, or rendaku errors. The audio is gTTS-rendered; non-native maintainers cannot judge pronunciation accurately.

### 2.3 Files we are NOT asking you to review

These are out of scope (skip):

- `data/audio_manifest.json`, `data/n5_kanji_whitelist.json`, `data/n5_vocab_whitelist.json` — generated artifacts; reviewing them would be reviewing a build output, not authored content
- `data/n5_kanji_readings.json` — covered fully by Pass-10 (audio/auto-furigana audit)
- `KnowledgeBank/sources.md` — references / meta-info, mostly English
- Anything in `js/`, `css/`, `tools/`, `tests.html`, `feedback/`, `specifications/` — code, plans, and process docs; not learner-facing JA content (apart from short UI labels which are out of this review's scope)

---

## 3. What to flag

### 3.1 IN scope (please flag)

- **Unnatural phrasing** - grammatically valid but no Japanese speaker would say it that way (例: 「電話番号は いくつですか」 should be 「何番ですか」)
- **Register clashes** - mixing politeness levels inappropriately (例: child describing own mother as 「教師」)
- **Particle errors** - especially は vs が, に vs で, を with intransitive verbs
- **Wrong readings** - especially compound rendaku, jukujikun / 熟字訓 (例: 今年 = ことし, not こんねん), and **context-sensitive readings** (例: 一日 = ついたち for the 1st of the month, but いちにち for "one day" duration; 一人 = ひとり not いちにん)
- **Two-correct-answer bugs** - any multiple-choice question where two options are grammatically valid (例: a question with both から AND ので as options when both fit)
- **Mismatched distractors** - distractors that are obviously wrong (no learning value) OR distractors that are accidentally correct
- **Inferential paraphrases sold as synonymy** (言い換え類義で類義語ではなく文脈推論を要求しているもの) - paraphrase questions where the relationship is "closest by elimination" but the rationale claims direct equivalence
- **Tense / aspect mismatches** - past-tense passage + present-tense answer, or specific-time marker (去年) combined with experience aspect (こと+ある)
- **Kanji that doesn't fit the context** - e.g., a stem using non-N5 kanji where the documented exception doesn't apply
- **Reading passage register anomalies** - child-voice mixed with formal vocabulary, or adult passage using childish phrasing
- **Vocab gloss errors** - English glosses that misrepresent the Japanese meaning or omit a critical sense
- **Kanji entry errors** - on/kun readings that don't match common N5 usage; example compounds that are not actually N5
- **Causative / passive forms** at the N5/N4 boundary - any させる / られる usage that exceeds N5 scope, or is used incorrectly (e.g., wrong intransitive/transitive pairing)
- **Counter-noun mismatches** - using まい for a non-flat object, ほん for a non-thin-long object, さつ for a non-bound-volume object, or 〜つ where a specific counter exists
- **Romaji** - any user-facing string containing romaji. Project policy is zero romaji; if found, **flag as CRITICAL** (it indicates an upstream content authoring leak)
- **Numeric representation drift** - convention is 漢数字 (一, 二, 三, ...) in narrative text and ASCII digits (1, 2, ...) in prices, addresses, schedules. Flag deviations.

### 3.2 OUT of scope (please skip)

- **JLPT format fidelity** (Mondai 1/2/3 numbering, 並べ替え format, etc.) - Pass 6 closed this comprehensively
- **Em-dashes / typography** - automated CI enforces zero em-dashes
- **Kanji-scope rule mechanics** - automated CI enforces (stems and correct-answers use only N5 kanji from `KnowledgeBank/kanji_n5.md`, except documented exceptions for reading passages)
- **Audio TTS pipeline** - Pass 10 closed the digit-normalization and primary-reading bugs
- **Coverage** - whether every grammar pattern has a question (project decision, automated check)
- **Pedagogical sequencing** - the order of patterns / categories (project decision)

If something is outside scope but you genuinely think it matters, flag it under a separate "Out-of-scope but noticed" section at the end.

---

## 4. Severity model

Use this exact taxonomy. CI gates and audit-pass logging assume these labels.

| Severity | Meaning | Example | Release impact |
|---|---|---|---|
| **CRITICAL** | Factual error, internal contradiction, or content that would teach **wrong Japanese** | Question with two grammatically-valid options; wrong reading taught (今年 = こんねん); particle error in a stem | Blocks release; we hotfix |
| **HIGH** | Unidiomatic phrasing, register clash, policy violation - jarring to a native ear but learner won't internalize wrong information | 「ははは教師です」 (too formal for own mother); 「みちを曲がる」 (should be 「角を曲がる」) | Fix in next release |
| **MEDIUM** | Pedagogical clarity issue - acceptable Japanese, but a better example exists | "Likes sports" → "plays sports often" inferential paraphrase rationale; 「ようやく」 (N3) used in N5 passage | Batch into next quarterly review |
| **LOW** | Polish / preference - suggested rewording, not a defect | Counter-form preference (一じかん vs 一時間 - both valid) | Batch into next quarterly review |

---

## 5. How to deliver findings

Please return a single Markdown file (we will ingest it as a Pass-11 audit entry in `verification.md`). Each finding follows this template:

```markdown
### F-N (severity)

**File:** `data/grammar.json` → pattern `n5-042` → example index 2
**Issue:** <what's wrong, in 1-2 sentences>
**Suggested fix:** <concrete replacement text or rule, in 1-2 sentences>
**Why:** <one-sentence native-speaker rationale - this is the part that has highest pedagogical value>
```

### Worked examples

Two examples are given so the **HIGH** and **CRITICAL** severity thresholds can be calibrated.

**Example 1 — HIGH severity (register clash, no factual error):**

```markdown
### F-12 (HIGH)

**File:** `data/grammar.json` → pattern `n5-018` → example index 3
**Issue:** Stem reads 「お母さんは 学校で きょうしです」. The polite prefix お~ on a third-person reference to one's own mother (when speaking outside the family) is a register clash; 教師 is also too formal for casual conversation.
**Suggested fix:** 「母は 学校の 先生です」.
**Why:** Within the speaker's in-group (uchi), one's own mother is referred to as 母 (no honorific) when speaking to outsiders; 先生 is the conversational form, 教師 is formal/written.
```

**Example 2 — CRITICAL severity (two grammatically-valid options):**

```markdown
### F-W2 (CRITICAL)

**File:** `data/questions.json` → question `q-0042`
**Issue:** Stem 「きょうは あつい（  ）まどを あけました」 with options 1.と 2.から 3.ので 4.が. Both から (option 2, marked correct) AND ので (option 3) are grammatically valid causal connectors. The question has two correct answers; auto-grading marks ので-pickers wrong on a defensible answer.
**Suggested fix:** Replace ので with けど (concessive; structurally distinct from causal から). New options: 1.と 2.から 3.けど 4.が.
**Why:** Multiple-choice auto-grading requires exactly one defensible answer. Two-correct-answer bugs teach learners that their correct reasoning is wrong, which is more harmful than any single content error — hence CRITICAL.
```

### Where to write your findings

The fillable template is **Part B at the bottom of this file**. Save a copy of this file as `feedback/pass-11-native-review-findings.md`, then replace the placeholders in Part B with your findings. Leave Part A untouched so the brief travels with the findings.

---

## 6. Hard constraints to respect

When suggesting fixes, please honor these project-level rules:

1. **N5 syllabus only.** Vocabulary and kanji must stay within `KnowledgeBank/vocabulary_n5.md` and `KnowledgeBank/kanji_n5.md`. If your fix introduces an N4+ word/kanji, please flag and offer an N5 alternative.
2. **No romaji** in any user-facing string.
3. **Stems and correct answers** use only N5 kanji. Distractors may use non-N5 kanji where authentic JLPT format requires (this exception is documented in the question files).
4. **Reading passages** (`data/reading.json` and `KnowledgeBank/dokkai_questions_n5.md`) carry a documented naturalness exception. The canonical allowed-set is:
   - **Family terms outside the strict N5 catalog:** 兄, 姉, 弟, 妹, 主人, 奥さん
   - **Common nouns ≥ 50% prevalence in N5 textbook corpora** (Genki / Minna / Try!): 部屋, 病院, 教室, 公園, 旅行, 仕事, 結婚, 自分, 番組, 季節, 切手, 切符, 図書館, 美術館
   - **All Japanese place names** in passages: 東京, 大阪, 京都, 北海道, 富士山, 大学名 etc.
   - **All proper-noun person names** in passages

   Anything outside this set in a passage is worth flagging. The exception applies to **passage prose only**, not to comprehension-question stems or correct-answer text — those still follow the strict N5 kanji rule.
5. **Furigana** is rendered as `<ruby><rt>` HTML in the runtime; you don't need to author furigana yourself, just flag if a reading is wrong.
6. **Polite register** (です/ます) is the default everywhere except inside reading-passage dialogue and clearly-marked casual contexts.
7. **Externally-sourced questions** in `KnowledgeBank/authentic_extracted_n5.md` are extracted from `learnjapaneseaz.com`, a third-party JLPT prep site. **They are NOT from JEES, the Japan Foundation, or any official JLPT past paper.** The file's "authentic" label has been retained for filename stability but the in-file header has been corrected to disclose the third-party provenance. If you flag one of these questions, please feel free to suggest a fix that diverges from the source — the project's bar is higher than the source's. (For Pass-12 we will consider re-sourcing this file from JEES jlpt.jp 公式サンプル問題.)
8. **Naturalness trumps policy.** If a stem or example follows every rule above but no Japanese speaker would actually produce it, flag it. The policies exist to serve naturalness, not the reverse.
9. **Numeric representation.** 漢数字 (一, 二, 三, 五, 十, 百, 千) in narrative text (e.g., 三人, 五さい); ASCII digits (1, 2, 100, 1000) in prices, addresses, schedules, time tables (e.g., 100円, 9:00). This matches authentic JLPT papers. Flag deviations.

---

## 7. Authoritative references (for fact-checking)

When sources disagree (and they often do for N5 boundary items), use your professional judgment. Flag the disagreement in the rationale so we know it was a borderline call. **When Japanese-side sources (§7.1) and Western prep materials (§7.2) conflict, Japanese-side sources prevail.**

### 7.1 Japanese-side authoritative sources (preferred for borderline calls)

- **国際交流基金 (Japan Foundation)** - https://www.jpf.go.jp - JF Standard / 「まるごと 日本のことばと文化」 A1/A2 specifications
- **JEES サンプル問題集 / 公式サンプル問題** - https://www.jlpt.jp/samples/sample09.html - publicly downloadable sample problems by level
- **旧 日本語能力試験 出題基準** (1994 / 2002 editions, 国際交流基金 + JEES) - the canonical pre-2010 Japanese-side scope document. Out of print but widely available in academic libraries; partially superseded by JF Standard but still cited
- **大学入試センター 日本語問題** - calibration reference for borderline-syllabus items
- **国立国語研究所 (NINJAL) 日本語コーパス** - https://www.ninjal.ac.jp - frequency / register / collocation reference for naturalness calls

### 7.2 Western-published / English-medium references (for cross-check)

- **Bunpro N5 deck** - https://bunpro.jp/grammar_points (~100 grammar points)
- **JLPT Sensei N5** - https://jlptsensei.com/jlpt-n5-grammar-list/
- **Genki I** (3rd ed.) - https://genki3.japantimes.co.jp/en/
- **Minna no Nihongo I**
- **Try!** N5
- **Tofugu N5 study guide**

The full annotated list of sources used by the project is in `KnowledgeBank/sources.md`.

---

## 8. Working with the project

### 8.1 How to access the files

The project is on GitHub Pages at the URL above; the repository is at https://github.com/gauravaccentureproducts/jlpt-n5-tutor. You can:

- **Read in browser:** click any file on GitHub to read it
- **Download once (no git required):** on the GitHub repository page, click the green 「Code」 button → 「Download ZIP」. This gives you the entire repository as a single .zip file. No `git` installation needed.
- **Download once (git):** `git clone https://github.com/gauravaccentureproducts/jlpt-n5-tutor`. Use this if you are familiar with git.
- **Local editor:** read locally in any text editor. VS Code is recommended for JSON files (it has built-in Japanese rendering and JSON syntax highlighting). Any plain-text editor works for the `KnowledgeBank/*.md` Markdown files.
- **Test in browser:** open `index.html` in any modern browser to see how the content renders to learners (recommended for `data/reading.json` and `data/listening.json` so you experience them as users do)

### 8.2 What you don't need to do

- You don't need to write code, run tests, or interact with Git.
- You don't need to fix anything yourself - flagging is enough.
- You don't need to read every example or every entry if your time is constrained; we'd rather get a thorough sample than a rushed full pass. **Tell us what you sampled** so we know what's still uncovered.
- You don't need to triage your findings into "what we should do" — we'll do that based on severity. Just flag everything that doesn't read right.

### 8.2.5 Language of findings

**English is preferred for ingestion** into the project's audit log, but **Japanese-language findings are welcome** — the project will translate ingested findings into the audit log. If you prefer Japanese for nuance (especially for HIGH/CRITICAL findings about pragmatics, register, or collocation), please write in Japanese. Mixed bilingual format is also fine: English for the structured fields (File / Issue / Suggested fix), Japanese for the **Why:** rationale where it captures the native-speaker observation more precisely.

### 8.3 What is unique about this project

- **No backend, no telemetry, no login.** Every fix you suggest goes into a static file that ships to the next release. Your contribution is permanent and visible.
- **Open audit history.** All 10 prior audits are documented in `verification.md` with severity tags. Your review will become Pass-11 and will be acknowledged in the same document.
- **No deadline pressure.** Take 1 week or 1 month - we'd rather have a careful pass than a fast one.

---

## 9. Logistics

- **Time:** Whatever fits your schedule; ideally split P1 (~2-3 hours) into 4-6 sessions of 30 minutes each so fatigue doesn't degrade later examples.
- **Tools:** Plain text editor (VS Code, Sublime, BBEdit, even Word) is fine. JSON syntax highlighting helps but is not required.
- **Communication:** Email or async messaging works; we don't need real-time meetings.
- **Acknowledgement:** with your permission, your name (or pseudonym, or "Native Japanese teacher") will be credited in `verification.md` Pass-11 entry and in the project CHANGELOG. If you prefer to remain anonymous, that is fine; just say so.

---

## 10. Why this matters

The app's source-of-truth `KnowledgeBank/` files have been audited 10 times. The runtime `data/*.json` files have been spot-checked but never deeply reviewed. Together they are the substance of what the learner sees.

A learner who finishes 100 lessons in this app should leave with **correct natural Japanese in their head, not weird textbook-Japanese**. That outcome depends on the files you'll be reviewing.

Your review will improve the educational quality of this app for current and future N5 candidates. The findings will be permanently logged in `verification.md` Pass-11 with severity tags, and they will inform subsequent content audits and curriculum decisions. The audit log is open and traceable; your professional contribution will be cited and acknowledged.

---

## 11. Conflict resolution

If the maintainer's interpretation of a finding diverges from your recommendation:

- **CRITICAL findings are binding.** The release does not ship until the CRITICAL is either fixed as recommended or the recommendation is renegotiated with the reviewer in writing. The audit log records the resolution.
- **HIGH / MEDIUM / LOW findings are advisory.** The project owner makes the final call, but disagreements are logged in `verification.md` so the audit history reflects both positions.
- **Reviewer override:** if you believe a HIGH/MEDIUM finding is being incorrectly downgraded to LOW or dismissed, you may flag it as "reviewer-elevated" and the project will document the disagreement publicly. Your professional reputation is not at stake on advisory items, but on CRITICAL items it is — hence the binding rule.

---

## 12. Independent verification context

The following automated and manual checks already cover certain areas, so you can deprioritize them in your review:

- **`tests.html`** runs 37 browser-runnable engine tests (SM-2 SRS algorithm, storage round-trip, furigana renderer, grading). The SRS math and storage layer are independently verified — content findings can focus on the JA itself.
- **`tools/check_content_integrity.py`** runs 18 invariants in CI: kanji catalog completeness, em-dash absence, ru-verb exception flags, primary-reading sanity, particle-set sanity, answer-key sanity, etc. CI gates the release on these. (Full list in `feedback/ui-testing-plan.md` §12.1.)
- **Lighthouse CI** gates Performance, Accessibility, Best Practices, SEO scores per release.

If your review surfaces something one of these checks should have caught (a regression of a previously-closed finding, an obvious em-dash, a Q-count drift), please flag it as **CRITICAL** with a note that "the automated check missed this" so we can extend the invariant set.

---

## 13. Contact / Acceptance

To accept this review:

1. Confirm what you'd like to review (single priority item, several, or full set; partial OK).
2. Confirm your estimated turnaround.
3. Note any clarifying questions before you start.

[Requester contact info goes here]

---

*This brief is also stored in the repo at `feedback/native-teacher-review-request.md` for archival.*

---

*Note on audit-pass numbering: the project uses sequential pass numbers (Pass 1 through Pass 11). Future passes (after Pass 20) may migrate to a year-based scheme like `Audit-2027-Q1-NatRev` for scannability, but the sequential scheme is canonical until then.*

---

# Part B - Findings (fill this in)

> Replace the bracketed placeholders below. Add as many `### F-N (...)` blocks as you need under each severity heading. Delete unused placeholder blocks. Leave Part A above untouched.

## B.1 Reviewer info

**Reviewer:** [your name / credentials, or "Anonymous native speaker"]
**Review window:** [dates - e.g., "2026-05-02 to 2026-05-08"]
**Files reviewed:** [P1 / P1+P2 / full set; sampling notes if partial]
**Total findings:** [fill in at end - CRITICAL / HIGH / MEDIUM / LOW counts]

---

## B.2 Approach

[Optional: 2-3 sentences on how you read the files. e.g. "Read all 187 patterns in data/grammar.json, sampled 5 examples per pattern. Read all 30 reading passages in full, mentally rendered them aloud. Skipped data/listening.json on this pass."]

---

## B.3 CRITICAL findings (release blockers)

### F-1 (CRITICAL)

**File:** `data/grammar.json` → pattern `n5-XXX` → example index N
**Issue:** [1-2 sentences]
**Suggested fix:** [concrete replacement text or rule]
**Why:** [native-speaker rationale, 1 sentence]

### F-2 (CRITICAL)

**File:**
**Issue:**
**Suggested fix:**
**Why:**

---

## B.4 HIGH findings (next release)

### F-N (HIGH)

**File:**
**Issue:**
**Suggested fix:**
**Why:**

---

## B.5 MEDIUM findings (next quarterly review)

### F-N (MEDIUM)

**File:**
**Issue:**
**Suggested fix:**
**Why:**

---

## B.6 LOW findings (polish)

### F-N (LOW)

**File:**
**Issue:**
**Suggested fix:**
**Why:**

---

## B.7 Out-of-scope but noticed

[Use this section for issues you spotted that fall outside the scope defined in Part A §3.2, but that you genuinely think matter. The maintainers will triage separately.]

---

## B.8 Files / patterns / passages I did NOT review

[If you skipped any items - pattern IDs, passage numbers, listening item IDs, KB question banks - list them here so the maintainers know what's still uncovered. This is honest hygiene, not a problem.]

---

## B.9 General observations

[Optional: 3-5 sentences about overall quality, recurring patterns of concern, or commendations. e.g. "The Mondai-3 paragraph passages are uniformly strong; the weak area is grammar-pattern example sentences for the te-form chain (n5-040..n5-052) where 4 of 13 patterns had unidiomatic stems."]

---

## B.10 Strategic recommendation - Japanese-language version

[Optional but valued: should this app, this brief, or both be made available in Japanese? Why or why not? Which audience would benefit most? This is strategic input only a native reviewer is positioned to give.]
