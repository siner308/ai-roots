# Model, Effort, and Subagent Delegation

For every task, deliberately choose the **executor** (main session vs subagent), **model** (Opus/Sonnet/Haiku), and **effort level**. Concentrate expensive models on architectural judgment; delegate well-specified implementation to cheaper models.

## Principle

Keep the main session on Opus — for planning, review, conversation, and localized edits. Delegate large, independent work to Sonnet/Haiku subagents. **The more specific the plan, the better weaker models preserve quality** — so the prerequisite for delegation is a precise plan.

## Execution Surface — Main vs Subagent vs Team

| Surface | When to use | Cross-worker comms |
|---------|-------------|--------------------|
| **Main session (inline)** | Interactive, localized, mid-stream judgment needed | N/A |
| **Subagent** | Independent, summarizable result, no debate required | None (returns single result) |
| **Team** | Competing hypotheses, cross-layer coordination, multi-lens review | Direct messaging between teammates |

See `parallel-execution-modes.md` for topology details.

**This rule applies per executor, not per session.** Teams do NOT bypass model-effort-delegation:
- The team lead (orchestrator) plays the same role as main Opus — planning, coordination, review
- Each teammate is selected independently by task type using the Model Selection table below
- Downgrade conditions (plan precision + verification loop) must be satisfied per teammate before assigning Sonnet/Haiku
- Escalation triggers apply to each teammate independently — a failing Sonnet teammate should be replaced or escalated, not tolerated because "the team is still running"

## Delegation Trigger — Subagent vs Inline

### Delegate to a subagent when ANY of the following hold
- Expected duration ≥ 5 minutes AND result can be summarized briefly
- **Independent** — no user input needed mid-execution, minimal main-context reference
- Two or more **parallelizable** independent tasks → spawn concurrently
- **Verbose output** (bulk grep, long logs, hundreds of files) — protect main context
- Long-running work suitable for **background** — builds, test suites, pipelines

### Keep inline (main Opus handles directly)
- 1–2 file localized edits
- Follow-up edits on a file just read (no re-exploration needed)
- Interactive work requiring ongoing user dialogue
- Tasks needing mid-stream judgment or producing long streaming output
- Briefing time would exceed the work itself

## Model Selection

| Task | Model | Rationale |
|------|-------|-----------|
| Architecture design, migration planning, tech selection | Opus | Trade-off judgment, ripple prediction |
| PR/code review, root-cause debugging | Opus | Hypothesis-falsification, tail cases matter |
| Plan-driven feature implementation | Sonnet | Clear spec narrows judgment space |
| Verifiable refactoring | Sonnet | Transformation rules are clear, tests catch drift |
| Test writing | Sonnet | Repetitive patterns, framework conventions |
| Bulk exploration, grep summaries | Haiku (Explore agent) | Path + summary is enough |
| Format conversion, comment adds, simple substitution | Haiku | Mechanical work |
| Log inspection, status checks | Haiku | Read-only, no judgment |

### Downgrade Conditions — STRICT

To downgrade to Sonnet/Haiku, BOTH must be true:
1. The plan specifies file paths, function signatures, and verification method
2. A **verification loop exists** — tests, type checker, lint, or similar

If either is missing, keep Opus. Downgrading without a verification loop produces silent quality regressions (see `evaluation-integrity`).

## Effort Selection

Orthogonal to model choice. Tune thinking budget to task risk.

| Effort | When to use |
|--------|-------------|
| **high** | Hard-to-reverse operations (DDL, production config, force-push), architecture decisions, debugging with unclear root cause |
| **medium** | Standard feature implementation, review, multi-layer refactoring |
| **low / off** | Single-file edits, mechanical transforms, tasks where verification catches errors immediately |

**Blast radius overrides effort.** A task that looks small but is hard to reverse stays at high + Opus.

## Escalation Triggers

If any signal appears during subagent execution, **escalate to Opus**:
- Same mistake repeated 3+ times
- Situation requiring a **design decision** not covered by the plan
- Failure rooted in **code comprehension gaps**, not spec ambiguity
- Verification loop fails repeatedly with unclear cause

Escalation is part of the rule, not a failure. Stubbornly pushing a weak model leads to hysteresis — the wrong direction gets locked in.

## Subagent Briefing Standard

When delegating to a weaker executor, the briefing MUST include:
- **File paths** and edit scope (explicit starting points)
- **Function signatures** or pseudocode
- **Existing code patterns** to follow (reference file + pattern)
- **Verification method** — which test or command determines success
- **Edge cases** and explicit out-of-scope items
- Request the subagent report **reasoning behind decisions** (for later traceability)

If the briefing would be thin, inline Opus is cheaper in practice.

## Examples

### Threshold-based delegation
```
Request: "Add avatar upload to the user profile page"
1. Main Opus: explore existing upload patterns inline (~2 min)
2. Main Opus: write plan — file paths, API endpoint, component structure, verification
3. Sonnet subagent: implement (independent, ~15 min)
4. Main Opus: review the result
```

### Inline handling
```
Request: "Add a nil check to the function you just looked at"
→ Main Opus edits inline. Briefing cost exceeds the work.
```

### Parallel delegation
```
Request: "Add the same endpoint pattern to 5 microservices"
→ Spawn 5 Sonnet subagents in parallel. Main does plan + review only.
```

### Over-delegation (bad)
```
Request: "Fix a typo in README"
Wrong: Haiku subagent — spawn overhead is 10× the work
Right: Inline edit
```

### Under-delegation (bad)
```
Request: "Audit the whole codebase for deprecated API usage"
Wrong: Main Opus runs repeated greps — main context gets polluted
Right: Delegate to Haiku Explore agent
```

## Rule Summary

- Main session stays on Opus — focus on planning, review, conversation, localized edits
- Delegate to a subagent when: ≥5 min + independent + verifiable
- Downgrade only when BOTH plan precision and a verification loop exist
- Never downgrade model or effort when blast radius is high
- Escalate to Opus after 3 failures or when a design decision surfaces
- Briefings must include file paths, signatures, verification, and a request for decision reasoning
