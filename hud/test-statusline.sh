#!/bin/sh
# Fixture tests for statusline-command.sh.

set -eu

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
TMP_ROOT="${TMPDIR:-/tmp}/ai-roots-hud-test.$$"
CLAUDE_DIR="$TMP_ROOT/.claude"
HOME_DIR="$TMP_ROOT/home"

cleanup() {
  rm -rf "$TMP_ROOT"
}
trap cleanup EXIT INT TERM

mkdir -p "$CLAUDE_DIR" "$HOME_DIR"

strip_ansi() {
  sed -E 's/\x1b\[[0-9;]*m//g'
}

assert_contains() {
  haystack=$1
  needle=$2
  if ! printf '%s' "$haystack" | grep -Fq "$needle"; then
    echo "missing expected text: $needle"
    echo "output:"
    printf '%s\n' "$haystack"
    exit 1
  fi
}

input=$(printf '{"workspace":{"current_dir":"%s"},"model":{"display_name":"Opus 4.7"},"context_window":{"used_percentage":42}}' "$SCRIPT_DIR")

out=$(printf '%s' "$input" \
  | CLAUDE_CONFIG_DIR="$CLAUDE_DIR" HOME="$HOME_DIR" sh "$SCRIPT_DIR/statusline-command.sh" \
  | strip_ansi)

assert_contains "$out" "hud"
assert_contains "$out" "[ctx:42%]"
assert_contains "$out" "Opus 4.7"

cat > "$CLAUDE_DIR/.usage-cache.json" <<'JSON'
{
  "timestamp": 9999999999,
  "data": {
    "five_hour": {"utilization": 42},
    "seven_day": {"utilization": 58},
    "seven_day_sonnet": {"utilization": 87}
  }
}
JSON

out=$(printf '%s' "$input" \
  | CLAUDE_CONFIG_DIR="$CLAUDE_DIR" HOME="$HOME_DIR" sh "$SCRIPT_DIR/statusline-command.sh" \
  | strip_ansi)

assert_contains "$out" "5h:42%"
assert_contains "$out" "7d:58%"
assert_contains "$out" "sonnet:87%"

echo "ok"
