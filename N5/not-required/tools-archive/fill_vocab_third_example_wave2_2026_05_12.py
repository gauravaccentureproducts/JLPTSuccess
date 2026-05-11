"""Wave 2 — extend 3rd vocab examples to ~90 total.

Wave 1 (2026-05-11) authored a 3rd example on the top-40 highest-
frequency entries. This wave covers the next 50 entries by
frequency_rank ascending.

Same schema as wave 1.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

THIRD = {
    'n5.vocab.12-time-frequency-sequen.もう':       {'ja': 'もう ばんごはんを 食べました。',          'translation_en': 'I have already eaten dinner.'},
    'n5.vocab.33-adverbs.もう':                    {'ja': 'もう すこし 待って ください。',            'translation_en': 'Please wait a little more.'},
    'n5.vocab.12-time-frequency-sequen.よく':      {'ja': 'この みせには よく 行きます。',            'translation_en': 'I often go to this shop.'},
    'n5.vocab.33-adverbs.ちょっと':                  {'ja': 'ちょっと 待って ください。',               'translation_en': 'Please wait a moment.'},
    'n5.vocab.33-adverbs.ただ':                    {'ja': 'ただの しゃしんですよ。',                 'translation_en': 'It\'s just a photograph.'},
    'n5.vocab.33-adverbs.やはり':                   {'ja': 'やはり 日本食が いちばん 好きです。',       'translation_en': 'After all, I like Japanese food the most.'},
    'n5.vocab.13-locations-and-places-.大学':      {'ja': '大学で 日本語を べんきょうして います。',    'translation_en': 'I study Japanese at university.'},
    'n5.vocab.33-adverbs.とても':                   {'ja': 'この えいがは とても おもしろいです。',     'translation_en': 'This movie is very interesting.'},
    'n5.vocab.24-school-and-study.電話':            {'ja': 'あした 電話して ください。',              'translation_en': 'Please call me tomorrow.'},
    'n5.vocab.27-verbs-group-1-verbs.行く':         {'ja': 'らいねん 日本へ 行きたいです。',           'translation_en': 'I want to go to Japan next year.'},
    'n5.vocab.14-nature-and-weather.いけ':         {'ja': 'こうえんの いけに さかなが います。',       'translation_en': 'There are fish in the park pond.'},
    'n5.vocab.33-adverbs.もちろん':                  {'ja': 'もちろん、いっしょに 行きますよ。',         'translation_en': 'Of course I\'ll go with you.'},
    'n5.vocab.31-adjectives.新しい':                {'ja': '新しい いえに ひっこしました。',          'translation_en': 'I moved into a new house.'},
    'n5.vocab.33-adverbs.一番':                    {'ja': 'あおが 一番 好きな いろです。',          'translation_en': 'Blue is my favorite color.'},
    'n5.vocab.31-adjectives.高い':                 {'ja': 'この くつは 高いです。',                'translation_en': 'These shoes are expensive.'},
    'n5.vocab.33-adverbs.もっと':                   {'ja': 'もっと べんきょうしましょう。',             'translation_en': 'Let\'s study more.'},
    'n5.vocab.33-adverbs.まず':                    {'ja': 'まず 手を あらいましょう。',              'translation_en': 'First, let\'s wash our hands.'},
    'n5.vocab.2-people-family.男':                {'ja': 'あの 男の 人は 父です。',               'translation_en': 'That man is my father.'},
    'n5.vocab.13-locations-and-places-.下':       {'ja': 'つくえの 下に かばんが あります。',        'translation_en': 'There is a bag under the desk.'},
    'n5.vocab.12-time-frequency-sequen.いつも':     {'ja': 'いつも 朝 七時に おきます。',           'translation_en': 'I always wake up at 7 AM.'},
    'n5.vocab.23-transport.車':                   {'ja': '車で かいしゃに 行きます。',              'translation_en': 'I go to work by car.'},
    'n5.vocab.40-misc-useful-items.ほう':          {'ja': '右の ほうへ いって ください。',            'translation_en': 'Please go to the right side.'},
    'n5.vocab.25-languages-and-countri.日本人':     {'ja': '兄の 友だちは 日本人です。',             'translation_en': 'My brother\'s friend is Japanese.'},
    'n5.vocab.30-verbs-existence-and-p.くれる':     {'ja': '父が 本を くれました。',                'translation_en': 'My father gave me a book.'},
    'n5.vocab.26-house-and-furniture.いえ':        {'ja': 'いえの まえに 大きな 木が あります。',      'translation_en': 'There is a big tree in front of the house.'},
    'n5.vocab.12-time-frequency-sequen.あまり':    {'ja': 'コーヒーは あまり 飲みません。',           'translation_en': 'I don\'t drink coffee much.'},
    'n5.vocab.12-time-frequency-sequen.すぐ':     {'ja': 'すぐ 行きます。 待って いて ください。',    'translation_en': 'I\'ll come right away — please wait.'},
    'n5.vocab.33-adverbs.すぐ':                    {'ja': 'すぐ こたえて ください。',               'translation_en': 'Please answer right away.'},
    'n5.vocab.11-time-days-weeks-month.今年':      {'ja': '今年は とても さむかったです。',          'translation_en': 'This year was very cold.'},
    'n5.vocab.37-common-nouns-miscella.ニュース':  {'ja': 'あさ テレビで ニュースを 見ます。',         'translation_en': 'I watch the news on TV in the morning.'},
    'n5.vocab.26-house-and-furniture.テレビ':       {'ja': 'テレビが こわれました。',                'translation_en': 'The TV broke.'},
    'n5.vocab.13-locations-and-places-.道':       {'ja': 'この 道を まっすぐ 行って ください。',      'translation_en': 'Please go straight along this road.'},
    'n5.vocab.23-transport.道':                   {'ja': '道が とても こんで います。',             'translation_en': 'The road is very crowded.'},
    'n5.vocab.1-people-pronouns-and-se.みんな':    {'ja': 'みんな いっしょに 食べましょう。',          'translation_en': 'Let\'s all eat together.'},
    'n5.vocab.2-people-family.子ども':             {'ja': '子どもが こうえんで あそんで います。',     'translation_en': 'The children are playing in the park.'},
    'n5.vocab.37-common-nouns-miscella.ゲーム':   {'ja': 'まいばん 子どもが ゲームを します。',       'translation_en': 'Every night the kids play games.'},
    'n5.vocab.30-verbs-existence-and-p.やる':      {'ja': 'いっしょに サッカーを やりませんか。',      'translation_en': 'Want to play soccer together?'},
    'n5.vocab.26-house-and-furniture.いま':        {'ja': 'いまで テレビを 見ます。',                'translation_en': 'I watch TV in the living room.'},
    'n5.vocab.13-locations-and-places-.外':       {'ja': '外で あそびましょう。',                  'translation_en': 'Let\'s play outside.'},
    'n5.vocab.33-adverbs.たくさん':                  {'ja': 'たくさん たべて ください。',               'translation_en': 'Please eat a lot.'},
    'n5.vocab.3-people-roles.学生':                {'ja': '兄は 大学の 学生です。',                'translation_en': 'My older brother is a university student.'},
    'n5.vocab.27-verbs-group-1-verbs.読む':         {'ja': 'まいばん 本を 読みます。',                'translation_en': 'I read a book every night.'},
    'n5.vocab.24-school-and-study.新聞':           {'ja': '父は 毎朝 新聞を 読みます。',             'translation_en': 'My father reads the newspaper every morning.'},
    'n5.vocab.12-time-frequency-sequen.毎日':     {'ja': '毎日 日本語を べんきょうします。',         'translation_en': 'I study Japanese every day.'},
    'n5.vocab.27-verbs-group-1-verbs.書く':         {'ja': 'てがみを 書いて ください。',               'translation_en': 'Please write a letter.'},
    'n5.vocab.25-languages-and-countri.日本語':     {'ja': '日本語は おもしろいです。',               'translation_en': 'Japanese is interesting.'},
    'n5.vocab.37-common-nouns-miscella.ほか':     {'ja': 'ほかに 何か ありますか。',                'translation_en': 'Is there anything else?'},
    'n5.vocab.2-people-family.女':                {'ja': 'あの 女の 人は 母の 友だちです。',         'translation_en': 'That woman is my mother\'s friend.'},
    'n5.vocab.14-nature-and-weather.木':          {'ja': 'こうえんに 木が たくさん あります。',       'translation_en': 'There are many trees in the park.'},
    'n5.vocab.25-languages-and-countri.外国':     {'ja': '外国へ いって みたいです。',              'translation_en': 'I\'d like to try going to a foreign country.'},
}


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_third_example_wave2')
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
    print(f'\nWave 2 added 3rd example on {n} more vocab entries.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
