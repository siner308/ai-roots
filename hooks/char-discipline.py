#!/usr/bin/env python3
"""Hook enforcing the character section of prose-style on two surfaces.

As PostToolUse on Edit/Write/MultiEdit it scans the text an edit adds, on every file type; as a Stop hook it scans the turn's final message, which is where the characters reach the user directly.
The character rule is the one writing concern a static check catches exactly: a codepoint is either there or not, so there is no heuristic and no language dependence. It is also the concern a resident rule protects worst, since emitting an em dash is not a decision the model makes deliberately; the glyph arrives with the sentence.
Two kinds get flagged. Visible glyphs (em dash, middle dot, curly quotes, ellipsis, arrows, decorative bullets) read as a machine signature however good the sentence is; invisible ones carry no meaning in prose and break code, commit messages, and search indexes with nothing on screen to explain why.
The legitimate keeps cannot be detected statically, so the block names them and asks for a verdict per occurrence with replace as the default, the same shape comment-discipline uses.
Fenced code blocks are skipped: they hold quoted commands and file content that has to stay byte-exact.
The Stop side blocks at most once per turn (stop_hook_active caps it) and fails open on any transcript error, so a stubborn exempt character can never trap the session.
Set AI_ROOTS_CHAR_CHECK=0 to disable both surfaces.
"""
import json
import os
import sys

from char_tables import KEEPS, report, scan, strip_fences
from hook_lang import localize

EDIT_TOOLS = {"Write", "Edit", "MultiEdit"}


def edit_lines(data):
    ti = data.get("tool_input", {})
    name = data.get("tool_name")
    if name == "Write":
        chunks = [ti.get("content", "")]
    elif name == "Edit":
        chunks = [ti.get("new_string", "")]
    else:
        chunks = [e.get("new_string", "") for e in ti.get("edits", [])]
    return [line for chunk in chunks for line in strip_fences(chunk)]


def final_message(path):
    """The turn's last assistant text, or empty when the transcript is unreadable."""
    try:
        with open(path) as f:
            entries = f.readlines()
    except OSError:
        return ""
    for raw in reversed(entries):
        try:
            entry = json.loads(raw)
        except Exception:
            continue
        if entry.get("isSidechain") or entry.get("type") != "assistant":
            continue
        content = (entry.get("message") or {}).get("content")
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            texts = [
                b.get("text", "")
                for b in content
                if isinstance(b, dict) and b.get("type") == "text"
            ]
            if texts:
                return "\n".join(texts)
    return ""


def main():
    if os.environ.get("AI_ROOTS_CHAR_CHECK") == "0":
        return 0
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0

    if data.get("tool_name") in EDIT_TOOLS:
        if not data.get("tool_input", {}).get("file_path"):
            return 0
        lines = edit_lines(data)
        where = "this edit adds"
        close = (
            "Give a verdict for each occurrence and replace it by default. Keep "
            f"one only where the character is the content: {KEEPS}. Name the "
            "exemption that applies and continue."
        )
    elif data.get("transcript_path"):
        if data.get("stop_hook_active"):
            return 0
        lines = strip_fences(final_message(data["transcript_path"]))
        where = "the reply you just wrote contains"
        close = (
            "Rewrite the affected sentences with the ASCII forms above, then close "
            "with the answer the user asked for. Keep a character only where it is "
            f"the content: {KEEPS}. Say which exemption applies and stop."
        )
    else:
        return 0

    counts, samples = scan(lines)
    if not counts:
        return 0

    total = sum(counts.values())
    print(json.dumps({
        "decision": "block",
        "reason": localize(
            f"char-discipline: {where} {total} occurrence(s) of characters the "
            "prose-style character rule bars:\n"
            + report(counts, samples)
            + "\n\n" + close
        ),
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
