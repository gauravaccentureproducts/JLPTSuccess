// Take a full-page screenshot of the live n5-017 page at typical
// desktop viewport (1366x768) and at mobile (390x844). Save to disk.
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const browser = await chromium.launch({ headless: true });
  try {
    for (const [name, viewport] of [
      ['desktop1366', { width: 1366, height: 768 }],
      ['desktop1920', { width: 1920, height: 1080 }],
      ['mobile390',  { width: 390,  height: 844 }],
    ]) {
      const ctx = await browser.newContext({ viewport });
      const page = await ctx.newPage();
      await page.goto('https://gauravaccentureproducts.github.io/JLPTSuccess/N5/learn/n5-017/', { waitUntil: 'networkidle', timeout: 30000 });
      await page.waitForTimeout(3000);
      const fp = path.join('.', `.tmp_n5_017_${name}.png`);
      await page.screenshot({ path: fp, fullPage: true });
      console.log('Saved', fp);
      // Also report the bounding rect of the .pattern-usage section
      const rect = await page.evaluate(() => {
        const s = document.querySelector('section.pattern-usage');
        if (!s) return null;
        const r = s.getBoundingClientRect();
        const t = s.querySelector('.pattern-usage-table');
        const c = s.querySelector('.pattern-conjugation-table');
        return {
          sect: { top: r.top, height: r.height, width: r.width },
          tableTop: t ? t.getBoundingClientRect() : null,
          conjTop:  c ? c.getBoundingClientRect() : null,
        };
      });
      console.log('  rect:', JSON.stringify(rect));
      await ctx.close();
    }
  } finally { await browser.close(); }
})();
