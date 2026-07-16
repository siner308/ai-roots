#!/usr/bin/env python3
"""PostToolUse hook for Edit/Write/MultiEdit on non-code prose files (Markdown).

Governs prose hygiene in docs: line breaks fall at meaning boundaries, and a substantial prose addition gets a conciseness re-check.
The comment-side twins of both concerns live in comment-discipline, which fires on every comment an edit adds; this hook is the non-code counterpart, keeping the two media on separate hooks so a code edit and a Markdown edit never double-fire.
Line-break detection is static because a punctuation-based check is language-agnostic enough for Markdown (a Korean sentence still ends on 다./요.).
Conciseness cannot be detected statically, so past a sentence-count gate the block delegates the judgment to the model — the same pattern comment-discipline uses for comment necessity.
Fires only on the text an edit adds, so pre-existing prose elsewhere in the file does not trigger it.
"""
import json
import re
import sys

TERMINAL = re.compile(r'[.!?:;…。！？](["\')\]`*_」』]*)$')
NEW_BLOCK = re.compile(r'^\s*(#|[-*+]\s|\d+\.\s|>|\||```|~~~|---\s*$)')
STRUCTURAL = re.compile(r'^\s*(#|\||```|~~~|---\s*$)')
SENTENCE_END = re.compile(r'[.!?…。！？](?=\s|$)')

CONCISE_SENTENCE_GATE = 6


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


def count_sentences(text, fence=False):
    n = 0
    for raw in text.splitlines():
        line = raw.rstrip()
        if line.startswith("```") or line.startswith("~~~"):
            fence = not fence
            continue
        if fence or not line.strip() or STRUCTURAL.match(line):
            continue
        n += len(SENTENCE_END.findall(line))
    return n


def fence_open_before(file_text, idx):
    opens = sum(
        1 for line in file_text[:idx].splitlines()
        if line.rstrip().startswith(("```", "~~~"))
    )
    return opens % 2 == 1


def added_text(data):
    # An Edit's new_string carries no surrounding fence markers, so code inside a fenced block
    # would read as prose. PostToolUse runs after the edit landed, so the chunk's fence state
    # is recovered by locating it in the written file.
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

    chunks = added_text(data)
    breaks = []
    sentences = 0
    for chunk, fence in chunks:
        breaks.extend(midsentence_breaks(chunk, fence))
        sentences += count_sentences(chunk, fence)
    breaks = list(dict.fromkeys(breaks))

    parts = []
    if breaks:
        sample = "\n".join("    " + h[:100] for h in breaks[:5])
        more = "" if len(breaks) <= 5 else f"\n    … and {len(breaks) - 5} more"
        parts.append(
            f"line breaks: this edit added {len(breaks)} line(s) that break "
            f"mid-sentence (the line ends without sentence-terminal punctuation "
            f"and the next line continues it):\n{sample}{more}\n"
            "Re-join each flagged line with its continuation so every hard break "
            "falls where a sentence ends — a line holding several sentences is "
            "fine. The only exemption is a linter or formatter that errors on "
            "line width in this project; name it and keep the wrap."
        )
    if sentences >= CONCISE_SENTENCE_GATE:
        parts.append(
            f"conciseness: this edit adds ~{sentences} sentences of prose. "
            "Re-read them as a skeptical editor and cut any that restate a "
            "neighbor, state the obvious, or hedge. A doc is expected to hold "
            "prose, so trim rather than blank it — but every surviving sentence "
            "should earn its place. If it is already tight, say so and continue."
        )
    if not parts:
        return 0

    print(json.dumps({
        "decision": "block",
        "reason": "prose-discipline:\n\n" + "\n\n".join(parts),
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
