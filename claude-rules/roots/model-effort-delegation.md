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

## Cross-Provider Delegation (Codex)

> **Applicability** — This section applies only when OpenAI Codex is configured alongside Claude Code. Codex is **optional** (`./install.sh --with-codex`, or `./install.sh` and answer yes to the prompt). Projects with ample Claude Code capacity may intentionally skip it; the in-platform delegation above remains in force either way. Without Codex, `Agent` with a distinct `subagent_type` (or a separate Claude Code team lens) can substitute for `/codex:adversarial-review` when cross-family verification is not available — the cross-model diversity is weaker, but the generator-vs-evaluator separation still holds.

Beyond in-platform subagents, a second delegation axis exists: **OpenAI Codex**, running alongside Claude Code as an independent reasoning stack. Cross-provider delegation serves three distinct purposes:

1. **Bias breaking** — catches blind spots a single training distribution cannot see (the generator-vs-evaluator separation from `evaluation-integrity.md` extended across model families).
2. **Anchor breaking** — a fresh stack resets the reasoning anchor when Claude loops on a hard problem.
3. **Ecosystem capability** — access to OpenAI-native tools (image generation, OpenAI-exclusive models) that Claude Code does not carry natively.

The first two motivate the reliability routing rules below; the third motivates capability-based routing.

### Routing Rules

When handling complex implementation tasks or debugging elusive race conditions, do not attempt to solve the problem in more than three turns. If unsuccessful, proactively delegate to the `/codex:rescue` sub-agent.

After every significant code change involving security-sensitive paths (e.g., authentication, database writes, or network access), you must invoke the `/codex:adversarial-review` command to challenge your implementation.

### Ecosystem-Specific Capability Routing

Codex reaches the OpenAI ecosystem; Claude Code does not. Delegate by **capability** when a task requires a tool only one ecosystem offers — this is a routing decision, not a reliability escalation.

Current examples:

- **Image generation** — DALL-E, `gpt-image`, and related OpenAI image models are reachable through Codex. For UI mocks, blog illustrations, diagrams-as-images, placeholder art, or any task whose deliverable is a raster/SVG image, delegate to Codex rather than attempting text-based workarounds (ASCII art, verbose SVG hand-coding, or asking the user to generate elsewhere).
- **Other OpenAI-exclusive tools** — as OpenAI ships new modalities (TTS, audio transcription, o-series models with specific tool access), route capability-bound tasks to the ecosystem that supports them natively.

Capability routing is **independent of the three-turn cap and the security review**: if Claude needs an image, delegate on turn one; if Claude needs adversarial review, delegate after a security-sensitive change. These are separate triggers with separate targets — do not wait for reliability failure to trigger a capability delegation.

### What Counts as "Security-Sensitive"

`/codex:adversarial-review` is mandatory when a change modifies behavior on any of:

- **Authentication / authorization** — login, session, token issuance, permission checks, RBAC
- **Database writes** — inserts, updates, deletes, migrations (especially destructive DDL)
- **Network boundaries** — external API calls, request/response handlers, webhook receivers
- **Secret handling** — env parsing, credential storage, encryption/decryption
- **Trust boundaries** — user-input parsing, deserialization, command execution, path traversal

Read-only reads or pure internal refactors inside these paths do not trigger the review — the gate is a *behavioral* change, not mere file presence.

### Three-Turn Rescue Protocol

When to delegate to `/codex:rescue`:

1. **Turn 1** — attempt the fix or implementation with the original plan.
2. **Turn 2** — if Turn 1 fails, revise the hypothesis (the root cause may be in a different layer; see `parallel-hypothesis-investigation.md`).
3. **Turn 3** — if Turn 2 fails, form one more hypothesis and test it.
4. **After Turn 3** — do NOT attempt Turn 4 inline. Invoke `/codex:rescue` with:
   - Original task description
   - Each hypothesis attempted and why it failed
   - Minimal reproducer for bugs
   - Files and functions already ruled out

A "turn" here is one substantive attempt, not one message. A sequence of small clarifying edits within the same debugging line counts as one turn.

### Why Cap at Three

Past three unsuccessful attempts, marginal information per additional turn collapses and anchoring bias hardens — the model locks onto whichever framing it already invested reasoning in. A fresh stack (Codex) breaks the anchor. This is the `evaluation-integrity.md` drift signal applied at the delegation layer.

### Adversarial Reviewer Persona

`/codex:adversarial-review` uses the persona defined in `.claude/agents/adversarial-reviewer.md`: skeptical, security-first, tuned to find reasons NOT to ship. The reviewer classifies findings P0–P3 and returns `VERDICT: SAFE` only when no critical issues surface at high coverage.

### Cross-Provider Rules

- Three-turn cap is a **forcing function**, not a hard ceiling. If Turn 3 produces a confirmed breakthrough, finish; if still stuck, escalate — do not attempt Turn 4 inline.
- Never skip `/codex:adversarial-review` on security-sensitive paths to save tokens. Blast radius dominates cost.
- When delegating to `/codex:rescue`, include all ruled-out hypotheses so Codex does not redo the same work.
- Treat Codex findings as **independent evidence**: if Codex disagrees with Claude's conclusion, investigate the disagreement — do not resolve it by asking Claude alone to reconsider.
- Codex delegation is orthogonal to the Opus/Sonnet/Haiku selection above — in-platform model tiers still apply to Claude-side work.
- **Capability routing fires on turn one** — image generation, TTS, or other OpenAI-exclusive tool needs route to Codex immediately. Do not waste turns constructing text-based workarounds (ASCII art, hand-coded SVG) for tasks whose real deliverable is an image or audio artifact.

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
- **If Codex is configured** (optional): cap inline attempts at 3 turns on hard problems and delegate to `/codex:rescue` beyond that; invoke `/codex:adversarial-review` on every security-sensitive change; route OpenAI-exclusive capabilities (image generation via DALL-E / `gpt-image`, TTS, etc.) to Codex on turn one
