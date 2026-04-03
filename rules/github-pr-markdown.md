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

Shell heredocs (`cat <<'EOF'`) and `gh pr create --body` corrupt markdown: dashes become `•`, backticks are stripped, indentation is added. **Never pass PR body through shell string interpolation.**

Safe method — write body to file with Python, then use `--body-file`:

```bash
# 1. Write body to file (Python preserves exact bytes)
python3 -c "
body = '''## Summary

- First bullet
- Second with \x60code ref\x60

## Test plan

- [ ] Verification item
'''
with open('/tmp/pr-body.md', 'w') as f:
    f.write(body)
"

# 2. Create PR with --body-file
gh pr create --title "the pr title" --body-file /tmp/pr-body.md
```

For edits, use the GitHub API directly (gh pr edit also corrupts):

```bash
python3 -c "
import json
body = open('/tmp/pr-body.md').read()
with open('/tmp/pr-payload.json', 'w') as f:
    json.dump({'body': body}, f)
"
curl -s -X PATCH \
  -H "Authorization: token $(gh auth token)" \
  -H "Content-Type: application/json" \
  -d @/tmp/pr-payload.json \
  https://api.github.com/repos/OWNER/REPO/pulls/NUMBER
```

Note: In Python strings, use `\x60` for backticks to avoid shell interpretation.

### Pre-submit Verification

After `gh pr create`, verify the raw body via API:

```bash
curl -s -H "Authorization: token $(gh auth token)" \
  https://api.github.com/repos/OWNER/REPO/pulls/NUMBER \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['body'][:300])"
```

Check:
1. `- ` bullets are ASCII dash `0x2d` (not `•` = `0xe2 0x80 0xa2`)
2. `- [ ]` checkboxes have `- ` prefix
3. Backticks `` ` `` are present around code references
4. URLs are wrapped as `[text](url)`

If any check fails, rewrite the body file and PATCH via API as shown above.
