#!/usr/bin/env python3
"""PreToolUse gate for Bash enforcing GitHub-flavored Markdown on gh / API writes.

Strengthened from a soft reminder into a hard gate. Two checks:

  Channel — gh CLI corrupts markdown in every body channel (`- ` -> `•`,
  backticks stripped, `- [ ]` -> `[ ]`), and that happens inside gh after any
  content check, so it can't be validated away. A `gh pr/issue ...` body that
  CONTAINS markdown is therefore blocked: create with an empty body, then PATCH
  via the GitHub API. A plain-text body (nothing for gh to mangle) passes.

  Content — a body sent through the API path (curl / gh api to /pulls or
  /issues) is inspectable, so its markdown is validated: no Unicode bullets,
  checkboxes carry a `- ` prefix, and a PR-resource body has ## Summary +
  ## Test plan.

Fail-open: any parse/IO error or unrecognized shape exits 0 (allow), so it never
wedges unrelated Bash. It blocks (exit 2) only on a positively-identified problem.
"""
import json
import os
import re
import shlex
import sys

UNICODE_BULLETS = "•‣⁃◦∙·"
GH_BODY_RE = re.compile(
    r"\bgh\s+(?:pr\s+(?:create|edit|comment|review)|issue\s+(?:create|edit|comment))\b"
)
API_RESOURCE_RE = re.compile(r"/repos/[^/\s]+/[^/\s]+/(?:pulls|issues)/\d+")
GH_API_RE = re.compile(r"\bgh\s+api\b")
# A PR-resource endpoint (pulls/N, not pulls/N/comments) must carry the PR sections.
# Anchored on repos/.../pulls/N so a `/pulls/N` mention inside a body doesn't count.
PR_RESOURCE_RE = re.compile(r"(?:^|/)repos/[^/\s]+/[^/\s]+/pulls/\d+(?![\d/])")
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


def json_body(raw):
    try:
        obj = json.loads(raw)
    except Exception:
        return None
    if not isinstance(obj, dict):
        return None
    body = obj.get("body")
    return body if isinstance(body, str) else None


def api_body(tokens):
    data = flag_value(tokens, {"-d", "--data", "--data-raw", "--data-binary", "--json"})
    if data is not None:
        raw = read_file(data[1:]) if data.startswith("@") else data
        if raw is not None:
            b = json_body(raw)
            if b is not None:
                return b
    for i, tok in enumerate(tokens):
        kv = matched = None
        for name in ("-f", "--field", "--raw-field", "-F"):
            if tok == name and i + 1 < len(tokens):
                kv, matched = tokens[i + 1], name
            elif tok.startswith(name + "="):
                kv, matched = tok[len(name) + 1:], name
        if kv is not None and kv.startswith("body="):
            val = kv[len("body="):]
            # gh expands @file only for -F/--field; -f/--raw-field sends @… literally.
            if val.startswith("@") and matched in ("-F", "--field"):
                return read_file(val[1:])
            return val
    inp = flag_value(tokens, {"--input"})
    if inp is not None and inp != "-":
        raw = read_file(inp)
        if raw is not None:
            return json_body(raw)
    return None


def validate(body, require_sections):
    problems = []
    if any(ch in body for ch in UNICODE_BULLETS):
        problems.append("유니코드 불릿(• 등) 발견 — ASCII '- '를 쓰세요")
    if re.search(r"(?m)^\s*\[[ xX]\]\s", body):
        problems.append("체크박스에 '- ' 접두가 없습니다 ('- [ ]' 형식이어야 렌더됨)")
    if require_sections:
        if not re.search(r"(?im)^\s*##\s+summary\b", body):
            problems.append("'## Summary' 섹션이 없습니다")
        if not re.search(r"(?im)^\s*##\s+test\s+plan\b", body):
            problems.append("'## Test plan' 섹션이 없습니다")
    return problems


def api_endpoint(tokens):
    # The endpoint is the URL/path token, never a -d/-f payload — so a /pulls/N
    # mention inside a JSON or field body can't be mistaken for a PR resource.
    skip_next = False
    for i, tok in enumerate(tokens):
        if skip_next:
            skip_next = False
            continue
        val = tok
        if tok == "--url" and i + 1 < len(tokens):
            val, skip_next = tokens[i + 1], True
        elif tok.startswith("--url="):
            val = tok[len("--url="):]
        elif tok.startswith("-"):
            continue
        if val.startswith(("http://", "https://", "repos/", "/repos/")):
            return val
    return None


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    if data.get("tool_name") != "Bash":
        return 0
    cmd = data.get("tool_input", {}).get("command", "")
    if not cmd:
        return 0

    is_gh_body = bool(GH_BODY_RE.search(cmd))
    is_api = bool(API_RESOURCE_RE.search(cmd)) or (
        bool(GH_API_RE.search(cmd)) and ("pulls/" in cmd or "issues/" in cmd)
    )
    if not (is_gh_body or is_api):
        return 0

    try:
        tokens = shlex.split(cmd)
    except Exception:
        return 0

    if is_gh_body:
        body = gh_body(tokens)
        if body is None or body.strip() == "":
            return 0
        if MARKDOWN_RE.search(body):
            block(
                "gh CLI는 본문 마크다운을 깨뜨립니다 (- → •, 백틱 제거, 체크박스 깨짐). "
                "마크다운이 든 본문은 빈 body로 만든 뒤 GitHub API로 PATCH 하세요. "
                "본문은 Write 툴로 작성(heredoc 금지) → python json 페이로드 → "
                "curl PATCH /repos/OWNER/REPO/pulls/N. (github-pr-markdown 스킬)"
            )
        return 0

    body = api_body(tokens)
    if not body:
        return 0
    endpoint = api_endpoint(tokens)
    problems = validate(body, require_sections=bool(endpoint) and bool(PR_RESOURCE_RE.search(endpoint)))
    if problems:
        block(
            "PR/이슈 본문 마크다운 위반 — " + "; ".join(problems) + ". "
            "본문을 Write 툴로 다시 작성하세요 (heredoc은 이 셸에서 마크다운을 망가뜨립니다). "
            "(github-pr-markdown 스킬)"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
