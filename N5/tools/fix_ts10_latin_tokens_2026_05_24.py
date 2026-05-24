#!/usr/bin/env python3
"""
Fix TS-10 Latin-token content issues in meaning_ja on 5 patterns.

Native-teacher review found:
- n5-165: 'wa-go' / 'kan-go' Latin terms → replace with 和語 / 漢語
- n5-183: '(with negative)' English aside → ない／ません と いっしょに
- n5-185: '(with negative)' English aside → ない／ません と いっしょに
- n5-186: placeholder 'question word + か / も' → real Japanese description
- n5-187: placeholder 'question word + か / も' → real Japanese description

The 20 patterns with 'Verb-' / 'Verb-stem' / 'counter' Latin slot-tokens
are LEGITIMATE pedagogical slot notation (per the convention used
throughout the corpus) — those don't need fixing; the audit tool
needs whitelist extension instead.
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


# Native-teacher rewrites for meaning_ja
REWRITES = {
    'n5-165': {
        'meaning_ja': (
            "「お〜／ご〜」は ことばの 前に つけて、ていねいな いいかたを つくります。"
            "お は 和語（やまとことば）に つけます：お花、お水。"
            "ご は 漢語（中国から きた ことば）に つけます：ごりょうしん、ごあいさつ。"
        ),
        'reason': 'wa-go/kan-go Latin terms replaced with 和語/漢語 (with Japanese gloss).',
    },
    'n5-183': {
        'meaning_ja': (
            "「だれか／なにか／どこか」は ある人・もの・ばしょを いいます。"
            "「だれも／なにも／どこも」は ない／ません と いっしょに つかって、"
            "「いない・ない」と いう いみに なります。"
        ),
        'reason': '"(with negative)" English aside replaced with ない／ません と いっしょに.',
    },
    'n5-185': {
        'meaning_ja': (
            "「だれか」は 「ある人」、「だれも」は ない／ません と いっしょに つかって "
            "「みんな〜ない／いない」を いいます。「だれかが 来ました」「だれも いません」。"
        ),
        'reason': '"(with negative)" English aside replaced.',
    },
    'n5-186': {
        'meaning_ja': (
            "「どこか」は ある ばしょを いいます。"
            "「どこも」は ない／ません と いっしょに つかって、"
            "「どこにも 〜ない」と いう いみに なります。"
            "「どこかへ 行きたいです」「どこも あいて いません」。"
        ),
        'reason': 'Replaced placeholder "question word + か / も" with real native-teacher description.',
    },
    'n5-187': {
        'meaning_ja': (
            "「いつか」は ある とき（みらいの こと）、"
            "「いつも」は つねに する こと（しゅうかん）を いいます。"
            "「いつか 日本に 行きたいです」「いつも 朝 7時に おきます」。"
        ),
        'reason': 'Replaced placeholder "question word + か / も" with real native-teacher description.',
    },
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()

    g = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    changes = []

    for p in g['patterns']:
        if p['id'] in REWRITES:
            repl = REWRITES[p['id']]
            before = p.get('meaning_ja', '')
            p['meaning_ja'] = repl['meaning_ja']
            p['provenance'] = PROV
            p['audit_wave'] = AUDIT_WAVE
            p['review_status'] = REVIEW_STATUS
            p['reviewer_note'] = repl['reason']
            changes.append({
                'pattern': p['id'],
                'before': before,
                'after': p['meaning_ja'],
                'reason': repl['reason'],
            })
            print(f'  {p["id"]}: {repl["reason"][:80]}')

    g['_meta']['version'] = '2026.05.24-ts10-cleanup'

    if args.apply:
        out = json.dumps(g, ensure_ascii=False, indent=2)
        GRAMMAR.write_text(out + '\n', encoding='utf-8')
        idx = json.loads(INDEX.read_text(encoding='utf-8'))
        new_size = lf_size(GRAMMAR)
        for entry in idx.get('files', []):
            if entry.get('path') == 'data/grammar.json':
                entry['size_bytes'] = new_size
                break
        INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

        log = json.loads(FIX_LOG.read_text(encoding='utf-8'))
        log['TS10_latin_token_cleanup'] = {
            'description': (
                'Native-teacher rewrite of meaning_ja on 5 patterns where Latin '
                'tokens were either explanatory English asides (n5-183/185 with '
                'negative), foreign-word Latin transcriptions (n5-165 wa-go/kan-go), '
                'or placeholder slot-labels left from initial authoring (n5-186/187).'
            ),
            'changes': changes,
        }
        FIX_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f'\napplied. grammar.json LF size: {new_size}')
    else:
        print('\n--dry-run')


if __name__ == '__main__':
    main()
