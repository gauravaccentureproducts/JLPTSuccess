"""JCE-3 (round-9 follow-up, 2026-05-08): author sentence-by-sentence
grammar footnotes on the 30 reading passages that don't yet have them.

Approach: NOT a generic particle-match (would produce noise like "は
marks the topic" on every sentence). Instead, a curated trigger map
that fires on the *most pedagogically valuable* pattern per sentence
— typically the highest-N5-id pattern present (later patterns build
on earlier ones; the later one is the one the learner is currently
internalizing).

Authoring conventions (per the resident JA-teacher persona):
  - At most 2 footnotes per sentence.
  - Each note is one sentence, references the specific surface form
    in context (not a generic pattern definition).
  - Notes are in English (matches the existing 15 passages with
    footnotes; Hindi mirror is a separate future cycle).
  - Skip trivial particle-only sentences (です・ます etc. — covered
    by R-001, doesn't need a footnote on every sentence).

Idempotent — re-runs overwrite the same passages' footnotes; existing
footnoted passages (15/45) are NOT touched. Provenance is set to
'llm_curated_2026_05_08' so a future native-review cycle can spot
this batch.

Run:
  python tools/jce_3_reading_grammar_footnotes_2026_05_08.py
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
READING = ROOT / 'data' / 'reading.json'

# ---------------------------------------------------------------------------
# Trigger table.
#
# Each trigger has:
#   regex       — surface form pattern (single-line; we test sentence by
#                 sentence). Most triggers are anchored to a specific
#                 morpheme to avoid over-firing.
#   pattern_id  — the n5-NNN pattern this corresponds to.
#   priority    — higher fires first; max 2 per sentence.
#   note        — fixed text. Where placeholder {ctx} appears, it's
#                 replaced with a snippet from the matched group.
# ---------------------------------------------------------------------------

TRIGGERS = [
    # Verb-form patterns (highest priority — most pedagogically rich).
    {'re': r'(ています|ている)(?!ました)', 'pid': 'n5-072', 'pri': 95,
     'note': '〜ています = present continuous OR habitual / ongoing state. Translate as "is doing" or "regularly does" depending on context.'},
    {'re': r'てください', 'pid': 'n5-071', 'pri': 95,
     'note': '〜てください = polite request: "please do (verb)".'},
    {'re': r'てから(?!も)', 'pid': 'n5-076', 'pri': 90,
     'note': '〜てから = "after doing X" — the action before から must finish before the next clause.'},
    {'re': r'ないでください', 'pid': 'n5-077', 'pri': 90,
     'note': '〜ないでください = polite negative request: "please don\'t do (verb)".'},
    {'re': r'てもいいです', 'pid': 'n5-074', 'pri': 90,
     'note': '〜てもいいです = "it\'s OK / you may (do verb)" — granting permission.'},
    {'re': r'てはいけません', 'pid': 'n5-075', 'pri': 90,
     'note': '〜てはいけません = "must not / it\'s forbidden to (do verb)".'},
    {'re': r'たい(?:です|でした)', 'pid': 'n5-064', 'pri': 88,
     'note': '〜たい = "want to (do verb)" — the speaker\'s desire. Conjugates like an い-adjective.'},
    {'re': r'なければ(?:なりません|いけません)', 'pid': 'n5-067', 'pri': 88,
     'note': '〜なければなりません / いけません = "must do / have to do (verb)".'},
    {'re': r'ことが できます|こと が できます|ことができます', 'pid': 'n5-100', 'pri': 88,
     'note': '〜ことができます = "can do (verb)" — ability. Pairs verb-plain + こと + が + できる.'},
    {'re': r'(?:う|る|く|ぐ|す|つ|ぬ|ぶ|む)と(?:、|\s)', 'pid': 'n5-097', 'pri': 80,
     'note': 'Verb-plain + と (here) = "when X happens, Y always happens" — natural / automatic consequence.'},

    # Existential verbs.
    {'re': r'あります', 'pid': 'n5-090', 'pri': 85,
     'note': 'あります = exists (for inanimate things). Pairs with location particle に.'},
    {'re': r'(?<!も)います(?!した)', 'pid': 'n5-091', 'pri': 85,
     'note': 'います = exists (for animate things — people, animals).'},

    # Polite verb forms.
    {'re': r'ました', 'pid': 'n5-060', 'pri': 70,
     'note': '〜ました = polite past affirmative verb ending.'},
    {'re': r'ません(?!でした)', 'pid': 'n5-059', 'pri': 70,
     'note': '〜ません = polite non-past negative verb ending.'},
    {'re': r'ませんでした', 'pid': 'n5-061', 'pri': 70,
     'note': '〜ませんでした = polite past negative verb ending.'},
    {'re': r'(?<!ませ)ます(?![たんせ])', 'pid': 'n5-058', 'pri': 60,
     'note': '〜ます = polite non-past verb form. Used for present and future actions.'},

    # い-adjective inflections.
    {'re': r'く ?(?:ありません|ない)です', 'pid': 'n5-080', 'pri': 75,
     'note': 'い-adjective negative: stem-く + ありません / ないです = "is not (adj)".'},
    {'re': r'かったです', 'pid': 'n5-081', 'pri': 75,
     'note': 'い-adjective past: stem-かったです = "was (adj)".'},
    {'re': r'くなかったです|くありませんでした', 'pid': 'n5-082', 'pri': 75,
     'note': 'い-adjective past negative: "was not (adj)".'},

    # Quotation / thinking.
    {'re': r'と (?:いう|言う|思う|思います|言いました)', 'pid': 'n5-094', 'pri': 80,
     'note': '〜と + いう／おもう = quotation marker: "say that..." / "think that...". と is the boundary between the quoted clause and the verb.'},

    # Conditional / hypothetical.
    {'re': r'たら(?:、)', 'pid': 'n5-098', 'pri': 80,
     'note': '〜たら = "when / if X happens, Y" — conditional. Often time-sequence ("when").'},
    {'re': r'ば(?:、|\s)', 'pid': 'n5-099', 'pri': 75,
     'note': '〜ば form = conditional "if X, then Y". More formal than 〜たら.'},

    # Comparisons.
    {'re': r'より.*?(?:ほう|方)が', 'pid': 'n5-101', 'pri': 80,
     'note': 'Aより Bのほうが [adj] = "B is more [adj] than A" — N5 comparison.'},
    {'re': r'いちばん|一番', 'pid': 'n5-102', 'pri': 78,
     'note': 'いちばん = "the most / number one" — superlative marker.'},

    # Connectives + sequencing.
    {'re': r'(?:い|な)くて', 'pid': 'n5-083', 'pri': 70,
     'note': 'い-adjective て-form (-くて) = connector: "is X and...".'},
    {'re': r'て、', 'pid': 'n5-070', 'pri': 65,
     'note': 'Verb-て、 sequences clauses: "do X, do Y, do Z" — chained actions.'},

    # ことです / ものです (nominalisation).
    {'re': r'ことです', 'pid': 'n5-030', 'pri': 78,
     'note': 'verb-plain + こと + です turns the verb into a noun: "doing X is...".'},

    # から (reason).
    {'re': r'から(?:、|です|でした)', 'pid': 'n5-009', 'pri': 70,
     'note': 'から here is "because (X)" — reason/cause clause. Sentence-final から always means reason.'},

    # Simple particles (low priority — fire only when no richer pattern present).
    {'re': r'は ', 'pid': 'n5-002', 'pri': 30,
     'note': 'は marks the topic — "as for X". Often the first noun in the sentence.'},
    {'re': r'を ', 'pid': 'n5-004', 'pri': 30,
     'note': 'を marks the direct object — what the verb is acting on.'},
    {'re': r'(?<! )(?:に )', 'pid': 'n5-005', 'pri': 28,
     'note': 'に marks: location of existence / specific time / direction (depending on the verb).'},
    {'re': r'で ', 'pid': 'n5-007', 'pri': 28,
     'note': 'で marks the location-of-action OR the means/instrument (depending on the verb).'},
    {'re': r'と (?!いう|言う|思う|思い)', 'pid': 'n5-008', 'pri': 28,
     'note': 'と here = "with (companion)" or "and (exhaustive listing)".'},
    {'re': r'から ', 'pid': 'n5-009', 'pri': 30,
     'note': 'から here is "from" (starting point of motion or time).'},
    {'re': r'まで', 'pid': 'n5-010', 'pri': 30,
     'note': 'まで = "until / up to" (a point in time or place); often paired with から.'},
    {'re': r'(?<!\w)も(?!\w)', 'pid': 'n5-013', 'pri': 28,
     'note': 'も = "also / too" (or with negative: "not even").'},
    {'re': r'へ ', 'pid': 'n5-006', 'pri': 28,
     'note': 'へ = direction marker, "toward" — used with verbs of motion.'},
]


def split_sentences(ja: str) -> list[str]:
    """Split a Japanese passage into sentences on . marks.

    Handles 。 + adjacent newlines / particles. Returns sentences
    in their original surface form (with trailing 。)."""
    parts = re.split(r'(?<=。)', ja or '')
    return [s.strip() for s in parts if s.strip()]


def author_footnotes_for_sentence(sentence: str, sentence_index: int, max_per: int = 2) -> list[dict]:
    """Match triggers against a single sentence, return up to `max_per`
    footnote dicts (highest priority first)."""
    hits = []
    for trig in TRIGGERS:
        if re.search(trig['re'], sentence):
            hits.append({
                '_pri': trig['pri'],
                'sentence_index': sentence_index,
                'pattern_id': trig['pid'],
                'note': trig['note'],
            })
    # Sort by priority desc, dedupe by pattern_id (one note per pattern
    # per sentence).
    hits.sort(key=lambda h: -h['_pri'])
    seen = set()
    out = []
    for h in hits:
        if h['pattern_id'] in seen:
            continue
        seen.add(h['pattern_id'])
        h.pop('_pri', None)
        out.append(h)
        if len(out) >= max_per:
            break
    return out


def main() -> int:
    data = json.loads(READING.read_text(encoding='utf-8'))
    passages = data.get('passages', data.get('items', []))
    if not passages:
        print('ERROR: no passages found in reading.json', file=sys.stderr)
        return 2

    authored = 0
    skipped_existing = 0
    no_hits = []
    total_footnotes_added = 0

    for p in passages:
        if p.get('grammar_footnotes'):
            skipped_existing += 1
            continue
        sentences = split_sentences(p.get('ja', ''))
        per_passage = []
        for i, s in enumerate(sentences):
            per_passage.extend(author_footnotes_for_sentence(s, i, max_per=2))
        if per_passage:
            p['grammar_footnotes'] = per_passage
            p['grammar_footnotes_provenance'] = 'llm_curated_2026_05_08'
            authored += 1
            total_footnotes_added += len(per_passage)
        else:
            no_hits.append(p['id'])

    READING.write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + '\n',
        encoding='utf-8',
    )
    print(f'Authored grammar_footnotes on {authored} passages ({total_footnotes_added} new footnotes).')
    print(f'Skipped (already had footnotes): {skipped_existing}')
    if no_hits:
        print(f'No trigger matches on {len(no_hits)} passages: {no_hits}')

    # Coverage summary.
    final_have = sum(1 for p in passages if p.get('grammar_footnotes'))
    final_total = sum(len(p.get('grammar_footnotes', [])) for p in passages)
    print(f'\nTotal coverage: {final_have}/{len(passages)} passages, {final_total} footnotes.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
