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

# Anchored to git's subcommand position so local-only lookalikes
# (`git stash push`) don't match; `subtree push` does publish, so it stays in.
PUSH_RE = re.compile(
    r"\bgit(?:\s+(?:-[Cc]\s+\S+|--[\w-]+(?:=\S+)?))*\s+(?:subtree\s+)?push\b"
)
FORCE_RE = re.compile(r"(^|\s)(--force(-with-lease(=\S+)?)?|-f)(\s|$)")
DRY_RE = re.compile(r"(^|\s)(--dry-run|-n)(\s|$)")
SEP_RE = re.compile(r"[|;&\n]")


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
    segments = []
    for match in PUSH_RE.finditer(cmd):
        segment = cmd[match.start():]
        sep = SEP_RE.search(segment)
        segments.append(segment[:sep.start()] if sep else segment)
    if not segments:
        return 0
    if any(FORCE_RE.search(s) for s in segments):
        decide("deny",
               "force push는 이미 리뷰된 히스토리를 다시 쓰므로 금지 — "
               "커밋을 쌓아서 일반 push로 올리세요.")
        return 0
    if all(DRY_RE.search(s) for s in segments):
        return 0
    if gate_off(data.get("cwd")):
        return 0
    decide("ask",
           "git push는 커밋을 원격에 공개합니다. 이 push에 대한 명시적 지시와 "
           "push 전 검증(리뷰·테스트·eval)이 있었는지 확인하세요.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
