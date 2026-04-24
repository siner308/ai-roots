# Parallel Hypothesis Investigation

When a problem has multiple plausible causes across different layers, investigate them concurrently rather than sequentially.

## When to apply

- The root cause is uncertain and could lie in 3+ distinct areas (library internals, config, infrastructure, etc.)
- Each hypothesis can be investigated independently without blocking others
- Sequential investigation would waste time if the first guess is wrong

## Protocol

1. **Enumerate hypotheses by layer.** Before investigating, list all plausible causes grouped by system layer (application code, library internals, infrastructure, external service). Aim for breadth over depth at this stage.
2. **Dispatch parallel agents.** Assign each hypothesis (or closely related cluster) to a separate agent with a clear investigation scope. Each agent should know what to look for, where to look, and what constitutes a finding.
3. **Synthesize, don't just aggregate.** When results arrive, cross-reference findings. One agent's discovery may explain or invalidate another's. The root cause often sits at the intersection of multiple layers.

## Agent briefing principles

- Give each agent enough context to make judgment calls, not just follow instructions
- Specify the exact directories, files, or functions to start from
- State the hypothesis being tested, not just "investigate X"
- Ask for concise findings, not exhaustive reports

## Signals this approach is needed

- You've already tried the obvious fix and it didn't work
- The user says "it should work but doesn't"
- The problem spans boundaries (env vars set correctly but behavior wrong, config exists but not applied)
- Initial investigation rules out the first layer, suggesting the cause is deeper or in a different layer entirely

## Rules

- Don't parallelize trivially. If there are only 1-2 obvious places to check, just check them directly.
- Each agent should cover a non-overlapping investigation scope to avoid redundant work.
- Present synthesized findings as a unified picture with a clear root cause chain, not as disconnected per-agent reports.
- When multiple agents converge on the same finding from different angles, that's strong signal. When they contradict, investigate the gap.
