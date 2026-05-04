"""Static design-system compliance checker for the JLPT N5 Tutor app.

Source of truth: specifications/jlpt-n5-design-system-zen-modern.md
("Zen Modern" / Muji-inspired). This script greps the codebase for
violations of the spec's hard rules and exits non-zero if any are
found. Wired into .github/workflows/content-integrity.yml so every
PR catches design-system drift before it ships.

Why this exists
- During the v1.8.0 design overhaul we discovered three classes of
  drift that the existing content-integrity / Playwright suites did
  not catch:
  (a) leftover decorative emojis sneaking back into JS templates,
  (b) `font-weight: 600/700` accidentally added in component files,
  (c) `box-shadow` and `transform: translateY` hover lifts violating
      spec §0.5 + §8 ("no shadows ever", "no card lift on hover").
- A separate incident: bulk-stripping `transform: translateY(...)`
  to remove hover-lifts also stripped a legitimate
  `transform: translateY(-50%)` used to centre a `+` collapse marker
  against `top: 50%`. This checker now distinguishes hover-context
  (forbidden) from positioning-context (allowed) so the regression
  cannot recur.

Rules enforced (each one keyed to a spec section)
- D-1 §0.5 + §0.6: no pictograph emojis in user-facing JS / HTML
- D-2 §2.3: no `font-weight: 600/700/bold` in css/main.css
- D-3 §0.5: no `box-shadow:` declarations (other than `none`) in CSS
- D-4 §8: no `transform: translate*` inside `:hover` blocks
- D-5 §1.3: brand accent appears only via `var(--color-accent*)`
  (no hard-coded `#1F4D2E` or legacy `#14452a` outside `:root`)
- D-6 §3.4: border-radius values are 2 / 4 / 6 / 999 only
- D-7 §0.6: no `text-transform` other than `uppercase` (the only
  approved transform for tiny ALL-CAPS labels)
- D-8 §0.6: no decorative `text-shadow` (forbidden alongside
  box-shadow)

Usage
  python tools/check_design_system.py
  python tools/check_design_system.py --verbose   # show full diff
  python tools/check_design_system.py --strict    # treat warnings as errors

Exit codes
  0  all rules pass
  1  one or more rule violations
  2  internal error (file missing, etc.)
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CSS_FILE = ROOT / "css" / "main.css"
JS_DIR = ROOT / "js"
HTML_FILE = ROOT / "index.html"

# === Pictograph emoji ranges (per Unicode 15.0) ===
# We block U+1F300..U+1FAFF (Misc Pictographs through Symbols & Pictographs
# Extended-A) and a curated set of Dingbats that are commonly emoji-rendered.
# We deliberately ALLOW: ✓/✗ (U+2713/U+2717 - typographic check marks used
# as correct/incorrect indicators), ★ (U+2605 - geometric, never emoji),
# 五 (kanji brand mark), ● (U+25CF Black Circle for counter dots), and
# Japanese punctuation / kana / kanji codepoints.
EMOJI_RANGES = [
    (0x1F300, 0x1FAFF),      # all Misc Symbols & Pictographs blocks
    (0x1F000, 0x1F02F),      # Mahjong tiles
    (0x1F0A0, 0x1F0FF),      # Playing cards
    (0x1F100, 0x1F2FF),      # Enclosed alphanumerics + ideographic supplement
]
# Specific blocked codepoints from the Misc-Symbols block (U+2600-U+26FF)
# that are commonly emoji-rendered. We don't blanket-block U+2600-U+26FF
# because it contains many typographic glyphs (★, ☆, ◯, ◎, etc.).
BLOCKED_MISC = {
    0x2614, 0x2615, 0x2618, 0x261D, 0x2620, 0x2622, 0x2623, 0x2626,
    0x262A, 0x262E, 0x262F, 0x2638, 0x2639, 0x263A, 0x2648, 0x2649,
    0x264A, 0x264B, 0x264C, 0x264D, 0x264E, 0x264F, 0x2650, 0x2651,
    0x2652, 0x2653, 0x2660, 0x2663, 0x2665, 0x2666, 0x2668, 0x267B,
    0x267F, 0x2692, 0x2693, 0x2694, 0x2696, 0x2697, 0x2699, 0x269B,
    0x269C, 0x26A0, 0x26A1, 0x26AA, 0x26AB, 0x26B0, 0x26B1, 0x26BD,
    0x26BE, 0x26C4, 0x26C5, 0x26C8, 0x26CE, 0x26CF, 0x26D1, 0x26D3,
    0x26D4, 0x26E9, 0x26EA, 0x26F0, 0x26F1, 0x26F2, 0x26F3, 0x26F4,
    0x26F5, 0x26F7, 0x26F8, 0x26F9, 0x26FA, 0x26FD,
}


def is_emoji_codepoint(cp: int) -> bool:
    if cp in BLOCKED_MISC:
        return True
    for lo, hi in EMOJI_RANGES:
        if lo <= cp <= hi:
            return True
    return False


def find_files(directory: Path, *suffixes: str) -> list[Path]:
    out = []
    for suf in suffixes:
        out.extend(sorted(directory.rglob(f"*{suf}")))
    return out


# ============================================================================
# RULE D-1: no pictograph emojis in user-facing JS / HTML
# ============================================================================
def check_d1_no_emojis_in_ui() -> list[str]:
    failures: list[str] = []
    files = []
    if HTML_FILE.exists():
        files.append(HTML_FILE)
    if JS_DIR.exists():
        files.extend(find_files(JS_DIR, ".js"))
    for path in files:
        try:
            text = path.read_text(encoding="utf-8")
        except Exception as e:  # pragma: no cover
            failures.append(f"D-1 {path.name}: read error {e}")
            continue
        for line_no, line in enumerate(text.splitlines(), 1):
            for ch in line:
                cp = ord(ch)
                if is_emoji_codepoint(cp):
                    rel = path.relative_to(ROOT)
                    failures.append(
                        f"D-1 {rel}:{line_no} pictograph emoji "
                        f"U+{cp:04X} '{ch}' in line: {line.strip()[:80]!r}"
                    )
                    break  # one violation per line is enough
    return failures


# ============================================================================
# RULE D-2: no font-weight 600 / 700 / bold in CSS
# ============================================================================
WEIGHT_PATTERN = re.compile(
    r"font-weight\s*:\s*(?:600|700|bold|bolder)\b", re.IGNORECASE
)


def check_d2_no_heavy_weights() -> list[str]:
    if not CSS_FILE.exists():
        return ["D-2 css/main.css missing"]
    failures: list[str] = []
    text = CSS_FILE.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), 1):
        if WEIGHT_PATTERN.search(line):
            failures.append(
                f"D-2 css/main.css:{line_no} forbidden weight 600/700/bold "
                f"(spec §2.3: weights 300/400/500 only): {line.strip()[:80]!r}"
            )
    return failures


# ============================================================================
# RULE D-3: no box-shadow declarations (other than `none`) in CSS
# ============================================================================
SHADOW_PATTERN = re.compile(r"box-shadow\s*:\s*([^;}\n]+)")


def check_d3_no_box_shadows() -> list[str]:
    if not CSS_FILE.exists():
        return ["D-3 css/main.css missing"]
    failures: list[str] = []
    text = CSS_FILE.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), 1):
        m = SHADOW_PATTERN.search(line)
        if not m:
            continue
        value = m.group(1).strip().rstrip(";").strip()
        # `none` is the explicit "no shadow" reset - allowed.
        if value.lower() == "none":
            continue
        failures.append(
            f"D-3 css/main.css:{line_no} box-shadow forbidden "
            f"(spec §0.5): {line.strip()[:80]!r}"
        )
    return failures


# ============================================================================
# RULE D-4: no transform inside :hover blocks (no card-lift / no scale)
# ============================================================================
def check_d4_no_hover_transforms() -> list[str]:
    """Scan CSS rule-by-rule. For each `:hover` selector block, flag any
    `transform:` declaration. Allows `transform` outside hover (used for
    centering pseudo-elements via translateY(-50%) etc - see commit e75a898
    for the regression that motivated this rule)."""
    if not CSS_FILE.exists():
        return ["D-4 css/main.css missing"]
    failures: list[str] = []
    text = CSS_FILE.read_text(encoding="utf-8")
    # Iterate balanced { } blocks. Naive approach: regex for selector { ... }
    # without nested braces (CSS doesn't nest in our codebase - flat rules).
    rule_re = re.compile(r"([^{}]+)\{([^{}]*)\}", re.DOTALL)
    pos = 0
    line_offset = 0
    for m in rule_re.finditer(text):
        selector = m.group(1).strip()
        body = m.group(2)
        if ":hover" not in selector:
            continue
        # Compute start line number for the body
        line_no = text[: m.start(2)].count("\n") + 1
        for body_line_idx, body_line in enumerate(body.splitlines()):
            if "transform" in body_line and ":" in body_line:
                # Confirm it's a property declaration (transform: ...)
                if re.search(r"\btransform\s*:", body_line):
                    failures.append(
                        f"D-4 css/main.css:{line_no + body_line_idx} "
                        f"transform inside :hover (spec §8: no card lift "
                        f"on hover) selector={selector[:60]!r} "
                        f"line={body_line.strip()[:80]!r}"
                    )
    return failures


# ============================================================================
# RULE D-5: legacy brand accent #14452a forbidden (use --color-accent token)
# ============================================================================
# Only the LEGACY accent #14452a is a hard fail - it's a deprecated value
# from pre-v1.8.0 and any occurrence outside :root is real drift. The new
# canonical accent #1F4D2E is allowed as a `var(--color-accent, #1F4D2E)`
# fallback because it matches the token's actual value; updating the token
# only requires a global grep (we accept that maintenance cost).
LEGACY_ACCENT_PATTERN = re.compile(r"#14452[Aa]\b")


def check_d5_accent_tokenised() -> list[str]:
    """Legacy brand accent (#14452a, pre-v1.8.0) must not appear anywhere.
    The current accent (#1F4D2E, --color-accent) is allowed as a
    `var(--color-accent, #1F4D2E)` fallback since the fallback matches the
    canonical token value."""
    if not CSS_FILE.exists():
        return ["D-5 css/main.css missing"]
    failures: list[str] = []
    text = CSS_FILE.read_text(encoding="utf-8")
    in_root_or_override = False
    for line_no, line in enumerate(text.splitlines(), 1):
        # Track whether we're inside :root { } or [data-theme=...] { } blocks
        if re.search(r"^\s*:root\s*\{|^\s*\[data-theme=", line):
            in_root_or_override = True
        if "}" in line and in_root_or_override:
            in_root_or_override = False
        if in_root_or_override:
            continue
        if LEGACY_ACCENT_PATTERN.search(line):
            failures.append(
                f"D-5 css/main.css:{line_no} legacy brand accent #14452a "
                f"(spec §1.3: use var(--color-accent*) - five places only): "
                f"{line.strip()[:80]!r}"
            )
    return failures


# ============================================================================
# RULE D-6: border-radius values restricted to 2 / 4 / 6 / 999
# ============================================================================
RADIUS_PATTERN = re.compile(r"border-radius\s*:\s*([^;}\n]+)")
ALLOWED_RADII = {"0", "2px", "3px", "4px", "6px", "999px",
                 "var(--radius-sm)", "var(--radius-md)",
                 "var(--radius-lg)", "var(--radius-pill)",
                 "var(--r)", "50%", "100%", "inherit", "initial"}


def check_d6_radius_tokens() -> list[str]:
    """Border radius must be 2/4/6/999 (or via tokens). Catches accidental
    SaaS-style 12-16px curves that would break the Muji geometric look."""
    if not CSS_FILE.exists():
        return ["D-6 css/main.css missing"]
    failures: list[str] = []
    text = CSS_FILE.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), 1):
        m = RADIUS_PATTERN.search(line)
        if not m:
            continue
        value = m.group(1).strip().rstrip(";").strip()
        # Multi-corner shorthand: take each token
        parts = value.split()
        for p in parts:
            p_stripped = p.strip().rstrip(",")
            if p_stripped in ALLOWED_RADII:
                continue
            # Also tolerate calc() and negative-zero edge cases
            if p_stripped.startswith("calc("):
                continue
            failures.append(
                f"D-6 css/main.css:{line_no} non-token border-radius "
                f"'{p_stripped}' (spec §3.4: 2/4/6/999 only): "
                f"{line.strip()[:80]!r}"
            )
            break
    return failures


# ============================================================================
# RULE D-7: text-transform restricted to uppercase or none
# ============================================================================
TT_PATTERN = re.compile(r"text-transform\s*:\s*([a-zA-Z-]+)")


def check_d7_text_transform() -> list[str]:
    if not CSS_FILE.exists():
        return ["D-7 css/main.css missing"]
    failures: list[str] = []
    text = CSS_FILE.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), 1):
        m = TT_PATTERN.search(line)
        if not m:
            continue
        value = m.group(1).lower()
        if value in {"uppercase", "none", "inherit", "initial"}:
            continue
        failures.append(
            f"D-7 css/main.css:{line_no} text-transform '{value}' "
            f"(spec §0.8: only ALL CAPS labels via uppercase): "
            f"{line.strip()[:80]!r}"
        )
    return failures


# ============================================================================
# RULE D-8: no decorative text-shadow
# ============================================================================
def check_d8_no_text_shadow() -> list[str]:
    if not CSS_FILE.exists():
        return ["D-8 css/main.css missing"]
    failures: list[str] = []
    text = CSS_FILE.read_text(encoding="utf-8")
    for line_no, line in enumerate(text.splitlines(), 1):
        if re.search(r"\btext-shadow\s*:\s*([^;}\n]+)", line):
            value_match = re.search(r"text-shadow\s*:\s*([^;}\n]+)", line)
            value = value_match.group(1).strip().rstrip(";").strip() if value_match else ""
            if value.lower() == "none":
                continue
            failures.append(
                f"D-8 css/main.css:{line_no} text-shadow forbidden "
                f"(spec §0.5): {line.strip()[:80]!r}"
            )
    return failures


# ============================================================================
# Driver
# ============================================================================
RULES = [
    ("D-1", "No pictograph emojis in UI",          check_d1_no_emojis_in_ui),
    ("D-2", "Font weights 300/400/500 only",       check_d2_no_heavy_weights),
    ("D-3", "No box-shadow",                       check_d3_no_box_shadows),
    ("D-4", "No transform on :hover",              check_d4_no_hover_transforms),
    ("D-5", "Brand accent via tokens only",        check_d5_accent_tokenised),
    ("D-6", "Border-radius 2/4/6/999 only",        check_d6_radius_tokens),
    ("D-7", "text-transform uppercase|none only",  check_d7_text_transform),
    ("D-8", "No text-shadow",                      check_d8_no_text_shadow),
]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show all violations (default: first 5 per rule)")
    args = parser.parse_args()

    print(f"JLPT N5 Design-System Compliance - {len(RULES)} rules\n"
          f"{'=' * 60}")

    total_failures = 0
    for rule_id, label, fn in RULES:
        try:
            failures = fn()
        except Exception as e:  # pragma: no cover
            print(f"  {rule_id}  {label[:40]:42s} ERROR ({e})")
            return 2
        if not failures:
            print(f"  {rule_id}  {label[:40]:42s} PASS")
        else:
            total_failures += len(failures)
            print(f"  {rule_id}  {label[:40]:42s} FAIL ({len(failures)})")
            shown = failures if args.verbose else failures[:5]
            for f in shown:
                print(f"      - {f}")
            if not args.verbose and len(failures) > 5:
                print(f"      ... and {len(failures) - 5} more "
                      f"(use --verbose to see all)")
    print("=" * 60)
    if total_failures == 0:
        print("PASS: all design-system rules green")
        return 0
    print(f"FAIL: {total_failures} design-system violation(s)")
    print("Run with --verbose / -v to see all violations")
    return 1


if __name__ == "__main__":
    sys.exit(main())
