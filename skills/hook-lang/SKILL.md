---
name: hook-lang
description: "[ai-roots] Set the language hook messages are relayed in. Use when the user asks for hook or block messages in their own language, or asks which language is set — /hook-lang (status), /hook-lang ko, /hook-lang en."
allowed-tools: "Bash(case *)"
---

# /hook-lang (ai-roots)

Sets the language hooks relay their verdicts in, via `~/.claude/.ai-roots/lang`. Hook scripts stay English-source per `CLAUDE.md`; when the language is not `en`, each block message carries an instruction to restate the verdict in that language.

The command below already executed during skill expansion — the line after this paragraph is its output, and it is the result. Do not run any further commands; report the outcome to the user in one sentence, in the user's language.

!`case "$ARGUMENTS" in en) mkdir -p "$HOME/.claude/.ai-roots" && echo en > "$HOME/.claude/.ai-roots/lang" && echo "hook-lang: en";; ko) mkdir -p "$HOME/.claude/.ai-roots" && echo ko > "$HOME/.claude/.ai-roots/lang" && echo "hook-lang: ko";; "") if [ -f "$HOME/.claude/.ai-roots/lang" ]; then echo "hook-lang: $(cat "$HOME/.claude/.ai-roots/lang")"; else echo "hook-lang: en (default)"; fi;; *) echo "unsupported language: $ARGUMENTS (expected en|ko)";; esac`

Meaning of each outcome:

- `hook-lang: en` — hook messages stay as written, with no relay instruction.
- `hook-lang: ko` — every hook block message gains a line telling the model to restate the verdict in Korean.
- `hook-lang: en (default)` — no setting is stored; hooks use English.
- `unsupported language` — relay the supported forms: `en` and `ko`, or no argument to read status.

## Notes

- The setting lives in `~/.claude/.ai-roots/lang` — global to this machine, persistent across sessions, never committed.
- It changes the *relay* instruction, not the message itself: the English text still appears, followed by a directive to restate it. A hook whose message is already written in the user's language (`push-gate`, `gh-markdown-style`) is unaffected.
- Adding a language means adding one entry to `RELAY` in `hooks/hook_lang.py` and one case here.
- Zero-model alternative for the user: typing `! echo ko > ~/.claude/.ai-roots/lang` in the prompt applies the same change without any model turn.
