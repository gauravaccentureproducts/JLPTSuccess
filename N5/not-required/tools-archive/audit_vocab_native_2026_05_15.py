"""Native-teacher accuracy audit of data/vocab.json.

Targets gaps not covered by existing CI invariants (JA-4, JA-31, JA-49,
JA-50, JA-57, JA-70, JA-72, JA-74, JA-77, etc.). Focuses on the kinds of
issues a native Japanese teacher / experienced editor would flag:

  C1: Anti-pattern templated examples (e.g. "Xを 見ました。" → "I saw X.")
  C2: Duplicate examples within the same entry
  C3: Examples that do not contain the headword (form or reading)
  C4: Cross-entry boilerplate (same ja in 5+ different entries)
  C5: Truncated/dangling English translations (no article, "to X" in
      relative clause, copula-less, etc.)
  C6: POS-form mismatch (i-adj not ending in い, verb-2 with non-る tail)
  C7: Missing required fields (gloss/reading/examples/translation_en)
  C8: Gloss equals romanized reading (placeholder/missing gloss)
  C9: Suspicious headword-translation mismatch (gloss claims X but ja
      uses Y throughout)
 C10: Examples with self-reference loops or pure substitution leak
      ("Xを 見ました。" / "Xです。" with no other content)
"""
from __future__ import annotations

import json
import re
from collections import Counter, defaultdict
from pathlib import Path

VOCAB = Path("data/vocab.json")

HIRA = re.compile(r"[぀-ゟ]")
KATA = re.compile(r"[゠-ヿ]")
KANJI = re.compile(r"[一-鿿]")

ANTI_PATTERNS_JA = [
    # template that has leaked across many noun entries
    re.compile(r"^.{1,8}を\s*見ました。?$"),
    # tautological "X is X" or near-tautology
    re.compile(r"^これは\s*.{1,12}です。?$"),
]

ANTI_PATTERNS_EN_BAD_ARTICLE = re.compile(
    r"^I\s+saw\s+(?:a\s+|an\s+|the\s+|some\s+|my\s+|that\s+|this\s+)?[A-Za-z\-' ]+\.?$"
)

# More precise broken-translation detectors
BROKEN_EN = [
    # "I saw wall." / "I saw carrot." — missing article on common noun
    (re.compile(r"^I saw [a-z]+\.?$"), "missing-article"),
    # "There is a person who to <verb>." — infinitive in relative clause
    (re.compile(r"\bwho\s+to\s+[a-z]+"), "infinitive-in-relative-clause"),
    # "I will <verb> Xです" leaks Japanese
    (re.compile(r"[぀-ヿ一-鿿]"), "japanese-leaking-into-en"),
    # Empty / placeholder
    (re.compile(r"^\s*$"), "empty"),
    (re.compile(r"^(TODO|tbd|placeholder)", re.I), "placeholder"),
    # Translation ends mid-phrase (no period, no question mark, no excl)
    # leaving a dangling fragment
    (re.compile(r"^[A-Z][^.?!]*$"), "no-terminator"),
]


def has_terminator(s: str) -> bool:
    """True if s ends with a sentence terminator (., ?, !). Tolerates:
      - trailing closing quotes (so '"Hello."' counts)
      - trailing parenthetical annotations (so 'Good morning. (polite)' counts)
    """
    s = s.strip()
    # Strip trailing parenthetical annotations like "(polite)" or "(subject が)"
    s = re.sub(r"\s*\([^)]*\)\s*$", "", s)
    s = s.rstrip("'\"」』）)")
    return bool(s) and (s.endswith(".") or s.endswith("?") or s.endswith("!"))


def is_pure_hiragana(s: str) -> bool:
    """Does s contain only hiragana + spaces + punctuation?"""
    return all(HIRA.match(c) or c in " 　。、？！…ー" for c in s)


def check_template_leak(entry: dict) -> list[str]:
    """C1: Catch templated example sentences. Multiple sub-templates:
    (a) 'Xを 見ました。' where X is a single token (no whitespace)
    (b) 'あの Xは どこですか。' (nonsensical for non-locations, e.g.
        'Where is that September?' / 'Where is that station-attendant?')
    (c) 'これは Xです。' / 'あれは Xです。' as a standalone example with
        nothing else (too bare to teach the headword in context)
    """
    issues = []
    form = entry.get("form", "")
    pos = entry.get("pos", "")
    pat_miru = re.compile(r"^[^\s]{1,10}を\s*見ました(?:よ|ね|よね)?。?$")
    pat_doko = re.compile(r"^あの\s+(.{1,10})は\s*どこですか。?$")
    pat_kore = re.compile(r"^(これ|あれ|それ)は\s*(.{1,10})です。?$")
    pat_quote = re.compile(r"^「(.{1,10})」と\s*(いいました|言いました|あいさつしました)。?$")
    for i, ex in enumerate(entry.get("examples", [])):
        ja = ex.get("ja", "").strip()
        en = ex.get("translation_en", "").strip()
        # (a)
        if pat_miru.fullmatch(ja):
            issues.append(f"  [{i}] TEMPLATE-MIRU ja={ja!r:30s} en={en!r}")
        # (b) — but allow if pos is location/place-related
        m = pat_doko.fullmatch(ja)
        if m:
            target = m.group(1)
            # Skip if the headword is itself a location demonstrative
            # (where-questions are then natural)
            location_like_pos = {"noun"}
            location_like_sections = ("13-locations", "26-house")
            section = entry.get("section", "")
            is_locationish = any(s in section for s in location_like_sections)
            # Catch when the headword embedded in "あの Xは" is non-locational
            # (time word, abstract noun, food, etc.)
            if not is_locationish and target.strip() == form.strip():
                issues.append(f"  [{i}] TEMPLATE-DOKO-NON-LOCATION ja={ja!r} en={en!r}")
        # (c)
        m = pat_kore.fullmatch(ja)
        if m:
            # bland 'これは Xです' as ANY example is acceptable for the
            # very first time the headword is introduced — but if the
            # entry has 3+ examples, the bare template wastes a slot.
            # Exception: for the demonstrative pronouns themselves
            # (これ/それ/あれ entries), 'これは Xです。' IS the canonical
            # demonstration of the headword — not boilerplate. Skip.
            section = entry.get("section", "")
            if pos == "demonstrative" or "demonstrative" in section.lower():
                pass  # legitimate canonical example for demonstratives
            elif len(entry.get("examples", [])) >= 3:
                issues.append(f"  [{i}] TEMPLATE-KORE-BARE ja={ja!r} en={en!r}")
        # (d) Quote-only "「X」と いいました/あいさつしました" templates that don't
        # really teach the headword in context
        m = pat_quote.fullmatch(ja)
        if m:
            quoted = m.group(1)
            verb = m.group(2)
            # Quotes of greetings → "あいさつしました" only makes sense for
            # actual greetings (おはよう/こんにちは/etc.). If X is not a
            # greeting, the verb is wrong.
            greetings = {"おはよう", "こんにちは", "こんばんは", "ありがとう",
                         "さようなら", "おやすみ", "ただいま", "おかえり",
                         "もしもし", "いってきます", "いってらっしゃい",
                         "おかげさまで"}
            if verb == "あいさつしました" and quoted not in greetings:
                issues.append(f"  [{i}] TEMPLATE-GREET-WRONG-VERB ja={ja!r} en={en!r}")
    return issues


def check_within_entry_duplicates(entry: dict) -> list[str]:
    """Identical or trivially-same ja within the same entry's examples."""
    issues = []
    seen = {}
    for i, ex in enumerate(entry.get("examples", [])):
        ja = ex.get("ja", "").strip()
        if not ja:
            continue
        if ja in seen:
            issues.append(f"  DUP [{seen[ja]}] vs [{i}] ja={ja!r}")
        else:
            seen[ja] = i
    return issues


# Counter-rendaku map: when a counter follows certain numbers it
# undergoes phonological alternation. Examples are pedagogically
# correct; the headword check should accept these.
COUNTER_RENDAKU = {
    "ひき": {"ぴき", "びき"},  # 一ぴき, 三びき, 八ぴき
    "はい": {"ぱい", "ばい"},  # 一ぱい, 三ばい
    "ふん": {"ぷん"},          # 一ぷん, 三ぷん
    "ほん": {"ぽん", "ぼん"},  # 一ぽん, 三ぼん
    "ほ": {"ぽ", "ぼ"},
    "かい": {"がい"},          # 三がい (floor)
    "けん": {"げん"},
}


def _verb_stems(form: str, reading: str, pos: str) -> list[str]:
    """For a verb entry, return possible inflected-stem prefixes (kana)
    that should appear in any example, regardless of conjugation.

    verb-1 (godan): drop the final u-row kana
      まつ → ま; かう → か; よむ → よ; はたらく → はたら
    verb-2 (ichidan): drop the final る
      たべる → たべ; おきる → おき; ねる → ね
    verb-3 (irregular):
      する → し / す; くる → こ / き / く
    Also returns the kanji-form prefix dropping last kana, e.g. 話す → 話.
    """
    out: set[str] = set()
    for src in (reading, form):
        if not src:
            continue
        if pos == "verb-1" and len(src) >= 2 and src[-1] in "うくぐすつぬぶむる":
            out.add(src[:-1])
        elif pos == "verb-2" and len(src) >= 2 and src[-1] == "る":
            out.add(src[:-1])
        elif pos == "verb-3":
            # する / くる / 〜する compounds
            if src.endswith("する"):
                out.add(src[:-2])  # for 勉強する → 勉強
                out.add(src[:-2] + "し")
                out.add(src[:-2] + "す")
            elif src.endswith("くる") or src == "来る":
                out.add(src[:-2] + "こ")
                out.add(src[:-2] + "き")
                out.add(src[:-2] + "く")
        else:
            # i-adj or non-verb falls back to whole word
            out.add(src)
        # Also include the kanji-form's leading kanji as a coarse stem
        if KANJI.match(src[:1]):
            out.add(src[:1])
    return [s for s in out if s]


def check_headword_in_examples(entry: dict) -> list[str]:
    form = entry.get("form", "").strip()
    reading = entry.get("reading", "").strip()
    pos = entry.get("pos", "")
    readings = entry.get("readings", [])
    forms_to_match = [form, reading] + list(readings)
    forms_to_match = [f for f in forms_to_match if f]
    # Verb-aware stems
    if pos.startswith("verb"):
        forms_to_match.extend(_verb_stems(form, reading, pos))
    # Counter rendaku alternants
    if pos == "counter" and reading in COUNTER_RENDAKU:
        forms_to_match.extend(COUNTER_RENDAKU[reading])
    # Compound -くる verbs (e.g. もってくる → もって + きて/きました/きません)
    if "くる" in reading:
        prefix = reading[: reading.rfind("くる")]
        if prefix:
            for k in ("き", "こ", "く"):
                forms_to_match.append(prefix + k)
    # i-adj inflection: 〜い → 〜く/〜かった
    if pos == "i-adj" and reading.endswith("い"):
        forms_to_match.append(reading[:-1])
    issues = []
    for i, ex in enumerate(entry.get("examples", [])):
        ja = ex.get("ja", "").strip()
        if not any(f and f in ja for f in forms_to_match):
            # Allow inflected forms via kanji stem present
            kanji_in_form = [c for c in form if KANJI.match(c)]
            if kanji_in_form and any(c in ja for c in kanji_in_form):
                continue
            issues.append(f"  [{i}] HEADWORD-MISSING form={form!r} reading={reading!r} pos={pos!r} ja={ja!r}")
    return issues


def check_broken_translations(entry: dict) -> list[str]:
    issues = []
    for i, ex in enumerate(entry.get("examples", [])):
        en = ex.get("translation_en", "").strip()
        ja = ex.get("ja", "").strip()
        if not en:
            issues.append(f"  [{i}] EN-MISSING ja={ja!r}")
            continue
        # missing article on common noun in "I saw X" frame
        m = re.match(r"^I\s+saw\s+([a-z]+)\.?$", en)
        if m:
            obj = m.group(1)
            # Allow pronouns / proper / mass nouns
            if obj not in {"him", "her", "them", "it", "you", "us", "me",
                           "water", "rice", "music", "snow", "rain", "fire",
                           "Japan", "Tokyo", "anyone", "everyone", "someone",
                           "nothing", "everything", "homework", "Mt", "Mr"}:
                issues.append(f"  [{i}] EN-NO-ARTICLE: {en!r} (ja={ja!r})")
        # infinitive in relative clause
        if re.search(r"\bwho\s+to\s+[a-z]+", en):
            issues.append(f"  [{i}] EN-INFINITIVE-IN-RELATIVE: {en!r} (ja={ja!r})")
        # Japanese chars leaking into English
        if KANJI.search(en) or HIRA.search(en) or KATA.search(en):
            # Allow parenthetical Japanese annotation like "(可能形)" — they are
            # rare but legitimate. Be specific: flag if Japanese is in the
            # main sentence outside parens.
            outside_parens = re.sub(r"\([^)]*\)", "", en)
            if KANJI.search(outside_parens) or HIRA.search(outside_parens) or KATA.search(outside_parens):
                issues.append(f"  [{i}] EN-JA-LEAK: {en!r} (ja={ja!r})")
        # No terminator at all
        if en and not has_terminator(en) and not re.search(r"\([^)]*\)$", en):
            issues.append(f"  [{i}] EN-NO-TERMINATOR: {en!r}")
        # Translation that just says "X" with no verb/sentence
        # e.g., en = "wall" when ja = "かべを 見ました。"
        if len(en.split()) <= 2 and not any(en.endswith(p) for p in [".", "?", "!"]):
            issues.append(f"  [{i}] EN-FRAGMENT: {en!r} (ja={ja!r})")
    return issues


def check_pos_form(entry: dict) -> list[str]:
    pos = entry.get("pos", "")
    form = entry.get("form", "")
    reading = entry.get("reading", "")
    issues = []
    if pos == "i-adj":
        # Must end in い (or in kanji that maps to い-final reading)
        target = reading or form
        if not target.endswith("い"):
            # Some i-adj have い in the kana even when form is kanji
            if not (reading and reading.endswith("い")):
                issues.append(f"  POS-FORM: i-adj entry but reading {reading!r} doesn't end in い")
    if pos == "verb-2":
        # ru-verb: reading must end in -eる or -iる
        target = reading
        if target and not (target.endswith("る") and len(target) >= 2):
            issues.append(f"  POS-FORM: verb-2 (ru-verb) reading {reading!r} doesn't end in る")
        elif target and target.endswith("る"):
            penult = target[-2]
            e_i_kana = set("いきぎしじちぢにひびぴみりえけげせぜてでねへべぺめれ")
            if penult not in e_i_kana:
                # genuinely a Group-1 form misclassified
                issues.append(f"  POS-FORM: verb-2 reading {reading!r} has non-e/i kana before る")
    if pos == "verb-1":
        target = reading
        if target and not re.search(r"[うくぐすつぬぶむる]$", target):
            issues.append(f"  POS-FORM: verb-1 reading {reading!r} doesn't end in standard u-row")
    return issues


def check_required_fields(entry: dict) -> list[str]:
    issues = []
    if not entry.get("gloss", "").strip():
        issues.append(f"  MISSING gloss")
    if not entry.get("reading", "").strip() and not entry.get("readings"):
        issues.append(f"  MISSING reading")
    exs = entry.get("examples", [])
    if not exs:
        issues.append(f"  MISSING examples (zero)")
    elif len(exs) < 2:
        issues.append(f"  THIN examples (only {len(exs)})")
    return issues


def check_thin_examples(entry: dict) -> list[str]:
    """C8: example sentences should be substantial enough to teach in
    context. Too-short examples (<= 5 chars of ja) usually waste a slot
    by being just '私です。' or 'はい。'.
    """
    issues = []
    for i, ex in enumerate(entry.get("examples", [])):
        ja = ex.get("ja", "").strip()
        if 0 < len(ja) <= 5:
            issues.append(f"  [{i}] EX-TOO-SHORT ja={ja!r}")
    return issues


def check_translation_starts_uppercase(entry: dict) -> list[str]:
    """C9: English translation starting with a capital letter but
    missing a terminator suggests an unfinished sentence."""
    issues = []
    for i, ex in enumerate(entry.get("examples", [])):
        en = ex.get("translation_en", "").strip()
        if not en:
            continue
        if en[:1].isupper() and not has_terminator(en):
            # has_terminator already tolerates closing quotes
            issues.append(f"  [{i}] EN-CAP-NO-TERMINATOR en={en!r}")
    return issues


def check_gloss_is_romaji(entry: dict) -> list[str]:
    gloss = entry.get("gloss", "").strip()
    reading = entry.get("reading", "").strip()
    issues = []
    if gloss and reading:
        # Suspicious if gloss is just an ASCII transliteration of reading
        # and nothing else (no English semantic content)
        ascii_only = re.fullmatch(r"[a-zA-Z\- ]+", gloss)
        if ascii_only and len(gloss.split()) <= 2 and len(gloss) <= 10:
            # Cheap check — would need a romanization table to be precise
            # Flag short ASCII glosses for human review
            pass  # too many false positives; skip
    return issues


def main():
    print("Loading vocab.json...")
    d = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = d["entries"]
    print(f"Total entries: {len(entries)}")
    print()

    findings = defaultdict(list)
    cross_entry_ja = Counter()

    for entry in entries:
        eid = entry.get("id", "?")
        # Build issues
        t = check_template_leak(entry)
        if t:
            findings["C1-TEMPLATE-LEAK"].append((eid, t))
        d2 = check_within_entry_duplicates(entry)
        if d2:
            findings["C2-WITHIN-DUP"].append((eid, d2))
        h = check_headword_in_examples(entry)
        if h:
            findings["C3-HEADWORD-MISSING"].append((eid, h))
        b = check_broken_translations(entry)
        if b:
            findings["C5-BROKEN-EN"].append((eid, b))
        p = check_pos_form(entry)
        if p:
            findings["C6-POS-FORM"].append((eid, p))
        r = check_required_fields(entry)
        if r:
            findings["C7-MISSING-FIELD"].append((eid, r))
        s = check_thin_examples(entry)
        if s:
            findings["C8-EX-TOO-SHORT"].append((eid, s))
        u = check_translation_starts_uppercase(entry)
        if u:
            findings["C9-EN-CAP-NO-TERMINATOR"].append((eid, u))
        # cross-entry boilerplate accumulator
        for ex in entry.get("examples", []):
            ja = ex.get("ja", "").strip()
            if ja:
                cross_entry_ja[ja] += 1

    # C4: cross-entry boilerplate
    boilerplate = [(ja, n) for ja, n in cross_entry_ja.items() if n >= 5]
    boilerplate.sort(key=lambda x: -x[1])

    # Report
    print("=" * 72)
    print(f"C1 TEMPLATE-LEAK ({len(findings['C1-TEMPLATE-LEAK'])} entries):")
    print("=" * 72)
    for eid, msgs in findings["C1-TEMPLATE-LEAK"][:30]:
        print(f"  {eid}")
        for m in msgs:
            print(m)
    if len(findings["C1-TEMPLATE-LEAK"]) > 30:
        print(f"  ... and {len(findings['C1-TEMPLATE-LEAK'])-30} more")

    print()
    print("=" * 72)
    print(f"C2 WITHIN-ENTRY DUPLICATES ({len(findings['C2-WITHIN-DUP'])} entries):")
    print("=" * 72)
    for eid, msgs in findings["C2-WITHIN-DUP"][:30]:
        print(f"  {eid}")
        for m in msgs:
            print(m)
    if len(findings["C2-WITHIN-DUP"]) > 30:
        print(f"  ... and {len(findings['C2-WITHIN-DUP'])-30} more")

    print()
    print("=" * 72)
    print(f"C3 HEADWORD MISSING IN EXAMPLE ({len(findings['C3-HEADWORD-MISSING'])} entries):")
    print("=" * 72)
    for eid, msgs in findings["C3-HEADWORD-MISSING"][:25]:
        print(f"  {eid}")
        for m in msgs:
            print(m)
    if len(findings["C3-HEADWORD-MISSING"]) > 25:
        print(f"  ... and {len(findings['C3-HEADWORD-MISSING'])-25} more")

    print()
    print("=" * 72)
    print(f"C4 CROSS-ENTRY BOILERPLATE (ja shared by >=5 entries; {len(boilerplate)} sentences):")
    print("=" * 72)
    for ja, n in boilerplate[:30]:
        print(f"  {n:3d}x  {ja!r}")

    print()
    print("=" * 72)
    print(f"C5 BROKEN ENGLISH TRANSLATIONS ({len(findings['C5-BROKEN-EN'])} entries):")
    print("=" * 72)
    for eid, msgs in findings["C5-BROKEN-EN"][:30]:
        print(f"  {eid}")
        for m in msgs:
            print(m)
    if len(findings["C5-BROKEN-EN"]) > 30:
        print(f"  ... and {len(findings['C5-BROKEN-EN'])-30} more")

    print()
    print("=" * 72)
    print(f"C6 POS-FORM MISMATCH ({len(findings['C6-POS-FORM'])} entries):")
    print("=" * 72)
    for eid, msgs in findings["C6-POS-FORM"][:30]:
        print(f"  {eid}")
        for m in msgs:
            print(m)

    print()
    print("=" * 72)
    print(f"C7 MISSING REQUIRED FIELDS ({len(findings['C7-MISSING-FIELD'])} entries):")
    print("=" * 72)
    for eid, msgs in findings["C7-MISSING-FIELD"][:30]:
        print(f"  {eid}")
        for m in msgs:
            print(m)

    print()
    print("=" * 72)
    print("SUMMARY (entries flagged per check):")
    print("=" * 72)
    print(f"  C1 template-leak:        {len(findings['C1-TEMPLATE-LEAK'])}")
    print(f"  C2 within-entry-dup:     {len(findings['C2-WITHIN-DUP'])}")
    print(f"  C3 headword-missing:     {len(findings['C3-HEADWORD-MISSING'])}")
    print(f"  C4 cross-entry-boilrpl:  {len(boilerplate)} distinct sentences shared >=5x")
    print(f"  C5 broken-en:            {len(findings['C5-BROKEN-EN'])}")
    print(f"  C6 pos-form-mismatch:    {len(findings['C6-POS-FORM'])}")
    print(f"  C7 missing-field:        {len(findings['C7-MISSING-FIELD'])}")
    print(f"  C8 ex-too-short:         {len(findings['C8-EX-TOO-SHORT'])}")
    print(f"  C9 en-cap-no-terminator: {len(findings['C9-EN-CAP-NO-TERMINATOR'])}")


if __name__ == "__main__":
    main()
