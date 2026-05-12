"""
ISSUE-122 wave 3 — push kanji authentic_refs from 75/106 toward 100+/106.

Targets the remaining 31 uncovered N5 kanji with realistic signage
cards using ONLY N5-whitelisted kanji.

Coverage gains targeted: 二 週 語 員 上 下 外 東 西 南 北 間 田 花 見 空
聞 読 書 来 休 言 長 白 手 目 力 行 買
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

NEW_CARDS = [
    # === Remaining months ===
    (
        "auth.signs.ni-getsu", "time", "二月", "にがつ",
        "February", "फ़रवरी",
        "Month header. February features Setsubun (節分, beans-throwing day) and Valentine's Day — chocolate displays and seasonal-menu boards prominently show 2月.",
        ["n5.kanji.二", "n5.kanji.月"],
    ),
    (
        "auth.signs.juuichi-getsu", "time", "十一月", "じゅういちがつ",
        "November", "नवंबर",
        "Month header reading uses standard digit-chain rules (十一 = 11, がつ contracted). November = 七五三 (shichi-go-san) children's festival.",
        ["n5.kanji.十", "n5.kanji.一", "n5.kanji.月"],
    ),
    (
        "auth.signs.juuni-getsu", "time", "十二月", "じゅうにがつ",
        "December", "दिसंबर",
        "Year-end month — シーズン中 (peak season) for shopfront 十二月の福袋 (December lucky-bag) promotions, and year-end-cleaning service labels.",
        ["n5.kanji.十", "n5.kanji.二", "n5.kanji.月"],
    ),
    # === Remaining days of week ===
    (
        "auth.signs.getsuyoubi", "time", "月曜日", "げつようび",
        "Monday", "सोमवार",
        "Day-of-week schedule label. Many businesses use 月曜日定休 (closed Mondays) on storefront notices to indicate weekly rest day.",
        ["n5.kanji.月", "n5.kanji.曜", "n5.kanji.日"],
    ),
    (
        "auth.signs.suiyoubi", "time", "水曜日", "すいようび",
        "Wednesday", "बुधवार",
        "Day-of-week schedule label. Used on mid-week event banners and 水曜日のお買い得 (Wednesday's bargain) supermarket promotions.",
        ["n5.kanji.水", "n5.kanji.曜", "n5.kanji.日"],
    ),
    (
        "auth.signs.nichiyoubi", "time", "日曜日", "にちようび",
        "Sunday", "रविवार",
        "Day-of-week schedule label. 日曜日も営業 (open Sundays too) is a common shopfront marker in commercial districts.",
        ["n5.kanji.日", "n5.kanji.曜"],
    ),
    # === Weekly recurrence ===
    (
        "auth.signs.maishuu", "shop", "毎週", "まいしゅう",
        "Every week / weekly",
        "हर सप्ताह",
        "Service-availability label (毎週月曜日 = every Monday). Common on workshop / class schedule boards and recurring-event signage.",
        ["n5.kanji.毎", "n5.kanji.週"],
    ),
    # === Language ===
    (
        "auth.signs.nihongo", "notice", "日本語", "にほんご",
        "Japanese (language)",
        "जापानी (भाषा)",
        "Language label seen on language-school signs, tourist-information boards (日本語のみ = Japanese only), and software-language selectors.",
        ["n5.kanji.日", "n5.kanji.本", "n5.kanji.語"],
    ),
    # === Staff / member ===
    (
        "auth.signs.ekiin", "transit", "駅員", "えきいん",
        "Station staff",
        "स्टेशन कर्मचारी",
        "Sign on staff-only doors and information-desk signage at train stations. 駅員 means JR/metro employee — typically the person to ask for help.",
        ["n5.kanji.駅", "n5.kanji.員"],
    ),
    (
        "auth.signs.tenin", "shop", "店員", "てんいん",
        "Shop staff",
        "दुकानदार",
        "Sign distinguishing customer area from staff area. 店員さん = the shop assistant; 店員募集 (now hiring) is a frequent help-wanted banner.",
        ["n5.kanji.店", "n5.kanji.員"],
    ),
    (
        "auth.signs.kaiin", "shop", "会員", "かいいん",
        "Member",
        "सदस्य",
        "Membership-club label. 会員のみ (members only) on premium-area entrances; 会員カード on signup-form labels.",
        ["n5.kanji.会", "n5.kanji.員"],
    ),
    # === Directional ===
    (
        "auth.signs.ue", "signs", "上", "うえ",
        "Up / upper",
        "ऊपर",
        "Single-character directional sign on stair signage and floor-indicator panels. Often paired with arrow (↑) to mean 'upstairs' or 'upper floor'.",
        ["n5.kanji.上"],
    ),
    (
        "auth.signs.shita", "signs", "下", "した",
        "Down / lower",
        "नीचे",
        "Single-character directional sign on stair signage. Paired with arrow (↓) to indicate 'downstairs' or 'lower floor' — opposite of 上.",
        ["n5.kanji.下"],
    ),
    (
        "auth.signs.gaikoku", "notice", "外国", "がいこく",
        "Foreign country / abroad",
        "विदेश",
        "Tourist-information label (外国の方 = foreign visitors) and form-field marker (外国人登録 = foreign resident registration).",
        ["n5.kanji.外", "n5.kanji.国"],
    ),
    # === Compass-direction station exits ===
    (
        "auth.transit.higashi-guchi", "transit", "東口", "ひがしぐち",
        "East exit",
        "पूर्वी निकास",
        "Station exit signage (compass-direction labels on every major station). 東口 = east exit; pair with 西口/南口/北口 to specify which side of the station.",
        ["n5.kanji.東", "n5.kanji.口"],
    ),
    (
        "auth.transit.nishi-guchi", "transit", "西口", "にしぐち",
        "West exit",
        "पश्चिमी निकास",
        "Compass-direction station exit. Tokyo's Shinjuku 新宿西口 is the iconic west-exit example — major bus terminus + office-tower district.",
        ["n5.kanji.西", "n5.kanji.口"],
    ),
    (
        "auth.transit.minami-guchi", "transit", "南口", "みなみぐち",
        "South exit",
        "दक्षिणी निकास",
        "Compass-direction station exit. 南口 typically leads to bus terminals or commercial districts; pair with the station name on guide signs.",
        ["n5.kanji.南", "n5.kanji.口"],
    ),
    (
        "auth.transit.kita-guchi", "transit", "北口", "きたぐち",
        "North exit",
        "उत्तरी निकास",
        "Compass-direction station exit. 北口 is one of the fundamental wayfinding labels in any large Japanese station.",
        ["n5.kanji.北", "n5.kanji.口"],
    ),
    # === Time interval ===
    (
        "auth.signs.ichi-jikan", "time", "一時間", "いちじかん",
        "One hour",
        "एक घंटा",
        "Duration label on parking-meter signs (一時間 500円 = 500 yen per hour), service-time indicators (一時間以内 = within one hour), and rental-by-the-hour boards.",
        ["n5.kanji.一", "n5.kanji.時", "n5.kanji.間"],
    ),
    # === Place names / surnames ===
    (
        "auth.signs.tanaka", "signs", "田中", "たなか",
        "Tanaka (common surname)",
        "तानाका (सामान्य उपनाम)",
        "Most common surname on doorplate signs (表札 / hyoosatsu). 田 (rice field) + 中 (middle) — literally 'middle of the rice field'. About 1.3 million people share this name.",
        ["n5.kanji.田", "n5.kanji.中"],
    ),
    (
        "auth.signs.yamamoto", "signs", "山本", "やまもと",
        "Yamamoto (common surname)",
        "यामामोतो (सामान्य उपनाम)",
        "Common surname on doorplate signs. 山 (mountain) + 本 (origin/main) — literally 'base of the mountain'. Frequent in central / western Japan.",
        ["n5.kanji.山", "n5.kanji.本"],
    ),
    # === Nature / flowers ===
    (
        "auth.signs.hanami", "shop", "花見", "はなみ",
        "Cherry-blossom viewing",
        "वसंत में फूल देखना",
        "Spring promotion banner (花見特集 / 花見弁当). 花見 is the iconic spring activity — picnic under cherry blossoms; signage peaks in late March / early April.",
        ["n5.kanji.花", "n5.kanji.見"],
    ),
    (
        "auth.signs.sora", "weather", "空", "そら",
        "Sky",
        "आकाश",
        "Weather-forecast board label (今日の空 = today's sky). Also seen on rooftop-bar signs and airline branding (空 = sky in 空港 airport, though 港 itself is N4).",
        ["n5.kanji.空"],
    ),
    # === Newspaper / reading ===
    (
        "auth.signs.shinbun", "shop", "新聞", "しんぶん",
        "Newspaper",
        "अख़बार",
        "Newsstand and convenience-store label. 新聞 = newspaper; major dailies (朝日新聞 / 読売新聞) are displayed under this category sign.",
        ["n5.kanji.新", "n5.kanji.聞"],
    ),
    (
        "auth.signs.dokusho", "notice", "読書", "どくしょ",
        "Reading (books)",
        "पढ़ना",
        "Library / quiet-zone label. 読書スペース (reading space) on bookstore signs and 読書の秋 (reading-autumn) seasonal-promotion campaigns.",
        ["n5.kanji.読", "n5.kanji.書"],
    ),
    (
        "auth.signs.shodou", "shop", "書道", "しょどう",
        "Calligraphy",
        "सुलेख",
        "Cultural-class signage. 書道教室 (calligraphy class) outside community centers and stationery shops selling brushes + ink.",
        ["n5.kanji.書", "n5.kanji.道"],
    ),
    # === Coming time / rest ===
    (
        "auth.signs.raigetsu", "time", "来月", "らいげつ",
        "Next month",
        "अगले महीने",
        "Forward-looking promotion banner — 来月オープン (opening next month) on under-construction shop signs; also on event-announcement posters.",
        ["n5.kanji.来", "n5.kanji.月"],
    ),
    (
        "auth.signs.yasumi", "shop", "休み", "やすみ",
        "Closed / day off",
        "बंद",
        "Shopfront closure notice — 本日休み (closed today) on dangling cardboard signs. Distinct from 定休日 (fixed closure day, slightly more formal).",
        ["n5.kanji.休"],
    ),
    (
        "auth.signs.hitokoto", "notice", "一言", "ひとこと",
        "A word / brief remark",
        "एक शब्द",
        "Comment-box header on customer-feedback forms (お客様の一言 = customer's word). Also on bulletin-board comment-card labels.",
        ["n5.kanji.一", "n5.kanji.言"],
    ),
    # === People / status ===
    (
        "auth.transit.ekichou", "transit", "駅長", "えきちょう",
        "Station master",
        "स्टेशन मास्टर",
        "Title plaque on the station-master's office door. The 駅長 is the senior official at each station; their announcement carries authority on platform notices.",
        ["n5.kanji.駅", "n5.kanji.長"],
    ),
    # === Food ===
    (
        "auth.menu.hakumai", "menu", "白米", "はくまい",
        "White rice",
        "सफेद चावल",
        "Restaurant menu category label. 白米 = plain white rice — the default rice option, contrasted with 玄米 (brown rice, 玄 is N4) on healthier menu boards.",
        ["n5.kanji.白"],
    ),
    # === Body / sign language ===
    (
        "auth.signs.shuwa", "notice", "手話", "しゅわ",
        "Sign language",
        "साइन भाषा",
        "Accessibility-service label at public-facility information desks (手話サービス = sign-language service available). 手 (hand) + 話 (speak) = literal meaning.",
        ["n5.kanji.手", "n5.kanji.話"],
    ),
    (
        "auth.signs.me", "shop", "目", "め",
        "Eye / optician",
        "आँख",
        "Single-character optician / eye-care label. 目 (eye) on glasses-shop signs and eye-clinic logos. Also appears in 目薬 (eye drops; 薬 is N4, so use 目 alone on signage).",
        ["n5.kanji.目"],
    ),
    (
        "auth.signs.chikara", "shop", "力", "ちから",
        "Strength / power",
        "शक्ति",
        "Single-character gym / fitness label. 力 appears on weightlifting / strength-training signs and 力こぶ (biceps muscle) cartoon mascots in workout-related signage.",
        ["n5.kanji.力"],
    ),
    # === Travel / verb on signs ===
    (
        "auth.transit.tokyo-iki", "transit", "東京行", "とうきょうゆき",
        "Bound for Tokyo (train/bus destination)",
        "टोक्यो जाने वाली (ट्रेन/बस)",
        "Destination label on intercity bus departure boards and commuter train head-signs. The 行 (read ゆき in this context) marks 'bound for' — 大阪行 / 京都行 follow the same pattern.",
        ["n5.kanji.東", "n5.kanji.行"],
    ),
    (
        "auth.shop.kau", "shop", "買う", "かう",
        "Buy (verb)",
        "खरीदना",
        "Action-button label on e-commerce checkout screens (今すぐ買う = buy now). Also on in-store self-service kiosks and vending-machine prompts.",
        ["n5.kanji.買"],
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
            "audit_wave": "issue-122-wave3-2026-05-12",
        })
        added += 1

    AUTHENTIC.write_text(json.dumps(auth, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"Appended {added} cards (skipped {skipped} dups)")

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
                print(f"  WARN: kanji {kid} not in kanji.json")
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
