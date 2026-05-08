# Codex Autopilot

Bounded implementation handoff using `codex exec --full-auto` (workspace-write, ask-for-approval on-request). Use when Codex should read, edit within the workspace, and run verification without repeated prompts. See `claude-rules/codex/codex-delegation.md` for mode boundaries.

```bash
codex exec --full-auto -m gpt-5.5 -c model_reasoning_effort=xhigh -
```

Stdin brief:

- Task goal and non-goals
- Files or directories Codex may edit
- Verification command
- Constraints to preserve
- Instruction not to commit, push, delete data, or change secrets unless explicitly requested
- Expected final report: changed files, verification result, unresolved risks

Append:

```text
Operate as a bounded implementation worker. Stay within the requested scope. Prefer small verifiable edits. Run the specified verification command before finishing. Do not commit, push, delete data, alter credentials, or weaken sandbox/security settings unless the user explicitly asked for that exact action. Extra user scope: $ARGUMENTS
```

Do not use `--dangerously-bypass-approvals-and-sandbox` from this command. For unattended runs use `/codex:overnight`; for explicit no-sandbox consent use `/codex:yolo-overnight`.
