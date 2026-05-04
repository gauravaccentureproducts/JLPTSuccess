"""Fix the 9-item infrastructure audit (2026-05-03).

Items 1.1, 2.1, 2.4, 3.1, 3.2, 3.3 covered here. 2.2 + 2.3 handled by
re-running tools/build_audio.py (manifest auto-refreshes) and a small
_meta refresh respectively. 4.1 (storage-waste low-priority) noted but
not actively fixed.

Idempotent. JA-13 enforced post-run.
"""
import io, json, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
EM_DASH = '—'


# ---------- 1.1 + 3.2 + 3.3: kanji-readings + kanji.json sync ----------
def fix_kanji_readings_and_kanji_json() -> int:
    """1.1: fix 3 wrong primaries (語→ご, 天→てん, 入→はい) and 1
    debatable (間→かん per audit recommendation).

    3.2: sync 入 kun list ordering between n5_kanji_readings.json and
    kanji.json so both surface the same default reading.

    3.3: propagate `primary` from n5_kanji_readings.json into
    kanji.json's `primary_reading` field for all 106 entries so the
    two files are now non-conflicting sources of truth.
    """
    rpath = ROOT / 'data' / 'n5_kanji_readings.json'
    kpath = ROOT / 'data' / 'kanji.json'
    # n5_kanji_readings.json shape: { "<glyph>": {on, kun, primary}, ... }
    readings = json.loads(rpath.read_text(encoding='utf-8'))
    kanji = json.loads(kpath.read_text(encoding='utf-8'))

    changed = 0
    # 1.1 — fix the 4 wrong/debatable primaries in n5_kanji_readings.json
    PRIMARY_FIXES = {
        '語': 'ご',     # was かた (literary)
        '天': 'てん',   # was あめ (rare for 天-alone)
        '入': 'はい',   # was い (compound stem; 入る = はいる)
        '間': 'かん',   # was あいだ (compounds dominate at N5)
    }
    for glyph, fix in PRIMARY_FIXES.items():
        entry = readings.get(glyph)
        if entry is None:
            continue
        if entry.get('primary') != fix:
            entry['primary'] = fix
            changed += 1
    rpath.write_text(json.dumps(readings, ensure_ascii=False, indent=2),
                     encoding='utf-8')

    # 3.2 + 3.3 — for each kanji.json entry, sync kun-list ordering with
    # the readings file AND propagate primary_reading.
    for k in kanji.get('entries', []):
        glyph = k.get('glyph')
        ref = readings.get(glyph)
        if ref is None:
            continue
        # 3.3: propagate primary_reading
        ref_primary = ref.get('primary')
        if ref_primary and k.get('primary_reading') != ref_primary:
            k['primary_reading'] = ref_primary
            changed += 1
        # 3.2: sync kun list ordering. Only reorder if both have the
        # same set; otherwise leave alone (data divergence beyond order).
        ref_kun = list(ref.get('kun') or [])
        cur_kun = list(k.get('kun') or [])
        if ref_kun and cur_kun and set(ref_kun) == set(cur_kun) and ref_kun != cur_kun:
            k['kun'] = ref_kun
            changed += 1
    kpath.write_text(json.dumps(kanji, ensure_ascii=False, indent=2),
                     encoding='utf-8')
    return changed


# ---------- 2.1: forward-slash all audio_manifest paths ----------
def fix_audio_manifest_paths() -> int:
    mpath = ROOT / 'data' / 'audio_manifest.json'
    data = json.loads(mpath.read_text(encoding='utf-8'))
    changed = 0
    items = data['items'] if isinstance(data, dict) and 'items' in data else data
    for it in items:
        for k in ('path', 'audio'):
            v = it.get(k)
            if isinstance(v, str) and '\\' in v:
                it[k] = v.replace('\\', '/')
                changed += 1
    mpath.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                     encoding='utf-8')
    return changed


# ---------- 2.4: sweep em-dashes in questions.json ----------
def fix_questions_em_dashes() -> int:
    qpath = ROOT / 'data' / 'questions.json'
    data = json.loads(qpath.read_text(encoding='utf-8'))
    changed = 0

    def fix_str(s: str) -> str:
        nonlocal changed
        if EM_DASH in s:
            new = s.replace(EM_DASH, ' - ')
            # Collapse "  - " (the em-dash usually had spaces around it)
            new = new.replace('  - ', ' - ').replace('  - ', ' - ')
            changed += s.count(EM_DASH)
            return new
        return s

    def walk(o):
        if isinstance(o, str):
            return fix_str(o)
        if isinstance(o, dict):
            return {k: walk(v) for k, v in o.items()}
        if isinstance(o, list):
            return [walk(x) for x in o]
        return o

    data = walk(data)
    qpath.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                     encoding='utf-8')
    return changed


# ---------- 2.3: refresh _meta in questions.json ----------
def fix_questions_meta() -> int:
    qpath = ROOT / 'data' / 'questions.json'
    data = json.loads(qpath.read_text(encoding='utf-8'))
    qs = data.get('questions', [])
    type_dist = {}
    for q in qs:
        t = q.get('type', 'mcq')
        type_dist[t] = type_dist.get(t, 0) + 1
    ids = sorted(q.get('id', '') for q in qs)
    meta = data.get('_meta', {})
    changed = 0
    if meta.get('question_count') != len(qs):
        meta['question_count'] = len(qs)
        changed += 1
    if meta.get('type_distribution') != type_dist:
        meta['type_distribution'] = type_dist
        changed += 1
    new_range = {'first': ids[0] if ids else '?', 'last': ids[-1] if ids else '?'}
    if meta.get('id_range') != new_range:
        meta['id_range'] = new_range
        changed += 1
    # Append history entry if not already there
    history = meta.get('audit_history') or meta.get('history') or []
    if isinstance(history, list):
        note = (
            'Pass-15+ coverage extension (2026-05-03): authored 75 mcq '
            '(q-0504..0578) bringing grammar-pattern coverage to 100% '
            '(177/177). Bank: 213 -> 288 (mcq 193 -> 258, sentence_order '
            '16, text_input 14).'
        )
        if not any('Pass-15+ coverage extension' in (h or '') for h in history):
            history.append(note)
            if 'audit_history' in meta:
                meta['audit_history'] = history
            else:
                meta['history'] = history
            changed += 1
    data['_meta'] = meta
    qpath.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                     encoding='utf-8')
    return changed


# ---------- 3.1: add 半分 to n5_vocab_whitelist.json ----------
def fix_vocab_whitelist() -> int:
    wpath = ROOT / 'data' / 'n5_vocab_whitelist.json'
    data = json.loads(wpath.read_text(encoding='utf-8'))
    changed = 0
    if '半分' not in data:
        data.append('半分')
        data.sort()
        changed += 1
    # Keep はんぶん too (recognizable form for fuzzy matching)
    wpath.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                     encoding='utf-8')
    return changed


def main() -> int:
    a = fix_kanji_readings_and_kanji_json()
    b = fix_audio_manifest_paths()
    c = fix_questions_em_dashes()
    d = fix_questions_meta()
    e = fix_vocab_whitelist()
    print(f'kanji-readings + kanji.json sync: {a}')
    print(f'audio_manifest path normalization: {b}')
    print(f'questions.json em-dashes: {c}')
    print(f'questions.json _meta refresh: {d}')
    print(f'vocab whitelist + 半分: {e}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
