# -*- coding: utf-8 -*-
"""Append 5 session-flagged bugs to the User Reported Bugs sheet of
the bug tracker xlsx, per Rule 5 artifact-class 5 sync requirement.

One-shot script: run once after the v1.17.13..v1.17.19 work this
session, then can be archived to not-required/."""

import openpyxl
from pathlib import Path

XLSX = Path(__file__).resolve().parent.parent / 'specifications' / 'test-scenarios-by-specialist-perspective.xlsx'

ENTRIES = [
    {
        'date': '2026-05-27',
        'reporter': 'User (live PDF review)',
        'title': 'Audio timer (0:00/0:00) + play/skip/rate buttons appearing in PDF export',
        'description': (
            'User screenshotted a listening-item PDF showing the on-page audio '
            'controls (back / play / forward / time-display / rate buttons) rendering '
            'in the printed/PDF output. Quoted: "when you download anything as pdf, '
            'is it possible not to have this audio timer in the pdf? On page it will '
            'be there, but wont be there on the pdf?"\n\n'
            'Root cause: css/main.css @media print had `audio { display: none }` '
            'which hides the NATIVE <audio> element, but NOT the custom skin wrapper '
            '<div class="audio-skin-controls"> rendered by js/audio-player.js. The '
            'skin is regular HTML — buttons + <span class="audio-skin-time"> showing '
            '"0:00 / 0:00" — so the audio { display: none } rule missed it.\n\n'
            '[FIX 2026-05-27 v1.17.13 (a48b2fdd)]: Added .audio-skin-controls, '
            '.example-audio, .reading-audio, .listening-audio { display: none '
            '!important } to the @media print block. Verified via Playwright print-'
            'media probe + live CSS string-match: all 4 selectors present in the '
            'deployed main.min.css. Listening drills, reading passages, grammar '
            'example audio, and vocab example audio all print without the player '
            'skin after this fix.'
        ),
        'severity': 'Medium',
        'priority': 'P2',
        'status': 'Fixed',
        'commit': 'a48b2fdd',
        'fix_date': '2026-05-27',
    },
    {
        'date': '2026-05-27',
        'reporter': 'User (live PDF review)',
        'title': 'Small empty square/checkbox under each grammar example in PDF export',
        'description': (
            'After the v1.17.13 audio-skin print-hide, user re-screenshotted the '
            'PDF: "one check box is still there on pdf, this also i think not '
            'required". A 17x17 px faint-tinted square was rendering under each '
            'AFFIRMATIVE-tagged grammar example.\n\n'
            'Two iterations to fix:\n\n'
            '[FIX-1 2026-05-27 v1.17.14 (710c8c8c)]: Added catch-all input, select, '
            'textarea, video { display: none !important } to @media print. '
            'Defensive guard against any stray form element. User reported "still '
            'there" after hard-refresh.\n\n'
            '[FIX-2 2026-05-27 v1.17.15 (a695b47b)]: Root-cause diagnosed via '
            'Playwright print-mode DOM probe (tools/diag_print_square_2026_05_27.py '
            'committed). The culprit was <div class="audio-skin"> — the OUTER '
            'wrapper that audio-player.js puts around the audio element + the inner '
            'skin-controls. v1.17.13 hid the INNER .audio-skin-controls but not the '
            'OUTER .audio-skin. With its children all hidden, the outer div '
            'collapsed to its border/padding box = the 17x17 square. Added '
            '.audio-skin to the print-hide list. Playwright probe re-run confirmed '
            "0 small visible elements remain in example li's.\n\n"
            'Process lesson logged in commit body: when a CSS leak survives two '
            'print-rule passes, stop guessing — open the DOM in print emulation '
            'and let the layout report the offender.'
        ),
        'severity': 'Low',
        'priority': 'P3',
        'status': 'Fixed',
        'commit': 'a695b47b',
        'fix_date': '2026-05-27',
    },
    {
        'date': '2026-05-27',
        'reporter': 'User (live PDF review, design-quality complaint)',
        'title': 'Large blank-space zones at page boundaries in grammar pattern PDFs (5pp where 3pp should suffice)',
        'description': (
            'User screenshotted a grammar pattern (n5-095) PDF showing EXPLANATION '
            'followed by ~500px of blank space, then a page break, then DEEP DIVE '
            'on page 2. Repeated at every section boundary -> 5 PDF pages with '
            'dead-space chunks. User quoted: "there\'s a lot of blank/negative '
            'space in the print outs. think like a designer. format properly."\n\n'
            'Root cause (Playwright print-mode probe): `.pattern-detail section { '
            'page-break-inside: avoid }` forced EVERY section (Examples, Deep dive, '
            'Categorized errors, Politeness ladder, etc.) to render atomically. '
            'For 700+px sections this pushed the whole block to the next page, '
            'leaving 200-500px blank at the bottom of the previous page. The wrong '
            'granularity — a printed textbook lets long lists flow across pages, '
            'it just never splits a single example mid-sentence.\n\n'
            '[FIX 2026-05-27 v1.17.16 (6e6d310f)]: 6 design changes to @media print '
            'in css/main.css:\n'
            '  1. Removed `.pattern-detail section { page-break-inside: avoid }`\n'
            '  2. Kept page-break-inside: avoid on individual example/mistakes li\n'
            '  3. Added page-break-after: avoid to .section-title (h3)\n'
            '  4. Added widows: 3; orphans: 3 to body + p + li\n'
            '  5. Tightened section margin 16pt -> 12pt; example-li margin 6pt -> 4pt\n'
            '  6. Set body font-size: 10.5pt; line-height: 1.45 in print only\n\n'
            'Verified via Playwright print-emulation probe on deployed v1.17.16: '
            'doc height 3043 -> 2849 px; sections with forced-avoid 12 -> 0; '
            'estimated pages 5 -> 3; forced-jump blank zones 4-5 -> 0.\n\n'
            '[FOLLOW-UP v1.17.17 (c3893aee)]: Extended same rules to .vocab-detail '
            '/ .kanji-detail / .reading-passage / .listening-item wrappers.'
        ),
        'severity': 'Medium',
        'priority': 'P2',
        'status': 'Fixed',
        'commit': '6e6d310f',
        'fix_date': '2026-05-27',
    },
    {
        'date': '2026-05-27',
        'reporter': 'User (live spot-check)',
        'title': 'Global app-header missing on every static SEO mirror -- 1,410 deep-link pages render without brand/nav',
        'description': (
            'User caught the regression on /N5/learn/n5-002/ and every other '
            'static mirror under /N5/learn/, /N5/kanji/, /N5/reading/, /N5/listening/, '
            '/N5/papers/. After v1.17.6 converted the 3 directory-level mirrors '
            '(learn/, drill/, mock/) to full SPA-shell clones, the 1,410 per-pattern '
            '/ per-page mirrors were left in their "standalone static content" form '
            '— no header, no primary nav. Anyone deep-linking to one of them saw '
            'the per-page content but no top-of-page chrome -> looked broken / '
            'orphaned.\n\n'
            '[FIX 2026-05-27 v1.17.9 (1d77c881)]: New tool '
            'tools/inject_app_header_into_mirrors_2026_05_27.py — injects a static '
            '<header class="app-header"> block (brand mark + 9 primary-nav links) '
            'immediately after the <body> tag in each mirror. All header href '
            'values are absolute (/JLPTSuccess/N5/...) so the same HTML works at '
            'any depth without a <base href>. Idempotent: skips files that already '
            'contain class="app-header".\n\n'
            'Coverage: 1,413 mirrors scanned; 3 already had header (skipped); '
            '1,410 injected; 1,222 also gained main.min.css link; 0 errors. '
            'Preserves every byte of existing per-page SEO content.\n\n'
            '[FOLLOW-UP v1.17.12 (bfee96d8)]: build_static_mirrors.py --stages meta '
            'wiped the header from 10 meta-route mirrors when refreshing them '
            'during the v1.17.11 build. Re-ran the inject script. Process lesson: '
            'meta-mirror regen must be followed by header re-injection in the same '
            'change set.'
        ),
        'severity': 'High',
        'priority': 'P1',
        'status': 'Fixed',
        'commit': '1d77c881',
        'fix_date': '2026-05-27',
    },
    {
        'date': '2026-05-27',
        'reporter': 'User (live spot-check)',
        'title': 'Stale corpus counts on Learn hub -- reading=30/listening=12 instead of 54/50',
        'description': (
            'User screenshot of /N5/learn/ home showed "Dokkai (Reading): 30 '
            'graded passages" and "Listening: 12 items" — hardcoded fallback '
            'constants in js/learn.js renderHub() that had not been updated when '
            'the reading/listening corpora grew. Live data/version.json.counts '
            'showed reading=54, listening=50. Quoted user response when shown the '
            'live page: "is this how this page is supposed to be? are you '
            'referring to design spec? where the hell is your bug verification '
            'mechanism?"\n\n'
            '[FIX 2026-05-27 v1.17.5 (e7ab0288)]: Fixed the 5 hardcoded fallback '
            'constants in renderHub() to match live counts (grammar=178, vocab=995, '
            'kanji=106, reading=54, listening=50). Added new CI invariant JA-169 '
            'to lock the fallbacks against data/version.json.counts going forward '
            '— future drift will fail CI until the fallback constants are bumped '
            'to match. 171 total invariants after this add.'
        ),
        'severity': 'Medium',
        'priority': 'P2',
        'status': 'Fixed',
        'commit': 'e7ab0288',
        'fix_date': '2026-05-27',
    },
]


def main():
    wb = openpyxl.load_workbook(XLSX)
    ws = wb['User Reported Bugs']
    print(f'Before append: max_row={ws.max_row}')
    for e in ENTRIES:
        next_row = ws.max_row + 1
        ws.cell(row=next_row, column=1, value='="BUG-"&TEXT(ROW()-3,"000")')
        ws.cell(row=next_row, column=2, value=e['date'])
        ws.cell(row=next_row, column=3, value=e['reporter'])
        ws.cell(row=next_row, column=4, value=e['title'])
        ws.cell(row=next_row, column=5, value=e['description'])
        ws.cell(row=next_row, column=6, value=e['severity'])
        ws.cell(row=next_row, column=7, value=e['priority'])
        ws.cell(row=next_row, column=8, value=e['status'])
        ws.cell(row=next_row, column=9, value=e['commit'])
        ws.cell(row=next_row, column=10, value=e['fix_date'])
        bug_id = f'BUG-{next_row-3:03d}'
        print(f'  added row {next_row}: {bug_id} - {e["title"][:55]}')
    wb.save(XLSX)
    print(f'After append: max_row={ws.max_row} (saved)')


if __name__ == '__main__':
    main()
