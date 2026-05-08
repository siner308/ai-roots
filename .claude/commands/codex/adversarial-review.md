# Codex Adversarial Review

Independent OpenAI Codex review for security-sensitive changes (auth, database writes, network boundaries, secrets, deserialization, command execution, file paths). See `claude-rules/codex/codex-delegation.md` for trigger criteria.

```bash
cat "$HOME/.claude/agents/adversarial-reviewer.md" | codex review -m gpt-5.5 -c model_reasoning_effort=xhigh --uncommitted -
```

Treat Codex output as independent evidence. Do not auto-apply fixes from this command — report findings, then let the main session decide.

If `$ARGUMENTS` is non-empty, append to the reviewer prompt:

```text
Additional user scope:
$ARGUMENTS
```
