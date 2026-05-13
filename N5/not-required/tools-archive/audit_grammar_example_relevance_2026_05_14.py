"""Audit grammar.json examples for pattern-relevance.

Two failure modes detected:
1. Example doesn't contain the pattern's marker at all
   (e.g. "じぶんで しゅくだいを します" on the と-particle page).
2. Example contains the marker only as a substring of an unrelated
   word (e.g. と in とけい "watch" on the と-particle page —
   particle と is meant, not the noun-internal と).
3. Same example sentence repeated across many patterns (boilerplate
   leak — a smell indicator).

Output: a structured report with per-pattern findings + a smell
summary, suitable for fix-pass triage.

Run from N5/ root:
    python -X utf8 not-required/tools-archive/audit_grammar_example_relevance_2026_05_14.py
"""
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

GRAMMAR = Path("data/grammar.json")

# Single-character particles that often false-positive on noun-internal hits.
# We treat these specially: the particle must appear preceded by a likely
# noun-ending character (kana, kanji) AND followed by a likely verb/adjective/
# clause-internal character (kana, kanji, or end-of-sentence punctuation).
SINGLE_CHAR_PARTICLES = set("をにへでとがはのもや")

# Distinctive trailing forms that distinguish particles from noun-internal use.
# For each particle, what tokens commonly FOLLOW the particle in N5 example
# sentences? If we see the particle followed by one of these, it's almost
# certainly being used as a particle, not buried in a noun.
PARTICLE_TRAILING = {
    "と": [" ", "いき", "いっ", "いい", "あいま", "はな", "話", "行", "言",
            "思", "見", "会", "や", "かい", "それ"],
    "を": [" ", "し", "見", "読", "書", "た", "の"],
    "に": [" ", "いき", "あ", "あい", "つ", "もら", "教", "見", "行"],
    "へ": [" ", "いき", "行"],
    "で": [" ", "し", "あ", "なに", "何", "じ"],
    "が": [" ", "あり", "い", "ほし", "好", "わかり"],
    "は": [" ", "なん", "なに", "どこ", "どう", "あり", "い", "に"],
    "の": [" ", "うえ", "した", "なか", "前", "後", "上", "下"],
    "も": [" ", "あり", "い", "ほし", "た", "好"],
    "や": [" ", "りんご"],
}


def particle_used_as_particle(text: str, particle: str) -> bool:
    """Heuristic: does `particle` appear as a particle in `text` (not buried
    inside a noun like とけい / となり / にちようび / でんしゃ)?"""
    if particle not in text:
        return False
    # Find all occurrences and test each one.
    trailing = PARTICLE_TRAILING.get(particle, [" "])
    for m in re.finditer(re.escape(particle), text):
        end = m.end()
        # Check what follows: a space, end-of-sentence, or any of the
        # particle-typical trailing tokens.
        if end >= len(text):
            return True  # particle at end-of-string is unusual but valid
        rest = text[end:end + 4]
        if rest.startswith(("。", "、", "?", "？", "!", "！")):
            return True
        if any(rest.startswith(t) for t in trailing):
            return True
        # Strong signal: preceded by kanji + space (bunsetsu boundary).
        start = m.start()
        if start > 0:
            prev = text[start - 1]
            if prev == " ":
                # Space-preceded particle is almost certainly a particle.
                return True
    return False


def example_demonstrates(pattern: str, ja: str) -> tuple[bool, str]:
    """Return (is_relevant, reason). Heuristic-based — false positives possible
    for complex patterns (e.g. 〜たい conjugations don't surface the literal
    string 'たい' on the i-stem)."""
    if not pattern or not ja:
        return False, "empty"
    p = pattern.strip()

    # Single-char particle: stricter check
    if len(p) == 1 and p in SINGLE_CHAR_PARTICLES:
        if particle_used_as_particle(ja, p):
            return True, "particle-used-as-particle"
        if p in ja:
            return False, f"contains-{p}-as-noun-internal-substring-only"
        return False, f"missing-{p}-particle"

    # Compound patterns (multi-char): substring match.
    # Strip 〜 (placeholder for verb/adjective stems) and split on ／ / "/"
    # so multi-marker patterns (これ／それ／あれ／どれ, V-ます／V-ません) match
    # if ANY alternative appears in the example.
    core = p.replace("〜", "").replace("~", "").strip()
    # Strip parenthetical reading hints like "何（なに／なん）" → "何"
    core = re.sub(r"（[^）]*）", "", core)
    core = re.sub(r"\([^)]*\)", "", core)
    # Strip "+ N (noun)" / "+ verb" trailing annotations
    core = re.sub(r"\s*[+＋]\s*\w.*$", "", core).strip()
    # Split on ／ or / for alternatives
    alternatives = [a.strip() for a in re.split(r"[／/]", core) if a.strip()]
    if not alternatives:
        return False, "empty-marker-after-normalisation"
    for alt in alternatives:
        # If the alternative itself contains parenthetical, strip again
        alt_clean = re.sub(r"（[^）]*）|\([^)]*\)", "", alt).strip()
        if alt_clean and alt_clean in ja:
            return True, f"marker-present:{alt_clean}"
        # Try the raw alternative (with kanji+reading bundle)
        if alt and alt in ja:
            return True, f"marker-present:{alt}"
    return False, f"missing-any-of-{alternatives}"


def main() -> None:
    d = json.loads(GRAMMAR.read_text(encoding="utf-8"))
    patterns = d.get("patterns", [])

    # 1. Per-example relevance check
    failures = []  # list of (pattern_id, pattern_str, ex_idx, ja, reason)
    for p in patterns:
        pid = p.get("id", "?")
        pstr = p.get("pattern", "")
        for i, ex in enumerate(p.get("examples", [])):
            ja = ex.get("ja", "")
            ok, reason = example_demonstrates(pstr, ja)
            if not ok:
                failures.append((pid, pstr, i, ja, reason))

    # 2. Boilerplate-leak check: examples appearing in multiple patterns
    ex_counter = Counter()
    ex_to_patterns = defaultdict(list)
    for p in patterns:
        pid = p.get("id", "?")
        for ex in p.get("examples", []):
            ja = ex.get("ja", "").strip()
            if ja:
                ex_counter[ja] += 1
                ex_to_patterns[ja].append(pid)
    boilerplate = [(ja, cnt, ex_to_patterns[ja]) for ja, cnt in ex_counter.most_common() if cnt >= 2]

    # --- Report ---
    print("=" * 70)
    print("PER-EXAMPLE RELEVANCE — examples that don't demonstrate the pattern")
    print("=" * 70)
    if not failures:
        print("No failures.")
    else:
        # Group by pattern
        by_pattern = defaultdict(list)
        for fid, pstr, idx, ja, reason in failures:
            by_pattern[(fid, pstr)].append((idx, ja, reason))
        for (pid, pstr), items in sorted(by_pattern.items()):
            print(f"\n{pid}  pattern={pstr!r}  ({len(items)} irrelevant example(s))")
            for idx, ja, reason in items:
                print(f"  [{idx}] {ja[:55]:55s}  reason={reason}")
    print()
    print(f"Total irrelevant examples: {len(failures)}")
    print(f"Patterns affected:          {len({(fid, pstr) for fid, pstr, _, _, _ in failures})}")

    print()
    print("=" * 70)
    print(f"BOILERPLATE-LEAK — examples repeated across ≥2 patterns ({len(boilerplate)} total)")
    print("=" * 70)
    for ja, cnt, pids in boilerplate[:30]:
        print(f"  x{cnt}  {ja[:50]:50s}  in: {', '.join(pids)}")
    if len(boilerplate) > 30:
        print(f"  ... and {len(boilerplate) - 30} more")


if __name__ == "__main__":
    main()
