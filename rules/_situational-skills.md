# Situational Skills Index

Some rules apply only in specific task contexts (CSS, PRs, Codex, parallelism, a debugging lesson). To keep the always-resident rule set small, their full bodies were moved into skills under `ai-roots/skills/<name>/` and load on demand when the harness invokes them. Only their one-line descriptions sit in context by default.

This index is the resident half: it stays loaded so the *trigger* is never forgotten even though the *body* is lazy. When a row's condition holds, invoke that skill **before** acting on the matching work — treat it as a binding rule, not a suggestion. Lazy loading is a context optimization; it does not lower the rule's priority.

| When this holds | Invoke skill |
|-----------------|--------------|
| Editing, writing, or reviewing CSS or any framework styling (Tailwind, CSS Modules, scoped styles, inline `style`, CSS-in-JS) | `css-discipline` |
| Composing or editing a PR body or title (`gh pr create`, `gh pr edit`, `gh api` PR updates) | `github-pr-markdown` |
| Deciding executor (main vs subagent vs team), model (Opus/Sonnet/Haiku), or effort before delegating non-trivial work | `model-effort-delegation` |
| Choosing sequential vs subagent vs team, or inline vs subagent, or foreground vs background | `parallel-execution-modes` |
| A problem has multiple plausible causes across layers, or output must pass multiple independent judgment criteria | `parallel-hypothesis-investigation` |
| Delegating to the OpenAI Codex CLI — rescue debugging, cross-provider review, current-docs research, or bounded implementation (Codex on `PATH`) | `codex-delegation` |
| The request asks to draw, generate, or make an image, or names a missing `.png`/`.jpg`/`.webp` asset to create (Codex on `PATH`) | `codex-imagegen` |
| Writing code against something you cannot see from here — external API, browser, tricky shell quoting, unfamiliar library, data pipeline | `incremental-verification` |
| Porting or rewriting code between languages/frameworks, or answering what existing code does at runtime | `simulate-dont-just-scan` |
| A long-running task runs in the background and the user needs completion or progress visibility — or you are tempted to monitor a subprocess via tmux split panes, sentinel strings, or a foreground tail/grep loop | `background-task-monitoring` |
| Browsing the web, extracting page content, scraping data, or fetching figures from sites — including when agent-browser returns blocked/empty/dynamic content and you are tempted to retry with another engine or guess sibling URLs | `web-research` |
| About to save a memory entry, or weighing whether a fact belongs in memory vs a version-controlled surface (rule, `CLAUDE.md`, project doc) | `memory-minimalism` |
| A request hands you three or more items to process the same way — fields, env vars, endpoints, records, files, test cases — or a batch edit across many sites. The count triggers it, not how uniform the items look | `verify-each-instance` |
| The user says or implies this is a repeat ("again", "세 번째인데"), or their request omitted something you had to ask for or guess | `user-growth-coaching` |

Two rows exist to reach a *different* provider: `codex-delegation` and `codex-imagegen` hand work to the Codex CLI. They fire only in a harness that is not Codex — inside Codex the work is already there, so do it directly.

## When a skill and the user disagree

A skill binds within its scope, and the user's explicit instruction in the session outranks it. When the two conflict, follow the user and say which skill line you set aside.

Unclear or conflicting skill guidance makes a model stop early — asking for confirmation, leaving requested work unfinished, or drifting from what was asked. When a skill does that to you, name the skill file, quote the line, and say whether it requires the pause or you read it that way. A silent pause looks like a model failure; a quoted line is something the user can fix.

## Rules

- When a trigger fires, invoking the matching skill is mandatory, not discretionary.
- A lazy skill carries the same authority as a resident rule — its body simply loads when needed instead of always.
- If you find yourself doing one of the triggered activities without having loaded its skill, stop and load it.
- The user's explicit instruction outranks a skill's; on conflict, follow the user and name the skill line you set aside.
- When a skill makes you pause, ask for confirmation, leave requested work unfinished, or change direction, name the skill file, quote the exact line, and separate what it requires from how you interpreted it.
