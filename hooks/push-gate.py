#!/usr/bin/env python3
"""PreToolUse hook for Bash: gate outward-facing git pushes.

A push publishes commits to a shared remote — it is the outward-facing moment of the git workflow, and a broad Bash allowlist or permissive session mode can let it through silently.
This hook forces a per-push human decision (permissionDecision "ask") so verification happens before publication, and hard-denies force pushes, which rewrite already-reviewed history.
Per-repo opt-out: `git config ai-roots.push-gate off` skips the ask for that repo (the force-push deny stays), restoring Claude Code's normal permission flow.
"""
import json
import re
import subprocess
import sys

PUSH_RE = re.compile(r"\bgit\b[^|;&\n]*?\bpush\b")
FORCE_RE = re.compile(r"(^|\s)(--force(-with-lease(=\S+)?)?|-f)(\s|$)")
DRY_RE = re.compile(r"(^|\s)(--dry-run|-n)(\s|$)")


def decide(decision, reason):
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PreToolUse",
            "permissionDecision": decision,
            "permissionDecisionReason": reason,
        }
    }))


def gate_off(cwd):
    try:
        out = subprocess.run(
            ["git", "-C", cwd or ".", "config", "--get", "ai-roots.push-gate"],
            capture_output=True, text=True, timeout=5,
        )
        return out.stdout.strip().lower() == "off"
    except Exception:
        return False


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    cmd = data.get("tool_input", {}).get("command", "")
    match = PUSH_RE.search(cmd)
    if not match:
        return 0
    segment = cmd[match.start():]
    if DRY_RE.search(segment):
        return 0
    if FORCE_RE.search(segment):
        decide("deny",
               "force push는 이미 리뷰된 히스토리를 다시 쓰므로 금지 — "
               "커밋을 쌓아서 일반 push로 올리세요.")
        return 0
    if gate_off(data.get("cwd")):
        return 0
    decide("ask",
           "git push는 커밋을 원격에 공개합니다. 이 push에 대한 명시적 지시와 "
           "push 전 검증(리뷰·테스트·eval)이 있었는지 확인하세요.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
