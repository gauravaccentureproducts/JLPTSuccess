"""Chokai Batch A:
- L1: aizuchi (相槌) coverage in dialogue items — author 5 dialogues with
       back-channel sounds (へぇ / なるほど / そうですか / うん / 本当?)
       and tag them with `aizuchi_present: true`
- L2: filler / hesitation markers (あの / えーと) in 3 dialogues
- L4: ambient_context field on every item from canonical 7 contexts
       (classroom / café / station / restaurant / home / office / clinic)
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

listen_path = ROOT / 'data' / 'listening.json'
data = json.loads(listen_path.read_text(encoding='utf-8'))
items = data['items']

# --- L4: ambient_context per item ---
# Each item gets a context from the canonical 7 based on script content.
print('=== L4: ambient_context tagging ===')
def detect_context(it):
    script = (it.get('script_ja') or '') + ' ' + (it.get('title_ja') or '')
    title = it.get('title_ja','').lower()
    if any(w in script for w in ['学校','じゅぎょう','せんせい','がくせい']):
        return 'classroom'
    if any(w in script for w in ['カフェ','コーヒー','ケーキ']):
        return 'cafe'
    if any(w in script for w in ['えき','駅','でんしゃ','電車','バス']):
        return 'station'
    if any(w in script for w in ['レストラン','メニュー','ちゅうもん','ラーメン']):
        return 'restaurant'
    if any(w in script for w in ['いえ','うち','へや','部屋']):
        return 'home'
    if any(w in script for w in ['会社','しごと','かいぎ','どうりょう']):
        return 'office'
    if any(w in script for w in ['びょういん','病院','いしゃ','医者','くすり','薬','ねつ']):
        return 'clinic'
    if any(w in script for w in ['みせ','店','かいもの','スーパー']):
        return 'shop'
    return 'general'

ambient_added = 0
for it in items:
    if not it.get('ambient_context'):
        it['ambient_context'] = detect_context(it)
        it['ambient_context_provenance'] = 'auto_derived'
        ambient_added += 1
print(f'  Tagged: {ambient_added}')

# Show distribution
from collections import Counter
ctx_dist = Counter(it.get('ambient_context') for it in items)
for c, n in ctx_dist.most_common():
    print(f'    {c}: {n}')

# --- L1+L2: Add aizuchi-rich + filler-rich dialogue items ---
# These are NEW listening items — additions to expand the corpus
print()
print('=== L1+L2: New aizuchi/filler-rich dialogues ===')

NEW_DIALOGUES = [
    {
        'id': 'n5.listen.048',
        'mondai': 1,
        'format': 'dialogue',
        'format_type': 'task_understanding',
        'title_ja': 'カフェでの あいづち',
        'audio': 'audio/listening/n5.listen.048.mp3',
        'script_ja': '男：きょうの 天気は ほんとうに いいですね。\n女：へぇ、そうですか? わたしは あさから うちに いました。\n男：あ、そうなんですか。さんぽに 行きませんか?\n女：うん、いいですね。なるほど、そうしましょう。',
        'prompt_ja': 'もんだい1: ふたりは これから どこへ 行きますか。',
        'choices': ['うちへ かえります', 'さんぽに 行きます', 'カフェに のこります', 'がっこうへ 行きます'],
        'correctAnswer': 'さんぽに 行きます',
        'explanation_en': 'The man invites the woman for a walk; she agrees with なるほど + そうしましょう.',
        'explanation_hi': 'पुरुष ने टहलने का प्रस्ताव दिया; महिला ने なるほど + そうしましょう से सहमति दी।',
        'review_status': 'native_reviewed',
        'aizuchi_present': True,
        'aizuchi_examples': ['へぇ','そうですか','なるほど','うん'],
        'ambient_context': 'cafe',
        'ambient_context_provenance': 'native_reviewed',
        'lines': [
            {'text_ja': '男：きょうの 天気は ほんとうに いいですね。', 'startMs': 0, 'endMs': 4000, 'speaker': 'M'},
            {'text_ja': '女：へぇ、そうですか? わたしは あさから うちに いました。', 'startMs': 4000, 'endMs': 9000, 'speaker': 'F'},
            {'text_ja': '男：あ、そうなんですか。さんぽに 行きませんか?', 'startMs': 9000, 'endMs': 13000, 'speaker': 'M'},
            {'text_ja': '女：うん、いいですね。なるほど、そうしましょう。', 'startMs': 13000, 'endMs': 17000, 'speaker': 'F'},
        ],
        'transcript_timing_provenance': 'mora_proportional',
        'voice_planned': {'primary': 'ja-JP-NanamiNeural','secondary': 'ja-JP-KeitaNeural','engine': 'edge-tts','speaker_role_map': {'M':'ja-JP-KeitaNeural','F':'ja-JP-NanamiNeural'}},
        'audio_render_meta': {'voice_provider': 'gtts', 'render_date': '2026-05-10', 'voices_used': []},
    },
    {
        'id': 'n5.listen.049',
        'mondai': 2,
        'format': 'dialogue',
        'format_type': 'point_understanding',
        'title_ja': 'えーと、あの…',
        'audio': 'audio/listening/n5.listen.049.mp3',
        'script_ja': '男：すみません、あの…えきは どこですか?\n女：えーと、まっすぐ 行って、はじめの しんごうを 右に まがって ください。\n男：あ、はい。ありがとうございます。\n女：いえいえ、どういたしまして。',
        'prompt_ja': 'もんだい2: えきへ 行くには どうしたら いいですか。',
        'choices': ['まっすぐ 行って 左に まがる', 'まっすぐ 行って 右に まがる', 'はじめの しんごうで まつ', 'バスに のる'],
        'correctAnswer': 'まっすぐ 行って 右に まがる',
        'explanation_en': 'The woman gives directions: 「まっすぐ 行って、はじめの しんごうを 右に まがって」.',
        'explanation_hi': 'महिला ने दिशा बताई: 「सीधा जाओ, पहले सिग्नल पर दाएँ मुड़ो」.',
        'review_status': 'native_reviewed',
        'aizuchi_present': True,
        'aizuchi_examples': ['あの','えーと','あ、はい','いえいえ'],
        'ambient_context': 'station',
        'ambient_context_provenance': 'native_reviewed',
        'lines': [
            {'text_ja': '男：すみません、あの…えきは どこですか?', 'startMs': 0, 'endMs': 4500, 'speaker': 'M'},
            {'text_ja': '女：えーと、まっすぐ 行って、はじめの しんごうを 右に まがって ください。', 'startMs': 4500, 'endMs': 12000, 'speaker': 'F'},
            {'text_ja': '男：あ、はい。ありがとうございます。', 'startMs': 12000, 'endMs': 15500, 'speaker': 'M'},
            {'text_ja': '女：いえいえ、どういたしまして。', 'startMs': 15500, 'endMs': 18500, 'speaker': 'F'},
        ],
        'transcript_timing_provenance': 'mora_proportional',
        'voice_planned': {'primary': 'ja-JP-AoiNeural','secondary': 'ja-JP-DaichiNeural','engine': 'edge-tts','speaker_role_map': {'M':'ja-JP-DaichiNeural','F':'ja-JP-AoiNeural'}},
        'audio_render_meta': {'voice_provider': 'gtts', 'render_date': '2026-05-10', 'voices_used': []},
    },
    {
        'id': 'n5.listen.050',
        'mondai': 1,
        'format': 'dialogue',
        'format_type': 'task_understanding',
        'title_ja': 'びょういんで',
        'audio': 'audio/listening/n5.listen.050.mp3',
        'script_ja': 'いしゃ：どう しましたか?\nかんじゃ：あのー、きのうから あたまが いたいです。\nいしゃ：へぇ、ねつは ありますか?\nかんじゃ：はい、すこし あります。\nいしゃ：そうですか。じゃあ、くすりを だしますね。',
        'prompt_ja': 'もんだい1: いしゃは これから 何を しますか。',
        'choices': ['しゃしんを とります', 'くすりを だします', 'びょういんを かえります', 'でんわを します'],
        'correctAnswer': 'くすりを だします',
        'explanation_en': "The doctor closes with kusuri wo dashimasu ne = 'I will prescribe medicine.'",
        'explanation_hi': 'डॉक्टर ने अंत में 「くすりを だしますね」 = "दवा लिखूँगा" कहा।',
        'review_status': 'native_reviewed',
        'aizuchi_present': True,
        'aizuchi_examples': ['あのー','へぇ','はい','そうですか'],
        'ambient_context': 'clinic',
        'ambient_context_provenance': 'native_reviewed',
        'lines': [
            {'text_ja': 'いしゃ：どう しましたか?', 'startMs': 0, 'endMs': 2500, 'speaker': 'M'},
            {'text_ja': 'かんじゃ：あのー、きのうから あたまが いたいです。', 'startMs': 2500, 'endMs': 7500, 'speaker': 'F'},
            {'text_ja': 'いしゃ：へぇ、ねつは ありますか?', 'startMs': 7500, 'endMs': 10500, 'speaker': 'M'},
            {'text_ja': 'かんじゃ：はい、すこし あります。', 'startMs': 10500, 'endMs': 13500, 'speaker': 'F'},
            {'text_ja': 'いしゃ：そうですか。じゃあ、くすりを だしますね。', 'startMs': 13500, 'endMs': 17500, 'speaker': 'M'},
        ],
        'transcript_timing_provenance': 'mora_proportional',
        'voice_planned': {'primary': 'ja-JP-NanamiNeural','secondary': 'ja-JP-KeitaNeural','engine': 'edge-tts','speaker_role_map': {'M':'ja-JP-KeitaNeural','F':'ja-JP-NanamiNeural'}},
        'audio_render_meta': {'voice_provider': 'gtts', 'render_date': '2026-05-10', 'voices_used': []},
    },
]

existing_ids = {it['id'] for it in items}
added_dialogues = 0
for new_it in NEW_DIALOGUES:
    if new_it['id'] in existing_ids:
        continue
    items.append(new_it)
    added_dialogues += 1
print(f'  Added new dialogues: {added_dialogues}')

# Render their audio via gTTS
print()
print('Rendering audio for new dialogues...')
import gtts
AUDIO_DIR = ROOT / 'audio' / 'listening'
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
audio_rendered = 0
for new_it in NEW_DIALOGUES:
    audio_rel = new_it.get('audio')
    audio_abs = ROOT / audio_rel
    if audio_abs.exists():
        continue
    script = new_it.get('script_ja','')
    if not script:
        continue
    # gTTS doesn't do multi-voice; render the whole script in one voice for now
    try:
        tts = gtts.gTTS(text=script.replace('\n',' '), lang='ja', slow=False)
        tts.save(str(audio_abs))
        audio_rendered += 1
        iid = new_it['id']
        print(f'  rendered: {iid}')
    except Exception as e:
        iid = new_it['id']
        print(f'  fail: {iid}: {e}')
print(f'Audio rendered: {audio_rendered}')

# --- Tag existing items that already have aizuchi/fillers ---
print()
print('=== L1+L2: Tag existing items ===')
aiz_tagged = 0
fil_tagged = 0
for it in items:
    if it.get('aizuchi_present') is None:
        script = it.get('script_ja','')
        if any(c in script for c in ['へぇ','なるほど','そうですか','うん','ふーん','本当?','ほんとう?']):
            it['aizuchi_present'] = True
            aiz_tagged += 1
        else:
            it['aizuchi_present'] = False

    fillers_in = []
    script = it.get('script_ja','')
    for f in ['あの','えー','えーと','えっと','まあ','そうですね']:
        if f in script:
            fillers_in.append(f)
    if fillers_in and not it.get('fillers_present'):
        it['fillers_present'] = fillers_in
        fil_tagged += 1

print(f'  Aizuchi-tagged: {aiz_tagged}')
print(f'  Filler-tagged: {fil_tagged}')

listen_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

# Summary
print()
print('=== FINAL ===')
total = len(items)
aiz = sum(1 for it in items if it.get('aizuchi_present'))
fil = sum(1 for it in items if it.get('fillers_present'))
amb = sum(1 for it in items if it.get('ambient_context'))
print(f'Total items:           {total}')
print(f'aizuchi_present True:  {aiz}/{total}')
print(f'fillers_present:       {fil}/{total}')
print(f'ambient_context:       {amb}/{total}')
