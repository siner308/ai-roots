#!/bin/bash
# ai-roots installer
# Symlinks rules into ~/.claude/rules/ai-roots/ and each skill subfolder into
# ~/.claude/skills/<skill-name>. Also links the adversarial-reviewer agent into
# ~/.claude/agents/.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RULES_SRC="$SCRIPT_DIR/rules"
SKILLS_SRC="$SCRIPT_DIR/skills"
AGENT_SRC="$SCRIPT_DIR/.claude/agents/adversarial-reviewer.md"

RULES_DST="$HOME/.claude/rules"
SKILLS_DST="$HOME/.claude/skills"
AGENTS_DST="$HOME/.claude/agents"

RULES_TARGET="$RULES_DST/ai-roots"
LEGACY_SKILLS_TARGET="$SKILLS_DST/ai-roots"
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

# Migration: previous versions linked the whole skills/ folder as
# ~/.claude/skills/ai-roots. Claude Code's skill loader expects
# ~/.claude/skills/<skill-name>/SKILL.md, so that layout was never picked up.
# Remove the legacy link if present.
if [ -L "$LEGACY_SKILLS_TARGET" ]; then
  echo "removing legacy skills symlink: $LEGACY_SKILLS_TARGET"
  rm "$LEGACY_SKILLS_TARGET"
elif [ -e "$LEGACY_SKILLS_TARGET" ]; then
  BACKUP="$LEGACY_SKILLS_TARGET.bak.$(date +%Y%m%d%H%M%S)"
  echo "backing up legacy skills dir: $LEGACY_SKILLS_TARGET -> $BACKUP"
  mv "$LEGACY_SKILLS_TARGET" "$BACKUP"
fi

# Link each skill subfolder individually so Claude Code recognizes each
# <skill-name>/SKILL.md.
for skill_dir in "$SKILLS_SRC"/*/; do
  [ -d "$skill_dir" ] || continue
  skill_name="$(basename "$skill_dir")"
  if [ ! -f "$skill_dir/SKILL.md" ]; then
    echo "skipping $skill_name: missing SKILL.md"
    continue
  fi
  skill_target="$SKILLS_DST/$skill_name"
  if [ -L "$skill_target" ]; then
    rm "$skill_target"
  elif [ -e "$skill_target" ]; then
    BACKUP="$skill_target.bak.$(date +%Y%m%d%H%M%S)"
    echo "backing up: $skill_target -> $BACKUP"
    mv "$skill_target" "$BACKUP"
  fi
  ln -s "${skill_dir%/}" "$skill_target"
  echo "linked skill: ${skill_dir%/} -> $skill_target"
done

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
