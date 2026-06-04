"""Apply native-reviewer Batch J — systematic template-artifact fixes
(2026-06-04 specific-bug audit).

The audit cited 12 bugs; reproduction showed they are instances of
systematic template-generation artifacts. Batch J fixes the
DETERMINISTIC + CONFIRMED-NONSENSE classes:

  J1) Verb conjugation artifacts (110 verbs). Every verb's
      particle_examples contained `<dict-form>ます` and
      `<dict-form>ました` — malformed Japanese (you cannot append
      ます to a dictionary form). Replace with the CORRECT polite /
      polite-past forms via a verb-class-aware conjugator
      (godan / ichidan / irregular). Fully deterministic.

  J2) い-adjective でした nonsense example sentences
      (「えいがは <i-adj>いでした。」 ~17 entries). These are both
      grammatically wrong (い-adj past is かったです, not いでした)
      AND semantically nonsense ("the movie was yellow / thin /
      bitter"). Remove them (each entry retains its good
      example[0]). Also remove the stray cross-contaminated
      particle_example 「しかくいでした」 from 書く.

  J3) 「今日は とても <X>です。」 nonsense example sentences (17).
      "Today is very <X>" is only valid for weather / day-quality
      adjectives. Remove for all NON-weather adjectives
      (白い/くろい/みじかい/まるい/ぬるい/とおい/おおい/…); keep the
      weather ones (すずしい, あたたかい, いい).

  J4) Cited specifics:
      - カタカナ particle_examples: remove the purchase/price/new
        nonsense (カタカナを かう / を ください / あたらしい / たかい /
        やすい — treats a writing system as a buyable object).
      - うるさい: remove the nonsense example 「この りんごは
        うるさいです。」 (an apple cannot be noisy).

GUARD: never reduce an entry below 1 example. If a removal would
empty the examples array, skip it and log for native attention.

Items intentionally LEFT for native judgment (BUG-263 / OPEN-003/004/013):
  - The broad adjective particle_examples noun-pairing nonsense
    (ぬるい ほん, まるい くるま, …) across ~100 i-adjectives.
  - The ~90 「この N は X」 example sentences (mostly natural;
    needs per-sentence judgment).
  - The 「よく/まいにち/いま <verb>」 adverb collocations'
    naturalness (まいにち すむ, いま すむ).

Run:
    python tools/apply_native_review_batch_j_2026_06_04.py --dry-run
    python tools/apply_native_review_batch_j_2026_06_04.py
"""
from __future__ import annotations
import argparse, io, json, re, sys
from pathlib import Path

if hasattr(sys.stdout, "buffer"):
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).resolve().parents[1]
VOCAB = ROOT / "data" / "vocab.json"

# --- godan final-kana → i-row mapping for ます-stem ---
GODAN_MASU_STEM = {
    "う": "い", "く": "き", "ぐ": "ぎ", "す": "し", "つ": "ち",
    "ぬ": "に", "ぶ": "び", "む": "み", "る": "り",
}


def conjugate_polite(form, pos):
    """Return (masu, mashita) for a verb dictionary form.
    pos: 'verb-1' (godan), 'verb-2' (ichidan), 'verb-3' (irregular)."""
    if not form:
        return None, None
    # Irregular
    if pos == "verb-3":
        if form == "する":
            return "します", "しました"
        if form == "来る":
            return "来ます", "来ました"
        if form == "くる":
            return "きます", "きました"
        if form.endswith("する"):
            stem = form[:-2]  # strip する
            return stem + "します", stem + "しました"
        # fallback — unknown irregular: don't guess
        return None, None
    if pos == "verb-2":  # ichidan: drop final る
        if form.endswith("る"):
            stem = form[:-1]
            return stem + "ます", stem + "ました"
        return None, None
    if pos == "verb-1":  # godan
        last = form[-1]
        istem = GODAN_MASU_STEM.get(last)
        if istem is None:
            return None, None
        stem = form[:-1] + istem
        return stem + "ます", stem + "ました"
    return None, None


# --- J3: 「今日は とても X」 — keep only weather / day-quality adjectives ---
KYOU_KEEP = {"すずしい", "あたたかい", "あたたかい", "あつい", "さむい",
             "いい", "よい", "わるい", "いそがしい", "ひま"}

# --- J4: カタカナ particle_examples to drop (purchase/price/new nonsense) ---
KATAKANA_DROP = {"カタカナを かう", "カタカナを ください",
                 "あたらしい カタカナ", "たかい カタカナ", "やすい カタカナ"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    v = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = v.get("entries", [])
    log = []
    n_j1 = n_j2 = n_j3 = n_j4 = 0
    skipped = []

    EIGA_RE = re.compile(r"^えいがは\s*.+でした")
    KYOU_RE = re.compile(r"^今日は\s*とても\s*(.+?)です")

    for e in entries:
        form = e.get("form", "") or ""
        pos = e.get("pos", "") or ""
        eid = e.get("id", "")

        # ---- J1: verb conjugation artifacts ----
        if pos in ("verb-1", "verb-2", "verb-3"):
            pe = e.get("particle_examples") or []
            if pe:
                masu, mashita = conjugate_polite(form, pos)
                if masu and mashita:
                    new_pe = []
                    changed = False
                    for p in pe:
                        if p == form + "ます":
                            new_pe.append(masu); changed = True
                        elif p == form + "ました":
                            new_pe.append(mashita); changed = True
                        else:
                            new_pe.append(p)
                    if changed:
                        e["particle_examples"] = new_pe
                        prov = e.get("particle_examples_provenance") or ""
                        e["particle_examples_provenance"] = (
                            (prov + " | " if prov else "")
                            + "native_review_2026_06_04 (batch J1: malformed "
                            "conjugation <dict>ます/<dict>ました corrected to "
                            "proper polite forms)"
                        )
                        log.append(f"  J1 {form} ({pos}): {form}ます→{masu}, {form}ました→{mashita}")
                        n_j1 += 1

        # ---- J2: remove えいがは <i-adj>でした nonsense examples ----
        examples = e.get("examples") or []
        if examples:
            keep = [x for x in examples if not EIGA_RE.match((x.get("ja", "") or "").strip())]
            removed = [x for x in examples if EIGA_RE.match((x.get("ja", "") or "").strip())]
            if removed:
                if len(keep) >= 1:
                    e["examples"] = keep
                    for x in removed:
                        log.append(f"  J2 {form}: removed example {x.get('ja')!r}")
                    n_j2 += 1
                else:
                    skipped.append(f"J2 {form}: would empty examples, skipped")

        # ---- J3: remove 「今日は とても X」 for non-weather adjectives ----
        examples = e.get("examples") or []
        if examples:
            new_keep = []
            removed_kyou = []
            for x in examples:
                ja = (x.get("ja", "") or "").strip()
                m = KYOU_RE.match(ja)
                if m:
                    adj = m.group(1).strip()
                    # adj may equal the entry form; keep only weather set
                    if adj in KYOU_KEEP or form in KYOU_KEEP:
                        new_keep.append(x)
                    else:
                        removed_kyou.append(x)
                else:
                    new_keep.append(x)
            if removed_kyou:
                if len(new_keep) >= 1:
                    e["examples"] = new_keep
                    for x in removed_kyou:
                        log.append(f"  J3 {form}: removed example {x.get('ja')!r}")
                    n_j3 += 1
                else:
                    skipped.append(f"J3 {form}: would empty examples, skipped")

        # ---- J4a: カタカナ particle_examples cleanup ----
        if form == "カタカナ":
            pe = e.get("particle_examples") or []
            new_pe = [p for p in pe if p not in KATAKANA_DROP]
            if new_pe != pe:
                e["particle_examples"] = new_pe
                prov = e.get("particle_examples_provenance") or ""
                e["particle_examples_provenance"] = (
                    (prov + " | " if prov else "")
                    + "native_review_2026_06_04 (batch J4: removed purchase/"
                    "price/new template collocations — カタカナ is a writing "
                    "system, not a buyable object)"
                )
                log.append(f"  J4a カタカナ: particle_examples {pe} → {new_pe}")
                n_j4 += 1

        # ---- J4b: うるさい — remove この りんごは うるさいです ----
        if form == "うるさい":
            examples = e.get("examples") or []
            keep = [x for x in examples if "りんご" not in (x.get("ja", "") or "")]
            if keep != examples and len(keep) >= 1:
                e["examples"] = keep
                log.append(f"  J4b うるさい: removed この りんごは うるさいです。")
                n_j4 += 1

        # ---- J2b: stray cross-contaminated particle_example in 書く ----
        if form == "書く":
            pe = e.get("particle_examples") or []
            new_pe = [p for p in pe if "しかくいでした" not in p and p != "しかくいでした"]
            if new_pe != pe:
                e["particle_examples"] = new_pe
                log.append(f"  J2b 書く: removed stray particle_example 'しかくいでした'")
                n_j2 += 1

    total = n_j1 + n_j2 + n_j3 + n_j4
    print("Batch J — systematic template-artifact fixes")
    print(f"  J1 verb conjugations corrected:    {n_j1}")
    print(f"  J2 えいがは nonsense removed:        {n_j2}")
    print(f"  J3 今日は nonsense removed:          {n_j3}")
    print(f"  J4 cited specifics (カタカナ/りんご): {n_j4}")
    print(f"  ------------------------------------")
    print(f"  total entries touched: {total}")
    if skipped:
        print(f"  SKIPPED (would empty examples): {len(skipped)}")
        for s in skipped:
            print(f"    {s}")
    print()
    if args.dry_run:
        print("(DRY RUN — no file written)")
    else:
        meta = v.get("_meta") or {}
        meta["native_review_pass_2026_06_04_batch_j"] = (
            f"Batch J applied: J1 fixed {n_j1} verbs' malformed "
            "<dict>ます/<dict>ました conjugations (deterministic, "
            "verb-class-aware); J2 removed えいがは <i-adj>でした nonsense "
            "example sentences; J3 removed 今日は とても <X> nonsense for "
            "non-weather adjectives; J4 cleaned cited カタカナ purchase-"
            "template collocations + この りんごは うるさいです. Broad "
            "adjective-particle_examples + この-frame review remain in "
            "BUG-263 (native judgment). Driver: "
            "tools/apply_native_review_batch_j_2026_06_04.py."
        )
        v["_meta"] = meta
        VOCAB.write_text(json.dumps(v, ensure_ascii=False, indent=2) + "\n",
                         encoding="utf-8")
        print(f"Wrote {VOCAB}")
    print()
    for line in log:
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
