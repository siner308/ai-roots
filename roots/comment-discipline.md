# Comment Discipline

Default to writing no comments. Well-named identifiers, clear control flow, and small functions already tell the reader WHAT the code does. Comments are for the one thing the code cannot express — WHY something non-obvious is true.

This applies everywhere: main session edits, subagent-generated code, refactors, and bug fixes. When delegating implementation to a subagent, include this rule in the briefing — weaker models regress to defensive commenting habits when the constraint isn't restated.

## When a comment earns its place

A comment is worth writing when removing it would leave a future reader confused. Concretely:

- **Hidden constraint**: an invariant enforced elsewhere that isn't visible here (e.g., "caller holds the lock")
- **Workaround for a specific bug**: with a link or issue reference so the comment can be retired when the upstream fix lands
- **Surprising behavior**: code that looks wrong but is correct for a non-obvious reason
- **Subtle invariant**: ordering, idempotency, or numerical precision assumption that a reader might accidentally break

Self-check before writing: "If I delete this comment, would a careful reader be confused or surprised?" If no — don't write it.

## Forbidden comment patterns

These add noise without signal and should never be written:

- **WHAT restatements**: `// increment counter`, `// loop through users`, `// return the result`
- **Signature echoes in docstrings**: repeating parameter names, types, and return values that are already in the signature
- **Task-context references**: `// added for the X flow`, `// used by Y`, `// fixes issue #123`, `// as requested in review`. These belong in the PR description and git log, and they rot as the codebase evolves.
- **Removal traces**: `// removed old logic`, `// no longer needed`, `// deprecated — use X instead`. If it's removed, delete it; don't leave a gravestone.
- **Section dividers**: `// === Helpers ===`, `// --- Setup ---`. If the file needs signposting, it's too big — split it.
- **TODO/FIXME without an owner or ticket**: an untracked TODO is a promise nobody will keep. Either file it as an issue or don't write it.

## Tension with other habits

Defensive commenting often masquerades as thoroughness. Signals you're drifting into it:

- You're adding a comment because the block "felt bare" without one
- The comment paraphrases the next three lines
- You're narrating the current task to a hypothetical reviewer instead of documenting the code
- Every function has a docstring regardless of whether anything non-obvious happens inside

When you catch any signal, delete the comment and trust the code.

## Rules

- No comments is the default. Each comment requires justification; silence does not.
- When comments are warranted, lead with WHY. A single precise sentence beats a paragraph.
- Never reference the current task, PR, or caller in code comments — those contexts belong in the PR body or commit message, not the source.
- When briefing a subagent for implementation work, restate this rule. The base instruction is not reliably preserved through delegation.
- Apply the same discipline to docstrings. A docstring that only restates the signature is noise.
