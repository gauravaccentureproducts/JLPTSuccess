# -*- coding: utf-8 -*-
"""Inject the global app-header (brand + primary nav) into every static
SEO mirror that lacks it.

STATUS (2026-05-29): PERMANENT, load-bearing component despite the dated
filename. This is REQUIRED step 2 of the static-mirror pipeline: run it after
tools/build_static_mirrors.py (which emits header-less mirrors) or every
mirror renders header-less ("looks broken" on deep-link). The builder's
docstring documents the two-step sequence and JA-170 in
check_content_integrity.py guards the result. Do NOT archive or delete this
during tools/ debris triage. Safe to run standalone (idempotent).

Why
---
The 1,413 static mirrors under /N5/learn/, /N5/kanji/, /N5/reading/,
/N5/listening/, /N5/papers/, etc. ship pre-rendered SEO content with
their own per-page <title>, <meta description>, OG tags, and inline
CSS. They do NOT include the global app-header (brand mark + primary
nav). User-visible result: when a visitor deep-links to one of these
URLs, they see content but no top-of-page header / navigation — looks
broken.

Three of the directory-level mirrors (/N5/learn/, /N5/drill/, /N5/mock/)
were converted to full SPA-shell clones in v1.17.6. That fix preserved
the header but DESTROYED the per-page SEO content. We can't do that for
the remaining 1,410 mirrors without losing 1,410 indexable per-pattern
pages.

This script does the right thing: it INJECTS the global header into
each mirror that lacks it, while preserving every byte of existing
per-page content. The header HTML uses absolute URLs (/JLPTSuccess/N5/…)
so it works from any depth without a <base href>.

Idempotency: skips files that already contain `class="app-header"`.
Run repeatedly = safe (no double-injection).
"""

from pathlib import Path

# Static header block. Absolute URLs so it works at any directory depth.
# Mirrors the structure in N5/index.html lines 233-301 but strips the
# search input + locale toggle + fullscreen toggle + settings link (all
# JS-dependent). The brand link + 9 nav items are the universal chrome.
HEADER_HTML = '''<header class="app-header" role="banner">
<div class="brand">
<h1>
<a href="/JLPTSuccess/" class="brand-link" aria-label="JLPTSuccess home, choose a level">
<svg class="brand-mark" viewBox="0 0 100 57" role="img" aria-hidden="true" focusable="false">
<g fill="currentColor">
<rect x="1" y="0"  width="98" height="9" rx="4.5"/>
<rect x="1" y="12" width="84" height="9" rx="4.5"/>
<rect x="1" y="24" width="64" height="9" rx="4.5"/>
<rect x="1" y="36" width="44" height="9" rx="4.5"/>
<rect x="1" y="48" width="22" height="9" rx="4.5"/>
</g>
</svg>
<span class="brand-wordmark">N5</span>
</a>
</h1>
</div>
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
'''

# Stylesheet link to add when missing. Uses absolute URL so depth doesn't
# matter. ?v= cache-buster matches the current frontend release.
CSS_LINK = '<link rel="stylesheet" href="/JLPTSuccess/N5/css/main.min.css?v=1.17.9">'

# Marker tags. Skip insertion if the file already has these.
HEADER_MARKER = 'class="app-header"'
MAIN_CSS_MARKER = 'main.min.css'


def inject_into(html: str) -> tuple[str, bool, bool]:
    """Return (new_html, header_injected, css_injected)."""
    header_injected = False
    css_injected = False

    # 1. Inject CSS link if absent. Put it inside <head> just before </head>.
    if MAIN_CSS_MARKER not in html:
        # Place right before </head>. If somehow no </head>, give up on CSS.
        if '</head>' in html:
            html = html.replace('</head>', CSS_LINK + '\n</head>', 1)
            css_injected = True

    # 2. Inject header right after the <body> open tag.
    if HEADER_MARKER not in html:
        # Handle both `<body>` and `<body class="...">` and `<body><main id="app">`.
        # We need to find the END of the <body> open tag.
        body_open = html.find('<body')
        if body_open >= 0:
            body_close = html.find('>', body_open)
            if body_close >= 0:
                insert_at = body_close + 1
                html = html[:insert_at] + '\n' + HEADER_HTML + html[insert_at:]
                header_injected = True

    return html, header_injected, css_injected


def main():
    repo_root = Path(__file__).resolve().parent.parent  # N5/
    stats = {
        'total': 0,
        'skipped_already_has_header': 0,
        'injected': 0,
        'css_added': 0,
        'errors': 0,
    }

    for p in repo_root.rglob('index.html'):
        # Skip the canonical SPA shell
        if p == repo_root / 'index.html':
            continue
        s = p.as_posix()
        # Skip review packets, node_modules, anything under /N4/
        if '_review_packet' in s or 'node_modules' in s:
            continue
        # We are inside N5/ already, so no /N4/ to worry about,
        # but defensive check in case anyone re-roots:
        rel = p.relative_to(repo_root).as_posix()
        if rel.startswith('N4/') or '/N4/' in rel:
            continue
        stats['total'] += 1
        try:
            txt = p.read_text(encoding='utf-8', errors='ignore')
            if HEADER_MARKER in txt:
                stats['skipped_already_has_header'] += 1
                continue
            new_txt, header_added, css_added = inject_into(txt)
            if header_added:
                p.write_text(new_txt, encoding='utf-8', newline='\n')
                stats['injected'] += 1
                if css_added:
                    stats['css_added'] += 1
        except Exception as e:
            stats['errors'] += 1
            print(f'ERROR {rel}: {e}')

    print('=' * 60)
    print('Header injection complete')
    print('=' * 60)
    for k, v in stats.items():
        print(f'  {k}: {v}')


if __name__ == '__main__':
    main()
