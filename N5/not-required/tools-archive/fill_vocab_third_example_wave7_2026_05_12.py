"""Waves 7+8 — extend 3rd vocab examples — next 100 by frequency_rank."""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

THIRD = {
    'n5.vocab.27-verbs-group-1-verbs.しまる':     {'ja': 'まどが しまりました。',                'translation_en': 'The window closed.'},
    'n5.vocab.31-adjectives.とおい':              {'ja': 'えきは ここから とおいです。',          'translation_en': 'The station is far from here.'},
    'n5.vocab.37-common-nouns-miscella.ほんとう':  {'ja': 'ほんとうに ありがとうございました。',    'translation_en': 'Thank you very much, truly.'},
    'n5.vocab.33-adverbs.とくに':                  {'ja': 'とくに 何も いりません。',              'translation_en': 'I don\'t especially need anything.'},
    'n5.vocab.11-time-days-weeks-month.来週':    {'ja': '来週 友だちが 来ます。',                'translation_en': 'A friend is coming next week.'},
    'n5.vocab.26-house-and-furniture.しんしつ':   {'ja': 'しんしつは 二かいに あります。',         'translation_en': 'The bedroom is on the second floor.'},
    'n5.vocab.32-adjectives.だいすき':             {'ja': 'すしが だいすきです。',                'translation_en': 'I love sushi.'},
    'n5.vocab.32-adjectives.たいへん':             {'ja': 'しごとが とても たいへんです。',        'translation_en': 'My work is very tough.'},
    'n5.vocab.24-school-and-study.れんしゅう':    {'ja': 'まいにち 日本語の れんしゅうを します。','translation_en': 'I practice Japanese every day.'},
    'n5.vocab.11-time-days-weeks-month.さらいねん':{'ja': 'さらいねん 大学を そつぎょうします。', 'translation_en': 'I\'ll graduate from university the year after next.'},
    'n5.vocab.13-locations-and-places-.くうこう': {'ja': 'くうこうから タクシーで 来ました。',    'translation_en': 'I came from the airport by taxi.'},
    'n5.vocab.28-verbs-group-2-verbs.あつめる':    {'ja': '子どもは きってを あつめて います。',   'translation_en': 'The child collects stamps.'},
    'n5.vocab.16-food-and-drink-genera.のみもの': {'ja': 'のみものは 何が いいですか。',          'translation_en': 'What would you like to drink?'},
    'n5.vocab.24-school-and-study.きょうかしょ':  {'ja': 'きょうかしょを 三十ページまで 読みました。','translation_en': 'I read up to page 30 of the textbook.'},
    'n5.vocab.33-adverbs.いっしょに':              {'ja': 'いっしょに カフェに 行きませんか。',    'translation_en': 'Would you like to go to a cafe together?'},
    'n5.vocab.13-locations-and-places-.こうえん': {'ja': 'こうえんで 子どもが あそんで います。', 'translation_en': 'Children are playing in the park.'},
    'n5.vocab.27-verbs-group-1-verbs.会う':       {'ja': 'あした 友だちに 会います。',            'translation_en': 'I\'ll meet my friend tomorrow.'},
    'n5.vocab.31-adjectives.あかるい':             {'ja': 'この へやは とても あかるいです。',     'translation_en': 'This room is very bright.'},
    'n5.vocab.13-locations-and-places-.ポスト':   {'ja': 'てがみを ポストに 入れました。',        'translation_en': 'I put the letter in the mailbox.'},
    'n5.vocab.14-nature-and-weather.たいよう':    {'ja': 'けさは たいようが きれいでした。',      'translation_en': 'The sun was beautiful this morning.'},
    'n5.vocab.27-verbs-group-1-verbs.おとす':     {'ja': 'さいふを おとして しまいました。',      'translation_en': 'I dropped my wallet.'},
    'n5.vocab.14-nature-and-weather.田':         {'ja': '田は あおく ひろがって います。',       'translation_en': 'The rice fields spread out in green.'},
    'n5.vocab.17-food-items.ケーキ':              {'ja': 'たんじょうびの ケーキを 食べました。', 'translation_en': 'I ate birthday cake.'},
    'n5.vocab.32-adjectives.だいきらい':            {'ja': 'にがい のみものは だいきらいです。',    'translation_en': 'I hate bitter drinks.'},
    'n5.vocab.13-locations-and-places-.どうぶつえん':{'ja': '子どもと どうぶつえんに 行きました。','translation_en': 'I went to the zoo with my child.'},
    'n5.vocab.24-school-and-study.じしょ':       {'ja': 'わからない ことばは じしょで しらべます。','translation_en': 'I look up unknown words in the dictionary.'},
    'n5.vocab.2-people-family.お父さん':           {'ja': 'お父さんは 何の しごとを して いますか。','translation_en': 'What does your father do for work?'},
    'n5.vocab.11-time-days-weeks-month.毎週':    {'ja': '毎週 日曜日に そうじを します。',       'translation_en': 'I clean every Sunday.'},
    'n5.vocab.3-people-roles.外国人':              {'ja': 'この まちには 外国人が おおぜい います。','translation_en': 'There are many foreigners in this town.'},
    'n5.vocab.10-time-general.びょう':            {'ja': '十びょう 待って ください。',            'translation_en': 'Please wait 10 seconds.'},
    'n5.vocab.11-time-days-weeks-month.たんじょうび':{'ja': 'たんじょうび、おめでとうございます。','translation_en': 'Happy birthday!'},
    'n5.vocab.17-food-items.ぎゅうにく':           {'ja': 'ぎゅうにくを 一キロ 買いました。',      'translation_en': 'I bought one kilo of beef.'},
    'n5.vocab.18-drinks.こうちゃ':                 {'ja': '朝は こうちゃを 飲みます。',           'translation_en': 'I drink black tea in the morning.'},
    'n5.vocab.19-tableware-and-cooking.ちゃわん': {'ja': 'ちゃわんに ごはんを 入れました。',      'translation_en': 'I put rice in the bowl.'},
    'n5.vocab.22-money-and-shopping.きって':      {'ja': '八十円の きってを 五枚 ください。',     'translation_en': 'Please give me five 80-yen stamps.'},
    'n5.vocab.23-transport.じどうしゃ':            {'ja': 'じどうしゃで 会社に 行きます。',        'translation_en': 'I go to work by car.'},
    'n5.vocab.25-languages-and-countri.かんこく': {'ja': 'かんこくに 行ったことが あります。',    'translation_en': 'I have been to Korea.'},
    'n5.vocab.26-house-and-furniture.もうふ':     {'ja': 'さむいから もうふを 一枚 ください。',   'translation_en': 'Please give me a blanket — it\'s cold.'},
    'n5.vocab.40-misc-useful-items.ばしょ':       {'ja': 'えきの ばしょを おしえて ください。',   'translation_en': 'Please tell me where the station is.'},
    'n5.vocab.13-locations-and-places-.まち':    {'ja': 'この まちは とても しずかです。',       'translation_en': 'This town is very quiet.'},
    'n5.vocab.13-locations-and-places-.びじゅつかん':{'ja': '土曜日に びじゅつかんに 行きました。','translation_en': 'I went to the art museum on Saturday.'},
    'n5.vocab.11-time-days-weeks-month.金曜日':  {'ja': '金曜日に 友だちと カフェに 行きます。', 'translation_en': 'I\'m going to a cafe with a friend on Friday.'},
    'n5.vocab.19-tableware-and-cooking.カップ':   {'ja': 'このカップは とても きれいです。',     'translation_en': 'This cup is very beautiful.'},
    'n5.vocab.31-adjectives.まるい':              {'ja': 'まるい テーブルが ほしいです。',        'translation_en': 'I want a round table.'},
    'n5.vocab.24-school-and-study.ざっし':       {'ja': 'まいしゅう ざっしを 一さつ 読みます。',  'translation_en': 'I read one magazine every week.'},
    'n5.vocab.13-locations-and-places-.えいがかん':{'ja': 'えいがかんで えいがを 見ました。',    'translation_en': 'I saw a movie at the movie theater.'},
    'n5.vocab.28-verbs-group-2-verbs.見せる':     {'ja': 'パスポートを 見せて ください。',        'translation_en': 'Please show me your passport.'},
    'n5.vocab.37-common-nouns-miscella.やくそく':{'ja': 'やくそくを わすれないで ください。',    'translation_en': 'Please don\'t forget our appointment.'},
    'n5.vocab.27-verbs-group-1-verbs.くもる':    {'ja': 'そらが くもって きました。',            'translation_en': 'The sky has clouded over.'},
    'n5.vocab.32-adjectives.かんたん':             {'ja': 'この しけんは とても かんたんでした。','translation_en': 'This exam was very easy.'},
    'n5.vocab.24-school-and-study.えんぴつ':     {'ja': 'えんぴつを 一本 ください。',             'translation_en': 'Please give me one pencil.'},
    'n5.vocab.33-adverbs.じぶんで':                {'ja': 'じぶんで しゅくだいを しました。',     'translation_en': 'I did my homework by myself.'},
    'n5.vocab.28-verbs-group-2-verbs.生まれる':    {'ja': '東京で 生まれました。',                'translation_en': 'I was born in Tokyo.'},
    'n5.vocab.13-locations-and-places-.にわ':    {'ja': 'にわに きれいな 花が さいて います。',  'translation_en': 'Beautiful flowers are blooming in the garden.'},
    'n5.vocab.12-time-frequency-sequen.まいばん':{'ja': 'まいばん 本を 読みます。',              'translation_en': 'I read a book every night.'},
    'n5.vocab.28-verbs-group-2-verbs.きえる':     {'ja': 'でんきが きえました。',                'translation_en': 'The light went out.'},
    'n5.vocab.31-adjectives.しかくい':            {'ja': 'しかくい テーブルが あります。',        'translation_en': 'There is a square table.'},
    'n5.vocab.37-common-nouns-miscella.ようじ':  {'ja': 'すこし ようじが あります。',            'translation_en': 'I have a little errand to run.'},
    'n5.vocab.16-food-and-drink-genera.あさごはん':{'ja': '七時に あさごはんを 食べます。',      'translation_en': 'I eat breakfast at 7.'},
    'n5.vocab.37-common-nouns-miscella.ペット':  {'ja': 'うちには ペットの ねこが います。',     'translation_en': 'I have a pet cat at home.'},
    'n5.vocab.24-school-and-study.まんねんひつ':  {'ja': '父から まんねんひつを もらいました。',  'translation_en': 'I received a fountain pen from my father.'},
    'n5.vocab.13-locations-and-places-.たいしかん':{'ja': '日本の たいしかんは どこですか。',    'translation_en': 'Where is the Japanese embassy?'},
    'n5.vocab.26-house-and-furniture.ほんだな':  {'ja': 'ほんだなに 本が たくさん あります。',   'translation_en': 'There are many books on the bookshelf.'},
    'n5.vocab.13-locations-and-places-.コンビニ':{'ja': 'コンビニで おにぎりを 買いました。',    'translation_en': 'I bought rice balls at the convenience store.'},
    'n5.vocab.14-nature-and-weather.ふゆ':        {'ja': 'ふゆは とても さむいです。',           'translation_en': 'Winter is very cold.'},
    'n5.vocab.37-common-nouns-miscella.もんだい': {'ja': 'この もんだいは むずかしいです。',     'translation_en': 'This problem is difficult.'},
    'n5.vocab.3-people-roles.店員':                {'ja': '店員に 道を 聞きました。',              'translation_en': 'I asked the shop clerk for directions.'},
    'n5.vocab.11-time-days-weeks-month.毎月':    {'ja': '毎月 はじめに かいぎが あります。',     'translation_en': 'There\'s a meeting at the beginning of every month.'},
    'n5.vocab.2-people-family.男の子':            {'ja': 'あの 男の子は おとうとです。',         'translation_en': 'That boy is my younger brother.'},
    'n5.vocab.27-verbs-group-1-verbs.けす':      {'ja': 'へやの 電気を けして ください。',      'translation_en': 'Please turn off the room\'s light.'},
    'n5.vocab.32-adjectives.たいせつ':             {'ja': 'たいせつな ものを なくしました。',     'translation_en': 'I lost something important.'},
    'n5.vocab.37-common-nouns-miscella.フィルム':{'ja': '新しい フィルムを 一本 買いました。',   'translation_en': 'I bought one new film.'},
    'n5.vocab.13-locations-and-places-.こうばん':{'ja': 'こうばんで けいかんに 聞きました。',    'translation_en': 'I asked the policeman at the police box.'},
    'n5.vocab.23-transport.じてんしゃ':            {'ja': 'じてんしゃで 学校に 行きます。',        'translation_en': 'I go to school by bicycle.'},
    'n5.vocab.24-school-and-study.こくばん':     {'ja': '先生が こくばんに 字を 書きました。',   'translation_en': 'The teacher wrote on the blackboard.'},
    'n5.vocab.11-time-days-weeks-month.五日':    {'ja': '五日に 大事な かいぎが あります。',     'translation_en': 'There is an important meeting on the 5th.'},
    'n5.vocab.31-adjectives.わかい':              {'ja': 'わかい ときは よく 走りました。',      'translation_en': 'When I was young, I often ran.'},
    'n5.vocab.2-people-family.おじさん':           {'ja': 'おじさんは おおさかに すんで います。','translation_en': 'My uncle lives in Osaka.'},
    'n5.vocab.11-time-days-weeks-month.月曜日':  {'ja': '月曜日から しごとが はじまります。',    'translation_en': 'Work starts on Monday.'},
    'n5.vocab.26-house-and-furniture.アパート':   {'ja': '新しい アパートに ひっこしました。',    'translation_en': 'I moved into a new apartment.'},
    'n5.vocab.13-locations-and-places-.こうじょう':{'ja': 'こうじょうの 中は うるさいです。',    'translation_en': 'It\'s noisy inside the factory.'},
    'n5.vocab.37-common-nouns-miscella.たて':    {'ja': 'このカードの たては 十センチです。',   'translation_en': 'This card is 10 centimeters tall.'},
    'n5.vocab.13-locations-and-places-.こうさてん':{'ja': 'こうさてんで みぎに まがって ください。','translation_en': 'Please turn right at the intersection.'},
    'n5.vocab.37-common-nouns-miscella.パーティー':{'ja': 'こんしゅうの どようびに パーティーが あります。','translation_en': 'There\'s a party this Saturday.'},
    'n5.vocab.17-food-items.ぶたにく':            {'ja': 'ぶたにくが すきです。',                'translation_en': 'I like pork.'},
    'n5.vocab.21-clothing-and-accessor.ようふく':{'ja': 'にちようびに ようふくを 買いました。',  'translation_en': 'I bought Western clothes on Sunday.'},
    'n5.vocab.22-money-and-shopping.ふうとう':   {'ja': 'ふうとうに きってを はりました。',      'translation_en': 'I stuck a stamp on the envelope.'},
    'n5.vocab.25-languages-and-countri.かんこくご':{'ja': 'かんこくごを 少し はなせます。',     'translation_en': 'I can speak a little Korean.'},
    'n5.vocab.26-house-and-furniture.はブラシ':  {'ja': '新しい はブラシを 買いました。',        'translation_en': 'I bought a new toothbrush.'},
    'n5.vocab.28-verbs-group-2-verbs.つかれる':    {'ja': 'きょうは とても つかれました。',       'translation_en': 'I\'m very tired today.'},
    'n5.vocab.31-adjectives.ちゃいろい':           {'ja': 'ちゃいろい かばんを かいました。',     'translation_en': 'I bought a brown bag.'},
    'n5.vocab.32-adjectives.あんぜん':             {'ja': 'この みちは あんぜんです。',           'translation_en': 'This road is safe.'},
    'n5.vocab.37-common-nouns-miscella.りょこう':{'ja': 'らいねんの なつに りょこうに 行きます。','translation_en': 'I\'ll go on a trip next summer.'},
    'n5.vocab.27-verbs-group-1-verbs.はらう':    {'ja': 'カードで はらいます。',                'translation_en': 'I\'ll pay by card.'},
    'n5.vocab.20-tableware-and-cooking.はし-chopsticks':{'ja': 'おはしで ごはんを 食べます。','translation_en': 'I eat rice with chopsticks.'},
    'n5.vocab.24-school-and-study.けしゴム':     {'ja': 'けしゴムを かして ください。',          'translation_en': 'Please lend me an eraser.'},
    'n5.vocab.13-locations-and-places-.プール':  {'ja': 'まいしゅう プールで およぎます。',      'translation_en': 'I swim at the pool every week.'},
    'n5.vocab.13-locations-and-places-.いりぐち':{'ja': 'えきの いりぐちで まちましょう。',     'translation_en': 'Let\'s meet at the station entrance.'},
    'n5.vocab.16-food-and-drink-genera.ひるごはん':{'ja': 'いっしょに ひるごはんを 食べませんか。','translation_en': 'Would you like to have lunch together?'},
    'n5.vocab.37-common-nouns-miscella.うんどう':{'ja': 'まいあさ うんどうを します。',         'translation_en': 'I exercise every morning.'},
}


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_third_example_wave78')
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
    print(f'\nWaves 7+8 added 3rd example on {n} more entries.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
