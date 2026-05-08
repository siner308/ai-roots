# Codex Rescue

Delegate a stuck problem to Codex after three substantive attempts. See `claude-rules/codex/codex-delegation.md` §Three-Turn Rescue Protocol for when this fires.

```bash
codex exec --sandbox read-only -m gpt-5.5 -c model_reasoning_effort=xhigh -
```

Stdin rescue brief:

- Original task description
- Repository path
- Exact command or test that reproduces the failure
- The three hypotheses already attempted, and why each failed
- Files/functions/layers already ruled out
- Constraints Codex must preserve

Append:

```text
You are an independent rescue debugger. Do not repeat the ruled-out hypotheses. Find a fresh explanation or a minimal next experiment. Return concise findings with file paths, commands, and the smallest verification step. Extra user scope: $ARGUMENTS
```

Read-only by default. If the user explicitly asks Codex to patch files, switch to `--full-auto` per `codex-delegation.md`. Claude remains responsible for which findings to apply.
