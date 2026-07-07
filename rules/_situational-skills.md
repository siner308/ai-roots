# Situational Skills Index

Some rules apply only in specific task contexts (CSS, PRs, Codex, parallelism, a debugging lesson). To keep the always-resident rule set small, their full bodies were moved into skills under `ai-roots/skills/<name>/` and load on demand via the Skill tool. Only their one-line descriptions sit in context by default.

This index is the resident half: it stays loaded so the *trigger* is never forgotten even though the *body* is lazy. When a row's condition holds, invoke that skill **before** acting on the matching work — treat it as a binding rule, not a suggestion. Lazy loading is a context optimization; it does not lower the rule's priority.

| When this holds | Invoke skill |
|-----------------|--------------|
| Editing, writing, or reviewing CSS or any framework styling (Tailwind, CSS Modules, scoped styles, inline `style`, CSS-in-JS) | `css-discipline` |
| Composing or editing a PR body or title (`gh pr create`, `gh pr edit`, `gh api` PR updates) | `github-pr-markdown` |
| Deciding executor (main vs subagent vs team), model (Fable/Opus/Sonnet/Haiku), or effort before delegating non-trivial work | `model-effort-delegation` |
| Choosing sequential vs subagent vs team, or inline vs subagent, or foreground vs background | `parallel-execution-modes` |
| A problem has multiple plausible causes across layers, or output must pass multiple independent judgment criteria | `parallel-hypothesis-investigation` |
| Delegating to the OpenAI Codex CLI — rescue debugging, cross-provider review, current-docs research, or bounded implementation (Codex on `PATH`) | `codex-delegation` |
| Task outcome is uncertain — external API, browser automation, shell escaping, unfamiliar library, data pipeline | `incremental-verification` |
| Porting, debugging, or implementing against code you have read but not run | `simulate-dont-just-scan` |
| A long-running task runs in the background and the user needs completion or progress visibility — or you are tempted to monitor a subprocess via tmux split panes, sentinel strings, or a foreground tail/grep loop | `background-task-monitoring` |
| Browsing the web, extracting page content, scraping data, or fetching figures from sites — including when agent-browser returns blocked/empty/dynamic content and you are tempted to retry with another engine or guess sibling URLs | `web-research` |

## Rules

- When a trigger fires, invoking the matching skill is mandatory, not discretionary.
- A lazy skill carries the same authority as a resident rule — its body simply loads when needed instead of always.
- If you find yourself doing one of the triggered activities without having loaded its skill, stop and load it.
