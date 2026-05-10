"""Dokkai Batch B (2026-05-10):
- D4: spacing_mode taxonomic tag on all 54 passages
- D5: cultural_callout — auto-tag canonical-12 cultural topics
- D2: backfill remaining grammar_footnotes
"""
from __future__ import annotations
import io, json, sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

reading_path = ROOT / 'data' / 'reading.json'
data = json.loads(reading_path.read_text(encoding='utf-8'))
passages = data['passages']

# === D4: spacing_mode classification ===
print('=== D4: spacing_mode classification ===')

def classify_spacing(ja: str) -> str:
    if not ja:
        return 'standard'
    n_chars = len(ja)
    n_spaces = ja.count(' ') + ja.count('　')
    if n_chars == 0:
        return 'standard'
    ratio = n_spaces / n_chars
    # Empirical thresholds for N5 reading texts
    if ratio >= 0.08:
        return 'wakachi_full'
    elif ratio >= 0.03:
        return 'wakachi_partial'
    else:
        return 'standard'

sm_counts = {'wakachi_full': 0, 'wakachi_partial': 0, 'standard': 0}
for p in passages:
    if p.get('spacing_mode'):
        continue
    mode = classify_spacing(p.get('ja', ''))
    p['spacing_mode'] = mode
    p['spacing_mode_provenance'] = 'auto_derived'
    sm_counts[mode] += 1

print(f'  spacing_mode distribution: {sm_counts}')


# === D5: cultural_callout — canonical 12 ===
print()
print('=== D5: cultural_callout (canonical-12) ===')
# Each callout has a list of trigger keywords (kanji or kana). Multi-tag allowed.
CULTURAL_CALLOUTS = {
    'self_introduction': {
        'label_en': 'Self-introduction (jikoshoukai)',
        'triggers': ['自己紹介', 'はじめまして', 'よろしく', 'どうぞ よろしく', 'です。', 'と もうします', 'と申します'],
        'note': 'Japanese self-intros follow a fixed sequence: greeting → name → affiliation → "yoroshiku".',
    },
    'family': {
        'label_en': 'Family (kazoku)',
        'triggers': ['家族', 'かぞく', '父', 'ちち', '母', 'はは', '兄', '姉', '弟', '妹', 'お父さん', 'お母さん', 'ご家族'],
        'note': 'Japanese distinguishes humble (own family: 父/母) vs honorific (others: お父さん/お母さん).',
    },
    'meals': {
        'label_en': 'Meals & itadakimasu',
        'triggers': ['食事', 'ごはん', 'いただきます', 'ごちそうさま', '朝ご飯', '昼ご飯', '晩ご飯', 'あさごはん', 'ひるごはん'],
        'note': 'Itadakimasu/gochisousama bracket meals; opt-out can offend hosts.',
    },
    'school': {
        'label_en': 'School / university',
        'triggers': ['学校', 'がっこう', '大学', 'だいがく', '学生', 'がくせい', '先生', 'せんせい', '宿題', 'しゅくだい', 'クラス', '勉強', 'べんきょう'],
        'note': 'School year starts in April; senpai (せんぱい) / kouhai (こうはい) hierarchy is rigid.',
    },
    'work': {
        'label_en': 'Work & company life',
        'triggers': ['仕事', 'しごと', '会社', 'かいしゃ', '会社員', '働く', 'はたらく', 'お疲れ様', '上司', 'じょうし', 'サラリーマン'],
        'note': 'Otsukaresama is a workplace closing; honne (ほんね) and tatemae (たてまえ) — true vs public face — shape office speech.',
    },
    'hobbies': {
        'label_en': 'Hobbies & leisure',
        'triggers': ['趣味', 'しゅみ', '映画', 'えいが', 'スポーツ', 'おんがく', '音楽', '読書', 'カラオケ', 'まんが', 'アニメ'],
        'note': 'Hobby-asking is a standard small-talk move; vague answers are polite.',
    },
    'seasons': {
        'label_en': 'Seasons (kisetsu)',
        'triggers': ['春', 'はる', '夏', 'なつ', '秋', 'あき', '冬', 'ふゆ', '季節', 'きせつ', '桜', 'さくら', '紅葉'],
        'note': 'Four-season awareness saturates Japanese culture; seasonal greetings (kigo, きご) expected in correspondence.',
    },
    'holidays': {
        'label_en': 'Holidays & festivals',
        'triggers': ['お正月', 'しょうがつ', 'お盆', 'ぼん', '七夕', 'たなばた', '花火', 'はなび', '祭り', 'まつり', 'クリスマス', '誕生日', 'お年玉'],
        'note': 'Major holidays: New Year (Jan 1-3), Golden Week (early May), Obon (mid-Aug).',
    },
    'food_culture': {
        'label_en': 'Food culture (washoku)',
        'triggers': ['寿司', 'すし', 'ラーメン', 'うどん', 'そば', 'お茶', 'おちゃ', 'みそ', '味噌', 'しょうゆ', 'たまご', 'ごはん'],
        'note': 'Washoku is UNESCO-listed; specific food terms carry strong cultural connotation.',
    },
    'manners': {
        'label_en': 'Manners (ojigi, kutsu wo nugu)',
        'triggers': ['お辞儀', 'おじぎ', '靴', 'くつ', '脱ぐ', 'ぬぐ', '手', 'て', '名刺', 'めいし', 'お礼', 'おれい', 'すみません', '失礼'],
        'note': 'Bowing (おじぎ) depth signals respect level; shoes (くつ) off indoors; meishi (めいし, business card) exchange has strict choreography.',
    },
    'city_transport': {
        'label_en': 'City & transport',
        'triggers': ['駅', 'えき', '電車', 'でんしゃ', 'バス', 'タクシー', '地下鉄', 'ちかてつ', '新幹線', '東京', 'とうきょう', '大阪', '京都'],
        'note': 'Punctual public transport is a cultural touchstone; Suica/PASMO ubiquity.',
    },
    'nature': {
        'label_en': 'Nature & landscape',
        'triggers': ['山', 'やま', '川', 'かわ', '海', 'うみ', '森', '空', 'そら', '雨', 'あめ', '雪', 'ゆき', '富士山'],
        'note': 'Nature reverence pervades daily speech (季語, weather small-talk).',
    },
}

callouts_added = 0
for p in passages:
    if p.get('cultural_callout'):
        continue
    ja = (p.get('ja') or '') + ' ' + (p.get('topic') or '') + ' ' + (p.get('title_ja') or '')
    matched = []
    for tag, info in CULTURAL_CALLOUTS.items():
        for trig in info['triggers']:
            if trig in ja:
                matched.append({
                    'tag': tag,
                    'label_en': info['label_en'],
                    'matched_trigger': trig,
                    'note': info['note'],
                })
                break  # one match per tag is enough
    if matched:
        p['cultural_callout'] = matched
        p['cultural_callout_provenance'] = 'auto_derived'
        callouts_added += 1

print(f'  Passages tagged: {callouts_added}')


# === D2: backfill remaining grammar_footnotes (lightweight) ===
print()
print('=== D2: grammar_footnotes backfill (remaining) ===')
G = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))['patterns']
PATTERN_SIGNATURES = []
for pat in G:
    s = pat.get('pattern','').replace('〜','').replace('～','').strip()
    if s and len(s) >= 2:
        PATTERN_SIGNATURES.append((s, pat['id'], pat.get('meaning_en','')))

footnotes_added = 0
for p in passages:
    if p.get('grammar_footnotes'):
        continue
    ja = p.get('ja','')
    if not ja:
        continue
    sentences = [s for s in ja.replace('\n','。').split('。') if s.strip()]
    footnotes = []
    for i, s in enumerate(sentences):
        s_pats = []
        for pat_s, pid, meaning in PATTERN_SIGNATURES:
            if len(pat_s) >= 2 and pat_s in s:
                s_pats.append({'pattern_id': pid, 'surface': pat_s, 'gloss': meaning[:60]})
        s_pats.sort(key=lambda x: -len(x['surface']))
        if s_pats[:3]:
            footnotes.append({
                'sentence_idx': i,
                'sentence_ja': s.strip()[:80],
                'patterns': s_pats[:3],
            })
    if footnotes:
        p['grammar_footnotes'] = footnotes
        p['grammar_footnotes_provenance'] = 'auto_derived'
        footnotes_added += 1

print(f'  Backfilled: {footnotes_added}')


# Save
reading_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Final
total = len(passages)
sm = sum(1 for p in passages if p.get('spacing_mode'))
cc = sum(1 for p in passages if p.get('cultural_callout'))
gf = sum(1 for p in passages if p.get('grammar_footnotes'))
audio = sum(1 for p in passages if p.get('audio'))
vp = sum(1 for p in passages if p.get('vocab_preview'))
print()
print('=== FINAL ===')
print(f'  spacing_mode:        {sm}/{total}')
print(f'  cultural_callout:    {cc}/{total}')
print(f'  grammar_footnotes:   {gf}/{total}')
print(f'  audio:               {audio}/{total}')
print(f'  vocab_preview:       {vp}/{total}')
