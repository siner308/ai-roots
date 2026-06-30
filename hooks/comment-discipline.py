#!/usr/bin/env python3
"""PostToolUse hook for Edit/Write/MultiEdit.

Detects comment lines newly added by the edit and, when found, re-surfaces the
comment-discipline allowlist so the model re-checks each comment at the moment
it wrote it. A resident prose rule competes with everything else in context and
loses; this fires only on edits that actually add comments, so it re-primes the
rule exactly when it matters. Non-blocking: legitimate WHY comments are kept
after the re-check, noise is removed.
"""
import json
import sys

# Full-line comment openers per language family. Trailing comments are NOT
# matched on purpose — `"http://..."` and `url // x` produce too many false
# positives, and the dominant over-commenting habit is whole comment lines
# (explanatory lines above code, doc comments, docstrings) anyway.
C_STYLE = {".go", ".c", ".cc", ".cpp", ".h", ".hpp", ".java", ".js", ".jsx",
           ".ts", ".tsx", ".rs", ".kt", ".kts", ".scala", ".swift", ".php",
           ".cs", ".dart", ".m", ".mm"}
HASH_STYLE = {".py", ".rb"}
DOCSTRING = {".py"}


def comment_lines(text, ext):
    out = []
    for raw in text.splitlines():
        line = raw.strip()
        if not line:
            continue
        if ext in C_STYLE and (line.startswith("//") or line.startswith("/*")
                               or line.startswith("*")):
            out.append(line)
        elif ext in HASH_STYLE and line.startswith("#") and not line.startswith("#!"):
            out.append(line)
        elif ext in DOCSTRING and (line.startswith('"""') or line.startswith("'''")):
            out.append(line)
    return out


def main():
    try:
        data = json.load(sys.stdin)
    except Exception as e:
        print(f"comment-discipline: failed to parse hook input: {e}", file=sys.stderr)
        return 0

    tool = data.get("tool_name", "")
    if tool not in ("Edit", "Write", "MultiEdit"):
        return 0

    ti = data.get("tool_input", {})
    path = ti.get("file_path", "")
    dot = path.rfind(".")
    ext = path[dot:] if dot != -1 else ""
    if ext not in C_STYLE and ext not in HASH_STYLE:
        return 0

    if tool == "Write":
        new_text, old_text = ti.get("content", ""), ""
    elif tool == "Edit":
        new_text, old_text = ti.get("new_string", ""), ti.get("old_string", "")
    else:
        edits = ti.get("edits", [])
        new_text = "\n".join(e.get("new_string", "") for e in edits)
        old_text = "\n".join(e.get("old_string", "") for e in edits)

    old = comment_lines(old_text, ext)
    added = []
    for line in comment_lines(new_text, ext):
        if line in old:
            old.remove(line)
        else:
            added.append(line)

    if not added:
        return 0

    sample = "\n".join("    " + c for c in added[:5])
    more = "" if len(added) <= 5 else f"\n    … and {len(added) - 5} more"
    msg = (
        f"comment-discipline: this edit added {len(added)} comment line(s):\n"
        f"{sample}{more}\n\n"
        "Re-check each against the closed allowlist — keep ONLY if it is a "
        "hidden constraint/precondition, a workaround (with link), "
        "surprising-but-correct code, or a subtle invariant. A comment or "
        "docstring is never mandatory; delete any that merely restate WHAT the "
        "code does, echo the signature, narrate the task/PR, or just fill a "
        "bare-looking block. If a kept comment is justified, leave it as is."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": msg,
        }
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
