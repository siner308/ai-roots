# gh Markdown Style Hook

A `PreToolUse` hook on `Bash` that enforces GitHub-flavored Markdown on `gh` and GitHub-API writes, applying the [`github-pr-markdown`](../skills/github-pr-markdown) skill at the tool boundary instead of relying on the model to remember it.

## Why it exists

It started as a soft reminder (it printed the markdown rules before `gh pr/issue` commands), but two things still slipped through:

1. The model composed a PR body without invoking the skill — a prompt-level rule it can forget.
2. Even with the right format, `gh` CLI and shell heredocs silently corrupted the markdown (`- ` → `•`, backticks stripped, `- [ ]` → `[ ]`) *before* it was published, so the breakage was invisible until the rendered page looked wrong.

A reliability gap needs deterministic enforcement, not a better prompt. This hook is now a hard gate: it inspects the command about to run and blocks it when the body is delivered through a channel that corrupts, or when the body content is already broken.

## What it does

On every `Bash` call it checks whether the command writes a `gh` body (`gh pr create/edit/comment/review`, `gh issue create/edit/comment`) or hits the GitHub API for a PR/issue (`curl`/`gh api` to `/repos/OWNER/REPO/{pulls,issues}/N`). If so:

- **Channel rule** — a `gh` body that *contains markdown* is **blocked**. `gh` corrupts markdown in every body channel, and that happens inside `gh` after any content check, so the only fix is to forbid the channel: empty body, then PATCH via the API. A plain-text body (nothing to mangle) passes.
- **Content rule** — for the API path the body is extracted (curl `-d @file`/inline JSON, or `gh api -f body=`) and **validated**: no Unicode bullets, checkboxes carry a `- ` prefix, and a PR-resource body (`/pulls/N`) has `## Summary` + `## Test plan`.

A block (exit 2) feeds the reason back to the model, which then re-authors the body via the Write tool (heredocs mangle markdown in this shell) and PATCHes via the API.

## What it skips

- **Non-body commands** — `gh pr review --approve`, reviewer-only edits, anything with no body: no firing.
- **Plain-text bodies** — a short `gh pr comment -b "lgtm"` with no markdown passes; only markdown-bearing bodies are pushed to the API path.
- **Unlocatable bodies** — if a body payload can't be parsed it **fails open** (allows) rather than wedge an unfamiliar command shape. It blocks only on a positively-identified problem.
- **Uninspectable body sources** — a body from stdin (`--body-file -`, `gh api --input -`, `curl --data @-`), a shell variable, or command substitution (`--body "$(cat f)"`) is not expanded at hook time, so it passes. The enforced path is what the model actually uses: inline `--body "…"`, `--body-file <path>`, or `curl -d @file`.

## Known limitations (reviewed, accepted)

Surfaced in adversarial review and consciously left unenforced. The principal here is the model/user, not an attacker — so deliberate-evasion shapes carry no real risk, and the common paths are covered. Don't treat the gate as total.

- **Stdin bodies aren't validated** (see above) — fail-open on what can't be inspected, rather than fail-closed and wedge legitimate stdin workflows.
- **String mentions can over-block** — a command that only *names* a gh body command without running it (e.g. `echo gh pr create -b '- x'`) is matched by substring and may be blocked. Rephrase if it trips.
- **URL-valued non-endpoint flags** — a URL passed to a flag like `curl -e <url>` can mis-resolve the endpoint and skew the PR-section check. Not a shape used for GitHub writes.
- **`gh api graphql`** body mutations are out of scope (no `/pulls|issues/N` in the command).

## Install and registration

`install.sh` runs `hooks/register.py`, which reads `hooks/manifest.json`, symlinks the script into `~/.claude/hooks/`, and merges the hook entry into `~/.claude/settings.json`. The merge is idempotent and backs `settings.json` up first, so re-running is safe. No manual editing.
