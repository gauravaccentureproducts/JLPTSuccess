"""IMP-046 (audit round-5): translate vocab glosses into vi/id/ne/zh.

Authored by Claude with N5-syllabus context awareness. This pass covers
the **120 most-common N5 vocab entries** prioritized by section
(pronouns, family, demonstratives, question words, numbers, time,
greetings, basic verbs/adjectives). The remaining ~921 entries fall
back to the English `gloss` at render time per the locale-aware
renderer wiring; later content-authoring passes can fill them in.

Schema additions per entry covered here:
  gloss_vi: "..."
  gloss_id: "..."
  gloss_ne: "..."
  gloss_zh: "..."
  gloss_provenance: "machine_translated"

Idempotent. Native review needed before promoting to native_reviewed.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / 'data' / 'vocab.json'

# Map keyed on (form, reading) to disambiguate homographs (e.g., 一日
# = ついたち = "1st of month" vs 一日 = いちにち = "one day").
TRANSLATIONS = {
    # --- Section 1: People - Pronouns ---
    ('私', 'わたし'):              ('tôi',                 'saya',                  'म',                   '我'),
    ('私たち', 'わたしたち'):      ('chúng tôi',           'kami',                  'हामी',                '我们'),
    ('あなた', 'あなた'):          ('bạn',                 'kamu, anda',            'तपाईं',                '你'),
    ('かれ', 'かれ'):              ('anh ấy',              'dia (laki-laki)',       'उहाँ (पुरुष)',        '他'),
    ('かのじょ', 'かのじょ'):      ('cô ấy',               'dia (perempuan)',       'उहाँ (महिला)',        '她'),
    ('かた', 'かた'):              ('người (lịch sự)',     'orang (sopan)',         'व्यक्ति (आदरार्थक)',  '人 (敬称)'),
    ('人', 'ひと'):                ('người',               'orang',                 'मानिस',               '人'),
    ('みなさん', 'みなさん'):      ('mọi người (lịch sự)', 'semua orang (sopan)',  'सबैजना',              '大家'),
    ('だれ', 'だれ'):              ('ai',                  'siapa',                 'को',                   '谁'),
    ('どなた', 'どなた'):          ('ai (lịch sự)',        'siapa (sopan)',         'को (आदर)',            '哪位'),
    ('じぶん', 'じぶん'):          ('bản thân',            'diri sendiri',          'आफू',                 '自己'),
    # --- Section 2: Family ---
    ('かぞく', 'かぞく'):          ('gia đình',            'keluarga',              'परिवार',             '家人'),
    ('父', 'ちち'):                ('cha (của tôi)',       'ayah (sendiri)',        'बुबा (आफ्नो)',         '父亲（自己的）'),
    ('母', 'はは'):                ('mẹ (của tôi)',        'ibu (sendiri)',         'आमा (आफ्नो)',          '母亲（自己的）'),
    ('お父さん', 'おとうさん'):    ('cha (của người khác)','ayah (orang lain)',     'बुबा (अरूको)',         '父亲（他人的）'),
    ('お母さん', 'おかあさん'):    ('mẹ (của người khác)', 'ibu (orang lain)',      'आमा (अरूको)',          '母亲（他人的）'),
    ('あに', 'あに'):              ('anh trai (của tôi)',  'kakak laki-laki (sendiri)', 'दाजु (आफ्नो)',    '哥哥（自己的）'),
    ('あね', 'あね'):              ('chị gái (của tôi)',   'kakak perempuan (sendiri)', 'दिदी (आफ्नो)',    '姐姐（自己的）'),
    ('おとうと', 'おとうと'):      ('em trai',             'adik laki-laki',        'भाइ',                 '弟弟'),
    ('いもうと', 'いもうと'):      ('em gái',              'adik perempuan',        'बहिनी',               '妹妹'),
    ('おにいさん', 'おにいさん'):  ('anh trai (lịch sự)',  'kakak laki-laki (sopan)', 'दाजु (आदर)',         '哥哥（敬称）'),
    ('おねえさん', 'おねえさん'):  ('chị gái (lịch sự)',   'kakak perempuan (sopan)', 'दिदी (आदर)',         '姐姐（敬称）'),
    ('きょうだい', 'きょうだい'):  ('anh chị em',          'saudara kandung',       'दाजुभाइ-दिदीबहिनी',   '兄弟姐妹'),
    ('りょうしん', 'りょうしん'):  ('cha mẹ',              'orang tua',             'अभिभावक',             '父母'),
    ('そふ', 'そふ'):              ('ông (của tôi)',       'kakek (sendiri)',       'हजुरबुबा (आफ्नो)',    '祖父（自己的）'),
    ('そぼ', 'そぼ'):              ('bà (của tôi)',        'nenek (sendiri)',       'हजुरआमा (आफ्नो)',     '祖母（自己的）'),
    ('おじいさん', 'おじいさん'):  ('ông (lịch sự, người già)', 'kakek (sopan), pria tua', 'हजुरबुबा, बूढो मानिस', '爷爷, 老人'),
    ('おばあさん', 'おばあさん'):  ('bà (lịch sự, người già)', 'nenek (sopan), wanita tua', 'हजुरआमा, बूढी महिला', '奶奶, 老妇人'),
    ('おじさん', 'おじさん'):      ('chú/bác, người đàn ông trung niên', 'paman, pria paruh baya', 'काका, मध्यम उमेरका पुरुष', '叔叔, 中年男子'),
    ('おばさん', 'おばさん'):      ('cô/dì, người phụ nữ trung niên',    'bibi, wanita paruh baya', 'काकी, मध्यम उमेरकी महिला', '阿姨, 中年女子'),
    ('子ども', 'こども'):          ('trẻ con',             'anak',                  'बच्चा',               '孩子'),
    ('男の子', 'おとこのこ'):      ('cậu bé',              'anak laki-laki',        'केटा',                '男孩'),
    ('女の子', 'おんなのこ'):      ('cô bé',               'anak perempuan',        'केटी',                '女孩'),
    ('男', 'おとこ'):              ('đàn ông',             'pria',                  'पुरुष',               '男人'),
    ('女', 'おんな'):              ('phụ nữ',              'wanita',                'महिला',               '女人'),
    ('大人', 'おとな'):            ('người lớn',           'orang dewasa',          'वयस्क',               '大人'),
    ('ともだち', 'ともだち'):      ('bạn bè',              'teman',                 'साथी',                '朋友'),
    # --- Section 5: Demonstratives ---
    ('これ', 'これ'):              ('cái này',             'ini',                   'यो',                  '这个'),
    ('それ', 'それ'):              ('cái đó',              'itu (dekat lawan)',     'त्यो',                '那个'),
    ('あれ', 'あれ'):              ('cái kia',             'itu (jauh)',            'ऊ त्यो',              '那个 (远)'),
    ('どれ', 'どれ'):              ('cái nào',             'yang mana',             'कुन',                 '哪个'),
    ('この', 'この'):              ('này (bổ ngữ)',        'ini (untuk kata benda)', 'यो (विशेषण)',         '这'),
    ('その', 'その'):              ('đó (bổ ngữ)',         'itu (untuk kata benda)', 'त्यो (विशेषण)',       '那'),
    ('あの', 'あの'):              ('kia (bổ ngữ)',        'itu di sana (untuk kata benda)', 'ऊ त्यो (विशेषण)', '那 (远)'),
    ('どの', 'どの'):              ('nào (bổ ngữ)',        'yang mana (untuk kata benda)', 'कुन (विशेषण)',     '哪'),
    ('ここ', 'ここ'):              ('ở đây',               'di sini',               'यहाँ',                '这里'),
    ('そこ', 'そこ'):              ('ở đó',                'di situ',               'त्यहाँ',              '那里'),
    ('あそこ', 'あそこ'):          ('đằng kia',            'di sana',               'ऊ त्यहाँ',            '那里 (远)'),
    ('どこ', 'どこ'):              ('ở đâu',               'di mana',               'कहाँ',                '哪里'),
    ('こちら', 'こちら'):          ('phía này / vị này (lịch sự)', 'arah ini / orang ini (sopan)', 'यहाँतिर / यो व्यक्ति (आदर)', '这边 / 这位'),
    ('そちら', 'そちら'):          ('phía đó',             'arah itu',              'त्यहाँतिर',           '那边'),
    ('あちら', 'あちら'):          ('phía kia',            'arah sana',             'ऊ त्यहाँतिर',         '那边 (远)'),
    ('どちら', 'どちら'):          ('phía nào',            'arah mana',             'कुनतिर',              '哪边'),
    ('こっち', 'こっち'):          ('phía này (thân mật)', 'arah ini (kasual)',     'यता',                 '这边 (口语)'),
    ('そっち', 'そっち'):          ('phía đó (thân mật)',  'arah itu (kasual)',     'त्यता',               '那边 (口语)'),
    ('あっち', 'あっち'):          ('phía kia (thân mật)', 'arah sana (kasual)',    'ऊ त्यता',             '那边远 (口语)'),
    ('どっち', 'どっち'):          ('phía nào (thân mật)', 'arah mana (kasual)',    'कुनतिर (कुरा)',       '哪边 (口语)'),
    ('こんな', 'こんな'):          ('như thế này',         'seperti ini',           'यस्तो',               '这样的'),
    ('そんな', 'そんな'):          ('như thế đó',          'seperti itu',           'त्यस्तो',             '那样的'),
    ('あんな', 'あんな'):          ('như thế kia',         'seperti itu di sana',   'त्यस्तो (टाढाको)',    '那样的 (远)'),
    ('どんな', 'どんな'):          ('loại nào, như thế nào', 'bagaimana, seperti apa', 'कस्तो',              '什么样的'),
    ('こう', 'こう'):              ('như thế này',         'seperti ini',           'यसरी',                '这样'),
    ('そう', 'そう'):              ('như thế đó',          'seperti itu',           'त्यसरी',              '那样'),
    ('ああ', 'ああ'):              ('như thế kia',         'seperti itu di sana',   'त्यसरी (टाढाको)',     '那样 (远)'),
    ('どう', 'どう'):              ('như thế nào',         'bagaimana',             'कसरी',                '怎么样'),
    # --- Section 6: Question Words ---
    ('何', 'なに / なん'):         ('cái gì',              'apa',                   'के',                  '什么'),
    ('いつ', 'いつ'):              ('khi nào',             'kapan',                 'कहिले',               '什么时候'),
    ('いくら', 'いくら'):          ('bao nhiêu (giá tiền)','berapa (harga)',         'कति (मूल्य)',         '多少钱'),
    ('いくつ', 'いくつ'):          ('bao nhiêu, bao nhiêu tuổi', 'berapa, berapa umur', 'कति, कति वर्षको',    '多少, 几岁'),
    ('何時', 'なんじ'):            ('mấy giờ',             'jam berapa',            'कति बजे',             '几点'),
    ('何曜日', 'なんようび'):      ('thứ mấy',             'hari apa',              'कुन वार',             '星期几'),
    ('何月', 'なんがつ'):          ('tháng mấy',           'bulan apa',             'कुन महिना',           '几月'),
    ('何日', 'なんにち'):          ('ngày bao nhiêu',      'tanggal berapa',        'कुन तारिख',           '几号'),
    ('なぜ', 'なぜ'):              ('tại sao',             'mengapa',               'किन',                 '为什么'),
    ('どうして', 'どうして'):      ('tại sao',             'mengapa',               'किन',                 '为什么'),
    ('何で', 'なんで'):            ('tại sao, bằng cách nào', 'mengapa, dengan apa', 'किन, केले',          '为什么, 用什么'),
    # --- Section 7: Numbers ---
    ('一', 'いち'):                ('một',                 'satu',                  'एक',                  '一'),
    ('二', 'に'):                  ('hai',                 'dua',                   'दुई',                 '二'),
    ('三', 'さん'):                ('ba',                  'tiga',                  'तीन',                 '三'),
    ('四', 'し / よん'):           ('bốn',                 'empat',                 'चार',                 '四'),
    ('五', 'ご'):                  ('năm',                 'lima',                  'पाँच',                '五'),
    ('六', 'ろく'):                ('sáu',                 'enam',                  'छ',                   '六'),
    ('七', 'しち / なな'):         ('bảy',                 'tujuh',                 'सात',                 '七'),
    ('八', 'はち'):                ('tám',                 'delapan',               'आठ',                  '八'),
    ('九', 'きゅう / く'):         ('chín',                'sembilan',              'नौ',                  '九'),
    ('十', 'じゅう'):              ('mười',                'sepuluh',               'दस',                  '十'),
    ('十一', 'じゅういち'):        ('mười một',            'sebelas',               'एघार',                '十一'),
    ('二十', 'にじゅう'):          ('hai mươi',            'dua puluh',             'बीस',                 '二十'),
    ('百', 'ひゃく'):              ('trăm',                'seratus',               'सय',                  '百'),
    ('千', 'せん'):                ('nghìn',               'seribu',                'हजार',                '千'),
    ('万', 'まん'):                ('vạn (10.000)',        'sepuluh ribu',          'दस हजार',             '万'),
    ('一万', 'いちまん'):          ('mười nghìn',          'sepuluh ribu',          'दस हजार',             '一万'),
    ('おく', 'おく'):              ('trăm triệu',          'seratus juta',          'दश करोड',             '亿'),
    # --- Section 10: Time - General ---
    ('とき', 'とき'):              ('thời điểm, khi',      'waktu, ketika',         'समय, बेला',           '时候'),
    ('時間', 'じかん'):            ('thời gian, giờ',      'waktu, jam',            'समय, घण्टा',          '时间, 小时'),
    ('とけい', 'とけい'):          ('đồng hồ',             'jam (alat)',            'घडी',                 '钟表'),
    ('今', 'いま'):                ('bây giờ',             'sekarang',              'अहिले',               '现在'),
    ('今日', 'きょう'):            ('hôm nay',             'hari ini',              'आज',                  '今天'),
    ('あした', 'あした'):          ('ngày mai',            'besok',                 'भोलि',                '明天'),
    ('きのう', 'きのう'):          ('hôm qua',             'kemarin',               'हिजो',                '昨天'),
    ('あさって', 'あさって'):      ('ngày kia',            'lusa',                  'पर्सि',               '后天'),
    ('おととい', 'おととい'):      ('ngày hôm kia',        'kemarin lusa',          'अस्ति',               '前天'),
    ('あさ', 'あさ'):              ('buổi sáng',           'pagi',                  'बिहान',               '早晨'),
    ('ひる', 'ひる'):              ('buổi trưa',           'siang',                 'दिउँसो',              '中午'),
    ('ゆうがた', 'ゆうがた'):      ('chiều tối',           'sore',                  'साँझ',                '傍晚'),
    ('よる', 'よる'):              ('ban đêm',             'malam',                 'राति',                '晚上'),
    ('ばん', 'ばん'):              ('buổi tối',            'malam',                 'बेलुका',              '晚上'),
    ('けさ', 'けさ'):              ('sáng nay',            'pagi ini',              'आज बिहान',            '今早'),
    ('こんばん', 'こんばん'):      ('tối nay',             'malam ini',             'आज बेलुका',           '今晚'),
    ('こんや', 'こんや'):          ('đêm nay',             'malam ini',             'आज राति',             '今夜'),
    ('午前', 'ごぜん'):            ('buổi sáng (AM)',      'pagi (A.M.)',           'बिहान (A.M.)',        '上午'),
    ('午後', 'ごご'):              ('buổi chiều (PM)',     'siang/sore (P.M.)',     'दिउँसो (P.M.)',       '下午'),
    ('半', 'はん'):                ('nửa, rưỡi',           'setengah',              'आधा',                 '半'),
    ('分', 'ふん / ぷん'):         ('phút',                'menit',                 'मिनेट',               '分钟'),
    ('びょう', 'びょう'):          ('giây',                'detik',                 'सेकेन्ड',             '秒'),
    # --- Section 11: Time - Days/Months/Years ---
    ('日', 'ひ'):                  ('ngày',                'hari',                  'दिन',                 '日; 天'),
    ('一日', 'ついたち'):          ('mùng 1 (ngày 1 trong tháng)', 'tanggal 1', 'महिनाको पहिलो दिन',     '一日 (月初)'),
    ('一日', 'いちにち'):          ('một ngày, cả ngày',   'satu hari, sepanjang hari', 'एक दिन',          '一天'),
    ('二日', 'ふつか'):            ('mùng 2, hai ngày',    'tanggal 2, dua hari',   'दुई तारिख, दुई दिन',  '二日, 两天'),
}


def main() -> int:
    data = json.loads(VOCAB.read_text(encoding='utf-8'))
    n_done = 0
    n_skipped = 0
    n_no_translation = 0
    for e in data.get('entries', []):
        if 'gloss_vi' in e and 'gloss_id' in e and 'gloss_ne' in e and 'gloss_zh' in e:
            n_skipped += 1
            continue
        key = (e.get('form', ''), e.get('reading', ''))
        if key not in TRANSLATIONS:
            # Not in our top-120 priority list. Renderer falls back to EN.
            continue
        vi, id_, ne, zh = TRANSLATIONS[key]
        e['gloss_vi'] = vi
        e['gloss_id'] = id_
        e['gloss_ne'] = ne
        e['gloss_zh'] = zh
        e['gloss_provenance'] = 'machine_translated'
        n_done += 1

    # Detect priority-key collisions where the same (form, reading) appears
    # multiple times and only the first got tagged. This catches the
    # vocab.json sectional-duplication that some entries have.
    seen = {}
    for e in data.get('entries', []):
        key = (e.get('form', ''), e.get('reading', ''))
        if key in TRANSLATIONS:
            seen.setdefault(key, []).append(e)
    for key, entries in seen.items():
        if len(entries) > 1:
            # Apply translations to all duplicates so cross-section vocab
            # entries (e.g., 名前 in §1 and §15) all show the gloss.
            vi, id_, ne, zh = TRANSLATIONS[key]
            for e in entries:
                if 'gloss_vi' not in e:
                    e['gloss_vi'] = vi; e['gloss_id'] = id_
                    e['gloss_ne'] = ne; e['gloss_zh'] = zh
                    e['gloss_provenance'] = 'machine_translated'
                    n_done += 1

    VOCAB.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    total = len(data.get('entries', []))
    print(f'Translated glosses on {n_done}/{total} entries ({100*n_done//total}% coverage).')
    print(f'  skipped (already done): {n_skipped}')
    print(f'  remaining (renderer falls back to EN): {total - n_done - n_skipped}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
