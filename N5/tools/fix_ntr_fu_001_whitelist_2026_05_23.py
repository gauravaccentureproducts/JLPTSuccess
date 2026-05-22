"""NTR-FU-001 fix: add 11 missing entries to n5_vocab_whitelist.json
so vocab forms (or readings) are a subset of the whitelist.

The 11 entries are:
  おはし / こくせき / だんだん / どきどき / にこにこ / ばい /
  ぴかぴか / ぺこぺこ / まあまあ / わくわく / ビル

After this fix:
  - Forward direction (JA-147): 4 whitelist tokens without vocab
    (倍/国籍/週末/では) remain documented Known mismatches.
  - Reverse direction (NEW JA-151): all vocab forms (and their
    readings) are in the whitelist; 0 mismatches.
"""
import sys, io, os, json, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_23"

ADD = [
    "おはし", "こくせき", "だんだん", "どきどき", "にこにこ",
    "ばい", "ぴかぴか", "ぺこぺこ", "まあまあ", "わくわく", "ビル",
]


def main():
    fp = os.path.join(REPO_N5, "data", "n5_vocab_whitelist.json")
    bak = fp + f".bak_{TODAY}_ntr_fu_001"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        wl = json.load(f)
    existing = set(wl if isinstance(wl, list) else wl.get("vocab", []))
    print(f"Whitelist before: {len(existing)} entries")
    added = []
    for t in ADD:
        if t not in existing:
            existing.add(t)
            added.append(t)
    new_wl = sorted(existing)
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(new_wl, f, ensure_ascii=False, indent=2)
    print(f"Whitelist after: {len(new_wl)} entries")
    print(f"Added: {added}")
    print(f"=== NTR-FU-001 fix applied: +{len(added)} entries ===")


if __name__ == "__main__":
    main()
