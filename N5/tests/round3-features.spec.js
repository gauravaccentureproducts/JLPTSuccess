// IMP-055 (audit round-4): regression coverage for the round-3 routes
// shipped in v1.12.30 + v1.12.31:
//   #/missed   - wrong-answer history
//   #/sitting  - full mock-paper sitting flow
//   home daily-goal progress + due-count surface
//   custom audio-player skin (skip ±5s + per-clip rate buttons)
//
// Plus round-4 surfaces:
//   home trust band (ISSUE-027 / IMP-048)
//   header locale-chip group (ISSUE-028)

const { test, expect } = require('@playwright/test');

// IMP-044 (2026-05-11) first-run onboarding redirects hash-less visits
// to #/diagnostic. Bypass via the onboardingSeen sentinel so tests
// hit the home / hash-explicit routes they actually assert against.
// See N5/js/app.js initApp() onboarding gate.
test.beforeEach(async ({ page }) => {
  await page.addInitScript(() => {
    try { localStorage.setItem('jlpt-n5-tutor:onboardingSeen', '1'); } catch {}
  });
});

test.describe('round-3 + round-4 surface regression', () => {

  // Trust-band test removed 2026-05-21: the `.syllabus-trust-band` +
  // `.trust-pill` UI was removed from the homepage in favor of in-card
  // niche-N2 messaging. Privacy/offline trust signals now live in the
  // footer `.footer-trust-strip` and on the level-picker landing page,
  // not on the per-level home. If the trust band is ever re-introduced
  // as a homepage block, restore the test from git history (round3-
  // features.spec.js prior to 2026-05-21).
  test.skip('home renders the trust band with 5 niche-N2 pills', () => {});

  // Hindi locale tab DISABLED for Phase-1 English-only launch (2026-05-24).
  // Hindi data retained in data/*.json + locales/hi.json for Phase-2;
  // the UI toggle is feature-flagged off. Tests skipped until Phase-2.
  // To re-enable: revert the feature-flag in js/i18n.js + remove the
  // .skip() here. See docs/AUDIT-COVERAGE-2026-05-24.md.
  test.skip('header has a locale toggle (EN ↔ HI) — redesigned 2026-05-09 (single icon-btn)', () => {});

  test.skip('clicking the locale toggle swaps the active locale to Hindi', () => {});

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
    // CTA copy was changed 2026-05-10 from "Start sitting" to
    // "Start full mock test →". The link target stays #/sitting.
    await expect(cta).toContainText('Start full mock test');
  });

  test('JSON-LD EducationalApplication schema present in head', async ({ page }) => {
    await page.goto('/');
    // IMP-142 (2026-05-09) added 2 more JSON-LD blocks (Course schema
    // for the N5 syllabus + BreadcrumbList). Find the
    // EducationalApplication block via page.evaluate() since Playwright's
    // locator.filter({ hasText }) only matches *visible* text and <script>
    // tags are display:none — the JSON content isn't considered visible.
    const data = await page.evaluate(() => {
      const scripts = Array.from(document.querySelectorAll('script[type="application/ld+json"]'));
      for (const s of scripts) {
        try {
          const j = JSON.parse(s.textContent);
          if (j['@type'] === 'EducationalApplication') return j;
        } catch {}
      }
      return null;
    });
    expect(data, 'EducationalApplication JSON-LD block must exist').not.toBeNull();
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
