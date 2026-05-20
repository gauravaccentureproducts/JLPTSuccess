"""IMP-094 pre-production: author per-item `recording_directions`
on a representative pilot batch of 8 listening items (2 per mondai
format), so a future native-recording session has worked-example
direction sheets in addition to the corpus-wide brief.

Authored by the project's resident 日本語教師 persona at round-9
close-out, 2026-05-07. Idempotent — re-runs overwrite the same 8
items' directions; other items are not touched.

Output: data/recording_directions.json (separate from listening.json
so the JA-13 N5-scope-kanji invariant doesn't reject the production-
side metadata, which references kanji like 韻律, 中立 etc. that are
out of N5 scope for *learners* but legitimate for *recording engineers*).

Direction structure follows the schema specified in
`docs/RECORDING-BRIEF.md` § 5:

  recording_directions:
    speakers:               [{role, voice (M/F), register}]
    pacing:                 string
    prosody_hints:          [{line_index, note}]
    pronunciation_callouts: [{form, reading}]
    do_not:                 [string]

Run:
  python tools/add_recording_directions_2026_05_07.py
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
LISTENING = ROOT / 'data' / 'listening.json'
OUT = ROOT / 'data' / 'recording_directions.json'

# ---------------------------------------------------------------------------
# Direction sheets, one per pilot item.
# ---------------------------------------------------------------------------
# Authoring conventions (per the JA-teacher persona):
#   - Each prosody hint is keyed by `line_index` (0-based, matching the
#     `lines[]` array on the item).
#   - `do_not` callouts target the specific distractor / wrong answer
#     to avoid telegraphing it via prosody.
#   - `pronunciation_callouts` only flag forms where the corpus has a
#     specific JLPT-N5 reading ruling (per RECORDING-BRIEF.md § 3).
# ---------------------------------------------------------------------------

DIRECTIONS = {
    # =====================================================================
    # MONDAI 1 — task understanding (dialogue, two voices)
    # =====================================================================
    'n5.listen.001': {
        'speakers': [
            {'role': 'narrator', 'voice': 'F', 'register': 'announcer-neutral'},
            {'role': '男',        'voice': 'M', 'register': 'polite-adult'},
            {'role': '女',        'voice': 'F', 'register': 'polite-adult'},
        ],
        'pacing': '180-220 morae/min; ~250ms inter-turn pause',
        'prosody_hints': [
            {'line_index': 0, 'note': 'Narrator scene-set + question. Read flatter than dialogue lines. Mild prosodic peak on どこ in the closing question.'},
            {'line_index': 1, 'note': 'Casual-friendly invitation. The 〜ませんか tag is rising, but only mildly — not gushing.'},
            {'line_index': 2, 'note': 'Receptive いいですね then a clean 何時に — keep it neutral, no excitement.'},
            {'line_index': 3, 'note': '三時に slows slightly to give the listener a chance to register the time. NOT a wh-word, no peak.'},
            {'line_index': 4, 'note': 'This is the resolution turn. えきの前は人がおおい sets up the rejection; カフェの前で会いましょう lands the answer. Both halves equally clear, NO emphasis on カフェの前 — that would telegraph it.'},
            {'line_index': 5, 'note': 'はい、わかりました — closing acknowledgement. Brisk, not slow.'},
        ],
        'pronunciation_callouts': [
            {'form': '明日',  'reading': 'あした'},
            {'form': '二人',  'reading': 'ふたり'},
            {'form': '三時',  'reading': 'さんじ'},
            {'form': '何時',  'reading': 'なんじ'},
        ],
        'do_not': [
            'Do not put extra emphasis on カフェの前 — that is the correct answer; emphasis is the listener\'s tell. Both location options must sound equally salient.',
            'Do not pause inside えきの前は人がおおいですね — the comma is a written aid, not a vocalised pause longer than ~150ms.',
        ],
    },
    'n5.listen.004': {
        'speakers': [
            {'role': 'narrator', 'voice': 'F', 'register': 'announcer-neutral'},
            {'role': '店員',      'voice': 'F', 'register': 'service-polite'},
            {'role': '男',        'voice': 'M', 'register': 'polite-adult'},
        ],
        'pacing': '180-220 morae/min; service-counter exchange so slightly brisker turn-taking (~200ms).',
        'prosody_hints': [
            {'line_index': 0, 'note': 'Narrator. Mild peak on 何 in the closing question.'},
            {'line_index': 1, 'note': 'いらっしゃいませ — standard service-counter greeting. Bright but professional, NOT overly cheerful (no fake-anime lilt).'},
            {'line_index': 2, 'note': 'すみません as turn-opener; コーヒーをください is the nominal request. Both halves clean.'},
            {'line_index': 3, 'note': 'あついコーヒーですか — confirmation question. Rising tag, polite but slightly probing.'},
            {'line_index': 4, 'note': 'いいえ rejects あつい; つめたいコーヒーで is the actual answer. NO extra emphasis on つめたい — both temperatures must sound equally weighted.'},
            {'line_index': 5, 'note': 'Final confirmation. Calm.'},
        ],
        'pronunciation_callouts': [
            {'form': 'コーヒー', 'reading': 'コ↓ーヒー (4 morae, atamadaka)'},
            {'form': '飲みます', 'reading': 'のみます'},
        ],
        'do_not': [
            'Do not over-emphasise つめたい — it is the correct answer; emphasis would telegraph it.',
            'Do not anglicise コーヒー. It is 4 morae in Japanese (こ・ー・ひ・ー), not 2 syllables in English.',
            'Do not skip the long ー on コーヒー — that is the most common synthetic-engine error this brief is correcting.',
        ],
    },

    # =====================================================================
    # MONDAI 2 — point comprehension (dialogue, two voices, why/how/which)
    # =====================================================================
    'n5.listen.005': {
        'speakers': [
            {'role': 'narrator', 'voice': 'F', 'register': 'announcer-neutral'},
            {'role': '先生',      'voice': 'M', 'register': 'authoritative-polite'},
            {'role': '学生',      'voice': 'F', 'register': 'apologetic-deferential'},
        ],
        'pacing': '180-210 morae/min; ~250ms turn-pause. The student\'s lines should sound contrite without being theatrical.',
        'prosody_hints': [
            {'line_index': 0, 'note': 'Narrator. Mild peak on どうして in the closing question.'},
            {'line_index': 1, 'note': '先生 question, mildly stern but not angry. どうして carries the wh-word peak.'},
            {'line_index': 2, 'note': 'Student\'s すみません apologetic, then あさ、でんしゃがおくれました — flat, factual. NO emotional colour.'},
            {'line_index': 3, 'note': '先生 receives the explanation neutrally. そうですか is acknowledgement, not approval.'},
            {'line_index': 4, 'note': 'はい、もうだいじょうぶです — student\'s reassurance. Calm.'},
        ],
        'pronunciation_callouts': [
            {'form': '今日',     'reading': 'きょう'},
            {'form': '学生',     'reading': 'がくせい'},
            {'form': '先生',     'reading': 'せんせい'},
            {'form': 'でんしゃ', 'reading': 'でんしゃ (heiban)'},
        ],
        'do_not': [
            'Do not under-emphasise でんしゃがおくれました — it is the correct reason; the listener should hear it just as clearly as the distractors. But also do NOT over-emphasise it.',
            'Do not soften 先生 into a sympathetic tone. The pedagogical point is that the student must report the reason; the teacher\'s tone is neutral-authoritative throughout.',
        ],
    },
    'n5.listen.008': {
        'speakers': [
            {'role': 'narrator', 'voice': 'F', 'register': 'announcer-neutral'},
            {'role': '女',        'voice': 'F', 'register': 'polite-friendly'},
            {'role': '男',        'voice': 'M', 'register': 'polite-friendly'},
        ],
        'pacing': '180-210 morae/min; conversational so turn-pauses can shrink to ~200ms.',
        'prosody_hints': [
            {'line_index': 0, 'note': 'Narrator. Mild peak on 何 in the closing question.'},
            {'line_index': 1, 'note': '女: probing question with two distinct candidates (本, とけい). Both candidates equally weighted.'},
            {'line_index': 2, 'note': '男: 本もいいですが is concessive — gentle rising-falling on いいですが to mark "but". The もっとほしいものがあります sets up the reveal.'},
            {'line_index': 3, 'note': '女: clarifying question. とけい still in candidate weight.'},
            {'line_index': 4, 'note': '男: いいえ rejects とけい. 新しいカメラがほしいです lands the answer. NO extra emphasis on カメラ — equal-weight rule.'},
            {'line_index': 5, 'note': 'そうですか — closing acknowledgement. Calm.'},
        ],
        'pronunciation_callouts': [
            {'form': 'カメラ', 'reading': 'か↓めら (3 morae, atamadaka)'},
            {'form': '新しい', 'reading': 'あたらしい'},
            {'form': '本',     'reading': 'ほん'},
            {'form': 'とけい', 'reading': 'とけい (heiban)'},
        ],
        'do_not': [
            'Do not over-emphasise カメラ. The distractors 本 and とけい must sound equally salient.',
            'Do not anglicise カメラ — Japanese atamadaka, drop on め.',
        ],
    },

    # =====================================================================
    # MONDAI 3 — utterance expression (scene + 3 candidate utterances)
    # =====================================================================
    'n5.listen.009': {
        'speakers': [
            {'role': 'narrator',  'voice': 'F', 'register': 'announcer-neutral'},
            {'role': 'candidate1', 'voice': 'F', 'register': 'polite-stranger-address'},
            {'role': 'candidate2', 'voice': 'F', 'register': 'polite-stranger-address'},
            {'role': 'candidate3', 'voice': 'F', 'register': 'polite-stranger-address'},
        ],
        'pacing': '~180 morae/min — slow side of the band because each utterance is short.',
        'prosody_hints': [
            {'line_index': 0, 'note': 'Narrator scene-set. Flat, slightly slower. The parenthetical aside should NOT sound like dialogue — it is stage direction.'},
            {'line_index': -1, 'note': 'All three candidate utterances should be read by the SAME voice with EQUAL prosodic weight. The listener decides on words, not delivery.'},
        ],
        'pronunciation_callouts': [
            {'form': '何時', 'reading': 'なんじ'},
            {'form': 'すみません', 'reading': 'すみません (heiban; do not over-emphasise the apologetic register)'},
        ],
        'do_not': [
            'Do not give the correct candidate (すみません、いま何時ですか) any extra polish. The wrong candidates must be read just as fluently.',
            'Do not vary speaker between candidates — that would add a non-content cue.',
            'Pre-roll the narrator scene-set with ~500ms of silence; this gives the listener the conventional "now I should think" moment.',
        ],
    },
    'n5.listen.028': {
        'speakers': [
            {'role': 'narrator',   'voice': 'F', 'register': 'announcer-neutral'},
            {'role': 'candidate1', 'voice': 'F', 'register': 'polite-friend-address'},
            {'role': 'candidate2', 'voice': 'F', 'register': 'polite-friend-address'},
            {'role': 'candidate3', 'voice': 'F', 'register': 'polite-friend-address'},
            {'role': 'candidate4', 'voice': 'F', 'register': 'polite-friend-address'},
        ],
        'pacing': '~180 morae/min',
        'prosody_hints': [
            {'line_index': 0, 'note': 'Narrator scene-set: 友だちのいえへ入ります。 Flat, slightly slower. NOT a question.'},
            {'line_index': -1, 'note': 'All four candidate utterances read by the same voice, equal prosodic weight. しつれいします (correct) is the most formal-sounding by content; do not let prosody amplify that. Read it as flatly as いただきます.'},
        ],
        'pronunciation_callouts': [
            {'form': '友だち', 'reading': 'ともだち'},
            {'form': '入ります', 'reading': 'はいります'},
            {'form': 'しつれいします', 'reading': 'しつれいします'},
            {'form': 'いただきます', 'reading': 'いただきます'},
            {'form': 'ただいま',     'reading': 'ただいま'},
        ],
        'do_not': [
            'Do not make しつれいします sound more "polite" than the others — content already encodes that. The listener has to recognise the social context, not detect emphasis.',
            'Do not laugh-track or warm-tone any of the candidates — Mondai 3 is decoy-heavy and tone-clean.',
        ],
    },

    # =====================================================================
    # MONDAI 4 — immediate response (stimulus + 3 short response candidates)
    # =====================================================================
    'n5.listen.041': {
        'speakers': [
            {'role': 'stimulus',   'voice': 'F', 'register': 'polite-leaving-workplace'},
            {'role': 'candidate1', 'voice': 'M', 'register': 'polite-colleague'},
            {'role': 'candidate2', 'voice': 'M', 'register': 'polite-colleague'},
            {'role': 'candidate3', 'voice': 'M', 'register': 'polite-colleague'},
        ],
        'pacing': '~200 morae/min — these items are short; do not rush, but also do not pad.',
        'prosody_hints': [
            {'line_index': 0, 'note': 'Stimulus: おさきにしつれいします — leaving the office. Slight politeness register but not overly formal. Crisp; ~2-3 seconds delivered.'},
            {'line_index': -1, 'note': 'Three candidates read by the SAME male voice, equal weight. おつかれさまでした (correct) is the formulaic workplace pair; do not let prosody amplify it.'},
        ],
        'pronunciation_callouts': [
            {'form': 'おさきに', 'reading': 'おさきに'},
            {'form': 'しつれいします', 'reading': 'しつれいします'},
            {'form': 'おつかれさまでした', 'reading': 'おつかれさまでした'},
            {'form': 'はじめまして', 'reading': 'はじめまして'},
            {'form': 'ごちそうさまでした', 'reading': 'ごちそうさまでした'},
        ],
        'do_not': [
            'Do not warm おつかれさまでした relative to はじめまして — equal weight rule.',
            'Pre-roll on the stimulus is ~300ms (not the 500ms of mondai 3); these items are tight.',
            'Inter-candidate pause: ~400-500ms — long enough that the listener registers the pivot from one candidate to the next.',
        ],
    },
    'n5.listen.045': {
        'speakers': [
            {'role': 'stimulus',   'voice': 'M', 'register': 'morning-greeting'},
            {'role': 'candidate1', 'voice': 'F', 'register': 'morning-greeting-response'},
            {'role': 'candidate2', 'voice': 'F', 'register': 'evening-greeting-response'},
            {'role': 'candidate3', 'voice': 'F', 'register': 'farewell'},
        ],
        'pacing': '~200 morae/min',
        'prosody_hints': [
            {'line_index': 0, 'note': 'Stimulus: おはようございます — morning greeting. Bright but not overly cheerful. The brightness comes from the time-of-day register, not from the actor.'},
            {'line_index': -1, 'note': 'Three candidate responses by the SAME female voice. Critical: おはようございます (correct response) must NOT sound brighter than the wrong おやすみなさい — both are time-of-day greetings; the listener has to map the time, not detect tone.'},
        ],
        'pronunciation_callouts': [
            {'form': 'おはようございます', 'reading': 'おはようございます'},
            {'form': 'おやすみなさい',     'reading': 'おやすみなさい'},
            {'form': 'さようなら',         'reading': 'さようなら'},
        ],
        'do_not': [
            'Do not give おはようございます candidate any extra brightness vs おやすみなさい. Same time-of-day-greeting register means same prosodic profile.',
            'さようなら is the universal farewell — keep it neutral, no sad lilt.',
        ],
    },
}


def main() -> int:
    # Confirm every target ID exists in listening.json — guard against
    # ID drift in future content edits.
    listening = json.loads(LISTENING.read_text(encoding='utf-8'))
    listening_ids = {it['id'] for it in listening['items']}
    missing = set(DIRECTIONS) - listening_ids
    if missing:
        print(f'ERROR: target IDs not found in listening.json: {missing}', file=sys.stderr)
        return 2

    # If a previous version of this script wrote `recording_directions`
    # *into* listening.json (which trips JA-13), strip them out so the
    # invariant passes. This is the migration step from the in-line
    # schema to the separate-file schema.
    cleaned = 0
    for it in listening['items']:
        if 'recording_directions' in it:
            del it['recording_directions']
            cleaned += 1
    if cleaned:
        LISTENING.write_text(
            json.dumps(listening, ensure_ascii=False, indent=2),
            encoding='utf-8',
        )
        print(f'Cleaned {cleaned} stale recording_directions out of listening.json (JA-13 protection).')

    # Write the directions to their own file. Keys are listening item
    # IDs; values are direction blocks. The file is a flat dict for
    # easy lookup at recording time.
    payload = {
        '_meta': {
            'authored_by': "project's resident 日本語教師 persona",
            'authored_at': '2026-05-07',
            'related_brief_en': 'docs/RECORDING-BRIEF.md',
            'related_brief_ja': 'docs/RECORDING-BRIEF.ja.md',
            'pilot_count': len(DIRECTIONS),
            'note': 'Production-side metadata for IMP-094 future native-recording session. Not learner-facing — kept out of listening.json so JA-13 (N5-scope-kanji invariant) does not reject the technical Japanese vocabulary used in directions.',
        },
        'directions': DIRECTIONS,
    }
    OUT.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding='utf-8',
    )
    print(f'Wrote {len(DIRECTIONS)} pilot direction sheets to {OUT.relative_to(ROOT)}:')
    for tid in sorted(DIRECTIONS):
        print(f'  - {tid}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
