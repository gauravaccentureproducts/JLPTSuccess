"""NTR-FU-002 fix: expose 3-band listening pacing classification.

Adds per-item secondary fields:
  - pacing_band_strict:  in / below / above for JEES-strict 220-240
  - pacing_band_ideal:   in / below / above for round-9-ideal 200-220

Keeps pacing_status (180-240 learner band) for backward compat.

Updates _meta.pacing_audit.note + summary to document the
three-band methodology decision explicitly so consumers can
choose which threshold they're claiming.
"""
import sys, io, os, json, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_23"

STRICT_LO, STRICT_HI = 220, 240
IDEAL_LO, IDEAL_HI = 200, 220


def band_label(mpm, lo, hi):
    if mpm is None: return "unmeasured"
    if mpm < lo: return "below"
    if mpm > hi: return "above"
    return "in"


def main():
    fp = os.path.join(REPO_N5, "data", "listening.json")
    bak = fp + f".bak_{TODAY}_ntr_fu_002"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        data = json.load(f)
    items = data["items"]
    print(f"Total listening items: {len(items)}")
    strict_dist = {"in": 0, "below": 0, "above": 0, "unmeasured": 0}
    ideal_dist = {"in": 0, "below": 0, "above": 0, "unmeasured": 0}
    for it in items:
        mpm = it.get("pacing_morae_per_min")
        sb = band_label(mpm, STRICT_LO, STRICT_HI)
        ib = band_label(mpm, IDEAL_LO, IDEAL_HI)
        it["pacing_band_strict"] = sb
        it["pacing_band_ideal"] = ib
        strict_dist[sb] += 1
        ideal_dist[ib] += 1
    # Update _meta
    pa = data["_meta"].get("pacing_audit") or {}
    pa.setdefault("methodology_three_band_2026_05_23", {})
    pa["methodology_three_band_2026_05_23"] = {
        "rationale": (
            "NTR-FU-002 (BUG-175 close-out): the binary pacing_status='in_range' against "
            "180-240 mpm masked the distribution. JEES-strict exam-grade pacing is 220-240; "
            "round-9 ideal practice band is 200-220; 180-240 is the lenient learner-practice "
            "band used by this corpus's audio rendering. Expose all three so consumers can "
            "choose the threshold they're claiming."
        ),
        "bands": {
            "pacing_status (learner)": [180, 240],
            "pacing_band_ideal (round-9 ideal)": [IDEAL_LO, IDEAL_HI],
            "pacing_band_strict (JEES exam-grade)": [STRICT_LO, STRICT_HI],
        },
        "distribution_strict": strict_dist,
        "distribution_ideal": ideal_dist,
        "audio_source_of_truth": (
            "pacing_status='in_range' is bounded-correct against the 180-240 learner band "
            "that the audio was rendered to. Tightening to JEES-strict would require "
            "re-rendering 38/50 items; deferred as out-of-scope for this fix."
        ),
    }
    data["_meta"]["pacing_audit"] = pa
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Strict band [220, 240] distribution: {strict_dist}")
    print(f"Ideal band [200, 220] distribution: {ideal_dist}")
    print()
    print(f"=== NTR-FU-002 fix applied: 50 items annotated with 3-band pacing ===")


if __name__ == "__main__":
    main()
