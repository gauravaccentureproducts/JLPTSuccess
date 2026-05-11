"""Fill the 9 missing summary_hi entries on data/reading.json
(passages n5.read.046..054).

Audit context: the 2026-05-09 richness audit (Section: Reading) flagged
9/54 passages still lacking `summary_hi`. The remaining 45 carry
native_reviewed Hindi summaries; these 9 went unfilled when the
late-passage authoring batch shipped.

Each summary is 1-2 sentences in Devanagari, capturing the gist
of the passage. Provenance is `llm_curated` (not native_reviewed)
since these are LLM-authored, not native-reviewed.

JA-41 compliance: when Hindi prose embeds Japanese terms with
Japanese particles, the particles stay in kana attached to the
Japanese term (e.g., ふじ山に, not ふजी山 के). This script's
drafts respect that — every Hindi grammatical postposition is
attached to a Hindi term, not a Japanese one.
"""
from __future__ import annotations
import io, json, shutil, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
while not (ROOT / 'data').exists() and ROOT != ROOT.parent:
    ROOT = ROOT.parent
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

DRAFTS = {
    'n5.read.046': "जापान के पूर्व में अमेरिका और पश्चिम में चीन है — देश में पहाड़, नदियाँ और धान के खेत भी हैं। उत्तरी पहाड़ ふじ山 बहुत ऊँचा और सुंदर है; लेखक अगले साल वहाँ जाना चाहता है।",
    'n5.read.047': "घर के पास एक नया स्टेशन है — स्टेशन से निकलकर बायें मुड़ने पर एक सस्ती दुकान मिलती है, जहाँ दरवाज़े पर खड़े वृद्ध मालिक हमेशा सज्जन हैं। सड़क के पार एक बड़ी दुकान भी है, महँगी पर तरह-तरह का सामान।",
    'n5.read.048': "तानाका का अपने मित्र यामादा को छोटा पत्र — हाल-चाल पूछना, फ़ोन-नम्बर माँगना और साथ बात करने की इच्छा व्यक्त करना।",
    'n5.read.049': "सुबह से बारिश थी, इसलिए लेखक घर के अंदर किताब पढ़ रहा था। दोपहर के बाद बारिश थमी, आसमान साफ़ हुआ — पार्क में जाकर खिले हुए फूल देखे। वसंत उसका सबसे प्रिय मौसम है।",
    'n5.read.050': "लेखक की कम्पनी में बीस पुरुष और तीस महिला कर्मचारी हैं। नाकायामा बड़े-कद के बलवान हैं, ओगावा छोटी-कद की पर बहुत फुर्तीली। सब लोग ज़ोर से बात करते हैं — साथ काम करना मज़ेदार है।",
    'n5.read.051': "लेखक ने आज सुबह सूपरमार्केट में ख़रीदारी की — एक सेब 100 येन के हिसाब से चार सेब और 200 येन की डबलरोटी। कुल मिलाकर लगभग 1000 येन में बहुत-कुछ ख़रीद लिया, इसलिए वह ख़ुश था।",
    'n5.read.052': "लेखक अपने मित्र के साथ स्कूल में पढ़ाई करता है — सुबह ऊपरी मंज़िल की कक्षा में जापानी, दोपहर निचली मंज़िल की कक्षा में अंग्रेज़ी। साथ रहकर हर दिन बहुत आनंददायक लगता है।",
    'n5.read.053': "लेखक ने आज पार्क में लम्बे समय तक दौड़ लगाई — अब पैर बहुत दुख रहे हैं, हाथ और आँखें भी थकी हुई हैं। कल आराम करने का इरादा है।",
    'n5.read.054': "अगले महीने लेखक अपने परिवार के साथ दक्षिणी द्वीप की यात्रा पर जा रहा है — द्वीप बहुत लम्बा है, समुद्र सुंदर। लगभग 10,000 येन में यात्रा हो जाती है। दक्षिण गरम होगा, मज़ा आएगा।",
}

def main() -> int:
    fp = ROOT / 'data' / 'reading.json'
    bak = fp.with_suffix('.json.bak_2026_05_11_summary_hi_fill')
    if not bak.exists():
        shutil.copy2(fp, bak)
        print(f'Backup: {bak.name}')

    data = json.loads(fp.read_text(encoding='utf-8'))
    by_id = {p['id']: p for p in data['passages']}

    n = 0
    for pid, summary in DRAFTS.items():
        if pid not in by_id:
            print(f'  ! missing in data: {pid}')
            continue
        p = by_id[pid]
        if p.get('summary_hi'):
            print(f'  - skip (already filled): {pid}')
            continue
        p['summary_hi'] = summary
        p['summary_hi_provenance'] = 'llm_curated'
        n += 1
        print(f'  + {pid}: {summary[:60]}...')

    fp.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(f'\nFilled {n} summary_hi entries.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
