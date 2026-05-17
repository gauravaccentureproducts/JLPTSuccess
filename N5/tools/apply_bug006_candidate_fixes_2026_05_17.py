"""Apply 14 BUG-006-CANDIDATE example replacements (Phase A).

Replaces wrong-pattern examples in grammar.json with new examples
that demonstrate the parent pattern, retiring the 14 entries in
data/_ja94_baseline.json. After this script, _ja94_baseline.json
becomes an empty allowlist and JA-94 enforces the marker-presence
invariant unconditionally on the current corpus.

Replacements authored 2026-05-17:

  n5-030 (nominalizer の): ex[4], [5], [6] used honorific お+adj+です
    or が-particle preference statements (no nominalizer). Replaced with
    V+のは / V+のが + adj/copula sentences.

  n5-048 (どこ): ex[0], [1], [6] used ここ / そこ / だれ (different
    demonstratives / question words). Replaced with どこ examples.

  n5-065 (Verb-る / Verb-う plain): ex[4] used polite かいません.
    Replaced with plain-form みる sentence.

  n5-071 (Verb-てください): ex[7] used noun+を+ください alone (no V-て).
    Replaced with V-て+ください request.

  n5-084 (な-Adj + な + Noun): ex[5] had no na-adjective. Replaced
    with べんりな きかい sentence.

  n5-112 (〜ふん/ぷん minutes): ex[8] used じはん / じかん (different time
    units). Replaced with じゅっぷん.

  n5-157 (〜でしょう probability): ex[4], [5], [6] used volitional
    ましょう. Replaced with でしょう probability/confirmation sentences.

  n5-164 (〜さん honorific): ex[6] had no さん. Replaced with
    たなかさん sentence.

Run from N5/:
    python tools/apply_bug006_candidate_fixes_2026_05_17.py
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_JSON = ROOT / "data" / "grammar.json"
BASELINE_JSON = ROOT / "data" / "_ja94_baseline.json"


# (pattern_id, ex_index, new_ja, new_translation_en)
REPLACEMENTS = [
    ("n5-030", 4, "うんどうするのは きもちが いいです。",
     "Exercising feels good."),
    ("n5-030", 5, "ピアノを ひくのが すきです。",
     "I like playing the piano."),
    ("n5-030", 6, "えいがを みるのが たのしいです。",
     "Watching movies is fun."),
    ("n5-048", 0, "ぎんこうは どこですか。",
     "Where is the bank?"),
    ("n5-048", 1, "どこで パンを かいますか。",
     "Where do you buy bread?"),
    ("n5-048", 6, "あなたの くには どこですか。",
     "Where is your country?"),
    ("n5-065", 4, "ともだちと えいがを みる。",
     "[I] watch a movie with a friend. (casual)"),
    ("n5-071", 7, "もう いちど せつめいして ください。",
     "Please explain once more."),
    ("n5-084", 5, "べんりな きかいです。",
     "It's a convenient machine."),
    ("n5-112", 8, "じゅっぷん やすみました。",
     "I rested for 10 minutes."),
    ("n5-157", 4, "あの えいがは おもしろい でしょう。",
     "That movie is probably interesting."),
    ("n5-157", 5, "電車は こんで いる でしょう。",
     "The train is probably crowded."),
    ("n5-157", 6, "この もんだいは むずかしい でしょう。",
     "This problem is probably difficult."),
    ("n5-164", 6, "たなかさんは げんきですか。",
     "Is Tanaka-san well?"),
]


def main() -> int:
    g = json.loads(GRAMMAR_JSON.read_text(encoding="utf-8"))
    by_pid = {p.get("id"): p for p in g.get("patterns") or []}
    n_applied = 0
    n_skipped = 0
    for pid, idx, new_ja, new_en in REPLACEMENTS:
        p = by_pid.get(pid)
        if not p:
            print(f"  SKIP {pid} ex[{idx}]: pattern not found")
            n_skipped += 1
            continue
        examples = p.get("examples") or []
        if idx >= len(examples):
            print(f"  SKIP {pid} ex[{idx}]: out of range "
                  f"(have {len(examples)})")
            n_skipped += 1
            continue
        ex = examples[idx]
        if not isinstance(ex, dict):
            print(f"  SKIP {pid} ex[{idx}]: not a dict")
            n_skipped += 1
            continue
        old_ja = ex.get("ja", "")
        old_en = ex.get("translation_en") or ex.get("en", "")
        # Replace
        ex["ja"] = new_ja
        # Set translation_en (overwriting whichever key was used)
        if "translation_en" in ex or "translation_en" in p.get(
            "examples", [{}])[0] if p.get("examples") else {}:
            ex["translation_en"] = new_en
        else:
            ex["translation_en"] = new_en
        # If old used "en" instead, drop it after migration
        if "en" in ex and "translation_en" in ex and ex.get("en") != ex.get(
            "translation_en"
        ):
            del ex["en"]
        n_applied += 1
        print(f"  {pid} ex[{idx}]:")
        print(f"    old ja: {old_ja!r}")
        print(f"    new ja: {new_ja!r}")
        print(f"    new en: {new_en!r}")
    GRAMMAR_JSON.write_text(
        json.dumps(g, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nApplied {n_applied} replacements; skipped {n_skipped}.")

    # Empty the JA-94 baseline (all 14 BUG-006-CANDIDATEs addressed)
    bl = json.loads(BASELINE_JSON.read_text(encoding="utf-8"))
    n_prior = len(bl.get("baseline_failing_examples") or [])
    bl["baseline_failing_examples"] = []
    if "_audit_summary" in bl and isinstance(bl["_audit_summary"], dict):
        bl["_audit_summary"]["examples_failing_marker_check"] = 0
        bl["_audit_summary"]["coverage_pct"] = 100.0
        bl["_audit_summary"]["patterns_with_failures"] = 0
        bl["_audit_summary"]["follow_on_target"] = (
            "RESOLVED 2026-05-17 (Phase A): all 14 BUG-006-CANDIDATE "
            "examples replaced with parent-pattern-demonstrating ones. "
            "JA-94 now enforces marker-presence unconditionally on the "
            "current corpus."
        )
    if "_meta" in bl and isinstance(bl["_meta"], dict):
        bl["_meta"]["purpose"] = (
            "Baseline allowlist for JA-94 (per-example structural-marker "
            "presence). RESOLVED 2026-05-17 (Phase A) — all 14 prior "
            "BUG-006-CANDIDATE entries addressed via example replacement. "
            "JA-94 enforces marker-presence unconditionally; this file's "
            "baseline_failing_examples array is empty and serves as a "
            "RESOLVED snapshot."
        )
        bl["_meta"]["resolution_date"] = "2026-05-17"
    BASELINE_JSON.write_text(
        json.dumps(bl, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"\nEmptied {BASELINE_JSON.name}: "
          f"{n_prior} -> 0 baseline_failing_examples")
    return 0 if n_applied == len(REPLACEMENTS) else 1


if __name__ == "__main__":
    sys.exit(main())
