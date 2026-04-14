# GitHub PR Markdown Convention

CRITICAL: When creating or editing PRs (`gh pr create`, `gh pr edit`, PR body composition), you MUST produce valid GitHub-flavored Markdown. Malformed markdown (broken checkboxes, stripped backticks, bare URLs) is a blocking defect — fix before submitting.

## Rules

### Structure
- PR title under 70 characters. Use the body for details
- Use `##` for sections (the PR title is H1, so never use `#` in the body)
- One blank line between sections

### Formatting — STRICT
- Bullet points: ALWAYS use `- ` (ASCII dash + space). NEVER use `•`, `·`, `*` or other Unicode bullets
- Task lists: ALWAYS use `- [ ]` / `- [x]` (dash + space + bracket). Bare `[ ]` without `- ` prefix will NOT render as checkboxes
- Code references: ALWAYS wrap in backticks (`` `componentName` ``, `` `fileName.ts` ``). Backticks must survive shell escaping — verify in the final output
- Do not use raw HTML when Markdown suffices
- Use GFM table syntax (pipes + alignment) for tables

### Links and References — STRICT
- Reference issues/PRs as `owner/repo#123` or `#123`
- URLs: ALWAYS use `[text](url)` format. Bare URLs are forbidden
- Images use `![alt text](url)` with descriptive alt text

### Required PR Body Sections
```markdown
## Summary
- bullet point 1
- bullet point 2

## Test plan
- [ ] Verification item 1
- [ ] Verification item 2
```

- `## Summary` and `## Test plan` sections are mandatory
- Additional sections like `## Breaking changes` or `## Notes` may be added as needed

### Body Delivery — STRICT

`gh` CLI corrupts markdown in ALL body delivery methods (`--body`, `--body-file`, `gh pr edit --body-file`): dashes become `•`, backticks are stripped, `- [ ]` becomes `[ ]`. **Never pass PR body through `gh` CLI. Always use the GitHub API directly.**

Safe method — create PR with empty body, then PATCH via API:

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
1. `- ` bullets are ASCII dash (not `•`)
2. `- [ ]` checkboxes have `- ` prefix
3. Backticks `` ` `` are present around code references

If any check fails, rewrite the payload and PATCH via API as shown above.
