// Verify v1.17.35 UI polish on a representative sample of pattern shapes.
// Run: node tools/probe_ui_polish_2026_05_31.js
const { chromium } = require('playwright');

const SAMPLES = [
  // [pid, expected_top_table, expected_conj_table, note]
  ['n5-001',  true,  true,  '3 attaches, 9 conjugations — both tables'],
  ['n5-008',  true,  true,  '2 attaches, 3 conjugations — both tables'],
  ['n5-093',  true,  false, '2 attaches, 1 conj — top table only (conj <2 hidden)'],
  ['n5-017',  false, true,  '1 attach, 4 conjugations — conj only (top hidden)'],
  ['n5-040',  false, false, '1 attach, no conj — section hidden entirely'],
  ['n5-045',  false, false, '1 attach, no conj — section hidden entirely (user-flagged pattern)'],
];

(async () => {
  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext({ viewport: { width: 1366, height: 900 } });
  const page = await ctx.newPage();
  let failures = 0;

  for (const [pid, expectTop, expectConj, note] of SAMPLES) {
    await page.goto(`http://127.0.0.1:8765/learn/${pid}/`, { waitUntil: 'networkidle', timeout: 30000 });
    await page.waitForTimeout(1500);
    const r = await page.evaluate(() => {
      const sect = document.querySelector('section.pattern-usage');
      const topTbl = document.querySelector('.pattern-usage-table');
      const conjTbl = document.querySelector('.pattern-conjugation-table');
      const h3s = Array.from(document.querySelectorAll('h3.section-title')).map(h => h.textContent.trim());
      const chips = Array.from(document.querySelectorAll('.pattern-usage-chip')).map(c => c.textContent.trim());
      const subtitle = document.querySelector('.meaning-en')?.textContent.trim();
      const title = document.querySelector('main h2.pattern-name')?.textContent.trim();
      return {
        sect_present: !!sect,
        top_tbl_present: !!topTbl,
        conj_tbl_present: !!conjTbl,
        chips: chips,
        h3s: h3s,
        title: title,
        subtitle: subtitle,
        subtitle_starts_with_title: !!(title && subtitle && subtitle.startsWith(title)),
      };
    });
    const okSect = (r.sect_present === (expectTop || expectConj));
    const okTop = (r.top_tbl_present === expectTop);
    const okConj = (r.conj_tbl_present === expectConj);
    const okSubtitle = !r.subtitle_starts_with_title;
    const overall = okSect && okTop && okConj && okSubtitle;
    console.log(`\n${pid} — ${note}`);
    console.log(`  section: ${r.sect_present ? 'present' : 'hidden'} (expect ${(expectTop||expectConj) ? 'present' : 'hidden'}) ${okSect ? 'OK' : 'FAIL'}`);
    console.log(`  top:     ${r.top_tbl_present ? 'present' : 'hidden'} (expect ${expectTop ? 'present' : 'hidden'}) ${okTop ? 'OK' : 'FAIL'}`);
    console.log(`  conj:    ${r.conj_tbl_present ? 'present' : 'hidden'} (expect ${expectConj ? 'present' : 'hidden'}) ${okConj ? 'OK' : 'FAIL'}`);
    console.log(`  subtitle: ${(r.subtitle || '').slice(0, 60)}`);
    console.log(`  subtitle echoes title: ${r.subtitle_starts_with_title} ${okSubtitle ? 'OK' : 'FAIL'}`);
    console.log(`  chips: ${JSON.stringify(r.chips)}`);
    if (!overall) failures++;
  }
  console.log(`\n=== SUMMARY: ${failures} failure(s) of ${SAMPLES.length} probed ===`);
  await browser.close();
  process.exit(failures > 0 ? 2 : 0);
})();
