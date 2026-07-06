# ai-roots update check — sourced from an interactive shell rc (~/.zshrc, ~/.bashrc).
# Mirrors oh-my-zsh: on a new terminal, throttled, asks before pulling. Nothing is
# pulled or executed without a "yes" at the prompt. Repo path comes from $AI_ROOTS_DIR,
# set by install.sh in the rc line that sources this file.

ai_roots_update_check() {
  # Interactive shells only — a script or CI that sources the rc must never block on read.
  case "$-" in *i*) ;; *) return 0 ;; esac
  case "${AI_ROOTS_AUTO_UPDATE:-1}" in 0 | false | no | off) return 0 ;; esac

  local repo="${AI_ROOTS_DIR:-}"
  [ -n "$repo" ] && [ -d "$repo/.git" ] || return 0
  command -v git >/dev/null 2>&1 || return 0

  local state="$HOME/.claude/.ai-roots"
  local stamp="$state/last-check"
  local interval="${AI_ROOTS_UPDATE_INTERVAL:-86400}"
  mkdir -p "$state" 2>/dev/null || return 0

  local now last
  now="$(date +%s)"
  last="$(cat "$stamp" 2>/dev/null || echo 0)"
  case "$last" in '' | *[!0-9]*) last=0 ;; esac
  [ "$((now - last))" -lt "$interval" ] && return 0
  # Stamp before fetching so an unreachable remote backs off for the interval
  # instead of probing the network on every new terminal.
  printf '%s\n' "$now" >"$stamp" 2>/dev/null

  # Read-only: fetch moves remote-tracking refs without touching the worktree.
  git -C "$repo" fetch --quiet 2>/dev/null || return 0
  local upstream behind
  upstream="$(git -C "$repo" rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null)" || return 0
  behind="$(git -C "$repo" rev-list --count "HEAD..$upstream" 2>/dev/null || echo 0)"
  case "$behind" in '' | *[!0-9]*) behind=0 ;; esac
  [ "$behind" -gt 0 ] || return 0

  # ff-only can't apply over local edits or a diverged branch, so don't offer it.
  if ! git -C "$repo" diff --quiet 2>/dev/null || ! git -C "$repo" diff --cached --quiet 2>/dev/null; then
    printf '[ai-roots] %s update(s) available, but the repo has local changes — skipping.\n' "$behind"
    return 0
  fi

  printf '[ai-roots] %s update(s) available. Apply now? [Y/n] ' "$behind"
  local reply="" ok=0
  # Single keystroke, no Enter needed — the flag is -k in zsh, -n in bash.
  if [ -n "${ZSH_VERSION:-}" ]; then
    read -r -k 1 reply && ok=1
  elif [ -n "${BASH_VERSION:-}" ]; then
    read -r -n 1 reply && ok=1
  else
    read -r reply && ok=1
  fi
  # A failed read means EOF / no TTY — never fall through to the yes-default.
  if [ "$ok" -ne 1 ]; then
    printf '\n[ai-roots] no input; skipped.\n'
    return 0
  fi
  # Enter already echoed its own newline; any other key leaves the cursor mid-line.
  case "$reply" in '' | $'\n') ;; *) printf '\n' ;; esac
  case "$reply" in
    '' | $'\n' | y | Y)
      if git -C "$repo" pull --ff-only && bash "$repo/install.sh"; then
        printf '[ai-roots] updated.\n'
      else
        printf '[ai-roots] update failed — run %s/install.sh manually.\n' "$repo"
      fi
      ;;
    *)
      printf '[ai-roots] skipped. Later: git -C %s pull --ff-only && %s/install.sh\n' "$repo" "$repo"
      ;;
  esac
}

ai_roots_update_check
