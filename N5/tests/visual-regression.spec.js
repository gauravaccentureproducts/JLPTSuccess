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
];

const VIEWPORTS = [
  { name: 'desktop', width: 1280, height: 800 },
  { name: 'mobile',  width: 375,  height: 812 },
];

test.describe('Visual regression — homepage + canonical routes', () => {
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
