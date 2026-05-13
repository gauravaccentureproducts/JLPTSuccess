"""Compare KnowledgeBank markdown scope against the live whitelist JSONs.

KnowledgeBank/*.md is the **N5 scope reference** -- the canonical human-
readable list of what is in scope for each paper section.

This tool was originally a generator: it extracted scope from KB and
wrote whitelist JSONs that the CI integrity checks consume. Over time
the maintainer hand-tuned BOTH layers:

  - The whitelist JSONs (n5_kanji_readings.json got deduplicated kun
    readings; i-adj kanji got their primary reading set to the kun-yomi;
    n5_vocab_whitelist.json picked up corpus-specific corrections).
  - The teaching-content JSONs (vocab.json, kanji.json) got pitch_accent,
    examples, collocations, frequent_patterns, verb_class, etymology,
    mnemonics, lookalikes -- none of which exist in KB.

Running the original generator would WIPE the hand-tuning on BOTH
layers -- a footgun caught during the run-4 accuracy audit (2026-05-14).
The tool is now **comparison-only**:

  - Default (`python tools/build_data.py`) -- diff KB-extracted scope
    against live whitelist files, report drift, no writes.
  - `--write` flag -- DANGEROUS; only use after confirming KB is the
    intended source-of-truth for the whitelist file in question (it
    isn't, currently -- the whitelists are hand-tuned).

If KB-to-whitelist drift becomes a concern (e.g., a new kanji added to
KB without being reflected in the whitelist), use the diff output to
decide whether to update KB or the whitelist; do NOT auto-write.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def extract_kanji(md_path: Path) -> list[str]:
    """Pull all kanji from bullet entries like '- **一**'."""
    text = md_path.read_text(encoding="utf-8")
    matches = re.findall(r"\*\*([一-鿿])\*\*", text)
    return sorted(set(matches))


# Katakana to hiragana conversion table for on'yomi normalization.
KATA_TO_HIRA = str.maketrans(
    "アイウエオカキクケコサシスセソタチツテトナニヌネノハヒフヘホマミムメモヤユヨラリルレロワヲンガギグゲゴザジズゼゾダヂヅデドバビブベボパピプペポャュョッー",
    "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわをんがぎぐげござじずぜぞだぢづでどばびぶべぼぱぴぷぺぽゃゅょっー",
)


def kata_to_hira(s: str) -> str:
    return s.translate(KATA_TO_HIRA)


def extract_kanji_readings(md_path: Path) -> dict[str, dict]:
    """Parse kanji entries with their On / Kun readings.

    Returns: { kanji: { 'on': [hiragana...], 'kun': [hiragana...], 'primary': str } }
    Primary picks the first kun-yomi (without okurigana), falls back to first on-yomi.
    Note: this is a single representative reading - real Japanese reading is
    context-dependent. The renderer applies this best-effort when the user's
    'Show furigana on N5 kanji' toggle is ON.
    """
    text = md_path.read_text(encoding="utf-8")
    entries: dict[str, dict] = {}
    current = None
    for raw in text.splitlines():
        line = raw.rstrip()
        # Tolerate trailing tags like `**[Ext]**` after the kanji header.
        # Pass-14 fix: previously the strict `\s*$` end-anchor caused 4
        # [Ext]-tagged entries (号, 員, 社, 私) to be dropped from the
        # readings file - kanji.json had them via extract_kanji_corpus
        # (which already had the lenient match) but n5_kanji_readings.json
        # was missing them. Now both extractors share the same regex.
        m = re.match(r"^\s*-\s+\*\*([一-鿿])\*\*", line)
        if m:
            current = m.group(1)
            entries[current] = {"on": [], "kun": [], "primary": None}
            continue
        if current is None:
            continue
        # Sub-bullet readings.
        on_m = re.match(r"^\s*-\s*On\s*:\s*(.+)$", line)
        if on_m:
            raws = [r.strip() for r in on_m.group(1).split(",")]
            entries[current]["on"] = [
                kata_to_hira(r) for r in raws if r and r != "-"
            ]
            continue
        kun_m = re.match(r"^\s*-\s*Kun\s*:\s*(.+)$", line)
        if kun_m:
            raws = [r.strip() for r in kun_m.group(1).split(",")]
            cleaned = []
            for r in raws:
                if not r or r == "-":
                    continue
                # Strip okurigana parens: ひと(つ) -> ひと
                core = re.sub(r"\(.*?\)", "", r).strip()
                if core:
                    cleaned.append(core)
            entries[current]["kun"] = cleaned
            continue
        # End of entry on blank line or new heading.
        if not line.strip() or line.startswith("##"):
            current = None

    # Pick a primary reading per kanji. The default "first kun, fall back to
    # first on" heuristic produces wrong results for most N5 kanji whose
    # context-most-common reading is the on-yomi (counters, time/date words,
    # compounds). Pass-10 reference table from
    # `feedback/ui-testing-plan.md` §12.1 X-6.9 lists the N5-correct primaries
    # for 35 such kanji - those overrides win. Any kanji not in the override
    # falls back to the kun-first heuristic.
    PASS10_PRIMARY_OVERRIDES = {
        "一": "いち", "二": "に",   "三": "さん", "四": "よん", "五": "ご",
        "六": "ろく", "七": "しち", "八": "はち", "九": "きゅう","十": "じゅう",
        "千": "せん", "本": "ほん", "日": "にち", "時": "じ",   "分": "ふん",
        "円": "えん", "月": "がつ", "学": "がく", "生": "せい", "先": "せん",
        "半": "はん", "番": "ばん", "国": "こく", "後": "あと", "会": "かい",
        "車": "しゃ", "高": "こう", "長": "ちょう","安": "あん", "新": "しん",
        "中": "ちゅう","外": "がい", "東": "とう", "年": "ねん", "人": "にん",
        # Pass-14c add (data-correction brief §3.10): 何's primary changed
        # から なに → なん. Across N5 vocab (何時/何曜日/何月/何日/何人),
        # なん dominates; なに is correct only for the standalone 何ですか.
        # Since `primary` is the default for the bare-kanji case in any
        # context, the more-frequent compound reading wins.
        "何": "なん",
    }
    for kanji, e in entries.items():
        override = PASS10_PRIMARY_OVERRIDES.get(kanji)
        if override:
            # Make sure the override is in the on/kun pool; if not, append to on
            # so the schema stays consistent.
            if override not in (e["on"] + e["kun"]):
                e["on"].append(override)
            e["primary"] = override
        else:
            e["primary"] = (e["kun"] or e["on"] or [""])[0]
    return entries


def extract_kanji_corpus(md_path: Path) -> list[dict]:
    """Parse kanji_n5.md into rich kanji records (each kanji + meaning + readings).

    Each entry shape:
        {
          "id": "n5.kanji.X",
          "glyph": "食",
          "on": [...],        # hiragana
          "kun": [...],       # hiragana, with okurigana stripped
          "meanings": [...],  # English glosses split on slash/comma
          "stroke_order_svg": "/svg/kanji/食.svg",  # placeholder; KanjiVG can drop in
        }
    """
    text = md_path.read_text(encoding="utf-8")
    out = []
    current = None
    meanings = ""
    for raw in text.splitlines():
        line = raw.rstrip()
        # Tolerate trailing tags like `**[Ext]**` after the kanji header.
        # Pre-fix bug: the strict `\s*$` end-anchor prevented `[Ext]`-tagged
        # entries (員, 号, 社, 私) from being recognized as new entries; their
        # field lines then contaminated the previous entry. See verification.md
        # Pass-13 F-13.1/F-13.2.
        m = re.match(r"^\s*-\s+\*\*([一-鿿])\*\*", line)
        if m:
            if current:
                out.append(current)
            current = {
                "id": f"n5.kanji.{m.group(1)}",
                "glyph": m.group(1),
                "on": [],
                "kun": [],
                "meanings": [],
                "stroke_order_svg": f"svg/kanji/{m.group(1)}.svg",
            }
            continue
        if current is None:
            continue
        on_m = re.match(r"^\s*-\s*On\s*:\s*(.+)$", line)
        if on_m:
            raws = [r.strip() for r in on_m.group(1).split(",")]
            current["on"] = [kata_to_hira(r) for r in raws if r and r != "-"]
            continue
        kun_m = re.match(r"^\s*-\s*Kun\s*:\s*(.+)$", line)
        if kun_m:
            raws = [r.strip() for r in kun_m.group(1).split(",")]
            cleaned = []
            seen = set()
            for r in raws:
                if not r or r == "-":
                    continue
                # Strip okurigana parentheses to get the bare reading.
                core = re.sub(r"\(.*?\)", "", r).strip()
                if core and core not in seen:
                    seen.add(core)
                    cleaned.append(core)
            current["kun"] = cleaned
            continue
        mn_m = re.match(r"^\s*-\s*Meaning\s*:\s*(.+)$", line)
        if mn_m:
            # Strip ALL parens (including nested) by repeatedly applying the
            # innermost match until none remain. Pre-fix bug (Pass 11):
            # `meaning: above (のぼ(る) "climb" is N4+; standard form is 登る)`
            # has nested parens; a single regex pass left
            # `above  "climb" is N4+; standard form is 登る)` and the trailing
            # commentary survived as fake "meanings".
            mtext = mn_m.group(1)
            prev = None
            while prev != mtext:
                prev = mtext
                mtext = re.sub(r"\([^()]*\)", " ", mtext)
            # Drop any stray closing parens left over from malformed entries.
            mtext = mtext.replace(")", "").replace("(", "").strip()
            # Strip trailing dash-prefixed authoring clause like
            # " - primary N5 use is in compounds...".
            mtext = re.split(r"\s+-\s+", mtext, maxsplit=1)[0].strip()
            # Drop entries that smell like leftover annotations (contain
            # "is N4+", quoted hints, or stray English author notes).
            BAD_MEANING_MARKERS = ("is N4+", "is N4 +", "standard form", "primary N5 use")
            current["meanings"] = [
                p.strip() for p in re.split(r"[/,;]", mtext)
                if p.strip() and not any(b in p for b in BAD_MEANING_MARKERS)
            ]
        # End of entry on blank line or new heading
        if not line.strip() or line.startswith("##"):
            if current:
                out.append(current)
                current = None
    if current:
        out.append(current)
    return out


def extract_vocab(md_path: Path) -> list[str]:
    """Pull vocab tokens from bullet entries like '- 学生 (がくせい) - student'."""
    text = md_path.read_text(encoding="utf-8")
    vocab = set()
    for line in text.splitlines():
        m = re.match(r"^\s*-\s+([^\s\(-]+)", line)
        if not m:
            continue
        tok = m.group(1).strip()
        if not tok:
            continue
        # Keep only tokens that contain at least one Japanese character.
        has_jp = any(
            "぀" <= ch <= "ヿ" or "一" <= ch <= "鿿"
            for ch in tok
        )
        if has_jp:
            vocab.add(tok)
    return sorted(vocab)


# Regex for full vocab entries: '- 学生 (がくせい) - student' or '- あなた - you'
# captures: form, optional reading, gloss
VOCAB_LINE_RE = re.compile(
    r"^\s*-\s+(?P<form>[^\s\(\-]+)\s*(?:\((?P<reading>[^)]+)\))?\s*[-]\s*(?P<gloss>.+?)$"
)


def extract_vocab_corpus(md_path: Path) -> list[dict]:
    """Parse vocabulary_n5.md into rich vocab records.

    Returns list of:
        {"form": str, "reading": str|None, "gloss": str, "section": str, "id": str}

    The "section" is the most recent ## heading.
    """
    text = md_path.read_text(encoding="utf-8")
    out = []
    section = ""
    seen_ids = set()
    for raw in text.splitlines():
        line = raw.rstrip()
        h = re.match(r"^##\s+(.+?)\s*$", line)
        if h:
            section = h.group(1).strip()
            continue
        m = VOCAB_LINE_RE.match(line)
        if not m:
            continue
        form = m.group("form").strip()
        reading = (m.group("reading") or "").strip() or None
        gloss = m.group("gloss").strip()
        # Pass-14 §3.3: for hiragana-only forms (no kanji), set reading = form
        # so consumers (SRS, TTS, search) always have a usable reading field.
        # Without this, ~795 kana-only vocab entries had reading=null and
        # required null-check defenses scattered across the app.
        if reading is None and form and not any("一" <= c <= "鿿" for c in form):
            reading = form
        # Strip catalog tag markers like **[Ext]** / **[Cul]** / **[Adv]** so
        # they don't leak into the user-facing gloss. The tags are author-side
        # metadata for scope tracking, not translations. Pass-11 finding C-5.
        gloss = re.sub(r"\s*\*\*\[(?:Ext|Cul|Adv)\]\*\*\s*$", "", gloss).strip()
        gloss = re.sub(r"\s*\*\*\[(?:Ext|Cul|Adv)\]\*\*\s*", " ", gloss).strip()
        if not form:
            continue
        # Require Japanese in the form
        if not any("぀" <= c <= "ヿ" or "一" <= c <= "鿿" for c in form):
            continue
        # Stable id: section slug + form. If duplicate, append index.
        slug = re.sub(r"[^a-z0-9]+", "-", section.lower()).strip("-")[:24] or "misc"
        base_id = f"n5.vocab.{slug}.{form}"
        vid = base_id
        i = 2
        while vid in seen_ids:
            vid = f"{base_id}.{i}"
            i += 1
        seen_ids.add(vid)
        out.append({
            "id": vid,
            "form": form,
            "reading": reading,
            "gloss": gloss,
            "section": section,
        })
    return out


def _diff_lists(kb_items, live_items, label):
    """Report drift between KB-extracted and live whitelist."""
    kb_set = set(kb_items)
    live_set = set(live_items)
    in_kb_only = sorted(kb_set - live_set)
    in_live_only = sorted(live_set - kb_set)
    if not in_kb_only and not in_live_only:
        print(f"  {label}: KB and live match ({len(live_items)} items)")
        return 0
    print(f"  {label}: DRIFT -- KB has {len(kb_items)}, live has {len(live_items)}")
    if in_kb_only:
        print(f"    in KB only ({len(in_kb_only)}): {in_kb_only[:20]}{'...' if len(in_kb_only) > 20 else ''}")
    if in_live_only:
        print(f"    in live only ({len(in_live_only)}): {in_live_only[:20]}{'...' if len(in_live_only) > 20 else ''}")
    return len(in_kb_only) + len(in_live_only)


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--write",
        action="store_true",
        help="DANGEROUS: overwrite live whitelist files with KB-extracted scope. "
             "The whitelists are hand-tuned in this repo; running with --write "
             "would lose the hand-tuning. Default is comparison-only.",
    )
    args = parser.parse_args()

    kanji_md = ROOT / "KnowledgeBank" / "kanji_n5.md"
    vocab_md = ROOT / "KnowledgeBank" / "vocabulary_n5.md"
    data_dir = ROOT / "data"

    if not kanji_md.exists():
        print(f"ERROR: missing {kanji_md}", file=sys.stderr)
        return 1
    if not vocab_md.exists():
        print(f"ERROR: missing {vocab_md}", file=sys.stderr)
        return 1

    kb_kanji = extract_kanji(kanji_md)
    kb_readings = extract_kanji_readings(kanji_md)
    kb_vocab = extract_vocab(vocab_md)

    if args.write:
        print("WARNING: --write mode will overwrite hand-tuned whitelist files.")
        print("Press Ctrl-C within 5 seconds to abort.")
        import time
        time.sleep(5)
        data_dir.mkdir(exist_ok=True)
        (data_dir / "n5_kanji_whitelist.json").write_text(
            json.dumps(kb_kanji, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Wrote {len(kb_kanji):>4} kanji to data/n5_kanji_whitelist.json")
        (data_dir / "n5_kanji_readings.json").write_text(
            json.dumps(kb_readings, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Wrote {len(kb_readings):>4} kanji readings to data/n5_kanji_readings.json")
        (data_dir / "n5_vocab_whitelist.json").write_text(
            json.dumps(kb_vocab, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        print(f"Wrote {len(kb_vocab):>4} vocab tokens to data/n5_vocab_whitelist.json")
        return 0

    # Comparison-only mode (default)
    print("KB-vs-live whitelist drift report (read-only; no writes)")
    print("-" * 60)
    drift = 0
    # Compare kanji whitelist
    live_kw_path = data_dir / "n5_kanji_whitelist.json"
    if live_kw_path.exists():
        live_kw = json.loads(live_kw_path.read_text(encoding="utf-8"))
        drift += _diff_lists(kb_kanji, live_kw, "kanji whitelist")
    else:
        print("  kanji whitelist: live file missing")
        drift += 1
    # Compare vocab whitelist (token list)
    live_vw_path = data_dir / "n5_vocab_whitelist.json"
    if live_vw_path.exists():
        live_vw = json.loads(live_vw_path.read_text(encoding="utf-8"))
        drift += _diff_lists(kb_vocab, live_vw, "vocab whitelist (tokens)")
    else:
        print("  vocab whitelist: live file missing")
        drift += 1
    # Kanji readings is a dict; compare keys + report value differences for shared keys
    live_kr_path = data_dir / "n5_kanji_readings.json"
    if live_kr_path.exists():
        live_kr = json.loads(live_kr_path.read_text(encoding="utf-8"))
        kb_keys = set(kb_readings.keys()) if isinstance(kb_readings, dict) else set()
        live_keys = set(live_kr.keys()) if isinstance(live_kr, dict) else set()
        only_kb = sorted(kb_keys - live_keys)
        only_live = sorted(live_keys - kb_keys)
        if only_kb or only_live:
            print(f"  kanji readings: KEY DRIFT -- KB has {len(kb_keys)}, live has {len(live_keys)}")
            if only_kb:
                print(f"    in KB only: {only_kb[:10]}")
            if only_live:
                print(f"    in live only: {only_live[:10]}")
            drift += len(only_kb) + len(only_live)
        else:
            # Same keys; check value drift on the primary-reading field
            same_keys_diff = 0
            for k in sorted(kb_keys):
                if kb_readings.get(k) != live_kr.get(k):
                    same_keys_diff += 1
            if same_keys_diff:
                print(f"  kanji readings: {same_keys_diff} entries differ in detail "
                      f"(expected -- hand-tuned for i-adj primary readings + dedup)")
            else:
                print(f"  kanji readings: KB and live match exactly")
    else:
        print("  kanji readings: live file missing")
        drift += 1
    print("-" * 60)
    if drift == 0:
        print("No structural drift between KB and live whitelist files.")
    else:
        print(f"Found {drift} structural-drift items (membership-level).")
        print("Decide manually whether KB or the whitelist needs updating.")
        print("Do NOT auto-resolve with --write (the whitelists are hand-tuned).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
