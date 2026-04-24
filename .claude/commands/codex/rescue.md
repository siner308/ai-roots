# Codex Rescue

Delegate a stuck debugging or implementation problem to OpenAI Codex after Claude has exhausted three substantive attempts.

## Required Brief

Before invoking Codex, prepare a concise rescue brief containing:

- Original task description
- Current repository path
- Exact command or test that reproduces the failure
- The three hypotheses already attempted
- Why each hypothesis failed
- Files, functions, or layers already ruled out
- Constraints Codex must preserve

## Protocol

1. Verify `codex` is available with `command -v codex`.
2. Run Codex in read-only mode unless the user explicitly asked for Codex to patch files:

```bash
codex exec -m gpt-5.5 -c reasoning_effort="high" --sandbox read-only -
```

3. Paste the rescue brief into stdin, followed by:

```text
You are an independent rescue debugger. Do not repeat the ruled-out hypotheses. Find a fresh explanation or a minimal next experiment. Return concise findings with file paths, commands, and the smallest verification step. Extra user scope: $ARGUMENTS
```

4. Claude remains responsible for deciding which Codex findings to apply.
