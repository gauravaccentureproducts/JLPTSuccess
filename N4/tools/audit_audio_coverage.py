"""Audit audio coverage — which audio refs declared in data files have
real .mp3 files on disk, and which are missing.

Three sources of audio refs:
  1. data/grammar.json — patterns[].examples[].audio (when present)
  2. data/reading.json — passages[].audio
  3. data/listening.json — items[].audio

Output: per-module coverage report (count + first-N missing IDs) + a
JSON dump of the gap list to feedback/audio-coverage-gaps.json so the
gap can be fed straight into a build script.
"""
from __future__ import annotations

import json
import sys
import io
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
ROOT = Path(__file__).resolve().parent.parent


def collect_grammar_refs() -> list[tuple[str, str, str]]:
    """Return [(item_id, ja_text, expected_path_relative_to_root), ...]"""
    g = json.loads((ROOT / "data" / "grammar.json").read_text(encoding="utf-8"))
    refs = []
    for p in g.get("patterns", []):
        pid = p.get("id")
        for i, ex in enumerate(p.get("examples") or []):
            ja = ex.get("ja", "")
            if not ja:
                continue
            # Convention: audio path is audio/grammar/<patternId>.<i>.mp3
            iid = f"grammar.{pid}.{i}"
            path = ROOT / "audio" / "grammar" / f"{pid}.{i}.mp3"
            refs.append((iid, ja, str(path.relative_to(ROOT))))
    return refs


def collect_reading_refs() -> list[tuple[str, str, str]]:
    r = json.loads((ROOT / "data" / "reading.json").read_text(encoding="utf-8"))
    refs = []
    for p in r.get("passages", []):
        rid = p.get("id")
        ja = p.get("ja", "")
        if not (rid and ja):
            continue
        iid = f"reading.{rid}"
        # Convention: audio/reading/<rid>.mp3 (id uses dots: n5.read.001 → file n5.read.001.mp3)
        path = ROOT / "audio" / "reading" / f"{rid}.mp3"
        refs.append((iid, ja, str(path.relative_to(ROOT))))
    return refs


def collect_listening_refs() -> list[tuple[str, str, str]]:
    li = json.loads((ROOT / "data" / "listening.json").read_text(encoding="utf-8"))
    refs = []
    for it in li.get("items", []):
        lid = it.get("id")
        if not lid:
            continue
        text = it.get("script_ja") or it.get("script") or it.get("ja") or ""
        # listening.json uses an explicit `audio` field with a relative path
        # (e.g. "audio/listening/n5.listen.001.mp3"); honor it when present,
        # else fall back to the convention.
        rel = it.get("audio") or f"audio/listening/{lid}.mp3"
        iid = f"listening.{lid}"
        refs.append((iid, text, rel))
    return refs


def main() -> int:
    sections = [
        ("grammar",   collect_grammar_refs()),
        ("reading",   collect_reading_refs()),
        ("listening", collect_listening_refs()),
    ]

    gaps: dict[str, list[dict]] = {}
    print("=" * 72)
    print(f"  AUDIO COVERAGE AUDIT — {ROOT}")
    print("=" * 72)
    overall_declared = overall_present = 0
    for name, refs in sections:
        present = []
        missing = []
        for iid, ja, rel in refs:
            full = ROOT / rel.replace("\\", "/")
            if full.exists():
                present.append(iid)
            else:
                missing.append({"id": iid, "expected_path": rel,
                                "ja_preview": ja[:60]})
        gaps[name] = missing
        overall_declared += len(refs)
        overall_present += len(present)
        pct = 100.0 * len(present) / max(1, len(refs))
        print(f"\n{name.upper()}: {len(present)}/{len(refs)} present "
              f"({pct:.1f}%), {len(missing)} missing")
        for g in missing[:5]:
            print(f"  MISSING {g['id']}  (expected: {g['expected_path']})")
        if len(missing) > 5:
            print(f"  ... and {len(missing) - 5} more")

    print(f"\n{'=' * 72}")
    pct = 100.0 * overall_present / max(1, overall_declared)
    print(f"OVERALL: {overall_present}/{overall_declared} ({pct:.1f}%)")
    print("=" * 72)

    out_path = ROOT / "feedback" / "audio-coverage-gaps.json"
    out_path.parent.mkdir(exist_ok=True)
    out_path.write_text(json.dumps(gaps, ensure_ascii=False, indent=2),
                        encoding="utf-8")
    total_missing = sum(len(v) for v in gaps.values())
    print(f"\nWrote gap list ({total_missing} entries) to:")
    print(f"  {out_path.relative_to(ROOT)}")
    return 0 if total_missing == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
