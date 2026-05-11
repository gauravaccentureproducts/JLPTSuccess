"""Deepen the 12 stroke_order_trap entries whose `trap` field is
under 30 characters.

Audit context: the 2026-05-09 richness audit's
`stroke-order mistakes annotated 25/106` reflected entries where
the `trap` field actually described a learner mistake (vs. just
the structural decomposition). 12 entries had short structural
notes in the `trap` slot that belonged in `correct_order_summary`
instead.

The renderer (js/kanji.js #renderStrokeOrderTrap) labels the
fields as:
  trap                   -> "What learners get wrong"
  correct_order_summary  -> "Correct order"
  why_it_matters         -> "Why it matters"

This script rewrites `trap` on each of the 12 to describe the
ACTUAL learner mistake. correct_order_summary + why_it_matters
remain untouched.

Provenance bump: stroke_order_trap_provenance stays `llm_curated`
(unchanged).
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

TRAPS = {
    '男': "Two common errors: (a) writing 力 first (left-to-right scan instinct), and (b) drawing 田 with the inner cross out of order. The cross inside 田 always comes after the outer box closes.",
    '会': "Many learners draw the bottom 云 first because it's the more prominent element. The top 人-hat (ノ then ╲) must come first — the same rule as 入 / 八 / 全.",
    '社': "The left radical 示 (ねへん) must finish completely before 土 starts. A common slip is interleaving — drawing 示's leftmost ノ, then jumping to 土's top horizontal.",
    '空': "Learners often start 工 before closing 穴 on top. The 穴 cap (5 strokes) is a single self-contained unit that must finish first — same hat-first rule as 究 / 突.",
    '書': "Starting with the bottom 曰 is the typical mistake. The order is the top horizontal first, then the 聿-like upper block top-to-bottom, then 曰 last. Mirror of the more visible bottom-half.",
    '話': "Drawing 舌 (the right element) before completing 言 (the left radical, ごんべん). All radical-on-left kanji follow left-first: finish 言 entirely, then start 舌.",
    '来': "Two issues: (a) confusing the central structure with 末 (similar silhouette, different mid-element), and (b) stroking the central vertical before completing the top horizontal. Top horizontal first, then the central frame top-down.",
    '休': "Drawing 木 (the right element) before 亻 (the left radical, にんべん). All にんべん kanji are left-first: finish 亻 (2 strokes), then start 木.",
    '安': "Drawing 女 before fully closing 宀 (うかんむり) is one slip; the other is reversing 女's own internal order — 女's long horizontal cross-stroke comes LAST, not first.",
    '古': "Writing 口 first is the common mistake. The 十 on top (horizontal then vertical) precedes the 口 box — top-down assembly. Inside 口, follow standard box rule (left side / top+right bracket / bottom horizontal).",
    '白': "Omitting the leading ノ turns 白 into 日 — a different kanji entirely. The short ノ at the very top is stroke #1, and is what distinguishes 白 from 日 visually and orthographically.",
    '号': "Writing the bottom 丂 before completing 口 is the typical mistake. The structure is top-down: 口 (3 strokes) first, then 丂 (horizontal then hook+curl). Same top-first rule as 員 / 品.",
}


def main() -> int:
    fp = ROOT / 'data' / 'kanji.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_stroke_traps_deepen')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    entries = data.get('entries', data) if isinstance(data, dict) else data
    entries_iter = entries.values() if isinstance(entries, dict) else entries
    by_glyph = {e.get('glyph'): e for e in entries_iter}

    n = 0
    for glyph, new_trap in TRAPS.items():
        if glyph not in by_glyph:
            print(f'  ! missing in data: {glyph}')
            continue
        e = by_glyph[glyph]
        cur = e.get('stroke_order_trap')
        if not isinstance(cur, dict):
            print(f'  ! {glyph}: stroke_order_trap not a dict')
            continue
        # Only deepen if the existing trap is short (<30 chars)
        if len(cur.get('trap', '')) >= 30:
            print(f'  - skip (trap already long): {glyph}')
            continue
        old = cur.get('trap', '')
        cur['trap'] = new_trap
        # Provenance stays llm_curated (unchanged).
        n += 1
        print(f'  + {glyph}: {len(old)} -> {len(new_trap)} chars')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nDeepened {n} stroke_order_trap entries.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
