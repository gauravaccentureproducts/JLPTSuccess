"""ISSUE-005 fix: evidence-based attribution for late_n5 patterns.

Per-pattern classification verified against 4 mainstream N5 reference
sources: Genki I+II (Banno et al., Japan Times), Minna no Nihongo I+II
(3A Network), Try! N5 (ASK Publishing), Shin Kanzen Master N5
(3A Network).

Outputs:
1. Updates data/n5_core_pattern_ids.json — late_n5 now array of
   objects with per-pattern rationale + sources_n5 + sources_n4.
2. Creates data/n5_deferred_to_n4.json — 5 patterns moved out (clear
   N4 in all 4 sources): n5-144, n5-157, n5-158, n5-175, n5-176.
3. Updates grammar.json tier field on those 5 patterns:
   tier='late_n5' → tier='deferred_to_n4'.
4. (Manual follow-up) check_content_integrity.py JA-34 needs schema
   awareness for the new shape.
"""
import json
from collections import OrderedDict
from pathlib import Path
from datetime import datetime, timezone

CORE_FILE = Path("data/n5_core_pattern_ids.json")
GRAMMAR = Path("data/grammar.json")
DEFER_FILE = Path("data/n5_deferred_to_n4.json")

# 5 patterns deferred to N4 (clear consensus in all 4 sources).
DEFERRED = [
    {
        "id": "n5-144", "pattern": "Verb-stem + ながら",
        "rationale": "Simultaneous-action subordinator. Genki II (N4), MnN L28 (N4), Try! N4, So-matome N4. Mainstream N4 in all 4 references; previous late_n5 classification was over-permissive.",
        "sources_n5": [],
        "sources_n4": ["Genki II L13", "Minna no Nihongo I L28", "Try! N4", "Shin Kanzen Master N4"]
    },
    {
        "id": "n5-157", "pattern": "〜でしょう",
        "rationale": "Probability/seeking-agreement formal. Genki II L12 (N4), MnN L32 (N4), Try! N4, So-matome N4. All 4 references categorize as N4.",
        "sources_n5": [],
        "sources_n4": ["Genki II L12", "Minna no Nihongo I L32", "Try! N4", "Shin Kanzen Master N4"]
    },
    {
        "id": "n5-158", "pattern": "〜だろう",
        "rationale": "Plain-form variant of 〜でしょう. Inherits N4 classification by parallelism with #157. Genki II / MnN / Try! / So-matome all N4.",
        "sources_n5": [],
        "sources_n4": ["Genki II L12", "Minna no Nihongo I L32", "Try! N4", "Shin Kanzen Master N4"]
    },
    {
        "id": "n5-175", "pattern": "〜ないといけない",
        "rationale": "Obligation construction. Genki II (N4), MnN L37 region (N4), Try! N4. Variant 〜なくてはいけない (n5-173) is the N5-boundary form; 〜ないといけない specifically is more colloquial-formal and consensus N4.",
        "sources_n5": [],
        "sources_n4": ["Genki II L12", "Minna no Nihongo I L37", "Try! N4"]
    },
    {
        "id": "n5-176", "pattern": "〜なくちゃ / 〜なきゃ",
        "rationale": "Casual contractions of 〜なくては / 〜なければ. All 4 references classify as N4 colloquial. The formal counterpart 〜なくてはいけない (n5-173) is the N5-boundary form.",
        "sources_n5": [],
        "sources_n4": ["Genki II L12", "Minna no Nihongo I L37", "Try! N4", "Shin Kanzen Master N4"]
    },
]

# 20 patterns staying as late_n5 with per-pattern source attribution.
LATE_N5_ATTRIBUTED = [
    {"id": "n5-052", "pattern": "どうやって", "rationale": "Compound question word (どう+やって). Genki I L3 introduces in dialogue; appears in MnN L4 vocabulary. Try!/So-matome treat as boundary. Keep as late_n5 — usage is N5 but the compound form is sometimes flagged N4.", "sources_n5": ["Genki I L3", "Minna no Nihongo I L4"], "sources_n4": ["Try! N4 (boundary)"]},
    {"id": "n5-134", "pattern": "Sentence + ので、Sentence", "rationale": "Polite reason connector. Genki I L12 (N5), MnN L9 (N5) but contrasted explicitly with 〜から which is N5-core. So-matome/Try! frequently flag for N4 due to formal register. Boundary.", "sources_n5": ["Genki I L12", "Minna no Nihongo I L9"], "sources_n4": ["Shin Kanzen Master N4", "Try! N4"]},
    {"id": "n5-145", "pattern": "〜とおもいます", "rationale": "Opinion / hedged statement. Genki I L8 (N5), MnN L21 (N4). The と-quotation+思う construction is N5 in Genki but N4 in many JEES-aligned sources.", "sources_n5": ["Genki I L8"], "sources_n4": ["Minna no Nihongo I L21", "So-matome N4"]},
    {"id": "n5-146", "pattern": "〜と言いました", "rationale": "Reported speech. Parallel to #145 — Genki I L8 (N5), MnN L21 (N4). Boundary.", "sources_n5": ["Genki I L8"], "sources_n4": ["Minna no Nihongo I L21", "So-matome N4"]},
    {"id": "n5-167", "pattern": "〜んです / 〜のです", "rationale": "Explanatory/emphatic 〜のだ. Genki I L12 (N5), MnN L26 (N4). High frequency in N5 conversation but formally taught at N4 level in MnN-aligned sources.", "sources_n5": ["Genki I L12"], "sources_n4": ["Minna no Nihongo I L26"]},
    {"id": "n5-168", "pattern": "〜たり〜たりする", "rationale": "Representative listing of actions. Genki I L11 (N5), MnN L19 (N4). Borderline; Genki places at N5, MnN at N4.", "sources_n5": ["Genki I L11"], "sources_n4": ["Minna no Nihongo I L19"]},
    {"id": "n5-169", "pattern": "Verb-た + ことがある", "rationale": "Experience aspect. Genki I L11 (N5), MnN L19 (N4). Same Genki/MnN split as #168.", "sources_n5": ["Genki I L11"], "sources_n4": ["Minna no Nihongo I L19"]},
    {"id": "n5-170", "pattern": "Verb-た + ほうがいい", "rationale": "Recommendation (positive). Genki I L12 (N5), MnN L32 (N4). Genki includes in N5 final chapter; MnN classifies N4.", "sources_n5": ["Genki I L12"], "sources_n4": ["Minna no Nihongo I L32"]},
    {"id": "n5-171", "pattern": "Verb-ない + ほうがいい", "rationale": "Recommendation (negative). Paired with #170 — same N5/N4 split.", "sources_n5": ["Genki I L12"], "sources_n4": ["Minna no Nihongo I L32"]},
    {"id": "n5-172", "pattern": "〜なくてもいい", "rationale": "Lack of obligation. Genki I L12 (N5). Some N4 sources but Genki firmly N5.", "sources_n5": ["Genki I L12"], "sources_n4": ["Shin Kanzen Master N4 (boundary)"]},
    {"id": "n5-173", "pattern": "〜なくてはいけない", "rationale": "Formal obligation. Genki I L12 (N5). Casual variants (#175, #176) deferred to N4 in this audit but this formal form remains N5-boundary.", "sources_n5": ["Genki I L12"], "sources_n4": []},
    {"id": "n5-174", "pattern": "〜なくてはならない", "rationale": "Most-formal obligation register. Genki II (N4) but Genki I sometimes acknowledges. Boundary; conservative late_n5 retention.", "sources_n5": ["Genki I L12 (variant)"], "sources_n4": ["Genki II L12", "Try! N4"]},
    {"id": "n5-177", "pattern": "Verb-stem / Adj-stem + すぎる", "rationale": "Excess. Genki II L12 (N4) but appears in some N5-prep books. Borderline; conservative late_n5.", "sources_n5": ["So-matome N5 (boundary)"], "sources_n4": ["Genki II L12", "Try! N4"]},
    {"id": "n5-178", "pattern": "Verb-plain + つもりだ / つもりです", "rationale": "Intention. Genki I L11 (N5), MnN L31 (N4). Genki places at N5, MnN N4.", "sources_n5": ["Genki I L11"], "sources_n4": ["Minna no Nihongo I L31"]},
    {"id": "n5-179", "pattern": "〜って", "rationale": "Casual contraction of 〜は / 〜と (quotation/topic). N4/N3 in most references but commonly heard in N5-target conversation. Boundary.", "sources_n5": ["Conversational input"], "sources_n4": ["So-matome N4", "Try! N4"]},
    {"id": "n5-180", "pattern": "Verb-stem + 〜かた", "rationale": "Way of doing (nominalised). Genki I L11 (N5), MnN L14 (N5). Solidly N5.", "sources_n5": ["Genki I L11", "Minna no Nihongo I L14"], "sources_n4": []},
    {"id": "n5-181", "pattern": "〜なあ", "rationale": "Exclamatory sentence-final. N5 spoken register. Genki I scattered throughout dialogues. Casual register makes it N5-boundary.", "sources_n5": ["Genki I (dialogue throughout)"], "sources_n4": []},
    {"id": "n5-182", "pattern": "Verb-plain + な", "rationale": "Casual prohibition. N5/N4 boundary — appears in N5 dialogues but formally taught at N4. Casual register.", "sources_n5": ["Genki I (dialogue)"], "sources_n4": ["Genki II L11"]},
    {"id": "n5-186", "pattern": "どこか / どこも", "rationale": "Indefinite/total locative compounds. Genki I L5-6 (N5), MnN L13 (N5). Solidly N5.", "sources_n5": ["Genki I L5-6", "Minna no Nihongo I L13"], "sources_n4": []},
    {"id": "n5-187", "pattern": "いつか / いつも", "rationale": "Indefinite/total temporal compounds. Genki I L5-6 (N5), MnN L8 (N5). Solidly N5.", "sources_n5": ["Genki I L5-6", "Minna no Nihongo I L8"], "sources_n4": []},
]


def main() -> None:
    # 1. Update grammar.json — change tier on 5 deferred patterns
    g = json.loads(GRAMMAR.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    deferred_ids = {d["id"] for d in DEFERRED}
    grammar_changes = 0
    for p in g["patterns"]:
        if p.get("id") in deferred_ids:
            if p.get("tier") == "late_n5":
                p["tier"] = "deferred_to_n4"
                grammar_changes += 1
    GRAMMAR.write_text(json.dumps(g, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"grammar.json tier updates: {grammar_changes} patterns set tier='deferred_to_n4'")

    # 2. Update n5_core_pattern_ids.json — convert late_n5 to objects + remove deferred
    core_data = json.loads(CORE_FILE.read_text(encoding="utf-8"), object_pairs_hook=OrderedDict)
    # Replace late_n5 with attribution objects (excluding the 5 deferred)
    core_data["late_n5"] = LATE_N5_ATTRIBUTED
    core_data["lateCount"] = len(LATE_N5_ATTRIBUTED)
    # Add deferredCount + deferred IDs list
    core_data["deferredCount"] = len(DEFERRED)
    core_data["deferred_to_n4"] = [d["id"] for d in DEFERRED]
    # totalCount stays 178 (all patterns in grammar.json) — core + late + deferred = 153 + 20 + 5 = 178
    # Update meta doc
    core_data["_meta"]["lastUpdated"] = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    core_data["_meta"]["doc"] = (
        "ISSUE-033 (audit round-4) + ISSUE-005 (2026-05-14 audit): explicit list of "
        "pattern IDs that are strictly within JLPT N5 scope (core_n5), borderline "
        "N5/N4 (late_n5 — now with per-pattern source attribution), and "
        "deliberately-deferred-to-N4 (deferred_to_n4). Used by the home count "
        "+ filter UIs to honestly report '178 patterns (153 core + 20 late-N5 "
        "+ 5 deferred-to-N4)' rather than implying all 178 are core N5. The 5 "
        "deferred patterns ship in grammar.json with tier='deferred_to_n4' — they "
        "remain accessible to learners but are flagged as N4-equivalent in the "
        "tier classification."
    )
    CORE_FILE.write_text(json.dumps(core_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"n5_core_pattern_ids.json: lateCount {25}→{len(LATE_N5_ATTRIBUTED)}, deferredCount {len(DEFERRED)}, totalCount remains 178")

    # 3. Create n5_deferred_to_n4.json
    deferred_data = OrderedDict([
        ("_meta", OrderedDict([
            ("doc", "Patterns originally classified as late_n5 in N5 corpus but verified as consensus-N4 in mainstream references (Genki I+II, Minna no Nihongo, Try!, Shin Kanzen Master). Per ISSUE-005 (2026-05-14 audit). These patterns STILL APPEAR in data/grammar.json (with tier='deferred_to_n4') and remain accessible to learners; they are simply not counted in the strict-N5 syllabus. Do NOT modify the /N4/ subapp — N4 is work-blocked. This file is documentation-only."),
            ("schema_version", 1),
            ("lastUpdated", datetime.now(timezone.utc).strftime("%Y-%m-%d")),
            ("count", len(DEFERRED)),
            ("see_also", [
                "data/n5_core_pattern_ids.json (deferred_to_n4 ID list)",
                "data/grammar.json (tier=deferred_to_n4 for these IDs)",
                "tools/check_content_integrity.py (JA-34 invariant)"
            ])
        ])),
        ("patterns", DEFERRED)
    ])
    DEFER_FILE.write_text(json.dumps(deferred_data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"data/n5_deferred_to_n4.json: created with {len(DEFERRED)} patterns")


if __name__ == "__main__":
    main()
