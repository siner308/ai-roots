# Codex Overnight

Delegate a long-running implementation task to OpenAI Codex with no approval prompts while keeping the workspace sandbox.

## When To Use

Use when the user wants Codex to keep working unattended, such as overnight implementation, broad test fixing, or multi-step refactoring with a clear verification command.

## Default Mode

```bash
codex exec -m gpt-5.5 -c reasoning_effort="high" --sandbox workspace-write --ask-for-approval never --search -
```

This keeps Codex inside the workspace sandbox but prevents approval prompts from stopping the run. Use `--search` so Codex can research public docs when needed. If the task must install dependencies or call external CLIs from the shell, make that requirement explicit in the brief; do not silently escalate to dangerous mode.

## Required Brief

- Goal and acceptance criteria
- Allowed edit paths
- Out-of-scope paths
- Verification command and expected result
- Whether dependency installation or network-backed commands are allowed
- Checkpoint behavior when blocked
- Final report requirements

## Prompt Tail

```text
Work unattended within the workspace sandbox. Keep changes scoped to the allowed paths. If blocked by sandbox, network, missing credentials, destructive operations, or workspace-external writes, do not work around it unsafely; record the blocker and continue with safe adjacent work. Run the verification command before finishing. Do not commit, push, delete data, alter secrets, or weaken security settings unless explicitly requested. Extra user scope: $ARGUMENTS
```
