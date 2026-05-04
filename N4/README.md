# JLPT N4 Tutor

A free, offline-capable, privacy-preserving study app for JLPT N4. No login, no telemetry, all progress stored locally on your device.

**Status:** v0.1.0 — skeleton (Pass-1 architecture; content authoring is Pass-2+).
**Live URL:** `https://<org>.github.io/jlpt-n4-tutor/` (configure on first deploy).

## What's in this repo

- `index.html`, `sw.js`, `manifest.webmanifest` — static PWA shell
- `js/` — vanilla ES modules (router, learn, test, drill, review, …)
- `css/main.css` — Zen Modern design system
- `data/` — runtime JSON (regenerated from `KnowledgeBank/` by `tools/build_data.py`)
- `KnowledgeBank/` — markdown source-of-truth content (currently skeleton; see TASKS.md Pass-2)
- `tools/` — Python build + audit pipeline
- `tests-e2e/` — Playwright smoke + a11y tests
- `audio/`, `svg/kanji/`, `fonts/` — static assets

## Build pipeline

Edit markdown in `KnowledgeBank/`, then:

```bash
python tools/build_data.py            # KB → data/*.json
python tools/build_papers.py          # questions → mock-test papers
python tools/link_grammar_examples_to_vocab.py
python tools/tag_vocab_pos.py
python tools/check_content_integrity.py   # 33 invariants — must pass
python tools/test_build_data.py
```

`tools/build_audio.py` re-renders synthetic TTS as needed.

## Local dev

```bash
python -m http.server 8765    # serve at http://localhost:8765
```

Then open the live URL hash route (e.g. `http://localhost:8765/#/home`).

## Deploy

Push to `main`. `.github/workflows/pages-build.yml` deploys to GitHub Pages automatically. Repo name → URL slug must be `jlpt-n4-tutor` per `<JLPT-root>/N4/procedure-manual-build-next-jlpt-level.N4.md` §35.

## Specification

The single source of truth for what this app must do is at `<JLPT-root>/N4/procedure-manual-build-next-jlpt-level.N4.md`. Read it before making any architectural change.

## Privacy

Per `PRIVACY.md`: no telemetry, no third-party scripts, no remote API calls during normal use. All data stays on your device. Export / import via the Settings page.

## License

Code: MIT. Content: original; see `CONTENT-LICENSE.md` for source authorities + reuse policy.
