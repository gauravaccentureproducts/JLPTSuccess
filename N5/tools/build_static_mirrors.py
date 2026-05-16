"""Build pre-rendered static HTML mirrors for every SPA route surface.

User-reported BUG-010 (2026-05-16) generalizes BUG-001 (grammar-only)
to every content + meta surface. Each pre-rendered file:

- Mirrors what the SPA would render for that route, as real HTML
  (not a meta refresh, not a noscript placeholder).
- Carries route-specific <title>, <meta name="description">, and OG
  tags (og:title, og:description, og:url, og:image).
- Carries <link rel="canonical"> pointing back to the live SPA hash
  route (so search engines deduplicate static + interactive views).
- Carries a small inline script: when JS is enabled, redirect after
  a short delay so a user landing on the static mirror flows to the
  interactive SPA. Search engines (which render JS but stop before
  redirect delay completes) still index the static content.
- Carries inline CSS sufficient to render readably without JS.

Surfaces (built in stages — see BUG-010 description):
- Stage 1: grammar (/N5/learn/grammar/<id>/index.html × 178 + index)
- Stage 2: vocab (/N5/learn/vocab/<form>/index.html × 1009 + index)
- Stage 3: kanji (/N5/kanji/<glyph>/index.html × 106 + index)
- Stage 4: reading (/N5/reading/<id>/index.html × 54 + index)
- Stage 5: listening (/N5/listening/<id>/index.html × 50 + index)
- Stage 6: meta routes (home / changelog / privacy / notices /
  feedback / settings / test / sitting / missed / summary) +
  /N5/sitemap.xml + /N5/robots.txt

Run from N5/:
  python tools/build_static_mirrors.py
  python tools/build_static_mirrors.py --stages grammar,vocab
  python tools/build_static_mirrors.py --stages all  (default)

Idempotent: re-running on unchanged inputs produces no diff. After
running, run tools/check_content_integrity.py to verify the new
JA-NN invariant (mirror-presence assertion).
"""
from __future__ import annotations

import argparse
import html
import io
import json
import re
import sys
import urllib.parse
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
GRAMMAR = DATA_DIR / "grammar.json"
VOCAB = DATA_DIR / "vocab.json"

# Live deploy base — used in canonical + og:url. Trailing slash matters.
SITE_BASE = "https://gauravaccentureproducts.github.io/JLPTSuccess/"
N5_BASE = SITE_BASE + "N5/"

# How long (ms) to wait before JS-redirecting to SPA. Long enough that
# search-engine bots which abort JS execution early still see the
# static content; short enough that human users don't wait visibly.
JS_REDIRECT_DELAY_MS = 1500


# ----- Common HTML chrome -----

INLINE_CSS = """
  :root { --green: #14452a; --green-soft: #1a5c38; --bg: #ffffff; --bg-soft: #f6f8f6; --text: #1a1a1a; --muted: #555; --border: #ddd; }
  * { box-sizing: border-box; }
  html, body { background: var(--bg); color: var(--text); }
  body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "Hiragino Sans", "Yu Gothic", "Noto Sans CJK JP", sans-serif; max-width: 760px; margin: 0 auto; padding: 1rem; line-height: 1.6; }
  a { color: var(--green); }
  a:hover { color: var(--green-soft); }
  h1 { font-size: 1.6em; margin: 0.5rem 0; line-height: 1.3; }
  h2 { font-size: 1.18em; border-bottom: 1px solid var(--border); padding-bottom: 0.3em; margin-top: 2rem; }
  h3 { font-size: 1.05em; margin-top: 1.4rem; }
  code { background: #f0f3f0; padding: 0.05em 0.35em; border-radius: 3px; font-size: 0.92em; }
  .meta-banner { background: var(--bg-soft); border-left: 3px solid var(--green); padding: 0.75rem 1rem; font-size: 0.92em; margin: 0 0 1.5rem 0; }
  .meta-banner a { font-weight: 600; }
  .lang-tag { display: inline-block; background: #eef; border: 1px solid #ccd; border-radius: 3px; padding: 0 0.4em; font-size: 0.8em; color: #336; margin-right: 0.45em; vertical-align: 1px; }
  .ex { margin: 0.8em 0; padding: 0.5em 0.7em; background: #fafbfa; border-left: 2px solid #e4ebe5; border-radius: 0 4px 4px 0; }
  .ex .ja { font-size: 1.05em; }
  .ex .en { color: var(--muted); font-size: 0.93em; margin-top: 0.2em; }
  .wrong { color: #a33; }
  .right { color: var(--green-soft); }
  .muted { color: var(--muted); font-size: 0.92em; }
  .index-section { margin-bottom: 1.4rem; }
  .index-section h3 { margin: 1rem 0 0.4rem 0; color: var(--green-soft); }
  .index-card { display: block; padding: 0.5em 0.7em; border: 1px solid #e0e6e0; border-radius: 4px; margin: 0.3em 0; text-decoration: none; color: inherit; }
  .index-card:hover { background: var(--bg-soft); }
  .index-card .label { font-weight: 600; color: var(--green); }
  .index-card .gloss { color: var(--muted); font-size: 0.9em; }
  footer { margin-top: 3rem; padding-top: 1rem; border-top: 1px solid var(--border); font-size: 0.85em; color: var(--muted); }
  @media (prefers-color-scheme: dark) {
    :root { --bg: #1a1d1b; --bg-soft: #232826; --text: #e7eae8; --muted: #a5aba8; --border: #383d3a; }
    code { background: #2a2f2c; }
    .ex { background: #1f2320; border-left-color: #2c3530; }
    .index-card { border-color: #2c3530; }
    .meta-banner { background: #232826; }
    .lang-tag { background: #2a2f3a; color: #b5bdce; border-color: #3a4150; }
  }
"""

# JS that redirects to the SPA hash route after a short delay so bots
# rendering JS still capture the static content (they typically time
# out execution before this fires).
JS_REDIRECT_TEMPLATE = """
<script>
(function(){{
  var goToSPA = function(){{ location.href = {spa_url_json}; }};
  // Bot-friendly: only redirect after delay, and skip redirect when
  // ?nojs=1 or ?goSPA=0 is in the URL (lets crawlers and reviewers
  // inspect the static surface directly).
  try {{
    var q = location.search || '';
    if (q.indexOf('nojs=1') !== -1 || q.indexOf('goSPA=0') !== -1) return;
    setTimeout(goToSPA, {delay_ms});
  }} catch (e) {{ /* never fail the static render on JS error */ }}
}})();
</script>
"""

PAGE_TEMPLATE = """<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title_tag}</title>
<meta name="description" content="{description}">
<meta name="robots" content="index,follow">
<link rel="canonical" href="{canonical_url}">
{hreflang_links}
<meta property="og:type" content="article">
<meta property="og:url" content="{canonical_url}">
<meta property="og:title" content="{og_title}">
<meta property="og:description" content="{description}">
<meta property="og:site_name" content="JLPT N5 Tutor">
<meta property="og:image" content="{og_image}">
<meta name="twitter:card" content="summary">
<meta name="twitter:title" content="{og_title}">
<meta name="twitter:description" content="{description}">
<style>{inline_css}</style>
{js_redirect}
</head>
<body>
<p class="meta-banner">
  <strong>Static read-only mirror.</strong>
  <a href="{spa_url}">Open the interactive version</a>{interactive_note}
</p>
<h1>{h1}</h1>
{body}
<footer>
  <p>{breadcrumb_html}</p>
  <p>Part of <a href="{n5_root}">JLPT N5 Tutor</a>. Content licensed CC BY-SA 4.0 · <a href="{n5_root}CONTENT-LICENSE.md">CONTENT-LICENSE.md</a>.</p>
  {footer_meta}
</footer>
</body>
</html>
"""


# ----- Helpers -----


def _esc(s: object) -> str:
    return html.escape(str(s) if s is not None else "")


def _relative_root_from(depth: int) -> str:
    """Path from a static mirror back up to /N5/. e.g. depth=3 -> '../../../'"""
    return "../" * depth if depth > 0 else "./"


def _build_page(
    *,
    lang: str = "en",
    title_tag: str,
    h1: str,
    description: str,
    canonical_url: str,
    spa_url: str,
    body_html: str,
    depth: int,
    og_title: str | None = None,
    breadcrumb: list[tuple[str, str]] | None = None,
    footer_meta_html: str = "",
    interactive_note: str = " (audio playback, drills, cross-references require JavaScript).",
    hreflang_alt_url: str | None = None,
    hreflang_lang: str | None = None,
    self_hreflang_lang: str | None = None,
) -> str:
    """Render the full HTML for one static mirror page."""
    n5_root = _relative_root_from(depth)
    og_img = N5_BASE + "icons/icon-512.png"  # static OG image; doesn't need per-page generation in this iteration

    hreflang_links = ""
    if hreflang_alt_url and hreflang_lang:
        self_lang = self_hreflang_lang or lang
        hreflang_links = (
            f'<link rel="alternate" hreflang="{self_lang}" href="{canonical_url}">\n'
            f'<link rel="alternate" hreflang="{hreflang_lang}" href="{hreflang_alt_url}">'
        )

    breadcrumb_html = ""
    if breadcrumb:
        parts = []
        for label, href in breadcrumb:
            if href:
                parts.append(f'<a href="{_esc(href)}">{_esc(label)}</a>')
            else:
                parts.append(_esc(label))
        breadcrumb_html = " · ".join(parts)

    js_redirect = JS_REDIRECT_TEMPLATE.format(
        spa_url_json=json.dumps(spa_url),
        delay_ms=JS_REDIRECT_DELAY_MS,
    )

    return PAGE_TEMPLATE.format(
        lang=lang,
        title_tag=_esc(title_tag),
        description=_esc(description),
        canonical_url=_esc(canonical_url),
        hreflang_links=hreflang_links,
        og_title=_esc(og_title or title_tag),
        og_image=_esc(og_img),
        inline_css=INLINE_CSS,
        js_redirect=js_redirect,
        spa_url=_esc(spa_url),
        interactive_note=interactive_note,
        h1=_esc(h1),
        body=body_html,
        n5_root=n5_root,
        breadcrumb_html=breadcrumb_html,
        footer_meta=footer_meta_html,
    )


def _write_if_changed(path: Path, content: str) -> bool:
    """Write content to path only if it differs. Returns True if written."""
    if path.exists() and path.read_text(encoding="utf-8") == content:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return True


# ----- Grammar renderer (Stage 1) -----


def _render_examples(examples: list) -> str:
    if not examples:
        return ""
    out = ["<h2>Examples</h2>"]
    for ex in examples:
        if not isinstance(ex, dict):
            continue
        ja = ex.get("ja") or ""
        en = ex.get("en") or ex.get("translation_en") or ""
        if not ja:
            continue
        out.append('<div class="ex">')
        out.append(f'<div class="ja" lang="ja"><span class="lang-tag">JA</span>{_esc(ja)}</div>')
        if en:
            out.append(f'<div class="en"><span class="lang-tag">EN</span>{_esc(en)}</div>')
        out.append("</div>")
    return "\n".join(out)


def _render_common_mistakes(cms: list) -> str:
    if not cms:
        return ""
    out = ["<h2>Common mistakes</h2>"]
    for cm in cms:
        if not isinstance(cm, dict):
            continue
        wrong = cm.get("wrong") or ""
        right = cm.get("right") or ""
        why = cm.get("why") or ""
        if not (wrong or right):
            continue
        out.append('<div class="ex">')
        if wrong:
            out.append(f'<div class="wrong" lang="ja">✗ {_esc(wrong)}</div>')
        if right:
            out.append(f'<div class="right" lang="ja">✓ {_esc(right)}</div>')
        if why:
            out.append(f'<div class="en">{_esc(why)}</div>')
        out.append("</div>")
    return "\n".join(out)


def _render_wcp(wcps: list) -> str:
    if not wcps:
        return ""
    out = ["<h2>Wrong / corrected pairs</h2>"]
    for wcp in wcps:
        if not isinstance(wcp, dict):
            continue
        wrong = wcp.get("wrong") or ""
        correct = wcp.get("correct") or wcp.get("right") or ""
        why = wcp.get("why") or ""
        if not (wrong or correct):
            continue
        out.append('<div class="ex">')
        if wrong:
            out.append(f'<div class="wrong" lang="ja">✗ {_esc(wrong)}</div>')
        if correct:
            out.append(f'<div class="right" lang="ja">✓ {_esc(correct)}</div>')
        if why:
            out.append(f'<div class="en">{_esc(why)}</div>')
        out.append("</div>")
    return "\n".join(out)


def _render_grammar_pattern_body(p: dict) -> tuple[str, str]:
    """Returns (body_html, description) for one grammar pattern."""
    title = p.get("pattern") or p.get("id")
    meaning_en = p.get("meaning_en") or ""
    meaning_ja = p.get("meaning_ja") or ""
    explanation_en = p.get("explanation_en") or ""

    desc = (meaning_en or title)[:155]

    parts: list[str] = []
    if meaning_en:
        parts.append(f'<p><span class="lang-tag">EN</span>{_esc(meaning_en)}</p>')
    if meaning_ja:
        parts.append(f'<p lang="ja"><span class="lang-tag">JA</span>{_esc(meaning_ja)}</p>')
    if explanation_en and explanation_en != meaning_en:
        parts.append(f'<h2>Explanation</h2><p>{_esc(explanation_en)}</p>')

    fr = p.get("form_rules") or {}
    if isinstance(fr, dict) and fr:
        atts = fr.get("attaches_to") or []
        if atts:
            parts.append(f'<h2>Attaches to</h2><p>{_esc(", ".join(atts))}</p>')

    parts.append(_render_examples(p.get("examples") or []))
    parts.append(_render_common_mistakes(p.get("common_mistakes") or []))
    parts.append(_render_wcp(p.get("wrong_corrected_pair") or []))

    body = "\n".join(x for x in parts if x)
    return body, desc


def build_grammar(sitemap_urls: list[str]) -> tuple[int, int, int]:
    """Stage 1 — grammar pattern mirrors.

    Returns (written, unchanged, total).
    """
    g = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    patterns = g.get("patterns", [])

    out_root = ROOT / "learn" / "grammar"
    written = 0
    unchanged = 0

    for p in patterns:
        pid = p.get("id")
        if not pid:
            continue
        title = p.get("pattern") or pid
        body, desc = _render_grammar_pattern_body(p)
        tier = p.get("tier") or ""
        category = p.get("category") or ""

        out_path = out_root / pid / "index.html"
        canonical = f"{N5_BASE}#/learn/{pid}"
        spa_url = canonical

        footer_meta = (
            f'<p>Pattern ID: <code>{_esc(pid)}</code>'
            + (f' · Tier: <code>{_esc(tier)}</code>' if tier else "")
            + (f' · Category: <code>{_esc(category)}</code>' if category else "")
            + "</p>"
        )

        breadcrumb = [
            ("Home", _relative_root_from(3) + "#/home"),
            ("Grammar", "../index.html"),
            (title, ""),
        ]

        html_text = _build_page(
            lang="en",
            title_tag=f"{title} — JLPT N5 Grammar",
            h1=title,
            description=desc,
            canonical_url=canonical,
            spa_url=spa_url,
            body_html=body,
            depth=3,
            og_title=f"{title} — JLPT N5 Grammar",
            breadcrumb=breadcrumb,
            footer_meta_html=footer_meta,
        )

        if _write_if_changed(out_path, html_text):
            written += 1
        else:
            unchanged += 1

        # Sitemap: list canonical SPA URL plus the static mirror.
        # The static mirror is the actual crawlable artifact.
        mirror_url = f"{N5_BASE}learn/grammar/{pid}/"
        sitemap_urls.append(mirror_url)

    # Grammar index page
    idx_items = sorted(patterns, key=lambda x: (x.get("categoryOrder", 999), x.get("patternOrder", 999)))
    by_cat: dict[str, list[dict]] = {}
    cat_order: list[str] = []
    for p in idx_items:
        cat = p.get("category") or "Other"
        if cat not in by_cat:
            by_cat[cat] = []
            cat_order.append(cat)
        by_cat[cat].append(p)

    idx_parts: list[str] = []
    idx_parts.append('<p>Static index of all N5 grammar patterns. Each entry links to a read-only mirror; the interactive version (audio, drills, cross-references) is at the SPA route.</p>')
    for cat in cat_order:
        idx_parts.append(f'<section class="index-section">')
        idx_parts.append(f'<h3>{_esc(cat)}</h3>')
        for p in by_cat[cat]:
            pid = p.get("id")
            title = p.get("pattern") or pid
            gloss = (p.get("meaning_en") or "")[:80]
            idx_parts.append(
                f'<a class="index-card" href="{_esc(pid)}/">'
                f'<span class="label" lang="ja">{_esc(title)}</span> — '
                f'<span class="gloss">{_esc(gloss)}</span>'
                f'</a>'
            )
        idx_parts.append("</section>")
    idx_body = "\n".join(idx_parts)

    idx_canonical = f"{N5_BASE}#/learn/grammar"
    idx_path = out_root / "index.html"
    idx_html = _build_page(
        lang="en",
        title_tag="N5 Grammar — All Patterns (static index)",
        h1="N5 Grammar — All Patterns",
        description=f"All {len(patterns)} N5 grammar patterns, organized by category. Static index for non-JS clients; interactive version at the SPA route.",
        canonical_url=idx_canonical,
        spa_url=idx_canonical,
        body_html=idx_body,
        depth=2,
        og_title="N5 Grammar — All Patterns",
        breadcrumb=[("Home", "../../#/home"), ("Grammar", "")],
        footer_meta_html=f"<p>{len(patterns)} patterns indexed.</p>",
    )
    if _write_if_changed(idx_path, idx_html):
        written += 1
    else:
        unchanged += 1
    sitemap_urls.append(f"{N5_BASE}learn/grammar/")

    return written, unchanged, len(patterns)


# ----- Vocab renderer (Stage 2) -----


def _encode_url_segment(s: str) -> str:
    """Percent-encode a single URL path segment (e.g. a vocab form)."""
    return urllib.parse.quote(s or "", safe="")


def _render_vocab_examples(examples: list) -> str:
    if not examples:
        return ""
    out = ["<h2>Examples</h2>"]
    for ex in examples:
        if not isinstance(ex, dict):
            continue
        ja = ex.get("ja") or ""
        en = ex.get("translation_en") or ex.get("en") or ""
        if not ja:
            continue
        out.append('<div class="ex">')
        out.append(f'<div class="ja" lang="ja"><span class="lang-tag">JA</span>{_esc(ja)}</div>')
        if en:
            out.append(f'<div class="en"><span class="lang-tag">EN</span>{_esc(en)}</div>')
        out.append("</div>")
    return "\n".join(out)


def _render_vocab_entry_block(e: dict) -> str:
    """Render one vocab entry (one sense). Multiple senses share a form page."""
    form = e.get("form") or ""
    reading = e.get("reading") or ""
    gloss = e.get("gloss") or ""
    gloss_hi = e.get("gloss_hi") or ""
    pos = e.get("pos") or ""
    section = e.get("section") or ""
    register = e.get("register") or ""
    counter = e.get("counter") or ""

    parts: list[str] = ['<article class="vocab-sense">']
    # Sense heading: pos · reading
    head_bits = []
    if pos:
        head_bits.append(f'<code>{_esc(pos)}</code>')
    if reading and reading != form:
        head_bits.append(f'<span class="lang-tag">読</span><span lang="ja">{_esc(reading)}</span>')
    if head_bits:
        parts.append(f'<p class="muted">{" · ".join(head_bits)}</p>')

    if gloss:
        parts.append(f'<p><span class="lang-tag">EN</span>{_esc(gloss)}</p>')
    if gloss_hi:
        parts.append(f'<p><span class="lang-tag">HI</span><span lang="hi">{_esc(gloss_hi)}</span></p>')

    meta_bits = []
    if section:
        meta_bits.append(f"Section: {_esc(section)}")
    if register and register != "neutral":
        meta_bits.append(f"Register: {_esc(register)}")
    if counter:
        meta_bits.append(f"Counter: <code lang=\"ja\">{_esc(counter)}</code>")
    pa = e.get("pitch_accent") or {}
    if isinstance(pa, dict) and pa.get("mora") is not None and pa.get("drop") is not None:
        meta_bits.append(
            f"Pitch: mora={_esc(pa.get('mora'))}, drop={_esc(pa.get('drop'))}"
        )
    if meta_bits:
        parts.append('<p class="muted">' + " · ".join(meta_bits) + "</p>")

    cols = e.get("collocations") or []
    if cols:
        parts.append("<h3>Common collocations</h3><ul>")
        for c in cols[:10]:
            if isinstance(c, str) and c:
                parts.append(f'<li lang="ja">{_esc(c)}</li>')
        parts.append("</ul>")

    parts.append(_render_vocab_examples(e.get("examples") or []))

    fp = e.get("frequent_patterns") or []
    if isinstance(fp, list) and fp:
        links = []
        for pid in fp[:8]:
            if isinstance(pid, str) and pid:
                links.append(
                    f'<a href="../../grammar/{_esc(pid)}/"><code>{_esc(pid)}</code></a>'
                )
        if links:
            parts.append("<h3>Often appears with</h3><p>" + " · ".join(links) + "</p>")

    parts.append("</article>")
    return "\n".join(parts)


def build_vocab(sitemap_urls: list[str]) -> tuple[int, int, int]:
    """Stage 2 — vocab mirrors. One static page per unique form.

    36 forms in the corpus have multiple sense entries (e.g., か, は, あの,
    人). All senses for a given form land on the same static page so a
    learner / reader sees every meaning.

    Returns (written, unchanged, total_forms).
    """
    v = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = v.get("entries", [])

    # Group entries by form (preserves first-seen order for stable index)
    by_form: dict[str, list[dict]] = {}
    form_order: list[str] = []
    for e in entries:
        form = e.get("form")
        if not form:
            continue
        if form not in by_form:
            by_form[form] = []
            form_order.append(form)
        by_form[form].append(e)

    out_root = ROOT / "learn" / "vocab"
    written = 0
    unchanged = 0

    for form in form_order:
        senses = by_form[form]
        # Use the first sense's reading + gloss as page summary
        primary = senses[0]
        reading = primary.get("reading") or form
        gloss = primary.get("gloss") or ""
        # If multiple senses, append a count hint to title
        sense_hint = f" ({len(senses)} senses)" if len(senses) > 1 else ""

        # Page body: render each sense in sequence
        body_parts: list[str] = []
        body_parts.append(
            f'<p class="muted">Reading: <span lang="ja">{_esc(reading)}</span></p>'
        )
        if len(senses) > 1:
            body_parts.append(
                f'<p class="muted">This form has {len(senses)} sense entries in the corpus. All shown below.</p>'
            )
        for idx, e in enumerate(senses):
            if len(senses) > 1:
                body_parts.append(f'<h2>Sense {idx + 1}</h2>')
            body_parts.append(_render_vocab_entry_block(e))
        body = "\n".join(body_parts)

        form_encoded = _encode_url_segment(form)
        canonical = f"{N5_BASE}#/learn/vocab/{form_encoded}"
        mirror_url = f"{N5_BASE}learn/vocab/{form_encoded}/"

        desc = (gloss or form)[:155]

        breadcrumb = [
            ("Home", "../../../#/home"),
            ("Vocab", "../index.html"),
            (form, ""),
        ]
        footer_meta = ""
        if primary.get("section"):
            footer_meta = (
                f'<p>Section: <code>{_esc(primary.get("section"))}</code>'
                + (f' · POS: <code>{_esc(primary.get("pos") or "")}</code>' if primary.get("pos") else "")
                + "</p>"
            )

        html_text = _build_page(
            lang="en",
            title_tag=f"{form} ({reading}) — JLPT N5 Vocab{sense_hint}",
            h1=f"{form}" + (f" — {reading}" if reading != form else ""),
            description=desc,
            canonical_url=canonical,
            spa_url=canonical,
            body_html=body,
            depth=3,
            og_title=f"{form} — JLPT N5 Vocab",
            breadcrumb=breadcrumb,
            footer_meta_html=footer_meta,
        )

        # Path on disk uses raw form chars (modern filesystems handle Unicode).
        out_path = out_root / form / "index.html"
        if _write_if_changed(out_path, html_text):
            written += 1
        else:
            unchanged += 1

        sitemap_urls.append(mirror_url)

    # Vocab index, grouped by section
    by_section: dict[str, list[str]] = {}
    section_order: list[str] = []
    for form in form_order:
        primary = by_form[form][0]
        section = primary.get("section") or "Other"
        if section not in by_section:
            by_section[section] = []
            section_order.append(section)
        by_section[section].append(form)

    # Sort sections by the leading integer when present
    def _section_sort_key(s: str) -> tuple:
        m = re.match(r"^\s*(\d+)\s*[.\-]", s)
        return (0, int(m.group(1))) if m else (1, s)

    section_order_sorted = sorted(section_order, key=_section_sort_key)

    idx_parts: list[str] = []
    idx_parts.append(
        f'<p>Static index of all {len(form_order)} unique vocabulary forms ({len(entries)} sense entries) for JLPT N5. Forms with multiple senses share one page; the interactive version (drills, SRS, audio) is at the SPA route.</p>'
    )
    for section in section_order_sorted:
        idx_parts.append('<section class="index-section">')
        idx_parts.append(f'<h3>{_esc(section)}</h3>')
        for form in by_section[section]:
            primary = by_form[form][0]
            reading = primary.get("reading") or form
            gloss = (primary.get("gloss") or "")[:60]
            form_encoded = _encode_url_segment(form)
            label_reading = f" ({reading})" if reading != form else ""
            idx_parts.append(
                f'<a class="index-card" href="{form_encoded}/">'
                f'<span class="label" lang="ja">{_esc(form)}</span>'
                f'<span class="muted">{_esc(label_reading)}</span> — '
                f'<span class="gloss">{_esc(gloss)}</span>'
                f'</a>'
            )
        idx_parts.append("</section>")
    idx_body = "\n".join(idx_parts)

    idx_canonical = f"{N5_BASE}#/learn/vocab"
    idx_path = out_root / "index.html"
    idx_html = _build_page(
        lang="en",
        title_tag="N5 Vocabulary — All Words (static index)",
        h1="N5 Vocabulary — All Words",
        description=f"All {len(form_order)} unique N5 vocabulary forms ({len(entries)} sense entries), grouped by section.",
        canonical_url=idx_canonical,
        spa_url=idx_canonical,
        body_html=idx_body,
        depth=2,
        og_title="N5 Vocabulary — All Words",
        breadcrumb=[("Home", "../../#/home"), ("Vocab", "")],
        footer_meta_html=f"<p>{len(form_order)} forms / {len(entries)} sense entries indexed.</p>",
    )
    if _write_if_changed(idx_path, idx_html):
        written += 1
    else:
        unchanged += 1
    sitemap_urls.append(f"{N5_BASE}learn/vocab/")

    return written, unchanged, len(form_order)


# ----- Sitemap + robots.txt -----


def write_sitemap(sitemap_urls: list[str]) -> bool:
    """Write /N5/sitemap.xml from accumulated URLs. Returns True if file changed."""
    # Sort + dedupe for deterministic output (idempotent re-runs).
    urls = sorted(set(sitemap_urls))
    lines = ['<?xml version="1.0" encoding="UTF-8"?>',
             '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    for u in urls:
        lines.append(f"  <url><loc>{_esc(u)}</loc></url>")
    lines.append("</urlset>")
    lines.append("")
    content = "\n".join(lines)
    return _write_if_changed(ROOT / "sitemap.xml", content)


def write_robots() -> bool:
    """Write /N5/robots.txt pointing at the sitemap."""
    content = (
        "User-agent: *\n"
        "Allow: /\n"
        f"Sitemap: {N5_BASE}sitemap.xml\n"
    )
    return _write_if_changed(ROOT / "robots.txt", content)


# ----- Entry point -----


STAGES_AVAILABLE = ["grammar", "vocab", "kanji", "reading", "listening", "meta"]


def main() -> int:
    parser = argparse.ArgumentParser(description="Build static HTML mirrors for non-JS clients.")
    parser.add_argument(
        "--stages",
        default="all",
        help=f"Comma-separated stages to build (default: all). Available: {','.join(STAGES_AVAILABLE)},all",
    )
    args = parser.parse_args()

    stages = (
        STAGES_AVAILABLE
        if args.stages == "all"
        else [s.strip() for s in args.stages.split(",") if s.strip()]
    )

    sitemap_urls: list[str] = []

    summary: list[tuple[str, int, int, int]] = []

    if "grammar" in stages:
        w, u, t = build_grammar(sitemap_urls)
        summary.append(("grammar", w, u, t))
        print(f"Stage 1 (grammar): wrote {w}, unchanged {u}, total {t} patterns (+1 index).")

    if "vocab" in stages:
        w, u, t = build_vocab(sitemap_urls)
        summary.append(("vocab", w, u, t))
        print(f"Stage 2 (vocab): wrote {w}, unchanged {u}, total {t} unique forms (+1 index).")

    # Stages 3-6 land in subsequent commits per BUG-010 staged rollout.
    for stage in ("kanji", "reading", "listening", "meta"):
        if stage in stages:
            print(f"Stage {stage}: not yet implemented (planned per BUG-010 staged rollout).")

    # Always rebuild sitemap + robots from the accumulated urls of the
    # stages we built. (When more stages are added, their URLs will be
    # included automatically.)
    if write_sitemap(sitemap_urls):
        print(f"Wrote sitemap.xml ({len(set(sitemap_urls))} URLs).")
    else:
        print(f"sitemap.xml unchanged ({len(set(sitemap_urls))} URLs).")
    if write_robots():
        print("Wrote robots.txt.")
    else:
        print("robots.txt unchanged.")

    return 0


if __name__ == "__main__":
    sys.exit(main())
