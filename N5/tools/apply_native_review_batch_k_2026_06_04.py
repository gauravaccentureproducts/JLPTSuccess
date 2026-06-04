"""Batch K — close the 2 remaining native-reviewer bugs on すむ (BUG-266
re-check, 2026-06-04).

The re-check confirmed 10/12 batch-J bugs fixed; 2 remain, both on すむ:
  - まいにち すむ  ("live every day" — unnatural)
  - いま すむ      ("live now" — incomplete/unnatural)
The reviewer supplied the native-approved fix: replace with location-
particle (に) collocations 東京に すむ / 日本に すむ / この町に すむ.

すむ is a stative verb, so frequency/time-adverb collocations don't fit.
よく すむ ("often live") is the SAME error class as the 2 cited, so we
replace all three frequency/time-adverb collocations with the reviewer's
location collocations — this also makes the field a proper set of
PARTICLE examples (に-location), which is what particle_examples should be.

Scope is deliberately すむ-ONLY. The broad "frequency-adverb + verb"
template across the other ~109 verbs stays in BUG-263 because it is
per-verb: よく ある ("there often is / common") is NATURAL, while
よく すむ is not. Only a native reviewer can make that call per verb;
for すむ the reviewer made it.

Run:
    python tools/apply_native_review_batch_k_2026_06_04.py --dry-run
    python tools/apply_native_review_batch_k_2026_06_04.py
"""
from __future__ import annotations
import argparse, io, json, sys
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "data" / "vocab.json"

# Frequency/time-adverb collocations to replace (all unnatural for stative すむ)
DROP = {"よく すむ", "まいにち すむ", "いま すむ"}
# Reviewer-approved location-particle replacements
ADD = ["東京に すむ", "日本に すむ", "この町に すむ"]


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    v = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = v.get("entries", [])
    e = next((x for x in entries if x.get("form") == "すむ"), None)
    if e is None:
        print("すむ not found"); return 1

    old = list(e.get("particle_examples") or [])
    # keep everything not in DROP, then append the location collocations
    kept = [p for p in old if p not in DROP]
    new = kept + ADD
    print("すむ particle_examples:")
    print(f"  before: {old}")
    print(f"  after:  {new}")

    if not args.dry_run:
        e["particle_examples"] = new
        prov = e.get("particle_examples_provenance") or ""
        e["particle_examples_provenance"] = (
            (prov + " | " if prov else "")
            + "native_review_2026_06_04 (batch K: replaced frequency/time-"
            "adverb collocations (よく/まいにち/いま すむ) with reviewer-approved "
            "location-particle collocations — すむ is stative and takes に for "
            "location; broad adverb-collocation review across other verbs "
            "remains BUG-263 as it is per-verb, e.g. よくある is natural)"
        )
        meta = v.get("_meta") or {}
        meta["native_review_pass_2026_06_04_batch_k"] = (
            "Batch K: closed the 2 remaining BUG-266 re-check items on すむ "
            "(まいにち すむ / いま すむ) + the same-class よく すむ, replaced with "
            "reviewer-approved location-particle collocations 東京に/日本に/"
            "この町に すむ. Driver: tools/apply_native_review_batch_k_2026_06_04.py."
        )
        v["_meta"] = meta
        VOCAB.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
        print(f"\nWrote {VOCAB}")
    else:
        print("\n(DRY RUN — no file written)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
