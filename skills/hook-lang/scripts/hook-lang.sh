#!/bin/sh
state="$HOME/.claude/.ai-roots/lang"
case "$1" in
  en|ko) mkdir -p "${state%/*}" && echo "$1" > "$state" && echo "hook-lang: $1" ;;
  "")
    if [ -f "$state" ]; then
      echo "hook-lang: $(cat "$state")"
    else
      echo "hook-lang: en (default)"
    fi
    ;;
  *) echo "unsupported language: $1 (expected en|ko)" ;;
esac
