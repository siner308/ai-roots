# Codex Autopilot

Delegate implementation work to OpenAI Codex with bounded autonomy.

## Default Mode

Use `--full-auto` for trusted local repositories when Codex should read files, edit within the workspace, and run verification commands without repeated prompts:

```bash
codex exec --full-auto -
```

Paste a brief with:

- Task goal and non-goals
- Files or directories Codex may edit
- Verification command
- Constraints to preserve
- Instruction not to commit, push, delete data, or change secrets unless explicitly requested
- Expected final report: changed files, verification result, unresolved risks

## Dangerous Mode

Do not use `--dangerously-bypass-approvals-and-sandbox` by default.

Only use it when all are true:

- The user explicitly requests dangerous/no-approval mode
- The repository is trusted
- An outer isolation boundary exists, such as a disposable devcontainer, VM, or other sandbox
- Network and secrets exposure have been considered

If any condition is missing, use `--full-auto` or `--sandbox read-only --ask-for-approval never` instead.

## Prompt Tail

Append this to the Codex prompt:

```text
Operate as a bounded implementation worker. Stay within the requested scope. Prefer small verifiable edits. Run the specified verification command before finishing. Do not commit, push, delete data, alter credentials, or weaken sandbox/security settings unless the user explicitly asked for that exact action. Extra user scope: $ARGUMENTS
```
