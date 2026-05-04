"""Tag every entry in data/vocab.json with a `pos` (part-of-speech) field.

Per data-correction brief §4.6: vocab schema lacked POS info, so the app
couldn't filter (e.g., "show only verbs") or generate inflection drills
automatically. This script populates `pos` on every entry in-place.

Strategy: section-name heuristic. The vocab corpus is already organised
into 40 thematic sections (e.g., "27. Verbs - Group 1 (う-verbs)"), and
~95% of entries can be classified directly from their section. The
remaining ~5% (mixed-content sections, e.g. "Misc Useful Items") get a
gloss-based fallback heuristic.

POS values used (keep this list in sync with the schema spec):
    noun, i-adj, na-adj, verb-1, verb-2, verb-3, adverb, particle,
    conjunction, interjection, pronoun, counter, numeral,
    demonstrative, question-word, expression

Run:
    python tools/tag_vocab_pos.py

Idempotent: re-running on already-tagged data overwrites with the same
heuristic result. To force re-classification across all entries even when
already tagged, just delete `pos` first.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "vocab.json"


# Section-name → POS. Match by lowercase substring; first match wins.
SECTION_RULES = [
    ("verbs - group 1",          "verb-1"),
    ("verbs - group 2",          "verb-2"),
    ("verbs - irregular",        "verb-3"),
    ("verbs - existence",        "verb-1"),  # ある/いる class
    ("い-adjectives",            "i-adj"),
    ("な-adjectives",            "na-adj"),
    ("adverbs",                  "adverb"),
    ("particles",                "particle"),
    ("conjunctions",             "conjunction"),
    ("interjections",            "interjection"),
    ("function / filler",        "expression"),
    ("greetings and set",        "expression"),
    ("pronouns and self",        "pronoun"),
    ("question words",           "question-word"),
    ("demonstratives",           "demonstrative"),
    ("numbers",                  "numeral"),
    ("counters",                 "counter"),
    ("native counters",          "counter"),
    ("sounds and voice",         "interjection"),
]


def section_pos(section: str) -> str | None:
    s = section.lower()
    for needle, pos in SECTION_RULES:
        if needle in s:
            return pos
    return None


# Gloss-based fallbacks for entries whose section doesn't directly imply POS
# (e.g., "Common Nouns - Miscellaneous" which is mostly nouns but can have
# stragglers).
GLOSS_VERB_RE = re.compile(r"^to\s+\w+", re.IGNORECASE)
GLOSS_I_ADJ_RE = re.compile(r"\(i-adj")
GLOSS_NA_ADJ_RE = re.compile(r"\(na-adj")


def gloss_pos(form: str, reading: str | None, gloss: str) -> str:
    g = gloss.lower()
    if GLOSS_I_ADJ_RE.search(g):
        return "i-adj"
    if GLOSS_NA_ADJ_RE.search(g):
        return "na-adj"
    if GLOSS_VERB_RE.match(g):
        # "to know (Group 1 ...)" etc. — distinguish via gloss markers if present
        if "group 1" in g or "godan" in g or "u-verb" in g:
            return "verb-1"
        if "group 2" in g or "ichidan" in g or "ru-verb" in g:
            return "verb-2"
        if "irregular" in g or "する" in form:
            return "verb-3"
        # Default verb without explicit group: try form-shape heuristic.
        if (reading or form).endswith("する"):
            return "verb-3"
        if (reading or form).endswith("る"):
            return "verb-2"  # weak guess; many Group-1 also end in る (the
            # Pass-9 audit warned about this — but at the bulk level, ru-verb
            # is the more frequent guess)
        return "verb-1"
    # Default: noun (the safe bet for "miscellaneous" sections)
    return "noun"


def classify(entry: dict) -> str:
    section_p = section_pos(entry.get("section", ""))
    if section_p:
        return section_p
    return gloss_pos(entry.get("form", ""), entry.get("reading"),
                     entry.get("gloss", ""))


def main() -> int:
    data = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = data["entries"]

    counts: dict[str, int] = {}
    for e in entries:
        e["pos"] = classify(e)
        counts[e["pos"]] = counts.get(e["pos"], 0) + 1

    VOCAB.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Tagged {len(entries)} entries.")
    for pos, n in sorted(counts.items(), key=lambda kv: -kv[1]):
        print(f"  {pos:<14s} {n:>4d}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
