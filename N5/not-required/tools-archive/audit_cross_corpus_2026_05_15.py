"""Wave 1 — Cross-corpus consistency audit.

For every kanji + vocabulary term referenced or quoted across the 12
content corpora, detect inconsistencies in reading / gloss.

Canonical source-of-truth ordering (highest authority first):
  1. data/vocab.json       (canonical for vocab readings + glosses)
  2. data/kanji.json        (canonical for kanji on/kun/primary)
  3. data/n5_kanji_readings.json (canonical for kanji readings, hiragana form)

Other corpora are CONSUMERS — their inline readings / glosses must
agree with the canonical sources.

Checks:
  X1  vocab_preview (reading.json) reading != vocab.json reading for
      the same vocab_id
  X2  vocab_preview gloss_en != vocab.json gloss for the same vocab_id
  X3  vocab_preview gloss_hi != vocab.json gloss_hi for the same vocab_id
  X4  vocab_glossary (listening.json) reading != vocab.json reading
  X5  vocab_glossary gloss != vocab.json gloss
  X6  examples within kanji.json reference compounds (e.g., 大学) — the
      reading attached should agree with vocab.json if that compound
      is in vocab.json
  X7  authentic.json reading field != vocab.json reading for any
      vocab_refs target
"""
from __future__ import annotations
import json
from collections import defaultdict
from pathlib import Path


def load_vocab_index():
    v = json.loads(Path("data/vocab.json").read_text(encoding="utf-8"))
    idx = {}
    by_form = defaultdict(list)
    for e in v["entries"]:
        idx[e["id"]] = e
        f = e.get("form", "")
        if f:
            by_form[f].append(e)
    return idx, by_form


def load_kanji_index():
    k = json.loads(Path("data/kanji.json").read_text(encoding="utf-8"))
    return {e["glyph"]: e for e in k["entries"]}


def main():
    vocab_idx, vocab_by_form = load_vocab_index()
    kanji_idx = load_kanji_index()

    findings = defaultdict(list)

    # --- reading.json: vocab_preview entries ---
    rd = json.loads(Path("data/reading.json").read_text(encoding="utf-8"))
    for p in rd.get("passages", []):
        pid = p.get("id", "?")
        for item in (p.get("vocab_preview") or []):
            # vocab_preview may be either a dict (full preview) or a
            # bare string (vocab_id). Only the dict form carries
            # inline reading/gloss that we can verify against vocab.json.
            if isinstance(item, str):
                # bare id reference — nothing to cross-check
                if item not in vocab_idx:
                    findings["X0-UNRESOLVED-VOCAB-ID"].append((pid, item))
                continue
            if not isinstance(item, dict):
                continue
            vid = item.get("vocab_id")
            if not vid:
                continue
            canonical = vocab_idx.get(vid)
            if not canonical:
                findings["X0-UNRESOLVED-VOCAB-ID"].append((pid, vid))
                continue
            # Check reading
            it_read = (item.get("reading") or "").strip()
            v_read = (canonical.get("reading") or "").strip()
            # Allow multi-reading display like "ふん / ぷん"
            if it_read and v_read and it_read != v_read:
                # Normalize: strip spaces and check substring match
                v_readings = set([v_read] + list(canonical.get("readings", []) or []))
                tokens = [t.strip() for t in it_read.replace("/", " ").split() if t.strip()]
                if not all(tok in v_readings for tok in tokens):
                    findings["X1-VOCAB-PREVIEW-READING-MISMATCH"].append(
                        (pid, vid, it_read, v_read)
                    )
            # Check gloss EN
            it_gloss = (item.get("gloss") or "").strip()
            v_gloss = (canonical.get("gloss") or "").strip()
            if it_gloss and v_gloss and it_gloss != v_gloss:
                findings["X2-VOCAB-PREVIEW-GLOSS-EN-MISMATCH"].append(
                    (pid, vid, it_gloss, v_gloss)
                )
            # Check gloss HI
            it_gloss_hi = (item.get("gloss_hi") or "").strip()
            v_gloss_hi = (canonical.get("gloss_hi") or "").strip()
            if it_gloss_hi and v_gloss_hi and it_gloss_hi != v_gloss_hi:
                findings["X3-VOCAB-PREVIEW-GLOSS-HI-MISMATCH"].append(
                    (pid, vid, it_gloss_hi, v_gloss_hi)
                )

    # --- listening.json: vocab_glossary entries ---
    ls = json.loads(Path("data/listening.json").read_text(encoding="utf-8"))
    for it in ls.get("items", []):
        iid = it.get("id", "?")
        for gx in (it.get("vocab_glossary") or []):
            if isinstance(gx, str):
                if gx not in vocab_idx:
                    findings["X0-UNRESOLVED-VOCAB-ID"].append((iid, gx))
                continue
            if not isinstance(gx, dict):
                continue
            vid = gx.get("vocab_id")
            if not vid:
                continue
            canonical = vocab_idx.get(vid)
            if not canonical:
                findings["X0-UNRESOLVED-VOCAB-ID"].append((iid, vid))
                continue
            r = (gx.get("reading") or "").strip()
            v_read = (canonical.get("reading") or "").strip()
            if r and v_read and r != v_read:
                v_readings = set([v_read] + list(canonical.get("readings", []) or []))
                tokens = [t.strip() for t in r.replace("/", " ").split() if t.strip()]
                if not all(tok in v_readings for tok in tokens):
                    findings["X4-VOCAB-GLOSSARY-READING-MISMATCH"].append(
                        (iid, vid, r, v_read)
                    )
            g = (gx.get("gloss") or "").strip()
            vg = (canonical.get("gloss") or "").strip()
            if g and vg and g != vg:
                findings["X5-VOCAB-GLOSSARY-GLOSS-MISMATCH"].append(
                    (iid, vid, g, vg)
                )

    # --- authentic.json: vocab_refs ---
    # NOTE: authentic.json `reading` field is the FULL read-aloud of the
    # card's `ja` field (which is the full signage / menu phrase). The
    # `vocab_refs` list just names which vocab entries appear inside.
    # Therefore we only cross-check reading when ja IS a single vocab
    # word (ja == one of the candidate vocab forms). Multi-word signage
    # like 'コーヒー 350円' is intentionally a full-phrase reading.
    au = json.loads(Path("data/authentic.json").read_text(encoding="utf-8"))
    for it in au.get("items", []):
        iid = it.get("id", "?")
        refs = it.get("vocab_refs") or []
        if len(refs) != 1:
            continue
        vid = refs[0] if isinstance(refs[0], str) else refs[0].get("vocab_id")
        if not vid:
            continue
        canonical = vocab_idx.get(vid)
        if not canonical:
            findings["X0-UNRESOLVED-VOCAB-ID"].append((iid, vid))
            continue
        ja = (it.get("ja") or "").strip()
        v_form = (canonical.get("form") or "").strip()
        # Strict reading-match only applies when the card IS the single
        # vocab word (ja matches the canonical form). Otherwise it's a
        # multi-word signage card and reading is the phrase-level
        # read-aloud — not a vocab reading mismatch.
        if ja != v_form:
            continue
        r = (it.get("reading") or "").strip()
        v_read = (canonical.get("reading") or "").strip()
        if r and v_read and r != v_read:
            v_readings = set([v_read] + list(canonical.get("readings", []) or []))
            if r not in v_readings:
                findings["X7-AUTHENTIC-READING-MISMATCH"].append(
                    (iid, vid, r, v_read)
                )

    # --- kanji.json examples cross-check vs vocab.json ---
    for glyph, e in kanji_idx.items():
        for ex in e.get("examples", []) or []:
            form = (ex.get("form") or "").strip()
            reading = (ex.get("reading") or "").strip()
            gloss = (ex.get("gloss") or "").strip()
            if not form:
                continue
            vocab_candidates = vocab_by_form.get(form, [])
            if not vocab_candidates:
                continue  # word not in vocab — fine
            # If only one candidate, check directly
            v = vocab_candidates[0] if len(vocab_candidates) == 1 else None
            if not v:
                continue
            v_read = (v.get("reading") or "").strip()
            v_readings = set([v_read] + list(v.get("readings", []) or []))
            if reading and v_read and reading != v_read:
                # tolerate "ふん / ぷん" style
                tokens = [t.strip() for t in reading.replace("/", " ").split() if t.strip()]
                if not all(tok in v_readings for tok in tokens):
                    findings["X6-KANJI-EXAMPLE-READING-MISMATCH"].append(
                        (glyph, form, reading, v_read)
                    )

    # Report
    print("=" * 72)
    print("WAVE 1 — CROSS-CORPUS CONSISTENCY AUDIT")
    print("=" * 72)
    total = 0
    for cat in sorted(findings):
        rows = findings[cat]
        total += len(rows)
        print(f"\n{cat:42s} {len(rows)}")
        for r in rows[:6]:
            print(f"  {r}")
        if len(rows) > 6:
            print(f"  ... +{len(rows)-6} more")
    print(f"\nTOTAL FINDINGS: {total}")


if __name__ == "__main__":
    main()
