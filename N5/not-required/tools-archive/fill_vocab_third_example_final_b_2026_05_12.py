"""Final wave B — the LAST 84 entries to reach 100% P3 #15 coverage."""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

THIRD = {
    # Family / roles
    'n5.vocab.2-people-family.あに':              {'ja': 'あには 大学生です。',                  'translation_en': 'My older brother is a university student.'},
    'n5.vocab.2-people-family.そぼ':              {'ja': 'そぼは とても げんきです。',           'translation_en': 'My grandmother is very energetic.'},
    'n5.vocab.3-people-roles.いしゃ':              {'ja': 'いしゃに 見て もらいました。',          'translation_en': 'I had a doctor examine me.'},
    'n5.vocab.3-people-roles.おまわりさん':         {'ja': 'こうばんで おまわりさんに 聞きました。','translation_en': 'I asked the friendly cop at the police box.'},

    # Time
    'n5.vocab.10-time-general.あさ':               {'ja': 'まいあさ 六時に おきます。',            'translation_en': 'I get up at 6 every morning.'},
    'n5.vocab.10-time-general.ひる':               {'ja': 'ひるに かれと 会います。',              'translation_en': 'I\'ll meet him at noon.'},
    'n5.vocab.11-time-days-weeks-month.三日':      {'ja': '三日に かいぎが あります。',             'translation_en': 'There\'s a meeting on the 3rd.'},
    'n5.vocab.11-time-days-weeks-month.十日':      {'ja': '十日に 友だちが きます。',              'translation_en': 'A friend is coming on the 10th.'},
    'n5.vocab.11-time-days-weeks-month.おととし':   {'ja': 'おととし 日本へ 行きました。',           'translation_en': 'I went to Japan the year before last.'},

    # Places
    'n5.vocab.13-locations-and-places-.かど':     {'ja': 'つぎの かどを 右に まがって ください。','translation_en': 'Please turn right at the next corner.'},

    # Nature
    'n5.vocab.14-nature-and-weather.くさ':        {'ja': 'にわの くさを 切りました。',            'translation_en': 'I cut the grass in the garden.'},
    'n5.vocab.14-nature-and-weather.くも':        {'ja': '空に 白い くもが あります。',           'translation_en': 'There are white clouds in the sky.'},
    'n5.vocab.14-nature-and-weather.くもり':       {'ja': 'あしたは くもりの 予報です。',          'translation_en': 'Tomorrow\'s forecast is cloudy.'},
    'n5.vocab.14-nature-and-weather.あつい':      {'ja': 'なつは とても あついです。',            'translation_en': 'Summer is very hot.'},

    # Animals
    'n5.vocab.15-animals.いぬ':                    {'ja': 'いぬは 私の 友だちです。',             'translation_en': 'A dog is my friend.'},
    'n5.vocab.15-animals.にわとり':                 {'ja': 'にわとりが 朝 はやく なきます。',       'translation_en': 'Roosters crow early in the morning.'},

    # Food
    'n5.vocab.17-food-items.たまご':                {'ja': 'まいあさ たまごを 食べます。',          'translation_en': 'I eat eggs every morning.'},
    'n5.vocab.17-food-items.くだもの':              {'ja': 'くだものは からだに いいです。',        'translation_en': 'Fruit is good for the body.'},
    'n5.vocab.17-food-items.すいか':                {'ja': 'なつには すいかを 食べます。',          'translation_en': 'I eat watermelon in summer.'},
    'n5.vocab.17-food-items.たまねぎ':              {'ja': 'たまねぎを 半分 切りました。',          'translation_en': 'I cut a half onion.'},
    'n5.vocab.17-food-items.しお':                 {'ja': 'スープに しおを 入れました。',          'translation_en': 'I added salt to the soup.'},
    'n5.vocab.17-food-items.さとう':                {'ja': 'コーヒーに さとうを 入れますか。',       'translation_en': 'Will you put sugar in your coffee?'},
    'n5.vocab.18-drinks.おちゃ':                   {'ja': '朝は おちゃを 飲みます。',             'translation_en': 'I drink tea in the morning.'},

    # Colors
    'n5.vocab.20-colors.あお':                     {'ja': 'あおい シャツを きました。',           'translation_en': 'I wore a blue shirt.'},

    # Clothing
    'n5.vocab.21-clothing-and-accessor.ワイシャツ':{'ja': '父は 白い ワイシャツを きて います。',  'translation_en': 'My father is wearing a white dress shirt.'},

    # School
    'n5.vocab.24-school-and-study.いみ':           {'ja': 'いみを じしょで しらべました。',        'translation_en': 'I looked up the meaning in a dictionary.'},
    'n5.vocab.24-school-and-study.もじ':           {'ja': '小さい もじが よみにくいです。',        'translation_en': 'Small characters are hard to read.'},
    'n5.vocab.24-school-and-study.チョーク':        {'ja': '先生が チョークで 書きました。',        'translation_en': 'The teacher wrote with chalk.'},
    'n5.vocab.24-school-and-study.おしらせ':       {'ja': '学校から おしらせが きました。',        'translation_en': 'A notice came from the school.'},

    # Languages
    'n5.vocab.25-languages-and-countri.外国語':   {'ja': '外国語を ふたつ はなせます。',          'translation_en': 'I can speak two foreign languages.'},

    # House
    'n5.vocab.26-house-and-furniture.ふとん':       {'ja': 'ふとんで ねます。',                   'translation_en': 'I sleep on a futon.'},
    'n5.vocab.26-house-and-furniture.たな':        {'ja': 'たなに 本を ならべました。',            'translation_en': 'I lined up books on the shelf.'},
    'n5.vocab.26-house-and-furniture.せっけん':     {'ja': 'せっけんで 手を あらいます。',          'translation_en': 'I wash my hands with soap.'},

    # Verb-1
    'n5.vocab.27-verbs-group-1-verbs.うたう':       {'ja': 'パーティーで うたを うたいました。',    'translation_en': 'I sang a song at the party.'},
    'n5.vocab.27-verbs-group-1-verbs.しる':        {'ja': 'この 人を しって いますか。',          'translation_en': 'Do you know this person?'},
    'n5.vocab.27-verbs-group-1-verbs.おわる':      {'ja': 'えいがは 九時に おわります。',          'translation_en': 'The movie ends at 9.'},
    'n5.vocab.27-verbs-group-1-verbs.おす':        {'ja': 'この ボタンを おして ください。',       'translation_en': 'Please press this button.'},
    'n5.vocab.27-verbs-group-1-verbs.よぶ':        {'ja': 'タクシーを よびました。',              'translation_en': 'I called a taxi.'},
    'n5.vocab.27-verbs-group-1-verbs.とぶ':        {'ja': 'とりが 空を とんで います。',           'translation_en': 'Birds are flying in the sky.'},
    'n5.vocab.27-verbs-group-1-verbs.こまる':       {'ja': 'お金が なくて、こまりました。',         'translation_en': 'I was in trouble because I had no money.'},
    'n5.vocab.27-verbs-group-1-verbs.ならぶ':       {'ja': 'みんな ならんで まちました。',          'translation_en': 'Everyone lined up and waited.'},
    'n5.vocab.27-verbs-group-1-verbs.わたす':      {'ja': '先生に レポートを わたしました。',     'translation_en': 'I handed the report to the teacher.'},
    'n5.vocab.27-verbs-group-1-verbs.ぬぐ':        {'ja': 'いえで くつを ぬぎます。',             'translation_en': 'I take off my shoes at home.'},
    'n5.vocab.27-verbs-group-1-verbs.あらう':      {'ja': 'まいあさ かおを あらいます。',          'translation_en': 'I wash my face every morning.'},
    'n5.vocab.27-verbs-group-1-verbs.すわる':      {'ja': 'いすに すわって ください。',           'translation_en': 'Please sit on the chair.'},
    'n5.vocab.27-verbs-group-1-verbs.たのむ':      {'ja': '友だちに しゅくだいを たのみました。', 'translation_en': 'I asked my friend a favor about homework.'},
    'n5.vocab.27-verbs-group-1-verbs.とまる':      {'ja': 'バスが えきに とまります。',            'translation_en': 'The bus stops at the station.'},

    # Verb-2
    'n5.vocab.28-verbs-group-2-verbs.おきる':      {'ja': 'まいあさ 七時に おきます。',           'translation_en': 'I get up at 7 every morning.'},
    'n5.vocab.28-verbs-group-2-verbs.おぼえる':    {'ja': '新しい かんじを 五つ おぼえました。',  'translation_en': 'I memorized five new kanji.'},
    'n5.vocab.28-verbs-group-2-verbs.あびる':      {'ja': 'まいあさ シャワーを あびます。',        'translation_en': 'I take a shower every morning.'},
    'n5.vocab.28-verbs-group-2-verbs.おちる':      {'ja': 'りんごが 木から おちました。',          'translation_en': 'An apple fell from the tree.'},
    'n5.vocab.28-verbs-group-2-verbs.はれる':      {'ja': '雨が やんで、空が はれました。',        'translation_en': 'The rain stopped and the sky cleared up.'},
    'n5.vocab.28-verbs-group-2-verbs.おりる':      {'ja': 'つぎの えきで おります。',              'translation_en': 'I\'ll get off at the next station.'},
    'n5.vocab.28-verbs-group-2-verbs.おくれる':    {'ja': '電車が おくれました。',                'translation_en': 'The train was late.'},
    'n5.vocab.28-verbs-group-2-verbs.ためる':      {'ja': '毎月 お金を ためて います。',          'translation_en': 'I\'m saving money every month.'},

    # Verb-1 (existence)
    'n5.vocab.30-verbs-existence-and-p.かえす':    {'ja': '友だちに 本を かえしました。',         'translation_en': 'I returned the book to my friend.'},
    'n5.vocab.30-verbs-existence-and-p.ござる':    {'ja': 'こちらに スプーンが ございます。',     'translation_en': 'Here is a spoon (very polite).'},

    # i-adj
    'n5.vocab.31-adjectives.あつい':              {'ja': 'なつは あついです。',                  'translation_en': 'Summer is hot.'},
    'n5.vocab.31-adjectives.あつい.2':            {'ja': 'おちゃが あついです。',                'translation_en': 'The tea is hot.'},
    'n5.vocab.31-adjectives.あつい.3':            {'ja': 'あつい 本を 読んで います。',          'translation_en': 'I\'m reading a thick book.'},
    'n5.vocab.31-adjectives.みじかい':             {'ja': 'みじかい てがみを 書きました。',        'translation_en': 'I wrote a short letter.'},
    'n5.vocab.31-adjectives.ひろい':              {'ja': 'この いえは とても ひろいです。',     'translation_en': 'This house is very spacious.'},
    'n5.vocab.31-adjectives.せまい':              {'ja': 'この みちは せまいですね。',           'translation_en': 'This road is narrow.'},
    'n5.vocab.31-adjectives.うすい':              {'ja': 'うすい シャツを きました。',           'translation_en': 'I wore a thin shirt.'},
    'n5.vocab.31-adjectives.つよい':              {'ja': '父は とても つよいです。',             'translation_en': 'My father is very strong.'},
    'n5.vocab.31-adjectives.はやい':              {'ja': 'はやく 出かけましょう。',              'translation_en': 'Let\'s leave early.'},
    'n5.vocab.31-adjectives.おそい':              {'ja': 'バスが おそく きました。',              'translation_en': 'The bus came late.'},
    'n5.vocab.31-adjectives.かなしい':             {'ja': 'えいがが とても かなしかったです。',    'translation_en': 'The movie was very sad.'},
    'n5.vocab.31-adjectives.いたい':              {'ja': 'あたまが いたいです。',                'translation_en': 'My head hurts.'},
    'n5.vocab.31-adjectives.うつくしい':           {'ja': 'うつくしい けしきですね。',            'translation_en': 'What beautiful scenery.'},
    'n5.vocab.31-adjectives.きたない':             {'ja': 'へやが きたないです。そうじします。',  'translation_en': 'The room is dirty. I\'ll clean it.'},
    'n5.vocab.31-adjectives.いそがしい':            {'ja': '今週は とても いそがしいです。',       'translation_en': 'This week is very busy.'},
    'n5.vocab.31-adjectives.あまい':              {'ja': 'この ケーキは あまいですね。',         'translation_en': 'This cake is sweet.'},
    'n5.vocab.31-adjectives.すくない':             {'ja': '人が すくないですね。',                'translation_en': 'There are few people.'},
    'n5.vocab.31-adjectives.ちかい':              {'ja': '駅は ちかいです。あるいて 行けます。',  'translation_en': 'The station is near. We can walk.'},
    'n5.vocab.31-adjectives.ぬるい':              {'ja': 'コーヒーが ぬるく なりました。',        'translation_en': 'The coffee got lukewarm.'},

    # na-adj
    'n5.vocab.32-adjectives.げんき':              {'ja': 'おばあさんは とても げんきです。',     'translation_en': 'Grandma is very energetic.'},
    'n5.vocab.32-adjectives.じょうず':             {'ja': 'うたが じょうずですね。',              'translation_en': 'You\'re good at singing.'},

    # Adverb
    'n5.vocab.33-adverbs.一人で':                  {'ja': '一人で りょこうに 行きました。',        'translation_en': 'I went on a trip alone.'},

    # Misc nouns
    'n5.vocab.37-common-nouns-miscella.さんぽ':   {'ja': 'こうえんで さんぽを しました。',        'translation_en': 'I took a walk in the park.'},
    'n5.vocab.37-common-nouns-miscella.くすり':   {'ja': 'びょういんで くすりを もらいました。', 'translation_en': 'I got medicine at the hospital.'},
    'n5.vocab.37-common-nouns-miscella.やすみ':   {'ja': '今日は やすみです。',                  'translation_en': 'Today is a holiday.'},
    'n5.vocab.37-common-nouns-miscella.ゆうべ':   {'ja': 'ゆうべは おそく まで しごとを しました。','translation_en': 'I worked late last night.'},
    'n5.vocab.37-common-nouns-miscella.テープレコーダー':{'ja': '古い テープレコーダーが あります。','translation_en': 'There\'s an old tape recorder.'},
}


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_third_example_final_b')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')
    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {e['id']: e for e in data['entries']}
    n = 0
    not_found = 0
    for vid, ex in THIRD.items():
        e = by_id.get(vid)
        if not e:
            not_found += 1
            print(f'  ! not found: {vid}')
            continue
        exs = e.get('examples') or []
        if len(exs) >= 3:
            continue
        exs.append({'ja': ex['ja'], 'translation_en': ex['translation_en'], 'provenance': 'llm_curated'})
        e['examples'] = exs
        n += 1
    print(f'\nFinal wave B added 3rd example on {n} entries. Not found: {not_found}.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
