#!/usr/bin/env python3
"""
TS-02 near-duplicate polish (post-reviewer-v5 correction).

Reviewer corrected my TS-02 over-strict flagging: 43 of the 60 flagged
"duplicates" are intentional kana↔kanji pedagogical variants (a feature,
not a bug); 11 are real near-duplicates of which 5 are arguably intentional
contrasts (へ vs に, synonyms, etc.) and 6 are likely accidental.

This script:

1. DROPS 6 clearly-accidental near-duplicate example rows (these are
   redundant; can be dropped without changing teaching intent).
2. ANNOTATES the 5 intentional-contrast pairs with
   `intentional_variant_pair: <other_index>` so future audits skip them.

Dropping examples is safe: no JA invariant requires exact 10/pattern.
The audio files for dropped examples become orphans (logged for future
manifest trimming, same approach as BUG-D leftover).
"""
import argparse
import json
from pathlib import Path

GRAMMAR = Path('data/grammar.json')
INDEX = Path('data/index.json')
FIX_LOG = Path('data/grammar.fix_log.json')

PROV = "auto_fix_2026_05_24"
AUDIT_WAVE = "claude_audit_2026_05_24"
REVIEW_STATUS = "ai_native_reviewer_2026_05_24"


def lf_size(path: Path) -> int:
    return len(path.read_bytes().replace(b"\r\n", b"\n"))


# Six clearly-accidental near-duplicates to drop.
# Drop the SECOND occurrence (higher index) of each pair to preserve
# the earlier-authored example as canonical.
DROPS = [
    ('n5-034', 9, 'duplicate of [4] modulo digit-vs-kana spelling (100→ひゃく)'),
    ('n5-035', 9, 'duplicate of [2] modulo digit-vs-kana spelling (10→じゅう)'),
    ('n5-092', 7, 'duplicate of [0] sans 上 (locative position word) — accidental'),
    ('n5-093', 7, 'duplicate of [0] sans 上 (locative position word) — accidental'),
    ('n5-103', 4, 'duplicate of [0] — expanded form (話す ことが できます) carries same EN'),
    ('n5-109', 6, 'word-order variant of [4]; same content, no contrastive intent'),
]

# Five intentional-contrast pairs to annotate (keep both; mark intent).
ANNOTATIONS = [
    ('n5-044', 4, 7, 'teaches synonym pair やる vs する for verb-of-doing'),
    ('n5-059', 0, 9, 'teaches topic-drop (with vs without わたしは)'),
    ('n5-062', 1, 8, 'teaches へ vs に particle equivalence for destination'),
    ('n5-073', 2, 5, 'teaches word-order flexibility with まだ + V-ていません'),
    ('n5-082', 1, 8, 'teaches その vs あの demonstrative contrast (mid-distance vs far)'),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    g = json.loads(GRAMMAR.read_text(encoding='utf-8'))

    drops_log = []
    annotations_log = []
    orphan_audio = []

    # 1. Drop accidentals
    for pid, drop_idx, reason in DROPS:
        for p in g['patterns']:
            if p['id'] != pid:
                continue
            exs = p.get('examples') or []
            if drop_idx >= len(exs):
                print(f'  WARN: {pid} ex[{drop_idx}] out of range, skipping')
                continue
            dropped = exs[drop_idx]
            audio = dropped.get('audio')
            if audio:
                orphan_audio.append(audio)
            del exs[drop_idx]
            # Tag pattern as touched
            p['provenance'] = PROV
            p['audit_wave'] = AUDIT_WAVE
            drops_log.append({
                'pattern': pid,
                'dropped_index': drop_idx,
                'dropped_example': dropped,
                'reason': reason,
                'orphan_audio': audio,
            })
            print(f'  DROP {pid} ex[{drop_idx}]: {reason}')

    # 2. Annotate intentional contrasts
    for pid, idx_a, idx_b, intent in ANNOTATIONS:
        for p in g['patterns']:
            if p['id'] != pid:
                continue
            exs = p.get('examples') or []
            if idx_a < len(exs) and idx_b < len(exs):
                exs[idx_a]['intentional_variant_pair'] = idx_b
                exs[idx_b]['intentional_variant_pair'] = idx_a
                exs[idx_a]['intentional_variant_intent'] = intent
                exs[idx_b]['intentional_variant_intent'] = intent
                annotations_log.append({
                    'pattern': pid,
                    'pair': (idx_a, idx_b),
                    'intent': intent,
                })
                print(f'  ANNOTATE {pid} ex[{idx_a}]<->ex[{idx_b}]: {intent}')

    g['_meta']['version'] = '2026.05.24-ts02-polish'
    g['_meta']['ts02_near_dup_polish_2026_05_24'] = (
        f'Reviewer v5 correction applied: 6 accidental near-duplicate examples dropped; '
        f'5 intentional-contrast example pairs annotated with intentional_variant_pair '
        f'markers. 43 kana↔kanji pedagogical variants retained as-is per reviewer guidance.'
    )

    if args.apply:
        out = json.dumps(g, ensure_ascii=False, indent=2)
        GRAMMAR.write_text(out + '\n', encoding='utf-8')

        idx_json = json.loads(INDEX.read_text(encoding='utf-8'))
        new_size = lf_size(GRAMMAR)
        for entry in idx_json.get('files', []):
            if entry.get('path') == 'data/grammar.json':
                entry['size_bytes'] = new_size
                break
        INDEX.write_text(json.dumps(idx_json, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        log = json.loads(FIX_LOG.read_text(encoding='utf-8'))
        log['TS02_near_dup_polish_2026_05_24'] = {
            'description': (
                'Reviewer v5 correction applied to TS-02 near-duplicates. '
                'Distinguished kana↔kanji pedagogical variants (kept) from '
                'intentional-contrast pairs (annotated) from accidental near-duplicates (dropped).'
            ),
            'drops': drops_log,
            'annotations': annotations_log,
            'orphan_audio_files': orphan_audio,
            'note': (
                'Orphan audio files exist on disk; audio_manifest entries remain. '
                'Consistent with BUG-D leftover handling (Part 56). Manifest trim '
                'deferred to a future cleanup pass.'
            ),
        }
        FIX_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'\napplied. grammar.json LF size: {new_size}')
    else:
        print('\n--dry-run')


if __name__ == '__main__':
    main()
