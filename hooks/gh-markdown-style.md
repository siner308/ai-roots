# gh Markdown Style Hook

A `PreToolUse` hook on `Bash` that blocks the one PR-markdown failure the [`github-pr-markdown`](../skills/github-pr-markdown) skill can't prevent on its own: `gh` CLI corrupting the body before it's published.

## Why it exists

It started as a soft reminder that printed the markdown rules before `gh pr/issue` commands. That wasn't enough on its own — but the durable reason it's a gate is narrower than "the model forgets the skill":

Even when the model follows the skill perfectly, `gh` CLI corrupts markdown in every body channel (`- ` → `•`, backticks stripped, `- [ ]` → `[ ]`), and that corruption happens *inside* `gh`, after the model has already done everything right. A prompt rule can't fix a corruption that happens past the prompt. Only a gate can.

So this hook enforces exactly that — the channel — and nothing else. Bullet/checkbox/section formatting, body length, and structure are the skill's job. The hook used to re-validate those too, which is what let the hook and the skill drift apart (the hook hard-required `## Summary` + `## Test plan` long after the skill moved to "short by default, follow the repo template"). A rule written in two places diverges; this one lives in the skill.

## What it does

On every `Bash` call it checks whether the command writes a `gh` body (`gh pr create/edit/comment/review`, `gh issue create/edit/comment`). If that body *contains markdown*, it's **blocked** — the body must be created empty and then PATCHed via the GitHub API. A plain-text body (nothing for `gh` to mangle) passes.

A block (exit 2) feeds the reason back to the model, pointing it at the `github-pr-markdown` skill for how to author and deliver the body.

## What it skips

- **Non-body commands** — `gh pr review --approve`, reviewer-only edits, anything with no body: no firing.
- **Plain-text bodies** — a short `gh pr comment -b "lgtm"` with no markdown passes; only markdown-bearing bodies are blocked.
- **The API path itself** — a `curl`/`gh api` PATCH is the *fix* this hook steers toward, so it isn't gated. Body content on that path (bullets, sections, links) is the skill's responsibility, not re-validated here.
- **Unlocatable / uninspectable bodies** — a body that can't be parsed, or comes from stdin (`--body-file -`), a shell variable, or command substitution (`--body "$(cat f)"`), is not expanded at hook time, so it **fails open** (allows) rather than wedge an unfamiliar command shape. The enforced path is what the model actually uses: inline `--body "…"` or `--body-file <path>`.

## Known limitations (reviewed, accepted)

The principal here is the model/user, not an attacker — so deliberate-evasion shapes carry no real risk, and the common paths are covered. Don't treat the gate as total.

- **Stdin / variable bodies aren't inspected** (see above) — fail-open on what can't be read at hook time, rather than fail-closed and wedge legitimate workflows.
- **String mentions can over-block** — a command that only *names* a gh body command without running it (e.g. `echo gh pr create -b '- x'`) is matched by substring and may be blocked. Rephrase if it trips.

## Install and registration

`install.sh` runs `hooks/register.py`, which reads `hooks/manifest.json`, symlinks the script into `~/.claude/hooks/`, and merges the hook entry into `~/.claude/settings.json`. The merge is idempotent and backs `settings.json` up first, so re-running is safe. No manual editing.
