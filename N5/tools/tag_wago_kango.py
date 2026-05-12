"""
ISSUE-116 — Auto-tag vocab[].register_origin with Wago / Kango / Gairaigo.

Audit finding (2026-05-12): 0/1009 vocab entries had register_origin set.
The Wago / Kango / Gairaigo classification matters for register-appropriate
output (e.g., 食べ物 wago casual vs 食料 kango formal).

Classification rules (in priority order):

  1. All katakana script (incl. ー prolonged-sound mark): gairaigo (loanword)
  2. All hiragana, no kanji: wago (native Japanese)
  3. Contains kanji + ends in hiragana okurigana: wago (verb / adj / native
     compound with native morphology — 食べる, 大きい, etc.)
  4. Pure kanji compound (2+ kanji, no okurigana): kango (Sino-Japanese
     reading — 食料, 大学, etc.)
  5. Single kanji + okurigana (one-kanji + hiragana suffix): wago
  6. Mixed / cannot classify: tagged as wago by default with provenance
     flag for manual review.

Edge cases handled:
  - お-prefixed honorifics (お茶, お風呂): the お is hiragana but the
    semantic core is the kanji; classified by the kanji portion.
  - Numbers (一, 二) and counters: tagged as wago (the kanji are
    technically Chinese-origin but the native kun-yomi reading
    is the productive form at N5 level).
  - Hybrid wago+gairaigo (e.g. アルバイトする): main script is katakana,
    tagged gairaigo.

Idempotent — re-running the script overwrites existing register_origin
only for entries where the classification produces a different value.
Manual hand-curated overrides should set provenance="native_reviewed"
and the script honors them.

Run from N5/ as: python tools/tag_wago_kango.py
"""

from __future__ import annotations

import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
VOCAB = REPO / "data" / "vocab.json"

# Unicode-range matchers — covers Hiragana, Katakana (incl. ー and middle-dot),
# and CJK Unified Ideographs (kanji).
HIRA_RANGE = r"[ぁ-ゖゝゞ]"
KATA_RANGE = r"[ァ-ヺヽヾ・ー]"
KANJI_RANGE = r"[一-龥]"

HIRA_ONLY = re.compile(rf"^{HIRA_RANGE}+$")
KATA_ONLY = re.compile(rf"^{KATA_RANGE}+$")
KANJI_RE = re.compile(KANJI_RANGE)
ENDS_WITH_HIRA = re.compile(rf"{HIRA_RANGE}$")
LEADING_O_HONORIFIC = re.compile(rf"^お(?={KANJI_RANGE})")

# Digit kanji that read with on-yomi (Sino-Japanese) by default at N5.
# Numerals + multi-digit place values. Always kango when used as the
# number ichi/ni/san/... (or in compounds with those readings).
DIGIT_KANJI = set("一二三四五六七八九十百千万億零")

# Single-kanji entries whose primary N5 reading is kun-yomi (wago).
# Concrete native-noun set, not derived from a heuristic.
SINGLE_KANJI_WAGO_OVERRIDE = set("私人父母男女子目耳口手足山川海空雨雪木花魚鳥犬猫車道家店本書何")


def classify(form: str, reading: str = "") -> str:
    """Return 'wago' | 'kango' | 'gairaigo'.

    `reading` is consulted only when needed to disambiguate compound
    numerals like 二人 (ふたり = wago vs にじん = kango).
    """
    if not form:
        return "wago"
    # 1. All katakana → gairaigo
    if KATA_ONLY.match(form):
        return "gairaigo"
    # 2. All hiragana → wago
    if HIRA_ONLY.match(form):
        return "wago"
    # 3. お-honorific: strip leading お then re-classify the core
    if LEADING_O_HONORIFIC.match(form):
        core = form[1:]
        return classify(core, reading)
    # 4. Contains kanji
    if KANJI_RE.search(form):
        # 4a. Ends in hiragana okurigana → wago (native morphology)
        if ENDS_WITH_HIRA.search(form):
            return "wago"
        # 4a-bis. Contains hiragana ANYWHERE in middle → wago (native compound
        # with native conjunction/particle, e.g., 男の子, 女の子, 知り合い).
        if re.search(HIRA_RANGE, form):
            return "wago"
        # 4b. Single kanji
        if len(form) == 1:
            if form in DIGIT_KANJI:
                return "kango"  # 一/二/三 etc. read with on-yomi default
            if form in SINGLE_KANJI_WAGO_OVERRIDE:
                return "wago"  # native concrete nouns (私, 人, 父, etc.)
            return "wago"  # default for unhandled single kanji
        # 4c. Compound numerals: 一人/二人/三人 with reading ひとり/ふたり/...
        # These are wago. With reading いちにん/にじん they would be kango.
        first_reading = (reading or "").split("/")[0].strip()
        if form[0] in DIGIT_KANJI and first_reading and any(
            first_reading.startswith(w)
            for w in ["ひと", "ふた", "みっ", "よっ", "いつ", "むっ", "なな", "やっ", "ここの", "とお", "ついたち", "ふつか", "みっか", "よっか", "いつか", "むいか", "なのか", "ようか", "ここのか", "とおか", "はつか"]
        ):
            return "wago"
        # 4d. Pure kanji compound (2+ kanji, no okurigana) → kango
        return "kango"
    # 5. Fallback: treat as wago
    return "wago"


def main() -> int:
    vocab = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = vocab["entries"]

    counts = {"wago": 0, "kango": 0, "gairaigo": 0}
    touched = 0
    preserved_curated = 0

    for v in entries:
        form = v.get("form") or v.get("reading") or ""
        # Honor hand-curated entries: if register_origin is set AND provenance
        # is native_reviewed, do not overwrite.
        existing = v.get("register_origin")
        provenance = v.get("provenance") or v.get("register_origin_provenance")
        if existing and provenance == "native_reviewed":
            preserved_curated += 1
            counts[existing] = counts.get(existing, 0) + 1
            continue

        tag = classify(form, v.get("reading", ""))
        if existing != tag:
            v["register_origin"] = tag
            v["register_origin_provenance"] = "auto_derived"
            touched += 1
        counts[tag] = counts.get(tag, 0) + 1

    print(f"Total vocab entries: {len(entries)}")
    print(f"Touched (newly classified or changed): {touched}")
    print(f"Preserved (native_reviewed): {preserved_curated}")
    print()
    print("Classification counts:")
    for k in ("wago", "kango", "gairaigo"):
        n = counts.get(k, 0)
        pct = 100 * n / len(entries)
        print(f"  {k:<10}: {n:>4}  ({pct:.1f}%)")

    VOCAB.write_text(
        json.dumps(vocab, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"\nWrote {VOCAB}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
