# Background Task Monitoring

When running a long background task, set up automatic periodic monitoring so the user doesn't have to ask for progress.

## Pattern

1. **Start the task with `run_in_background: true`.** This keeps the conversation unblocked.
2. **Immediately schedule a monitoring loop.** Use `ScheduleWakeup` (or `/loop`) at 1-2 minute intervals to `tail` the output file and report progress.
3. **Report concisely each tick.** Show which phase completed, what's in progress, and how many remain. One table or 2-3 lines max.
4. **End the loop on completion.** When the output shows the final summary or the background task notification arrives, stop scheduling and report the final result.

## Why

`run_in_background` produces no visible output. Without automatic monitoring, the user must repeatedly ask "how's it going?" — this is friction that should never exist. The user told you to run it; they expect you to track it.

Conversely, running long tasks in foreground (timeout 600000) blocks the entire conversation. The user can't do anything else.

## Example

Bad: Run seed script in background → user waits → user asks "is it done?" → check tail → repeat 5 times

Good:
```
Step 1: Bash(run_in_background: true) — start the long task
Step 2: ScheduleWakeup(120s) — "monitoring background task progress"
Step 3: Each wakeup → tail -10 output file → report progress → schedule next
Step 4: Task completes → report final result → stop loop
```

## When to Apply

- Any `run_in_background` task expected to take more than 2 minutes
- Build processes, test suites, data pipelines, migrations
- Any operation where the user would otherwise have no visibility into progress
