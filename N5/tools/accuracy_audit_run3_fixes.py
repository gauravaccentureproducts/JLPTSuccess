"""Accuracy-audit run-3 fix — F-7: form-field consistency on examples.

Anti-pattern §3.2.34 (procedure manual): when some examples in a
pattern have `form` populated and others don't, the UI renders partial
badges (broken UX). Either all examples have form, or none.

Scope: 177/178 patterns have at least 1 example missing form. Concentrated
at slots 4 (152 patterns), 5 (176), and 6 (177) — these slots were
added in a later authoring wave without form values.

Fix: derive form from the example's `ja` content using simple rules:
  - Ends in か / ですか / ますか → "question"
  - Contains ません / なかった / じゃない / じゃありません / ではありません → "negative"
  - Contains ました / でした / だった (past markers) → "past"
  - Otherwise → "affirmative"

Provenance flagged as "auto_derived_form_2026_05_13" so future native
review can promote / refine.

Run-3 false positives explicitly DOCUMENTED (NOT fixed; these are correct):
  - おととい / おととし (legitimate N5 words containing とと)
  - 5時までです / 9時までです (legitimate sequence: まで + です copula)
  Both are within-word or within-grammatical-unit, NOT particle doubling.
  JA-78's stricter 3-consecutive-kana check correctly does NOT flag these.
"""
import json
import io
import sys
import shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

GRAMMAR = "data/grammar.json"
GRAMMAR_BAK = "data/grammar.json.bak_2026_05_13_form_fix"


def derive_form(ja: str) -> str:
    """Derive form label from JA example text using N5-pedagogical conventions."""
    if not ja:
        return "affirmative"
    # Strip terminal punctuation for stem check
    stripped = ja.rstrip("。、！？")
    # Question: ends in か or ですか/ますか or has ? marker
    if stripped.endswith("か") or "ですか" in ja or "ますか" in ja:
        return "question"
    # Negative past: でしたか / なかった / ませんでした
    if "ませんでした" in ja or "なかった" in ja:
        return "past-negative"
    # Past affirmative: ました / でした (without negative)
    if ("ました" in ja or "でした" in ja or "だった" in ja or "かった" in ja) \
            and "ません" not in ja and "なかった" not in ja:
        return "past"
    # Negative: ません / じゃない / ではない / じゃありません / ではありません
    if any(neg in ja for neg in ["ません", "じゃない", "じゃありません",
                                   "ではない", "ではありません", "なくて"]):
        return "negative"
    # Default
    return "affirmative"


def main():
    shutil.copy2(GRAMMAR, GRAMMAR_BAK)
    g_raw = json.load(open(GRAMMAR, encoding="utf-8"))

    filled = 0
    patterns_affected = 0
    for p in g_raw["patterns"]:
        any_changed = False
        exs = p.get("examples") or []
        for ex in exs:
            if not isinstance(ex, dict):
                continue
            if not ex.get("form"):
                ja = ex.get("ja") or ""
                ex["form"] = derive_form(ja)
                ex["form_provenance"] = "auto_derived_form_2026_05_13"
                filled += 1
                any_changed = True
        if any_changed:
            patterns_affected += 1

    with open(GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(g_raw, f, ensure_ascii=False, indent=2)

    print(f"F-7: filled {filled} missing form values across {patterns_affected} patterns")

    # Verify all patterns now have consistent form coverage
    g2 = json.load(open(GRAMMAR, encoding="utf-8"))
    inconsistent = 0
    for p in g2["patterns"]:
        exs = p.get("examples") or []
        if not exs:
            continue
        has = sum(1 for ex in exs if ex.get("form"))
        if 0 < has < len(exs):
            inconsistent += 1
    print(f"Patterns still with mixed form coverage: {inconsistent}")


if __name__ == "__main__":
    main()
