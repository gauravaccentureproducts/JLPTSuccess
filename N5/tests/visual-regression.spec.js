// Visual-regression smoke per feedback/ui-testing-plan.md §16 + DEFER-6.
//
// Captures screenshots of the 6 routes that drive the most page-paint risk
// (home / learn hub / grammar TOC / kanji index / reading list / settings).
// Compares against committed baselines in tests/__screenshots__. First run
// after a layout change should be `npx playwright test --update-snapshots`.
//
// Why scoped this narrowly: visual-regression with full coverage breeds
// flakes (font-rendering, scrollbar width, cursor blink). The 6 routes
// here cover every CSS layout shipped (3-col grid, 2-col grid, card
// matrix, list, form, single-pane). New routes don't need a separate
// snapshot unless they introduce a new layout pattern.
//
// Animations are disabled per-test via `prefers-reduced-motion: reduce`
// emulation; the runner waits for `networkidle` so PWA-cache warm-up
// doesn't paint differently between baseline and run.
const { test, expect } = require('@playwright/test');

const ROUTES = [
  { path: '/',                      slug: 'home' },
  { path: '/#/learn',               slug: 'learn-hub' },
  { path: '/#/learn/grammar',       slug: 'learn-grammar-toc' },
  { path: '/#/kanji',               slug: 'kanji-index' },
  { path: '/#/reading',             slug: 'reading-list' },
  { path: '/#/settings',            slug: 'settings' },
  // ISSUE-045 / IMP-065 (audit round-5): coverage for the round-3/4
  // surfaces that previously had zero pixel-drift protection.
  { path: '/#/missed',              slug: 'missed-empty' },
  { path: '/#/sitting',             slug: 'sitting-picker' },
  { path: '/#/test',                slug: 'test-setup' },
  // ISSUE-072 (audit round-9): expanded coverage to highest-traffic
  // surfaces previously uncovered. These three close out the
  // "no visual-regression on home/settings/vocab list" finding.
  { path: '/#/learn/vocab',         slug: 'vocab-list' },
  { path: '/#/listening',           slug: 'listening-list' },
  { path: '/#/papers',              slug: 'papers-list' },
  { path: '/#/drill',               slug: 'drill-setup' },
  { path: '/#/review',              slug: 'review-empty' },
  { path: '/#/summary',             slug: 'summary' },
];

const VIEWPORTS = [
  { name: 'desktop', width: 1280, height: 800 },
  { name: 'mobile',  width: 375,  height: 812 },
];

// 2026-05-21: visual-regression suite is gated to local-only runs.
//
// The committed baselines under tests/visual-regression.spec.js-snapshots/
// were all generated on Windows (file suffix `-win32.png`). When CI runs
// on ubuntu-latest, Playwright looks for `-linux.png` baselines — none
// exist — and reports "snapshot doesn't exist, writing actual" for each
// of the ~76 viewport×project×OS combinations, surfacing as 38 unique
// failures.
//
// The right fix is a CI workflow_dispatch input that runs the suite
// with `--update-snapshots` and uploads the new Linux PNGs as an
// artifact for committing. That's a separate piece of work and the
// rest of the smoke suite is being unblocked first. Until then this
// suite runs locally (where the win32 baselines apply) and is skipped
// on CI.
//
// Tracking: tests/visual-regression.spec.js Linux-baseline regen
// will be its own commit + workflow_dispatch addition.
test.describe('Visual regression - homepage + canonical routes', () => {
  // Skip on CI until Linux baselines land.
  // Two gates:
  //   - On CI without an explicit update opt-in, skip (baselines
  //     are -win32.png and the runner is Linux).
  //   - Opt-in via workflow_dispatch input `update_snapshots: true`
  //     sets PLAYWRIGHT_UPDATE_SNAPSHOTS=true → suite runs with
  //     --update-snapshots so missing baselines get written.
  test.skip(
    !!process.env.CI && process.env.PLAYWRIGHT_UPDATE_SNAPSHOTS !== 'true',
    'Visual-regression baselines are -win32.png; Linux baselines need workflow_dispatch update_snapshots run. See file header.'
  );
  for (const vp of VIEWPORTS) {
    for (const route of ROUTES) {
      test(`${route.slug} @ ${vp.name}`, async ({ page }) => {
        await page.setViewportSize({ width: vp.width, height: vp.height });
        await page.emulateMedia({ reducedMotion: 'reduce' });
        await page.goto(route.path);
        await page.waitForLoadState('networkidle');
        // Mask the streak / daily-status row on home: it changes daily,
        // which would flake the baseline. Other routes have no
        // time-dependent content.
        const masks = route.slug === 'home'
          ? [page.locator('.syllabus-daily-status')]
          : [];
        await expect(page).toHaveScreenshot(`${route.slug}-${vp.name}.png`, {
          fullPage: true,
          mask: masks,
          // Pixel-diff threshold: 0.1% of pixels can differ before fail.
          // Calibrated to absorb sub-pixel font rendering between runs
          // while still catching real layout regressions (e.g. a card
          // shifted 4px would blow past 0.1%).
          maxDiffPixelRatio: 0.001,
          animations: 'disabled',
        });
      });
    }
  }
});

// ISSUE-072 (audit round-9) — Hindi locale visual regression coverage.
// Catches Devanagari-rendering regressions (font-fallback, line-height,
// reflow with Hindi glyphs which have a taller base box than Latin
// fonts) on the highest-traffic surfaces. Localised UI strings ship
// in N5/locales/hi.json; the actual Devanagari rendering depends on
// the system font stack, so a baseline locks the rendered look.
const HINDI_ROUTES = [
  { path: '/',                      slug: 'home-hi' },
  { path: '/#/learn',               slug: 'learn-hub-hi' },
  { path: '/#/settings',            slug: 'settings-hi' },
  { path: '/#/learn/vocab',         slug: 'vocab-list-hi' },
];

test.describe('Visual regression - Hindi locale (Devanagari)', () => {
  // Same CI gate as the main visual-regression describe above. See
  // the file-header comment for the win32 → linux baseline migration plan.
  // Two gates:
  //   - On CI without an explicit update opt-in, skip (baselines
  //     are -win32.png and the runner is Linux).
  //   - Opt-in via workflow_dispatch input `update_snapshots: true`
  //     sets PLAYWRIGHT_UPDATE_SNAPSHOTS=true → suite runs with
  //     --update-snapshots so missing baselines get written.
  test.skip(
    !!process.env.CI && process.env.PLAYWRIGHT_UPDATE_SNAPSHOTS !== 'true',
    'Visual-regression baselines are -win32.png; Linux baselines need workflow_dispatch update_snapshots run. See file header.'
  );
  for (const vp of VIEWPORTS) {
    for (const route of HINDI_ROUTES) {
      test(`${route.slug} @ ${vp.name}`, async ({ page }) => {
        await page.setViewportSize({ width: vp.width, height: vp.height });
        await page.emulateMedia({ reducedMotion: 'reduce' });
        // Pre-set the locale before the first paint so the Hindi
        // shell renders immediately. The localStorage key matches
        // the JA-37 namespace invariant.
        await page.goto('/');
        await page.evaluate(() => {
          localStorage.setItem(
            'jlpt-n5-tutor:settings',
            JSON.stringify({ locale: 'hi' })
          );
        });
        await page.goto(route.path);
        await page.waitForLoadState('networkidle');
        const masks = route.slug === 'home-hi'
          ? [page.locator('.syllabus-daily-status')]
          : [];
        await expect(page).toHaveScreenshot(`${route.slug}-${vp.name}.png`, {
          fullPage: true,
          mask: masks,
          maxDiffPixelRatio: 0.002,  // slightly more tolerance for
                                     // Devanagari font-rendering variation
          animations: 'disabled',
        });
      });
    }
  }
});
