# Comment Discipline Hook

A `PostToolUse` hook that enforces the [`comment-discipline`](../rules/comment-discipline) rule.

## Why it exists

`comment-discipline` is a resident rule — it sits in context every session. But a prose rule competes with everything else loaded there and loses to the strong prior that "documentation is helpful," so comments kept appearing anyway. Rewording the rule doesn't change that: a reliability gap needs deterministic enforcement, not a better prompt. This hook is that enforcement.

## What it does

After every `Edit`, `Write`, or `MultiEdit` on a **code file**, it diffs the comment lines the edit adds. When an edit introduces new comment lines, it demands a per-line verdict with **DELETE as the default**: a line survives only if the model can name which allowlist entry it is — a hidden constraint, a workaround (with link), surprising-but-correct code, or a subtle invariant. "It explains why" is not sufficient; the why must be one a careful reader could not recover from the code itself. When in doubt, delete. The sole carve-out is a one-line contract doc on an exported identifier that lint tooling enforces.

It emits `decision: "block"`, so the verdict is a prompt the model must answer — delete the noise or name each survivor's category — rather than background context it can skim past. (An earlier `additionalContext` version proved too easy to ignore: the model rationalized comments as "WHY comments" and kept them.) The tool call itself already ran; the block only forces the re-check, it does not undo the edit. Because it fires only on edits that actually add comments, it stays quiet once the habit holds — the better the discipline, the rarer the nudge.

## What it skips

- **Pre-existing comments** — only lines the edit newly adds are flagged (the old text is diffed out), so untouched comments never trigger it.
- **Non-code files** — Markdown, text, config: no firing. It keys off code file extensions (Go, TS/JS, Python, Rust, Java, and the rest of the C-style family).
- **Shebangs** and **comment markers inside strings** (e.g. a `https://` URL) — by design it matches whole comment lines, not trailing tokens, to keep false positives low.

## Install and registration

`install.sh` runs `hooks/register.py`, which reads `hooks/manifest.json`, symlinks the script into `~/.claude/hooks/`, and merges the hook entry into `~/.claude/settings.json`. The merge is idempotent and backs `settings.json` up first, so re-running is safe. No manual editing.

To add another hook: drop the script in `hooks/`, add a `manifest.json` entry (`event`, `matcher`, `script`, `run`), and re-run `install.sh`.
