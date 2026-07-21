---
name: fact-check
description: "[ai-roots] Tune or toggle the grounded-assertions Stop-hook audit. Use when the user asks to turn the claim audit on or off, change its sentence gate, or check whether it is active — /fact-check (status), /fact-check on, /fact-check off, /fact-check <number> (set the gate)."
allowed-tools: "Bash(case *)"
---

# /fact-check (ai-roots)

Controls the `grounded-assertions` Stop hook via `~/.claude/.ai-roots/fact-check`. The hook reads the file on every turn end, so a change applies from the very next turn, in every session.

The command below already executed during skill expansion — the line after this paragraph is its output, and it is the result. Do not run any further commands; report the outcome to the user in one sentence, in the user's language.

!`case "$ARGUMENTS" in off) mkdir -p "$HOME/.claude/.ai-roots" && echo off > "$HOME/.claude/.ai-roots/fact-check" && echo "fact-check: off";; on) rm -f "$HOME/.claude/.ai-roots/fact-check"; echo "fact-check: on (gate 8, default)";; "") if [ -f "$HOME/.claude/.ai-roots/fact-check" ]; then v=$(cat "$HOME/.claude/.ai-roots/fact-check"); if [ "$v" = "off" ]; then echo "fact-check: off"; else echo "fact-check: on (gate $v)"; fi; else echo "fact-check: on (gate 8, default)"; fi;; *[!0-9]*) echo "unknown subcommand: $ARGUMENTS (expected on|off|<number>)";; *) mkdir -p "$HOME/.claude/.ai-roots" && echo "$ARGUMENTS" > "$HOME/.claude/.ai-roots/fact-check" && echo "fact-check: on (gate $ARGUMENTS)";; esac`

Meaning of each outcome:

- `fact-check: off` — the Stop-hook audit is disabled everywhere until turned back on.
- `fact-check: on (gate N)` — the audit fires on turns whose final message holds at least N sentences; a smaller N audits more turns, a larger N fewer.
- `fact-check: on (gate 8, default)` — no override is stored; the hook uses its built-in default.
- `unknown subcommand` — relay the expected forms: no argument reads status, `on`/`off` toggle, a number sets the gate.

## Notes

- The setting lives in `~/.claude/.ai-roots/fact-check` — global to this machine (the hook itself is registered globally), persistent across sessions, never committed.
- The default gate (8) is defined in `hooks/grounded-assertions.py` (`SENTENCE_GATE`); `on` here just removes the override, so the two never drift.
- Zero-model alternative for the user: typing `! echo 12 > ~/.claude/.ai-roots/fact-check` in the prompt applies the same change without any model turn.
