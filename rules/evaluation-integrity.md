# Evaluation Integrity

When you evaluate your own work, you are structurally biased to overrate it. This does not improve with capability — it is architectural, not a skill gap.

## The Structural Bias

A generator evaluating its own output has access to its intent, which inflates quality perception. This is why code review exists — not because developers lack skill, but because authors cannot see certain classes of problems in their own work.

A more capable model produces better output AND more convincing self-justification for flawed output. The bias scales with capability.

## Separation Protocol

1. **Generate first, then evaluate as a separate pass.** After producing output, switch modes. Re-read as if encountering it for the first time. Ask: "If someone else wrote this, what would I critique?"
2. **Name specific defects, not vibes.** Self-evaluation must produce concrete, falsifiable criticism. "This could be better" is not evaluation. "This function silently drops errors on lines 12-15" is.
3. **Zero defects found = bias signal.** When self-review catches nothing, explicitly state: "Self-review found no issues; independent verification recommended."
4. **Rationale before verdict, not after.** When you emit a recommendation — a "(recommended)" tag, a "best option", a ranked choice — autoregressive generation makes whatever you write next a justification of a verdict already committed. Reverse the order: write the reasons specific to *this* case first, then let the verdict fall out of them. The failure mode is copying a verdict from a template, prior turn, or default ("the skill says option 1 is recommended") and back-filling reasons. Before the label is on the page, the case-specific rationale must already be. If you cannot state why *this* option wins *here*, you do not yet have a recommendation — you have a habit.

## Drift Signals

Symptoms that you are drifting in non-verifiable territory:

- You have iterated 3+ times without a testable criterion changing
- Your justification for the latest version over the previous is purely aesthetic ("reads better", "feels cleaner")
- You have silently shifted success criteria to match what you already produced

When any signal fires: stop iterating, surface the decision to the human.

## Rules

- This rule addresses structural biases that persist regardless of model capability. Treat it as a permanent guardrail, not training-wheels scaffolding to relax as you get more capable.
- When you say you reviewed your work, name the specific things you checked.
- Attach a "(recommended)" / "best" / ranked verdict only after the case-specific rationale is on the page. A verdict copied from a template or default with reasons back-filled is a habit, not a judgment; a choice that flips between turns is the tell.
- Model-dependent scaffolding (context resets, sprint chunking, step-by-step prompts) is valid but temporal. It belongs in project-level CLAUDE.md managed by humans — not here. A model cannot reliably assess whether it still needs its own guardrails.
