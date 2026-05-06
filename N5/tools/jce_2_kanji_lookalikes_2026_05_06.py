"""JCE-2: Author `look_alike` cross-link field on N5 kanji entries.

Adds a `look_alike` array per entry — list of visually-confusable kanji
with each glyph's visual-difference annotation. Enables explicit
cross-link cards on the kanji detail page so learners do not silently
conflate them.

Schema (each look_alike entry):
  {
    "glyph": "<kanji>",            # the look-alike glyph
    "in_n5": true | false,         # whether it's in this app's N5 set
    "diff": "<short visual diff>"  # what learners must notice
  }

The 8 confusable N5 clusters per the N5Improvement.txt audit prompt:
  - 大/犬/太 (dot moves)
  - 木/本/末/未 (line position)
  - 人/入/八 (radical similarity)
  - 日/目/白 (rectangle variations)
  - 千/干/王/玉 (vertical bar)
  - 上/止/正 (cross-bar position)
  - 古/占 (stroke count)
  - 千/午 (top stroke direction)

For kanji not in N5 (e.g., 末, 未, 干, 王, 玉, 止, 正, 占, 太, 犬), the
cross-link is still authored on the in-N5 partner side — the learner
benefits from knowing "this looks like X" even if X isn't in their
core deck. Marked `in_n5: false` on those entries so the renderer can
gray-style them or omit deep-link.

Idempotent: skips entries that already have a populated look_alike.
Marks `look_alike_provenance: llm_curated` on each authored entry.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KANJI = ROOT / 'data' / 'kanji.json'

# Each cluster lists every member with the visual difference it has
# from its siblings. The renderer is expected to show "Compare with: ..."
# on each kanji's detail page using this data.
CLUSTERS: list[dict[str, list[dict]]] = [
    # 大 / 犬 / 太 — dot position changes meaning
    {
        '大': [
            {'glyph': '犬', 'in_n5': False, 'diff': '点 (dot) above the right shoulder = "dog"'},
            {'glyph': '太', 'in_n5': False, 'diff': '点 (dot) inside the lower triangle = "thick / fat"'},
        ],
    },
    # 木 / 本 / 末 / 未 — horizontal line position changes meaning
    {
        '木': [
            {'glyph': '本', 'in_n5': True, 'diff': 'extra short horizontal stroke at the base = "origin / book"'},
            {'glyph': '末', 'in_n5': False, 'diff': 'extra horizontal stroke at the TOP, short = "end / extremity"'},
            {'glyph': '未', 'in_n5': False, 'diff': 'extra horizontal stroke at the TOP, longer than 末 = "not yet"'},
        ],
        '本': [
            {'glyph': '木', 'in_n5': True, 'diff': 'no base stroke = "tree"'},
            {'glyph': '末', 'in_n5': False, 'diff': 'extra stroke is at TOP not BASE = "end"'},
            {'glyph': '未', 'in_n5': False, 'diff': 'extra stroke is at TOP, longer = "not yet"'},
        ],
    },
    # 人 / 入 / 八 — opening direction / line angle
    {
        '人': [
            {'glyph': '入', 'in_n5': True, 'diff': 'left stroke goes UP-then-down (like an arrow entering from the right); 人 left stroke goes straight down-left'},
            {'glyph': '八', 'in_n5': True, 'diff': 'two short separate strokes that do NOT touch at the top'},
        ],
        '入': [
            {'glyph': '人', 'in_n5': True, 'diff': 'left stroke goes straight down-left (no upward hook)'},
            {'glyph': '八', 'in_n5': True, 'diff': 'two short separate strokes that do NOT touch at the top'},
        ],
        '八': [
            {'glyph': '人', 'in_n5': True, 'diff': 'two strokes TOUCH at the top (one continuous V); 八 strokes are separate'},
            {'glyph': '入', 'in_n5': True, 'diff': 'left stroke has an upward hook; 八 strokes are short and separate'},
        ],
    },
    # 日 / 目 / 白 — number of internal lines, top hook
    {
        '日': [
            {'glyph': '目', 'in_n5': True, 'diff': 'TWO horizontal strokes inside the box (vs 日 = 一 stroke)'},
            {'glyph': '白', 'in_n5': True, 'diff': 'has a 丿 (slash) on top of the box'},
        ],
        '目': [
            {'glyph': '日', 'in_n5': True, 'diff': 'ONE horizontal stroke inside the box'},
            {'glyph': '白', 'in_n5': True, 'diff': 'has a 丿 on top + ONE inside stroke'},
        ],
        '白': [
            {'glyph': '日', 'in_n5': True, 'diff': 'no 丿 on top; ONE inside stroke'},
            {'glyph': '目', 'in_n5': True, 'diff': 'no 丿 on top; TWO inside strokes'},
        ],
    },
    # 千 / 干 / 王 / 玉 — vertical bar variations
    {
        '千': [
            {'glyph': '干', 'in_n5': False, 'diff': 'TWO horizontal strokes (top + middle); 千 has only ONE plus a 丿'},
            {'glyph': '王', 'in_n5': False, 'diff': 'THREE horizontal strokes (king); 千 has 1 + 丿'},
            {'glyph': '玉', 'in_n5': False, 'diff': 'THREE horizontal + 点 (dot) = "ball / jewel"'},
            {'glyph': '午', 'in_n5': True, 'diff': 'top stroke is a 丿 (slash going LEFT); 千 top stroke goes RIGHT'},
        ],
    },
    # 上 / 止 / 正 — cross-bar / extra strokes
    {
        '上': [
            {'glyph': '止', 'in_n5': False, 'diff': 'extra short top horizontal + 丨 inside = "stop"'},
            {'glyph': '正', 'in_n5': False, 'diff': 'has an extra horizontal stroke + 一 base = "correct"'},
        ],
    },
    # 古 / 占 — stroke count difference
    {
        '古': [
            {'glyph': '占', 'in_n5': False, 'diff': 'top stroke is 卜 (vertical + dot); 古 top is 十 (cross). Different meaning entirely'},
        ],
    },
    # 千 / 午 — top stroke direction
    {
        '午': [
            {'glyph': '千', 'in_n5': True, 'diff': 'top stroke goes RIGHT (丿 sweep); 午 top stroke goes LEFT'},
        ],
    },
]


def main():
    with KANJI.open('r', encoding='utf-8') as f:
        data = json.load(f)

    entries = data['entries']
    by_glyph: dict[str, dict] = {e.get('glyph'): e for e in entries if e.get('glyph')}

    # Flatten clusters into glyph -> look_alike list
    seed: dict[str, list[dict]] = {}
    for cluster in CLUSTERS:
        for glyph, look_alikes in cluster.items():
            seed.setdefault(glyph, []).extend(look_alikes)

    matched = 0
    skipped = 0
    not_in_corpus = []
    for glyph, look_alikes in seed.items():
        entry = by_glyph.get(glyph)
        if entry is None:
            not_in_corpus.append(glyph)
            continue
        if entry.get('look_alike'):
            skipped += 1
            continue
        # De-duplicate by glyph (multiple clusters can name the same partner)
        seen = set()
        unique = []
        for la in look_alikes:
            g = la.get('glyph')
            if g and g not in seen:
                seen.add(g)
                unique.append(la)
        entry['look_alike'] = unique
        # Mark provenance
        prov = entry.get('look_alike_provenance') or 'llm_curated'
        entry['look_alike_provenance'] = prov
        matched += 1

    print(f'Authored look_alike on {matched} kanji.')
    print(f'Skipped (already had look_alike): {skipped}.')
    if not_in_corpus:
        print(f'Glyphs in cluster but not in N5 corpus (cross-link is one-way): {not_in_corpus}')

    with KANJI.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Wrote: {KANJI}')


if __name__ == '__main__':
    main()
