# JLPT N5 Tutor - UI-Level Testing Plan

**Site under test:** https://gauravaccentureproducts.github.io/jlpt-n5-tutor/
**Local:** `index.html` served from project root (any static file server).
**Last updated:** 2026-04-30 (synced to UX Brief 2 Phases 1-4 + Learn hub + per-vocab detail; SW `jlpt-n5-tutor-v18`)
**Scope:** End-to-end UI testing of the deployed web app from every reasonable perspective. Engine-layer unit tests (currently 37/37 in `tests.html`) are out of scope here - this document covers what those tests cannot reach.

> **★ Foundational principle:** This app's purpose is to teach **correct Japanese**. Every other concern in this plan (performance, accessibility, design, even cross-browser support) is subordinate. **§12 - Japanese language accuracy & content integrity** is the bar this app must clear; it is enforced as a hard CI release blocker (§12.1), spot-checked at every release (§12.2), and re-audited quarterly (§12.3). Read §12 first. Everything else follows.

---

## 0. How to use this plan

Each section below names a **perspective**, the **questions** that perspective asks, the **specific tests** to run, and (where useful) the **tool** that automates it.

The plan is intentionally large because the app has 17 routes × multiple sub-paths × 5 locales × multiple input modalities. Triage by:

1. **P0 - Smoke (5 min, every release):** §17.1
2. **P1 - Pre-release gate (60 min, every release):** §17.2 (extends existing gate in `TASKS.md`)
3. **P2 - Full regression (one full session, every milestone):** §17.3
4. **P3 - Deep-dive perspectives (ad-hoc / quarterly):** §1-§16

Treat §1-§16 as a **catalog of perspectives**. Pick the ones that match the change you just shipped.

### 0.1 Route map (current)

| Route | Renders | Notes |
|---|---|---|
| `#/home` | Landing - first-time vs returning state, 3 pillar cards, streak heatmap | default route |
| `#/learn` | **5-card hub** (Grammar, Vocabulary, Kanji, Dokkai, Listening) | new in Brief 2 |
| `#/learn/grammar` | 187 grammar cards across 32 categories | sub-path |
| `#/learn/vocab` | 1002 vocab cards across 40 sections | sub-path |
| `#/learn/vocab/<form>` | Per-word detail (form / reading / gloss / 5 example sentences) | sub-path |
| `#/learn/<patternId>` | Pattern detail (existing) | sub-path |
| `#/kanji` | 106 kanji cards (glyph + meaning + readings) | sub-path |
| `#/kanji/<glyph>` | Per-kanji detail | sub-path |
| `#/test` / `#/test/<n>` | Mock exam setup / direct-launch (n ∈ 20/30/50) | quit-prompt protected |
| `#/drill` (Practice) | Daily mixed drill | renamed from "Daily Drill" |
| `#/review` | SM-2 SRS session | |
| `#/summary` | Diagnostic dashboard | |
| `#/diagnostic` | Placement check | |
| `#/settings` | UI lang / theme / font / 3-mode furigana / audio speed / reduce motion / typed-phrase reset / export / import | |
| `#/reading` | 30 graded passages | |
| `#/listening` | 12 listening items (3 formats) | |
| `#/kosoado` `#/waga` `#/verbclass` `#/teform` `#/particles` `#/counters` | Topic deep-dives | |

---

## 1. End-learner perspective (the target user)

The whole app exists for this person. Every other perspective is in service of it.

**Persona:** Adult self-studier, has 10-30 minutes a day, wants to pass N5. Has tried Duolingo / Anki / Memrise / Bunpro and is skeptical.

### 1.1 The "first lesson" journey

| Step | What to verify |
|---|---|
| Land on home | First-time CTA "Start your first lesson" is above the fold. Trust strip ("Works offline / No login / Progress stays on this device") is visible without scrolling. No login wall. |
| Click "Start your first lesson" | Routes to `#/learn` hub showing 5 cards: Grammar / Vocabulary / Kanji / Dokkai (Reading) / Listening. |
| Click "Grammar" card | Routes to `#/learn/grammar`; 187 pattern cards in 32 categories; back link visible. |
| Click any pattern card | Routes to `#/learn/<patternId>`; detail shows pattern + EN meaning + JA meaning (`意味（やさしい にほんご）`) + ≥1 example with EN translation + audio player. |
| Click any kanji glyph in the lesson | Popover opens with on/kun/meaning + "I know this kanji" toggle. |
| Toggle "I know this kanji" | Popover closes; ruby on that kanji disappears (when furigana mode is `hide-known`). Persists in localStorage `knownKanji`. |
| Read explanation | Explanation is in the user's locale. No untranslated keys. No "Lorem ipsum." |
| Hit a practice question | Question shows. 4 options. Tap or press 1-4. Drill shows immediate feedback; Test deliberately end-of-test. |
| Get a wrong answer | Feedback is encouraging, not punishing. Shows the correct answer with explanation. |
| Finish a lesson | Progress is saved. Streak record updates. Returning to home shows the Continue card. |

**Acceptance:** A new user can complete a lesson without reading any documentation.

### 1.2 The "did I really learn it" journey

| Step | What to verify |
|---|---|
| Complete 5 lessons | Daily Drill / Review queue starts populating |
| Wait 24 hours (or simulate via system clock) | Review queue surfaces yesterday's items at correct intervals |
| Get an item wrong in review | SRS demotes it; it appears again sooner |
| Get an item right 3+ times | Interval grows per SM-2 |
| After a week | Diagnostic page shows error patterns and weak areas |

**Acceptance:** SRS schedule matches SM-2 algorithm (verified in `tests.html`); UI surfaces what's due, what's overdue, and what's mastered.

### 1.3 Test-mode honesty

| Step | What to verify |
|---|---|
| Start a 20-question mock test | Questions are randomized; no obvious pattern bias |
| Complete the test | Score, time taken, weak areas shown |
| Repeat the test | Different question order; no repeated questions back-to-back |
| Fail badly | Recommended-next-session points to the weak area, not generic advice |

**Acceptance:** The user can take 5 mock tests and the experience feels different each time.

---

## 2. First-time-visitor perspective

**Question:** "What is this site? Should I trust it? How do I start?"

| Test | Pass condition |
|---|---|
| Above-the-fold CTA on landing | Single primary action ("Start learning" or equivalent). No menu paralysis. |
| Trust signals | Privacy / offline / no-login messaging visible without scrolling (per UX Brief 2 §1.1.5) |
| Time to first action | Under 5 seconds from page paint to "user clicked something meaningful" |
| Bounce-prevention | No popup, no email-capture wall, no cookie banner that can't be dismissed |
| First-paint copy | Tagline communicates "JLPT N5" + "free" + "no signup" in <70 chars |

**Tool:** Run a Lighthouse "Best Practices" audit; manually time-to-interactive on Slow-4G in DevTools.

---

## 3. Returning-visitor perspective

**Question:** "Where was I? What's due today?"

| Test | Pass condition |
|---|---|
| Land on home with existing progress | "Continue" button shows last lesson; "Today's queue" shows due Review count |
| Streak indicator | Shows current streak; explains how to keep it (per UX Brief 2 §6) |
| Daily goal | Visible; clickable to start |
| Last-active marker | Some indication of "you last studied 2 days ago" |

**Acceptance:** A returning user knows exactly what to click within 3 seconds.

---

## 4. Mobile-user perspective (≤480px)

**Question:** "Can I study on the train?"

| Test | Pass condition |
|---|---|
| Viewport meta | `width=device-width, initial-scale=1` present |
| Tap targets | All ≥44×44px (per UX Brief 2 §9 / WCAG 2.5.5) |
| Bottom nav | Sticky bottom nav for primary actions on small screens |
| Safe-area insets | Content respects notch / home-indicator on iOS |
| Landscape | App still works at 480×320 landscape |
| One-thumb operation | All quiz interactions reachable with right thumb at average reach |
| Pull-to-refresh | Either works correctly or is disabled (no broken half-state) |
| Zoom | Pinch-zoom is not blocked (`user-scalable=no` is forbidden) |
| Soft keyboard | Type-input questions don't get hidden behind the on-screen keyboard |

**Tool:** Chrome DevTools device emulation, real iPhone + Pixel via BrowserStack.

---

## 5. Accessibility perspective (WCAG 2.1 AA)

**Question:** "Can a screen-reader user pass N5 with this?"

### 5.1 Automated checks

| Tool | What it catches |
|---|---|
| **axe-core / @axe-core/playwright** | Most WCAG violations (contrast, missing labels, ARIA misuse, heading order) |
| **Lighthouse a11y audit** | Coarse pass/fail score |
| **Pa11y** | Same engine as axe; CLI-friendly |

Target: zero `serious` or `critical` axe violations on every route.

### 5.2 Manual checks (axe cannot test)

| Test | Pass condition |
|---|---|
| Keyboard-only | Tab through every interactive element on every route. Visible focus ring. No keyboard trap. |
| Screen reader (NVDA / JAWS / VoiceOver) | Reads question stem, then options, then current selection. Furigana doesn't double-announce. |
| Reduced motion | `prefers-reduced-motion: reduce` disables non-essential transitions |
| High contrast / forced colors | Windows high-contrast mode preserves all info; no `display: none` of visible text |
| 200% zoom | Layout doesn't break; no horizontal scroll on 1280px viewport |
| Color-only meaning | A correct/incorrect answer has more than just green/red - icon or text too |
| Skip link | "Skip to content" works from keyboard |
| Furigana announcement | `<rt>` doesn't get re-read inline; if it does, add `aria-hidden="true"` to ruby text |

### 5.3 Cognitive accessibility

| Test | Pass condition |
|---|---|
| Reading level of UI copy | English UI ≤ B1-CEFR (no idioms, no business jargon) |
| Error messages | Plain language; explain what to do next |
| Consistency | Same action looks the same across views (e.g., "Next" button always in the same spot) |
| Time pressure | If a test has a timer, user can pause or extend it |

---

## 6. Internationalization perspective (5 locales)

**Locales:** en, vi (Vietnamese), id (Indonesian), ne (Nepali), zh (Chinese)

### 6.1 Per-locale checks

For each locale, switch to it via Settings and run §17.1 smoke. Specifically check:

| Test | Pass condition |
|---|---|
| No untranslated keys | Console clean; no `t("foo.bar")` literal renders |
| No truncation | Long Vietnamese / German / Nepali strings don't get cut off |
| Mirrored layout | (Not applicable - none of the 5 are RTL, but verify the assumption holds) |
| Pluralization | `1 question` vs `2 questions` rendered correctly per locale's rules |
| Number formatting | Dates, counts, durations match locale convention |
| Mixed JA + locale | Furigana renders correctly while UI chrome is in the chosen locale |
| Locale persistence | Refresh page → locale stays |

### 6.2 Cross-locale data integrity

| Test | Pass condition |
|---|---|
| `data/*.json` is locale-agnostic | No translatable strings in question / vocab / kanji JSON |
| `locales/*.json` has same key set | All 5 files have the same key tree (a missing key = fallback to English) |
| Furigana rendering doesn't depend on locale | A kanji's reading is the same in en and zh |

**Tool:** Diff `locales/en.json` against the others - report missing keys.

---

## 7. Slow-connection perspective (Slow-4G / 3G)

**Question:** "Does this load on a metro / village WiFi?"

| Test | Pass condition |
|---|---|
| FCP < 1.8s on Slow-4G | Already documented at ~555ms in `TASKS.md` QA gate |
| LCP < 2.5s | Lighthouse |
| Total first-load size | <300KB excluding audio (already 60KB critical-path per QA gate) |
| Audio lazy-loads | First lesson page loads without fetching MP3s; audio fetched on first play only |
| Offline after first load | Service worker `jlpt-n5-tutor-v18` caches shell (stale-while-revalidate) + content (cache-first) |
| Update toast | When SW pulls new shell, user sees "Update available" - clicking refreshes (UX Brief 2 §12.1) |
| Slow network during study | Mid-lesson network drop doesn't lose answer; retry button on save-failed |
| Skeleton placeholders | Every route change shows route-shape-matched skeletons within 50 ms; replaced by real content as data resolves; 5 s timeout shows "Couldn't load this view - Retry" |

**Tool:** DevTools Network throttle = Slow 4G; Lighthouse mobile profile.

---

## 8. Offline perspective

**Question:** "Can I study on a flight?"

| Test | Pass condition |
|---|---|
| Cold offline | Visit once online → kill network → reload → app loads from SW |
| Audio offline | If played at least once, audio replays from cache offline |
| Audio first-time offline | If MP3 was never fetched, app degrades gracefully (no broken player) |
| Progress save offline | LocalStorage writes persist; sync to remote not required (no remote anyway) |
| Offline indicator | Visible UI sign that "you are offline" (UX Brief 2 §12.4) |
| Offline → online recovery | When connectivity returns, indicator disappears; SW updates if shell changed |

**Tool:** DevTools "Offline" checkbox; Application > Service Workers panel.

---

## 9. Power-user perspective

**Question:** "Can I move at the speed of thought?"

| Test | Pass condition |
|---|---|
| Keyboard shortcuts | `1` `2` `3` `4` to pick options; `Space` reveal/flip; `Enter` to advance; `Esc` to dismiss overlays; `?` for cheatsheet; `/` to focus search (UX Brief 2 §7.2, §8) |
| Deep links | `#/learn/<patternId>`, `#/learn/vocab/<form>`, `#/kanji/<glyph>`, `#/test/<n>` (n ∈ 20/30/50) resolve directly without going via home (UX Brief 2 §14.1) |
| Hub sub-paths | `#/learn/grammar` and `#/learn/vocab` both resolve directly and show their TOC card grids |
| Bookmarkable progress | A bookmarked deep link still works after upgrade |
| Search | `/` to focus search; finds across grammar / vocab / kanji; results group by type with counts; clicking deep-links to that item (UX Brief 2 §8) |
| Quit-prompt in Test | Mid-test browser-back / hash-change prompts "Quit this test? Progress so far will be saved"; cancel reverts hash |
| Furigana quick-toggle | Header checkbox toggles between `always` and `hide-known` modes; takes effect on next route render |
| Undo on grading | Mis-tap "Again" in Review → can correct within 2 seconds |

**Tool:** Manual; record a 60s screencast of "I want to drill kosoado for 5 mins" and count clicks.

---

## 10. Cross-browser perspective

| Browser | Version target | Critical for |
|---|---|---|
| Chrome desktop | latest 2 | reference platform |
| Firefox desktop | latest 2 | rendering differences |
| Safari macOS | latest 2 | Safari-specific bugs (audio autoplay, SW quirks) |
| Edge desktop | latest 2 | mostly Chrome-equivalent; spot-check |
| Safari iOS | iOS 16+ | mobile fonts, audio, viewport |
| Chrome Android | latest | mobile reference |
| Firefox Android | latest | spot-check |
| Samsung Internet | latest | popular in some regions |

**Per-browser smoke:** §17.1 plus three browser-specific traps:

- **Safari:** audio playback (especially first-tap requirement on iOS), `<ruby>` fallback, IndexedDB quirks
- **Firefox:** font fallback chain (Noto Sans JP), ServiceWorker scope
- **Edge:** legacy compat headers (HSTS / referrer policy)

**Tool:** BrowserStack Live or Sauce Labs for the long tail.

---

## 11. Cross-OS perspective

| OS | What's special |
|---|---|
| Windows 10/11 | No Japanese font installed by default → must rely on Noto Sans JP / Yu Gothic / Meiryo cascade |
| macOS | Hiragino is system; should pick up first |
| Linux (Ubuntu) | Often missing Noto CJK; verify fallback rendering doesn't show tofu (□) |
| iOS | Safari quirks; PWA install via "Add to Home Screen" |
| Android | Chrome PWA install banner |
| ChromeOS | Tablet + keyboard hybrid; should behave like desktop Chrome |

**Tool:** Real-device verification via BrowserStack or local VMs.

---

## 12. Japanese language accuracy & content integrity (MOST IMPORTANT)

> **Foundational principle:** Every other perspective in this plan assumes the Japanese itself is correct. A perfectly accessible, fast-loading, beautifully-designed app that teaches **wrong Japanese** is actively harmful. **JA accuracy is the bar this app is built to clear.** It outranks performance, design, and even accessibility.
>
> The KB content has been audited 9 times (see `verification.md` Passes 1-9). This section's job is to **prevent regressions** between audits and to keep the audit's invariants enforceable in CI.

This section has three layers:

- **§12.1** Automated content invariants — the audit's checks running on every PR
- **§12.2** Runtime JA accuracy spot-checks — what to verify in the live app
- **§12.3** Periodic re-audit cadence — Pass-N protocol

### 12.1 Automated content invariants in CI

Re-encode the Pass-9 cross-file consistency checks (`verification.md` §8.6) as automated assertions. Any future JSON / KB edit that breaks one fails the build.

| Invariant | Check | Source of truth |
|---|---|---|
| **X-6.1 Catalog completeness** | Every kanji used as a *correct answer* in any question file appears in `kanji_n5.md` AND in `data/kanji.json` | catalog files |
| **X-6.2 Reading consistency** | Every reading taught in `vocabulary_n5.md` matches the reading rendered in question files. Specifically: 今年 = ことし everywhere except as a deliberate distractor | vocab catalog |
| **X-6.3 No mixed-kanji-kana words** | No word contains kanji directly followed by hiragana that is *not* okurigana of that kanji (excludes legitimate forms like 食べる, 大きい). Guard list: 図しょかん, 大さか, 東きょう, 京と, 時かん, 中ご, 日ご | regex sweep |
| **X-6.4 No orphan vocab in question stems** | Every non-trivial word in a question stem appears in `vocabulary_n5.md` or is covered by a documented exception | vocab catalog |
| **X-6.5 No em-dashes** | Zero `—` (U+2014) across all 9 KB files | grep |
| **X-6.6 Group-1 ru-verb flags** | 入る, 帰る, 走る, 知る, 切る, 要る all carry the "Group 1 exception" annotation in `vocabulary_n5.md` | vocab catalog |
| **X-6.7 No false direct-synonymy** | No rationale claims "Direct synonymy" / "Direct antonym pair" / "= " for relationships that are actually approximation-by-elimination (whitelist of genuinely-synonymous pairs maintained) | rationale audit |
| **X-6.8 No raw ASCII digits in TTS source** | No string in `data/grammar.json` `examples[].ja`, `data/reading.json` `passages[].ja`, or `data/listening.json` `items[].script_ja` contains an ASCII digit (`[0-9]`) adjacent to Japanese characters at audio-build time. `tools/build_audio.py:normalize_for_tts()` substitutes ASCII digits → kanji digits before passing to gTTS so the audio reads "三" (さん), not "three" (スリー). The regression guard verifies that every MP3 in `audio/` was generated AFTER the most recent edit to its source `ja` field. | `tools/check_content_integrity.py` (new check) |
| **X-6.9 Furigana primary-reading sanity** | Every kanji in `data/n5_kanji_readings.json` has a `primary` reading that matches the **N5-context-most-common** reading for that kanji. Reference list maintained in the audit script; e.g. 本→ほん, 時→じ, 分→ふん, 円→えん, 月→がつ, 学→がく, 人→にん, 三→さん. The auto-ruby renderer (`js/furigana.js`) uses `primary` when no explicit `furigana` annotation is provided. | `tools/check_content_integrity.py` reference table |

**Beyond X-6.1–X-6.7, also enforce:**

| Invariant | Check |
|---|---|
| **JA-1 Stem-kanji scope** | Every kanji in a question stem AND every kanji in the correct-answer text is in `KnowledgeBank/kanji_n5.md`. Distractors are exempt (per documented exception). |
| **JA-2 Particle-set sanity** | Every question whose options include particles uses only N5 particles (は/が/を/に/で/へ/と/から/まで/より/の/も/や/か/ね/よ/ぐらい/ごろ/だけ/しか/など). |
| **JA-3 Furigana ↔ catalog match** | Every `<ruby>` tag's reading text matches the kun/on yomi listed in `kanji_n5.md` for that kanji. |
| **JA-4 Vocab-reading uniqueness** | If a vocab entry has multiple readings (e.g., 毎年 まいとし/まいねん), all are listed; no ambiguous single-reading citation. |
| **JA-5 Answer-key sanity** | For every question: the `answer` index ∈ {1,2,3,4}; the option text at that index actually exists; the option is not empty/whitespace. |
| **JA-6 No two-correct-answers** | For every multiple-choice question with a particle/grammar slot, only one option is grammatically valid (regression guard for the kind of bug C-1.3 caught: から vs ので both correct). |
| **JA-7 No same-stem duplicates within file** | No two questions in the same file share an identical stem (regression guard: the Q24/Q40 collision in authentic_extracted that was caught in sanity scan). |
| **JA-8 Q-count integrity** | moji=100, goi=100, bunpou=100, dokkai=102, authentic=189. Total=591. Any deviation fails the build. |
| **JA-9 Engine display contract** | Every question file contains the "Engine display note" header so the runtime knows to hide answers in test mode. |

**Tool:** A `tools/check_content_integrity.py` script (or `.js`) wired into the CI workflow from §19. Failures block merge.

```python
# Skeleton (place in tools/check_content_integrity.py)
INVARIANTS = [
    check_x_6_1_kanji_catalog,
    check_x_6_2_reading_consistency,
    check_x_6_3_no_mixed_kanji_kana,
    # ... etc
    check_ja_1_stem_kanji_scope,
    # ... etc
    check_ja_8_q_count_integrity,
]
failures = [c.__name__ for c in INVARIANTS if not c()]
sys.exit(1 if failures else 0)
```

Each check is one short function. Total: ~16 invariants, ~150 lines of Python.

### 12.2 Runtime JA accuracy spot-checks (during UI testing)

The CI invariants catch **structural** breakage in the JSON. They cannot catch **semantic** breakage — for example, a perfectly-formed question whose Japanese is unnatural. That requires human review.

For every UI test session (P0 / P1 / P2), include the following JA spot-checks:

#### 12.2.1 Always check (P0 smoke, 30 seconds)

- [ ] Pick any 3 random questions from `Test` mode. Read the stem and answer aloud as a Japanese speaker would. **Sounds natural?** If anything jars, log to a new audit-pass entry.
- [ ] Open a Learn lesson in `vi` locale. Confirm the **Japanese stays Japanese** (UI chrome translates; example sentences and furigana do not).
- [ ] Trigger a kanji popover (e.g., on 学). Verify on/kun readings match `kanji_n5.md`.

#### 12.2.2 Per-route check (P1 gate, 5 minutes)

For each of the 17 routes that surfaces JA content:

| Route | Spot-check |
|---|---|
| `#/learn` | All 5 hub cards render and link to the right destinations |
| `#/learn/grammar` | 187 cards present; categories sort numerically; sample card text matches `data/grammar.json` |
| `#/learn/<patternId>` | Example sentences are grammatical; furigana matches catalog reading; meaning_ja section uses N5-scope kanji only |
| `#/learn/vocab` | 1002 cards in 40 sections; reading + gloss render under each form |
| `#/learn/vocab/<form>` | Detail shows form + reading + gloss + section; ≥0 example sentences (sourced from grammar.json by either form OR reading); examples that render must be grammatical |
| `#/test` / `#/test/<n>` | Question stems use only N5 syllabus kanji; correct answer is unambiguous; deep-link `#/test/30` skips setup |
| `#/drill` (Practice) | Immediate per-question feedback; same content invariants as Test |
| `#/review` (SRS) | When an item is shown, the reading and gloss match the original lesson |
| `#/kanji` | 106 cards (glyph + first meaning + first kun/on); cards link to detail |
| `#/kanji/<glyph>` | Stroke order, on/kun, example compounds match `kanji_n5.md`; prev/next nav stays inside the 106 entries |
| `#/reading` | Passage text uses only N5 vocab + documented-exception kanji |
| `#/listening` | Audio matches the on-screen transcript verbatim |
| `#/counters` | Counter readings (一本 = いっぽん etc.) are correct; rendaku rules respected |
| `#/teform` | Drill output matches the て-form conjugation table |
| `#/verbclass` | Group-1 / Group-2 / irregular classifications are correct (especially the 6 ru-verb exceptions) |
| `#/waga` | は vs が examples are linguistically defensible (not just memorizable rules) |
| `#/particles` | Minimal pairs are genuinely minimal (one particle change) |
| `#/kosoado` | こ/そ/あ/ど series mappings are complete and correct |

Pass condition: every spot-check succeeds, OR the failure is logged as a new finding and triaged.

#### 12.2.3 Cross-perspective JA checks

- **JA × i18n (§6):** Switching locales must not corrupt Japanese text rendering. Specifically, no half-width katakana when full-width was authored; no kanji turned into "?" boxes.
- **JA × a11y (§5):** Screen readers should announce furigana correctly (or `aria-hidden` it if double-announcement happens). NVDA + Japanese voice should pronounce 学校 as がっこう, not as がく-こう.
- **JA × audio (§7-§8):** TTS audio should match the on-screen reading. If 今日 is shown with reading きょう, the audio should say きょう, not こんにち. **Specific regression guard (Pass-10):** numbers must read in Japanese, not English. Every audio-bearing example with a digit (e.g. `本を 3さつ 読みました`) must read "さんさつ" via the `normalize_for_tts()` digit→kanji substitution; "スリーさつ" is a hard fail. Spot-check by playing one MP3 from each of `audio/grammar/n5-005.0.mp3` (7じ), `audio/listening/n5.listen.001.mp3` (3時), `audio/reading/n5.read.002.mp3` (6時, 9時, 5時, 10時) — every digit should be rendered in Japanese.
- **JA × visual (§16):** Furigana ruby alignment is correct (centered above base text); no overlapping; readable at 100% zoom and at 200% zoom.

### 12.3 Periodic re-audit (Pass-N protocol)

**Cadence:** Every quarter, OR after any batch of 10+ KB edits, OR before any major version bump.

**Process:**

1. Pick an audit lens for this pass: paper-maker (Pass 6), native-teacher (Pass 8), external-brief (Pass 9), or new (e.g., "child-learner readability"). Each lens surfaces different findings.
2. Read all 5 question files + 4 catalog files end-to-end.
3. Log findings with severity (CRITICAL / HIGH / MEDIUM / LOW).
4. Register in `TASKS.md` as "Pass N+1 - <lens name>".
5. Fix in priority order. Each fix → update `verification.md` immediately.
6. Re-run §12.1 invariants. All must pass.
7. Mark Pass N+1 closed in `verification.md`. Update cumulative tally.

**Why this matters:** Static checks (§12.1) catch structural regressions but cannot catch *new* unnatural-Japanese introduced by an edit. Only a human re-read finds those. The Pass-N protocol ensures the bar set by Passes 1-9 stays raised over time.

### 12.4 Content-integrity (UI ↔ data mapping)

These were the original §12 checks — kept here because they're still important, but subordinate to JA accuracy.

| Test | Pass condition |
|---|---|
| Coverage | Every entry in `data/grammar.json`, `data/vocab.json`, `data/kanji.json`, `data/reading.json`, `data/listening.json`, `data/questions.json` is reachable via at least one route |
| No orphan content | No JSON entry that doesn't render anywhere |
| No phantom content | No UI surface with no backing data |
| Cross-reference | When learn page mentions a kanji, the popover shows the same data as `data/kanji.json` |
| Vocab → grammar example sourcing | For each vocab entry that has examples in the grammar corpus (matching by form OR reading), the detail page shows up to 5; words with no matches show an honest empty state ("No example sentences in the corpus yet for this word") |
| Question randomization | Same lesson played twice doesn't show questions in identical order |
| All four options renderable | No `undefined` or `[object Object]` in any option |
| Correct answer exists in options | The "answer" field always matches one of the option indices |
| Audio file matches | `audio/grammar/n5-001.0.mp3` exists for grammar example `n5-001.0` (per `data/audio_manifest.json`); 449 grammar + 30 reading + 12 listening MP3s currently shipped |
| Furigana doesn't lie | When ruby renders, the reading matches `data/n5_kanji_readings.json` |
| Storage v2 round-trip | Settings → Export. Reset all progress (typed-phrase confirm). Import. All 5 keys restored: settings, history, results, knownKanji (per-kanji "I know this" flags), streak ({current, longest, lastStudyDate, days}). |

**Tool:** Same `tools/check_content_integrity.py` from §12.1; these are added as additional invariants (UI-1 through UI-9).

### 12.5 Severity escalation

If a §12.1 invariant fires in CI, treat it as a **release blocker**. JA accuracy regressions cannot ship.

If a §12.2 spot-check finds a semantic issue mid-test:

- **CRITICAL** (factual error, internal contradiction, would teach wrong Japanese) → block the release; open a hotfix Pass-N entry; fix immediately
- **HIGH** (unidiomatic, register clash, or policy violation) → log; fix in next milestone
- **MEDIUM / LOW** → log; batch into next quarterly Pass-N audit

---

## 13. Performance perspective

| Metric | Target | Tool |
|---|---|---|
| Lighthouse Performance | ≥90 mobile, ≥95 desktop | Lighthouse CI |
| FCP | <1.8s mobile Slow-4G | Lighthouse |
| LCP | <2.5s | Lighthouse / Web Vitals JS |
| TBT | <200ms | Lighthouse |
| CLS | <0.1 | Lighthouse |
| Bundle size | <100KB JS gzipped (no framework, so should be easy) | Chrome DevTools Coverage |
| Long tasks | No task >50ms during user interaction | Performance panel |
| Memory | <50MB after a 20-question test | Performance > Memory |

**Tool:** Lighthouse CI in GitHub Actions; failing budget should fail the build.

---

## 14. Security perspective

This is a static no-login no-server app, but still:

| Test | Pass condition |
|---|---|
| No outbound network calls | Network tab is empty during a normal session (already in QA gate) |
| Strict CSP | Add `<meta http-equiv="Content-Security-Policy">` if not present; `default-src 'self'`; allow only inline styles needed; no `unsafe-eval` |
| HTTPS only | GitHub Pages enforces; verify in browser address bar (lock icon) |
| No telemetry | No `navigator.sendBeacon`, no `fetch` to analytics, no `<img>` 1x1 trackers |
| LocalStorage doesn't leak PII | Export the storage payload; verify no email / IP / device-id |
| XSS surface | If any user input is rendered (e.g., text-input answers), it's escaped before going into the DOM |
| Service worker scope | `sw.js` only caches first-party assets; doesn't intercept third-party requests |
| `target="_blank"` links | All have `rel="noopener noreferrer"` |
| External JSON | Validate shape on load; tolerate missing fields |

**Tool:** Mozilla Observatory for headers; manual DevTools network audit.

---

## 15. PWA perspective

| Test | Pass condition |
|---|---|
| `manifest.webmanifest` valid | Lighthouse PWA score 100 |
| Installable | "Install app" prompt appears in Chrome desktop and Android (per UX Brief 2 §12.3) |
| Standalone mode | Installed app opens without browser chrome |
| App icon | 192px and 512px icons render on home screen |
| Splash screen | iOS shows app icon, not white screen |
| Update flow | New shell version → toast appears → click reloads (UX Brief 2 §12.1) |
| Uninstall | User can uninstall and reinstall without losing exported progress |

**Tool:** Chrome DevTools > Application > Manifest; PWA Builder.

---

## 16. Visual / UX consistency perspective

| Test | Pass condition |
|---|---|
| Visual regression | Run Playwright/Percy snapshots before and after each merge; flag pixel diffs |
| Theme consistency | All buttons share the same focus-ring spec |
| Empty states | Every list has an empty-state UI - no blank page (UX Brief 2 §3.2) |
| Loading states | Skeleton screens, not "Loading..." text (UX Brief 2 §3.1) |
| Error states | Network failure shows actionable message + retry button |
| Disabled states | Disabled controls have `aria-disabled="true"` and a 4.5:1 contrast ratio |
| Hover states | Don't introduce hover-only functionality (mobile users have no hover) |
| Animation consistency | All transitions use the same duration/easing tokens |

**Tool:** Playwright `toHaveScreenshot()`; or Percy/Chromatic SaaS.

---

## 17. Test execution levels

### 17.1 P0 - Smoke (5 minutes, every release)

Pre-flight before any deploy:

- [ ] **§12.1 invariants pass** (all 18 content checks green - this is a HARD release blocker; X-6.8 digit-in-TTS and X-6.9 primary-reading sanity are part of this set)
- [ ] **§12.2.1 JA spot-check** (3 random questions read naturally; kanji popover matches catalog)
- [ ] **Audio digit spot-check (Pass-10 regression):** play any MP3 from `audio/grammar/n5-005.0.mp3` (7じに) and `audio/listening/n5.listen.003.mp3` (8時半 / 9時). Numbers must read in Japanese (しちじ / はちじはん / くじ), never in English ("seven" / "eight" / "nine" / "スリー").
- [ ] Home page loads. Title is correct. No console errors. Trust strip visible above the fold.
- [ ] Click "Learn" → 5-card hub shows (Grammar / Vocabulary / Kanji / Dokkai / Listening).
- [ ] Click "Grammar" card → grammar TOC of cards loads; click any card → pattern detail shows pattern + EN + JA meaning + ≥1 example with translation.
- [ ] Click "Vocabulary" card → vocab cards load; click any card → vocab detail shows form / reading / gloss / examples.
- [ ] Click "Kanji" card → kanji card grid loads; click any card → kanji detail shows on/kun/meaning.
- [ ] Click "Test" → question shows. Pick an answer → moves to next.
- [ ] Click "Settings" → switch locale to `vi` → UI updates. Switch furigana to "Always show" → ruby renders on every kanji. Switch back to "Hide on known kanji" → previously-marked kanji stay un-rubied.
- [ ] Open kanji popover (click any glyph) → toggle "I know this kanji" → reload → ruby still hidden on that kanji.
- [ ] Refresh page. Locale + furigana mode + "I know this" flags + streak all persist.
- [ ] Open DevTools → Network panel → no third-party requests.
- [ ] Lighthouse mobile run completes; score not regressed by >5pts.

### 17.2 P1 - Pre-release gate (60 minutes, every release)

Already covered by §9 of original Brief 1; extend with:

- [ ] **§12.1 invariants pass** (re-confirmed after any KB / data edit)
- [ ] **§12.2.2 per-route JA spot-check** (every route surfacing JA content is sampled; semantic issues logged)
- [ ] All 17 routes + sub-paths load without console errors (use `for route in routes; navigate; assert no error`). Sub-paths to include: `#/learn/grammar`, `#/learn/vocab`, `#/learn/vocab/<form>`, `#/learn/<patternId>`, `#/kanji/<glyph>`, `#/test/<n>`.
- [ ] axe-core shows zero `serious` violations on Home, Learn (hub + grammar TOC + vocab list + vocab detail), Test, Review, Settings, Kanji index, Kanji detail.
- [ ] Lighthouse mobile Perf/A11y/PWA/SEO all ≥90.
- [ ] Offline mode: kill network, reload home, app still works. Verify SW served stale shell + content.
- [ ] Export progress JSON (schemaVersion 2). Wipe localStorage with typed-phrase reset. Import. All 5 storage keys restored (settings, history, results, knownKanji, streak).
- [ ] PWA install prompt fires once on supported browser; "Not now" persists; doesn't re-prompt.
- [ ] SW update toast: bump cache version locally, reload, expect "Update available" toast → click Reload → new shell active.
- [ ] Run full `tests.html`; 37/37 pass.

### 17.3 P2 - Full regression (one full session, every milestone)

Run §1-§16 systematically. Time budget ~4 hours for a single tester.

**Mandatory in P2:**
- [ ] **§12.3 Pass-N re-audit** of all 5 question files + 4 catalog files from one chosen lens (paper-maker / native-teacher / external-brief / new lens). Document findings as a new Pass-N entry in `verification.md`.

Document findings in a Pass-N audit entry.

### 17.4 P3 - Deep-dive perspectives (ad-hoc)

When a specific change ships (e.g., "we redesigned the Review screen"), pick the perspective most affected and run that section deeply. Don't run the whole §1-§16 every time.

**Special case:** Any change touching `KnowledgeBank/*.md` or `data/*.json` automatically triggers §12.1 (CI invariants) AND §12.2.1 (smoke JA spot-check) AND a focused §12.2.2 on the affected route. JA accuracy is non-negotiable.

---

## 18. Recommended tooling stack

For a static no-server JLPT app maintained by 1-2 people:

| Layer | Tool | Why this one |
|---|---|---|
| **E2E browser** | **Playwright** | Best in class; cross-browser; built-in screenshots; no flakiness from CDP races |
| **Visual regression** | **Playwright `toHaveScreenshot()`** | Already on Playwright; no separate SaaS needed |
| **Accessibility** | **@axe-core/playwright** | Same Playwright run; one report |
| **Performance** | **Lighthouse CI** in GitHub Actions | Free; runs on every PR |
| **PWA validator** | **PWA Builder** + Lighthouse PWA audit | Free; comprehensive |
| **Cross-browser** | **BrowserStack Live** (free trial) or local-only Chrome+Firefox+Safari | Real Safari/iOS coverage matters |
| **Manual exploratory** | **Chrome DevTools** + a notes doc | Catch the things automation misses |
| **Heuristic eval** | **Nielsen 10 heuristics** as a checklist | Catches UX issues automation can't |
| **AI-assisted black-box** | **Claude in Chrome MCP** (already in env) | Useful for "behave like a confused user" sessions |

**Anti-pattern:** Don't add Cypress / Selenium / Puppeteer alongside Playwright. Pick one.

---

## 19. CI integration

Add a single GitHub Actions workflow that runs on every PR to `main`:

```yaml
name: ui-regression
on:
  pull_request:
    branches: [main]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm ci
      - run: npx playwright install --with-deps
      - run: npx playwright test
      - run: npx @lhci/cli autorun
      - uses: actions/upload-artifact@v4
        if: always()
        with:
          name: test-artifacts
          path: |
            playwright-report/
            .lighthouseci/
```

Fail the build on:
- Any Playwright test failure
- axe `serious` or `critical` violation
- Lighthouse Perf/A11y drop >5pts vs baseline
- Visual regression > 0.1% pixel diff (after a manual approval workflow)

---

## 20. Heuristic checklist (Nielsen 10, applied to this app)

For ad-hoc UX review:

1. **Visibility of system status** - Loading skeletons, save indicators, streak progress all visible.
2. **Match between system and real world** - "Daily Drill" not "Spaced repetition queue v2."
3. **User control & freedom** - Can pause / quit / undo any action without penalty.
4. **Consistency & standards** - All "next" buttons same shape/place; all destructive actions confirm.
5. **Error prevention** - Disabled states for invalid actions; confirm before wiping progress.
6. **Recognition over recall** - Show furigana toggle state; show selected option visually, not just by tab focus.
7. **Flexibility & efficiency** - Keyboard shortcuts for power users; touch-friendly for mobile.
8. **Aesthetic & minimalist design** - Don't add decoration that doesn't aid learning.
9. **Help users recognize & recover from errors** - "You picked X, the answer was Y because Z."
10. **Help & documentation** - `?` key for shortcut cheatsheet; per-screen help link if needed.

---

## 21. What this plan deliberately does NOT cover

- **Backend testing** - there is no backend.
- **Auth / accounts** - not in scope; PWA design is no-login (Brief 1 hard constraint #3).
- **Cloud sync** - out of scope (Brief 1 #2 / Out-of-scope).
- **Speaking practice** - out of scope (microphone input).
- **Engine math (SRS intervals)** - already covered by `tests.html`.

**Note on JA correctness:** Earlier drafts of this plan listed "Content correctness in JA" as out of scope. **That was wrong.** JA accuracy is the foundational concern of this app and is now §12 — the most important perspective in the plan. Audit Passes 1-9 in `verification.md` set the bar; §12.1 keeps it enforced in CI; §12.2 keeps it spot-checked at runtime; §12.3 keeps it re-audited every quarter.

---

## 22. Acceptance criteria for this plan

The plan itself is "in use" when:

1. **§12.1 invariants are enforceable** — `tools/check_content_integrity.py` exists, runs all 16 checks, and is wired into CI as a release blocker.
2. **§12.2 spot-checks are documented** — every release log includes the 3-question JA spot-check from §12.2.1.
3. **§12.3 re-audit cadence is set** — calendar reminder for quarterly Pass-N re-audit; or trigger on any 10+ KB-edit batch.
4. Every release runs §17.1 (P0 smoke).
5. Every release runs §17.2 (P1 gate); failures block deploy.
6. Every milestone runs §17.3 (P2 full regression); findings logged as Pass-N audit entry.
7. Tooling from §18 is installed in the repo with a `package.json` script entry point.
8. CI from §19 is wired and green on `main`.

When all eight hold, the app has a defensible "we teach correct Japanese, and we test it" story.

---

## 23. Appendix - perspective coverage matrix

| Perspective | Section | Priority | Manual? | Automated? |
|---|---|---|---|---|
| **JA accuracy & content integrity** | **§12** | **P0 (foundational - blocks release)** | **Yes (§12.2)** | **Yes (§12.1 invariants in CI)** |
| End learner | §1 | P1 | Yes | Partial (E2E happy path) |
| First-time visitor | §2 | P1 | Yes | Lighthouse copy/CTA |
| Returning visitor | §3 | P1 | Yes | E2E with localStorage seed |
| Mobile user | §4 | P1 | Yes | Playwright device emulation |
| Accessibility | §5 | P1 | Yes | axe-core + Lighthouse |
| i18n | §6 | P1 | Yes | Per-locale Playwright run |
| Slow connection | §7 | P2 | Yes | Lighthouse Slow-4G |
| Offline | §8 | P2 | Yes | Playwright with `context.setOffline` |
| Power user | §9 | P2 | Yes | E2E keyboard interactions |
| Cross-browser | §10 | P2 | Yes | Playwright `--project` per browser |
| Cross-OS | §11 | P3 | Yes | BrowserStack |
| Performance | §13 | P1 | No | Lighthouse CI |
| Security | §14 | P1 | Partial | Mozilla Observatory + manual DevTools |
| PWA | §15 | P2 | Partial | Lighthouse PWA |
| Visual / UX consistency | §16 | P2 | Yes | Playwright screenshots |

---

*End of plan. Total: 22 perspectives across 17 routes (plus sub-paths under `#/learn/...`, `#/kanji/...`, `#/test/...`) × 5 locales × 8 browsers × 6 OSes. **§12 (Japanese language accuracy) is the foundational concern; everything else assumes the JA is correct.** Triage ruthlessly.*

---

## Changelog (this document)

- **2026-04-30** Synced to UX Brief 2 Phases 1-4 + Learn hub + per-vocab detail flow:
  - Added §0.1 route map covering the new `#/home`, `#/learn/grammar`, `#/learn/vocab`, `#/learn/vocab/<form>`, `#/kanji/<glyph>`, `#/test/<n>` sub-paths.
  - Updated §1.1 first-lesson journey to include the 5-card hub, grammar/vocab/kanji card listings, and the kanji popover's "I know this kanji" flag.
  - Updated §7 SW reference from v15 to v18 + added skeleton-placeholder check.
  - Updated §9 power-user shortcuts (`Esc`, `/`) and added quit-prompt + furigana quick-toggle rows.
  - Updated §12.2.2 per-route table to include the new hub, grammar TOC, vocab list, vocab detail, and kanji card index.
  - Updated §12.4 content-integrity table with vocab→grammar example sourcing rule and storage v2 round-trip check (5 keys).
  - Updated §17.1 P0 smoke to walk the hub → cards → detail flow and verify "I know this kanji" persistence.
  - Updated §17.2 P1 gate to include sub-path coverage, install prompt, SW update toast, and storage-v2 export/import.
