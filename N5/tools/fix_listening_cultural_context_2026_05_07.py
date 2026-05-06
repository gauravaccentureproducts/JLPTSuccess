"""Author cultural_context on the 38 listening items missing it.
Focuses on Japanese pragmatic + cultural conventions relevant to the
listening situation (politeness, social expectations, etiquette).

Idempotent. Marks cultural_context_provenance: llm_curated.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LISTENING = ROOT / 'data' / 'listening.json'

CALLOUTS: dict[str, str] = {
    'n5.listen.004': 'Japanese cafés default to hot drinks — staff will ask あつい (atsui, hot)? if you order a coffee/tea without specifying. Saying つめたい (cold) explicitly avoids ambiguity.',
    'n5.listen.006': 'Japanese librarians/clerks often gesture with あの たな (over there shelf) plus 上/下 (top/bottom). Confirming with question intonation (上ですか?) before reaching is polite.',
    'n5.listen.007': 'Seasonal preference is a common conversational icebreaker in Japan. あき (autumn) is widely loved for the moderate weather and 旬 seasonal foods (栗, 柿, さつまいも). Saying 〜が一番好きです is the standard preference structure.',
    'n5.listen.008': 'Birthday gift conversations: the asker often suggests likely gifts (本ですか? とけいですか?). The respondent gracefully redirects (いいえ, 新しい〜が ほしいです) without seeming demanding.',
    'n5.listen.009': 'Asking strangers for the time: open with すみません (excuse me) before すみません, 今 何時ですか? Maintaining brief eye contact and a small bow on receipt is conventional.',
    'n5.listen.010': 'Train ticket purchase at まどぐち (window): standard pattern — destination + 大人 (adult) X枚, 子供 (child) Y枚. Card readers are everywhere; tourists often use IC cards (Suica/PASMO) instead.',
    'n5.listen.011': 'Refusing food politely: いいえ、けっこうです (no thank you) is the standard polite refusal. Adding もう おなかが いっぱいです (already full) softens the refusal further. Just いりません (don\'t need) is too direct.',
    'n5.listen.012': 'Morning teacher greeting: おはようございます (good morning, polite) is the standard form for school/work; おはよう (casual) only with peers. A small bow accompanies it.',
    'n5.listen.013': 'Setting a meeting time: 何時に 会いますか? is the standard ask. Arriving 5 minutes early is normal in Japan; arriving on the dot is acceptable; even 1 minute late requires a brief すみません.',
    'n5.listen.014': 'Stations have multiple exits (出口). 北の出口 (north exit), 東口 (east exit), or specific 中央口 (central). Always confirming the specific exit avoids 30-min searches in major stations.',
    'n5.listen.015': 'Family shopping conversation pattern: parent asks 何を 買いますか?, child lists items with quantities and counters (りんごを 三つ, ぎゅうにゅうを 一本). Counters are mandatory in Japanese shopping speech.',
    'n5.listen.016': 'Schedule changes are normal: ですから (therefore) introduces the new plan. The pattern いそがしい (busy) → ですから 〜 (therefore X) is common.',
    'n5.listen.017': 'Late arrivals: たぶん (probably / maybe) softens the time prediction. 道が こんで います (the road is congested) is the most common reason given for delay; weather second.',
    'n5.listen.018': 'Travel verb 何で 行きますか? asks about transport mode (literally "by what?"). Standard answers: 電車で / バスで / 車で / 飛行機で (by train/bus/car/plane).',
    'n5.listen.019': 'School excuse pattern: a brief すみません (apology) opens; 〜が いたかった (was sick) is the most common reason; teachers often accept without further question for small lapses.',
    'n5.listen.020': 'Price commentary: 高いですね (its expensive) is a common conversational acknowledgment, not a complaint. Even when expensive, でも、おもしろい (but its interesting) softens the cost into a justification.',
    'n5.listen.021': 'Library hours change between weekdays and weekends — typical Japanese pattern: weekday 9-5, Saturday 1-4, Sunday closed. School libraries differ from public libraries.',
    'n5.listen.022': 'Weather small talk: 〜の 天気は どうですか? is the standard ask. Tomorrow weather (あしたの 天気) is the most common topic, followed by この 週末 (this weekend).',
    'n5.listen.023': 'Homework due-dates: 火よう日 / 木よう日 (Tuesday / Thursday) — Japanese teachers often give M-W-F or T-Th cycles. ありますか? confirms whether a particular day has homework.',
    'n5.listen.024': 'Hosting visitors: listing arrivals chronologically (父の 先生 + 母の 友だち + 父も). わかりました (understood) acknowledges the schedule.',
    'n5.listen.025': 'Morning school greeting: standard expected response is おはようございます (good morning, polite). A casual おはよう would be inappropriate to a teacher.',
    'n5.listen.026': 'Café ordering: すみません (excuse me) opens, then [item]を ください (please give me X) or [item]を おねがいします (Id like X). Both work; おねがいします is slightly more polite.',
    'n5.listen.027': 'Drink refusal politely: いいえ、けっこうです (no thank you, polite) or ありがとう、でも (thank you, but...) softens. Direct いりません (dont need) is too blunt.',
    'n5.listen.028': 'Entering someones home: おじゃまします (literally "Im intruding/disturbing") — said when entering. The host responds どうぞ (please, come in). Shoes go off at the entryway (げんかん).',
    'n5.listen.029': 'Before eating: いただきます (mandatory in Japan; literally "I humbly receive"). Said with palms joined or hands together briefly. Skipping it is socially rude even in casual settings.',
    'n5.listen.030': 'Asking directions: すみません (excuse me) → 〜へ 行きたいです (Id like to go to X) → 道が わかりません (I dont know the way). The askee will often gesture and walk you part of the way.',
    'n5.listen.031': 'Gift selection conversation pattern: 何が いいですか? (whats good?) → 〜が いいと 思います (I think X is good). Department stores have dedicated gift floors with wrapping included.',
    'n5.listen.032': 'Doctor visit: 一週間 (one week) of medication is a common prescription length. お大事に (take care / get well soon) is the standard parting from medical staff.',
    'n5.listen.033': 'Class scheduling: 月よう日と 水よう日 (Monday and Wednesday) — Japanese university classes often run on alternating days. 〜時から 〜時まで (from X to Y) is the standard time-range pattern.',
    'n5.listen.034': 'Restaurant order checks: ぜんぶで 〜円 (X yen total) closes the bill. Tipping does not exist in Japan — paying the exact bill amount or with bills/coins is normal.',
    'n5.listen.035': 'Birthday party invitation: いっしょに ケーキを 食べませんか? (wont you eat cake with us?) — the negative-question form (-ませんか) is the standard polite invitation.',
    'n5.listen.036': 'Lost-and-found at stations: えきいん (station staff) handle lost items. 落とし物 (lost item) is the formal term; 忘れ物 (forgotten thing) for things left on trains.',
    'n5.listen.037': 'Train delays: 電車が おくれて (the train is delayed) — train staff often issue a 遅延証明書 (delay certificate) so commuters can present it to teachers/employers.',
    'n5.listen.038': 'Asking about hobbies: しゅみは 何ですか? is the standard small-talk question. Common N5-level answers: スポーツ, おんがく, りょこう, りょうり (cooking).',
    'n5.listen.039': 'Apartment-search vocabulary: 駅から ちかい (close to the station), へやが 大きい (big rooms), 家ちんは X円 (rent is Y) — these are the standard housing-search criteria in Japanese.',
    'n5.listen.040': 'Gift exchange: もらう (receive) for things given to you, あげる (give) for things you give to others, くれる (give to me/us) for things others give to you. The trio is mandatory N5 vocabulary.',
    'n5.listen.046': 'Borrowing items politely: すみません (excuse me) + [item]を かして ください (please lend me X). 貸す (kasu, to lend) and 借りる (kariru, to borrow) are paired verbs — direction matters.',
    'n5.listen.047': 'Apology after a mistake: すみませんでした (Im sorry, past form) — used after the offense; すみません (present) before/during. The past form acknowledges that the offense happened.',
}


def main():
    with LISTENING.open('r', encoding='utf-8') as f:
        data = json.load(f)
    items = data['items']
    by_id = {it['id']: it for it in items}
    matched = 0
    skipped = 0
    not_found = []
    for iid, callout in CALLOUTS.items():
        it = by_id.get(iid)
        if it is None:
            not_found.append(iid)
            continue
        if it.get('cultural_context'):
            skipped += 1
            continue
        it['cultural_context'] = callout
        it['cultural_context_provenance'] = 'llm_curated'
        matched += 1
    print(f'Authored cultural_context on {matched} listening items.')
    print(f'Skipped (already had value): {skipped}')
    if not_found:
        print(f'IDs not found: {not_found}')
    with LISTENING.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


if __name__ == '__main__':
    main()
