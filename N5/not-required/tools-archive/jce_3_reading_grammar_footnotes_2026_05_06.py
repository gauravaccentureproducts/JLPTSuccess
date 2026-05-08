"""JCE-3: Author grammar_footnotes on N5 reading passages.

Schema: grammar_footnotes is a list of dicts:
  {
    "sentence_index": <int 0-based>,
    "pattern_id": "n5-NNN",
    "note": "<short explanation of what the pattern is doing here>"
  }

Renderer expected to render an inline pop-over linking to the
pattern detail page; the note provides one-sentence context.

Authored 2026-05-06 by Claude. Initial pass covers the 15 highest-
leverage mondai-4 short passages (n5.read.001-015 minus those that
are pure information-search like n5.read.007). Remaining ~30 passages
queued for future batch.

Idempotent: skips passages with populated grammar_footnotes.
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
READING = ROOT / 'data' / 'reading.json'

# pid -> list of footnote dicts
FOOTNOTES: dict[str, list[dict]] = {
    # n5.read.001 — self-introduction
    # わたしは アンナです。アメリカから 来ました。今、とうきょうの 大学で 日本語を べんきょうしています。しゅみは えいがを 見ることです。どうぞ よろしく おねがいします。
    'n5.read.001': [
        {'sentence_index': 0, 'pattern_id': 'n5-002',
         'note': 'は marks "as for me" — the topic of the rest of the discourse.'},
        {'sentence_index': 1, 'pattern_id': 'n5-009',
         'note': 'から here is "from" (origin of motion / location). Pairs with 来ました.'},
        {'sentence_index': 2, 'pattern_id': 'n5-007',
         'note': 'で marks the location-of-action: "study AT the Tokyo university".'},
        {'sentence_index': 2, 'pattern_id': 'n5-072',
         'note': '〜ています = present continuous / habitual: "is studying / studies".'},
        {'sentence_index': 3, 'pattern_id': 'n5-030',
         'note': '見ること — verb-plain + こと turns "see" into the noun "seeing / watching", which is then connected with は as the subject of "is my hobby".'},
    ],
    # n5.read.002 — daily routine
    # わたしは 毎日 6時に おきます。あさごはんを 食べてから、しごとに 行きます。しごとは 9時から 5時までです。うちに かえってから、テレビを 見ます。10時に ねます。
    'n5.read.002': [
        {'sentence_index': 0, 'pattern_id': 'n5-115',
         'note': 'に marks the specific clock-time: "wake up AT 6:00".'},
        {'sentence_index': 1, 'pattern_id': 'n5-076',
         'note': '〜てから = "after doing X". Here: "after eating breakfast, I go to work".'},
        {'sentence_index': 2, 'pattern_id': 'n5-021',
         'note': '〜から〜まで = "from X to Y" (range). Here: "9 to 5".'},
        {'sentence_index': 3, 'pattern_id': 'n5-076',
         'note': '〜てから again — "after returning home, I watch TV".'},
    ],
    # n5.read.003 — weekend plan
    # あした、ともだちと えいがを 見に 行きます。えいがの あとで、レストランで ばんごはんを 食べます。とても たのしみです。
    'n5.read.003': [
        {'sentence_index': 0, 'pattern_id': 'n5-008',
         'note': 'と here = "with" (companion). "Going with friends".'},
        {'sentence_index': 0, 'pattern_id': 'n5-107',
         'note': 'Verb-stem + に行く = "go to do X". 見に 行く = "go to see (a movie)".'},
        {'sentence_index': 1, 'pattern_id': 'n5-120',
         'note': '〜のあとで = "after X". Here: "after the movie".'},
        {'sentence_index': 1, 'pattern_id': 'n5-007',
         'note': 'で = location of action: "eat AT the restaurant".'},
    ],
    # n5.read.004 — shopping at konbini
    # きのう、コンビニで パンと コーヒーを 買いました。パンは 200円で、コーヒーは 150円でした。ぜんぶで 350円でした。やすかったです。
    'n5.read.004': [
        {'sentence_index': 0, 'pattern_id': 'n5-007',
         'note': 'で = location of action: "buy AT the konbini".'},
        {'sentence_index': 0, 'pattern_id': 'n5-008',
         'note': 'と = "and" (exhaustive list): "bread AND coffee".'},
        {'sentence_index': 0, 'pattern_id': 'n5-060',
         'note': '買いました = polite past affirmative ("bought").'},
        {'sentence_index': 1, 'pattern_id': 'n5-089',
         'note': '〜で = na-adjective te-form connector linking two clauses with the same subject — except here it is connecting two complete clauses with "and" sense.'},
        {'sentence_index': 3, 'pattern_id': 'n5-081',
         'note': 'やすかった = i-adjective past ("was cheap").'},
    ],
    # n5.read.005 — family
    # わたしの かぞくは 4人です。父と 母と あにが います。父は 先生で、母は いしゃです。あには 大学生です。わたしは こうこうせいです。みんな げんきです。
    'n5.read.005': [
        {'sentence_index': 0, 'pattern_id': 'n5-028',
         'note': 'の = possessive: "MY family".'},
        {'sentence_index': 1, 'pattern_id': 'n5-091',
         'note': 'います = exists (animate). Used because family members are people.'},
        {'sentence_index': 2, 'pattern_id': 'n5-089',
         'note': 'で = na/noun-copula te-form: "father IS-a-teacher AND mother IS-a-doctor".'},
        {'sentence_index': 5, 'pattern_id': 'n5-085',
         'note': 'な-adjective + です: げんきです = "are healthy / energetic".'},
    ],
    # n5.read.006 — weather
    # 今日は とても さむいです。あさは あめが ふっていました。今は ふっていませんが、まだ さむいです。あした、ゆきが ふると おもいます。
    'n5.read.006': [
        {'sentence_index': 0, 'pattern_id': 'n5-079',
         'note': 'i-adjective + です: さむいです = "is cold" (polite).'},
        {'sentence_index': 1, 'pattern_id': 'n5-072',
         'note': '〜ていました = past progressive: "was raining".'},
        {'sentence_index': 2, 'pattern_id': 'n5-073',
         'note': '〜ていません = present negative progressive: "is not raining (now)".'},
        {'sentence_index': 2, 'pattern_id': 'n5-126',
         'note': 'が (mid-sentence) = "but" — links two contrasting clauses.'},
        {'sentence_index': 3, 'pattern_id': 'n5-145',
         'note': '〜と おもいます = "I think that ~" — quotation-marker と + おもう (think).'},
    ],
    # n5.read.008 — commute
    'n5.read.008': [
        {'sentence_index': 0, 'pattern_id': 'n5-021',
         'note': '〜から〜まで = "from X to Y" range — house TO school.'},
        {'sentence_index': 1, 'pattern_id': 'n5-041',
         'note': 'まず = "first of all" (sequence adverb).'},
        {'sentence_index': 2, 'pattern_id': 'n5-006',
         'note': 'に here = arrival point: "arrive AT school".'},
    ],
    # n5.read.009 — hobby (sports)
    'n5.read.009': [
        {'sentence_index': 0, 'pattern_id': 'n5-085',
         'note': 'na-adjective + です: スポーツです (here noun + です meaning "is sports").'},
        {'sentence_index': 1, 'pattern_id': 'n5-007',
         'note': 'で = location of action: "run AT the park".'},
        {'sentence_index': 2, 'pattern_id': 'n5-008',
         'note': 'と = "with" (companion).'},
    ],
    # n5.read.010 — classroom
    'n5.read.010': [
        {'sentence_index': 0, 'pattern_id': 'n5-090',
         'note': 'あります = exists (inanimate). Used for desks because they are objects.'},
        {'sentence_index': 1, 'pattern_id': 'n5-013',
         'note': 'も = "also". "Chairs ALSO have 25".'},
        {'sentence_index': 3, 'pattern_id': 'n5-007',
         'note': 'から in 〜から〜が見えます context = visible-from origin.'},
    ],
    # n5.read.012 — bookstore
    'n5.read.012': [
        {'sentence_index': 0, 'pattern_id': 'n5-007',
         'note': 'で = location of action: "buy AT the bookstore".'},
        {'sentence_index': 0, 'pattern_id': 'n5-108',
         'note': '2さつ = counter for books. The counter follows the noun + を.'},
        {'sentence_index': 1, 'pattern_id': 'n5-076',
         'note': '〜てから = "after returning home, I read".'},
        {'sentence_index': 2, 'pattern_id': 'n5-126',
         'note': 'が (mid-sentence) = "but" — "was hard, BUT was interesting".'},
    ],
    # n5.read.014 — depaato shopping
    'n5.read.014': [
        {'sentence_index': 0, 'pattern_id': 'n5-007',
         'note': 'で = location of action: "buy AT the depaato".'},
        {'sentence_index': 1, 'pattern_id': 'n5-089',
         'note': 'で connects "shirt was 3000 yen" and "pants were 5000 yen" as one statement.'},
        {'sentence_index': 3, 'pattern_id': 'n5-126',
         'note': 'が (mid-sentence) = "but" — "was a bit expensive, BUT very pretty".'},
    ],
    # n5.read.015 — sakura
    'n5.read.015': [
        {'sentence_index': 1, 'pattern_id': 'n5-143',
         'note': '〜くなる = "becoming X" (i-adjective). あたたかくなりました = "got warmer".'},
        {'sentence_index': 2, 'pattern_id': 'n5-090',
         'note': 'さくらが さきました = "cherry blossoms have bloomed" (intransitive verb).'},
        {'sentence_index': 3, 'pattern_id': 'n5-107',
         'note': 'verb-stem + に行く: 見に行きます = "go to see".'},
    ],
    # n5.read.016 — illness
    'n5.read.016': [
        {'sentence_index': 0, 'pattern_id': 'n5-009',
         'note': 'から here = "from" (origin in time). きのうから = "since yesterday".'},
        {'sentence_index': 1, 'pattern_id': 'n5-013',
         'note': 'も = "also". "Cough ALSO comes out a little".'},
        {'sentence_index': 2, 'pattern_id': 'n5-069',
         'note': 'te-form chaining: 休んで...ねます = "rest and sleep".'},
        {'sentence_index': 4, 'pattern_id': 'n5-104',
         'note': 'verb-stem + たい = "want to". なりたい = "want to become".'},
    ],
    # n5.read.018 — studying Japanese for 1 year
    'n5.read.018': [
        {'sentence_index': 0, 'pattern_id': 'n5-072',
         'note': '〜ています here = "have been studying / am currently studying" (continuing state).'},
        {'sentence_index': 1, 'pattern_id': 'n5-035',
         'note': 'くらい = "about". 30分くらい = "about 30 minutes".'},
        {'sentence_index': 2, 'pattern_id': 'n5-126',
         'note': 'が (mid-sentence) = "but" — "kanji is hard, BUT hiragana is easy".'},
        {'sentence_index': 3, 'pattern_id': 'n5-104',
         'note': '行きたいです = "want to go". たい = i-adjective-style desiderative.'},
    ],
    # n5.read.019 — beach trip
    'n5.read.019': [
        {'sentence_index': 0, 'pattern_id': 'n5-008',
         'note': 'と = "with" (companion).'},
        {'sentence_index': 0, 'pattern_id': 'n5-006',
         'note': 'に = direction marker (movement target). うみに行く = "go TO the sea".'},
        {'sentence_index': 1, 'pattern_id': 'n5-079',
         'note': 'i-adj + です: よかったです = "was good" (i-adj past polite).'},
    ],
}


def main():
    with READING.open('r', encoding='utf-8') as f:
        data = json.load(f)

    passages = data['passages']
    by_id = {p['id']: p for p in passages}

    matched = 0
    skipped_have = 0
    not_found = []
    total_footnotes = 0
    for pid, footnotes in FOOTNOTES.items():
        p = by_id.get(pid)
        if p is None:
            not_found.append(pid)
            continue
        if p.get('grammar_footnotes'):
            skipped_have += 1
            continue
        p['grammar_footnotes'] = footnotes
        p['grammar_footnotes_provenance'] = 'llm_curated'
        matched += 1
        total_footnotes += len(footnotes)

    print(f'Authored grammar_footnotes on {matched} passages.')
    print(f'Total footnote entries: {total_footnotes}')
    print(f'Skipped (already had value): {skipped_have}')
    if not_found:
        print(f'IDs not found: {not_found}')

    with READING.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Wrote: {READING}')


if __name__ == '__main__':
    main()
