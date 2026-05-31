// Horizontal sweep: for every pattern that has form_rules.attaches_to OR
// form_rules.conjugations, navigate to its detail page and verify
// section.pattern-usage exists AND has non-trivial text content.
//
// Catches any pattern where the renderer would produce empty content
// despite the data being present (e.g. mis-keyed attaches_to, missing
// labels, all-empty examples, conditional rendering bug, locale gap).
//
// Run against the local dev server on :8765 by default; override via
// arg.
const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const BASE = process.argv[2] || 'http://127.0.0.1:8765';

(async () => {
  const grammar = JSON.parse(fs.readFileSync(path.join('data','grammar.json'), 'utf8'));
  const patterns = grammar.patterns || [];
  const targets = patterns.filter(p => {
    const fr = p.form_rules || {};
    return (fr.attaches_to && fr.attaches_to.length) || (fr.conjugations && fr.conjugations.length);
  });
  console.log(`Total patterns: ${patterns.length}`);
  console.log(`With form_rules.attaches_to OR .conjugations: ${targets.length}`);

  const browser = await chromium.launch({ headless: true });
  const ctx = await browser.newContext();
  const page = await ctx.newPage();
  page.on('pageerror', () => {});
  page.on('console', () => {});

  const failures = [];
  let i = 0;
  for (const p of targets) {
    i++;
    const url = `${BASE}/learn/${p.id}/`;
    try {
      await page.goto(url, { waitUntil: 'networkidle', timeout: 20000 });
      await page.waitForTimeout(500);
      const r = await page.evaluate(() => {
        const s = document.querySelector('section.pattern-usage');
        if (!s) return { sect: false };
        const text = s.textContent.trim();
        const topTbl = s.querySelector('.pattern-usage-table');
        const conjTbl = s.querySelector('.pattern-conjugation-table');
        return {
          sect: true,
          text_len: text.length,
          topTbl_rows: topTbl ? topTbl.querySelectorAll('tbody tr').length : 0,
          conjTbl_rows: conjTbl ? conjTbl.querySelectorAll('tbody tr').length : 0,
        };
      });
      const fr = p.form_rules || {};
      const att = (fr.attaches_to || []).length;
      const conj = (fr.conjugations || []).length;
      const expectTop = att > 0;
      const expectConj = conj >= 2;
      const ok =
        r.sect &&
        r.text_len > 0 &&
        (!expectTop || r.topTbl_rows >= 1) &&
        (!expectConj || r.conjTbl_rows === conj);
      if (!ok) {
        failures.push({
          id: p.id, url, att, conj, expectTop, expectConj,
          actual: r,
        });
        console.log(`  [${i}/${targets.length}] FAIL ${p.id} (att=${att} conj=${conj}) -> ${JSON.stringify(r)}`);
      } else if (i % 20 === 0) {
        console.log(`  [${i}/${targets.length}] ok ${p.id}`);
      }
    } catch (e) {
      failures.push({ id: p.id, url, error: e.message });
      console.log(`  [${i}/${targets.length}] ERROR ${p.id}: ${e.message}`);
    }
  }
  await browser.close();
  console.log('\n=== SWEEP COMPLETE ===');
  console.log(`Total scanned:  ${targets.length}`);
  console.log(`Failures:       ${failures.length}`);
  if (failures.length) {
    fs.writeFileSync('.tmp_pattern_usage_render_failures.json', JSON.stringify(failures, null, 2));
    console.log('Failures written to .tmp_pattern_usage_render_failures.json');
    process.exit(2);
  }
  console.log('All targets render non-empty section.pattern-usage.');
})();
