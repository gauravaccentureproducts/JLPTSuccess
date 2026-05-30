#!/usr/bin/env python3
"""Register 5 strategic-improvement items (IMP-1..5) to the bug tracker.

Source: 2026-05-27 5-point quality-improvement audit (user-requested).
Items are improvement opportunities, not defects — same shape as
prior IMP-NN entries (e.g., IMP-101 native-teacher review).
"""
from openpyxl import load_workbook
from pathlib import Path

XLSX = Path('specifications/test-scenarios-by-specialist-perspective.xlsx')
SHEET = 'User Reported Bugs'

ROWS = [
    # (severity, priority, status, title, description)
    (
        'High', 'P2', 'Open (Deferred — budget-gated)',
        "IMP-1 -- Native-human Japanese-teacher review pass (gated by budget; IMP-101 generalization)",
        "5-point quality audit 2026-05-27 surfaced: ~57 cm rows + 23 ambiguity-fix rows + 173 auto-authored explanation_ja entries all carry review_status='ai_native_reviewer_2026_05_24' which is EXPLICITLY bounded as not equivalent to a human native-Japanese-teacher pass (per _meta.review_status_note). The single highest content-quality lever; programmatic audits catch shape but cannot catch: natural-sounding vs awkward Japanese sentences, cultural appropriateness, JLPT-level fit, audio pitch accent quality, semantic precision of explanation_ja. Action: hire JLPT-certified freelance teacher (Lang-8 / italki / local) for ~10 hours; use provenance='auto_fix_2026_05_24' filter to focus the review pass; update review_status to 'native_reviewed' on each row they pass. Estimated cost: ~$300-500 at freelance rates. Generalization of IMP-101 which is queued behind monetization/sponsorship per _meta.review_status_note."
    ),
    (
        'Medium', 'P3', 'Open',
        "IMP-2 -- 'Report a problem' button missing from learner UI (production feedback loop)",
        "5-point quality audit 2026-05-27 surfaced: no in-app channel for actual learners to flag content errors / UI bugs / suggestions. Currently all changes are reviewer-driven (user + Claude + occasional independent reviewers). One real learner spotting a wrong answer is worth 100 audit cycles in surfacing real issues. Action: add a small 'Report' button (e.g., bottom-right of pattern detail pages + listening items + reading passages) that opens a pre-filled GitHub issue via gauravaccentureproducts/JLPTSuccess/issues/new?template=content-error.md with URL + pattern/item ID + free-text box. Anonymous GitHub issues work; no login required. Closes the production feedback gap once real users arrive. Estimated effort: 1 commit, ~1 hour."
    ),
    (
        'Medium', 'P2', 'Open',
        "IMP-3 -- CI workflow not running on git push (drift accumulates silently)",
        "5-point quality audit 2026-05-27 surfaced: tools/check_content_integrity.py (169 invariants) + tools/audit_all.py (7 corpora) + Playwright suite all run LOCALLY ONLY when the user/Claude manually invokes them. Between manual runs, drift can accumulate; a broken commit can sit on master for days before being noticed. Action: add .github/workflows/ci.yml with 3 jobs — (1) python tools/check_content_integrity.py, (2) python tools/audit_all.py, (3) npm ci && npm run test:smoke. Triggers on push to master + on PRs. PR turns red if any job fails. Free for public repos. Estimated effort: 1 commit, ~30 min including yaml + jobs config + first-push verification."
    ),
    (
        'Low', 'P3', 'Open (Deferred — high refactor risk)',
        "IMP-4 -- data/grammar.json 3MB load on every page (perf — defer until N4/N3 expansion or mobile complaints)",
        "5-point quality audit 2026-05-27 surfaced: data/grammar.json is 3.2 MB on the wire; every page download hauls all 178 patterns even when the user is viewing 1. On mobile / slow Wi-Fi this is noticeable. Proposed fix: split into data/grammar/n5-001.json ... n5-188.json (one file per pattern, ~18 KB each) + thin data/grammar-index.json (~30 KB) for the listing page. Service worker prefetches next 5 patterns in background. RISK: ~50 places reference data/grammar.json directly — CI invariants (10+ JA-NN checks), audit_all.py, check_content_integrity.py, the SPA's learn-grammar.js fetch wrapper, 178 static mirrors, service worker PRECACHE list, search index builder. Multi-day refactor with high regression risk; the audits THEMSELVES need updating during the refactor. DEFERRED: file load takes 1-2s on modern connections, no real user complaints yet, structural refactor only justified when N4/N3 levels are added (total >5 MB makes split mandatory) OR when first mobile-slow-connection complaint arrives. Estimated effort: 3-5 days when triggered."
    ),
    (
        'Medium', 'P3', 'Open',
        "IMP-5 -- No production error monitoring (Sentry or equivalent) -- invisible runtime errors in production",
        "5-point quality audit 2026-05-27 surfaced: when a real user hits a JavaScript error on the live site (https://gauravaccentureproducts.github.io/JLPTSuccess/), it disappears into their browser console. The maintainer never sees it. Production-only bugs (specific Safari versions, weird input data, race conditions, network failures, service-worker cache misses) are entirely invisible without telemetry. Action: sign up free Sentry account (free tier = 5K events/month, sufficient for early-stage site); add ~5 lines to js/app.js to initialize SDK with project DSN; errors auto-report with stack trace + browser/OS/URL. Sentry DSN is non-sensitive but kept in .claude/settings.local.json (gitignored) for personal-machine setup. Claude can implement the SDK integration with a placeholder DSN; user finishes by pasting actual DSN. Estimated effort: 1 commit by Claude + 5 min user setup. Combined with IMP-2 (Report button), forms a complete production-feedback loop."
    ),
]


def main():
    wb = load_workbook(XLSX)
    ws = wb[SHEET]
    start_row = ws.max_row + 1
    fix_date = ''
    fix_commit = ''

    print(f'starting at row {start_row}')
    for off, (sev, pri, status, title, desc) in enumerate(ROWS):
        r = start_row + off
        ws.cell(row=r, column=1, value='="BUG-"&TEXT(ROW()-3,"000")')
        ws.cell(row=r, column=2, value='2026-05-27')
        ws.cell(row=r, column=3, value="Internal -- 5-point strategic-improvement audit (2026-05-27)")
        ws.cell(row=r, column=4, value=title)
        ws.cell(row=r, column=5, value=desc)
        ws.cell(row=r, column=6, value=sev)
        ws.cell(row=r, column=7, value=pri)
        ws.cell(row=r, column=8, value=status)
        ws.cell(row=r, column=9, value=fix_date)
        ws.cell(row=r, column=10, value=fix_commit)
        print(f'  row {r}: {title[:80]}')

    wb.save(XLSX)
    print(f'\nsaved: {XLSX}')


if __name__ == '__main__':
    main()
