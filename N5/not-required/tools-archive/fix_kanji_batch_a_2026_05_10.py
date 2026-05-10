"""Kanji Batch A:
- K1: confusable cluster cross-links (extend the 29/106 already linked)
- K3: okurigana boundary cuts (auto-derivable from kun-yomi + dictionary form)
- K4: on/kun rule-of-thumb pedagogical note (per-kanji)
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

kanji_path = ROOT / 'data' / 'kanji.json'
data = json.loads(kanji_path.read_text(encoding='utf-8'))
entries = data.get('entries', data) if isinstance(data, dict) else data
if isinstance(entries, dict):
    entries = list(entries.values())
    if 'entries' in data:
        data['entries'] = entries

# --- K1: extended confusable clusters ---
# Canonical N5 confusable clusters (all members are N5 kanji)
print('=== K1: Confusable kanji clusters ===')
CLUSTERS = [
    ['大', '犬', '太'],            # big / dog / fat
    ['木', '本', '末'],            # tree / book / end (未 is N4)
    ['人', '入', '八'],            # person / enter / eight
    ['日', '目', '白'],            # day / eye / white
    ['千', '干', '王'],            # thousand / dry (N4) / king (N4) — but useful confusable
    ['上', '止'],                  # up / stop (止 is N4 but useful)
    ['古', '占'],                  # old / fortune (占 is N4 but useful)
    ['千', '午'],                  # thousand / noon
    ['一', '二', '三'],            # 1 / 2 / 3 (visual horizontals)
    ['四', '西'],                  # four / west (visual square)
    ['口', '日', '目', '白'],      # mouth / day / eye / white (small box family)
    ['月', '日'],                  # month / day (visual rectangles)
    ['火', '水'],                  # fire / water (often paired)
    ['金', '銀'],                  # gold/silver — but 銀 is N4
    ['男', '女', '子'],            # man / woman / child (people-family)
    ['父', '母'],                  # father / mother
    ['東', '西', '南', '北'],      # 4 cardinal directions
    ['手', '足'],                  # hand / foot
    ['見', '貝'],                  # see / shellfish (similar shape)
    ['川', '州'],                  # river / state
    ['行', '街'],                  # go / street
    ['学', '字'],                  # study / character
]

# Build glyph → existing entry map
glyph_to_entry = {}
for e in entries:
    g = e.get('glyph') or (e.get('id', '').split('.')[-1])
    if g:
        glyph_to_entry[g] = e

# For each cluster, link every glyph IN the corpus to all OTHER members in
# the corpus. Use the lookalikes / lookalike_clusters field already used.
linked = 0
for cluster in CLUSTERS:
    in_corpus = [g for g in cluster if g in glyph_to_entry]
    if len(in_corpus) < 2: continue
    for g in in_corpus:
        e = glyph_to_entry[g]
        others = [og for og in in_corpus if og != g]
        existing = e.get('lookalikes') or []
        if not isinstance(existing, list): existing = []
        new = list(set(existing) | set(others))
        if new != existing:
            e['lookalikes'] = sorted(new)
            e['lookalikes_provenance'] = 'llm_curated'
            linked += 1

print(f'  Kanji with updated lookalikes: {linked}')


# --- K3: okurigana boundary cuts ---
print()
print('=== K3: Okurigana boundary cuts ===')
# For kanji entries with verbs in `examples`, derive okurigana cuts.
# E.g., kanji 食 with example 食べる → okurigana_cuts = ['食:べる']
# This is derivable from the kun-yomi field.
cuts_added = 0
for e in entries:
    g = e.get('glyph') or (e.get('id', '').split('.')[-1])
    if not g or e.get('okurigana_cuts'):
        continue
    # Look at kun_yomi field — entries like "た‧べる" already use the marker
    kun = e.get('kun') or []
    cuts = []
    for k in kun:
        if not isinstance(k, str): continue
        # Standard convention: kun written as "stem.okurigana" e.g., "た.べる"
        # or with a dot ・ or full-width period
        for sep in ('.', '・', '‧'):
            if sep in k:
                stem, suffix = k.split(sep, 1)
                cuts.append(f'{g}:{suffix}')
                break
    if cuts:
        e['okurigana_cuts'] = sorted(set(cuts))
        e['okurigana_cuts_provenance'] = 'auto_derived'
        cuts_added += 1
print(f'  Kanji with okurigana_cuts: {cuts_added}')


# --- K4: on/kun rule-of-thumb pedagogical note ---
print()
print('=== K4: On/kun rule-of-thumb notes ===')
# Generic rule + per-kanji concrete example
# Apply to each kanji as a `reading_rule` field
RULE_TEMPLATE = "Standalone kanji typically takes the kun-yomi ({kun}). In compounds with another kanji, on-yomi is more common ({on}). Example: {example}."

EXAMPLES = {
    '日': '日 (ひ, kun, "day") — standalone. 日本 (にほん, on+on, "Japan") — compound.',
    '月': '月 (つき, kun, "moon") — standalone. 月曜日 (げつようび, on, "Monday") — compound.',
    '火': '火 (ひ, kun, "fire") — standalone. 火曜日 (かようび, on, "Tuesday") — compound.',
    '水': '水 (みず, kun, "water") — standalone. 水曜日 (すいようび, on, "Wednesday") — compound.',
    '木': '木 (き, kun, "tree") — standalone. 木曜日 (もくようび, on, "Thursday") — compound.',
    '金': '金 (かね, kun, "money") — standalone. 金曜日 (きんようび, on, "Friday") — compound.',
    '土': '土 (つち, kun, "earth") — standalone. 土曜日 (どようび, on, "Saturday") — compound.',
    '人': '人 (ひと, kun, "person") — standalone. 日本人 (にほんじん, on, "Japanese person") — compound suffix.',
    '生': '生 (い-きる/うまれる, kun) — standalone verbs. 学生 (がくせい, on, "student") — compound.',
    '本': '本 (ほん, on, "book") — standalone (irregular: uses on even alone). 日本 (にほん, on) — compound.',
    '一': 'Numbers usually take on-yomi: 一 (いち), 一月 (いちがつ, January). Kun ひと appears in 一つ (ひとつ, one thing).',
    '学': '学 (まな-ぶ, kun, "to learn") — verb. 学校 (がっこう, on, "school") — compound noun.',
    '校': '校 (こう, on) — appears in compounds: 学校, 高校 — rarely standalone.',
    '時': '時 (とき, kun, "time, occasion") — standalone. 時間 (じかん, on, "time-duration") — compound.',
    '間': '間 (あいだ, kun, "between"). 時間 (じかん, on) — compound.',
    '見': '見 (み-る, kun, "to see") — verb. 意見 (いけん, on, "opinion") — compound.',
    '聞': '聞 (き-く, kun, "to listen/ask") — verb. 新聞 (しんぶん, on, "newspaper") — compound.',
    '行': '行 (い-く, kun, "to go") — verb. 銀行 (ぎんこう, on, "bank") — compound.',
    '来': '来 (く-る, kun, "to come") — verb. 来年 (らいねん, on, "next year") — compound.',
    '食': '食 (た-べる, kun, "to eat") — verb. 食事 (しょくじ, on, "meal") — compound.',
    '飲': '飲 (の-む, kun, "to drink") — verb. 飲料 (いんりょう, on) — compound (N4+).',
    '私': '私 (わたし/わたくし, kun, "I") — standalone. 私生活 (しせいかつ, on, "private life") — compound (N4+).',
    '何': '何 (なに/なん) — both kun. なに alone (何ですか), なん before counters (何時, なんじ).',
    '父': '父 (ちち, kun, humble "my father") — standalone. お父さん (おとうさん, kun-based polite) — used about others.',
    '母': '母 (はは, kun, humble) — standalone. お母さん (おかあさん, kun-based polite) — about others.',
}

rule_added = 0
for e in entries:
    g = e.get('glyph') or (e.get('id', '').split('.')[-1])
    if not g or e.get('reading_rule'):
        continue
    on_list = e.get('on') or []
    kun_list = e.get('kun') or []
    rule = ('Generic rule: standalone kanji → typically kun-yomi; '
            'compound kanji → typically on-yomi.')
    if g in EXAMPLES:
        rule += f' For {g}: {EXAMPLES[g]}'
    elif on_list and kun_list:
        rule += f' For {g}: standalone use of kun ({kun_list[0]}); compounds use on ({on_list[0]}).'
    elif on_list and not kun_list:
        rule += f' For {g}: only on-readings ({", ".join(on_list[:2])}); appears mostly in compounds.'
    elif kun_list and not on_list:
        rule += f' For {g}: kun ({kun_list[0]}) is the dominant reading.'
    e['reading_rule'] = rule
    e['reading_rule_provenance'] = 'llm_curated'
    rule_added += 1

print(f'  Kanji with reading_rule: {rule_added}')


kanji_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Summary
look = sum(1 for e in entries if e.get('lookalikes'))
cuts = sum(1 for e in entries if e.get('okurigana_cuts'))
rules = sum(1 for e in entries if e.get('reading_rule'))
print()
print('=== FINAL ===')
print(f'  lookalikes:       {look}/106')
print(f'  okurigana_cuts:   {cuts}/106')
print(f'  reading_rule:     {rules}/106')
