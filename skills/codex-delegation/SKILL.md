---
name: codex-delegation
description: "Apply when delegating work to the OpenAI Codex CLI — rescue debugging after Claude is stuck (three-turn cap), cross-provider/security-sensitive review, current-docs web research, or bounded/unattended implementation. Covers mode and flag selection, reasoning effort, the rescue protocol, plan-stage review, and execution mechanics. Trigger only when Codex CLI is on PATH."
---

# Codex Delegation

> **Applicability** — This rule applies when OpenAI Codex CLI is available on PATH alongside Claude Code. Without Codex, the `/review` skill falls back to a single-evaluator review (Claude subagent only); the cross-provider generator-vs-evaluator separation is weaker, but the rules-side policy below still applies to Claude-side work.

Cross-provider delegation serves three purposes:

1. **Bias breaking** — catches blind spots a single training distribution misses (the generator-vs-evaluator separation from evaluation-integrity.md extended across model families).
2. **Anchor breaking** — a fresh stack resets the reasoning anchor when Claude loops on a hard problem.
3. **Ecosystem capability** — access to OpenAI-native tools (image generation, OpenAI-exclusive models) that Claude Code does not carry natively.

The first two motivate reliability routing; the third motivates capability routing.

## Entry Point

Codex work arrives two ways. Match the entry point to how it was requested.

**Review → the `/review` skill, always.** For any review-class work use `/review` (`skills/review/SKILL.md`): it resolves one shared artifact, runs a Claude subagent and a Codex run in parallel on it, and synthesizes per evaluation-integrity.md §Multi-advisor synthesis. This is the single review entry point — do not reach for `codex review` or `/codex:review` directly.

**Anything else → a natural-language "delegate this to Codex" request.** Map it to a reliable invocation by intent. All three paths are verified on codex-cli 0.128:

- **Diagnosis / stuck debugging** → `/codex:rescue`, or the Agent tool with `subagent_type: "codex:codex-rescue"`. Read-only, runs on the companion runtime with completion wired to the harness.
- **Write / research / bounded implementation** → manual `codex exec` with the flags and mechanics below. Clean exit when the timeout is hardened (see Codex Execution Mechanics).

**Footgun — never `Skill(codex:rescue)`.** Calling it as a skill re-enters the slash command and hangs the session. Invoke rescue only through the `/codex:rescue` command or the Agent tool with `subagent_type: "codex:codex-rescue"`. A wrong entry point — not a broken runtime — is the usual cause of "Codex delegation hung."

## Reasoning effort

Always xhigh. Pass `-c model_reasoning_effort=xhigh` on every invocation.

## Flag placement (codex-cli ≥ 0.125)

`--search`, `-a`/`--ask-for-approval`, and `--dangerously-bypass-approvals-and-sandbox` are **top-level flags** and precede the subcommand. `--sandbox`, `--full-auto`, and `-c key=value` are **exec subcommand flags** and follow `exec`. Misplacement fails with `error: unexpected argument '--ask-for-approval' found`. Verify with `codex --help` and `codex exec --help`.

```
codex [TOP-LEVEL FLAGS] exec [EXEC FLAGS] -- - < prompt
codex review [REVIEW FLAGS]    # read-only by design; does not accept --sandbox / -a
```

## Mode Cheatsheet

`/review` (review) and `/codex:rescue` (diagnosis) supersede the matching rows below. The remaining rows — write, research, bounded/unattended implementation — are the normal manual `codex exec` invocations for those intents.

| Need | Invocation |
|------|------------|
| Independent + security-sensitive review | `/review` skill |
| Stuck after three failed attempts | `codex exec --sandbox read-only -m gpt-5…` |
| Current docs or web research | `codex --search -a never exec --sandbox …` |
| Bounded implementation (workspace edit…) | `codex exec --full-auto -m gpt-5.5 -c mo…` |
| Unattended long implementation (worksp…) | `codex --search -a never exec --sandbox …` |
| Explicit no-sandbox run (only when use…) | `codex --search --dangerously-bypass-app…` |

Do not pick a broader mode for convenience. Research does not need write access. Image generation needs ecosystem capability, not no-sandbox access. Dependency installation, external CLIs, and private network calls are separate requirements that must be named in the brief.

## Routing Rules

**Three-turn cap on stuck problems.** Do not attempt a 4th inline turn on the same hypothesis. Delegate to `/codex:rescue` (read-only) with all ruled-out hypotheses included — see the Three-Turn Rescue Protocol.

**Adversarial review on security-sensitive changes.** After every behavioral change touching authentication, authorization, database writes, network boundaries, secret handling, or trust boundaries, invoke `/review`. Read-only reads or pure internal refactors do not trigger. The reviewer persona — skeptical, security-first, classifies findings P0–P3, returns `VERDICT: SAFE` only when no critical issues surface at high coverage — lives in agents/adversarial-reviewer.md (installed to `~/.claude/agents/`) and is piped via stdin to `codex review` by the skill.

**Capability routing fires on turn one.** Image generation, TTS, or other OpenAI-exclusive tool needs route to Codex immediately. Do not waste turns on text-based workarounds (ASCII art, hand-coded SVG) when the deliverable is an image or audio artifact.

## Three-Turn Rescue Protocol

1. **Turn 1** — original plan.
2. **Turn 2** — revise the hypothesis (root cause may be in a different layer; see parallel-hypothesis-investigation.md).
3. **Turn 3** — one more hypothesis.
4. **After Turn 3** — hand it to `/codex:rescue` (or the Agent tool with `subagent_type: "codex:codex-rescue"`): the original task, each hypothesis attempted and why it failed, a minimal reproducer, and ruled-out files. Without the companion plugin, fall back to `codex exec --sandbox read-only ...` with the same content on stdin.

A "turn" is one substantive attempt, not one message. Past three, marginal information collapses and anchoring bias hardens.

## Codex Execution Mechanics

These mechanics apply to the manual `codex exec` path (write / research / bounded implementation, and any run when the companion plugin is absent). `/codex:rescue` and `/review` handle these concerns themselves.

Three concerns to manage independently:

1. **Claude must know when codex finishes.** Use `run_in_background: true` Bash; the harness's completion notification wakes Claude.
2. **The user may want to see codex's reasoning live.** Give them the log path; let them `tail -f` in their own terminal. Do not script the live view from Claude's side.
3. **Codex must be guaranteed to finish.** A hung codex never exits, so its completion notification never fires and the main session waits forever. Wrap every codex invocation in a timeout (`timeout <secs> codex …`, or `gtimeout` on macOS without coreutils; degrade gracefully if neither exists). On expiry codex exits 124 — read the exit status and treat a timeout as codex being unavailable, not as a clean result. Plain `timeout` signals only the direct child; codex (node) can leave grandchildren that hold the pipe open, so `| tee` never sees EOF and the background job hangs even after codex is killed. Use the kill-after grace (`gtimeout -k 10 <secs> …`) and redirect to a file (`> "$LOG" 2>&1`) rather than `| tee` when a run hangs at completion.

```
LOG="/tmp/codex-$(date +%Y%m%d-%H%M%S).log"
Bash(
  run_in_background: true,
  command: "<codex invocation> 2>&1 | tee '$LOG'"
)
# When the background task completes, Read "$LOG".
```

No sentinel, no `tail -f` from Claude, no split pane. See lessons/codex-tmux-monitoring.md for why the previous wrapper failed.

**Stdin-piping invocations** (`exec`, `review`) take their prompt via stdin. Write to a temp file first, then redirect:

```
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
- Codex delegation is orthogonal to the in-platform model tiers in model-effort-delegation.md — those still apply to Claude-side work.
- **Stale-revision verification on every Codex round.** Codex sometimes outputs analysis from a previous invocation when called repeatedly on the same file. In every round-N prompt, ask Codex to first echo the current revision identifier (`file head -1`, `git HEAD` short SHA, or a unique header line). Verdicts that reproduce stale line numbers from a since-changed file are untrusted; retry with a fresh session (not `codex resume`).
- **Project CLAUDE.md may strengthen these defaults** — e.g., per-PR two-reviewer rule. Project-specific strengthening overrides the minimum; the minimum applies where the project is silent.
