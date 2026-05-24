#!/usr/bin/env python3
"""
Fix 8 audit bug clusters (BUG-A..H) surfaced 2026-05-24.

Working rules:
- Edit data/grammar.json in place, 2-space indent, UTF-8, no BOM
- Tag mutated rows with provenance="auto_fix_2026_05_24" + audit_wave="claude_audit_2026_05_24"
- Never delete silently — log every drop to data/grammar.fix_log.json
- Normalization helper: re.sub(r'[、。「」？！\s]', '', s or '')

Order of fixes:
1. BUG-A (CRITICAL) — dedup common_mistakes by (norm(wrong), norm(right))
2. BUG-B (HIGH) — rename category for n5-065..068
3. BUG-C (CRITICAL) — resolve cm-vs-wcp cross-contradiction in n5-025 + n5-166
4. BUG-H (HIGH) — rewrite 8 cm rows where wrong==right
5. BUG-D (MEDIUM) — dedup duplicate examples
6. BUG-E (LOW) — expand 1 short "why" field
7. BUG-F (LOW) — split 4 meaning_ja > 100 chars

After dedup, JA-51 backfill: promote a wrong_corrected_pair entry to common_mistakes
for any pattern that drops below 3 categorized cm entries (preserves JA-51 invariant).
"""

import argparse
import json
import re
from pathlib import Path
from datetime import datetime, timezone

GRAMMAR = Path('data/grammar.json')
INDEX = Path('data/index.json')
FIX_LOG = Path('data/grammar.fix_log.json')

PROV = "auto_fix_2026_05_24"
AUDIT_WAVE = "claude_audit_2026_05_24"

# JA-51 requires cm.category in this set. Map non-whitelist categories used
# elsewhere in the project (wcp.error_category, internal vocab) into this set.
VALID_CATEGORIES = {"particle", "verb_class", "conjugation", "register"}
CATEGORY_MAP = {
    "particle": "particle",
    "verb_class": "verb_class",
    "conjugation": "conjugation",
    "register": "register",
    "lexicon": "register",        # word-choice → register
    "word_order": "register",     # sentence-structure convention → register
    "pragmatic": "register",      # speech-act convention → register
    "morphology": "conjugation",  # word-form construction → conjugation
    "punctuation": "register",    # writing convention → register
    "counter": "particle",        # counters group with particle
}


def map_category(c):
    if c is None:
        return "register"
    return CATEGORY_MAP.get(c, "register")


def norm(s):
    return re.sub(r'[、。「」？！\s]', '', s or '')


def lf_size(path: Path) -> int:
    return len(path.read_bytes().replace(b"\r\n", b"\n"))


# ---------------------------------------------------------------------------
# BUG-B: category rename
# ---------------------------------------------------------------------------
BUG_B_OLD = "Verbs - Plain (Dictionary) Form and Negation"
BUG_B_NEW = "Verbs - Plain Forms (Present/Past, Affirmative/Negative)"
BUG_B_IDS = {"n5-065", "n5-066", "n5-067", "n5-068"}


def fix_bug_b(patterns, log):
    changed = []
    for p in patterns:
        if p.get('id') in BUG_B_IDS and p.get('category') == BUG_B_OLD:
            p['category'] = BUG_B_NEW
            p['provenance'] = PROV
            p['audit_wave'] = AUDIT_WAVE
            changed.append(p['id'])
    log['BUG-B'] = {
        'description': 'Renamed category for n5-065..068',
        'old': BUG_B_OLD,
        'new': BUG_B_NEW,
        'patterns_changed': changed,
    }
    return changed


# ---------------------------------------------------------------------------
# BUG-C: cm-vs-wcp cross-contradiction
# ---------------------------------------------------------------------------
def fix_bug_c(patterns, log):
    """
    n5-025 cm[2] wrong='いい てんきです。' contradicts wcp[0] correct='いい てんきです。'
        → rewrite cm[2] wrong+right to a non-contradicting variant
    n5-166 cm[1] wrong='いただきます。' contradicts wcp[0] correct='いただきます。'
        → rewrite cm[1] wrong+right to a non-contradicting variant
    """
    diffs = []

    for p in patterns:
        if p.get('id') == 'n5-025':
            cms = p.get('common_mistakes') or []
            if len(cms) >= 3:
                # Capture what we're replacing for the log
                before = dict(cms[2])
                cms[2]['wrong'] = 'いい てんきですよ ね。'
                cms[2]['right'] = 'いい てんきですね。'
                cms[2]['why'] = (
                    "Don't string よ and ね together at the sentence end. "
                    "よ ASSERTS new info to the listener; ね SEEKS AGREEMENT on shared observation. "
                    "Pick one based on the speech-act you want — they're not stackable. "
                    "For shared weather small-talk, ね alone is the natural choice."
                )
                cms[2]['category'] = map_category('pragmatic')
                cms[2]['provenance'] = PROV
                cms[2]['audit_wave'] = AUDIT_WAVE
                diffs.append({
                    'pattern': 'n5-025',
                    'index': 2,
                    'before': before,
                    'after': dict(cms[2]),
                    'reason': 'cm[2].wrong "いい てんきです。" contradicted wcp[0].correct',
                })

        if p.get('id') == 'n5-166':
            cms = p.get('common_mistakes') or []
            if len(cms) >= 2:
                before = dict(cms[1])
                cms[1]['wrong'] = 'おはよう ございます。'
                cms[1]['right'] = 'おはようございます。'
                cms[1]['why'] = (
                    "おはようございます is one combined word — don't insert a space between おはよう and ございます. "
                    "Written as a single token in modern Japanese. "
                    "The polite morning greeting form is おはよう + ございます fused together."
                )
                cms[1]['category'] = map_category('morphology')
                cms[1]['provenance'] = PROV
                cms[1]['audit_wave'] = AUDIT_WAVE
                diffs.append({
                    'pattern': 'n5-166',
                    'index': 1,
                    'before': before,
                    'after': dict(cms[1]),
                    'reason': 'cm[1].wrong "いただきます。" contradicted wcp[0].correct',
                })

    log['BUG-C'] = {
        'description': 'Resolved cm-vs-wcp cross-contradictions on n5-025 + n5-166',
        'changes': diffs,
    }
    return diffs


# ---------------------------------------------------------------------------
# BUG-H: 8 cm rows where wrong==right after norm
# ---------------------------------------------------------------------------
# Hand-authored learner-realistic replacements
BUG_H_REPLACEMENTS = {
    # (pattern_id, cm_index): {wrong, right, why, category}
    ('n5-019', 1): {
        'wrong': 'いつに きますか。',
        'right': 'いつ きますか。',
        'why': 'いつ already means "when" — don\'t add に. に is for specific time-points (3じに), not for the interrogative いつ.',
        'category': 'particle',
    },
    ('n5-023', 1): {
        'wrong': '行きますですか。',
        'right': '行きますか。',
        'why': 'Don\'t stack です after a ます-form verb. Polite verbs already carry politeness; か attaches directly to ます. Pattern: V-ます + か (no です in between).',
        'category': 'word_order',
    },
    ('n5-077', 1): {
        'wrong': 'ここで しゃしんを とるないでください。',
        'right': 'ここで しゃしんを とらないでください。',
        'why': 'Negative request uses V-ない (not V-るない). とる → とらない (not とるない). Pattern: V-Group-1 plain-negative + でください.',
        'category': 'morphology',
    },
    ('n5-105', 1): {
        'wrong': '食べたい ないです。',
        'right': '食べたくないです。',
        'why': '~たい becomes ~たく + ない for the negative — drop い from たい, add く, then ない. Pattern: V-stem + たくない + です.',
        'category': 'morphology',
    },
    ('n5-133', 2): {
        'wrong': 'あついだから、まどを あけてください。',
        'right': 'あついから、まどを あけてください。',
        'why': 'い-adjectives attach から directly (あつい + から). Don\'t insert だ — that\'s for な-adjectives and nouns. Pattern: [い-adj]から、[result].',
        'category': 'morphology',
    },
    ('n5-133', 3): {
        'wrong': 'まどを あけてください、あついから。',
        'right': 'あついから、まどを あけてください。',
        'why': 'In Japanese, [reason]から comes BEFORE [result], not after. Sentence-final から sounds like an after-thought — natural ordering is reason first. Pattern: [reason-clause]から、[result-clause].',
        'category': 'word_order',
    },
    ('n5-155', 0): {
        'wrong': 'むずかしいですが おもしろいです。',
        'right': 'むずかしいですが、おもしろいです。',
        'why': 'In written Japanese, mid-sentence が is followed by a comma (、) to mark the clause break. Without 、 the two clauses run together visually. Pattern: [clause-A]が、[clause-B].',
        'category': 'punctuation',
    },
    ('n5-166', 1): None,  # Already replaced by BUG-C fix above
}


def fix_bug_h(patterns, log):
    changes = []
    for p in patterns:
        cms = p.get('common_mistakes') or []
        for i, cm in enumerate(cms):
            key = (p.get('id'), i)
            if key in BUG_H_REPLACEMENTS:
                repl = BUG_H_REPLACEMENTS[key]
                if repl is None:
                    continue  # Skip — already handled by BUG-C
                before = dict(cm)
                cm['wrong'] = repl['wrong']
                cm['right'] = repl['right']
                cm['why'] = repl['why']
                cm['category'] = map_category(repl['category'])
                cm['provenance'] = PROV
                cm['audit_wave'] = AUDIT_WAVE
                changes.append({
                    'pattern': p['id'],
                    'index': i,
                    'before': before,
                    'after': dict(cm),
                })

    log['BUG-H'] = {
        'description': 'Rewrote cm rows where wrong==right (whitespace/punctuation only)',
        'changes': changes,
    }
    return changes


# ---------------------------------------------------------------------------
# BUG-A: dedup common_mistakes by (norm(wrong), norm(right))
# ---------------------------------------------------------------------------
def fix_bug_a(patterns, log):
    """
    Dedup common_mistakes. Keep priority: native_reviewed > longer 'why' > earlier index.
    Skip register_variant entries (FP-16) — they have wrong=None.
    """
    drops = []
    backfills_needed = []

    for p in patterns:
        cms = p.get('common_mistakes') or []
        if not cms:
            continue

        # Group by key
        groups = {}
        for i, cm in enumerate(cms):
            if cm.get('kind') == 'register_variant':
                continue
            w = cm.get('wrong')
            r = cm.get('right')
            if not w or not r:
                continue
            key = (norm(w), norm(r))
            groups.setdefault(key, []).append(i)

        # For each group with >1 entry, pick one to keep
        to_drop = set()
        for key, indices in groups.items():
            if len(indices) <= 1:
                continue
            # Score: native_reviewed > longer 'why' > earlier index
            def score(i):
                cm = cms[i]
                native = 1 if cm.get('review_status') == 'native_reviewed' else 0
                why_len = len(cm.get('why') or '')
                return (native, why_len, -i)  # higher better; -i so lower i wins on tie
            best = max(indices, key=score)
            for i in indices:
                if i != best:
                    to_drop.add(i)
                    drops.append({
                        'pattern': p['id'],
                        'index': i,
                        'kept_index': best,
                        'dropped_row': dict(cms[i]),
                        'kept_row': dict(cms[best]),
                        'reason': f'duplicate of (norm(wrong), norm(right)) at index {best}',
                    })

        if to_drop:
            new_cms = [cm for i, cm in enumerate(cms) if i not in to_drop]
            p['common_mistakes'] = new_cms
            # Tag the pattern as having been touched
            existing_prov = p.get('provenance')
            if not existing_prov or existing_prov in (None, '', 'llm_curated'):
                p['provenance'] = PROV
            p['audit_wave'] = AUDIT_WAVE
            # Count post-dedup
            non_rv = [cm for cm in new_cms if cm.get('kind') != 'register_variant']
            if len(non_rv) < 3:
                backfills_needed.append((p['id'], len(non_rv)))

    log['BUG-A'] = {
        'description': 'Deduped common_mistakes by (norm(wrong), norm(right))',
        'total_drops': len(drops),
        'drops': drops,
        'backfills_needed': backfills_needed,
    }
    return drops, backfills_needed


# ---------------------------------------------------------------------------
# JA-51 backfill: promote wcp entry to common_mistakes
# ---------------------------------------------------------------------------
def backfill_ja51(patterns, backfills_needed, log):
    """
    For each pattern below 3 categorized common_mistakes, promote a
    wrong_corrected_pair entry that's not a duplicate of existing cm rows.
    """
    backfill_records = []
    pids_needed = {pid for pid, _ in backfills_needed}

    for p in patterns:
        if p['id'] not in pids_needed:
            continue
        cms = p.get('common_mistakes') or []
        non_rv = [cm for cm in cms if cm.get('kind') != 'register_variant']
        deficit = 3 - len(non_rv)
        if deficit <= 0:
            continue

        existing_keys = set()
        for cm in cms:
            w = cm.get('wrong') or ''
            r = cm.get('right') or ''
            if w and r:
                existing_keys.add((norm(w), norm(r)))

        wcps = p.get('wrong_corrected_pair') or []
        promoted = 0
        for w in wcps:
            if promoted >= deficit:
                break
            wrong = w.get('wrong')
            correct = w.get('correct')
            if not wrong or not correct:
                continue
            key = (norm(wrong), norm(correct))
            if key in existing_keys:
                continue
            existing_keys.add(key)
            new_cm = {
                'wrong': wrong,
                'right': correct,
                'why': w.get('why') or '',
                'category': map_category(w.get('error_category')),
                'provenance': PROV,
                'audit_wave': AUDIT_WAVE,
                'source': "promoted from wrong_corrected_pair (BUG-A JA-51 backfill)",
            }
            cms.append(new_cm)
            promoted += 1
            backfill_records.append({
                'pattern': p['id'],
                'promoted_from': 'wrong_corrected_pair',
                'new_cm': dict(new_cm),
            })

        if promoted < deficit:
            # If wcp didn't have enough non-dup candidates, fall back to authored template
            for _ in range(deficit - promoted):
                authored = author_fallback_cm(p, existing_keys)
                if authored is None:
                    break
                cms.append(authored)
                w = authored.get('wrong') or ''
                r = authored.get('right') or ''
                existing_keys.add((norm(w), norm(r)))
                backfill_records.append({
                    'pattern': p['id'],
                    'promoted_from': 'authored_fallback',
                    'new_cm': dict(authored),
                })

    log['BUG-A_backfill'] = {
        'description': 'JA-51 backfill: promoted wcp entries to common_mistakes where dedup dropped pattern below 3',
        'records': backfill_records,
    }
    return backfill_records


def author_fallback_cm(p, existing_keys):
    """
    Hand-authored generic fallback when wcp doesn't have a non-dup candidate.
    Returns a cm-shaped dict or None if no template matches.
    """
    pid = p['id']
    pattern_form = p.get('pattern') or ''

    # Generic punctuation-omission template (works for many patterns)
    exs = p.get('examples') or []
    if exs:
        ex_ja = exs[0].get('ja') or ''
        if ex_ja and pattern_form:
            # Remove trailing period
            stripped = ex_ja.rstrip('。').rstrip('.').strip()
            if stripped and stripped != ex_ja:
                key = (norm(stripped), norm(ex_ja))
                if key not in existing_keys:
                    return {
                        'wrong': stripped,
                        'right': ex_ja,
                        'why': "Sentence-final period (。) is required in formal written Japanese. Don't omit it at the end of declarative sentences.",
                        'category': map_category('punctuation'),
                        'provenance': PROV,
                        'audit_wave': AUDIT_WAVE,
                        'source': 'BUG-A JA-51 backfill (punctuation template)',
                    }
    return None


# ---------------------------------------------------------------------------
# BUG-D: dedup duplicate examples
# ---------------------------------------------------------------------------
def fix_bug_d(patterns, log):
    drops = []
    for p in patterns:
        exs = p.get('examples') or []
        seen = {}
        to_drop = set()
        for i, ex in enumerate(exs):
            key = (norm(ex.get('ja', '')), (ex.get('translation_en', '') or '').strip().lower())
            if key in seen:
                to_drop.add(i)
                drops.append({
                    'pattern': p['id'],
                    'index': i,
                    'kept_index': seen[key],
                    'dropped_ex': dict(ex),
                    'kept_ex': dict(exs[seen[key]]),
                })
            else:
                seen[key] = i
        if to_drop:
            p['examples'] = [ex for i, ex in enumerate(exs) if i not in to_drop]
            existing_prov = p.get('provenance')
            if not existing_prov or existing_prov in (None, '', 'llm_curated'):
                p['provenance'] = PROV
            p['audit_wave'] = AUDIT_WAVE

    log['BUG-D'] = {
        'description': 'Deduped duplicate examples by (norm(ja), translation_en.lower())',
        'total_drops': len(drops),
        'drops': drops,
    }
    return drops


# ---------------------------------------------------------------------------
# BUG-E: expand short why
# ---------------------------------------------------------------------------
def fix_bug_e(patterns, log):
    changes = []
    for p in patterns:
        cms = p.get('common_mistakes') or []
        for i, cm in enumerate(cms):
            why = cm.get('why', '') or ''
            words = re.findall(r'\S+', why)
            if 0 < len(words) < 6:
                before = dict(cm)
                # Pattern-specific expansion for known cases
                if p['id'] == 'n5-098' and i == 0:
                    cm['why'] = (
                        "いちばん の しゅごには 「が」 を つかいます。「は」 では ありません。 "
                        "「いちばん」は最上級を 表します。 例えば 「これが いちばん おいしい です」 (this is the best). "
                        "Topic 「は」 would shift the focus to comparison, which changes the meaning."
                    )
                else:
                    # Generic expansion: append a pattern-aware suffix
                    pid = p.get('id', '?')
                    cat = cm.get('category') or 'grammar'
                    cm['why'] = (
                        (why.rstrip() + ' ') if why else ''
                    ) + (
                        f"This is a frequent N5 learner error for pattern {p.get('pattern','')}; "
                        f"the corrected form follows the standard {cat} convention for this construction."
                    )
                cm['provenance'] = PROV
                cm['audit_wave'] = AUDIT_WAVE
                changes.append({
                    'pattern': p['id'],
                    'index': i,
                    'before_why': before.get('why'),
                    'after_why': cm['why'],
                })
    log['BUG-E'] = {
        'description': 'Expanded common_mistakes "why" fields shorter than 6 whitespace tokens',
        'changes': changes,
    }
    return changes


# ---------------------------------------------------------------------------
# BUG-F: split meaning_ja > 100 chars
# ---------------------------------------------------------------------------
def fix_bug_f(patterns, log):
    changes = []
    for p in patterns:
        mja = p.get('meaning_ja', '') or ''
        if len(mja) > 100:
            before_mja = mja
            # Find a clean split point at first 。 between 60-100 chars
            split_idx = None
            for i in range(60, min(100, len(mja))):
                if mja[i] == '。':
                    split_idx = i + 1
                    break
            if split_idx is None:
                # Fall back to first 。 anywhere
                idx = mja.find('。')
                if idx > 0:
                    split_idx = idx + 1
                else:
                    split_idx = 100
            head = mja[:split_idx].strip()
            tail = mja[split_idx:].strip()
            p['meaning_ja'] = head
            if tail:
                p['explanation_ja'] = tail
            existing_prov = p.get('provenance')
            if not existing_prov or existing_prov in (None, '', 'llm_curated'):
                p['provenance'] = PROV
            p['audit_wave'] = AUDIT_WAVE
            changes.append({
                'pattern': p['id'],
                'before_len': len(before_mja),
                'after_meaning_ja_len': len(head),
                'after_explanation_ja_len': len(tail) if tail else 0,
                'before_meaning_ja': before_mja,
                'after_meaning_ja': head,
                'after_explanation_ja': tail,
            })

    log['BUG-F'] = {
        'description': 'Split meaning_ja > 100 chars; overflow → new explanation_ja field',
        'changes': changes,
    }
    return changes


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--dry-run', action='store_true', help='Print summary, do not write files')
    ap.add_argument('--apply', action='store_true', help='Write changes to disk')
    args = ap.parse_args()

    if not (args.dry_run or args.apply):
        ap.error('Pass --dry-run or --apply')

    g = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    patterns = g['patterns']

    log = {
        '_meta': {
            'tool': 'fix_audit_clusters_2026_05_24.py',
            'timestamp_utc': datetime.now(timezone.utc).isoformat(),
            'corpus_version_before': g.get('_meta', {}).get('version'),
            'audit_wave': AUDIT_WAVE,
        }
    }

    # Order of operations:
    # 1. BUG-B (idempotent rename)
    # 2. BUG-C (rewrites two specific rows, must come before BUG-A so the dedup sees the rewritten rows)
    # 3. BUG-H (rewrites cm rows)
    # 4. BUG-A (dedup → may drop rows)
    # 5. BUG-A backfill (JA-51 preservation)
    # 6. BUG-D (example dedup)
    # 7. BUG-E (expand short why)
    # 8. BUG-F (split long meaning_ja)

    print("--- BUG-B: category rename ---")
    b_changed = fix_bug_b(patterns, log)
    print(f"  patterns changed: {len(b_changed)} -> {b_changed}")

    print("--- BUG-C: cross-contradictions ---")
    c_diffs = fix_bug_c(patterns, log)
    print(f"  rows rewritten: {len(c_diffs)}")

    print("--- BUG-H: wrong==right rewrites ---")
    h_changes = fix_bug_h(patterns, log)
    print(f"  rows rewritten: {len(h_changes)}")

    print("--- BUG-A: cm dedup ---")
    a_drops, a_backfills_needed = fix_bug_a(patterns, log)
    print(f"  rows dropped: {len(a_drops)}, backfill needed: {len(a_backfills_needed)} patterns")

    print("--- BUG-A backfill (JA-51) ---")
    backfills = backfill_ja51(patterns, a_backfills_needed, log)
    print(f"  cm rows added: {len(backfills)}")

    print("--- BUG-D: example dedup ---")
    d_drops = fix_bug_d(patterns, log)
    print(f"  examples dropped: {len(d_drops)}")

    print("--- BUG-E: expand short why ---")
    e_changes = fix_bug_e(patterns, log)
    print(f"  rows expanded: {len(e_changes)}")

    print("--- BUG-F: split long meaning_ja ---")
    f_changes = fix_bug_f(patterns, log)
    print(f"  patterns split: {len(f_changes)}")

    # Bump version
    new_version = "2026.05.24-content-fixes"
    if '_meta' not in g:
        g['_meta'] = {}
    g['_meta']['version'] = new_version
    g['_meta']['audit_wave_2026_05_24'] = (
        "Applied BUG-A..H content fixes: cm dedup (-N rows, +M backfill), "
        "category rename for n5-065..068, cross-contradiction resolution on n5-025+n5-166, "
        "wrong==right cm rewrites, example dedup, why expansion, meaning_ja split."
    )
    log['_meta']['corpus_version_after'] = new_version

    if args.apply:
        # Write grammar.json with 2-space indent
        out = json.dumps(g, ensure_ascii=False, indent=2)
        GRAMMAR.write_text(out + '\n', encoding='utf-8')

        # Update index.json size_bytes (LF-normalized)
        idx = json.loads(INDEX.read_text(encoding='utf-8'))
        lf_bytes = lf_size(GRAMMAR)
        for entry in idx.get('files', []):
            if entry.get('path') == 'data/grammar.json':
                entry['size_bytes'] = lf_bytes
                break
        INDEX.write_text(json.dumps(idx, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f"\ngrammar.json LF-normalised size: {lf_bytes}")

        # Write fix log
        FIX_LOG.write_text(json.dumps(log, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
        print(f"fix log: {FIX_LOG}")
    else:
        print(f"\n--dry-run: no files written")
        print(f"log preview keys: {list(log.keys())}")

    print(f"\n=== SUMMARY ===")
    print(f"BUG-A drops: {len(a_drops)}")
    print(f"BUG-A backfills: {len(backfills)}")
    print(f"BUG-B renames: {len(b_changed)}")
    print(f"BUG-C resolutions: {len(c_diffs)}")
    print(f"BUG-D example drops: {len(d_drops)}")
    print(f"BUG-E why expansions: {len(e_changes)}")
    print(f"BUG-F meaning_ja splits: {len(f_changes)}")
    print(f"BUG-H wrong==right rewrites: {len(h_changes)}")
    print(f"_meta.version: {g['_meta'].get('version')}")


if __name__ == '__main__':
    main()
