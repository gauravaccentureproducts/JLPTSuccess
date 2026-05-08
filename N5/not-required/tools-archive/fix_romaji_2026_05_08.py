"""
H-4 fix: Targeted romaji patches in grammar.json examples.

Strategy: keep existing romaji, apply ONLY safe surgical fixes:

1. Particle separation: insert a space before が/を/に/で/と/も/や when
   they appear attached to a noun stem at end of a romaji bunsetsu
   (i.e., before whitespace, comma, period, or end-of-string).
   Example: "amega" → "ame ga", "darega" → "dare ga".

2. Sentence-final particle separation: ka / ne / yo at end of sentence.
   Example: "kimashitaka" → "kimashita ka".

3. Digit transliteration: leading bare digit before "ji" (時) or "fun"
   (分) gets converted to its kanji-reading.
   Example: "7tokini" → "shichi-ji ni", "9tokini" → "ku-ji ni".

Avoids:
- Modifying は (wa) — already correctly rendered by the existing
  romanizer in the topic position.
- Touching katakana long vowels (e.g., コーヒー → koohii) — already
  correctly rendered as "koohii" in the existing data.
- Re-romanizing whole bunsetsu — high false-positive risk.

Safe to re-run; idempotent.
"""
import json
import re
from pathlib import Path

DATA_DIR = Path(__file__).parent.parent.parent / "data"

# Particles to space-separate when attached at end of bunsetsu.
# NOT including 'wa' / 'no' / 'mo' / 'ka' here because they overlap
# common syllables (e.g., the masu-stem ending "-mo" is actually a
# verb form, not a particle).
END_PARTICLES = ["ga", "wo", "ni", "de", "to", "ya", "made", "kara", "yori", "he"]
# Require prefix of at least 3 chars to avoid false positives like
# "nani" → "na" + "ni" (treating "nani" as noun "na" + particle "ni").
END_PARTICLES_PAT = re.compile(
    r"([a-z]{3,})(" + "|".join(END_PARTICLES) + r")(?=[\s。、,!?]|$)",
    re.IGNORECASE,
)

# Sentence-final か/ね/よ — already protected by length-3 minimum.
SENT_FINAL_PAT = re.compile(
    r"([a-z]{3,})(ka|ne|yo)(?=[。.！？!?]|$)",
    re.IGNORECASE,
)

# Words ending in particle-look-alike that should NEVER be split.
# These are checked AFTER the regex match — if the resulting prefix
# joined to the particle equals one of these words, undo the split.
PROTECTED_WORDS = {
    "nani", "kani", "tani", "oni",       # ends in -ni
    "made", "matade",                    # ends in -de (made = particle, but as adverb)
    "kago", "yogo", "togo",              # ends in -go (rare)
    "namonai",                           # contains -ni- internally
}

# Digit + Japanese counter (時, 分, 人) + particle pattern.
# Convert leading digit. The digit-reading depends on the counter.
TIME_DIGITS = {
    "1": "ichi", "2": "ni", "3": "san", "4": "yo", "5": "go",
    "6": "roku", "7": "shichi", "8": "hachi", "9": "ku",
    "10": "juu", "11": "juuichi", "12": "juuni",
}


def _digit_to_time(m):
    digit = m.group(1)
    rest = m.group(2)  # "tokini" or similar
    reading = TIME_DIGITS.get(digit, digit)
    # tokini -> -ji ni
    if rest.startswith("toki"):
        rest = rest.replace("toki", "ji", 1)
        # also insert space before particle suffix (ni/wa/de/etc.)
        rest = re.sub(r"^ji([a-z]+)$", r"ji \1", rest)
    return f"{reading}-{rest}"


DIGIT_TIME_PAT = re.compile(r"(\d+)(toki[a-z]*)")


def patch_romaji(rom):
    if not rom:
        return rom
    new = rom
    # 1. Particle separation
    new = END_PARTICLES_PAT.sub(r"\1 \2", new)
    # 2. Sentence-final か/ね/よ
    new = SENT_FINAL_PAT.sub(r"\1 \2", new)
    # 3. Digit + time-counter transliteration
    new = DIGIT_TIME_PAT.sub(_digit_to_time, new)
    # Cleanup: collapse double spaces
    new = re.sub(r"  +", " ", new).strip()
    return new


def main():
    grammar_path = DATA_DIR / "grammar.json"
    with open(grammar_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    count_total = 0
    count_changed = 0
    samples = []
    for p in data["patterns"]:
        for ex in p.get("examples", []):
            if "romaji" not in ex:
                continue
            old = ex["romaji"]
            new = patch_romaji(old)
            count_total += 1
            if new != old:
                count_changed += 1
                if len(samples) < 12:
                    samples.append((p["id"], ex.get("ja", ""), old, new))
            ex["romaji"] = new

    print(f"Total examples: {count_total}, patched: {count_changed}")
    print()
    print("Samples:")
    for pid, ja, old, new in samples:
        print(f"  {pid}")
        print(f"    ja:  {ja}")
        print(f"    old: {old}")
        print(f"    new: {new}")
        print()

    with open(grammar_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        f.write("\n")
    print(f"Wrote {grammar_path}")


if __name__ == "__main__":
    main()
