# Codex Delegation

> **Applicability** — This rule applies when OpenAI Codex CLI is available on `PATH` alongside Claude Code. Without Codex, the `/review` skill falls back to a single-evaluator review (Claude subagent only); the cross-provider generator-vs-evaluator separation is weaker but the rules-side policy below still applies to Claude-side work.

Cross-provider delegation serves three purposes:

1. **Bias breaking** — catches blind spots a single training distribution misses (the generator-vs-evaluator separation from `evaluation-integrity.md` extended across model families).
2. **Anchor breaking** — a fresh stack resets the reasoning anchor when Claude loops on a hard problem.
3. **Ecosystem capability** — access to OpenAI-native tools (image generation, OpenAI-exclusive models) that Claude Code does not carry natively.

The first two motivate reliability routing; the third motivates capability routing.

## Entry Point

The only ai-roots-provided surface that wraps Codex is the **`/review` skill** (`skills/review.md`). It spawns a Claude Code subagent and a `codex review --uncommitted` in parallel, then synthesizes per `evaluation-integrity.md` §Multi-advisor synthesis. Use it for any review-class delegation: general diff review, security-sensitive review, both.

For non-review Codex work (rescue debugging, research, bounded implementation), invoke `codex` directly via Bash with the appropriate flags. There is no longer a slash-command wrapper for those modes — see the per-mode invocations below.

## Reasoning effort

Always `xhigh`. Pass `-c model_reasoning_effort=xhigh` on every invocation.

## Flag placement (codex-cli ≥ 0.125)

`--search`, `-a/--ask-for-approval`, and `--dangerously-bypass-approvals-and-sandbox` are **top-level flags** and precede the subcommand. `--sandbox`, `--full-auto`, and `-c key=value` are **exec subcommand flags** and follow `exec`. Misplacement fails with `error: unexpected argument '--ask-for-approval' found`. Verify with `codex --help` and `codex exec --help`.

```
codex [TOP-LEVEL FLAGS] exec [EXEC FLAGS] -- - < prompt
codex review [REVIEW FLAGS]    # read-only by design; does not accept --sandbox / -a
```

## Mode Cheatsheet

| Need | Invocation |
|------|------------|
| Independent + security-sensitive review | `/review` skill |
| Stuck after three failed attempts | `codex exec --sandbox read-only -m gpt-5.5 -c model_reasoning_effort=xhigh -` with rescue brief on stdin |
| Current docs or web research | `codex --search -a never exec --sandbox read-only -m gpt-5.5 -c model_reasoning_effort=xhigh -` |
| Bounded implementation (workspace edits, approval on-request) | `codex exec --full-auto -m gpt-5.5 -c model_reasoning_effort=xhigh -` |
| Unattended long implementation (workspace sandbox, no approvals) | `codex --search -a never exec --sandbox workspace-write -m gpt-5.5 -c model_reasoning_effort=xhigh -` |
| Explicit no-sandbox run (only when user explicitly accepts) | `codex --search --dangerously-bypass-approvals-and-sandbox exec -m gpt-5.5 -c model_reasoning_effort=xhigh -` |

Do not pick a broader mode for convenience. Research does not need write access. Image generation needs ecosystem capability, not no-sandbox access. Dependency installation, external CLIs, and private network calls are separate requirements that must be named in the brief.

## Routing Rules

**Three-turn cap on stuck problems.** Do not attempt a 4th inline turn on the same hypothesis. Delegate to a Codex rescue (read-only sandbox) with all ruled-out hypotheses included.

**Adversarial review on security-sensitive changes.** After every behavioral change touching authentication, authorization, database writes, network boundaries, secret handling, or trust boundaries, invoke `/review`. Read-only reads or pure internal refactors do not trigger. The reviewer persona — skeptical, security-first, classifies findings P0–P3, returns `VERDICT: SAFE` only when no critical issues surface at high coverage — lives in `agents/adversarial-reviewer.md` (installed to `~/.claude/agents/`) and is piped via stdin to `codex review` by the skill.

**Capability routing fires on turn one.** Image generation, TTS, or other OpenAI-exclusive tool needs route to Codex immediately. Do not waste turns on text-based workarounds (ASCII art, hand-coded SVG) when the deliverable is an image or audio artifact.

## Three-Turn Rescue Protocol

1. **Turn 1** — original plan.
2. **Turn 2** — revise the hypothesis (root cause may be in a different layer; see `parallel-hypothesis-investigation.md`).
3. **Turn 3** — one more hypothesis.
4. **After Turn 3** — `codex exec --sandbox read-only ...` with original task, each hypothesis attempted and why it failed, minimal reproducer, and ruled-out files on stdin.

A "turn" is one substantive attempt, not one message. Past three, marginal information collapses and anchoring bias hardens.

## Codex Execution Mechanics

Two concerns to manage independently:

1. **Claude must know when codex finishes.** Use `run_in_background: true` Bash; the harness's completion notification wakes Claude.
2. **The user may want to see codex's reasoning live.** Give them the log path; let them `tail -f` in their own terminal. Do not script the live view from Claude's side.
3. **Codex must be guaranteed to finish.** A hung codex never exits, so its completion notification never fires and the main session waits forever. Wrap every codex invocation in a timeout (`timeout <secs> codex …`, or `gtimeout` on macOS without coreutils; degrade gracefully if neither exists). On expiry codex exits 124 — read the exit status and treat a timeout as codex being unavailable, not as a clean result.

```bash
LOG="/tmp/codex-$(date +%Y%m%d-%H%M%S).log"
Bash(
  run_in_background: true,
  command: "<codex invocation> 2>&1 | tee '$LOG'"
)
# When the background task completes, Read "$LOG".
```

No sentinel, no `tail -f` from Claude, no split pane. See `lessons/codex-tmux-monitoring.md` for why the previous wrapper failed.

**Stdin-piping invocations** (`exec`, `review`) take their prompt via stdin. Write to a temp file first, then redirect:

```bash
PROMPT="$(mktemp)"
cat > "$PROMPT" <<'EOF'
<reviewer prompt or task brief>
EOF
Bash(run_in_background: true, command: "codex exec ... -- - < '$PROMPT' 2>&1 | tee '$LOG'")
```

## Plan-stage Review

Two-reviewer review is also valuable *before* code is written, when the artifact is a **plan** rather than a diff. Catches design decisions that would be expensive to retract once implementation starts.

**Pays off when:** the plan touches multiple files / new modules / new abstractions; depends on framework or library APIs the planner has not personally verified; the implementation is large enough that throwing it away mid-stream is costly (≥ 1 PR or ≥ a few hundred lines).

**Skip when:** one or two file edits with obvious shape, or exploratory ("try X, see what happens").

**Format:** `VERDICT: PLAN_APPROVED | REVISE_PLAN` (not `SAFE | NEEDS_CHANGES` — those are diff-review verdicts). Findings classify P0–P3.

**Plan review is advisory, not blocking.** PR-stage review remains mandatory. The user makes the call on whether to revise or proceed.

**Anti-patterns:** stale-revision review (see Cross-Provider Rules below); round inflation past ~3 (the plan owner has not converged — clarify goals with the user instead); treating advisory as blocking.

## Cross-Provider Rules

- Three-turn cap is a forcing function, not a hard ceiling. If Turn 3 produces a confirmed breakthrough, finish; otherwise escalate.
- Never skip `/review` on security-sensitive paths to save tokens.
- When invoking a Codex rescue, include ruled-out hypotheses so Codex does not redo the same work.
- Treat Codex findings as **independent evidence**: investigate disagreements with Claude's conclusion; do not resolve them by asking Claude alone to reconsider.
- Codex delegation is orthogonal to the Opus/Sonnet/Haiku tiers in `model-effort-delegation.md` — those still apply to Claude-side work.
- **Stale-revision verification on every Codex round.** Codex sometimes outputs analysis from a previous invocation when called repeatedly on the same file. In every round-N prompt, ask Codex to first echo the current revision identifier (file `head -1`, git HEAD short SHA, or a unique header line). Verdicts that reproduce stale line numbers from a since-changed file are untrusted; retry with a fresh session (not `codex resume`).
- **Project CLAUDE.md may strengthen these defaults** — e.g., per-PR two-reviewer rule. Project-specific strengthening overrides the minimum; the minimum applies where the project is silent.
