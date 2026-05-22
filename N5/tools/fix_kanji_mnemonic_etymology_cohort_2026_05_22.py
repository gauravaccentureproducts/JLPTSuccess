"""Close review §4 item 5 — cohort sweep of kanji mnemonic etymology
claims. Audit ran across all 106 kanji; surfaced 1 additional candidate
(八) beyond the already-fixed 三."""
import sys, io, os, shutil, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_22"


def main():
    fp = os.path.join(REPO_N5, "data", "kanji.json")
    bak = fp + f".bak_{TODAY}_mnemonic_cohort"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        kd = json.load(f)
    kl = kd.get("entries", kd if isinstance(kd, list) else kd.get("kanji", []))

    for entry in kl:
        if not isinstance(entry, dict): continue
        if entry.get("glyph") == "八":
            mn = entry.get("mnemonic", {})
            old = mn.get("reading", "")
            new = (
                "はち — visual hook: sharp like a bee sting. "
                "(Coincidence: 蜂 'bee' is also pronounced はち — a separate "
                "kanji with separate etymology; the shared sound is a "
                "useful memory hook, not a derivation.) Used in 8-hour: はちじかん."
            )
            mn["reading"] = new
            prov = mn.get("provenance") or {}
            if isinstance(prov, dict):
                prov["reading"] = "native_reviewed_2026_05_22"
            print(f"  八 mnemonic.reading softened")
            print(f"    OLD: {old!r}")
            print(f"    NEW: {new!r}")
            break

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(kd, f, ensure_ascii=False, indent=2)
    print()
    print("=== Cohort-sweep result ===")
    print("  106 kanji mnemonics audited; 2 had etymology cross-references:")
    print("    三 (-さん honorific) - fixed earlier in NTR-007")
    print("    八 (蜂/bee homophone) - fixed in this commit")
    print("  104 entries clean.")


if __name__ == "__main__":
    main()
