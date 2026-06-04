# Auto-Update Hook

A `SessionStart` hook that keeps a local ai-roots clone current by pulling
upstream and re-running `install.sh` when anything changed.

## Why it exists

The installer symlinks `rules/`, `skills/`, `agents/`, and `hooks/` straight into
`~/.claude`, so the clone *is* the live source. That makes updates trivial in
principle — `git pull` and you have the latest — but in practice people forget,
and the rules drift out of date silently. This hook closes that loop: every
ai-roots user receives updates without thinking about it.

## What it does

On session start it runs `hooks/auto-update.sh`, which:

1. Checks a throttle stamp (`~/.claude/.ai-roots/last-update`). If the last run
   was within the interval (default 24h), it exits immediately — so the cost on a
   typical session start is one `stat`, not a network round-trip.
2. When due, takes a lock, `git pull --ff-only` on the clone's current branch, and
   if `HEAD` moved, re-runs `install.sh` to relink new skills/agents and register
   new hooks.
3. Writes a one-line notice to stderr only when an update was actually applied.

Rule and skill **content** is live the moment the pull lands (the files are
symlinked). New **skills, agents, or hooks** only take effect on the *next*
session, because their symlinks and `settings.json` entries are read at startup.

## What it skips — fail-open by design

A failed update must never block or break a session, so every error path exits
0 and logs to `~/.claude/.ai-roots/update.log` instead of surfacing:

- **`git pull --ff-only`** — a clone with local commits or uncommitted changes is
  left untouched. If you've forked or edited the repo, updates quietly stop rather
  than clobber your work (check the log if you expected an update).
- **No `git`, not a repo, detached HEAD** — skipped.
- **Throttled / locked** — a run inside the interval, or a concurrent session
  already updating, exits without acting. A lock left by a killed run is cleared
  after an hour.

## Opt out

- `AI_ROOTS_AUTO_UPDATE=0` (or `false`/`no`/`off`) in the environment, or
- create `~/.claude/.ai-roots/disabled`.

Tune the cadence with `AI_ROOTS_UPDATE_INTERVAL` (seconds; default `86400`).

## Install and registration

`install.sh` runs `hooks/register.py`, which reads `hooks/manifest.json`, symlinks
the script into `~/.claude/hooks/`, and merges three `SessionStart` entries
(`startup`, `resume`, `clear`) into `~/.claude/settings.json`. The lock and
throttle make the duplicate triggers harmless — at most one pull per interval. The
merge is idempotent and backs up `settings.json` first.
