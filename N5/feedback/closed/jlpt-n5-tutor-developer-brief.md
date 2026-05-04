# JLPT N5 Tutor — Developer Instruction Brief

**Project:** `https://gauravaccentureproducts.github.io/jlpt-n5-tutor/`
**Current state:** Static SPA, GitHub Pages, hash-based routing, tabs for Learn / Test / Drill 0 / Review / Summary, furigana toggle, on-device only (no backend, no analytics).
**Goal of this work:** Turn the existing shell into a pedagogically complete JLPT N5 tutor that prepares a learner for the actual exam (vocabulary, grammar, reading, *and* listening) without sacrificing the static, privacy-preserving, on-device posture.

---

## 0. Hard constraints to preserve

These are non-negotiable and must hold after every change:

1. **Static-only.** Must continue to deploy to GitHub Pages with no server.
2. **No data leaves the device.** No analytics, no telemetry, no third-party tracking, no remote API calls during normal use. All progress, SRS state, and settings live in `localStorage` (or `IndexedDB` if size demands it).
3. **No login, no account.** Anonymous by default.
4. **Offline-capable.** Must work fully offline after first load. Implement a service worker and PWA manifest.
5. **Cross-browser.** Chrome, Firefox, Safari, Edge — last 2 versions. Mobile Safari and Chrome Android are first-class.
6. **Backups via export/import.** Because there is no cloud sync, the user must be able to export their progress to a JSON file and re-import it.

---

## 1. Curriculum scope (what content must be covered)

### 1.1 Grammar (target: full N5 set, ~80–100 patterns)

The Learn module must cover at minimum the following pattern families. Sequence them in the order below (this approximates the union of Genki I and Minna no Nihongo I, the two dominant textbooks):

- Copula: `Xはです`, `Xじゃありません`, past `でした` / `じゃありませんでした`
- Particles, in this introduction order: `は`, `も`, `を`, `が`, `に` (location of existence, time point, direction, indirect object), `で` (location of action, means/instrument), `へ`, `と` (with, and), `から`〜`まで`, `や` (non-exhaustive listing), `の` (possessive, modifier), `か` (question, alternative)
- Demonstratives: full こそあど grid — `これ／それ／あれ／どれ`, `この／その／あの／どの＋N`, `ここ／そこ／あそこ／どこ`, `こちら／そちら／あちら／どちら`
- Existence: `あります／います` with `に` and `が`
- い-adjectives: present/past, affirmative/negative, attributive vs predicative, `〜くて` connecting form
- な-adjectives: same four corners, `〜で` connecting form
- Verbs: dictionary form → polite `〜ます／〜ません／〜ました／〜ませんでした`, then plain past `〜た／〜なかった`, plain negative `〜ない`
- `〜て` form (dedicated module — see §2.2)
- `〜ています` (continuous / habitual / state — note all three uses)
- `〜てください`, `〜てもいいです`, `〜てはいけません`
- `〜たいです` (desire), `〜ませんか／〜ましょう` (invitation)
- `〜が好き／嫌い／上手／下手／分かる／ある／いる`
- Comparison: `XはYより〜`, `XとYとどちらが〜`, `〜の中で〜がいちばん〜`
- Time expressions: `〜時／〜分`, `〜年／〜月／〜日／〜曜日`, frequency adverbs (`いつも、よく、ときどき、あまり、ぜんぜん`)
- Counters (dedicated module — see §2.4)
- Question words: `何、誰、どこ、いつ、どう、どの、どれ、いくら、いくつ、どうして／なぜ`
- Conjunctions: `そして、それから、でも、しかし、〜が`
- Sentence-level: `〜から` (because), `〜とき`, `〜前に`, `〜あとで`

For each pattern, the data must include:
- Pattern ID (stable, e.g. `n5.te-form`, `n5.particle-de`)
- Form notation (e.g. `V[て] + ください`)
- 2–3 sentence English explanation written for an absolute beginner
- 4–6 example sentences with kana, kanji, English gloss, and audio
- 1–2 contrast notes against patterns that are commonly confused (e.g. `に` vs `で` for location)
- Common-mistake notes ("Learners often drop `は` here" etc.)

### 1.2 Vocabulary (~800 words)

Use a published open N5 list (e.g. the union of Genki I + Minna I + JLPT N5 vocab CSVs). Each entry needs: kanji, kana, romaji, English gloss, part of speech, audio, and a tag for which lesson/topic it belongs to (food, family, transport, school, etc.). Words should be tagged with their grammatical class so verb-group classification can be auto-derived (see §2.1).

### 1.3 Kanji (~100 N5 kanji)

For each kanji: glyph, on'yomi, kun'yomi, English meanings, stroke count, stroke-order animation or static stroke diagram, 3–5 example words drawn from the vocab list, and a `joyo` flag.

### 1.4 Reading and listening corpus

Build a corpus of ~30 short passages (80–200 characters) graded by lesson coverage. Each passage needs comprehension questions in the JLPT format (内容理解・短文／中文／情報検索). Audio recordings for every passage.

---

## 2. Modules to build or rebuild

### 2.1 Verb classification module (NEW — must come before conjugation)

**Why:** Students can only conjugate confidently if they can classify a verb on sight. Skipping this is the single most common cause of N5 conjugation breakdown.

**What to build:**
- A teaching screen that explains the three groups: Group 1 (五段 / u-verbs), Group 2 (一段 / ru-verbs, dictionary form ends in `〜iる` or `〜eる`), Group 3 (irregulars: `する`, `来る`).
- A drill mode that shows a dictionary-form verb and asks "Group 1, 2, or 3?" with immediate feedback.
- Must handle the high-frequency exceptions explicitly: `帰る`, `入る`, `走る`, `知る`, `切る`, `要る`, `しゃべる`, `すべる` are Group 1 even though they end in `〜る` after `e/i`. The drill must oversample these.
- After the user passes a threshold (e.g. 90% on 50 mixed verbs), unlock the conjugation gym (§2.3).

### 2.2 て-form gym (NEW — dedicated module)

**Why:** て-form gates almost every later pattern.

**What to build:**
- Teaching page with the full transformation table:
  - `〜う／〜つ／〜る` → `〜って`
  - `〜ぬ／〜ぶ／〜む` → `〜んで`
  - `〜く` → `〜いて` (irregular: `行く → 行って`)
  - `〜ぐ` → `〜いで`
  - `〜す` → `〜して`
  - Group 2: drop `る`, add `て`
  - Irregulars: `する → して`, `来る → きて`
- Drill mode: show dictionary form, accept て-form input via keyboard.
- Accept input as either kana or romaji (with auto-conversion).
- Mistake screen must show the rule the user violated, not just "wrong."
- Track per-ending accuracy (e.g. "you miss `〜ぐ → 〜いで` 60% of the time") and surface this in the Summary tab.

### 2.3 Conjugation gym (NEW — superset of て-form)

A four-corner grid drill: present/past × affirmative/negative, in both 丁寧形 and 普通形. Cycle through:
- Verb forms (all groups)
- い-adjective forms (note: `いい` is irregular; conjugates from `よい`)
- な-adjective forms
- Noun + copula forms

The drill should be configurable: pick which corner(s) to test, which form group(s), which verb group(s).

### 2.4 Counters module (NEW)

**Why:** Counters are an N5 weak spot that pure flashcards do not fix.

**What to build:**
- Coverage of `〜つ、〜人、〜本、〜枚、〜匹、〜冊、〜回、〜歳、〜階、〜個、〜台、〜杯、〜分、〜時、〜時間、〜年、〜か月、〜日、〜週間、〜円`
- A reading reference table with all the rendaku and irregular readings called out (`一本いっぽん／三本さんぼん／六本ろっぽん／八本はっぽん／何本なんぼん`; `一階いっかい／三階さんがい`; `二十歳はたち`; `一人ひとり／二人ふたり`).
- An image-based "how many?" drill: show a picture of N objects, ask the user to type the counted phrase. Accept kana input.
- A "pick the correct counter" drill where the user matches a counter to a noun.

### 2.5 こそあど systems page (NEW)

A single page that presents the 4-row × 4-column grid (`これ／それ／あれ／どれ` etc.) with a proximity diagram showing speaker, listener, and far-side. Drill mode selects a row+column at random and asks for the form.

### 2.6 は vs が module (NEW or reworked)

Must teach all of the following, with minimal-pair examples for each:
- `は` as topic / known information
- `が` as exhaustive-listing answer to a `誰／何／どれ` question
- `が` as neutral description (`雨が降っている`)
- `が` with stative predicates (`〜が好き／分かる／ある／いる／上手`)
- The "X has Y" pattern with `XはYがあります／います`
- Why `〜は〜が〜` is grammatical and common

Drill mode: show a sentence with both `は` and `が` blanked out, plus context, and the user fills both. Accept multiple correct answers where context allows.

### 2.7 Particle minimal-pair drills

Replace any single-correct-answer particle drill with minimal-pair items where both answers are grammatical but the meaning differs. Mandatory pairs to cover:
- `に` vs `で` (location)
- `に` vs `へ` (direction)
- `を` vs `が` (with `好き`, `分かる`, etc.)
- `と` vs `に` (with people / interaction verbs)
- `か` vs `や` (listing)

Each item must show both translations after the user answers, so the user learns the *meaning difference*, not just the "right" particle.

### 2.8 Reading passages module (NEW)

JLPT-format reading: short passages, multiple-choice comprehension questions, no time pressure in practice mode, optional timer in test mode. Difficulty must scale with which patterns the learner has unlocked (don't show passages using `〜ている` until that pattern is taught).

### 2.9 Listening module (NEW — biggest gap in current app)

**Why:** N5 listening = ~30 min, ~24 questions, roughly a third of the exam. The current app has no audio. This is the most important addition.

**What to build:**
- Native-speaker audio for every example sentence and every reading passage. If hiring native voice talent is out of scope, use a high-quality TTS (e.g. Azure Japanese neural voices, Google Cloud TTS Japanese — but cache outputs as MP3/Ogg and ship them as static assets so no runtime API call happens).
- Three drill formats matching the JLPT N5 listening section:
  1. **課題理解** (task comprehension): play audio, show 4 picture/text options, pick the correct one.
  2. **ポイント理解** (point comprehension): same shape, audio is dialogic.
  3. **発話表現** (utterance expression): show a picture, play 3 audio choices, pick the appropriate utterance.
- Speed control (0.75×, 1.0×, 1.25×) and replay button (limit to 2 replays in test mode, unlimited in learn mode).

### 2.10 Production tasks (NEW)

The current app likely tests recognition only. Add production:
- **並べ替え** (sentence reordering): show 5–7 word/phrase chips, ask the user to drag them into a grammatical sentence. This mirrors a real JLPT question type.
- **Type-the-answer** drills: short answers in kana or romaji, with a forgiving matcher (accept `わたしは` or `watashi wa`, ignore trailing punctuation, normalize half/full-width).

### 2.11 Spaced-repetition Review (REWORK existing tab)

Replace the current Review behavior with a real SRS:
- Algorithm: FSRS (preferred — modern, open) or SM-2 (simpler, well-known). Either is fine.
- State per item: stability, difficulty, due-date, lapses, reps. Persist in `localStorage`.
- Daily session: show only items due today plus a configurable number of new items (default 10).
- Grading: 4 buttons (Again / Hard / Good / Easy) feed back into the algorithm.
- Mixed-content review: grammar patterns, vocab, kanji, and conjugations all flow into the same review queue.
- "Review heatmap" calendar on the Summary tab showing streaks.

### 2.12 Diagnostic Summary (REWORK existing tab)

The Summary should be diagnostic, not just descriptive. Required sections:
- **Mastery map:** every grammar pattern, vocab item, and kanji with a color-coded mastery level (new / learning / young / mature / burned, à la WaniKani).
- **Error patterns:** auto-detected weak spots, e.g. "Particle `を` accuracy: 62%", "て-form `〜ぐ` ending: 4/12", "は vs が in exhaustive-listing contexts: 30%". These are computed from per-item error logs, not just raw scores.
- **Recommended next session:** a generated list of 5–10 items to focus on, drawn from the weak spots.
- **Session log:** chronological list of past sessions with date, items, accuracy.

### 2.13 Rename "Drill 0"

The label `Drill 0` is opaque. Rename to whatever it actually is — likely `Daily Drill`, `Mixed Review`, or `Today's Practice`. If the `0` is meaningful (e.g. drill index in a series), expose what 1, 2, 3 are too, or remove the index.

---

## 3. Cross-cutting requirements

### 3.1 Furigana with `<ruby>`

Replace any parenthesized-kana approach with semantic ruby:

```html
<ruby>日本語<rt>にほんご</rt></ruby>
```

Reasons: screen readers handle `<ruby>` correctly, copy-paste behaves better, and CSS gives finer control. The furigana toggle should hide `<rt>` via CSS (`rt { display: none }`) rather than re-render the text.

Add a per-kanji "I know this" toggle so a learner can suppress furigana on kanji they've burned, while keeping it on the rest.

### 3.2 Language metadata

Every Japanese text node must be wrapped (or its container marked) with `lang="ja"`. The page itself is `lang="en"` (or whatever the UI language is). This is required for correct font selection and screen-reader pronunciation.

### 3.3 Typography

Load **Noto Sans JP** as the primary Japanese webfont (subset to JLPT N5 + N4 character sets to keep file size down — roughly 200KB woff2). Fallback stack:

```css
font-family: "Noto Sans JP", "Hiragino Kaku Gothic ProN", "Yu Gothic", "Meiryo", sans-serif;
```

Without this, Windows machines without an installed Japanese font render some shared CJK codepoints as Chinese glyph variants, which is a real bug for kanji like `直`, `海`, `骨`, `今`, `画`.

### 3.4 Accessibility (WCAG 2.1 AA)

- All interactive controls reachable by keyboard, with visible focus rings.
- Color contrast ≥ 4.5:1 for text, ≥ 3:1 for UI controls.
- All images and audio have text alternatives.
- Audio drills must offer a transcript toggle.
- No information conveyed by color alone (e.g. correct/wrong needs a check/cross icon as well as green/red).
- Test with NVDA, VoiceOver, and TalkBack.

### 3.5 Internationalization of the UI chrome

The lesson content stays Japanese; the *interface* and English glosses should be translatable. JLPT N5 candidates worldwide are heavily Vietnamese, Indonesian, Nepali, and Chinese — not just English speakers. Build with an i18n layer (e.g. a simple `t(key)` lookup against JSON files in `/locales/{en,vi,id,ne,zh}.json`) even if only `en` ships at v1. UI language selectable in Settings.

### 3.6 Settings panel (NEW)

One screen with:
- UI language
- Furigana: always on / always off / on for unknown kanji only
- Theme: light / dark / system
- Font size: S / M / L / XL
- Audio speed default
- Daily new-card limit
- Daily review cap
- Reset progress (with double confirm)
- Export progress (downloads `progress.json`)
- Import progress (uploads `progress.json`)

### 3.7 Performance

- First contentful paint < 1.5s on 4G.
- Total initial JS bundle < 100KB gzipped. Lesson data, audio, and stroke diagrams lazy-load on demand.
- Skeleton screens instead of "Loading...".
- Service worker caches the shell and any visited lesson data; subsequent loads are instant and offline-capable.

### 3.8 PWA

Add a `manifest.webmanifest` with proper icons, name, and `display: standalone` so the user can install the app to their home screen on mobile. Required because the typical N5 learner studies on a phone.

---

## 4. Data schema (suggested)

All data ships as static JSON in `/data/`. Suggested shapes:

### `grammar.json`

```json
{
  "id": "n5.te-form",
  "title": "て-form",
  "category": "verb-conjugation",
  "lesson": 14,
  "prerequisites": ["n5.verb-groups", "n5.masu-form"],
  "explanation_md": "...",
  "patterns": [
    { "form": "V[て]", "english": "and (then) / connecting" }
  ],
  "examples": [
    {
      "ja_kanji": "ご飯を食べて、コーヒーを飲みます。",
      "ja_kana":  "ごはんをたべて、コーヒーをのみます。",
      "en": "I eat a meal and (then) drink coffee.",
      "audio": "/audio/n5.te-form.ex01.mp3"
    }
  ],
  "common_mistakes": [
    "Confusing 〜く verbs (書く → 書いて) with the 行く exception (行く → 行って)."
  ]
}
```

### `vocab.json`

```json
{
  "id": "n5.vocab.tabemono",
  "kanji": "食べ物",
  "kana": "たべもの",
  "romaji": "tabemono",
  "en": "food",
  "pos": "noun",
  "tags": ["food", "genki-l3"],
  "audio": "/audio/vocab/tabemono.mp3"
}
```

### `kanji.json`

```json
{
  "id": "n5.kanji.食",
  "glyph": "食",
  "on": ["ショク", "ジキ"],
  "kun": ["た.べる", "く.う", "く.らう"],
  "meanings": ["eat", "food"],
  "strokes": 9,
  "stroke_order_svg": "/svg/kanji/食.svg",
  "examples": ["n5.vocab.taberu", "n5.vocab.tabemono", "n5.vocab.shokudou"]
}
```

### `srs_state` (in `localStorage`)

```json
{
  "n5.te-form": {
    "stability": 4.2,
    "difficulty": 0.3,
    "due": "2026-05-03",
    "lapses": 1,
    "reps": 7,
    "history": [
      { "ts": "2026-04-29T10:12:33Z", "grade": 3 }
    ]
  }
}
```

---

## 5. Tech recommendations (non-binding)

- **Framework:** Vanilla JS, Preact, or Svelte. Avoid heavy frameworks — bundle size matters and there is no SSR need.
- **Build:** Vite with the `vite-plugin-pwa` plugin.
- **State:** Zustand or a small custom store; SRS state in `localStorage`, larger logs in `IndexedDB` via `idb-keyval`.
- **Routing:** Continue with hash-based routing for GitHub Pages compatibility.
- **Audio:** `<audio>` element with preload="none"; cache via service worker.
- **Stroke order:** SVG with CSS-animated `stroke-dasharray`, or static numbered diagrams.
- **TTS pipeline (build-time):** Generate MP3 files once during build, commit to repo or to a separate assets repo. Do not call TTS at runtime.

---

## 6. Acceptance criteria (per feature)

A feature is "done" only when all of the following hold. Apply this checklist to each module above.

1. **Functional:** every documented behavior works in Chrome, Firefox, Safari, Edge, Mobile Safari, Chrome Android.
2. **Offline:** feature works after the page is loaded once, with the network disabled.
3. **Accessible:** keyboard-navigable, screen-reader-tested, contrast meets WCAG AA.
4. **Localized:** every UI string flows through the i18n layer (no hardcoded English in JSX/HTML).
5. **Persistent:** any learner state generated by the feature survives page reload and is included in export/import.
6. **Performant:** module's JS adds < 30KB gzipped to its route's bundle; module's data lazy-loads.
7. **Documented:** README has a one-paragraph description of the module and the data files it consumes.
8. **Tested:** at least smoke tests for the happy path; SRS algorithm has unit tests for grading and scheduling.

---

## 7. Phasing (suggested order of work)

**Phase 1 — Foundation (highest leverage, fixes the biggest gaps):**
1. Add native-speaker / TTS audio to all existing example sentences.
2. Replace Review with a real SRS (FSRS or SM-2).
3. Rebuild Summary as a diagnostic dashboard.
4. Rename "Drill 0" and clarify navigation labels.
5. Migrate furigana to `<ruby>`; set `lang="ja"`; load Noto Sans JP.

**Phase 2 — Curriculum completeness:**
6. Verb classification module + drill.
7. Dedicated て-form gym.
8. Counters module with image drills.
9. こそあど systems page.
10. は vs が module with minimal pairs.
11. Particle minimal-pair drills replacing any single-answer particle drills.

**Phase 3 — Test fidelity:**
12. Listening module with all three JLPT N5 listening question types.
13. Reading passages module with comprehension questions.
14. 並べ替え production drills.
15. Type-the-answer production drills with forgiving matcher.

**Phase 4 — Polish and reach:**
16. Settings panel (themes, font sizes, language).
17. PWA + service worker + offline.
18. i18n with at least English; structure ready for VI/ID/NE/ZH.
19. Export/import progress.
20. Accessibility audit pass.

---

## 8. Out of scope (do not build)

- User accounts, social features, leaderboards.
- Cloud sync (export/import covers this).
- Anything beyond N5 in this codebase. (If N4+ is wanted, fork.)
- Speaking practice with microphone input (out of N5 exam scope and adds complexity).
- AI-generated content at runtime. Any AI use must happen at build time and bake outputs into static assets.

---

## 9. QA checklist before any release

- [ ] Loads with JS-only (no console errors).
- [ ] Loads under 1.5s FCP on simulated 4G.
- [ ] Works fully offline after one online load.
- [ ] All Japanese text renders in a Japanese font on a clean Windows machine without Japanese language pack.
- [ ] Furigana toggle hides/shows ruby across the entire app.
- [ ] Audio plays on iOS Safari (this is historically broken — verify autoplay policies).
- [ ] Export → wipe → import round-trips progress without loss.
- [ ] Lighthouse: Performance ≥ 90, Accessibility ≥ 95, Best Practices ≥ 95, SEO ≥ 90, PWA installable.
- [ ] Screen reader announces "に, particle" not "ni" or silence when reading drills.
- [ ] No outbound network calls during a normal learning session (verify in DevTools Network tab with cache disabled).

---

## 10. Notes for the developer

- The pedagogical priority is **listening + SRS + diagnostic feedback**. Those three deliver the biggest learning gain per hour of dev work and address the current app's largest gaps.
- Resist the temptation to add more grammar patterns before the existing ones have audio and SRS.
- Resist adding gamification (streaks, XP, badges) until SRS works correctly. Gamification on top of broken pedagogy makes the problem harder to see.
- When in doubt about whether a feature is in N5 scope, check the official JLPT sample questions at `https://www.jlpt.jp/e/samples/sampleindex.html` and the Genki I / Minna no Nihongo I tables of contents.
- Write data files in a way that a non-developer (e.g. a Japanese teacher contributor) could edit them. JSON is fine; YAML is friendlier; either way avoid burying content in TypeScript files.

---

*End of brief.*
