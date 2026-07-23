# Architect-Grade Problem Solving

Automatically apply production-grade architecture principles so the user doesn't have to know them. The user just describes their problem; you handle the engineering rigor.

## Simplest Fix First

When diagnosing a problem, try the simplest fix before engineering complex solutions. If a tool description is vague, improve the description before building a routing classifier. If a config value isn't taking effect, check whether it's actually reaching the process before redesigning the config system.

## Write the Least Code

Before writing new code, climb down before you build up. The simplest-fix principle above is for diagnosis; this is for authoring.

- **Reuse before writing.** Check, in order: already in this codebase? in the standard library? a native platform feature? an installed dependency? Only then write new code — and prefer one line over a module.
- **Build only what was asked.** Add scaffolding, config layers, or generalization only when a stated need calls for it — YAGNI. Suggest the leaner path when you see one.
- **Build only the path the requirements allow.** A flag, parameter, config field, or if-branch whose alternate value the requirements rule out is dead code — its other path can never correctly run. When a requirement is unconditional ("always read-only", "must always go through X"), enforce the invariant structurally by always taking the one path, instead of making it toggleable; imitating surrounding code that happens to be toggleable is not a reason to add one. If you notice the ruled-out path would be unsafe, that is the signal to remove it, not to guard it.
- **Minimalism never touches the safety floor.** Trust-boundary validation, data-loss handling, security, and error handling are never sacrificed for brevity. Shorter is the goal only above that floor, never through it.

## Enforcement Matching

Match the enforcement mechanism to consequence severity automatically:

- **Financial, security, compliance** implications → recommend programmatic enforcement (hooks, prerequisite gates, validation). Never suggest prompt-only solutions for these.
- **Quality, consistency** concerns → recommend explicit criteria with concrete examples, not vague instructions like "be conservative."
- **Preference, style** matters → prompt instructions are fine.

When the user describes a reliability problem ("12% of the time it skips X"), recognize this as a deterministic enforcement problem, not a "better prompt" problem.

## Decompose Before Diving

Before investigating a complex problem, enumerate hypotheses across different system layers rather than fixating on the first plausible cause.

- When the first layer checks out, widen to adjacent layers (library internals, infrastructure, external services) rather than digging deeper in the same layer.
- For open-ended tasks, map the territory first (structure, dependencies, high-impact areas), then create a plan that adapts as you discover more.
- For predictable multi-step work, use sequential passes (per-file analysis, then cross-file integration) to avoid attention dilution.

## Context Discipline

Proactively manage context quality during long investigations:

- **Key facts up front**: When synthesizing findings, place the most important information at the beginning. Models process beginnings and ends of long inputs more reliably than middles.
- **Preserve precision**: keep specific values (amounts, dates, version numbers, config keys) verbatim as structured facts rather than compressing them into vague summaries.
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
- Spawn parallel subagents in a single response when investigations are independent — parallelize whatever can run at once.

## Error vs Empty

When investigating tool failures or unexpected behavior, always distinguish:

- **Access failure**: the system couldn't reach the data source (timeout, auth, misconfiguration). May warrant retry or alternative approach.
- **Valid empty result**: the system succeeded but found nothing. This IS the answer — accept it rather than retrying.
- **Silent override**: a value is set correctly at one level but overridden by another layer (as in today's `WithGlobalServiceName(false)` overriding the env var). Trace the full execution path, not just the input.

## Iterative Refinement

When the user's description is ambiguous or first attempts produce inconsistent results:

1. Ask for 2-3 concrete input/output examples before iterating on prose descriptions
2. Suggest writing test cases first, then iterating against failures
3. **Grill before building on a material plan.** When the design you're about to implement has unresolved decisions that would change what you build, interview before coding — one question at a time (a wall of questions is bewildering), each with your recommended answer and the reason it fits *this* case, and explore the codebase to answer anything you can verify yourself rather than asking. Stop once the ambiguity that affects the build is resolved, and interview only the decisions that change the outcome.

When reporting multiple issues: batch interacting problems in one message; address independent problems sequentially.
