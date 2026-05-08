# Codex YOLO Overnight

Codex with no sandbox and no approval prompts. **Dangerous full access** — can read/write outside workspace, run destructive commands, access local credentials, use network without approval. See `claude-rules/codex/codex-delegation.md` for mode boundaries.

```bash
codex --search --dangerously-bypass-approvals-and-sandbox exec -m gpt-5.5 -c model_reasoning_effort=xhigh -
```

## Preflight (mandatory)

Before running, state the risk in one sentence and confirm the user **explicitly** requested YOLO/no-sandbox behavior for this task. Do not infer consent from a generic "autopilot" or "overnight" request — those have their own commands.

Append:

```text
The user explicitly requested no-sandbox/no-approval YOLO mode. Still act conservatively: keep edits scoped to the task, avoid destructive operations unless necessary and reversible, do not commit or push unless explicitly requested, and report all commands that materially changed state. Use network/search when useful. Extra user scope: $ARGUMENTS
```
