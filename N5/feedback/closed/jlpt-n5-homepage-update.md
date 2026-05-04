# JLPT N5 Tutor - Homepage Copy Update

**Date:** 2026-05-02
**Scope:** Homepage (`#/home`) only. Nothing else.

This document is for the developer / coding agent. Read it end to end before doing anything. The work happens in two steps, in this order:

- **Step 1:** Update the design-system markdown to reflect the new homepage rules.
- **Step 2:** Apply the changes to the actual homepage.

Do not skip Step 1. The design-system document is the source of truth; the rendered page must match it. If you change the page first, the spec drifts and future contributors will not know which is canonical.

---

## Step 1: Update the design system

**File to edit:** `C:\Users\gaurav.l.srivastava\Documents\VS Code\JLPT\N5\specifications\jlpt-n5-design-system-zen-modern.md`

Make the following changes inside that file. Each change is described as "what to find, what to replace it with."

### 1.1 §0 Design principles - add an eleventh principle

**Find:** the numbered list of 10 design principles in §0.

**Add as principle 11:**

> 11. **Describe the contents. Offer no opinion about them.** Homepage copy is neutral and inventorial. No outcome claims, no second-person, no verbs of encouragement, no trust reassurance, no superlatives, no quantifier softeners. Counts are bare numerals plus nouns. The product is a study material; the copy says what it is, not what it does for the visitor.

This becomes the eleventh rule. The "If a proposed change would violate any of these, the proposed change is wrong" sentence at the end of §0 then covers this rule too.

### 1.2 §4.1 Header - reduce primary nav from four items to two

**Find:** the header HTML and CSS example in §4.1, specifically the `<nav class="primary-nav">` block:

```html
<nav class="primary-nav">
  <a href="#/learn">Learn</a>
  <a href="#/practice">Practice</a>
  <a href="#/review" class="has-badge">Review<span class="badge">12</span></a>
  <a href="#/test">Test</a>
</nav>
```

**Replace with:**

```html
<nav class="primary-nav">
  <a href="#/learn">Learn</a>
  <a href="#/test">Test</a>
</nav>
```

**Find:** the `.badge` CSS rule and any `.has-badge` references in §4.1.

**Action:** keep the CSS in place (it's used elsewhere in the app), but remove the homepage-nav badge example and the `has-badge` class from the example HTML.

**Find:** the brand-mark example showing `<span class="brand-mark lang-ja">五</span>`.

**Action:** no change. The mark stays.

**Find:** the brand-name example showing `<span class="brand-name">JLPT N5</span>`.

**Action:** no change.

### 1.3 §5.1 Home page - rewrite the layout description and ASCII mock

**Find:** the entire §5.1 "Home (landing)" section, including the "Layout:" ASCII mock and the "Specific rules for this page:" bullet list.

**Replace the layout block with this:**

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

**Replace the "Specific rules for this page" bullets with this list:**

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

**Remove the existing §5.1 paragraph that begins** "The headline wraps to two lines deliberately. Don't stretch the container to put it on one line - the wrap is a design feature." This refers to the old "Pass JLPT N5 with 15 minutes a day" headline and is now obsolete.

**Remove the existing §5.1 paragraph about the stats sub-line** with middle-dot separators (`<span> · </span>`). The new inventory uses one-per-line, no separators.

**Remove the existing §5.1 paragraph that begins** "Trust line ('Works offline · ...') sits BELOW the CTA, not above." There is no trust line and no CTA in the new design.

**Remove the existing §5.1 paragraph about** "Returning users (localStorage shows progress): replace the hero with a 'Pick up where you left off' card." Replaced by the resume-strip rule above.

### 1.4 §5.1 Home page - add a new "Copy register" subsection

**At the end of §5.1, add:**

```
### 5.1.1 Copy register (mandatory)

The homepage is the most-seen surface in the app. Its copy sets the
register for everything else. The rules:

1. Describe the contents. Offer no opinion about them.
2. No outcome claims. The product is a study material, not a promise.
3. No second-person ("you", "your"). Use noun phrases or impersonal sentences.
4. No verbs of encouragement ("start", "begin", "explore", "discover").
5. No trust reassurance ("works offline", "no login", "privacy-first")
   on the homepage. Those properties live in About / Privacy.
6. No service-encounter politeness ("please", "feel free to").
7. Counts are bare numerals plus nouns. No "~1000", no "1000+",
   no "carefully selected", no "all".
8. No superlatives: best, most comprehensive, complete, definitive.
9. No flattering self-description: clean, minimal, elegant,
   distraction-free. The design demonstrates these; the copy must
   not assert them.
10. Sentence case throughout. ALL CAPS only for the small letter-spaced
    section labels.

If a proposed homepage string violates any of these, the string is wrong.

The same register applies to all homepage variants: light mode, dark
mode, mobile, returning-user, and translated locales.
```

### 1.5 §5.2 Learn index - update to reflect two-card homepage

**Find:** any reference in §5.2 that says or implies that the Learn index lives behind a single homepage card.

**Action:** confirm §5.2 still describes the Learn page itself (the page reached by clicking the Learn card). If §5.2 contains language like "the Learn card on the homepage links here", that's accurate and stays. If §5.2 contains language about a 5-card homepage grid linking to individual sections, that's now wrong and should be updated to clarify that the homepage has only two cards (Learn / Test) and that the five sections (Grammar / Vocabulary / Kanji / Reading / Listening) live inside the Learn page.

### 1.6 §11 Footer - confirm copy

**Find:** the footer HTML example in §5.11 (or §11, depending on numbering) showing:

```html
<p class="footer-meta">v1.5.0 · Updated April 2026</p>
```

**Replace with:**

```html
<p class="footer-meta">v1.8.9 · What's new</p>
```

**Note:** the version number in the footer must be read at runtime from `package.json` or equivalent. Do not hardcode `1.8.9`. Drop the "Updated [Month Year]" suffix - it's not a homepage concern. "What's new" is a link, rendered as part of `.footer-nav` not `.footer-meta`. Adjust the example HTML accordingly.

### 1.7 §11 Footer - confirm "What's new" links to an in-app surface, not raw markdown

**Find:** any reference to `What's new` linking to a `.md` file on GitHub.

**Action:** replace with a link to `#/changelog` (an in-app modal or styled page). A user clicking "What's new" should not land on `https://github.com/.../CHANGELOG.md`. They should see the changelog rendered in the app's typography.

### 1.8 Save the file.

After all the above edits, save `jlpt-n5-design-system-zen-modern.md`. Verify zero em-dashes (`—`, U+2014) and zero en-dashes (`–`, U+2013) in the modified sections. Verify no emojis were added.

---

## Step 2: Apply the changes to the homepage

Only after Step 1 is saved and committed. The design system is now the source of truth; the page must match it.

### 2.1 Tab title

**Find:** in `index.html` (or wherever the `<title>` element lives):

```html
<title>JLPT N5 — study material</title>
```

**Replace with:**

```html
<title>JLPT N5</title>
```

The em-dash version is a project-policy violation. Drop the subtitle entirely.

### 2.2 Header

**Find:** the primary nav component (in `js/components/header.js`, `index.html`, or wherever it's rendered).

**Action:** remove the Practice and Review nav links. The final list is:

```html
<a href="#/learn">Learn</a>
<a href="#/test">Test</a>
```

The right cluster (search input, Summary link, cog icon) does not change. Confirm the cog uses an SVG icon, not the word "Settings" and not a Unicode `⚙` glyph.

### 2.3 Hero block

**Find:** the hero card on `#/home` containing "Pass JLPT N5 with 15 minutes a day" or any equivalent marketing-register headline, the stats line with middle-dot separators, the trust line ("Works offline · No login required · Your progress stays on this device"), and the primary "Start your first lesson" / "Take a placement check" button pair.

**Replace with:**

```html
<section class="hero">
  <h1 class="hero-headline">JLPT N5 study material.</h1>
  <ul class="hero-inventory">
    <li>187 grammar patterns.</li>
    <li>1,003 vocabulary items.</li>
    <li>106 kanji.</li>
    <li>30 reading passages.</li>
    <li>12 listening drills.</li>
  </ul>
</section>
```

**Implementation requirements:**

- The five counts must be read at runtime from `data/grammar.json`, `data/vocab.json`, `data/kanji.json`, `data/reading.json`, `data/listening.json` `_meta.entity_count` fields. Do not hardcode.
- Use `Intl.NumberFormat('en-US')` or equivalent to render `1003` as `1,003`.
- The `<ul>` must have `list-style: none; padding: 0` and each `<li>` must render as a normal sentence, not a bulleted item.
- The `<h1>` uses `.h1` class per design system §2.6: `--text-2xl` weight 300.
- The `<ul>` uses `--text-base` weight 400 with one line per item.

### 2.4 Sections grid

**Find:** the existing card grid on `#/home`.

**Replace with two cards:**

```html
<section class="sections">
  <header class="section-label">
    <span class="section-label-text">SECTIONS</span>
    <span class="section-label-rule"></span>
  </header>
  <div class="learn-grid">
    <a class="card card-link" href="#/learn">
      <p class="card-index">01</p>
      <h3 class="card-title">Learn</h3>
      <p class="card-meta">Grammar, vocabulary, kanji, reading, listening.</p>
      <span class="card-arrow" aria-hidden="true">→</span>
    </a>
    <a class="card card-link" href="#/test">
      <p class="card-index">02</p>
      <h3 class="card-title">Test</h3>
      <p class="card-meta">15-question mock exam.</p>
      <span class="card-arrow" aria-hidden="true">→</span>
    </a>
  </div>
</section>
```

**Implementation requirements:**

- Two-column grid on desktop, stacked on mobile. Use `grid-template-columns: repeat(2, 1fr)` with a media query collapsing to `1fr` below 768px.
- No "Browse" text label. The `→` chevron is the affordance.
- Card hover state per design system §4.3: lighten background to `--color-surface-alt`, darken border slightly. No transform, no shadow.

### 2.5 Below the grid

**Find:** the existing "Already partway through? Take the placement check above so you don't repeat what you know." sentence (or any equivalent helper line).

**Replace with:**

```html
<p class="placement-link">
  <a href="#/placement">Placement check available.</a>
</p>
```

**Implementation requirements:**

- Inline link. The whole sentence is the link.
- Link styling: color `--color-text` (NOT browser-default purple/blue), text-decoration `none` by default, `underline` on hover only. The underline color uses `--color-text-muted` for the hairline feel.
- No icon. No heading above. No explanatory clause.

### 2.6 Resume strip (returning users)

**Find:** any existing "Pick up where you left off" element.

**Replace with a conditionally rendered strip ABOVE the SECTIONS label:**

```html
<a class="resume-strip" href="#/learn/[resumption-target]" hidden>
  Last session: <span class="resume-section">[section name]</span>,
  <span class="resume-topic">[topic]</span>.
  <span class="resume-progress">[N]</span> of
  <span class="resume-total">[M]</span>.
</a>
```

**Implementation requirements:**

- Render only if `localStorage.getItem('jlpt-n5-last-session')` (or equivalent key) is not null. Otherwise the element has the `hidden` attribute set.
- The whole element is a single anchor; no nested links.
- Styling: muted background (`--color-surface`), hairline border, single line of text, no icons.
- No fallback message for first-time visitors. The strip is invisible.

### 2.7 Footer

**Find:** the existing footer.

**Confirm the structure matches:**

```html
<footer class="app-footer">
  <div class="container footer-grid">
    <p class="footer-meta">v1.8.9</p>
    <nav class="footer-nav">
      <a href="#/changelog">What's new</a>
      <a href="#/privacy">Privacy</a>
      <a href="https://github.com/[user]/[repo]">Source on GitHub</a>
    </nav>
  </div>
</footer>
```

**Implementation requirements:**

- Version number (`1.8.9`) is read at runtime from `package.json` or equivalent. Do not hardcode.
- Drop the `Updated [Month Year]` suffix.
- "What's new" links to `#/changelog`, an in-app surface. NOT to a raw `.md` file on GitHub.
- The three links in `.footer-nav` are separated by middle-dots with spaces in the rendered output (`What's new · Privacy · Source on GitHub`). Implement via CSS or inline separators - whatever the existing footer uses.

### 2.8 Visual regression check

After applying §2.1 through §2.7:

1. Load `#/home` in light mode. Confirm it matches the ASCII layout in §5.1 of the updated design system.
2. Load it in dark mode. Confirm token parity.
3. Resize to 375px (mobile). Confirm cards stack, inventory list does not wrap awkwardly, no horizontal scroll.
4. Resize to 768px (tablet). Confirm two-column card grid still works.
5. Resize to 1280px (desktop). Confirm container is centered at 880px max-width with generous side margins.
6. Open DevTools, search the rendered HTML and CSS for any of the strings listed in §3 below. Confirm zero matches.

### 2.9 Strings to remove (audit checklist)

Run a grep across the homepage source files (HTML, JS templates, locale files) and confirm none of these strings appear on the home page after the change:

- `Pass JLPT N5`
- `15 minutes a day`
- `Start your first lesson`
- `Take a placement check` (the verb-led version; the noun version "Placement check available" is the new copy)
- `Works offline`
- `No login required`
- `Your progress stays on this device`
- `Pick up where you left off`
- `Already partway through`
- `pick a section`
- `Browse →` (button text inside cards)
- `Practice` (in primary nav)
- `Review` (in primary nav)
- `Daily mixed drills`
- `spaced-repetition Review`
- `Updated [Month] [Year]` in the footer
- Any em-dash `—` (U+2014)
- Any en-dash `–` (U+2013)
- Any emoji
- `Search...` (with ellipsis; the placeholder is the single word `Search`)

If any match is found, remove it. If a match cannot be removed without breaking another surface, the design system needs to be updated first - go back to Step 1.

---

## Definition of done

This work is complete when:

1. `jlpt-n5-design-system-zen-modern.md` has been updated per Step 1 and saved.
2. The homepage has been updated per Step 2 and renders correctly in light mode, dark mode, and at all three viewport breakpoints.
3. The audit checklist in §2.9 returns zero matches.
4. A reader unfamiliar with the project loads the homepage and reports that nothing on it sounds like marketing copy.
5. A `git diff` of the design-system markdown and the homepage source files corresponds 1:1 to the changes described in this document. No unscoped edits.

If anything in this document is ambiguous or contradicts an existing design-system rule, stop and surface the ambiguity. Do not improvise.

---

*End of update. Prepared 2026-05-02. Homepage scope only.*
