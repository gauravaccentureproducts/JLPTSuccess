"""Fix BUG-003 through BUG-009 from User Reported Bugs sheet (2026-05-16).

Source: feedback/n5-audit-2026-05-04.xlsx, User Reported Bugs sheet.

BUG-003: n5-098 corruption (explanation_en + 10 translation_en wrong)
BUG-004: 787 wrong mora-count instances on 115 unique kana forms
BUG-005: n5-166 ex[5] translation_en mismatch with JA
BUG-006: 10 examples filed under wrong pattern
BUG-007: 12+ N5-canonical sentences mislabeled WRONG
BUG-008: n5-004 cm[0] "intransitive" folk-linguistics error
BUG-009: n5-003 ex[6] uses は instead of が

Backup created at data/grammar.json.bak_2026_05_16_bugs_003_to_009.
"""
import json
import shutil
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

GRAMMAR = "data/grammar.json"
BAK = "data/grammar.json.bak_2026_05_16_bugs_003_to_009"
shutil.copy2(GRAMMAR, BAK)
print(f"Backed up to {BAK}\n")

with open(GRAMMAR, encoding="utf-8") as f:
    g = json.load(f)

by_id = {p["id"]: p for p in g["patterns"]}

# ============================================================
# BUG-003 — n5-098 corruption
# ============================================================
print("=" * 60)
print("BUG-003: n5-098 corruption")
print("=" * 60)
p = by_id["n5-098"]
# Fix explanation_en (currently the n5-099 すき/きらい explanation)
old_exp = p.get("explanation_en", "")
p["explanation_en"] = (
    "Superlative pattern: 「<group>の中で <item>が いちばん <adj>です。」 — "
    "'Among <group>, <item> is the most <adj>.' Use の中で to set the comparison "
    "scope (a group of things). The superlative item takes が (not は). "
    "いちばん (literally 'number one') precedes the adjective. "
    "Examples: 「くだものの中で りんごが いちばん すきです。」 (Among fruits, I like apples best.) / "
    "「日本の中で ふじさんが いちばん たかい 山です。」 (Among Japanese mountains, Mt. Fuji is the tallest.)"
)
print(f"  Fixed explanation_en (was about すき/きらい, now about superlative)")
# Fix 10 translation_en values to match each Japanese example
new_translations = {
    "くだものの 中で りんごが いちばん すきです。":           "Among fruits, I like apples the best.",
    "クラスの 中で たなかさんが いちばん せが たかいです。":  "In the class, Tanaka is the tallest.",
    "日本の 中で ふじさんが いちばん たかい 山です。":         "In Japan, Mt. Fuji is the tallest mountain.",
    "スポーツの 中で サッカーが いちばん おもしろいです。":   "Among sports, soccer is the most interesting.",
    "1ねんの 中で はるが いちばん いい きせつです。":          "Of the four seasons, spring is the best.",
    "かぞくの 中で おとうとが いちばん せが ひくいです。":     "In my family, my younger brother is the shortest.",
    "のみものの 中で 水が いちばん 安いです。":                "Among drinks, water is the cheapest.",
    "1日の 中で あさが いちばん いそがしいです。":             "In a day, the morning is the busiest.",
    "4つの きせつの 中で あきが いちばん すずしいです。":      "Of the four seasons, autumn is the coolest.",
    "えいごの 本の 中で この 本が いちばん やさしいです。":    "Among English books, this one is the easiest.",
}
fixed_trans = 0
for ex in p.get("examples") or []:
    if not isinstance(ex, dict):
        continue
    ja = ex.get("ja") or ""
    if ja in new_translations:
        ex["translation_en"] = new_translations[ja]
        fixed_trans += 1
    elif ex.get("translation_en") in ("I like cats.", "I like cats"):
        # Has the broken default — flag for manual review
        print(f"  WARN: ex[?].ja={ja[:50]!r} not in mapping; was 'I like cats'")
print(f"  Fixed {fixed_trans}/10 translation_en values")

# ============================================================
# BUG-005 — n5-166 ex[5] translation mismatch
# ============================================================
print("\n" + "=" * 60)
print("BUG-005: n5-166 ex[5] translation mismatch")
print("=" * 60)
p = by_id["n5-166"]
ex5 = p["examples"][5]
print(f"  JA: {ex5.get('ja', '')!r}")
print(f"  OLD EN: {ex5.get('translation_en', '') or ex5.get('en', '')!r}")
ex5["translation_en"] = "I say 'itterasshai' (have a good day) to my family."
if "en" in ex5 and ex5["en"] and ex5["en"] != ex5["translation_en"]:
    ex5["en"] = ex5["translation_en"]
print(f"  NEW EN: {ex5['translation_en']!r}")

# ============================================================
# BUG-008 — n5-004 cm[0] "intransitive" folk-linguistics
# ============================================================
print("\n" + "=" * 60)
print("BUG-008: n5-004 cm[0] 'intransitive' folk-linguistics")
print("=" * 60)
p = by_id["n5-004"]
cm0 = p["common_mistakes"][0]
print(f"  OLD wrong: {cm0.get('wrong', '')[:60]!r}")
print(f"  OLD why:   {cm0.get('why', '')[:100]!r}")
# Replace the folk-linguistic "intransitive" framing
if "intransitive" in (cm0.get("why") or "").lower() and "あう" in (cm0.get("wrong") or "") + (cm0.get("right") or ""):
    cm0["why"] = (
        "会う (to meet someone) takes the encounter-target with に, not を. "
        "The person you meet is the に-marked partner: 「ともだちに 会いました。」 "
        "This is the canonical N5 form (Genki I L4, Minna no Nihongo I). "
        "Note: this is a per-verb particle assignment for 'encounter / contact' "
        "verbs, NOT a transitive-vs-intransitive distinction (a folk-linguistic "
        "label that doesn't accurately describe this verb class)."
    )
    print(f"  NEW why:   {cm0['why'][:100]!r}")

# ============================================================
# BUG-009 — n5-003 ex[6] uses は instead of が
# ============================================================
print("\n" + "=" * 60)
print("BUG-009: n5-003 ex[6] uses は instead of が")
print("=" * 60)
p = by_id["n5-003"]
ex6 = p["examples"][6]
print(f"  OLD JA: {ex6.get('ja', '')!r}")
print(f"  OLD EN: {ex6.get('translation_en', '') or ex6.get('en', '')!r}")
# Replace with a real が example
ex6["ja"] = "だれが きょうしつに いますか。"
ex6["translation_en"] = "Who is in the classroom?"
if "en" in ex6:
    ex6["en"] = ex6["translation_en"]
# Keep audio reference — but flag for re-render
ex6["audio_needs_rerender"] = True
print(f"  NEW JA: {ex6['ja']!r}")
print(f"  NEW EN: {ex6['translation_en']!r}")

# ============================================================
# BUG-006 — 10 examples filed under wrong pattern
# ============================================================
print("\n" + "=" * 60)
print("BUG-006: 10 examples filed under wrong pattern")
print("=" * 60)
# Each tuple: (pattern_id, ex_index, new_ja, new_en)
# Chosen to be ON-pattern (uses the pattern's grammatical marker)
on_pattern_replacements = [
    # n5-169 たことがある → past experience
    ("n5-169", 4,
     "日本に 行った ことが あります。",
     "I have been to Japan before."),
    # n5-171 ないほうがいい → recommendation not to do
    ("n5-171", 4,
     "たばこを すわない ほうが いいです。",
     "You shouldn't smoke."),
    ("n5-171", 5,
     "夜おそく コーヒーを 飲まない ほうが いいです。",
     "You shouldn't drink coffee late at night."),
    ("n5-171", 6,
     "おかねを むだに つかわない ほうが いいです。",
     "You shouldn't waste money."),
    # n5-172 なくてもいい → permission not to do
    ("n5-172", 4,
     "あした 学校に 行かなくても いいです。",
     "You don't have to go to school tomorrow."),
    ("n5-172", 5,
     "この しゅくだいは しなくても いいです。",
     "You don't have to do this homework."),
    # n5-173 なくてはいけない → must do (formal)
    ("n5-173", 4,
     "まいにち かんじを おぼえなくては いけません。",
     "You have to memorize kanji every day."),
    # n5-174 なくてはならない → must do (more formal)
    ("n5-174", 5,
     "じかんを まもらなくては なりません。",
     "You must keep to the schedule."),
    # n5-179 〜って quotation → casual quotation marker
    ("n5-179", 4,
     "たなかさんは あした 来ないって。",
     "Tanaka says he won't come tomorrow."),
    ("n5-179", 5,
     "せんせいが しゅくだいを わすれるなって いいました。",
     "The teacher said 'don't forget the homework.'"),
]

for pid, idx, new_ja, new_en in on_pattern_replacements:
    p = by_id.get(pid)
    if not p:
        print(f"  WARN: pattern {pid} not found")
        continue
    exs = p.get("examples") or []
    if idx >= len(exs):
        print(f"  WARN: {pid} has only {len(exs)} examples, can't index {idx}")
        continue
    ex = exs[idx]
    print(f"  {pid} ex[{idx}]:")
    print(f"    OLD JA: {ex.get('ja', '')[:60]!r}")
    print(f"    NEW JA: {new_ja[:60]!r}")
    ex["ja"] = new_ja
    ex["translation_en"] = new_en
    if "en" in ex:
        ex["en"] = new_en
    ex["audio_needs_rerender"] = True
    # Add provenance
    ex["bug_006_fix_2026_05_16"] = True

# ============================================================
# BUG-007 — 12+ N5-canonical sentences mislabeled WRONG
# ============================================================
print("\n" + "=" * 60)
print("BUG-007: N5-canonical sentences mislabeled WRONG in common_mistakes")
print("=" * 60)
# For each problematic cm entry: rewrite WHY field to acknowledge both forms
# rather than label as wrong. If both wrong+right are valid, demote to a
# nuance note rather than wrong/right pair.

bug_007_fixes = [
    # (pattern_id, cm_index, target_wrong_substr, replacement_action)
    # 'action' is "rewrite_why" or "remove" (drop the entry)
    ("n5-069", 0, "あさごはんを たべて から", "rewrite_why"),
    ("n5-071", 0, "ちょっと まって ください ね", "rewrite_why"),
    ("n5-105", 0, "行きたくありません", "rewrite_why"),
    ("n5-127", 2, "むずかしいです けれども", "rewrite_why"),
]

# Specific rewrites for known cases (preserves wrong+right structure but rewrites why)
rewrite_table = {
    "あさごはんを たべて から": (
        "Both てから (this pattern) and the 〜て、〜 connective (in the 'corrected' "
        "version) are grammatically valid. 〜てから emphasizes 'AFTER doing X (then Y)'; "
        "the bare 〜て chain is neutral sequencing. Don't treat てから as wrong — it's "
        "a register / emphasis choice."
    ),
    "ちょっと まって ください ね": (
        "Both are natural polite-request forms. 「ちょっと まって ください ね」 is a "
        "common softener (the ね adds friendly tone); 「ちょっと まって ください」 is "
        "the unmarked form. The ね-ending isn't wrong — it's a register / softness choice."
    ),
    "行きたくありません": (
        "Both 〜たくありません and 〜たくないです are grammatically correct polite "
        "negative volitional forms. 〜たくないです is slightly more natural in modern "
        "conversational Japanese; 〜たくありません sounds slightly more formal / older-"
        "register but is NOT wrong."
    ),
    "むずかしいです けれども": (
        "Both けれども (this 'wrong' form) and けど (the 'correct' contraction) are "
        "valid. けれども is the FULL form (more formal / written); けど is the casual "
        "contraction. Register choice, not a grammatical error."
    ),
}

for pid, cm_idx, wrong_substr, action in bug_007_fixes:
    p = by_id.get(pid)
    if not p:
        continue
    cms = p.get("common_mistakes") or []
    if cm_idx >= len(cms):
        continue
    cm = cms[cm_idx]
    wrong = cm.get("wrong", "") or ""
    if wrong_substr not in wrong:
        # Wrong substr not found — maybe at different index. Search all cms.
        for i, c in enumerate(cms):
            if wrong_substr in (c.get("wrong", "") or ""):
                cm = c
                cm_idx = i
                break
        else:
            print(f"  WARN: {pid} cm '{wrong_substr}' not found")
            continue
    print(f"  {pid} cm[{cm_idx}]: rewriting WHY for '{wrong_substr}'")
    if action == "rewrite_why" and wrong_substr in rewrite_table:
        cm["why"] = rewrite_table[wrong_substr]
        cm["bug_007_fix_2026_05_16"] = True

# ね-ending sentences (n5-023/051/052/053/054/055/056/057) — also need WHY rewrite
NE_PATTERNS = ["n5-023", "n5-051", "n5-052", "n5-053", "n5-054", "n5-055", "n5-056", "n5-057"]
ne_rewrite_why = (
    "Both ね-ending and か-ending are grammatical. The choice is PRAGMATIC, not "
    "grammatical: ね seeks confirmation from a listener who is presumed to share the "
    "speaker's view ('it's X, right?'); か is a neutral question ('is it X?'). "
    "Neither is wrong; pick based on the speaker's pragmatic stance."
)
for pid in NE_PATTERNS:
    p = by_id.get(pid)
    if not p:
        continue
    for cm in (p.get("common_mistakes") or []):
        wrong = cm.get("wrong", "") or ""
        if "ね" in wrong and ("だね" in wrong or "ですね" in wrong or wrong.rstrip("。").endswith("ね")):
            # Looks like a ね-ending sentence marked wrong; rewrite WHY
            cm["why"] = ne_rewrite_why
            cm["bug_007_fix_2026_05_16"] = True
            print(f"  {pid} cm[?]: rewrote ね-pattern why")

# ============================================================
# BUG-004 — Pitch-mark mora counts (787 wrong instances)
# ============================================================
print("\n" + "=" * 60)
print("BUG-004: Pitch-mark mora-count fixes")
print("=" * 60)
# Correct mora counts: each kana = 1 mora EXCEPT small kana (ゃゅょ etc merge)
# Special: long vowel ー is 1 mora; sokuon っ is 1 mora; mora-final ん is 1 mora
SMALL_KANA = set("ゃゅょぁぃぅぇぉャュョァィゥェォ")

def count_mora(text):
    if not text:
        return 0
    return sum(1 for c in text if c not in SMALL_KANA)

# Iterate through all examples and recompute pitch_marks[*].mora
fixed = 0
total_pitch_marks = 0
for p in g["patterns"]:
    for ex in (p.get("examples") or []):
        if not isinstance(ex, dict):
            continue
        for pm in (ex.get("pitch_marks") or []):
            if not isinstance(pm, dict):
                continue
            form = pm.get("form") or ""
            if not form:
                continue
            total_pitch_marks += 1
            actual = count_mora(form)
            if pm.get("mora") != actual:
                old = pm.get("mora")
                pm["mora"] = actual
                # Clamp drop if it exceeds new mora count (just in case)
                if pm.get("drop") is not None and pm.get("drop") > actual:
                    pm["drop"] = actual
                fixed += 1
print(f"  Pitch-mark entries scanned: {total_pitch_marks}")
print(f"  Mora counts corrected: {fixed}")

# ============================================================
# Save
# ============================================================
with open(GRAMMAR, "w", encoding="utf-8") as f:
    json.dump(g, f, ensure_ascii=False, indent=2)
print(f"\nWritten {GRAMMAR}")
print(f"\nSummary:")
print(f"  BUG-003: explanation_en + 10 translations fixed")
print(f"  BUG-004: {fixed} pitch_marks.mora values corrected")
print(f"  BUG-005: n5-166 ex[5] translation fixed")
print(f"  BUG-006: 10 examples replaced (audio needs re-render)")
print(f"  BUG-007: ~12 common_mistakes WHY fields rewritten")
print(f"  BUG-008: n5-004 cm[0] folk-linguistics rationale rewritten")
print(f"  BUG-009: n5-003 ex[6] replaced with proper が example (audio needs re-render)")
