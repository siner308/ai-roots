---
name: github-pr-markdown
description: "Apply when creating or editing a pull request body or title (gh pr create, gh pr edit, gh api PR updates) or composing any PR description, including when another skill or workflow produces one. The body is capped at three lines — a hard ceiling, not a default — with the repo's PR template as the only exception. Enforces GitHub-flavored Markdown: ASCII dash bullets, task-list checkboxes, backtick code refs, and the safe API-PATCH body delivery that avoids gh CLI markdown corruption."
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

### Body length — HARD CAP

The PR body is at most **three lines**. This is a ceiling, not a default — a big diff does not buy a longer body. Long generated bodies read as machine output and reviewers skip them; three lines that say what changed and why get read.

- No `## Summary`, `## Test plan`, `## References`, TL;DR, or any other ceremony section. Deeper context belongs in commit messages or review comments, not the body.
- A line may be a sentence, a `- ` bullet, or a verified `[text](url)` link — but three lines total. Never include a guessed URL; open any link and confirm it contains what you cite before adding it.
- Open with the problem or motivation, then the change. Never lead with the fix before the reader knows the problem.

**Only exception — the repo's PR template** (`.github/pull_request_template.md` or `.github/PULL_REQUEST_TEMPLATE/`): the template's structure wins, but the cap moves inside it — at most three lines per section you fill. Omit sections that don't apply rather than writing "N/A" filler, and never add sections the template doesn't define. The formatting rules (ASCII bullets, backtick code refs, API delivery) still apply inside it.

### Body Delivery — STRICT

gh CLI corrupts markdown in ALL body delivery methods (`--body`, `--body-file`, `gh pr edit --body-file`): dashes become •, backticks are stripped, `- [ ]` becomes `[ ]`. **Never pass the PR body through the gh CLI. Always use the GitHub API directly.**

Safe method — create the PR with an empty body, then PATCH via API:

```bash
# 1. Create PR with empty body
gh pr create --title "the pr title" --body "" --draft

# 2. Write body payload with Python (preserves exact bytes)
python3 -c "
import json
body = '''Show codex token usage on API-key auth, where \x60rate_limits\x60 is null so the quota line stayed blank.

- [ ] Statusline renders token counts in apikey mode
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
