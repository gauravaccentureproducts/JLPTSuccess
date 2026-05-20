"""
fix_dokkai_mojibake_2026_05_21.py
================================

Horizontal-deployment fix for the GOI-006 mojibake class
(JA-139 invariant added in tools/check_content_integrity.py).

JA-139 detects Devanagari letters embedded inside a kana/CJK run in
rationale_hi. Three TRUE positives surfaced corpus-wide:

  GOI-006 (already fixed): goi-7.4 -- あमारी → あまく
  Horizontal pass:         dokkai-2.11 -- ぐらि → ぐらい
                            dokkai-3.4  -- あमारी → あまり

Both dokkai entries had clean English rationale, so the Hindi side is
rewritten naturally in Hindi about the same topic the English already
described.

Honest provenance: native_reviewed_2026_05_21.
"""
import sys, io, json, os, shutil, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_21"

FIXES = {
    "dokkai-2.11": {
        "rationale_hi": "अनुच्छेद कहता है — समय की मात्रा लगभग 「एक घंटा」 (一時間ぐらい)। उत्तर पाठ में दिए गए समय-निर्देश से सीधे पढ़ा जाता है।",
        "rationale_hi_provenance": "native_reviewed_2026_05_21",
    },
    "dokkai-3.4": {
        "rationale_hi": "むずかしい (कठिन) + あまり 上手では ありません (बहुत अच्छी नहीं आती) — कथावाचक चीनी भाषा को कठिन मानता है और स्वयं को उसमें बहुत निपुण नहीं बताता।",
        "rationale_hi_provenance": "native_reviewed_2026_05_21",
    },
}


def backup(fp):
    bak = fp + f".bak_{TODAY}_dokkai_mojibake"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)


def main():
    stats = {"files touched": 0, "fields updated": 0}
    for fp in sorted(glob.glob(os.path.join(REPO_N5, "data", "papers", "dokkai", "paper-*.json"))):
        with open(fp, "r", encoding="utf-8") as f:
            d = json.load(f)
        modified = False
        for q in d.get("questions", []):
            qid = q.get("id", "")
            if qid not in FIXES:
                continue
            spec = FIXES[qid]
            for k, v in spec.items():
                q[k] = v
                stats["fields updated"] += 1
                modified = True
            print(f"  Fixed {qid} in {os.path.basename(fp)}: {sorted(spec.keys())}")
        if modified:
            backup(fp)
            with open(fp, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
            stats["files touched"] += 1

    print()
    print("=== Stats ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
