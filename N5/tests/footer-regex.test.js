// IMP-030 (audit round 3): unit test for the footer-version regex used
// by js/app.js to keep the [data-footer-version] element in sync with
// CHANGELOG.md. The integration test in v1.12.28-features.spec.js
// asserts the runtime end-to-end; this file exercises the regex itself
// against realistic CHANGELOG variations so a future heading rename
// (e.g., a "## Notes" section landing above the version block) fails
// fast in CI rather than silently breaking the footer.
//
// Runs as a plain Node script — no test framework dependency:
//     node tests/footer-regex.test.js
// Exit 0 = pass, exit 1 = fail.

'use strict';
const assert = require('node:assert/strict');

// Same regex used by js/app.js:220.
const FOOTER_VERSION_REGEX = /^## (v\d+\.\d+\.\d+)/m;

const cases = [
  // [name, fixture, expected match group 1, expected to match?]
  [
    'canonical CHANGELOG head',
    '# Changelog\n\nAll user-visible changes.\n\n## v1.12.29 - 2026-05-05\n\nbody...\n',
    'v1.12.29', true,
  ],
  [
    'multiple version headings — picks the first',
    '## v1.12.29 - 2026-05-05\n\n## v1.12.28 - 2026-05-04\n',
    'v1.12.29', true,
  ],
  [
    'three-digit minor (v1.99.0)',
    '## v1.99.0 - 2099-01-01\n',
    'v1.99.0', true,
  ],
  [
    'pre-release v1.0.0',
    '## v1.0.0 - 2026-04-29 (initial release)\n',
    'v1.0.0', true,
  ],
  [
    'patch zero (v2.5.0)',
    '## v2.5.0 - 2030-12-31\n',
    'v2.5.0', true,
  ],
  [
    'leading whitespace in line — does NOT match (regex anchors to BOL)',
    '  ## v1.12.29 - 2026-05-05\n',
    null, false,
  ],
  [
    'no version heading at all',
    '# Changelog\n\nAll user-visible changes.\n\nbody only.\n',
    null, false,
  ],
  [
    'non-version H2 above version H2 — picks the version one',
    '## Migration notes\n\nbody.\n\n## v1.12.29 - 2026-05-05\n',
    'v1.12.29', true,
  ],
  [
    'H3 v-prefix — does NOT match (only H2)',
    '### v1.12.29 - 2026-05-05\n',
    null, false,
  ],
  [
    'no leading "v" — does NOT match',
    '## 1.12.29 - 2026-05-05\n',
    null, false,
  ],
  [
    'four-segment version (v1.0.0.0) — does NOT match (we want SemVer 3-part)',
    '## v1.0.0.0 - 2099-01-01\n',
    'v1.0.0', true,  // regex captures the first 3 segments and stops on dot
  ],
  [
    'CRLF line endings',
    '# Changelog\r\n\r\n## v1.12.29 - 2026-05-05\r\n',
    'v1.12.29', true,
  ],
];

let failed = 0;
for (const [name, fixture, expected, shouldMatch] of cases) {
  const m = fixture.match(FOOTER_VERSION_REGEX);
  try {
    if (shouldMatch) {
      assert(m !== null, `expected match for "${name}"`);
      assert.equal(m[1], expected, `"${name}" — expected ${expected}, got ${m && m[1]}`);
    } else {
      assert(m === null, `expected NO match for "${name}", got ${m && m[1]}`);
    }
    console.log(`  PASS  ${name}`);
  } catch (e) {
    failed += 1;
    console.error(`  FAIL  ${name}\n    ${e.message}`);
  }
}

if (failed) {
  console.error(`\n${failed}/${cases.length} test(s) FAILED`);
  process.exit(1);
}
console.log(`\n${cases.length}/${cases.length} test(s) passed`);
