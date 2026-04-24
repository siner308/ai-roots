# Background Task Monitoring

When a long-running task sits in the background, the user should never have to ask "is it done?" — but the mechanism for providing that visibility should be **event-driven first, interval-driven only as fallback**. Earlier versions of this lesson recommended `ScheduleWakeup` polling as the default; that was over-fitted to the handful of tasks with no native completion signal.

## The Decision Ladder

Pick the cheapest mechanism that actually fits the task. Going down the ladder means more tokens, more latency, and more rituals — only pay the cost when the rung above cannot answer the question.

### Rung 1 — Completion notification only (default)

If the only thing the user needs is "tell me when it's done with the result," don't monitor at all. The harness already notifies when a `run_in_background: true` Bash completes. Kick off the task, continue with other work, and react to the completion event when it fires.

```
Bash(command: "...", run_in_background: true)
→ continue with unrelated work
→ completion notification arrives → Read output → report result
```

Applies to: Codex reviews, single-shot builds, test suites, one-off migrations, any task whose value is in the final result, not the journey.

### Rung 2 — Streamed events (when progress matters)

If the user benefits from seeing progress as it happens — phases completing, records processed, errors emerging — use the `Monitor` tool to subscribe to stdout lines. Each line becomes a notification, so updates are real (not polled) and the cadence matches the task's actual pace.

```
Bash(run_in_background: true, command: "... 2>&1 | tee /tmp/task.log")
Monitor(path: "/tmp/task.log") → each line is an event
→ summarize meaningful phases as they arrive
→ completion event stops the subscription
```

Applies to: data pipelines with phase boundaries, long seed scripts, crawlers, anything where mid-run phase boundaries carry information the user wants.

### Rung 3 — Interval polling (fallback only)

`ScheduleWakeup` (or `/loop`) at 1–2 minute intervals is the right choice **only** when all of these hold:

- The task has no clean completion signal (external system, log file that never terminates, polling-only API)
- Progress is meaningful to the user but the task does not emit discrete events `Monitor` can key on
- The briefing cost per tick is low enough to be worth it

When you reach for `ScheduleWakeup` by default, you are paying polling cost for a question the harness would have answered for free. Audit: would Rung 1 or Rung 2 cover this?

Applies to: external async jobs you can only probe (cloud builds, remote workflows, third-party queues), subagent work where you must interleave status into the main conversation, progress dashboards the user watches live with you.

## Anti-patterns

- **Polling for the result.** If you only want the final output, trust the completion notification. `ScheduleWakeup` for a 3-minute task that will notify when done is pure overhead.
- **Foreground with long timeout to "keep it simple,"** then the conversation is blocked and the user can't interrupt or ask follow-ups. Foreground is fine for sub-minute tasks whose result is the only next step; past that, prefer Rung 1.
- **Monitor subscription with no structure.** Dumping every stdout line back to the user reproduces the raw log. `Monitor` pays off only if you summarize phase transitions, not if you echo lines.
- **Interval polling a task that streams.** If the task writes to a file you could tail, use Rung 2 — polling a tail every 2 minutes discards the low-latency information the stream already provides.

## User-visible Streaming (Separate Concern)

"I want to watch the output live" is a different requirement from "don't make me ask if it's done." Harness-side monitoring (ladder above) keeps Claude informed; user-side streaming gives the user their own view. Split the stream with `tee`:

```bash
command ... 2>&1 | tee /tmp/task-$$.log
```

Then either: let the user `tail -f` that path in their own terminal, launch a tmux split-pane on it, or spawn a separate Terminal window. Choice depends on their harness environment; the stream-splitting convention is what makes any of them work.

## Why

The original anti-pattern ("user keeps asking if it's done") is real, but the cure was mis-specified. The underlying principle is **the user should have visibility proportional to the value of seeing progress**. Interval polling enforces visibility at a fixed cost regardless of value; event-driven mechanisms match cost to real information arrivals.

A 5-minute Codex review gains nothing from minute-by-minute polling — the result IS the progress. A 45-minute seed pipeline with 12 phases gains a lot from phase-boundary notifications, but `Monitor` provides that at zero polling cost.

## When to Apply

- Any `run_in_background: true` task expected to outlive a single turn
- Codex delegations (`/codex:overnight`, `/codex:autopilot`) — usually Rung 1
- Data pipelines, migrations, crawlers with observable phases — usually Rung 2
- External async jobs without completion hooks — Rung 3

## Rule Summary

- Default to Rung 1 (completion notification only). Polling is not the default anymore.
- Escalate to Rung 2 when phase-level progress has real user value.
- Reach for Rung 3 only when no native completion or stream signal exists.
- User-visible live streaming is a `tee` problem, not a monitoring problem — don't conflate them.
