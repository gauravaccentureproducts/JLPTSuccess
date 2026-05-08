"""ISSUE-062 / ISSUE-089 / ISSUE-090 (round-9 deferred → planned 2026-05-06):
voice variety plan for the 47 listening items.

Audit deferred this 3 times (round-3, round-7, round-8) because the
voice-variety upgrade was framed as needing a budget decision (Q42 —
ElevenLabs subscription, native recording, or VOICEVOX local install).
But option (c) — VOICEVOX local install — is a free 4-6hr task that
unblocks all 47 items without external cost.

This script does NOT install VOICEVOX (the install must be done on
the maintainer's machine). It does:

  1. Populate `voice_planned` on each listening item — the target
     voicevox character ID for that item, chosen for per-item
     dialogue diversity (2 voices per mondai-1/-2 dialogue item; 1
     varied voice per mondai-3/-4 single-speaker item).
  2. Add `voice_variety_status` field — currently "planned" everywhere;
     once VOICEVOX render runs, it flips to "rendered".
  3. Documents the canonical voice mapping in `_meta.voice_variety_plan`.
  4. Provides the render-command template (in a comment) for the
     maintainer to run once VOICEVOX is installed.

Voice diversity target per JLPT N5 chokai authenticity:
  - ≥4 distinct voices across the 47-item corpus
  - Per dialogue item, 2 distinct voices (男 / 女)
  - Cross-corpus: mix of 4 male + 4 female voicevox characters

VOICEVOX free voices (catalog as of 2026-05):
  Female:  2 (Shikoku Metan ノーマル) — already used
           3 (Zundamon ノーマル) — different, lower
           8 (Hau-tsumugi ノーマル) — softer, younger
           14 (Mei Hima ノーマル) — adult
  Male:    11 (Shirakami Kotaro ふつう) — adult male
           12 (Aoyama Ryusei ノーマル) — professional
           53 (Kenshin タカヒロ ノーマル) — older
           20 (Mochiko-san ノーマル) — neutral

Mapping convention:
  For dialogue items (mondai-1, mondai-2):
    'male' speaker (男, 先生男, 父, etc.) → male voice (alternates 11/12/53)
    'female' speaker (女, お母さん, etc.) → female voice (alternates 2/3/8/14)
    'staff' speaker (店員, 先生, etc.) → varies by item

  For single-speaker items (mondai-3, mondai-4):
    Rotates across voices for cross-item variety.

Idempotent: re-runs overwrite voice_planned + voice_variety_status.

To execute the actual re-render:
    pip install voicevox_core==<latest>  # 100MB ML model download
    # Or run VOICEVOX desktop's HTTP API at localhost:50021
    python tools/render_listening_audio_voicevox.py  # NOT included here
"""
from __future__ import annotations
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

LISTENING = Path(__file__).parent.parent / 'data' / 'listening.json'

# VOICEVOX speaker_id catalog (free tier).
VOICES = {
    # speaker_id : description
    2: 'shikoku-metan-normal',     # female young, currently used
    3: 'zundamon-normal',          # female lower
    8: 'hau-tsumugi-normal',       # female young soft
    14: 'mei-hima-normal',         # female adult
    11: 'shirakami-kotaro-normal', # male adult young
    12: 'aoyama-ryusei-normal',    # male professional
    53: 'kenshin-takahiro-normal', # male older
    20: 'mochiko-san-normal',      # neutral
}

# Round-robin pool for variety. Ordered to alternate male/female.
DIVERSITY_POOL = [11, 2, 12, 3, 53, 8, 20, 14]


def assign_voice(item: dict, idx: int) -> dict:
    """Assign per-line voice planned IDs based on item content.

    For dialogue items (with multiple speakers), produce a 2-voice
    plan keyed by speaker label. For single-speaker items, pick one
    voice from the diversity pool by item index.
    """
    script = item.get('script_ja', '')
    mondai = item.get('mondai')
    lines = [l.strip() for l in script.split('\n') if l.strip()]

    # Detect speaker labels: lines starting with X： where X is 1-5 chars
    speakers = []
    for line in lines:
        if '：' in line:
            label = line.split('：', 1)[0].strip()
            if 1 <= len(label) <= 5 and label not in speakers:
                speakers.append(label)

    # Heuristic: classify each speaker as male / female / staff
    MALE_HINTS = {'男', '父', '先生男', 'かれ', 'お父さん'}
    FEMALE_HINTS = {'女', '母', '先生女', 'かのじょ', 'お母さん'}

    voice_map = {}
    male_counter = 0
    female_counter = 0
    other_counter = 0
    male_pool = [11, 12, 53]
    female_pool = [2, 3, 8, 14]
    other_pool = [20, 11, 14]

    for spk in speakers:
        if spk in MALE_HINTS or spk == '男':
            voice_map[spk] = male_pool[male_counter % len(male_pool)]
            male_counter += 1
        elif spk in FEMALE_HINTS or spk == '女':
            voice_map[spk] = female_pool[female_counter % len(female_pool)]
            female_counter += 1
        else:
            voice_map[spk] = other_pool[other_counter % len(other_pool)]
            other_counter += 1

    # If no labeled speakers (single-narration), assign one voice from pool by item idx
    if not voice_map:
        return {
            'voice_planned': {'_narration': DIVERSITY_POOL[idx % len(DIVERSITY_POOL)]},
            'voice_variety_status': 'planned',
        }

    return {
        'voice_planned': voice_map,
        'voice_variety_status': 'planned',
    }


def main() -> int:
    doc = json.loads(LISTENING.read_text(encoding='utf-8'))
    items = doc['items']

    n_planned = 0
    voices_used = set()

    for idx, it in enumerate(items):
        plan = assign_voice(it, idx)
        it['voice_planned'] = plan['voice_planned']
        it['voice_variety_status'] = plan['voice_variety_status']
        voices_used.update(plan['voice_planned'].values())
        n_planned += 1

    # _meta plan
    if '_meta' not in doc:
        doc['_meta'] = {}
    doc['_meta']['voice_variety_plan'] = {
        'note': (
            'ISSUE-062 / ISSUE-089 / ISSUE-090 round-9 plan (2026-05-06): '
            'voice variety target ≥4 distinct voices across 47 items + '
            '2 voices per dialogue item. Audit was deferred 3× for budget; '
            'this plan uses VOICEVOX free tier (8 voices, multi-character) '
            'which costs nothing — only ~4-6hr to install on the maintainer\'s '
            'machine. Once VOICEVOX runs, the per-item voice_planned IDs '
            'drive a re-render script (tools/render_listening_audio_voicevox.py — '
            'to be authored when VOICEVOX is installed).'
        ),
        'target_voices': len(voices_used),
        'target_dialogue_voices_per_item': 2,
        'voicevox_speaker_catalog': VOICES,
        'speaker_label_classification': {
            'male_hints': sorted(['男', '父', '先生男', 'かれ', 'お父さん']),
            'female_hints': sorted(['女', '母', '先生女', 'かのじょ', 'お母さん']),
            'other (staff/teacher/etc.)': 'rotates across voicevox 20/11/14',
        },
        'render_command_template': (
            "Once VOICEVOX is installed (localhost:50021), run:\n"
            "  for item in listening.items:\n"
            "    for line, speaker in zip(item.lines, item.voice_planned):\n"
            "      audio = curl -X POST localhost:50021/audio_query?speaker={voice} ...\n"
            "      audio = curl -X POST localhost:50021/synthesis?speaker={voice} ...\n"
            "      append to item.audio file"
        ),
        'speakers_planned_distribution': {},  # filled below
    }

    # Compute distribution of planned speakers
    spk_dist = {}
    for it in items:
        for label, vid in it.get('voice_planned', {}).items():
            spk_dist.setdefault(label, {}).setdefault(vid, 0)
            spk_dist[label][vid] += 1
    doc['_meta']['voice_variety_plan']['speakers_planned_distribution'] = spk_dist

    LISTENING.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    print(f'Planned voice mapping for {n_planned} items.')
    print(f'Target voices in plan: {len(voices_used)}')
    print(f'  voicevox IDs: {sorted(voices_used)}')
    print(f'\nSample plans (first 3 items):')
    for it in items[:3]:
        print(f'  {it["id"]} mondai={it.get("mondai")} -> voice_planned={it.get("voice_planned")}')

    return 0


if __name__ == '__main__':
    sys.exit(main())
