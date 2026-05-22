"""
fix_docs_vocab_005_2026_05_22.py
=================================

Closes DOCS-VOCAB-005 (BUG-136) — addresses the unaddressed half of
DOCS-VOCAB-003 which had marked itself Fixed without actually touching
the 28 paper-file source_file fields.

Replaces the verbose prose annotation:
  "(authored in-place; was KnowledgeBank/<x>_questions_n5.md before
   KnowledgeBank/ merge into data/ + docs/N5-syllabus-methodology.md
   on 2026-05-14)"

with the trimmed canonical sentinel:
  "(authored in-place)"

Why trim and not point at a methodology-doc anchor:
  - The questions ARE authored in-place; there is no upstream source file.
  - The methodology doc has no #bunpou-questions etc. anchors anyway.
  - Pointing source_file at a methodology doc would falsely imply that
    doc contains the questions.
  - Historical KB breadcrumb is preserved in CHANGELOG + git history +
    n5_vocab_whitelist_README.md — doesn't need to live in 28 places.

Bumps version.json patch v1.15.5 → v1.15.6 (data change to source_file
field across 28 paper files).
"""
import sys, io, json, os, shutil, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_22"
SENTINEL = "(authored in-place)"


def backup(fp):
    bak = fp + f".bak_{TODAY}_docs_vocab_005"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)


def main():
    stats = {"files touched": 0, "fields trimmed": 0}
    for fp in sorted(glob.glob(os.path.join(REPO_N5, "data", "papers", "*", "paper-*.json"))):
        with open(fp, "r", encoding="utf-8") as f:
            d = json.load(f)
        before = d.get("source_file")
        if not isinstance(before, str):
            continue
        if before == SENTINEL:
            continue  # idempotent
        if "authored in-place" not in before:
            # Defensive: only trim known prose; if something else lives there, skip
            print(f"  SKIP {os.path.basename(fp)}: source_file is not the expected prose: {before[:60]!r}")
            continue
        d["source_file"] = SENTINEL
        backup(fp)
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
        stats["files touched"] += 1
        stats["fields trimmed"] += 1
        rel = os.path.relpath(fp, REPO_N5).replace("\\", "/")
        print(f"  Trimmed {rel}: source_file → {SENTINEL!r}")

    # Bump version.json
    vfp = os.path.join(REPO_N5, "data", "version.json")
    with open(vfp, "r", encoding="utf-8") as f:
        v = json.load(f)
    before_ver = v.get("version")
    if before_ver == "v1.15.5":
        v["version"] = "v1.15.6"
        v["cacheVersion"] = "jlptsuccess-n5-v1.15.6"
        v["builtAt"] = "2026-05-22T00:00:00Z"
        backup(vfp)
        with open(vfp, "w", encoding="utf-8") as f:
            json.dump(v, f, ensure_ascii=False, indent=2)
        print(f"  Bumped version.json: {before_ver} → v1.15.6")
    else:
        print(f"  SKIP version bump: current version is {before_ver!r}, expected 'v1.15.5'")

    print()
    print("=== Stats ===")
    for k, val in stats.items():
        print(f"  {k}: {val}")


if __name__ == "__main__":
    main()
