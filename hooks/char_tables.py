"""Shared character tables for the prose-style character rule.

Imported by char-discipline.py (file edits and turn-final chat text) and gh-markdown-style.py (PR and issue bodies), so the barred set is defined once and the three surfaces can never disagree about it.
Registered as a support module in register.py, not as a hook of its own.
"""

VISIBLE = {
    "—": ("em dash", "a period, a comma, a colon, or parentheses"),
    "–": ("en dash", "a hyphen, or the word 'to' for a range"),
    "―": ("horizontal bar", "a period, a comma, or parentheses"),
    "·": ("middle dot", "a comma, or 'and' / '와' / '과'"),
    "•": ("bullet", "an ASCII '-'"),
    "◦": ("white bullet", "an ASCII '-'"),
    "‣": ("triangular bullet", "an ASCII '-'"),
    "▪": ("small black square", "an ASCII '-'"),
    "“": ("left double quotation mark", "an ASCII double quote"),
    "”": ("right double quotation mark", "an ASCII double quote"),
    "‘": ("left single quotation mark", "an ASCII apostrophe"),
    "’": ("right single quotation mark", "an ASCII apostrophe"),
    "…": ("horizontal ellipsis", "three periods"),
    "→": ("rightwards arrow", "'->', or the relation in words"),
    "←": ("leftwards arrow", "'<-', or the relation in words"),
    "⇒": ("rightwards double arrow", "'=>', or the relation in words"),
}

INVISIBLE = {
    "\u00a0": "no-break space",
    "\u202f": "narrow no-break space",
    "\u205f": "medium mathematical space",
    "\u3000": "ideographic space",
    "\u2800": "braille pattern blank",
    "\u200b": "zero width space",
    "\u200c": "zero width non-joiner",
    "\u200d": "zero width joiner",
    "\u2060": "word joiner",
    "\ufeff": "byte order mark",
    "\u00ad": "soft hyphen",
    "\u200e": "left-to-right mark",
    "\u200f": "right-to-left mark",
    "\u202e": "right-to-left override",
    "\u2061": "function application",
    "\u2062": "invisible times",
    "\u2063": "invisible separator",
    "\u2064": "invisible plus",
}
for _cp in range(0x2000, 0x200B):
    INVISIBLE.setdefault(chr(_cp), "fixed-width space")

BARRED = VISIBLE.keys() | INVISIBLE.keys()

KEEPS = (
    "a rule, doc, or fixture that names the character on purpose; quoted source "
    "text or upstream data copied as it is; an identifier or filename; punctuation "
    "the language requires; a math, unit, or currency symbol; a comparison "
    "label"
)


def describe(ch):
    """Return (label, replacement) for one barred character."""
    if ch in VISIBLE:
        name, fix = VISIBLE[ch]
        return f"'{ch}' {name} (U+{ord(ch):04X})", fix
    return f"{INVISIBLE[ch]} (U+{ord(ch):04X}, invisible)", "a plain ASCII space, or nothing"


def strip_fences(text):
    """Drop fenced code blocks, which hold quoted commands and file content verbatim."""
    out, fence = [], False
    for line in text.splitlines():
        if line.lstrip().startswith(("```", "~~~")):
            fence = not fence
            continue
        if not fence:
            out.append(line)
    return out


def scan(lines):
    """Count barred characters per codepoint and keep one sample line for each."""
    counts, samples = {}, {}
    for line in lines:
        for ch in set(line) & BARRED:
            counts[ch] = counts.get(ch, 0) + line.count(ch)
            samples.setdefault(ch, line.strip()[:120])
    return counts, samples


def report(counts, samples, sample_limit=3):
    """Render the per-character findings block, heaviest first."""
    lines, shown = [], 0
    for ch in sorted(counts, key=lambda c: -counts[c]):
        label, fix = describe(ch)
        lines.append(f"    {label} x{counts[ch]} -> write {fix}")
        if ch in VISIBLE and shown < sample_limit:
            lines.append(f"        seen in: {samples[ch]}")
            shown += 1
    return "\n".join(lines)
