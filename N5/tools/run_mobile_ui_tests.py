#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Execute mobile-UI test scenarios from O. Mobile UI testing tab.

Approach:
1. Local server at 127.0.0.1:8765 (assumed already running per UI Tests
   convention; see specifications/JLPT-N5-Current-Implementation-Spec.md).
2. Chrome --headless=new with mobile-emulation via set_window_size +
   touch-emulation Emulation.setTouchEmulationEnabled CDP command.
3. Execute the automatable scenario subset. Each scenario is
   re-expressed as a deterministic check (CSS selector + assertion).
4. Collect (scenario_id, device, status, evidence). FAILs and
   anomalies are captured for bug-sheet writing.

This is NOT a complete execution of all 134 scenarios — it executes
the subset that's expressible as a single deterministic assertion
without soft-keyboard / IME / real-device gestures (those 16 Manual
scenarios are skipped with status='SKIP-MANUAL').

Writing-discipline note: results below are bounded by the assertions
this runner actually executed. A PASS means "this specific check
passed on this device profile"; it does not assert universal
correctness of the screen.

Run: python tools/run_mobile_ui_tests.py
"""
from __future__ import annotations

import io
import json
import sys
import time
import traceback
from pathlib import Path
from dataclasses import dataclass, field
from typing import Callable, Optional

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (TimeoutException, NoSuchElementException,
                                         WebDriverException, JavascriptException)

# UTF-8 on cp932 Windows
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

BASE = "http://127.0.0.1:8765"
DEVICES = {
    "D-320": (320, 568),
    "D-360": (360, 800),
    "D-375": (375, 667),
    "D-390": (390, 844),
    "D-414": (414, 896),
    "D-768": (768, 1024),
    "D-360L": (800, 360),
}

ROUTES_TO_VISIT = [
    "#/home", "#/learn", "#/learn/grammar", "#/learn/vocab",
    "#/kanji", "#/reading", "#/listening", "#/listening/story",
    "#/test", "#/sitting", "#/missed", "#/summary",
    "#/settings", "#/changelog", "#/privacy", "#/notices",
    "#/feedback", "#/diagnostic", "#/drill", "#/examday",
    "#/papers", "#/review", "#/weakareas", "#/strategy",
    "#/levels", "#/mining", "#/authentic",
]


@dataclass
class Result:
    scenario_id: str
    device: str
    status: str            # PASS, FAIL, ERROR, SKIP-MANUAL
    title: str
    expected: str
    actual: str
    evidence: str = ""
    severity: str = "Major"
    route: str = ""

    def is_fail(self) -> bool:
        return self.status in ("FAIL", "ERROR")


RESULTS: list[Result] = []


def log(r: Result) -> None:
    RESULTS.append(r)
    icon = {"PASS": "[+]", "FAIL": "[-]", "ERROR": "[!]", "SKIP-MANUAL": "[~]"}.get(r.status, "[?]")
    print(f"  {icon} {r.scenario_id:14s} {r.device:7s} {r.status:11s} {r.title[:60]}")
    if r.is_fail():
        print(f"      expected: {r.expected[:120]}")
        print(f"      actual:   {r.actual[:120]}")


def make_driver(width: int, height: int) -> webdriver.Chrome:
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument(f"--window-size={width},{height}")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    d = webdriver.Chrome(options=opts)
    d.set_window_size(width, height)
    # Touch emulation via CDP
    try:
        d.execute_cdp_cmd("Emulation.setTouchEmulationEnabled",
                          {"enabled": True, "maxTouchPoints": 1})
        d.execute_cdp_cmd("Emulation.setDeviceMetricsOverride", {
            "width": width, "height": height,
            "deviceScaleFactor": 2.0,
            "mobile": True,
        })
    except Exception:
        pass
    return d


def wait_for_app(driver, timeout=10):
    """Wait for skeleton to clear and #app to have rendered content."""
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script(
                "var s=document.querySelector('.skeleton-wrap');"
                "var a=document.getElementById('app');"
                "return (!s || s.offsetParent === null) "
                "  && a && a.children.length > 0;"
            )
        )
        return True
    except TimeoutException:
        return False


def js_safe(driver, script, default=None):
    try:
        return driver.execute_script(script)
    except (JavascriptException, WebDriverException):
        return default


# ---------------------------------------------------------------------------
# Per-scenario test functions. Each returns a Result.
# ---------------------------------------------------------------------------

def test_no_horizontal_scroll(driver, device, route, scenario_id) -> Result:
    """O-X-001..005: no horizontal scroll at viewport width."""
    driver.get(BASE + "/" + route)
    # Wait briefly for SPA to render route
    wait_for_app(driver, 8)
    time.sleep(0.5)
    sw = js_safe(driver, "return document.documentElement.scrollWidth")
    iw = js_safe(driver, "return window.innerWidth")
    passed = sw is not None and iw is not None and sw <= iw + 1  # +1 px slack
    return Result(
        scenario_id=scenario_id,
        device=device,
        route=route,
        title=f"No horizontal scroll on {route}",
        expected=f"scrollWidth <= innerWidth ({iw})",
        actual=f"scrollWidth = {sw}, innerWidth = {iw}",
        status="PASS" if passed else "FAIL",
        severity="Major" if not passed else "Major",
    )


def test_app_renders(driver, device, route, scenario_id) -> Result:
    """Generic: route loads without skeleton-permanent + has DOM content."""
    driver.get(BASE + "/" + route)
    ok = wait_for_app(driver, 8)
    children = js_safe(driver,
        "var a=document.getElementById('app'); return a ? a.children.length : 0", 0)
    has_error = js_safe(driver,
        "return document.body.innerText.toLowerCase().includes('error') "
        "&& document.body.innerText.toLowerCase().includes('not found')", False)
    passed = ok and children > 0
    return Result(
        scenario_id=scenario_id, device=device, route=route,
        title=f"Route {route} renders (skeleton clears, content present)",
        expected="skeleton hidden, #app has children",
        actual=f"skeleton-cleared={ok}, #app children={children}, error-text-detected={has_error}",
        status="PASS" if passed else "FAIL",
    )


def test_nav_links_present(driver, device, scenario_id) -> Result:
    """Header nav has all 9 primary links."""
    driver.get(BASE + "/")
    wait_for_app(driver, 8)
    routes_expected = ["learn/grammar", "learn/vocab", "kanji", "reading",
                       "listening", "test", "sitting", "missed", "summary"]
    found = []
    for r in routes_expected:
        n = js_safe(driver,
            f"return document.querySelectorAll(\"a[data-route='{r}']\").length", 0)
        if n and n > 0:
            found.append(r)
    missing = [r for r in routes_expected if r not in found]
    return Result(
        scenario_id=scenario_id, device=device,
        title="Primary nav has 9 links",
        expected=", ".join(routes_expected),
        actual=f"found {len(found)}/9; missing={missing}",
        status="PASS" if not missing else "FAIL",
    )


def test_search_input_font_size(driver, device, scenario_id) -> Result:
    """Search input font-size >= 16px (iOS auto-zoom prevention)."""
    driver.get(BASE + "/")
    wait_for_app(driver, 8)
    fs = js_safe(driver,
        "var e=document.getElementById('search-input');"
        "return e ? parseFloat(getComputedStyle(e).fontSize) : null")
    passed = fs is not None and fs >= 16
    return Result(
        scenario_id=scenario_id, device=device,
        title="Search input font-size >= 16px",
        expected=">= 16px",
        actual=f"{fs}px" if fs is not None else "input not found",
        status="PASS" if passed else "FAIL",
    )


def test_touch_target_size(driver, device, scenario_id) -> Result:
    """Every nav link is >= 44x44 CSS px."""
    driver.get(BASE + "/")
    wait_for_app(driver, 8)
    sizes = js_safe(driver, """
        var links = document.querySelectorAll('a[data-route]');
        var out = [];
        for (var i = 0; i < links.length; i++) {
            var r = links[i].getBoundingClientRect();
            out.push({route: links[i].getAttribute('data-route'),
                      w: Math.round(r.width), h: Math.round(r.height)});
        }
        return out;
    """, [])
    failing = [s for s in sizes if min(s["w"], s["h"]) < 44]
    return Result(
        scenario_id=scenario_id, device=device,
        title="All nav links >= 44x44 px",
        expected="min(w,h) >= 44 for every a[data-route]",
        actual=(f"{len(failing)} undersized: " +
                ", ".join(f"{s['route']}={s['w']}x{s['h']}" for s in failing[:5])
                if failing else f"all {len(sizes)} links pass"),
        status="PASS" if not failing else "FAIL",
        severity="Major",
    )


def test_locale_toggle(driver, device, scenario_id) -> Result:
    """Locale toggle is present + tappable + size >= 44px."""
    driver.get(BASE + "/")
    wait_for_app(driver, 8)
    info = js_safe(driver, """
        var e = document.getElementById('locale-toggle');
        if (!e) return null;
        var r = e.getBoundingClientRect();
        var label = e.querySelector('[data-locale-label]');
        return {
            w: Math.round(r.width), h: Math.round(r.height),
            label: label ? label.textContent.trim() : null
        };
    """, None)
    if info is None:
        return Result(scenario_id=scenario_id, device=device,
                      title="Locale toggle present", expected="exists",
                      actual="not found", status="FAIL")
    passed = info["w"] >= 44 and info["h"] >= 44
    return Result(
        scenario_id=scenario_id, device=device,
        title="Locale toggle is touch-friendly",
        expected="w/h >= 44px, label EN or HI",
        actual=f"w={info['w']}, h={info['h']}, label={info['label']}",
        status="PASS" if passed else "FAIL",
    )


def test_locale_persists(driver, device, scenario_id) -> Result:
    """Locale toggle change persists in localStorage + survives reload."""
    driver.get(BASE + "/")
    wait_for_app(driver, 8)
    initial_lang = js_safe(driver, "return document.documentElement.lang")
    # Tap toggle
    clicked = js_safe(driver, """
        var e = document.getElementById('locale-toggle');
        if (!e) return false;
        e.click();
        return true;
    """, False)
    time.sleep(0.6)
    after_lang = js_safe(driver, "return document.documentElement.lang")
    # Reload
    driver.refresh()
    wait_for_app(driver, 8)
    final_lang = js_safe(driver, "return document.documentElement.lang")
    passed = clicked and initial_lang != after_lang and after_lang == final_lang
    return Result(
        scenario_id=scenario_id, device=device,
        title="Locale toggle persists across reload",
        expected="lang changes on click + persists after reload",
        actual=f"clicked={clicked}, initial={initial_lang}, after={after_lang}, "
               f"after-reload={final_lang}",
        status="PASS" if passed else "FAIL",
    )


def test_footer_reachable(driver, device, route, scenario_id) -> Result:
    """Scroll to bottom; footer.app-footer visible."""
    driver.get(BASE + "/" + route)
    wait_for_app(driver, 8)
    time.sleep(0.4)
    visible = js_safe(driver, """
        window.scrollTo(0, document.body.scrollHeight);
        var f = document.querySelector('footer.app-footer');
        if (!f) return null;
        var r = f.getBoundingClientRect();
        return {top: Math.round(r.top), bottom: Math.round(r.bottom),
                ih: window.innerHeight,
                inview: r.top < window.innerHeight && r.bottom > 0};
    """, None)
    if visible is None:
        return Result(scenario_id=scenario_id, device=device, route=route,
                      title=f"Footer reachable on {route}",
                      expected="footer.app-footer found",
                      actual="not found", status="FAIL")
    return Result(
        scenario_id=scenario_id, device=device, route=route,
        title=f"Footer reachable on {route}",
        expected="footer in viewport after scrollTo bottom",
        actual=f"top={visible['top']}, bottom={visible['bottom']}, "
               f"innerHeight={visible['ih']}, inview={visible['inview']}",
        status="PASS" if visible["inview"] else "FAIL",
        severity="Minor",
    )


def test_sticky_header(driver, device, scenario_id) -> Result:
    """Header stays at top after long scroll."""
    driver.get(BASE + "/learn/grammar")
    wait_for_app(driver, 8)
    time.sleep(0.5)
    info = js_safe(driver, """
        window.scrollTo(0, 5000);
        var h = document.querySelector('.top-bar, header.app-header, header');
        if (!h) return null;
        var r = h.getBoundingClientRect();
        return {top: Math.round(r.top), pos: getComputedStyle(h).position};
    """, None)
    if info is None:
        return Result(scenario_id=scenario_id, device=device,
                      title="Header sticky on long scroll",
                      expected="header element found",
                      actual="header element not found", status="FAIL")
    sticky = info["top"] <= 5 and info["pos"] in ("sticky", "fixed")
    return Result(
        scenario_id=scenario_id, device=device,
        title="Header sticky on long scroll",
        expected="header.top ~ 0 with position sticky/fixed",
        actual=f"top={info['top']}, position={info['pos']}",
        status="PASS" if sticky else "FAIL",
        severity="Major",
    )


def test_404_route(driver, device, scenario_id) -> Result:
    """Invalid route shows graceful fallback, not blank page."""
    driver.get(BASE + "/#/nonexistent-route-zzz")
    time.sleep(1.5)
    wait_for_app(driver, 5)
    text = js_safe(driver, "return document.getElementById('app').innerText", "")
    children = js_safe(driver,
        "return document.getElementById('app').children.length", 0)
    # Pass if either (a) text mentions not found / home / or (b) graceful redirect to home content
    has_message = any(w in (text or "").lower() for w in
                      ["not found", "404", "home", "jlpt", "learn", "grammar"])
    return Result(
        scenario_id=scenario_id, device=device,
        title="Invalid route handled gracefully",
        expected="non-blank fallback (404 message or home redirect)",
        actual=f"children={children}, text_preview={(text or '')[:80]}",
        status="PASS" if children > 0 and has_message else "FAIL",
        severity="Minor",
    )


def test_corrupt_storage(driver, device, scenario_id) -> Result:
    """Corrupt localStorage doesn't crash app."""
    driver.get(BASE + "/")
    wait_for_app(driver, 8)
    js_safe(driver, """
        try {
            localStorage.setItem('n5:progress', '{garbage');
            localStorage.setItem('n5:srs', 'not json at all');
        } catch (e) {}
    """)
    driver.refresh()
    ok = wait_for_app(driver, 10)
    children = js_safe(driver,
        "return document.getElementById('app').children.length", 0)
    return Result(
        scenario_id=scenario_id, device=device,
        title="Corrupt localStorage recovery",
        expected="App still loads + renders",
        actual=f"skeleton-cleared={ok}, #app children={children}",
        status="PASS" if ok and children > 0 else "FAIL",
        severity="Critical" if not (ok and children > 0) else "Major",
    )


def test_lang_attribute_after_locale(driver, device, scenario_id) -> Result:
    """<html lang> reflects locale + changes on toggle."""
    driver.get(BASE + "/")
    wait_for_app(driver, 8)
    lang1 = js_safe(driver, "return document.documentElement.lang")
    js_safe(driver, "var e=document.getElementById('locale-toggle'); if(e) e.click()")
    time.sleep(0.5)
    lang2 = js_safe(driver, "return document.documentElement.lang")
    passed = lang1 and lang2 and lang1 != lang2 and \
             lang1 in ("en", "hi") and lang2 in ("en", "hi")
    return Result(
        scenario_id=scenario_id, device=device,
        title="<html lang> reflects + changes on locale toggle",
        expected="lang ∈ {en, hi} and changes after toggle",
        actual=f"before={lang1}, after={lang2}",
        status="PASS" if passed else "FAIL",
    )


def test_root_resolves_to_home(driver, device, scenario_id) -> Result:
    """Loading / resolves to #/home (or shows home content)."""
    driver.get(BASE + "/")
    wait_for_app(driver, 8)
    time.sleep(0.5)
    h = js_safe(driver, "return location.hash") or ""
    has_home = js_safe(driver, """
        var t = (document.body.innerText || '').toLowerCase();
        return t.includes('jlpt') || t.includes('n5') || t.includes('grammar');
    """, False)
    return Result(
        scenario_id=scenario_id, device=device,
        title="/ resolves to home content",
        expected="hash starts with #/home or home text present",
        actual=f"hash={h}, home-text-detected={has_home}",
        status="PASS" if (h.startswith("#/home") or h == "" or has_home) else "FAIL",
        severity="Major",
    )


def test_audio_buttons_route_loads(driver, device, route, scenario_id) -> Result:
    """For audio-bearing routes, verify any audio button or element exists."""
    driver.get(BASE + "/" + route)
    wait_for_app(driver, 8)
    time.sleep(0.5)
    audio_info = js_safe(driver, """
        var audios = document.querySelectorAll('audio');
        var btns = document.querySelectorAll(
            'button[data-audio], button.play-audio, .audio-play-button, button[aria-label*="play" i]');
        return {audios: audios.length, buttons: btns.length};
    """, {"audios": 0, "buttons": 0})
    found = audio_info["audios"] + audio_info["buttons"]
    return Result(
        scenario_id=scenario_id, device=device, route=route,
        title=f"Audio UI present on {route}",
        expected=">= 1 audio element or play-button",
        actual=f"audio={audio_info['audios']}, buttons={audio_info['buttons']}",
        status="PASS" if found >= 1 else "FAIL",
        severity="Minor",
    )


def test_kanji_grid_touch(driver, device, scenario_id) -> Result:
    """Kanji grid items >= 44x44."""
    driver.get(BASE + "/#/kanji")
    wait_for_app(driver, 8)
    time.sleep(0.6)
    sizes = js_safe(driver, """
        var items = document.querySelectorAll(
            '.kanji-grid a, .kanji-card, [data-kanji-glyph], .kanji-tile, a[href*="#/kanji/"]');
        var out = [];
        for (var i = 0; i < items.length; i++) {
            var r = items[i].getBoundingClientRect();
            if (r.width > 0)
                out.push({w: Math.round(r.width), h: Math.round(r.height)});
        }
        return out;
    """, [])
    if not sizes:
        return Result(scenario_id=scenario_id, device=device,
                      title="Kanji grid items touch-sized",
                      expected=">=1 kanji item with size >=44x44",
                      actual="no kanji grid items found via expected selectors",
                      status="FAIL", severity="Major")
    failing = [s for s in sizes if min(s["w"], s["h"]) < 44]
    return Result(
        scenario_id=scenario_id, device=device,
        title="Kanji grid items >= 44x44",
        expected="all kanji grid items meet HIG minimum",
        actual=f"{len(failing)}/{len(sizes)} undersized",
        status="PASS" if not failing else "FAIL",
        severity="Major",
    )


def test_grammar_list_count(driver, device, scenario_id) -> Result:
    """Grammar list shows expected count of patterns."""
    driver.get(BASE + "/#/learn/grammar")
    wait_for_app(driver, 12)
    time.sleep(1.0)
    count = js_safe(driver, """
        var items = document.querySelectorAll(
            'a[href*="#/learn/"], [data-pattern-id], .grammar-card, .pattern-item');
        return items.length;
    """, 0)
    return Result(
        scenario_id=scenario_id, device=device,
        title="Grammar list shows pattern entries",
        expected="≥ 50 pattern entries (~178 total in N5)",
        actual=f"found {count} candidate items",
        status="PASS" if count >= 50 else "FAIL",
        severity="Major",
    )


def test_settings_route(driver, device, scenario_id) -> Result:
    """Settings route renders interactive controls."""
    driver.get(BASE + "/#/settings")
    wait_for_app(driver, 8)
    time.sleep(0.5)
    controls = js_safe(driver, """
        var c = document.querySelectorAll(
            '#app input, #app select, #app button, #app [role="switch"]');
        return c.length;
    """, 0)
    return Result(
        scenario_id=scenario_id, device=device,
        title="Settings has interactive controls",
        expected="≥ 2 form controls in settings route",
        actual=f"found {controls} input/select/button/switch",
        status="PASS" if controls >= 2 else "FAIL",
        severity="Major",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_all():
    print("=" * 72)
    print("Mobile UI test execution — JLPT N5")
    print("=" * 72)
    print(f"Base URL: {BASE}")
    print(f"Devices: {list(DEVICES.keys())}")
    print()

    # Smoke + cross-cutting on D-360 (primary mobile baseline)
    d = make_driver(*DEVICES["D-360"])
    try:
        print("--- Cross-cutting on D-360 ---")
        log(test_root_resolves_to_home(d, "D-360", "O-X-rootnav"))
        log(test_nav_links_present(d, "D-360", "O-X-010"))
        log(test_search_input_font_size(d, "D-360", "O-X-015"))
        log(test_touch_target_size(d, "D-360", "O-X-021"))
        log(test_locale_toggle(d, "D-360", "O-X-018"))
        log(test_locale_persists(d, "D-360", "O-X-017"))
        log(test_lang_attribute_after_locale(d, "D-360", "O-X-lang"))
        log(test_sticky_header(d, "D-360", "O-X-012"))
        log(test_404_route(d, "D-360", "O-S-err404"))
        log(test_corrupt_storage(d, "D-360", "O-S-corrupt"))

        # Per-route smoke renders
        print("\n--- Per-route renders on D-360 ---")
        for route in ROUTES_TO_VISIT:
            log(test_app_renders(d, "D-360", route, f"O-S-r-{route.strip('#/').replace('/','_')[:18]}"))

        # Footer reachability sample
        print("\n--- Footer reachability sample on D-360 ---")
        for route in ["#/home", "#/learn/grammar", "#/kanji", "#/reading", "#/settings"]:
            log(test_footer_reachable(d, "D-360", route,
                f"O-S-f-{route.strip('#/').replace('/','_')[:18]}"))

        # Audio UI sample
        print("\n--- Audio UI sample on D-360 ---")
        for route in ["#/listening", "#/listening/story", "#/reading"]:
            log(test_audio_buttons_route_loads(d, "D-360", route,
                f"O-S-a-{route.strip('#/').replace('/','_')[:18]}"))

        # Targeted screens
        print("\n--- Targeted-screen checks on D-360 ---")
        log(test_kanji_grid_touch(d, "D-360", "O-S-k-grid"))
        log(test_grammar_list_count(d, "D-360", "O-S-g-count"))
        log(test_settings_route(d, "D-360", "O-S-s-controls"))
    finally:
        d.quit()

    # No-horizontal-scroll across multiple viewports
    for label in ["D-320", "D-360", "D-375", "D-414", "D-768"]:
        w, h = DEVICES[label]
        print(f"\n--- No-horizontal-scroll on {label} ({w}x{h}) ---")
        d = make_driver(w, h)
        try:
            for route in ["#/home", "#/learn/grammar", "#/learn/vocab",
                          "#/kanji", "#/reading", "#/listening",
                          "#/test", "#/settings", "#/missed", "#/summary"]:
                log(test_no_horizontal_scroll(d, label, route,
                    f"O-X-hs-{label}-{route.strip('#/').replace('/','_')[:14]}"))
        finally:
            d.quit()


def print_summary():
    print()
    print("=" * 72)
    print("SUMMARY")
    print("=" * 72)
    by_status = {}
    for r in RESULTS:
        by_status.setdefault(r.status, 0)
        by_status[r.status] += 1
    for s in ("PASS", "FAIL", "ERROR", "SKIP-MANUAL"):
        if s in by_status:
            print(f"  {s:11s}: {by_status[s]}")
    print(f"  TOTAL      : {len(RESULTS)}")
    print()
    fails = [r for r in RESULTS if r.is_fail()]
    if fails:
        print(f"FAILURES ({len(fails)}):")
        for r in fails:
            print(f"  {r.scenario_id} {r.device} on {r.route or '-'}: {r.title}")
            print(f"     expected: {r.expected}")
            print(f"     actual:   {r.actual}")


def write_json_for_bug_loader():
    """Dump results to JSON so bug-loader script can ingest."""
    out = []
    for r in RESULTS:
        out.append({
            "scenario_id": r.scenario_id,
            "device": r.device,
            "route": r.route,
            "status": r.status,
            "title": r.title,
            "expected": r.expected,
            "actual": r.actual,
            "severity": r.severity,
        })
    path = Path(__file__).resolve().parent.parent / "specifications" / \
        "mobile_ui_test_results.json"
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nResults written: {path}")


if __name__ == "__main__":
    t0 = time.time()
    try:
        run_all()
    except Exception:
        print("FATAL:")
        traceback.print_exc()
    print_summary()
    write_json_for_bug_loader()
    print(f"\nElapsed: {time.time() - t0:.1f}s")
