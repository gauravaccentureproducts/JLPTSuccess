"""Apply remaining grammar-corpus fixes from the v4 test review.

P2 (DROPPED) — Empty wrong/right rows in common_mistakes were initially
     considered for deletion, but invariant JA-51 ('every grammar
     pattern has >=3 categorized common_mistakes') counts those padded
     rows. Removing them caused 16 patterns to drop below the threshold.
     The correct fix is to AUTHOR new content for those rows, which is
     out of scope for this session. The empty-row TS-03 Fails remain
     as known-open authoring tasks.

P3 — Wire audio paths for n5-098. All 10 audio files exist on disk at
     audio/grammar/n5-098.<i>.mp3 but the examples[].audio field is
     empty. Populate the field.

P4 — Replace n5-011 cm[2] and n5-024 cm[1] with genuinely-wrong learner
     errors (rather than meaning-difference particle swaps that were
     mis-labelled as grammar errors).

Backup: data/grammar.json -> data/grammar.json.bak_2026_05_24_remaining
(re-use the existing backup file from the earlier P2 attempt — it holds
the pre-P3/P4 baseline since P2 has been reverted.)
"""
from __future__ import annotations

import json
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GRAMMAR_JSON = ROOT / "data" / "grammar.json"
INDEX_JSON = ROOT / "data" / "index.json"
BACKUP = ROOT / "data" / "grammar.json.bak_2026_05_24_remaining"

# --- P4 — manual replacements for n5-011 cm[2] and n5-024 cm[1] ---

P4_REPLACEMENTS = [
    {
        "pid": "n5-011",
        "cm_index": 2,
        "expect_wrong": "りんごと バナナを たべます。",
        "new_wrong": "りんご バナナを たべます。",
        "new_right": "りんごや バナナを たべます。",
        "new_why": "や connects multiple nouns to indicate a non-exhaustive list ('apples, bananas, etc.'). Two nouns side-by-side without any listing particle is ungrammatical — Japanese requires や (non-exhaustive) or と (exhaustive) between them.",
    },
    {
        "pid": "n5-024",
        "cm_index": 1,
        "expect_wrong": "コーヒーと おちゃが いいです。",
        "new_wrong": "コーヒー おちゃが いいです。",
        "new_right": "コーヒーか おちゃが いいです。",
        "new_why": "Mid-sentence か links alternatives ('coffee OR tea'). Two unconnected nouns in this slot are ungrammatical — Japanese needs か for 'or', と for 'both', or や for 'and others'.",
    },
]


def remove_empty_cm_rows(p):
    """Return (kept_rows, removed_indices_with_content_summary)."""
    removed = []
    kept = []
    for i, m in enumerate(p.get("common_mistakes") or []):
        w = (m.get("wrong") or "").strip()
        r = (m.get("right") or "").strip()
        if not w or not r:
            removed.append((i, w[:40], r[:40]))
            continue
        kept.append(m)
    return kept, removed


def main():
    # Backup (never overwrite an existing backup)
    if BACKUP.exists():
        idx = 2
        while True:
            cand = ROOT / "data" / f"grammar.json.bak_2026_05_24_remaining_v{idx}"
            if not cand.exists():
                shutil.copy2(GRAMMAR_JSON, cand)
                print(f"Backup -> {cand.name}")
                break
            idx += 1
    else:
        shutil.copy2(GRAMMAR_JSON, BACKUP)
        print(f"Backup -> {BACKUP.name}")

    g = json.loads(GRAMMAR_JSON.read_text(encoding="utf-8"))
    patterns = {p["id"]: p for p in g["patterns"]}

    # === P2: DROPPED — removing empty common_mistakes rows breaks JA-51
    # (every pattern must have >=3 categorized common_mistakes). Keep
    # the empty padded rows; they fail TS-03 but unblock the invariant.
    print(f"\nP2 — Empty-row removal: SKIPPED (would break JA-51 invariant; needs authoring instead)")

    # === P3: wire audio for n5-098 ===
    p3 = patterns.get("n5-098")
    p3_count = 0
    if p3:
        for i, ex in enumerate(p3.get("examples") or []):
            expected = f"audio/grammar/n5-098.{i}.mp3"
            audio_file = ROOT / expected
            if audio_file.exists() and not (ex.get("audio") or "").strip():
                ex["audio"] = expected
                p3_count += 1

    print(f"\nP3 — n5-098 audio wiring:")
    print(f"  paths populated  : {p3_count}/10")

    # === P4: replace problematic particle-swap rows ===
    p4_applied = 0
    p4_skipped = []
    for fx in P4_REPLACEMENTS:
        p = patterns.get(fx["pid"])
        if not p:
            p4_skipped.append(f"{fx['pid']}: pattern not found")
            continue
        cms = p.get("common_mistakes") or []
        i = fx["cm_index"]
        if i >= len(cms):
            p4_skipped.append(f"{fx['pid']}.cm[{i}]: out of range (len={len(cms)})")
            continue
        cm = cms[i]
        if cm.get("wrong", "").strip() != fx["expect_wrong"]:
            p4_skipped.append(f"{fx['pid']}.cm[{i}]: expected wrong='{fx['expect_wrong']}' but found '{cm.get('wrong','')[:60]}'")
            continue
        cm["wrong"] = fx["new_wrong"]
        cm["right"] = fx["new_right"]
        cm["why"] = fx["new_why"]
        p4_applied += 1

    print(f"\nP4 — Particle-swap row replacement:")
    print(f"  rows replaced    : {p4_applied}/{len(P4_REPLACEMENTS)}")
    for s in p4_skipped:
        print(f"  SKIPPED          : {s}")

    # === Write grammar.json ===
    GRAMMAR_JSON.write_text(json.dumps(g, ensure_ascii=False, indent=2), encoding="utf-8")
    on_disk_size = GRAMMAR_JSON.stat().st_size
    # JA-125 uses an LF-normalized byte count (git-storage representation),
    # not the raw on-disk size — Windows CRLF endings inflate the on-disk
    # value. Recompute the size the same way the integrity check does.
    with open(GRAMMAR_JSON, "rb") as fh:
        lf_size = len(fh.read().replace(b"\r\n", b"\n"))
    print(f"\nWrote grammar.json ({on_disk_size} bytes on-disk, {lf_size} LF-normalised)")

    # === Update index.json size_bytes (JA-125 invariant) ===
    idx = json.loads(INDEX_JSON.read_text(encoding="utf-8"))
    for f in idx.get("files", []):
        if f.get("path") == "data/grammar.json":
            old_size = f.get("size_bytes")
            f["size_bytes"] = lf_size
            print(f"Updated index.json size_bytes: {old_size} -> {lf_size} (LF-normalised)")
            break
    INDEX_JSON.write_text(json.dumps(idx, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
