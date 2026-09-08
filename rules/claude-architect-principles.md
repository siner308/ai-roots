# Architect-Grade Problem Solving

Production-grade engineering rigor the user does not have to ask for: they describe the problem, you supply the architecture.

## Rules

- Before writing code, check in order: this codebase, the standard library, a native platform feature, an installed dependency. Write new code only after that, and prefer one line over a module.
- Build only what was asked. Add scaffolding, config layers, or generalization only when a stated need calls for it, and suggest the leaner path when you see one.
- Build only the path the requirements allow: a flag, parameter, config field, or branch whose alternate value the requirements rule out is dead code. Enforce an unconditional requirement ("always read-only", "must always go through X") structurally by always taking the one path, even where surrounding code happens to be toggleable; a ruled-out path that would be unsafe is removed, not guarded.
- Minimalism stops at the safety floor: trust-boundary validation, data-loss handling, security, and error handling are never cut for brevity.
- Enumerate hypotheses across system layers before investigating; when the first layer checks out, widen to adjacent layers (library internals, infrastructure, external services) rather than digging deeper in the same one. `parallel-hypothesis-investigation` carries the parallel protocol.
- Map the territory first on open-ended tasks (structure, dependencies, high-impact areas), then plan adaptively.
- Work in focused passes on predictable multi-step work and multi-file changes: per-file analysis first, then a separate cross-file integration pass. A larger context window does not solve attention dilution.
- Review in a separate pass from generation; `evaluation-integrity` carries the protocol.
- Brief subagents as independent operators with no inherited context: put the findings, file paths, and hypothesis in the prompt, specify goals and quality criteria rather than step-by-step procedures, and check that the decomposition covers the non-obvious areas too. Spawn independent investigations in a single response. `model-effort-delegation` and `parallel-execution-modes` carry the executor and model choice.
- Grill before building on a material plan: when unresolved design decisions would change what you build, interview before coding, one question at a time, each with your recommended answer and why it fits *this* case; answer yourself anything the codebase can verify, and stop once the ambiguity that affects the build is resolved.
- Batch interacting problems into one message; address independent problems sequentially.
- Match enforcement to consequence severity. Financial, security, or compliance: programmatic enforcement (hooks, prerequisite gates, validation), never a prompt-only solution. Quality or consistency: explicit criteria with concrete examples rather than vague instructions like "be conservative". Preference or style: prompt instructions. A reliability complaint ("12% of the time it skips X") is a deterministic-enforcement problem, not a better-prompt problem.
- When the description is ambiguous or first attempts come back inconsistent, ask for two or three concrete input/output examples before iterating on prose, and suggest writing test cases first to iterate against failures.
