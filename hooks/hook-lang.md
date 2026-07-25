# hook_lang

Shared helper, not a registered hook. `hooks/hook_lang.py` reads `~/.claude/.ai-roots/lang` and appends a relay instruction to a block message when the language is not `en`.

## Why it exists

Hook block messages surface in the user's session, so a Korean-speaking user gets English mid-conversation. Worse, an English instruction arriving right before the model's next message pulls that message into English too — the drift is visible in any Korean session where a Stop-hook audit fires.

Translating every string in every hook would fork the text and let the copies drift, and `CLAUDE.md` keeps `hooks/` English-source. So the message stays English and gains one line telling the model to restate the verdict in the user's language.

## Usage

```python
from hook_lang import localize

print(json.dumps({"decision": "block", "reason": localize(msg)}))
```

`localize` degrades to the untouched message when the state file is missing, empty, or names an unknown language — a bad setting can never break editing.

## Wiring

`hook_lang.py` is listed in `SUPPORT_MODULES` in `hooks/register.py`, not in `manifest.json`: it needs to be symlinked beside the hooks that import it, and the orphan prune must spare it. Adding another support module means adding it to that list.

Currently used by `comment-discipline.py`, `prose-discipline.py`, and `grounded-assertions.py`. `push-gate.py` and `gh-markdown-style.py` already write their messages in Korean and are left alone.

## Adding a language

Add an entry to `RELAY` in `hooks/hook_lang.py` and a case to `skills/hook-lang/SKILL.md` (and its Korean mirror).
