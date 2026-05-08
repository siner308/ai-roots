# Codex Diff Review

Run a general production-code review with OpenAI Codex as an independent reviewer. See `claude-rules/codex/codex-delegation.md` for routing context.

```bash
codex review -m gpt-5.5 -c model_reasoning_effort=xhigh --uncommitted "Review this diff as a production code reviewer. Prioritize correctness bugs, regressions, missing tests, security issues, and maintainability risks. Return findings first, ordered by severity, with exact file/line references. Avoid broad summaries unless there are no findings. Extra scope: $ARGUMENTS"
```

If there are no uncommitted changes and `$ARGUMENTS` names a base branch or commit, use `codex review --base <branch>` or `codex review --commit <sha>`. Read-only — do not ask Codex to edit files here.
