---
name: model-effort-delegation
description: "Apply when deciding which executor (main session vs subagent vs team), which model (Opus/Sonnet/Haiku), and what effort level fits a task — i.e. before delegating non-trivial work or launching a multi-agent workflow/fan-out. Covers strict downgrade conditions (plan precision + verification loop), per-stage model pinning for fan-outs, escalation triggers, blast-radius override, and the subagent briefing standard."
---

# Model, Effort, and Subagent Delegation

For every task, deliberately choose the **executor** (main session vs subagent), **model** (Opus / Sonnet / Haiku), and **effort level**. Concentrate expensive models on architectural judgment; delegate well-specified implementation to cheaper models.

## Principle

Keep the main session on Opus — for planning, review, conversation, and localized edits. Delegate large, independent work to Sonnet/Haiku subagents. **The more specific the plan, the better weaker models preserve quality** — so the prerequisite for delegation is a precise plan.

## Executor Selection

For executor topology (main session / subagent / team) and the inline-vs-subagent threshold, see the parallel-execution-modes skill. This rule covers the orthogonal choice of *which model* runs in the chosen executor.

**Per-executor application.** The rule applies per executor, not per session. In a team, the team lead plays the same role as main Opus (planning, coordination, review); each teammate is selected by task type using the table below; downgrade conditions and escalation triggers apply to each teammate independently.

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

### Above Opus — when a higher tier is available

Anthropic occasionally makes a tier above Opus available (a limited release or research preview). When one is, it is never the default — Opus stays the ceiling for everyday architectural work, and you escalate deliberately, for the exceptional case, on observable signals only. "This feels hard" or "Opus seems stuck" is a self-assessment, not a trigger:

- **Non-convergence** — Opus made 3+ consecutive failed hypotheses or fix attempts on the same problem despite a working verification loop.
- **Contradictory analysis** — Opus reached mutually conflicting conclusions on the same question across 2+ passes.
- **Unresolved hard-to-reverse decision** — a schema migration, public API contract, or similar one-way door where a full Opus analysis pass still leaves the trade-off unresolved.
- **Lost coherence on a long-horizon run** — a single autonomous run where Opus has already re-derived or contradicted its own earlier work 2+ times.

When no higher tier is available, these same signals mean: stop grinding, change strategy — decompose differently, bring in a cross-provider evaluator (see codex-delegation), or surface the unresolved trade-off to the user.

### Downgrade Conditions — STRICT

To downgrade to Sonnet/Haiku, BOTH must be true:

1. The plan specifies file paths, function signatures, and verification method
2. A **verification loop exists** — tests, type checker, lint, or similar

If either is missing, keep Opus. Downgrading without a verification loop produces silent quality regressions (see evaluation-integrity).

### Fan-outs Pin Models Explicitly

Workflow scripts and multi-agent fan-outs inherit the session model by default, and fan-out multiplies that model's cost by the agent count. A 30-agent run inheriting a top-tier session (Opus or above) spends 30× top-tier tokens — almost never what anyone intended. This happened: a 32-agent concept tournament launched on a Mythos-tier session had to be killed mid-run.

- Before launching any workflow or fan-out of 3+ agents, set the model per stage explicitly in the script or spawn opts. Never rely on session-model inheritance for workers.
- The downgrade conditions apply at stage granularity: a precise rubric (checklist skill, fixed output schema) substitutes for plan precision, and structural redundancy (N independent votes, adversarial verify, majority rule) substitutes for a verification loop. High-volume judge/scan stages usually qualify for Sonnet; creative generation and cross-item synthesis usually don't — keep those on Opus.
- A session tier above Opus is for the orchestrator's judgment (planning, briefing, reading results), never for fan-out workers.

Example (32-agent concept tournament): scout = Sonnet (specified research, sources checkable), ideation = Opus (creative, no verification loop), 27 judges = Sonnet (each a single narrow lens + gate checklist + 3-vote redundancy), synthesis = Opus (cross-item trade-offs).

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

Escalation is part of the rule, not a failure. Stubbornly pushing a weak model leads to hysteresis — the wrong direction gets locked in. Above Opus there is a rung only when a higher tier happens to be available (see Above Opus) — and even then only on the observable signals listed there, never on a feeling that the problem is hard.

## Cross-Provider Delegation (Codex)

If Codex CLI is available on PATH, see the codex-delegation skill for mode selection, three-turn rescue protocol, security-sensitive review triggers (/review), capability routing, execution mechanics, and plan-stage review. Codex delegation is orthogonal to the in-platform model tiers above — those model tiers still apply to Claude-side work.

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
- A tier above Opus, when one is available, is escalation-only: observable signals (3+ failed attempts, contradictory conclusions, unresolved one-way-door decision, lost coherence), never the default
- Delegate to a subagent when: ≥5 min + independent + verifiable
- Downgrade only when BOTH plan precision and a verification loop exist
- Never downgrade model or effort when blast radius is high
- Fan-outs never inherit the session model — pin a model per stage before launching any 3+-agent workflow; a stage-level rubric plus vote redundancy can satisfy the downgrade conditions
- Escalate to Opus after 3 failures or when a design decision surfaces
- Briefings must include file paths, signatures, verification, and a request for decision reasoning
- If Codex CLI is available, see the codex-delegation skill for cross-provider rules (three-turn cap, adversarial review via /review, capability routing, plan-stage review).
- **Project CLAUDE.md can strengthen these defaults** — e.g., per-PR two-reviewer rule. Project rules override the minimum where they are stricter; the minimum applies where the project is silent.
