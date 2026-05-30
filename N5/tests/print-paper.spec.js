// IMP-6 first-wave: dedicated test coverage for js/print-paper.js
//
// Recent BUG history (3 PDF defects in 2 weeks motivated this spec):
//   - BUG-226: audio timer (0:00/0:00) + play/skip/rate buttons
//              appearing in PDF export
//   - BUG-227: small empty square/checkbox under each grammar example
//              in PDF export
//   - BUG-228: large blank-space zones at page boundaries in grammar
//              pattern PDFs (5pp where 3pp expected)
//
// js/print-paper.js renders #/print/<paperId> in a layout designed
// for paper consumption rather than the screen. Key invariants:
//   - @media print hides all web chrome (.primary-nav, .site-footer,
//     .skip-link, anything outside .print-paper-root)
//   - Page-break before each mondai cluster
//   - A4 size, 11pt body, no audio controls in the printed flow
//
// Playwright can't actually generate a PDF for inspection (would need
// browser print-to-PDF API), but it CAN:
//   - Verify the .print-paper-root element exists
//   - Verify @media print CSS rules apply when the print media query
//     is emulated (`page.emulateMedia({ media: 'print' })`)
//   - Verify no <audio> player controls render inside the print root
//   - Verify the page has expected mondai structure

const { test, expect } = require('@playwright/test');

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    try { localStorage.setItem('jlpt-n5-tutor:onboardingSeen', '1'); } catch {}
  });
});

test.describe('print-paper — js/print-paper.js', () => {

  // Use a paper ID that we know exists. data/papers/bunpou/paper-1.json
  // is the canonical first paper. The print route accepts paper IDs in
  // multiple forms; test the SPA hash route.
  const PAPER_ROUTE = '/#/print/bunpou-1';

  test('print route resolves and renders .print-paper-root', async ({ page }) => {
    await page.goto(PAPER_ROUTE);
    await page.waitForLoadState('networkidle');
    const root = page.locator('.print-paper-root');
    await expect(root).toBeVisible();
  });

  test('BUG-226 regression guard: no audio-player controls inside .print-paper-root', async ({ page }) => {
    await page.goto(PAPER_ROUTE);
    await page.waitForLoadState('networkidle');
    // The 3 buttons our audio-player.js renders: skip-back, play, skip-fwd
    // None should appear inside the print root.
    const audioBtns = page.locator('.print-paper-root button[aria-label="Play or pause"], .print-paper-root button[aria-label="Skip back 5 seconds"], .print-paper-root button[aria-label="Skip forward 5 seconds"]');
    const count = await audioBtns.count();
    expect(count, 'audio-player controls must not appear in printed paper layout (BUG-226 regression)').toBe(0);
    // Also no <audio> element with controls attribute exposed in print mode
    const audioControls = page.locator('.print-paper-root audio[controls]');
    const ac = await audioControls.count();
    expect(ac, 'native <audio controls> must not be in print layout').toBe(0);
  });

  test('BUG-227 regression guard: no orphan checkboxes under grammar examples', async ({ page }) => {
    await page.goto(PAPER_ROUTE);
    await page.waitForLoadState('networkidle');
    // BUG-227: stray <input type="checkbox"> rendered under each example
    // inside the print root. They shouldn't be there in print layout.
    const checkboxes = page.locator('.print-paper-root input[type="checkbox"]');
    const count = await checkboxes.count();
    expect(count, 'orphan checkboxes must not appear in printed paper (BUG-227 regression)').toBe(0);
  });

  test('@media print emulation: web chrome is hidden', async ({ page }) => {
    await page.goto(PAPER_ROUTE);
    await page.waitForLoadState('networkidle');
    // Emulate print media to verify @media print rules apply.
    await page.emulateMedia({ media: 'print' });
    // .primary-nav (header nav) should be display:none in print
    const nav = page.locator('.primary-nav').first();
    if (await nav.count() > 0) {
      const display = await nav.evaluate(el => getComputedStyle(el).display);
      expect(display, '.primary-nav must be hidden under @media print').toBe('none');
    }
    // .site-footer should also be hidden
    const footer = page.locator('.site-footer').first();
    if (await footer.count() > 0) {
      const display = await footer.evaluate(el => getComputedStyle(el).display);
      expect(display, '.site-footer must be hidden under @media print').toBe('none');
    }
  });

  test('paper renders the mondai cluster structure (heading + questions)', async ({ page }) => {
    await page.goto(PAPER_ROUTE);
    await page.waitForLoadState('networkidle');
    const root = page.locator('.print-paper-root');
    await expect(root).toBeVisible();
    // At least one heading-style label inside the print root
    // (could be h2/h3/h4/.mondai-heading depending on convention)
    const headings = root.locator('h2, h3, h4, .mondai-heading, [class*="mondai"]');
    const hCount = await headings.count();
    expect(hCount, 'print paper should have at least 1 mondai heading element').toBeGreaterThanOrEqual(1);
  });

  test('no console errors on print page load', async ({ page }) => {
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    await page.goto(PAPER_ROUTE);
    await page.waitForLoadState('networkidle');
    expect(errors, `Console errors on print page: ${errors.join('\n')}`).toEqual([]);
  });

});
