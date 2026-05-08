"""Author the 45 missing dokkai rationales (Q11-Q60 with empty fields).

Updates BOTH:
  - KnowledgeBank/dokkai_questions_n5.md (source MD)
  - data/papers/dokkai/paper-{1..4}.json (extracted paper JSONs)

Each rationale references the passage detail that justifies the marked
correct answer. Brief 1-line format mirroring the existing 15 dokkai
rationales (e.g., "first action is meeting at station." for Q9). Style
varies - sometimes English narration, sometimes Japanese excerpt - to
match what the corpus already does.

JA-32 compliance: every kanji used in a new rationale also appears in
the corresponding MD Q-block (passage + stem + choices), so the
"stale-extract" check stays green.

Idempotent: skips entries that already have non-empty rationales.
"""
from __future__ import annotations
import io
import json
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
KB_MD = ROOT / 'KnowledgeBank' / 'dokkai_questions_n5.md'
PAPERS = ROOT / 'data' / 'papers' / 'dokkai'

# kbSourceId → rationale (the 45 originally-empty ones)
RATIONALES: dict[str, str] = {
    # ---- Paper 1 (Q11-Q16 in scope; only Q11/Q12/Q13/Q15/Q16 empty) ----
    'Q11': 'asks やまださん to bring the homework paper from the classroom locker.',
    'Q12': 'ロッカーの ばんごうは 七です - locker number is 7.',
    'Q13': 'こうえんを さんぽする - walks through the park each morning.',
    'Q15': 'ケーキは 友だちが 作って もって 来ます - friend makes and brings the cake.',
    'Q16': 'ともだちは みんな 八時に 来ます - everyone arrives at 8 o\'clock.',

    # ---- Paper 2 (Q17-Q32 in scope; 13 empty in this set) ----
    'Q18': '水曜日は 病院に 行きました - went to the hospital on Wednesday.',
    'Q19': 'asks everyone to call (電話して ください) if they want to come.',
    'Q20': '弁当と 水を じぶんで もって 来て - bring lunch and water yourself.',
    'Q21': '母は 病院で はたらいて います - mother works at the hospital.',
    'Q22': '日曜日は いつも 家に いて、 私と あそびます - Sundays at home with the narrator.',
    'Q23': 'たくさん 雨が ふりました - heavy rain last night.',
    'Q24': 'こうえんで お弁当を 食べる つもり - plans to eat bento in the park today.',
    'Q25': '私は えいごの じゅぎょうが すきです - likes the English class.',
    'Q28': 'ばんごはんは いつも かいしゃの ちかくの レストランで 食べます - always eats dinner at a restaurant near the office.',
    'Q29': 'シロは 五さいです - Shiro is 5 years old.',
    'Q30': '白い 犬ですから、 シロです - named Shiro because the dog is white (white = しろい).',
    'Q31': 'まいばん、 ねる まえに 一時間 ピアノを ひきます - plays piano alone every night before bed.',
    'Q32': 'こんしゅうの どようび、 がっこうで コンサートが あります - concert this Saturday at the school.',

    # ---- Paper 3 (Q33-Q48 in scope; 16 empty in this set) ----
    'Q33': 'えいがは 三時から 五時まで - movie runs 3 to 5; starts at 3.',
    'Q34': 'えいがが 終わったら、 こうちゃの きっさてんで - after the movie, goes to a tea cafe.',
    'Q35': '父は 大学生の とき、 中国に すんで いました - lived in China during university.',
    'Q36': 'むずかしい...あまり 上手では ありません - narrator finds Chinese hard, not very good at it.',
    'Q37': '一しゅうかんに 三回 - three times a week.',
    'Q38': '日曜日は 学校が 休みですから、 プールも 使えません - pool unavailable on Sundays.',
    'Q39': 'パンが ありませんでしたから、 ごはんを 食べました - no bread, so ate rice instead.',
    'Q40': 'パンが ありませんでした - usual bread+milk replaced by rice+tea today.',
    'Q41': 'こんしゅうの 火曜日、 友だちの たんじょうびです - friend\'s birthday is this Tuesday.',
    'Q42': '大きい ケーキは 高いです - big cakes are expensive, so picks small ones.',
    'Q43': '妹は 日本語を べんきょうしたい - younger sister wants to study Japanese.',
    'Q44': '家は 大学から とおいですから、 ...アパートに ひっこします - house is far from the university, so she\'ll move closer.',
    'Q45': '私の しゅみは しゃしんを とる こと - narrator\'s hobby is photography.',
    'Q46': 'はなや 木や そらの しゃしんを とります - takes photos of flowers, trees, and the sky.',
    'Q47': 'あさ 七時の しんかんせんに のります - takes the 7 AM shinkansen tomorrow.',
    'Q48': '大阪から 東京に かえるのは あさっての よる - returns to Tokyo on the evening of the day after tomorrow.',

    # ---- Paper 4 (Q49-Q60 in scope; 11 empty in this set) ----
    'Q49': 'でんしゃで かいしゃに 行きます - commutes by train.',
    'Q50': 'でんしゃは とても こんで います。...父は いつも 立って います - packed train, has to stand the whole way.',
    'Q52': '大学の コンサートで ひきます - older brother plays at the university concert this week.',
    'Q53': 'まい朝、 でんしゃの 中で パンを 食べます - usually eats breakfast (bread) on the train.',
    'Q54': 'でんしゃが こんで いて、 パンを 食べる ことが できませんでした - couldn\'t eat breakfast on the crowded train, so ate more at lunch.',
    'Q55': 'いま 日本の かいしゃで はたらいて います - currently works at a Japanese company.',
    'Q56': '五年 まえに 日本に 来ました - came to Japan 5 years ago.',
    'Q57': 'その みせは 三月に できました - the cafe opened in March.',
    'Q58': 'コーヒーが おいしくて、 ねだんも 安いです - coffee is delicious and prices are cheap; wants to bring a friend.',
    'Q59': 'こんしゅうの 土曜日、 ...ハイキングに 行く つもりでした - original plan was hiking this Saturday.',
    'Q60': '木曜日から 雨が ふって います。土曜日も 雨の よほうです - has been raining since Thursday, Saturday\'s forecast is also rain, so postponed to next week.',
}


changes: list[str] = []


def update_paper_json() -> None:
    for n in (1, 2, 3, 4):
        p_path = PAPERS / f'paper-{n}.json'
        paper = json.loads(p_path.read_text(encoding='utf-8'))
        modified = False
        for q in paper.get('questions', []):
            kb = q.get('kbSourceId')
            if kb in RATIONALES and not (q.get('rationale') or '').strip():
                q['rationale'] = RATIONALES[kb]
                modified = True
                changes.append(f'paper-{n}.json {q.get("id", "?")} ({kb}): authored rationale')
        if modified:
            p_path.write_text(json.dumps(paper, ensure_ascii=False, indent=2),
                              encoding='utf-8')


def update_md() -> None:
    """Replace `**Answer: N**.` with `**Answer: N** - <rationale>` in MD source.

    Only updates Q-blocks whose answer line is the bare period form
    (no rationale text yet). Idempotent.
    """
    text = KB_MD.read_text(encoding='utf-8')
    for kb_q, rat in RATIONALES.items():
        # Find the Q-block first
        block_re = re.compile(
            rf'(### {re.escape(kb_q)}\b[\s\S]+?\*\*Answer:\s*\d+\*\*)\.(?!\s*-)'
        )
        m = block_re.search(text)
        if m is None:
            continue
        # Replace the trailing period with " - <rationale>."
        replacement = f'{m.group(1)} - {rat}'
        new_text = text[:m.start()] + replacement + text[m.end():]
        if new_text != text:
            text = new_text
            changes.append(f'dokkai_questions_n5.md {kb_q}: authored rationale')
    KB_MD.write_text(text, encoding='utf-8')


def main() -> int:
    update_md()       # MD first so paper update can verify against it
    update_paper_json()

    if not changes:
        print('No changes (all rationales already authored).')
        return 0
    print(f'{len(changes)} edits applied:')
    for c in changes:
        print(f'  - {c}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
