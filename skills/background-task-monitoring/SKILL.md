---
name: background-task-monitoring
description: "Apply when a long-running task runs in the background and the user needs visibility into its completion or progress — choosing between completion-notification-only (default), streamed events via Monitor, and interval polling via ScheduleWakeup. Also apply when tempted to monitor a subprocess via tmux split panes, sentinel strings, or a foreground tail/grep loop — that pattern failed and its post-mortem lives here. Covers the decision ladder, anti-patterns, and tee-based user-visible streaming."
---

# Background Task Monitoring

When a long-running task sits in the background, the user should never have to ask "is it done?" — but the mechanism for providing that visibility should be **event-driven first, interval-driven only as fallback**. Earlier versions of this lesson recommended ScheduleWakeup polling as the default; that was over-fitted to the handful of tasks with no native completion signal.

## The Decision Ladder

Pick the cheapest mechanism that actually fits the task. Going down the ladder means more tokens, more latency, and more rituals — only pay the cost when the rung above cannot answer the question.

### Rung 1 — Completion notification only (default)

If the only thing the user needs is "tell me when it's done with the result," don't monitor at all. The harness already notifies when a `run_in_background: true` Bash completes. Kick off the task, continue with other work, and react to the completion event when it fires.

```
Bash(command: "...", run_in_background: true)
→ continue with unrelated work
→ completion notification arrives → Read output → report result
```

Applies to: single-shot builds, test suites, one-off migrations, any task whose value is in the final result, not the journey.

### Rung 2 — Streamed events (when progress matters)

If the user benefits from seeing progress as it happens — phases completing, records processed, errors emerging — use the Monitor tool to subscribe to stdout lines. Each line becomes a notification, so updates are real (not polled) and the cadence matches the task's actual pace.

```
Bash(run_in_background: true, command: "... 2>&1 | tee /tmp/task.log")
Monitor(path: "/tmp/task.log") → each line is an event
→ summarize meaningful phases as they arrive
→ completion event stops the subscription
```

Applies to: codex `--json` reviews (the `/review` skill — the event stream shows which files codex is inspecting and its reasoning live), data pipelines with phase boundaries, long seed scripts, crawlers, anything where mid-run phase boundaries carry information the user wants.

### Rung 3 — Interval polling (fallback only)

ScheduleWakeup (or /loop) at 1–2 minute intervals is the right choice **only** when all of these hold:

- The task has no clean completion signal (external system, log file that never terminates, polling-only API)
- Progress is meaningful to the user but the task does not emit discrete events Monitor can key on
- The briefing cost per tick is low enough to be worth it

When you reach for ScheduleWakeup by default, you are paying polling cost for a question the harness would have answered for free. Audit: would Rung 1 or Rung 2 cover this?

Applies to: external async jobs you can only probe (cloud builds, remote workflows, third-party queues), subagent work where you must interleave status into the main conversation, progress dashboards the user watches live with you.

## Anti-patterns

- **Polling for the result.** If you only want the final output, trust the completion notification. ScheduleWakeup for a 3-minute task that will notify when done is pure overhead.
- **Foreground with long timeout to "keep it simple,"** then the conversation is blocked and the user can't interrupt or ask follow-ups. Foreground is fine for sub-minute tasks whose result is the only next step; past that, prefer Rung 1.
- **Monitor subscription with no structure.** Dumping every stdout line back to the user reproduces the raw log. Monitor pays off only if you summarize phase transitions, not if you echo lines.
- **Interval polling a task that streams.** If the task writes to a file you could tail, use Rung 2 — polling a tail every 2 minutes discards the low-latency information the stream already provides.
- **tmux split panes, sentinel strings, or a foreground tail/grep loop.** This pattern was tried and failed reliably — see the lesson below.

## Lesson — the tmux sentinel wrapper failed

A previous version of the delegation rules told Claude to run every long codex command inside a tmux split pane, print a `=== DONE ===` sentinel at the end, and wake the main session with a foreground `tail -f "$LOG" | grep -qm1 'DONE'`. The pattern looked rigorous on paper. In practice both halves of the contract broke: the pane stayed open (manual close required), and Claude never noticed completion — the user had to type "it's done" to advance the turn, even though the sentinel had landed in the log.

Why the wake-up failed: Claude's main turn only advances on (a) user input, or (b) completion of a `run_in_background: true` Bash. The `tail -f | grep` ran in foreground — at which point the main session was blocked, and even when the sentinel arrived there was no event the harness translated into "Claude's turn is up."

The deeper flaw: the design conflated two independent goals into one mechanism — (1) wake Claude when the subprocess exits, (2) show the subprocess's output live to the user. Goal 1 is solved natively by `run_in_background: true` Bash (the harness fires a completion notification). Goal 2 is solved by tee-ing to a log and letting the user run their own `tail -f`. Forcing both through a tmux + sentinel + grep wrapper added new failure modes (sentinel race with tee flush, foreground-vs-background ambiguity, manual pane close) without making either goal more reliable.

The standing rules from that post-mortem:

- Do not script tmux split panes from Claude's side to deliver subprocess output to the user. The user's own terminal already runs tmux; Claude does not need to drive it.
- Do not write sentinel strings whose only consumer is a Claude-side grep waiting on them. The completion of the background Bash is itself the deterministic signal.
- When two goals (wake Claude / show output to the user) tempt you toward one mechanism, decompose them. The simpler pair beats the unified wrapper.

## User-visible Streaming (Separate Concern)

"I want to watch the output live" is a different requirement from "don't make me ask if it's done." Harness-side monitoring (ladder above) keeps Claude informed; user-side streaming gives the user their own view. Split the stream with tee:

```
command ... 2>&1 | tee /tmp/task-$$.log
```

Then let the user `tail -f` that path in their own terminal. The stream-splitting convention is what makes it work; Claude does not script the live view.

## Why

The original anti-pattern ("user keeps asking if it's done") is real, but the cure was mis-specified. The underlying principle is **the user should have visibility proportional to the value of seeing progress**. Interval polling enforces visibility at a fixed cost regardless of value; event-driven mechanisms match cost to real information arrivals.

A 5-minute Codex review should not be interval-polled (Rung 3); with `--json` it streams events, so the live log IS the progress — Rung 2 surfaces it at zero polling cost. A 45-minute seed pipeline with 12 phases gains a lot from phase-boundary notifications, and Monitor provides that at zero polling cost too.

## When to Apply

- Any `run_in_background: true` task expected to outlive a single turn
- Codex delegations (long-running codex exec, /review) — usually Rung 2 (`--json` event stream)
- Data pipelines, migrations, crawlers with observable phases — usually Rung 2
- External async jobs without completion hooks — Rung 3

## Rule Summary

- Default to Rung 1 (completion notification only). Polling is not the default anymore.
- Escalate to Rung 2 when phase-level progress has real user value.
- Reach for Rung 3 only when no native completion or stream signal exists.
- User-visible live streaming is a tee problem, not a monitoring problem — don't conflate them.
- Never rebuild the tmux/sentinel/foreground-grep wrapper; the background-Bash completion notification is the wake signal.
