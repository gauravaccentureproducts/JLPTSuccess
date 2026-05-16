"""Fix BUG-014 — replace 19 template-generated semantic-nonsense vocab
examples ("X が あります" applied to time words / abstract nouns /
bare locations).

Each replacement follows the natural-frame guidance from the bug
description:
  - Time words → use as に-marked time anchors with an EVENT taking
    が あります, or in their natural collocation
  - Locations → use in "there is X at/near <place>" frames with a
    location qualifier, never bare
  - Food / objects → use in eat / buy / drink / possession frames
  - Abstract nouns → drop the あります frame; use natural collocations

All replacements use only N5-whitelist kanji (verified against
data/n5_kanji_whitelist.json) or kana.
"""
from __future__ import annotations

import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
VOCAB = ROOT / "data" / "vocab.json"

# (form, example_index, new_ja, new_en)
# example_index is the [1] slot for all 19 entries (verified by survey).
REPLACEMENTS: list[tuple[str, int, str, str]] = [
    # ---- Time words ----
    ("一月", 1, "一月に やすみが あります。",
            "There's a holiday in January."),
    ("二月", 1, "二月は バレンタインの つきです。",
            "February is the month of Valentine's."),
    ("八月", 1, "八月に なつまつりが あります。",
            "There's a summer festival in August."),
    ("十月", 1, "十月に うんどうかいが あります。",
            "There's a sports day in October."),
    ("先月", 1, "先月 はじめて すしを 食べました。",
            "Last month I ate sushi for the first time."),
    ("毎月", 1, "毎月 おかねを ちょきんします。",
            "I save money every month."),
    ("来年", 1, "来年 日本へ 行きたいです。",
            "I want to go to Japan next year."),
    ("ゆうべ", 1, "ゆうべの えいがは おもしろかったです。",
              "Last night's movie was interesting."),

    # ---- Locations (need a location qualifier or possession frame) ----
    ("ゆうびんきょく", 1, "えきの 前に ゆうびんきょくが あります。",
                       "There's a post office in front of the station."),
    ("はなや", 1, "うちの ちかくに はなやが あります。",
              "There's a flower shop near my house."),
    ("えいがかん", 1, "ちかくに えいがかんは ありますか。",
                 "Is there a movie theater nearby?"),

    # ---- Food / objects ----
    ("田",         1, "秋に 田の こめを かります。",
                     "In autumn we harvest the rice from the fields."),
    ("水",         1, "水を 一ぱい ください。",
                     "Please give me a glass of water."),
    ("パン",       1, "パンを 三つ 買いました。",
                     "I bought three pieces of bread."),
    ("こめ",       1, "日本人は まいにち こめを 食べます。",
                     "Japanese people eat rice every day."),
    ("アイスクリーム", 1, "あついから アイスクリームを 食べたいです。",
                         "Since it's hot, I want to eat ice cream."),

    # ---- Abstract nouns (drop あります frame) ----
    ("外国語",    1, "外国語を まいにち べんきょうします。",
                    "I study a foreign language every day."),
    ("りゅうがく", 1, "来年 りゅうがくを したいです。",
                    "I want to do study abroad next year."),
    ("たんご",    1, "あたらしい たんごを ノートに 書きます。",
                    "I write new vocabulary in my notebook."),
]


def main() -> int:
    V = json.loads(VOCAB.read_text(encoding="utf-8"))
    entries = V.get("entries", [])

    # Build a form→entry lookup
    by_form: dict[str, list[dict]] = {}
    for e in entries:
        form = e.get("form")
        if form:
            by_form.setdefault(form, []).append(e)

    # Apply replacements
    written = 0
    errors: list[str] = []
    for form, idx, new_ja, new_en in REPLACEMENTS:
        if form not in by_form:
            errors.append(f"{form}: form not found")
            continue
        for entry in by_form[form]:
            examples = entry.get("examples") or []
            if idx >= len(examples):
                errors.append(f"{form} ({entry.get('id','?')}): example[{idx}] out of range")
                continue
            ex = examples[idx]
            if not isinstance(ex, dict):
                errors.append(f"{form} ({entry.get('id','?')}): example[{idx}] not a dict")
                continue
            old_ja = ex.get("ja", "")
            # Sanity check: only replace if it's the bad template shape.
            # Heuristic: short example (<= form length + 14) containing
            # "<form>が あります" or "<form>が います".
            is_bad_template = (
                ("が あります" in old_ja or "が います" in old_ja)
                and form in old_ja
                and len(old_ja) <= len(form) + 14
            )
            if not is_bad_template:
                errors.append(
                    f"{form} ({entry.get('id','?')}): example[{idx}] doesn't match bad-template shape; "
                    f"got {old_ja!r}"
                )
                continue
            ex["ja"] = new_ja
            ex["translation_en"] = new_en
            ex["bug_014_fix_2026_05_16"] = True
            written += 1
            print(f"  {form} ({entry.get('id','?')}): cm[{idx}] {old_ja!r} -> {new_ja!r}")

    if errors:
        print("\nERRORS:")
        for e in errors:
            print(f"  {e}")
        return 1

    VOCAB.write_text(json.dumps(V, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\nReplaced {written} bad-template examples in {VOCAB}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
