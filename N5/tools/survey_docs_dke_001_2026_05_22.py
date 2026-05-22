"""Survey: where does each of the 25 placeholder-rationale kanji
actually appear in the dokkai corpus? Inform the backfill rationale
for DOCS-DKE-001.

Scan: data/reading.json passages + data/papers/dokkai/paper-*.json
question stems/choices/rationales. Output for each kanji: list of
(passage_id / question_id, surface context).
"""
import sys, io, json, glob, os, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

PLACEHOLDERS = ["京", "作", "使", "同", "回", "図", "妹", "家", "弁", "当",
                "思", "教", "朝", "楽", "犬", "病", "紙", "終", "自", "近",
                "阪", "院", "青", "館", "黒"]


def context_window(text: str, kanji: str, width: int = 25) -> list[str]:
    """Find each occurrence of `kanji` in `text` and return a window
    of `width` chars on each side."""
    results = []
    for m in re.finditer(re.escape(kanji), text or ""):
        start = max(0, m.start() - width)
        end = min(len(text), m.end() + width)
        snippet = text[start:end].replace("\n", " ").strip()
        results.append(snippet)
        if len(results) >= 3:
            break
    return results


def main():
    findings: dict[str, list] = {k: [] for k in PLACEHOLDERS}

    # 1. Scan dokkai paper files (passages + question stems + rationales)
    for fp in sorted(glob.glob("data/papers/dokkai/paper-*.json")):
        d = json.load(open(fp, encoding="utf-8"))
        # Passages
        for p in d.get("passages", []) or []:
            text = p.get("text", "") or ""
            label = p.get("label", "?")
            for k in PLACEHOLDERS:
                if k in text:
                    for ctx in context_window(text, k):
                        findings[k].append(("passage", f"{os.path.basename(fp)}#{label}", ctx))
        # Questions
        for q in d.get("questions", []) or []:
            qid = q.get("id", "?")
            surfaces = [
                ("stem", q.get("stem_html", "") or ""),
                ("answer", q.get("correctAnswer", "") or ""),
                ("rationale", q.get("rationale", "") or ""),
            ]
            for cls, text in surfaces:
                for k in PLACEHOLDERS:
                    if k in text:
                        for ctx in context_window(text, k, width=20):
                            findings[k].append((cls, qid, ctx))

    # 2. Scan reading.json passages
    r = json.load(open("data/reading.json", encoding="utf-8"))
    passages = r if isinstance(r, list) else r.get("passages", r.get("entries", []))
    for p in passages:
        if not isinstance(p, dict):
            continue
        text = p.get("text", "") or p.get("body", "") or ""
        pid = p.get("id", "?")
        for k in PLACEHOLDERS:
            if k in text:
                for ctx in context_window(text, k):
                    findings[k].append(("reading", pid, ctx))

    # Report per-kanji
    for k in PLACEHOLDERS:
        hits = findings[k]
        print(f"=== {k} ({len(hits)} hits) ===")
        # Show up to 5 unique-ish context snippets
        seen = set()
        for cls, loc, ctx in hits[:8]:
            key = ctx[:30]
            if key in seen:
                continue
            seen.add(key)
            print(f"  [{cls}] {loc}: ...{ctx}...")
        print()


if __name__ == "__main__":
    main()
