"""IMP-021: build-time CSS minifier (audit 2026-05-04 round 2).

Reads `css/main.css` and writes `css/main.min.css`. The deployed `index.html`
references the .min.css; the source `.css` stays in the repo for editing
and review (via the Sources tab in DevTools when debugging).

Conservative approach — no third-party dependency, only the standard library:
1. Strip `/* ... */` comments (multi-line aware), but skip them when they
   sit inside a CSS string literal `"..."` / `'...'`.
2. Collapse runs of whitespace (including newlines) to a single space.
3. Drop the space immediately before/after `{`, `}`, `;`, `,`.
4. Drop the redundant `;` immediately before `}`.

What we do NOT do (to keep the minifier safe-by-default):
- We do NOT strip space around `:`, `-`, `+`, `*`, `/`, `>`, `~`. Selectors
  like `.a > .b` are unchanged; calc() expressions like `calc(100vh - 240px)`
  retain their required spaces around the binary operator.
- We do NOT shorten color literals (`#ffffff` -> `#fff`) or zero-units
  (`0px` -> `0`). Those transforms have edge cases (e.g. `#ffffff80` for
  alpha) and are not worth the maintenance burden.

Compression empirically lands around 30-35% file-size reduction for
heavily-commented stylesheets like ours, which is enough to justify the
extra HTTP byte saving without risking visual regressions.

Idempotent: running this twice produces the same `.min.css`.
"""
from __future__ import annotations
import io, re, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / 'css' / 'main.css'
DST = ROOT / 'css' / 'main.min.css'


def strip_comments_outside_strings(text: str) -> str:
    """Strip /* ... */ blocks, but only when not inside a "..."/' quote."""
    out: list[str] = []
    i = 0
    n = len(text)
    in_str: str | None = None  # holds the opening quote char while inside
    while i < n:
        ch = text[i]
        if in_str:
            out.append(ch)
            if ch == '\\' and i + 1 < n:
                out.append(text[i + 1])
                i += 2
                continue
            if ch == in_str:
                in_str = None
            i += 1
            continue
        if ch in ('"', "'"):
            in_str = ch
            out.append(ch)
            i += 1
            continue
        if ch == '/' and i + 1 < n and text[i + 1] == '*':
            # find closing
            j = text.find('*/', i + 2)
            if j < 0:
                # unterminated — keep verbatim and stop
                out.append(text[i:])
                return ''.join(out)
            i = j + 2
            continue
        out.append(ch)
        i += 1
    return ''.join(out)


def minify(css: str) -> str:
    css = strip_comments_outside_strings(css)
    # Collapse runs of whitespace (incl. newlines) to a single space.
    css = re.sub(r'\s+', ' ', css)
    # Drop whitespace immediately around the structural punctuators.
    css = re.sub(r'\s*([{};,])\s*', r'\1', css)
    # Drop redundant ; before } (declarations don't need a trailing ;).
    css = css.replace(';}', '}')
    return css.strip() + '\n'


def main() -> int:
    if not SRC.exists():
        print(f'ERROR: {SRC} not found.')
        return 1

    src = SRC.read_text(encoding='utf-8')
    dst = minify(src)

    # Header banner so the file is identifiable when served.
    banner = (
        '/*! JLPT N5 styles (build-min). Source: css/main.css. '
        'Regen: python tools/build_min_css.py */\n'
    )
    DST.write_text(banner + dst, encoding='utf-8')

    src_bytes = len(src.encode('utf-8'))
    dst_bytes = len(dst.encode('utf-8')) + len(banner.encode('utf-8'))
    saving = 100 * (src_bytes - dst_bytes) // src_bytes
    print(f'main.css       {src_bytes:>7} bytes')
    print(f'main.min.css   {dst_bytes:>7} bytes  (-{saving}%)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
