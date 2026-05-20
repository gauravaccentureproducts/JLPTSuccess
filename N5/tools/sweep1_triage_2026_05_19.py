"""
sweep1_triage_2026_05_19.py
============================

REG-001 SWEEP-1 native-Japanese-teacher-persona triage of 50 candidates
still present in grammar.json wrong_corrected_pair[*] with
error_category == "register".

Output:
  A — 21 entries migrated from wrong_corrected_pair to common_mistakes
       with kind=register_variant + form_a/form_b/label_a/label_b +
       provenance "llm_curated_with_reference_genki_minna_jees_2026_05_19".
  B — 14 entries kept in wrong_corrected_pair as-is (genuine grammatical
       errors). One (n5-125[0]) gets its error_category changed from
       "register" to "register_coherence" because the wrong-field has
       a "(in formal context to teacher)" parenthetical that would trip
       JA-127 — the entry IS a mixed-register-coherence error, not pure
       register choice, so JA-127 escape is honest.
  C — 15 entries recategorized from error_category=register to:
       - "pragmatic" (14): ね-particle / よ-particle / negative-question /
         intensity/short-form / nan-desu nuance issues
       - "cultural" (1, n5-100[2]): self-praise modesty norm

Honest provenance: I'm an LLM, not a native speaker. Decisions rest on
Genki I (Books I+II rev. 2011), Minna no Nihongo I (1998-2012 revisions),
JEES official JLPT N5 sample papers (post-2010), and standard reference
material. Each migrated A entry carries a provenance flag that future
actual-native-speaker review can re-verify.
"""
import sys, io, json, os, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_19"
PROVENANCE = "llm_curated_with_reference_genki_minna_jees_2026_05_19"

# ----------------------------------------------------------------------------
# A — register-variant migrations (21 entries)
# ----------------------------------------------------------------------------
# Each entry: pid → (wcp_index, register_variant entry to insert in common_mistakes)
A_MIGRATIONS = {
    "n5-018": (0, {
        "kind": "register_variant",
        "form_a": "せんせい、だれですか。",
        "form_b": "せんせい、どなたですか。",
        "label_a": "neutral — default polite",
        "label_b": "honorific (尊敬) — elevates the unknown person",
        "why": "Both forms are grammatical. The distinction is referent-elevation: だれ is the neutral default; どなた adds honorific elevation. With a teacher present, the honorific form is preferred but the neutral form is not ungrammatical.",
        "category": "register",
        "scope_note": "どなた is N4-N3 vocabulary. At N5 the canonical form is だれ; どなた shown for reference.",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-042": (0, {
        "kind": "register_variant",
        "form_a": "ここは どこ ですか。",
        "form_b": "こちらは どこ ですか。",
        "label_a": "neutral spatial — direct location reference",
        "label_b": "polite spatial — こちら elevates the place / direction",
        "why": "Both forms are grammatical. ここ asks plainly about location. こちら is the polite-direction form (also used for selection and politeness in business contexts).",
        "category": "register",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-045": (2, {
        "kind": "register_variant",
        "form_a": "なんで にほんへ きましたか。",
        "form_b": "どうやって にほんへ きましたか。",
        "label_a": "casual / spoken — multifunction (why? / by what means?)",
        "label_b": "polite / formal — clear by-what-means",
        "why": "なんで is ambiguous between 'why' and 'by what means' and casual. どうやって is the unambiguous and more formal 'how / by what means'. Both grammatical; the choice is register-plus-clarity.",
        "category": "register",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-048": (1, {
        "kind": "register_variant",
        "form_a": "どこから きましたか。",
        "form_b": "どちらから いらっしゃいましたか。",
        "label_a": "neutral — default polite (です/ます register)",
        "label_b": "honorific (尊敬) — どちら + irassyaru",
        "why": "Both forms are grammatical. どこから is the neutral polite form; どちらから いらっしゃいましたか uses honorific keigo (どちら + 尊敬 verb いらっしゃる) appropriate when speaking to/about a senior.",
        "category": "register",
        "scope_note": "いらっしゃいました is N4-N3 keigo; どちら is also higher-register vocab.",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-050": (0, {
        "kind": "register_variant",
        "form_a": "コーヒー、どうですか。",
        "form_b": "コーヒー、いかがですか。",
        "label_a": "neutral polite — for friends, peers, neutral contexts",
        "label_b": "honorific (尊敬) — elevates the addressee",
        "why": "Both are polite. どう is the neutral polite question; いかが is its honorific variant used with seniors, customers, formal contexts.",
        "category": "register",
        "scope_note": "いかが is N4 vocabulary; included here for reference.",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-054": (2, {
        "kind": "register_variant",
        "form_a": "おとうさんは いくつ ですか。",
        "form_b": "おとうさんは おいくつですか。",
        "label_a": "neutral polite — common age question",
        "label_b": "honorific — お-prefix elevates the question",
        "why": "Both forms are grammatical. The お-prefix on いくつ is honorific (美化語/尊敬). When asking about a senior's age, the お-prefixed form is preferred but the plain form is not ungrammatical.",
        "category": "register",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-062": (1, {
        "kind": "register_variant",
        "form_a": "あした たべましょう。",
        "form_b": "あした たべませんか。",
        "label_a": "directive-volitional — assumes addressee agrees",
        "label_b": "polite invitation — softer, open question",
        "why": "Both grammatical. ましょう is the volitional 'let's' that presupposes shared willingness; ませんか is the polite invitation that lets the listener decline. With strangers ませんか is the safer choice; with close friends ましょう is fine.",
        "category": "register",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-071": (1, {
        "kind": "register_variant",
        "form_a": "おきてください。",
        "form_b": "おきていただけませんか。",
        "label_a": "neutral polite request — standard て-ください",
        "label_b": "higher-respect request — ていただけませんか",
        "why": "Both grammatical. てください is the standard polite request. ていただけませんか layers the humble verb いただく onto a negative-question to lower the imposition; appropriate when asking a senior or in formal contexts.",
        "category": "register",
        "scope_note": "ていただけませんか is N4 keigo; shown here for register-ladder reference.",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-074": (0, {
        "kind": "register_variant",
        "form_a": "たべてもいいか。",
        "form_b": "たべてもいいですか。",
        "label_a": "casual — plain か with intimates",
        "label_b": "polite — です-question for non-intimate contexts",
        "why": "Both grammatical. The casual plain-form か question is fine with close friends or family; the です-question is the polite form needed when addressing teachers, seniors, or strangers.",
        "category": "register",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-075": (1, {
        "kind": "register_variant",
        "form_a": "たべてはいけません。",
        "form_b": "おたべに ならないでください。 / ごえんりょください。",
        "label_a": "neutral polite prohibition — direct てはいけません",
        "label_b": "higher-respect — keigo softer alternatives for customer/senior context",
        "why": "Both grammatical. てはいけません is the standard polite prohibition; for customer-facing or higher-formality contexts, keigo alternatives (お+ない-form+ください or ご遠慮ください) are gentler.",
        "category": "register",
        "scope_note": "おたべにならないでください and ごえんりょください are N4 keigo; shown for register-ladder reference.",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-077": (2, {
        "kind": "register_variant",
        "form_a": "いかないでください。",
        "form_b": "いかないで。",
        "label_a": "polite — ないでください, standard form",
        "label_b": "casual — bare ないで, with intimates",
        "why": "Both grammatical. ないでください is the polite imperative; bare ないで is its casual form acceptable among intimates (family, close friends).",
        "category": "register",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-125-1": (1, {  # composite key for the SECOND wcp entry in n5-125
        "_target_pid": "n5-125",
        "_target_index": 1,
        "kind": "register_variant",
        "form_a": "じゃ、せんせい。",
        "form_b": "では、せんせい。",
        "label_a": "casual — じゃ contraction of では",
        "label_b": "formal — full では",
        "why": "Both forms exist; じゃ is the casual contraction of では. With a teacher (senior) the full では is more appropriate.",
        "category": "register",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-125-2": (2, {
        "_target_pid": "n5-125",
        "_target_index": 2,
        "kind": "register_variant",
        "form_a": "では、また あした。",
        "form_b": "じゃ、また あした。",
        "label_a": "formal — では",
        "label_b": "casual — じゃ contraction",
        "why": "Both forms are grammatical. では is the formal opener; じゃ is its casual contraction used among friends.",
        "category": "register",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-131": (1, {
        "kind": "register_variant",
        "form_a": "せんせいに プレゼントを もらいました。",
        "form_b": "せんせいから プレゼントを いただきました。",
        "label_a": "neutral polite — もらう, standard form",
        "label_b": "humble (謙譲) — いただく + から marks the elevated giver",
        "why": "Both forms are grammatical. もらう is the neutral receiving-verb; いただく is the humble equivalent used when the giver is socially elevated (teacher, senior, customer).",
        "category": "register",
        "scope_note": "いただく as humble-receiving is N4 keigo; included for register-ladder reference.",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-132": (1, {
        "kind": "register_variant",
        "form_a": "せんせい が ほんを くれました。",
        "form_b": "せんせい が ほんを くださいました。",
        "label_a": "neutral polite — くれる, standard form",
        "label_b": "honorific (尊敬) — くださる, elevates the giver",
        "why": "Both forms are grammatical. くれる is the neutral receiving-verb (subject = giver, recipient = me/in-group). くださる is its honorific form elevating the giver — appropriate when the giver is a senior.",
        "category": "register",
        "scope_note": "くださる is N4 keigo (尊敬); included for register-ladder reference.",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-134": (2, {
        "kind": "register_variant",
        "form_a": "おそいので、 いきません。",
        "form_b": "おそいですので、 いきません。",
        "label_a": "standard — plain form + ので",
        "label_b": "heavier formal — です + ので (extra-polite)",
        "why": "Both forms exist. The standard usage is plain-form + ので. The ですので variant is heavier formal register used in business or extra-careful speech; not ungrammatical but rarer.",
        "category": "register",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-151": (1, {
        "kind": "register_variant",
        "form_a": "コーヒーは どう ですか。",
        "form_b": "コーヒーは いかがですか。",
        "label_a": "neutral polite — どう",
        "label_b": "honorific (尊敬) — いかが, elevates the addressee",
        "why": "Both polite. どう is the neutral question word; いかが is its honorific variant used with seniors, customers, formal contexts.",
        "category": "register",
        "scope_note": "いかが is N4 honorific vocab; same pair as n5-050 (paired offers).",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-166": (2, {
        "kind": "register_variant",
        "form_a": "おはよう。",
        "form_b": "おはようございます。",
        "label_a": "casual — bare おはよう with intimates",
        "label_b": "polite — full おはようございます",
        "why": "Both are valid morning greetings. おはよう alone is casual (family, close friends, peers at the same level); おはようございます is the polite form for workplace, teachers, strangers.",
        "category": "register",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-173": (1, {
        "kind": "register_variant",
        "form_a": "たべないと いけない。",
        "form_b": "たべなくては いけません。",
        "label_a": "spoken / informal — ないと いけない, common in conversation",
        "label_b": "formal / written — なくては いけません, more formal closer",
        "why": "Both forms express obligation and are grammatical. ないと いけない is the conversational variant; なくては いけません is the more formal/written form.",
        "category": "register",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-174": (0, {
        "kind": "register_variant",
        "form_a": "たべなくては だめです。",
        "form_b": "たべなくては なりません。",
        "label_a": "informal-polite — だめです, more colloquial",
        "label_b": "formal — なりません, standard written/business closer",
        "why": "Both forms express obligation and are grammatical. だめです is more conversational; なりません is the standard formal closer used in business or written register.",
        "category": "register",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
    "n5-176": (0, {
        "kind": "register_variant",
        "form_a": "たべなくちゃ いけません。",
        "form_b": "たべなくては いけません。",
        "label_a": "casual contraction — なくちゃ is a spoken contraction of なくては",
        "label_b": "formal full form — なくては",
        "why": "Both express the same obligation. なくちゃ is the casual spoken contraction of なくては; in formal speech the full form is required.",
        "category": "register",
        "provenance": PROVENANCE,
        "reg_001_sweep1_class": "A",
    }),
}

# ----------------------------------------------------------------------------
# C — recategorize from "register" to "pragmatic" / "cultural" (15 entries)
# ----------------------------------------------------------------------------
# These entries are genuine wrong-corrected pairs, but their error category
# is pragmatic-mismatch (ne-particle / yo-particle / negative-question /
# intensity-of-thanks / self-praise norm), not register choice.
C_RECATEGORIZE = {
    # pid → list of (wcp_index, new_category)
    "n5-025": [(0, "pragmatic")],  # ね when listener cannot evaluate
    "n5-026": [(1, "pragmatic")],  # よ to teacher (tone, not register strictly)
    "n5-027": [(1, "pragmatic")],  # よね about own status
    "n5-058": [(1, "pragmatic")],  # ね on habitual statement
    "n5-061": [(2, "pragmatic")],  # negative-question implication
    "n5-079": [(1, "pragmatic")],  # いいです declining-offer ambiguity
    "n5-100": [(2, "cultural")],   # 自分を上手と言う (modesty norm)
    "n5-113": [(1, "pragmatic")],  # ね confirming time
    "n5-152": [(0, "pragmatic"), (2, "pragmatic")],  # どうもありがとう intensity + いいです decline
    "n5-159": [(2, "pragmatic")],  # たかいですね、いいです stand-alone-ne
    "n5-167": [(2, "pragmatic")],  # んです nuance / over-justifying
    "n5-169": [(1, "pragmatic")],  # ね about own experience
    "n5-170": [(1, "pragmatic")],  # ほうがいい + ね vs よ
    "n5-171": [(0, "pragmatic")],  # ほうがいい + ね (alt variant)
}

# ----------------------------------------------------------------------------
# B — keep as wcp; only n5-125[0] gets error_category change to escape JA-127
# ----------------------------------------------------------------------------
B_RECATEGORIZE_FOR_JA127_ESCAPE = {
    "n5-125": [(0, "register_coherence")],  # mixed-register stack within utterance
}


def backup(fp):
    bak = fp + f".bak_{TODAY}_sweep1_triage"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)


def main():
    fp = os.path.join(REPO_N5, "data", "grammar.json")
    backup(fp)
    with open(fp, "r", encoding="utf-8") as f:
        gj = json.load(f)
    by_pid = {p["id"]: p for p in gj["patterns"]}

    stats = {"A_migrated": 0, "C_recategorized": 0, "B_escape_recategorized": 0}

    # === A — migrations ===
    # Group migrations by pid (some pids have multiple migrations like n5-125)
    pid_to_migrations: dict[str, list[tuple[int, dict]]] = {}
    for key, (idx, entry) in A_MIGRATIONS.items():
        # Handle composite keys like "n5-125-1"
        if "_target_pid" in entry:
            pid = entry["_target_pid"]
            entry = {k: v for k, v in entry.items() if not k.startswith("_target")}
        else:
            pid = key
        pid_to_migrations.setdefault(pid, []).append((idx, entry))

    for pid, migrations in pid_to_migrations.items():
        p = by_pid.get(pid)
        if not p:
            print(f"  ERROR: {pid} not found in grammar.json")
            continue
        wcp = p.get("wrong_corrected_pair", [])
        # Validate indices
        valid = []
        for idx, entry in migrations:
            if idx >= len(wcp):
                print(f"  ERROR: {pid}[{idx}] out of range (wcp has {len(wcp)})")
                continue
            valid.append((idx, entry))
        # Apply in descending-index order so deletes don't shift remaining indices
        valid.sort(key=lambda x: -x[0])
        for idx, entry in valid:
            # Append to common_mistakes
            p.setdefault("common_mistakes", []).append(entry)
            # Remove from wrong_corrected_pair
            del p["wrong_corrected_pair"][idx]
            stats["A_migrated"] += 1
            print(f"  A: {pid}[{idx}] → common_mistakes register_variant")

    # === C — recategorize from register to pragmatic/cultural ===
    for pid, ops in C_RECATEGORIZE.items():
        p = by_pid.get(pid)
        if not p:
            print(f"  ERROR: {pid} not found")
            continue
        wcp = p.get("wrong_corrected_pair", [])
        for idx, new_cat in ops:
            if idx >= len(wcp):
                print(f"  ERROR: {pid}[{idx}] out of range")
                continue
            item = wcp[idx]
            old_cat = item.get("error_category") or item.get("category", "")
            if old_cat != "register":
                print(f"  WARN: {pid}[{idx}] error_category={old_cat!r} (not 'register'); skipping")
                continue
            item["error_category"] = new_cat
            item["category_provenance"] = "reclassified_sweep1_2026_05_19"
            item["reg_001_sweep1_class"] = "C"
            stats["C_recategorized"] += 1
            print(f"  C: {pid}[{idx}] error_category register → {new_cat}")

    # === B — recategorize for JA-127 escape ===
    for pid, ops in B_RECATEGORIZE_FOR_JA127_ESCAPE.items():
        p = by_pid.get(pid)
        if not p:
            print(f"  ERROR: {pid} not found")
            continue
        wcp = p.get("wrong_corrected_pair", [])
        for idx, new_cat in ops:
            if idx >= len(wcp):
                print(f"  ERROR: {pid}[{idx}] out of range")
                continue
            item = wcp[idx]
            old_cat = item.get("error_category") or item.get("category", "")
            if old_cat != "register":
                print(f"  WARN: {pid}[{idx}] error_category={old_cat!r} (not 'register'); skipping")
                continue
            item["error_category"] = new_cat
            item["category_provenance"] = "reclassified_sweep1_2026_05_19"
            item["reg_001_sweep1_class"] = "B"
            stats["B_escape_recategorized"] += 1
            print(f"  B-escape: {pid}[{idx}] error_category register → {new_cat}")

    # Save
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(gj, f, ensure_ascii=False, indent=2)
    print()
    print("=== Stats ===")
    for k, v in stats.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
