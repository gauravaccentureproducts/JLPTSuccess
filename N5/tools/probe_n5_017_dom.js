// One-shot Playwright probe for n5-017 HOW TO USE section.
// User reported the HOW TO USE / 使い方 section renders empty.
// This script navigates a headless Chromium to the static mirror,
// waits for SPA hydration, then dumps:
//   - whether section.pattern-usage exists
//   - innerHTML of that section
//   - any console errors
//   - computed display/visibility of inner tables (if present)
//
// Run: node tools/probe_n5_017_dom.js
const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push('pageerror: ' + e.message));
  page.on('console', m => {
    if (m.type() === 'error') errors.push('console.error: ' + m.text());
  });
  try {
    await page.goto('http://127.0.0.1:8765/learn/n5-017/', { waitUntil: 'networkidle', timeout: 30000 });
    // Give SPA time to render
    await page.waitForTimeout(2000);

    const result = await page.evaluate(() => {
      const sect = document.querySelector('section.pattern-usage');
      const header = document.querySelector('.pattern-usage-header');
      const topTbl = document.querySelector('.pattern-usage-table');
      const conjTbl = document.querySelector('.pattern-conjugation-table');
      const main = document.querySelector('main');
      const allSectionTitles = Array.from(
        document.querySelectorAll('h3.section-title')
      ).map(h => h.textContent.trim());
      return {
        url: location.href,
        sect_exists: !!sect,
        sect_html: sect ? sect.outerHTML.slice(0, 4000) : null,
        header_exists: !!header,
        header_text: header ? header.textContent.trim() : null,
        topTbl_exists: !!topTbl,
        topTbl_rowcount: topTbl ? topTbl.querySelectorAll('tr').length : 0,
        topTbl_text: topTbl ? topTbl.textContent.trim().slice(0, 200) : null,
        conjTbl_exists: !!conjTbl,
        conjTbl_rowcount: conjTbl ? conjTbl.querySelectorAll('tbody tr').length : 0,
        conjTbl_text: conjTbl ? conjTbl.textContent.trim().slice(0, 400) : null,
        main_length: main ? main.textContent.length : 0,
        h3_section_titles: allSectionTitles,
        sect_computed_display: sect ? getComputedStyle(sect).display : null,
        sect_computed_visibility: sect ? getComputedStyle(sect).visibility : null,
      };
    });
    console.log('PROBE RESULT:');
    console.log(JSON.stringify(result, null, 2));
    console.log('\nCONSOLE / PAGE ERRORS:');
    for (const e of errors) console.log('  ', e);
  } catch (e) {
    console.error('Probe failed:', e.message);
  } finally {
    await browser.close();
  }
})();
