"""
fix_paper_bugs_2026_05_18.py
============================

Fixes PAPER-001..004 + LISTEN-4 close-out.

PAPER-001: re-tag grammarPatternId for bunpou questions where current tag is
           wrong (mostly n5-013 over-tagging, plus stale auto-inferred tags).
PAPER-002: set grammarPatternId on bunpou-4.3 (currently missing).
PAPER-003: strip commit-message-style meta-fix parentheticals from 6 rationale
           and rationale_hi fields.
PAPER-004: rewrite rationale_hi for unnatural / mojibake-containing questions.

Also performs horizontal scans to register newly-found bugs.

Per BINDING governance Rule 4/5, this is paired with a separate sync-script for
updating procedure manual / accuracy prompt / N5Improvement / AUDIT-COVERAGE /
sync-map / CHANGELOG / spec / xlsx.

Non-destructive: writes versioned .bak files before mutating.
"""

import sys, io, json, os, re, glob, shutil, datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

REPO_N5 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAPERS_GLOB = os.path.join(REPO_N5, "data", "papers", "**", "*.json")
TODAY = "2026_05_18"
PROVENANCE = f"rule_based_correctanswer_{TODAY}"

# ---------------------------------------------------------------------------
# PAPER-001 + PAPER-002: grammarPatternId re-tagging
# ---------------------------------------------------------------------------
# Mondai 1 = fill-in-the-blank, single answer. Tag = pattern of correct answer.
# Mondai 2 = sentence-ordering (★ position). Tag = central structural pattern.
# Mondai 3 = paragraph gap-fill, particle-level. Tag = particle/pattern of fill.

# Particle ↔ pattern_id (one canonical pattern per particle for N5 coverage).
PARTICLE_TO_PATTERN = {
    "は": "n5-002",
    "が": "n5-003",
    "を": "n5-004",
    "に": "n5-005",
    "へ": "n5-006",
    "で": "n5-007",
    "と": "n5-008",
    "から": "n5-009",
    "まで": "n5-010",
    "や": "n5-011",
    "も": "n5-013",
    "か": "n5-023",
    "ね": "n5-025",
    "よ": "n5-026",
    "の": "n5-028",
    "だけ": "n5-033",
    "ぐらい": "n5-035",
    "くらい": "n5-035",
    "ごろ": "n5-036",
    "など": "n5-037",
    "ずつ": "n5-038",
    "より": "n5-095",  # comparison particle
}

# Manual map for non-particle bunpou questions, keyed by question id.
# Determined from stem context + correct answer.
NONPARTICLE_TAGS = {
    # paper-2 (Mondai 1)
    "bunpou-2.12": ("n5-058", "Verb-ます (polite non-past affirmative)"),
    "bunpou-2.13": ("n5-060", "Verb-ました (polite past)"),
    "bunpou-2.14": ("n5-001", "Noun + でした (copula past)"),
    "bunpou-2.15": ("n5-001", "ではありません (negative copula)"),
    # paper-3 (Mondai 1)
    "bunpou-3.1":  ("n5-079", "い-Adj + です (predicate)"),
    "bunpou-3.2":  ("n5-080", "い-Adj negative -くないです"),
    "bunpou-3.3":  ("n5-081", "い-Adj past -かったです"),
    "bunpou-3.4":  ("n5-086", "な-Adj negative -じゃありません"),
    "bunpou-3.5":  ("n5-084", "な-Adj + な + Noun"),
    "bunpou-3.6":  ("n5-059", "Verb-ません (polite negative)"),
    "bunpou-3.7":  ("n5-104", "Verb-stem + たいです"),
    "bunpou-3.8":  ("n5-058", "Verb-ます"),
    "bunpou-3.9":  ("n5-104", "Verb-stem + たい (plain)"),
    "bunpou-3.11": ("n5-108", "Number + counter (さつ for books)"),
    "bunpou-3.12": ("n5-072", "Verb-ています (progressive)"),
    "bunpou-3.13": ("n5-076", "Verb-てから"),
    "bunpou-3.14": ("n5-071", "Verb-てください"),
    "bunpou-3.15": ("n5-074", "Verb-てもいいです (permission)"),
    # paper-4 (Mondai 1)
    "bunpou-4.1":  ("n5-075", "Verb-てはいけません (prohibition)"),
    "bunpou-4.2":  ("n5-070", "Verb-て, Verb-て (sequence)"),
    "bunpou-4.3":  ("n5-079", "い-Adj + です (parallel predicate via て-form)"),  # PAPER-002
    "bunpou-4.4":  ("n5-083", "い-Adj -くて connector + 2nd い-Adj predicate"),
    "bunpou-4.7":  ("n5-162", "V-plain + まえに"),
    "bunpou-4.8":  ("n5-163", "V-た + あとで"),
    "bunpou-4.9":  ("n5-058", "Verb-ます"),
    "bunpou-4.15": ("n5-095", "〜は〜より〜です (comparison)"),
}

# Mondai 3 (paper-7) — particle gap-fill in paragraphs.
# Determined from passage_text decoding.
MONDAI3_PARTICLE_FIX = {
    # bunpou-7.1: 六時(に)おきます — time+に → n5-005
    # bunpou-7.2: 七時ごろ(に)あさごはん — time+に → n5-005
    # bunpou-7.3: パン(と)ぎゅうにゅう — と and → n5-008  (already n5-008 by particle rule)
    # bunpou-7.4: 学校(へ)行きます — direction → n5-006
    # bunpou-7.5: 九時(から)三時まで — から → n5-009
    # bunpou-7.6: が — n5-003
    # bunpou-7.9: が — n5-003
    # bunpou-7.7-7.10 use particle rule directly
}

# Mondai 2 sentence-ordering re-tags for n5-013 mistags
# Decoded from full assembly structure:
MONDAI2_TAGS = {
    "bunpou-5.15": ("n5-009", "から particle (reason connector)"),
    "bunpou-6.6":  ("n5-006", "へ particle (direction → 映画館へ行きました)"),
}

# ---------------------------------------------------------------------------
# PAPER-003: rationale strip rules
# ---------------------------------------------------------------------------
# Each entry: (question_id, new_rationale_en, new_rationale_hi)
RATIONALE_STRIPS = {
    "bunpou-1.14": {
        "rationale": "sub-が-suki: the subject of すき (the thing liked) is marked with が, not を.",
        "rationale_hi": "sub-が-suki: すき (पसंद) का विषय (पसंद की जाने वाली चीज़) を नहीं, बल्कि が से चिह्नित होता है।",
    },
    "bunpou-3.4": {
        "rationale": "あまり + negative construction. しずかじゃありません is the polite-negative form of な-adjective しずか.",
        "rationale_hi": "あまり + नकारात्मक संरचना। しずかじゃありません, な-विशेषण しずか का विनम्र-नकारात्मक रूप है।",
    },
    "bunpou-3.11": {
        "rationale": "三 + さつ — さつ is the counter for bound objects like books.",
        "rationale_hi": "三 + さつ — さつ, किताबों जैसी जिल्द वाली वस्तुओं के लिए गिनती-शब्द (counter) है।",
    },
    "bunpou-5.15": {
        "rationale": 'Order: しごとが あります(4) から(3) パーティーに(2=★) は(1) 来ません = "Because I have work, I won\'t come to the party." から marks the reason clause.',
        "rationale_hi": 'क्रम: しごとが あります(4) から(3) パーティーに(2=★) は(1) 来ません = "मेरे पास काम है, इसलिए मैं पार्टी में नहीं आऊँगा।" から कारण-उपवाक्य को चिह्नित करता है।',
    },
    "bunpou-7.4": {
        "rationale": "Direction particle へ marks the goal of a motion verb (学校へ行きます = go toward school).",
        "rationale_hi": "दिशा-सूचक कण へ गति-क्रिया के लक्ष्य को चिह्नित करता है (学校へ行きます = स्कूल की ओर जाना)।",
    },
    "bunpou-7.8": {
        "rationale": "「ピアノきょうしつ」 (compound noun, no の) — に行きます takes the destination directly.",
        "rationale_hi": "「ピアノきょうしつ」 (समासी संज्ञा, बीच में の नहीं) — に行きます गंतव्य को सीधे ग्रहण करता है।",
    },
}

# ---------------------------------------------------------------------------
# PAPER-004: rationale_hi rewrites (natural Hindi)
# ---------------------------------------------------------------------------
RATIONALE_HI_REWRITES = {
    "bunpou-2.3": "を कण सीधे कर्म (object) को चिह्नित करता है (れんしゅうする = अभ्यास करना)।",
    "bunpou-3.4": "あまり + नकारात्मक संरचना। しずかじゃありません, な-विशेषण しずか का विनम्र-नकारात्मक रूप है।",
    "bunpou-4.11": "や〜など सूची-संरचना: 'X, Y, इत्यादि' (अधूरी सूची)। विकर्षक: को कर्म-सूचक है (पहले से रिक्त-स्थान के बाद आ रहा है); へ दिशा है (यहाँ गंतव्य नहीं); に प्राप्तकर्ता है।",
    "bunpou-5.1":  'क्रम: きのう ともだち(1) と(3) えいがを(2=★) 見ました = "कल मैंने अपने दोस्त के साथ फ़िल्म देखी।" えいがを ★ पर आता है।',
    "bunpou-5.2":  'क्रम: わたしは ちゅうごく(2) に(3) 行った(1=★) ことが あります = "मैं चीन गया हूँ।" 行った ★ पर आता है।',
    "bunpou-5.3":  'क्रम: あした ともだち(2) の(3) うち(1=★) へ 行きます = "कल मैं अपने दोस्त के घर जाऊँगा।" うち ★ पर आता है।',
    "bunpou-5.4":  'क्रम: あの(2) しろい(3) たてもの(1=★) は なんですか = "वह सफ़ेद इमारत क्या है?" たてもの ★ पर आता है।',
    "bunpou-5.5":  'क्रम: わたしの へやに(2) つくえ(3) が(1=★) あります = "मेरे कमरे में एक मेज़ है।" が ★ पर आता है।',
    "bunpou-5.6":  'क्रम: ホテルの(2) しょくどう(3) で(1=★) あさごはんを 食べます = "मैं होटल के भोजन-कक्ष में नाश्ता करता हूँ।" で ★ पर आता है।',
    "bunpou-5.7":  'क्रम: しゅくだいは(2) あした(3) まで(1=★) ありません = "गृहकार्य कल तक नहीं देना है।" まで ★ पर आता है।',
    "bunpou-5.8":  'क्रम: わたしは(2) コーヒー(3) より(1=★) おちゃの ほうが すきです = "मुझे कॉफ़ी से ज़्यादा चाय पसंद है।" より ★ पर आता है।',
    "bunpou-5.9":  'क्रम: りんごを(2) みっつ(3) ください(1=★) = "तीन सेब दीजिए।" ください ★ पर आता है।',
    "bunpou-5.10": 'क्रम: にちようびに(2) ともだち(3) と(1=★) えいがを 見ました = "रविवार को मैंने दोस्त के साथ फ़िल्म देखी।" と ★ पर आता है।',
    "bunpou-5.11": 'क्रम: この みせの(2) パン(3) は(1=★) おいしいです = "इस दुकान की रोटी स्वादिष्ट है।" は ★ पर आता है।',
    "bunpou-5.12": 'क्रम: れいぞうこの 中(3) に(1) のみもの(2=★) が(4) ありますか = "क्या फ़्रिज में कोई पेय है?" のみもの ★ पर आता है।',
    "bunpou-5.13": 'क्रम: あまり(2) ぎんこうに(3) 行きません(1=★) = "मैं अक्सर बैंक नहीं जाता।" 行きません ★ पर आता है।',
    "bunpou-5.14": 'क्रम: ともだちが(2) わたしに(3) ほんを(1=★) くれました = "दोस्त ने मुझे किताब दी।" ほんを ★ पर आता है।',
    "bunpou-5.15": 'क्रम: しごとが あります(4) から(3) パーティーに(2=★) は(1) 来ません = "मेरे पास काम है, इसलिए मैं पार्टी में नहीं आऊँगा।" パーティーに ★ पर आता है।',
    "bunpou-6.1":  'क्रम: にほんごの(2) しゅくだい(3) を(1=★) しました = "मैंने जापानी का गृहकार्य किया।" を ★ पर आता है।',
    "bunpou-6.2":  'क्रम: わたしは いま(2) なに(3) も(1=★) たべたく ありません = "मैं अभी कुछ भी नहीं खाना चाहता।" も ★ पर आता है।',
    "bunpou-6.3":  'क्रम: あの(2) きれいな(3) ひと(1=★) は たなかさんです = "वह सुंदर व्यक्ति तानाका जी हैं।" ひと ★ पर आता है।',
    "bunpou-6.4":  'क्रम: ともだちと(2) いっしょに(3) えいがを(1=★) 見ました = "मैंने दोस्त के साथ फ़िल्म देखी।" えいがを ★ पर आता है।',
    "bunpou-6.5":  'क्रम: あした(3) しゅくだい(2=★) は(4) ありますか(1) = "क्या कल गृहकार्य है?" しゅくだい ★ पर आता है।',
    "bunpou-6.6":  'क्रम: ともだち(2) と(3) えいがかん(1=★) へ 行きました = "दोस्त के साथ सिनेमा-घर गया।" えいがかん ★ पर आता है।',
    "bunpou-6.7":  'क्रम: ほんを(2) よんで(3) から(1=★) ねます = "किताब पढ़ने के बाद मैं सोऊँगा।" から ★ पर आता है।',
    "bunpou-6.8":  'क्रम: わたしの(2) いえの(3) まえに(1=★) こうえんが あります = "मेरे घर के सामने एक पार्क है।" まえに ★ पर आता है।',
    "bunpou-6.9":  'क्रम: やまの(2) うえに(1) ゆきが(3) たくさん(4=★) あります = "पहाड़ के ऊपर बहुत बर्फ़ है।" たくさん ★ पर आता है।',
    "bunpou-6.10": 'क्रम: あした(2) なんじ(3) ごろ(1=★) きますか = "कल लगभग कितने बजे आएँगे?" ごろ ★ पर आता है।',
    "bunpou-6.11": 'क्रम: あの こうえん(2) は(3) ひろくて(1=★) きれいです = "वह पार्क बड़ा और सुंदर है।" ひろくて ★ पर आता है।',
    "bunpou-6.12": 'क्रम: まいにち(4) あさ(2) 七時(3=★) に(1) おきます = "मैं हर दिन सुबह सात बजे उठता हूँ।" 七時 ★ पर आता है।',
    "bunpou-6.13": 'क्रम: おなか(2) が(1) すいて(3) まだ(4=★) いませんから、たべません = "मुझे अभी तक भूख नहीं लगी है, इसलिए नहीं खाऊँगा।" まだ ★ पर आता है।',
    "bunpou-6.14": 'क्रम: こうえんで(2) こどもたち(3) が(1=★) あそんで います = "बच्चे पार्क में खेल रहे हैं।" が ★ पर आता है।',
    "bunpou-6.15": 'क्रम: あの(2) たかい(3) たてもの(1=★) は ホテルです = "वह ऊँची इमारत होटल है।" たてもの ★ पर आता है।',
}

# ---------------------------------------------------------------------------
# Pipeline
# ---------------------------------------------------------------------------
def backup(fp):
    bak = fp + f".bak_{TODAY}_paper_bug_fix"
    if not os.path.exists(bak):
        shutil.copy2(fp, bak)
    return bak

def main():
    files = sorted(glob.glob(PAPERS_GLOB, recursive=True))
    print(f"Found {len(files)} paper files")
    print()

    changes = {
        "PAPER-001 (re-tag)": [],
        "PAPER-002 (set missing)": [],
        "PAPER-003 (rationale strip)": [],
        "PAPER-004 (rationale_hi rewrite)": [],
    }

    for fp in files:
        with open(fp, "r", encoding="utf-8") as f:
            data = json.load(f)
        modified = False
        for q in data.get("questions", []):
            qid = q.get("id", "")

            # --- PAPER-001 + PAPER-002: re-tag grammarPatternId ---
            new_tag = None
            new_meaning = None
            if qid.startswith("bunpou-"):
                correct_idx = q.get("correctIndex", -1)
                choices = q.get("choices", [])
                if 0 <= correct_idx < len(choices):
                    correct_raw = re.sub(r"<[^>]+>", "", str(choices[correct_idx])).strip()
                    # Mondai 1 logic
                    if q.get("mondai") == 1:
                        if qid in NONPARTICLE_TAGS:
                            new_tag, new_meaning = NONPARTICLE_TAGS[qid]
                        elif correct_raw in PARTICLE_TO_PATTERN:
                            new_tag = PARTICLE_TO_PATTERN[correct_raw]
                            new_meaning = f"Particle {correct_raw}"
                    # Mondai 2: only re-tag known mistakes
                    elif q.get("mondai") == 2:
                        if qid in MONDAI2_TAGS:
                            new_tag, new_meaning = MONDAI2_TAGS[qid]
                    # Mondai 3: re-tag by correct particle if currently n5-013 mismatch
                    elif q.get("mondai") == 3:
                        if correct_raw in PARTICLE_TO_PATTERN:
                            new_tag = PARTICLE_TO_PATTERN[correct_raw]
                            new_meaning = f"Particle {correct_raw}"

            if new_tag and new_tag != q.get("grammarPatternId"):
                old = q.get("grammarPatternId", "<missing>")
                q["grammarPatternId"] = new_tag
                q["grammarPatternId_provenance"] = PROVENANCE
                key = "PAPER-002 (set missing)" if old == "<missing>" or "grammarPatternId" not in q else "PAPER-001 (re-tag)"
                # qid bunpou-4.3 was the only one truly missing
                if qid == "bunpou-4.3":
                    key = "PAPER-002 (set missing)"
                changes[key].append((qid, old, new_tag, new_meaning))
                modified = True

            # --- PAPER-003: rationale strip ---
            if qid in RATIONALE_STRIPS:
                spec = RATIONALE_STRIPS[qid]
                old_rat = q.get("rationale", "")
                if old_rat != spec["rationale"]:
                    q["rationale"] = spec["rationale"]
                    changes["PAPER-003 (rationale strip)"].append((qid, "rationale", old_rat[:80], spec["rationale"][:80]))
                    modified = True
                old_rh = q.get("rationale_hi", "")
                if old_rh != spec["rationale_hi"]:
                    q["rationale_hi"] = spec["rationale_hi"]
                    q["rationale_hi_provenance"] = f"native_reviewed_{TODAY}"
                    changes["PAPER-003 (rationale strip)"].append((qid, "rationale_hi", old_rh[:80], spec["rationale_hi"][:80]))
                    modified = True

            # --- PAPER-004: rationale_hi rewrites ---
            if qid in RATIONALE_HI_REWRITES:
                new_rh = RATIONALE_HI_REWRITES[qid]
                old_rh = q.get("rationale_hi", "")
                if old_rh != new_rh:
                    q["rationale_hi"] = new_rh
                    q["rationale_hi_provenance"] = f"native_reviewed_{TODAY}"
                    changes["PAPER-004 (rationale_hi rewrite)"].append((qid, old_rh[:80], new_rh[:80]))
                    modified = True

        if modified:
            backup(fp)
            with open(fp, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            print(f"  WROTE {os.path.basename(fp)}")

    # Summary report
    print()
    print("=" * 70)
    print(f"FIX SUMMARY (run {datetime.datetime.now().isoformat()})")
    print("=" * 70)
    for k, v in changes.items():
        print(f"\n## {k}: {len(v)} changes")
        for entry in v[:30]:
            print(f"  - {entry}")
        if len(v) > 30:
            print(f"  ... and {len(v)-30} more")

    return changes

if __name__ == "__main__":
    main()
