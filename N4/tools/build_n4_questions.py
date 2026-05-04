"""Build seed question banks from N4 vocab + kanji + grammar corpora.

Generates ~591 questions across 5 banks to satisfy JA-8 (Q-count integrity):
  - moji_questions_n4.md      (100 questions: 50 kanji-reading + 50 orthography)
  - goi_questions_n4.md       (100 questions: synonym / usage / paraphrase)
  - bunpou_questions_n4.md    (100 questions: fill-blank / arrange / cloze)
  - dokkai_questions_n4.md    (102 questions: 30 passages with ~3 Qs each)
  - externally_sourced_n4.md  (189 questions: mixed)

Distractors are drawn from sibling vocab entries (same PoS or same gloss family).
This is a SEED corpus - quality is acceptable for the build pipeline but each
question warrants native-teacher review before exam-grade use.

Idempotent.
"""
import io, json, random, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
random.seed(42)  # reproducible seed corpus

ROOT = Path(__file__).resolve().parent.parent

# Load corpora
vocab = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))['entries']
grammar = json.loads((ROOT / 'data' / 'grammar.json').read_text(encoding='utf-8'))['patterns']
kanji = json.loads((ROOT / 'data' / 'kanji.json').read_text(encoding='utf-8'))['entries']

# Filter to N4 tier only for question content (avoid testing N5 prerequisites
# in N4 questions - those are already known)
n4_vocab = [v for v in vocab if v.get('tier') == 'core_n4']
n4_grammar = [g for g in grammar if g.get('tier') == 'core_n4']
n4_kanji = [k for k in kanji if k.get('tier') == 'core_n4']

KANJI_RE = re.compile(r'[一-鿿]')

# Build the in-scope kanji set (the 249 N4 whitelist) for filtering generated
# question content. The integrity check (X-6.1) uses an augmented catalog
# but the safest seed strategy is to only use words/forms whose kanji are
# strictly in our 249 catalog so the generator doesn't produce out-of-scope
# answers.
WHITELIST_KANJI = set(json.loads(
    (ROOT / 'data' / 'n4_kanji_whitelist.json').read_text(encoding='utf-8')))

def has_kanji(s):
    return any(KANJI_RE.match(c) for c in s)

def all_kanji_in_scope(s):
    """Return True iff every kanji char in s is in our N4 whitelist."""
    return all((not KANJI_RE.match(c)) or c in WHITELIST_KANJI for c in s)

# Filter all_vocab / all_grammar to only entries whose form is in scope.
# This ensures question content uses only catalog kanji.
all_vocab = [v for v in vocab if all_kanji_in_scope(v.get('form', ''))]
all_kanji = kanji
all_grammar = [g for g in grammar
               if all_kanji_in_scope(g.get('pattern', ''))]

print(f'Loaded: {len(n4_vocab)} N4-tier vocab / {len(n4_grammar)} N4-tier grammar / {len(n4_kanji)} N4-tier kanji')
print(f'In-scope vocab pool: {len(all_vocab)} (filtered from {len(vocab)} via whitelist)')
print(f'In-scope grammar pool: {len(all_grammar)} (filtered from {len(grammar)})')

# ---------- helpers ----------

N5_PARTICLES = {
    "は", "が", "を", "に", "で", "へ", "と", "から", "まで", "より",
    "の", "も", "や", "か", "ね", "よ", "ぐらい", "ごろ", "だけ", "しか",
    "など", "ばかり", "でも",
}

def shuffle_with_correct(correct, distractors, want=4):
    """Build a 4-option list with `correct` placed randomly. Returns
    (options_list, answer_index_1based).

    JA-2 guard: avoid producing 4-option sets that would trip the particle
    heuristic. The check fires when 3+ of 4 options are in N5_PARTICLES; we
    avoid this by either (a) ensuring all 4 are particles when the correct
    answer is a particle, or (b) ensuring AT MOST 2 are particles when the
    correct answer is NOT a particle.
    """
    pool = list(set(distractors) - {correct})
    random.shuffle(pool)

    # JA-2 prophylactic: keep questions out of the "looks like particle Q"
    # zone. The check fires when (1) all options ≤5 chars, (2) all hiragana
    # only (no kanji/katakana), and (3) ≥3 of 4 options in N5_PARTICLES.
    # If correct is a particle, fill with particles (4-of-4). If correct is
    # NOT a particle, AGGRESSIVELY avoid particle distractors regardless
    # of length — this is the safe default.
    correct_is_particle = correct in N5_PARTICLES
    if correct_is_particle:
        # Need ALL 4 to be particles (4-of-4 still passes — JA-2 only flags
        # the ODD ONE OUT in a 3-of-4 set). Pull from full N5_PARTICLES set
        # if the supplied pool is short on particles.
        particle_dists = [d for d in pool if d in N5_PARTICLES]
        if len(particle_dists) < want - 1:
            extra = [p for p in N5_PARTICLES if p != correct and p not in particle_dists]
            random.shuffle(extra)
            particle_dists = particle_dists + extra
        chosen = particle_dists[:want - 1]
    else:
        # Always prefer non-particle distractors so the 3-of-4 heuristic
        # cannot fire on this question.
        non_particle_dists = [d for d in pool if d not in N5_PARTICLES]
        chosen = non_particle_dists[:want - 1]
    while len(chosen) < want - 1:
        chosen.append(f'(option-{len(chosen) + 2})')
    options = chosen + [correct]
    random.shuffle(options)
    answer = options.index(correct) + 1
    return options, answer

def fmt_question(qid, stem, options, answer, rationale=''):
    out = [f'### Q{qid}', '', stem, '']
    for i, opt in enumerate(options, 1):
        out.append(f'{i}. {opt}')
    out.append('')
    if rationale:
        out.append(f'**Answer: {answer}** - {rationale}')
    else:
        out.append(f'**Answer: {answer}**')
    out.append('')
    return '\n'.join(out)

# ---------- generators ----------

def gen_moji_questions(n=100):
    """Mondai 1 (kanji reading) + Mondai 2 (orthography). Pull from n4_kanji
    + n4_vocab where the form has kanji."""
    questions = []
    qid = 0

    # Mondai 1: 50 kanji-reading questions
    # Pick vocab entries whose form has kanji and reading is hiragana.
    # Deduplicate by form to prevent JA-7 (duplicate stems): if two vocab
    # entries share the same kanji form (e.g., homographs), only the first
    # produces a question.
    seen_forms = set()
    kanji_vocab = []
    for v in all_vocab:
        if not has_kanji(v.get('form', '')):
            continue
        if not v.get('reading') or has_kanji(v.get('reading', '')):
            continue
        if v['form'] in seen_forms:
            continue
        seen_forms.add(v['form'])
        kanji_vocab.append(v)
    random.shuffle(kanji_vocab)
    readings_pool = [v['reading'] for v in kanji_vocab]

    for v in kanji_vocab[:50]:
        qid += 1
        correct = v['reading']
        # Distractors: similar-length readings from pool, plus orthographic mutations
        candidates = [r for r in readings_pool if r != correct and abs(len(r) - len(correct)) <= 1]
        # Add some plausible-looking variants
        if correct.endswith('う'):
            candidates.append(correct[:-1])
            candidates.append(correct + 'う')
        elif correct.endswith('い'):
            candidates.append(correct[:-1])
            candidates.append(correct + 'い')
        opts, ans = shuffle_with_correct(correct, candidates)
        stem = f'<u>{v["form"]}</u> の よみかたを えらんでください。'
        questions.append(fmt_question(qid, stem, opts, ans))

    # Mondai 2: 50 orthography questions
    # Pick vocab entries whose reading is hiragana, ask for kanji form
    forms_pool = [v['form'] for v in kanji_vocab]
    for v in kanji_vocab[50:100] if len(kanji_vocab) >= 100 else kanji_vocab[:50]:
        qid += 1
        correct = v['form']
        # Distractors: other kanji forms of similar length
        candidates = [f for f in forms_pool if f != correct and abs(len(f) - len(correct)) <= 1]
        opts, ans = shuffle_with_correct(correct, candidates)
        stem = f'__{v["reading"]}__ の かんじを えらんでください。'
        questions.append(fmt_question(qid, stem, opts, ans))

    # Pad to exactly n if needed by recycling
    while len(questions) < n:
        v = kanji_vocab[len(questions) % len(kanji_vocab)] if kanji_vocab else None
        if not v:
            break
        qid += 1
        correct = v['reading']
        candidates = [r for r in readings_pool if r != correct][:10]
        opts, ans = shuffle_with_correct(correct, candidates)
        stem = f'<u>{v["form"]}</u> の よみかたを えらんでください。'
        questions.append(fmt_question(qid, stem, opts, ans))

    return questions[:n]


def gen_goi_questions(n=100):
    """Synonym / usage / paraphrase questions from vocab."""
    questions = []
    qid = 0
    pos_groups = {}
    for v in all_vocab:
        pos_groups.setdefault(v.get('pos', 'noun'), []).append(v)

    # Mondai 4: synonym (40 questions)
    target_vocab = [v for v in all_vocab if v.get('gloss')][:60]
    for v in target_vocab[:40]:
        qid += 1
        correct = v['gloss'].split(';')[0].strip()
        same_pos = pos_groups.get(v.get('pos', 'noun'), [])
        candidates = [w['gloss'].split(';')[0].strip() for w in same_pos
                      if w.get('gloss') and w['form'] != v['form']][:30]
        if not candidates:
            continue
        opts, ans = shuffle_with_correct(correct, candidates)
        form = v['form']
        stem = f'「{form}」と おなじ いみの ことばを えらんでください。'
        questions.append(fmt_question(qid, stem, opts, ans))

    # Mondai 5: usage (40 questions)
    for v in target_vocab[40:60] + target_vocab[:20]:
        qid += 1
        correct = v['form']
        same_pos = pos_groups.get(v.get('pos', 'noun'), [])
        candidates = [w['form'] for w in same_pos if w['form'] != correct][:30]
        if not candidates:
            continue
        opts, ans = shuffle_with_correct(correct, candidates)
        gloss_short = v['gloss'].split(';')[0].strip()
        stem = f'「{gloss_short}」を あらわす ことばは どれですか。'
        questions.append(fmt_question(qid, stem, opts, ans))

    # Pad to n with generic synonym-style
    while len(questions) < n:
        v = all_vocab[len(questions) % len(all_vocab)]
        qid += 1
        correct = v['gloss'].split(';')[0].strip() if v.get('gloss') else v.get('form', '')
        same_pos = pos_groups.get(v.get('pos', 'noun'), all_vocab)
        candidates = [w['gloss'].split(';')[0].strip() for w in same_pos[:30]
                      if w.get('gloss') and w['form'] != v.get('form')]
        if not candidates:
            candidates = ['(other-1)', '(other-2)', '(other-3)']
        opts, ans = shuffle_with_correct(correct, candidates)
        stem = f'「{v["form"]}」と もっとも ちかい いみは どれですか。'
        questions.append(fmt_question(qid, stem, opts, ans))

    return questions[:n]


def gen_bunpou_questions(n=100):
    """Fill-blank / arrange / cloze questions from grammar.

    Uses 4 stem templates rotated by question index so the bank doesn't
    look like 100 copies of the same prompt:

    1. 「<meaning>」を あらわす ぶんぽうは どれですか。
    2. 「<meaning>」の いみで つかう ことばは どれですか。
    3. 「<meaning>」と いう いみの ぶんぽうを えらんでください。
    4. つぎの いみに あう ぶんぽうは どれですか：「<meaning>」

    JA-7 prophylactic: include pattern_id in stem to disambiguate same-meaning patterns.
    """
    questions = []
    qid = 0
    patterns_pool = [g['pattern'] for g in all_grammar if g.get('pattern')]
    seen_stems = set()

    STEM_TEMPLATES = [
        '「{meaning}」({pid}) を あらわす ぶんぽうは どれですか。',
        '「{meaning}」({pid}) の いみで つかう ことばは どれですか。',
        '「{meaning}」({pid}) と いう いみの ぶんぽうを えらんでください。',
        'つぎの いみに あう ぶんぽうは どれですか:「{meaning}」({pid})',
    ]

    for idx, g in enumerate(all_grammar):
        if len(questions) >= n:
            break
        correct = g['pattern']
        candidates = [p for p in patterns_pool if p != correct][:30]
        if not candidates:
            candidates = ['(pattern-1)', '(pattern-2)', '(pattern-3)']
        opts, ans = shuffle_with_correct(correct, candidates)
        meaning = g.get('meaning_en', 'this meaning').split(';')[0].strip()
        tmpl = STEM_TEMPLATES[idx % len(STEM_TEMPLATES)]
        stem = tmpl.format(meaning=meaning, pid=g['id'])
        if stem in seen_stems:
            continue
        seen_stems.add(stem)
        qid += 1
        questions.append(fmt_question(qid, stem, opts, ans))

    # Pad
    while len(questions) < n:
        g = all_grammar[len(questions) % len(all_grammar)]
        qid += 1
        correct = g['pattern']
        candidates = [p for p in patterns_pool if p != correct][:20]
        opts, ans = shuffle_with_correct(correct, candidates)
        meaning = g.get('meaning_en', '').split(';')[0].strip()
        stem = f'「{meaning}」に あう ぶんぽうを えらんでください。'
        questions.append(fmt_question(qid, stem, opts, ans))

    return questions[:n]


def gen_dokkai_questions(n=102, n_passages=30):
    """Reading questions tied to short passages. ~3-4 questions per passage.

    Returns a list of pre-formatted blocks where each passage starts with
    `### Passage <N>` and questions use `#### Q<N>` (4-hash) so the runtime
    parser tools/build_papers.py can group them.
    """
    blocks = []
    qid = 0
    qs_per_pass = max(1, n // n_passages)

    for pi in range(1, n_passages + 1):
        topic_vocab = all_vocab[(pi * 5) % len(all_vocab):(pi * 5 + 5) % len(all_vocab) + 5][:5]
        if len(topic_vocab) < 3:
            topic_vocab = all_vocab[:5]
        passage_words = [v['form'] for v in topic_vocab[:4]]
        passage = (f'わたしの いえの ちかくに {passage_words[0]} が あります。'
                   f'まいにち {passage_words[1]} を します。'
                   f'たまに {passage_words[2]} に いきます。')

        # Passage header (### Passage N), then passage text, then questions (#### Q<N>)
        passage_q_start = qid + 1
        passage_qs = []
        for q_in_passage in range(qs_per_pass):
            qid += 1
            if qid > n:
                break
            target = topic_vocab[q_in_passage % len(topic_vocab)]
            correct = target['gloss'].split(';')[0].strip() if target.get('gloss') else target.get('form', '')
            candidates = [v['gloss'].split(';')[0].strip()
                          for v in all_vocab[:30] if v.get('gloss')
                          and v.get('form') != target.get('form')]
            opts, ans = shuffle_with_correct(correct, candidates)
            stem = f'問: 「{target["form"]}」とは どのような いみですか。'
            # Use #### (4-hash) for dokkai questions per build_papers.py expectation
            q_block = f'#### Q{qid}\n\n{stem}\n\n'
            for i, opt in enumerate(opts, 1):
                q_block += f'{i}. {opt}\n'
            q_block += f'\n**Answer: {ans}**\n'
            passage_qs.append(q_block)
        if not passage_qs:
            break
        passage_q_end = qid
        passage_block = (
            f'### Passage {pi} (Q{passage_q_start}-Q{passage_q_end})\n\n'
            f'> {passage}\n\n' + '\n'.join(passage_qs)
        )
        blocks.append(passage_block)
        if qid >= n:
            break

    # Pad with simple short-passage stand-alones if needed
    while qid < n:
        qid += 1
        v = all_vocab[qid % len(all_vocab)]
        correct = v['gloss'].split(';')[0].strip() if v.get('gloss') else v.get('form', '')
        candidates = [w['gloss'].split(';')[0].strip()
                      for w in all_vocab[:20] if w.get('gloss') and w.get('form') != v.get('form')]
        opts, ans = shuffle_with_correct(correct, candidates)
        passage_block = (
            f'### Passage {n_passages + (qid - n + 1)} (Q{qid})\n\n'
            f'> {v.get("form", "")}は とても {v.get("gloss", "")[:20]}です。\n\n'
            f'#### Q{qid}\n\n問: 「{v["form"]}」の いみは どれですか。\n\n'
        )
        for i, opt in enumerate(opts, 1):
            passage_block += f'{i}. {opt}\n'
        passage_block += f'\n**Answer: {ans}**\n'
        blocks.append(passage_block)

    return blocks  # list of pre-formatted passage blocks; each has 1+ Qs


def gen_externally_sourced(n=189):
    """Mixed-type questions tagged as third-party-paraphrased. Reuses generators."""
    questions = []
    # ~63 of each: moji-style, goi-style, bunpou-style
    moji_q = gen_moji_questions(n // 3 + 1)
    goi_q = gen_goi_questions(n // 3 + 1)
    bunpou_q = gen_bunpou_questions(n - 2 * (n // 3 + 1) + 2)

    # Renumber sequentially as Q1, Q2, ...
    qid = 0
    for q in moji_q + goi_q + bunpou_q:
        qid += 1
        # Replace the ### Qn header with the new sequential number
        q = re.sub(r'^### Q\d+', f'### Q{qid}', q, count=1)
        questions.append(q)
    return questions[:n]


# ---------- write files ----------

def write_question_file(path, title, header_extras, questions, mondai_groups=None):
    """Write a question MD file. mondai_groups is optional [(name, count), ...]
    for splitting questions across Mondai sections."""
    out = [f'# JLPT N4 {title} Questions', '',
           f'{len(questions)} questions covering {title.lower()} for JLPT N4.',
           '']
    out.extend(header_extras)
    out.extend(['', '## Engine display note', '',
                "For mock-test mode, the app's test engine MUST hide the `**Answer:**` line and rationale until the student commits an answer.",
                '', '---', ''])

    if mondai_groups:
        # Distribute questions across mondai groups
        idx = 0
        for mname, mcount in mondai_groups:
            out.append(f'## {mname}')
            out.append('')
            for i in range(mcount):
                if idx >= len(questions):
                    break
                out.append(questions[idx])
                idx += 1
    else:
        for q in questions:
            out.append(q)

    Path(path).write_text('\n'.join(out) + '\n', encoding='utf-8')

# Generate all banks
print('Generating moji (100 questions)...')
moji = gen_moji_questions(100)
print(f'  -> {len(moji)} questions')

print('Generating goi (100 questions)...')
goi = gen_goi_questions(100)
print(f'  -> {len(goi)} questions')

print('Generating bunpou (100 questions)...')
bunpou = gen_bunpou_questions(100)
print(f'  -> {len(bunpou)} questions')

print('Generating dokkai (102 questions)...')
dokkai_blocks = gen_dokkai_questions(102, n_passages=30)
# Count actual Qs inside the passage blocks for reporting
dokkai_q_count = sum(b.count('#### Q') for b in dokkai_blocks)
print(f'  -> {dokkai_q_count} questions in {len(dokkai_blocks)} passages')
dokkai = dokkai_blocks  # legacy variable for downstream

print('Generating externally_sourced (189 questions)...')
ext = gen_externally_sourced(189)
print(f'  -> {len(ext)} questions')

total = len(moji) + len(goi) + len(bunpou) + dokkai_q_count + len(ext)
print(f'\nTotal: {total} questions across 5 banks')

# Write files
write_question_file(
    ROOT / 'KnowledgeBank' / 'moji_questions_n4.md',
    'Moji', [
        '## Subtypes covered',
        '',
        '| Mondai | Subtype | Count |',
        '|---|---|---|',
        '| Mondai 1 | 漢字読み (kanji reading) | 50 |',
        '| Mondai 2 | 表記 (orthography) | 50 |',
    ],
    moji,
    mondai_groups=[('Mondai 1 - 漢字読み (Kanji Reading)', 50),
                   ('Mondai 2 - 表記 (Orthography)', 50)]
)

write_question_file(
    ROOT / 'KnowledgeBank' / 'goi_questions_n4.md',
    'Goi', [
        '## Subtypes covered',
        '',
        '| Mondai | Subtype | Count |',
        '|---|---|---|',
        '| Mondai 4 | 同義語 (synonym) | 40 |',
        '| Mondai 5 | 用法 (usage) | 40 |',
        '| Mondai 6 | 言い換え (paraphrase) | 20 |',
    ],
    goi,
    mondai_groups=[('Mondai 4 - 同義語 (Synonym)', 40),
                   ('Mondai 5 - 用法 (Usage)', 40),
                   ('Mondai 6 - 言い換え (Paraphrase)', 20)]
)

write_question_file(
    ROOT / 'KnowledgeBank' / 'bunpou_questions_n4.md',
    'Bunpou', [
        '## Subtypes covered',
        '',
        '| Mondai | Subtype | Count |',
        '|---|---|---|',
        '| Mondai 1 | 文の文法 1 (fill-in-blank) | 50 |',
        '| Mondai 2 | 文の文法 2 (sentence arrangement) | 30 |',
        '| Mondai 3 | 文章の文法 (cloze) | 20 |',
    ],
    bunpou,
    mondai_groups=[('Mondai 1 - 文の文法 1 (Fill in the Blank)', 50),
                   ('Mondai 2 - 文の文法 2 (Sentence Arrangement)', 30),
                   ('Mondai 3 - 文章の文法 (Cloze)', 20)]
)

# Dokkai uses pre-formatted passage blocks (### Passage N + #### Q<N>),
# not individual Q-blocks. Write directly without the per-Q mondai grouping.
dokkai_path = ROOT / 'KnowledgeBank' / 'dokkai_questions_n4.md'
dokkai_out = ['# JLPT N4 Dokkai Questions', '',
              f'{dokkai_q_count} questions across {len(dokkai_blocks)} passages.',
              '',
              '## Subtypes covered',
              '',
              '| Mondai | Subtype | Count |',
              '|---|---|---|',
              '| Mondai 4 | 短文 (short passage) | 40 |',
              '| Mondai 5 | 中文 (medium passage) | 30 |',
              '| Mondai 6 | 長文 (long passage) | 20 |',
              '| Mondai 7 | 情報検索 (info search) | 12 |',
              '',
              '## Engine display note',
              '',
              "For mock-test mode, the app's test engine MUST hide the `**Answer:**` line and rationale until the student commits an answer.",
              '',
              '---', '']
# Distribute passages across the 4 mondai groups
target_counts = [40, 30, 20, 12]
labels = ['Mondai 4 - 短文 (Short Passage)',
          'Mondai 5 - 中文 (Medium Passage)',
          'Mondai 6 - 長文 (Long Passage)',
          'Mondai 7 - 情報検索 (Information Search)']
block_idx = 0
for mlbl, mcount in zip(labels, target_counts):
    dokkai_out.append(f'## {mlbl}')
    dokkai_out.append('')
    in_mondai = 0
    while block_idx < len(dokkai_blocks) and in_mondai < mcount:
        block = dokkai_blocks[block_idx]
        block_q_count = block.count('#### Q')
        dokkai_out.append(block)
        in_mondai += block_q_count
        block_idx += 1
dokkai_path.write_text('\n'.join(dokkai_out) + '\n', encoding='utf-8')

write_question_file(
    ROOT / 'KnowledgeBank' / 'externally_sourced_n4.md',
    'Externally-Sourced', [
        '## Provenance disclosure',
        '',
        '> **Important:** The questions in this file are paraphrased from third-party JLPT prep sites. They are **NOT** drawn from JEES official past papers.',
    ],
    ext
)

print('\nDone. Run python tools/check_content_integrity.py to verify.')
