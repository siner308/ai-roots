# Codex Overnight

Unattended implementation with no approval prompts but workspace sandbox preserved. Use for "work while I sleep" requests with clear acceptance criteria and verification. See `claude-rules/codex/codex-delegation.md` for mode boundaries.

```bash
codex --search -a never exec --sandbox workspace-write -m gpt-5.5 -c model_reasoning_effort=xhigh -
```

If the task must install dependencies or call external CLIs, name that requirement explicitly in the brief — do not silently escalate to dangerous mode.

Stdin brief:

- Goal and acceptance criteria
- Allowed edit paths
- Out-of-scope paths
- Verification command and expected result
- Whether dependency installation or network-backed commands are allowed
- Checkpoint behavior when blocked
- Final report requirements

Append:

```text
Work unattended within the workspace sandbox. Keep changes scoped to the allowed paths. If blocked by sandbox, network, missing credentials, destructive operations, or workspace-external writes, do not work around it unsafely; record the blocker and continue with safe adjacent work. Run the verification command before finishing. Do not commit, push, delete data, alter secrets, or weaken security settings unless explicitly requested. Extra user scope: $ARGUMENTS
```
