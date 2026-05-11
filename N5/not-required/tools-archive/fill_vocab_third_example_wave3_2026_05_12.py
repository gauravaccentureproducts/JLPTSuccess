"""Wave 3 — extend 3rd vocab examples — next 60 by frequency_rank."""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

THIRD = {
    'n5.vocab.22-money-and-shopping.お金':         {'ja': 'お金が ありません。',                'translation_en': 'I don\'t have any money.'},
    'n5.vocab.32-adjectives.いや':                {'ja': 'あめが いやですね。',                 'translation_en': 'I don\'t like the rain.'},
    'n5.vocab.25-languages-and-countri.ドイツ':    {'ja': 'ドイツへ いって みたいです。',           'translation_en': 'I\'d like to visit Germany.'},
    'n5.vocab.24-school-and-study.え':            {'ja': '子どもが きれいな えを かきました。',     'translation_en': 'The child drew a beautiful picture.'},
    'n5.vocab.26-house-and-furniture.え':         {'ja': 'かべに 大きな えが あります。',          'translation_en': 'There is a big picture on the wall.'},
    'n5.vocab.28-verbs-group-2-verbs.出る':        {'ja': 'まいあさ 七時に いえを 出ます。',        'translation_en': 'I leave home at 7 AM every morning.'},
    'n5.vocab.13-locations-and-places-.駅':       {'ja': 'えきの まえで まって ください。',        'translation_en': 'Please wait in front of the station.'},
    'n5.vocab.22-money-and-shopping.ドル':         {'ja': '一ドルは いまの れーとで いくらですか。', 'translation_en': 'How much is one dollar at today\'s rate?'},
    'n5.vocab.25-languages-and-countri.フランス':  {'ja': 'フランス語を べんきょうしたいです。',    'translation_en': 'I want to study French.'},
    'n5.vocab.10-time-general.よる':              {'ja': 'よるは あまり 食べません。',            'translation_en': 'I don\'t eat much at night.'},
    'n5.vocab.10-time-general.午後':              {'ja': '午後 二時に 会いましょう。',            'translation_en': 'Let\'s meet at 2 PM.'},
    'n5.vocab.26-house-and-furniture.もん':       {'ja': 'がっこうの もんは 八時に しまります。',  'translation_en': 'The school gate closes at 8.'},
    'n5.vocab.14-nature-and-weather.火':          {'ja': '火を つけて ください。',               'translation_en': 'Please light the fire.'},
    'n5.vocab.13-locations-and-places-.ホテル':    {'ja': 'ホテルの レストランで 食べました。',    'translation_en': 'I ate at the hotel\'s restaurant.'},
    'n5.vocab.27-verbs-group-1-verbs.入る':        {'ja': 'いえに 入って ください。',             'translation_en': 'Please come into the house.'},
    'n5.vocab.31-adjectives.長い':                {'ja': '長い りょこうから かえりました。',      'translation_en': 'I returned from a long trip.'},
    'n5.vocab.14-nature-and-weather.花':          {'ja': 'はるは いろいろな 花が さきます。',     'translation_en': 'Various flowers bloom in spring.'},
    'n5.vocab.14-nature-and-weather.山':          {'ja': 'らいしゅう 山へ のぼります。',          'translation_en': 'I will climb the mountain next week.'},
    'n5.vocab.37-common-nouns-miscella.スポーツ':  {'ja': 'すきな スポーツは サッカーです。',     'translation_en': 'My favorite sport is soccer.'},
    'n5.vocab.31-adjectives.ほしい':              {'ja': '新しい くつが ほしいです。',           'translation_en': 'I want new shoes.'},
    'n5.vocab.13-locations-and-places-.とおり':    {'ja': 'この とおりは とても にぎやかです。',  'translation_en': 'This street is very lively.'},
    'n5.vocab.27-verbs-group-1-verbs.おく':       {'ja': 'かばんを いすの 上に おきました。',     'translation_en': 'I placed the bag on the chair.'},
    'n5.vocab.31-adjectives.大きい':              {'ja': '大きい こえで 話して ください。',      'translation_en': 'Please speak in a loud voice.'},
    'n5.vocab.27-verbs-group-1-verbs.聞く':       {'ja': 'わからないことは 先生に 聞きます。',    'translation_en': 'I ask the teacher about things I don\'t understand.'},
    'n5.vocab.23-transport.バス':                 {'ja': 'バスで 学校へ 行きます。',              'translation_en': 'I go to school by bus.'},
    'n5.vocab.2-people-family.母':                {'ja': '母は とても いそがしいです。',         'translation_en': 'My mother is very busy.'},
    'n5.vocab.14-nature-and-weather.雨':          {'ja': 'けさから ずっと 雨です。',              'translation_en': 'It\'s been raining since this morning.'},
    'n5.vocab.33-adverbs.きっと':                  {'ja': 'きっと いい てんきに なります。',     'translation_en': 'The weather will surely turn nice.'},
    'n5.vocab.25-languages-and-countri.イギリス':  {'ja': 'イギリスから てがみが きました。',     'translation_en': 'A letter came from the UK.'},
    'n5.vocab.13-locations-and-places-.高校':    {'ja': 'あには 高校の せんせいです。',         'translation_en': 'My older brother is a high-school teacher.'},
    'n5.vocab.30-verbs-existence-and-p.もらう':    {'ja': 'たんじょうびに プレゼントを もらいました。', 'translation_en': 'I received a present for my birthday.'},
    'n5.vocab.27-verbs-group-1-verbs.かかる':     {'ja': 'えきまで 十五分 かかります。',         'translation_en': 'It takes 15 minutes to the station.'},
    'n5.vocab.2-people-family.大人':              {'ja': '大人は 五百円です。',                  'translation_en': 'It\'s 500 yen for adults.'},
    'n5.vocab.13-locations-and-places-.左':      {'ja': 'つぎの しんごうを 左に まがって ください。','translation_en': 'Please turn left at the next traffic light.'},
    'n5.vocab.37-common-nouns-miscella.クラス':   {'ja': 'わたしの クラスは 二十人です。',       'translation_en': 'My class has 20 students.'},
    'n5.vocab.10-time-general.午前':              {'ja': '午前 中に かいぎが あります。',        'translation_en': 'There\'s a meeting in the morning.'},
    'n5.vocab.26-house-and-furniture.ドア':       {'ja': 'ドアを しめて ください。',             'translation_en': 'Please close the door.'},
    'n5.vocab.33-adverbs.ぜひ':                   {'ja': 'ぜひ いっしょに 来て ください。',       'translation_en': 'Please come with us by all means.'},
    'n5.vocab.33-adverbs.いっぱい':                {'ja': '食べものが テーブルに いっぱい あります。','translation_en': 'There is lots of food on the table.'},
    'n5.vocab.2-people-family.父':                {'ja': '父は あした かえって きます。',         'translation_en': 'My father will return tomorrow.'},
    'n5.vocab.27-verbs-group-1-verbs.買う':       {'ja': '新しい じてんしゃを 買いたいです。',    'translation_en': 'I want to buy a new bicycle.'},
    'n5.vocab.13-locations-and-places-.右':      {'ja': '右の ドアから 入って ください。',      'translation_en': 'Please enter through the right door.'},
    'n5.vocab.28-verbs-group-2-verbs.入れる':      {'ja': 'おちゃに さとうを 入れますか。',       'translation_en': 'Will you put sugar in the tea?'},
    'n5.vocab.24-school-and-study.テスト':       {'ja': 'らいしゅう 日本語の テストが あります。','translation_en': 'There is a Japanese test next week.'},
    'n5.vocab.14-nature-and-weather.空':          {'ja': '空が とても きれいですね。',           'translation_en': 'The sky is very beautiful, isn\'t it?'},
    'n5.vocab.26-house-and-furniture.カメラ':     {'ja': '新しい カメラを 買いました。',         'translation_en': 'I bought a new camera.'},
    'n5.vocab.26-house-and-furniture.ビデオ':     {'ja': 'こん夜 ビデオを 見ましょう。',          'translation_en': 'Let\'s watch a video tonight.'},
    'n5.vocab.13-locations-and-places-.北':      {'ja': '北の ほうへ あるいて ください。',      'translation_en': 'Please walk toward the north.'},
    'n5.vocab.28-verbs-group-2-verbs.食べる':      {'ja': 'まいあさ パンを 食べます。',           'translation_en': 'I eat bread every morning.'},
    'n5.vocab.23-transport.電車':                 {'ja': 'えきで 電車を まちます。',              'translation_en': 'I wait for the train at the station.'},
    'n5.vocab.2-people-family.かぞく':            {'ja': 'わたしの かぞくは よ人です。',          'translation_en': 'My family has four members.'},
    'n5.vocab.10-time-general.とけい':            {'ja': 'かべの とけいは 五時です。',           'translation_en': 'The wall clock shows 5 o\'clock.'},
    'n5.vocab.27-verbs-group-1-verbs.はしる':     {'ja': 'こうえんで はしりました。',             'translation_en': 'I ran in the park.'},
    'n5.vocab.11-time-days-weeks-month.週':      {'ja': 'こんしゅうは いそがしいです。',         'translation_en': 'This week is busy.'},
    'n5.vocab.25-languages-and-countri.スペイン':  {'ja': 'スペインへ 行ったことが あります。',   'translation_en': 'I have been to Spain.'},
    'n5.vocab.24-school-and-study.電気':         {'ja': '電気を けして ください。',             'translation_en': 'Please turn off the light.'},
    'n5.vocab.26-house-and-furniture.電気':       {'ja': 'へやの 電気が つきません。',           'translation_en': 'The light in the room doesn\'t turn on.'},
    'n5.vocab.31-adjectives.小さい':              {'ja': 'この くつは 小さいです。',            'translation_en': 'These shoes are small.'},
    'n5.vocab.10-time-general.半':                {'ja': '三時半に きて ください。',             'translation_en': 'Please come at 3:30.'},
    'n5.vocab.33-adverbs.すごく':                  {'ja': 'きょうは すごく さむいです。',          'translation_en': 'It\'s really cold today.'},
}


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_third_example_wave3')
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
    print(f'\nWave 3 added 3rd example on {n} more entries.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
