"""Initialize grammar_review_verdicts.json:
  - TS-01 set to N/A for all (no JA explanation field exists)
  - TS-06 set to N/A for all (audio not text-assessable)
  - TS-02..TS-05 and TS-07..TS-10 left empty for reviewer to fill
"""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IN_FILE = ROOT / "tools" / "grammar_review_input.json"
OUT_FILE = ROOT / "tools" / "grammar_review_verdicts.json"

REVIEW_DATE = date.today().isoformat()

TS_LIST = ["TS-01", "TS-02", "TS-03", "TS-04", "TS-05", "TS-06", "TS-07", "TS-08", "TS-09", "TS-10"]

# Auto-fill rules (with reason text)
AUTO = {
    "TS-01": ("N/A", "JA explanation field is Phase-2 placeholder; not authored yet (acknowledged gap)."),
    "TS-06": ("N/A", "Audio review requires native human listening; not assessable from text data alone."),
}


def main():
    patterns = json.loads(IN_FILE.read_text(encoding="utf-8"))
    verdicts = {}
    for p in patterns:
        pid = p["id"]
        v = {}
        for ts in TS_LIST:
            if ts in AUTO:
                status, note = AUTO[ts]
                v[ts] = [status, note]
            else:
                v[ts] = ["", ""]  # to be filled by reviewer
        v["overall"] = ""
        v["bugs"] = ""
        verdicts[pid] = v
    OUT_FILE.write_text(json.dumps(verdicts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"OK wrote {OUT_FILE}  ({len(verdicts)} patterns; TS-01/TS-06 pre-filled N/A)")


if __name__ == "__main__":
    main()
