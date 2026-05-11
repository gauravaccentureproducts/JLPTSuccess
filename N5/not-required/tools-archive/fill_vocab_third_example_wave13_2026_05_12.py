"""Waves 13+14 — extend 3rd vocab examples — next 100 by frequency_rank."""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

THIRD = {
    'n5.vocab.27-verbs-group-1-verbs.ふく':       {'ja': 'きょうは かぜが つよく ふいて います。','translation_en': 'The wind is blowing strongly today.'},
    'n5.vocab.37-common-nouns-miscella.けが':    {'ja': 'スポーツで けがを しました。',          'translation_en': 'I got injured playing sports.'},
    'n5.vocab.17-food-items.サンドイッチ':           {'ja': 'お昼は サンドイッチを 食べました。',   'translation_en': 'I had a sandwich for lunch.'},
    'n5.vocab.13-locations-and-places-.となり':   {'ja': 'いえの となりは こうえんです。',        'translation_en': 'Next to my house is a park.'},
    'n5.vocab.27-verbs-group-1-verbs.はじまる':   {'ja': 'えいがは 七時に はじまります。',         'translation_en': 'The movie starts at 7.'},
    'n5.vocab.24-school-and-study.かみ':         {'ja': '白い かみに 名前を 書きます。',        'translation_en': 'I write my name on white paper.'},
    'n5.vocab.13-locations-and-places-.はし':   {'ja': 'はしを わたって ください。',            'translation_en': 'Please cross the bridge.'},
    'n5.vocab.19-tableware-and-cooking.はし':    {'ja': 'はしで すしを 食べます。',              'translation_en': 'I eat sushi with chopsticks.'},
    'n5.vocab.28-verbs-group-2-verbs.しめる':     {'ja': 'まどを しめて ください。',              'translation_en': 'Please close the window.'},
    'n5.vocab.28-verbs-group-2-verbs.しめる.2':   {'ja': 'ネクタイを きちんと しめて ください。','translation_en': 'Please tie your necktie properly.'},
    'n5.vocab.37-common-nouns-miscella.ストーブ': {'ja': 'ふゆは ストーブを つかいます。',        'translation_en': 'I use a heater in winter.'},
    'n5.vocab.14-nature-and-weather.もり':       {'ja': 'いえの ちかくに もりが あります。',     'translation_en': 'There is a forest near my house.'},
    'n5.vocab.17-food-items.いちご':              {'ja': 'いちごの ケーキを 食べました。',        'translation_en': 'I ate strawberry cake.'},
    'n5.vocab.27-verbs-group-1-verbs.のぼる':   {'ja': 'らいしゅう 山に のぼります。',          'translation_en': 'I\'ll climb a mountain next week.'},
    'n5.vocab.27-verbs-group-1-verbs.さく':     {'ja': 'にわの 花が さきました。',              'translation_en': 'The garden flowers have bloomed.'},
    'n5.vocab.10-time-general.あした':            {'ja': 'あしたは 雨でしょう。',                'translation_en': 'It will probably rain tomorrow.'},
    'n5.vocab.17-food-items.ハンバーガー':         {'ja': 'お昼は ハンバーガーに します。',       'translation_en': 'I\'ll have a hamburger for lunch.'},
    'n5.vocab.17-food-items.ぶどう':              {'ja': 'あきは ぶどうが おいしいです。',        'translation_en': 'Grapes are delicious in autumn.'},
    'n5.vocab.30-verbs-existence-and-p.かす':    {'ja': '友だちに 本を かしました。',            'translation_en': 'I lent a book to a friend.'},
    'n5.vocab.32-adjectives.りっぱ':              {'ja': 'りっぱな ホテルですね。',              'translation_en': 'What a splendid hotel.'},
    'n5.vocab.17-food-items.天ぷら':              {'ja': '天ぷらを 食べたことが あります。',      'translation_en': 'I have eaten tempura before.'},
    'n5.vocab.4-body-parts.くち':                 {'ja': 'くちを あけて ください。',              'translation_en': 'Please open your mouth.'},
    'n5.vocab.21-clothing-and-accessor.かさ':    {'ja': 'あめなので、かさを もって 行きます。',  'translation_en': 'It\'s raining, so I\'ll take an umbrella.'},
    'n5.vocab.38-sounds-and-voice.こえ':         {'ja': '大きい こえで 話して ください。',      'translation_en': 'Please speak in a loud voice.'},
    'n5.vocab.21-clothing-and-accessor.セーター':{'ja': 'ふゆは セーターを きます。',            'translation_en': 'In winter I wear a sweater.'},
    'n5.vocab.24-school-and-study.れい':         {'ja': 'れいを 見せて ください。',              'translation_en': 'Please show me an example.'},
    'n5.vocab.28-verbs-group-2-verbs.いれる':    {'ja': 'コーヒーを いれましょうか。',           'translation_en': 'Shall I make some coffee?'},
    'n5.vocab.14-nature-and-weather.ほし':       {'ja': 'よる、ほしが きれいです。',             'translation_en': 'At night, the stars are beautiful.'},
    'n5.vocab.14-nature-and-weather.はれ':       {'ja': 'あしたは はれの 予報です。',            'translation_en': 'Tomorrow\'s forecast is clear.'},
    'n5.vocab.32-adjectives.にぎやか':             {'ja': 'この まちは とても にぎやかです。',     'translation_en': 'This town is very lively.'},
    'n5.vocab.14-nature-and-weather.なつ':       {'ja': 'なつは うみで およぎます。',            'translation_en': 'In summer I swim at the beach.'},
    'n5.vocab.33-adverbs.かならず':                {'ja': 'かならず 来て ください。',             'translation_en': 'Please come without fail.'},
    'n5.vocab.4-body-parts.かお':                 {'ja': 'まいあさ かおを あらいます。',          'translation_en': 'I wash my face every morning.'},
    'n5.vocab.14-nature-and-weather.うみ':       {'ja': 'なつに うみへ 行きます。',              'translation_en': 'I\'ll go to the sea in summer.'},
    'n5.vocab.16-food-and-drink-genera.おかし':  {'ja': 'おかしを 食べすぎました。',             'translation_en': 'I ate too many sweets.'},
    'n5.vocab.21-clothing-and-accessor.ハンカチ':{'ja': '新しい ハンカチを 一枚 もって います。','translation_en': 'I\'m carrying one new handkerchief.'},
    'n5.vocab.11-time-days-weeks-month.一日':    {'ja': '一日に 友だちと 会います。',             'translation_en': 'I\'ll meet a friend on the 1st.'},
    'n5.vocab.11-time-days-weeks-month.一日.2':  {'ja': '一日 中 雨でした。',                   'translation_en': 'It rained all day.'},
    'n5.vocab.17-food-items.みそ':                {'ja': 'みそスープを つくりました。',           'translation_en': 'I made miso soup.'},
    'n5.vocab.24-school-and-study.ボールペン':   {'ja': '青い ボールペンで しけんを 書きます。', 'translation_en': 'I write the exam with a blue pen.'},
    'n5.vocab.38-sounds-and-voice.おと':         {'ja': '大きい おとが しました。',              'translation_en': 'There was a loud sound.'},
    'n5.vocab.27-verbs-group-1-verbs.ひく':     {'ja': '父は ピアノを ひきます。',              'translation_en': 'My father plays the piano.'},
    'n5.vocab.27-verbs-group-1-verbs.ひく.2':   {'ja': '子どもが お母さんの 手を ひいて います。','translation_en': 'The child is pulling on their mother\'s hand.'},
    'n5.vocab.27-verbs-group-1-verbs.はく':     {'ja': '新しい くつを はきました。',            'translation_en': 'I put on new shoes.'},
    'n5.vocab.27-verbs-group-1-verbs.ふる':     {'ja': 'あめが はげしく ふって います。',       'translation_en': 'It\'s raining heavily.'},
    'n5.vocab.11-time-days-weeks-month.二日':    {'ja': '二日に かいぎが あります。',             'translation_en': 'There\'s a meeting on the 2nd.'},
    'n5.vocab.21-clothing-and-accessor.きもの': {'ja': 'ことしの しょうがつに きものを きました。','translation_en': 'I wore a kimono this New Year.'},
    'n5.vocab.27-verbs-group-1-verbs.わたる':   {'ja': 'はしを わたって こうえんへ 行きます。', 'translation_en': 'I cross the bridge to go to the park.'},
    'n5.vocab.20-colors.くろ':                    {'ja': 'くろい くつが すきです。',             'translation_en': 'I like black shoes.'},
    'n5.vocab.4-body-parts.あし':                  {'ja': 'はしったので、あしが いたいです。',     'translation_en': 'I ran, so my legs hurt.'},
    'n5.vocab.27-verbs-group-1-verbs.のる':     {'ja': '七時の 電車に のります。',              'translation_en': 'I\'ll catch the 7 o\'clock train.'},
    'n5.vocab.20-colors.いろ':                    {'ja': 'すきな いろは 何ですか。',             'translation_en': 'What\'s your favorite color?'},
    'n5.vocab.32-adjectives.きらい':              {'ja': 'にがい のみものが きらいです。',        'translation_en': 'I dislike bitter drinks.'},
    'n5.vocab.10-time-general.おととい':           {'ja': 'おととい 友だちと 会いました。',        'translation_en': 'I met a friend the day before yesterday.'},
    'n5.vocab.17-food-items.にく':                {'ja': '今夜は にくを 食べます。',             'translation_en': 'Tonight we\'re having meat.'},
    'n5.vocab.31-adjectives.わるい':              {'ja': 'てんきが わるく なって きました。',     'translation_en': 'The weather has gotten worse.'},
    'n5.vocab.21-clothing-and-accessor.かばん': {'ja': 'かばんに 本を 入れました。',             'translation_en': 'I put a book in my bag.'},
    'n5.vocab.19-tableware-and-cooking.なべ':   {'ja': 'なべで スープを つくりました。',        'translation_en': 'I made soup in a pot.'},
    'n5.vocab.26-house-and-furniture.まど':     {'ja': 'まどから うみが 見えます。',            'translation_en': 'You can see the sea from the window.'},
    'n5.vocab.37-common-nouns-miscella.キロメートル':{'ja': '駅まで 二キロメートル あります。', 'translation_en': 'It\'s 2 kilometers to the station.'},
    'n5.vocab.32-adjectives.ひま':               {'ja': 'こん夜は ひまですか。',                'translation_en': 'Are you free tonight?'},
    'n5.vocab.28-verbs-group-2-verbs.こたえる':   {'ja': 'しつもんに こたえて ください。',        'translation_en': 'Please answer the question.'},
    'n5.vocab.17-food-items.きゅうり':            {'ja': 'サラダに きゅうりを 入れました。',     'translation_en': 'I put cucumber in the salad.'},
    'n5.vocab.14-nature-and-weather.かぜ':       {'ja': 'きょうは かぜが つよいです。',          'translation_en': 'The wind is strong today.'},
    'n5.vocab.37-common-nouns-miscella.かぜ':   {'ja': 'かぜを ひきました。',                  'translation_en': 'I caught a cold.'},
    'n5.vocab.27-verbs-group-1-verbs.あく':     {'ja': 'まどが あきました。',                  'translation_en': 'The window opened.'},
    'n5.vocab.17-food-items.あめ':                {'ja': '子どもに あめを あげました。',          'translation_en': 'I gave candy to the child.'},
    'n5.vocab.21-clothing-and-accessor.めがね': {'ja': '父は めがねを かけて います。',         'translation_en': 'My father wears glasses.'},
    'n5.vocab.17-food-items.じゃがいも':            {'ja': 'じゃがいもで カレーを つくりました。',  'translation_en': 'I made curry with potatoes.'},
    'n5.vocab.32-adjectives.だいじょうぶ':         {'ja': 'だいじょうぶです、心配しないで ください。','translation_en': 'It\'s OK, please don\'t worry.'},
    'n5.vocab.32-adjectives.だいじ':              {'ja': 'これは とても だいじな ものです。',     'translation_en': 'This is a very important thing.'},
    'n5.vocab.32-adjectives.じょうぶ':             {'ja': 'この かばんは じょうぶです。',          'translation_en': 'This bag is sturdy.'},
    'n5.vocab.11-time-days-weeks-month.四日':    {'ja': '四日に お休みを とります。',             'translation_en': 'I\'ll take the 4th off.'},
    'n5.vocab.17-food-items.しょうゆ':             {'ja': 'すしに しょうゆを つけます。',          'translation_en': 'I dip the sushi in soy sauce.'},
    'n5.vocab.37-common-nouns-miscella.スリッパ':{'ja': 'いえの 中では スリッパを はきます。',  'translation_en': 'I wear slippers inside the house.'},
    'n5.vocab.10-time-general.けさ':              {'ja': 'けさは 六時に おきました。',           'translation_en': 'This morning I got up at 6.'},
    'n5.vocab.2-people-family.ともだち':           {'ja': '土曜日に ともだちと 出かけます。',     'translation_en': 'I\'m going out with a friend on Saturday.'},
    'n5.vocab.26-house-and-furniture.かぎ':     {'ja': 'いえの かぎを わすれました。',          'translation_en': 'I forgot my house key.'},
    'n5.vocab.28-verbs-group-2-verbs.あける':    {'ja': 'ドアを あけて ください。',              'translation_en': 'Please open the door.'},
    'n5.vocab.15-animals.ぶた':                   {'ja': 'のうじょうで ぶたを 見ました。',         'translation_en': 'I saw pigs at the farm.'},
    'n5.vocab.32-adjectives.へた':                {'ja': 'うたは とても へたです。',             'translation_en': 'I\'m really bad at singing.'},
    'n5.vocab.10-time-general.あさって':           {'ja': 'あさってから しごとが はじまります。', 'translation_en': 'Work starts the day after tomorrow.'},
    'n5.vocab.3-people-roles.駅員':                {'ja': '駅員に みちを 聞きました。',           'translation_en': 'I asked the station staff for directions.'},
    'n5.vocab.31-adjectives.おおい':              {'ja': 'こうえんに 人が おおいですね。',        'translation_en': 'There are many people in the park.'},
    'n5.vocab.17-food-items.にんじん':            {'ja': 'にんじんを 三本 買いました。',          'translation_en': 'I bought three carrots.'},
    'n5.vocab.27-verbs-group-1-verbs.つかう':   {'ja': 'まいにち パソコンを つかいます。',     'translation_en': 'I use a computer every day.'},
    'n5.vocab.27-verbs-group-1-verbs.すう':     {'ja': 'いきを 深く すって ください。',         'translation_en': 'Please take a deep breath.'},
    'n5.vocab.31-adjectives.あぶない':             {'ja': 'よるは ひとりで あるかないで。あぶないですよ。','translation_en': 'Don\'t walk alone at night — it\'s dangerous.'},
    'n5.vocab.33-adverbs.ぜんぶ':                  {'ja': 'ぜんぶ 食べました。',                 'translation_en': 'I ate all of it.'},
    'n5.vocab.21-clothing-and-accessor.くつ':   {'ja': '新しい くつを 一足 買いました。',       'translation_en': 'I bought one new pair of shoes.'},
    'n5.vocab.31-adjectives.さびしい':             {'ja': 'ひとりで いると さびしいです。',       'translation_en': 'I feel lonely when I\'m alone.'},
    'n5.vocab.15-animals.むし':                   {'ja': 'なつは むしが おおいです。',           'translation_en': 'In summer there are many insects.'},
    'n5.vocab.27-verbs-group-1-verbs.はたらく': {'ja': '父は ぎんこうで はたらいて います。',  'translation_en': 'My father works at a bank.'},
    'n5.vocab.13-locations-and-places-.よこ':  {'ja': 'いえの よこに こうえんが あります。',   'translation_en': 'There is a park beside my house.'},
    'n5.vocab.31-adjectives.たのしい':             {'ja': 'パーティーは とても たのしかったです。','translation_en': 'The party was very fun.'},
    'n5.vocab.32-adjectives.しずか':              {'ja': 'この としょかんは とても しずかです。','translation_en': 'This library is very quiet.'},
    'n5.vocab.28-verbs-group-2-verbs.つとめる':   {'ja': '兄は 大きい 会社に つとめて います。', 'translation_en': 'My older brother works for a big company.'},
    'n5.vocab.13-locations-and-places-.ちかく': {'ja': 'えきの ちかくに カフェが あります。',   'translation_en': 'There\'s a cafe near the station.'},
    'n5.vocab.26-house-and-furniture.まくら':   {'ja': '新しい まくらを 買いました。',          'translation_en': 'I bought a new pillow.'},
    'n5.vocab.37-common-nouns-miscella.キログラム':{'ja': 'こめを 五キログラム 買いました。',  'translation_en': 'I bought 5 kilograms of rice.'},
}


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_third_example_wave1314')
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
    print(f'\nWaves 13+14 added 3rd example on {n} more entries.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
