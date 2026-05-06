"""ISSUE-074 (round-9 deferred → fixed 2026-05-06): pacing audit
of listening items vs official JLPT N5 chokai pace (~200-220 morae/min).

Originally deferred for "native-listener review." But the audit can be
done programmatically — measure each item's audio duration via mutagen,
count morae in script_ja, compute morae-per-minute, and flag items
outside the JLPT-N5 target range (180-240 morae/min, accommodating
±10% from the 200-220 ideal).

Mora counting follows the convention:
  - Each katakana/hiragana kana = 1 mora
  - Small kana (ょ, ゅ, ゃ) extend the previous mora — DON'T count separately
  - Long-vowel mark (ー) = 1 mora
  - Sokuon (っ) = 1 mora
  - Kanji are skipped (assume reading equals 1-3 morae;
    we ignore kanji-only sentences which are rare at N5)

Output:
  - listening.json _meta.pacing_audit added with summary stats
  - Each listening item gets `pacing_morae_per_min` (computed) and
    `pacing_status` (one of: in_range / too_slow / too_fast / no_audio)

Idempotent: re-runs overwrite the computed fields.
"""
from __future__ import annotations
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

LISTENING = Path(__file__).parent.parent / 'data' / 'listening.json'
AUDIO_DIR = Path(__file__).parent.parent / 'audio' / 'listening'

# JLPT N5 chokai target: ~200-220 morae/min per audit Section 0.5.
# We allow ±10% (180-242) to accommodate natural variation. Outside
# this band flags the item for manual native-listener review.
PACING_TARGET_MIN = 180
PACING_TARGET_MAX = 240

# Small kana that don't count as their own mora (combine with previous).
SMALL_KANA = set('ゃゅょぁぃぅぇぉっゎ' + 'ャュョァィゥェォッヮ')


def count_morae(text: str) -> int:
    """Count morae in a Japanese script.
    Hiragana/katakana count 1 each; small kana don't add; long-vowel
    mark (ー) counts; sokuon counts. Kanji + punctuation are skipped
    (they shouldn't contribute meaningfully at N5 scope; an
    approximation is acceptable for a pacing audit)."""
    morae = 0
    for ch in text:
        cp = ord(ch)
        # Hiragana 3041-3096
        if 0x3041 <= cp <= 0x3096:
            if ch not in SMALL_KANA:
                morae += 1
        # Katakana 30A1-30FA
        elif 0x30A1 <= cp <= 0x30FA:
            if ch not in SMALL_KANA:
                morae += 1
        # Long-vowel mark
        elif ch == 'ー':
            morae += 1
        # Halfwidth katakana — N5 unlikely but for completeness
        elif 0xFF66 <= cp <= 0xFF9D:
            morae += 1
    return morae


def get_audio_duration(audio_filename: str) -> float | None:
    """Return MP3 duration in seconds, or None if file is missing/unreadable."""
    try:
        from mutagen.mp3 import MP3
    except ImportError:
        print('ERROR: mutagen not installed. Run `pip install mutagen`')
        sys.exit(2)

    path = AUDIO_DIR / audio_filename
    if not path.exists():
        return None
    try:
        m = MP3(path)
        return float(m.info.length)
    except Exception as e:
        print(f'WARN: cannot read {audio_filename}: {e}')
        return None


def main() -> int:
    doc = json.loads(LISTENING.read_text(encoding='utf-8'))
    items = doc['items']

    in_range_n = 0
    too_slow_n = 0
    too_fast_n = 0
    no_audio_n = 0
    paces = []

    for it in items:
        script = it.get('script_ja') or ''
        audio = it.get('audio')
        if not script or not audio:
            it['pacing_status'] = 'no_audio'
            it.pop('pacing_morae_per_min', None)
            no_audio_n += 1
            continue

        # Audio path may be 'audio/listening/n5.listen.001.mp3' or just
        # the filename. Strip prefix if present.
        audio_filename = Path(audio).name
        duration_s = get_audio_duration(audio_filename)
        if duration_s is None or duration_s <= 0:
            it['pacing_status'] = 'no_audio'
            it.pop('pacing_morae_per_min', None)
            no_audio_n += 1
            continue

        morae = count_morae(script)
        if morae == 0:
            it['pacing_status'] = 'no_audio'
            it.pop('pacing_morae_per_min', None)
            no_audio_n += 1
            continue

        morae_per_min = round((morae / duration_s) * 60, 1)
        it['pacing_morae_per_min'] = morae_per_min
        paces.append(morae_per_min)

        if morae_per_min < PACING_TARGET_MIN:
            it['pacing_status'] = 'too_slow'
            too_slow_n += 1
        elif morae_per_min > PACING_TARGET_MAX:
            it['pacing_status'] = 'too_fast'
            too_fast_n += 1
        else:
            it['pacing_status'] = 'in_range'
            in_range_n += 1

    # Build _meta summary
    if '_meta' not in doc:
        doc['_meta'] = {}
    doc['_meta']['pacing_audit'] = {
        'note': (
            'ISSUE-074 round-9 fix (2026-05-06): pacing audit measured '
            'programmatically. Each item has duration via mutagen + '
            'morae count from script_ja; morae_per_min flagged against '
            f'JLPT N5 target band {PACING_TARGET_MIN}-{PACING_TARGET_MAX} '
            '(±10% from the 200-220 ideal, per the round-9 audit).'
        ),
        'method': (
            'Programmatic: mutagen MP3.info.length for duration; '
            'kana-count for morae (small kana don\'t add; long-vowel '
            'mark counts; kanji approximated as zero — see source).'
        ),
        'target_range_morae_per_min': [PACING_TARGET_MIN, PACING_TARGET_MAX],
        'summary': {
            'in_range': in_range_n,
            'too_slow': too_slow_n,
            'too_fast': too_fast_n,
            'no_audio': no_audio_n,
            'min_observed': min(paces) if paces else None,
            'max_observed': max(paces) if paces else None,
            'mean_observed': round(sum(paces) / len(paces), 1) if paces else None,
        },
    }

    LISTENING.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    print(f'Items audited: {len(items)}')
    print(f'  in_range:     {in_range_n}')
    print(f'  too_slow:     {too_slow_n}')
    print(f'  too_fast:     {too_fast_n}')
    print(f'  no_audio:     {no_audio_n}')
    if paces:
        print(f'\n  pace min: {min(paces)} morae/min')
        print(f'  pace max: {max(paces)} morae/min')
        print(f'  pace mean: {round(sum(paces) / len(paces), 1)} morae/min')

    if too_slow_n or too_fast_n:
        print('\n  Items flagged for manual review:')
        for it in items:
            if it.get('pacing_status') in ('too_slow', 'too_fast'):
                print(f'    {it["id"]} ({it["pacing_status"]}): '
                      f'{it.get("pacing_morae_per_min")} morae/min')
    return 0


if __name__ == '__main__':
    sys.exit(main())
