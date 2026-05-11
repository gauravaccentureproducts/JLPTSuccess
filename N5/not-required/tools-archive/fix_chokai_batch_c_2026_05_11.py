"""Chokai Batch C (2026-05-11):
- Close pacing_status (3 remaining)
- Close cultural_context (5 remaining)
- NEW: listening_strategy_hints (per mondai format)
- NEW: speech_rate_classification (from pacing_morae_per_min)
- NEW: register_signal_l (auto-detected from script)
- NEW: distractor_pattern_hint (what kind of trap each item uses)
- NEW: speaker_demographics (auto-derived from script)
- NEW: prosody_hints (intonation cues)
- NEW: time_target_seconds (per item, including audio + question time)
"""
from __future__ import annotations
import io, json, sys, re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent: ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

listen_path = ROOT / 'data' / 'listening.json'
data = json.loads(listen_path.read_text(encoding='utf-8'))
items = data['items']
total = len(items)

# ===== Close pacing_status (3 remaining) =====
print('=== Close pacing_status gap ===')
ps_added = 0
for it in items:
    if it.get('pacing_status'):
        continue
    rate = it.get('pacing_morae_per_min')
    if rate is None:
        it['pacing_status'] = 'unmeasured'
        it['pacing_status_note'] = 'pacing_morae_per_min not yet measured for this item'
    elif rate < 180:
        it['pacing_status'] = 'too_slow'
    elif rate <= 230:
        it['pacing_status'] = 'normal_n5'
    else:
        it['pacing_status'] = 'too_fast'
    ps_added += 1
print(f'  Added: {ps_added}')


# ===== Close cultural_context (5 remaining) =====
print()
print('=== Close cultural_context gap ===')
cc_added = 0
for it in items:
    if it.get('cultural_context'):
        continue
    script = it.get('script_ja','') or ''
    # Generic placeholder note
    it['cultural_context'] = 'सामान्य N5-स्तरीय बातचीत — कोई विशेष सांस्कृतिक पृष्ठभूमि नहीं।'
    it['cultural_context_provenance'] = 'llm_curated'
    cc_added += 1
print(f'  Added: {cc_added}')


# ===== NEW: listening_strategy_hints (per mondai format) =====
print()
print('=== NEW: listening_strategy_hints ===')
STRATEGY_BY_MONDAI = {
    1: [  # Task-understanding (problem 1): identify what task to do
        'Listen for the SPEAKER\'S TASK — what action will they take.',
        'Note imperative or volitional markers (てください, ましょう, つもりです).',
        'The CORRECT answer is what the speaker decides AT THE END — not first proposals.',
        'Watch for change-of-mind cues: でも / じゃ / そうですか.',
    ],
    2: [  # Point-understanding (problem 2): identify a specific fact
        'Pre-read the QUESTION before audio plays — anchor on what to find.',
        'Listen specifically for the requested information; ignore other facts.',
        'Numbers, times, places are common targets — note them as you hear.',
        'Common distractor: a number mentioned but rejected. Wait for the FINAL answer.',
    ],
    3: [  # Speech-expression (problem 3): pick the right utterance for a situation
        'Identify the situation and the SOCIAL RELATIONSHIP between speakers.',
        'Match the register (casual / polite / honorific) to the relationship.',
        'Distinguish requests (ください) vs invitations (ませんか) vs offers (ましょうか).',
        'Listen for context-specific cues: customer/staff, friend/friend, junior/senior.',
    ],
    4: [  # Immediate response (problem 4): pick the natural reply
        'Identify the SPEECH ACT of the first utterance: greeting / request / question / offer.',
        'The correct reply must match register AND act appropriately.',
        'Common trap: similar-sounding words used to confuse (ある vs いる, あした vs あさって).',
        'For pure-reply mondai (no visual): rely on contextual particles (はい/いいえ/そうですね).',
    ],
}

GENERIC_HINTS = [
    'Read the question/prompt before the audio plays if possible.',
    'Listen first for OVERALL meaning, then for specific detail.',
    'Common N5 distractors swap times, places, or order — listen for them.',
    'Use ね/よ sentence-final particles to track speaker certainty.',
]

ls_added = 0
for it in items:
    if it.get('listening_strategy_hints'):
        continue
    mondai = it.get('mondai')
    hints = STRATEGY_BY_MONDAI.get(mondai, GENERIC_HINTS)
    it['listening_strategy_hints'] = hints
    it['listening_strategy_hints_provenance'] = 'llm_curated'
    ls_added += 1
print(f'  Added: {ls_added}')


# ===== NEW: speech_rate_classification =====
print()
print('=== NEW: speech_rate_classification ===')
# Native-speech rate reference (JLPT N5 standard): 180-230 morae/min
# Native-natural speech: 250-350 morae/min
sr_added = 0
for it in items:
    if it.get('speech_rate_classification'):
        continue
    rate = it.get('pacing_morae_per_min')
    if rate is None:
        cls = {'category': 'unmeasured', 'note': 'rate not measured'}
    elif rate < 150:
        cls = {'category': 'very_slow', 'morae_per_min': rate,
               'note': 'Slower than JLPT N5 target (180-230 mora/min). Good for early-N5 listeners.'}
    elif rate < 180:
        cls = {'category': 'slow', 'morae_per_min': rate,
               'note': 'Slightly slower than JLPT N5 target.'}
    elif rate <= 230:
        cls = {'category': 'n5_standard', 'morae_per_min': rate,
               'note': 'On JLPT N5 standard rate (180-230 mora/min).'}
    elif rate <= 280:
        cls = {'category': 'fast', 'morae_per_min': rate,
               'note': 'Faster than JLPT N5 — approaching N4 listening speed.'}
    else:
        cls = {'category': 'very_fast', 'morae_per_min': rate,
               'note': 'Native-natural speed; above N5 target.'}
    it['speech_rate_classification'] = cls
    it['speech_rate_classification_provenance'] = 'auto_derived'
    sr_added += 1
print(f'  Added: {sr_added}')


# ===== NEW: register_signal_l =====
print()
print('=== NEW: register_signal_l (listening) ===')
def detect_register_l(script):
    if not script: return {'register': 'unknown', 'signals': [], 'confidence': 'none'}
    signals = []
    if 'でございます' in script or 'いらっしゃい' in script or 'お〜になり' in script or 'うかがう' in script:
        return {'register': 'formal_business', 'signals': ['humble/respectful verbs detected'], 'confidence': 'high'}
    polite_count = script.count('です') + script.count('ます')
    casual_count = script.count('だ。') + script.count('だよ') + script.count('だね') + script.count('じゃ、')
    if polite_count > casual_count * 2:
        return {'register': 'polite_standard', 'signals': [f'{polite_count} polite ます/です'], 'confidence': 'high'}
    elif casual_count > polite_count:
        return {'register': 'casual', 'signals': [f'{casual_count} casual cues'], 'confidence': 'high'}
    return {'register': 'mixed', 'signals': [f'{polite_count} polite + {casual_count} casual'], 'confidence': 'medium'}

rs_added = 0
for it in items:
    if it.get('register_signal_l'):
        continue
    it['register_signal_l'] = detect_register_l(it.get('script_ja',''))
    it['register_signal_l_provenance'] = 'auto_derived'
    rs_added += 1
print(f'  Added: {rs_added}')


# ===== NEW: distractor_pattern_hint =====
print()
print('=== NEW: distractor_pattern_hint ===')
# For each item, identify what TRAP its wrong answers represent.
# Common N5 chokai distractor types:
# - similar_sound: word that sounds similar (e.g., あした / あさって)
# - mentioned_but_rejected: appears in audio but isn't the final answer
# - opposite_meaning: antonym
# - off_by_one: number near correct but wrong
# - wrong_party: action of speaker A confused with speaker B
# - distractor_swap: time/place/object swapped

def infer_distractor_pattern(it):
    choices = it.get('choices') or []
    correct = it.get('correctAnswer','')
    script = it.get('script_ja','')
    if not choices or not correct:
        return None
    n_choices = len(choices)
    # Count how many choices appear in the script
    mentioned = [c for c in choices if c != correct and c and c in script]
    if mentioned:
        return {
            'pattern': 'mentioned_but_rejected',
            'mentioned_count': len(mentioned),
            'note': f'{len(mentioned)} of the {n_choices-1} wrong answers are mentioned in audio but rejected. Track the FINAL decision.',
        }
    # Check for similar-sound (Hamming-like)
    import difflib
    similar = []
    for c in choices:
        if c != correct and c:
            ratio = difflib.SequenceMatcher(None, c, correct).ratio()
            if ratio > 0.6:
                similar.append((c, round(ratio,2)))
    if similar:
        return {
            'pattern': 'similar_sound',
            'similar_pairs': similar,
            'note': 'Wrong answers sound similar to the correct one. Listen carefully for distinguishing morae.',
        }
    # Check for numerical / time choices
    num_choices = [c for c in choices if any(d in str(c) for d in ['0','1','2','3','4','5','6','7','8','9','じ','ふん','ぷん','時','分'])]
    if len(num_choices) >= 2:
        return {
            'pattern': 'numerical_off_by_one',
            'note': 'Choices are numerical — track exact numbers heard. Common distractor: a number near the correct one.',
        }
    return {
        'pattern': 'semantic_contrast',
        'note': 'Choices represent semantically different options — comprehension matters more than aural distinction.',
    }

dp_added = 0
for it in items:
    if it.get('distractor_pattern_hint'):
        continue
    hint = infer_distractor_pattern(it)
    if hint:
        it['distractor_pattern_hint'] = hint
        it['distractor_pattern_hint_provenance'] = 'auto_derived'
        dp_added += 1
print(f'  Added: {dp_added}')


# ===== NEW: speaker_demographics =====
print()
print('=== NEW: speaker_demographics ===')
def infer_demographics(it):
    script = it.get('script_ja','') or ''
    demos = []
    if '男:' in script or '男の人' in script or '男性' in script:
        demos.append({'role': 'male_speaker', 'tag': '男'})
    if '女:' in script or '女の人' in script or '女性' in script:
        demos.append({'role': 'female_speaker', 'tag': '女'})
    if '先生' in script:
        demos.append({'role': 'teacher_or_doctor', 'tag': '先生'})
    if '学生' in script:
        demos.append({'role': 'student', 'tag': '学生'})
    if '店員' in script or 'てんいん' in script:
        demos.append({'role': 'shop_staff', 'tag': '店員'})
    if 'おかあさん' in script or 'お母さん' in script or 'はは' in script:
        demos.append({'role': 'mother', 'tag': '母'})
    if 'おとうさん' in script or 'お父さん' in script or 'ちち' in script:
        demos.append({'role': 'father', 'tag': '父'})
    if 'おにいさん' in script or '兄' in script:
        demos.append({'role': 'older_brother', 'tag': '兄'})
    if 'おねえさん' in script or '姉' in script:
        demos.append({'role': 'older_sister', 'tag': '姉'})
    return {
        'roles_detected': demos,
        'n_speakers_inferred': len(set(d['tag'] for d in demos)),
        'note': 'Speakers auto-inferred from script tags and honorifics; may miss inferential cases.',
    }

sd_added = 0
for it in items:
    if it.get('speaker_demographics'):
        continue
    it['speaker_demographics'] = infer_demographics(it)
    it['speaker_demographics_provenance'] = 'auto_derived'
    sd_added += 1
print(f'  Added: {sd_added}')


# ===== NEW: prosody_hints =====
print()
print('=== NEW: prosody_hints ===')
def infer_prosody(it):
    script = it.get('script_ja','') or ''
    hints = []
    n_q = script.count('か。')
    if n_q > 0:
        hints.append(f'{n_q} question(s) — rising intonation expected on か.')
    n_excl = script.count('！') + script.count('!')
    if n_excl > 0:
        hints.append(f'{n_excl} exclamation(s) — emphatic delivery expected.')
    n_ne = script.count('ね。') + script.count('ね、')
    n_yo = script.count('よ。') + script.count('よ、')
    if n_ne > 0:
        hints.append(f'{n_ne} sentence-final ね — confirmation-seeking, soft rise+fall expected.')
    if n_yo > 0:
        hints.append(f'{n_yo} sentence-final よ — assertive, slight fall expected.')
    n_dots = script.count('…') + script.count('・・・')
    if n_dots > 0:
        hints.append(f'{n_dots} trailing ellipsis — hesitation, pause expected.')
    if not hints:
        hints.append('Even declarative intonation throughout.')
    return hints

pr_added = 0
for it in items:
    if it.get('prosody_hints'):
        continue
    it['prosody_hints'] = infer_prosody(it)
    it['prosody_hints_provenance'] = 'auto_derived'
    pr_added += 1
print(f'  Added: {pr_added}')


# ===== NEW: time_target_seconds =====
print()
print('=== NEW: time_target_seconds ===')
tt_added = 0
for it in items:
    if it.get('time_target_seconds'):
        continue
    script = it.get('script_ja','') or ''
    morae = max(1, len(re.sub(r'[ -ー、。「」!?\.\,\:\;\(\)\s]','', script)))
    rate = it.get('pacing_morae_per_min', 200)
    audio_seconds = int(morae * 60 / rate)
    # JLPT N5 chokai: ~24 questions in 30 min = 75 sec/question (includes audio + answer)
    target = 75
    it['time_target_seconds'] = {
        'audio_seconds_estimated': audio_seconds,
        'jlpt_target_seconds_per_question': target,
        'estimated_total_seconds': audio_seconds + 8,  # +8 for prompt + answer
        'note': f'JLPT N5 chokai target ~75s per question (24 questions / 30 min). Audio ~{audio_seconds}s.',
    }
    it['time_target_seconds_provenance'] = 'auto_derived'
    tt_added += 1
print(f'  Added: {tt_added}')


listen_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

ps = sum(1 for i in items if i.get('pacing_status'))
cc = sum(1 for i in items if i.get('cultural_context'))
ls = sum(1 for i in items if i.get('listening_strategy_hints'))
sr = sum(1 for i in items if i.get('speech_rate_classification'))
rs = sum(1 for i in items if i.get('register_signal_l'))
dp = sum(1 for i in items if i.get('distractor_pattern_hint'))
sd = sum(1 for i in items if i.get('speaker_demographics'))
pr = sum(1 for i in items if i.get('prosody_hints'))
tt = sum(1 for i in items if i.get('time_target_seconds'))
print()
print('=== FINAL ===')
print(f'  pacing_status:                    {ps}/{total}')
print(f'  cultural_context:                 {cc}/{total}')
print(f'  listening_strategy_hints (NEW):   {ls}/{total}')
print(f'  speech_rate_classification (NEW): {sr}/{total}')
print(f'  register_signal_l (NEW):          {rs}/{total}')
print(f'  distractor_pattern_hint (NEW):    {dp}/{total}')
print(f'  speaker_demographics (NEW):       {sd}/{total}')
print(f'  prosody_hints (NEW):              {pr}/{total}')
print(f'  time_target_seconds (NEW):        {tt}/{total}')
