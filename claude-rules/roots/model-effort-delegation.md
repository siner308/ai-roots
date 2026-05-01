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

> **Applicability** — This section applies only when OpenAI Codex is configured alongside Claude Code. Codex is **optional** (`./install.sh --with-codex` installs the `/codex:*` commands and reviewer agent). Projects with ample Claude Code capacity may intentionally skip it; the in-platform delegation above remains in force either way. Without Codex, `Agent` with a distinct `subagent_type` (or a separate Claude Code team lens) can substitute for `/codex:adversarial-review` when cross-family verification is not available — the cross-model diversity is weaker, but the generator-vs-evaluator separation still holds.

Beyond in-platform subagents, a second delegation axis exists: **OpenAI Codex**, running alongside Claude Code as an independent reasoning stack. Cross-provider delegation serves three distinct purposes:

1. **Bias breaking** — catches blind spots a single training distribution cannot see (the generator-vs-evaluator separation from `evaluation-integrity.md` extended across model families).
2. **Anchor breaking** — a fresh stack resets the reasoning anchor when Claude loops on a hard problem.
3. **Ecosystem capability** — access to OpenAI-native tools (image generation, OpenAI-exclusive models) that Claude Code does not carry natively.

The first two motivate the reliability routing rules below; the third motivates capability-based routing.

### Codex Mode Selection

Choose the narrowest Codex mode that can finish the delegated job:

**Reasoning effort:** Always use `xhigh` — pass `-c model_reasoning_effort=xhigh` on every `codex` invocation. This is the maximum available level and should never be omitted.

| Need | Command | Codex flags | Why |
|------|---------|-------------|-----|
| Independent code review | `/codex:diff-review` | `codex review --uncommitted -c model_reasoning_effort=xhigh` | Read-only reviewer; no implementation drift |
| Security-sensitive review | `/codex:adversarial-review` | `codex review --uncommitted -c model_reasoning_effort=xhigh` + adversarial prompt | Cross-family gate for auth, data, network, secrets, trust boundaries |
| Current docs or web research | `/codex:research` | `--sandbox read-only --ask-for-approval never --search -c model_reasoning_effort=xhigh` | Web-backed research without write access |
| Stuck after three failed attempts | `/codex:rescue` | `--sandbox read-only -c model_reasoning_effort=xhigh` by default | Fresh reasoning stack without changing files |
| Bounded implementation | `/codex:autopilot` | `--full-auto -c model_reasoning_effort=xhigh` | Workspace edits allowed; risky actions still request approval |
| Unattended long implementation | `/codex:overnight` | `--sandbox workspace-write --ask-for-approval never --search -c model_reasoning_effort=xhigh` | Avoids approval stalls while preserving workspace sandbox |
| Explicit no-sandbox run | `/codex:yolo-overnight` | `--dangerously-bypass-approvals-and-sandbox --search -c model_reasoning_effort=xhigh` | Only when the user explicitly accepts no sandbox/no approvals |

Do not use a broader mode just because it is more convenient. Research does not need write access. Image generation or web research needs ecosystem capability, not no-sandbox access. Dependency installation, external CLIs, and private network calls are separate requirements that must be named in the brief.

### Routing Rules

When handling complex implementation tasks or debugging elusive race conditions, do not attempt to solve the problem in more than three turns. If unsuccessful, proactively delegate through the `/codex:rescue` command.

After every significant code change involving security-sensitive paths (e.g., authentication, database writes, or network access), you must invoke the `/codex:adversarial-review` command to challenge your implementation.

### Ecosystem-Specific Capability Routing

Codex reaches the OpenAI ecosystem; Claude Code does not. Delegate by **capability** when a task requires a tool only one ecosystem offers — this is a routing decision, not a reliability escalation.

Current examples:

- **Image generation** — DALL-E, `gpt-image`, and related OpenAI image models are reachable through Codex. For UI mocks, blog illustrations, diagrams-as-images, placeholder art, or any task whose deliverable is a raster/SVG image, delegate to Codex rather than attempting text-based workarounds (ASCII art, verbose SVG hand-coding, or asking the user to generate elsewhere).
- **Other OpenAI-exclusive tools** — as OpenAI ships new modalities (TTS, audio transcription, o-series models with specific tool access), route capability-bound tasks to the ecosystem that supports them natively.

Capability routing is **independent of the three-turn cap and the security review**: if Claude needs an image, delegate on turn one; if Claude needs adversarial review, delegate after a security-sensitive change. These are separate triggers with separate targets — do not wait for reliability failure to trigger a capability delegation.

### Codex Live Execution (tmux)

By default, subprocess output of `/codex:*` commands is captured into Claude's transcript and invisible to the user until Claude relays it. This hides Codex's live reasoning — which is often the most valuable part of delegating to a second stack.

When `$TMUX` is set (i.e. Claude Code is running inside a tmux session), wrap every `/codex:*` invocation in a split-pane + `tee` + sentinel pattern so the user sees output streaming in real time AND Claude gets a clean log file to read on completion. When `$TMUX` is unset, fall back to the plain invocation documented in each command.

**Pattern:**

```bash
LOG="/tmp/codex-$(date +%Y%m%d-%H%M%S).log"
RUNNER="$(mktemp)"
cat > "$RUNNER" <<EOF
#!/bin/bash
<codex invocation for this command, writing to stdout/stderr>
echo
echo '=== CODEX DONE ==='
read -p 'press enter to close'
EOF
chmod +x "$RUNNER"
tmux split-window -h "$RUNNER 2>&1 | tee '$LOG'"
# Event-driven wait — completion notification fires when sentinel hits.
# Run this in background so the main session stays responsive.
tail -f "$LOG" | grep -qm1 'CODEX DONE'
# After the tail exits, Read "$LOG" for authoritative output.
```

**Rules:**

- **Event-driven wait only.** Use `tail -f | grep -qm1 <sentinel>` (or the `Monitor` tool on the log file) run in background. Do NOT use `ScheduleWakeup` polling to check completion — the sentinel is a deterministic signal, polling adds cost without information. See `lessons/background-task-monitoring.md` for the full decision ladder.
- **Sentinel is mandatory and must be inside the `tee` pipeline.** The `=== CODEX DONE ===` marker is what makes the wait deterministic. Echo it via `stdout` (so `tee` writes it to the log) *immediately after* codex exits and *before* the `read -p` that pauses the pane. **Do NOT write the sentinel via `>> "$LOG"` from the runner script** — the runner itself is *not* inside the `tee` pipeline (only its stdout is), so the redirect races with `tee`'s flush. **Do NOT put the sentinel echo *after* `read -p`** — `read -p` blocks until the user presses Enter, so the sentinel never reaches the log until then.
- **Keep the pane open on exit.** The trailing `read -p` lets the user scroll the output after completion. Claude is reading from the log file, not the pane, so the pane's lifetime does not block Claude.
- **If the sentinel never fires, fall back to direct log read.** If the user reports "codex is done" but the background `tail` never exited (sentinel write failed or got eaten by the runner), `Read` the log file directly and grep for the verdict. Do NOT keep the user waiting on a missed signal — sentinels can drop, the log is authoritative.
- **Stdin-piping commands** (adversarial-review, rescue, overnight, research, yolo-overnight, autopilot) still take their prompt via stdin — redirect from a temp file written before the tmux call, e.g. `codex exec -- - < "$PROMPT_FILE"`.
- **Fallback when not in tmux.** If `[ -z "$TMUX" ]`, run the command's documented bash block directly. Do not try to spawn a new Terminal window silently — that surprises the user more than a foreground invocation.

This convention applies to every `/codex:*` command uniformly; individual command files document the specific codex invocation, not the wrapping.

### Codex Autopilot Approval Policy

Use `/codex:autopilot` for bounded implementation work when Codex should act as an independent worker. The default command must use `codex exec --full-auto`, which OpenAI documents as `--sandbox workspace-write --ask-for-approval on-request`: Codex can work inside the workspace, while network access and writes outside the workspace still require approval.

Use `/codex:overnight` when the user wants Codex to continue unattended. This mode removes approval prompts but keeps the workspace sandbox. It is the default for "work while I sleep" requests when the task has clear acceptance criteria and verification.

Do not use `--dangerously-bypass-approvals-and-sandbox` as a default. OpenAI documents it as dangerous full access: no sandbox and no approvals. Use `/codex:yolo-overnight` only when the user explicitly requests no-sandbox/no-approval behavior for this task and accepts that local credentials, workspace-external files, network access, and destructive commands are no longer guarded by Codex approvals. If consent is unclear, use `/codex:overnight` instead.

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
- **Stale-revision verification on every Codex round.** Codex sometimes outputs analysis from a *previous* invocation (line numbers and findings frozen to an old revision of the same path) when called repeatedly on the same file. Two countermeasures:
  - In every round-N prompt, ask Codex to *first* echo the current revision identifier — file `head -1`, git HEAD short SHA, or a unique header line that only the latest revision carries. The verdict is trustworthy only when that identifier matches what you just wrote.
  - When a Codex verdict reproduces *exact* line numbers from a prior round whose file has since changed substantively, treat the verdict as stale and retry with a fresh session (not `codex resume`). The first try is not always the failure — but a stale verdict is worse than a missed round because it claims to have seen current state.
- **Project CLAUDE.md may strengthen these defaults.** This rule defines the *minimum* delegation policy. A project's `CLAUDE.md` (or per-repo memory) can require stricter behavior — e.g., "every PR (not just security-sensitive) requires both reviewers SAFE in the same round" or "every plan round logs to a tracked artifact." Project-specific strengthening overrides the minimum; the minimum still applies where the project is silent.

## Plan-stage Review

Two-reviewer review (Claude subagent + Codex) is also valuable *before* code is written, when the artifact under review is a **plan** rather than a diff. Catches design decisions that would be expensive to retract once implementation starts (wrong abstraction, missed edge case, fictional API).

**When plan-stage review pays off:**

- The plan touches multiple files / new modules / new abstractions.
- The plan depends on framework or library APIs the planner has not personally verified (e.g., "use `Foo.bar()` to do X" without testing that `bar()` exists at the expected signature).
- The implementation work is large enough that throwing it away mid-stream is costly (≥ 1 PR or ≥ a few hundred lines).
- A user explicitly asks for plan review before implementation.

**When to skip:**

- The plan is one or two file edits with obvious shape — review cost > expected catch.
- The plan is exploratory ("try X, see what happens") and you want to learn from the implementation, not pre-flight it.

**Format:**

- Use `VERDICT: PLAN_APPROVED | REVISE_PLAN` (not `SAFE | NEEDS_CHANGES` — those are diff-review verdicts and conflate "code is correct" with "design is sound").
- Findings still classify as P0 (blocking design flaw), P1 (material missing decision), P2 (minor gap), P3 (informational).
- **Plan review is advisory, not blocking.** PR-stage review remains mandatory; plan-stage findings are absorbed into the plan and re-reviewed only if they materially change implementation. The user makes the call on whether to revise or proceed.

**Anti-patterns:**

- Stale-revision review: see "Cross-Provider Rules" below — Codex reading round N-1 cached analysis instead of round N. Identical with diff review but more common in plan loops where the file path doesn't change.
- Round inflation: more than ~3 plan rounds usually means the plan owner has not converged on the design yet. Step back from review and clarify the goals with the user instead of looping.
- Treating advisory as blocking: plan review is a *help*, not a gate. If a finding is small enough that you'd accept it during PR review anyway, accept it now and move on.

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
- Plan-stage two-reviewer review is available before implementation — advisory only, `VERDICT: PLAN_APPROVED | REVISE_PLAN`. Use it when implementation work is large or depends on unverified APIs; skip when the plan is one-or-two-file obvious.
- **If Codex is configured** (optional): choose the narrowest `/codex:*` mode; cap inline attempts at 3 turns on hard problems and delegate to `/codex:rescue` beyond that; invoke `/codex:adversarial-review` on every security-sensitive change; use `/codex:research` for web-backed research; use `/codex:autopilot` for bounded implementation; use `/codex:overnight` for unattended work; reserve `/codex:yolo-overnight` for explicit no-sandbox/no-approval consent; route OpenAI-exclusive capabilities (image generation via DALL-E / `gpt-image`, TTS, etc.) to Codex on turn one
- **Codex stale-revision check**: every round-N Codex prompt asks Codex to echo the current revision identifier first; treat verdicts that reproduce stale line numbers as untrusted and retry with a fresh session.
- **Project CLAUDE.md can strengthen these defaults** — e.g., per-PR two-reviewer rule. Project rules override the minimum where they are stricter; the minimum applies where the project is silent.
