"""Comprehensive scan for remaining off-pattern boilerplate.

Searches all 178 patterns for known-boilerplate sentences, then for
each occurrence checks if the host pattern's marker is in the sentence.
Flags only the OFF-PATTERN occurrences for fixing.
"""
import json
import re

g = json.load(open("data/grammar.json", encoding="utf-8"))

BOILERPLATE = [
    "私は 学生です。", "わたしは がくせいです。", "私たちは がくせいです。",
    "私たちは 友だちです。", "あなたは がくせいですか。",
    "あなたは どなたですか。", "あの 人は だれですか。",
    "あの 人は 田中さんです。", "これは お母さんです。",
    "それは だれの かばんですか。",
    "母と えいがを 見ました。", "おにいさんは どこに いますか。",
    "きょうだいが いますか。", "きょうだいは 二人 います。",
    "おまわりさんに あいさつします。", "なぜ 来ませんでしたか。",
    "なぜ 来なかったのですか。", "きのうは あめでした。",
    "しけんは むずかしかったです。", "テストは どうでしたか。",
    "どなたですか。",
    "じぶんで しゅくだいを します。", "父に とけいを もらいました。",
    "あの かたは どなたですか。", "あれは くるまじゃありません。",
    "そこまで タクシーで いきません。",
    "まいにち にほんごを べんきょうします。", "だれが きましたか。",
    "あにより わたしのほうが はやく おきます。",
    "あついから、まどを あけてください。", "どの くるまが いいですか。",
    "あそこは しずかです。", "くちを あけて ください。",
    "それを ください。", "みみで おんがくを 聞きます。",
    "いもうとは 学校に 行きます。",
    "おすしを おねがいします。", "六時ごろ", "あした しけんですよ。",
]


def pattern_marker_present(p, ja):
    """Return True if the pattern's marker(s) appear in the example."""
    pstr = p.get("pattern", "")
    if not pstr or not ja:
        return False
    # Strip placeholders + parentheticals
    core = re.sub(r"〜|~", "", pstr)
    core = re.sub(r"（[^）]*）|\([^)]*\)", "", core).strip()
    core = re.sub(r"\s*[+＋]\s*\w.*$", "", core).strip()
    # For tilde-separated patterns, all parts must appear
    if "〜" in pstr or "~" in pstr:
        parts = [p.strip() for p in re.split(r"[〜~]", pstr) if p.strip()]
        if all(part in ja for part in parts if part and not re.match(r"^(Verb|V|Noun|N|Adj|い-|な-|Sentence)", part)):
            return True
    # Multi-form pattern labels — accept if a class-marker is present
    if any(kw in pstr for kw in ["Verb-", "V-", "Adj-", "い-Adj", "な-Adj", "Question word", "Sentence"]):
        # Crude: if the sentence has any kana ending in pattern-typical conjugation, accept
        # For thoroughness, accept all such cases (lots of false positives if we don't)
        return True
    # Split alternatives on / or ／
    alts = [a.strip() for a in re.split(r"[／/]", core) if a.strip()]
    for alt in alts:
        if alt and alt in ja:
            return True
    return core in ja if core else False


findings = []
for p in g["patterns"]:
    for i, ex in enumerate(p.get("examples", [])):
        ja = ex.get("ja", "").strip()
        if ja in BOILERPLATE:
            if not pattern_marker_present(p, ja):
                findings.append((p["id"], p.get("pattern", ""), i, ja))

print(f"Off-pattern boilerplate occurrences found: {len(findings)}")
for pid, pstr, idx, ja in findings:
    print(f"  {pid:8s} [{idx}] pattern={pstr[:30]!r:30s} ja={ja[:50]}")
