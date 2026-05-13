"""Native-teacher audit run-3 fixes.

R3-T1 (Medium): 2 more cross-contaminated grammar meaning_ja that JA-71
  still didn't catch:
    n5-154 (もう + Verb-ました) → was describing へ direction
    n5-106 (Noun + が ほしいです) → was describing 〜をください
  JA-71 misses these because the full meaning_ja happens to contain
  one of the pattern's kana (も, です, etc.) incidentally. Subtle
  cases like these require manual native-teacher review; the
  invariant catches egregious cases only.

R3-T2 (Low): see_also targets — 5 unresolved entries from G-2 cleanup.
  My G-2 extraction stored marker strings (like "Verb", "〜",
  "Adjective + Noun") instead of resolving to specific pattern_ids.
  For unresolvable targets, remove from see_also. For resolvable
  targets, map to pattern_id where possible.

R3-T3 (Low): listening speaker tag normalization.
  3 items (n5.listen.048, .049, plus one more) use single-letter M/F
  tags from hand-authored dialogue items. Normalize to "male"/"female"
  for schema parity with the T-2 fix output.
"""
import json
import io
import sys
import shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

GRAMMAR = "data/grammar.json"
LISTENING = "data/listening.json"
GRAMMAR_BAK = "data/grammar.json.bak_2026_05_13_run3"
LISTENING_BAK = "data/listening.json.bak_2026_05_13_run3"


# === R3-T1: meaning_ja rewrites ===
MEANING_JA_FIXES = {
    "n5-154": (
        "「もう + Verb-ました」で、すでに した ことを いいます。「もう "
        "食べました」「もう しゅくだいを しました」。よく 「まだ + "
        "Verb-ていません」(まだ 食べて いません) と ペアで つかいます。"
    ),
    "n5-106": (
        "「Noun + が ほしいです」で、ほしい ものを いいます。「車が "
        "ほしいです」「あたらしい かばんが ほしいです」。を ではなく "
        "が を つかう ことが ポイントです。"
    ),
}


# === R3-T2: see_also resolution map ===
# For each pattern, map the unresolved see_also target to either a
# specific pattern_id (when resolvable) or None (remove).
SEE_ALSO_RESOLUTIONS = {
    "n5-045": ("なん / なに", None),       # abstract reading variant; just remove
    "n5-098": ("〜", None),                  # empty placeholder; remove
    "n5-136": ("Adjective + Noun", None),    # abstract category; remove
    "n5-162": ("Verb", None),                # abstract category; remove
    "n5-163": ("Verb", None),                # abstract category; remove
}


def fix_t1():
    g_raw = json.load(open(GRAMMAR, encoding="utf-8"))
    fixed = 0
    for p in g_raw["patterns"]:
        pid = p["id"]
        if pid in MEANING_JA_FIXES:
            old = p.get("meaning_ja", "")
            p["meaning_ja"] = MEANING_JA_FIXES[pid]
            p["meaning_ja_audit_wave"] = "r3-t1-meaning-ja-fix-2026-05-13"
            p["meaning_ja_provenance"] = "native_teacher_review_run3_2026_05_13"
            fixed += 1
            print(f"  {pid}: meaning_ja rewritten")
    with open(GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(g_raw, f, ensure_ascii=False, indent=2)
    print(f"R3-T1: {fixed} meaning_ja rewrites")


def fix_t2():
    g_raw = json.load(open(GRAMMAR, encoding="utf-8"))
    cleaned = 0
    for p in g_raw["patterns"]:
        pid = p["id"]
        targets = p.get("see_also") or []
        if not targets:
            continue
        new_targets = []
        for t in targets:
            if pid in SEE_ALSO_RESOLUTIONS and t == SEE_ALSO_RESOLUTIONS[pid][0]:
                resolved = SEE_ALSO_RESOLUTIONS[pid][1]
                if resolved is None:
                    cleaned += 1
                    continue  # drop the unresolvable target
                new_targets.append(resolved)
            else:
                new_targets.append(t)
        if new_targets != targets:
            if new_targets:
                p["see_also"] = new_targets
            else:
                p.pop("see_also", None)
    with open(GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(g_raw, f, ensure_ascii=False, indent=2)
    print(f"R3-T2: {cleaned} unresolvable see_also targets dropped")


def fix_t3():
    shutil.copy2(LISTENING, LISTENING_BAK)
    l_raw = json.load(open(LISTENING, encoding="utf-8"))
    normalized = 0
    for li in l_raw["items"]:
        for ln in li.get("lines") or []:
            sp = ln.get("speaker")
            if sp == "M":
                ln["speaker"] = "male"
                normalized += 1
            elif sp == "F":
                ln["speaker"] = "female"
                normalized += 1
    with open(LISTENING, "w", encoding="utf-8") as f:
        json.dump(l_raw, f, ensure_ascii=False, indent=2)
    print(f"R3-T3: {normalized} M/F speaker tags normalized to male/female")


def main():
    shutil.copy2(GRAMMAR, GRAMMAR_BAK)
    print("Backups created.")
    print()
    print("=" * 60)
    print("R3-T1: cross-contaminated meaning_ja (n5-154, n5-106)")
    print("=" * 60)
    fix_t1()
    print()
    print("=" * 60)
    print("R3-T2: see_also unresolvable targets")
    print("=" * 60)
    fix_t2()
    print()
    print("=" * 60)
    print("R3-T3: speaker tag normalization M/F → male/female")
    print("=" * 60)
    fix_t3()


if __name__ == "__main__":
    main()
