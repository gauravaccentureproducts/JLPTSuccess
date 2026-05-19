# JLPT N5 Functional Specification - v3.1 Supplement  (REDUCED TO REDIRECT STUB)

**Status:** **MERGED + SUPERSEDED on 2026-05-19.** The functional / governance
content of this supplement (sections A–F) was merged into the canonical
`specifications/JLPT-N5-Current-Implementation-Spec.md` (renamed to
"JLPT N5 — Functional & Implementation Specification" in the same revision).

**Where to read instead:** open
[`JLPT-N5-Current-Implementation-Spec.md`](./JLPT-N5-Current-Implementation-Spec.md)
— that is now the single canonical source-of-truth for "what the N5 app
is, how it's built, what governance + quality contracts apply." See §§ 26–38
of that document for the content merged out of this file.

**What remains here:** the *Zen Modern design system* (§G below) is
preserved unchanged at the bottom of this file because the canonical spec
points to it as a companion-document reference (§36 of the merged spec). A
future revision may extract §G to a standalone
`specifications/jlpt-n5-design-system-zen-modern.md`; until that happens,
this file is the canonical home of the design tokens.

**Git history note:** the full pre-merge content (sections A–F, plus the
historical errata + 2026-05-03 §F revision block + 2026-05-01 §B additions)
is preserved in the git history of this file. Use
`git log specifications/JLPT-N5-Functional-Spec-v3.1-supplement.md` from
before commit-of-merge to recover any specific paragraph if needed. A
backup copy is also at
`specifications/JLPT-N5-Functional-Spec-v3.1-supplement.md.bak_YYYY_MM_DD_pre_merge`.

---

## Subsection-by-subsection redirect map

| Old section in this supplement | Where it now lives |
|---|---|
| A.1 Sections missing from v3 | §§26–35 of merged spec |
| A.2 Drift v3 → current | Historical; resolved per §§3–25 of merged spec |
| B.1 Document control | §1 of merged spec |
| B.2 Glossary | §26 of merged spec |
| B.3 Stakeholders | §27 |
| B.4 User stories | §28 |
| B.5 Success metrics / KPIs | §29 |
| B.6.1 NFR-I Internationalization | §30.1 |
| B.6.2 NFR-W PWA | §30.2 |
| B.6.3 NFR-P Performance | §29 + §30.3 |
| B.6.4 NFR-A Accessibility | §30.4 |
| B.7 Test strategy | §19 + §25 + §32.2 |
| B.8 Risks register | §31 |
| B.9 Open questions / decisions log | Historical (workbook + verification.md) |
| B.10 Maintenance and support model | §32 |
| B.11 Release process | §32.3 |
| B.12 Copy voice contract | §33 |
| B.13 External-blocked items reframed | Historical (verification.md + IMP closures) |
| B.14 Pass 15a heuristic audit | §34.1 |
| B.15 Microinteractions vs Zen Modern | §35 |
| C.1 Scope movement (Audio, etc.) | §22 |
| C.2 Global navigation rewrite | §4.2 + §5.1 |
| C.3 §5 sub-sections | §5.1 – §5.16 |
| C.4 Drill / SRS Leitner → SM-2 → FSRS-4.5 | §5.9 + §5.10 + §22 |
| C.5 Data model additions | §7 + §8 |
| C.6 Repository structure | §3.1 |
| C.7 NFR replacement | §30 |
| C.8 Future enhancements rewrite | §23 |
| D Pass-N audit protocol | §34 |
| E Acceptance criteria for v4 | §37 |
| F.1 Mobile UI NFR-M1..M9 | §30.5 (extended with NFR-M10 / M11 on 2026-05-19) |
| F.2 Disabled-button feedback NFR-U | §30.6 |
| F.3 JA-25..JA-33 invariants | §25 (extended through JA-136+) |
| F.4 Anti-patterns AP-7..AP-10 | Procedure manual Appendix F + workbook tabs |
| F.5 Corpus state snapshot | §7.1 |
| F.6 New routes | §4.2 |
| F.7 SW version + PWA contract | §9 + §30.2 |
| F.8 Pass-N audit log | §34.1 |
| F.9 Procedure manual + companion docs | §32.4 + procedure manual itself |
| F.10 Open / deferred items snapshot | Historical (workbook + verification.md) |
| **G Design System Zen Modern** | **Preserved below in this file** (referenced by §36 of merged spec) |

---

## §G Design System (Zen Modern) - merged 2026-05-04

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

The version number must be read at runtime (e.g., from `package.json` or a build-time constant), not hardcoded. The "Updated [Month Year]" suffix from earlier drafts is dropped - the changelog link replaces that affordance. "What's new" links to the in-app `#/changelog` route which renders the markdown changelog with the app's typography; never to a raw `.md` file on GitHub.

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
