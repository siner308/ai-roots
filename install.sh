#!/bin/bash
# ai-roots installer
# Symlinks rules into ~/.claude/rules/ai-roots/, each skill subfolder into
# ~/.claude/skills/<skill-name>, each agent file into ~/.claude/agents/, and
# each hook script into ~/.claude/hooks/. Hook *scripts* are linked here, but
# their registration lives in ~/.claude/settings.json — see README.

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
RULES_SRC="$SCRIPT_DIR/rules"
SKILLS_SRC="$SCRIPT_DIR/skills"
AGENTS_SRC="$SCRIPT_DIR/agents"
HOOKS_SRC="$SCRIPT_DIR/hooks"

RULES_DST="$HOME/.claude/rules"
SKILLS_DST="$HOME/.claude/skills"
AGENTS_DST="$HOME/.claude/agents"

RULES_TARGET="$RULES_DST/ai-roots"
LEGACY_SKILLS_TARGET="$SKILLS_DST/ai-roots"

# Only dangling links resolving into $SCRIPT_DIR are removed, so a user's own or
# another tool's links are never touched.
prune_orphans() {
  dir="$1"
  [ -d "$dir" ] || return 0
  for link in "$dir"/*; do
    [ -L "$link" ] || continue
    case "$(readlink "$link")" in
      "$SCRIPT_DIR"/*)
        [ -e "$link" ] || { rm "$link" && echo "pruned orphaned link: $link"; }
        ;;
    esac
  done
}

if [ ! -d "$RULES_SRC" ]; then
  echo "error: rules source not found: $RULES_SRC"
  exit 1
fi
if [ ! -d "$SKILLS_SRC" ]; then
  echo "error: skills source not found: $SKILLS_SRC"
  exit 1
fi
if [ ! -d "$AGENTS_SRC" ]; then
  echo "error: agents source not found: $AGENTS_SRC"
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
prune_orphans "$SKILLS_DST"

# Link each agent file individually so Claude Code recognizes each
# ~/.claude/agents/<agent-name>.md. The adversarial-reviewer agent previously
# lived under .claude/agents/ in this repo; the legacy symlink target is the
# same path, so the loop below transparently refreshes it.
for agent_file in "$AGENTS_SRC"/*.md; do
  [ -f "$agent_file" ] || continue
  agent_name="$(basename "$agent_file")"
  agent_target="$AGENTS_DST/$agent_name"
  if [ -L "$agent_target" ]; then
    rm "$agent_target"
  elif [ -e "$agent_target" ]; then
    BACKUP="$agent_target.bak.$(date +%Y%m%d%H%M%S)"
    echo "backing up: $agent_target -> $BACKUP"
    mv "$agent_target" "$BACKUP"
  fi
  ln -s "$agent_file" "$agent_target"
  echo "linked agent: $agent_file -> $agent_target"
done
prune_orphans "$AGENTS_DST"

# Hooks need a JSON merge into settings.json, so register.py handles both the
# symlinking and the registration (declared in hooks/manifest.json). It is
# idempotent and backs settings.json up before writing.
if [ -f "$HOOKS_SRC/manifest.json" ]; then
  python3 "$HOOKS_SRC/register.py" "$HOOKS_SRC" "$HOME"
fi

# Source the update checker from the user's interactive shell rc so a new terminal
# offers updates (oh-my-zsh style). Idempotent via a marker block; rc is backed up.
UPDATE_SRC="$SCRIPT_DIR/shell/ai-roots-update.sh"
if [ -f "$UPDATE_SRC" ]; then
  case "${SHELL##*/}" in
    bash) RC="$HOME/.bashrc" ;;
    *) RC="$HOME/.zshrc" ;;
  esac
  MARKER="# >>> ai-roots update check >>>"
  if [ -f "$RC" ] && grep -qF "$MARKER" "$RC"; then
    echo "shell update check already present in $RC"
  else
    [ -f "$RC" ] && cp "$RC" "$RC.bak.$(date +%Y%m%d%H%M%S)"
    {
      printf '\n%s\n' "$MARKER"
      printf '[ -f "%s" ] && AI_ROOTS_DIR="%s" . "%s"\n' "$UPDATE_SRC" "$SCRIPT_DIR" "$UPDATE_SRC"
      printf '# <<< ai-roots update check <<<\n'
    } >>"$RC"
    echo "added ai-roots update check to $RC"
  fi
fi

echo "done."
