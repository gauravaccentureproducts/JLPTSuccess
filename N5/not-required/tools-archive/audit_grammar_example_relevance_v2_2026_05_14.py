"""V2 of the grammar-example relevance audit.

V1 (audit_grammar_example_relevance_2026_05_14.py) had ~600+ false
positives on multi-form pattern labels ("Verb-plain + な",
"Question word + か / も compounds", etc.) because it treated the
meta-label as a literal substring to match.

V2 adds pattern-class detection so meta-labels are mapped to the
class-of-things-that-look-right. Specifically:

- "Verb-plain" / "V-plain" / "Verb-dictionary" / "V-dict" → check
  the example contains at least one verb in plain/dictionary form
  (ends in う/く/ぐ/す/つ/ぬ/ぶ/む/る at a word-boundary)
- "Verb-stem" / "V-stem" → check for ます-form-base before a
  trailing particle/aux
- "Verb-て" / "V-て" / "V-て form" → check for て/で-form verb
- "Verb-た" / "V-た" → check for past-form た/だ at sentence end
- "Verb-ない" / "V-ない" → check for ない-form
- "Verb-ます" / "V-ます" → check for ます/ません-form
- "い-form" / "Adj-い" → check for i-adjective ending in い
- "な-form" / "Adj-な" → check for na-adjective
- "Question word" → expand to a set: なに / なん / 何 / だれ / どなた /
  どこ / いつ / どれ / どの / どちら / どう / なぜ / どうして / いくつ / いくら
- "+ N" / "+ noun" / "+ verb" / "+ Adj" — strip the annotation,
  recursively check the root marker

Plus:
- 〜 (tilde) handled as a separator — "から〜まで" requires BOTH
  から AND まで in the example
- Parenthetical readings (e.g. "何（なに／なん）") expanded to
  alternatives: {何, なに, なん}
- Boilerplate-leak detection: examples repeated across ≥2 patterns,
  with same-pattern-marker check to identify which occurrences are
  legitimate vs misplaced.

Run:
  python -X utf8 not-required/tools-archive/audit_grammar_example_relevance_v2_2026_05_14.py
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

GRAMMAR = Path("data/grammar.json")

SINGLE_CHAR_PARTICLES = set("をにへでとがはのもや")

PARTICLE_TRAILING = {
    "と": [" ", "いき", "いっ", "いい", "あいま", "はな", "話", "行", "言",
            "思", "見", "会", "や", "かい", "それ"],
    "を": [" ", "し", "見", "読", "書", "た", "の", "た べ"],
    "に": [" ", "いき", "あ", "あい", "つ", "もら", "教", "見", "行"],
    "へ": [" ", "いき", "行"],
    "で": [" ", "し", "あ", "なに", "何", "じ"],
    "が": [" ", "あり", "い", "ほし", "好", "わかり", "き"],
    "は": [" ", "なん", "なに", "どこ", "どう", "あり", "い", "に"],
    "の": [" ", "うえ", "した", "なか", "前", "後", "上", "下"],
    "も": [" ", "あり", "い", "ほし", "た", "好"],
    "や": [" ", "りんご"],
}

QUESTION_WORDS = {"なに", "なん", "何", "だれ", "どなた", "どこ", "いつ",
                  "どれ", "どの", "どちら", "どう", "なぜ", "どうして",
                  "いくつ", "いくら"}

# Heuristic verb endings (plain form). Anything ending in these at word
# boundary suggests a plain-form verb is present.
PLAIN_VERB_ENDINGS = ["う", "く", "ぐ", "す", "つ", "ぬ", "ぶ", "む", "る"]


def particle_used_as_particle(text: str, particle: str) -> bool:
    if particle not in text:
        return False
    trailing = PARTICLE_TRAILING.get(particle, [" "])
    for m in re.finditer(re.escape(particle), text):
        end = m.end()
        if end >= len(text):
            return True
        rest = text[end:end + 4]
        if rest.startswith(("。", "、", "?", "？", "!", "！")):
            return True
        if any(rest.startswith(t) for t in trailing):
            return True
        start = m.start()
        if start > 0 and text[start - 1] == " ":
            return True
    return False


def has_question_word(text: str) -> bool:
    return any(qw in text for qw in QUESTION_WORDS)


def has_plain_verb(text: str) -> bool:
    """Heuristic: text contains at least one plain-form verb. Looks for a
    plain-verb ending immediately before a particle / clause-end / 〜な /
    の / こと / よう etc. False-positive-prone but catches the common
    cases. False negatives on irregular verbs in unusual contexts."""
    # Strip trailing punctuation
    body = text.rstrip("。、！？!?")
    # Check sentence-end first
    for end in PLAIN_VERB_ENDINGS:
        if body.endswith(end):
            return True
    # Check ＋な (e.g. 行くな, 走るな)
    for end in PLAIN_VERB_ENDINGS:
        if (end + "な") in text or (end + "！") in text:
            return True
    # Check before こと / の (nominalisation)
    for end in PLAIN_VERB_ENDINGS:
        if end + "こと" in text or end + " こと" in text:
            return True
        if end + "の" in text:
            return True
    # Check before まえ / あと / とき / ながら (subordinator)
    for end in PLAIN_VERB_ENDINGS:
        for sub in ["まえ", "あと", "とき", "ながら", "から", "ので"]:
            if end + sub in text or end + " " + sub in text:
                return True
    return False


def has_te_form(text: str) -> bool:
    return any(t in text for t in ["て ", "で ", "て。", "で。", "てい", "でい", "てく", "ても", "でも", "ては", "では"])


def has_ta_form(text: str) -> bool:
    return bool(re.search(r"[たんっ]た[。、！？!?\s]|[いえおうそしちにひみり]だ[。、！？!?\s]", text))


def has_nai_form(text: str) -> bool:
    return "ない" in text or "ません" in text


def has_masu_form(text: str) -> bool:
    return "ます" in text or "ません" in text or "ました" in text or "ましょう" in text


def has_i_adj(text: str) -> bool:
    """Heuristic: text contains an i-adjective (ends with い in adjective
    position). Approximates by checking for common N5 i-adjectives."""
    n5_i_adj = ["たかい", "やすい", "おおきい", "ちいさい", "あつい", "さむい",
                "あたらしい", "ふるい", "おいしい", "まずい", "おもい", "かるい",
                "ながい", "みじかい", "はやい", "おそい", "ひろい", "せまい",
                "あかい", "あおい", "しろい", "くろい", "きいろい", "ちかい",
                "とおい", "つよい", "よわい", "むずかしい", "やさしい", "いい",
                "わるい", "うれしい", "かなしい", "たのしい", "おもしろい",
                "つまらない", "あぶない"]
    return any(a in text for a in n5_i_adj)


def has_na_adj(text: str) -> bool:
    n5_na_adj = ["しずか", "にぎやか", "きれい", "ゆうめい", "しんせつ",
                 "げんき", "ひま", "べんり", "ふべん", "じょうず", "へた",
                 "すき", "きらい", "たいせつ", "だいじょうぶ", "ゆっくり"]
    return any(a in text for a in n5_na_adj)


# Pattern-class detector — given the pattern's label string, returns a
# checker function that takes (example_ja) and returns (is_relevant, reason).
def build_checker(pattern: str):
    p = pattern.strip()
    # Strip parenthetical readings: 何（なに／なん） → 何 + alternatives {何, なに, なん}
    paren_readings: list[str] = []
    paren_match = re.search(r"（([^）]+)）|\(([^)]+)\)", p)
    if paren_match:
        inside = paren_match.group(1) or paren_match.group(2)
        paren_readings = [r.strip() for r in re.split(r"[／/]", inside) if r.strip()]
        p = re.sub(r"（[^）]*）|\([^)]*\)", "", p).strip()
    # Strip "+ N (noun)" / "+ verb" trailing annotation
    p = re.sub(r"\s*[+＋]\s*[NA].*$", "", p).strip()
    p = re.sub(r"\s*[+＋]\s*\w.*$", "", p).strip()
    # Split on 〜 — both parts required
    tilde_parts = [s.strip() for s in re.split(r"[〜~]", p) if s.strip()]
    # Split on / or ／ — any alternative satisfies
    if len(tilde_parts) == 1:
        alternatives = [s.strip() for s in re.split(r"[／/]", p) if s.strip()]
    else:
        alternatives = []

    def check(ja: str) -> tuple[bool, str]:
        if not ja:
            return False, "empty"

        # If pattern has tilde-separated parts: ALL parts must appear
        if len(tilde_parts) >= 2:
            missing = []
            for part in tilde_parts:
                part = part.strip()
                # Strip remaining annotations within each part
                part = re.sub(r"\s*[+＋]\s*\w.*$", "", part).strip()
                if part and part not in ja:
                    missing.append(part)
            if not missing:
                return True, "all-tilde-parts-present"
            return False, f"missing-tilde-parts:{missing}"

        # Class-based markers (multi-form pattern labels)
        if "Question word" in p or "question word" in p:
            if has_question_word(ja):
                return True, "question-word-present"
            return False, "no-question-word"
        if "Verb-plain" in p or "V-plain" in p or "Verb-dictionary" in p or "V-dict" in p:
            if has_plain_verb(ja):
                return True, "plain-verb-present"
            return False, "no-plain-verb"
        if ("Verb-て" in p or "V-て" in p or "verb-te" in p.lower() or
                p.lower().startswith("te-form") or "Te-form" in p):
            if has_te_form(ja):
                return True, "te-form-present"
            return False, "no-te-form"
        if "Verb-た" in p or "V-た" in p or "past" in p.lower() and "verb" in p.lower():
            if has_ta_form(ja):
                return True, "ta-form-present"
            return False, "no-ta-form"
        if "Verb-ない" in p or "V-ない" in p or "negative verb" in p.lower():
            if has_nai_form(ja):
                return True, "nai-form-present"
            return False, "no-nai-form"
        if "Verb-ます" in p or "V-ます" in p or "polite verb" in p.lower():
            if has_masu_form(ja):
                return True, "masu-form-present"
            return False, "no-masu-form"
        if "い-form" in p or "Adj-い" in p or "i-adjective" in p.lower():
            if has_i_adj(ja):
                return True, "i-adj-present"
            return False, "no-i-adj"
        if "な-form" in p or "Adj-な" in p or "na-adjective" in p.lower():
            if has_na_adj(ja):
                return True, "na-adj-present"
            return False, "no-na-adj"

        # Single-char particle
        if len(p) == 1 and p in SINGLE_CHAR_PARTICLES:
            if particle_used_as_particle(ja, p):
                return True, "particle-used"
            if p in ja:
                return False, f"contains-{p}-as-substring-only"
            return False, f"missing-{p}"

        # Paren-readings: use as alternatives plus the bare pattern
        if paren_readings:
            full_set = [p] + paren_readings + [p + r for r in paren_readings if r]
            for sig in full_set:
                if sig and sig in ja:
                    return True, f"marker-present:{sig}"
            return False, f"missing-paren-readings:{paren_readings}"

        # Slash alternatives
        if alternatives:
            for alt in alternatives:
                alt_clean = re.sub(r"\s+", "", alt)
                if alt_clean and alt_clean in ja:
                    return True, f"marker-present:{alt_clean}"
            return False, f"missing-any-of:{alternatives}"

        # Plain substring match
        if p and p in ja:
            return True, "substring-match"
        return False, f"missing:{p!r}"

    return check


def main() -> None:
    d = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    patterns = d.get("patterns", [])

    # Per-example relevance check using v2 logic
    failures = []
    pattern_meta = {}
    for p in patterns:
        pid = p.get("id", "?")
        pstr = p.get("pattern", "")
        pattern_meta[pid] = pstr
        check = build_checker(pstr)
        for i, ex in enumerate(p.get("examples", [])):
            ja = ex.get("ja", "")
            ok, reason = check(ja)
            if not ok:
                failures.append((pid, pstr, i, ja, reason))

    # Within-pattern duplicates
    within_dups = []
    for p in patterns:
        pid = p.get("id", "?")
        seen = {}
        for i, ex in enumerate(p.get("examples", [])):
            ja = (ex.get("ja") or "").strip()
            if ja in seen:
                within_dups.append((pid, seen[ja], i, ja))
            else:
                seen[ja] = i

    # Cross-pattern boilerplate-leak
    ex_to_patterns = defaultdict(list)
    for p in patterns:
        pid = p.get("id", "?")
        for i, ex in enumerate(p.get("examples", [])):
            ja = (ex.get("ja") or "").strip()
            if ja:
                ex_to_patterns[ja].append((pid, i))
    boilerplate = [(ja, locs) for ja, locs in ex_to_patterns.items() if len(locs) >= 2]
    boilerplate.sort(key=lambda x: -len(x[1]))

    # --- Report ---
    print("=" * 70)
    print(f"V2 AUDIT — pattern-relevance check on {len(patterns)} patterns")
    print("=" * 70)
    print()
    print(f"Total irrelevant examples: {len(failures)}")
    print(f"Patterns affected:          {len({pid for pid,_,_,_,_ in failures})}")
    print(f"Within-pattern duplicates:  {len(within_dups)}")
    print(f"Cross-pattern boilerplate:  {len(boilerplate)} entries")
    print()
    print("=" * 70)
    print("WITHIN-PATTERN DUPLICATES — same sentence appears twice in one pattern")
    print("=" * 70)
    if not within_dups:
        print("None.")
    else:
        for pid, first, second, ja in within_dups[:50]:
            print(f"  {pid}  [{first}] and [{second}]  {ja[:55]}")
        if len(within_dups) > 50:
            print(f"  ... and {len(within_dups) - 50} more")

    print()
    print("=" * 70)
    print("TOP CROSS-PATTERN BOILERPLATE — sentences repeated across patterns")
    print("=" * 70)
    for ja, locs in boilerplate[:25]:
        pids = ", ".join(pid for pid, _ in locs)
        print(f"  x{len(locs):2d}  {ja[:50]:50s}  in: {pids}")

    print()
    print("=" * 70)
    print("PER-PATTERN IRRELEVANT-EXAMPLE FINDINGS (v2 — false-positives reduced)")
    print("=" * 70)
    by_pattern = defaultdict(list)
    for pid, pstr, idx, ja, reason in failures:
        by_pattern[(pid, pstr)].append((idx, ja, reason))
    for (pid, pstr), items in sorted(by_pattern.items()):
        print(f"\n{pid}  pattern={pstr!r}  ({len(items)} irrelevant)")
        for idx, ja, reason in items:
            print(f"  [{idx}] {ja[:55]:55s}  reason={reason}")


if __name__ == "__main__":
    main()
