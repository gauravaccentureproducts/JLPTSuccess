# -*- coding: utf-8 -*-
"""Verify v1.17.15 print fix: load grammar pattern in print emulation,
load the LOCAL main.min.css (not live, since deploy hasn't happened
yet), and assert no small visible elements remain inside example <li>s."""

import asyncio
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pathlib import Path
from playwright.async_api import async_playwright


async def main():
    async with async_playwright() as pw:
        browser = await pw.chromium.launch()
        ctx = await browser.new_context()
        page = await ctx.new_page()
        await page.emulate_media(media='print')

        # Load live page first, then inject the LOCAL main.min.css to test the not-yet-deployed CSS
        await page.goto("https://gauravaccentureproducts.github.io/JLPTSuccess/N5/#/learn/n5-095", wait_until='networkidle')
        await page.wait_for_timeout(1200)

        local_css = (Path(__file__).resolve().parent.parent / 'css' / 'main.min.css').read_text(encoding='utf-8')
        await page.evaluate(f"""
() => {{
    // Remove all linked stylesheets
    document.querySelectorAll('link[rel=stylesheet]').forEach(l => l.remove());
    // Inject the local v1.17.15 CSS
    const style = document.createElement('style');
    style.textContent = {local_css!r};
    document.head.appendChild(style);
}}
""")
        await page.wait_for_timeout(500)

        result = await page.evaluate(r"""
() => {
    const lis = document.querySelectorAll('main ul li, main ol li');
    const findings = [];
    let liIdx = 0;
    for (const li of lis) {
        for (const el of li.querySelectorAll('*')) {
            const cs = getComputedStyle(el);
            if (cs.display === 'none') continue;
            const w = el.offsetWidth, h = el.offsetHeight;
            const hasBg = cs.backgroundColor !== 'rgba(0, 0, 0, 0)' && cs.backgroundColor !== 'transparent';
            const isSmall = w > 0 && w < 24 && h > 0 && h < 24;
            if (isSmall) {
                findings.push({liIdx, tag: el.tagName, classes: el.className, w, h, bg: cs.backgroundColor, text: (el.textContent||'').slice(0,30)});
            }
        }
        liIdx++;
        if (liIdx > 3) break;
    }
    return findings;
}
""")

        print(f"After v1.17.15 CSS: {len(result)} small visible elements remaining in first 4 <li>s")
        for f in result:
            print(f"  li[{f['liIdx']}] {f['tag']}.{f['classes']!r} {f['w']}x{f['h']}  bg={f['bg']!r}  text={f['text']!r}")

        # Sanity — count visible kanji-glyph spans (these SHOULD be there)
        glyphs = await page.evaluate("() => document.querySelectorAll('.kanji-glyph').length")
        print(f"\nSanity: visible .kanji-glyph spans in <li>s = {glyphs} (these are expected; they're kanji characters, not chrome)")

        await browser.close()

asyncio.run(main())
