# Guardrail Maker — Tacit Knowledge Auto-Capture

When the user corrects your understanding or behavior, that correction is tacit knowledge surfacing. Detect it automatically and propose a persistent guardrail so the same correction never needs to happen twice.

## Detection

Scan every user message for correction signals. Detection is semantic, not literal — match the intent, regardless of language or phrasing.

### Tier 1 — Direct Corrections (High Confidence)

The user explicitly tells you something is wrong and provides the right answer. Includes identity/meaning corrections, prohibitions ("don't / stop / never"), mandates ("always / from now on"), and substitutions ("use X instead of Y").

### Tier 2 — Repeated Corrections (High Confidence)

The user signals they have corrected this before. Highest-value candidates because the gap is actively causing repeated waste — "I already told you this", "same mistake again", "how many times do I have to say it".

### Tier 3 — Convention Declarations (Medium Confidence)

The user states a project, team, or domain rule preemptively, without a preceding mistake — naming conventions, architectural patterns, workflow rules, domain term definitions.

### Tier 4 — Implicit Corrections (Medium Confidence)

The user signals something is off without being fully explicit — "not quite right", "close but not exactly", silent rephrasing of something you appeared to understand, or quietly fixing your output and continuing. Verify worthiness more carefully before proposing.

### Tier 5 — Frustration Signals (Highest Urgency)

Emotional frustration about a repeated or obvious mistake — exasperation in any language, re-sent instructions with added emphasis, short sharp responses ("no.", "wrong.", "again?"). Treat with Tier 2 urgency.

## Response Protocol

### Step 1: Apply First, Propose Second

Accept the correction immediately. Fix the current task. Never block work to discuss the guardrail.

### Step 2: Assess Guardrail Worthiness

| Capture as guardrail | Do NOT capture |
|---------------------|----------------|
| Convention applicable to future work | One-time factual error (wrong file path, typo) |
| Repeated correction pattern | Simple misunderstanding resolved by clarification |
| Domain knowledge not derivable from code | Info already in existing rules or CLAUDE.md |
| Behavioral rule (always/never patterns) | Task-specific preference for current conversation only |
| Cross-project principle | Correction about ephemeral state (branch name, current PR) |

### Step 3: Propose the Guardrail

After applying the correction, append this proposal:

```
---
Guardrail proposal — saving this as a rule prevents the same mistake in future conversations.

Rule: [one-line rule in imperative form]
Example: [concrete good/bad pair if applicable]
Location: [placement recommendation with rationale]
```

If the user is visibly frustrated (Tier 5), keep it to one line:
```
---
Guardrail proposal: "[one-line rule]" — save to [location]?
```

Wait for user confirmation before writing.

### Step 4: Write on Confirmation

1. **Search for overlap** — check existing rules and CLAUDE.md for related content
2. **If overlap found** — propose updating the existing rule, show the diff
3. **If new** — write to the agreed location, matching the target file's existing style
4. **After writing** — confirm what was written and where

## Placement Decision

| Signal | Location | Rationale |
|--------|----------|-----------|
| Universal principle (any project) | `ai-roots/rules/roots/` | Symlinked to `~/.claude/rules/ai-roots/`, loaded everywhere |
| Lesson learned from a mistake | `ai-roots/rules/lessons/` | Concrete pattern from real failure — describes what works better |
| Project-specific convention | Project `CLAUDE.md` | Loaded per-project |
| Project-specific, standalone topic | Project `.claude/rules/` | Modular, avoids bloating CLAUDE.md |
| Updates an existing rule | Same file as existing | Avoids fragmentation |

**Rules vs Lessons:** Rules (`rules/roots/`) define principles and protocols — they say what to do. Lessons (`rules/lessons/`) capture concrete patterns learned from real mistakes — they show what works better with before/after examples. If the correction is "never do X" → rule. If the correction is "we tried X and Y works better because Z" → lesson.

**Writing location:** `~/.claude/rules/ai-roots` is a symlink to this repository's `rules/` directory. Resolve the actual repo path with `readlink -f ~/.claude/rules/ai-roots` and write into the real git-tracked tree (`rules/roots/...` or `rules/lessons/...`) — never into `~/.claude/rules/ai-roots/...` directly, since symlinks can be confusing to reason about and the canonical source is the git repo.

When unsure about scope, ask the user whether the rule applies to other projects too.

## Writing Standards

A well-crafted guardrail:
- **Imperative form** — "Use X" over "You should use X"
- **Concrete example** — at least one good/bad pair when the distinction is subtle
- **Brief rationale** — one sentence on WHY, so edge cases can be judged
- **Self-contained** — understandable without reading other rules
- **Positive framing preferred** — "Use X" over "Don't use Y", but prohibitions are fine when the mistake is the core signal

## Non-Goals

- Does NOT auto-write guardrails without user confirmation
- Does NOT capture every conversation detail — only corrections that prevent future mistakes
- Does NOT replace the memory system — memories track context, guardrails enforce behavior
