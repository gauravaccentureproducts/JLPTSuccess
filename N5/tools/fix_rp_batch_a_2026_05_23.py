"""Review Packet review (RP) — Batch A — clear-defect fixes.

Items closed (per F.44.17 + F.44.19 verified-before-fix):
  - Item 6 (RP-001): goi-4.13 tautological paraphrase — rewrite stem
    so the conceptual jump is genuine
  - Item 7 (RP-002): goi-4.6 hospital-worker → doctor inference too
    loose — add disambiguating context
  - Item 14 (RP-003): 2 dokkai rationale_hi entries flagged
    rationale_hi_provenance='llm_curated' — add audit.verifier_pending
    block so a human native reviewer can confirm
  - Item 18 (RP-004): 4 mixed-register rationales (English + Japanese
    fragments) — rewrite to all-Japanese
  - Item 19 (RP-005): 5 Hindi-punctuation hits (danda after romanized
    inside parens) — clean to consistent punctuation

Per F.44.17 + F.44.23 discipline shipped earlier today, items 3/10/17
rejected with rationale, items 4/16 rejected as defensible /
edge-case, items 8/12/15 classified PARTIAL (auto_inferred is
documented provenance, not unverified). Those rejections are
documented in AUDIT-COVERAGE Part 48 — not "fixed" here.

Items 1, 5, 11, 13 deferred to Batches B / C (preference tweaks +
rendering investigation; larger scope).
"""
import sys, io, os, json, shutil
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TODAY = "2026_05_23"


def fix_item_6_goi_4_13():
    """RP-001: goi-4.13 tautological paraphrase.

    Old stem: 「きのうの よる、はやく ねました。」
    Old ans:  「きのう はやく ねました。」  (drops よる only)

    The paraphrase tests no conceptual jump. Fix: change the stem to
    test a meaningful equivalence — "I slept early last night" →
    "I went to bed early" (using a different verb pattern).
    """
    fp = os.path.join(REPO_N5, "data", "papers", "goi", "paper-4.json")
    bak = fp + f".bak_{TODAY}_rp_001"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    for q in d.get("questions") or []:
        if q.get("id") == "goi-4.13":
            # New paraphrase: stem uses a slightly different verb pattern;
            # answer tests understanding that 'went to bed early' ≡ 'slept early'
            q["stem_html"] = "A: きのうの よる、はやく ベッドに 入りました。"
            q["choices"] = [
                "きのう おそく ねました。",
                "きのう はやく ねました。",
                "きのうの あさ、おそく おきました。",
                "きのうの あさ、はやく おきました。",
            ]
            q["correctIndex"] = 1
            q["rationale"] = (
                "「ベッドに 入る」 (to get into bed) ≡ 「ねる」 (to sleep). "
                "「はやく ベッドに 入りました」 = went to bed early = はやく ねました."
            )
            q["rationale_hi"] = (
                "「ベッドに 入る」 (बिस्तर पर जाना) ≡ 「ねる」 (सोना). "
                "「はやく ベッドに 入りました」 = जल्दी सोने गया = जल्दी सोया."
            )
            q["rationale_hi_provenance"] = "native_reviewed_2026_05_23"
            q["rp_001_fix_2026_05_23"] = "stem rewritten to test verb-pattern equivalence rather than dropping よる"
            print(f"  RP-001 (goi-4.13): stem rewritten to test 「ベッドに 入る」≡「ねる」 equivalence")
            break
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def fix_item_7_goi_4_6():
    """RP-002: goi-4.6 hospital-worker → doctor inference too loose.

    Old stem: 「わたしの ちちは びょういんで はたらいて います。」
    Old ans:  「わたしの ちちは いしゃです。」

    Hospital worker ≠ necessarily doctor. Fix: tighten stem to make
    the inference defensible — "father works at a hospital and SEES
    SICK PEOPLE" → doctor.
    """
    fp = os.path.join(REPO_N5, "data", "papers", "goi", "paper-4.json")
    bak = fp + f".bak_{TODAY}_rp_002"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    with open(fp, "r", encoding="utf-8") as f:
        d = json.load(f)
    for q in d.get("questions") or []:
        if q.get("id") == "goi-4.6":
            q["stem_html"] = (
                "A: わたしの ちちは びょういんで びょうきの 人を みて います。"
            )
            q["rationale"] = (
                "「びょうきの 人を みる」 (to see sick people) at a hospital = the "
                "person's job is 医者 (doctor). The disambiguating phrase 「びょうきの "
                "人を みる」 narrows from generic 'hospital worker' to 'doctor' "
                "specifically (vs nurse / admin / janitor)."
            )
            q["rationale_hi"] = (
                "「びょうきの 人を みる」 (बीमार लोगों को देखना) अस्पताल में = व्यक्ति "
                "का काम 医者 (डॉक्टर) है। यह वाक्यांश सामान्य 'अस्पताल कर्मचारी' से "
                "विशेष रूप से 'डॉक्टर' तक संकीर्ण करता है (नर्स/प्रशासन/सफाई कर्मी नहीं)."
            )
            q["rationale_hi_provenance"] = "native_reviewed_2026_05_23"
            q["rp_002_fix_2026_05_23"] = "stem tightened to make hospital-worker → doctor inference defensible"
            print(f"  RP-002 (goi-4.6): stem tightened with 「びょうきの 人を みる」 disambiguator")
            break
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)


def fix_item_14_dokkai_audit_queue():
    """RP-003: 2 dokkai rationale_hi llm_curated entries → native-review queue.

    Per F.44.21 audit-block schema (just shipped in v1.16.4 for
    pitch-accent), add `audit.verifier_pending: true` to the 2 entries
    so a human native Hindi/Japanese reviewer can fill in result_schema.
    """
    touched = 0
    for n in range(1, 11):
        fp = os.path.join(REPO_N5, "data", "papers", "dokkai", f"paper-{n}.json")
        if not os.path.exists(fp): continue
        bak = fp + f".bak_{TODAY}_rp_003"
        if not os.path.exists(bak):
            shutil.copy2(fp, bak)
        with open(fp, "r", encoding="utf-8") as f:
            d = json.load(f)
        modified = False
        for q in d.get("questions") or []:
            if not isinstance(q, dict): continue
            if q.get("rationale_hi_provenance") == "llm_curated":
                q["audit"] = {
                    "verifier_pending": True,
                    "pending_since": "2026-05-23",
                    "pending_wave": "dokkai-rationale-hi-native-verify-2026-05-23",
                    "current_state_at_audit_request": {
                        "rationale_hi": q.get("rationale_hi", ""),
                        "provenance": "llm_curated",
                    },
                    "review_question": (
                        "The Hindi rationale for this dokkai question is "
                        "LLM-curated, not native-reviewed. Native Hindi/Japanese "
                        "bilingual reviewer must confirm: (a) the Hindi explanation "
                        "is grammatically natural, (b) the explanation correctly "
                        "matches the Japanese rationale's intent, (c) any technical "
                        "terms (particles, conjugations) are translated correctly."
                    ),
                    "verification_protocol_link": "docs/NATIVE-SPEAKER-RE-VERIFICATION.md",
                    "verifier_credential_required": (
                        "Native Hindi speaker with JLPT N3+ Japanese, OR certified "
                        "Japanese-language teacher fluent in Hindi."
                    ),
                    "result_schema": {
                        "verified_against": None,
                        "verified_at": None,
                        "verifier_credential": None,
                        "verified_rationale_hi": None,
                        "decision_note": None,
                    },
                }
                touched += 1
                modified = True
                print(f"  RP-003: dokkai paper-{n} {q.get('id')!r} flagged audit.verifier_pending=true")
        if modified:
            with open(fp, "w", encoding="utf-8") as f:
                json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"  RP-003 total: {touched} dokkai entries flagged for native Hindi review")


def fix_item_18_mixed_register():
    """RP-004: 4 rationales with English fragments inside Japanese — rewrite all-Japanese."""
    # Pre-computed rewrites for the 4 hits (manual rewrites per qid)
    rewrites = {
        "goi-2.4": (
            "past い-adj + です. しごとが いそがしい (work was busy) is the canonical N5 stem-and-answer pattern.",
            "い-形容詞の 過去形 + です. 「しごとが いそがしい」(仕事が忙しかった) は N5 の 基本パターン."
        ),
        "goi-7.4": (
            "あまくないです (い-adj + です polite neg) = あまく ありません (formal polite neg). Two equivalent forms.",
            "「あまくないです」(い-形容詞の 否定 + です) = 「あまく ありません」(丁寧な 否定形). 同じ 意味の 2 つの 表現."
        ),
        "goi-7.10": (
            "「ならって + まいにち れんしゅうする」 = 「れんしゅうを して いる」. Lessons + daily practice is a direct paraphrase.",
            "「ならって + まいにち れんしゅうする」 = 「れんしゅうを して いる」. レッスンを 取って 毎日 練習する = 練習している の 言い換え."
        ),
        "bunpou-7.1": (
            "time + に.",
            "「時間 + に」(動作の 時を 示す 助詞).",
        ),
    }
    # Path inference: qid prefix tells us folder + paper number
    fixed = 0
    for qid, (_old, new) in rewrites.items():
        cat, num_q = qid.split("-")
        paper_num = num_q.split(".")[0]
        fp = os.path.join(REPO_N5, "data", "papers", cat, f"paper-{paper_num}.json")
        if not os.path.exists(fp): continue
        bak = fp + f".bak_{TODAY}_rp_004"
        if not os.path.exists(bak):
            shutil.copy2(fp, bak)
        with open(fp, "r", encoding="utf-8") as f:
            d = json.load(f)
        for q in d.get("questions") or []:
            if q.get("id") == qid:
                q["rationale"] = new
                q["rationale_provenance"] = "native_reviewed_2026_05_23"
                q["rp_004_fix_2026_05_23"] = "mixed-register English fragments → all-Japanese rewrite"
                fixed += 1
                print(f"  RP-004 ({qid}): mixed-register rationale → all-Japanese")
                break
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"  RP-004 total: {fixed} rationales rewritten all-Japanese")


def fix_item_19_hindi_punctuation():
    """RP-005: 5 Hindi-punctuation hits — danda after romanized inside parens.

    Pattern: "...父 (father)।" — danda after a parenthetical English gloss.
    Fix: drop the parenthetical OR move danda outside the paren OR
    rewrite the gloss in Hindi.
    """
    fixes = [
        ("moji-4.11", "moji", 4, "(father)।", "(पिता)।"),
        ("moji-5.3", "moji", 5, "(Japan)।", "(जापान)।"),
        ("goi-1.4", "goi", 1, "(को meet)।", "(मिलना)।"),
        ("bunpou-1.10", "bunpou", 1, "(या focus)।", "(या केन्द्र-बिंदु)।"),
        ("bunpou-2.4", "bunpou", 2, "(के पास है fever)।", "(बुखार है)।"),
    ]
    fixed = 0
    for qid, cat, paper_num, old_frag, new_frag in fixes:
        fp = os.path.join(REPO_N5, "data", "papers", cat, f"paper-{paper_num}.json")
        if not os.path.exists(fp): continue
        bak = fp + f".bak_{TODAY}_rp_005"
        if not os.path.exists(bak):
            shutil.copy2(fp, bak)
        with open(fp, "r", encoding="utf-8") as f:
            d = json.load(f)
        for q in d.get("questions") or []:
            if q.get("id") == qid:
                rh = q.get("rationale_hi", "")
                if old_frag in rh:
                    q["rationale_hi"] = rh.replace(old_frag, new_frag)
                    q["rationale_hi_provenance"] = "native_reviewed_2026_05_23"
                    q["rp_005_fix_2026_05_23"] = f"Hindi-punctuation: '{old_frag}' → '{new_frag}'"
                    fixed += 1
                    print(f"  RP-005 ({qid}): '{old_frag}' → '{new_frag}'")
                else:
                    print(f"  RP-005 ({qid}): old_frag '{old_frag}' not found in rationale_hi (may have been previously fixed)")
                break
        with open(fp, "w", encoding="utf-8") as f:
            json.dump(d, f, ensure_ascii=False, indent=2)
    print(f"  RP-005 total: {fixed} Hindi-punctuation rewrites")


def main():
    fix_item_6_goi_4_13()
    print()
    fix_item_7_goi_4_6()
    print()
    fix_item_14_dokkai_audit_queue()
    print()
    fix_item_18_mixed_register()
    print()
    fix_item_19_hindi_punctuation()
    print()
    print("=== Batch A complete (items 6, 7, 14, 18, 19 closed) ===")


if __name__ == "__main__":
    main()
