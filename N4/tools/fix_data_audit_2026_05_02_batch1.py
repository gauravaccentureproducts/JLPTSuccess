"""Fix batch 1 from feedback/jlpt-n5-data-files-audit-2026-05-02.md.

Items addressed in this script:
  2.1  vocab.json - はんぶん form/reading swap
  2.2  grammar.json - 10 broken cross-refs to retired patterns
  2.3  grammar.json - n5-134 (ので) tier core_n5 → late_n5
  3.2  kanji.json   - dedupe duplicate (form, reading) examples in 10 entries
  3.3  grammar.json - 8 em/en-dashes → ASCII hyphens
  4.2  kanji.json   - add jukujikun note to 大人 example in 大

Items NOT in this script (separate handling):
  1.1  vocab.json PoS mass-mistag — runs in fix_pos_thematic_sections.py
  2.4  132 vocab entries without examples — content authoring (Phase 6)
  3.1  Section 38 retention — kept as deliberate; doc-only, no data change
  4.1  32 stub patterns — explicitly "deliberate design choice" per audit

Idempotent: re-running is a no-op once fixes are in.
"""
import io, json, sys, re
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent

# ============================================================
# 2.1 はんぶん form/reading swap
# ============================================================
def fix_2_1_hambun(vocab):
    fixed = 0
    for e in vocab['entries']:
        if e.get('id', '').endswith('はんぶん') and \
           e.get('form') == 'はんぶん' and e.get('reading') == '半分':
            e['form'] = '半分'
            e['reading'] = 'はんぶん'
            fixed += 1
    return fixed

# ============================================================
# 2.2 grammar.json broken cross-refs to retired patterns
# Mapping decisions:
#   - n5-012 (retired formal-か question) → no canonical replacement;
#     n5-023 IS the current canonical for sentence-final か.
#     Fix: remove the broken contrast (it self-referenced via the
#     "duplicate entry" stale note) and remove the broken `see_also`
#     conjugation entry.
#   - n5-128 (retired Sentence+から、Sentence) → n5-009 is the canonical
#     for から (because/from). Repoint contrasts and form_rule labels.
# ============================================================
RETIRED = {'n5-012', 'n5-128'}  # Currently flagged in audit
RETIRED_TO_CANONICAL = {
    'n5-128': 'n5-009',   # から (because) → canonical n5-009
    # n5-012 has no canonical (n5-023 absorbed its content); references
    # are removed rather than repointed.
}

def fix_2_2_broken_refs(grammar):
    patterns = grammar['patterns']
    fixed_contrasts = 0
    fixed_form_rules = 0
    removed_contrasts = 0

    for p in patterns:
        # Fix contrasts.with_pattern_id pointing to retired
        new_contrasts = []
        for c in p.get('contrasts', []):
            target = c.get('with_pattern_id')
            if target in RETIRED_TO_CANONICAL:
                # Repoint to canonical
                c['with_pattern_id'] = RETIRED_TO_CANONICAL[target]
                # Update note text if it mentions the retired ID literally
                if 'note' in c and target in c['note']:
                    c['note'] = c['note'].replace(target, RETIRED_TO_CANONICAL[target])
                new_contrasts.append(c)
                fixed_contrasts += 1
            elif target == 'n5-012':
                # Remove the contrast entirely (canonical is the pattern itself,
                # so the contrast was a stale stub annotation).
                removed_contrasts += 1
                continue
            else:
                new_contrasts.append(c)
        if new_contrasts != p.get('contrasts', []):
            p['contrasts'] = new_contrasts

        # Fix form_rules.conjugations entries with see_also to retired
        fr = p.get('form_rules', {})
        if isinstance(fr, dict) and 'conjugations' in fr:
            new_conj = []
            for cv in fr['conjugations']:
                if not isinstance(cv, dict):
                    new_conj.append(cv); continue
                label = cv.get('label', '')
                form = cv.get('form', '')
                # Detect "See n5-XXX" pattern with retired target
                m = re.search(r'\b(n5-\d{3})\b', label)
                if form == 'see_also' and m:
                    target = m.group(1)
                    if target in RETIRED_TO_CANONICAL:
                        cv['label'] = label.replace(target, RETIRED_TO_CANONICAL[target])
                        new_conj.append(cv)
                        fixed_form_rules += 1
                        continue
                    elif target == 'n5-012':
                        # n5-023, n5-024, n5-031 are themselves the canonical;
                        # remove the broken see_also entry.
                        fixed_form_rules += 1
                        continue
                new_conj.append(cv)
            fr['conjugations'] = new_conj

    return fixed_contrasts, removed_contrasts, fixed_form_rules

# ============================================================
# 2.3 n5-134 tier core_n5 → late_n5
# ============================================================
def fix_2_3_n5_134_tier(grammar):
    for p in grammar['patterns']:
        if p['id'] == 'n5-134' and p.get('tier') == 'core_n5':
            p['tier'] = 'late_n5'
            return 1
    return 0

# ============================================================
# 3.2 kanji.json: dedupe duplicate (form, reading) examples
# Strategy: keep the example whose gloss does NOT contain "(also in §"
# (the cross-listing annotation); fall back to first occurrence.
# ============================================================
def fix_3_2_kanji_dedupe(kanji):
    fixed = 0
    for ke in kanji['entries']:
        examples = ke.get('examples', [])
        seen = {}
        order = []
        for ex in examples:
            key = (ex.get('form'), ex.get('reading'))
            if key in seen:
                # Pick the cleaner gloss
                existing = seen[key]
                ex_gloss = (ex.get('gloss') or '')
                ex_clean = '(also in §' not in ex_gloss
                ext_clean = '(also in §' not in (existing.get('gloss') or '')
                # Prefer the longer non-annotated gloss (more informative),
                # else any non-annotated, else first.
                if ex_clean and not ext_clean:
                    seen[key] = ex
                elif ex_clean and ext_clean and len(ex_gloss) > len(existing.get('gloss') or ''):
                    seen[key] = ex
                # else keep existing
                fixed += 1
            else:
                seen[key] = ex
                order.append(key)
        if len(seen) != len(examples):
            ke['examples'] = [seen[k] for k in order]
    return fixed

# ============================================================
# 3.3 grammar.json: replace em/en-dashes with ASCII hyphens
# Em-dash (U+2014): typically use " - " (hyphen with surrounding space)
# En-dash (U+2013): typically use "-" (range hyphen, no surrounding space change)
# ============================================================
def fix_3_3_dashes(grammar):
    em = '—'
    en = '–'
    em_count = 0
    en_count = 0

    def fix_str(s):
        nonlocal em_count, en_count
        if not isinstance(s, str): return s
        em_count += s.count(em)
        en_count += s.count(en)
        # Em-dash: " — " → " - " (preserve spacing); standalone em → "-"
        s = s.replace(' — ', ' - ').replace('—', '-')
        # En-dash: standalone en → "-" (range marker)
        s = s.replace('–', '-')
        return s

    def walk(o):
        if isinstance(o, dict):
            for k, v in list(o.items()):
                if isinstance(v, str):
                    o[k] = fix_str(v)
                else:
                    walk(v)
        elif isinstance(o, list):
            for i, v in enumerate(o):
                if isinstance(v, str):
                    o[i] = fix_str(v)
                else:
                    walk(v)

    walk(grammar)
    return em_count, en_count

# ============================================================
# 4.2 kanji.json: add jukujikun note to 大人 example in 大
# ============================================================
def fix_4_2_jukujikun(kanji):
    for ke in kanji['entries']:
        if ke.get('glyph') == '大':
            for ex in ke.get('examples', []):
                if ex.get('form') == '大人' and ex.get('reading') == 'おとな' \
                   and 'note' not in ex:
                    ex['note'] = ('Irregular jukujikun reading: 大 here is '
                                  'not pronounced as either おお, だい, or たい.')
                    return 1
    return 0

# ============================================================
# Main
# ============================================================
def main():
    vocab_path = ROOT / 'data' / 'vocab.json'
    grammar_path = ROOT / 'data' / 'grammar.json'
    kanji_path = ROOT / 'data' / 'kanji.json'

    vocab = json.loads(vocab_path.read_text(encoding='utf-8'))
    grammar = json.loads(grammar_path.read_text(encoding='utf-8'))
    kanji = json.loads(kanji_path.read_text(encoding='utf-8'))

    n_2_1 = fix_2_1_hambun(vocab)
    n_2_2c, n_2_2r, n_2_2f = fix_2_2_broken_refs(grammar)
    n_2_3 = fix_2_3_n5_134_tier(grammar)
    n_3_2 = fix_3_2_kanji_dedupe(kanji)
    n_3_3em, n_3_3en = fix_3_3_dashes(grammar)
    n_4_2 = fix_4_2_jukujikun(kanji)

    # Write back
    vocab_path.write_text(
        json.dumps(vocab, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8')
    grammar_path.write_text(
        json.dumps(grammar, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8')
    kanji_path.write_text(
        json.dumps(kanji, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8')

    print('=== Fix batch 1 results ===')
    print(f'  2.1 はんぶん form/reading swap:    {n_2_1} entries fixed')
    print(f'  2.2 broken cross-refs:')
    print(f'        contrasts repointed:        {n_2_2c}')
    print(f'        contrasts removed (n5-012): {n_2_2r}')
    print(f'        form_rules see_also fixed:  {n_2_2f}')
    print(f'  2.3 n5-134 tier core_n5→late_n5:  {n_2_3} pattern fixed')
    print(f'  3.2 kanji duplicate examples:     {n_3_2} duplicates removed')
    print(f'  3.3 grammar.json dashes:          {n_3_3em} em + {n_3_3en} en replaced')
    print(f'  4.2 大人 jukujikun note added:    {n_4_2} example annotated')

if __name__ == '__main__':
    main()
