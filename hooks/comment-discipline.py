#!/usr/bin/env python3
"""PostToolUse hook for Edit/Write/MultiEdit.

Detects comment lines newly added by the edit and, when found, demands a
per-line verdict against the comment-discipline allowlist with DELETE as the
default. A resident prose rule competes with everything else in context and
loses; this fires only on edits that actually add comments, so it re-primes the
rule exactly when it matters. It emits decision:"block" so the verdict is a
prompt the model must answer, not background context it can skim past — an
earlier additionalContext version proved too easy to ignore.
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
        "Verdict each line now. The default verdict is DELETE — a line stays "
        "only if you can name which allowlist entry it is: hidden "
        "constraint/precondition, workaround (with link or issue), "
        "surprising-but-correct code (with the reason), or subtle invariant a "
        "reader could break. 'It explains why' is not sufficient — keep it "
        "only if a careful reader could NOT recover that why from the code "
        "itself. Anything else — restating WHAT the next lines do, echoing a "
        "signature, narrating the task or PR, filling a bare-looking block — "
        "is noise: remove it with an Edit before continuing. When in doubt, "
        "delete. Sole carve-out: a one-line contract doc on an exported "
        "identifier that lint tooling enforces. If every line clearly names "
        "its category, keep them and continue."
    )
    print(json.dumps({
        "decision": "block",
        "reason": msg,
    }))
    return 0


if __name__ == "__main__":
    sys.exit(main())
