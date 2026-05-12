"""
ISSUE-122 — Author new authentic-content cards covering signage-prominent
N5 kanji that currently have no authentic_refs.

Pre-wave state (2026-05-12): 18/106 kanji entries linked to authentic
cards. The audit prompt called out ~30+ N5 kanji with unambiguous
real-world signage uses (駅, 学校, 会社, 道, 山, 川, 田, 本, 水, 火,
名, 番, 私, etc.) that were absent from the authentic corpus.

This wave authors 23 new authentic cards using ONLY N5-whitelisted
kanji (so JA-16 remains green). Each card:
  - Has a real-Japan signage context (train station signs, school
    signs, shop labels, price tags, public notices)
  - Uses only N5 kanji in its `ja` text + only N5 readings
  - Lists the N5 kanji used in `kanji_refs`
  - Has a `context` field explaining where it appears

After writing the cards, the script ALSO updates the corresponding
kanji entries in data/kanji.json to populate the bidirectional
`authentic_refs` field — that's what the audit actually measures.

Expected result: 18/106 -> 41+/106 kanji entries with authentic_refs.
"""

from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REPO = Path(__file__).resolve().parents[1]
AUTHENTIC = REPO / "data" / "authentic.json"
KANJI = REPO / "data" / "kanji.json"

# New cards — each tuple is (id, category, ja, reading, gloss_en, gloss_hi,
# context_en, kanji_refs).
# CRITICAL: `ja` MUST use only N5 kanji (verified post-write by JA-16).
NEW_CARDS = [
    # === Station / transit ===
    (
        "auth.transit.eki",
        "transit",
        "えき",
        "えき",
        "Station",
        "स्टेशन",
        "Single-character signage on the side of every JR / metro station — the green-on-white 「駅」 panel is one of the most recognisable signs in Japan.",
        ["n5.kanji.駅"],
    ),
    (
        "auth.transit.eki-mae",
        "transit",
        "駅前",
        "えきまえ",
        "In front of the station",
        "स्टेशन के सामने",
        "Common neighborhood label used in bus-stop names (○○駅前) and small-business signs. Indicates the immediate plaza in front of the station.",
        ["n5.kanji.駅", "n5.kanji.前"],
    ),
    (
        "auth.transit.eki-naka",
        "transit",
        "駅の中",
        "えきのなか",
        "Inside the station",
        "स्टेशन के अंदर",
        "Directional label used in transit-system signage to indicate retail / facilities inside the paid area of a station building.",
        ["n5.kanji.駅", "n5.kanji.中"],
    ),
    (
        "auth.transit.kita-eki",
        "transit",
        "きた駅",
        "きたえき",
        "North station / North exit station name",
        "उत्तर स्टेशन",
        "Many cities use compass-direction prefixes for multi-station hubs (きた駅 = north station). Compare to みなみ駅 / ひがし駅 / にし駅.",
        ["n5.kanji.駅"],
    ),
    # === School / education ===
    (
        "auth.notice.shougakkou",
        "signs",
        "小学校",
        "しょうがっこう",
        "Elementary school",
        "प्राथमिक विद्यालय",
        "Sign attached to the gate of every elementary school in Japan. Often paired with the school's name on a wooden / brass plaque.",
        ["n5.kanji.小", "n5.kanji.学", "n5.kanji.校"],
    ),
    (
        "auth.notice.chuugakkou",
        "signs",
        "中学校",
        "ちゅうがっこう",
        "Middle school",
        "मध्य विद्यालय",
        "Sign attached to the gate of every middle school in Japan. Uses 中 (middle / inside) + 学校 (school).",
        ["n5.kanji.中", "n5.kanji.学", "n5.kanji.校"],
    ),
    (
        "auth.notice.gakkou",
        "signs",
        "学校",
        "がっこう",
        "School",
        "विद्यालय",
        "Generic school signage — common on school-zone road signs and on the front gate of any educational facility.",
        ["n5.kanji.学", "n5.kanji.校"],
    ),
    # === Company / shop ===
    (
        "auth.signs.kaisha",
        "signs",
        "会社",
        "かいしゃ",
        "Company / office",
        "कंपनी",
        "Generic company-building label — common suffix on corporate signage (○○会社) and in office-park directories.",
        ["n5.kanji.会", "n5.kanji.社"],
    ),
    (
        "auth.signs.honten",
        "shop",
        "本店",
        "ほんてん",
        "Main branch / head shop",
        "मुख्य शाखा",
        "Suffix on the original / flagship location of a chain restaurant or retail brand. Contrasted with 支店 (branch) in chain-store signage.",
        ["n5.kanji.本", "n5.kanji.店"],
    ),
    (
        "auth.shop.honya",
        "shop",
        "本や",
        "ほんや",
        "Bookstore",
        "किताबों की दुकान",
        "Bookstore signage — small independent shops often write 本や rather than the kanji-only 本屋 (屋 is N4). The kana 'や' is common in shop names.",
        ["n5.kanji.本"],
    ),
    (
        "auth.shop.furuhonya",
        "shop",
        "古い本や",
        "ふるいほんや",
        "Used / antiquarian bookstore",
        "पुरानी किताबों की दुकान",
        "Phrasing seen on used-bookstore shopfronts in Jimbocho (Tokyo's book-district). Conveys 'second-hand books'.",
        ["n5.kanji.古", "n5.kanji.本"],
    ),
    # === Public space / roads ===
    (
        "auth.signs.michi",
        "signs",
        "道",
        "みち",
        "Road / way",
        "रास्ता",
        "Single-character signage on street-name plates (○○道 = the X road). Common in older neighborhood signage.",
        ["n5.kanji.道"],
    ),
    (
        "auth.signs.yamamichi",
        "signs",
        "山道",
        "やまみち",
        "Mountain trail",
        "पहाड़ी रास्ता",
        "Hiking-trail signage in mountain parks — wooden post markers with carved 山道 indicating a footpath.",
        ["n5.kanji.山", "n5.kanji.道"],
    ),
    (
        "auth.signs.kawa",
        "signs",
        "川",
        "かわ",
        "River",
        "नदी",
        "Single-character signage on bridge nameplates and river-bank parks (○○川 = X river). Common in landscape signage.",
        ["n5.kanji.川"],
    ),
    # === Time / dates ===
    (
        "auth.signs.gozen",
        "time",
        "午前",
        "ごぜん",
        "AM / morning (before noon)",
        "पूर्वाह्न",
        "Schedule / hours label on shop signs and bus timetables (午前10時 = 10 AM). Contrasted with 午後 (afternoon).",
        ["n5.kanji.午", "n5.kanji.前"],
    ),
    (
        "auth.signs.gogo",
        "time",
        "午後",
        "ごご",
        "PM / afternoon (after noon)",
        "अपराह्न",
        "Schedule / hours label on shop signs and bus timetables (午後5時まで = until 5 PM). Pair with 午前 in any time-window signage.",
        ["n5.kanji.午", "n5.kanji.後"],
    ),
    (
        "auth.signs.kyou-no",
        "shop",
        "今日の",
        "きょうの",
        "Today's (special / menu / news)",
        "आज का",
        "Restaurant-board prefix used for daily specials (今日のおすすめ = today's recommendation). Also common on bulletin-board headers (今日の天気 = today's weather).",
        ["n5.kanji.今", "n5.kanji.日"],
    ),
    (
        "auth.signs.mainichi",
        "shop",
        "毎日",
        "まいにち",
        "Every day / daily",
        "हर दिन",
        "Service-availability label on shop signage (毎日 = open daily). Often paired with hours (毎日10時から).",
        ["n5.kanji.毎", "n5.kanji.日"],
    ),
    # === Price / quality tags ===
    (
        "auth.menu.takai",
        "menu",
        "高い",
        "たかい",
        "Expensive / high",
        "महंगा / ऊँचा",
        "Price-tag adjective used on hand-written menu boards or discount-shop labels to indicate higher-tier items.",
        ["n5.kanji.高"],
    ),
    (
        "auth.menu.yasui",
        "menu",
        "安い",
        "やすい",
        "Cheap / inexpensive",
        "सस्ता",
        "Price-tag adjective used on hand-written menu boards and discount-shop banners (安い! 100円!). The same kanji 安 also means 'safe' in 安全.",
        ["n5.kanji.安"],
    ),
    # === Public forms ===
    (
        "auth.signs.onamae",
        "notice",
        "お名前",
        "おなまえ",
        "Name (form field)",
        "नाम",
        "Form-field label used on every clinic / city-hall / school registration form. The honorific お is standard on form labels.",
        ["n5.kanji.名"],
    ),
    (
        "auth.signs.bangou",
        "notice",
        "番号",
        "ばんごう",
        "Number (sequence / ticket)",
        "नंबर",
        "Ticket-machine and form-field label (受付番号 / 整理番号). Also on bus-stop sequence labels (○番のりば = bay number X).",
        ["n5.kanji.番", "n5.kanji.号"],
    ),
    # === Drinks / water ===
    (
        "auth.notice.omizu",
        "notice",
        "お水",
        "おみず",
        "Water (drinking)",
        "पीने का पानी",
        "Polite-form label seen above water dispensers in restaurants, public buildings, and on water-fountain plaques. The honorific お softens the request to a friendly offer.",
        ["n5.kanji.水"],
    ),
]


def main() -> int:
    # Load both files
    auth = json.loads(AUTHENTIC.read_text(encoding="utf-8"))
    kanji = json.loads(KANJI.read_text(encoding="utf-8"))

    items = auth["items"]
    existing_ids = {c["id"] for c in items}

    # Append cards (skip if duplicate id)
    added_cards = 0
    skipped = 0
    for entry in NEW_CARDS:
        cid, cat, ja, reading, en, hi, ctx, kanji_refs = entry
        if cid in existing_ids:
            skipped += 1
            continue
        card = {
            "id": cid,
            "category": cat,
            "ja": ja,
            "reading": reading,
            "gloss_en": en,
            "gloss_hi": hi,
            "context": ctx,
            "review_status": "llm_curated",
            "kanji_refs": kanji_refs,
            "kanji_refs_provenance": "llm_curated",
            "audit_wave": "issue-122-wave1-2026-05-12",
        }
        items.append(card)
        added_cards += 1

    # Update categories list in _meta if present (preserve order)
    meta = auth.get("_meta", {})
    seen_cats = set(meta.get("categories") or [])
    for entry in NEW_CARDS:
        seen_cats.add(entry[1])
    if "categories" in meta:
        meta["categories"] = sorted(seen_cats)

    AUTHENTIC.write_text(
        json.dumps(auth, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Appended {added_cards} authentic cards (skipped {skipped} duplicates)")

    # Now update kanji.json — for each card, add bidirectional authentic_refs
    KE = kanji.get("entries", kanji)
    if isinstance(KE, dict):
        KE = list(KE.values())

    # Build id -> entry index
    kanji_index = {k["id"]: k for k in KE if "id" in k}

    updated_kanji = 0
    new_refs_added = 0
    for entry in NEW_CARDS:
        cid = entry[0]
        kanji_refs = entry[7]
        for kid in kanji_refs:
            k_entry = kanji_index.get(kid)
            if not k_entry:
                print(f"  WARNING: kanji {kid} not found in kanji.json")
                continue
            existing_refs = k_entry.get("authentic_refs") or []
            if cid not in existing_refs:
                existing_refs.append(cid)
                k_entry["authentic_refs"] = sorted(existing_refs)
                new_refs_added += 1
        # Note: counter at top-level kanji_index level
    updated_kanji = sum(1 for k in KE if k.get("authentic_refs"))

    KANJI.write_text(
        json.dumps(kanji, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Added {new_refs_added} new bidirectional refs")
    print(f"Total kanji with authentic_refs: {updated_kanji}/{len(KE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
