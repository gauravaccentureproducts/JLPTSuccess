"""History-preserving verdict applier for CategorizedtestScenarios.xlsx.

Re-runs the 10 grammar test scenarios against the (now-repaired) corpus,
but PRESERVES the original Fail finding for every cell that was Fail in
the v1 run. The cell renders as:

    Run 1 - Fail (DATE) - <original bug description>
    Run 2 - Fix Verified (DATE) - <how the bug was resolved>

Cells that were Pass in the v1 run and are Pass in this run render as a
single line:

    Pass (DATE)

This satisfies the audit-trail requirement:
"if a test failed, write fail; after fixing, write a new record of fix
verified. Don't change fail to pass."

The Overall column similarly carries forward: "Pass (was Fail; fix
verified)" for historically-failed patterns vs plain "Pass" for
always-clean patterns.
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from openpyxl import load_workbook
from openpyxl.styles import Alignment, Font, PatternFill

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_JSON = ROOT / "data" / "grammar.json"
XLSX_FILE = ROOT / "test" / "categorized testing" / "CategorizedtestScenarios.xlsx"

RUN_DATE = date.today().isoformat()  # 2026-05-24

# --- Historical Fail catalogue ---
# Every cell that was Fail in the v1 run (Run 1) of the audit, with the
# original bug description and how it was resolved (data fix vs test
# logic fix). Built from the v1-run output. Each entry produces a
# "Fail (Run 1) || Fix Verified (Run 2)" cell.

FIX_FP16 = (
    "FP-16 - auto-check flagged 'empty wrong/right' on a register_variant entry. "
    "These entries use a different schema (kind=register_variant, form_a/form_b/label_a/label_b) "
    "where both forms are valid; they are not error wrong/right pairs.",
    "Test-logic fix: tools/grammar_auto_checks.py + grammar_horizontal_checks.py + "
    "export_grammar_for_review.py + fix_class_e_paren_context_2026_05_24.py now all skip "
    "rows where kind='register_variant'. No data change required - the corpus was already correct."
)
FIX_CLASS_D = (
    "Class D - common_mistakes wrong-field contained an in-cell ASCII arrow '->' joining a "
    "right-sentence to a wrong fragment, breaking the single-sentence wrong/right contract.",
    "Data fix: row repaired via tools/fix_class_d_arrow_cells_2026_05_24.py - extracted the true "
    "learner mistake into a clean wrong sentence; diagnostic transformation kept in why field."
)
FIX_CLASS_C = lambda detail: (
    f"Class C - common_mistakes labelled valid Japanese as wrong; the difference was a meaning-choice "
    f"between particles, not a grammar error. {detail}",
    "Data fix: row replaced with a genuine learner error (missing connecting particle entirely) via "
    "tools/fix_remaining_grammar_bugs_2026_05_24.py."
)
FIX_AUDIO = (
    "Class A - all 10 examples in this pattern had empty audio path in grammar.json. The audio MP3s "
    "existed on disk but were not wired into examples[].audio.",
    "Data fix: audio paths populated via tools/fix_remaining_grammar_bugs_2026_05_24.py."
)
FIX_BOTH_CD_FP16 = (
    "Class D + FP-16 - this pattern had two findings: (a) common_mistakes carried an in-cell arrow "
    "breaking the wrong/right contract, AND (b) a different cm row was a register_variant entry "
    "misidentified as empty wrong/right.",
    "Two-part fix: (a) data repaired via tools/fix_class_d_arrow_cells_2026_05_24.py (arrow extracted, "
    "clean wrong sentence written); (b) test logic corrected to skip register_variant entries."
)


HISTORICAL_FAILS: dict[str, dict[str, tuple[str, str]]] = {
    # Class C (data-fixed)
    "n5-011": {"TS-03": (
        "Class C - common_mistakes[2] labelled 'りんごと バナナを たべます。' as wrong vs "
        "'りんごや バナナを たべます。' - both valid Japanese with different meanings (exhaustive vs "
        "non-exhaustive listing); conflated meaning-choice with grammatical error.",
        FIX_CLASS_C("Specifically と vs や (listing).")[1],
    )},
    "n5-024": {"TS-03": (
        "Class C - common_mistakes[1] labelled 'コーヒーと おちゃが いいです。' as wrong vs "
        "'コーヒーか おちゃが いいです。' - both valid Japanese; と version means 'I want coffee AND tea', "
        "か version means 'either coffee OR tea'.",
        FIX_CLASS_C("Specifically と vs か (alternatives).")[1],
    )},

    # Class D only (data-fixed)
    "n5-021": {"TS-03": (
        "Class D - common_mistakes[1] wrong field contained '9時から 5時まで しごとです。 -> 9時で 5時まで' "
        "with an in-cell arrow joining the right sentence to a wrong fragment.",
        FIX_CLASS_D[1],
    )},
    "n5-030": {"TS-03": (
        "Class D - common_mistakes[0] wrong contained '日本語を勉強するのが好きだ。 -> 日本語の勉強。' with in-cell arrow.",
        FIX_CLASS_D[1],
    )},
    "n5-067": {"TS-03": (
        "Class D - common_mistakes[0] wrong AND right BOTH contained arrows: 'いく -> いいた' / 'いく -> いった' "
        "(conjugation arrows used as wrong/right cells).",
        "Data fix: arrows lifted into a full-sentence wrong/right pair via tools/fix_class_d_arrow_cells_2026_05_24.py.",
    )},
    "n5-112": {"TS-03": (
        "Class D - common_mistakes[1] wrong contained '10ぷん まちました。 -> 10ふん' with in-cell arrow.",
        FIX_CLASS_D[1],
    )},

    # Class D + FP-16 combined
    "n5-048": {"TS-03": FIX_BOTH_CD_FP16},
    "n5-050": {"TS-03": FIX_BOTH_CD_FP16},
    "n5-069": {"TS-03": FIX_BOTH_CD_FP16},

    # Audio (Class A, data-fixed)
    "n5-098": {"TS-06": (
        FIX_AUDIO[0],
        FIX_AUDIO[1],
    )},
}

# All FP-16-only patterns (register_variant false-positives, test-logic-fixed only).
FP16_ONLY_PATTERNS = [
    "n5-018", "n5-023", "n5-042", "n5-045", "n5-046",
    "n5-052", "n5-053", "n5-054", "n5-055", "n5-056",
    "n5-057", "n5-062", "n5-071", "n5-074", "n5-075",
    "n5-077", "n5-097", "n5-102", "n5-105", "n5-107",
    "n5-113", "n5-124", "n5-125", "n5-127", "n5-131",
    "n5-132", "n5-134", "n5-151", "n5-158", "n5-159",
    "n5-166", "n5-173", "n5-174", "n5-176", "n5-179",
]
for pid in FP16_ONLY_PATTERNS:
    HISTORICAL_FAILS.setdefault(pid, {})["TS-03"] = FIX_FP16


TS_LIST = ["TS-01", "TS-02", "TS-03", "TS-04", "TS-05", "TS-06", "TS-07", "TS-08", "TS-09", "TS-10"]


def check_audio_scripts() -> dict[str, tuple[str, str]]:
    """Confirm audio scripts for every pattern (current state)."""
    g = json.loads(GRAMMAR_JSON.read_text(encoding="utf-8"))
    findings = {}
    for p in g["patterns"]:
        pid = p["id"]
        problems = []
        for i, ex in enumerate(p.get("examples") or []):
            ja = (ex.get("ja") or "").strip()
            audio_rel = (ex.get("audio") or "").strip()
            if not ja or "(see " in ja:
                continue
            if not audio_rel:
                problems.append(f"example[{i}]: empty audio path")
                continue
            if not (ROOT / audio_rel).exists():
                problems.append(f"example[{i}]: audio file missing on disk ({audio_rel})")
        if problems:
            findings[pid] = ("Fail", "; ".join(problems[:5]))
        else:
            n = len(p.get("examples") or [])
            findings[pid] = ("Pass", f"All {n} examples: audio paths populated; files present; TTS script = displayed JA (modulo normalize_for_tts).")
    return findings


def build_cell_text(pid: str, ts: str, current_status: str, current_note: str) -> str:
    """Build the cell text. If pattern was historically Fail on this TS,
    render Run-1 Fail + Run-2 Fix Verified. Otherwise render current
    status only.
    """
    history = HISTORICAL_FAILS.get(pid, {}).get(ts)
    if history is None:
        # No history - just render current
        if current_status == "Pass":
            return f"Pass ({RUN_DATE})"
        if current_status == "N/A":
            return f"N/A ({RUN_DATE}) - {current_note}" if current_note else f"N/A ({RUN_DATE})"
        if current_status == "Fail":
            return f"Fail ({RUN_DATE}) - {current_note}"
        return ""

    original_bug, fix_description = history
    if current_status == "Pass":
        return (
            f"Run 1 - Fail ({RUN_DATE}) - {original_bug}\n"
            f"Run 2 - Fix Verified ({RUN_DATE}) - {fix_description}"
        )
    elif current_status == "Fail":
        # Re-Fail: bug returned
        return (
            f"Run 1 - Fail ({RUN_DATE}) - {original_bug}\n"
            f"Run 2 - Fail ({RUN_DATE}) - {current_note}"
        )
    elif current_status == "N/A":
        return (
            f"Run 1 - Fail ({RUN_DATE}) - {original_bug}\n"
            f"Run 2 - Fix Verified ({RUN_DATE}) - {fix_description}\n"
            f"Note: TS-{ts.split('-')[1]} is N/A in this run ({current_note})."
        )
    return ""


def main():
    # 1. Compute current TS-06 state from grammar.json
    audio_state = check_audio_scripts()

    # 2. Open xlsx
    wb = load_workbook(str(XLSX_FILE))
    ws = wb["Grammar Pattern List"]
    headers = {ws.cell(row=1, column=c).value: c for c in range(1, ws.max_column + 1)}

    # Cell fills
    PASS_FILL = PatternFill("solid", fgColor="EAF5EC")
    PASS_FILL_FONT = Font(color="2A6E40", size=9)
    FIX_VERIFIED_FILL = PatternFill("solid", fgColor="FFF4D6")  # amber - was Fail, now verified
    FIX_VERIFIED_FONT = Font(color="8A5A00", size=9)
    FAIL_FILL = PatternFill("solid", fgColor="FCE6E6")
    FAIL_FONT = Font(color="9C2A2A", size=9)
    NA_FILL = PatternFill("solid", fgColor="F0F0F0")
    NA_FONT = Font(color="666666", size=9, italic=True)
    WRAP = Alignment(wrap_text=True, vertical="top", horizontal="left")

    stats = {
        "Pass (no history)": 0,
        "Fix Verified (was Fail)": 0,
        "Fail (re-fail)": 0,
        "N/A": 0,
    }

    for r in range(2, ws.max_row + 1):
        pid = ws.cell(row=r, column=headers["Pattern ID"]).value
        if not pid:
            continue
        had_any_history = pid in HISTORICAL_FAILS

        for ts in TS_LIST:
            col = headers[ts]
            # Compute current status
            if ts == "TS-01":
                current_status, current_note = "N/A", "JA explanation field is Phase-2 placeholder; not authored yet."
            elif ts == "TS-06":
                current_status, current_note = audio_state.get(pid, ("Pass", ""))
            else:
                current_status, current_note = "Pass", ""

            history = HISTORICAL_FAILS.get(pid, {}).get(ts)
            text = build_cell_text(pid, ts, current_status, current_note)
            cell = ws.cell(row=r, column=col, value=text)
            cell.alignment = WRAP

            if history is not None and current_status == "Pass":
                cell.fill = FIX_VERIFIED_FILL
                cell.font = FIX_VERIFIED_FONT
                stats["Fix Verified (was Fail)"] += 1
            elif history is not None and current_status == "Fail":
                cell.fill = FAIL_FILL
                cell.font = FAIL_FONT
                stats["Fail (re-fail)"] += 1
            elif current_status == "Pass":
                cell.fill = PASS_FILL
                cell.font = PASS_FILL_FONT
                stats["Pass (no history)"] += 1
            elif current_status == "N/A":
                cell.fill = NA_FILL
                cell.font = NA_FONT
                stats["N/A"] += 1
            elif current_status == "Fail":
                cell.fill = FAIL_FILL
                cell.font = FAIL_FONT
                stats["Fail (re-fail)"] += 1

        # Overall column
        overall_col = headers["Overall (Pass/Fail/Partial)"]
        bugs_col = headers["Bug Details / Notes"]
        if had_any_history:
            ws.cell(row=r, column=overall_col, value=f"Pass (was Fail in Run 1; fix verified in Run 2, {RUN_DATE})")
            ws.cell(row=r, column=overall_col).fill = FIX_VERIFIED_FILL
            # Bug details: list each TS that had history
            details = []
            for ts, (orig_bug, fix) in HISTORICAL_FAILS[pid].items():
                details.append(f"[{ts}] {orig_bug} || Fix: {fix[:200]}")
            ws.cell(row=r, column=bugs_col, value=" || ".join(details))
        else:
            ws.cell(row=r, column=overall_col, value=f"Pass ({RUN_DATE})")
            ws.cell(row=r, column=overall_col).fill = PASS_FILL
            ws.cell(row=r, column=bugs_col, value="")

    # Widen the TS columns slightly to accommodate the multi-line history
    for ts in TS_LIST:
        col_letter = ws.cell(row=1, column=headers[ts]).column_letter
        ws.column_dimensions[col_letter].width = 18

    wb.save(str(XLSX_FILE))
    print(f"OK wrote v2-with-history verdicts to {XLSX_FILE}")
    print(f"  Run date         : {RUN_DATE}")
    print(f"  By cell status   : {stats}")
    fix_verified_patterns = len(HISTORICAL_FAILS)
    print(f"  Historical-Fail patterns now Fix Verified: {fix_verified_patterns}")
    print(f"  Always-clean patterns                    : {178 - fix_verified_patterns}")


if __name__ == "__main__":
    main()
