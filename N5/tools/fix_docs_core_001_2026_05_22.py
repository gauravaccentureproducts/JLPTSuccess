"""Close DOCS-CORE-001 (BUG-157) — add scope='n4' + scope_note to the 5
grammar.json entries classified deferred_to_n4 in n5_core_pattern_ids.json.
Also add a grammar_n5 dual-count to version.json.counts.

Fix option (b) per the bug spec — preserves the audit trail in
n5_core_pattern_ids.json while giving downstream consumers (lint,
UI, paper-builder) a clean `scope === 'n5'` filter.
"""
import sys, io, os, shutil, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_22"

DEFERRED = {
    "n5-144": {
        "scope_note": "Deferred to N4 per n5_core_pattern_ids.json deferred_to_n4 classification. Verb-stem + ながら is mainstream N4 in Genki II L13, Minna no Nihongo I L28, Try! N4, Shin Kanzen Master N4. Previous late_n5 classification was over-permissive. Retained in grammar.json for traceability + future N4 build; scope='n4' filters it out of N5-only consumers.",
    },
    "n5-157": {
        "scope_note": "Deferred to N4 per n5_core_pattern_ids.json deferred_to_n4 classification. 〜でしょう (probability / seeking-agreement formal) is consensus N4 across Genki II L12, Minna no Nihongo I L32, Try! N4, Shin Kanzen Master N4. scope='n4' filters it out of N5-only consumers.",
    },
    "n5-158": {
        "scope_note": "Deferred to N4 per n5_core_pattern_ids.json deferred_to_n4 classification. 〜だろう is the plain-form variant of 〜でしょう (n5-157); inherits N4 classification by parallelism. Genki II / Minna no Nihongo I / Try! / Shin Kanzen Master all categorize as N4. scope='n4' filters it out of N5-only consumers.",
    },
    "n5-175": {
        "scope_note": "Deferred to N4 per n5_core_pattern_ids.json deferred_to_n4 classification. 〜ないといけない (obligation, colloquial-formal) is consensus N4 across Genki II L12, Minna no Nihongo I L37 region, Try! N4. The variant 〜なくてはいけない (n5-173) is the N5-boundary form retained in scope. scope='n4' filters this entry out of N5-only consumers.",
    },
    "n5-176": {
        "scope_note": "Deferred to N4 per n5_core_pattern_ids.json deferred_to_n4 classification. 〜なくちゃ / 〜なきゃ are casual contractions of 〜なくては / 〜なければ. All 4 references (Genki II, Minna no Nihongo I, Try! N4, Shin Kanzen Master N4) classify as N4 colloquial. The formal counterpart 〜なくてはいけない (n5-173) is the N5-boundary form retained. scope='n4' filters this entry out of N5-only consumers.",
    },
}


def backup(fp):
    bak = fp + f".bak_{TODAY}_docs_core_001"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)


def main():
    # 1. Add scope + scope_note to 5 grammar.json entries
    gfp = os.path.join(REPO_N5, "data", "grammar.json")
    with open(gfp, "r", encoding="utf-8") as f:
        g = json.load(f)
    grammar_list = g if isinstance(g, list) else g.get("patterns", g.get("grammar", []))
    touched = 0
    for entry in grammar_list:
        if not isinstance(entry, dict):
            continue
        eid = entry.get("id")
        if eid in DEFERRED:
            entry["scope"] = "n4"
            entry["scope_note"] = DEFERRED[eid]["scope_note"]
            print(f"  {eid}: added scope='n4' + scope_note")
            touched += 1
    if touched != len(DEFERRED):
        print(f"  WARNING: expected {len(DEFERRED)} entries, touched {touched}")
    backup(gfp)
    with open(gfp, "w", encoding="utf-8") as f:
        json.dump(g, f, ensure_ascii=False, indent=2)

    # 2. Add grammar_n5 dual-count to version.json.counts
    vfp = os.path.join(REPO_N5, "data", "version.json")
    with open(vfp, "r", encoding="utf-8") as f:
        v = json.load(f)
    counts = v.setdefault("counts", {})
    n5_count = len([e for e in grammar_list if isinstance(e, dict) and e.get("scope") != "n4"])
    counts["grammar_n5"] = n5_count
    print(f"  version.json.counts.grammar_n5 = {n5_count} (total grammar still {counts.get('grammar')})")
    backup(vfp)
    with open(vfp, "w", encoding="utf-8") as f:
        json.dump(v, f, ensure_ascii=False, indent=2)

    print()
    print("=== Done ===")
    print(f"  grammar.json entries touched: {touched}")
    print(f"  version.json.counts.grammar_n5: {n5_count}")


if __name__ == "__main__":
    main()
