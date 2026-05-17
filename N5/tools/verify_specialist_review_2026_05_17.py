"""Verification checks for D/E/F/G/H/I/J/K/L/M/N tab scenarios.

Runs all agent-side-verifiable checks in one pass and reports
findings. Used to inform the specialist-review stamping batch on
2026-05-17.
"""
from __future__ import annotations

import glob
import io
import json
import os
import re
import sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ROOT = Path(__file__).resolve().parent.parent
os.chdir(str(ROOT))


def section(name: str) -> None:
    print(f"\n=== {name} ===")


# ----------- F. SECURITY -----------
def check_security():
    section("F. SECURITY")
    findings = {}

    # F-005..008: HTML security headers
    html = Path("index.html").read_text(encoding="utf-8")
    csp_match = re.search(
        r'<meta[^>]*Content-Security-Policy[^>]*content="([^"]+)"',
        html, re.IGNORECASE,
    )
    csp = csp_match.group(1) if csp_match else ""
    findings["F-005 CSP present"] = bool(csp_match)
    findings["F-005 CSP frame-ancestors"] = "frame-ancestors" in csp
    findings["F-006 X-Frame-Options"] = "X-Frame-Options" in html
    findings["F-007 Referrer-Policy"] = (
        "Referrer-Policy" in html or 'name="referrer"' in html
    )
    findings["F-008 Permissions-Policy"] = "Permissions-Policy" in html

    # F-018: workflow permissions block
    wf_dir = Path(".github/workflows")
    if wf_dir.exists():
        wfs = sorted(wf_dir.iterdir())
        n_with_perms = 0
        for wf in wfs:
            c = wf.read_text(encoding="utf-8")
            if re.search(r"^permissions:", c, re.MULTILINE):
                n_with_perms += 1
        findings["F-018 workflows-with-permissions-block"] = (
            f"{n_with_perms}/{len(wfs)}"
        )
        # F-019: fork-PR protection (no pull_request_target use)
        any_prtarget = any(
            "pull_request_target" in w.read_text(encoding="utf-8")
            for w in wfs
        )
        findings["F-019 pull_request_target use"] = any_prtarget

    # F-014/015: secrets
    secret_pats = [
        r"AKIA[0-9A-Z]{16}",
        r"ghp_[A-Za-z0-9]{36}",
        r"gho_[A-Za-z0-9]{36}",
        r"-----BEGIN.*PRIVATE KEY-----",
    ]
    n_secrets = 0
    for path in glob.glob("**/*.py", recursive=True) + glob.glob(
        "**/*.js", recursive=True
    ) + glob.glob("**/*.json", recursive=True):
        if "node_modules" in path or ".bak" in path:
            continue
        try:
            content = Path(path).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for pat in secret_pats:
            if re.search(pat, content):
                n_secrets += 1
                print(f"  SECRET in {path}: pattern {pat!r}")
    findings["F-014 secrets found"] = n_secrets

    env_files = [f for f in Path(".").glob("**/.env*")
                 if "node_modules" not in str(f)]
    findings["F-015 .env files"] = len(env_files)

    for k, v in findings.items():
        print(f"  {k}: {v}")
    return findings


# ----------- G. PRIVACY -----------
def check_privacy():
    section("G. PRIVACY")
    findings = {}
    # G-001: analytics — verify ALL hits are negative-assertion / prose context
    analytics_actual = 0
    analytics_re = re.compile(
        r"(?:google-analytics|googletagmanager|mixpanel|segment\.io|"
        r"plausible\.io|amplitude\.com|gtag\(|fbq\()"
    )
    for path in glob.glob("**/*.html", recursive=True) + glob.glob(
        "**/*.js", recursive=True
    ):
        if "node_modules" in path or ".min." in path:
            continue
        try:
            c = Path(path).read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for m in analytics_re.finditer(c):
            # Only count actual <script>/<src>/import — not prose
            start = max(0, m.start() - 30)
            ctx = c[start: m.end() + 30]
            if 'src="' in ctx or "src='" in ctx or "import " in ctx:
                analytics_actual += 1
    findings["G-001 actual analytics integrations"] = analytics_actual

    # G-003: document.cookie actual use
    cookie_actual = 0
    for path in glob.glob("js/*.js"):
        c = Path(path).read_text(encoding="utf-8", errors="ignore")
        if re.search(r"document\.cookie\s*=", c) or re.search(
            r"document\.cookie\.\w", c
        ):
            cookie_actual += 1
            print(f"  document.cookie WRITE/USE in {path}")
    findings["G-003 actual cookie use"] = cookie_actual

    # G-008/009/010 attribution
    cl = Path("CONTENT-LICENSE.md").read_text(encoding="utf-8")
    nt = Path("NOTICES.md").read_text(encoding="utf-8")
    findings["G-008 kanjium in CONTENT-LICENSE"] = "kanjium" in cl.lower()
    findings["G-008 kanjium in NOTICES"] = "kanjium" in nt.lower()
    findings["G-009 VOICEVOX in CONTENT-LICENSE"] = "VOICEVOX" in cl
    findings["G-009 VOICEVOX in NOTICES"] = "VOICEVOX" in nt
    findings["G-010 LICENSE at repo root"] = (
        Path("../LICENSE").exists() or Path("LICENSE").exists()
    )

    # G-014 README claims
    readme = Path("README.md").read_text(encoding="utf-8")
    findings["G-014 README claims 'no-track'"] = bool(
        re.search(r"no[\s-]?track|zero[\s-]?tracking", readme, re.IGNORECASE)
    )

    for k, v in findings.items():
        print(f"  {k}: {v}")
    return findings


# ----------- H. PERFORMANCE -----------
def check_performance():
    section("H. PERFORMANCE")
    findings = {}
    # H-004 JS bundle sizes
    js_total = sum(os.path.getsize(f) for f in glob.glob("js/*.js"))
    min_total = sum(os.path.getsize(f) for f in glob.glob("js/min/*.js"))
    findings["H-004 JS unminified total (KB)"] = f"{js_total / 1024:.1f}"
    findings["H-004 JS minified total (KB)"] = f"{min_total / 1024:.1f}"

    # H-006/010 SW
    sw = Path("sw.js")
    if sw.exists():
        sc = sw.read_text(encoding="utf-8")
        findings["H-006 SW CACHE_VERSION constant"] = "CACHE_VERSION" in sc
        findings["H-006 SW precaches audio"] = ".mp3" in sc
        findings["H-010 SW skipWaiting"] = "skipWaiting" in sc

    # H-022 sitemap
    sm = Path("sitemap.xml")
    findings["H-022 sitemap.xml exists"] = sm.exists()
    if sm.exists():
        findings["H-022 sitemap URLs"] = sm.read_text(encoding="utf-8").count(
            "<url>"
        )

    # H-023 OG tags
    html = Path("index.html").read_text(encoding="utf-8")
    for og in ("og:title", "og:description", "og:type", "og:image", "og:url"):
        findings[f"H-023 {og}"] = og in html

    # H-024 canonical
    findings["H-024 canonical link"] = 'rel="canonical"' in html

    # H-018 Noto Sans fallback in CSS
    css_files = glob.glob("css/*.css")
    has_noto_cjk = False
    for cf in css_files:
        if "Noto Sans CJK" in Path(cf).read_text(encoding="utf-8"):
            has_noto_cjk = True
            break
    findings["H-018 Noto Sans CJK in CSS"] = has_noto_cjk

    # H-021 Hindi text-expansion CSS
    has_hi_expansion = False
    for cf in css_files:
        c = Path(cf).read_text(encoding="utf-8")
        if "lang=" in c or ".hi" in c or "[lang|='hi']" in c:
            has_hi_expansion = True
            break
    findings["H-021 Hindi locale-specific CSS"] = has_hi_expansion

    for k, v in findings.items():
        print(f"  {k}: {v}")
    return findings


# ----------- I. DATA ENGINEERING -----------
def check_data_eng():
    section("I. DATA ENGINEERING")
    findings = {}
    # I-004: schema_version field
    n_with_sv = 0
    n_without_sv = 0
    for path in glob.glob("data/*.json"):
        if ".bak" in path:
            continue
        try:
            d = json.load(open(path, encoding="utf-8"))
        except Exception:
            continue
        if not isinstance(d, dict):
            continue
        sv = (
            d.get("_meta", {}).get("schema_version")
            if isinstance(d.get("_meta"), dict)
            else None
        ) or d.get("schema_version")
        if sv:
            n_with_sv += 1
        else:
            n_without_sv += 1
    findings["I-004 data files with schema_version"] = n_with_sv
    findings["I-004 data files without schema_version"] = n_without_sv

    # I-007: backup files in tree
    n_baks = len(list(Path("data").rglob("*.bak*")))
    findings["I-007 data/*.bak* files"] = n_baks

    # I-009: CI runs check_content_integrity.py
    wf = Path(".github/workflows/content-integrity.yml")
    if wf.exists():
        wc = wf.read_text(encoding="utf-8")
        findings["I-009 CI runs check_content_integrity.py"] = (
            "check_content_integrity.py" in wc
        )

    # I-011: CI timeout
    timeouts = []
    for wf in Path(".github/workflows").iterdir():
        c = wf.read_text(encoding="utf-8")
        timeouts.extend(re.findall(r"timeout-minutes:\s*(\d+)", c))
    findings["I-011 workflow timeouts (minutes)"] = timeouts

    for k, v in findings.items():
        print(f"  {k}: {v}")
    return findings


# ----------- M. OPERATIONS -----------
def check_ops():
    section("M. OPERATIONS")
    findings = {}
    # M-001 deploy rollback procedure documented
    sh = Path("SELFHOST.md").read_text(encoding="utf-8") if Path(
        "SELFHOST.md"
    ).exists() else ""
    findings["M-001 SELFHOST.md mentions rollback"] = (
        "rollback" in sh.lower() or "revert" in sh.lower()
    )

    # M-007 README accuracy — check version match
    readme = Path("README.md").read_text(encoding="utf-8")
    version_json = json.load(open("data/version.json", encoding="utf-8"))
    counts = version_json.get("counts", {})
    # Look for grammar pattern count in README
    n_pat = counts.get("grammar", 178)
    findings[f"M-007 README mentions {n_pat} grammar"] = (
        str(n_pat) in readme
    )

    # M-008 CONTRIBUTING.md
    findings["M-008 CONTRIBUTING.md exists"] = (
        Path("CONTRIBUTING.md").exists()
        or Path("../CONTRIBUTING.md").exists()
    )

    # M-009 cross-link integrity within /docs
    n_docs_links = 0
    n_broken_docs_links = 0
    docs_dir = Path("docs")
    if docs_dir.exists():
        for md in docs_dir.rglob("*.md"):
            try:
                c = md.read_text(encoding="utf-8")
            except Exception:
                continue
            for m in re.finditer(r"\]\(([^)]+\.md)\)", c):
                n_docs_links += 1
                target = m.group(1)
                if target.startswith("http"):
                    continue
                resolved = (md.parent / target).resolve()
                if not resolved.exists():
                    n_broken_docs_links += 1
                    if n_broken_docs_links < 6:
                        print(f"  BROKEN docs link in {md.name}: {target}")
    findings["M-009 docs internal links"] = n_docs_links
    findings["M-009 broken docs links"] = n_broken_docs_links

    # M-010 audit-coverage doc dated correctly
    ac = Path("docs/AUDIT-COVERAGE-2026-05-15.md")
    if ac.exists():
        c = ac.read_text(encoding="utf-8")
        findings["M-010 audit-coverage has 2026-05-17 addendum"] = (
            "2026-05-17" in c
        )

    # M-013/014 dev briefs
    dev_briefs = list(Path(".").glob("**/jlpt-n5-tutor-developer-brief*"))
    findings["M-013/014 developer-brief docs"] = len(dev_briefs)

    for k, v in findings.items():
        print(f"  {k}: {v}")
    return findings


# ----------- L. CULTURAL -----------
def check_cultural():
    section("L. CULTURAL")
    findings = {}
    # L-003 gender balance in dialogue speakers (listening.json)
    L = json.load(open("data/listening.json", encoding="utf-8"))
    f_count = 0
    m_count = 0
    for it in L.get("items", []):
        vp = it.get("audio_render_meta", {}).get("voice_planned_for_engine") or {}
        f = vp.get("F")
        m = vp.get("M")
        if f and isinstance(f, dict):
            f_count += 1
        if m and isinstance(m, dict):
            m_count += 1
    findings["L-003 F-speaker items"] = f_count
    findings["L-003 M-speaker items"] = m_count
    findings["L-003 F/(F+M) ratio"] = (
        f"{f_count / (f_count + m_count):.2f}" if (f_count + m_count) else "n/a"
    )

    for k, v in findings.items():
        print(f"  {k}: {v}")
    return findings


# ----------- D. UX (limited agent-side) -----------
def check_ux():
    section("D. UX DESIGN")
    findings = {}
    # D-001 Submit button prominence — look for primary action in CSS
    css = ""
    for f in glob.glob("css/*.css"):
        css += Path(f).read_text(encoding="utf-8") + "\n"
    findings["D primary-action CSS class"] = bool(
        re.search(r"\.(primary|btn-primary|cta|submit)\b", css)
    )

    # D-018 error-state surfacing
    findings["D error-state CSS"] = bool(
        re.search(r"\.(error|err|invalid|wrong)\b", css)
    )

    for k, v in findings.items():
        print(f"  {k}: {v}")
    return findings


# ----------- E. ACCESSIBILITY -----------
def check_a11y():
    section("E. ACCESSIBILITY")
    findings = {}
    html = Path("index.html").read_text(encoding="utf-8")
    findings["E html-lang attribute"] = bool(re.search(r'<html[^>]*lang=', html))
    findings["E skip-link / skip-to-main"] = bool(
        re.search(r"skip[\s-]?to[\s-]?(main|content)|#main\b", html, re.IGNORECASE)
    )
    findings["E aria-live regions in HTML"] = "aria-live" in html
    # Check ARIA in JS UI builders
    js_content = ""
    for f in glob.glob("js/*.js"):
        try:
            js_content += Path(f).read_text(encoding="utf-8") + "\n"
        except Exception:
            pass
    findings["E aria-* in JS rendering"] = bool(
        re.search(r"aria-(label|describedby|live|hidden|expanded)", js_content)
    )
    findings["E role=button in HTML/JS"] = 'role="button"' in html or 'role="button"' in js_content

    for k, v in findings.items():
        print(f"  {k}: {v}")
    return findings


# ----------- N. END-USER POV (limited) -----------
def check_enduser():
    section("N. END-USER POV")
    findings = {}
    # N-001 onboarding visible
    html = Path("index.html").read_text(encoding="utf-8")
    findings["N onboarding text in shell"] = (
        "onboard" in html.lower() or "welcome" in html.lower() or "start" in html.lower()
    )
    # N-005 feedback channel
    findings["N feedback channel link"] = bool(
        re.search(r'feedback|contact|report', html, re.IGNORECASE)
    )

    for k, v in findings.items():
        print(f"  {k}: {v}")
    return findings


def main() -> int:
    check_security()
    check_privacy()
    check_performance()
    check_data_eng()
    check_ops()
    check_cultural()
    check_ux()
    check_a11y()
    check_enduser()
    return 0


if __name__ == "__main__":
    sys.exit(main())
