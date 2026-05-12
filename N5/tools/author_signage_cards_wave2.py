"""
ISSUE-122 wave 2 — push kanji authentic_refs from 43/106 toward 65+/106.

Wave 1 hit 18 -> 43. Wave 2 targets the remaining easy wins:
  - Numeric kanji (一-十, 百, 千, 万) via price tags + serving counts
  - Calendar month names (一月..十二月)
  - Day-of-week markers (火曜日, 木曜日, 金曜日, 土曜日; 月/水/日 already done)
  - Time units (年, 分, 半)
  - People kanji on signage (子, 生, 先, 父, 母, 友)
  - Misc (国, 私, 立, 何)

Each card uses ONLY N5 kanji so JA-16 stays green. The bidirectional
update on kanji.json adds card IDs to the relevant entries'
authentic_refs arrays.
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

# Card schema: (id, category, ja, reading, gloss_en, gloss_hi, context, kanji_refs)
NEW_CARDS = [
    # === Price tags / quantity ===
    (
        "auth.menu.hyaku-en",
        "menu",
        "百円",
        "ひゃくえん",
        "100 yen",
        "100 येन",
        "Price-tag denomination seen on 100-yen-shop banners and bargain-bin labels (the ubiquitous 百均 / 100-yen store culture).",
        ["n5.kanji.百"],
    ),
    (
        "auth.menu.sen-en",
        "menu",
        "千円",
        "せんえん",
        "1000 yen",
        "1000 येन",
        "Price tag at the next-up denomination. Common on bento-box prices and small-purchase ATM withdrawal prompts (千円札 = 1000-yen note).",
        ["n5.kanji.千"],
    ),
    (
        "auth.menu.ichiman-en",
        "menu",
        "一万円",
        "いちまんえん",
        "10,000 yen",
        "10,000 येन",
        "Major-purchase denomination — the largest single Japanese banknote. Seen on cash-deposit ATM screens and high-tier menu/sake-bottle prices.",
        ["n5.kanji.一", "n5.kanji.万"],
    ),
    (
        "auth.menu.ichi-ninmae",
        "menu",
        "一人前",
        "いちにんまえ",
        "One serving",
        "एक हिस्सा",
        "Menu-board quantity label — '1 portion for 1 person'. Often paired with prices (一人前 1,200円) for set meals.",
        ["n5.kanji.一"],
    ),
    (
        "auth.menu.san-ninmae",
        "menu",
        "三人前",
        "さんにんまえ",
        "Three servings",
        "तीन हिस्से",
        "Family-size or shareable-portion label — common on takeout-bento promotional banners (三人前 2,800円).",
        ["n5.kanji.三"],
    ),
    # === Months ===
    (
        "auth.signs.ichi-getsu",
        "time",
        "一月",
        "いちがつ",
        "January",
        "जनवरी",
        "Month header on calendars, magazine covers, and seasonal-promotion signs. Read with on-yomi いち + がつ. Note: 1月 (Arabic numeral) is equally common.",
        ["n5.kanji.一", "n5.kanji.月"],
    ),
    (
        "auth.signs.shi-getsu",
        "time",
        "四月",
        "しがつ",
        "April",
        "अप्रैल",
        "April marks the start of the Japanese fiscal/school year — 4月 banners on new-employee welcome signs, school-entrance ceremonies, cherry-blossom-season menus.",
        ["n5.kanji.四", "n5.kanji.月"],
    ),
    (
        "auth.signs.go-getsu",
        "time",
        "五月",
        "ごがつ",
        "May",
        "मई",
        "May features Golden Week 5月の連休 — multiple national holidays. Travel-promotion signs and koinobori (carp-streamer) displays carry this date prominently.",
        ["n5.kanji.五", "n5.kanji.月"],
    ),
    (
        "auth.signs.roku-getsu",
        "time",
        "六月",
        "ろくがつ",
        "June",
        "जून",
        "Rainy-season starts in June — 6月の梅雨 forecasts on weather-board displays. Also seen on rainy-season umbrella-shop promotional banners.",
        ["n5.kanji.六", "n5.kanji.月"],
    ),
    (
        "auth.signs.shichi-getsu",
        "time",
        "七月",
        "しちがつ",
        "July",
        "जुलाई",
        "Summer-festival 七夕 (Tanabata) on July 7 is heavily signed — 7月7日 wishes on bamboo decorations in shops and stations.",
        ["n5.kanji.七", "n5.kanji.月"],
    ),
    (
        "auth.signs.hachi-getsu",
        "time",
        "八月",
        "はちがつ",
        "August",
        "अगस्त",
        "August = obon-festival month (お盆) — train-station signs announce holiday-period schedules; 8月のお盆 fireworks-festival banners.",
        ["n5.kanji.八", "n5.kanji.月"],
    ),
    (
        "auth.signs.kyuu-getsu",
        "time",
        "九月",
        "くがつ",
        "September",
        "सितंबर",
        "September starts autumn — autumn-foods menu rotations and 9月の秋祭り (autumn-festival) banners replace summer signage.",
        ["n5.kanji.九", "n5.kanji.月"],
    ),
    (
        "auth.signs.juu-getsu",
        "time",
        "十月",
        "じゅうがつ",
        "October",
        "अक्टूबर",
        "Read じゅうがつ (irregular contraction of じゅう + がつ → not じゅうげつ). October hosts Sports Day 体育の日 and harvest-festival signs.",
        ["n5.kanji.十", "n5.kanji.月"],
    ),
    # === Days of week ===
    (
        "auth.signs.kayoubi",
        "time",
        "火曜日",
        "かようび",
        "Tuesday",
        "मंगलवार",
        "Day-of-week schedule label on shop signs (火曜日定休 = closed Tuesdays) and clinic-hours boards. Read with on-yomi か (fire) + よう + び.",
        ["n5.kanji.火", "n5.kanji.曜"],
    ),
    (
        "auth.signs.mokuyoubi",
        "time",
        "木曜日",
        "もくようび",
        "Thursday",
        "गुरुवार",
        "Tree-themed day label. Common on rotating-special menus (木曜日のおすすめ = Thursday's recommendation) and weekly farmer's-market schedules.",
        ["n5.kanji.木", "n5.kanji.曜"],
    ),
    (
        "auth.signs.kinyoubi",
        "time",
        "金曜日",
        "きんようび",
        "Friday",
        "शुक्रवार",
        "End-of-workweek day — 金曜日のハッピーアワー (Friday happy hour) on izakaya promotional signs; also payday-related (金 = money).",
        ["n5.kanji.金", "n5.kanji.曜"],
    ),
    (
        "auth.signs.doyoubi",
        "time",
        "土曜日",
        "どようび",
        "Saturday",
        "शनिवार",
        "Weekend day label on store-hours signs (土曜日10:00-20:00) and family-event banners. Most retail and dining establishments operate full hours on Saturdays.",
        ["n5.kanji.土", "n5.kanji.曜"],
    ),
    # === Time units ===
    (
        "auth.signs.kotoshi",
        "time",
        "今年",
        "ことし",
        "This year",
        "इस वर्ष",
        "Seasonal promotional banner prefix — 今年もよろしくお願いします (this year too, please favor us). Common on New Year's shopfront greetings.",
        ["n5.kanji.今", "n5.kanji.年"],
    ),
    (
        "auth.signs.juppun",
        "time",
        "10分",
        "じゅっぷん",
        "10 minutes",
        "10 मिनट",
        "Quick-service signage (10分でカット = 10-minute haircut) and short-wait time indicators on station departure boards.",
        ["n5.kanji.分"],
    ),
    (
        "auth.shop.hachi-ji-han",
        "time",
        "8時半",
        "はちじはん",
        "8:30",
        "8:30",
        "Casual time-of-day label on shop signs — 8時半から (from 8:30) is common on morning-hours boards. The kanji 半 = half, paired with 時 to mean 'half-hour past'.",
        ["n5.kanji.半"],
    ),
    # === People kanji ===
    (
        "auth.signs.kodomo",
        "shop",
        "子ども",
        "こども",
        "Children",
        "बच्चे",
        "Kids' section / children's products label. The hiragana ども-form is preferred over kanji 子供 on consumer-facing signage to soften the tone for parents.",
        ["n5.kanji.子"],
    ),
    (
        "auth.signs.gakusei",
        "notice",
        "学生",
        "がくせい",
        "Student",
        "विद्यार्थी",
        "Student-discount sign at museums and theaters (学生 800円 = student 800 yen); also used on student-ID labels (学生証).",
        ["n5.kanji.学", "n5.kanji.生"],
    ),
    (
        "auth.signs.sensei",
        "notice",
        "先生",
        "せんせい",
        "Teacher / doctor (honorific)",
        "अध्यापक / डॉक्टर",
        "Faculty-office nameplate on school doors (○○先生); also addresses doctors at clinics (山田先生). The 先生 honorific is used for any expert-recognition role.",
        ["n5.kanji.先", "n5.kanji.生"],
    ),
    (
        "auth.signs.tomodachi",
        "shop",
        "友だち",
        "ともだち",
        "Friend",
        "मित्र",
        "Friendship-themed retail signage — 友だち と一緒に (with friends) on group-discount banners at restaurants and entertainment venues.",
        ["n5.kanji.友"],
    ),
    (
        "auth.signs.chichi-no-hi",
        "shop",
        "父の日",
        "ちちのひ",
        "Father's Day",
        "पिता दिवस",
        "Department-store seasonal promotion banner (third Sunday of June). 父の日プレゼント = Father's Day gift display tables.",
        ["n5.kanji.父"],
    ),
    (
        "auth.signs.haha-no-hi",
        "shop",
        "母の日",
        "ははのひ",
        "Mother's Day",
        "मातृ दिवस",
        "Department-store seasonal promotion banner (second Sunday of May). 母の日に贈る花 = flowers to give on Mother's Day, common florist signage.",
        ["n5.kanji.母"],
    ),
    # === Country / formal ===
    (
        "auth.signs.chuugoku",
        "shop",
        "中国",
        "ちゅうごく",
        "China",
        "चीन",
        "中国 = China — common prefix on restaurant signs 中国料理 (Chinese cuisine) and tourism-info boards. Reads ちゅうごく; 中 is also Japan's western Chuugoku region.",
        ["n5.kanji.国"],
    ),
    (
        "auth.signs.shiritsu-gakkou",
        "notice",
        "私立学校",
        "しりつがっこう",
        "Private school",
        "निजी विद्यालय",
        "School-classification label — 私立 (private) vs 公立 (public, N4). The 私 (I / private) appears on school-gate plaques and admission-document headers.",
        ["n5.kanji.私", "n5.kanji.立"],
    ),
    (
        "auth.signs.nanji-kara",
        "shop",
        "何時から",
        "なんじから",
        "From what time",
        "किस समय से",
        "Customer-facing question form on shop-hours notices (何時から何時まで = from what time until what time). Also common in casual conversation.",
        ["n5.kanji.何"],
    ),
]


def main() -> int:
    auth = json.loads(AUTHENTIC.read_text(encoding="utf-8"))
    kanji = json.loads(KANJI.read_text(encoding="utf-8"))

    items = auth["items"]
    existing_ids = {c["id"] for c in items}

    added = 0
    skipped = 0
    for entry in NEW_CARDS:
        cid, cat, ja, reading, en, hi, ctx, krefs = entry
        if cid in existing_ids:
            skipped += 1
            continue
        items.append({
            "id": cid,
            "category": cat,
            "ja": ja,
            "reading": reading,
            "gloss_en": en,
            "gloss_hi": hi,
            "context": ctx,
            "review_status": "llm_curated",
            "kanji_refs": krefs,
            "kanji_refs_provenance": "llm_curated",
            "audit_wave": "issue-122-wave2-2026-05-12",
        })
        added += 1

    AUTHENTIC.write_text(json.dumps(auth, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Appended {added} cards (skipped {skipped} dups)")

    # Update kanji-side authentic_refs (bidirectional)
    KE = kanji.get("entries", kanji)
    if isinstance(KE, dict):
        KE = list(KE.values())
    kanji_index = {k["id"]: k for k in KE if "id" in k}

    new_refs_added = 0
    for entry in NEW_CARDS:
        cid = entry[0]
        for kid in entry[7]:
            kk = kanji_index.get(kid)
            if not kk:
                print(f"  WARNING: kanji {kid} not in kanji.json")
                continue
            refs = kk.get("authentic_refs") or []
            if cid not in refs:
                refs.append(cid)
                kk["authentic_refs"] = sorted(refs)
                new_refs_added += 1

    total_covered = sum(1 for k in KE if k.get("authentic_refs"))
    KANJI.write_text(json.dumps(kanji, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Added {new_refs_added} new bidirectional refs")
    print(f"Total kanji with authentic_refs: {total_covered}/{len(KE)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
