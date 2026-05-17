"""Dump all browser console errors from index.html."""
from __future__ import annotations
import io, sys, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

opts = Options()
opts.add_argument("--headless=new")
opts.add_argument("--no-sandbox")
opts.add_argument("--disable-dev-shm-usage")
opts.set_capability("goog:loggingPrefs", {"browser": "ALL"})

d = webdriver.Chrome(options=opts)
try:
    d.get("http://127.0.0.1:8765/index.html")
    time.sleep(3)
    # Trigger SW + a few route changes to catch all errors
    for r in ("#/home", "#/learn/grammar", "#/listening", "#/settings"):
        d.execute_script(f"window.location.hash = '{r}'")
        time.sleep(1.5)
    logs = d.get_log("browser")
    severe = [l for l in logs if l.get("level") == "SEVERE"]
    warning = [l for l in logs if l.get("level") == "WARNING"]
    print(f"=== {len(severe)} SEVERE + {len(warning)} WARNING ===")
    for l in severe:
        print(f"\nSEVERE: {l.get('message','')[:300]}")
    print()
    for l in warning[:5]:
        print(f"WARN: {l.get('message','')[:300]}")
finally:
    d.quit()
