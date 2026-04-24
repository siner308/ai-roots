#!/bin/bash
# ai-roots installer
# Symlinks only Claude rule files into ~/.claude/rules/.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RULES_SRC="$SCRIPT_DIR/claude-rules"
RULES_DST="$HOME/.claude/rules"
LINK_NAME="ai-roots"
TARGET="$RULES_DST/$LINK_NAME"

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
