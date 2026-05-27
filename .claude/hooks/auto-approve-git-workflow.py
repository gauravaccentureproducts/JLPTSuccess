#!/usr/bin/env python3
"""
PreToolUse hook — auto-approve standard git/gh workflow commands.

Reads a Claude Code PreToolUse JSON envelope on stdin. If tool_name is
Bash AND tool_input.command matches a safe git/gh workflow shape, emits
an 'allow' decision so the user isn't re-prompted for routine workflow
commands.

Safe shapes covered:
  - git <subcmd> ...                          (standalone)
  - cd PATH && git <subcmd> ...               (with cd prefix)
  - cd PATH && git <subcmd> ... && git <subcmd> ... (chained)
  - cd PATH && ... && rm -f <something> && git push ...  (post-commit cleanup)
  - gh pr/issue/repo/release/workflow/run/api/auth ...  (GitHub CLI)
  - Any of the above piped to | tail / | head / | grep / | wc
  - Any of the above with 2>&1 stderr redirect

Defense in depth — denied shapes are NOT approved here even if the
match succeeds; the deny list in settings.local.json still fires:
  - git push --force / -f / --force-with-lease / --no-verify
  - git reset --hard
  - git branch -D
  - git clean -f / -fd
  - git checkout -- (revert-discard)
  - git filter-branch / filter-repo
  - rm -rf / rm -fr (anything)
  - Anything under C:/Users/.../SS&SC/ (restricted directory)

Non-matching commands silently exit 0; permission system handles them
normally.

Output format follows Claude Code hook v3 schema:
  {
    "hookSpecificOutput": {
      "hookEventName": "PreToolUse",
      "permissionDecision": "allow",
      "permissionDecisionReason": "<why>"
    }
  }

Author: Gaurav Srivastava (via Claude). Created 2026-05-27.
"""
import json
import re
import sys


def main():
    # Read invocation envelope
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return 0
        invocation = json.loads(raw)
    except json.JSONDecodeError:
        return 0  # Malformed input — defer to permission system
    except Exception:
        return 0

    tool_name = invocation.get('tool_name', '')
    if tool_name != 'Bash':
        return 0  # Only auto-approve Bash; defer all other tools

    command = invocation.get('tool_input', {}).get('command', '') or ''
    if not command:
        return 0

    # DENY-FIRST: never approve destructive operations even if shape matches.
    DENY_PATTERNS = [
        r'git push\s+(?:[^&|;]*\s)?(--force|--force-with-lease|-f|--no-verify)\b',
        r'git reset\s+--hard\b',
        r'git branch\s+-D\b',
        r'git clean\s+-f(d|r)?\b',
        r'git checkout\s+--\s',
        r'git filter-branch\b',
        r'git filter-repo\b',
        r'\brm\s+-rf\b',
        r'\brm\s+-fr\b',
        r'\brm\s+-r\s',
        r'SS&SC',  # Restricted directory
    ]
    for pat in DENY_PATTERNS:
        if re.search(pat, command):
            return 0  # Deny rule will fire; we don't approve

    # SAFE shapes: any of these starting forms qualify.
    GIT_SUBCMDS = (r'(?:add|commit|push|fetch|pull|status|diff|log|branch|'
                   r'stash|tag|merge|rebase|show|remote|config|restore|'
                   r'checkout|mv|ls-files|rev-parse|blame|cherry-pick|'
                   r'describe|reflog|worktree|submodule)')
    GH_SUBCMDS = r'(?:pr|issue|repo|release|workflow|run|api|auth|gist|alias|browse|search)'

    SAFE_PATTERNS = [
        # Standalone git/gh
        rf'^git\s+{GIT_SUBCMDS}\b',
        rf'^gh\s+{GH_SUBCMDS}\b',
        # cd PATH (quoted) && git ...
        rf'^cd\s+"[^"]*"\s+&&\s+git\s+{GIT_SUBCMDS}\b',
        rf'^cd\s+\'[^\']*\'\s+&&\s+git\s+{GIT_SUBCMDS}\b',
        # cd PATH (unquoted, no & or | in path — common case) && git ...
        rf'^cd\s+[^&|;\s]+\s+&&\s+git\s+{GIT_SUBCMDS}\b',
        # cd PATH && gh ...
        rf'^cd\s+"[^"]*"\s+&&\s+gh\s+{GH_SUBCMDS}\b',
        rf'^cd\s+[^&|;\s]+\s+&&\s+gh\s+{GH_SUBCMDS}\b',
        # File-based commit workflow: cd && git add && git commit -F MSG && (optional rm cleanup) && git push
        rf'^cd\s+(?:"[^"]*"|\'[^\']*\'|[^&|;\s]+)\s+&&\s+git\s+add\s.+\s+&&\s+git\s+commit\b',
    ]

    for pat in SAFE_PATTERNS:
        if re.match(pat, command):
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "allow",
                    "permissionDecisionReason": (
                        "Auto-approved by .claude/hooks/auto-approve-git-workflow.py "
                        "(safe git/gh workflow shape; deny rules still apply)."
                    ),
                }
            }
            print(json.dumps(output))
            return 0

    # No safe match; defer to permission system silently
    return 0


if __name__ == '__main__':
    sys.exit(main())
