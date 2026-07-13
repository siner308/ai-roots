#!/usr/bin/env python3
"""PreToolUse gate for Bash blocking the one thing the skill can't self-enforce.

gh CLI corrupts markdown in every body channel (`- ` -> `•`, backticks stripped, `- [ ]` -> `[ ]`), and that happens inside gh AFTER the model has done everything right — so even a body that perfectly follows the `github-pr-markdown` skill comes out broken.
A prompt rule can't fix a corruption that happens past the prompt; only a gate can.
So a `gh pr/issue ...` body that CONTAINS markdown is blocked: create with an empty body, then PATCH via the GitHub API.
A plain-text body (nothing for gh to mangle) passes.

Everything else — bullet/checkbox/section formatting, body length, structure — is the `github-pr-markdown` skill's job.
This hook does not re-encode those rules; it points at the skill.
Duplicating them here is what let the two drift apart.

Fail-open: any parse/IO error or unrecognized shape exits 0 (allow), so it never wedges unrelated Bash.
It blocks (exit 2) only on a positively-identified problem.
"""
import json
import os
import re
import shlex
import sys

GH_BODY_RE = re.compile(
    r"\bgh\s+(?:pr\s+(?:create|edit|comment|review)|issue\s+(?:create|edit|comment))\b"
)
# Any of these means the body holds markdown gh would corrupt.
MARKDOWN_RE = re.compile(r"(?m)^\s*[-*+]\s|`|^\s*#{1,6}\s|^\s*\[[ xX]\]|\[[^\]]+\]\([^)]+\)")

BODY_FLAGS = {"-b", "--body"}
BODY_FILE_FLAGS = {"-F", "--body-file"}


def block(reason):
    print("gh-markdown-style: " + reason, file=sys.stderr)
    sys.exit(2)


def read_file(path):
    try:
        with open(os.path.expanduser(path), encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def flag_value(tokens, names):
    for i, tok in enumerate(tokens):
        for name in names:
            if tok == name and i + 1 < len(tokens):
                return tokens[i + 1]
            if tok.startswith(name + "="):
                return tok[len(name) + 1:]
    return None


def gh_body(tokens):
    inline = flag_value(tokens, BODY_FLAGS)
    if inline is not None:
        return inline
    path = flag_value(tokens, BODY_FILE_FLAGS)
    if path is not None and path != "-":
        return read_file(path) or ""
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    cmd = data.get("tool_input", {}).get("command", "")
    if not cmd or not GH_BODY_RE.search(cmd):
        return 0

    try:
        tokens = shlex.split(cmd)
    except Exception:
        return 0

    body = gh_body(tokens)
    if body is None or body.strip() == "":
        return 0
    if MARKDOWN_RE.search(body):
        block(
            "gh CLI는 본문 마크다운을 깨뜨립니다 (- → •, 백틱 제거, 체크박스 깨짐). "
            "빈 body로 PR/이슈를 만든 뒤 GitHub API로 PATCH 하세요. "
            "본문 작성·전달 방법은 github-pr-markdown 스킬을 따르세요."
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
