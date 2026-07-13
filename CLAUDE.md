# ai-roots

This repo is the source of the Claude Code rules, skills, agents, and hooks that
`install.sh` symlinks into `~/.claude`. Editing a file here changes Claude's
behavior on the next session.

## Authoring conventions

When writing or editing any `.md` under `rules/`, `skills/`, `agents/`, or
`hooks/` (and its Korean mirror):

- Use generic placeholders, never real product/company names or real PR numbers.
  Write `[Title of the spec or doc](url)` or `owner/repo#123`, not a concrete
  product, tool, or PR. The motivating case can live in a commit message or PR
  body, but the rule/skill text stays generic.
- Nothing from the machine-local `~/.claude/CLAUDE.md` leaks in: no org
  structure, team names, or product characteristics (e.g. which component
  consumes which API). ai-roots is org-agnostic — an example that only makes
  sense given the author's org must be rewritten in neutral terms.
- Write clean GitHub-flavored Markdown. No fixed-width padding (e.g. trailing
  spaces to an 82-column box) and no mid-sentence hard line breaks — one bullet
  is one line; let it soft-wrap. Use `-` bullets and fenced code blocks.
- English source files (`rules/`, `skills/`, `agents/`, `hooks/`) are written in
  English. Use another language only for content that is inherently
  language-specific — translationese examples, a Korean `~는/은` grammar
  illustration — never for explanatory prose that English can carry. The Korean
  mirror under `i18n/ko/` is where the full translation lives.
- In shell snippets a skill tells Claude to execute, prefix `command` on stock
  text/file utilities whose output is piped, redirected, or read back: `cat`,
  `ls`, `grep`, `find`, `diff`, `head`, `tail`, `less`, `tree`. These get
  aliased to renderers/colorizers (`glow`, `bat`, `eza`, `rg`, `delta`) that
  silently corrupt the consumed bytes. Don't blanket-prefix: `command` can't
  precede shell keywords (`if`/`for`/`{`) and is noise where there's no alias.
  Executed snippets only — not prose examples or commit messages.

## Hooks

`hooks/` holds hook scripts plus `manifest.json`, which declares how each one is
registered (event, matcher, command). `install.sh` runs `hooks/register.py`,
which symlinks every declared script into `~/.claude/hooks/` **and** merges its
entry into `~/.claude/settings.json`. The merge is idempotent and backs
settings.json up first, so re-running is safe. To add a hook: drop the script in
`hooks/`, add a `manifest.json` entry, re-run `install.sh`. Hook **scripts**
(`.py`/`.json`/`.sh`) have no Korean mirror — they are code. A hook's **doc** page
(`hooks/<name>.md`) does: mirror it as `i18n/ko/hooks/<name>.md`, same as a rule,
and `check-sync.sh` enforces it.

`hooks/comment-discipline.py` is a `PostToolUse` hook on `Edit|Write|MultiEdit`:
it detects comment lines an edit newly adds to a code file (pre-existing
comments excluded) and emits `decision: "block"` demanding a per-line verdict
against the `comment-discipline` allowlist, with delete as the default. It
enforces what a resident prose rule alone couldn't.

## Staying up to date

`shell/ai-roots-update.sh` is sourced from the user's interactive shell rc
(`install.sh` adds an idempotent marker block to `~/.zshrc`/`~/.bashrc`, backed up
first). Like oh-my-zsh, a new terminal does a throttled, read-only `git fetch`
(default 24h, via `~/.claude/.ai-roots/last-check`) and, if the clone is behind,
prompts before doing anything; on `yes` it runs `git pull --ff-only` then
`install.sh`. Nothing is pulled or executed without confirmation, and a
dirty/diverged clone is skipped. Opt out with `AI_ROOTS_AUTO_UPDATE=0`; tune the
cadence with `AI_ROOTS_UPDATE_INTERVAL` (seconds). The script lives in `shell/`
(not `hooks/`) because it is a shell-rc snippet, not a Claude Code hook, so it has
no Korean mirror.

## Keep the Korean mirror in sync — easy to miss

`rules/`, `skills/`, `agents/` are the **English source of truth** — the only
trees symlinked into `~/.claude` and loaded by Claude. `i18n/ko/` is a
**read-only Korean mirror** for humans; Claude never loads it.

Because the Korean copy lives in a separate tree, it is easy to forget when
editing a rule. So:

- When you **add, edit, rename, or delete** any `.md` file under `rules/`,
  `skills/`, `agents/`, or `hooks/`, make the matching change to
  `i18n/ko/<same path>` in the same commit. (Skills mirror as
  `i18n/ko/skills/<name>/SKILL.md`; `rules/_x.md` mirrors as
  `i18n/ko/rules/_x.md`; `hooks/<name>.md` mirrors as `i18n/ko/hooks/<name>.md`.)
  Hook scripts (`.py`/`.json`) are not mirrored.
- Run `./i18n/check-sync.sh` before committing — it reports any English file
  missing a Korean mirror, or an orphan mirror whose source is gone.
- Never change behavior by editing the Korean file. Fix the English source,
  then update the mirror to match.

## Docs site

`site/` is a VitePress site published to GitHub Pages
(https://siner308.github.io/ai-roots/) on every push to `main` that touches
`rules/`, `skills/`, `agents/`, `hooks/`, `i18n/`, or `site/`. It assembles both
languages at build time via `site/scripts/sync-content.mjs`; you don't edit
anything under `site/rules`, `site/skills`, etc. (those are generated and
git-ignored).
