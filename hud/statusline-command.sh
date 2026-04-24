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
transcript=$(echo "$input" | jq -r '.transcript_path // empty')

# Effort resolution order:
#   1. Session-level /effort or /model command (parsed from transcript tail)
#   2. Persistent effortLevel in settings.json
effort=""
if [ -n "$transcript" ] && [ -f "$transcript" ]; then
  # Transcript stores ANSI as literal \u001b[...m — strip before matching
  effort=$(tail -500 "$transcript" 2>/dev/null \
    | sed -E 's/\\u001b\[[0-9;]*m//g' \
    | grep -oE 'Set effort level to [a-zA-Z]+|with [a-zA-Z]+ effort' \
    | tail -1 \
    | sed -E 's/Set effort level to //; s/with ([a-zA-Z]+) effort/\1/')
fi
if [ -z "$effort" ] && [ -f "$HOME/.claude/settings.json" ]; then
  effort=$(jq -r '.effortLevel // empty' "$HOME/.claude/settings.json" 2>/dev/null)
fi

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

# Effort part
effort_part=""
if [ -n "$effort" ]; then
  if [ "$effort" = "max" ]; then
    # Animated rainbow — shifts with time so repeated statusline redraws appear to flow
    rainbow=$(python3 -c "
import time
text='max'
palette=[196,202,208,214,226,190,118,82,46,49,51,45,33,21,57,93,129,165,201,197]
tick=int(time.time()*5)
out=''
for i,ch in enumerate(text):
    c=palette[(tick+i)%len(palette)]
    out+=f'\x1b[1;38;5;{c}m{ch}'
out+='\x1b[0m'
print(out,end='')
" 2>/dev/null)
    effort_part=" ${ESC}[2meffort:${ESC}[0m${rainbow:-${ESC}[1;35mmax${ESC}[0m}"
  else
    case "$effort" in
      low)            ec="${ESC}[32m" ;;
      medium)         ec="${ESC}[33m" ;;
      high)           ec="${ESC}[31m" ;;
      xhigh|xHigh)    ec="${ESC}[35m" ;;
      *)              ec="${ESC}[2m" ;;
    esac
    effort_part=" ${ESC}[2meffort:${ESC}[0m${ec}${effort}${ESC}[0m"
  fi
fi

# --- Rate limits (cached) ---
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
CACHE_FILE="$CLAUDE_DIR/.usage-cache.json"
LOCK_DIR="$CACHE_FILE.lock"
CACHE_TTL=90
now_ts=$(date +%s)

usage_part=""

# Fetch usage if cache is stale or missing
fetch_needed=1
if [ -f "$CACHE_FILE" ]; then
  cache_ts=$(jq -r '.timestamp // 0' "$CACHE_FILE" 2>/dev/null)
  age=$((now_ts - cache_ts))
  if [ "$age" -lt "$CACHE_TTL" ]; then
    fetch_needed=0
  fi
fi

if [ "$fetch_needed" -eq 1 ]; then
  # Background fetch to avoid blocking statusline
  if mkdir "$LOCK_DIR" 2>/dev/null; then
    (
    trap 'rmdir "$LOCK_DIR" 2>/dev/null' EXIT INT TERM
    mkdir -p "$CLAUDE_DIR" 2>/dev/null
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
        # Enrich with epoch timestamps for countdown display
        enriched=$(echo "$resp" | python3 -c "
import json,sys
from datetime import datetime
d=json.load(sys.stdin)
for k in ('five_hour','seven_day','seven_day_sonnet'):
    v=d.get(k)
    if v and v.get('resets_at'):
        try: v['resets_at_epoch']=int(datetime.fromisoformat(v['resets_at']).timestamp())
        except: pass
json.dump(d,sys.stdout)
" 2>/dev/null)
        src="${enriched:-$resp}"
        echo "$src" | jq --argjson ts "$now_ts" '{timestamp: $ts, data: .}' > "${CACHE_FILE}.tmp" 2>/dev/null
        mv "${CACHE_FILE}.tmp" "$CACHE_FILE" 2>/dev/null
      fi
    fi
    ) &
  fi
fi

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

# Format seconds as compact countdown (e.g. 2h30m, 5d2h)
format_countdown() {
  secs=$1
  if [ "$secs" -le 0 ] 2>/dev/null; then return; fi
  mins=$((secs / 60))
  if [ "$mins" -lt 60 ]; then
    printf '%dm' "$mins"
  else
    h=$((mins / 60)); m=$((mins % 60))
    if [ "$h" -ge 24 ]; then
      d=$((h / 24)); rh=$((h % 24))
      if [ "$rh" -gt 0 ]; then printf '%dd%dh' "$d" "$rh"; else printf '%dd' "$d"; fi
    elif [ "$m" -gt 0 ]; then
      printf '%dh%dm' "$h" "$m"
    else
      printf '%dh' "$h"
    fi
  fi
}

# Read from cache
if [ -f "$CACHE_FILE" ]; then
  five_h=$(jq -r '.data.five_hour.utilization // empty' "$CACHE_FILE" 2>/dev/null)
  weekly=$(jq -r '.data.seven_day.utilization // empty' "$CACHE_FILE" 2>/dev/null)
  sonnet_w=$(jq -r '.data.seven_day_sonnet.utilization // empty' "$CACHE_FILE" 2>/dev/null)

  five_h_epoch=$(jq -r '.data.five_hour.resets_at_epoch // empty' "$CACHE_FILE" 2>/dev/null)
  weekly_epoch=$(jq -r '.data.seven_day.resets_at_epoch // empty' "$CACHE_FILE" 2>/dev/null)
  sonnet_epoch=$(jq -r '.data.seven_day_sonnet.resets_at_epoch // empty' "$CACHE_FILE" 2>/dev/null)

  parts=""
  if [ -n "$five_h" ]; then
    c=$(color_for_pct "$five_h")
    five_int=$(printf "%.0f" "$five_h")
    cd_str=""
    if [ -n "$five_h_epoch" ]; then cd_str=$(format_countdown $((five_h_epoch - now_ts))); fi
    if [ -n "$cd_str" ]; then
      parts="5h:${c}${five_int}%${ESC}[0m${ESC}[2m(${cd_str})${ESC}[0m"
    else
      parts="5h:${c}${five_int}%${ESC}[0m"
    fi
  fi
  if [ -n "$weekly" ]; then
    c=$(color_for_pct "$weekly")
    w_int=$(printf "%.0f" "$weekly")
    cd_str=""
    if [ -n "$weekly_epoch" ]; then cd_str=$(format_countdown $((weekly_epoch - now_ts))); fi
    if [ -n "$cd_str" ]; then
      parts="${parts:+${parts} }7d:${c}${w_int}%${ESC}[0m${ESC}[2m(${cd_str})${ESC}[0m"
    else
      parts="${parts:+${parts} }7d:${c}${w_int}%${ESC}[0m"
    fi
  fi
  if [ -n "$sonnet_w" ]; then
    c=$(color_for_pct "$sonnet_w")
    s_int=$(printf "%.0f" "$sonnet_w")
    cd_str=""
    if [ -n "$sonnet_epoch" ]; then cd_str=$(format_countdown $((sonnet_epoch - now_ts))); fi
    if [ -n "$cd_str" ]; then
      parts="${parts:+${parts} }sonnet:${c}${s_int}%${ESC}[0m${ESC}[2m(${cd_str})${ESC}[0m"
    else
      parts="${parts:+${parts} }sonnet:${c}${s_int}%${ESC}[0m"
    fi
  fi

  if [ -n "$parts" ]; then
    usage_part=" ${ESC}[2m[${ESC}[0m${parts}${ESC}[2m]${ESC}[0m"
  fi
fi

# --- Codex rate limits (parsed from latest local session jsonl, cached) ---
CODEX_DIR_HOME="$HOME/.codex/sessions"
CODEX_CACHE="$CLAUDE_DIR/.codex-usage-cache.json"
CODEX_LOCK="$CODEX_CACHE.lock"
codex_part=""

codex_fetch_needed=1
if [ -f "$CODEX_CACHE" ]; then
  cx_cache_ts=$(jq -r '.timestamp // 0' "$CODEX_CACHE" 2>/dev/null)
  if [ $((now_ts - cx_cache_ts)) -lt "$CACHE_TTL" ]; then
    codex_fetch_needed=0
  fi
fi

if [ "$codex_fetch_needed" -eq 1 ] && [ -d "$CODEX_DIR_HOME" ]; then
  if mkdir "$CODEX_LOCK" 2>/dev/null; then
    (
    trap 'rmdir "$CODEX_LOCK" 2>/dev/null' EXIT INT TERM
    latest=$(find "$CODEX_DIR_HOME" -type f -name "*.jsonl" -mtime -7 2>/dev/null \
      | xargs -I {} stat -f '%m %N' {} 2>/dev/null \
      | sort -rn | head -1 | cut -d' ' -f2-)
    if [ -n "$latest" ] && [ -f "$latest" ]; then
      result=$(python3 - "$latest" <<'PY' 2>/dev/null
import json, sys
path = sys.argv[1]
last = None
try:
    with open(path) as fh:
        for line in fh:
            if '"rate_limits"' not in line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                continue
            stack = [obj]
            while stack:
                o = stack.pop()
                if isinstance(o, dict):
                    rl = o.get('rate_limits')
                    if isinstance(rl, dict):
                        last = rl
                    stack.extend(o.values())
                elif isinstance(o, list):
                    stack.extend(o)
except Exception:
    pass
if last:
    print(json.dumps(last))
PY
)
      if [ -n "$result" ]; then
        ts=$(date +%s)
        printf '{"timestamp":%s,"data":%s}' "$ts" "$result" > "${CODEX_CACHE}.tmp" 2>/dev/null \
          && mv "${CODEX_CACHE}.tmp" "$CODEX_CACHE" 2>/dev/null
      fi
    fi
    ) &
  fi
fi

if [ -f "$CODEX_CACHE" ]; then
  cx_5h=$(jq -r '.data.primary.used_percent // empty' "$CODEX_CACHE" 2>/dev/null)
  cx_7d=$(jq -r '.data.secondary.used_percent // empty' "$CODEX_CACHE" 2>/dev/null)
  cx_5h_e=$(jq -r '.data.primary.resets_at // empty' "$CODEX_CACHE" 2>/dev/null)
  cx_7d_e=$(jq -r '.data.secondary.resets_at // empty' "$CODEX_CACHE" 2>/dev/null)

  cx_parts=""
  if [ -n "$cx_5h" ]; then
    c=$(color_for_pct "$cx_5h"); v=$(printf "%.0f" "$cx_5h")
    cd_str=""
    if [ -n "$cx_5h_e" ]; then cd_str=$(format_countdown $((cx_5h_e - now_ts))); fi
    if [ -n "$cd_str" ]; then
      cx_parts="5h:${c}${v}%${ESC}[0m${ESC}[2m(${cd_str})${ESC}[0m"
    else
      cx_parts="5h:${c}${v}%${ESC}[0m"
    fi
  fi
  if [ -n "$cx_7d" ]; then
    c=$(color_for_pct "$cx_7d"); v=$(printf "%.0f" "$cx_7d")
    cd_str=""
    if [ -n "$cx_7d_e" ]; then cd_str=$(format_countdown $((cx_7d_e - now_ts))); fi
    if [ -n "$cd_str" ]; then
      cx_parts="${cx_parts:+${cx_parts} }7d:${c}${v}%${ESC}[0m${ESC}[2m(${cd_str})${ESC}[0m"
    else
      cx_parts="${cx_parts:+${cx_parts} }7d:${c}${v}%${ESC}[0m"
    fi
  fi

  if [ -n "$cx_parts" ]; then
    codex_part=" ${ESC}[2m[${ESC}[0m${cx_parts}${ESC}[2m]${ESC}[0m"
  fi
fi

# Line 1: prompt + ctx + model + effort
line1="${ESC}[32m➜${ESC}[0m  ${ESC}[36m${dir_name}${ESC}[0m${git_part}${ctx_part}${model_part}${effort_part}"

# Line 2: claude usage (icon ✦)
line2=""
if [ -n "$usage_part" ]; then
  line2="${ESC}[2m✦ claude${ESC}[0m${usage_part}"
fi

# Line 3: codex usage (icon ◆)
line3=""
if [ -n "$codex_part" ]; then
  line3="${ESC}[2m✦ codex${ESC}[0m${codex_part}"
fi

out="$line1"
[ -n "$line2" ] && out="${out}
${line2}"
[ -n "$line3" ] && out="${out}
${line3}"
printf "%s" "$out"
