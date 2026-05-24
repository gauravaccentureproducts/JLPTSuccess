"""Append the 9 bugs surfaced + fixed in the 2026-05-24 session to the
User Reported Bugs sheet of the canonical bug tracker.

Schema (row 3 headers):
  col 1: Bug ID (often blank; BUG-NNN id is embedded in col 4 Title)
  col 2: Date Reported
  col 3: Reported By
  col 4: Title (with BUG-NNN prefix)
  col 5: Description
  col 6: Severity
  col 7: Priority
  col 8: Status
  col 9: Fix Commit
  col 10: Fix Date
"""
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment
from pathlib import Path

XLSX = Path(r"specifications/test-scenarios-by-specialist-perspective.xlsx")

ENTRIES = [
    # Grammar v4 test-review batch (commit 4fb081e)
    {
        "date": "2026-05-24",
        "reporter": "JLPT-expert grammar audit (v4 test-scenario review session, 2026-05-24)",
        "title": "BUG-019 — Class D arrow notation in 7 common_mistakes wrong/right cells (n5-021, n5-030, n5-048, n5-050, n5-067, n5-069, n5-112)",
        "description": "The `wrong` (and sometimes `right`) field in 7 common_mistakes rows contained an in-cell ASCII arrow '→' joining a right-sentence to a wrong fragment, breaking the single-sentence wrong/right contract. Example (n5-021 cm[1]): wrong='9時から 5時まで しごとです。 → 9時で 5時まで'. Diagnostic transformations should live in the `why` field; wrong/right cells must be clean sentences. Fixed via tools/fix_class_d_arrow_cells_2026_05_24.py — extracted the true learner mistake into a clean wrong sentence.",
        "severity": "Medium",
        "priority": "P3",
        "status": "Fixed",
        "fix_commit": "4fb081e",
        "fix_date": "2026-05-24",
    },
    {
        "date": "2026-05-24",
        "reporter": "JLPT-expert grammar audit (v4 test-scenario review session, 2026-05-24)",
        "title": "BUG-020 — Class E English parenthetical context in wrong-field (154 rows across common_mistakes + wrong_corrected_pair)",
        "description": "wrong-field carried a JA sentence followed by an English parenthetical context annotation, e.g. n5-010 cm[0] wrong='5時から しごとです。 (when meaning until 5)'. The JA sentence alone is grammatically valid — the parenthetical is essential teaching context but structurally awkward inside the wrong field. Fixed via tools/fix_class_e_paren_context_2026_05_24.py — parenthetical moved to the `why` field as 'Context: ...' prefix. Touched 154 rows; register_variant entries skipped (different schema).",
        "severity": "Low",
        "priority": "P4",
        "status": "Fixed",
        "fix_commit": "4fb081e",
        "fix_date": "2026-05-24",
    },
    {
        "date": "2026-05-24",
        "reporter": "JLPT-expert grammar audit (v4 test-scenario review session, 2026-05-24)",
        "title": "BUG-021 — n5-098 (〜の中で〜が いちばん) audio paths empty in grammar.json despite all 10 MP3s existing on disk",
        "description": "All 10 examples in n5-098 had `audio: ''` in grammar.json. The MP3 files audio/grammar/n5-098.0..9.mp3 existed on disk but were not wired into the data. Affected: the entire superlative-pattern page had no audio playback. Fixed via tools/fix_remaining_grammar_bugs_2026_05_24.py — populated audio paths from the on-disk files.",
        "severity": "Medium",
        "priority": "P3",
        "status": "Fixed",
        "fix_commit": "4fb081e",
        "fix_date": "2026-05-24",
    },
    {
        "date": "2026-05-24",
        "reporter": "JLPT-expert grammar audit (v4 test-scenario review session, 2026-05-24)",
        "title": "BUG-022 — n5-011 (や) and n5-024 (か alternatives) particle-swap rows labelled valid Japanese as wrong (Class C)",
        "description": "n5-011 cm[2] labelled 'りんごと バナナを たべます' as wrong vs 'りんごや バナナを' — but both are valid (exhaustive vs non-exhaustive listing); the difference is meaning, not grammar. Same issue at n5-024 cm[1] (と vs か). Conflated meaning-choice with grammatical error. Fixed via tools/fix_remaining_grammar_bugs_2026_05_24.py — rows replaced with genuine learner mistakes (missing listing/alternative particle entirely).",
        "severity": "Medium",
        "priority": "P3",
        "status": "Fixed",
        "fix_commit": "4fb081e",
        "fix_date": "2026-05-24",
    },
    {
        "date": "2026-05-24",
        "reporter": "Internal — test-scenario tooling false-positive surfaced during v4 review session",
        "title": "BUG-023 — TS-03 auto-check false-positive on register_variant entries (catalogued as FP-16)",
        "description": "tools/grammar_auto_checks.py flagged 38 patterns as 'TS-03 Fail: empty wrong/right' when in fact those rows were `kind: register_variant` entries with a different schema (form_a/form_b/label_a/label_b — both forms valid). Auto-check tooling must short-circuit on kind=='register_variant' before reading wrong/right. Catalogued as FP-16 in prompts/Japanese language Accuracy check.txt. Test logic corrected in grammar_auto_checks.py + grammar_horizontal_checks.py + export_grammar_for_review.py + fix_class_e_paren_context_2026_05_24.py.",
        "severity": "Low",
        "priority": "P4",
        "status": "Fixed",
        "fix_commit": "4fb081e",
        "fix_date": "2026-05-24",
    },

    # Routing migration + follow-ups
    {
        "date": "2026-05-24",
        "reporter": "User-reported (ClaudeChat external-fetch request 2026-05-24) — SPA hash routing made /learn/n5-066 return 404",
        "title": "BUG-024 — SPA used hash routing (#/learn/n5-001); deep links to clean paths 404'd and corpus had two URLs per pattern (SPA hash + static mirror at learn/grammar/<id>/)",
        "description": "Architectural issue. SPA used location.hash for routing (legacy GitHub Pages pattern). Deep links like /JLPTSuccess/N5/learn/n5-066 returned 404. Static mirrors lived at learn/grammar/<id>/ and JS-redirected to the SPA hash URL after 1.5s. Two URLs per pattern (wasteful); LLMs/crawlers couldn't fetch content without knowing the mirror path. Fixed via full history-mode migration: parseRoute() reads pathname; in-app nav uses pushState; 178 mirrors moved to learn/<id>/; mirrors boot SPA in place; 404.html with rafgraph snippet for non-mirror routes; SW CACHE_VERSION bumped.",
        "severity": "High",
        "priority": "P2",
        "status": "Fixed",
        "fix_commit": "85f8a01",
        "fix_date": "2026-05-24",
    },
    {
        "date": "2026-05-24",
        "reporter": "User-reported 2026-05-24 — audio not playing on /learn/n5-067/ after history-mode migration",
        "title": "BUG-025 — Audio not playing after history-mode migration: relative <audio src> resolves against deep mirror path (404)",
        "description": "Regression of BUG-024 fix. The base-aware fetch wrapper in router.js covers fetch() calls but NOT HTML attribute resolution. <audio src='audio/grammar/n5-067.0.mp3'> from a page at /learn/n5-067/ resolves to /learn/n5-067/audio/grammar/n5-067.0.mp3 → 404. Same bug class affected 4 SPA modules: learn-grammar.js, listening.js, listening-story.js, reading.js. Fixed by adding assetUrl(path) helper in router.js + wrapping every <audio src> injection through assetUrl() so the URL is base-anchored regardless of the booting page's depth.",
        "severity": "High",
        "priority": "P1",
        "status": "Fixed",
        "fix_commit": "52d8a9d",
        "fix_date": "2026-05-24",
    },
    {
        "date": "2026-05-24",
        "reporter": "User-reported 2026-05-24 — 'formatting gone for a toss' after audio src fix",
        "title": "BUG-026 — Static mirrors didn't link main.min.css → SPA-rendered content unstyled (audio controls + pattern-nav rendered as plain buttons in a row)",
        "description": "Regression of BUG-024 fix. When the SPA boots from a static mirror and replaces #app, the rendered content uses SPA-specific CSS class names (.audio-skin-*, .example-audio, .pattern-nav-*, etc.) that live in css/main.min.css. The mirrors had only their own inline <style> block — so audio controls rendered as plain unstyled buttons in a row. Fixed by adding <link rel='stylesheet' href='../../css/main.min.css'> to each of 178 mirror heads via tools/add_main_css_to_mirrors_2026_05_24.py (idempotent).",
        "severity": "Medium",
        "priority": "P2",
        "status": "Fixed",
        "fix_commit": "52d8a9d",
        "fix_date": "2026-05-24",
    },
    {
        "date": "2026-05-24",
        "reporter": "User-reported 2026-05-24 — 'even the audio is still not playing' after audio + CSS fix landed",
        "title": "BUG-027 — SPA cache-buster ?v=1.16.9 not bumped after audio fix → browsers serving stale cached app.js",
        "description": "Follow-on to BUG-025 fix. The <script src='...app.js?v=1.16.9'> tag in index.html + all 178 mirrors still referenced the old cache-buster, so browsers (and the service worker on old CACHE_VERSION) kept serving the previously-cached app.js even though server had the fix. Fixed by bumping every app.js?v=... tag to ?v=1.17.0 (matching sw.js CACHE_VERSION). Scripted via tools/bump_spa_cache_buster_2026_05_24.py.",
        "severity": "Medium",
        "priority": "P2",
        "status": "Fixed",
        "fix_commit": "9cc58e2",
        "fix_date": "2026-05-24",
    },
]


def main():
    wb = load_workbook(str(XLSX))
    ws = wb["User Reported Bugs"]
    start_row = ws.max_row + 1
    print(f"Appending {len(ENTRIES)} entries starting at row {start_row}")

    wrap = Alignment(wrap_text=True, vertical="top")

    for i, e in enumerate(ENTRIES):
        r = start_row + i
        ws.cell(row=r, column=2, value=e["date"]).alignment = wrap
        ws.cell(row=r, column=3, value=e["reporter"]).alignment = wrap
        ws.cell(row=r, column=4, value=e["title"]).alignment = wrap
        ws.cell(row=r, column=5, value=e["description"]).alignment = wrap
        ws.cell(row=r, column=6, value=e["severity"]).alignment = wrap
        ws.cell(row=r, column=7, value=e["priority"]).alignment = wrap
        ws.cell(row=r, column=8, value=e["status"]).alignment = wrap
        ws.cell(row=r, column=9, value=e["fix_commit"]).alignment = wrap
        ws.cell(row=r, column=10, value=e["fix_date"]).alignment = wrap

    wb.save(str(XLSX))
    print(f"OK wrote {len(ENTRIES)} new bug entries to {XLSX}")
    print(f"  Last row is now {ws.max_row}")


if __name__ == "__main__":
    main()
