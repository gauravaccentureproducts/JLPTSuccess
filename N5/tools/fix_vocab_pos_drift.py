"""One-shot script: align KnowledgeBank/vocabulary_n5.md PoS tags to
data/vocab.json `pos` field, using the markdown's `##` section header
as a disambiguator for homographs.

JA-31 (added 2026-05-02) detected 69 drift cases between the two
files after the DEFER-5 PoS-injection pass. Root cause: the original
injection script used `setdefault(form, pos)` which picked the FIRST
JSON entry per form — wrong for homographs that appear in multiple
thematic sections (はる as noun-spring vs verb-stretch, ふく as
noun-clothes vs verb-blow, etc.).

This fix walks the markdown line-by-line, tracks the current `## N.
Section title` heading, and for each entry looks up the JSON record
by (form, reading, section). When the JSON's `section` matches the
heading, we use that entry's pos; otherwise we fall back to (form,
reading) with the heading as a tiebreaker via partial-match.

Run-once 2026-05-02 after JA-31 was added.
"""
import json
import re
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent

POS_ABBREV = {
    "noun": "n.", "verb-1": "v1", "verb-2": "v2", "verb-3": "v3",
    "i-adj": "i-adj", "na-adj": "na-adj", "adverb": "adv.",
    "particle": "part.", "conjunction": "conj.", "pronoun": "pron.",
    "counter": "count.", "numeral": "num.", "demonstrative": "dem.",
    "question-word": "Q-word", "expression": "exp.",
    "interjection": "interj.",
}
POS_TAGS = list(POS_ABBREV.values())
POS_TAGS_RE = "|".join(re.escape(t) for t in POS_TAGS)

vocab = json.load((ROOT / "data" / "vocab.json").open(encoding="utf-8"))

# Build lookup: (form, reading, section_normalized) → pos_tag.
# Also a (form, reading) → list of (section, tag) for homograph fallback.
def normalize_section(s: str) -> str:
    """Strip leading number + dot from section, lowercase, normalize whitespace.
    "1. People - Pronouns and Self" → "people - pronouns and self"
    """
    s = re.sub(r"^\d+\.\s*", "", s).strip().lower()
    return re.sub(r"\s+", " ", s)


by_full: dict[tuple[str, str, str], str] = {}
by_form_reading: dict[tuple[str, str], list[tuple[str, str]]] = {}
for e in vocab.get("entries", []):
    form = e.get("form")
    reading = e.get("reading", form)
    pos = e.get("pos")
    section = e.get("section", "")
    if not (form and pos):
        continue
    tag = POS_ABBREV.get(pos, pos)
    sec_norm = normalize_section(section)
    by_full[(form, reading, sec_norm)] = tag
    by_form_reading.setdefault((form, reading), []).append((sec_norm, tag))

LINE_RE = re.compile(
    r"^(- )([^\s\(]+)(\s+\(([^)]+)\))?( \[(?:Ext|Cul)\])?(\s*-\s*)"
    rf"\[({POS_TAGS_RE})\]\s+(.+)$"
)
SECTION_HEADER_RE = re.compile(r"^##\s+(.+?)\s*$")
is_jp = re.compile(r"^[ぁ-んァ-ヶー一-鿿]")

md_path = ROOT / "KnowledgeBank" / "vocabulary_n5.md"
text = md_path.read_text(encoding="utf-8")

current_section = ""
out_lines = []
fixed = 0
skipped = 0
for raw in text.splitlines(keepends=True):
    sh = SECTION_HEADER_RE.match(raw.rstrip("\n"))
    if sh:
        current_section = normalize_section(sh.group(1))
        out_lines.append(raw)
        continue

    m = LINE_RE.match(raw.rstrip("\n"))
    if not m:
        out_lines.append(raw)
        continue

    prefix, form, paren_full, reading_grp, tier_grp, sep, md_tag, gloss = m.groups()
    reading = reading_grp or form
    if not is_jp.match(form):
        out_lines.append(raw)
        continue

    # Lookup with section. Use exact match if available; else fall back
    # to (form, reading) with heading-similarity tiebreaker.
    expected = by_full.get((form, reading, current_section))
    if expected is None:
        # Heuristic: pick the JSON record whose section shares the most
        # words with the current heading. If only one record matches the
        # form-reading pair, use it directly.
        candidates = by_form_reading.get((form, reading), [])
        if len(candidates) == 1:
            expected = candidates[0][1]
        elif candidates:
            # Score each candidate by word-overlap with current section
            cur_words = set(current_section.split())
            best = None; best_score = -1
            for sec, tag in candidates:
                score = len(cur_words & set(sec.split()))
                if score > best_score:
                    best, best_score = tag, score
            expected = best

    if expected is None or md_tag == expected:
        out_lines.append(raw)
        continue

    # Rewrite the line with the corrected tag
    new_raw = (f"{prefix}{form}{paren_full or ''}{tier_grp or ''}"
               f"{sep}[{expected}] {gloss}\n")
    out_lines.append(new_raw)
    fixed += 1
    print(f"  line ?? '{form}' ({reading}) [{md_tag}] → [{expected}]  "
          f"section: '{current_section[:40]}'")

md_path.write_text("".join(out_lines), encoding="utf-8")
print(f"\nFixed {fixed} entries; {skipped} skipped.")
