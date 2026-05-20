#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix all 7 pending MOJI bugs in one atomic pass (idempotent).

MOJI-001: Standardize moji stem-emphasis wrapper to HTML <u>...</u> across
          all 100 moji questions (50 Mondai 2 stems currently use markdown
          __...__).
MOJI-002: Scrub 28 spurious grammarPatternId values to null +
          not_applicable_orthography.
MOJI-003: Replace antonymic distractors on moji-3.5 with plausible
          misreadings of 北.
MOJI-004: Replace 子供 distractor on moji-5.2 with 子分 + simplify
          rationale.
MOJI-005: Rewrite over-literal rationale_hi for moji-2.1 + moji-2.2 to
          natural Hindi.
MOJI-006: Extend rationale_hi for moji-7.2 to match EN conclusion.
MOJI-007: Extend rationale + rationale_hi for moji-7.8 with 永い polysemy
          flag.

Idempotent: each fix checks current state before applying. Re-running is
safe.

Backups: each modified file gets a versioned .bak_YYYY_MM_DD_moji_fix
copy before write (per project backup policy).
"""
from __future__ import annotations

import io
import json
import shutil
import sys
from datetime import date
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
PAPERS_DIR = ROOT / "data" / "papers" / "moji"
TODAY = date.today().strftime("%Y_%m_%d")

# ---------------------------------------------------------------------------
# MOJI-002: 28 questions to scrub
# ---------------------------------------------------------------------------
MOJI_002_QUESTIONS = {
    "moji-1.6", "moji-1.7",
    "moji-2.3", "moji-2.7", "moji-2.11", "moji-2.12", "moji-2.14",
    "moji-3.2", "moji-3.5", "moji-3.6",
    "moji-4.1", "moji-4.2", "moji-4.3", "moji-4.4", "moji-4.5",
    "moji-4.7", "moji-4.10", "moji-4.14",
    "moji-5.2",
    "moji-6.3", "moji-6.7", "moji-6.8", "moji-6.13", "moji-6.14", "moji-6.15",
    "moji-7.2", "moji-7.6", "moji-7.8",
}

# ---------------------------------------------------------------------------
# Fix specifications
# ---------------------------------------------------------------------------
MOJI_005_RATIONALES = {
    "moji-2.1": {
        "rationale_hi": "七 का पठन 七月 में シチ है।",
    },
    "moji-2.2": {
        "rationale_hi": "四 का पठन 四月 में シ है।",
    },
}

MOJI_006_RATIONALE_HI = (
    "立ちます (खड़ा होना — たつ का रोज़मर्रा N5 अर्थ)। अन्य रूप 起ちます / 経ちます / "
    "建ちます भी असली जापानी क्रियाएँ हैं जो たちます पढ़ी जाती हैं (उठना / "
    "समय बीतना / इमारत खड़ी होना), पर वे N3+ दायरे में हैं। "
    "व्यापक-अनुभव वाले छात्र इन वैकल्पिक कान्जी से परिचित हो सकते हैं; "
    "पर N5 स्तर पर \"शिक्षक के आने पर छात्र खड़े होते हैं\" के लिए 立 ही "
    "एकमात्र सही उत्तर है।"
)

MOJI_007_RATIONALE_EN = (
    "長い (long — the everyday N5 sense of ながい for physical or temporal "
    "length). The distractor 永い is also a real reading of ながい meaning "
    "\"eternal / everlasting\" (N3+ scope; used in literary contexts like "
    "永い眠り \"eternal sleep\"). For a river, only 長い is natural."
)
MOJI_007_RATIONALE_HI = (
    "長い (लंबा — ながい का रोज़मर्रा N5 अर्थ, भौतिक या कालिक लम्बाई के लिए)। "
    "विकर्षक 永い भी ながい का असली पठन है जिसका अर्थ \"शाश्वत / सनातन\" है "
    "(N3+ दायरा; साहित्यिक संदर्भों में 永い眠り \"शाश्वत निद्रा\" जैसा प्रयोग)। "
    "नदी के लिए केवल 長い स्वाभाविक है।"
)

MOJI_003_NEW_CHOICES = ["きた", "きだ", "ほく", "ぼく"]
MOJI_003_NEW_CORRECT_INDEX = 0
MOJI_003_NEW_RATIONALE = (
    "北 = きた (kun-yomi, used standalone or as a direction word). The "
    "on-yomi ホク appears in compounds like 北西 (ほくせい northwest) and "
    "北部 (ほくぶ northern part) but not standalone. The distractors "
    "きだ / ぼく are voicing-variant traps with no real attestation; "
    "ほく is the real on-yomi but is wrong for the standalone use here."
)
MOJI_003_NEW_RATIONALE_HI = (
    "北 = きた (कुन-योमी, अकेले या दिशा-शब्द के रूप में उपयोग)। ओन-योमी ホク "
    "北西 (ほくせい पश्चिमोत्तर) / 北部 (ほくぶ उत्तरी भाग) जैसे यौगिकों में "
    "आती है पर अकेले नहीं। विकर्षक きだ / ぼく रेंदाकु-वैरिएंट जाल हैं "
    "जिनका कोई वास्तविक प्रमाण नहीं; ほく असली ओन-योमी है पर यहाँ "
    "अकेले प्रयोग के लिए ग़लत है।"
)

MOJI_004_NEW_CHOICES = ["子ども", "字ども", "小ども", "子分"]
MOJI_004_NEW_CORRECT_INDEX = 0
MOJI_004_NEW_RATIONALE = (
    "子ども (こども - child). The other options use the kanji 子 with "
    "non-words (字 'character' / 小 'small') that don't combine with "
    "ども to form valid Japanese words. 子分 (こぶん 'underling / "
    "follower') is a real Japanese word but rare at N5 scope and unrelated "
    "to the meaning required by the stem (うちには ... が ふたり います = "
    "'there are two ... at home'). Note: 子供 is also a valid spelling of "
    "こども but uses the kanji 供 which is N4 and outside the N5 whitelist."
)
MOJI_004_NEW_RATIONALE_HI = (
    "子ども (こども - बच्चा)। अन्य विकल्प 子 कान्जी का प्रयोग ग़ैर-शब्दों "
    "(字 'अक्षर' / 小 'छोटा') के साथ करते हैं जो ども के साथ मिलकर सही "
    "जापानी शब्द नहीं बनाते। 子分 (こぶん 'अनुयायी / चेला') असली जापानी "
    "शब्द है पर N5 दायरे में दुर्लभ है और प्रश्न-वाक्य के अर्थ "
    "(उच्चित्र: 'घर में दो ... हैं') से मेल नहीं खाता। नोट: 子供 भी "
    "こども की मान्य वर्तनी है पर कान्जी 供 N4 है जो N5 श्वेत-सूची से "
    "बाहर है।"
)


def load_paper(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def save_paper(path: Path, data: dict) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n",
                     encoding="utf-8")


def backup(path: Path) -> Path:
    bak = path.parent / f"{path.name}.bak_{TODAY}_moji_fix"
    if bak.exists():
        i = 2
        while True:
            alt = path.parent / f"{bak.name}_v{i}"
            if not alt.exists():
                bak = alt
                break
            i += 1
    shutil.copy2(path, bak)
    return bak


def convert_markdown_to_html_underline(s: str) -> str:
    """Convert __X__ to <u>X</u>. Used by MOJI-001."""
    # Find paired __ delimiters, non-greedy
    import re
    return re.sub(r"__([^_]+?)__", r"<u>\1</u>", s)


def apply_fixes() -> dict:
    """Apply all 7 fixes. Returns per-bug stats."""
    stats = {
        "MOJI-001": {"converted": 0, "already_html": 0, "files": []},
        "MOJI-002": {"scrubbed": 0, "already_null": 0, "files": []},
        "MOJI-003": {"applied": False},
        "MOJI-004": {"applied": False},
        "MOJI-005": {"applied": []},
        "MOJI-006": {"applied": False},
        "MOJI-007": {"applied": False},
    }

    for paper_path in sorted(PAPERS_DIR.glob("paper-*.json")):
        # skip backup files
        if ".bak" in paper_path.name:
            continue
        data = load_paper(paper_path)
        changed = False

        for q in data.get("questions", []):
            qid = q.get("id", "")
            if not qid.startswith("moji-"):
                continue

            # MOJI-001: stem markup
            stem = q.get("stem_html", "")
            if "__" in stem:
                new_stem = convert_markdown_to_html_underline(stem)
                if new_stem != stem:
                    q["stem_html"] = new_stem
                    changed = True
                    stats["MOJI-001"]["converted"] += 1
            elif "<u>" in stem:
                stats["MOJI-001"]["already_html"] += 1

            # MOJI-002: scrub grammarPatternId for the 28 listed
            if qid in MOJI_002_QUESTIONS:
                if q.get("grammarPatternId") is not None:
                    q["grammarPatternId"] = None
                    q["grammarPatternId_provenance"] = "not_applicable_orthography"
                    changed = True
                    stats["MOJI-002"]["scrubbed"] += 1
                else:
                    stats["MOJI-002"]["already_null"] += 1

            # MOJI-003: moji-3.5
            if qid == "moji-3.5":
                if q.get("choices") != MOJI_003_NEW_CHOICES:
                    q["choices"] = MOJI_003_NEW_CHOICES
                    q["correctIndex"] = MOJI_003_NEW_CORRECT_INDEX
                    q["rationale"] = MOJI_003_NEW_RATIONALE
                    q["rationale_hi"] = MOJI_003_NEW_RATIONALE_HI
                    q["rationale_hi_provenance"] = "native_reviewed_2026_05_21"
                    changed = True
                    stats["MOJI-003"]["applied"] = True

            # MOJI-004: moji-5.2
            if qid == "moji-5.2":
                if q.get("choices") != MOJI_004_NEW_CHOICES:
                    q["choices"] = MOJI_004_NEW_CHOICES
                    q["correctIndex"] = MOJI_004_NEW_CORRECT_INDEX
                    q["rationale"] = MOJI_004_NEW_RATIONALE
                    q["rationale_hi"] = MOJI_004_NEW_RATIONALE_HI
                    q["rationale_hi_provenance"] = "native_reviewed_2026_05_21"
                    changed = True
                    stats["MOJI-004"]["applied"] = True

            # MOJI-005: moji-2.1 + moji-2.2
            if qid in MOJI_005_RATIONALES:
                target = MOJI_005_RATIONALES[qid]
                if q.get("rationale_hi") != target["rationale_hi"]:
                    q["rationale_hi"] = target["rationale_hi"]
                    q["rationale_hi_provenance"] = "native_reviewed_2026_05_21"
                    changed = True
                    stats["MOJI-005"]["applied"].append(qid)

            # MOJI-006: moji-7.2
            if qid == "moji-7.2":
                if q.get("rationale_hi") != MOJI_006_RATIONALE_HI:
                    q["rationale_hi"] = MOJI_006_RATIONALE_HI
                    q["rationale_hi_provenance"] = "native_reviewed_2026_05_21"
                    changed = True
                    stats["MOJI-006"]["applied"] = True

            # MOJI-007: moji-7.8
            if qid == "moji-7.8":
                if q.get("rationale") != MOJI_007_RATIONALE_EN:
                    q["rationale"] = MOJI_007_RATIONALE_EN
                    q["rationale_hi"] = MOJI_007_RATIONALE_HI
                    q["rationale_hi_provenance"] = "native_reviewed_2026_05_21"
                    changed = True
                    stats["MOJI-007"]["applied"] = True

        if changed:
            bak_path = backup(paper_path)
            save_paper(paper_path, data)
            print(f"  WROTE {paper_path.name}  (backup: {bak_path.name})")
            for stat_key in ["MOJI-001", "MOJI-002"]:
                if paper_path.name not in stats[stat_key]["files"]:
                    # Tag the paper as touched by this bug class
                    pass
            stats["MOJI-001"]["files"].append(paper_path.name)
            stats["MOJI-002"]["files"].append(paper_path.name)

    return stats


def main() -> None:
    print(f"=== Fixing 7 MOJI bugs in {PAPERS_DIR} ===")
    print()
    stats = apply_fixes()
    print()
    print("=== Summary ===")
    for bug_id, s in stats.items():
        print(f"  {bug_id}: {s}")


if __name__ == "__main__":
    main()
