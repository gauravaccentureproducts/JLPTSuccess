// P0 smoke tests for JLPT N4 Tutor.
//
// Goal: catch regressions in core navigation, primary content routes
// (Grammar / Vocab / Kanji / Test), and accessibility. Runs under 60s on
// a clean machine. Wired into CI as a release gate.

const { test, expect } = require('@playwright/test');
const AxeBuilder = require('@axe-core/playwright').default;

test.describe('P0 smoke - core navigation', () => {
  test('home loads with no console errors', async ({ page }) => {
    const errors = [];
    page.on('pageerror', e => errors.push(e.message));
    page.on('console', m => { if (m.type() === 'error') errors.push(m.text()); });

    await page.goto('/');
    await expect(page).toHaveTitle('JLPT N4');
    await expect(page.locator('.brand-link')).toContainText('JLPT N4');

    // Wait for the app shell to render (skeleton → real content).
    // The home route renders syllabus cards.
    await page.waitForSelector('.syllabus-card, .home-pillar, h2, h1', { timeout: 10_000 });

    // Allow router/SW errors that are benign (favicon, optional assets).
    const real = errors.filter(e =>
      !/favicon|manifest|404/i.test(e)
    );
    expect(real).toEqual([]);
  });

  test('brand-link routes to level picker', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    await page.click('.brand-link');
    await expect(page).toHaveURL(/#\/levels/);
    // Both N5 and N4 should be available; N3-N1 disabled.
    await page.waitForSelector('.level-card, [data-level]', { timeout: 5_000 });
  });

  test('grammar route renders patterns', async ({ page }) => {
    await page.goto('/#/learn/grammar');
    await page.waitForLoadState('networkidle');
    // The catalogue should expose some text content from the 129 N4 patterns.
    const body = await page.locator('main').innerText();
    expect(body.length).toBeGreaterThan(100);
  });

  test('vocab route renders entries', async ({ page }) => {
    await page.goto('/#/learn/vocab');
    await page.waitForLoadState('networkidle');
    const body = await page.locator('main').innerText();
    expect(body.length).toBeGreaterThan(100);
  });

  test('kanji route renders glyphs', async ({ page }) => {
    await page.goto('/#/kanji');
    await page.waitForLoadState('networkidle');
    const body = await page.locator('main').innerText();
    expect(body.length).toBeGreaterThan(100);
  });

  test('test route renders mock-test entry point', async ({ page }) => {
    await page.goto('/#/test');
    await page.waitForLoadState('networkidle');
    const body = await page.locator('main').innerText();
    expect(body.length).toBeGreaterThan(50);
  });
});

test.describe('P0 smoke - data integrity', () => {
  test('whitelist + grammar + vocab + kanji JSON load successfully', async ({ page }) => {
    const failures = [];
    page.on('response', resp => {
      if (resp.url().includes('/data/') && resp.url().endsWith('.json')) {
        if (!resp.ok()) failures.push(`${resp.status()} ${resp.url()}`);
      }
    });
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    expect(failures).toEqual([]);
  });

  test('listening MP3 is reachable', async ({ page }) => {
    const resp = await page.request.get('/audio/listening/n4.listen.001.mp3');
    expect(resp.status()).toBe(200);
  });

  test('kanji SVG is reachable', async ({ page }) => {
    // 会 is in the N5 prereq whitelist - URL-encoded
    const resp = await page.request.get('/svg/kanji/' + encodeURIComponent('会') + '.svg');
    expect(resp.status()).toBe(200);
  });

  test('paper manifest loads with 28 papers', async ({ page }) => {
    const resp = await page.request.get('/data/papers/manifest.json');
    expect(resp.ok()).toBe(true);
    const m = await resp.json();
    // manifest schema v3: { schema_version, totalPapers, totalQuestions, categories }
    expect(m.schema_version).toBeDefined();
    expect(m.totalPapers).toBe(28);
    expect(m.totalQuestions).toBeGreaterThanOrEqual(400);
  });
});

test.describe('P0 smoke - accessibility', () => {
  test('home has no serious/critical axe violations', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const results = await new AxeBuilder({ page })
      .withTags(['wcag2a', 'wcag2aa'])
      .analyze();
    const blocking = results.violations.filter(
      v => v.impact === 'serious' || v.impact === 'critical'
    );
    if (blocking.length) {
      console.log('Axe violations:', JSON.stringify(blocking, null, 2));
    }
    expect(blocking).toEqual([]);
  });
});

test.describe('P0 smoke - PWA basics', () => {
  test('service worker registers', async ({ page }) => {
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const swRegistered = await page.evaluate(async () => {
      if (!('serviceWorker' in navigator)) return false;
      const reg = await navigator.serviceWorker.getRegistration();
      return !!reg;
    });
    expect(swRegistered).toBe(true);
  });

  test('manifest is valid JSON', async ({ page }) => {
    const resp = await page.request.get('/manifest.webmanifest');
    expect(resp.ok()).toBe(true);
    const m = await resp.json();
    expect(m.name || m.short_name).toMatch(/N4/i);
  });
});
