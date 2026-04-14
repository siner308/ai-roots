#!/bin/bash
# ai-roots installer
# Symlinks this repo into ~/.claude/rules/ so Claude Code loads all .md files recursively

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RULES_DST="$HOME/.claude/rules"
LINK_NAME="ai-roots"
TARGET="$RULES_DST/$LINK_NAME"

mkdir -p "$RULES_DST"

if [ -L "$TARGET" ]; then
  echo "updating symlink: $TARGET"
  rm "$TARGET"
elif [ -d "$TARGET" ]; then
  echo "backing up existing directory: $TARGET -> $TARGET.bak"
  mv "$TARGET" "$TARGET.bak"
fi

ln -s "$SCRIPT_DIR" "$TARGET"
echo "done. linked $SCRIPT_DIR -> $TARGET"
