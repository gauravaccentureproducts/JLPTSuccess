"""Wave 5+6 — extend 3rd vocab examples — next 100 by frequency_rank."""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

THIRD = {
    'n5.vocab.26-house-and-furniture.テーブル':    {'ja': 'テーブルの 上に 本が あります。',         'translation_en': 'There is a book on the table.'},
    'n5.vocab.13-locations-and-places-.きょうしつ':{'ja': 'きょうしつで しずかに しましょう。',     'translation_en': 'Let\'s be quiet in the classroom.'},
    'n5.vocab.31-adjectives.かるい':              {'ja': 'この かばんは かるいです。',             'translation_en': 'This bag is light.'},
    'n5.vocab.2-people-family.おねえさん':         {'ja': 'おねえさんは どこに すんで いますか。',  'translation_en': 'Where does your older sister live?'},
    'n5.vocab.26-house-and-furniture.ピアノ':      {'ja': 'まいにち 三十分 ピアノを ひきます。',    'translation_en': 'I play piano for 30 minutes every day.'},
    'n5.vocab.28-verbs-group-2-verbs.わすれる':    {'ja': 'なまえを わすれて しまいました。',       'translation_en': 'I\'ve forgotten the name.'},
    'n5.vocab.40-misc-useful-items.コンサート':    {'ja': '土曜日に コンサートに 行きます。',       'translation_en': 'I\'m going to a concert on Saturday.'},
    'n5.vocab.24-school-and-study.ノート':        {'ja': '新しい ノートを 一さつ 買いました。',    'translation_en': 'I bought one new notebook.'},
    'n5.vocab.3-people-roles.会社員':              {'ja': '父は ぎんこうの 会社員です。',          'translation_en': 'My father is a bank employee.'},
    'n5.vocab.13-locations-and-places-.としょかん':{'ja': 'としょかんで しずかに 本を 読みます。',  'translation_en': 'I quietly read books at the library.'},
    'n5.vocab.21-clothing-and-accessor.ボタン':    {'ja': 'シャツの ボタンが とれました。',        'translation_en': 'A button came off my shirt.'},
    'n5.vocab.11-time-days-weeks-month.九日':      {'ja': '九日に 友だちと 会います。',             'translation_en': 'I\'m meeting a friend on the 9th.'},
    'n5.vocab.13-locations-and-places-.びょういん':{'ja': '父は びょういんで はたらいて います。',  'translation_en': 'My father works at a hospital.'},
    'n5.vocab.13-locations-and-places-.トイレ':    {'ja': 'トイレは どこですか。',                 'translation_en': 'Where is the toilet?'},
    'n5.vocab.27-verbs-group-1-verbs.まがる':     {'ja': 'つぎの かどを 左に まがって ください。', 'translation_en': 'Please turn left at the next corner.'},
    'n5.vocab.31-adjectives.ふとい':              {'ja': 'この えんぴつは ふといです。',          'translation_en': 'This pencil is thick.'},
    'n5.vocab.2-people-family.きょうだい':         {'ja': 'きょうだいが 三人 います。',             'translation_en': 'I have three siblings.'},
    'n5.vocab.2-people-family.お母さん':           {'ja': '田中さんの お母さんは しんせつですね。','translation_en': 'Tanaka-san\'s mother is kind, isn\'t she?'},
    'n5.vocab.30-verbs-existence-and-p.あげる':   {'ja': '友だちに プレゼントを あげました。',     'translation_en': 'I gave my friend a present.'},
    'n5.vocab.24-school-and-study.べんきょう':    {'ja': '日本語の べんきょうは たのしいです。',  'translation_en': 'Studying Japanese is fun.'},
    'n5.vocab.32-adjectives.しんせつ':             {'ja': 'あの 人は とても しんせつです。',       'translation_en': 'That person is very kind.'},
    'n5.vocab.33-adverbs.おおぜい':                 {'ja': 'こうえんに おおぜいの 人が います。',   'translation_en': 'There are many people in the park.'},
    'n5.vocab.13-locations-and-places-.ぎんこう':  {'ja': 'ぎんこうは 三時に しまります。',         'translation_en': 'The bank closes at 3 o\'clock.'},
    'n5.vocab.37-common-nouns-miscella.メートル':  {'ja': '百メートル 走りました。',                'translation_en': 'I ran 100 meters.'},
    'n5.vocab.17-food-items.そば':                {'ja': 'お昼ごはんに そばを 食べました。',       'translation_en': 'I ate soba for lunch.'},
    'n5.vocab.12-time-frequency-sequen.時々':     {'ja': '時々 母から 電話が きます。',            'translation_en': 'Sometimes a call comes from my mother.'},
    'n5.vocab.32-adjectives.けっこう':              {'ja': 'もう けっこうです。',                  'translation_en': 'That\'s enough, thank you.'},
    'n5.vocab.24-school-and-study.じゅぎょう':    {'ja': 'じゅぎょうは 九時から はじまります。',  'translation_en': 'Class starts at 9 o\'clock.'},
    'n5.vocab.13-locations-and-places-.ゆうびんきょく':{'ja': 'ゆうびんきょくで きってを 買いました。','translation_en': 'I bought stamps at the post office.'},
    'n5.vocab.31-adjectives.ほそい':              {'ja': 'ほそい かみで 書きました。',            'translation_en': 'I wrote on thin paper.'},
    'n5.vocab.11-time-days-weeks-month.日曜日':   {'ja': '日曜日は うちで 休みます。',             'translation_en': 'On Sunday I rest at home.'},
    'n5.vocab.2-people-family.りょうしん':         {'ja': 'りょうしんは おおさかに すんで います。','translation_en': 'My parents live in Osaka.'},
    'n5.vocab.11-time-days-weeks-month.二十日':   {'ja': '二十日に かいぎが あります。',           'translation_en': 'There is a meeting on the 20th.'},
    'n5.vocab.27-verbs-group-1-verbs.みがく':    {'ja': 'まいばん はを みがきます。',             'translation_en': 'I brush my teeth every night.'},
    'n5.vocab.13-locations-and-places-.じむしょ': {'ja': 'じむしょは 三かいに あります。',         'translation_en': 'The office is on the third floor.'},
    'n5.vocab.32-adjectives.べんり':              {'ja': 'この パソコンは とても べんりです。',   'translation_en': 'This computer is very convenient.'},
    'n5.vocab.27-verbs-group-1-verbs.うる':      {'ja': 'この 店は 本を うって います。',         'translation_en': 'This shop sells books.'},
    'n5.vocab.24-school-and-study.しゅくだい':    {'ja': '先生から しゅくだいを もらいました。',  'translation_en': 'I got homework from the teacher.'},
    'n5.vocab.11-time-days-weeks-month.今月':     {'ja': '今月は とても いそがしいです。',         'translation_en': 'This month is very busy.'},
    'n5.vocab.23-transport.タクシー':              {'ja': 'えきから タクシーで 行きました。',      'translation_en': 'I went by taxi from the station.'},
    'n5.vocab.3-people-roles.けいかん':            {'ja': 'けいかんに みちを 聞きました。',        'translation_en': 'I asked the policeman for directions.'},
    'n5.vocab.13-locations-and-places-.お店':    {'ja': 'この お店は とても 安いです。',         'translation_en': 'This shop is very cheap.'},
    'n5.vocab.11-time-days-weeks-month.週末':    {'ja': '週末は うちで 休みます。',               'translation_en': 'I rest at home on the weekend.'},
    'n5.vocab.31-adjectives.よわい':              {'ja': 'こん夜は からだが よわいです。',        'translation_en': 'I feel weak tonight.'},
    'n5.vocab.24-school-and-study.しけん':       {'ja': 'らいしゅう しけんが あります。',        'translation_en': 'There is an exam next week.'},
    'n5.vocab.33-adverbs.もうすこし':               {'ja': 'もうすこし 待って ください。',         'translation_en': 'Please wait a little more.'},
    'n5.vocab.2-people-family.そふ':              {'ja': 'そふは 八十才です。',                  'translation_en': 'My grandfather is 80 years old.'},
    'n5.vocab.24-school-and-study.ことば':       {'ja': 'この ことばの いみが わかりません。',   'translation_en': 'I don\'t understand this word.'},
    'n5.vocab.37-common-nouns-miscella.ことば':   {'ja': '日本語の ことばを ノートに 書きます。', 'translation_en': 'I write Japanese words in my notebook.'},
    'n5.vocab.23-transport.バイク':                {'ja': '兄は バイクで かよって います。',       'translation_en': 'My older brother commutes by motorbike.'},
    'n5.vocab.12-time-frequency-sequen.はじめて':  {'ja': 'はじめて 日本に 来ました。',             'translation_en': 'I came to Japan for the first time.'},
    'n5.vocab.10-time-general.こんや':            {'ja': 'こんや えいがを 見ましょう。',          'translation_en': 'Let\'s watch a movie tonight.'},
    'n5.vocab.13-locations-and-places-.きっさてん':{'ja': 'きっさてんで 友だちと 話しました。',  'translation_en': 'I chatted with a friend at a cafe.'},
    'n5.vocab.27-verbs-group-1-verbs.もっていく':  {'ja': '会社に お弁当を もっていきます。',     'translation_en': 'I take a bento to work.'},
    'n5.vocab.26-house-and-furniture.ベッド':     {'ja': '新しい ベッドを 買いました。',          'translation_en': 'I bought a new bed.'},
    'n5.vocab.11-time-days-weeks-month.しゅうまつ':{'ja': 'しゅうまつは 友だちと 出かけます。',  'translation_en': 'I go out with friends on weekends.'},
    'n5.vocab.32-adjectives.ふべん':              {'ja': 'この いえは バスが ないので、ふべんです。','translation_en': 'This house has no bus service, so it\'s inconvenient.'},
    'n5.vocab.24-school-and-study.しつもん':      {'ja': 'しつもんが あったら、聞いて ください。','translation_en': 'If you have questions, please ask.'},
    'n5.vocab.11-time-days-weeks-month.土曜日':   {'ja': '土曜日に かいものに 行きます。',         'translation_en': 'I\'ll go shopping on Saturday.'},
    'n5.vocab.31-adjectives.うれしい':             {'ja': 'プレゼントを もらって、とても うれしいです。', 'translation_en': 'I got a present, and I\'m very happy.'},
    'n5.vocab.13-locations-and-places-.やおや':   {'ja': 'やおやで やさいを 買いました。',         'translation_en': 'I bought vegetables at the greengrocer.'},
    'n5.vocab.31-adjectives.からい':              {'ja': 'この カレーは とても からいです。',     'translation_en': 'This curry is very spicy.'},
    'n5.vocab.12-time-frequency-sequen.たまに':   {'ja': 'たまに 母に 電話します。',               'translation_en': 'Occasionally I call my mother.'},
    'n5.vocab.3-people-roles.高校生':              {'ja': 'おとうとは 高校生です。',              'translation_en': 'My younger brother is a high school student.'},
    'n5.vocab.13-locations-and-places-.カフェ':   {'ja': 'カフェで 友だちを 待ちます。',          'translation_en': 'I\'ll wait for my friend at the cafe.'},
    'n5.vocab.27-verbs-group-1-verbs.飲む':       {'ja': 'まいあさ ジュースを 飲みます。',        'translation_en': 'I drink juice every morning.'},
    'n5.vocab.31-adjectives.かわいい':             {'ja': 'かわいい ねこですね。',                'translation_en': 'What a cute cat!'},
    'n5.vocab.24-school-and-study.ひらがな':      {'ja': 'まず ひらがなを おぼえましょう。',     'translation_en': 'First, let\'s learn hiragana.'},
    'n5.vocab.37-common-nouns-miscella.へん':    {'ja': 'この へんに ぎんこうは ありますか。',  'translation_en': 'Is there a bank around here?'},
    'n5.vocab.13-locations-and-places-.ほんや':   {'ja': 'えきの ちかくの ほんやで 本を 買いました。','translation_en': 'I bought a book at the bookstore near the station.'},
    'n5.vocab.27-verbs-group-1-verbs.立つ':       {'ja': '電車では 立って いました。',             'translation_en': 'I was standing on the train.'},
    'n5.vocab.4-body-parts.みみ':                  {'ja': 'みみが いたいです。',                   'translation_en': 'My ears hurt.'},
    'n5.vocab.12-time-frequency-sequen.まいあさ': {'ja': 'まいあさ ジョギングを します。',        'translation_en': 'I go jogging every morning.'},
    'n5.vocab.14-nature-and-weather.みずうみ':    {'ja': 'みずうみで さかなを つります。',        'translation_en': 'I fish at the lake.'},
    'n5.vocab.16-food-and-drink-genera.たべもの': {'ja': 'にほんの たべものは おいしいです。',    'translation_en': 'Japanese food is delicious.'},
    'n5.vocab.22-money-and-shopping.ねだん':       {'ja': 'この くつの ねだんは いくらですか。',    'translation_en': 'What is the price of these shoes?'},
    'n5.vocab.25-languages-and-countri.えいご':   {'ja': 'えいごの 先生は アメリカ人です。',      'translation_en': 'The English teacher is American.'},
    'n5.vocab.26-house-and-furniture.かいだん':   {'ja': 'かいだんを 上がって ください。',        'translation_en': 'Please go up the stairs.'},
    'n5.vocab.28-verbs-group-2-verbs.ならべる':    {'ja': 'テーブルに おさらを ならべました。',    'translation_en': 'I lined up plates on the table.'},
    'n5.vocab.27-verbs-group-1-verbs.もってくる': {'ja': 'あした しゅくだいを もってきて ください。','translation_en': 'Please bring your homework tomorrow.'},
    'n5.vocab.31-adjectives.おもしろい':           {'ja': 'おもしろい 本を 読みました。',           'translation_en': 'I read an interesting book.'},
    'n5.vocab.13-locations-and-places-.はなや':   {'ja': 'はなやで 花を 三本 買いました。',       'translation_en': 'I bought three flowers at the flower shop.'},
    'n5.vocab.32-adjectives.ゆうめい':             {'ja': 'この レストランは とても ゆうめいです。','translation_en': 'This restaurant is very famous.'},
    'n5.vocab.24-school-and-study.ぶんしょう':    {'ja': '長い ぶんしょうを 書きました。',        'translation_en': 'I wrote a long composition.'},
    'n5.vocab.33-adverbs.ほんとうに':              {'ja': 'ほんとうに ありがとうございます。',      'translation_en': 'Thank you very much, truly.'},
    'n5.vocab.11-time-days-weeks-month.きょねん': {'ja': 'きょねん 日本に 来ました。',             'translation_en': 'I came to Japan last year.'},
    'n5.vocab.31-adjectives.にがい':              {'ja': 'この コーヒーは にがいですね。',         'translation_en': 'This coffee is bitter, isn\'t it?'},
    'n5.vocab.1-people-pronouns-and-se.かた':     {'ja': 'あの かたは どなたですか。',             'translation_en': 'Who is that person (polite)?'},
    'n5.vocab.37-common-nouns-miscella.かた':     {'ja': 'たべかたを おしえて ください。',         'translation_en': 'Please teach me how to eat this.'},
    'n5.vocab.17-food-items.ラーメン':             {'ja': 'ラーメンを 一杯 食べました。',          'translation_en': 'I ate a bowl of ramen.'},
    'n5.vocab.26-house-and-furniture.ギター':     {'ja': '兄は ギターを ひきます。',              'translation_en': 'My older brother plays the guitar.'},
    'n5.vocab.3-people-roles.りゅうがくせい':      {'ja': '中国からの りゅうがくせいです。',        'translation_en': 'I\'m an international student from China.'},
    'n5.vocab.24-school-and-study.かな':          {'ja': 'かなを 全部 おぼえました。',             'translation_en': 'I memorized all the kana.'},
    'n5.vocab.13-locations-and-places-.にくや':   {'ja': 'にくやで ぶたにくを 買いました。',      'translation_en': 'I bought pork at the butcher.'},
    'n5.vocab.24-school-and-study.ぶんぽう':      {'ja': '日本語の ぶんぽうは むずかしいです。',  'translation_en': 'Japanese grammar is difficult.'},
    'n5.vocab.17-food-items.カレー':              {'ja': '今夜の ばんごはんは カレーです。',      'translation_en': 'Tonight\'s dinner is curry.'},
    'n5.vocab.33-adverbs.だいたい':                {'ja': '駅まで だいたい 十分です。',             'translation_en': 'It\'s about 10 minutes to the station.'},
    'n5.vocab.13-locations-and-places-.ビル':    {'ja': 'この ビルは 二十かい あります。',       'translation_en': 'This building has 20 floors.'},
    'n5.vocab.13-locations-and-places-.パンや':   {'ja': 'パンやで しょくパンを 買いました。',     'translation_en': 'I bought a loaf at the bakery.'},
    'n5.vocab.37-common-nouns-miscella.レコード':{'ja': '父は 古い レコードを たくさん もっています。', 'translation_en': 'My father has many old records.'},
}


def main() -> int:
    fp = ROOT / 'data' / 'vocab.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_third_example_wave56')
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
    print(f'\nWaves 5+6 added 3rd example on {n} more entries.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
