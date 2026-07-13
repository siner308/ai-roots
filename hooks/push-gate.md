# Push Gate Hook

A `PreToolUse` hook on `Bash` that forces a per-push human decision before `git push`, and denies force pushes outright.

## Why it exists

Pushing is the outward-facing moment of the git workflow: commits become visible to teammates (and, for a public repo, to everyone) and start being reviewed, pulled, and built on. Approval to push once does not extend to the next commit — but inside a long session, an earlier "push it" instruction reads like standing permission, and a broad Bash allowlist or permissive session mode executes the next push silently. The motivating incident was exactly that: freshly written work was pushed to a public repo on the momentum of an earlier push instruction, before the user had verified it.

A prompt rule cannot close this reliably — the model that misreads the earlier instruction as standing permission is the same model that would apply the rule. So the hook returns `permissionDecision: "ask"`, which surfaces a permission prompt to the human even when the command would otherwise be auto-approved. Verification-before-publication becomes a property of the harness, not of model judgment.

## What it does

- **`git push` (any remote, any form, including compound commands, `git -C dir push`, and `git subtree push`)** → `ask`: the user confirms this specific push, with a reason reminding that explicit instruction and pre-push verification should exist.
- **`git push --force` / `--force-with-lease` / `-f`** → `deny`: force pushes rewrite already-reviewed history; stacking commits is the required alternative.
- **`git push --dry-run` / `-n`** → allowed through: nothing is published.
- **Local-only lookalikes** (`git stash push`) → untouched: the pattern matches `push` only in git's subcommand position, so commands that merely contain the word publish nothing and pass through.
- **Non-push commands** (`git status`, `echo push`, `git log | grep push`) → untouched; the push pattern does not cross pipe or `;`/`&&` boundaries into other commands, and each push's flags (`--force`, `--dry-run`) are judged within its own command segment even when several pushes are chained.

## Per-repo opt-out

Some repos run autopilot-style, where a per-push prompt defeats the purpose; others hold careful design work, where the prompt is the point. The gate is therefore toggleable per repository via git config, which lives in `.git/config` — local to the clone, never committed, persistent across sessions:

```sh
git config ai-roots.push-gate off    # this repo: pushes skip the ask
git config --unset ai-roots.push-gate    # restore the gate (or set it to `on`)
```

Inside a Claude Code session, the `push-gate` skill wraps this: `/push-gate` toggles, `/push-gate on|off|status` sets or reads explicitly.

With the gate off the hook passes the push through without a decision rather than force-allowing it, so Claude Code's normal permission flow still applies: a permissive session mode pushes silently, while default mode still shows the standard Bash prompt. The force-push `deny` holds regardless of the toggle — protecting reviewed history is not a per-repo preference.

The toggle is read from the session's working directory, so a `git -C dir push` into a *different* repo is judged by the session repo's setting, not the target's.

## Known limitations (reviewed, accepted)

The principal is the model/user, not an attacker. A push wrapped in a script, alias, or `sh -c` string is not detected — the enforced path is the way the model actually pushes (a direct `git push` in a Bash call). `gh pr merge`, `git remote` manipulation, and other outward-facing operations are out of scope; each would need its own case for a reason as clear as this one.
