# Terminology Discipline

Spell out domain terms. Abbreviations that feel obvious to the author are ambiguous to readers, and they collide with other domain terms in ways that silently flip meaning.

## Three Categories

| Category | Treatment | Examples |
|----------|-----------|----------|
| **Industry-standard abbreviations** | Use as-is | `env`, `prod`, `dev`, `repo`, `svc`, `db`, `api`, `url`, `id`, `auth`, `config`, `ctx`, `req`, `res` |
| **Established domain terms** | Keep the abbreviation, but expand on first use | Project-specific abbreviations already entrenched in the codebase or team vocabulary |
| **Ad-hoc abbreviations** | Forbidden | `usrCnt` → `userCount`, `prodInfo` → `productInfo`, `memInfo` → `memberInfo` |

An abbreviation qualifies as industry-standard only if it appears in the same form across external sources — official documentation, language specs, widely-used libraries. Internal company shorthand is a domain term, not an industry standard.

## Collision Signals

When an abbreviation could be misread as a different domain concept, spell it out or qualify it.

- `uid` — user id or unique id?
- `pid` — process id, player id, or product id?
- `mid` — member id, message id, middleware id, or something else entirely?

If an abbreviation has two or more plausible readings, expand it (`userId`, `processId`, `messageId`) or attach a qualifier that disambiguates.

## Scope

- **New identifiers** — default to spelled-out names for variables, functions, and types. Industry-standard abbreviations are allowed.
- **User-facing explanations** — when referencing an established domain term, expand it on first use ("X (what it means in this domain)"), then the short form is fine.
- **Documentation and comments** — disambiguate collision-prone abbreviations with a qualifier.
- **Editing existing code** — do NOT bulk-rename established abbreviations to spell them out. Codebase consistency outweighs the rule.

## Rules

- New identifiers default to spelled-out form. Abbreviate only when the term is industry-standard or already established in the domain.
- Established domain abbreviations: expand on first use, then the short form is acceptable.
- Collision-prone abbreviations: add a qualifier or expand to remove ambiguity.
- Preserve existing codebase conventions — do not partially expand an entrenched abbreviation.
