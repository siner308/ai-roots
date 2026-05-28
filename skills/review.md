---
name: review
description: Two-evaluator code review. Spawn a Claude Code subagent and a Codex review in parallel on the current uncommitted diff, then synthesize findings using the Agreed / Conflicting / Chosen-direction format from rules/roots/evaluation-integrity.md §Multi-advisor synthesis. Use whenever the user requests a review of pending changes and both Claude and Codex are available.
---

# ai-roots:review

Independent two-evaluator review for the current uncommitted diff. The two evaluators run in parallel and do not see each other's output until synthesis.

## Evaluators

### 1. Claude Code subagent

Invoke the `Agent` tool with `subagent_type: adversarial-reviewer` (persona at `~/.claude/agents/adversarial-reviewer.md`). The agent is briefed to review the uncommitted diff with the security-first, P0–P3 classification described in its own persona file. Pass the diff scope and any additional user scope as the agent prompt.

If the `adversarial-reviewer` agent is not registered, fall back to `subagent_type: general-purpose` and inline the persona body as the prompt.

### 2. Codex review

Run in parallel via background Bash:

```bash
LOG="/tmp/ai-roots-review-codex-$(date +%Y%m%d-%H%M%S).log"
cat "$HOME/.claude/agents/adversarial-reviewer.md" \
  | codex review -m gpt-5.5 -c model_reasoning_effort=xhigh --uncommitted - \
  2>&1 | tee "$LOG"
```

Use `run_in_background: true` so the main session is notified when Codex exits. If `codex` is not on `PATH`, skip this evaluator and note in the synthesis that only one reviewer ran.

### Parallelism

Spawn the Agent call and the Bash invocation in the same response so they run concurrently. Wait for both to complete before producing the synthesis.

## Synthesis

Apply `rules/roots/evaluation-integrity.md` §Multi-advisor synthesis. The output MUST separate three buckets:

1. **Agreed** — findings that appeared in BOTH evaluators. Highest confidence.
2. **Conflicting** — findings flagged by only one evaluator, or where evaluators disagree on severity / cause / fix. Single-evaluator findings belong here, not in Agreed. Silence is not agreement.
3. **Chosen direction + rationale** — the decision given the conflicts, and why. If a conflict is unresolved, say so and escalate to the user rather than picking silently.

For each finding, preserve the originating evaluator's severity classification (P0–P3 for adversarial reviewer; whatever Codex produces for its half). Do not re-rank findings to look consistent across evaluators — disagreement on severity is itself signal.

## Scope

Pass the user's additional scope (if any) to BOTH evaluators verbatim. Do not paraphrase or trim. If the user passes a file/path filter, narrow both evaluators to that scope.

## Anti-patterns

- Running only one evaluator and labeling the result a "review" — that defeats the cross-provider purpose of this skill. If Codex is unavailable, say so explicitly.
- Smoothing over disagreements in synthesis. The Conflicting bucket exists precisely because the synthesizer is biased toward making the output sound confident.
- Promoting a single-evaluator finding to "Agreed" because nothing contradicted it.
- Auto-applying fixes from either evaluator. Report findings; the main session decides what to apply.
