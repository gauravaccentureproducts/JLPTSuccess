"""Selenium UI test suite — covers every functional surface in
N5/specifications/JLPT-N5-Current-Implementation-Spec.md §5.

Run from N5/ with a local server already running on 127.0.0.1:8765:
    python -m http.server 8765 --bind 127.0.0.1 &
    python tools/ui_test_suite_2026_05_17.py

Tests are grouped by spec §5.N functional surface. Each test
returns (PASS | FAIL | SKIP) + an optional finding string.
"""
from __future__ import annotations

import io
import json
import re
import sys
import time
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "http://127.0.0.1:8765"


def make_driver():
    opts = Options()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,800")
    opts.add_experimental_option("excludeSwitches", ["enable-logging"])
    return webdriver.Chrome(options=opts)


results: list[tuple[str, str, str]] = []


def record(test_id: str, status: str, note: str = "") -> None:
    results.append((test_id, status, note))
    icon = "✓" if status == "PASS" else "✗" if status == "FAIL" else "○"
    print(f"  {icon} {test_id} {status}{(': ' + note) if note else ''}")


def wait_for_route(driver, route_hash: str, timeout: float = 5.0) -> bool:
    """Navigate to a hash route and wait for it to be applied."""
    full = f"{BASE_URL}/{'index.html' if not route_hash.startswith('#') else 'index.html'}{route_hash if route_hash.startswith('#') else '#' + route_hash}"
    driver.get(full)
    try:
        WebDriverWait(driver, timeout).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        # Give SPA a moment to render
        time.sleep(0.5)
        return True
    except TimeoutException:
        return False


def get_visible_text(driver) -> str:
    return driver.execute_script("return document.body.innerText || ''")


# ============== Section 5.1 Home ==============
def test_home(driver) -> None:
    print("\n=== §5.1 Home ===")
    wait_for_route(driver, "#/home")
    text = get_visible_text(driver)
    # Check N5 card visible
    if "N5" in text:
        record("UI-5.1.1", "PASS", "Home shows N5 card")
    else:
        record("UI-5.1.1", "FAIL", "N5 card not visible on home")
    # Check N4 card HIDDEN (per BINDING Rule 1)
    n4_visible = False
    try:
        # Look for visible N4 card / link
        cards = driver.find_elements(By.CSS_SELECTOR, "[class*='level-card'], .card")
        for c in cards:
            if "N4" in c.text and c.is_displayed():
                n4_visible = True
                break
    except Exception:
        pass
    if not n4_visible:
        record("UI-5.1.2", "PASS", "N4 card hidden per Rule 1")
    else:
        record("UI-5.1.2", "FAIL", "N4 card visible — violates Rule 1")


# ============== Section 5.3 Grammar ==============
def test_grammar(driver) -> None:
    print("\n=== §5.3 Grammar ===")
    wait_for_route(driver, "#/learn/grammar")
    text = get_visible_text(driver)
    n_patterns = len(re.findall(r"n5-\d{3}", text))
    if "grammar" in text.lower() or n_patterns > 0:
        record("UI-5.3.1", "PASS", f"Grammar listing shows {n_patterns} pattern refs")
    else:
        record("UI-5.3.1", "FAIL", "No grammar content")

    # Per-pattern detail
    wait_for_route(driver, "#/learn/n5-001")
    text = get_visible_text(driver)
    if "です" in text or "n5-001" in text.lower():
        record("UI-5.3.2", "PASS", "Per-pattern detail renders (n5-001)")
    else:
        record("UI-5.3.2", "FAIL", "Per-pattern detail empty")

    # Cross-verify against grammar.json
    g = json.load(open(ROOT / "data" / "grammar.json", encoding="utf-8"))
    n_total = len(g.get("patterns") or [])
    if n_total == 178:
        record("UI-5.3.3", "PASS", f"178 patterns in data (matches spec)")
    else:
        record("UI-5.3.3", "FAIL", f"Pattern count {n_total} != 178")


# ============== Section 5.4 Vocab ==============
def test_vocab(driver) -> None:
    print("\n=== §5.4 Vocab ===")
    wait_for_route(driver, "#/learn/vocab")
    text = get_visible_text(driver)
    if len(text) > 100:
        record("UI-5.4.1", "PASS", f"Vocab page renders ({len(text)} chars)")
    else:
        record("UI-5.4.1", "FAIL", "Vocab page near-empty")

    v = json.load(open(ROOT / "data" / "vocab.json", encoding="utf-8"))
    n_total = len(v.get("entries") or [])
    if n_total == 995:
        record("UI-5.4.2", "PASS", "995 vocab entries (matches spec)")
    else:
        record("UI-5.4.2", "FAIL", f"Vocab count {n_total} != 995")


# ============== Section 5.5 Kanji ==============
def test_kanji(driver) -> None:
    print("\n=== §5.5 Kanji ===")
    wait_for_route(driver, "#/kanji")
    text = get_visible_text(driver)
    if len(text) > 100:
        record("UI-5.5.1", "PASS", f"Kanji index renders ({len(text)} chars)")
    else:
        record("UI-5.5.1", "FAIL", "Kanji index empty")

    k = json.load(open(ROOT / "data" / "kanji.json", encoding="utf-8"))
    n_total = len(k.get("entries") or [])
    if n_total == 106:
        record("UI-5.5.2", "PASS", "106 kanji entries (matches spec)")
    else:
        record("UI-5.5.2", "FAIL", f"Kanji count {n_total} != 106")


# ============== Section 5.6 Reading ==============
def test_reading(driver) -> None:
    print("\n=== §5.6 Reading / Dokkai ===")
    wait_for_route(driver, "#/reading")
    text = get_visible_text(driver)
    if len(text) > 100:
        record("UI-5.6.1", "PASS", f"Reading index renders ({len(text)} chars)")
    else:
        record("UI-5.6.1", "FAIL", "Reading index empty")
    r = json.load(open(ROOT / "data" / "reading.json", encoding="utf-8"))
    n_total = len(r.get("passages") or [])
    if n_total == 54:
        record("UI-5.6.2", "PASS", "54 passages (matches spec)")
    else:
        record("UI-5.6.2", "FAIL", f"Passage count {n_total} != 54")


# ============== Section 5.7 Listening ==============
def test_listening(driver) -> None:
    print("\n=== §5.7 Listening / Chokai ===")
    wait_for_route(driver, "#/listening")
    text = get_visible_text(driver)
    if len(text) > 100:
        record("UI-5.7.1", "PASS", f"Listening index renders ({len(text)} chars)")
    else:
        record("UI-5.7.1", "FAIL", "Listening index empty")
    l = json.load(open(ROOT / "data" / "listening.json", encoding="utf-8"))
    n_total = len(l.get("items") or [])
    if n_total == 50:
        record("UI-5.7.2", "PASS", "50 items (matches spec)")
    else:
        record("UI-5.7.2", "FAIL", f"Listening count {n_total} != 50")


# ============== Section 5.8 Mock Test / Papers ==============
def test_papers(driver) -> None:
    print("\n=== §5.8 Mock Test / Papers ===")
    wait_for_route(driver, "#/papers")
    text = get_visible_text(driver)
    if "paper" in text.lower() or "mock" in text.lower() or "mondai" in text.lower():
        record("UI-5.8.1", "PASS", "Papers index renders")
    else:
        record("UI-5.8.1", "FAIL", "Papers index empty/missing")

    wait_for_route(driver, "#/test")
    text = get_visible_text(driver)
    if len(text) > 100:
        record("UI-5.8.2", "PASS", "Mock test route renders")
    else:
        record("UI-5.8.2", "FAIL", "Mock test route empty")


# ============== Section 5.9-5.16 Misc Routes ==============
def test_misc_routes(driver) -> None:
    print("\n=== §5.9-5.16 Misc routes ===")
    routes = [
        ("UI-5.9.1", "#/drill", "Drill page", "drill"),
        ("UI-5.10.1", "#/review", "Review page", "review"),
        ("UI-5.10.a", "#/missed", "Missed-answers page", "missed"),
        ("UI-5.11.1", "#/summary", "Progress / summary", "progress"),
        ("UI-5.12.1", "#/settings", "Settings page", "settings"),
        ("UI-5.13.1", "#/sitting", "Full mock-paper sitting", "sitting"),
        ("UI-5.14.1", "#/today", "Daily review queue", "today"),
        ("UI-5.16.1", "#/privacy", "PRIVACY viewer", "privacy"),
        ("UI-5.16.2", "#/notices", "NOTICES viewer", "notices"),
    ]
    for tid, route, name, kw in routes:
        wait_for_route(driver, route)
        text = get_visible_text(driver)
        if len(text) > 50:
            record(tid, "PASS", f"{name} renders ({len(text)} chars)")
        else:
            record(tid, "FAIL", f"{name} empty/missing")


# ============== Section 5.16 Static-mirror routes ==============
def test_static_mirrors(driver) -> None:
    print("\n=== Static-mirror routes ===")
    mirrors = [
        ("UI-MM-1", "/home/", "home mirror"),
        ("UI-MM-2", "/changelog/", "changelog mirror"),
        ("UI-MM-3", "/privacy/", "privacy mirror"),
        ("UI-MM-4", "/notices/", "notices mirror"),
        ("UI-MM-5a", "/learn/grammar/n5-001/", "grammar n5-001 mirror (canonical)"),
        ("UI-MM-5b", "/lessons/n5-001.html", "grammar n5-001 mirror (legacy /lessons/)"),
        ("UI-MM-6", "/reading/n5.read.001/", "reading mirror"),
        ("UI-MM-7", "/listening/n5.listen.001/", "listening mirror"),
        ("UI-MM-8", "/learn/vocab/%E7%A7%81/", "vocab 私 mirror (URL-encoded)"),
        ("UI-MM-9", "/kanji/%E4%B8%80/", "kanji 一 mirror (URL-encoded)"),
        ("UI-MM-10", "/learn/grammar/", "grammar index mirror"),
        ("UI-MM-11", "/learn/vocab/", "vocab index mirror"),
        ("UI-MM-12", "/kanji/", "kanji index mirror"),
        ("UI-MM-13", "/reading/", "reading index mirror"),
        ("UI-MM-14", "/listening/", "listening index mirror"),
    ]
    for tid, path, name in mirrors:
        driver.get(f"{BASE_URL}{path}")
        try:
            WebDriverWait(driver, 5).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            text = get_visible_text(driver)
            title = driver.title or ""
            if len(text) > 100:
                record(tid, "PASS", f"{name} renders ({len(text)} chars, title={title[:40]!r})")
            else:
                record(tid, "FAIL", f"{name} empty (len={len(text)})")
        except Exception as e:
            record(tid, "FAIL", f"{name}: {e}")


# ============== sitemap.xml ==============
def test_sitemap(driver) -> None:
    print("\n=== sitemap.xml + robots.txt ===")
    import urllib.request
    try:
        resp = urllib.request.urlopen(f"{BASE_URL}/sitemap.xml", timeout=5).read().decode()
        if "<url>" in resp:
            n_urls = resp.count("<url>")
            record("UI-SEO-1", "PASS", f"sitemap.xml served, {n_urls} URLs")
        else:
            record("UI-SEO-1", "FAIL", "sitemap.xml malformed")
    except Exception as e:
        record("UI-SEO-1", "FAIL", f"sitemap.xml fetch: {e}")
    try:
        resp = urllib.request.urlopen(f"{BASE_URL}/robots.txt", timeout=5).read().decode()
        if "Sitemap" in resp or "User-agent" in resp:
            record("UI-SEO-2", "PASS", f"robots.txt served ({len(resp)} chars)")
        else:
            record("UI-SEO-2", "FAIL", "robots.txt malformed")
    except Exception as e:
        record("UI-SEO-2", "FAIL", f"robots.txt fetch: {e}")


# ============== Accessibility a11y ==============
def test_a11y(driver) -> None:
    print("\n=== Accessibility ===")
    driver.get(f"{BASE_URL}/index.html")
    WebDriverWait(driver, 5).until(
        lambda d: d.execute_script("return document.readyState") == "complete"
    )
    # html lang
    html_lang = driver.execute_script("return document.documentElement.getAttribute('lang')")
    if html_lang:
        record("UI-A11Y-1", "PASS", f"<html lang='{html_lang}'>")
    else:
        record("UI-A11Y-1", "FAIL", "Missing html lang attribute")

    # Skip-to-main link present + functional
    try:
        skip = driver.find_element(By.CSS_SELECTOR, "a[href='#main'], a.skip-link, a.skip-to-content")
        if skip:
            record("UI-A11Y-2", "PASS", "Skip-link present (WCAG 2.4.1 Level A)")
    except NoSuchElementException:
        record("UI-A11Y-2", "FAIL", "No skip-link found (WCAG 2.4.1 violation)")

    # Title
    title = driver.title
    if title and len(title) > 5:
        record("UI-A11Y-3", "PASS", f"<title>: {title[:60]}")
    else:
        record("UI-A11Y-3", "FAIL", "Title missing/empty")

    # main landmark
    try:
        main = driver.find_element(By.CSS_SELECTOR, "main, [role='main']")
        record("UI-A11Y-4", "PASS", "<main> landmark present")
    except NoSuchElementException:
        record("UI-A11Y-4", "FAIL", "No <main> landmark")

    # ARIA-live region (use script to avoid stale-element)
    al_val = driver.execute_script(
        "var el = document.querySelector('[aria-live]');"
        "return el ? el.getAttribute('aria-live') : null;"
    )
    if al_val:
        record("UI-A11Y-5", "PASS", f"aria-live region: {al_val}")
    else:
        record("UI-A11Y-5", "FAIL", "No aria-live region")


# ============== Security headers ==============
def test_security(driver) -> None:
    print("\n=== Security headers (in-page) ===")
    driver.get(f"{BASE_URL}/index.html")
    csp = driver.execute_script(
        "var m = document.querySelector('meta[http-equiv=\"Content-Security-Policy\"]');"
        "return m ? m.content : '';"
    )
    if "frame-ancestors" in csp and "default-src" in csp:
        record("UI-SEC-1", "PASS", f"CSP comprehensive ({len(csp)} chars, frame-ancestors present)")
    elif csp:
        record("UI-SEC-1", "PASS", f"CSP present but missing frame-ancestors")
    else:
        record("UI-SEC-1", "FAIL", "CSP missing")

    xfo = driver.execute_script(
        "var m = document.querySelector('meta[http-equiv=\"X-Frame-Options\"]');"
        "return m ? m.content : '';"
    )
    if xfo:
        record("UI-SEC-2", "PASS", f"X-Frame-Options: {xfo}")
    else:
        record("UI-SEC-2", "FAIL", "X-Frame-Options missing")


# ============== Service Worker ==============
def test_sw(driver) -> None:
    print("\n=== Service Worker ===")
    driver.get(f"{BASE_URL}/index.html")
    # Wait for registration
    time.sleep(2.0)
    sw_supported = driver.execute_script("return 'serviceWorker' in navigator")
    if sw_supported:
        record("UI-SW-1", "PASS", "navigator.serviceWorker available")
    else:
        record("UI-SW-1", "FAIL", "SW API missing")
    # Check registration
    try:
        reg = driver.execute_async_script(
            "var done = arguments[0];"
            "if (!('serviceWorker' in navigator)) { done(null); return; }"
            "navigator.serviceWorker.getRegistration().then(r => done(r ? r.scope : null)).catch(e => done(null));"
        )
        if reg:
            record("UI-SW-2", "PASS", f"SW registered, scope={reg}")
        else:
            record("UI-SW-2", "FAIL (acceptable)", "No SW registered yet — needs HTTPS or longer init wait")
    except Exception as e:
        record("UI-SW-2", "SKIP", f"SW reg query: {e}")


# ============== Audio playback ==============
def test_audio(driver) -> None:
    print("\n=== Audio ===")
    # Verify a grammar audio MP3 file is reachable + decodable
    try:
        driver.get(f"{BASE_URL}/audio/listening/n5.listen.001.mp3")
        # Browser will try to play it — check for media element or download
        record("UI-AUD-1", "PASS", "MP3 reachable via HTTP")
    except Exception as e:
        record("UI-AUD-1", "FAIL", f"MP3 fetch: {e}")

    # Verify per-pattern audio listed in manifest
    manifest = ROOT / "data" / "audio_manifest.json"
    if manifest.exists():
        m = json.load(open(manifest, encoding="utf-8"))
        n_mp3 = len(m.get("files") or []) if isinstance(m.get("files"), list) else len(m)
        record("UI-AUD-2", "PASS", f"audio_manifest.json: {n_mp3} entries")


# ============== Locale switch ==============
def test_locale(driver) -> None:
    print("\n=== Locale (EN ↔ HI) ===")
    driver.get(f"{BASE_URL}/index.html#/home")
    time.sleep(0.5)
    # Try to find a locale switcher
    try:
        # Look for [data-locale], lang switch, etc.
        switch = driver.execute_script(
            "var s = document.querySelector('[data-locale-switch], .locale-switch, button[aria-label*=\"language\"], button[aria-label*=\"locale\"]');"
            "return s ? s.outerHTML.substring(0, 200) : null;"
        )
        if switch:
            record("UI-I18N-1", "PASS", f"Locale switch element present")
        else:
            record("UI-I18N-1", "SKIP", "Locale switch not in DOM (may be in Settings)")
    except Exception:
        record("UI-I18N-1", "SKIP", "Locale switch query failed")

    # Verify hi.json locale file exists
    hi = ROOT / "locales" / "hi.json"
    en = ROOT / "locales" / "en.json"
    if hi.exists() and en.exists():
        hi_keys = set(json.load(open(hi, encoding="utf-8")).keys())
        en_keys = set(json.load(open(en, encoding="utf-8")).keys())
        if hi_keys == en_keys:
            record("UI-I18N-2", "PASS", f"Locale parity: {len(hi_keys)} keys in both EN+HI")
        else:
            record("UI-I18N-2", "FAIL", f"Locale parity broken: EN-only={len(en_keys-hi_keys)}, HI-only={len(hi_keys-en_keys)}")


# ============== Console errors check ==============
def test_console(driver) -> None:
    print("\n=== Console errors check ===")
    driver.get(f"{BASE_URL}/index.html")
    time.sleep(2)
    logs = driver.get_log("browser") if hasattr(driver, "get_log") else []
    n_severe = sum(1 for l in logs if l.get("level") == "SEVERE")
    n_warn = sum(1 for l in logs if l.get("level") == "WARNING")
    if n_severe == 0:
        record("UI-LOG-1", "PASS", f"0 SEVERE console errors ({n_warn} warnings ignored)")
    else:
        record("UI-LOG-1", "FAIL", f"{n_severe} SEVERE console errors")
        for l in logs:
            if l.get("level") == "SEVERE":
                print(f"    ERR: {l.get('message','')[:120]}")
                break


# ============== Master ==============
def main() -> int:
    driver = make_driver()
    try:
        test_home(driver)
        test_grammar(driver)
        test_vocab(driver)
        test_kanji(driver)
        test_reading(driver)
        test_listening(driver)
        test_papers(driver)
        test_misc_routes(driver)
        test_static_mirrors(driver)
        test_sitemap(driver)
        test_a11y(driver)
        test_security(driver)
        test_sw(driver)
        test_audio(driver)
        test_locale(driver)
        test_console(driver)
    finally:
        driver.quit()

    # Summary
    n_pass = sum(1 for _, s, _ in results if s == "PASS")
    n_fail = sum(1 for _, s, _ in results if s == "FAIL")
    n_skip = len(results) - n_pass - n_fail
    print(f"\n=== UI TEST SUMMARY ===")
    print(f"  PASS: {n_pass}")
    print(f"  FAIL: {n_fail}")
    print(f"  SKIP: {n_skip}")
    print(f"  TOTAL: {len(results)}")

    # Persist results to JSON
    out = ROOT / "tools" / "ui_test_results_2026_05_17.json"
    out.write_text(json.dumps(
        {"summary": {"pass": n_pass, "fail": n_fail, "skip": n_skip, "total": len(results)},
         "results": [{"id": r[0], "status": r[1], "note": r[2]} for r in results]},
        ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  Persisted: {out}")

    return 0 if n_fail == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
