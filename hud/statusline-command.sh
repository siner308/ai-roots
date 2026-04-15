#!/bin/sh
# Claude Code statusLine — robbyrussell theme + rate limits
# Reads JSON from stdin, outputs a styled status line
#
# Features:
#   - robbyrussell-style prompt (➜ dir git:(branch))
#   - Context window usage percentage
#   - Rate limits: 5h, 7d (all models), 7d Sonnet
#   - Color-coded: green <50%, yellow 50-79%, red ≥80%
#   - Background API fetch with 90s cache TTL

input=$(cat)

cwd=$(echo "$input" | jq -r '.workspace.current_dir // .cwd // empty')
model=$(echo "$input" | jq -r '.model.display_name // empty')
used=$(echo "$input" | jq -r '.context_window.used_percentage // empty')

ESC=$(printf '\033')

# Directory name
if [ -n "$cwd" ]; then
  dir_name=$(basename "$cwd")
else
  dir_name="."
fi

# Git branch
git_part=""
if [ -n "$cwd" ] && [ -d "$cwd" ]; then
  branch=$(GIT_OPTIONAL_LOCKS=0 git -C "$cwd" symbolic-ref --short HEAD 2>/dev/null)
  if [ -n "$branch" ]; then
    if GIT_OPTIONAL_LOCKS=0 git -C "$cwd" status --porcelain 2>/dev/null | grep -q .; then
      dirty=" ${ESC}[31m✗${ESC}[0m"
    else
      dirty=""
    fi
    git_part=" ${ESC}[33mgit:(${ESC}[31m${branch}${ESC}[33m)${ESC}[0m${dirty}"
  fi
fi

# Context usage
ctx_part=""
if [ -n "$used" ]; then
  used_int=$(printf "%.0f" "$used")
  ctx_part=" ${ESC}[2m[ctx:${used_int}%]${ESC}[0m"
fi

# Model part
model_part=""
if [ -n "$model" ]; then
  model_part=" ${ESC}[2m${model}${ESC}[0m"
fi

# --- Rate limits (cached) ---
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
CACHE_FILE="$CLAUDE_DIR/.usage-cache.json"
CACHE_TTL=90

usage_part=""

# Fetch usage if cache is stale or missing
fetch_needed=1
if [ -f "$CACHE_FILE" ]; then
  cache_ts=$(jq -r '.timestamp // 0' "$CACHE_FILE" 2>/dev/null)
  now_ts=$(date +%s)
  age=$((now_ts - cache_ts))
  if [ "$age" -lt "$CACHE_TTL" ]; then
    fetch_needed=0
  fi
fi

if [ "$fetch_needed" -eq 1 ]; then
  # Background fetch to avoid blocking statusline
  (
    token=""
    # macOS: try Keychain first
    if command -v security >/dev/null 2>&1; then
      token=$(security find-generic-password -s "Claude Code-credentials" -w 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(d.get('claudeAiOauth',{}).get('accessToken',''))" 2>/dev/null)
    fi
    # Fallback: credentials file
    if [ -z "$token" ] && [ -f "$CLAUDE_DIR/.credentials.json" ]; then
      token=$(python3 -c "import json; d=json.load(open('$CLAUDE_DIR/.credentials.json')); print(d.get('claudeAiOauth',{}).get('accessToken',''))" 2>/dev/null)
    fi
    if [ -n "$token" ]; then
      resp=$(curl -s --max-time 5 -H "Authorization: Bearer $token" -H "anthropic-beta: oauth-2025-04-20" "https://api.anthropic.com/api/oauth/usage" 2>/dev/null)
      if echo "$resp" | jq -e '.five_hour' >/dev/null 2>&1; then
        now_ts=$(date +%s)
        echo "$resp" | jq --argjson ts "$now_ts" '{timestamp: $ts, data: .}' > "${CACHE_FILE}.tmp" 2>/dev/null
        mv "${CACHE_FILE}.tmp" "$CACHE_FILE" 2>/dev/null
      fi
    fi
  ) &
fi

# Read from cache
if [ -f "$CACHE_FILE" ]; then
  five_h=$(jq -r '.data.five_hour.utilization // empty' "$CACHE_FILE" 2>/dev/null)
  weekly=$(jq -r '.data.seven_day.utilization // empty' "$CACHE_FILE" 2>/dev/null)
  sonnet_w=$(jq -r '.data.seven_day_sonnet.utilization // empty' "$CACHE_FILE" 2>/dev/null)

  # Color based on utilization level
  color_for_pct() {
    pct=$1
    pct_int=$(printf "%.0f" "$pct")
    if [ "$pct_int" -ge 80 ]; then
      printf '%s' "${ESC}[31m"  # red
    elif [ "$pct_int" -ge 50 ]; then
      printf '%s' "${ESC}[33m"  # yellow
    else
      printf '%s' "${ESC}[32m"  # green
    fi
  }

  parts=""
  if [ -n "$five_h" ]; then
    c=$(color_for_pct "$five_h")
    five_int=$(printf "%.0f" "$five_h")
    parts="5h:${c}${five_int}%${ESC}[0m"
  fi
  if [ -n "$weekly" ]; then
    c=$(color_for_pct "$weekly")
    w_int=$(printf "%.0f" "$weekly")
    parts="${parts:+${parts} }7d:${c}${w_int}%${ESC}[0m"
  fi
  if [ -n "$sonnet_w" ]; then
    c=$(color_for_pct "$sonnet_w")
    s_int=$(printf "%.0f" "$sonnet_w")
    parts="${parts:+${parts} }sonnet:${c}${s_int}%${ESC}[0m"
  fi

  if [ -n "$parts" ]; then
    usage_part=" ${ESC}[2m[${ESC}[0m${parts}${ESC}[2m]${ESC}[0m"
  fi
fi

printf "%s" "${ESC}[32m➜${ESC}[0m  ${ESC}[36m${dir_name}${ESC}[0m${git_part}${ctx_part}${usage_part}${model_part}"
