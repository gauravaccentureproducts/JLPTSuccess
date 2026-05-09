"""IMP-125 follow-up: replace auto_derived mnemonic stubs with
hand-authored visual + reading mnemonics for all 106 N5 kanji.

Each entry in MNEMONICS has:
  visual:  vivid image tying the glyph shape / radicals to the meaning
  reading: memorable hook for the most-used on-reading

The existing `summary` and `meaning` fields (native_reviewed
content) are preserved unchanged. Only the auto_derived stubs are
replaced. After this pass, provenance bumps to 'llm_curated'
(consistent with the project's existing `llm_curated` tier — not
claiming native review, but quality-checked content rather than
machine-generated stubs).
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Authored mnemonics for all 106 N5 kanji.
# visual: imagery tying components to meaning.
# reading: hook for the most-common reading (typically on-reading first).
MNEMONICS = {
    # ===== Numbers (1-10, 100, 1000, 10000) =====
    '一': {
        'visual': 'A single horizontal stroke — ONE finger held up flat.',
        'reading': 'いち / いつ — counting "ichi, ni, san" starts with ichi. Kun ひと appears in 一つ (hitotsu, one thing).',
    },
    '二': {
        'visual': 'Two horizontal strokes — TWO chopsticks resting parallel.',
        'reading': 'に — "ni" is the second beat in counting. Kun ふた lives in 二つ (futatsu, two things).',
    },
    '三': {
        'visual': 'Three horizontal strokes — THREE fingers raised.',
        'reading': 'さん — borrowed everywhere from "Mr/Ms" (-さん) to 三月 (sangatsu, March). Kun み in 三つ (mittsu).',
    },
    '四': {
        'visual': 'A box with two legs sticking down — FOUR legs of a table inside a frame.',
        'reading': 'し / よん — "shi" sounds like death so よん is preferred when counting people. Both readings are common.',
    },
    '五': {
        'visual': 'A capital "I" with extra strokes — FIVE fingers locked in a tight grip.',
        'reading': 'ご — quick and clean, as in 五月 (gogatsu, May). Kun いつ in 五つ (itsutsu).',
    },
    '六': {
        'visual': 'A roof over a pair of legs — SIX is the legs of a SIX-pack of beer under a tavern roof.',
        'reading': 'ろく — like rolling a SIX on a die: "rock and roll" → roku.',
    },
    '七': {
        'visual': 'A cross with a diagonal slash — SEVEN looks like a sliced NIL.',
        'reading': 'しち / なな — "shichi" can be misheard, so なな is common spoken-language fallback.',
    },
    '八': {
        'visual': 'Two strokes splaying outward — EIGHT legs of an OCTOPUS spread wide.',
        'reading': 'はち — sharp like a bee sting (hachi = bee in Japanese!), and 8 hours is はちじかん.',
    },
    '九': {
        'visual': 'A hooked stroke meeting a vertical — NINE looks like a fishhook catching a fish.',
        'reading': 'きゅう / く — "kyuu" used in counting, "ku" used in dates (九月 kugatsu, September).',
    },
    '十': {
        'visual': 'A perfect cross — TEN is two roads meeting; tally bars at TEN strokes.',
        'reading': 'じゅう / じっ — "juu" stretches to mean "complete." Used in 十時 (juuji, 10 o\'clock).',
    },
    '百': {
        'visual': 'One (一) stacked on white (白) — the FIRST WHITE coin: HUNDRED yen.',
        'reading': 'ひゃく — 100 of anything. Watch for sound shift: 三百 (sanbyaku), 六百 (roppyaku), 八百 (happyaku).',
    },
    '千': {
        'visual': 'A slash crossing a ten — like THOUSAND sticks falling at a slight angle.',
        'reading': 'せん — bills come in 千円 notes (sen-en). Kun ち in names like 千葉 (Chiba).',
    },
    '万': {
        'visual': 'A flag with a pole and a swooping line — TEN THOUSAND flags waving in a parade.',
        'reading': 'まん — used in 一万 (ichiman, 10,000). Watch the price tags for 万 to denote ten-thousand.',
    },
    '円': {
        'visual': 'A box with rounded inside — a coin in a wallet pocket. ROUND like the YEN coin.',
        'reading': 'えん — every yen price ends in 円. Also means "round" — an えんりょ-shaped coin.',
    },

    # ===== Calendar (day, month, week-elements) =====
    '日': {
        'visual': 'A box with a line through the middle — the SUN at noon, light splitting the sky.',
        'reading': 'にち / じつ / ひ / び — Sunday is にちようび. The kun ひ appears in 日 (hi, day) and 毎日 (mainichi, every day).',
    },
    '月': {
        'visual': 'A crescent shape with two horizontal lines — the MOON inside a window frame.',
        'reading': 'げつ / つき — Monday is げつようび. Kun つき: 月 (tsuki, moon).',
    },
    '火': {
        'visual': 'Sparks flying outward from a central point — FIRE leaping with two side flames.',
        'reading': 'か / ひ — Tuesday is かようび. Kun ひ: 火事 (kaji, fire emergency) but also ひ: 火 (hi, fire).',
    },
    '水': {
        'visual': 'A central drop with splashes either side — WATER spreading on impact.',
        'reading': 'すい / みず — Wednesday is すいようび. Kun みず is the base word for "water."',
    },
    '木': {
        'visual': 'A vertical trunk with branches outward and roots downward — a TREE.',
        'reading': 'もく / き — Thursday is もくようび. Kun き: 木 (ki, tree); also 木曜日 (mokuyoubi).',
    },
    '金': {
        'visual': 'A roof with two diamonds inside — GOLD nuggets hidden under the roof of a cave.',
        'reading': 'きん / かね — Friday is きんようび. Kun かね: お金 (okane, money).',
    },
    '土': {
        'visual': 'A cross with a bottom line — a stake driven into the EARTH with the line marking ground level.',
        'reading': 'ど / つち — Saturday is どようび. Kun つち: 土 (tsuchi, soil).',
    },
    '曜': {
        'visual': 'Sun (日) + wings + bird (隹) — the day BIRD soars across the SKY each WEEKDAY.',
        'reading': 'よう — only meaningful in 曜日 (youbi, day-of-week). Memorize the chunk: 月曜日 / 火曜日 ...',
    },
    '年': {
        'visual': 'A person leaning on a stick — an old man carrying the weight of YEARS.',
        'reading': 'ねん / とし — 一年 (ichinen, one year). Kun とし: 今年 (kotoshi, this year).',
    },
    '時': {
        'visual': 'Sun (日) + temple (寺) — the temple bell rings out the TIME of day.',
        'reading': 'じ / とき — clock times: 三時 (sanji, 3 o\'clock). Kun とき: そのとき (sono toki, at that time).',
    },
    '分': {
        'visual': 'Eight (八) over sword (刀) — divide a thing by cutting eight ways. A MINUTE is a divided slice of an hour.',
        'reading': 'ふん / ぷん / ぶん — minutes shift voicing: 一分 (ippun), 三分 (sanpun). Also ぶん in 自分 (jibun, oneself).',
    },
    '半': {
        'visual': 'Eight on top + cow below cut down the middle — HALF of a cow.',
        'reading': 'はん — 半分 (hanbun, half) and 三時半 (sanji-han, 3:30). Always はん.',
    },
    '今': {
        'visual': 'A roof over a small mark — sheltering RIGHT NOW under the present moment.',
        'reading': 'こん / いま — 今日 (kyou, today!) and 今週 (konshuu, this week). Kun いま: 今 (ima, now).',
    },
    '毎': {
        'visual': 'A person bent forward + 母 mother — every mother bends to her child EVERY day.',
        'reading': 'まい — only in compounds: 毎日 (mainichi, every day), 毎週 (maishuu, every week), 毎年 (maitoshi).',
    },
    '週': {
        'visual': 'Walking radical (⻌) + 周 around — a WEEK is what you walk around in seven days.',
        'reading': 'しゅう — 今週 (konshuu, this week), 来週 (raishuu, next week). Always しゅう.',
    },
    '午': {
        'visual': 'A horizontal line with a pestle below — at NOON the sun pounds straight down on the ground.',
        'reading': 'ご — only in 午前 (gozen, AM) and 午後 (gogo, PM). Solid ご.',
    },
    '何': {
        'visual': 'A person (亻) + 可 can — when a person CAN\'T name something, they ask "WHAT?"',
        'reading': 'なに / なん — なに alone (何ですか) but なん before some sounds (何時, nanji). Watch the shift!',
    },

    # ===== People (you, family, body) =====
    '人': {
        'visual': 'Two strokes leaning into each other — a PERSON walking on two legs.',
        'reading': 'じん / にん / ひと — country + 人 = nationality (日本人 nihonjin). Kun ひと: あの人 (ano hito).',
    },
    '男': {
        'visual': 'Field (田) on top + power (力) below — a MAN providing POWER to the FIELD.',
        'reading': 'だん / おとこ — 男の人 (otoko no hito, man). Also 男性 (dansei, male).',
    },
    '女': {
        'visual': 'A figure with crossed legs gracefully kneeling — a WOMAN sitting in seiza.',
        'reading': 'じょ / おんな — 女の人 (onna no hito, woman). 女性 (josei, female).',
    },
    '子': {
        'visual': 'A baby with arms out and legs swaddled — a CHILD bundled tight.',
        'reading': 'し / こ — kun こ in 子供 (kodomo, child). On し in 男子 (danshi).',
    },
    '父': {
        'visual': 'Two crossed arms over a base — FATHER holding everything together.',
        'reading': 'ふ / ちち / とう — Polite お父さん (otousan), humble 父 (chichi). On ふ in 父親 (chichioya).',
    },
    '母': {
        'visual': 'A figure with two prominent dots — MOTHER with caring eyes (or feeding her child).',
        'reading': 'ぼ / はは / かあ — Polite お母さん (okaasan), humble 母 (haha). On ぼ in 母国 (bokoku, motherland).',
    },
    '友': {
        'visual': 'Two crossed hands — FRIENDS shaking hands or high-fiving.',
        'reading': 'ゆう / とも — 友達 (tomodachi, friend). On ゆう in 友人 (yuujin).',
    },
    '先': {
        'visual': 'A leg stepping forward, leading the way — going FIRST and AHEAD.',
        'reading': 'せん / さき — 先生 (sensei, teacher = "born ahead"). Kun さき: 先 (saki, ahead).',
    },
    '生': {
        'visual': 'A sprout pushing through the earth — LIFE BEING BORN.',
        'reading': 'せい / しょう / い / う / なま — 学生 (gakusei, student), 生まれる (umareru, to be born). Hugely flexible kanji.',
    },
    '手': {
        'visual': 'A hand with three fingers and a thumb — HAND raised.',
        'reading': 'しゅ / て — 手 (te, hand) — direct and frequent. On しゅ in 手段 (shudan, method).',
    },
    '足': {
        'visual': 'Top mouth + bottom path — using your FEET to walk and TALK.',
        'reading': 'そく / あし / た — 足 (ashi, foot/leg). 足りる (tariru, to be enough).',
    },
    '目': {
        'visual': 'A vertical eye, the iris in the middle — EYE rotated 90°.',
        'reading': 'もく / め — Kun め: 目 (me, eye), very common. 目的 (mokuteki, purpose) for the on.',
    },
    '口': {
        'visual': 'A square box opening — an open MOUTH.',
        'reading': 'こう / くち / ぐち — 入り口 (iriguchi, entrance), 人口 (jinkou, population).',
    },
    '力': {
        'visual': 'A bicep flexed — pure muscle POWER.',
        'reading': 'りょく / ちから — 力 (chikara, strength). 体力 (tairyoku, physical strength).',
    },

    # ===== School & study =====
    '学': {
        'visual': 'A roof over a child reaching for knowledge — STUDYING under a school.',
        'reading': 'がく / まな — 学校 (gakkou, school), 学生 (gakusei, student). Kun まな: 学ぶ (manabu).',
    },
    '校': {
        'visual': 'Tree (木) + 交 cross — buildings made of wood standing in CROSSED rows: a SCHOOL campus.',
        'reading': 'こう — 学校 (gakkou). Always こう.',
    },
    '本': {
        'visual': 'A tree (木) with a bar at the base — the ROOT of the tree, the ORIGIN, a BOOK at its core.',
        'reading': 'ほん / もと / ぼん / ぽん — 日本 (Nihon, Japan), 本 (hon, book). Kun もと: 本 (moto, origin).',
    },
    '語': {
        'visual': 'Speech (言) + 五 five + 口 mouth — five mouths SPEAKING a LANGUAGE.',
        'reading': 'ご — 日本語 (nihongo), 英語 (eigo). Always ご.',
    },
    '国': {
        'visual': 'Border (囗) around 玉 jade — a COUNTRY is a treasure surrounded by a border.',
        'reading': 'こく / ごく / くに — 国 (kuni, country). 中国 (chuugoku, China).',
    },
    '会': {
        'visual': 'A roof over 云 cloud — people MEETING under a roof, MEETING at the cloud level.',
        'reading': 'かい / あ — 会社 (kaisha, company), 会議 (kaigi, meeting). Kun あ: 会う (au, to meet).',
    },
    '社': {
        'visual': 'Spirit altar (示) + 土 earth — the COMPANY shrine where workers pray to the earth-god.',
        'reading': 'しゃ — 会社 (kaisha, company), 社員 (shain, employee). Always しゃ.',
    },
    '員': {
        'visual': 'Mouth (口) over 貝 shell-money — the MEMBER who counts shells with mouth open.',
        'reading': 'いん — 会社員 (kaishain), 駅員 (ekiin, station-staff), 店員 (tenin, shop clerk).',
    },

    # ===== Size & position =====
    '大': {
        'visual': 'A person (人) with arms outstretched — "It was THIS BIG!"',
        'reading': 'だい / たい / おお — 大学 (daigaku, university), 大きい (ookii, big).',
    },
    '中': {
        'visual': 'A box with a vertical line piercing through the MIDDLE — bull\'s eye.',
        'reading': 'ちゅう / なか — 中国 (chuugoku, China), 中 (naka, inside).',
    },
    '小': {
        'visual': 'A central stroke with two flecks — SMALL grains of rice on either side.',
        'reading': 'しょう / ちい / こ / お — 小さい (chiisai, small), 小学校 (shougakkou, primary school).',
    },
    '上': {
        'visual': 'A bar above the ground line — UP, ABOVE.',
        'reading': 'じょう / うえ / あ / のぼ — 上 (ue, above), 上手 (jouzu, skilled), 上る (noboru, to climb).',
    },
    '下': {
        'visual': 'A bar below the ground line — DOWN, BELOW.',
        'reading': 'か / げ / した / さ / お — 下 (shita, below), 地下 (chika, underground).',
    },
    '左': {
        'visual': 'A hand sweeping left over a workbench — your LEFT hand at the workshop.',
        'reading': 'さ / ひだり — 左 (hidari, left). 左右 (sayuu, left and right).',
    },
    '右': {
        'visual': 'A hand bringing food to the mouth — your RIGHT hand eats for you.',
        'reading': 'ゆう / う / みぎ — 右 (migi, right). 右側 (migigawa, right side).',
    },
    '前': {
        'visual': 'Horns (or a moon) in BEFORE-sky — what comes BEFORE.',
        'reading': 'ぜん / まえ — 前 (mae, in front). 午前 (gozen, AM), 前回 (zenkai, previous time).',
    },
    '後': {
        'visual': 'Walking radical + thread + bottom — the THREAD comes BEHIND on the path.',
        'reading': 'ご / こう / あと / うし / おく — 後 (ato, after). 午後 (gogo, PM), 後ろ (ushiro, behind).',
    },
    '外': {
        'visual': 'Evening (夕) + divination (卜) — fortune-telling done OUTSIDE.',
        'reading': 'がい / げ / そと / ほか — 外国 (gaikoku, foreign country), 外 (soto, outside).',
    },

    # ===== Directions =====
    '東': {
        'visual': 'Sun (日) caught in a tree (木) — the sun rising in the EAST through the trees.',
        'reading': 'とう / ひがし — 東京 (Toukyou, Tokyo, "Eastern capital"). Kun ひがし: 東 (higashi).',
    },
    '西': {
        'visual': 'A bird-cage at sunset — birds returning to the cage in the WEST.',
        'reading': 'せい / さい / にし — 西 (nishi, west). 西洋 (seiyou, the West/Western).',
    },
    '南': {
        'visual': 'A roof, a samurai banner — banners flying SOUTH in summer wind.',
        'reading': 'なん / みなみ — 南 (minami, south). 南極 (nankyoku, Antarctica).',
    },
    '北': {
        'visual': 'Two figures back-to-back — turning their backs to the cold NORTH wind.',
        'reading': 'ほく / きた — 北 (kita, north). 東北 (Touhoku, the northeast region).',
    },
    '間': {
        'visual': 'Gate (門) with sun (日) inside — the SPACE BETWEEN two walls where light enters.',
        'reading': 'かん / けん / あいだ / ま — 時間 (jikan, time-space), 間 (aida, between).',
    },

    # ===== Nature =====
    '山': {
        'visual': 'Three peaks rising in a row — MOUNTAIN ridge.',
        'reading': 'さん / やま — 富士山 (Fujisan, Mt. Fuji), 山 (yama, mountain).',
    },
    '川': {
        'visual': 'Three flowing vertical strokes — water FLOWING DOWN a RIVER.',
        'reading': 'せん / かわ / がわ — 川 (kawa, river). 川辺 (kawabe, riverside).',
    },
    '田': {
        'visual': 'A grid of four rice paddies — RICE FIELDS divided by levees.',
        'reading': 'でん / た / だ — common in surnames: 田中 (Tanaka), 山田 (Yamada).',
    },
    '雨': {
        'visual': 'A roof with four drops falling — RAIN coming down outside.',
        'reading': 'う / あめ — 雨 (ame, rain). 大雨 (ooame, heavy rain).',
    },
    '天': {
        'visual': 'A person (大) reaching above — touching the SKY/HEAVENS.',
        'reading': 'てん / あま / あめ — 天気 (tenki, weather), 天才 (tensai, genius).',
    },
    '気': {
        'visual': 'Steam rising — the air ENERGY surrounding things.',
        'reading': 'き / け — 元気 (genki, energetic), 天気 (tenki, weather), 病気 (byouki, sickness).',
    },
    '花': {
        'visual': 'Grass (艹) + 化 change — a sprout CHANGED into a FLOWER.',
        'reading': 'か / はな — 花 (hana, flower). 花見 (hanami, flower viewing).',
    },
    '空': {
        'visual': 'Cave (穴) + 工 work — the EMPTY SKY carved out above.',
        'reading': 'くう / そら / から / あ — 空 (sora, sky), 空気 (kuuki, air), 空く (aku, to become empty).',
    },
    '電': {
        'visual': 'Rain (雨) + 田 lightning streak — ELECTRICITY: lightning in the rain.',
        'reading': 'でん — 電車 (densha, train), 電話 (denwa, phone), 電気 (denki, electricity).',
    },

    # ===== Travel & shops =====
    '車': {
        'visual': 'A wagon viewed from above — the body and two wheels of a CAR.',
        'reading': 'しゃ / くるま — 自動車 (jidousha, automobile), 車 (kuruma, car).',
    },
    '道': {
        'visual': 'Walking radical + neck (首) — keeping your NECK aimed at the ROAD ahead.',
        'reading': 'どう / みち — 道 (michi, road), 北海道 (Hokkaidou). 茶道 (sadou, tea ceremony "way").',
    },
    '店': {
        'visual': 'Shed (广) + 占 fortune — fortune-tellers SET UP SHOP under a roof.',
        'reading': 'てん / みせ — 店 (mise, shop). 店員 (tenin, shop clerk), 喫茶店 (kissaten, café).',
    },
    '駅': {
        'visual': 'Horse (馬) + 尺 measure — STATIONS are where horses were measured/changed.',
        'reading': 'えき — 駅 (eki, station). 東京駅 (Toukyou-eki). Always えき.',
    },

    # ===== Eating, drinking, perceiving =====
    '食': {
        'visual': 'A roof over rice — sheltering the FOOD beneath.',
        'reading': 'しょく / く / た — 食べる (taberu, to eat), 食事 (shokuji, meal).',
    },
    '飲': {
        'visual': 'Eat-radical (食) + 欠 lack — you lack water, so you DRINK.',
        'reading': 'いん / の — 飲む (nomu, to drink), 飲み物 (nomimono, drink).',
    },
    '見': {
        'visual': 'An eye (目) on legs (儿) — eyes that walk around to SEE everything.',
        'reading': 'けん / み — 見る (miru, to see/watch). 意見 (iken, opinion).',
    },
    '聞': {
        'visual': 'Gate (門) + ear (耳) — putting your EAR to the GATE to LISTEN.',
        'reading': 'ぶん / もん / き — 聞く (kiku, to listen/ask). 新聞 (shinbun, newspaper).',
    },
    '読': {
        'visual': 'Speech (言) + 売 sell — READING ALOUD to sell the words to the audience.',
        'reading': 'どく / よ — 読む (yomu, to read). 読書 (dokusho, reading books).',
    },
    '書': {
        'visual': 'Brush (聿) + 日 page — a BRUSH WRITING on the page.',
        'reading': 'しょ / か — 書く (kaku, to write). 図書館 (toshokan, library).',
    },
    '話': {
        'visual': 'Speech (言) + tongue (舌) — words spoken with the tongue: TALK.',
        'reading': 'わ / はな — 話す (hanasu, to talk). 電話 (denwa, phone), 会話 (kaiwa, conversation).',
    },

    # ===== Movement verbs =====
    '来': {
        'visual': 'A person (人) under a tree — COME under the shade.',
        'reading': 'らい / く / き / こ — 来る (kuru, to come). 来週 (raishuu, next week).',
    },
    '行': {
        'visual': 'A crossroads viewed from above — choose where to GO.',
        'reading': 'こう / ぎょう / い / おこな — 行く (iku, to go). 銀行 (ginkou, bank), 行事 (gyouji, event).',
    },
    '出': {
        'visual': 'A mountain on top of a mountain — climbing OUT of the valley.',
        'reading': 'しゅつ / すい / で / だ — 出る (deru, to leave). 出口 (deguchi, exit), 出発 (shuppatsu).',
    },
    '入': {
        'visual': 'Two strokes meeting at a point — entering through a doorway, GOING IN.',
        'reading': 'にゅう / い / はい — 入る (hairu, to enter). 入口 (iriguchi, entrance), 入学 (nyuugaku).',
    },
    '立': {
        'visual': 'A person standing tall on the ground — STAND UP straight.',
        'reading': 'りつ / りゅう / た — 立つ (tatsu, to stand). 国立 (kokuritsu, national).',
    },
    '休': {
        'visual': 'A person (亻) leaning against a tree (木) — REST against the trunk.',
        'reading': 'きゅう / やす — 休む (yasumu, to rest). 休日 (kyuujitsu, day off).',
    },
    '言': {
        'visual': 'A mouth with words coming out in layered lines — SPEAKING multiple ideas.',
        'reading': 'げん / ごん / い / こと — 言う (iu, to say). 言葉 (kotoba, word), 言語 (gengo, language).',
    },
    '買': {
        'visual': 'A net (罒) over shell-money (貝) — netting up coins to BUY something.',
        'reading': 'ばい / か — 買う (kau, to buy). 売買 (baibai, buying-and-selling).',
    },

    # ===== Adjectives =====
    '高': {
        'visual': 'A tall pagoda silhouette — TALL/HIGH/EXPENSIVE building.',
        'reading': 'こう / たか — 高い (takai, tall/expensive). 高校 (koukou, high school).',
    },
    '安': {
        'visual': 'A roof over a woman — woman safe at home: PEACEFUL, also CHEAP.',
        'reading': 'あん / やす — 安い (yasui, cheap). 安心 (anshin, peace of mind).',
    },
    '新': {
        'visual': 'Stand (立) + tree (木) + axe (斤) — chopping NEW wood with a fresh axe.',
        'reading': 'しん / あたら / あら / にい — 新しい (atarashii, new). 新聞 (shinbun, newspaper).',
    },
    '古': {
        'visual': 'Ten (十) + mouth (口) — ten generations of mouths talking: this is OLD news.',
        'reading': 'こ / ふる — 古い (furui, old). 中古 (chuuko, used/secondhand).',
    },
    '長': {
        'visual': 'A figure with long flowing hair down the back — LONG and the HEAD/CHIEF.',
        'reading': 'ちょう / なが — 長い (nagai, long). 社長 (shachou, company president).',
    },
    '白': {
        'visual': 'A simple kanji with a tail — a candle\'s WHITE flame casting light.',
        'reading': 'はく / びゃく / しろ / しら — 白い (shiroi, white). 白人 (hakujin, white person).',
    },

    # ===== Naming, ordering =====
    '名': {
        'visual': 'Evening (夕) + mouth (口) — at evening you speak your NAME.',
        'reading': 'めい / みょう / な — 名前 (namae, name). 有名 (yuumei, famous).',
    },
    '番': {
        'visual': 'Rice (米) + field (田) — taking your TURN in the rice field.',
        'reading': 'ばん — 番号 (bangou, number), 一番 (ichiban, #1, first). Always ばん.',
    },
    '号': {
        'visual': 'Mouth (口) + bent breath — calling out a NUMBER/CALL-SIGN.',
        'reading': 'ごう — 番号 (bangou, number), 信号 (shingou, traffic signal). Always ごう.',
    },

    # ===== I, the watashi =====
    '私': {
        'visual': 'Rice (禾) + 厶 private — your PRIVATE rice supply: I, ME.',
        'reading': 'し / わたし / わたくし — 私 (watashi, I). On し in 私生活 (shiseikatsu, private life).',
    },
}

# ---- Apply ----
kanji_path = ROOT / 'data' / 'kanji.json'
data = json.loads(kanji_path.read_text(encoding='utf-8'))
entries = data.get('entries', data) if isinstance(data, dict) else data

updated_visual = 0
updated_reading = 0
missing = []

for e in entries:
    g = e.get('glyph')
    if g not in MNEMONICS:
        missing.append(g)
        continue
    mn = MNEMONICS[g]
    em = e.get('mnemonic')
    if not isinstance(em, dict):
        continue
    em['visual'] = mn['visual']
    em['reading'] = mn['reading']
    em.setdefault('provenance', {})
    em['provenance']['visual'] = 'llm_curated'
    em['provenance']['reading'] = 'llm_curated'
    updated_visual += 1
    updated_reading += 1

kanji_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print(f'Total kanji: {len(entries)}')
print(f'  visual mnemonics authored:  {updated_visual}')
print(f'  reading mnemonics authored: {updated_reading}')
print(f'  glyphs not in MNEMONICS dict: {len(missing)}')
if missing:
    print(f'  missing: {" ".join(missing)}')
