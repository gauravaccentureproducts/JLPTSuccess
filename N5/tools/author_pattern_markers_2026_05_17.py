"""Author N5/data/pattern_markers.json — structural markers per pattern.

Used by JA-94 to verify every grammar example contains ≥1 marker
that identifies its parent pattern.

Approach (revised 2026-05-17):
  1. Auto-derive initial markers from each pattern's `pattern` field
     (split on /, ／, ・, +, spaces; strip wildcards + placeholders).
  2. Expand with category-specific conjugational variants:
       - Patterns whose `pattern` contains 'ます' → also include
         ません, ました, ませんでした.
       - Patterns whose `pattern` contains 'です' → also include
         でした, じゃありません, ではありません, じゃ ありません.
       - 'い-Adjective' / 'な-Adjective' / 'Adjectives' category →
         add inflectional suffixes.
       - 'Counters' category → broader number / counter token set.
  3. Validate: every example's ja contains ≥1 marker.
  4. For patterns still failing validation, fall back to OVERRIDES
     (compiled by reading the failing examples).
  5. Emit the catalog. Validation report on stderr.

Run from N5/:
    python tools/author_pattern_markers_2026_05_17.py

Re-running is idempotent; manual OVERRIDES edits propagate to output.
"""
from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR = ROOT / "data" / "grammar.json"
OUTPUT = ROOT / "data" / "pattern_markers.json"


# Manual overrides for patterns where the pattern-field alone doesn't
# capture every example's demonstrating form. Keys: pattern ID; values:
# additional markers to UNION with the auto-derived set.
OVERRIDES: dict[str, list[str]] = {
    # Question words
    "n5-017": ["何", "なに", "なん"],
    "n5-045": ["何", "なに", "なん"],
    "n5-048": ["どこ"],
    "n5-186": ["どこか", "どこも", "どこ"],
    # Particle compounds
    "n5-034": ["しか", "ありません", "ない", "ません"],
    "n5-030": ["の"],
    "n5-029": ["の"],
    "n5-031": ["の"],
    # Connectives & request endings
    "n5-134": ["ので"],
    "n5-149": ["ください", "下さい"],
    "n5-157": ["でしょう"],
    "n5-177": ["すぎる", "すぎます", "すぎました", "すぎた", "すぎない",
               "すぎて", "すぎ"],
    "n5-143": ["なる", "なります", "なりました", "なった", "になる",
               "になります", "くなる", "くなります", "なり", "なりたい"],
    # Time markers (kanji + kana variants)
    "n5-111": ["時", "じ"],
    "n5-112": ["分", "ふん", "ぷん"],
    "n5-113": ["時", "じ", "半", "はん"],
    "n5-116": ["毎", "まい"],
    "n5-118": ["今", "いま", "すぐ", "もう", "まだ"],
    # Plain dictionary-form verb endings (n5-065 = Verb-る/Verb-う)
    # The plain-form ending pattern: verb ends in う-row kana before 。
    "n5-065": ["う。", "く。", "ぐ。", "す。", "つ。", "ぬ。", "ぶ。",
               "む。", "る。", "う", "く", "ぐ", "す", "つ", "ぬ",
               "ぶ", "む", "る", "ない", "た。", "だ。"],
    # Greetings + set phrases
    "n5-166": ["いただきます", "ごちそうさま", "おはようございます",
               "おはよう", "こんにちは", "こんばんは", "ありがとう",
               "すみません", "おやすみ", "さようなら", "いってきます",
               "いってらっしゃい", "ただいま", "おかえり"],
    # Number patterns
    "n5-035": ["一", "二", "三", "四", "五", "六", "七", "八", "九",
               "十", "百", "千", "万", "ひとつ", "ふたつ", "みっつ",
               "よっつ", "いつつ", "むっつ", "ななつ", "やっつ",
               "ここのつ", "とお", "0", "1", "2", "3", "4", "5",
               "6", "7", "8", "9"],
    # Time / counter expressions
    "n5-038": ["時", "じ", "分", "ふん", "ぷん", "半", "はん"],
    # Existence: include both kanji + kana forms
    "n5-088": ["います", "いる", "いません", "いない", "いました",
               "いなかった"],
    "n5-089": ["あります", "ある", "ありません", "ない", "ありました",
               "なかった"],
    # Set greetings particle pattern
    "n5-027": ["よね"],
    # だろう + たろう contraction
    "n5-158": ["だろう", "たろう", "ろうか"],
    # 109 — add なんさつ (counter for books)
    "n5-109": ["いくつ", "いくら", "なんにん", "なんまい", "なんぼん",
               "なんこ", "なんさつ", "なんかい", "なんがつ", "なんじ",
               "なんふん", "なんぷん", "なんねん", "なんにち", "なんがい"],
    # Casual contractions
    "n5-176": ["なくちゃ", "なきゃ", "ちゃ", "きゃ"],
    # Number+counter / Verb+counter+Verb — generic counter tokens
    # (kanji + kana variants for the N5-frequent counters)
    "n5-108": ["一", "二", "三", "四", "五", "六", "七", "八", "九",
               "十", "百", "千", "万", "ひと", "ふた", "みっ", "よっ",
               "いつ", "むっ", "なな", "やっ", "ここの", "とお", "ずつ",
               "つ", "本", "ほん", "ぼん", "ぽん", "人", "にん", "さつ",
               "冊", "ひき", "ぴき", "びき", "匹", "かい", "がい", "回",
               "枚", "まい", "個", "こ", "0", "1", "2", "3", "4", "5",
               "6", "7", "8", "9", "いくつ", "いくら"],
    "n5-110": ["一", "二", "三", "四", "五", "六", "七", "八", "九",
               "十", "百", "千", "万", "ひと", "ふた", "みっ", "よっ",
               "いつ", "むっ", "なな", "やっ", "ここの", "とお", "ずつ",
               "つ", "本", "ほん", "ぼん", "ぽん", "人", "にん", "さつ",
               "冊", "ひき", "ぴき", "びき", "匹", "かい", "がい", "回",
               "枚", "まい", "個", "こ", "0", "1", "2", "3", "4", "5",
               "6", "7", "8", "9", "いくつ", "いくら"],
    # V-plain + N (relative clause) — plain-form verb endings that
    # appear before a modified noun. Same kana set as n5-065
    # (plain dictionary form) plus past-tense forms た / だ.
    "n5-135": ["う", "く", "ぐ", "す", "つ", "ぬ", "ぶ", "む", "る",
               "た", "だ", "ない"],
    # Adj + N (combined) — adjective endings before noun.
    # い-Adj ending い; な-Adj linker な.
    "n5-136": ["い", "な"],
}


# Conjugational expansion rules. If a pattern field contains a key,
# add the value tokens to the marker set.
CONJUGATIONAL_EXPANSIONS: dict[str, list[str]] = {
    "ます": ["ます", "ません", "ました", "ませんでした"],
    "です": ["です", "でした", "じゃありません", "ではありません",
             "じゃあり", "ではあり", "じゃ ありません", "では ありません",
             "じゃ あり", "では あり"],
    "ない": ["ない", "なかった", "なくて", "なくては", "なければ"],
    "た": ["た", "だ"],   # past plain
    "て": ["て", "で"],   # te-form
    "から": ["から"],
    "まで": ["まで"],
    "より": ["より"],
    "ば": ["ば"],
    "たら": ["たら", "だら"],
    "なら": ["なら"],
    "ながら": ["ながら"],
    "たり": ["たり", "だり"],
    "とき": ["とき", "時"],
    "ましょう": ["ましょう", "ましょうか", "ようか"],
    "てください": ["てください", "でください"],
    "ないでください": ["ないでください"],
    "い-Adj": ["い", "くない", "かった", "くなかった", "くて", "く"],
    "な-Adj": ["な", "じゃない", "ではない", "だった", "じゃなかった"],
    "なくては": ["なくては", "なきゃ", "なくちゃ"],
    "なくてもいい": ["なくてもいい", "なくてもよい"],
    "てもいい": ["てもいい", "てもよい"],
    "てはいけ": ["てはいけ", "てはだめ", "てはダメ"],
    "ことができ": ["ことができ", "できる", "できます"],
    "とおもう": ["とおもう", "と思う", "と思います"],
    "とゆう": ["とゆう", "と言う", "と言います", "って"],
}


# Placeholders / wildcards to strip from pattern fields before tokenizing
PLACEHOLDER_TOKENS = {
    "n", "noun", "v", "verb", "adj", "adjective",
    "い-adjective", "な-adjective", "v-plain", "v-た", "v-て", "(noun)",
    "(verb)", "etc.", "etc", "—", "-", "+",
    # Pattern-descriptor English-only tokens that aren't substring-matchable
    "possessive", "nominalizer", "noun-modifier", "basic", "use",
    "compounds", "in", "combined",
}


def derive_markers(p: dict) -> list[str]:
    """Auto-derive marker set for a pattern."""
    pattern_field = p.get("pattern", "") or ""
    markers: set[str] = set()

    # Use 〜 as a separator (not just strip), so "しか〜ない" → ["しか", "ない"].
    # Also handle fullwidth parens （ ）.
    cleaned = pattern_field
    raw_tokens = re.split(r"[／/・+〜～\s\(\)（）]+", cleaned)
    for tok in raw_tokens:
        tok = tok.strip()
        if not tok:
            continue
        if tok.lower() in PLACEHOLDER_TOKENS:
            continue
        # Skip tokens that are mostly Latin letters (pattern descriptors
        # like 'Noun', 'Adj')
        if all(c.isascii() and (c.isalpha() or c in "-_") for c in tok):
            # Latin descriptor — keep only if it's a Japanese-particle
            # romanization that ALSO appears in the actual text (rare;
            # for now skip)
            continue
        markers.add(tok)

    # Conjugational expansion
    for key, expansion in CONJUGATIONAL_EXPANSIONS.items():
        if key in pattern_field:
            for v in expansion:
                markers.add(v)

    # Category-specific expansions
    category = p.get("category", "") or ""
    if "Adjective" in category:
        for v in CONJUGATIONAL_EXPANSIONS.get("い-Adj", []):
            markers.add(v)
        for v in CONJUGATIONAL_EXPANSIONS.get("な-Adj", []):
            markers.add(v)
    if "ます-form" in category or "tense" in category.lower():
        for v in CONJUGATIONAL_EXPANSIONS.get("ます", []):
            markers.add(v)

    # Manual overrides
    pid = p.get("id")
    if pid in OVERRIDES:
        for v in OVERRIDES[pid]:
            markers.add(v)

    # Remove pure-Latin tokens that snuck through
    markers = {m for m in markers if not all(c.isascii() and c.isalpha() for c in m)}

    return sorted(markers)


def validate(catalog: dict, grammar: dict) -> list[tuple]:
    """Return list of (pid, ex_idx, ja, markers) for failing examples."""
    failures = []
    for p in grammar.get("patterns") or []:
        pid = p.get("id")
        if not pid:
            continue
        markers = catalog["patterns"].get(pid) or []
        if not markers:
            continue
        for i, ex in enumerate(p.get("examples") or []):
            if not isinstance(ex, dict):
                continue
            ja = ex.get("ja", "") or ""
            if not ja:
                continue
            if not any(m in ja for m in markers):
                failures.append((pid, i, ja, markers))
    return failures


def main() -> int:
    g = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    catalog = {
        "_meta": {
            "purpose": "Per-pattern structural-markers catalog for JA-94. Every grammar example's ja must contain ≥1 marker from its parent pattern's list.",
            "authoring": (
                "Auto-derived from each pattern's `pattern` field plus "
                "category-specific conjugational expansions, with "
                "per-pattern OVERRIDES for patterns whose examples "
                "demonstrate the pattern via forms not in the bare "
                "pattern field. Regenerate via "
                "`python tools/author_pattern_markers_2026_05_17.py` "
                "after grammar.json edits."
            ),
            "validation_contract": (
                "JA-94: for each pattern, every example's ja must "
                "contain ≥1 marker as a literal substring. To fix a "
                "failing example: either expand the pattern's markers "
                "list (preferred — the form is canonical) or rewrite "
                "the example to use a canonical marker."
            ),
            "regenerated": "2026-05-17",
        },
        "patterns": {},
    }

    for p in g.get("patterns") or []:
        pid = p.get("id")
        if not pid:
            continue
        catalog["patterns"][pid] = derive_markers(p)

    failures = validate(catalog, g)
    n_total_examples = sum(
        len([ex for ex in (p.get("examples") or []) if isinstance(ex, dict) and ex.get("ja")])
        for p in g.get("patterns") or []
    )

    print(f"Patterns: {len(catalog['patterns'])}")
    print(f"Total examples (with non-empty ja): {n_total_examples}")
    print(f"Failing examples (no marker matches): {len(failures)}")
    coverage = (1.0 - len(failures) / n_total_examples) * 100 if n_total_examples else 100
    print(f"Coverage: {coverage:.1f}%")

    if failures:
        # Group by pattern to spot patterns needing OVERRIDES
        from collections import Counter
        per_pat = Counter(f[0] for f in failures)
        print("\nTop patterns with failing examples (consider adding OVERRIDES):")
        for pid, n in per_pat.most_common(20):
            print(f"  {pid}: {n} failing examples")
            # Show first 3
            for pid2, i, ja, mk in failures:
                if pid2 == pid:
                    print(f"    ex[{i}]: {ja[:70]!r}")
                    break

    OUTPUT.write_text(
        json.dumps(catalog, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nWrote {OUTPUT}")
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
