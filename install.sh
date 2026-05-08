#!/bin/bash
# ai-roots installer
# Symlinks Claude rule directories into ~/.claude/rules/.
# Always installs roots/ and lessons/. Codex rules and commands are opt-in via --with-codex.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RULES_SRC="$SCRIPT_DIR/claude-rules"
RULES_DST="$HOME/.claude/rules"
LINK_NAME="ai-roots"
TARGET="$RULES_DST/$LINK_NAME"
WITH_CODEX=0

for arg in "$@"; do
  case "$arg" in
    --with-codex)
      WITH_CODEX=1
      ;;
    *)
      echo "usage: ./install.sh [--with-codex]"
      exit 1
      ;;
  esac
done

if [ ! -d "$RULES_SRC" ]; then
  echo "error: rule source not found: $RULES_SRC"
  exit 1
fi

mkdir -p "$RULES_DST"

# Migration: previous versions symlinked the entire claude-rules/ directory as
# $TARGET. Replace that single symlink with a real directory holding per-subdir
# symlinks so we can opt in/out of Codex rules independently.
if [ -L "$TARGET" ]; then
  echo "migrating from single symlink layout: $TARGET"
  rm "$TARGET"
fi
mkdir -p "$TARGET"

# Always link roots/ and lessons/. Codex rules sit under claude-rules/codex/ and
# are linked only with --with-codex, so non-Codex users do not load Codex policy.
for sub in roots lessons; do
  SUB_SRC="$RULES_SRC/$sub"
  SUB_TARGET="$TARGET/$sub"
  if [ -L "$SUB_TARGET" ]; then
    rm "$SUB_TARGET"
  elif [ -e "$SUB_TARGET" ]; then
    BACKUP="$SUB_TARGET.bak.$(date +%Y%m%d%H%M%S)"
    echo "backing up: $SUB_TARGET -> $BACKUP"
    mv "$SUB_TARGET" "$BACKUP"
  fi
  ln -s "$SUB_SRC" "$SUB_TARGET"
  echo "done. linked $SUB_SRC -> $SUB_TARGET"
done

CODEX_RULE_TARGET="$TARGET/codex"
COMMANDS_SRC="$SCRIPT_DIR/.claude/commands/codex"
COMMANDS_DST="$HOME/.claude/commands"
COMMANDS_TARGET="$COMMANDS_DST/codex"
AGENTS_SRC="$SCRIPT_DIR/.claude/agents/adversarial-reviewer.md"
AGENTS_DST="$HOME/.claude/agents"
AGENTS_TARGET="$AGENTS_DST/adversarial-reviewer.md"

if [ "$WITH_CODEX" -eq 1 ]; then
  CODEX_RULE_SRC="$RULES_SRC/codex"
  if [ ! -d "$CODEX_RULE_SRC" ]; then
    echo "error: Codex rules not found: $CODEX_RULE_SRC"
    exit 1
  fi
  if [ -L "$CODEX_RULE_TARGET" ]; then
    rm "$CODEX_RULE_TARGET"
  elif [ -e "$CODEX_RULE_TARGET" ]; then
    BACKUP="$CODEX_RULE_TARGET.bak.$(date +%Y%m%d%H%M%S)"
    echo "backing up: $CODEX_RULE_TARGET -> $BACKUP"
    mv "$CODEX_RULE_TARGET" "$BACKUP"
  fi
  ln -s "$CODEX_RULE_SRC" "$CODEX_RULE_TARGET"
  echo "done. linked $CODEX_RULE_SRC -> $CODEX_RULE_TARGET"

  if [ ! -d "$COMMANDS_SRC" ]; then
    echo "error: Codex commands not found: $COMMANDS_SRC"
    exit 1
  fi
  if [ ! -f "$AGENTS_SRC" ]; then
    echo "error: Codex reviewer agent not found: $AGENTS_SRC"
    exit 1
  fi

  mkdir -p "$COMMANDS_DST" "$AGENTS_DST"

  if [ -L "$COMMANDS_TARGET" ]; then
    rm "$COMMANDS_TARGET"
  elif [ -e "$COMMANDS_TARGET" ]; then
    BACKUP="$COMMANDS_TARGET.bak.$(date +%Y%m%d%H%M%S)"
    echo "backing up existing Codex commands: $COMMANDS_TARGET -> $BACKUP"
    mv "$COMMANDS_TARGET" "$BACKUP"
  fi

  if [ -L "$AGENTS_TARGET" ]; then
    rm "$AGENTS_TARGET"
  elif [ -e "$AGENTS_TARGET" ]; then
    BACKUP="$AGENTS_TARGET.bak.$(date +%Y%m%d%H%M%S)"
    echo "backing up existing reviewer agent: $AGENTS_TARGET -> $BACKUP"
    mv "$AGENTS_TARGET" "$BACKUP"
  fi

  ln -s "$COMMANDS_SRC" "$COMMANDS_TARGET"
  ln -s "$AGENTS_SRC" "$AGENTS_TARGET"
  echo "done. linked Codex commands -> $COMMANDS_TARGET"
  echo "done. linked Codex reviewer agent -> $AGENTS_TARGET"
else
  # Without --with-codex, remove any stale Codex symlinks left by prior runs.
  # If a real file/directory exists where a symlink would be, leave it alone but
  # warn — Claude Code may still load that content.
  if [ -L "$CODEX_RULE_TARGET" ]; then
    rm "$CODEX_RULE_TARGET"
    echo "removed stale Codex rules symlink: $CODEX_RULE_TARGET"
  elif [ -e "$CODEX_RULE_TARGET" ]; then
    echo "warning: $CODEX_RULE_TARGET is a real file/directory, not a symlink. Codex rules may still load. Remove it manually if intended."
  fi
  if [ -L "$COMMANDS_TARGET" ]; then
    rm "$COMMANDS_TARGET"
    echo "removed stale Codex commands symlink: $COMMANDS_TARGET"
  elif [ -e "$COMMANDS_TARGET" ]; then
    echo "warning: $COMMANDS_TARGET is a real file/directory, not a symlink. /codex:* commands may still load. Remove it manually if intended."
  fi
  if [ -L "$AGENTS_TARGET" ]; then
    rm "$AGENTS_TARGET"
    echo "removed stale Codex reviewer agent symlink: $AGENTS_TARGET"
  elif [ -e "$AGENTS_TARGET" ]; then
    echo "warning: $AGENTS_TARGET is a real file/directory, not a symlink. The reviewer agent may still load. Remove it manually if intended."
  fi
fi
