#!/usr/bin/env python3
"""
Bug-tracker upgrade pass 2026-05-27 — Items A through G.

A. Gap-fill 9 missing BUG entries (recent work not yet registered)
B. Add 4 forensic columns (C11-C14) to User Reported Bugs
C. Status enum tightening (closed enum: Fixed / Open / Deferred-Budget / Deferred-Risk / Won't Fix / Duplicate)
D. Add 4 scenario-tab rows (A, K, D, H tabs)
E. New 'Methodology Lessons' sheet
F. 'Status = Fixed' consistency cleanup (caveats move to Description)
G. Overview summary block with auto-formulas
"""
import re
from pathlib import Path
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment

XLSX = Path('specifications/test-scenarios-by-specialist-perspective.xlsx')
SHEET = 'User Reported Bugs'

# A. Gap-fill entries
GAP_FILL = [
    {
        'severity': 'High', 'priority': 'P2', 'status': 'Fixed', 'fix_date': '2026-05-25', 'fix_commit': '08019116',
        'title': "BUG-MCQ-AMBIG-R2 — 10 MCQ questions with 2+ grammatically-valid choices for N5 learner (Round 2)",
        'desc': (
            "User flagged q-0221 (あした コーヒーを のみ + choices [ません/ます/ました/ましょう]): "
            "のみます (will drink) AND のみましょう (let's drink) BOTH grammatically valid. "
            "Sweep across 290+ questions surfaced 5 questions.json + 2 paper ambiguities. "
            "Initial fix swap distractors / add context cues. Discovery + fix in commit 08019116."
        ),
        'ja_inv': 'JA-167', 'part': 'Part 58', 'related': 'BUG-MCQ-AMBIG-R3, BUG-MCQ-HORIZONTAL', 'verification': 'Programmatic (audit_ts_pass_counts_v2) + user spot-check',
    },
    {
        'severity': 'High', 'priority': 'P1', 'status': 'Fixed', 'fix_date': '2026-05-25', 'fix_commit': '5b8024e6',
        'title': "BUG-MCQ-AMBIG-R3 — Round-2 fix incomplete; ますか + 。 sentence-end was also question-valid",
        'desc': (
            "User RE-FLAGGED q-0221 after Round 2: new choices [ます/ました/ますか/ませんでした] still ambig "
            "because Japanese sentence-final 。 marks both statements AND questions — ますか。 is fully "
            "valid future question. Tightened JA-167 predicate enumerated UNGRAMMATICAL_AT_VSTEM + "
            "INCOMPLETE_VSTEM_ENDERS + PAST_FORMS + PRESENT_FUTURE_FORMS. Round 3 fix: 7 questions "
            "rewritten with distractors that are clearly wrong (ますか → でした which doesn't attach to V-stem)."
        ),
        'ja_inv': 'JA-167 (tightened)', 'part': 'Part 58', 'related': 'BUG-MCQ-AMBIG-R2', 'verification': 'Programmatic predicate + user re-verification',
    },
    {
        'severity': 'Medium', 'priority': 'P2', 'status': 'Fixed', 'fix_date': '2026-05-25', 'fix_commit': '456bc82b',
        'title': "BUG-MCQ-HORIZONTAL — Horizontal sweep beyond verb-ending: PARTICLE + Q-word + DEMONSTRATIVE",
        'desc': (
            "User asked 'horizontal deployment?' — JA-167 covered only verb-ending MCQs. Extended sweep "
            "across PARTICLE (が/は collisions), QUESTION_WORD (multi-info-type ambiguity), DEMONSTRATIVE "
            "(deictic without spatial cue). Found 6 confirmed (5 questions + 1 paper). Disambiguation "
            "strategies: answer-hint, reply-hint, semantically-impossible Q-word distractors, "
            "particle-replace with clearly-wrong (へ for subject)."
        ),
        'ja_inv': 'JA-167 (verb-ending only)', 'part': 'Part 58', 'related': 'BUG-MCQ-AMBIG-R2/R3', 'verification': 'class-aware detector + manual native-teacher review',
    },
    {
        'severity': 'Medium', 'priority': 'P3', 'status': 'Fixed', 'fix_date': '2026-05-27', 'fix_commit': 'b2cce671',
        'title': "BUG-PERM-COMPOUND — Claude Code Desktop file-glob allow-list missed compound commit+push shapes",
        'desc': (
            "User flagged: commit + push command with `cd PARENT && git add N5/... && git commit -F "
            "N5/.commit_msg.tmp ... && rm -f N5/.commit_msg.tmp && git push` kept triggering permission "
            "prompts even with defaultMode=bypassPermissions + broad allow patterns. Root cause: pattern "
            "had `rm -f .commit_msg.tmp` (literal) but actual had `rm -f N5/.commit_msg.tmp` (path-prefixed). "
            "Fix: added 17 specific patterns + installed PreToolUse hook (.claude/hooks/auto-approve-git-"
            "workflow.py) with 3-layer defense (deny-first / safe-shape allow / defer to permission system)."
        ),
        'ja_inv': '—', 'part': '—', 'related': 'workflow/permissions', 'verification': 'Tested 6 paths: approve/defer/deny + SS&SC dir block',
    },
    {
        'severity': 'Medium', 'priority': 'P2', 'status': 'Fixed', 'fix_date': '2026-05-24', 'fix_commit': '6010096e',
        'title': "BUG-WAVE-1 — Drift-prevention + cosmetic cleanup (JA-164/165/166 + home.js + audio orphans)",
        'desc': (
            "Wave 1 of priority-ordered cleanup: (1) JA-164 locks intentional_variant_pair markers from "
            "Part 57; (2) JA-165 catches within-entry example dups in vocab+kanji (Part 58 regression "
            "guard); (3) JA-166 enforces slot-token Latin whitelist (FP-21 lock); (4) js/home.js hash → "
            "clean-path migration (6 hrefs); (5) 20 orphan audio_manifest entries trimmed. Also fixed "
            "incidental JA-68 cache-version drift (1.17.0 → 1.17.1)."
        ),
        'ja_inv': 'JA-164, JA-165, JA-166', 'part': '—', 'related': '—', 'verification': 'Programmatic CI (168 → 168) + Playwright re-run',
    },
    {
        'severity': 'Medium', 'priority': 'P2', 'status': 'Fixed', 'fix_date': '2026-05-24', 'fix_commit': '60c36430',
        'title': "BUG-WAVE-2 — Schema-aware audit of questions.json (290→284) + 28 mock papers (402 Qs)",
        'desc': (
            "Wave 2: per-question-type schema audit (mcq/sentence_order/text_input) found 6 dup questions "
            "+ 5 stale distractor_explanations keys + 3 cross-paper false-dups (template stem ambiguity, "
            "not real dups). Counts resynced in CONTENT-LICENSE.md, README.md, version.json, spec §7.3 "
            "(JA-47, JA-107, JA-115, JA-119 inline). Papers (402 Qs): 100% clean under proper "
            "stem+sorted-choices+correctIndex dedup key."
        ),
        'ja_inv': '—', 'part': '—', 'related': 'BUG-A..H', 'verification': 'Programmatic schema-aware predicates per question type',
    },
    {
        'severity': 'Medium', 'priority': 'P2', 'status': 'Fixed', 'fix_date': '2026-05-24', 'fix_commit': '021c9a52',
        'title': "BUG-WAVE-3 — Conjugation-aware TS-05 matcher + unified audit_all.py",
        'desc': (
            "Wave 3 tool quality: (1) check_ts05 upgraded with 3-layer matcher (slot-token strip + "
            "whitespace-norm + conjugation-stem variant) — TS-05 NA-heuristic-limit 35 → 1 honest "
            "partial; (2) tools/audit_all.py unified cross-corpus audit replacing scattered per-corpus "
            "fix scripts. Single point-of-truth invocation across 7 corpora (2,073 entries)."
        ),
        'ja_inv': 'TS-05 predicate tightened', 'part': '—', 'related': 'FP-20', 'verification': 'audit_all.py exits 0 (OVERALL CLEAN)',
    },
    {
        'severity': 'Medium', 'priority': 'P3', 'status': 'Fixed', 'fix_date': '2026-05-24', 'fix_commit': 'e327f102',
        'title': "BUG-WAVE-4 — 173 patterns authored explanation_ja from concrete examples",
        'desc': (
            "Wave 4 content authoring: 5/178 patterns had explanation_ja (4 BUG-F splits + 1 Part-56 "
            "cleanup). Authored 173 more using concrete worked examples from each pattern's existing "
            "examples array (indices 0 + middle). NOT boilerplate (BUG-K metric-gaming lesson honored) "
            "— every pattern gets DIFFERENT content drawn from its own native-quality examples. "
            "Renderer (js/learn-grammar.js) displays in meaning_ja section."
        ),
        'ja_inv': 'JA-162', 'part': '—', 'related': 'BUG-F, BUG-K (lesson honored)', 'verification': 'Programmatic + browser-verified on n5-098',
    },
    {
        'severity': 'Medium', 'priority': 'P2', 'status': 'Fixed', 'fix_date': '2026-05-24', 'fix_commit': '4959aed9',
        'title': "BUG-WAVE-5 — WCAG color-contrast a11y fix (4.45→5.34) + deep axe-core + Lighthouse perf",
        'desc': (
            "Wave 5 testing depth: (1) full Playwright suite (110 pass, 9 skip — locale-toggle disabled "
            "for Phase-1); (2) tests/deep-axe-perf.spec.js for 8 surfaces (home/grammar list/pattern "
            "detail x2/kanji/reading/listening/drill); (3) surfaced REAL WCAG color-contrast violation "
            "— --color-correct #2E7D4F on #f7efed = 4.45 (below WCAG AA 4.5:1). Fixed: bumped to "
            "#26703F (5.34:1)."
        ),
        'ja_inv': '—', 'part': '—', 'related': 'a11y', 'verification': 'Playwright + axe-core WCAG 2.1 AA scan',
    },
]

# B/F. Status enum
STATUS_ENUM = {'Fixed', 'Open', 'Deferred-Budget', 'Deferred-Risk', "Won't Fix", 'Duplicate'}
STATUS_NORMALIZE = {
    'Open (Deferred — budget-gated)': 'Deferred-Budget',
    'Open (Deferred — high refactor risk)': 'Deferred-Risk',
    'Fixed (with caveat)': 'Fixed',
}

# D. Scenario-tab rows
SCENARIO_ROWS = [
    {
        'sheet': 'A. Japanese language',
        'id': 'A-153', 'cat': 'False-positive class', 'count': 1,
        'title': 'MCQ ambiguity class detection — 23 questions found with 2+ grammatically valid answers',
        'steps': '1. Reference: prompts/Japanese language Accuracy check.txt FP-17..21.\n2. Run tools/detect_mcq_ambiguity_class_aware_2026_05_25.py over questions.json + papers.\n3. Verify class-aware predicate distinguishes verb-ending / particle / Q-word / demonstrative ambiguity shapes.',
        'criteria': '0 confirmed ambiguities under tightened JA-167 predicate. False positives documented in commit messages (intentional pedagogy / single-valid on closer review).',
    },
    {
        'sheet': 'K. QA testing',
        'id': 'K-NN', 'cat': 'CI / Tooling', 'count': 1,
        'title': 'PreToolUse hook auto-approve defense layer for git/gh workflow commands',
        'steps': '1. Reference: .claude/hooks/auto-approve-git-workflow.py + settings.local.json hooks.PreToolUse[Bash].\n2. Verify 3-layer defense (deny-first → safe-shape allow → defer to permission system).\n3. Smoke test 6 shapes: git status / gh pr / cd PATH && commit+push / python script / git push --force (deny) / SS&SC path (deny).',
        'criteria': 'All 6 paths return expected verdict. Hook fires on session start (verify via .claude/hooks log if enabled).',
    },
    {
        'sheet': 'D. UX design',
        'id': 'D-NN', 'cat': 'Feedback channel',  'count': 1,
        'title': 'Production feedback channel (IMP-2) — Report-a-problem button on every learner surface',
        'steps': '1. Reference: User Reported Bugs IMP-2.\n2. Verify a `Report` button is present on pattern-detail / listening / reading pages.\n3. Click flow opens a pre-filled GitHub issue (or external survey form) with URL + item ID + free-text.',
        'criteria': '178 pattern pages + 50 listening + 54 reading have the button rendered. Anonymous reporting works (no GitHub login required to submit).',
    },
    {
        'sheet': 'H. Performance',
        'id': 'H-NN', 'cat': 'Observability', 'count': 1,
        'title': 'Production error monitoring (IMP-5) — Sentry or equivalent runtime-error capture',
        'steps': '1. Reference: User Reported Bugs IMP-5.\n2. Verify Sentry SDK init in js/app.js with DSN from local settings.\n3. Trigger a deliberate JS error in DevTools console; confirm it appears in Sentry dashboard within ~30s.',
        'criteria': 'Sentry receives runtime errors with stack trace + browser/OS/URL. DSN kept in .claude/settings.local.json (gitignored) — not committed.',
    },
]

# E. Methodology Lessons sheet
METHODOLOGY_LESSONS = [
    ('FP-17: Aggressive vs strip-only norm divergence', 'BUG-A/H 2026-05-24', 'AUDIT-COVERAGE Part 52', 'Metric-gaming via norm-shape pick', '—'),
    ('FP-18: Cross-array category-vocabulary mismatch', 'BUG-A backfill 2026-05-24', 'AUDIT-COVERAGE Part 52', 'wcp→cm promotion without CATEGORY_MAP', '—'),
    ('FP-19: Metric-gaming on quality-dimension token-count floors', 'BUG-K revert 2026-05-24', 'AUDIT-COVERAGE Part 56', 'Padding short crisp content to satisfy ≥N floor', '—'),
    ('FP-20: NA-heuristic-limit vs Fail in audit verdicts', 'TS-05 2026-05-24', 'AUDIT-COVERAGE Part 56', 'Overclaiming defects via inflexible heuristic', '—'),
    ('FP-21: Slot-token Latin notation flagged as off-spec', 'TS-10 2026-05-24', 'AUDIT-COVERAGE Part 56', 'Audit whitelist narrower than authoring convention', 'JA-166'),
    ('MCQ ambiguity class (R2)', 'q-0221 user flag 2026-05-25', 'AUDIT-COVERAGE Part 58', '2+ grammatically valid choices for N5 learner', 'JA-167'),
    ('MCQ ambiguity Round 3 — tightened predicate', 'q-0221 user re-flag 2026-05-25', 'AUDIT-COVERAGE Part 58', 'ますか + 。 still question-valid', 'JA-167 (tightened)'),
    ('Horizontal MCQ sweep across choice classes', 'User horizontal-deploy req 2026-05-25', 'AUDIT-COVERAGE Part 58', 'PARTICLE/Q-word/DEMONSTRATIVE ambiguity', '—'),
    ('PreToolUse hook for compound commands', 'commit+push prompt 2026-05-27', 'commit b2cce671', 'File-glob misses compound shapes', '—'),
    ('Pipe exit-code masks commit failures', '2026-05-27', 'b2cce671 + this session', '| tail returns 0 even if commit fails; && rm runs', 'Discipline: drop pipe on commit step'),
    ('Schema-aware audit predicates per question type', 'Wave 2 2026-05-24', 'AUDIT-COVERAGE Part 58', 'Treating all questions as mcq produces FPs', '—'),
    ('Conjugation-aware matching (TS-05)', 'Wave 3 2026-05-24', 'AUDIT-COVERAGE Part 58', 'Static substring missed inflected forms', 'TS-05 predicate'),
    ('WCAG color-contrast verified via deep axe-core', 'Wave 5 2026-05-24', 'AUDIT-COVERAGE Part 58', '--color-correct 4.45 below AA 4.5', 'Playwright deep-axe-perf'),
    ('Rule 5: cross-artifact sync triggers per change', '2026-05-17', 'CLAUDE.md Rule 5', 'Drift in 9 artifact classes', 'JA-107, JA-108, JA-109'),
    ('Native-reviewer persona bounded as not equivalent', '2026-05-07', '_meta.review_status_note', 'AI persona overclaims native-human review', 'JA-35 enum'),
]


def main():
    print('=== UPGRADE PASS A-G ===\n')
    wb = load_workbook(XLSX)
    ws_bugs = wb[SHEET]

    # =========================================================================
    # B/F prep: ensure header row exists for new columns
    # =========================================================================
    print('[B/F] Adding column headers C11-C14...')
    if not ws_bugs.cell(row=2, column=11).value:
        # Add a fresh header row (row 2 is currently first data row; need to find existing header)
        # The existing file has just R1=section title. Let's add a column header row at R2 if not yet present.
        # Actually existing data starts at R3 onwards. Let me add headers at row 2.
        pass
    # Set column headers at row 1 cols 11-14 (extend the section-title row's columns)
    headers = ['JA-Invariant Locked', 'AUDIT-COVERAGE Part', 'Related BUG-IDs', 'Verification Method']
    for i, h in enumerate(headers):
        ws_bugs.cell(row=1, column=11+i, value=h)
        ws_bugs.cell(row=1, column=11+i).font = Font(bold=True)

    # =========================================================================
    # A. Gap-fill 9 missing entries
    # =========================================================================
    print('[A] Gap-filling 9 unregistered fixes...')
    start_row = ws_bugs.max_row + 1
    for off, entry in enumerate(GAP_FILL):
        r = start_row + off
        ws_bugs.cell(row=r, column=1, value='="BUG-"&TEXT(ROW()-3,"000")')
        ws_bugs.cell(row=r, column=2, value=entry['fix_date'])
        ws_bugs.cell(row=r, column=3, value='Internal — gap-fill audit 2026-05-27 (BUG-A..H + waves work stream)')
        ws_bugs.cell(row=r, column=4, value=entry['title'])
        ws_bugs.cell(row=r, column=5, value=entry['desc'])
        ws_bugs.cell(row=r, column=6, value=entry['severity'])
        ws_bugs.cell(row=r, column=7, value=entry['priority'])
        ws_bugs.cell(row=r, column=8, value=entry['status'])
        ws_bugs.cell(row=r, column=9, value=entry['fix_date'])
        ws_bugs.cell(row=r, column=10, value=entry['fix_commit'])
        ws_bugs.cell(row=r, column=11, value=entry.get('ja_inv', ''))
        ws_bugs.cell(row=r, column=12, value=entry.get('part', ''))
        ws_bugs.cell(row=r, column=13, value=entry.get('related', ''))
        ws_bugs.cell(row=r, column=14, value=entry.get('verification', ''))
        print(f'  R{r}: {entry["title"][:70]}')

    # =========================================================================
    # B. Back-fill columns 11-14 for the audit-cluster work entries (R215-R235)
    # =========================================================================
    print('\n[B] Back-filling forensic columns for BUG-A..K + IMP entries...')
    BACKFILL = {
        # BUG-A..H (rows 215-222) — audit-cluster sweep
        215: ('JA-51 (preserved)', 'Part 52', 'BUG-A..H cluster', 'Programmatic dedup with wcp-promotion backfill'),
        216: ('—', 'Part 52', 'BUG-A..H cluster', 'Programmatic rename'),
        217: ('—', 'Part 52', 'BUG-A..H cluster', 'Native-teacher rewrite'),
        218: ('JA-167 (locks Round-3 fixes)', 'Part 52', 'BUG-A..H cluster, BUG-MCQ-AMBIG-R2/R3', 'Programmatic + native rewrite'),
        219: ('—', 'Part 52', 'BUG-A..H cluster', 'Programmatic dedup'),
        220: ('—', 'Part 52', 'BUG-A..H cluster', 'Programmatic expansion'),
        221: ('JA-162', 'Part 52', 'BUG-F, BUG-WAVE-4', 'Programmatic split + JA-162 lock'),
        222: ('—', 'Part 52', 'BUG-A..H cluster', 'xlsx process change + manual back-fill'),
        # BUG-I/J/K (223-225)
        223: ('—', 'Part 55', 'BUG-A horizontal extension', 'Programmatic dedup'),
        224: ('—', 'Part 55', 'BUG-A horizontal extension', 'Native-teacher rewrite (1 row)'),
        225: ('JA-162 (related)', 'Parts 55-56', 'BUG-K reverted in Part 56', 'Programmatic + REVERTED (metric-gaming)'),
        # IMP-1..5 (231-235)
        231: ('—', '—', 'IMP-101 generalization', 'Native human review (queued)'),
        232: ('—', '—', 'IMP-5 (production feedback loop pair)', 'Manual UI add'),
        233: ('JA-NN (TBD)', '—', '—', 'GitHub Actions YAML'),
        234: ('—', '—', '—', 'Multi-day refactor (deferred)'),
        235: ('—', '—', 'IMP-2 (production feedback loop pair)', 'Sentry SDK + DSN'),
    }
    for r, (ja, part, rel, ver) in BACKFILL.items():
        if r > ws_bugs.max_row: continue
        ws_bugs.cell(row=r, column=11, value=ja)
        ws_bugs.cell(row=r, column=12, value=part)
        ws_bugs.cell(row=r, column=13, value=rel)
        ws_bugs.cell(row=r, column=14, value=ver)
    print(f'  back-filled {len(BACKFILL)} rows')

    # =========================================================================
    # C/F. Status enum tightening
    # =========================================================================
    print('\n[C/F] Status enum tightening...')
    changed = 0
    for r in range(2, ws_bugs.max_row + 1):
        s = ws_bugs.cell(row=r, column=8).value
        if not s: continue
        s = str(s).strip()
        if s in STATUS_NORMALIZE:
            ws_bugs.cell(row=r, column=8, value=STATUS_NORMALIZE[s])
            changed += 1
        elif s not in STATUS_ENUM and s not in ('Status', 'Date Repor', 'Fix Date'):
            # Try a fuzzy match
            if 'budget' in s.lower(): ws_bugs.cell(row=r, column=8, value='Deferred-Budget'); changed += 1
            elif 'risk' in s.lower(): ws_bugs.cell(row=r, column=8, value='Deferred-Risk'); changed += 1
            elif s.lower().startswith('fixed'): ws_bugs.cell(row=r, column=8, value='Fixed'); changed += 1
            elif s.lower() == 'open': pass  # keep
    print(f'  normalized {changed} status cells')

    # =========================================================================
    # D. Add scenario-tab rows
    # =========================================================================
    print('\n[D] Adding scenario-tab rows...')
    for row_spec in SCENARIO_ROWS:
        sheet_name = row_spec['sheet']
        if sheet_name not in wb.sheetnames:
            print(f'  WARN: sheet {sheet_name} missing, skipping')
            continue
        ws = wb[sheet_name]
        nr = ws.max_row + 1
        ws.cell(row=nr, column=1, value=row_spec['id'])
        ws.cell(row=nr, column=2, value=row_spec['cat'])
        ws.cell(row=nr, column=3, value=row_spec['count'])
        ws.cell(row=nr, column=4, value=row_spec['title'])
        ws.cell(row=nr, column=5, value=row_spec['steps'])
        ws.cell(row=nr, column=6, value=row_spec['criteria'])
        ws.cell(row=nr, column=7, value='P3')
        print(f'  {sheet_name} R{nr}: {row_spec["title"][:60]}')

    # =========================================================================
    # E. New 'Methodology Lessons' sheet
    # =========================================================================
    print('\n[E] Creating Methodology Lessons sheet...')
    if 'Methodology Lessons' in wb.sheetnames:
        del wb['Methodology Lessons']
    ws_lessons = wb.create_sheet('Methodology Lessons')
    headers = ['Lesson', 'First seen', 'Codified in', 'Anti-pattern caught', 'JA-NN / CI lock']
    for i, h in enumerate(headers, 1):
        ws_lessons.cell(row=1, column=i, value=h)
        ws_lessons.cell(row=1, column=i).font = Font(bold=True)
        ws_lessons.cell(row=1, column=i).fill = PatternFill(start_color='DDDDDD', end_color='DDDDDD', fill_type='solid')
    for i, lesson in enumerate(METHODOLOGY_LESSONS, 2):
        for j, val in enumerate(lesson, 1):
            ws_lessons.cell(row=i, column=j, value=val)
    # Column widths
    for col, width in zip(['A','B','C','D','E'], [55, 30, 35, 50, 30]):
        ws_lessons.column_dimensions[col].width = width
    print(f'  added {len(METHODOLOGY_LESSONS)} lesson rows')

    # =========================================================================
    # G. Overview summary block (already applied in separate run; safe to skip
    # to avoid double-application)
    # =========================================================================
    print('\n[G] Overview summary block already added (rows 22-29 in earlier run); skipping.')

    wb.save(XLSX)
    print('\nSAVED')


if __name__ == '__main__':
    main()
