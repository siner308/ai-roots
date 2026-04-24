# Codex Diff Review

Run a general production-code review with OpenAI Codex as an independent reviewer.

## Protocol

1. Verify `codex` is available with `command -v codex`.
2. Review all uncommitted changes:

```bash
codex review -m gpt-5.5 -c model_reasoning_effort=xhigh --uncommitted "Review this diff as a production code reviewer. Prioritize correctness bugs, regressions, missing tests, security issues, and maintainability risks. Return findings first, ordered by severity, with exact file/line references. Avoid broad summaries unless there are no findings. Extra scope: $ARGUMENTS"
```

3. If there are no uncommitted changes and the user named a base branch or commit in `$ARGUMENTS`, use the matching `codex review --base <branch>` or `codex review --commit <sha>` form.
4. Keep this command read-only. Do not ask Codex to edit files here.
