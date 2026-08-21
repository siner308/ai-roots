#!/bin/sh
state="$HOME/.claude/.ai-roots/fact-check"
case "$1" in
  off) mkdir -p "${state%/*}" && echo off > "$state" && echo "fact-check: off" ;;
  on) rm -f "$state"; echo "fact-check: on (gate 8, default)" ;;
  "")
    if [ -f "$state" ]; then
      v=$(cat "$state")
      if [ "$v" = "off" ]; then echo "fact-check: off"; else echo "fact-check: on (gate $v)"; fi
    else
      echo "fact-check: on (gate 8, default)"
    fi
    ;;
  *[!0-9]*) echo "unknown subcommand: $1 (expected on|off|<number>)" ;;
  *) mkdir -p "${state%/*}" && echo "$1" > "$state" && echo "fact-check: on (gate $1)" ;;
esac
