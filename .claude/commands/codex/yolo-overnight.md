# Codex YOLO Overnight

Run Codex with no sandbox and no approval prompts.

## Risk Boundary

This command uses dangerous full access:

```bash
codex exec -m gpt-5.5 -c reasoning_effort="extra-high" --dangerously-bypass-approvals-and-sandbox --search -
```

Use only when the user explicitly accepts the risk for the current repository. This mode can read and write outside the workspace, run destructive commands, access local credentials available to the process, and use the network without approval prompts.

## Preflight

Before running, state the risk in one sentence and confirm that the user requested YOLO/no-sandbox behavior for this task. Do not infer consent from a generic request for "autopilot" or "overnight".

## Prompt Tail

```text
The user explicitly requested no-sandbox/no-approval YOLO mode. Still act conservatively: keep edits scoped to the task, avoid destructive operations unless necessary and reversible, do not commit or push unless explicitly requested, and report all commands that materially changed state. Use network/search when useful. Extra user scope: $ARGUMENTS
```
