<?xml version="1.0" encoding="UTF-8"?>
<!--
  Browser-only presentation layer for /N5/sitemap.xml.
  Referenced via the <?xml-stylesheet?> processing instruction the
  sitemap generator (tools/build_llm_surfaces_2026_05_18.py) emits.
  Search-engine crawlers ignore this stylesheet and read the raw
  <urlset>; only browsers apply it, so SEO is unaffected. The chrome
  matches the static summary pages (same brand header + design tokens).
-->
<xsl:stylesheet version="1.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
  xmlns:s="http://www.sitemaps.org/schemas/sitemap/0.9">
<xsl:output method="html" encoding="UTF-8" indent="yes" doctype-system="about:legacy-compat"/>
<xsl:template match="/">
<html lang="en">
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Sitemap — JLPT N5</title>
<meta name="robots" content="noindex,follow"/>
<link rel="stylesheet" href="/JLPTSuccess/N5/css/main.min.css?v=1.17.30"/>
<style>:root{--green:#14452a;--green-soft:#1a5c38;--bg:#fff;--bg-soft:#f6f8f6;--text:#1a1a1a;--muted:#555;--border:#ddd}*{box-sizing:border-box}html,body{background:var(--bg);color:var(--text)}body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI","Hiragino Sans","Yu Gothic","Noto Sans CJK JP",sans-serif;line-height:1.6;margin:0}.page{max-width:920px;margin:0 auto;padding:1rem}.page a{color:var(--green);word-break:break-all}.page a:hover{color:var(--green-soft)}h1.page-title{font-size:1.6em;margin:.5rem 0}.meta-banner{background:var(--bg-soft);border-left:3px solid var(--green);padding:.75rem 1rem;font-size:.92em;margin-bottom:1.25rem}.muted{color:var(--muted);font-size:.92em}table.sitemap{border-collapse:collapse;width:100%;font-size:.92em}table.sitemap th,table.sitemap td{text-align:left;padding:.45em .6em;border-bottom:1px solid var(--border);vertical-align:top}table.sitemap th{color:var(--green);border-bottom:2px solid var(--green)}table.sitemap td.idx{color:var(--muted);text-align:right;white-space:nowrap;width:3em}table.sitemap tr:hover td{background:var(--bg-soft)}.page-footer{max-width:920px;margin:2.5rem auto 0;padding:1rem 1rem 2.5rem;border-top:1px solid var(--border);font-size:.85em;color:var(--muted)}.page-footer a{color:var(--green)}@media (prefers-color-scheme:dark){:root{--bg:#1a1d1b;--bg-soft:#232826;--text:#e7eae8;--muted:#a5aba8;--border:#383d3a}}</style>
</head>
<body>
<header class="app-header" role="banner">
<div class="brand"><h1><a href="/JLPTSuccess/" class="brand-link" aria-label="JLPTSuccess home, choose a level"><svg class="brand-mark" viewBox="0 0 100 57" role="img" aria-hidden="true" focusable="false"><g fill="currentColor">
<rect x="1" y="0" width="98" height="9" rx="4.5"/><rect x="1" y="12" width="84" height="9" rx="4.5"/>
<rect x="1" y="24" width="64" height="9" rx="4.5"/><rect x="1" y="36" width="44" height="9" rx="4.5"/>
<rect x="1" y="48" width="22" height="9" rx="4.5"/></g></svg></a><a href="/JLPTSuccess/N5/" class="brand-link" aria-label="N5 home"><span class="brand-wordmark">N5</span></a></h1></div>
<nav class="primary-nav" aria-label="Primary">
<a href="/JLPTSuccess/N5/learn/grammar/">Grammar</a>
<a href="/JLPTSuccess/N5/learn/vocab/">Vocabulary</a>
<a href="/JLPTSuccess/N5/kanji/">Kanji</a>
<a href="/JLPTSuccess/N5/reading/">Reading</a>
<a href="/JLPTSuccess/N5/listening/">Listening</a>
<a href="/JLPTSuccess/N5/test/">Test</a>
<a href="/JLPTSuccess/N5/missed/">Missed</a>
<a href="/JLPTSuccess/N5/summary/">Progress</a>
</nav>
</header>
<div class="page">
<div class="meta-banner"><strong>XML sitemap</strong> — machine-readable index of every crawlable URL on the JLPT N5 site. This is the browser-friendly view; search engines read the underlying XML.</div>
<h1 class="page-title">Sitemap</h1>
<p class="muted"><xsl:value-of select="count(s:urlset/s:url)"/> URLs</p>
<table class="sitemap">
<thead><tr><th class="idx">#</th><th>URL</th></tr></thead>
<tbody>
<xsl:for-each select="s:urlset/s:url">
<tr><td class="idx"><xsl:value-of select="position()"/></td><td><a href="{s:loc}"><xsl:value-of select="s:loc"/></a></td></tr>
</xsl:for-each>
</tbody>
</table>
</div>
<footer class="page-footer">
<p>↩ <a href="/JLPTSuccess/N5/home.html">N5 syllabus overview</a> · <a href="/JLPTSuccess/N5/#/home">Interactive app</a> · <a href="/JLPTSuccess/">All levels</a></p>
<p>JLPT® and the Japanese-Language Proficiency Test® are trademarks of the Japan Foundation and JEES. This independent study site is not affiliated with, endorsed by, or sponsored by them.</p>
</footer>
</body>
</html>
</xsl:template>
</xsl:stylesheet>
