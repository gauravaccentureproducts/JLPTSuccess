"""Apply Class-D fixes: 7 common_mistakes rows across 7 patterns where
the wrong (and sometimes right) cell contained an ASCII arrow joining
two fragments. Replace with clean single-sentence wrong/right pairs.

Backup: data/grammar.json -> data/grammar.json.bak_2026_05_24_class_d_fix
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_JSON = ROOT / "data" / "grammar.json"
BACKUP = ROOT / "data" / "grammar.json.bak_2026_05_24_class_d_fix"


# Per-pattern fixes. Each entry says: locate common_mistakes[index]
# matching `match_wrong_substring`, then replace wrong/right (and optionally why).
FIXES = [
    {
        "pid": "n5-021",
        "cm_index": 1,
        "expect_wrong_substring": "→ 9時で 5時まで",
        "new_wrong": "9時で 5時まで しごとです。",
        "new_right": "9時から 5時まで しごとです。",
        # why unchanged
    },
    {
        "pid": "n5-030",
        "cm_index": 0,
        "expect_wrong_substring": "→ 日本語の勉強",
        "new_wrong": "日本語の勉強が好きだ。",
        "new_right": "日本語を勉強するのが好きだ。",
        # why unchanged
    },
    {
        "pid": "n5-048",
        "cm_index": 0,
        "expect_wrong_substring": "→ 銀行はどこですか",
        # Original "right" cell carried English meta-explanation, not a JA sentence.
        # Reframe as: wrong = どこですか (when asking for directions) is misleading,
        # right = どこにありますか (locates the place).
        "new_wrong": "銀行はどこですか。",
        "new_right": "銀行はどこにありますか。",
        "new_why": "Beginners conflate どこですか (asking the place name / identification) with どこにありますか (asking where it exists / for directions). When you need directions, use にある; when you're identifying which place it is, use です.",
    },
    {
        "pid": "n5-050",
        "cm_index": 1,
        "expect_wrong_substring": "→ どうだ",
        "new_wrong": "おしごとは どうだ。",
        "new_right": "おしごとは どうですか。",
        # why unchanged
    },
    {
        "pid": "n5-067",
        "cm_index": 0,
        "expect_wrong_substring": "いく → いいた",
        "new_wrong": "きのう がっこうへ いいた。",
        "new_right": "きのう がっこうへ いった。",
        # why unchanged
    },
    {
        "pid": "n5-069",
        "cm_index": 0,
        "expect_wrong_substring": "いく → いいて",
        "new_wrong": "がっこうへ いいて、ともだちに あいました。",
        "new_right": "がっこうへ 行って、ともだちに あいました。",
        # why unchanged
    },
    {
        "pid": "n5-112",
        "cm_index": 1,
        "expect_wrong_substring": "→ 10ふん",
        "new_wrong": "10ふん まちました。",
        "new_right": "10ぷん まちました。",
        # why unchanged
    },
]


def main():
    # 1. Versioned backup (never overwrite an existing backup, per project policy)
    if BACKUP.exists():
        # find next free version
        idx = 2
        while True:
            cand = ROOT / "data" / f"grammar.json.bak_2026_05_24_class_d_fix_v{idx}"
            if not cand.exists():
                shutil.copy2(GRAMMAR_JSON, cand)
                print(f"Backup -> {cand.name}")
                break
            idx += 1
    else:
        shutil.copy2(GRAMMAR_JSON, BACKUP)
        print(f"Backup -> {BACKUP.name}")

    # 2. Load, apply fixes, save
    g = json.loads(GRAMMAR_JSON.read_text(encoding="utf-8"))
    patterns = {p["id"]: p for p in g["patterns"]}

    applied = []
    skipped = []
    for fx in FIXES:
        pid = fx["pid"]
        p = patterns.get(pid)
        if not p:
            skipped.append(f"{pid}: pattern not found")
            continue
        cms = p.get("common_mistakes") or []
        i = fx["cm_index"]
        if i >= len(cms):
            skipped.append(f"{pid}: cm[{i}] out of range (len={len(cms)})")
            continue
        cm = cms[i]
        old_wrong = cm.get("wrong", "")
        if fx["expect_wrong_substring"] not in old_wrong:
            skipped.append(f"{pid}.cm[{i}]: expected substring '{fx['expect_wrong_substring']}' not found in wrong='{old_wrong[:80]}'")
            continue
        # apply
        cm["wrong"] = fx["new_wrong"]
        cm["right"] = fx["new_right"]
        if "new_why" in fx:
            cm["why"] = fx["new_why"]
        applied.append(f"{pid}.cm[{i}]: '{old_wrong[:60]}' -> '{fx['new_wrong']}'")

    # 3. Write
    GRAMMAR_JSON.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nApplied: {len(applied)}/{len(FIXES)}")
    for a in applied:
        print(f"  OK  {a}")
    for s in skipped:
        print(f"  SKIP {s}")


if __name__ == "__main__":
    main()
