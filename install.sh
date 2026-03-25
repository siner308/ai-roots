#!/bin/bash
# ai-roots installer
# Symlinks rules from this repo into ~/.claude/rules/

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RULES_SRC="$SCRIPT_DIR/rules"
RULES_DST="$HOME/.claude/rules"

mkdir -p "$RULES_DST"

for file in "$RULES_SRC"/*.md; do
  name="$(basename "$file")"
  target="$RULES_DST/$name"

  if [ -L "$target" ]; then
    echo "updating: $name"
    rm "$target"
  elif [ -f "$target" ]; then
    echo "backing up existing: $name -> $name.bak"
    mv "$target" "$target.bak"
  else
    echo "linking: $name"
  fi

  ln -s "$file" "$target"
done

echo "done. $(ls "$RULES_SRC"/*.md | wc -l | tr -d ' ') rules linked to $RULES_DST"