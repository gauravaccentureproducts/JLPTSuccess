"""Wave 4 — extend 3rd vocab examples — next 60 by frequency_rank."""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

THIRD = {
    'n5.vocab.2-people-family.女の子':              {'ja': 'あの 女の子は わたしの いもうとです。',  'translation_en': 'That girl is my younger sister.'},
    'n5.vocab.24-school-and-study.じ':             {'ja': 'この じが よめません。',              'translation_en': 'I can\'t read this character.'},
    'n5.vocab.14-nature-and-weather.川':           {'ja': 'いえの ちかくに 川が あります。',       'translation_en': 'There is a river near my house.'},
    'n5.vocab.27-verbs-group-1-verbs.とる':         {'ja': 'たなから 本を とって ください。',       'translation_en': 'Please take the book from the shelf.'},
    'n5.vocab.27-verbs-group-1-verbs.とる.2':       {'ja': 'しゃしんを とっても いいですか。',      'translation_en': 'May I take a photo?'},
    'n5.vocab.31-adjectives.古い':                 {'ja': 'この いえは とても 古いです。',         'translation_en': 'This house is very old.'},
    'n5.vocab.37-common-nouns-miscella.はんぶん':    {'ja': 'ケーキを はんぶん 食べました。',        'translation_en': 'I ate half of the cake.'},
    'n5.vocab.2-people-family.あね':                {'ja': 'あねは 大学で べんきょうして います。', 'translation_en': 'My older sister studies at university.'},
    'n5.vocab.13-locations-and-places-.東':        {'ja': '東の 空が あかいですね。',              'translation_en': 'The eastern sky is red, isn\'t it?'},
    'n5.vocab.1-people-pronouns-and-se.みなさん':   {'ja': 'みなさん、こんにちは。',               'translation_en': 'Hello, everyone.'},
    'n5.vocab.27-verbs-group-1-verbs.およぐ':       {'ja': 'なつ プールで およぎます。',           'translation_en': 'I swim at the pool in summer.'},
    'n5.vocab.13-locations-and-places-.南':        {'ja': '南の しまへ りょこうに 行きます。',     'translation_en': 'I\'m going on a trip to the southern islands.'},
    'n5.vocab.17-food-items.パン':                 {'ja': 'まいあさ パンと たまごを 食べます。',   'translation_en': 'Every morning I eat bread and eggs.'},
    'n5.vocab.33-adverbs.ゆっくり':                  {'ja': 'もっと ゆっくり 話して ください。',     'translation_en': 'Please speak more slowly.'},
    'n5.vocab.11-time-days-weeks-month.毎年':      {'ja': '毎年 さくらが きれいに さきます。',     'translation_en': 'Cherry blossoms bloom beautifully every year.'},
    'n5.vocab.4-body-parts.め':                    {'ja': 'こん夜は めが つかれました。',          'translation_en': 'My eyes are tired tonight.'},
    'n5.vocab.28-verbs-group-2-verbs.つける':       {'ja': 'へやの 電気を つけて ください。',      'translation_en': 'Please turn on the room\'s light.'},
    'n5.vocab.31-adjectives.安い':                 {'ja': 'この くつは 安くて いいですね。',      'translation_en': 'These shoes are cheap and good.'},
    'n5.vocab.4-body-parts.あたま':                 {'ja': 'けさから あたまが いたいです。',       'translation_en': 'I\'ve had a headache since this morning.'},
    'n5.vocab.11-time-days-weeks-month.六日':      {'ja': '六日に かいぎが あります。',           'translation_en': 'There\'s a meeting on the 6th.'},
    'n5.vocab.27-verbs-group-1-verbs.分かる':      {'ja': 'いみが よく 分かりません。',           'translation_en': 'I don\'t understand the meaning well.'},
    'n5.vocab.13-locations-and-places-.スーパー':   {'ja': 'スーパーで くだものを 買いました。',    'translation_en': 'I bought fruit at the supermarket.'},
    'n5.vocab.11-time-days-weeks-month.今週':      {'ja': '今週の しゅうまつは いそがしいです。',  'translation_en': 'This weekend is busy.'},
    'n5.vocab.2-people-family.おとうと':            {'ja': 'おとうとは 中学生です。',              'translation_en': 'My younger brother is a middle-school student.'},
    'n5.vocab.20-colors.白':                       {'ja': '白い ねこを かって います。',          'translation_en': 'I\'m raising a white cat.'},
    'n5.vocab.27-verbs-group-1-verbs.いそぐ':      {'ja': 'えきへ いそいで 行きました。',         'translation_en': 'I hurried to the station.'},
    'n5.vocab.33-adverbs.たぶん':                   {'ja': 'たぶん あしたは 雨です。',             'translation_en': 'It will probably rain tomorrow.'},
    'n5.vocab.32-adjectives.きれい':                {'ja': 'へやが とても きれいですね。',         'translation_en': 'The room is very clean, isn\'t it?'},
    'n5.vocab.11-time-days-weeks-month.来年':      {'ja': '来年 大学を そつぎょうします。',       'translation_en': 'I\'ll graduate from university next year.'},
    'n5.vocab.26-house-and-furniture.ラジオ':       {'ja': 'まいあさ ラジオを 聞きます。',          'translation_en': 'I listen to the radio every morning.'},
    'n5.vocab.37-common-nouns-miscella.プレゼント':{'ja': '友だちに プレゼントを あげました。',  'translation_en': 'I gave a present to my friend.'},
    'n5.vocab.26-house-and-furniture.マンション':  {'ja': '新しい マンションに ひっこしました。',  'translation_en': 'I moved into a new condo.'},
    'n5.vocab.27-verbs-group-1-verbs.つく':         {'ja': '六時に えきに つきました。',           'translation_en': 'I arrived at the station at 6.'},
    'n5.vocab.2-people-family.いもうと':            {'ja': 'いもうとは 高校生です。',              'translation_en': 'My younger sister is a high-school student.'},
    'n5.vocab.3-people-roles.せいと':               {'ja': 'この クラスには 二十人の せいとが います。','translation_en': 'There are 20 pupils in this class.'},
    'n5.vocab.13-locations-and-places-.だいどころ':{'ja': 'だいどころで りょうりを しています。', 'translation_en': 'I\'m cooking in the kitchen.'},
    'n5.vocab.28-verbs-group-2-verbs.おしえる':     {'ja': 'みちを おしえて ください。',           'translation_en': 'Please show me the way.'},
    'n5.vocab.31-adjectives.つめたい':              {'ja': 'つめたい みずを ください。',           'translation_en': 'Please give me cold water.'},
    'n5.vocab.11-time-days-weeks-month.七日':      {'ja': '七日に 友だちが 来ます。',              'translation_en': 'A friend is coming on the 7th.'},
    'n5.vocab.27-verbs-group-1-verbs.話す':        {'ja': '先生と 日本語で 話します。',           'translation_en': 'I speak Japanese with the teacher.'},
    'n5.vocab.13-locations-and-places-.西':       {'ja': '西の そらが あかく なりました。',       'translation_en': 'The western sky turned red.'},
    'n5.vocab.27-verbs-group-1-verbs.つくる':       {'ja': '母が ばんごはんを つくります。',       'translation_en': 'My mother makes dinner.'},
    'n5.vocab.13-locations-and-places-.おてあらい':{'ja': 'おてあらいは どこですか。',            'translation_en': 'Where is the restroom?'},
    'n5.vocab.27-verbs-group-1-verbs.しぬ':        {'ja': 'にじゅう年前 そふが しにました。',      'translation_en': 'My grandfather died 20 years ago.'},
    'n5.vocab.13-locations-and-places-.レストラン':{'ja': 'えきの ちかくに レストランが あります。','translation_en': 'There is a restaurant near the station.'},
    'n5.vocab.28-verbs-group-2-verbs.かける':       {'ja': '母に 電話を かけました。',             'translation_en': 'I called my mother.'},
    'n5.vocab.18-drinks.コーヒー':                  {'ja': '朝 コーヒーを 一杯 飲みます。',         'translation_en': 'I drink one cup of coffee in the morning.'},
    'n5.vocab.2-people-family.おにいさん':           {'ja': 'おにいさんは どこに すんで いますか。', 'translation_en': 'Where does your older brother live?'},
    'n5.vocab.31-adjectives.ひくい':               {'ja': 'こえが ひくいですね。',                'translation_en': 'Your voice is low.'},
    'n5.vocab.18-drinks.ワイン':                   {'ja': 'たんじょうびに ワインを 飲みました。', 'translation_en': 'I had wine on my birthday.'},
    'n5.vocab.18-drinks.ビール':                   {'ja': '父は まいばん ビールを 一本 飲みます。','translation_en': 'My father drinks one bottle of beer every night.'},
    'n5.vocab.10-time-general.ゆうがた':            {'ja': 'ゆうがた こうえんで さんぽします。',    'translation_en': 'I take a walk in the park in the evening.'},
    'n5.vocab.14-nature-and-weather.天気':         {'ja': 'きょうは いい 天気ですね。',           'translation_en': 'The weather is nice today, isn\'t it?'},
    'n5.vocab.27-verbs-group-1-verbs.もつ':        {'ja': 'おもい にもつを もって います。',      'translation_en': 'I\'m holding heavy luggage.'},
    'n5.vocab.13-locations-and-places-.後ろ':     {'ja': 'いえの 後ろに 大きな 木が あります。', 'translation_en': 'There is a big tree behind the house.'},
    'n5.vocab.11-time-days-weeks-month.八日':      {'ja': '八日に 日本に つきました。',            'translation_en': 'I arrived in Japan on the 8th.'},
    'n5.vocab.31-adjectives.おいしい':              {'ja': 'この ラーメンは とても おいしいです。','translation_en': 'This ramen is very delicious.'},
    'n5.vocab.11-time-days-weeks-month.先週':      {'ja': '先週 友だちと えいがを 見ました。',     'translation_en': 'Last week I watched a movie with a friend.'},
    'n5.vocab.15-animals.とり':                    {'ja': 'こうえんに とりが たくさん います。',  'translation_en': 'There are many birds in the park.'},
    'n5.vocab.27-verbs-group-1-verbs.ならう':      {'ja': '父から ピアノを ならいました。',       'translation_en': 'I learned piano from my father.'},
}


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_third_example_wave4')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')
    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {e['id']: e for e in data['entries']}
    n = 0
    for vid, ex in THIRD.items():
        e = by_id.get(vid)
        if not e:
            print(f'  ! vocab not found: {vid}'); continue
        exs = e.get('examples') or []
        if len(exs) >= 3:
            print(f'  - skip: {vid}'); continue
        exs.append({'ja': ex['ja'], 'translation_en': ex['translation_en'], 'provenance': 'llm_curated'})
        e['examples'] = exs
        n += 1
    print(f'\nWave 4 added 3rd example on {n} more entries.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
