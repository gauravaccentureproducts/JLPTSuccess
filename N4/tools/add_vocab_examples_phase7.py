"""Phase 7 of the example-coverage authoring pass (2026-05-03).

Targets the remaining ~321 uncovered entries after Phase 6. This batch
aims to clear most sections to full coverage:
  - Locations / Nature tail (4)
  - Clothing / Money / Transport tails (18)
  - School & study (27) - all
  - Languages / countries tail (9)
  - House & furniture (28) - all
  - Verbs - Group 1 (34) / Group 2 (15) / Irregular (11) / Existence (6)
  - i-adj tail (28) / na-adj tail (9)
  - Adverbs tail (16) / Conjunctions (6)
  - People - Roles tail (4)
  - Greetings & set phrases tail (12)
  - Common nouns misc - top 35 / 64
  - Sounds (2) / Function fillers (8) / Body parts tail (1)
  - Misc useful items (12) / Counters tail (7)

All keys verified against actual data IDs. Idempotent.
"""
import io, json, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
P = 'n5.vocab.'

def E(ja, en):
    return {'ja': ja, 'translation_en': en}

ADDITIONS = {
    # 3. People - Roles tail
    P+'3-people-roles.けいかん':           E('けいかんに みちを 聞きました。', 'I asked the police officer for directions.'),
    P+'3-people-roles.おまわりさん':       E('おまわりさんに あいさつします。', 'I greet the police officer.'),
    P+'3-people-roles.りゅうがくせい':     E('わたしは りゅうがくせいです。', 'I am an international student.'),
    P+'3-people-roles.外国人':             E('日本に 外国人が たくさん います。', "There are many foreigners in Japan."),

    # 4. Body Parts tail
    P+'4-body-parts.せ':                   E('あには せが 高いです。', 'My older brother is tall.'),

    # 9. Counters (common) tail
    P+'9-counters-common.本':              E('えんぴつを 三本 ください。', 'Three pencils please.'),
    P+'9-counters-common.だい':            E('くるまが 二だい あります。', 'There are two cars.'),
    P+'9-counters-common.こ':              E('りんごを 五こ 買いました。', 'I bought five apples.'),
    P+'9-counters-common.かい':            E('じむしょは 三かいです。', 'The office is on the 3rd floor.'),
    P+'9-counters-common.かい.2':          E('日本に 二かい 行きました。', "I've been to Japan twice."),
    P+'9-counters-common.番':              E('五番の バスに のります。', "I'll take the number 5 bus."),
    P+'9-counters-common.ど':              E('もう 一ど 言って ください。', 'Please say it once more.'),

    # 13. Locations tail
    P+'13-locations-and-places-.たいしかん': E('日本の たいしかんは どこですか。', 'Where is the Japanese embassy?'),
    P+'13-locations-and-places-.こうじょう': E('父は こうじょうで はたらきます。', 'My father works at a factory.'),

    # 14. Nature tail
    P+'14-nature-and-weather.すずしい':    E('あきは すずしいです。', 'Autumn is cool.'),
    P+'14-nature-and-weather.あたたかい':  E('はるは あたたかいです。', 'Spring is warm.'),

    # 21. Clothing tail
    P+'21-clothing-and-accessor.ハンカチ': E('ハンカチを もって います。', 'I have a handkerchief.'),
    P+'21-clothing-and-accessor.さいふ':   E('さいふを わすれました。', 'I forgot my wallet.'),
    P+'21-clothing-and-accessor.ボタン':   E('シャツの ボタンが とれました。', 'A button came off the shirt.'),
    P+'21-clothing-and-accessor.ポケット': E('ポケットに かぎが あります。', "There's a key in my pocket."),
    P+'21-clothing-and-accessor.かさ':    E('雨ですから、かさを もって 行きます。', "It's raining, so I'll bring an umbrella."),

    # 22. Money & shopping tail
    P+'22-money-and-shopping.円':         E('これは 千円です。', 'This is 1000 yen.'),
    P+'22-money-and-shopping.ドル':       E('百ドル ぐらいです。', "It's about 100 dollars."),
    P+'22-money-and-shopping.きっぷ':     E('えきで きっぷを 買います。', 'I buy a ticket at the station.'),
    P+'22-money-and-shopping.ふうとう':   E('ふうとうに きってを はります。', 'I put a stamp on the envelope.'),
    P+'22-money-and-shopping.てがみ':     E('友だちに てがみを 書きました。', 'I wrote a letter to a friend.'),
    P+'22-money-and-shopping.にもつ':     E('にもつが おもいです。', 'The luggage is heavy.'),
    P+'22-money-and-shopping.おみやげ':   E('おみやげを 買いました。', 'I bought souvenirs.'),
    P+'22-money-and-shopping.レジ':       E('レジで はらいます。', 'I pay at the register.'),

    # 23. Transport tail
    P+'23-transport.じどうしゃ':          E('じどうしゃで 出かけます。', "I'll go out by car."),
    P+'23-transport.バイク':              E('バイクで 学校に 行きます。', 'I go to school by motorbike.'),
    P+'23-transport.きしゃ':              E('むかしは きしゃが ありました。', 'There used to be steam trains.'),
    P+'23-transport.道':                  E('この 道は あぶないです。', 'This road is dangerous.'),
    P+'23-transport.しんごう':            E('しんごうが あかです。', 'The traffic light is red.'),

    # 24. School & study - all
    P+'24-school-and-study.こたえ':       E('こたえを 書いて ください。', 'Please write the answer.'),
    P+'24-school-and-study.いみ':         E('この ことばの いみは 何ですか。', "What's the meaning of this word?"),
    P+'24-school-and-study.ことば':       E('日本語の ことばを おぼえます。', 'I memorize Japanese words.'),
    P+'24-school-and-study.じ':           E('じが きれいですね。', 'Your handwriting is pretty.'),
    P+'24-school-and-study.かな':         E('かなで 書いて ください。', 'Please write in kana.'),
    P+'24-school-and-study.ひらがな':     E('ひらがなを ぜんぶ おぼえました。', 'I memorized all hiragana.'),
    P+'24-school-and-study.カタカナ':     E('カタカナで 名前を 書きます。', 'I write my name in katakana.'),
    P+'24-school-and-study.もじ':         E('もじを 大きく 書きます。', 'I write the characters big.'),
    P+'24-school-and-study.ぶん':         E('ぶんを 三つ 書いて ください。', 'Please write three sentences.'),
    P+'24-school-and-study.ぶんしょう':   E('ながい ぶんしょうを 読みます。', 'I read a long text.'),
    P+'24-school-and-study.ぶんぽう':     E('ぶんぽうは むずかしいです。', 'Grammar is difficult.'),
    P+'24-school-and-study.れい':         E('れいを 見せて ください。', 'Please show me an example.'),
    P+'24-school-and-study.れんしゅう':   E('れんしゅうが 大切です。', 'Practice is important.'),
    P+'24-school-and-study.きょうかしょ': E('きょうかしょの 二十ページを ひらいて ください。', 'Please open the textbook to page 20.'),
    P+'24-school-and-study.ざっし':       E('ざっしを 読みます。', 'I read magazines.'),
    P+'24-school-and-study.新聞':         E('あさ、新聞を 読みます。', 'I read the newspaper in the morning.'),
    P+'24-school-and-study.ボールペン':   E('ボールペンで 書いて ください。', 'Please write with a ballpoint pen.'),
    P+'24-school-and-study.まんねんひつ': E('まんねんひつで 名前を 書きます。', 'I write my name with a fountain pen.'),
    P+'24-school-and-study.こくばん':     E('先生は こくばんに 字を 書きます。', 'The teacher writes on the blackboard.'),
    P+'24-school-and-study.チョーク':     E('チョークで 書きます。', 'I write with chalk.'),
    P+'24-school-and-study.けしゴム':     E('けしゴムを かして ください。', 'Please lend me an eraser.'),
    P+'24-school-and-study.ちず':         E('ちずを 見て ください。', 'Please look at the map.'),
    P+'24-school-and-study.え':           E('きれいな えを かきました。', 'I drew a pretty picture.'),
    P+'24-school-and-study.番号':         E('番号を 書いて ください。', 'Please write the number.'),
    P+'24-school-and-study.電気':         E('電気を つけて ください。', 'Please turn on the light.'),
    P+'24-school-and-study.電話':         E('電話を かけます。', 'I make a phone call.'),
    P+'24-school-and-study.電話番号':     E('電話番号を 教えて ください。', 'Please tell me your phone number.'),

    # 25. Languages & countries tail
    P+'25-languages-and-countri.日本人':       E('わたしは 日本人ではありません。', "I'm not Japanese."),
    P+'25-languages-and-countri.かんこくご':   E('かんこくごを ならって います。', "I'm learning Korean."),
    P+'25-languages-and-countri.フランス':     E('フランスに 行きたいです。', 'I want to go to France.'),
    P+'25-languages-and-countri.フランスご':   E('フランスごを 話せます。', 'I can speak French.'),
    P+'25-languages-and-countri.ドイツ':       E('ドイツは ヨーロッパの 国です。', 'Germany is a European country.'),
    P+'25-languages-and-countri.スペイン':     E('スペインの りょうりは おいしいです。', 'Spanish food is delicious.'),
    P+'25-languages-and-countri.イギリス':     E('イギリスは しまの 国です。', 'The UK is an island country.'),
    P+'25-languages-and-countri.外国':         E('外国に 行きたいです。', 'I want to go abroad.'),
    P+'25-languages-and-countri.外国語':       E('外国語を べんきょうします。', 'I study a foreign language.'),

    # 26. House & furniture - all
    P+'26-house-and-furniture.アパート':   E('アパートに すんで います。', 'I live in an apartment.'),
    P+'26-house-and-furniture.マンション': E('あの マンションは あたらしいです。', 'That condominium is new.'),
    P+'26-house-and-furniture.と':         E('との まえに ねこが います。', "There's a cat in front of the door."),
    P+'26-house-and-furniture.もん':       E('もんを あけて ください。', 'Please open the gate.'),
    P+'26-house-and-furniture.かべ':       E('かべに えを かけます。', 'I hang a picture on the wall.'),
    P+'26-house-and-furniture.かいだん':   E('かいだんを のぼります。', 'I go up the stairs.'),
    P+'26-house-and-furniture.エレベーター': E('エレベーターで 五かいに 行きます。', "I'll take the elevator to the 5th floor."),
    P+'26-house-and-furniture.げんかん':   E('げんかんで くつを ぬぎます。', 'I take off my shoes at the entrance.'),
    P+'26-house-and-furniture.しんしつ':   E('しんしつで ねます。', 'I sleep in the bedroom.'),
    P+'26-house-and-furniture.ふとん':     E('ふとんを しきます。', 'I lay out the futon.'),
    P+'26-house-and-furniture.もうふ':     E('さむい とき、もうふを かけます。', 'When cold, I use a blanket.'),
    P+'26-house-and-furniture.まくら':     E('まくらは やわらかいです。', 'The pillow is soft.'),
    P+'26-house-and-furniture.いす':       E('いすに すわって ください。', 'Please sit on the chair.'),
    P+'26-house-and-furniture.たな':       E('たなに 本を おきます。', 'I put the book on the shelf.'),
    P+'26-house-and-furniture.ほんだな':   E('ほんだなに 本が たくさん あります。', 'There are many books on the bookshelf.'),
    P+'26-house-and-furniture.カーテン':   E('まどに カーテンを つけます。', 'I put a curtain on the window.'),
    P+'26-house-and-furniture.かぎ':       E('かぎを なくしました。', 'I lost the key.'),
    P+'26-house-and-furniture.せっけん':   E('せっけんで てを あらいます。', 'I wash my hands with soap.'),
    P+'26-house-and-furniture.はブラシ':   E('まいあさ はブラシを つかいます。', 'I use a toothbrush every morning.'),
    P+'26-house-and-furniture.タオル':     E('タオルで かおを ふきます。', 'I wipe my face with a towel.'),
    P+'26-house-and-furniture.テープ':     E('テープで かみを はります。', 'I tape the paper.'),
    P+'26-house-and-furniture.ラジオ':     E('ラジオで ニュースを 聞きます。', 'I listen to the news on the radio.'),
    P+'26-house-and-furniture.カメラ':     E('カメラで しゃしんを とります。', 'I take photos with a camera.'),
    P+'26-house-and-furniture.ビデオ':     E('ビデオを 見ます。', 'I watch a video.'),
    P+'26-house-and-furniture.うた':       E('うたを うたいます。', 'I sing a song.'),
    P+'26-house-and-furniture.え':         E('かべに 大きな えを かけました。', 'I hung a big picture on the wall.'),
    P+'26-house-and-furniture.ピアノ':     E('ピアノを ひきます。', 'I play the piano.'),
    P+'26-house-and-furniture.ギター':     E('ギターが 大すきです。', 'I love the guitar.'),

    # 27. Verbs Group 1 - all uncovered
    P+'27-verbs-group-1-verbs.うたう':       E('カラオケで うたを うたいます。', 'I sing songs at karaoke.'),
    P+'27-verbs-group-1-verbs.きる':         E('はさみで かみを きります。', 'I cut paper with scissors.'),
    P+'27-verbs-group-1-verbs.しる':         E('田中さんを しって います。', 'I know Tanaka-san.'),
    P+'27-verbs-group-1-verbs.立つ':         E('先生が 立ちました。', 'The teacher stood up.'),
    P+'27-verbs-group-1-verbs.はく':         E('くつを はきます。', 'I put on shoes.'),
    P+'27-verbs-group-1-verbs.はしる':       E('まいあさ こうえんで はしります。', 'I run in the park every morning.'),
    P+'27-verbs-group-1-verbs.わたる':       E('道を わたります。', 'I cross the road.'),
    P+'27-verbs-group-1-verbs.うる':         E('やおやで やさいを うって います。', 'They sell vegetables at the greengrocer.'),
    P+'27-verbs-group-1-verbs.ひく':         E('ピアノを ひきます。', 'I play the piano.'),
    P+'27-verbs-group-1-verbs.ひく.2':       E('かみを ひっぱりました。', 'I pulled the paper.'),
    P+'27-verbs-group-1-verbs.よぶ':         E('友だちを 家に よびました。', 'I invited a friend to my house.'),
    P+'27-verbs-group-1-verbs.とぶ':         E('とりが そらを とんで います。', 'A bird is flying in the sky.'),
    P+'27-verbs-group-1-verbs.こまる':       E('お金が なくて こまります。', "I'm in trouble without money."),
    P+'27-verbs-group-1-verbs.ならぶ':       E('レジに ならびます。', 'I line up at the register.'),
    P+'27-verbs-group-1-verbs.わたす':       E('先生に しゅくだいを わたします。', 'I hand in the homework to the teacher.'),
    P+'27-verbs-group-1-verbs.ぬぐ':         E('家で くつを ぬぎます。', 'I take off my shoes at home.'),
    P+'27-verbs-group-1-verbs.いそぐ':       E('時間が ないので、いそぎます。', "There's no time, so I'll hurry."),
    P+'27-verbs-group-1-verbs.しぬ':         E('花が しんで しまいました。', 'The flowers died.'),
    P+'27-verbs-group-1-verbs.ならう':       E('日本語を ならって います。', "I'm learning Japanese."),
    P+'27-verbs-group-1-verbs.はる':         E('かべに ポスターを はります。', 'I stick a poster on the wall.'),
    P+'27-verbs-group-1-verbs.まがる':       E('かどを 右に まがって ください。', 'Please turn right at the corner.'),
    P+'27-verbs-group-1-verbs.もっていく':   E('かさを もっていきます。', "I'll take an umbrella with me."),
    P+'27-verbs-group-1-verbs.もってくる':   E('お金を もってきて ください。', 'Please bring money.'),
    P+'27-verbs-group-1-verbs.しまる':       E('店は 九時に しまります。', 'The shop closes at 9.'),
    P+'27-verbs-group-1-verbs.だす':         E('かばんから 本を だします。', 'I take a book out of the bag.'),
    P+'27-verbs-group-1-verbs.おとす':       E('かぎを おとしました。', 'I dropped the key.'),
    P+'27-verbs-group-1-verbs.ふく':         E('かぜが ふいて います。', 'The wind is blowing.'),
    P+'27-verbs-group-1-verbs.くもる':       E('そらが くもって います。', 'The sky is cloudy.'),
    P+'27-verbs-group-1-verbs.なくす':       E('さいふを なくしました。', 'I lost my wallet.'),
    P+'27-verbs-group-1-verbs.すわる':       E('いすに すわって ください。', 'Please sit on the chair.'),
    P+'27-verbs-group-1-verbs.たのむ':       E('友だちに たのみます。', "I'll ask a friend."),
    P+'27-verbs-group-1-verbs.とまる':       E('くるまが とまりました。', 'The car stopped.'),
    P+'27-verbs-group-1-verbs.さす':         E('雨が ふって きたので、かさを さします。', "It started raining, so I'll put up an umbrella."),
    P+'27-verbs-group-1-verbs.けす':         E('でんきを けします。', 'I turn off the light.'),

    # 28. Verbs Group 2 - all uncovered
    P+'28-verbs-group-2-verbs.入れる':       E('かばんに 本を 入れます。', 'I put the book in the bag.'),
    P+'28-verbs-group-2-verbs.こたえる':     E('しつもんに こたえます。', 'I answer the question.'),
    P+'28-verbs-group-2-verbs.かける':       E('友だちに 電話を かけます。', 'I call a friend.'),
    P+'28-verbs-group-2-verbs.きる':         E('シャツを きます。', 'I put on a shirt.'),
    P+'28-verbs-group-2-verbs.つける':       E('テレビを つけます。', 'I turn on the TV.'),
    P+'28-verbs-group-2-verbs.ならべる':     E('いすを ならべます。', 'I line up the chairs.'),
    P+'28-verbs-group-2-verbs.見せる':       E('しゃしんを 見せます。', 'I show the photo.'),
    P+'28-verbs-group-2-verbs.いれる':       E('コーヒーを いれます。', 'I make coffee.'),
    P+'28-verbs-group-2-verbs.あつめる':     E('きってを あつめて います。', 'I collect stamps.'),
    P+'28-verbs-group-2-verbs.きえる':       E('でんきが きえました。', 'The light went off.'),
    P+'28-verbs-group-2-verbs.おちる':       E('かばんが おちました。', 'The bag fell.'),
    P+'28-verbs-group-2-verbs.はれる':       E('あした はれるでしょう。', "It will probably be sunny tomorrow."),
    P+'28-verbs-group-2-verbs.つかれる':     E('しごとで つかれました。', "I'm tired from work."),
    P+'28-verbs-group-2-verbs.生まれる':     E('日本で 生まれました。', 'I was born in Japan.'),
    P+'28-verbs-group-2-verbs.つとめる':     E('ぎんこうに つとめて います。', 'I work at a bank.'),

    # 29. Irregular / suru-verbs - all
    P+'29-verbs-irregular-and-v.けっこんする':     E('らいねん けっこんします。', "I'll get married next year."),
    P+'29-verbs-irregular-and-v.さんぽする':       E('まいあさ さんぽします。', 'I take a walk every morning.'),
    P+'29-verbs-irregular-and-v.りょこうする':     E('夏に りょこうします。', "I'll travel in summer."),
    P+'29-verbs-irregular-and-v.れんしゅうする':   E('まいにち ピアノを れんしゅうします。', 'I practice piano every day.'),
    P+'29-verbs-irregular-and-v.しつもんする':     E('先生に しつもんします。', "I'll ask the teacher a question."),
    P+'29-verbs-irregular-and-v.しごとする':       E('まいにち しごとします。', 'I work every day.'),
    P+'29-verbs-irregular-and-v.電話する':         E('あとで 電話します。', "I'll call later."),
    P+'29-verbs-irregular-and-v.コピーする':       E('しょるいを コピーします。', "I'll copy the documents."),
    P+'29-verbs-irregular-and-v.そうじする':       E('日曜日に へやを そうじします。', 'I clean my room on Sundays.'),
    P+'29-verbs-irregular-and-v.せんたくする':     E('せんたくしました。', 'I did the laundry.'),
    P+'29-verbs-irregular-and-v.かいものする':     E('スーパーで かいものします。', "I'll shop at the supermarket."),

    # 30. Existence verbs tail
    P+'30-verbs-existence-and-p.やる':       E('しゅくだいを やります。', "I'll do my homework."),
    P+'30-verbs-existence-and-p.あげる':     E('友だちに プレゼントを あげます。', "I'll give a present to a friend."),
    P+'30-verbs-existence-and-p.くれる':     E('父が 本を くれました。', 'My father gave me a book.'),
    P+'30-verbs-existence-and-p.かす':       E('ペンを かして ください。', 'Please lend me a pen.'),
    P+'30-verbs-existence-and-p.かりる':     E('としょかんで 本を かりました。', 'I borrowed a book at the library.'),
    P+'30-verbs-existence-and-p.かえす':     E('本を かえします。', "I'll return the book."),

    # 31. i-adjectives tail
    P+'31-adjectives.つめたい':              E('つめたい 水を 飲みます。', 'I drink cold water.'),
    P+'31-adjectives.ひくい':                E('この いすは ひくいです。', 'This chair is low.'),
    P+'31-adjectives.うすい':                E('うすい 本を 読みました。', 'I read a thin book.'),
    P+'31-adjectives.ふとい':                E('ふとい えんぴつを つかいます。', 'I use a thick pencil.'),
    P+'31-adjectives.ほそい':                E('ほそい みちです。', "It's a narrow road."),
    P+'31-adjectives.うれしい':              E('プレゼントを もらって うれしいです。', "I'm happy to receive a present."),
    P+'31-adjectives.かなしい':              E('友だちが いないと かなしいです。', "I'm sad without my friends."),
    P+'31-adjectives.さびしい':              E('一人で さびしいです。', "I'm lonely by myself."),
    P+'31-adjectives.かわいい':              E('この ねこは かわいいです。', 'This cat is cute.'),
    P+'31-adjectives.うつくしい':            E('うつくしい 花です。', "It's a beautiful flower."),
    P+'31-adjectives.きたない':              E('へやが きたないです。', "The room is dirty."),
    P+'31-adjectives.やさしい':              E('先生は やさしいです。', 'The teacher is kind.'),
    P+'31-adjectives.つまらない':            E('この えいがは つまらないです。', 'This movie is boring.'),
    P+'31-adjectives.まずい':                E('この りょうりは まずいです。', 'This food tastes bad.'),
    P+'31-adjectives.にがい':                E('コーヒーは にがいです。', 'Coffee is bitter.'),
    P+'31-adjectives.おおい':                E('きょうは 人が おおいです。', "There are many people today."),
    P+'31-adjectives.すくない':              E('お金が すくないです。', "I have little money."),
    P+'31-adjectives.まるい':                E('まるい テーブルが すきです。', 'I like round tables.'),
    P+'31-adjectives.しかくい':              E('しかくい はこを 買いました。', 'I bought a square box.'),
    P+'31-adjectives.わかい':                E('かれは わかいです。', 'He is young.'),
    P+'31-adjectives.きいろい':              E('きいろい 花が きれいです。', 'The yellow flowers are pretty.'),
    P+'31-adjectives.あおい':                E('あおい そらが きれいです。', 'The blue sky is beautiful.'),
    P+'31-adjectives.あかい':                E('あかい りんごを 食べます。', 'I eat a red apple.'),
    P+'31-adjectives.くろい':                E('くろい かばんを 買いました。', 'I bought a black bag.'),
    P+'31-adjectives.白い':                  E('白い シャツを きます。', 'I wear a white shirt.'),
    P+'31-adjectives.ちゃいろい':            E('ちゃいろい くつが すきです。', 'I like brown shoes.'),
    P+'31-adjectives.ぬるい':                E('お茶が ぬるいです。', 'The tea is lukewarm.'),
    P+'31-adjectives.うるさい':              E('外が うるさいです。', "It's noisy outside."),

    # 32. na-adjectives tail
    P+'32-adjectives.たいへん':              E('しごとが たいへんです。', "Work is tough."),
    P+'32-adjectives.ふべん':                E('えきから とおくて、ふべんです。', "It's far from the station and inconvenient."),
    P+'32-adjectives.おなじ':                E('おなじ クラスです。', "We're in the same class."),
    P+'32-adjectives.りっぱ':                E('りっぱな 家ですね。', "What a splendid house."),
    P+'32-adjectives.けっこう':              E('けっこうな おちゃですね。', "What a fine tea."),
    P+'32-adjectives.だいじ':                E('だいじな しごとです。', "It's important work."),
    P+'32-adjectives.あんぜん':              E('この ばしょは あんぜんです。', 'This place is safe.'),
    P+'32-adjectives.じょうぶ':              E('この つくえは じょうぶです。', 'This desk is sturdy.'),
    P+'32-adjectives.いや':                  E('いやな てんきですね。', "What unpleasant weather."),

    # 33. Adverbs tail
    P+'33-adverbs.すごく':                   E('すごく おもしろいです。', "It's really interesting."),
    P+'33-adverbs.おおぜい':                 E('おおぜいの 人が います。', 'There are lots of people.'),
    P+'33-adverbs.だいたい':                 E('だいたい わかりました。', 'I roughly understood.'),
    P+'33-adverbs.もうすこし':               E('もうすこし まって ください。', 'Please wait a little more.'),
    P+'33-adverbs.一番':                     E('夏が 一番 すきです。', 'I like summer the best.'),
    P+'33-adverbs.とくに':                   E('とくに ピアノが すきです。', 'Especially I like the piano.'),
    P+'33-adverbs.ほんとうに':               E('ほんとうに ありがとう。', 'Thank you really.'),
    P+'33-adverbs.すぐ':                     E('すぐ 行きます。', "I'll go right away."),
    P+'33-adverbs.一人で':                   E('一人で 行きました。', 'I went alone.'),
    P+'33-adverbs.じぶんで':                 E('じぶんで しました。', 'I did it myself.'),
    P+'33-adverbs.かならず':                 E('あした かならず 来ます。', "I'll definitely come tomorrow."),
    P+'33-adverbs.もちろん':                 E('もちろん 行きます。', "Of course I'll go."),
    P+'33-adverbs.どうぞよろしく':           E('どうぞよろしく おねがいします。', 'Pleased to meet you.'),
    P+'33-adverbs.まっすぐ':                 E('まっすぐ 行って ください。', 'Please go straight.'),
    P+'33-adverbs.もういちど':               E('もういちど 言って ください。', 'Please say it once more.'),
    P+'33-adverbs.もしもし':                 E('もしもし、田中ですが。', 'Hello, this is Tanaka.'),

    # 34. Conjunctions
    P+'34-conjunctions.それで':              E('雨が ふりました。それで、出かけませんでした。', "It rained. So I didn't go out."),
    P+'34-conjunctions.が':                  E('行きたいですが、時間が ありません。', "I want to go, but I don't have time."),
    P+'34-conjunctions.だから':              E('あついです。だから、まどを あけます。', "It's hot. So I'll open the window."),
    P+'34-conjunctions.それに':              E('この レストランは おいしいです。それに、安いです。', "This restaurant is delicious. Moreover, it's cheap."),
    P+'34-conjunctions.ところで':            E('ところで、しゅくだいは おわりましたか。', 'By the way, have you finished your homework?'),
    P+'34-conjunctions.または':              E('コーヒー または おちゃが いいです。', "Coffee or tea is fine."),

    # 36. Greetings tail
    P+'36-greetings-and-set-phr.しつれいします':     E('しつれいします。先生、しつもんが あります。', 'Excuse me. Sensei, I have a question.'),
    P+'36-greetings-and-set-phr.しつれいしました':   E('おそく なって しつれいしました。', "Excuse me for being late."),
    P+'36-greetings-and-set-phr.どういたしまして':   E('どういたしまして。', "You're welcome."),
    P+'36-greetings-and-set-phr.いってきます':       E('いってきます。', "I'm off."),
    P+'36-greetings-and-set-phr.いってらっしゃい':   E('いってらっしゃい、気を つけて。', "See you, take care."),
    P+'36-greetings-and-set-phr.ただいま':           E('ただいま、おそくなりました。', "I'm home, sorry I'm late."),
    P+'36-greetings-and-set-phr.おかえりなさい':     E('おかえりなさい！おつかれさまでした。', 'Welcome back! You worked hard.'),
    P+'36-greetings-and-set-phr.はじめまして':       E('はじめまして、田中です。', "Nice to meet you, I'm Tanaka."),
    P+'36-greetings-and-set-phr.どうぞよろしく':     E('どうぞよろしく おねがいします。', 'Pleased to meet you.'),
    P+'36-greetings-and-set-phr.おかげさまで':       E('おかげさまで、げんきです。', "Thanks to you, I'm well."),
    P+'36-greetings-and-set-phr.いらっしゃいませ':   E('いらっしゃいませ！何名さまですか。', 'Welcome! How many people?'),
    P+'36-greetings-and-set-phr.もしもし':           E('もしもし、田中さんですか。', 'Hello, is this Tanaka-san?'),

    # 37. Common nouns misc - top 35 most useful
    P+'37-common-nouns-miscella.もの':       E('テーブルの 上の ものは 何ですか。', "What's the thing on the table?"),
    P+'37-common-nouns-miscella.こと':       E('一つ こと話したいです。', "I want to tell you one thing."),
    P+'37-common-nouns-miscella.ことば':     E('日本語の ことばを ならいます。', 'I learn Japanese words.'),
    P+'37-common-nouns-miscella.話':         E('おもしろい 話を 聞きました。', 'I heard an interesting story.'),
    P+'37-common-nouns-miscella.やくそく':   E('友だちと やくそくが あります。', 'I have an appointment with a friend.'),
    P+'37-common-nouns-miscella.ようじ':     E('ようじが あって、行けません。', "I have an errand, so I can't go."),
    P+'37-common-nouns-miscella.もんだい':   E('むずかしい もんだいです。', "It's a difficult problem."),
    P+'37-common-nouns-miscella.しゅみ':     E('わたしの しゅみは どくしょです。', 'My hobby is reading.'),
    P+'37-common-nouns-miscella.さんぽ':     E('こうえんで さんぽを します。', 'I take a walk in the park.'),
    P+'37-common-nouns-miscella.うんどう':   E('まいにち うんどうします。', 'I exercise every day.'),
    P+'37-common-nouns-miscella.ゲーム':     E('ゲームが すきです。', 'I like games.'),
    P+'37-common-nouns-miscella.しあい':     E('あした サッカーの しあいです。', "Tomorrow there's a soccer match."),
    P+'37-common-nouns-miscella.ニュース':   E('ニュースを 見ました。', 'I watched the news.'),
    P+'37-common-nouns-miscella.パーティー': E('土曜日に パーティーが あります。', "There's a party on Saturday."),
    P+'37-common-nouns-miscella.きって':     E('きってを 三まい 買いました。', 'I bought three stamps.'),
    P+'37-common-nouns-miscella.はがき':     E('はがきを 出します。', "I'll send a postcard."),
    P+'37-common-nouns-miscella.てがみ':     E('母に てがみを 書きます。', 'I write a letter to my mother.'),
    P+'37-common-nouns-miscella.きっぷ':     E('きっぷを 買います。', "I'll buy a ticket."),
    P+'37-common-nouns-miscella.おみやげ':   E('日本の おみやげを 買いました。', 'I bought Japanese souvenirs.'),
    P+'37-common-nouns-miscella.りゅうがく': E('日本に りゅうがくしました。', 'I studied abroad in Japan.'),
    P+'37-common-nouns-miscella.かぜ':       E('かぜを ひきました。', 'I caught a cold.'),
    P+'37-common-nouns-miscella.びょうき':   E('びょうきに なりました。', 'I got sick.'),
    P+'37-common-nouns-miscella.くすり':     E('くすりを 飲みます。', 'I take medicine.'),
    P+'37-common-nouns-miscella.けが':       E('けがを しました。', 'I got injured.'),
    P+'37-common-nouns-miscella.おゆ':       E('おゆを わかします。', 'I boil water.'),
    P+'37-common-nouns-miscella.おふろ':     E('おふろに 入ります。', 'I take a bath.'),
    P+'37-common-nouns-miscella.スリッパ':   E('スリッパを はきます。', 'I put on slippers.'),
    P+'37-common-nouns-miscella.ティッシュ': E('ティッシュを ください。', 'Tissues please.'),
    P+'37-common-nouns-miscella.よてい':     E('しゅうまつの よていは 何ですか。', "What's your weekend plan?"),
    P+'37-common-nouns-miscella.はこ':       E('はこの 中に 本が あります。', "There's a book in the box."),
    P+'37-common-nouns-miscella.はんぶん':   E('ケーキを はんぶん 食べました。', 'I ate half the cake.'),
    P+'37-common-nouns-miscella.はたち':     E('はたちに なりました。', 'I turned twenty.'),
    P+'37-common-nouns-miscella.ほか':       E('ほかの ものは ありますか。', 'Are there other things?'),
    P+'37-common-nouns-miscella.ほんとう':   E('ほんとうですか。', 'Is that true?'),
    P+'37-common-nouns-miscella.なつやすみ': E('なつやすみは 八月です。', 'Summer vacation is in August.'),
    P+'37-common-nouns-miscella.ペット':     E('うちの ペットは ねこです。', 'Our pet is a cat.'),
    P+'37-common-nouns-miscella.カレンダー': E('かべに カレンダーが あります。', "There's a calendar on the wall."),

    # 37. Common nouns misc - tail (final 27)
    P+'37-common-nouns-miscella.りょかん':       E('りょかんに とまりました。', 'I stayed at a Japanese inn.'),
    P+'37-common-nouns-miscella.マッチ':         E('マッチで 火を つけます。', 'I light a fire with a match.'),
    P+'37-common-nouns-miscella.はいざら':       E('はいざらは ありますか。', 'Is there an ashtray?'),
    P+'37-common-nouns-miscella.フィルム':       E('カメラの フィルムを かいました。', 'I bought camera film.'),
    P+'37-common-nouns-miscella.レコード':       E('むかしの レコードを 聞きます。', 'I listen to old records.'),
    P+'37-common-nouns-miscella.テープ':         E('テープに ろくおんします。', "I'll record on the tape."),
    P+'37-common-nouns-miscella.じかんわり':     E('じかんわりを 見せて ください。', 'Please show me the timetable.'),
    P+'37-common-nouns-miscella.へん':           E('この へんに スーパーは ありますか。', 'Is there a supermarket around here?'),
    P+'37-common-nouns-miscella.かてい':         E('かていの りょうりが すきです。', 'I like home cooking.'),
    P+'37-common-nouns-miscella.かびん':         E('かびんに 花を 入れます。', 'I put flowers in the vase.'),
    P+'37-common-nouns-miscella.かた':           E('この かんじの 読みかたを 教えて ください。', "Please teach me how to read this kanji."),
    P+'37-common-nouns-miscella.おくさん':       E('田中さんの おくさんは 先生です。', "Tanaka-san's wife is a teacher."),
    P+'37-common-nouns-miscella.せびろ':         E('せびろを きて 出かけます。', "I go out wearing a business suit."),
    P+'37-common-nouns-miscella.大きな':         E('大きな こえで 話します。', 'I speak in a loud voice.'),
    P+'37-common-nouns-miscella.たて':           E('はこの たては 三十センチです。', 'The box is 30 cm tall.'),
    P+'37-common-nouns-miscella.ゆうべ':         E('ゆうべは おそく ねました。', "Last night I went to bed late."),
    P+'37-common-nouns-miscella.にっき':         E('まいにち にっきを 書きます。', 'I write a diary every day.'),
    P+'37-common-nouns-miscella.さくぶん':       E('さくぶんを 書いて ください。', 'Please write a composition.'),
    P+'37-common-nouns-miscella.じびき':         E('じびきを ひきます。', "I'll look it up in the dictionary."),
    P+'37-common-nouns-miscella.テープレコーダー': E('テープレコーダーで ろくおんします。', "I'll record with a tape recorder."),
    P+'37-common-nouns-miscella.ストーブ':       E('冬は ストーブを つかいます。', 'In winter I use a heater.'),
    P+'37-common-nouns-miscella.ページ':         E('五ページを ひらいて ください。', 'Please open to page 5.'),
    P+'37-common-nouns-miscella.クラス':         E('わたしの クラスは 三十人です。', 'My class has 30 people.'),
    P+'37-common-nouns-miscella.グラム':         E('にくを 二百グラム ください。', '200 grams of meat please.'),
    P+'37-common-nouns-miscella.メートル':       E('百メートル はしりました。', 'I ran 100 meters.'),
    P+'37-common-nouns-miscella.キログラム':     E('五キログラムの 米を 買いました。', 'I bought 5 kg of rice.'),
    P+'37-common-nouns-miscella.キロメートル':   E('えきまで 三キロメートルです。', "It's 3 km to the station."),

    # 38. Sounds and voice
    P+'38-sounds-and-voice.おと':            E('外で 大きい おとが しました。', 'A loud sound came from outside.'),
    P+'38-sounds-and-voice.うた':            E('日本の うたが すきです。', 'I like Japanese songs.'),

    # 39. Function / filler expressions
    P+'39-function-filler-expre.えーと':     E('えーと、こたえは 三です。', "Um, the answer is three."),
    P+'39-function-filler-expre.そうですね': E('そうですね、いいですね。', "That's right, it's good."),
    P+'39-function-filler-expre.そうですか': E('そうですか、わかりました。', "Is that so. I see."),
    P+'39-function-filler-expre.ええ':       E('ええ、そうです。', "Yes, that's right."),
    P+'39-function-filler-expre.うん':       E('うん、いいよ。', "Yeah, sure."),
    P+'39-function-filler-expre.ううん':     E('ううん、ちがう。', "No, that's wrong."),
    P+'39-function-filler-expre.さあ':       E('さあ、わかりません。', "Hmm, I don't know."),
    P+'39-function-filler-expre.それでは':   E('それでは、はじめましょう。', "Well then, let's begin."),

    # 40. Misc useful items
    P+'40-misc-useful-items.もの':           E('大切な ものを なくしました。', "I lost something important."),
    P+'40-misc-useful-items.こと':           E('話したい ことが あります。', "There's something I want to talk about."),
    P+'40-misc-useful-items.ばしょ':         E('しずかな ばしょが すきです。', 'I like quiet places.'),
    P+'40-misc-useful-items.ばあい':         E('雨の ばあい、出かけません。', "In case of rain, I won't go out."),
    P+'40-misc-useful-items.ほう':           E('右の ほうに あります。', "It's on the right side."),
    P+'40-misc-useful-items.とき':           E('小さい とき、よく あそびました。', "When I was little, I played a lot."),
    P+'40-misc-useful-items.番号':           E('電話番号を 教えて ください。', 'Please tell me your phone number.'),
    P+'40-misc-useful-items.じゅうしょ':     E('じゅうしょを 書いて ください。', 'Please write your address.'),
    P+'40-misc-useful-items.ねんれい':       E('ねんれいを 聞いても いいですか。', 'May I ask your age?'),
    P+'40-misc-useful-items.学校':           E('学校に かよって います。', "I'm attending school."),
    P+'40-misc-useful-items.しゅみ':         E('しゅみは 音楽です。', 'My hobby is music.'),
    P+'40-misc-useful-items.しゅっしん':     E('しゅっしんは どこですか。', "Where are you from?"),
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
