#!/bin/sh
case "$1" in
  off) git config ai-roots.push-gate off && echo "push-gate: off" ;;
  on) git config --unset ai-roots.push-gate; echo "push-gate: on" ;;
  "")
    if [ "$(git config --get ai-roots.push-gate)" = "off" ]; then
      git config --unset ai-roots.push-gate
      echo "push-gate: on (toggled)"
    else
      git config ai-roots.push-gate off && echo "push-gate: off (toggled)"
    fi
    ;;
  status) echo "push-gate: $(git config --get ai-roots.push-gate || echo on)" ;;
  *) echo "unknown subcommand: $1 (expected on|off|status)" ;;
esac
