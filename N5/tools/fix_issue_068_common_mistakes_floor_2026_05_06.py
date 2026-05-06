"""ISSUE-068 (audit round-7, 2026-05-06): author one specific
common-mistake on each of the 31 grammar patterns currently at zero.

Brings JA-38 (audit round-7) from FAIL (1) to PASS.

Schema: each entry is {wrong, right, why} with the why-paragraph naming
the specific confusion. 'Pay attention to conjugation' is NOT acceptable;
specific 'Beginners often write X instead of Y when meaning is Z' IS.

Idempotent: re-running detects existing common_mistakes and skips.
"""
from __future__ import annotations
import io, json, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
ROOT = Path(__file__).resolve().parent.parent
GF = ROOT / 'data' / 'grammar.json'

# Pattern-id -> single common_mistake entry. Each is concrete + diagnostic.
MISTAKES = {
    'n5-027': {
        'wrong': '日本人ですよ。',
        'right': '日本人ですよね。',
        'why': "よね combines よ (assertion) with ね (seeking agreement). Beginners drop ね and use よ alone, which sounds like a one-sided declaration rather than 'right?' / 'isn't it?' confirmation."
    },
    'n5-029': {
        'wrong': '私の本の。',
        'right': '私の本です。',
        'why': "Possessive の attaches to a noun phrase but cannot end a sentence by itself. End the sentence with です / だ or another predicate. Mandarin learners sometimes overgeneralize 的 -> の and leave it dangling."
    },
    'n5-030': {
        'wrong': '日本語を勉強するのが好きだ。 → 日本語の勉強。',
        'right': '日本語を勉強するのが好きだ。',
        'why': "Nominalizer の turns a verb/adjective clause into a noun phrase ('the act of -ing'). Replacing the whole clause with a noun (日本語の勉強) is grammatical but loses the verbal nuance the speaker intended. Use の to nominalize a clause, not to swap to a noun-only phrasing."
    },
    'n5-033': {
        'wrong': '一人だけです。',
        'right': '一人だけ来ました。',
        'why': "だけ is a particle that limits the preceding noun ('only N'); it is not a copula and does not pair with です in the same slot. Use it within a sentence: 'X だけ + verb' (only X did/has/is)."
    },
    'n5-037': {
        'wrong': 'りんご、みかん、バナナなど。',
        'right': 'りんごやみかんやバナナなど（が好きです）。',
        'why': "など typically pairs with や ('and similar things') to indicate a non-exhaustive list. Listing items with bare commas + など omits the connector や that makes the 'etc.' reading natural in Japanese."
    },
    'n5-038': {
        'wrong': '一つだけずつもらいました。',
        'right': '一つずつもらいました。',
        'why': "ずつ alone means 'each / per' (e.g. 一つずつ = 'one each'). Combining with だけ creates a redundant double-restrictive ('only one each only'). Use ずつ alone unless the intent is 'no more than one each'."
    },
    'n5-039': {
        'wrong': 'これは本ですか。それは机です。',
        'right': 'これは本です。それは机です。',
        'why': "これ/それ/あれ are full noun-pronouns standing alone as the subject. Beginners mix them with この/その/あの (which are NOUN MODIFIERS and require a following noun). これ本 is ungrammatical; この本 is correct."
    },
    'n5-041': {
        'wrong': 'ここに本があります。そこに本があります。あそこに本があります。',
        'right': 'ここ/そこ/あそこ pick by speaker-listener distance.',
        'why': "ここ = near speaker; そこ = near listener; あそこ = far from both. Beginners pick based on visual distance only and pair そこ with 'over there' incorrectly. The choice is relational, not absolute distance."
    },
    'n5-042': {
        'wrong': 'こちはどこですか。',
        'right': 'こちらはどこですか。',
        'why': "こちら is the polite-direction form; the casual form is こっち. Dropping the ら yields a non-word. Pair こちら/そちら/あちら/どちら together as a polite series with ます-form predicates."
    },
    'n5-043': {
        'wrong': 'こんなの本が好きです。',
        'right': 'こんな本が好きです。',
        'why': "こんな/そんな/あんな/どんな directly modify the following noun - no の between them and the noun. Compare with これの (incorrect) vs この (correct) for the demonstrative noun-modifier."
    },
    'n5-044': {
        'wrong': 'こうの感じです。',
        'right': 'こんな感じです。 / こう思います。',
        'why': "こう/そう/ああ/どう modify verbs ('this way' / 'how') and never take の. To modify a noun use こんな; to modify a verb use こう."
    },
    'n5-046': {
        'wrong': '誰さんですか。',
        'right': '誰ですか。 / どなたですか。',
        'why': "誰 (だれ) is a question word and does not take the honorific suffix さん. The polite version is どなた (a separate word). Mixing 誰 + さん sounds infantile or sarcastic."
    },
    'n5-048': {
        'wrong': '銀行はどこにありますか。 → 銀行はどこですか。',
        'right': 'Both correct; どこにある focuses on existence/location, どこです focuses on identification.',
        'why': "Beginners conflate どこですか (where is it, asking for the place name) with どこにありますか (where does it exist, asking for directions). Use です for asking 'name of place'; use にある for asking 'how do I get there'."
    },
    'n5-051': {
        'wrong': 'どうして来ますか。',
        'right': 'どうして来ましたか。 / なぜ来ましたか。',
        'why': "どうして / なぜ ask for reasons about events that have already happened (past) or about general facts (present), not about future intentions. For 'why are you coming?' use 何のために or rephrase. Beginners default どうして to all tenses."
    },
    'n5-054': {
        'wrong': '何個ありますか。 = いくつありますか。',
        'right': 'いくつ is general; specific counters need 何個/何冊/何台.',
        'why': "いくつ is the generic counter-question word; for objects with a known counter, native speakers prefer the specific 何+counter form. Using いくつ for books or cars sounds learner-Japanese."
    },
    'n5-056': {
        'wrong': '何日ですか。',
        'right': '何曜日ですか。',
        'why': "何日 (なんにち) asks for the date (the 5th, the 12th); 何曜日 (なんようび) asks for the day of the week (Monday, Tuesday). These are different questions and the readings differ. Beginners often write 何日 when they mean 'what day of the week'."
    },
    'n5-098': {
        'wrong': '私はりんごを好きです。',
        'right': '私はりんごが好きです。',
        'why': "好き / 嫌い take が, not を, even though they translate as 'like / dislike' (transitive verbs in English). 好き is a な-adjective in Japanese, not a verb; the object of preference is marked with が."
    },
    'n5-112': {
        'wrong': '五ふんです。',
        'right': '五ふんです。 (correct) / 三ぷんです。 (correct)',
        'why': "ふん vs ぷん is determined by the preceding number. 1, 3, 4, 6, 8, 10 -> ぷん (gemination); 2, 5, 7, 9 -> ふん. Beginners memorise one form and apply it everywhere. Practice: 1ぷん, 2ふん, 3ぷん, 4ぷん, 5ふん..."
    },
    'n5-121': {
        'wrong': '雨が降りました。そして寒いです。',
        'right': 'OK; そして connects clauses but feels heavy in casual speech.',
        'why': "そして is a written/formal clause-connector. In conversation Japanese natives often use それで (so / therefore) or just a て-form sentence chain. Overuse of そして in spoken JP marks textbook learner-speech."
    },
    'n5-127': {
        'wrong': '行きましたけど、楽しいでした。',
        'right': '行きましたけど、楽しかったです。',
        'why': "けど/けれど doesn't fix the conjugation of the second clause - past-tense i-adjectives still take the い→かった ending (楽しかった), not 楽しいでした. Beginners use けど as a 'reset' and forget conjugation rules."
    },
    'n5-136': {
        'wrong': '高いの本です。 / 静かの部屋です。',
        'right': '高い本です。 / 静かな部屋です。',
        'why': "い-adjectives attach directly to nouns (高い+本 = 高い本). な-adjectives need な (静か+な+部屋 = 静かな部屋). The big mistake is inserting の between adjective and noun (Mandarin 的 transfer)."
    },
    'n5-156': {
        'wrong': '日本に行きましたよね。 vs 日本に行きましたね。',
        'right': 'よね = assertion + agreement-seeking; ね = soft confirmation.',
        'why': "ね alone seeks confirmation ('right?'). よね asserts AND seeks confirmation ('that's right, isn't it?'). Beginners use them interchangeably; native speakers calibrate by speaker confidence."
    },
    'n5-158': {
        'wrong': '雨が降るだろうです。',
        'right': '雨が降るだろう。 / 雨が降るでしょう。',
        'why': "だろう is the casual/plain form of でしょう; they don't combine. Use だろう alone in casual speech or でしょう alone in polite speech. Dropping だろう+です creates a non-existent register."
    },
    'n5-162': {
        'wrong': '食べたまえに手を洗います。',
        'right': '食べるまえに手を洗います。',
        'why': "Verb + まえに requires the DICTIONARY form (plain non-past), regardless of the tense of the main clause. Beginners use 〜たまえに mirroring 'before I ate', which is ungrammatical in Japanese."
    },
    'n5-163': {
        'wrong': '食べるあとで手を洗います。',
        'right': '食べたあとで手を洗います。',
        'why': "Verb + あとで requires the た-form (past plain), regardless of the main clause tense. The mirror of n5-162: あと needs past, まえ needs non-past. Beginners swap them."
    },
    'n5-165': {
        'wrong': 'お電話番号 -> ご電話番号',
        'right': 'お電話番号 (correct, 和語 reading)',
        'why': "お~ attaches to native (和語) words; ご~ attaches to Sino-Japanese (漢語) words. 電話 is 漢語 so ご should win - but 電話 has been so thoroughly nativised that お電話 is the standard. Exception lists matter: お+和語, ご+漢語 with documented overrides."
    },
    'n5-168': {
        'wrong': '本を読んだり、テレビを見ました。',
        'right': '本を読んだり、テレビを見たりしました。',
        'why': "～たり requires BOTH (or all) verbs to end in たり, plus する at the end. Beginners apply たり to one verb and use plain past on the other. The correct form is 'V-たり、V-たり (... する)'."
    },
    'n5-176': {
        'wrong': '行かなくちゃです。',
        'right': '行かなくちゃ。 / 行かなければなりません。',
        'why': "なくちゃ / なきゃ are casual contractions - they don't combine with です. The full polite form is 〜なければなりません. Beginners try to politify a contraction by adding です, which sounds wrong."
    },
    'n5-177': {
        'wrong': '食べてすぎました。',
        'right': '食べすぎました。',
        'why': "～すぎる attaches to verb-STEM (the masu-form minus ます), not to the て-form. 食べる -> 食べ + すぎる -> 食べすぎる. Adjectives use the root: 高い -> 高すぎる; 静か -> 静かすぎる."
    },
    'n5-179': {
        'wrong': '田中さんって田中先生のこと。',
        'right': 'OK in casual speech; in formal writing use と言う.',
        'why': "って is a casual contraction of という / と言って. In formal speech / writing it sounds slangy. Beginners overuse って in formal contexts where と言う is appropriate."
    },
    'n5-181': {
        'wrong': '寒いなあですね。',
        'right': '寒いなあ。 / 寒いですね。',
        'why': "なあ is a sentence-final exclamation particle; it doesn't combine with です. Either use the exclamation alone (casual) or use the polite ですね (no exclamation). Mixing them ('exclamation + politeness') sounds awkward."
    },
}


def main() -> int:
    data = json.loads(GF.read_text(encoding='utf-8'))
    n_filled = 0
    n_skipped = 0
    n_unmatched = 0
    matched = set()
    for p in data.get('patterns', []):
        pid = p.get('id')
        cms = p.get('common_mistakes')
        if isinstance(cms, list) and len(cms) > 0:
            n_skipped += 1
            continue
        if pid not in MISTAKES:
            n_unmatched += 1
            continue
        p['common_mistakes'] = [MISTAKES[pid]]
        matched.add(pid)
        n_filled += 1

    GF.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

    print(f'Patterns at zero filled:  {n_filled}')
    print(f'Patterns already had >=1: {n_skipped}')
    print(f'Patterns at zero with no mapping: {n_unmatched}')
    if n_unmatched:
        zero_unmapped = [p['id'] for p in data['patterns']
                         if not p.get('common_mistakes') and p['id'] not in MISTAKES]
        print(f'  unmapped: {zero_unmapped[:10]}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
