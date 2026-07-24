# ai-roots

This repo is the source of the Claude Code rules, skills, agents, and hooks that `install.sh` symlinks into `~/.claude`.
Editing a file here changes Claude's behavior on the next session.

## Authoring conventions

When writing or editing any `.md` in this repo (including this file, the READMEs, and the Korean mirror):

- Use generic placeholders, never real product/company names or real PR numbers. Write `[Title of the spec or doc](url)` or `owner/repo#123`, not a concrete product, tool, or PR. The motivating case can live in a commit message or PR body, but the rule/skill text stays generic.
- Nothing from the machine-local `~/.claude/CLAUDE.md` leaks in: no org structure, team names, or product characteristics (e.g. which component consumes which API). ai-roots is org-agnostic — an example that only makes sense given the author's org must be rewritten in neutral terms.
- Fictional examples must also avoid the org's real *business domains*: a made-up service in a business area the org actually works in still reveals what the org does. Set examples in distant domains (a library, an observatory, a greenhouse), not adjacent ones with the names swapped.
- Never hard-break mid-sentence, unless a linter or formatter errors on the width. A hard break may fall only where a sentence ends — and is never required there; a line holding several sentences is fine. A file's incumbent hard-wrap style is not a width limit and gets re-flowed on edit, not imitated. No fixed-width padding (e.g. trailing spaces to an 82-column box). Use `-` bullets and fenced code blocks. Enforced by the `prose-discipline.py` hook.
- English source files (`rules/`, `skills/`, `agents/`, `hooks/`) are written in English. Use another language only for content that is inherently language-specific — translationese examples, a Korean `~는/은` grammar illustration — never for explanatory prose that English can carry. The Korean mirror under `i18n/ko/` is where the full translation lives.
- In shell snippets a skill tells Claude to execute, prefix `command` on stock text/file utilities whose output is piped, redirected, or read back: `cat`, `ls`, `grep`, `find`, `diff`, `head`, `tail`, `less`, `tree`. These get aliased to renderers/colorizers (`glow`, `bat`, `eza`, `rg`, `delta`) that silently corrupt the consumed bytes. Prefix only where an alias actually applies: `command` can't precede shell keywords (`if`/`for`/`{`) and is noise where there's no alias. Executed snippets only — not prose examples or commit messages.
- Write each directive as the action to take, so a reader can act on the sentence alone — `Open the PR as ready`, rather than `Don't open a draft PR` (which leaves the move unstated: ready it, or open none at all?). Phrase rules, skills, and docs as positive directives. Keep a crisp negative where it guards a bright-line hazard (security, data loss, irreversible action) or names the exact anti-pattern the rule exists to prevent — there the prohibition instructs an LLM more reliably; state the positive action and hold the negative alongside it.

## Hooks

`hooks/` holds hook scripts plus `manifest.json`, which declares how each one is registered (event, matcher, command).
`install.sh` runs `hooks/register.py`, which symlinks every declared script into `~/.claude/hooks/` **and** merges its entry into `~/.claude/settings.json`.
The merge is idempotent and backs settings.json up first, so re-running is safe.
To add a hook: drop the script in `hooks/`, add a `manifest.json` entry, re-run `install.sh`.
Hook **scripts** (`.py`/`.json`/`.sh`) have no Korean mirror — they are code.
A hook's **doc** page (`hooks/<name>.md`) does: mirror it as `i18n/ko/hooks/<name>.md`, same as a rule, and `check-sync.sh` enforces it.

`hooks/comment-discipline.py` is a `PostToolUse` hook on `Edit|Write|MultiEdit`: it detects comment lines an edit newly adds to a code file (pre-existing comments excluded) and emits `decision: "block"` demanding a per-line verdict against the `comment-discipline` allowlist, with delete as the default.
When an added comment spans multiple lines it also asks the model to check that each break falls at a meaning boundary, not mid-phrase — the code-comment side of line-break discipline, judged by the model so it works in any language.
`hooks/prose-discipline.py` is the non-code counterpart on the same event: on Markdown it flags mid-sentence hard breaks and, past a sentence-count gate, asks for a conciseness pass. The two never double-fire — code edits hit `comment-discipline`, Markdown edits hit `prose-discipline`.
Both enforce what a resident prose rule alone couldn't.
`hooks/grounded-assertions.py` is a `Stop` hook: when a turn's final message passes a sentence-count gate, it blocks once (`stop_hook_active` caps the loop) and demands a claim-by-claim audit — evidenced claims stay untouched, verifiable ones get verified now, the rest get their uncertainty markers restored. It is the enforcement layer for the `grounded-assertions` rule; `/fact-check` (skill) toggles it or tunes the gate, and `AI_ROOTS_FACT_CHECK=0` is the emergency off switch.

## Writing discipline: three layers, one concern

Rules on how to write are spread across three layers on purpose — a rule holds the knowledge, a hook enforces it, a skill carries the situational case.
This is not accidental scatter: a resident rule competes with the whole context and loses under pressure, and a hook is the only layer that runs after an edit to force a correction — so anything that must hold every time needs one, not a better-worded rule.
Use this map to find where a writing concern lives before changing it.

| Concern | Knowledge (rule) | Enforcement (hook) | Situational (skill) |
|---------|------------------|--------------------|---------------------|
| Comment existence | `comment-discipline` | `comment-discipline.py` | — |
| Code-comment line breaks | `prose-style` | `comment-discipline.py` (multi-line comments) | — |
| Markdown line breaks | `prose-style` | `prose-discipline.py` | — |
| Doc conciseness | `prose-style` | `prose-discipline.py` (sentence gate) | — |
| Plain language, noun-stacks, translationese | `prose-style` | — (not statically detectable) | — |
| Korean naturalness + voice (loanwords, translationese, rhythm; first-person, motivation-first, honest) | `korean-style` | — (chat: rule-only) | — |
| Terminology, abbreviations | `terminology-discipline` | — | — |
| Ungrounded assertions (hedge-stripping) | `grounded-assertions` | `grounded-assertions.py` (Stop, sentence gate) | — |
| PR body format and delivery | — | `gh-markdown-style.py` (delivery only) | `github-pr-markdown` |

A blank enforcement cell means the concern is rule-only: it can't be detected statically, so it rides on the resident rule.
When a criterion changes, the rule is the source of truth; a hook that also restates that criterion (`comment-discipline`, `prose-discipline`) has to be updated alongside it, or the two drift — the known cost of keeping the hook message self-contained instead of a bare pointer.

## Staying up to date

`shell/ai-roots-update.sh` is sourced from the user's interactive shell rc (`install.sh` adds an idempotent marker block to `~/.zshrc`/`~/.bashrc`, backed up first).
Like oh-my-zsh, a new terminal does a throttled, read-only `git fetch` (default 24h, via `~/.claude/.ai-roots/last-check`) and, if the clone is behind, prompts before doing anything; on `yes` it runs `git pull --ff-only` then `install.sh`.
Nothing is pulled or executed without confirmation, and a dirty/diverged clone is skipped.
Opt out with `AI_ROOTS_AUTO_UPDATE=0`; tune the cadence with `AI_ROOTS_UPDATE_INTERVAL` (seconds).
The script lives in `shell/` (not `hooks/`) because it is a shell-rc snippet, not a Claude Code hook, so it has no Korean mirror.

## Keep the Korean mirror in sync — easy to miss

`rules/`, `skills/`, `agents/` are the **English source of truth** — the only trees symlinked into `~/.claude` and loaded by Claude.
`i18n/ko/` is a **read-only Korean mirror** for humans; Claude never loads it.

Because the Korean copy lives in a separate tree, it is easy to forget when editing a rule. So:

- When you **add, edit, rename, or delete** any `.md` file under `rules/`, `skills/`, `agents/`, or `hooks/`, make the matching change to `i18n/ko/<same path>` in the same commit. (Skills mirror as `i18n/ko/skills/<name>/SKILL.md`; `rules/_x.md` mirrors as `i18n/ko/rules/_x.md`; `hooks/<name>.md` mirrors as `i18n/ko/hooks/<name>.md`.) Hook scripts (`.py`/`.json`) are not mirrored.
- Run `./i18n/check-sync.sh` before committing — it reports any English file missing a Korean mirror, or an orphan mirror whose source is gone.
- Never change behavior by editing the Korean file. Fix the English source, then update the mirror to match.

## Docs site

`site/` is a VitePress site published to GitHub Pages (https://siner308.github.io/ai-roots/) on every push to `main` that touches `rules/`, `skills/`, `agents/`, `hooks/`, `i18n/`, or `site/`.
It assembles both languages at build time via `site/scripts/sync-content.mjs`; you don't edit anything under `site/rules`, `site/skills`, etc. (those are generated and git-ignored).
