# Guardrail Maker

When the user corrects your understanding or behavior, detect it and propose a persistent guardrail so the same correction never happens twice.

## Rules

- Scan every user message for correction signals and match the intent regardless of language or phrasing; the Detection tiers table grades them.
- Apply the correction first and fix the current task; then append the proposal (The proposal section) to the reply and wait for confirmation before writing.
- Capture only corrections that prevent a future mistake, judged by the Worth capturing? table, and let the rest go.
- Search existing rules and `CLAUDE.md` for overlap first. On overlap, propose updating the existing rule and show the diff rather than adding a second copy. If new, write to the agreed location, matching the target file's existing style.
- Write resident rules into the git-tracked source tree (`rules/...`), never into an installed symlink or a generated block. Resolve the real path first (`readlink -f ~/.claude/rules/ai-roots`). Situational skills go in `skills/<name>/SKILL.md` with YAML frontmatter carrying `name` and a trigger-focused `description`. Re-running `install.sh` propagates both.
- A skill's `description` must match something visible in the request: a task type, an artifact, a phrase the user said, a countable property. A trigger that asks the model to notice its own state ("when work tempts autopilot", "when the outcome is uncertain", "after a vague ask cost time") does not fire: four skills phrased that way fired 0-1 times in 4, and rewritten around observable conditions they fired 2-4 times in 4. That figure measures firing only; whether firing improves the output is not measurable, since a control arm needs the skill unreachable while the agent runs and skill visibility is fixed at session start.
- Write in imperative form ("Use X", not "You should use X"), self-contained, with one sentence of WHY and a concrete good/bad pair when the distinction is subtle. Prefer positive framing ("Use X" over "Don't use Y"), but a prohibition is fine when the mistake is the core signal.
- Ask whether the rule applies to other projects when the scope is unclear.
- Confirm what was written and where, after writing.
- Memories track context; guardrails enforce behavior.

## Detection tiers

| Tier | Signal | Confidence |
|------|--------|------------|
| 1 | Direct correction: this is wrong and here is the right answer. Includes identity and meaning corrections, prohibitions ("don't", "stop", "never"), mandates ("always", "from now on"), substitutions ("use X instead of Y"). | High |
| 2 | Repeated correction: "I already told you this", "same mistake again", "how many times do I have to say it". Highest-value. | High |
| 3 | Convention declaration: a project, team, or domain rule stated preemptively with no preceding mistake. Naming conventions, architectural patterns, workflow rules, domain term definitions. | Medium |
| 4 | Implicit correction: "not quite right", "close but not exactly", a silent rephrasing, or quietly fixing your output and continuing. Verify worthiness more carefully. | Medium |

## Worth capturing?

| Capture | Skip |
|---------|------|
| Convention applicable to future work | One-time factual error (wrong path, typo) |
| Repeated correction pattern | Misunderstanding resolved by clarification |
| Domain knowledge not derivable from code | Already in existing rules or `CLAUDE.md` |
| Behavioral rule (always/never) | Preference for this conversation only |
| Cross-project principle | Ephemeral state (branch name, current PR) |

## The proposal

```
---
Guardrail proposal. Saving this as a rule prevents the same mistake in future conversations.

Rule: [one-line rule in imperative form]
Example: [concrete good/bad pair if applicable]
Location: [placement recommendation with rationale]
```

For a repeated correction, one line is enough:

```
---
Guardrail proposal: "[one-line rule]", save to [location]?
```
