"""Lint /data/grammar.json and /data/questions.json for non-N5 content.

Run from the repo root:
    python tools/lint_content.py

Two checks:
  1. Kanji scope     -- any kanji NOT on data/n5_kanji_whitelist.json (errors).
  2. Vocab scope     -- kanji-bearing word-tokens NOT in data/n5_vocab_whitelist.json
                       AND not derivable from a whitelist token by simple inflection
                       (warnings -- false positives are common without a real tokenizer).

Exits 0 even on warnings in this scaffold; promote to non-zero in CI when
content is finalized.

Spec reference: §4.7 (vocab whitelist) + §4.8 (kanji whitelist).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# A "kanji-bearing token" = at least one CJK char, optionally followed by hiragana/katakana.
# Captures e.g. 学生, 食べます, 読みました, 上手, 駅員さん.
KANJI_TOKEN_RE = re.compile(r"[一-鿿][぀-ゟ゠-ヿ一-鿿]*")
# Pure-kanji prefix of a token (used for "derivable from whitelist" check).
KANJI_PREFIX_RE = re.compile(r"^[一-鿿]+")


def collect_text(obj) -> list[str]:
    """Walk JSON and return all string values."""
    out = []
    if isinstance(obj, str):
        out.append(obj)
    elif isinstance(obj, dict):
        for v in obj.values():
            out.extend(collect_text(v))
    elif isinstance(obj, list):
        for v in obj:
            out.extend(collect_text(v))
    return out


def kanji_prefixes(whitelist: set[str]) -> set[str]:
    """Return the set of leading kanji-only stems from each whitelist entry.

    Example: '食べる' -> '食'; '上手' -> '上手'; 'あなた' -> '' (skipped).
    Allows token derivation: '食べます' / '食べました' / '食べません' will all
    match because their kanji prefix '食' matches '食べる' -> '食'.
    """
    prefixes = set()
    for entry in whitelist:
        m = KANJI_PREFIX_RE.match(entry)
        if m:
            prefixes.add(m.group(0))
    return prefixes


def main() -> int:
    kanji_path = ROOT / "data" / "n5_kanji_whitelist.json"
    vocab_path = ROOT / "data" / "n5_vocab_whitelist.json"

    if not kanji_path.exists() or not vocab_path.exists():
        print(
            "ERROR: data/n5_kanji_whitelist.json or n5_vocab_whitelist.json missing. "
            "Run: python tools/build_data.py",
            file=sys.stderr,
        )
        return 2

    kanji_whitelist = set(json.loads(kanji_path.read_text(encoding="utf-8")))
    vocab_whitelist = set(json.loads(vocab_path.read_text(encoding="utf-8")))
    vocab_prefixes = kanji_prefixes(vocab_whitelist)

    kanji_issues: dict[str, set[str]] = {}
    vocab_issues: dict[str, set[str]] = {}

    for fname in ("grammar.json", "questions.json"):
        path = ROOT / "data" / fname
        if not path.exists():
            continue
        data = json.loads(path.read_text(encoding="utf-8"))
        strings = collect_text(data)
        for s in strings:
            # Check 1 -- kanji scope.
            for ch in re.findall(r"[一-鿿]", s):
                if ch not in kanji_whitelist:
                    kanji_issues.setdefault(fname, set()).add(ch)
            # Check 2 -- vocab scope (kanji-bearing tokens).
            for token in KANJI_TOKEN_RE.findall(s):
                if token in vocab_whitelist:
                    continue
                # Tolerate inflections: token whose kanji prefix matches a known stem.
                m = KANJI_PREFIX_RE.match(token)
                stem = m.group(0) if m else ""
                if stem and stem in vocab_prefixes:
                    continue
                vocab_issues.setdefault(fname, set()).add(token)

    if not kanji_issues and not vocab_issues:
        print("OK: all kanji and vocab in scope (or no content yet)")
        return 0

    if kanji_issues:
        print("Out-of-scope kanji (FAIL -- must be on N5 whitelist or behind furigana):")
        for fname, chars in kanji_issues.items():
            print(f"  {fname}: {' '.join(sorted(chars))}")

    if vocab_issues:
        print("\nOut-of-scope vocab tokens (WARN -- may be false positives without tokenizer):")
        for fname, tokens in vocab_issues.items():
            shown = sorted(tokens)[:30]
            suffix = f" ... +{len(tokens) - 30} more" if len(tokens) > 30 else ""
            print(f"  {fname}: {' '.join(shown)}{suffix}")
        print(
            "\nVocab warnings are advisory -- the lint has no morphological analyzer, "
            "so compounds like '学校' may register against the standalone whitelist entry "
            "'学校' but '小学校' will warn. Review and silence by adding to whitelist or "
            "rewording in kana."
        )

    print("\nNote: scaffold runs warning-only -- exit 0 even on findings.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
