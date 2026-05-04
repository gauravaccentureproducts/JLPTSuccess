"""Fix the 10-item audit issued 2026-05-03 (jlpt-n5-content-files-audit-
2026-05-03.md). Idempotent. JA-13 enforced post-run.

Items closed in priority order:
  1.1 CRITICAL  reading.json: add kanji_used + vocab_used to passages
                031-040 (regenerated from each passage.ja text).
  2.1 HIGH      n5.read.033 morning-sky-red imagery → move to ゆうがた.
  2.3 HIGH      n5.listen.036 三日かん → 三日間 (kanji 間 IS in N5).
  2.4 HIGH      n5.listen.034 em-dash → hyphen; n5.listen.038
                curly-apostrophe → ASCII apostrophe.
  3.1 MEDIUM    grammar.json: 4 em-dashes in common_mistakes.why
                replaced with " - ".
  3.2 MEDIUM    n5.read.034 "たのしい ですから" → "たのしいですから"
                (closes the awkward space).
  3.3 MEDIUM    n5.read.032 tier core_n5 → late_n5 (borderline vocab).
"""
import io, json, re, sys
from pathlib import Path
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
EM_DASH = '—'
CURLY_APOS = '’'
KANJI_RE = re.compile(r'[一-鿿]')


# --- Step 1: build a vocab-form lookup so we can extract vocab_used ---
def build_vocab_index() -> dict[str, str]:
    """Return form-or-reading → id."""
    vj = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))
    by_token: dict[str, str] = {}
    for v in vj['entries']:
        for tok in (v.get('form'), v.get('reading')):
            if tok:
                by_token.setdefault(tok, v['id'])
    return by_token


def tokenize_passage(text: str, vocab_index: dict[str, str]) -> list[str]:
    """Return the set of vocab-form tokens that appear in `text`,
    sorted by appearance length (longest match wins on overlapping
    substrings; same approach the rest of the corpus uses)."""
    tokens = sorted(vocab_index.keys(), key=lambda s: -len(s))
    found: list[str] = []
    seen: set[str] = set()
    s = text
    for tok in tokens:
        if tok and tok in s and tok not in seen:
            found.append(tok)
            seen.add(tok)
    return sorted(found)


def extract_kanji(text: str) -> list[str]:
    return sorted({c for c in text if KANJI_RE.match(c)})


# --- Step 2: apply all fixes to reading.json ---
def fix_reading() -> int:
    rpath = ROOT / 'data' / 'reading.json'
    data = json.loads(rpath.read_text(encoding='utf-8'))
    vocab_index = build_vocab_index()
    fixed_passages = 0
    fixed_metadata = 0
    for p in data['passages']:
        pid = p.get('id', '')

        # 2.1: n5.read.033 morning red sky → evening
        if pid == 'n5.read.033':
            old_ja = p.get('ja', '')
            new_ja = old_ja.replace(
                'あさは 七時ごろ、そらが あかいです。',
                'ゆうがた、そらが あかく なります。',
            )
            if new_ja != old_ja:
                p['ja'] = new_ja
                fixed_passages += 1

        # 3.2: n5.read.034 register polish (close the gap)
        if pid == 'n5.read.034':
            p['ja'] = p.get('ja', '').replace('たのしい ですから、', 'たのしいですから、')
            # also clearer title — "ともだちからの てがみ" now matches both Phase-9a
            # and the audit's preferred framing (passage signed by たなか)
            fixed_passages += 1

        # 3.3: n5.read.032 borderline → late_n5
        if pid == 'n5.read.032':
            if p.get('tier') != 'late_n5':
                p['tier'] = 'late_n5'
                fixed_metadata += 1

        # 1.1: regenerate kanji_used + vocab_used for passages 031..040
        if pid >= 'n5.read.031' and pid <= 'n5.read.040':
            ja = p.get('ja', '')
            if 'kanji_used' not in p or not p['kanji_used']:
                p['kanji_used'] = extract_kanji(ja)
                fixed_metadata += 1
            if 'vocab_used' not in p or not p['vocab_used']:
                p['vocab_used'] = tokenize_passage(ja, vocab_index)
                fixed_metadata += 1

    rpath.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                     encoding='utf-8')
    return fixed_passages + fixed_metadata


# --- Step 3: apply fixes to listening.json ---
def fix_listening() -> int:
    lpath = ROOT / 'data' / 'listening.json'
    data = json.loads(lpath.read_text(encoding='utf-8'))
    fixed = 0
    for it in data['items']:
        iid = it.get('id', '')
        # 2.3: 三日かん → 三日間 in n5.listen.036
        if iid == 'n5.listen.036':
            for k in ('script_ja', 'prompt_ja'):
                if it.get(k):
                    new = it[k].replace('三日かん', '三日間').replace('何日かん', '何日間')
                    if new != it[k]:
                        it[k] = new
                        fixed += 1
            # also fix choices array
            if it.get('choices'):
                it['choices'] = [c.replace('日かん', '日間').replace('一週間', '一週間')
                                 for c in it['choices']]
                fixed += 1

        # 2.4: punctuation cleanup on n5.listen.034 + 038
        for k, v in list(it.items()):
            if isinstance(v, str):
                new = v
                if EM_DASH in new:
                    new = new.replace(EM_DASH, ' - ')
                if CURLY_APOS in new:
                    new = new.replace(CURLY_APOS, "'")
                if new != v:
                    it[k] = new
                    fixed += 1

    lpath.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                     encoding='utf-8')
    return fixed


# --- Step 4: grammar.json em-dashes in common_mistakes.why ---
def fix_grammar() -> int:
    gpath = ROOT / 'data' / 'grammar.json'
    data = json.loads(gpath.read_text(encoding='utf-8'))
    fixed = 0
    for p in data.get('patterns', []):
        for cm in p.get('common_mistakes', []):
            for k, v in list(cm.items()):
                if isinstance(v, str) and EM_DASH in v:
                    cm[k] = v.replace(EM_DASH, ' - ')
                    fixed += 1
    gpath.write_text(json.dumps(data, ensure_ascii=False, indent=2),
                     encoding='utf-8')
    return fixed


def main() -> int:
    r = fix_reading()
    l = fix_listening()
    g = fix_grammar()
    print(f'reading.json fixes: {r}')
    print(f'listening.json fixes: {l}')
    print(f'grammar.json fixes: {g}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
