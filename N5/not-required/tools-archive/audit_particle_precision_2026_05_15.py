"""Wave 2 — Particle-precision L2-error audit.

Scans every Japanese sentence across all 12 content corpora for the
top L2-learner particle/grammar errors that a structural audit can
catch. Each pattern is a known N5/N4 L2 trap.

Patterns checked:

  P1  「Xを 好き」  — should be「Xが 好き」(stative-adj particle is が)
  P2  「Xを 上手」  — should be「Xが 上手」(skill is が)
  P3  「Xを 下手」  — same as 上手 — should be「Xが 下手」
  P4  「Xを きらい」 — should be「Xが きらい」(stative-adj が)
  P5  「Xを ほしい」 — should be「Xが ほしい」(desire-adj が)
  P6  「Xを 分かる/わかる」 — should be「Xが 分かる」(stative が)
  P7  「Xを いる」 / 「Xを ある」 — should be「Xが いる/ある」(existential が)
  P8  「Xに あげる」 (recipient が-particle wrong) — should be「Xに XをあげるY」
      actually: 「Yに Xを あげる」(に for recipient, を for object).
      Specifically flag「Xを あげる」 standalone where to-be-receiver is
      missing — but lots of false positives possible; defer.

  Particle pairs that often confuse:
  P9  「で」 used where「に」 is required for arrival points:
      「Xで 行く」 → should be「Xに 行く」 or「Xへ 行く」
  P10 「に」 used where「で」 is required for action-location:
      「Xに 食べる」 → should be「Xで 食べる」 (location of action)

  Spacing / orthography quirks:
  P11 「Xわ」 mid-sentence where it should be「Xは」 (topic marker)
      — N5 corpus uses は consistently; わ should not appear as a particle
"""
from __future__ import annotations
import json
import re
from collections import defaultdict
from pathlib import Path


def all_ja_sentences():
    """Yield (corpus, item_id, field_path, ja_text) for every Japanese
    sentence/phrase in the corpus."""
    # grammar.json — pattern.examples[].ja
    g = json.loads(Path("data/grammar.json").read_text(encoding="utf-8"))
    for p in g.get("patterns", []):
        pid = p.get("id", "?")
        for i, ex in enumerate(p.get("examples") or []):
            ja = (ex.get("ja") or "").strip()
            if ja:
                yield ("grammar", pid, f"examples[{i}].ja", ja)
    # vocab.json — entry.examples[].ja
    v = json.loads(Path("data/vocab.json").read_text(encoding="utf-8"))
    for e in v.get("entries", []):
        vid = e.get("id", "?")
        for i, ex in enumerate(e.get("examples") or []):
            ja = (ex.get("ja") or "").strip()
            if ja:
                yield ("vocab", vid, f"examples[{i}].ja", ja)
    # kanji.json — entry.sentences[].ja
    k = json.loads(Path("data/kanji.json").read_text(encoding="utf-8"))
    for e in k.get("entries", []):
        kid = e.get("glyph", "?")
        for i, s in enumerate(e.get("sentences") or []):
            ja = (s.get("ja") or "").strip()
            if ja:
                yield ("kanji", kid, f"sentences[{i}].ja", ja)
    # reading.json — passage.ja + questions[].prompt_ja
    r = json.loads(Path("data/reading.json").read_text(encoding="utf-8"))
    for p in r.get("passages", []):
        pid = p.get("id", "?")
        ja = (p.get("ja") or "").strip()
        if ja:
            yield ("reading", pid, "ja", ja)
        for i, q in enumerate(p.get("questions") or []):
            stem = (q.get("prompt_ja") or "").strip()
            if stem:
                yield ("reading", pid, f"questions[{i}].prompt_ja", stem)
    # listening.json — script_ja + prompt_ja
    l = json.loads(Path("data/listening.json").read_text(encoding="utf-8"))
    for it in l.get("items", []):
        iid = it.get("id", "?")
        for fld in ("script_ja", "prompt_ja"):
            ja = (it.get(fld) or "").strip()
            if ja:
                yield ("listening", iid, fld, ja)
    # authentic.json — items[].ja
    a = json.loads(Path("data/authentic.json").read_text(encoding="utf-8"))
    for it in a.get("items", []):
        iid = it.get("id", "?")
        ja = (it.get("ja") or "").strip()
        if ja:
            yield ("authentic", iid, "ja", ja)
    # questions.json — question_ja
    q = json.loads(Path("data/questions.json").read_text(encoding="utf-8"))
    for qq in q.get("questions", []):
        qid = qq.get("id", "?")
        ja = (qq.get("question_ja") or "").strip()
        if ja:
            yield ("questions", qid, "question_ja", ja)
    # drills_auto.json — stem
    d = json.loads(Path("data/drills_auto.json").read_text(encoding="utf-8"))
    for qq in d.get("questions", []):
        did = qq.get("id", "?")
        ja = (qq.get("stem") or "").strip()
        if ja:
            yield ("drills", did, "stem", ja)
    # papers/*/paper-*.json — questions[].stem_html + passage_text
    for cat in ("dokkai", "bunpou", "goi", "moji"):
        pdir = Path(f"data/papers/{cat}")
        if not pdir.exists():
            continue
        for pf in sorted(pdir.glob("paper-*.json")):
            paper = json.loads(pf.read_text(encoding="utf-8"))
            for q in paper.get("questions") or []:
                qid = q.get("id", f"{pf.stem}.q?")
                for fld in ("stem_html", "passage_text"):
                    ja = (q.get(fld) or "").strip()
                    if ja:
                        yield (f"papers/{cat}", qid, f"{pf.name}.{fld}", ja)


# Particle-error patterns (regex)
PATTERNS = [
    # P1-P7: stative/desire/skill-adjectives demanding が, not を
    ("P1-WO-WITH-SUKI", re.compile(r"[をｦ]\s*(?:が\s*)?(?:大?好き|だいすき|すき)")),
    ("P2-WO-WITH-JOUZU", re.compile(r"[を]\s*(?:が\s*)?(?:じょうず|上手)")),
    ("P3-WO-WITH-HETA", re.compile(r"[を]\s*(?:が\s*)?(?:へた|下手)")),
    ("P4-WO-WITH-KIRAI", re.compile(r"[を]\s*(?:が\s*)?(?:嫌い|きらい)")),
    ("P5-WO-WITH-HOSHII", re.compile(r"[を]\s*(?:が\s*)?(?:ほしい|欲しい)")),
    ("P6-WO-WITH-WAKARU", re.compile(r"[を]\s*(?:が\s*)?(?:わか(?:り|る|れ)|分か(?:り|る|れ))")),
    ("P7-WO-WITH-ARU-IRU",
     re.compile(r"[をｦ]\s*(?:が\s*)?(?:あります|います|ある|いる)\b")),
    # Conjugation errors
    # P8: i-adjective with copula だ/です STACKED after い (overlapping
    # negation marker) — 〜くないだ is L2-error for 〜くない or 〜くないです
    ("P8-IADJ-NEG-WITH-DA", re.compile(r"(?<![ぁ-ゟ一-鿿])くないだ(?![け])")),
    # P9: double polite-past 「ましたした」
    ("P9-DOUBLE-MASHITA", re.compile(r"ました(?:した|ました)")),
    # P10: doubled です — 「ですです」
    ("P10-DOUBLE-DESU", re.compile(r"ですです")),
    # P11: double particle 「でに」or 「にで」 (illegal stacking in N5)
    # Exclude the compound adverb ひとりでに ("by oneself", fixed expr).
    ("P11-DOUBLE-PARTICLE-DENI", re.compile(r"(?<!ひとり)でに\s")),
    ("P11-DOUBLE-PARTICLE-NIDE", re.compile(r"にで\s")),
    # P12: na-adj with i-adj copula — 「きれいいです」
    ("P12-NAADJ-AS-IADJ", re.compile(r"きれいい|げんきい|しずかい")),
    # P13: 「行きました ました」 stutter
    ("P13-STUTTER-MASHITA", re.compile(r"きました\s+ました")),
    # P14: question marker stacked 「ですかか」or 「ますかか」
    ("P14-DOUBLE-KA", re.compile(r"(?:です|ます)かか")),
]


def main():
    findings = defaultdict(list)
    n_sentences = 0
    for corpus, iid, field, ja in all_ja_sentences():
        n_sentences += 1
        for tag, rx in PATTERNS:
            for m in rx.finditer(ja):
                findings[tag].append((corpus, iid, field, m.group(0), ja[:80]))
    print("=" * 72)
    print(f"WAVE 2 — PARTICLE-PRECISION AUDIT ({n_sentences} sentences scanned)")
    print("=" * 72)
    total = 0
    for cat in sorted(findings):
        rows = findings[cat]
        total += len(rows)
        print(f"\n{cat:30s} {len(rows)}")
        for r in rows[:6]:
            print(f"  {r}")
        if len(rows) > 6:
            print(f"  ... +{len(rows)-6} more")
    print(f"\nTOTAL: {total}")


if __name__ == "__main__":
    main()
