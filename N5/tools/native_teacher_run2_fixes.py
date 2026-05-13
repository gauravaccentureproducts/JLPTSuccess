"""Native-teacher review run-2 fixes — T-1 + T-3.

T-1: 2 more cross-contaminated grammar meaning_ja entries (n5-151,
n5-183) that JA-71 missed due to single-character coincidental overlap.
Rewrite both + tighten JA-71's threshold to require ≥2-char overlap.

T-3: 9 reading questions use legacy `question_ja` schema key. Rename to
canonical `prompt_ja` + add JA-73 invariant.

T-2 (C-1 announcer+content speaker refinement) is OPT-IN per the run-2
review; not included here.
"""
import json
import io
import sys
import shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

GRAMMAR = "data/grammar.json"
READING = "data/reading.json"
GRAMMAR_BAK = "data/grammar.json.bak_2026_05_13_run2_fixes"
READING_BAK = "data/reading.json.bak_2026_05_13_run2_fixes"


# T-1: 2 meaning_ja rewrites
MEANING_JA_FIXES = {
    "n5-151": (
        "「〜は いかがですか」は、ものを すすめる ときや たずねる ときの "
        "ていねいな いいかたです。「おちゃは いかがですか」「コーヒーは "
        "いかがですか」。"
    ),
    "n5-183": (
        "「だれか／なにか／どこか」は ある人・もの・ばしょを いいます。"
        "「だれも／なにも／どこも」は (with negative) いない・ない、と "
        "いう いみに なります。「だれかが 来ました」「なにも 食べませんでした」。"
    ),
}


def fix_t1():
    shutil.copy2(GRAMMAR, GRAMMAR_BAK)
    g_raw = json.load(open(GRAMMAR, encoding="utf-8"))
    fixed = 0
    for p in g_raw["patterns"]:
        pid = p["id"]
        if pid in MEANING_JA_FIXES:
            old = p.get("meaning_ja", "")
            p["meaning_ja"] = MEANING_JA_FIXES[pid]
            p["meaning_ja_provenance"] = "native_teacher_review_run2_2026_05_13"
            p["meaning_ja_audit_wave"] = "t1-r2-meaning-ja-fix-2026-05-13"
            print(f"  {pid}: meaning_ja rewritten (old: '{old[:40]}', new: '{MEANING_JA_FIXES[pid][:40]}')")
            fixed += 1
    with open(GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(g_raw, f, ensure_ascii=False, indent=2)
    print(f"T-1: {fixed}/{len(MEANING_JA_FIXES)} meaning_ja rewrites applied")


def fix_t3():
    shutil.copy2(READING, READING_BAK)
    r_raw = json.load(open(READING, encoding="utf-8"))
    renamed = 0
    for r in r_raw["passages"]:
        for q in r.get("questions") or []:
            if "question_ja" in q and "prompt_ja" not in q:
                q["prompt_ja"] = q.pop("question_ja")
                renamed += 1
    with open(READING, "w", encoding="utf-8") as f:
        json.dump(r_raw, f, ensure_ascii=False, indent=2)
    print(f"T-3: {renamed} questions renamed question_ja -> prompt_ja")


def main():
    print("=" * 60)
    print("T-1: meaning_ja cross-contamination (n5-151, n5-183)")
    print("=" * 60)
    fix_t1()
    print()
    print("=" * 60)
    print("T-3: schema rename question_ja -> prompt_ja")
    print("=" * 60)
    fix_t3()


if __name__ == "__main__":
    main()
