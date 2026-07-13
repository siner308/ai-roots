---
name: push-gate
description: "[ai-roots] Toggle the per-push confirmation gate for the current repository. Use when the user asks to turn the push gate on or off, allow pushes without prompts (autopilot), or check whether the gate is active — /push-gate (toggle), /push-gate on, /push-gate off, /push-gate status."
allowed-tools: "Bash(case *), Bash(git config *)"
---

# /push-gate (ai-roots)

Controls the `push-gate` PreToolUse hook for the **current repository** via `ai-roots.push-gate` in the repo's local git config. The hook reads it live, so a change applies to the very next push.

The toggle below already executed during skill expansion — the line after this paragraph is its output, and it is the result. Do not run any further commands; report the outcome to the user in one sentence, in the user's language.

!`case "$ARGUMENTS" in off) git config ai-roots.push-gate off && echo "push-gate: off";; on) git config --unset ai-roots.push-gate; echo "push-gate: on";; "") if [ "$(git config --get ai-roots.push-gate)" = "off" ]; then git config --unset ai-roots.push-gate; echo "push-gate: on (toggled)"; else git config ai-roots.push-gate off && echo "push-gate: off (toggled)"; fi;; status) echo "push-gate: $(git config --get ai-roots.push-gate || echo on)";; *) echo "unknown subcommand: $ARGUMENTS (expected on|off|status)";; esac`

Meaning of each outcome:

- `push-gate: off` — pushes from this repo skip the per-push ask: a permissive session mode pushes silently, default mode still shows the standard Bash prompt. Force pushes stay denied regardless.
- `push-gate: on` — the gate is active: every push asks for confirmation.
- An error mentioning "not in a git repository" — say the command only works inside a git repo.
- `unknown subcommand` — relay the expected forms: no argument toggles, `on`/`off` set explicitly, `status` reads without changing.

## Notes

- The setting lives in `.git/config` — local to this clone, never committed, persistent across sessions.
- Turning the gate off is an outward-facing loosening: when the user asks for it in passing (not via the explicit command), restate in one line that pushes from this repo will no longer be individually confirmed.
- Zero-model alternative for the user: typing `! git config ai-roots.push-gate off` in the prompt runs the same toggle without any model turn.
