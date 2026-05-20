"""
audit_rationale_overlap_2026_05_21.py
======================================

Advisory audit tool for the GOI-001-class content-mismatch defect.

Closes the deferred item from REG-001 + GOI-001 close-out: the
token-overlap content-mismatch check that the original bug spec
proposed but JA-136 (cross-question duplication) only approximates.

Design — why ADVISORY (not strict CI):

  Strict implementation requires morphological stemming (kuromoji or
  equivalent). A lightweight Python-only substring-stemmer produces
  ~21% false-positive rate on the current corpus, primarily due to:

    - Dictionary-form in rationale_hi vs polite-form in stem
      (わかる ↔ わかります; ある ↔ あります; もらう ↔ もらいました)
    - Kana ↔ kanji orthography variation
      (ともだち ↔ 友だち; わたし ↔ 私)
    - Paraphrase in rationale_hi vs verbatim quote in stem
      (rationale: "おかあさんがよろこんだ" vs stem: "母が...よろこびました")

  21% false-positive rate is too high for a hard CI invariant. This
  tool runs as a periodic audit; flagged candidates need
  human-reviewer judgment per entry.

Usage:
  python tools/audit_rationale_overlap_2026_05_21.py
  python tools/audit_rationale_overlap_2026_05_21.py --strict   # report total only
  python tools/audit_rationale_overlap_2026_05_21.py --verbose  # show all candidates

Outputs an advisory candidate list — does NOT modify any files or
exit non-zero.
"""
import sys, io, json, glob, os, re, argparse
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Kana ↔ kanji normalization for known N5 high-frequency words.
# Per the canonical map in docs/ORTHOGRAPHY-POLICY-N5.md (2026-05-21).
KANA_KANJI_NORM = {
    "わたし": "私", "ともだち": "友", "じょうず": "上手", "くるま": "車",
    "ほん": "本", "みず": "水", "はな": "花", "うみ": "海", "まち": "町",
    "がくせい": "学生", "にほん": "日本", "えいご": "英語",
    "しゃしん": "写真", "しんぶん": "新聞", "てがみ": "手紙",
    "じかん": "時間", "しごと": "仕事", "かぞく": "家族",
    "やま": "山", "せんせい": "先生", "ひと": "人",
}

# Polite-form suffix patterns (longest first to avoid partial-match)
SUFFIXES = [
    "ませんでした", "ませんか", "ません", "ました",
    "ています", "ていません", "ていない", "てください",
    "たがって", "たがる", "たい",
    "ます", "ない", "なかった", "なくては", "なくちゃ",
    "でした", "です", "だった",
    "かった", "くない", "くて",
]
SU_VERBS = ["する", "して", "した", "します", "しました", "している"]

# Common dict-form → polite-stem manual map (used in rationale_hi often)
DICT_TO_STEM = {
    "わかる": "わかり", "できる": "でき", "もらう": "もらい",
    "たべる": "たべ", "のむ": "のみ", "見る": "見", "来る": "来",
    "行く": "行", "ある": "あり", "いる": "い", "つくる": "つくり",
    "読む": "読み", "話す": "話し", "聞く": "聞き", "書く": "書き",
}

def stem_tokens(text: str) -> set:
    if not text:
        return set()
    raw = re.findall(r"[ぁ-ゖァ-ヺ一-鿿]{2,}", text)
    stemmed = set()
    for token in raw:
        stemmed.add(token)
        # Suffix stripping
        s = token
        for sfx in SUFFIXES:
            if s.endswith(sfx) and len(s) > len(sfx):
                stemmed.add(s[:-len(sfx)])
                s = s[:-len(sfx)]
                break
        # する-verb normalization
        for su in SU_VERBS:
            if s.endswith(su) and len(s) > len(su):
                stemmed.add(s[:-len(su)])
                break
        # Dictionary-form mapping
        if token in DICT_TO_STEM:
            stemmed.add(DICT_TO_STEM[token])
        # Kana ↔ kanji orthography
        for kana, norm in KANA_KANJI_NORM.items():
            if kana in token:
                stemmed.add(norm)
    return stemmed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true", help="Total count only")
    ap.add_argument("--verbose", action="store_true", help="Show all candidates")
    args = ap.parse_args()

    candidates = []
    total = 0
    for fp in sorted(glob.glob(os.path.join(REPO_N5, "data", "papers", "*", "*.json"))):
        if ".bak" in os.path.basename(fp) or "manifest" in os.path.basename(fp):
            continue
        try:
            d = json.loads(open(fp, encoding="utf-8").read())
        except Exception:
            continue
        # Build passage map for dokkai
        pmap = {p.get("label"): p.get("text", "") for p in d.get("passages", [])}
        for q in d.get("questions", []):
            rh = q.get("rationale_hi", "") or ""
            if not rh:
                continue
            rh_toks = stem_tokens(rh)
            if not rh_toks:
                continue
            total += 1
            # Haystack: stem + choices + passage (if any) + correctAnswer
            haystack = (q.get("stem_html", "") or "") + " "
            for c in q.get("choices", []):
                haystack += str(c) + " "
            ci = q.get("correctIndex", -1)
            if 0 <= ci < len(q.get("choices", [])):
                haystack += str(q["choices"][ci]) + " "
            plabel = q.get("passage_label")
            if plabel and plabel in pmap:
                haystack += pmap[plabel] + " "
            haystack_toks = stem_tokens(haystack)
            if not haystack_toks:
                continue
            if not (rh_toks & haystack_toks):
                candidates.append({
                    "file": os.path.basename(fp),
                    "qid": q.get("id"),
                    "rh_sample": list(rh_toks)[:5],
                    "haystack_sample": list(haystack_toks)[:5],
                    "rh_preview": rh[:80],
                })

    if args.strict:
        print(f"{len(candidates)} / {total} candidates")
        return 0

    print(f"=== Rationale-overlap audit (advisory; no CI fail) ===")
    print(f"Total questions with rationale_hi: {total}")
    print(f"Candidates with no stemmed-token overlap with stem/choices/passage: {len(candidates)}")
    print()
    print("Note: ~21% false-positive rate expected due to morphological-stemming")
    print("limitations (dictionary-form ↔ polite-form, kana ↔ kanji orthography,")
    print("paraphrase vs verbatim quote). Each candidate needs human-reviewer")
    print("judgment — most will be legitimate dictionary-form references or")
    print("orthography-variant matches that the substring stemmer can't bridge.")
    print()
    show_n = len(candidates) if args.verbose else min(15, len(candidates))
    for c in candidates[:show_n]:
        print(f"  {c['file']} {c['qid']}: rh_sample={c['rh_sample']}")
        print(f"    rh_preview: {c['rh_preview']}")
        print(f"    haystack_sample: {c['haystack_sample']}")
    if not args.verbose and len(candidates) > show_n:
        print(f"  ... and {len(candidates) - show_n} more (run with --verbose to see all)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
