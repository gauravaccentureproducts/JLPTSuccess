"""Second-pass native-teacher audit fix — 17 findings from re-audit
on data/grammar.json (2026-05-14 v2 pass).

Same anti-pattern as the first pass (off-pattern boilerplate at
indices [4][5][6]), but in conjugation/late patterns not touched in
Phase 1/2:

  n5-044 (manner-demonstratives こう/そう/ああ/どう) — 3 fixes
  n5-104 (Verb-stem + たいです)                    — 2 fixes
  n5-142 (〜にします)                              — 2 fixes (incl 1 dup)
  n5-145 (〜とおもいます)                          — 3 fixes
  n5-167 (〜んです / 〜のです)                     — 3 fixes
  n5-170 (Verb-た + ほうがいい)                    — 3 fixes
  n5-066 (Verb-ない)                              — 1 form-tag fix

Plus: false positives in v2 audit checker noted (no fix needed):
- おもしろうございます is correctly contracted (o+u→ō, spelling stays
  the same). Checker's SUSPICIOUS_PRE_GOZA list overreaches.
- n5-135[0] "わたしが 買った 本" relative-clause past — past marker
  is mid-sentence, not at end; checker's heuristic missed it.
- CHECK 8 17 mixed-orthography findings are style/policy decisions
  not strict accuracy bugs; deferred to a future consistency pass.
"""
import json
from collections import OrderedDict
from pathlib import Path

GRAMMAR = Path("data/grammar.json")

CONTENT_FIXES = {
    # n5-044 こう/そう/ああ/どう — pattern teaches manner demonstratives
    ("n5-044", 4): ("こう やりましょう。", "Let's do it this way."),
    ("n5-044", 5): ("ああ しましょう。", "Let's do it that way."),
    ("n5-044", 6): ("どう おもいますか。", "What do you think?"),

    # n5-104 Verb-stem + たいです
    ("n5-104", 5): ("なにを 買いたいですか。", "What do you want to buy?"),
    ("n5-104", 6): ("どこに 行きたいですか。", "Where do you want to go?"),

    # n5-142 〜にします — pattern teaches choice/decision
    ("n5-142", 4): ("ジュースに します。", "I'll have juice."),
    ("n5-142", 5): ("ばんごはんは てんぷらに します。", "I'll have tempura for dinner."),

    # n5-145 〜とおもいます — pattern teaches "I think that ..."
    ("n5-145", 4): ("やまださんは いい 先生だと おもいます。", "I think Yamada-san is a good teacher."),
    ("n5-145", 5): ("あの ホテルは たかいと おもいます。", "I think that hotel is expensive."),
    ("n5-145", 6): ("この りょうりは おいしいと おもいます。", "I think this dish is delicious."),

    # n5-167 〜んです / 〜のです — pattern teaches explanatory/emphatic copula
    ("n5-167", 4): ("どうして べんきょうしないんですか。", "Why aren't you studying?"),
    ("n5-167", 5): ("どこへ 行ったんですか。", "Where did you go?"),
    ("n5-167", 6): ("きょうは いそがしいんです。", "It's that I'm busy today."),

    # n5-170 Verb-た + ほうがいい — pattern teaches recommendation
    ("n5-170", 4): ("やすんだ ほうが いいです。", "You should rest."),
    ("n5-170", 5): ("さんぽした ほうが いいですよ。", "You should go for a walk."),
    ("n5-170", 6): ("くすりを のんだ ほうが いいです。", "You should take medicine."),
}

FORM_FIXES = {
    # n5-066 [4] "そんな ことは 言わないで ください" uses ないで (negative-te-form
    # request), so the form tag should reflect that, not "affirmative".
    ("n5-066", 4): "negative-request",
}


def main() -> None:
    d = json.loads(GRAMMAR.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    applied_content = applied_form = 0
    missing = []
    for (pid, idx), (new_ja, new_en) in CONTENT_FIXES.items():
        for p in d["patterns"]:
            if p["id"] != pid:
                continue
            if idx >= len(p.get("examples", [])):
                missing.append((pid, idx, "out-of-range"))
                break
            ex = p["examples"][idx]
            ex["ja"] = new_ja
            ex["translation_en"] = new_en
            if "vocab_ids" in ex:
                ex["vocab_ids"] = []
            if "pitch_marks" in ex:
                ex["pitch_marks"] = []
            applied_content += 1
            break
    for (pid, idx), new_form in FORM_FIXES.items():
        for p in d["patterns"]:
            if p["id"] != pid:
                continue
            if idx >= len(p.get("examples", [])):
                missing.append((pid, idx, "out-of-range"))
                break
            p["examples"][idx]["form"] = new_form
            applied_form += 1
            break
    GRAMMAR.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"V2 native-audit fixes applied:")
    print(f"  CRITICAL off-pattern content: {applied_content}/{len(CONTENT_FIXES)}")
    print(f"  MAJOR form-tag fixes:         {applied_form}/{len(FORM_FIXES)}")
    if missing:
        print(f"MISSING: {missing}")


if __name__ == "__main__":
    main()
