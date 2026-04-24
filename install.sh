#!/bin/bash
# ai-roots installer
# Symlinks only Claude rule files into ~/.claude/rules/.

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

if [ -L "$TARGET" ]; then
  echo "updating symlink: $TARGET"
  rm "$TARGET"
elif [ -d "$TARGET" ]; then
  BACKUP="$TARGET.bak.$(date +%Y%m%d%H%M%S)"
  echo "backing up existing directory: $TARGET -> $BACKUP"
  mv "$TARGET" "$BACKUP"
fi

ln -s "$RULES_SRC" "$TARGET"
echo "done. linked $RULES_SRC -> $TARGET"

if [ "$WITH_CODEX" -eq 1 ]; then
  COMMANDS_SRC="$SCRIPT_DIR/.claude/commands/codex"
  COMMANDS_DST="$HOME/.claude/commands"
  COMMANDS_TARGET="$COMMANDS_DST/codex"
  AGENTS_SRC="$SCRIPT_DIR/.claude/agents/adversarial-reviewer.md"
  AGENTS_DST="$HOME/.claude/agents"
  AGENTS_TARGET="$AGENTS_DST/adversarial-reviewer.md"

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
fi
