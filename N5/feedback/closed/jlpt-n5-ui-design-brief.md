# JLPT N5 Tutor - UI Design Improvement Brief

**Project:** `https://gauravaccentureproducts.github.io/jlpt-n5-tutor/`
**Scope:** Visual UI design critique (typography, color, hierarchy, layout, spacing, polish). Page-by-page improvements with concrete CSS-level guidance.
**Out of scope here:** UX/IA issues like empty states, navigation labels, missing features. Those are covered in the separate UX brief.

This document is grounded in:
- Direct observation of the landing page screenshot (verified)
- The site's nav structure (Learn / Practice / Review / Test / Summary)
- The data shapes from the JSON bundle (vocab, grammar, kanji, questions, reading, listening)

Where I can't directly observe a page (the inner tabs render via JavaScript), recommendations are framed as patterns to apply once the developer compares them against the actual current state.

---

## 0. Design system foundation (apply globally before any page-specific work)

Before fixing individual pages, lock down the design tokens. Without them every page looks different.

### 0.1 Color palette

Current state shows three colors: a dark green (header text, headings, CTA button background), a near-white cream background, and a subtle border gray. Define formally:

```css
:root {
  /* Brand */
  --color-brand-900: #14532d;   /* Deepest green - headlines, primary CTA bg */
  --color-brand-700: #166534;   /* Heading green - section titles */
  --color-brand-500: #22c55e;   /* Accent green - active states, success */
  --color-brand-50:  #f0fdf4;   /* Tint background for cards/highlights */

  /* Neutrals */
  --color-bg:        #fafaf7;   /* Page background (current cream) */
  --color-surface:   #ffffff;   /* Card backgrounds */
  --color-border:    #e5e5e0;   /* Card borders, dividers */
  --color-text:      #1f2937;   /* Body text */
  --color-text-muted:#6b7280;   /* Captions, helper text */

  /* Semantic */
  --color-correct:   #16a34a;   /* Right answers */
  --color-incorrect: #dc2626;   /* Wrong answers */
  --color-warning:   #d97706;   /* Almost-due review badge */
  --color-info:      #2563eb;   /* Tips, callouts */
}
```

**Critical:** The current CTA "Start your first lesson" uses near-black-green (~#14532d). The secondary "Take a placement check" button is rendered in a light green/white tone. Establish formal button variants:

```css
.btn-primary   { background: var(--color-brand-900); color: white; }
.btn-secondary { background: white; color: var(--color-brand-900); border: 1px solid var(--color-brand-900); }
.btn-ghost     { background: transparent; color: var(--color-brand-700); }
```

### 0.2 Typography

The current stack appears to be a default sans-serif (likely `system-ui` or similar). For a Japanese-learning app this is acceptable but underspecified. Lock down:

```css
:root {
  --font-jp: "Noto Sans JP", "Hiragino Kaku Gothic ProN",
             "Yu Gothic", "Meiryo", sans-serif;
  --font-en: "Inter", -apple-system, BlinkMacSystemFont,
             "Segoe UI", system-ui, sans-serif;
}
body { font-family: var(--font-en); }
.lang-ja { font-family: var(--font-jp); }
```

**Type scale** (use a modular scale, not arbitrary px values):

```css
:root {
  --text-xs:   0.75rem;   /* 12px - tiny captions */
  --text-sm:   0.875rem;  /* 14px - helper text */
  --text-base: 1rem;      /* 16px - body */
  --text-lg:   1.125rem;  /* 18px - card body */
  --text-xl:   1.25rem;   /* 20px - card titles */
  --text-2xl:  1.5rem;    /* 24px - section headings */
  --text-3xl:  1.875rem;  /* 30px - page titles */
  --text-4xl:  2.25rem;   /* 36px - hero headline */
}
```

Headings use `--font-en` weight 700; body uses 400; Japanese uses weight 500 to match optical balance against Latin 400.

### 0.3 Spacing scale

Currently the spacing looks improvised. The hero card has notably tight padding (~24px) while the cards below have similar but inconsistent padding. Adopt an 8-point scale:

```css
:root {
  --space-1: 0.25rem;   /* 4px */
  --space-2: 0.5rem;    /* 8px */
  --space-3: 0.75rem;   /* 12px */
  --space-4: 1rem;      /* 16px */
  --space-5: 1.5rem;    /* 24px */
  --space-6: 2rem;      /* 32px */
  --space-8: 3rem;      /* 48px */
  --space-10: 4rem;     /* 64px */
  --space-12: 6rem;     /* 96px */
}
```

### 0.4 Border radius

Cards in the screenshot have a subtle but slightly inconsistent radius. Define:

```css
:root {
  --radius-sm: 4px;    /* small chips, badges */
  --radius-md: 8px;    /* buttons, inputs */
  --radius-lg: 12px;   /* cards */
  --radius-xl: 16px;   /* hero cards */
}
```

Apply `--radius-lg` (12px) to all the existing cards.

### 0.5 Shadow system

Currently the cards have no shadow, just a thin border. This is a defensible choice but produces a flat, low-energy feel. Add a soft shadow on hover only:

```css
.card {
  border: 1px solid var(--color-border);
  border-radius: var(--radius-lg);
  background: var(--color-surface);
  transition: box-shadow 200ms ease, transform 200ms ease;
}
.card:hover {
  box-shadow: 0 4px 12px rgba(20, 83, 45, 0.08);
  transform: translateY(-2px);
}
```

The translate-on-hover gives the interactivity affordance the cards currently lack.

---

## 1. Landing page (Home) - observed issues and fixes

This is the page in the screenshot. Critique by region.

### 1.1 Header - issues

**Observed:**
- "JLPT N5 Grammar Tutor" wordmark sits flush left with no logomark.
- Center nav: Learn / Practice / Review / Test (4 items, evenly spaced).
- Practice has an underline/dash next to it suggesting it's the active tab - but this is the home page, not the Practice page, so the indicator is wrong.
- Right cluster: search input, "Summary" link, and a settings cog icon.
- Header has no background color or shadow separating it from the page.

**Issues:**

1. **"Grammar Tutor" undersells the product.** The site has vocab, kanji, reading, and listening as well. The wordmark scope contradicts the hero ("187 grammar patterns · ~1000 vocab · 97 N5 kanji · 30 reading passages · 12 listening drills"). Decide: drop "Grammar" from the title, OR drop the non-grammar content from the hero.
2. **Practice tab shows a dangling dash/underline.** This appears to be an active-state indicator that's misfiring on the home page. Fix: either hide the indicator when no tab is selected, or correctly set Home as a fifth nav item with the indicator there.
3. **No logomark.** A small ja-themed mark (一 or あ in a circle, 30×30 px) next to the wordmark would lift the brand from "default text" to "considered." Optional but recommended.
4. **Header has no demarcation from the body.** When the user scrolls down on inner pages, the header will visually merge with the content. Add a bottom border or subtle shadow:

```css
.app-header {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  position: sticky; top: 0; z-index: 50;
}
```

5. **Right cluster mixes search input + link + icon.** Three different control types crammed together with no spacing rhythm. Recommend:
 - Group search alone on the right with a search icon prefix inside.
 - Move "Summary" into the primary nav (or into the cog menu) - currently it's orphaned.
 - The cog (settings) is fine as the rightmost item.

**Concrete fix - CSS structure:**

```html
<header class="app-header">
  <div class="container header-grid">
    <a class="brand" href="#/home">
      <span class="brand-mark">一</span>
      <span class="brand-name">JLPT N5 Tutor</span>
    </a>
    <nav class="primary-nav">
      <a href="#/learn">Learn</a>
      <a href="#/practice" class="active">Practice</a>
      <a href="#/review">Review <span class="badge">12</span></a>
      <a href="#/test">Test</a>
    </nav>
    <div class="header-tools">
      <input type="search" placeholder="Search...">
      <button aria-label="Settings" class="icon-btn"><!-- settings icon SVG --></button>
    </div>
  </div>
</header>
```

```css
.header-grid {
  display: grid;
  grid-template-columns: auto 1fr auto;
  align-items: center;
  gap: var(--space-6);
  padding: var(--space-3) var(--space-5);
}
.primary-nav {
  display: flex;
  justify-content: center;
  gap: var(--space-6);
}
.primary-nav a {
  padding: var(--space-2) var(--space-3);
  color: var(--color-text);
  font-weight: 500;
  position: relative;
}
.primary-nav a.active {
  color: var(--color-brand-700);
}
.primary-nav a.active::after {
  content: "";
  position: absolute;
  left: 12px; right: 12px; bottom: -6px;
  height: 2px;
  background: var(--color-brand-700);
  border-radius: 2px;
}
```

The `::after` pseudo-element pattern produces a clean underline indicator instead of the current dangling dash.

### 1.2 Hero card - issues

**Observed:**
- Headline: "Pass JLPT N5 with 15 minutes a day" - strong and concrete. 
- Sub-line: stats list with middle-dot separators. Functional.
- Three trust badges (Works offline / No login required / Your progress stays on this device).
- Two CTAs: primary "Start your first lesson" (filled green) + secondary "Take a placement check" (outlined).

**Issues:**

1. **The hero is centered visually but typographically left-aligned, creating a weak diagonal.** The card itself is centered; the text inside is left-aligned. Headline starts at the same x as the trust ticks. This is a common, defensible choice but reads slightly amateur. Strengthen by either:
 - **Option A (recommended):** Keep left-aligned text but reduce card width to ~700px (currently appears ~900px) so the line lengths are tighter. Long lines feel formless.
 - **Option B:** Make headline + sub-line center-aligned, keep CTAs centered too. More marketing-page feel; probably wrong for a study tool.

2. **Stats sub-line lacks visual hierarchy.** "187 grammar patterns · ~1000 vocab · 97 N5 kanji · 30 reading passages · 12 listening drills." This is a stat dump. Visualize as small badges or paired number+label cards:

```html
<div class="hero-stats">
  <span class="stat"><b>187</b> grammar</span>
  <span class="stat"><b>1000+</b> vocab</span>
  <span class="stat"><b>97</b> kanji</span>
  <span class="stat"><b>30</b> reading</span>
  <span class="stat"><b>12</b> listening</span>
</div>
```

```css
.hero-stats { display: flex; flex-wrap: wrap; gap: var(--space-2); margin: var(--space-4) 0; }
.stat {
  display: inline-flex; align-items: baseline; gap: var(--space-1);
  background: var(--color-brand-50);
  padding: var(--space-1) var(--space-3);
  border-radius: 999px;
  font-size: var(--text-sm);
  color: var(--color-text-muted);
}
.stat b { color: var(--color-brand-900); font-weight: 600; }
```

This converts a flat sentence into a glanceable scoreboard.

3. **Trust ticks are inline plain text.** Currently they read as small body copy with a check-mark prefix. Promote them to small badges using the same pill pattern, but with neutral coloring and an actual icon (SVG check, not the `` glyph which renders inconsistently across platforms).

4. **CTAs need a hover state and clearer hierarchy.** The primary button (dark green) and secondary (outlined) are an OK pairing, but:
 - The secondary button's text "Take a placement check" looks slightly purple (browser default link color leaking through?). Override to match brand green.
 - Hover states aren't visible from the screenshot; ensure both buttons have hover states (primary: darken; secondary: fill light green).

```css
.btn-primary { background: var(--color-brand-900); color: white; }
.btn-primary:hover { background: #0f3d22; }
.btn-secondary { background: white; color: var(--color-brand-700); border: 1px solid var(--color-brand-700); }
.btn-secondary:hover { background: var(--color-brand-50); }
```

5. **Hero has no visual anchor - no illustration, kanji, or graphic.** A study app with zero visual is plain. Suggest one of:
 - A small decorative kanji (e.g., 学 in 80% opacity, large, positioned bottom-right of the card)
 - A simple SVG illustration of stacked books or a kana stroke
 - A subtle radial gradient using `--color-brand-50` behind the card

```css
.hero-card {
  position: relative;
  background:
    radial-gradient(ellipse at top right, var(--color-brand-50), transparent 60%),
    var(--color-surface);
  overflow: hidden;
}
.hero-card::after {
  content: "学";
  position: absolute;
  right: -20px; bottom: -40px;
  font-family: var(--font-jp);
  font-size: 240px;
  color: var(--color-brand-900);
  opacity: 0.04;
  font-weight: 900;
  pointer-events: none;
}
```

The ::after gives the card a kanji watermark - present but not loud.

### 1.3 Three-card row (Learn / Practice / Test) - issues

**Observed:**
- Three equal-width cards with a heading and one-line description.
- Cards are not visually clickable (no hover affordance, no chevron, no button).

**Issues:**

1. **Cards look like read-only callouts, not navigation.** They probably *are* clickable links to the respective sections, but a user can't tell from the design. Add:
 - Hover state (already specified in §0.5)
 - A subtle `→` chevron in the bottom-right
 - Cursor pointer

```html
<article class="path-card">
  <h3>Learn</h3>
  <p>Grammar, vocab, kanji, reading, listening - pick a section.</p>
  <span class="card-arrow" aria-hidden="true">→</span>
</article>
```

```css
.path-card { position: relative; padding: var(--space-5); cursor: pointer; }
.card-arrow {
  position: absolute; right: var(--space-5); bottom: var(--space-5);
  color: var(--color-brand-700);
  transition: transform 200ms ease;
}
.path-card:hover .card-arrow { transform: translateX(4px); }
```

2. **The card titles lack visual weight against the descriptions.** "Learn", "Practice", "Test" should be more dominant. Use `var(--text-xl)` (20px) bold + brand color, vs. `var(--text-base)` regular for body.

3. **No visual distinction between the three cards.** Each represents a different mode (input, practice, evaluation). Use small icons (24px SVG or emoji wrapper) at the top of each card to differentiate:
 - Learn → (open book) or a kanji-themed icon
 - Practice → (target) or (refresh for SRS)
 - Test → (clipboard) or (trophy)

Don't use inline emoji directly - wrap in SVG sprites for cross-platform consistency.

4. **Three is the wrong count if Review is its own nav item.** The hero pillars don't include Review, but Review has a top-nav slot. Add a fourth card OR remove Review from the top nav. Currently the IA tells the user "there are 4 things to do" but the home page tells them "there are 3."

5. **Card text "Daily mixed drills + spaced-repetition Review."** has an inconsistent capitalization. "Review" is capitalized mid-sentence as if it's a proper noun. Either keep all section names capitalized as proper nouns, or none of them.

### 1.4 Below-cards helper line - issues

**Observed:** "Already partway through? Take the placement check above so you don't repeat what you know."

**Issues:**

1. **Typo: "partway" is correct but "partway through" is awkward.** Better: "Already familiar with some N5 material? Take the placement check above to skip what you know."

2. **The line is orphaned at the bottom of the hero section with no visual treatment.** It reads as fine-print. If it's important, give it weight (a subtle background pill, an icon, or an info callout). If not, delete it - it duplicates the placement-check CTA above.

3. **Better still - make this contextual:** show this line ONLY if the user clicks "Start your first lesson" without taking the placement check first. Inline it as a hint after they've started, not as preemptive copy.

### 1.5 Footer - issues

**Observed:** "Works offline · No login · Progress stays on device · v1.5.0 · What's new"

**Issues:**

1. **Trust messaging duplicated.** The same three points appear in the hero badges. Either remove from the footer or remove from the hero - not both. Recommend: keep in hero (where users see them on first load), remove from footer.

2. **Version + "What's new" link are useful but visually weak.** Small underline-blue-link in a sea of gray text. Make "What's new" a proper button:

```html
<footer class="app-footer">
  <span class="footer-meta">v1.5.0</span>
  <a class="footer-link" href="#/changelog">What's new</a>
</footer>
```

3. **Add a privacy/source link.** Footer is the conventional place. "About · Privacy · Source on GitHub" - three small links, right-aligned.

### 1.6 Landing page - overall composition

The vertical rhythm is currently:

```
[header - 60px]
[white space - 64px]
[hero card - 220px]
[white space - 32px]
[3-card row - 160px]
[white space - 16px]
[helper line - 24px]
[white space - 80px]
[footer - 40px]
```

**Issues:**

1. **Vast white space above the hero.** ~64px of nothing between header and first content. On larger screens this is wasteful. Reduce to 32px on desktop, or fill with a small breadcrumb or daily-goal strip for returning users.

2. **No "where you left off" state for returning users.** First-time landing is fine; the page makes no concession for the user on visit #50 who just wants to resume. Add (per the UX brief, but relevant visually here) a small top-of-page strip:

```html
<section class="resume-strip" hidden>
  <div class="resume-content">
    <span class="resume-label">Pick up where you left off</span>
    <span class="resume-detail">Lesson 14 · て-form · 7 of 12 examples done</span>
  </div>
  <button class="btn-primary btn-sm">Resume</button>
</section>
```

This sits above the hero on the home page when localStorage shows progress. Visually it's a thin (~56px) strip in `--color-brand-50`.

3. **Mobile: review at 375px width.** I can only verify desktop from the screenshot, but based on the desktop layout, the hero stats line will wrap awkwardly on mobile. Test at 375px and 414px viewports; consider stacking hero stats vertically there.

---

## 2. Learn page - design recommendations (inferred)

Based on the data shape (`grammar.json` with categories, `vocab.json` with sections, `kanji.json` with 106 entries, `reading.json` with 30 passages, `listening.json` with 12 items), the Learn page is presumably an index that routes to five sub-modules.

### 2.1 Layout pattern: section grid

Use a 2×3 or 3×2 grid of large cards. Each card represents one learning track:

```
[ Grammar     ] [ Vocab       ] [ Kanji       ]
  187 patterns    1,003 words     106 chars
  ━━━━━━━━━━     ━━━━━━━━       ━━━━━━━━
  Progress bar    Progress bar    Progress bar

[ Reading     ] [ Listening   ]
  30 passages     12 drills
  ━━━━━━━━━      ━━━━━━━
  Progress bar    Progress bar
```

Each card:
- Top: section name (text-xl, bold)
- Stat line: total count of items in that section (text-sm, muted)
- Progress bar: visual indicator of % completed (use `--color-brand-500` fill on `--color-brand-50` track)
- Hover: lift + chevron

```css
.learn-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: var(--space-4);
  max-width: 960px;
  margin: 0 auto;
}
.learn-card { padding: var(--space-5); }
.learn-card .progress-track {
  height: 6px;
  background: var(--color-brand-50);
  border-radius: 999px;
  margin-top: var(--space-3);
}
.learn-card .progress-fill {
  height: 100%;
  background: var(--color-brand-500);
  border-radius: 999px;
  transition: width 400ms ease;
}
```

### 2.2 Inside a sub-module (e.g., Grammar)

Two-column layout on desktop, one column on mobile:

- **Left rail (240px):** Categorical index. Pulled from `grammar.json` categories: Particles (31), Adjectives (12), Te-form (9), etc. Click a category, the right pane scrolls/loads.
- **Right pane (flex-1):** The pattern detail. Title, conjugation table, examples, common mistakes, contrasts.

```css
.learn-detail { display: grid; grid-template-columns: 240px 1fr; gap: var(--space-6); }
@media (max-width: 768px) {
  .learn-detail { grid-template-columns: 1fr; }
  .learn-rail { order: 2; } /* nav below content on mobile */
}
```

### 2.3 Pattern detail card

The data has rich structure: `pattern`, `meaning_en`, `meaning_ja`, `form_rules`, `explanation_en`, `examples[]`, `common_mistakes[]`, `contrasts[]`, `notes`. Render them with clear visual sectioning, not as a single paragraph dump:

```html
<article class="pattern">
  <header class="pattern-header">
    <h2 class="pattern-form lang-ja">〜です／〜ます</h2>
    <p class="pattern-meaning">Polite copula / polite verb ending</p>
  </header>

  <section class="pattern-rules">
    <h3>Form</h3>
    <table class="conjugation-table">...</table>
  </section>

  <section class="pattern-examples">
    <h3>Examples</h3>
    <ol class="example-list">
      <li class="example">
        <p class="example-ja lang-ja">わたしは <ruby>学生<rt>がくせい</rt></ruby>です。</p>
        <p class="example-en">I am a student.</p>
        <button class="example-audio" aria-label="Play audio">▶</button>
      </li>
    </ol>
  </section>

  <section class="pattern-mistakes">
    <h3>Common mistakes</h3>
    <div class="mistake">
      <p class="mistake-wrong"><span class="mistake-label">Wrong</span> <span class="lang-ja">わたしは がくせいです じゃありません。</span></p>
      <p class="mistake-right"><span class="mistake-label">Right</span> <span class="lang-ja">わたしは がくせいじゃありません。</span></p>
      <p class="mistake-why">Don't combine です and じゃありません.</p>
    </div>
  </section>
</article>
```

Visual treatment:
- Pattern form: large (text-3xl) Japanese, centered, with a `--color-brand-50` background block behind
- Examples: numbered, with audio button on the right; ja text in `--font-jp` weight 500, en in `--font-en` weight 400 muted color
- Common mistakes: "Wrong" label in red and "Right" label in green; the wrong line in muted gray with strikethrough, or simply `--color-incorrect` accent
- Conjugation table: bordered cells, header row in `--color-brand-50`

### 2.4 Vocab module

Different shape: ~1,000 entries across ~40 thematic sections. UI options:

**Option A - flashcard mode:** Single card center-screen, kana on front, kanji+meaning on back. Swipe/click to advance. Minimalist, focused.

**Option B - section browser:** Left rail of section names; right pane of vocab as a compact table or grid of small cards (kanji, kana, meaning).

Recommend Option B as the default Learn view, with a "Drill this section" button that switches into Option A flashcard mode for the active section.

### 2.5 Kanji module

A grid of large kanji tiles. Each tile shows the kanji glyph at ~64px font size, with on/kun readings on hover or below in tiny text. Click a tile → modal or detail page with stroke order, on/kun, meaning, example words.

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
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  cursor: pointer;
  transition: all 200ms ease;
}
.kanji-tile:hover {
  border-color: var(--color-brand-500);
  transform: scale(1.04);
}
.kanji-tile .glyph {
  font-family: var(--font-jp);
  font-size: 64px;
  line-height: 1;
  color: var(--color-brand-900);
  font-weight: 500;
}
.kanji-tile .meaning { font-size: var(--text-xs); color: var(--color-text-muted); margin-top: var(--space-2); }
```

This will look distinctly Japanese-flavored - the large kanji is the visual anchor.

### 2.6 Reading & Listening modules

Use a card list where each card represents one passage/drill:

- Title (English short title)
- Length indicator (chars for reading; seconds for listening)
- Difficulty pill (easy/medium/hard)
- Status (not started / in progress / completed)
- For listening: a small play-button icon

---

## 3. Practice page - design recommendations

The Practice tab serves drills and SRS reviews. Typical UI is a single-card-at-a-time flow.

### 3.1 Drill card design

Center one large card on the page. Drill UI follows this pattern:

```
┌──────────────────────────────────────┐
│  Question 7 of 20   ━━━━━━━━━━━━━━  │  <- Progress bar
├──────────────────────────────────────┤
│                                      │
│    わたし（  ）がくせいです。        │  <- Question (large, ja)
│                                      │
├──────────────────────────────────────┤
│   [ は ]   [ が ]   [ を ]   [ に ]  │  <- Answer choices
└──────────────────────────────────────┘
              [ Skip ] [ Next ]
```

Critical visual rules:

- **One card per screen, max width 640px.** Don't fight to fill the viewport.
- **Question text is the focal point**: `--text-2xl` or `--text-3xl`, `--font-jp`, weight 500, line-height 1.6.
- **Answer choices as buttons**, full-width or 2×2 grid. Use `--text-lg`, weight 500. On hover, `--color-brand-50` background.
- **Feedback is immediate and visually unambiguous** after answering:
 - Correct: green border on selected button, green check icon, brief celebration animation (subtle scale pulse, no confetti).
 - Wrong: red border on selected button, gray border on the correct one with a small "← correct" label, explanation panel slides up from below.
- **Keyboard: 1/2/3/4 to select**, Enter/Space to advance. Show keys on the buttons (small superscript) once user has used keyboard once.

```css
.drill-card {
  max-width: 640px;
  margin: var(--space-8) auto;
  background: var(--color-surface);
  border: 1px solid var(--color-border);
  border-radius: var(--radius-xl);
  padding: var(--space-6);
}
.drill-question {
  font-family: var(--font-jp);
  font-size: var(--text-2xl);
  font-weight: 500;
  line-height: 1.7;
  text-align: center;
  margin: var(--space-6) 0;
}
.drill-choices { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-3); }
.drill-choice {
  padding: var(--space-4);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-md);
  background: var(--color-surface);
  font-family: var(--font-jp);
  font-size: var(--text-lg);
  cursor: pointer;
  transition: all 150ms ease;
}
.drill-choice:hover { border-color: var(--color-brand-500); background: var(--color-brand-50); }
.drill-choice.correct { border-color: var(--color-correct); background: #f0fdf4; }
.drill-choice.incorrect { border-color: var(--color-incorrect); background: #fef2f2; }
```

### 3.2 SRS grade buttons

For review-mode cards, after answering, show four grading buttons (Again / Hard / Good / Easy) as a row at the bottom. Color-code:
- Again: `--color-incorrect` (red)
- Hard: `--color-warning` (orange)
- Good: `--color-correct` (green)
- Easy: `--color-info` (blue)

Each button shows the next interval below the label, e.g., "Hard · 1 day" / "Good · 3 days" / "Easy · 1 week" - calculated from FSRS/SM-2 state.

### 3.3 Session-end screen

When the user finishes a drill batch, show a summary:

```
┌──────────────────────────────────────┐
│          Session complete           │
│                                      │
│           18 / 20 correct             │  <- Big number, brand color
│                                      │
│    ━━━━━━━━━━━━━━━━━━━━━━━━━━━━     │  <- Time spent
│           4 minutes 22 seconds        │
│                                      │
│   [ Review missed ] [ Continue ]      │
└──────────────────────────────────────┘
```

No confetti. No XP. A clean stat summary.

---

## 4. Review page - design recommendations

If implemented as SRS (per UX brief), the Review page is a special case of Practice but with additional state visualization.

### 4.1 Top strip: queue overview

Above the drill card, show a small strip:

```
[ Due today: 12 ]  [ Learning: 5 ]  [ Mastered: 217 ]    4 min
```

Three pills with counts, color-coded:
- Due today: `--color-warning` background, dark orange text
- Learning: `--color-info` background, dark blue
- Mastered: `--color-correct` background, dark green

The estimated time pill on the right gives the user a sense of session length.

### 4.2 Empty state (zero reviews due)

If no reviews are due, the page should NOT be blank or show "0". Show:

```
   All caught up!

  No reviews due right now.
  Come back in 4 hours, or
  [ start a new lesson ]
```

Centered, minimal, optimistic. The "come back in 4 hours" calculates from the next-due card in the SRS queue.

### 4.3 Review heatmap (optional, on Summary page)

GitHub-style 7-row × 53-column grid showing daily review activity. One cell per day, color intensity = number of reviews completed. Use `--color-brand-50` (lightest) to `--color-brand-900` (darkest) ramp.

This is optional for v1 but high-impact for habit formation.

---

## 5. Test page - design recommendations

Mock JLPT-format exams. Different feel from Practice - should feel like a test, not a casual drill.

### 5.1 Test landing (before starting)

Card-list of available mock tests:

```
┌────────────────────────────────────┐
│ Mock Test 1                        │
│ 30 questions · 25 minutes          │
│ Grammar · Vocab · Reading           │
│                          [ Start ] │
└────────────────────────────────────┘
```

Show an estimated duration so the user can decide if they have time.

### 5.2 In-test UI

Should feel formal:
- Header strip with test name + remaining time (`mm:ss`, monospaced font, prominent)
- Question number indicator: "Question 7 of 30"
- Progress strip showing answered/unanswered/flagged questions as colored dots
- No immediate feedback - answers locked in but not graded until submit
- "Mark for review" / "Flag" button per question
- "Submit" button enabled only when all answered (or after warning)

```css
.test-header {
  background: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  padding: var(--space-3) var(--space-5);
  display: flex; justify-content: space-between; align-items: center;
}
.test-timer {
  font-family: ui-monospace, "SF Mono", Menlo, monospace;
  font-size: var(--text-xl);
  color: var(--color-text);
  font-variant-numeric: tabular-nums;
}
.test-timer.warning { color: var(--color-warning); }
.test-timer.critical { color: var(--color-incorrect); animation: pulse 1s infinite; }
```

### 5.3 Test results screen

After submission:

- Overall score (large, brand color)
- Pass/fail indicator (JLPT N5 passing is 80/180; calibrate threshold)
- Section breakdown (grammar X/Y, vocab X/Y, reading X/Y)
- Missed questions list with click-to-expand explanations
- "Retake" and "Review wrong answers" CTAs

Treat this screen with weight - it's a milestone moment for the learner.

---

## 6. Summary page - design recommendations

The diagnostic dashboard. This is where most study apps fail visually.

### 6.1 Layout: top stats + sectional breakdown

```
┌─────────────────────────────────────────────────┐
│ [ Streak: 12 days ]  [ Total: 247 ]  [ Today: 23 ]│
└─────────────────────────────────────────────────┘

[ Grammar mastery       ━━━━━━━━━━━━━━━ 73% ]
[ Vocab mastery         ━━━━━━━━━━━━━━━ 61% ]
[ Kanji mastery         ━━━━━━━━━━━━━━━ 45% ]
[ Reading speed         ━━━━━━━━━━━━━━━ 58% ]
[ Listening accuracy    ━━━━━━━━━━━━━━━ 39% ]

╔══════════════════════════════╗
║ Weak spots                    ║
║ ┌─────────────────────────┐  ║
║ │ Particle を:  62% acc    │  ║
║ │ て-form (ぐ): 4 / 12     │  ║
║ │ は vs が:    30% acc    │  ║
║ │ Counter 本:  fewer right │  ║
║ └─────────────────────────┘  ║
║      [ Drill these now ]      ║
╚══════════════════════════════╝
```

### 6.2 Mastery bars

Use a labeled progress bar for each section. The fill color reflects the mastery level:
- 0 - 25%: red ramp (struggling)
- 25 - 60%: orange ramp (learning)
- 60 - 85%: yellow-green ramp (consolidating)
- 85 - 100%: green ramp (mature)

Don't use a single `--color-brand-500` for everything - the gradation is itself information.

### 6.3 Weak-spots panel

This is the most useful and most under-designed part of any study app. Make it pop visually:
- Background `--color-warning` with 6% opacity
- Border-left 4px in `--color-warning`
- Strong heading
- A clear "drill these" CTA at the bottom

This panel is what separates a diagnostic dashboard from a vanity dashboard. Spend design time here.

### 6.4 Activity heatmap

GitHub-style heatmap. Reuse from §4.3.

### 6.5 Avoid trap: too many numbers, not enough actions

Common Summary-page mistake: showing 15 stats in a grid with no next action. Each panel should answer: "given this stat, what should the user do?" If a panel doesn't answer that, demote or delete it.

---

## 7. Settings (cog menu) page - design recommendations

Per the UX brief, Settings is needed. Visual treatment:

- One-column layout, max-width 640px, centered
- Sectioned (Display / Audio / Furigana / Daily limits / Data / About)
- Each setting on its own row: label on left, control on right
- Use native form controls styled minimally (don't reinvent the toggle)
- Destructive actions (Reset progress) at bottom, in red

```html
<div class="settings-section">
  <h2>Furigana</h2>
  <div class="setting-row">
    <label for="furigana-mode">Show furigana</label>
    <select id="furigana-mode">
      <option>Always</option>
      <option selected>Only on unknown kanji</option>
      <option>Never</option>
    </select>
  </div>
</div>
```

---

## 8. Cross-cutting visual improvements

### 8.1 Loading states

Replace any "Loading..." text with skeleton screens. Skeleton uses a shimmering placeholder block matching the shape of incoming content.

```css
@keyframes shimmer {
  0% { background-position: -200% 0; }
  100% { background-position: 200% 0; }
}
.skeleton {
  background: linear-gradient(90deg, var(--color-border) 0%, #f5f5f0 50%, var(--color-border) 100%);
  background-size: 200% 100%;
  animation: shimmer 1.5s infinite;
  border-radius: var(--radius-md);
}
```

### 8.2 Microinteractions

A study app benefits from small, well-tuned microinteractions:
- Card hover lift (already specified)
- Button press: scale 0.98 for 100ms
- Correct answer: subtle green pulse on the chosen button
- Wrong answer: gentle horizontal shake (no jarring camera shake)

```css
@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-4px); }
  75% { transform: translateX(4px); }
}
.choice.incorrect { animation: shake 200ms ease; }
```

Keep all motion under 300ms. Respect `prefers-reduced-motion`.

### 8.3 Furigana via `<ruby>`

Don't use parenthesized kana. Use semantic ruby:

```html
<ruby>日本語<rt>にほんご</rt></ruby>
```

```css
ruby rt {
  font-size: 0.5em;
  color: var(--color-text-muted);
  font-weight: 400;
}
.furigana-off rt { display: none; }
```

The toggle hides ruby instantly via CSS - no re-render needed.

### 8.4 Japanese-character rendering

Add this to global CSS:

```css
:lang(ja), .lang-ja {
  font-family: var(--font-jp);
  font-feature-settings: "palt" 1; /* proportional alternate widths for cleaner ja layout */
}
```

The `palt` feature setting makes Japanese punctuation tighter and more elegant. Small detail; native readers notice.

### 8.5 Dark mode

Define dark-mode tokens. A study app gets used at night.

```css
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #0f1612;
    --color-surface: #1a221d;
    --color-border: #2a342d;
    --color-text: #e5e7eb;
    --color-text-muted: #9ca3af;
    --color-brand-900: #4ade80;
    --color-brand-700: #22c55e;
    --color-brand-50: #1a3a26;
  }
}
```

Test that the brand green still meets WCAG AA contrast (≥4.5:1) against the dark background.

### 8.6 Focus states

Every interactive element needs a visible focus ring. Don't use the browser default - design one:

```css
:focus-visible {
  outline: 2px solid var(--color-brand-500);
  outline-offset: 2px;
}
```

Critical for keyboard users (which a serious study tool will have).

---

## 9. Quick wins (highest visual ROI per hour of dev work)

If you only do five things from this brief, do these:

1. **Lock down the design tokens (§0)** - without these, every other improvement is hand-rolled.
2. **Hero card visual upgrade (§1.2)** - add the kanji watermark, convert stats to pill badges, add hover states to CTAs. ~2 hours of work; biggest perception change.
3. **Three-card row interactivity (§1.3)** - add hover lift, chevron, icon. ~1 hour. Currently the cards look dead.
4. **Standardize loading + empty states (§8.1, §4.2)** - replace "Loading..." with skeletons everywhere; design empty states for Review/Test/Summary. ~3 hours.
5. **Drill card redesign (§3.1)** - single 640px card, large ja question, immediate feedback colors, keyboard hints. ~4 hours. This is the screen the user sees most often; invest in it.

---

## 10. What I couldn't review (request screenshots)

I designed this brief from one screenshot (the landing page) plus the data shapes. To tighten the recommendations, the most useful screenshots would be:

1. The Learn index page (after clicking Learn)
2. A Grammar pattern detail (any pattern with examples + common mistakes)
3. A drill / Practice question in mid-flow
4. A drill / Practice answer-feedback state (right and wrong)
5. The Review tab (with and without due items)
6. The Test landing and an in-test screen
7. The Summary tab
8. Mobile view of the home page (375px width)

Send those when convenient and I'll do a second-pass critique with the same level of specificity, but tied to actual current state instead of inferred patterns.

---

*End of brief.*
