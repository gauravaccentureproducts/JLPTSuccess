"""NTR-FU-003 fix v2: rename `collocations` → `particle_examples`
corpus-wide.

Reverses approach from v1 (provenance-only labeling). User's review
explicitly says: "Rename `particle_examples` or replace where
genuine collocations exist." NTR-011 renamed 12 pronouns; broader
corpus (983 remaining) still uses `collocations`. The current state
also caused a silent UI regression on the 12 pronouns (UI reads
`entry.collocations`, doesn't see the renamed `particle_examples`).

Operations per entry:
  - rename `collocations` → `particle_examples` (carry value)
  - rename `collocations_provenance` → `particle_examples_provenance`
  - if neither rename target exists, no-op
  - if BOTH old + new exist (the 12 pronouns), drop old, keep new

Companion UI updates land in same commit:
  - js/learn-vocab.js reads `entry.particle_examples` with fallback
    to `entry.collocations` for safety during rolling deploys
  - js/min/learn-vocab.js rebuilt via tools/build_min_js.py
  - locales/{en,hi}.json: `vocab_detail.collocations` → `.particle_examples`
  - index.html ?v= cache-bust bumped to v1.16.2
"""
import sys, io, os, json, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_23"


def main():
    fp = os.path.join(REPO_N5, "data", "vocab.json")
    bak = fp + f".bak_{TODAY}_ntr_fu_003_rename"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        v = json.load(f)
    vl = v if isinstance(v, list) else v.get("vocab", v.get("entries", []))
    renamed = 0
    already_renamed = 0
    both_existed = 0
    for entry in vl:
        if not isinstance(entry, dict): continue
        has_old = "collocations" in entry
        has_new = "particle_examples" in entry
        if has_new and not has_old:
            already_renamed += 1
            continue
        if has_old and has_new:
            # The 12 pronouns from NTR-011: drop old, keep new
            entry.pop("collocations", None)
            entry.pop("collocations_provenance", None)
            both_existed += 1
            continue
        if has_old:
            entry["particle_examples"] = entry.pop("collocations")
            if "collocations_provenance" in entry:
                entry["particle_examples_provenance"] = entry.pop("collocations_provenance")
            else:
                entry["particle_examples_provenance"] = "template_substitution_2026_05_23"
            renamed += 1
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)
    print(f"Newly renamed (collocations → particle_examples): {renamed}")
    print(f"Already-renamed (NTR-011 pronouns): {already_renamed}")
    print(f"Had both fields (dropped old, kept new): {both_existed}")
    print()
    # Verify
    still_old = sum(1 for e in vl if isinstance(e, dict) and "collocations" in e)
    has_new = sum(1 for e in vl if isinstance(e, dict) and "particle_examples" in e)
    print(f"After: collocations field still present in {still_old} entries")
    print(f"After: particle_examples field present in {has_new} entries")
    print()
    print(f"=== NTR-FU-003 rename applied: {renamed + both_existed + already_renamed} entries unified ===")


if __name__ == "__main__":
    main()
