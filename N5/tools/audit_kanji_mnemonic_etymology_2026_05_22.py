"""Audit all 106 kanji mnemonics for etymology-conflation patterns
(per native-teacher review §4 item 5 — cohort sweep after 三 fix).

The 三 case was: "さん — borrowed everywhere from 'Mr/Ms' (-さん) to
三月..." — implied the kanji's reading SOURCES the honorific. False:
the honorific さん derives from 様 → さま → さん, separate root.

Pattern signals to flag:
  - "borrowed", "from", "comes from", "source of", "derives from"
  - "same as" + honorific/particle/word with the same kana
  - "(-NN)" parenthetical honorific patterns
  - Cross-reference claims between the kanji's reading and unrelated
    homophonic words

Output: per-kanji findings + suggested softer rewrites.
"""
import sys, io, json, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Phrasing patterns that often signal false-etymology claims
ETYMOLOGY_FLAGS = [
    r"borrowed everywhere",
    r"borrowed from",
    r"from\s+['\"]?Mr/Ms",
    r"comes from\s+the honorific",
    r"same\s+(root|origin|source)\s+as",
    r"derived\s+from",
    r"derives\s+from",
    r"etymological",
    r"-\s*さん\b",       # explicit honorific cross-reference (in non-三 entries)
    r"-\s*さま\b",
    r"the honorific\s+",
    r"shares?\s+(root|etymology|origin)\s+with",
    r"shared\s+root",
]

ETYMOLOGY_RE = re.compile("|".join(ETYMOLOGY_FLAGS), re.IGNORECASE)


def main():
    fp = os.path.join(REPO_N5, "data", "kanji.json")
    with open(fp, "r", encoding="utf-8") as f:
        kd = json.load(f)
    kl = kd.get("entries", kd if isinstance(kd, list) else kd.get("kanji", []))

    flagged = []
    total = 0
    for entry in kl:
        if not isinstance(entry, dict):
            continue
        total += 1
        glyph = entry.get("glyph") or entry.get("kanji") or "?"
        mn = entry.get("mnemonic") or {}
        if not isinstance(mn, dict):
            continue
        # Check each mnemonic sub-field
        for field in ("reading", "summary", "visual", "meaning"):
            text = mn.get(field, "") or ""
            if not text:
                continue
            matches = ETYMOLOGY_RE.findall(text)
            if matches:
                flagged.append({
                    "glyph": glyph,
                    "field": field,
                    "text": text,
                    "matched_phrases": matches,
                })

    print(f"=== Audited {total} kanji mnemonics ===")
    print(f"Flagged {len(flagged)} mnemonic fields with potential etymology-claim phrasings:")
    print()
    for f in flagged:
        print(f"  {f['glyph']} . mnemonic.{f['field']}:")
        print(f"    matched: {f['matched_phrases']}")
        print(f"    text: {f['text'][:200]!r}")
        print()


if __name__ == "__main__":
    main()
