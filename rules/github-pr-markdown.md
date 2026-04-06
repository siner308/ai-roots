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

`gh pr create --body` and shell string interpolation corrupt markdown: dashes become `•`, backticks are stripped, indentation is added. **Always write body to a file first, then use `--body-file`.**

Safe method — single-quoted heredoc to file, then `--body-file`:

```bash
# 1. Write body to file (single-quoted heredoc preserves all characters literally)
cat <<'EOF' > /tmp/pr-body.md
## Summary

- First bullet with `code ref`

## Test plan

- [ ] Verification item
EOF

# 2. Create or edit PR with --body-file
gh pr create --title "the pr title" --body-file /tmp/pr-body.md
gh pr edit NUMBER --body-file /tmp/pr-body.md
```

**Do NOT** encode non-ASCII characters as Python byte escapes (e.g. `\xec\x97\x90`). Write Unicode text directly — both heredocs and Python preserve UTF-8 as-is.

### Pre-submit Verification

After `gh pr create`, verify the body renders correctly on the PR page. If corruption is found, rewrite `/tmp/pr-body.md` and run `gh pr edit NUMBER --body-file /tmp/pr-body.md`.
