"""Phase 6 of the example-coverage authoring pass (2026-05-03).

Targets the still-uncovered sections after Phase 5: time-general tail,
days-of-month + months, locations tail, food items tail, tableware,
clothing tail, animals tail, common nouns misc, school/study tail.

All keys verified against actual data IDs (no more form-mismatches).

Idempotent. Constraints: N5 kanji + kana only.
"""
import io, json, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
P = 'n5.vocab.'

def E(ja, en):
    return {'ja': ja, 'translation_en': en}

ADDITIONS = {
    # 10. Time-general tail
    P+'10-time-general.とき':           E('小さい とき、よく あそびました。', 'When I was little, I used to play a lot.'),
    P+'10-time-general.とけい':         E('とけいを 見ます。', 'I look at the clock.'),
    P+'10-time-general.おととい':       E('おととい 友だちに 会いました。', 'I met a friend the day before yesterday.'),
    P+'10-time-general.けさ':           E('けさ パンを 食べました。', 'This morning I ate bread.'),
    P+'10-time-general.こんばん':       E('こんばん えいがを 見ます。', 'This evening I will watch a movie.'),
    P+'10-time-general.こんや':         E('こんや 家に います。', "I'll be home tonight."),
    P+'10-time-general.午前':           E('午前 九時に はじまります。', 'It starts at 9 a.m.'),
    P+'10-time-general.午後':           E('午後 三時に 会いましょう。', "Let's meet at 3 p.m."),
    P+'10-time-general.半':             E('今 三時半です。', "It's 3:30 now."),
    P+'10-time-general.分':             E('十分 まって ください。', 'Please wait ten minutes.'),

    # 11. Days/months
    P+'11-time-days-weeks-month.一日':       E('一日に 田中さんに 会います。', "I'll see Tanaka-san on the 1st."),
    P+'11-time-days-weeks-month.一日.2':     E('一日 ゆっくり 休みました。', 'I rested for a whole day.'),
    P+'11-time-days-weeks-month.二日':       E('二日 休みを とります。', "I'll take two days off."),
    P+'11-time-days-weeks-month.三日':       E('三日 まえに 来ました。', 'I came three days ago.'),
    P+'11-time-days-weeks-month.四日':       E('四日 まちました。', 'I waited four days.'),
    P+'11-time-days-weeks-month.五日':       E('五日に 出かけます。', "I'll go out on the 5th."),
    P+'11-time-days-weeks-month.六日':       E('六日まで 休みです。', "I'm off until the 6th."),
    P+'11-time-days-weeks-month.七日':       E('七日に 友だちと 会います。', "I'll meet a friend on the 7th."),
    P+'11-time-days-weeks-month.八日':       E('八日に たんじょうびが あります。', "There's a birthday on the 8th."),
    P+'11-time-days-weeks-month.九日':       E('九日に かえります。', "I'll return on the 9th."),
    P+'11-time-days-weeks-month.十日':       E('十日 やすみます。', "I'll rest for ten days."),
    P+'11-time-days-weeks-month.二十日':     E('二十日に しゅっぱつします。', "I'll depart on the 20th."),
    P+'11-time-days-weeks-month.週':         E('一週に 二かい じゅぎょうが あります。', 'There are classes twice a week.'),
    P+'11-time-days-weeks-month.先週':       E('先週 京都に 行きました。', 'I went to Kyoto last week.'),
    P+'11-time-days-weeks-month.月':         E('月が きれいです。', 'The moon is beautiful.'),
    P+'11-time-days-weeks-month.一月':       E('一月は さむいです。', 'January is cold.'),
    P+'11-time-days-weeks-month.二月':       E('二月に たんじょうびが あります。', "My birthday is in February."),
    P+'11-time-days-weeks-month.三月':       E('三月は はるです。', 'March is spring.'),
    P+'11-time-days-weeks-month.四月':       E('四月に 学校が はじまります。', 'School begins in April.'),
    P+'11-time-days-weeks-month.五月':       E('五月は あたたかいです。', 'May is warm.'),
    P+'11-time-days-weeks-month.六月':       E('六月は 雨が おおいです。', 'June has lots of rain.'),
    P+'11-time-days-weeks-month.七月':       E('七月は 夏です。', 'July is summer.'),
    P+'11-time-days-weeks-month.八月':       E('八月は あついです。', 'August is hot.'),
    P+'11-time-days-weeks-month.九月':       E('九月に 学校が はじまります。', 'School starts in September.'),
    P+'11-time-days-weeks-month.十月':       E('十月は すずしいです。', 'October is cool.'),
    P+'11-time-days-weeks-month.十一月':     E('十一月は あきです。', 'November is autumn.'),
    P+'11-time-days-weeks-month.十二月':     E('十二月は さむいです。', 'December is cold.'),
    P+'11-time-days-weeks-month.先月':       E('先月 旅行しました。', 'I traveled last month.'),
    P+'11-time-days-weeks-month.毎月':       E('毎月 一回 あいます。', 'We meet once a month.'),
    P+'11-time-days-weeks-month.年':         E('一年は 十二か月です。', 'One year is twelve months.'),
    P+'11-time-days-weeks-month.きょねん':   E('きょねん 日本に 行きました。', 'I went to Japan last year.'),
    P+'11-time-days-weeks-month.毎年':       E('毎年 たんじょうびを いわいます。', 'I celebrate my birthday every year.'),
    P+'11-time-days-weeks-month.おととし':   E('おととし 大学を そつぎょうしました。', 'I graduated university the year before last.'),
    P+'11-time-days-weeks-month.さらいねん': E('さらいねん 日本に 行きます。', "I'll go to Japan the year after next."),

    # 12. Time-frequency tail
    P+'12-time-frequency-sequen.まいあさ':   E('まいあさ コーヒーを 飲みます。', 'I drink coffee every morning.'),
    P+'12-time-frequency-sequen.まいばん':   E('まいばん 本を 読みます。', 'I read a book every night.'),
    P+'12-time-frequency-sequen.すぐ':       E('すぐ 来ます。', "I'll come right away."),
    P+'12-time-frequency-sequen.もうすぐ':   E('もうすぐ 学校が はじまります。', 'School starts soon.'),
    P+'12-time-frequency-sequen.さいしょ':   E('さいしょに 名前を 書きます。', 'First, write your name.'),
    P+'12-time-frequency-sequen.つぎ':       E('つぎは わたしです。', "I'm next."),
    P+'12-time-frequency-sequen.後で':       E('後で でんわします。', "I'll call later."),

    # 13. Locations tail
    P+'13-locations-and-places-.ところ':     E('しずかな ところで 休みます。', 'I rest in a quiet place.'),
    P+'13-locations-and-places-.だいどころ': E('だいどころで りょうりを します。', 'I cook in the kitchen.'),
    P+'13-locations-and-places-.おてあらい': E('おてあらいは どこですか。', 'Where is the restroom?'),
    P+'13-locations-and-places-.トイレ':     E('トイレは あちらです。', "The toilet is over there."),
    P+'13-locations-and-places-.おふろ':     E('おふろに 入ります。', 'I take a bath.'),
    P+'13-locations-and-places-.げんかん':   E('げんかんで くつを ぬぎます。', 'I take off my shoes at the entrance.'),
    P+'13-locations-and-places-.にわ':       E('にわに 花が あります。', 'There are flowers in the garden.'),
    P+'13-locations-and-places-.高校':       E('高校に かよって います。', "I'm attending high school."),
    P+'13-locations-and-places-.会社':       E('父は 会社で はたらきます。', 'My father works at a company.'),
    P+'13-locations-and-places-.じむしょ':   E('じむしょは 二かいです。', "The office is on the 2nd floor."),
    P+'13-locations-and-places-.お店':       E('お店で 買いものを します。', 'I shop at the store.'),
    P+'13-locations-and-places-.やおや':     E('やおやで やさいを 買います。', 'I buy vegetables at the greengrocer.'),
    P+'13-locations-and-places-.ほんや':     E('ほんやで 本を 買いました。', 'I bought a book at the bookstore.'),
    P+'13-locations-and-places-.はなや':     E('はなやで 花を 買います。', 'I buy flowers at the florist.'),
    P+'13-locations-and-places-.にくや':     E('にくやで にくを 買います。', 'I buy meat at the butcher.'),
    P+'13-locations-and-places-.パンや':     E('パンやで パンを 買いました。', 'I bought bread at the bakery.'),
    P+'13-locations-and-places-.くうこう':   E('くうこうで ともだちを むかえます。', "I'll meet my friend at the airport."),
    P+'13-locations-and-places-.どうぶつえん': E('どうぶつえんで パンダを 見ました。', 'I saw a panda at the zoo.'),
    P+'13-locations-and-places-.びじゅつかん': E('びじゅつかんで えを 見ます。', 'I look at paintings at the art museum.'),
    P+'13-locations-and-places-.えいがかん': E('えいがかんで えいがを 見ます。', 'I watch movies at the theater.'),
    P+'13-locations-and-places-.ホテル':     E('ホテルに とまります。', "I'll stay at the hotel."),
    P+'13-locations-and-places-.りょかん':   E('りょかんで 一ぱく しました。', 'I stayed one night at a Japanese inn.'),
    P+'13-locations-and-places-.こうばん':   E('こうばんで みちを 聞きます。', 'I ask for directions at the police box.'),
    P+'13-locations-and-places-.こうさてん': E('こうさてんで まがります。', 'I turn at the intersection.'),
    P+'13-locations-and-places-.いりぐち':   E('いりぐちは あちらです。', 'The entrance is over there.'),
    P+'13-locations-and-places-.しょくどう': E('しょくどうで ひるごはんを 食べます。', 'I eat lunch in the cafeteria.'),
    P+'13-locations-and-places-.たてもの':   E('あの たてものは 大学です。', 'That building is a university.'),
    P+'13-locations-and-places-.ろうか':     E('ろうかで 走らないで ください。', "Don't run in the hallway."),
    P+'13-locations-and-places-.プール':     E('プールで およぎます。', 'I swim in the pool.'),
    P+'13-locations-and-places-.ポスト':     E('ポストに てがみを 入れます。', 'I put a letter in the mailbox.'),
    P+'13-locations-and-places-.道':         E('道を わたります。', 'I cross the road.'),
    P+'13-locations-and-places-.とおり':     E('この とおりは にぎやかです。', 'This street is lively.'),
    P+'13-locations-and-places-.かど':       E('かどを みぎに まがります。', 'Turn right at the corner.'),
    P+'13-locations-and-places-.はし':       E('はしを わたります。', 'I cross the bridge.'),
    P+'13-locations-and-places-.むら':       E('小さい むらに すんで います。', 'I live in a small village.'),
    P+'13-locations-and-places-.国':         E('わたしの 国は 大きいです。', 'My country is big.'),
    P+'13-locations-and-places-.前':         E('えきの 前で 会いましょう。', "Let's meet in front of the station."),
    P+'13-locations-and-places-.後ろ':       E('わたしの 後ろに 田中さんが います。', 'Tanaka-san is behind me.'),
    P+'13-locations-and-places-.左':         E('左に 学校が あります。', "The school is on the left."),
    P+'13-locations-and-places-.右':         E('右に スーパーが あります。', "There's a supermarket on the right."),
    P+'13-locations-and-places-.となり':     E('となりに 友だちが すんで います。', 'My friend lives next door.'),
    P+'13-locations-and-places-.よこ':       E('テーブルの よこに いすが あります。', "There's a chair next to the table."),
    P+'13-locations-and-places-.とおく':     E('とおくに 山が 見えます。', 'I can see mountains in the distance.'),
    P+'13-locations-and-places-.むこう':     E('むこうに 大きい ビルが あります。', "There's a big building over there."),
    P+'13-locations-and-places-.北':         E('北は さむいです。', 'The north is cold.'),
    P+'13-locations-and-places-.南':         E('南は あついです。', 'The south is hot.'),
    P+'13-locations-and-places-.東':         E('東に 山が あります。', "There are mountains to the east."),
    P+'13-locations-and-places-.西':         E('西に 海が あります。', "There's the sea to the west."),

    # 14. Nature tail
    P+'14-nature-and-weather.いけ':         E('こうえんに いけが あります。', "There's a pond in the park."),
    P+'14-nature-and-weather.みずうみ':     E('みずうみで およぎました。', 'I swam in the lake.'),
    P+'14-nature-and-weather.もり':         E('もりに 入ります。', 'I enter the forest.'),
    P+'14-nature-and-weather.くさ':         E('にわに くさが はえて います。', 'Grass is growing in the garden.'),
    P+'14-nature-and-weather.は':           E('木の はが おちました。', 'A tree leaf fell.'),
    P+'14-nature-and-weather.いし':         E('道に 大きい いしが あります。', "There's a big stone on the road."),
    P+'14-nature-and-weather.田':           E('田の 中で 米を つくります。', 'They grow rice in the rice field.'),
    P+'14-nature-and-weather.くも':         E('そらに くもが あります。', "There are clouds in the sky."),
    P+'14-nature-and-weather.たいよう':     E('たいようが 出ました。', 'The sun came out.'),
    P+'14-nature-and-weather.かぜ':         E('今日は かぜが つよいです。', 'The wind is strong today.'),
    P+'14-nature-and-weather.はれ':         E('今日は はれです。', "It's clear today."),
    P+'14-nature-and-weather.くもり':       E('あした くもりです。', 'Tomorrow will be cloudy.'),
    P+'14-nature-and-weather.なつ':         E('なつは あついです。', 'Summer is hot.'),
    P+'14-nature-and-weather.ふゆ':         E('ふゆは ゆきが ふります。', 'It snows in winter.'),
    P+'14-nature-and-weather.火':           E('火に 気を つけて ください。', 'Please be careful with fire.'),
    P+'14-nature-and-weather.水':           E('水を 飲みます。', 'I drink water.'),
    P+'14-nature-and-weather.おゆ':         E('おゆを わかします。', 'I boil water.'),

    # 15. Animals tail
    P+'15-animals.にわとり':                E('にわとりが たまごを うみます。', 'Hens lay eggs.'),
    P+'15-animals.ぞう':                    E('ぞうは とても 大きいです。', 'Elephants are very big.'),
    P+'15-animals.むし':                    E('にわに むしが います。', "There are insects in the garden."),

    # 16. Food/drink general tail
    P+'16-food-and-drink-genera.たべもの':  E('日本の たべものが すきです。', 'I like Japanese food.'),
    P+'16-food-and-drink-genera.のみもの':  E('のみものは 何が いいですか。', 'What would you like to drink?'),
    P+'16-food-and-drink-genera.ゆうはん':  E('ゆうはんは すしを 食べました。', 'I ate sushi for dinner.'),
    P+'16-food-and-drink-genera.しょくじ':  E('しょくじの じかんです。', "It's mealtime."),
    P+'16-food-and-drink-genera.おべんとう': E('おべんとうを もって 行きます。', "I bring a packed lunch."),

    # 17. Food items tail
    P+'17-food-items.ぎゅうにく':          E('ぎゅうにくは 高いです。', 'Beef is expensive.'),
    P+'17-food-items.ぶたにく':            E('ぶたにくを 食べます。', 'I eat pork.'),
    P+'17-food-items.とりにく':            E('とりにくは あっさりして います。', 'Chicken is light/mild.'),
    P+'17-food-items.さかな':              E('さかなを 食べます。', 'I eat fish.'),
    P+'17-food-items.いちご':              E('いちごは あまいです。', 'Strawberries are sweet.'),
    P+'17-food-items.ぶどう':              E('ぶどうを 買いました。', 'I bought grapes.'),
    P+'17-food-items.すいか':              E('夏は すいかが おいしいです。', 'Watermelon is tasty in summer.'),
    P+'17-food-items.レモン':              E('レモンは すっぱいです。', 'Lemons are sour.'),
    P+'17-food-items.だいこん':            E('だいこんで サラダを つくります。', 'I make salad with daikon.'),
    P+'17-food-items.にんじん':            E('にんじんは あかい やさいです。', 'Carrots are red vegetables.'),
    P+'17-food-items.たまねぎ':            E('たまねぎを 切ります。', 'I cut onions.'),
    P+'17-food-items.じゃがいも':          E('じゃがいもを 入れて ください。', 'Please add potatoes.'),
    P+'17-food-items.トマト':              E('トマトは あかい くだものです。', 'Tomatoes are red.'),
    P+'17-food-items.きゅうり':            E('きゅうりを サラダに 入れます。', 'I put cucumber in the salad.'),
    P+'17-food-items.キャベツ':            E('キャベツを 切ります。', 'I cut cabbage.'),
    P+'17-food-items.こめ':                E('こめは 日本の しゅしょくです。', 'Rice is the staple food in Japan.'),
    P+'17-food-items.しお':                E('しおを 入れて ください。', 'Please add salt.'),
    P+'17-food-items.さとう':              E('コーヒーに さとうを 入れます。', 'I put sugar in my coffee.'),
    P+'17-food-items.しょうゆ':            E('すしに しょうゆを つけます。', 'I dip sushi in soy sauce.'),
    P+'17-food-items.みそ':                E('みそしるが すきです。', 'I like miso soup.'),
    P+'17-food-items.カレー':              E('夕ごはんは カレーです。', 'Dinner is curry.'),
    P+'17-food-items.うどん':              E('うどんを 食べます。', 'I eat udon.'),
    P+'17-food-items.そば':                E('おみそかに そばを 食べます。', 'I eat soba on New Year\'s Eve.'),
    P+'17-food-items.ハンバーガー':        E('ハンバーガーを 二つ ください。', 'Two hamburgers please.'),
    P+'17-food-items.サンドイッチ':        E('サンドイッチを 食べました。', 'I ate a sandwich.'),
    P+'17-food-items.サラダ':              E('サラダが すきです。', 'I like salad.'),
    P+'17-food-items.スープ':              E('スープを 飲みます。', 'I have soup.'),
    P+'17-food-items.チョコレート':        E('チョコレートが すきです。', 'I like chocolate.'),

    # 18. Drinks tail
    P+'18-drinks.おゆ':                    E('おゆを ください。', 'Hot water please.'),
    P+'18-drinks.こうちゃ':                E('こうちゃを 飲みます。', 'I drink black tea.'),

    # 19. Tableware - all
    P+'19-tableware-and-cooking.さら':     E('さらに りょうりを のせます。', 'I put the food on a plate.'),
    P+'19-tableware-and-cooking.おさら':   E('おさらを あらいます。', 'I wash the plates.'),
    P+'19-tableware-and-cooking.ちゃわん': E('ちゃわんに ごはんを 入れます。', 'I put rice in the bowl.'),
    P+'19-tableware-and-cooking.おわん':   E('おわんで みそしるを 飲みます。', 'I drink miso soup from a bowl.'),
    P+'19-tableware-and-cooking.はし':     E('はしで ごはんを 食べます。', 'I eat rice with chopsticks.'),
    P+'19-tableware-and-cooking.スプーン': E('スプーンで スープを 飲みます。', 'I eat soup with a spoon.'),
    P+'19-tableware-and-cooking.フォーク': E('フォークで サラダを 食べます。', 'I eat salad with a fork.'),
    P+'19-tableware-and-cooking.ナイフ':   E('ナイフで パンを 切ります。', 'I cut bread with a knife.'),
    P+'19-tableware-and-cooking.コップ':   E('コップに 水を 入れます。', 'I put water in the glass.'),
    P+'19-tableware-and-cooking.カップ':   E('カップで コーヒーを 飲みます。', 'I drink coffee from a cup.'),
    P+'19-tableware-and-cooking.れいぞうこ': E('れいぞうこに ぎゅうにゅうが あります。', "There's milk in the fridge."),
    P+'19-tableware-and-cooking.なべ':     E('なべで スープを つくります。', 'I make soup in the pot.'),

    # 20. Colors tail
    P+'20-colors.いろ':                    E('すきな いろは あおです。', 'My favorite color is blue.'),
    P+'20-colors.ピンク':                  E('ピンクの 花が きれいです。', 'The pink flowers are pretty.'),

    # 21. Clothing tail
    P+'21-clothing-and-accessor.ようふく': E('ようふくを 買いました。', 'I bought Western clothes.'),
    P+'21-clothing-and-accessor.きもの':   E('お正月に きものを きます。', "I wear a kimono on New Year's."),
    P+'21-clothing-and-accessor.うわぎ':   E('うわぎを ぬぎます。', 'I take off my jacket.'),
    P+'21-clothing-and-accessor.コート':   E('冬に コートを きます。', 'I wear a coat in winter.'),
    P+'21-clothing-and-accessor.セーター': E('さむい とき、セーターを きます。', 'I wear a sweater when cold.'),
    P+'21-clothing-and-accessor.Tシャツ':  E('夏に Tシャツを きます。', 'I wear T-shirts in summer.'),
    P+'21-clothing-and-accessor.ワイシャツ': E('しごとには ワイシャツを きます。', 'I wear a dress shirt to work.'),
    P+'21-clothing-and-accessor.ネクタイ': E('ネクタイを しめます。', 'I tie my necktie.'),
}


def main() -> int:
    vpath = ROOT / 'data' / 'vocab.json'
    data = json.loads(vpath.read_text(encoding='utf-8'))
    by_id = {v['id']: v for v in data['entries']}
    added, skipped, not_found = [], [], []
    for vid, new_ex in ADDITIONS.items():
        v = by_id.get(vid)
        if v is None:
            not_found.append(vid); continue
        existing = v.get('examples') or []
        if any(e.get('ja') == new_ex['ja'] for e in existing):
            skipped.append(vid); continue
        existing.append(new_ex)
        v['examples'] = existing
        added.append(vid)
    if added:
        vpath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
    print(f'Added inline example to {len(added)} vocab entries.')
    if skipped: print(f'Skipped (already had it): {len(skipped)}')
    if not_found:
        print(f'NOT FOUND ({len(not_found)}):')
        for v in sorted(not_found):
            print(f'  {v}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
