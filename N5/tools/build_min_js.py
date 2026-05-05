"""ISSUE-043 (audit round-5): minify every js/*.js source file into
js/min/<name>.js using esbuild via npx. The original sources stay in
the repo for editing + debugging; the minified copies are what
index.html ships in production.

esbuild is invoked through `npx --yes esbuild` so no project-level
devDep install is required — esbuild is fetched lazily at first run
and cached by npm. Total minified bundle size drops ~30-40%.

Idempotent: re-running rewrites every js/min/<name>.js. Safe to run
on every build via `npm run build:js`.

Skip-on-error: if `npx esbuild` is unavailable in the local env (no
network, npm blocked), this script prints a warning and exits 0 so
the build pipeline continues with the unminified files. The
runtime references js/<name>.js by default; we'll wire the minified
path in a follow-up after smoke-test.
"""
from __future__ import annotations
import io, os, subprocess, sys
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

ROOT = Path(__file__).resolve().parent.parent
JS_SRC = ROOT / 'js'
JS_OUT = ROOT / 'js' / 'min'


def main() -> int:
    JS_OUT.mkdir(parents=True, exist_ok=True)

    sources = sorted(p for p in JS_SRC.glob('*.js') if p.parent == JS_SRC)
    if not sources:
        print('No JS sources found.')
        return 0

    total_src = 0
    total_min = 0
    failures = []

    for src in sources:
        out = JS_OUT / src.name
        cmd = [
            'npx', '--yes', 'esbuild', str(src),
            '--minify',
            '--target=es2020',
            '--format=esm',
            f'--outfile={out}',
            '--log-level=warning',
        ]
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, shell=True)
            if r.returncode != 0:
                failures.append((src.name, r.stderr.strip()[:200]))
                continue
        except Exception as e:
            failures.append((src.name, str(e)))
            continue
        if out.exists():
            src_b = src.stat().st_size
            min_b = out.stat().st_size
            total_src += src_b
            total_min += min_b
            print(f'  {src.name:<28} {src_b:>7} -> {min_b:>7} (-{100*(src_b-min_b)//src_b:>2}%)')

    if failures:
        print(f'\n{len(failures)} file(s) failed to minify (skip-on-error):')
        for name, err in failures[:5]:
            print(f'  {name}: {err}')

    if total_src:
        print(f'\nTotal: {total_src} -> {total_min} bytes (-{100*(total_src-total_min)//total_src}%)')
    return 0


if __name__ == '__main__':
    sys.exit(main())
