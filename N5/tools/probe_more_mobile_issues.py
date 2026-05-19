#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Probe additional mobile-UI issues not caught in primary run."""
import io, json, sys, time
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.add_argument("--window-size=360,800")
d = webdriver.Chrome(options=opts)
d.execute_cdp_cmd("Emulation.setDeviceMetricsOverride",
                   {"width": 360, "height": 800, "deviceScaleFactor": 2.0, "mobile": True})

# 1. Reading detail font + a11y
d.get("http://127.0.0.1:8765/#/reading")
time.sleep(2.5)
deep = d.execute_script(
    "var a = document.querySelector('a[href*=\\\"reading/\\\"]');"
    "return a ? a.getAttribute('href') : null;"
)
print(f"Reading deep href: {deep}")
if deep:
    d.get("http://127.0.0.1:8765/" + deep)
    time.sleep(3.0)
    info = d.execute_script("""
        var ps = document.querySelectorAll('#app p, #app .passage-body, #app .reading-passage, #app .passage');
        var out = [];
        for (var i = 0; i < Math.min(5, ps.length); i++) {
            out.push({
                fs: parseFloat(getComputedStyle(ps[i]).fontSize),
                lh: getComputedStyle(ps[i]).lineHeight,
                text: ps[i].textContent.trim().slice(0,40)
            });
        }
        return out;
    """)
    print(f"Reading detail paragraphs: {json.dumps(info, ensure_ascii=False, indent=2)}")

# 2. HI locale check
d.get("http://127.0.0.1:8765/#/home")
time.sleep(2.5)
d.execute_script("try { localStorage.setItem('n5.locale', 'en'); } catch(e){}")
d.refresh()
time.sleep(2.0)
lang_before = d.execute_script("return document.documentElement.lang")
print(f"\nBefore toggle: lang={lang_before}")
d.execute_script("var t=document.getElementById('locale-toggle'); if(t) t.click();")
time.sleep(1.5)
lang_after = d.execute_script("return document.documentElement.lang")
print(f"After toggle: lang={lang_after}")

# Sample nav text + body text in HI
hi_info = d.execute_script("""
    var nav = document.querySelector('nav.primary-nav');
    var sec = document.querySelector('nav.secondary-nav');
    return {
        nav_text: nav ? nav.innerText.slice(0,250) : null,
        secondary_aria: sec ? Array.from(sec.querySelectorAll('[aria-label]')).map(function(e){return e.getAttribute('aria-label');}) : null,
        body_start: (document.getElementById('app').innerText || '').slice(0, 400)
    };
""")
print(f"HI nav primary text: {hi_info['nav_text']}")
print(f"HI secondary aria-labels: {hi_info['secondary_aria']}")
print(f"HI body start: {hi_info['body_start']}")

# 3. Tab through home — does focus indicator render?
d.execute_script("try{localStorage.setItem('n5.locale','en');}catch(e){}")
d.refresh()
time.sleep(2.0)
d.get("http://127.0.0.1:8765/#/home")
time.sleep(2.0)
focus_check = d.execute_script("""
    var a = document.querySelector('a.study-order-link');
    if (!a) return null;
    a.focus();
    var cs = getComputedStyle(a);
    return {
        outline_width: cs.outlineWidth, outline_style: cs.outlineStyle,
        outline_color: cs.outlineColor, outline_offset: cs.outlineOffset,
        box_shadow: cs.boxShadow.slice(0,80),
        has_focus: document.activeElement === a
    };
""")
print(f"\nFocus outline on study-order-link: {focus_check}")

# 4. iOS auto-zoom check for ALL inputs
d.get("http://127.0.0.1:8765/#/feedback")
time.sleep(2.0)
inputs = d.execute_script("""
    var els = document.querySelectorAll('input, textarea, select');
    var out = [];
    for (var i = 0; i < els.length; i++) {
        var cs = getComputedStyle(els[i]);
        out.push({
            tag: els[i].tagName, type: els[i].getAttribute('type') || '',
            fs: parseFloat(cs.fontSize),
            id: els[i].id || '',
            name: els[i].name || '',
            placeholder: (els[i].getAttribute('placeholder') || '').slice(0,30)
        });
    }
    return out;
""")
print(f"\nInputs on #/feedback (font-size check):")
for i in inputs:
    flag = "" if i['fs'] >= 16 else "  <-- under 16px (iOS auto-zoom risk)"
    print(f"  <{i['tag']}> id={i['id']} name={i['name']} fs={i['fs']}{flag}")

# 5. Print route check
d.get("http://127.0.0.1:8765/#/print")
time.sleep(2.5)
print_info = d.execute_script("""
    return {
        hash: location.hash,
        body_data_route: document.body.getAttribute('data-route'),
        children: document.getElementById('app').children.length,
        text: (document.getElementById('app').innerText || '').slice(0,150)
    };
""")
print(f"\n#/print route: {print_info}")

# 6. Drill route - does it have an actual playable drill?
d.get("http://127.0.0.1:8765/#/drill")
time.sleep(2.5)
drill = d.execute_script("""
    var btns = document.querySelectorAll('#app button');
    var inputs = document.querySelectorAll('#app input');
    return {
        hash: location.hash, buttons: btns.length, inputs: inputs.length,
        body_text: (document.getElementById('app').innerText || '').slice(0,300)
    };
""")
print(f"\n#/drill route: {drill}")

# 7. Search input + autocomplete behavior
d.get("http://127.0.0.1:8765/#/home")
time.sleep(2.0)
s = d.execute_script("""
    var inp = document.getElementById('search-input');
    if (!inp) return {error: 'no input'};
    inp.focus();
    inp.value = 'taberu';
    inp.dispatchEvent(new Event('input', {bubbles: true}));
    return {focused: document.activeElement === inp, value: inp.value};
""")
print(f"\nSearch typing test: {s}")
time.sleep(1.5)
result_check = d.execute_script("""
    var possible = document.querySelectorAll('#search-results, .search-results, [role=listbox], .search-result, ul.search-list, .search-dropdown');
    var visible_count = 0;
    for (var i = 0; i < possible.length; i++) {
        var r = possible[i].getBoundingClientRect();
        if (r.width > 0 && r.height > 0) visible_count++;
    }
    return {selectors_matched: possible.length, visible: visible_count};
""")
print(f"Search result containers: {result_check}")

# 8. Locale-switch text expansion: check if HI nav overflows
d.get("http://127.0.0.1:8765/#/home")
time.sleep(2.0)
d.execute_script("try{localStorage.setItem('n5.locale','hi');}catch(e){}")
d.refresh()
time.sleep(2.0)
nav_overflow = d.execute_script("""
    var nav = document.querySelector('nav.primary-nav');
    if (!nav) return null;
    return {
        scrollWidth: nav.scrollWidth,
        clientWidth: nav.clientWidth,
        overflow: nav.scrollWidth > nav.clientWidth + 1,
        lang: document.documentElement.lang
    };
""")
print(f"\nHI nav overflow check: {nav_overflow}")

d.quit()
