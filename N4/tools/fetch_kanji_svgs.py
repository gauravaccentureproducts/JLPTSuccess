"""Fetch stroke-order SVGs for all 249 N4 kanji.

Strategy:
1. Copy 106 N5 prerequisite SVGs from <JLPT-root>/N5/svg/kanji/ verbatim.
2. Fetch the remaining 143 N4-new SVGs from KanjiVG (GitHub raw).

KanjiVG license: CC BY-SA 3.0 (Ulrich Apel, et al). Attribution noted in NOTICES.md.

KanjiVG URL pattern: github.com/KanjiVG/kanjivg/raw/master/kanji/{codepoint}.svg
where codepoint is the lowercase hex Unicode code point (e.g., 4e00 for 一,
zero-padded to 5 digits for some files).

Idempotent: skips files that already exist.
"""
import io, json, sys, shutil, urllib.request, urllib.error
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
N5 = ROOT.parent / 'N5'
N5_SVG_DIR = N5 / 'svg' / 'kanji'
N4_SVG_DIR = ROOT / 'svg' / 'kanji'
N4_SVG_DIR.mkdir(parents=True, exist_ok=True)

# Load full whitelist
whitelist = json.loads((ROOT / 'data' / 'n4_kanji_whitelist.json').read_text(encoding='utf-8'))
n5_whitelist = set(json.loads((N5 / 'data' / 'n5_kanji_whitelist.json').read_text(encoding='utf-8')))

print(f'Total N4 whitelist: {len(whitelist)} kanji')
print(f'  - N5 prerequisite: {sum(1 for g in whitelist if g in n5_whitelist)}')
print(f'  - N4 new:          {sum(1 for g in whitelist if g not in n5_whitelist)}')

KANJIVG_BASE = 'https://raw.githubusercontent.com/KanjiVG/kanjivg/master/kanji'

def codepoint_filename(glyph):
    """Convert glyph to KanjiVG filename. KanjiVG uses 5-digit lowercase hex."""
    cp = ord(glyph)
    return f'{cp:05x}.svg'

# Step 1: Copy N5 prerequisite SVGs
copied = 0
n5_missing = []
for g in whitelist:
    if g not in n5_whitelist:
        continue
    target = N4_SVG_DIR / f'{g}.svg'
    if target.exists():
        continue
    src = N5_SVG_DIR / f'{g}.svg'
    if src.exists():
        shutil.copy2(src, target)
        copied += 1
    else:
        n5_missing.append(g)

print(f'\n[1] Copied {copied} N5-prerequisite SVGs from N5 repo.')
if n5_missing:
    print(f'    {len(n5_missing)} N5 prerequisite SVGs missing from source: {"".join(n5_missing)}')

# Step 2: Fetch N4-new SVGs from KanjiVG
fetched = 0
fetch_fails = []
n4_only = [g for g in whitelist if g not in n5_whitelist]
print(f'\n[2] Fetching {len(n4_only)} N4-new SVGs from KanjiVG...')

for i, g in enumerate(n4_only):
    target = N4_SVG_DIR / f'{g}.svg'
    if target.exists():
        continue
    url = f'{KANJIVG_BASE}/{codepoint_filename(g)}'
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (build-agent)'})
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = resp.read()
        target.write_bytes(data)
        fetched += 1
        if (i + 1) % 25 == 0:
            print(f'    {i + 1}/{len(n4_only)} fetched...')
    except urllib.error.HTTPError as e:
        fetch_fails.append((g, f'HTTP {e.code}'))
    except urllib.error.URLError as e:
        fetch_fails.append((g, f'URL error: {e.reason}'))
    except Exception as e:
        fetch_fails.append((g, f'{type(e).__name__}: {e}'))

print(f'\n[3] Fetched {fetched} N4-new SVGs.')
if fetch_fails:
    print(f'    {len(fetch_fails)} failures:')
    for g, err in fetch_fails[:10]:
        print(f'      {g} ({hex(ord(g))}): {err}')

# Final report
present = sum(1 for g in whitelist if (N4_SVG_DIR / f'{g}.svg').exists())
missing = [g for g in whitelist if not (N4_SVG_DIR / f'{g}.svg').exists()]
print(f'\nFinal: {present}/{len(whitelist)} SVGs in svg/kanji/')
if missing:
    print(f'  Missing: {"".join(missing)}')
