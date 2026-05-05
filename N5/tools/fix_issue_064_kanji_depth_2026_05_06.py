"""ISSUE-064 + IMP-082 (audit round-7, 2026-05-06): kanji depth fields.

Adds three optional fields to data/kanji.json entries:
  radical                — primary radical name + glyph
  radical_decomposition  — list of components (kanji or radical bits)
  mnemonic               — one-line memorable phrase tying components to meaning

Covers all 106 N5 kanji. Authored from N5-syllabus knowledge — no
external KanjiVG dependency. Decomposition is component-level (not
stroke-level) so it doubles as visual-mnemonic seed.

Idempotent: re-running diffs against existing values and updates only
when changed.

Native review pending: tag meanings_provenance stays as-is; we are
adding NEW fields, not retranslating existing ones.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
KF = ROOT / 'data' / 'kanji.json'

# Each kanji -> (radical_glyph, radical_name, [components], mnemonic_en)
# Components are listed by visual-spatial order (top-to-bottom, left-to-right).
# Mnemonics are concise + memorable; native review later refines.
KANJI_DEPTH = {
    # === Numbers 1-10 ===
    '一': ('一', 'one (radical 1)',           ['一'],         'A single horizontal stroke = ONE.'),
    '二': ('二', 'two',                        ['一', '一'],   'Two horizontal strokes = TWO.'),
    '三': ('一', 'one (radical 1)',            ['一', '一', '一'], 'Three horizontal strokes = THREE.'),
    '四': ('囗', 'enclosure',                  ['囗', '儿'],   'Four legs (儿) inside a box = FOUR.'),
    '五': ('一', 'one (radical 1)',            ['一', '丁', '一'], 'Roman numeral V tilted between two horizontal lines = FIVE.'),
    '六': ('八', 'eight',                       ['亠', '八'],   'A lid (亠) over a split (八) = SIX.'),
    '七': ('一', 'one (radical 1)',            ['七'],         'A horizontal stroke crossed by a hook = SEVEN.'),
    '八': ('八', 'eight (radical 12)',         ['八'],         'Two strokes splitting outward like a fan = EIGHT.'),
    '九': ('乙', 'second / hook',              ['丿', '乙'],   'A diagonal hook curling like the digit 9 = NINE.'),
    '十': ('十', 'ten (radical 24)',           ['十'],         'A plus sign — Roman numeral X rotated = TEN.'),
    # === Larger numbers + money ===
    '百': ('白', 'white',                      ['一', '白'],   'One (一) over white (白) = a HUNDRED whitewashed walls.'),
    '千': ('十', 'ten',                        ['丿', '十'],   'A slash (丿) over ten (十) = a THOUSAND tally marks.'),
    '万': ('一', 'one',                        ['一', '万'],   'A swooping line tied off = TEN THOUSAND.'),
    '円': ('冂', 'down box',                   ['冂', '土'],   'Inside the box (冂) is earth (土) = round YEN coin.'),
    # === Time: day / month / year ===
    '日': ('日', 'sun (radical 72)',           ['日'],         'A box with a stroke inside = the SUN, a DAY.'),
    '月': ('月', 'moon (radical 74)',          ['月'],         'A crescent shape = the MOON, a MONTH.'),
    '火': ('火', 'fire (radical 86)',          ['火'],         'Flames flickering upward = FIRE.'),
    '水': ('水', 'water (radical 85)',         ['水'],         'A central drop with splashes = WATER.'),
    '木': ('木', 'tree (radical 75)',          ['木'],         'A trunk with branches and roots = TREE.'),
    '金': ('金', 'metal/gold (radical 167)',   ['人', '王', '丶'], 'A person (人) over a king (王) with two specks of gold = METAL/GOLD.'),
    '土': ('土', 'earth (radical 32)',         ['十', '一'],   'A cross stuck in the ground = EARTH.'),
    '曜': ('日', 'sun',                        ['日', '羽', '隹'], 'Sun (日) + feathers (羽) + bird (隹) — DAY OF THE WEEK named after a celestial body.'),
    '年': ('干', 'dry',                        ['一', '丨', '干'], 'A stalk grown over time = a YEAR.'),
    '時': ('日', 'sun',                        ['日', '寺'],   'Sun (日) + temple (寺, time-keeper) = TIME / hour.'),
    '分': ('刀', 'knife',                      ['八', '刀'],   'Splitting (八) with a knife (刀) = MINUTE / divide.'),
    '半': ('十', 'ten',                        ['丷', '一', '十'], 'Mark cutting in two = HALF.'),
    '今': ('人', 'person',                     ['人', '丶', '一'], 'A person under a roof at this very instant = NOW.'),
    '毎': ('毋', 'mother',                     ['人', '母'],   'A person (人) over a mother (母) — every child has one = EVERY.'),
    '週': ('辶', 'walk',                       ['辶', '周'],   'Walking (辶) around (周) the calendar = WEEK.'),
    '午': ('十', 'ten',                        ['丿', '十'],   'A pestle pointing down at noon = NOON.'),
    # === Question word ===
    '何': ('亻', 'person (left form)',         ['亻', '可'],   'A person (亻) asking what is possible (可) = WHAT.'),
    # === People / family / body ===
    '人': ('人', 'person (radical 9)',         ['人'],         'Two legs walking = a PERSON.'),
    '男': ('田', 'rice paddy',                 ['田', '力'],   'Power (力) in the rice field (田) = MAN.'),
    '女': ('女', 'woman (radical 38)',         ['女'],         'A figure with crossed legs sitting gracefully = WOMAN.'),
    '子': ('子', 'child (radical 39)',         ['子'],         'A baby with arms outstretched and swaddled = CHILD.'),
    '父': ('父', 'father (radical 88)',        ['父'],         'Two crossing strokes — paternal authority figure = FATHER.'),
    '母': ('母', 'mother (radical 80)',        ['母'],         'Two breasts inside a body = MOTHER.'),
    '友': ('又', 'right hand',                 ['ナ', '又'],   'Two hands clasped = FRIEND.'),
    '先': ('儿', 'human legs',                 ['牛', '儿'],   'A person (儿) striding ahead = PREVIOUS / earlier.'),
    '生': ('生', 'birth/life (radical 100)',   ['生'],         'A plant sprouting from the soil = LIFE / birth.'),
    '手': ('手', 'hand (radical 64)',          ['手'],         'Five fingers spreading from a wrist = HAND.'),
    '足': ('足', 'foot (radical 157)',         ['口', '止'],   'Mouth-shape (口) over stop (止) = FOOT (where you stop).'),
    '目': ('目', 'eye (radical 109)',          ['目'],         'A vertical eye with pupil-bars = EYE.'),
    '口': ('口', 'mouth (radical 30)',         ['口'],         'A square opening = MOUTH.'),
    '力': ('力', 'power (radical 19)',         ['力'],         'A flexed arm muscle = POWER.'),
    # === School / society ===
    '学': ('子', 'child',                      ['ツ', '冖', '子'], 'A child (子) under a roof (冖) with knowledge crowning down = STUDY.'),
    '校': ('木', 'tree',                       ['木', '交'],   'Tree (木) where people meet (交) = SCHOOL.'),
    '本': ('木', 'tree',                       ['木', '一'],   'A line at the root of a tree (木) = ORIGIN / book.'),
    '語': ('言', 'speech (radical 149)',       ['言', '吾'],   'Speech (言) of myself (吾) = LANGUAGE.'),
    '国': ('囗', 'enclosure',                  ['囗', '玉'],   'A jewel (玉) inside borders (囗) = COUNTRY.'),
    '会': ('人', 'person',                     ['人', '云'],   'People (人) gathering in clouds (云) = MEET.'),
    '社': ('礻', 'altar',                      ['礻', '土'],   'Altar (礻) on the earth (土) where people gather = COMPANY / shrine.'),
    '員': ('口', 'mouth',                      ['口', '貝'],   'Mouth (口) over shell-money (貝) — a paid speaker = MEMBER / employee.'),
    # === Size / position ===
    '大': ('大', 'big (radical 37)',           ['大'],         'A person with arms stretched wide = BIG.'),
    '中': ('丨', 'line',                       ['口', '丨'],   'A line through the middle of a box = MIDDLE.'),
    '小': ('小', 'small (radical 42)',         ['小'],         'Three small specks scattered = SMALL.'),
    '上': ('一', 'one',                        ['上'],         'A mark above the baseline = UP.'),
    '下': ('一', 'one',                        ['下'],         'A mark below the baseline = DOWN.'),
    '左': ('工', 'work',                       ['ナ', '工'],   'A hand (ナ) holding a tool (工) — natural left-hand grip = LEFT.'),
    '右': ('口', 'mouth',                      ['ナ', '口'],   'A hand (ナ) over a mouth (口) — natural right-hand bite = RIGHT.'),
    '前': ('刂', 'knife (right)',              ['丷', '一', '月', '刂'], 'In FRONT, knife (刂) ready, sharing meat (月) with a smile (丷一).'),
    '後': ('彳', 'going man',                  ['彳', '幺', '夂'], 'A traveler (彳) trailing behind = AFTER.'),
    '外': ('夕', 'evening',                    ['夕', '卜'],   'Evening (夕) divination (卜) — done OUTSIDE the home.'),
    # === Compass directions ===
    '東': ('木', 'tree',                       ['木', '日'],   'Sun (日) rising behind a tree (木) = EAST.'),
    '西': ('襾', 'cover',                      ['西'],         'A bird returning to its nest at sunset = WEST.'),
    '南': ('十', 'ten',                        ['南'],         'A bell-shape facing the warm sun direction = SOUTH.'),
    '北': ('匕', 'spoon',                      ['北'],         'Two figures back-to-back facing away from the cold = NORTH.'),
    '間': ('門', 'gate',                       ['門', '日'],   'Sun (日) shining through a gate (門) = INTERVAL / between.'),
    # === Nature ===
    '山': ('山', 'mountain (radical 46)',      ['山'],         'Three peaks of a MOUNTAIN range.'),
    '川': ('川', 'river (radical 47)',         ['川'],         'Three flowing lines of a RIVER.'),
    '田': ('田', 'rice paddy (radical 102)',   ['田'],         'A grid of irrigation channels = RICE PADDY.'),
    '雨': ('雨', 'rain (radical 173)',         ['雨'],         'Drops falling from a cloud-shaped roof = RAIN.'),
    '天': ('大', 'big',                        ['一', '大'],   'The biggest thing (大) under the line (一) = HEAVEN / sky.'),
    '気': ('气', 'steam',                      ['气', '〆'],   'Steam (气) rising = SPIRIT / mood / air.'),
    '花': ('艹', 'grass',                      ['艹', '化'],   'Grass (艹) transforming (化) = FLOWER.'),
    '空': ('穴', 'cave',                       ['穴', '工'],   'A cave (穴) of work (工) — empty above = SKY / empty.'),
    '電': ('雨', 'rain',                       ['雨', '田'],   'Rain (雨) hitting a paddy (田) — lightning = ELECTRICITY.'),
    # === Travel + transport ===
    '車': ('車', 'vehicle (radical 159)',      ['車'],         'A wheel with axle and bed = VEHICLE / car.'),
    '道': ('辶', 'walk',                       ['辶', '首'],   'Walking (辶) with one\'s head (首) up = ROAD / way.'),
    '店': ('广', 'roof',                       ['广', '占'],   'Under a roof (广), claim a spot (占) = SHOP.'),
    '駅': ('馬', 'horse',                      ['馬', '尺'],   'Horse (馬) measured (尺) — a relay STATION.'),
    # === Eating + sensing ===
    '食': ('食', 'eat (radical 184)',          ['食'],         'A roof over good things to eat = EAT.'),
    '飲': ('食', 'eat',                        ['飠', '欠'],   'Food (飠) and a yawn (欠) — DRINK to wash it down.'),
    '見': ('見', 'see (radical 147)',          ['目', '儿'],   'Eye (目) on legs (儿) — looking around = SEE.'),
    '聞': ('門', 'gate',                       ['門', '耳'],   'Ear (耳) at the gate (門) = HEAR.'),
    '読': ('言', 'speech',                     ['言', '売'],   'Speech (言) selling (売) ideas = READ.'),
    '書': ('日', 'sun',                        ['書'],         'A brush over a writing surface in daylight = WRITE / book.'),
    '話': ('言', 'speech',                     ['言', '舌'],   'Speech (言) using the tongue (舌) = TALK / story.'),
    # === Motion ===
    '来': ('木', 'tree',                       ['一', '米'],   'Like a tree growing toward you = COME.'),
    '行': ('行', 'go (radical 144)',           ['彳', '亍'],   'Two walking-man halves = GO.'),
    '出': ('凵', 'open box',                   ['出'],         'Stacked containers — sticking OUT.'),
    '入': ('入', 'enter (radical 11)',         ['入'],         'Two strokes meeting at a point — going INSIDE = ENTER.'),
    '立': ('立', 'stand (radical 117)',        ['立'],         'A person planted on the ground = STAND.'),
    '休': ('亻', 'person (left)',              ['亻', '木'],   'A person (亻) leaning on a tree (木) = REST.'),
    '言': ('言', 'speech (radical 149)',       ['言'],         'Words (言) leaving the mouth = SAY.'),
    '買': ('貝', 'shell/money',                ['四', '貝'],   'Net (四) for shell-money (貝) = BUY.'),
    # === Adjectives ===
    '高': ('高', 'tall (radical 189)',         ['高'],         'A tall pavilion silhouette = TALL / expensive.'),
    '安': ('宀', 'roof',                       ['宀', '女'],   'A woman (女) under a roof (宀) — peaceful and CHEAP.'),
    '新': ('斤', 'axe',                        ['立', '木', '斤'], 'A standing tree freshly cut by an axe = NEW.'),
    '古': ('口', 'mouth',                      ['十', '口'],   'Ten (十) generations of stories (口) = OLD.'),
    '長': ('長', 'long (radical 168)',         ['長'],         'Long flowing hair on an elder = LONG.'),
    '白': ('白', 'white (radical 106)',        ['丿', '日'],   'A ray (丿) shining on the sun (日) = WHITE.'),
    # === Misc ===
    '名': ('口', 'mouth',                      ['夕', '口'],   'In the evening (夕), call out (口) the NAME.'),
    '番': ('田', 'rice paddy',                 ['釆', '田'],   'A claw (釆) ordering rice paddies (田) by NUMBER.'),
    '号': ('口', 'mouth',                      ['口', '丂'],   'Mouth (口) shouting a NUMBER / call sign.'),
    '私': ('禾', 'grain',                      ['禾', '厶'],   'My (厶) grain (禾) = PRIVATE / I.'),
}


def main() -> int:
    data = json.loads(KF.read_text(encoding='utf-8'))
    n_radical = 0
    n_decomp = 0
    n_mnemonic = 0
    matched = set()
    unmatched_existing = []

    for e in data.get('entries', []):
        glyph = e.get('glyph')
        if glyph not in KANJI_DEPTH:
            unmatched_existing.append(glyph)
            continue
        radical_glyph, radical_name, components, mnemonic = KANJI_DEPTH[glyph]
        new_radical = {'glyph': radical_glyph, 'name': radical_name}
        if e.get('radical') != new_radical:
            e['radical'] = new_radical
            n_radical += 1
        if e.get('radical_decomposition') != components:
            e['radical_decomposition'] = components
            n_decomp += 1
        if e.get('mnemonic') != mnemonic:
            e['mnemonic'] = mnemonic
            n_mnemonic += 1
        matched.add(glyph)

    KF.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    total = len(data.get('entries', []))
    nr = sum(1 for e in data['entries'] if e.get('radical'))
    nd = sum(1 for e in data['entries'] if e.get('radical_decomposition'))
    nm = sum(1 for e in data['entries'] if e.get('mnemonic'))
    print(f'[ISSUE-064 + IMP-082] Kanji depth fields')
    print(f'  Kanji matched:      {len(matched)} of {len(KANJI_DEPTH)} planned')
    print(f'  radical writes:        {n_radical} (now {nr}/{total})')
    print(f'  decomposition writes:  {n_decomp} (now {nd}/{total})')
    print(f'  mnemonic writes:       {n_mnemonic} (now {nm}/{total})')
    if unmatched_existing:
        print(f'  Catalog kanji not in plan: {unmatched_existing[:10]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
