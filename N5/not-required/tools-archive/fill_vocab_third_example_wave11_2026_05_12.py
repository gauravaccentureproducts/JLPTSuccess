"""Waves 11+12 — extend 3rd vocab examples — next 100 by frequency_rank."""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

THIRD = {
    'n5.vocab.40-misc-useful-items.おもちゃ':      {'ja': '子どもに おもちゃを 買いました。',      'translation_en': 'I bought a toy for the child.'},
    'n5.vocab.37-common-nouns-miscella.カレンダー':{'ja': 'かべに カレンダーが あります。',       'translation_en': 'There is a calendar on the wall.'},
    'n5.vocab.10-time-general.こんばん':           {'ja': 'こんばんは あめが ふります。',           'translation_en': 'It will rain this evening.'},
    'n5.vocab.21-clothing-and-accessor.シャツ':    {'ja': '白い シャツを きました。',              'translation_en': 'I wore a white shirt.'},
    'n5.vocab.37-common-nouns-miscella.せびろ':    {'ja': 'けっこんしきで せびろを きました。',     'translation_en': 'I wore a suit at the wedding.'},
    'n5.vocab.31-adjectives.やさしい':              {'ja': 'この もんだいは やさしいです。',         'translation_en': 'This problem is easy.'},
    'n5.vocab.31-adjectives.むずかしい':            {'ja': 'かんじは とても むずかしいです。',      'translation_en': 'Kanji are very difficult.'},
    'n5.vocab.40-misc-useful-items.ねんれい':      {'ja': 'ねんれいを 書いて ください。',          'translation_en': 'Please write your age.'},
    'n5.vocab.28-verbs-group-2-verbs.出かける':     {'ja': '土曜日に 友だちと 出かけます。',        'translation_en': 'I\'m going out with a friend on Saturday.'},
    'n5.vocab.11-time-days-weeks-month.六月':      {'ja': '六月から なつが はじまります。',        'translation_en': 'Summer starts in June.'},
    'n5.vocab.37-common-nouns-miscella.にっき':    {'ja': 'まいばん にっきを 書きます。',          'translation_en': 'I write in my diary every night.'},
    'n5.vocab.19-tableware-and-cooking.ナイフ':    {'ja': 'ナイフで パンを 切ります。',             'translation_en': 'I cut bread with a knife.'},
    'n5.vocab.37-common-nouns-miscella.さくぶん':  {'ja': 'なつやすみの さくぶんを 書きました。',   'translation_en': 'I wrote a composition about summer vacation.'},
    'n5.vocab.2-people-family.おばさん':            {'ja': 'おばさんは 子どもが 三人 います。',      'translation_en': 'My aunt has three children.'},
    'n5.vocab.15-animals.ねこ':                    {'ja': 'うちには ねこが 二匹 います。',          'translation_en': 'We have two cats at home.'},
    'n5.vocab.24-school-and-study.ぶん':           {'ja': 'この ぶんは ながいですね。',            'translation_en': 'This sentence is long, isn\'t it?'},
    'n5.vocab.37-common-nouns-miscella.シャワー':  {'ja': 'まいあさ シャワーを あびます。',         'translation_en': 'I take a shower every morning.'},
    'n5.vocab.13-locations-and-places-.フロント': {'ja': 'ホテルの フロントで キーを もらいました。','translation_en': 'I got the key at the hotel front desk.'},
    'n5.vocab.21-clothing-and-accessor.とけい':    {'ja': '父から とけいを もらいました。',        'translation_en': 'I received a watch from my father.'},
    'n5.vocab.37-common-nouns-miscella.じびき':    {'ja': 'むかしは じびきで しらべました。',       'translation_en': 'In the past, I looked things up in a dictionary.'},
    'n5.vocab.13-locations-and-places-.出口':     {'ja': '出口は どこですか。',                   'translation_en': 'Where is the exit?'},
    'n5.vocab.33-adverbs.すこし':                   {'ja': 'すこし 待って ください。',              'translation_en': 'Please wait a little.'},
    'n5.vocab.27-verbs-group-1-verbs.だす':       {'ja': 'かばんから 本を だしました。',           'translation_en': 'I took the book out of the bag.'},
    'n5.vocab.14-nature-and-weather.あき':         {'ja': 'あきは すずしくて きもちが いいです。',  'translation_en': 'Autumn is cool and pleasant.'},
    'n5.vocab.11-time-days-weeks-month.七月':      {'ja': '七月から あつく なります。',            'translation_en': 'It gets hot from July.'},
    'n5.vocab.27-verbs-group-1-verbs.きる':       {'ja': 'ナイフで にんじんを きります。',         'translation_en': 'I cut the carrot with a knife.'},
    'n5.vocab.28-verbs-group-2-verbs.きる':        {'ja': 'けさは 青い シャツを きました。',       'translation_en': 'This morning I wore a blue shirt.'},
    'n5.vocab.11-time-days-weeks-month.九月':      {'ja': '九月に 学校が はじまります。',          'translation_en': 'School starts in September.'},
    'n5.vocab.11-time-days-weeks-month.八月':      {'ja': '八月は とても あついです。',            'translation_en': 'August is very hot.'},
    'n5.vocab.11-time-days-weeks-month.来月':      {'ja': '来月 けっこんします。',                'translation_en': 'I\'m getting married next month.'},
    'n5.vocab.13-locations-and-places-.デパート': {'ja': 'デパートで プレゼントを 買いました。',  'translation_en': 'I bought a present at the department store.'},
    'n5.vocab.22-money-and-shopping.レジ':         {'ja': 'レジで お金を はらいます。',            'translation_en': 'I pay at the cashier.'},
    'n5.vocab.11-time-days-weeks-month.二月':      {'ja': '二月は さむくて ゆきが ふります。',     'translation_en': 'February is cold and it snows.'},
    'n5.vocab.40-misc-useful-items.しゅっしん':    {'ja': 'しゅっしんは どこですか。',              'translation_en': 'Where are you from?'},
    'n5.vocab.4-body-parts.からだ':                {'ja': 'からだに 気を つけて ください。',       'translation_en': 'Please take care of your health.'},
    'n5.vocab.26-house-and-furniture.ベンチ':     {'ja': 'こうえんの ベンチで 休みました。',      'translation_en': 'I rested on the park bench.'},
    'n5.vocab.26-house-and-furniture.エレベーター':{'ja': 'エレベーターで 五かいに 行きました。',   'translation_en': 'I went to the 5th floor by elevator.'},
    'n5.vocab.33-adverbs.まっすぐ':                {'ja': 'まっすぐ 行って ください。',            'translation_en': 'Please go straight.'},
    'n5.vocab.15-animals.うま':                    {'ja': 'こうえんで うまを 見ました。',           'translation_en': 'I saw a horse at the park.'},
    'n5.vocab.12-time-frequency-sequen.ぜんぜん':  {'ja': 'おさけは ぜんぜん 飲みません。',         'translation_en': 'I don\'t drink alcohol at all.'},
    'n5.vocab.31-adjectives.うるさい':              {'ja': 'この みちは とても うるさいです。',     'translation_en': 'This street is very noisy.'},
    'n5.vocab.37-common-nouns-miscella.たばこ':    {'ja': 'たばこは すいません。',                'translation_en': 'I don\'t smoke.'},
    'n5.vocab.28-verbs-group-2-verbs.はじめる':    {'ja': '日本語の べんきょうを はじめました。', 'translation_en': 'I started studying Japanese.'},
    'n5.vocab.11-time-days-weeks-month.十月':      {'ja': '十月は うんどうかいの きせつです。',    'translation_en': 'October is the season for sports days.'},
    'n5.vocab.17-food-items.バナナ':                {'ja': 'まいあさ バナナを 一本 食べます。',     'translation_en': 'I eat one banana every morning.'},
    'n5.vocab.11-time-days-weeks-month.十二月':    {'ja': '十二月は とても いそがしいです。',      'translation_en': 'December is very busy.'},
    'n5.vocab.10-time-general.きのう':             {'ja': 'きのう 友だちと えいがを 見ました。',   'translation_en': 'I saw a movie with a friend yesterday.'},
    'n5.vocab.21-clothing-and-accessor.Tシャツ':  {'ja': 'なつは Tシャツを きます。',             'translation_en': 'I wear a T-shirt in summer.'},
    'n5.vocab.14-nature-and-weather.いし':         {'ja': '川に きれいな いしが あります。',       'translation_en': 'There are pretty stones in the river.'},
    'n5.vocab.31-adjectives.おもい':               {'ja': 'この にもつは おもいですね。',          'translation_en': 'This luggage is heavy.'},
    'n5.vocab.4-body-parts.おなか':                {'ja': 'おなかが すきました。',                'translation_en': 'I\'m hungry.'},
    'n5.vocab.26-house-and-furniture.タオル':     {'ja': 'シャワーの あとで タオルを つかいます。','translation_en': 'I use a towel after showering.'},
    'n5.vocab.28-verbs-group-2-verbs.ねる':       {'ja': 'まいばん 十時に ねます。',              'translation_en': 'I go to bed at 10 every night.'},
    'n5.vocab.15-animals.うし':                    {'ja': 'うしの ミルクを 飲みます。',            'translation_en': 'I drink cow\'s milk.'},
    'n5.vocab.27-verbs-group-1-verbs.まつ':       {'ja': 'えきで 友だちを まちました。',          'translation_en': 'I waited for a friend at the station.'},
    'n5.vocab.21-clothing-and-accessor.スカート':  {'ja': '新しい スカートを 買いました。',        'translation_en': 'I bought a new skirt.'},
    'n5.vocab.27-verbs-group-1-verbs.ちがう':     {'ja': 'こたえが ちがいます。',                'translation_en': 'The answer is different.'},
    'n5.vocab.26-house-and-furniture.カーテン':    {'ja': 'まどの カーテンを しめて ください。',   'translation_en': 'Please close the window curtain.'},
    'n5.vocab.17-food-items.こめ':                 {'ja': 'こめを 一キロ 買いました。',             'translation_en': 'I bought one kilo of rice.'},
    'n5.vocab.37-common-nouns-miscella.グラム':    {'ja': 'りんごは 二百グラムです。',             'translation_en': 'The apple weighs 200 grams.'},
    'n5.vocab.32-adjectives.すき':                 {'ja': 'にほんりょうりが すきです。',           'translation_en': 'I like Japanese cuisine.'},
    'n5.vocab.11-time-days-weeks-month.十一月':    {'ja': '十一月は こうようの きせつです。',      'translation_en': 'November is the season for autumn leaves.'},
    'n5.vocab.12-time-frequency-sequen.つぎ':     {'ja': 'つぎの 駅で 出ます。',                 'translation_en': 'I get off at the next station.'},
    'n5.vocab.10-time-general.ばん':               {'ja': 'ばんは おそく まで しごとを しました。','translation_en': 'I worked late into the evening.'},
    'n5.vocab.21-clothing-and-accessor.ズボン':   {'ja': '青い ズボンを きました。',              'translation_en': 'I wore blue trousers.'},
    'n5.vocab.27-verbs-group-1-verbs.休む':       {'ja': '土曜日は しごとを 休みます。',          'translation_en': 'I take Saturday off work.'},
    'n5.vocab.27-verbs-group-1-verbs.すむ':       {'ja': '兄は とうきょうに すんで います。',     'translation_en': 'My older brother lives in Tokyo.'},
    'n5.vocab.19-tableware-and-cooking.フォーク':  {'ja': 'フォークで サラダを 食べます。',        'translation_en': 'I eat salad with a fork.'},
    'n5.vocab.17-food-items.バター':                {'ja': 'パンに バターを ぬりました。',          'translation_en': 'I spread butter on the bread.'},
    'n5.vocab.19-tableware-and-cooking.おさら':    {'ja': 'おさらに ケーキを のせて ください。',   'translation_en': 'Please put the cake on the plate.'},
    'n5.vocab.14-nature-and-weather.はる':         {'ja': 'はるは あたたかいです。',              'translation_en': 'Spring is warm.'},
    'n5.vocab.27-verbs-group-1-verbs.はる':       {'ja': 'てがみに きってを はりました。',         'translation_en': 'I stuck a stamp on the letter.'},
    'n5.vocab.27-verbs-group-1-verbs.さす':       {'ja': 'あめが ふったので、かさを さしました。','translation_en': 'It rained, so I opened my umbrella.'},
    'n5.vocab.27-verbs-group-1-verbs.おもう':     {'ja': 'あしたは 雨だと おもいます。',          'translation_en': 'I think it will rain tomorrow.'},
    'n5.vocab.20-colors.あか':                     {'ja': 'あかい くるまが すきです。',           'translation_en': 'I like red cars.'},
    'n5.vocab.17-food-items.レモン':                {'ja': 'おちゃに レモンを 入れますか。',        'translation_en': 'Would you put lemon in your tea?'},
    'n5.vocab.17-food-items.キャベツ':              {'ja': 'キャベツを 半分 切りました。',          'translation_en': 'I cut a cabbage in half.'},
    'n5.vocab.26-house-and-furniture.かべ':       {'ja': 'かべに とけいが かかって います。',     'translation_en': 'There\'s a clock hanging on the wall.'},
    'n5.vocab.24-school-and-study.カタカナ':       {'ja': 'カタカナは 外来語に つかいます。',     'translation_en': 'Katakana is used for loanwords.'},
    'n5.vocab.27-verbs-group-1-verbs.かえる':     {'ja': 'まいばん 六時に いえに かえります。', 'translation_en': 'I return home at 6 every evening.'},
    'n5.vocab.15-animals.ぞう':                    {'ja': 'どうぶつえんで ぞうを 見ました。',       'translation_en': 'I saw an elephant at the zoo.'},
    'n5.vocab.21-clothing-and-accessor.ネクタイ':  {'ja': '父は 毎日 ネクタイを します。',         'translation_en': 'My father wears a necktie every day.'},
    'n5.vocab.17-food-items.みかん':                {'ja': 'ふゆは みかんを たくさん 食べます。',   'translation_en': 'In winter I eat lots of mandarins.'},
    'n5.vocab.19-tableware-and-cooking.コップ':    {'ja': 'コップに 水を 入れて ください。',       'translation_en': 'Please pour water into the cup.'},
    'n5.vocab.37-common-nouns-miscella.ティッシュ':{'ja': 'ティッシュを 一枚 ください。',          'translation_en': 'Please give me a tissue.'},
    'n5.vocab.2-people-family.おばあさん':          {'ja': 'おばあさんは いつも やさしいです。',   'translation_en': 'My grandmother is always kind.'},
    'n5.vocab.27-verbs-group-1-verbs.なくす':     {'ja': 'さいふを なくして しまいました。',      'translation_en': 'I lost my wallet.'},
    'n5.vocab.17-food-items.りんご':               {'ja': 'りんごを 二つ 買いました。',             'translation_en': 'I bought two apples.'},
    'n5.vocab.13-locations-and-places-.むら':     {'ja': 'この むらは とても しずかです。',       'translation_en': 'This village is very quiet.'},
    'n5.vocab.32-adjectives.おなじ':               {'ja': '二人は おなじ クラスです。',            'translation_en': 'The two are in the same class.'},
    'n5.vocab.19-tableware-and-cooking.さら':     {'ja': 'さらに 食べものを のせます。',          'translation_en': 'I put the food on the plate.'},
    'n5.vocab.2-people-family.おじいさん':          {'ja': 'おじいさんは 元気です。',              'translation_en': 'My grandfather is in good health.'},
    'n5.vocab.24-school-and-study.こたえ':         {'ja': 'こたえは わかりません。',               'translation_en': 'I don\'t know the answer.'},
    'n5.vocab.20-colors.みどり':                   {'ja': 'みどりの 木が きれいです。',           'translation_en': 'The green trees are beautiful.'},
    'n5.vocab.24-school-and-study.かんじ':         {'ja': '日本語の かんじを 五十 おぼえました。', 'translation_en': 'I learned 50 Japanese kanji.'},
    'n5.vocab.17-food-items.すし':                 {'ja': 'こん夜 すしを 食べに 行きませんか。',   'translation_en': 'Want to go eat sushi tonight?'},
    'n5.vocab.17-food-items.アイスクリーム':        {'ja': 'なつは アイスクリームを 毎日 食べます。','translation_en': 'I eat ice cream every day in summer.'},
    'n5.vocab.19-tableware-and-cooking.スプーン':  {'ja': 'スープを スプーンで 飲みます。',        'translation_en': 'I eat soup with a spoon.'},
    'n5.vocab.4-body-parts.はな':                   {'ja': 'はなが かゆいです。',                  'translation_en': 'My nose is itchy.'},
    'n5.vocab.21-clothing-and-accessor.ふく':     {'ja': '新しい ふくが ほしいです。',            'translation_en': 'I want new clothes.'},
}


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_third_example_wave1112')
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
    print(f'\nWaves 11+12 added 3rd example on {n} more entries.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
