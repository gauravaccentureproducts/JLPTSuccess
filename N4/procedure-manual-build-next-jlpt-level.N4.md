# JLPT N4 Tutor App — Specification and Build Manual

**Status:** Single-source-of-truth N4 specification.
**Target:** A coding agent (or developer) can build the complete JLPT N4 Tutor app from this document alone, without needing to read any other file.
**Source basis:** Distilled and locked from the level-agnostic playbook at `procedure-manual-build-next-jlpt-level.md`. All `<L>` placeholders substituted with `4`. All "copy from N5" instructions resolved to explicit file-by-file recipes.
**Prepared:** 2026-05-04.

---

## 1. Purpose

This document specifies the JLPT N4 Tutor: a free, offline-capable, no-login, browser-based study application for the JLPT N4 level. It exists to teach a learner who has completed N5 the grammar, vocabulary, kanji, reading, and listening required to pass JLPT N4. Progress is local; no backend, no telemetry, no account.

The document is **prescriptive**. Where it says "must", that is a build requirement. Where it says "should", that is a strong recommendation with documented exception cases. Where it says "may", the agent has discretion.

---

## 2. Target App Identity

| Attribute | Value |
|---|---|
| **App name** | JLPT N4 Tutor |
| **Target level** | JLPT N4 |
| **Brand mark** | "四" (kanji for 4) in a hairline-bordered square, paired with the wordmark "JLPT N4" |
| **URL slug / repo** | `jlpt-n4-tutor` |
| **Live URL pattern** | `https://<org>.github.io/jlpt-n4-tutor/` |
| **Local path** | `<JLPT-root>/N4/` (sibling of `<JLPT-root>/N5/`) |
| **Service-worker name** | `jlpt-n4-tutor-v1` (bumped on every shell change) |
| **localStorage namespace** | `jlpt-n4-tutor:*` |
| **Tag prefix in IDs** | `n4-` (grammar / kanji), `n4.vocab.` (vocab), `n4.read.` (reading), `n4.listen.` (listening), `q-NNNN` (questions, opaque IDs) |
| **CHANGELOG / version** | Semantic versioning starting at v0.1.0 (skeleton), v1.0.0 (first complete release) |

---

## 3. Relationship to Existing N5 App

**N4 is a standalone application.** It lives at `<JLPT-root>/N4/` as a sibling of the existing N5 repo at `<JLPT-root>/N5/`. It is **not** a level extension of N5; it does not share a runtime, a storage namespace, or a service worker with N5.

What N4 inherits from N5:

- **Architecture**: vanilla static HTML + ES modules + CSS, no build step for runtime, hash-based router, PWA shell.
- **Build pipeline**: `tools/build_data.py` + `tools/check_content_integrity.py` + the rest of `tools/` per §34.
- **Design system**: Zen Modern (hairlines, no shadows, no gradients, weights 300/400/500), per §25.
- **Scoring engine**: SM-2 SRS for review, mock-test auto-grading, weak-area detection — unchanged.
- **i18n shell**: 5 locales (en / vi / id / ne / zh) with the same key tree.

What N4 does **not** inherit:

- **Content**: zero N5 content carries over verbatim. Every grammar pattern, vocab entry, kanji glyph, reading passage, listening item, and question is N4-original (or marked as N5-prerequisite, see §8).
- **Storage**: progress is stored under `jlpt-n4-tutor:*` keys; users do not migrate their N5 progress into N4.
- **Service worker**: a new `jlpt-n4-tutor-v1` SW; precaches the N4 shell only.

The only cross-link in user-facing UI is a **brand-link to the level picker** (`#/levels`) at `<JLPT-root>/` which lets a learner navigate between N5, N4, N3, N2, N1.

---

## 4. Target Users

**Primary user profile:**

- A learner who has completed N5 (~80-100 grammar patterns, ~800-1000 vocab, ~106 kanji) and is preparing for the JLPT N4 examination.
- Self-paced, typically 3-9 months of preparation.
- Studies in 15-30 minute sessions, 3-7 times per week.
- Uses laptop (desktop / tablet) and mobile (phone) interchangeably.
- Connectivity is intermittent (commute, travel) — offline mode is essential.
- Privacy-conscious — does not want to log in, does not want telemetry, does not want their study habits leaving their device.
- May or may not be a fluent English speaker; the app's chrome ships in 5 locales but Japanese teaching content is always Japanese.

**Primary user goals:**

1. Move from "passed N5" to "ready for N4".
2. Cover the full N4 syllabus systematically (grammar / vocab / kanji / reading / listening).
3. Practice with mock-exam questions in each Mondai section.
4. Identify weak areas and re-drill them efficiently.
5. Track progress across sessions and devices (via export / import).

**Secondary user profile:**

- A learner who passed N4 long ago and wants to refresh; uses Drill / Review without doing the placement check.
- A teacher who wants to recommend a free study tool to students.
- A developer/forker who wants to adapt the architecture to a different language or level.

**Non-users:**

- Absolute beginners with no N5 prerequisite — should use the N5 app first.
- Learners targeting N3 or higher — should use the N3 app (when built).
- JLPT examiners or content creators looking for licensed past-paper material — this app is original-content (see §30).

---

## 5. Product Scope

The app **must** ship with all of the following:

1. **Home / syllabus dashboard** — entry point, shows the 6 syllabus cards + recommended study order + progress overview.
2. **Grammar module** — pattern catalogue, detail pages, examples, common-mistakes blocks.
3. **Vocabulary module** — corpus catalogue, detail pages with example sentences, mark-as-known toggle.
4. **Kanji module** — kanji catalogue, detail pages with on/kun/example words/stroke-order SVG, mark-as-known toggle.
5. **Reading module** — 30+ graded passages with comprehension questions.
6. **Listening module** — 30+ items with audio (synthetic TTS for v1, native re-record path for v2) and comprehension questions.
7. **Test module** — full mock test (60+ questions, configurable length 20/30/50), section practice (per skill), placement check (one-time short test that recommends starting tier).
8. **Test results page** — score, per-section breakdown, question-by-question review with explanations.
9. **Weak-area review module** — surfaces incorrect answers grouped by skill, offers re-drill.
10. **Progress module** — shows completed-vs-total per section, mock test history, latest score, weak areas remaining, reset-with-confirmation, export / import.
11. **Search module** — global search across grammar / vocab / kanji by Japanese / kana / English / pattern / glyph / tag.
12. **Settings module** — UI language / theme / font size / furigana toggle / English translation toggle / default test length / shuffle / audio playback rate / reduce motion / reset / export / import.
13. **Footer** — version, privacy link, feedback link, what's-new link.

The app **must** support: keyboard navigation, screen-reader basics, mobile bottom-nav, offline operation after first load, install-as-PWA, dark mode (system / light / dark).

The app **must** ship with: SM-2 spaced repetition for review queue, FSRS-4 algorithm in v2 (deferred), weak-area tagging on every wrong answer, immediate auto-grading.

---

## 6. Out of Scope

Permanently out of scope (these are **non-goals**, not "future enhancements"):

- **User accounts / login.** No authentication.
- **Server-side analytics or telemetry.** No remote API calls during normal operation.
- **Cloud sync.** Progress lives on the device; export / import is the cross-device path.
- **Multi-learner profiles.** One device = one profile.
- **Open-ended writing or essay evaluation.** No free-text questions without a deterministic grading rubric.
- **Speaking practice / microphone input.** Out of scope for any level.
- **Runtime AI / LLM calls.** No external AI dependency at runtime. (LLM audit is a build-time tool, not a runtime feature.)
- **Native-mobile wrapper (Capacitor / React Native).** PWA satisfies the use case.
- **Subscription / monetisation.** App is free, no monetisation.
- **N5, N3, N2, N1 content in this app.** Each JLPT level is a separate app. Cross-level navigation happens at `<JLPT-root>/#/levels`.

Deferred to v2 (planned, not v1):

- Native-recorded listening audio (v1 ships synthetic TTS via gtts).
- FSRS-4 SRS algorithm (v1 ships SM-2).
- Handwriting / kanji stroke practice canvas.
- IME-typing input mode for text_input questions (v1 ships kana-strict).
- Reading-speed test mode with timer.
- Browser-resident LLM-backed natural-language search.

---

## 7. JLPT N4 Pedagogical Scope

**N4 assumes complete N5 knowledge.** A learner using this app is presumed fluent in: hiragana, katakana, ~106 N5 kanji, ~800-1000 N5 vocab, ~80-100 N5 grammar patterns, basic polite/casual register split.

**N4 introduces:**

- **~174 additional kanji** for a total whitelist of **280 kanji** (106 N5 prerequisite + 174 N4 new).
- **~700 additional vocab entries** for a total of **~1500 vocab**.
- **~30-50 additional grammar patterns** for a total of **~210 patterns** (a mix of new patterns and N5-pattern variations).
- **Longer reading passages**: short passages 80-150 chars (as in N5) plus medium passages 250-300 chars (new).
- **Listening at natural-but-slowed pace** (vs N5's slow / clear). Multi-turn dialogues. Implicit-meaning questions.
- **More natural expressions**: idioms in casual register, formal register markers (です/ます consistency in formal contexts), giving / receiving with proper register.
- **More complex grammar**: て-form chains, multi-clause conditionals, volitional + suggestion forms, potential form, passive form (basic), causative form (basic), giving / receiving (あげる / くれる / もらう trio with proper directionality).
- **Recognition vs production split**: at N4, learners primarily need **recognition** of N4 kanji (read in context); production (write from memory) is N3+.

**N4 does not introduce:**

- Abstract / literary / academic Japanese (those are N3+).
- Newspaper or business-formal writing (those are N2+).
- Honorific (尊敬語) / humble (謙譲語) language as a primary teaching focus (N3+).
- Compound kanji readings beyond common everyday compounds.

**Difficulty markers:**

- **Core N4** — solidly N4 scope, must-author.
- **Late N4** — N4 scope but typically taught at the end of N4 / borderline N3. Author with `tier: late_n4` flag.
- **N3 Borderline / Recognition Only** — appears in N4 materials (textbooks, JLPT samples) but is N3 nuance; flag `tier: n3_borderline` and treat as recognition-only (don't author production questions for these).
- **N5 Review / Prerequisite** — N5 patterns / words / kanji that appear in N4 materials; flag `tier: n5_prerequisite` so the runtime can de-emphasise them in the N4 syllabus dashboard while keeping them browsable.

---

## 8. N4 vs N5 Migration Rules

This section is the **explicit replacement checklist**. When porting from `<JLPT-root>/N5/` to `<JLPT-root>/N4/`, every item in this list must be applied or skipped with a documented reason.

| # | Item | Action |
|---|---|---|
| 1 | Title `JLPT N5 Tutor` | Replace with `JLPT N4 Tutor` everywhere |
| 2 | Brand mark `五` | Replace with `四` |
| 3 | Repo / URL slug `jlpt-n5-tutor` | Replace with `jlpt-n4-tutor` |
| 4 | localStorage namespace `jlpt-n5-tutor:*` | Replace with `jlpt-n4-tutor:*` |
| 5 | Service worker name `jlpt-n5-tutor-v<N>` | Replace with `jlpt-n4-tutor-v1` (start fresh; bump on every shell change) |
| 6 | All `n5-NNN` / `n5.vocab.` / `n5.read.` / `n5.listen.` IDs | Replace with `n4-` prefix |
| 7 | Path-name tokens `*_n5.md` | Replace with `*_n4.md` |
| 8 | Path-name tokens `n5_kanji_whitelist.json` etc. | Replace with `n4_kanji_whitelist.json` etc. |
| 9 | All N5 grammar patterns in `data/grammar.json` | Delete; replace with N4 grammar dataset per §12 |
| 10 | All N5 vocab entries in `data/vocab.json` | Delete; replace with N4 vocab dataset per §13 |
| 11 | All N5 kanji entries in `data/kanji.json` | Delete; replace with N4 kanji dataset (includes 106 N5-prerequisite + 174 N4-new) per §14 |
| 12 | All N5 reading passages in `data/reading.json` | Delete; replace with N4 reading dataset per §15 |
| 13 | All N5 listening items in `data/listening.json` | Delete; replace with N4 listening dataset per §16 |
| 14 | All N5 questions in `data/questions.json` | Delete; replace with N4 questions per §17-18 |
| 15 | All N5 mock-test paper structure under `data/papers/` | Delete; replace with N4 papers per §17-18 |
| 16 | Weak-area tags referencing N5 patterns | Replace with N4 tags |
| 17 | Homepage syllabus card descriptions ("177 patterns" etc.) | Replace with N4 counts (live-derived from `data/*.json` per §10) |
| 18 | UI language: any string containing "JLPT N5" or "N5" | Replace with N4 (except where explicitly showing prerequisite badges) |
| 19 | i18n locale messages: any N5-specific copy | Replace |
| 20 | Audio files under `audio/` (~491 N5 MP3s) | Re-render via `tools/build_audio.py` against new N4 corpus |
| 21 | Font subset (Noto Sans JP) | Re-subset against N5 ∪ N4 kanji union (~280 glyphs) |

**Non-negotiable rule (NN-1):** No user-facing N5 label may remain in the N4 app **unless** the content is explicitly shown as N5 prerequisite / review material with a `[N5 Review]` badge.

**Architecture preserves:**

- All `js/` modules (router, learn, test, drill, review, settings, etc.) — port verbatim with token substitution per items 1-8 above.
- All `tools/*.py` scripts — port verbatim with token substitution.
- `index.html`, `sw.js`, `manifest.webmanifest` — port verbatim with substitution.
- `css/main.css` — port verbatim. Design tokens unchanged.
- `locales/*.json` — port verbatim. Translate any N5-specific strings only.
- `feedback/ui-testing-plan.md` — port verbatim. Update level references in test-name-strings.

**Architecture does NOT preserve:**

- `data/*.json` content (entries-arrays only; structure preserved).
- `KnowledgeBank/*.md` source-of-truth content (markdown structure preserved, content N4).
- `audio/*.mp3` (regenerate).

---

## 9. Functional Modules

The app must implement all of the following modules. Each maps to a route in §11.

| # | Module | Route | Description |
|---|---|---|---|
| 1 | **Home / Syllabus Dashboard** | `#/home` | Default landing inside the N4 app. 6-card syllabus + study order + progress + placement check. Per §10. |
| 2 | **Grammar** | `#/grammar`, `#/grammar/<id>` | Pattern catalogue + detail pages. Per §12. |
| 3 | **Vocabulary** | `#/vocabulary`, `#/vocabulary/<form>` | Corpus catalogue + detail pages. Per §13. |
| 4 | **Kanji** | `#/kanji`, `#/kanji/<glyph>` | Kanji catalogue + detail pages. Per §14. |
| 5 | **Reading** | `#/reading`, `#/reading/<id>` | Passage list + reading session. Per §15. |
| 6 | **Listening** | `#/listening`, `#/listening/<id>` | Listening list + audio session. Per §16. |
| 7 | **Test** | `#/test`, `#/test/<n>`, `#/test/result` | Mock-test setup + active session + results. Per §18-19. |
| 8 | **Placement Check** | `#/placement` | One-time short diagnostic that recommends a starting tier. Per §18.2. |
| 9 | **Weak-area Review** | `#/weak-areas` | Lists incorrect answers grouped by skill; entry to re-drill. Per §20. |
| 10 | **Progress** | `#/progress` | Aggregate progress display + mock test history + reset / export / import. Per §21. |
| 11 | **Search** | `#/search?q=...` | Global search across grammar / vocab / kanji / reading / listening. Per §22. |
| 12 | **Settings** | `#/settings` | All user preferences. Per §23. |
| 13 | **Changelog** | `#/changelog` | Auto-rendered from `CHANGELOG.md`. |
| 14 | **Feedback** | `#/feedback` | Bug-report / suggestion form (mailto link with email obfuscation). |
| 15 | **About / Privacy** | `PRIVACY.md` (linked from footer) | Static MD page. No tracking, no telemetry, no cookies. |

**Footer (every page):**

- Version (e.g., "v1.0.0")
- "What's new" link → `#/changelog`
- "Privacy" link → `PRIVACY.md`
- "Feedback" link → `#/feedback`
- (No source-code link by default; see §25 anti-promotional rule.)

---

## 10. Homepage / Syllabus Dashboard Specification

The homepage at `#/home` is a **practical syllabus dashboard**, not a marketing landing page. It is **prohibited** from containing any of: outcome promises ("Pass JLPT N4!"), time-to-result claims ("in 30 days"), second-person imperatives at the brand level, celebration glyphs (✓, ★), defensive trust statements ("No login!"), or gamification glitter at the surface.

### 10.1 Required structure (in this exact vertical order)

```
1. Brand row (header — sticky)
   - Brand mark "四" + wordmark "JLPT N4"
   - Primary nav: Grammar / Vocabulary / Kanji / Reading / Listening / Test / Progress
   - Secondary: search input + settings cog

2. Up-link
   "← All JLPT levels" → routes to <JLPT-root>/#/levels

3. Resume strip (returning visitors only — when localStorage has any progress)
   "Last session: <pattern-id> — <pattern>" → routes to that detail page

4. Page title
   <h1>JLPT N4 Syllabus</h1>

5. Subtitle (one sentence, neutral)
   "Study grammar, vocabulary, kanji, reading, and listening in a structured order."

6. Daily-status row (returning visitors only)
   - "Streak: N days"
   - "✓ Practiced today" / "○ Not yet practiced today"

7. Section label
   <h2 class="section-label">SYLLABUS</h2>

8. Six syllabus cards in a 3 × 2 grid (desktop) / single column (mobile):

   Card 01: Grammar
     count:  "<N> patterns"           (live from data/grammar.json)
     desc:   "Verb forms, te-form chains, conditionals, giving and
              receiving, requests, obligation, comparison, conjunctions,
              and more N4 patterns."
     action: "Open Grammar Syllabus →"  → #/grammar

   Card 02: Vocabulary
     count:  "<N> words"               (live from data/vocab.json)
     desc:   "Daily life, school and work, travel, shopping, food,
              health, weather, feelings, verbs, adjectives, and
              common N4 expressions."
     action: "Open Vocabulary List →"  → #/vocabulary

   Card 03: Kanji
     count:  "<N> characters"          (live from data/kanji.json)
     desc:   "N5 prerequisite kanji plus N4 additions across people,
              time, society, work, school, transport, and the body."
     action: "Open Kanji List →"      → #/kanji

   Card 04: Reading
     count:  "<N> passages"            (live from data/reading.json)
     desc:   "Short notices, simple emails, diary-style passages,
              invitations, schedules, and short opinion passages."
     action: "Start Reading Practice →" → #/reading

   Card 05: Listening
     count:  "<N> items"               (live from data/listening.json)
     desc:   "Daily conversations, classroom phrases, shopping,
              workplace exchanges, directions, and short Q&A."
     action: "Start Listening Practice →" → #/listening

   Card 06: Mock Test
     count:  "<N> questions"           (configurable: 20/30/50)
     desc:   "Auto-scored mock test with correct answers,
              explanations, and weak-area review."
     action: "Take Mock Test →"        → #/test

9. Section label
   <h2 class="section-label">RECOMMENDED STUDY ORDER</h2>

10. Numbered ordered list (8 items, neutral phrasing):
    1. Take the placement check to see where to start
    2. Study new grammar patterns by category
    3. Drill new vocabulary alongside grammar
    4. Practice kanji recognition with example words
    5. Read short passages to build comprehension speed
    6. Listen to short dialogues to build aural comprehension
    7. Take a section practice test to identify weak areas
    8. Take the full mock test when each section is steady

11. Section label
    <h2 class="section-label">PROGRESS</h2>

12. Six progress rows (one per syllabus card):
     Grammar       <done> / <total>   <progress-bar>
     Vocabulary    <done> / <total>   <progress-bar>
     Kanji         <done> / <total>   <progress-bar>
     Reading       <done> / <total>   <progress-bar>
     Listening     <done> / <total>   <progress-bar>
     Mock Test     <latest score> %   <last-attempt-date>

13. Placement-check entry block
    <h3>Not sure where to start?</h3>
    <p>The placement check is a 10-minute diagnostic that recommends
       which N4 areas to study first.</p>
    <a class="btn-action" href="#/placement">Run placement check →</a>
    <a class="btn-action btn-secondary" href="#/learn">Skip and start learning →</a>

14. Footer (per §9 module list)
```

### 10.2 First-time vs returning behaviour

- **First-time visitor** (localStorage empty): hide the resume strip and the daily-status row. Show all 6 syllabus cards, the study-order list, and the placement-check entry block. Progress section shows 0/total per row.
- **Returning visitor** (any localStorage progress): show resume strip + daily-status row at the top. Same cards / order list / progress / placement-check below.

### 10.3 Hard rules for the homepage

| ID | Rule |
|---|---|
| HP-1 | No promotional copy. No outcome claims. No "in N days" framing. |
| HP-2 | No celebration glyphs (✓ except in the daily-status row). |
| HP-3 | No second-person imperatives at the brand level. "Open Grammar" not "Start your grammar journey!" |
| HP-4 | Counts (`<N> patterns`) are live-derived from `data/*.json` `_meta.entity_count` field. They update automatically when content is added; never hardcoded. |
| HP-5 | Card descriptions are factual, single-sentence, period-terminated, no trailing exclamation marks. |
| HP-6 | The page is the syllabus dashboard. The browser title is `JLPT N4 Syllabus`. The h1 is `JLPT N4 Syllabus`. |

---

## 11. Navigation and Routing

### 11.1 Required routes

All routes are hash-based (`#/...`) so the app works on GitHub Pages without server-side rewrites.

| Route | Page | Notes |
|---|---|---|
| `#/home` | Home / Syllabus Dashboard | Default after `#/levels` redirect, or after the user picks N4 from the level picker |
| `#/levels` | Level picker (lives at `<JLPT-root>/`, not in the N4 repo) | Renders the 5-card N5/N4/N3/N2/N1 picker; from N4 app, only the up-link "← All JLPT levels" routes here |
| `#/grammar` | Grammar list | All N4 grammar patterns, grouped by category |
| `#/grammar/<id>` | Grammar detail | One pattern, all examples, common-mistakes block, mark-as-known toggle, prev/next nav |
| `#/vocabulary` | Vocab list | All N4 vocab, grouped by thematic section |
| `#/vocabulary/<form>` | Vocab detail | One word, examples, mark-as-known toggle |
| `#/kanji` | Kanji list | All N4 kanji (N5 prerequisite + N4 new), filterable by tier |
| `#/kanji/<glyph>` | Kanji detail | One glyph, on/kun, examples, stroke-order SVG, mark-as-known toggle |
| `#/reading` | Reading list | All passages |
| `#/reading/<id>` | Reading session | One passage + comprehension questions |
| `#/listening` | Listening list | All items |
| `#/listening/<id>` | Listening session | One item + audio player + comprehension questions |
| `#/test` | Test setup | Test length picker, start button |
| `#/test/<n>` | Test session (deep-link) | Skip setup, start a test of length N |
| `#/test/result` | Test result | Score, breakdown, review, retest weak-areas action |
| `#/placement` | Placement check | One-time diagnostic (8-15 questions across all skills) |
| `#/weak-areas` | Weak-area review | Grouped weak-area list + drill-again actions |
| `#/progress` | Progress dashboard | Aggregate progress, mock-test history, reset / export / import |
| `#/search?q=...` | Search results | Global search across grammar / vocab / kanji / reading / listening |
| `#/settings` | Settings | All preferences |
| `#/changelog` | What's new | Auto-rendered from `CHANGELOG.md` |
| `#/feedback` | Feedback form | mailto with email obfuscation |

### 11.2 Routing rules

| ID | Rule |
|---|---|
| RT-1 | Hash-based router. Refreshing any route must not 404. |
| RT-2 | Default fallback when hash is empty: redirect to `#/levels` (then user picks N4 → `#/home`). |
| RT-3 | Unknown route fallback: render the `Home` page with a small "Page not found" notice; don't 404. |
| RT-4 | Module-level state (`view`, `session`, `lastResults`) MUST reset when the URL navigates AWAY from a "results" / "finished" view. Mid-attempt state preserves on refresh; finished state clears on URL change. (Anti-pattern documented in §40.) |
| RT-5 | No server-side rewrites required. All routes resolve client-side. |
| RT-6 | Brand link routes to `#/levels`. |
| RT-7 | Active-route highlighting: the primary-nav item matching the current route gets `class="active"`. |

---

## 12. Grammar Specification

### 12.1 Per-entry schema

Each grammar pattern entry in `data/grammar.json#patterns[]` has these fields:

```json
{
  "id": "n4-001",
  "pattern": "〜ように",
  "name": "yō ni",
  "meaning_en": "in order to / so that",
  "meaning_ja": "「もくてき」を しめす",
  "category": "Conjunctions and sentence connectors",
  "tier": "core_n4",
  "prerequisite": ["n4-pre-005", "n5-067"],
  "form_rules": {
    "attaches_to": ["verb-dictionary-form", "verb-nai-form"],
    "conjugations": [
      {"form": "purpose", "label": "in order to (positive)", "example": "Verb-dictionary + ように"},
      {"form": "purpose-neg", "label": "so as not to", "example": "Verb-nai + ように"}
    ]
  },
  "examples": [
    {
      "form": "purpose",
      "ja": "わすれないように メモを とりました。",
      "translation_en": "I took notes so as not to forget.",
      "vocab_ids": ["n4.vocab.something1", "n4.vocab.something2"],
      "audio": "audio/n4-001.0.mp3"
    }
  ],
  "common_mistakes": [
    {
      "wrong": "勉強するために 早く ねます。",
      "right": "勉強できるように 早く ねます。",
      "why": "ために takes a verbal noun or volitional verb expressing the actor's intention; ように is for indirect / non-volitional outcomes."
    }
  ],
  "notes": "Compare with 〜ために (n4-002): ために emphasises purpose with the actor's volition; ように for indirect or non-volitional outcomes.",
  "related": ["n4-002", "n4-150"],
  "tags": ["purpose", "conjunction", "intermediate"],
  "auto": false,
  "review_status": "llm_only"
}
```

**Field requirements:**

| Field | Required | Type | Notes |
|---|---|---|---|
| `id` | yes | string | Format `n4-NNN` (3-digit zero-pad). Reserve numeric ranges per category (see §12.2). Never re-numbered. |
| `pattern` | yes | string | The pattern in canonical form (e.g., `〜ように`, `〜ために`). Use 〜 for the slot. |
| `name` | no | string | Romanised reading hint for English speakers. |
| `meaning_en` | yes | string | One-sentence English. No marketing voice. |
| `meaning_ja` | yes | string | One-sentence simple Japanese (using N5+N4 vocabulary). |
| `category` | yes | string | One of the 18 categories in §12.2. |
| `tier` | yes | enum | One of: `core_n4`, `late_n4`, `n3_borderline`, `n5_prerequisite`. |
| `prerequisite` | no | array | IDs of patterns / vocab the learner should already know. |
| `form_rules` | yes | object | `attaches_to`: verb forms / particles / etc. `conjugations`: form-by-form examples. |
| `examples` | yes | array | 2-5 example sentences. Each has `form`, `ja`, `translation_en`, `vocab_ids` (homograph guard), optional `audio` and `furigana`. |
| `common_mistakes` | yes | array | At least one entry showing a typical wrong form, the correct form, and a one-sentence reason. |
| `notes` | no | string | Cross-references, register notes, contrast with related patterns. |
| `related` | no | array | IDs of related / contrastive patterns. |
| `tags` | no | array | Free-form tags for search / filtering. |
| `auto` | yes | bool | `false` = hand-authored. `true` = template-generated (subject to review). |
| `review_status` | yes | enum | `pending`, `llm_only`, `native_reviewed`. v1 ships at `llm_only` for all hand-authored entries. |

### 12.2 Required categories (18)

Author at least one entry per category; aim for balanced coverage.

| # | Category | Approx. patterns |
|---|---|---|
| 1 | Verb forms (overview) | 8-12 |
| 2 | Te-form patterns | 10-15 |
| 3 | Nai-form patterns | 8-12 |
| 4 | Ta-form patterns | 6-10 |
| 5 | Dictionary-form patterns | 8-12 |
| 6 | Potential form | 5-8 |
| 7 | Volitional form | 5-8 |
| 8 | Conditionals (たら / ば / なら / と) | 12-18 |
| 9 | Giving and receiving (あげる / くれる / もらう) | 10-15 |
| 10 | Requests and permission | 8-12 |
| 11 | Obligation and prohibition | 10-15 |
| 12 | Experience and plans | 6-10 |
| 13 | Comparison and degree | 8-12 |
| 14 | Conjunctions and sentence connectors | 12-18 |
| 15 | Quotation and thought | 8-12 |
| 16 | Explanation and reason | 10-15 |
| 17 | Time expressions | 8-12 |
| 18 | Frequency and adverbs | 6-10 |

Sum target: **~210 patterns**. Adjust per cross-source authority data (see §30); record final per-category counts in `_meta` of `data/grammar.json`.

### 12.3 Tier assignment rule

| Source authority pattern | Tier |
|---|---|
| Appears in BOTH Bunpro N4 AND JLPT-Sensei N4 | `core_n4` |
| Appears in Bunpro N4 only (Bunpro tends to include borderline upper-N4) | `late_n4` |
| Appears in N3 sources but commonly taught in N4 textbooks (Genki II late chapters / Minna II) | `n3_borderline` |
| Was N5 grammar; appears in N4 examples only as prerequisite | `n5_prerequisite` |

### 12.4 Authoring rules

- **Examples must use N4-or-prerequisite vocabulary only.** Vocab IDs in `vocab_ids` must resolve to entries in `data/vocab.json`.
- **Examples must use N4-or-prerequisite kanji only.** Any out-of-scope kanji must be replaced with kana.
- **Common-mistakes block must show a wrong form, the right form, and a reason.** Reason in plain English; no jargon.
- **No "(see n4-XXX)" stub redirects in user-facing fields.** If pattern A and pattern B are similar, write a real `notes` paragraph contrasting them.
- **No multi-correct grammar questions.** If two patterns are pragmatically interchangeable, write a `notes` block explaining the contrast and ensure questions disambiguate via context.

---

## 13. Vocabulary Specification

### 13.1 Per-entry schema

Each vocab entry in `data/vocab.json#entries[]` has these fields:

```json
{
  "id": "n4.vocab.21-travel-and-transportation.乗り換える",
  "form": "乗り換える",
  "reading": "のりかえる",
  "gloss": "to change trains / transfer",
  "section": "21. Travel and Transportation",
  "pos": "verb-2",
  "tier": "core_n4",
  "kanji_level": ["乗", "換"],
  "examples": [
    {
      "ja": "新宿で 乗り換えてください。",
      "translation_en": "Please change trains at Shinjuku."
    }
  ],
  "notes": "Group 2 (ichidan) verb. Used with で marking the transfer location.",
  "auto": false,
  "review_status": "llm_only"
}
```

**Field requirements:**

| Field | Required | Type | Notes |
|---|---|---|---|
| `id` | yes | string | Format `n4.vocab.<section-slug>.<form>[.<disambiguator>]`. Section-slug encodes the thematic section so a word can be cross-listed. |
| `form` | yes | string | Headword. With kanji where N4-allowed; otherwise hiragana. |
| `reading` | yes | string | Hiragana-only reading. (Katakana for loanwords.) |
| `gloss` | yes | string | One-sentence English. |
| `section` | yes | string | Thematic section name (matches §13.2 list). |
| `pos` | yes | enum | One of: `noun`, `verb-1` (godan), `verb-2` (ichidan), `verb-3` (irregular), `i-adj`, `na-adj`, `adverb`, `pronoun`, `particle`, `conjunction`, `expression`, `counter`, `demonstrative`, `numeral`, `question-word`, `interjection`. **Tag the WORD, not the section.** (Anti-pattern §40.) |
| `tier` | yes | enum | `core_n4`, `late_n4`, `n3_borderline`, `n5_prerequisite`. |
| `kanji_level` | no | array | Glyph chars used in `form`. For PoS-aware kanji-tier filters. |
| `examples` | yes | array | At least 1 example sentence; aim for 1-2. Each: `ja`, `translation_en`. |
| `notes` | no | string | Conjugation hints, register, register-distinction, idiom warnings. |
| `auto` | yes | bool | – |
| `review_status` | yes | enum | – |

### 13.2 Required thematic sections (18)

| # | Section | Approx. entries |
|---|---|---|
| 1 | People and relationships | 60-80 |
| 2 | Home and daily life | 70-90 |
| 3 | School and study | 50-70 |
| 4 | Work and society | 60-80 |
| 5 | Travel and transportation | 50-70 |
| 6 | Shopping and money | 50-70 |
| 7 | Food and restaurants | 60-80 |
| 8 | Health and body | 50-70 |
| 9 | Weather and nature | 40-60 |
| 10 | Time and frequency | 50-70 |
| 11 | Feelings and opinions | 50-70 |
| 12 | Verbs (general) | 150-200 |
| 13 | I-adjectives | 50-70 |
| 14 | Na-adjectives | 40-60 |
| 15 | Adverbs | 50-70 |
| 16 | Conjunctions | 30-40 |
| 17 | Counters and quantities | 30-40 |
| 18 | Set phrases / expressions | 40-60 |

Sum target: **~1500 entries**. Adjust per cross-source authority data; record final per-section counts in `_meta`.

### 13.3 Scope-control rules

| ID | Rule |
|---|---|
| VS-1 | Do not include N3+ vocabulary as `core_n4`. Mark borderline N3 as `n3_borderline` and limit to ~5% of the corpus. |
| VS-2 | Mark borderline N4 (typically late N4) as `late_n4` and limit to ~10% of the corpus. |
| VS-3 | Avoid dictionary-like over-expansion. Don't author every conjugated form as a separate entry; conjugations are a grammar concern. |
| VS-4 | Separate **core N4** vocabulary from **extended / recognition-only** items via the `tier` field. The runtime can then surface `core_n4` first. |
| VS-5 | Cross-listing is allowed (e.g., 学校 in both "School and study" and "Buildings/places") but requires consistent PoS across copies. (Anti-pattern §40 / §31.2.) |
| VS-6 | All `examples[].ja` must use N4-or-prerequisite kanji only. |

---

## 14. Kanji Specification

### 14.1 Pedagogical framing (read first)

At N4, learners primarily need **recognition**: read and understand kanji in context. Production (write from memory, choose correct form for kana input) is N3+. Author kanji entries for recognition; provide stroke-order SVG for learners who want to practise writing, but do not gate progression on writing skill.

The N4 kanji whitelist is the **union of N5 + N4**: 106 N5 prerequisite glyphs + ~174 N4-new glyphs = ~280 total. Each entry carries a `tier` field distinguishing the two groups.

### 14.2 Per-entry schema

Each kanji entry in `data/kanji.json#entries[]` has these fields:

```json
{
  "id": "n4.kanji.乗",
  "glyph": "乗",
  "tier": "core_n4",
  "n5_prerequisite": false,
  "lesson_order": 107,
  "frequency_rank": 412,
  "on": ["ジョウ"],
  "kun": ["の(る)", "の(せる)"],
  "primary_reading": "ジョウ",
  "primary_kind": "on",
  "meanings": ["ride", "board (a vehicle)"],
  "stroke_order_svg": "svg/kanji/乗.svg",
  "recognition_priority": 1,
  "examples": [
    {"form": "乗る", "reading": "のる", "gloss": "to ride / board"},
    {"form": "乗り換える", "reading": "のりかえる", "gloss": "to change (trains)"}
  ],
  "notes": "Common in transportation context. Often appears with に (に乗る = to ride / board)."
}
```

**Field requirements:**

| Field | Required | Type | Notes |
|---|---|---|---|
| `id` | yes | string | Format `n4.kanji.<glyph>`. |
| `glyph` | yes | string | The kanji character. |
| `tier` | yes | enum | `n5_prerequisite` (all 106 N5 kanji) or `core_n4` (~174 N4-new). |
| `n5_prerequisite` | yes | bool | Convenience flag: `true` if learner should already know it from N5. |
| `lesson_order` | yes | int | 1-280 (N5 first, then N4). Unique. |
| `frequency_rank` | yes | int | 1-280, JLPT-N4-corpus frequency. Unique. |
| `on` | yes | array | On-yomi readings in katakana. |
| `kun` | yes | array | Kun-yomi readings in hiragana. Slot indicators in parens, e.g., `の(る)`. |
| `primary_reading` | yes | string | The most-common reading in N4 context. |
| `primary_kind` | yes | enum | `on` or `kun`. |
| `meanings` | yes | array | English meanings, ordered by frequency. |
| `stroke_order_svg` | yes | string | Path to stroke-order SVG. Required (provide SVGs for all 280 glyphs at `svg/kanji/<glyph>.svg`). |
| `recognition_priority` | yes | int | 1-3. 1 = high (very common, recognise first). 3 = low (rare in N4 context). |
| `examples` | yes | array | 2-5 example words using this kanji. Each: `form`, `reading`, `gloss`. Examples must use only N4-or-prerequisite kanji. |
| `notes` | no | string | – |

### 14.3 Whitelist files

- `data/n4_kanji_whitelist.json`: array of 280 glyphs, sorted by `lesson_order`.
- `data/n4_kanji_readings.json`: per-glyph dictionary `{glyph: {on: [...], kun: [...], primary: "..."}}`.
- `data/n4_vocab_whitelist.json`: array of all `form` values from `data/vocab.json` (~1500 entries).

These three files are the source of truth for the integrity-check tool's "anything user-facing must use N4-whitelist kanji only" rule (per §31).

### 14.4 Authoring rules

| ID | Rule |
|---|---|
| KJ-1 | Whitelist is the union N5 ∪ N4. Every glyph carries `tier` so the runtime can distinguish. |
| KJ-2 | Examples for a given kanji must use only N4-or-prerequisite kanji. (No N3 leakage.) |
| KJ-3 | Each kanji needs at least 2 example words; ideally 3-5. |
| KJ-4 | `primary_reading` reflects the most common N4-context reading. For i-adjectives ending in `い`, prefer kun-yomi as primary. |
| KJ-5 | Stroke-order SVG must exist for every glyph. Source: KanjiVG (open-source, MIT license). |
| KJ-6 | `recognition_priority` defaults to 2; bump to 1 for the ~50 most common kanji; reserve 3 for tail-end uncommon. |

---

## 15. Reading Specification

### 15.1 Required passage types (9)

| # | Type | Length | Approx. count |
|---|---|---|---|
| 1 | Short notices (signs, posters) | 60-100 chars | 4 |
| 2 | Simple emails | 100-180 chars | 4 |
| 3 | Diary-style passages | 150-220 chars | 4 |
| 4 | Invitations | 100-180 chars | 3 |
| 5 | Schedules (bus, train, class) | 80-150 chars | 3 |
| 6 | Store / school / work notices | 100-180 chars | 4 |
| 7 | Simple explanations (how-to, instructions) | 180-280 chars | 3 |
| 8 | Daily-life messages (text-message, memo) | 80-150 chars | 3 |
| 9 | Short opinion passages | 200-300 chars | 2 |

Sum target: **~30 passages**. Format split: 22 short-medium passages + 5 long passages + 3 info-search passages (Mondai 6 format). Adjust counts to hit ~30 total.

### 15.2 Per-entry schema

Each reading passage in `data/reading.json#passages[]` has these fields:

```json
{
  "id": "n4.read.012",
  "title_ja": "図書館の おしらせ",
  "title_en": "Library notice (internal)",
  "type": "notice",
  "format_type": "short",
  "level": "core_n4",
  "estimated_time_seconds": 90,
  "ja": "つぎの 月よう日から 新しい...",
  "kanji_in_passage": ["新", "図", "書", "館"],
  "vocabulary_support": ["n4.vocab.13-locations.図書館"],
  "questions": [
    {
      "id": "n4.read.012.q1",
      "type": "mcq",
      "stem_ja": "おしらせの ないようは 何ですか。",
      "choices": [
        "A. としょかんが 新しく なります。",
        "B. としょかんの 時間が かわります。",
        "C. としょかんが しまります。",
        "D. 本を かりる 方法が かわります。"
      ],
      "correctAnswer": "B",
      "explanation_en": "The notice says the library hours change starting Monday — option B.",
      "weak_area_tags": ["reading-comprehension", "notice-format"],
      "distractor_explanations": {
        "A": "The library is not getting new (location/equipment); the hours are changing.",
        "C": "The notice does not say the library is closing.",
        "D": "Borrowing methods are not mentioned."
      }
    }
  ],
  "audio": "audio/n4.read.012.mp3",
  "auto": false,
  "review_status": "llm_only"
}
```

**Field requirements:**

| Field | Required | Type | Notes |
|---|---|---|---|
| `id` | yes | string | Format `n4.read.NNN`. |
| `title_ja` | yes | string | Japanese title. NEVER an English title. (JA-first surface; see §31.) |
| `title_en` | no | string | Internal-only English title (for editor reference). NEVER rendered in UI. |
| `type` | yes | enum | One of the 9 types above. |
| `format_type` | yes | enum | `short` (Mondai 4), `medium` (Mondai 5), `info_search` (Mondai 6). |
| `level` | yes | enum | `core_n4`, `late_n4`, `n3_borderline`. |
| `estimated_time_seconds` | yes | int | – |
| `ja` | yes | string | The passage in Japanese. Uses only N4-or-prerequisite kanji. |
| `kanji_in_passage` | yes | array | All unique kanji in `ja` (used by JA-13 invariant). |
| `vocabulary_support` | no | array | Vocab IDs of words above N4-prerequisite that the passage gracefully introduces (allowed if learner can infer from context; flag for editor review). |
| `questions` | yes | array | 2-3 questions per passage (Mondai 4: 2; Mondai 5: 3; Mondai 6: 1-2). |
| `audio` | no | string | Optional read-along audio. Synthetic for v1. |
| `auto` | yes | bool | – |
| `review_status` | yes | enum | – |

### 15.3 Question schema (used in reading + listening + papers)

```json
{
  "id": "n4.read.012.q1",
  "type": "mcq",
  "stem_ja": "...",
  "choices": ["A. ...", "B. ...", "C. ...", "D. ..."],
  "correctAnswer": "B",
  "explanation_en": "...",
  "weak_area_tags": ["reading-comprehension"],
  "distractor_explanations": {"A": "...", "C": "...", "D": "..."}
}
```

### 15.4 Authoring rules

| ID | Rule |
|---|---|
| RD-1 | Passages use only N4-whitelist kanji. (JA-13.) |
| RD-2 | Comprehension questions test reading skill, not obscure vocabulary. |
| RD-3 | **Exactly one correct answer per question.** No multi-correct. (JA-6.) |
| RD-4 | Distractor explanations must contrast the wrong choice with the correct one (not "Wrong choice — see passage"). |
| RD-5 | Title is always Japanese (`title_ja`). Never render `title_en` in UI. (JA-27.) |
| RD-6 | Question stems use only N4-whitelist kanji. (JA-1.) |
| RD-7 | Question explanation kanji must be a subset of passage kanji + N4-whitelist. (JA-18.) |
| RD-8 | Question choices kanji must match the passage's kanji form. (JA-20.) |
| RD-9 | Info-search passages have `format_type: "info_search"`. (JA-19.) |

---

## 16. Listening Specification

### 16.1 Audio source decision (LOCKED)

**v1 ships synthetic TTS via gtts** (the existing `tools/build_audio.py` pipeline). Each item is flagged `voice: "synthetic"`. The runtime listens to MP3 files at `audio/n4.listen.<id>.mp3`.

**Fallback chain:**
1. If the MP3 exists → play it.
2. If MP3 missing AND browser supports SpeechSynthesis API → use browser TTS with the closest Japanese voice available.
3. If neither → render the script as text with a "Audio unavailable" notice and let the learner read.

**v2 deferred:** native-recorded audio. Replace synthetic items per-item; flag `voice: "native"`. The runtime swaps to native MP3s automatically (same path, regenerated by build pipeline).

### 16.2 Per-entry schema

Each listening item in `data/listening.json#items[]` has these fields:

```json
{
  "id": "n4.listen.014",
  "title_ja": "駅員と 旅行者の 会話",
  "format": "Mondai 1 (kadai-rikai / task-oriented)",
  "level": "core_n4",
  "estimated_time_seconds": 60,
  "setup_ja": "駅で、駅員と 旅行者が 話して います。旅行者は どこへ 行きますか。",
  "script_ja": "[男1] すみません、新宿に 行きたいんですが…\n[女]  はい、新宿へは 8番線から 出ます…",
  "audio": "audio/n4.listen.014.mp3",
  "voice": "synthetic",
  "transcript_reveal": "after_answer",
  "questions": [
    {
      "id": "n4.listen.014.q1",
      "type": "mcq",
      "stem_ja": "旅行者は どこへ 行きますか。",
      "choices": ["A. 池袋", "B. 新宿", "C. 渋谷", "D. 東京駅"],
      "correctAnswer": "B",
      "explanation_en": "The traveller says they want to go to Shinjuku; the staff confirms platform 8.",
      "weak_area_tags": ["listening-detail", "transportation"]
    }
  ],
  "auto": false,
  "review_status": "llm_only"
}
```

**Field requirements:**

| Field | Required | Type | Notes |
|---|---|---|---|
| `id` | yes | string | Format `n4.listen.NNN`. |
| `title_ja` | yes | string | Japanese title. (Never rendered as English.) |
| `format` | yes | string | One of the 4 JLPT N4 listening formats: Mondai 1 (課題理解), Mondai 2 (ポイント理解), Mondai 3 (発話表現), Mondai 4 (即時応答). |
| `level` | yes | enum | – |
| `setup_ja` | yes | string | The "scene-setting" Japanese sentence the listener hears before the dialogue (per JLPT convention: "[Person]と [Person]が 話して います。[question prompt]"). |
| `script_ja` | yes | string | The full dialogue with speaker prefixes (`[男]`, `[女]`, `[先生]`, `[学生]`, `[A]`, `[B]`, etc.). |
| `audio` | yes | string | Path to MP3 (synthetic or native). |
| `voice` | yes | enum | `synthetic` (gtts), `native` (recorded), `browser_tts` (runtime fallback). |
| `transcript_reveal` | yes | enum | `after_answer` (default; show transcript only after submit), `always` (for accessibility), `never` (advanced mode). |
| `questions` | yes | array | 1-3 questions per item per JLPT format. Mondai 1-2: 1 question. Mondai 3: 1 utterance + correct response selection. Mondai 4: 1 prompt + correct response selection. |
| `auto` | yes | bool | – |
| `review_status` | yes | enum | – |

### 16.3 Required listening formats (JLPT N4 official structure)

| # | Mondai | Japanese | Tests | Approx. count |
|---|---|---|---|---|
| 1 | Mondai 1 | 課題理解 (kadai-rikai / task-oriented) | What action does the listener take next? | 8-10 |
| 2 | Mondai 2 | ポイント理解 (point-oriented) | What is the specific detail? | 6-8 |
| 3 | Mondai 3 | 発話表現 (expression-selection) | Pick the correct response in a scene | 5-7 |
| 4 | Mondai 4 | 即時応答 (immediate-response) | Quick conversational response | 8-10 |

Sum target: **~30 items**.

### 16.4 Authoring rules

| ID | Rule |
|---|---|
| LS-1 | Title is always Japanese. (JA-27.) |
| LS-2 | Scripts use only N4-whitelist kanji. |
| LS-3 | Exactly one correct answer per question. |
| LS-4 | Speaker prefixes follow JLPT convention. |
| LS-5 | Audio file must exist on disk for every item with `voice: "synthetic"` or `voice: "native"`. (JA-15.) |
| LS-6 | Distractor explanations follow §15 rule (no stub redirects). |
| LS-7 | Pacing: aim for natural-but-slowed; 4-6 turns per dialogue. |

---

## 17. Question Bank Specification

### 17.1 Question files

The N4 corpus has **5 question files** in `KnowledgeBank/`, parsed by `tools/build_data.py` into `data/questions.json` and `data/papers/manifest.json`.

| File | Mondai | Approx. questions |
|---|---|---|
| `KnowledgeBank/moji_questions_n4.md` | Mondai 1 (kanji reading), Mondai 2 (orthography), Mondai 3 (word formation) | 150 |
| `KnowledgeBank/goi_questions_n4.md` | Mondai 4 (context fill-in), Mondai 5 (paraphrase), Mondai 6 (usage) | 150 |
| `KnowledgeBank/bunpou_questions_n4.md` | Mondai 1 (sentence grammar 1), Mondai 2 (sentence grammar 2), Mondai 3 (text grammar) | 100 |
| `KnowledgeBank/dokkai_questions_n4.md` | Mondai 4 (short reading), Mondai 5 (medium reading), Mondai 6 (info search) | 70 |
| `KnowledgeBank/chokai_questions_n4.md` | Mondai 1-4 listening | 60 |

**Sum target: ~530 questions**, organised into mock-test "papers" of 15 questions each via the structure under `data/papers/<category>/paper-<n>.json`.

### 17.2 Per-question schema

```json
{
  "id": "q-0123",
  "category": "bunpou",
  "subcategory": "Mondai 1",
  "grammarPatternId": "n4-001",
  "type": "mcq",
  "subtype": null,
  "direction": "Choose the best particle/word for the blank.",
  "prompt_ja": "つぎの ぶんを よんで しつもんに こたえなさい。",
  "question_ja": "わすれない （ ）　メモを とりました。",
  "choices": ["A. ように", "B. ために", "C. ても", "D. のに"],
  "correctAnswer": "A",
  "explanation_en": "ように for indirect / non-volitional outcomes (so as not to forget).",
  "distractor_explanations": {
    "B": "ために takes a verbal noun or volitional verb expressing actor's intention.",
    "C": "ても means 'even if'; doesn't fit the purpose meaning here.",
    "D": "のに expresses contrast / contradictory result."
  },
  "high_confusion": false,
  "difficulty": "core_n4",
  "auto": false
}
```

### 17.3 Allowed question types

| Type | Use case |
|---|---|
| `mcq` | Multiple choice (4 options). Most common. |
| `mcq` (subtype `paraphrase`) | Goi Mondai 5: pick the synonymous sentence. |
| `mcq` (subtype `kanji_writing`) | Moji Mondai 2: pick the correct kanji for the kana. |
| `sentence_order` | Bunpou Mondai 2: arrange tiles in correct order. |
| `text_input` | Type the kana/kanji answer (forgiving matcher accepts kana / romaji / particle homophones). |

**Subtype taxonomy is closed.** `paraphrase` and `kanji_writing` are the only allowed subtypes for v1. New subtypes require a code change, not a data sneak-in. (JA-29.)

**Prohibited:** free-writing questions without a deterministic grading rubric. (NN-4.)

### 17.4 Authoring rules

| ID | Rule |
|---|---|
| QB-1 | Stems use only N4-whitelist kanji. (JA-1.) |
| QB-2 | All 4 MCQ choices distinct. (JA-11.) |
| QB-3 | `correctAnswer` matches one of the `choices` exactly. (JA-5.) |
| QB-4 | Exactly one correct answer. No multi-correct via interchangeable particles (に/へ, は/が, から/ので) without scene context. (JA-23.) |
| QB-5 | No "see pattern detail" stub distractor explanations. Author them by hand. |
| QB-6 | Every question has `grammarPatternId` for gap analysis. |
| QB-7 | Distractor explanations contrast WRONG with CORRECT, not generic disclaimer. |
| QB-8 | No past-paper provenance signatures (specific phrasings from JEES samples). (JA-30.) Original content only. |
| QB-9 | No duplicate question IDs across the entire bank. (JA-26.) |
| QB-10 | Question count `_meta.question_count` matches `len(questions)`. (JA-8.) |

---

## 18. Test Engine Specification

### 18.1 Test modes

The runtime supports the following test modes, all auto-graded immediately on submit, no reload required:

| Mode | Route | Question source | Length |
|---|---|---|---|
| **Placement check** | `#/placement` | Curated 8-15 question diagnostic across all 5 question files | 8-15 |
| **Section practice (Grammar)** | `#/test?section=bunpou&n=20` | Random sample from `data/questions.json` filtered by `category=bunpou` | 20 / 30 / 50 |
| **Section practice (Vocabulary)** | `#/test?section=goi&n=20` | Filtered by `category=goi` | 20 / 30 / 50 |
| **Section practice (Kanji)** | `#/test?section=moji&n=20` | Filtered by `category=moji` | 20 / 30 / 50 |
| **Section practice (Reading)** | `#/test?section=dokkai&n=20` | Filtered by `category=dokkai` | 20 / 30 / 50 |
| **Section practice (Listening)** | `#/test?section=chokai&n=20` | Filtered by `category=chokai` | 20 / 30 / 50 |
| **Full mock test** | `#/test?n=60` | Balanced sample mirroring JLPT-N4 paper proportions (per §18.3) | 60 (default) |
| **Weak-area retest** | `#/test?weak=1` | Questions targeting current weak-area tags | 10-30 |
| **Mock-test paper** | `#/papers/<category>/<n>` | Pre-curated 15-question paper from `data/papers/<category>/paper-<n>.json` | 15 |

### 18.2 Placement check details

A one-time short diagnostic that recommends a starting tier. Triggered:

- Automatically on first visit to `#/home` if `localStorage.placement_completed` is not set.
- Manually via the placement-check entry on the homepage.

Structure:

- 8-15 questions sampled across grammar / vocab / kanji / reading / listening, balanced.
- Mix of `core_n4` (60%) and `late_n4` (30%) and `n5_prerequisite` (10%) difficulty.
- 10 minutes target completion time.

After submission, the result page shows:

- Recommended starting area (e.g., "Start with Grammar — your kanji is solid").
- Per-skill score breakdown.
- A direct-launch button to the recommended section.

The placement check stores its result in `localStorage.placement_result`. The user can re-take it any time via Settings.

### 18.3 Full mock test composition

Default 60 questions. Composition mirrors JLPT N4 paper proportions:

| Section | Question source | Count |
|---|---|---|
| Grammar (bunpou) | All 3 Mondai | 17 |
| Vocab (goi) | All 3 Mondai | 17 |
| Kanji (moji) | All 3 Mondai | 17 |
| Reading (dokkai) | Mondai 4-6 | 6 |
| Listening (chokai) | Mondai 1-4 | 3 |

User can override the length to 20 / 30 / 50 in the test setup screen; the engine downsamples proportionally.

### 18.4 Test session state

The test module holds module-level state:

```js
{
  view: 'setup' | 'attempting' | 'results',
  session: {
    questions: [...],   // selected sample
    answers: {},        // questionId → answer
    startedAt: ISO,
    config: {n, sections, mode}
  },
  lastResults: { ... }
}
```

State-reset rule per RT-4 / §40: when the user navigates AWAY from `#/test*` after `view === 'results'`, the state resets so a future visit to `#/test` starts fresh.

### 18.5 Engine display contract (JA-9)

The UI MUST hide `correctAnswer` and `explanation_en` until the user submits. Specifically:

- During `view === 'attempting'`: question stem + choices + selection state. No answer marker. No explanation.
- After submit: `view === 'results'`. Now show every question with: user's answer, correct answer, explanation, weak-area tags.

**Test the contract via Playwright/headless smoke test on every release.**

---

## 19. Submit and Results Rules

### 19.1 Submit-button behaviour (consolidated from §4.6 / JA-9)

| ID | Rule |
|---|---|
| SR-1 | Submit button is **disabled** until every question has an answer. |
| SR-2 | The disabled state shows a **visible reason** in UI text (not just a `title` tooltip): `Submit (N remaining)` in button text, plus a hint paragraph: `"Answer all <total> questions to submit · <N> questions unanswered"`. (Anti-pattern §40.) |
| SR-3 | When all answered: button text becomes `Submit`, hint paragraph disappears. |
| SR-4 | On submit click: results display **immediately**. No page reload. No server call. |
| SR-5 | Results page receives `view = 'results'` and persists `lastResults` until user navigates away. |
| SR-6 | The `correctAnswer` and `explanation_en` for any question MUST NOT be in the rendered DOM until submit fires. (Audit via DOM-inspection in Playwright.) |
| SR-7 | After submit, on every question card: show user's answer (highlighted), correct answer (highlighted), per-question explanation, weak-area tags. |

### 19.2 Results page structure

```
1. Result header
   - Total score        e.g., "47 / 60"
   - Percentage         "78%"
   - Per-section breakdown (bunpou / goi / moji / dokkai / chokai with N/total each)
   - Verdict line       e.g., "Above passing threshold (need 90/180 ≈ 50%; you scored 78%)"

2. Section navigation
   - Tabs: All / Bunpou / Goi / Moji / Dokkai / Chokai

3. Question-by-question review (one card per question)
   - Question ID + section tag
   - Stem (Japanese)
   - Choices: user's choice marked, correct choice marked
   - Explanation (English)
   - Weak-area tags
   - Related grammar / vocab / kanji link (e.g., "Related: n4-001 〜ように")

4. Weak-area summary
   - Top 3-5 weak-area tags by error count
   - "Retest weak areas" button → routes to #/weak-areas
   - "Back to Test" button → routes to #/test (resets state per RT-4)

5. Mock-test history
   - List of previous mock-test attempts: date, score, percentage
   - "Take another test" button
```

### 19.3 No manual grading. No server. No reload.

| ID | Rule |
|---|---|
| RR-1 | All grading is auto-grading. Question types where auto-grading isn't possible are **prohibited** (NN-4). |
| RR-2 | Submit triggers no network request. |
| RR-3 | Submit does not reload the page. |
| RR-4 | Results persist in `localStorage.history.<sessionId>` so the test history list survives page refresh. |

---

## 20. Weak-Area Review Specification

### 20.1 Weak-area generation

Weak areas are generated from incorrect answers across all test sessions. Source data: `localStorage.history` (test attempts) + `localStorage.review` (SRS state per pattern).

A weak area surfaces when:

- A learner answers a question incorrectly (any test mode).
- An SRS card lapses ("Again" grade).
- A pattern is missed in 3+ consecutive sessions.

### 20.2 Weak-area grouping

Group by:

| Group | Source | Example |
|---|---|---|
| **Grammar** | Grammar pattern ID from question's `grammarPatternId` | n4-001 〜ように |
| **Vocabulary** | Vocab ID from question's vocab tags | n4.vocab.21-travel.乗り換える |
| **Kanji** | Glyph from kanji-question incorrect answers | 乗 |
| **Reading skill** | `weak_area_tags` like `reading-comprehension`, `reading-detail`, `reading-info-search` | reading-detail |
| **Listening skill** | `weak_area_tags` like `listening-detail`, `listening-task`, `listening-expression` | listening-task |

### 20.3 Weak-area item display

Per grouping, each weak-area item is rendered as:

```
- Item name              e.g., "n4-001 〜ように"
- Meaning                "in order to / so that"
- Short explanation      "Used for indirect or non-volitional outcomes (vs ために for actor's intention)"
- Why mistake likely     "Confused with ために (which expresses actor's intention with a volitional verb)."
- Review examples        2-3 example sentences from the pattern
- Practice-again button  → Routes to a focused drill targeting this pattern (`#/test?weak=1&pattern=n4-001`)
```

### 20.4 Weak-area page (`#/weak-areas`)

```
1. Header
   <h1>Weak Areas</h1>
   <p>Items you missed in tests, grouped by skill. Drill them to improve.</p>

2. Group tabs
   Grammar (N items) | Vocabulary (N) | Kanji (N) | Reading (N) | Listening (N)

3. Per-group list
   - Sorted by miss count descending
   - Each item per §20.3 above
   - Each item has its "Practice again" button

4. Bulk actions
   "Drill 10 weak items now" button → samples top-10 weak items into a session
   "Mark area as resolved" toggle (manual override)

5. Empty state (no weak areas)
   "No weak areas right now. Take a test to identify gaps."
```

### 20.5 Resolution rules

A weak area is automatically marked resolved when:

- The learner answers 3 questions correctly on the same pattern in a row.
- An SRS card graduates (rep ≥ 5 with all "Good" grades).

The learner can manually mark resolved via the toggle.

---

## 21. Progress Tracking Specification

### 21.1 What's tracked

LocalStorage namespace: `jlpt-n4-tutor:*`. Key schema:

```
jlpt-n4-tutor:settings              # User preferences (per §23)
jlpt-n4-tutor:history               # SRS card states {patternId: {EF, rep, due, interval, lapses}}
jlpt-n4-tutor:knownKanji            # Set of kanji glyphs marked known
jlpt-n4-tutor:knownVocab            # Set of vocab forms marked known
jlpt-n4-tutor:streak                # {current, longest, lastStudyDate, days[30]}
jlpt-n4-tutor:results               # Array of test attempts: {date, score, percentage, breakdown, sessionId}
jlpt-n4-tutor:lastViewed            # Pattern/glyph/vocab last opened (for resume strip)
jlpt-n4-tutor:placement_result      # {date, recommendation, breakdown}
jlpt-n4-tutor:placement_completed   # Boolean
jlpt-n4-tutor:completedReading      # Set of reading IDs completed
jlpt-n4-tutor:completedListening    # Set of listening IDs completed
jlpt-n4-tutor:weakAreas             # Object mapping weak-area-tag → miss count
```

### 21.2 Progress UI (`#/progress`)

```
1. Header
   <h1>Your Progress</h1>

2. Per-section completed-vs-total
   Grammar      <known>/<total>      <progress-bar>
   Vocabulary   <known>/<total>      <progress-bar>
   Kanji        <known>/<total>      <progress-bar>
   Reading      <completed>/<total>  <progress-bar>
   Listening    <completed>/<total>  <progress-bar>
   Mock Test    <highest>%           <last-attempt-date>

3. Streak
   "Current streak: <N> days"
   "Longest streak: <N> days"
   30-day mini-heatmap

4. Mock-test history
   Table: Date | Score | % | Section breakdown
   Last 10 attempts

5. Weak areas remaining
   "<N> weak areas across grammar / vocab / kanji / reading / listening"
   Link to #/weak-areas

6. Data actions
   Export progress (button → downloads jlpt-n4-progress-<date>.json)
   Import progress (button → file picker → confirms before applying)
   Reset progress (typed-confirmation guard: type "RESET" to enable confirm button)
```

### 21.3 Reset behaviour

| ID | Rule |
|---|---|
| PR-1 | Reset wipes every `jlpt-n4-tutor:*` key. |
| PR-2 | Reset requires typed-phrase confirmation: an input field must contain `RESET` (case-sensitive) for the confirm button to enable. |
| PR-3 | After reset, the user is redirected to `#/home` and the app behaves as first-visit. |

### 21.4 Export / import

| ID | Rule |
|---|---|
| PR-4 | Export bundles all `jlpt-n4-tutor:*` keys into one JSON, schema-versioned. |
| PR-5 | Filename: `jlpt-n4-progress-YYYY-MM-DD.json`. |
| PR-6 | Import accepts the same schema; refuses unknown schema versions; merges on conflict by taking the MAX of `(rep, interval)` per item; prefers most-recent EF; sums lapses. |
| PR-7 | After successful import, page reloads to apply new state. |

---

## 22. Search Specification

### 22.1 Search inputs

The search input lives in the secondary nav (header). Triggered by:

- Click into the input
- Keyboard shortcut `/` (focus the input)
- Direct URL `#/search?q=<term>`

### 22.2 What gets indexed

- Grammar: `pattern`, `name`, `meaning_en`, `meaning_ja`, `tags`.
- Vocabulary: `form`, `reading`, `gloss`, all examples' `ja`.
- Kanji: `glyph`, `meanings`, all `examples[].form` and `examples[].reading`.
- Reading: `title_ja` only (passages are too long to index meaningfully).
- Listening: `title_ja` only.

### 22.3 Search behaviour

| ID | Rule |
|---|---|
| SE-1 | Match against Japanese (kanji + kana), English, and grammar pattern strings. |
| SE-2 | Optional romaji-to-kana on input: type `nori` → matches `のり` / `乗り`. |
| SE-3 | Case-insensitive on English. |
| SE-4 | Substring match on Japanese; ranked by exact-prefix > prefix > substring > tag. |
| SE-5 | Results: max 50; show "X results" if more. |
| SE-6 | Search runs in-browser; no network call; corpus pre-loaded with the data files. |
| SE-7 | No fuzzy matching at v1 (causes false-positives at this corpus size). |

### 22.4 Result format

Each result row:

```
[Type badge: Grammar / Vocab / Kanji / Reading / Listening]
[Title in Japanese]                        [Tier badge: core_n4 / late_n4 / etc.]
[Short meaning / English gloss]            [Link → detail page]
```

Empty state: "No matches found for <query>."

---

## 23. Settings Specification

The settings page at `#/settings` exposes these preferences. All persist in `localStorage.jlpt-n4-tutor:settings`.

| Setting | Type | Default | Visible side-effect |
|---|---|---|---|
| **UI language** | dropdown (en/vi/id/ne/zh) | en | Page reloads on change |
| **Theme** | dropdown (system/light/dark) | system | CSS class flips immediately |
| **Font size** | dropdown (S/M/L/XL → 13/15/17/19 px) | M | `html` `data-font` attribute flips |
| **Show furigana** | toggle (on/off) | on | All ruby spans show/hide |
| **Show English translation under examples** | toggle (on/off) | on | `.translation` blocks show/hide |
| **Compact / detailed study mode** | toggle | detailed | Compact hides notes/explanations on detail pages |
| **Default test length** | dropdown (20/30/50) | 30 | – |
| **Shuffle questions** | toggle (on/off) | on | – |
| **Audio playback rate** | dropdown (0.75/1.0/1.25) | 1.0 | – |
| **Reduce motion** | dropdown (auto/on/off) | auto | – |
| **Reset all progress** | button | – | Typed-confirmation flow per PR-2 |
| **Export progress** | button | – | Triggers download |
| **Import progress** | button + file input | – | Imports JSON |

### 23.1 Settings save feedback (per §40)

For settings that have **no immediate visible side-effect** (Default test length, Audio playback rate, Reduce motion, etc.), show a brief `Saved: <label> = <value>` toast after change. Bottom-centre, 1800 ms auto-dismiss, fades. Settings with visible side-effects (Theme, Font size, UI language) skip the toast — the page itself changes.

For Export action: show a status line `Exported to <filename> (check your downloads folder).` for 4 seconds.

---

## 24. Furigana and Kanji Display Rules

### 24.1 Default behaviour

Furigana is **on by default** but is filtered:

- **N5 prerequisite kanji**: NO furigana by default. Learner is presumed to know these.
- **N4 new kanji**: furigana ON in learn mode (grammar / vocab / kanji detail pages, reading-passage browse). Helps with recognition.
- **N3+ kanji** (out of scope): authoring rule prefers replacing with kana (NN-11). If unavoidable in a real-life passage, furigana ON unconditionally.

### 24.2 Furigana in test mode

| ID | Rule |
|---|---|
| FU-1 | In test sessions (`#/test*`), furigana on the question stem MUST NOT reveal the answer. If a question asks "What is the reading of 乗り換える?" then furigana on 乗り換える is hidden. |
| FU-2 | Furigana on choices is shown for new N4 kanji only when it doesn't trivialise the question. |
| FU-3 | If a question is a kanji-reading question itself, no furigana anywhere. |
| FU-4 | The furigana-show toggle in Settings does NOT override test-mode hiding. (Test-mode wins.) |

### 24.3 Furigana rendering

- HTML: `<ruby><rb>kanji</rb><rt>reading</rt></ruby>`.
- CSS: `ruby rt { font-size: 0.6em; }` (with `display: ruby-text;` for browsers that need it).
- Tokenisation: at build time via `mecab-python3` (or kuromoji.js fallback), per-example, per-passage. Reading is the most-common N4-context reading.
- The `furigana[]` field on a grammar example / passage is an OPTIONAL OVERRIDE — used when the auto-renderer would produce the wrong context-dependent reading (e.g., 大学 = だいがく vs 大[おお]+学[がく]).

### 24.4 Out-of-scope kanji

| ID | Rule |
|---|---|
| KD-1 | Authored content prefers replacing N3+ kanji with kana. (e.g., 颯爽 → さっそう). |
| KD-2 | If the kanji is structurally important and replacement loses meaning, keep the kanji and FORCE furigana on every occurrence. |
| KD-3 | Author MUST add the out-of-scope kanji to `tools/check_content_integrity.py` augmented set with a WHY comment. (JA-25.) |

---

## 25. UI / Visual Design Requirements

### 25.1 Design directives (Zen Modern)

The N4 app follows **clean Japanese educational minimalism**. Inherited from the design system originally authored for N5.

| ID | Directive |
|---|---|
| DS-1 | **Syllabus-first layout.** Pages open into the syllabus or section grid, not into a hero / banner / tagline. |
| DS-2 | **Calm, practical.** No celebration glyphs, no animated mascots, no exclamation marks in microcopy. |
| DS-3 | **Not promotional.** No "Pass JLPT N4!", no "Easy!", no time-to-result claims. (See HP-1.) |
| DS-4 | **Not corporate-heavy.** No corporate hero blocks, no testimonials, no big logos. |
| DS-5 | **Low visual clutter.** Hairlines (0.5px borders), no shadows, no gradients, no glass effects, no glow. |
| DS-6 | **Clear hierarchy.** h1 22 px / h2 18 px on mobile, 24 / 20 on desktop. Body 15-16 px. Section labels in ALL CAPS at 12 px with 0.06 em letter-spacing. |
| DS-7 | **Single accent colour:** brand green `#14452a`. Used only for primary CTAs, links on hover, focus rings. |
| DS-8 | **Weights only 300 / 400 / 500.** No 700 / 900. |
| DS-9 | **Hairline rules** (0.5 px) instead of borders. Borders only at 1 px on cards. |

### 25.2 Layout

| Property | Mobile | Desktop |
|---|---|---|
| Content max-width | 100vw | 1080-1120 px (centred) |
| Card grid | 1 column | 2-3 columns (auto-fit minmax(240, 1fr)) |
| Card border-radius | 12 px | 6 px (var(--radius-lg)) |
| Card padding | 16 px | 24-32 px |
| Inline gutter | 16 px | 22.5 px |
| Header height | 56 px sticky | 56 px sticky |

### 25.3 Forbidden motion

- Card hover lift / shadow on hover
- Bouncy springs / wiggle / shake / pulse / glow
- Sliding panes
- Fading entire pages from blank
- Auto-playing audio without user gesture

### 25.4 Hover / focus / active

- **Hover (desktop)**: background lightens to `--color-surface-alt`, border strengthens to `--color-line-strong`. No translation, no shadow.
- **Focus (keyboard)**: 2 px solid outline with `--color-accent`, 2 px offset. Visible on every interactive element.
- **Active (mobile)**: brief `transform: scale(0.97); opacity: 0.85;` 80 ms transition. Applied at `≤768 px` only.

### 25.5 Disabled-button feedback (per §19 / §40)

Every disabled button must show a visible reason in UI text — not only via `title` tooltip. Patterns:

- Submit / Finish disabled until N answered → button text `Submit (N remaining)` + hint paragraph above.
- Check Answer disabled until any answer → type-aware hint: "Pick a choice", "Tap the tiles", "Type your answer".
- Confirm disabled until typed phrase → input field IS the visible reason.

---

## 26. Responsive Design Requirements

### 26.1 Required viewports

The app must render correctly at:

| Width | Device class | Notes |
|---|---|---|
| **320 px** | Galaxy S9+ tier (smallest supported) | All bottom-nav items fit; no horizontal scroll |
| **360 px** | Pixel / common Android | – |
| **390 px** | iPhone 14 / 15 | – |
| **480 px** | Small tablet portrait | Mobile bottom nav still active |
| **768 px** | iPad portrait / large tablet | Mobile bottom nav transitions to top primary nav |
| **1280 px** | Laptop | Desktop layout |
| **1920 px** | Full HD desktop | Desktop layout, max-width caps content at 1120 |

### 26.2 Mobile contract (consolidated)

`@media (max-width: 768px)`:

- `html, body { overflow-x: hidden; }` (safety belt)
- `html { scroll-behavior: smooth; }`
- All inputs (text/search/email/number, textarea, select) `font-size: 16px;` (iOS auto-zoom prevention)
- Body `font-size: max(16px, var(--text-base));`
- All interactive elements have `min-height: 44px` tap-target floor
- Visible `:active { transform: scale(0.97); opacity: 0.85; transition: 80ms }` on primary tap targets
- Heading hierarchy: `h2 { font-size: 18px; line-height: 1.35; }` (not desktop's 22 px)

`@media (max-width: 480px)`:

- Bottom-nav fixed at `position: fixed; bottom: 0; left: 0; right: 0; z-index: 900; gap: 0;`
- Pattern-detail header column-stacks (title + Mark-as-known toggle below)
- `main, .app-footer { padding-inline: 16px; }`
- `.app-header { gap: 12px; padding-inline: 16px; }`
- Pattern-usage-form table cell: `white-space: nowrap; word-break: keep-all;` for short Japanese forms

`@media (max-width: 380px)`:

- Bottom-nav font 11 px, padding 4 2, min-width 0 (so 5 nav items fit without overflow)

### 26.3 Hard rules

| ID | Rule |
|---|---|
| RES-1 | No horizontal scroll at any width 320-1920. |
| RES-2 | No card / Japanese sentence / table / button / grid item overflows its container at any width. |
| RES-3 | No CJK per-character wrap on titles. (Heading wrapping with avg < 3 chars/line is broken.) |
| RES-4 | All tap targets ≥ 44 px on smallest dimension at mobile widths. |
| RES-5 | Card descriptions render with clean line-aligned ellipsis; never mid-line clip (per §40). |
| RES-6 | Desktop (>768 px) is byte-identical after every mobile sweep — verify computed values match pre-sweep defaults. |

---

## 27. Accessibility Requirements

### 27.1 Conformance target

**WCAG 2.1 Level AA.**

### 27.2 Required behaviour

| ID | Requirement |
|---|---|
| AC-1 | Skip-to-content link works from keyboard, visible on focus. |
| AC-2 | All interactive elements reachable via Tab. Tab order matches visual order. |
| AC-3 | All interactive elements have visible focus indicators (2 px solid `--color-accent` outline at 2 px offset). |
| AC-4 | Sufficient contrast: text ≥ 4.5:1 against background; UI elements ≥ 3:1. Verified via axe-core. |
| AC-5 | Search input has an accessible label. |
| AC-6 | Correct/incorrect feedback NEVER conveyed by colour alone — always paired with text and/or icon. |
| AC-7 | Test choices keyboard-selectable (arrow keys + Enter; or 1/2/3/4 number keys). |
| AC-8 | Tap targets ≥ 44×44 px on mobile (per RES-4). |
| AC-9 | Disabled controls show a visible reason (per §19, §25.5). |
| AC-10 | `prefers-reduced-motion` disables non-essential animations. User can override in Settings. |
| AC-11 | Forced-colors / Windows High Contrast mode: all visible text remains visible. |
| AC-12 | Furigana ruby announces correctly by NVDA + Japanese voice. |
| AC-13 | Banner / nav / main / contentinfo landmarks present. |
| AC-14 | One `<h1>` per page; heading hierarchy descends without skipping levels. |
| AC-15 | Audio elements have controls; transcripts available per LS rules. |

### 27.3 CI gate

axe-core runs on Home / Learn / Test / Review / Settings on every release. Zero `serious` / `critical` violations. (Per `feedback/ui-testing-plan.md` §5.)

---

## 28. Data Model and JSON Schemas

The runtime data lives in `data/*.json`. **All schemas are embedded below; do NOT extract from the N5 source.** Every file has a `_meta` block with `schema_version`, `entity_count`, `id_range`, `id_gap_policy`, `history`.

### 28.1 `data/grammar.json`

```json
{
  "_meta": {
    "schema_version": 1,
    "entity_count": 210,
    "id_range": "n4-001..n4-210",
    "id_gap_policy": "Reserve numeric ranges per category. Retired IDs are NEVER re-used.",
    "history": [
      {"date": "2026-05-04", "delta": "+210 N4 patterns initial authoring"}
    ]
  },
  "patterns": [
    /* per §12.1 */
  ]
}
```

### 28.2 `data/vocab.json`

```json
{
  "_meta": {
    "schema_version": 2,
    "entity_count": 1500,
    "id_range": "n4.vocab.<section-slug>.<form>",
    "id_gap_policy": "Section-slug encoding allows cross-listing; same form in 2+ sections is intentional.",
    "history": [
      {"date": "2026-05-04", "delta": "+1500 N4 vocab initial authoring"}
    ]
  },
  "entries": [
    /* per §13.1 */
  ]
}
```

### 28.3 `data/kanji.json`

```json
{
  "_meta": {
    "schema_version": 1,
    "entity_count": 280,
    "id_range": "n4.kanji.<glyph>",
    "id_gap_policy": "ID is the literal glyph; never gappy.",
    "history": [
      {"date": "2026-05-04", "delta": "+280 kanji (106 N5 prerequisite + 174 N4 new)"}
    ]
  },
  "entries": [
    /* per §14.2 */
  ]
}
```

### 28.4 `data/reading.json`

```json
{
  "_meta": {
    "schema_version": 1,
    "entity_count": 30,
    "id_range": "n4.read.001..n4.read.030",
    "history": [
      {"date": "2026-05-04", "delta": "+30 N4 passages initial authoring"}
    ]
  },
  "passages": [
    /* per §15.2 */
  ]
}
```

### 28.5 `data/listening.json`

```json
{
  "_meta": {
    "schema_version": 1,
    "entity_count": 30,
    "id_range": "n4.listen.001..n4.listen.030",
    "history": [
      {"date": "2026-05-04", "delta": "+30 N4 items initial authoring"}
    ]
  },
  "items": [
    /* per §16.2 */
  ]
}
```

### 28.6 `data/questions.json`

```json
{
  "_meta": {
    "schema_version": 1,
    "entity_count": 530,
    "id_range": "q-0001..q-9999 (opaque, never re-numbered)",
    "history": [
      {"date": "2026-05-04", "delta": "+530 N4 questions initial authoring"}
    ]
  },
  "questions": [
    /* per §17.2 */
  ]
}
```

### 28.7 `data/papers/manifest.json`

```json
{
  "_meta": {
    "schema_version": 1,
    "totalPapers": 35,
    "totalQuestions": 525
  },
  "categories": [
    {
      "id": "moji",
      "label": "Moji (Kanji)",
      "label_ja": "文字",
      "description": "Kanji reading, orthography, word formation",
      "paperCount": 10,
      "questionCount": 150,
      "papers": [
        {"id": "moji-1", "questions": 15, "title": "Moji Paper 1"},
        {"id": "moji-2", "questions": 15, "title": "Moji Paper 2"},
        ...
      ]
    },
    {"id": "goi", ...},
    {"id": "bunpou", ...},
    {"id": "dokkai", ...}
  ]
}
```

### 28.8 `data/papers/<category>/paper-<n>.json`

```json
{
  "_meta": {
    "id": "moji-1",
    "category": "moji",
    "paper_number": 1,
    "question_count": 15
  },
  "questions": [
    /* per §17.2; subset of data/questions.json */
  ]
}
```

### 28.9 `data/audio_manifest.json`

```json
{
  "_meta": {
    "schema_version": 1,
    "total_files": 600,
    "voice_default": "synthetic"
  },
  "files": {
    "n4-001.0": {"path": "audio/n4-001.0.mp3", "voice": "synthetic", "duration_sec": 4.2},
    "n4.read.001": {"path": "audio/n4.read.001.mp3", "voice": "synthetic", "duration_sec": 22.8},
    "n4.listen.001": {"path": "audio/n4.listen.001.mp3", "voice": "synthetic", "duration_sec": 35.4}
  }
}
```

### 28.10 `data/n4_kanji_whitelist.json`

```json
[
  "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
  /* ... 270 more ... */
]
```

### 28.11 `data/n4_kanji_readings.json`

```json
{
  "一": {"on": ["イチ", "イツ"], "kun": ["ひと(つ)", "ひと"], "primary": "イチ", "primary_kind": "on"},
  /* ... per §14.2 ... */
}
```

### 28.12 `data/n4_vocab_whitelist.json`

```json
[
  "私", "あなた", "学生", "先生",
  /* ... 1496 more entries ... */
]
```

### 28.13 LocalStorage schemas (runtime state)

```js
// jlpt-n4-tutor:settings (per §23)
{
  "uiLang": "en",
  "theme": "system",
  "fontSize": "m",
  "showFurigana": true,
  "showEnglishTranslation": true,
  "studyMode": "detailed",
  "lastTestLength": 30,
  "shuffleQuestions": true,
  "audioPlaybackRate": 1.0,
  "reduceMotion": "auto"
}

// jlpt-n4-tutor:history (per §10 / §A.10 SM-2)
{
  "n4-001": {"EF": 2.5, "rep": 2, "interval": 6, "due": "2026-05-10", "lapses": 0},
  ...
}

// jlpt-n4-tutor:streak
{"current": 7, "longest": 23, "lastStudyDate": "2026-05-04", "days": [...]}

// jlpt-n4-tutor:results (test attempts)
[
  {"sessionId": "s-001", "date": "2026-05-04", "score": 47, "total": 60, "pct": 78,
   "breakdown": {"bunpou": [13,17], "goi": [14,17], "moji": [15,17], "dokkai": [3,6], "chokai": [2,3]}}
]

// jlpt-n4-tutor:weakAreas
{
  "n4-001": 3,
  "reading-detail": 2,
  "listening-task": 1
}
```

### 28.14 Export bundle schema

```json
{
  "schemaVersion": 2,
  "exportedAt": "2026-05-04T12:00:00Z",
  "appVersion": "v1.0.0",
  "settings": {...},
  "history": {...},
  "knownKanji": [...],
  "knownVocab": [...],
  "streak": {...},
  "results": [...],
  "weakAreas": {...},
  "completedReading": [...],
  "completedListening": [...],
  "placement_result": {...}
}
```

---

## 29. File and Folder Structure

The full N4 repo structure. Every path is locked.

```
jlpt-n4-tutor/
├── .claude/
│   ├── CLAUDE.md                      # Binding rule for Claude Code (autonomous in this repo)
│   └── settings.local.json            # Local permission overrides (gitignored)
├── .github/
│   └── workflows/
│       ├── content-integrity.yml      # CI: runs check_content_integrity.py + test_build_data.py on every PR/push
│       ├── lighthouse.yml             # CI: runs Lighthouse on Home/Learn/Test
│       ├── playwright.yml             # CI: runs Playwright smoke tests
│       └── pages-build.yml            # GitHub Pages deployment workflow
├── KnowledgeBank/                     # Source-of-truth markdown (human-editable)
│   ├── grammar_n4.md
│   ├── kanji_n4.md
│   ├── vocabulary_n4.md
│   ├── moji_questions_n4.md
│   ├── goi_questions_n4.md
│   ├── bunpou_questions_n4.md
│   ├── dokkai_questions_n4.md
│   ├── chokai_questions_n4.md
│   └── sources.md                     # Source authorities + citation policy
├── data/                              # Runtime JSON (regenerated from KB by build_data.py)
│   ├── grammar.json
│   ├── vocab.json
│   ├── kanji.json
│   ├── reading.json
│   ├── listening.json
│   ├── questions.json
│   ├── audio_manifest.json
│   ├── n4_kanji_whitelist.json
│   ├── n4_kanji_readings.json
│   ├── n4_vocab_whitelist.json
│   └── papers/
│       ├── manifest.json
│       ├── moji/paper-1.json ... paper-10.json
│       ├── goi/paper-1.json ... paper-10.json
│       ├── bunpou/paper-1.json ... paper-7.json
│       └── dokkai/paper-1.json ... paper-5.json
├── tools/                             # Build-time Python scripts
│   ├── build_data.py
│   ├── build_audio.py
│   ├── build_papers.py
│   ├── check_content_integrity.py
│   ├── test_build_data.py
│   ├── link_grammar_examples_to_vocab.py
│   ├── scan_multi_correct.py
│   ├── heuristic_audit.py
│   ├── llm_audit.py
│   ├── tag_vocab_pos.py
│   ├── coverage_compare.py
│   └── prompts/
│       └── llm_audit.prompt.md
├── js/                                # Vanilla ES modules (one per route/concern)
│   ├── app.js                         # Entry: router, route handlers, skeleton render
│   ├── home.js                        # Syllabus dashboard
│   ├── learn.js                       # Grammar list + detail
│   ├── vocab.js                       # Vocab list + detail
│   ├── kanji.js                       # Kanji list + detail
│   ├── kanji-popover.js               # Inline kanji popover on hover
│   ├── reading.js                     # Reading module
│   ├── listening.js                   # Listening module
│   ├── test.js                        # Test engine
│   ├── papers.js                      # Mock-test papers
│   ├── placement.js                   # Placement check
│   ├── results.js                     # Test results page
│   ├── weak-areas.js                  # Weak-area review
│   ├── progress.js                    # Progress dashboard
│   ├── search.js                      # Global search
│   ├── settings.js                    # Settings page
│   ├── changelog.js                   # CHANGELOG.md renderer
│   ├── feedback.js                    # Feedback form
│   ├── storage.js                     # LocalStorage wrappers + SM-2 SRS math
│   ├── srs.js                         # SM-2 SRS pure functions
│   ├── furigana.js                    # Ruby renderer + tokeniser hook
│   ├── i18n.js                        # Locale loading + translation
│   ├── pwa.js                         # SW registration + install prompt
│   └── shortcuts.js                   # Keyboard shortcuts
├── css/
│   └── main.css                       # All styles (no preprocessor; vanilla CSS)
├── locales/
│   ├── en.json
│   ├── vi.json
│   ├── id.json
│   ├── ne.json
│   └── zh.json
├── audio/                             # MP3s (synthetic for v1; native re-record path for v2)
│   ├── n4-001.0.mp3 ... n4-XXX.X.mp3 # Grammar example audio
│   ├── n4.read.001.mp3 ...           # Reading passage audio
│   └── n4.listen.001.mp3 ...         # Listening item audio
├── svg/
│   └── kanji/
│       └── 一.svg ... 力.svg          # 280 KanjiVG stroke-order SVGs
├── fonts/
│   ├── inter-300.woff2
│   ├── inter-400.woff2
│   ├── inter-500.woff2
│   └── noto-sans-jp-400.woff2         # Subset to N4 (N5 ∪ N4 = 280 kanji)
├── tests.html                         # Browser-runnable engine tests (~40 tests)
├── playwright.config.js               # Playwright config (smoke + visual regression)
├── tests-e2e/                         # Playwright tests
│   ├── p0-smoke.spec.js
│   ├── homepage.spec.js
│   ├── grammar-detail.spec.js
│   ├── test-flow.spec.js
│   ├── search.spec.js
│   ├── responsive.spec.js
│   └── a11y.spec.js
├── feedback/
│   ├── ui-testing-plan.md
│   └── (other feedback / audit docs)
├── specifications/
│   └── (level-specific design notes if any)
├── package.json                       # Playwright + lighthouse-ci + axe-core dependencies only
├── index.html
├── manifest.webmanifest
├── sw.js                              # Service worker (jlpt-n4-tutor-v1)
├── README.md
├── CHANGELOG.md
├── PRIVACY.md
├── NOTICES.md
├── CONTENT-LICENSE.md                 # Original-content policy + reference sources + JEES contact path
├── TASKS.md                           # Single source of truth for project state
├── MEMORY.md                          # Session-to-session continuity (≤200 lines)
└── .gitignore
```

### 29.1 Source-of-truth approach

**Markdown-first, JSON-derived.** `KnowledgeBank/*.md` is human-editable; `data/*.json` is regenerated from it by `tools/build_data.py`. Never edit `data/*.json` directly. (NN-13.)

Exception: post-build enrichment scripts (`link_grammar_examples_to_vocab.py`, `tag_vocab_pos.py`) add fields the markdown doesn't carry (vocab_ids, audio paths, detected PoS). These run after `build_data.py` and before integrity check.

---

## 30. Content Source and Research Rules

### 30.1 Authoritative sources for N4 content

JLPT no longer publishes a fixed official grammar / vocabulary / kanji list (last official list: 2009 syllabus). N4 content must be triangulated across credible sources:

| Source | URL | Use for |
|---|---|---|
| **JLPT Sensei N4** | jlptsensei.com/jlpt-n4-{kanji,vocab,grammar}-list/ | Primary inventory list |
| **Tanos N4** | tanos.co.uk/jlpt/jlpt4/{kanji,vocab,grammar}/ | Cross-reference inventory + frequency data |
| **Bunpro N4** | bunpro.jp/jlpt/n4 | Grammar pattern catalogue + register notes |
| **JLPT.jp official samples** | jlpt.jp/e/samples/n4/index.html | Authentic question format reference |
| **Genki II / Minna no Nihongo II** | (textbooks) | Pedagogy + chapter ordering |

### 30.2 Source rules

| ID | Rule |
|---|---|
| CS-1 | No single source is absolute. Cross-reference at least TWO sources per item before adding to a catalogue. |
| CS-2 | Discrepancies between sources → resolve in favour of the most-recent JLPT.jp official sample. |
| CS-3 | Do NOT copy copyrighted past-paper questions verbatim. Use as reference for format / topic distribution / difficulty calibration only. |
| CS-4 | Final authored content is original. (Per `CONTENT-LICENSE.md`.) |
| CS-5 | Past-paper provenance signatures (specific phrasings from JEES samples) are checked at CI by `tools/audit_provenance.py`. (JA-30.) |
| CS-6 | When listing source citations in `KnowledgeBank/sources.md`, include date-of-fetch and URL. Sources with paywall or login: don't use. |

### 30.3 Original-content policy

The N4 corpus (grammar examples, vocabulary, kanji example words, reading passages, listening scripts, mock-test questions) MUST be authored fresh. Reuse from N5 corpus is allowed for:

- N5 prerequisite kanji (reuse N5 kanji entries verbatim, retag `tier: n5_prerequisite`).
- N5 prerequisite vocab if it appears in N4 contexts (reuse with retag).

Never reuse: N4 grammar / N4 reading / N4 listening / N4 questions. Author all N4-specific content fresh per §12-17.

---

## 31. Japanese Language Quality Rules

### 31.1 Hard quality bar

Every authored entry must pass these checks before release:

| ID | Check |
|---|---|
| Q-1 | Natural Japanese (read aloud by a native speaker → no awkwardness). |
| Q-2 | Correct grammar explanations (English text matches what Japanese examples actually do). |
| Q-3 | Correct particles (は/が/を/に/で/と/から/まで/より/の/も used per N4 norms). |
| Q-4 | Correct conjugations (especially Group-1 vs Group-2 verbs, see §31.2 anti-pattern). |
| Q-5 | Correct readings (verified against the N4 readings table). |
| Q-6 | Correct kanji usage (in-scope only, per JA-13). |
| Q-7 | Correct English meanings (no semantic drift). |
| Q-8 | Appropriate N4 difficulty (not N3 or higher unless tagged). |
| Q-9 | No N3+ content presented as core_n4 (NN-2). |
| Q-10 | No unnatural examples (e.g., "Watashi wa pan to coffee wo tabemashita" — you don't *eat* coffee). |
| Q-11 | No misleading explanations (e.g., calling と for direction when it's actually で). |

### 31.2 Anti-patterns (lessons from N5)

| ID | Anti-pattern | Mitigation |
|---|---|---|
| AP-1 | **PoS by thematic section**: marking every entry in section "Time / Frequency" as `pos: noun` regardless of word. Adverbs (`いつも`, `よく`) get mistagged. **Group-2 verbs in section "Existence / Possession" mistagged as `verb-1` causes `*あげります` instead of `あげます` to be taught — pedagogically dangerous.** | Tag PoS per-WORD, never per-section default. JA-31 enforces parity. |
| AP-2 | **Multi-correct via interchangeable particles**: questions where both に AND へ appear in choices for direction-of-motion, or both から AND ので for reason. | Multi-correct scanner (`tools/scan_multi_correct.py`); JA-23. |
| AP-3 | **Stub redirect text**: auto-generated `"see pattern X"` distractor explanations or note fields. | Author distractor explanations by hand; JA-10. |
| AP-4 | **Cross-references to retired patterns**: `contrasts.with_pattern_id` pointing to a deleted ID. | Repoint or remove on every dedup pass; JA-32. |
| AP-5 | **PoS taxonomy drift**: introducing new question subtypes via data without code change. | JA-29 closes the subtype taxonomy; new subtypes require code change. |
| AP-6 | **Past-paper provenance**: copying JEES sample wording verbatim. | `tools/audit_provenance.py` + JA-30. |
| AP-7 | **Mid-line clip on tile-grid card descriptions**: `flex: 1` + `-webkit-line-clamp` + fixed parent height = mid-line crop. | `max-height: Nlh` + remove `flex: 1` + `margin-top: auto` on action element. |
| AP-8 | **Stale module state on URL navigation**: `view === 'finished'` short-circuits routing when user clicks "Back". | Reset state on URL change (per RT-4). |

### 31.3 Reviewer roles

| Role | Coverage | When |
|---|---|---|
| **Native Japanese teacher review** | Spot-check ~30% of corpus | After 50% authoring (Pass-1) and after 100% authoring (Pass-2) |
| **LLM audit** (Claude API via `tools/llm_audit.py`) | All grammar patterns + 25% sample of questions | Between native review windows; ~$11.50 per full pattern-corpus pass |
| **Deterministic lint scripts** | All content | Every commit (CI gate) |
| **Final human sponsor sign-off** | Verify acceptance criteria met | Before v1.0.0 release |

---

## 32. Build Pipeline Requirements

### 32.1 `tools/build_data.py`

Reads `KnowledgeBank/*.md` and writes `data/*.json`.

| Behaviour | Required |
|---|---|
| Idempotent | Re-running on unchanged input produces no diff |
| Parser | Per-file regexes per N4 KB markdown grammar (see §32.4) |
| Output | `data/grammar.json`, `data/vocab.json`, `data/kanji.json`, `data/questions.json`, with `_meta` blocks populated |
| Test coverage | `tools/test_build_data.py` covers regression cases (e.g., `[Ext]`-tagged kanji headers, parenthetical glosses with commas) |

### 32.2 `tools/build_audio.py`

Auto-detects available TTS backend in this priority order: piper-tts > gtts > pyttsx3. Reads `data/grammar.json` + `data/reading.json` + `data/listening.json`, renders missing MP3s to `audio/`. Writes / updates `data/audio_manifest.json`. Idempotent.

### 32.3 `tools/build_papers.py`

Reads `data/questions.json`, partitions per category, slices into 15-question papers, writes `data/papers/<category>/paper-<n>.json` and `data/papers/manifest.json`.

### 32.4 KB markdown grammar (BNF-ish)

The build pipeline parses `KnowledgeBank/*.md` per these rules (consistent with N5):

```
GRAMMAR_FILE := SECTION_HEADER ENTRY+ (SECTION_HEADER ENTRY+)*
SECTION_HEADER := "## " <name> "\n"
ENTRY := PATTERN_HEADER FIELD+ EXAMPLE+ COMMON_MISTAKES?
PATTERN_HEADER := "### " <pattern> " — " <id> "\n"
FIELD := "**" <field-name> ":** " <value> "\n"
EXAMPLE := "- ex" <n> ": " <ja> " — " <en> "\n"

VOCAB_FILE := SECTION_HEADER ENTRY+ ...
ENTRY := "- **" <form> "** [" <reading> "] (" <pos> ") — " <gloss> "\n"
       | "- **" <form> "** [" <reading> "] (" <pos> ") (" <tier> ") — " <gloss> "\n"

KANJI_FILE := KANJI_ENTRY+
KANJI_ENTRY := "## " <glyph> "\n" "- on: " <on-list> "\n" "- kun: " <kun-list> "\n" ...

QUESTION_FILE := MONDAI_HEADER QUESTION+
MONDAI_HEADER := "## Mondai " <n> " — " <name> "\n"
QUESTION := "### Q" <n> "\n" STEM CHOICES ANSWER EXPLANATION
```

Full parser tests in `tools/test_build_data.py`.

### 32.5 Build flow on every commit

```
1. python tools/build_data.py
2. python tools/build_papers.py
3. python tools/link_grammar_examples_to_vocab.py
4. python tools/tag_vocab_pos.py
5. python tools/check_content_integrity.py    # MUST exit 0
6. python tools/test_build_data.py            # MUST exit 0
```

CI workflow `.github/workflows/content-integrity.yml` runs steps 1-6 on every push and PR. Hard fail. Never `continue-on-error: true`.

---

## 33. Content Integrity and Validation Rules

### 33.1 Required validation rules (33 invariants)

| ID | What it checks |
|---|---|
| **X-6.1** | Catalogue completeness — every grammar pattern has examples + form_rules |
| **X-6.2** | Year-form consistency — 今年 / こんねん / ことし usage matches policy |
| **X-6.3** | No mixed kanji+kana words (e.g., 大さか for おおさか) |
| **X-6.4** | Lint script present |
| **X-6.5** | No em-dashes (U+2014) or en-dashes (U+2013) anywhere |
| **X-6.6** | Group-1 ru-verb exceptions flagged at section header AND per-entry |
| **X-6.7** | No false synonymy ("direct synonym" / "directly equivalent") in goi rationales |
| **X-6.8** | No ASCII digits in TTS source (numbers must be in kanji or kana) |
| **X-6.9** | Primary-reading sanity — most-frequent in N4 context |
| **JA-1** | Stem kanji scope — question stems use only N4-whitelist kanji |
| **JA-2** | Particle-set sanity — particle MCQs have valid particle distractors |
| **JA-3** | Furigana / catalogue match — annotations match catalogue |
| **JA-4** | Vocab reading uniqueness — no accidental duplicate readings |
| **JA-5** | Answer-key sanity — `correctAnswer` in `choices` |
| **JA-6** | No two-correct-answers — duplicate stem with same answer |
| **JA-7** | No duplicate stems in file |
| **JA-8** | Q-count integrity — `_meta.question_count` matches `len(questions)` |
| **JA-9** | Engine display contract — UI hides answer until commit (Playwright test) |
| **JA-10** | No "see pattern X" stub redirects in user-facing fields |
| **JA-11** | No duplicate MCQ choices — all 4 distinct |
| **JA-12** | Kanji KB / JSON consistency — KB markdown and JSON have same set |
| **JA-13** | No out-of-scope kanji in user-facing data |
| **JA-14** | No auto-ruby in renderer — UI never auto-applies furigana to whitelisted kanji |
| **JA-15** | Audio refs resolve — every audio path in JSON has a file on disk |
| **JA-16** | Kanji example whitelist — examples use only target+whitelist kanji |
| **JA-17** | Grammar examples have `vocab_ids` (homograph guard) |
| **JA-18** | Reading explanation kanji ⊂ passage |
| **JA-19** | Reading info-search has `format_type` |
| **JA-20** | Reading choices kanji ⊂ passage |
| **JA-21** | Late-tier markers require `tier=late_n4` |
| **JA-22** | Vocab kun readings deduplicated |
| **JA-23** | Multi-correct scanner — interchangeable particle pairs without scene context flagged |
| **JA-24** | i-adjective primary reading is kun-yomi |
| **JA-25** | Whitelist exceptions documented — out-of-scope kanji require WHY-comment |
| **JA-26** | No duplicate question IDs across the entire bank |
| **JA-27** | No English-translation/title fields in reading/listening (JA-first surface) |
| **JA-28** | Dokkai-paper kanji bounded by N4 + exception list |
| **JA-29** | Question subtype taxonomy is closed (paraphrase / kanji_writing only) |
| **JA-30** | No past-paper provenance signatures in question text |
| **JA-31** | Vocab PoS parity — `pos` field in JSON agrees with KB markdown PoS tags (homograph-aware set-valued match) |
| **JA-32** | Broken cross-references — `contrasts.with_pattern_id` and "See n4-NNN" in `form_rules.conjugations.label` resolve to existing IDs |
| **JA-33** | No mid-line clipping in tile-grid card descriptions — Playwright visual regression |

### 33.2 Required scripts

- `tools/check_content_integrity.py` — runs all 33 invariants; exits 0 / prints violations
- `tools/test_build_data.py` — build pipeline regression tests
- `tools/scan_multi_correct.py` — JA-23 multi-correct scanner
- `tools/heuristic_audit.py` — fast deterministic content audit (~75% precision per N5 baseline)
- `tools/llm_audit.py` — Claude API audit for deeper semantic review

### 33.3 Required CI checks

- `.github/workflows/content-integrity.yml` — runs steps 1-6 from §32.5 on every push + PR
- `.github/workflows/lighthouse.yml` — runs Lighthouse on Home/Learn/Test; PWA = 100, Performance ≥ 90 mobile / ≥ 95 desktop, Accessibility ≥ 95
- `.github/workflows/playwright.yml` — runs `tests-e2e/p0-smoke.spec.js` + `a11y.spec.js`
- `.github/workflows/pages-build.yml` — deploys to GitHub Pages on `main` push (only after the above pass)

### 33.4 Required acceptance criteria

| ID | Criterion |
|---|---|
| AT-1 | All 33 invariants pass (`tools/check_content_integrity.py` exits 0) |
| AT-2 | Build pipeline tests pass (`tools/test_build_data.py` exits 0) |
| AT-3 | All `data/*.json` parse, have populated `_meta`, `_meta.entity_count == len(entries)` |
| AT-4 | No duplicate IDs across questions / patterns / vocab / kanji / reading / listening |
| AT-5 | No empty user-facing fields |
| AT-6 | Zero matches for `see n4-` / `see pattern detail` in user-facing fields |
| AT-7 | Zero out-of-scope kanji in user-facing text (JA-13) |
| AT-8 | Browser smoke test: `index.html` loads, hash routes resolve, no console errors, SW registers |
| AT-9 | Question count meets minimum: ≥150 moji, ≥150 goi, ≥100 bunpou, ≥70 dokkai, ≥60 chokai |
| AT-10 | PWA installable; manifest valid; offline shell works |
| AT-11 | TASKS.md current; status snapshot reflects corpus counts; no `[ ]` items in active Pass without "deferred" rationale |
| AT-12 | No em-dashes / en-dashes in committed files (X-6.5) |

---

## 34. Tooling Requirements

Port these scripts from `<JLPT-root>/N5/tools/` to `<target-repo>/tools/` verbatim. Token-substitute `n5` → `n4`, `N5` → `N4`. Order = priority for a one-shot build.

| # | Script | What it does |
|---|---|---|
| 1 | `build_data.py` | KB markdown → JSON. Most-important script. |
| 2 | `check_content_integrity.py` | 33-invariant CI gate. |
| 3 | `test_build_data.py` | Build-pipeline regression tests. |
| 4 | `link_grammar_examples_to_vocab.py` | Homograph-aware vocab linking. Extend `HOMOGRAPH_RULES` for N4-specific clusters (e.g., 込 readings). |
| 5 | `scan_multi_correct.py` | Multi-correct candidate scanner. CI gate. |
| 6 | `heuristic_audit.py` | Cheap mass-scan deterministic findings. |
| 7 | `llm_audit.py` | Claude API audit. Update prompt template at `tools/prompts/llm_audit.prompt.md` for N4 scope. |
| 8 | `build_audio.py` | TTS pipeline. Idempotent. |
| 9 | `build_papers.py` | Slices `data/questions.json` into 15-question papers. |
| 10 | `tag_vocab_pos.py` | PoS tagging for vocab. Extend rules per §13.1 / §31.2 anti-pattern. |
| 11 | `coverage_compare.py` | External-corpus gap analysis. |
| 12 | `audit_provenance.py` | JA-30 past-paper provenance check. |
| 13 | `audit_audio_coverage.py` | Audio file presence vs `data/audio_manifest.json`. |

Skip these (one-shot N5 diagnostics): `_inspect_*.py`, `_check_*.py`, `fix_kosoado_*.py`, `fix_pass15_tier2.py`. They are N5-specific debugging artifacts.

---

## 35. GitHub Pages Deployment Requirements

### 35.1 Hard requirements

| ID | Rule |
|---|---|
| GH-1 | Static-site only. No backend. |
| GH-2 | Repository name: `jlpt-n4-tutor`. |
| GH-3 | Base path: `/jlpt-n4-tutor/` (i.e., `<org>.github.io/jlpt-n4-tutor/`). |
| GH-4 | All asset paths in `index.html`, `sw.js`, `manifest.webmanifest`, JS modules MUST be relative (`./js/app.js`, not `/js/app.js`). |
| GH-5 | Hash-based routing (`#/...`) — refresh on any route MUST not 404. |
| GH-6 | Service worker path: `/sw.js` at the repo root; scope = `/jlpt-n4-tutor/`. |
| GH-7 | Deployment branch: `main` (auto-deploy via `.github/workflows/pages-build.yml`). |
| GH-8 | A `404.html` fallback at the repo root that just `<meta http-equiv="refresh" content="0;url=./">` redirects. (For the rare case a non-hash 404 happens.) |
| GH-9 | `manifest.webmanifest` `start_url` and `scope` are relative (`.`). |
| GH-10 | All build artifacts (HTML/CSS/JS/JSON/MP3/SVG/woff2) committed to the repo. No external CDN dependency at runtime. |

### 35.2 Deployment workflow

```yaml
# .github/workflows/pages-build.yml (skeleton)
name: Pages build
on:
  push:
    branches: [main]
permissions:
  contents: read
  pages: write
  id-token: write
jobs:
  deploy:
    environment:
      name: github-pages
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/configure-pages@v4
      - uses: actions/upload-pages-artifact@v3
        with:
          path: '.'
      - id: deployment
        uses: actions/deploy-pages@v4
```

### 35.3 PWA / Service worker

- `sw.js` precaches the shell + `data/*.json` + audio + fonts on install.
- Strategy: stale-while-revalidate for shell; cache-first for content (data/audio/locales).
- On new shell bytes detected: post `SW_UPDATE_AVAILABLE` to clients; UI shows non-blocking "Update available" toast with reload button.
- Cache version: `jlpt-n4-tutor-v<N>`. Bump on every shell change.

---

## 36. QA Test Scenarios

Run all 14 before declaring v1 release-ready.

| # | Scenario | Pass criteria |
|---|---|---|
| 1 | Open homepage `#/home` | h1 reads `JLPT N4 Syllabus`. Footer shows version. No N5 labels. |
| 2 | Verify no N5 labels remain except prerequisite references | Grep DOM for "N5" → only matches inside prerequisite badges. |
| 3 | Open each of the 6 syllabus cards | Each routes to its module page, page loads with expected content. |
| 4 | Open grammar list `#/grammar` and a detail page `#/grammar/n4-001` | List renders with grouping; detail shows pattern + examples + common-mistakes. |
| 5 | Search "ように" via search input | Results show ≥1 match (the n4-001 grammar entry); clicking navigates to detail. |
| 6 | Take mock test with all correct answers | Submit enables; results show 100%; weak areas list is empty. |
| 7 | Take mock test with wrong answers | Submit; results show <100%; weak-areas page shows the missed items. |
| 8 | Verify weak areas are generated | After scenario 7, `#/weak-areas` shows the missed patterns grouped by skill. |
| 9 | Verify progress updates | Mark a kanji as known on detail page; `#/progress` Kanji row updates. |
| 10 | Reset progress | Settings → Reset → type "RESET" → confirm. localStorage cleared. Redirected to `#/home`. |
| 11 | Refresh GitHub Pages route | At `<live>/jlpt-n4-tutor/#/grammar/n4-001`, F5 → page reloads to same route (no 404). |
| 12 | Test mobile layout at 320 / 360 / 390 px | No horizontal scroll. Bottom nav visible. Submit button hint shows count. Card descriptions don't mid-line clip. |
| 13 | Verify no horizontal overflow at any width | Resize 320 → 1920; `document.scrollWidth === clientWidth` at every step. |
| 14 | Verify Japanese examples are natural and N4-appropriate | Sample 50 random examples; native or LLM review; zero unnatural / N3+ leakage. |

---

## 37. Acceptance Criteria

The N4 app is **complete and release-ready** only when ALL items below are true:

| # | Criterion | Verification |
|---|---|---|
| 1 | All 13 functional modules exist (§9) | Manual click-through of every route |
| 2 | All N4 datasets load (`data/*.json` has populated `entries`) | `_meta.entity_count > 0` for each |
| 3 | Homepage shows N4 syllabus dashboard per §10 | h1 = "JLPT N4 Syllabus", 6 cards, study order, progress, placement entry |
| 4 | Tests auto-score (no manual grading) | Submit a test → results render immediately, no network call |
| 5 | Submit button is disabled until all answered, with visible reason | Manual: leave 1 question blank → button shows `Submit (1 remaining)` + hint |
| 6 | Results display immediately, no reload | Manual: submit → results page shows instantly without `location.reload()` |
| 7 | Weak areas generate correctly | After a failed test, `#/weak-areas` populated |
| 8 | Progress persists across reload | Mark kanji known → reload → still marked known |
| 9 | Search works (Japanese / kana / English / pattern / kanji) | All 5 input types return relevant results |
| 10 | GitHub Pages deployment works | Live site loads at `<org>.github.io/jlpt-n4-tutor/` |
| 11 | No N5 labels remain (except prerequisite badges) | Grep DOM at every route |
| 12 | Japanese content passes quality review | LLM audit + spot-check by native reviewer; zero CRITICAL findings |
| 13 | All 33 CI invariants pass | `python tools/check_content_integrity.py` exits 0 |
| 14 | All Playwright smoke tests pass | `npx playwright test` exits 0 |
| 15 | Lighthouse: PWA = 100, Performance ≥ 90 mobile, Accessibility ≥ 95 | CI gate |
| 16 | Responsive at 320 / 360 / 390 / 768 / 1280 / 1920 with no horizontal scroll | Manual + Playwright responsive.spec.js |
| 17 | Accessibility: zero axe-core `serious` / `critical` violations | CI gate |
| 18 | Em-dash-free | `tools/check_content_integrity.py` X-6.5 |
| 19 | TASKS.md current; status snapshot accurate | Manual review of TASKS.md top section |
| 20 | CHANGELOG.md has v1.0.0 entry | Manual |

---

## 38. Final Deliverables

The build is complete on delivery of:

1. **Working N4 web app** at `https://<org>.github.io/jlpt-n4-tutor/`.
2. **Complete source repo** at `<JLPT-root>/N4/` with the file structure per §29.
3. **N4 grammar dataset** — `data/grammar.json` with ~210 patterns + KB markdown source.
4. **N4 vocabulary dataset** — `data/vocab.json` with ~1500 entries + KB markdown source.
5. **N4 kanji dataset** — `data/kanji.json` with 280 kanji entries + KB markdown source + 280 stroke-order SVGs.
6. **N4 reading dataset** — `data/reading.json` with ~30 passages + KB markdown source.
7. **N4 listening dataset + scripts** — `data/listening.json` + ~30 MP3s in `audio/` + KB markdown source.
8. **N4 question bank** — `data/questions.json` with ~530 questions across 5 Mondai files.
9. **N4 mock-test paper structure** — `data/papers/manifest.json` + ~32 paper JSONs.
10. **Homepage syllabus dashboard** — per §10.
11. **Test engine** — placement / section / full / weak-area / paper modes, per §18.
12. **Weak-area review module** — per §20.
13. **Progress tracking** — per §21.
14. **Search** — per §22.
15. **Settings** — per §23.
16. **README.md** — project overview, link to live site, link to spec, contributor guide.
17. **TASKS.md** — single source of truth for project state. Pass-1 section populated with deferred items + rationale.
18. **MEMORY.md** — ≤200 lines, summarises project location, branch, HEAD SHA, file inventory, current state, what's next.
19. **CHANGELOG.md** — v1.0.0 entry describing what shipped.
20. **PRIVACY.md** — privacy policy (no telemetry, no accounts, all-local).
21. **CONTENT-LICENSE.md** — original-content policy + reference sources.
22. **Validation checklist** — `tools/check_content_integrity.py -v` output (saved as `feedback/validation-v1.0.0.txt`).
23. **Deployment instructions** — README.md "Deploy" section + `.github/workflows/pages-build.yml`.

---

## 39. Coding Agent Execution Instructions

### 39.1 The trigger

When a human says any of:
- "build the N4 app"
- "build the next level"
- "make N4"
- "scaffold N4"
- "go" (immediately after this spec was shared)
- "ya" / "yes" / "proceed" (after offering "shall I build N4?")

…execute the procedure in §39.3 autonomously.

### 39.2 Required runtime posture

Before starting:

1. Confirm running with `--dangerously-skip-permissions` (or equivalent). If not, halt: "Cannot run autonomously without skip-permissions flag. Restart with the flag and re-trigger."
2. Confirm `<JLPT-root>` resolves to the parent of the source N5 repo. (E.g., `C:\Users\.../Documents/VS Code/JLPT/`.)
3. Confirm target directory `<JLPT-root>/N4/` does NOT exist (or is empty). If non-empty, halt: "Target N4 directory non-empty. Clear it manually or specify a different path."

### 39.3 Execution sequence (15 steps)

Each step is **idempotent**: it checks `<JLPT-root>/N4/.build-progress.json` and skips if already complete. After each step, write to `.build-progress.json`, commit with tag `[build-step N/15]`, and proceed.

```
STEP 0: PRE-FLIGHT
  - Resolve paths.
  - Verify halt conditions (§39.2).
  - Read source repo (<JLPT-root>/N5/) for token substitution context.
  - Read or create .build-progress.json.

STEP 1: REPO SKELETON  (~30 min)
  - mkdir <target>; cd <target>; git init.
  - Copy directory structure from <source-repo> per §29, applying token substitutions:
    * filenames containing 'n5' → 'n4'
    * file contents: s/N5/N4/g, s/n5/n4/g, s/jlpt-n5-tutor/jlpt-n4-tutor/g
  - Wipe content from KB markdown (keep section structure only).
  - Wipe content from data/*.json (keep _meta, set entries:[]).
  - Touch TASKS.md, MEMORY.md per templates.
  - .build-progress.json = {step: 1, ...}.
  - git add -A; git commit -m "chore: scaffold N4 from N5 [build-step 1/15]"
  - git push origin HEAD (best-effort).

STEP 2: PERMISSION + CI WIRING  (~10 min)
  - Verify .claude/settings.local.json has skip-permissions deny-list.
  - Verify .github/workflows/* fire on push/pr/dispatch.
  - Run python tools/check_content_integrity.py — pass on empty corpus.
  - Commit "ci: integrity gate green on empty corpus [build-step 2/15]"

STEP 3: KANJI WHITELIST  (~1-2 hr)
  - Read feedback/n4-kanji-inventory.md if present.
  - Else WebFetch jlptsensei.com/jlpt-n4-kanji-list/ + tanos.co.uk/jlpt/jlpt4/kanji/.
  - Merge with N5 whitelist; total = 280 glyphs.
  - Write data/n4_kanji_whitelist.json (sorted by lesson_order).
  - Write data/n4_kanji_readings.json with on/kun/primary per glyph.
  - Run X-6.9 invariant; fix any inconsistencies.
  - Commit "data: kanji whitelist (280 glyphs) [build-step 3/15]"

STEP 4: KANJI CATALOGUE  (~2-4 hr)
  - Author KnowledgeBank/kanji_n4.md per §14.2: glyph + on/kun + 2-5 example words + brief notes.
  - Run python tools/build_data.py.
  - Run integrity check; fix violations.
  - Commit "data: kanji catalogue [build-step 4/15]"

STEP 5: VOCABULARY CORPUS  (~6-12 hr)
  - Read feedback/n4-vocab-inventory*.md or fetch Tanos N4 CSV.
  - Author KnowledgeBank/vocabulary_n4.md grouped by 18 thematic sections per §13.2.
  - Apply per-WORD PoS rule (§13.1).
  - Run python tools/build_data.py + python tools/tag_vocab_pos.py.
  - Run integrity check (especially JA-31 vocab PoS parity).
  - Commit "data: vocab corpus (~1500 entries) [build-step 5/15]"

STEP 6: GRAMMAR CATALOGUE  (~8-16 hr)
  - Read feedback/n4-grammar-inventory.md or fetch Bunpro N4 + Tanos N4.
  - Decide tier per pattern per §12.3.
  - Author KnowledgeBank/grammar_n4.md per §12.1: 18 categories, ~210 patterns, 2-5 examples each, common-mistakes per pattern.
  - Run python tools/build_data.py.
  - Run python tools/link_grammar_examples_to_vocab.py.
  - Run integrity check; fix violations.
  - Commit "data: grammar catalogue (~210 patterns) [build-step 6/15]"

STEP 7: READING + LISTENING CORPORA  (~6-10 hr)
  - Author KnowledgeBank/dokkai_questions_n4.md — ~30 passages per §15.
  - Author KnowledgeBank/chokai_questions_n4.md — ~30 listening items per §16.
  - Run python tools/build_data.py.
  - Run python tools/build_audio.py (synthetic, mark voice='synthetic').
  - Run integrity check (especially JA-15 audio refs resolve).
  - Commit "data: reading + listening corpora [build-step 7/15]"

STEP 8: QUESTION BANKS  (~12-24 hr)
  - Author moji_questions_n4.md (~150 questions per Mondai 1/2/3).
  - Author goi_questions_n4.md (~150 questions per Mondai 4/5/6).
  - Author bunpou_questions_n4.md (~100 questions per Mondai 1/2/3).
  - dokkai_questions: passages + 2-3 questions each → ~70 questions.
  - Run python tools/build_data.py + python tools/build_papers.py.
  - Run python tools/scan_multi_correct.py — fix every flag (no multi-correct allowed).
  - Run python tools/heuristic_audit.py — apply auto-fixes.
  - Run integrity check (all 33 invariants).
  - Commit "data: question banks (~530 questions) [build-step 8/15]"

STEP 9: UI MODULES  (~2-4 hr)
  - For each js/ module in <source-repo>/js/: copy to <target>/js/.
  - Replace 'n5' → 'n4' in literals.
  - Replace 'jlpt-n5-tutor' → 'jlpt-n4-tutor' in cache keys + storage keys + manifest references.
  - Apply §3.2.9 mid-line-clip prophylactic to every tile-grid card description.
  - Apply §3.2.10 state-reset prophylactic to render modules with module-level view/session.
  - Apply §4.5 mobile UI contract.
  - Apply §4.6 disabled-button feedback contract.
  - Apply §10 / §22 / §23 specific N4 module wiring.
  - Commit "ui: port js + css modules with N4 spec applied [build-step 9/15]"

STEP 10: AUDIO PIPELINE  (~30 min)
  - Run python tools/build_audio.py for every grammar example, reading passage, listening item that doesn't have an audio file.
  - Confirm data/audio_manifest.json has every item from data/*.json.
  - Commit "audio: synthetic TTS pass [build-step 10/15]"

STEP 11: LLM AUDIT  (~1-2 hr; ~$10-15 API)
  - Run python tools/llm_audit.py over the question banks.
  - Apply HIGH/CRITICAL findings via auto-fixers if available; flag others in TASKS.md Pass-1.
  - Run integrity check.
  - Commit "audit: llm pass [build-step 11/15]"

STEP 12: COVERAGE COMPARISON  (~30 min)
  - Run python tools/coverage_compare.py against external N4 corpus (jlptsensei).
  - Note gaps in TASKS.md as Pass-2 follow-up.
  - Commit "audit: coverage gap analysis [build-step 12/15]"

STEP 13: BROWSER SMOKE TEST  (~10 min)
  - Run npm install + npx playwright test tests-e2e/p0-smoke.spec.js.
  - Verify: index.html loads, hash routes resolve, no console errors, SW registers, manifest valid.
  - Commit "test: smoke test pass [build-step 13/15]"

STEP 14: TASKS.md + MEMORY.md FINALISATION  (~30 min)
  - Populate TASKS.md status snapshot with corpus counts, SW version, route list.
  - Add Pass-1 section with all deferred items + their §39.2 default rationale.
  - Populate MEMORY.md ≤200 lines.
  - Commit "docs: TASKS + MEMORY populated [build-step 14/15]"

STEP 15: DEFINITION-OF-DONE FINAL CHECK + REPORT
  - Run §37 acceptance criteria checklist (20 items).
  - Generate handoff report per Appendix E.
  - If all GREEN: tag commit n4-v1.0.0.
  - Commit "release: N4 v1.0.0 ready [build-step 15/15]"
  - git push origin HEAD --tags.
  - Echo report to user / stdout.
```

### 39.4 Critical rules across all steps

| ID | Rule |
|---|---|
| EX-1 | **Idempotent.** Every step checks `.build-progress.json`. Re-running on partial state continues from next-incomplete step. |
| EX-2 | **Checkpointed.** Every step writes `.build-progress.json` and commits with `[build-step N/15]` tag. |
| EX-3 | **Halt-on-integrity.** Any integrity violation halts the build. Don't proceed. Don't silence. |
| EX-4 | **No silent skips.** Skipped steps log to stdout: `[skip] step N — already complete`. |
| EX-5 | **Use this spec as the single source of truth.** Don't ask follow-up questions unless a blocking contradiction exists. |
| EX-6 | **Build the complete N4 app in one implementation pass where feasible.** Total time estimate: 50-80 hours autonomous. |
| EX-7 | **If content cannot be completed, create complete architecture + clearly marked content placeholders, log in TASKS.md.** |
| EX-8 | **Reuse N5 architecture unless this spec explicitly says otherwise.** Replace all N5-specific user-facing content with N4. |
| EX-9 | **Run all validation and QA checks before final handoff.** §36 + §37. |
| EX-10 | **Generate the handoff report (Appendix E).** Either success or halt-state. |

### 39.5 Halt conditions

The agent halts ONLY in these cases:

1. Target directory non-empty (per §39.2).
2. No source N5 repo found at `<JLPT-root>/N5/`.
3. Skip-permissions flag not active.
4. Integrity violation that the agent cannot auto-fix.
5. Network unreachable AND inventory files missing (no jlptsensei + no Tanos + no `feedback/n4-*-inventory*.md`).

In every other case, complete §39.3 end-to-end.

---

## 40. Non-Negotiable Rules

These rules are **hard constraints**. Any violation blocks release.

| NN | Rule |
|---|---|
| NN-1 | No user-facing N5 label in the N4 app, except inside `[N5 Review]` prerequisite badges. |
| NN-2 | No N3+ content presented as `core_n4`. |
| NN-3 | No copyrighted past-paper questions or passages copied verbatim. |
| NN-4 | No free-text questions without deterministic grading rubric. |
| NN-5 | Submit cannot fire before all questions are answered. |
| NN-6 | Results cannot show before Submit. |
| NN-7 | No backend services. App is static-only. |
| NN-8 | GitHub Pages routing must work — no 404 on refresh. |
| NN-9 | No UI overflow at any width 320-1920. |
| NN-10 | No promotional copy on the homepage (HP-1). |
| NN-11 | No unnatural Japanese examples. (Q-10.) |
| NN-12 | No bypassing validation checks. CI integrity gate is hard fail. |
| NN-13 | No editing `data/*.json` directly when KB markdown is the source of truth. |
| NN-14 | No vague "copy from N5" instructions in this document. Where reuse is required, list exact files + transformations. (This rule applies to the SPECIFICATION; it has been satisfied.) |

---

## 41. Appendices

### Appendix A — Example JSON Objects (full samples)

#### A.1 Grammar entry (full sample)

```json
{
  "id": "n4-001",
  "pattern": "〜ように",
  "name": "yō ni",
  "meaning_en": "in order to / so that (indirect or non-volitional outcome)",
  "meaning_ja": "もくてき（かんせつてき・ひいしてき）を しめす",
  "category": "Conjunctions and sentence connectors",
  "tier": "core_n4",
  "prerequisite": ["n5-067"],
  "form_rules": {
    "attaches_to": ["verb-dictionary-form", "verb-nai-form"],
    "conjugations": [
      {"form": "purpose", "label": "in order to (positive outcome)", "example": "Verb-dict + ように"},
      {"form": "purpose-neg", "label": "so as not to (negative outcome)", "example": "Verb-nai + ように"}
    ]
  },
  "examples": [
    {
      "form": "purpose-neg",
      "ja": "わすれないように メモを とりました。",
      "translation_en": "I took notes so as not to forget.",
      "vocab_ids": ["n4.vocab.18-set-phrases.メモを とる"],
      "audio": "audio/n4-001.0.mp3"
    },
    {
      "form": "purpose",
      "ja": "あした はやく おきられるように 早く ねます。",
      "translation_en": "I'll go to bed early so I can get up early tomorrow.",
      "vocab_ids": [],
      "audio": "audio/n4-001.1.mp3"
    },
    {
      "form": "purpose",
      "ja": "子どもが わかるように やさしい ことばで せつめいしました。",
      "translation_en": "I explained in simple words so the child would understand.",
      "vocab_ids": [],
      "audio": "audio/n4-001.2.mp3"
    }
  ],
  "common_mistakes": [
    {
      "wrong": "勉強するために 早く ねます。",
      "right": "勉強できるように 早く ねます。",
      "why": "ために takes a verbal noun or volitional verb expressing the actor's intention. ように is for indirect or non-volitional outcomes (potential / non-actor / hope)."
    }
  ],
  "notes": "Compare with 〜ために (n4-002). ために emphasises purpose with the actor's volition; ように for indirect or non-volitional outcomes. With potential verbs (できる, わかる, 見える), use ように.",
  "related": ["n4-002"],
  "tags": ["purpose", "conjunction", "core"],
  "auto": false,
  "review_status": "llm_only"
}
```

#### A.2 Vocab entry (full sample)

```json
{
  "id": "n4.vocab.5-travel-and-transportation.乗り換える",
  "form": "乗り換える",
  "reading": "のりかえる",
  "gloss": "to change trains / transfer (between vehicles)",
  "section": "5. Travel and Transportation",
  "pos": "verb-2",
  "tier": "core_n4",
  "kanji_level": ["乗", "換"],
  "examples": [
    {
      "ja": "新宿で 山手線に 乗り換えてください。",
      "translation_en": "Please change to the Yamanote line at Shinjuku."
    }
  ],
  "notes": "Group 2 (ichidan) verb. Used with で marking the transfer location and に marking the new line/vehicle.",
  "auto": false,
  "review_status": "llm_only"
}
```

#### A.3 Kanji entry (full sample)

```json
{
  "id": "n4.kanji.乗",
  "glyph": "乗",
  "tier": "core_n4",
  "n5_prerequisite": false,
  "lesson_order": 107,
  "frequency_rank": 412,
  "on": ["ジョウ"],
  "kun": ["の(る)", "の(せる)"],
  "primary_reading": "ジョウ",
  "primary_kind": "on",
  "meanings": ["ride", "board", "get on (a vehicle)"],
  "stroke_order_svg": "svg/kanji/乗.svg",
  "recognition_priority": 1,
  "examples": [
    {"form": "乗る", "reading": "のる", "gloss": "to ride / board"},
    {"form": "乗り換える", "reading": "のりかえる", "gloss": "to change trains"},
    {"form": "乗車", "reading": "じょうしゃ", "gloss": "boarding (a train)"}
  ],
  "notes": "Common in transportation contexts. に乗る = to ride / board (X). Don't confuse with 上 (うえ, 'on top of')."
}
```

#### A.4 Reading passage (full sample)

```json
{
  "id": "n4.read.012",
  "title_ja": "図書館の おしらせ",
  "type": "notice",
  "format_type": "short",
  "level": "core_n4",
  "estimated_time_seconds": 90,
  "ja": "つぎの 月よう日（６月５日）から、新しい 開館時間が はじまります。\n月よう日から 金よう日：あさ 9時 〜 よる 9時\n土よう日・日よう日：あさ 10時 〜 ゆうがた 6時\n本の かりかたや 図書館の つかいかたは かわりません。\nよろしく おねがいします。",
  "kanji_in_passage": ["新", "開", "館", "時", "間", "月", "日", "金", "土", "本", "図", "書"],
  "vocabulary_support": [],
  "questions": [
    {
      "id": "n4.read.012.q1",
      "type": "mcq",
      "stem_ja": "おしらせの ないようは 何ですか。",
      "choices": [
        "A. としょかんが 新しく できます。",
        "B. としょかんの 開館時間が かわります。",
        "C. としょかんが しまります。",
        "D. 本を かりる 方法が かわります。"
      ],
      "correctAnswer": "B",
      "explanation_en": "The notice says the opening hours change starting June 5 — option B.",
      "weak_area_tags": ["reading-comprehension", "notice-format"],
      "distractor_explanations": {
        "A": "The library is not new; only the hours change.",
        "C": "The notice does not say the library is closing.",
        "D": "The notice explicitly says borrowing methods do NOT change."
      }
    }
  ],
  "audio": "audio/n4.read.012.mp3",
  "auto": false,
  "review_status": "llm_only"
}
```

#### A.5 Listening item (full sample)

```json
{
  "id": "n4.listen.014",
  "title_ja": "駅員と 旅行者の 会話",
  "format": "Mondai 1 (kadai-rikai)",
  "level": "core_n4",
  "estimated_time_seconds": 60,
  "setup_ja": "駅で、駅員と 旅行者が 話して います。旅行者は どの 電車に 乗りますか。",
  "script_ja": "[男]すみません、新宿に 行きたいんですが、どの 電車ですか。\n[女]新宿ですか。8番線の 山手線が べんりです。\n[男]あ、どうも。\n[女]あ、ちょっと まって ください。今は こうじちゅうですから、5番線の りんかい線の ほうが 早いですよ。\n[男]わかりました。ありがとうございます。",
  "audio": "audio/n4.listen.014.mp3",
  "voice": "synthetic",
  "transcript_reveal": "after_answer",
  "questions": [
    {
      "id": "n4.listen.014.q1",
      "type": "mcq",
      "stem_ja": "旅行者は どの 電車に 乗りますか。",
      "choices": [
        "A. 8番線の 山手線",
        "B. 5番線の りんかい線",
        "C. 8番線の りんかい線",
        "D. 5番線の 山手線"
      ],
      "correctAnswer": "B",
      "explanation_en": "The staff first suggests 8番線 山手線 but corrects to 5番線 りんかい線 because of construction. The traveller takes that route.",
      "weak_area_tags": ["listening-task", "transportation", "scene-correction"]
    }
  ],
  "auto": false,
  "review_status": "llm_only"
}
```

#### A.6 Question entry (full sample)

```json
{
  "id": "q-0123",
  "category": "bunpou",
  "subcategory": "Mondai 1",
  "grammarPatternId": "n4-001",
  "type": "mcq",
  "subtype": null,
  "direction": "Choose the best particle/word for the blank.",
  "prompt_ja": "つぎの ぶんを よんで しつもんに こたえなさい。",
  "question_ja": "わすれない（ ）　メモを とりました。",
  "choices": ["A. ように", "B. ために", "C. ても", "D. のに"],
  "correctAnswer": "A",
  "explanation_en": "ように for indirect / non-volitional outcomes (so as not to forget).",
  "distractor_explanations": {
    "B": "ために takes a verbal noun or volitional verb expressing the actor's intention; doesn't fit a non-volitional state like 'not forgetting'.",
    "C": "ても means 'even if'; doesn't fit a purpose meaning here.",
    "D": "のに expresses contrast / contradictory result; doesn't fit a purpose meaning."
  },
  "high_confusion": true,
  "difficulty": "core_n4",
  "auto": false
}
```

### Appendix B — N4 Content Count Targets

Final corpus targets (subject to ±10% variance based on cross-source authority data). Record actual counts in `_meta.entity_count` of each `data/*.json`.

| Content | Target | Acceptable range | Source authority |
|---|---|---|---|
| Grammar patterns | 210 | 190-230 | Bunpro N4 + Tanos N4 + Genki II + Minna II |
| Vocabulary entries | 1500 | 1400-1600 | Tanos N4 vocab CSV + JLPT-Sensei N4 |
| Kanji whitelist | 280 | 274-286 | JLPT-Sensei N4 kanji + Tanos N4 (106 N5 prerequisite + 174 N4 new) |
| Reading passages | 30 | 25-35 | Authored fresh; format follows JLPT.jp samples |
| Listening items | 30 | 25-35 | Authored fresh; format follows JLPT.jp samples |
| Moji questions | 150 | 130-170 | Authored fresh per §17 budget |
| Goi questions | 150 | 130-170 | – |
| Bunpou questions | 100 | 90-120 | – |
| Dokkai questions | 70 | 60-90 | Each passage 2-3 questions |
| Chokai questions | 60 | 50-80 | Each item 1-3 questions |
| **Total questions** | **530** | **460-600** | – |
| Mock-test papers | 32 | 28-36 | 15 questions each, sliced from question pool |
| MP3 files (synthetic v1) | ~600 | – | Grammar examples ~450, reading 30, listening 30, plus ~90 vocab/kanji example audio |

### Appendix C — CI / Validation Checklist

Run BEFORE every release. All MUST pass.

```
[ ] python tools/build_data.py             — exits 0
[ ] python tools/build_audio.py            — exits 0; data/audio_manifest.json updated
[ ] python tools/build_papers.py           — exits 0
[ ] python tools/link_grammar_examples_to_vocab.py  — 100% linkage
[ ] python tools/tag_vocab_pos.py          — 100% PoS coverage
[ ] python tools/check_content_integrity.py — all 33 invariants pass
[ ] python tools/test_build_data.py        — all regression tests pass
[ ] python tools/scan_multi_correct.py     — zero unresolved multi-correct
[ ] python tools/heuristic_audit.py        — zero CRITICAL/HIGH findings
[ ] python tools/audit_provenance.py       — no past-paper signatures (JA-30)
[ ] python tools/audit_audio_coverage.py   — every JSON audio ref has MP3
[ ] python tools/coverage_compare.py       — gap analysis logged in TASKS.md
[ ] npm test (Playwright)                  — all p0-smoke tests pass
[ ] npx lighthouse-ci                      — Perf ≥90 mobile / ≥95 desktop, A11y ≥95, PWA = 100
[ ] axe-core scan                          — zero serious/critical violations
[ ] tests-e2e/responsive.spec.js           — no horizontal overflow at 320-1920
[ ] tests-e2e/a11y.spec.js                 — keyboard / focus / contrast pass
[ ] grep -r "U+2014\|U+2013" .             — zero matches (X-6.5)
[ ] grep -r "see n4-" data/                — zero matches in user-facing fields (JA-10)
[ ] grep -r "JLPT N5\|N5" --include="*.html" --include="*.js" js/ index.html
                                           — zero matches except in [N5 Review] prerequisite badges
```

### Appendix D — TASKS.md Template

```markdown
# JLPT N4 Tutor — Tasks

Last updated: <DATE>

## Live site
- Repo: https://github.com/<org>/jlpt-n4-tutor
- Live URL: https://<org>.github.io/jlpt-n4-tutor/
- Engine tests: <X/Y> passing (`tests.html`)
- CI invariants: <Z/33> green

## Status snapshot
- v<X.Y.Z>
- SW version: jlpt-n4-tutor-v<N>
- Grammar: <N> patterns
- Vocab: <N> entries
- Kanji: <N> glyphs
- Reading: <N> passages
- Listening: <N> items
- Questions: <N> total (~<M>moji + <G>goi + <B>bunpou + <D>dokkai + <C>chokai)
- Mock-test papers: <N>
- Audio: <N> MP3s (synthetic)
- Locales: 5 (en/vi/id/ne/zh)
- Routes: <list>

## External-blocked backlog
- EB-1: Native-recorded listening audio (v2; gtts in v1)
- EB-2: Native-teacher review (v2; LLM-only in v1)
- EB-3: Translation of brief to Japanese (v2)
- EB-4: FSRS-4 SRS migration (v2; SM-2 in v1)

## Pass-1 (initial build, <DATE>)
- [x] Repo skeleton
- [x] CI wiring
- [x] Kanji whitelist
- [x] Kanji catalogue
- [x] Vocab corpus
- [x] Grammar catalogue
- [x] Reading + Listening corpora
- [x] Question banks
- [x] UI modules
- [x] Audio pipeline
- [x] LLM audit
- [x] Coverage comparison
- [x] Browser smoke test
- [x] Documentation
- [x] Definition of done

## Pass-2 (post-launch follow-up, target <DATE+90d>)
- [ ] Native-teacher review of grammar patterns
- [ ] Native-recorded listening audio
- [ ] Coverage gap fixes from Pass-1 §12
- [ ] FSRS-4 migration

## Known limitations
- Synthetic listening audio (gtts) — not native pacing
- LLM-only reviewer; no native sign-off
```

### Appendix E — Handoff Report Template

Generate at end of build (step 15).

#### E.1 Success report

```
N4 BUILD COMPLETE — v1.0.0
================================================================
Source:    N5 at <source-path>
Target:    N4 at <target-path>
Started:   <ISO datetime>
Finished:  <ISO datetime>
Duration:  <hours>h <minutes>m
Commits:   <count>  (HEAD: <SHA short>)
Tag:       n4-v1.0.0

DEFINITION-OF-DONE (§37)
[x] item 1: All 13 functional modules exist
[x] item 2: All N4 datasets load
[x] item 3: Homepage shows N4 syllabus dashboard per §10
[x] item 4: Tests auto-score
[x] item 5: Submit rule works (disabled until all answered)
[x] item 6: Results display immediately, no reload
[x] item 7: Weak areas generate correctly
[x] item 8: Progress persists across reload
[x] item 9: Search works
[x] item 10: GitHub Pages deployment works
[x] item 11: No N5 labels remain
[x] item 12: Japanese content passes quality review
[x] item 13: All 33 CI invariants pass
[x] item 14: All Playwright smoke tests pass
[x] item 15: Lighthouse PWA=100, Perf≥90, A11y≥95
[x] item 16: Responsive 320-1920 with no overflow
[x] item 17: A11y zero serious/critical violations
[x] item 18: Em-dash-free
[x] item 19: TASKS.md current
[x] item 20: CHANGELOG v1.0.0 entry

CORPUS COUNTS
  Grammar patterns:   <n>  (target ~210)
  Vocab entries:      <n>  (target ~1500)
  Kanji glyphs:       <n>  (target 280 = 106 N5 + 174 N4)
  Reading passages:   <n>  (target ~30)
  Listening items:    <n>  (target ~30)
  Questions total:    <n>  (target ~530)
  Mock-test papers:   <n>  (target ~32)
  Audio MP3s:         <n>  (target ~600 synthetic)

DEFAULTS APPLIED
  Native voice:        synthetic (gtts) — flagged Pass-2 EB-1
  Native review:       LLM-only — flagged Pass-2 EB-2
  Translation:         English-only — flagged Pass-2 EB-3
  Monetisation:        free, no telemetry
  SRS algorithm:       SM-2 (FSRS-4 deferred to v2)

DEFERRED TO PASS-2
  - Native-recorded listening audio (24+ items)
  - Native-teacher review of grammar patterns
  - Coverage gap fixes (see TASKS.md Pass-2)
  - FSRS-4 SRS migration

KNOWN LIMITATIONS
  - <list any items not GREEN>
  - <list any layer-3+ shortfalls per §A.4 MVS>

NEXT STEPS FOR HUMAN
  1. Manual native review of grammar patterns (Pass-2)
  2. Recruit native voice talent for listening re-record
  3. <other ranked TODOs>
================================================================
```

#### E.2 Halt-state report

```
N4 BUILD HALTED — RESUME AFTER FIX
================================================================
Last completed step:    <step-number>/15
Halt reason:            <one-line explanation>
What needs to happen:   <one or two specific fixes the human must do>
How to resume:          <exact command to re-trigger the build>
================================================================
```

---

*End of N4 Specification.*

*Prepared 2026-05-04 by distilling and locking the level-agnostic playbook at `procedure-manual-build-next-jlpt-level.md`. Use this document as the single source of truth for the JLPT N4 Tutor build. The level-agnostic playbook remains the source for future N3, N2, N1 builds.*

*Document versioning: this file uses semantic versioning (v1.0.0). Every revision appends a dated line below. Major version bump (v2.0.0) when the N4 build target completes; minor when a new section is added; patch when wording is clarified.*

*Trailer:*
- *v1.0.0 (2026-05-04): Initial N4 specification distilled from level-agnostic playbook.*
