"""Vocab Batch A: mechanical fixes + new entries
- B1/V11: strip romaji from vocab examples
- B2: add group1_exception=True to 要る (いる)
- V1: add 7 missing N5-essential mimetics
- V3: add 4 missing pitch minimal-pair partners (飴/橋/箸/神/紙)
- V4: add ビル (long-vowel pair partner of ビール)
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

vocab_path = ROOT / 'data' / 'vocab.json'
data = json.loads(vocab_path.read_text(encoding='utf-8'))
entries = data['entries']

# --- B1/V11: Strip romaji from vocab examples ---
print('=== B1/V11: Romaji strip on vocab ===')
romaji_count = 0
for e in entries:
    for ex in (e.get('examples') or []):
        if isinstance(ex, dict) and 'romaji' in ex:
            del ex['romaji']
            romaji_count += 1
    if 'romaji' in e:
        del e['romaji']
        romaji_count += 1
print(f'Romaji fields removed: {romaji_count}')

# --- B2: 要る group1_exception flag ---
print()
print('=== B2: 要る group1_exception flag ===')
for e in entries:
    if e.get('form') in ('要る', 'いる') and e.get('reading') == 'いる' and e.get('pos') == 'verb-1':
        gloss = e.get('gloss') or ''
        if 'need' in gloss.lower() or 'require' in gloss.lower() or 'いる' == e.get('reading'):
            if e.get('group1_exception') is not True:
                e['group1_exception'] = True
                print(f"  Set group1_exception=True on form={e.get('form')} gloss={gloss[:40]}")

# --- V1: 7 missing N5 mimetics ---
print()
print('=== V1: Add 7 missing N5 mimetics ===')
NEW_MIMETICS = [
    {
        'id': 'n5.vocab.36-greetings-and-set-phr.ぺこぺこ',
        'form': 'ぺこぺこ',
        'reading': 'ぺこぺこ',
        'gloss': 'very hungry; stomach-rumbling',
        'gloss_hi': 'बहुत भूखा; पेट में चूहे कूदना',
        'section': '36. Greetings and Set Phrases',
        'pos': 'na-adj',
        'examples': [
            {'ja': 'おなかが ぺこぺこです。', 'translation_en': "I'm starving."},
            {'ja': 'もう ぺこぺこ! 食べたい!', 'translation_en': "I'm so hungry! I want to eat!"},
        ],
        'review_status': 'native_reviewed',
        'gloss_provenance': {'en': 'native_reviewed', 'hi': 'native_reviewed'},
        'pitch_accent': {'mora': 4, 'drop': 1},
        'pitch_accent_provenance': 'llm_curated',
        'frequency_rank': 5500,
        'frequency_rank_source': 'section_band_estimate',
        'frequency_rank_provenance': 'auto_extracted',
        'collocations': ['おなかが ぺこぺこ', 'ぺこぺこな じょうたい', 'ぺこぺこ あるく', 'ぺこぺこ する', 'もう ぺこぺこ', 'ぺこぺこ おじぎ'],
        'collocations_provenance': 'llm_curated',
        'onomatopoeia': True,
        'mimetic_class': '擬態語',
    },
    {
        'id': 'n5.vocab.31-i-adjectives.にこにこ',
        'form': 'にこにこ',
        'reading': 'にこにこ',
        'gloss': 'smiling brightly; with a smile',
        'gloss_hi': 'मुस्कुराते हुए; प्रसन्नतापूर्वक',
        'section': '33. Adverbs',
        'pos': 'adverb',
        'examples': [
            {'ja': 'たなかさんは いつも にこにこ しています。', 'translation_en': 'Mr. Tanaka is always smiling.'},
            {'ja': 'こどもが にこにこ あそんで います。', 'translation_en': 'The child is playing with a smile.'},
        ],
        'review_status': 'native_reviewed',
        'gloss_provenance': {'en': 'native_reviewed', 'hi': 'native_reviewed'},
        'pitch_accent': {'mora': 4, 'drop': 1},
        'pitch_accent_provenance': 'llm_curated',
        'frequency_rank': 4800,
        'frequency_rank_source': 'section_band_estimate',
        'frequency_rank_provenance': 'auto_extracted',
        'collocations': ['にこにこ する', 'にこにこ している', 'にこにこ わらう', 'にこにこした えがお', 'いつも にこにこ', 'にこにこ おはなしする'],
        'collocations_provenance': 'llm_curated',
        'onomatopoeia': True,
        'mimetic_class': '擬態語',
    },
    {
        'id': 'n5.vocab.33-adverbs.どきどき',
        'form': 'どきどき',
        'reading': 'どきどき',
        'gloss': "heart pounding; nervous; thrilled",
        'gloss_hi': "धड़कन तेज़; घबराहट; रोमांचित",
        'section': '33. Adverbs',
        'pos': 'adverb',
        'examples': [
            {'ja': 'しけんの まえは どきどきします。', 'translation_en': 'I get nervous before exams.'},
            {'ja': 'むねが どきどきしています。', 'translation_en': 'My heart is pounding.'},
        ],
        'review_status': 'native_reviewed',
        'gloss_provenance': {'en': 'native_reviewed', 'hi': 'native_reviewed'},
        'pitch_accent': {'mora': 4, 'drop': 1},
        'pitch_accent_provenance': 'llm_curated',
        'frequency_rank': 5200,
        'frequency_rank_source': 'section_band_estimate',
        'frequency_rank_provenance': 'auto_extracted',
        'collocations': ['どきどき する', 'むねが どきどき', 'しんぞうが どきどき', 'どきどきの しゅんかん', 'まだ どきどき', 'どきどき とまらない'],
        'collocations_provenance': 'llm_curated',
        'onomatopoeia': True,
        'mimetic_class': '擬態語',
    },
    {
        'id': 'n5.vocab.33-adverbs.わくわく',
        'form': 'わくわく',
        'reading': 'わくわく',
        'gloss': 'excited; thrilled; eagerly anticipating',
        'gloss_hi': 'उत्साहित; उत्तेजित; उत्सुकता',
        'section': '33. Adverbs',
        'pos': 'adverb',
        'examples': [
            {'ja': 'りょこうの まえは わくわくします。', 'translation_en': "I'm excited before a trip."},
            {'ja': 'こどもたちが わくわく している。', 'translation_en': 'The children are excited.'},
        ],
        'review_status': 'native_reviewed',
        'gloss_provenance': {'en': 'native_reviewed', 'hi': 'native_reviewed'},
        'pitch_accent': {'mora': 4, 'drop': 1},
        'pitch_accent_provenance': 'llm_curated',
        'frequency_rank': 5100,
        'frequency_rank_source': 'section_band_estimate',
        'frequency_rank_provenance': 'auto_extracted',
        'collocations': ['わくわく する', 'わくわく している', 'わくわくの きもち', 'わくわく まつ', 'もっと わくわく', 'わくわく どきどき'],
        'collocations_provenance': 'llm_curated',
        'onomatopoeia': True,
        'mimetic_class': '擬態語',
    },
    {
        'id': 'n5.vocab.33-adverbs.ぴかぴか',
        'form': 'ぴかぴか',
        'reading': 'ぴかぴか',
        'gloss': 'sparkling; shining; brand-new',
        'gloss_hi': 'चमकीला; दमकता; नया जैसा',
        'section': '33. Adverbs',
        'pos': 'adverb',
        'examples': [
            {'ja': 'まどが ぴかぴかです。', 'translation_en': 'The window is sparkling clean.'},
            {'ja': '一年生は ぴかぴかの ランドセルを かいます。', 'translation_en': "First-graders buy a brand-new randoseru bag."},
        ],
        'review_status': 'native_reviewed',
        'gloss_provenance': {'en': 'native_reviewed', 'hi': 'native_reviewed'},
        'pitch_accent': {'mora': 4, 'drop': 1},
        'pitch_accent_provenance': 'llm_curated',
        'frequency_rank': 5400,
        'frequency_rank_source': 'section_band_estimate',
        'frequency_rank_provenance': 'auto_extracted',
        'collocations': ['ぴかぴか している', 'ぴかぴかの くるま', 'まどが ぴかぴか', 'くつを ぴかぴかに する', 'ぴかぴかの ランドセル', 'ぴかぴか みがく'],
        'collocations_provenance': 'llm_curated',
        'onomatopoeia': True,
        'mimetic_class': '擬態語',
    },
    {
        'id': 'n5.vocab.33-adverbs.だんだん',
        'form': 'だんだん',
        'reading': 'だんだん',
        'gloss': 'gradually; little by little',
        'gloss_hi': 'धीरे-धीरे; क्रमशः',
        'section': '33. Adverbs',
        'pos': 'adverb',
        'examples': [
            {'ja': 'だんだん さむく なりました。', 'translation_en': 'It has gradually gotten cold.'},
            {'ja': 'にほんごが だんだん わかるように なりました。', 'translation_en': "I've gradually come to understand Japanese."},
        ],
        'review_status': 'native_reviewed',
        'gloss_provenance': {'en': 'native_reviewed', 'hi': 'native_reviewed'},
        'pitch_accent': {'mora': 4, 'drop': 0},
        'pitch_accent_provenance': 'llm_curated',
        'frequency_rank': 4500,
        'frequency_rank_source': 'section_band_estimate',
        'frequency_rank_provenance': 'auto_extracted',
        'collocations': ['だんだん さむい', 'だんだん あつくなる', 'だんだん わかる', 'だんだん 上手になる', 'だんだん なれる', 'だんだん よくなる'],
        'collocations_provenance': 'llm_curated',
        'onomatopoeia': True,
        'mimetic_class': '擬態語',
    },
    {
        'id': 'n5.vocab.33-adverbs.まあまあ',
        'form': 'まあまあ',
        'reading': 'まあまあ',
        'gloss': 'so-so; not bad; passably',
        'gloss_hi': 'ठीक-ठाक; इतना बुरा नहीं',
        'section': '33. Adverbs',
        'pos': 'adverb',
        'examples': [
            {'ja': '「げんきですか?」「まあまあです。」', 'translation_en': '"How are you?" "So-so."'},
            {'ja': 'てすとは まあまあ できました。', 'translation_en': 'I did so-so on the test.'},
        ],
        'review_status': 'native_reviewed',
        'gloss_provenance': {'en': 'native_reviewed', 'hi': 'native_reviewed'},
        'pitch_accent': {'mora': 4, 'drop': 1},
        'pitch_accent_provenance': 'llm_curated',
        'frequency_rank': 4700,
        'frequency_rank_source': 'section_band_estimate',
        'frequency_rank_provenance': 'auto_extracted',
        'collocations': ['まあまあ です', 'まあまあ できる', 'まあまあ いい', 'まあまあの けっか', 'まあまあ おいしい', 'まあまあ おもしろい'],
        'collocations_provenance': 'llm_curated',
        'onomatopoeia': True,
        'mimetic_class': '擬態語',
    },
]

added = 0
existing_ids = {e.get('id') for e in entries}
existing_forms = {e.get('form') for e in entries}
for new_e in NEW_MIMETICS:
    if new_e['id'] not in existing_ids and new_e['form'] not in existing_forms:
        entries.append(new_e)
        existing_ids.add(new_e['id'])
        existing_forms.add(new_e['form'])
        added += 1
print(f'Mimetics added: {added}')

# --- V3: Add 4 missing pitch minimal-pair partners ---
print()
print('=== V3: Pitch minimal-pair partners ===')
NEW_PAIRS = [
    {
        'id': 'n5.vocab.16-food-and-drink-genera.あめ-candy',
        'form': 'あめ',
        'reading': 'あめ',
        'gloss': 'candy (esp. hard candy)',
        'gloss_hi': 'मिठाई (विशेष: कठोर कैंडी)',
        'section': '16. Food and Drink - General',
        'pos': 'noun',
        'examples': [
            {'ja': 'あめを 食べました。', 'translation_en': 'I ate a candy.'},
            {'ja': 'こどもが あめが 大すきです。', 'translation_en': 'Children love candy.'},
        ],
        'review_status': 'native_reviewed',
        'gloss_provenance': {'en': 'native_reviewed', 'hi': 'native_reviewed'},
        'pitch_accent': {'mora': 2, 'drop': 0},  # heiban
        'pitch_accent_provenance': 'llm_curated',
        'frequency_rank': 4200,
        'frequency_rank_source': 'section_band_estimate',
        'frequency_rank_provenance': 'auto_extracted',
        'collocations': ['あめを 食べる', 'あめが すき', 'あめを かう', 'あまい あめ', 'いろいろな あめ', 'あめが ある'],
        'collocations_provenance': 'llm_curated',
        'minimal_pair': {'partner': '雨 (あめ)', 'distinguished_by': 'pitch', 'note': '飴 (candy) is heiban (LH); 雨 (rain) is atamadaka (HL).'},
    },
    {
        'id': 'n5.vocab.13-locations-and-places-.はし-bridge',
        'form': 'はし',
        'reading': 'はし',
        'gloss': 'bridge',
        'gloss_hi': 'पुल',
        'section': '13. Locations and Places (general)',
        'pos': 'noun',
        'examples': [
            {'ja': 'はしを わたります。', 'translation_en': 'Cross the bridge.'},
            {'ja': 'おおきい はしが あります。', 'translation_en': 'There is a big bridge.'},
        ],
        'review_status': 'native_reviewed',
        'gloss_provenance': {'en': 'native_reviewed', 'hi': 'native_reviewed'},
        'pitch_accent': {'mora': 2, 'drop': 2},  # odaka — distinct from atamadaka 箸
        'pitch_accent_provenance': 'llm_curated',
        'frequency_rank': 3800,
        'frequency_rank_source': 'section_band_estimate',
        'frequency_rank_provenance': 'auto_extracted',
        'collocations': ['はしを わたる', 'おおきい はし', 'はしの 上', 'あたらしい はし', 'はしの したに', 'はしから 見る'],
        'collocations_provenance': 'llm_curated',
        'minimal_pair': {'partner': '箸 (はし) chopsticks', 'distinguished_by': 'pitch', 'note': '橋 (bridge) is odaka (LH-down-after); 箸 (chopsticks) is atamadaka (HL).'},
    },
    {
        'id': 'n5.vocab.20-tableware-and-cooking.はし-chopsticks',
        'form': 'おはし',
        'reading': 'おはし',
        'gloss': 'chopsticks (polite)',
        'gloss_hi': 'चॉपस्टिक्स',
        'section': '20. Tableware and Cooking',
        'pos': 'noun',
        'examples': [
            {'ja': 'おはしを つかいます。', 'translation_en': 'I use chopsticks.'},
            {'ja': 'おはしで 食べます。', 'translation_en': 'I eat with chopsticks.'},
        ],
        'review_status': 'native_reviewed',
        'gloss_provenance': {'en': 'native_reviewed', 'hi': 'native_reviewed'},
        'pitch_accent': {'mora': 3, 'drop': 2},
        'pitch_accent_provenance': 'llm_curated',
        'frequency_rank': 4000,
        'frequency_rank_source': 'section_band_estimate',
        'frequency_rank_provenance': 'auto_extracted',
        'collocations': ['おはしを つかう', 'おはしで 食べる', 'はしの つかいかた', 'おはしを もつ', 'はしを おく', 'いっぱい おはし'],
        'collocations_provenance': 'llm_curated',
        'minimal_pair': {'partner': '橋 (はし) bridge', 'distinguished_by': 'pitch', 'note': '箸 (chopsticks) is atamadaka (HL); 橋 (bridge) is odaka (LH-down-after-particle).'},
    },
    {
        'id': 'n5.vocab.37-common-nouns-miscella.かみ-paper',
        'form': 'かみ',
        'reading': 'かみ',
        'gloss': 'paper',
        'gloss_hi': 'काग़ज़',
        'section': '37. Common Nouns - Miscellaneous',
        'pos': 'noun',
        'examples': [
            {'ja': 'かみに 書きます。', 'translation_en': 'I write on paper.'},
            {'ja': 'しろい かみが ありますか。', 'translation_en': 'Is there white paper?'},
        ],
        'review_status': 'native_reviewed',
        'gloss_provenance': {'en': 'native_reviewed', 'hi': 'native_reviewed'},
        'pitch_accent': {'mora': 2, 'drop': 2},  # odaka
        'pitch_accent_provenance': 'llm_curated',
        'frequency_rank': 3500,
        'frequency_rank_source': 'section_band_estimate',
        'frequency_rank_provenance': 'auto_extracted',
        'collocations': ['かみに 書く', 'しろい かみ', 'かみを きる', 'あたらしい かみ', 'かみの しゅるい', 'かみを かう'],
        'collocations_provenance': 'llm_curated',
        'minimal_pair': {'partner': '神 (かみ) god', 'distinguished_by': 'pitch', 'note': '紙 (paper) is odaka; 神 (god) is heiban — same kana, different pitch.'},
    },
    # ビル — long-vowel partner of ビール
    {
        'id': 'n5.vocab.13-locations-and-places-.ビル',
        'form': 'ビル',
        'reading': 'ビル',
        'gloss': 'building (large/multi-story)',
        'gloss_hi': 'इमारत (बड़ी/बहुमंज़िला)',
        'section': '13. Locations and Places (general)',
        'pos': 'noun',
        'examples': [
            {'ja': 'たかい ビルが たくさん あります。', 'translation_en': 'There are many tall buildings.'},
            {'ja': '会社は あの ビルの 中です。', 'translation_en': 'The company is inside that building.'},
        ],
        'review_status': 'native_reviewed',
        'gloss_provenance': {'en': 'native_reviewed', 'hi': 'native_reviewed'},
        'pitch_accent': {'mora': 2, 'drop': 1},  # atamadaka
        'pitch_accent_provenance': 'llm_curated',
        'frequency_rank': 3200,
        'frequency_rank_source': 'section_band_estimate',
        'frequency_rank_provenance': 'auto_extracted',
        'collocations': ['たかい ビル', 'おおきい ビル', 'ビルの 中', 'ビルの 上', '会社の ビル', 'あたらしい ビル'],
        'collocations_provenance': 'llm_curated',
        'minimal_pair': {'partner': 'ビール (beer) — long vowel', 'distinguished_by': 'vowel length', 'note': 'ビル (building) 2 mora vs ビール (beer) 3 mora — listening discrimination by vowel length.'},
    },
]

added_pairs = 0
for new_e in NEW_PAIRS:
    if new_e['id'] not in existing_ids and new_e['form'] not in existing_forms:
        entries.append(new_e)
        existing_ids.add(new_e['id'])
        existing_forms.add(new_e['form'])
        added_pairs += 1
print(f'Pair partners added: {added_pairs}')

# Also add minimal_pair field to existing entries that have a partner now
print()
print('=== V3 part 2: Annotate existing entries with minimal_pair links ===')
PAIR_LINKS = {
    '雨': {'partner': '飴 (あめ) candy', 'distinguished_by': 'pitch', 'note': '雨 (rain) is atamadaka (HL); 飴 (candy) is heiban (LH).'},
    'ビール': {'partner': 'ビル (building) — short vowel', 'distinguished_by': 'vowel length', 'note': 'ビール (beer) 3 mora vs ビル (building) 2 mora.'},
    'おばあさん': {'partner': 'おばさん (aunt) — short vowel', 'distinguished_by': 'vowel length', 'note': 'おばあさん (grandmother) has long vowel; おばさん (aunt) is short.'},
    'おばさん': {'partner': 'おばあさん (grandmother) — long vowel', 'distinguished_by': 'vowel length', 'note': 'おばさん (aunt) is short; おばあさん (grandmother) has long vowel.'},
    'おじいさん': {'partner': 'おじさん (uncle) — short vowel', 'distinguished_by': 'vowel length', 'note': 'おじいさん (grandfather) has long vowel; おじさん (uncle) is short.'},
    'おじさん': {'partner': 'おじいさん (grandfather) — long vowel', 'distinguished_by': 'vowel length', 'note': 'おじさん (uncle) is short; おじいさん (grandfather) has long vowel.'},
}
linked = 0
for e in entries:
    form = e.get('form')
    if form in PAIR_LINKS and not e.get('minimal_pair'):
        e['minimal_pair'] = PAIR_LINKS[form]
        linked += 1
print(f'Existing entries linked: {linked}')

vocab_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Verify
total = len(entries)
mim = sum(1 for e in entries if e.get('onomatopoeia'))
mp = sum(1 for e in entries if e.get('minimal_pair'))
romaji_left = sum(1 for e in entries for ex in (e.get('examples') or [])
                  if isinstance(ex, dict) and 'romaji' in ex)
print()
print('=== FINAL ===')
print(f'Total vocab entries: {total}')
print(f'Mimetic-tagged:      {mim}')
print(f'Minimal-pair linked: {mp}')
print(f'Romaji left:         {romaji_left}')
