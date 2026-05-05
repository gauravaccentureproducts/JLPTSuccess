"""IMP-047 (audit round-5): translate kanji meanings into vi/id/ne/zh.

For each of the 106 N5 kanji, populate `meanings_vi/_id/_ne/_zh` arrays
mirroring the structure of the existing `meanings` (English) array.
Authored by Claude using N5-syllabus context awareness — these are
short concrete concepts (numbers, days, body parts, basic verbs) where
machine-translation quality is high but native review is still
recommended before promoting `_provenance` to `native_reviewed`.

Each entry's translations preserve the same number of senses as the
English array (e.g., 日 has 2 EN meanings ["day","sun"] -> 2 entries
per locale).

Schema additions per kanji:
  meanings_vi: [...]
  meanings_id: [...]
  meanings_ne: [...]
  meanings_zh: [...]
  meanings_provenance: "machine_translated"

Idempotent: items already carrying the new fields are skipped.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KANJI = ROOT / 'data' / 'kanji.json'

# Format per kanji: (vi, id, ne, zh) — each is a list of strings, one
# per English-meaning sense. Aligned positionally with the existing
# `meanings` array.
TRANSLATIONS = {
    '一': (['một'],                   ['satu'],                  ['एक'],                       ['一; 一个']),
    '二': (['hai'],                   ['dua'],                   ['दुई'],                      ['二; 两']),
    '三': (['ba'],                    ['tiga'],                  ['तीन'],                      ['三']),
    '四': (['bốn'],                   ['empat'],                 ['चार'],                      ['四']),
    '五': (['năm'],                   ['lima'],                  ['पाँच'],                     ['五']),
    '六': (['sáu'],                   ['enam'],                  ['छ'],                        ['六']),
    '七': (['bảy'],                   ['tujuh'],                 ['सात'],                      ['七']),
    '八': (['tám'],                   ['delapan'],               ['आठ'],                       ['八']),
    '九': (['chín'],                  ['sembilan'],              ['नौ'],                       ['九']),
    '十': (['mười'],                  ['sepuluh'],               ['दस'],                       ['十']),
    '百': (['trăm'],                  ['seratus'],               ['सय'],                       ['百']),
    '千': (['nghìn'],                 ['seribu'],                ['हजार'],                     ['千']),
    '万': (['mười nghìn (vạn)'],      ['sepuluh ribu'],          ['दस हजार'],                  ['万; 一万']),
    '円': (['yên (đồng tiền Nhật)'],  ['yen (mata uang Jepang)'], ['येन (जापानी मुद्रा)'],    ['日元']),
    '日': (['ngày', 'mặt trời'],      ['hari', 'matahari'],      ['दिन', 'सूर्य'],            ['日; 天', '太阳']),
    '月': (['tháng', 'mặt trăng'],    ['bulan', 'bulan (di langit)'], ['महिना', 'चन्द्रमा'],   ['月; 月份', '月亮']),
    '火': (['lửa', 'thứ Ba'],         ['api', 'Selasa'],         ['आगो', 'मङ्गलबार'],         ['火', '星期二']),
    '水': (['nước', 'thứ Tư'],        ['air', 'Rabu'],           ['पानी', 'बुधबार'],           ['水', '星期三']),
    '木': (['cây', 'gỗ', 'thứ Năm'],  ['pohon', 'kayu', 'Kamis'], ['रूख', 'काठ', 'बिहीबार'],  ['树; 木', '木材', '星期四']),
    '金': (['vàng', 'tiền', 'thứ Sáu'], ['emas', 'uang', 'Jumat'], ['सुन', 'पैसा', 'शुक्रबार'], ['金子', '钱', '星期五']),
    '土': (['đất', 'thổ nhưỡng', 'thứ Bảy'], ['tanah', 'tanah liat', 'Sabtu'], ['माटो', 'भूमि', 'शनिबार'], ['泥土', '土壤', '星期六']),
    '曜': (['ngày trong tuần'],       ['hari (dalam minggu)'],   ['हप्ताको दिन'],              ['星期的日子']),
    '年': (['năm (đơn vị thời gian)'], ['tahun'],                ['वर्ष'],                     ['年']),
    '時': (['thời gian', 'giờ'],       ['waktu', 'jam'],          ['समय', 'घण्टा'],             ['时间', '小时']),
    '分': (['phút', 'phần', 'chia'],   ['menit', 'bagian', 'membagi'], ['मिनेट', 'भाग', 'विभाजन'], ['分钟', '部分', '分开']),
    '半': (['nửa'],                    ['setengah'],              ['आधा'],                      ['一半']),
    '今': (['bây giờ'],                ['sekarang'],              ['अब'],                       ['现在']),
    '毎': (['mỗi'],                    ['setiap'],                ['प्रत्येक'],                 ['每']),
    '週': (['tuần'],                   ['minggu (7 hari)'],       ['हप्ता'],                    ['周; 星期']),
    '午': (['trưa'],                   ['siang'],                 ['मध्याह्न'],                 ['正午']),
    '何': (['gì', 'cái nào'],          ['apa'],                   ['के'],                       ['什么']),
    '人': (['người'],                  ['orang'],                 ['मानिस'],                    ['人']),
    '男': (['đàn ông', 'nam'],         ['pria', 'laki-laki'],     ['पुरुष', 'मानिस'],          ['男人', '男性']),
    '女': (['phụ nữ', 'nữ'],           ['wanita', 'perempuan'],   ['महिला', 'स्त्री'],          ['女人', '女性']),
    '子': (['trẻ con'],                ['anak'],                  ['बच्चा'],                    ['孩子']),
    '父': (['cha', 'bố'],               ['ayah'],                  ['बुबा', 'बाबा'],             ['父亲']),
    '母': (['mẹ'],                     ['ibu'],                   ['आमा'],                      ['母亲']),
    '友': (['bạn'],                    ['teman'],                 ['साथी'],                     ['朋友']),
    '先': (['trước', 'phía trước', 'đầu (đỉnh)'], ['sebelumnya', 'di depan', 'ujung'], ['पहिले', 'अघि', 'टुप्पो'], ['以前', '前面', '尖端']),
    '生': (['sự sống', 'sinh ra'],      ['kehidupan', 'kelahiran'], ['जीवन', 'जन्म'],            ['生命', '出生']),
    '手': (['tay'],                    ['tangan'],                ['हात'],                      ['手']),
    '足': (['bàn chân', 'chân'],        ['kaki', 'tungkai'],       ['खुट्टा', 'गोडा'],           ['脚', '腿']),
    '目': (['mắt'],                    ['mata'],                  ['आँखा'],                     ['眼睛']),
    '口': (['miệng'],                  ['mulut'],                 ['मुख'],                      ['嘴; 口']),
    '力': (['sức mạnh', 'lực'],         ['kekuatan', 'tenaga'],    ['शक्ति', 'बल'],              ['力量', '力气']),
    '学': (['học', 'việc học'],         ['belajar', 'pembelajaran'], ['अध्ययन', 'सिकाइ'],        ['学习', '学问']),
    '校': (['trường học'],              ['sekolah'],               ['विद्यालय'],                 ['学校']),
    '本': (['sách', 'gốc', 'chính'],    ['buku', 'asal', 'utama'], ['पुस्तक', 'मूल', 'मुख्य'],   ['书', '本源', '主要']),
    '語': (['ngôn ngữ', 'từ'],          ['bahasa', 'kata'],        ['भाषा', 'शब्द'],             ['语言', '词语']),
    '国': (['nước (quốc gia)'],         ['negara'],                ['देश'],                      ['国家']),
    '会': (['cuộc gặp', 'hội'],         ['pertemuan', 'asosiasi'], ['भेट', 'सङ्घ'],              ['会议', '协会']),
    '社': (['công ty'],                 ['perusahaan'],            ['कम्पनी'],                   ['公司']),
    '員': (['thành viên', 'nhân viên'], ['anggota', 'staf'],       ['सदस्य', 'कर्मचारी'],        ['成员', '职员']),
    '大': (['to', 'lớn'],               ['besar'],                 ['ठूलो'],                     ['大']),
    '中': (['giữa', 'bên trong'],       ['tengah', 'di dalam'],    ['बीच', 'भित्र'],             ['中间', '里面']),
    '小': (['nhỏ', 'bé'],               ['kecil'],                 ['सानो'],                     ['小']),
    '上': (['trên', 'phía trên'],       ['atas', 'di atas'],       ['माथि', 'माथिल्लो'],         ['上面', '在上']),
    '下': (['dưới', 'phía dưới'],       ['bawah', 'di bawah'],     ['तल', 'तल्लो'],              ['下面', '在下']),
    '左': (['bên trái'],                ['kiri'],                  ['बायाँ'],                    ['左']),
    '右': (['bên phải'],                ['kanan'],                 ['दायाँ'],                    ['右']),
    '前': (['trước', 'phía trước'],     ['sebelum', 'depan'],      ['अघि', 'अगाडि'],             ['以前', '前面']),
    '後': (['sau', 'phía sau'],         ['setelah', 'belakang'],   ['पछि', 'पछाडि'],             ['之后', '后面']),
    '外': (['bên ngoài'],               ['luar'],                  ['बाहिर'],                    ['外面']),
    '東': (['phía đông'],               ['timur'],                 ['पूर्व'],                    ['东']),
    '西': (['phía tây'],                ['barat'],                 ['पश्चिम'],                   ['西']),
    '南': (['phía nam'],                ['selatan'],               ['दक्षिण'],                   ['南']),
    '北': (['phía bắc'],                ['utara'],                 ['उत्तर'],                    ['北']),
    '間': (['khoảng', 'giữa', 'không gian'], ['interval', 'antara', 'ruang'], ['अन्तराल', 'बीच', 'खाली ठाउँ'], ['间隔', '之间', '空间']),
    '山': (['núi'],                     ['gunung'],                ['पहाड'],                     ['山']),
    '川': (['sông'],                    ['sungai'],                ['नदी'],                      ['河; 川']),
    '田': (['ruộng (lúa)'],             ['sawah'],                 ['धानखेत'],                   ['稻田']),
    '雨': (['mưa'],                     ['hujan'],                 ['वर्षा', 'पानी पर्ने'],      ['雨']),
    '天': (['trời', 'bầu trời'],        ['surga', 'langit'],       ['स्वर्ग', 'आकाश'],           ['天堂', '天空']),
    '気': (['tinh thần', 'tâm trạng', 'không khí'], ['semangat', 'suasana hati', 'udara'], ['भावना', 'मनस्थिति', 'हावा'], ['精神', '心情', '空气']),
    '花': (['hoa'],                     ['bunga'],                 ['फूल'],                      ['花']),
    '空': (['bầu trời', 'trống rỗng'],  ['langit', 'kosong'],      ['आकाश', 'खाली'],             ['天空', '空的']),
    '電': (['điện'],                    ['listrik'],               ['विद्युत्'],                 ['电']),
    '車': (['xe', 'phương tiện'],       ['mobil', 'kendaraan'],    ['गाडी', 'सवारी साधन'],       ['汽车', '车辆']),
    '道': (['đường', 'lối'],            ['jalan', 'jalur'],        ['बाटो', 'मार्ग'],            ['道路', '道']),
    '店': (['cửa hàng'],                ['toko'],                  ['पसल'],                      ['店; 商店']),
    '駅': (['ga (xe điện)'],            ['stasiun'],               ['स्टेसन'],                   ['车站']),
    '食': (['ăn', 'thức ăn'],           ['makan', 'makanan'],      ['खानु', 'खाना'],             ['吃', '食物']),
    '飲': (['uống'],                    ['minum'],                 ['पिउनु'],                    ['喝']),
    '見': (['nhìn', 'xem'],             ['melihat', 'memperhatikan'], ['हेर्नु', 'देख्नु'],     ['看', '观看']),
    '聞': (['nghe', 'lắng nghe', 'hỏi'], ['mendengar', 'mendengarkan', 'bertanya'], ['सुन्नु', 'ध्यानले सुन्नु', 'सोध्नु'], ['听', '聆听', '问']),
    '読': (['đọc'],                     ['membaca'],               ['पढ्नु'],                    ['读']),
    '書': (['viết'],                    ['menulis'],               ['लेख्नु'],                   ['写']),
    '話': (['nói', 'kể chuyện', 'câu chuyện'], ['berbicara', 'bercakap', 'cerita'], ['बोल्नु', 'भन्नु', 'कथा'], ['说', '讲', '故事']),
    '来': (['đến'],                     ['datang'],                ['आउनु'],                     ['来']),
    '行': (['đi', 'tiến hành'],         ['pergi', 'melaksanakan'], ['जानु', 'सञ्चालन गर्नु'],    ['去', '进行']),
    '出': (['đi ra', 'ra ngoài', 'đưa ra'], ['keluar', 'pergi ke luar', 'mengeluarkan'], ['निस्किनु', 'बाहिर जानु', 'निकाल्नु'], ['出去', '外出', '取出']),
    '入': (['vào', 'cho vào'],          ['masuk', 'memasukkan'],   ['प्रवेश गर्नु', 'राख्नु'],   ['进入', '放入']),
    '立': (['đứng'],                    ['berdiri'],               ['उभिनु'],                    ['站; 站立']),
    '休': (['nghỉ', 'kỳ nghỉ'],         ['istirahat', 'libur'],    ['आराम', 'बिदा'],             ['休息', '假日']),
    '言': (['nói', 'từ'],                ['mengatakan', 'kata'],    ['भन्नु', 'शब्द'],            ['说', '话语']),
    '買': (['mua'],                     ['membeli'],               ['किन्नु'],                   ['买']),
    '高': (['cao', 'mắc tiền'],          ['tinggi', 'mahal'],       ['उच्च', 'महँगो'],            ['高', '昂贵']),
    '安': (['rẻ', 'an toàn', 'bình yên'], ['murah', 'aman', 'damai'], ['सस्तो', 'सुरक्षित', 'शान्त'], ['便宜', '安全', '安宁']),
    '新': (['mới'],                     ['baru'],                  ['नयाँ'],                     ['新']),
    '古': (['cũ'],                      ['lama'],                  ['पुरानो'],                   ['旧; 古']),
    '長': (['dài', 'người đứng đầu'],    ['panjang', 'pemimpin'],   ['लामो', 'नेता'],             ['长', '首领']),
    '白': (['trắng'],                   ['putih'],                 ['सेतो'],                     ['白色']),
    '名': (['tên'],                     ['nama'],                  ['नाम'],                      ['名字']),
    '番': (['số', 'lượt'],               ['nomor', 'giliran'],      ['नम्बर', 'पालो'],            ['号', '轮次']),
    '号': (['số'],                      ['nomor'],                 ['संख्या'],                   ['号']),
    '私': (['tôi'],                     ['saya'],                  ['म'],                        ['我']),
}


def main() -> int:
    data = json.loads(KANJI.read_text(encoding='utf-8'))
    n_done = 0
    n_skipped = 0
    n_missing = 0
    for e in data.get('entries', []):
        glyph = e.get('glyph')
        if not glyph: continue
        if 'meanings_vi' in e and 'meanings_id' in e and 'meanings_ne' in e and 'meanings_zh' in e:
            n_skipped += 1
            continue
        if glyph not in TRANSLATIONS:
            n_missing += 1
            print(f'  WARN: no translation for {glyph!r}')
            continue
        vi, id_, ne, zh = TRANSLATIONS[glyph]
        en = e.get('meanings', [])
        # Sanity: keep the same number of senses; if count differs, pad with first.
        def align(lst, target_len):
            if len(lst) == target_len: return lst
            if len(lst) < target_len: return lst + [lst[-1] if lst else ''] * (target_len - len(lst))
            return lst[:target_len]
        e['meanings_vi'] = align(vi, len(en))
        e['meanings_id'] = align(id_, len(en))
        e['meanings_ne'] = align(ne, len(en))
        e['meanings_zh'] = align(zh, len(en))
        e['meanings_provenance'] = 'machine_translated'
        n_done += 1

    KANJI.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'Translated meanings on {n_done} kanji entries.')
    print(f'  skipped (already done): {n_skipped}')
    print(f'  missing translation:    {n_missing}')
    print(f'Provenance: machine_translated. Native review needed before')
    print(f'`meanings_provenance` is upgraded to `native_reviewed`.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
