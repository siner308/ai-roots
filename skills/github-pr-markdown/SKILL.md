---
name: github-pr-markdown
description: "Apply when creating or editing a pull request body or title (gh pr create, gh pr edit, gh api PR updates) or composing any PR description, including when another skill or workflow produces one. Enforces GitHub-flavored Markdown: ASCII dash bullets, task-list checkboxes, backtick code refs, mandatory Summary/Test plan sections, and the safe API-PATCH body delivery that avoids gh CLI markdown corruption. Also adds a one-line TL;DR lead, problem→cause→solution ordering in the Summary, and an optional References section whose every link is opened and verified before inclusion."
---

# GitHub PR Markdown Convention

CRITICAL: When creating or editing PRs (gh pr create, gh pr edit, PR body composition), you MUST produce valid GitHub-flavored Markdown. Malformed markdown (broken checkboxes, stripped backticks, bare URLs) is a blocking defect — fix before submitting.

## Rules

### Structure

- PR title under 70 characters. Use the body for details
- Use `##` for sections (the PR title is H1, so never use `#` in the body)
- One blank line between sections

### Formatting — STRICT

- Bullet points: ALWAYS use `- ` (ASCII dash + space). NEVER use •, ·, * or other Unicode bullets
- Task lists: ALWAYS use `- [ ]` / `- [x]` (dash + space + bracket). Bare `[ ]` without a `- ` prefix will NOT render as checkboxes
- Code references: ALWAYS wrap in backticks (`componentName`, `fileName.ts`). Backticks must survive shell escaping — verify in the final output
- Do not use raw HTML when Markdown suffices
- Use GFM table syntax (pipes + alignment) for tables

### Links and References — STRICT

- Reference issues/PRs as `owner/repo#123` or `#123`
- URLs: ALWAYS use `[text](url)` format. Bare URLs are forbidden
- Images use `![alt text](url)` with descriptive alt text

### Required PR Body Sections

```markdown
> **TL;DR** — one sentence: the problem and the outcome.

## Summary
- **Problem:** what was wrong, or why this change is needed
- **Cause:** the underlying reason (bugfix), or the motivation (feature/refactor)
- **Fix:** what this change does

## References
- [Title of the spec or doc](url) — what it backs up

## Test plan
- [ ] Verification item 1
- [ ] Verification item 2
```

- `## Summary` and `## Test plan` are mandatory
- If the repo has a PR template (`.github/pull_request_template.md` or `.github/PULL_REQUEST_TEMPLATE/`), include its required sections too — the TL;DR, problem→cause→fix ordering, and verified References still apply within them
- Lead with a one-line TL;DR (blockquote) above Summary when the body is non-trivial (Summary has 3+ bullets, or there are extra sections). A short 2-bullet PR may skip it — the Summary already is the gist
- Open with context, then mechanism. Bugfix: problem → cause → fix. Feature/refactor: motivation → what changed → why this approach. Never lead with the cause or the fix before the reader knows the problem
- `## References` is optional — include it when the change relies on documented external behavior (a system's documented behavior, a library API spec, an RFC, an internal design doc). One link can sit inline in its bullet; collect several under `## References`
- Before adding any reference link, OPEN it and confirm two things: it is reachable, AND the page actually contains the behavior you cite. Never include an unverified or guessed URL
- Additional sections like `## Breaking changes` or `## Notes` may be added as needed

### Body Delivery — STRICT

gh CLI corrupts markdown in ALL body delivery methods (`--body`, `--body-file`, `gh pr edit --body-file`): dashes become •, backticks are stripped, `- [ ]` becomes `[ ]`. **Never pass the PR body through the gh CLI. Always use the GitHub API directly.**

Safe method — create the PR with an empty body, then PATCH via API:

```bash
# 1. Create PR with empty body
gh pr create --title "the pr title" --body "" --draft

# 2. Write body payload with Python (preserves exact bytes)
python3 -c "
import json
body = '''## Summary

- First bullet with \x60code ref\x60

## Test plan

- [ ] Verification item
'''
with open('/tmp/pr-payload.json', 'w', encoding='utf-8') as f:
    json.dump({'body': body}, f, ensure_ascii=False)
"

# 3. PATCH via GitHub API
curl -s -X PATCH \
  -H "Authorization: token $(gh auth token)" \
  -H "Content-Type: application/json; charset=utf-8" \
  -d @/tmp/pr-payload.json \
  https://api.github.com/repos/OWNER/REPO/pulls/NUMBER
```

For edits, reuse steps 2-3 with the updated body.

Notes:

- In Python strings, use `\x60` for backticks to avoid shell interpretation
- **Do NOT** encode non-ASCII characters as byte escapes (e.g. `\xec\x97\x90`). Write Unicode text directly

### Pre-submit Verification

After creating/editing a PR, verify the raw body via API:

```bash
gh pr view NUMBER --json body --jq .body | head -10
```

Check:

1. `- ` bullets are ASCII dash (not •)
2. `- [ ]` checkboxes have a `- ` prefix
3. Backticks `` ` `` are present around code references

If any check fails, rewrite the payload and PATCH via API as shown above.
