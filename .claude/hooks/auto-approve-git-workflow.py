#!/usr/bin/env python3
"""
PreToolUse hook — allow EVERYTHING in this repo EXCEPT delete/remove.

Rewritten 2026-05-30. The prior version enumerated "safe shapes" and DEFERRED
everything else to a permission prompt — that was whack-a-mole: every new
command shape (curl chains, `python -c`, pytest, node, ...) produced a fresh
prompt. This version inverts the posture to match the user's standing grant
("full autonomous permission EXCEPT delete/remove"):

    1. transient temp-file cleanup (rm -f *.commit_msg.tmp / *.tmp / .tmp_*) -> ALLOW
    2. ANY other delete / remove / history-destroy / system-destructive op    -> DENY
    3. everything else                                                         -> ALLOW

Why a hook and not just settings allow/deny? In Claude Code Desktop,
defaultMode "bypassPermissions" + a `Bash(*)` allow rule do NOT reliably
suppress prompts for multi-line / compound commands, but a PreToolUse hook
that emits an explicit permissionDecision is honored for every command shape.
A hook "deny" overrides the `Bash(*)` allow, so deletions are reliably blocked.

Fail-safe: when a command contains a delete/remove verb that is NOT a clean
transient-temp cleanup, we DENY (never silently allow a deletion). The settings
deny list in settings.local.json remains as a second, independent backstop.

Governs the Bash and PowerShell tools (register via matcher "Bash|PowerShell").
Non-shell tools, empty input, and parse errors exit 0 silently so the normal
permission system decides.

Output (Claude Code hook v3 schema):
  {"hookSpecificOutput": {"hookEventName": "PreToolUse",
                          "permissionDecision": "allow"|"deny",
                          "permissionDecisionReason": "<why>"}}

Limitation: shell-level deletes are caught; arbitrary in-code deletions beyond
the common shutil/os/pathlib calls below are not regex-detectable.

Author: Gaurav Srivastava (via Claude). Created 2026-05-27; allow-all-except-
delete rewrite 2026-05-30.
"""
import json
import re
import sys

# --- delete / remove detection --------------------------------------------
# A segment is a DELETE only when a delete verb is in COMMAND position (start
# of the segment), so "grep rm ...", "man rm", paths containing 'rm', etc. are
# NOT mis-flagged. git ref-removal and common in-code deletions are matched
# anywhere in the segment.
_DELETE_CMD_RE = re.compile(
    r'^(?:rm|rmdir|unlink|shred|del|erase|Remove-Item|Clear-Content)\b',
    re.IGNORECASE)
_GIT_REMOVE_RE = re.compile(
    r'\bgit\s+(?:rm\b|branch\s+-D\b|tag\s+-d\b|stash\s+(?:drop|clear)\b)',
    re.IGNORECASE)
_PY_DELETE_RE = re.compile(
    r'(?:shutil\.rmtree|os\.removedirs|os\.remove|os\.unlink|os\.rmdir'
    r'|\.unlink\(|\.rmdir\()',
    re.IGNORECASE)

# A token is a transient scratch file Claude itself creates/cleans up.
_TRANSIENT_TOKEN_RE = re.compile(r'(?:\.commit_msg\.tmp$|\.tmp$|\.tmp_)',
                                 re.IGNORECASE)
# Recursive / force-recursive delete flags (never a legit transient cleanup).
_RECURSIVE_RE = re.compile(r'(?:-[A-Za-z]*[rR]\b|/[sS]\b|-Recurse\b)')

# History-rewriting / system-destructive ops that are not plain file deletes.
# Includes positional backstops (recursive rm / find -delete / xargs rm) so a
# wrapped form (sudo/time/...) is still caught even if command-position
# detection above missed it.
_DESTRUCTIVE_RE = [re.compile(p, re.IGNORECASE) for p in (
    r'\brm\s+-[A-Za-z]*[rR]\b',                 # recursive rm anywhere
    r'\bfind\b[^|&;\n]*-delete\b',
    r'\bfind\b[^|&;\n]*-exec\s+rm',
    r'\bxargs\b[^|&;\n]*\brm\b',
    r'\bgit\s+push\s+[^|&;\n]*(?:--force|--force-with-lease|-f\b|--no-verify)',
    r'\bgit\s+reset\s+--hard\b',
    r'\bgit\s+clean\s+-[A-Za-z]*f',
    r'\bgit\s+filter-(?:branch|repo)\b',
    r'\bformat\b', r'\bmkfs', r'\bdd\s+if=',
    r'\bshutdown\b', r'\breboot\b', r'\bdiskpart\b',
    r'\bStop-Computer\b', r'\bRestart-Computer\b', r'\bFormat-Volume\b',
    r'\bStop-Process\s+[^|&;\n]*-Force',
    r'\bnpm\s+uninstall\b', r'\bpip3?\s+uninstall\b',
    r'(?:\bmv\b|\bcp\b|\bMove-Item\b|\bCopy-Item\b)[^|&;\n]*\.(?:bak|backup)\b',
)]


def _decide(decision, reason):
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": decision,
        "permissionDecisionReason": reason,
    }}))
    return 0


def _segments(command):
    return re.split(r'(?:&&|\|\||[;|&\n])', command)


def _strip_wrappers(seg):
    s = seg.strip().lstrip('(').strip()
    # Drop common leading wrappers so "sudo rm", "time rm" still detect.
    s = re.sub(r'^(?:sudo|time|nice|nohup|command|builtin|exec)\s+', '', s,
               flags=re.IGNORECASE)
    return s


def _segment_is_delete(seg):
    s = _strip_wrappers(seg)
    return bool(_DELETE_CMD_RE.match(s) or _GIT_REMOVE_RE.search(seg)
                or _PY_DELETE_RE.search(seg))


def _is_safe_transient_delete(seg):
    """True only if seg is a non-recursive rm/del whose every target is a
    scratch temp file (*.commit_msg.tmp / *.tmp / .tmp_*)."""
    s = _strip_wrappers(seg)
    if not re.match(r'^(?:rm|del|erase|Remove-Item)\b', s, re.IGNORECASE):
        return False
    if _RECURSIVE_RE.search(s) or _GIT_REMOVE_RE.search(seg) or _PY_DELETE_RE.search(seg):
        return False
    targets = [t.strip('"\'') for t in s.split()[1:]
               if not t.startswith('-') and not t.startswith('/')]
    return bool(targets) and all(_TRANSIENT_TOKEN_RE.search(t) for t in targets)


def _command_has_delete(command):
    return any(_segment_is_delete(seg) for seg in _segments(command))


def _deletes_are_only_transient(command):
    for seg in _segments(command):
        if _segment_is_delete(seg) and not _is_safe_transient_delete(seg):
            return False
    return True


def main():
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return 0
        invocation = json.loads(raw)
    except Exception:
        return 0  # malformed input — defer to permission system

    if invocation.get('tool_name', '') not in ('Bash', 'PowerShell'):
        return 0  # only govern shell tools; defer everything else
    command = (invocation.get('tool_input', {}) or {}).get('command', '') or ''
    if not command.strip():
        return 0

    # 1. Restricted directory — never touch.
    if 'SS&SC' in command:
        return _decide('deny', 'Restricted directory SS&SC is off-limits.')

    # 2. Delete / remove: allow ONLY transient temp-file cleanup; deny the rest.
    if _command_has_delete(command):
        if _deletes_are_only_transient(command):
            return _decide('allow', 'Transient temp-file cleanup (non-destructive).')
        return _decide('deny', 'Delete/remove blocked by repo policy '
                               '(full permission granted EXCEPT delete/remove).')

    # 3. History-rewriting / system-destructive ops — deny.
    for rx in _DESTRUCTIVE_RE:
        if rx.search(command):
            return _decide('deny',
                           'Destructive/history-rewriting op blocked by repo policy.')

    # 4. Everything else — allow (zero-prompt posture).
    return _decide('allow', 'Allowed by repo policy (full permission except delete/remove).')


if __name__ == '__main__':
    sys.exit(main())
