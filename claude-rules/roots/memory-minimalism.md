# Memory Minimalism

The auto memory system stores entries on a single device's filesystem. It does not sync across machines, projects, or working contexts. When the same user works from multiple devices, alternates between main and side projects, or improves shared rule repositories from different environments, memory entries diverge silently — what was saved in one session is invisible in the next, and the asymmetry is undetectable from inside any single session.

Prefer durable, version-controlled artifacts (rule files, `CLAUDE.md`, project documentation) over memory entries whenever the content is reusable.

## When NOT to Use Memory

- **Conventions, principles, behavioral rules** — these belong in `claude-rules/roots/` (universal) or project `CLAUDE.md` (project-specific). Both are version-controlled and identical on every device.
- **Project facts that outlive the conversation** — these belong in the project's documentation, `CLAUDE.md`, or a dedicated rule file.
- **Authoring rules for shared repositories** — meta-rules about how to write rules belong in the repository itself, not in memory.
- **Anything that would benefit a teammate or a future session on another device** — by definition, memory cannot deliver it.
- **Repeated corrections** — if the same correction has been needed twice, it has earned a rule file. Do not let it accumulate as memory.

## When Memory Is Still Appropriate

- **Strictly personal, non-shareable context** — the user's role, working hours, or preferences they do not want in any shared file.
- **Ephemeral cross-conversation state with a clear expiration** — "user is mid-migration on X this week," dated explicitly.
- **References to external systems** too project-coupled for a shared rule file but too persistent to restate every conversation.

## Decision Order

When tempted to save a memory entry:

1. Could this be a rule in `claude-rules/roots/`? → write a rule instead.
2. Could this be a project `CLAUDE.md` or repo-local documentation entry? → write that instead.
3. Is it strictly personal and not shareable? → memory is appropriate.
4. Otherwise, default to NOT saving. Repeating the context next session is cheaper than letting devices diverge silently.

## Why

Memory's failure mode is silent. A guardrail captured on the work laptop simply does not exist on the home laptop. The user cannot see what is missing, so they cannot prompt the missing rule into existence. Version-controlled rule files eliminate this asymmetry — every device sees the same source of truth, and improvements propagate via `git pull`. Memory should be the exception, not the default surface for collaboration knowledge.

## Rules

- Prefer durable rules and project docs over memory for any content that is reusable, conventional, or shareable.
- Do not save the same correction twice — if it recurs, it belongs in a rule file.
- When migrating an existing memory entry into a rule, delete the memory afterwards to prevent drift between the two surfaces.
- When in doubt about whether memory is appropriate, ask the user where the content should live rather than defaulting to memory.
