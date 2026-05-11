"""Wave 3 — finish kanji etymology (lesson_order 62-106).

After this, coverage 61/106 -> 106/106 (100%).
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ETYMOLOGIES = {
    '後': {'origin_type': 'compound_ideograph',
           'story': '彳 (walking) + 幺 (small) + 夂 (footprint) — slow walker lagging behind. Came to mean "after / behind" in space and time.'},
    '外': {'origin_type': 'compound_ideograph',
           'story': '夕 (evening) + 卜 (divination) — evening divination done OUTSIDE the proper ritual schedule. Hence "outside / external".'},
    '東': {'origin_type': 'pictograph',
           'story': 'Pictograph of the sun (日) rising behind a tree (木) — the eastern horizon. Combined element captures sunrise direction.'},
    '西': {'origin_type': 'pictograph',
           'story': 'Pictograph of a bird in its nest (settling at sunset) — the direction the sun sets toward, "west".'},
    '南': {'origin_type': 'pictograph',
           'story': 'Pictograph of a bell-like musical instrument hung in the warm SOUTHERN exposure of an ancient hall. Came to denote the south compass direction.'},
    '北': {'origin_type': 'pictograph',
           'story': 'Pictograph of two people sitting back-to-back — the COLD direction one turns away from. Hence "north" (with the secondary connotation "to flee" surviving in 敗北).'},
    '間': {'origin_type': 'compound_ideograph',
           'story': '門 (gate) + 日 (sun) — sunlight visible BETWEEN the gate doors. The "in-between" sense extended to time intervals.'},
    '山': {'origin_type': 'pictograph',
           'story': 'Pictograph of three mountain peaks rising — central peak tallest, two flanking peaks. One of the oldest oracle-bone characters.'},
    '川': {'origin_type': 'pictograph',
           'story': 'Pictograph of three flowing streams — central current with two side waters. Captures the linear flow of a river.'},
    '田': {'origin_type': 'pictograph',
           'story': 'Pictograph of a rice paddy divided into four sections by levees — birds-eye view of cultivated land. The internal cross IS the paddy walls.'},
    '雨': {'origin_type': 'pictograph',
           'story': 'Pictograph of raindrops (4 dots) falling from a cloud (top horizontal) under the sky (top horizontal above it). Hence "rain".'},
    '天': {'origin_type': 'compound_ideograph',
           'story': '大 (big/person with arms outstretched) + a horizontal stroke above the head = "what is ABOVE the person" — heaven / sky.'},
    '気': {'origin_type': 'compound_ideograph',
           'story': 'Simplified from 氣 — 气 (steam / vapor rising) + 米 (rice). Steam rising from cooked rice = invisible essence / spirit / mood / air.'},
    '花': {'origin_type': 'phono_semantic',
           'story': '艹 (grass / plant radical) + 化 (change, phonetic) — the part of a plant that transforms (blooms). Hence "flower".'},
    '空': {'origin_type': 'compound_ideograph',
           'story': '穴 (hole / cave) + 工 (work / craft / pierce) — a hollowed-out, empty space. Came to mean "sky" (the vast empty above) and "empty".'},
    '電': {'origin_type': 'compound_ideograph',
           'story': '雨 (rain) + 申 (lightning bolt) — a lightning bolt during rain. Originally "lightning"; in modern Japanese, extended to "electricity".'},
    '車': {'origin_type': 'pictograph',
           'story': 'Pictograph of a chariot seen from above — two wheels (the dots on each side, now simplified into the framing strokes) and an axle (vertical line).'},
    '道': {'origin_type': 'compound_ideograph',
           'story': '辶 (move / walk) + 首 (head / neck) — to walk WITH ONE\'S HEAD AHEAD on a path. Came to mean "road / way / the Way (philosophy)".'},
    '店': {'origin_type': 'compound_ideograph',
           'story': '广 (roofed structure) + 占 (occupy / claim a spot) — a roofed place where someone has claimed a spot to sell goods. Hence "shop".'},
    '駅': {'origin_type': 'compound_ideograph',
           'story': 'Simplified from 驛 — 馬 (horse) + 尺 (measure / station post). A relay station where horses were swapped. Modern: train station.'},
    '食': {'origin_type': 'pictograph',
           'story': 'Pictograph of a covered vessel of cooked food — top is the lid, body is the container holding rice or grain. Hence "to eat / food".'},
    '飲': {'origin_type': 'compound_ideograph',
           'story': '食 (food / drink) + 欠 (open mouth / yawn) — the action of opening one\'s mouth to take in fluid. Specifically "to drink" (vs eat).'},
    '見': {'origin_type': 'compound_ideograph',
           'story': '目 (eye) on top of 人 (legs/person) — a person with prominent eye, the act of LOOKING. The eye stands tall.'},
    '聞': {'origin_type': 'compound_ideograph',
           'story': '門 (gate) + 耳 (ear) — listening at the gate. Came to mean "hear / listen / ask".'},
    '読': {'origin_type': 'phono_semantic',
           'story': '言 (speech / word radical) + 売 (sell, phonetic component, simplified from 賣). The 言 anchors it as a speech-related action: "to read aloud".'},
    '書': {'origin_type': 'compound_ideograph',
           'story': '聿 (brush) + 者 (person / object) — a person holding a brush. Hence "to write" and "writing / book / document".'},
    '話': {'origin_type': 'compound_ideograph',
           'story': '言 (speech) + 舌 (tongue) — the act of moving the tongue to speak. Hence "to talk / story / conversation".'},
    '来': {'origin_type': 'pictograph',
           'story': 'Pictograph of a ripening grain plant (wheat / barley) — originally meant the grain itself. Borrowed phonetically for "to come" in ancient Chinese; the grain meaning migrated to other characters.'},
    '行': {'origin_type': 'pictograph',
           'story': 'Pictograph of a crossroads / intersection — two paths crossing. Originally meant "intersection / road"; came to mean "to go / conduct" via the road sense.'},
    '出': {'origin_type': 'pictograph',
           'story': 'Pictograph of a plant emerging from the ground — vertical stroke up + horizontal base. Captures "to come out / exit / produce".'},
    '入': {'origin_type': 'pictograph',
           'story': 'Pictograph of an arrow or pointed object entering — two strokes converging downward. Captures "to enter / put in".'},
    '立': {'origin_type': 'pictograph',
           'story': 'Pictograph of a person STANDING on the ground (横 horizontal bar at bottom). Captures the stance of standing upright.'},
    '休': {'origin_type': 'compound_ideograph',
           'story': '亻 (person) + 木 (tree) — a person resting under a tree. Captures "to rest / take a break".'},
    '言': {'origin_type': 'compound_ideograph',
           'story': '辛 (knife / sharp) + 口 (mouth) — words come out of the mouth like cuts from a blade. Hence "to say / word".'},
    '買': {'origin_type': 'compound_ideograph',
           'story': '罒 (net / catch) + 貝 (shell / money) — to catch / acquire something using money. Hence "to buy".'},
    '高': {'origin_type': 'pictograph',
           'story': 'Pictograph of a tall multi-story building / tower seen from the side. Captures "high / tall" through architectural elevation.'},
    '安': {'origin_type': 'compound_ideograph',
           'story': '宀 (roof / house) + 女 (woman) — a woman safely at home under a roof. Originally "peaceful / safe"; extended to "cheap / inexpensive (no risk)".'},
    '新': {'origin_type': 'phono_semantic',
           'story': '木 (tree) + 斤 (axe) + 立 (stand) — chopping NEW wood with an axe. Hence "new / fresh".'},
    '古': {'origin_type': 'compound_ideograph',
           'story': '十 (ten) + 口 (mouth) — what has been spoken (mouth) for ten generations. Captures "old / antique".'},
    '長': {'origin_type': 'pictograph',
           'story': 'Pictograph of a long-haired elder with a staff — captures "long" (physical length) and "leader / elder" (the long-haired one in authority).'},
    '白': {'origin_type': 'pictograph',
           'story': 'Pictograph of an acorn / sun ray / thumbnail (etymology contested). The leading ノ stroke distinguishes 白 (white) from 日 (sun). One reading: a sunbeam shining white.'},
    '名': {'origin_type': 'compound_ideograph',
           'story': '夕 (evening) + 口 (mouth) — in the evening dark you must SAY your NAME to be recognized. Hence "name".'},
    '番': {'origin_type': 'compound_ideograph',
           'story': '釆 (animal tracks pattern) + 田 (field) — taking turns walking the field paths. Came to mean "ordinal number / turn / one\'s position in a sequence".'},
    '号': {'origin_type': 'compound_ideograph',
           'story': '口 (mouth) + 丂 (signal flag / breath) — making a signal by mouth. Hence "to call out / number / signal".'},
    '私': {'origin_type': 'compound_ideograph',
           'story': '禾 (grain plant) + 厶 (self / private) — one\'s own private grain (vs the lord\'s public grain). Hence "I / private / personal".'},
}


def main() -> int:
    fp = ROOT / 'data' / 'kanji.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_etymology_wave3')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')
    data = json.loads(fp.read_text(encoding='utf-8'))
    entries = data.get('entries', data) if isinstance(data, dict) else data
    entries_iter = entries.values() if isinstance(entries, dict) else entries
    by_glyph = {e.get('glyph'): e for e in entries_iter}
    n = 0
    for glyph, etym in ETYMOLOGIES.items():
        if glyph not in by_glyph:
            print(f'  ! missing: {glyph}'); continue
        e = by_glyph[glyph]
        if e.get('etymology'):
            print(f'  - skip: {glyph}'); continue
        e['etymology'] = etym
        e['etymology_provenance'] = 'llm_curated'
        n += 1
    print(f'\nWave 3 added etymology on {n} more kanji.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
