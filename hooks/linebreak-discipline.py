#!/usr/bin/env python3
"""PostToolUse hook for Edit/Write/MultiEdit on Markdown files.

Detects newly added hard line breaks that fall mid-sentence.
A break after a sentence ends is fine but never required — a line may hold several sentences; the only violation is cutting a sentence across lines.
The prose-style rule already forbids this, but the pull to imitate a file's incumbent hard-wrap style overrides a resident rule in practice — the same failure mode that made comment-discipline a hook.
Fires only on the text an edit adds, so pre-existing wrapping elsewhere in the file does not trigger it.
"""
import json
import re
import sys

TERMINAL = re.compile(r'[.!?:;…。！？](["\')\]`*_」』]*)$')
NEW_BLOCK = re.compile(r'^\s*(#|[-*+]\s|\d+\.\s|>|\||```|~~~|---\s*$)')
STRUCTURAL = re.compile(r'^\s*(#|\||```|~~~|---\s*$)')


def midsentence_breaks(text):
    out = []
    fence = False
    lines = text.splitlines()
    for i, raw in enumerate(lines[:-1]):
        line = raw.rstrip()
        if line.startswith("```") or line.startswith("~~~"):
            fence = not fence
            continue
        if fence or not line.strip():
            continue
        nxt = lines[i + 1].rstrip()
        if not nxt.strip() or NEW_BLOCK.match(nxt):
            continue
        if STRUCTURAL.match(line):
            continue
        if not TERMINAL.search(line):
            out.append(line.strip())
    return out


def added_text(data):
    name = data.get("tool_name")
    ti = data.get("tool_input", {})
    if name == "Write":
        content = ti.get("content", "")
        if content.startswith("---\n"):
            end = content.find("\n---", 4)
            if end != -1:
                content = content[end + 4:]
        return [content]
    if name == "Edit":
        return [ti.get("new_string", "")]
    if name == "MultiEdit":
        return [e.get("new_string", "") for e in ti.get("edits", [])]
    return []


def main():
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0
    path = data.get("tool_input", {}).get("file_path", "")
    if not path.endswith((".md", ".markdown")):
        return 0

    hits = []
    for chunk in added_text(data):
        hits.extend(midsentence_breaks(chunk))
    if not hits:
        return 0

    sample = "\n".join("    " + h[:100] for h in hits[:5])
    more = "" if len(hits) <= 5 else f"\n    … and {len(hits) - 5} more"
    print(json.dumps({
        "decision": "block",
        "reason": (
            f"linebreak-discipline: this edit added {len(hits)} line(s) that "
            f"break mid-sentence (the line ends without sentence-terminal "
            f"punctuation and the next line continues it):\n{sample}{more}\n\n"
            "Don't break a sentence across lines. Re-join each flagged line "
            "with its continuation so every hard break falls where a sentence "
            "ends — a line holding several sentences is fine. The only "
            "exemption is a linter or formatter that errors on line width in "
            "this project — if that applies, name the tool and keep the wrap; "
            "a file's existing wrap style or your display width does not "
            "qualify."
        ),
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
