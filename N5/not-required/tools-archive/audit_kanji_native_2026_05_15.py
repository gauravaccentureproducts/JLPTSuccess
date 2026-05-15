"""Native-teacher accuracy audit of data/kanji.json.

CI already covers structural invariants (JA-12, JA-13, JA-16, JA-22,
JA-24, JA-76). This script targets content-quality gaps a native
teacher / experienced editor would flag.

  K1: Sentence with empty translation_en
  K2: Within-entry duplicate sentences
  K3: Sentence does not contain the target kanji (glyph or its reading)
  K4: examples (compounds) that don't contain the target kanji
  K5: Within-entry duplicate examples (same form twice)
  K6: Lookalike entries that are themselves OOS-of-N5 (whitelist)
  K7: Mnemonic field contains placeholder text
  K8: Stroke count missing / mismatch with stroke_order_summary
  K9: meanings field empty / missing
  K10: examples count too low (<2 — N5 deserves >=3)
  K11: sentences count zero
  K12: Cross-entry sentence boilerplate (same ja in 5+ kanji entries)
  K13: Translation contains Japanese characters (script leak)
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

KANJI = Path("data/kanji.json")

HIRA = re.compile(r"[぀-ゟ]")
KATA = re.compile(r"[゠-ヿ]")
HAN = re.compile(r"[一-鿿]")

PLACEHOLDER_PATTERNS = [
    re.compile(r"\bTODO\b", re.I),
    re.compile(r"\bTBD\b", re.I),
    re.compile(r"\bplaceholder\b", re.I),
    re.compile(r"\bfixme\b", re.I),
    re.compile(r"\bunspecified\b", re.I),
    re.compile(r"^\s*(\.\.\.|n/a|na)\s*$", re.I),
]


def is_placeholder(s: str) -> bool:
    return bool(s) and any(p.search(s) for p in PLACEHOLDER_PATTERNS)


def has_japanese(s: str) -> bool:
    return bool(HIRA.search(s) or KATA.search(s) or HAN.search(s))


def check_entry(entry: dict, all_whitelist: set) -> dict[str, list]:
    issues = defaultdict(list)
    glyph = entry.get("glyph", "")
    on_readings = entry.get("on", []) or []
    kun_readings = entry.get("kun", []) or []
    # Reading variants in hiragana (kun) and katakana converted to hira-or-original
    reading_alternants = set()
    for r in kun_readings:
        if isinstance(r, str):
            reading_alternants.add(r)
            # i-adj-style readings often end in -い; the stem is what appears
            reading_alternants.add(r.rstrip("いるくつぶむすぐぬ"))
    # Katakana on-yomi: convert to hiragana for matching against kun-style
    for r in on_readings:
        if isinstance(r, str):
            hira = "".join(chr(ord(c) - 0x60) if "ァ" <= c <= "ヶ" else c for c in r)
            reading_alternants.add(hira)
    # Also accept rendaku variants of kun (はな→ばな, etc.) — too noisy to
    # enumerate here; rely on KANJI substring as primary match.

    # K1 / K2 / K3 / K13: sentences
    sentences = entry.get("sentences", []) or []
    sentence_ja_seen = {}
    for i, s in enumerate(sentences):
        ja = (s.get("ja") or "").strip()
        en = (s.get("translation_en") or "").strip()
        if not ja:
            continue
        if not en:
            issues["K1-EMPTY-TRANSLATION"].append((i, ja))
        if ja in sentence_ja_seen:
            issues["K2-DUP-SENTENCE"].append(
                (sentence_ja_seen[ja], i, ja)
            )
        else:
            sentence_ja_seen[ja] = i
        # K3: does the sentence contain the target kanji glyph or any reading?
        if glyph and glyph not in ja:
            # Accept if any reading-alternant appears
            if not any(r and r in ja for r in reading_alternants):
                issues["K3-NO-KANJI-OR-READING-IN-SENTENCE"].append(
                    (i, glyph, ja)
                )
        # K13: Japanese leaking into the English translation
        if en and has_japanese(re.sub(r"\([^)]*\)", "", en)):
            issues["K13-JA-LEAK-IN-EN"].append((i, en))

    # K11: zero sentences
    if not sentences:
        issues["K11-NO-SENTENCES"].append(glyph)

    # K4 / K5: examples (compounds)
    # K5 dup logic: same form is fine when the readings differ (e.g.
    # 十 / じゅう and 十 / とお; 人 / ひと and 人 / にん). Flag only if
    # both form AND reading match.
    examples = entry.get("examples", []) or []
    seen: dict[tuple[str, str], int] = {}
    for i, ex in enumerate(examples):
        form = (ex.get("form") or "").strip()
        reading = (ex.get("reading") or "").strip()
        if not form:
            continue
        if glyph and glyph not in form:
            issues["K4-KANJI-NOT-IN-COMPOUND-FORM"].append((i, glyph, form))
        key = (form, reading)
        if key in seen:
            issues["K5-DUP-COMPOUND"].append(
                (seen[key], i, form, reading)
            )
        else:
            seen[key] = i
    # K10: thin examples
    if len(examples) < 2:
        issues["K10-THIN-EXAMPLES"].append((glyph, len(examples)))

    # K6: lookalikes pointing outside N5 whitelist
    lookalikes = entry.get("lookalikes", []) or []
    for la in lookalikes:
        if isinstance(la, dict):
            la_glyph = la.get("glyph") or la.get("kanji") or ""
        else:
            la_glyph = la
        if la_glyph and la_glyph not in all_whitelist:
            issues["K6-LOOKALIKE-OOS"].append((glyph, la_glyph))

    # K7: mnemonic with placeholder text
    mnem = entry.get("mnemonic")
    if isinstance(mnem, dict):
        for k, v in mnem.items():
            if k in ("provenance",):
                continue
            if isinstance(v, str) and is_placeholder(v):
                issues["K7-MNEMONIC-PLACEHOLDER"].append(
                    (glyph, k, v[:80])
                )

    # K8: stroke_count missing / suspicious
    sc = entry.get("stroke_count")
    if sc is None or (isinstance(sc, int) and sc <= 0):
        issues["K8-STROKE-COUNT-MISSING"].append(glyph)
    # Cross-check with stroke_order_trap text mentioning stroke total
    sot = entry.get("stroke_order_trap") or {}
    why = (sot.get("why_it_matters") or "") if isinstance(sot, dict) else ""
    if sc and why:
        m = re.search(r"(\d+)\s*stroke", why)
        if m:
            claimed = int(m.group(1))
            if claimed != sc:
                issues["K8-STROKE-COUNT-MISMATCH"].append(
                    (glyph, sc, claimed, why[:60])
                )

    # K9: meanings empty
    meanings = entry.get("meanings", []) or []
    if not meanings or not any(m for m in meanings if isinstance(m, str) and m.strip()):
        issues["K9-MEANINGS-EMPTY"].append(glyph)

    # K14: mnemonic field structure — all 4 sub-fields present + non-trivial
    mnem = entry.get("mnemonic")
    if isinstance(mnem, dict):
        for sub in ("summary", "visual", "reading", "meaning"):
            v = mnem.get(sub, "")
            if not isinstance(v, str) or len(v.strip()) < 10:
                issues["K14-MNEMONIC-THIN"].append((glyph, sub, v[:40] if isinstance(v,str) else type(v).__name__))
    elif mnem is None:
        issues["K14-MNEMONIC-MISSING"].append(glyph)

    # K15: stroke_order_trap fields all filled
    sot = entry.get("stroke_order_trap")
    if isinstance(sot, dict):
        for sub in ("trap", "correct_order_summary", "why_it_matters"):
            v = sot.get(sub, "")
            if not isinstance(v, str) or len(v.strip()) < 10:
                issues["K15-TRAP-THIN"].append((glyph, sub, v[:40] if isinstance(v,str) else type(v).__name__))

    # K16: meanings_hi present + same cardinality as meanings (ideally)
    mhi = entry.get("meanings_hi", []) or []
    if not mhi:
        issues["K16-MEANINGS-HI-MISSING"].append(glyph)

    # K17: lookalikes structure — should be glyphs that exist in N5 whitelist
    # (already partially K6 — but K17 also catches missing rationale)
    lookalikes = entry.get("lookalikes", []) or []
    for la in lookalikes:
        if isinstance(la, dict):
            # If dict, expect 'glyph' + 'why' / 'reason' fields
            if not la.get("why") and not la.get("reason"):
                pass  # rationale fields are optional in current schema
        elif not isinstance(la, str):
            issues["K17-LOOKALIKE-MALFORMED"].append((glyph, type(la).__name__, repr(la)[:40]))

    # K18: n5_compounds cross-validation (each compound should be a real word)
    # Skipping vocab.json cross-ref here — too expensive; defer to a JA-XX
    # check.

    # K19: HTML markup in `ja` field — typically only intended for highlighting
    # but can leak past sanitization. Flag <u>/</u> as a notable presence
    # (often legitimate but worth surfacing for review).
    for i, s in enumerate(entry.get("sentences", []) or []):
        ja = (s.get("ja") or "")
        if "<u>" in ja or "</u>" in ja:
            issues["K19-HTML-IN-SENTENCE-JA"].append((i, ja[:60]))

    # K20: sentence has fill-in-the-blank `（　　）` — fine for mock-test
    # items but the translation should reflect that it's a test fragment
    for i, s in enumerate(entry.get("sentences", []) or []):
        ja = (s.get("ja") or "")
        en = (s.get("translation_en") or "")
        if "（　" in ja or "（ 　" in ja:
            if "(" not in en and "blank" not in en.lower():
                issues["K20-BLANK-NOT-IN-TRANSLATION"].append((i, ja[:60], en[:60]))

    # K21: stroke_count out of plausible range (1-30 covers all real kanji)
    sc = entry.get("stroke_count")
    if isinstance(sc, int) and (sc < 1 or sc > 30):
        issues["K21-STROKE-COUNT-OUT-OF-RANGE"].append((glyph, sc))

    # K22: examples count = 0 (very thin)
    if not examples:
        issues["K22-NO-EXAMPLES"].append(glyph)

    # K23: meanings_hi cardinality vs meanings (loose check: should have at
    # least 1 if meanings has any)
    if meanings and not mhi:
        issues["K23-MEANINGS-HI-MISSING-VS-EN"].append(glyph)

    # K24: meanings_hi contains non-Devanagari characters (Hindi expected)
    DEVANAGARI = re.compile(r"[ऀ-ॿ]")
    if isinstance(mhi, list):
        for j, m in enumerate(mhi):
            if isinstance(m, str) and m.strip() and not DEVANAGARI.search(m):
                # Permit parenthetical English clarifications like "(noun)"
                if not re.fullmatch(r"[A-Za-z0-9\s\(\),.\-]+", m):
                    issues["K24-MEANINGS-HI-SCRIPT-LEAK"].append((glyph, j, m[:40]))
                else:
                    issues["K24-MEANINGS-HI-NO-DEVANAGARI"].append((glyph, j, m[:40]))

    # K25: reading_rule missing / trivially short
    rr = entry.get("reading_rule")
    if rr is None or (isinstance(rr, str) and len(rr.strip()) < 20):
        issues["K25-READING-RULE-MISSING-OR-THIN"].append((glyph, str(rr)[:40]))

    # K26: etymology missing / thin (etymology should have origin_type + story)
    et = entry.get("etymology")
    if et is None:
        issues["K26-ETYMOLOGY-MISSING"].append(glyph)
    elif isinstance(et, dict):
        story = et.get("story", "")
        if not isinstance(story, str) or len(story.strip()) < 15:
            issues["K26-ETYMOLOGY-STORY-THIN"].append((glyph, story[:40] if isinstance(story,str) else type(story).__name__))

    # K27: on_kun_pair_drill missing / thin
    okp = entry.get("on_kun_pair_drill")
    if okp is None:
        issues["K27-ON-KUN-DRILL-MISSING"].append(glyph)

    # K28: examples reading mismatches form's morphological structure
    # (sanity: reading should be hiragana/katakana, not raw English)
    for i, ex in enumerate(examples):
        reading = (ex.get("reading") or "").strip()
        if reading and not re.fullmatch(r"[぀-ヿ ／/]+", reading):
            # Allow rendaku-marker forms like 'ふん / ぷん'
            issues["K28-EXAMPLE-READING-SCRIPT-LEAK"].append((i, reading[:30]))

    # K29: HTML entity leakage in any user-facing string field
    ENTITY_RX = re.compile(r"&(amp|lt|gt|quot|apos|#\d+);")
    USER_FACING_FIELDS = ("meanings", "meanings_hi", "primary_reading")
    for field in USER_FACING_FIELDS:
        v = entry.get(field)
        if isinstance(v, list):
            for j, item in enumerate(v):
                if isinstance(item, str) and ENTITY_RX.search(item):
                    issues["K29-HTML-ENTITY-LEAK"].append((glyph, field, j, item[:40]))
        elif isinstance(v, str) and ENTITY_RX.search(v):
            issues["K29-HTML-ENTITY-LEAK"].append((glyph, field, None, v[:40]))
    # Also check sentence ja + translation
    for i, s in enumerate(entry.get("sentences", []) or []):
        for field in ("ja", "translation_en"):
            v = s.get(field, "")
            if isinstance(v, str) and ENTITY_RX.search(v):
                issues["K29-HTML-ENTITY-LEAK"].append(
                    (glyph, f"sentences[{i}].{field}", None, v[:40])
                )

    # K30: meanings field contains Japanese characters (script leak — should
    # be English only)
    for j, m in enumerate(meanings):
        if isinstance(m, str) and has_japanese(m):
            issues["K30-MEANINGS-JA-LEAK"].append((glyph, j, m[:40]))

    return dict(issues)


def main():
    print("Loading kanji.json...")
    d = json.loads(KANJI.read_text(encoding="utf-8"))
    entries = d["entries"]
    print(f"Total entries: {len(entries)}\n")

    whitelist = {e.get("glyph", "") for e in entries if e.get("glyph")}

    all_findings: dict[str, list] = defaultdict(list)
    cross_entry_ja: Counter[str] = Counter()

    for entry in entries:
        issues = check_entry(entry, whitelist)
        for cat, rows in issues.items():
            all_findings[cat].extend(
                (entry.get("glyph"), row) for row in rows
            )
        for s in entry.get("sentences", []) or []:
            ja = (s.get("ja") or "").strip()
            if ja:
                cross_entry_ja[ja] += 1

    # K12: cross-entry sentence boilerplate
    boilerplate = [(ja, n) for ja, n in cross_entry_ja.items() if n >= 5]
    boilerplate.sort(key=lambda x: -x[1])

    # Report
    def header(title, count):
        print("=" * 72)
        print(f"{title} ({count})")
        print("=" * 72)

    show_first = 30
    for cat in sorted(all_findings):
        rows = all_findings[cat]
        header(cat, len(rows))
        for glyph, row in rows[:show_first]:
            print(f"  {glyph}  {row}")
        if len(rows) > show_first:
            print(f"  ... and {len(rows)-show_first} more")
        print()

    header("K12-CROSS-ENTRY-BOILERPLATE (ja shared by >=5 entries)",
           len(boilerplate))
    for ja, n in boilerplate[:30]:
        print(f"  {n:3d}x  {ja!r}")
    print()

    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    for cat in sorted(all_findings):
        print(f"  {cat:40s} {len(all_findings[cat])}")
    print(f"  {'K12-CROSS-ENTRY-BOILERPLATE':40s} {len(boilerplate)}")


if __name__ == "__main__":
    main()
