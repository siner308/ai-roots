#!/usr/bin/env bash
# ai-roots auto-update, run from a SessionStart hook.
#
# Fail-open: every path exits 0 so a bad network or diverged clone never blocks a
# session. Stay silent on stdout — SessionStart stdout is injected into the
# session context; real output goes to the log file.
set -u

case "${AI_ROOTS_AUTO_UPDATE:-1}" in 0 | false | no | off) exit 0 ;; esac

# This script is symlinked into ~/.claude/hooks/, so resolve $0 back to the
# working tree before deriving the repo path.
SOURCE="${BASH_SOURCE[0]}"
while [ -L "$SOURCE" ]; do
  dir="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [ "${SOURCE#/}" = "$SOURCE" ] && SOURCE="$dir/$SOURCE"
done
HOOK_DIR="$(cd -P "$(dirname "$SOURCE")" >/dev/null 2>&1 && pwd)"
REPO="$(cd -P "$HOOK_DIR/.." >/dev/null 2>&1 && pwd)"

STATE="$HOME/.claude/.ai-roots"
mkdir -p "$STATE" 2>/dev/null || exit 0
STAMP="$STATE/last-update"
LOG="$STATE/update.log"
LOCK="$STATE/update.lock"
INTERVAL="${AI_ROOTS_UPDATE_INTERVAL:-86400}"

log() { printf '%s %s\n' "$(date '+%Y-%m-%dT%H:%M:%S')" "$*" >>"$LOG" 2>/dev/null; }

[ -f "$STATE/disabled" ] && exit 0

now="$(date +%s)"
if [ -f "$STAMP" ]; then
  last="$(cat "$STAMP" 2>/dev/null)"
  case "$last" in '' | *[!0-9]*) last=0 ;; esac
  [ "$((now - last))" -lt "$INTERVAL" ] && exit 0
fi

# Drop a lock left behind by a killed run (hook timeout) so it can't wedge forever.
[ -d "$LOCK" ] && [ -n "$(find "$LOCK" -maxdepth 0 -mmin +60 2>/dev/null)" ] && rmdir "$LOCK" 2>/dev/null
mkdir "$LOCK" 2>/dev/null || exit 0
trap 'rmdir "$LOCK" 2>/dev/null' EXIT

# Stamp before pulling so a broken remote backs off for the interval instead of
# retrying on every session start.
printf '%s\n' "$now" >"$STAMP" 2>/dev/null

command -v git >/dev/null 2>&1 || { log "git not found; skip"; exit 0; }
[ -d "$REPO/.git" ] || { log "no .git at $REPO; skip"; exit 0; }
git -C "$REPO" symbolic-ref -q HEAD >/dev/null || { log "detached HEAD; skip"; exit 0; }
git -C "$REPO" diff --quiet && git -C "$REPO" diff --cached --quiet || { log "local changes; skip"; exit 0; }

before="$(git -C "$REPO" rev-parse --short HEAD 2>/dev/null)"
if ! out="$(git -C "$REPO" pull --ff-only --quiet 2>&1)"; then
  log "pull skipped (ff-only): ${out:-diverged}"
  exit 0
fi
after="$(git -C "$REPO" rev-parse --short HEAD 2>/dev/null)"
[ "$before" = "$after" ] && { log "up to date ($after)"; exit 0; }

log "updated $before -> $after; running install.sh"
if inst="$(bash "$REPO/install.sh" 2>&1)"; then
  log "install.sh ok"
else
  log "install.sh failed: $inst"
fi

# New content is live now; new skills/agents/hooks only register next session.
printf 'ai-roots updated: %s -> %s (new skills/hooks apply next session)\n' "$before" "$after" >&2
exit 0
