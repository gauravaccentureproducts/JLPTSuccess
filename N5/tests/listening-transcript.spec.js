// IMP-6 second wave: tests/listening-transcript.spec.js
//
// js/listening-transcript.js: optional listening transcript-aligned
// playback renderer (IMP-070, audit round-6).
//
// When listening.json item has `lines: [{ text_ja, startMs? }, ...]`,
// the rendered transcript shows each line as a separate row. With
// startMs, the row is click-to-seek + auto-highlighted in sync with
// audio current time. Without startMs, the row stays static text.
//
// No standalone route — exercised on the /#/listening listing or
// individual items.

const { test, expect } = require('@playwright/test');

test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    try { localStorage.setItem('jlpt-n5-tutor:onboardingSeen', '1'); } catch {}
  });
});

test.describe('listening-transcript — js/listening-transcript.js', () => {

  async function gotoListening(page) {
    await page.goto('/#/listening');
    await page.waitForFunction(
      () => (document.querySelector('main')?.textContent || '').length > 100,
      { timeout: 20000 }
    ).catch(() => {});
  }

  test('listening page loads and renders content', async ({ page }) => {
    await gotoListening(page);
    const mainText = await page.locator('main').textContent();
    expect(mainText.length, 'listening page should render substantive content').toBeGreaterThan(50);
  });

  test('no console errors on listening page (excluding benign chatter)', async ({ page }) => {
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });
    await gotoListening(page);
    const real = errors.filter(e =>
      !e.includes('downloadable font') &&
      !e.includes('Failed to load resource') &&
      !e.includes('favicon') &&
      !e.includes('preload')
    );
    expect(real, `Console errors: ${real.join('\n')}`).toEqual([]);
  });

});
