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


def midsentence_breaks(text, fence=False):
    out = []
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


def fence_open_before(file_text, idx):
    opens = sum(
        1 for line in file_text[:idx].splitlines()
        if line.rstrip().startswith(("```", "~~~"))
    )
    return opens % 2 == 1


def added_text(data):
    # An Edit's new_string carries no surrounding fence markers, so code inside a
    # fenced block would read as prose. PostToolUse runs after the edit landed, so
    # the chunk's fence state is recovered by locating it in the written file.
    name = data.get("tool_name")
    ti = data.get("tool_input", {})
    if name == "Write":
        content = ti.get("content", "")
        if content.startswith("---\n"):
            end = content.find("\n---", 4)
            if end != -1:
                content = content[end + 4:]
        return [(content, False)]

    try:
        with open(ti.get("file_path", "")) as f:
            file_text = f.read()
    except OSError:
        file_text = None

    def occurrences(new_string):
        if not new_string:
            return []
        if file_text is None:
            return [(new_string, False)]
        out, start = [], 0
        while (idx := file_text.find(new_string, start)) != -1:
            out.append((new_string, fence_open_before(file_text, idx)))
            start = idx + 1
        return out or [(new_string, False)]

    if name == "Edit":
        return occurrences(ti.get("new_string", ""))
    if name == "MultiEdit":
        return [p for e in ti.get("edits", []) for p in occurrences(e.get("new_string", ""))]
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
    for chunk, fence in added_text(data):
        hits.extend(midsentence_breaks(chunk, fence))
    hits = list(dict.fromkeys(hits))
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
