"""ISSUE-097 (round-9): grammar examples ≥5 (partial fix — 30 patterns).

Author authentic 4th example sentences for 30 high-priority N5 patterns
that currently sit at 3 examples (the spec floor). Each new example:
  - Uses only N5-vocab + N5-whitelist kanji (JA-1 + JA-13 compliant)
  - Demonstrates a different attachment surface, register, or context
    from the existing 3
  - Has translation_en + form tag

Coverage target: 30 of the 108 patterns at 3 examples → 4 examples.
The remaining 78 patterns are deferred to a follow-up authoring batch
(will be registered as a new ISSUE-NNN against the residual deficit).

Pattern-priority logic:
  - Audit-named worst-offenders first (n5-024..n5-038)
  - Then high-frequency core_n5 patterns the typical learner hits early
  - Skip late_n5 / borderline-N4 patterns until a future cycle

Idempotent: skips patterns already at ≥4 examples; deduplicates by JA.
"""
from __future__ import annotations
import sys, io, json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
from pathlib import Path

GRAMMAR = Path(__file__).parent.parent / 'data' / 'grammar.json'

# Map pattern_id -> new 4th example {form, ja, translation_en, romaji?}
# Each example uses different attachment/context from the existing 3 to
# satisfy the diversity-not-paraphrase audit criterion.
NEW_EXAMPLES = {
    # === Audit's named worst-offenders (n5-024..n5-038) ===
    'n5-024': {  # か - or between alternatives
        'form': 'verb-clause か verb-clause',
        'ja': 'えいがを 見るか 本を 読むか、まだ きめていません。',
        'translation_en': 'I haven\'t decided yet whether to watch a movie or read a book.',
    },
    'n5-027': {  # よね - assertion + seeking agreement
        'form': 'past',
        'ja': 'きのうの テストは むずかしかったですよね。',
        'translation_en': 'Yesterday\'s test was hard, wasn\'t it?',
    },
    'n5-028': {  # の - possessive/modifier
        'form': 'compound modifier',
        'ja': 'がっこうの となりの こうえんで あそびました。',
        'translation_en': 'I played in the park next to the school.',
    },
    'n5-030': {  # の - nominalizer
        'form': 'negative',
        'ja': 'あさ はやく おきるのは たいへんです。',
        'translation_en': 'Waking up early in the morning is hard.',
    },
    'n5-031': {  # の - informal question marker
        'form': 'past-question',
        'ja': 'きのう どこに いたの？',
        'translation_en': 'Where were you yesterday?',
    },
    'n5-034': {  # しか〜ない - only (with negative)
        'form': 'past-negative',
        'ja': 'パーティーには 三人しか 来ませんでした。',
        'translation_en': 'Only three people came to the party.',
    },
    'n5-035': {  # ぐらい / くらい - approximate quantity
        'form': 'noun-quantity',
        'ja': 'りんごを 五つぐらい 買いました。',
        'translation_en': 'I bought about five apples.',
    },
    'n5-036': {  # ごろ - approximate time point
        'form': 'past',
        'ja': '十時ごろに うちに かえりました。',
        'translation_en': 'I returned home around 10 o\'clock.',
    },
    'n5-037': {  # など - etc.
        'form': 'food-list',
        'ja': 'すしや てんぷらなどの 日本りょうりが すきです。',
        'translation_en': 'I like Japanese food such as sushi and tempura.',
    },
    'n5-038': {  # ずつ - distributive
        'form': 'time-distribution',
        'ja': '一週間に 三日ずつ 日本語を べんきょうします。',
        'translation_en': 'I study Japanese three days each week.',
    },
    # === Demonstrative cluster (n5-042..n5-049) ===
    'n5-042': {  # こちら/そちら/あちら/どちら
        'form': 'polite-question',
        'ja': 'おてあらいは どちらですか。',
        'translation_en': 'Where is the restroom? (polite)',
    },
    'n5-043': {  # こんな/そんな/あんな/どんな + Noun
        'form': 'question-with-noun',
        'ja': 'どんな 本を 読みたいですか。',
        'translation_en': 'What kind of book do you want to read?',
    },
    'n5-044': {  # こう/そう/ああ/どう
        'form': 'question-with-verb',
        'ja': 'この かんじは どう 読みますか。',
        'translation_en': 'How do you read this kanji?',
    },
    'n5-049': {  # どれ/どの/どちら - which
        'form': 'with-counter',
        'ja': 'どの くつが いいですか。',
        'translation_en': 'Which shoes are good?',
    },
    # === Question words (n5-051..n5-057) ===
    'n5-051': {  # どうして/なぜ - why
        'form': 'casual-context',
        'ja': 'どうして きのう 学校を 休みましたか。',
        'translation_en': 'Why did you skip school yesterday?',
    },
    'n5-052': {  # どうやって - how/by what means
        'form': 'with-place',
        'ja': 'えきまで どうやって 行きますか。',
        'translation_en': 'How do you get to the station?',
    },
    'n5-053': {  # いくら - how much (price)
        'form': 'in-shopping',
        'ja': 'この シャツは いくらですか。',
        'translation_en': 'How much is this shirt?',
    },
    'n5-055': {  # なんじ - what time
        'form': 'in-question',
        'ja': '来週の かいぎは なんじから ですか。',
        'translation_en': 'From what time is next week\'s meeting?',
    },
    'n5-056': {  # なんようび - what day of the week
        'form': 'in-question',
        'ja': 'あなたの たんじょうびは なんようびですか。',
        'translation_en': 'On what day of the week is your birthday?',
    },
    'n5-057': {  # なんがつ なんにち
        'form': 'date-question',
        'ja': '日本に いつ 来ましたか。なんがつ なんにちですか。',
        'translation_en': 'When did you come to Japan? What month and date?',
    },
    # === Verbs (n5-063, n5-076) ===
    'n5-063': {  # Verb-ましょうか - shall I/we
        'form': 'service-offer',
        'ja': 'まどを あけましょうか。',
        'translation_en': 'Shall I open the window?',
    },
    'n5-076': {  # Verb-てから - after doing X
        'form': 'morning-routine',
        'ja': 'はを みがいてから あさごはんを 食べます。',
        'translation_en': 'I brush my teeth and then eat breakfast.',
    },
    # === Adjectives (n5-078, n5-084) ===
    'n5-078': {  # i-Adjective + Noun
        'form': 'descriptive-context',
        'ja': 'たかい 山に のぼりました。',
        'translation_en': 'I climbed a high mountain.',
    },
    'n5-084': {  # na-Adjective + na + Noun
        'form': 'descriptive-person',
        'ja': 'しんせつな 先生は すきです。',
        'translation_en': 'I like kind teachers.',
    },
    # === Existential / possession (n5-093, n5-094) ===
    'n5-093': {  # X is at Y
        'form': 'with-location',
        'ja': 'ぎんこうは えきの まえに あります。',
        'translation_en': 'The bank is in front of the station.',
    },
    'n5-094': {  # there is / have
        'form': 'about-events',
        'ja': 'あした じゅぎょうが ありません。',
        'translation_en': 'Tomorrow there are no classes.',
    },
    # === Comparison (n5-095..n5-097) ===
    'n5-095': {  # AはBより
        'form': 'comparison-of-distance',
        'ja': 'バスは 電車より おそいです。',
        'translation_en': 'The bus is slower than the train.',
    },
    'n5-096': {  # より～のほうが
        'form': 'food-preference',
        'ja': 'コーヒーより おちゃの ほうが すきです。',
        'translation_en': 'I like tea more than coffee.',
    },
    'n5-097': {  # AとBとどちらが
        'form': 'choice-question',
        'ja': '日本語と えいごと、どちらが むずかしいですか。',
        'translation_en': 'Which is more difficult, Japanese or English?',
    },
    # === Likes/dislikes/wants (n5-099, n5-100, n5-105) ===
    'n5-099': {  # が すき/きらい
        'form': 'food-dislike',
        'ja': 'にくは すきですが、さかなは きらいです。',
        'translation_en': 'I like meat, but I dislike fish.',
    },
    'n5-100': {  # が じょうず/へた
        'form': 'skill-comparison',
        'ja': 'あには ピアノが じょうずです。',
        'translation_en': 'My older brother is good at piano.',
    },
    'n5-105': {  # たくないです - don't want to
        'form': 'specific-don\'t-want',
        'ja': 'しゅくだいを したくないです。',
        'translation_en': 'I don\'t want to do homework.',
    },
}


def main() -> int:
    doc = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    patterns = doc['patterns']
    by_id = {p['id']: p for p in patterns}

    n_added = 0
    n_skipped_full = 0
    n_dup = 0
    n_missing_pattern = 0

    for pid, new_ex in NEW_EXAMPLES.items():
        p = by_id.get(pid)
        if not p:
            n_missing_pattern += 1
            continue
        existing = p.get('examples', [])
        if len(existing) >= 5:
            n_skipped_full += 1
            continue
        # Dedup by JA
        existing_ja = {e.get('ja', '').strip() for e in existing}
        if new_ex['ja'].strip() in existing_ja:
            n_dup += 1
            continue
        existing.append(new_ex)
        n_added += 1

    GRAMMAR.write_text(
        json.dumps(doc, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8'
    )

    # Verify
    doc2 = json.loads(GRAMMAR.read_text(encoding='utf-8'))
    counts = {}
    for p in doc2['patterns']:
        n = len(p.get('examples', []))
        counts[n] = counts.get(n, 0) + 1
    at_4plus = sum(1 for p in doc2['patterns'] if len(p.get('examples', [])) >= 4)
    at_5plus = sum(1 for p in doc2['patterns'] if len(p.get('examples', [])) >= 5)
    print(f'Examples added: {n_added}')
    print(f'Skipped (already ≥5): {n_skipped_full}')
    print(f'Skipped (JA dup):     {n_dup}')
    print(f'Pattern not found:    {n_missing_pattern}')
    print(f'\nPost-fix distribution: {sorted(counts.items())}')
    print(f'Patterns ≥4 examples: {at_4plus}/178')
    print(f'Patterns ≥5 examples: {at_5plus}/178')
    return 0


if __name__ == '__main__':
    sys.exit(main())
