"""Round-9 residual: 35 kanji at <3 examples (corpus-limited).

After ISSUE-101 closed in v1.12.43, 35 kanji remained at exactly 2
examples because their N5-only compound forms were exhausted. This
script adds a 3rd example to each by sourcing N5-whitelist-only
compounds from a wider standard-textbook list — including compounds
that combine two N5-whitelist kanji (which the round-9 fix script
had missed because they weren't in the curated CURATED_COMPOUNDS map).

Each compound:
  - Uses ONLY N5-whitelist kanji in its `form` field (JA-16)
  - Has correct furigana reading + English gloss
  - Drawn from Genki I, JLPT Sensei N5, JLPT.jp 旧出題基準

Idempotent: skips kanji already at >=3 examples; dedups by (form,reading).
"""
from __future__ import annotations
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

KANJI = Path(__file__).parent.parent / 'data' / 'kanji.json'

# Each compound uses ONLY N5-whitelist kanji.
# Format: kanji_glyph -> [{form, reading, gloss}]
RESIDUAL_COMPOUNDS = {
    '火': [{'form': '花火', 'reading': 'はなび', 'gloss': 'fireworks'}],
    '水': [{'form': '水道', 'reading': 'すいどう', 'gloss': 'water supply / tap water'}],
    '木': [{'form': '大木', 'reading': 'たいぼく', 'gloss': 'big tree'}],
    '金': [{'form': '金時', 'reading': 'きんとき', 'gloss': 'golden time / sweet potato dish (named after a folk hero)'}],
    '土': [{'form': '土の上', 'reading': 'つちのうえ', 'gloss': 'on top of the dirt / on the ground'}],
    '半': [{'form': '半年', 'reading': 'はんとし', 'gloss': 'half a year'}],
    '午': [{'form': '午後三時', 'reading': 'ごごさんじ', 'gloss': '3 p.m. (3 o\'clock in the afternoon)'}],
    '父': [{'form': '父母', 'reading': 'ふぼ', 'gloss': 'parents (father and mother; formal)'}],
    '母': [{'form': '母校', 'reading': 'ぼこう', 'gloss': 'alma mater (one\'s school)'}],
    '社': [{'form': '社長', 'reading': 'しゃちょう', 'gloss': 'company president'}],
    '小': [{'form': '小川', 'reading': 'こがわ', 'gloss': 'small stream / brook (also a common surname)'}],
    '上': [{'form': '上下', 'reading': 'じょうげ', 'gloss': 'top and bottom / up and down'}],
    '下': [{'form': '下山', 'reading': 'げざん', 'gloss': 'descending a mountain'}],
    '左': [{'form': '左右', 'reading': 'さゆう', 'gloss': 'left and right'}],
    '右': [{'form': '右上', 'reading': 'みぎうえ', 'gloss': 'upper right'}],
    '東': [{'form': '中東', 'reading': 'ちゅうとう', 'gloss': 'Middle East (geographic region)'}],
    '西': [{'form': '西日', 'reading': 'にしび', 'gloss': 'westerly sun (afternoon sunlight)'}],
    '南': [{'form': '南北', 'reading': 'なんぼく', 'gloss': 'north and south (axis)'}],
    '北': [{'form': '南北', 'reading': 'なんぼく', 'gloss': 'north and south (axis)'}],
    '山': [{'form': '山道', 'reading': 'やまみち', 'gloss': 'mountain path / trail'}],
    '雨': [{'form': '小雨', 'reading': 'こさめ', 'gloss': 'light rain / drizzle'}],
    '天': [{'form': '天の川', 'reading': 'あまのがわ', 'gloss': 'the Milky Way (lit. river of heaven)'}],
    '花': [{'form': '花火', 'reading': 'はなび', 'gloss': 'fireworks'}],
    '空': [{'form': '大空', 'reading': 'おおぞら', 'gloss': 'wide-open sky'}],
    '道': [{'form': '山道', 'reading': 'やまみち', 'gloss': 'mountain path / trail'}],
    '店': [{'form': '本店', 'reading': 'ほんてん', 'gloss': 'head store / main branch'}],
    '食': [{'form': '食前', 'reading': 'しょくぜん', 'gloss': 'before a meal (e.g. medicine instructions)'}],
    '飲': [{'form': '飲み水', 'reading': 'のみみず', 'gloss': 'drinking water'}],
    '立': [{'form': '立ち入り', 'reading': 'たちいり', 'gloss': 'entry / entering (often "立入禁止" = no entry)'}],
    '買': [{'form': '買い手', 'reading': 'かいて', 'gloss': 'buyer / purchaser'}],
    '安': [{'form': '大安', 'reading': 'たいあん', 'gloss': 'auspicious / lucky day (per Japanese calendar)'}],
    '新': [{'form': '新年', 'reading': 'しんねん', 'gloss': 'new year (the calendar new year)'}],
    '名': [{'form': '大名', 'reading': 'だいみょう', 'gloss': 'feudal lord (historical, Edo period)'}],
    '号': [{'form': '年号', 'reading': 'ねんごう', 'gloss': 'era name (e.g. 令和)'}],
    '私': [{'form': '私語', 'reading': 'しご', 'gloss': 'private talk / whispering'}],
}


def main() -> int:
    doc = json.loads(KANJI.read_text(encoding='utf-8'))
    wl = set(json.loads(
        (Path(__file__).parent.parent / 'data' / 'n5_kanji_whitelist.json').read_text(encoding='utf-8')
    ))

    n_added = 0
    n_skipped_full = 0
    n_dup = 0
    n_oos = 0

    for kx in doc['entries']:
        g = kx['glyph']
        existing = kx.get('examples', [])
        if len(existing) >= 3:
            n_skipped_full += 1
            continue
        if g not in RESIDUAL_COMPOUNDS:
            continue

        existing_keys = {(e.get('form'), e.get('reading')) for e in existing}
        for entry in RESIDUAL_COMPOUNDS[g]:
            # Validate JA-16: every kanji in form must be in whitelist
            ja_chars = [c for c in entry['form'] if 0x4E00 <= ord(c) <= 0x9FFF]
            oos = [c for c in ja_chars if c not in wl]
            if oos:
                n_oos += 1
                print(f'WARN: {g} - "{entry["form"]}" has OOS kanji {oos}; skipping')
                continue

            key = (entry['form'], entry['reading'])
            if key in existing_keys:
                n_dup += 1
                continue

            existing.append(entry)
            existing_keys.add(key)
            n_added += 1
            if len(existing) >= 3:
                break
        kx['examples'] = existing

    KANJI.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    # Update _meta to reflect closure
    doc2 = json.loads(KANJI.read_text(encoding='utf-8'))
    if '_meta' in doc2 and 'examples_corpus_constraint' in doc2['_meta']:
        still_under = [
            f'{x["glyph"]}: {len(x.get("examples", []))}'
            for x in doc2['entries']
            if len(x.get('examples', [])) < 3
        ]
        doc2['_meta']['examples_corpus_constraint']['kanji_below_3_examples_after_fix'] = still_under
        doc2['_meta']['examples_corpus_constraint']['note'] += (
            ' [Updated 2026-05-06 round-9 residual: dropped from 35 to '
            f'{len(still_under)} after the residual-compounds pass.]'
        )
        KANJI.write_text(
            json.dumps(doc2, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8'
        )

    counts = {}
    for x in doc2['entries']:
        n = len(x.get('examples', []))
        counts[n] = counts.get(n, 0) + 1
    at_3 = sum(1 for x in doc2['entries'] if len(x.get('examples', [])) >= 3)
    print(f'\nResidual examples added: {n_added}')
    print(f'  Skipped (already ≥3): {n_skipped_full}')
    print(f'  Skipped (dup): {n_dup}')
    print(f'  Skipped (OOS): {n_oos}')
    print(f'\nPost-fix examples-count distribution: {sorted(counts.items())}')
    print(f'Kanji with ≥3 examples: {at_3}/{len(doc2["entries"])}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
