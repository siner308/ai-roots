# Push Gate Hook

A `PreToolUse` hook on `Bash` that forces a per-push human decision before `git push`, and denies force pushes outright.

## Why it exists

Pushing is the outward-facing moment of the git workflow: commits become visible to teammates (and, for a public repo, to everyone) and start being reviewed, pulled, and built on. Approval to push once does not extend to the next commit — but inside a long session, an earlier "push it" instruction reads like standing permission, and a broad Bash allowlist or permissive session mode executes the next push silently. The motivating incident was exactly that: freshly written work was pushed to a public repo on the momentum of an earlier push instruction, before the user had verified it.

A prompt rule cannot close this reliably — the model that misreads the earlier instruction as standing permission is the same model that would apply the rule. So the hook returns `permissionDecision: "ask"`, which surfaces a permission prompt to the human even when the command would otherwise be auto-approved. Verification-before-publication becomes a property of the harness, not of model judgment.

## What it does

- **`git push` (any remote, any form, including compound commands and `git -C dir push`)** → `ask`: the user confirms this specific push, with a reason reminding that explicit instruction and pre-push verification should exist.
- **`git push --force` / `--force-with-lease` / `-f`** → `deny`: force pushes rewrite already-reviewed history; stacking commits is the required alternative.
- **`git push --dry-run` / `-n`** → allowed through: nothing is published.
- **Non-push commands** (`git status`, `echo push`, `git log | grep push`) → untouched; the push pattern does not cross pipe or `;`/`&&` boundaries into other commands.

## Known limitations (reviewed, accepted)

The principal is the model/user, not an attacker. A push wrapped in a script, alias, or `sh -c` string is not detected — the enforced path is the way the model actually pushes (a direct `git push` in a Bash call). `gh pr merge`, `git remote` manipulation, and other outward-facing operations are out of scope; each would need its own case for a reason as clear as this one.
