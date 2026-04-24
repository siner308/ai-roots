# Codex Adversarial Review

Run an independent OpenAI Codex review for security-sensitive changes.

## When To Use

Use after behavioral changes touching authentication, authorization, database writes, network boundaries, secret handling, user-input parsing, deserialization, command execution, or file paths.

## Protocol

1. Verify `codex` is available with `command -v codex`.
2. Verify there are reviewable changes with `git diff --quiet`, `git diff --cached --quiet`, and `git ls-files --others --exclude-standard`.
3. Run Codex against all uncommitted changes:

```bash
cat "$HOME/.claude/agents/adversarial-reviewer.md" | codex review -m gpt-5.5 -c reasoning_effort="extra-high" --uncommitted -
```

4. Treat Codex output as independent evidence. If it disagrees with Claude's conclusion, investigate the disagreement before deciding.
5. Do not auto-apply fixes from Codex in this command. Report findings first, then let the main Claude session decide what to change.

## Extra Scope

If the user supplied arguments, append them to the reviewer prompt before invoking Codex:

```text
Additional user scope:
$ARGUMENTS
```
