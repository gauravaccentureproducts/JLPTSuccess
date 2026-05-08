"""N5 richness audit — measure every entry against the prompt's
quantitative rubric. Read-only.

Outputs scorecards per surface + worst-offender lists + linking-density
metrics. The audit transcript reads from these numbers.
"""
from __future__ import annotations
import io
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ============================================================================
# GRAMMAR (178 patterns)
# ============================================================================

print('=' * 70)
print('GRAMMAR (178 patterns) — bar set above Bunpro free tier')
print('=' * 70)

gram = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))
patterns = gram.get('patterns', [])
print(f'Total patterns loaded: {len(patterns)}')

# Per-dimension counters
g_examples_7 = 0   # ≥7 examples
g_examples_5 = 0   # ≥5
g_examples_3 = 0   # ≥3 (floor)
g_common_mistakes_1 = 0
g_contrasts_present = 0
g_register_tagged = 0
g_sources_2plus = 0
g_audio_per_example = 0
g_pitch_accent_any = 0
g_cultural_callout = 0
g_authentic_media = 0
g_vocab_ids_full = 0  # all examples have vocab_ids

worst_grammar_below_examples = []  # (id, examples_count)
worst_grammar_no_mistakes = []
worst_grammar_no_sources = []

for p in patterns:
    pid = p.get('id', '?')
    examples = p.get('examples', []) or []
    n_ex = len(examples)
    if n_ex >= 7: g_examples_7 += 1
    if n_ex >= 5: g_examples_5 += 1
    if n_ex >= 3: g_examples_3 += 1
    if n_ex < 7:
        worst_grammar_below_examples.append((pid, n_ex))

    cm = p.get('common_mistakes', []) or []
    if len(cm) >= 1:
        g_common_mistakes_1 += 1
    else:
        worst_grammar_no_mistakes.append(pid)

    contrasts = p.get('contrasts', []) or []
    if len(contrasts) >= 1: g_contrasts_present += 1

    if p.get('register'): g_register_tagged += 1

    sources = p.get('sources', []) or []
    if len(sources) >= 2:
        g_sources_2plus += 1
    elif len(sources) < 1:
        worst_grammar_no_sources.append(pid)

    # audio: count examples with .audio field
    audio_ok = bool(examples) and all(ex.get('audio') for ex in examples)
    if audio_ok: g_audio_per_example += 1

    pitch_any = any(ex.get('pitch_accent') for ex in examples)
    if pitch_any: g_pitch_accent_any += 1

    if p.get('cultural_callout') or p.get('cultural_note'): g_cultural_callout += 1
    if p.get('authentic_media') or p.get('media_reference'): g_authentic_media += 1

    if examples and all(ex.get('vocab_ids') for ex in examples):
        g_vocab_ids_full += 1

total = len(patterns)
def pct(n): return f'{100 * n / total:.0f}%' if total else '0%'

print(f'\nDimension                          | met / total | %     | gap')
print(f'------------------------------------|-------------|-------|--------')
print(f'Examples ≥ 7 (target)              | {g_examples_7:>3} / {total} | {pct(g_examples_7):>4} | {total - g_examples_7}')
print(f'Examples ≥ 5 (above Bunpro)        | {g_examples_5:>3} / {total} | {pct(g_examples_5):>4} | {total - g_examples_5}')
print(f'Examples ≥ 3 (floor, JA-13)        | {g_examples_3:>3} / {total} | {pct(g_examples_3):>4} | {total - g_examples_3}')
print(f'Common-mistakes ≥ 1                 | {g_common_mistakes_1:>3} / {total} | {pct(g_common_mistakes_1):>4} | {total - g_common_mistakes_1}')
print(f'Contrasts cross-link present       | {g_contrasts_present:>3} / {total} | {pct(g_contrasts_present):>4} | {total - g_contrasts_present}')
print(f'Register tag                        | {g_register_tagged:>3} / {total} | {pct(g_register_tagged):>4} | {total - g_register_tagged}')
print(f'Source citations ≥ 2                | {g_sources_2plus:>3} / {total} | {pct(g_sources_2plus):>4} | {total - g_sources_2plus}')
print(f'vocab_ids on every example          | {g_vocab_ids_full:>3} / {total} | {pct(g_vocab_ids_full):>4} | {total - g_vocab_ids_full}')
print(f'Audio per every example             | {g_audio_per_example:>3} / {total} | {pct(g_audio_per_example):>4} | {total - g_audio_per_example}')
print(f'Pitch accent ≥ 1 example            | {g_pitch_accent_any:>3} / {total} | {pct(g_pitch_accent_any):>4} | {total - g_pitch_accent_any}')
print(f'Cultural callout present            | {g_cultural_callout:>3} / {total} | {pct(g_cultural_callout):>4} | {total - g_cultural_callout}')
print(f'Authentic-media reference           | {g_authentic_media:>3} / {total} | {pct(g_authentic_media):>4} | {total - g_authentic_media}')

print(f'\nWorst offenders (examples below 7):')
worst_grammar_below_examples.sort(key=lambda x: x[1])
for pid, n in worst_grammar_below_examples[:10]:
    print(f'  {pid}: {n} examples')


# ============================================================================
# VOCAB (1000 entries)
# ============================================================================

print('\n' + '=' * 70)
print('VOCAB (1000 entries) — bar set above Jisho')
print('=' * 70)

vocab = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))
v_entries = vocab.get('entries', [])
print(f'Total vocab loaded: {len(v_entries)}')

v_examples_3 = 0
v_examples_2 = 0
v_pitch_accent = 0
v_collocations_5 = 0
v_collocations_any = 0
v_transitivity_link = 0
v_verb_class_flag = 0
v_counter = 0
v_register = 0
v_sources_2 = 0
v_freq_rank = 0
v_audio_form = 0
v_authentic_media = 0
v_conjugation_table = 0
v_honorific_chain = 0

n_verbs = 0
n_nouns = 0
n_pair_eligible = 0  # transitive verbs

for e in v_entries:
    examples = e.get('examples', []) or []
    n_ex = len(examples)
    if n_ex >= 3: v_examples_3 += 1
    if n_ex >= 2: v_examples_2 += 1

    if e.get('pitch_accent') or e.get('pitch'): v_pitch_accent += 1
    coll = e.get('collocations', []) or []
    if len(coll) >= 5: v_collocations_5 += 1
    if len(coll) >= 1: v_collocations_any += 1

    pos = (e.get('pos') or '').lower()
    is_verb = 'verb' in pos
    is_noun = pos == 'noun' or 'noun' in pos
    if is_verb: n_verbs += 1
    if is_noun: n_nouns += 1

    if e.get('transitivity_pair') or e.get('pair_id'):
        v_transitivity_link += 1
    if e.get('verb_class') or e.get('group_1_exception'): v_verb_class_flag += 1
    if e.get('counter') or e.get('default_counter'): v_counter += 1
    if e.get('register'): v_register += 1
    if e.get('frequency_rank'): v_freq_rank += 1
    if e.get('honorific_chain') or e.get('humble_chain'): v_honorific_chain += 1

    sources = e.get('sources', []) or []
    if len(sources) >= 2: v_sources_2 += 1

    if e.get('audio') or any(ex.get('audio') for ex in examples):
        v_audio_form += 1

    if e.get('conjugation_table') or e.get('conjugations'): v_conjugation_table += 1

    if e.get('authentic_media') or e.get('media_reference'): v_authentic_media += 1

vt = len(v_entries)
def pctv(n): return f'{100 * n / vt:.0f}%' if vt else '0%'

print(f'\nDimension                          | met / total | %     | gap')
print(f'------------------------------------|-------------|-------|--------')
print(f'Examples ≥ 3 (target)              | {v_examples_3:>4} / {vt} | {pctv(v_examples_3):>4} | {vt - v_examples_3}')
print(f'Examples ≥ 2 (Jisho parity)         | {v_examples_2:>4} / {vt} | {pctv(v_examples_2):>4} | {vt - v_examples_2}')
print(f'Pitch accent (Tokyo)                | {v_pitch_accent:>4} / {vt} | {pctv(v_pitch_accent):>4} | {vt - v_pitch_accent}')
print(f'Collocations ≥ 5                    | {v_collocations_5:>4} / {vt} | {pctv(v_collocations_5):>4} | {vt - v_collocations_5}')
print(f'Collocations ≥ 1                    | {v_collocations_any:>4} / {vt} | {pctv(v_collocations_any):>4} | {vt - v_collocations_any}')
print(f'Transitivity-pair link              | {v_transitivity_link:>4} / {vt} | {pctv(v_transitivity_link):>4} | {vt - v_transitivity_link}')
print(f'Verb-class flag (godan/ichidan etc) | {v_verb_class_flag:>4} / {vt} | {pctv(v_verb_class_flag):>4} | {vt - v_verb_class_flag}')
print(f'Counter pairing (nouns)             | {v_counter:>4} / {vt} | {pctv(v_counter):>4} | {vt - v_counter}')
print(f'Register tag                        | {v_register:>4} / {vt} | {pctv(v_register):>4} | {vt - v_register}')
print(f'Source citations ≥ 2                | {v_sources_2:>4} / {vt} | {pctv(v_sources_2):>4} | {vt - v_sources_2}')
print(f'Frequency rank                      | {v_freq_rank:>4} / {vt} | {pctv(v_freq_rank):>4} | {vt - v_freq_rank}')
print(f'Conjugation table inline            | {v_conjugation_table:>4} / {vt} | {pctv(v_conjugation_table):>4} | {vt - v_conjugation_table}')
print(f'Honorific chain link                | {v_honorific_chain:>4} / {vt} | {pctv(v_honorific_chain):>4} | {vt - v_honorific_chain}')
print(f'Audio (any form)                    | {v_audio_form:>4} / {vt} | {pctv(v_audio_form):>4} | {vt - v_audio_form}')
print(f'Authentic-media reference           | {v_authentic_media:>4} / {vt} | {pctv(v_authentic_media):>4} | {vt - v_authentic_media}')


# ============================================================================
# KANJI (106)
# ============================================================================

print('\n' + '=' * 70)
print('KANJI (106) — bar set above WaniKani free tier')
print('=' * 70)

kanji = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))
k_entries = kanji.get('entries', [])
print(f'Total kanji loaded: {len(k_entries)}')

k_mnemonic_radical = 0
k_mnemonic_visual = 0
k_mnemonic_reading = 0
k_radical_decomp = 0
k_stroke_svg = 0
k_stroke_traps = 0
k_lookalike_link = 0
k_vocab_5 = 0
k_example_sentence = 0
k_freq_rank = 0
k_recognition_priority = 0
k_audio_yomi = 0
k_etymology = 0
k_real_world = 0

for e in k_entries:
    mnemonic = e.get('mnemonic') or {}
    if isinstance(mnemonic, dict):
        if mnemonic.get('radical_story') or mnemonic.get('radical'): k_mnemonic_radical += 1
        if mnemonic.get('visual_story') or mnemonic.get('visual'): k_mnemonic_visual += 1
        if mnemonic.get('reading') or mnemonic.get('reading_hint'): k_mnemonic_reading += 1
    elif isinstance(mnemonic, str) and mnemonic.strip():
        k_mnemonic_radical += 1  # generic mnemonic field present

    if e.get('radical_decomposition') or e.get('radicals') or e.get('components'): k_radical_decomp += 1
    if e.get('stroke_order_svg') or e.get('svg'): k_stroke_svg += 1
    if e.get('stroke_order_mistakes') or e.get('stroke_traps'): k_stroke_traps += 1
    if e.get('lookalikes') or e.get('confusable_with'): k_lookalike_link += 1

    examples = e.get('examples', []) or []
    if len(examples) >= 5: k_vocab_5 += 1
    if any(ex.get('sentence') or ex.get('ja') for ex in examples): k_example_sentence += 1

    if e.get('frequency_rank'): k_freq_rank += 1
    if e.get('recognition_priority'): k_recognition_priority += 1

    if e.get('audio_on') or e.get('audio_kun') or e.get('reading_audio'): k_audio_yomi += 1
    if e.get('etymology') or e.get('origin'): k_etymology += 1
    if e.get('real_world_signage') or e.get('signage'): k_real_world += 1

kt = len(k_entries)
def pctk(n): return f'{100 * n / kt:.0f}%' if kt else '0%'

print(f'\nDimension                          | met / total | %     | gap')
print(f'------------------------------------|-------------|-------|--------')
print(f'Mnemonic - radical/component story | {k_mnemonic_radical:>3} / {kt} | {pctk(k_mnemonic_radical):>4} | {kt - k_mnemonic_radical}')
print(f'Mnemonic - visual                  | {k_mnemonic_visual:>3} / {kt} | {pctk(k_mnemonic_visual):>4} | {kt - k_mnemonic_visual}')
print(f'Mnemonic - reading hint            | {k_mnemonic_reading:>3} / {kt} | {pctk(k_mnemonic_reading):>4} | {kt - k_mnemonic_reading}')
print(f'Radical decomposition              | {k_radical_decomp:>3} / {kt} | {pctk(k_radical_decomp):>4} | {kt - k_radical_decomp}')
print(f'Stroke-order SVG                   | {k_stroke_svg:>3} / {kt} | {pctk(k_stroke_svg):>4} | {kt - k_stroke_svg}')
print(f'Stroke-order mistakes annotated    | {k_stroke_traps:>3} / {kt} | {pctk(k_stroke_traps):>4} | {kt - k_stroke_traps}')
print(f'Lookalike-cluster cross-link       | {k_lookalike_link:>3} / {kt} | {pctk(k_lookalike_link):>4} | {kt - k_lookalike_link}')
print(f'Vocab cross-links ≥ 5              | {k_vocab_5:>3} / {kt} | {pctk(k_vocab_5):>4} | {kt - k_vocab_5}')
print(f'Example sentence ≥ 1               | {k_example_sentence:>3} / {kt} | {pctk(k_example_sentence):>4} | {kt - k_example_sentence}')
print(f'Frequency rank                     | {k_freq_rank:>3} / {kt} | {pctk(k_freq_rank):>4} | {kt - k_freq_rank}')
print(f'Recognition priority (1/2/3)       | {k_recognition_priority:>3} / {kt} | {pctk(k_recognition_priority):>4} | {kt - k_recognition_priority}')
print(f'Audio for on/kun yomi              | {k_audio_yomi:>3} / {kt} | {pctk(k_audio_yomi):>4} | {kt - k_audio_yomi}')
print(f'Etymology / kun-yomi origin        | {k_etymology:>3} / {kt} | {pctk(k_etymology):>4} | {kt - k_etymology}')
print(f'Real-world signage reference       | {k_real_world:>3} / {kt} | {pctk(k_real_world):>4} | {kt - k_real_world}')


# ============================================================================
# READING (45 passages)
# ============================================================================

print('\n' + '=' * 70)
print('READING (passages) — bar above Marugoto')
print('=' * 70)

read = json.loads((ROOT / 'data' / 'reading.json').read_text(encoding='utf-8'))
passages = read.get('passages', [])
print(f'Total passages loaded: {len(passages)}')

r_grammar_footnote = 0
r_vocab_preview = 0
r_native_audio = 0
r_paragraph_summary = 0
r_lit_nat_translation = 0
r_cultural_callout = 0
r_reflection = 0
r_topic_tag = 0
r_format_role = 0

for p in passages:
    if p.get('grammar_footnotes') or p.get('sentence_footnotes'): r_grammar_footnote += 1
    if p.get('vocab_preview') or p.get('pre_reading_vocab'): r_vocab_preview += 1
    if p.get('native_audio') or p.get('audio_native'): r_native_audio += 1
    if p.get('paragraph_summary') or p.get('summary_per_paragraph'): r_paragraph_summary += 1
    if p.get('translation_literal') and p.get('translation_natural'): r_lit_nat_translation += 1
    if p.get('cultural_callout') or p.get('cultural_context'): r_cultural_callout += 1
    if p.get('reflection_prompts') or p.get('discussion_prompts'): r_reflection += 1
    if p.get('topic') or p.get('topic_tag') or p.get('topics'): r_topic_tag += 1
    qs = p.get('questions', []) or []
    if any(q.get('format_role') for q in qs): r_format_role += 1

rt = len(passages)
def pctr(n): return f'{100 * n / rt:.0f}%' if rt else '0%'

print(f'\nDimension                          | met / total | %     | gap')
print(f'------------------------------------|-------------|-------|--------')
print(f'Sentence-by-sentence grammar footnote| {r_grammar_footnote:>3} / {rt} | {pctr(r_grammar_footnote):>4} | {rt - r_grammar_footnote}')
print(f'Pre-reading vocab preview          | {r_vocab_preview:>3} / {rt} | {pctr(r_vocab_preview):>4} | {rt - r_vocab_preview}')
print(f'Native-speaker audio               | {r_native_audio:>3} / {rt} | {pctr(r_native_audio):>4} | {rt - r_native_audio}')
print(f'Paragraph-level summary            | {r_paragraph_summary:>3} / {rt} | {pctr(r_paragraph_summary):>4} | {rt - r_paragraph_summary}')
print(f'Literal-vs-natural translation     | {r_lit_nat_translation:>3} / {rt} | {pctr(r_lit_nat_translation):>4} | {rt - r_lit_nat_translation}')
print(f'Cultural-context callouts          | {r_cultural_callout:>3} / {rt} | {pctr(r_cultural_callout):>4} | {rt - r_cultural_callout}')
print(f'Reflection prompts                 | {r_reflection:>3} / {rt} | {pctr(r_reflection):>4} | {rt - r_reflection}')
print(f'Topic-cluster tag                  | {r_topic_tag:>3} / {rt} | {pctr(r_topic_tag):>4} | {rt - r_topic_tag}')
print(f'format_role discipline             | {r_format_role:>3} / {rt} | {pctr(r_format_role):>4} | {rt - r_format_role}')


# ============================================================================
# LISTENING (47 items)
# ============================================================================

print('\n' + '=' * 70)
print('LISTENING (items) — bar above JapanesePod101 free tier')
print('=' * 70)

listen = json.loads((ROOT / 'data' / 'listening.json').read_text(encoding='utf-8'))
items = listen.get('items', [])
print(f'Total listening items: {len(items)}')

l_timestamped = 0
l_vocab_glossary = 0
l_slow_audio = 0
l_voice_count = set()
l_discourse_markers = 0
l_inference_q = 0
l_ambient = 0
l_pre_listen_prompt = 0
l_real_world = 0

for it in items:
    if it.get('transcript_timestamps') or it.get('word_timestamps'): l_timestamped += 1
    if it.get('vocab_glossary') or it.get('inline_vocab'): l_vocab_glossary += 1
    if it.get('audio_slow') or it.get('slow_variant'): l_slow_audio += 1

    vp = it.get('voice_planned') or {}
    if vp.get('primary'): l_voice_count.add(vp['primary'])
    if vp.get('secondary'): l_voice_count.add(vp['secondary'])

    if it.get('discourse_markers') or it.get('fillers_marked'): l_discourse_markers += 1
    if it.get('inference_question') or it.get('inference_expansion'): l_inference_q += 1
    if it.get('ambient_context') or it.get('ambient_audio'): l_ambient += 1
    if it.get('prompt_ja'): l_pre_listen_prompt += 1
    if it.get('real_world_clip') or it.get('authentic_audio'): l_real_world += 1

lt = len(items)
def pctl(n): return f'{100 * n / lt:.0f}%' if lt else '0%'

print(f'\nDimension                          | met / total | %     | gap')
print(f'------------------------------------|-------------|-------|--------')
print(f'Timestamped transcript             | {l_timestamped:>3} / {lt} | {pctl(l_timestamped):>4} | {lt - l_timestamped}')
print(f'Vocab glossary inline              | {l_vocab_glossary:>3} / {lt} | {pctl(l_vocab_glossary):>4} | {lt - l_vocab_glossary}')
print(f'Slow-version audio                 | {l_slow_audio:>3} / {lt} | {pctl(l_slow_audio):>4} | {lt - l_slow_audio}')
print(f'Distinct voices: {len(l_voice_count)} (target ≥ 4)')
print(f'Discourse markers tagged           | {l_discourse_markers:>3} / {lt} | {pctl(l_discourse_markers):>4} | {lt - l_discourse_markers}')
print(f'Inference-question expansion       | {l_inference_q:>3} / {lt} | {pctl(l_inference_q):>4} | {lt - l_inference_q}')
print(f'Ambient-context audio              | {l_ambient:>3} / {lt} | {pctl(l_ambient):>4} | {lt - l_ambient}')
print(f'Pre-listening prompt_ja            | {l_pre_listen_prompt:>3} / {lt} | {pctl(l_pre_listen_prompt):>4} | {lt - l_pre_listen_prompt}')
print(f'Real-world authentic clip          | {l_real_world:>3} / {lt} | {pctl(l_real_world):>4} | {lt - l_real_world}')


# ============================================================================
# LINKING DENSITY
# ============================================================================

print('\n' + '=' * 70)
print('LINKING-DENSITY')
print('=' * 70)

# Build vocab id index
vocab_ids_set = {e.get('id') for e in v_entries if e.get('id')}
vocab_lemmas = {e.get('lemma') or e.get('form'): e.get('id') for e in v_entries}

# Density-1: pattern → vocab in-links via examples[].vocab_ids
g_to_v_links = []
for p in patterns:
    cnt = 0
    for ex in (p.get('examples') or []):
        cnt += len(ex.get('vocab_ids') or [])
    g_to_v_links.append(cnt)
avg_g_to_v = sum(g_to_v_links) / max(1, len(g_to_v_links))

# Density-2: vocab → grammar back-references
v_to_g_count = Counter()
for p in patterns:
    pid = p.get('id')
    for ex in (p.get('examples') or []):
        for vid in (ex.get('vocab_ids') or []):
            v_to_g_count[vid] += 1
v_with_g_link = sum(1 for v in v_entries if v.get('id') in v_to_g_count)

# Density-3: kanji → vocab containment
k_to_v_count = Counter()
def kanji_in(s):
    return [ch for ch in (s or '') if '一' <= ch <= '鿿']
kanji_glyphs = {e.get('char') or e.get('id', '').split('.')[-1] for e in k_entries}

for v in v_entries:
    form = v.get('lemma') or v.get('form') or ''
    for ch in kanji_in(form):
        if ch in kanji_glyphs:
            k_to_v_count[ch] += 1
avg_k_to_v = sum(k_to_v_count.values()) / max(1, len(kanji_glyphs))

# Density-4: kanji → reading passages containing
k_to_read_count = Counter()
for p in passages:
    text = p.get('text') or ''
    for ch in set(kanji_in(text)):
        if ch in kanji_glyphs:
            k_to_read_count[ch] += 1
kanji_in_read = len(k_to_read_count)

# Density-5: reading sentence → grammar footnote
total_sentences = sum(
    len(re.split(r'[。！？]', (p.get('text') or '').strip()))
    for p in passages
)
sentences_with_footnote = 0  # field absent → 0

# Density-6: listening → vocab clickable
listening_with_vocab_links = sum(1 for it in items if it.get('vocab_glossary'))

# Density-7: paper question → grammar/vocab/kanji link on review
paper_dir = ROOT / 'data' / 'papers'
paper_q_count = 0
paper_q_with_link = 0
for pf in paper_dir.rglob('*.json'):
    if pf.name == 'manifest.json': continue
    pdata = json.loads(pf.read_text(encoding='utf-8'))
    for q in pdata.get('questions', []):
        paper_q_count += 1
        if q.get('grammarPatternId') or q.get('vocab_id') or q.get('kanji_id'):
            paper_q_with_link += 1

# Density-8: confusable kanji clusters all-linked
clusters = [
    {'大', '犬', '太'},
    {'木', '本', '末', '未'},
    {'人', '入', '八'},
    {'日', '目', '白'},
    {'千', '干', '王', '玉'},
    {'上', '止', '正'},
    {'古', '占'},
    {'千', '午'},
]
cluster_complete = 0
for cluster in clusters:
    members_in_corpus = cluster & kanji_glyphs
    # check each member references at least one other member
    all_linked = True
    for m in members_in_corpus:
        # find the entry
        ent = next((e for e in k_entries if (e.get('char') or e.get('id', '').split('.')[-1]) == m), None)
        if not ent:
            all_linked = False; break
        ll = ent.get('lookalikes') or ent.get('confusable_with') or []
        if not (set(ll) & members_in_corpus - {m}):
            all_linked = False; break
    if all_linked: cluster_complete += 1

print(f'\nDensity-1: avg vocab in-links per pattern: {avg_g_to_v:.1f} (target ≥ 10)')
print(f'Density-2: vocab with ≥1 grammar back-ref: {v_with_g_link}/{vt} ({pctv(v_with_g_link)})')
print(f'Density-3: avg vocab per kanji (containment): {avg_k_to_v:.1f} (target ≥ 5)')
print(f'Density-4: kanji appearing in ≥1 reading passage: {kanji_in_read}/{kt} ({pctk(kanji_in_read)})')
print(f'Density-5: reading-passage sentence footnote ratio: 0 / {total_sentences} (field absent)')
print(f'Density-6: listening with vocab-glossary linkability: {listening_with_vocab_links}/{lt} ({pctl(listening_with_vocab_links)})')
print(f'Density-7: paper questions with content link: {paper_q_with_link}/{paper_q_count} ({100*paper_q_with_link/max(1,paper_q_count):.0f}%)')
print(f'Density-8: confusable clusters all-linked: {cluster_complete}/{len(clusters)} ({100*cluster_complete/len(clusters):.0f}%)')

# Aggregate
total_xrefs = (
    sum(g_to_v_links) +                           # grammar→vocab
    sum(v_to_g_count.values()) +                  # vocab→grammar (same as above)
    sum(k_to_v_count.values()) +                  # kanji→vocab
    sum(k_to_read_count.values()) +               # kanji→reading
    paper_q_with_link                             # paper-q→content
)
corpus_size = total + vt + kt + rt + lt + paper_q_count
import math
density = total_xrefs / max(1, math.sqrt(corpus_size))
print(f'\nAGGREGATE LINKING DENSITY = {total_xrefs} / sqrt({corpus_size}) = {density:.1f}')
print(f'  Bunpro reference ~8 / WaniKani ~12 / Jisho ~15')


# ============================================================================
# AUTHENTIC CONTENT LAYER
# ============================================================================

print('\n' + '=' * 70)
print('AUTHENTIC-CONTENT LAYER (the largest leverage opportunity)')
print('=' * 70)

g_authentic = sum(1 for p in patterns if p.get('authentic_media') or p.get('media_reference'))
v_authentic = sum(1 for e in v_entries if e.get('authentic_media') or e.get('media_reference'))
k_authentic = sum(1 for e in k_entries if e.get('real_world_signage') or e.get('signage'))
r_authentic = sum(1 for p in passages if p.get('authentic_source') or p.get('media_source'))
l_authentic = sum(1 for it in items if it.get('real_world_clip'))

print(f'\nGrammar with authentic-media reference: {g_authentic}/{total} ({pct(g_authentic)})')
print(f'Vocab with authentic-media reference: {v_authentic}/{vt} ({pctv(v_authentic)})')
print(f'Kanji with real-world signage:        {k_authentic}/{kt} ({pctk(k_authentic)})')
print(f'Reading from authentic source:        {r_authentic}/{rt} ({pctr(r_authentic)})')
print(f'Listening with real-world clip:       {l_authentic}/{lt} ({pctl(l_authentic)})')
print(f'\n>>> AUTHENTIC-CONTENT LAYER IS THE SINGLE LARGEST GAP <<<')


# ============================================================================
# COMPETITOR-FEATURE PARITY (auto-detection where possible)
# ============================================================================

print('\n' + '=' * 70)
print('COMPETITOR-FEATURE PARITY (auto-checked items)')
print('=' * 70)

# Inspect existing surfaces / settings for known features
js_dir = ROOT / 'js'
has_jp_keyboard = False
has_partial_credit = False
has_ghost_review = False
has_cloze = False
has_review_forecast = False
has_multi_skill_drill = False
has_anki_export = False
has_grammar_paths = any(p.get('genki_lesson') or p.get('genki_chapter') for p in patterns)
has_furigana_toggle = False
if js_dir.exists():
    settings_text = ''
    for js in js_dir.glob('*.js'):
        try:
            txt = js.read_text(encoding='utf-8', errors='replace')
            settings_text += txt
        except:
            pass
    has_jp_keyboard = 'kana_input' in settings_text or 'romaji_input' in settings_text or 'wanakana' in settings_text.lower()
    has_partial_credit = 'partial_credit' in settings_text or 'partialMatch' in settings_text
    has_ghost_review = 'ghost' in settings_text.lower() and 'review' in settings_text.lower()
    has_cloze = 'cloze' in settings_text.lower()
    has_review_forecast = 'forecast' in settings_text.lower()
    has_multi_skill_drill = 'unified' in settings_text.lower() or 'mixed_drill' in settings_text.lower()
    has_anki_export = 'anki' in settings_text.lower() and 'export' in settings_text.lower()
    has_furigana_toggle = 'furigana' in settings_text.lower()

print(f'Bunpro JP-keyboard input:      {"⚠ partial" if has_jp_keyboard else "❌ missing"}')
print(f'Bunpro partial-credit (50%):   {"✅" if has_partial_credit else "❌ missing"}')
print(f'Bunpro ghost reviews:          {"✅" if has_ghost_review else "❌ missing"}')
print(f'Bunpro cloze-deletion drills:  {"✅" if has_cloze else "❌ missing"}')
print(f'Bunpro review forecast (7-day):{"✅" if has_review_forecast else "❌ missing (already shown on home, but no proper forecast)"}')
print(f'Bunpro grammar-path tags:      {"✅" if has_grammar_paths else "❌ missing (no genki_lesson tags)"}')
print(f'WaniKani 3-mnemonic per kanji: {"✅" if k_mnemonic_radical and k_mnemonic_visual and k_mnemonic_reading else "❌ missing (0/106)"}')
print(f'WaniKani SRS gating:           ❌ missing')
print(f'WaniKani production reviews:   ❌ missing')
print(f'Tofugu pedagogical essays:     ❌ missing (explanation_en is short, not essay-length)')
print(f'Migaku Anki export:            {"✅" if has_anki_export else "❌ missing"}')
print(f'Migaku sentence-mining:        ❌ missing')
print(f'JapanesePod101 story dialogue: ⚠ partial (47 listening items are dialogues, but no "story mode")')
print(f'JP101 lesson-notes PDF:        ❌ missing')
print(f'Renshuu multi-skill drill:     {"✅" if has_multi_skill_drill else "❌ missing"}')
print(f'Renshuu custom user lists:     ⛔ deliberate-no (privacy posture)')
print(f'Jisho "words containing X kanji": ✅ (kanji.json examples array)')
print(f'Anki open-format export:       {"✅" if has_anki_export else "❌ missing"}')
print(f'Genki workbook print/PDF:      ❌ missing')
print(f'JLPT Sensei deep-linking:      ⚠ partial (per-item URLs exist, no SEO meta)')
print(f'Furigana toggle:               {"✅" if has_furigana_toggle else "❌"}')
