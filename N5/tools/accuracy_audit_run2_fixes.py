"""Accuracy-audit run-2 fixes — F4, F5, F6.

F-4 CRITICAL: n5-098.wrong_corrected_pair[1] and [2] are LITERAL
  PLACEHOLDERS. Fields read:
    wrong: "(unspecified — keep prior)"
    correct: "(unspecified — keep prior)"
    why: "Pattern-shape placeholder; primary entry covers main trap."
  These would render in the UI as broken entries. Replace with real
  wrong/right pairs for the すき/きらい が-not-を pattern.

F-5 MAJOR: n5-072 ex[9] has "ははは でんわを かけて います" — 3
  consecutive は kana parses correctly to natives (母 + は particle)
  but reads as a typo to N5 learners. 母 IS in N5 kanji.
  Fix: ははは → 母は.

F-6 MAJOR: n5-146 ex[8] has "ははが くると いいました" — same class
  of issue (はは + が particle).
  Fix: ははが → 母が.

JA-77 invariant: any field whose string value contains placeholder
  text ('(unspecified', 'placeholder', 'TODO', 'TBD', 'keep prior',
  '(temp)', 'FIXME', 'INSERT_', 'fallback ref') triggers FAIL. Locks
  out future leakage.

JA-78 invariant: example sentences must not contain 3+ consecutive
  same hiragana (catches the n5-072/n5-146 typo-looking class).
"""
import json
import io
import sys
import shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

GRAMMAR = "data/grammar.json"
GRAMMAR_BAK = "data/grammar.json.bak_2026_05_13_accuracy_run2"


def fix_f4():
    """Replace 2 placeholder wrong_corrected_pair entries in n5-098."""
    g_raw = json.load(open(GRAMMAR, encoding="utf-8"))
    for p in g_raw["patterns"]:
        if p["id"] != "n5-098":
            continue
        wcp = p.get("wrong_corrected_pair") or []
        if len(wcp) < 3:
            print("  ! n5-098 has fewer than 3 wcp entries; skipping")
            return
        # Replace wcp[1] — じょうず variant (same が-not-を class, different
        # な-adjective; classic N5 trap)
        wcp[1] = {
            "wrong": "日本ごを じょうずです。",
            "correct": "日本ごが じょうずです。",
            "why": "じょうず / へた / すき / きらい / ほしい mark their target with が, not を. "
                   "They're な-adjectives functioning as predicate-state — the target is the "
                   "subject of the state, not the object of an action.",
            "provenance": "native_teacher_review_2026_05_13",
            "error_category": "particle",
            "audit_wave": "accuracy-audit-f4-fix-2026-05-13",
        }
        # Replace wcp[2] — きらい variant (negative preference)
        wcp[2] = {
            "wrong": "なっとうを きらいです。",
            "correct": "なっとうが きらいです。",
            "why": "きらい (na-adj, 'disliked') takes its target with が. Same rule as すき: "
                   "the disliked thing is the SUBJECT of the dislike-state, not a direct object.",
            "provenance": "native_teacher_review_2026_05_13",
            "error_category": "particle",
            "audit_wave": "accuracy-audit-f4-fix-2026-05-13",
        }
        p["wrong_corrected_pair"] = wcp
        print("  F-4: n5-098 wcp[1] and wcp[2] replaced with real wrong/right pairs")
        break
    with open(GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(g_raw, f, ensure_ascii=False, indent=2)


def fix_f5_f6():
    """Replace ははは → 母は in n5-072 ex[9] and ははが → 母が in n5-146 ex[8]."""
    g_raw = json.load(open(GRAMMAR, encoding="utf-8"))
    changes = []
    for p in g_raw["patterns"]:
        if p["id"] == "n5-072":
            exs = p.get("examples") or []
            if len(exs) > 9:
                old = exs[9].get("ja")
                if "ははは" in old:
                    exs[9]["ja"] = old.replace("ははは", "母は", 1)
                    exs[9]["audit_wave"] = "accuracy-audit-f5-fix-2026-05-13"
                    changes.append(("F-5", "n5-072 ex[9]", old, exs[9]["ja"]))
        elif p["id"] == "n5-146":
            exs = p.get("examples") or []
            if len(exs) > 8:
                old = exs[8].get("ja")
                if "ははが" in old:
                    exs[8]["ja"] = old.replace("ははが", "母が", 1)
                    exs[8]["audit_wave"] = "accuracy-audit-f6-fix-2026-05-13"
                    changes.append(("F-6", "n5-146 ex[8]", old, exs[8]["ja"]))
    with open(GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(g_raw, f, ensure_ascii=False, indent=2)
    for tag, where, old, new in changes:
        print(f"  {tag} {where}: {old!r} -> {new!r}")


def main():
    shutil.copy2(GRAMMAR, GRAMMAR_BAK)
    print("=" * 60)
    print("F-4: n5-098 placeholder wrong_corrected_pair replacement")
    print("=" * 60)
    fix_f4()
    print()
    print("=" * 60)
    print("F-5 + F-6: ははは / ははが → 母は / 母が in examples")
    print("=" * 60)
    fix_f5_f6()


if __name__ == "__main__":
    main()
