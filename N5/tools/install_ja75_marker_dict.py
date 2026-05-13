"""Install per-pattern meaning_ja canonical-marker dictionary + JA-75.

DESIGN INSIGHT: rather than try to predict what meaning_ja SHOULD say
(which fails for terse entries like "ていねいな いいかた"), this script
SNAPSHOTS the current (post-3-audit-runs, verified-correct) meaning_ja's
distinctive vocabulary as markers. JA-75 then catches any future edit
that drifts AWAY from the verified state.

For each pattern, `_meaning_ja_markers` contains:
  1. Literal grammar markers from the `pattern` field (e.g., です, ます)
  2. The first 「marker」 substring from the current meaning_ja, if any
  3. The first 2-3 distinctive content-words from meaning_ja (concept
     function names like ていねい, しゅだい, ふつうけい)
  4. Manual additions for 37 Latin/single-char patterns

JA-75 invariant: every pattern's meaning_ja must contain at least one
of its _meaning_ja_markers as a substring. This locks the current
verified-correct state forward — any future edit that changes the
concept-vocabulary materially will fail CI.
"""
import json
import io
import sys
import shutil
import re

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

GRAMMAR = "data/grammar.json"
BAK = "data/grammar.json.bak_2026_05_13_ja75_install"

JA_RE = re.compile(r'[ぁ-んァ-ヿ一-鿿]+')
QUOTE_RE = re.compile(r'「([^」]+)」')


def auto_extract_pattern_markers(pattern_field):
    """Pull >=2-char Japanese substrings from pattern field."""
    if not pattern_field:
        return []
    cleaned = pattern_field.replace("〜", "").replace("～", "")
    markers = [m for m in JA_RE.findall(cleaned) if len(m) >= 2]
    seen = set()
    out = []
    for m in markers:
        if m not in seen:
            seen.add(m)
            out.append(m)
    return out


def extract_meaning_ja_distinctive(meaning_ja):
    """Pull distinctive markers from a meaning_ja string:
      - Any 「marker」 substrings
      - The first 2-3 content-words (Japanese >=2 chars) that aren't
        boilerplate (は、を、に、の、で、と connectives).
    """
    if not meaning_ja:
        return []
    out = []
    # 1. All quoted markers
    for m in QUOTE_RE.findall(meaning_ja):
        if len(m) >= 2:
            out.append(m)
    # 2. Distinctive Japanese content-words: extract >=3-char strings
    # from outside the quotes (more selective).
    blob_no_quotes = QUOTE_RE.sub("", meaning_ja)
    for m in JA_RE.findall(blob_no_quotes):
        # Pick out function-name terms (>=3 chars, kana or kanji)
        if len(m) >= 3:
            out.append(m)
        if len(out) >= 8:
            break
    # Dedup
    seen = set()
    deduped = []
    for m in out:
        if m not in seen:
            seen.add(m)
            deduped.append(m)
    return deduped[:6]  # cap at 6


# Manual markers for 37 Latin / single-char patterns (added on top of
# auto-extracted ones)
MANUAL_MARKERS = {
    "n5-002": ["「は」", "しゅだい", "わだい", "topic"],
    "n5-003": ["「が」", "しゅご", "subject", "あたらしい じょうほう"],
    "n5-004": ["「を」", "もくてきご", "direct object"],
    "n5-005": ["「に」", "場所", "ばしょ", "時間", "じかん"],
    "n5-006": ["「へ」", "ほうこう", "direction"],
    "n5-007": ["「で」", "ばしょ", "しゅだん", "means"],
    "n5-008": ["「と」", "いっしょ", "with"],
    "n5-011": ["「や」", "ならべ", "and"],
    "n5-013": ["「も」", "ほかにも", "おなじ", "also"],
    "n5-023": ["「か」", "しつもん", "question"],
    "n5-024": ["「か」", "えらぶ", "or"],
    "n5-025": ["「ね」", "かくにん", "あい手"],
    "n5-026": ["「よ」", "つたえる", "あらたしい じょうほう"],
    "n5-028": ["「の」", "しょゆう", "めいし"],
    "n5-029": ["「の」", "しょゆう", "possessive"],
    "n5-030": ["「の」", "めいし", "nominalizer"],
    "n5-031": ["「の」", "しつもん"],
    "n5-065": ["じしょけい", "ふつうけい", "plain", "dictionary"],
    "n5-067": ["「〜た」", "かこ"],
    "n5-069": ["「〜て」", "つなぐ", "form"],
    "n5-070": ["「〜て」", "じゅんじょ", "ならべ"],
    "n5-078": ["い-けいようし", "い-adj"],
    "n5-084": ["な-けいようし", "な-adj"],
    "n5-089": ["な-けいようし", "な-adj"],
    "n5-108": ["「数+counter」", "かず", "数"],
    "n5-110": ["counter", "かず", "数"],
    "n5-111": ["「〜じ」", "時"],
    "n5-115": ["「に」", "場所", "目てき", "時間"],
    "n5-126": ["「が」", "but", "つなぐ", "ぶんと ぶん"],
    "n5-135": ["どうし", "めいし", "しゅうしょく", "relative"],
    "n5-136": ["けいようし", "めいし", "Adj"],
    "n5-137": ["めいし", "Noun", "の"],
    "n5-155": ["「〜が」", "but", "ふたつの ぶん"],
    "n5-156": ["「〜ね」", "「〜よ」", "文の おわり"],
    "n5-165": ["「お〜」", "「ご〜」", "ていねい"],
    "n5-182": ["「〜な」", "きんし", "prohibition", "つよい"],
    "n5-183": ["だれか", "なにか", "どこか", "Question word"],
}


def main():
    shutil.copy2(GRAMMAR, BAK)
    g_raw = json.load(open(GRAMMAR, encoding="utf-8"))

    populated = 0
    for p in g_raw["patterns"]:
        pid = p["id"]
        pat = p.get("pattern") or ""
        mj = p.get("meaning_ja") or ""

        # Combine three sources
        markers = set()
        # 1. Auto from pattern field
        for m in auto_extract_pattern_markers(pat):
            markers.add(m)
        # 2. Distinctive from current meaning_ja (snapshot the verified state)
        for m in extract_meaning_ja_distinctive(mj):
            markers.add(m)
        # 3. Manual additions
        if pid in MANUAL_MARKERS:
            for m in MANUAL_MARKERS[pid]:
                markers.add(m)

        # Dedup + cap
        marker_list = sorted(markers, key=lambda x: -len(x))[:10]
        if marker_list:
            p["_meaning_ja_markers"] = marker_list
            populated += 1

    with open(GRAMMAR, "w", encoding="utf-8") as f:
        json.dump(g_raw, f, ensure_ascii=False, indent=2)

    print(f"Populated _meaning_ja_markers on {populated}/{len(g_raw['patterns'])} patterns")

    # Verify: dry-run JA-75
    g2 = json.load(open(GRAMMAR, encoding="utf-8"))
    failing = []
    for p in g2["patterns"]:
        markers = p.get("_meaning_ja_markers") or []
        if not markers:
            continue
        mj = p.get("meaning_ja") or ""
        if not any(m in mj for m in markers):
            failing.append((p["id"], p.get("pattern"), markers[:3], mj[:80]))
    print(f"\nJA-75 dry-run: {len(failing)} patterns FAIL (should be 0 after snapshot)")
    for pid, pat, markers, mj in failing[:10]:
        print(f"  {pid}: pat={pat!r}, markers[:3]={markers}, meaning_ja={mj!r}")


if __name__ == "__main__":
    main()
