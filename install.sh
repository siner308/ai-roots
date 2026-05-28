#!/bin/bash
# ai-roots installer
# Symlinks rules into ~/.claude/rules/ai-roots/ and skills into ~/.claude/skills/ai-roots.
# Also links the adversarial-reviewer agent into ~/.claude/agents/.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RULES_SRC="$SCRIPT_DIR/rules"
SKILLS_SRC="$SCRIPT_DIR/skills"
AGENT_SRC="$SCRIPT_DIR/.claude/agents/adversarial-reviewer.md"

RULES_DST="$HOME/.claude/rules"
SKILLS_DST="$HOME/.claude/skills"
AGENTS_DST="$HOME/.claude/agents"

RULES_TARGET="$RULES_DST/ai-roots"
SKILLS_TARGET="$SKILLS_DST/ai-roots"
AGENT_TARGET="$AGENTS_DST/adversarial-reviewer.md"

if [ ! -d "$RULES_SRC" ]; then
  echo "error: rules source not found: $RULES_SRC"
  exit 1
fi
if [ ! -d "$SKILLS_SRC" ]; then
  echo "error: skills source not found: $SKILLS_SRC"
  exit 1
fi
if [ ! -f "$AGENT_SRC" ]; then
  echo "error: adversarial-reviewer agent not found: $AGENT_SRC"
  exit 1
fi

mkdir -p "$RULES_DST" "$SKILLS_DST" "$AGENTS_DST"

# Migration: previous versions used a single symlink for the entire claude-rules
# directory, or per-subdir symlinks under ~/.claude/rules/ai-roots/. Replace
# either layout with a single symlink to the new rules/ directory.
if [ -L "$RULES_TARGET" ]; then
  rm "$RULES_TARGET"
elif [ -d "$RULES_TARGET" ]; then
  BACKUP="$RULES_TARGET.bak.$(date +%Y%m%d%H%M%S)"
  echo "backing up existing rules dir: $RULES_TARGET -> $BACKUP"
  mv "$RULES_TARGET" "$BACKUP"
elif [ -e "$RULES_TARGET" ]; then
  BACKUP="$RULES_TARGET.bak.$(date +%Y%m%d%H%M%S)"
  echo "backing up: $RULES_TARGET -> $BACKUP"
  mv "$RULES_TARGET" "$BACKUP"
fi
ln -s "$RULES_SRC" "$RULES_TARGET"
echo "linked rules: $RULES_SRC -> $RULES_TARGET"

if [ -L "$SKILLS_TARGET" ]; then
  rm "$SKILLS_TARGET"
elif [ -e "$SKILLS_TARGET" ]; then
  BACKUP="$SKILLS_TARGET.bak.$(date +%Y%m%d%H%M%S)"
  echo "backing up: $SKILLS_TARGET -> $BACKUP"
  mv "$SKILLS_TARGET" "$BACKUP"
fi
ln -s "$SKILLS_SRC" "$SKILLS_TARGET"
echo "linked skills: $SKILLS_SRC -> $SKILLS_TARGET"

if [ -L "$AGENT_TARGET" ]; then
  rm "$AGENT_TARGET"
elif [ -e "$AGENT_TARGET" ]; then
  BACKUP="$AGENT_TARGET.bak.$(date +%Y%m%d%H%M%S)"
  echo "backing up: $AGENT_TARGET -> $BACKUP"
  mv "$AGENT_TARGET" "$BACKUP"
fi
ln -s "$AGENT_SRC" "$AGENT_TARGET"
echo "linked agent: $AGENT_SRC -> $AGENT_TARGET"

echo "done."
