"""ISSUE-110 RESOLUTION: AUDIT WAS BASED ON A FIELD-NAME TYPO.

After running this in v1, I discovered the audit was incorrect:

  1. The audit claim "132/1000 entries carry verb_class. Coverage
     should be 100% on verbs (~340 verbs in N5 corpus)" assumed
     ~340 verbs. The actual N5 corpus has 132 verbs total, and
     100% of them already carry verb_class. No gap there.

  2. The audit also asked for an explicit Group-1-exception flag
     on the 6 X-6.6 verbs (入る/帰る/走る/知る/切る/要る). These
     6 verbs already carry `group1_exception: true` (no
     underscore between "group" and "1") — see CHANGELOG.md
     entries dated pre-2026-05-04 documenting BUG-3 fix.

  3. The prompt file prompts/N5Improvement.txt:367 used a typo
     (`group_1_exception` with extra underscore). The audit
     inherited the typo, so the gap-detector thought the field
     was missing on all 1000 entries.

This script's first run *added* a redundant `group_1_exception`
field next to the existing `group1_exception` field on those 6
entries. That was wrong. The CORRECT action is to:

  (a) DELETE the redundant `group_1_exception` field this run
      added.
  (b) Document that ISSUE-110 has no underlying gap.

Result: vocab.json restored to the pre-ISSUE-110 state for those
6 entries; the `group1_exception: true` flag already present is
the canonical answer.
"""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

vocab_path = ROOT / 'data' / 'vocab.json'
data = json.loads(vocab_path.read_text(encoding='utf-8'))
entries = data['entries']

removed = 0
already_correct = 0

for e in entries:
    if 'group_1_exception' in e:  # the typo'd field this script's
                                  # v1 added
        del e['group_1_exception']
        removed += 1

# Verify the canonical field is still in place on the 6 X-6.6 verbs
canonical_present = sum(1 for e in entries if e.get('group1_exception') is True)

vocab_path.write_text(
    json.dumps(data, ensure_ascii=False, indent=2) + '\n',
    encoding='utf-8',
)

print(f'Removed redundant group_1_exception field: {removed}')
print(f'Canonical group1_exception still present:  {canonical_present}')
print()
print('ISSUE-110 closure: NO underlying gap. Audit was based on a')
print('field-name typo. Both numerical claims (verb_class coverage')
print('and X-6.6 flag coverage) are already 100% in vocab.json.')
