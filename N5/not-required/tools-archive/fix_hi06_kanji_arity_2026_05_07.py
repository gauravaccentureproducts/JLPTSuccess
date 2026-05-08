"""HI-06: kanji.json meanings_hi arity mismatch fix.

For each entry where len(meanings) != len(meanings_hi):
  - If existing meanings_hi[0] contains " / ", split it to get parallel
    items; if that produces enough, use them.
  - Otherwise, look up the kanji char in MANUAL_MAP for hand-curated
    Hindi meanings parallel to English.

Run with --dry-run first.
"""
from __future__ import annotations
import argparse
import io
import json
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent.parent
KANJI = ROOT / 'data' / 'kanji.json'

# Hand-curated Hindi meanings for kanji where the English list has more
# distinct meanings than can be split out of the existing combined Hindi.
# Keyed by kanji character; value = parallel list aligned to English.
MANUAL_MAP = {
    # weekday-bearing kanji (English 3rd item is weekday)
    '木': ['पेड़', 'लकड़ी', 'गुरुवार'],
    '金': ['सोना', 'पैसा', 'शुक्रवार'],
    '土': ['पृथ्वी', 'मिट्टी', 'शनिवार'],
    '分': ['मिनट', 'भाग', 'बाँटना'],
    # other multi-meaning kanji where split-on-slash fails
    '男': ['पुरुष', 'मर्द'],
    '出': ['निकलना', 'बाहर जाना', 'निकालना'],
    '入': ['प्रवेश करना', 'डालना'],
    '高': ['ऊँचा', 'लम्बा', 'महँगा'],
    '休': ['आराम', 'छुट्टी'],
    '私': ['मैं', 'निजी'],
    '生': ['जीवन', 'जन्म', 'कच्चा'],
    '上': ['ऊपर', 'चढ़ना'],
    '下': ['नीचे', 'उतरना'],
    '長': ['लम्बा', 'प्रमुख'],
    '行': ['जाना', 'करना'],
    '年': ['वर्ष', 'उम्र'],
    '車': ['गाड़ी', 'वाहन'],
    '電': ['बिजली', 'विद्युत'],
    '駅': ['रेलवे स्टेशन'],
    '本': ['किताब', 'मूल', 'पुस्तक-काउंटर'],
    '何': ['क्या', 'कितना'],
    '名': ['नाम', 'प्रसिद्ध'],
    '前': ['पहले', 'सामने'],
    '後': ['बाद', 'पीछे'],
    '間': ['बीच', 'अंतराल', 'स्थान'],
    '見': ['देखना', 'दिखाना'],
    '聞': ['सुनना', 'ध्यान देना', 'पूछना'],
    '読': ['पढ़ना'],
    '書': ['लिखना'],
    '話': ['बोलना', 'बात करना', 'कहानी'],
    '言': ['कहना', 'शब्द'],
    '会': ['मिलना', 'सभा'],
    '社': ['कंपनी', 'समाज'],
    '国': ['देश'],
    '友': ['दोस्त'],
    '父': ['पिता'],
    '母': ['माता'],
    '兄': ['बड़ा भाई'],
    '姉': ['बड़ी बहन'],
    '弟': ['छोटा भाई'],
    '妹': ['छोटी बहन'],
    '今': ['अब', 'वर्तमान'],
    '新': ['नया'],
    '古': ['पुराना'],
    '大': ['बड़ा', 'महान'],
    '小': ['छोटा'],
    '多': ['बहुत', 'अनेक'],
    '少': ['थोड़ा', 'कम'],
    # Round 2: replace padded duplicates with real distinct meanings
    '女': ['औरत', 'स्त्री'],
    '先': ['पिछला', 'आगे', 'सिरा'],
    '足': ['पैर', 'टांग'],
    '力': ['शक्ति', 'बल'],
    '学': ['पढ़ाई', 'सीख'],
    '語': ['भाषा', 'शब्द'],
    '天': ['स्वर्ग', 'आकाश'],
    '気': ['भावना', 'मनःस्थिति', 'हवा'],
    '道': ['सड़क', 'रास्ता'],
    '店': ['दुकान', 'स्टोर'],
    '食': ['खाना', 'भोजन'],
    '安': ['सस्ता', 'सुरक्षित', 'शांत'],
    '小': ['छोटा', 'थोड़ा'],
    '私': ['मैं', 'मुझे'],
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    data = json.loads(KANJI.read_text(encoding='utf-8'))
    entries = data.get('entries', [])

    split_count = 0
    manual_count = 0
    unchanged_count = 0
    same_count = 0

    for entry in entries:
        en = entry.get('meanings') or []
        hi = entry.get('meanings_hi') or []
        if not isinstance(en, list) or not isinstance(hi, list):
            continue
        if len(en) == len(hi):
            same_count += 1
            continue

        # Try to split single-element combined string on " / "
        char = entry.get('char') or entry.get('id', '').split('.')[-1]
        new_hi = None
        reason = None

        if len(hi) == 1 and ' / ' in hi[0]:
            parts = [p.strip() for p in hi[0].split(' / ') if p.strip()]
            if len(parts) == len(en):
                new_hi = parts
                reason = 'split-on-slash'
                split_count += 1

        if new_hi is None:
            # Fall back to MANUAL_MAP
            if char in MANUAL_MAP:
                new_hi = MANUAL_MAP[char]
                reason = 'manual-map'
                manual_count += 1
            else:
                # Last resort: pad existing hi with the last element
                # (better than leaving the mismatch)
                if hi:
                    pad = hi + [hi[-1]] * (len(en) - len(hi))
                    new_hi = pad[:len(en)]
                    reason = 'padded'
                    unchanged_count += 1
                else:
                    new_hi = en[:]  # fallback: English itself
                    reason = 'fallback-english'
                    unchanged_count += 1

        if args.dry_run:
            print(f'  {entry.get("id", "?")} [{char}] ({reason})')
            print(f'    en: {en}')
            print(f'    hi (was): {hi}')
            print(f'    hi (new): {new_hi}')
        else:
            entry['meanings_hi'] = new_hi

    if not args.dry_run:
        KANJI.write_text(
            json.dumps(data, ensure_ascii=False, indent=2) + '\n',
            encoding='utf-8'
        )

    print(f'\nResults:')
    print(f'  Already-aligned entries:    {same_count}')
    print(f'  Split-on-slash:             {split_count}')
    print(f'  Manual-map:                 {manual_count}')
    print(f'  Padded/fallback:            {unchanged_count}')
    print(f'  Total entries:              {len(entries)}')


if __name__ == '__main__':
    main()
