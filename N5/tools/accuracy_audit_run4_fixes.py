"""Accuracy-audit run-4 fixes for F-1 + F-2 (n5-166 cross-contamination).

F-1: meaning_ja describes の particle, not set greetings. Replace with
     corrected text + re-derive _meaning_ja_markers from the new text.

F-2: examples[5] and examples[6] are off-topic (comparison / simple
     statement) — replace with set-greeting variants using ただいま,
     おかえりなさい, いってらっしゃい (all confirmed N5 vocab).

Run-4 root cause: when the install_ja75_marker_dict.py script bootstrapped
markers (2026-05-13 morning), n5-166 already had the wrong meaning_ja
text. The auto-extractor took distinctive tokens from the WRONG text,
producing markers that self-match (so JA-75 passes). JA-71 passes via
fallback (set-greeting katakana shares chars with meaning_ja). Both
guards fail open on the bootstrap-with-wrong-state case.

Follow-up: add JA-80 invariant that cross-checks meaning_ja contains at
least one ≥3-char Japanese substring from meaning_en, catching the
specific case where the install script blessed the wrong markers.
"""
import json
import io
import sys
import shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

GRAMMAR = "data/grammar.json"
GRAMMAR_BAK = "data/grammar.json.bak_2026_05_13_n5_166_fix"

# Backup
shutil.copy2(GRAMMAR, GRAMMAR_BAK)
print(f"Backed up grammar.json to {GRAMMAR_BAK}")

g = json.load(open(GRAMMAR, encoding="utf-8"))

target = None
for p in g["patterns"]:
    if p["id"] == "n5-166":
        target = p
        break

assert target is not None, "n5-166 not found"

# ----- F-1: meaning_ja rewrite -----
NEW_MEANING_JA = (
    "きまった あいさつの ことばです。"
    "「いただきます」(ごはんの まえ)、"
    "「ごちそうさま」(ごはんの あと)、"
    "「おはようございます」(あさ)、"
    "「いってきます」(でかける とき)、"
    "「こんにちは」(ひる)。"
    "これらは そのまま おぼえます。"
)

print(f"\nOLD meaning_ja: {target['meaning_ja']!r}")
target["meaning_ja"] = NEW_MEANING_JA
print(f"NEW meaning_ja: {NEW_MEANING_JA!r}")

# ----- F-1: re-derive _meaning_ja_markers -----
# Pull distinctive content tokens from the new text. Snapshot the
# verified-correct meaning_ja's vocabulary so JA-75 going forward.
NEW_MARKERS = [
    "いただきます",
    "ごちそうさま",
    "おはようございます",
    "いってきます",
    "あいさつ",
    "きまった",
    "おぼえます",
    "ごはんの まえ",
    "ごはんの あと",
    "そのまま",
]
print(f"\nOLD _meaning_ja_markers: {target.get('_meaning_ja_markers')}")
target["_meaning_ja_markers"] = NEW_MARKERS
print(f"NEW _meaning_ja_markers: {NEW_MARKERS}")

# Verify JA-75 will pass:
# (a) ≥2 markers in meaning_ja OR (b) ≥1 distinctive (≥3-char) marker
matched = [m for m in NEW_MARKERS if m in NEW_MEANING_JA]
distinctive = [m for m in matched if len(m) >= 3]
print(f"\nJA-75 self-check: matched={len(matched)} markers; distinctive={len(distinctive)}")
assert len(matched) >= 2 or len(distinctive) >= 1, "JA-75 would fail!"

# ----- F-2: replace examples [5] and [6] -----
exs = target["examples"]
print(f"\nOLD ex[5]: {exs[5]['ja']!r}")
print(f"OLD ex[6]: {exs[6]['ja']!r}")

# Preserve existing keys/structure; only replace ja + vocab_ids
exs[5] = {
    **exs[5],
    "ja": "「いってらっしゃい」と かぞくに いいます。",
    "vocab_ids": [
        "n5.vocab.36-greetings-and-set-phr.いってらっしゃい",
        "n5.vocab.2-people-family.かぞく",
        "n5.vocab.27-verbs-group-1-verbs.言う",
    ],
}
exs[6] = {
    **exs[6],
    "ja": "「ただいま」と いえに かえった とき いいます。",
    "vocab_ids": [
        "n5.vocab.36-greetings-and-set-phr.ただいま",
        "n5.vocab.26-house-and-furniture.いえ",
        "n5.vocab.27-verbs-group-1-verbs.かえる",
        "n5.vocab.27-verbs-group-1-verbs.言う",
    ],
}
print(f"NEW ex[5]: {exs[5]['ja']!r}")
print(f"NEW ex[6]: {exs[6]['ja']!r}")

# Provenance flag
target["meaning_ja_provenance"] = "n5_166_cross_contamination_fix_2026_05_13_run4"

# Write
with open(GRAMMAR, "w", encoding="utf-8") as f:
    json.dump(g, f, ensure_ascii=False, indent=2)

print(f"\nWritten {GRAMMAR} — n5-166 cross-contamination fixed")
