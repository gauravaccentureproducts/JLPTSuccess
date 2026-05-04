# Privacy

JLPTSuccess is a static client-side app. No telemetry. No tracking. No analytics. No external API calls.

## What's stored

Each level's app uses **browser localStorage on your device only** to remember:
- Your study progress (which patterns / vocab / kanji you've reviewed)
- SRS schedule (next-review timestamps)
- UI preferences (locale, fullscreen, etc.)

This data **never leaves your device**. The app has no server, no backend, no account system.

## Per-level isolation

Each level (N5, N4, etc.) namespaces its own localStorage keys (e.g. `n5.*`, `n4.*`). Progress in one level is not visible to another and is not shared across levels.

## Service worker

Each level registers a service worker scoped to its own subdirectory (`/JLPTSuccess/N5/`, `/JLPTSuccess/N4/`). The service worker pre-caches the app shell, content JSON, and audio files so the app works offline. The service worker stores cached assets locally; nothing is sent to a remote.

## Third-party assets

Some content uses third-party data sources, attributed in each level's `NOTICES.md`:
- **KanjiVG** stroke-order SVGs (CC BY-SA 3.0)
- **JLPT Sensei** vocabulary inventory (used at build time only; not at runtime)

None of these are loaded from a third-party origin at runtime — all assets are self-hosted.

## What's not stored

- No personally-identifiable information.
- No IP address (the static host's logs are subject to GitHub Pages' standard policy; the app itself collects nothing).
- No cookies (other than what GitHub Pages sets at the host level for its own infrastructure).

## Clearing your data

Use your browser's "Clear site data" feature, or each level's in-app **Settings → Clear Progress** if available.
