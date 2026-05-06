# Privacy

**Last updated:** 2026-05-05.

JLPTSuccess is a static client-side app. No telemetry. No tracking. No analytics. No remote API calls during normal use. No third-party scripts. No accounts.

## What's stored

Each level's app uses **browser localStorage on your device only** to remember:

- Your study progress (which patterns / vocab / kanji you've reviewed)
- SRS schedule (next-review timestamps)
- UI preferences (locale, theme, font size, audio speed, furigana mode)
- The set of kanji you've marked "I already know"
- A study-streak counter (private - no public leaderboard)

This data **never leaves your device**. The app has no server, no backend, no account system.

## Per-level isolation (actual runtime keys)

Each level namespaces its own localStorage keys with a per-level prefix:

- N5 keys are prefixed **`jlpt-n5-tutor:`** (e.g. `jlpt-n5-tutor:settings`, `jlpt-n5-tutor:srs`)
- N4 keys are prefixed **`jlpt-n4-tutor:`** (legacy backup; N4 sub-app is currently work-blocked but its previously-deployed shell still serves)

Progress in one level is not visible to another and is not shared across levels. (You can verify this by opening DevTools → Application → Local Storage on the live site.)

## Service worker

Each level registers a service worker scoped to its own subdirectory (`/JLPTSuccess/N5/`, `/JLPTSuccess/N4/`). The service worker pre-caches the app shell, content JSON, and the kanji stroke-order SVGs so the app works offline. Audio files (~22 MB) are cached lazily on first fetch - they are not pre-loaded.

The service worker stores cached assets in the browser's Cache Storage. Nothing is sent to a remote.

## Content Security Policy

Each level's `index.html` carries a meta-tag CSP enforcing same-origin loading (`default-src 'self'`). Scripts are restricted to self-hosted ES modules with no inline-script allowance - any inline-script regression fails fast. The N5 sub-app additionally splits `style-src-elem` (no inline `<style>` blocks) from `style-src-attr` (allows the small set of inline `style="width:N%"` writes used by progress bars).

## Third-party assets (build-time only, no runtime calls)

Some content was sourced at build time from third-party providers, with attribution per each level's `NOTICES.md`:

- **KanjiVG** stroke-order SVGs (CC BY-SA 3.0) - bundled and self-hosted
- **JLPT Sensei** vocabulary inventory (used at build time only; not at runtime)
- **gtts** Python library - used at build time to render the audio MP3s; the rendered files are self-hosted

None of these are loaded from a third-party origin at runtime - all assets are self-hosted under the GitHub Pages domain.

## What's not stored

- No personally-identifiable information.
- No IP address (the static host's logs are subject to GitHub Pages' standard policy; the app itself collects nothing).
- No cookies (other than what GitHub Pages sets at the host level for its own infrastructure).

## Clearing your data

Use your browser's "Clear site data" feature, or each level's in-app **Settings → Reset progress** when available.

You can also export your progress as a JSON file (Settings → Export progress) and re-import it on a different device - useful if you want to back up your study history without using a cloud service.
