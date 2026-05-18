"""
fix_reg_001_d6_migrations_2026_05_18.py
========================================

JA-127 (the REG-001 D6 invariant added in this commit) caught 5 more
wrong_corrected_pair entries with the same defect pattern as the
original REG-001 finding: error_category=register AND wrong-field
contains a self-contradicting parenthetical like "(in formal context)".

These 5 entries (n5-097, n5-102, n5-127, n5-173, n5-179) all describe
plain/casual-vs-polite contractions that ARE register variants, not
grammatical errors. Migrate to register_variant kind in common_mistakes.
"""
import sys, io, json, os, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_18"

MIGRATIONS = {
    # pid: (wcp_index, register_variant entry)
    "n5-097": (1, {
        "kind": "register_variant",
        "form_a": "A と B と、どっちが すきですか。",
        "form_b": "A と B と、どちらが すきですか。",
        "label_a": "casual / spoken — fine with friends and intimates",
        "label_b": "polite / written / formal — どちら is the polite version of どっち",
        "why": "どっち is the casual contraction of どちら. Both are grammatical; the choice is register, not correctness. Use どちら in business/formal/written contexts; どっち is fine with intimates.",
        "category": "register",
        "provenance": "native_reviewed",
        "provenance_note": "REG-001 D6 follow-up migration 2026-05-18 — moved from wrong_corrected_pair to common_mistakes register_variant. Caught by JA-127.",
        "bug_reg_001_d6_fix_2026_05_18": True,
    }),
    "n5-102": (2, {
        "kind": "register_variant",
        "form_a": "わかってる。",
        "form_b": "わかります。 / わかっています。",
        "label_a": "casual / plain spoken — contraction of わかっている",
        "label_b": "polite / formal — full polite form",
        "why": "わかってる is the casual spoken contraction of わかっている. Both express the same state; the choice is register. Use わかります/わかっています in polite contexts; わかってる among intimates.",
        "category": "register",
        "provenance": "native_reviewed",
        "provenance_note": "REG-001 D6 follow-up migration 2026-05-18 — moved from wrong_corrected_pair to common_mistakes register_variant. Caught by JA-127.",
        "bug_reg_001_d6_fix_2026_05_18": True,
    }),
    "n5-127": (0, {
        "kind": "register_variant",
        "form_a": "たかい けど、おいしい。",
        "form_b": "たかい けれど、おいしい。 / たかい です が、おいしい です。",
        "label_a": "casual / spoken — informal contraction",
        "label_b": "polite / written / formal — full form けれど or 〜です が",
        "why": "けど is the casual contraction of けれど. Both work as contrastive connectors. The choice is register: use けれど or 〜が in business/written/formal; けど is fine in casual speech.",
        "category": "register",
        "provenance": "native_reviewed",
        "provenance_note": "REG-001 D6 follow-up migration 2026-05-18 — moved from wrong_corrected_pair to common_mistakes register_variant. Caught by JA-127.",
        "bug_reg_001_d6_fix_2026_05_18": True,
    }),
    "n5-173": (1, {
        "kind": "register_variant",
        "form_a": "たべなくちゃ いけない。",
        "form_b": "たべなくては いけません。",
        "label_a": "casual / spoken — contraction of なくては",
        "label_b": "polite / formal — full なくては + polite いけません",
        "why": "なくちゃ is the casual contraction of なくては. Both express obligation. The choice is register: use なくては + いけません in business/formal/written; なくちゃ is fine in casual speech.",
        "category": "register",
        "provenance": "native_reviewed",
        "provenance_note": "REG-001 D6 follow-up migration 2026-05-18 — moved from wrong_corrected_pair to common_mistakes register_variant. Caught by JA-127.",
        "bug_reg_001_d6_fix_2026_05_18": True,
    }),
    "n5-179": (1, {
        "kind": "register_variant",
        "form_a": "たなかさんですって?",
        "form_b": "たなかさんですか。",
        "label_a": "casual / spoken — hearsay-question 〜って? as casual quotative",
        "label_b": "polite / neutral — standard question marker か",
        "why": "〜って? at the end of a question is a casual quotative-question (\"so it's Tanaka, huh?\"). か is the neutral question marker. The choice is register, not correctness — use か in formal/business contexts; 〜って? is fine in casual speech.",
        "category": "register",
        "provenance": "native_reviewed",
        "provenance_note": "REG-001 D6 follow-up migration 2026-05-18 — moved from wrong_corrected_pair to common_mistakes register_variant. Caught by JA-127.",
        "bug_reg_001_d6_fix_2026_05_18": True,
    }),
}

def main():
    fp = os.path.join(REPO_N5, "data", "grammar.json")
    bak = fp + f".bak_{TODAY}_reg_001_d6"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        gj = json.load(f)

    # Apply migrations: highest index first to avoid renumbering issues
    by_pid = {p["id"]: p for p in gj["patterns"]}
    for pid, (idx, new_entry) in MIGRATIONS.items():
        p = by_pid.get(pid)
        if not p:
            print(f"  ERROR: {pid} not found")
            continue
        wcp = p.get("wrong_corrected_pair", [])
        if idx >= len(wcp):
            print(f"  ERROR: {pid} wcp[{idx}] out of range")
            continue
        old = wcp[idx]
        # Confirm marker
        if "(in formal context)" not in old.get("wrong", ""):
            print(f"  WARN: {pid} wcp[{idx}] doesn't match expected D6 marker; skipping")
            continue
        # Move to common_mistakes
        p.setdefault("common_mistakes", []).append(new_entry)
        # Remove from wrong_corrected_pair
        p["wrong_corrected_pair"] = [e for i, e in enumerate(wcp) if i != idx]
        print(f"  Migrated {pid}.wrong_corrected_pair[{idx}] → register_variant")

    with open(fp, "w", encoding="utf-8") as f:
        json.dump(gj, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
