"""Build a compact review packet from N5/data/ for hand-off to a Claude chat.

Drops fields that are review-noise (metadata, timestamps, audio file
paths, schema version blocks, retired_pattern_ids tombstones) and
keeps everything that's substantive content (JA/EN/HI text, IDs,
distractors, rationale, cross-refs).

Output: N5/data/_review_packet/
  - README.md           — data model + stripping rules + corpus counts
  - <source>.json       — content-only version of each top-level file
  - papers/<cat>.json   — concatenated by paper category (4 files instead of 28)

Idempotent: rebuilds the packet from scratch every run.

Usage:
    python N5/tools/build_review_packet.py

Designed for upload to Claude chat (claude.ai) Projects or one-shot
chat attach. After build, see _review_packet/README.md for the
per-file size table and what was dropped.
"""

from __future__ import annotations
import json
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent  # N5/
DATA = ROOT / "data"
OUT = DATA / "_review_packet"

# === Stripping rules ====================================================

# Keys to drop from any dict (including nested) — these are CI/build
# metadata, not review-meaningful content.
DROP_KEYS_ANYWHERE = {
    "_meta",
    "generated_at",
    "last_modified",
    "last_audited",
    "last_updated",
    "build_timestamp",
    "build_id",
    "audio_files",          # list of audio paths; not review-meaningful
    "audio_manifest_hash",
    "checksum",
    "etag",
    "_source_path",
    "_source_file",
    "schema_version",
    "spec_version",
}

# Top-level files to skip entirely — pure build/CI artifacts or backups.
SKIP_FILES = {
    "audio_manifest.json",        # 770KB of file paths only
    "audio_manifest_voice.json",  # voice-style mapping; not content review
    "build_metadata.json",        # CI artifact
    "index.json",                 # generated index
    "_ja91_baseline.json",        # invariant baseline snapshot
    "_ja94_baseline.json",        # invariant baseline snapshot
    "recording_directions.json",  # studio-direction notes, not data
}


def strip(value: Any) -> Any:
    """Recursively drop noise keys; preserve all content."""
    if isinstance(value, dict):
        return {
            k: strip(v)
            for k, v in value.items()
            if k not in DROP_KEYS_ANYWHERE
        }
    if isinstance(value, list):
        return [strip(item) for item in value]
    return value


def write_json(path: Path, payload: Any) -> int:
    """Write JSON to path, return byte size."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = json.dumps(payload, ensure_ascii=False, indent=2)
    path.write_text(text, encoding="utf-8")
    return len(text.encode("utf-8"))


def main() -> int:
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    inventory: list[tuple[str, int, int]] = []  # (relpath, before, after)

    # --- Top-level JSON files ---
    for src in sorted(DATA.glob("*.json")):
        if src.name in SKIP_FILES:
            continue
        if ".bak" in src.name:
            continue
        before = src.stat().st_size
        try:
            payload = json.loads(src.read_text(encoding="utf-8"))
        except Exception as exc:
            print(f"  skip (parse error): {src.name} :: {exc}")
            continue
        stripped = strip(payload)
        out_path = OUT / src.name
        after = write_json(out_path, stripped)
        inventory.append((src.name, before, after))

    # --- Papers subdir: concatenate per category ---
    papers_root = DATA / "papers"
    if papers_root.exists():
        papers_out = OUT / "papers"
        papers_out.mkdir(exist_ok=True)
        for cat_dir in sorted(papers_root.iterdir()):
            if not cat_dir.is_dir():
                continue
            bundle: dict[str, Any] = {"category": cat_dir.name, "papers": []}
            before_total = 0
            for paper_file in sorted(cat_dir.glob("*.json")):
                if ".bak" in paper_file.name:
                    continue
                before_total += paper_file.stat().st_size
                payload = json.loads(paper_file.read_text(encoding="utf-8"))
                bundle["papers"].append({
                    "source_filename": paper_file.name,
                    "content": strip(payload),
                })
            out_path = papers_out / f"{cat_dir.name}.json"
            after = write_json(out_path, bundle)
            inventory.append((f"papers/{cat_dir.name}/*", before_total, after))

    # --- README ---
    total_before = sum(b for _, b, _ in inventory)
    total_after = sum(a for _, _, a in inventory)
    rows = "\n".join(
        f"| `{name}` | {before/1024:.1f} | {after/1024:.1f} | -{(1 - after/before)*100:.1f}% |"
        for name, before, after in inventory
        if before > 0
    )
    readme = f"""# N5 Data Review Packet

Compact representation of `N5/data/` for review by a Claude chat / Project.
Built by `N5/tools/build_review_packet.py`.

## Upload guidance

- **Claude chat (claude.ai) one-shot:** attach the files you want reviewed
  via the paperclip icon. Each file ≤ 30 MB; multiple per message OK.
- **Claude Projects:** add this entire `_review_packet/` folder to Project
  Knowledge. The Project then has persistent access to the data across
  every conversation in that Project.

## What was stripped vs kept

**Stripped (review-noise):**
- `_meta` blocks (provenance, doc-strings, see_also refs)
- Timestamps: `generated_at`, `last_modified`, `last_audited`, `last_updated`,
  `build_timestamp`, `build_id`
- `audio_files` lists (just per-item file paths; review the audio elsewhere)
- `schema_version`, `spec_version`, hash/etag/checksum fields
- **`branding.json`: all string values replaced with empty strings**
  (`brand.name`, `brand.short_name`, `brand.header_label`, `brand.watermark_text`,
  `brand.footer_attribution_html`, `brand.footer_homepage_url`,
  `meta.title`, `meta.description`, `meta.og_title`, `meta.og_description`,
  `meta.og_url`, `meta.twitter_title`, `meta.canonical_url`,
  `trust_strip.en`, `trust_strip.hi`). The schema-shape is preserved
  (all keys present, all values blank). **This is a privacy/anonymity
  strip** to protect brand-identifying content from leaking into the
  review chat — it is NOT a bug in the live site. The live site's
  branding works via hardcoded values in `N5/index.html`
  (`<title>JLPT N5</title>` + ~46 other JLPT references); branding.json
  is consumed as an optional override layer for self-host deploys.
  Added 2026-05-22 per DOCS-BRAND-001 to prevent reviewers from
  misreading the all-empty branding.json as a live-site defect.

**Files skipped entirely (pure CI/build artifacts):**
- `audio_manifest.json` — 770 KB of file paths
- `audio_manifest_voice.json` — voice-style mapping
- `build_metadata.json` — CI snapshot
- `index.json` — derived index
- `_ja91_baseline.json`, `_ja94_baseline.json` — invariant baselines
- `recording_directions.json` — studio direction notes (not learner content)

**Papers subtree** (`papers/bunpou/`, `papers/dokkai/`, `papers/goi/`,
`papers/moji/`) was concatenated: each category's `paper-1.json`..
`paper-7.json` are wrapped into a single `papers/<cat>.json` file with
the original filename preserved under `source_filename`.

**Everything else is preserved verbatim**, including:
- All JA/EN/HI text (vocabulary, grammar patterns, kanji entries,
  reading passages, listening transcripts, mock-test questions,
  distractors, rationales)
- All cross-reference IDs (`pattern_id`, `vocab_id`, kanji glyphs)
- Status flags (`provenance: human_curated|auto_inferred`,
  `polysemy`, etc.)
- N5 corpus structure

## File inventory

| File | Original (KB) | Stripped (KB) | Δ |
|---|---:|---:|---:|
{rows}
| **Total** | **{total_before/1024:.1f}** | **{total_after/1024:.1f}** | **-{(1 - total_after/total_before)*100:.1f}%** |

## How to ask the other Claude

Useful framings (the corpus is sizable; narrow scope per turn):

- "Review `vocab.json` for entries where `gloss_en` and `gloss_hi`
  don't appear to describe the same meaning. List up to 20 with
  pattern_id + form + EN + HI + your reasoning."
- "Audit `papers/moji.json` paper 3 for: (a) stem markup
  consistency, (b) distractor plausibility, (c) rationale_hi
  fidelity to rationale_en."
- "In `grammar.json`, find patterns where the JA example sentence
  uses a kanji not in `n5_kanji_whitelist.json`."
- "Cross-check `kanji.json` against `n5_kanji_readings.json` —
  any kanji missing readings?"
"""
    (OUT / "README.md").write_text(readme, encoding="utf-8")

    print(f"Wrote {len(inventory)} files + README to {OUT.relative_to(ROOT.parent)}")
    print(f"Total size: {total_before/1024:.0f} KB → {total_after/1024:.0f} KB "
          f"(-{(1 - total_after/total_before)*100:.1f}% size reduction)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
