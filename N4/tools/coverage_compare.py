"""
Quick coverage comparison: our questions.json (163 questions tagged to N5
patterns) vs the externally extracted learnjapaneseaz.com corpus (175
questions across 17 tests).

External corpus has no pattern-id tags — we infer the topic by inspecting
the BLANK in each stem, since the answer is the particle/grammar form
being tested. Then we tally: what fraction of N5 patterns covered, and
which N5 patterns are over- or under-represented.

Output: short markdown report at feedback/coverage-comparison.md.
"""
import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXT_PATH = ROOT / 'feedback' / 'external-questions-learnjapaneseaz.md'
QS_PATH = ROOT / 'data' / 'questions.json'
OUT_PATH = ROOT / 'feedback' / 'coverage-comparison.md'

# --- Load our questions ---
with QS_PATH.open(encoding='utf-8') as f:
    qd = json.load(f)
our_q = qd['questions']

our_pattern_counts = Counter(q.get('grammarPatternId', '?') for q in our_q)
our_correct_counts = Counter(
    q.get('correctAnswer', '?') for q in our_q if q.get('type') == 'mcq'
)

# --- Parse external corpus ---
# Format per Q in the markdown:
#   **Qn** stem: <text with （ ））>
#   - Options: [a / b / c / d]   OR   options: a / b / c / d
#   - Correct: <answer>
ext_text = EXT_PATH.read_text(encoding='utf-8')

# Pull each "Correct: X" line. Naive but works since the format is regular.
correct_lines = re.findall(r'Correct:\s*([^\n]+)', ext_text, re.IGNORECASE)
# Strip surrogate-mark prefixes like "4 (を)" -> "を"
ext_correct = []
for line in correct_lines:
    line = line.strip()
    m = re.search(r'\((.+?)\)', line)
    if m:
        ext_correct.append(m.group(1).strip())
    else:
        # bare "へ" / "から" / "見せて" etc.
        ext_correct.append(line.split()[0] if ' ' in line else line)
ext_correct_counts = Counter(ext_correct)

# --- Compare top correctAnswer distributions ---
report = []
report.append('# Cross-coverage comparison: our 163 vs learnjapaneseaz.com 175')
report.append('')
report.append(f'- Our questions:  {len(our_q)} total ({sum(1 for q in our_q if q.get("type")=="mcq")} mcq)')
report.append(f'- External:       {len(ext_correct)} questions across 17 tests')
report.append('')
report.append('## Most-tested correct-answer tokens')
report.append('')
report.append('| Token | Ours | External | Δ (ours−ext) |')
report.append('|-------|-----:|---------:|------------:|')

all_tokens = set(our_correct_counts) | set(ext_correct_counts)
# Sort by combined frequency
ranked = sorted(all_tokens,
                key=lambda t: -(our_correct_counts[t] + ext_correct_counts[t]))
for t in ranked[:25]:
    ours = our_correct_counts[t]
    ext = ext_correct_counts[t]
    report.append(f'| {t} | {ours} | {ext} | {ours - ext:+d} |')

# Tokens covered by external but not us
report.append('')
report.append('## Tokens tested by external corpus but absent from our correct-answer set')
report.append('')
not_in_ours = sorted([(t, c) for t, c in ext_correct_counts.items()
                       if t not in our_correct_counts and len(t) <= 8],
                      key=lambda x: -x[1])
if not_in_ours:
    for t, c in not_in_ours[:30]:
        report.append(f'- `{t}` × {c}')
else:
    report.append('(none)')

report.append('')
report.append('## Tokens we test that external doesn\'t')
report.append('')
not_in_ext = sorted([(t, c) for t, c in our_correct_counts.items()
                      if t not in ext_correct_counts and len(t) <= 8],
                     key=lambda x: -x[1])
if not_in_ext:
    for t, c in not_in_ext[:30]:
        report.append(f'- `{t}` × {c}')
else:
    report.append('(none)')

report.append('')
report.append('## Pattern coverage in our bank')
report.append('')
report.append(f'- Unique pattern IDs covered: {len(our_pattern_counts)}')
report.append(f'- Most over-represented (top 10):')
for pid, c in our_pattern_counts.most_common(10):
    report.append(f'  - `{pid}` × {c}')
report.append(f'- Singletons (patterns with 1 question): '
              f'{sum(1 for c in our_pattern_counts.values() if c == 1)}')

report.append('')
report.append('## Notes for downstream review')
report.append('')
report.append('- The external corpus does not tag questions to grammar-pattern IDs, so this comparison is at the *correct-answer token* level only. A finer-grained mapping would require manually tagging each external question.')
report.append('- Tokens absent from our correct-answer set may either be (a) genuine coverage gaps OR (b) variants we test under a different surface form (e.g., we test `見て` and they test `見せて`).')
report.append('- Use this as a triage signal, not as a definitive gap report. Items in "external but not ours" with count ≥ 3 are the strongest candidates for new question authoring.')

OUT_PATH.write_text('\n'.join(report) + '\n', encoding='utf-8')
print(f'Wrote {OUT_PATH.relative_to(ROOT)} ({len(report)} lines)')
print()
print('Top tokens absent from ours:')
for t, c in not_in_ours[:10]:
    print(f'  {t} × {c}')
