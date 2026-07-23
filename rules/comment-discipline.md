# Comment Discipline

Default: write no comment. Good names, small functions, and clear control flow already say WHAT the code does. A comment exists only to add what the code cannot — a non-obvious WHY.

Comments and docstrings are not required, and a function without one is not unfinished. Clean code that needs no comment is the goal, not a gap waiting to be filled. Never add a comment or docstring just because one is missing — absence is the correct default, presence is the exception that must earn itself.

This applies everywhere: main-session edits, subagent-generated code, refactors, bug fixes. When delegating implementation, restate this rule in the briefing — weaker models regress to defensive commenting when the constraint isn't repeated.

## The only comments worth writing

Write a comment ONLY when it is one of these. The list is closed: if what you're about to write isn't clearly on it, delete it.

- **Hidden constraint / precondition** — an invariant this code assumes but can't show: `// caller holds the lock`, `// must run inside a transaction`.
- **Workaround** — why this odd code exists, with a link or issue so it can be retired when the upstream fix lands.
- **Surprising-but-correct** — code that looks wrong until you know the reason; state the reason.
- **Subtle invariant** — an ordering, idempotency, or numerical-precision assumption a reader could accidentally break.

Self-check: "If I delete this, would a careful reader be *confused or surprised*?" If no, delete it. The bar is confusion — not a bare-looking block.

## Everything else: no comment

Don't keep a catalog of forbidden comment types — that list never ends, and the next bad comment always slips between its entries. There is one rule: **not on the allowlist above → don't write it.**

The familiar ways code gets over-commented are not separate rules to memorize — they are all the same failure (not on the list): restating WHAT the next lines do, echoing the signature, narrating the task or PR, describing what a *caller or another layer* does with the result, scratchpad notes, gravestones for deleted code, section dividers. Don't enumerate them; just apply the list.

Signals you're drifting into defensive commenting: the block "felt bare," the comment paraphrases the next three lines, you're narrating to a hypothetical reviewer, or every function gets a docstring regardless. Notice it, delete it, trust the code.

## Rules

- No comment is the default, and a comment or docstring is never mandatory. Clean uncommented code is the finished state, not an incomplete one — never add one only because it's absent.
- A comment needs justification from the allowlist; silence needs none.
- When a comment is warranted, lead with WHY in one precise sentence.
- A comment documents THIS unit's own non-obvious facts — not a map of what callers or other layers do (that belongs in the PR body or commit message). A precondition the unit assumes is part of its own contract, so it stays.
- State each non-obvious fact once. Don't restate in a local comment what a file-header or adjacent comment already established — reference it or omit; a second copy drifts out of sync.
- When briefing a subagent for implementation, restate this rule — it is not reliably preserved through delegation.
- Same discipline for docstrings; signature paraphrase is noise. Carve-out: when language tooling enforces public-API docs (Go `revive`, Rust `missing_docs`, Python `pydocstyle`), a one-line contract description on exported identifiers is fine — describe the contract, not the signature.
