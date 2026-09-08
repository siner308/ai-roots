# Comment Discipline

A comment exists only to add what the code cannot show: a non-obvious WHY. This applies to every edit: main-session, subagent-generated, refactors, bug fixes.

## Rules

- No comment is the default; a comment or docstring is never mandatory, and clean uncommented code is the finished state. Never add one only because it is absent.
- A comment needs justification from the closed allowlist below; silence needs none. Not clearly on the list means delete it.
- Self-check: without this comment, would a careful reader be confused or surprised? If no, delete it.
- When a comment is warranted, lead with WHY in one precise sentence.
- A comment documents THIS unit's own non-obvious facts, not what callers or other layers do (that belongs in the PR body or commit message). A precondition the unit assumes is part of its own contract and stays.
- State each non-obvious fact once; where a file header or adjacent comment already established it, reference that or leave the local comment out.
- Docstrings follow the same discipline; a signature paraphrase is noise. Where tooling enforces public-API docs (Go `revive`, Rust `missing_docs`, Python `pydocstyle`), a one-line contract description on exported identifiers is fine: describe the contract, not the signature.
- When briefing a subagent for implementation, restate this rule; it is not reliably preserved through delegation.

## The allowlist

- **Hidden constraint or precondition**: an invariant this code assumes but cannot show. `// caller holds the lock`, `// must run inside a transaction`.
- **Workaround**: why this odd code exists, with the link or issue that retires it once the upstream fix lands.
- **Surprising-but-correct**: code that looks wrong until you know the reason; state the reason.
- **Subtle invariant**: an ordering, idempotency, or numerical-precision assumption a reader could accidentally break.

## Drift signals

Restating WHAT the next lines do, echoing the signature, narrating the task or PR, scratchpad notes, gravestones for deleted code, section dividers: all one failure, not on the list.
You are drifting when the block "felt bare", the comment paraphrases the next three lines, you are narrating to a hypothetical reviewer, or every function gets a docstring regardless.

The `comment-discipline.py` hook enforces this on every comment an edit adds and checks that a multi-line comment breaks at meaning boundaries per `prose-style`.
