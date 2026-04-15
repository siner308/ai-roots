#!/bin/bash
# ai-roots HUD installer
# Installs the statusline-command.sh and configures settings.json

set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
DEST="$CLAUDE_DIR/statusline-command.sh"
SETTINGS="$CLAUDE_DIR/settings.json"

# Check dependencies
for cmd in jq curl python3; do
  if ! command -v "$cmd" >/dev/null 2>&1; then
    echo "error: $cmd is required but not found"
    exit 1
  fi
done

# Copy statusline script
cp "$SCRIPT_DIR/statusline-command.sh" "$DEST"
chmod +x "$DEST"
echo "installed: $DEST"

# Configure settings.json
if [ -f "$SETTINGS" ]; then
  # Check if statusLine is already configured
  existing=$(jq -r '.statusLine.command // empty' "$SETTINGS" 2>/dev/null)
  if [ -n "$existing" ] && [ "$existing" != "sh $DEST" ]; then
    echo "existing statusLine found: $existing"
    read -p "overwrite? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
      echo "skipped settings.json update. to apply manually, add:"
      echo "  \"statusLine\": {\"type\": \"command\", \"command\": \"sh $DEST\"}"
      exit 0
    fi
  fi
  # Update statusLine in settings.json
  jq --arg cmd "sh $DEST" '.statusLine = {"type": "command", "command": $cmd}' "$SETTINGS" > "${SETTINGS}.tmp"
  mv "${SETTINGS}.tmp" "$SETTINGS"
  echo "configured: statusLine in $SETTINGS"
else
  echo "warning: $SETTINGS not found — create it or add statusLine manually:"
  echo "  \"statusLine\": {\"type\": \"command\", \"command\": \"sh $DEST\"}"
fi

echo ""
echo "done. restart Claude Code to see the status line."
