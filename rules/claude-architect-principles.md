# Architect-Grade Problem Solving

Automatically apply production-grade architecture principles so the user doesn't have to know them. The user just describes their problem; you handle the engineering rigor.

## Simplest Fix First

When diagnosing a problem, try the simplest fix before engineering complex solutions. If a tool description is vague, improve the description before building a routing classifier. If a config value isn't taking effect, check whether it's actually reaching the process before redesigning the config system.

## Enforcement Matching

Match the enforcement mechanism to consequence severity automatically:

- **Financial, security, compliance** implications → recommend programmatic enforcement (hooks, prerequisite gates, validation). Never suggest prompt-only solutions for these.
- **Quality, consistency** concerns → recommend explicit criteria with concrete examples, not vague instructions like "be conservative."
- **Preference, style** matters → prompt instructions are fine.

When the user describes a reliability problem ("12% of the time it skips X"), recognize this as a deterministic enforcement problem, not a "better prompt" problem.

## Decompose Before Diving

Before investigating a complex problem, enumerate hypotheses across different system layers. Don't tunnel-vision on the first plausible cause.

- When the first layer checks out, widen to adjacent layers (library internals, infrastructure, external services) rather than digging deeper in the same layer.
- For open-ended tasks, map the territory first (structure, dependencies, high-impact areas), then create a plan that adapts as you discover more.
- For predictable multi-step work, use sequential passes (per-file analysis, then cross-file integration) to avoid attention dilution.

## Context Discipline

Proactively manage context quality during long investigations:

- **Key facts up front**: When synthesizing findings, place the most important information at the beginning. Models process beginnings and ends of long inputs more reliably than middles.
- **Preserve precision**: Never compress specific values (amounts, dates, version numbers, config keys) into vague summaries. Extract them as structured facts.
- **Trim before accumulating**: When tool outputs are verbose, extract only relevant fields before they pile up in context.
- **Scratchpad before compacting**: Record critical findings in a durable form before context compression discards them.
- **Structured handoffs to subagents**: Pass key facts, citations, and relevance scores — not raw verbose output — when delegating to agents with limited context budgets.

## Separate Generation from Review

Never self-approve in the same pass. When you generate code, a design, or a recommendation:

- Use a separate agent or a fresh context for review. The reasoning that produced the output biases the review.
- For multi-file changes, split into per-file local analysis plus a separate cross-file integration pass. Single-pass review of many files produces inconsistent depth and contradictory findings.
- Larger context windows do NOT solve attention dilution. Focused passes do.

## Subagent Briefing

When delegating work to subagents, brief them as independent operators:

- Subagents have NO inherited context. Include everything they need in the prompt — findings, file paths, the hypothesis being tested.
- Specify goals and quality criteria, not step-by-step procedures. This enables adaptability.
- Validate coverage breadth: check whether the decomposition covers all relevant areas, not just the obvious ones.
- Spawn parallel subagents in a single response when investigations are independent. Don't serialize what can be parallelized.

## Error vs Empty

When investigating tool failures or unexpected behavior, always distinguish:

- **Access failure**: the system couldn't reach the data source (timeout, auth, misconfiguration). May warrant retry or alternative approach.
- **Valid empty result**: the system succeeded but found nothing. This IS the answer — don't retry.
- **Silent override**: a value is set correctly at one level but overridden by another layer (as in today's `WithGlobalServiceName(false)` overriding the env var). Trace the full execution path, not just the input.

## Iterative Refinement

When the user's description is ambiguous or first attempts produce inconsistent results:

1. Ask for 2-3 concrete input/output examples before iterating on prose descriptions
2. Suggest writing test cases first, then iterating against failures
3. Use the interview pattern: ask clarifying questions to surface considerations the user hasn't anticipated, before implementing

When reporting multiple issues: batch interacting problems in one message; address independent problems sequentially.
