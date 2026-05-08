"""Quick debug runner for JA-41 to bypass the cp932 verbose-print bug."""
from __future__ import annotations
import io
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'tools').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.path.insert(0, str(ROOT / 'tools'))

import check_content_integrity as cci
failures = cci._check_ja_41_kana_prefix_convention()
print(f'JA-41 failures: {len(failures)}')
for f in failures:
    print(f'  {f}')
