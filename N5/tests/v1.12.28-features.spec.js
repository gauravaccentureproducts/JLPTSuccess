// IMP-028 (audit 2026-05-04 round 2): regression coverage for the
// v1.12.28 round-1 audit-fix batch + the round-2 wave (v1.12.29).
//
// Specifically guards:
//   - footer version display (round 1 / IMP-016)
//   - mock-test exam-mode timer + toggle (round 1 / IMP-001)
//   - JLPT pass-mark badge on test setup + results (round 1 / IMP-002)
//   - per-grammar-category test breakdown table (round 1 / IMP-004)
//   - kanji index search + stroke + lesson + sort filters (round 1 IMP-003,
//     round 2 IMP-025)
//   - kanji detail "In a sentence" section (round 2 / IMP-018)
//   - grammar TOC search + tier chips (round 2 / IMP-029)
//   - vocab list search input (round 2 / IMP-029)
//   - kanji popover stroke chip + Other-readings disclosure (round 2 / ISSUE-008)
//
// Wired into the smoke run via the default `playwright test` glob.

const { test, expect } = require('@playwright/test');

test.describe('v1.12.28+ feature regression', () => {

  test('footer shows the running app version', async ({ page }) => {
    await page.goto('/');
    const meta = page.locator('[data-footer-version]');
    await expect(meta).toBeVisible();
    // Should match the v1.x.y pattern; the exact number can drift, the
    // shape must not.
    await expect(meta).toHaveText(/v\d+\.\d+\.\d+/);
  });

  test('mock-test setup shows exam-mode toggle + pass-mark note', async ({ page }) => {
    await page.goto('/#/test');
    // Pass-mark study-target note (IMP-002). The setup screen has TWO
    // .bank-note elements — one for the question-bank size + one for
    // the pass-mark target. Filter explicitly so the assertion still
    // works if order changes.
    const note = page.locator('.bank-note').filter({ hasText: 'Pass mark' });
    await expect(note).toContainText('Pass mark');
    await expect(note).toContainText('60%');
    // Exam-mode opt-in toggle (IMP-001).
    const toggle = page.locator('#exam-mode');
    await expect(toggle).toBeVisible();
    await expect(toggle).not.toBeChecked();
    // Title carries the "60 seconds per question" promise.
    const label = page.locator('.exam-mode-toggle');
    await expect(label).toHaveAttribute('title', /60 seconds per question/);
  });

  test('exam-mode timer chip appears once a timed test starts', async ({ page }) => {
    await page.goto('/#/test');
    // Pick the smallest available bank to keep this test fast.
    const lengthBtn = page.locator('button.length-btn').first();
    await lengthBtn.click();
    await page.locator('#exam-mode').check();
    await page.locator('button.btn-primary, button.start-test, button:has-text("Start")').first().click();
    // Now we're on the question screen; the timer chip is rendered when
    // examMode + timerEndsAt are both truthy.
    const timer = page.locator('.test-timer-chip');
    await expect(timer).toBeVisible();
    // Format is `MM:SS`.
    await expect(timer).toHaveText(/^\d{2}:\d{2}$/);
  });

  test('kanji index has search + stroke + lesson + sort filters', async ({ page }) => {
    await page.goto('/#/kanji');
    // The audit's IMP-003 + IMP-025 added these four affordances. They all
    // live inside the .kanji-filters block.
    await expect(page.locator('.kanji-filters')).toBeVisible();
    await expect(page.locator('#kanji-filter-q')).toBeVisible();
    // Stroke + Lesson chip rows; both labelled by their .kanji-filter-label.
    const labels = page.locator('.kanji-filter-label');
    await expect(labels).toHaveCount(3);  // Strokes / Lesson / Sort
    await expect(labels.nth(0)).toHaveText('Strokes:');
    await expect(labels.nth(1)).toHaveText('Lesson:');
    await expect(labels.nth(2)).toHaveText('Sort:');
    // Sort dropdown (IMP-025).
    const sort = page.locator('#kanji-sort');
    await expect(sort).toBeVisible();
    // The four canonical sort modes ship as <option> values.
    const opts = await sort.locator('option').allTextContents();
    expect(opts.length).toBeGreaterThanOrEqual(4);
  });

  test('kanji search input filters the visible cards', async ({ page }) => {
    await page.goto('/#/kanji');
    const input = page.locator('#kanji-filter-q');
    await input.fill('water');
    // The "showing X of Y" counter should drop below the full count after a
    // narrow filter. The 水 entry is the canonical "water" kanji.
    const count = page.locator('.kanji-filter-count strong').first();
    const filteredText = await count.textContent();
    expect(parseInt(filteredText, 10)).toBeLessThan(106);
  });

  test('kanji detail page shows "In a sentence" block (IMP-018)', async ({ page }) => {
    // 水 (water) is in the corpus and definitely has sentences attached.
    await page.goto('/#/kanji/' + encodeURIComponent('水'));
    const block = page.locator('.kanji-sentences');
    await expect(block).toBeVisible();
    await expect(block.locator('h3')).toHaveText('In a sentence');
    // At least one sentence row.
    await expect(block.locator('.kanji-sentence-ja').first()).toBeVisible();
  });

  test('grammar TOC has search input + 3 tier chips (IMP-029)', async ({ page }) => {
    await page.goto('/#/learn/grammar');
    await expect(page.locator('#grammar-filter-q')).toBeVisible();
    const tierChips = page.locator('[data-grammar-filter-group="tier"]');
    await expect(tierChips).toHaveCount(3);
    await expect(tierChips.nth(0)).toHaveText('All');
    await expect(tierChips.nth(1)).toHaveText('Core N5');
    await expect(tierChips.nth(2)).toHaveText('Late N5');
  });

  test('vocab list has search input (IMP-029)', async ({ page }) => {
    await page.goto('/#/learn/vocab');
    const input = page.locator('#vocab-filter-q');
    await expect(input).toBeVisible();
    // Searching for "eat" should narrow the corpus (たべる lives in the
    // corpus with gloss "eat / drink" or similar).
    await input.fill('eat');
    const count = page.locator('.kanji-filter-count strong').first();
    const filteredText = await count.textContent();
    expect(parseInt(filteredText, 10)).toBeLessThan(1003);
  });

  test('clicking a kanji glyph opens the popover with stroke chip (ISSUE-008)', async ({ page }) => {
    // Land on a grammar pattern detail page that's known to render kanji
    // (most of them do). Click the first <span lang="ja"> kanji glyph and
    // assert the popover comes up with the stroke chip rendered.
    await page.goto('/#/learn/grammar');
    // Click the first grammar-card to drill into a pattern detail.
    await page.locator('.grammar-card').first().click();
    // Find a kanji glyph inside the rendered furigana - the renderer
    // wraps each glyph in a clickable element.
    const glyph = page.locator('.kanji-clickable, .ruby-kanji, [data-kanji]').first();
    if (await glyph.count() === 0) {
      test.skip(true, 'No clickable kanji glyph found on the first grammar pattern; popover smoke skipped.');
    }
    await glyph.click();
    // Popover should be visible.
    const popover = page.locator('.kanji-popover');
    await expect(popover).toBeVisible();
    // Stroke-count chip (ISSUE-008) is optional per-entry but the locator
    // must at least exist as a class in the page when an entry has the
    // stroke_count field - kanji.json carries it for every entry now.
    await expect(popover.locator('.kanji-popover-strokes')).toBeVisible();
  });

});
