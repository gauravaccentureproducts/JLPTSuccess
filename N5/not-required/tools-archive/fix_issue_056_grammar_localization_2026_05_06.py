"""ISSUE-056 + IMP-080 (audit round-7, 2026-05-06): grammar localization +
L1-interference notes for the top-30 N5 patterns.

Schema additions per pattern covered here:
  meaning_vi / meaning_id / meaning_ne / meaning_zh
  explanation_vi / explanation_id / explanation_ne / explanation_zh
  meaning_provenance: "machine_translated"
  explanation_provenance: "machine_translated"
  l1_notes: { vi, id, ne, zh }   (top-15 patterns only - IMP-080)

Per user clarification (2026-05-06): translate the meaning + explanation
INSTRUCTIONS only. The Japanese pattern itself, Japanese examples, and
meaning_ja stay in Japanese - that is what the learner is studying.

Idempotent. All translations remain `machine_translated` until native
review per Q21 provenance-badge launch policy.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
GF = ROOT / 'data' / 'grammar.json'

# Each pattern entry: pattern_id -> {
#   meaning: {vi, id, ne, zh},
#   explanation: {vi, id, ne, zh},
#   l1_notes: {vi, id, ne, zh}   # optional, top-15 only
# }
TRANSLATIONS = {
    'n5-001': {
        'meaning': {
            'vi': 'Vĩ tố lịch sự です / ます (động từ và hệ từ thể lịch sự)',
            'id': 'Akhiran sopan です / ます (kopula dan kata kerja bentuk sopan)',
            'ne': 'विनम्र अन्त्य です / ます (विनम्र क्रिया र be-क्रिया)',
            'zh': '礼貌结尾 です / ます（系词与动词的礼貌形式）',
        },
        'explanation': {
            'vi': 'です đứng cuối câu sau danh từ hoặc tính từ-na, nghĩa là "là". ます là vĩ tố lịch sự gắn vào gốc động từ. Đây là dạng cơ bản nhất của tiếng Nhật lịch sự.',
            'id': 'です muncul di akhir kalimat setelah kata benda atau kata sifat-na, berarti "adalah". ます adalah akhiran sopan yang menempel pada batang kata kerja. Ini adalah bentuk paling dasar dari bahasa Jepang sopan.',
            'ne': 'です वाक्यको अन्त्यमा संज्ञा वा na-विशेषण पछि आउँछ, अर्थ "हो"। ます क्रियाको स्तेममा जोडिने विनम्र अन्त्य हो। यो विनम्र जापानीको सबैभन्दा आधारभूत रूप हो।',
            'zh': 'です 出现在名词或な-形容词后的句末，意思是"是"。ます 是附加在动词词干上的礼貌后缀。这是最基本的礼貌日语形式。',
        },
        'l1_notes': {
            'vi': 'Tiếng Việt không có hệ từ "là" bắt buộc trong câu khẳng định danh từ ("Tôi là sinh viên" thường nói "Tôi sinh viên"). Người học Việt thường quên です ở cuối câu.',
            'id': 'Bahasa Indonesia tidak memiliki kopula wajib ("Saya mahasiswa" tanpa "adalah"). Pelajar Indonesia sering lupa です di akhir kalimat.',
            'ne': 'नेपालीमा "हो" को आवश्यकता हुन्छ तर वाक्यको अन्तमा होइन, बीचमा। です को स्थान फरक छ; भाषाको क्रम बुझ्नुहोस्।',
            'zh': '中文的「是」可省略，日语的 です 不可省略（除非降级为だ）。中国学习者常因母语习惯遗漏 です。礼貌等级与中文「您好」类似但适用更广。',
        },
    },
    'n5-002': {
        'meaning': {
            'vi': 'Trợ từ chủ đề は (giới thiệu chủ đề câu)',
            'id': 'Partikel topik は (menandai topik kalimat)',
            'ne': 'विषय चिन्ह は (वाक्यको विषय जनाउँछ)',
            'zh': '主题标记 は（标示句子的主题）',
        },
        'explanation': {
            'vi': 'は theo sau danh từ để biến nó thành chủ đề ("nói về X..."). Phát âm là "wa" mặc dù viết bằng は. Chủ đề thường là thông tin đã biết; thông tin mới đi với が.',
            'id': 'は mengikuti kata benda untuk menjadikannya topik ("mengenai X..."). Diucapkan "wa" meskipun ditulis は. Topik biasanya informasi yang sudah diketahui; informasi baru memakai が.',
            'ne': 'は संज्ञा पछि आएर त्यसलाई विषय बनाउँछ ("X को बारेमा...")। लेखाइ は तर उच्चारण "wa" हो। विषय सामान्यतया पहिले देखि थाहा भएको कुरा हुन्छ; नयाँ जानकारीमा が आउँछ।',
            'zh': 'は 跟在名词后将其转为主题（"关于X..."）。虽然写作 は 但读作 "wa"。主题通常是已知信息；新信息用 が。',
        },
        'l1_notes': {
            'vi': 'Tiếng Việt không có trợ từ chủ đề rõ ràng. は và が là một trong những điểm khó nhất của tiếng Nhật N5: は dùng cho thông tin đã biết, が cho thông tin mới hoặc trọng tâm. Hãy luyện tập tương phản.',
            'id': 'Bahasa Indonesia tidak memiliki partikel topik eksplisit. は vs が adalah salah satu titik tersulit dari N5: は untuk info yang sudah diketahui, が untuk info baru atau fokus.',
            'ne': 'नेपालीमा "ले" subject जनाउँछ तर topic र subject फरक होइनन्। は (topic) र が (subject) को भेद जापानी सिक्ने सबैको लागि कठिन छ।',
            'zh': '中文没有专门的主题助词，但语序常隐含主题（"我嘛..."）。は 类似中文的"...呢..."的话题化，が 标示新信息。中国学习者容易混淆 は 和 が。',
        },
    },
    'n5-003': {
        'meaning': {
            'vi': 'Trợ từ chủ ngữ が (đánh dấu thông tin mới hoặc trọng tâm)',
            'id': 'Partikel subjek が (menandai informasi baru atau fokus)',
            'ne': 'कर्ता चिन्ह が (नयाँ जानकारी वा फोकस जनाउँछ)',
            'zh': '主语标记 が（标示新信息或焦点）',
        },
        'explanation': {
            'vi': 'が theo sau danh từ để đánh dấu chủ ngữ ngữ pháp, đặc biệt khi thông tin là mới hoặc trọng tâm. Đối lập với は (chủ đề đã biết). Bắt buộc với một số động từ và tính từ như ある, いる, 好き, 上手.',
            'id': 'が mengikuti kata benda untuk menandai subjek gramatikal, terutama saat informasi baru atau menjadi fokus. Berlawanan dengan は (topik yang sudah diketahui). Wajib dengan beberapa kata kerja dan kata sifat seperti ある, いる, 好き, 上手.',
            'ne': 'が संज्ञा पछि व्याकरणिक कर्ता चिन्ह बन्छ, विशेष गरी नयाँ जानकारी वा फोकसको लागि। は (पहिले देखि थाहा भएको topic) सँग विपरीत। ある, いる, 好き, 上手 जस्ता क्रिया/विशेषणसँग अनिवार्य।',
            'zh': 'が 跟在名词后标示语法主语，特别是新信息或焦点时使用。与 は（已知主题）对比。某些动词和形容词如 ある、いる、好き、上手 必须用 が。',
        },
        'l1_notes': {
            'vi': 'Người học Việt thường dùng は cho mọi vai trò chủ ngữ. Cần ghi nhớ: 好き, 上手, 下手, 分かる, できる đi với が, không phải を hay は.',
            'id': 'Pelajar Indonesia sering pakai は untuk semua peran subjek. Perlu diingat: 好き, 上手, 下手, 分かる, できる pakai が, bukan を atau は.',
            'ne': 'नेपालीमा "ले" र object marker फरक छ; が चाहिँ subject only हो, object को लागि を छुट्टै छ। 好き सँग が चाहिन्छ (を होइन)।',
            'zh': '中文的"喜欢"是动词，宾语用"我喜欢苹果"中的"苹果"为宾语。日语 好き 是な-形容词，喜欢的对象用 が 而非 を：「私はりんごが好きです」。',
        },
    },
    'n5-004': {
        'meaning': {
            'vi': 'Trợ từ tân ngữ trực tiếp を (đánh dấu danh từ nhận hành động)',
            'id': 'Partikel objek langsung を (menandai kata benda yang menerima aksi)',
            'ne': 'सीधा कर्म चिन्ह を (कार्य प्राप्त गर्ने संज्ञा जनाउँछ)',
            'zh': '直接宾语标记 を（标示接受动作的名词）',
        },
        'explanation': {
            'vi': 'を theo sau danh từ là tân ngữ trực tiếp của ngoại động từ (パンを食べる "ăn bánh mì"). Phát âm là "o", không phải "wo". Chỉ dùng với ngoại động từ; tự động từ dùng が hoặc に.',
            'id': 'を mengikuti kata benda yang menjadi objek langsung dari kata kerja transitif (パンを食べる "makan roti"). Diucapkan "o", bukan "wo". Hanya untuk kata kerja transitif; intransitif memakai が atau に.',
            'ne': 'を सकर्मक क्रियाको प्रत्यक्ष कर्म जनाउने संज्ञा पछि आउँछ (パンを食べる "रोटी खाने")। उच्चारण "o" हो, "wo" होइन। सकर्मक क्रियासँग मात्र; अकर्मकमा が वा に।',
            'zh': 'を 跟在他动词的直接宾语名词后（パンを食べる "吃面包"）。读作 "o" 而非 "wo"。仅用于他动词；自动词用 が 或 に。',
        },
        'l1_notes': {
            'vi': 'Tiếng Việt không có sự phân biệt rõ ngoại động từ / tự động từ về mặt hình thái. Lỗi phổ biến: dùng を với 入る (tự động từ - phải là が hoặc に). Hãy học cặp 入れる/入る.',
            'id': 'Bahasa Indonesia tidak memiliki morfologi transitif/intransitif yang jelas. Kesalahan umum: menggunakan を dengan 入る (intransitif - harus が atau に). Pelajari pasangan 入れる/入る.',
            'ne': 'नेपालीमा सकर्मक/अकर्मक भेद हुन्छ तर मार्किङ फरक छ। 入れる (सकर्मक) सँग を, 入る (अकर्मक) सँग に वा が। दुवै जोडी सिक्नुहोस्।',
            'zh': '中文动词大多没有自他动词的形态对立。日语有成对的他动词/自动词（开ける/开く、入れる/入る等），他动词的对象用 を，自动词无对象。',
        },
    },
    'n5-005': {
        'meaning': {
            'vi': 'Trợ từ đa năng に (vị trí tồn tại / thời gian cụ thể / đích đến)',
            'id': 'Partikel multifungsi に (lokasi keberadaan / waktu spesifik / tujuan)',
            'ne': 'बहुउद्देश्यीय に (अस्तित्व स्थान / निश्चित समय / गन्तव्य)',
            'zh': '多用途助词 に（存在地点 / 具体时间 / 目的地）',
        },
        'explanation': {
            'vi': 'に có 3 vai trò chính ở N5: (1) vị trí tồn tại với ある/いる ("ở đâu có/ở"); (2) thời gian cụ thể (七時に "lúc 7 giờ"); (3) đích đến với động từ chuyển động ("đến đâu"). So sánh với で (nơi diễn ra hành động).',
            'id': 'に memiliki 3 peran utama di N5: (1) lokasi keberadaan dengan ある/いる ("di mana ada/berada"); (2) waktu spesifik (七時に "pada jam 7"); (3) tujuan dengan kata kerja gerakan ("ke mana"). Bandingkan dengan で (tempat aksi).',
            'ne': 'に का N5 मा 3 मुख्य भूमिका: (1) ある/いる सँग अस्तित्व स्थान; (2) निश्चित समय (七時に "७ बजे"); (3) गति क्रियासँग गन्तव्य ("कहाँ"). で (कार्य स्थान) सँग तुलना।',
            'zh': 'に 在 N5 有三个主要功能：(1) 与 ある/いる 配合表示存在地点；(2) 具体时间点（七時に "在7点"）；(3) 与移动动词配合表示目的地。与 で（动作地点）对比。',
        },
        'l1_notes': {
            'vi': 'Tiếng Việt dùng "ở" cho vị trí và "lúc" cho thời gian - hai từ riêng biệt. Tiếng Nhật gộp thành một に. Lỗi phổ biến: dùng で thay vì に cho vị trí tồn tại.',
            'id': 'Bahasa Indonesia memakai "di" untuk lokasi dan "pada" untuk waktu - dua kata terpisah. Bahasa Jepang menggabungkannya menjadi に. Kesalahan umum: pakai で alih-alih に untuk lokasi keberadaan.',
            'ne': 'नेपालीमा स्थान र समयको लागि "मा" साझा छ - に सँग समान। तर に र で को भेद नेपालीमा छैन। 学校にいる (विद्यालयमा छ) vs 学校で勉強する (विद्यालयमा पढ्ने) फरक हो।',
            'zh': '中文「在」既表静态存在也表动态发生（"在家"/"在家吃饭"）。日语严格区分：静态存在用 に（家にいる），动作进行用 で（家で食べる）。这是日语初学者最大难点之一。',
        },
    },
    'n5-006': {
        'meaning': {
            'vi': 'Trợ từ phương hướng へ (đến / hướng về - dùng với động từ chuyển động)',
            'id': 'Partikel arah へ (menuju - dipakai dengan kata kerja gerakan)',
            'ne': 'दिशा चिन्ह へ (तिर / लाई - गति क्रियासँग प्रयोग)',
            'zh': '方向标记 へ（朝向 - 与移动动词搭配）',
        },
        'explanation': {
            'vi': 'へ theo sau danh từ chỉ đích đến với động từ chuyển động (行く, 来る, 帰る). Phát âm là "e", không phải "he". に cũng có thể dùng tương tự, nhưng へ nhấn mạnh hơn vào hướng đi (quá trình); に nhấn vào điểm đích (kết quả).',
            'id': 'へ mengikuti kata benda tujuan dengan kata kerja gerakan (行く, 来る, 帰る). Diucapkan "e", bukan "he". に juga bisa dipakai serupa, tetapi へ menekankan arah (proses); に menekankan titik tujuan (hasil).',
            'ne': 'へ गति क्रिया (行く, 来る, 帰る) सँग गन्तव्य संज्ञा पछि आउँछ। उच्चारण "e" हो, "he" होइन। に पनि उस्तै प्रयोग हुन्छ, तर へ ले दिशा (प्रक्रिया) जोड दिन्छ; に ले गन्तव्य बिन्दु (परिणाम)।',
            'zh': 'へ 跟在移动动词（行く、来る、帰る）的目的地名词后。读作 "e" 而非 "he"。に 也可类似使用，但 へ 强调方向（过程），に 强调目的地（结果）。',
        },
    },
    'n5-007': {
        'meaning': {
            'vi': 'Trợ từ で (nơi diễn ra hành động / phương tiện / công cụ)',
            'id': 'Partikel で (lokasi aksi / sarana / alat)',
            'ne': 'で (कार्य स्थान / साधन / उपकरण)',
            'zh': '助词 で（动作发生地点 / 手段 / 工具）',
        },
        'explanation': {
            'vi': 'で có 3 vai trò N5: (1) nơi diễn ra hành động (学校で勉強する "học ở trường"); (2) phương tiện (バスで来る "đến bằng xe buýt"); (3) công cụ / nguyên liệu (はしで食べる "ăn bằng đũa"). So sánh với に (vị trí tồn tại tĩnh).',
            'id': 'で memiliki 3 peran N5: (1) tempat aksi (学校で勉強する "belajar di sekolah"); (2) sarana (バスで来る "datang naik bis"); (3) alat / bahan (はしで食べる "makan dengan sumpit"). Bandingkan dengan に (lokasi keberadaan statis).',
            'ne': 'で का N5 मा 3 भूमिका: (1) कार्य स्थान (学校で勉強する "विद्यालयमा पढ्ने"); (2) साधन (バスで来る "बसले आउने"); (3) उपकरण/सामग्री (はしで食べる "चपस्टिकले खाने")। に (स्थिर अस्तित्व स्थान) सँग तुलना।',
            'zh': 'で 在 N5 有三个功能：(1) 动作发生地点（学校で勉強する "在学校学习"）；(2) 交通手段（バスで来る "坐公交来"）；(3) 工具/材料（はしで食べる "用筷子吃"）。与 に（静态存在地点）对比。',
        },
        'l1_notes': {
            'vi': 'Lỗi で vs に là điểm khó nhất ở N5. Quy tắc: hành động chuyển động → で (nơi đang xảy ra); tồn tại tĩnh → に (đang ở). 図書館で本を読む (đọc sách ở thư viện) vs 図書館にいる (đang ở thư viện).',
            'id': 'Kesalahan で vs に adalah titik tersulit N5. Aturan: aksi berlangsung → で (tempat aksi); keberadaan statis → に (lokasi). 図書館で本を読む (baca buku di perpustakaan) vs 図書館にいる (berada di perpustakaan).',
            'ne': 'で र に को भेद नेपाली बक्ताहरूको लागि कठिन। नियम: गतिशील क्रिया → で; स्थिर अस्तित्व → に। 図書館で本を読む vs 図書館にいる दुवै "मा" अनुवाद हुन्छ तर जापानी फरक छ।',
            'zh': '中文「在」涵盖动作和存在两种语境。日语严格区分：动作性「在...」用 で（学校で勉強する），存在性「在...」用 に（学校にいる）。中国学习者最常混淆。',
        },
    },
    'n5-008': {
        'meaning': {
            'vi': 'Trợ từ と (cùng với / và (liệt kê đầy đủ) / trích dẫn)',
            'id': 'Partikel と (bersama / dan (daftar lengkap) / kutipan)',
            'ne': 'と (सँगै / र (पूर्ण सूची) / उद्धरण)',
            'zh': '助词 と（和（伴随）/ 和（列举）/ 引语）',
        },
        'explanation': {
            'vi': 'と có 3 vai trò N5: (1) cùng với ai đó (ともだちと行く "đi với bạn"); (2) liệt kê đầy đủ A và B (パンとミルク "bánh mì và sữa" - chỉ A và B); (3) trích dẫn (「はい」と言う "nói rằng \'vâng\'"). So sánh với や (liệt kê không đầy đủ).',
            'id': 'と memiliki 3 peran N5: (1) bersama seseorang (ともだちと行く "pergi dengan teman"); (2) daftar lengkap A dan B (パンとミルク "roti dan susu" - hanya A dan B); (3) kutipan (「はい」と言う "berkata \'ya\'"). Bandingkan dengan や (daftar tidak lengkap).',
            'ne': 'と का N5 मा 3 भूमिका: (1) कसैसँग (ともだちと行く "साथीसँग जाने"); (2) पूर्ण सूची A र B (パンとミルク "रोटी र दूध - खालि A र B"); (3) उद्धरण (「はい」と言う "\'ho\' भन्ने")। や (अपूर्ण सूची) सँग तुलना।',
            'zh': 'と 在 N5 有三个功能：(1) 与某人同行（ともだちと行く "和朋友去"）；(2) 完全列举 A 和 B（パンとミルク "面包和牛奶 - 仅A和B"）；(3) 引语（「はい」と言う "说\'是\'"）。与 や（不完全列举）对比。',
        },
    },
    'n5-009': {
        'meaning': {
            'vi': 'Trợ từ から (từ - điểm bắt đầu / vì - lý do)',
            'id': 'Partikel から (dari - titik awal / karena - alasan)',
            'ne': 'から (देखि / बाट - सुरु बिन्दु / किनभने - कारण)',
            'zh': '助词 から（从 - 起点 / 因为 - 原因）',
        },
        'explanation': {
            'vi': 'から có 2 vai trò N5: (1) điểm bắt đầu trong thời gian / không gian (九時から "từ 9 giờ", 学校から "từ trường"); (2) lý do - gắn vào câu hoàn chỉnh (ねむいから帰ります "vì buồn ngủ nên về"). Đi cặp với まで (đến).',
            'id': 'から memiliki 2 peran N5: (1) titik awal waktu/ruang (九時から "dari jam 9", 学校から "dari sekolah"); (2) alasan - menempel pada klausa lengkap (ねむいから帰ります "karena ngantuk pulang"). Berpasangan dengan まで (sampai).',
            'ne': 'から का N5 मा 2 भूमिका: (1) समय/स्थानको सुरु बिन्दु (九時から "९ बजे देखि", 学校から "विद्यालयबाट"); (2) कारण - पूर्ण उपवाक्यमा जोडिएर (ねむいから帰ります "निद्रा लागेको हुनाले फर्किने")। まで (सम्म) सँग जोडी।',
            'zh': 'から 在 N5 有两个功能：(1) 时间/空间起点（九時から "从9点起"、学校から "从学校"）；(2) 原因 - 接在完整句末（ねむいから帰ります "因为困了所以回去"）。与 まで（直到）配对。',
        },
        'l1_notes': {
            'vi': 'Người học Việt thường nhầm から (lý do, ý chủ quan) với ので (lý do, khách quan/lịch sự). から OK trong hội thoại; ので lịch sự hơn cho lý do trang trọng.',
            'id': 'Pelajar Indonesia sering bingung から (alasan, subjektif) dengan ので (alasan, objektif/sopan). から OK untuk percakapan; ので lebih sopan untuk alasan formal.',
            'ne': 'नेपालीको "किनभने" र "हुनाले" को भेद から र ので सँग मिल्छ। から बोलचालमा, ので औपचारिकमा।',
            'zh': '中文「因为」可对应日语 から、ので 两者。から 主观、口语；ので 客观、礼貌。两者用法重合度高，但礼貌等级不同。',
        },
    },
    'n5-010': {
        'meaning': {
            'vi': 'Trợ từ まで (đến / cho đến - điểm kết thúc thời gian hoặc không gian)',
            'id': 'Partikel まで (sampai - titik akhir waktu atau ruang)',
            'ne': 'まで (सम्म - समय वा स्थानको अन्त्य बिन्दु)',
            'zh': '助词 まで（到 - 时间或空间终点）',
        },
        'explanation': {
            'vi': 'まで đánh dấu điểm kết thúc trong thời gian (五時まで "đến 5 giờ") hoặc không gian (駅まで歩く "đi bộ đến ga"). Thường đi cặp với から để chỉ phạm vi (九時から五時まで "từ 9 đến 5 giờ").',
            'id': 'まで menandai titik akhir waktu (五時まで "sampai jam 5") atau ruang (駅まで歩く "berjalan sampai stasiun"). Sering berpasangan dengan から untuk rentang (九時から五時まで "dari jam 9 sampai 5").',
            'ne': 'まで समय (五時まで "५ बजे सम्म") वा स्थानको (駅まで歩く "स्टेसन सम्म हिँड्ने") अन्त्य बिन्दु जनाउँछ। から सँग जोडी बनाएर सीमा (九時から五時まで "९ देखि ५ बजे सम्म")।',
            'zh': 'まで 标示时间（五時まで "到5点"）或空间（駅まで歩く "走到车站"）的终点。常与 から 配对表示范围（九時から五時まで "从9点到5点"）。',
        },
    },
    'n5-011': {
        'meaning': {
            'vi': 'Trợ từ や (và - liệt kê không đầy đủ, "X, Y và những thứ tương tự")',
            'id': 'Partikel や (dan - daftar tidak lengkap, "X, Y dan sejenisnya")',
            'ne': 'や (र - अपूर्ण सूची, "X, Y र अन्य")',
            'zh': '助词 や（和 - 不完全列举，"X、Y 等"）',
        },
        'explanation': {
            'vi': 'や liệt kê hai hoặc nhiều thứ một cách không đầy đủ, ngụ ý "và những thứ khác tương tự". Khác với と (liệt kê đầy đủ chỉ X và Y). Thường đi với など ở cuối: パンやミルクなど "bánh mì, sữa và các thứ khác".',
            'id': 'や mendaftar dua atau lebih hal secara tidak lengkap, mengisyaratkan "dan hal-hal lain serupa". Berbeda dari と (daftar lengkap hanya X dan Y). Sering dengan など di akhir: パンやミルクなど "roti, susu dan lain-lain".',
            'ne': 'や दुई वा बढी कुरा अपूर्ण रूपमा सूचीबद्ध गर्छ, "र अन्य उस्तै कुरा" जनाउँछ। と (पूर्ण सूची X र Y मात्र) सँग फरक। अन्त्यमा など सँग सामान्य: パンやミルクなど "रोटी, दूध आदि"।',
            'zh': 'や 列举两件或多件物品，暗示"等等"。与 と（完全列举 X 和 Y）不同。常与 など 配合：パンやミルクなど "面包、牛奶等"。',
        },
    },
    'n5-013': {
        'meaning': {
            'vi': 'Trợ từ も (cũng / nữa / thậm chí (với phủ định: không... một ai))',
            'id': 'Partikel も (juga / pun / bahkan (dengan negasi: tidak... satu pun))',
            'ne': 'も (पनि / सम्म (नकारात्मकसँग: कुनै ... पनि छैन))',
            'zh': '助词 も（也 / 都 / 甚至（与否定连用：一个也不...））',
        },
        'explanation': {
            'vi': 'も thay thế cho は hoặc が để nói "cũng/nữa" (わたしも学生です "tôi cũng là sinh viên"). Với phủ định + も = "không một ai/cái gì" (だれも来ない "không ai đến").',
            'id': 'も menggantikan は atau が untuk berarti "juga" (わたしも学生です "saya juga mahasiswa"). Dengan negasi + も = "tidak satu pun" (だれも来ない "tidak ada yang datang").',
            'ne': 'も ले は वा が को सट्टा "पनि" को अर्थ दिन्छ (わたしも学生です "म पनि विद्यार्थी")। नकारात्मक + も = "कुनै ... पनि छैन" (だれも来ない "कोही पनि आएन")।',
            'zh': 'も 替代 は 或 が 表示"也"（わたしも学生です "我也是学生"）。与否定连用 + も = "一个也不"（だれも来ない "谁也没来"）。',
        },
    },
    'n5-014': {
        'meaning': {
            'vi': 'Đại từ chỉ định: これ / それ / あれ / どれ (cái này / cái đó / cái kia / cái nào)',
            'id': 'Kata ganti tunjuk: これ / それ / あれ / どれ (ini / itu (dekat lawan) / itu (jauh) / yang mana)',
            'ne': 'सर्वनाम: これ / それ / あれ / どれ (यो / त्यो (श्रोता नजिक) / त्यो (टाढा) / कुन)',
            'zh': '指示代词：これ / それ / あれ / どれ（这个 / 那个（近听者）/ 那个（远）/ 哪个）',
        },
        'explanation': {
            'vi': 'Bộ này thay cho danh từ trong câu (これは本です "đây là sách"). Phân biệt theo khoảng cách: これ gần người nói; それ gần người nghe; あれ xa cả hai; どれ là câu hỏi. Khác với この/その/あの là tính từ chỉ định cần đi kèm danh từ.',
            'id': 'Set ini menggantikan kata benda dalam kalimat (これは本です "ini buku"). Dibedakan oleh jarak: これ dekat penutur; それ dekat lawan bicara; あれ jauh dari keduanya; どれ adalah pertanyaan. Berbeda dari この/その/あの yang adalah kata sifat penunjuk perlu kata benda.',
            'ne': 'यो सेटले वाक्यमा संज्ञालाई प्रतिस्थापित गर्छ (これは本です "यो किताब हो")। दूरी अनुसार छुट्टिन्छ: これ वक्ता नजिक; それ श्रोता नजिक; あれ दुवै बाट टाढा; どれ प्रश्न। この/その/あの (विशेषण, संज्ञा चाहिने) सँग फरक।',
            'zh': '该组在句中替代名词（これは本です "这是书"）。按距离区分：これ 近说话者；それ 近听者；あれ 离两者都远；どれ 是疑问词。与 この/その/あの（指示形容词，必须接名词）不同。',
        },
        'l1_notes': {
            'vi': 'Tiếng Việt có "này/đó/kia" nhưng không phân biệt rõ "gần người nghe" và "xa cả hai" như tiếng Nhật. Nhớ それ là khoảng cách RELATIONAL - gần người nghe, không phải gần người nói.',
            'id': 'Bahasa Indonesia memiliki "ini/itu" tapi tidak membedakan "dekat lawan bicara" vs "jauh dari keduanya" seperti bahasa Jepang. Ingat それ adalah jarak RELASIONAL - dekat lawan bicara.',
            'ne': 'नेपालीमा "यो/त्यो/उ" भेद छ तर श्रोता-केन्द्रित そ-छुट्टै छैन। それ श्रोता नजिक हो (वक्ता बाट होइन)।',
            'zh': '中文「这/那」二分；日语 こ・そ・あ 三分，且 そ 是"听者侧"而非简单的"远近"。中国学习者最易在 それ vs あれ 上犯错。',
        },
    },
    'n5-015': {
        'meaning': {
            'vi': 'Tính từ chỉ định: この / その / あの / どの + Danh từ (luôn cần danh từ theo sau)',
            'id': 'Kata sifat penunjuk: この / その / あの / どの + Kata Benda (selalu butuh kata benda)',
            'ne': 'विशेषण: この / その / あの / どの + संज्ञा (सधैं संज्ञा चाहिन्छ)',
            'zh': '指示形容词：この / その / あの / どの + 名词（必须接名词）',
        },
        'explanation': {
            'vi': 'Đây là dạng tính từ của これ/それ/あれ/どれ. Bắt buộc đi kèm danh từ ngay sau (この本 "cuốn sách này", *これ本 sai). Quy tắc khoảng cách giống như đại từ chỉ định.',
            'id': 'Ini adalah bentuk kata sifat dari これ/それ/あれ/どれ. Wajib diikuti kata benda langsung (この本 "buku ini", *これ本 salah). Aturan jarak sama dengan kata ganti tunjuk.',
            'ne': 'यो これ/それ/あれ/どれ को विशेषण रूप हो। तुरुन्तै संज्ञा चाहिन्छ (この本 "यो किताब", *これ本 गलत)। सर्वनाम जस्तै दूरी नियम।',
            'zh': '这是 これ/それ/あれ/どれ 的形容词形式。必须立即接名词（この本 "这本书"，*これ本 错误）。距离规则与指示代词相同。',
        },
        'l1_notes': {
            'vi': 'Lỗi phổ biến: chuyển ngữ "cái này sách" → これ本 (sai). Đúng: この本.',
            'id': 'Kesalahan umum: transfer "ini buku" → これ本 (salah). Benar: この本.',
            'ne': 'सामान्य गल्ती: "यो किताब" लाई これ本 भन्ने (गलत)। सही この本.',
            'zh': '中文「这本书」对应「この本」，不是「これ本」。中国学习者初期常误用 これ 替代 この。',
        },
    },
    'n5-016': {
        'meaning': {
            'vi': 'Từ chỉ địa điểm: ここ / そこ / あそこ / どこ (ở đây / ở đó / ở kia / ở đâu)',
            'id': 'Kata lokasi: ここ / そこ / あそこ / どこ (di sini / di situ / di sana / di mana)',
            'ne': 'स्थान शब्द: ここ / そこ / あそこ / どこ (यहाँ / त्यहाँ / उहाँ / कहाँ)',
            'zh': '地点词：ここ / そこ / あそこ / どこ（这里 / 那里(近) / 那里(远) / 哪里）',
        },
        'explanation': {
            'vi': 'Đây là bộ từ chỉ địa điểm theo cùng quy tắc khoảng cách. Dùng làm chủ ngữ hoặc tân ngữ: ここはトイレです "đây là nhà vệ sinh", ここで食べる "ăn ở đây". Lưu ý あそこ (không phải あこ).',
            'id': 'Ini adalah set kata lokasi dengan aturan jarak yang sama. Dipakai sebagai subjek atau objek: ここはトイレです "ini toilet", ここで食べる "makan di sini". Perhatikan あそこ (bukan あこ).',
            'ne': 'यो उही दूरी नियम भएको स्थान शब्दहरूको सेट हो। कर्ता वा कर्मको रूपमा प्रयोग: ここはトイレです "यो शौचालय हो", ここで食べる "यहाँ खाने"। あそこ (あこ होइन) ध्यान दिनुहोस्।',
            'zh': '这是按相同距离规则的地点词组。可作主语或宾语：ここはトイレです "这里是洗手间"，ここで食べる "在这里吃"。注意是 あそこ 不是 あこ。',
        },
    },
    'n5-017': {
        'meaning': {
            'vi': 'なに / なん (cái gì - phát âm thay đổi tùy ngữ cảnh)',
            'id': 'なに / なん (apa - pengucapan berubah tergantung konteks)',
            'ne': 'なに / なん (के - सन्दर्भ अनुसार उच्चारण फरक)',
            'zh': 'なに / なん（什么 - 读音随上下文变化）',
        },
        'explanation': {
            'vi': '何 đọc là なに hoặc なん tùy theo từ theo sau: trước /d/, /n/, /t/, hoặc đếm số → なん (なんですか, なんにん). Trước các âm khác → なに (なにを, なにが). Là từ hỏi cơ bản nhất ở N5.',
            'id': '何 dibaca なに atau なん tergantung kata setelahnya: sebelum /d/, /n/, /t/, atau hitungan → なん (なんですか, なんにん). Sebelum suara lain → なに (なにを, なにが). Kata tanya paling dasar di N5.',
            'ne': '何 को उच्चारण पछि आउने शब्द अनुसार なに वा なん हुन्छ: /d/, /n/, /t/, वा गणना अघि → なん (なんですか, なんにん)। अन्य आवाज अघि → なに (なにを, なにが)। N5 को सबैभन्दा आधारभूत प्रश्न शब्द।',
            'zh': '何 根据后续音读作 なに 或 なん：/d/、/n/、/t/ 或量词前 → なん（なんですか、なんにん）；其他音前 → なに（なにを、なにが）。N5 最基本的疑问词。',
        },
    },
    'n5-018': {
        'meaning': {
            'vi': 'だれ / どなた (ai - だれ thân mật; どなた lịch sự)',
            'id': 'だれ / どなた (siapa - だれ kasual; どなた sopan)',
            'ne': 'だれ / どなた (को - だれ अनौपचारिक; どなた आदर)',
            'zh': 'だれ / どなた（谁 - だれ 普通；どなた 尊敬）',
        },
        'explanation': {
            'vi': 'だれ là dạng cơ bản. どなた là dạng lịch sự, dùng khi hỏi tên người không quen hoặc khách hàng. Cả hai không đi với さん (誰さん là sai).',
            'id': 'だれ adalah bentuk dasar. どなた adalah bentuk sopan, dipakai saat menanyakan nama orang yang tidak dikenal atau pelanggan. Keduanya tidak dengan さん (誰さん salah).',
            'ne': 'だれ आधारभूत रूप हो। どなた आदरयुक्त रूप, अपरिचित व्यक्ति वा ग्राहकको नाम सोध्दा प्रयोग। दुवै सँग さん जोडिन्न (誰さん गलत)।',
            'zh': 'だれ 是基本形式。どなた 是敬语形式，用于询问陌生人或客户的姓名。两者都不接 さん（誰さん 错误）。',
        },
    },
    'n5-019': {
        'meaning': {
            'vi': 'いつ (khi nào - đi với から / まで / ごろ để hỏi thời gian chi tiết)',
            'id': 'いつ (kapan - dipakai dengan から / まで / ごろ untuk pertanyaan waktu lebih detail)',
            'ne': 'いつ (कहिले - から / まで / ごろ सँग समय विस्तृत प्रश्नको लागि)',
            'zh': 'いつ（什么时候 - 与 から / まで / ごろ 配合提问更详细的时间）',
        },
        'explanation': {
            'vi': 'いつ là từ hỏi thời gian cơ bản. Khi muốn cụ thể: いつから ("từ khi nào"), いつまで ("đến khi nào"), いつごろ ("khoảng khi nào"). いつ không cần trợ từ に sau nó (いつ来ますか không phải いつに).',
            'id': 'いつ adalah kata tanya waktu dasar. Untuk lebih spesifik: いつから ("dari kapan"), いつまで ("sampai kapan"), いつごろ ("sekitar kapan"). いつ tidak butuh partikel に setelahnya (いつ来ますか bukan いつに).',
            'ne': 'いつ आधारभूत समय प्रश्न शब्द हो। थप विशिष्टको लागि: いつから ("कहिले देखि"), いつまで ("कहिले सम्म"), いつごろ ("करिब कहिले")। いつ पछि に जोडिँदैन (いつ来ますか, いつに होइन)।',
            'zh': 'いつ 是基本时间疑问词。要更具体：いつから（从何时）、いつまで（到何时）、いつごろ（大约何时）。いつ 后不接 に（いつ来ますか，不是 いつに）。',
        },
    },
    'n5-021': {
        'meaning': {
            'vi': 'から ～ まで (từ X đến Y - đánh dấu phạm vi đôi, thời gian hoặc không gian)',
            'id': 'から ～ まで (dari X sampai Y - menandai rentang ganda, waktu atau ruang)',
            'ne': 'から ～ まで (X देखि Y सम्म - दोहोरो सीमा चिन्ह, समय वा स्थान)',
            'zh': 'から ～ まで（从 X 到 Y - 双重范围标记，时间或空间）',
        },
        'explanation': {
            'vi': 'Cặp X から Y まで đánh dấu phạm vi đầy đủ trong thời gian (九時から五時まで "từ 9 đến 5 giờ") hoặc không gian (東京から大阪まで "từ Tokyo đến Osaka"). Cả hai trợ từ thường xuất hiện cùng nhau.',
            'id': 'Pasangan X から Y まで menandai rentang lengkap dalam waktu (九時から五時まで "dari jam 9 sampai 5") atau ruang (東京から大阪まで "dari Tokyo sampai Osaka"). Kedua partikel biasanya muncul bersama.',
            'ne': 'X から Y まで जोडीले समय (九時から五時まで "९ देखि ५ बजे") वा स्थान (東京から大阪まで "टोकियो देखि ओसाका") को पूरा सीमा जनाउँछ। दुवै कण सँगै आउँछन्।',
            'zh': 'X から Y まで 配对标示时间（九時から五時まで "从9点到5点"）或空间（東京から大阪まで "从东京到大阪"）的完整范围。两个助词常成对出现。',
        },
    },
    'n5-023': {
        'meaning': {
            'vi': 'か (trợ từ cuối câu hỏi)',
            'id': 'か (partikel akhir pertanyaan)',
            'ne': 'か (प्रश्न वाक्य अन्त्य कण)',
            'zh': 'か（句末疑问助词）',
        },
        'explanation': {
            'vi': 'か thêm vào cuối câu để biến nó thành câu hỏi. Trong tiếng Nhật lịch sự (です/ます), không cần dấu chấm hỏi - か đã đủ. (これは本です + か = これは本ですか). Trong văn phong thân mật, dấu hỏi đôi khi đi với か hoặc thay か.',
            'id': 'か ditambahkan di akhir kalimat untuk menjadikannya pertanyaan. Dalam bahasa Jepang sopan (です/ます), tidak butuh tanda tanya - か sudah cukup. (これは本です + か = これは本ですか). Dalam gaya kasual, tanda tanya kadang menyertai か atau menggantikannya.',
            'ne': 'か वाक्यको अन्त्यमा जोडेर प्रश्न बनाइन्छ। विनम्र जापानीमा (です/ます), प्रश्न चिन्ह आवश्यक छैन - か पर्याप्त छ। (これは本です + か = これは本ですか)। अनौपचारिक शैलीमा प्रश्न चिन्ह か सँगै वा か को सट्टा आउँछ।',
            'zh': 'か 加在句末使其成为疑问句。礼貌日语（です/ます）不需问号--か 即可。(これは本です + か = これは本ですか)。口语中问号有时与 か 同用或代替 か。',
        },
    },
    'n5-024': {
        'meaning': {
            'vi': 'か (hoặc - giữa các lựa chọn)',
            'id': 'か (atau - di antara pilihan)',
            'ne': 'か (वा - विकल्पहरूको बीच)',
            'zh': 'か（或 - 在选项之间）',
        },
        'explanation': {
            'vi': 'か giữa hai danh từ có nghĩa "hoặc" (パンかミルク "bánh mì hoặc sữa"). Khác với か cuối câu hỏi. Có thể nối nhiều lựa chọn: パンかミルクかコーヒー. Để hỏi "X hay Y?" dùng XかY (どちら)ですか.',
            'id': 'か di antara dua kata benda berarti "atau" (パンかミルク "roti atau susu"). Berbeda dari か akhir pertanyaan. Bisa menghubungkan beberapa pilihan: パンかミルクかコーヒー. Untuk tanya "X atau Y?" pakai XかY (どちら)ですか.',
            'ne': 'दुई संज्ञाको बीच か को अर्थ "वा" हो (パンかミルク "रोटी वा दूध")। प्रश्न अन्त्य か सँग फरक। धेरै विकल्प जोड्न सक्नुहुन्छ: パンかミルクかコーヒー। "X वा Y?" सोध्न XかY (どちら)ですか।',
            'zh': '两个名词间的 か 表示"或"（パンかミルク "面包或牛奶"）。与句末疑问 か 不同。可连接多个选项：パンかミルクかコーヒー。问"X 还是 Y？"用 XかY (どちら)ですか。',
        },
    },
    'n5-025': {
        'meaning': {
            'vi': 'ね (trợ từ cuối câu xác nhận / tìm sự đồng tình)',
            'id': 'ね (partikel akhir kalimat konfirmasi / mencari persetujuan)',
            'ne': 'ね (वाक्य अन्त्य पुष्टि / सहमति खोज्ने कण)',
            'zh': 'ね（句末确认 / 寻求同意助词）',
        },
        'explanation': {
            'vi': 'ね ở cuối câu mời người nghe đồng tình ("phải không?", "đúng không?"). きれいですね "đẹp nhỉ?" Khác với よ (khẳng định cho người nghe). Tone thân thiện, rất thường gặp trong hội thoại.',
            'id': 'ね di akhir kalimat mengundang lawan bicara untuk setuju ("kan?", "ya?"). きれいですね "indah ya?" Berbeda dari よ (asersi untuk lawan bicara). Nada ramah, sangat umum dalam percakapan.',
            'ne': 'ね ले वाक्यको अन्त्यमा श्रोतालाई सहमति माग्छ ("होइन र?", "हो हो")। きれいですね "राम्रो छ है?" よ (श्रोतालाई दाबी) सँग फरक। मित्रवत् स्वर, बोलचालमा धेरै सामान्य।',
            'zh': '句末 ね 邀请对方同意（"对吧？""是吗？"）。きれいですね "真漂亮啊"。与 よ（向对方断言）不同。友好语气，对话中极为常见。',
        },
    },
    'n5-026': {
        'meaning': {
            'vi': 'よ (trợ từ cuối câu khẳng định / thông tin mới)',
            'id': 'よ (partikel akhir kalimat asersi / informasi baru)',
            'ne': 'よ (वाक्य अन्त्य दाबी / नयाँ जानकारी कण)',
            'zh': 'よ（句末断言 / 提供新信息助词）',
        },
        'explanation': {
            'vi': 'よ ở cuối câu nhấn mạnh thông tin mới cho người nghe ("đấy", "cơ"). 雨が降っていますよ "đang mưa đấy". Khác với ね (tìm đồng tình). Dùng quá nhiều có thể nghe áp đặt; dùng đúng giúp giao tiếp mạch lạc.',
            'id': 'よ di akhir kalimat menekankan informasi baru ke lawan bicara ("loh", "kok"). 雨が降っていますよ "loh hujan". Berbeda dari ね (cari persetujuan). Pakai terlalu banyak terdengar memaksa; pakai tepat membantu komunikasi mengalir.',
            'ne': 'よ ले वाक्यको अन्त्यमा श्रोतालाई नयाँ जानकारीमा जोड दिन्छ ("नि", "त")। 雨が降っていますよ "पानी परिरहेको छ नि"। ね (सहमति खोज्ने) सँग फरक। धेरै प्रयोगले थोपर्ने जस्तो; ठीक प्रयोगले संवाद बहाव मद्दत।',
            'zh': '句末 よ 强调对听者的新信息（"哦"、"呢"）。雨が降っていますよ "在下雨呢"。与 ね（寻求同意）不同。过度使用显得强硬；恰当使用有助于对话流畅。',
        },
    },
    'n5-027': {
        'meaning': {
            'vi': 'よね (kết hợp: khẳng định + tìm đồng tình)',
            'id': 'よね (gabungan: asersi + cari persetujuan)',
            'ne': 'よね (संयोजन: दाबी + सहमति खोज्ने)',
            'zh': 'よね（组合：断言 + 寻求同意）',
        },
        'explanation': {
            'vi': 'よね kết hợp よ (khẳng định) + ね (tìm đồng tình): "đúng không nhỉ?" Người nói tin chắc nhưng vẫn muốn xác nhận. 日本人ですよね "anh là người Nhật, đúng không?" Khác với chỉ ね (mức độ chắc chắn thấp hơn).',
            'id': 'よね menggabungkan よ (asersi) + ね (cari persetujuan): "benar kan?" Penutur yakin tapi ingin konfirmasi. 日本人ですよね "Anda orang Jepang, kan?" Berbeda dari hanya ね (tingkat kepastian lebih rendah).',
            'ne': 'よね ले よ (दाबी) + ね (सहमति) जोड्छ: "होइन र?" वक्ता पक्का छ तर पुष्टि चाहन्छ। 日本人ですよね "तपाईं जापानी हो, होइन?" खालि ね (कम निश्चितता) सँग फरक।',
            'zh': 'よね 组合 よ（断言）+ ね（寻求同意）："是吧？"说话者确信但想确认。日本人ですよね "你是日本人，对吧？"与单独 ね（确信度较低）不同。',
        },
    },
    'n5-028': {
        'meaning': {
            'vi': '〜の (trợ từ sở hữu / bổ ngữ danh từ)',
            'id': '〜の (partikel posesif / pemodifikasi nomina)',
            'ne': '〜の (स्वामित्व कण / संज्ञा उपसर्ग)',
            'zh': '〜の（属格 / 名词修饰助词）',
        },
        'explanation': {
            'vi': 'の nối hai danh từ - danh từ đầu mô tả hoặc sở hữu danh từ thứ hai. 私の本 "sách của tôi", 日本の食べ物 "thức ăn Nhật". Tương đương với "của" trong tiếng Việt nhưng dùng phổ quát hơn (không chỉ sở hữu).',
            'id': 'の menghubungkan dua kata benda - KB pertama menjelaskan atau memiliki KB kedua. 私の本 "buku saya", 日本の食べ物 "makanan Jepang". Setara dengan "punya" di Indonesia tapi dipakai lebih luas (tidak hanya kepemilikan).',
            'ne': 'の दुई संज्ञा जोड्छ - पहिलो संज्ञाले दोस्रोलाई वर्णन गर्छ वा स्वामित्व जनाउँछ। 私の本 "मेरो किताब", 日本の食べ物 "जापानी खाना"। नेपाली "को" जस्तै तर थप व्यापक।',
            'zh': 'の 连接两个名词 - 第一个名词修饰或拥有第二个名词。私の本 "我的书"、日本の食べ物 "日本的食物"。类似中文「的」但用法更广。',
        },
        'l1_notes': {
            'zh': '中文「的」与日语 の 极相似，导致中国学习者容易过度使用 の。但日语形容词不接 の：「红的书」是「赤い本」，不是「赤いの本」。「漂亮的人」是「きれいな人」，不是「きれいなの人」。这是中国学习者最高频的 N5 错误。',
            'vi': 'Tiếng Việt "của" hẹp hơn の. Lưu ý tính từ tiếng Nhật KHÔNG đi với の: "sách đỏ" là 赤い本, không phải 赤いの本.',
            'id': 'Bahasa Indonesia tidak punya partikel posesif universal. Hati-hati: kata sifat tidak diikuti の: "buku merah" adalah 赤い本, bukan 赤いの本.',
            'ne': 'नेपाली "को" र जापानी の समान हुन् तर विशेषण पछि の आउँदैन: "रातो किताब" は 赤い本, 赤いの本 होइन।',
        },
    },
    'n5-029': {
        'meaning': {
            'vi': 'Sở hữu / bổ ngữ danh từ',
            'id': 'Posesif / pemodifikasi nomina',
            'ne': 'स्वामित्व / संज्ञा उपसर्ग',
            'zh': '属格 / 名词修饰',
        },
        'explanation': {
            'vi': 'Là biến thể của 〜の. Xem n5-028 để biết chi tiết. の có thể chỉ sở hữu, mô tả nguồn gốc, vai trò hoặc thuộc tính của danh từ kia.',
            'id': 'Adalah varian dari 〜の. Lihat n5-028 untuk detail. の bisa menunjukkan kepemilikan, asal, peran, atau atribut kata benda lain.',
            'ne': 'यो 〜の को रूप हो। विवरणको लागि n5-028 हेर्नुहोस्। の ले स्वामित्व, मूल, भूमिका, वा अरू संज्ञाको गुण देखाउन सक्छ।',
            'zh': '是 〜の 的变体。详情见 n5-028。の 可标示所有、来源、角色或对方名词的属性。',
        },
    },
    'n5-030': {
        'meaning': {
            'vi': '〜の (danh từ hóa - biến mệnh đề thành danh từ)',
            'id': '〜の (nominalisator - mengubah klausa menjadi kata benda)',
            'ne': '〜の (नामकरण - उपवाक्यलाई संज्ञा बनाउने)',
            'zh': '〜の（名词化 - 将子句转为名词）',
        },
        'explanation': {
            'vi': 'の sau dạng từ điển của động từ hoặc tính từ biến cả mệnh đề thành một danh từ ("việc làm X"). 日本語を勉強するのが好きです "tôi thích việc học tiếng Nhật". Khác với の sở hữu - nominalize chuyển toàn bộ động từ thành noun phrase.',
            'id': 'の setelah bentuk kamus kata kerja atau kata sifat mengubah seluruh klausa menjadi kata benda ("hal melakukan X"). 日本語を勉強するのが好きです "saya suka belajar bahasa Jepang". Berbeda dari の posesif - nominalize mengubah seluruh kata kerja menjadi frasa nomina.',
            'ne': 'क्रिया वा विशेषणको शब्दकोश रूप पछि の ले उपवाक्यलाई संज्ञामा रूपान्तरण गर्छ ("X गर्ने कुरा")। 日本語を勉強するのが好きです "जापानी भाषा पढ्ने मन पर्छ"। स्वामित्व の सँग फरक।',
            'zh': '动词或形容词字典形后接 の 将整个子句名词化（"做 X 的事"）。日本語を勉強するのが好きです "我喜欢学日语"。与所有格 の 不同--nominalize 将整个动词转为名词性词组。',
        },
    },
}


def main() -> int:
    data = json.loads(GF.read_text(encoding='utf-8'))
    n_meaning = 0
    n_explanation = 0
    n_l1notes = 0
    matched = set()

    for p in data.get('patterns', []):
        pid = p.get('id')
        if pid not in TRANSLATIONS:
            continue
        spec = TRANSLATIONS[pid]

        # meaning_{lc}
        for lc, txt in spec['meaning'].items():
            field = f'meaning_{lc}'
            if p.get(field) != txt:
                p[field] = txt
                n_meaning += 1
        if 'meaning_provenance' not in p:
            p['meaning_provenance'] = 'machine_translated'

        # explanation_{lc}
        for lc, txt in spec['explanation'].items():
            field = f'explanation_{lc}'
            if p.get(field) != txt:
                p[field] = txt
                n_explanation += 1
        if 'explanation_provenance' not in p:
            p['explanation_provenance'] = 'machine_translated'

        # l1_notes (top-15 only)
        if 'l1_notes' in spec:
            existing = p.get('l1_notes') or {}
            if not isinstance(existing, dict):
                existing = {}
            for lc, txt in spec['l1_notes'].items():
                if existing.get(lc) != txt:
                    existing[lc] = txt
                    n_l1notes += 1
            p['l1_notes'] = existing

        matched.add(pid)

    GF.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    total = len(data.get('patterns', []))
    nm = sum(1 for p in data['patterns'] if p.get('meaning_vi'))
    ne = sum(1 for p in data['patterns'] if p.get('explanation_vi'))
    nl = sum(1 for p in data['patterns'] if p.get('l1_notes'))
    print(f'[ISSUE-056 + IMP-080] Grammar localization batch')
    print(f'  Patterns matched:   {len(matched)} of {len(TRANSLATIONS)} planned')
    print(f'  meaning_<lc> writes:    {n_meaning} (now {nm}/{total})')
    print(f'  explanation_<lc> writes:{n_explanation} (now {ne}/{total})')
    print(f'  l1_notes writes:        {n_l1notes} (now {nl}/{total} patterns have any l1_notes)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
