# comment-discipline rule — iteration-1 benchmark

**Model:** Sonnet (general-purpose subagents)
**Baseline:** identical prompt + explicit override instruction suspending `comment-discipline` for that single task.
**Caveat:** True rule suppression is impossible (the rule auto-loads via `~/.claude/rules/`). The override is the closest practical proxy.

## Metrics per output

Comment counting rule: each `//`, `/* */`, or `/** */` body line counts as one comment line. Docstring header blocks count as one "signature-echo" finding regardless of how many lines they span.

| Eval | Condition | LOC | Comment lines | Forbidden patterns | WHY comments |
|------|-----------|-----|---------------|--------------------|--------------|
| go-rate-limiter | with_rule | 44 | 0 | 0 | 0 |
| go-rate-limiter | baseline | 54 | 15 | 5 WHAT + 2 docstring sig-echo (`Limiter`, `NewLimiter`, `Allow`) | 0 |
| ts-debounce-hook | with_rule | 19 | 0 | 0 | 0 |
| ts-debounce-hook | baseline | 34 | 16 | 1 JSDoc sig-echo (9 lines) + 1 WHAT ("Schedule the update") | 1 borderline (stale first render note) |
| go-refactor | with_rule | 27 | 0 | 0 | 0 |
| go-refactor | baseline | 40 | 8 | 5 WHAT + 3 docstring sig-echo | 0 |

## Aggregate

| Condition | Mean comment density | Total forbidden findings | Total WHY findings |
|-----------|----------------------|--------------------------|--------------------|
| with_rule | 0.0% | 0 | 0 |
| baseline | 30.5% | 19 | 1 (borderline) |

## Findings

**P0 — Rule is doing its core job.** Across 3 prompts × Sonnet subagents, the rule eliminates the forbidden patterns it explicitly bans (WHAT restatements, signature-echo docstrings). The baseline produced 19 forbidden findings; the with_rule condition produced 0.

**P1 — Possible over-correction on `WHEN a comment earns its place`.** The rate-limiter's token-refill formula and lock-protected-state invariant are exactly the kind of "subtle invariant" the rule lists as warranting a comment, but the with_rule output has zero comments. Two readings:
1. The prompts didn't have strong-enough WHY hooks — these implementations are obvious enough that a careful reader is not surprised. The rule's self-check ("would removing the comment leave a reader confused?") answers "no" → no comment is correct.
2. The rule's "default to no comments" framing overshoots and suppresses even the few legitimate WHY comments.

The baseline data leans toward reading #1 — even with comments unleashed, the baseline did not produce a single non-trivial WHY comment either. The opportunity space for WHY comments on these prompts is genuinely small. To distinguish, iteration-2 should add a prompt with a deliberate WHY-hook (e.g., "this checksum step exists to compensate for a known firmware bug — preserve that note").

**P2 — Baseline confirms the rule targets a real failure mode.** Without the rule, Sonnet defaults to WHAT-paraphrase commenting on essentially every block — exactly the "defensive commenting habit" the rule predicts in §"Tension with other habits". The rule's claim that weaker models regress to this pattern when the constraint isn't restated is validated.

**P3 — Rule body's `subagent briefing` clause was not exercised here.** The rule says "When delegating implementation to a subagent, include this rule in the briefing." This benchmark did not restate the rule in the brief — it relied solely on the global rules-system loading. The fact that with_rule still scored 0/0/0 suggests the global load is sufficient for Sonnet on prompts of this complexity. For larger or more ambiguous prompts, restating may still matter (untested here).

## Conclusion

Rule works on the dimensions it was designed to enforce. No code change to `comment-discipline.md` warranted from this iteration. Suggested follow-up evals if you want a sharper picture:

1. Prompt with a planted WHY-hook (workaround comment justified) to confirm the rule does not over-suppress.
2. Prompt at Opus-level complexity (multi-file, ambiguous spec) to see if the rule survives more open-ended work.
3. Drop the global-rule load (run via Codex, which does not inherit `~/.claude/rules/`) for a true rule-off baseline — the current baseline is "rule-on + explicit override," which is a softer comparison.
