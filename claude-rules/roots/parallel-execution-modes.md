# Parallel Execution Modes

When work can be parallelized, there are three distinct strategies. Choose based on whether workers need to communicate and how independent the tasks are.

## The Three Modes

| Mode | When to use | Token cost | Cross-worker communication |
|------|-------------|------------|---------------------------|
| **Sequential** | Tasks depend on each other, or only 1-2 quick checks | Lowest | N/A |
| **Subagents** | Independent tasks where only the result matters | Medium | None (report back to main only) |
| **Teams** | Complex work where workers need to share findings, challenge each other, or coordinate on their own | Highest | Direct messaging between teammates |

## Decision Protocol

1. **Can tasks be parallelized at all?** If each step depends on the previous result, use sequential.
2. **Do workers need to talk to each other?** If yes → teams. If no → subagents.
3. **Is the work complex enough to justify coordination overhead?** Research, review, competing hypotheses, cross-layer changes → teams. Focused lookups, test runs, file analysis → subagents.

## Subagents (Agent tool)

Spawn via the `Agent` tool. Each subagent runs in its own context window and returns a single result to the caller. Workers are invisible to each other.

Best for:
- Researching independent questions in parallel
- Delegating isolated implementation tasks
- Protecting main context from verbose tool output

## Teams (TeamCreate tool)

Requires `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in settings. Teammates share a task list, message each other directly, and self-coordinate without the lead's involvement.

Best for:
- Debugging with competing hypotheses (teammates actively disprove each other)
- Cross-layer work: frontend + backend + tests each owned by a different teammate
- Code review with distinct lenses (security, performance, test coverage) running simultaneously
- Open-ended research where findings in one lane should influence another

Practical limits:
- Start with 3–5 teammates; coordination overhead grows faster than throughput beyond that
- Aim for 5–6 tasks per teammate — small enough to check in, large enough to be self-contained
- Each teammate has its own context window; token cost scales linearly with team size
- Teammates do not inherit the lead's conversation history — include all task-specific context in the spawn prompt

## Rules

- Default to subagents for parallelism unless workers need to cross-communicate or debate findings.
- Default to sequential when there are only 1-2 obvious things to check — parallelism has overhead.
- When spawning teams, give each teammate a distinct, non-overlapping scope to prevent file conflicts and redundant work.
- Teams are experimental and do not support session resumption for in-process teammates.
- Never use teams as a substitute for clear task decomposition — a well-scoped subagent beats a poorly-briefed teammate.
