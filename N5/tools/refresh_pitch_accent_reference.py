"""Refresh data/n5_pitch_accent_reference.json from the kanjium dataset.

Pulls the latest kanjium accents.txt (pinned to a specific commit SHA),
filters to entries that match our 1,009 N5 vocab entries by (form,
reading), and writes a clean JSON reference.

Run periodically (or when adding new vocab) to keep the reference in
sync with upstream. The pinned commit ensures reproducibility — bump
the SHA below to upgrade.

USAGE:
    python tools/refresh_pitch_accent_reference.py

Output:
    data/n5_pitch_accent_reference.json

Provenance: kanjium project (https://github.com/mifunetoshiro/kanjium)
License: CC-BY-SA 4.0
"""
from __future__ import annotations
import json
import re
import sys
import urllib.request
from collections import OrderedDict
from datetime import date
from pathlib import Path

# === Pinned to this kanjium commit for reproducibility ===
KANJIUM_COMMIT_SHA = "8a0cdaa16d64a281a2048de2eee2ec5e3a440fa6"
KANJIUM_URL = (
    f"https://raw.githubusercontent.com/mifunetoshiro/kanjium/"
    f"{KANJIUM_COMMIT_SHA}/data/source_files/raw/accents.txt"
)
CACHE = Path("not-required/external-data/kanjium_accents_raw.txt")
VOCAB = Path("data/vocab.json")
OUT = Path("data/n5_pitch_accent_reference.json")


def normalize_full_width(s: str) -> str:
    """kanjium uses full-width digits (０-９); our vocab uses
    half-width. Normalize for matching."""
    out = []
    for c in s:
        if "０" <= c <= "９":
            out.append(chr(ord(c) - ord("０") + ord("0")))
        else:
            out.append(c)
    return "".join(out)


def fetch_kanjium() -> str:
    """Use cached copy if it exists; otherwise download."""
    if CACHE.exists() and CACHE.stat().st_size > 100_000:
        print(f"  using cache: {CACHE} ({CACHE.stat().st_size} bytes)")
        return CACHE.read_text(encoding="utf-8")
    print(f"  fetching {KANJIUM_URL}...")
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(KANJIUM_URL, timeout=60) as r:
        data = r.read().decode("utf-8")
    CACHE.write_text(data, encoding="utf-8")
    print(f"  saved cache: {CACHE} ({CACHE.stat().st_size} bytes)")
    return data


def parse_kanjium(raw: str) -> tuple[dict, dict]:
    """Parse TSV into two indexes:
      primary: {(form, reading) -> [drop_int, ...]} — exact match
      by_reading: {reading -> [drop_int, ...]} — union across all
        kanjium forms with this reading (for kana-only N5 vocab entries
        whose form lacks kanji to match kanjium's kanji-first scheme).

    Multiple drops mean attested alternates within a single
    kanjium entry.
    """
    primary = {}
    by_reading = {}
    for line in raw.splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        if len(parts) < 3:
            continue
        form = normalize_full_width(parts[0]).strip()
        reading = parts[1].strip()
        drops_str = parts[2].strip()
        # CRITICAL: when kanjium leaves the reading column EMPTY, it means
        # the form IS the reading (katakana-only loanwords like バナナ,
        # hiragana-only function words like こんな). Treat form as
        # reading in this case — this is the dominant convention in
        # the kanjium dataset for kana-only entries.
        if not reading:
            reading = form
        # Some kanjium entries prefix POS markers like '(副)3,(形動)0'.
        # Strip parenthetical content before parsing integer drops.
        # Also handle '0,1,2' simple comma-separated lists.
        cleaned = re.sub(r"\([^)]*\)", "", drops_str)
        drops = []
        for piece in cleaned.split(","):
            piece = piece.strip()
            if piece and piece.lstrip("-").isdigit():
                drops.append(int(piece))
        if not drops:
            continue
        # dedupe but preserve order
        seen = set()
        drops = [d for d in drops if not (d in seen or seen.add(d))]
        key = (form, reading)
        if key in primary:
            for d in drops:
                if d not in primary[key]:
                    primary[key].append(d)
        else:
            primary[key] = list(drops)
        # by-reading aggregate (union)
        if reading in by_reading:
            for d in drops:
                if d not in by_reading[reading]:
                    by_reading[reading].append(d)
        else:
            by_reading[reading] = list(drops)
    return primary, by_reading


def build_reference():
    print("Fetching kanjium dataset...")
    raw = fetch_kanjium()
    print(f"Parsing {len(raw)} bytes...")
    primary, by_reading = parse_kanjium(raw)
    print(f"  parsed {len(primary)} unique (form, reading) entries")
    print(f"  parsed {len(by_reading)} unique readings")

    print("Loading vocab.json...")
    vocab = json.load(open(VOCAB, encoding="utf-8"))
    entries = vocab["entries"]
    print(f"  {len(entries)} vocab entries")

    print("Filtering kanjium to N5 vocab scope...")
    out_entries = []
    matched_exact = 0
    matched_by_reading = 0
    for e in entries:
        form = (e.get("form") or "").strip()
        reading = (e.get("reading") or "").strip()
        readings_alt = e.get("readings", []) or []
        all_readings = [reading] + list(readings_alt)
        # 1) Exact (form, reading) match
        hit = None
        for r in all_readings:
            if (form, r) in primary:
                hit = (form, r, primary[(form, r)], "exact")
                break
        # 2) Reading-only match (when form is kana-only or otherwise
        #    doesn't appear in kanjium with that exact form)
        if hit is None:
            for r in all_readings:
                if r and r in by_reading:
                    hit = (form, r, by_reading[r], "by-reading")
                    break
        if hit:
            cand_form, cand_reading, drops, match_kind = hit
            out_entries.append({
                "vocab_id": e["id"],
                "form": cand_form,
                "reading": cand_reading,
                "drops": drops,
                "match_kind": match_kind,
            })
            if match_kind == "exact":
                matched_exact += 1
            else:
                matched_by_reading += 1
    total = matched_exact + matched_by_reading
    print(f"  matched exact:      {matched_exact}/{len(entries)}")
    print(f"  matched by reading: {matched_by_reading}/{len(entries)}")
    print(f"  TOTAL matched:      {total}/{len(entries)} ({total*100//len(entries)}%)")

    out_doc = OrderedDict([
        ("_meta", OrderedDict([
            ("doc", "Pitch-accent reference for vocab.json, filtered from the "
                    "kanjium project's accents.txt to the (form, reading) pairs "
                    "present in our N5 vocab corpus. Used by JA-90 to validate "
                    "vocab pitch_accent.drop values against an authoritative "
                    "source. The 'drops' array lists ALL attested drop positions "
                    "for the entry — some words have multiple acceptable "
                    "accents (heiban + odaka alternates etc.)."),
            ("source", "kanjium project (https://github.com/mifunetoshiro/kanjium)"),
            ("source_pinned_commit", KANJIUM_COMMIT_SHA),
            ("source_url", KANJIUM_URL),
            ("license", "CC-BY-SA 4.0"),
            ("attribution",
             "Pitch accent data from kanjium project (CC-BY-SA 4.0). "
             "Original data primarily sourced from EDICT/EDRDG and NHK 日本語発音"
             "アクセント新辞典 references."),
            ("downloaded_at", date.today().isoformat()),
            ("entries_in_upstream", len(primary)),
            ("matched_exact_form_reading", matched_exact),
            ("matched_by_reading_only", matched_by_reading),
            ("entries_matched_to_n5_vocab", total),
            ("vocab_corpus_size", len(entries)),
            ("match_kind_note",
             "exact = (form, reading) tuple matched kanjium; by-reading = "
             "matched by reading alone (used for kana-only forms where "
             "kanjium has the kanji form). by-reading matches use the UNION "
             "of all drops across kanjium entries with that reading — wider "
             "but less precise. Confidence reflects this in JA-90."),
            ("schema_version", 1),
            ("consumers", ["tools/check_content_integrity.py JA-90"]),
            ("regenerate_with", "python tools/refresh_pitch_accent_reference.py"),
        ])),
        ("entries", out_entries),
    ])
    OUT.write_text(json.dumps(out_doc, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(f"  wrote {OUT} ({OUT.stat().st_size} bytes)")


if __name__ == "__main__":
    build_reference()
