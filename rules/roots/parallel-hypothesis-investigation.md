# Parallel Hypothesis Investigation

When a problem has multiple plausible causes or multiple independent judgment criteria, investigate them concurrently rather than sequentially.

## Decomposition Axes

Parallel investigation only pays off when the work decomposes cleanly. Two axes are valid, and they are not interchangeable — picking the wrong one produces overlapping workers that redo each other's work.

| Axis | When to use | Worker framing |
|------|-------------|----------------|
| **Layer (hypothesis)** | Root cause is uncertain; could sit in application, library, infrastructure, or external service | "Test whether the cause is in layer X" |
| **Criterion (evaluation)** | Output must pass multiple independent judgment axes — correctness, security, UX, performance, compliance | "Judge the output against criterion X, ignoring the others" |

The layer axis is for *finding* something; the criterion axis is for *judging* something. Review and advisor-style work is usually criterion-axis; debugging is usually layer-axis. A single task can use both sequentially — first find the cause (layer), then judge the fix (criterion) — but do not mix them in a single parallel batch.

For criterion-axis synthesis output format, see `evaluation-integrity.md` §Multi-advisor synthesis.

## When to apply

- The root cause is uncertain and could lie in 3+ distinct areas (library internals, config, infrastructure, etc.)
- The output must satisfy 2+ independent judgment criteria that a single reviewer would blur together
- Each worker can proceed independently without blocking others
- Sequential investigation would waste time if the first guess is wrong

## Protocol

1. **Pick the axis first, then enumerate.** Decide whether you are decomposing by layer or by criterion. Then list the workers — hypotheses for layer-axis, judgment criteria for criterion-axis. Aim for breadth over depth at this stage.
2. **Dispatch parallel agents.** Assign each worker a non-overlapping scope. Each agent should know what to look for (layer-axis) or what to judge against (criterion-axis), and what constitutes a finding.
3. **Synthesize, don't just aggregate.** When results arrive, cross-reference findings. On the layer axis, one agent's discovery may explain or invalidate another's — the root cause often sits at the intersection of multiple layers. On the criterion axis, agents will often disagree on the same artifact; that disagreement is signal, not noise (see `evaluation-integrity.md`).

## Agent briefing principles

- Give each agent enough context to make judgment calls, not just follow instructions
- Specify the exact directories, files, or functions to start from
- State the hypothesis being tested (layer-axis) or the criterion being judged (criterion-axis), not just "investigate X"
- For criterion-axis agents, explicitly forbid cross-criterion commentary — a security reviewer should not argue about UX, or the criteria collapse back into one blurred review
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
