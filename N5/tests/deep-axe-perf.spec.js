// W5.2 — Deep axe-core a11y + perf checks beyond P0 home-route.
//
// Walks key surfaces (grammar list, pattern detail, kanji index,
// reading index, listening index, learn hub, drill) and runs:
//   1. axe-core scan (WCAG 2.1 AA, color-contrast included)
//   2. Performance measurements (DOMContentLoaded, load, FCP-proxy)
//
// Reports per-page. Fails if a page has critical/serious a11y violations
// or load takes > 5s on local dev server.

const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

const PAGES = [
  { name: 'home',           url: '/',                       maxLoadMs: 5000 },
  { name: 'grammar list',   url: '/learn/grammar/',         maxLoadMs: 5000 },
  { name: 'pattern detail', url: '/learn/n5-001/',          maxLoadMs: 5000 },
  { name: 'pattern w/ exp', url: '/learn/n5-098/',          maxLoadMs: 5000 },  // has explanation_ja
  { name: 'kanji index',    url: '/kanji/',                 maxLoadMs: 5000 },
  { name: 'reading index',  url: '/reading/',               maxLoadMs: 5000 },
  { name: 'listening idx',  url: '/listening/',             maxLoadMs: 5000 },
  { name: 'drill',          url: '/drill/',                 maxLoadMs: 5000 },
];

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    try { localStorage.setItem('jlpt-n5-tutor:onboardingSeen', '1'); } catch {}
  });
});

for (const p of PAGES) {
  test(`a11y deep — ${p.name} (${p.url}) — no critical/serious axe violations`, async ({ page }) => {
    await page.goto(p.url);
    await page.waitForLoadState('networkidle');
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa'])
      .analyze();
    const critical = results.violations.filter(v => v.impact === 'critical');
    const serious = results.violations.filter(v => v.impact === 'serious');
    // Report all for log
    if (results.violations.length > 0) {
      console.log(`[${p.name}] axe violations (${results.violations.length}):`);
      for (const v of results.violations.slice(0, 5)) {
        console.log(`  [${v.impact}] ${v.id}: ${v.help}`);
      }
    }
    expect(critical, `${p.name}: ${critical.length} critical axe violations`).toHaveLength(0);
    expect(serious, `${p.name}: ${serious.length} serious axe violations`).toHaveLength(0);
  });

  test(`perf — ${p.name} (${p.url}) — load < ${p.maxLoadMs}ms`, async ({ page }) => {
    const t0 = Date.now();
    await page.goto(p.url, { waitUntil: 'load' });
    const loadMs = Date.now() - t0;
    const navTiming = await page.evaluate(() => {
      const t = performance.timing;
      return {
        dom: t.domContentLoadedEventEnd - t.navigationStart,
        load: t.loadEventEnd - t.navigationStart,
      };
    });
    console.log(`[${p.name}] load=${loadMs}ms dom=${navTiming.dom}ms loadEvt=${navTiming.load}ms`);
    expect(loadMs, `${p.name} load=${loadMs}ms > ${p.maxLoadMs}ms`).toBeLessThan(p.maxLoadMs);
  });
}
