# Privacy

This app does not collect, transmit, or store any personal data on a remote server.

## What we do NOT do

- **No accounts, no login.** You can use every feature without identifying yourself.
- **No telemetry, no analytics.** No page-view, click, or session data is sent anywhere.
- **No third-party scripts.** The app loads only from this domain (enforced by Content-Security-Policy in `index.html`).
- **No tracking cookies.** Nothing is set in `document.cookie`.
- **No remote API calls during normal use.** Once the page is loaded (or cached by the service worker for offline use), every interaction is handled locally in your browser.

## What stays on your device

All learning state — answers you've given, items you've marked known, your study streak, test results, settings — is held only in your browser's `localStorage`, namespaced under `jlpt-n5-tutor:*`. It never leaves your device.

You can:

- **Export** your progress at any time via Settings → Export progress (downloads a `.json` file you control).
- **Import** a previously exported file to restore state on the same device or transfer to a different one.
- **Wipe** everything by clearing the site's storage in your browser (DevTools → Application → Local Storage), or via Settings → Reset progress.

## Audio

Audio assets (MP3 files for grammar examples, listening drills, reading passages) are static files served from the same origin. They are not streamed from a third party.

## Independently verifiable

Open the browser's Network tab and watch a session. You will see only same-origin requests for the assets the app needs to run (HTML, CSS, JS, JSON, fonts, MP3s, SVGs). No third-party hosts, no analytics endpoints, no tracking pixels. The build does not inject analytics or trackers post-deploy.

## Updates

If this app's privacy posture ever changes, the change will be documented in the `CHANGELOG.md` and announced on the home page before it ships.

---

*Last updated: 2026-05-02*
