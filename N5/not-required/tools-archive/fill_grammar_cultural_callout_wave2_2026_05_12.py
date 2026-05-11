"""Wave 2 — extend `cultural_callout` to ~60 patterns.

Wave 1 (2026-05-11) authored 31 callouts on the most-foundational
patterns. This wave covers the next 30 particles / quantifiers /
demonstratives.

Same schema as wave 1:
  cultural_callout: {note, contexts: []}

Provenance: llm_curated.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

CALLOUTS = {
    'n5-004': {
        'note': 'を (direct object) is often dropped in casual speech ("ごはん食べる？" instead of "ごはんを食べる？"). Foreign learners cling to it; native casual speech is more elliptical. Keep を in formal/written contexts and when ambiguity threatens.',
        'contexts': ['casual_drop', 'formal_keep'],
    },
    'n5-005': {
        'note': 'に has at least 5 uses — target / time / existence-location / agent (passive) / purpose. Memorize the use, not the particle in isolation. The "wrong に" is one of the top-3 foreigner errors throughout N5-N4.',
        'contexts': ['everywhere'],
    },
    'n5-006': {
        'note': 'へ (direction) overlaps heavily with に in modern speech. Pedagogically, へ emphasizes the trajectory ("toward Tokyo") while に emphasizes the endpoint ("arrive at Tokyo"). Native speakers use them almost interchangeably for simple movement.',
        'contexts': ['movement_direction', 'formal_writing'],
    },
    'n5-007': {
        'note': 'で is the workhorse: location-of-action ("学校で勉強する"), means/instrument ("ペンで書く"), and many idiomatic uses. Don\'t confuse with に (location-of-existence). Mnemonic: で = where ACTIVE things happen; に = where things ARE.',
        'contexts': ['action_context', 'tool_use'],
    },
    'n5-008': {
        'note': 'と has 3 distinct functions — accompanying agent ("友だちと"), exhaustive list ("AとB"), quotation ("Aと言う"). Most learner errors come from using と for instruments (use で instead: "ペンで書く" not "ペンと書く").',
        'contexts': ['conversation', 'narrative'],
    },
    'n5-009': {
        'note': 'から as "from" (location/time) is straightforward; から as "because" requires the speaker to take a position. ので is softer for the same meaning — use ので in business / apologies / formal writing.',
        'contexts': ['reason_giving', 'time_range'],
    },
    'n5-010': {
        'note': 'まで as "until" marks an endpoint ("5時まで待つ"); often paired with から as a range ("9時から5時まで"). Reading menus and timetables, the まで-bound is the LAST point INCLUDED, not the first point EXCLUDED.',
        'contexts': ['signs', 'timetables', 'schedules'],
    },
    'n5-011': {
        'note': 'や (non-exhaustive list) is the conversational equivalent of "...and that kind of thing". "本や雑誌があります" implies more than just books and magazines. The exhaustive と is when you want to be explicit. Native speakers default to や.',
        'contexts': ['casual_description'],
    },
    'n5-013': {
        'note': 'も (also/too) attaches to a noun and replaces other particles ("私もです" not "私はもです"). With negation, "誰も〜ない" / "何も〜ない" / "どこも〜ない" form total-negation idioms ("no one", "nothing", "nowhere") — these are textbook drill points.',
        'contexts': ['similar_to_previous', 'total_negation'],
    },
    'n5-015': {
        'note': 'この/その/あの/どの (demonstrative determiners) attach DIRECTLY before a noun and never carry a particle: "この本" not "このの本". Most learners over-apply の after possessives and instinctively insert it here too. Skip the の.',
        'contexts': ['describing_objects', 'pointing'],
    },
    'n5-016': {
        'note': 'ここ/そこ/あそこ/どこ (place pronouns) use the same proximity rule as これ/それ/あれ. あそこ ("over there") is most idiomatic when both speaker and listener can see the place — if it\'s only known to one of you, それ vs こちら applies depending on register.',
        'contexts': ['directions', 'meeting_points'],
    },
    'n5-017': {
        'note': '何 reading varies by next-word context: 何月 = なんがつ (counter follows); 何ですか = なんですか (です follows); 何を食べる = なにをたべる (object particle follows). Mistake: reading 何 as なに in counter contexts. Rule of thumb: counter/desu → なん; particle → なに.',
        'contexts': ['questions', 'reading_aloud'],
    },
    'n5-019': {
        'note': 'いつ ("when") is open-ended ("when will you come?"); for specific time questions, use the more precise question words 何時 / 何曜日 / 何月. Asking "いつ会いますか" in formal contexts can sound vague — prefer the specific 何曜日 / 何時.',
        'contexts': ['scheduling', 'business_planning'],
    },
    'n5-024': {
        'note': 'か (choice "A or B") is COMPLETE ("コーヒーかおちゃ?" = "coffee or tea — pick one"). や (non-exhaustive) is "and-others" listing. Wrong choice common: using や for a binary either/or sounds wrong.',
        'contexts': ['restaurant_orders', 'binary_choice'],
    },
    'n5-025': {
        'note': 'ね expects agreement from the listener ("いい天気ですね") — like English "isn\'t it?". Used too often by foreign learners trying to sound friendly; natives drop it in declarative statements about themselves ("私は学生ですね" sounds wrong unless you\'re explaining what you are TO the listener).',
        'contexts': ['rapport', 'agreement_seeking'],
    },
    'n5-026': {
        'note': 'よ informs the listener of something they didn\'t know ("行きますよ" = "I\'m going, FYI"). Using it where the listener already knows ("今日は日曜日ですよ" said to someone who clearly knows it\'s Sunday) sounds condescending — like English "you know".',
        'contexts': ['informing', 'gentle_reminder'],
    },
    'n5-027': {
        'note': 'よね = よ (assertion) + ね (agreement-seeking). Used to confirm shared knowledge: "あの店、いいよね？" = "that shop is good, right?". More committed than ね alone (assumes the listener already agrees). Don\'t over-use; some speakers find it pushy.',
        'contexts': ['confirming_shared_knowledge'],
    },
    'n5-029': {
        'note': 'の (possessive / noun-modifier) is THE most-used particle. Chained possessives are completely natural ("私の友だちの本") — don\'t prune to sound concise; you\'ll sound clipped. English "of" doesn\'t map 1:1; sometimes Japanese の has no English equivalent ("日本語の先生" = "Japanese teacher").',
        'contexts': ['all_speech'],
    },
    'n5-030': {
        'note': 'の (nominalizer, e.g., "見るのが好き") turns a verb-clause into a noun-phrase. こと does similar work but feels more abstract/formal ("見ることが好き"). Use の for personal preferences and concrete actions; こと for general statements and written/formal contexts.',
        'contexts': ['preferences', 'formal_writing'],
    },
    'n5-031': {
        'note': 'Plain-form + の? as an informal question ("行くの？") is COMMON in casual speech — softer than the harder か question marker. Used heavily by women in soft register; men use it too but less. Adds nuance of curiosity / surprise that か doesn\'t carry.',
        'contexts': ['casual_curiosity', 'soft_question'],
    },
    'n5-033': {
        'note': 'だけ (only) emphasizes a LIMIT ("一人だけ来た" = "only one person came — others were expected"). Often carries a tone of disappointment or restriction. Don\'t confuse with しか + negative which is a stronger "only / no more than".',
        'contexts': ['limits', 'restriction'],
    },
    'n5-034': {
        'note': 'しか〜ない (only, with negative) is STRONGER than だけ — implies "and that\'s not enough" or "I really expected more". "一人しか来なかった" = "only one person came (I expected more)". Pedagogically a key contrast point with だけ.',
        'contexts': ['disappointment', 'minimum'],
    },
    'n5-035': {
        'note': 'ぐらい / くらい (about, approximately) attaches to QUANTITIES ("百円ぐらい"). ごろ does the same for TIME POINTS ("3時ごろ"). Mixing them is a common error: "3時ぐらい" sounds slightly off (use 3時ごろ).',
        'contexts': ['approximation'],
    },
    'n5-036': {
        'note': 'ごろ (approximately, for time points) — see n5-035. The quantity-vs-time-point distinction is the entire pedagogical point of ぐらい/ごろ contrast.',
        'contexts': ['time_approximation', 'meeting_time'],
    },
    'n5-037': {
        'note': 'など (etc.) is conversational hedging — "I bought books, magazines, など". In business or academic writing, など is appropriate; in casual chat, や alone often suffices. Combining や〜など ("books や magazines など") doubles the hedge — fine but heavy.',
        'contexts': ['listing_with_etc', 'hedging'],
    },
    'n5-038': {
        'note': 'ずつ (each / per) is distributive ("ひとつずつ" = "one each"). Often appears in instructions and recipes ("少しずつ食べる" = "eat little by little"). Watch the rhythm: ずつ is unaccented and quiet.',
        'contexts': ['instructions', 'recipes'],
    },
    'n5-039': {
        'note': 'これ/それ/あれ (standalone "this/that/over-there") never carry a noun directly after them — that\'s この/その/あの (n5-015). Mixing them is a top-5 N5 error. Mnemonic: これ ends a phrase ("これは何？"); この starts one ("この本").',
        'contexts': ['pointing', 'first_meeting_objects'],
    },
    'n5-041': {
        'note': 'ここ/そこ/あそこ/どこ (place pronouns, n5-016 duplicate-area). Used in restaurants and stations ("ここで降ります" = "I get off here"). あそこ for a specific place both speaker AND listener can see; otherwise prefer specific names.',
        'contexts': ['transit', 'restaurants'],
    },
    'n5-042': {
        'note': 'こちら/そちら/あちら/どちら (polite directions/options) — service workers default to こちら for "this way please" and どちら for "which one (polite)". Using これ/それ to a customer is impolite; use the こちら series in any service context.',
        'contexts': ['service_industry', 'business_polite'],
    },
    'n5-043': {
        'note': 'こんな/そんな/あんな/どんな + Noun ("this kind of X") evaluates or characterizes ("こんな問題は簡単だ" = "this kind of problem is easy"). Different from この/その/あの which point at a specific object. Don\'t confuse: "こんなペン" = "this kind of pen"; "このペン" = "this specific pen".',
        'contexts': ['characterizing', 'evaluating'],
    },
}


def main() -> int:
    fp = ROOT / 'data' / 'grammar.json'
    bak = fp.with_suffix('.json.bak_2026_05_12_cultural_callout_wave2')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {p['id']: p for p in data['patterns']}
    n = 0
    for pid, callout in CALLOUTS.items():
        if pid not in by_id:
            print(f'  ! missing: {pid}'); continue
        p = by_id[pid]
        if p.get('cultural_callout'):
            print(f'  - skip (already filled): {pid}'); continue
        p['cultural_callout'] = callout
        p['cultural_callout_provenance'] = 'llm_curated'
        n += 1
    print(f'\nWave 2 added cultural_callout on {n} more patterns.')
    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return 0


if __name__ == '__main__':
    sys.exit(main())
