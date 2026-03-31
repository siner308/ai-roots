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

### Pre-submit Verification

After `gh pr create`, run `gh pr view <number> --json body` and verify:
1. `- ` bullets are intact (not converted to `•`)
2. `- [ ]` checkboxes are intact (not bare `[ ]`)
3. Backticks are present around code references
4. URLs are wrapped as `[text](url)`

If any check fails, immediately fix with `gh pr edit <number> --body`.
