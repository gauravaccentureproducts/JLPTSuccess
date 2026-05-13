# Self-hosting JLPTSuccess — operator guide

This guide is for institutions (vocational schools, language schools,
NGOs, individual instructors) who want to fork and self-host the
JLPTSuccess N5 tutor.

The app is designed to support this workflow: **fully static**, **no
network calls at runtime**, **no account/auth/database needed**, **no
build step**. Drop the files behind any HTTP server and it works.

## Quick start (3 commands)

```bash
git clone https://github.com/gauravaccentureproducts/JLPTSuccess.git
cd JLPTSuccess
# Serve N5 locally on port 8000 — adjust port as needed:
python -m http.server 8000 --directory .
# Open http://localhost:8000/N5/ in any modern browser
```

That's it. The PWA loads from local disk; the service worker caches
everything on first load; subsequent visits run fully offline.

## License posture

### Code (MIT)
The repository's JavaScript, CSS, HTML, Python tools, and configuration
files are MIT-licensed. You can fork, modify, redistribute, sublicense
— commercial or non-commercial.

### Content (CC BY-NC 4.0 — see CONTENT-LICENSE.md)
The N5 grammar / vocab / kanji / reading / listening corpus is licensed
**CC BY-NC 4.0** — free for **non-commercial educational** use with
attribution. Commercial use (selling the corpus, embedding in paid
products without explicit license) requires permission.

If you're a school or NGO running this as an internal learning tool,
that's non-commercial use and you're covered. If you're a for-profit
publishing house repackaging the corpus, contact the maintainer.

### Third-party content (preserved attributions)
The repository includes content from upstream sources that must keep
their attribution. See `NOTICES.md` for the full list. Highlights:
- **KanjiVG stroke-order SVGs** — CC BY-SA 3.0 (Ulrich Apel; the SVG
  comment headers carry the upstream copyright line and must NOT be
  stripped).
- **Kanjium pitch-accent dictionary** — CC BY-SA 4.0 (EDICT-derived).
- **VOICEVOX TTS engine** — engine is LGPL-2.1 / dual-licensed; voice
  models (四国めたん, ずんだもん, etc.) each have individual licenses
  (mostly free for non-commercial educational use; check per-speaker
  terms before commercial redistribution of the audio assets).

## What you get out of the box

| Surface | Count | Notes |
|---|---:|---|
| Grammar patterns | 178 | Every pattern: ≥10 example sentences, ≥3 categorized common mistakes, ≥1 contrast, ≥500-char essay, cultural callout, PD-literature references, audio per example. |
| Vocabulary entries | 1009 | Every entry: 3+ examples, pitch-accent {mora, drop}, register tag, wago/kango/gairaigo origin, collocations. |
| Kanji glyphs | 106 | Every kanji: 3-mnemonic structure (radical-story + visual + reading), KanjiVG stroke-order, lookalike clusters, real-world signage refs, per-yomi audio. |
| Reading passages | 54 | Every passage: grammar-sentence footnotes, vocab preview, audio, per-paragraph summaries, cultural callouts, reflection prompts. |
| Listening items | 50 | Every item: timestamped transcript, vocab glossary inline, slow-version variant, ambient context layer, 6 distinct VOICEVOX voices. |
| Mock paper files | 28 | 402 paper-bound questions across moji/goi/bunpou/dokkai/chokai mondai. |

All content is bundled into `N5/data/*.json` and loaded statically.

## Deployment paths

### Path A — GitHub Pages (zero infrastructure)

If your fork lives on GitHub:

1. Settings → Pages → Source: deploy from branch
2. Branch: `master`, folder: `/` (root)
3. Wait 30-60s; site live at `https://<your-org>.github.io/<repo>/N5/`

The existing `.github/workflows/static.yml` already does this on the
upstream repo. Your fork can keep, modify, or remove the workflow.

### Path B — Static CDN / S3 / nginx

1. Run `python tools/build_min_css.py` and `python tools/build_min_js.py`
   to regenerate the minified bundles (only needed if you edit
   `css/main.css` or `js/*.js`).
2. Upload the `N5/` directory (and `index.html` from repo root if you
   want the landing page) to any static host.
3. Ensure the server sends `Content-Type: application/manifest+json`
   for `N5/manifest.webmanifest` so the PWA installs correctly.

### Path C — Local LAN / classroom server

Any of these work:
```bash
# Python (any version 3.x)
python -m http.server 8000 --directory .

# Node.js
npx http-server -p 8000

# nginx (production)
# Add to your sites-available conf:
# location /jlpt/ {
#   alias /var/www/JLPTSuccess/;
#   try_files $uri $uri/ /N5/index.html;
# }
```

Teachers connect students to `http://classroom-server.local:8000/N5/`.
No accounts, no progress sync to a central server (by design — see
"Privacy posture" below).

## Forking and modifying content

The corpus is in `N5/data/*.json`. The schema for each file is
documented inline (top-level keys + structure visible from any sample
entry). Common modifications:

### Translate to a new locale (e.g., Spanish)

The codebase already supports `en` + `hi` via the `_es` / `_hi` field
convention. To add Spanish:

1. Add `meaning_es`, `explanation_es`, etc. fields to grammar/vocab/
   kanji/reading/listening entries.
2. Update `js/i18n.js` to register the `es` locale.
3. Update `tools/check_content_integrity.py` JA-39 invariant to
   include `es` in the allowed locale set.

### Add or modify entries

Edit the relevant `data/*.json` file. After saving:

1. Run `python tools/check_content_integrity.py` — 70 invariants must
   all PASS.
2. Run `python tools/audit_refresh_state.py` — to see the updated
   scorecard.
3. Hard-refresh the browser (Cmd+Shift+R / Ctrl+Shift+R) to bypass
   the service-worker cache.

### Add new mock-paper questions

Drop new question files in `N5/data/papers/`. The naming convention
is `<level>-<year>-<paper>.json`. See existing files for the
question schema (stem, choices, correctAnswer, rationale).

## Privacy posture (do not break)

The upstream app makes the following commitments. Forks SHOULD
preserve them to honor the user expectation:

1. **No fetch to non-local URLs at runtime.** CI invariant JA-60
   enforces this. Search the codebase for any `fetch(` and confirm
   the target is relative or same-origin only.
2. **No account / cloud sync.** Progress is in `localStorage`, scoped
   to the user's browser. CI invariants JA-37 + JA-60 enforce.
3. **No analytics / telemetry.** Search for `gtag`, `analytics`,
   `posthog`, `mixpanel`, etc.; the upstream finds zero results.
4. **No third-party iframes.** Embedded YouTube / Vimeo / etc. would
   break the offline guarantee.

If your fork needs to add classroom-progress sync for a teacher
dashboard, that's a legitimate institutional extension — but
clearly document it for users and ideally make it opt-in via a
setting.

## Customizing branding

The visible "JLPTSuccess" brand is in:
- `index.html` (site landing)
- `N5/index.html` (N5 landing)
- `N5/manifest.webmanifest` (PWA name)
- `N5/css/main.css` (theme colors)

The fork can rebrand freely. The CC-BY-NC content license requires
attribution to the upstream content authors (see CONTENT-LICENSE.md
for the exact attribution string); the MIT code license has its own
header pattern in the LICENSE file.

## Backup / restore strategy

The corpus is plain JSON in git. There is no database. Backup =
`git push` to a private mirror. Restore = `git pull`.

For local snapshots before a content edit run, the upstream tooling
uses dated `.bak_*` files (gitignored via `.gitignore`). The
`tools/archive_old_snapshots.py` script archives older snapshots to
`not-required/` after their parent commits ship.

## Testing your fork

Before deploying changes:

```bash
# 1. CI invariants (release-blocker; 70 checks)
python tools/check_content_integrity.py

# 2. Audit refresh (per-surface scorecards)
python tools/audit_refresh_state.py

# 3. If you have Playwright installed:
npx playwright test tests/playwright/p0-smoke.spec.ts

# 4. Manual smoke test in browser:
#    - Grammar page renders 178 patterns
#    - Click into one pattern; example audio plays
#    - Vocab list loads
#    - Kanji stroke-order SVG animates
#    - Reading passage loads with audio
#    - Listening item plays
#    - Test mode: take a mock paper, get scored
#    - Toggle Hindi locale — every text surface shows Hindi
```

## Getting help

- **File an issue** on the upstream repo at
  `github.com/gauravaccentureproducts/JLPTSuccess/issues` —
  helpful for general questions.
- **Content questions** (JLPT-correctness, register, register, native
  usage): file an issue with a concrete pattern/word ID and the
  observed vs. expected behavior.
- **Self-hosting troubleshooting**: include your deployment
  environment (server, OS, browser), reproduction steps, and any
  console errors.

## Contributing back

If your fork makes a non-locale, non-branding improvement (CI
hardening, content correction, schema extension), opening a PR
upstream is welcome. The upstream maintains the canonical content;
running your improvement through upstream CI (70 invariants) and
review keeps the shared baseline strong.
