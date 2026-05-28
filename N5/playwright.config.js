// Playwright config for the P0 smoke suite (testing-plan §17.1).
//
// We don't ship a node server with the app - it's static HTML/CSS/JS.
// Use python's built-in http.server as the test fixture so the suite
// can run anywhere Python 3 is available (which CI guarantees).
//
// Run locally:
//   npm install
//   npm run test:install-browsers   # one-time: downloads Chromium
//   npm run test:smoke              # full suite headless
//   npm run test:smoke:headed       # watch the browser

const { defineConfig, devices } = require('@playwright/test');

module.exports = defineConfig({
  testDir: './tests',
  testMatch: '**/*.spec.js',
  timeout: 30_000,
  expect: { timeout: 5_000 },
  fullyParallel: true,
  forbidOnly: !!process.env.CI,
  retries: process.env.CI ? 1 : 0,
  // 2026-05-21: workers 1 → 2 on CI. With 60 tests × 2 projects = 120
  // instances on a single worker, runtime exceeded 15 min on GitHub-
  // hosted ubuntu-latest (2 cores). Using both cores roughly halves
  // execution time; `fullyParallel: true` was already set. If this
  // surfaces flakiness, fall back to a matrix-shard-by-project layout
  // (one job per device profile) rather than re-serializing.
  workers: process.env.CI ? 2 : undefined,
  reporter: process.env.CI ? [['html', { open: 'never' }], ['github']] : 'list',
  use: {
    // 2026-05-27: index.html ships with `<base href="/JLPTSuccess/N5/">`
    // since v1.17.7 to pin asset resolution across the SPA's
    // history-mode replaceState() calls (so invalid-URL deep-links
    // still resolve their CSS/JS/fonts). On production GitHub Pages
    // the site IS at /JLPTSuccess/N5/ so it works. The local test
    // server has to MIRROR that URL prefix or the browser fetches
    // /JLPTSuccess/N5/css/main.min.css → 404 → SPA never boots →
    // every assertion fails on an empty DOM. See the webServer block
    // below for the symlink that gives python http.server the
    // /JLPTSuccess/N5/ path.
    baseURL: 'http://localhost:8000/JLPTSuccess/N5/',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    // 2026-05-21: video off on CI. `retain-on-failure` always records
    // (just discards on pass) which costs CPU per test on a 2-core
    // runner; screenshots + on-first-retry traces are sufficient for
    // triage. Locally we keep video for interactive debugging.
    video: process.env.CI ? 'off' : 'retain-on-failure',
  },
  projects: [
    {
      name: 'chromium-desktop',
      use: { ...devices['Desktop Chrome'] },
    },
    {
      name: 'chromium-mobile',
      use: { ...devices['Pixel 5'] },
    },
  ],
  webServer: {
    // 2026-05-27: build a tiny URL-prefix shim so the local server
    // matches the production GitHub Pages path. Creates
    // `.test-server/JLPTSuccess/N5` as a symlink to the current
    // working directory (= N5/), then serves http.server from
    // `.test-server/`. Result: GET /JLPTSuccess/N5/css/main.min.css
    // → symlink → N5/css/main.min.css → 200. Matches the `<base
    // href>` in index.html that ships with the production build.
    //
    // The `mkdir -p` is idempotent; `ln -sfn` overwrites any stale
    // symlink (so re-running the suite locally without cleaning up
    // works). The whole `.test-server/` directory is gitignored.
    command: 'mkdir -p .test-server/JLPTSuccess && ln -sfn "$PWD" .test-server/JLPTSuccess/N5 && cd .test-server && python -m http.server 8000',
    url: 'http://localhost:8000/JLPTSuccess/N5/',
    timeout: 15_000,
    reuseExistingServer: !process.env.CI,
    stdout: 'ignore',
    stderr: 'pipe',
  },
});
