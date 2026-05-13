"""Migrate inline pedagogical reading annotations from KnowledgeBank/kanji_n5.md
into data/kanji.json as a `reading_notes` field.

Extracts the 17 kanji entries that carry annotations like
'[N4+ prefix; recognition only]' or 'kun reading X is N4+; not tested
at N5'. Captures them as structured notes so KB can be deleted without
information loss.
"""
import json
import io
import sys
import shutil

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

# Hand-curated migration of the 17 annotated entries from KB/kanji_n5.md
# Each entry: glyph -> list of notes (one per annotated reading or scope note)
READING_NOTES = {
    "万": ["バン on-reading is rare/specialized; not N5."],
    "円": ["Primary N5 use is in compounds like 100円.",
           "Kun reading まる(い) 'round' is N4+; not tested at N5."],
    "木": ["Kun こ- is N4+ prefix; recognition only."],
    "金": ["Kun かな- is N4+ prefix; recognition only."],
    "半": ["Kun なか(ば) is N3+ noun reading; recognition only."],
    "何": ["On カ is N3+ reading; recognition only."],
    "語": ["Kun かた(る) is N3 verb reading; recognition only."],
    "小": ["Kun こ- is N4+ prefix.",
           "Kun お- is N4+ prefix."],
    "上": ["Kun あ(げる) is N4+ verb reading; listed for recognition only."],
    "下": ["Kun さ(げる) is N4+ verb reading; listed for recognition only."],
    "後": ["Kun のち is N4+ literary reading."],
    "見": ["Kun み(える) is N4 verb reading; recognition only.",
           "Kun み(せる) is N4-N5 borderline (見せる 'to show')."],
    "聞": ["Kun き(こえる) is N4 verb reading; recognition only."],
    "来": ["Kun きた(る) is N3+ literary reading."],
    "行": ["Kun ゆ(く) is N4+ poetic alternative of い(く).",
           "Kun おこな(う) is N3 verb reading."],
    "新": ["Kun あら(た) is N3 stem reading.",
           "Kun にい- is N4+ prefix; recognition only."],
    "白": ["Kun しら- is N3+ prefix; recognition only."],
}

KANJI = "data/kanji.json"
KANJI_BAK = "data/kanji.json.bak_2026_05_14_kb_migration"

shutil.copy2(KANJI, KANJI_BAK)
print(f"Backed up kanji.json to {KANJI_BAK}")

with open(KANJI, encoding="utf-8") as f:
    g = json.load(f)

entries = g.get("entries", g) if isinstance(g, dict) else g
if isinstance(entries, dict):
    entry_list = list(entries.values())
else:
    entry_list = entries

added = 0
for k in entry_list:
    glyph = k.get("glyph")
    if glyph in READING_NOTES:
        k["reading_notes"] = READING_NOTES[glyph]
        k["reading_notes_provenance"] = "kb_migration_2026_05_14"
        added += 1
        print(f"  {glyph}: added {len(READING_NOTES[glyph])} notes")

print(f"\nAdded reading_notes to {added}/{len(READING_NOTES)} expected kanji entries")

with open(KANJI, "w", encoding="utf-8") as f:
    json.dump(g, f, ensure_ascii=False, indent=2)
print(f"Written {KANJI}")
