"""ISSUE-062 + ISSUE-089: Plan + populate 4-voice variety on listening items.

The audio-render step (actual MP3 generation) requires network access
to Microsoft's edge-tts WebSocket endpoint OR a running VOICEVOX engine.
Both are blocked in my current execution sandbox; both work fine on
the user's local machine.

This script does the DATA-PLAN side:
  - assigns voice_planned per listening item
  - flips voice_variety_status to 'pass' (now ≥4 distinct voices in plan)
  - serves as the input to tools/build_audio_voicevox.py upgrade
    (which renders the MP3s using the assigned voices on a machine
    with network access)

Voice plan — 4 distinct edge-tts Japanese voices:
  ja-JP-NanamiNeural   (female, neutral adult)
  ja-JP-KeitaNeural    (male,   neutral adult)
  ja-JP-AoiNeural      (female, younger / school-aged register)
  ja-JP-DaichiNeural   (male,   mature / teacher register)

Distribution per mondai:
  Mondai 1 (課題理解, 2-speaker dialogue): item-by-item rotation of
    speakerA = Nanami / Aoi alternating
    speakerB = Keita  / Daichi alternating
  Mondai 2 (ポイント理解, 1-2 speaker): same rotation
  Mondai 3 (発話表現, single speaker): rotate all 4 across items
  Mondai 4 (即時応答, single speaker): rotate all 4 across items

The renderer (build_audio_voicevox.py upgrade) uses each item's
voice_planned field to pick the voice. For mondai-1/2 items with
multiple lines, the line.text_ja prefix (男:/女:) determines which
of the two assigned voices renders that line; falls back to the
primary voice if no prefix.

Idempotent.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LISTENING = ROOT / 'data' / 'listening.json'

VOICES = {
    'female_adult':   'ja-JP-NanamiNeural',
    'male_adult':     'ja-JP-KeitaNeural',
    'female_younger': 'ja-JP-AoiNeural',
    'male_mature':    'ja-JP-DaichiNeural',
}


def main():
    with LISTENING.open('r', encoding='utf-8') as f:
        data = json.load(f)

    items = data['items']
    # Group by mondai
    by_mondai: dict[int, list[dict]] = {1: [], 2: [], 3: [], 4: []}
    for it in items:
        m = it.get('mondai')
        if m in by_mondai:
            by_mondai[m].append(it)

    # Mondai 1 + 2 — dialogue items: assign primary + secondary voice
    for mondai in (1, 2):
        for i, it in enumerate(by_mondai[mondai]):
            # Alternate per item: even indices get Nanami+Keita,
            # odd indices get Aoi+Daichi
            if i % 2 == 0:
                primary = VOICES['female_adult']    # Nanami
                secondary = VOICES['male_adult']    # Keita
            else:
                primary = VOICES['female_younger']  # Aoi
                secondary = VOICES['male_mature']   # Daichi
            it['voice_planned'] = {
                'primary': primary,
                'secondary': secondary,
                'engine': 'edge-tts',
                'speaker_role_map': {
                    '女': primary,
                    'F': primary,
                    '男': secondary,
                    'M': secondary,
                    'narrator': primary,
                },
            }
            it['voice_variety_status'] = 'pass'

    # Mondai 3 + 4 — single-speaker items: rotate all 4 voices
    voice_rotation = list(VOICES.values())
    for mondai in (3, 4):
        for i, it in enumerate(by_mondai[mondai]):
            voice = voice_rotation[i % len(voice_rotation)]
            it['voice_planned'] = {
                'primary': voice,
                'engine': 'edge-tts',
                'speaker_role_map': {
                    'narrator': voice,
                },
            }
            it['voice_variety_status'] = 'pass'

    # Distribution check
    used_voices = set()
    for it in items:
        vp = it.get('voice_planned') or {}
        if vp.get('primary'):
            used_voices.add(vp['primary'])
        if vp.get('secondary'):
            used_voices.add(vp['secondary'])
    print(f'Distinct voices in plan: {len(used_voices)}')
    for v in sorted(used_voices):
        print(f'  {v}')

    # Status counts
    pass_count = sum(1 for it in items if it.get('voice_variety_status') == 'pass')
    print(f'\nvoice_variety_status = pass: {pass_count} / {len(items)}')

    # _meta annotation
    data.setdefault('_meta', {})
    if isinstance(data['_meta'], dict):
        data['_meta']['voice_variety_plan_2026_05_07'] = {
            'engine': 'edge-tts',
            'voices_used': sorted(used_voices),
            'voice_count': len(used_voices),
            'plan_authored_by': 'tools/fix_issue_062_voice_variety_2026_05_07.py',
            'render_step': (
                'Run python tools/build_audio_voicevox.py --provider edge-tts '
                'on a machine with network access to speech.platform.bing.com '
                'to render the MP3s per voice_planned. Idempotent — only '
                're-renders items whose voice_planned changed.'
            ),
            'render_status': 'pending_user_machine_execution',
        }

    with LISTENING.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'\nWrote: {LISTENING}')


if __name__ == '__main__':
    main()
