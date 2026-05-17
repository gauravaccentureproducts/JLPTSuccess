"""Cross-Artifact Synchronization Report (Rule 5, 2026-05-17).

Emits the structured report described by the cross-artifact sync
protocol — a snapshot of each of the 9 artifact classes plus the
INV-1..INV-10 invariant check, mapping each invariant to its JA-NN
hard-CI counterpart (or to its current convention-only / partial
status).

Usage:
    python tools/cross_artifact_sync_report.py
    python tools/cross_artifact_sync_report.py --verbose
    python tools/cross_artifact_sync_report.py --json

Exit code:
    0 — all wired invariants pass
    1 — any wired invariant fails (drift detected)

This is a thin wrapper around tools/check_content_integrity.py that
rolls up the cross-artifact view. For the per-JA detail, run
check_content_integrity.py directly. For the human-readable artifact
map + INV→JA matrix, see N5/docs/cross-artifact-sync-map.md.
"""
from __future__ import annotations

import argparse
import io
import json
import subprocess
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent  # N5/
REPO_ROOT = ROOT.parent  # JLPTSuccess/


# The 9 artifact classes mapped to representative file globs. Used by
# the report to count and verify the artifact's presence on disk.
ARTIFACT_CLASSES = [
    ("1. Specifications", [
        "specifications/JLPT-N5-Current-Implementation-Spec.md",
        "specifications/test-scenarios-by-specialist-perspective.xlsx",
        "docs/N5-syllabus-methodology.md",
        "docs/RECOMMENDER-RULES.md",
        "docs/UNIFIED-REVIEW-QUEUE-DESIGN.md",
    ]),
    ("2. Code", [
        "js/*.js",
        "tools/*.py",
        "sw.js",
        "css/*.css",
        "playwright.config.js",
        "package.json",
    ]),
    ("3. Data / content", [
        "data/*.json",
        "data/papers/manifest.json",
        "locales/*.json",
        "external-data/*",
    ]),
    ("4. UI", [
        "index.html",
        "learn/grammar/*/index.html",
        "learn/vocab/*/index.html",
        "kanji/*/index.html",
        "reading/*/index.html",
        "listening/*/index.html",
        "manifest.webmanifest",
        "sitemap.xml",
        "robots.txt",
    ]),
    ("5. Bug tracker", [
        "specifications/test-scenarios-by-specialist-perspective.xlsx",
        "feedback/n5-audit-2026-05-04.xlsx",
    ]),
    ("6. Test scenarios", [
        "specifications/test-scenarios-by-specialist-perspective.xlsx",
        "tools/check_content_integrity.py",
        "feedback/ui-testing-plan.md",
    ]),
    ("7. Prompts", [
        "prompts/Japanese language Accuracy check.txt",
        "prompts/N5Improvement.txt",
    ]),
    ("8. Procedure manuals", [
        "../JLPT Common/procedure-manual-build-next-jlpt-level.md",
        "docs/NATIVE-AUDIO-WORKFLOW.md",
        "docs/RECORDING-BRIEF.md",
        "docs/REVIEWER-PACK.ja.md",
        "docs/SELF-HOST.md",
        "SELFHOST.md",
    ]),
    ("9. User-facing docs", [
        "README.md",
        "README.hi.md",
        "CHANGELOG.md",
        "PRIVACY.md",
        "NOTICES.md",
        "CONTENT-LICENSE.md",
        "AUDIO.md",
        "TASKS.md",
        "docs/AUDIT-COVERAGE-*.md",
        "docs/PROJECT-OVERVIEW.ja.md",
        "docs/TRANSLATING.md",
    ]),
]


# INV-N → JA-NN mapping. Status one of {wired, partial, convention, oos}.
INV_MAPPING = [
    ("INV-1",  "Bug-fix commit touches test or annotates 'no test'", "convention", []),
    ("INV-2",  "Spec change references corresponding code change", "convention", []),
    ("INV-3",  "Code public-API change updates API docs", "oos", []),
    ("INV-4",  "Data-file count changes update version.json AND CHANGELOG", "wired", ["JA-107", "JA-47"]),
    ("INV-5",  "UI string change propagates to all locales", "wired", ["JA-108"]),
    ("INV-6",  "Prompt change includes regression test of golden output", "convention", []),
    ("INV-7",  "Cross-file references resolve", "partial", ["JA-15", "JA-17", "JA-82", "JA-100", "JA-105"]),
    ("INV-8",  "CHANGELOG entry names every dependent updated", "convention", []),
    ("INV-9",  "Closed bug links to fix commit + regression test", "partial", ["spec §25.8"]),
    ("INV-10", "Procedure-manual script/tool references resolve", "wired", ["JA-109"]),
]


def count_files(patterns: list[str]) -> tuple[int, list[str]]:
    """Return (total_count, missing_patterns) for a list of glob patterns."""
    total = 0
    missing: list[str] = []
    for pat in patterns:
        if pat.startswith("../"):
            base = REPO_ROOT
            rel = pat[3:]
        else:
            base = ROOT
            rel = pat
        matched = list(base.glob(rel))
        if not matched and "*" not in rel and "?" not in rel and "[" not in rel:
            # Literal path that doesn't exist.
            missing.append(pat)
        else:
            total += len(matched)
    return total, missing


def run_ci_check() -> tuple[int, str]:
    """Run tools/check_content_integrity.py and return (exit_code, full_stdout)."""
    try:
        result = subprocess.run(
            [sys.executable, "tools/check_content_integrity.py"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=300,
        )
    except subprocess.TimeoutExpired:
        return 124, "check_content_integrity.py timed out after 300s"
    except Exception as e:
        return 1, f"failed to run check_content_integrity.py: {e}"
    out = (result.stdout or "") + (result.stderr or "")
    return result.returncode, out


def emit_text_report(verbose: bool) -> int:
    print("=" * 72)
    print("Cross-Artifact Synchronization Report (Rule 5, 2026-05-17)")
    print("Generated by: tools/cross_artifact_sync_report.py")
    print("=" * 72)
    print()

    # Artifact-class inventory
    print("ARTIFACT CLASSES (file presence inventory)")
    print("-" * 72)
    for name, patterns in ARTIFACT_CLASSES:
        total, missing = count_files(patterns)
        status = "OK" if not missing else f"MISSING {len(missing)}"
        print(f"  {name:<32} files={total:<5} {status}")
        if missing and verbose:
            for m in missing:
                print(f"      -> missing literal path: {m}")
    print()

    # CI / invariant check
    print("INTEGRITY CHECK")
    print("-" * 72)
    ci_exit, ci_out = run_ci_check()
    summary_line = ""
    for line in ci_out.splitlines():
        if line.startswith("PASS:") or line.startswith("FAIL:"):
            summary_line = line.strip()
            break
    if not summary_line:
        summary_line = "(no PASS/FAIL summary line in check output)"
    print(f"  CI summary: {summary_line}")
    if verbose or ci_exit != 0:
        print()
        print("  Full output:")
        for line in ci_out.splitlines():
            print(f"    {line}")
    print()

    # INV-N invariant matrix
    print("PROTOCOL INVARIANTS (INV-1..INV-10 status)")
    print("-" * 72)
    wired = partial = convention = oos = 0
    for inv, desc, status, jas in INV_MAPPING:
        label = ", ".join(jas) if jas else "—"
        print(f"  {inv:<8} {status:<11} {desc}")
        print(f"           via: {label}")
        if status == "wired":
            wired += 1
        elif status == "partial":
            partial += 1
        elif status == "convention":
            convention += 1
        elif status == "oos":
            oos += 1
    print()
    print(f"  Wired (hard CI): {wired}    Partial: {partial}    "
          f"Convention only: {convention}    Out of scope: {oos}")
    print()

    print("=" * 72)
    if ci_exit == 0:
        print("EXIT: CLEAN — all wired invariants green; no drift detected.")
    else:
        print(f"EXIT: DRIFT DETECTED — check_content_integrity.py exited {ci_exit}.")
        print("       Fix the failing invariant before considering the change complete.")
    print()
    print("See N5/docs/cross-artifact-sync-map.md for the dependency")
    print("matrix and per-class commit-time checklist.")
    print("=" * 72)
    return ci_exit


def emit_json_report() -> int:
    """JSON output for tooling consumption."""
    artifact_inventory = []
    for name, patterns in ARTIFACT_CLASSES:
        total, missing = count_files(patterns)
        artifact_inventory.append({
            "class": name,
            "file_count": total,
            "missing_literal_paths": missing,
        })

    ci_exit, ci_out = run_ci_check()
    summary_line = ""
    for line in ci_out.splitlines():
        if line.startswith("PASS:") or line.startswith("FAIL:"):
            summary_line = line.strip()
            break

    inv_status = []
    for inv, desc, status, jas in INV_MAPPING:
        inv_status.append({
            "invariant": inv,
            "description": desc,
            "status": status,
            "via": jas,
        })

    payload = {
        "report_version": "1.0",
        "generator": "tools/cross_artifact_sync_report.py",
        "artifact_inventory": artifact_inventory,
        "ci": {
            "exit_code": ci_exit,
            "summary": summary_line,
        },
        "invariants": inv_status,
        "exit": "CLEAN" if ci_exit == 0 else "DRIFT",
    }
    print(json.dumps(payload, indent=2, ensure_ascii=False))
    return ci_exit


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--verbose", "-v", action="store_true",
                   help="Show full CI output and missing-path detail.")
    p.add_argument("--json", action="store_true",
                   help="Emit machine-readable JSON report.")
    args = p.parse_args(argv)

    if args.json:
        return emit_json_report()
    return emit_text_report(args.verbose)


if __name__ == "__main__":
    sys.exit(main())
