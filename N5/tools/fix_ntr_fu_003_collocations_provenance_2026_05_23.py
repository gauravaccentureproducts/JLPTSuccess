"""NTR-FU-003 fix: stamp collocations_provenance on all entries
that hold the `collocations` field.

The `collocations` field across 983 entries is mass template-
substitution (228x "を かう", 220x "を つかう", 215x "は どこ",
etc.) — not real corpus collocations. NTR-011 renamed 12 pronoun
entries to `particle_examples`; broader corpus remains.

Per F.44.9 (field-name overclaim discipline), the honest fix is
either:
  (a) Rename to particle_examples corpus-wide — breaks UI consumers
      that reference `collocations`.
  (b) Add provenance flag honest-labeling the field semantics —
      preserves field name, preserves UI behavior, documents that
      these are template-substitution slot fills.

Choosing (b) for minimal-disruption. UI consumers can opt-in to
the rename later. The provenance flag locks honest labeling so
the field-name overclaim is documented at the data layer.
"""
import sys, io, os, json, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_23"


def main():
    fp = os.path.join(REPO_N5, "data", "vocab.json")
    bak = fp + f".bak_{TODAY}_ntr_fu_003"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        v = json.load(f)
    vl = v if isinstance(v, list) else v.get("vocab", v.get("entries", []))
    touched = 0
    skipped_already = 0
    for entry in vl:
        if not isinstance(entry, dict): continue
        c = entry.get("collocations")
        if not c: continue
        if entry.get("collocations_provenance"):
            skipped_already += 1
            continue
        entry["collocations_provenance"] = "template_substitution_2026_05_23"
        touched += 1
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)
    print(f"Stamped collocations_provenance on {touched} entries")
    print(f"Already-stamped (skipped): {skipped_already}")
    print()
    print(f"=== NTR-FU-003 fix applied: {touched} entries flagged template_substitution ===")


if __name__ == "__main__":
    main()
