"""Waves 9+10 — extend 3rd vocab examples — next 100 by frequency_rank."""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

THIRD = {
    'n5.vocab.25-languages-and-countri.国籍':     {'ja': '国籍は どこですか。',                  'translation_en': 'What is your nationality?'},
    'n5.vocab.22-money-and-shopping.アルバイト':  {'ja': '土曜日に アルバイトを して います。',  'translation_en': 'I work part-time on Saturdays.'},
    'n5.vocab.24-school-and-study.ちず':         {'ja': 'ちずを 見て みちを さがしました。',     'translation_en': 'I looked at the map to find my way.'},
    'n5.vocab.13-locations-and-places-.しょくどう':{'ja': '会社の しょくどうで 食べます。',      'translation_en': 'I eat at the company cafeteria.'},
    'n5.vocab.23-transport.きしゃ':              {'ja': 'むかしは きしゃで りょこうしました。',  'translation_en': 'In the past, we traveled by steam train.'},
    'n5.vocab.13-locations-and-places-.たてもの':{'ja': 'あの たてものは とても 高いです。',    'translation_en': 'That building is very tall.'},
    'n5.vocab.14-nature-and-weather.さむい':     {'ja': 'こん夜は とても さむいですね。',        'translation_en': 'It\'s very cold tonight, isn\'t it?'},
    'n5.vocab.37-common-nouns-miscella.しあい':  {'ja': 'らいしゅうの しあいは 土曜日です。',     'translation_en': 'Next week\'s match is on Saturday.'},
    'n5.vocab.33-adverbs.もういちど':              {'ja': 'もういちど 言って ください。',         'translation_en': 'Please say it once more.'},
    'n5.vocab.26-house-and-furniture.えいが':    {'ja': 'こん夜 えいがを 見ましょう。',          'translation_en': 'Let\'s watch a movie tonight.'},
    'n5.vocab.40-misc-useful-items.ばあい':      {'ja': 'いそぐ ばあいは タクシーを よびます。','translation_en': 'In an urgent case, I\'ll call a taxi.'},
    'n5.vocab.13-locations-and-places-.ろうか':  {'ja': 'ろうかで 走らないで ください。',        'translation_en': 'Please don\'t run in the hallway.'},
    'n5.vocab.37-common-nouns-miscella.きって':  {'ja': 'てがみに きってを はりました。',        'translation_en': 'I put a stamp on the letter.'},
    'n5.vocab.12-time-frequency-sequen.後で':   {'ja': '後で 電話します。',                    'translation_en': 'I\'ll call you later.'},
    'n5.vocab.24-school-and-study.電話番号':    {'ja': '電話番号を おしえて ください。',       'translation_en': 'Please tell me your phone number.'},
    'n5.vocab.12-time-frequency-sequen.さいしょ':{'ja': 'さいしょに 名前を 書いて ください。',  'translation_en': 'Please write your name first.'},
    'n5.vocab.17-food-items.スープ':             {'ja': 'あったかい スープを 飲みました。',      'translation_en': 'I had warm soup.'},
    'n5.vocab.13-locations-and-places-.とおく': {'ja': 'とおくに 山が 見えます。',              'translation_en': 'You can see mountains far away.'},
    'n5.vocab.25-languages-and-countri.中国語': {'ja': '中国語を べんきょうして います。',      'translation_en': 'I\'m studying Chinese.'},
    'n5.vocab.24-school-and-study.ペン':        {'ja': '青い ペンを かして ください。',        'translation_en': 'Please lend me a blue pen.'},
    'n5.vocab.21-clothing-and-accessor.うわぎ': {'ja': 'さむいから うわぎを きました。',        'translation_en': 'I put on a jacket because it\'s cold.'},
    'n5.vocab.37-common-nouns-miscella.りゅうがく':{'ja': '兄は アメリカに りゅうがくして います。','translation_en': 'My older brother is studying abroad in America.'},
    'n5.vocab.24-school-and-study.じゅんび':    {'ja': 'しけんの じゅんびを して います。',     'translation_en': 'I\'m preparing for the exam.'},
    'n5.vocab.21-clothing-and-accessor.コート': {'ja': 'ふゆは コートを きます。',              'translation_en': 'I wear a coat in winter.'},
    'n5.vocab.13-locations-and-places-.むこう': {'ja': 'みちの むこうに ぎんこうが あります。','translation_en': 'There is a bank on the other side of the road.'},
    'n5.vocab.16-food-and-drink-genera.ばんごはん':{'ja': 'ばんごはんは いっしょに 食べましょう。','translation_en': 'Let\'s have dinner together.'},
    'n5.vocab.11-time-days-weeks-month.四月':   {'ja': '四月から 新しい しごとが はじまります。','translation_en': 'A new job starts in April.'},
    'n5.vocab.15-animals.どうぶつ':              {'ja': 'どうぶつが すきな 子どもです。',        'translation_en': 'The child likes animals.'},
    'n5.vocab.17-food-items.とりにく':           {'ja': 'こん夜は とりにくを 食べます。',        'translation_en': 'Tonight we\'re having chicken.'},
    'n5.vocab.18-drinks.ぎゅうにゅう':            {'ja': 'まいあさ ぎゅうにゅうを 一杯 飲みます。','translation_en': 'I drink a cup of milk every morning.'},
    'n5.vocab.19-tableware-and-cooking.おわん': {'ja': 'おわんに スープを 入れて ください。',  'translation_en': 'Please put the soup in the bowl.'},
    'n5.vocab.20-colors.きいろ':                 {'ja': 'きいろい シャツを きました。',         'translation_en': 'I wore a yellow shirt.'},
    'n5.vocab.23-transport.ちかてつ':            {'ja': 'ちかてつで 学校に 行きます。',         'translation_en': 'I go to school by subway.'},
    'n5.vocab.25-languages-and-countri.フランスご':{'ja': 'フランスごを 少し はなせます。',    'translation_en': 'I can speak a little French.'},
    'n5.vocab.26-house-and-furniture.おんがく':  {'ja': 'まいばん おんがくを 聞きます。',       'translation_en': 'I listen to music every night.'},
    'n5.vocab.37-common-nouns-miscella.けっこん':{'ja': '兄は 来年 けっこんします。',           'translation_en': 'My older brother is getting married next year.'},
    'n5.vocab.13-locations-and-places-.おてら': {'ja': 'きょうとの おてらに 行きました。',     'translation_en': 'I went to a temple in Kyoto.'},
    'n5.vocab.24-school-and-study.たんご':      {'ja': '毎日 新しい たんごを おぼえます。',    'translation_en': 'I memorize new vocabulary every day.'},
    'n5.vocab.33-adverbs.べつべつ':              {'ja': 'はらいは べつべつで おねがいします。','translation_en': 'Please charge us separately.'},
    'n5.vocab.33-adverbs.だんだん':              {'ja': 'だんだん さむく なります。',            'translation_en': 'It\'s gradually getting cold.'},
    'n5.vocab.12-time-frequency-sequen.もうすぐ':{'ja': 'もうすぐ えきに つきます。',           'translation_en': 'We\'ll arrive at the station soon.'},
    'n5.vocab.14-nature-and-weather.ゆき':       {'ja': '今 ふゆで、ゆきが ふって います。',     'translation_en': 'It\'s winter now and snowing.'},
    'n5.vocab.14-nature-and-weather.すずしい':  {'ja': 'あきは すずしいです。',                 'translation_en': 'Autumn is cool.'},
    'n5.vocab.37-common-nouns-miscella.びょうき':{'ja': '父が びょうきで にゅういんしました。', 'translation_en': 'My father became ill and was hospitalized.'},
    'n5.vocab.11-time-days-weeks-month.三月':   {'ja': '三月に 学校を そつぎょうします。',     'translation_en': 'I\'ll graduate from school in March.'},
    'n5.vocab.37-common-nouns-miscella.はいざら':{'ja': 'はいざらは ありません。たばこは すえません。','translation_en': 'There\'s no ashtray. No smoking.'},
    'n5.vocab.33-adverbs.まあまあ':              {'ja': 'きょうの しけんは まあまあでした。',   'translation_en': 'Today\'s exam was so-so.'},
    'n5.vocab.17-food-items.チョコレート':       {'ja': 'たんじょうびに チョコレートを もらいました。','translation_en': 'I got chocolate for my birthday.'},
    'n5.vocab.16-food-and-drink-genera.ゆうはん':{'ja': 'ゆうはんは ラーメンに しましょう。',  'translation_en': 'Let\'s have ramen for dinner.'},
    'n5.vocab.21-clothing-and-accessor.ぼうし': {'ja': 'あつい 日には ぼうしを かぶります。',  'translation_en': 'On hot days I wear a hat.'},
    'n5.vocab.37-common-nouns-miscella.よてい':  {'ja': 'こん夜の よていは ありますか。',       'translation_en': 'Do you have plans for tonight?'},
    'n5.vocab.31-i-adjectives.にこにこ':         {'ja': 'おばあさんは いつも にこにこ して います。','translation_en': 'Grandmother is always smiling.'},
    'n5.vocab.37-common-nouns-miscella.マッチ':  {'ja': 'マッチで 火を つけました。',           'translation_en': 'I lit the fire with a match.'},
    'n5.vocab.23-transport.ひこうき':            {'ja': 'ひこうきで パリへ 行きます。',          'translation_en': 'I\'m flying to Paris.'},
    'n5.vocab.37-common-nouns-miscella.じかんわり':{'ja': '新しい じかんわりを もらいました。','translation_en': 'I received a new timetable.'},
    'n5.vocab.20-colors.ピンク':                 {'ja': 'ピンクの ぼうしを 買いました。',       'translation_en': 'I bought a pink hat.'},
    'n5.vocab.17-food-items.チーズ':             {'ja': 'パンに チーズを のせて 食べます。',    'translation_en': 'I put cheese on bread and eat it.'},
    'n5.vocab.17-food-items.うどん':             {'ja': 'お昼に うどんを 食べました。',          'translation_en': 'I had udon for lunch.'},
    'n5.vocab.12-time-frequency-sequen.さいご': {'ja': 'さいごに 答えを しらべました。',       'translation_en': 'I checked the answers at the end.'},
    'n5.vocab.17-food-items.やさい':             {'ja': 'まいにち やさいを 食べて います。',    'translation_en': 'I eat vegetables every day.'},
    'n5.vocab.22-money-and-shopping.にもつ':    {'ja': 'にもつは おもいです。',                'translation_en': 'The luggage is heavy.'},
    'n5.vocab.37-common-nouns-miscella.はこ':   {'ja': 'はこに プレゼントを 入れました。',      'translation_en': 'I put the present in a box.'},
    'n5.vocab.40-misc-useful-items.じゅうしょ':  {'ja': 'じゅうしょを 書いて ください。',        'translation_en': 'Please write your address.'},
    'n5.vocab.25-languages-and-countri.スペイン人':{'ja': '友だちは スペイン人です。',           'translation_en': 'My friend is Spanish.'},
    'n5.vocab.28-verbs-group-2-verbs.聞こえる':  {'ja': 'こえが 聞こえません。',                'translation_en': 'I can\'t hear your voice.'},
    'n5.vocab.11-time-days-weeks-month.先月':   {'ja': '先月から 日本語を 始めました。',       'translation_en': 'I started Japanese last month.'},
    'n5.vocab.22-money-and-shopping.セール':    {'ja': 'きょうから 大セールが はじまります。',  'translation_en': 'A big sale starts today.'},
    'n5.vocab.37-common-nouns-miscella.はたち': {'ja': 'こんしゅう はたちに なりました。',     'translation_en': 'I turned 20 this week.'},
    'n5.vocab.33-adverbs.わくわく':              {'ja': 'りょこうの まえは わくわくします。',   'translation_en': 'I get excited before a trip.'},
    'n5.vocab.16-food-and-drink-genera.しょくじ':{'ja': 'しょくじの じかんですよ。',            'translation_en': 'It\'s meal time.'},
    'n5.vocab.11-time-days-weeks-month.火曜日':  {'ja': '火曜日に かいぎが あります。',          'translation_en': 'There\'s a meeting on Tuesday.'},
    'n5.vocab.23-transport.ふね':                {'ja': 'ふねで しまへ 行きました。',            'translation_en': 'I went to the island by boat.'},
    'n5.vocab.14-nature-and-weather.さくら':    {'ja': '四月に さくらが きれいに さきます。',  'translation_en': 'Cherry blossoms bloom beautifully in April.'},
    'n5.vocab.21-clothing-and-accessor.くつした':{'ja': '新しい くつしたを 一足 買いました。',  'translation_en': 'I bought one pair of new socks.'},
    'n5.vocab.37-common-nouns-miscella.なつやすみ':{'ja': 'なつやすみに りょこうに 行きました。','translation_en': 'I went on a trip during summer vacation.'},
    'n5.vocab.33-adverbs.どきどき':              {'ja': 'しけんの まえは どきどきします。',     'translation_en': 'Before exams my heart pounds.'},
    'n5.vocab.17-food-items.トマト':             {'ja': 'にわで トマトを そだてて います。',    'translation_en': 'I\'m growing tomatoes in the garden.'},
    'n5.vocab.11-time-days-weeks-month.五月':   {'ja': '五月に たんじょうびが あります。',     'translation_en': 'My birthday is in May.'},
    'n5.vocab.21-clothing-and-accessor.ポケット':{'ja': 'ポケットに かぎを 入れました。',        'translation_en': 'I put the key in my pocket.'},
    'n5.vocab.37-common-nouns-miscella.りょうり':{'ja': '母は りょうりが じょうずです。',       'translation_en': 'My mother is good at cooking.'},
    'n5.vocab.11-time-days-weeks-month.木曜日':  {'ja': '木曜日に 日本語の じゅぎょうが あります。','translation_en': 'There\'s a Japanese class on Thursday.'},
    'n5.vocab.11-time-days-weeks-month.一月':   {'ja': '一月は とても さむいです。',           'translation_en': 'January is very cold.'},
    'n5.vocab.18-drinks.ジュース':                {'ja': '子どもは ジュースが すきです。',        'translation_en': 'Children like juice.'},
    'n5.vocab.37-common-nouns-miscella.かてい': {'ja': 'この 子は あたたかい かていに そだちました。','translation_en': 'This child grew up in a warm home.'},
    'n5.vocab.33-adverbs.ぴかぴか':              {'ja': '新しい くつが ぴかぴか して います。', 'translation_en': 'The new shoes are sparkling.'},
    'n5.vocab.11-time-days-weeks-month.水曜日':  {'ja': '水曜日は 学校が ありません。',          'translation_en': 'There\'s no school on Wednesday.'},
    'n5.vocab.16-food-and-drink-genera.ごはん': {'ja': 'こん夜は ごはんを たくさん 食べました。','translation_en': 'I ate a lot of rice tonight.'},
    'n5.vocab.17-food-items.サラダ':             {'ja': 'ばんごはんに サラダを つくりました。', 'translation_en': 'I made a salad for dinner.'},
    'n5.vocab.16-food-and-drink-genera.おべんとう':{'ja': 'まいにち おべんとうを もって 行きます。','translation_en': 'I bring a bento every day.'},
    'n5.vocab.17-food-items.だいこん':           {'ja': 'やおやで 大きい だいこんを 買いました。','translation_en': 'I bought a big daikon at the greengrocer.'},
    'n5.vocab.18-drinks.おさけ':                {'ja': 'おさけは あまり 飲みません。',          'translation_en': 'I don\'t drink alcohol much.'},
    'n5.vocab.19-tableware-and-cooking.れいぞうこ':{'ja': 'たべものを れいぞうこに 入れて ください。','translation_en': 'Please put the food in the fridge.'},
    'n5.vocab.20-colors.ちゃいろ':                {'ja': 'ちゃいろの くつが 好きです。',          'translation_en': 'I like brown shoes.'},
    'n5.vocab.23-transport.しんごう':            {'ja': 'しんごうが あかです。',                'translation_en': 'The traffic light is red.'},
    'n5.vocab.37-common-nouns-miscella.かびん': {'ja': 'かびんに 花を 入れました。',             'translation_en': 'I put flowers in the vase.'},
    'n5.vocab.36-greetings-and-set-phr.ぺこぺこ':{'ja': 'おなかが ぺこぺこです。',              'translation_en': 'I\'m starving.'},
    'n5.vocab.31-adjectives.まずい':              {'ja': 'この りょうりは まずいですね。',       'translation_en': 'This dish tastes bad.'},
    'n5.vocab.31-adjectives.つまらない':           {'ja': 'この えいがは つまらないです。',       'translation_en': 'This movie is boring.'},
    'n5.vocab.21-clothing-and-accessor.さいふ':  {'ja': 'さいふを 家に わすれました。',          'translation_en': 'I forgot my wallet at home.'},
    'n5.vocab.37-common-nouns-miscella.おくさん':{'ja': '田中さんの おくさんは 先生です。',     'translation_en': 'Mr. Tanaka\'s wife is a teacher.'},
}


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_third_example_wave910')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')
    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {e['id']: e for e in data['entries']}
    n = 0
    for vid, ex in THIRD.items():
        e = by_id.get(vid)
        if not e:
            print(f'  ! not found: {vid}'); continue
        exs = e.get('examples') or []
        if len(exs) >= 3:
            continue
        exs.append({'ja': ex['ja'], 'translation_en': ex['translation_en'], 'provenance': 'llm_curated'})
        e['examples'] = exs
        n += 1
    print(f'\nWaves 9+10 added 3rd example on {n} more entries.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
