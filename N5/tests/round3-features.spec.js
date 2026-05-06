// IMP-055 (audit round-4): regression coverage for the round-3 routes
// shipped in v1.12.30 + v1.12.31:
//   #/missed   — wrong-answer history
//   #/sitting  — full mock-paper sitting flow
//   home daily-goal progress + due-count surface
//   custom audio-player skin (skip ±5s + per-clip rate buttons)
//
// Plus round-4 surfaces:
//   home trust band (ISSUE-027 / IMP-048)
//   header locale-chip group (ISSUE-028)

const { test, expect } = require('@playwright/test');

test.describe('round-3 + round-4 surface regression', () => {

  test('home renders the trust band with 5 niche-N2 pills', async ({ page }) => {
    await page.goto('/');
    const band = page.locator('.syllabus-trust-band');
    await expect(band).toBeVisible();
    const pills = band.locator('.trust-pill');
    await expect(pills).toHaveCount(5);
    await expect(pills.nth(0)).toContainText('No login');
    await expect(pills.nth(1)).toContainText('No tracking');
    await expect(pills.nth(2)).toContainText('Works offline');
    await expect(pills.nth(3)).toContainText('Open source');
    await expect(pills.nth(4)).toContainText('100% on-device');
  });

  test('header has 2 locale chips (EN / HI) — narrowed 2026-05-06 per IMP-096', async ({ page }) => {
    await page.goto('/');
    const group = page.locator('#locale-chip-group');
    await expect(group).toBeVisible();
    const chips = group.locator('.locale-chip');
    await expect(chips).toHaveCount(2);
    const labels = await chips.allTextContents();
    expect(labels).toEqual(['EN', 'HI']);
    // EN is active for an EN-default browser context.
    await expect(chips.nth(0)).toHaveClass(/is-active/);
  });

  test('clicking the HI chip swaps the active locale to Hindi', async ({ page }) => {
    await page.goto('/');
    await page.locator('#locale-chip-group .locale-chip[data-lc="hi"]').click();
    // After click, HI chip should be active.
    await expect(page.locator('.locale-chip[data-lc="hi"]')).toHaveClass(/is-active/);
    await expect(page.locator('.locale-chip[data-lc="en"]')).not.toHaveClass(/is-active/);
  });

  test('#/missed shows the empty-state message when history is empty', async ({ page }) => {
    await page.goto('/#/missed');
    // First-paint: no wrong answers logged yet.
    await expect(page.locator('h2')).toContainText('Wrong-answer history');
    await expect(page.locator('.placeholder')).toContainText("haven't missed");
  });

  test('#/sitting picker shows 7 paper cards', async ({ page }) => {
    await page.goto('/#/sitting');
    await expect(page.locator('h2')).toContainText('Full mock-test sitting');
    const cards = page.locator('.sitting-paper-card');
    await expect(cards).toHaveCount(7);
    await expect(cards.first()).toContainText('Paper 1');
    await expect(cards.last()).toContainText('Paper 7');
  });

  test('home daily-status block is hidden for first-time visitors', async ({ page }) => {
    // Fresh context = no history / no streak. Daily-status should not render.
    await page.goto('/');
    await expect(page.locator('.syllabus-daily-status')).toHaveCount(0);
  });

  test('test setup CTA links to #/sitting', async ({ page }) => {
    await page.goto('/#/test');
    const cta = page.locator('.test-sitting-cta a[href*="sitting"]');
    await expect(cta).toBeVisible();
    await expect(cta).toContainText('Start sitting');
  });

  test('JSON-LD EducationalApplication schema present in head', async ({ page }) => {
    await page.goto('/');
    const ld = await page.locator('script[type="application/ld+json"]').textContent();
    expect(ld).toBeTruthy();
    const data = JSON.parse(ld);
    expect(data['@type']).toBe('EducationalApplication');
    expect(data.educationalLevel).toBe('JLPT N5');
    expect(data.isAccessibleForFree).toBe(true);
  });

  test('og:image + twitter:card meta tags present', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('meta[property="og:image"]')).toHaveAttribute('content', /icon-512\.png$/);
    await expect(page.locator('meta[name="twitter:card"]')).toHaveAttribute('content', 'summary_large_image');
  });

});
