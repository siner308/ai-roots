---
name: github-pr-markdown
description: "Apply when creating or editing a pull request body or title (gh pr create, gh pr edit, gh api PR updates) or composing any PR description, including when another skill or workflow produces one. Keep bodies short — three lines or fewer by default, scaled to the change — and follow the repo's PR template when one exists. Enforces GitHub-flavored Markdown: ASCII dash bullets, task-list checkboxes, backtick code refs, and the safe API-PATCH body delivery that avoids gh CLI markdown corruption. For non-trivial changes adds a Summary (problem→cause→fix), a Test plan, and a References section whose every link is opened and verified before inclusion."
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

### Body length and structure

Keep PR bodies short. Aim for three lines or fewer by default — match the body to the size of the change, and never pad it with ceremony sections that add nothing. Most PRs are small and need only a sentence or two on what changed and why.

**Follow the repo's PR template if one exists** (`.github/pull_request_template.md` or `.github/PULL_REQUEST_TEMPLATE/`). Read it, fill the sections it defines in its order, and omit sections that don't apply rather than writing "N/A" filler. The template's structure replaces the default below; the formatting rules (ASCII bullets, backtick code refs, verified links, API delivery) still apply inside it.

**With no template, scale the body to the change:**

- **Small / self-explanatory** — one to three lines: what changed and why. No headings, no checkboxes.
- **Non-trivial** (several files, a behavior change, needs review context) — add `## Summary` (problem → cause → fix) and a `## Test plan` checklist. Add a one-line `> **TL;DR**` lead only when the body is long enough that the reader needs the gist first.
- `## References` — optional, only when the change relies on documented external behavior (a system's documented behavior, a library API spec, an RFC, an internal design doc). Before adding any link, OPEN it and confirm it is reachable AND actually contains the behavior you cite. Never include a guessed URL. Additional sections like `## Breaking changes` may be added when they carry real content.

Whatever the length, open with context before mechanism: problem before cause/fix, motivation before what changed. Never lead with the fix before the reader knows the problem.

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
