# JLPT N5 Tutor — UX Fixes Developer Brief

**Project:** `https://gauravaccentureproducts.github.io/jlpt-n5-tutor/`
**Scope of this brief:** User experience fixes only. Curriculum and pedagogical work is covered in a separate document. Do not change lesson content as part of this work.
**Goal:** Make the existing app understandable, usable, and trustworthy on first contact, and frictionless on the 50th visit.

---

## 0. Hard constraints to preserve

These must remain true after every change:

1. Static-only deployment (GitHub Pages).
2. No data leaves the device. No analytics, no telemetry, no third-party tracking.
3. No login, no account.
4. Works fully offline after first load.
5. Cross-browser: Chrome, Firefox, Safari, Edge — last 2 versions. Mobile Safari and Chrome Android are first-class.
6. Hash-based routing must continue (GitHub Pages constraint).

---

## 1. Landing screen — rebuild

The current landing screen shows: title, four-word tagline, five flat tabs, a furigana toggle, a persistent "Loading...", and a footer line. This is insufficient for a first-time visitor and disorienting for a returning one.

### 1.1 First-time visitor state

When `localStorage` shows no progress, the landing screen must contain, in this vertical order:

1. **Product name and one-line scope.** Replace "Learn. Test. Review. Master." with a concrete value proposition such as: *"Pass JLPT N5 with 15 minutes a day. ~80 grammar patterns, ~800 words, ~100 kanji. No login, no ads, no data shared."* The exact wording is editable; the requirement is that it states scope and differentiation, not vibe.
2. **Primary CTA button** labeled "Start your first lesson" that routes to the first unstudied Learn item.
3. **Secondary link** "Take a placement check" that routes to a short diagnostic (10–15 items) which marks already-known patterns as such, so returning learners aren't forced through lesson 1.
4. **Three-card row** summarizing the three product pillars: Learn (with count of patterns), Practice (drills + SRS), Test (mock exams). Each card is clickable and routes to that section.
5. **Trust strip** (small text, but above the fold): "✓ Works offline ✓ No login required ✓ Your progress stays on this device." This is the actual differentiator against commercial apps and must not be buried.

### 1.2 Returning visitor state

When `localStorage` shows progress, the landing screen must additionally show, above the three-card row:

1. **"Continue where you left off" card** showing the last lesson or drill, with a single-click resume button.
2. **"Today's review queue" card** showing how many SRS items are due today, with a "Start review" button. If zero are due, show a positive empty state ("All caught up — come back tomorrow") rather than hiding the card.
3. **Streak / progress strip** showing current daily streak and a 7-day mini-heatmap. Keep it small; do not gamify aggressively.

### 1.3 Acceptance criteria for the landing screen

- A first-time user can identify what to click within 3 seconds of landing.
- A returning user can resume their last activity in 1 click.
- No element on the landing screen says "Loading..." for longer than 200ms after first paint.
- The privacy/offline/no-login claim is visible without scrolling on a 360×640 mobile viewport.

---

## 2. Navigation — rebuild

### 2.1 Rename "Drill 0"

This label is meaningless to users. Rename to its actual function. If it is the daily mixed-practice queue, rename to **"Practice"** or **"Daily Drill."** If it is something else, rename to whatever that something else is. Do not ship a label that requires the user to click to find out what it means.

### 2.2 Reorder and regroup the nav

The current order — Learn / Test / Drill 0 / Review / Summary — does not reflect how the app is used. Restructure as follows:

**Primary nav (always visible):**
- **Learn** — new material
- **Practice** — drills (renamed from Drill 0)
- **Review** — SRS queue, with a small badge showing items due today
- **Test** — mock exams

**Secondary nav (in a header menu or footer):**
- **Summary** — diagnostic dashboard
- **Settings** — preferences
- **Help / About**

The reasoning: Learn / Practice / Review is the daily loop. Test is a periodic event. Summary is metadata. Putting these as five flat siblings implies they are equivalent moves; they are not.

### 2.3 Active-state indication

The current tab must be visually distinct from inactive tabs (different weight, color, or underline). Hover and focus states must also be distinct from active state. Test that all three states are visible in light theme, dark theme, and at WCAG AA contrast.

### 2.4 Persistent location indicator

Inside any tab, the user must always be able to see *where they are* without scrolling: e.g. "Lesson 4 of 22 · て-form" at the top of the Learn view, "Question 7 of 20" at the top of a drill, "Day 12 streak" on the home dashboard. This is one of the most common UX failures in study apps; do not skip it.

---

## 3. Loading and error states

### 3.1 Eliminate the persistent "Loading..." text

The shell currently shows literal "Loading..." that is visible long enough to capture in a server-rendered fetch. This must be replaced with:

1. **Skeleton screens** — gray placeholder blocks that match the shape of the content being loaded. Render these immediately on tab change.
2. **Lazy data loading** — lesson JSON loads on tab activation, not on initial app boot. Initial JS bundle target: < 100KB gzipped.
3. **Loader timeout** — if any data fetch takes longer than 5 seconds, surface a real error UI ("Couldn't load this lesson. Retry?") rather than spinning forever.

### 3.2 Empty states for every tab

When a tab has no data to show, render a real empty state, not a blank screen or a zero. Required empty states:

- **Review tab, no items due:** "🌱 No reviews due right now. Come back later, or [start a new lesson]."
- **Review tab, no progress yet:** "Reviews appear here after you finish your first lesson. [Go to Learn]."
- **Test tab, no completed tests:** "Take your first mock test when you've covered at least lessons 1–10. [Continue learning]."
- **Summary tab, no progress yet:** "Your dashboard fills in as you study. [Start your first lesson]."
- **Practice tab, no items unlocked:** "Practice unlocks after you finish your first lesson. [Go to Learn]."

Each empty state must include a routing button, not just text.

### 3.3 Network failure handling

If a JSON file fails to load (rare, but happens on flaky connections):

- Show a retry button, not a blank screen.
- Surface the actual problem in plain language ("You appear to be offline" vs "Couldn't reach the lesson file").
- If offline and the data is in the service worker cache, use the cache silently — do not surface a "you're offline" warning when the app is functioning normally.

---

## 4. Furigana — upgrade from binary toggle

### 4.1 Three-mode furigana setting

Replace the current single toggle with three modes, exposed as a radio group in Settings and as a quick-toggle on the lesson screen:

1. **Always show** — ruby on every kanji
2. **Hide on known kanji** *(default)* — ruby is shown only on kanji the user has not marked as "I know this"
3. **Always hide** — no ruby anywhere

### 4.2 Per-kanji "I know this" affordance

Every kanji rendered in the app must be tappable / clickable. On tap, show a small popover with:
- The kanji glyph, on'yomi, kun'yomi, English meanings, stroke count
- A toggle: "I know this kanji" (persists in `localStorage`)
- A link to the kanji's full lesson page

### 4.3 Live preview next to the toggle

When the user changes the furigana setting, a small inline preview must update in real time, e.g. showing `日本語` with and without ruby, so the user can see what they're choosing before applying it to the whole app.

### 4.4 Implementation requirements

- Use semantic `<ruby>` and `<rt>` markup, not parenthesized kana strings. This is required for accessibility and copy-paste behavior.
- Toggle furigana via CSS (`rt { display: none }`), not by re-rendering the DOM, so toggling is instant.
- Furigana setting persists across sessions in `localStorage`.

---

## 5. Settings panel (NEW)

Add a Settings page accessible from the secondary nav. It must include:

- **UI language** — dropdown. Ship with English at v1; structure must support adding Vietnamese, Indonesian, Nepali, and Simplified Chinese later (these are large JLPT N5 demographics and currently underserved).
- **Theme** — Light / Dark / System (default System; respect `prefers-color-scheme`).
- **Font size** — S / M / L / XL. Affects all Japanese and English text proportionally.
- **Furigana mode** — three options per §4.1.
- **Audio playback speed** — 0.75× / 1.0× / 1.25× (default 1.0×). Applies to all audio in the app.
- **Daily new-card limit** — slider, default 10, range 5–30.
- **Daily review cap** — slider, default 100, range 20–500.
- **Reduce motion** — toggle, default reads `prefers-reduced-motion`.
- **Reset progress** — destructive action, requires double confirmation with typed phrase ("Type RESET to confirm").
- **Export progress** — downloads a `progress.json` file containing all `localStorage` data.
- **Import progress** — uploads a `progress.json` file. Must validate before applying. On schema mismatch, show a clear error and do not overwrite existing data.

All settings persist in `localStorage`. Settings page itself must work offline.

---

## 6. Daily rhythm and orientation

### 6.1 Streak and daily goal

A small, non-intrusive streak indicator on the landing screen and in the header. Default daily goal: 15 minutes or 20 reviews, whichever comes first. User-configurable in Settings.

Do not gate functionality behind streaks. Do not punish missed days with red warnings or guilt-trip copy. The streak is a quiet positive signal, nothing more.

### 6.2 Session-end screen

After completing a Learn lesson or finishing a Review/Practice/Test session, show a session-end screen with:

- What the user did (e.g. "Reviewed 24 items, 3 lapses, 21 correct")
- A single recommended next action (e.g. "Continue to next lesson" or "All done for today — see you tomorrow")
- A "back to home" button

Do not auto-advance to the next session. Session boundaries matter.

---

## 7. Drill / quiz interaction patterns

### 7.1 Immediate feedback per question

Every drill question must show feedback *immediately after answering*, not at the end of the drill. Required feedback content:

- Correct/incorrect indicator (icon + color, never color alone — accessibility)
- The correct answer if user was wrong
- A one-sentence explanation of *why* — pulled from the lesson's `common_mistakes` field
- A "Continue" button or `space`/`enter` keyboard advance

### 7.2 Keyboard shortcuts

All drill flows must support keyboard:

- `1` / `2` / `3` / `4` — select multiple-choice answers
- `space` — flip a flashcard or reveal answer
- `enter` — submit / continue
- `?` — open a keyboard-shortcut cheatsheet overlay

A small "?" affordance in the drill UI should reveal the cheatsheet so shortcuts are discoverable.

### 7.3 Quit / pause behavior

Inside a Test or drill:
- The browser back button must prompt: "Quit this test? Progress so far will be saved." Three options: Quit, Stay, Save & Quit.
- An explicit "Pause" / "Quit" button must always be visible.
- Quitting a Test mid-stream must save partial results; the user should never lose 15 minutes of work to a misclick or a phone call.

### 7.4 Scroll and state preservation on tab switch

Switching from Learn to Review and back must preserve the user's scroll position and any in-progress drill state. Do not reset on every tab change.

---

## 8. Search

Add a search input, accessible from the header on every page (icon on mobile, full input on desktop). Initial scope:

- Search across grammar pattern IDs, titles, and English explanations
- Search across vocabulary entries (kanji, kana, English)
- Search across kanji entries (glyph, readings, meanings)

Results group by type (Grammar / Vocab / Kanji) with a count per group. Clicking a result deep-links to the relevant lesson with that item highlighted. Search must work offline.

Keyboard shortcut: `/` focuses the search input.

---

## 9. Mobile and responsive

The dominant device for N5 study is a phone. The app must be designed mobile-first.

### 9.1 Breakpoints
- ≤ 480px: single column, bottom nav bar
- 481–1024px: single column, top nav
- ≥ 1025px: optional two-column layout for Learn (lesson on left, examples on right)

### 9.2 Tap targets
All interactive elements must be ≥ 44×44 CSS pixels per Apple HIG and WCAG 2.1 AA target-size guidance.

### 9.3 Safe areas
Respect iOS safe-area insets (`env(safe-area-inset-bottom)` etc.) so the bottom nav doesn't sit under the home indicator.

### 9.4 No horizontal scroll
On any viewport ≥ 320px wide, the app must never produce horizontal scroll.

### 9.5 Touch behavior
- Long-press should not trigger text selection on interactive elements.
- Swipe gestures (optional but nice): swipe left/right to advance / go back through flashcards.
- No hover-only affordances. Anything visible only on hover must also be reachable on tap and keyboard.

---

## 10. Accessibility (WCAG 2.1 AA)

### 10.1 Required behaviors
- All interactive elements keyboard-reachable with visible focus rings.
- Color contrast ≥ 4.5:1 for normal text, ≥ 3:1 for large text and UI controls.
- No information conveyed by color alone (correct/wrong needs an icon as well).
- All audio has a transcript toggle.
- All images have meaningful `alt` text or `alt=""` if decorative.
- Respect `prefers-reduced-motion`: disable card flip animations, disable streak confetti, disable any motion that isn't strictly functional.

### 10.2 Japanese text and screen readers
- Japanese text containers must have `lang="ja"` so screen readers use the correct voice.
- Furigana via `<ruby>` is required (parenthesized kana breaks both screen readers and copy-paste).
- The page itself remains `lang="en"` (or the active UI language).

### 10.3 Testing
Smoke-test with NVDA on Windows, VoiceOver on macOS and iOS, and TalkBack on Android. Document the test results in the PR.

---

## 11. Typography and rendering

### 11.1 Japanese webfont
Load **Noto Sans JP** as the primary Japanese font, subset to N5 + N4 character ranges to keep size down (~200KB woff2). Fallback stack:

```css
font-family: "Noto Sans JP", "Hiragino Kaku Gothic ProN",
             "Yu Gothic", "Meiryo", sans-serif;
```

Without an explicit Japanese webfont, Windows machines without the Japanese language pack render shared CJK codepoints in Chinese variants (visible on `直`, `海`, `骨`, `今`, `画`, etc.). This is a real bug, not a polish item.

### 11.2 Font loading
Use `font-display: swap` so text is readable while the font loads. Preload the woff2 file in `<head>`.

### 11.3 Latin font
A neutral system stack is fine for Latin text:

```css
font-family: -apple-system, BlinkMacSystemFont, "Segoe UI",
             Roboto, "Helvetica Neue", Arial, sans-serif;
```

---

## 12. Offline and PWA

### 12.1 Service worker
- Cache the app shell on first load.
- Cache lesson JSON, audio, and kanji SVGs on first access (cache-on-use).
- Update strategy: stale-while-revalidate for the shell; cache-first for content assets.
- Surface a small "Update available — reload?" toast when a new shell version is detected.

### 12.2 Manifest
Ship a `manifest.webmanifest` with:
- Name, short name
- Icons at 192×192, 512×512, and a maskable variant
- `display: standalone`
- `theme_color` and `background_color` matching the app theme
- `start_url` set to the home route

### 12.3 Install prompt
On supported browsers, show a small "Install this app" banner once per user (dismissible, persisted in `localStorage`). Do not nag.

### 12.4 Offline indicator
Detect `navigator.onLine` and show a tiny offline indicator only when offline AND when a feature requires network (none should, in the steady state). When offline-but-functional, do not surface anything — the user shouldn't care.

---

## 13. Internationalization scaffolding

Even if v1 ships English-only, build the i18n layer now. Specifically:

- Every UI string flows through a `t("key")` function.
- Translations live in `/locales/{en,vi,id,ne,zh}.json`.
- Language detection: read `navigator.language`, fall back to English, allow override in Settings.
- Right-to-left support is not required for this app.
- Lesson content (Japanese sentences, kanji) is *not* translated — only the UI chrome and English glosses.

---

## 14. URL and shareability

### 14.1 Deep links
Every meaningful state must have a unique URL:

- `#/learn/n5.te-form` — specific lesson
- `#/practice/te-form` — specific drill type
- `#/test/2` — specific mock test
- `#/kanji/食` — specific kanji page

Sharing the URL with another user must open the app to that exact state.

### 14.2 Browser history
- Forward/back navigation must work as expected.
- Inside a drill, back must prompt before discarding state (see §7.3).

### 14.3 Print stylesheet
Add a `@media print` stylesheet that produces a clean printable view of any Learn lesson: hides nav, expands all content, uses serif body font, includes furigana inline. Some N5 learners study on paper.

---

## 15. Copy revisions

Replace the following strings:

- **Tagline** — "Learn. Test. Review. Master." → "Pass JLPT N5 with 15 minutes a day. No login, no ads, no data shared." (or equivalent — must state scope and differentiation)
- **Footer** — "Static app. Runs from any browser. No data leaves this device." → "Works offline. No login. Your progress stays on this device." (replaces developer-speak with user-facing reassurance)
- **Tab: Drill 0** — rename per §2.1
- **Toggle: Show furigana on N5 kanji** — replaced by three-mode setting per §4.1
- **Loading...** — replaced by skeletons per §3.1

Do not introduce em-dashes, exclamation marks, or marketing exclamations into UI copy. Plain, concrete language only.

---

## 16. What's new / version

Add to the Settings page or footer:

- App version number (e.g. "v1.4.0")
- Last content update date (e.g. "Content updated April 2026")
- A "What's new" link that opens a `CHANGELOG.md` rendered as HTML, listing recent changes in plain language.

---

## 17. Things explicitly out of scope

Do not, as part of this UX work, do any of the following. They are either separate workstreams or rejected:

- Add user accounts, social features, friend lists, or leaderboards.
- Add cloud sync (export/import covers this need).
- Add ads, sponsorships, or promotional content of any kind.
- Add aggressive gamification (XP bars, level-ups, streak-loss penalties, push notifications).
- Add AI features that require runtime API calls.
- Change lesson content, example sentences, or grammar explanations. (Curriculum work is a separate brief.)
- Add speaking practice with microphone input.
- Add features beyond N5.

---

## 18. Acceptance checklist (per feature)

A feature is "done" only when every line is true:

1. **Functional:** works in Chrome, Firefox, Safari, Edge, Mobile Safari, Chrome Android — last 2 versions.
2. **Offline:** works after page is loaded once, with the network disabled.
3. **Accessible:** keyboard-navigable, screen-reader-tested, contrast meets WCAG 2.1 AA, respects `prefers-reduced-motion` and `prefers-color-scheme`.
4. **Localized:** every UI string uses `t()`. No hardcoded English in components.
5. **Persistent:** any state generated by the feature survives reload and is included in export/import.
6. **Performant:** does not push initial bundle above 100KB gzipped or push FCP above 1.5s on simulated 4G.
7. **Mobile-first:** designed for 360×640 first, then scaled up.
8. **Documented:** README updated with a one-paragraph description of the feature.

---

## 19. Phasing (suggested order)

**Phase 1 — Stop the bleeding (week 1):**
- Rename "Drill 0"
- Replace persistent "Loading..." with skeletons + 5s timeout error
- Add empty states for Review, Test, Summary, Practice
- Add deep-link URLs per §14.1
- Promote privacy/offline/no-login messaging to landing screen

**Phase 2 — Daily-use friction (week 2):**
- Three-mode furigana setting + `<ruby>` migration + per-kanji "known" toggle
- Settings panel (theme, font size, audio speed, reset, export, import)
- Persistent location indicator across all views
- Immediate per-question feedback in drills
- Keyboard shortcuts in drill flows

**Phase 3 — Landing and orientation (week 3):**
- Rebuild landing screen (first-time and returning states)
- Streak + daily goal + session-end screens
- Search across grammar, vocab, kanji
- Restructure nav (primary vs secondary)

**Phase 4 — Polish and reach (week 4):**
- PWA manifest + service worker + install prompt
- Mobile responsive review pass
- Accessibility audit pass with NVDA/VoiceOver/TalkBack
- i18n scaffolding (ship English; structure ready for VI/ID/NE/ZH)
- Print stylesheet
- Noto Sans JP webfont + `lang="ja"` audit

---

## 20. QA checklist before any release

- [ ] No console errors on any route, in any browser.
- [ ] First Contentful Paint < 1.5s on simulated 4G (Lighthouse).
- [ ] Initial JS bundle < 100KB gzipped.
- [ ] Lighthouse: Performance ≥ 90, Accessibility ≥ 95, Best Practices ≥ 95, PWA installable.
- [ ] Works fully offline after one online load (test with DevTools → Offline).
- [ ] No outbound network requests during a steady-state learning session (verify in Network tab with cache disabled).
- [ ] Furigana toggle changes are instant (no reflow flash) and persist across reload.
- [ ] Export → wipe → import round-trips all progress without loss.
- [ ] Browser back button does not cause data loss inside drills.
- [ ] Tab switching preserves scroll position and in-progress drill state.
- [ ] All Japanese text renders in a Japanese font on a clean Windows machine without the Japanese language pack.
- [ ] Screen reader announces Japanese text using a Japanese voice (verify `lang="ja"`).
- [ ] No element has a tap target smaller than 44×44 CSS pixels.
- [ ] No horizontal scroll on viewports ≥ 320px wide.
- [ ] Theme switches instantly between light/dark/system without flash of wrong theme.

---

## 21. Notes for the developer

- Resist adding features. The product currently has too few features done well; do not add more half-finished ones.
- Prioritize *clarity over cleverness* in every copy and IA decision. If you find yourself explaining what a label means, the label is wrong.
- The privacy + offline + no-account posture is the actual differentiator against Duolingo, Bunpo, and Renshuu. Treat it as a first-class product feature, not a footer.
- When in doubt about a UX decision, simulate a learner who has 15 minutes, is on a phone, on a train, with 30% battery. If the design fails for that user, redesign it.
- Do not introduce dependencies that require a build server, paid SaaS, or runtime API keys. Static-only is a constraint, not a guideline.

---

*End of brief.*
