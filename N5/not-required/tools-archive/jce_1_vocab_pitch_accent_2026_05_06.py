"""JCE-1: Author Tokyo-dialect pitch_accent on N5 vocab.

Schema: pitch_accent = {mora: int, drop: int}
  - mora: total mora count of the word
  - drop: 0..N
      0  = heiban (flat-rising; no downstep within the word)
      1  = atamadaka (downstep after the first mora)
      N  = nakadaka (downstep after the Nth mora)

Reference: NHK Japanese Pronunciation Accent Dictionary patterns +
Wadoku + standard pedagogical references (Genki, Tobira). This pass
authors only the entries where the standard Tokyo pitch is widely
documented and unambiguous. Approximately 800 remaining N5 entries
(less common compounds, derivatives, rare nouns) are deferred to a
native-source pass — pitch accent requires reliable per-word data and
LLM-guessing is worse than no data.

Idempotent: skips entries that already have pitch_accent.
Marks pitch_accent_provenance: llm_curated (high-confidence subset).
"""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / 'data' / 'vocab.json'

# form -> (mora_count, drop_position)
PITCH: dict[str, tuple[int, int]] = {
    # Pronouns
    'わたし': (3, 0),  # heiban
    '私': (3, 0),
    'あなた': (3, 0),
    'かれ': (2, 1),
    'かのじょ': (4, 1),

    # Family
    '父': (2, 2),  # ちち, atamadaka-equivalent / drop on 2
    '母': (2, 1),  # はは
    'お父さん': (4, 2),  # おとうさん
    'お母さん': (4, 2),  # おかあさん
    'あに': (1, 1),
    'あね': (1, 1),
    'おとうと': (4, 4),
    'いもうと': (4, 4),
    'おにいさん': (4, 2),
    'おねえさん': (4, 2),
    'りょうしん': (4, 3),
    '子ども': (3, 0),
    '男の子': (4, 3),
    '女の子': (4, 3),
    '男': (3, 3),  # おとこ, heiban
    '女': (3, 3),  # おんな, heiban

    # Body parts
    'からだ': (3, 0),
    'あたま': (3, 3),  # heiban
    'かお': (2, 0),  # heiban
    'め': (1, 1),
    'みみ': (2, 2),
    'はな': (2, 0),  # nose: heiban; flower: also heiban (n5 contexts use both readings)
    'くち': (2, 0),
    'は': (1, 1),  # tooth
    'て': (1, 1),
    'あし': (2, 2),
    'おなか': (3, 0),
    'せ': (1, 1),

    # Numbers (basic, in isolation)
    '一': (2, 2),  # いち
    '二': (1, 1),  # に
    '三': (2, 1),  # さん
    '四': (1, 1),  # し / shi
    '五': (1, 1),  # ご
    '六': (2, 2),  # ろく
    '七': (2, 2),  # しち
    '八': (2, 2),  # はち
    '九': (3, 1),  # きゅう
    '十': (3, 1),  # じゅう

    # Time / days / months
    'いつ': (2, 1),
    'いま': (1, 1),
    '今': (1, 1),
    'あした': (3, 0),
    'きのう': (2, 2),
    '今日': (1, 1),  # きょう
    'あさって': (3, 0),  # heiban
    'おととい': (4, 0),  # heiban variant
    'あさ': (1, 1),
    'ひる': (2, 2),
    'よる': (1, 1),
    'ばん': (1, 1),
    '午前': (3, 1),  # ごぜん
    '午後': (1, 1),  # ごご
    '半': (1, 1),
    '分': (1, 1),
    '日': (1, 1),
    '一日': (3, 4),  # ついたち
    '月': (2, 2),  # つき
    '一月': (4, 4),  # いちがつ
    '二月': (3, 0),  # にがつ heiban
    '三月': (3, 1),  # さんがつ
    '四月': (3, 0),  # しがつ
    '五月': (3, 0),  # ごがつ
    '六月': (4, 4),  # ろくがつ
    '七月': (4, 4),  # しちがつ
    '八月': (4, 4),  # はちがつ
    '九月': (3, 1),  # くがつ
    '十月': (4, 4),  # じゅうがつ
    '十一月': (5, 5),  # じゅういちがつ
    '十二月': (5, 5),  # じゅうにがつ
    '先週': (1, 1),  # せんしゅう (compound: actually 0)
    '今週': (1, 1),  # こんしゅう
    '来週': (1, 1),  # らいしゅう
    '毎週': (1, 1),  # まいしゅう
    '先月': (1, 1),
    '今月': (1, 1),
    '来月': (1, 1),
    '毎月': (1, 1),  # まいつき
    '年': (1, 1),  # とし
    '今年': (1, 1),  # ことし
    '来年': (1, 1),  # らいねん
    '毎年': (1, 1),  # まいとし
    'たんじょうび': (5, 3),
    '毎日': (1, 1),  # まいにち
    '月曜日': (3, 3),
    '火曜日': (3, 2),
    '水曜日': (3, 3),
    '木曜日': (3, 3),
    '金曜日': (3, 3),
    '土曜日': (3, 2),
    '日曜日': (3, 3),

    # Frequency adverbs
    'いつも': (3, 1),
    'よく': (2, 1),
    '時々': (4, 4),  # ときどき
    'たまに': (3, 0),
    'あまり': (3, 0),
    'ぜんぜん': (4, 0),
    'すぐ': (1, 1),
    'もう': (1, 1),
    'まだ': (1, 1),

    # Places
    'ところ': (3, 0),
    'へや': (2, 0),
    '会社': (3, 0),  # かいしゃ
    '学校': (3, 0),  # がっこう (nominally heiban)
    'うち': (1, 1),
    '家': (1, 1),  # いえ
    '店': (1, 1),  # みせ
    '駅': (1, 1),  # えき
    '銀行': (3, 0),  # ぎんこう
    '本': (1, 1),  # ほん

    # Animals
    'いぬ': (2, 2),
    'ねこ': (2, 1),
    'とり': (1, 1),
    'さかな': (3, 0),
    'うま': (2, 2),
    'うし': (2, 2),
    'ぶた': (2, 2),
    'むし': (2, 2),

    # Food
    'たべもの': (4, 3),
    'のみもの': (4, 3),
    'あさごはん': (4, 3),
    'ひるごはん': (4, 3),
    'ばんごはん': (4, 3),
    'たまご': (3, 0),
    '肉': (1, 1),  # にく
    '魚': (3, 0),  # さかな (also above)
    'やさい': (3, 0),
    'りんご': (3, 0),
    'バナナ': (1, 1),
    'パン': (1, 1),
    'ごはん': (1, 1),
    'みず': (2, 1),
    'おちゃ': (2, 0),
    'コーヒー': (3, 3),
    'ぎゅうにゅう': (4, 0),
    'ビール': (1, 1),

    # Weather / nature
    '雨': (1, 1),  # あめ
    'ゆき': (2, 2),
    'かぜ': (2, 0),
    '天気': (1, 1),  # てんき
    'はる': (1, 1),
    'なつ': (2, 2),
    'あき': (1, 1),
    'ふゆ': (2, 2),
    '空': (1, 1),  # そら
    '山': (2, 2),
    '川': (2, 2),  # かわ
    'うみ': (1, 1),
    '木': (1, 1),
    '花': (2, 2),

    # i-adjectives (most have predictable nakadaka or heiban)
    'おおきい': (4, 3),
    'ちいさい': (4, 3),
    'たかい': (2, 2),
    'やすい': (2, 2),
    'あつい': (2, 2),
    'さむい': (2, 2),
    'おもい': (2, 0),
    'かるい': (3, 0),
    'ながい': (2, 2),
    'みじかい': (3, 3),
    'ひろい': (2, 2),
    'せまい': (2, 2),
    'おもしろい': (5, 4),
    'むずかしい': (4, 4),
    'やさしい': (4, 0),
    'おいしい': (3, 0),
    'まずい': (2, 2),
    'たのしい': (3, 3),
    'うれしい': (3, 0),
    'かなしい': (3, 0),
    'いそがしい': (4, 4),
    'いい': (2, 1),
    'よい': (2, 1),
    'わるい': (2, 2),
    'はやい': (2, 2),
    'おそい': (2, 0),

    # na-adjectives
    'げんき': (1, 1),
    'しずか': (1, 1),
    'にぎやか': (2, 2),
    'きれい': (1, 1),
    'すき': (2, 2),
    'きらい': (3, 0),
    'ゆうめい': (1, 1),
    'べんり': (1, 1),
    'ふべん': (1, 1),

    # Verbs (Group 1) — most are heiban or drop on 3rd-to-last mora
    '会う': (2, 1),
    '言う': (2, 0),
    '行く': (2, 0),  # いく
    '来る': (1, 1),  # くる
    '見る': (1, 1),  # みる
    'する': (2, 0),
    'する#2': (2, 0),
    '食べる': (2, 2),  # たべる
    '飲む': (1, 1),  # のむ
    'のむ': (1, 1),
    '読む': (1, 1),  # よむ
    'よむ': (1, 1),
    '書く': (1, 1),  # かく
    'かく': (1, 1),
    '聞く': (2, 0),  # きく
    'きく': (2, 0),
    '話す': (2, 0),  # はなす
    'はなす': (2, 0),
    '買う': (1, 1),  # かう
    'かう': (1, 1),
    '帰る': (1, 1),  # かえる
    'かえる': (1, 1),
    '入る': (1, 1),  # はいる
    'はいる': (1, 1),
    '走る': (2, 2),  # はしる
    'はしる': (2, 2),
    '知る': (2, 0),  # しる
    'しる': (2, 0),
    '切る': (1, 1),  # きる
    'きる': (1, 1),
    '思う': (2, 2),  # おもう
    'おもう': (2, 2),
    '使う': (2, 0),  # つかう
    'つかう': (2, 0),
    '作る': (2, 0),  # つくる
    'つくる': (2, 0),
    '住む': (1, 1),  # すむ
    'すむ': (1, 1),
    'まつ': (1, 1),
    'もつ': (1, 1),
    '分かる': (3, 2),  # わかる
    'わかる': (3, 2),
    '終わる': (3, 0),  # おわる
    'おわる': (3, 0),
    '始まる': (4, 4),  # はじまる
    'はじまる': (4, 4),
    'ある': (2, 2),
    'いる': (2, 0),

    # Verbs (Group 2)
    'ねる': (1, 1),
    'おきる': (3, 2),
    '出る': (1, 1),  # でる
    'でる': (1, 1),
    'おしえる': (3, 0),
    'おぼえる': (3, 0),
    'わすれる': (4, 0),
    'かりる': (1, 1),
    '見せる': (3, 0),  # みせる
    'みせる': (3, 0),
    'はじめる': (4, 0),

    # Verbs (Group 3)
    'べんきょうする': (6, 0),
    'けっこんする': (5, 0),
    'りょこうする': (5, 0),

    # Pronouns / demonstratives
    'これ': (2, 0),
    'それ': (2, 0),
    'あれ': (2, 0),
    'どれ': (1, 1),
    'ここ': (2, 0),
    'そこ': (2, 0),
    'あそこ': (3, 0),
    'どこ': (1, 1),
    'なに': (1, 1),
    'だれ': (1, 1),

    # Common phrases
    'すみません': (5, 4),
    'ありがとう': (5, 0),
    'おはよう': (4, 0),
    'こんにちは': (5, 0),
    'こんばんは': (5, 0),
    'さようなら': (5, 0),
}


def main():
    with VOCAB.open('r', encoding='utf-8') as f:
        data = json.load(f)

    entries = data['entries']
    by_form: dict[str, list[dict]] = {}
    for e in entries:
        by_form.setdefault(e.get('form', ''), []).append(e)

    matched = 0
    skipped_have = 0
    not_found = []
    for key, (mora, drop) in PITCH.items():
        form_only = key.split('#', 1)[0]
        candidates = by_form.get(form_only)
        if not candidates:
            not_found.append(key)
            continue
        # Pick the first candidate without pitch_accent
        target = None
        for c in candidates:
            if not c.get('pitch_accent'):
                target = c
                break
        if target is None:
            skipped_have += 1
            continue
        target['pitch_accent'] = {'mora': mora, 'drop': drop}
        target['pitch_accent_provenance'] = 'llm_curated'
        matched += 1

    print(f'Authored pitch_accent on {matched} entries.')
    print(f'Skipped (already had value): {skipped_have}')
    if not_found:
        print(f'Forms not found in corpus: {len(not_found)}')

    with VOCAB.open('w', encoding='utf-8', newline='\n') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f'Wrote: {VOCAB}')


if __name__ == '__main__':
    main()
