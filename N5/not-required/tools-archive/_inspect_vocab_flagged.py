"""Inspect the vocab entries flagged by the sanity scan."""
from __future__ import annotations
import io
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

d = json.loads((ROOT / 'data' / 'vocab.json').read_text(encoding='utf-8'))
items = d['entries']
flagged = [138, 165, 210, 224, 591, 612, 649, 672]
for i in flagged:
    if i < len(items):
        e = items[i]
        print(f"\n--- entry [{i}] ---")
        print(f"  id: {e.get('id', '?')}")
        print(f"  lemma: {e.get('lemma', '?')}")
        print(f"  reading: {e.get('reading', '?')}")
        print(f"  gloss: {e.get('gloss', '')[:160]}")
        print(f"  gloss_hi: {e.get('gloss_hi', '')[:160]}")
