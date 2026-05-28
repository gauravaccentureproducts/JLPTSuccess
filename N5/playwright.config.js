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
    // baseURL has no /JLPTSuccess/N5 prefix. The webServer below
    // (tools/test_server.py) makes `GET /foo` and `GET /JLPTSuccess/
    // N5/foo` resolve to the SAME file (`N5/foo`), so the SPA's
    // base-href-resolved asset fetches AND test calls like
    // `page.goto('/learn/n5-098/')` both work.
    baseURL: 'http://localhost:8000',
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
    // 2026-05-27: custom test server (tools/test_server.py) instead
    // of plain `python -m http.server`. The custom server strips the
    // /JLPTSuccess/N5 production URL prefix from inbound paths so
    // both `GET /css/main.min.css` AND `GET /JLPTSuccess/N5/css/
    // main.min.css` resolve to N5/css/main.min.css on disk. Needed
    // because index.html ships with `<base href="/JLPTSuccess/N5/">`
    // (v1.17.7) — without the prefix-stripping the browser issues
    // base-href-resolved asset fetches that all 404, the SPA never
    // boots, and every test fails on an empty DOM.
    //
    // Tests can use bare paths (page.goto('/'), page.goto(
    // '/learn/n5-098/')) and the SPA's relative-asset fetches both
    // work. Pure shell-portable (Python 3 only); no symlinks, no
    // platform-specific commands. See tools/test_server.py docstring.
    command: 'python tools/test_server.py',
    url: 'http://localhost:8000/',
    timeout: 15_000,
    reuseExistingServer: !process.env.CI,
    stdout: 'ignore',
    stderr: 'pipe',
  },
});
