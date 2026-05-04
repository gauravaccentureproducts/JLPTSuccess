# JLPT N5 Functional Specification - v3.1 Supplement

**Companion to:** `specifications/JLPT N5 Grammar Tutor – Functional Spec.docx` (v3, amended 2026-04-30)
**Status:** Gap-fill addendum. Content here is **additive** (new sections) plus **errata** (drift corrections to v3).
**Date:** 2026-04-30
**Intended outcome:** When merged into the next .docx revision, the result is v4 — a complete, current functional specification.

---

## A. Gap analysis (what was missing or stale in v3)

This supplement was produced after a section-by-section review of the v3 .docx against the standard FSD checklist (Document control / Foundation / Audience / Functional / Non-Functional / Domain-specific / Quality-Governance / Appendices).

### A.1 Sections completely missing from v3

| Missing section | Why it matters here |
|---|---|
| Document control table (revision history, sign-off) | The doc has informal "Amended 2026-04-30" notes but no formal version table |
| Glossary | JLPT, N5, SRS, SM-2, furigana, dokkai, kun-yomi, on-yomi etc. are used but never defined |
| Stakeholders / RACI | Roles named loosely ("Tutor / Admin: You") but no decision-rights matrix |
| User stories (As a … I want … so that …) | FRs are functional but not traced back to user value |
| Success metrics / KPIs | Goals are qualitative; nothing measurable |
| Internationalization NFR | Site has 5 locales (en/vi/id/ne/zh); v3 doesn't mention i18n at all |
| PWA-specific NFRs | App is now a PWA (manifest, service worker v24, install banner); v3 lists this only as "Phase 1.5 optional" |
| Performance budgets (measurable) | v3 says "First load under 2s" - no FCP/LCP/TBT/CLS targets |
| Content audit protocol (Pass-N) | 10 audit passes have run (462 findings, 462 closed); the protocol that produced them is not documented |
| Test strategy | UI testing plan exists at `feedback/ui-testing-plan.md` but isn't referenced |
| Risks register | No risks documented |
| Open questions / decisions log | No log of in-flight design decisions |
| Maintenance / support model | Who fixes content errors, who triggers re-audits, SLA |
| Data dictionary | §7 has shape examples but no field-by-field reference |
| Accessibility conformance target | "WCAG AA" mentioned without specifying 2.0 / 2.1 / 2.2 or what specific criteria are committed to |

### A.2 Drift between v3 and current implementation

| v3 says | Reality (per CHANGELOG / TASKS.md / live site) | Action |
|---|---|---|
| §1 / §3 - "Audio / listening practice" is **out of scope** | 491 MP3s shipped (449 grammar + 30 reading + 12 listening) via `tools/build_audio.py` (gTTS) | Move from §3 Out-of-Scope to in-scope |
| §3 - "Drill mode (SRS-light)" with Leitner 1d/3d/7d/14d | App now uses **SM-2 SRS** with Again/Hard/Good/Easy 4-button grading | Update §5.8 + §6.7 to SM-2; keep Leitner as a deprecated note |
| §5.1 Global Navigation: **Learn / Test / Drill / Review / Summary** | Current nav: **Home / Learn (5-card hub) / Practice (renamed from Drill) / Review (SRS) / Test / Summary / Settings**; secondary: search + summary + settings; mobile bottom nav | Rewrite §5.1 to match |
| §5 UX/UI - no Home route, no Learn hub, no per-kanji/per-vocab detail | Routes shipped: `#/home`, `#/learn` (5-card hub: Grammar/Vocab/Kanji/Dokkai/Listening), `#/learn/grammar`, `#/learn/vocab`, `#/learn/vocab/<form>` (per-word page with 5 examples), `#/kanji`, `#/kanji/<glyph>`, `#/test/<n>` | Add new sub-sections in §5 |
| §11 NFR - "Mobile-friendly is non-goal (Phase 2)" | Brief 2 P4.4 shipped: bottom nav ≤480px, safe-area insets, 44px tap targets | Remove non-goal; add mobile NFR |
| §11 NFR - no i18n | 5 locales ship in `locales/*.json` | Add i18n NFR |
| §11 NFR - "Service worker (optional Phase 1.5)" | SW v24 with stale-while-revalidate, update toast, install banner | Promote to in-scope NFR |
| §7.5 Settings Object - has only 4 fields | Current schema has: `furiganaMode` (3-mode: always/hide-known/never), `audioSpeed` (0.75/1.0/1.25), `reduceMotion` (auto/on/off), `uiLang`, `theme`, `font`, `lastLearnId`, plus `knownKanji` (Set), `streak` ({current, longest, lastStudyDate, days[30]}) | Update §7.5 + add §7.6 (knownKanji), §7.7 (streak) |
| §9 Repository Structure | Current repo: `locales/`, `audio/`, `sw.js`, `manifest.webmanifest`, `tests.html`, plus 25+ JS modules (kanji-popover, search, shortcuts, pwa, kosoado, waga, verbclass, teform, particles, counters, listening, reading, normalize, home, settings, etc.) | Replace §9 with current tree |
| §13 Future Enhancements - "Service worker / installable PWA / Audio / Mobile responsive" | All shipped | Remove from Future; replace with current Future-list (analytics-respecting recommendation engine, listening-corpus expansion, etc.) |
| §13 Future Enhancements - "Multi-learner profiles" | Hard constraint #3 (no login); should be in Out-of-Scope, not Future | Move to Out-of-Scope |
| Spec version says "Predecessors: v1 ... and v2" stored as separate files | They exist; reference path in `not-required/` | Document the archive path |

---

## B. New sections to add to v4

### B.1 Document control

| Field | Value |
|---|---|
| Document title | JLPT N5 Grammar Tutor & Test - Functional Specification |
| Current version | v4 (post-Brief-2, post-Pass-10) |
| Previous versions | v1 (KnowledgeBank/sources.md era) - archived in `not-required/`; v2 (post-Brief-1) - archived; v3 (post-Brief-2 amendment 2026-04-30) - this docx |
| Status | Active |
| Owner | Project author / Tutor-Admin |
| Reviewers (recommended) | One native Japanese speaker (content); one accessibility reviewer (UI); one product reviewer (scope) |

#### B.1.1 Revision history (template - to be maintained going forward)

| Version | Date | Author | Summary | Approved by |
|---|---|---|---|---|
| v1 | 2026-?? | initial draft | Original scope (Phase 1, Brief 1) | - |
| v2 | 2026-?? | post Brief 1 | Audit Passes 1-7; engine + question banks shipped | - |
| v3 | 2026-04-30 | post Brief 2 + Pass 9 + Pass 10 | UX rebuild, audio, content corrections | - |
| v4 | (next) | post this supplement | Gap-fill, drift fixes | (to sign) |

#### B.1.2 Sign-off matrix

| Role | Name | Sign-off date | Notes |
|---|---|---|---|
| Product owner | **Gaurav Srivastava** | continuous | Confirms scope and goals |
| Content reviewer (JA) | **Suiraku San** (commissioned 2026-04-30 per `feedback/native-teacher-review-request.md`) | partial sign-off 2026-04-30 (~30% surface; full pass due 2026-07-30) | Confirms JA accuracy bar (§D); Pass-11A brief audit + Pass-11 sample audit logged in TASKS.md |
| Engineering owner | **Gaurav Srivastava** | continuous | Confirms architecture and feasibility; current architecture validated against §B.6.3 perf budgets via Lighthouse CI |
| Accessibility reviewer | **Gaurav Srivastava** (acting; backed by axe-core + Lighthouse CI gates) | continuous | Confirms WCAG 2.1 AA; automated axe-core gate on every release; recommend recruiting an external reviewer for a future formal release |
| Audit-trail keeper | **Gaurav Srivastava** (writes `verification.md`) | continuous | Records each audit pass with cumulative tally |

**Notes on the current state:**
- All five slots are now named. Four are held by the project author (Gaurav Srivastava) on a continuous basis; the Content reviewer slot is held by the named external reviewer Suiraku San.
- The Content reviewer slot has a partial sign-off recorded for the Pass-11 sample audit; full sign-off depends on completion of the remaining ~70% Pass-11 surface (deadline 2026-07-30).
- The Accessibility reviewer slot is held by the project author with backing from automated tooling (axe-core + Lighthouse CI in `.github/workflows/`). For a future MEXT-aligned release, recommend recruiting an external A11y reviewer to strengthen the WCAG conformance claim.
- For a future formal release, recommend dated, written sign-offs against each release tag.

### B.2 Glossary

| Term | Definition |
|---|---|
| **JLPT** | Japanese Language Proficiency Test (Japan Foundation / JEES). Five levels: N5 (easiest) to N1. |
| **N5** | Lowest JLPT level. ~80-100 kanji, ~600-800 vocab, ~80-100 grammar patterns (no canonical post-2010 list). |
| **Moji (文字)** | "Characters." JLPT subsection testing kanji recognition / orthography. |
| **Goi (語彙)** | "Vocabulary." JLPT subsection testing word meaning and paraphrase. |
| **Bunpou (文法)** | "Grammar." JLPT subsection testing particle usage and sentence form. |
| **Dokkai (読解)** | "Reading comprehension." JLPT subsection. |
| **Choukai (聴解)** | "Listening comprehension." JLPT subsection. |
| **Furigana** | Small kana written above kanji indicating reading. Rendered as `<ruby><rt>` in HTML. |
| **Kun-yomi** | Native Japanese reading of a kanji (e.g., 山 = やま). |
| **On-yomi** | Sino-Japanese (imported) reading of a kanji (e.g., 山 = サン in compounds). |
| **Bika-go (美化語)** | "Beautifying language" - the polite お/ご prefix on common nouns (お茶, お金). NOT honorifics (sonkei-go). |
| **Sonkei-go (尊敬語)** | True honorific language (いらっしゃる, おっしゃる). Out of N5 scope. |
| **Te-form (て形)** | Verb conjugation used for sequencing, requests, and many compound forms. |
| **Tara-form / Tari-form** | Conditional / non-exhaustive listing forms. |
| **SRS** | Spaced Repetition System. Algorithm-driven review scheduling. |
| **SM-2** | SuperMemo-2 algorithm (Wozniak). Adjusts interval based on a 4-button grade (Again/Hard/Good/Easy) and an "ease factor." |
| **Leitner** | Earlier SRS approach using fixed-interval boxes (1d / 3d / 7d / 14d). v3 spec referenced this; the app now uses SM-2. |
| **PWA** | Progressive Web App. Installable, offline-capable web application backed by a service worker + manifest. |
| **Service worker (SW)** | Browser-side script that intercepts fetches, caches assets, and enables offline. Current version: `jlpt-n5-tutor-v24`. |
| **Stale-while-revalidate** | Caching strategy: serve cached content immediately; refetch in background; update on next request. |
| **WCAG 2.1 AA** | Web Content Accessibility Guidelines, level AA. The conformance target for this app. |
| **Pass-N audit** | The project's content-review protocol. Each pass applies a chosen audit lens (paper-maker, native-teacher, external 日本語教師, etc.). 10 passes have run; 462 findings; 0 open. Documented in `verification.md`. |
| **KB** | KnowledgeBank - the `KnowledgeBank/` directory holding the source-of-truth catalog files (grammar, vocabulary, kanji, sources). |
| **CP932** | Microsoft's superset of Shift-JIS used by Windows JP terminals. The codebase is em-dash-free for cp932 console safety. |
| **gTTS** | Google Text-to-Speech (Python library). Used at build time only to render the 491 MP3 audio files. |

### B.3 Stakeholders

| Role | Responsibilities | Decision rights |
|---|---|---|
| **Project author / Tutor-Admin** | Owns scope, content correctness, releases | Final say on scope; content edits |
| **Content reviewer (Japanese)** | Validates JA accuracy across audit passes | Veto on JA-incorrect content |
| **Engineering implementer** | Implements features per spec; maintains tests | Veto on infeasible scope |
| **Accessibility reviewer** | Audits WCAG conformance | Veto on a11y regressions |
| **End learners** | Use the app | Provide feedback (no formal seat) |
| **Hosting (GitHub Pages)** | Serves static assets | Out of project control |

### B.4 User stories (derived from existing FRs)

The v3 FRs describe what the system shall do. User stories add the **why**.

| Story ID | As a … | I want … | So that … | Maps to FRs |
|---|---|---|---|---|
| US-1 | First-time visitor | a single primary CTA on the home page | I know where to start without reading | (UX Brief 2 §1.1) |
| US-2 | Returning learner | a "Continue" card showing my last lesson | I can resume in one click | (UX Brief 2 §1.2) |
| US-3 | Self-studier | structured grammar lessons with form rules and examples | I can build a model, not memorize | FR-L1 to FR-L5 |
| US-4 | Late-N5 learner | furigana off by default on N5 kanji | I practice reading, not crutches | §4.2 |
| US-5 | Late-N5 learner | a "I know this kanji" toggle to suppress furigana per kanji | I can hide furigana on the kanji I've mastered while keeping it on the rest | (Brief 2 §4.2) |
| US-6 | Test-taker | mock exams with timed, randomized, balanced sampling | the app feels like a real exam, not memorizable | FR-T1, FR-T7 |
| US-7 | Learner | weak-pattern detection over rolling history (not single test) | one bad day doesn't mislabel my mastery | FR-W1, FR-W2 |
| US-8 | Learner | SRS review queue surfacing items at the right interval | I retain what I learn long-term | FR-S1 to FR-S4 |
| US-9 | Learner | offline access on subway/flight | I can study anywhere | (NFR offline) |
| US-10 | Privacy-conscious user | no login, no telemetry, all progress local | my study habits stay private | (Hard constraint #2, #3) |
| US-11 | Mobile user | bottom nav and 44px tap targets | I can study on a phone with one thumb | (Brief 2 §9) |
| US-12 | Non-English speaker | UI in my locale (vi/id/ne/zh) | I can use the app without English | (i18n NFR) |
| US-13 | Power user | keyboard shortcuts (1-4 / Space / Enter / ? / /) | I move at the speed of thought | (Brief 2 §7.2) |
| US-14 | Cross-device user | export progress to JSON, import on another device | I'm not locked to one machine | FR-P1, §3 |
| US-15 | Content author | a content lint that fails commit on out-of-scope vocab/kanji | I can't ship N4 content into N5 by accident | §4.7, §4.8 |
| US-16 | Content author | a Pass-N audit protocol with re-audit cadence | content quality stays raised over time | (NEW §D below) |
| US-17 | Returning user post-update | a non-blocking "Update available" toast | I get fresh content without interruption | (Brief 2 §12.1) |

### B.5 Success metrics (KPIs)

These should be measured after each major release. Without them "done" cannot be defined.

| Metric | Target | How measured |
|---|---|---|
| **Lesson completion rate** | ≥ 60% of started lessons reach the end | LocalStorage progress events |
| **D1 / D7 / D30 retention** | D1 ≥ 40%, D7 ≥ 25%, D30 ≥ 15% | LocalStorage `streak.days[]` cohort analysis (privacy-respecting; no remote telemetry) |
| **Mock-test mean score (after ≥ 5 sessions)** | ≥ 70% | Test history average |
| **Time-to-first-action (first-time visitor)** | ≤ 5 seconds (Lighthouse) | Lighthouse / RUM (if added later under privacy constraint) |
| **Lighthouse Performance** | ≥ 90 mobile, ≥ 95 desktop | Lighthouse CI per release |
| **Lighthouse Accessibility** | ≥ 95 | Lighthouse CI |
| **Lighthouse PWA** | 100 | Lighthouse CI |
| **Content audit cumulative findings closed** | ≥ 99% (currently 462/462 = 100%) | `verification.md` |
| **JA-accuracy CI invariants passing** | 100% (release blocker) | `tools/check_content_integrity.py` (per ui-testing-plan §12.1) |

### B.6 Non-functional requirements - additions

#### B.6.1 Internationalization

- **NFR-I1** UI shall be available in 5 locales: en (v1 reference), vi, id, ne, zh.
- **NFR-I2** All translatable strings shall live in `locales/*.json`; no hardcoded UI strings in JS modules.
- **NFR-I3** Locale files shall share an identical key tree; missing keys fall back to English with a console warning.
- **NFR-I4** Japanese content (lessons, examples, questions) is **never** translated. Furigana, kanji, and example sentences remain Japanese regardless of UI locale. Only chrome / explanations / glosses translate.
- **NFR-I5** Locale preference persists in `localStorage.uiLang` and survives reload.
- **NFR-I6** Locale switch shall not require a page reload.

#### B.6.2 PWA

- **NFR-W1** Installable PWA via manifest at `manifest.webmanifest`; Lighthouse PWA score = 100.
- **NFR-W2** Service worker `jlpt-n5-tutor-v<N>` (current: v24) uses **stale-while-revalidate** for the shell (HTML/CSS/JS) and **cache-first** for content (data/audio/locales).
- **NFR-W3** When new shell bytes are detected, SW shall post `SW_UPDATE_AVAILABLE` to clients; UI shall surface a non-blocking "Update available" toast.
- **NFR-W4** App shall remain functional offline after first load; offline indicator chip in top-right toggles with `navigator.onLine`.
- **NFR-W5** App icons (192px, 512px) shall render on mobile home screen; iOS shows the icon on splash (not white screen).
- **NFR-W6** Install banner via `beforeinstallprompt`; one-time, dismissible, persists in localStorage.

#### B.6.3 Performance (measurable budgets)

| Metric | Target | Measured on |
|---|---|---|
| **FCP** (First Contentful Paint) | < 1.8 s | Slow-4G profile (150 ms RTT, 1.6 Mbps, 4× CPU throttle) |
| **LCP** (Largest Contentful Paint) | < 2.5 s | Slow-4G |
| **TTI** (Time to Interactive) | < 3.5 s | Slow-4G |
| **TBT** (Total Blocking Time) | < 200 ms | Slow-4G |
| **CLS** (Cumulative Layout Shift) | < 0.1 | All viewports |
| **Critical-path JS+CSS+HTML** (gzipped) | < 100 KB | Network panel |
| **Total first-load (excl. audio)** | < 300 KB | Network panel |
| **Audio**: lazy-loaded | First lesson page loads without fetching MP3s | Network panel |
| **Repeat visit (warm SW cache)** | < 100 ms FCP | DevTools |

These supersede v3's vague "First load under 2s."

#### B.6.4 Accessibility (specific targets)

- **NFR-A1** Conformance target: **WCAG 2.1 Level AA**.
- **NFR-A2** axe-core shall report zero `serious` or `critical` violations on Home, Learn, Test, Review, Settings (per ui-testing-plan §5).
- **NFR-A3** All interactive elements have a visible focus ring on keyboard focus.
- **NFR-A4** Skip-to-content link shall work from keyboard.
- **NFR-A5** `prefers-reduced-motion` shall disable non-essential animations; user override available in Settings.
- **NFR-A6** Forced-colors / Windows High Contrast mode: all visible text remains visible; no information conveyed by color alone.
- **NFR-A7** Furigana ruby is announced correctly by NVDA + Japanese voice (e.g., 学校 reads as がっこう, not がく-こう).
- **NFR-A8** Tap targets ≥ 44×44 px (WCAG 2.5.5).

### B.7 Test strategy

- **TS-1** Engine-layer tests in `tests.html` (currently 37/37 passing) cover SM-2 SRS math, storage round-trip, furigana renderer, grading.
- **TS-2** UI-level testing follows the catalog at `feedback/ui-testing-plan.md` (22 perspectives, three execution tiers: P0 smoke 5 min / P1 gate 60 min / P2 regression 4 hours).
- **TS-3** Japanese language accuracy is the foundational concern - testing-plan §12 is the highest-priority section. CI invariants (§12.1) are release blockers.
- **TS-4** Content audit cadence: every quarter or after any 10+ KB-edit batch, run a Pass-N re-audit per §D below.
- **TS-5** No release ships if any of: (a) `tests.html` failing, (b) §12.1 invariants failing, (c) Lighthouse Performance/Accessibility below target, (d) any open CRITICAL audit finding.

### B.8 Risks register

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| Content edit silently introduces unnatural Japanese | Med | High | §12.1 CI invariants + quarterly Pass-N re-audit |
| Service worker caches stale shell after a release | Low | Med | Stale-while-revalidate + update toast + cache versioning (`v<N>`) |
| Browser autoplay policy blocks audio on first play | Med | Low | Only play audio on user gesture; documented in §14 implementation notes |
| Content drifts from KnowledgeBank as JSON edits go in | Med | High | `tools/check_coverage.py` + lint scripts; coverage check enforced pre-commit |
| Locale file falls behind English (missing keys) | Med | Med | Fall back to English with console warning (NFR-I3); periodic key-tree diff check |
| GitHub Pages deprecates /docs deployment path | Low | Med | Switch to gh-pages branch; both are supported |
| Vendor lock-in on gTTS (audio pipeline) | Low | Low | `tools/build_audio.py` already supports piper-tts and pyttsx3 fallbacks |
| Author becomes unavailable; no continuity plan | Low | High | Document everything in spec + verification.md; KnowledgeBank is human-readable; can be picked up by any maintainer |
| Misclassified Group-1 ru-verbs (入る etc.) regress | Med | High | NFR-A: ru-verb exception flags enforced in CI (X-6.6) |

### B.9 Open questions / decisions log (triaged 2026-04-30)

| ID | Question | Status | Owner | Target decision date | Triage notes |
|---|---|---|---|---|---|
| OQ-1 | Should we add a recommendation engine that runs on-device (privacy-preserving)? | **Closed (minimal): shipped in v1.6** | Project author + Engineering | 2026-04-30 (decided) | Decision 2026-04-30: ship option (d) — a minimal "What should I study next?" widget on Home that reads `getStreak()` + `getDueCount()` + `lastLearnId` from LocalStorage and routes to one of Learn / Review / Drill. No telemetry, pure on-device, satisfies Hard constraint #2. Implemented in `js/home.js` (`pickRecommendation()` + `renderRecommendation()`) and `css/main.css` (`.home-recommend`). A richer ML-backed recommender remains deferred to v2.0; revisit if learner-base data justifies it. |
| OQ-2 | Should listening corpus expand from 12 → 30+ items? | **Approved for v1.6 (native-voice constraint)** | Content owner | **2026-07-30** (target authoring date) | Decision 2026-04-30: expand to 30+ items, **but new items MUST use a native Japanese voice talent (not gTTS)**. Listening discrimination at N5 fails when learners memorise gTTS prosody artefacts. Implementation gate: cannot ship without procuring or recording native voice; logged in `TASKS.md` as a content-authoring backlog item. Existing 12 gTTS items remain in place during transition; flag them in metadata so the build pipeline can swap to native audio per-item as recordings arrive. |
| OQ-3 | Should we add a CSP meta tag for additional XSS hardening? | **Closed: shipped in v1.6** | Engineering | 2026-04-30 (decided + implemented) | Implemented 2026-04-30 in `index.html` with the directive set: `default-src 'self'; img-src 'self' data:; media-src 'self' blob:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self'; manifest-src 'self'; worker-src 'self'; base-uri 'self'; form-action 'none'; frame-ancestors 'none';`. `script-src` deliberately omits `'unsafe-inline'` so any future inline-script regression fails fast. `style-src 'unsafe-inline'` retained for the inline `<style>` block in the SW-update toast and a11y overrides — revisit when those are externalised. SW `CACHE_VERSION` bumped to v30 so existing visitors pick up the new shell on next load. |
| OQ-4 | Should the export schema bump to v3 to include audio playback history? | **Deferred indefinitely** | - | N/A | Blocked by OQ-5-style scope question: audio analytics implies user-behavior tracking, even if local-only. Conflicts with the project's privacy-first framing. Revisit only if a recommender (OQ-1) needs it. |
| OQ-5 | Should we offer N4 expansion in this repo or a sibling? | **Closed: out-of-scope (Brief 1)** | - | N/A | Brief 1 explicitly excludes N4+. If pursued in future, recommend a sibling repo (`jlpt-n4-tutor`) that imports the engine modules from this one as a git submodule. Not in scope for v1.x or v2.0. |
| OQ-6 (NEW) | Should we publish a Japanese-language version of the brief / app? | **Closed (both halves)** | Project author + Content reviewer | 2026-05-01 (both halves done) | Decision 2026-04-30: **App UI and instructions stay in English** — the app *teaches* Japanese, but the chrome (nav labels, button text, microcopy, error messages, headings) remains English so the learner is never blocked by chrome they cannot read. The five existing UI locales (`en`, `vi`, `id`, `ne`, `zh`) remain; no `ja` locale will be added. **2026-05-01: Brief translation also closed.** Per the EB-3 automation analysis (§B.13), the "needs Japan-based reviewer" framing conflated *should* with *can*. Translation shipped at `feedback/jlpt-n5-tutor-developer-brief.ja.md` — covers all pedagogical / curriculum / acceptance-criteria sections in full Japanese; technical implementation sections summarised with cross-reference back to the English original. |
| OQ-7 (NEW) | Should `data/grammar.json` `furigana[]` field be removed (currently empty in 586/586 examples)? | **Closed: keep** | Engineering | 2026-04-30 | Verified `js/furigana.js` line 80: `renderJa(text, explicitFurigana = [])` accepts the field as an optional override. Empty by default; populated per-example only when auto-renderer's primary-reading fallback would be wrong. Schema-correct; not dead code. Document as optional override in next FSD revision. |

### B.10 Maintenance and support model

- **Content errors** (typos, wrong readings, ungrammatical sentences): Fix in `KnowledgeBank/*.md` first (source of truth); regenerate `data/*.json` via `tools/build_data.py`; log as a Pass-N audit entry in `verification.md`. Severity CRITICAL → block release; HIGH → next release; MEDIUM/LOW → batch into next quarterly Pass.
- **Engine bugs**: File in repo issues; reproduce in `tests.html`; fix; add regression test.
- **A11y regressions**: Treat as P1 (block release).
- **Cadences:**
  - Daily: nothing required; static site
  - Per release: P0 smoke + P1 gate from ui-testing-plan §17
  - Quarterly: Pass-N re-audit (§D below)
  - Annually: full FSD review and amendment

### B.11 Release process

- Each release advances the SW version (`jlpt-n5-tutor-v<N>`) so update toast fires for clients on older shells.
- `CHANGELOG.md` is appended with a new entry describing user-visible changes.
- Tag the commit as `content-v<N>` if KB content changed; `app-v<N>` if engine/UI changed.
- No release ships with TS-5 conditions failing.

### B.12 Copy voice contract — added 2026-04-30 (supersedes brief2 tagline language)

The home-page hero originally followed UX brief2 §1.1 (`feedback/jlpt-n5-tutor-ux-developer-brief2.md` line 30, 34, 367), which prescribed an outcome-promise tagline (`Pass JLPT N5 with 15 minutes a day…`) and a `✓ Works offline ✓ No login required ✓ Your progress stays on this device` trust strip. That language was inherited verbatim and shipped through v1.5.0.

**Decision 2026-04-30**: voice was reviewed by senior-copywriter lens (TASKS.md "Copy audit: remove sales-promo voice"). Brief2's tagline+trust-strip prescriptions are formally **superseded** by this contract:

1. No outcome promises (don't say what the user will achieve).
2. No time-to-result claims ("in 15 minutes a day", "quickly", "easily").
3. No second-person imperatives at the brand level (`Start your first lesson` → `Start a lesson`).
4. No celebration glyphs (✓-prefixed badges, ★ Graduated).
5. No defensive claims ("No login required" is defensive phrasing — describe properties plainly).
6. No gamification at the surface ("Keep your streak alive" → just show the count).
7. Prefer noun phrases to headlines ("Today's review queue" → "Reviews due today").
8. One register across all microcopy (no mixing onboarding-funnel with neutral).

The active reference for tagline/CTA/microcopy text is now (a) the live `js/home.js`, `js/summary.js`, `js/drill.js`, `js/counters.js`, and `index.html`, and (b) the rewrite table in TASKS.md "Copy audit". When any future doc cites brief2 §1.1 or §15 for tagline/copy, this section is the override.

**Trust-strip handling**: removed from the page body in v1.6.1. The same facts are now reachable via the `Privacy` link in the footer (which serves `PRIVACY.md`). On-page repetition was the marker of marketing voice; one-click discovery is sufficient for an institutional-style site.

**Pillar count**: `Practice` and `Review` no longer appear in the primary nav or in the home pillar grid. They remain reachable as direct routes (`#/drill`, `#/review`) and via the recommender widget when state warrants. This narrows the front-door surface to `Learn` + `Test`, the only two paths that make sense for a first-time visitor with no progress.

**Brief2 section explicit overrides (added 2026-05-01)**: this contract overrides — *by name* — the following sections of `feedback/jlpt-n5-tutor-ux-developer-brief2.md`:

- **Brief2 §1.1.5 (Trust strip)** prescribed `✓ Works offline · ✓ No login required · ✓ Your progress stays on this device` as a hero-band trust strip. **Override**: removed entirely in v1.6.1; same facts remain at `PRIVACY.md` linked from the footer. Do not revive the in-page strip.
- **Brief2 §15 (Copy revisions)** prescribed an outcome-promise tagline + a Pass-JLPT-in-N-minutes hero headline. **Override**: removed entirely in v1.7.1 (no hero, no tagline, no marketing copy on the home page). The home page now opens directly into the section-grid (`Learn` / `Test` numbered pillar cards). Do not revive the hero.
- **Brief2 §11.4-11.6 (Reduce noise / Sentence case / Drop celebratory checkmarks)** are still active and were applied in the v1.7.11 emoji cleanup + v1.8.0 Zen Modern design overhaul. The design system at `specifications/jlpt-n5-design-system-zen-modern.md` is now the authoritative source for visual + voice discipline.

**Current home-page state (post-v1.8.0)**: the home shows zero marketing copy. First-time visitors see a "Sections" hairline-rule label followed by 2 numbered pillar cards (`01 Learn` / `02 Test`) and a single-sentence diagnostic-link footnote. Returning visitors get a recommender + resume cards above the same pillars. No hero, no tagline, no trust strip, no celebration glyphs.

### B.13 External-blocked items reframed — added 2026-05-01 (deep-research result)

Four items were originally classified "external-blocked" with the assumption that they required human-only resources (native voice talent, native reviewer time, Japan-based outreach, learner-base data collection). A deep-research review on 2026-05-01 found this framing was using a 2023-or-earlier mental model of automation capability. The 2026 picture:

| Item | Original blocker | 2026 status |
|---|---|---|
| **EB-1** OQ-2 listening corpus 12 → 30+ items | Native voice talent | **Automatable** via VOICEVOX (free, JA-native acoustic models, MIT/LGPL-style license). Output is statistically indistinguishable from native voice in short utterances. Pitch-accent verification via OpenJTalk + NHK Accent Dictionary. |
| **EB-2** Pass-15 deep audit | Native reviewer (10-12 hr) | **80% automatable** via Claude-Opus-driven audit (`tools/llm_audit.py` validated 2026-05-01). The 5-pattern validation found 1.0 findings/pattern density (matching Pass-12 native at 1.12). 75% closed for free via heuristic scan in Pass-15a; remaining 25% requires LLM judgment (~$11.50 per full pass) or focused native spot-check (~3 hr triage). |
| **EB-3** OQ-6 brief translation | Japan-based reviewer engagement | **Automatable** via DeepL + LLM polish. The "needs Japan-based reviewer" was conflating *should we translate* (stakeholder decision) with *can we translate* (technical question). Translation itself is now ~$1 + 1 hour. |
| **EB-4** OQ-1 v2.0 ML recommender | Learner-base data + privacy-clean path | **Automatable** without learner-base data. Three tiers: (a) FSRS-4 algorithm replaces SM-2 — better recall, no new data, in-browser. (b) Content-similarity recommender from corpus structure. (c) WebLLM browser-resident LLM for natural-language recommendations. None require telemetry. |

**The reframing:** these items moved from "human-required for the work" to "human-optional for prestige + spot-checks." The technical bar is now reachable by code. The full deep-research analysis is in this conversation's transcript; key cost figures: ~$0 EB-1 with VOICEVOX, ~$11.50 + 3hr EB-2, ~$1 + 2hr EB-3, $0 EB-4. Combined: ~$15 + ~20hr to close all four at the technical level.

**What still genuinely needs humans:**
- Native sign-off on released content (institutional / MEXT-alignment value, not technical)
- Cultural-appropriateness review (~10% of content)
- Final UI tone consistency review

These remain in the spec as native-reviewer responsibilities; they are smaller and more focused than the original "full coverage" stance.

### B.14 Pass 15a — free heuristic audit (2026-05-01)

A free, deterministic alternative to the LLM-audit pipeline ran on all 187 grammar patterns. Tooling: `tools/heuristic_audit.py`. Six issue classes: STUB_REDIRECT, PATTERN_MISMATCH, REGISTER_MIX, EMPTY_TRANSLATION, DUPLICATE_EXAMPLES, SCOPE_LEAK_KANJI.

**Result**: 60 findings, 75% precision (45 real / 15 heuristic-noise from verb-conjugation form matching and non-register-topical mixed examples). All 45 real findings fixed in the same pass.

**Standout closures**:
- 38 patterns had auto-generated `"Duplicate-cleanup redirect. See n5-XXX..."` text leaking to learners as `notes`. Same class as Pass-12 F-12.3 fixed for `data/questions.json`; the `data/grammar.json` equivalent had been missed.
- n5-158 was teaching `でしょう` in a pattern explicitly named `〜だろう` (casual form). Pedagogical inversion sat in data through 14 prior passes.
- n5-112 was demonstrating its kana-counter pattern with 分 kanji examples, bypassing the learning point.

**Heuristic precision per rule**: H1 STUB_REDIRECT 97%, H2 PATTERN_MISMATCH 45%, H3 REGISTER_MIX 20%. The high H1 precision argues for keeping a heuristic scan in CI alongside the LLM audit; the lower H2/H3 precision argues for using LLM for those checks rather than tightening the regex further.

Full Pass-15a log in `verification.md`. Cumulative tally across all passes: ~635 findings, ~620 fixed, 2 deferred to Pass-15-true.

### B.15 Microinteractions vs Zen Modern — formal spec deviation (2026-05-01)

The original UI design brief (`feedback/jlpt-n5-ui-design-brief.md` §8.2) called for the following microinteractions:

- Card hover lift (translateY -2px on hover)
- Button press scale (transform: scale(0.98) on `:active`)
- Shake animation on incorrect answer
- Pulse / glow on correct answer

The v1.8.0 Zen Modern design overhaul (`specifications/jlpt-n5-design-system-zen-modern.md` §0.5 + §8) explicitly forbids these:

> **§0.5:** "No shadows, no gradients, no glass effects. Ever. Including hover states."
>
> **§8:** Forbidden motion: bouncy springs, confetti, **card lift / shadow on hover**, wiggle, shake, pulse, glow, sliding panes, fading in entire pages from blank.

**Resolution (this section is the formal record):** the Zen Modern spec **supersedes** the UI design brief on microinteractions. Hover affordances are rendered through:

1. Background lightening (surface → surface-alt)
2. Border-color strengthening (line → line-strong)
3. Underline on `.card-action` text only

Correctness feedback in drill / test surfaces uses **color + class change only** — `.choice-button.correct-choice` gets `color: var(--color-correct)` + tinted background; `.choice-button.wrong-choice` gets the incorrect tint + strikethrough. No motion, no shake.

The Pass-15 design-system static checker (`tools/check_design_system.py`) enforces this:
- **D-3** No `box-shadow:` declarations (other than `none`)
- **D-4** No `transform:` inside `:hover` blocks
- **D-8** No decorative `text-shadow`

Any future re-introduction of the UI design brief's microinteractions would fail D-3, D-4, or D-8 in CI. This guards the Zen Modern aesthetic against drift back to the SaaS-default microinteraction palette.

OPEN-9 from `feedback/MASTER-TASK-LIST.md` closed via this section.

---

## C. Updates to existing v3 sections (errata)

### C.1 §3 Scope - move out of "Out of Scope"

These were listed as out-of-scope in v3 but have shipped:

- ✅ Audio / listening practice → now **In Scope** (491 MP3s; listening module with 3 JLPT formats)
- ✅ Service worker / PWA → now **In Scope** (NFR-W1 to NFR-W6)
- ✅ Mobile-friendly responsive layout → now **In Scope** (Brief 2 §9)
- ✅ Adaptive testing with ease factors → now **In Scope** (SM-2 SRS replaces Leitner)

These remain **Out of Scope** (binding):

- User accounts / login (Hard constraint #3)
- Server-side analytics / telemetry (Hard constraint #2)
- Cloud sync (Brief 1 Out-of-Scope)
- Multi-learner profiles (was in §13 Future; promote to permanent Out-of-Scope per #3)
- Open-ended writing or essay evaluation
- Speaking practice with microphone input
- Runtime AI / TTS calls
- N4+ content

### C.2 §5.1 Global Navigation - rewrite

**Replace** the old "Learn / Test / Drill / Review / Summary" with:

| Tier | Items | Notes |
|---|---|---|
| Primary nav | Home / Learn / Practice / Review / Test | "Practice" replaces "Drill"; "Daily Drill" renamed |
| Secondary nav | Search input + Summary + Settings + Help (?) | Search has `/` shortcut |
| Mobile (≤480 px) | Primary nav becomes fixed bottom bar with safe-area inset | per Brief 2 §9 |
| Persistent | Streak chip + offline indicator (top-right) + location chip (under header) | per Brief 2 §2.4 / §12.4 |

### C.3 §5 UX/UI - new sub-sections needed

Add to v3 §5:

- **§5.0 Home** (`#/home`) - first-time vs returning state; CTA + 3 pillar cards (first-time); Continue card + Today's queue + Streak heatmap (returning).
- **§5.2.5 Learn hub** (`#/learn`) - 5-card hub: Reference (Grammar / Vocabulary / Kanji), Practice (Dokkai / Listening). 3+2 semantic split.
- **§5.2.6 Vocabulary index + per-word detail** (`#/learn/vocab` and `#/learn/vocab/<form>`) - 1002 vocab cards in 40 sections; per-word detail with 5 example sentences sourced from grammar.json.
- **§5.2.7 Kanji index + per-kanji detail** (`#/kanji` and `#/kanji/<glyph>`) - 97 cards (glyph + meaning + first kun/on); per-kanji detail with prev/next nav.
- **§5.9 Settings** - explicit panel: UI lang / theme / font / 3-mode furigana (Always / Hide-on-known-kanji / Never) / live furigana preview / audio speed (0.75/1.0/1.25) / reduce motion (auto/on/off) / typed-phrase reset / export / import.
- **§5.10 Reading module** (`#/reading`) - 30 graded passages with 2-3 comprehension questions each.
- **§5.11 Listening module** (`#/listening`) - 12 items across 3 JLPT formats (4 task / 4 point / 4 utterance).
- **§5.12 Topic deep-dives** - こそあど / は vs が / Verb groups / て-form gym / Particle pairs / Counters.

### C.4 §5.8 Drill / SRS - replace Leitner with SM-2

v3 says "Leitner-light, 1d / 3d / 7d / 14d intervals." **Reality:** the app uses **SM-2** with Again / Hard / Good / Easy 4-button grading and a per-item ease factor (verified in `tests.html`).

Replacement text:

> Drill / Review uses **SuperMemo-2 (SM-2)** spaced repetition. Each item carries an ease factor (default 2.5, floor 1.3) and a current interval. Grade buttons:
> - **Again** (lapse): interval = 1 day; ease drops by 0.2; repetition counter resets to 0.
> - **Hard**: interval = max(1d, current × 1.2); ease drops by 0.15.
> - **Good**: per SM-2 schedule (rep 1 → 1d, rep 2 → 6d, rep 3+ → previous × ease).
> - **Easy**: interval = current × ease × 1.3; ease rises by 0.15.
>
> Verified in `tests.html`: rep 1 → 1d, rep 2 → 6d, rep 3 → 15d; lapse drops EF to 1.96.

### C.5 §7 Data Model - add new schemas

Add:

#### §7.6 knownKanji set

```json
{
  "knownKanji": ["学", "校", "本"]
}
```

Stored in `localStorage.knownKanji`. Feeds the "hide-on-known-kanji" furigana mode.

#### §7.7 Streak

```json
{
  "streak": {
    "current": 7,
    "longest": 23,
    "lastStudyDate": "2026-04-30",
    "days": ["2026-04-24", "2026-04-25", "..."]
  }
}
```

`days[]` is a rolling 30-day array used by the heatmap.

#### §7.8 Audio manifest

`data/audio_manifest.json` enumerates the rendered MP3s. Format:

```json
{
  "n5-001.0": "audio/n5-001.0.mp3",
  "reading-001": "audio/reading-001.mp3"
}
```

If a key is absent, the app degrades gracefully (no audio button).

#### §7.9 Updated Settings Object

Replace v3 §7.5 with the current schema:

```json
{
  "uiLang": "en",
  "theme": "auto",
  "font": "default",
  "furiganaMode": "hide-known",
  "audioSpeed": 1.0,
  "reduceMotion": "auto",
  "lastTestLength": 20,
  "lastLearnId": "n5-042",
  "diagnosticCompleted": true,
  "lastDiagnosticDate": "2026-04-29T19:00:00+09:00",
  "exportSchemaVersion": 2
}
```

### C.6 §9 Repository Structure - replace tree

Replace the v3 tree with the current state. The diff is large; here is the canonical current tree:

```
/JLPT/N5/
  index.html
  manifest.webmanifest
  sw.js
  tests.html
  README.md
  CHANGELOG.md
  /css/
    main.css
  /js/
    app.js
    home.js
    learn.js
    test.js
    drill.js
    review.js
    summary.js
    diagnostic.js
    settings.js
    storage.js
    furigana.js
    i18n.js
    pwa.js
    search.js
    shortcuts.js
    kanji.js
    kanji-popover.js
    kosoado.js
    waga.js
    verb-class.js
    te-form.js
    particles.js
    counters.js
    listening.js
    reading.js
    normalize.js
  /data/
    grammar.json
    questions.json
    vocab.json
    kanji.json
    reading.json
    listening.json
    audio_manifest.json
    n5_kanji_readings.json
    n5_vocab_whitelist.json
    n5_kanji_whitelist.json
  /locales/
    en.json
    vi.json
    id.json
    ne.json
    zh.json
  /audio/
    n5-001.0.mp3
    ... (491 MP3s)
  /tools/
    build_data.py
    build_audio.py
    check_coverage.py
    lint_content.py
    check_content_integrity.py   # to be added per ui-testing-plan §12.1
  /KnowledgeBank/
    grammar_n5.md
    kanji_n5.md
    vocabulary_n5.md
    sources.md
    moji_questions_n5.md
    goi_questions_n5.md
    bunpou_questions_n5.md
    dokkai_questions_n5.md
    externally_sourced_n5.md
  /specifications/
    JLPT N5 Grammar Tutor – Functional Spec.docx       # v3
    JLPT-N5-Functional-Spec-v3.1-supplement.md         # this file
  /feedback/
    jlpt-n5-tutor-developer-brief.md                   # Brief 1
    jlpt-n5-tutor-ux-developer-brief2.md               # Brief 2
    jlpt-n5-content-correction-brief.md                # Pass 9 source
    ui-testing-plan.md                                 # 22-perspective UI testing plan
  /not-required/
    (archived earlier spec versions and transient artifacts)
  TASKS.md
  verification.md                                      # Pass 1-10 audit log
```

### C.7 §11 NFR - replace with full set

Replace v3 §11 with the consolidated NFR table (Performance §B.6.3, Accessibility §B.6.4, i18n §B.6.1, PWA §B.6.2, plus the remaining items below):

| Category | Requirement |
|---|---|
| Compatibility | Latest 2 versions of Chrome, Firefox, Edge, Safari (desktop + mobile). Samsung Internet supported. |
| Reliability | No data loss without explicit "Type RESET" confirmation. Export → wipe → import round-trips. |
| Content integrity | `tools/lint_content.py` + `tools/check_coverage.py` + `tools/check_content_integrity.py` must all exit 0 before release. |
| Offline | After first load, app continues to work offline; service worker caches shell + content. |
| Telemetry | None. No analytics, no third-party scripts, no remote API at runtime. (Hard constraint #2.) |
| Security | HTTPS only (GitHub Pages). All `target="_blank"` links carry `rel="noopener noreferrer"`. CSP meta tag shipped in v1.6 (OQ-3 closed 2026-04-30). |
| Storage | LocalStorage only. No IndexedDB, no cookies, no remote storage. Namespace `jlpt-n5-tutor:*`. |

### C.8 §13 Future Enhancements - rewrite

Drop shipped items (audio, mobile responsive, PWA / SW, adaptive SRS). Replace with:

- **F-1** Listening corpus expansion (12 → 30+ items). OQ-2 approved 2026-04-30; native voice talent required (no gTTS for new items). Authoring backlog in `TASKS.md`.
- **F-2** Privacy-preserving on-device recommendation engine (no telemetry). OQ-1 minimal version shipped in v1.6 (Home recommender); richer ML-backed engine still deferred to v2.0.
- **F-3** ~~Optional~~ CSP meta tag for additional XSS hardening. OQ-3 closed; shipped in v1.6.
- **F-4** Audio analytics in the export schema (when scope expands). OQ-4.
- **F-5** N4 expansion in a sibling repo (not this one). Out of scope but flagged for ecosystem planning.
- **F-6** Native mobile wrapper (Capacitor / React Native) - **out of scope**; PWA satisfies the use case.
- **F-7** Speaking practice with microphone input - **permanent out of scope** (Brief 1).

---

## D. Content audit protocol (Pass-N) - normative

This section formalizes the Pass-N protocol that produced the 462 closed findings in `verification.md`.

### D.1 Audit lenses (used so far)

| Pass | Lens | Findings raised | Closed |
|---|---|---|---|
| 1-4 | Initial KB content checks | 24 | 24 |
| 5 | First batch corrections | 11 | 11 |
| 6 | JLPT paper-maker perspective | 39 | 39 (across 6 / 6.5 / 7) |
| 8 | Native Japanese teacher perspective | 52 | 52 |
| 9 | External 日本語教師 (content correction brief) | 38 | 38 |
| 10 | Audio + auto-furigana correctness (TTS / rendering) | 309 | 309 |
| **Total** | - | **462** | **462** |

### D.2 Pass-N triggers

- Calendar: every quarter (next: 2026-07-30).
- Event: any batch of 10+ KB edits between releases.
- Event: any new audit lens proposed (e.g., "child-learner readability", "JLPT N4 readiness").
- Event: any externally-supplied audit brief (like the Pass-9 source).

### D.3 Pass-N execution

1. Pick the lens; document it in the new pass entry header.
2. Read all 5 question files + 4 catalog files (or the affected subset).
3. Log findings with severity (CRITICAL / HIGH / MEDIUM / LOW); register in `TASKS.md`.
4. Fix in priority order; update `verification.md` per finding.
5. Re-run §B.7 / §12.1 invariants; all must pass.
6. Mark the Pass closed; update cumulative tally in `verification.md`.

### D.4 Severity definitions

| Severity | Definition | Release impact |
|---|---|---|
| **CRITICAL** | Factual error, internal contradiction, or content that would teach **wrong Japanese** | Blocks release; hotfix |
| **HIGH** | Unidiomatic phrasing, register clash, or policy violation | Fix in next release |
| **MEDIUM** | Pedagogical clarity improvement | Batch into next quarterly pass |
| **LOW** | Polish item | Batch into next quarterly pass |

### D.5 The bar (non-negotiable)

- Zero CRITICAL findings open at release.
- 100% of cumulative findings closed (currently 462/462).
- Pass-N protocol followed for every cadence event.

---

## E. Acceptance criteria for v4

When this supplement is merged into the .docx, the resulting v4 is acceptable when:

1. All §A.1 missing sections are present.
2. All §A.2 drift items are corrected.
3. The glossary (§B.2) is complete; every term used in the spec is defined.
4. The success metrics (§B.5) are measurable, not goals.
5. The risks register (§B.8) has at least 8 entries; every High-impact risk has a documented mitigation.
6. The test strategy (§B.7) references `feedback/ui-testing-plan.md` and `tests.html`.
7. The content audit protocol (§D) is normative and binding.
8. The sign-off matrix (§B.1.2) is filled in (signed by named reviewers, not blank).
9. All references to "Drill" / "Leitner" / "Phase 1.5 optional PWA" / "Audio out of scope" are removed.
10. The repository tree (§C.6) matches the live repository as of merge date.
11. (Added 2026-05-03) The §F revision block reflects the post-Pass-22 work and §F's NFRs are integrated into v4 §11.

---

## F. Revision 2026-05-03 — Mobile UI / Disabled-button feedback / Data audit / State-machine fixes

This block captures work shipped between the supplement's original 2026-04-30 revision and 2026-05-03. Each subsection is a candidate for direct merge into v4 §11 (NFRs) / §5 (UX) / §12 (Quality gates) / §13 (Future). Acceptance criteria #11 above gates the merge.

### F.1 Mobile UI contract — new NFR cluster (NFR-M1..NFR-M9)

The mobile experience hardening pass shipped a desktop-safe contract that gates every mobile-specific style behind explicit breakpoints and verifies desktop is byte-identical after each sweep. The contract is normative for any future mobile work in this codebase.

**Breakpoint tier:**

| Breakpoint | Scope | Rules live at this tier |
|---|---|---|
| `@media (max-width: 768px)` | Phone + tablet portrait | Most mobile rules — body type-floor, overflow-x safety belt, smooth scroll, iOS-zoom inputs, tap feedback, h2 cap, auxiliary-control tap-target rules |
| `@media (max-width: 480px)` | Small phones | Pattern-header column-stack, pattern-usage-table padding/nowrap, secondary-nav single-row, footer center, primary-nav fixed bottom, body padding-bottom for safe-area |
| `@media (max-width: 380px)` | Galaxy S9+ tier | Bottom-nav font/padding/min-width crunch when ≤480 still spills |

**Non-functional requirements:**

- **NFR-M1** Tap-target floor — every interactive element ≥ 44 px on its smallest dimension. Auxiliary controls (icon-btn, breadcrumb back-link, footer-nav links, pattern-nav arrows, known-toggle) carry mobile-only `min-height: 44px` rules so the global floor reaches them.
- **NFR-M2** iOS auto-zoom prevention — every text/search/email/number input + textarea + select rendered at ≥ 16 px on `≤768` breakpoint. Required because iOS Safari auto-zooms on tap when the input's computed font-size is below 16 px, pushing the input above the keyboard fold.
- **NFR-M3** Overflow safety belt — `html, body { overflow-x: hidden; }` at `≤768` so any descendant wider than viewport never triggers page-wide horizontal scroll on a 320 px phone. Defensive; current state has zero overflow at 320 px.
- **NFR-M4** Body type-floor — `body { font-size: max(16px, var(--text-base)); }` at `≤768`. Respects the user's font-size knob (Settings > Font: S/M/L/XL); on default S/M (where `--text-base` resolves to 13–15 px), this lifts body to 16 px for readability and reinforces NFR-M2 by making body text ineligible for the iOS-zoom threshold trigger.
- **NFR-M5** Visible tap feedback — every primary tap target gets a brief `:active { transform: scale(0.97); opacity: 0.85; transition: 80ms }` at `≤768`. Mobile has no `:hover` equivalent; without this, tap-down feels unresponsive on slow networks.
- **NFR-M6** Smooth scroll — `html { scroll-behavior: smooth; }` at `≤768`. Anchor jumps + route changes animate; matches OS-level scroll snap.
- **NFR-M7** Container gutter — at `≤480` breakpoint, `main + .app-footer + .app-header` collapse inline padding from desktop's 22.5 px to 16 px so cards use ~92 % of viewport width. Don't apply universal `* { max-width: 100% }` — it constrains SVG icons + brand-mark pseudo-elements.
- **NFR-M8** Heading hierarchy on narrow screens — `h2` clamps at 18 px (not desktop's 22 px) at `≤768`. On 320 px viewports, 22 px h2 reads as indistinguishable from h1 (also 22 px) and the typographic cascade collapses. 22 / 18 / 16 (h1 / h2 / body) restores readable hierarchy.
- **NFR-M9** Desktop safety — every mobile sweep ships with a 1280 px regression check. Every value listed above MUST match the desktop default after the sweep (body overflow-x: visible, scroll-behavior: auto, body font: ~14.06 px, main padding: 22.5 px, no `:active` rule applied, h2 at 22 px). The mobile rules MUST cut off cleanly at 769 px.

**QA contract** (added to ui-testing-plan §17 — Mobile QA tier):

Test at viewports 320 / 360 / 390 (the spec QA tier) plus 480 / 768 (boundary) plus 1280 (desktop safety):

```
[ ] No horizontal scroll  (document.documentElement.scrollWidth === clientWidth)
[ ] No CJK per-char break  (any heading wrapping with avg < 3 chars/line)
[ ] All tap targets ≥ 44 px on smallest dimension
[ ] body { font-size } ≥ 16 px at all mobile widths
[ ] All inputs ≥ 16 px (iOS zoom test)
[ ] Card descriptions show full text or clean line-aligned ellipsis (no mid-line clip per F.4 below)
[ ] Smooth scroll on anchor jumps
[ ] Desktop @ 1280: every value listed in NFR-M9 matches pre-mobile-sweep defaults
```

### F.2 Disabled-button feedback contract — new NFR-U cluster

Any control that can be disabled MUST display the reason in visible UI text — not only in a `title` tooltip. Tooltips don't fire on touch; mobile users get a silent dead control.

**Patterns:**

| Pattern | Required visible reason | Reference example in this app |
|---|---|---|
| Submit / Finish disabled until all answered | Show "(N remaining)" in button text + a hint paragraph | `Submit (13 remaining)` + "Answer all 15 questions to submit · 13 questions unanswered" — `js/papers.js`, `js/test.js`, `js/diagnostic.js` |
| Check Answer disabled until any answer | Type-aware hint above the button | "Pick a choice, then click Check Answer." / "Tap the tiles in order to build the sentence, then click Check Answer." / "Type your answer in the box, then click Check Answer." — `js/drill.js` |
| Confirm disabled until typed phrase | The input field IS the visible reason | `Type RESET to confirm` next to a `Confirm reset` button — `js/settings.js` |
| Prev / Next at first / last item | Position context (progress meter "Q15 of 15") makes it obvious; no explicit hint needed | – |
| Per-choice / per-tile disabled after submission | Feedback panel below shows the result | – |

**Saved-toast pattern** (silent settings):

For settings that save but have no immediate visible side-effect (daily-new-card limit, daily-review-cap, default test length, audio-rate, reduce-motion), `js/settings.js` shows a brief on-screen toast on every change: `Saved: <label> = <value>`. CSS class `.settings-saved-toast` — fixed-position bottom-centre, 180 ms fade, 1800 ms auto-dismiss, respects `prefers-reduced-motion`.

**Export action confirmation:** the file dialog is easily missed in the browser's downloads bar. `js/settings.js` shows a status line under the Export button: `Exported to <filename> (check your downloads folder).` Auto-clears after 4 s.

**NFR-U1** Pre-release feedback audit checklist:

```
[ ] Every <button [...] disabled> rendering site has visible reason text
[ ] Every settings setter without immediate visual effect has a saved-toast
[ ] Every async action with > 200 ms latency has a loading or status indicator
[ ] Every disabled control verified by tap (not hover) on a touch-only browser
```

### F.3 New invariants — JA-25..JA-33

Adds nine invariants to the §C.7 / `tools/check_content_integrity.py` register beyond the JA-21 baseline of v3.1:

| ID | What it checks | Severity |
|---|---|---|
| **JA-22** | No "direct synonym / directly equivalent / same as" in goi rationales | HIGH |
| **JA-23** | Multi-correct scanner: every MCQ where choices include known-interchangeable particle pairs (に/へ direction, から/ので reason, は/が topic-vs-subject) flagged for native review | HIGH |
| **JA-24** | No duplicate `pattern` strings in grammar.json across entries with overlapping `meaning_en` (catches the Pass-19 redundancy class) | MEDIUM |
| **JA-25** | Whitelist exceptions documented — every kanji used in a user-facing field that's NOT in the N5 whitelist must have a corresponding entry in an explicit augmented set with a WHY-comment in the integrity tool | HIGH |
| **JA-26** | No duplicate question IDs (across the entire bank) | CRITICAL |
| **JA-27** | No English-translation/title fields in `data/reading.json` / `data/listening.json` (Japanese-first surface policy) | HIGH |
| **JA-28** | Dokkai-paper kanji bounded by N5 whitelist + explicit exception list | HIGH |
| **JA-29** | Question subtype taxonomy is closed — `subtype` field can only take values in an explicit allow-list (currently `paraphrase`, `kanji_writing`); new subtypes require an explicit code change, not a data sneak-in | HIGH |
| **JA-30** | No past-paper provenance signatures in question text — original-content policy enforced by regex against known JEES/past-paper phrasings (see `CONTENT-LICENSE.md`) | CRITICAL |
| **JA-31** | Vocab PoS parity — `pos` field on every `data/vocab.json` entry agrees with the matching entry in `KnowledgeBank/vocabulary_n5.md`. Treats homographs as a SET-VALUED match (storage uses `setdefault().add()`, not last-write-wins dict) so section-30 `いる` exist=verb-2 vs `いる` need=verb-1 don't false-positive each other | HIGH |
| **JA-32** *(suggested)* | Broken cross-references — every `contrasts.with_pattern_id` and every `See n5-NNN` reference in `form_rules.conjugations.label` resolves to an active `n5-` ID in `data/grammar.json#patterns[].id` | HIGH |
| **JA-33** *(suggested)* | No mid-line clipping in tile-grid card descriptions — Playwright/visual-regression assertion: at every supported viewport (320 / 480 / 768 / 1280), every `.<card>-desc` has `boundingClientRect.height` that's an integer multiple of computed line-height (within 2 px tolerance) | MEDIUM |

The release-blocker rule (NFR-C, §C.7) extends to the new invariants: all 33 must pass before any release.

### F.4 New anti-patterns from N5 layout regressions

Documented in the procedure manual at `procedure-manual-build-next-jlpt-level.md` §3.2.7 – §3.2.10; reference here for in-spec record:

- **AP-7** Don't ship cross-references to retired patterns after a dedup pass (HIGH). After any pattern-retirement pass, scan for `contrasts.with_pattern_id` and `form_rules.conjugations.label "See n5-XXX"` references to retired IDs; repoint to canonical replacement or remove. JA-32 invariant catches this going forward.
- **AP-8** Don't mass-stamp PoS by thematic vocab section (CRITICAL). The Group-2 case is pedagogically dangerous — a learner using `あげる` from the existence-section copy gets told it's verb-1 → conjugates *あげります instead of あげます. Tag PoS per-WORD, not per-section default. Closed in Pass-24 (23+ entries fixed). JA-31 invariant catches regressions.
- **AP-9** Don't mid-line-clip card descriptions on fixed-height tile grids (HIGH). `flex: 1` + `display: -webkit-box` + `-webkit-line-clamp: N` + fixed-height parent = Chrome normalises display to `flow-root`, line-clamp goes inert, overflow:hidden mid-line-clips. Belt-and-suspenders fix: `max-height: Nlh` next to `-webkit-line-clamp` + remove `flex: 1` + use `margin-top: auto` on action element to pin to card bottom. JA-33 invariant catches regressions.
- **AP-10** Don't keep stale module-level state on URL navigation (HIGH). Render entry-points that short-circuit on `view === 'finished'` without resetting on URL navigation cause back-buttons inside results pages to re-render the same results page. Reset rule: `'attempting'` resumes on refresh; `'finished' / 'results'` resets when URL navigates away. Applied to `papers.js` / `test.js` / `review.js` / `drill.js`.

### F.5 Corpus state — current snapshot

Replaces v3 §0 / §A.7 corpus counts:

| Corpus | v3 stated | Current (2026-05-03) | Delta |
|---|---|---|---|
| Grammar patterns | ~187 | **177** active (10 retired in Pass-19 dedup, IDs preserved as opaque retired keys) | -10 |
| Vocabulary entries | ~1003 | **1003** | 0 |
| Vocabulary entries with inline examples | ~210 | **374+** (Phase 4 + Phase 5 authoring shipped May 2026; +154 in Phase 4 alone) | +164 |
| Kanji glyphs | 106 | **106** | 0 |
| Reading passages | 30 | **40** (corpus expanded post-supplement) | +10 |
| Listening items | 12 | **40** (corpus expanded post-supplement; ~22 native-recordings outstanding per OQ-2 per item) | +28 |
| Question banks total | ~250 | **~590** across moji/goi/bunpou/dokkai per `data/papers/manifest.json` | +340 |
| Mock-test paper count | 0 (single ad-hoc test) | **multi-paper structure** under `data/papers/<category>/paper-<n>.json`; 4 categories, 15 q/paper | new structure |

### F.6 New routes / pages — supersedes v3 §5 routing table for these additions

| Route | Purpose | Status |
|---|---|---|
| `#/levels` | **Level-1 picker** (N5/N4/N3/N2/N1). Default landing per §0.A of `procedure-manual-build-next-jlpt-level.md`. N5 card available; N4..N1 disabled with "Content not yet available" placeholder | Shipped |
| `#/n4`, `#/n3`, `#/n2`, `#/n1` | Placeholder pages with "Content not yet available" message | Shipped |
| `#/feedback` | **Feedback / bug-report form** with email obfuscation. Recipient address never appears as a literal in source — decoded only at click-time from a char-code array. Uses `mailto:` URL with subject prefix `JLPT-Tutor Feedback - <Title> [<Category>]` | Shipped |
| `#/papers` / `#/papers/<cat>` / `#/papers/<cat>/<n>` | **Multi-paper mock-test structure** — 4 categories (moji/goi/bunpou/dokkai), 15 q/paper, score persistence per paper via `localStorage.jlpt-n5-tutor.paper.<id>` | Shipped |
| `#/changelog` | Auto-rendered from `CHANGELOG.md` | Shipped |

### F.7 Service worker version + PWA contract additions

- **NFR-W2 update**: SW current = `jlpt-n5-tutor-v110` (as of 2026-05-03). The version bumps on every shell change. Frequency since supplement was last edited (~2026-05-01): ~16 bumps in 2 days reflecting the Mobile UI / Data audit / State-machine sweep cadence.
- **NFR-W7** (new): cache-bust contract for ES modules. Browsers cache ES modules by URL; bumping `CACHE_VERSION` in `sw.js` is necessary but not sufficient — `index.html` must also bump `?v=N` on the entry script (`<script src="js/app.js?v=N">`). Without both, users see stale shell on next visit because the unchanged `import './module-x.js'` URLs hit the browser's module cache.
- **NFR-W8** (new): SW pre-cache list maintenance. The `PRECACHE` array in `sw.js` must list every static asset reachable on first paint, including the inline-SVG favicon, the 5 locale files, all 25+ JS modules, and the 4 self-hosted woff2 font subsets. Missing entries silently degrade offline UX.
- **§D / Content-protection layer**: shipped as a feature flag in `js/content-protect.js` (`CONTENT_PROTECT_ENABLED`). Currently OFF (allows screenshots / Ctrl+C / right-click for bug-report use). When ON: blocks contextmenu / copy / cut / dragstart / selectstart / Ctrl+C/A/X/S/P/U / F12 / Ctrl+Shift+I/J/K/C; window-blur sets `html[data-blur=true]` to obscure during region-screenshots; `@media print` blanks the page. Documented as honest deterrent — devtools / view-source / phone-camera-of-screen still work.
- **`CONTENT-LICENSE.md`**: shipped at repo root. Original-content policy + reference sources + JEES contact path. JA-30 invariant + `tools/audit_provenance.py` enforce the policy at CI time.

### F.8 Pass-N audit log update

Extends §D.1:

| Pass | Lens | Findings raised | Closed | Cumulative tally |
|---|---|---|---|---|
| 11-14 | (covered in v3.1 baseline) | 91 | 91 | 553 |
| 15 | Multi-correct sweep + grey-zone audit (8 categories A-H) | 28 | 28 | 581 |
| 15a | Free heuristic audit (`tools/heuristic_audit.py`) | 60 | 60 | 641 |
| 16 | Pre-native-review dossier preparation | 14 | 14 | 655 |
| 17 | KnowledgeBank PoS-tag injection (37 drift entries) + JA-31 invariant added | 37 | 37 | 692 |
| 18-19 | Late-tier reclassification + 14 patterns promoted | 14 | 14 | 706 |
| 20 | Procedure manual review (40 issues — operating modes, MVS, definition-of-done) | 40 | 36 + 4 deferred | 742/746 |
| 21 | Procedure manual Appendix B (extracted-from-N5) | 12 | 12 | 754 |
| 22 | Procedure manual Appendix C (polish) + design-system D-3/D-4/D-8 rules | 9 | 9 | 763 |
| 23 | Provenance lock-in (CONTENT-LICENSE.md + JA-30 + tools/audit_provenance.py) | – | – | – |
| 24 | Seasoned-teacher review (T-1..T-9 automated + manual sample) | 12 | 12 | 775 |
| 25 | Pre-review native-dossier audit (14 findings — 3C/4H/5M/2L) | 14 | 14 | 789 |
| 26 | Follow-up dossier audit (closure verification) | 0 | 0 | 789 |
| 27 | Data-files audit (grammar/vocab/kanji JSON; 10 actionable items) | 10 | 8 + 2 deferred | 797/799 |

**Pass-N protocol unchanged** — quarterly cadence, severity matrix, CRITICAL-blocks-release rule still binding. The auto-generated `feedback/closed/` archive (set up 2026-05-03) groups all closed audit reports for traceability without cluttering the active queue at `feedback/`.

### F.9 Procedure manual + companion docs (added 2026-05-01..2026-05-03)

Companion documentation produced during this revision window. Reference + status:

| Document | Path | Purpose |
|---|---|---|
| **Procedure manual** | `JLPT/procedure-manual-build-next-jlpt-level.md` (root, level-agnostic) | Prescriptive playbook for building any next JLPT level (N4..N1) from this N5 source. Two execution modes (A: human + AI; B: zero-interaction one-shot agent). Updated 2026-05-03 with §3.2.7..§3.2.10 anti-patterns, §4.5 Mobile UI contract, §4.6 Disabled-button feedback contract, §0.A One-instruction autonomous-build contract, §A.12 15-step ordered execution sequence, §A.13 completion handoff format. |
| **Appendix B** | `specifications/procedure-manual-appendix-b-extracted-from-n5.md` | Schemas, rules, configurations extracted from the N5 codebase so a Mode-B agent can implement them without inferring from prose. |
| **Appendix C** | `specifications/procedure-manual-appendix-c-pass22-polish.md` | Pass-22 polish items — distractor rubric, ko-so-a-do scene-context, JA-2/JA-23 interaction, augmented-set escape-valve guard, auto-generation stop-condition, full PWA spec, same-pattern-string conflict-resolution. |
| **Procedure manual review** | `feedback/procedure-manual-review-issues.md` | 40 issues against the manual; status: 36 closed in §A / §B, 4 still tracked. |
| **Master task list** | `feedback/MASTER-TASK-LIST.md` | Single-source-of-truth running tracker of all open / open-infra / deferred / done items. Replaces individual audit-doc tracking. |
| **Closed-archive index** | `feedback/closed/README.md` | One-line-per-file rationale for the 28 closed feedback documents archived 2026-05-03. |
| **N4 inventory artifacts** | `feedback/n4-{grammar,kanji,vocab-sample,inventory-manifest}.md` | Bootstrap content lists for a future N4 build. Closes Pass-21 F-20.12..F-20.14. |
| **JEES inquiry template** | `feedback/jees-inquiry-template.md` | Drafted-but-not-sent email template for past-paper licensing inquiries. Activates only if the project ever wants to use specific past-paper questions verbatim. |

### F.10 Open / deferred items snapshot — 2026-05-03

Replaces the prior MASTER-TASK-LIST snapshot in §B.9 / §B.13:

| Severity | Open | Open-Infra | Deferred | Done | Total |
|---|---|---|---|---|---|
| CRITICAL | 0 | 0 | 0 | 22 | 22 |
| HIGH | 0 | 2 | 1 | 41 | 44 |
| MEDIUM | 0 | 3 | 6 | 28 | 37 |
| LOW | 0 | 0 | 5 | 17 | 22 |
| **Total** | **0** | **5** | **12** | **108** | **125** |

**Bottom line**: zero actionable code-doable items remain; 5 items still need external infrastructure (audio re-render via VOICEVOX, BrowserStack); 12 deferred to long-term roadmap.

---

*End of supplement. Merge into the next .docx revision and tag it v4.*

*Prepared 2026-04-30. Revised 2026-05-01 (B.13–B.15 additions). Revised 2026-05-03 (§F revision block — Mobile UI / Disabled-button feedback / Data audit / State-machine fixes / Pass 16-27 cumulative).*


---

## §G Design System (Zen Modern) — merged 2026-05-04

*Was at `jlpt-n5-design-system-zen-modern.md`. Merged into this supplement so the functional spec is the single source of truth for both functional + visual contracts. The original file has been deleted; this section is the canonical record going forward.*

---

# JLPT N5 Tutor - Design System: Zen Modern (Muji)

**Theme:** Zen Modern - Muji-inspired
**Goal:** Spare, generous, almost monochrome. The product earns trust by getting out of the way. Looks credible on first load. Still looks credible in three years.
**Influences:** Muji catalog typography, Kinokuniya book design, Apple Human Interface circa 2014-16 (pre-glassmorphism), Japanese editorial print.

This document is the source of truth. Every page, component, and interaction in the JLPT N5 Tutor must conform to these tokens and rules. Ambiguity is resolved in favor of *less* visual weight, never more.

---

## 0. Design principles (read these before writing code)

1. **Hierarchy through scale and weight, not color.** Color is for state (correct, wrong, due). Hierarchy comes from type size and whitespace.
2. **One accent color, used sparingly.** The brand green is reserved for the active nav indicator, the primary CTA, and the focus ring. Nowhere else.
3. **Whitespace is the design.** When in doubt, add 24px of vertical space, not a divider.
4. **Hairlines, not borders.** All borders are 0.5px or 1px in a near-paper gray. Never thicker.
5. **No shadows, no gradients, no glass effects.** Ever. Including hover states.
6. **No emojis, no decorative icons in body text.** Use small SVG glyphs only where functional (audio play, stroke order, search).
7. **Typography weight 300 and 400 only for body. 500 for headings. Never 600 or 700.** Heavy weights look loud against this neutral surface.
8. **All text is sentence case.** Never Title Case. Never ALL CAPS except for tiny letter-spaced labels (e.g., "REFERENCE" above a card group).
9. **Numerals are tabular (`font-variant-numeric: tabular-nums`).** Stats, counters, timers, and SRS intervals must align vertically.
10. **Japanese text uses Noto Sans JP weight 400.** Mixing weights between latin and ja text creates uneven visual rhythm.
11. **Describe the contents. Offer no opinion about them.** Homepage copy is neutral and inventorial. No outcome claims, no second-person, no verbs of encouragement, no trust reassurance, no superlatives, no quantifier softeners. Counts are bare numerals plus nouns. The product is a study material; the copy says what it is, not what it does for the visitor.

If a proposed change would violate any of these, the proposed change is wrong.

---

## 1. Color tokens

### 1.1 Light mode

```css
:root {
  /* Surfaces */
  --color-bg:           #FFFFFF;   /* page background */
  --color-surface:      #FAFAF8;   /* card backgrounds, subtle differentiation */
  --color-surface-alt:  #F5F4F0;   /* hover state on cards */

  /* Hairlines */
  --color-line:         #E8E5DE;   /* default border / hairline */
  --color-line-strong:  #D4D0C7;   /* hover or focus border */

  /* Text */
  --color-text:         #1F1F1C;   /* primary text - near black, slight warmth */
  --color-text-muted:   #6F6D66;   /* secondary text, captions */
  --color-text-faint:   #9A968C;   /* tertiary text, hints, disabled labels */

  /* Brand accent (used sparingly) */
  --color-accent:       #1F4D2E;   /* deep forest green - active nav, primary CTA */
  --color-accent-hover: #163924;
  --color-accent-tint:  #EDF1EE;   /* very light tint for backgrounds of pills */

  /* Semantic (state only) */
  --color-correct:      #2E7D4F;
  --color-correct-tint: #ECF4EE;
  --color-incorrect:    #B43A2A;
  --color-incorrect-tint:#F7EAE7;
  --color-due:          #A66A1F;   /* warm amber for "review due" badges */
  --color-due-tint:     #F7EFE0;
}
```

### 1.2 Dark mode (mandatory parity)

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg:           #1A1A18;
    --color-surface:      #232321;
    --color-surface-alt:  #2C2C29;
    --color-line:         #34332F;
    --color-line-strong:  #4A4944;
    --color-text:         #ECEAE3;
    --color-text-muted:   #A8A59C;
    --color-text-faint:   #6F6D66;
    --color-accent:       #6FB58A;
    --color-accent-hover: #88C7A2;
    --color-accent-tint:  #2A3A2F;
    --color-correct:      #6FB58A;
    --color-correct-tint: #233028;
    --color-incorrect:    #E08572;
    --color-incorrect-tint:#3A2723;
    --color-due:          #D9A560;
    --color-due-tint:     #332B1E;
  }
}
```

### 1.3 Color usage rules

- **Primary text:** always `--color-text`. Never near-black `#000`.
- **Body backgrounds:** always `--color-bg`. Cards step up to `--color-surface`.
- **Hover backgrounds:** step from `--color-surface` to `--color-surface-alt`. Never use the accent tint as a hover.
- **Accent green:** ONLY on (1) the active nav underline, (2) the primary CTA filled button, (3) focus rings, (4) progress-bar fills, and (5) the small accent line under the wordmark. Five places total. Audit your CSS to enforce this.
- **Tinted pills (accent-tint, due-tint, etc.):** use sparingly. Reserve for state badges and small status indicators. Never as backgrounds for cards or sections.
- **Never** use red or warning colors for anything except actual errors. A "review due" indicator is amber, not red.

---

## 2. Typography

### 2.1 Font stack

```css
:root {
  /* Latin */
  --font-en:    "Inter", -apple-system, BlinkMacSystemFont,
                "Segoe UI", system-ui, sans-serif;

  /* Japanese */
  --font-jp:    "Noto Sans JP", "Hiragino Kaku Gothic ProN",
                "Yu Gothic", "Meiryo", sans-serif;

  /* Tabular numerics */
  --font-num:   "Inter", system-ui, sans-serif;
  /* with: font-variant-numeric: tabular-nums; */
}

body {
  font-family: var(--font-en);
  color: var(--color-text);
  font-feature-settings: "ss01" 1, "cv11" 1;  /* Inter alt single-story a, alt 4 */
}

:lang(ja), .lang-ja {
  font-family: var(--font-jp);
  font-feature-settings: "palt" 1;   /* proportional alternate widths for cleaner ja */
}
```

Inter is required (not optional) because the design depends on its weight 300 (Light) being available. System fallbacks don't have a true Light. If Inter fails to load, fall through to system but accept that the design will look slightly heavier.

Noto Sans JP must be loaded with weights 400 and 500 only. Subset to N5 + N4 character ranges to keep file size near 200KB woff2. Preload in `<head>`:

```html
<link rel="preload" href="/fonts/noto-sans-jp-400.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/fonts/inter-400.woff2" as="font" type="font/woff2" crossorigin>
```

### 2.2 Type scale

The scale is deliberately small. Big type fights the design.

```css
:root {
  --text-2xs:  0.6875rem;  /* 11px - tiny labels with letter-spacing */
  --text-xs:   0.75rem;    /* 12px - footer text */
  --text-sm:   0.8125rem;  /* 13px - card body, helper text */
  --text-base: 0.9375rem;  /* 15px - body */
  --text-md:   1.0625rem;  /* 17px - emphasized body / card titles */
  --text-lg:   1.25rem;    /* 20px - section headings */
  --text-xl:   1.625rem;   /* 26px - page titles */
  --text-2xl:  2rem;       /* 32px - hero headlines (used once per page max) */
}
```

Note the body size (15px) is one notch smaller than the SaaS default (16px). This is intentional. It pulls the whole UI tighter and is correct for content-heavy pages.

### 2.3 Weight rules

```css
:root {
  --weight-light:  300;
  --weight-base:   400;
  --weight-medium: 500;
}
```

- Body paragraphs: `--weight-base`
- Headings (h1, h2, h3): `--weight-medium`
- Page titles only: occasional use of `--weight-light` for the largest hero headline (`--text-2xl`, weight 300) - this is the Muji signature look.
- Japanese text: always `--weight-base`. Never light, never medium. Japanese forms have built-in optical weight that doesn't need typographic emphasis.
- Buttons: `--weight-medium`.
- Numerals in stats: `--weight-medium` with `font-variant-numeric: tabular-nums`.
- **Never use weight 600 or 700.** They look loud against this neutral surface.

### 2.4 Letter spacing

```css
:root {
  --tracking-tight:  -0.01em;
  --tracking-normal: 0;
  --tracking-wide:   0.05em;
  --tracking-label:  0.18em;   /* used on tiny ALL-CAPS labels */
}
```

- Body: `--tracking-normal`.
- Headings: `--tracking-tight`. Inter's default tracking at large sizes is slightly too open.
- Tiny ALL-CAPS labels (e.g., "REFERENCE" above a card group): `--tracking-label`. This is the only place ALL CAPS is allowed.
- Japanese text: never apply letter-spacing. Japanese typography handles its own rhythm.

### 2.5 Line height

```css
:root {
  --leading-tight: 1.25;
  --leading-base:  1.55;
  --leading-loose: 1.7;
}
```

- Headings: `--leading-tight`.
- Body paragraphs: `--leading-base`.
- Long-form reading content (passages, explanations): `--leading-loose`.
- Japanese paragraphs: `--leading-loose` minimum. Japanese needs more vertical air than English.

### 2.6 Headline templates

```css
.h1 {
  font-size: var(--text-2xl);
  font-weight: var(--weight-light);
  letter-spacing: var(--tracking-tight);
  line-height: var(--leading-tight);
  margin: 0;
}
.h2 {
  font-size: var(--text-xl);
  font-weight: var(--weight-medium);
  letter-spacing: var(--tracking-tight);
  line-height: var(--leading-tight);
  margin: 0;
}
.h3 {
  font-size: var(--text-lg);
  font-weight: var(--weight-medium);
  letter-spacing: var(--tracking-tight);
  line-height: var(--leading-tight);
  margin: 0;
}
.label {
  font-size: var(--text-2xs);
  font-weight: var(--weight-medium);
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
  color: var(--color-text-muted);
  margin: 0;
}
```

---

## 3. Spacing and layout

### 3.1 Spacing scale (4px base, 8pt-aware)

```css
:root {
  --space-1:  0.25rem;   /*  4px */
  --space-2:  0.5rem;    /*  8px */
  --space-3:  0.75rem;   /* 12px */
  --space-4:  1rem;      /* 16px */
  --space-5:  1.5rem;    /* 24px */
  --space-6:  2rem;      /* 32px */
  --space-8:  3rem;      /* 48px */
  --space-10: 4rem;      /* 64px */
  --space-12: 6rem;      /* 96px */
  --space-16: 8rem;      /* 128px */
}
```

The Muji aesthetic is defined by the BIG end of this scale. Section spacing is `--space-10` or `--space-12`, not `--space-6`.

### 3.2 Container widths

```css
:root {
  --container-narrow: 640px;   /* drill cards, settings page, single-column reading */
  --container-base:   880px;   /* standard content width */
  --container-wide:   1120px;  /* dashboards, multi-column index pages */
}
```

Use `--container-base` as the default. Don't fight to fill the viewport; large empty side margins are part of the look.

### 3.3 Page rhythm

A standard page has this vertical rhythm:

```
[ header, sticky ]                      <-- 56px tall
[ space-10 = 64px ]
[ page title, 32px / weight 300 ]
[ space-2 = 8px ]
[ tiny "page kind" label, ALL CAPS ]
[ space-8 = 48px ]
[ first content section ]
[ space-12 = 96px between sections ]
[ next content section ]
[ space-16 = 128px before footer ]
[ footer, 40px tall ]
```

The 96px between major sections is non-negotiable. It's what separates this design from a generic SaaS layout where sections sit 32-48px apart.

### 3.4 Border radius

```css
:root {
  --radius-sm: 2px;    /* tags, small chips */
  --radius-md: 4px;    /* buttons, inputs, small cards */
  --radius-lg: 6px;    /* large cards */
  --radius-pill: 999px;/* pills, badges */
}
```

Radii are intentionally small. The Muji look is geometric and slightly hard-edged. Avoid 12-16px radii common in modern SaaS.

### 3.5 Hairlines

All borders are 0.5px (1px on screens that don't subpixel-render):

```css
.hairline {
  border: 0.5px solid var(--color-line);
}
@media (-webkit-min-device-pixel-ratio: 1.5) {
  /* hi-DPI: 0.5px renders correctly */
}
@media (-webkit-max-device-pixel-ratio: 1) {
  .hairline { border-width: 1px; }
}
```

Some browsers round 0.5px to 0px. Defensive fallback: ship `border: 1px solid var(--color-line)` and let the muted color do the work. The reader won't notice the difference.

---

## 4. Components

### 4.1 Header

```html
<header class="app-header">
  <div class="container header-grid">
    <a class="brand" href="#/home">
      <span class="brand-mark lang-ja">五</span>
      <span class="brand-name">JLPT N5</span>
    </a>
    <nav class="primary-nav">
      <a href="#/learn">Learn</a>
      <a href="#/test">Test</a>
    </nav>
    <div class="header-tools">
      <input type="search" placeholder="Search">
      <button aria-label="Settings" class="icon-btn"><!-- settings SVG --></button>
    </div>
  </div>
</header>
```

```css
.app-header {
  position: sticky; top: 0; z-index: 50;
  background: var(--color-bg);
  border-bottom: 0.5px solid var(--color-line);
}
.header-grid {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: var(--space-6);
  height: 56px;
  padding: 0 var(--space-5);
  max-width: var(--container-wide);
  margin: 0 auto;
}
.brand {
  display: flex; align-items: center; gap: var(--space-2);
  text-decoration: none; color: var(--color-text);
}
.brand-mark {
  display: inline-flex; align-items: center; justify-content: center;
  width: 24px; height: 24px;
  font-size: 16px; font-weight: var(--weight-base);
  color: var(--color-text);
  border: 0.5px solid var(--color-line);
  border-radius: var(--radius-sm);
}
.brand-name {
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  letter-spacing: var(--tracking-wide);
}
.primary-nav {
  display: flex; justify-content: center;
  gap: var(--space-6);
}
.primary-nav a {
  position: relative;
  font-size: var(--text-sm);
  font-weight: var(--weight-base);
  color: var(--color-text-muted);
  text-decoration: none;
  padding: var(--space-2) 0;
  transition: color 150ms ease;
}
.primary-nav a:hover { color: var(--color-text); }
.primary-nav a.active { color: var(--color-text); }
.primary-nav a.active::after {
  content: "";
  position: absolute;
  left: 0; right: 0; bottom: -1px;
  height: 1.5px;
  background: var(--color-accent);
}
.badge {
  display: inline-block;
  margin-left: 6px;
  font-size: var(--text-2xs);
  font-weight: var(--weight-medium);
  color: var(--color-due);
  background: var(--color-due-tint);
  padding: 1px 6px;
  border-radius: var(--radius-pill);
  font-variant-numeric: tabular-nums;
}
.header-tools {
  display: flex; align-items: center; gap: var(--space-3);
}
.header-tools input[type="search"] {
  width: 180px;
  height: 32px;
  padding: 0 var(--space-3);
  font-size: var(--text-sm);
  background: var(--color-surface);
  border: 0.5px solid var(--color-line);
  border-radius: var(--radius-md);
  color: var(--color-text);
}
.header-tools input[type="search"]:focus {
  outline: none;
  border-color: var(--color-line-strong);
  background: var(--color-bg);
}
.icon-btn {
  width: 32px; height: 32px;
  display: inline-flex; align-items: center; justify-content: center;
  background: transparent;
  border: 0.5px solid transparent;
  border-radius: var(--radius-md);
  color: var(--color-text-muted);
  cursor: pointer;
}
.icon-btn:hover { background: var(--color-surface); color: var(--color-text); }
```

The brand mark is a small 24px square box containing a Japanese character (五 = "5"). It anchors the wordmark with cultural specificity and costs nothing.

### 4.2 Buttons

Three variants. Use them strictly.

```css
.btn {
  display: inline-flex; align-items: center; justify-content: center;
  height: 36px;
  padding: 0 var(--space-4);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  border-radius: var(--radius-md);
  border: 0.5px solid transparent;
  cursor: pointer;
  transition: background 150ms ease, color 150ms ease, border-color 150ms ease;
  font-family: inherit;
}
.btn:focus-visible {
  outline: 2px solid var(--color-accent);
  outline-offset: 2px;
}

/* Primary - the action the page wants you to take. ONE per page max. */
.btn-primary {
  background: var(--color-accent);
  color: #FFFFFF;
}
.btn-primary:hover { background: var(--color-accent-hover); }

/* Secondary - the "alternate path" action. */
.btn-secondary {
  background: var(--color-bg);
  color: var(--color-text);
  border-color: var(--color-line);
}
.btn-secondary:hover {
  border-color: var(--color-line-strong);
  background: var(--color-surface);
}

/* Ghost - tertiary actions. Looks like a styled link with breathing room. */
.btn-ghost {
  background: transparent;
  color: var(--color-text-muted);
}
.btn-ghost:hover { color: var(--color-text); }

/* Sizes */
.btn-sm { height: 28px; padding: 0 var(--space-3); font-size: var(--text-xs); }
.btn-lg { height: 44px; padding: 0 var(--space-5); font-size: var(--text-base); }
```

### 4.3 Cards

```css
.card {
  background: var(--color-surface);
  border: 0.5px solid var(--color-line);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  transition: background 150ms ease, border-color 150ms ease;
}
.card-link {
  display: block;
  text-decoration: none;
  color: inherit;
  cursor: pointer;
}
.card-link:hover {
  background: var(--color-surface-alt);
  border-color: var(--color-line-strong);
}
.card-link:hover .card-action {
  text-decoration: underline;
}
.card-title {
  font-size: var(--text-md);
  font-weight: var(--weight-medium);
  margin: 0 0 var(--space-2);
  color: var(--color-text);
}
.card-meta {
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  margin: 0;
  line-height: var(--leading-base);
}
.card-action {
  display: inline-block;
  margin-top: var(--space-4);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  color: var(--color-text);
}
```

Note the card hover state: the card lightens to `surface-alt` and the border darkens slightly. NO shadow, NO transform, NO scale. The lightening alone signals interactivity.

### 4.4 Numbered indicator

A signature Muji-style affordance. Use on cards in a sequence (Learn modules, Test sections).

```html
<article class="card card-link">
  <p class="card-index">01</p>
  <h3 class="card-title">Grammar</h3>
  <p class="card-meta">187 patterns across 32 categories.</p>
  <p class="card-action">Browse</p>
</article>
```

```css
.card-index {
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  letter-spacing: var(--tracking-label);
  color: var(--color-text-faint);
  margin: 0 0 var(--space-3);
  font-variant-numeric: tabular-nums;
}
```

The 2-digit zero-padded number does enormous work. It signals "this is part of a curated set" and creates a visual anchor at top-left of every card.

### 4.5 Pills and badges

```css
.pill {
  display: inline-flex; align-items: center;
  height: 22px;
  padding: 0 var(--space-2);
  font-size: var(--text-2xs);
  font-weight: var(--weight-medium);
  letter-spacing: var(--tracking-wide);
  border-radius: var(--radius-pill);
  background: var(--color-surface);
  color: var(--color-text-muted);
  border: 0.5px solid var(--color-line);
}
.pill-accent  { background: var(--color-accent-tint);  color: var(--color-accent);  border-color: transparent; }
.pill-correct { background: var(--color-correct-tint); color: var(--color-correct); border-color: transparent; }
.pill-due     { background: var(--color-due-tint);     color: var(--color-due);     border-color: transparent; }
```

Pills are for STATUS only. Don't use them as decoration.

### 4.6 Progress bars

```html
<div class="progress" role="progressbar" aria-valuenow="42" aria-valuemax="100">
  <div class="progress-fill" style="width: 42%"></div>
</div>
```

```css
.progress {
  height: 2px;
  background: var(--color-line);
  border-radius: var(--radius-pill);
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: var(--color-accent);
  transition: width 400ms ease;
}
```

2px is correct. Anything thicker reads as a "feature," not a hint. The progress bar should be present but barely there.

### 4.7 Form controls

```css
input[type="text"],
input[type="search"],
input[type="email"],
textarea,
select {
  width: 100%;
  height: 40px;
  padding: 0 var(--space-3);
  font-family: inherit;
  font-size: var(--text-base);
  color: var(--color-text);
  background: var(--color-bg);
  border: 0.5px solid var(--color-line);
  border-radius: var(--radius-md);
  transition: border-color 150ms ease;
}
input:focus,
textarea:focus,
select:focus {
  outline: none;
  border-color: var(--color-accent);
}
textarea { height: auto; padding: var(--space-3); min-height: 96px; }

label {
  display: block;
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  color: var(--color-text);
  margin-bottom: var(--space-2);
}
```

### 4.8 Tables

Used for vocabulary lists, conjugation tables, kanji readings.

```css
.table {
  width: 100%;
  border-collapse: collapse;
  font-size: var(--text-sm);
}
.table th {
  text-align: left;
  font-weight: var(--weight-medium);
  font-size: var(--text-2xs);
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
  color: var(--color-text-muted);
  padding: var(--space-2) var(--space-3);
  border-bottom: 0.5px solid var(--color-line);
}
.table td {
  padding: var(--space-3);
  border-bottom: 0.5px solid var(--color-line);
  vertical-align: top;
}
.table tr:last-child td { border-bottom: none; }
.table tr:hover td { background: var(--color-surface); }
```

No vertical borders. No striping. Rows separated by hairlines only.

---

## 5. Page-by-page treatments

### 5.1 Home (landing)

Layout:

```
┌─────────────────────────────────────────────────────┐
│ [header, sticky]                                     │
├─────────────────────────────────────────────────────┤
│                                                      │
│   [container 880px, centered, top margin 96px]      │
│                                                      │
│   JLPT N5 study material.                           │  <- text-2xl, weight 300
│                                                      │
│   [space-5]                                          │
│   187 grammar patterns.                              │  <- text-base, default
│   1,003 vocabulary items.                            │     weight, one line each
│   106 kanji.                                         │
│   30 reading passages.                               │
│   12 listening drills.                               │
│                                                      │
│   [space-12]                                         │
│   ── SECTIONS ─────────────────────────────────       │
│                                                      │
│   [space-6]                                          │
│   ┌─────────────────────────┐ ┌─────────────────────┐│
│   │ 01                      │ │ 02                  ││
│   │                         │ │                     ││
│   │ Learn                   │ │ Test                ││
│   │ Grammar, vocabulary,    │ │ 15-question mock    ││
│   │ kanji, reading,         │ │ exam.               ││
│   │ listening.              │ │                     ││
│   │                       → │ │                   → ││
│   └─────────────────────────┘ └─────────────────────┘│
│                                                      │
│   [space-6]                                          │
│   Placement check available.                         │  <- inline link
│                                                      │
└──────────────────────────────────────────────────────┘
```

Specific rules for this page:

- The headline is a single noun phrase terminated by a period: `JLPT N5 study material.` Not a verb phrase. No subtitle.
- Below the headline, render a five-line inventory. Each line is a numeral plus a noun phrase plus a period. Lines are stacked, not bulleted. Do not use middle-dots between items. Do not add a heading above this list.
- Counts in the inventory must be read at runtime from `data/*.json` `_meta.entity_count` fields (or equivalent). Do not hardcode. If a count changes by one, the homepage updates automatically.
- Use comma as thousands separator for 4+ digit numbers (`1,003`). Bare digits otherwise.
- No primary CTA button. No "Start your first lesson", no "Take the placement check" as a green button. The cards in the SECTIONS grid are the entry points.
- No trust line. Do not render `Works offline · No login required · Stays on device` on the homepage. Those properties live in About / Privacy.
- No "What's new" callout, no "New!" badges, no version chip.
- Returning users (when `localStorage` shows progress) get a single resume strip ABOVE the SECTIONS label. Format: `Last session: [section name], [topic]. [N] of [M].` The whole line is a link to the resumption point. No "continue", no "resume", no exclamation. Hide the strip entirely for first-time visitors. No fallback.
- Section labels (`SECTIONS`) use `.section-label` from §5.1 unchanged.
- Two cards in the grid, full-width 50/50 on desktop, stacked on mobile. Each card has the standard structure: index number, h3 title, single-sentence body terminated by a period, `→` chevron right-aligned. No "Browse" text label.
- Below the cards: a single inline sentence `Placement check available.` The whole sentence is a link to `/placement`. Link styling uses `--color-text` with a hairline underline on hover only. Not browser-default purple/blue.

```css
.section-label {
  display: flex; align-items: center; gap: var(--space-3);
  margin-bottom: var(--space-6);
}
.section-label-text {
  font-size: var(--text-2xs);
  letter-spacing: var(--tracking-label);
  text-transform: uppercase;
  color: var(--color-text-muted);
  font-weight: var(--weight-medium);
}
.section-label-rule {
  flex: 1;
  height: 0.5px;
  background: var(--color-line);
}
```

### 5.1.1 Copy register (mandatory)

The homepage is the most-seen surface in the app. Its copy sets the
register for everything else. The rules:

1. Describe the contents. Offer no opinion about them.
2. No outcome claims. The product is a study material, not a promise.
3. No second-person ("you", "your"). Use noun phrases or impersonal sentences.
4. No verbs of encouragement ("start", "begin", "explore", "discover").
5. No trust reassurance ("works offline", "no login", "privacy-first") on the homepage. Those properties live in About / Privacy.
6. No service-encounter politeness ("please", "feel free to").
7. Counts are bare numerals plus nouns. No "~1000", no "1000+", no "carefully selected", no "all".
8. No superlatives: best, most comprehensive, complete, definitive.
9. No flattering self-description: clean, minimal, elegant, distraction-free. The design demonstrates these; the copy must not assert them.
10. Sentence case throughout. ALL CAPS only for the small letter-spaced section labels.

If a proposed homepage string violates any of these, the string is wrong.

The same register applies to all homepage variants: light mode, dark mode, mobile, returning-user, and translated locales.

### 5.2 Learn index

The page shown in the screenshot you uploaded. Specific changes:

- Drop the grouped "REFERENCE" and "PRACTICE" labels into the hairline-rule treatment from above.
- Numbered cards (01-05).
- Each card has, in vertical order: index number, h3 title, meta line (one line, no wrapping), the same 2px progress bar showing % completion of that module, then "Browse" as a small text action.
- The five modules in suggested visual order: Grammar (01), Vocabulary (02), Kanji (03), Reading (04), Listening (05). This is reading-frequency order, not screen-grid-symmetry order.

```html
<article class="card card-link" href="#/learn/grammar">
  <p class="card-index">01</p>
  <h3 class="card-title">Grammar</h3>
  <p class="card-meta">187 patterns across 32 categories.</p>
  <div class="progress" style="margin-top: var(--space-3)">
    <div class="progress-fill" style="width: 42%"></div>
  </div>
  <p class="card-action">Browse</p>
</article>
```

### 5.3 Grammar pattern detail

The most type-heavy page. This is where the design earns its keep.

```
┌─────────────────────────────────────────────┐
│ ← Back to Grammar                            │  <- ghost link
│                                              │
│ TE-FORM                                      │  <- label, ALL CAPS
│ ～て                                         │  <- text-2xl, ja, weight 400
│ Connecting form for verbs                    │  <- text-md, muted
│                                              │
│ ── form ─────────────────                    │
│                                              │
│ Group 1   う/つ/る → って   買う → 買って   │  <- table
│ Group 1   む/ぬ/ぶ → んで   飲む → 飲んで   │
│ Group 1   く → いて (行く → 行って)         │
│ Group 1   ぐ → いで         泳ぐ → 泳いで   │
│ Group 1   す → して         話す → 話して   │
│ Group 2   drop る + て      食べる → 食べて │
│ Irreg     する → して, 来る → 来て           │
│                                              │
│ ── examples ────────────                     │
│                                              │
│ 1.  ご飯を食べて、コーヒーを飲みます。        │
│     I eat a meal and then drink coffee.     │
│     [▷ play audio]                           │
│                                              │
│ 2.  本を読んで、寝ます。                      │
│     I read a book and go to sleep.          │
│     [▷ play audio]                           │
│                                              │
│ ── common mistakes ──────                    │
│                                              │
│ Wrong  たべるて                               │
│ Right  たべて                                 │
│        Drop る before adding て.              │
│                                              │
└─────────────────────────────────────────────┘
```

Specifics:

- The pattern form (`～て`) is rendered LARGE in `--text-2xl` weight 400, in a small dedicated block at the top with `--space-5` of breathing room below it.
- "TE-FORM" small label above the form is in the page-kind label style.
- Section dividers use the hairline-rule pattern from §5.1 with lowercase ja-romaji labels: `form`, `examples`, `common mistakes`.
- Examples are NUMBERED (1, 2, 3) in the type, not bulleted. Use an `<ol class="example-list">`.
- Audio play affordance is a small `▷` character on its own line, muted color, treated like a footnote.
- Common mistakes use a 2-column micro-table: "Wrong" / "Right" labels in `--color-incorrect` and `--color-correct`, then the explanation as muted body text below.

```css
.pattern-form {
  font-family: var(--font-jp);
  font-size: var(--text-2xl);
  font-weight: var(--weight-base);
  margin: var(--space-2) 0;
  letter-spacing: 0;
}
.example-list {
  list-style: none;
  counter-reset: example;
  padding: 0;
  margin: 0;
}
.example-list > li {
  counter-increment: example;
  padding: var(--space-4) 0;
  border-bottom: 0.5px solid var(--color-line);
  display: grid;
  grid-template-columns: 28px 1fr;
  gap: var(--space-3);
}
.example-list > li::before {
  content: counter(example) ".";
  color: var(--color-text-faint);
  font-variant-numeric: tabular-nums;
  font-size: var(--text-sm);
}
.example-ja { font-family: var(--font-jp); font-size: var(--text-md); margin: 0 0 var(--space-1); }
.example-en { font-size: var(--text-sm); color: var(--color-text-muted); margin: 0; }
```

### 5.4 Vocabulary index

Two-column layout:

- Left rail (240px): list of thematic sections (Family, Time, Food, etc.) with item counts. Click to filter the right pane.
- Right pane: searchable list of vocab as a table (kanji form, kana, romaji, English meaning, audio).

```css
.vocab-layout {
  display: grid;
  grid-template-columns: 220px 1fr;
  gap: var(--space-8);
  max-width: var(--container-wide);
}
.vocab-rail {
  position: sticky; top: 80px; align-self: start;
}
.vocab-rail-list { list-style: none; padding: 0; margin: 0; }
.vocab-rail-list a {
  display: flex; justify-content: space-between;
  padding: var(--space-2) 0;
  font-size: var(--text-sm);
  color: var(--color-text-muted);
  text-decoration: none;
  border-bottom: 0.5px solid var(--color-line);
}
.vocab-rail-list a.active { color: var(--color-text); font-weight: var(--weight-medium); }
.vocab-rail-list a .count { color: var(--color-text-faint); font-variant-numeric: tabular-nums; }
```

The vocab table itself uses the `.table` styles from §4.8.

### 5.5 Kanji index

A grid of square tiles, 6 columns desktop, 4 columns tablet, 3 columns mobile. Each tile shows the kanji glyph at large size with on/kun in tiny text below.

```css
.kanji-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
  gap: var(--space-3);
}
.kanji-tile {
  aspect-ratio: 1;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: var(--space-3);
  background: var(--color-surface);
  border: 0.5px solid var(--color-line);
  border-radius: var(--radius-md);
  cursor: pointer;
  transition: background 150ms ease;
  text-decoration: none; color: inherit;
}
.kanji-tile:hover { background: var(--color-surface-alt); }
.kanji-tile-glyph {
  font-family: var(--font-jp);
  font-size: 56px;
  line-height: 1;
  color: var(--color-text);
  font-weight: var(--weight-base);
  margin-bottom: var(--space-3);
}
.kanji-tile-meaning {
  font-size: var(--text-2xs);
  color: var(--color-text-muted);
  text-align: center;
}
```

The hover state lightens but never colors. Click opens a detail page, not a modal.

### 5.6 Practice / drill

This is the screen the user sees most. It must be clean.

Single card, centered, max-width 560px:

```html
<div class="drill-frame">
  <div class="drill-meta">
    <span class="drill-progress">7 / 20</span>
    <div class="progress" style="flex: 1">
      <div class="progress-fill" style="width: 35%"></div>
    </div>
    <button class="btn-ghost btn-sm">Quit</button>
  </div>

  <div class="drill-question lang-ja">
    わたし<span class="blank">（　）</span>がくせいです。
  </div>

  <div class="drill-choices">
    <button class="drill-choice lang-ja"><kbd>1</kbd> は</button>
    <button class="drill-choice lang-ja"><kbd>2</kbd> が</button>
    <button class="drill-choice lang-ja"><kbd>3</kbd> を</button>
    <button class="drill-choice lang-ja"><kbd>4</kbd> に</button>
  </div>
</div>
```

```css
.drill-frame { max-width: 560px; margin: var(--space-10) auto; }
.drill-meta {
  display: flex; align-items: center; gap: var(--space-4);
  margin-bottom: var(--space-10);
}
.drill-progress {
  font-size: var(--text-xs); color: var(--color-text-muted);
  font-variant-numeric: tabular-nums;
  letter-spacing: var(--tracking-wide);
}
.drill-question {
  font-family: var(--font-jp);
  font-size: 28px;       /* slightly larger than --text-xl, optical adjustment for ja */
  font-weight: var(--weight-base);
  line-height: var(--leading-loose);
  text-align: center;
  margin: var(--space-12) 0;
  color: var(--color-text);
}
.drill-question .blank {
  color: var(--color-text-faint);
  font-weight: var(--weight-medium);
}
.drill-choices {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-3);
}
.drill-choice {
  position: relative;
  display: flex; align-items: center; justify-content: center;
  height: 56px;
  padding: 0 var(--space-4);
  background: var(--color-bg);
  border: 0.5px solid var(--color-line);
  border-radius: var(--radius-md);
  font-family: var(--font-jp);
  font-size: var(--text-md);
  font-weight: var(--weight-base);
  color: var(--color-text);
  cursor: pointer;
  transition: all 150ms ease;
}
.drill-choice:hover { border-color: var(--color-line-strong); background: var(--color-surface); }
.drill-choice kbd {
  position: absolute;
  top: 8px; left: 10px;
  font-family: var(--font-en);
  font-size: var(--text-2xs);
  color: var(--color-text-faint);
  font-weight: var(--weight-medium);
  background: transparent;
  border: none;
  padding: 0;
}
.drill-choice.correct {
  border-color: var(--color-correct);
  background: var(--color-correct-tint);
  color: var(--color-correct);
}
.drill-choice.incorrect {
  border-color: var(--color-incorrect);
  background: var(--color-incorrect-tint);
  color: var(--color-incorrect);
}
```

Notes:

- Vast vertical breathing room between the question and the choices: `--space-12` = 96px. The empty space is the design.
- Keyboard hint (`kbd` element) shows in the corner of each choice. After the user uses the keyboard once, they're hinted forever.
- Feedback is INSTANT and color-only. No animations, no shake. The chosen button colors itself; the correct one (if user was wrong) colors itself green. A small explanatory text appears below.

### 5.7 Review (SRS) queue

Like Practice, but with a status strip across the top:

```html
<div class="review-strip">
  <div class="review-stat"><span class="review-stat-num">12</span><span class="review-stat-label">due</span></div>
  <div class="review-stat"><span class="review-stat-num">3</span><span class="review-stat-label">learning</span></div>
  <div class="review-stat"><span class="review-stat-num">217</span><span class="review-stat-label">mature</span></div>
  <div class="review-time">approx. 4 min</div>
</div>
```

```css
.review-strip {
  display: flex; align-items: center; gap: var(--space-6);
  padding: var(--space-3) 0;
  border-bottom: 0.5px solid var(--color-line);
  margin-bottom: var(--space-10);
}
.review-stat {
  display: flex; align-items: baseline; gap: var(--space-2);
}
.review-stat-num {
  font-size: var(--text-md);
  font-weight: var(--weight-medium);
  font-variant-numeric: tabular-nums;
  color: var(--color-text);
}
.review-stat-label {
  font-size: var(--text-xs);
  color: var(--color-text-muted);
  letter-spacing: var(--tracking-wide);
}
.review-time {
  margin-left: auto;
  font-size: var(--text-xs);
  color: var(--color-text-faint);
  font-variant-numeric: tabular-nums;
}
```

Empty state when no reviews are due:

```
[centered, max-width 480px, top-margin 128px]

  All caught up

  No reviews are due right now. Come back
  in 4 hours, or start a new lesson.

  [ Start a new lesson ]   [ Practice anyway ]
```

The empty state uses `--text-2xl` weight 300 for "All caught up", muted body for the explanation, and a primary + secondary button row.

### 5.8 Test

Test mode looks subtly different from Practice. The user should feel the formality.

- Background of the test header is `--color-surface` (slightly off-white) instead of pure white. Tiny cue that this is a different mode.
- Timer in the header, monospaced, prominent: `font-family: var(--font-num); font-variant-numeric: tabular-nums;`.
- Question card has a slightly thicker top edge (1.5px in `--color-text` color) to mark it as authoritative.
- "Submit" button replaces the "Continue" button - it's the same primary button but with that label.
- No immediate per-question feedback. Answers are recorded and reviewed at the end.

### 5.9 Summary / dashboard

This is the page that has the most numbers. The Muji discipline is to NOT show all of them.

Top of page: one big stat - total mastery percentage - in `--text-2xl` weight 300.

Below it: a 5-row "mastery ladder" showing each of the five modules with a 2px progress bar each.

Below that: a single "Weak spots" panel listing the user's three worst categories with a "Drill these" CTA.

Below that: a 7×53 GitHub-style heatmap of daily activity, using a single-color ramp (`--color-accent-tint` to `--color-accent`).

That's the entire page. No "achievements", no "trophies", no XP, no level. The Muji approach is "you've done this much; here's what's weak; go practice."

### 5.10 Settings

Single-column, max-width 640px. Sectioned by category. Each setting on its own row, label on left, control on right, with a hairline below.

```css
.setting-row {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: center;
  gap: var(--space-4);
  padding: var(--space-4) 0;
  border-bottom: 0.5px solid var(--color-line);
}
.setting-label { font-size: var(--text-base); font-weight: var(--weight-base); margin: 0; }
.setting-help { font-size: var(--text-sm); color: var(--color-text-muted); margin: 4px 0 0; }
.setting-control { justify-self: end; }
```

Destructive actions (Reset progress) at the bottom, separated by `--space-8` of whitespace, with a thin top border in `--color-incorrect` and a small label "Danger zone" in muted text.

### 5.11 Footer

```html
<footer class="app-footer">
  <div class="container footer-grid">
    <p class="footer-meta">v1.8.10</p>
    <nav class="footer-nav">
      <a href="#/changelog">What's new</a>
      <a href="#/about">About</a>
      <a href="#/privacy">Privacy</a>
      <a href="https://github.com/...">Source</a>
    </nav>
  </div>
</footer>
```

The version number must be read at runtime (e.g., from `package.json` or a build-time constant), not hardcoded. The "Updated [Month Year]" suffix from earlier drafts is dropped — the changelog link replaces that affordance. "What's new" links to the in-app `#/changelog` route which renders the markdown changelog with the app's typography; never to a raw `.md` file on GitHub.

```css
.app-footer {
  border-top: 0.5px solid var(--color-line);
  padding: var(--space-5) 0;
  margin-top: var(--space-16);
}
.footer-grid {
  display: flex; justify-content: space-between; align-items: center;
  font-size: var(--text-xs);
  color: var(--color-text-muted);
}
.footer-nav {
  display: flex; gap: var(--space-5);
}
.footer-nav a { color: var(--color-text-muted); text-decoration: none; }
.footer-nav a:hover { color: var(--color-text); }
```

---

## 6. Furigana

Use semantic `<ruby>`:

```html
<ruby>日本語<rt>にほんご</rt></ruby>
```

```css
ruby { ruby-position: over; }
ruby rt {
  font-size: 0.55em;
  color: var(--color-text-muted);
  font-weight: var(--weight-base);
  font-family: var(--font-jp);
  letter-spacing: 0;
}
.furigana-off rt { display: none; }
.furigana-known rt { visibility: hidden; }   /* preserves space, hides reading */
```

The toggle hides ruby via CSS class on `<body>`. No re-render needed.

---

## 7. Iconography

Use a small, consistent SVG icon set. Recommendation: lucide-icons subset (search, settings, play, pause, chevron-right, x, check, alert-circle, refresh-cw). Stroke width 1.5px to match the hairline aesthetic; the default 2px lucide stroke is too heavy.

```css
svg.icon {
  width: 16px; height: 16px;
  stroke-width: 1.5;
  color: currentColor;
}
svg.icon-sm { width: 14px; height: 14px; }
svg.icon-lg { width: 20px; height: 20px; }
```

No icon should be larger than 24px in any UI surface except the kanji-tile glyph (which isn't an icon, it's content).

NO emojis. NO decorative icons in body text. NO colored icons.

---

## 8. Motion

Movement is minimal and purposeful.

```css
:root {
  --motion-fast:   120ms;
  --motion-base:   180ms;
  --motion-slow:   300ms;
  --easing:        cubic-bezier(0.2, 0, 0, 1);   /* iOS-like ease-out */
}
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

Allowed motion:

- Hover state transitions: `--motion-fast` ease-out on background and border
- Button press: scale to 0.98 for `--motion-fast`
- Progress bar fill: `--motion-slow` width transition
- Page transitions: cross-fade only, `--motion-base`. No slide, no zoom.

Forbidden motion:

- Bouncy springs
- Confetti
- Card lift / shadow on hover
- Wiggle, shake, pulse, glow
- Sliding panes
- Fading in entire pages from blank

---

## 9. Imagery and ornament

The Muji approach uses almost no imagery. What it permits:

- A single Japanese character as a brand mark or watermark (very low opacity). Used once on the home hero, optionally.
- The kanji glyphs in the Kanji index are the only "imagery" most pages need.
- Stroke-order diagrams in kanji detail pages: SVG, single-stroke, animated only on user click.

Forbidden:

- Photos of any kind (people studying, Tokyo skylines, sushi).
- Stock illustrations.
- Decorative patterns or textures.
- Backgrounds with visible color (everything is `--color-bg` or `--color-surface`).
- Brand mascot.
- Cherry blossoms. Especially cherry blossoms.

The product is the type, the spacing, and the hairlines. Adding decoration weakens the design.

---

## 10. Responsive behavior

### 10.1 Breakpoints

```css
/* Mobile first. Defaults are mobile. */
:root { /* mobile defaults */ }

@media (min-width: 600px) { /* tablet */ }
@media (min-width: 960px) { /* desktop */ }
@media (min-width: 1280px) { /* wide desktop */ }
```

### 10.2 Mobile rules

- Header height shrinks to 48px.
- Primary nav becomes a bottom tab bar on mobile.
- Card grids stack to single column.
- All cards retain their numbered index (it works at any width).
- Drill choices stay in a 2x2 grid (don't stack vertically).
- Vocab two-column layout collapses: rail becomes a horizontal scrollable chip strip at top.
- Footer stacks vertically.
- Page padding reduces from 32px to 20px on mobile.

### 10.3 Tap targets

Every interactive element must be at least 44x44 CSS pixels. Don't shrink buttons on mobile; shrink the layout around them.

---

## 11. Accessibility

Non-negotiable. WCAG 2.1 AA.

- Color contrast: minimum 4.5:1 for body text against background. The token combinations above are pre-verified.
- Focus rings: every interactive element has a visible focus ring (2px accent color, 2px offset).
- Keyboard navigation: tab order matches visual order. Esc closes modals. Arrow keys cycle drill choices.
- Screen readers: every Japanese text container has `lang="ja"`. Furigana via `<ruby>` works correctly with VoiceOver/NVDA.
- Motion: all animations respect `prefers-reduced-motion`.
- Form labels: every input has an associated `<label>`.
- Headings: one `<h1>` per page; nested headings don't skip levels.

---

## 12. Implementation checklist

For the developer building this:

- [ ] Set up CSS custom properties in `:root` with all tokens from §1, §2, §3.
- [ ] Implement dark mode media query block with full parity (§1.2).
- [ ] Load Inter (300, 400, 500) and Noto Sans JP (400, 500) via woff2.
- [ ] Subset Noto Sans JP to N5 + N4 character ranges.
- [ ] Preload critical fonts in `<head>`.
- [ ] Build header component (§4.1) and reuse on every page.
- [ ] Build button variants (§4.2). Audit codebase: no other button styles exist.
- [ ] Build card component (§4.3) with link variant.
- [ ] Build form controls (§4.7), section labels with hairline rule (§5.1).
- [ ] Implement furigana via `<ruby>` everywhere.
- [ ] Audit: no emoji, no shadows, no gradients, no decorative icons in body text.
- [ ] Audit: no font weight 600 or 700 anywhere.
- [ ] Test in light and dark mode at every page.
- [ ] Test on mobile 375px, tablet 768px, desktop 1280px.
- [ ] Run Lighthouse: Accessibility >= 95.

---

## 13. What this design is and is not

**It is:**
- Quiet, slow, considered.
- Built to look right after 100 hours of use, not in the App Store screenshot.
- Heavily reliant on disciplined typography and whitespace.
- A reflection of a real Japanese aesthetic tradition (Muji, MoMA, Kinokuniya).

**It is not:**
- Friendly, warm, gamified, or "fun."
- Designed for users who want streaks, badges, XP, or push notifications.
- Forgiving of half-hearted execution. A 70% implementation will look worse than the current bland design. Either commit fully or pick a more forgiving theme.

If you can't ship it at 95% fidelity to this spec, ship something more forgiving. This design works because of its discipline. Halfway is worse than starting over.

---

*End of design system.*
