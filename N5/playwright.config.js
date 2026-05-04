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
  workers: process.env.CI ? 1 : undefined,
  reporter: process.env.CI ? [['html', { open: 'never' }], ['github']] : 'list',
  use: {
    baseURL: 'http://localhost:8000',
    trace: 'on-first-retry',
    screenshot: 'only-on-failure',
    video: 'retain-on-failure',
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
    command: 'python -m http.server 8000',
    url: 'http://localhost:8000/',
    timeout: 15_000,
    reuseExistingServer: !process.env.CI,
    stdout: 'ignore',
    stderr: 'pipe',
  },
});
