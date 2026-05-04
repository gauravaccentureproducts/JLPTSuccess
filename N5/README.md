# JLPT N5 Grammar Tutor

Browser-based static web app for studying JLPT N5 grammar. **No build step. No server. No accounts.**

## Run locally

Open `index.html` in a modern browser (Chrome, Edge, Firefox).

> Some browsers block `file://` JSON fetches. If pages stay blank, serve over HTTP:
> ```
> python -m http.server 8000
> ```
> Then open http://localhost:8000.

## Deploy to GitHub Pages

1. Commit and push this folder (or its parent repo) to GitHub.
2. **Settings → Pages → Source** = `main` branch, root folder (or `/docs` if you nest the app under that).
3. After the first build (~30 seconds), visit `https://<your-user>.github.io/<repo>/JLPT/N5/` (or wherever the app lives in your repo).
4. Verify the four chapters load: Learn, Test, Drill, Summary. Take a quick test, miss something, and confirm the Drill badge updates and Chapter 3 / 4 reflect it.

The app uses **only relative paths** and **hash routing** (`#/learn`, `#/test`, …), so it works without any path-rewriting on GitHub Pages - no `404.html` fallback, no `gh-pages` action, nothing else needed.

A **service worker** (`sw.js`) is included and pre-caches the app shell + all data files. After your first online visit, the app continues to work offline. Bump `CACHE_VERSION` in `sw.js` when shipping a release so old caches get evicted.

## File map

```
/index.html                            entry point
/sw.js                                 service worker (offline cache)
/css/main.css                          styling
/js/                                   app logic (one module per chapter / mode)
  app.js storage.js furigana.js
  learn.js test.js review.js summary.js drill.js diagnostic.js
/data/                                 JSON consumed by the app
  grammar.json questions.json
  n5_kanji_whitelist.json n5_vocab_whitelist.json n5_kanji_readings.json
/tools/                                Python scripts run by the content author only
  build_data.py check_coverage.py lint_content.py
  build_spec.py generate_stub_questions.py
/KnowledgeBank/grammar_n5.md           canonical N5 pattern catalog (human source-of-truth)
/KnowledgeBank/kanji_n5.md             N5 kanji catalog with on/kun readings
/KnowledgeBank/vocabulary_n5.md        N5 vocab catalog
/KnowledgeBank/sources.md              reference / authority documentation
verification.md                        cross-source audit of KnowledgeBank content
TASKS.md                               task list (mirrors session TodoWrite)
JLPT N5 Grammar Tutor – Functional Spec.docx     full functional spec
```

## Content authoring workflow

1. Edit the markdown source-of-truth files in `KnowledgeBank/` (`grammar_n5.md`, `kanji_n5.md`, `vocabulary_n5.md`).
2. Edit rich content in `data/grammar.json` and `data/questions.json` (the app consumes these).
3. Regenerate whitelists + kanji-reading map from the markdown:
   ```
   python tools/build_data.py
   ```
4. Verify pattern coverage:
   ```
   python tools/check_coverage.py
   ```
5. Lint for out-of-scope kanji + vocab tokens:
   ```
   python tools/lint_content.py
   ```
6. (Optional) Generate stub MCQ questions for any patterns missing one:
   ```
   python tools/generate_stub_questions.py
   ```
7. (Optional) Regenerate the spec docx:
   ```
   python tools/build_spec.py
   ```

The learner never runs any of these scripts - they are author-side only.

## Authoring conventions

### Vocabulary whitelist exemptions

The `data/n5_vocab_whitelist.json` lookup is the source of truth for "what counts as N5 vocabulary." Two classes of items are intentionally excluded from the whitelist:

1. **Personal names** (e.g., マリア, ヤマダ, スズキ, たなか, アンナ) — universally exempted from textbook vocabulary lists. Names appear in passages and questions but never in the whitelist; CI does not flag this. If you add a new passage with a new personal name, do NOT add the name to the whitelist.
2. **Place names with no compound logic** (e.g., スペイン, アメリカ, メキシコ) — country names already in the whitelist are fine. Compound forms like スペイン人 / アメリカ人 are tracked since they're useful learner vocabulary. Don't bulk-add every conceivable place name.

Where to add: append the new term to `data/n5_vocab_whitelist.json` (sorted alphabetically) and run `python tools/check_content_integrity.py` to confirm the JA-13 / JA-15 / JA-16 invariants still pass.

### Spacing policy in passages

Insert a single space at every word boundary in `ja` text — particles, kanji compounds, demonstrative + noun, etc. The corpus is consistently spaced; new content must match.

- ✓ `わたしは とうきょうの 大学で 日本語を べんきょうしています。`
- ✗ `わたしは とうきょうの大学で 日本語を べんきょうしています。` (missing space before 大学)

Exceptions: spaces are NOT inserted within a single compound (e.g., `日本語` stays as one token; do not split as `日本 語`).

### N4 grammar leakage

N5 passages must use only N5 grammar markers. The two patterns most likely to slip through are:

- **〜と conditional** (`Verb-dict + と + comma + result-clause`) — this is N4 (Genki II L18, Minna I L23). Use te-form imperative or split into two sentences instead.
- **Potential form** (`Verb-stem + える/られる`) — this is N4 (Genki II L13). Use `Verb-dict + ことが できる` instead.

The `JA-21` content-integrity invariant catches both heuristically. Passages that intentionally include borderline late-N5 grammar should set `tier: "late_n5"` to opt out of the strict check.

### Kanji reading display convention

`data/n5_kanji_readings.json` stores both `on` and `kun` readings as **hiragana** (e.g., 高 → on `["こう"]`, kun `["たか"]`). This is a deliberate choice — the traditional pedagogical convention is on-yomi in katakana / kun in hiragana, but uniform-hiragana is simpler to render, easier to compare for invariant checks (JA-22 dedup, JA-24 i-adj-primary-kun), and the on/kun distinction is already conveyed via the labelled fields. UI surfaces that want the typographic split can apply it at render time. Closes OPEN-4 from `feedback/MASTER-TASK-LIST.md`.

### Counter-numeral display convention

The corpus standardises on **arabic numeral + counter** with the counter as kanji when it is in the N5 whitelist (e.g., `7時`, `5本`, `3人`, `100円`) and as kana when it is not (e.g., `1かい`, `8ふん`, `1ぱい` since 階 / 分 / 杯 are out-of-scope). Survey of the corpus 2026-05-01: 194 occurrences arabic+N5-kanji, 43 arabic+kana, 34 kanji+kanji (legacy), 29 kanji+kana (legacy). The arabic-first style dominates and is the going-forward convention. The remaining ~30 kanji+kanji occurrences (e.g., `二人`) appear inside passage prose where the kanji-form is natural reading-text style and don't need normalisation. Closes OPEN-5 from `feedback/MASTER-TASK-LIST.md`.

### Furigana mode

The app exposes a binary on/off furigana toggle (Settings panel). The `feedback/jlpt-n5-tutor-ux-developer-brief2.md` §4.1 originally called for a 3-mode toggle (always / known-only-hide / never), but Pass-13 native-teacher review concluded that auto-furigana produces wrong context-dependent readings (大学 = だいがく vs 大[おお]+学[がく]) and the feature was dropped. In-scope kanji render plain; out-of-scope words are authored in kana. The 3-mode requirement is formally dropped — see `js/settings.js` line 119 + `verification.md` Pass 13. Closes OPEN-8 from `feedback/MASTER-TASK-LIST.md`.

## Spec

See [`JLPT N5 Grammar Tutor – Functional Spec.docx`](JLPT%20N5%20Grammar%20Tutor%20%E2%80%93%20Functional%20Spec.docx) for the full functional specification, including content rules, UX requirements, data model, and acceptance criteria.

## Status

All Phase 1 features implemented and verified end-to-end in a browser preview:
- Chapter 1 Learn (TOC + 7-block detail + Mark-as-known)
- Chapter 2 Test (MCQ + dropdown + sentence-ordering, visible-but-disabled Submit, instant scoring, per-distractor explanations)
- Chapter 3 Review (weak-pattern cards driven by rolling-history threshold)
- Chapter 4 Summary (stats + category heatmap + reset)
- Drill mode (SRS engine with 1d / 3d / 7d / 14d boxes + immediate feedback + graduation)
- First-run Diagnostic (10 questions across categories, seeds SRS without affecting test history)
- Furigana toggle with N5-kanji ruby annotation (pragmatic single-pick readings)
- Service worker for offline capability

Content: 187 patterns across 23 categories (grammar.json), 219 questions (51 fully authored + 168 stubs). See `TASKS.md` for what remains.
